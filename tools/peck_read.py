#!/usr/bin/env python3
"""LOKI-19 bars 5a (DOSE) and 5b (MECHANISM) read: builder attacks on the
enemy-core footprint, from archived replays.

Prereg: docs/prereg/PREREG-loki19-core-peck-2026-08-11.md, section 5.
  5a DOSE       -- builder attacks on the enemy-core footprint, per game,
                   ours, live unrated. Treatment > 0, control ~= 0.
  5b MECHANISM  -- enemy-core HP removed by builder melee (2 dmg/swing),
                   per game, ours.

⛔ WHY THIS FILE EXISTS INSTEAD OF A QUERY ON throws.tsv:
`tools/corpus/replay_throws.py:134` admits ONLY `kind == 'INSERT'` bots into
its `active` dict (the launcher-kidnap tracker), so `corpus/throws.tsv`'s
`core_atk` column counts pecks by FERRIED bots ONLY and reads structurally 0
for every builder that walked there, built there, or was never launcher-
inserted at all. Bar 5a is about ALL our builders. Do not reach for
throws.tsv for this bar -- it is silently zero by construction, not by
measurement.

MACHINERY REUSED FROM `tools/ring_read.py` (LOKI-16's blessed ring decoder),
per the standing rule against re-deriving a protobuf parser:
  * `fields`, `read_pos`, `WIRE_LEN` -- imported from `tools/replay_census.py`
    exactly as ring_read.py imports them.
  * Seat resolution + the seat-validation check (decoded winner tally must
    reproduce the platform's `scoreA`) -- copied from ring_read.py's
    `run_arm`, verbatim in spirit. This is the reason the tool is
    trustworthy; do not drop it.
  * The synthetic-replay fixture writer (`_sf_v`, `_sf_l`, `_sf_pos`,
    `_sf_entity`, `_sf_place`, `_sf_turn`, `_sf_replay`) is IMPORTED from
    ring_read.py unmodified, plus one new helper (`_sf_attack`) for the
    `BuilderAttack` update this file actually needs to write, which
    ring_read.py never emits. `_sf_move`/`_sf_remove` are not imported --
    this decoder never needs an attacker's own position (the target tile is
    already in the event), so no fixture cell here moves or removes a
    builder mid-game.

FACTS THIS DECODER LEANS ON (tools/replay_schema.md):
  * `Update.builderAttack` is field 13: `BuilderAttack{ id=1, target=2 }`.
    Same shape as `MoveBuilderBot{id=1, to=2}` -- `id` is the ACTING
    builder's entity id, `target` is the attacked tile (a `Pos`, not an
    entity id: a builder attack always damages the BUILDING standing on that
    tile, per the schema's damage-target law).
  * Cores are NEVER placed by an update; they exist only in `map.cores`
    (Map field 4: `CorePosition{id=1, team=2, position=3}`).
  * A Core's `position` is the NW corner of its 2x2 footprint:
    `{(x,y), (x+1,y), (x,y+1), (x+1,y+1)}`. The visualiser additionally
    treats a 3x3 block around `position` as "belonging to the Core" for its
    own delivery-target lookup -- that is a DELIBERATE SUPERSET and NOT the
    footprint this decoder must use. The OFF_FOOTPRINT and CORNER_CLIPPED
    selftest cells below exist specifically to catch a decoder that
    accidentally reaches for the 3x3 superset instead of the 2x2 footprint.
  * `turns[i]` IS round `i`, 0-based.
  * The attacker's TEAM comes from tracking `placeEntity` ids -> team
    (`moveBuilderBot` only changes position, never team; `removeEntity`
    would only need to matter here if an id were reused after death, which
    is not observed and not handled, exactly as ring_read.py's `team_of`
    is never popped either).

WHAT THIS FILE DOES NOT DO: it does not use builder POSITION at all -- the
attack's `target` field already names the tile, so no `moveBuilderBot`
tracking is needed for the attacker's own position (unlike ring_read.py,
which needs live positions because occupancy is a standing-body question).

Usage: python3 tools/peck_read.py scratchpad/arm_loki19_ctrl_w1.txt [more.txt ...]
       python3 tools/peck_read.py --selftest

Gate on the printed `PECK_READ_SELFTEST: PASS` token, never on `$?`.
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
from ring_read import (  # noqa: E402  -- reuse the fixture writer, do not re-derive it
    _sf_v, _sf_l, _sf_pos, _sf_entity, _sf_place, _sf_turn, _sf_replay,
)

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
# _sf_move/_sf_remove are NOT imported: this decoder never needs an attacker's
# own position (the BuilderAttack.target field already names the tile), so no
# fixture cell here moves or removes a builder mid-game.

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"   # OpenSverige
ARCHIVE = ROOT / "replay_archive"


def ids_from_file(p: Path) -> list[str]:
    out = []
    for line in p.read_text().splitlines():
        if '"matchId"' in line:
            out.append(json.loads(line[line.index("{"):])["matchId"])
    return out


def core_footprint(pos: tuple[int, int]) -> set[tuple[int, int]]:
    """2x2 footprint, NW corner convention. NOT the visualiser's 3x3 superset."""
    x, y = pos
    return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


def decode(path: Path, our_team: int):
    """-> dict of per-game peck metrics, or None if unparseable.

    our_core_atk / our_total_atk / our_hp_removed are OURS (team `our_team`).
    opp_* are the live control column: the same three numbers for the other
    team, attacking OUR footprint. Both are computed in one pass so the
    control costs nothing extra and is never a separate, driftable query.
    """
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

    cores = []
    for num, wire, value in fields(map_buf):
        if num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(2, 0), read_pos(d[3])))
    footprint: dict[int, set] = {}
    for team, pos in cores:
        footprint.setdefault(team, set()).update(core_footprint(pos))
    if 0 not in footprint or 1 not in footprint:
        return None   # both teams' cores must be present to score either side

    their_team = 1 - our_team
    team_of: dict[int, int] = {}
    our_core_atk = our_total_atk = 0
    opp_core_atk = opp_total_atk = 0
    unresolved = 0   # attacker id never seen via placeEntity -- can't attribute a team

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:              # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        team_of[e.id] = e.team
                elif unum == 13:           # builderAttack
                    aid, tgt = None, None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if aid is None or tgt is None:
                        continue
                    atk_team = team_of.get(aid)
                    if atk_team is None:
                        unresolved += 1
                        continue
                    if atk_team == our_team:
                        our_total_atk += 1
                        if tgt in footprint[their_team]:
                            our_core_atk += 1
                    elif atk_team == their_team:
                        opp_total_atk += 1
                        if tgt in footprint[our_team]:
                            opp_core_atk += 1
                    # a third team value is impossible (Team is A/B only); no
                    # else branch needed and none is silently swallowed.

    return {
        "rounds": len(turn_bufs),
        "winner": winner,
        "our_core_atk": our_core_atk,
        "our_total_atk": our_total_atk,
        "our_hp_removed": our_core_atk * 2,
        "opp_core_atk": opp_core_atk,
        "opp_total_atk": opp_total_atk,
        "opp_hp_removed": opp_core_atk * 2,
        "unresolved_attacks": unresolved,
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
        # SEAT CHECK, carried over from ring_read.py verbatim in spirit: the
        # replay-side winner tally must reproduce the platform's scoreA. If
        # seat mapping (replay Team 0 == platform teamA) were wrong, or if
        # our_team were assumed instead of resolved, this is where it breaks.
        seat_check.append((mid, wins_a, meta["scoreA"], n, meta["scoreB"]))
    return games, per_opp, seat_check


def pct(xs):
    xs = sorted(xs)
    if not xs:
        return "n/a"
    q = lambda f: xs[min(len(xs) - 1, int(f * len(xs)))]
    return (f"n={len(xs)} min={xs[0]} p25={q(.25)} med={statistics.median(xs):.1f} "
            f"p75={q(.75)} p90={q(.90)} max={xs[-1]} mean={statistics.mean(xs):.2f}")


def _rate(games, key):
    hit = len([g for g in games if g[key] > 0])
    return f"{hit}/{len(games)} = {hit/len(games):.1%}" if games else "n/a"


def report(label, games, per_opp, seat_check):
    print(f"\n{'='*78}\n=== {label}  (n={len(games)} games, "
          f"{len(seat_check)} matches) ===\n{'='*78}")
    bad = [s for s in seat_check if s[1] != s[2] or s[3] != 5]
    print(f"  SEAT/PARSE VALIDATION: replay winner tally == platform scoreA in "
          f"{len(seat_check)-len(bad)}/{len(seat_check)} matches"
          + ("" if not bad else f"  ** MISMATCH: {bad}"))
    unres = sum(g["unresolved_attacks"] for g in games)
    if unres:
        print(f"  ** {unres} builderAttack event(s) with an unresolved attacker "
              f"team (id never seen via placeEntity) -- excluded from all counts "
              f"below, not attributed to either side.")

    vers = Counter((g["ourver"], g["opp"], g["oppver"], g["seat"]) for g in games)
    print("  our_ver / opponent / opp_ver / seat  -> games")
    for k, v in sorted(vers.items()):
        print(f"    v{k[0]:<4} {k[1]:<22} oppv{k[2]:<4} seat {k[3]}  {v}")

    print(f"\n  -- 5a DOSE: builder attacks on the enemy-core footprint, per game --")
    print(f"    OURS  core-peck/game:      {pct([g['our_core_atk'] for g in games])}")
    print(f"          games with >=1 peck: {_rate(games, 'our_core_atk')}")
    print(f"          total attacks/game (any target): "
          f"{pct([g['our_total_atk'] for g in games])}")
    print(f"    OPP   core-peck/game:      {pct([g['opp_core_atk'] for g in games])}"
          f"   [live control column]")
    print(f"          games with >=1 peck: {_rate(games, 'opp_core_atk')}")
    print(f"          total attacks/game (any target): "
          f"{pct([g['opp_total_atk'] for g in games])}")

    print(f"\n  -- 5b MECHANISM: enemy-core HP removed by builder melee "
          f"(2 dmg/swing), per game --")
    print(f"    OURS  HP removed/game: {pct([g['our_hp_removed'] for g in games])}")
    print(f"    OPP   HP removed/game: {pct([g['opp_hp_removed'] for g in games])}"
          f"   [live control column]")

    print(f"\n  -- PER OPPONENT (dose + mechanism, both sides) --")
    print(f"    {'opponent':<24}{'n':>4}{'our_pk':>8}{'our_tot':>9}{'our_hp':>8}"
          f"{'opp_pk':>8}{'opp_tot':>9}{'opp_hp':>8}")
    for opp in sorted(per_opp):
        gs = per_opp[opp]
        mo = lambda k: statistics.mean(g[k] for g in gs)
        print(f"    {opp:<24}{len(gs):>4}{mo('our_core_atk'):>8.2f}"
              f"{mo('our_total_atk'):>9.2f}{mo('our_hp_removed'):>8.2f}"
              f"{mo('opp_core_atk'):>8.2f}{mo('opp_total_atk'):>9.2f}"
              f"{mo('opp_hp_removed'):>8.2f}")

    print(f"\n  TOTAL: {len(games)} games across {len(seat_check)} matches "
          f"in this arm file.")
    return {
        "our_core_atk_mean": statistics.mean(g["our_core_atk"] for g in games)
        if games else 0.0,
        "opp_core_atk_mean": statistics.mean(g["opp_core_atk"] for g in games)
        if games else 0.0,
    }


# =============================================================================
# SELFTEST -- forced-answer cells, real engine protobuf, decode() unmodified.
# =============================================================================
#
# The fixture writer (_sf_v/_sf_l/_sf_pos/_sf_entity/_sf_place/_sf_turn/
# _sf_replay) is IMPORTED from ring_read.py, unmodified. The one addition
# this file needs is _sf_attack, for the BuilderAttack update ring_read.py
# never emits -- same shape as MoveBuilderBot (id=varint field 1, then a Pos
# submessage field 2), just field number 13.

def _sf_attack(eid: int, xy) -> bytes:               # Update{builderAttack{id,target}}
    return _sf_l(13, _sf_v(1, eid) + _sf_l(2, _sf_pos(xy)))


# --- fixture geometry ---------------------------------------------------------
# Same 12x12 all-EMPTY map as ring_read.py's selftest, 40 rounds (attacks don't
# need ring_read's 100-round occupancy horizon). Our core id=1 team=0 at
# (1,1) -> our footprint {(1,1),(2,1),(1,2),(2,2)}. Enemy core id=2 team=1 at
# (8,8) -> enemy footprint {(8,8),(9,8),(8,9),(9,9)}.
_SF_W = _SF_H = 12
_SF_N = 40
_SF_CORES = [(1, 0, (1, 1)), (2, 1, (8, 8))]
_SF_ENEMY_FP_TILE = (9, 9)     # in the enemy 2x2 footprint
_SF_OFF_FP_TILE = (7, 8)       # orthogonally adjacent to (8,8), NOT in the 2x2
                                # footprint, but INSIDE the visualiser's 3x3
                                # superset {7,8,9}x{7,8,9} around (8,8) -- this
                                # is the tile that separates a correct decoder
                                # from one that reached for the 3x3 block.
_SF_OUR_FP_TILE = (1, 1)       # in OUR 2x2 footprint (the NW corner itself)


def _sf_blank_turns(n=_SF_N):
    return [[] for _ in range(n)]


def _sf_cells():
    """-> [(name, why_forced, replay_bytes, our_team, [(label, forced, key)])]

    Every forced answer is forced BY CONSTRUCTION -- arithmetic on the
    fixture, never a stored figure.
    """
    cells = []

    def add(name, why, turns, our_team, checks, cores=None):
        cells.append((name, why,
                      _sf_replay(_SF_W, _SF_H, cores or _SF_CORES, turns),
                      our_team, checks))

    # 1. FLOOR -- our builder exists but never attacks anything.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (2, 2), "builder_bot"))]
    add("FLOOR_no_attacks",
        "our sole builder placed, zero builderAttack updates all game",
        t, 0,
        [("our_core_atk", 0, lambda g: g["our_core_atk"]),
         ("our_total_atk", 0, lambda g: g["our_total_atk"]),
         ("our_hp_removed", 0, lambda g: g["our_hp_removed"]),
         ("opp_core_atk", 0, lambda g: g["opp_core_atk"])])

    # 2. CEILING -- our builder lands N=5 swings, all on the SAME enemy-core
    # footprint tile.
    N = 5
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (7, 9), "builder_bot"))]
    for i, rnd in enumerate((2, 5, 8, 11, 14)):
        t[rnd] = [_sf_attack(10, _SF_ENEMY_FP_TILE)]
    add("CEILING_N5_on_footprint",
        f"our builder swings {N}x at {_SF_ENEMY_FP_TILE} (in the enemy 2x2 "
        f"footprint): count must be exactly {N}, HP removed {2*N}",
        t, 0,
        [("our_core_atk", N, lambda g: g["our_core_atk"]),
         ("our_total_atk", N, lambda g: g["our_total_atk"]),
         ("our_hp_removed", 2 * N, lambda g: g["our_hp_removed"]),
         ("opp_core_atk", 0, lambda g: g["opp_core_atk"])])

    # 3. OFF-FOOTPRINT -- the cell that separates a correct 2x2 footprint from
    # the visualiser's 3x3 superset. Our builder swings N=4 times at a tile
    # orthogonally adjacent to the enemy core but NOT inside its 2x2
    # footprint. core-peck must read 0 while total-attacks reads N.
    N = 4
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (7, 9), "builder_bot"))]
    for rnd in (2, 5, 8, 11):
        t[rnd] = [_sf_attack(10, _SF_OFF_FP_TILE)]
    add("OFF_FOOTPRINT_adjacent_not_in",
        f"our builder swings {N}x at {_SF_OFF_FP_TILE}: orthogonally adjacent "
        f"to enemy core (8,8) and inside the visualiser's 3x3 superset, but "
        f"NOT one of the 4 tiles in the true 2x2 footprint. core-peck must be "
        f"0; total-attacks must be {N}.",
        t, 0,
        [("our_core_atk", 0, lambda g: g["our_core_atk"]),
         ("our_total_atk", N, lambda g: g["our_total_atk"]),
         ("our_hp_removed", 0, lambda g: g["our_hp_removed"])])

    # 4. TEAM CONTROL -- the ENEMY builder attacks OUR core footprint N=3
    # times; ours attacks nothing. A decoder with no team check would read N
    # for us instead of 0.
    N = 3
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(20, 1, (3, 1), "builder_bot"))]
    for rnd in (1, 4, 7):
        t[rnd] = [_sf_attack(20, _SF_OUR_FP_TILE)]
    add("TEAM_enemy_attacks_our_footprint",
        f"a TEAM-1 builder swings {N}x at {_SF_OUR_FP_TILE} (in OUR 2x2 "
        f"footprint) while we (team 0) attack nothing: our_core_atk must "
        f"stay 0 and the opponent column must read {N}.",
        t, 0,
        [("our_core_atk", 0, lambda g: g["our_core_atk"]),
         ("our_total_atk", 0, lambda g: g["our_total_atk"]),
         ("opp_core_atk", N, lambda g: g["opp_core_atk"]),
         ("opp_total_atk", N, lambda g: g["opp_total_atk"]),
         ("opp_hp_removed", 2 * N, lambda g: g["opp_hp_removed"])])

    # 5. SEAT CONTROL -- CEILING's own bytes, decoded from the OPPOSITE seat.
    # The attacker (team 0) and target (team-1's footprint) don't move; only
    # which side is "ours" does. The numbers must swap: our_core_atk 5->0,
    # opp_core_atk 0->5.
    N = 5
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (7, 9), "builder_bot"))]
    for rnd in (2, 5, 8, 11, 14):
        t[rnd] = [_sf_attack(10, _SF_ENEMY_FP_TILE)]
    add("SEAT_ceiling_bytes_other_seat",
        f"CEILING's exact bytes decoded with our_team=1: the attacker was "
        f"team 0 (now the opponent) hitting team 1's footprint (now ours' "
        f"target from the opponent's side). our_core_atk must read 0 "
        f"(was {N}) and opp_core_atk must read {N} (was 0) -- numbers swap.",
        t, 1,
        [("our_core_atk", 0, lambda g: g["our_core_atk"]),
         ("opp_core_atk", N, lambda g: g["opp_core_atk"])])

    # 6. CORNER-CLIPPED footprint -- enemy core at (0,0), footprint
    # {(0,0),(1,0),(0,1),(1,1)}. An attack on (0,0) is in the footprint; an
    # attack on (2,0) (two tiles east, orthogonally adjacent to the footprint
    # tile (1,0) but not itself in it) is not.
    t = _sf_blank_turns()
    t[0] = [_sf_place(_sf_entity(10, 0, (5, 5), "builder_bot"))]
    t[2] = [_sf_attack(10, (0, 0))]
    t[6] = [_sf_attack(10, (2, 0))]
    add("CORNER_CLIPPED_footprint",
        "enemy core at (0,0): footprint is {(0,0),(1,0),(0,1),(1,1)}. Attack "
        "on (0,0) -> in footprint (count 1); attack on (2,0) -> not in "
        "footprint (count 0). our_core_atk must be exactly 1, "
        "our_total_atk exactly 2.",
        t, 0,
        [("our_core_atk", 1, lambda g: g["our_core_atk"]),
         ("our_total_atk", 2, lambda g: g["our_total_atk"]),
         ("our_hp_removed", 2, lambda g: g["our_hp_removed"])],
        cores=[(1, 0, (9, 9)), (2, 1, (0, 0))])

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

    Prints a terminal `PECK_READ_SELFTEST: PASS|FAIL` token -- gate on the
    TOKEN, not on `$?` (which is the pipe's status behind a pager/tee).
    """
    import tempfile
    from replay_census import Replay  # independent parser: fixture cross-check

    tmp = Path(tempfile.mkdtemp(prefix="peck_read_selftest_"))
    print("PECK_READ SELFTEST -- forced-answer cells, real engine protobuf, "
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
        # independently-written replay_census parser. A fixture only this
        # file can read proves nothing about this file.
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
            print(f"       {'ok  ' if ok else 'FAIL'}  {label:<18}"
                  f" forced {forced!r:<8} observed {obs!r}")
    print(f"\n  {n_ok} assertions passed, {n_fail} failed, "
          f"over {len(_sf_cells())} cells")
    for f in fails:
        print(f"    FAILED: {f[0]} :: {f[1]} :: {f[2]}")
    print("\n  WHAT THIS DOES NOT COVER: aggregation across games (run_arm/"
          "report are untested here); real-replay geometry beyond these "
          "cells; multiple cores per team; and an attacker id that is reused "
          "by the engine after its original entity died (unhandled, same as "
          "ring_read.py's team_of/kind_of, which are also never popped on "
          "removeEntity).")
    print(f"\nPECK_READ_SELFTEST: {'PASS' if n_fail == 0 else 'FAIL'}")
    return 1 if n_fail else 0


# =============================================================================
# MUTATION TEST OF THE SELFTEST ITSELF -- run once, recorded here, not part of
# normal execution. A selftest that passes on both the real file and a
# deliberately broken copy is worthless (this is the exact defect
# `ring_retention.py --selftest` had: it passed while its occupancy rule was
# wrong, because it only ever exercised ring GEOMETRY).
#
# DECLARED MUTANT: widen `core_footprint()` from the true 2x2
#   {(x,y), (x+1,y), (x,y+1), (x+1,y+1)}
# to the visualiser's 3x3 superset
#   {(x-1..x+1), (y-1..y+1)}   (9 tiles instead of 4)
# -- i.e. reach for the same superset the schema doc warns is NOT the
# footprint. This is the decoder's own specific risk (unlike a team-check
# drop, which is a generic risk shared with every team-scoped decoder), so it
# is the mutation exercised here.
#
# Recipe (run against a SCRATCH COPY, never against tools/):
#
#   d=$(mktemp -d); mkdir -p $d/tools
#   cp tools/replay_census.py tools/ring_read.py $d/tools/
#   python3 - "$d/tools/peck_read.py" <<'PY'
#   import re, sys
#   src = open("tools/peck_read.py").read()
#   old = ("def core_footprint(pos: tuple[int, int]) -> set[tuple[int, int]]:\n"
#          '    """2x2 footprint, NW corner convention. NOT the visualiser\'s 3x3 superset."""\n'
#          "    x, y = pos\n"
#          "    return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}\n")
#   new = ("def core_footprint(pos: tuple[int, int]) -> set[tuple[int, int]]:\n"
#          '    """MUTATED: 3x3 superset, not the true 2x2 footprint."""\n'
#          "    x, y = pos\n"
#          "    return {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}\n")
#   assert old in src
#   open(sys.argv[1], "w").write(src.replace(old, new))
#   PY
#   python3 $d/tools/peck_read.py --selftest    # must print PECK_READ_SELFTEST: FAIL
#
# OBSERVED (run 2026-08-11, this repo, scratch copy at
# $SCRATCHPAD/peck_read_mutant/tools/peck_read.py, ring_read.py and
# replay_census.py copied in unmodified alongside it):
#
#   CELL OFF_FOOTPRINT_adjacent_not_in
#        FAIL  our_core_atk       forced 0        observed 4
#        FAIL  our_hp_removed     forced 0        observed 8
#        (our_total_atk still ok at 4 -- it doesn't depend on footprint width)
#   CELL CORNER_CLIPPED_footprint  -- STILL PASSES under this mutation. The
#        enemy core sits at (0,0), so even the mutated 3x3 superset is only
#        {-1,0,1}x{-1,0,1}; the off-footprint probe tile (2,0) is 2 tiles away
#        in x and falls outside BOTH the true 2x2 and the mutated 3x3, so this
#        cell cannot distinguish the two footprint definitions at this corner.
#        (Recorded here so the next reader doesn't expect it to fail too.)
#
#   19 assertions passed, 2 failed, over 6 cells
#   PECK_READ_SELFTEST: FAIL
#
# Confirms OFF_FOOTPRINT_adjacent_not_in is the cell that separates the two
# footprint definitions, and it is the one designed to (its probe tile (7,8)
# is one step outside the true 2x2 but still inside the mutated 3x3 -- by
# construction, not by luck). The mutant's PECK_READ_SELFTEST token read
# FAIL, not PASS, and the real file (verified immediately above) reads PASS.
# =============================================================================


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for f in sys.argv[1:]:
        fp = Path(f)
        games, per_opp, sc = run_arm(fp)
        report(fp.name, games, per_opp, sc)
