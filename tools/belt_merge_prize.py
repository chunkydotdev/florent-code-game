#!/usr/bin/env python3
"""QUEUE #78 mechanism (a): size the prize of TRUNK-MERGE belt routing.

THE DEFECT (code read, not re-derived here). `bots/_v223sealrepair/eco.py:391
_link_path` builds `raw_goals` from `core_tiles(self.core) x CARDINALS` and
NOTHING ELSE. Friendly conveyors/splitters are deliberately not obstacles, so a
route may pass THROUGH an existing belt, but a belt tile is never a
DESTINATION. Every harvester therefore routes its own shortest path to the core
ring; trunks are never joined on purpose.

THE PROPOSED FIX: seed `raw_goals` with our own live belt tiles as well as the
core ring, so a new line terminates at the nearest existing trunk.

WHAT THIS TOOL COMPUTES, and the design constraint that governs all of it:
**THE COUNTERFACTUAL MODELS THE PROPOSED FIX, NOT PERFECTION.** The fix is
GREEDY (nearest live acceptor at that moment), ORDER-CONSTRAINED and ONLINE
(harvesters are replayed in their real build order; the planner cannot see
future harvesters). Three arms are simulated on the REAL map geometry:

  BASE   goals = core ring                      (what we ship today)
  MERGE  goals = core ring + live belt tiles    (mechanism (a))
  PRIM   offline Prim-style Steiner heuristic, sees every harvester at once
         and is order-free.  Reported ONLY as an indicative bound, never as
         the estimate -- our planner is neither offline nor order-free.

Conveyor accounting is identical in every arm: a planned path tile that
already carries one of our conveyors is NOT rebuilt (this is what
`_build_next_link` does -- it pops occupied tiles), so
`new = |path \\ laid|` and then `laid |= path`.

BLOCKED SET, faithful to the map_grid branch of `_link_path`:
  walls, ore tiles (except the harvester's own tile), the 4 core tiles, and
  our own live non-belt buildings. Friendly belt is traversable. `_pave_ban`
  is None in the shipped tree (`HS_SEAT_BAN_CONVEYORS = False`).

CONTROLS (all run by --controls, and the tool refuses to publish without them):
  C1 GEOMETRY   every BUILD row's recomputed d2 to the map-file core anchor
                must equal the corpus `d2_own`; every harvester must land on
                an ORE tile of the map file.  Catches a wrong map name or a
                team-index slip, loudly.
  C2 SINGLE-H   games with exactly ONE harvester MUST show zero saving by
                construction.  A model that "saves" there is broken.
  C3 HAND CASE  a synthetic 2-harvester grid with no possible merge must
                return the identical path in BASE and MERGE.
  C4 TIE-BREAK  re-run with shuffled goal order; the spread bounds how much
                of the delta is BFS tie-breaking rather than topology.

Usage:
  .venv/bin/python tools/belt_merge_prize.py --versions 140 --controls
  .venv/bin/python tools/belt_merge_prize.py --versions 140 --json out.json
"""
from __future__ import annotations

import sys

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__))
        raise SystemExit(0)

import argparse
import collections
import csv
import json
import random
import statistics
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26  # noqa: E402

CARDINALS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # N, E, S, W -- eco.py order

# additive cost-scale contributions, CLAUDE.md (engine-confirmed, bots/_probe_scale)
SCALE_ADD = {
    "conveyor": 0.01, "splitter": 0.01, "barrier": 0.01,
    "harvester": 0.05, "launcher": 0.10,
    "builder_bot": 0.20, "gunner": 0.20, "sentinel": 0.20,
}
BASE_COST = {
    "conveyor": 3, "splitter": 6, "barrier": 3, "harvester": 20,
    "launcher": 20, "builder_bot": 30, "gunner": 20, "sentinel": 30,
}


# ---------------------------------------------------------------- geometry --
def core_tiles(o):
    x, y = o
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def ring_goals(o, w, h):
    ct = set(core_tiles(o))
    out = set()
    for cx, cy in ct:
        for dx, dy in CARDINALS:
            t = (cx + dx, cy + dy)
            if 0 <= t[0] < w and 0 <= t[1] < h and t not in ct:
                out.add(t)
    return out


def bfs_path(start, goals, blocked, w, h, order=None):
    """Faithful to `_link_path`'s map_grid branch: BFS OUT FROM THE GOALS,
    stop when `start` is reached, then walk the parent chain back.

    Returns the tile list from the first step after `start` through the goal
    tile inclusive -- i.e. exactly the tiles that need a conveyor. [] if
    unreachable or if `start` is itself a goal.
    """
    if start in goals or not goals:
        return []
    g = [t for t in goals if t not in blocked]
    if not g:
        return []
    g = sorted(g) if order is None else order(g)
    parent = {t: None for t in g}
    q = deque(g)
    while q and start not in parent:
        x, y = q.popleft()
        for dx, dy in CARDINALS:
            n = (x + dx, y + dy)
            if n in parent or n in blocked or not (0 <= n[0] < w and 0 <= n[1] < h):
                continue
            parent[n] = (x, y)
            q.append(n)
    if start not in parent:
        return []
    path, cur = [], start
    while parent[cur] is not None:
        cur = parent[cur]
        path.append(cur)
    return path


# ------------------------------------------------------------- simulation --
def simulate(game, arm, order=None):
    """game: dict(w,h,core,walls,ores,harvesters=[(rnd,pos)],statics=[(rnd,pos)])

    arm: 'base' (core ring only) or 'merge' (core ring + live belt).
    Returns (n_conveyors_laid, per_harvester=[(rnd, laid_this_line)]).
    """
    w, h, o = game["w"], game["h"], game["core"]
    ring = ring_goals(o, w, h)
    ct = set(core_tiles(o))
    laid = set()
    out = []
    load = collections.Counter()   # harvester lines routed through each tile
    seats = set()                  # distinct terminal tiles (core-ring entries)
    route = {}                     # tile -> route home, for flow accounting
    statics = sorted(game["statics"])           # (rnd, pos) non-belt buildings
    si = 0
    live_static = set()
    total = 0
    for rnd, hp in game["harvesters"]:
        while si < len(statics) and statics[si][0] <= rnd:
            live_static.add(statics[si][1])
            si += 1
        blocked = set(game["walls"])
        blocked |= {t for t in game["ores"] if t != hp}
        blocked |= ct
        blocked |= {t for t in live_static if t != hp}
        goals = set(ring) if arm == "base" else (set(ring) | laid)
        path = bfs_path(hp, goals, blocked, w, h, order=order)
        new = [t for t in path if t not in laid]
        # FLOW, not the planned path: `_build_next_link` pops tiles that already
        # carry a conveyor WITHOUT reorienting them, so a stack entering an
        # existing belt tile follows THAT tile's route home, not the rest of the
        # plan. This is why BASE already merges incidentally.
        j = next((i for i, t in enumerate(path) if t in laid), None)
        if j is None:
            flow = list(path)
        else:
            flow = list(path[:j]) + list(route.get(path[j], (path[j],)))
        for i in range(len(flow)):
            route.setdefault(flow[i], tuple(flow[i:]))
        laid.update(path)
        total += len(new)
        out.append((rnd, len(new)))
        for t in flow:
            load[t] += 1
        if flow:
            seats.add(flow[-1])
    return total, out, laid, load, seats


def simulate_prim(game):
    """Offline Prim-style Steiner heuristic: repeatedly attach the harvester
    whose shortest route to the CURRENT tree is cheapest. Order-free, sees
    every harvester. INDICATIVE BOUND ONLY -- not the Steiner optimum, and our
    planner is neither offline nor order-free."""
    w, h, o = game["w"], game["h"], game["core"]
    ring = ring_goals(o, w, h)
    ct = set(core_tiles(o))
    # deliberately the MOST GENEROUS blocked set (walls/core/ore only): this arm
    # is a bound, so it must not be handicapped by obstacles the online arms face.
    blocked_base = set(game["walls"]) | ct
    ores = set(game["ores"])
    laid = set()
    todo = [hp for _r, hp in game["harvesters"]]
    total = 0
    while todo:
        best = None
        for hp in todo:
            blocked = (blocked_base | (ores - {hp})) - {hp} - laid
            goals = set(ring) | laid
            path = bfs_path(hp, goals, blocked, w, h)
            cost = len([t for t in path if t not in laid]) if path else 10**6
            if best is None or cost < best[0]:
                best = (cost, hp, path)
        cost, hp, path = best
        todo.remove(hp)
        if cost >= 10**6:
            continue
        laid.update(path)
        total += cost
    return total


# ------------------------------------------------------------------ scale --
def scale_series(events, cutoffs):
    """events: [(rnd, 'BUILD'|'DEATH', kind)] for OUR team, in file order.
    Returns {cutoff: scale_multiplier} using the additive rule (destruction
    removes the contribution)."""
    add = 1.0
    out = {}
    idx = 0
    cuts = sorted(cutoffs)
    for rnd, ev, kind in events:
        while idx < len(cuts) and rnd > cuts[idx]:
            out[cuts[idx]] = add
            idx += 1
        c = SCALE_ADD.get(kind, 0.0)
        add += c if ev == "BUILD" else -c
    while idx < len(cuts):
        out[cuts[idx]] = add
        idx += 1
    return out


# ------------------------------------------------------------------- load --
def load_maps():
    maps = {}
    for p in sorted((ROOT / "maps").glob("*.map26")):
        w, h, rows, cores = parse_map26(p)
        walls = {(x, y) for y in range(h) for x in range(w) if rows[y][x] == 1}
        ores = {(x, y) for y in range(h) for x in range(w) if rows[y][x] == 2}
        anchors = {t: (x, y) for t, x, y in cores}
        maps[p.stem] = dict(w=w, h=h, walls=walls, ores=ores, anchors=anchors)
    return maps


def load_population(versions):
    pop = {}
    with open(ROOT / "corpus/join.tsv") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["ourver"] in versions:
                pop[r["file"]] = r
    return pop


def load_events(pop):
    ours = collections.defaultdict(list)
    theirs_conv = collections.Counter()
    with open(ROOT / "corpus/events.tsv") as fh:
        fh.readline()
        for line in fh:
            p = line.rstrip("\n").split("\t")
            r = pop.get(p[0])
            if r is None:
                continue
            if p[3] != r["our_team"]:
                if p[1] == "BUILD" and p[4] == "conveyor":
                    theirs_conv[p[0]] += 1
                continue
            ours[p[0]].append((int(p[2]), p[1], p[4], int(p[5]), int(p[6]), int(p[7])))
    return ours, theirs_conv


# ------------------------------------------------------------------ main ---
BELT = ("conveyor", "splitter")
STATIC = ("barrier", "gunner", "sentinel", "launcher", "harvester")


def build_game(fname, meta, evs, maps):
    m = maps.get(meta["map"])
    if m is None:
        return None, "no map file"
    team = int(meta["our_team"])
    anchor = m["anchors"].get(team)
    if anchor is None:
        return None, "no core anchor"
    # C1 GEOMETRY control -----------------------------------------------
    bad = 0
    for rnd, ev, kind, x, y, d2own in evs:
        if (x - anchor[0]) ** 2 + (y - anchor[1]) ** 2 != d2own:
            bad += 1
    if bad:
        return None, f"C1 d2_own mismatch {bad}/{len(evs)}"
    hbad = sum(1 for rnd, ev, kind, x, y, _ in evs
               if ev == "BUILD" and kind == "harvester" and (x, y) not in m["ores"])
    if hbad:
        return None, f"C1 harvester off ore {hbad}"
    harvesters = [(rnd, (x, y)) for rnd, ev, kind, x, y, _ in evs
                  if ev == "BUILD" and kind == "harvester"]
    statics = [(rnd, (x, y)) for rnd, ev, kind, x, y, _ in evs
               if ev == "BUILD" and kind in STATIC]
    game = dict(w=m["w"], h=m["h"], core=anchor, walls=m["walls"], ores=m["ores"],
                harvesters=harvesters, statics=statics,
                statics_all={p for _r, p in statics})
    return game, None


def main(argv=None):
    ap = argparse.ArgumentParser(description="size the QUEUE #78 trunk-merge prize")
    ap.add_argument("--versions", default="140",
                    help="comma-separated ourver values (join.tsv), default 140")
    ap.add_argument("--controls", action="store_true", help="run C2/C3/C4")
    ap.add_argument("--json", default=None)
    ap.add_argument("--cutoffs", default="150,250")
    a = ap.parse_args(argv)
    versions = set(a.versions.split(","))
    cutoffs = [int(x) for x in a.cutoffs.split(",")]

    maps = load_maps()
    pop = load_population(versions)
    ours, theirs = load_events(pop)
    print(f"POPULATION RULE: corpus/join.tsv rows (ladder games, our-seat known) "
          f"with ourver in {sorted(versions)} -> {len(pop)} games; "
          f"{len(ours)} have BUILD/DEATH rows in corpus/events.tsv")

    rows, drops = [], collections.Counter()
    for f, meta in sorted(pop.items()):
        evs = ours.get(f)
        if not evs:
            drops["no events"] += 1
            continue
        game, err = build_game(f, meta, evs, maps)
        if game is None:
            drops[err.split()[0] + " " + err.split()[1] if " " in err else err] += 1
            continue
        obs_conv = sum(1 for r, ev, k, *_ in evs if ev == "BUILD" and k in BELT)
        obs_tiles = {(x, y) for r, ev, k, x, y, _ in evs if ev == "BUILD" and k in BELT}
        base, base_per, base_tiles, bload, bseats = simulate(game, "base")
        merge, merge_per, _mt, mload, mseats = simulate(game, "merge")
        prim = simulate_prim(game)
        hit = len(obs_tiles & base_tiles)
        sc = scale_series([(r, ev, k) for r, ev, k, *_ in evs], cutoffs)
        saved_by = {}
        for c in cutoffs:
            b = sum(n for r, n in base_per if r <= c)
            g = sum(n for r, n in merge_per if r <= c)
            saved_by[c] = b - g
        # titanium freed by the cheaper scale, over every build AFTER each cutoff
        freed = {}
        for c in cutoffs:
            d = 0.01 * saved_by[c]
            s = sc[c]
            tot = 0.0
            for r, ev, k, *_ in evs:
                if ev != "BUILD" or r < c or k not in BASE_COST:
                    continue
                tot += int(s * BASE_COST[k]) - int(max(1.0, s - d) * BASE_COST[k])
            # plus the conveyors never built, at the price they would have cost
            tot += saved_by[c] * int(s * BASE_COST["conveyor"])
            freed[c] = tot
        rows.append(dict(
            file=f, map=meta["map"], w=game["w"], h=game["h"], turns=int(meta["turns"]),
            nh=len(game["harvesters"]), obs=obs_conv, obs_tiles=len(obs_tiles),
            base=base, merge=merge, prim=prim, hit=hit, base_tiles=len(base_tiles),
            bmaxload=max(bload.values()) if bload else 0,
            mmaxload=max(mload.values()) if mload else 0,
            bseats=len(bseats), mseats=len(mseats),
            scale={c: sc[c] for c in cutoffs},
            saved={c: saved_by[c] for c in cutoffs},
            freed={c: freed[c] for c in cutoffs},
            theirs=theirs.get(f, 0)))
    print(f"USABLE: {len(rows)} games; drops: {dict(drops)}")
    if not rows:
        return 1

    def mean(xs):
        return sum(xs) / len(xs)

    n = len(rows)
    print("\n--- CURRENT STATE (our team) ---")
    print(f"observed conveyor+splitter builds/game: mean {mean([r['obs'] for r in rows]):.1f}"
          f"  median {statistics.median([r['obs'] for r in rows]):.0f}")
    print(f"harvesters/game:                        mean {mean([r['nh'] for r in rows]):.2f}")
    tn = [r["turns"] for r in rows]
    print(f"game length (turns): mean {mean(tn):.0f} median {statistics.median(tn):.0f}; "
          f"alive at r150 {sum(1 for t in tn if t>=150)}/{n}, at r250 {sum(1 for t in tn if t>=250)}/{n}")
    for c in cutoffs:
        s = [r["scale"][c] for r in rows]
        print(f"modelled scale at r{c}: mean {mean(s)*100:.1f}%  median {statistics.median(s)*100:.1f}%"
              f"  (n={len(s)})")

    print("\n--- MODEL vs OBSERVED (validation of the BASE arm) ---")
    print(f"BASE modelled conveyors/game: {mean([r['base'] for r in rows]):.1f}"
          f"   observed builds: {mean([r['obs'] for r in rows]):.1f}"
          f"   observed DISTINCT tiles: {mean([r['obs_tiles'] for r in rows]):.1f}"
          f"   ratio(model/distinct) {mean([r['base'] for r in rows])/mean([r['obs_tiles'] for r in rows]):.2f}")
    tp = sum(r["hit"] for r in rows)
    print(f"TILE-SET AGREEMENT: {tp}/{sum(r['obs_tiles'] for r in rows)} observed belt tiles "
          f"({tp/sum(r['obs_tiles'] for r in rows)*100:.1f}%) are also predicted by the BASE model; "
          f"{tp}/{sum(r['base_tiles'] for r in rows)} "
          f"({tp/sum(r['base_tiles'] for r in rows)*100:.1f}%) of modelled tiles were really built")

    print("\n--- THE DELTA ---")
    sav = [r["base"] - r["merge"] for r in rows]
    prim_sav = [r["base"] - r["prim"] for r in rows]
    print(f"GREEDY MERGE saving/game: mean {mean(sav):.2f}  median {statistics.median(sav):.0f}"
          f"  max {max(sav)}  zero-in {sum(1 for x in sav if x == 0)}/{n}")
    print(f"  as share of BASE belt: {sum(sav)/sum(r['base'] for r in rows)*100:.1f}%")
    print(f"OFFLINE PRIM bound/game:  mean {mean(prim_sav):.2f}  (UPPER BOUND, not the estimate)")
    for c in cutoffs:
        s = [r["saved"][c] for r in rows]
        fr = [r["freed"][c] for r in rows]
        gs = [int(r["scale"][c] * 20) for r in rows]
        print(f"  by r{c}: conveyors saved mean {mean(s):.2f} -> scale -{mean(s)*1:.2f}pp;"
              f" Ti freed mean {mean(fr):.1f};"
              f" gunner price {mean(gs):.1f} Ti -> extra gunners {mean(fr)/max(1e-9, mean(gs)):.3f}")

    # size class split
    print("\n--- CONGESTION RISK (unmodelled cost of merging) ---")
    print("  a conveyor moves at most 1 stack/round; a harvester emits 1 stack/4 rounds,")
    print("  so a shared tile saturates once more than 4 harvester lines route through it.")
    bl = [r["bmaxload"] for r in rows]; ml = [r["mmaxload"] for r in rows]
    print(f"  busiest tile, lines through it: BASE mean {mean(bl):.2f} max {max(bl)}"
          f" | MERGE mean {mean(ml):.2f} max {max(ml)}")
    print(f"  games with a tile carrying >4 lines: BASE {sum(1 for x in bl if x>4)}/{n}"
          f" | MERGE {sum(1 for x in ml if x>4)}/{n}")
    print(f"  distinct terminal tiles: BASE mean {mean([r['bseats'] for r in rows]):.2f}"
          f" | MERGE mean {mean([r['mseats'] for r in rows]):.2f}")

    print("\n--- BY MAP SIZE CLASS (area = w*h) ---")
    for lo, hi, lab in ((0, 200, "small <200"), (200, 500, "mid 200-499"), (500, 10**9, "big >=500")):
        g = [r for r in rows if lo <= r["w"] * r["h"] < hi]
        if not g:
            continue
        print(f"  {lab:12s} n={len(g):3d}  obs {mean([r['obs'] for r in g]):5.1f}"
              f"  base {mean([r['base'] for r in g]):5.1f}"
              f"  saved {mean([r['base']-r['merge'] for r in g]):.2f}"
              f"  prim {mean([r['base']-r['prim'] for r in g]):.2f}")

    if a.controls:
        run_controls(rows, pop, ours, maps)
    if a.json:
        Path(a.json).write_text(json.dumps(
            [{k: (v if not isinstance(v, dict) else {str(kk): vv for kk, vv in v.items()})
              for k, v in r.items()} for r in rows], indent=1))
        print(f"\nwrote {a.json}")
    return 0


def run_controls(rows, pop, ours, maps):
    print("\n=== CONTROLS ===")
    one = [r for r in rows if r["nh"] == 1]
    bad = [r for r in one if r["base"] != r["merge"]]
    print(f"C2 SINGLE-HARVESTER: n={len(one)} games with exactly 1 harvester; "
          f"non-zero saving in {len(bad)}  -> {'PASS' if not bad else 'FAIL'}")
    two = [r for r in rows if r["nh"] == 2]
    print(f"   (n={len(two)} two-harvester games, mean saving "
          f"{sum(r['base']-r['merge'] for r in two)/max(1,len(two)):.2f})")

    # C3 hand case: two harvesters on opposite sides of the core, no shared route
    w = h = 11
    game = dict(w=w, h=h, core=(5, 5), walls=set(), ores={(1, 5), (9, 5)},
                harvesters=[(0, (1, 5)), (10, (9, 5))], statics=[], statics_all=set())
    b, bp, _, _, _ = simulate(game, "base")
    m, mp, _, _, _ = simulate(game, "merge")
    print(f"C3 HAND CASE (harvesters at (1,5) and (9,5), core (5,5), open 11x11): "
          f"BASE={b} MERGE={m} per-line base={[x[1] for x in bp]} merge={[x[1] for x in mp]}")
    print(f"   expected: no merge available (opposite sides) -> BASE == MERGE  "
          f"-> {'PASS' if b == m else 'FAIL'}")
    # and its mirror: two harvesters on the SAME side, merge MUST save
    game2 = dict(w=w, h=h, core=(5, 5), walls=set(), ores={(1, 5), (1, 6)},
                 harvesters=[(0, (1, 5)), (10, (1, 6))], statics=[], statics_all=set())
    b2, _, _, _, _ = simulate(game2, "base")
    m2, _, _, _, _ = simulate(game2, "merge")
    print(f"C3b MIRROR (two harvesters stacked at (1,5),(1,6)): BASE={b2} MERGE={m2} "
          f"-> {'PASS (merge saves)' if m2 < b2 else 'FAIL (instrument never finds a saving)'}")

    # C4 tie-break sensitivity
    print("C4 TIE-BREAK: re-running 60 games with shuffled goal order, 3 seeds")
    sub = rows[:60]
    files = {r["file"] for r in sub}
    tot = []
    for seed in (1, 2, 3):
        rng = random.Random(seed)

        def order(g, rng=rng):
            g = list(g)
            rng.shuffle(g)
            return g
        s = 0
        for f in sorted(files):
            meta = pop[f]
            game, err = build_game(f, meta, ours[f], maps)
            if game is None:
                continue
            b, *_x = simulate(game, "base", order=order)
            m, *_y = simulate(game, "merge", order=order)
            s += b - m
        tot.append(s / len(files))
    det = sum(r["base"] - r["merge"] for r in sub) / len(sub)
    print(f"   deterministic {det:.2f}/game vs shuffled {['%.2f' % x for x in tot]} "
          f"-> spread {max(tot)-min(tot):.2f}")


if __name__ == "__main__":
    raise SystemExit(main())
