"""WHAT ARE THE 'GHOST' SHOTS? — sentinels that fired with 0 end-of-round availability.

Two candidate explanations and they point in OPPOSITE directions:
  (a) transient targets we cannot see  -> availability is suppressed for us
  (b) the target DIED in the round it was shot -> the snapshot misses it BECAUSE
      we killed it, which is a consequence of firing, not a suppression of
      opportunity.
Discriminator: for each ghost shot, was there a removeEntity for an enemy entity
standing on the shot's target tile in that same round?
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa

SIDE = {"a": 0, "b": 1}
rows = []
with open("corpus/meta_join.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r.get("triggeredBy") == "ladder" and r.get("us_side") in SIDE:
            rows.append((r["file"], SIDE[r["us_side"]]))
AR = Path("replay_archive")
same_round_death = 0
no_death = 0
n = 0
for fname, ours in rows[:600]:
    p = AR / fname
    if not p.exists():
        continue
    data = p.read_bytes()
    turns = []
    for num, wire, val in fields(data):
        if num == 3 and wire == WIRE_LEN:
            turns.append(val)
    ent_pos, ent_team = {}, {}
    for rnd, tb in enumerate(turns):
        fires, removed_pos = [], set()
        pend = []
        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:
                    for en, _e, eb in fields(ubuf):
                        if en == 1:
                            e = parse_entity(eb, rnd)
                            if e is not None:
                                ent_pos[e.id] = e.pos; ent_team[e.id] = e.team
                elif un == 2:
                    d = {k: v for k, _w2, v in fields(ubuf)}
                    if 1 in d and 2 in d:
                        ent_pos[d[1]] = read_pos(d[2])
                elif un == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        if rv in ent_pos:
                            removed_pos.add(ent_pos[rv])
                        ent_pos.pop(rv, None); ent_team.pop(rv, None)
                elif un == 12:
                    d = {}
                    for fn, _fw, fv in fields(ubuf):
                        d[fn] = fv
                    if 2 in d:
                        fires.append(read_pos(d[2]))
        for tgt in fires:
            n += 1
            if tgt in removed_pos:
                same_round_death += 1
            else:
                no_death += 1
print(f"turret shots examined: {n:,}  (600-replay slice of our rated ladder games)")
print(f"  target tile ALSO saw a removeEntity that same round: {same_round_death:,} "
      f"= {100*same_round_death/max(n,1):.2f}%")
print(f"  no same-round removal on the target tile:            {no_death:,}")
