#!/usr/bin/env python3
"""Rebuild the CORRECTED nest label from corpus/events.tsv only.

seed  = enemy gunner/sentinel BUILD with d2 to OUR core <= 32,
        no enemy turret alive within d2<=8 of the seed tile at plant time,
        and >= 30 rounds of game remaining.
nest  = a further enemy turret BUILD on a DISTINCT tile within d2<=8 of the
        seed tile, in rounds (rnd, rnd+30], while the seed is still alive.

Lifetimes come from FIFO BUILD->DEATH pairing on (file, team, kind, x, y),
which is sound for buildings (they cannot co-occupy a tile).
Outputs seeds.tsv + per-game game.tsv.
"""
import csv, collections, sys

B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"
S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")

J = {r["file"]: r for r in csv.DictReader(open(B + "join.tsv"), delimiter="\t")}
print(f"join.tsv rows: {len(J)}", file=sys.stderr)

# ---- pass 1: bucket every event of an attributed file by file -------------
ev = collections.defaultdict(list)
nrows = 0
for r in csv.DictReader(open(B + "events.tsv"), delimiter="\t"):
    nrows += 1
    if r["file"] not in J:
        continue
    ev[r["file"]].append((int(r["rnd"]), r["ev"], int(r["team"]), r["kind"],
                          int(r["x"]), int(r["y"]), int(r["d2_own"]),
                          int(r["d2_enemy"])))
print(f"events.tsv rows: {nrows}; attributed files with events: {len(ev)}",
      file=sys.stderr)

TUR = ("gunner", "sentinel")
seeds, games = [], []
n_plants = 0
for f, rows in ev.items():
    j = J[f]
    ours = int(j["our_team"])
    them = 1 - ours
    rows.sort(key=lambda t: (t[0], t[1]))  # BUILD before DEATH within a round
    lastrnd = max(t[0] for t in rows)

    # --- lifetimes for enemy turrets, FIFO per tile ------------------------
    pend = collections.defaultdict(collections.deque)
    life = []            # (rnd_build, rnd_death|None, kind, x, y) enemy turrets
    for rnd, e, tm, kind, x, y, d2o, d2e in rows:
        if tm != them or kind not in TUR:
            continue
        key = (kind, x, y)
        if e == "BUILD":
            life.append([rnd, None, kind, x, y])
            pend[key].append(len(life) - 1)
        else:
            if pend[key]:
                life[pend[key].popleft()][1] = rnd
    # index enemy turret builds by round for the window scan
    tb = [(l[0], l[3], l[4]) for l in life]

    # --- our own book-keeping for the harm metrics -------------------------
    ourbb_build = ourbb_death = 0
    bb_delta = collections.Counter()
    home_bb_deaths = 0
    for rnd, e, tm, kind, x, y, d2o, d2e in rows:
        if kind != "builder_bot" or tm != ours:
            continue
        if e == "BUILD":
            ourbb_build += 1
            bb_delta[rnd] += 1
        else:
            ourbb_death += 1
            bb_delta[rnd] -= 1
            if d2o <= 32:
                home_bb_deaths += 1
    alive, bbrounds = 0, 0
    for r in range(0, lastrnd + 1):
        alive += bb_delta.get(r, 0)
        bbrounds += alive

    # --- seeds --------------------------------------------------------------
    g_seeds = g_nests = g_plants = 0
    for i, (rb, rd, kind, x, y) in enumerate(life):
        # in-band?  d2_enemy of an enemy build is distance to OUR core
        pass
    for rnd, e, tm, kind, x, y, d2o, d2e in rows:
        if e != "BUILD" or tm != them or kind not in TUR or d2e > 32:
            continue
        n_plants += 1
        g_plants += 1
        if lastrnd - rnd < 30:
            continue
        # pre-existing enemy turret alive within d2<=8 of this tile (other tile
        # or same tile) at plant time?
        pre = 0
        for lb, ld, lk, lx, ly in life:
            if lb >= rnd:
                continue
            if ld is not None and ld <= rnd:
                continue
            if (lx - x) ** 2 + (ly - y) ** 2 <= 8:
                pre += 1
        if pre:
            continue
        # this seed's own death round (FIFO: first lifetime at this tile with
        # build round == rnd)
        mydeath = None
        for lb, ld, lk, lx, ly in life:
            if lb == rnd and lx == x and ly == y and lk == kind:
                mydeath = ld
                break
        nest = 0
        fastest = None
        for lb, lk, lx, ly in [(l[0], l[2], l[3], l[4]) for l in life]:
            if not (rnd < lb <= rnd + 30):
                continue
            if lx == x and ly == y:
                continue                      # same-tile rebuild is NOT a nest
            if (lx - x) ** 2 + (ly - y) ** 2 > 8:
                continue
            if mydeath is not None and mydeath <= lb:
                continue                      # seed already dead: no coexistence
            nest += 1
            if fastest is None or lb - rnd < fastest:
                fastest = lb - rnd
        g_seeds += 1
        g_nests += 1 if nest else 0
        seeds.append(dict(file=f, opp=j["opp"], oppver=j["oppver"],
                          ourver=j["ourver"], map=j["map"], seat=ours,
                          match=j["match"], won=j["won"], rnd=rnd, kind=kind,
                          x=x, y=y, d2=d2e, nest=1 if nest else 0,
                          lag=fastest if fastest is not None else -1,
                          lastrnd=lastrnd))
    games.append(dict(file=f, match=j["match"], opp=j["opp"],
                      oppver=j["oppver"], ourver=j["ourver"], map=j["map"],
                      seat=ours, won=j["won"], turns=j["turns"],
                      lastrnd=lastrnd, plants=g_plants, seeds=g_seeds,
                      nests=g_nests, our_bb_built=ourbb_build,
                      our_bb_died=ourbb_death, home_bb_deaths=home_bb_deaths,
                      bb_rounds=bbrounds))

with open(S + "seeds.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(seeds[0]), delimiter="\t")
    w.writeheader(); w.writerows(seeds)
with open(S + "games.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(games[0]), delimiter="\t")
    w.writeheader(); w.writerows(games)

nn = sum(s["nest"] for s in seeds)
print(f"in-band enemy plants: {n_plants}")
print(f"seeds (pre_t8==0, >=30 rounds left): {len(seeds)}")
print(f"nests (distinct tile, <=30 rounds, seed alive): {nn} "
      f"= {nn/len(seeds):.1%}")
print(f"games: {len(games)}")
