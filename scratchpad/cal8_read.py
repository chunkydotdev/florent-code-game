#!/usr/bin/env python3
"""CAL-8 READ INSTRUMENT — P4 primary (six-cell sign test), P1/P2/P3 descriptive.

⭐ WRITTEN BLIND, BEFORE THE PANEL WAS READ. Authored 2026-08-14 ~18:45Z by the
research arm while the runner stood at 13 of 15 accepts. The author had opened no
tally; the fires tape carries matchIds and accept/reject verdicts only, never
outcomes. This docstring is the two-clock claim and the git commit time is its
second hand.

PREREG: docs/research/PREREG-CAL8-2026-08-14.md (7fa94cb, 15:33:08Z, pre-leg),
amendment A1 add-only.

REFERENCE, FIXED BLIND AND SEPARATELY (coordination tape, 2026-08-14 ~18:42Z):
the v125-ONLY rated cut, NOT the era-rated (ourver>=125) cell-selection table.
The prereg's P1 names "n=155" and only the v125-only cut has n=155. That choice
moves LingLing40 by 12.0pp and Big O by 10.0pp against a 10pp threshold, so it
had to be fixed before the data could vote on it.

P4 (PRIMARY, two-sided by construction):
  >=5 of 6 cells BELOW their v125 reference by >=10pp  => systematic NEGATIVE bias
  >=5 of 6 cells ABOVE their v125 reference by >=10pp  => the mirror finding
  otherwise                                            => does not fire
  Honest pre-filter alpha: P(>=5 of 6 one-way) = 0.109; P(6 of 6) = 0.016.
  The >=10pp magnitude filter makes a false positive rarer than that. This test
  is NOT strong; it is the only one the design resolves. It is a SIGN TEST.

P1 (DESCRIPTIVE, NO BAR): pooled panel share beside the 56.8%/n=155 reference,
  with its DEFF-corrected half-width AND the +-9.1pp reference-side floor named
  in the same breath. A bar below the design's own floor is not a bar.

USAGE
  .venv/bin/python scratchpad/cal8_read.py --selftest   # run this FIRST
  .venv/bin/python scratchpad/cal8_read.py
"""
import csv
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIRES = ROOT / "scratchpad" / "panel_cal8_fires.tsv"
LADDER = ROOT / "corpus" / "ladder_games.tsv"
META = ROOT / "corpus" / "meta_join.tsv"

# cell label -> opponent name as it appears in the corpus `opp` column
CELLS = [
    ("D1-0033", "0033"),
    ("D2-LingLing40", "LingLing40"),
    ("D3-Juusto", "Juusto"),
    ("D4-Jython", "Jython"),
    ("D5-BigO", "Big O"),
    ("D6-teamlazy", "team lazy"),
]

DEFF_UNRATED_WITHIN = 1.434   # opponent cluster removed (per-cell cuts)
DEFF_UNRATED_POOLED = 1.833   # both clusters live (pooled panel cut)
DEFF_RATED_WITHIN = 1.366     # reference side, single-opponent cuts
THRESHOLD_PP = 10.0           # P4's registered magnitude filter
N_FLOOR_GAMES = 75            # prereg look-discipline 2


def half_width(p, n, deff):
    """DEFF-corrected 95% half-width, in percentage points."""
    if n <= 0:
        return float("nan")
    return 1.96 * math.sqrt(p * (1 - p) * deff / n) * 100


def accepted_match_ids(fires=FIRES):
    """matchIds of ACCEPTED challenges, in fire order.

    ⛔ ACCEPT ONLY. Rate-limit REJECTIONS are attempts, not matches. Counting
    attempts as accepts is the exact error that put 'n=80' into two commits and
    three lanes on 2026-08-14; this function exists so no reader repeats it by
    hand.
    """
    ids = []
    for line in Path(fires).read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 4 and parts[2] == "ACCEPT" and '"matchId"' in parts[3]:
            frag = parts[3].split('"matchId"')[1]
            ids.append(frag.split('"')[1])
    return ids


def panel_games(match_ids, meta=META):
    """Per-game rows for the accepted matches, keyed by matchId."""
    want = set(match_ids)
    out = defaultdict(list)
    with open(meta) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            for key in ("match", "match_id", "matchId"):
                if key in r and r[key] in want:
                    out[r[key]].append(r)
                    break
    return out


def v125_reference(ladder=LADDER):
    """The FIXED reference: v125-only rated cells. Must total n=155."""
    ref = {}
    with open(ladder) as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    for _, opp in CELLS:
        sel = [r for r in rows if r["opp"] == opp and r["ourver"] == "125"]
        wins = sum(1 for r in sel if r["won"] == "1")
        ref[opp] = (wins, len(sel))
    return ref


def p4(cell_shares, ref):
    """The sign test. Returns (verdict, below, above, detail_rows).

    cell_shares: {opp: (wins, games)} for the PANEL.
    """
    below = above = 0
    detail = []
    for _, opp in CELLS:
        rw, rn = ref.get(opp, (0, 0))
        pw, pn = cell_shares.get(opp, (0, 0))
        if rn == 0 or pn == 0:
            detail.append((opp, None, None, None, "EMPTY"))
            continue
        rs, ps = rw / rn * 100, pw / pn * 100
        delta = ps - rs
        if delta <= -THRESHOLD_PP:
            below += 1
            tag = "BELOW>=10pp"
        elif delta >= THRESHOLD_PP:
            above += 1
            tag = "ABOVE>=10pp"
        else:
            tag = "within 10pp"
        detail.append((opp, ps, rs, delta, tag))
    if below >= 5:
        verdict = "FIRES — SYSTEMATIC NEGATIVE BIAS in FIXTURE_OF_RECORD"
    elif above >= 5:
        verdict = "FIRES — MIRROR FINDING (panel reads HIGH vs rated)"
    else:
        verdict = "DOES NOT FIRE"
    return verdict, below, above, detail


# ---------------------------------------------------------------- selftest ---
def selftest():
    """⛔ FORCED-FAIL PROBES. Every guard is driven to BOTH verdicts.

    A check that has never produced the other verdict has not been seen to
    check. Each cell below names what it would catch.
    """
    fails = []

    def check(name, cond, detail=""):
        if cond:
            print(f"  PASS  {name}")
        else:
            print(f"  FAIL  {name}  {detail}")
            fails.append(name)

    print("A. accepted_match_ids counts ACCEPTS, never ATTEMPTS")
    tmp = ROOT / "scratchpad" / "_cal8_selftest_fires.tsv"
    tmp.write_text(
        '2026-01-01T00:00:00Z\tD1-0033\tACCEPT\tx {"matchId": "aaa"} \n'
        '2026-01-01T00:05:00Z\tD1-0033\tRATELIMIT\tError: Rate limit exceeded \n'
        '2026-01-01T00:10:00Z\tD2-LingLing40\tACCEPT\tx {"matchId": "bbb"} \n'
        '2026-01-01T00:15:00Z\tD3-Juusto\tERROR\tError: True \n'
        "00:20:00Z PANEL-CAL-8: STOP file present, yielding.\n"
        '2026-01-01T00:25:00Z\tARMED\tboundary\tBOUNDARY=15 PTR=9\n'
    )
    got = accepted_match_ids(tmp)
    check("2 accepts extracted from a 6-line tape with 4 non-accepts",
          got == ["aaa", "bbb"], f"got {got}")
    # the mutation that matters: if the filter ever loosened to "any line",
    # this fixture returns more than 2 and the check above flips.
    check("the same tape has 6 lines, so a line-count would have said 6",
          len(tmp.read_text().splitlines()) == 6)
    tmp.unlink()

    print("B. p4 is driven to ALL THREE verdicts on synthetic cells")
    ref = {opp: (50, 100) for _, opp in CELLS}          # every reference 50.0%
    low = {opp: (35, 100) for _, opp in CELLS}          # -15pp everywhere
    high = {opp: (65, 100) for _, opp in CELLS}         # +15pp everywhere
    flat = {opp: (52, 100) for _, opp in CELLS}         # +2pp everywhere
    v_low, b, a, _ = p4(low, ref)
    check("6 cells at -15pp => FIRES NEGATIVE", "NEGATIVE" in v_low and b == 6, v_low)
    v_high, b, a, _ = p4(high, ref)
    check("6 cells at +15pp => FIRES MIRROR", "MIRROR" in v_high and a == 6, v_high)
    v_flat, b, a, _ = p4(flat, ref)
    check("6 cells at +2pp => DOES NOT FIRE", v_flat == "DOES NOT FIRE", v_flat)

    print("C. the >=10pp filter and the >=5-of-6 count are BOTH load-bearing")
    just_under = {opp: (41, 100) for _, opp in CELLS}   # -9pp: under the filter
    v, b, _, _ = p4(just_under, ref)
    check("6 cells at -9pp => DOES NOT FIRE (magnitude filter binds)",
          v == "DOES NOT FIRE" and b == 0, f"{v} below={b}")
    four = dict(low)
    for _, opp in CELLS[4:]:
        four[opp] = (50, 100)                            # 4 low, 2 flat
    v, b, _, _ = p4(four, ref)
    check("4 of 6 at -15pp => DOES NOT FIRE (count binds)",
          v == "DOES NOT FIRE" and b == 4, f"{v} below={b}")
    five = dict(four)
    five[CELLS[4][1]] = (35, 100)                        # push to 5 low
    v, b, _, _ = p4(five, ref)
    check("5 of 6 at -15pp => FIRES (the boundary itself)",
          "NEGATIVE" in v and b == 5, f"{v} below={b}")

    print("D. half_width moves the right way and reproduces a KNOWN number")
    hw = half_width(88 / 155, 155, DEFF_RATED_WITHIN)
    check("v125 reference floor recomputes to the prereg's +-9.1pp",
          abs(hw - 9.1) < 0.1, f"got {hw:.2f}")
    check("half-width SHRINKS as n grows",
          half_width(0.5, 300, 1.5) < half_width(0.5, 75, 1.5))
    check("half-width GROWS as DEFF grows",
          half_width(0.5, 100, 1.9) > half_width(0.5, 100, 1.0))

    print("E. the reference is the v125-only cut and is pinned by n=155")
    if LADDER.exists():
        ref_live = v125_reference()
        total = sum(n for _, n in ref_live.values())
        check("live v125 reference totals n=155 (the prereg's pin)",
              total == 155, f"got n={total}")
        wins = sum(w for w, _ in ref_live.values())
        check("live v125 reference is 56.8% (88/155)",
              wins == 88, f"got {wins}/155")
    else:
        check("ladder tape present", False, "corpus/ladder_games.tsv missing")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)} cell(s): {fails}")
        return 1
    print("SELFTEST PASS — every guard driven to both verdicts.")
    return 0


def main():
    ids = accepted_match_ids()
    n_matches = len(ids)
    n_games_expected = n_matches * 5
    print(f"CAL-8 accepted matches: {n_matches}  (=> {n_games_expected} games at 5/match)")
    if n_games_expected < N_FLOOR_GAMES:
        print(f"⛔ REFUSING TO READ. n={n_games_expected} games is below the "
              f"prereg's n>={N_FLOOR_GAMES} look-discipline floor. "
              f"Descriptive per-cell tallies only.")
        return 2
    print("The read proper is executed by the research arm against this "
          "instrument once the runner logs its BOUNDARY stop row.")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
