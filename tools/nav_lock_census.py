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
rounds in which

    (1) the bot occupies at most `MAX_TILES` distinct tiles, AND
    (2) it never sits on one tile for more than `MAX_DWELL` consecutive rounds.

Clause (2) is what makes this an OSCILLATION detector rather than an idleness
detector: a bot that simply parks has dwell = the whole window and is excluded,
which is exactly what `HOME-LOCK-MECHANISM-2026-08-14.md:150` records —
*"a pocket produces either a stall (long dwell — excluded by the detector's
MAX_DWELL = 2) or a 2-cycle"*.  Drop clause (2) and the v125 rate reads 41.5%
instead of 11.6%, because every parked builder counts.

Two readings of the window, and they are NOT interchangeable:

  * **STRICT** (the headline) — a *permanent* lock: the qualifying window runs
    to the bot's last living round.  The bot never came out of it.  Onset is the
    earliest round from which the tail of the track stays inside <= MAX_DWELL
    tiles.  This is the metric all the published `#54` figures use.
  * **SOFT** — the union of *every* qualifying window anywhere in the track, so
    a bot that locks, escapes, and locks again is counted for both stretches.

`MIN_SPAN = 50`, `MAX_DWELL = 2` are the recorded parameter names and values of
the lost original.  `MAX_TILES = 2` is NOT recorded — it is inferred from the
row's own wording ("two-tile lock") and is stated as an inference in the spec,
alongside everything else about the predicate that is reconstruction rather than
record.

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

# --- the detector's parameters -----------------------------------------------
# MIN_SPAN and MAX_DWELL are the recorded names and values of the lost original
# (`analyze_bot_lock`, `find_windows`, MIN_SPAN=50, MAX_DWELL=2).  MAX_TILES is
# an inference — see the spec.  Constants, never magic numbers: every call site
# takes them as defaults, so a sensitivity sweep is one flag and not an edit.
MIN_SPAN = 50    # a window must span at least this many consecutive rounds
MAX_TILES = 2    # ...over at most this many distinct tiles ("two-tile lock")
MAX_DWELL = 2    # ...never resting on one tile more than this many rounds

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

def left_bounds(track, max_tiles=MAX_TILES, max_dwell=MAX_DWELL):
    """For each index r, the smallest l for which the window [l..r] qualifies
    on the two shape constraints (span is applied by the caller).

    A window qualifies when
      * it contains at most `max_tiles` distinct positions, and
      * every maximal run of identical consecutive positions INSIDE the window
        — boundary runs included, truncated by the window edges — is at most
        `max_dwell` rounds long.

    Both constraints are monotone in l (shrinking a window from the left can
    only drop tiles and can only truncate the leftmost run), so one forward
    two-pointer computes both exactly in O(n).  `l_tiles` is the classic
    distinct-count pointer; `l_run` is pinned forward whenever the run ending at
    r has already outgrown max_dwell, since the only way to satisfy the bound
    then is to cut into that run.
    """
    counts = {}
    out = []
    l_tiles = 0
    l_run = 0
    run = 0
    prev = object()
    for r, p in enumerate(track):
        run = run + 1 if p == prev else 1
        prev = p
        if run > max_dwell:
            l_run = max(l_run, r - max_dwell + 1)
        counts[p] = counts.get(p, 0) + 1
        while len(counts) > max_tiles:
            q = track[l_tiles]
            counts[q] -= 1
            if not counts[q]:
                del counts[q]
            l_tiles += 1
        out.append(max(l_tiles, l_run))
    return out


def find_windows(track, min_span=MIN_SPAN, max_tiles=MAX_TILES,
                 max_dwell=MAX_DWELL, lb=None):
    """Maximal qualifying windows as inclusive [start, end] round indices.

    Maximal = not contained in another qualifying window; overlapping or
    abutting maximal windows are merged, because they describe one
    uninterrupted stretch of locked rounds and must not be counted twice.
    """
    n = len(track)
    if n < min_span:
        return []
    if lb is None:
        lb = left_bounds(track, max_tiles, max_dwell)
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


def analyze_bot_lock(track, min_span=MIN_SPAN, max_tiles=MAX_TILES,
                     max_dwell=MAX_DWELL):
    """Lock verdict for one bot's position track (index i == its i-th living round).

    Returns:
      strict         permanent lock: a qualifying window runs to the last round
      onset          index of the first round of that permanent window (else None)
      strict_rounds  length of the permanent window (0 when not strict)
      lock_tiles     the <= max_tiles tiles of the permanent window
      soft_rounds    rounds covered by ANY qualifying window
      windows        the maximal qualifying windows
    """
    n = len(track)
    empty = dict(strict=False, onset=None, strict_rounds=0, lock_tiles=[],
                 soft_rounds=0, windows=[])
    if n < min_span:
        return empty
    lb = left_bounds(track, max_tiles, max_dwell)
    windows = find_windows(track, min_span, max_tiles, max_dwell, lb=lb)
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
    """Two fingerprints per known map.

    `grid`  (width, height, tile grid) -> name          — exact, always trusted
    `sig`   (width, height, coreA, coreB) -> {names}    — layout signature

    The signature exists because the PLATFORM HAS RESHIPPED GRIDS.  The v125
    population was played on valkyrie and glacierkeep layouts that differ from
    the copies now in `maps/` by 10 and 9 tiles — and those two `.map26` files
    were only committed on 2026-08-14 22:07Z (`f9fda96a`), i.e. AFTER the
    original census ran.  Exact-grid alone therefore leaves 144 of 1,160 v125
    games unnamed (80 valkyrie + 64 glacierkeep), which is where the original's
    "64 UNKNOWN games ... verified by dims+cores (14,2)/(14,26)" note came from.
    A signature hit is reported with a `*` suffix so a re-grid is never silently
    laundered into an exact match.
    """
    global _MAP_INDEX
    if _MAP_INDEX is not None:
        return _MAP_INDEX
    grid = {}
    sig = defaultdict(set)
    for p in sorted(Path(maps_dir).glob("*.map26")):
        buf = p.read_bytes()
        w = h = 0
        rows = []
        cores = {}
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
            elif num == 4:
                d = {}
                for cn, _cw, cv in fields(value):
                    d[cn] = cv
                cores[d.get(2, 0)] = read_pos(d[3]) if 3 in d else None
        grid[(w, h, tuple(rows))] = p.stem
        sig[(w, h, cores.get(0), cores.get(1))].add(p.stem)
    _MAP_INDEX = {"grid": grid, "sig": dict(sig)}
    return _MAP_INDEX


def identify_map(width, height, tiles, cores=None, maps_dir=DEFAULT_MAPS):
    """'<name>' on an exact grid match, '<name>*' on a unique layout signature,
    else 'UNKNOWN'.

    midgard and ragnarok share dims AND core positions, so the signature stage
    deliberately refuses to guess when more than one map matches — those two are
    only ever named by the exact grid.
    """
    idx = map_index(maps_dir)
    name = idx["grid"].get((width, height, tuple(tiles)))
    if name:
        return name
    if cores:
        cand = idx["sig"].get((width, height, cores.get(0), cores.get(1)))
        if cand and len(cand) == 1:
            return next(iter(cand)) + "*"
    return "UNKNOWN"


# =============================================================================
# PER-GAME CENSUS
# =============================================================================

def census_game(path, our_team, min_span=MIN_SPAN, max_tiles=MAX_TILES,
                max_dwell=MAX_DWELL, maps_dir=DEFAULT_MAPS, with_map=True):
    """One game -> one census record (the JSONL row)."""
    g = decode_tracks(path, our_team)
    name = (identify_map(g["width"], g["height"], g["tiles"], g["cores"], maps_dir)
            if with_map else None)
    own_core = g["cores"].get(our_team)
    bots_out = []
    for eid, b in sorted(g["bots"].items()):
        track = b["track"]
        a = analyze_bot_lock(track, min_span, max_tiles, max_dwell)
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
# The recorded NEGATIVE control: 1/6.  Game 2 of the same match, our own side —
# the complement group, same bot, same opponent, same session, and it comes out
# the other way.  This one is load-bearing: under a tiles-only predicate (no
# MAX_DWELL clause) the same cell reads 3/6, so this control is what separates
# the two candidate readings of MAX_DWELL.
NEG_CONTROL_FILE = "483b5bcd-b4e4-4db7-a554-e204d1f42015_game_2.replay26"
NEG_CONTROL_TEAM = 1
NEG_CONTROL_EXPECT = (1, 6)
# Window lengths recorded in QUEUE #54 for the six hand-traced ids.  ⚠ THESE ARE
# NOT THIS DETECTOR'S OUTPUT: they come from `six_bot_oscillation.py`, the s39
# hand tracer that ran BEFORE the census and used a parity/two-tile window with
# no dwell clause.  Reported as a cross-check, NOT gated — see the spec's
# reproduction table for the two that differ and why.
TRACER_WINDOWS = {4: 807, 11: 961, 18: 970, 435: 626, 724: 629, 760: 606}


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
    p("  cross-check vs the s39 HAND TRACER's windows (informational, not gated —")
    p("  different instrument: parity window, no dwell clause):")
    for i, want in sorted(TRACER_WINDOWS.items()):
        got = by_id[i]["strict_rounds"]
        p(f"    id={i:<4} tracer={want:<5} census={got:<5} "
          f"{'same' if got == want else 'DIFFERS'}")

    p("")
    p("NEGATIVE CONTROLS — the same detector must come out the other way")

    # N0 — THE RECORDED ONE.  Our own builders in game 2 of the same match:
    # 1/6, against 11/11 in game 1.  Same bot, same opponent, same session,
    # same wire path; only the game changes.
    neg = census_game(Path(archive) / NEG_CONTROL_FILE, NEG_CONTROL_TEAM)
    nlocked = [b["id"] for b in neg["bots"] if b["strict"]]
    got = (len(nlocked), len(neg["bots"]))
    good = got == NEG_CONTROL_EXPECT
    p(f"  N0 RECORDED complement (g2, our side): {got[0]}/{got[1]} locked {nlocked} "
      f"— recorded {NEG_CONTROL_EXPECT[0]}/{NEG_CONTROL_EXPECT[1]}  "
      f"{'PASS' if good else 'FAIL'}")
    ok &= good

    # N1 — the complement side of the very same wire read: the OPPONENT's
    # builders in the identical replay.  Same file, same parser, same detector;
    # only the team byte changes.  A detector that reports locks unconditionally
    # cannot produce 11/11 here and 0/8 there.
    enemy = census_game(path, 1 - POS_CONTROL_TEAM)
    elocked = [b["id"] for b in enemy["bots"] if b["strict"]]
    good = len(elocked) < len(enemy["bots"])
    p(f"  N1 opponent side, same file: {len(elocked)}/{len(enemy['bots'])} locked "
      f"{elocked}  {'PASS' if good else 'FAIL'}")
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

    # N4 — park each traced bot: replace its permanent window with a stall on
    # one of its own two lock tiles.  This is the control for the MAX_DWELL
    # clause specifically, and it is the one that matters most: with the clause
    # dropped, the v125 headline reads 41.5% instead of 11.6%, so a detector
    # that passes N1-N3 but fails N4 is the exact detector that produces the
    # wrong number.
    flipped = 0
    g = decode_tracks(path, POS_CONTROL_TEAM)
    for i in POS_CONTROL_IDS:
        track = list(g["bots"][i]["track"])
        onset = analyze_bot_lock(track)["onset"]
        park = track[-1]
        track[onset:] = [park] * (len(track) - onset)
        if not analyze_bot_lock(track)["strict"]:
            flipped += 1
    good = flipped == len(POS_CONTROL_IDS)
    p(f"  N4 window replaced by a STALL: {flipped}/{len(POS_CONTROL_IDS)} "
      f"read UNLOCKED  {'PASS' if good else 'FAIL'}")
    ok &= good


    p("")
    p("  N0's identity was RECOVERED, not recorded: the original published only")
    p("  the bare string 'negative control 1/6'.  Game 2 of the control match,")
    p("  our own side, is the only cell in the match that reads 1/6 — and it")
    p("  reads 3/6 under the tiles-only predicate, which is how the same figure")
    p("  also discriminates between the two readings of MAX_DWELL.")

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

    # left_bounds, element by element, on hand-computable cases
    check("left_bounds tiles ABCA", left_bounds([A, B, C, A], 2, 9), [0, 0, 1, 2])
    check("left_bounds dwell cut", left_bounds([A, A, A, B], 9, 2), [0, 0, 1, 1])
    check("left_bounds tiles=1", left_bounds([A, A, B], 1, 9), [0, 0, 2])

    # the forward two-pointer must agree with a naive O(n^2) reference on the
    # suffix onset — this is the check that the l_run pin is not an approximation
    import random
    rng = random.Random(20260814)
    pool = [(0, 0), (0, 1), (1, 0), (1, 1)]

    def naive_onset(t, mt, md):
        for l in range(len(t)):
            w = t[l:]
            if len(set(w)) > mt:
                continue
            runs, cur = [], 1
            for i in range(1, len(w)):
                if w[i] == w[i - 1]:
                    cur += 1
                else:
                    runs.append(cur)
                    cur = 1
            runs.append(cur)
            if max(runs) <= md:
                return l
        return len(t)

    bad = 0
    for _ in range(300):
        t = [rng.choice(pool) for _ in range(rng.randint(1, 40))]
        for mt in (1, 2, 3):
            for md in (1, 2, 3):
                if left_bounds(t, mt, md)[-1] != naive_onset(t, mt, md):
                    bad += 1
    check("two-pointer == naive reference (300 random tracks x 9 params)", bad, 0)

    # MIN_SPAN binds in both directions
    check("50-round 2-cycle is locked",
          analyze_bot_lock([A, B] * 25)["strict"], True)
    check("49-round 2-cycle is NOT locked",
          analyze_bot_lock(([A, B] * 25)[:49])["strict"], False)

    # MAX_TILES binds in both directions
    check("3-tile cycle is NOT locked",
          analyze_bot_lock([A, B, C] * 100)["strict"], False)
    check("3-tile cycle IS locked at max_tiles=3",
          analyze_bot_lock([A, B, C] * 100, max_tiles=3)["strict"], True)

    # MAX_DWELL binds in both directions.  THIS IS THE CLAUSE THAT SEPARATES AN
    # OSCILLATION FROM A STALL — without it the v125 rate reads 41.5%, not 11.6%.
    check("parked bot is NOT locked (stall, long dwell)",
          analyze_bot_lock([A] * 600)["strict"], False)
    check("parked bot IS locked at max_dwell=600",
          analyze_bot_lock([A] * 600, max_dwell=600)["strict"], True)
    check("dwell-2 alternation is locked",
          analyze_bot_lock([A, A, B, B] * 50)["strict"], True)
    check("dwell-3 alternation is NOT locked",
          analyze_bot_lock([A, A, A, B, B, B] * 50)["strict"], False)
    check("dwell-3 alternation IS locked at max_dwell=3",
          analyze_bot_lock([A, A, A, B, B, B] * 50, max_dwell=3)["strict"], True)

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
    check("short track inert", analyze_bot_lock([A, B] * 5)["strict"], False)
    check("empty track inert", analyze_bot_lock([])["strict"], False)

    # find_windows merges overlaps rather than emitting one window per round
    check("one long window stays one",
          find_windows([A, B] * 200), [(0, 399)])

    # map fingerprinting, driven to all three verdicts
    idx = map_index()
    if idx["grid"]:
        (w, h, rows), name = next(iter(sorted(idx["grid"].items(), key=lambda kv: kv[1])))
        cores = None
        for sig, names in idx["sig"].items():
            if names == {name}:
                cores = {0: sig[2], 1: sig[3]}
                break
        check("known map resolves exactly", identify_map(w, h, rows, cores), name)
        bad = list(rows)
        bad[0] = tuple((v + 1) % 3 for v in bad[0])
        # a re-gridded map still resolves, but flagged with '*'
        check("re-gridded map -> signature hit", identify_map(w, h, bad, cores),
              name + "*")
        # ...and with no signature to fall back on it must refuse, not guess
        check("re-gridded, no signature -> UNKNOWN",
              identify_map(w, h, bad, {0: (99, 99), 1: (98, 98)}), "UNKNOWN")
        check("wrong dims -> UNKNOWN", identify_map(w + 1, h, rows, cores), "UNKNOWN")
        # midgard/ragnarok share dims AND cores: the signature stage must refuse
        shared = [s for s, n in idx["sig"].items() if len(n) > 1]
        if shared:
            s = shared[0]
            check("ambiguous signature -> UNKNOWN",
                  identify_map(s[0], s[1], [(9, 9)], {0: s[2], 1: s[3]}), "UNKNOWN")
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
    ap.add_argument("--max-tiles", type=int, default=MAX_TILES)
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
        rec = census_game(args.game, args.team, args.min_span, args.max_tiles,
                          args.max_dwell, args.maps)
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
            rec = census_game(path, team, args.min_span, args.max_tiles,
                              args.max_dwell, args.maps)
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
    agg["max_tiles"] = args.max_tiles
    agg["max_dwell"] = args.max_dwell
    if args.report:
        print(f"population {len(pop)} games, parse errors {errors}, "
              f"MIN_SPAN={args.min_span} MAX_TILES={args.max_tiles} "
              f"MAX_DWELL={args.max_dwell}")
        print_report(agg)
    else:
        print(json.dumps({k: v for k, v in agg.items() if k != "per_map"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
