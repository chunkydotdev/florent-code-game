#!/usr/bin/env python3
"""v519 replay-side instrument: HEAL-BACK SHARE and THE INCOME PROXY.

⛔ COPIED, NOT REWRITTEN.  The wire walk, the core-HP ledger, the delta
alphabet and the HP-identity guard are `scratchpad/s51_rush_autopsy/attrib.py`
(s51 rush autopsy, guards already driven both ways there); this file adds three
columns the autopsy did not need and re-runs those guards in place.

WHAT IS NEW HERE
  * `heal_back`  = healing landed on the ENEMY core / damage landed on it.
    The autopsy's ledger method: UpdateHp deltas on the enemy core id, with
    +1..+4 healing and -18/-7/-2 damage.  This is THE number v519 exists to
    move -- the autopsy measured it at EXACTLY 100.0% in 11 of 12 failed sieges
    and the whole cripple thesis is that cutting their income cuts it.
  * `opp_harv_built` / `opp_belt_built` / `opp_eco_killed` -- THE INCOME PROXY.
    Every enemy HARVESTER/CONVEYOR/SPLITTER spawn, and every removal of one,
    read off the same entity/removal streams the turret registry uses.
  * `fwd_gun_first` / `fwd_gun_n` -- OUR beltbreak shredders (a GUNNER of ours
    at d^2 <= LOKI_BELTBREAK_DSQ_HI=100 of the ENEMY core), so "the first plant
    lands at r36-75" is a measured column and not a memory.

GUARDS (all three must produce the other verdict before any number is read):
  1. HP IDENTITY on our own core, per game (from attrib.py, unchanged).
  2. DELTA ALPHABET: any delta outside {-18,-7,-2,+1..+4} is reported.
  3. ⭐ TEAM-SWAP POSITIVE CONTROL: re-running one game with `our_team` flipped
     must move `heal_back` and the income columns.  A column that reads the
     same either way is reading nothing.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "reel"))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos,
)
from tape import dsq  # noqa: E402

DMG = {-18: "sent", -7: "gun", -2: "peck"}
ECO = ("harvester", "conveyor", "splitter")


def analyse(path: Path, our_team: int):
    data = path.read_bytes()
    map_buf = None
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    cores = []
    for num, _w, value in fields(map_buf):
        if num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    core_id = {c["team"]: c["id"] for c in cores}
    core_c = {c["team"]: (c["pos"][0] + .5, c["pos"][1] + .5) for c in cores}
    opp = 1 - our_team
    pc = core_c[opp]

    ledger = {our_team: defaultdict(int), opp: defaultdict(int)}
    unknown = set()
    ents = {}
    eco = {}            # id -> (team, kind, built)
    guns = []           # our gunners: (round, dsq_to_enemy_core)
    sents = []          # our sentinels: (round, dsq_to_enemy_core)
    launs = []          # our launchers: (round, dsq_to_enemy_core)
    collar = []         # our barriers within d^2<=8 of the enemy core
    eco_killed = defaultdict(int)
    eco_built = defaultdict(int)
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        ent = parse_entity(ebuf, rnd)
                        if ent is None or ent.id in ents:
                            continue
                        ents[ent.id] = ent
                        if ent.kind in ECO:
                            eco[ent.id] = (ent.team, ent.kind, rnd)
                            eco_built[(ent.team, ent.kind)] += 1
                        elif ent.kind == "gunner" and ent.team == our_team:
                            guns.append((rnd, dsq(ent.pos, pc)))
                        elif ent.kind == "sentinel" and ent.team == our_team:
                            sents.append((rnd, dsq(ent.pos, pc)))
                        elif ent.kind == "launcher" and ent.team == our_team:
                            launs.append((rnd, dsq(ent.pos, pc)))
                        elif ent.kind == "barrier" and ent.team == our_team:
                            if dsq(ent.pos, pc) <= 8:
                                collar.append(rnd)
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                            if rv in eco:
                                t, k, _b = eco.pop(rv)
                                eco_killed[(t, k)] += 1
                elif unum == 5:
                    eid, delta = parse_update_hp(ubuf)
                    for t in (our_team, opp):
                        if eid == core_id[t]:
                            ledger[t][delta] += 1
                            if delta not in DMG and not (1 <= delta <= 4):
                                unknown.add(delta)
    return dict(core_id=core_id, ledger=ledger, unknown=unknown, guns=guns,
                sents=sents, launs=launs, collar=collar,
                eco_built=eco_built, eco_killed=eco_killed,
                rounds=len(turn_bufs), our_team=our_team, opp=opp)


def summarise(r):
    our_team, opp = r["our_team"], r["opp"]
    out = {}
    for tag, team in (("ourcore", our_team), ("oppcore", opp)):
        L = r["ledger"][team]
        out["%s_dmg" % tag] = sum(-d * L.get(d, 0) for d in DMG)
        out["%s_heal" % tag] = sum(d * L.get(d, 0) for d in (1, 2, 3, 4))
        out["%s_hp_calc" % tag] = 500 + sum(d * c for d, c in L.items())
    d = out["oppcore_dmg"]
    out["heal_back"] = round(out["oppcore_heal"] / d, 4) if d else None
    d2 = out["ourcore_dmg"]
    out["heal_back_ours"] = round(out["ourcore_heal"] / d2, 4) if d2 else None
    # the income proxy: THEIR economy, built and destroyed
    out["opp_harv_built"] = r["eco_built"].get((opp, "harvester"), 0)
    out["opp_belt_built"] = (r["eco_built"].get((opp, "conveyor"), 0)
                             + r["eco_built"].get((opp, "splitter"), 0))
    out["opp_harv_killed"] = r["eco_killed"].get((opp, "harvester"), 0)
    out["opp_belt_killed"] = (r["eco_killed"].get((opp, "conveyor"), 0)
                              + r["eco_killed"].get((opp, "splitter"), 0))
    out["opp_eco_killed"] = out["opp_harv_killed"] + out["opp_belt_killed"]
    # our shredders (gunners in the beltbreak annulus of THEIR core)
    fg = [g for g in r["guns"] if g[1] <= 100]
    out["fwd_gun_n"] = len(fg)
    out["fwd_gun_first"] = min((g[0] for g in fg), default=None)
    out["gun_n"] = len(r["guns"])
    fs = [s for s in r["sents"] if s[1] <= 40]
    out["fwd_sent_n"] = len(fs)
    out["fwd_sent_first"] = min((s[0] for s in fs), default=None)
    # ⭐ THE MODESWITCH BEHAVIOURAL SIGNATURE, engine-side.  With the siege
    # plank stood down there is no ferry chain and no collar: our launchers in
    # the enemy half and our barriers on their ring both go to ~0.
    fl = [x for x in r["launs"] if x[1] <= 100]
    out["fwd_laun_n"] = len(fl)
    out["fwd_laun_first"] = min((x[0] for x in fl), default=None)
    out["collar_bar_n"] = len(r["collar"])
    out["unknown_deltas"] = ",".join(str(x) for x in sorted(r["unknown"]))
    return out


def run(grid_tsv, repdir, out_tsv, label=""):
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    out, fails, n_ident = [], [], 0
    for g in rows:
        tag = g["tag"]
        p = Path(repdir) / (tag + ".replay26")
        if not p.exists():
            continue
        our_team = 0 if g["seat"] == "A" else 1
        r = analyse(p, our_team)
        s = summarise(r)
        destroyed = (g["ours"] == "OPP" and g["cond"].startswith("Core destroyed"))
        calc = s["ourcore_hp_calc"]
        if destroyed:
            if not (-18 < calc <= 0):
                fails.append("%s: destroyed but ledger hp %d" % (tag, calc))
            else:
                n_ident += 1
        else:
            n_ident += 1
        if s["unknown_deltas"]:
            fails.append("%s: unknown deltas %s" % (tag, s["unknown_deltas"]))
        out.append(dict(tag=tag, map=g["map"], seed=g["seed"], seat=g["seat"],
                        ours=g["ours"], cond=g["cond"], turn=g["turn"],
                        arm=label, **s))
    if fails:
        sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails[:20]) + "\n")
        raise SystemExit(2)
    sys.stderr.write("guards OK: %d games, HP identity %d, alphabet clean\n"
                     % (len(out), n_ident))
    cols = list(out[0].keys())
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for x in out:
            fh.write("\t".join("" if x[c] is None else str(x[c])
                               for c in cols) + "\n")
    return out


def control(grid_tsv, repdir):
    """GUARD 3: the team-swap positive control, on the first game."""
    g = next(csv.DictReader(open(grid_tsv), delimiter="\t"))
    p = Path(repdir) / (g["tag"] + ".replay26")
    a = summarise(analyse(p, 0 if g["seat"] == "A" else 1))
    b = summarise(analyse(p, 1 if g["seat"] == "A" else 0))
    moved = [k for k in ("heal_back", "opp_harv_built", "opp_belt_built",
                         "fwd_gun_n", "oppcore_dmg", "fwd_laun_n",
                         "collar_bar_n")
             if a.get(k) != b.get(k)]
    print("TEAM-SWAP CONTROL on %s: columns that MOVED: %s" % (g["tag"], moved))
    print("   as-played: heal_back=%s opp_harv=%s oppcore_dmg=%s"
          % (a["heal_back"], a["opp_harv_built"], a["oppcore_dmg"]))
    print("   swapped  : heal_back=%s opp_harv=%s oppcore_dmg=%s"
          % (b["heal_back"], b["opp_harv_built"], b["oppcore_dmg"]))
    if not moved:
        raise SystemExit("CONTROL FAILED: the instrument reads the same either way")
    return moved


if __name__ == "__main__":
    if sys.argv[1] == "--control":
        control(sys.argv[2], sys.argv[3])
    else:
        run(sys.argv[1], sys.argv[2], sys.argv[3],
            sys.argv[4] if len(sys.argv) > 4 else "")
