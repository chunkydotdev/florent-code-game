#!/usr/bin/env python3
"""FORWARD vs HOME split of sentinel siting, on top of sent_read.py.

Read-only. Imports sent_read (validated decoder, 15/15 fixtures, both
declared mutants failing) rather than reimplementing any of its protobuf
walk. This script adds exactly one thing sent_read.analyse() does not
compute: each sentinel's distance to its OWN core footprint vs the ENEMY
core footprint, so pooled availability/conversion can be split into the
FORWARD branch (siting near the enemy core -- the only branch the
programme allows) and the HOME branch (siting near our own approaches --
PLAY_DEFENCE: never).

Population: corpus/meta_join.tsv rows with triggeredBy == 'ladder' and
us_side in {'a','b'} -- 2,355 replays / 471 matches, exactly reproducing
the population cited by the prior sentinel-siting finding (2d44c37).
Seat: meta_join.us_side ('a' -> team 0, 'b' -> team 1), NEVER
ladder_games.tsv (whose seat column is the WINNING seat, per CLAUDE.md).
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sent_read as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_JOIN = os.path.join(ROOT, "corpus", "meta_join.tsv")
ARCHIVE = os.path.join(ROOT, "replay_archive")


def load_population():
    with open(META_JOIN, newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    pop = [r for r in rows
           if r.get("triggeredBy") == "ladder" and r.get("us_side") in ("a", "b")]
    return pop


def seat_consistency_check(pop):
    """Every game of a match must carry the same us_side. Report matches/disagreements."""
    by_match = defaultdict(set)
    for r in pop:
        by_match[r["match"]].add(r["us_side"])
    bad = {m: s for m, s in by_match.items() if len(s) != 1}
    return len(by_match), bad


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def core_tiles_by_team(cores):
    """cores: [(cid, team, (x,y))] -> {team: [4 footprint tiles, ...]} (may
    have >1 core's tiles pooled per team if that ever occurs)."""
    out = defaultdict(list)
    for cid, ct, (cx, cy) in cores:
        out[ct].extend([(cx, cy), (cx + 1, cy), (cx, cy + 1), (cx + 1, cy + 1)])
    return out


def nearest_d2(pos, tiles):
    if not tiles:
        return None
    return min(d2(pos, t) for t in tiles)


BAND_EDGES = [32, 100, 250, 600]
BAND_LABELS = ["<=32", "33-100", "101-250", "251-600", ">600"]


def band_of(d2_enemy):
    for edge, label in zip(BAND_EDGES, BAND_LABELS):
        if d2_enemy <= edge:
            return label
    return BAND_LABELS[-1]


def main():
    pop = load_population()
    n_matches, bad = seat_consistency_check(pop)
    print(f"POPULATION: {len(pop)} replays / {n_matches} matches "
          f"(triggeredBy=ladder, us_side in a/b)")
    print(f"SEAT CONSISTENCY: {n_matches - len(bad)}/{n_matches} matches have a single "
          f"us_side across all their games ({len(bad)} disagreements)")
    missing_files = sum(1 for r in pop
                         if not os.path.exists(os.path.join(ARCHIVE, r["file"])))
    print(f"FILES: {len(pop) - missing_files}/{len(pop)} present in replay_archive/")

    # groups: key = (population, split) -> pooled accumulators
    groups = defaultdict(lambda: {"n": 0, "shots": 0, "opp": 0, "alive": 0,
                                   "hist": Counter()})
    forward_band = defaultdict(lambda: {"n": 0, "shots": 0, "opp": 0, "alive": 0})
    # per-sentinel availability -> conversion bins (US sentinels only)
    avail_bins = defaultdict(lambda: {"n": 0, "shots": 0, "opp": 0})

    no_own_core = 0
    no_enemy_core = 0
    parse_errors = 0
    n_sent_us = n_sent_opp = 0

    for r in pop:
        path = os.path.join(ARCHIVE, r["file"])
        if not os.path.exists(path):
            continue
        seat = 0 if r["us_side"] == "a" else 1
        try:
            R = S.parse_replay(path)
            st = S.analyse(path, None)
        except Exception:
            parse_errors += 1
            continue
        tiles = core_tiles_by_team(R["cores"])
        for rec in st["sent"]:
            team = rec["team"]
            is_us = (team == seat)
            pos = rec["pos"]
            own_t = tiles.get(team)
            enemy_t = tiles.get(1 - team)
            d2_own = nearest_d2(pos, own_t)
            d2_enemy = nearest_d2(pos, enemy_t)
            if d2_own is None:
                no_own_core += 1
                continue
            if d2_enemy is None:
                no_enemy_core += 1
                continue
            forward = d2_enemy < d2_own
            alive = rec["end"] - rec["build"] + 1
            shots = rec["shots"]
            opp = rec["opp_rounds"]
            bucket = S.bucket(rec)

            side = "us" if is_us else "opp"
            split = "FORWARD" if forward else "HOME"
            key = (side, split)
            g = groups[key]
            g["n"] += 1
            g["shots"] += shots
            g["opp"] += opp
            g["alive"] += alive
            g["hist"][bucket] += 1

            if is_us:
                n_sent_us += 1
                if forward:
                    b = band_of(d2_enemy)
                    fb = forward_band[b]
                    fb["n"] += 1
                    fb["shots"] += shots
                    fb["opp"] += opp
                    fb["alive"] += alive
                # availability-vs-conversion binning: all our sentinels
                if alive > 0:
                    avail = opp / alive
                    if avail == 0:
                        binlabel = "0%"
                    elif avail <= 0.10:
                        binlabel = "(0-10%]"
                    elif avail <= 0.25:
                        binlabel = "(10-25%]"
                    elif avail <= 0.50:
                        binlabel = "(25-50%]"
                    elif avail <= 0.75:
                        binlabel = "(50-75%]"
                    else:
                        binlabel = "(75-100%]"
                    ab = avail_bins[binlabel]
                    ab["n"] += 1
                    ab["shots"] += shots
                    ab["opp"] += opp
            else:
                n_sent_opp += 1

    print(f"\nSENTINELS DECODED: us={n_sent_us} opp={n_sent_opp} "
          f"(dropped: no_own_core={no_own_core} no_enemy_core={no_enemy_core} "
          f"parse_errors={parse_errors})")

    def pct(a, b):
        return 100.0 * a / b if b else float("nan")

    print("\n=== FORWARD/HOME SPLIT (us and mirrored opponent control) ===")
    total_us = groups[("us", "FORWARD")]["n"] + groups[("us", "HOME")]["n"]
    total_opp = groups[("opp", "FORWARD")]["n"] + groups[("opp", "HOME")]["n"]
    for side, total in (("us", total_us), ("opp", total_opp)):
        for split in ("FORWARD", "HOME"):
            g = groups[(side, split)]
            avail = pct(g["opp"], g["alive"])
            conv = pct(g["shots"], g["opp"])
            per100alive = pct(g["shots"], g["alive"])
            share = pct(g["n"], total)
            hist = g["hist"]
            hist_pct = {k: round(pct(v, g["n"]), 2) for k, v in hist.items()}
            print(f"{side:3s} {split:8s} n={g['n']:5d} ({share:5.1f}% of {side}) "
                  f"alive_rounds={g['alive']:8d} opp_rounds={g['opp']:7d} shots={g['shots']:6d}")
            print(f"          availability={avail:6.2f}%  conversion(/100opp)={conv:6.2f}  "
                  f"shots/100alive={per100alive:6.2f}  (product check: "
                  f"{avail*conv/100:6.2f})")
            print(f"          hist: {dict(hist)}  pct: {hist_pct}")

    print("\n=== OUR FORWARD SENTINELS, AVAILABILITY BY d2_enemy BAND ===")
    for label in BAND_LABELS:
        fb = forward_band[label]
        if fb["n"] == 0:
            print(f"  {label:>8s}: n=0 (empty)")
            continue
        avail = pct(fb["opp"], fb["alive"])
        conv = pct(fb["shots"], fb["opp"])
        print(f"  {label:>8s}: n={fb['n']:5d} alive={fb['alive']:7d} "
              f"opp={fb['opp']:6d} shots={fb['shots']:5d} "
              f"availability={avail:6.2f}% conversion={conv:6.2f}")

    print("\n=== CONVERSION vs AVAILABILITY, OUR SENTINELS (all, not just forward) ===")
    order = ["0%", "(0-10%]", "(10-25%]", "(25-50%]", "(50-75%]", "(75-100%]"]
    for label in order:
        ab = avail_bins[label]
        if ab["n"] == 0:
            print(f"  {label:>10s}: n=0 (empty)")
            continue
        conv = pct(ab["shots"], ab["opp"]) if ab["opp"] else float("nan")
        print(f"  {label:>10s}: n={ab['n']:5d} shots={ab['shots']:5d} "
              f"opp_rounds={ab['opp']:6d} conversion(/100opp)={conv:6.2f}")


if __name__ == "__main__":
    main()
