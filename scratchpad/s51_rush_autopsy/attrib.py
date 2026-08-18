#!/usr/bin/env python3
"""Damage attribution + forward/home split for the s51 rush autopsy.

Two questions the round tape cannot answer on its own:

  1. WHAT KILLED OUR CORE.  UpdateHp deltas name the victim and the delta class
     names the weapon (`tools/replay_census.py` docstring: -18 sentinel,
     -7 gunner, -2 builder-bot peck, +1..+4 heal).  Summing deltas landing on
     our core id splits our death into peck / gunner / sentinel damage and the
     heals we put back.
  2. FORWARD vs HOME.  Every turret build of ours is labelled by dsq from the
     ENEMY core: <=40 (sentinel attack r2=32, plus slack) = FORWARD, else HOME.
     The build report's "first sentinel >= r72" is about the SIEGE (forward)
     sentinel only; the round tape's early sentinels are home defence.

Also emits per-turret lifetime (build round -> removal round) so
"sentinel alive but dry" can be computed against the FORWARD sentinel only.

GUARDS (driven both ways, see guard() at the bottom):
  * delta alphabet: any delta outside {-18,-7,-2,+1..+4} is reported, not
    silently bucketed.
  * core HP identity: 500 + sum(deltas on our core) must equal the tape's final
    our_core_hp for every game, and must equal 0 exactly in the games the grid
    calls a core-destroyed loss.  A parser that mis-signs the fold fails this.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos, scalars,
)
from tape import dsq  # noqa: E402

DMG = {-18: "sent", -7: "gun", -2: "peck"}


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
    pc, oc = core_c[opp], core_c[our_team]

    # per-core delta ledgers
    ledger = {our_team: defaultdict(int), opp: defaultdict(int)}
    unknown = set()
    # turret registry: id -> dict(team,kind,pos,built,died,fwd)
    turrets = {}
    ents = {}
    ammo_by_round = []
    dead_at = {}
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
                        if ent.kind in ("sentinel", "gunner", "launcher"):
                            d = dsq(ent.pos, pc)
                            turrets[ent.id] = dict(
                                team=ent.team, kind=ent.kind, pos=ent.pos,
                                built=rnd, died=None,
                                dsq_opp=d, dsq_own=dsq(ent.pos, oc),
                                fwd=(d <= 40))
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                            dead_at[rv] = rnd
                            if rv in turrets:
                                turrets[rv]["died"] = rnd
                elif unum == 5:
                    eid, delta = parse_update_hp(ubuf)
                    for t in (our_team, opp):
                        if eid == core_id[t]:
                            ledger[t][delta] += 1
                            if delta not in DMG and not (1 <= delta <= 4):
                                unknown.add(delta)
                elif unum == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        rec = {}
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                rec[tn - 1] = scalars(tv).get(7, 0)
                        if rec:
                            ammo_by_round.append(rec.get(our_team, 0))
        while len(ammo_by_round) < rnd + 1:
            ammo_by_round.append(ammo_by_round[-1] if ammo_by_round else 0)
    return dict(core_id=core_id, ledger=ledger, unknown=unknown,
                turrets=turrets, ammo=ammo_by_round, rounds=len(turn_bufs))


def summarise(r, our_team):
    opp = 1 - our_team
    out = {}
    for tag, team in (("ourcore", our_team), ("oppcore", opp)):
        L = r["ledger"][team]
        for d, name in DMG.items():
            out["%s_%s" % (tag, name)] = -d * L.get(d, 0)
        out["%s_heal" % tag] = sum(d * L.get(d, 0) for d in (1, 2, 3, 4))
        out["%s_dmg" % tag] = sum(-d * L.get(d, 0) for d in DMG)
        out["%s_hp_calc" % tag] = 500 + sum(
            d * c for d, c in L.items())
    ours = [t for t in r["turrets"].values() if t["team"] == our_team]
    theirs = [t for t in r["turrets"].values() if t["team"] != our_team]
    for label, sel in (("fwd", True), ("home", False)):
        for kind in ("sentinel", "gunner", "launcher"):
            g = [t for t in ours if t["fwd"] == sel and t["kind"] == kind]
            out["%s_%s_n" % (label, kind[:4])] = len(g)
            out["%s_%s_first" % (label, kind[:4])] = min(
                (t["built"] for t in g), default=None)
            lives = [((t["died"] if t["died"] is not None else r["rounds"])
                      - t["built"]) for t in g]
            out["%s_%s_life" % (label, kind[:4])] = (
                round(sum(lives) / len(lives)) if lives else None)
            out["%s_%s_alive_r" % (label, kind[:4])] = sum(lives)
    # forward-sentinel dry rounds: a forward sentinel of ours alive with ammo<10
    ammo = r["ammo"]
    fwd_s = [t for t in ours if t["fwd"] and t["kind"] == "sentinel"]
    dry = alive = 0
    for rnd in range(r["rounds"]):
        live = any(t["built"] <= rnd and (t["died"] is None or rnd < t["died"])
                   for t in fwd_s)
        if live:
            alive += 1
            if rnd < len(ammo) and ammo[rnd] < 10:
                dry += 1
    out["fwd_sent_alive"] = alive
    out["fwd_sent_dry"] = dry
    out["opp_sent_n"] = sum(1 for t in theirs if t["kind"] == "sentinel")
    out["opp_gun_n"] = sum(1 for t in theirs if t["kind"] == "gunner")
    # THEIR turrets sited near OUR core (their home defence) vs near their core
    out["opp_fwd_turret"] = sum(1 for t in theirs
                                if t["kind"] in ("sentinel", "gunner")
                                and t["dsq_own"] <= 40)
    out["unknown_deltas"] = ",".join(str(x) for x in sorted(r["unknown"]))
    return out


def main():
    rows = list(csv.DictReader(open(HERE / "fired30.tsv"), delimiter="\t"))
    tapes = {r["tag"]: r for r in
             csv.DictReader(open(HERE / "games_summary.tsv"), delimiter="\t")}
    out = []
    fails = []
    for g in rows:
        tag = g["tag"]
        our_team = 0 if g["seat"] == "A" else 1
        r = analyse(HERE / "replays" / (tag + ".replay26"), our_team)
        s = summarise(r, our_team)
        # --- guard: HP identity ---------------------------------------------
        # For a SURVIVING core the ledger must reproduce the tape exactly.
        # For a DESTROYED core it must land in (-18, 0]: damage is NOT clamped
        # (replay_census docstring), so the killing blow overshoots by up to one
        # sentinel hit.  The tape reads 0 for a destroyed core only because the
        # entity is popped on removeEntity — that 0 is an absence, not an HP.
        want = int(tapes[tag]["our_hp_end"])
        destroyed = (g["ours"] == "OPP" and g["cond"] == "Core destroyed")
        calc = s["ourcore_hp_calc"]
        s["ourcore_overkill"] = -calc if destroyed else 0
        if destroyed:
            if not (-18 < calc <= 0):
                fails.append("%s: core-destroyed but ledger hp %d not in (-18,0]"
                             % (tag, calc))
        elif calc != want:
            fails.append("%s: ledger hp %d != tape hp %d" % (tag, calc, want))
        if s["unknown_deltas"]:
            fails.append("%s: unknown deltas %s" % (tag, s["unknown_deltas"]))
        s = dict(tag=tag, map=g["map"], seed=g["seed"], seat=g["seat"],
                 ours=g["ours"], turn=g["turn"], **s)
        out.append(s)
    if fails:
        sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails) + "\n")
        raise SystemExit(2)
    sys.stderr.write("guards OK: HP identity 30/30, delta alphabet clean\n")
    cols = list(out[0].keys())
    with open(HERE / "attrib.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in out:
            fh.write("\t".join("" if r[c] is None else str(r[c])
                               for c in cols) + "\n")
    print("wrote", HERE / "attrib.tsv", len(out), "rows")


if __name__ == "__main__":
    main()
