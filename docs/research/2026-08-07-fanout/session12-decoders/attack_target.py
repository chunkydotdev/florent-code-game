#!/usr/bin/env python3
"""What was a given (file, round, unit_id) attacking, and what killed it?"""
import importlib.util
import sys
from pathlib import Path

RC_PATH = Path("/Users/junghard/Projects/Work/florent-code-game/tools/replay_census.py")
spec = importlib.util.spec_from_file_location("replay_census", RC_PATH)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def analyze(path, target_round, target_id):
    data = Path(path).read_bytes()
    turn_bufs = []
    map_buf = None
    for num, wire, value in rc.fields(data):
        if num == 1 and wire == rc.WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == rc.WIRE_LEN:
            turn_bufs.append(value)

    entities = {}
    for num, wire, value in rc.fields(map_buf):
        if num == 4:
            core = {"id": 0, "team": 0, "pos": (0, 0)}
            for cnum, _cw, cval in rc.fields(value):
                if cnum == 1:
                    core["id"] = cval
                elif cnum == 2:
                    core["team"] = cval
                elif cnum == 3:
                    core["pos"] = rc.read_pos(cval)
            entities[core["id"]] = rc.Entity(core["id"], core["team"], core["pos"], "core", 500, 500, None, 0)

    for rnd, turn_buf in enumerate(turn_bufs):
        if rnd > target_round:
            break
        round_updates = []
        for _num, _wire, update_buf in rc.fields(turn_buf):
            for unum, _uwire, ubuf in rc.fields(update_buf):
                round_updates.append((unum, ubuf))
        for unum, ubuf in round_updates:
            if unum == 1:
                for enum_, _ew, ebuf in rc.fields(ubuf):
                    if enum_ != 1:
                        continue
                    ent = rc.parse_entity(ebuf, rnd)
                    if ent:
                        entities[ent.id] = ent
            elif unum == 2:
                eid = to = None
                for mnum, _mw, mval in rc.fields(ubuf):
                    if mnum == 1:
                        eid = mval
                    elif mnum == 2:
                        to = rc.read_pos(mval)
                e = entities.get(eid)
                if e and to:
                    e.pos = to
        if rnd == target_round:
            for unum, ubuf in round_updates:
                if unum == 13:
                    d = rc.scalars(ubuf)
                    if d.get(1) == target_id:
                        tgt = rc.read_pos(d[2]) if 2 in d else None
                        occ = [e for e in entities.values() if e.pos == tgt]
                        print(f"{path} r{rnd} unit {target_id} attacked {tgt}: "
                              f"{[(e.kind, 'A' if e.team==0 else 'B', e.id, e.hp, e.max_hp) for e in occ]}")
            for unum, ubuf in round_updates:
                if unum == 3:
                    for rnum, _rw, rval in rc.fields(ubuf):
                        if rnum == 1:
                            entities.pop(rval, None)
            break
        for unum, ubuf in round_updates:
            if unum == 3:
                for rnum, _rw, rval in rc.fields(ubuf):
                    if rnum == 1:
                        entities.pop(rval, None)


if __name__ == "__main__":
    cases = [
        ("replays/orizon_g1.replay26", 14, 4),
        ("replays/orizon_g3.replay26", 54, 4),
        ("replays/orizon_g3.replay26", 108, 10),
        ("replays/orizon_g5.replay26", 27, 10),
        ("replays/ouroboros_g1.replay26", 70, 10),
        ("replays/ouroboros_g2.replay26", 180, 4),
        ("replays/ouroboros_g3.replay26", 40, 4),
        ("replays/ouroboros_g4.replay26", 44, 4),
        ("replays/ouroboros_g4.replay26", 56, 9),
        ("replays/ouroboros_g5.replay26", 45, 4),
        ("replays/singlecore_g3.replay26", 26, 4),
    ]
    for path, rnd, uid in cases:
        analyze(path, rnd, uid)
