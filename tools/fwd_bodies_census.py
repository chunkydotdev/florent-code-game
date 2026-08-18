#!/usr/bin/env python3
"""FORWARD-BODY CENSUS — how many attacker builder bots does a team park at the
enemy core AT THE SAME TIME, and what co-occurs when it runs two or more.

WHY. `_v513siegecrew`'s deviation 1 measured a SECOND forward body at −15.6pp
(local, n=90/arm, `docs/research/BUILD-REPORT-v513siegecrew-2026-08-17.md:83-105`)
with median titanium collected 380 (crew on) vs 565 (crew off) — the hypothesis
being FUNDING CONTENTION. This decoder supplies the FIELD PRIOR: does anyone out
there run ≥2 forward bodies, and when they do, what happens.

WHAT IT EMITS. One row per (replay file, team) — i.e. both sides of every game,
each measured against ITS OWN enemy geometry. Columns are documented in COLS.

DEFINITIONS (chosen to compose with the two neighbouring studies)
-----------------------------------------------------------------
* **siege zone** = tiles at d² ≤ 8 of the NEAREST tile of the enemy core's 2x2
  footprint. d²≤8 is the radius `REPLAY-STUDY-jython-inspiration-2026-08-17.md:115`
  used for "raider at d²≤8 of enemy core", so the two studies share a zone.
* **ring** = d² ≤ 2 of the footprint — the 12 tiles a body must stand on to peck
  the core or to deny a spawn seat (`FIELD-SIEGE-RESPONSE-2026-08-17.md:13`).
* **forward body** = a LIVING builder bot of the attacking team that is inside
  the zone AND strictly closer to the enemy core than to its own. Buildings are
  not bodies.
* **dweller** = a body that accumulates ≥ DWELL_MIN rounds in the zone over the
  whole game. Simultaneity counts are computed over DWELLERS ONLY.
* A round counts once per team no matter how many bodies; `fwd2_rounds` counts
  rounds where the team had **≥2 distinct dwelling builder bots** in the zone at
  the same time. That simultaneity is the whole question.

⛔ THE TWO GUARDS ABOVE ARE NOT COSMETIC — THEY ARE WHAT MAKES THE COUNT MEAN
ANYTHING ON THIS ARCHIVE. Maps run 8x8 to 30x30. On a 10x10 map the two core
footprints sit ~5 tiles apart, so a raw "d²≤8 of the enemy footprint" zone covers
a quarter of the board and **every bot on the map reads as a siege body**: the
first cut of this decoder scored a known one-raider Jython game at
`peak_bodies = 21`, which is more bots than a team can profitably own. The
own-core comparison kills the overlap; the dwell filter kills bots in transit.

THE FOUR TRAPS THIS PAYS FOR (all previously paid for in this repo)
-------------------------------------------------------------------
1. **`rotate()` re-emits `placeEntity` for an existing id** (corpus-howto trap 1)
   — only the FIRST placement of an id is a build. Guarded by `seen`.
2. **`removeEntity` carries an id only** — a body's position must be tracked
   through `moveBuilderBot` (unum 2) or every bot sits at its spawn tile forever
   and no team ever has a forward body (`tools/fwd_read.py` trap 2).
3. **A launcher throw is also a `moveBuilderBot`** — that is fine here (we want
   where the body IS, not how it got there), but it means a ferried raider
   appears in the zone with no walking path. Do not infer travel from these rows.
4. **The map buffer holds BOTH cores** — the zone is computed per team against
   the OTHER team's core, so both sides of one game are measured honestly.

USAGE
  .venv/bin/python tools/fwd_bodies_census.py <replay-dir-or-list> -o out.tsv
  .venv/bin/python tools/fwd_bodies_census.py --selftest    # both-verdicts control
"""
from __future__ import annotations

import argparse
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__))
        raise SystemExit(0)

ZONE_D2 = 8
RING_D2 = 2
DWELL_MIN = 10          # rounds in zone before a body counts as a siege body

COLS = [
    "file", "team", "mw", "mh", "core_sep_d2", "rounds", "winner", "wincond",
    "fwd1_rounds", "fwd2_rounds", "fwd3_rounds", "peak_bodies",
    "ring1_rounds", "ring2_rounds",
    "first_fwd_rnd", "first_fwd2_rnd", "distinct_fwd_bots",
    "n_builder", "n_harvester", "n_conveyor", "n_splitter", "n_barrier",
    "n_gunner", "n_sentinel", "n_launcher",
    "fwd_barrier", "fwd_turret", "fwd_launcher", "fwd_builds_all",
    "ti_collected_end", "ti_end",
    "enemy_core_death_rnd", "own_core_death_rnd",
]


def _foot(core):
    return [(core[0] + dx, core[1] + dy) for dx in (0, 1) for dy in (0, 1)]


def _dwellers(zone_tape):
    """Bot ids with >= DWELL_MIN rounds in the zone. One definition, one place —
    decode() and selftest() must not be able to drift apart."""
    tot = {}
    for ids in zone_tape:
        for i in ids:
            tot[i] = tot.get(i, 0) + 1
    return {i for i, n in tot.items() if n >= DWELL_MIN}


def _mind2(pos, foot):
    x, y = pos
    return min((x - fx) ** 2 + (y - fy) ** 2 for fx, fy in foot)


ANCHOR_SHIFT = (0, 0)   # MUTATION CONTROL: move the "enemy core" anchor off the
                        # real core. A classifier that reads the same counts
                        # against a false anchor is measuring map traffic, not
                        # sieges. Set with --anchor-shift dx,dy.


def decode(path: Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    map_buf, turn_bufs = None, []
    winner, wincond = -1, ""
    mw = mh = 0
    try:
        for num, wire, value in fields(data):
            if num == 1 and wire == WIRE_LEN:
                map_buf = value
            elif num == 3 and wire == WIRE_LEN:
                turn_bufs.append(value)
            elif num == 4 and wire == WIRE_VARINT:
                winner = value
            elif num == 6 and wire == WIRE_LEN:
                wincond = value.decode("utf-8", "replace")
    except Exception:
        return None
    if map_buf is None or not turn_bufs:
        return None

    cores = {}
    core_ids = {}
    try:
        for num, _w, value in fields(map_buf):
            if num == 1:
                mw = value
                continue
            if num == 2:
                mh = value
                continue
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
                core_ids[cid] = cteam or 0
    except Exception:
        return None
    if len(cores) != 2:
        return None

    dx, dy = ANCHOR_SHIFT
    foot = {t: _foot((cores[1 - t][0] + dx, cores[1 - t][1] + dy))
            for t in (0, 1)}                          # enemy footprint per team
    home = {t: _foot(cores[t]) for t in (0, 1)}       # own footprint per team
    core_sep = _mind2(cores[0], _foot(cores[1]))

    team_of, kind_of, pos_of = {}, {}, {}
    seen = set()
    counts = {t: dict.fromkeys(
        ("builder_bot", "harvester", "conveyor", "splitter", "barrier",
         "gunner", "sentinel", "launcher"), 0) for t in (0, 1)}
    fwd_b = {0: [0, 0, 0, 0], 1: [0, 0, 0, 0]}   # barrier, turret, launcher, all
    zone_tape = {0: [], 1: []}      # per round: frozenset of bot ids in zone
    ring_tape = {0: [], 1: []}
    ti_coll = {0: 0, 1: 0}
    ti_end = {0: 0, 1: 0}
    core_death = {0: -1, 1: -1}

    for rnd, turn_buf in enumerate(turn_bufs):
        try:
            for _n, _w, ub in fields(turn_buf):
                for unum, _uw, ubuf in fields(ub):
                    if unum == 1:                       # placeEntity
                        for en, _ew, ebuf in fields(ubuf):
                            if en != 1:
                                continue
                            e = parse_entity(ebuf, rnd)
                            if e is None:
                                continue
                            team_of[e.id] = e.team
                            kind_of[e.id] = e.kind
                            pos_of[e.id] = e.pos
                            if e.id in seen:            # TRAP 1: rotate re-emit
                                continue
                            seen.add(e.id)
                            if e.kind in counts[e.team]:
                                counts[e.team][e.kind] += 1
                            if e.kind != "builder_bot" and e.kind != "core":
                                _d = _mind2(e.pos, foot[e.team])
                                if _d <= ZONE_D2 and _d < _mind2(e.pos, home[e.team]):
                                    fwd_b[e.team][3] += 1
                                    if e.kind == "barrier":
                                        fwd_b[e.team][0] += 1
                                    elif e.kind in ("gunner", "sentinel"):
                                        fwd_b[e.team][1] += 1
                                    elif e.kind == "launcher":
                                        fwd_b[e.team][2] += 1
                    elif unum == 2:                     # moveBuilderBot
                        mid = to = None
                        for mn, _mw, mv in fields(ubuf):
                            if mn == 1:
                                mid = mv
                            elif mn == 2:
                                to = read_pos(mv)
                        if mid is not None and to is not None:
                            pos_of[mid] = to
                    elif unum == 3:                     # removeEntity
                        rid = None
                        for rn, _rw, rv in fields(ubuf):
                            if rn == 1:
                                rid = rv
                        if rid is not None:
                            if kind_of.get(rid) == "core" or rid in core_ids:
                                ct = team_of.get(rid, core_ids.get(rid))
                                if ct is not None and core_death[ct] < 0:
                                    core_death[ct] = rnd
                            pos_of.pop(rid, None)
                            kind_of.pop(rid, None)
                    elif unum == 6:                     # updatePlayers
                        for pn, _pw, pv in fields(ubuf):
                            if pn != 1:
                                continue
                            for tn, _tw, tv in fields(pv):
                                if tn not in (1, 2):
                                    continue
                                d = {}
                                for k, w2, v in fields(tv):
                                    if w2 == 0:
                                        d[k] = v
                                ti_end[tn - 1] = d.get(1, 0)
                                ti_coll[tn - 1] = d.get(4, 0)
        except Exception:
            break

        # per-round occupancy, both teams
        live_bots = {0: [], 1: []}
        for eid, p in pos_of.items():
            if kind_of.get(eid) != "builder_bot":
                continue
            t = team_of.get(eid)
            if t in (0, 1):
                live_bots[t].append((eid, p))
        for t in (0, 1):
            inz, inr = [], []
            for eid, p in live_bots[t]:
                d2 = _mind2(p, foot[t])
                if d2 > ZONE_D2:
                    continue
                # FORWARD GUARD: strictly nearer the enemy core than its own.
                if d2 >= _mind2(p, home[t]):
                    continue
                inz.append(eid)
                if d2 <= RING_D2:
                    inr.append(eid)
            zone_tape[t].append(inz)
            ring_tape[t].append(inr)

    rows = []
    for t in (0, 1):
        c = counts[t]
        dwell = _dwellers(zone_tape[t])   # SAME helper the selftest drives
        f1 = f2 = f3 = r1 = r2 = 0
        peak = 0
        first = first2 = -1
        for rnd, ids in enumerate(zone_tape[t]):
            n = sum(1 for i in ids if i in dwell)
            if n >= 1:
                f1 += 1
                if first < 0:
                    first = rnd
            if n >= 2:
                f2 += 1
                if first2 < 0:
                    first2 = rnd
            if n >= 3:
                f3 += 1
            if n > peak:
                peak = n
            nr = sum(1 for i in ring_tape[t][rnd] if i in dwell)
            if nr >= 1:
                r1 += 1
            if nr >= 2:
                r2 += 1
        rows.append([
            path.name, t, mw, mh, core_sep, len(turn_bufs), winner, wincond,
            f1, f2, f3, peak, r1, r2,
            first, first2, len(dwell),
            c["builder_bot"], c["harvester"], c["conveyor"], c["splitter"],
            c["barrier"], c["gunner"], c["sentinel"], c["launcher"],
            fwd_b[t][0], fwd_b[t][1], fwd_b[t][2], fwd_b[t][3],
            ti_coll[t], ti_end[t],
            core_death[1 - t], core_death[t],
        ])
    return rows


def _init(shift):
    # ⛔ macOS spawns worker processes, which RE-IMPORT this module and reset
    # ANCHOR_SHIFT to (0,0). A `global` set in main() never reaches them, so the
    # mutation control would silently run as the unmutated instrument and
    # "prove" the classifier survives a false anchor. Set it in the child.
    global ANCHOR_SHIFT
    ANCHOR_SHIFT = shift


def _work(p):
    try:
        return decode(Path(p))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="replay dir, or a file listing paths")
    ap.add_argument("-o", "--out", required=False)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--anchor-shift", default="0,0",
                    help="mutation control: shift the enemy-core anchor by dx,dy")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    global ANCHOR_SHIFT
    ANCHOR_SHIFT = tuple(int(v) for v in args.anchor_shift.split(","))

    tp = Path(args.target)
    if tp.is_dir():
        files = sorted(str(p) for p in tp.glob("*.replay26"))
    else:
        files = [ln.strip() for ln in tp.read_text().splitlines() if ln.strip()]
    out = open(args.out, "w") if args.out else sys.stdout
    out.write("\t".join(COLS) + "\n")
    n = 0
    with Pool(args.jobs, initializer=_init, initargs=(ANCHOR_SHIFT,)) as pool:
        for rows in pool.imap_unordered(_work, files, chunksize=16):
            if not rows:
                continue
            for r in rows:
                out.write("\t".join(str(x) for x in r) + "\n")
            n += 1
            if n % 2000 == 0:
                print(f"  {n} files", file=sys.stderr)
    if args.out:
        out.close()
    print(f"decoded {n}/{len(files)} files", file=sys.stderr)
    return 0


def classify(zone_tape, ring_tape=None):
    """Tape of per-round in-zone bot-id lists -> (arm, f1, f2, peak, n_dwellers).

    Split out of decode() so the DWELL FILTER and the simultaneity count can be
    driven to every verdict without constructing a replay.
    """
    dwell = _dwellers(zone_tape)
    f1 = f2 = peak = 0
    for ids in zone_tape:
        n = sum(1 for i in ids if i in dwell)
        f1 += n >= 1
        f2 += n >= 2
        peak = max(peak, n)
    arm = "NONE" if f1 < 20 else ("MULTI" if f2 >= 20 else "SINGLE")
    return arm, f1, f2, peak, len(dwell)


def selftest() -> int:
    """BOTH-VERDICTS CONTROL — every verdict this instrument can emit, forced.

    ⛔ WHY THIS IS NOT A PRINT STATEMENT. A classifier that has only ever
    returned one verdict has not been seen to classify, and the FIRST version of
    this decoder scored a known one-raider game at peak_bodies=21 — i.e. it had
    a failure mode that only a case designed to come out the other way exposes.
    Four cases below; each must land on a DIFFERENT verdict, and case 3 is the
    one that catches a missing dwell filter (a hundred one-round tourists must
    NOT read as a siege).
    """
    cases = [
        ("empty map",          [[] for _ in range(300)],                    "NONE"),
        ("one dweller",        [[7] for _ in range(300)],                   "SINGLE"),
        ("100 tourists",       [[i] for i in range(300)],                   "NONE"),
        ("two dwellers",       [[7, 9] for _ in range(300)],                "MULTI"),
        ("dweller + tourist",  [[7, 1000 + i] for i in range(300)],         "SINGLE"),
        ("brief overlap (<20)",[[7, 9] if r < 15 else [7]
                                for r in range(300)],                       "SINGLE"),
    ]
    bad = 0
    for lab, tape, want in cases:
        arm, f1, f2, peak, nd = classify(tape)
        ok = arm == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {lab:22s} -> {arm:6s} "
              f"(want {want:6s})  f1={f1} f2={f2} peak={peak} dwellers={nd}")
    seen = {classify(t)[0] for _, t, _ in cases}
    if len(seen) < 3:
        print(f"FAIL: only {len(seen)} distinct verdicts produced — the "
              f"classifier has not been seen to discriminate", file=sys.stderr)
        bad += 1
    print("PASS: all three verdicts forced; dwell filter rejects tourists"
          if not bad else "FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
