#!/usr/bin/env python3
"""HEAL_READ — the opponent's healing response, decoded off the `builderHeal`
EVENT rather than off positive HP deltas.

WHY A SECOND INSTRUMENT AT ALL. The LOKI-19 read-out's §11 healing asymmetry was
measured by summing POSITIVE UpdateHp deltas on the enemy core (`hp_ledger.py`).
That instrument has no selftest and its first output was wrong by nineteen orders
of magnitude. This walks a DIFFERENT wire path — `Update{builderHeal{id,target}}`
(field 15) — which additionally carries WHO healed and WHEN, so it can answer the
question the delta sum cannot: **is the healing TRIGGERED by our peck, or is it a
LEVEL difference that would show against any pressure?**

The two paths are related by an arithmetic identity the engine gives us for free:
a heal is +4 HP to all friendly entities on the target tile, so for heals aimed at
the enemy core footprint

    4 x (their core heals)  ==  (sum of positive HP deltas on their core)

EXCEPT where a heal is clipped by max HP. That identity is selftest cell F, and it
is what lets this decoder and `hp_ledger` check each other instead of agreeing by
construction.

  --selftest   synthetic replays with answers forced BY CONSTRUCTION
  --leg        the 100 LOKI-19 games, per arm and per cell
  --archive    the trigger-vs-level cut over the wider archive

Read-only. Research-arm scratch instrument. Not a bar.
"""
from __future__ import annotations
import json, sys, glob, statistics
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402
from peck_read import core_footprint                                # noqa: E402
from ring_read import (_sf_v, _sf_l, _sf_pos, _sf_entity, _sf_place,  # noqa: E402
                       _sf_replay, _sf_blank_turns, _sf_turn)

ARCHIVE = ROOT / "replay_archive"
U_PLACE, U_HP, U_ATTACK, U_HEAL = 1, 5, 13, 15


def _signed(v: int) -> int:
    """protobuf int32: negatives arrive sign-extended to 64 bits."""
    return v - (1 << 64) if v >= (1 << 63) else v


def decode(path: Path, our_team: int) -> dict | None:
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(1, 0), d.get(2, 0), read_pos(d[3])))
    theirs = [c for c in cores if c[1] != our_team]
    ours = [c for c in cores if c[1] == our_team]
    if not theirs or not ours:
        return None
    ecid, _, epos = theirs[0]
    efoot = core_footprint(epos)
    ocid, _, opos = ours[0]
    ofoot = core_footprint(opos)

    team_of: dict[int, int] = {}
    r = dict(rounds=len(turn_bufs),
             our_pecks=0, first_peck=-1,
             their_core_heals=0, their_heals_any=0,
             our_core_heals=0, our_heals_any=0,
             ecore_neg=0, ecore_pos=0, ocore_neg=0, ocore_pos=0)
    heals_by_round: dict[int, int] = defaultdict(int)
    pecks_by_round: dict[int, int] = defaultdict(int)

    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == U_PLACE:
                    for en, _ew, ebuf in fields(ubuf):
                        if en == 1:
                            e = parse_entity(ebuf, rnd)
                            if e is not None:
                                team_of[e.id] = e.team
                elif unum in (U_ATTACK, U_HEAL):
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if aid is None or tgt is None:
                        continue
                    t = team_of.get(aid)
                    if unum == U_ATTACK:
                        if t == our_team and tgt in efoot:
                            r["our_pecks"] += 1
                            pecks_by_round[rnd] += 1
                            if r["first_peck"] < 0:
                                r["first_peck"] = rnd
                    else:
                        if t is not None and t != our_team:
                            r["their_heals_any"] += 1
                            if tgt in efoot:
                                r["their_core_heals"] += 1
                                heals_by_round[rnd] += 1
                        elif t == our_team:
                            r["our_heals_any"] += 1
                            if tgt in ofoot:
                                r["our_core_heals"] += 1
                elif unum == U_HP:
                    d = {n: v for n, _, v in fields(ubuf)}
                    eid, dl = d.get(1), _signed(d.get(2, 0))
                    if eid == ecid:
                        r["ecore_neg" if dl < 0 else "ecore_pos"] += abs(dl)
                    elif eid == ocid:
                        r["ocore_neg" if dl < 0 else "ocore_pos"] += abs(dl)
    r["heals_by_round"] = dict(heals_by_round)
    r["pecks_by_round"] = dict(pecks_by_round)
    return r


# ---------------------------------------------------------------------------
# SELFTEST — every answer forced by construction, never by a stored figure.
# Enemy core id=2 team=1 at (8,8) -> footprint {(8,8),(9,8),(8,9),(9,9)}.
# ---------------------------------------------------------------------------
def _sf_evt(unum: int, eid: int, xy) -> bytes:
    return _sf_l(unum, _sf_v(1, eid) + _sf_l(2, _sf_pos(xy)))


def _sf_hp(eid: int, delta: int) -> bytes:
    enc = delta if delta >= 0 else delta + (1 << 64)
    return _sf_l(U_HP, _sf_v(1, eid) + _sf_v(2, enc))


_W = _H = 12
_CORES = [(1, 0, (1, 1)), (2, 1, (8, 8))]
_FOOT = (8, 8)          # a tile INSIDE the enemy core footprint
_OFF = (5, 5)           # a tile outside every footprint
_THEM, _US = 20, 10     # builder bot ids


def _cells():
    cells = []
    base = [_sf_place(_sf_entity(_US, 0, (7, 8), "builder_bot")),
            _sf_place(_sf_entity(_THEM, 1, (8, 7), "builder_bot"))]

    # A. nothing happens -> every counter zero. Catches a decoder that invents.
    t = _sf_blank_turns(); t[0] = base
    cells.append(("A quiet game", "no attack/heal events exist at all",
                  _sf_replay(_W, _H, _CORES, t), 0,
                  [("our_pecks", 0), ("their_core_heals", 0),
                   ("their_heals_any", 0), ("ecore_pos", 0)]))

    # B. 7 of their heals ON the core footprint, 3 OFF it.
    t = _sf_blank_turns(); t[0] = base
    for i in range(7):
        t[i + 1] = [_sf_evt(U_HEAL, _THEM, _FOOT)]
    for i in range(3):
        t[i + 20] = [_sf_evt(U_HEAL, _THEM, _OFF)]
    cells.append(("B heal targeting", "7 aimed at the footprint, 3 away from it",
                  _sf_replay(_W, _H, _CORES, t), 0,
                  [("their_core_heals", 7), ("their_heals_any", 10)]))

    # C. OUR heals must never be counted as theirs. Same events, our team.
    t = _sf_blank_turns(); t[0] = base
    for i in range(5):
        t[i + 1] = [_sf_evt(U_HEAL, _US, _FOOT)]
    cells.append(("C team attribution", "5 heals by OUR bot at THEIR footprint",
                  _sf_replay(_W, _H, _CORES, t), 0,
                  [("their_core_heals", 0), ("their_heals_any", 0),
                   ("our_heals_any", 5)]))

    # D. the same replay decoded from the OTHER side must mirror exactly.
    #    Forces the our_team argument to be load-bearing rather than decorative.
    t = _sf_blank_turns(); t[0] = base
    for i in range(6):
        t[i + 1] = [_sf_evt(U_HEAL, _THEM, _FOOT)]
    cells.append(("D side symmetry", "decoded as team 1: their heals become ours",
                  _sf_replay(_W, _H, _CORES, t), 1,
                  [("their_core_heals", 0), ("our_heals_any", 6)]))

    # E. first_peck is the ROUND of the first footprint attack, not of any attack.
    t = _sf_blank_turns(); t[0] = base
    t[5] = [_sf_evt(U_ATTACK, _US, _OFF)]         # off-footprint: not a peck
    t[9] = [_sf_evt(U_ATTACK, _US, _FOOT)]
    t[11] = [_sf_evt(U_ATTACK, _US, _FOOT)]
    cells.append(("E first peck round", "off-footprint swing at r5 must not count",
                  _sf_replay(_W, _H, _CORES, t), 0,
                  [("our_pecks", 2), ("first_peck", 9)]))

    # F. THE CROSS-PATH IDENTITY, and it is the cell that matters:
    #    4 heals on the footprint + the +4 HP deltas the engine would emit.
    #    heal EVENTS and HP DELTAS are different fields; if the decoder read one
    #    and reported the other, this cell separates them.
    t = _sf_blank_turns(); t[0] = base
    for i in range(4):
        t[i + 1] = [_sf_evt(U_HEAL, _THEM, _FOOT), _sf_hp(2, +4)]
    t[30] = [_sf_hp(2, -18)]                      # a sentinel hit, negative int32
    cells.append(("F cross-path identity", "4 heals <-> +16 HP, and one -18",
                  _sf_replay(_W, _H, _CORES, t), 0,
                  [("their_core_heals", 4), ("ecore_pos", 16), ("ecore_neg", 18)]))
    return cells


def selftest() -> int:
    import tempfile, os
    ok = True
    for name, why, blob, team, checks in _cells():
        fd, p = tempfile.mkstemp(suffix=".replay26")
        os.write(fd, blob)
        os.close(fd)
        got = decode(Path(p), team)
        os.unlink(p)
        if got is None:
            print(f"  FAIL {name}: decode returned None")
            ok = False
            continue
        for key, forced in checks:
            mark = "ok  " if got[key] == forced else "FAIL"
            if got[key] != forced:
                ok = False
            print(f"  {mark} {name:24} {key:18} forced={forced:<5} got={got[key]}")
        print(f"       ^ forced because: {why}")
    # the identity, stated as a check rather than assumed
    print("\n  IDENTITY CELL F: 4 heals x 4 HP = 16 == ecore_pos. If this cell ever")
    print("  passes while cell B fails, the decoder is reading HP deltas and")
    print("  calling them heal events.")
    print(f"\nHEAL_READ_SELFTEST: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _meta(mid: str):
    d = json.load(open(ARCHIVE / f"{mid}.meta.json"))
    if d.get("teamAName") == "OpenSverige":
        return d["teamBName"], 0, d.get("teamAVersion"), d.get("teamBVersion")
    if d.get("teamBName") == "OpenSverige":
        return d["teamAName"], 1, d.get("teamBVersion"), d.get("teamAVersion")
    return None


ARMS = {
    "CTRL_W1": "scratchpad/arm_loki19_ctrl_w1.txt",
    "CTRL_W2": "scratchpad/arm_unrated_v104_20260811T052031Z.txt",
    "TREAT_W1": "scratchpad/arm_loki19_treat_w1.txt",
    "TREAT_W2": "scratchpad/arm_unrated_v108_20260811T053112Z.txt",
}


def leg_ids():
    out = {}
    for arm, p in ARMS.items():
        for line in open(ROOT / p):
            i = line.find('"matchId": "')
            if i >= 0:
                out[line[i + 12:].split('"')[0]] = arm
    return out


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if "--leg" in sys.argv:
        rows = []
        for mid, arm in leg_ids().items():
            m = _meta(mid)
            if m is None:
                continue
            opp, us, ourv, theirv = m
            for g in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
                d = decode(g, us)
                if d is None:
                    continue
                d.update(arm=arm, opp=opp, ourv=ourv, theirv=theirv, file=g.name)
                rows.append(d)
        json.dump(rows, open(ROOT / "scratchpad/heal_leg.json", "w"))
        print(f"wrote {len(rows)} game rows -> scratchpad/heal_leg.json")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
