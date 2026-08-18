#!/usr/bin/env python3
"""Fire-rate / funding decomposition for the s51 rush autopsy.

For each game, for BOTH sides, per round:
  * is a forward sentinel of that team alive (dsq<=40 of the target core)?
  * is that team's ammo >= 10 (one sentinel shot)?
  * did that team's core-damage stream record a shot this round?

Gives three denominators for "why didn't we shoot":
    alive_r        sentinel exists
    funded_r       sentinel exists AND ammo >= 10
    shots          -18 events landing on the target core

    rate_capacity  = shots / (alive_r / 2)      (reload 2 => 0.5/round ceiling)
    rate_funded    = shots / (funded_r / 2)     (share of FUNDED capacity used)

If rate_funded is near 1 the binder is AMMO; if rate_funded is low while
funded_r is large the binder is TARGETING/BLOCKING, not money.

Also: heal-back on each core (sum of +1..+4 deltas), and the net.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos, scalars,
)
from tape import dsq  # noqa: E402


def run(path: Path, our_team: int):
    data = path.read_bytes()
    map_buf = None
    turns = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turns.append(value)
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
    cid = {c["team"]: c["id"] for c in cores}
    cpos = {c["team"]: (c["pos"][0] + .5, c["pos"][1] + .5) for c in cores}
    opp = 1 - our_team

    sent = {}      # id -> (team, built, died, dsq_to_enemy_core_of_that_team)
    ents = {}
    per = []       # per round dicts
    ammo = {0: 0, 1: 0}
    for rnd, tb in enumerate(turns):
        shots = {our_team: 0, opp: 0}   # shots landing on the OTHER team's core
        heals = {our_team: 0, opp: 0}   # heals on own core
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in ents:
                            continue
                        ents[e.id] = e
                        if e.kind == "sentinel":
                            tgt = 1 - e.team
                            sent[e.id] = dict(team=e.team, built=rnd, died=None,
                                              d=dsq(e.pos, cpos[tgt]))
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                            if rv in sent:
                                sent[rv]["died"] = rnd
                elif unum == 5:
                    eid, delta = parse_update_hp(ubuf)
                    for t in (0, 1):
                        if eid == cid[t]:
                            if delta == -18:
                                shots[1 - t] += 1
                            elif 1 <= delta <= 4:
                                heals[t] += delta
                elif unum == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                ammo[tn - 1] = scalars(tv).get(7, 0)
        row = {"r": rnd}
        for t, lbl in ((our_team, "our"), (opp, "opp")):
            live = sum(1 for s in sent.values()
                       if s["team"] == t and s["d"] <= 40
                       and s["built"] <= rnd
                       and (s["died"] is None or rnd < s["died"]))
            row[lbl + "_fwd_live"] = live
            row[lbl + "_ammo"] = ammo[t]
            row[lbl + "_shots"] = shots[t]
            row[lbl + "_heal_own_core"] = heals[t]
        per.append(row)
    return per


def agg(per, lbl):
    alive = sum(1 for r in per if r[lbl + "_fwd_live"] > 0)
    funded = sum(1 for r in per if r[lbl + "_fwd_live"] > 0
                 and r[lbl + "_ammo"] >= 10)
    shots = sum(r[lbl + "_shots"] for r in per)
    # capacity: each live forward sentinel can fire every 2 rounds
    cap = sum(r[lbl + "_fwd_live"] for r in per) / 2.0
    capf = sum(r[lbl + "_fwd_live"] for r in per
               if r[lbl + "_ammo"] >= 10) / 2.0
    return dict(alive=alive, funded=funded, shots=shots,
                cap=round(cap, 1), capf=round(capf, 1),
                use_cap=round(shots / cap, 3) if cap else None,
                use_funded=round(shots / capf, 3) if capf else None,
                heal_own=sum(r[lbl + "_heal_own_core"] for r in per))


def main():
    rows = list(csv.DictReader(open(HERE / "fired30.tsv"), delimiter="\t"))
    out = []
    for g in rows:
        our_team = 0 if g["seat"] == "A" else 1
        per = run(HERE / "replays" / (g["tag"] + ".replay26"), our_team)
        a, b = agg(per, "our"), agg(per, "opp")
        out.append(dict(
            tag=g["tag"], map=g["map"], ours=g["ours"], turn=int(g["turn"]),
            our_alive=a["alive"], our_funded=a["funded"], our_shots=a["shots"],
            our_cap=a["cap"], our_capf=a["capf"],
            our_use_cap=a["use_cap"], our_use_funded=a["use_funded"],
            oppcore_heal=b["heal_own"],
            opp_alive=b["alive"], opp_funded=b["funded"], opp_shots=b["shots"],
            opp_cap=b["cap"], opp_use_cap=b["use_cap"],
            opp_use_funded=b["use_funded"], ourcore_heal=a["heal_own"],
            our_net=a["shots"] * 18 - b["heal_own"],
            opp_net=b["shots"] * 18 - a["heal_own"],
        ))
    cols = list(out[0].keys())
    with open(HERE / "rate.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in out:
            fh.write("\t".join("" if r[c] is None else str(r[c])
                               for c in cols) + "\n")
    for r in out:
        print("\t".join("" if r[c] is None else str(r[c]) for c in cols))


if __name__ == "__main__":
    main()
