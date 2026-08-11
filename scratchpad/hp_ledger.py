#!/usr/bin/env python3
"""VALIDITY CHECK on LOKI-19 bar 5b's pre-registered estimator.

5b says: "Enemy-core HP removed by builder melee, per game (2 dmg/swing)".
That estimator is SWINGS x 2. A 500 HP core cannot lose 2,066 HP, so wherever
swings x 2 exceeds 500 the estimator is provably not measuring net damage.

This walks the actual core HP ledger off the same replays:
  * cores are seeded at 500 (they are NEVER placed by an update)
  * UpdateHp{id, delta} on the enemy core id is summed, split into negative
    (damage from any source: our melee AND our turrets) and positive (their
    healing)
and reports it beside swings x 2, per game.

It cannot ATTRIBUTE damage to melee vs turret -- both land on the same core and
the wire carries no source. So it bounds the estimator rather than replacing it:
  swings x 2      = an upper bound on melee damage DEALT
  -sum(neg delta) = total damage from ALL our sources, net of nothing
  +sum(pos delta) = healing they bought
Read-only. Scratch instrument for one question; not a bar, not committed.
"""
from __future__ import annotations
import json, statistics, sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa
from ring_read import ids_from_file, ARCHIVE, OUR_TEAM_ID  # noqa
from peck_read import core_footprint  # noqa

CORE_HP = 500


def walk(path: Path, our_team: int):
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
    their = [c for c in cores if c[1] != our_team]
    if not their:
        return None
    ecid, _, epos = their[0]
    foot = core_footprint(epos)
    team_of = {}
    swings = 0
    neg = pos = 0
    died = False
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en == 1:
                            e = parse_entity(ebuf, rnd)
                            if e is not None:
                                team_of[e.id] = e.team
                elif unum == 13:
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if aid is not None and tgt is not None \
                       and team_of.get(aid) == our_team and tgt in foot:
                        swings += 1
                elif unum == 5:                      # updateHp{id, delta}
                    d = {n: v for n, _, v in fields(ubuf)}
                    if d.get(1) == ecid:
                        dl = d.get(2, 0)
                        # A protobuf `int32` holding a NEGATIVE value is
                        # sign-extended to 64 bits and written as a 10-byte
                        # varint -- so it arrives here as a huge unsigned int
                        # and the fold-back constant is 2**64, NOT 2**32.
                        # (First pass used 2**32 and produced "healing" of
                        # 4e21 HP/game, which is how the bug announced itself.)
                        if dl >= 2 ** 63:
                            dl -= 2 ** 64
                        if dl < 0:
                            neg += -dl
                        else:
                            pos += dl
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rv == ecid:
                            died = True
    return dict(swings=swings, est=swings * 2, dmg=neg, heal=pos, died=died,
                rounds=len(turn_bufs))


def main(armfile):
    rows = []
    for mid in ids_from_file(Path(armfile)):
        meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
        we_a = meta["teamAId"] == OUR_TEAM_ID
        ot = 0 if we_a else 1
        opp = meta["teamBName"] if we_a else meta["teamAName"]
        for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
            r = walk(rp, ot)
            if r:
                r["opp"] = opp
                rows.append(r)
    print(f"=== {Path(armfile).name}  n={len(rows)} games ===")
    est = [r["est"] for r in rows]
    dmg = [r["dmg"] for r in rows]
    heal = [r["heal"] for r in rows]
    over = [r for r in rows if r["est"] > CORE_HP]
    print(f"  5b ESTIMATOR swings x 2   mean {statistics.mean(est):8.1f}  "
          f"median {statistics.median(est):7.1f}  max {max(est)}")
    print(f"  ACTUAL enemy-core damage  mean {statistics.mean(dmg):8.1f}  "
          f"median {statistics.median(dmg):7.1f}  max {max(dmg)}   "
          f"(ALL our sources: melee + turrets, unattributable on the wire)")
    print(f"  enemy healing ON the core mean {statistics.mean(heal):8.1f}  "
          f"median {statistics.median(heal):7.1f}  max {max(heal)}")
    print(f"  games where swings x 2 EXCEEDS a full 500 HP core: "
          f"{len(over)}/{len(rows)} = {100*len(over)/len(rows):.0f}%  "
          f"-- in these the estimator is provably not net damage")
    print(f"  enemy core destroyed in {sum(1 for r in rows if r['died'])}/"
          f"{len(rows)} games")
    print(f"  ratio actual-damage / estimator, per game (median): "
          f"{statistics.median([r['dmg']/r['est'] for r in rows if r['est']>0] or [0]):.2f}")
    print(f"  {'opponent':<24}{'n':>4}{'swx2':>9}{'dmg':>9}{'heal':>9}"
          f"{'net':>9}{'kills':>7}")
    for opp in sorted({r["opp"] for r in rows}):
        s = [r for r in rows if r["opp"] == opp]
        e = statistics.mean(r["est"] for r in s)
        d = statistics.mean(r["dmg"] for r in s)
        h = statistics.mean(r["heal"] for r in s)
        print(f"  {opp:<24}{len(s):>4}{e:>9.1f}{d:>9.1f}{h:>9.1f}{d-h:>9.1f}"
              f"{sum(1 for r in s if r['died']):>4}/{len(s)}")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        main(f)
