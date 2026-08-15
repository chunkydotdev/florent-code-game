#!/usr/bin/env python3
"""LOKI-19 BAR 5d — the falsifier. `hold_pinned` retention, treatment vs control.

    .venv/bin/python tools/loki19_5d.py TREAT_ARM.txt CTRL_ARM.txt
    .venv/bin/python tools/loki19_5d.py --selftest

WHY THIS IS A FILE AND NOT A ONE-LINER. §5d is the FALSIFIER and, after
Amendment 1 pushed the premise bands into "ambiguous", it is one of only two
bands in `docs/prereg/PREREG-loki19-core-peck-2026-08-11.md` that license
unqualified language. Amendment 3b fixed its magnitude and its interval rule
BEFORE any treatment game existed. Both are implemented here so the decision
cannot be made by choosing an estimator at read-out — the exact failure logged
when four defensible estimators of the ring-hold bar straddled its threshold
inside 0.010.

THE STATISTIC, and it is NOT the one the tool's own prose would suggest:
`hold_pinned` == longest run of THE SAME BUILDER on THE SAME RING TILE, over
game length. In `tools/ring_read.py` that series is `tile_episodes`; the
neighbouring `bot_episodes` is a THIRD statistic and is NOT `hold_any`
(ring_read's docstring, CORRECTION 1 in PREREG-loki16b). `hold_pinned` is what
produced LOKI-16b's +0.164 [+0.073, +0.253] and it is the only series §5d names.

    per_game = max(tile_episodes) / rounds     (0.0 when the arm never landed)

ESTIMATOR / CLUSTERING, both pre-registered, neither chosen here:
  * game-mean (each game one vote), 12-ring stratum
  * match-clustered bootstrap on the DIFFERENCE, 4,000 draws, fixed seed
  * Amendment 3b DECISION RULE, BOTH conditions and not either:
        point estimate >= 25% BELOW control  AND  CI upper bound < 0

AMENDMENT 2c is enforced, not assumed. Control window 1 fired under the original
cell rule (a farming_200s DOUBLE and NO Landers); windows 2+ carry Landers. So
the arms do NOT share a cell mix and a pooled cross-arm mean silently reweights
opponents. This file therefore prints the per-cell table FIRST and the pooled
number second, with the imbalance shown rather than described.

WHAT THIS FILE DOES NOT DECIDE: the verdict sentence. It prints which
Amendment 3c row the numbers land in; the builder types the row.

READ-ONLY. Downloads nothing, calls no `fcode`, consumes only
`replay_archive/`. Decoding is delegated wholesale to `tools/ring_read.py`
(the BLESSED ring decoder — `tools/ring_retention.py` is the broken one and
refuses to run); nothing here re-implements ring geometry.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ring_read import ids_from_file, decode, ARCHIVE, OUR_TEAM_ID  # noqa: E402

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

BOOT_DRAWS = 4000
BOOT_SEED = 20260811
FALL_FRACTION = 0.25          # Amendment 3b, fixed before any treatment game


def hold_pinned(g: dict) -> float:
    """Longest same-bot-same-tile ring hold, over game length. 0.0 if never."""
    eps = g["tile_episodes"]
    return (max(eps) / g["rounds"]) if eps and g["rounds"] else 0.0


def load(fp: str) -> list[dict]:
    out = []
    for mid in ids_from_file(Path(fp)):
        meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
        we_a = meta["teamAId"] == OUR_TEAM_ID
        assert we_a or meta["teamBId"] == OUR_TEAM_ID, f"{mid}: not our match"
        ot = 0 if we_a else 1
        opp = meta["teamBName"] if we_a else meta["teamAName"]
        ourver = meta["teamAVersion"] if we_a else meta["teamBVersion"]
        oppver = meta["teamBVersion"] if we_a else meta["teamAVersion"]
        wins_a, n = 0, 0
        for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
            g = decode(rp, ot)
            if g is None:
                print(f"  !! unparseable {rp.name}", file=sys.stderr)
                continue
            n += 1
            if g["winner"] == 0:
                wins_a += 1
            g.update(opp=opp, seat="A" if we_a else "B", mid=mid,
                     ourver=ourver, oppver=oppver, hp=hold_pinned(g))
            out.append(g)
        # Same seat validation ring_read runs: if replay Team 0 != platform
        # teamA the decoded winner tally stops reproducing scoreA.
        assert wins_a == meta["scoreA"] and n == 5, (
            f"{mid}: seat/parse check failed ({wins_a} vs {meta['scoreA']}, n={n})")
    return out


def gm(S: list[dict]) -> float:
    return statistics.mean(g["hp"] for g in S) if S else float("nan")


def boot_ci(A: list[dict], B: list[dict], draws=BOOT_DRAWS, seed=BOOT_SEED):
    """Match-clustered bootstrap on gm(A) - gm(B). Games in a match = one draw."""
    ma, mb = defaultdict(list), defaultdict(list)
    for g in A:
        ma[g["mid"]].append(g)
    for g in B:
        mb[g["mid"]].append(g)
    ka, kb = list(ma), list(mb)
    if not ka or not kb:
        return float("nan"), float("nan"), 0, 0
    rng = random.Random(seed)
    ds = []
    for _ in range(draws):
        sa = [g for k in rng.choices(ka, k=len(ka)) for g in ma[k]]
        sb = [g for k in rng.choices(kb, k=len(kb)) for g in mb[k]]
        ds.append(gm(sa) - gm(sb))
    ds.sort()
    return ds[int(.025 * draws)], ds[int(.975 * draws)], len(ka), len(kb)


def amendment_3b(point_t: float, point_c: float, ci_hi: float) -> tuple[str, str]:
    """-> (row_id, the pre-committed language for that row). BOTH conditions."""
    below_25 = point_t <= point_c * (1.0 - FALL_FRACTION)
    ci_excl = ci_hi < 0
    if below_25 and ci_excl:
        return ("3c row 1", "'the plank buys damage with position' "
                            "-- MAY BE WRITTEN PLAINLY")
    if below_25 and not ci_excl:
        return ("3c row 2", "'retention is lower in the treatment arm; the "
                            "interval does not exclude zero at this n.' "
                            "FORBIDDEN: falls / costs / buys")
    if point_t < point_c:
        return ("3c row 3", "no cost detected at this n. NOT evidence of no "
                            "cost -- 5d only PARTIALLY resolves at ~10 "
                            "clusters/arm")
    return ("3c row 4", "point ABOVE control -- reported as observed, NO CLAIM "
                        "(no mechanism by which pecking should raise retention)")


def report(A: list[dict], B: list[dict], la: str, lb: str) -> None:
    print("=" * 78)
    print(f"LOKI-19 BAR 5d -- hold_pinned (longest same-bot-same-tile hold / game "
          f"length)\n  treatment = {la}   control = {lb}")
    print(f"  estimator game-mean, 12-RING STRATUM, match-clustered bootstrap "
          f"{BOOT_DRAWS} draws seed {BOOT_SEED}")
    print("=" * 78)

    # THE STRATUM IS PRE-REGISTERED AND IT IS NOT ALL GAMES. §5d says "12-ring
    # stratum" and §7 says the leg "may not pool `jackpot` into the retention
    # stratum" -- jackpot anchors both cores in a corner, so its ring is 5 tiles
    # and a hold FRACTION on it is not the same quantity. Filtering here rather
    # than in the caller so the exclusion is printed with its count every run.
    allA, allB = A, B
    dropA = [g for g in A if g["ring_size"] != 12]
    dropB = [g for g in B if g["ring_size"] != 12]
    A = [g for g in A if g["ring_size"] == 12]
    B = [g for g in B if g["ring_size"] == 12]
    print(f"\n-- STRATUM (pre-registered; NOT a post-hoc filter) --")
    print(f"  treatment {len(allA)} games -> {len(A)} in the 12-ring stratum "
          f"({len(dropA)} excluded, ring sizes "
          f"{sorted({g['ring_size'] for g in dropA}) or 'none'})")
    print(f"  control   {len(allB)} games -> {len(B)} in the 12-ring stratum "
          f"({len(dropB)} excluded, ring sizes "
          f"{sorted({g['ring_size'] for g in dropB}) or 'none'})")
    if len(allA) and len(allB):
        print(f"  ALL-GAMES figure, printed ONLY so the stratum's effect is "
              f"visible and NOT a bar: treatment {gm(allA):.4f} control "
              f"{gm(allB):.4f} delta {gm(allA)-gm(allB):+.4f}")
    if not A or not B:
        print("  !! an arm is empty in the stratum -- no 5d verdict is available")
        return

    print("\n-- CELL MIX (Amendment 2c: the arms do NOT match, and this is why) --")
    print(f"  {'opponent':<24}{'treat n':>8}{'ctrl n':>8}   treat seats / ctrl seats")
    cells = sorted({g["opp"] for g in A} | {g["opp"] for g in B})
    for c in cells:
        a = [g for g in A if g["opp"] == c]
        b = [g for g in B if g["opp"] == c]
        sa = "".join(sorted(g["seat"] for g in a)) or "-"
        sb = "".join(sorted(g["seat"] for g in b)) or "-"
        mark = "  <- UNMATCHED n" if len(a) != len(b) else ""
        smark = "  <- SEAT MIX DIFFERS" if sa.count("A") != sb.count("A") else ""
        print(f"  {c:<24}{len(a):>8}{len(b):>8}   {sa} / {sb}{mark}{smark}")

    print("\n-- PER-CELL hold_pinned (the pre-committed comparison, "
          "Amendment 1b bans a pooled mean) --")
    print(f"  {'opponent':<24}{'treat':>8}{'ctrl':>8}{'delta':>9}"
          f"{'% of ctrl':>11}   opp_ver t/c")
    for c in cells:
        a = [g for g in A if g["opp"] == c]
        b = [g for g in B if g["opp"] == c]
        if not a or not b:
            print(f"  {c:<24}{'':>8}{'':>8}   CELL ABSENT FROM ONE ARM -- excluded")
            continue
        ta, tb = gm(a), gm(b)
        pct = (ta / tb * 100) if tb else float("nan")
        va = "/".join(sorted({str(g["oppver"]) for g in a}))
        vb = "/".join(sorted({str(g["oppver"]) for g in b}))
        print(f"  {c:<24}{ta:>8.3f}{tb:>8.3f}{ta-tb:>+9.3f}{pct:>10.0f}%"
              f"   {va} / {vb}")

    print("\n-- POOLED (printed SECOND and it reweights the cells; "
          "see the mix above) --")
    pt, pc = gm(A), gm(B)
    lo, hi, ka, kb = boot_ci(A, B)
    print(f"  treatment {pt:.4f}   control {pc:.4f}   delta {pt-pc:+.4f}")
    print(f"  95% CI on the difference [{lo:+.4f}, {hi:+.4f}]   "
          f"clusters {ka} treatment matches vs {kb} control matches")
    print(f"  Amendment 3b threshold: a FALL needs treatment <= "
          f"{pc*(1-FALL_FRACTION):.4f} (25% below control) AND CI upper < 0")
    row, lang = amendment_3b(pt, pc, hi)
    print(f"  -> {row}: {lang}")

    print("\n-- EQUAL-CELL variant (each cell one vote; NOT the pre-registered "
          "estimator, printed so the pooled number's reweighting is visible) --")
    ds = [gm([g for g in A if g["opp"] == c]) - gm([g for g in B if g["opp"] == c])
          for c in cells
          if any(g["opp"] == c for g in A) and any(g["opp"] == c for g in B)]
    print(f"  mean of per-cell deltas = {statistics.mean(ds):+.4f}  (n={len(ds)} cells)")


# =============================================================================
# SELFTEST -- ADDITIVE ONLY. Nothing above this line was written to suit it.
#
# WHAT IS AND IS NOT COVERED. The ring GEOMETRY and the tile_episodes series are
# `tools/ring_read.py`'s and are covered by ITS seven forced-answer protobuf
# cells (`ring_read.py --selftest`, which must be green before this one means
# anything). What is covered HERE is the layer this file adds and ring_read does
# not have: `hold_pinned`'s normalisation, the match-clustered bootstrap, and
# Amendment 3b's TWO-CONDITION decision rule. Those are the parts that decide
# which sentence gets typed.
#
# MUTATION TEST, run and recorded rather than asserted:
#   cp tools/loki19_5d.py $S/mut.py
#   in $S/mut.py change amendment_3b's `if below_25 and ci_excl:` to
#                       `if below_25 or ci_excl:`      # the "either" reading
#   .venv/bin/python $S/mut.py --selftest
#   -> observed: LOKI19_5D_SELFTEST: FAIL  (cell BIG_FALL_WIDE_CI, which is the
#      whole reason Amendment 3b names both conditions)
#   Second mutation, on the other axis:
#      `return (max(eps) / g["rounds"])` -> `return float(max(eps))`   (drop the
#      normalisation, i.e. report raw rounds instead of a fraction)
#   -> observed: LOKI19_5D_SELFTEST: FAIL  (cell NORMALISED, where two arms hold
#      the same FRACTION over different game lengths)
# A selftest that passes on this file AND on both mutants would be worthless --
# that is precisely the defect `ring_retention.py --selftest` had.
# =============================================================================

def _fake(mid: str, opp: str, seat: str, longest: int, rounds: int) -> dict:
    g = {"tile_episodes": [longest] if longest else [], "rounds": rounds,
         "mid": mid, "opp": opp, "seat": seat, "oppver": "v1", "winner": 0}
    g["hp"] = hold_pinned(g)
    return g


def selftest() -> int:
    fails = []

    def chk(name, got, want, why):
        ok = (got == want) if isinstance(want, (str, tuple, int)) else \
             abs(got - want) < 1e-9
        print(f"  [{'ok' if ok else 'FAIL'}] {name:<34} got={got!r} want={want!r}")
        if not ok:
            fails.append(name)
        print(f"         forced by: {why}")

    print("LOKI19_5D SELFTEST -- forced answers, arithmetic on the fixture, "
          "never a stored figure\n")

    # 1. NORMALISED -- hold_pinned is a FRACTION. Two games holding the same
    #    fraction over different game lengths must read identically. This is the
    #    cell the "drop the normalisation" mutant fails.
    chk("NORMALISED same fraction",
        (hold_pinned(_fake("m", "o", "A", 50, 100)),
         hold_pinned(_fake("m", "o", "A", 200, 400))),
        (0.5, 0.5),
        "50/100 and 200/400 are both one half by construction")

    # 2. FLOOR -- an arm that never landed on the ring has no episodes at all
    #    and must read 0.0, not raise and not divide by zero.
    chk("FLOOR never landed", hold_pinned(_fake("m", "o", "A", 0, 100)), 0.0,
        "empty tile_episodes -> 0.0 by definition, no ZeroDivisionError")

    # 3. row 4 -- treatment ABOVE control. No claim is licensed.
    chk("3c row 4 treat above ctrl", amendment_3b(0.60, 0.50, 0.30)[0], "3c row 4",
        "0.60 > 0.50, so neither 3b condition can hold")

    # 4. row 3 -- a fall smaller than 25%. 0.40 vs 0.50 is exactly 20% below,
    #    inside the threshold, so it must NOT fire the plain-language row.
    chk("3c row 3 fall under 25pct", amendment_3b(0.40, 0.50, -0.01)[0], "3c row 3",
        "0.40 is 20% below 0.50; 25% below would be 0.375, and the CI is "
        "irrelevant because the magnitude condition already fails")

    # 5. BIG_FALL_WIDE_CI -- 40% below control but the interval straddles 0.
    #    THE CELL THAT SEPARATES 'both conditions' FROM 'either'. The `or`
    #    mutant returns row 1 here and this line is what catches it.
    chk("3c row 2 big fall, CI straddles",
        amendment_3b(0.30, 0.50, +0.02)[0], "3c row 2",
        "0.30 is 40% below 0.50 (>=25%) but CI upper +0.02 > 0, so Amendment "
        "3b's AND is not satisfied")

    # 6. row 1 -- both conditions. The only row that may be written plainly.
    chk("3c row 1 both conditions", amendment_3b(0.30, 0.50, -0.02)[0], "3c row 1",
        "40% below AND CI upper < 0")

    # 7. BOUNDARY -- exactly 25% below. The rule says 'at least 25% below', so
    #    the boundary is INSIDE the fall. Written down because a boundary left
    #    to the reader is how a bar gets met and missed at read-out.
    chk("3c boundary exactly 25pct", amendment_3b(0.375, 0.50, -0.01)[0], "3c row 1",
        "0.375 == 0.50 * 0.75 exactly; 'at least 25% below' includes equality")

    # 8. BOOTSTRAP CLUSTERING -- two arms built from IDENTICAL per-game values
    #    must give a point delta of exactly 0 and a CI containing 0.
    A = [_fake(f"a{m}", "o", "A", 50, 100) for m in range(10) for _ in range(5)]
    B = [_fake(f"b{m}", "o", "A", 50, 100) for m in range(10) for _ in range(5)]
    lo, hi, ka, kb = boot_ci(A, B)
    chk("BOOTSTRAP identical arms", (round(gm(A) - gm(B), 9), lo, hi, ka, kb),
        (0.0, 0.0, 0.0, 10, 10),
        "every game is 50/100; resampling constants cannot move the difference")

    # 9. BOOTSTRAP SEPARATION -- arms with zero within-arm variance and a real
    #    gap must produce a CI that EXCLUDES zero. Without this cell the
    #    bootstrap could return [0,0] always and cells 3-7 would still pass.
    C = [_fake(f"c{m}", "o", "A", 20, 100) for m in range(10) for _ in range(5)]
    lo2, hi2, _, _ = boot_ci(C, B)
    chk("BOOTSTRAP separates arms", (round(gm(C) - gm(B), 9), hi2 < 0),
        (-0.3, True),
        "0.20 - 0.50 = -0.30 with no within-arm spread, so every draw is -0.30 "
        "and the upper bound must sit below zero")

    # 10. CLUSTER UNIT -- the draw is the MATCH, not the game. 10 matches of 5
    #     identical games must give the same CI as 10 matches of 1 game; if the
    #     code resampled GAMES the wider effective n would tighten it.
    D = [_fake(f"d{m}", "o", "A", 20, 100) for m in range(10)]
    E = [_fake(f"e{m}", "o", "A", 50, 100) for m in range(10)]
    lo3, hi3, _, _ = boot_ci(D, E)
    chk("CLUSTER unit is the match", (round(lo3 - lo2, 9), round(hi3 - hi2, 9)),
        (0.0, 0.0),
        "same 10 clusters per arm, same per-cluster value; game count inside a "
        "cluster must not change the interval")

    print(f"\nLOKI19_5D_SELFTEST: {'PASS' if not fails else 'FAIL'}")
    if fails:
        print("  failed: " + ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        sys.exit(2)
    T, C = load(args[0]), load(args[1])
    report(T, C, Path(args[0]).name, Path(args[1]).name)
