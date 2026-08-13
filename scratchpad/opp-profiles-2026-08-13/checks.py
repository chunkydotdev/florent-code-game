#!/usr/bin/env python3
"""Controls + ammo/shot ledger. Usage: checks.py <Opponent>"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / "docs/research/lazy-profile-scripts-2026-08-13"))
sys.path.insert(0, str(ROOT / "tools"))
import lazy_profile as LP  # noqa: E402
from prof import games_for  # noqa: E402


def main():
    opp = sys.argv[1]
    print("####", opp)
    print("tag\tmap\trounds\ttled\tcpumax\tconv_ti\tammo_end\tshots\tshots_g\tshots_s\tspend")
    for path, oi, ourver, oppver, won, match, gm in games_for(opp):
        g = LP.parse(path)
        conv, prev = 0, None
        for rnd, row in g["ammo_hist"]:
            cur = row.get(oi)
            if cur and prev and cur[2] > prev[2]:
                conv += cur[2] - prev[2]
            prev = cur
        sh = {"gunner": 0, "sentinel": 0, "?": 0}
        for rnd, frm, to, tteam, kind, sid in g["fires"]:
            if tteam == oi:
                sh[kind] = sh.get(kind, 0) + 1
        ammo_end = g["ammo_hist"][-1][1].get(oi, (0, 0, 0))[2] if g["ammo_hist"] else -1
        spend = sh["gunner"] * 4 + sh["sentinel"] * 10
        print(f"{match[:8]}g{gm}\t{g['w']}x{g['h']}\t{g['rounds']}\t{g['tled'][oi]}\t"
              f"{g['execmax'][oi]}\t{conv}\t{ammo_end}\t"
              f"{sum(sh.values())}\t{sh['gunner']}\t{sh['sentinel']}\t{spend}")


if __name__ == "__main__":
    main()
