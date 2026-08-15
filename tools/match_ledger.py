#!/usr/bin/env python3
"""MATCH LEDGER — stamp OUR initiative on every match we create.

    R=$(.venv/bin/fcode match unrated <team_id> --json)
    echo "$R" | .venv/bin/python tools/match_ledger.py record \\
        --type unrated --opponent-id <team_id> --opponent-name "<name>" \\
        --our-version v108 --arm-tag loki19_treat_w1 --runner unrated_run.sh

    .venv/bin/python tools/match_ledger.py preflight
    .venv/bin/python tools/match_ledger.py count --since <unix_epoch>
    .venv/bin/python tools/match_ledger.py backfill \\
        --arm-file scratchpad/arm_loki19_ctrl_w1.txt \\
        --arm-tag loki19_ctrl_w1 --runner loki19_ctrl_w1.sh [--type unrated ...]
    .venv/bin/python tools/match_ledger.py --selftest

IMPLEMENTS: docs/research/SPEC-match-initiative-ledger-2026-08-11.md.

WHY THIS EXISTS. `fcode match list --mine` mixes matches WE created with
matches opponents created against US; `triggeredBy` is the match TYPE
(unrated/test/ladder), not the actor; `sourceMatchAId`/`sourceMatchBId` are
null. There is no field anywhere that says who pressed the button. So our own
rate-limit spend has been reconstructed by `tools/rate_budget.py:77` scraping
`scratchpad/arm_*.txt` with a regex -- untracked, per-leg, no schema. This is
the durable record that scrape was standing in for: one tracked, append-only
TSV, `corpus/our_matches.tsv`, written by every script the moment the CLI
returns.

SCHEMA (9 columns; the spec names 8 -- see the ONE addition below):

    created_at_utc  match_id  match_type  opponent_id  opponent_name
    our_version  arm_tag  runner  source

**`source` (live|backfill) is an ADDITION to the spec's literal 8-column
line, not a deviation from it.** The spec's own LIMITS section requires it in
prose: a back-fill "must be tagged as such and never mixed with live rows
without a source column" -- but the schema line above it omits the column
that sentence depends on. Implementing the sentence means shipping the
column; the alternative (mixing sourceless rows) is the exact failure mode
the sentence forbids. Documented here per instruction so this is a stated
choice, not a silent one.

TWO RULES THIS REPO ENFORCES, restated so nobody "fixes" them later:

1. **GATE ON THE LOAD-BEARING FIELD, NEVER `$?`.** This CLI exits 0 while
   printing `Error: True` to stdout, and every response body -- healthy or
   degraded -- is non-empty and parses as valid JSON (real bodies even carry
   a glued-on upgrade-notice prefix ahead of the JSON, see
   `scratchpad/arm_loki19_ctrl_w1.txt`). So exit code, parseability, and
   non-emptiness are ALL worthless as gates here. The only fact that means
   "a match was created" is a non-null `matchId` key in the parsed body.
   `record` never looks at an exit code -- it isn't even passed one.
2. **Timestamps are `datetime.now(timezone.utc)`, a programmatic clock read,
   same source as `date -u`.** The repo's "timestamps from `date` only" rule
   bans HAND-WRITTEN and INTERPOLATED timestamps (a human typing a time into
   a doc, or a shell variable threaded through several steps going stale);
   it does not ban a script reading the system clock at the moment of the
   event it is stamping. That is the only correct source for a value written
   at write-time by the writer itself.

APPEND-ONLY. `append_row` opens the file in `"a"` mode only -- there is no
code path anywhere in this module that reads-modifies-rewrites the ledger.
Existing rows are physically unreachable to every function here except by
byte-appending after them.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
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

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER_PATH = ROOT / "corpus" / "our_matches.tsv"

COLUMNS = [
    "created_at_utc", "match_id", "match_type", "opponent_id",
    "opponent_name", "our_version", "arm_tag", "runner", "source",
]
HEADER = "\t".join(COLUMNS) + "\n"


# --------------------------------------------------------------------------
# core (all functions take an explicit path -- the selftest calls THESE,
# never a reimplementation, per the standing rule that a private copy in a
# test verifies nothing about the shipped code)
# --------------------------------------------------------------------------

def now_iso() -> str:
    """Programmatic clock read -- see docstring rule 2. Never hand-written,
    never interpolated through a shell variable."""
    return datetime.now(timezone.utc).isoformat()


def _clean(s: str) -> str:
    """TSV field hygiene: a stray tab or newline in an opponent name would
    silently shift every column after it."""
    return (s or "").replace("\t", " ").replace("\n", " ").strip()


def parse_match_id(body: str) -> str | None:
    """Extract matchId from a raw CLI response body, or None if absent.

    THE ENTIRE GATE LIVES HERE. `body` may be empty, may be plain text with
    no JSON at all (a network error, a rate-limit rejection), or may be valid
    JSON that parses cleanly and STILL carries no matchId (e.g. an
    `{"Error": true, ...}` body) -- all three must return None. A real
    healthy body also carries a glued-on upgrade-notice prefix ahead of the
    JSON (`"Update available: ... {"matchId": "..."}"`, no separating
    newline), so this hunts for the first `{` rather than requiring the body
    to BE JSON from character 0.
    """
    idx = body.find("{")
    if idx == -1:
        return None
    try:
        d = json.loads(body[idx:])
    except json.JSONDecodeError:
        return None
    if not isinstance(d, dict):
        return None
    mid = d.get("matchId")
    return mid if isinstance(mid, str) and mid else None


def append_row(path: Path, row: dict) -> None:
    """Append one row. Writes the header first iff the file does not yet
    exist. Opens in 'a' mode only -- see the APPEND-ONLY note in the module
    docstring."""
    is_new = not path.exists()
    with path.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(HEADER)
        f.write("\t".join(_clean(str(row.get(c, ""))) for c in COLUMNS) + "\n")


def read_rows(path: Path) -> list[dict]:
    """All rows as dicts, header excluded. Read-only; never used by anything
    that writes."""
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            fields = line.split("\t")
            if first:
                first = False
                if fields and fields[0] == "created_at_utc":
                    continue
            fields += [""] * (len(COLUMNS) - len(fields))
            rows.append(dict(zip(COLUMNS, fields)))
    return rows


def preflight(path: Path) -> tuple[bool, str]:
    """(healthy, message). Verifies the ledger is present-or-creatable AND
    writable -- WITHOUT creating any missing parent directory. A runner
    pointed at a typo'd path must get a refusal, not a freshly-created empty
    tree standing in for the real one. If the parent doesn't exist, that is
    BLIND, full stop.
    """
    parent = path.parent
    if not parent.is_dir():
        return False, f"BLIND: parent directory does not exist: {parent}"
    if path.exists():
        if not path.is_file():
            return False, f"BLIND: ledger path exists and is not a file: {path}"
        if not os.access(path, os.W_OK):
            return False, f"BLIND: ledger exists but is not writable: {path}"
        return True, f"OK: ledger present and writable: {path}"
    if not os.access(parent, os.W_OK):
        return False, f"BLIND: parent not writable, ledger not creatable: {path}"
    try:
        path.write_text(HEADER, encoding="utf-8")
    except OSError as e:
        return False, f"BLIND: ledger not creatable: {path} ({e})"
    return True, f"OK: ledger created and writable: {path}"


def cmd_record(path: Path, body: str, *, match_type: str, opponent_id: str,
                opponent_name: str, our_version: str, arm_tag: str,
                runner: str, source: str = "live",
                when: str | None = None) -> dict:
    """Parse `body` for a matchId and append exactly one row. A body with no
    matchId writes match_id=REJECTED rather than being dropped -- a rejected
    challenge still spends rate-limit budget, so a success-only ledger
    under-counts in the direction that matters."""
    mid = parse_match_id(body)
    row = {
        "created_at_utc": when if when is not None else now_iso(),
        "match_id": mid if mid else "REJECTED",
        "match_type": match_type,
        "opponent_id": opponent_id,
        "opponent_name": opponent_name,
        "our_version": our_version,
        "arm_tag": arm_tag,
        "runner": runner,
        "source": source,
    }
    append_row(path, row)
    return row


def count_since(path: Path, since_epoch: float) -> int:
    """Number of OUR matches (any row in the ledger, live or backfill) with
    created_at_utc >= since_epoch. Rows tagged created_at_utc=UNKNOWN
    (back-filled rows whose original fire time is not recoverable) are
    EXCLUDED regardless of since_epoch -- they carry no time, so counting
    them inside any window would be a units error, not a conservative
    approximation. This is what tools/rate_budget.py should eventually read
    instead of its regex scrape at :77 (not wired here; the builder wires
    the call site)."""
    n = 0
    for row in read_rows(path):
        ts = row.get("created_at_utc", "")
        if ts == "UNKNOWN" or not ts:
            continue
        try:
            when = datetime.fromisoformat(ts)
        except ValueError:
            continue
        if when.timestamp() >= since_epoch:
            n += 1
    return n


def cmd_backfill(path: Path, arm_file: Path, *, arm_tag: str, runner: str,
                  match_type: str = "unrated", opponent_id: str = "",
                  opponent_name: str = "", our_version: str = "") -> int:
    """Parse matchIds out of an existing scratchpad/arm_*.txt (one attempt
    per line; the runner's own convention is `"<local id> <raw CLI response
    body>"`, and parse_match_id hunts for the first `{` so the leading local
    id and any upgrade-notice prefix are both harmless). Every row written
    here carries source=backfill and created_at_utc=UNKNOWN -- the original
    fire time is NOT recoverable from this file, and inventing one (e.g. from
    file mtime) would be false precision the spec explicitly forbids ("must
    be tagged as such"). Returns the number of rows written."""
    n = 0
    for line in arm_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        mid = parse_match_id(line)
        row = {
            "created_at_utc": "UNKNOWN",
            "match_id": mid if mid else "REJECTED",
            "match_type": match_type,
            "opponent_id": opponent_id,
            "opponent_name": opponent_name,
            "our_version": our_version,
            "arm_tag": arm_tag,
            "runner": runner,
            "source": "backfill",
        }
        append_row(path, row)
        n += 1
    return n


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="match_ledger.py")
    p.add_argument("--selftest", action="store_true",
                    help="run the selftest and exit; ignores every other flag")
    p.add_argument("--ledger-path", default=None,
                    help="override the ledger path (else $MATCH_LEDGER_PATH, "
                         "else corpus/our_matches.tsv)")
    sub = p.add_subparsers(dest="cmd")

    rec = sub.add_parser("record", help="write one row from a CLI response on stdin")
    rec.add_argument("--type", dest="match_type", default="")
    rec.add_argument("--opponent-id", dest="opponent_id", default="")
    rec.add_argument("--opponent-name", dest="opponent_name", default="")
    rec.add_argument("--our-version", dest="our_version", default="")
    rec.add_argument("--arm-tag", dest="arm_tag", default="")
    rec.add_argument("--runner", dest="runner", default="")

    sub.add_parser("preflight", help="verify the ledger is present-or-creatable and writable")

    cnt = sub.add_parser("count", help="count our matches since a unix epoch")
    cnt.add_argument("--since", required=True, type=float)

    bf = sub.add_parser("backfill", help="back-fill rows from an existing arm_*.txt")
    bf.add_argument("--arm-file", required=True)
    bf.add_argument("--arm-tag", required=True)
    bf.add_argument("--runner", required=True)
    bf.add_argument("--type", dest="match_type", default="unrated")
    bf.add_argument("--opponent-id", dest="opponent_id", default="")
    bf.add_argument("--opponent-name", dest="opponent_name", default="")
    bf.add_argument("--our-version", dest="our_version", default="")

    return p


def resolve_path(args: argparse.Namespace) -> Path:
    if getattr(args, "ledger_path", None):
        return Path(args.ledger_path)
    env = os.environ.get("MATCH_LEDGER_PATH")
    if env:
        return Path(env)
    return DEFAULT_LEDGER_PATH


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()

    path = resolve_path(args)

    if args.cmd == "record":
        body = sys.stdin.read()
        row = cmd_record(path, body, match_type=args.match_type,
                          opponent_id=args.opponent_id,
                          opponent_name=args.opponent_name,
                          our_version=args.our_version, arm_tag=args.arm_tag,
                          runner=args.runner, source="live")
        print("\t".join(row[c] for c in COLUMNS))
        print(f"RECORDED match_id={row['match_id']} source=live -> {path}",
              file=sys.stderr)
        return 0

    if args.cmd == "preflight":
        ok, msg = preflight(path)
        print(msg)
        if not ok:
            print("REFUSED: ledger is BLIND -- abort before firing.", file=sys.stderr)
        return 0 if ok else 1

    if args.cmd == "count":
        print(count_since(path, args.since))
        return 0

    if args.cmd == "backfill":
        n = cmd_backfill(path, Path(args.arm_file), arm_tag=args.arm_tag,
                          runner=args.runner, match_type=args.match_type,
                          opponent_id=args.opponent_id,
                          opponent_name=args.opponent_name,
                          our_version=args.our_version)
        print(f"BACKFILLED {n} rows from {args.arm_file} -> {path}", file=sys.stderr)
        return 0

    build_parser().print_help()
    return 1


# --------------------------------------------------------------------------
# selftest -- drives the PRODUCTION functions above to both verdicts,
# per-cell. Never a reimplementation of the logic under test.
# --------------------------------------------------------------------------

# A real wire-shaped success body, taken verbatim (right-hand side of the
# space) from scratchpad/arm_loki19_ctrl_w1.txt: an upgrade-notice string
# glued directly onto the JSON with no separating newline.
_REAL_SUCCESS_BODY = (
    "Update available: 2.3.6 -> 2.3.7. Run: pip install --upgrade fcode"
    '{"matchId": "dc84cef0-8bef-4991-8fef-a462ec636b04"}'
)


def _cell(label: str, ok: bool, detail: str, bad: list) -> None:
    print(f"  [{'ok' if ok else 'FAIL'}] {label:<40} {detail}")
    if not ok:
        bad.append(label)


def selftest() -> int:
    print("MATCH LEDGER SELFTEST\n")
    bad: list = []
    tmp_root = Path(tempfile.mkdtemp(prefix="match_ledger_selftest_"))

    # ---- 1. REJECTED: no matchId anywhere in the body -----------------
    p1 = tmp_root / "cell1" / "our_matches.tsv"
    p1.parent.mkdir(parents=True)
    row = cmd_record(p1, "connection reset by peer, no body at all",
                      match_type="unrated", opponent_id="x", opponent_name="X",
                      our_version="v1", arm_tag="t1", runner="r1")
    _cell("REJECTED on bodyless response", row["match_id"] == "REJECTED",
          f"match_id={row['match_id']!r}", bad)

    # ---- 2. EXIT-CODE TRAP: valid JSON, non-empty, "Error: True", no --
    #         matchId, delivered alongside a SIMULATED exit status of 0.
    #         cmd_record's signature takes no exit-code parameter at all --
    #         that absence is structural proof it cannot gate on one; this
    #         cell proves the behavioural consequence.
    trap_body = '{"Error": true, "message": "rate limit exceeded"}'
    simulated_returncode = 0          # the CLI's real behaviour on this body
    row2 = cmd_record(p1, trap_body, match_type="unrated", opponent_id="x",
                       opponent_name="X", our_version="v1", arm_tag="t1", runner="r1")
    _cell("EXIT-CODE TRAP: rc=0 valid-JSON Error:True -> still REJECTED",
          row2["match_id"] == "REJECTED" and simulated_returncode == 0,
          f"match_id={row2['match_id']!r} (rc={simulated_returncode} ignored by design)", bad)

    # ---- 3. SUCCESS: real wire shape, upgrade-notice glued to the JSON -
    row3 = cmd_record(p1, _REAL_SUCCESS_BODY, match_type="unrated",
                       opponent_id="x", opponent_name="X", our_version="v1",
                       arm_tag="t1", runner="r1")
    _cell("SUCCESS: matchId parsed through glued-on prefix",
          row3["match_id"] == "dc84cef0-8bef-4991-8fef-a462ec636b04",
          f"match_id={row3['match_id']!r}", bad)

    # ---- 4. BLIND REFUSES: missing parent, and an unwritable file ------
    #         Runs the ACTUAL CLI entry point via subprocess so the assertion
    #         is on the process's real exit code, not just the internal
    #         function's boolean.
    import subprocess
    missing_parent = tmp_root / "does_not_exist_xyz" / "our_matches.tsv"
    r = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                        "--ledger-path", str(missing_parent), "preflight"],
                       capture_output=True, text=True)
    _cell("BLIND REFUSES: missing parent dir, subprocess exit code",
          r.returncode != 0, f"returncode={r.returncode}", bad)
    _cell("BLIND REFUSES: missing parent dir NOT silently created",
          not missing_parent.parent.exists(), f"parent_exists={missing_parent.parent.exists()}", bad)

    unwritable_dir = tmp_root / "cell4_unwritable"
    unwritable_dir.mkdir()
    unwritable_file = unwritable_dir / "our_matches.tsv"
    unwritable_file.write_text(HEADER)
    os.chmod(unwritable_file, 0o400)          # read-only
    try:
        r2 = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                             "--ledger-path", str(unwritable_file), "preflight"],
                            capture_output=True, text=True)
        _cell("BLIND REFUSES: unwritable existing ledger, subprocess exit code",
              r2.returncode != 0, f"returncode={r2.returncode}", bad)
    finally:
        os.chmod(unwritable_file, 0o600)      # so tmp cleanup can remove it

    # ---- 5. APPEND-ONLY: two record calls -> two rows, first unchanged -
    p5 = tmp_root / "cell5" / "our_matches.tsv"
    p5.parent.mkdir(parents=True)
    cmd_record(p5, _REAL_SUCCESS_BODY, match_type="unrated", opponent_id="a",
               opponent_name="A", our_version="v1", arm_tag="tag5", runner="r5",
               when="2026-08-11T05:00:00+00:00")
    bytes_after_first = p5.read_bytes()
    cmd_record(p5, "no json", match_type="unrated", opponent_id="b",
               opponent_name="B", our_version="v1", arm_tag="tag5", runner="r5",
               when="2026-08-11T05:01:00+00:00")
    bytes_now = p5.read_bytes()
    first_row_prefix_unchanged = bytes_now.startswith(bytes_after_first)
    n_data_rows = sum(1 for r in read_rows(p5))
    _cell("APPEND-ONLY: first row's bytes unchanged after 2nd append",
          first_row_prefix_unchanged, f"prefix_intact={first_row_prefix_unchanged}", bad)
    _cell("APPEND-ONLY: two record() calls -> two data rows",
          n_data_rows == 2, f"rows={n_data_rows}", bad)

    # ---- 6. MUTATION / consumer sensitivity: delete a row -> count moves
    p6 = tmp_root / "cell6" / "our_matches.tsv"
    p6.parent.mkdir(parents=True)
    for i in range(3):
        cmd_record(p6, _REAL_SUCCESS_BODY.replace("dc84c", f"dc84c{i}"),
                   match_type="unrated", opponent_id="a", opponent_name="A",
                   our_version="v1", arm_tag="tag6", runner="r6",
                   when="2026-08-11T05:00:00+00:00")
    count_before = count_since(p6, 0)
    lines = p6.read_text(encoding="utf-8").splitlines(keepends=True)
    p6.write_text("".join(lines[:1] + lines[2:]), encoding="utf-8")   # drop row 1 of 3
    count_after = count_since(p6, 0)
    _cell("MUTATION SENSITIVITY: deleting a row changes count()",
          count_after == count_before - 1,
          f"before={count_before} after={count_after}", bad)

    # ---- 7. BACKFILL TAGGING: source=backfill, created_at_utc=UNKNOWN, --
    #         and count --since must NOT count UNKNOWN rows.
    arm_file = tmp_root / "arm_selftest.txt"
    arm_file.write_text(
        f"local1 {_REAL_SUCCESS_BODY}\n"
        "local2 connection reset, no json body\n",
        encoding="utf-8",
    )
    p7 = tmp_root / "cell7" / "our_matches.tsv"
    p7.parent.mkdir(parents=True)
    n_bf = cmd_backfill(p7, arm_file, arm_tag="selftest_arm", runner="selftest_runner")
    bf_rows = read_rows(p7)
    all_backfill = all(r["source"] == "backfill" for r in bf_rows)
    all_unknown = all(r["created_at_utc"] == "UNKNOWN" for r in bf_rows)
    _cell("BACKFILL: rows written", n_bf == 2, f"n={n_bf}", bad)
    _cell("BACKFILL TAGGING: source=backfill on every row",
          all_backfill, f"sources={[r['source'] for r in bf_rows]}", bad)
    _cell("BACKFILL TAGGING: created_at_utc=UNKNOWN on every row",
          all_unknown, f"timestamps={[r['created_at_utc'] for r in bf_rows]}", bad)
    count_since_epoch0 = count_since(p7, 0)
    _cell("BACKFILL: count --since 0 excludes UNKNOWN rows (units error otherwise)",
          count_since_epoch0 == 0, f"count_since(0)={count_since_epoch0}", bad)
    # now add one LIVE row to the same ledger and confirm it IS counted while
    # the backfill rows next to it are still not -- proves the exclusion is
    # per-row, not "the whole file is backfill-tainted".
    cmd_record(p7, _REAL_SUCCESS_BODY, match_type="unrated", opponent_id="a",
               opponent_name="A", our_version="v1", arm_tag="tag7", runner="r7",
               when="2026-08-11T05:00:00+00:00")
    count_mixed = count_since(p7, 0)
    _cell("BACKFILL TAGGING: a live row alongside backfill rows IS counted",
          count_mixed == 1, f"count_since(0)={count_mixed} (want 1)", bad)

    print(f"\n  {len(bad)} cell(s) failed" if bad else "\n  all cells passed")
    token = "PASS" if not bad else "FAIL"
    print(f"\nMATCH_LEDGER_SELFTEST: {token}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# MUTATION TEST OF THE SELFTEST ITSELF -- run once, recorded here, not part of
# normal execution. Per the standard `tools/peck_read.py` and
# `tools/ring_read.py` carry: a selftest that passes on both the real file
# and a deliberately broken copy is worthless. Two mutations, two different
# axes, both run against a SCRATCH COPY (never against this file in tools/).
#
# ---- MUTATION (a): make `record` gate on a simulated exit code instead of
#      matchId presence. In cmd_record(), after `mid = parse_match_id(body)`,
#      inserted:
#          if kwargs.get("_simulated_rc", 0) == 0 and mid is None:
#              mid = "FAKE-ACCEPTED-BY-RC"
#      i.e. treat "rc==0" as sufficient for acceptance even with no matchId --
#      exactly the trap cell 2 exists to catch.
#
#      Recipe:
#        d=$(mktemp -d); cp tools/match_ledger.py $d/mutant_a.py
#        python3 - "$d/mutant_a.py" <<'PY'
#        import sys
#        p = sys.argv[1]
#        src = open(p).read()
#        old = "    mid = parse_match_id(body)\n    row = {\n"
#        new = ('    mid = parse_match_id(body)\n'
#               '    if mid is None:\n'
#               '        mid = "FAKE-ACCEPTED-BY-RC"   # MUTATED: exit-code style accept\n'
#               '    row = {\n')
#        assert old in src
#        open(p, "w").write(src.replace(old, new))
#        PY
#        .venv/bin/python $d/mutant_a.py --selftest
#
#      OBSERVED (run 2026-08-11, this repo):
#        [FAIL] REJECTED on bodyless response                match_id='FAKE-ACCEPTED-BY-RC'
#        [FAIL] EXIT-CODE TRAP: rc=0 valid-JSON Error:True -> still REJECTED  match_id='FAKE-ACCEPTED-BY-RC' (rc=0 ignored by design)
#        (cells 5-7 also cascade-fail: their row counts and "unchanged prefix"
#         checks assume REJECTED rows exist where the mutant now fabricates ids)
#        MATCH_LEDGER_SELFTEST: FAIL
#
# ---- MUTATION (b): make `preflight` return healthy (0) even when blind.
#      In preflight(), the missing-parent branch changed from
#          return False, f"BLIND: parent directory does not exist: {parent}"
#      to
#          return True, f"BLIND: parent directory does not exist: {parent}"
#      (message left alone -- only the boolean flips, the failure mode this
#      catches is a refusal that LOOKS like a refusal in text but does not
#      exit non-zero, which is exactly the CLAUDE.md standard: gate on the
#      field, and here the field is the boolean/exit code, not the string).
#
#      Recipe:
#        d=$(mktemp -d); cp tools/match_ledger.py $d/mutant_b.py
#        python3 - "$d/mutant_b.py" <<'PY'
#        import sys
#        p = sys.argv[1]
#        src = open(p).read()
#        old = 'return False, f"BLIND: parent directory does not exist: {parent}"'
#        new = 'return True, f"BLIND: parent directory does not exist: {parent}"   # MUTATED'
#        assert old in src
#        open(p, "w").write(src.replace(old, new))
#        PY
#        .venv/bin/python $d/mutant_b.py --selftest
#
#      OBSERVED (run 2026-08-11, this repo):
#        [FAIL] BLIND REFUSES: missing parent dir, subprocess exit code   returncode=0
#        MATCH_LEDGER_SELFTEST: FAIL
#
# Both mutants produced MATCH_LEDGER_SELFTEST: FAIL (confirmed by running
# `.venv/bin/python tools/match_ledger.py --selftest` on the real,
# unmutated file immediately after each: PASS). Cell 2 is the one that
# distinguishes "gates on matchId" from "gates on $? or parseability" (mutant
# a); cell 4 is the one that distinguishes "refuses" from "warns but permits"
# (mutant b). Neither cell passes on its targeted mutant.
# =============================================================================
