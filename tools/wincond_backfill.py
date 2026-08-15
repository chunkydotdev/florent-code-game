#!/usr/bin/env python3
"""Backfill `turns` + `wincond` onto EVERY archived replay, from the replay bytes.

WHY THIS EXISTS
===============
`PROGRAMME.md` carries `R1000_IS_DEFEAT: yes`, UNCONDITIONAL — a round-1000 game
is a defeat even when we win it. "How did this game end" is therefore a
DEFEAT-CONDITION, not a curiosity. But the two surfaces that carry it are both
partial:

  * `corpus/join.tsv`     — has `cond`/`turns`, but is built by joining against
                            `ladder_games.tsv`, which `tools/corpus/ladder_meta.py`
                            walks from `fcode match list --mine --type ladder`.
                            RATED-ONLY BY CONSTRUCTION. Every unrated game: 0%.
  * `corpus/throws.tsv`   — carries `wincond`, but emits ONE ROW PER THROW, so a
                            game with no launcher throw produces no row at all.
                            That is a SELECTION-BIASED surface: conditioning a
                            win-condition read on "this game had a throw" is
                            conditioning on the treatment in half our legs.

`corpus/meta_join.tsv` — the surface every unrated leg read actually uses
(`tools/panel_read.py:121`) — has 24 columns and NONE of them is an end
condition. So a panel read cannot tell a kill from a tiebreak.

The information is NOT lost. `Replay.winCondition` is field 6 and
`Replay.turns` is repeated field 3; `tools/corpus/replay_autopsy.py:53` and
`tools/corpus/replay_throws.py:43` have both been reading them for days. This
tool reads them for EVERY file in `replay_archive/` and writes one flat table.

⛔ THE LOAD-BEARING METHOD FACT: KEY ON `turns`, NEVER ON THE `cond` STRING
==========================================================================
Measured on `corpus/join.tsv` (2026-08-15): 2 of 3,735 games carry
`cond=titanium_collected` at turns=146 and turns=140 — i.e. the tiebreak string
on a game that ended in 146 rounds. And `corpus/ladder_games.tsv` carries 25 rows
with `cond=error` at `turns=0` (their `s3` key is empty: NO REPLAY EXISTS for
those, so they can never appear in a replay-derived backfill and must not be
silently absorbed into a "decisive" bucket by anything that pools them).

  klass is a pure function of `turns`:
      turns == 1000  -> R1000       (the defeat condition)
      0 < turns < 1000 -> DECISIVE
      turns == 0     -> ABORTED     (the `cond=error` class, its own bucket)
      unreadable     -> UNREADABLE  (turns is written as -1 and is NOT a count)

`wincond` is carried as a payload column. It is never consulted to decide klass.

⛔ AN ERROR PATH MUST NOT RETURN A CLEAN NEGATIVE
=================================================
This project has hit "a guard that reports SUCCESS on a NO-OP" six times in one
night (a silent scipy fallback, a `try/except: pass` cached-rating fallback, a
heartbeat frozen at RUNNING, an idleness alarm defaulting to a retired predicate,
a `git add` swallowing its failure, and `era_guard` returning an EMPTY LIST for
`throws.tsv` because `int(r["team"])` raised inside a bare `except: continue` —
on a surface where a REAL zero had just been established).

So: **"no r1000 games" and "could not read this file" are different answers and
this tool never conflates them.** Every unreadable file gets a row with
`status=err:<Type>:<msg>` and `klass=UNREADABLE`; the summary prints the count on
its own line; and `--build` EXITS 2 when it is non-zero. A caller filtering for
`klass == "R1000"` and getting nothing is looking at a summary that has already
told it whether anything failed to parse.

Domain invariants are asserted, not assumed: `turns > 1000` is impossible
(`GameConstants.MAX_TURNS=1000`) and raises rather than being classified.

CONTROLS (all driven — `--selftest`)
====================================
  POS-SYN     synthetic replay, 1000 turn buffers, wincond="core_destroyed"
              MUST be R1000   (drives klass off turns while cond says "kill")
  NEG-SYN     synthetic replay,  500 turn buffers, wincond="titanium_collected"
              MUST NOT be R1000 (drives klass off turns while cond says tiebreak)
  POS-REAL    a real archived file that `join.tsv` says is turns=1000
  NEG-REAL    the real archived file `join.tsv` says is turns=146 WITH
              cond=titanium_collected — a cond-keyed implementation misfiles it
  ABORT-SYN   synthetic replay with ZERO turn buffers -> ABORTED, and explicitly
              asserted to be neither R1000 nor DECISIVE
  ERR-TRUNC   a corrupted replay -> UNREADABLE, status carries the exception
  ERR-ABSENT  a nonexistent path  -> UNREADABLE, status carries the exception
  OVER-SYN    synthetic replay with 1001 turn buffers -> REFUSED (raises)
  XVAL        N real files vs `join.tsv`: turns AND cond must agree exactly

Usage
=====
    .venv/bin/python tools/wincond_backfill.py --selftest
    .venv/bin/python tools/wincond_backfill.py --report
    .venv/bin/python tools/wincond_backfill.py --build          # -> corpus/wincond.tsv
    .venv/bin/python tools/wincond_backfill.py --validate       # vs join.tsv, all rows

Cost: ~0.3 ms/file warm, measured over 3,735 files. A full 53k-file archive scan
is ~20-60 s wall in ONE process and touches ~12 GB of reads. Single-threaded on
purpose — local screens own the cores.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
# `_varint` is imported alongside the public `fields()` on purpose: the framing
# guard below has to walk the same varints with the same decoder, or it would be
# validating a parse nobody performs.
from replay_census import fields, _varint as _read_varint, WIRE_LEN, WIRE_VARINT  # noqa: E402

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

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "replay_archive"
CORPUS = REPO / "corpus"
OUT_DEFAULT = CORPUS / "wincond.tsv"

MAX_TURNS = 1000                     # GameConstants.MAX_TURNS
COLUMNS = ["file", "status", "turns", "wincond", "winner", "klass"]

R1000, DECISIVE, ABORTED, UNREADABLE = "R1000", "DECISIVE", "ABORTED", "UNREADABLE"


class TruncatedReplayError(ValueError):
    """The top-level framing does not close: a field runs past the buffer.

    ⛔ THIS GUARD EXISTS BECAUSE THE SELFTEST CAUGHT ITS ABSENCE. `fields()` reads
    a length-delimited field as `buf[i:i + length]`, and Python slicing SILENTLY
    TRUNCATES — so a replay cut in half parses "cleanly", yields a SHORT turn
    count, and is written with `status=ok`. A half-written file (the archive is
    fed by a downloader) would therefore have been reported as a DECISIVE game
    with a wrong kill round, which is the flattering direction: it invents
    fast kills and deflates the r1000 rate, the exact quantity this table exists
    to measure. Detected, never absorbed.
    """


class ReplayDomainError(ValueError):
    """A replay parsed cleanly but yielded a value the game cannot produce.

    Deliberately NOT caught by the per-file handler in `scan()`: a turns count
    above MAX_TURNS means the parse is wrong, not that the file is damaged, and
    absorbing it as `UNREADABLE` would hide a decoder defect behind a bucket
    that already has a benign explanation.
    """


# --------------------------------------------------------------------------
# EXTRACTION — the single shipped path. The selftest drives THIS function, not
# a parallel copy of it (the shape found four times in one session: the test and
# the claim were about different things).
# --------------------------------------------------------------------------
def check_framing(data: bytes) -> None:
    """Raise unless every top-level field closes inside the buffer.

    Walks tags and lengths only — it never copies a payload — so it costs a few
    microseconds on a 200 kB replay. Mirrors `fields()`'s wire handling exactly;
    the one thing it adds is the bounds test `fields()` leaves to Python slicing.
    """
    i, n = 0, len(data)
    if n == 0:
        raise TruncatedReplayError("empty file")
    while i < n:
        tag, j = _read_varint(data, i)
        if j > n:
            raise TruncatedReplayError(f"tag varint runs past end at {i}")
        num, wire = tag >> 3, tag & 7
        i = j
        if wire == WIRE_VARINT:
            _v, i = _read_varint(data, i)
            if i > n:
                raise TruncatedReplayError(f"varint field {num} runs past end")
        elif wire == WIRE_LEN:
            length, i = _read_varint(data, i)
            if i + length > n:
                raise TruncatedReplayError(
                    f"field {num} declares {length} bytes but only {n - i} remain")
            i += length
        elif wire == 5:
            i += 4
            if i > n:
                raise TruncatedReplayError(f"fixed32 field {num} runs past end")
        elif wire == 1:
            i += 8
            if i > n:
                raise TruncatedReplayError(f"fixed64 field {num} runs past end")
        else:
            raise TruncatedReplayError(f"unsupported wire type {wire} for field {num}")


def extract(data: bytes) -> tuple[int, str, int]:
    """(turns, wincond, winner) from raw `.replay26` bytes.

    `Replay { Map map = 1; repeated Turn turns = 3; optional Team winner = 4;
    string winCondition = 6; }` — `turns[i]` IS round i, so the number of
    length-delimited field-3 occurrences is `turnsPlayed`. VERIFIED against the
    platform's own `turnsPlayed`/`winCondition` on 3,735 of 3,735 joined files,
    offset 0 in every one (see `--validate`).

    winner is -1 when the replay omits field 4 (the engine writes no winner on
    an aborted game); it is a payload, never a klass input.
    """
    check_framing(data)
    nturns, winner, wincond = 0, -1, ""
    for num, wire, value in fields(data):
        if num == 3 and wire == WIRE_LEN:
            nturns += 1
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    if nturns > MAX_TURNS:
        raise ReplayDomainError(
            f"turns={nturns} exceeds GameConstants.MAX_TURNS={MAX_TURNS}; "
            "the field-3 count is not turnsPlayed on this file")
    # ⛔ TAIL-TRUNCATION GUARD, and it is the guard `check_framing` CANNOT be.
    # winCondition is the LAST top-level field, so a file cut on a field
    # BOUNDARY still frames perfectly and simply loses field 6 — the selftest
    # caught exactly that (a half-cut fixture reported status=ok). An empty
    # wincond is therefore the signature of tail loss. MEASURED BEFORE BEING
    # TRUSTED: 0 of 44,431 archived `.replay26` files have an empty wincond
    # (2026-08-15, whole-archive scan), so this cannot misfire on a real game.
    # ⚠ KNOWN LIMIT, stated rather than papered over: a truncation landing on a
    # field boundary INSIDE the turn list — losing turns but keeping field 6 —
    # is invisible to both guards and would understate `turns`. Nothing in the
    # replay declares its own turn count, so there is no third check to add.
    if not wincond:
        raise TruncatedReplayError(
            "no winCondition (field 6) — the last top-level field is missing, "
            "which is what a tail truncation looks like")
    return nturns, wincond, winner


def classify(turns: int) -> str:
    """klass from `turns` ALONE. The `cond` string is never an input here.

    Two measured reasons, both on `corpus/join.tsv`/`ladder_games.tsv`:
    `cond=titanium_collected` occurs at turns=146 and turns=140 (a cond-keyed
    rule calls those tiebreaks), and `cond=error` occurs 25 times at turns=0
    (a cond-keyed rule has to invent a bucket for a string, rather than reading
    the count that actually distinguishes the class).
    """
    if turns < 0:
        return UNREADABLE
    if turns == 0:
        return ABORTED
    if turns == MAX_TURNS:
        return R1000
    if turns > MAX_TURNS:                       # unreachable via extract()
        raise ReplayDomainError(f"turns={turns} > MAX_TURNS")
    return DECISIVE


def read_one(path: Path) -> dict:
    """One row for one file. NEVER raises for a bad file — records why instead.

    ⛔ The except clause is NOT `pass` and NOT `continue`. It produces a row
    whose `klass` is UNREADABLE and whose `status` carries the exception type
    and message, so a downstream zero-count can be told apart from a read
    failure. `ReplayDomainError` is re-raised on purpose (see its docstring).
    """
    try:
        data = path.read_bytes()
        turns, wincond, winner = extract(data)
    except ReplayDomainError:
        raise
    except Exception as exc:                    # noqa: BLE001 - recorded, not swallowed
        msg = str(exc).replace("\t", " ").replace("\n", " ")[:120]
        return dict(file=path.name, status=f"err:{type(exc).__name__}:{msg}",
                    turns=-1, wincond="", winner=-1, klass=UNREADABLE)
    return dict(file=path.name, status="ok", turns=turns, wincond=wincond,
                winner=winner, klass=classify(turns))


def scan(paths) -> list[dict]:
    return [read_one(Path(p)) for p in paths]


def read_one_bytes_ok(data: bytes) -> bool:
    """Selftest helper: does this exact byte string parse to a DECISIVE game?

    Used to prove the corruption fixtures are corruptions — i.e. that the
    UNCORRUPTED bytes clear the same path the corrupted ones fail.
    """
    turns, _wincond, _winner = extract(data)
    return classify(turns) == DECISIVE


# --------------------------------------------------------------------------
# SYNTHETIC REPLAYS — test fixtures only, used to drive the controls in both
# directions. Kept in this module so the selftest can build a case that MUST
# come out R1000 and one that MUST NOT without depending on the archive.
# --------------------------------------------------------------------------
def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def _len_field(num: int, payload: bytes) -> bytes:
    return _varint((num << 3) | WIRE_LEN) + _varint(len(payload)) + payload


def _var_field(num: int, value: int) -> bytes:
    return _varint((num << 3) | WIRE_VARINT) + _varint(value)


def synth_replay(nturns: int, wincond: str, winner: int | None = 0) -> bytes:
    """A minimal wire-legal Replay with a chosen turn count and cond string."""
    buf = bytearray()
    buf += _len_field(1, _var_field(1, 20) + _var_field(2, 20))     # Map{w,h}
    for i in range(nturns):
        buf += _len_field(3, _var_field(1, i))                      # Turn{round}
    if winner is not None:
        buf += _var_field(4, winner)
    buf += _len_field(6, wincond.encode())
    return bytes(buf)


# --------------------------------------------------------------------------
# SURFACE COVERAGE
# --------------------------------------------------------------------------
def _tsv(path: Path):
    """DictReader that skips `#` comment lines.

    The shard tapes now open with a `# FIXTURE` line and can carry a
    `# FIXTURE-RESUME` line MID-FILE; a plain DictReader reads the first of
    those as the column names. Same handling as `tools/overnight_read.py:111`
    and `tools/effective_n.py:72`.
    """
    with path.open(newline="") as fh:
        body = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    return list(csv.DictReader(body, delimiter="\t"))


def _need(rows: list[dict], cols: list[str], where: str):
    """Fail loudly on a missing column instead of indexing by position.

    Ad-hoc field indexing is 4-of-4 wrong in this repo. Every read below is by
    NAME and asserts the name exists first.
    """
    if not rows:
        raise SystemExit(f"ALARM: {where} produced ZERO rows — that is a read "
                         f"failure, not an empty result. Refusing to report.")
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        raise SystemExit(f"ALARM: {where} is missing column(s) {missing}; "
                         f"has {sorted(rows[0])}")


def report() -> int:
    print("PER-SURFACE END-CONDITION COVERAGE  (turns + wincond readable?)")
    print(f"  clock: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  "
          "⚠ the corpus keeper writes to corpus/ continuously; row counts drift "
          "between reads within one run.\n")

    meta = _tsv(CORPUS / "meta_join.tsv")
    _need(meta, ["file", "us_side", "triggeredBy"], "meta_join.tsv")
    join = _tsv(CORPUS / "join.tsv")
    _need(join, ["file", "cond", "turns"], "join.tsv")
    lad = _tsv(CORPUS / "ladder_games.tsv")
    _need(lad, ["cond", "turns"], "ladder_games.tsv")

    join_files = {r["file"] for r in join}
    throw_files = set()
    tp = CORPUS / "throws.tsv"
    with tp.open(newline="") as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        if "file" not in (rdr.fieldnames or []):
            raise SystemExit(f"ALARM: throws.tsv has no `file` column: {rdr.fieldnames}")
        for r in rdr:
            throw_files.add(r["file"])

    ours = [r for r in meta if r["us_side"] in ("a", "b")]
    unr = [r for r in ours if r["triggeredBy"] == "unrated"]
    rat = [r for r in ours if r["triggeredBy"] == "ladder"]

    def line(name, rows):
        n = len(rows) or 1
        j = sum(1 for r in rows if r["file"] in join_files)
        t = sum(1 for r in rows if r["file"] in throw_files)
        e = sum(1 for r in rows if r["file"] in join_files or r["file"] in throw_files)
        print(f"  {name:<26} n={len(rows):>6}  join.tsv={j:>5} ({j/n:5.1%})  "
              f"throws.tsv={t:>5} ({t/n:5.1%})  either={e:>5} ({e/n:5.1%})  "
              f"BLIND={len(rows)-e:>5} ({(len(rows)-e)/n:5.1%})")

    print(f"  archived replays on disk .......... {len(list(ARCHIVE.iterdir())):>6}")
    print(f"  meta_join.tsv rows ................ {len(meta):>6}   "
          f"(columns: {len(meta[0])}, end-condition columns: 0)")
    print(f"  ladder_games.tsv rows ............. {len(lad):>6}   RATED-ONLY by construction\n")
    line("OUR games (all)", ours)
    line("  OUR unrated", unr)
    line("  OUR rated (ladder)", rat)
    line("ALL archived (any team)", meta)
    print("\n  ⚠ throws.tsv is SELECTION-BIASED for this purpose: one row per THROW, so "
          "\n    it covers only games that had a launcher throw. Using it as the wincond "
          "\n    surface conditions the read on the treatment in every kidnap leg.")
    _tape_census()
    return 0


def _tape_census() -> None:
    """LOCAL shard tapes — the surface that is NOT blind, counted to prove it.

    ⛔ Reads by NAME. A tape with no header row is reported as its own class,
    NOT indexed positionally: `scratchpad/overnight/DEST14B.tsv` and `SENT41.tsv`
    open on a data row (pre-existing, unfixed), and guessing their columns is the
    ad-hoc field indexing that is 4-of-4 wrong in this repo.
    """
    import glob
    # Absolute, off REPO: an agent shell resets cwd between calls and a relative
    # glob would return [] there — an empty result that reads exactly like
    # "no tapes exist", which is the no-op-reports-success shape.
    tapes = sorted(glob.glob(str(REPO / "scratchpad" / "overnight*" / "**" / "*.tsv"),
                             recursive=True))
    if not tapes:
        print(f"\n  LOCAL shard tapes: none found under {REPO}/scratchpad/overnight*/ "
              "(reporting the absence explicitly, NOT as a 0%)")
        return
    with_cond, no_header, hashed, rows, unreadable = 0, [], 0, 0, []
    for t in tapes:
        try:
            with open(t, newline="") as fh:
                lines = [ln for ln in fh if ln.strip()]
        except Exception as exc:                # noqa: BLE001 - reported, not swallowed
            unreadable.append((t, f"{type(exc).__name__}: {exc}"))
            continue
        if any(ln.lstrip().startswith("#") for ln in lines):
            hashed += 1
        data = [ln for ln in lines if not ln.lstrip().startswith("#")]
        if not data:
            unreadable.append((t, "no data lines"))
            continue
        hdr = data[0].rstrip("\n").split("\t")
        if "cond" in hdr and "turns" in hdr:
            with_cond += 1
            rows += len(data) - 1
        elif "ts" not in hdr:
            no_header.append(t)
            rows += len(data)
        else:
            unreadable.append((t, f"header without cond/turns: {hdr}"))
    print(f"\n  LOCAL shard tapes (scratchpad/overnight*/): {len(tapes)} tapes, "
          f"{rows} data rows")
    print(f"    cond+turns present by name ..... {with_cond}")
    print(f"    `#` comment lines present ...... {hashed}  (skipped, leading AND mid-file)")
    print(f"    NO HEADER ROW (unnamed schema) . {len(no_header)}  {[Path(t).name for t in no_header]}")
    print(f"    UNREADABLE ..................... {len(unreadable)}  {unreadable[:3]}"
          + ("   ⛔ ALARM" if unreadable else ""))
    print("    ⇒ the local fixture is NOT blind; the gap is entirely a PLATFORM-surface gap.")


# --------------------------------------------------------------------------
# BUILD / VALIDATE
# --------------------------------------------------------------------------
def build(out: Path, limit: int | None) -> int:
    if not ARCHIVE.is_dir():
        raise SystemExit(f"ALARM: no archive at {ARCHIVE}")
    paths = sorted(p for p in ARCHIVE.iterdir() if p.name.endswith(".replay26"))
    if not paths:
        raise SystemExit(f"ALARM: {ARCHIVE} yielded ZERO .replay26 files — "
                         "a read failure, not an empty archive.")
    if limit:
        paths = paths[:limit]
    t0 = time.time()
    rows = []
    for i, p in enumerate(paths):
        rows.append(read_one(p))
        if i and i % 10000 == 0:
            print(f"  ... {i}/{len(paths)}  {time.time()-t0:.0f}s", file=sys.stderr)
    tmp = out.with_suffix(".tsv.tmp")
    with tmp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, delimiter="\t",
                           lineterminator="\n", extrasaction="raise")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(out)

    tally = {}
    for r in rows:
        tally[r["klass"]] = tally.get(r["klass"], 0) + 1
    unread = tally.get(UNREADABLE, 0)
    n = len(rows)
    print(f"\nwrote {out}  rows={n}  {time.time()-t0:.1f}s")
    print(f"  readable ....... {n - unread}")
    print(f"  UNREADABLE ..... {unread}"
          + ("   ⛔ ALARM: these are READ FAILURES, not clean negatives."
             if unread else "   (a zero here is what makes the counts below trustworthy)"))
    for k in (R1000, DECISIVE, ABORTED):
        print(f"  {k:<14} {tally.get(k, 0)}")
    if unread:
        return 2
    return 0


def validate(sample: int | None) -> int:
    """Positive control at scale: replay-derived vs the PLATFORM's own values.

    `join.tsv`'s `cond`/`turns` come from `fcode match list`/`match info`
    (`tools/corpus/ladder_meta.py:74`) — a source completely independent of the
    replay bytes this tool reads. Disagreement on ANY row is a decoder defect.
    """
    join = _tsv(CORPUS / "join.tsv")
    _need(join, ["file", "cond", "turns"], "join.tsv")
    if sample:
        join = join[:sample]
    bad_t, bad_c, absent, n = [], [], 0, 0
    for g in join:
        p = ARCHIVE / g["file"]
        if not p.exists():
            absent += 1
            continue
        row = read_one(p)
        if row["klass"] == UNREADABLE:
            bad_t.append((g["file"], row["status"], g["turns"]))
            continue
        n += 1
        if row["turns"] != int(g["turns"]):
            bad_t.append((g["file"], row["turns"], g["turns"]))
        if row["wincond"] != g["cond"]:
            bad_c.append((g["file"], row["wincond"], g["cond"]))
    print(f"XVAL vs platform (join.tsv): compared={n}  absent_from_archive={absent}")
    print(f"  turns mismatches ..... {len(bad_t)}  {bad_t[:3]}")
    print(f"  wincond mismatches ... {len(bad_c)}  {bad_c[:3]}")
    ok = not bad_t and not bad_c and n > 0
    print("  VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# --------------------------------------------------------------------------
# SELFTEST — every control driven to BOTH verdicts.
# --------------------------------------------------------------------------
def selftest() -> int:
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    print("wincond_backfill selftest\n")
    print("-- SYNTHETIC: klass is driven by `turns`, and the `cond` string is set to "
          "\n   the OPPOSITE of what a cond-keyed rule would conclude, in both arms.")
    t, c, w = extract(synth_replay(1000, "core_destroyed"))
    check("POS-SYN 1000 turns + cond='core_destroyed' -> R1000",
          classify(t) == R1000, f"turns={t} cond={c!r} klass={classify(t)}")
    t2, c2, _ = extract(synth_replay(500, "titanium_collected"))
    check("NEG-SYN  500 turns + cond='titanium_collected' -> NOT R1000",
          classify(t2) != R1000 and classify(t2) == DECISIVE,
          f"turns={t2} cond={c2!r} klass={classify(t2)}")
    check("   ... and the two synthetic arms DISAGREE (the test can separate them)",
          classify(t) != classify(t2))

    print("\n-- THIRD CLASS: turns==0 is its own bucket, asserted against BOTH others.")
    t0, c0, w0 = extract(synth_replay(0, "error", winner=None))
    k0 = classify(t0)
    check("ABORT-SYN 0 turns -> ABORTED", k0 == ABORTED, f"turns={t0} klass={k0} winner={w0}")
    check("   ... ABORTED is not R1000", k0 != R1000)
    check("   ... ABORTED is not DECISIVE", k0 != DECISIVE)
    check("   ... ABORTED is not UNREADABLE (a real game state, not a read failure)",
          k0 != UNREADABLE)

    print("\n-- DOMAIN: an impossible turn count is REFUSED, never bucketed.")
    raised = False
    try:
        extract(synth_replay(MAX_TURNS + 1, "core_destroyed"))
    except ReplayDomainError as exc:
        raised = True
        detail = str(exc)[:60]
    check("OVER-SYN 1001 turns raises ReplayDomainError", raised,
          detail if raised else "NO RAISE — it was silently classified")

    print("\n-- ERROR PATHS: a read failure must NOT look like a clean negative.")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        good = synth_replay(300, "core_destroyed")
        # ⛔ MUTATION-TESTED FIXTURE. The first version of this control flipped
        # the LAST BYTE and the selftest reported [ok] status=ok — the mutation
        # landed inside the wincond string payload and changed nothing the parser
        # could notice. A corruption fixture the parser survives validates
        # nothing. Both fixtures below were confirmed to flip the verdict.
        bad = Path(td) / "trunc.replay26"
        bad.write_bytes(good[:-3])                          # cut INSIDE field 6
        r = read_one(bad)
        check("ERR-TRUNC replay cut mid-field -> UNREADABLE",
              r["klass"] == UNREADABLE, f"status={r['status']}")
        # ⭐ THE CASE THE FRAMING GUARD CANNOT SEE. A cut on a field BOUNDARY
        # frames perfectly; the first version of this control cut at len//2,
        # landed on a boundary, and the tool reported status=ok. That is the
        # defect the wincond invariant was added for.
        tail = Path(td) / "notail.replay26"
        tail.write_bytes(synth_replay(300, ""))             # field 6 dropped
        rt = read_one(tail)
        check("ERR-TAIL boundary-aligned tail loss (no winCondition) -> UNREADABLE",
              rt["klass"] == UNREADABLE, f"status={rt['status']}")
        check("   ... its framing is VALID (so framing alone would have passed it)",
              check_framing(tail.read_bytes()) is None)
        badwire = Path(td) / "badwire.replay26"
        badwire.write_bytes(b"\x3e" + good)                 # field 7, wire type 6
        rw = read_one(badwire)
        check("ERR-WIRE illegal wire type -> UNREADABLE",
              rw["klass"] == UNREADABLE, f"status={rw['status']}")
        check("   ... and the SAME bytes uncorrupted parse cleanly (the fixture "
              "is not just always-fail)",
              read_one_bytes_ok(good), "clean 300-turn replay -> DECISIVE")
        check("   ... status names the exception (not an empty string)",
              r["status"].startswith("err:") and len(r["status"]) > 8, r["status"])
        check("   ... turns is -1, i.e. NOT a count that can be summed",
              r["turns"] == -1)
        absent = read_one(Path(td) / "does_not_exist.replay26")
        check("ERR-ABSENT missing file -> UNREADABLE with a named exception",
              absent["klass"] == UNREADABLE and "FileNotFoundError" in absent["status"],
              absent["status"])
        # ⭐ THE DISCRIMINATOR THIS WHOLE TOOL EXISTS FOR. A batch of two broken
        # files and one clean 400-round game must report "0 R1000" and
        # "2 UNREADABLE" as SEPARATE facts. The failure mode being excluded is
        # a run that reports 0 r1000 games because it could not read anything.
        clean = Path(td) / "clean.replay26"
        clean.write_bytes(synth_replay(400, "core_destroyed"))
        batch = scan([bad, badwire, tail, Path(td) / "nope.replay26", clean])
        n_r1000 = sum(1 for x in batch if x["klass"] == R1000)
        n_unread = sum(1 for x in batch if x["klass"] == UNREADABLE)
        n_ok = sum(1 for x in batch if x["status"] == "ok")
        check("DISCRIMINATOR: 0 R1000 rows, 4 UNREADABLE and 1 ok are three "
              "SEPARATE facts", n_r1000 == 0 and n_unread == 4 and n_ok == 1,
              f"R1000={n_r1000} UNREADABLE={n_unread} ok={n_ok}")

    print("\n-- GUARD ON THE COVERAGE READER: a zero-row surface is an ALARM, not a 0%.")
    with tempfile.TemporaryDirectory() as td:
        empty = Path(td) / "empty.tsv"
        empty.write_text("file\tcond\tturns\n")
        rows = _tsv(empty)
        hit = False
        try:
            _need(rows, ["file"], "empty.tsv")
        except SystemExit as exc:
            hit = "ZERO rows" in str(exc)
        check("_need() refuses a zero-row surface", hit)
        hashed = Path(td) / "hashed.tsv"
        hashed.write_text("# FIXTURE start=X\nts\tcond\tturns\n1\tcore_destroyed\t300\n"
                          "# FIXTURE-RESUME\n2\ttiebreak\t1000\n")
        hr = _tsv(hashed)
        check("_tsv() skips `# FIXTURE` lines, leading AND mid-file",
              len(hr) == 2 and hr[0]["cond"] == "core_destroyed" and hr[1]["turns"] == "1000",
              f"rows={len(hr)} first_key={sorted(hr[0])[:3] if hr else None}")
        wrongcol = Path(td) / "wrong.tsv"
        wrongcol.write_text("a\tb\n1\t2\n")
        hit2 = False
        try:
            _need(_tsv(wrongcol), ["turns"], "wrong.tsv")
        except SystemExit as exc:
            hit2 = "missing column" in str(exc)
        check("_need() refuses a surface without the named column", hit2)

    print("\n-- REAL ARCHIVE CONTROLS (skipped if the archive is absent).")
    jp = CORPUS / "join.tsv"
    if ARCHIVE.is_dir() and jp.exists():
        join = _tsv(jp)
        _need(join, ["file", "cond", "turns"], "join.tsv")
        pos = next((g for g in join if int(g["turns"]) == MAX_TURNS
                    and (ARCHIVE / g["file"]).exists()), None)
        # ⭐ THE SHARP NEGATIVE: cond says `titanium_collected` (the tiebreak
        # string) on a game that ended in 146 rounds. A cond-keyed tool calls
        # this an r1000. There are exactly 2 such rows in join.tsv and this
        # control exists because of them.
        neg = next((g for g in join if g["cond"] == "titanium_collected"
                    and int(g["turns"]) != MAX_TURNS
                    and (ARCHIVE / g["file"]).exists()), None)
        if pos:
            r = read_one(ARCHIVE / pos["file"])
            check(f"POS-REAL {pos['file'][:20]}… platform turns={pos['turns']} -> R1000",
                  r["klass"] == R1000 and r["turns"] == MAX_TURNS,
                  f"got turns={r['turns']} klass={r['klass']} cond={r['wincond']!r}")
        else:
            check("POS-REAL available", False, "no r1000 row with an on-disk replay")
        if neg:
            r = read_one(ARCHIVE / neg["file"])
            check(f"NEG-REAL cond='titanium_collected' at turns={neg['turns']} "
                  "-> NOT R1000",
                  r["klass"] != R1000 and r["klass"] == DECISIVE,
                  f"got turns={r['turns']} klass={r['klass']} cond={r['wincond']!r} "
                  "— a cond-keyed rule fails HERE")
        else:
            check("NEG-REAL available", False,
                  "no cond=titanium_collected row below 1000 turns on disk")
        n = min(400, len(join))
        rc = validate(sample=n)
        check(f"XVAL {n} real files agree with the platform on turns AND cond",
              rc == 0)
    else:
        print("  (archive or join.tsv absent — real controls skipped)")

    print("\n" + ("SELFTEST PASS" if not fails else f"SELFTEST FAIL: {fails}"))
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.report:
        return report()
    if a.build:
        return build(Path(a.out), a.limit)
    if a.validate:
        return validate(a.limit)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
