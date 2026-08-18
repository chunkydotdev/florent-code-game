#!/usr/bin/env python3
"""Fold sentrace.py TSVs into one row per arm."""
import sys

H = ["tag", "rounds", "sent_r", "conc_r", "max_sent", "hit_r", "conc_hit_r",
     "max_hit", "shots", "dealt", "healed", "healshare", "opp_hp"]


def load(p):
    out = []
    for line in open(p):
        f = line.rstrip("\n").split("\t")
        if len(f) != len(H) or f[0] in ("tag",) or not f[1].isdigit():
            continue
        out.append(dict(zip(H, f)))
    return out


def main():
    name = sys.argv[1]
    d = []
    for p in sys.argv[2:]:
        d += load(p)
    I = lambda k: sum(int(x[k]) for x in d)
    dealt, healed = I("dealt"), I("healed")
    sr = I("sent_r")
    hr = I("hit_r")
    print("%-10s games=%3d | FWD sent_r=%6d conc_r=%5d g>0=%3d | "
          "HITTING hit_r=%6d conc_hit_r=%5d g>0=%3d max>=2=%3d | "
          "shots=%5d shots/hit_r=%.4f | dealt=%7d healed=%7d healshare=%.3f"
          % (name, len(d), sr, I("conc_r"),
             sum(1 for x in d if int(x["conc_r"]) > 0),
             hr, I("conc_hit_r"),
             sum(1 for x in d if int(x["conc_hit_r"]) > 0),
             sum(1 for x in d if int(x["max_hit"]) >= 2),
             I("shots"), I("shots") / hr if hr else -1,
             dealt, healed, healed / dealt if dealt else -1))


main()
