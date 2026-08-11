#!/usr/bin/env python3
"""LOKI-16 MECHANISM read: enemy-spawn-ring occupancy, from archived replays.

⭐ THIS IS THE BLESSED RING DECODER. `tools/ring_retention.py` IS THE BROKEN ONE
AND IT REFUSES TO RUN -- read its docstring before reaching for it.

PROVENANCE (2026-08-11 adjudication, docs/research/ADJUDICATION-ring-occupancy-
decoders-2026-08-11.md): validated on SEVEN forced-answer synthetic replays
written as real engine protobuf, covering floor AND ceiling, with both decoders
imported unmodified. The cell that separates them: a BARRIER on the ring with
zero builder-rounds must read 0.000 -- this file reads 0.000, ring_retention
reads 0.900.

WHY IT LIVES HERE NOW: it was UNTRACKED in scratchpad/ while producing
LOKI-16b's +0.164 read-out AND serving as the decoder for LOKI-19's falsifier --
the only band in that prereg that may be written plainly. Two resolvable results
resting on a file one `rm -rf scratchpad/` from gone, while a WRONG decoder sat
in tools/ with a passing selftest. That is the LOKI-17 shape exactly: the
artefact said one thing, the record said another, and nothing made them meet.

READ-ONLY. Downloads nothing. Consumes replay_archive/<matchId>_game_<N>.replay26
plus <matchId>.meta.json (for the seat, which is NEVER assumed).

⛔⛔ THE TWO EPISODE SERIES ARE NOT `hold_any` AND `hold_pinned`. READ THIS
BEFORE QUOTING EITHER — the names were matched to the series BY POSITION, by
three lanes, over hours, and nobody checked:

    per_bot_tile[(eid, p)]  -> "tile_episodes"   same bot, SAME tile
                                                 == hold_pinned  ✅ correct
    per_bot_any[eid]        -> "bot_episodes"    same bot, ANY ring tile
                                                 != hold_any     ⛔ A THIRD THING

`hold_any` as the 2026-08-11 adjudication defines it — *longest unbroken run with
>=1 of OUR BUILDERS anywhere on the ring* — **IS NOT COMPUTED BY THIS FILE AT
ALL.** The RELAY selftest cell forces the distinction: bot A on tile T rounds
0-49, bot B on the SAME tile 50-99 gives true `hold_any` = 100, while
`bot_episodes` maxes at 50 and `tile_episodes` == [50, 50]. **No series here
returns 100.**

⇒ LOKI-16b's PRIMARY is `tile_episodes` = `hold_pinned` = +0.164, and that is
  correct and published. The +0.137 that circulated as "hold_any" is
  `bot_episodes` and must never be quoted under that name.
⇒ `docs/research/ADJUDICATION-ring-occupancy-decoders-2026-08-11.md` still tells
  a reader to "name it hold_any or hold_pinned" for a tool implementing neither
  under those names. The correction lives in
  `docs/prereg/PREREG-loki16b-ring-retention-2026-08-10.md` (CORRECTION 1).
  **If you arrived here from the adjudication, that document is older than this
  comment.**

RING DEFINITION -- the same 12 tiles the bot itself derives
(bots/_v133loki16/eco.py: heal_seats + core_corners, clipped to map bounds):
a Core's `position` is the NW corner of its 2x2 footprint {(x,y),(x+1,y),
(x,y+1),(x+1,y+1)}; the ring is the 8 orthogonal neighbours of that footprint
plus the 4 diagonal corners.

OCCUPANCY = END-OF-ROUND SNAPSHOT. A body counts for round r if it is standing
on a ring tile after every update in turns[r] has been applied. That is
"standing, not placed-then-lost" by construction.

Usage: python3 tools/ring_read.py scratchpad/arm_loki16.txt [more.txt ...]
       python3 tools/ring_read.py --selftest

⭐ THE ADJUDICATION'S CELLS ARE NOW RE-EXECUTABLE: `--selftest` rebuilds them as
real engine protobuf and drives the UNMODIFIED `decode()` over them (see the
SELFTEST block at the foot of this file, including the declared mutant that must
make it FAIL). Gate on the printed `RING_READ_SELFTEST: PASS` token, not on `$?`.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos, WIRE_LEN  # noqa: E402

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"   # OpenSverige
ARCHIVE = ROOT / "replay_archive"


def ids_from_file(p: Path) -> list[str]:
    out = []
    for line in p.read_text().splitlines():
        if '"matchId"' in line:
            out.append(json.loads(line[line.index("{"):])["matchId"])
    return out


def ring_tiles(anchor, w, h):
    x, y = anchor
    seats = [(x, y - 1), (x + 1, y - 1), (x + 2, y), (x + 2, y + 1),
             (x + 1, y + 2), (x, y + 2), (x - 1, y + 1), (x - 1, y)]
    corners = [(x - 1, y - 1), (x + 2, y - 1), (x - 1, y + 2), (x + 2, y + 2)]
    return frozenset(t for t in seats + corners
                     if 0 <= t[0] < w and 0 <= t[1] < h)


def decode(path: Path, our_team: int):
    """-> dict of per-game ring metrics, or None if unparseable."""
    data = path.read_bytes()
    map_buf, turn_bufs, winner = None, [], None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == 0:
            winner = value
    if map_buf is None:
        return None
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(2, 0), read_pos(d[3])))
    enemy = [pos for team, pos in cores if team != our_team]
    if len(enemy) != 1:
        return None
    ring = ring_tiles(enemy[0], w, h)

    pos_of, team_of, kind_of = {}, {}, {}
    # per-round series
    n_bodies = []                 # our builder bots standing on enemy ring
    per_bot_tile = defaultdict(list)   # (botid, tile) -> [rounds]
    per_bot_any = defaultdict(list)    # botid -> [rounds on any ring tile]
    bld_tiles_per_round = []      # our BUILDINGS on distinct enemy ring tiles

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:            # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                elif unum == 2:          # moveBuilderBot
                    bid, to = None, None
                    for mn, mw_, mv in fields(ubuf):
                        if mn == 1:
                            bid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if bid is not None and to is not None:
                        pos_of[bid] = to
                elif unum == 3:          # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            pos_of.pop(rv, None)
        # --- end-of-round snapshot ---
        c = 0
        btiles = set()
        for eid, p in pos_of.items():
            if team_of.get(eid) != our_team or p not in ring:
                continue
            if kind_of.get(eid) == "builder_bot":
                c += 1
                per_bot_tile[(eid, p)].append(rnd)
                per_bot_any[eid].append(rnd)
            elif kind_of.get(eid) not in (None, "core"):
                btiles.add(p)
        n_bodies.append(c)
        bld_tiles_per_round.append(len(btiles))

    def episodes(series_map):
        out = []
        for _k, rounds in series_map.items():
            run = 1
            for a, b in zip(rounds, rounds[1:]):
                if b == a + 1:
                    run += 1
                else:
                    out.append(run)
                    run = 1
            out.append(run)
        return out

    rounds = len(turn_bufs)
    occupied = [r for r, c in enumerate(n_bodies) if c > 0]
    return {
        "rounds": rounds,
        "winner": winner,
        "ring_size": len(ring),
        "seat_rounds": sum(n_bodies),
        "cover_rounds": len(occupied),
        "coverage": len(occupied) / rounds if rounds else 0.0,
        "first_arrival": occupied[0] if occupied else None,
        "cov_lt250": (len([r for r in occupied if r < 250]) / min(250, rounds)
                      if rounds else 0.0),
        "simul_hist": Counter(n_bodies),
        "max_simul": max(n_bodies) if n_bodies else 0,
        "tile_episodes": episodes(per_bot_tile),
        "bot_episodes": episodes(per_bot_any),
        "bld_ring_tiles_mean": (sum(bld_tiles_per_round) / rounds) if rounds else 0.0,
        "bld_ring_tiles_end": bld_tiles_per_round[-1] if bld_tiles_per_round else 0,
    }


def run_arm(fp: Path):
    mids = ids_from_file(fp)
    games, per_opp = [], defaultdict(list)
    seat_check = []
    for mid in mids:
        meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
        we_are_a = meta["teamAId"] == OUR_TEAM_ID
        assert we_are_a or meta["teamBId"] == OUR_TEAM_ID, f"{mid}: not our match"
        our_team = 0 if we_are_a else 1
        opp = meta["teamBName"] if we_are_a else meta["teamAName"]
        ourver = meta["teamAVersion"] if we_are_a else meta["teamBVersion"]
        oppver = meta["teamBVersion"] if we_are_a else meta["teamAVersion"]
        wins_a = 0
        n = 0
        for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
            g = decode(rp, our_team)
            if g is None:
                print(f"  !! unparseable {rp.name}", file=sys.stderr)
                continue
            n += 1
            if g["winner"] == 0:
                wins_a += 1
            g.update(opp=opp, seat="A" if we_are_a else "B", mid=mid,
                     ourver=ourver, oppver=oppver)
            games.append(g)
            per_opp[opp].append(g)
        # VALIDATION: replay-side winner tally must reproduce the platform's
        # scoreA. If seat mapping (replay Team 0 == platform teamA) were wrong
        # this is where it breaks.
        seat_check.append((mid, wins_a, meta["scoreA"], n, meta["scoreB"]))
    return games, per_opp, seat_check


def pct(xs):
    xs = sorted(xs)
    if not xs:
        return "n/a"
    q = lambda f: xs[min(len(xs) - 1, int(f * len(xs)))]
    return (f"n={len(xs)} min={xs[0]} p25={q(.25)} med={statistics.median(xs):.0f} "
            f"p75={q(.75)} p90={q(.90)} max={xs[-1]} mean={statistics.mean(xs):.1f}")


def report(label, games, per_opp, seat_check):
    print(f"\n{'='*78}\n=== {label}  (n={len(games)} games, "
          f"{len(seat_check)} matches) ===\n{'='*78}")
    bad = [s for s in seat_check if s[1] != s[2] or s[3] != 5]
    print(f"  SEAT/PARSE VALIDATION: replay winner tally == platform scoreA in "
          f"{len(seat_check)-len(bad)}/{len(seat_check)} matches"
          + ("" if not bad else f"  ** MISMATCH: {bad}"))
    vers = Counter((g["ourver"], g["opp"], g["oppver"], g["seat"]) for g in games)
    print("  our_ver / opponent / opp_ver / seat  -> games")
    for k, v in sorted(vers.items()):
        print(f"    v{k[0]:<4} {k[1]:<22} oppv{k[2]:<4} seat {k[3]}  {v}")

    occ = [g for g in games if g["first_arrival"] is not None]
    print(f"\n  -- TREATMENT OCCURRENCE (measured BEFORE retention) --")
    print(f"    games with >=1 of our bodies STANDING on an enemy ring tile "
          f"at end of any round: {len(occ)}/{len(games)} = {len(occ)/len(games):.1%}")
    fa = [g["first_arrival"] for g in occ]
    print(f"    first-arrival round: {pct(fa)}")
    gl = [g["rounds"] for g in games]
    print(f"    game length (rounds): {pct(gl)}")

    print(f"\n  -- RETENTION --")
    cov = [g["coverage"] for g in games]
    print(f"    ring-body COVERAGE (fraction of game rounds with >=1 body): "
          f"mean {statistics.mean(cov):.3f}  median {statistics.median(cov):.3f}"
          f"  min {min(cov):.3f} max {max(cov):.3f}")
    cov250 = [g["cov_lt250"] for g in games]
    print(f"    coverage restricted to rounds <250: mean "
          f"{statistics.mean(cov250):.3f}  median {statistics.median(cov250):.3f}")
    sr = [g["seat_rounds"] for g in games]
    print(f"    SEAT-ROUNDS per game (sum over rounds of bodies on ring): {pct(sr)}")
    te = [e for g in games for e in g["tile_episodes"]]
    print(f"    per-(bot,tile) HOLD EPISODES, consecutive rounds: {pct(te)}")
    be = [e for g in games for e in g["bot_episodes"]]
    print(f"    per-bot ring episodes (any ring tile), consec rounds: {pct(be)}")
    longest = [max(g["tile_episodes"]) if g["tile_episodes"] else 0 for g in games]
    print(f"    LONGEST single-tile hold per game: {pct(longest)}")
    lfrac = [(max(g["tile_episodes"]) / g["rounds"]) if g["tile_episodes"] else 0.0
             for g in games]
    print(f"    longest single-tile hold / game length: mean "
          f"{statistics.mean(lfrac):.3f} median {statistics.median(lfrac):.3f}")

    print(f"\n  -- SIMULTANEITY (prereg spec is ONE body) --")
    hist = Counter()
    tot = 0
    for g in games:
        hist += g["simul_hist"]
        tot += g["rounds"]
    for k in sorted(hist):
        print(f"    {k} bodies on ring: {hist[k]:>7} rounds = {hist[k]/tot:6.2%}")
    occ_rounds = tot - hist[0]
    if occ_rounds:
        mean_when_occ = sum(k * v for k, v in hist.items()) / occ_rounds
        print(f"    mean bodies GIVEN >=1 present: {mean_when_occ:.2f}")
    ms = [g["max_simul"] for g in games]
    print(f"    max simultaneous bodies per game: {pct(ms)}")

    print(f"\n  -- COST SIDE (prereg: body-for-barrier trade) --")
    bt = [g["bld_ring_tiles_end"] for g in games]
    print(f"    distinct enemy-ring tiles holding OUR building at game end: {pct(bt)}")
    btm = [g["bld_ring_tiles_mean"] for g in games]
    print(f"    ...time-averaged over the game: mean {statistics.mean(btm):.2f}")

    print(f"\n  -- PER OPPONENT --")
    print(f"    {'opponent':<24}{'n':>4}{'occ':>7}{'cover':>8}{'seatR':>8}"
          f"{'medEp':>7}{'maxSim':>8}")
    for opp in sorted(per_opp):
        gs = per_opp[opp]
        o = len([g for g in gs if g["first_arrival"] is not None])
        c = statistics.mean(g["coverage"] for g in gs)
        s = statistics.median(g["seat_rounds"] for g in gs)
        eps = [e for g in gs for e in g["tile_episodes"]]
        m = statistics.median(eps) if eps else 0
        sim = statistics.mean(g["max_simul"] for g in gs)
        print(f"    {opp:<24}{len(gs):>4}{o/len(gs):>7.0%}{c:>8.3f}{s:>8.0f}"
              f"{m:>7.0f}{sim:>8.2f}")
    return {"cov": statistics.mean(cov), "cov250": statistics.mean(cov250)}


# =============================================================================
# SELFTEST -- ADDITIVE ONLY. Nothing above this line was touched when it landed.
# =============================================================================
#
# WHY IT EXISTS. The correctness argument for this file lived only as PROSE in
# docs/research/ADJUDICATION-ring-occupancy-decoders-2026-08-11.md: seven
# forced-answer cells, run once, by an agent, in a scratch dir that no longer
# exists. A correctness argument that cannot be re-executed is a CLAIM, not a
# CONTROL -- and this file produced LOKI-16b's committed read-out and is the
# decoder for LOKI-19's falsifier.
#
# HOW IT WORKS, AND THE ONE CONSTRAINT THAT SHAPED IT. `decode()` produced a
# number already committed to a pre-registration, so it MUST NOT be refactored
# to make it testable -- adding seams risks silently moving that number. So the
# selftest synthesises `.replay26` files as REAL ENGINE PROTOBUF (schema:
# tools/replay_schema.md) and calls the EXISTING `decode(path, our_team)`
# unmodified. What follows is a protobuf WRITER for fixtures; the reader above
# is untouched.
#
# THE DECLARED MUTANT (docs/research/SPEC-mutation-harness-2026-08-11.md,
# fixture #1). Delete the entity-kind condition from the end-of-round snapshot
# in `decode()` -- i.e. let every entity of ours count as a body, which is
# exactly the defect that made `tools/ring_retention.py` read 0.900 where the
# forced answer is 0.000. Apply it to a SCRATCH COPY (never to tools/) and the
# BARRIER_ONLY cell below MUST FAIL. Recipe, and it is the acceptance
# criterion for this selftest:
#
#   d=$(mktemp -d); mkdir -p $d/tools
#   cp tools/replay_census.py $d/tools/
#   sed 's/^            if kind_of\.get.*$/            if True:/' \
#       tools/ring_read.py > $d/tools/ring_read.py
#   python3 $d/tools/ring_read.py --selftest    # must print RING_READ_SELFTEST: FAIL
#
# A selftest that passes on both the real file and the mutant is worthless --
# that is precisely the defect `ring_retention.py --selftest` had (it passed
# while the occupancy rule was wrong, because it only ever tested the ring
# GEOMETRY).

_SF_KIND_FIELD = {"builder_bot": 10, "conveyor": 11, "splitter": 12,
                  "harvester": 15, "barrier": 18, "core": 20, "gunner": 21,
                  "sentinel": 22, "launcher": 24}


def _sf_varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b, n = n & 0x7F, n >> 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _sf_v(num: int, value: int) -> bytes:            # varint field
    return _sf_varint(num << 3) + _sf_varint(value)


def _sf_l(num: int, payload: bytes) -> bytes:        # length-delimited field
    return _sf_varint(num << 3 | 2) + _sf_varint(len(payload)) + payload


def _sf_pos(xy) -> bytes:                            # Pos{x=1,y=2}
    return _sf_v(1, xy[0]) + _sf_v(2, xy[1])


def _sf_entity(eid: int, team: int, xy, kind: str, hp: int = 40) -> bytes:
    """Entity{id=1,team=2,position=3,hp=4,maxHp=5,<kind>=K}."""
    body = (_sf_v(1, eid) + _sf_v(2, team) + _sf_l(3, _sf_pos(xy))
            + _sf_v(4, hp) + _sf_v(5, hp))
    # Barrier is an EMPTY message -> zero-length submessage on the wire
    # (tools/replay_schema.md); everything else carries at least one scalar.
    sub = b"" if kind == "barrier" else _sf_v(1, 0)
    return body + _sf_l(_SF_KIND_FIELD[kind], sub)


def _sf_place(entity: bytes) -> bytes:               # Update{placeEntity{entity}}
    return _sf_l(1, _sf_l(1, entity))


def _sf_move(eid: int, xy) -> bytes:                 # Update{moveBuilderBot{id,to}}
    return _sf_l(2, _sf_v(1, eid) + _sf_l(2, _sf_pos(xy)))


def _sf_remove(eid: int) -> bytes:                   # Update{removeEntity{id}}
    return _sf_l(3, _sf_v(1, eid))


def _sf_turn(updates) -> bytes:                      # Turn{repeated Update=1}
    return b"".join(_sf_l(1, u) for u in updates)


def _sf_replay(w, h, cores, turns, winner=1, walls=()) -> bytes:
    """Replay{map=1, turns=3(repeated), winner=4, winCondition=6}.

    cores: [(id, team, (x, y))]; turns: [[update_bytes, ...], ...] (one per
    round, turns[i] IS round i). `walls` are (x, y) tiles written as ENV_WALL.
    """
    grid = [[0] * w for _ in range(h)]
    for x, y in walls:
        grid[y][x] = 1
    rows = b"".join(_sf_l(3, _sf_l(1, b"".join(_sf_varint(t) for t in row)))
                    for row in grid)
    cbuf = b"".join(_sf_l(4, _sf_v(1, cid) + _sf_v(2, team) + _sf_l(3, _sf_pos(xy)))
                    for cid, team, xy in cores)
    mp = _sf_v(1, w) + _sf_v(2, h) + rows + cbuf
    return (_sf_l(1, mp) + b"".join(_sf_l(3, _sf_turn(t)) for t in turns)
            + _sf_v(4, winner) + _sf_l(6, b"core_destroyed"))


# --- fixture geometry (identical to the adjudication's) ----------------------
# 12x12 all-EMPTY map, 100 rounds. Our core id=1 team=0 at (1,1); enemy core
# id=2 team=1 at (8,8). Enemy ring is fully in bounds and is these 12 tiles:
#   (8,7)(9,7)(10,8)(10,9)(9,10)(8,10)(7,9)(7,8) + (7,7)(10,7)(7,10)(10,10)
_SF_W = _SF_H = 12
_SF_N = 100
_SF_CORES = [(1, 0, (1, 1)), (2, 1, (8, 8))]
_SF_T = (8, 7)          # a ring tile
_SF_T2 = (9, 7)         # a second ring tile, orthogonally adjacent to _SF_T
_SF_OFF = (8, 6)        # ONE cardinal step north of _SF_T, off the ring
_SF_FAR = (2, 2)        # min d^2 to any ring tile >= 25: no contact possible


def _sf_blank_turns(n=_SF_N):
    return [[] for _ in range(n)]


def _sf_cells():
    """-> [(name, why_forced, replay_bytes, our_team, [(label, forced, key)])]

    `key` is a callable on decode()'s dict. Every forced answer is forced BY
    CONSTRUCTION -- it is arithmetic on the fixture, never a stored figure.
    """
    cells = []

    def add(name, why, turns, our_team, checks, cores=None, walls=()):
        cells.append((name, why,
                      _sf_replay(_SF_W, _SF_H, cores or _SF_CORES, turns,
                                 walls=walls),
                      our_team, checks))

    # 1. FLOOR -- no contact. Our sole builder never approaches the ring.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_FAR, "builder_bot"))]
    add("FLOOR_no_contact",
        "sole builder parked at (2,2); min d^2 to any ring tile >= 25",
        t, 0,
        [("coverage", 0.0, lambda g: g["coverage"]),
         ("seat_rounds", 0, lambda g: g["seat_rounds"]),
         ("first_arrival", None, lambda g: g["first_arrival"]),
         ("len(tile_episodes)", 0, lambda g: len(g["tile_episodes"])),
         ("max_simul", 0, lambda g: g["max_simul"])])

    # 2. BARRIER_ONLY -- THE CELL THAT SEPARATES THE TWO DECODERS.
    # One of OUR BARRIERS on ring tile (7,7) from r10 to r99, and ZERO
    # builder-bot rounds on the ring. ring_retention.py reads 0.900 here.
    # The cost-side assertions are load-bearing: they prove the barrier IS
    # parsed and IS on the ring, so 0.000 occupancy is the KIND FILTER doing
    # its job and not the fixture failing to place anything.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_FAR, "builder_bot"))]
    t[10] = [_sf_place(_sf_entity(20, 0, (7, 7), "barrier", hp=30))]
    add("BARRIER_ONLY",
        "our barrier on ring tile (7,7) r10-99 (90 rounds); zero builder-rounds "
        "on the ring",
        t, 0,
        [("coverage", 0.0, lambda g: g["coverage"]),
         ("seat_rounds", 0, lambda g: g["seat_rounds"]),
         ("len(tile_episodes)", 0, lambda g: len(g["tile_episodes"])),
         # cost side: the barrier is seen, on 1 distinct ring tile, 90/100 rounds
         ("bld_ring_tiles_end", 1, lambda g: g["bld_ring_tiles_end"]),
         ("bld_ring_tiles_mean", 0.9, lambda g: g["bld_ring_tiles_mean"])])

    # 3. CEILING -- one builder pinned on one ring tile for all 100 rounds.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    add("CEILING_pinned",
        "one builder placed on (8,7) at r0, never moves, never removed: 100/100",
        t, 0,
        [("coverage", 1.0, lambda g: g["coverage"]),
         ("seat_rounds", 100, lambda g: g["seat_rounds"]),
         ("first_arrival", 0, lambda g: g["first_arrival"]),
         ("max(tile_episodes)", 100, lambda g: max(g["tile_episodes"])),
         ("max(bot_episodes)", 100, lambda g: max(g["bot_episodes"])),
         ("max_simul", 1, lambda g: g["max_simul"])])

    # 4. RELAY -- pins the granularity the adjudication's SECOND FINDING names.
    # Bot A holds tile T for r0-49; at r50 A is removed and bot B takes the
    # SAME tile T for r50-99, with no gap. Coverage (>=1 body on the ring in a
    # round) is unbroken at 1.000, but no (bot,tile) pair and no single bot
    # exceeds 50. THIS IS WHY `hold_any` AND `hold_pinned` ARE NOT THE SAME
    # NUMBER, and why a document must name which one it quotes.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    t[50] = [_sf_remove(10), _sf_place(_sf_entity(11, 0, _SF_T, "builder_bot"))]
    add("RELAY_same_tile_two_bots",
        "bot A on (8,7) r0-49, bot B on the SAME tile r50-99, no gap",
        t, 0,
        [("coverage", 1.0, lambda g: g["coverage"]),
         ("cover_rounds", 100, lambda g: g["cover_rounds"]),
         ("seat_rounds", 100, lambda g: g["seat_rounds"]),
         ("max_simul", 1, lambda g: g["max_simul"]),
         ("max(tile_episodes)", 50, lambda g: max(g["tile_episodes"])),
         ("sorted(tile_episodes)", [50, 50], lambda g: sorted(g["tile_episodes"])),
         ("max(bot_episodes)", 50, lambda g: max(g["bot_episodes"]))])

    # 4b. WALK -- separates bot_episodes from tile_episodes in the OTHER
    # direction. ONE bot, two ring tiles, no gap: same-bot ring residency is
    # 100 while the longest same-tile hold is 70. Without this cell the two
    # series are indistinguishable on every cell above.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    t[30] = [_sf_move(10, _SF_T2)]
    add("WALK_one_bot_two_tiles",
        "one bot on (8,7) r0-29 then one cardinal step to (9,7) r30-99",
        t, 0,
        [("coverage", 1.0, lambda g: g["coverage"]),
         ("sorted(tile_episodes)", [30, 70], lambda g: sorted(g["tile_episodes"])),
         ("max(bot_episodes)", 100, lambda g: max(g["bot_episodes"]))])

    # 5a. TEAM control -- an ENEMY builder sitting on the ENEMY ring all game.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 1, _SF_T, "builder_bot"))]
    add("TEAM_enemy_bot_on_enemy_ring",
        "a TEAM-1 builder pinned on (8,7) r0-99 while we are team 0",
        t, 0,
        [("coverage", 0.0, lambda g: g["coverage"]),
         ("seat_rounds", 0, lambda g: g["seat_rounds"])])

    # 5b. SEAT control -- the CEILING bytes read from the opposite seat. Same
    # file, our_team=1: "the enemy ring" is now the ring of the team-0 core at
    # (1,1) and the team-0 builder on (8,7) is theirs, not ours.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    add("SEAT_ceiling_bytes_other_seat",
        "CEILING fixture decoded with our_team=1: ring moves to (1,1) and the "
        "body is the enemy's",
        t, 1,
        [("coverage", 0.0, lambda g: g["coverage"]),
         ("ring_size", 12, lambda g: g["ring_size"])])

    # 6. MID -- hand-countable partial. On (8,7) for r0-39 (40 rounds), then
    # ONE cardinal step north off the ring at r40 and never back.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    t[40] = [_sf_move(10, _SF_OFF)]
    add("MID_40_of_100",
        "on (8,7) r0-39 then steps to (8,6), off-ring, for r40-99: exactly 40/100",
        t, 0,
        [("coverage", 0.4, lambda g: g["coverage"]),
         ("cover_rounds", 40, lambda g: g["cover_rounds"]),
         ("seat_rounds", 40, lambda g: g["seat_rounds"]),
         ("max(tile_episodes)", 40, lambda g: max(g["tile_episodes"]))])

    # 7. LATENT id-swap -- byte-identical to CEILING except the two cores'
    # `id` values are reversed against their `team`. CorePosition field 1 is
    # the ID and field 2 is the TEAM; keying on field 1 (ring_retention.py's
    # defect) returns 0.000 where the forced answer is 1.000.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    add("LATENT_core_id_swap",
        "CEILING with core ids reversed vs teams: id=2/team=0 at (1,1), "
        "id=1/team=1 at (8,8)",
        t, 0,
        [("coverage", 1.0, lambda g: g["coverage"]),
         ("ring_size", 12, lambda g: g["ring_size"])],
        cores=[(2, 0, (1, 1)), (1, 1, (8, 8))])

    # 8. CLIPPED ring -- enemy core in the NW corner at (0,0): 5 of the 12 ring
    # tiles are in bounds. Guards the bounds clip in ring_tiles(), and the
    # stratum the adjudication says to stratify on.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (2, 0), "builder_bot"))]
    add("CLIPPED_corner_ring",
        "enemy core at (0,0): ring clipped to 5 in-bounds tiles; our bot on "
        "(2,0), one of them, all game",
        t, 0,
        [("ring_size", 5, lambda g: g["ring_size"]),
         ("coverage", 1.0, lambda g: g["coverage"])],
        cores=[(1, 0, (9, 9)), (2, 1, (0, 0))])

    # 9. WALL inside the ring -- the agreed definition says do NOT drop WALL
    # tiles from the ring (a wall can never hold a body, so dropping one only
    # changes the reported ring size and therefore the stratum). Ring tile
    # (7,7) is ENV_WALL here and the ring must still be 12.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, _SF_T, "builder_bot"))]
    add("WALL_in_ring_not_dropped",
        "ring tile (7,7) is ENV_WALL; ring size must stay 12 (agreed definition)",
        t, 0,
        [("ring_size", 12, lambda g: g["ring_size"]),
         ("coverage", 1.0, lambda g: g["coverage"])],
        walls=[(7, 7)])

    return cells


def _sf_eq(forced, observed) -> bool:
    if isinstance(forced, float) or isinstance(observed, float):
        try:
            return abs(float(forced) - float(observed)) < 1e-9
        except (TypeError, ValueError):
            return False
    return forced == observed


def selftest() -> int:
    """Drive the UNMODIFIED decode() over forced-answer synthetic replays.

    Returns a process exit code and prints a terminal
    `RING_READ_SELFTEST: PASS|FAIL` token -- gate on the TOKEN, not on `$?`,
    because `$?` behind a pipe is the pipe's status.
    """
    import tempfile
    from replay_census import Replay  # independent parser: fixture cross-check

    tmp = Path(tempfile.mkdtemp(prefix="ring_read_selftest_"))
    print("RING_READ SELFTEST -- forced-answer cells, real engine protobuf, "
          "decode() unmodified")
    print(f"  fixtures: {tmp}")
    n_ok = n_fail = 0
    fails = []
    cells = _sf_cells()
    for name, why, blob, our_team, checks in cells:
        path = tmp / f"{name}.replay26"
        path.write_bytes(blob)
        print(f"\n  CELL {name}  (our_team={our_team})\n       forced because: {why}")
        # Fixture self-check: the bytes must also parse under the
        # independently-written replay_census parser. A fixture only this file
        # can read proves nothing about this file.
        try:
            rp = Replay(path, track_flow=False)
            assert rp.rounds == _SF_N, f"rounds {rp.rounds} != {_SF_N}"
            assert len(rp.cores) == 2, f"{len(rp.cores)} cores"
            assert (rp.width, rp.height) == (_SF_W, _SF_H), "map dims"
            assert rp.unknown_kinds == set(), f"unknown kinds {rp.unknown_kinds}"
        except Exception as exc:                       # noqa: BLE001
            n_fail += 1
            fails.append((name, "fixture unparseable by replay_census", exc))
            print(f"       FAIL  fixture does not parse under replay_census: {exc}")
            continue
        g = decode(path, our_team)
        if g is None:
            n_fail += 1
            fails.append((name, "decode() returned None", None))
            print("       FAIL  decode() returned None")
            continue
        for label, forced, key in checks:
            try:
                obs = key(g)
            except Exception as exc:                   # noqa: BLE001
                obs = f"<raised {exc!r}>"
            ok = _sf_eq(forced, obs)
            n_ok, n_fail = n_ok + ok, n_fail + (not ok)
            if not ok:
                fails.append((name, label, f"forced {forced!r} observed {obs!r}"))
            print(f"       {'ok  ' if ok else 'FAIL'}  {label:<26}"
                  f" forced {forced!r:<12} observed {obs!r}")
    print(f"\n  {n_ok} assertions passed, {n_fail} failed, "
          f"over {len(_sf_cells())} cells")
    for f in fails:
        print(f"    FAILED: {f[0]} :: {f[1]} :: {f[2]}")
    print("\n  WHAT THIS DOES NOT COVER: aggregation across games (run_arm/"
          "report are untested here); real-replay geometry beyond these cells; "
          "and decode()'s removeEntity handler popping pos_of without popping "
          "team_of/kind_of (harmless as written, live if anyone reads those "
          "maps outside the position loop).")
    print(f"\nRING_READ_SELFTEST: {'PASS' if n_fail == 0 else 'FAIL'}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    res = {}
    for f in sys.argv[1:]:
        fp = Path(f)
        games, per_opp, sc = run_arm(fp)
        res[fp.name] = report(fp.name, games, per_opp, sc)
    if len(res) == 2:
        (na, a), (nb, b) = res.items()
        print(f"\n{'='*78}\n=== MECHANISM DELTA {na} minus {nb} ===")
        print(f"  ring-body coverage      {a['cov']:.3f} - {b['cov']:.3f} = "
              f"{a['cov']-b['cov']:+.3f}   [prereg MECHANISM BAR: >= +0.08]")
        print(f"  coverage rounds <250    {a['cov250']:.3f} - {b['cov250']:.3f} = "
              f"{a['cov250']-b['cov250']:+.3f}")
