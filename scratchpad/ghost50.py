"""ATTRIBUTE THE ~50 GHOST SENTINELS: kills, or blindness?

A ghost = a sentinel with opp_rounds == 0 (no enemy ever seen in its ray at an
end-of-round snapshot) that nevertheless FIRED. Two readings point opposite ways:
  KILL      -- it erased its own target in-round, so the snapshot misses it
               BECAUSE it worked; availability is understated for the side that
               kills more, and OUR ghost rate is 7.17x theirs.
  BLINDNESS -- a transient target we never see; availability is suppressed.
Decidable per case now that the wire is confirmed ORDERED within a Turn: for each
round in which a ghost fired, did a removeEntity land on a tile of ITS ray?
Read-only. Reuses the validated decoder for the ghost list and its ray.
"""
import csv, sys
from pathlib import Path
sys.path.insert(0, "scratchpad"); sys.path.insert(0, "tools")
import sent_read
from sent_read import analyse  # noqa
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa

SIDE = {"a": 0, "b": 1}
rows = []
with open("corpus/meta_join.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r.get("triggeredBy") == "ladder" and r.get("us_side") in SIDE:
            rows.append((r["file"], SIDE[r["us_side"]]))
AR = Path("replay_archive")

def ray_tiles(pos, direction, w, h):
    """The sentinel's firing line. `_ray` already returns the OFFSET tuple with
    the r^2<=32 cap applied, so reuse it rather than re-deriving the cap here --
    re-deriving it is how two decoders drift apart."""
    x, y = pos
    return {(x + dx, y + dy) for dx, dy in sent_read.RAY.get(direction, ())
            if 0 <= x + dx < w and 0 <= y + dy < h}


tally = {0: {"kill": 0, "blind": 0, "n": 0}, 1: {"kill": 0, "blind": 0, "n": 0}}
for fname, ours in rows:
    p = AR / fname
    if not p.exists():
        continue
    try:
        st = analyse(p, None)
    except Exception:
        continue
    ghosts = [r for r in st["sent"] if r["opp_rounds"] == 0 and r["shots"] > 0]
    if not ghosts:
        continue
    data = p.read_bytes()
    turns = []
    mapbuf = None
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN: mapbuf = val
        elif num == 3 and wire == WIRE_LEN: turns.append(val)
    w = h = 0
    for num, wire, val in fields(mapbuf):
        if num == 1: w = val
        elif num == 2: h = val
    grays = {g["id"]: ray_tiles(g["pos"], g["dir"], w, h) for g in ghosts}
    gpos = {g["id"]: g["pos"] for g in ghosts}
    fired_rounds = {g["id"]: set() for g in ghosts}
    hit = {g["id"]: False for g in ghosts}
    ent_pos = {}
    for rnd, tb in enumerate(turns):
        removed = set(); fires_from = []
        for _a, _b, ub in fields(tb):
            for un, _w2, ubuf in fields(ub):
                if un == 1:
                    for en, _e, eb in fields(ubuf):
                        if en == 1:
                            e = parse_entity(eb, rnd)
                            if e is not None: ent_pos[e.id] = e.pos
                elif un == 2:
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d: ent_pos[d[1]] = read_pos(d[2])
                elif un == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        q = ent_pos.pop(rv, None)
                        if q is not None: removed.add(q)
                elif un == 12:
                    d = {}
                    for fn, _fw, fv in fields(ubuf): d[fn] = fv
                    if 1 in d: fires_from.append(read_pos(d[1]))
        for gid, gp in gpos.items():
            if gp in fires_from:
                fired_rounds[gid].add(rnd)
                if removed & grays[gid]:
                    hit[gid] = True
    for g in ghosts:
        side = 0 if g["team"] == ours else 1
        tally[side]["n"] += 1
        tally[side]["kill" if hit[g["id"]] else "blind"] += 1

print("GHOST SENTINELS (opp_rounds==0 yet fired), our rated ladder games\n")
print(f"{'':<10}{'n':>5}{'KILL (removal on its ray, same round it fired)':>50}{'BLIND':>8}")
for side, lbl in ((0, "OURS"), (1, "THEIRS")):
    t = tally[side]
    n = max(t["n"], 1)
    print(f"{lbl:<10}{t['n']:>5}{t['kill']:>44} ({100*t['kill']/n:.0f}%){t['blind']:>8}")
