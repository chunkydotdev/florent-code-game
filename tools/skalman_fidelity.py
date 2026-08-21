#!/usr/bin/env python3
"""SKALMAN phase-1 REPLICATION-FIDELITY instrument.

Reads the seven mechanism signatures of the league's rank-1 bot ("Bean counters")
off a set of replays, for ONE SUBJECT SIDE, and prints them next to the measured
Bean-counters target and our own old baseline.

⛔ WHAT THIS TOOL IS FOR, AND WHAT IT IS NOT.  Phase-1 SKALMAN verdicts are NOT
game share.  They are: *does our candidate's replay signature match the numbers
we measured on Bean counters?*  This tool emits those numbers and nothing else.
It does not decide whether a bot is good; a fidelity row at target says the
mechanism is running, not that it pays.  (`PROGRAMME.md`: `R1000_IS_DEFEAT`
survives the line change — the cage/belt/nest are means, core destruction is the
end.)

PROVENANCE OF EVERY TARGET IN THE TABLE
=======================================
  M1 belt connectivity   docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md
                         §3.3 seeded-fragment-1 (v68 81.4% = 445/547 over 90
                         games; v47 82.7% = 6,722/8,133 over 1,235) — ours 58.8%
                         is the study's §1 "last comparable cut" and carries NO n.
  M2 cage                STUDY §3.4 (v47 55.5% ring share / 22.3% full seal /
                         median first ring build r35; v68 39.6% / 22.2%, n=90)
                         and §6.2 (us v168-v177: 75.4% / 12.0% / r12, n=1,115).
  M3 drip clock          PLAYBOOK-beancounters-PART-v68 §2.2 (67 calls p90 102,
                         first convert median r27.5 p10 11, peak balance 26 p90
                         34, 97.3% = 8,054/8,278 lattice) and PLAYBOOK §6 COPY 7.
  M4 nest siting         STUDY §3.5 (sentinel d² to ENEMY core: v47 23.9% ≤13 /
                         48.1% band 14-32; v68 53.3% / 32.1%).
  M5 four roles          PART-v68 §3.3 (exactly four builders in 104/112 games,
                         fourth at r3, p10=p90=3) and PLAYBOOK §6 COPY 8.
  M6 ore denial          PART-v68 §1 (v68: 37.9% = 784/2,068 barriers on ore;
                         92.5% = 185/200 enemy harvester kills covered within 30
                         rounds, median latency 1; us: 0 of 1,381, n=150 games).
  M7 home-ring clearance STUDY §3.6 seeded-fragment-2 (v47 79.7% ± 2.2 over
                         1,131 games / 5,803 turrets; v68 76.6% ± 11.1 over 61
                         games / 117 turrets; us v168-v177 42.8% ± 3.3, n=961).

⚠ THE TARGET COLUMN IS ERA-SPECIFIC AND THE TWO ERAS DISAGREE.  v47 and v68 are
different bots on M2 (55.5% vs 39.6% ring share) and OPPOSITE on M4 (48.1% band
vs 53.3% point-blank).  `--era v68` (default) / `--era v47` picks which column is
printed.  Copying the wrong era is a real risk the playbook flags explicitly
(PLAYBOOK §6 COPY 5: "do not copy the point-blank plant without the clearance
verb").

DECODER REUSE — NOTHING HAND-ROLLED
===================================
Wire primitives (`fields`, `read_pos`, `parse_entity`, `packed_varints`,
`scalars`) come from `tools/replay_census.py` per `tools/replay_schema.md`, the
same way the s53 probes do.  **M1 is not re-implemented at all**: it calls
`replay_census.Replay.chains` unbound, on a shim carrying this scan's own final
entity set — so the directed-connectivity number is produced by *literally the
study's instrument*, and `--selftest` cross-checks the shim against a full
`Replay(...)` parse on 5 replays to prove the reuse is faithful.

SIDE ATTRIBUTION IS THE FAILURE MODE
====================================
Every replay has two teams and every metric here is asymmetric.  A wrong-side
read produces a clean, confident number on the wrong bot.  The subject side must
come from `corpus/meta_join.tsv` (`--team-id`/`--team-name` + `--versions`), from
a manifest column, or be stated with `--side`.  `--selftest` includes a
DELIBERATE WRONG-SIDE READ and requires it to FAIL, so the attribution guard is
driven, not merely present.

USAGE
=====
    .venv/bin/python tools/skalman_fidelity.py \
        --manifest scratchpad/s53_beanwatch68_v68files.tsv --label "BC v68"
    .venv/bin/python tools/skalman_fidelity.py \
        --team-name "OpenSverige" --versions 175,176,177 --label "us v175-177"
    .venv/bin/python tools/skalman_fidelity.py --dir path/to/replays --side 0
    ... --json out.json          machine-readable, every number with its denominator
    ... --selftest               both-ways drive on two known populations

INTERVALS
=========
Shares that are per-game are reported as a games-as-units mean with a 95%
half-width inflated by sqrt(DEFF); `--deff` defaults to **1.833**, the measured
unrated-pool design effect (CLAUDE.md, s40) — these archived pools are
unrated-dominated.  Pooled (event-level) ratios are printed as the headline where
the study quotes them that way, with the game-level interval beside them and
BOTH denominators named.  A pooled ratio has no DEFF applied and says so.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from replay_census import (  # noqa: E402
    Entity, Replay, fields, packed_varints, parse_entity, read_pos, scalars,
    WIRE_LEN,
)

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
ENV_WALL = 1
ENV_ORE = 2
TURRETS = ("gunner", "sentinel")
DEFAULT_REPLAY_ROOT = ROOT / "replay_archive"
META_JOIN = ROOT / "corpus" / "meta_join.tsv"

# --- the 4/10 ammunition lattice ---------------------------------------------
# gunner 4 ammo/shot, sentinel 10 (CLAUDE.md).  A drip implementation converts
# exactly the cost of the shots it is about to take, so its convert amounts are
# nonneg integer combinations of 4 and 10.  Representable: 0, 4, 8, and every
# even number >= 10.  NOT representable: every odd number, 2, and 6 — those three
# classes are what make this a test rather than an "is it even" tautology.
_LATTICE = {0}
for _a in range(0, 400):
    for _b in range(0, 160):
        _v = 4 * _a + 10 * _b
        if _v <= 1500:
            _LATTICE.add(_v)


def in_lattice(amount: int) -> bool:
    if amount < 0:
        return False
    if amount <= 1500:
        return amount in _LATTICE
    return amount % 2 == 0          # every even >= 10 is representable


# --- geometry -----------------------------------------------------------------

def footprint(pos):
    x, y = pos
    return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


def ring_of(fp, w, h):
    """The orthogonal neighbours of a 2x2 core footprint, in bounds.

    Same shape as `scratchpad/s53_bean_seal.py` / `_ourseal.py`, which produced
    the study's §3.4 and §6.2 rows.  Walls are filtered by the caller (the study
    counts only NON-WALL ring tiles as 'open'), reproduced exactly: our-side
    aggregation of `s53_bean_ourseal.jsonl` under this definition returns 12.0%
    full seal / 75.4% ring share / median first ring build r12 — the three
    numbers §6.2 prints.
    """
    out = set()
    for (x, y) in fp:
        for dx, dy in CARD:
            t = (x + dx, y + dy)
            if t not in fp and 0 <= t[0] < w and 0 <= t[1] < h:
                out.add(t)
    return out


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def dsq_to_set(p, tiles):
    return min(dsq(p, t) for t in tiles)


# --- the scan -----------------------------------------------------------------

class _ChainShim:
    """Carries exactly what `Replay.chains` reads, so the study's own code runs.

    `Replay.chains` touches self.entities, self.core_footprint(team) and
    self.ship_from and nothing else.  Calling it unbound on this shim reuses the
    instrument rather than re-deriving directed connectivity — and `--selftest`
    drives the equivalence against a real `Replay(...)` on 5 replays, because a
    shim that has drifted from the class it imitates is a silent wrong number.
    """

    def __init__(self, entities, cores, ship_from):
        self.entities = entities
        self._cores = cores
        self.ship_from = ship_from

    def core_footprint(self, team):
        out = set()
        for c in self._cores:
            if c["team"] == team:
                out |= footprint(c["pos"])
        return out


def _roles(subj_bots):
    """The four PLAYBOOK COPY 8 role recognisers, verbatim from its own table.

        HOME KEEPER     forward-action share 0.000
        CAGE WALKER     places most ring barriers; high batk
        ORE DENIER      highest melee count; EVERY barrier on ore
        SIEGE ENGINEER  batk 0; the sentinel build is its signature

    Returns which roles are present and whether four DISTINCT bots fill them —
    the checkable form of "four fixed jobs".  A bot is only eligible for a role
    if it did enough to have a signature at all (>= 5 actions), otherwise a bot
    that idled all game trivially satisfies "forward share 0.000" and "batk 0"
    and every game would score four roles.
    """
    active = [b for b in subj_bots if b["actions"] >= 5]
    out = {"home_keeper": None, "cage_walker": None,
           "ore_denier": None, "siege_engineer": None}
    for b in active:
        if b["fwd_actions"] == 0 and out["home_keeper"] is None:
            out["home_keeper"] = b["id"]
    ring = [b for b in active if b["ring_barriers"] > 0]
    if ring:
        out["cage_walker"] = max(ring, key=lambda b: b["ring_barriers"])["id"]
    ore = [b for b in active
           if b["ore_barriers"] > 0 and b["ore_barriers"] == b["barriers"]]
    if ore:
        out["ore_denier"] = max(ore, key=lambda b: b["batk"])["id"]
    siege = [b for b in active if b["sentinel_builds"] > 0 and b["batk"] == 0]
    if siege:
        out["siege_engineer"] = siege[0]["id"]
    filled = [v for v in out.values() if v is not None]
    out["n_roles"] = len(filled)
    out["four_distinct"] = len(filled) == 4 and len(set(filled)) == 4
    return out


def scan_replay(path: Path, side: int, deny_window: int = 3) -> dict:
    """One pass over a replay; every per-game contribution for the SUBJECT side.

    `side` is the subject's team index (0 = A, 1 = B).  Every metric below is
    computed FOR that side, except M7 which is computed AGAINST it (the subject
    is the defender clearing turrets planted in its own half).
    """
    data = path.read_bytes()
    map_buf = None
    turns = []
    winner = None
    wincond = ""
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = val
        elif num == 3 and wire == WIRE_LEN:
            turns.append(val)
        elif num == 4 and wire == 0:
            winner = val
        elif num == 6 and wire == WIRE_LEN:
            wincond = val.decode("utf-8", "replace")
    if map_buf is None:
        raise ValueError(f"{path}: no battlecode.Map (field 1) — not a replay?")

    w = h = 0
    tiles = []
    cores = []
    for num, wire, val in fields(map_buf):
        if num == 1:
            w = val
        elif num == 2:
            h = val
        elif num == 3:
            row = []
            for rn, rw, rv in fields(val):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(val):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        raise ValueError(f"{path}: {len(cores)} cores, expected 2")

    def env(p):
        x, y = p
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return ENV_WALL

    enemy = 1 - side
    cfoot = {c["team"]: footprint(c["pos"]) for c in cores}
    # ⛔ TWO ORIGINS, AND THEY DISAGREE BY UP TO ~19pp ON THE BAND SHARE.
    # PLAYBOOK §6 COPY 5 specifies the nest band as "d^2 14-32 from the enemy
    # core FOOTPRINT"; the measured table it cites (STUDY §3.5) was computed by
    # `tools/corpus/replay_events.py:92,114`, which uses `corepos[team]` — the
    # core's NW-CORNER ANCHOR, not the footprint.  On BC v47's 2,979 sentinels
    # the footprint origin reads 66.9% in-band / 33.1% point-blank and the anchor
    # origin reads 48.1% / 23.9% — the study's exact numbers.  Both are emitted:
    # the footprint reading is the one the SPEC asks for and the one the engine's
    # reach actually obeys, the anchor reading is STUDY-COMPAT.  Publishing one
    # under the other's target would be a 19pp error that looks like a finding.
    canchor = {c["team"]: c["pos"] for c in cores}
    enemy_ring_all = ring_of(cfoot[enemy], w, h)
    enemy_ring = {t for t in enemy_ring_all if env(t) != ENV_WALL}
    own_ring = {t for t in ring_of(cfoot[side], w, h) if env(t) != ENV_WALL}

    # live state
    entities: dict[int, Entity] = {}
    for c in cores:
        entities[c["id"]] = Entity(c["id"], c["team"], c["pos"], "core",
                                   500, 500, None, 0)
    occ: dict[tuple, tuple] = {}          # pos -> (team, kind, id) for BUILDINGS
    for c in cores:
        for p in footprint(c["pos"]):
            occ[p] = (c["team"], "core", c["id"])

    # collected series
    builds = []            # (rnd, team, kind, id, pos)
    deaths = []            # (rnd, team, kind, id, pos)
    build_at = {}          # (rnd, pos) -> (team, kind, id)
    converts = {0: [], 1: []}
    peak_ammo = {0: 0, 1: 0}
    ship_from = set()
    bots = {}              # builder id -> signature dict
    max_seal = 0
    first_ring_build = None
    barriers_total = 0
    barriers_on_ring = 0
    barriers_on_ore = 0

    def bot(bid, team):
        b = bots.get(bid)
        if b is None:
            b = bots[bid] = {"id": bid, "team": team, "born": None,
                             "builds": 0, "fwd_actions": 0, "actions": 0,
                             "ring_barriers": 0, "batk": 0, "batk_harvester": 0,
                             "bheal": 0, "sentinel_builds": 0, "gunner_builds": 0,
                             "ore_barriers": 0, "barriers": 0}
        return b

    def forward(p):
        return dsq_to_set(p, cfoot[enemy]) < dsq_to_set(p, cfoot[side])

    # ⛔ builderBuild (update 16) is emitted BEFORE the placeEntity (update 1) it
    # causes — verified on the wire (round 1 of a v68 replay reads
    # [1,7,9,1,7,9,2,8,9,7,16,1,9,6]).  Resolving a build's KIND at the moment
    # the builderBuild arrives therefore finds nothing and silently attributes
    # ZERO ring barriers to every bot, which reads as "no bot owns the cage" —
    # a clean wrong zero.  Buffer per round, resolve at end of round.
    pending_builds = []
    for rnd, tbuf in enumerate(turns):
        pending_builds.clear()
        for _n, _w, ubuf_outer in fields(tbuf):
            for unum, _uw, ub in fields(ubuf_outer):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        old = entities.get(e.id)
                        if old is not None:
                            # rotation / re-emit: state update, NOT a build
                            # (replay_census docstring, s19 find)
                            old.pos = e.pos
                            if e.direction is not None:
                                old.direction = e.direction
                            continue
                        entities[e.id] = e
                        if e.kind == "builder_bot":
                            b = bot(e.id, e.team)
                            b["born"] = rnd
                            continue
                        occ[e.pos] = (e.team, e.kind, e.id)
                        builds.append((rnd, e.team, e.kind, e.id, e.pos))
                        build_at[(rnd, e.pos)] = (e.team, e.kind, e.id)
                        if e.team == side:
                            if e.pos in enemy_ring and first_ring_build is None:
                                first_ring_build = rnd
                            if e.kind == "barrier":
                                barriers_total += 1
                                if e.pos in enemy_ring:
                                    barriers_on_ring += 1
                                if env(e.pos) == ENV_ORE:
                                    barriers_on_ore += 1
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = entities.get(eid)
                    if e is not None and to is not None:
                        e.pos = to
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ub):
                        e = entities.pop(rv, None)
                        if e is None:
                            continue
                        if e.kind != "builder_bot":
                            if occ.get(e.pos, (None, None, None))[2] == rv:
                                occ.pop(e.pos, None)
                            deaths.append((rnd, e.team, e.kind, rv, e.pos))
                        else:
                            deaths.append((rnd, e.team, e.kind, rv, e.pos))
                elif unum == 4:                                  # distributeRes.
                    for _mn, _mw, mbuf in fields(ub):
                        for pn, _pw, pv in fields(mbuf):
                            if pn == 1:
                                ship_from.add(read_pos(pv))
                elif unum == 6:                                  # updatePlayers
                    for pn, _pw, pv in fields(ub):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                d = scalars(tv)
                                t = tn - 1
                                a = d.get(7, 0)
                                if a > peak_ammo[t]:
                                    peak_ammo[t] = a
                elif unum == 14:                                 # coreConvertAmmo
                    tm = amt = 0
                    for cn, _cw, cv in fields(ub):
                        if cn == 1:
                            tm = cv
                        elif cn == 2:
                            amt = cv
                    converts[tm].append((rnd, amt))
                elif unum in (13, 15, 16):        # builderAttack / Heal / Build
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if aid is None or tgt is None:
                        continue
                    e = entities.get(aid)
                    team = e.team if e is not None else bots.get(aid, {}).get("team")
                    if team is None:
                        continue
                    b = bot(aid, team)
                    b["actions"] += 1
                    if forward(tgt):
                        b["fwd_actions"] += 1
                    if unum == 13:
                        b["batk"] += 1
                        tgt_ent = occ.get(tgt)
                        if tgt_ent and tgt_ent[1] == "harvester" and tgt_ent[0] != team:
                            b["batk_harvester"] += 1
                    elif unum == 15:
                        b["bheal"] += 1
                    else:
                        b["builds"] += 1
                        pending_builds.append((aid, tgt))
        for aid, tgt in pending_builds:                 # resolve KIND end-of-round
            made = build_at.get((rnd, tgt))
            if made is None:
                continue
            b = bots.get(aid)
            if b is None:
                continue
            kind = made[1]
            if kind == "sentinel":
                b["sentinel_builds"] += 1
            elif kind == "gunner":
                b["gunner_builds"] += 1
            elif kind == "barrier":
                b["barriers"] += 1
                if tgt in enemy_ring:
                    b["ring_barriers"] += 1
                if env(tgt) == ENV_ORE:
                    b["ore_barriers"] += 1
        held = sum(1 for t in enemy_ring if occ.get(t, (None,))[0] == side)
        if held > max_seal:
            max_seal = held

    # ---- M1 via the study's own instrument ---------------------------------
    shim = _ChainShim(entities, cores, ship_from)
    ch = Replay.chains(shim, side)

    # ---- M4 nest siting -----------------------------------------------------
    turret_builds = []
    for (rnd, team, kind, eid, pos) in builds:
        if team != side or kind not in TURRETS:
            continue
        de = dsq_to_set(pos, cfoot[enemy])
        do = dsq_to_set(pos, cfoot[side])
        dea = dsq(pos, canchor[enemy])
        doa = dsq(pos, canchor[side])
        turret_builds.append({"round": rnd, "kind": kind, "pos": list(pos),
                              "dsq_enemy": de, "dsq_own": do,
                              "dsq_enemy_anchor": dea, "dsq_own_anchor": doa,
                              "forward": de < do, "forward_anchor": dea < doa})

    # ---- M5 four roles ------------------------------------------------------
    subj_bots = [b for b in bots.values() if b["team"] == side and b["born"] is not None]
    subj_bots.sort(key=lambda b: (b["born"], b["id"]))
    spawn_rounds = [b["born"] for b in subj_bots]
    ring_by_bot = [b["ring_barriers"] for b in subj_bots]
    ring_total = sum(ring_by_bot)
    ring_top_share = (max(ring_by_bot) / ring_total) if ring_total else None

    # ---- M6 ore denial ------------------------------------------------------
    enemy_harv_deaths = [(rnd, pos) for (rnd, team, kind, _i, pos) in deaths
                         if kind == "harvester" and team == enemy]
    subj_barrier_at = {}
    for (rnd, team, kind, _i, pos) in builds:
        if team == side and kind == "barrier":
            subj_barrier_at.setdefault(pos, []).append(rnd)
    cov_w = cov_30 = 0
    latencies = []
    for (drnd, pos) in enemy_harv_deaths:
        later = [r for r in subj_barrier_at.get(pos, []) if r >= drnd]
        if later:
            lat = min(later) - drnd
            if lat <= deny_window:
                cov_w += 1
            if lat <= 30:
                cov_30 += 1
                latencies.append(lat)

    # ---- M7 home-ring clearance (subject = DEFENDER) ------------------------
    # Study §3.6 definition, verbatim: "forward turret = a gunner/sentinel built
    # closer to the defender's core than to its own; removal = a death of that
    # kind on that tile at a later round".  Implemented literally.  `by_id` is a
    # strictly tighter variant kept as a DIAGNOSTIC so the looseness of the
    # published definition is visible rather than assumed harmless.
    death_kind_pos = {}
    for (rnd, team, kind, eid, pos) in deaths:
        death_kind_pos.setdefault((kind, pos), []).append(rnd)
    death_ids = {eid for (_r, _t, _k, eid, _p) in deaths}
    fwd_against = 0
    fwd_removed = 0
    fwd_removed_by_id = 0
    fwd_against_anchor = 0
    fwd_removed_anchor = 0
    for (rnd, team, kind, eid, pos) in builds:
        if team != enemy or kind not in TURRETS:
            continue
        removed = any(r > rnd for r in death_kind_pos.get((kind, pos), ()))
        if dsq_to_set(pos, cfoot[side]) < dsq_to_set(pos, cfoot[enemy]):
            fwd_against += 1
            if removed:
                fwd_removed += 1
            if eid in death_ids:
                fwd_removed_by_id += 1
        if dsq(pos, canchor[side]) < dsq(pos, canchor[enemy]):
            fwd_against_anchor += 1
            if removed:
                fwd_removed_anchor += 1

    conv = converts[side]
    return {
        "file": path.name,
        "side": side,
        "rounds": len(turns),
        "winner": winner,
        "win_condition": wincond,
        "map": [w, h],
        # M1
        "harv_end_total": ch["total"],
        "harv_end_directed": ch["directed"],
        "harv_end_connected": ch["connected"],
        # M2
        "barriers_total": barriers_total,
        "barriers_on_enemy_ring": barriers_on_ring,
        "ring_open": len(enemy_ring),
        "max_seal": max_seal,
        "full_seal": bool(enemy_ring) and max_seal >= len(enemy_ring),
        "first_ring_build": first_ring_build,
        # M3
        "converts_n": len(conv),
        "converts_ti": sum(a for _r, a in conv),
        "converts_lattice": sum(1 for _r, a in conv if in_lattice(a)),
        "first_convert": conv[0][0] if conv else None,
        "peak_ammo": peak_ammo[side],
        "convert_amounts": [a for _r, a in conv],
        # M4
        "turret_builds": turret_builds,
        # M5
        "builders_spawned": len(subj_bots),
        "spawn_rounds": spawn_rounds,
        "ring_top_share": ring_top_share,
        "bot_signatures": [
            {"id": b["id"], "born": b["born"], "actions": b["actions"],
             "fwd_action_share": (b["fwd_actions"] / b["actions"]) if b["actions"] else None,
             "ring_barriers": b["ring_barriers"], "ore_barriers": b["ore_barriers"],
             "batk": b["batk"], "batk_harvester": b["batk_harvester"],
             "bheal": b["bheal"], "builds": b["builds"],
             "barriers": b["barriers"],
             "sentinel_builds": b["sentinel_builds"],
             "gunner_builds": b["gunner_builds"]}
            for b in subj_bots],
        "roles": _roles(subj_bots),
        # M6
        "barriers_on_ore": barriers_on_ore,
        "enemy_harv_deaths": len(enemy_harv_deaths),
        "ore_covered_w": cov_w,
        "ore_covered_30": cov_30,
        "ore_latencies": latencies,
        # M7
        "fwd_turrets_against": fwd_against,
        "fwd_turrets_removed": fwd_removed,
        "fwd_turrets_removed_by_id": fwd_removed_by_id,
        "fwd_turrets_against_anchor": fwd_against_anchor,
        "fwd_turrets_removed_anchor": fwd_removed_anchor,
    }


# --- aggregation --------------------------------------------------------------

def ci95(values, deff):
    """Games-as-units 95% half-width, inflated by sqrt(DEFF)."""
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None
    sd = statistics.pstdev(vals) if len(vals) < 3 else statistics.stdev(vals)
    return 1.96 * sd / math.sqrt(len(vals)) * math.sqrt(deff)


def _median(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def _pct(num, den):
    return 100.0 * num / den if den else None


def _pctile(vals, q):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return None
    i = min(len(vals) - 1, int(len(vals) * q))
    return vals[i]


# target column: (v68, v47, our_old_baseline).  None = the study prints no
# number for that era; "—" reaches the table as an empty cell, never as a 0.
TARGETS = {
    "M1 belt_connectivity_directed":      (81.4, 82.7, 58.8),
    "M1b belt_connectivity_undirected":   (None, None, None),
    "M2a cage_ring_share":                (39.6, 55.5, 75.4),
    "M2b full_seal_rate":                 (22.2, 22.3, 12.0),
    "M2c first_ring_build_median":        (52.0, 35.0, 12.0),
    "M2d ring_tiles_held_median":         (6.0, 5.0, 5.0),
    "M3a drip_lattice_share":             (97.3, None, None),
    # ⚠ v47 column left blank on purpose: STUDY §3.3 prints 56.2 calls / 530 Ti
    # as MEANS, and this row is a MEDIAN (the v68 target IS a median, PART-v68
    # §2.2).  Putting the mean in the target cell of a median row is exactly the
    # kind of silent unit mismatch this table exists to prevent; the means ride
    # in the note instead.
    "M3b converts_per_game_median":       (67.0, None, None),
    "M3c converted_ti_per_game_median":   (650.0, None, None),
    "M3d peak_ammo_median":               (26.0, None, None),
    "M3e first_convert_round_median":     (27.5, None, None),
    "M4a fwd_turret_band_share":          (None, None, None),
    "M4b fwd_turret_pointblank_share":    (None, None, None),
    "M4c sentinel_band_share":            (None, None, None),
    "M4d sentinel_pointblank_share":      (None, None, None),
    "M4e sentinel_band_share_anchor":     (32.1, 48.1, None),
    "M4f sentinel_pointblank_share_anchor": (53.3, 23.9, None),
    "M5a builders_per_game_median":       (4.0, 4.0, None),
    "M5b exactly_four_builders_share":    (92.9, None, None),
    "M5c fourth_spawn_round_median":      (3.0, None, None),
    # ⚠ The 1.000 is a v47 measurement (PLAYBOOK T2: "median v47 game, n=924
    # games with >=4 ring barriers", field 0.857).  COPY 8 reprints it as a
    # SKALMAN target beside v68 numbers, but v68 does NOT run a single-owner
    # ring: measured 0.80 here, and COPY 8's own id-tracked watch (A game 5)
    # shows bot #5 with 6 ring barriers and bot #13 with 3 — a top share of
    # 0.667.  The v68 column is therefore left blank rather than borrowed.
    "M5d ring_barrier_top_share_median":  (None, 1.0, None),
    "M5e role_home_keeper_share":         (None, None, None),
    "M5f role_cage_walker_share":         (None, None, None),
    "M5g role_ore_denier_share":          (None, None, None),
    "M5h role_siege_engineer_share":      (None, None, None),
    "M5i four_distinct_roles_share":      (None, None, None),
    "M6a barriers_on_ore_share":          (37.9, 35.9, 0.0),
    "M6b ore_denial_coverage_w30":        (92.5, 90.6, 0.0),
    "M6c ore_denial_coverage_w3":         (None, 80.3, 0.0),
    "M6d ore_denial_latency_median":      (1.0, 1.0, None),
    "M7 fwd_turret_removal_rate":         (76.6, 79.7, 42.8),
    "M7b fwd_turret_removal_rate_anchor": (None, None, None),
}


def aggregate(rows, deff, deny_window):
    """rows -> ordered list of metric dicts.  Every value carries its denominator."""
    n = len(rows)
    out = []

    def add(metric, value, n_str, ci=None, note=""):
        v68, v47, base = TARGETS.get(metric, (None, None, None))
        out.append({"metric": metric, "value": value, "n": n_str, "ci95": ci,
                    "target_bc_v68": v68, "target_bc_v47": v47,
                    "our_old_baseline": base, "note": note})

    # ---- M1 ---------------------------------------------------------------
    ht = sum(r["harv_end_total"] for r in rows)
    hd = sum(r["harv_end_directed"] for r in rows)
    hc = sum(r["harv_end_connected"] for r in rows)
    per_game = [r["harv_end_directed"] / r["harv_end_total"]
                for r in rows if r["harv_end_total"]]
    add("M1 belt_connectivity_directed", _pct(hd, ht),
        f"{hd}/{ht} harvesters alive at end, {n} games",
        ci95([100 * v for v in per_game], deff),
        "replay_census.Replay.chains(chain_dir), pooled over harvesters; "
        "CI is games-as-units over the %d games with >=1 surviving harvester"
        % len(per_game))
    add("M1b belt_connectivity_undirected", _pct(hc, ht),
        f"{hc}/{ht} harvesters alive at end, {n} games", None,
        "diagnostic: ignores conveyor facing")

    # ---- M2 ---------------------------------------------------------------
    bt = sum(r["barriers_total"] for r in rows)
    br = sum(r["barriers_on_enemy_ring"] for r in rows)
    pg = [100 * r["barriers_on_enemy_ring"] / r["barriers_total"]
          for r in rows if r["barriers_total"]]
    add("M2a cage_ring_share", _pct(br, bt),
        f"{br}/{bt} barriers built, {n} games", ci95(pg, deff),
        "share of ALL subject barriers landing on the enemy core's non-wall ring")
    full = sum(1 for r in rows if r["full_seal"])
    add("M2b full_seal_rate", _pct(full, n), f"{full}/{n} games",
        ci95([100 * int(r["full_seal"]) for r in rows], deff),
        "max ring tiles simultaneously held == open ring tiles")
    firsts = [r["first_ring_build"] for r in rows if r["first_ring_build"] is not None]
    add("M2c first_ring_build_median", _median(firsts),
        f"{len(firsts)}/{n} games with any ring build", None,
        "first round ANY subject building lands on the enemy ring")
    add("M2d ring_tiles_held_median", _median([r["max_seal"] for r in rows]),
        f"{n} games", None, "max simultaneously held, of a median %s open"
        % _median([r["ring_open"] for r in rows]))

    # ---- M3 ---------------------------------------------------------------
    cn = sum(r["converts_n"] for r in rows)
    cl = sum(r["converts_lattice"] for r in rows)
    add("M3a drip_lattice_share", _pct(cl, cn),
        f"{cl}/{cn} convert_ammo calls, {n} games", None,
        "amount is an exact nonneg sum of 4s and 10s; ACCEPTANCE TEST for the "
        "drip (PLAYBOOK COPY 7)")
    cns = [r["converts_n"] for r in rows]
    cts = [r["converts_ti"] for r in rows]
    add("M3b converts_per_game_median", _median(cns), f"{n} games", None,
        "p90 %s, MEAN %.1f (STUDY §3.3's v47 figure 56.2 is a mean, not a "
        "median — compare like for like)" % (_pctile(cns, 0.9),
                                             statistics.mean(cns) if cns else 0))
    add("M3c converted_ti_per_game_median", _median(cts), f"{n} games", None,
        "p90 %s, MEAN %.0f (STUDY §3.3's v47 figure 530 is a mean)"
        % (_pctile(cts, 0.9), statistics.mean(cts) if cts else 0))
    add("M3d peak_ammo_median", _median([r["peak_ammo"] for r in rows]),
        f"{n} games", None,
        "p90 %s, max %s" % (_pctile([r["peak_ammo"] for r in rows], 0.9),
                            max([r["peak_ammo"] for r in rows], default=None)))
    fc = [r["first_convert"] for r in rows if r["first_convert"] is not None]
    add("M3e first_convert_round_median", _median(fc),
        f"{len(fc)}/{n} games with any convert", None,
        "p10 %s; r0 in %d games (the field's habit, not the drip's)"
        % (_pctile(fc, 0.10), sum(1 for v in fc if v == 0)))

    # ---- M4 ---------------------------------------------------------------
    fwd = [t for r in rows for t in r["turret_builds"] if t["forward"]]
    band = sum(1 for t in fwd if 14 <= t["dsq_enemy"] <= 32)
    pb = sum(1 for t in fwd if t["dsq_enemy"] <= 13)
    add("M4a fwd_turret_band_share", _pct(band, len(fwd)),
        f"{band}/{len(fwd)} forward gunner+sentinel builds, {n} games", None,
        "d^2 14-32 from the ENEMY core footprint: inside sentinel reach, "
        "outside every gunner's")
    add("M4b fwd_turret_pointblank_share", _pct(pb, len(fwd)),
        f"{pb}/{len(fwd)} forward gunner+sentinel builds, {n} games", None,
        "d^2 <= 13 — inside a defending gunner's reach. FLAG unless home-ring "
        "clearance (M7) is at parity (PLAYBOOK COPY 5)")
    sents = [t for r in rows for t in r["turret_builds"] if t["kind"] == "sentinel"]
    sband = sum(1 for t in sents if 14 <= t["dsq_enemy"] <= 32)
    spb = sum(1 for t in sents if t["dsq_enemy"] <= 13)
    sband_a = sum(1 for t in sents if 14 <= t["dsq_enemy_anchor"] <= 32)
    spb_a = sum(1 for t in sents if t["dsq_enemy_anchor"] <= 13)
    add("M4c sentinel_band_share", _pct(sband, len(sents)),
        f"{sband}/{len(sents)} sentinel builds (ALL, not only forward), {n} games",
        None, "FOOTPRINT origin (PLAYBOOK COPY 5's wording). median d^2 %s"
        % _median([t["dsq_enemy"] for t in sents]))
    add("M4d sentinel_pointblank_share", _pct(spb, len(sents)),
        f"{spb}/{len(sents)} sentinel builds (ALL), {n} games", None,
        "FOOTPRINT origin")
    add("M4e sentinel_band_share_anchor", _pct(sband_a, len(sents)),
        f"{sband_a}/{len(sents)} sentinel builds (ALL), {n} games", None,
        "STUDY-COMPAT: d^2 to the core's NW-CORNER ANCHOR, the origin STUDY "
        "§3.5's table was actually computed on (tools/corpus/replay_events.py). "
        "This is the row that reproduces the published 48.1/32.1. median d^2 %s"
        % _median([t["dsq_enemy_anchor"] for t in sents]))
    add("M4f sentinel_pointblank_share_anchor", _pct(spb_a, len(sents)),
        f"{spb_a}/{len(sents)} sentinel builds (ALL), {n} games", None,
        "STUDY-COMPAT anchor origin; reproduces the published 23.9/53.3")

    # ---- M5 ---------------------------------------------------------------
    bs = [r["builders_spawned"] for r in rows]
    add("M5a builders_per_game_median", _median(bs), f"{n} games", None,
        "mean %.2f, max %s" % (statistics.mean(bs) if bs else float("nan"),
                               max(bs, default=None)))
    ex4 = sum(1 for v in bs if v == 4)
    add("M5b exactly_four_builders_share", _pct(ex4, n), f"{ex4}/{n} games",
        ci95([100 * int(v == 4) for v in bs], deff),
        ">4 in %d games, <4 in %d" % (sum(1 for v in bs if v > 4),
                                      sum(1 for v in bs if v < 4)))
    fourth = [sorted(r["spawn_rounds"])[3] for r in rows
              if len(r["spawn_rounds"]) >= 4]
    add("M5c fourth_spawn_round_median", _median(fourth),
        f"{len(fourth)}/{n} games with >=4 builders", None,
        "p10 %s p90 %s" % (_pctile(fourth, 0.10), _pctile(fourth, 0.90)))
    # ⚠ POPULATION IS PART OF THE DEFINITION HERE.  PLAYBOOK T2's median 1.000
    # is measured on "n=924 games with >=4 ring barriers" (v47), against a field
    # of 0.857.  Read on games with >=1 ring barrier the same bot medians 0.83,
    # because a game with two ring barriers laid by two bots scores 0.5 and drags
    # the median with no information in it.  The >=4 filter is reproduced.
    tops = [r["ring_top_share"] for r in rows
            if r["ring_top_share"] is not None
            and r["barriers_on_enemy_ring"] >= 4]
    tops_any = [r["ring_top_share"] for r in rows if r["ring_top_share"] is not None]
    add("M5d ring_barrier_top_share_median", _median(tops),
        f"{len(tops)}/{n} games with >=4 ring barriers (PLAYBOOK T2's "
        f"population)", None,
        "1.000 = one bot laid every ring barrier that game (a fixed job). "
        "field reference 0.857. On the looser >=1-ring-barrier population "
        "(n=%d) this reads %s — do not mix the two"
        % (len(tops_any), round(_median(tops_any), 3) if tops_any else None))

    for key, label in (("home_keeper", "M5e role_home_keeper_share"),
                       ("cage_walker", "M5f role_cage_walker_share"),
                       ("ore_denier", "M5g role_ore_denier_share"),
                       ("siege_engineer", "M5h role_siege_engineer_share")):
        k = sum(1 for r in rows if r["roles"][key] is not None)
        add(label, _pct(k, n), f"{k}/{n} games", None,
            "PLAYBOOK COPY 8 recogniser, on builders with >=5 actions")
    four = sum(1 for r in rows if r["roles"]["four_distinct"])
    add("M5i four_distinct_roles_share", _pct(four, n), f"{four}/{n} games",
        ci95([100 * int(r["roles"]["four_distinct"]) for r in rows], deff),
        "all four COPY-8 roles filled by four DIFFERENT builders in the same "
        "game — the checkable form of 'four fixed jobs'. ⛔ READ THE CAVEAT: on "
        "Bean counters v68 this measures 1.8% (2/112). The literal recognisers "
        "COPY 8 publishes co-occur almost never, so 'four fixed jobs' is a "
        "watched-game narrative, NOT a census-verified property. Do not set a "
        "SKALMAN acceptance bar on this row; use M5b + M5g + M5d instead")

    # ---- M6 ---------------------------------------------------------------
    onore = sum(r["barriers_on_ore"] for r in rows)
    add("M6a barriers_on_ore_share", _pct(onore, bt),
        f"{onore}/{bt} barriers built, {n} games", None,
        "engine: harvesters can only be built on ore, so a barrier there "
        "denies the tile permanently")
    hd_n = sum(r["enemy_harv_deaths"] for r in rows)
    c30 = sum(r["ore_covered_30"] for r in rows)
    cw = sum(r["ore_covered_w"] for r in rows)
    add("M6b ore_denial_coverage_w30", _pct(c30, hd_n),
        f"{c30}/{hd_n} enemy harvester deaths, {n} games", None,
        "subject barriers that tile within 30 rounds — the study's window")
    add("M6c ore_denial_coverage_w3", _pct(cw, hd_n),
        f"{cw}/{hd_n} enemy harvester deaths, {n} games", None,
        f"within {deny_window} rounds — the tight window the COPY-1 trigger "
        "specifies")
    lats = [v for r in rows for v in r["ore_latencies"]]
    add("M6d ore_denial_latency_median", _median(lats),
        f"{len(lats)} covered deaths", None,
        "p90 %s, min %s" % (_pctile(lats, 0.9), min(lats) if lats else None))

    # ---- M7 ---------------------------------------------------------------
    ft = sum(r["fwd_turrets_against"] for r in rows)
    fr = sum(r["fwd_turrets_removed"] for r in rows)
    fid = sum(r["fwd_turrets_removed_by_id"] for r in rows)
    fta = sum(r["fwd_turrets_against_anchor"] for r in rows)
    fra = sum(r["fwd_turrets_removed_anchor"] for r in rows)
    gshare_a = [100 * r["fwd_turrets_removed_anchor"] / r["fwd_turrets_against_anchor"]
                for r in rows if r["fwd_turrets_against_anchor"]]
    gshare = [100 * r["fwd_turrets_removed"] / r["fwd_turrets_against"]
              for r in rows if r["fwd_turrets_against"]]
    # ⭐ GAMES AS UNITS is the study's own stated unit for this row ("games as
    # units, DEFF 1.833") and it is NOT the same number as the pooled turret
    # share — 75.8% vs 66.9% on BC v68, because games with many forward turrets
    # are games where clearance is failing.  Publishing the pooled number under
    # the study's label would silently compare two different statistics, so the
    # headline is the game-level mean and the pooled ratio rides in the note.
    add("M7 fwd_turret_removal_rate",
        statistics.mean(gshare) if gshare else None,
        f"{len(gshare)}/{n} games holding >=1 enemy forward turret "
        f"({fr}/{ft} turrets)", ci95(gshare, deff),
        "GAMES AS UNITS (the study's unit). subject is the DEFENDER. "
        "pooled turret share %s%%; entity-id-matched variant %s%% of turrets "
        "(diagnostic — the study's published definition matches on "
        "(kind, tile, later round) only, so it can credit a REBUILT turret's "
        "death to the original)"
        % (round(_pct(fr, ft), 1) if ft else None,
           round(_pct(fid, ft), 1) if ft else None))
    add("M7b fwd_turret_removal_rate_anchor",
        statistics.mean(gshare_a) if gshare_a else None,
        f"{len(gshare_a)}/{n} games holding >=1 ({fra}/{fta} turrets)",
        ci95(gshare_a, deff),
        "STUDY-COMPAT origin (NW-corner anchor) for the 'forward' test only")
    return out


# --- population loading -------------------------------------------------------

def load_manifest(path: Path, replay_root: Path):
    out = []
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 2:
            raise SystemExit(f"{path}: manifest needs file<TAB>side, got: {line!r}")
        out.append((replay_root / p[0], int(p[1])))
    return out


def load_corpus(team_id=None, team_name=None, versions=None, replay_root=None):
    """Subject side from corpus/meta_join.tsv — the authority for who is who."""
    if not META_JOIN.exists():
        raise SystemExit(f"{META_JOIN} not found")
    want = set(versions) if versions else None
    out = []
    with open(META_JOIN) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if team_id and r["teamAId"] == team_id:
                side, ver = 0, r["teamAVersion"]
            elif team_id and r["teamBId"] == team_id:
                side, ver = 1, r["teamBVersion"]
            elif team_name and r["teamAName"] == team_name:
                side, ver = 0, r["teamAVersion"]
            elif team_name and r["teamBName"] == team_name:
                side, ver = 1, r["teamBVersion"]
            else:
                continue
            if want and ver not in want:
                continue
            out.append((replay_root / r["file"], side))
    return out


def run_population(files, deff, deny_window, flip_side=False):
    rows = []
    skipped = []
    t0 = time.time()
    for path, side in files:
        if not path.exists():
            skipped.append((str(path), "missing"))
            continue
        try:
            rows.append(scan_replay(path, (1 - side) if flip_side else side,
                                    deny_window))
        except Exception as exc:                                # noqa: BLE001
            skipped.append((path.name, f"{type(exc).__name__}: {exc}"))
    if not rows:
        raise SystemExit("no replays scanned — REFUSING to print an empty table "
                         "(an empty population reads as a clean zero on every "
                         "metric, which is the worst reading in this repo)")
    metrics = aggregate(rows, deff, deny_window)
    return {"n_games": len(rows), "skipped": skipped,
            "elapsed_s": round(time.time() - t0, 2),
            "metrics": metrics, "per_game": rows}


def print_table(res, label, era, out=sys.stdout):
    tgt = "target_bc_v68" if era == "v68" else "target_bc_v47"
    print(f"# SKALMAN FIDELITY  label={label!r}  games={res['n_games']}  "
          f"era_column={era}  elapsed={res['elapsed_s']}s", file=out)
    if res["skipped"]:
        print(f"# skipped={len(res['skipped'])}  first: {res['skipped'][0]}",
              file=out)
    cols = ["metric", "value", "ci95", "n", f"target_bc_{era}",
            "our_old_baseline", "note"]
    print("\t".join(cols), file=out)
    for m in res["metrics"]:
        def f(v):
            if v is None:
                return ""
            return f"{v:.1f}" if isinstance(v, float) else str(v)
        print("\t".join([m["metric"], f(m["value"]), f(m["ci95"]), m["n"],
                         f(m[tgt]), f(m["our_old_baseline"]), m["note"]]),
              file=out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="SKALMAN phase-1 replication-fidelity instrument")
    ap.add_argument("--manifest", help="TSV: file<TAB>subject_side[<TAB>...]")
    ap.add_argument("--dir", help="directory of .replay26 files")
    ap.add_argument("--team-id", help="team uuid; subject side from meta_join")
    ap.add_argument("--team-name", help="team name; subject side from meta_join")
    ap.add_argument("--versions", help="comma-separated versions to keep")
    ap.add_argument("--side", type=int, choices=(0, 1),
                    help="subject side for --dir when meta_join is not used")
    ap.add_argument("--replay-root", default=str(DEFAULT_REPLAY_ROOT))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--label", default="unnamed population")
    ap.add_argument("--era", choices=("v68", "v47"), default="v68",
                    help="which Bean-counters era the target column shows")
    ap.add_argument("--deff", type=float, default=1.833,
                    help="design effect for games-as-units intervals "
                         "(1.833 unrated / 1.529 rated, CLAUDE.md s40)")
    ap.add_argument("--deny-window", type=int, default=3,
                    help="M6c ore-denial window in rounds")
    ap.add_argument("--json", help="write the machine-readable result here "
                                   "('-' for stdout)")
    ap.add_argument("--per-game", action="store_true",
                    help="include the per-game records in --json")
    a = ap.parse_args()

    root = Path(a.replay_root)
    if a.manifest:
        files = load_manifest(Path(a.manifest), root)
    elif a.dir:
        paths = sorted(Path(a.dir).glob("*.replay26"))
        if a.side is not None:
            files = [(p, a.side) for p in paths]
        elif a.team_id or a.team_name:
            lut = {p.name: s for p, s in load_corpus(a.team_id, a.team_name,
                                                    None, root)}
            missing = [p.name for p in paths if p.name not in lut]
            if missing:
                raise SystemExit(
                    f"--dir: {len(missing)} files not in meta_join, so their "
                    f"subject side is UNKNOWN (first: {missing[0]}). Pass "
                    f"--side explicitly or fix the corpus — REFUSING to guess.")
            files = [(p, lut[p.name]) for p in paths]
        else:
            raise SystemExit("--dir needs --side or --team-id/--team-name: the "
                             "subject side is not in the file")
    elif a.team_id or a.team_name:
        vers = a.versions.split(",") if a.versions else None
        files = load_corpus(a.team_id, a.team_name, vers, root)
    else:
        raise SystemExit("need one of --manifest / --dir / --team-id / --team-name")
    files.sort()
    if a.limit:
        files = files[:a.limit]
    res = run_population(files, a.deff, a.deny_window)
    print_table(res, a.label, a.era)
    if a.json:
        payload = {"label": a.label, "era": a.era, "deff": a.deff,
                   "deny_window": a.deny_window, "n_games": res["n_games"],
                   "skipped": res["skipped"], "elapsed_s": res["elapsed_s"],
                   "metrics": res["metrics"]}
        if a.per_game:
            payload["per_game"] = res["per_game"]
        text = json.dumps(payload, indent=2)
        if a.json == "-":
            print(text)
        else:
            Path(a.json).write_text(text + "\n")
            print(f"# json -> {a.json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
