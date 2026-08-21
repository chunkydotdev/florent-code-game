#!/usr/bin/env python3
"""Q2 aggregation: belt survival on tape602."""
import json, statistics as st
from pathlib import Path
SP = Path(__file__).parent
D = json.loads((SP / "tape602_raw.json").read_text())
BELTK = ("conveyor", "splitter")


def won(r): return r["winner"] == r["side"] and r["cond"] == "core_destroyed"


def cls(d):
    """Killer class by standing position relative to OUR core."""
    if d["killer_kind"] is None:
        return "no-damage (our own destroy)"
    if d.get("killer_dsq_ourcore") is None:
        return d["killer_kind"] + " (pos unknown)"
    dq = d["killer_dsq_ourcore"]
    if dq <= 13:
        band = "door d2<=13"
    elif dq <= 100:
        band = "ANNULUS d2 20-100"
    else:
        band = "far d2>100"
    return f"{d['killer_kind']} @ {band}"


print("=== 1. PER-GAME BELT LEDGER ===")
print(f"{'game':22}{'res':>6}{'harvB':>7}{'harvD':>7}{'harvAlive':>10}"
      f"{'beltB':>7}{'beltD':>7}{'stacks':>8}{'Ti':>7}")
rows = []
for n, r in sorted(D.items()):
    side = r["side"]
    hb = sum(1 for tl, lst in r["our_builds_by_tile"].items()
             for (rn, k, i) in lst if k == "harvester")
    hd = sum(len(v) for v in r["harv_deaths_by_tile"].values())
    bb = sum(1 for tl, lst in r["our_builds_by_tile"].items()
             for (rn, k, i) in lst if k in BELTK)
    bd = sum(len(v) for v in r["belt_deaths_by_tile"].values())
    ti = r["ti_collected"][str(side)] if str(side) in r["ti_collected"] else r["ti_collected"][side]
    stk = r["deliv_stacks"][str(side)] if str(side) in r["deliv_stacks"] else r["deliv_stacks"][side]
    res = "WIN" if won(r) else ("r1000" if r["rounds"] >= 1000 else "loss")
    rows.append(dict(g=n, res=res, hb=hb, hd=hd, bb=bb, bd=bd, ti=ti, stk=stk,
                     win=won(r), rounds=r["rounds"]))
    print(f"{n.replace('.replay26',''):22}{res:>6}{hb:>7}{hd:>7}{hb-hd:>10}"
          f"{bb:>7}{bd:>7}{stk:>8}{ti:>7}")
print()
print(f"POOLED n=30: harvesters built {sum(x['hb'] for x in rows)}, died "
      f"{sum(x['hd'] for x in rows)} ({100.0*sum(x['hd'] for x in rows)/max(sum(x['hb'] for x in rows),1):.1f}%), "
      f"alive at end {sum(x['hb']-x['hd'] for x in rows)}")
print(f"            belt pieces built {sum(x['bb'] for x in rows)}, died "
      f"{sum(x['bd'] for x in rows)} ({100.0*sum(x['bd'] for x in rows)/max(sum(x['bb'] for x in rows),1):.1f}%)")
print(f"harvester deaths/game: median {st.median([x['hd'] for x in rows])} "
      f"mean {sum(x['hd'] for x in rows)/30:.2f}")
print(f"belt deaths/game: median {st.median([x['bd'] for x in rows])} "
      f"mean {sum(x['bd'] for x in rows)/30:.2f}")
print(f"Ti delivered/game: median {st.median([x['ti'] for x in rows])} "
      f"mean {sum(x['ti'] for x in rows)/30:.1f}")
w = [x for x in rows if x["win"]]; l = [x for x in rows if not x["win"]]
print(f"  WINS n={len(w)}: median Ti {st.median([x['ti'] for x in w])}, "
      f"median harvD {st.median([x['hd'] for x in w])}, median beltD {st.median([x['bd'] for x in w])}")
print(f"  NON  n={len(l)}: median Ti {st.median([x['ti'] for x in l])}, "
      f"median harvD {st.median([x['hd'] for x in l])}, median beltD {st.median([x['bd'] for x in l])}")

print()
print("=== 2. KILLER TABLE (our harvesters) ===")
kt = {}; hd_all = []
for n, r in sorted(D.items()):
    for tl, lst in r["harv_deaths_by_tile"].items():
        for d in lst:
            kt[cls(d)] = kt.get(cls(d), 0) + 1
            hd_all.append(d)
tot = sum(kt.values())
for k, v in sorted(kt.items(), key=lambda z: -z[1]):
    print(f"  {k:34} {v:5}  {100.0*v/max(tot,1):5.1f}%")
print("  total harvester deaths", tot)
if hd_all:
    dd = [d["killer_dsq_ourcore"] for d in hd_all if d.get("killer_dsq_ourcore") is not None]
    print(f"  killer d^2 to OUR core: median {st.median(dd)} min {min(dd)} max {max(dd)} n={len(dd)}")
    print(f"  in annulus 20-100: {sum(1 for x in dd if 20 <= x <= 100)}/{len(dd)}")
    lf = [d["life"] for d in hd_all]
    print(f"  harvester lifetime (rounds): median {st.median(lf)} mean {sum(lf)/len(lf):.1f}")
    print(f"  covered by one of OUR live turret rays at death: "
          f"{sum(1 for d in hd_all if d['covered_at_death'])}/{len(hd_all)}")

print()
print("=== 3. KILLER TABLE (our conveyors/splitters) ===")
kt2 = {}; bd_all = []
for n, r in sorted(D.items()):
    for tl, lst in r["belt_deaths_by_tile"].items():
        for d in lst:
            kt2[cls(d)] = kt2.get(cls(d), 0) + 1
            bd_all.append(d)
tot2 = sum(kt2.values())
for k, v in sorted(kt2.items(), key=lambda z: -z[1]):
    print(f"  {k:34} {v:5}  {100.0*v/max(tot2,1):5.1f}%")
print("  total belt deaths", tot2)
if bd_all:
    dd = [d["killer_dsq_ourcore"] for d in bd_all if d.get("killer_dsq_ourcore") is not None]
    if dd:
        print(f"  killer d^2 to OUR core: median {st.median(dd)} min {min(dd)} max {max(dd)}")
        print(f"  in annulus 20-100: {sum(1 for x in dd if 20 <= x <= 100)}/{len(dd)}")
    vd = [d["dsq_ourcore"] for d in bd_all]
    print(f"  VICTIM d^2 to our core: median {st.median(vd)} "
          f"<=13 (inside trunk cut): {sum(1 for x in vd if x <= 13)}/{len(vd)}  "
          f">13 (TRUNK): {sum(1 for x in vd if x > 13)}/{len(vd)}")
    import collections
    b = collections.Counter()
    for x in vd:
        b[("d2<=4" if x <= 4 else "5-13" if x <= 13 else "14-32" if x <= 32
           else "33-100" if x <= 100 else ">100")] += 1
    print("  victim distance bands:", dict(b))
    print(f"  covered by one of OUR live turret rays at death: "
          f"{sum(1 for d in bd_all if d['covered_at_death'])}/{len(bd_all)}"
          f"   (v601/tape30 baseline: 0/42)")

print()
print("=== 4. ESCALATION BAN: does the rebuild loop stop? ===")
# per ore tile: builds of harvesters, deaths.  SK_HARV_REBUILD_ESCALATE=2, ban 60r
allb = []
viol = 0; viol_detail = []
tiles_ge2 = 0
for n, r in sorted(D.items()):
    for tl, lst in r["our_builds_by_tile"].items():
        hb = sorted(rn for (rn, k, i) in lst if k == "harvester")
        if not hb:
            continue
        allb.append((n, tl, len(hb)))
        dl = sorted(d["rnd"] for d in r["harv_deaths_by_tile"].get(tl, []))
        if len(dl) >= 2:
            tiles_ge2 += 1
            esc = dl[1]              # the death that escalates the tile
            nxt = [b for b in hb if b > esc]
            if nxt and nxt[0] - esc < 60:
                viol += 1
                viol_detail.append((n, tl, esc, nxt[0], nxt[0] - esc))
cnt = {}
for (n, tl, k) in allb:
    cnt[k] = cnt.get(k, 0) + 1
print("  harvesters built per ore tile (count of tiles by n_builds):",
      dict(sorted(cnt.items())))
print(f"  ore tiles with >=3 harvesters built: "
      f"{sum(v for k, v in cnt.items() if k >= 3)}/{sum(cnt.values())}")
print(f"  max harvesters on one tile: {max(cnt) if cnt else 0}   "
      f"(v601/tape30 worst: 22 on one icefloe tile)")
print(f"  ore tiles reaching the escalation threshold (>=2 harvester deaths): {tiles_ge2}")
print(f"  BAN VIOLATIONS (rebuild <60 rounds after the 2nd death): {viol}/{tiles_ge2}")
for v in viol_detail:
    print("    ", v)

print()
print("=== 5. BELT RE-LAY LEDGER ===")
cnt2 = {}
relay = []
for n, r in sorted(D.items()):
    for tl, lst in r["our_builds_by_tile"].items():
        bb = sorted(rn for (rn, k, i) in lst if k in BELTK)
        if not bb:
            continue
        cnt2[len(bb)] = cnt2.get(len(bb), 0) + 1
        dl = sorted(d["rnd"] for d in r["belt_deaths_by_tile"].get(tl, []))
        for dr in dl:
            nx = [b for b in bb if b > dr]
            if nx:
                relay.append(nx[0] - dr)
print("  belt pieces built per tile:", dict(sorted(cnt2.items())))
print(f"  tiles rebuilt >=3 times: {sum(v for k, v in cnt2.items() if k >= 3)}"
      f"/{sum(cnt2.values())}  (SK_REBUILD_ESCALATE=3)")
if relay:
    print(f"  belt re-lay latency: median {st.median(relay)} mean {sum(relay)/len(relay):.1f} "
          f"n={len(relay)}  (of {sum(len(v) for r in D.values() for v in r['belt_deaths_by_tile'].values())} deaths)")

print()
print("=== 6. OUR TURRETS: did SK_BELT_COVER buy trunk guns? ===")
tt = {}
sites = []
allt = []
for n, r in sorted(D.items()):
    for tid, rec in r["our_turrets"].items():
        tt[rec["kind"]] = tt.get(rec["kind"], 0) + 1
        allt.append((n, rec))
print("  our turret builds pooled:", tt, " games:", 30)
guns = [(n, x) for (n, x) in allt if x["kind"] == "gunner"]
sents = [(n, x) for (n, x) in allt if x["kind"] == "sentinel"]
print(f"  GUNNERS: {len(guns)} in 30 games ({len(guns)/30:.2f}/game; "
      f"SK_DOOR_GUN_CAP=2/builder)")
if guns:
    dq = [x["dsq_ourcore"] for (n, x) in guns]
    print(f"    site d^2 to OUR core: median {st.median(dq)} "
          f"<=13 (home huddle): {sum(1 for v in dq if v <= 13)}/{len(dq)} "
          f"14-32: {sum(1 for v in dq if 14 <= v <= 32)}/{len(dq)} "
          f">32: {sum(1 for v in dq if v > 32)}/{len(dq)}")
    fired = sum(1 for (n, x) in guns if x["shots"] > 0)
    print(f"    ever fired: {fired}/{len(guns)}   total shots "
          f"{sum(x['shots'] for (n, x) in guns)}")
    vict = {}
    for (n, x) in guns:
        for k, v in x["shot_victims"].items():
            side = D[n]["side"]
            t, kk = k.split(":")
            lab = ("THEIR " if int(t) != side else "OUR ") + kk
            vict[lab] = vict.get(lab, 0) + v
    print("    gunner shot victims:", vict)
    alive = sum(1 for (n, x) in guns if x["died"] is None)
    print(f"    survived to end of game: {alive}/{len(guns)}")
    kil = {}
    for (n, x) in guns:
        if x["died"] is not None:
            kil[x["killer"]] = kil.get(x["killer"], 0) + 1
    print("    gunner killers:", kil)
    life = [(x["died"] - x["born"]) for (n, x) in guns if x["died"] is not None]
    if life:
        print(f"    gunner lifetime when killed: median {st.median(life)}")
print(f"  SENTINELS: {len(sents)} in 30 games ({len(sents)/30:.2f}/game)")
if sents:
    dq = [x["dsq_theircore"] for (n, x) in sents]
    print(f"    site d^2 to THEIR core: median {st.median(dq)} "
          f"in band 14-32: {sum(1 for v in dq if 14 <= v <= 32)}/{len(dq)}")
    print(f"    ever fired: {sum(1 for (n, x) in sents if x['shots'] > 0)}/{len(sents)}"
          f"   total shots {sum(x['shots'] for (n, x) in sents)}")
    print(f"    survived: {sum(1 for (n, x) in sents if x['died'] is None)}/{len(sents)}")
    vict = {}
    for (n, x) in sents:
        for k, v in x["shot_victims"].items():
            side = D[n]["side"]
            t, kk = k.split(":")
            lab = ("THEIR " if int(t) != side else "OUR ") + kk
            vict[lab] = vict.get(lab, 0) + v
    print("    sentinel shot victims:", vict)

print()
print("=== 7. DID OUR GUNS SHOOT THE BELT KILLERS? ===")
# for every distinct enemy turret that killed one of our belt/harvester pieces,
# did any of our turrets ever fire at its tile?
hit = 0; tot3 = 0
for n, r in sorted(D.items()):
    side = r["side"]
    killers = set()
    for src in (r["harv_deaths_by_tile"], r["belt_deaths_by_tile"]):
        for tl, lst in src.items():
            for d in lst:
                if d.get("killer_pos"):
                    killers.add(tuple(d["killer_pos"]))
    if not killers:
        continue
    # tiles our turrets ever fired at: reconstruct from shot victims is not enough;
    # use: did any of our turrets ever REMOVE an enemy turret standing there
    dead_enemy_turret_tiles = set(
        tuple(d["pos"]) for d in r["deaths"]
        if d["team"] != side and d["kind"] in ("gunner", "sentinel", "launcher"))
    for k in killers:
        tot3 += 1
        if k in dead_enemy_turret_tiles:
            hit += 1
print(f"  distinct enemy belt-killer TILES: {tot3}; killer removed during the game: {hit}")
