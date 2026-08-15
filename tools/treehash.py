#!/usr/bin/env python3
"""Version-identity digest over an ENTIRE bot directory, not just main.py.

Why this exists: every tape row, pre-ship check, and HANDOVER STATE block has
identified a bot version by `md5 main.py`. That was fine while every bot was
one file. Now that we ship multi-file bots (e.g. bots/_v103split/ = main.py +
doctrine.py), `md5 main.py` silently stops being a version identity: two bots
with identical main.py but different doctrine.py hash the same and look like
the same version on the tape.

This hashes every file that actually ships in the bot zip, keyed by
(relative path, content), so a change anywhere in the shipped bundle --
including a same-content file renamed, or a second file added -- changes the
digest.

File set matches `fcode submission upload`'s packaging exactly (measured
against the installed fcode 2.3.6 CLI,
.venv/lib/python3.13/site-packages/fcode/commands/submission.py:_make_zip /
_is_junk, 2026-08-09): a directory walk that drops __pycache__ and a longer
list of junk dirs/files (.git, .DS_Store, editor/VCS caches, etc.) and any
*.pyc/*.pyo. See _JUNK_DIRS / _JUNK_FILES / _JUNK_EXTENSIONS below -- kept
as a literal copy of the CLI's lists, not a guess, because a mismatch here
would make the digest lie about what ships. If the installed fcode version's
packaging logic changes, re-diff this against it.

Usage:
    .venv/bin/python tools/treehash.py bots/_v103split
    .venv/bin/python tools/treehash.py bots/_v103split bots/_v100hf bots/_v89sh
    .venv/bin/python tools/treehash.py bots/_v100hf --legacy   # single-file bot: also print md5(main.py)
    .venv/bin/python tools/treehash.py bots/_v103split --full  # print the full digest, not the 8-char short form
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

# Copied verbatim from fcode 2.3.6's fcode/commands/submission.py so the file
# set this tool hashes matches the file set `fcode submit`/`fcode submission
# upload` actually zips. Do not hand-edit these without re-checking the
# installed fcode version's _make_zip/_is_junk.
_JUNK_DIRS = {
    "__pycache__",
    ".git",
    ".svn",
    ".hg",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__MACOSX",
    ".tox",
    ".eggs",
    ".nox",
}

_JUNK_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    ".thumbs",
    "ehthumbs.db",
    "ehthumbs_vista.db",
    ".Spotlight-V100",
    ".Trashes",
    ".directory",
}

_JUNK_EXTENSIONS = {".pyc", ".pyo"}

SHORT_LEN = 8


def _is_junk(relpath: Path) -> bool:
    if relpath.name in _JUNK_FILES or relpath.name.startswith("._"):
        return True
    if relpath.suffix in _JUNK_EXTENSIONS:
        return True
    return any(part in _JUNK_DIRS for part in relpath.parts)


def shipped_files(bot_dir: Path) -> list[Path]:
    """Relative paths (sorted) of every file that would land in the zip
    `fcode submit` builds from bot_dir. Sorted so the caller's hash is
    order-independent regardless of the filesystem's readdir order."""
    out = []
    for path in bot_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(bot_dir)
        if _is_junk(rel):
            continue
        out.append(rel)
    out.sort(key=lambda p: p.as_posix())
    return out


def tree_hash(bot_dir: Path) -> str:
    """One digest over every shipped file's (relpath, content), order-independent.

    Feeds `relpath + NUL + content` per file into a single running hash, files
    taken in sorted-relpath order. NUL-separating path from content, and
    including the path at all, means a same-byte file that's renamed (or a
    file moved between subdirs) changes the digest -- not just content drift.
    """
    h = hashlib.sha256()
    for rel in shipped_files(bot_dir):
        h.update(rel.as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update((bot_dir / rel).read_bytes())
    return h.hexdigest()


def legacy_md5_main(bot_dir: Path) -> str | None:
    """The old identity: md5 of main.py alone. None if there's no main.py."""
    main_py = bot_dir / "main.py"
    if not main_py.is_file():
        return None
    return hashlib.md5(main_py.read_bytes()).hexdigest()


def is_single_file_bot(bot_dir: Path) -> bool:
    """True iff main.py is the only shipped file (legacy md5-main-py bots)."""
    files = shipped_files(bot_dir)
    return files == [Path("main.py")]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bot_dirs", nargs="+", help="One or more bot directories.")
    ap.add_argument("--full", action="store_true",
                     help="Print the full digest instead of the 8-char short form.")
    ap.add_argument("--legacy", action="store_true",
                     help="Also print the legacy md5(main.py) value, for cross-walking old tape rows.")
    args = ap.parse_args()

    multi = len(args.bot_dirs) > 1
    exit_code = 0
    for raw in args.bot_dirs:
        bot_dir = Path(raw)
        if not bot_dir.is_dir():
            print(f"error: not a directory: {bot_dir}", file=sys.stderr)
            exit_code = 1
            continue
        digest = tree_hash(bot_dir)
        short = digest[:SHORT_LEN]
        shown = digest if args.full else short

        line = f"{shown}\t{raw}" if multi else shown
        print(line)

        if args.legacy:
            legacy = legacy_md5_main(bot_dir)
            if legacy is None:
                print(f"  legacy md5(main.py): n/a (no main.py in {raw})", file=sys.stderr)
            else:
                note = "" if is_single_file_bot(bot_dir) else " (bot has extra files -- legacy value under-identifies it)"
                print(f"  legacy md5(main.py): {legacy}{note}", file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
