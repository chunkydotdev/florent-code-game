#!/usr/bin/env python3
"""EFFECTIVE n OF A LOCAL BATTERY — how many DISTINCT games are behind a denominator.

WHY THIS EXISTS (QUEUE.md #15, and the s32 measurement that opened it).
A battery run with `NOISE_ON = False` on BOTH sides can play the same game over
and over under different `--seed` values: s32 measured `_v148ferryfirst` vs
`_v148null` at **1 distinct outcome across 6 distinct seeds on 3 of 4 maps**.
When that happens the row count is not the sample size. A 1,024-row battery can
carry ~8-16 distinct games -- a one-to-two-order-of-magnitude overstatement of
precision that is invisible in every denominator we print, on batteries
`gate.py` PASSED because they complied with its own prescription.

⛔⛔ AND THE MIRROR, ADDED s33: `NOISE_ON=True` ALSO DEFEATS SEED CONTROL, THE
OTHER WAY. `_v146gunaxis/main.py:276` is `random.Random().randrange(97)` -- NO
ARGUMENT, so it seeds from the OS and `--seed` has never controlled our spawn
ordering. So False => games DEGENERATE (identical), True => games UNREPRODUCIBLE.
The property that makes a 5,408-row battery honest is the same one that makes a
6-game "paired, same-seed" contrast NOT PAIRED -- demonstrated at 4 gunners vs 17
on the same bot, same seeds, run twice. Read effective n here as a property of a
LARGE battery; it says nothing about whether a small paired contrast is paired.

⛔ THE TRAP THIS TOOL IS BUILT TO AVOID, and it cost the first version of this
analysis a wrong headline. `distinct(winner, cond, turns)` UNDERCOUNTS distinct
games, because `turns` is a bounded integer (~1..1000, in practice ~200 plausible
values per cell). Two genuinely independent games collide on it by pure birthday
chance. Measured on the overnight shards: 338 seeds per cell produced ~245
distinct tuples -- a 1.4x row:distinct ratio that is ALMOST ENTIRELY COLLISION,
not degeneracy. **Reading that 1.4x as "40% of our rows are redundant" would be
wrong.** So the headline statistic here is NOT the distinct count. It is:

  * DEGENERATE CELLS -- cells where every row shares ONE outcome tuple. This is
    the s32 failure exactly, and it is unambiguous: no birthday effect can
    manufacture it, and no independent battery can produce it at n>>1.
  * MODAL SHARE -- the largest fraction of a cell held by a single identical
    outcome tuple. Degeneracy drives this to 1.0; independence leaves it small.

A cell's effective n is reported as its distinct-tuple count, but the VERDICT is
driven by degeneracy and modal share, which are robust to the collision artefact.

POSITIVE AND NEGATIVE CONTROL: `--selftest` builds both a fully degenerate
fixture and a fully independent one and requires the tool to separate them. A
tool that has only ever seen one verdict has not been seen to check -- the
independent fixture is the cell that would have caught the collision trap.

USAGE
  effective_n.py scratchpad/overnight/*.tsv     # report per shard
  effective_n.py --selftest                     # drive it both ways
Rows need columns: map, seed, seat, winner, cond, turns  (the overnight schema).
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict

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

CELL_KEYS = ("map", "seat")
OUTCOME_KEYS = ("winner", "cond", "turns")

# A cell is called DEGENERATE when it has >1 row and exactly 1 distinct outcome.
# MIN_ROWS_FOR_VERDICT keeps a 1-row cell from reading as degenerate by arithmetic.
MIN_ROWS_FOR_VERDICT = 2
# Modal share above this in a large cell is a degeneracy smell even if not exactly 1.0.
MODAL_SHARE_WARN = 0.50


def load(path):
    # ⛔ FILTER `#` LINES BEFORE DictReader. The shard tape now opens with a
    # `# FIXTURE` line carrying the runner's START stamp, and DictReader takes
    # the FIRST line as its fieldnames -- so an unfiltered read would name every
    # column after the fixture header and silently return rows of None.
    with open(path, newline="") as fh:
        body = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(body, delimiter="\t"))


def analyse(rows):
    """Return per-shard stats. Pure; takes dict rows, so the selftest can drive it."""
    cells = defaultdict(list)
    for r in rows:
        try:
            cell = tuple(r[k] for k in CELL_KEYS)
            outcome = tuple(r[k] for k in OUTCOME_KEYS)
        except KeyError as exc:
            raise SystemExit(f"missing column {exc} -- not a battery row file")
        cells[cell].append(outcome)

    degenerate, modal_shares, eff = [], [], 0
    for cell, outcomes in cells.items():
        distinct = len(set(outcomes))
        eff += distinct
        if len(outcomes) >= MIN_ROWS_FOR_VERDICT and distinct == 1:
            degenerate.append((cell, len(outcomes)))
        modal_shares.append(Counter(outcomes).most_common(1)[0][1] / len(outcomes))

    n = len(rows)
    sizes = [len(v) for v in cells.values()]
    k = (sum(sizes) / len(sizes)) if sizes else 0.0        # seeds per cell
    mean_distinct = (eff / len(cells)) if cells else 0.0
    return {
        "rows": n,
        "cells": len(cells),
        "cell_key": CELL_KEYS,
        "seeds_per_cell": k,
        "mean_distinct": mean_distinct,
        "eff_n": eff,
        "ratio": (n / eff) if eff else float("nan"),
        "degenerate_cells": degenerate,
        "max_modal_share": max(modal_shares) if modal_shares else float("nan"),
        "mean_modal_share": (sum(modal_shares) / len(modal_shares)) if modal_shares else float("nan"),
        "at_ceiling": bool(k >= 2 and mean_distinct >= CEILING_FRAC * k),
    }


# ⛔ CEILING. Distinct-outcomes-per-cell is CENSORED ABOVE AT k, the seed budget:
# a cell drawn 3 times can report at most 3 distinct games however many the bots
# could actually produce. When mean distinct/cell sits at the ceiling the statistic
# is measuring THE BUDGET, NOT THE OUTCOME SPACE, and it must not be quoted as an
# overstatement factor. Measured on `NULL114.tsv` (NOISE_ON=True, 16 cells x 338
# seeds), censoring the SAME shard to smaller k:
#     k=2 -> 2.00   k=3 -> 3.00   k=5 -> 5.00   k=10 -> 10.00   (all exactly k)
#     k=50 -> 46.44   k=338 -> 238.44   (truth: 1.4x overstatement)
# So a k=3 read of that shard "predicts" a 112.7x overstatement where the real
# figure is 1.4x. Raised by the side lane against this file's own first output,
# which projected a 30x hazard from k=3 data. The projection was withdrawn.
CEILING_FRAC = 0.98


def verdict(st):
    """DEGENERATE / CEILING / SUSPECT / OK.

    CEILING outranks OK because an unpinned-looking OK at low k is the dangerous
    reading: it says "these games are all distinct" when it can only ever have
    said that. DEGENERATE still outranks CEILING -- a cell that returns 1 distinct
    outcome out of k is BELOW the ceiling and is therefore real information.
    """
    if st["degenerate_cells"]:
        return "DEGENERATE"
    if st.get("at_ceiling"):
        return "CEILING"
    if st["max_modal_share"] >= MODAL_SHARE_WARN:
        return "SUSPECT"
    return "OK"


def report(paths):
    hdr = (f"{'shard':<14}{'rows':>7}{'cells':>7}{'k/cell':>8}{'dist/cell':>10}"
           f"{'eff_n':>8}{'ratio':>7}{'modal':>7}{'degen':>7}  verdict")
    print(f"cell key = {CELL_KEYS}   fingerprint = {OUTCOME_KEYS}")
    print(hdr)
    print("-" * len(hdr))
    worst = "OK"
    for p in paths:
        rows = load(p)
        if not rows:
            print(f"{p:<14}  EMPTY")
            continue
        st = analyse(rows)
        v = verdict(st)
        if v == "DEGENERATE" or (v == "SUSPECT" and worst == "OK"):
            worst = v
        name = p.split("/")[-1].replace(".tsv", "")
        print(f"{name:<14}{st['rows']:>7}{st['cells']:>7}{st['seeds_per_cell']:>8.0f}"
              f"{st['mean_distinct']:>10.2f}{st['eff_n']:>8}"
              f"{st['ratio']:>6.1f}x{st['max_modal_share']:>7.2f}"
              f"{len(st['degenerate_cells']):>7}  {v}")
        if v == "CEILING":
            print(f"    ⛔ AT CEILING: mean distinct/cell {st['mean_distinct']:.2f} of a "
                  f"{st['seeds_per_cell']:.0f}-seed budget. This is measuring THE BUDGET,\n"
                  f"       not the outcome space. `ratio` here is NOT quotable as an "
                  f"overstatement factor.")
        for cell, k in st["degenerate_cells"][:5]:
            print(f"    ⛔ DEGENERATE CELL {cell}: {k} rows, 1 distinct outcome "
                  f"-> this cell's effective n is 1, not {k}")
    print("-" * len(hdr))
    print("NOTE: `ratio` is row:distinct-tuple and is INFLATED BY BIRTHDAY COLLISION on the\n"
          "      bounded `turns` field. It is NOT a redundancy estimate. Read `degen` and\n"
          "      `modal`; they are what separate a degenerate battery from an honest one.")
    return 0 if worst == "OK" else (2 if worst == "DEGENERATE" else 1)


def selftest() -> int:
    """BOTH WAYS. A tool that only ever returns one verdict validates anything."""
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    def row(m, sd, seat, w, turns):
        return {"map": m, "seed": str(sd), "seat": seat,
                "winner": w, "cond": "core_destroyed", "turns": str(turns)}

    maps = ["antler", "atoll", "hive", "meander"]

    # --- NEGATIVE FIXTURE: seed drives nothing. Every seed in a cell replays one game.
    # This is the s32 configuration (NOISE_ON=False both sides) and MUST be caught.
    degen = [row(m, sd, seat, "A", 300)
             for m in maps for seat in "AB" for sd in range(50)]
    st = analyse(degen)
    check("degenerate fixture is flagged DEGENERATE", verdict(st) == "DEGENERATE",
          f"verdict={verdict(st)}")
    check("degenerate fixture: eff_n collapses to the cell count",
          st["eff_n"] == st["cells"] == 8, f"eff_n={st['eff_n']} cells={st['cells']}")
    check("degenerate fixture: 400 rows carry 8 distinct games",
          st["rows"] == 400 and st["eff_n"] == 8, f"{st['rows']} rows -> {st['eff_n']}")
    check("degenerate fixture: modal share is 1.0", st["max_modal_share"] == 1.0)

    # --- POSITIVE FIXTURE: independent games. MUST NOT be flagged.
    # Deterministic pseudo-random so the test is reproducible without a seeded RNG.
    def prng(i):
        return (i * 1103515245 + 12345) & 0x7FFFFFFF

    indep = []
    i = 0
    for m in maps:
        for seat in "AB":
            for sd in range(50):
                i += 1
                h = prng(i)
                indep.append(row(m, sd, seat, "AB"[h & 1], 120 + (h >> 8) % 400))
    st2 = analyse(indep)
    check("independent fixture is NOT flagged DEGENERATE", verdict(st2) != "DEGENERATE",
          f"verdict={verdict(st2)} modal={st2['max_modal_share']:.2f}")
    check("independent fixture: no degenerate cells", not st2["degenerate_cells"])
    check("independent fixture: eff_n is near the row count, not the cell count",
          st2["eff_n"] > 0.7 * st2["rows"], f"eff_n={st2['eff_n']} of {st2['rows']} rows")

    # --- ⛔ THE CEILING CELL. This is the one that would have caught the withdrawn
    # 30x projection, and the cell it REPLACES is the one that certified it: the
    # assertion above ("eff_n is near the row count") reads TRUE at the ceiling by
    # construction, so at low k the tool's own PASS condition was the bug.
    # Same KNOWN-INDEPENDENT games as `indep`, censored to 3 seeds per cell.
    by_cell = defaultdict(list)
    for r in indep:
        by_cell[(r["map"], r["seat"])].append(r)
    censored = [r for v in by_cell.values() for r in v[:3]]
    st4 = analyse(censored)
    check("censored-to-k=3 independent fixture reads CEILING, not OK",
          verdict(st4) == "CEILING",
          f"verdict={verdict(st4)} mean_distinct={st4['mean_distinct']:.2f} k={st4['seeds_per_cell']:.0f}")
    check("censored fixture: mean distinct/cell is pinned AT the seed budget",
          abs(st4["mean_distinct"] - 3.0) < 1e-9,
          f"mean_distinct={st4['mean_distinct']:.2f} of k=3")
    # NOTE, and it is the honest reading rather than a weakened assertion: the
    # UNCENSORED independent fixture ALSO reads CEILING (50.00 of k=50), because
    # its outcome space is wide enough that 50 draws never collide. That is the
    # correct verdict, and it is the point -- CEILING is the DEFAULT state of any
    # well-separated battery, and an overstatement factor is only quotable once
    # collisions appear. The "not at ceiling" case is therefore the COLLISION
    # fixture, asserted below, not this one. A first draft asserted the opposite
    # here and FAILED, which is how the distinction got found.
    # A degenerate cell is BELOW ceiling and must still win -- it is real information.
    # degen[:3] is one cell (antler/A) drawn 3 times, all identical: k=3, distinct=1.
    st5 = analyse(degen[:3])
    check("degeneracy still outranks CEILING at low k",
          verdict(st5) == "DEGENERATE",
          f"verdict={verdict(st5)} mean_distinct={st5['mean_distinct']:.2f} k={st5['seeds_per_cell']:.0f}")

    # --- THE COLLISION CELL. This is the one that would have caught the wrong headline.
    # Independent games over a NARROW turns range collide by birthday alone. The ratio
    # must move a lot while the verdict must NOT, or `ratio` is being read as redundancy.
    narrow = []
    i = 0
    for m in maps:
        for seat in "AB":
            for sd in range(50):
                i += 1
                h = prng(i)
                narrow.append(row(m, sd, seat, "AB"[h & 1], 200 + (h >> 8) % 6))
    st3 = analyse(narrow)
    check("collision fixture: ratio inflates well above 1.0",
          st3["ratio"] > 2.0, f"ratio={st3['ratio']:.1f}x on INDEPENDENT games")
    check("collision fixture: verdict still NOT degenerate (ratio is not redundancy)",
          not st3["degenerate_cells"], f"verdict={verdict(st3)}")
    # THE OTHER HALF OF THE CEILING PAIR: real collisions pull mean distinct/cell
    # off the ceiling, so this fixture -- and only this one -- is quotable as a
    # ratio. Without this cell, CEILING could be a constant that fires on everything.
    check("collision fixture is NOT at ceiling (so its ratio IS quotable)",
          verdict(st3) != "CEILING",
          f"verdict={verdict(st3)} mean_distinct={st3['mean_distinct']:.2f} "
          f"of k={st3['seeds_per_cell']:.0f}")

    # --- Guard: a 1-row cell must not read as degenerate by arithmetic.
    single = [row("antler", 1, "A", "A", 300)]
    check("a 1-row cell is not called degenerate", not analyse(single)["degenerate_cells"])

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)} cell(s): {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED — the tool was driven to DEGENERATE and to OK, and the\n"
          "collision cell confirms `ratio` alone does not decide the verdict.")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    if "--selftest" in sys.argv[1:]:
        return selftest()
    if not args:
        print(__doc__)
        return 64
    return report(args)


if __name__ == "__main__":
    sys.exit(main())
