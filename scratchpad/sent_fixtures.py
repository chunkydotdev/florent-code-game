#!/usr/bin/env python3
"""Forced-answer fixtures for sent_read.py, written as REAL engine protobuf.

Writer helpers (_sf_*) are the ones from tools/ring_read.py (reuse explicitly
sanctioned by the task), extended with _sf_fire for Update.fireTurret=12.

Every expected answer is forced BY CONSTRUCTION from the fixture geometry.
Gate on the printed SENT_FIXTURES: PASS token, never on $?.

DECLARED MUTANTS (acceptance criterion -- each must make this FAIL):
  1. facing-blind:  RAY[d] -> union of all 8 rays
        sed 's/^RAY = .*$/RAY = {d: tuple(set(sum((_ray(k) for k in DELTA), ()))) for d in DELTA}/'
  2. range-blind:   SENT_RSQ = 32 -> 10**9
        sed 's/^SENT_RSQ = 32$/SENT_RSQ = 10**9/'
"""
from __future__ import annotations

import os
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sent_read as S

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


def _sf_v(num, value):
    return _sf_varint(num << 3) + _sf_varint(value)


def _sf_l(num, payload):
    return _sf_varint(num << 3 | 2) + _sf_varint(len(payload)) + payload


def _sf_pos(xy):
    return _sf_v(1, xy[0]) + _sf_v(2, xy[1])


def _sf_entity(eid, team, xy, kind, hp=40, direction=None):
    body = (_sf_v(1, eid) + _sf_v(2, team) + _sf_l(3, _sf_pos(xy))
            + _sf_v(4, hp) + _sf_v(5, hp))
    if kind == "barrier":
        sub = b""
    elif direction is not None:
        sub = _sf_v(1, direction)
    else:
        sub = _sf_v(1, 0)
    return body + _sf_l(_SF_KIND_FIELD[kind], sub)


def _sf_place(entity):
    return _sf_l(1, _sf_l(1, entity))


def _sf_move(eid, xy):
    return _sf_l(2, _sf_v(1, eid) + _sf_l(2, _sf_pos(xy)))


def _sf_remove(eid):
    return _sf_l(3, _sf_v(1, eid))


def _sf_fire(frm, to):                      # Update{fireTurret=12{from=1,to=2}}
    return _sf_l(12, _sf_l(1, _sf_pos(frm)) + _sf_l(2, _sf_pos(to)))


def _sf_turn(updates):
    return b"".join(_sf_l(1, u) for u in updates)


def _sf_replay(w, h, cores, turns, winner=1, walls=()):
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


# ---------------------------------------------------------------- geometry ---
W = H = 24
N = 100
CORES = [(1, 0, (0, 0)), (2, 1, (22, 22))]     # both far from every ray below
SENT = (5, 5)
EAST, SE = 3, 4
# EAST ray from (5,5): (6,5)..(10,5)   [d^2 = 1..25;  (11,5) is d^2=36 -> OUT]
# SE   ray from (5,5): (6,6)..(9,9)    [d^2 = 2..32; (10,10) is d^2=50 -> OUT]
SENT_ID, ENEMY_ID = 100, 200


def blank(n=N):
    return [[] for _ in range(n)]


def cell(name, expected, turns, walls=(), extra_checks=None):
    return (name, expected, _sf_replay(W, H, CORES, turns, walls=walls),
            extra_checks)


def cells():
    C = []

    def sentinel(d=EAST, team=0, at=SENT):
        return _sf_place(_sf_entity(SENT_ID, team, at, "sentinel", direction=d))

    def enemy(at, team=1, kind="builder_bot", eid=ENEMY_ID):
        return _sf_place(_sf_entity(eid, team, at, kind))

    # 1. target present ON the ray, and it fires -> FIRED
    t = blank()
    t[0] = [sentinel(), enemy((8, 5))]
    t[10] = [_sf_fire(SENT, (8, 5))]
    C.append(cell("FIRED_with_target", ("us", "FIRED"), t,
                  extra_checks=lambda r: (r["shots"] == 1
                                          and r["first_shot"] - r["build"] == 10)))

    # 2. identical geometry, NO fire event -> HAD_TARGET_NEVER_FIRED,
    #    opportunity rounds forced = 100 (enemy stands there rounds 0..99)
    t = blank()
    t[0] = [sentinel(), enemy((8, 5))]
    C.append(cell("HAD_TARGET_never_fired", ("us", "HAD_TARGET_NEVER_FIRED"), t,
                  extra_checks=lambda r: r["opp_rounds"] == 100))

    # 3. enemy exists for 100 rounds but OFF the facing ray (due south of a
    #    sentinel facing EAST) -> NO_TARGET_EVER.  MUTANT 1 must flip this.
    t = blank()
    t[0] = [sentinel(), enemy((5, 8))]
    C.append(cell("NO_TARGET_offray", ("us", "NO_TARGET_EVER"), t,
                  extra_checks=lambda r: r["opp_rounds"] == 0))

    # 4. no enemy entity anywhere except the far enemy core -> NO_TARGET_EVER
    t = blank()
    t[0] = [sentinel()]
    C.append(cell("NO_TARGET_empty", ("us", "NO_TARGET_EVER"), t))

    # 5. built r0, removed r1 (lifespan 2 < 3) with a target in line -> DIED_YOUNG
    t = blank()
    t[0] = [sentinel(), enemy((8, 5))]
    t[1] = [_sf_remove(SENT_ID)]
    C.append(cell("DIED_YOUNG", ("us", "DIED_YOUNG"), t,
                  extra_checks=lambda r: r["end"] - r["build"] + 1 == 2))

    # 6. lifespan exactly 3 with a target -> NOT died-young; the boundary cell
    t = blank()
    t[0] = [sentinel(), enemy((8, 5))]
    t[2] = [_sf_remove(SENT_ID)]
    C.append(cell("LIFESPAN3_boundary", ("us", "HAD_TARGET_NEVER_FIRED"), t,
                  extra_checks=lambda r: r["end"] - r["build"] + 1 == 3))

    # 7. RANGE CEILING, cardinal: enemy at d^2=25 (in) vs d^2=36 (out).
    t = blank()
    t[0] = [sentinel(), enemy((10, 5))]
    C.append(cell("RANGE_in_d25", ("us", "HAD_TARGET_NEVER_FIRED"), t))
    t = blank()
    t[0] = [sentinel(), enemy((11, 5))]
    C.append(cell("RANGE_out_d36", ("us", "NO_TARGET_EVER"), t))

    # 8. RANGE CEILING, diagonal: d^2=32 (in) vs d^2=50 (out). MUTANT 2 flips.
    t = blank()
    t[0] = [sentinel(d=SE), enemy((9, 9))]
    C.append(cell("RANGE_diag_in_d32", ("us", "HAD_TARGET_NEVER_FIRED"), t))
    t = blank()
    t[0] = [sentinel(d=SE), enemy((10, 10))]
    C.append(cell("RANGE_diag_out_d50", ("us", "NO_TARGET_EVER"), t))

    # 9. IGNORES OBSTACLES: a WALL tile and a friendly barrier both sit between
    #    the sentinel and the enemy on the ray. Still a target.
    t = blank()
    t[0] = [sentinel(), enemy((10, 5)),
            _sf_place(_sf_entity(301, 0, (7, 5), "barrier"))]
    C.append(cell("IGNORES_OBSTACLES", ("us", "HAD_TARGET_NEVER_FIRED"), t,
                  walls=((6, 5),)))

    # 10. TEAM-BLINDNESS GUARD: a FRIENDLY unit standing in the ray is not a
    #     target -> NO_TARGET_EVER.
    t = blank()
    t[0] = [sentinel(), enemy((8, 5), team=0)]
    C.append(cell("FRIENDLY_in_line_is_not_target", ("us", "NO_TARGET_EVER"), t))

    # 11. OPPONENT COLUMN: identical to cell 2 but the sentinel is team 1 and
    #     the body in its line is team 0 -> must land in the opponent column.
    t = blank()
    t[0] = [_sf_place(_sf_entity(SENT_ID, 1, SENT, "sentinel", direction=EAST)),
            _sf_place(_sf_entity(ENEMY_ID, 0, (8, 5), "builder_bot"))]
    C.append(cell("OPPONENT_side", ("opp", "HAD_TARGET_NEVER_FIRED"), t))

    # 12. MOVING enemy: enters the ray only at round 50 -> opp_rounds == 50.
    t = blank()
    t[0] = [sentinel(), enemy((8, 12))]
    t[50] = [_sf_move(ENEMY_ID, (8, 5))]
    C.append(cell("MOVING_enemy_enters_ray", ("us", "HAD_TARGET_NEVER_FIRED"), t,
                  extra_checks=lambda r: r["opp_rounds"] == 50))

    # 13. ENEMY CORE FOOTPRINT is a target: sentinel at (20,22) facing EAST,
    #     ray (21,22)..(23,22) overlaps the 2x2 core at (22,22).
    t = blank()
    t[0] = [_sf_place(_sf_entity(SENT_ID, 0, (20, 22), "sentinel",
                                 direction=EAST))]
    C.append(cell("ENEMY_CORE_is_target", ("us", "HAD_TARGET_NEVER_FIRED"), t,
                  extra_checks=lambda r: r["opp_rounds"] == 100))
    return C


def run():
    ok = True
    tmp = tempfile.mkdtemp(prefix="sentfix_")
    for name, (side, want), blob, extra in cells():
        p = os.path.join(tmp, name + ".replay26")
        with open(p, "wb") as fh:
            fh.write(blob)
        st = S.analyse(p, None)
        recs = st["sent"]
        if len(recs) != 1:
            print(f"  FAIL {name}: expected 1 sentinel, decoded {len(recs)}")
            ok = False
            continue
        r = recs[0]
        got_side = "us" if r["team"] == 0 else "opp"
        got = S.bucket(r)
        good = (got_side == side and got == want)
        if extra is not None and good:
            good = bool(extra(r))
        print(f"  {'PASS' if good else 'FAIL'} {name:32s} want={side}/{want:22s}"
              f" got={got_side}/{got:22s} shots={r['shots']} "
              f"opp_rounds={r['opp_rounds']} life={r['end']-r['build']+1}")
        ok = ok and good
    print(f"SENT_FIXTURES: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
