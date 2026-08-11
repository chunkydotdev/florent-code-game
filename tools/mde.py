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
the effect. `_v148null` is byte-identical to the incumbent `_v148ferryfirst` (verified: 0
differing files) and differs only in directory name, which is also why identical
basenames are refused by h2h.sh and overnight.sh.
"""
import statistics, subprocess, sys, math
from pathlib import Path
sys.path.insert(0, "tools")
import score  # noqa

ROOT = Path(__file__).resolve().parent.parent
FC = str(ROOT / ".venv" / "bin" / "fcode")
# ⛔ MOVED s32 2026-08-11. WAS `_v130null` / `_v130loki13` (v104), which was TWO
# SHIPS STALE: v104 -> v112 landed 2026-08-11 13:14Z and `PROGRAMME.md:169` is
# explicit -- *"when a ship lands, EVERY control moves with it"*. A stale control
# measures the wrong contrast and still reads as a valid result. Found by the s32
# instruments audit, not by this file's own selftest, because the selftest cells
# are PURE ARITHMETIC on a stored sd and cannot see which bots produced it.
#
# ⚠ AND THE STORED sd IS STILL THE OLD PAIR'S. The 14.31 in the selftest below
# was measured against the v104 null and every bar quoted from it inherits that.
# RE-MEASURE before quoting a new bar. Reassuringly small in practice: the s32
# audit computed sd(diff) = 14.08 directly off tonight's v112-based shards,
# 1.6% from the stored 14.31 -- so this staleness moved the bar by ~1.6%, not by
# anything that changed a verdict. Recorded as measured, not as reassurance.
TREAT, CTRL = "bots/_v146null", "bots/_v146gunaxis"
TB, CB = "_v146null", "_v146gunaxis"


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


Z = 2.802     # z_{0.975} + z_{0.80}, the 80%-power two-sided-5% constant


def mde(sd, n):
    """Minimum detectable effect. PURE ARITHMETIC — hand-checkable, and the
    reason the selftest below can have forced answers at all."""
    if n <= 0:
        raise ValueError("mde: n must be positive")
    return Z * sd / math.sqrt(n)


def selftest() -> int:
    """⛔ THIS FILE COMPUTES THE BAR EVERY VERDICT IS READ AGAINST, AND IT
    SHIPPED WITHOUT A SELFTEST. Flagged by the side lane as the highest-value
    unbuilt check on the board, and they were right: if this arithmetic is off,
    every screen verdict inherits the error and nothing downstream would show it.

    Forced answers are arithmetic on the fixture, never stored figures.
    """
    fails = []

    def chk(name, got, want, why, tol=1e-9):
        ok = abs(got - want) < tol if isinstance(want, float) else got == want
        print(f"  [{'ok' if ok else 'FAIL'}] {name:<44} got={got!r} want={want!r}")
        print(f"         forced by: {why}")
        if not ok:
            fails.append(name)

    # 1. SCALING. MDE falls as 1/sqrt(n): quadrupling n must HALVE it exactly.
    chk("MDE halves when n quadruples", mde(10.0, 400) / mde(10.0, 100), 0.5,
        "Z*sd/sqrt(4n) over Z*sd/sqrt(n) is exactly 1/2, independent of Z and sd")

    # 2. LINEARITY IN sd. Doubling the noise doubles the MDE.
    chk("MDE doubles when sd doubles", mde(20.0, 64) / mde(10.0, 64), 2.0,
        "MDE is linear in sd by construction")

    # 3. A HAND-COMPUTABLE VALUE. sd=14.31 at n=4096: 2.802*14.31/64.
    chk("hand value sd=14.31 n=4096", round(mde(14.31, 4096), 4),
        round(2.802 * 14.31 / 64.0, 4),
        "sqrt(4096)=64 exactly, so this is 2.802*14.31/64 with no floating slack")

    # 4. THE MEASURED FLOOR REPRODUCES THE PUBLISHED BAR. sd=14.31 overnight
    #    (n=10800) was published to Magnus as 0.39 points/game.
    chk("published overnight bar", round(mde(14.31, 10800), 2), 0.39,
        "the number this session put in front of Magnus as THE BAR; if this "
        "cell ever fails, that figure was wrong when it was quoted")

    # 5. DEGENERATE n MUST RAISE, NOT RETURN A NUMBER. A silent value here
    #    would be a bar computed from nothing.
    try:
        mde(1.0, 0)
        chk("n=0 raises rather than returning", False, True, "n<=0 has no MDE")
    except ValueError:
        chk("n=0 raises rather than returning", True, True,
            "n<=0 has no MDE; returning a number would be a bar computed from "
            "no games")

    # 6. ZERO NOISE MEANS ZERO MDE. Degenerate but it must not blow up.
    chk("sd=0 gives MDE 0", mde(0.0, 64), 0.0,
        "with no variance any non-zero effect is detectable")

    print("")
    print(f"MDE_SELFTEST: {'PASS' if not fails else 'FAIL'}")
    return 1 if fails else 0


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
    if not diffs:
        print("no games completed — cannot measure a floor from nothing", file=sys.stderr)
        return 1
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
        m = mde(sd, k)
        print(f"    {k:>9}  {m:>17.3f}  {100*m/20:>27.2f}%")
    print()
    print("  Read it as: an arm must move the mean kill-speed score by at least")
    print("  the MDE at the n you can afford, or the run cannot see it AT ALL.")


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    except ValueError:
        print(f"usage: mde.py <n_games> [maps...]   (got {sys.argv[1]!r})",
              file=sys.stderr)
        raise SystemExit(2)
    maps = sys.argv[2:] or ["antler", "atoll", "drumlin", "fjordgate",
                            "heart", "hive", "meander", "nordkap"]
    main(n, maps)
