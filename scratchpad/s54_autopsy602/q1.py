#!/usr/bin/env python3
"""Q1 aggregation: what blocks the full seal."""
import json, statistics as st
from pathlib import Path
SP = Path(__file__).parent
D = json.loads((SP / "tape602_raw.json").read_text())

def won(r):
    return r["winner"] == r["side"] and r["cond"] == "core_destroyed"

def lost_core(r):
    return r["core_dead"][str(r["side"])] is not None

rows = []
for n, r in sorted(D.items()):
    side = r["side"]
    seal = r["seal"]
    op = len(r["seal_open"])
    nwall = 8 - op
    ever = [t for t, s in seal.items() if s["our_builds"]]
    never = [t for t, s in seal.items() if not s["our_builds"]]
    lost = sum(len(s["our_losses"]) for s in seal.values())
    builds = sum(len(s["our_builds"]) for s in seal.values())
    kill_r = r["core_dead"][str(1 - side)]
    held_at_kill = r["held_series"][kill_r] if kill_r is not None else None
    # held one round BEFORE the kill (the cage state that produced it)
    held_pre = r["held_series"][kill_r - 1] if kill_r else None
    rows.append(dict(game=n, side=side, rounds=r["rounds"], win=won(r),
                     cond=r["cond"], winner=r["winner"],
                     our_core_dead=r["core_dead"][str(side)],
                     kill_r=kill_r, open=op, walls=nwall,
                     max_held=r["max_held"], ever=len(ever), never=len(never),
                     builds=builds, lost=lost,
                     held_at_kill=held_at_kill, held_pre=held_pre,
                     ti=r["ti_collected"][str(side)] if str(side) in r["ti_collected"] else r["ti_collected"][side]))

print("=== PER-GAME SEAL TABLE ===")
print(f"{'game':22}{'sd':>3}{'rnds':>6}{'res':>6}{'open':>5}{'wall':>5}"
      f"{'maxheld':>8}{'ever':>5}{'never':>6}{'blds':>5}{'lost':>5}{'@kill':>6}")
for x in rows:
    res = "WIN" if x["win"] else ("r1000" if x["rounds"] >= 1000 else "loss")
    print(f"{x['game'].replace('.replay26',''):22}{x['side']:>3}{x['rounds']:>6}{res:>6}"
          f"{x['open']:>5}{x['walls']:>5}{x['max_held']:>8}{x['ever']:>5}"
          f"{x['never']:>6}{x['builds']:>5}{x['lost']:>5}"
          f"{'-' if x['held_at_kill'] is None else x['held_at_kill']:>6}")

wins = [x for x in rows if x["win"]]
loss = [x for x in rows if not x["win"]]
print()
print("n games", len(rows), " wins", len(wins))
print("max_held median all", st.median([x["max_held"] for x in rows]),
      " wins", st.median([x["max_held"] for x in wins]),
      " losses", st.median([x["max_held"] for x in loss]))
print("open median", st.median([x["open"] for x in rows]))
print("ever-built median", st.median([x["ever"] for x in rows]),
      "of open median", st.median([x["open"] for x in rows]))
print("never-attempted median", st.median([x["never"] for x in rows]))
print("total ring builds", sum(x["builds"] for x in rows),
      "total ring losses", sum(x["lost"] for x in rows))
print("games reaching max_held == open:",
      sum(1 for x in rows if x["max_held"] == x["open"]), "/", len(rows))
print("games reaching max_held >= 7:", sum(1 for x in rows if x["max_held"] >= 7))
print()
print("WIN games cage-at-kill:")
for x in wins:
    print(f"  {x['game'].replace('.replay26',''):22} kill r{x['kill_r']:<5} "
          f"held_at_kill={x['held_at_kill']} held_prev={x['held_pre']} "
          f"max_held={x['max_held']} open={x['open']} ever={x['ever']}")

# ---- decomposition of the gap: open - max_held
print()
print("=== BLOCKER DECOMPOSITION (per game: open tiles minus max simultaneous held) ===")
tot = {"never_enemybld": 0, "never_empty": 0, "never_other": 0,
       "ever_lost_at_peak": 0, "n_gap": 0}
detail = []
for n, r in sorted(D.items()):
    seal = r["seal"]
    op = len(r["seal_open"])
    gap = op - r["max_held"]
    cats = {"never_enemybld": 0, "never_empty": 0, "never_ourother": 0,
            "ever": 0}
    for t, s in seal.items():
        if s["our_builds"]:
            cats["ever"] += 1
        elif s["enemy_bld_rounds"] > 0:
            cats["never_enemybld"] += 1
        elif s["our_other_bld_rounds"] > 0:
            cats["never_ourother"] += 1
        else:
            cats["never_empty"] += 1
    detail.append((n, op, r["max_held"], gap, cats))
    tot["n_gap"] += gap
for n, op, mh, gap, c in detail:
    print(f"{n.replace('.replay26',''):22} open={op} maxheld={mh} gap={gap} "
          f"ever={c['ever']} neverEnemyBld={c['never_enemybld']} "
          f"neverEmpty={c['never_empty']} neverOurOther={c['never_ourother']}")

print()
print("=== NEVER-ATTEMPTED TILES: what occupied them (tile-rounds, pooled) ===")
occ = {"enemy_bld": 0, "enemy_body": 0, "our_bld": 0, "empty": 0}
kinds = {}
nev_tiles = 0
nev_with_evict = 0
nev_walker_adj = 0
for n, r in sorted(D.items()):
    for t, s in r["seal"].items():
        if s["our_builds"]:
            continue
        nev_tiles += 1
        occ["enemy_bld"] += s["enemy_bld_rounds"]
        occ["our_bld"] += s["our_other_bld_rounds"]
        occ["empty"] += s["empty_rounds"]
        occ["enemy_body"] += s["enemy_body_rounds"]
        for k, v in s["enemy_bld_kinds"].items():
            kinds[k] = kinds.get(k, 0) + v
        if s["our_attacks"]:
            nev_with_evict += 1
        if s["walker_adj_rounds"] or s["walker_on_rounds"]:
            nev_walker_adj += 1
tr = sum(occ.values()) - occ["enemy_body"]
print("never-attempted tiles:", nev_tiles)
for k in ("empty", "enemy_bld", "our_bld"):
    print(f"  {k:12} {occ[k]:8} tile-rounds  {100.0*occ[k]/max(tr,1):5.1f}%")
print(f"  (enemy BODY standing on tile: {occ['enemy_body']} tile-rounds)")
print("  enemy building kinds on never-attempted seal tiles:", kinds)
print(f"  never-attempted tiles our walker ever attacked (eviction engaged): "
      f"{nev_with_evict}/{nev_tiles}")
print(f"  never-attempted tiles our builder ever stood on/adjacent: "
      f"{nev_walker_adj}/{nev_tiles}")

print()
print("=== BUILT-THEN-LOST: killer table ===")
kt = {}
relay = []
nolose = 0
for n, r in sorted(D.items()):
    for t, s in r["seal"].items():
        for L in s["our_losses"]:
            k = (L["killer_kind"], L["killer_team"])
            kt[k] = kt.get(k, 0) + 1
        # relay latency: for each loss, next build on the same tile
        bl = sorted([b[0] for b in s["our_builds"]])
        for L in s["our_losses"]:
            nxt = [b for b in bl if b > L["rnd"]]
            if nxt:
                relay.append(nxt[0] - L["rnd"])
            else:
                nolose += 1
tot_lost = sum(kt.values())
for k, v in sorted(kt.items(), key=lambda z: -z[1]):
    kk = "OUR OWN destroy()" if k[0] is None else f"{k[0]} (team {k[1]})"
    print(f"  {kk:34} {v:5}  {100.0*v/max(tot_lost,1):5.1f}%")
print("  total ring losses", tot_lost)
if relay:
    print(f"  re-lay latency (rounds, n={len(relay)}): median {st.median(relay)} "
          f"mean {sum(relay)/len(relay):.2f} min {min(relay)} max {max(relay)} "
          f"<=2 rounds: {sum(1 for x in relay if x<=2)}/{len(relay)}")
print(f"  losses never re-laid: {nolose}/{tot_lost}")

print()
print("=== HELD-SERIES SHAPE ===")
for n, r in sorted(D.items()):
    hs = r["held_series"]
    op = len(r["seal_open"])
    # last 100 rounds mean
    tail = hs[-100:] if len(hs) > 100 else hs
    print(f"{n.replace('.replay26',''):22} open={op} max={max(hs)} "
          f"mean_last100={sum(tail)/len(tail):.2f} "
          f"rounds_at_max={sum(1 for x in hs if x==max(hs))} "
          f"rounds_held>=open-1={sum(1 for x in hs if x>=op-1)}")
