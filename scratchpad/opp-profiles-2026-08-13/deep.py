#!/usr/bin/env python3
"""Targeted follow-ups. Usage: deep.py <Opponent>"""
from __future__ import annotations
import hashlib
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


def main():
    opp = sys.argv[1]
    print("#### ", opp)
    kill_rounds, death_rounds = [], []
    sieges = []
    for path, oi, ourver, oppver, won, match, gm in games_for(opp):
        g = LP.parse(path)
        ui = 1 - oi
        oc, uc = g["corepos"][oi], g["corepos"][ui]
        ufoot, ofoot = g["foot"][ui], g["foot"][oi]
        tag = f"{match[:8]}g{gm}"
        # map fingerprint (terrain only)
        mh = hashlib.sha1(str(g["tiles"]).encode()).hexdigest()[:8]
        # ore tiles near their core
        ore = [(x, y) for y, row in enumerate(g["tiles"]) for x, v in enumerate(row) if v == 2]
        near = sorted(ore, key=lambda p: d2(p, oc))[:4]
        h1 = [b for b in g["builds"] if b[1] == oi and b[2] == "harvester"]
        print(f"\n== {tag} {g['w']}x{g['h']} map={mh} r={g['rounds']} cond={g['wincond']} "
              f"we_won={won} ore_n={len(ore)} nearest_ore_d2={[d2(p,oc) for p in near]}")
        print(f"   harvesters={[(b[0], tuple(b[3]), d2(b[3],oc)) for b in h1][:6]}")
        # ammo conversions
        conv = []
        prev = None
        for rnd, row in g["ammo_hist"]:
            cur = row.get(oi)
            if cur and prev and cur[2] > prev[2]:
                conv.append((rnd, cur[2] - prev[2]))
            prev = cur
        print(f"   ammo converts n={len(conv)} first={conv[:4]} total={sum(c[1] for c in conv)}")
        # SIEGE: their turret builds at d2<=26 of OUR core, with replacement latency
        sg = [(b[0], b[2], tuple(b[3]), d2(b[3], uc), b[5]) for b in g["builds"]
              if b[1] == oi and b[2] in TUR and d2(b[3], uc) <= 26]
        print(f"   siege turrets (d2<=26 of OUR core) n={len(sg)}: {sg[:10]}")
        sieges += [s[3] for s in sg]
        # replacement latency: after each siege turret death, next siege turret build
        dth = {d[4]: d[0] for d in g["deaths"]}
        lat = []
        for r0, k, p, dd, eid in sg:
            if eid in dth:
                nxt = [s[0] for s in sg if s[0] > dth[eid]]
                if nxt:
                    lat.append(min(nxt) - dth[eid])
        if lat:
            print(f"   siege replacement latency after death: {sorted(lat)}")
        # core death rounds
        ucid, ocid = g["coreid"][ui], g["coreid"][oi]
        if g["winner"] == oi and g["wincond"] == "core_destroyed":
            death_rounds.append(g["rounds"] - 1)
        if g["winner"] == ui and g["wincond"] == "core_destroyed":
            kill_rounds.append(g["rounds"] - 1)
        # do they heal turrets in place? per-turret heal counts
        obt = {}
        for rnd, t, kind, pos, dirn, eid in g["builds"]:
            if t == oi:
                obt.setdefault(tuple(pos), set()).add(kind)
        ht = {}
        for r, t, aid, tgt in g["bheals"]:
            if t == oi and tgt in obt and obt[tgt] & set(TUR):
                ht[tgt] = ht.get(tgt, 0) + 1
        if ht:
            print(f"   heals on own turret tiles: {sorted(ht.items(), key=lambda x:-x[1])[:5]}")
        # our first forward turret and their response
        ourfwd = [b for b in g["builds"] if b[1] == ui and b[2] in TUR
                  and d2(b[3], oc) < d2(b[3], uc)]
        for b in ourfwd[:3]:
            fs = [rnd for rnd, frm, to, tt, kind, sid in g["fires"]
                  if to == tuple(b[3]) and rnd >= b[0]]
            ba = [rnd for rnd, at, aid, ap, tgt in g["batks"]
                  if at == oi and tgt == tuple(b[3]) and rnd >= b[0]]
            dd = [d[0] for d in g["deaths"] if d[4] == b[5]]
            print(f"   OURFWD {b[2]} r{b[0]}@{tuple(b[3])} d2theircore={d2(b[3],oc)}: "
                  f"first_shot={min(fs) if fs else None} first_builder_atk={min(ba) if ba else None} "
                  f"n_atk={len(ba)} died_r={dd[0] if dd else None}")
    print(f"\n>> our core died rounds {sorted(death_rounds)} (n={len(death_rounds)})")
    print(f">> their core died rounds {sorted(kill_rounds)} (n={len(kill_rounds)})")
    if sieges:
        print(f">> siege turret d2-to-our-core: median={st.median(sieges)} "
              f"dist={sorted(sieges)}")


if __name__ == "__main__":
    main()
