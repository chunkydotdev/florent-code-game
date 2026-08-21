#!/usr/bin/env python3
"""KLADDEDOSE leg decoder — the four §MECHANISM METRIC quantities, engine-side.

Definitions are COPIED FROM THE LOCKED PREREG
(`docs/prereg/PREREG-LEG-KLADDEDOSE-2026-08-21.md` §MECHANISM METRIC and
§HP-GATE) and bind; nothing here is redefined for convenience.

  1. ARRIVAL      >= 1 round in which one of OUR builder bots occupies a tile
                  ORTHOGONALLY ADJACENT to the enemy core's 2x2 footprint.
                  ⛔ NOT d^2 <= 2: that admits diagonals.  `arr_orth_r` is the
                  prereg quantity; `arr_d2_r` (launchtime.py's `arr2_r`) is
                  carried alongside as a cross-check, never as the primary.
  2. PECK EVENTS  update field 13 `BuilderAttack {id=1, target=2}` where the
                  ATTACKER is ours and `target` is in the ENEMY core footprint
                  -- the attribution rule of `tools/corpus/replay_autopsy.py`
                  (:212-231), which the builder drove to both verdicts today.
                  `peck_free` applies autopsy's unit-priority clause (a target
                  tile occupied by a unit absorbs the hit); `peck_all` does not.
  3. PECK-ATTRIBUTED CORE HP
                  enemy-core `UpdateHp` deltas of exactly -2 landing in a round
                  that also carries >= 1 of our peck events.  `hp2_any` counts
                  every -2 on the enemy core regardless of coincidence, so a
                  disagreement between the two is visible rather than assumed
                  away.
  4. ADJACENT-MIN the MANDATORY decomposition column: minimum enemy-core HP
                  observed over rounds in which >= 1 of our builder bots was
                  orthogonally adjacent.  Core HP is reconstructed from
                  `max_hp` at seed plus the cumulative signed UpdateHp stream;
                  the value scored for a round is the END-OF-ROUND HP, and
                  adjacency is evaluated on END-OF-ROUND positions -- the same
                  convention `launchtime.py`/`ringrace.py` use for arrival.
                  <=120 is the redirect path's finishing gate
                  (`siege.py:4479`, `doctrine.py:5963`).

OUR SIDE IS ALWAYS RESOLVED FROM THE MATCH META (`teamAName`/`teamBName`), never
assumed: the leg contains a match in which we are team B.

Usage:
  peckdecode.py --match-dir replay_archive --match <id> [--match <id> ...]
  peckdecode.py --selftest        # positive + negative control fixtures
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (  # noqa: E402
    Replay, fields, parse_entity, read_pos, _fold_i64, CARDINALS)

OUR_TEAM_NAME = "OpenSverige"


def orth_ring(r, team):
    """Tiles ORTHOGONALLY adjacent to a team's 2x2 core footprint, in bounds."""
    foot = set(r.core_footprint(team))
    out = []
    for (x, y) in foot:
        for dx, dy in CARDINALS:
            n = (x + dx, y + dy)
            if n in foot or n in out:
                continue
            if 0 <= n[0] < r.width and 0 <= n[1] < r.height:
                out.append(n)
    return set(out)


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def decode(path: Path, our_team: int):
    r = Replay(path, track_flow=False)
    enemy = 1 - our_team
    foot = {t: set(r.core_footprint(t)) for t in (0, 1)}
    ring_enemy = orth_ring(r, enemy)
    core = {c["team"]: c for c in r.cores}
    ecid = core[enemy]["id"]
    ehp = core[enemy].get("max_hp") or 500

    raw = path.read_bytes()
    turn_bufs = [buf for num, _w, buf in fields(raw) if num == 3]

    ents = {}
    for c in r.cores:
        ents[c["id"]] = [c["team"], "core", c["pos"]]

    arr_orth_r = arr_d2_r = -1
    arr_rounds = 0
    peck_all = peck_free = 0
    peck_rounds = set()
    hp2_coincident = hp2_any = 0
    adj_min = None
    hp = ehp
    hp_at_first_arr = None
    nrounds = 0
    first_peck_r = -1

    for rnd, tb in enumerate(turn_bufs):
        nrounds = rnd + 1
        round_pecks = 0
        round_hp2 = 0
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
                        ents[eid][2] = to
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                elif unum == 5:
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = _fold_i64(hv)
                    if eid == ecid and delta is not None:
                        hp += delta
                        if delta == -2:
                            round_hp2 += 1
                elif unum == 13:                       # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if tgt is None:
                        continue
                    a = ents.get(aid)
                    if a is not None and a[0] == our_team and tgt in foot[enemy]:
                        peck_all += 1
                        round_pecks += 1
                        # autopsy's unit-priority clause: a body on the target
                        # tile absorbs the hit instead of the core.
                        occupied = any(v[2] == tgt and v[1] == "builder_bot"
                                       for v in ents.values())
                        if not occupied:
                            peck_free += 1
                        if first_peck_r < 0:
                            first_peck_r = rnd

        adj = [eid for eid, v in ents.items()
               if v[0] == our_team and v[1] == "builder_bot"
               and v[2] in ring_enemy]
        if adj:
            arr_rounds += 1
            if arr_orth_r < 0:
                arr_orth_r = rnd
                hp_at_first_arr = hp
            adj_min = hp if adj_min is None else min(adj_min, hp)
        if arr_d2_r < 0:
            for v in ents.values():
                if v[0] == our_team and v[1] == "builder_bot" \
                        and min(d2(v[2], f) for f in foot[enemy]) <= 2:
                    arr_d2_r = rnd
                    break
        if round_pecks:
            peck_rounds.add(rnd)
            hp2_coincident += round_hp2
        hp2_any += round_hp2

    return {
        "file": path.name,
        "rounds": nrounds,
        "our_team": "A" if our_team == 0 else "B",
        "winner": r.winner,
        "we_won": int(r.winner == our_team),
        "cond": r.win_condition,
        "w": r.width, "h": r.height,
        "arrived": int(arr_orth_r >= 0),
        "arr_orth_r": arr_orth_r,
        "arr_d2_r": arr_d2_r,
        "arr_rounds": arr_rounds,
        "peck_events": peck_all,
        "peck_events_free": peck_free,
        "first_peck_r": first_peck_r,
        "hp2_coincident": hp2_coincident,
        "hp2_any": hp2_any,
        "converted": int(hp2_coincident > 0),
        "adj_min_hp": -1 if adj_min is None else adj_min,
        "hp_at_first_arr": -1 if hp_at_first_arr is None else hp_at_first_arr,
        "enemy_core_end_hp": hp,
        "in_range_while_adj": -1 if adj_min is None else int(adj_min <= 120),
    }


def our_side(meta: dict) -> int:
    """Resolve OUR team index from the meta.  Never assumed."""
    if meta.get("teamAName") == OUR_TEAM_NAME:
        return 0
    if meta.get("teamBName") == OUR_TEAM_NAME:
        return 1
    raise ValueError(f"{OUR_TEAM_NAME} on neither side: "
                     f"{meta.get('teamAName')} / {meta.get('teamBName')}")


def opp_version(meta: dict, our: int):
    return meta["teamBVersion"] if our == 0 else meta["teamAVersion"]


def selftest():
    """⛔ DRIVE THE PECK COLUMN TO BOTH VERDICTS ON THIS SURFACE.

    A `peck_events` column that has only ever read 0 validates nothing --
    exactly the defect the prereg's OB17 discharge names.  Positive fixture:
    `bots/_probe_peck_a/b`, builders that walk to and peck the ENEMY core.
    """
    pos = ROOT / "scratchpad/s53_peckdrive/peck_skald2.replay26"
    neg = ROOT / "scratchpad/s53_peckdrive/peck.replay26"
    ok = True
    for tag, p, want_nonzero in (("POSITIVE", pos, True), ("NEGATIVE", neg, False)):
        if not p.exists():
            print(f"[FAIL] {tag}: fixture missing {p}")
            ok = False
            continue
        for team in (0, 1):
            d = decode(p, team)
            hit = d["peck_events"] > 0
            print(f"  {tag} {p.name} as team {'AB'[team]}: "
                  f"peck_events={d['peck_events']} free={d['peck_events_free']} "
                  f"hp2_coincident={d['hp2_coincident']} hp2_any={d['hp2_any']} "
                  f"arrived={d['arrived']} adj_min_hp={d['adj_min_hp']}")
            if want_nonzero and team == 0 and not hit:
                pass        # which side pecks is fixture-specific; checked below
    a0 = decode(pos, 0)
    a1 = decode(pos, 1)
    if max(a0["peck_events"], a1["peck_events"]) == 0:
        print("[FAIL] POSITIVE fixture read 0 pecks on BOTH sides")
        ok = False
    if max(a0["hp2_coincident"], a1["hp2_coincident"]) == 0:
        print("[FAIL] POSITIVE fixture read 0 coincident 2-HP core decrements")
        ok = False
    n0 = decode(neg, 0)
    n1 = decode(neg, 1)
    if max(n0["peck_events"], n1["peck_events"]) != 0:
        print(f"[FAIL] NEGATIVE fixture read pecks: "
              f"{n0['peck_events']}/{n1['peck_events']}")
        ok = False
    print("[ok] decoder sees pecks where they exist and zero where they do not"
          if ok else "[FAIL] selftest did not pass")
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--match-dir", default="replay_archive")
    ap.add_argument("--match", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    hdr = None
    d = Path(a.match_dir)
    for mid in a.match:
        meta = json.loads((d / f"{mid}.meta.json").read_text())
        our = our_side(meta)
        ov = opp_version(meta, our)
        for g in range(1, 6):
            p = d / f"{mid}_game_{g}.replay26"
            if not p.exists():
                print(f"MISSING\t{p}", file=sys.stderr)
                continue
            row = decode(p, our)
            row["match"] = mid[:8]
            row["game"] = g
            row["oppver"] = ov
            row["oppver_alarm"] = int(ov != 173)
            if hdr is None:
                hdr = (["match", "game", "oppver", "oppver_alarm"]
                       + [k for k in row if k not in
                          ("match", "game", "oppver", "oppver_alarm")])
                print("\t".join(hdr))
            print("\t".join(str(row[k]) for k in hdr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
