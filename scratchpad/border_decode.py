#!/usr/bin/env python3
"""Natural border-crash decoder for the four LOKI-14b carriers.

Per replay, for ONE named team (the carrier), emits:
  - border / off-border builder-ROUNDS (denominators), measured at ROUND START
  - undamaged builder removals (crash_census rule: removeEntity with no
    updateHp EVER for that id), split by border/off-border and by whether the
    builder was THROWN (a moveBuilderBot of >1 tile) within 3 rounds
  - the same for damage-killed removals, for scale

Reuses tools/replay_census.py primitives (fields, parse_entity, read_pos).
Read-only. Scratch.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
sys.path.insert(0, "tools")
from replay_census import fields, parse_entity, read_pos, WIRE_LEN  # noqa: E402


def decode(path: Path, team_idx: int) -> dict:
    data = path.read_bytes()
    map_buf = None
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        raise ValueError(f"{path}: no map")
    W = H = None
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            W = value
        elif num == 2:
            H = value
        elif num == 4 and wire == WIRE_LEN:
            cid = cteam = None
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    cid = cv
                elif cn == 2:
                    cteam = cv
            if cid is not None:
                cores.append((cid, cteam or 0))
    if not W or not H:
        raise ValueError(f"{path}: no map dims W={W} H={H}")

    nrounds = len(turn_bufs)
    last = nrounds - 1

    # id -> (team, kind); builders also tracked in pos{}
    ents = {cid: (cteam, "core") for cid, cteam in cores}
    pos = {}                      # builder id -> current pos
    born = {}                     # builder id -> placement round
    damaged = set()               # ids that ever had an updateHp
    thrown_round = {}             # builder id -> last round it was thrown
    core_removed = {}             # team -> round

    hp = {}                       # builder id -> reconstructed hp
    everneg = set()
    throws = 0                    # >1-tile moveBuilderBot of THIS team's builders

    bnd_rounds = 0
    off_rounds = 0
    # events: list of dicts
    und = []      # undamaged builder removals
    dmg = []      # damage-killed builder removals
    other_und = []  # undamaged removals of non-builder unit kinds (for scale)

    for rnd, turn_buf in enumerate(turn_bufs):
        # --- ROUND-START denominator over living builders of team_idx ---
        start_pos = {}
        for bid, p in pos.items():
            if ents.get(bid, (None, None))[0] != team_idx:
                continue
            start_pos[bid] = p
            if p[0] == 0 or p[1] == 0 or p[0] == W - 1 or p[1] == H - 1:
                bnd_rounds += 1
            else:
                off_rounds += 1

        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                  # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in ents:          # rotation re-emit guard
                            continue
                        ents[e.id] = (e.team, e.kind)
                        if e.kind == "builder_bot":
                            pos[e.id] = e.pos
                            hp[e.id] = e.hp
                            born[e.id] = rnd
                elif unum == 2:                                # moveBuilderBot
                    bid = None
                    to = None
                    for n2, w2, v2 in fields(ubuf):
                        if n2 == 1:
                            bid = v2
                        elif n2 == 2 and w2 == WIRE_LEN:
                            to = read_pos(v2)
                    if bid is not None and to is not None:
                        old = pos.get(bid)
                        if old is not None:
                            d = max(abs(old[0] - to[0]), abs(old[1] - to[1]))
                            if d > 1:
                                thrown_round[bid] = rnd
                                if ents.get(bid, (None,))[0] == team_idx:
                                    throws += 1
                        pos[bid] = to
                elif unum == 5:                                # updateHp
                    eid = None
                    delta = 0
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            eid = v2
                        elif n2 == 2:
                            # 64-bit two's-complement varint (corpus-howto TRAP 2)
                            delta = v2 - (1 << 64) if v2 >= (1 << 63) else v2
                    if eid is not None:
                        damaged.add(eid)
                        if eid in hp:
                            hp[eid] += delta
                            if delta < 0:
                                everneg.add(eid)
                elif unum == 3:                                # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        tk = ents.pop(rv, None)
                        p = pos.pop(rv, None)
                        hp_at = hp.pop(rv, None)
                        if tk is None:
                            continue
                        team, kind = tk
                        if kind == "core":
                            core_removed.setdefault(team, rnd)
                        if team != team_idx:
                            continue
                        if kind == "builder_bot":
                            sp = start_pos.get(rv, p)
                            if sp is None:
                                continue
                            border = (sp[0] == 0 or sp[1] == 0
                                      or sp[0] == W - 1 or sp[1] == H - 1)
                            tr = thrown_round.get(rv)
                            rec = {"round": rnd, "x": sp[0], "y": sp[1],
                                   "border": border,
                                   "final": rnd == last,
                                   "thrown3": tr is not None and rnd - tr <= 3,
                                   "ever_thrown": tr is not None,
                                   "hp_at": hp_at,
                                   "everneg": rv in everneg,
                                   "nohp": rv not in damaged,
                                   "age": rnd - born.get(rv, -1),
                                   "in_denom": rv in start_pos}
                            (dmg if rv in damaged else und).append(rec)
                        elif kind in ("gunner", "sentinel", "launcher", "core"):
                            if rv not in damaged:
                                other_und.append({"round": rnd, "kind": kind})

    return {
        "file": path.name, "W": W, "H": H, "rounds": nrounds,
        "team_idx": team_idx,
        "border_builder_rounds": bnd_rounds,
        "offborder_builder_rounds": off_rounds,
        "throws_of_own_builders": throws,
        "undamaged": und, "damage_killed": dmg,
        "other_undamaged_units": other_und,
        "core_removed": {str(k): v for k, v in core_removed.items()},
    }


if __name__ == "__main__":
    jobs = json.load(open(sys.argv[1]))   # [[path, team_idx, tag], ...]
    out = []
    for i, (p, t, tag) in enumerate(jobs):
        try:
            r = decode(Path(p), t)
            r["tag"] = tag
            out.append(r)
        except Exception as exc:                              # noqa: BLE001
            out.append({"file": Path(p).name, "tag": tag,
                        "error": f"{type(exc).__name__}: {exc}"})
        if (i + 1) % 100 == 0:
            print(f"  ...{i+1}/{len(jobs)}", file=sys.stderr, flush=True)
    json.dump(out, open(sys.argv[2], "w"))
