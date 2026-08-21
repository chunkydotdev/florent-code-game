#!/usr/bin/env python3
"""v602 signature decoder -- READ-ONLY, built on the s54 autopsy decoder.

Reuses `scratchpad/s54_autopsy601/walker.py::decode` unmodified (it was
cross-validated 45/45 games against `tools/skalman_fidelity.py`'s independent
ring-barrier recogniser) and reports the five signatures v602's fixes are
supposed to move:

  storm     builders spawned / died, worst death-tile pooling, killer
  cycle     share of builder steps that revisit the tile two back (A-B-A-B)
  dwell     worst consecutive-rounds-on-one-tile, overall and on the enemy lap
  cage      lap-rounds, lap actions split build/peck, pecks at the enemy CORE
  deaths    no-damage removals (the engine's exception-destroy channel)

usage: sig.py <replay> <our_side>            (one game)
       sig.py --dir <dir> <A_side> <B_side>  (battery: *_seatA / *_seatB)
"""
import os
import sys
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
os.environ["KEEP_TRACK"] = "1"
sys.path.insert(0, str(ROOT / "scratchpad" / "s54_autopsy601"))
from walker import decode, ROLE_NAME, cage_lap, LAP_SEAL_IDX   # noqa: E402


def one(path: Path, side: int):
    r = decode(path, side)
    lap = set(r["lap"])
    seal = set(tuple(t) for t in r["seal_set"])
    steps = revisits = 0
    worst_dwell = 0
    worst_lap_dwell = 0
    ring_bar = lap_rounds = lap_builds = lap_pecks = core_pecks = 0
    for b in r["bots"].values():
        tr = [t[1] for t in b.get("track", [])]
        # 2-cycle share: a step that lands where the body was two rounds ago
        for i in range(2, len(tr)):
            if tr[i] != tr[i - 1]:
                steps += 1
                if tr[i] == tr[i - 2]:
                    revisits += 1
        run = 1
        lrun = 0
        for i in range(1, len(tr)):
            if tr[i] == tr[i - 1]:
                run += 1
            else:
                run = 1
            if run > worst_dwell:
                worst_dwell = run
            if tr[i] in lap:
                lrun = run
                if lrun > worst_lap_dwell:
                    worst_lap_dwell = lrun
        ring_bar += b["ring_barriers"]
        lap_rounds += b["lap_rounds"]
        lap_builds += b["build_kinds"].get("barrier", 0) if b["lap_rounds"] else 0
        for k, n in b["peck_kinds"].items():
            if k == "core":
                core_pecks += n
    ours = [d for d in r["deaths"] if d["team"] == side]
    bots_dead = [d for d in ours if d["kind"] == "builder_bot"]
    tiles = {}
    for d in bots_dead:
        tiles[tuple(d["pos"])] = tiles.get(tuple(d["pos"]), 0) + 1
    top = max(tiles.items(), key=lambda kv: kv[1]) if tiles else (None, 0)
    killers = {}
    for d in bots_dead:
        killers[(d["killer_kind"], tuple(d["killer_pos"]) if d["killer_pos"] else None)] = \
            killers.get((d["killer_kind"], tuple(d["killer_pos"]) if d["killer_pos"] else None), 0) + 1
    topk = max(killers.items(), key=lambda kv: kv[1]) if killers else (None, 0)
    turret_deaths = sum(n for (k, _p), n in killers.items()
                        if k in ("gunner", "sentinel"))
    return {
        "file": path.name, "side": side, "rounds": r["rounds"],
        "winner": r["winner"], "cond": r["cond"],
        "builders": len(r["bots"]), "bot_deaths": len(bots_dead),
        "nodamage": sum(1 for d in ours if d["nodamage"]),
        "top_death_tile": top[0], "top_death_n": top[1],
        "top_killer": topk[0], "top_killer_n": topk[1],
        "turret_deaths": turret_deaths,
        "steps": steps, "revisits": revisits,
        "cycle_share": (100.0 * revisits / steps) if steps else 0.0,
        "worst_dwell": worst_dwell, "worst_lap_dwell": worst_lap_dwell,
        "ring_barriers": ring_bar, "lap_rounds": lap_rounds,
        "lap_barriers": lap_builds, "core_pecks": core_pecks,
        "seals": len(seal),
    }


HDR = ("game", "rnds", "win", "blds", "deaths", "nodmg", "topTile", "n",
       "turretKill", "cyc%", "dwell", "lapDwell", "ringBar", "lapRnds", "corePeck")


def show(rows):
    print("\t".join(HDR))
    for x in rows:
        print("\t".join(str(v) for v in (
            x["file"].replace(".replay26", ""), x["rounds"], x["winner"],
            x["builders"], x["bot_deaths"], x["nodamage"],
            x["top_death_tile"], x["top_death_n"], x["turret_deaths"],
            f"{x['cycle_share']:.1f}", x["worst_dwell"], x["worst_lap_dwell"],
            x["ring_barriers"], x["lap_rounds"], x["core_pecks"])))
    if len(rows) > 1:
        st = sum(x["steps"] for x in rows)
        rv = sum(x["revisits"] for x in rows)
        print(f"TOTALS  builders={sum(x['builders'] for x in rows)} "
              f"deaths={sum(x['bot_deaths'] for x in rows)} "
              f"nodamage={sum(x['nodamage'] for x in rows)} "
              f"ring_barriers={sum(x['ring_barriers'] for x in rows)} "
              f"(per game {sum(x['ring_barriers'] for x in rows)/len(rows):.3f}) "
              f"lap_rounds={sum(x['lap_rounds'] for x in rows)} "
              f"core_pecks={sum(x['core_pecks'] for x in rows)} "
              f"cycle_share={100.0*rv/st if st else 0:.1f}% ({rv}/{st}) "
              f"worst_dwell={max(x['worst_dwell'] for x in rows)}")


def main():
    if sys.argv[1] == "--dir":
        d = Path(sys.argv[2])
        a_side, b_side = int(sys.argv[3]), int(sys.argv[4])
        rows = []
        for p in sorted(d.glob("*.replay26")):
            side = a_side if "seatA" in p.name else b_side
            rows.append(one(p, side))
        show(rows)
    else:
        show([one(Path(sys.argv[1]), int(sys.argv[2]))])


if __name__ == "__main__":
    main()
