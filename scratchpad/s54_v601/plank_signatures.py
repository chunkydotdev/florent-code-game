#!/usr/bin/env python3
"""v601 PER-PLANK ABLATION SIGNATURES, read off local replays.

Reuses `scratchpad/s54_autopsy/tape30_deaths.py` verbatim -- the decoder whose
attribution was driven both ways in the autopsy (baseline 0/246 self-check
mismatches; damage alphabet perturbed by one point -> 166/246 mismatches; shadow
index off -> 258/295 deaths unattributed).  NOTHING is re-implemented here; this
file only aggregates.

  PLANK 1  SK_HARV_ESCALATE : harvester builds by us onto a tile that has
                              ALREADY lost >= SK_HARV_REBUILD_ESCALATE
                              harvesters ("rebuilds into a known killzone").
                              Target: DOWN.
  PLANK 2  SK_BELT_COVER    : share of our destroyed belt/harvester pieces that
                              were inside a LIVE turret of ours' actual firing
                              ray at the moment of death.  Baseline 0/42.
                              Target: UP (> 0).
  PLANK 3  SK_TARGET_PRIO   : share of our turret shots, and of our builder
                              pecks, that landed on an enemy BARRIER.
                              Baseline 75.3% / 74.8%.  Target: DOWN.

The SEAT is read from the filename suffix `_seat{A,B}` written by battery.sh --
a wrong-side read produces a clean confident number about the OPPONENT, so it is
never guessed.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "scratchpad" / "s54_autopsy"))
from tape30_deaths import decode, reach_tiles          # noqa: E402

ESCALATE_N = 2          # must track sk_maps.SK_HARV_REBUILD_ESCALATE
BELT_KINDS = ("harvester", "conveyor", "splitter")


def seat_of(path: Path) -> int:
    name = path.name
    if "_seatA" in name:
        return 0
    if "_seatB" in name:
        return 1
    raise SystemExit(f"{name}: no _seatA/_seatB in the filename -- refusing to "
                     f"guess the subject side")


def one(path: Path):
    our = seat_of(path)
    r = decode(path, our=our)
    w, h = r["w"], r["h"]

    # --- PLANK 1 -----------------------------------------------------------
    deaths_by_tile = {}
    rebuild_into_killzone = 0
    harv_builds = 0
    # births and deaths are both in round order; replay one timeline.
    events = []
    for (rnd, team, kind, eid, pos) in r["births"]:
        if team == our and kind == "harvester":
            events.append((rnd, 0, pos))
    for d in r["deaths"]:
        if d["team"] == our and d["kind"] == "harvester":
            events.append((d["rnd"], 1, d["pos"]))
    # a death is resolved at END of round, so a build in the same round is first
    events.sort(key=lambda e: (e[0], e[1]))
    for rnd, kind, pos in events:
        if kind == 0:
            harv_builds += 1
            if deaths_by_tile.get(pos, 0) >= ESCALATE_N:
                rebuild_into_killzone += 1
        else:
            deaths_by_tile[pos] = deaths_by_tile.get(pos, 0) + 1

    # --- PLANK 2 -----------------------------------------------------------
    belt_dead = 0
    belt_dead_ray = 0
    for d in r["deaths"]:
        if d["team"] != our or d["kind"] not in BELT_KINDS:
            continue
        belt_dead += 1
        cov = set()
        for (tp, tk, td) in d["our_turrets_live"]:
            cov |= reach_tiles(tp, tk, td, w, h, False)
        if d["pos"] in cov:
            belt_dead_ray += 1

    # PLANK 2, MECHANISM SIDE: where our turrets actually get planted.  The
    # autopsy's siting mismatch was 12 of 18 inside d^2 10 of our own core
    # while 85.7% of the dead belt sat outside d^2 13.
    turr_in = turr_out = 0
    for rec in r["our_turrets"].values():
        if rec["dsq_our"] <= 13:
            turr_in += 1
        else:
            turr_out += 1
    belt_dead_no_turret = sum(
        1 for d in r["deaths"]
        if d["team"] == our and d["kind"] in BELT_KINDS
        and not d["our_turrets_live"])

    # ⭐ P2b -- COVERAGE WITHOUT THE COLLIDER.  The briefed signature ("was a
    # dead belt piece covered") is conditioned on the piece DYING, and PLANK 1
    # exists to stop it dying: with P1 on, the surviving deaths concentrate in
    # the window before any turret of ours exists (measured 8/14 here), so the
    # death-conditioned metric can read 0 for a reason that is PLANK 1 working.
    # This is the same shape as the collider `PROGRAMME.md` flags on the
    # kill-round bar.  So: sample every round, over LIVE trunk tiles, whether a
    # LIVE turret of ours has them on its ray.
    # ⚠ FACING IS THE FINAL FACING (the decoder keeps one `dir` per entity and
    # a gunner may rotate), so this is exact for anything that never rotated
    # and approximate otherwise.
    died_at = {}
    for d in r["deaths"]:
        died_at.setdefault(d["id"], d["rnd"])
    end = r["rounds"]
    ours_belt = [(e.born, died_at.get(e.id, end), e.pos)
                 for e in r["ever"].values()
                 if e.team == our and e.kind in BELT_KINDS]
    corenw = r["corepos"][our]
    from tape30_deaths import dsq_foot
    ours_belt = [b for b in ours_belt if dsq_foot(b[2], corenw) > 13]
    ours_turr = [(e.born, died_at.get(e.id, end), e.pos, e.kind, e.dir)
                 for e in r["ever"].values()
                 if e.team == our and e.kind in ("gunner", "sentinel")]
    trunk_rounds = 0
    trunk_covered = 0
    if ours_belt:
        ray_cache = {}
        for rr in range(end):
            live_t = [t for t in ours_turr if t[0] <= rr < t[1]]
            if not live_t:
                trunk_rounds += sum(1 for b in ours_belt if b[0] <= rr < b[1])
                continue
            cov = set()
            for t in live_t:
                key = (t[2], t[3], t[4])
                if key not in ray_cache:
                    ray_cache[key] = reach_tiles(t[2], t[3], t[4], w, h, False)
                cov |= ray_cache[key]
            for b in ours_belt:
                if b[0] <= rr < b[1]:
                    trunk_rounds += 1
                    if b[2] in cov:
                        trunk_covered += 1

    # --- PLANK 3 -----------------------------------------------------------
    shots = shots_barrier = pecks = pecks_barrier = 0
    for (rnd, skind, steam, frm, vid, vkind, vteam, to) in r["damage_log"]:
        if steam != our:
            continue
        if skind == "peck":
            pecks += 1
            if vkind == "barrier":
                pecks_barrier += 1
        elif skind in ("gunner", "sentinel"):
            shots += 1
            if vkind == "barrier":
                shots_barrier += 1

    return dict(file=path.name, our=our, rounds=r["rounds"],
                cond=r["cond"], winner=r["winner"],
                mismatch=r["mismatch"], checked=r["checked"],
                harv_builds=harv_builds,
                harv_deaths=sum(deaths_by_tile.values()),
                rebuild_into_killzone=rebuild_into_killzone,
                belt_dead=belt_dead, belt_dead_ray=belt_dead_ray,
                turr_in=turr_in, turr_out=turr_out,
                belt_dead_no_turret=belt_dead_no_turret,
                trunk_rounds=trunk_rounds, trunk_covered=trunk_covered,
                shots=shots, shots_barrier=shots_barrier,
                pecks=pecks, pecks_barrier=pecks_barrier)


def agg(d: Path, label: str):
    rows = [one(p) for p in sorted(d.glob("*.replay26"))]
    if not rows:
        print(f"{label}: NO REPLAYS in {d}")
        return None
    t = {k: sum(x[k] for x in rows) for k in
         ("harv_builds", "harv_deaths", "rebuild_into_killzone", "belt_dead",
          "belt_dead_ray", "turr_in", "turr_out", "belt_dead_no_turret",
          "trunk_rounds", "trunk_covered",
          "shots", "shots_barrier", "pecks", "pecks_barrier",
          "mismatch", "checked", "rounds")}
    wins = sum(1 for x in rows
               if (x["winner"] == x["our"]))
    pct = lambda a, b: ("n/a" if not b else f"{100.0*a/b:.1f}%")
    print(f"--- {label}   n={len(rows)} games, {t['rounds']} rounds, "
          f"our-side wins {wins}/{len(rows)}")
    print(f"    instrument self-check mismatches {t['mismatch']}/{t['checked']}")
    print(f"    P1 harvester builds {t['harv_builds']}  deaths {t['harv_deaths']}"
          f"  REBUILDS INTO A >= {ESCALATE_N}-DEATH TILE {t['rebuild_into_killzone']}"
          f"  ({pct(t['rebuild_into_killzone'], t['harv_builds'])} of builds)")
    print(f"    P2 our belt pieces destroyed {t['belt_dead']}  "
          f"IN A LIVE FIRING RAY AT DEATH {t['belt_dead_ray']}"
          f"  ({pct(t['belt_dead_ray'], t['belt_dead'])})")
    print(f"    P2 our turrets built: d2<=13 of our core {t['turr_in']}  "
          f"OUTSIDE (annulus) {t['turr_out']}   |  belt deaths with NO live "
          f"turret of ours {t['belt_dead_no_turret']}/{t['belt_dead']}")
    print(f"    P2b TRUNK-TILE-ROUNDS covered by a live ray "
          f"{t['trunk_covered']}/{t['trunk_rounds']} "
          f"({pct(t['trunk_covered'], t['trunk_rounds'])})  [death-independent]")
    print(f"    P3 our turret shots {t['shots']}  on BARRIERS {t['shots_barrier']}"
          f"  ({pct(t['shots_barrier'], t['shots'])})")
    print(f"    P3 our builder pecks {t['pecks']}  on BARRIERS {t['pecks_barrier']}"
          f"  ({pct(t['pecks_barrier'], t['pecks'])})")
    return t


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        d = Path(arg)
        agg(d, d.name)
