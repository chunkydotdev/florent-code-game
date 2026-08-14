#!/usr/bin/env python3
"""NAV LOCK CENSUS — how much of our builder workforce is stuck in a two-tile
navigation limit cycle, measured off the archived replay corpus.

WHY THIS FILE EXISTS
====================
QUEUE `#54` (the nav limit cycle): our builder bots routinely end up alternating
between two tiles forever.  `eco.py`'s `self.stuck` counter only increments when
*all four* candidate moves fail, and `_nav`'s fallback ladder ends in
`desired.opposite()` — so an oscillation is made entirely of SUCCESSFUL moves,
`stuck` stays 0, and neither escape hatch (`stuck >= 5` repick, `nav_fail >= 8`
ban) can ever fire.  The bot is stuck in a way its own watchdog cannot see.

This census is simultaneously the **dose instrument**, the **mechanism metric**
and the **retirement predicate** for four queue rows — `#54` (the cycle itself),
`#63` (long-approach arrival), `#64` (spawnpocket) and the `RETIRE60` plank.

Its predecessor, `nav_limit_cycle_census.py`, lived only in a session scratchpad
and has now been **lost twice** (once recovered from two dying scratchpad dirs,
then purged from `/private/tmp` for good).  Both of its output files
(`census_v125.withmap.jsonl`, `census_v125.jsonl`) went with it.  This is the
committed rebuild; the algorithm, the inferred predicate and the reproduction
gate are written down in `docs/research/SPEC-nav-lock-census-2026-08-14.md`.

WHAT IT COMPUTES
================
For every one of OUR builder bots in a game, the per-round position track is
decoded straight off the `.replay26` wire (`placeEntity` / `moveBuilderBot` /
`removeEntity`).  A **LOCK** is a window of at least `MIN_SPAN` consecutive
rounds during which the bot occupies at most `MAX_DWELL` distinct tiles.

Two readings of that, and they are NOT interchangeable:

  * **STRICT** (the headline) — a *permanent* lock: the qualifying window runs
    to the bot's last living round.  The bot never came out of it.  Onset is the
    earliest round from which the tail of the track stays inside <= MAX_DWELL
    tiles.  This is the metric all the published `#54` figures use.
  * **SOFT** — the union of *every* qualifying window anywhere in the track, so
    a bot that locks, escapes, and locks again is counted for both stretches.

`MIN_SPAN = 50`, `MAX_DWELL = 2` are the recorded parameter names and values of
the lost original.  See the spec for exactly which parts of the predicate around
them are inference rather than record.

USAGE
=====
    .venv/bin/python tools/nav_lock_census.py --selftest
    .venv/bin/python tools/nav_lock_census.py --controls
    .venv/bin/python tools/nav_lock_census.py --ourver 125 --report
    .venv/bin/python tools/nav_lock_census.py --ourver 125 --limit 1160 \
        --jsonl census_v125.jsonl --report
    .venv/bin/python tools/nav_lock_census.py --game <path.replay26> --team 1

`--limit N` takes the **N oldest games by `completedAt`**, which is how a past
archive snapshot is approximated (the published headline was taken when the
archive held 1,160 v125 games; it now holds 1,185).  It is deliberately NOT a
random or arbitrary-order cut.

⚠ POPULATION CAVEAT.  `ourver` here is derived per game from `meta_join.tsv`'s
`teamAVersion`/`teamBVersion` + `us_side`, i.e. the version the PLATFORM recorded
for that match.  Elsewhere in this repo `ourver` sometimes means the poll-time
tag out of `elo_history.tsv`, which is a different and less precise thing; a
version boundary inside a match still lands on whichever side the platform
stamped.  Treat a version cell as approximate at the boundaries.

⚠ SURFACE CAVEAT.  This reads `meta_join.tsv`, which pools rated ladder games
with unrated challenge games.  That is correct HERE — the question is a property
of our own code, not a win-rate denominator — but any win-rate cut taken off
this population would breach the standing "never `meta_join` for a denominator"
rule.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# Wire helpers are REUSED from the existing decoder rather than re-rolled — the
# recovered protobuf schema lives in tools/replay_schema.md and there must be
# exactly one implementation of it in the tree.
from replay_census import fields, read_pos, packed_varints  # noqa: E402

# --- the detector's two parameters -------------------------------------------
# Recorded names and values of the lost original (`analyze_bot_lock`,
# `find_windows`, MIN_SPAN=50, MAX_DWELL=2).  Constants, never magic numbers:
# every call site takes them as defaults so a sweep is one flag, not an edit.
MIN_SPAN = 50    # a window must span at least this many consecutive rounds
MAX_DWELL = 2    # ...during which the bot occupies at most this many tiles

# --- wire constants ----------------------------------------------------------
WIRE_LEN = 2
ENTITY_BUILDER_BOT = 10          # Entity.builderBot field number
UPD_PLACE, UPD_MOVE, UPD_REMOVE = 1, 2, 3
# builderAttack / builderHeal / builderBuild.  These three are the only builder
# actions the wire attributes to a bot id; `destroy` and `self_destruct` surface
# as an unattributed removeEntity, so "never acted" below means "never built,
# healed or attacked".  See the spec.
UPD_ACTIONS = (13, 15, 16)
SIDE_TO_TEAM = {"a": 0, "b": 1}  # standing mapping, inherited (spec §Caveats)

DEFAULT_META = REPO / "corpus" / "meta_join.tsv"
DEFAULT_ARCHIVE = REPO / "replay_archive"
DEFAULT_MAPS = REPO / "maps"


# =============================================================================
# THE DETECTOR
# =============================================================================

def left_bounds(track, max_dwell=MAX_DWELL):
    """For each index r, the smallest l with |{track[l..r]}| <= max_dwell.

    Standard two-pointer over a distinct-count window: O(n) and exact.  This is
    the primitive both `find_windows` and `analyze_bot_lock` are built on, so it
    is the one thing the selftest checks element by element.
    """
    counts = {}
    out = []
    l = 0
    for r, p in enumerate(track):
        counts[p] = counts.get(p, 0) + 1
        while len(counts) > max_dwell:
            q = track[l]
            counts[q] -= 1
            if not counts[q]:
                del counts[q]
            l += 1
        out.append(l)
    return out


def find_windows(track, min_span=MIN_SPAN, max_dwell=MAX_DWELL, lb=None):
    """Maximal qualifying windows as inclusive [start, end] round indices.

    A window qualifies when it spans >= min_span rounds and the bot occupies
    <= max_dwell distinct tiles across it.  Maximal = not contained in another
    qualifying window; overlapping maximal windows are merged, because two
    windows that overlap describe one uninterrupted stretch of locked rounds.
    """
    n = len(track)
    if n < min_span:
        return []
    if lb is None:
        lb = left_bounds(track, max_dwell)
    spans = []
    for r in range(n):
        if r - lb[r] + 1 >= min_span:
            s = lb[r]
            if spans and s <= spans[-1][1] + 1:
                spans[-1][1] = r
                spans[-1][0] = min(spans[-1][0], s)
            else:
                spans.append([s, r])
    return [(a, b) for a, b in spans]


def analyze_bot_lock(track, min_span=MIN_SPAN, max_dwell=MAX_DWELL):
    """Lock verdict for one bot's position track (index i == its i-th living round).

    Returns:
      strict         permanent lock: a qualifying window runs to the last round
      onset          index of the first round of that permanent window (else None)
      strict_rounds  length of the permanent window (0 when not strict)
      lock_tiles     the <= max_dwell tiles of the permanent window
      soft_rounds    rounds covered by ANY qualifying window
      windows        the maximal qualifying windows
    """
    n = len(track)
    empty = dict(strict=False, onset=None, strict_rounds=0, lock_tiles=[],
                 soft_rounds=0, windows=[])
    if n < min_span:
        return empty
    lb = left_bounds(track, max_dwell)
    windows = find_windows(track, min_span, max_dwell, lb=lb)
    onset = lb[n - 1]
    strict_rounds = n - onset
    strict = strict_rounds >= min_span
    return dict(
        strict=strict,
        onset=onset if strict else None,
        strict_rounds=strict_rounds if strict else 0,
        lock_tiles=sorted(set(track[onset:])) if strict else [],
        soft_rounds=sum(b - a + 1 for a, b in windows),
        windows=windows,
    )


# =============================================================================
# WIRE DECODE
# =============================================================================

def decode_tracks(path, our_team):
    """Decode one replay into per-round position tracks for OUR builder bots.

    A bot's track index 0 is the first round it is alive at end-of-round; its
    absolute round is `spawn + i`.  Rounds are 0-based (`turns[i]` IS round i).
    """
    data = Path(path).read_bytes()
    map_buf = None
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        raise ValueError(f"{path}: no battlecode.Map (field 1) — not a replay?")

    width = height = 0
    tiles = []
    cores = {}
    for num, wire, value in fields(map_buf):
        if num == 1:
            width = value
        elif num == 2:
            height = value
        elif num == 3:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            tiles.append(tuple(row))
        elif num == 4:
            team = 0
            pos = (0, 0)
            for cn, _cw, cv in fields(value):
                if cn == 2:
                    team = cv
                elif cn == 3:
                    pos = read_pos(cv)
            cores[team] = pos

    bots = {}       # id -> {"spawn": r, "track": [...], "acts": n}
    alive = {}      # id -> current position (our builders only)
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, upd in fields(turn_buf):
            for unum, _uw, ubuf in fields(upd):
                if unum == UPD_PLACE:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        eid = None
                        team = 0          # proto3: team A (0) is omitted
                        pos = None
                        is_builder = False
                        for fn, _fw, fv in fields(ebuf):
                            if fn == 1:
                                eid = fv
                            elif fn == 2:
                                team = fv
                            elif fn == 3:
                                pos = read_pos(fv)
                            elif fn == ENTITY_BUILDER_BOT:
                                is_builder = True
                        if is_builder and team == our_team and eid is not None:
                            # First placeEntity for an id is the spawn; later
                            # ones are state re-emits (rotation guard, see
                            # replay_census.py) and must not restart the track.
                            if eid not in bots:
                                bots[eid] = {"spawn": rnd, "track": [], "acts": 0}
                            alive[eid] = pos
                elif unum == UPD_MOVE:
                    eid = None
                    to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if to is not None and eid in alive:
                        alive[eid] = to
                elif unum == UPD_REMOVE:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            alive.pop(rv, None)
                elif unum in UPD_ACTIONS:
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            if av in bots:
                                bots[av]["acts"] += 1
                            break
        for eid, pos in alive.items():
            bots[eid]["track"].append(pos)

    return dict(rounds=len(turn_bufs), width=width, height=height,
                tiles=tiles, cores=cores, bots=bots)


# =============================================================================
# MAP IDENTIFICATION
# =============================================================================

_MAP_INDEX = None


def map_index(maps_dir=DEFAULT_MAPS):
    """Fingerprint every known map by (width, height, tile grid) -> name."""
    global _MAP_INDEX
    if _MAP_INDEX is not None:
        return _MAP_INDEX
    idx = {}
    for p in sorted(Path(maps_dir).glob("*.map26")):
        buf = p.read_bytes()
        w = h = 0
        rows = []
        for num, wire, value in fields(buf):
            if num == 1:
                w = value
            elif num == 2:
                h = value
            elif num == 3:
                row = []
                for rn, rw, rv in fields(value):
                    if rn == 1:
                        row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
                rows.append(tuple(row))
        idx[(w, h, tuple(rows))] = p.stem
    _MAP_INDEX = idx
    return idx


def identify_map(width, height, tiles, maps_dir=DEFAULT_MAPS):
    """Exact-grid map name, or 'UNKNOWN'.

    UNKNOWN is not a parse failure: the platform has served grids that differ
    from the copies in maps/ (the pre-MAPFIX glacierkeep layout is the known
    case, 64 games in the v125 population).  Those games still carry dims and
    core positions in the JSONL, which is how they were identified by hand.
    """
    return map_index(maps_dir).get((width, height, tuple(tiles)), "UNKNOWN")


# =============================================================================
# PER-GAME CENSUS
# =============================================================================

def census_game(path, our_team, min_span=MIN_SPAN, max_dwell=MAX_DWELL,
                maps_dir=DEFAULT_MAPS, with_map=True):
    """One game -> one census record (the JSONL row)."""
    g = decode_tracks(path, our_team)
    name = identify_map(g["width"], g["height"], g["tiles"], maps_dir) if with_map else None
    own_core = g["cores"].get(our_team)
    bots_out = []
    for eid, b in sorted(g["bots"].items()):
        track = b["track"]
        a = analyze_bot_lock(track, min_span, max_dwell)
        max_d2 = 0
        if own_core and track:
            cx, cy = own_core
            max_d2 = max((x - cx) ** 2 + (y - cy) ** 2 for x, y in track)
        rec = dict(
            id=eid,
            spawn=b["spawn"],
            life=len(track),
            acts=b["acts"],
            strict=a["strict"],
            onset=(b["spawn"] + a["onset"]) if a["strict"] else None,
            strict_rounds=a["strict_rounds"],
            soft_rounds=a["soft_rounds"],
            lock_tiles=[list(t) for t in a["lock_tiles"]],
            max_d2_own=max_d2,
        )
        if a["strict"] and own_core:
            lx, ly = a["lock_tiles"][0]
            cx, cy = own_core
            rec["lock_d2_own"] = (lx - cx) ** 2 + (ly - cy) ** 2
        bots_out.append(rec)
    return dict(
        file=Path(path).name,
        rounds=g["rounds"],
        width=g["width"],
        height=g["height"],
        map=name,
        our_team=our_team,
        cores={str(k): list(v) for k, v in sorted(g["cores"].items())},
        builder_rounds=sum(x["life"] for x in bots_out),
        bots=bots_out,
    )


# =============================================================================
# POPULATION
# =============================================================================

def population(ourver=None, meta=DEFAULT_META, archive=DEFAULT_ARCHIVE, limit=None):
    """[(replay_path, our_team, completedAt)] for games matching `ourver`.

    `--limit N` returns the N OLDEST by completedAt.  That is how a past archive
    snapshot is approximated; see the module docstring.
    """
    rows = []
    with open(meta) as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            side = row["us_side"]
            if side not in SIDE_TO_TEAM:
                continue
            ver = row["teamAVersion"] if side == "a" else row["teamBVersion"]
            if ourver is not None and ver != str(ourver):
                continue
            p = Path(archive) / row["file"]
            if not p.exists():
                continue
            rows.append((p, SIDE_TO_TEAM[side], row.get("completedAt", ""), ver))
    rows.sort(key=lambda r: (r[2], r[0].name))
    if limit is not None:
        rows = rows[:limit]
    return rows


# =============================================================================
# AGGREGATION / REPORT
# =============================================================================

def aggregate(records):
    tot_rounds = 0
    tot_soft = 0
    tot_strict = 0
    locked_bots = 0
    never_acted = 0
    onsets = []
    games_with_lock = 0
    per_map = defaultdict(lambda: [0, 0, 0])   # map -> [rounds, strict, games]
    per_map_games = Counter()
    for rec in records:
        tot_rounds += rec["builder_rounds"]
        has = False
        for b in rec["bots"]:
            tot_soft += b["soft_rounds"]
            if b["strict"]:
                has = True
                locked_bots += 1
                tot_strict += b["strict_rounds"]
                onsets.append(b["onset"])
                if b["acts"] == 0:
                    never_acted += 1
        if has:
            games_with_lock += 1
        m = rec.get("map") or "UNKNOWN"
        per_map[m][0] += rec["builder_rounds"]
        per_map[m][1] += sum(b["strict_rounds"] for b in rec["bots"])
        per_map_games[m] += 1
    return dict(
        games=len(records),
        builder_rounds=tot_rounds,
        strict_rounds=tot_strict,
        soft_rounds=tot_soft,
        strict_pct=100.0 * tot_strict / tot_rounds if tot_rounds else 0.0,
        soft_pct=100.0 * tot_soft / tot_rounds if tot_rounds else 0.0,
        locked_bots=locked_bots,
        never_acted=never_acted,
        never_acted_pct=100.0 * never_acted / locked_bots if locked_bots else 0.0,
        median_onset=statistics.median(onsets) if onsets else None,
        games_with_lock=games_with_lock,
        games_with_lock_pct=100.0 * games_with_lock / len(records) if records else 0.0,
        per_map={m: dict(builder_rounds=v[0], strict_rounds=v[1],
                         pct=100.0 * v[1] / v[0] if v[0] else 0.0,
                         games=per_map_games[m])
                 for m, v in per_map.items()},
    )


def print_report(agg, fh=sys.stdout):
    p = lambda *a: print(*a, file=fh)
    p(f"games                    {agg['games']}")
    p(f"builder-rounds           {agg['builder_rounds']}")
    p(f"STRICT locked rounds     {agg['strict_rounds']}  "
      f"({agg['strict_pct']:.2f}% of builder-rounds)")
    p(f"SOFT locked rounds       {agg['soft_rounds']}  ({agg['soft_pct']:.2f}%)")
    p(f"locked bots (STRICT)     {agg['locked_bots']}")
    p(f"  never acted            {agg['never_acted']}  ({agg['never_acted_pct']:.2f}%)")
    p(f"median lock onset round  {agg['median_onset']}")
    p(f"games with >=1 lock      {agg['games_with_lock']}  "
      f"({agg['games_with_lock_pct']:.1f}%)")
    p("")
    p(f"{'map':<16}{'games':>7}{'b-rounds':>11}{'locked':>10}{'pct':>8}")
    for m, v in sorted(agg["per_map"].items(), key=lambda kv: -kv[1]["pct"]):
        p(f"{m:<16}{v['games']:>7}{v['builder_rounds']:>11}"
          f"{v['strict_rounds']:>10}{v['pct']:>7.1f}%")


# =============================================================================
# CONTROLS
# =============================================================================

# The reproduction gate's positive control: every one of our 11 builders in this
# game ends permanently locked, and six of the ids were hand-traced in s39.
POS_CONTROL_FILE = "483b5bcd-b4e4-4db7-a554-e204d1f42015_game_1.replay26"
POS_CONTROL_TEAM = 1                                   # us_side = 'b'
POS_CONTROL_IDS = [4, 11, 18, 435, 724, 760]           # hand-traced in s39
# Their recorded permanent-window lengths (QUEUE #54).  Bot 4's recorded 807 is
# from the ORIGINAL hand tracer's oscillation-window definition, not from this
# detector — it is the one bot the trace note flags as having exceptions
# ("zero exceptions for 5 of 6 traced").  Only the five clean ones are asserted.
POS_CONTROL_WINDOWS = {11: 961, 18: 970, 435: 626, 724: 629, 760: 606}


def run_controls(archive=DEFAULT_ARCHIVE, fh=sys.stdout):
    """Drive the wire-level controls in BOTH directions.

    Positive: the known 11/11 game, including all six hand-traced ids and the
    five recorded window lengths.
    Negative: the same detector on the SAME wire path must come out the other
    way — three groups, each of which would expose a detector that says "locked"
    unconditionally.
    """
    ok = True
    p = lambda *a: print(*a, file=fh)
    path = Path(archive) / POS_CONTROL_FILE

    p("POSITIVE CONTROL — 483b5bcd g1, our side (team 1)")
    rec = census_game(path, POS_CONTROL_TEAM)
    locked = [b["id"] for b in rec["bots"] if b["strict"]]
    p(f"  builders={len(rec['bots'])} locked={len(locked)} ids={locked}")
    good = len(locked) == len(rec["bots"]) == 11
    p(f"  11/11 locked ................ {'PASS' if good else 'FAIL'}")
    ok &= good
    have = all(i in locked for i in POS_CONTROL_IDS)
    p(f"  all six traced ids present .. {'PASS' if have else 'FAIL'}  {POS_CONTROL_IDS}")
    ok &= have
    by_id = {b["id"]: b for b in rec["bots"]}
    for i, want in sorted(POS_CONTROL_WINDOWS.items()):
        got = by_id[i]["strict_rounds"]
        good = got == want
        p(f"  window id={i:<4} recorded={want:<5} got={got:<5} "
          f"{'PASS' if good else 'FAIL'}")
        ok &= good

    p("")
    p("NEGATIVE CONTROLS — the same detector must come out the other way")

    # N1 — the complement side of the very same wire read: the OPPONENT's
    # builders in the identical replay.  Same file, same parser, same detector;
    # only the team byte changes.  A detector that reports locks unconditionally
    # cannot produce a split here.
    enemy = census_game(path, 1 - POS_CONTROL_TEAM)
    elocked = [b["id"] for b in enemy["bots"] if b["strict"]]
    good = 0 < len(elocked) < len(enemy["bots"])
    p(f"  N1 opponent side, same file: {len(elocked)}/{len(enemy['bots'])} locked "
      f"{elocked}  {'PASS' if good else 'FAIL'} (must be a strict split)")
    ok &= good

    # N2 — mutation of the positive control's own tracks: splice a third tile
    # into each traced bot's permanent window.  Every one MUST flip to unlocked.
    flipped = 0
    for i in POS_CONTROL_IDS:
        g = decode_tracks(path, POS_CONTROL_TEAM)
        track = list(g["bots"][i]["track"])
        onset = analyze_bot_lock(track)["onset"]
        x, y = track[-1]
        for r in range(onset, len(track), 3):        # a 3rd tile every 3 rounds
            track[r] = (x + 7, y + 7)
        if not analyze_bot_lock(track)["strict"]:
            flipped += 1
    good = flipped == len(POS_CONTROL_IDS)
    p(f"  N2 third tile spliced in:    {flipped}/{len(POS_CONTROL_IDS)} flip to UNLOCKED"
      f"  {'PASS' if good else 'FAIL'}")
    ok &= good

    # N3 — truncation: the same locked tracks cut to MIN_SPAN-1 rounds of the
    # window must all read unlocked, which is what proves MIN_SPAN binds.
    flipped = 0
    g = decode_tracks(path, POS_CONTROL_TEAM)
    for i in POS_CONTROL_IDS:
        track = g["bots"][i]["track"]
        onset = analyze_bot_lock(track)["onset"]
        if not analyze_bot_lock(track[onset:onset + MIN_SPAN - 1])["strict"]:
            flipped += 1
    good = flipped == len(POS_CONTROL_IDS)
    p(f"  N3 window cut to {MIN_SPAN - 1} rounds:   {flipped}/{len(POS_CONTROL_IDS)} "
      f"read UNLOCKED  {'PASS' if good else 'FAIL'}")
    ok &= good

    p("")
    p(f"CONTROLS: {'ALL PASS' if ok else 'FAILURE'}")
    return ok


# =============================================================================
# SELFTEST
# =============================================================================

def selftest(fh=sys.stdout):
    """Unit-level checks.  Every guard is driven to BOTH verdicts."""
    p = lambda *a: print(*a, file=fh)
    fails = []

    def check(name, got, want):
        good = got == want
        p(f"  {'PASS' if good else 'FAIL'}  {name}: got {got!r} want {want!r}")
        if not good:
            fails.append(name)

    A, B, C = (1, 1), (1, 2), (5, 5)

    # left_bounds, element by element, on a hand-computable case
    check("left_bounds ABCA", left_bounds([A, B, C, A], 2), [0, 0, 1, 2])
    check("left_bounds dwell1", left_bounds([A, A, B], 1), [0, 0, 2])

    # MIN_SPAN binds in both directions
    check("50-round 2-cycle is locked",
          analyze_bot_lock([A, B] * 25)["strict"], True)
    check("49-round 2-cycle is NOT locked",
          analyze_bot_lock(([A, B] * 25)[:49])["strict"], False)

    # MAX_DWELL binds in both directions
    check("3-tile cycle is NOT locked",
          analyze_bot_lock([A, B, C] * 100)["strict"], False)
    check("stationary bot IS locked (dwell 1)",
          analyze_bot_lock([A] * 60)["strict"], True)
    check("3-tile cycle IS locked at max_dwell=3",
          analyze_bot_lock([A, B, C] * 100, max_dwell=3)["strict"], True)

    # a free walk is never locked
    walk = [(i, 0) for i in range(500)]
    check("monotone walk not locked", analyze_bot_lock(walk)["strict"], False)
    check("monotone walk soft=0", analyze_bot_lock(walk)["soft_rounds"], 0)

    # STRICT is PERMANENT: a lock that ends before the bot does is soft-only
    esc = [A, B] * 100 + walk[:100]
    a = analyze_bot_lock(esc)
    check("escaped lock: strict False", a["strict"], False)
    check("escaped lock: soft counts it", a["soft_rounds"], 200)

    # onset is the EARLIEST start of the permanent window, not the latest
    a = analyze_bot_lock(walk[:100] + [A, B] * 100)
    check("onset after 100 rounds of travel", a["onset"], 100)
    check("strict_rounds is the whole tail", a["strict_rounds"], 200)
    check("lock tiles recovered", a["lock_tiles"], [A, B])

    # soft unions two disjoint windows and does not double count
    two = [A, B] * 50 + walk[:200] + [C, (6, 6)] * 60
    a = analyze_bot_lock(two)
    check("two windows -> soft 220", a["soft_rounds"], 220)
    check("two windows -> 2 maximal windows", len(a["windows"]), 2)

    # a bot shorter than MIN_SPAN is inert, not an exception
    check("short track inert", analyze_bot_lock([A] * 10)["strict"], False)
    check("empty track inert", analyze_bot_lock([])["strict"], False)

    # find_windows merges overlaps rather than emitting one window per round
    check("one long window stays one",
          find_windows([A, B] * 200), [(0, 399)])

    # map fingerprinting: a real map resolves, a mutated grid does not
    idx = map_index()
    if idx:
        (w, h, rows), name = next(iter(sorted(idx.items(), key=lambda kv: kv[1])))
        check("known map resolves", identify_map(w, h, rows), name)
        bad = list(rows)
        bad[0] = tuple((v + 1) % 3 for v in bad[0])
        check("mutated grid -> UNKNOWN", identify_map(w, h, bad), "UNKNOWN")
    else:
        fails.append("map index empty")
        p("  FAIL  map index empty")

    p(f"SELFTEST: {'ALL PASS' if not fails else 'FAILED ' + ', '.join(fails)}")
    return not fails


# =============================================================================
# MAIN
# =============================================================================

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true", help="unit checks, no corpus")
    ap.add_argument("--controls", action="store_true",
                    help="drive the positive + negative wire controls")
    ap.add_argument("--game", help="census a single replay file")
    ap.add_argument("--team", type=int, help="our team index for --game (0=A, 1=B)")
    ap.add_argument("--ourver", default="125", help="version to census (default 125)")
    ap.add_argument("--all-versions", action="store_true",
                    help="ignore --ourver and take every game with a known us_side")
    ap.add_argument("--limit", type=int,
                    help="take the N OLDEST games by completedAt (snapshot approximation)")
    ap.add_argument("--min-span", type=int, default=MIN_SPAN)
    ap.add_argument("--max-dwell", type=int, default=MAX_DWELL)
    ap.add_argument("--jsonl", help="write one census record per game here")
    ap.add_argument("--report", action="store_true", help="print the aggregate report")
    ap.add_argument("--meta", default=str(DEFAULT_META))
    ap.add_argument("--archive", default=str(DEFAULT_ARCHIVE))
    ap.add_argument("--maps", default=str(DEFAULT_MAPS))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return 0 if selftest() else 1
    if args.controls:
        return 0 if run_controls(args.archive) else 1
    if args.game:
        if args.team is None:
            ap.error("--game needs --team")
        rec = census_game(args.game, args.team, args.min_span, args.max_dwell, args.maps)
        print(json.dumps(rec))
        return 0

    pop = population(None if args.all_versions else args.ourver,
                     args.meta, args.archive, args.limit)
    if not pop:
        print("empty population", file=sys.stderr)
        return 1
    out = open(args.jsonl, "w") if args.jsonl else None
    records = []
    errors = 0
    for n, (path, team, _when, _ver) in enumerate(pop, 1):
        try:
            rec = census_game(path, team, args.min_span, args.max_dwell, args.maps)
        except Exception as exc:                       # noqa: BLE001
            errors += 1
            print(f"PARSE ERROR {path.name}: {exc}", file=sys.stderr)
            continue
        records.append(rec)
        if out:
            out.write(json.dumps(rec) + "\n")
        if not args.quiet and n % 200 == 0:
            print(f"  ...{n}/{len(pop)}", file=sys.stderr)
    if out:
        out.close()
    agg = aggregate(records)
    agg["parse_errors"] = errors
    agg["min_span"] = args.min_span
    agg["max_dwell"] = args.max_dwell
    if args.report:
        print(f"population {len(pop)} games, parse errors {errors}, "
              f"MIN_SPAN={args.min_span} MAX_DWELL={args.max_dwell}")
        print_report(agg)
    else:
        print(json.dumps({k: v for k, v in agg.items() if k != "per_map"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
