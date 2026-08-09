#!/usr/bin/env python3
"""Assemble the per-GAME feature table for the core-kill incidence cut, and
validate the two new fine-band decoders against the packaged corpus.

Input (all read from a FROZEN snapshot dir, never from live corpus/):
  join.tsv           file -> match, opponent, oppbef, map, cond, turns, won, our_team
  ladder_games.tsv   adds `seat` (join.tsv has no seat column)
  events.tsv         every BUILD and DEATH, per round, per team, with d2_own/d2_enemy
  build_agg.tsv      coarse-band counters   (VALIDATION reference)
  econ.tsv           coarse-band econ       (VALIDATION reference)
  fineband.tsv       NEW: 25-round shot/ammo/builder-action counters
  positions.tsv      NEW: 25-round builder-bot position aggregates

Output:
  dataset.tsv        one row per joined ladder game, US_* and THEM_* features
                     accumulated over CUMULATIVE windows r<25, r<50, r<75, r<100,
                     r<125, r<150.
  validation.txt     decoder cross-checks

DESIGN NOTE -- outcome conditioning.
Every feature is a LANDMARK feature: it is accumulated strictly inside [0, T) and
the analysis population at landmark T is restricted to games still running at T
(`turns` > T). That is what keeps "we had more stuff" from being a restatement of
"we had already won". See the deliverable's DESIGN section.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

BANDS = ["r0-25", "r25-50", "r50-75", "r75-100", "r100-125", "r125-150"]
WINDOWS = [25, 50, 75, 100, 125, 150]
KINDS = ["builder_bot", "harvester", "conveyor", "gunner", "sentinel",
         "launcher", "barrier", "splitter"]
FB_COUNTERS = ["shot", "batk", "batk_core", "ammo_converted", "heals", "tled"]
FB_SNAPS = ["ti_end", "ammo_end", "ti_collected_end"]


def band_of(r: int) -> str:
    lo = (r // 25) * 25
    return f"r{lo}-{lo+25}"


def main(snap: str, outdir: str) -> None:
    S, O = Path(snap), Path(outdir)
    O.mkdir(parents=True, exist_ok=True)

    def rd(name):
        return csv.DictReader(open(S / name), delimiter="\t")

    J = {r["file"]: r for r in rd("join.tsv")}
    # seat lives only in ladder_games.tsv, keyed (match, game)
    seat = {}
    for r in rd("ladder_games.tsv"):
        seat[(r["match"], r["s3"])] = r["seat"]

    # ---------- events -> per file/team cumulative build + death counters ----------
    ev = collections.defaultdict(collections.Counter)      # (file,team) -> counter
    mapdim = {}
    for r in rd("events.tsv"):
        f = r["file"]
        if f not in J:
            continue
        rnd = int(r["rnd"])
        if rnd >= 150:
            continue
        t, k, b = r["team"], r["kind"], band_of(rnd)
        c = ev[(f, t)]
        pre = "B" if r["ev"] == "BUILD" else "D"
        c[f"{pre}_{k}|{b}"] += 1
        mapdim[f] = (int(r["mw"]), int(r["mh"]))
        if r["ev"] == "BUILD":
            de, do = int(r["d2_enemy"]), int(r["d2_own"])
            if k in ("gunner", "sentinel", "launcher"):
                c[f"TURFWD|{b}"] += 1 if de < do else 0
                c[f"TUR36|{b}"] += 1 if de <= 36 else 0
                key = f"TURMIND|{b}"
                c[key] = min(c[key], de) if key in c else de
                fk = f"FIRSTTUR"
                if fk not in c:
                    c[fk] = rnd
                if k == "launcher" and "FIRSTLAU" not in c:
                    c["FIRSTLAU"] = rnd
            if k in ("conveyor", "barrier", "harvester") and de < do:
                c[f"ECOFWD|{b}"] += 1

    # ---------- fine-band decoders ----------
    fb = collections.defaultdict(dict)                     # (file,team,band) -> row
    for r in rd("fineband.tsv"):
        if r["file"] in J:
            fb[(r["file"], r["team"], r["band"])] = r
    po = collections.defaultdict(dict)
    for r in rd("positions.tsv"):
        if r["file"] in J:
            po[(r["file"], r["team"], r["band"])] = r

    # ---------- throws (launcher interception / insertion), per file/thrower-team ----------
    # Kept as a candidate because enemy launcher activity IS runtime-observable
    # (a launcher is a building a unit can see) and is very live against some
    # opponents -- Lunds Stallions throw our bots ~14x/game. It is NOT a live
    # hypothesis for Ouroboros: 0 launcher builds, 0 throws in 105 games.
    th = collections.defaultdict(collections.Counter)      # file -> counter
    for r in rd("throws.tsv"):
        f = r["file"]
        if f not in J:
            continue
        rnd = int(r["rnd"])
        if rnd >= 150 or r["amb"] != "one":                # trap 3: skip UNATTRIB
            continue
        th[f][f"{r['tteam']}|{r['bteam']}|{band_of(rnd)}"] += 1

    # ================= VALIDATION =================
    vlines = []
    ba = collections.Counter()
    for r in rd("build_agg.tsv"):
        if r["file"] in J and r["band"] == "r0-150":
            ba[(r["file"], r["team"], r["metric"])] += int(r["n"])
    ec = {}
    for r in rd("econ.tsv"):
        if r["file"] in J and r["band"] == "r0-150":
            ec[(r["file"], r["team"])] = r

    for metric in ("shot", "batk", "batk_core"):
        agree = dis = 0
        for (f, t), _ in [(k, 1) for k in {(a, b) for a, b, _ in ba}]:
            mine = sum(int(fb[(f, t, b)][metric]) for b in BANDS if (f, t, b) in fb)
            theirs = ba[(f, t, metric)]
            if mine == theirs:
                agree += 1
            else:
                dis += 1
        vlines.append(f"fineband vs build_agg[r0-150] {metric:10s}: "
                      f"{agree} agree / {dis} disagree")
    # ammo_converted vs econ
    agree = dis = 0
    for (f, t), row in ec.items():
        mine = sum(int(fb[(f, t, b)]["ammo_converted"]) for b in BANDS if (f, t, b) in fb)
        if mine == int(row["ammo_converted"]):
            agree += 1
        else:
            dis += 1
    vlines.append(f"fineband vs econ[r0-150] ammo_converted   : {agree} agree / {dis} disagree")
    # events builds vs build_agg builds (independent decoders, same guard)
    for k in ("gunner", "sentinel", "harvester", "builder_bot", "conveyor"):
        agree = dis = 0
        for (f, t) in {(a, b) for a, b, _ in ba}:
            mine = sum(ev[(f, t)][f"B_{k}|{b}"] for b in BANDS)
            theirs = ba[(f, t, "build_" + k)]
            if mine == theirs:
                agree += 1
            else:
                dis += 1
        vlines.append(f"events vs build_agg[r0-150] build_{k:12s}: {agree} agree / {dis} disagree")
    # all-zero column check on the NEW files (trap 5/6 class)
    for name, rows, cols in (("fineband.tsv", fb, FB_COUNTERS + FB_SNAPS),
                             ("positions.tsv", po, ["bots_mean", "collar8_mean",
                                                    "collar2_mean", "fwd_mean",
                                                    "r36_rounds", "r20_rounds"])):
        for c in cols:
            tot = sum(float(r[c]) for r in rows.values())
            vlines.append(f"NONZERO {name}:{c:18s} sum={tot:.1f}"
                          + ("   <<< ALL ZERO -- BUG SIGNATURE" if tot == 0 else ""))

    (O / "validation.txt").write_text("\n".join(vlines) + "\n")
    print("\n".join(vlines))

    # ================= DATASET =================
    feat_names = []
    rows = []
    for f, j in J.items():
        us, them = j["our_team"], str(1 - int(j["our_team"]))
        turns = int(j["turns"])
        rec = {
            "file": f, "match": j["match"], "opp": j["opp"], "map": j["map"],
            "oppbef": j["oppbef"], "cond": j["cond"], "turns": turns,
            "ourver": j["ourver"],
            "won": j["won"], "our_team": us,
            "seat": seat.get((j["match"], f), "?"),
            "mw": mapdim.get(f, (0, 0))[0], "mh": mapdim.get(f, (0, 0))[1],
            "y_corekill": 1 if (j["cond"] == "core_destroyed" and j["won"] == "1") else 0,
            "y_corelost": 1 if (j["cond"] == "core_destroyed" and j["won"] == "0") else 0,
        }
        for side, t in (("US", us), ("THEM", them)):
            for W in WINDOWS:
                bs = [b for b in BANDS if int(b.split("-")[1]) <= W]
                c = ev[(f, t)]
                for k in KINDS:
                    rec[f"{side}_b_{k}_w{W}"] = sum(c[f"B_{k}|{b}"] for b in bs)
                    rec[f"{side}_d_{k}_w{W}"] = sum(c[f"D_{k}|{b}"] for b in bs)
                rec[f"{side}_b_turret_w{W}"] = sum(
                    rec[f"{side}_b_{k}_w{W}"] for k in ("gunner", "sentinel", "launcher"))
                rec[f"{side}_turfwd_w{W}"] = sum(c[f"TURFWD|{b}"] for b in bs)
                rec[f"{side}_tur36_w{W}"] = sum(c[f"TUR36|{b}"] for b in bs)
                rec[f"{side}_ecofwd_w{W}"] = sum(c[f"ECOFWD|{b}"] for b in bs)
                mds = [c[f"TURMIND|{b}"] for b in bs if f"TURMIND|{b}" in c]
                rec[f"{side}_turmind_w{W}"] = min(mds) if mds else 9999
                for m in FB_COUNTERS:
                    rec[f"{side}_{m}_w{W}"] = sum(
                        int(fb[(f, t, b)][m]) for b in bs if (f, t, b) in fb)
                # snapshots: last band present in the window
                last = None
                for b in bs:
                    if (f, t, b) in fb:
                        last = fb[(f, t, b)]
                for m in FB_SNAPS:
                    rec[f"{side}_{m}_w{W}"] = int(last[m]) if last else 0
                # positions: rounds-weighted means over the window
                pr = [po[(f, t, b)] for b in bs if (f, t, b) in po]
                nr = sum(int(x["rounds"]) for x in pr) or 1
                for m in ("bots_mean", "collar8_mean", "collar2_mean", "fwd_mean"):
                    rec[f"{side}_{m}_w{W}"] = sum(
                        float(x[m]) * int(x["rounds"]) for x in pr) / nr
                rec[f"{side}_bots_max_w{W}"] = max(
                    [int(x["bots_max"]) for x in pr], default=0)
                rec[f"{side}_collar8_max_w{W}"] = max(
                    [int(x["collar8_max"]) for x in pr], default=0)
                mind = [int(x["mindist_enemy"]) for x in pr if int(x["mindist_enemy"]) >= 0]
                rec[f"{side}_botmind_w{W}"] = min(mind) if mind else 9999
                rec[f"{side}_r36_w{W}"] = sum(int(x["r36_rounds"]) for x in pr)
                rec[f"{side}_r20_w{W}"] = sum(int(x["r20_rounds"]) for x in pr)
                # throws BY this side, of either team's bots
                rec[f"{side}_throws_w{W}"] = sum(
                    th[f][f"{t}|{bt}|{b}"] for b in bs for bt in ("0", "1"))
                rec[f"{side}_throws_of_enemy_w{W}"] = sum(
                    th[f][f"{t}|{1-int(t)}|{b}"] for b in bs)
            rec[f"{side}_firsttur"] = ev[(f, t)].get("FIRSTTUR", 999)
            rec[f"{side}_firstlau"] = ev[(f, t)].get("FIRSTLAU", 999)
        rows.append(rec)
        if not feat_names:
            feat_names = list(rec.keys())

    with open(O / "dataset.tsv", "w") as fh:
        fh.write("\t".join(feat_names) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[k]) for k in feat_names) + "\n")
    print(f"\ndataset.tsv: {len(rows)} games x {len(feat_names)} columns")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
