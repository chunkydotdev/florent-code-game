#!/usr/bin/env python3
"""Loss/win classifier for the s51 rush autopsy.

TWO ORTHOGONAL AXES, because forcing one label hides which half failed:

  OFFENCE (why the rush did not kill, or that it did):
    KILLED         our sentinel line put >= 28 shots on their core and it died
    NO_TURRET      no turret of ours ever landed ONE shot on their core
    MAG_STARVED    a core-hitting sentinel existed but team ammo was >= 10 in
                   < 25% of its life (the weapon stood unfunded)
    HEAL_OUTRUN    funded (>=25%) yet >= 80% of the damage we dealt to their
                   core was healed straight back
    TURRET_LOST    funded, not out-healed, but the sentinel died short of 28
                   shots and nothing replaced it in time

  DEFENCE (how the game ended for our core):
    CORE_KILLED / SURVIVED

Facts come from turret_ledger/turret_game (fireTurret channel), attrib (UpdateHp
channel) and the phase timeline parsed out of the bot's own FS PHASE stderr.
The two replay channels were cross-checked against each other in turrets.py
(30/30 exact) before any of this ran.

DECISION-LIST ORDER IS FIXED AND THE THRESHOLDS ARE WRITTEN DOWN HERE, not
tuned per game.  Sensitivity of the counts to each threshold is printed.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FUNDED_MIN = 0.25
HEAL_MAX = 0.80
KILL_SHOTS = 28


def classify(g):
    shots = g["siege_shots"]
    life = g["siege_life"]
    funded = g["siege_funded"]
    heal = g["oppcore_heal"]
    dealt = shots * 18
    fs = (funded / life) if life else 0.0
    hs = (heal / dealt) if dealt else 0.0
    killed = (g["cond"] == "Core destroyed" and g["ours"] == "US")
    if killed:
        off = "KILLED"
    elif shots == 0:
        off = "NO_TURRET"
    elif fs < FUNDED_MIN:
        off = "MAG_STARVED"
    elif hs >= HEAL_MAX:
        off = "HEAL_OUTRUN"
    else:
        off = "TURRET_LOST"
    dfc = "CORE_KILLED" if (g["ours"] == "OPP"
                            and g["cond"] == "Core destroyed") else "SURVIVED"
    return off, dfc, round(fs, 3), round(hs, 3)


def load():
    tg = {r["tag"]: r for r in
          csv.DictReader(open(HERE / "turret_game.tsv"), delimiter="\t")}
    at = {r["tag"]: r for r in
          csv.DictReader(open(HERE / "attrib.tsv"), delimiter="\t")}
    out = []
    for tag, r in tg.items():
        a = at[tag]
        out.append(dict(
            tag=tag, map=r["map"], seed=r["seed"], seat=r["seat"],
            ours=r["ours"], cond=r["cond"], turn=int(r["turn"]),
            siege_shots=int(r["siege_shots"]), siege_life=int(r["siege_life"]),
            siege_funded=int(r["siege_funded"]),
            siege_first=int(r["siege_first"]) if r["siege_first"] else None,
            sent_n=int(r["sent_n"]), siege_n=int(r["siege_n"]),
            dud_sent_n=int(r["dud_sent_n"]),
            dud_funded_r=int(r["dud_funded_r"]),
            oppcore_heal=int(a["oppcore_heal"]),
            ourcore_heal=int(a["ourcore_heal"]),
            their_shots=int(r["their_siege_shots"]),
            their_first=int(r["their_siege_first"]) if r["their_siege_first"]
            else None,
        ))
    return out


def main():
    rows = load()
    for r in rows:
        off, dfc, fs, hs = classify(r)
        r.update(offence=off, defence=dfc, funded_share=fs, heal_share=hs)
    cols = ["tag", "map", "seat", "ours", "cond", "turn", "offence", "defence",
            "siege_n", "sent_n", "dud_sent_n", "siege_first", "siege_shots",
            "siege_life", "siege_funded", "funded_share", "oppcore_heal",
            "heal_share", "their_first", "their_shots"]
    with open(HERE / "classified.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join("" if r[c] is None else str(r[c])
                               for c in cols) + "\n")
    w = [max(len(c), max(len(str(r[c]) if r[c] is not None else "-")
                         for r in rows)) for c in cols]
    print(" ".join(c.ljust(x) for c, x in zip(cols, w)))
    for r in sorted(rows, key=lambda x: (x["offence"], x["map"])):
        print(" ".join((str(r[c]) if r[c] is not None else "-").ljust(x)
                       for c, x in zip(cols, w)))
    print()
    from collections import Counter
    print("OFFENCE:", dict(Counter(r["offence"] for r in rows)))
    print("DEFENCE:", dict(Counter(r["defence"] for r in rows)))
    print("cross:", dict(Counter((r["offence"], r["defence"]) for r in rows)))
    print("wins by offence:",
          dict(Counter(r["offence"] for r in rows if r["ours"] == "US")))
    # threshold sensitivity
    print("\nSENSITIVITY (offence counts as thresholds move)")
    import copy
    global FUNDED_MIN, HEAL_MAX
    base = (FUNDED_MIN, HEAL_MAX)
    for fm in (0.15, 0.25, 0.40):
        for hm in (0.70, 0.80, 0.90):
            FUNDED_MIN, HEAL_MAX = fm, hm
            c = Counter(classify(r)[0] for r in copy.deepcopy(rows))
            print("  funded<%.2f heal>=%.2f -> %s" % (fm, hm, dict(c)))
    FUNDED_MIN, HEAL_MAX = base


if __name__ == "__main__":
    main()
