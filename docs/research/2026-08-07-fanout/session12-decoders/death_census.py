#!/usr/bin/env python3
"""Per-death, per-role census for seat-B builder losses.

Read-only analysis tool. Reuses the low-level wire parsing helpers from
tools/replay_census.py (fields/parse_entity/read_pos/scalars) rather than
duplicating them, and adds:

  - builder spawn-order tracking per team -> role_n attribution (0-indexed,
    matches the live bot's SLOT_ROLE_N counter: the Nth builder a team ever
    places, in ascending placeEntity order, gets role_n = N-1).
  - per-round FireTurret / BuilderAttack event tracking, correlated by
    position match against the position of a builder_bot at the moment of
    its removeEntity, to attribute a killer.
  - last-action-before-death classification (moved / built / healed /
    attacked / idle) from the update stream in the death round and the
    round immediately prior.

ROLE_N -> LIVE-BOT ROLE (from bots/_v72e2/main.py, confirmed by code read):
  0 = saboteur from spawn (forward siege engineer / first artillery builder)
  1 = expand, but calls self._intercept(ct) every turn before anything else
      (the interceptor; falls back to ordinary _pick-routed expand work on
      turns _intercept finds nothing to chase)
  2 = expand; sole promotion candidate to role_n=4 "defend" if the defender
      dies and stays dead > DEFEND_BEAT_STALE_RNDS past DEFEND_BEAT_MIN_RND
  3 = expand until (harv>=4 and round>=12), then permanently flips to
      saboteur (second forward artillery builder)
  4 = defend (home defender / counterbattery hunter); rare map-specific
      exceptions exist (nordkap mature_cap=4 has no native role_n==4 seat)
  5+ = generic expand (replacements bought back on death, later "surge" seats)

Usage:
    .venv/bin/python death_census.py replays/*.replay26
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RC_PATH = Path("/Users/junghard/Projects/Work/florent-code-game/tools/replay_census.py")
spec = importlib.util.spec_from_file_location("replay_census", RC_PATH)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)  # type: ignore

TEAM_NAME = {0: "A", 1: "B"}
ROLE_NAME = {
    0: "siege-engineer(saboteur@spawn)",
    1: "interceptor(role1)",
    2: "expand(defend-succession-cand)",
    3: "expand->2nd-saboteur@r12+",
    4: "defend(home defender)",
}


def role_label(role_n):
    if role_n is None:
        return "UNATTRIBUTED"
    return ROLE_NAME.get(role_n, f"expand(replacement,role_n={role_n})")


def core_footprint(pos, ):
    x, y = pos
    return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


def min_dist(pos, footprint):
    x, y = pos
    return min(abs(x - fx) + abs(y - fy) for fx, fy in footprint)


class DeathCensus:
    def __init__(self, path: Path):
        self.path = path
        data = path.read_bytes()
        map_buf = None
        turn_bufs = []
        winner = None
        win_condition = ""
        for num, wire, value in rc.fields(data):
            if num == 1 and wire == rc.WIRE_LEN:
                map_buf = value
            elif num == 3 and wire == rc.WIRE_LEN:
                turn_bufs.append(value)
            elif num == 4 and wire == rc.WIRE_VARINT:
                winner = value
            elif num == 6 and wire == rc.WIRE_LEN:
                win_condition = value.decode("utf-8", "replace")
        if map_buf is None:
            raise ValueError(f"{path}: not a replay")

        width = height = 0
        cores = []
        for num, wire, value in rc.fields(map_buf):
            if num == 1:
                width = value
            elif num == 2:
                height = value
            elif num == 4:
                core = {"id": 0, "team": 0, "pos": (0, 0)}
                for cnum, _cw, cval in rc.fields(value):
                    if cnum == 1:
                        core["id"] = cval
                    elif cnum == 2:
                        core["team"] = cval
                    elif cnum == 3:
                        core["pos"] = rc.read_pos(cval)
                cores.append(core)
        self.width, self.height, self.cores = width, height, cores
        self.winner, self.win_condition = winner, win_condition
        self.rounds = len(turn_bufs)

        core_pos = {c["team"]: c["pos"] for c in cores}
        self.core_fp = {t: core_footprint(core_pos[t]) for t in core_pos}

        entities = {}
        for c in cores:
            entities[c["id"]] = rc.Entity(c["id"], c["team"], c["pos"], "core", 500, 500, None, 0)

        spawn_order = {0: [], 1: []}
        deaths = []
        # per-unit last observed action classification (round, label)
        last_action = {}

        for rnd, turn_buf in enumerate(turn_bufs):
            # Materialize this round's updates once: within a Turn, event
            # ORDER DOES NOT MATCH temporal/resolution order for combat
            # events -- measured directly (ouroboros_g2 r81: the killing
            # FireTurret update is emitted AFTER the RemoveEntity it caused
            # in the wire stream). So combat correlation is done as an
            # unordered per-round set lookup, not a sequential scan.
            round_updates = []
            for _num, _wire, update_buf in rc.fields(turn_buf):
                for unum, _uwire, ubuf in rc.fields(update_buf):
                    round_updates.append((unum, ubuf))

            fires_to = []      # [(from_pos, to_pos)]
            atk_targets = []   # [(attacker_id, target_pos)]
            for unum, ubuf in round_updates:
                if unum == 12:  # fireTurret
                    d = rc.scalars(ubuf)
                    frm = rc.read_pos(d[1]) if 1 in d else None
                    to = rc.read_pos(d[2]) if 2 in d else None
                    fires_to.append((frm, to))
                elif unum == 13:  # builderAttack
                    d = rc.scalars(ubuf)
                    aid = d.get(1)
                    tgt = rc.read_pos(d[2]) if 2 in d else None
                    atk_targets.append((aid, tgt))

            for unum, ubuf in round_updates:
                if unum == 1:  # placeEntity
                    for enum_, _ew, ebuf in rc.fields(ubuf):
                        if enum_ != 1:
                            continue
                        ent = rc.parse_entity(ebuf, rnd)
                        if ent is None:
                            continue
                        entities[ent.id] = ent
                        if ent.kind == "builder_bot":
                            spawn_order[ent.team].append(ent.id)
                elif unum == 2:  # moveBuilderBot
                    eid = to = None
                    for mnum, _mw, mval in rc.fields(ubuf):
                        if mnum == 1:
                            eid = mval
                        elif mnum == 2:
                            to = rc.read_pos(mval)
                    ent = entities.get(eid)
                    if ent is not None and to is not None:
                        ent.pos = to
                        last_action[eid] = (rnd, "move")
                elif unum == 13:  # builderAttack
                    d = rc.scalars(ubuf)
                    aid = d.get(1)
                    if aid is not None:
                        last_action[aid] = (rnd, "attack")
                elif unum == 15:  # builderHeal
                    d = rc.scalars(ubuf)
                    if 1 in d:
                        last_action[d[1]] = (rnd, "heal")
                elif unum == 16:  # builderBuild
                    d = rc.scalars(ubuf)
                    if 1 in d:
                        last_action[d[1]] = (rnd, "build")
                elif unum == 3:  # removeEntity
                    for rnum, _rw, rval in rc.fields(ubuf):
                        if rnum != 1:
                            continue
                        eid = rval
                        ent = entities.get(eid)
                        if ent is not None and ent.kind == "builder_bot":
                            team = ent.team
                            pos = ent.pos
                            role_n = (spawn_order[team].index(eid)
                                      if eid in spawn_order[team] else None)
                            killer = "unknown"
                            killer_team = None
                            # Unordered per-round match: any FireTurret whose
                            # `to` equals this unit's death-round position,
                            # fired by an enemy gunner/sentinel standing at
                            # the matching `from` tile.
                            for frm, to in fires_to:
                                if to == pos and frm is not None:
                                    shooter = None
                                    for e2 in entities.values():
                                        if (e2.pos == frm
                                                and e2.kind in ("gunner", "sentinel")
                                                and e2.team != team):
                                            shooter = e2
                                            break
                                    if shooter is not None:
                                        killer = shooter.kind
                                        killer_team = shooter.team
                                    else:
                                        killer = "turret(shooter-not-found)"
                                    break
                            if killer == "unknown":
                                for aid, tgt in atk_targets:
                                    if tgt == pos:
                                        killer = "builder_attack(?!-should-not-kill-units)"
                                        break
                            own_fp = self.core_fp.get(team, set())
                            enemy_fp = self.core_fp.get(1 - team, set())
                            act_rnd, act_label = last_action.get(eid, (None, "idle/unseen"))
                            deaths.append({
                                "id": eid,
                                    "team": team,
                                    "role_n": role_n,
                                    "round": rnd,
                                    "pos": pos,
                                    "dist_own_core": min_dist(pos, own_fp) if own_fp else None,
                                    "dist_enemy_core": min_dist(pos, enemy_fp) if enemy_fp else None,
                                    "killer": killer,
                                    "killer_team": killer_team,
                                    "last_action_round": act_rnd,
                                    "last_action": act_label,
                                })
                        entities.pop(eid, None)

        self.deaths = deaths
        self.spawn_order = spawn_order


def main():
    paths = [Path(p) for p in sys.argv[1:]]
    cols = ["file", "map_wh", "rounds_total", "win_cond", "winner",
            "team", "unit_id", "role_n", "role", "death_round",
            "pos", "dist_own_core", "dist_enemy_core",
            "killer", "last_action_round", "last_action"]
    print("\t".join(cols))
    for path in paths:
        try:
            dc = DeathCensus(path)
        except Exception as exc:
            print(f"{path}: FAILED {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        for d in sorted(dc.deaths, key=lambda x: (x["round"], x["team"])):
            row = [
                path.name,
                f"{dc.width}x{dc.height}",
                str(dc.rounds),
                dc.win_condition,
                TEAM_NAME.get(dc.winner, "-"),
                TEAM_NAME.get(d["team"], "?"),
                str(d["id"]),
                str(d["role_n"]),
                role_label(d["role_n"]),
                str(d["round"]),
                f'{d["pos"][0]},{d["pos"][1]}',
                str(d["dist_own_core"]),
                str(d["dist_enemy_core"]),
                d["killer"],
                str(d["last_action_round"]),
                d["last_action"],
            ]
            print("\t".join(row))


if __name__ == "__main__":
    main()
