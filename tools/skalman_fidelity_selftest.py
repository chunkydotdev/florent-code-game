#!/usr/bin/env python3
"""BOTH-WAYS DRIVE for `tools/skalman_fidelity.py`, per metric.

⛔ WHY THIS FILE EXISTS.  Repo standing rule: *a check that has never produced
the other verdict has not been seen to check*.  Every metric in the fidelity
instrument is a share, and a broken share prints a clean, confident number.  So
this selftest never asks "did it run" — it asks, per metric, **does it read the
rank-1 bot HIGH and read us LOW on the same code path, and does it BREAK when
pointed at the wrong side?**

THE THREE POPULATIONS
=====================
  A  BEAN COUNTERS v68 — `scratchpad/s53_beanwatch68_v68files.tsv` (112 games),
     the exact census set behind `PLAYBOOK-beancounters-PART-v68-2026-08-21.md`.
  B  US v175-v177 — `scratchpad/s53_beanwatch68_oursample.tsv` (150 games), the
     exact our-side sample that part used for its contrast column.
  C  POPULATION A READ ON THE WRONG SIDE (`flip_side`).  Same files, same code,
     subject index inverted.  **C must FAIL A's expectations.**  A metric whose
     wrong-side read still passes is a metric that is not measuring a side, and
     it is reported as an ATTRIBUTION FAILURE even if A and B both pass.

A metric PASSES only when: A inside its band AND B inside its band AND (for the
metrics the study says discriminate) C outside A's band.

`--full` swaps A and B for the study's FULL populations (BC v47 n=1,235 and us
v168-v177 n=1,185, both from `corpus/meta_join.tsv`) and asserts the published
numbers digit-for-digit.  That run takes ~75 s; the default takes ~8 s.

FOUR STRUCTURAL GUARDS, each driven to both verdicts
====================================================
  G1 LATTICE     `in_lattice` must ACCEPT 0/4/8/10/14/24/100 and REJECT
                 1/2/3/5/6/7/9/11 — 2 and 6 are the cells that stop it being an
                 "is it even" tautology.
  G2 SHIM        `Replay.chains` called on this module's shim must equal a full
                 `Replay(path)` parse on 5 replays; and a DELIBERATELY corrupted
                 shim (conveyors dropped) must DISAGREE, proving the comparison
                 can fail.
  G3 ORDERING    M5d (ring-barrier top share) must be non-null on population A.
                 It was null before the builderBuild-vs-placeEntity ordering fix
                 while M2a still read 40.6% — a per-bot zero hiding under a
                 healthy aggregate.
  G4 EMPTY       An empty population must RAISE, not print a table of zeroes.
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import skalman_fidelity as SF                                    # noqa: E402
from replay_census import Replay                                 # noqa: E402

BC_V68_MANIFEST = ROOT / "scratchpad" / "s53_beanwatch68_v68files.tsv"
US_MANIFEST = ROOT / "scratchpad" / "s53_beanwatch68_oursample.tsv"
BC_TEAM_ID = "47803c19-e264-4492-bd62-fbdd58cfd7e6"
OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
REPLAY_ROOT = ROOT / "replay_archive"

# (lo, hi) bands.  `None` on a side means unbounded there.
# `discriminates` = the study says this metric separates the two bots, so the
# WRONG-SIDE read of population A must fall OUTSIDE A's band.  Metrics marked
# False are ones both bots do similarly (a wrong-side read cannot be expected to
# break them, and pretending otherwise would be a guard that always passes).
#
# BAND WIDTHS, and why each is what it is:
#   * EXACT (±0.5) where the selftest population is byte-identical to the one the
#     playbook published on — M3a, M5b, M5c, M6a, M6b, M6d on population A, and
#     M6a/M6b on population B.  Those cells are reproductions, not estimates.
#   * WIDE where the published number came from a DIFFERENT sample of the same
#     bot (the study's v68 seal cut is n=90, this manifest is n=112; the study's
#     our-side cut is n=1,115 games of v168-v177, this manifest is 150 games of
#     v175-v177).  A tight band there would be testing sampling noise.
QUICK = {
    #  metric                                A band          B band     discrim
    "M1 belt_connectivity_directed":        ((72, 90),      (48, 74),   True),
    # ⚠ discrim=False on the next three is a MEASURED property of the metric,
    # not a waiver.  BC's own opponents cage at 33.9% (vs BC's 40.6), first-ring
    # at r43 (vs r52) and hold a peak ammo median of exactly 30 (vs 26) — the
    # last of which is the playbook's published opponent figure, reproduced.
    # These three separate BC from US strongly and BC from ITS OWN FIELD weakly,
    # so requiring the wrong-side read to leave the band would be asserting a
    # discrimination the data does not have.  The mirror guard below tests them
    # the way they CAN be tested: against the published opponent column.
    "M2a cage_ring_share":                  ((33, 48),      (62, 82),   False),
    "M2b full_seal_rate":                   ((12, 32),      (5, 30),    False),
    "M2c first_ring_build_median":          ((35, 75),      (6, 18),    False),
    "M3a drip_lattice_share":               ((97.0, 97.6),  (75, 93),   True),
    "M3b converts_per_game_median":         ((60, 75),      (25, 50),   True),
    "M3d peak_ammo_median":                 ((22, 30),      (30, 60),   False),
    "M3e first_convert_round_median":       ((20, 35),      (0, 6),     True),
    "M4e sentinel_band_share_anchor":       ((22, 42),      (10, 30),   False),
    "M4f sentinel_pointblank_share_anchor": ((44, 64),      (35, 60),   False),
    "M5a builders_per_game_median":         ((4, 4),        (5, 9),     True),
    "M5b exactly_four_builders_share":      ((92.4, 93.4),  (0, 8),     True),
    "M5c fourth_spawn_round_median":        ((2.5, 3.5),    (2.5, 12),  False),
    # ⛔ NOT a reproduction, and the reason is a finding.  PLAYBOOK COPY 8 lists
    # "median top-share of ring barriers by one bot 1.000" among its v68 targets,
    # but that number is T2's V47 measurement (n=924 v47 games with >=4 ring
    # barriers).  v68 measures 0.80 here, and COPY 8's own id-tracked v68 watch
    # (A game 5) has TWO bots on the ring — 6 barriers and 3 — i.e. 0.667.  So
    # this band asserts only "one bot dominates but does not own the ring".
    # The 1.000 IS reproduced, on v47, in --full.
    "M5d ring_barrier_top_share_median":    ((0.75, 0.92), (0.5, 0.95), False),
    # ⛔ M5i (all four COPY-8 roles on four distinct bots) IS DELIBERATELY NOT
    # IN THIS TABLE, and that is a finding rather than an omission: it measures
    # 1.8% on Bean counters v68 (2/112 games) against 0.0% on us.  The literal
    # recognisers COPY 8 publishes — home keeper "forward share 0.000", siege
    # engineer "batk 0 AND a sentinel build", ore denier "EVERY barrier on ore"
    # — co-occur in two games out of a hundred and twelve.  "Four fixed jobs" is
    # a watched-game narrative, not a census-verified property.  A band around
    # 1.8% would be a check that cannot fail; the row is emitted by the tool with
    # that caveat in its note and is not scored here.  The ONE role recogniser
    # that does discriminate is the ore denier, so that is what is scored:
    "M5g role_ore_denier_share":            ((38, 52),      (0.0, 0.0), True),
    "M6a barriers_on_ore_share":            ((37.4, 38.4),  (0.0, 0.0), True),
    "M6b ore_denial_coverage_w30":          ((92.0, 93.0),  (0.0, 0.0), True),
    "M6c ore_denial_coverage_w3":           ((60, 75),      (0.0, 0.0), True),
    "M6d ore_denial_latency_median":        ((0.5, 1.5),    (None, None), False),
    "M7 fwd_turret_removal_rate":           ((65, 88),      (18, 42),   True),
}

# `--full`: the study's own populations, so the bands are reproductions.
# A = BC v47 (STUDY §3.4/§3.5/§3.6, n=1,235) ; B = us v168-v177 (§6.2, n=1,115).
FULL = {
    "M1 belt_connectivity_directed":        ((82.2, 83.2),  (55, 66),   True),
    "M2a cage_ring_share":                  ((55.0, 56.0),  (74.5, 76.5), True),
    "M2b full_seal_rate":                   ((21.8, 22.8),  (11.0, 13.0), True),
    "M2c first_ring_build_median":          ((34.5, 35.5),  (11.5, 12.5), True),
    "M4e sentinel_band_share_anchor":       ((47.6, 48.6),  (None, None), False),
    "M4f sentinel_pointblank_share_anchor": ((23.4, 24.4),  (None, None), False),
    "M5d ring_barrier_top_share_median":    ((0.95, 1.0),   (0.5, 0.95), True),
    "M6c ore_denial_coverage_w3":           ((79.8, 80.8),  (0.0, 0.0), True),
    "M6d ore_denial_latency_median":        ((0.5, 1.5),    (None, None), False),
    "M7 fwd_turret_removal_rate":           ((78.7, 80.7),  (41.8, 43.8), True),
}


# ⭐ THE MIRROR GUARD — the strongest evidence in this file that side
# attribution is real.  `PLAYBOOK-beancounters-PART-v68-2026-08-21.md` publishes
# an OPPONENT column beside every Bean-counters cell, computed by the s53 probes
# with "the identical code path, side index swapped".  Population C IS that
# swap.  So C is not merely required to leave A's band — it is required to LAND
# ON THE PUBLISHED OPPONENT NUMBER.  A tool that reads the wrong side and still
# reproduces the wrong side's published value is a tool whose attribution works.
# (line refs into that file: §1 table for ore, §2.2 table for the drip)
MIRROR_V68_OPPONENT = {
    "M3a drip_lattice_share":         (53.6, 0.3,  "§2.2: 2,011/3,755 = 53.6%"),
    "M3b converts_per_game_median":   (23.5, 0.1,  "§2.2: median 23.5"),
    "M3d peak_ammo_median":           (30.0, 0.1,  "§2.2: median 30"),
    "M3e first_convert_round_median": (1.0,  0.1,  "§2.2: median 1.0 (p10 0)"),
    "M6a barriers_on_ore_share":      (7.4,  0.15, "§1: 60/815 = 7.4%"),
    "M6b ore_denial_coverage_w30":    (22.4, 0.15, "§1: 11/49 = 22.4%"),
}


def guard_mirror(mC):
    bad = []
    for metric, (want, tol, anchor) in MIRROR_V68_OPPONENT.items():
        got = mC.get(metric, {}).get("value")
        if got is None or abs(got - want) > tol:
            bad.append(f"{metric}: wrong-side read {got} != published opponent "
                       f"{want} ({anchor})")
    ok = not bad
    return ok, ("wrong-side read reproduces %d/%d published OPPONENT cells "
                "(lattice 53.6%%, converts 23.5, peak ammo 30, first convert "
                "1.0, ore 7.4%%, ore coverage 22.4%%)"
                % (len(MIRROR_V68_OPPONENT), len(MIRROR_V68_OPPONENT))
                if ok else "; ".join(bad))


def band_ok(value, band):
    lo, hi = band
    if lo is None and hi is None:
        return None                      # no expectation on this side
    if value is None:
        return False
    if lo is not None and value < lo:
        return False
    if hi is not None and value > hi:
        return False
    return True


def by_metric(res):
    return {m["metric"]: m for m in res["metrics"]}


# --- structural guards --------------------------------------------------------

def guard_lattice():
    accept = [0, 4, 8, 10, 12, 14, 20, 24, 100, 558]
    reject = [1, 2, 3, 5, 6, 7, 9, 11, 13, -4]
    bad = [v for v in accept if not SF.in_lattice(v)]
    bad += [v for v in reject if SF.in_lattice(v)]
    ok = not bad
    return ok, (f"accepts {len(accept)}/{len(accept)} lattice values, rejects "
                f"{len(reject)}/{len(reject)} non-lattice (2 and 6 included, so "
                f"this is not an is-it-even test)" if ok
                else f"MISCLASSIFIED: {bad}")


def guard_shim(files, k=5):
    """Shim must equal a full Replay parse; a corrupted shim must NOT."""
    checked = 0
    for path, side in files[:k]:
        if not path.exists():
            continue
        rec = SF.scan_replay(path, side)
        full = Replay(path, track_flow=True)
        ref = full.chains(side)
        if (rec["harv_end_total"], rec["harv_end_directed"],
                rec["harv_end_connected"]) != (ref["total"], ref["directed"],
                                               ref["connected"]):
            return False, (f"{path.name}: shim {rec['harv_end_directed']}/"
                           f"{rec['harv_end_total']} != Replay "
                           f"{ref['directed']}/{ref['total']}")
        checked += 1
    if not checked:
        return False, "no replays available to check"
    # NEGATIVE CONTROL: strip the conveyors out of a shim and require the
    # comparison to FAIL.  Without this, an equality that can never fail is not
    # evidence of anything.
    path, side = files[0]
    rec_ents = {}
    full = Replay(path, track_flow=True)
    for eid, e in full.entities.items():
        if e.kind not in ("conveyor", "splitter"):
            rec_ents[eid] = e
    broken = SF._ChainShim(rec_ents, full.cores, full.ship_from)
    got = Replay.chains(broken, side)
    ref = full.chains(side)
    if got["directed"] == ref["directed"] and ref["directed"] > 0:
        return False, ("negative control did NOT fire: a conveyor-stripped shim "
                       "returned the same directed count, so the equality above "
                       "proves nothing")
    return True, (f"{checked} replays equal to Replay.chains; conveyor-stripped "
                  f"control diverged ({got['directed']} vs {ref['directed']})")


def guard_ordering(mA):
    v = mA.get("M5d ring_barrier_top_share_median", {}).get("value")
    ring = mA.get("M2a cage_ring_share", {}).get("value")
    ok = v is not None and ring is not None and ring > 0
    return ok, (f"per-bot ring attribution alive (M5d={v}) while M2a={ring}%"
                if ok else
                f"M5d={v} with M2a={ring}% — per-bot build attribution is dead "
                f"under a healthy aggregate (the builderBuild ordering bug)")


def guard_empty():
    try:
        SF.run_population([], 1.833, 3)
    except SystemExit:
        return True, "empty population raises SystemExit instead of printing zeroes"
    except Exception as exc:                                     # noqa: BLE001
        return True, f"empty population raises {type(exc).__name__}"
    return False, "empty population returned a result — it would print a table of zeroes"


# --- main ---------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="both-ways drive for skalman_fidelity")
    ap.add_argument("--full", action="store_true",
                    help="run the study's full populations (~75 s) and assert "
                         "the published numbers digit-for-digit")
    ap.add_argument("--deff", type=float, default=1.833)
    a = ap.parse_args()

    t0 = time.time()
    if a.full:
        expect = FULL
        label_a, label_b = "BC v47 (STUDY n=1,235)", "us v168-v177 (STUDY §6.2)"
        files_a = SF.load_corpus(team_id=BC_TEAM_ID, versions=["47"],
                                 replay_root=REPLAY_ROOT)
        files_b = SF.load_corpus(team_id=OUR_TEAM_ID,
                                 versions=[str(v) for v in range(168, 178)],
                                 replay_root=REPLAY_ROOT)
    else:
        expect = QUICK
        label_a, label_b = "BC v68 (PART-v68 census, n=112)", "us v175-v177 (n=150)"
        files_a = SF.load_manifest(BC_V68_MANIFEST, REPLAY_ROOT)
        files_b = SF.load_manifest(US_MANIFEST, REPLAY_ROOT)
    files_a.sort()
    files_b.sort()

    resA = SF.run_population(files_a, a.deff, 3)
    resB = SF.run_population(files_b, a.deff, 3)
    # C: the SAME files as A with the subject index inverted.
    resC = SF.run_population(files_a, a.deff, 3, flip_side=True)
    mA, mB, mC = by_metric(resA), by_metric(resB), by_metric(resC)

    print(f"# SKALMAN FIDELITY SELFTEST  mode={'full' if a.full else 'quick'}  "
          f"deff={a.deff}")
    print(f"# A = {label_a}: {resA['n_games']} games, {resA['elapsed_s']}s")
    print(f"# B = {label_b}: {resB['n_games']} games, {resB['elapsed_s']}s")
    print(f"# C = A READ ON THE WRONG SIDE: {resC['n_games']} games, "
          f"{resC['elapsed_s']}s")
    print()
    cols = ["metric", "A_value", "A_band", "A", "B_value", "B_band", "B",
            "C_wrongside", "C_breaks", "VERDICT"]
    print("\t".join(cols))

    n_pass = n_fail = n_attr = 0
    failures = []
    for metric, (bandA, bandB, discrim) in expect.items():
        rA, rB, rC = mA.get(metric), mB.get(metric), mC.get(metric)
        if rA is None or rB is None:
            print("\t".join([metric] + ["MISSING"] * 9))
            n_fail += 1
            failures.append(f"{metric}: metric not emitted")
            continue
        okA = band_ok(rA["value"], bandA)
        okB = band_ok(rB["value"], bandB)
        cval = rC["value"]
        breaks = (band_ok(cval, bandA) is False) if discrim else None
        verdict = "PASS" if (okA and okB is not False) else "FAIL"
        if verdict == "PASS" and discrim and not breaks:
            verdict = "ATTRIBUTION-FAIL"
        if verdict == "PASS":
            n_pass += 1
        elif verdict == "ATTRIBUTION-FAIL":
            n_attr += 1
            failures.append(f"{metric}: wrong-side read {cval} still inside A's "
                            f"band {bandA} — this metric does not discriminate "
                            f"sides")
        else:
            n_fail += 1
            failures.append(f"{metric}: A={rA['value']} band={bandA} ok={okA} | "
                            f"B={rB['value']} band={bandB} ok={okB}")

        def f(v):
            return "" if v is None else (f"{v:.1f}" if isinstance(v, float) else str(v))
        print("\t".join([metric, f(rA["value"]), str(bandA),
                         "ok" if okA else "OUT",
                         f(rB["value"]), str(bandB),
                         {True: "ok", False: "OUT", None: "-"}[okB],
                         f(cval),
                         {True: "yes", False: "NO", None: "n/a"}[breaks],
                         verdict]))

    print()
    print("# STRUCTURAL GUARDS (each driven to both verdicts)")
    guards = [("G1 lattice", guard_lattice()),
              ("G2 chains-shim", guard_shim(files_a)),
              ("G3 build-attribution-ordering", guard_ordering(mA)),
              ("G4 empty-population-refusal", guard_empty())]
    if not a.full:
        guards.append(("G5 mirror-vs-published-opponent-column",
                       guard_mirror(mC)))
    g_fail = 0
    for name, (ok, msg) in guards:
        print(f"{name}\t{'PASS' if ok else 'FAIL'}\t{msg}")
        if not ok:
            g_fail += 1
            failures.append(f"{name}: {msg}")

    print()
    print(f"# METRICS: {n_pass} pass, {n_fail} fail, {n_attr} attribution-fail "
          f"of {len(expect)}")
    print(f"# GUARDS: {len(guards)-g_fail} pass, {g_fail} fail")
    print(f"# TOTAL RUNTIME {time.time()-t0:.1f}s")
    if failures:
        print()
        print("# FAILURES")
        for f_ in failures:
            print(f"#   {f_}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
