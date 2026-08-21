#!/usr/bin/env python3
"""v603 signature aggregator -- READ-ONLY.

Built on `scratchpad/s54_v603/cage603.py`, which is `scratchpad/s54_autopsy602/
cage602.py` (the validated tape602 decoder: damage attribution 335/335, core
channel 60/60, delivered-Ti 30/30) plus two additive extensions, both of which
are validated here by driving them to the other verdict:

  peck_census    every BuilderAttack classed (attacker team, victim team, victim
                 kind, victim d^2-band to OUR core: collar <=5, ring <=13, far)
  ring_evictions enemy buildings on a SEAL SEAT removed by OUR peck

One row per fix:
  FIX1  sentinels built; share of games with >= 2
  FIX2  gunner site d^2 to our core; peck-class belt deaths and their
        covered-at-death share; terminus (d^2<=4) belt deaths
  FIX3  eviction-armed round share (rounds with zero empty seal seats);
        our attacks on seal seats; ring evictions that converted
  FIX4  collar pecks (ours, into THEIR buildings at d^2 <= 5 of OUR core)
  FIX5  share of rounds at/over the dynamic accept bar min(7, max(3, 8-enemy))
  OUT   kills, kill round, r1000s   (DESCRIPTIVE ONLY -- no game-share claim)

usage: sig603.py <dir> [<dir> ...]      (*_seatA => side 0, *_seatB => side 1)
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "scratchpad" / "s54_v603"))
from cage603 import decode, dsq_foot          # noqa: E402

BELTK = ("conveyor", "splitter")


def med(v):
    v = sorted(v)
    return None if not v else (v[len(v) // 2] if len(v) % 2
                               else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2)


def one(path: Path, side: int):
    r = decode(path, side)
    them = 1 - side
    out = {"file": path.name, "rounds": r["rounds"],
           "mismatch": r["mismatch"], "checked": r["checked"],
           "nodmg_partial": r["nodmg_with_prior_hp"]}

    # --- outcome (descriptive) --------------------------------------------
    dead_them = r["core_dead"][them]
    dead_us = r["core_dead"][side]
    out["kill"] = 1 if dead_them is not None else 0
    out["killed"] = 1 if dead_us is not None else 0
    out["kill_round"] = dead_them
    out["r1000"] = 1 if (dead_them is None and dead_us is None) else 0
    out["core_dmg_them"] = dict(r["core_dmg"][them])
    out["ti"] = r["ti_collected"][side]

    # --- FIX 1: sentinels ---------------------------------------------------
    sents = [t for t in r["our_turrets"].values() if t["kind"] == "sentinel"]
    guns = [t for t in r["our_turrets"].values() if t["kind"] == "gunner"]
    out["sentinels"] = len(sents)
    out["sent_shots"] = sum(t["shots"] for t in sents)
    out["sent_alive_end"] = sum(1 for t in sents if t["died"] is None)
    out["sent_pair"] = 1 if len(sents) >= 2 else 0
    out["sent_first_round"] = min((t["born"] for t in sents), default=None)
    out["sent_second_round"] = (sorted(t["born"] for t in sents)[1]
                                if len(sents) >= 2 else None)

    # --- FIX 2: trunk guns --------------------------------------------------
    out["gunners"] = len(guns)
    out["gun_dsq"] = [t["dsq_ourcore"] for t in guns]
    out["gun_near"] = sum(1 for t in guns if t["dsq_ourcore"] <= 13)
    out["gun_shots"] = sum(t["shots"] for t in guns)
    gv = {}
    for t in guns:
        for k, n in t["shot_victims"].items():
            gv[k] = gv.get(k, 0) + n
    out["gun_victims"] = gv
    belt_deaths = [d for d in r["deaths"]
                   if d["team"] == side and d["kind"] in BELTK]
    peck_deaths = [d for d in belt_deaths if d["killer_kind"] == "peck"]
    out["belt_deaths"] = len(belt_deaths)
    out["belt_peck_deaths"] = len(peck_deaths)
    out["belt_peck_covered"] = sum(1 for d in peck_deaths if d["covered_at_death"])
    out["belt_term_deaths"] = sum(1 for d in belt_deaths if d["dsq_ourcore"] <= 4)
    out["belt_cov_any"] = sum(1 for d in belt_deaths if d["covered_at_death"])
    out["harv_deaths"] = sum(1 for d in r["deaths"]
                             if d["team"] == side and d["kind"] == "harvester")

    # near-trunk coverage AT END: our live belt/harvester tiles at d^2<=13 of
    # our core that sit inside a live turret ray of ours.
    from cage603 import ray_tiles
    cov = set()
    for (eid, team, kind, pos, di) in r["final_ents"]:
        if team == side and kind in ("gunner", "sentinel"):
            cov |= ray_tiles(pos, kind, di, r["w"], r["h"])
    near = [pos for (eid, team, kind, pos, di) in r["final_ents"]
            if team == side and kind in BELTK + ("harvester",)
            and dsq_foot(pos, r["corepos"][side]) <= 13]
    out["near_trunk_n"] = len(near)
    out["near_trunk_cov"] = sum(1 for p in near if p in cov)

    # --- FIX 3: eviction ----------------------------------------------------
    series = r["seal_state_series"]
    out["armed_rounds"] = sum(1 for (h_, e_, m_) in series if m_ == 0)
    out["seal_attacks"] = sum(s["our_attacks"] for s in r["seal"].values())
    out["ring_evictions"] = len(r["ring_evictions"])
    out["max_held"] = r["max_held"]
    out["contested_max"] = max((e_ for (h_, e_, m_) in series), default=0)

    # --- FIX 5: dynamic accept bar -----------------------------------------
    at_bar = 0
    for (h_, e_, m_) in series:
        acc = 8 - e_
        acc = 7 if acc > 7 else (3 if acc < 3 else acc)
        if h_ >= acc and m_ == 0:
            at_bar += 1
    out["at_bar_rounds"] = at_bar
    out["at_bar"] = 1 if at_bar else 0

    # --- FIX 4: pecks -------------------------------------------------------
    ours_collar = ours_all = theirs_all = 0
    ours_by = {}
    for k, n in r["peck_census"].items():
        at, vt, kind, band = eval(k)                    # noqa: S307 (own data)
        if at == side:
            ours_all += n
            if vt == them:
                ours_by[(kind, band)] = ours_by.get((kind, band), 0) + n
                if band == "collar":
                    ours_collar += n
        elif at == them:
            theirs_all += n
    out["our_pecks"] = ours_all
    out["our_collar_pecks"] = ours_collar
    out["their_pecks"] = theirs_all
    out["our_pecks_by"] = {f"{a}/{b}": c for (a, b), c in sorted(ours_by.items())}
    return out


def main(dirs):
    for d in dirs:
        d = Path(d)
        rows = []
        for f in sorted(d.glob("*.replay26")):
            side = 0 if "_seatA" in f.name or f.name.endswith("_A.replay26") else 1
            rows.append(one(f, side))
        if not rows:
            print(f"{d}: no replays")
            continue
        n = len(rows)
        s = lambda k: sum(x[k] for x in rows)                     # noqa: E731
        print(f"\n=== {d}  n={n} games ===")
        print(f"  INSTRUMENT   attributed==hp {s('checked')-s('mismatch')}/"
              f"{s('checked')}  mismatches {s('mismatch')}  "
              f"our-destroy-at-partial-hp {s('nodmg_partial')}")
        kr = [x['kill_round'] for x in rows if x['kill_round'] is not None]
        print(f"  OUTCOME      kills {s('kill')}/{n}  killed {s('killed')}/{n}  "
              f"r1000 {s('r1000')}  kill rounds {sorted(kr)}  "
              f"median {med(kr)}  by-r300 {sum(1 for k in kr if k <= 300)}/{n}")
        print(f"  FIX1 nest    sentinels {s('sentinels')} "
              f"(median/game {med([x['sentinels'] for x in rows])})  "
              f">=2 in {s('sent_pair')}/{n} = {100*s('sent_pair')/n:.1f}%  "
              f"shots {s('sent_shots')}  alive-end {s('sent_alive_end')}  "
              f"2nd-gun round median "
              f"{med([x['sent_second_round'] for x in rows if x['sent_second_round'] is not None])}")
        gd = [v for x in rows for v in x['gun_dsq']]
        print(f"  FIX2 trunk   gunners {s('gunners')}  site d^2 median {med(gd)}  "
              f"<=13 of our core {s('gun_near')}/{s('gunners') or 1}  "
              f"shots {s('gun_shots')}")
        print(f"               belt deaths {s('belt_deaths')} "
              f"(peck-class {s('belt_peck_deaths')}, of which covered "
              f"{s('belt_peck_covered')})  terminus d^2<=4 deaths "
              f"{s('belt_term_deaths')}  harv deaths {s('harv_deaths')}")
        print(f"               near-trunk tiles covered at end "
              f"{s('near_trunk_cov')}/{s('near_trunk_n')}")
        print(f"  FIX3 evict   armed rounds {s('armed_rounds')}/{s('rounds')} = "
              f"{100*s('armed_rounds')/max(s('rounds'),1):.2f}%  "
              f"seal-seat attacks {s('seal_attacks')}  "
              f"ring evictions {s('ring_evictions')}  "
              f"max_held median {med([x['max_held'] for x in rows])}")
        print(f"  FIX4 collar  OUR pecks {s('our_pecks')} "
              f"({s('our_pecks')/n:.1f}/game)  of which COLLAR (their bldg, "
              f"d^2<=5 of our core) {s('our_collar_pecks')} "
              f"({s('our_collar_pecks')/n:.1f}/game)  THEIR pecks {s('their_pecks')}")
        print(f"  FIX5 ceil    rounds at/over dynamic bar {s('at_bar_rounds')}  "
              f"games reaching it {s('at_bar')}/{n} = {100*s('at_bar')/n:.1f}%")
        by = {}
        for x in rows:
            for k, v in x['our_pecks_by'].items():
                by[k] = by.get(k, 0) + v
        print(f"               our peck targets: "
              f"{dict(sorted(by.items(), key=lambda kv: -kv[1])[:6])}")
        if "--per-game" in sys.argv:
            for x in rows:
                print(f"    {x['file']:<28} kill={x['kill']} r={x['kill_round']} "
                      f"sent={x['sentinels']} gun={x['gunners']} "
                      f"held={x['max_held']} evict={x['ring_evictions']} "
                      f"collar={x['our_collar_pecks']} ti={x['ti']} "
                      f"coredmg={x['core_dmg_them']}")


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
