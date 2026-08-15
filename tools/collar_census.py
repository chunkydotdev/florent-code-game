#!/usr/bin/env python3
"""Does the collar actually seal, and does sealing stop the heal line?

LOKI-1's whole doctrine is one claim: barrier the 8 tiles orthogonally adjacent
to the enemy 2x2 core and the defender can no longer repair it, so every point
of damage becomes permanent. The design doc prices the prize precisely -- net HP
to kill a core is a stable 500-512, but raw hits landed range 28 -> 1206 across
decoded games, and that 43x spread IS the defender's heal line.

The battery says LOKI-1 kills cores (91% core-kill share vs v92's 61%). It does
NOT say the collar is why. This separates them, because the next iteration
depends on which:

  * collar seals and heals collapse  -> the doctrine works, iterate on coverage
  * collar seals and heals continue  -> the seal leaks, or heals come from
                                        inside the footprint (co-occupation)
  * collar never seals               -> LOKI-1 is winning on the forward
                                        sentinel alone and the collar is
                                        decoration; iterate on the gun instead

Per game it reports, for each side: barriers we placed ON a collar seat of the
ENEMY core, how many of the 8 seats were ever held, and the enemy's own
BuilderHeal actions targeting its core footprint (Update field 15) before and
after the seal.

Read-only over a directory of replays (use `mech_battery.py --keep-replays`).

Usage:
  .venv/bin/python tools/collar_census.py scratchpad/loki2/replays
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))


def collar_seats(core):
    """The 8 tiles orthogonally adjacent to a 2x2 footprint at `core` (NW corner)."""
    foot = {(core[0] + dx, core[1] + dy) for dx in (0, 1) for dy in (0, 1)}
    out = set()
    for fx, fy in foot:
        for dx, dy in CARD:
            t = (fx + dx, fy + dy)
            if t not in foot:
                out.add(t)
    return out


def decode(path: Path):
    name = path.name
    arm = "variant" if name.startswith("variant__") else "control"
    our = 0 if name.endswith("__a.replay26") else 1
    try:
        data = path.read_bytes()
    except OSError:
        return None
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    cores = {}
    for num, _w, value in fields(map_buf):
        if num != 4:
            continue
        cid = cteam = cpos = None
        for cn, _cw, cv in fields(value):
            if cn == 1:
                cid = cv
            elif cn == 2:
                cteam = cv
            elif cn == 3:
                cpos = read_pos(cv)
        if cid is not None and cpos is not None:
            cores[cteam or 0] = cpos
    if len(cores) != 2:
        return None
    enemy = 1 - our
    seats = collar_seats(cores[enemy])
    foot = {(cores[enemy][0] + dx, cores[enemy][1] + dy) for dx in (0, 1) for dy in (0, 1)}

    team_of, kind_of = {}, {}
    pos_of = {}
    held = {}                       # seat -> round first held by OUR building
    seal_round = None
    heals_before = heals_after = 0
    # DOSE-RESPONSE. "Games fully sealed" scores our EFFORT; what decides a
    # siege is how much healing we actually deny, and the rush does not need a
    # perfect 12/12 lock -- it needs the heal detail suppressed for the ~28
    # rounds a sentinel line needs through 500 HP. So bucket every round by how
    # many of the 8 orthogonal seats we deny that round, and record the enemy's
    # own core-heal actions in it. A monotone curve is the claim; a flat one
    # refutes the doctrine regardless of how many seats we hold.
    dose = {}                       # denied-count -> [rounds, enemy core heals]
    for rnd, turn_buf in enumerate(turn_bufs):
        round_heals = [0]
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in team_of:
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        if (e.team == our and e.kind != "builder_bot"
                                and e.pos in seats and e.pos not in held):
                            held[e.pos] = rnd
                            if len(held) == len(seats) and seal_round is None:
                                seal_round = rnd
                elif unum == 2:                        # moveBuilderBot
                    mid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            mid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if mid is not None and to is not None:
                        pos_of[mid] = to
                elif unum == 3:                        # removeEntity
                    rid = None
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rid = rv
                    if rid is not None:
                        pos_of.pop(rid, None)
                elif unum == 15:                       # builderHeal
                    hid = tgt = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            hid = hv
                        elif hn == 2:
                            tgt = read_pos(hv)
                    if hid is None or tgt is None:
                        continue
                    if team_of.get(hid) == enemy and tgt in foot:
                        if seal_round is None:
                            heals_before += 1
                        else:
                            heals_after += 1
                        round_heals[0] += 1
        # Denied = an ORTHOGONAL heal seat occupied by anything of ours this
        # round, body or building. A body denies exactly as well as a barrier
        # (verified: an enemy body makes can_spawn False, and a builder cannot
        # heal from a tile it is not standing on).
        ours_at = {pos_of[i] for i in pos_of if team_of.get(i) == our}
        denied = len(seats & ours_at)
        d = dose.setdefault(denied, [0, 0])
        d[0] += 1
        d[1] += round_heals[0]
    return (arm, len(seats), len(held), seal_round is not None,
            min(held.values()) if held else None,
            heals_before, heals_after, len(turn_bufs), dose)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("replays")
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()
    files = sorted(Path(args.replays).glob("*.replay26"))
    print(f"{len(files)} replays", file=sys.stderr)
    if not files:
        return 1
    agg = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    firsts = defaultdict(list)
    dosed = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    with Pool(args.jobs) as pool:
        for r in pool.map(decode, files):
            if r is None:
                continue
            arm, nseats, nheld, sealed, first, hb, ha, turns, dose = r
            for k, (rr, hh) in dose.items():
                d = dosed[arm][k]
                d[0] += rr
                d[1] += hh
            a = agg[arm]
            a[0] += 1
            a[1] += nheld
            a[2] += 1 if sealed else 0
            a[3] += hb
            a[4] += ha
            a[5] += turns
            if first is not None:
                firsts[arm].append(first)
    print("\nCOLLAR CENSUS — did we hold the 8 tiles the enemy core must heal from?")
    print(f"  {'arm':9s} {'games':>6s} {'seats held/game':>16s} {'games fully sealed':>19s} "
          f"{'first seat @rnd':>16s} {'enemy core heals: pre-seal':>27s} {'post-seal':>10s}")
    for arm in ("control", "variant"):
        g, held, sealed, hb, ha, turns = agg[arm]
        if not g:
            continue
        f = firsts[arm]
        med = sorted(f)[len(f) // 2] if f else float("nan")
        print(f"  {arm:9s} {g:6d} {held / g:16.2f} {sealed:19d} {med:16.0f} "
              f"{hb:27d} {ha:10d}")
    print("\nDOSE-RESPONSE — the metric that actually decides a siege.")
    print("  Every round bucketed by how many of the enemy's 8 heal seats WE deny that")
    print("  round (body or building), against their own core-heal actions in it.")
    print(f"  {'arm':9s} {'seats denied':>13s} {'rounds':>9s} {'enemy core heals':>17s} {'heals / 100 rnd':>16s}")
    for arm in ("control", "variant"):
        if arm not in dosed:
            continue
        for k in sorted(dosed[arm]):
            rr, hh = dosed[arm][k]
            if rr < 50:
                continue
            print(f"  {arm:9s} {k:13d} {rr:9d} {hh:17d} {100 * hh / rr:16.2f}")
    print("\n  Monotone fall = the doctrine works and partial denial is worth building.")
    print("  Flat = the collar is decoration and LOKI-1 wins on the forward sentinel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
