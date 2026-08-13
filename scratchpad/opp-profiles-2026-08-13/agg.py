#!/usr/bin/env python3
"""Aggregate opponent metrics across the tri-arm games. Usage: agg.py <Opponent>"""
from __future__ import annotations
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / "docs/research/lazy-profile-scripts-2026-08-13"))
sys.path.insert(0, str(ROOT / "tools"))
import lazy_profile as LP  # noqa: E402
from prof import games_for  # noqa: E402

d2 = LP.d2
TUR = ("gunner", "sentinel", "launcher")


def med(xs):
    return round(st.median(xs), 1) if xs else None


def main():
    opp = sys.argv[1]
    gs = games_for(opp)
    rows = []
    for path, oi, ourver, oppver, won, match, gm in gs:
        g = LP.parse(path)
        ui = 1 - oi
        oc, uc = g["corepos"][oi], g["corepos"][ui]
        ufoot, ofoot = g["foot"][ui], g["foot"][oi]
        R = {"tag": f"{match[:8]}g{gm}", "map": f"{g['w']}x{g['h']}",
             "rounds": g["rounds"], "cond": g["wincond"], "we_won": won,
             "ourver": ourver}
        B = g["builds"]
        ob = [b for b in B if b[1] == oi]
        # opening
        h1 = [b for b in ob if b[2] == "harvester"]
        R["harv1"] = h1[0][0] if h1 else None
        R["harv1_d2"] = d2(h1[0][3], oc) if h1 else None
        R["harv_n"] = len(h1)
        R["harv_lost"] = len([d for d in g["deaths"] if d[1] == oi and d[2] == "harvester"])
        R["conv_n"] = len([b for b in ob if b[2] == "conveyor"])
        R["split_n"] = len([b for b in ob if b[2] == "splitter"])
        R["barr_n"] = len([b for b in ob if b[2] == "barrier"])
        bb = [b[0] for b in ob if b[2] == "builder_bot"]
        R["bb_n"] = len(bb)
        R["bb_r30"] = len([r for r in bb if r <= 30])
        R["bb_rounds"] = bb[:8]
        tur = [b for b in ob if b[2] in TUR]
        R["tur1"] = tur[0][0] if tur else None
        fwd = [b for b in tur if d2(b[3], uc) < d2(b[3], oc)]
        R["fwd1"] = fwd[0][0] if fwd else None
        R["fwd1_d2enemy"] = d2(fwd[0][3], uc) if fwd else None
        R["n_gun"] = len([b for b in tur if b[2] == "gunner"])
        R["n_sen"] = len([b for b in tur if b[2] == "sentinel"])
        R["n_lau"] = len([b for b in tur if b[2] == "launcher"])
        R["n_fwd"] = len(fwd)
        # turret deaths / disposability
        hp_ids = {e for _r, e, *_ in g["hpev"]}
        tdead = [d for d in g["deaths"] if d[1] == oi and d[2] in TUR]
        R["tur_dead"] = len(tdead)
        R["tur_selfrm"] = len([d for d in tdead if d[4] not in hp_ids])
        R["tur_life"] = med([d[0] - d[5] for d in tdead])
        R["nodmg_rm"] = [(d[0], d[2], tuple(d[3])) for d in g["deaths"]
                         if d[1] == oi and d[4] not in hp_ids]
        # our core damage: who did it
        ucid = g["coreid"][ui]
        dmg = [(r, dl) for r, e, *_x, dl in
               [(h[0], h[1], h[2], h[3], h[4], h[5]) for h in g["hpev"]]
               if e == ucid and dl < 0]
        R["ourcore_dmg"] = -sum(dl for _r, dl in dmg)
        R["ourcore_heal"] = sum(h[5] for h in g["hpev"] if h[1] == ucid and h[5] > 0)
        R["ourcore_first"] = dmg[0][0] if dmg else None
        R["ourcore_dead"] = (g["winner"] == oi and g["wincond"] == "core_destroyed")
        shooters = {}
        for rnd, frm, to, tteam, kind, sid in g["fires"]:
            if to in ufoot:
                k = shooters.setdefault((kind, sid, frm), [0, rnd])
                k[0] += 1
        R["killers"] = sorted(
            [(kind, sid, frm, n, r0, d2(frm, uc)) for (kind, sid, frm), (n, r0)
             in shooters.items()], key=lambda x: -x[3])[:4]
        R["batk_core"] = len([1 for r, at, aid, ap, tgt in g["batks"]
                              if at == oi and tgt in ufoot])
        # heals
        ob_tiles = {}
        for rnd, t, kind, pos, dirn, eid in B:
            if t == oi:
                ob_tiles.setdefault(tuple(pos), []).append(kind)
        hb = [(r, tgt) for r, t, aid, tgt in g["bheals"] if t == oi]
        R["heal_n"] = len(hb)
        R["heal_core"] = len([1 for r, tgt in hb if tgt in ofoot])
        R["heal_econ"] = len([1 for r, tgt in hb if tgt in ob_tiles and
                              any(k in ("harvester", "conveyor", "splitter", "barrier")
                                  for k in ob_tiles[tuple(tgt)])])
        R["heal_tur"] = len([1 for r, tgt in hb if tgt in ob_tiles and
                             any(k in TUR for k in ob_tiles[tuple(tgt)])])
        R["heal_us"] = len([1 for r, t, aid, tgt in g["bheals"] if t == ui])
        # belt repair
        dl = [(d[0], tuple(d[3])) for d in g["deaths"] if d[1] == oi and d[2] == "conveyor"]
        bl = [(b[0], tuple(b[3])) for b in B if b[1] == oi and b[2] == "conveyor"]
        reb = [min(c) - dr for dr, dp in dl
               for c in [[r for r, p in bl if p == dp and r > dr]] if c]
        R["conv_cut"] = len(dl)
        R["conv_reb"] = len(reb)
        # defence reaction
        ev = []
        for rnd, t, kind, pos, dirn, eid in B:
            if t == ui and kind != "builder_bot" and d2(pos, oc) <= 36:
                ev.append(rnd)
        obt = {tuple(b[3]) for b in B if b[1] == oi and b[2] != "builder_bot"}
        for rnd, at, aid, ap, tgt in g["batks"]:
            if at == ui and (tgt in obt or tgt in ofoot):
                ev.append(rnd)
        for rnd, t, eid, frm, to in g["moves"]:
            if t == ui and d2(to, oc) <= 8:
                ev.append(rnd)
        arr = min(ev) if ev else None
        R["intrude"] = arr
        R["predef"] = len([b for b in ob if b[2] in ("gunner", "sentinel", "launcher", "barrier")
                           and d2(b[3], oc) <= 60 and (arr is None or b[0] < arr)])
        if arr is not None:
            resp = sorted([b[0] for b in ob if b[2] in ("gunner", "sentinel", "launcher", "barrier")
                           and b[0] >= arr and d2(b[3], oc) <= 60])
            R["def_lat"] = resp[0] - arr if resp else None
        else:
            R["def_lat"] = None
        # our forward turret survival + their first shot at it (joint metric)
        ourfwd = [b for b in B if b[1] == ui and b[2] in TUR and d2(b[3], oc) < d2(b[3], uc)]
        R["ourfwd_n"] = len(ourfwd)
        lives = []
        for b in ourfwd:
            dd = [d for d in g["deaths"] if d[4] == b[5]]
            if dd:
                lives.append(dd[0][0] - b[0])
        R["ourfwd_life"] = med(lives)
        R["ourfwd_died"] = len(lives)
        # first shot by them at any of our forward turret tiles after build
        lat = []
        for b in ourfwd:
            fs = [rnd for rnd, frm, to, tt, kind, sid in g["fires"]
                  if to == tuple(b[3]) and rnd >= b[0]]
            if fs:
                lat.append(min(fs) - b[0])
        R["shot_lat"] = med(lat)
        R["shot_lat_n"] = len(lat)
        # cpu
        R["cpu_max"] = g["execmax"][oi]
        R["tled"] = g["tled"][oi]
        R["cpu_max_us_ours"] = g["execmax"][ui]
        R["tled_ours"] = g["tled"][ui]
        if g["ammo_hist"]:
            last = g["ammo_hist"][-1][1]
            R["ti_coll"] = last.get(oi, (0, 0, 0))[1]
            R["ammo_end"] = last.get(oi, (0, 0, 0))[2]
        rows.append(R)

    keys1 = ["tag", "map", "rounds", "cond", "we_won", "harv1", "harv1_d2", "harv_n",
             "harv_lost", "conv_n", "split_n", "barr_n", "bb_n", "bb_r30", "tur1",
             "fwd1", "fwd1_d2enemy", "n_gun", "n_sen", "n_lau", "n_fwd", "tur_dead",
             "tur_selfrm", "tur_life", "ourcore_dmg", "ourcore_heal", "ourcore_first",
             "ourcore_dead", "batk_core", "heal_n", "heal_core", "heal_econ",
             "heal_tur", "heal_us", "conv_cut", "conv_reb", "intrude", "predef",
             "def_lat", "ourfwd_n", "ourfwd_died", "ourfwd_life", "shot_lat",
             "cpu_max", "tled", "cpu_max_us_ours", "tled_ours", "ti_coll", "ammo_end"]
    print("\t".join(keys1))
    for R in rows:
        print("\t".join(str(R.get(k, "")) for k in keys1))
    print("\n--- killers (turret tiles that shot our core footprint) ---")
    for R in rows:
        print(R["tag"], R["killers"])
    print("\n--- no-damage removals (opp) ---")
    for R in rows:
        if R["nodmg_rm"]:
            print(R["tag"], R["nodmg_rm"][:12], "n=", len(R["nodmg_rm"]))
    print("\n--- builder spawn rounds (opp, first 8) ---")
    for R in rows:
        print(R["tag"], R["bb_rounds"])

    def col(k):
        return [R[k] for R in rows if R.get(k) is not None]
    print("\n--- SUMMARY n=%d games ---" % len(rows))
    for k in ["harv1", "tur1", "fwd1", "fwd1_d2enemy", "def_lat", "tur_life",
              "ourfwd_life", "shot_lat", "cpu_max", "tled", "heal_n"]:
        v = col(k)
        print(f"  {k:14s} n={len(v):2d} med={med(v)} min={min(v) if v else None} "
              f"max={max(v) if v else None} vals={sorted(v)}")
    print("  heals: core=%d econ=%d turret=%d total=%d" %
          (sum(R["heal_core"] for R in rows), sum(R["heal_econ"] for R in rows),
           sum(R["heal_tur"] for R in rows), sum(R["heal_n"] for R in rows)))
    print("  turrets: gun=%d sen=%d lau=%d fwd=%d dead=%d selfrm=%d" %
          tuple(sum(R[k] for R in rows) for k in
                ["n_gun", "n_sen", "n_lau", "n_fwd", "tur_dead", "tur_selfrm"]))
    print("  our core died in %d/%d; conv cut %d rebuilt %d; harv built %d lost %d" %
          (sum(1 for R in rows if R["ourcore_dead"]), len(rows),
           sum(R["conv_cut"] for R in rows), sum(R["conv_reb"] for R in rows),
           sum(R["harv_n"] for R in rows), sum(R["harv_lost"] for R in rows)))
    print("  predef>0 in %d/%d games; splitters %d; barriers %d" %
          (sum(1 for R in rows if R["predef"] > 0), len(rows),
           sum(R["split_n"] for R in rows), sum(R["barr_n"] for R in rows)))


if __name__ == "__main__":
    main()
