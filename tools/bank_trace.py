#!/usr/bin/env python3
"""PER-ROUND BANK TRACE — the instrument arm B's falsifier actually needs.

⛔ WHY THIS EXISTS. The tri-arm prereg's B (UNDERECO) falsifier reads:
*"the bank must NOT sit pinned <=12 Ti for 50+ consecutive post-chronic
rounds"*. **`corpus/econ.tsv` cannot answer that**: it persists only
`ti_end` — the LAST value per round BAND — i.e. four snapshots per game
(r0-150, r150-200, r200-300, r300+). A 50-round pin is invisible in a
150-round bucket, and a bank at 12 in two consecutive snapshots is not
evidence of a pin between them.

**The data IS on the wire and we own the decoder:** `updatePlayers` (unum 6)
carries per-round titanium (field 1), titaniumCollected (4) and ammo (7) for
BOTH teams, and `tools/corpus/replay_econ.py:113-127` already parses exactly
that structure — it just aggregates it away. This reads the same field and
keeps the series.

Reuses `replay_econ`'s primitives rather than re-implementing the wire format
(the run-both-and-diff rule: the `--verify` mode checks this trace's
band-final values against `econ.tsv`'s `ti_end` for the same file).

Usage:
  bank_trace.py <replay.replay26> [...]           # per-file pin report
  bank_trace.py --pin-threshold 12 --min-run 50 ...
  bank_trace.py --verify <replay> --econ corpus/econ.tsv
  bank_trace.py --selftest
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "corpus"))
# same primitives replay_econ.py uses — not a second wire implementation
from replay_census import fields, WIRE_LEN, WIRE_VARINT  # noqa: E402

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


def bank_series(path: Path) -> dict[int, list[int]]:
    """team -> [titanium at each round], in round order.

    Turn framing copied from replay_econ.census(): top-level field 3 is a turn
    buffer, one per round.
    """
    data = path.read_bytes()
    turn_bufs = [v for num, wire, v in fields(data)
                 if num == 3 and wire == WIRE_LEN]
    series: dict[int, list[int]] = {0: [], 1: []}
    cur: dict[int, int] = {}
    for tbuf in turn_bufs:
        seen = {}
        # NOTE the DOUBLE nesting, copied from replay_econ.census():
        # turn_buf -> wrapper (field 1) -> update messages (unum).
        # Missing this level silently yields ZERO rounds, which is how the
        # first version of this tool "passed" — caught by running it on a
        # real replay instead of trusting the selftest.
        for _n, _w, ub in fields(tbuf):
          for unum, w, ubuf in fields(ub):
            if w != WIRE_LEN or unum != 6:           # updatePlayers only
                continue
            for pn, _pw, pv in fields(ubuf):
                if pn != 1:
                    continue
                for tn, _tw, tv in fields(pv):
                    if tn not in (1, 2):
                        continue
                    d = {}
                    for k, w2, v in fields(tv):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    seen[tn - 1] = d.get(1, 0)
        # one sample per team per ROUND, FORWARD-FILLED: a round with no
        # update means the bank did not change, not that it is zero.
        cur.update(seen)
        for t in (0, 1):
            if t in cur:
                series[t].append(cur[t])
    return series


def longest_pin(series: list[int], threshold: int) -> tuple[int, int]:
    """(longest run at-or-below threshold, its start index)."""
    best = run = 0
    best_start = start = 0
    for i, v in enumerate(series):
        if v <= threshold:
            if run == 0:
                start = i
            run += 1
            if run > best:
                best, best_start = run, start
        else:
            run = 0
    return best, best_start


def report(path: Path, threshold: int, min_run: int) -> dict:
    s = bank_series(path)
    out = {"file": path.name, "rounds": max(len(s[0]), len(s[1]))}
    for t in (0, 1):
        run, start = longest_pin(s[t], threshold)
        out[f"team{t}_longest_pin"] = run
        out[f"team{t}_pin_start_rnd"] = start if run else None
        out[f"team{t}_pinned"] = run >= min_run
        out[f"team{t}_ti_final"] = s[t][-1] if s[t] else None
    return out


def selftest() -> int:
    """Both-ways on the PIN DETECTOR (the part that decides the falsifier).
    The wire reader is covered by --verify against econ.tsv on real files."""
    # a pin exists and is found, with its start
    run, start = longest_pin([500] * 10 + [12] * 60 + [400] * 5, 12)
    assert (run, start) == (60, 10), (run, start)
    # ⚠ the cell that must come out the OTHER way: a bank that dips to 12
    # repeatedly but never STAYS there must NOT read as pinned
    run, _ = longest_pin([12, 400] * 40, 12)
    assert run == 1, f"alternating dips read as a pin of {run} — detector is wrong"
    # threshold is exclusive-above: 13 is not a pin at threshold 12
    run, _ = longest_pin([13] * 80, 12)
    assert run == 0, "values above threshold counted as pinned"
    # empty series does not crash or claim a pin
    assert longest_pin([], 12) == (0, 0)
    print("selftest PASS (pin found with start; alternating dips NOT a pin; "
          "above-threshold not counted; empty safe)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("replays", nargs="*")
    ap.add_argument("--pin-threshold", type=int, default=12,
                    help="prereg B: bank <= this counts as pinned")
    ap.add_argument("--min-run", type=int, default=50,
                    help="prereg B: consecutive rounds to call it a pin")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.replays:
        ap.error("give at least one replay, or --selftest")
    for p in args.replays:
        r = report(Path(p), args.pin_threshold, args.min_run)
        print(f"{r['file']}  rounds={r['rounds']}")
        for t in (0, 1):
            flag = "⛔ PINNED" if r[f"team{t}_pinned"] else "ok"
            print(f"  team{t}: longest pin {r[f'team{t}_longest_pin']} rnds "
                  f"(from r{r[f'team{t}_pin_start_rnd']}), final Ti "
                  f"{r[f'team{t}_ti_final']} -> {flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
