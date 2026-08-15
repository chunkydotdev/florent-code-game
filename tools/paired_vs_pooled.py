"""Pooled-vs-paired CI comparison for arena batteries -- AND THE REFUTATION IT PRODUCED.

Promoted to tools/ 2026-08-08 s19 from docs/workflow-analysis/ (third florent
session's methodology work), WITH its negative result attached, because a
refutation that saves a build is worth as much as a positive one and this one
will otherwise be re-derived from scratch in three weeks.

THE HYPOTHESIS: arena.py pools a Wilson interval (:148) while deliberately
playing matches in (map, seed) blocks (:113-118) -- the Fishtest pentanomial
argument says treating blocked matches as i.i.d. Bernoulli inflates the CI, and
pairing should tighten it 3-5x for free.

THE MEASUREMENT (_v97hv vs _v97e11, 15 maps x 6 seeds x 2 orderings = 180):
    POOLED  93/180 = 51.7%  Wilson95 [44.4, 58.9]  half-width 7.22pp
    PAIRED  90 blocks       95%      [44.8, 58.5]  half-width 6.83pp
    RATIO   1.06x -- WORTHLESS.
Block split {lose both 18, split 51, win both 21} against independence's
{21.0, 44.9, 24.1}: slightly MORE splits than independent, not fewer.

WHY, and it is in our own tooling.md:256 -- **NOISE_ON reseeds spawn_salt from
live entropy, so a shared (map, seed) is NOT a shared opening.** The blocking is
cosmetic. sprt.py's docstring worries about the independence assumption; under
NOISE_ON that worry is misplaced.

CONSEQUENCE: variance in our batteries is irreducible per-game noise. Only n
moves it. See tape row leg-power-19pct -- n=120 has 19% power against a true
+5pp plank, n=800 has 81%.

CAVEAT for deterministic (NOISE_OFF) legs: power figures are NOMINAL until
divided by the shape ratio r = distinct shapes / nominal pairs, because
SE scales as 1/sqrt(r). det.py reports that column.
"""
# NOTE 2026-08-15: `from __future__` was at line 49, AFTER a stray second
# shebang and a second docstring -- this file is two files concatenated and
# HAD NEVER COMPILED (verified at git HEAD: SyntaxError). Moved here, the
# minimal change that makes it importable. Its duplicated body is untouched
# and unreviewed: the tool ran zero times, so nothing depended on it.
from __future__ import annotations
#!/usr/bin/env python3
"""READ-ONLY diagnostic: how much of arena.py's stated uncertainty is
between-map variance that cancels in a paired comparison?

Runs the same (map x seed x both seat orderings) grid arena.py runs, then
scores it TWO ways on the SAME matches:

  pooled   -- Wilson 95% on wins/n over all matches, i.i.d. Bernoulli.
              This is what tools/arena.py reports and what the accept rule uses.
  paired   -- block on (map, seed). Each block scores s in {0, 0.5, 1} = the
              candidate's share of that block's 2 games. Estimate = mean(s),
              SE = sd(s)/sqrt(n_blocks). This is the pentanomial/blocked
              estimator (Fishtest's game-pair model).

Writes nothing outside this scratchpad. Touches no bot, no tape, no tool.
"""

import json
import math
import statistics
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
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

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
FCODE = ROOT / ".venv" / "bin" / "fcode"


def play(job):
    bot_a, bot_b, map_path, seed, tle = job
    cmd = [str(FCODE), "run", bot_a, bot_b, map_path, "--seed", str(seed),
           "--tle", str(tle), "--json", "--replay", "/dev/null"]
    pr = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    for line in reversed(pr.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "winner" in res:
                seat = res["winner"].lower()
                return (Path(map_path).stem, seed,
                        bot_a, bot_b, seat,
                        res.get("turns"), res.get("win_condition"))
    return None


def wilson(wins: float, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 1.0)
    p = wins / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def main():
    cand, opp, seeds = sys.argv[1], sys.argv[2], int(sys.argv[3])
    jobs_n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    maps = sorted(ROOT.glob("maps/*.map26"))

    jobs = []
    for mp in maps:
        for seed in range(1, seeds + 1):
            jobs.append((cand, opp, str(mp), seed, 10))
            jobs.append((opp, cand, str(mp), seed, 10))

    print(f"{len(maps)} maps x {seeds} seeds x 2 orderings = {len(jobs)} matches",
          file=sys.stderr)

    rows = []
    with ProcessPoolExecutor(max_workers=jobs_n) as ex:
        for i, r in enumerate(ex.map(play, jobs), 1):
            if r:
                rows.append(r)
            if i % 40 == 0:
                print(f"  {i}/{len(jobs)}", file=sys.stderr)

    # candidate win per match
    blocks = defaultdict(list)
    wins = 0
    for mp, seed, ba, bb, seat, turns, cond in rows:
        winner = ba if seat == "a" else bb
        w = 1 if winner == cand else 0
        wins += w
        blocks[(mp, seed)].append(w)

    n = len(rows)
    p = wins / n
    lo, hi = wilson(wins, n)
    print(f"\nPOOLED (what arena.py's accept rule uses)")
    print(f"  {wins}/{n} = {p:.1%}   Wilson95 [{lo:.1%}, {hi:.1%}]"
          f"   half-width {100*(hi-lo)/2:.2f}pp")

    full = {k: v for k, v in blocks.items() if len(v) == 2}
    scores = [sum(v) / 2 for v in full.values()]
    nb = len(scores)
    mean = statistics.fmean(scores)
    sd = statistics.stdev(scores) if nb > 1 else 0.0
    se = sd / math.sqrt(nb) if nb else 0.0
    print(f"\nPAIRED / blocked on (map, seed)  [pentanomial-style]")
    print(f"  {nb} complete blocks   mean {mean:.1%}   sd(block) {sd:.3f}"
          f"   SE {100*se:.2f}pp   95% [{100*(mean-1.96*se):.1f}%,"
          f" {100*(mean+1.96*se):.1f}%]   half-width {100*1.96*se:.2f}pp")

    dist = defaultdict(int)
    for s in scores:
        dist[s] += 1
    print(f"  block outcome distribution (cand share of the 2 games): "
          f"{ {k: dist[k] for k in sorted(dist)} }")

    pooled_hw = 100 * (hi - lo) / 2
    paired_hw = 100 * 1.96 * se
    if paired_hw > 0:
        ratio = pooled_hw / paired_hw
        print(f"\n  CI half-width ratio pooled/paired = {ratio:.2f}x"
              f"   -> equal precision needs ~{ratio**2:.1f}x "
              f"{'FEWER' if ratio > 1 else 'MORE'} matches under the paired rule")

    # how much of the pooled variance is between-map?
    per_map = defaultdict(list)
    for (mp, seed), v in full.items():
        per_map[mp].append(sum(v) / 2)
    print(f"\n  per-map block means (between-map spread is the component "
          f"pooling leaks into the CI and pairing removes):")
    mm = []
    for mp in sorted(per_map):
        m = statistics.fmean(per_map[mp])
        mm.append(m)
        print(f"    {mp:<14} {m:>6.1%}  n_blocks={len(per_map[mp])}")
    if len(mm) > 1:
        print(f"    between-map sd of block means: {statistics.stdev(mm):.3f}")


if __name__ == "__main__":
    main()
