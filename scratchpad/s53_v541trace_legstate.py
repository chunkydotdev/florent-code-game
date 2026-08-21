#!/usr/bin/env python3
"""s53 / QUEUE #109 -- LEG-STATE reconstruction for the v541 additive path.

WHAT THIS ANSWERS.  The additive path was inert in the shipped bytes
(`FS_V541_IDLEPECK = False`, doctrine.py:5937), so its refusal coverage is 100%
by construction and needs no replay.  This script answers the NEXT question,
which is the one the builder actually needs for the fix decision:

    IF the flag had shipped True, which of the downstream clauses would have
    refused, and on how many of the leg's exposed adjacent rounds?

INPUTS RECONSTRUCTED PER ROUND, ENGINE-SIDE:
  * our global AMMUNITION and TITANIUM        <- update field 6 `updatePlayers`
                                                 (d[1]=titanium, d[7]=ammo;
                                                 the same decode
                                                 tools/corpus/replay_econ.py:316-330
                                                 uses).  END-OF-ROUND values.
  * our live FORWARD SENTINELS                 <- entity registry, ours, kind
                                                 sentinel, dsq_core(pos, ENEMY
                                                 core) <= 40 -- the engine-side
                                                 truth behind
                                                 `_fs_live_sentinels_vision`
                                                 (siege.py:5668).
  * ORTHOGONAL ADJACENCY of our builders to the enemy core footprint
  * whether that body MOVED / ATTACKED in the round (idle proxy)

⚠ WHAT IS *NOT* RECONSTRUCTIBLE AND IS BOUNDED INSTEAD -- stated, not hidden:
  1. `_fs_live_sentinels` is a VISION census (max'd with a team-global beat).
     This script computes the ENGINE truth (all our sentinels within d^2<=40 of
     the enemy core), which is an UPPER bound on the vision census and, via the
     beat's `max(1, ...)`, an upper bound on the function too.  A larger `live`
     makes the ammunition clause MORE likely to refuse and the KEEP_SENT term
     LESS likely to refuse, so the two counts bracket rather than agree.
  2. The bot reads ammo/titanium DURING its turn; `updatePlayers` is the
     END-OF-ROUND value.  Intra-round spend (a barrier, a sentinel, a
     convert_ammo) is not separable, so both series are approximations at
     round resolution.
  3. `len(needed)` (the collar's remaining barrier debt) is PER-BODY private
     state and is not in the replay.  The reserve is therefore computed with
     `needed = []` -- the RAID-layer call site's own value (raid.py:480) and a
     strict LOWER bound on the siege call sites' reserve.  Reserve refusals are
     consequently a LOWER bound.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (  # noqa: E402
    Replay, fields, parse_entity, read_pos, CARDINALS)

OUR_TEAM_NAME = "OpenSverige"

# shipped constants, quoted with anchors (never re-derived here)
FS_V541_AMMO_MIN = 120      # doctrine.py:6049
FS_V541_TI_FLOOR = 8        # doctrine.py:5976
FS_SEAL_MARGIN = 6          # doctrine.py:2448
SENTINEL_BASE_COST = 30     # scaled at runtime; see the note in the readout
FWD_SENT_DSQ = 40           # siege.py:5677


def orth_ring(r, team):
    foot = set(r.core_footprint(team))
    out = set()
    for (x, y) in foot:
        for dx, dy in CARDINALS:
            n = (x + dx, y + dy)
            if n in foot:
                continue
            if 0 <= n[0] < r.width and 0 <= n[1] < r.height:
                out.add(n)
    return out


def dsq_core(pos, foot):
    return min((pos[0] - f[0]) ** 2 + (pos[1] - f[1]) ** 2 for f in foot)


def decode(path: Path, our_team: int, sent_cost: int):
    r = Replay(path, track_flow=False)
    enemy = 1 - our_team
    foot = {t: set(r.core_footprint(t)) for t in (0, 1)}
    ring_enemy = orth_ring(r, enemy)

    raw = path.read_bytes()
    turn_bufs = [buf for num, _w, buf in fields(raw) if num == 3]

    ents = {}
    for c in r.cores:
        ents[c["id"]] = [c["team"], "core", c["pos"]]

    ti = {0: 500, 1: 500}
    ammo = {0: 0, 1: 0}

    acc = dict(
        adj_body_rounds=0,        # (round, body) cells with orth adjacency
        adj_rounds=0,             # rounds with >=1 adjacent body
        idle_cells=0,             # adjacent cells where the body neither moved
                                  # nor attacked that round
        ammo_refuse=0, ammo_refuse_idle=0,
        res_refuse=0, res_refuse_idle=0,
        both_refuse=0, none_refuse=0, none_refuse_idle=0,
        live_sent_cells=0,
        ammo_min=None, ammo_max=0, ti_min=None, ti_max=0,
    )

    for rnd, tb in enumerate(turn_bufs):
        moved = set()
        attacked = set()
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is not None:
                            ents[e.id] = [e.team, e.kind, e.pos]
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        if ents[eid][2] != to:
                            moved.add(eid)
                        ents[eid][2] = to
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                elif unum == 13:
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            attacked.add(av)
                elif unum == 6:                     # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn not in (1, 2):
                                continue
                            d = {}
                            for k, w2, v in fields(tv):
                                d[k] = v
                            # ⛔ PROTO3 OMITS ZERO-VALUED FIELDS.  Carrying the
                            # previous value forward on an absent field reads a
                            # ZERO bank/magazine as the last NONZERO one --
                            # caught 2026-08-21 by cross-checking against
                            # tools/corpus/replay_econ.py:328-330, which
                            # defaults to 0 and disagreed with the
                            # carry-forward form on exactly the zero cells
                            # (6db3add5 g1 team B: econ 0, carry-forward 10).
                            # Absent == 0, per that decoder.
                            ti[tn - 1] = d.get(1, 0)
                            ammo[tn - 1] = d.get(7, 0)

        our_ammo, our_ti = ammo[our_team], ti[our_team]
        acc["ammo_max"] = max(acc["ammo_max"], our_ammo)
        acc["ti_max"] = max(acc["ti_max"], our_ti)

        live = sum(1 for v in ents.values()
                   if v[0] == our_team and v[1] == "sentinel"
                   and dsq_core(v[2], foot[enemy]) <= FWD_SENT_DSQ)

        adj = [eid for eid, v in ents.items()
               if v[0] == our_team and v[1] == "builder_bot"
               and v[2] in ring_enemy]
        if adj:
            acc["adj_rounds"] += 1
            if acc["ammo_min"] is None or our_ammo < acc["ammo_min"]:
                acc["ammo_min"] = our_ammo
            if acc["ti_min"] is None or our_ti < acc["ti_min"]:
                acc["ti_min"] = our_ti
        for eid in adj:
            acc["adj_body_rounds"] += 1
            if live:
                acc["live_sent_cells"] += 1
            idle = (eid not in moved) and (eid not in attacked)
            if idle:
                acc["idle_cells"] += 1
            # --- the shipped clauses, re-evaluated on this cell -------------
            a_ref = (live > 0 and our_ammo < FS_V541_AMMO_MIN)
            reserve = FS_SEAL_MARGIN + FS_V541_TI_FLOOR
            if live == 0:
                reserve += sent_cost
            r_ref = our_ti < reserve
            if a_ref:
                acc["ammo_refuse"] += 1
                if idle:
                    acc["ammo_refuse_idle"] += 1
            if r_ref:
                acc["res_refuse"] += 1
                if idle:
                    acc["res_refuse_idle"] += 1
            if a_ref and r_ref:
                acc["both_refuse"] += 1
            if not a_ref and not r_ref:
                acc["none_refuse"] += 1
                if idle:
                    acc["none_refuse_idle"] += 1

    acc["rounds"] = len(turn_bufs)
    acc["file"] = path.name
    acc["ammo_min"] = -1 if acc["ammo_min"] is None else acc["ammo_min"]
    acc["ti_min"] = -1 if acc["ti_min"] is None else acc["ti_min"]
    return acc


def our_side(meta):
    if meta.get("teamAName") == OUR_TEAM_NAME:
        return 0
    if meta.get("teamBName") == OUR_TEAM_NAME:
        return 1
    raise ValueError("our team on neither side")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--match-dir", default="replay_archive")
    ap.add_argument("--match", action="append", default=[])
    ap.add_argument("--sent-cost", type=int, default=SENTINEL_BASE_COST,
                    help="scaled sentinel cost used in the KEEP_SENT reserve "
                         "term; 30 is the BASE cost and therefore the LOWEST "
                         "the live scaled value can ever be -> reserve "
                         "refusals stay a lower bound")
    a = ap.parse_args(argv)
    d = Path(a.match_dir)
    hdr = None
    tot = {}
    for mid in a.match:
        meta = json.loads((d / f"{mid}.meta.json").read_text())
        our = our_side(meta)
        for g in range(1, 6):
            p = d / f"{mid}_game_{g}.replay26"
            if not p.exists():
                print("MISSING\t%s" % p, file=sys.stderr)
                continue
            row = decode(p, our, a.sent_cost)
            row["match"] = mid[:8]
            row["game"] = g
            if hdr is None:
                hdr = (["match", "game", "rounds", "adj_rounds",
                        "adj_body_rounds", "idle_cells", "live_sent_cells",
                        "ammo_refuse", "ammo_refuse_idle", "res_refuse",
                        "res_refuse_idle", "both_refuse", "none_refuse",
                        "none_refuse_idle", "ammo_min", "ammo_max",
                        "ti_min", "ti_max"])
                print("\t".join(hdr))
            print("\t".join(str(row[k]) for k in hdr))
            for k in hdr[2:]:
                if k in ("ammo_min", "ti_min"):
                    continue
                if k in ("ammo_max", "ti_max"):
                    tot[k] = max(tot.get(k, 0), row[k])
                else:
                    tot[k] = tot.get(k, 0) + row[k]
    print("\nPOOLED (25 games):", file=sys.stderr)
    for k, v in tot.items():
        print("  %-20s %d" % (k, v), file=sys.stderr)
    n = tot.get("adj_body_rounds", 0)
    if n:
        print("\n  denominator = %d (round, adjacent-body) cells" % n,
              file=sys.stderr)
        for k in ("ammo_refuse", "res_refuse", "both_refuse", "none_refuse",
                  "idle_cells", "live_sent_cells"):
            print("  %-20s %6d  = %5.1f%%"
                  % (k, tot[k], 100.0 * tot[k] / n), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
