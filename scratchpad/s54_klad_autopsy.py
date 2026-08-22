"""Core-kill autopsy for the kladde v173 study.

Attribution rule from tools/replay_schema.md "Damage-target law" (same rule
tools/corpus/replay_autopsy.py uses):
  * FireTurret {from,to} with `to` on the victim core footprint AND no unit on
    that tile -> damage to the core; shooter resolved from `from` occupancy.
  * BuilderAttack {id,target} with target on the footprint and no unit there
    -> 2 dmg.
Self-check: attributed damage must equal the summed negative UpdateHp deltas on
the core id. Mismatch is REPORTED, not hidden.
Occupancy is resolved at ROUND START (schema.md FireTurret ordering trap).
"""
from __future__ import annotations

import sys
sys.path.insert(0, "scratchpad")
from s54_klad_lib import Game, d2  # noqa: E402

DMG = {"gunner": 7, "sentinel": 18}


def autopsy(g: Game, victim_team: int):
    """Return dict: attribution of damage to `victim_team`'s core."""
    cid = g.core_id(victim_team)
    fp = g.footprint(victim_team)
    # ledger of true damage from UpdateHp
    true_dmg = 0
    for rnd, kind, pl in g.ev:
        if kind == "HP" and pl[0] == cid and pl[1] < 0:
            true_dmg += -pl[1]

    # walk rounds keeping round-start occupancy
    pos = {}
    for c in g.cores:
        pos[c["id"]] = c["pos"]
    alive = {c["id"] for c in g.cores}
    attrib = {}          # source-kind -> damage
    by_round = []        # (rnd, kind, dmg, srcpos, d2_to_core)
    unattrib = 0

    # group events by round
    from itertools import groupby
    core_nw = g.core_pos(victim_team)
    for rnd, evs in groupby(g.ev, key=lambda e: e[0]):
        evs = list(evs)
        # round-start occupancy: unit ids (builder bots + turrets are units;
        # for the damage-target law only BODIES on the tile matter)
        occ = {}
        for eid in alive:
            e = g.ever[eid]
            if e["kind"] in ("builder_bot", "gunner", "sentinel", "launcher", "core"):
                occ.setdefault(pos.get(eid), set()).add(eid)
        for _r, kind, pl in evs:
            if kind == "FIRE":
                frm, to = pl
                if to in fp:
                    # unit on target tile absorbs (unit priority)
                    bodies = [i for i in occ.get(to, ()) if g.ever[i]["kind"] != "core"]
                    if bodies:
                        continue
                    shooter = None
                    for eid in alive:
                        if pos.get(eid) == frm and g.ever[eid]["kind"] in DMG:
                            shooter = eid
                            break
                    if shooter is None:
                        unattrib += 1
                        by_round.append((rnd, "unattrib_fire", 0, frm,
                                         d2(frm, core_nw)))
                        continue
                    k = g.ever[shooter]["kind"]
                    attrib[k] = attrib.get(k, 0) + DMG[k]
                    by_round.append((rnd, k, DMG[k], frm, d2(frm, core_nw)))
            elif kind == "BATK":
                bid, tgt = pl
                if tgt in fp:
                    bodies = [i for i in occ.get(tgt, ()) if g.ever[i]["kind"] != "core"]
                    if bodies:
                        continue
                    attrib["builder"] = attrib.get("builder", 0) + 2
                    by_round.append((rnd, "builder", 2, pos.get(bid),
                                     d2(pos.get(bid, core_nw), core_nw)))
        # apply the round's state changes
        for _r, kind, pl in evs:
            if kind in ("BUILD", "REEMIT"):
                pos[pl[0]] = pl[3]
                alive.add(pl[0])
            elif kind == "MOVE":
                pos[pl[0]] = pl[2]
            elif kind == "DEATH":
                alive.discard(pl[0])
    return {"true": true_dmg, "attrib": attrib, "by_round": by_round,
            "unattrib_fire": unattrib,
            "sum": sum(attrib.values())}
