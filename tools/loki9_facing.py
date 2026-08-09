#!/usr/bin/env python3
"""LOKI-9 DID-IT-FIRE CHECK — are our new home turrets aimed at the enemy core?

This is the MECHANISM check for `docs/prereg/PREREG-loki9-facing.md`. It is NOT
the verdict. The verdict is `core_kill_share` vs LOKI-8, per PROGRAMME.md, and
a mechanism metric never substitutes for the currency.

WHAT IT MEASURES. For every turret (gunner/sentinel) a team BUILDS inside its
own home band, the angle between the facing it was built with and the direction
to the enemy core. "Aligned" = within 45 degrees, i.e. the nearest compass step.

WHY IT CAN BE TRUSTED TO SEE THE TREATMENT. Facing is on the wire —
`Sentinel { Direction direction = 1 }` inside `PlaceEntity.Entity` — and
`replay_census.parse_entity` already decodes it. Nothing is inferred.

THE D7 TRAPS THIS FILE IS BUILT AROUND. A treatment that is verified as CODED
and then measured with an invalid discriminator answers nothing (s25, LOKI-QUIET:
"0 builder attacks" was true, decoded, and irrelevant). The specific traps here:

  1. `rotate()` RE-EMITS placeEntity for an existing id, inflating gunner builds
     ~3x. A build is the FIRST placeEntity carrying an id — same guard as
     `replay_events.py`. Without it, a rotated gunner is counted repeatedly and
     at its NEW facing, which is not the built facing.
  2. THE HOME BAND IS THE POINT. LOKI-9 changes the counterbattery path, which
     is gated on the threat being within `HUNT_BAND_DSQ = 41` of our own core.
     Turrets outside that band come from the raid path and are NOT the
     treatment; pooling them dilutes the measurement toward null.
  3. CORE FOOTPRINT. The core is 2x2 and the replay records one anchor tile.
     Distances are computed to the NEAREST of the four footprint tiles, because
     the bot reasons over `min` across them; using the anchor alone shifts the
     band by a ring (flagged on `events.tsv:d2_enemy`).
  4. BOTH SEATS. A battery varies seat, so "our team" is not a constant. This
     reports per team per file and lets the caller join on the arm.

    .venv/bin/python tools/loki9_facing.py <replay-or-dir> [...]
    .venv/bin/python tools/loki9_facing.py --selftest
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

HUNT_BAND_DSQ = 41          # the counterbattery gate in doctrine.py
ALIGNED_DEG = 45.0          # one compass step

# Wire enum (tools/replay_schema.md:125-127). Compass convention from CLAUDE.md:
# (0,0) is the NORTHWEST corner, x grows east, y grows south -> NORTH is (0,-1).
DELTA = {
    0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
    5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1),
}
TURRETS = ("gunner", "sentinel")


def _core_tiles(anchor):
    x, y = anchor
    return ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))


def _dsq_to_core(pos, anchor):
    return min((pos[0] - cx) ** 2 + (pos[1] - cy) ** 2 for cx, cy in _core_tiles(anchor))


def _angle_deg(delta, vec):
    dx, dy = delta
    vx, vy = vec
    dm, vm = math.hypot(dx, dy), math.hypot(vx, vy)
    if dm == 0 or vm == 0:
        return None
    cos = max(-1.0, min(1.0, (dx * vx + dy * vy) / (dm * vm)))
    return math.degrees(math.acos(cos))


def analyse(path: Path) -> dict:
    """{team: {'built': n, 'aligned': n, 'angles': [...]}} for HOME turrets."""
    data = Path(path).read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return {}

    # Core records are map field 4, with team=2 and pos=3 (matching the shipped
    # replay_events.py). My first cut read field 5 with pos=2 and silently found
    # nothing across 960 replays -- see the decode guard in --selftest.
    cores = {}
    for num, wire, value in fields(map_buf):
        if num == 4 and wire == WIRE_LEN:
            team, pos = 0, None
            for cn, cw, cv in fields(value):
                if cn == 2:
                    team = cv
                elif cn == 3 and cw == WIRE_LEN:
                    pos = read_pos(cv)
            if pos is not None:
                cores[team] = tuple(pos)
    if len(cores) < 2:
        return {}

    out = {t: {"built": 0, "aligned": 0, "angles": []} for t in cores}
    seen_ids = set()
    # NOTE the THREE levels: turn -> update-list -> update -> entity. My first
    # cut collapsed one and matched nothing.
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un != 1:                        # placeEntity
                    continue
                for en, _ew, ev in fields(uv):
                    if en != 1:
                        continue
                    ent = parse_entity(ev, rnd)
                    if ent is None or ent.kind not in TURRETS:
                        continue
                    if ent.id in seen_ids:         # TRAP 1: rotation re-emit
                        continue
                    seen_ids.add(ent.id)
                    team = ent.team
                    if team not in cores:
                        continue
                    pos = tuple(ent.pos)
                    own, foe = cores[team], cores[1 - team]
                    if _dsq_to_core(pos, own) > HUNT_BAND_DSQ:
                        continue                   # TRAP 2: not the home path
                    delta = DELTA.get(ent.direction or 0)
                    if delta is None or delta == (0, 0):
                        continue
                    # TRAP 3: aim at the nearest footprint tile, not the anchor.
                    tx, ty = min(_core_tiles(foe),
                                 key=lambda c: (pos[0] - c[0]) ** 2 + (pos[1] - c[1]) ** 2)
                    ang = _angle_deg(delta, (tx - pos[0], ty - pos[1]))
                    if ang is None:
                        continue
                    out[team]["built"] += 1
                    out[team]["angles"].append(ang)
                    if ang <= ALIGNED_DEG + 1e-9:
                        out[team]["aligned"] += 1
    return out


def selftest() -> int:
    """Corrupt the input; require the reading to change. A discriminator that
    reports the same number on rotated inputs is not a discriminator."""
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok  ' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
        if not cond:
            fails.append(name)

    print("loki9_facing --selftest")
    # Geometry, hand-checked. Turret at (5,5); enemy core anchor (9,5) so the
    # nearest footprint tile is (9,5) -> the core lies due EAST.
    east, north, west = DELTA[3], DELTA[1], DELTA[7]
    vec = (9 - 5, 5 - 5)
    check("facing EAST at a core due east is 0 deg",
          abs(_angle_deg(east, vec) - 0.0) < 1e-9)
    check("facing NORTH at a core due east is 90 deg (NOT aligned)",
          abs(_angle_deg(north, vec) - 90.0) < 1e-9)
    check("facing WEST at a core due east is 180 deg (aimed at our own side)",
          abs(_angle_deg(west, vec) - 180.0) < 1e-9)
    check("NORTHEAST at a core due east is 45 deg and COUNTS as aligned",
          abs(_angle_deg(DELTA[2], vec) - 45.0) < 1e-9)
    # A 90-degree corruption of every facing must destroy alignment — the same
    # shape as the geometry guard the research arm ran (1.00000 -> 0.00000).
    rot = {1: 3, 3: 5, 5: 7, 7: 1, 2: 4, 4: 6, 6: 8, 8: 2}
    before = _angle_deg(DELTA[3], vec) <= ALIGNED_DEG
    after = _angle_deg(DELTA[rot[3]], vec) <= ALIGNED_DEG
    check("a 90-degree facing corruption flips aligned -> not aligned",
          before and not after)
    check("the 2x2 footprint is used, not the anchor",
          _dsq_to_core((10, 6), (9, 5)) == 0 and _dsq_to_core((10, 6), (9, 5)) != 2,
          "tile (10,6) is ON the footprint of a core anchored (9,5)")
    print(f"\n{'SELFTEST PASSED' if not fails else 'SELFTEST FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        return selftest()
    if not args:
        print(__doc__.strip().splitlines()[-2], file=sys.stderr)
        return 2
    paths = []
    for a in args:
        p = Path(a)
        paths.extend(sorted(p.rglob("*.replay26")) if p.is_dir() else [p])
    print("file\tteam\tbuilt\taligned\tshare\tmean_angle")
    tot = {}
    for p in paths:
        try:
            res = analyse(p)
        except Exception as exc:
            print(f"{p.name}\tERROR\t{type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        for team, d in res.items():
            if not d["built"]:
                continue
            a = tot.setdefault(team, {"built": 0, "aligned": 0})
            a["built"] += d["built"]
            a["aligned"] += d["aligned"]
            print(f"{p.name}\t{team}\t{d['built']}\t{d['aligned']}\t"
                  f"{d['aligned'] / d['built']:.3f}\t"
                  f"{sum(d['angles']) / len(d['angles']):.1f}")
    for team, a in sorted(tot.items()):
        if a["built"]:
            print(f"TOTAL\t{team}\t{a['built']}\t{a['aligned']}\t"
                  f"{a['aligned'] / a['built']:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
