#!/usr/bin/env python3
"""Per-game causal summary for the s51 rush autopsy.

Reads fired30.tsv + replays/ + logs/ and emits one wide row per game with the
facts a proximate-cause chain needs.  Also emits the raw per-round tape as
games/<tag>.tape.tsv for the games a human reads by hand.

INSTRUMENT CROSS-CHECK (runs every time, refuses on failure): the replay's own
`winner` field, mapped through the seat->team assumption (seat A = team 0),
must agree with the grid tsv's `ours` column for every game.  A disagreement
means the seat mapping is wrong and every "our"/"opp" column is transposed.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tape import Tape, dsq  # noqa: E402

REP = HERE / "replays"
LOG = HERE / "logs"
GAMES = HERE / "games"


def load_grid():
    rows = []
    with open(HERE / "fired30.tsv") as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            rows.append(dict(zip(hdr, f)))
    return rows


LOG_RE = re.compile(r"^FS ([A-Z_]+) (\d+)\b(.*)$")


def parse_log(tag):
    p = LOG / (tag + ".err")
    evs = []
    if not p.exists():
        return evs
    for line in p.read_text(errors="replace").splitlines():
        m = LOG_RE.match(line)
        if m:
            evs.append((m.group(1), int(m.group(2)), m.group(3).strip()))
    return evs


def first_below(rows, key, thresh):
    for r in rows:
        if r[key] <= thresh:
            return r["r"]
    return None


def main():
    GAMES.mkdir(exist_ok=True)
    grid = load_grid()
    out = []
    alarms = []
    for g in grid:
        tag = g["tag"]
        our_team = 0 if g["seat"] == "A" else 1
        t = Tape(REP / (tag + ".replay26"), our_team)
        # --- cross-check -------------------------------------------------
        won_by_replay = (t.winner == our_team)
        won_by_grid = (g["ours"] == "US")
        if won_by_replay != won_by_grid:
            alarms.append("%s: replay winner=%s our_team=%s but grid ours=%s"
                          % (tag, t.winner, our_team, g["ours"]))
        rows = t.rows
        last = rows[-1]
        # sentinel / launcher / gunner build+death events, ours
        our_b = [(r, k, i, p) for (r, tm, k, i, p) in t.builds if tm == our_team]
        our_d = [(r, k, i, p, br) for (r, tm, k, i, p, br) in t.deaths
                 if tm == our_team]
        opp_b = [(r, k, i, p) for (r, tm, k, i, p) in t.builds if tm != our_team]
        sent_b = [r for (r, k, _i, _p) in our_b if k == "sentinel"]
        sent_d = [r for (r, k, _i, _p, _br) in our_d if k == "sentinel"]
        gun_b = [r for (r, k, _i, _p) in our_b if k == "gunner"]
        lau_b = [r for (r, k, _i, _p) in our_b if k == "launcher"]
        harv_b = [r for (r, k, _i, _p) in our_b if k == "harvester"]
        opp_sent_b = [r for (r, k, _i, _p) in opp_b if k == "sentinel"]
        opp_gun_b = [r for (r, k, _i, _p) in opp_b if k == "gunner"]
        # our builder-bot deaths inside the enemy ring (dsq<=13 of enemy core)
        pc = t.core_c[1 - our_team]
        raider_deaths = [r for (r, k, _i, p, _br) in our_d
                         if k == "builder_bot" and dsq(p, pc) <= 25]
        # rounds where a sentinel of ours was ALIVE but ammo < 10 (dry)
        dry = sum(1 for r in rows if r["sent"] > 0 and r["our_ammo"] < 10)
        sent_alive = sum(1 for r in rows if r["sent"] > 0)
        # rounds with no builder bot of ours within dsq<=8 of the enemy core,
        # counted only after our first arrival
        arr = next((r["r"] for r in rows if r["near_bot"] > 0), None)
        gap = (sum(1 for r in rows if r["r"] >= arr and r["near_bot"] == 0)
               if arr is not None else None)
        # enemy pressure on our core
        opp_press = sum(1 for r in rows if r["opp_near_bot"] > 0)
        opp_press_start = next((r["r"] for r in rows if r["opp_near_bot"] > 0),
                               None)
        # our core HP milestones
        hp_first_hit = next((r["r"] for r in rows if r["our_core_hp"] < 500), None)
        hp250 = first_below(rows, "our_core_hp", 250)
        opp_hp_min = min(r["opp_core_hp"] for r in rows)
        opp_hp_min_r = next(r["r"] for r in rows
                            if r["opp_core_hp"] == opp_hp_min)
        our_hp_min = min(r["our_core_hp"] for r in rows)
        # economy: last round our collected total increased
        coll_last = 0
        for r in rows:
            if r["our_coll"] > coll_last:
                coll_last = r["our_coll"]
                coll_last_r = r["r"]
        coll_last_r = locals().get("coll_last_r", 0)
        ammo_max = max(r["our_ammo"] for r in rows)
        evs = parse_log(tag)
        ecount = {}
        for k, _r, _rest in evs:
            ecount[k] = ecount.get(k, 0) + 1
        arrive_r = [r for (k, r, _x) in evs if k == "ARRIVE"]
        degrade_r = [r for (k, r, _x) in evs if k == "DEGRADE"]
        sentlog_r = [r for (k, r, _x) in evs if k == "SENTINEL"]
        sentdead_r = [r for (k, r, _x) in evs if k == "SENTDEAD"]
        cleared_r = [r for (k, r, _x) in evs if k == "CLEARED"]
        row = dict(
            tag=tag, map=g["map"], seed=g["seed"], seat=g["seat"],
            ours=g["ours"], cond=g["cond"], turn=int(g["turn"]),
            our_hp_end=last["our_core_hp"], opp_hp_end=last["opp_core_hp"],
            our_hp_min=our_hp_min, opp_hp_min=opp_hp_min,
            opp_hp_min_r=opp_hp_min_r,
            hp_first_hit=hp_first_hit, hp250=hp250,
            opp_press=opp_press, opp_press_start=opp_press_start,
            our_arrive=arr, raider_gap=gap, raider_deaths=len(raider_deaths),
            sent_n=len(sent_b), sent_first=(sent_b[0] if sent_b else None),
            sent_deaths=len(sent_d), sent_alive_r=sent_alive, sent_dry_r=dry,
            gun_n=len(gun_b), lau_n=len(lau_b), harv_n=len(harv_b),
            ammo_max=ammo_max, ammo_end=last["our_ammo"],
            our_coll=last["our_coll"], opp_coll=last["opp_coll"],
            coll_stop=coll_last_r,
            opp_sent_n=len(opp_sent_b),
            opp_sent_first=(opp_sent_b[0] if opp_sent_b else None),
            opp_gun_n=len(opp_gun_b),
            log_arrive=len(arrive_r), log_degrade=len(degrade_r),
            log_sent=len(sentlog_r), log_sentdead=len(sentdead_r),
            log_cleared=len(cleared_r),
            log_throw=ecount.get("THROW", 0), log_evict=ecount.get("EVICT", 0),
            log_seal=ecount.get("SEAL", 0), log_clear=ecount.get("CLEAR", 0),
            arrive_rounds=",".join(str(x) for x in arrive_r[:6]),
            degrade_rounds=",".join(str(x) for x in degrade_r[:6]),
        )
        out.append(row)
        # write the per-game tape
        with open(GAMES / (tag + ".tape.tsv"), "w") as fh:
            cols = list(rows[0].keys())
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
    if alarms:
        sys.stderr.write("INSTRUMENT ALARM (seat->team mapping):\n  "
                         + "\n  ".join(alarms) + "\n")
        raise SystemExit(2)
    sys.stderr.write("cross-check OK: 30/30 replay winner agrees with grid "
                     "under seat A=team0\n")
    cols = list(out[0].keys())
    with open(HERE / "games_summary.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in out:
            fh.write("\t".join("" if r[c] is None else str(r[c])
                               for c in cols) + "\n")
    print("\t".join(cols))
    for r in out:
        print("\t".join("" if r[c] is None else str(r[c]) for c in cols))


if __name__ == "__main__":
    main()
