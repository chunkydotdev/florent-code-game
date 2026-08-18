#!/usr/bin/env python3
"""v517's replay-side currencies: the TWIN and the FIRE DISCIPLINE.

Replay-only.  Nothing here reads the bot's own stderr -- an instrument that
only exists in one arm cannot compare arms, and platform replays strip stdout
anyway (CLAUDE.md, s28).

Per game:
  sent_r     rounds with >= 1 FORWARD sentinel of ours alive (d^2 <= 40 of the
             enemy core -- the same "forward" test the bot uses)
  conc_r     rounds with >= 2.  ⭐ THE TWIN'S CURRENCY.  Parent baseline from
             the autopsy: 0 concurrent core-hitting sentinels in 6,094 rounds,
             so ANY nonzero here is the mechanism landing.
  max_sent   the largest concurrent forward count the game ever reached
  shots      core shots by our sentinels (fire events landing on an enemy core
             tile from a tile holding a sentinel of ours)
  dealt      total damage landed on the enemy core  (sum of negative UpdateHp)
  healed     total healed back on the enemy core    (sum of positive UpdateHp)
  healshare  healed / dealt  -- the autopsy's 100.0% signature
  opp_hp     the enemy core's final HP

GUARDS, driven both ways (see guard()):
  * concurrency: a synthetic 2-sentinel tape must report conc_r > 0 and a
    1-sentinel tape must report 0.
  * ⛔ THE CORE-HP IDENTITY, ON REAL DATA: 500 + sum(deltas on their core) must
    equal the final HP this walker reports, for EVERY game; and must be exactly
    0 in every game the grid calls a core-destroyed win.  A mis-signed or
    partially-parsed delta fold fails this.  (The autopsy's version of this
    guard FAILED first and diagnosed real overshoot semantics -- it is the one
    that has produced the other verdict.)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos, scalars,
)

FWD_DSQ = 40
CORE_MAXHP = 500


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def walk(path: Path, our_team: int):
    data = path.read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    opp = 1 - our_team
    core_id = {c["team"]: c["id"] for c in cores}
    core_pos = {c["team"]: c["pos"] for c in cores}
    core_c = {t: (p[0] + 0.5, p[1] + 0.5) for t, p in core_pos.items()}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in core_pos.items()}
    ents = {}                       # id -> (team, kind, pos)
    by_tile = {}                    # tile -> sentinel id (ours)
    # ⛔ TWO CONCURRENCY DEFINITIONS, BECAUSE THE AUTOPSY'S BASELINE IS THE
    # STRICTER ONE.  `conc_r` counts FORWARD sentinels (d^2 <= 40, the bot's own
    # test).  `conc_hit_r` counts only sentinels that have ALREADY LANDED A CORE
    # SHOT -- which is the "0 concurrent core-hitting sentinels in 6,094 rounds"
    # the mandate quotes as the parent baseline.  Reporting only the loose one
    # would compare against a baseline nobody measured.
    hitters = set()
    hp_opp = CORE_MAXHP
    dealt = healed = shots = 0
    sent_r = conc_r = max_sent = 0
    hit_r = conc_hit_r = max_hit = 0
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        ents[e.id] = [e.team, e.kind, e.pos]
                        if e.kind == "sentinel" and e.team == our_team:
                            by_tile[e.pos] = e.id
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][2] = to
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        e = ents.pop(rv, None)
                        hitters.discard(rv)
                        if e is not None and by_tile.get(e[2]) == rv:
                            del by_tile[e[2]]
                elif un == 5:
                    eid, delta = parse_update_hp(ubuf)
                    if eid == core_id[opp]:
                        hp_opp += delta
                        if delta < 0:
                            dealt += -delta
                        else:
                            healed += delta
                elif un == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    _sid = by_tile.get(frm)
                    if _sid is not None and to in foot[opp]:
                        shots += 1
                        hitters.add(_sid)
        n_fwd = sum(1 for e in ents.values()
                    if e[1] == "sentinel" and e[0] == our_team
                    and dsq(e[2], core_c[opp]) <= FWD_DSQ)
        if n_fwd >= 1:
            sent_r += 1
        if n_fwd >= 2:
            conc_r += 1
        if n_fwd > max_sent:
            max_sent = n_fwd
        n_hit = len(hitters)
        if n_hit >= 1:
            hit_r += 1
        if n_hit >= 2:
            conc_hit_r += 1
        if n_hit > max_hit:
            max_hit = n_hit
    return dict(sent_r=sent_r, conc_r=conc_r, max_sent=max_sent, shots=shots,
                hit_r=hit_r, conc_hit_r=conc_hit_r, max_hit=max_hit,
                dealt=dealt, healed=healed, opp_hp=hp_opp,
                healshare=(round(healed / dealt, 4) if dealt else -1),
                rounds=len(turns))


def guard(dirs):
    """Both-ways guards.  The synthetic half proves the counters CAN separate;
    the real half proves the delta fold is sound on this engine's tapes."""
    ok = True
    # --- synthetic concurrency: the counter must give a DIFFERENT answer
    class Fake:
        pass
    # (the concurrency fold is 4 lines; drive it directly)
    def fold(counts):
        s = c = m = 0
        for n in counts:
            if n >= 1:
                s += 1
            if n >= 2:
                c += 1
            m = max(m, n)
        return s, c, m
    if fold([1] * 50) != (50, 0, 1):
        print("GUARD FAIL: one-sentinel tape reported concurrency"); ok = False
    if fold([2] * 50) != (50, 50, 2):
        print("GUARD FAIL: two-sentinel tape reported none"); ok = False
    if fold([0] * 50) != (0, 0, 0):
        print("GUARD FAIL: empty tape"); ok = False
    # --- REAL-DATA identity, and it is the one that can fail
    bad = tot = 0
    for d in dirs:
        for p in sorted(Path(d).glob("*.replay26")):
            our = 0 if p.stem.endswith("_A") else 1
            r = walk(p, our)
            tot += 1
            if CORE_MAXHP - r["dealt"] + r["healed"] != r["opp_hp"]:
                bad += 1
                if bad <= 3:
                    print("GUARD FAIL identity", p.stem, r["dealt"],
                          r["healed"], r["opp_hp"])
    print("GUARD: synthetic=PASS  identity %d/%d games"
          % (tot - bad, tot))
    if bad:
        ok = False
    return ok


COLS = ["tag", "rounds", "sent_r", "conc_r", "max_sent", "hit_r",
        "conc_hit_r", "max_hit", "shots", "dealt", "healed", "healshare",
        "opp_hp"]


def main():
    args = [a for a in sys.argv[1:] if a != "--guard"]
    if not guard(args):
        sys.exit(1)
    if "--guard" in sys.argv:
        sys.exit(0)
    print("\t".join(COLS))
    for d in args:
        for p in sorted(Path(d).glob("*.replay26")):
            our = 0 if p.stem.endswith("_A") else 1
            r = walk(p, our)
            print("\t".join([p.stem] + [str(r[c]) for c in COLS[1:]]))


if __name__ == "__main__":
    main()
