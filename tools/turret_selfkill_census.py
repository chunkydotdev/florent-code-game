#!/usr/bin/env python3
"""Do opponents' GUNNERS/SENTINELS destroy themselves by firing at zero ammo?

THE MECHANISM BEING TESTED (engine facts, per CLAUDE.md / the guard-matrix read
`docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md` -- NOT re-derived
here, but every one of them is load-bearing so they are written down):

  * turrets fire from a TEAM-GLOBAL ammo pool; gunner 4/shot, sentinel 10/shot.
  * `can_fire@0x16280` contains NO ammo reference -- it returns TRUE at 0 ammo.
    The real check lives in `finish_firing_turret@0x26eac` and RAISES.
  * an exception escaping `run()` makes the engine PERMANENTLY destroy that unit
    (`0x1ac5c` -> `Game::destroy_entity`).

=> a bot that trusts `can_fire()` and calls `fire()` with less ammo than the shot
costs destroys its own turret, with NO damage event, on that round.

WHY THIS IS NOT `tools/crash_census.py` ALL OVER AGAIN
=====================================================
`crash_census.py` buckets EVERY `removeEntity` by one bit: "did this id ever have
an `updateHp` event". No-hp + a code-running kind => `crash_candidate`. That
number (11,239 league-wide; 2,451 for opponents in 1,855 of our games) is a
4-way conflation it states honestly: crash / self_destruct / friendly destroy() /
resign. It has NO ammo axis, NO adjacency axis, and no per-opponent attribution
(its `OUR_TEAM_ID` constant is defined and never used). It cannot answer this
question. This tool adds exactly the three axes that separate the ammo story
from the teardown story, and reports the base rate that says whether they
separate at all:

  1. **AMMO AT THE MOMENT OF DEATH.** `Update.updatePlayers` (field 6) carries
     `Player.ammo` (field 7) for BOTH teams EVERY round -- verified 246/246
     rounds on the first archive file probed. If the turret raised inside
     `finish_firing_turret`, the team's ammo balance was BELOW that turret's shot
     cost when it did, and (because the raise consumes nothing) it is still below
     it at end of round. `ammo_end[R] < cost` is therefore NECESSARY.
     It is not sufficient -- see THE BASE-RATE PROBLEM below, which is the whole
     reason this tool prints a control column instead of a headline.
  2. **FRIENDLY-BUILDER ADJACENCY.** `destroy()` needs a friendly builder bot on
     an ORTHOGONALLY adjacent tile. Turrets ARE buildings, so a teardown is the
     single largest non-crash explanation for a turret vanishing undamaged. If no
     friendly builder was anywhere adjacent during that round, destroy() was
     impossible and the teardown branch is excluded on geometry.
     (`self_destruct()` is a builder-bot action and `resign()` kills the core;
     neither can remove a turret. So for GUNNER/SENTINEL specifically the 4-way
     conflation collapses to 2: crash, or friendly teardown.)
  3. **HEAL vs DAMAGE.** `updateHp.delta` is signed and a friendly heal is +4.
     `crash_census` keys on "ever had an hp event" and so silently reclassifies a
     HEALED-then-crashed turret as a damage death. This tool splits the sign, and
     reports `HEALED_ONLY` as its own class rather than folding it either way.

THE BASE-RATE PROBLEM, STATED BEFORE THE RESULT
===============================================
Teams sit at ammo 0 for large stretches of a game. "Died while ammo < cost" is
worth nothing unless it is rarer among turrets that demonstrably died some OTHER
way. So every run prints the SAME ammo statistic over the DAMAGE_DEATH turrets
-- turrets killed by measured HP loss, which by construction did not crash. If
the two rates match, the ammo axis does not discriminate and this tool says so.
That control column is not decoration; read it before reading anything else.

CLASSES (one per turret LIFE that ended in a `removeEntity`)
============================================================
  DAMAGE_DEATH             >=1 `updateHp` with a NEGATIVE delta.
  HEALED_ONLY              >=1 `updateHp`, all POSITIVE (healed, never damaged),
                           then vanished. A crash candidate that `crash_census`
                           calls a damage death.
  TEARDOWN_CONSISTENT      no hp event ever, AND a friendly builder bot occupied
                           an orthogonally adjacent tile at some point in the
                           removal round -> `destroy()` was available.
  SELFKILL_BATTERY_EXHAUSTED
                           ⭐ the sharp class. All of SELFKILL_AMMO_CONSISTENT,
                           PLUS: the team COMPLETED >=1 turret shot that round
                           (the pool was being actively drained, not merely flat
                           at zero all game) AND this turret emitted NO
                           `fireTurret` of its own that round (its fire() never
                           completed). This is the wire fingerprint of "more
                           turrets were ready to fire than the pool could pay
                           for" -- hand-verified below.
  SELFKILL_AMMO_CONSISTENT no hp event, NO friendly builder adjacent (teardown
                           geometrically impossible), AND `ammo_end[R] < cost`,
                           but WITHOUT the battery fingerprint (e.g. the team
                           had been flat at 0 ammo for the whole game, so the
                           ammo coincidence is cheap).
  CRASH_AMMO_RICH          no hp event, no friendly builder adjacent, but the
                           team had ENOUGH ammo -> a crash from some other cause
                           (the negative-space control for class 4).
  UNRESOLVED               the file could not answer for this turret (no ammo
                           snapshot for that round, id removed before it was ever
                           placed, ...). ⛔ THIS IS A DISTINCT VALUE FROM EVERY
                           CLEAN RESULT ABOVE, ON PURPOSE: this repo's signature
                           failure is an error path that renders identically to a
                           clean negative. `UNRESOLVED` is never summed into any
                           rate; it is printed on its own line.

WHAT THIS STILL CANNOT DO
=========================
  * It cannot see a traceback (replays carry none; `stdout` is stripped on
    platform-downloaded files -- 0 of 30,664 `BotOutput` events carry text).
  * `SELFKILL_AMMO_CONSISTENT` is CONSISTENT WITH, not PROOF OF, the ammo
    mechanism. Any uncaught exception whatsoever, raised on a round when the team
    happened to be ammo-poor, lands in it. The base-rate control is what turns it
    into a claim, and only if the control comes out low.
  * A turret torn down by a builder standing adjacent for OTHER reasons is
    counted `TEARDOWN_CONSISTENT` even if it actually crashed. That direction is
    deliberate: it costs recall, not precision, on the class being claimed.

USAGE
=====
    .venv/bin/python tools/turret_selfkill_census.py --selftest
    .venv/bin/python tools/turret_selfkill_census.py replay_archive/ --limit 500
    .venv/bin/python tools/turret_selfkill_census.py replay_archive/ \\
        --meta corpus/meta_join.tsv --by-opponent
    .venv/bin/python tools/turret_selfkill_census.py --detail <file> <entity_id>

Reuses `tools/replay_census.py`'s wire primitives (`fields`, `parse_entity`,
`read_pos`, `WIRE_LEN`) and `tools/corpus/replay_throws.py`'s synthetic-replay
encoders for the self-test -- no third protobuf walker is written here.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "tools")
sys.path.insert(0, "tools/corpus")
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

ROOT = Path(__file__).resolve().parents[1]

TEAM_NAME = {0: "A", 1: "B"}
TURRET_KINDS = ("gunner", "sentinel")
# Per-shot ammo cost from the team-global pool (CLAUDE.md entity table).
# Launchers use NO ammo, so they CANNOT die to this mechanism and are excluded
# from the population entirely rather than silently swept in.
SHOT_COST = {"gunner": 4, "sentinel": 10}

ORTHO = ((0, -1), (0, 1), (-1, 0), (1, 0))

CLASSES = ("DAMAGE_DEATH", "HEALED_ONLY", "TEARDOWN_CONSISTENT",
           "SELFKILL_BATTERY_EXHAUSTED", "SELFKILL_AMMO_CONSISTENT", "CRASH_AMMO_RICH")
SELFKILL_CLASSES = ("SELFKILL_BATTERY_EXHAUSTED", "SELFKILL_AMMO_CONSISTENT")
UNRESOLVED = "UNRESOLVED"


# --------------------------------------------------------------------------
# core walk
# --------------------------------------------------------------------------
def census(path: Path, keep_detail: bool = False) -> dict:
    """Walk one replay; return per-turret-life records plus file-level context.

    Raises on a file that is not a replay -- callers count those as errors and
    NEVER as "no self-kills found".
    """
    data = path.read_bytes()
    map_buf = None
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        raise ValueError(f"{path}: no battlecode.Map (field 1) -- not a replay?")

    # entity id -> dict. Cores seeded from map.cores (never emitted as updates).
    ents: dict[int, dict] = {}
    for num, _w, value in fields(map_buf):
        if num == 4:
            cid = cteam = None
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    cid = cv
                elif cn == 2:
                    cteam = cv
            if cid is not None:
                ents[cid] = {"team": cteam, "kind": "core", "pos": None}

    # per-round end-of-round ammo, per team. index = round.
    ammo = {0: [], 1: []}
    turrets: dict[int, dict] = {}       # id -> live record
    finished: list[dict] = []
    bot_pos: dict[int, tuple[int, int]] = {}    # builder bot id -> current tile
    tile_turret: dict[tuple[int, int], int] = {}  # tile -> live turret id

    for rnd, turn_buf in enumerate(turn_bufs):
        # tiles any builder bot of each team touched THIS round (start position
        # plus every move destination) -- destroy() only needs adjacency at some
        # point in the round, and update order inside a round is not reliable.
        round_tiles = {0: set(), 1: set()}
        for bid, p in bot_pos.items():
            t = ents.get(bid, {}).get("team")
            if t in round_tiles:
                round_tiles[t].add(p)
        pending_removals: list[tuple[int, dict]] = []
        ammo_this = {0: None, 1: None}
        # ⭐ shots each team COMPLETED this round, and which turrets completed
        # them. `fireTurret` is emitted on a shot that went through; a turret
        # whose fire() raised inside finish_firing_turret emits none. See the
        # BATTERY-EXHAUSTION class below for why this is the sharp column.
        team_shots = {0: 0, 1: 0}
        fired_ids: set[int] = set()

        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            # rotation / re-emit: same id placed again. Keep the
                            # original record (crash_census uses the same guard).
                            continue
                        ents[e.id] = {"team": e.team, "kind": e.kind, "pos": e.pos}
                        if e.kind == "builder_bot":
                            bot_pos[e.id] = e.pos
                            if e.team in round_tiles:
                                round_tiles[e.team].add(e.pos)
                        elif e.kind in SHOT_COST:
                            turrets[e.id] = {
                                "id": e.id, "team": e.team, "kind": e.kind,
                                "pos": e.pos, "born": rnd,
                                "hp_neg": 0, "hp_pos": 0,
                                "attacked_by": Counter(),   # team -> builder attacks on its tile
                                "fired_at_by": Counter(),   # team -> turret shots landing on its tile
                                "shots": 0,
                                "detail": [] if keep_detail else None,
                            }
                            tile_turret[e.pos] = e.id
                elif unum == 2:                                 # moveBuilderBot
                    bid = None
                    to = None
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            bid = v2
                        elif n2 == 2:
                            to = read_pos(v2)
                    if bid is not None and to is not None:
                        bot_pos[bid] = to
                        t = ents.get(bid, {}).get("team")
                        if t in round_tiles:
                            round_tiles[t].add(to)
                elif unum == 5:                                 # updateHp
                    eid = delta = None
                    for n2, w2, v2 in fields(ubuf):
                        if n2 == 1:
                            eid = v2
                        elif n2 == 2:
                            delta = v2
                    rec = turrets.get(eid)
                    if rec is not None and delta is not None:
                        # proto3 int32 negatives are 10-byte varints; `fields`
                        # returns the raw unsigned value, so fold it back.
                        d = delta - (1 << 64) if delta >= (1 << 63) else delta
                        if d < 0:
                            rec["hp_neg"] += 1
                        elif d > 0:
                            rec["hp_pos"] += 1
                        if rec["detail"] is not None:
                            rec["detail"].append((rnd, "hp", d))
                elif unum == 12:                                # fireTurret
                    frm = to = None
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            frm = read_pos(v2)
                        elif n2 == 2:
                            to = read_pos(v2)
                    if frm is not None:
                        sid = tile_turret.get(frm)
                        if sid is not None and sid in turrets:
                            turrets[sid]["shots"] += 1
                            fired_ids.add(sid)
                            team_shots[turrets[sid]["team"]] += 1
                    if to is not None:
                        tid = tile_turret.get(to)
                        if tid is not None and tid in turrets:
                            shooter_team = None
                            if frm is not None and tile_turret.get(frm) in ents:
                                shooter_team = ents[tile_turret[frm]]["team"]
                            turrets[tid]["fired_at_by"][shooter_team] += 1
                elif unum == 13:                                # builderAttack
                    aid = tgt = None
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            aid = v2
                        elif n2 == 2:
                            tgt = read_pos(v2)
                    if tgt is not None:
                        tid = tile_turret.get(tgt)
                        if tid is not None and tid in turrets:
                            at = ents.get(aid, {}).get("team")
                            turrets[tid]["attacked_by"][at] += 1
                            if turrets[tid]["detail"] is not None:
                                turrets[tid]["detail"].append((rnd, "attacked_by_team", at))
                elif unum == 6:                                 # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:                             # Players
                            continue
                        for tn, _tw, tv in fields(pv):          # a=1, b=2
                            team = tn - 1
                            if team not in ammo_this:
                                continue
                            val = 0
                            for fn, _fw, fv in fields(tv):
                                if fn == 7:
                                    val = fv
                            ammo_this[team] = val
                elif unum == 3:                                 # removeEntity
                    rid = None
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            rid = v2
                    if rid is None:
                        continue
                    rec = turrets.pop(rid, None)
                    meta = ents.pop(rid, None)
                    if meta is not None and meta.get("kind") == "builder_bot":
                        bot_pos.pop(rid, None)
                    if rec is not None:
                        tile_turret.pop(rec["pos"], None)
                        pending_removals.append((rnd, rec))

        for t in (0, 1):
            ammo[t].append(ammo_this[t] if ammo_this[t] is not None else None)

        for rr, rec in pending_removals:
            rec["died"] = rr
            # adjacency is evaluated over the tiles friendly builders touched in
            # the removal round; that is the window in which destroy() could fire.
            fr = round_tiles.get(rec["team"], set())
            x, y = rec["pos"]
            rec["adj_friendly_builder"] = any((x + dx, y + dy) in fr for dx, dy in ORTHO)
            rec["team_shots_at_death"] = team_shots.get(rec["team"], 0)
            rec["self_fired_at_death"] = rec["id"] in fired_ids
            finished.append(rec)

    # turrets still alive at the end are exposure, not events
    survivors = list(turrets.values())

    for rec in finished:
        rec.update(_classify(rec, ammo))
    return {
        "file": path.name,
        "path": str(path),
        "rounds": len(turn_bufs),
        "removed": finished,
        "survivors": survivors,
        "ammo": ammo,
    }


def _classify(rec: dict, ammo: dict) -> dict:
    """Classify one ended turret life. Returns the fields to merge into it."""
    rnd = rec["died"]
    team = rec["team"]
    cost = SHOT_COST[rec["kind"]]
    series = ammo.get(team) or []
    a_now = series[rnd] if 0 <= rnd < len(series) else None
    a_prev = series[rnd - 1] if 1 <= rnd - 1 < len(series) else None
    out = {"ammo_end": a_now, "ammo_prev": a_prev, "cost": cost}

    # ⭐ THE PER-EVENT NULL EXPECTATION. If the round a turret dies carries no
    # information about ammo, the chance of finding the team ammo-short at that
    # round is just the share of the turret's OWN LIFETIME the team spent below
    # that shot cost. Summed over events this is the exact expected count under
    # the null, and it is a far better control than comparing against combat
    # deaths (which are selected on being under attack, hence on late-game
    # ammo drain). `None` rounds are excluded from both numerator and
    # denominator so a truncated ammo series cannot masquerade as "not short".
    lo, hi = rec["born"], min(rnd, len(series) - 1)
    window = [v for v in series[lo:hi + 1] if v is not None]
    out["life_rounds"] = len(window)
    out["life_short_frac"] = (sum(1 for v in window if v < cost) / len(window)) if window else None

    if team not in (0, 1) or a_now is None:
        out["cls"] = UNRESOLVED
        out["why"] = "no ammo snapshot for the removal round"
        return out
    if rec["hp_neg"] > 0:
        out["cls"] = "DAMAGE_DEATH"
    elif rec["hp_pos"] > 0:
        out["cls"] = "HEALED_ONLY"
    elif rec["adj_friendly_builder"]:
        out["cls"] = "TEARDOWN_CONSISTENT"
    elif a_now < cost:
        # ⭐⭐ THE BATTERY-EXHAUSTION REFINEMENT. Hand-verified on the wire
        # (Lorem Ipsum, `030be598..._game_2`, r17): the trigger is NOT "the team
        # sat at 0 ammo". It is "MORE TURRETS WERE READY TO FIRE THIS ROUND THAN
        # THE POOL COULD PAY FOR". The battery drains the pool in turret order;
        # every turret after the pool runs dry raises and dies. The wire
        # fingerprint is exact:
        #   * the team COMPLETED >=1 shot this round (so the pool was actively
        #     being drained, not merely empty all game), AND
        #   * this turret emitted NO fireTurret of its own that round (its own
        #     fire() never completed -- it raised).
        # This is a strict subset of SELFKILL_AMMO_CONSISTENT and is much
        # harder to reach by coincidence, so it is reported separately rather
        # than folded in.
        if rec.get("team_shots_at_death", 0) >= 1 and not rec.get("self_fired_at_death"):
            out["cls"] = "SELFKILL_BATTERY_EXHAUSTED"
        else:
            out["cls"] = "SELFKILL_AMMO_CONSISTENT"
    else:
        out["cls"] = "CRASH_AMMO_RICH"
    out["ammo_short"] = a_now < cost
    return out


# --------------------------------------------------------------------------
# aggregation
# --------------------------------------------------------------------------
def load_meta(meta_path: Path) -> dict[str, dict]:
    """file -> {A: name, B: name, us_side, verA, verB}. `corpus/meta_join.tsv`.

    meta_join covers ~44k archived files; `corpus/join.tsv` covers ~3.7k. Using
    join.tsv for a league-wide denominator understates it ~10x.
    """
    out = {}
    with meta_path.open(newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out[row["file"]] = {
                0: row.get("teamAName", ""), 1: row.get("teamBName", ""),
                "verA": row.get("teamAVersion", ""), "verB": row.get("teamBVersion", ""),
                "us_side": row.get("us_side", ""),
            }
    return out


def aggregate(results: list[dict], meta: dict | None) -> dict:
    by_class = Counter()
    lives = 0
    removals = 0
    survivors = 0
    # base-rate control: ammo-short share among turrets that died of MEASURED
    # damage (they demonstrably did not crash).
    ctrl = {"n": 0, "short": 0, "exp": 0.0}
    trt = {"n": 0, "short": 0, "exp": 0.0}   # among no-hp, no-adjacency removals
    allr = {"n": 0, "short": 0, "exp": 0.0}  # every ended life, any class
    per_team = defaultdict(lambda: {"lives": 0, "removed": 0, "files": set(),
                                    **{c: 0 for c in CLASSES}, UNRESOLVED: 0,
                                    "dmg_short": 0, "dmg_n": 0})
    for r in results:
        m = meta.get(r["file"]) if meta else None
        for rec in r["removed"] + r["survivors"]:
            name = (m[rec["team"]] if m else TEAM_NAME[rec["team"]]) or "?"
            per_team[name]["lives"] += 1
            per_team[name]["files"].add(r["file"])
            lives += 1
        for rec in r["removed"]:
            name = (m[rec["team"]] if m else TEAM_NAME[rec["team"]]) or "?"
            removals += 1
            by_class[rec["cls"]] += 1
            per_team[name]["removed"] += 1
            per_team[name][rec["cls"]] += 1
            lsf = rec.get("life_short_frac")
            if rec["cls"] != UNRESOLVED and lsf is not None:
                allr["n"] += 1
                allr["short"] += 1 if rec.get("ammo_short") else 0
                allr["exp"] += lsf
            if rec["cls"] == "DAMAGE_DEATH":
                ctrl["n"] += 1
                ctrl["short"] += 1 if rec.get("ammo_short") else 0
                if lsf is not None:
                    ctrl["exp"] += lsf
                per_team[name]["dmg_n"] += 1
                per_team[name]["dmg_short"] += 1 if rec.get("ammo_short") else 0
            if rec["cls"] in SELFKILL_CLASSES + ("CRASH_AMMO_RICH",):
                trt["n"] += 1
                trt["short"] += 1 if rec.get("ammo_short") else 0
                if lsf is not None:
                    trt["exp"] += lsf
        survivors += len(r["survivors"])
    return {"files": len(results), "turret_lives": lives, "removals": removals,
            "survivors": survivors, "by_class": dict(by_class),
            "ctrl_damage_deaths": ctrl, "crash_pool": trt, "all_ended": allr,
            "per_team": {k: {**v, "files": len(v["files"])} for k, v in per_team.items()}}


# --------------------------------------------------------------------------
# self-test: forced-answer cells on SYNTHETIC replays, driven through census()
# --------------------------------------------------------------------------
def _synth_mod():
    import replay_throws as rt
    return rt


def _u_place_turret(rt, eid, team, p, kind, hp=25):
    field = {"gunner": 21, "sentinel": 22, "builder_bot": 10, "launcher": 24}[kind]
    ent = (rt._vf(1, eid) + rt._vf(2, team) + rt._ld(3, rt._pos(p))
           + rt._vf(4, hp) + rt._vf(5, hp) + rt._ld(field, b""))
    return rt._ld(1, rt._ld(1, ent))


def _u_players(rt, ti_a, ammo_a, ti_b, ammo_b):
    a = rt._vf(1, ti_a) + rt._vf(7, ammo_a)
    b = rt._vf(1, ti_b) + rt._vf(7, ammo_b)
    return rt._ld(6, rt._ld(1, rt._ld(1, a) + rt._ld(2, b)))


def _u_attack(rt, aid, p):
    return rt._ld(13, rt._vf(1, aid) + rt._ld(2, rt._pos(p)))


def _u_hp_neg(rt, eid, delta):
    # proto3 int32 negatives are encoded as 10-byte two's-complement varints.
    return rt._ld(5, rt._vf(1, eid) + rt._vf(2, (1 << 64) + delta))


def selftest(out=sys.stdout) -> int:
    rt = _synth_mod()
    W = H = 12
    CORES = {0: (1, 1), 1: (10, 10)}
    cells: list[tuple[str, bool, str]] = []

    def cell(name, cond, detail=""):
        cells.append((name, bool(cond), detail))

    with tempfile.TemporaryDirectory(prefix="turret_selfkill_") as td:
        td = Path(td)
        tmp = td / "_s.replay26"

        def run(script, nrounds=12):
            tmp.write_bytes(rt.synth(W, H, CORES, script, nrounds))
            return census(tmp, keep_detail=True)

        GUN, BOT_FRIEND, BOT_ENEMY = 11, 12, 13
        GPOS = (5, 5)

        # ---- CELL PAIR 1: ammo short vs ammo rich, everything else identical.
        base = {
            0: [_u_place_turret(rt, GUN, 1, GPOS, "gunner"),
                _u_players(rt, 100, 0, 100, 0)],
            **{r: [_u_players(rt, 100, 0, 100, 0)] for r in range(1, 12)},
        }
        short = dict(base)
        short[5] = [_u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_short = run(short)
        rec = r_short["removed"][0]
        cell("ammo 2 < gunner cost 4, no hp event, no friendly builder -> SELFKILL_AMMO_CONSISTENT",
             rec["cls"] == "SELFKILL_AMMO_CONSISTENT", f'{rec["cls"]} ammo={rec["ammo_end"]}')

        rich = dict(base)
        rich[5] = [_u_players(rt, 100, 0, 100, 40), rt.u_remove(GUN)]
        r_rich = run(rich)
        rec_rich = r_rich["removed"][0]
        cell("SAME fixture with ammo 40 >= cost -> CRASH_AMMO_RICH (the ammo axis moves the verdict)",
             rec_rich["cls"] == "CRASH_AMMO_RICH", f'{rec_rich["cls"]} ammo={rec_rich["ammo_end"]}')

        # ---- CELL PAIR 2: sentinel cost is 10, not 4.
        sent = {
            0: [_u_place_turret(rt, GUN, 1, GPOS, "sentinel", hp=40),
                _u_players(rt, 100, 0, 100, 0)],
            **{r: [_u_players(rt, 100, 0, 100, 6)] for r in range(1, 12)},
        }
        sent[5] = [_u_players(rt, 100, 0, 100, 6), rt.u_remove(GUN)]
        r_sent = run(sent)
        cell("ammo 6 is SHORT for a sentinel (cost 10) -> SELFKILL_AMMO_CONSISTENT",
             r_sent["removed"][0]["cls"] == "SELFKILL_AMMO_CONSISTENT",
             r_sent["removed"][0]["cls"])
        gun6 = dict(base)
        gun6[5] = [_u_players(rt, 100, 0, 100, 6), rt.u_remove(GUN)]
        r_gun6 = run(gun6)
        cell("the SAME ammo 6 is RICH for a gunner (cost 4) -> CRASH_AMMO_RICH "
             "(per-kind cost is real, not a constant)",
             r_gun6["removed"][0]["cls"] == "CRASH_AMMO_RICH", r_gun6["removed"][0]["cls"])

        # ---- CELL PAIR 3: friendly adjacency flips it to TEARDOWN.
        tear = dict(short)
        tear[0] = short[0] + [_u_place_turret(rt, BOT_FRIEND, 1, (5, 4), "builder_bot")]
        r_tear = run(tear)
        cell("a FRIENDLY builder orthogonally adjacent at the removal round -> TEARDOWN_CONSISTENT",
             r_tear["removed"][0]["cls"] == "TEARDOWN_CONSISTENT", r_tear["removed"][0]["cls"])
        enemy = dict(short)
        enemy[0] = short[0] + [_u_place_turret(rt, BOT_ENEMY, 0, (5, 4), "builder_bot")]
        r_enemy = run(enemy)
        cell("an ENEMY builder on that same tile does NOT excuse it (team check works) "
             "-> still SELFKILL_AMMO_CONSISTENT",
             r_enemy["removed"][0]["cls"] == "SELFKILL_AMMO_CONSISTENT",
             r_enemy["removed"][0]["cls"])
        diag = dict(short)
        diag[0] = short[0] + [_u_place_turret(rt, BOT_FRIEND, 1, (4, 4), "builder_bot")]
        r_diag = run(diag)
        cell("a friendly builder DIAGONALLY adjacent cannot destroy() -> not TEARDOWN",
             r_diag["removed"][0]["cls"] == "SELFKILL_AMMO_CONSISTENT",
             r_diag["removed"][0]["cls"])
        moved = dict(short)
        moved[0] = short[0] + [_u_place_turret(rt, BOT_FRIEND, 1, (5, 2), "builder_bot")]
        moved[5] = [rt.u_move(BOT_FRIEND, (5, 4)), _u_players(rt, 100, 0, 100, 2),
                    rt.u_remove(GUN)]
        r_moved = run(moved)
        cell("adjacency counts a builder that MOVED next to it that round -> TEARDOWN_CONSISTENT",
             r_moved["removed"][0]["cls"] == "TEARDOWN_CONSISTENT", r_moved["removed"][0]["cls"])

        # ---- CELL PAIR 4: damage vs heal split (crash_census cannot do this).
        dmg = dict(short)
        dmg[4] = [_u_players(rt, 100, 0, 100, 2), _u_hp_neg(rt, GUN, -7)]
        r_dmg = run(dmg)
        cell("a NEGATIVE hp delta -> DAMAGE_DEATH, never a self-kill",
             r_dmg["removed"][0]["cls"] == "DAMAGE_DEATH", r_dmg["removed"][0]["cls"])
        heal = dict(short)
        heal[4] = [_u_players(rt, 100, 0, 100, 2), rt.u_hp(GUN, 4)]
        r_heal = run(heal)
        cell("a POSITIVE hp delta (a heal) is NOT damage -> HEALED_ONLY, not DAMAGE_DEATH",
             r_heal["removed"][0]["cls"] == "HEALED_ONLY", r_heal["removed"][0]["cls"])

        # ---- CELL PAIR 3b: the BATTERY-EXHAUSTION fingerprint, driven both ways.
        # `u_fire` is the fireTurret update; a turret that completed a shot that
        # round did NOT raise inside finish_firing_turret.
        def u_fire(frm, to):
            return rt._ld(12, rt._ld(1, rt._pos(frm)) + rt._ld(2, rt._pos(to)))

        SIB = 21
        batt = dict(short)
        batt[0] = short[0] + [_u_place_turret(rt, SIB, 1, (8, 8), "gunner")]
        batt[5] = [u_fire((8, 8), (2, 2)), _u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_batt = run(batt)
        got = [x for x in r_batt["removed"] if x["id"] == GUN][0]
        cell("a SIBLING turret completed a shot that round and the dying one did NOT "
             "-> SELFKILL_BATTERY_EXHAUSTED",
             got["cls"] == "SELFKILL_BATTERY_EXHAUSTED", got["cls"])
        selffire = dict(batt)
        selffire[5] = [u_fire((8, 8), (2, 2)), u_fire(GPOS, (2, 2)),
                       _u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_sf = run(selffire)
        got_sf = [x for x in r_sf["removed"] if x["id"] == GUN][0]
        cell("the SAME round with the dying turret's OWN shot completing -> NOT battery "
             "exhaustion (its fire() did not raise)",
             got_sf["cls"] == "SELFKILL_AMMO_CONSISTENT", got_sf["cls"])
        noshot = dict(batt)
        noshot[5] = [_u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_ns = run(noshot)
        got_ns = [x for x in r_ns["removed"] if x["id"] == GUN][0]
        cell("no shot completed by ANYONE that round -> falls back to "
             "SELFKILL_AMMO_CONSISTENT (the pool was not being drained)",
             got_ns["cls"] == "SELFKILL_AMMO_CONSISTENT", got_ns["cls"])

        # ---- CELL PAIR 4b: the NULL-EXPECTATION column must track the team's
        # actual ammo history, not be a constant. Same death, same class, two
        # different lifetime histories -> two different expectations.
        poor = {0: [_u_place_turret(rt, GUN, 1, GPOS, "gunner"),
                    _u_players(rt, 100, 0, 100, 0)],
                **{r: [_u_players(rt, 100, 0, 100, 0)] for r in range(1, 12)}}
        poor[5] = [_u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_poor = run(poor)
        cell("a team ammo-starved its whole life -> life_short_frac == 1.00 "
             "(the death round is UNSURPRISING)",
             abs(r_poor["removed"][0]["life_short_frac"] - 1.0) < 1e-9,
             str(r_poor["removed"][0]["life_short_frac"]))
        rich_hist = {0: [_u_place_turret(rt, GUN, 1, GPOS, "gunner"),
                         _u_players(rt, 100, 0, 100, 80)],
                     **{r: [_u_players(rt, 100, 0, 100, 80)] for r in range(1, 12)}}
        rich_hist[5] = [_u_players(rt, 100, 0, 100, 2), rt.u_remove(GUN)]
        r_rh = run(rich_hist)
        got = r_rh["removed"][0]["life_short_frac"]
        cell("the SAME death with an ammo-RICH history -> life_short_frac == 1/6 "
             "(so obs/exp can exceed 1 and the column is not constant)",
             abs(got - 1.0 / 6.0) < 1e-9, str(got))

        # ---- CELL 5: the error path renders DIFFERENTLY from a clean negative.
        noplayers = {0: [_u_place_turret(rt, GUN, 1, GPOS, "gunner")], 5: [rt.u_remove(GUN)]}
        r_np = run(noplayers)
        cell("a file with NO updatePlayers ammo for that round -> UNRESOLVED, "
             "NOT any clean class (error path must not read as a result)",
             r_np["removed"][0]["cls"] == UNRESOLVED, r_np["removed"][0]["cls"])

        # ---- CELL 6: survivors are exposure, not events.
        surv = dict(base)
        r_surv = run(surv)
        cell("a turret alive at the end is counted as EXPOSURE and produces no event",
             len(r_surv["removed"]) == 0 and len(r_surv["survivors"]) == 1,
             f'removed={len(r_surv["removed"])} surv={len(r_surv["survivors"])}')

        # ---- CELL 7: launchers use no ammo and must not enter the population.
        lau = {0: [rt.u_place(1000 + 4, 1, (7, 7), "launcher"), _u_players(rt, 1, 0, 1, 0)],
               5: [_u_players(rt, 1, 0, 1, 0), rt.u_remove(1004)]}
        r_lau = run(lau)
        cell("a LAUNCHER (0 ammo per action) never enters the turret population",
             len(r_lau["removed"]) == 0 and len(r_lau["survivors"]) == 0,
             f'removed={len(r_lau["removed"])}')

        # ---- CELL 8: builderAttack on its tile is recorded (attribution axis).
        atk = dict(short)
        atk[0] = short[0] + [_u_place_turret(rt, BOT_ENEMY, 0, (5, 4), "builder_bot")]
        atk[3] = [_u_players(rt, 100, 0, 100, 2), _u_attack(rt, BOT_ENEMY, GPOS)]
        r_atk = run(atk)
        rec_atk = r_atk["removed"][0]
        cell("a builderAttack targeting the turret's tile is attributed to the ATTACKER's team",
             rec_atk["attacked_by"].get(0, 0) == 1 and rec_atk["attacked_by"].get(1, 0) == 0,
             str(dict(rec_atk["attacked_by"])))
        cell("...and a fixture with NO attack records zero (the column is not constant)",
             r_short["removed"][0]["attacked_by"].get(0, 0) == 0,
             str(dict(r_short["removed"][0]["attacked_by"])))

    npass = sum(1 for _n, c, _d in cells if c)
    out.write("\n  TURRET SELF-KILL CENSUS -- forced-answer cells "
              "(synthetic replays, driven through census() from raw bytes)\n\n")
    for name, ok, detail in cells:
        out.write(f"  [{'PASS' if ok else 'FAIL'}] {name}\n")
        if not ok:
            out.write(f"          got: {detail}\n")
    out.write(f"\n  {npass}/{len(cells)} cells pass\n")
    return 0 if npass == len(cells) else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def collect_paths(args: list[str]) -> list[Path]:
    paths: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.replay26")))
        elif any(ch in a for ch in "*?[]"):
            import glob as _glob
            paths.extend(sorted(Path(x) for x in _glob.glob(a)))
        else:
            paths.append(p)
    return paths


def detail_report(path: Path, eid: int, out=sys.stdout) -> int:
    r = census(path, keep_detail=True)
    for rec in r["removed"] + r["survivors"]:
        if rec["id"] != eid:
            continue
        team = rec["team"]
        out.write(f"file {r['file']}  rounds={r['rounds']}\n")
        out.write(f"entity {eid}: kind={rec['kind']} team={TEAM_NAME[team]} pos={rec['pos']} "
                  f"born=r{rec['born']} died=r{rec.get('died', '-')}\n")
        out.write(f"  class={rec.get('cls', 'ALIVE_AT_END')}\n")
        out.write(f"  updateHp events: negative={rec['hp_neg']} positive={rec['hp_pos']}\n")
        out.write(f"  builderAttack on its tile, by team: {dict(rec['attacked_by'])}\n")
        out.write(f"  turret fire landing on its tile, by team: {dict(rec['fired_at_by'])}\n")
        out.write(f"  shots it fired: {rec['shots']}\n")
        out.write(f"  shots its TEAM completed in the removal round: "
                  f"{rec.get('team_shots_at_death')}; did IT fire that round: "
                  f"{rec.get('self_fired_at_death')}\n")
        out.write(f"  friendly builder orthogonally adjacent in removal round: "
                  f"{rec.get('adj_friendly_builder')}\n")
        if "died" in rec:
            d = rec["died"]
            lo, hi = max(0, d - 8), min(len(r["ammo"][team]), d + 3)
            out.write(f"  team {TEAM_NAME[team]} ammo (end of round) r{lo}..r{hi - 1}: "
                      + ", ".join(f"r{i}={r['ammo'][team][i]}" for i in range(lo, hi)) + "\n")
            out.write(f"  shot cost for {rec['kind']} = {SHOT_COST[rec['kind']]}; "
                      f"ammo at death = {rec.get('ammo_end')}\n")
        if rec["detail"]:
            out.write(f"  event log: {rec['detail']}\n")
        return 0
    out.write(f"entity {eid} is not a gunner/sentinel in {path.name}\n")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\nUSAGE\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("replays", nargs="*", help=".replay26 file(s), a directory, or a glob")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--detail", nargs=2, metavar=("FILE", "ENTITY_ID"))
    ap.add_argument("--meta", default=None, help="corpus/meta_join.tsv for team names")
    ap.add_argument("--by-opponent", action="store_true")
    ap.add_argument("--min-lives", type=int, default=100,
                    help="per-team rows need this many turret lives to be printed")
    ap.add_argument("--limit", type=int, default=None, help="first N files only")
    ap.add_argument("--sample", type=int, default=None)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--json", default=None, help="write the aggregate to this path")
    ap.add_argument("--events-tsv", default=None,
                    help="write one row per ended turret life to this path")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.detail:
        return detail_report(Path(args.detail[0]), int(args.detail[1]))
    if not args.replays:
        ap.error("give replays, or --selftest, or --detail FILE ID")

    paths = collect_paths(args.replays)
    if args.sample is not None and args.sample < len(paths):
        paths = random.Random(args.seed).sample(paths, args.sample)
    if args.limit:
        paths = paths[:args.limit]
    if not paths:
        print("no .replay26 files matched", file=sys.stderr)
        return 1

    meta = load_meta(Path(args.meta)) if args.meta else None

    results, errors = [], []
    ev_fh = None
    if args.events_tsv:
        ev_fh = open(args.events_tsv, "w")
        ev_fh.write("file\tid\tteam\tteamname\tkind\tborn\tdied\tcls\tammo_end\tammo_prev"
                    "\tcost\thp_neg\thp_pos\tshots\tadj_friendly\tatk_own\tatk_enemy"
                    "\tlife_rounds\tlife_short_frac\tteam_shots_R\tself_fired_R\n")
    for i, p in enumerate(paths):
        try:
            r = census(p)
        except Exception as exc:                                    # noqa: BLE001
            errors.append((p.name, f"{type(exc).__name__}: {exc}"))
            continue
        if ev_fh:
            m = meta.get(r["file"]) if meta else None
            for rec in r["removed"]:
                nm = (m[rec["team"]] if m else TEAM_NAME[rec["team"]]) or "?"
                ev_fh.write("\t".join(str(x) for x in [
                    r["file"], rec["id"], TEAM_NAME[rec["team"]], nm, rec["kind"],
                    rec["born"], rec["died"], rec["cls"], rec.get("ammo_end"),
                    rec.get("ammo_prev"), rec.get("cost"), rec["hp_neg"], rec["hp_pos"],
                    rec["shots"], int(bool(rec.get("adj_friendly_builder"))),
                    rec["attacked_by"].get(rec["team"], 0),
                    rec["attacked_by"].get(1 - rec["team"], 0),
                    rec.get("life_rounds"), rec.get("life_short_frac"),
                    rec.get("team_shots_at_death"),
                    int(bool(rec.get("self_fired_at_death")))]) + "\n")
        # drop the heavy per-entity detail before keeping the file around
        r["removed"] = [{k: v for k, v in rec.items() if k != "detail"} for rec in r["removed"]]
        r["survivors"] = [{"team": s["team"], "kind": s["kind"]} for s in r["survivors"]]
        r["ammo"] = None
        results.append(r)
        if (i + 1) % 2000 == 0:
            print(f"  ...{i + 1}/{len(paths)}", file=sys.stderr, flush=True)
    if ev_fh:
        ev_fh.close()

    agg = aggregate(results, meta)
    agg["errors"] = len(errors)
    agg["files_requested"] = len(paths)

    print("\n=== TURRET SELF-KILL CENSUS ===")
    print(f"files parsed: {agg['files']} of {len(paths)} requested "
          f"({agg['errors']} parse errors -- NOT counted as 'no self-kills')")
    print(f"gunner/sentinel LIVES (exposure): {agg['turret_lives']}  "
          f"(ended {agg['removals']}, alive at end {agg['survivors']})")
    print("\nclass breakdown of ENDED lives:")
    tot = agg["removals"] or 1
    for c in CLASSES + (UNRESOLVED,):
        n = agg["by_class"].get(c, 0)
        print(f"  {c:26s} {n:8d}  {100.0 * n / tot:6.2f}%")
    ctrl, trt, allr = agg["ctrl_damage_deaths"], agg["crash_pool"], agg["all_ended"]
    print("\n⭐ BASE-RATE CONTROL -- share of deaths where the team's ammo was BELOW")
    print("   that turret's shot cost at end of the death round, against the")
    print("   EXPECTED share under 'the death round says nothing about ammo'")
    print("   (= mean share of each turret's OWN LIFETIME spent below that cost):")
    print(f"   {'pool':42s} {'observed':>16s} {'expected':>10s} {'obs/exp':>9s}")
    for label, d in (("no-hp, no-adjacency (crash pool)", trt),
                     ("DAMAGE_DEATH (demonstrably NOT a crash)", ctrl),
                     ("all ended turret lives", allr)):
        if not d["n"]:
            print(f"   {label:42s} {'NO EVENTS':>16s}")
            continue
        obs = d["short"] / d["n"]
        exp = d["exp"] / d["n"]
        ratio = (obs / exp) if exp else float("nan")
        print(f"   {label:42s} {d['short']:6d}/{d['n']:<6d}={100 * obs:5.2f}% "
              f"{100 * exp:9.2f}% {ratio:9.2f}")
    if ctrl["n"] and trt["n"] and ctrl["short"]:
        lift = (trt["short"] / trt["n"]) / (ctrl["short"] / ctrl["n"])
        print(f"   LIFT (crash pool / damage-death control): {lift:.2f}x")
    print("   ⚠ obs/exp near 1.00 means the ammo axis does NOT discriminate;")
    print("     BELOW 1.00 means undamaged turret removals happen when the team is")
    print("     ammo-RICH, i.e. the opposite of the fire-at-zero-ammo mechanism.")

    if args.by_opponent:
        print("\nper-team (teams with >= "
              f"{args.min_lives} turret lives), sorted by selfkill share of lives:")
        rows = [(k, v) for k, v in agg["per_team"].items() if v["lives"] >= args.min_lives]
        def _sk(v):
            return v["SELFKILL_BATTERY_EXHAUSTED"] + v["SELFKILL_AMMO_CONSISTENT"]
        rows.sort(key=lambda kv: -_sk(kv[1]) / max(1, kv[1]["lives"]))
        hdr = (f"  {'team':26s}{'files':>7s}{'lives':>8s}{'ended':>7s}{'batt':>6s}"
               f"{'ammoOK':>7s}{'selfkill/1k':>12s}{'crashrich':>10s}{'teardown':>9s}{'dmg':>8s}{'unres':>7s}")
        print(hdr)
        for k, v in rows[:60]:
            sk = _sk(v)
            print(f"  {k[:25]:26s}{v['files']:>7d}{v['lives']:>8d}{v['removed']:>7d}"
                  f"{v['SELFKILL_BATTERY_EXHAUSTED']:>6d}{v['SELFKILL_AMMO_CONSISTENT']:>7d}"
                  f"{1000.0 * sk / v['lives']:>12.2f}{v['CRASH_AMMO_RICH']:>10d}"
                  f"{v['TEARDOWN_CONSISTENT']:>9d}{v['DAMAGE_DEATH']:>8d}{v[UNRESOLVED]:>7d}")

    if errors:
        print(f"\n{len(errors)} parse error(s):", file=sys.stderr)
        for n, m in errors[:10]:
            print(f"  {n}: {m}", file=sys.stderr)
    if args.json:
        Path(args.json).write_text(json.dumps(agg, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
