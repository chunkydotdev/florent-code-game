#!/usr/bin/env python3
"""THE BAR: what is the SMALLEST change our current tools can actually detect?

    .venv/bin/python tools/mde.py <n_games> [maps...]

Magnus, 2026-08-11: *"Figure out the smallest change we can find out using our
current tools, that's the bar."* This measures it rather than assuming it.

METHOD. Play the NULL — a byte-identical renamed copy of the incumbent against
the incumbent — and record the per-game kill-speed score for both sides. The
spread of that difference under a TRUE ZERO effect is the noise floor, and the
minimum detectable effect is

    MDE = (z_{1-a/2} + z_{power}) * sd(diff) / sqrt(n)        = 2.802 * sd / sqrt(n)

for 80% power at a two-sided 5%. Everything else in this repo quotes MDE from a
BINOMIAL on win rate; this measures the CURRENCY's own variance, which is the
quantity that actually governs what we can see.

WHY THE NULL AND NOT A TREATMENT: the noise floor must be measured where the
effect is known to be exactly zero, or the estimate of the floor absorbs part of
the effect. `_v130null` is byte-identical to `_v130loki13` and differs only in
directory name, which is also why identical basenames are refused by h2h.sh.
"""
import statistics, subprocess, sys, math
from pathlib import Path
sys.path.insert(0, "tools")
import score  # noqa

ROOT = Path(__file__).resolve().parent.parent
FC = str(ROOT / ".venv" / "bin" / "fcode")
TREAT, CTRL = "bots/_v130null", "bots/_v130loki13"
TB, CB = "_v130null", "_v130loki13"


def one(mapname, seed, flip):
    a, b = (CTRL, TREAT) if flip else (TREAT, CTRL)
    r = subprocess.run([FC, "run", a, b, f"maps/{mapname}.map26", "--seed", str(seed)],
                       capture_output=True, text=True, cwd=ROOT)
    line = next((l for l in r.stdout.splitlines() if "Winner:" in l), None)
    if not line:
        return None
    treat_won = TB in line
    cond = "core_destroyed" if "Core destroyed" in line else "tiebreak"
    try:
        turns = int(line.split("turn ")[1].rstrip(") "))
    except (IndexError, ValueError):
        return None
    ts = score.game_score(treat_won, cond, turns)
    cs = score.game_score(not treat_won, cond, turns)
    return ts, cs


def main(n, maps):
    diffs, tsc, csc = [], [], []
    seed = 1
    while len(diffs) < n:
        for m in maps:
            for flip in (False, True):
                if len(diffs) >= n:
                    break
                r = one(m, seed, flip)
                if r is None:
                    continue
                ts, cs = r
                tsc.append(ts); csc.append(cs); diffs.append(ts - cs)
        seed += 1
    sd = statistics.pstdev(diffs)
    print(f"NULL, n={len(diffs)} games  (byte-identical copy vs the incumbent)")
    print(f"  treatment mean score {statistics.mean(tsc):+.3f}   "
          f"control mean {statistics.mean(csc):+.3f}")
    print(f"  mean DIFF {statistics.mean(diffs):+.3f}  (must be ~0 — this is the check "
          f"that the floor is a floor)")
    print(f"  sd(diff)  {sd:.3f}   <- THE NOISE FLOOR, in kill-speed points per game")
    print()
    print("  MINIMUM DETECTABLE EFFECT, 80% power, two-sided 5%:")
    print(f"    {'n games':>9}  {'MDE (score/game)':>17}  {'as % of the -10..+10 range':>28}")
    for k in (64, 256, 1024, 4096, 16384, 65536):
        mde = 2.802 * sd / math.sqrt(k)
        print(f"    {k:>9}  {mde:>17.3f}  {100*mde/20:>27.2f}%")
    print()
    print("  Read it as: an arm must move the mean kill-speed score by at least")
    print("  the MDE at the n you can afford, or the run cannot see it AT ALL.")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    maps = sys.argv[2:] or ["antler", "atoll", "drumlin", "fjordgate",
                            "heart", "hive", "meander", "nordkap"]
    main(n, maps)
