"""DENOMINATORS FOR THE SHIP-GATE COLUMNS — `dd_z`, `resolvable_k`, `p_null`,
and the DERIVED activation baseline.

WHY THIS FILE EXISTS. On 2026-08-12 (s33) three instruments in this repo were
found, by three different lanes within four hours, printing a THRESHOLD WITHOUT
ITS DENOMINATOR: `effective_n`'s overstatement ratio with no `seeds_per_cell`,
`overnight_read`'s bands with no calibration, and `ship_watch`'s `drawdown` /
`RULE=SLOT FREE` with no n and no base rate. This module supplies the missing
denominators for the third, as pure functions so they can be driven both ways.

    .venv/bin/python tools/slot_denoms.py --selftest

⛔ EVERY FUNCTION HERE IS PURE AND TAKES ITS DATA AS AN ARGUMENT. That is
deliberate: the defect these columns exist to fix was a monitor consuming a
HAND-SET CONSTANT (`SHIP_BASELINE=1689`) that no measurement produced. A helper
that reads a file it was not handed reintroduces exactly that.

THE THREE COLUMNS, and what each answers:

  dd_z          "is this drawdown bigger than the noise it sits in?"
                net / (sd * sqrt(k)).  A -36 drawdown at k=27 with the tape's
                sd is -0.80 -- inside one sd, i.e. nothing.

  resolvable_k  "how many matches would this holder's OBSERVED rate need before
                it could be called?"  ((z_a+z_b)*sd/|mean|)^2.  At -1.68/match
                the answer is 94 and we routinely decide at 8.

  p_null        "how often would a bot with NO EFFECT AT ALL have freed the
                slot by now?"  14.1% at k=8, 74.6% at k=27, 97.0% at k=60.
                ⭐ THE ASYMMETRY IS THE POINT: `SLOT FREE` is close to
                uninformative on its own because it is the MAJORITY outcome for
                a neutral holder by k=27, while `RULE=held` is the informative
                half -- only ~25% of neutral holders get that far without
                tripping. Nobody was reading it in that direction because the
                column did not exist.

⚠ `p_null` IS A BASE RATE, NOT A p-VALUE. The bootstrap resamples i.i.d.; real
ladder deltas were tested for serial structure (Ljung-Box Q(5)=8.99 against a
95% critical value of 11.07 -- none detectable) and a moving-block bootstrap
(block=10) agreed within 2.2pp, running CONSERVATIVE. So it is robust to serial
structure within ~2pp. Two limits survive that and are not fixable by
resampling: absence of DETECTABLE autocorrelation at n=795 is not proof of
independence, and the sample is US-ONLY.

SEEDED DETERMINISTICALLY, and that is load-bearing rather than tidy: a column
that jitters between polls on identical input reads as signal. Same input ->
same number, forever.
"""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

# alpha = 0.15 one-sided (the SPRT's own alpha), 80% power.
Z_ALPHA = 1.036
Z_BETA = 0.842

SEED = 20260812
TRIALS = 4000          # +-0.6pp at p=0.5; the column is reported to 2 decimals


# ---------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------

def intervals_from_ladder(path: Path | str) -> list[float]:
    """Per-MATCH Elo intervals for our own ladder run, oldest first.

    `ladder_games.tsv` is one row per GAME (five per match), so rows are
    collapsed by `match` id before differencing -- differencing the game rows
    would report four zeros and one delta per match and crush the sd by ~sqrt(5).
    Returns [] on any failure; every caller must treat [] as UNDERIVED rather
    than as a zero.
    """
    try:
        seen = {}
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                seen.setdefault(r["match"], r)
        rows = sorted(seen.values(), key=lambda r: r["created"])
        bef = [float(r["ourbef"]) for r in rows]
        return [bef[i + 1] - bef[i] for i in range(len(bef) - 1)]
    except Exception:
        return []


def activation_baseline(version: str, path: Path | str) -> float | None:
    """The holder's TRUE activation rating: `ourbef` of its FIRST ladder match.

    ⛔ THIS IS THE FIX FOR A DEFECT THE MONITOR DOCUMENTED AND THEN REPRODUCED.
    `ship_watch.py:52-54` records that v102 was armed at 1577.5 -- "the rating
    before v101's LAST game" -- when the true activation rating was 1567.44,
    because "the tape row tagged v102 is not the first v102 MATCH". The repair
    made the ALARM immune to a wrong baseline and left the REPORTING column
    consuming a hand-set env var, so on 2026-08-12 `SHIP_BASELINE=1689` was
    again the `ourbef` of the PREVIOUS holder's last match (v112, 1688.8986)
    while v114's first match carried 1685.6150 -- crediting a -3.28 v112 game to
    v114's drawdown. Two lanes misread the resulting column within one hour.

    The per-match `ourver` on `ladder_games.tsv` is the ground truth CLAUDE.md
    points at; the elo tape's tag is a POLL-TIME tag and carries the defect.
    Returns None if it cannot be derived -- callers print UNDERIVED and never a
    guess.
    """
    tag = str(version).lstrip("vV")
    try:
        seen = {}
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                seen.setdefault(r["match"], r)
        rows = sorted((r for r in seen.values()
                       if str(r["ourver"]).lstrip("vV") == tag),
                      key=lambda r: r["created"])
        return float(rows[0]["ourbef"]) if rows else None
    except Exception:
        return None


def sd_of(xs) -> float | None:
    """Sample sd. None below 2 points -- a one-point sd is 0, and a 0 in a
    denominator is how a column becomes infinite instead of absent."""
    xs = list(xs)
    if len(xs) < 2:
        return None
    mu = sum(xs) / len(xs)
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))


# ---------------------------------------------------------------------------
# the columns
# ---------------------------------------------------------------------------

def dd_z(net: float, k: int, sd: float | None) -> float | None:
    """The drawdown in units of its own noise."""
    if sd is None or sd <= 0 or k is None or k < 1:
        return None
    return net / (sd * math.sqrt(k))


def resolvable_k(mean_per_match: float | None, sd: float | None) -> float | None:
    """Matches needed to call an effect of this SIZE at alpha/power above.

    Returns None at mean == 0: "how long to detect nothing" has no answer, and
    returning a huge number instead would read as a measurement.
    """
    if sd is None or sd <= 0 or not mean_per_match:
        return None
    return ((Z_ALPHA + Z_BETA) * sd / abs(mean_per_match)) ** 2


def p_null(k: int, intervals, threshold: float = -21.0, window: int = 5,
           arm_after: int = 8, trials: int = TRIALS,
           seed: int = SEED) -> float | None:
    """P(a bot with NO EFFECT frees the slot at least once within k matches).

    The intervals are CENTRED first -- that is what makes this a null model
    rather than a description of our actual run. Windows overlap and are
    therefore correlated, which is why this is simulated rather than computed as
    1-(1-p)^n: that closed form assumes independence and materially overstates.
    """
    xs = list(intervals)
    if len(xs) < 2 or k is None or k < arm_after:
        return None
    mu = sum(xs) / len(xs)
    cen = [x - mu for x in xs]
    rng = random.Random(seed)
    fired = 0
    for _ in range(trials):
        cum, tot = [0.0], 0.0
        for _ in range(k):
            tot += cen[rng.randrange(len(cen))]
            cum.append(tot)
        for m in range(arm_after, k + 1):
            if m >= window and cum[m] - cum[m - window] <= threshold:
                fired += 1
                break
    return fired / trials


# ---------------------------------------------------------------------------
# selftest — every cell drives a value that must DIFFER from another cell's
# ---------------------------------------------------------------------------

def selftest() -> int:
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok  ' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
        if not cond:
            fails.append(name)

    print("slot_denoms --selftest")
    sd = 8.667                      # the tape's measured per-match sd, s33

    # --- dd_z: must be small for the real case and large for a real bleed.
    z_real = dd_z(-36.0, 27, sd)
    z_bad = dd_z(-200.0, 27, sd)
    check("dd_z: a -36 drawdown at k=27 is INSIDE one sd (i.e. nothing)",
          -1.0 < z_real < -0.6, f"dd_z={z_real:+.2f}")
    check("dd_z: a -200 drawdown at the same k is far outside",
          z_bad < -4, f"dd_z={z_bad:+.2f}")
    check("dd_z: the two cells DIFFER (the column is not a constant)",
          abs(z_real - z_bad) > 3)
    check("dd_z: no sd -> None, never a number", dd_z(-36.0, 27, None) is None)

    # --- resolvable_k: the three rates from the s33 spec.
    r10, r4, r168 = (resolvable_k(-10.0, sd), resolvable_k(-4.0, sd),
                     resolvable_k(-1.68, sd))
    check("resolvable_k: MU0 fast (-10/match) needs ~3 matches",
          2 <= r10 <= 4, f"k>={r10:.1f}")
    check("resolvable_k: MU0 slow (-4/match) needs ~17",
          15 <= r4 <= 19, f"k>={r4:.1f}")
    check("resolvable_k: v114's observed -1.68/match needs ~94 -- WE DECIDE AT 8",
          88 <= r168 <= 100, f"k>={r168:.1f}")
    check("resolvable_k: mean of exactly 0 -> None, not a huge number",
          resolvable_k(0.0, sd) is None)

    # --- p_null: THE LOAD-BEARING CELLS. k=8 and k=27 must differ materially,
    #     or the column validates anything it is printed beside.
    ivs = [sd * z for z in (-1.7, -1.1, -0.7, -0.4, -0.15, 0.05, 0.25, 0.5,
                            0.8, 1.2, 1.7, -0.9, 0.35, -0.5, 0.65)]
    p8, p27, p60 = p_null(8, ivs), p_null(27, ivs), p_null(60, ivs)
    check("p_null: a NEUTRAL holder frees the slot ~14% of the time by k=8",
          0.09 < p8 < 0.20, f"p={p8:.3f}")
    check("p_null: ...and the MAJORITY of the time by k=27",
          0.60 < p27 < 0.88, f"p={p27:.3f}")
    check("p_null: ...and almost always by k=60", p60 > 0.90, f"p={p60:.3f}")
    check("p_null: k=8 and k=27 DIFFER MATERIALLY (not a constant column)",
          p27 - p8 > 0.35, f"{p8:.3f} -> {p27:.3f}")
    check("p_null: monotone in k", p8 <= p27 <= p60)

    # sd sensitivity: a column that ignores its own sd is the docstring-constant
    # defect one level up.
    tight = p_null(27, [x / 4 for x in ivs])
    check("p_null: MOVES with sd -- quarter the spread, far fewer trips",
          tight < p27 - 0.3, f"tight={tight:.3f} vs {p27:.3f}")

    # determinism: same input twice -> identical, or the column reads as signal.
    check("p_null: DETERMINISTIC (same input -> same number)",
          p_null(27, ivs) == p27)

    # refusals
    check("p_null: below the arming point -> None", p_null(5, ivs) is None)
    check("p_null: too few intervals -> None", p_null(27, [1.0]) is None)

    # --- activation_baseline: derived vs UNDERIVED, driven both ways.
    import tempfile
    hdr = "match\tcreated\topp\toppver\tourver\tourbef\n"
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
    fh.write(hdr)
    # v112's LAST match is the trap: its ourbef is what a hand-set baseline
    # picks up, and it is NOT the next holder's activation rating.
    fh.write("m1\t2026-08-11T19:12:59Z\tX\t4\t112\t1688.8986\n")
    fh.write("m2\t2026-08-11T19:32:59Z\tX\t4\t114\t1685.6150\n")
    fh.write("m2\t2026-08-11T19:32:59Z\tX\t4\t114\t1685.6150\n")   # same match
    fh.write("m3\t2026-08-11T19:52:59Z\tX\t4\t114\t1676.7895\n")
    fh.close()
    got = activation_baseline("v114", fh.name)
    check("activation_baseline: derives the holder's FIRST match, not the "
          "previous holder's last", got is not None and abs(got - 1685.6150) < 1e-6,
          f"got={got}")
    check("...and it is NOT 1688.8986, which is what SHIP_BASELINE=1689 was",
          got is not None and abs(got - 1688.8986) > 3)
    check("activation_baseline: 'v' prefix optional", activation_baseline("114", fh.name) == got)
    check("activation_baseline: unknown holder -> None (UNDERIVED, not a guess)",
          activation_baseline("v999", fh.name) is None)
    check("activation_baseline: missing file -> None",
          activation_baseline("v114", "/nonexistent/nope.tsv") is None)

    # --- intervals_from_ladder must COLLAPSE games to matches.
    ivs2 = intervals_from_ladder(fh.name)
    check("intervals_from_ladder: 3 matches (not 4 game rows) -> 2 intervals",
          len(ivs2) == 2, f"n={len(ivs2)}")
    check("...and it did not emit a spurious 0 for the duplicate game row",
          all(abs(x) > 1e-9 for x in ivs2), f"{[round(x,3) for x in ivs2]}")
    check("intervals_from_ladder: missing file -> [] (UNDERIVED, not [0.0])",
          intervals_from_ladder("/nonexistent/nope.tsv") == [])

    print(f"\n{'SELFTEST PASSED' if not fails else 'SELFTEST FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    import sys
    raise SystemExit(selftest() if "--selftest" in sys.argv else selftest())
