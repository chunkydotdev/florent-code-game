#!/usr/bin/env python
"""s55: SKALMAN-SIDE damage-into-enemy-core by channel, 65 first-contact games.

The #119 withdrawal's residual (b): the decode's channel split covers damage INTO
us; this measures OUR damage OUT, plus builder core-adjacency (parked rounds) vs
melee count -- the design-relevant "parked without pecking" cell.

Method mirrors the decode agent's ledger: per game, enemy core HP deltas are the
truth; attribution = BATK by our builder onto the enemy core footprint (x2 dmg)
+ FIRE from a tile holding OUR gunner (x7) / sentinel (x18) whose target is in
the footprint. Known cell: d18b7d7b_g5 must read builder 446 / sentinel 54.
Mutation control: --mutate (builder dmg 2->3) must BREAK the ledger match.
"""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from s54_klad_lib import Game, d2

MUTATE = "--mutate" in sys.argv
B_DMG = 3 if MUTATE else 2

ARCH = Path("replay_archive")
MATCHES = ["4bc7ed13","e46e55fd","0e5b63ea","5ee3afec",       # mirror
           "ab068a0d","e200bcab","919000f0","64a8beb6",       # pivot
           "82a03bfd","b6ec7f91","d18b7d7b","0de59936","abd8f4fc"]  # kladde
CELL = {m:("MIRROR" if i<4 else "PIVOT" if i<8 else "KLADDE")
        for i,m in enumerate(MATCHES)}

# our seat per file, from the corpus
seat = {}
for r in csv.DictReader(open("corpus/unrated_games.tsv"), delimiter="\t"):
    seat[r["file"]] = r["our_team"]

def footprint_tiles(g, team):
    return set((p.x, p.y) if hasattr(p, "x") else tuple(p) for p in g.footprint(team))

rows = []
for m in MATCHES:
    for f in sorted(ARCH.glob(m + "*_game_*.replay26")):
        us = seat.get(f.name)
        if us is None:
            print("NO SEAT:", f.name); continue
        us_i = 0 if us == "A" else 1
        them_i = 1 - us_i
        g = Game(f)
        their_core_id = g.core_id(them_i)
        fp = footprint_tiles(g, them_i)
        # static turret registry: id -> (team,kind); position at build
        turret_at = {}     # (x,y) -> (team, kind) latest occupant
        builder_team = {}  # builder id -> team
        dmg_hp = 0         # true: negative HP deltas on their core
        by = {"builder":0, "gunner":0, "sentinel":0}
        batk_core = 0
        adj_rounds = 0     # our-builder-rounds adjacent to their core
        # replay positions: track builder pos via BUILD/MOVE
        bpos = {}
        for rnd, kind, pl in g.ev:
            if kind == "BUILD":
                eid, team, ek, pos = pl
                if ek in ("gunner", "sentinel"):
                    turret_at[(pos.x, pos.y) if hasattr(pos,"x") else tuple(pos)] = (team, ek)
                if ek == "builder_bot":
                    builder_team[eid] = team
                    bpos[eid] = (pos.x, pos.y) if hasattr(pos,"x") else tuple(pos)
            elif kind == "MOVE":
                eid, frm, to = pl
                if eid in builder_team:
                    bpos[eid] = (to.x, to.y) if hasattr(to,"x") else tuple(to)
            elif kind == "HP":
                eid, delta = pl
                if eid == their_core_id and delta < 0:
                    dmg_hp += -delta
            elif kind == "BATK":
                eid, t = pl
                if t is None: continue
                txy = (t.x, t.y) if hasattr(t,"x") else tuple(t)
                if builder_team.get(eid) == us_i and txy in fp:
                    by["builder"] += B_DMG
                    batk_core += 1
            elif kind == "FIRE":
                frm, to = pl
                if frm is None or to is None: continue
                fxy = (frm.x, frm.y) if hasattr(frm,"x") else tuple(frm)
                txy = (to.x, to.y) if hasattr(to,"x") else tuple(to)
                if txy in fp:
                    tk = turret_at.get(fxy)
                    if tk and tk[0] == us_i:
                        by[tk[1]] += 7 if tk[1] == "gunner" else 18
        # adjacency: count per round after events settle is heavy; approximate by
        # sampling builder positions per round via MOVE stream -> per-round set
        # (re-walk events cheaply)
        cur = {}
        rnd_seen = -1
        for rnd, kind, pl in g.ev:
            if rnd != rnd_seen and rnd_seen >= 0:
                for eid, xy in cur.items():
                    if builder_team.get(eid) == us_i and any(
                            abs(xy[0]-c[0]) + abs(xy[1]-c[1]) == 1 for c in fp):
                        adj_rounds += 1
            rnd_seen = rnd
            if kind == "BUILD" and pl[2] == "builder_bot":
                cur[pl[0]] = (pl[3].x, pl[3].y) if hasattr(pl[3],"x") else tuple(pl[3])
            elif kind == "MOVE" and pl[0] in cur:
                cur[pl[0]] = (pl[2].x, pl[2].y) if hasattr(pl[2],"x") else tuple(pl[2])
            elif kind == "DEATH" and pl[0] in cur:
                del cur[pl[0]]
        attributed = sum(by.values())
        rows.append((CELL[m], f.name, dmg_hp, attributed, by["builder"], by["gunner"],
                     by["sentinel"], batk_core, adj_rounds))

print(f"{'cell':7} {'game':44} {'trueHP':>6} {'attr':>5} {'bldr':>5} {'gun':>4} {'sent':>5} {'batk':>4} {'adjR':>5}")
mis = 0
for r in rows:
    flag = "" if r[2] == r[3] else "  <-- MISMATCH"
    if r[2] != r[3]: mis += 1
    print(f"{r[0]:7} {r[1]:44} {r[2]:6d} {r[3]:5d} {r[4]:5d} {r[5]:4d} {r[6]:5d} {r[7]:4d} {r[8]:5d}{flag}")
print(f"\nmismatches: {mis}/{len(rows)}  (MUTATE={MUTATE})")
tot_b = sum(r[4] for r in rows); tot_g = sum(r[5] for r in rows); tot_s = sum(r[6] for r in rows)
tot = tot_b + tot_g + tot_s
if tot:
    print(f"OUR damage into their cores, all games: builder {tot_b} ({100*tot_b/tot:.1f}%) "
          f"gunner {tot_g} ({100*tot_g/tot:.1f}%) sentinel {tot_s} ({100*tot_s/tot:.1f}%)")
print(f"our-builder adjacency rounds total: {sum(r[8] for r in rows)}; "
      f"core melee attacks total: {sum(r[7] for r in rows)}")
kc = [r for r in rows if r[0]=="KLADDE" and "d18b7d7b" in r[1] and "game_5" in r[1]]
if kc:
    r = kc[0]
    print(f"KNOWN CELL d18b7d7b_g5: builder {r[4]} (expect 446), sentinel {r[6]} (expect 54)")
