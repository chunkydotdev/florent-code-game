#!/usr/bin/env python3
"""Deep per-round decoder for Ouroboros replays. Read-only: imports
tools/replay_census.py for wire-format helpers and final-state aggregates,
then does a second pass over the same turn buffers to extract the
event-level detail replay_census.py doesn't retain (fire, builder melee,
heal, hp deltas, removals, ammo conversion, per-round player economy).

Usage: .venv/bin/python decode.py <file.replay26> [file2 ...]
Prints one detailed report per file to stdout.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
import replay_census as rc  # noqa: E402

TEAM_NAME = {0: "A", 1: "B"}
CARDINALS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def top_level(data: bytes):
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
    return map_buf, turn_bufs, winner, win_condition


def to_signed(v):
    """protobuf int32 negative values are wire-encoded as sign-extended 64-bit
    varints (10 bytes). Our varint reader treats everything as unsigned, so a
    delta of -7 comes back as 2**64 - 7. Recover the signed value."""
    if v >= 2 ** 63:
        return v - 2 ** 64
    return v


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def min_dsq_to_footprint(pos, footprint):
    return min(dsq(pos, t) for t in footprint)


class EventReplay:
    def __init__(self, path: Path):
        self.path = path
        data = path.read_bytes()
        map_buf, self.turn_bufs, self.winner, self.win_condition = top_level(data)
        # Reuse rc.Replay for map geometry + final aggregates (cheap, files are small).
        self.base = rc.Replay(path, track_flow=True)
        self.width, self.height = self.base.width, self.base.height
        self.cores = self.base.cores
        self.core_fp = {0: self.base.core_footprint(0), 1: self.base.core_footprint(1)}
        self.rounds = len(self.turn_bufs)

        # Live entity state as we replay.
        entities = {}
        for core in self.cores:
            entities[core["id"]] = dict(team=core["team"], kind="core", pos=core["pos"],
                                         hp=500, max_hp=500, built_round=0)

        self.builds = []       # (round, team, kind, id, pos)
        self.removes = []      # (round, id, team, kind, pos)
        self.fires = []        # (round, from_pos, to_pos, shooter_id, shooter_team, shooter_kind)
        self.battacks = []     # (round, attacker_id, attacker_team, target_pos)
        self.bheals = []       # (round, healer_id, healer_team, target_pos)
        self.hpdeltas = []     # (round, id, team, kind, delta, hp_after)
        self.convert_ammo = []  # (round, team, amount)
        self.players_over_time = []  # (round, {team0:{...}, team1:{...}})
        self.moves = []        # (round, id, team, kind, to_pos) -- builder bot moves incl. launcher throws

        for rnd, turn_buf in enumerate(self.turn_bufs):
            for _num, _wire, update_buf in rc.fields(turn_buf):
                for unum, _uwire, ubuf in rc.fields(update_buf):
                    if unum == 1:  # placeEntity
                        for enum_, _ew, ebuf in rc.fields(ubuf):
                            if enum_ != 1:
                                continue
                            ent = rc.parse_entity(ebuf, rnd)
                            if ent is None:
                                continue
                            entities[ent.id] = dict(team=ent.team, kind=ent.kind, pos=ent.pos,
                                                     hp=ent.hp, max_hp=ent.max_hp,
                                                     built_round=rnd, direction=ent.direction)
                            self.builds.append((rnd, ent.team, ent.kind, ent.id, ent.pos))
                    elif unum == 2:  # moveBuilderBot
                        eid = to = None
                        for mnum, _mw, mval in rc.fields(ubuf):
                            if mnum == 1:
                                eid = mval
                            elif mnum == 2:
                                to = rc.read_pos(mval)
                        e = entities.get(eid)
                        if e is not None and to is not None:
                            e["pos"] = to
                            self.moves.append((rnd, eid, e["team"], e["kind"], to))
                    elif unum == 3:  # removeEntity
                        for rnum_, _rw, rval in rc.fields(ubuf):
                            e = entities.pop(rval, None)
                            if e is not None:
                                self.removes.append((rnd, rval, e["team"], e["kind"], e["pos"]))
                            else:
                                self.removes.append((rnd, rval, None, None, None))
                    elif unum == 4:  # distributeResources -- skip detail, base already has totals
                        pass
                    elif unum == 5:  # updateHp
                        d = rc.scalars(ubuf)
                        eid, delta = d.get(1), to_signed(d.get(2, 0))
                        e = entities.get(eid)
                        if e is not None:
                            e["hp"] = e.get("hp", 0) + delta
                            self.hpdeltas.append((rnd, eid, e["team"], e["kind"], delta, e["hp"]))
                        else:
                            self.hpdeltas.append((rnd, eid, None, None, delta, None))
                    elif unum == 6:  # updatePlayers
                        for pnum, _pw, pval in rc.fields(ubuf):
                            if pnum != 1:
                                continue
                            snap = {}
                            for tnum, _tw, tval in rc.fields(pval):
                                if tnum in (1, 2):
                                    dd = rc.scalars(tval)
                                    snap[tnum - 1] = {
                                        "titanium": dd.get(1, 0),
                                        "resources_collected": dd.get(3, 0),
                                        "titanium_collected": dd.get(4, 0),
                                        "ammo": dd.get(7, 0),
                                    }
                            self.players_over_time.append((rnd, snap))
                    elif unum == 12:  # fireTurret
                        frm = to = None
                        for fnum, _fw, fval in rc.fields(ubuf):
                            if fnum == 1:
                                frm = rc.read_pos(fval)
                            elif fnum == 2:
                                to = rc.read_pos(fval)
                        shooter_id = shooter_team = shooter_kind = None
                        if frm is not None:
                            for eid, e in entities.items():
                                if e["pos"] == frm and e["kind"] in ("gunner", "sentinel", "builder_bot"):
                                    shooter_id, shooter_team, shooter_kind = eid, e["team"], e["kind"]
                                    break
                        self.fires.append((rnd, frm, to, shooter_id, shooter_team, shooter_kind))
                    elif unum == 13:  # builderAttack
                        aid = target = None
                        for anum, _aw, aval in rc.fields(ubuf):
                            if anum == 1:
                                aid = aval
                            elif anum == 2:
                                target = rc.read_pos(aval)
                        e = entities.get(aid)
                        self.battacks.append((rnd, aid, e["team"] if e else None, target))
                    elif unum == 14:  # coreConvertAmmo
                        d = rc.scalars(ubuf)
                        # proto3 omits zero-value fields on the wire, so team A
                        # (TEAM_A = 0) events have no field-1 byte at all.
                        self.convert_ammo.append((rnd, d.get(1, 0), d.get(2, 0)))
                    elif unum == 15:  # builderHeal
                        hid = target = None
                        for hnum, _hw, hval in rc.fields(ubuf):
                            if hnum == 1:
                                hid = hval
                            elif hnum == 2:
                                target = rc.read_pos(hval)
                        e = entities.get(hid)
                        self.bheals.append((rnd, hid, e["team"] if e else None, target))
                    # unum 7,8 (cooldowns), 9 (botOutput), 10/11 (indicators), 16 (builderBuild): skip

        self.final_entities = entities

    def counts_at(self, round_limit, team):
        """Reconstruct per-kind counts for `team` alive as of end of round_limit
        (inclusive), by replaying builds/removes up to that point."""
        alive = {}
        for rnd, t, kind, eid, pos in self.builds:
            if rnd > round_limit:
                break
            if t == team:
                alive[eid] = kind
        for rnd, eid, t, kind, pos in self.removes:
            if rnd > round_limit:
                break
            alive.pop(eid, None)
        out = {}
        for kind in alive.values():
            out[kind] = out.get(kind, 0) + 1
        return out

    def players_at(self, round_limit):
        """Last known player snapshot at or before round_limit."""
        snap = {0: {}, 1: {}}
        for rnd, s in self.players_over_time:
            if rnd > round_limit:
                break
            snap.update(s)
        return snap


def report(path: Path):
    r = EventReplay(path)
    print(f"\n{'=' * 100}")
    print(f"FILE: {path.name}")
    print(f"map {r.width}x{r.height}  rounds={r.rounds}  winner={TEAM_NAME.get(r.winner,'-')}"
          f"  win_condition={r.win_condition}")
    core_pos = {t: next((c['pos'] for c in r.cores if c['team'] == t), None) for t in (0, 1)}
    print(f"core A@{core_pos[0]}  core B@{core_pos[1]}  "
          f"core-core dsq={dsq(core_pos[0], core_pos[1]) if core_pos[0] and core_pos[1] else '-'}")

    # kill round detection: round our (team B) core is removed, if any
    our_core_id = next((c['id'] for c in r.cores if c['team'] == 1), None)
    enemy_core_id = next((c['id'] for c in r.cores if c['team'] == 0), None)
    our_core_death = next((rr for rr in r.removes if rr[1] == our_core_id), None)
    enemy_core_death = next((rr for rr in r.removes if rr[1] == enemy_core_id), None)
    print(f"our core id={our_core_id}  death={our_core_death}")
    print(f"enemy core id={enemy_core_id}  death={enemy_core_death}")

    # first builds per team/kind
    print("\n-- first build (round, pos) per team/kind --")
    firsts = {}
    for rnd, team, kind, eid, pos in r.builds:
        key = (team, kind)
        if key not in firsts:
            firsts[key] = (rnd, pos, eid)
    for team in (0, 1):
        row = []
        for kind in ("builder_bot", "gunner", "sentinel", "launcher", "harvester",
                     "conveyor", "splitter", "barrier"):
            got = firsts.get((team, kind))
            if got:
                d = min_dsq_to_footprint(got[1], r.core_fp[1 - team]) if kind in ("gunner", "sentinel", "launcher") else None
                extra = f" dsq_to_enemycore={d}" if d is not None else ""
                row.append(f"{kind}=r{got[0]}@{got[1]}{extra}")
        print(f"  team {TEAM_NAME[team]}: " + "; ".join(row))

    # army composition bands for enemy (team A / Ouroboros)
    kill_round = None
    if our_core_death:
        kill_round = our_core_death[0]
    checkpoints = [20, 40, 60, 80, 100, 120, 150, 200, 250, 300, 400, 500]
    if kill_round:
        checkpoints = sorted(set(c for c in checkpoints if c < kill_round) | {max(kill_round - 1, 0)})
    else:
        checkpoints = sorted(set(c for c in checkpoints if c < r.rounds))
    print(f"\n-- Ouroboros (team A) army composition bands (kill_round={kill_round}) --")
    for cp in checkpoints:
        c = r.counts_at(cp, 0)
        parts = ", ".join(f"{k}={v}" for k, v in sorted(c.items()))
        print(f"  r<={cp:4d}: {parts}")
    print(f"-- Our (team B) army composition bands --")
    for cp in checkpoints:
        c = r.counts_at(cp, 1)
        parts = ", ".join(f"{k}={v}" for k, v in sorted(c.items()))
        print(f"  r<={cp:4d}: {parts}")

    # economy curve
    print("\n-- economy at checkpoints (titanium, titanium_collected, ammo) --")
    for cp in checkpoints:
        p = r.players_at(cp)
        a, b = p.get(0, {}), p.get(1, {})
        print(f"  r<={cp:4d}: A ti={a.get('titanium','-')} coll={a.get('titanium_collected','-')} "
              f"ammo={a.get('ammo','-')}  |  B ti={b.get('titanium','-')} coll={b.get('titanium_collected','-')} "
              f"ammo={b.get('ammo','-')}")

    # kill mechanism: damage into our core in the last stretch before death
    if kill_round is not None:
        window_start = max(0, kill_round - 60)
        our_core_hp_events = [e for e in r.hpdeltas if e[1] == our_core_id]
        print(f"\n-- damage to OUR core, all HP delta events (id={our_core_id}) --")
        cum = 500
        first_dmg_round = None
        for rnd, eid, team, kind, delta, hp_after in our_core_hp_events:
            if delta < 0 and first_dmg_round is None:
                first_dmg_round = rnd
        print(f"  first damage to our core: round {first_dmg_round}")
        # sum damage in windows of 50 rounds
        from collections import defaultdict
        window_dmg = defaultdict(int)
        for rnd, eid, team, kind, delta, hp_after in our_core_hp_events:
            if delta < 0:
                window_dmg[rnd // 50 * 50] += -delta
        for w in sorted(window_dmg):
            print(f"  rounds {w}-{w+49}: {window_dmg[w]} dmg to our core")
        # fires landing on our core footprint, in the window before death
        core_hits = [f for f in r.fires if f[2] in r.core_fp[1] and f[0] >= window_start]
        print(f"\n  fireTurret shots landing on our core footprint in r{window_start}-{kill_round} "
              f"(n={len(core_hits)}):")
        by_shooter = defaultdict(list)
        for rnd, frm, to, sid, steam, skind in core_hits:
            by_shooter[(sid, steam, skind, frm)].append(rnd)
        for (sid, steam, skind, frm), rnds in sorted(by_shooter.items(), key=lambda x: min(x[1])):
            d = min_dsq_to_footprint(frm, r.core_fp[1]) if frm else None
            print(f"    shooter id={sid} team={TEAM_NAME.get(steam,'?')} kind={skind} at {frm} "
                  f"dsq_to_ourcore={d}  shots={len(rnds)}  rounds={rnds[:5]}{'...' if len(rnds)>5 else ''}"
                  f"  last={rnds[-1]}")
        # builder melee attacks landing on our core tiles
        battacks_core = [ba for ba in r.battacks if ba[3] in r.core_fp[1] and ba[0] >= window_start]
        print(f"\n  builderAttack (melee) hits on our core footprint in r{window_start}-{kill_round} "
              f"(n={len(battacks_core)}):")
        by_att = defaultdict(list)
        for rnd, aid, ateam, target in battacks_core:
            by_att[(aid, ateam)].append(rnd)
        for (aid, ateam), rnds in sorted(by_att.items(), key=lambda x: min(x[1])):
            print(f"    attacker id={aid} team={TEAM_NAME.get(ateam,'?')}  hits={len(rnds)}  "
                  f"rounds={rnds[:5]}{'...' if len(rnds)>5 else ''}  last={rnds[-1]}")

    # enemy first turret near our core (siege signature)
    print("\n-- Ouroboros turret placements (all gunner/sentinel/launcher builds) --")
    for rnd, team, kind, eid, pos in r.builds:
        if team == 0 and kind in ("gunner", "sentinel", "launcher"):
            d = min_dsq_to_footprint(pos, r.core_fp[1])
            in_hunt_band = d <= 41
            in_intruder_band = d <= 20
            print(f"  r{rnd:4d} id={eid} {kind:9s} at {pos}  dsq_to_ourcore={d:4d}  "
                  f"hunt_band<=41:{in_hunt_band}  intruder_band<=20:{in_intruder_band}")

    # our defensive engagement: hunt (builderAttack on enemy turrets) and heal timing
    enemy_turret_ids = {eid for rnd, team, kind, eid, pos in r.builds if team == 0 and kind in ("gunner", "sentinel", "launcher")}
    our_hunt_attacks = [ba for ba in r.battacks if ba[2] == 1]
    # figure out which builderAttacks target a position that (at the time) held an enemy turret
    print(f"\n-- our team builderAttack events (melee), n={len(our_hunt_attacks)} --")
    if our_hunt_attacks:
        rounds_ = [ba[0] for ba in our_hunt_attacks]
        print(f"  first at r{min(rounds_)}, last at r{max(rounds_)}, count={len(rounds_)}")
        print(f"  sample: {our_hunt_attacks[:5]}")
    else:
        print("  NONE — our builders never landed a single melee attack this game")

    our_heals = [bh for bh in r.bheals if bh[2] == 1]
    print(f"\n-- our team builderHeal events, n={len(our_heals)} --")
    if our_heals:
        rounds_ = [bh[0] for bh in our_heals]
        print(f"  first at r{min(rounds_)}, last at r{max(rounds_)}, count={len(rounds_)}")
    else:
        print("  NONE — our builders never healed anything this game")

    # our builder deaths timeline
    our_builder_deaths = [rm for rm in r.removes if rm[2] == 1 and rm[3] == "builder_bot"]
    print(f"\n-- our builder_bot deaths, n={len(our_builder_deaths)} --")
    for rnd, eid, team, kind, pos in sorted(our_builder_deaths):
        d = min_dsq_to_footprint(pos, r.core_fp[1]) if pos else None
        # what hit near this position/round?
        nearby_fire = [f for f in r.fires if f[0] == rnd and f[2] == pos]
        nearby_battack = [ba for ba in r.battacks if ba[0] == rnd and ba[3] == pos]
        cause = ""
        if nearby_fire:
            cause = f"fire from {nearby_fire[0][1]} (team {TEAM_NAME.get(nearby_fire[0][4],'?')} {nearby_fire[0][5]})"
        elif nearby_battack:
            cause = f"melee from id={nearby_battack[0][1]} team {TEAM_NAME.get(nearby_battack[0][2],'?')}"
        print(f"  r{rnd:4d} id={eid} at {pos}  dsq_to_ourcore={d}  cause={cause or 'unknown/no-event-same-round'}")

    # ammo conversion (economy signal)
    print(f"\n-- coreConvertAmmo events: A={sum(a for r_,t,a in r.convert_ammo if t==0)} total, "
          f"B={sum(a for r_,t,a in r.convert_ammo if t==1)} total --")
    a_conv = [(rnd, amt) for rnd, t, amt in r.convert_ammo if t == 0]
    if a_conv:
        print(f"  Ouroboros first convert at r{a_conv[0][0]} amt={a_conv[0][1]}; n={len(a_conv)}")


def main():
    for arg in sys.argv[1:]:
        report(Path(arg))


if __name__ == "__main__":
    main()
