#!/usr/bin/env python3
"""cluster_ci.py -- an estimate ARRIVES WITH ITS INTERVAL, or it does not arrive.

WHY THIS EXISTS, and it is one specific failure repeated three times in one
session (research arm, s48, 2026-08-17).  Every one of that session's three
directional retractions had the SAME shape:

    the point estimate was quoted, THEN the uncertainty was computed,
    and the uncertainty killed the direction.

  * "we are the field's worst victim of belt-cutting and we repair at the
    floor"          -> died when the ourver SPLIT was applied.
  * "our forward gunners plant in the right band but do not convert"
                    -> died when the ourver SPLIT was applied.
  * "Sleipnir raised the eco/sentinel coupling, 0.809 -> 1.164"
                    -> died when a MATCH-CLUSTER BOOTSTRAP gave
                       [-14.712, +1.846] on 22 matches.

The lane's first response was to adopt an ordering rule: *compute the interval
BEFORE the sentence*.  The side lane refused that fix, correctly, and the
argument is worth repeating in full because it generalises far past this file:

    "Two ordering rules were named today and the other one failed on its
     first test.  FIRINGS-BEFORE-PRIMARY was adopted 2026-08-16 and inverted
     the very first time a verdict was typed under time pressure.  An
     ordering rule held by INTENTION is exactly the class that breaks when
     the clock is tight, which is precisely when it matters.  It wants the
     treatment control_pin got: the mechanism holds and the attention does
     not, so this is a tool that exits nonzero, not a paragraph."

So: no ordering to get wrong.  The interval is computed by the same call that
computes the estimate, and there is no code path that returns one without the
other.

------------------------------------------------------------------------------
WHY *MATCH* IS THE CLUSTER, AND WHY A DEFF CONSTANT IS NOT ENOUGH

`CLAUDE.md` carries measured design effects (rated 1.529 pooled / 1.366
within-opponent; unrated 1.833 / 1.434) and they are written for SHARES.  Two
consequences everyone was getting wrong:

  1. A REGRESSION COEFFICIENT HAS THE SAME CLUSTER AND NO PUBLISHED CONSTANT.
     The 5 games of a match share the opponent, the opponent's version and one
     20-minute slice of the ladder.  That is as true of a slope as of a share.
     The s48 slope cell was 92 games from 22 matches -- mbar = 4.2, essentially
     the maximum clustering the fixture permits -- and it was quoted naked
     because "there is no DEFF for a slope".

     THAT WAS THE RIGHT INSTINCT AND THE WRONG STOPPING POINT.  No closed form
     is needed.  A cluster bootstrap makes no distributional assumption, works
     for ANY statistic you can write as a function of the rows, and is ten
     lines.

  2. THE CLUSTER MUST BE ENUMERATED, NOT ASSUMED.  `CLAUDE.md` is explicit that
     the design effect is a PROCEDURE and not a lookup table: name every
     cluster the data has, state whether YOUR stratum can hold more than one
     member of it, and VERIFY that rather than asserting it.  A per-MAP cut,
     for instance, kills the match cluster outright -- a 5-game match uses five
     DIFFERENT maps, so (match, map) pairs with more than one game numbered
     0 of 415 -- while the OPPONENT cluster survives it.  This tool takes the
     cluster column as an ARGUMENT for exactly that reason; it will not guess.

     ** A correction applied where it does not belong inflates intervals for
        nothing and fails in the FLATTERING direction for a null.  Both over-
        and under-correction are errors.  Only the enumeration catches either. **

------------------------------------------------------------------------------
DIRECTION, because widening does not make every claim harder

Widening an interval only ever makes an EXCLUSION claim harder (superiority,
harm-exclusion, closure-by-upper-bound).  It makes a FAIL-TO-EXCLUDE claim
EASIER -- "no significant rise", "consistent with zero", a null banked because
nothing cleared.  So a fail-to-exclude claim must FIRST be restated as an
exclusion (does the CI exclude the regression bar?) and only then corrected.
Applied to the unrestated form, clustering launders a weak null into a
confident one.  `--null` exists to force that restatement: give it the bar and
the tool answers EXCLUDES / DOES-NOT-EXCLUDE rather than leaving you to eyeball
whether an interval "contains" something.

------------------------------------------------------------------------------
USAGE

    tools/cluster_ci.py --tsv rows.tsv --cluster match --value won
    tools/cluster_ci.py --tsv rows.tsv --cluster match --x first_deliv --y first_sent
    tools/cluster_ci.py --tsv rows.tsv --cluster match --x d --y s --stratum map
    tools/cluster_ci.py --tsv rows.tsv --cluster match --value won --null 0.5133
    tools/cluster_ci.py --selftest

  --value V              statistic = MEAN of column V (a share, if V is 0/1)
  --x X --y Y            statistic = SLOPE of Y on X
  --stratum S            de-mean x and y within S before the slope
                         (the within-map / fixed-effects form)
  --cluster C            resampling unit.  REQUIRED.  Pass the column whose
                         members share a common shock -- normally `match`.
  --null Z               restate as an exclusion against Z and say which way
  -B N                   bootstrap resamples (default 2000)
  --seed N               default 20260817; runs are reproducible by default
                         because an irreproducible interval is not evidence

Exit codes:  0 the estimate is reported.  2 the input cannot support an
estimate (too few clusters, no variance, missing columns) -- and it says so
instead of printing a number.  ** A tool that prints an estimate it cannot
support is the failure this file exists to prevent, so the refusal is loud. **

MIN_CLUSTERS = 8 is a floor, not a blessing: below it the bootstrap has too few
distinct units to resample and the interval means nothing.  Above it the
interval can still be enormous -- that is the tool WORKING (see the s48 cell:
22 matches, [-14.712, +1.846]).
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import defaultdict

# ---------------------------------------------------------------------------
# THE TWO THRESHOLDS, AND THEY ARE CONVENTIONS RATHER THAN DERIVED CONSTANTS.
# Saying so is the point: the side lane asked "is 8 a derived floor or a round
# number?" and the honest answer is a round number, so the design is arranged
# so that being wrong about the exact value cannot produce a confident error.
#
#   MIN_CLUSTERS        below this, refuse outright -- too few distinct units
#                       to resample at all.
#   EXCLUSION_MIN_CLUSTERS
#                       below this, print the interval but ISSUE NO VERDICT.
#
# WHY THE SECOND ONE EXISTS, and it is the failure the first one does NOT
# cover.  A cluster bootstrap between roughly 8 and 30 clusters is a known-poor
# regime: the percentile interval does not have its nominal coverage, AND THE
# ERROR IS NOT CONSERVATIVE IN A PREDICTABLE DIRECTION.
#
#   * spuriously NARROW -> a false EXCLUDES, i.e. a confident wrong claim;
#   * spuriously WIDE   -> a false DOES-NOT-EXCLUDE, which per CLAUDE.md's
#                          direction clause is the one that LAUNDERS a real
#                          effect into "consistent with zero" and flatters a
#                          null.
#
# ** Both directions are live, so below EXCLUSION_MIN_CLUSTERS the tool
#    reports the interval and refuses BOTH verdicts.  A warning a reader can
#    skim past is not enough when the number itself is the hazard. **
#
# The s48 cell that motivated this sits at 22 clusters -- inside the bad
# regime -- and happened to return a visibly enormous interval.  It could
# equally have returned a narrow one, and then the warning would have been the
# only thing between a reader and a confident wrong exclusion.
MIN_CLUSTERS = 8
EXCLUSION_MIN_CLUSTERS = 30
DEFAULT_SEED = 20260817
DEFAULT_B = 2000


# --------------------------------------------------------------------------
# statistics.  Each takes rows already grouped into clusters and returns a
# float or None.  None means "this resample cannot support the statistic",
# which the bootstrap loop drops rather than counting as zero.
# --------------------------------------------------------------------------

def stat_mean(rows, _):
    vals = [r["_v"] for r in rows]
    return sum(vals) / len(vals) if vals else None


def stat_slope(rows, stratum):
    """OLS slope of y on x.  With a stratum, de-mean within it first -- the
    fixed-effects form, which is what "within-map slope" means."""
    groups = defaultdict(list)
    for r in rows:
        groups[r["_s"] if stratum else ""].append(r)
    num = den = 0.0
    for _, pts in groups.items():
        if len(pts) < 2:
            continue
        mx = sum(p["_x"] for p in pts) / len(pts)
        my = sum(p["_y"] for p in pts) / len(pts)
        num += sum((p["_x"] - mx) * (p["_y"] - my) for p in pts)
        den += sum((p["_x"] - mx) ** 2 for p in pts)
    return num / den if den else None


# --------------------------------------------------------------------------

def cluster_bootstrap(by_cluster, statfn, stratum, B, seed):
    """Resample CLUSTERS with replacement, recompute, return sorted estimates.

    Resampling whole clusters -- not rows -- is the entire point: it reproduces
    the fact that all 5 games of a match arrive or do not arrive together."""
    rng = random.Random(seed)
    keys = list(by_cluster)
    out = []
    for _ in range(B):
        rows = []
        for _ in range(len(keys)):
            rows.extend(by_cluster[rng.choice(keys)])
        s = statfn(rows, stratum)
        if s is not None:
            out.append(s)
    out.sort()
    return out


def _row_bootstrap_MUTANT(by_cluster, statfn, stratum, B, seed):
    """THE MUTATION, SHIPPED ON PURPOSE.  Resamples ROWS, ignoring clusters --
    i.e. the exact bug this whole file exists to prevent.

    It is here so `selftest()` can inject it and PROVE that the discriminating
    case still discriminates.  See case F.  Never call it from `analyse`."""
    rng = random.Random(seed)
    allrows = [r for rows in by_cluster.values() for r in rows]
    out = []
    for _ in range(B):
        rows = [rng.choice(allrows) for _ in range(len(allrows))]
        s = statfn(rows, stratum)
        if s is not None:
            out.append(s)
    out.sort()
    return out


def pct(sorted_vals, p):
    if not sorted_vals:
        return None
    i = int(p * (len(sorted_vals) - 1))
    return sorted_vals[i]


def analyse(rows, cluster, statfn, stratum, B, seed, null, _boot=None):
    """_boot=None means LOOK THE BOOTSTRAP UP AT CALL TIME.

    ⛔ It used to be `_boot=cluster_bootstrap`, a default argument bound at def
    time -- which meant an auditor patching the MODULE ATTRIBUTE
    (`m.cluster_bootstrap = ...`, the obvious way to mutate this file) would
    not be seen by `analyse` at all.  The selftest would then pass against a
    module the auditor believed they had broken: a green result for the wrong
    reason, in the exact class of silent failure this file exists to close.
    Self-found while documenting the injection point for the side lane's
    harness; fixed before it bit anyone."""
    if _boot is None:
        _boot = globals()["cluster_bootstrap"]
    by_cluster = defaultdict(list)
    for r in rows:
        by_cluster[r["_c"]].append(r)
    n_cl = len(by_cluster)
    if n_cl < MIN_CLUSTERS:
        return None, f"REFUSED: {n_cl} clusters, below MIN_CLUSTERS={MIN_CLUSTERS}. Too few units to resample; no interval is meaningful."
    point = statfn(rows, stratum)
    if point is None:
        return None, "REFUSED: the statistic is undefined on this input (no variance in x, or no usable stratum)."
    boots = _boot(by_cluster, statfn, stratum, B, seed)
    if len(boots) < B * 0.5:
        return None, f"REFUSED: only {len(boots)} of {B} resamples produced a defined statistic. The estimate is not stable enough to quote."
    lo, hi = pct(boots, 0.025), pct(boots, 0.975)
    mbar = len(rows) / n_cl
    res = {
        "point": point, "lo": lo, "hi": hi, "n": len(rows),
        "clusters": n_cl, "mbar": mbar, "B": len(boots),
    }
    if null is not None:
        res["null"] = null
        res["excludes"] = (lo > null) or (hi < null)
        res["verdict_issued"] = n_cl >= EXCLUSION_MIN_CLUSTERS
    return res, None


def report(res, label):
    print(f"{label}")
    print(f"  point estimate          {res['point']:+.4f}")
    print(f"  cluster-bootstrap 95%   [{res['lo']:+.4f}, {res['hi']:+.4f}]"
          f"   ({res['B']} resamples)")
    print(f"  n rows {res['n']}   clusters {res['clusters']}   mean rows/cluster {res['mbar']:.2f}")
    if res["clusters"] < EXCLUSION_MIN_CLUSTERS:
        print(f"  ** {res['clusters']} clusters is BELOW EXCLUSION_MIN_CLUSTERS={EXCLUSION_MIN_CLUSTERS}.")
        print(f"     A percentile interval does not have nominal coverage in this regime,")
        print(f"     and the error is NOT conservative in a predictable direction. **")
    if "null" in res:
        if not res["verdict_issued"]:
            print(f"  vs null {res['null']:+.4f}:  ** NO VERDICT ISSUED **")
            print(f"     Too few clusters to support EITHER direction: a spuriously NARROW")
            print(f"     interval would give a false EXCLUDES, and a spuriously WIDE one a")
            print(f"     false DOES-NOT-EXCLUDE, which launders a real effect into a null.")
            print(f"     The interval above is DESCRIPTIVE. Get more clusters, not more games.")
        else:
            verdict = "EXCLUDES" if res["excludes"] else "DOES NOT EXCLUDE"
            print(f"  vs null {res['null']:+.4f}:  {verdict}")
            if not res["excludes"]:
                print(f"  ** DOES-NOT-EXCLUDE is NOT 'no effect'. State the largest effect the")
                print(f"     interval fails to exclude -- here {res['lo']:+.4f} on the low side,")
                print(f"     {res['hi']:+.4f} on the high side -- never the half-width. **")


# --------------------------------------------------------------------------

def load(path, cluster, value, x, y, stratum):
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            try:
                out = {"_c": r[cluster]}
                if value is not None:
                    out["_v"] = float(r[value])
                else:
                    out["_x"] = float(r[x])
                    out["_y"] = float(r[y])
                if stratum:
                    out["_s"] = r[stratum]
            except (KeyError, ValueError, TypeError):
                continue
            rows.append(out)
    return rows


def selftest():
    """Drive BOTH verdicts on data whose right answer is known by construction.

    A guard that has never produced the other verdict has not been seen to
    check.  So: the SAME point estimate, once with independent clusters (where
    the naive reading is right and the interval excludes the null) and once
    with the rows glued into a few clusters (where it must not).  If clustering
    made no difference the second case would pass and the tool would be inert.
    """
    ok = True
    rng = random.Random(1)

    # CASE A -- 200 independent clusters, true share 0.62 vs a 0.50 null.
    rows = [{"_c": f"m{i}", "_v": 1.0 if rng.random() < 0.62 else 0.0}
            for i in range(200)]
    res, err = analyse(rows, "match", stat_mean, None, 500, 7, 0.50)
    assert err is None, err
    print(f"  A independent clusters      point {res['point']:+.4f} "
          f"[{res['lo']:+.4f},{res['hi']:+.4f}] excludes-0.50={res['excludes']}")
    if not res["excludes"]:
        print("  ** FAIL: case A should EXCLUDE the null **"); ok = False

    # CASE B -- 200 observations glued into 40 clusters of 5 perfectly
    # correlated rows: a fifth of the independent information.
    #
    # ⛔ TWO CONSTRAINTS ON THIS FIXTURE, BOTH LEARNED THE HARD WAY, AND THEY
    #    PULL AGAINST EACH OTHER:
    #  * clusters must be ABOVE EXCLUSION_MIN_CLUSTERS, or the case tests the
    #    gate instead of the clustering;
    #  * the point estimate must be FAR ENOUGH FROM THE NULL that removing
    #    clustering CROSSES it.  A first re-cut of this case sat at +0.55 and
    #    the row-resampled interval still straddled 0.50 -- so the mutation
    #    narrowed the interval by 53% and the assertion never noticed.  ** The
    #    case passed in both states and its discriminating power was gone. **
    #    (Caught by the side lane re-running the mutation after the edit.)
    # 25 of 40 clusters positive => point 0.625, deterministic, not sampled.
    rows_b = []
    for c in range(40):
        v = 1.0 if c < 25 else 0.0
        rows_b.extend({"_c": f"m{c}", "_v": v} for _ in range(5))
    res_b, err = analyse(rows_b, "match", stat_mean, None, 500, 7, 0.50)
    assert err is None, err
    print(f"  B clustered, same n         point {res_b['point']:+.4f} "
          f"[{res_b['lo']:+.4f},{res_b['hi']:+.4f}] excludes-0.50={res_b['excludes']} "
          f"(verdict issued={res_b['verdict_issued']})")
    if res_b["excludes"]:
        print("  ** FAIL: case B must NOT exclude -- 40 glued clusters are not 200 games **")
        ok = False
    if not res_b["verdict_issued"]:
        print("  ** FAIL: case B has 40 clusters and MUST issue a verdict, else it is")
        print("     testing the gate rather than the clustering **")
        ok = False

    # CASE E -- the low-cluster regime must issue NO VERDICT in either
    # direction, even when the interval happens to look decisive.
    rows_e = [{"_c": f"m{i}", "_v": 1.0} for i in range(12)]
    res_e, err = analyse(rows_e, "match", stat_mean, None, 300, 7, 0.50)
    assert err is None, err
    print(f"  E 12 clusters, degenerate   point {res_e['point']:+.4f} "
          f"[{res_e['lo']:+.4f},{res_e['hi']:+.4f}] verdict issued={res_e['verdict_issued']}")
    if res_e["verdict_issued"]:
        print("  ** FAIL: 12 clusters is inside the bad regime; NO verdict may be issued,")
        print("     because a spuriously narrow interval here is a confident wrong claim **")
        ok = False

    # CASE C -- the refusal must fire, not degrade into a number.
    res_c, err = analyse([{"_c": f"m{i}", "_v": 1.0} for i in range(3)],
                         "match", stat_mean, None, 100, 7, None)
    if res_c is not None or "REFUSED" not in (err or ""):
        print("  ** FAIL: case C should REFUSE (3 clusters) **"); ok = False
    else:
        print(f"  C too few clusters          {err.split('.')[0]}")

    # CASE D -- slope, and the stratum must actually change the answer.
    pts = []
    for g, shift in (("mapA", 0), ("mapB", 100)):
        for i in range(60):
            pts.append({"_c": f"m{g}{i//5}", "_s": g,
                        "_x": i + shift, "_y": 0.5 * i + shift * 3 + rng.random()})
    flat, _ = analyse(pts, "match", stat_slope, None, 300, 7, None)
    within, _ = analyse(pts, "match", stat_slope, "map", 300, 7, None)
    print(f"  D slope pooled {flat['point']:+.3f}   within-stratum {within['point']:+.3f}")
    if abs(within["point"] - 0.5) > 0.1:
        print("  ** FAIL: within-stratum slope should recover 0.5 **"); ok = False
    if abs(flat["point"] - within["point"]) < 0.5:
        print("  ** FAIL: the stratum should have CHANGED the answer; if it does not,")
        print("     the fixed-effects path is not being exercised **"); ok = False

    # CASE F -- ⭐⭐ THE SELFTEST TESTS ITSELF.  Inject the mutation (resample
    # ROWS, ignoring clusters) and require case B's verdict to FLIP.
    #
    # WHY THIS CASE EXISTS AND WHY IT IS THE MOST IMPORTANT ONE HERE.  Case B's
    # job is to fail when clustering is broken.  NO ASSERTION ABOUT B'S OWN
    # OUTPUT CAN GUARANTEE THAT -- and a fixture edit destroyed exactly that
    # property once already, silently, while B kept passing.  The side lane's
    # rule, which this case implements:
    #
    #    "A selftest's discriminating power is not preserved by assertions;
    #     it is preserved by RE-RUNNING THE MUTATION after every edit to the
    #     fixture.  Editing a test case silently destroys the thing the case
    #     was for, and the edited case still passes -- which is exactly why
    #     it is silent."
    #
    # So the mutation lives in the file.  "This selftest has been seen to fail"
    # becomes a property of the code rather than of whoever last remembered to
    # check.  Same move as the tool itself: out of attention, into mechanism.
    res_f, err = analyse(rows_b, "match", stat_mean, None, 500, 7, 0.50,
                         _boot=_row_bootstrap_MUTANT)
    assert err is None, err
    print(f"  F MUTATION (rows not clusters) same point {res_f['point']:+.4f} "
          f"[{res_f['lo']:+.4f},{res_f['hi']:+.4f}] excludes-0.50={res_f['excludes']}")
    if res_f["point"] != res_b["point"]:
        print("  ** FAIL: the mutation must not change the POINT estimate -- if it does,")
        print("     case F is testing something other than the interval **"); ok = False
    if not res_f["excludes"]:
        print("  ** FAIL: with clustering REMOVED, case B's data must EXCLUDE 0.50.")
        print("     It does not, so case B cannot detect a broken bootstrap and its")
        print("     discriminating power is gone. Move B's point further from the null. **")
        ok = False
    wc = res_b["hi"] - res_b["lo"]
    wf = res_f["hi"] - res_f["lo"]
    collapse = 1 - wf / wc if wc else 0.0
    # ⛔ AND F IS ALSO A SECOND, INDEPENDENT DETECTOR: if the SHIPPED bootstrap
    # has itself been replaced by a row resampler, F compares mutant to mutant,
    # the widths match, and its excludes-assertion passes VACUOUSLY.  Requiring
    # a real collapse catches that -- without this line F prints "Case B bites"
    # in exactly the state where nothing bites.
    if collapse < 0.30:
        print(f"  ** FAIL: removing clustering collapsed the interval by only "
              f"{100 * collapse:.0f}% ({wc:.4f} -> {wf:.4f}).")
        print("     Either the fixture has too little clustering to matter, or the")
        print("     SHIPPED bootstrap is already resampling rows and F is comparing")
        print("     the mutant against itself. **")
        ok = False
    elif res_f["excludes"]:
        print(f"    interval width {wc:.4f} clustered -> {wf:.4f} mutated "
              f"({100 * collapse:.0f}% collapse), and the verdict FLIPS. Case B bites.")

    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tsv")
    ap.add_argument("--cluster", help="column whose members share a shock; normally `match`")
    ap.add_argument("--value", help="statistic = mean of this column")
    ap.add_argument("--x")
    ap.add_argument("--y", help="with --x: statistic = slope of y on x")
    ap.add_argument("--stratum", help="de-mean x and y within this column first")
    ap.add_argument("--null", type=float, help="restate as an exclusion against this value")
    ap.add_argument("-B", type=int, default=DEFAULT_B)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.tsv or not a.cluster:
        ap.error("--tsv and --cluster are required (the cluster is never guessed)")
    if a.value is None and (a.x is None or a.y is None):
        ap.error("give either --value, or both --x and --y")

    rows = load(a.tsv, a.cluster, a.value, a.x, a.y, a.stratum)
    if not rows:
        print("REFUSED: no usable rows (check column names and that values parse).",
              file=sys.stderr)
        return 2
    statfn = stat_mean if a.value is not None else stat_slope
    label = (f"MEAN of `{a.value}`" if a.value is not None
             else f"SLOPE of `{a.y}` on `{a.x}`"
                  + (f", within `{a.stratum}`" if a.stratum else ""))
    label += f"   [clustered on `{a.cluster}`]"
    res, err = analyse(rows, a.cluster, statfn, a.stratum, a.B, a.seed, a.null)
    if err:
        print(err, file=sys.stderr)
        return 2
    report(res, label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
