#!/usr/bin/env python3
"""diag F/G: why the ray-trigger dodge never saved a raider.

Read-only over the 24 v512 local replays.  Reuses walk.py / feat.py decoders.
"""
import collections
import math
import os
import sys

V512 = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures"
sys.path.insert(0, V512)
import feat
import walk

REP = os.path.join(V512, "replays")

SENT_R2 = 32
GUN_R2 = 13
BOT_VIS = 20


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def foot(p):
    return [(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)]


class Game:
    def __init__(self, tag, ordl):
        self.tag = tag
        mb, turns, winner, cond = walk.load(os.path.join(REP, tag + ".replay26"))
        self.W, self.H, self.tiles, cores = walk.parse_map(mb)
        self.n = len(turns)
        self.ourteam = 0 if ordl == "A" else 1
        self.oc = [c for c in cores if c["team"] == self.ourteam][0]
        self.ec = [c for c in cores if c["team"] != self.ourteam][0]
        self.ecf = foot(self.ec["pos"])
        self.winner, self.cond = winner, cond

        ents = {}
        born, died = {}, {}
        pos = {}
        hist = collections.defaultdict(dict)     # id -> {rnd: pos}
        hp = {}
        hphist = collections.defaultdict(list)   # id -> [(rnd, delta, hp_after)]
        draws = collections.Counter()
        fires = []                               # (rnd, seq, frm, to)
        hits = []                                # (rnd, victim, delta, source_kind, source_id, frm)
        allfires_by_src = collections.defaultdict(list)
        jumps = []

        seq = 0
        raw_att = []
        recent_fires = []   # this round: (seq, frm, to)
        recent_atk = []     # this round: (seq, attacker_id, target)
        cur_rnd = -1
        attacks = []        # (rnd, attacker_id, target)
        for rnd, k, p in walk.events(turns):
            if rnd != cur_rnd:
                cur_rnd = rnd
                recent_fires = []
                recent_atk = []
            seq += 1
            if k == "place":
                if p.id not in ents:
                    ents[p.id] = {"team": p.team, "kind": p.kind, "birth": tuple(p.pos)}
                    born[p.id] = rnd
                    hp[p.id] = p.hp
                pos[p.id] = tuple(p.pos)
                hist[p.id][rnd] = tuple(p.pos)
            elif k == "move":
                old = pos.get(p["id"])
                pos[p["id"]] = tuple(p["to"])
                hist[p["id"]][rnd] = tuple(p["to"])
                if old and abs(old[0] - p["to"][0]) + abs(old[1] - p["to"][1]) > 1:
                    jumps.append((rnd, p["id"], old, tuple(p["to"])))
            elif k == "remove":
                died[p["id"]] = rnd
            elif k == "fire":
                frm, to = tuple(p["from"]), tuple(p["to"])
                fires.append((rnd, seq, frm, to))
                recent_fires.append((seq, frm, to))
                src = None
                for eid, e in ents.items():
                    if pos.get(eid) == frm and e["kind"] in ("sentinel", "gunner", "launcher") \
                       and eid not in died:
                        src = eid
                        break
                allfires_by_src[src].append((rnd, frm, to))
            elif k == "attack":
                recent_atk.append((seq, p["id"], tuple(p["target"])))
                attacks.append((rnd, p["id"], tuple(p["target"])))
            elif k in ("dot", "line"):
                draws[p["id"]] += 1
            elif k == "hp":
                eid = p["id"]
                hp[eid] = hp.get(eid, 0) + p["delta"]
                hphist[eid].append((rnd, p["delta"], hp[eid]))
                if p["delta"] < 0:
                    hits.append([rnd, eid, p["delta"], None, None, None, pos.get(eid)])
                    raw_att.append((rnd, eid, p["delta"], pos.get(eid)))

        self.ents, self.born, self.died = ents, born, died
        self.hist, self.hphist, self.draws = hist, hphist, draws
        self.fires = fires
        self.allfires_by_src = allfires_by_src
        self.jumps = jumps
        self.finalpos = pos
        self.attacks = attacks

        # ---- SECOND PASS: attribute each damaging hp event to a fire.
        # Within-round event order is unit-execution order, so the victim's
        # position at hp-event time can be either its pre- or post-move tile.
        # Match on the FIRE's `to` tile against {pos(r-1), pos(r), pos_at_event},
        # and disambiguate with the damage magnitude (18 = sentinel, 7 = gunner,
        # 2 = builder attack) -- the delta alphabet measured on these replays.
        turret_at = {}
        for eid, e in ents.items():
            if e["kind"] in ("sentinel", "gunner"):
                turret_at.setdefault(e["birth"], []).append(eid)
        DMG = {"sentinel": 18, "gunner": 7}
        fires_by_rnd = collections.defaultdict(list)
        for (r, s, f, t) in fires:
            fires_by_rnd[r].append((s, f, t))
        self.unattributed = []
        for h in hits:
            rnd, eid, delta, _, _, _, evpos = h
            cands = {evpos, self.posat(eid, rnd), self.posat(eid, rnd - 1)}
            cands.discard(None)
            best = None
            for (s, f, t) in fires_by_rnd.get(rnd, []):
                if t not in cands:
                    continue
                srcs = turret_at.get(f, [])
                for cid in srcs:
                    if DMG.get(ents[cid]["kind"]) == -delta:
                        best = (ents[cid]["kind"], cid, f, t)
                        break
                if best:
                    break
                if srcs and best is None:
                    best = (ents[srcs[0]]["kind"], srcs[0], f, t)
            if best is None:
                for (r2, aid, t) in attacks:
                    if r2 == rnd and t in cands:
                        best = ("builder_attack", aid, pos.get(aid), t)
                        break
            if best is None:
                self.unattributed.append((rnd, eid, delta, evpos))
                h[3], h[4], h[5] = None, None, None
                h.append(None)
            else:
                h[3], h[4], h[5] = best[0], best[1], best[2]
                h.append(best[3])   # index 7 = hit tile (fire `to`)
        self.hits = hits

    def posat(self, eid, rnd):
        h = self.hist.get(eid, {})
        best = None
        for r in h:
            if r <= rnd and (best is None or r > best):
                best = r
        if best is None:
            # not yet born at rnd -> use birth pos
            return self.ents[eid]["birth"] if eid in self.ents else None
        return h[best]

    def is_wall(self, x, y):
        if not (0 <= x < self.W and 0 <= y < self.H):
            return True
        return self.tiles[y][x] == 1


def ray_dir(frm, to):
    dx, dy = to[0] - frm[0], to[1] - frm[1]
    g = math.gcd(abs(dx), abs(dy))
    if g == 0:
        return None
    return (dx // g, dy // g)


def on_same_ray(frm, prev_to, tile):
    """Is `tile` on the straight line from frm through prev_to (same side)?"""
    d1 = ray_dir(frm, prev_to)
    d2_ = ray_dir(frm, tile)
    return d1 is not None and d1 == d2_


def steps_out_of_range(g, start, turret, rng2):
    """BFS over non-wall terrain: cardinal steps to first tile with d2>rng2."""
    if d2(start, turret) > rng2:
        return 0
    seen = {start}
    q = collections.deque([(start, 0)])
    while q:
        (x, y), dist = q.popleft()
        if dist > 25:
            return None
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen or g.is_wall(nx, ny):
                continue
            seen.add((nx, ny))
            if d2((nx, ny), turret) > rng2:
                return dist + 1
            q.append(((nx, ny), dist + 1))
    return None


def analyse(g):
    ourteam = g.ourteam
    raiders = set(i for i in g.draws
                  if g.ents.get(i, {}).get("team") == ourteam
                  and g.ents[i]["kind"] == "builder_bot")
    # set B: all our builder deaths with death position d2<=60 from enemy core
    setB = set()
    for i, e in g.ents.items():
        if e["team"] != ourteam or e["kind"] != "builder_bot":
            continue
        if i not in g.died:
            continue
        dp = g.posat(i, g.died[i])
        if dp and d2(dp, g.ec["pos"]) <= 60:
            setB.add(i)

    rows = []
    for i in sorted(raiders | setB):
        if i not in g.died:
            continue
        drnd = g.died[i]
        dp = g.posat(i, drnd)
        myhits = [h for h in g.hits if h[1] == i]
        # only damaging events
        myhits = [h for h in myhits if h[2] < 0]
        fatal = None
        for h in reversed(myhits):
            if h[0] <= drnd:
                fatal = h
                break
        pen = None
        if fatal is not None:
            idx = myhits.index(fatal)
            if idx > 0:
                pen = myhits[idx - 1]
        killer_id = fatal[4] if fatal else None
        killer_kind = fatal[3] if fatal else None
        killer_pos = fatal[5] if fatal else None
        rpos_fatal = (fatal[7] if (fatal and fatal[7]) else
                      (g.posat(i, fatal[0]) if fatal else dp))
        fatal_d2 = d2(rpos_fatal, killer_pos) if killer_pos else None
        pen_d2 = None
        pen_tile = None
        if pen and pen[5]:
            pen_tile = pen[7] if pen[7] else g.posat(i, pen[0])
            pen_d2 = d2(pen_tile, pen[5])
        firsthit = myhits[0] if myhits else None
        dmg_rounds = sorted(set(h[0] for h in myhits))
        rounds_before_death = [r for r in dmg_rounds if r < (fatal[0] if fatal else drnd)]

        # vision test
        vis_min = None
        vis_ever = False
        if killer_pos and fatal:
            for r in range(max(0, fatal[0] - 10), fatal[0]):
                if r < g.born.get(i, 0):
                    continue
                rp = g.posat(i, r)
                if rp is None:
                    continue
                dd = d2(rp, killer_pos)
                if vis_min is None or dd < vis_min:
                    vis_min = dd
                if dd <= BOT_VIS:
                    vis_ever = True
        # d2 at the moment of first damage FROM THAT TURRET
        first_from_killer = None
        for h in myhits:
            if killer_id is not None and h[4] == killer_id:
                first_from_killer = h
                break
            if killer_id is None and h[5] == killer_pos:
                first_from_killer = h
                break
        d2_firstdmg = None
        if first_from_killer and first_from_killer[5]:
            ft = first_from_killer[7] or g.posat(i, first_from_killer[0])
            d2_firstdmg = d2(ft, first_from_killer[5])

        # ray test on the fatal tile
        ray_same = ray_any = None
        if killer_pos and fatal:
            prev_same = [f for f in g.fires if f[2] == killer_pos and f[0] < fatal[0]]
            ray_same = any(on_same_ray(killer_pos, f[3], rpos_fatal) for f in prev_same)
            enemy_turret_pos = set()
            for eid, e in g.ents.items():
                if e["team"] != ourteam and e["kind"] in ("sentinel", "gunner"):
                    enemy_turret_pos.add(e["birth"])
            ray_any = False
            for f in g.fires:
                if f[0] >= fatal[0] or f[2] not in enemy_turret_pos:
                    continue
                if on_same_ray(f[2], f[3], rpos_fatal):
                    ray_any = True
                    break

        # hp reconstruction
        hp_after_pen = None
        if pen:
            hp_after_pen = pen[2 + 0]  # placeholder
        hpseq = g.hphist.get(i, [])
        hp_after_pen = None
        if pen:
            for (r, dl, after) in hpseq:
                if r == pen[0] and dl == pen[2]:
                    hp_after_pen = after
                    break
        rounds_at_that_hp = (fatal[0] - pen[0]) if (pen and fatal) else None

        # retreat feasibility
        rng2 = SENT_R2 if killer_kind == "sentinel" else (GUN_R2 if killer_kind == "gunner" else None)
        retreat = None
        if killer_pos and rng2 and pen_tile:
            retreat = steps_out_of_range(g, pen_tile, killer_pos, rng2)
        retreat_from_fatal = None
        if killer_pos and rng2:
            retreat_from_fatal = steps_out_of_range(g, rpos_fatal, killer_pos, rng2)

        rows.append(dict(
            tag=g.tag, rid=i, is_raider=(i in raiders), in_setB=(i in setB),
            born=g.born[i], died=drnd, deathpos=dp,
            d2_to_ecore=d2(dp, g.ec["pos"]) if dp else None,
            killer_kind=killer_kind, killer_id=killer_id, killer_pos=killer_pos,
            fatal_rnd=fatal[0] if fatal else None, fatal_delta=fatal[2] if fatal else None,
            fatal_d2=fatal_d2, pen_rnd=pen[0] if pen else None, pen_d2=pen_d2,
            pen_kind=pen[3] if pen else None,
            first_hit_rnd=firsthit[0] if firsthit else None,
            warn_first=(drnd - firsthit[0]) if firsthit else None,
            gap_pen_fatal=(fatal[0] - pen[0]) if (pen and fatal) else None,
            n_dmg_rounds_before=len(rounds_before_death),
            n_hits=len(myhits),
            vis_ever=vis_ever, vis_min=vis_min, d2_firstdmg=d2_firstdmg,
            ray_same=ray_same, ray_any=ray_any,
            hp_after_pen=hp_after_pen, rounds_at_hp=rounds_at_that_hp,
            retreat_steps=retreat, retreat_from_fatal=retreat_from_fatal,
            fatal_tile=rpos_fatal, pen_tile=pen_tile,
            hpseq=[(r, dl, a) for r, dl, a in hpseq],
            hitlog=[(h[0], h[2], h[3], h[5], h[7]) for h in myhits],
        ))
    return rows, raiders, setB


def main():
    B = {r["tag"]: r for r in feat.load_batch()}
    allrows = []
    meta = []
    unatt = 0
    for tag in sorted(B):
        g = Game(tag, B[tag]["ord"])
        rows, raiders, setB = analyse(g)
        allrows += rows
        unatt += len(g.unattributed)
        meta.append((tag, len(raiders), len([i for i in raiders if i in g.died]), len(setB)))
    print("UNATTRIBUTED damaging hp events across all entities, all 24 games: %d" % unatt)
    import pickle
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rows.pkl"), "wb") as fh:
        pickle.dump((allrows, meta), fh)
    print("games=%d  rows=%d" % (len(meta), len(allrows)))
    for m in meta:
        print("   %-16s raiders=%d raider_deaths=%d setB_deaths=%d" % m)


if __name__ == "__main__":
    main()
