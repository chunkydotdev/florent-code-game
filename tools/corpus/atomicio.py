#!/usr/bin/env python3
"""Atomic file writes for the corpus — temp file in the destination directory,
flush + fsync, then `os.replace`.

⛔ WHY THIS EXISTS (2026-08-17, s50). Every table the keeper rebuilds was written
IN PLACE: `open(path, "w")` truncates the file to zero and then refills it over
seconds, and `Path.write_text` does the same. `corpus/meta_join.tsv` is 24 MB, so
its rewrite is a multi-second window during which the file on disk is a VALID
TSV that is simply SHORT — header present, rows well formed, row count wrong.
The research lane read it inside that window overnight and silently lost 62% of
the joins. **Nothing raised.** A truncated TSV parses; that is exactly why this
class of bug is invisible and why the fix has to be in the WRITER — no reader
check can distinguish "the table is short" from "the corpus is short".

`os.replace` is atomic within a filesystem (POSIX `rename(2)`): a reader either
opens the OLD complete inode or the NEW complete inode, never a partial one, and
a reader that already has the old file open keeps reading it to the end. Hence
the temp file MUST be created in the DESTINATION DIRECTORY — a temp in /tmp is a
different filesystem, `os.replace` degrades to a copy, and the atomicity is gone.

WHAT THIS DOES **NOT** COVER: appends. `sync.py` appends decoded rows to
`events.tsv` et al. and the keeper appends lines to `keeper.log`. An append never
truncates, so the 62% class cannot happen there; the residual is a reader seeing
a torn final line, which costs one row and is visible as a short row rather than
a short table. Converting an append into a rewrite of a 999 MB table to close
that would be the worse trade.

    from atomicio import atomic_write_text, atomic_open   # same directory

    atomic_write_text(path, body)
    with atomic_open(path) as fh:      # fh is a normal text handle
        fh.write(...)                  # rename happens on clean exit only
"""
from __future__ import annotations

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0. This is a LIBRARY,
# but the sweep globs `tools/corpus/*.py` and a library with no stdout fails its
# assertion (2) exactly as a broken tool would.
# ⛔ GATED ON `__main__`: this module is IMPORTED by keeper/sync/meta_attrib.
# Ungated, it would fire during that import and make the PARENT exit 0 mid-run.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import gzip
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

# Mode for a freshly created corpus table. Source: the existing corpus files,
# `ls -l corpus/` on 2026-08-17 — every *.tsv is `-rw-r--r--` (0644). mkstemp
# creates 0600, so without this every atomically-written table would silently
# become unreadable to any other account/process that reads the corpus.
_DEFAULT_MODE = 0o644


def _tmp_for(path: Path) -> tuple[int, str]:
    """A temp fd in the DESTINATION DIRECTORY (see module docstring: a temp on
    another filesystem makes os.replace a non-atomic copy).

    Dot-prefixed so a `glob("*")` sweep — tests/test_instruments.py's
    `_fs_signature` — does not see the transient file and attribute it to
    whatever tool is under test.

    ⛔ THE TEMP KEEPS THE DESTINATION'S SUFFIX (`.tsv`, not `.tmp`), because
    `replay_census.guard_out` REFUSES an output path that is an existing
    non-`.tsv` file — the guard that exists because a decoder once opened a
    replay "w" and destroyed it. A `.tmp` temp handed to a decoder as its output
    argv trips that guard on every run.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return tempfile.mkstemp(dir=str(path.parent), prefix="." + path.name + ".",
                            suffix=path.suffix or ".tmp")


def _finish(tmp: str, path: Path) -> None:
    try:
        os.chmod(tmp, path.stat().st_mode & 0o7777)   # keep the existing mode
    except OSError:
        os.chmod(tmp, _DEFAULT_MODE)
    os.replace(tmp, path)


@contextmanager
def atomic_open(path, mode: str = "w", **kw):
    """Write `path` through a temp file; rename only on a clean exit.

    An exception inside the block leaves the ORIGINAL file untouched and removes
    the temp — which is the second half of why this matters: the in-place form
    left a HALF-WRITTEN table on disk when a writer died mid-run, and that file
    then looked exactly like a complete one.
    """
    path = Path(path)
    if "a" in mode or "r" in mode or "+" in mode:
        raise ValueError(f"atomic_open is for whole-file writes, not {mode!r}; "
                         "an append must not be turned into a rewrite")
    fd, tmp = _tmp_for(path)
    try:
        with os.fdopen(fd, mode, **kw) as fh:
            yield fh
            fh.flush()
            os.fsync(fh.fileno())
        _finish(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_text(path, text: str, encoding: str = "utf-8") -> Path:
    """`Path.write_text` with the truncation window removed."""
    path = Path(path)
    with atomic_open(path, "w", encoding=encoding) as fh:
        fh.write(text)
    return path


def atomic_write_gzip(path, text: str) -> Path:
    """Same contract for the committed `.gz` siblings. A truncated gzip at least
    RAISES on read, unlike a truncated TSV — but a stale-and-valid sibling beats
    a corrupt one, and the cost is identical."""
    path = Path(path)
    fd, tmp = _tmp_for(path)
    try:
        with os.fdopen(fd, "wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw) as gz:
                gz.write(text.encode())
            raw.flush()
            os.fsync(raw.fileno())
        _finish(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


@contextmanager
def atomic_subprocess_target(path):
    """For a writer that is a SUBPROCESS writing to a path (stdout redirect or
    an output argv). Yields the temp path; renames it over `path` on clean exit.

    ⛔ The caller must still decide whether the subprocess SUCCEEDED — this only
    guarantees that no reader sees the file half-built. Renaming a temp that a
    failed decoder left short is the same defect one layer down.
    """
    path = Path(path)
    fd, tmp = _tmp_for(path)
    os.close(fd)
    try:
        yield Path(tmp)
        _finish(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
