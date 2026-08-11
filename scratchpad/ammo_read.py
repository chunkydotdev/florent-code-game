#!/usr/bin/env python3
"""AMMO POLICY, LEAGUE-WIDE — is converting titanium to ammunition an axis of
play, or a settled question?

Commissioned by the builder arm (s30) as the OPPONENT-SIDE half of their ammo
hypothesis. Their half (our own fire rate / idle-gap histogram) is running
separately; this half asks whether the teams climbing fastest convert MORE
titanium into ammunition, and EARLIER.

`CoreConvertAmmo{team=1, amount=2}` (update field 14) CARRIES THE TEAM, so this
needs no seat inference from throw geometry -- the join failure that returned
"0 of 185,695" on the builder's first EXILE run cannot occur here. The only
mapping required is replay team index -> A/B, verified separately on 2,335
joined rows (1,175 (0,a) + 1,160 (1,b), zero cross cells).

Population: every archived match with a platform meta.json sidecar, INCLUDING
12,425 third-party games across 72 teams -- so this is a league-wide read, not
an us-only one.

  --selftest   forced-answer cells
  --run        walk the archive -> scratchpad/ammo_league.json
"""
from __future__ import annotations
import json, sys, glob
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402
from ring_read import _sf_v, _sf_l, _sf_replay, _sf_blank_turns      # noqa: E402

ARCHIVE = ROOT / "replay_archive"
U_PLACE, U_FIRE, U_AMMO = 1, 12, 14


def decode(path: Path) -> dict | None:
    data = path.read_bytes()
    turn_bufs = []
    map_buf = None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    conv = defaultdict(int)            # team -> total titanium converted
    nconv = defaultdict(int)           # team -> number of convert calls
    first = {}                         # team -> first conversion round
    turrets = defaultdict(int)         # team -> gunners+sentinels placed
    shots = defaultdict(int)           # team -> FireTurret events attributed
    pos_team: dict[tuple[int, int], int] = {}
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == U_AMMO:
                    d = {n: v for n, _, v in fields(ubuf)}
                    t, amt = d.get(1, 0), d.get(2, 0)
                    conv[t] += amt
                    nconv[t] += 1
                    first.setdefault(t, rnd)
                elif unum == U_PLACE:
                    for en, _ew, ebuf in fields(ubuf):
                        if en == 1:
                            e = parse_entity(ebuf, rnd)
                            if e is not None and e.kind in ("gunner", "sentinel"):
                                turrets[e.team] += 1
                                pos_team[e.pos] = e.team
                elif unum == U_FIRE:
                    frm = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                    if frm is not None and frm in pos_team:
                        shots[pos_team[frm]] += 1
    return dict(rounds=len(turn_bufs),
                conv={str(k): v for k, v in conv.items()},
                nconv={str(k): v for k, v in nconv.items()},
                first={str(k): v for k, v in first.items()},
                turrets={str(k): v for k, v in turrets.items()},
                shots={str(k): v for k, v in shots.items()})


def _sf_ammo(team: int, amount: int) -> bytes:
    return _sf_l(U_AMMO, _sf_v(1, team) + _sf_v(2, amount))


def selftest() -> int:
    import tempfile, os
    cores = [(1, 0, (1, 1)), (2, 1, (8, 8))]
    ok = True
    cases = []
    # A. no conversions at all -> empty, not zero-filled
    t = _sf_blank_turns()
    cases.append(("A none", "no coreConvertAmmo events exist", t,
                  [("conv", {}), ("first", {})]))
    # B. team 0 converts 10 at r3 and 25 at r40; team 1 converts 5 at r7.
    t = _sf_blank_turns()
    t[3] = [_sf_ammo(0, 10)]
    t[7] = [_sf_ammo(1, 5)]
    t[40] = [_sf_ammo(0, 25)]
    cases.append(("B totals and timing", "10+25 for team 0 first at r3; 5 for team 1 at r7",
                  t, [("conv", {"0": 35, "1": 5}), ("first", {"0": 3, "1": 7}),
                      ("nconv", {"0": 2, "1": 1})]))
    # C. the team field is load-bearing: same amounts, teams swapped
    t = _sf_blank_turns()
    t[3] = [_sf_ammo(1, 10)]
    t[40] = [_sf_ammo(1, 25)]
    cases.append(("C team field", "identical amounts booked to team 1 instead",
                  t, [("conv", {"1": 35}), ("first", {"1": 3})]))
    for name, why, turns, checks in cases:
        fd, p = tempfile.mkstemp(suffix=".replay26")
        os.write(fd, _sf_replay(12, 12, cores, turns))
        os.close(fd)
        got = decode(Path(p))
        os.unlink(p)
        for key, forced in checks:
            good = got[key] == forced
            ok &= good
            print(f"  {'ok  ' if good else 'FAIL'} {name:22} {key:8} forced={forced} got={got[key]}")
        print(f"       ^ forced because: {why}")
    print(f"\nAMMO_READ_SELFTEST: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if "--run" not in sys.argv:
        print(__doc__)
        return 0
    out = []
    metas = glob.glob(str(ARCHIVE / "*.meta.json"))
    for i, p in enumerate(metas):
        try:
            d = json.load(open(p))
        except Exception:
            continue
        a, b = d.get("teamAName"), d.get("teamBName")
        if not a or not b:
            continue
        for g in sorted(ARCHIVE.glob(f"{d['id']}_game_*.replay26")):
            r = decode(g)
            if r is None:
                continue
            r.update(match=d["id"], A=a, B=b, avA=d.get("teamAVersion"),
                     avB=d.get("teamBVersion"), created=d.get("createdAt"),
                     rA=d.get("ratingABefore"), rB=d.get("ratingBBefore"))
            out.append(r)
        if i % 500 == 0:
            print(f"  {i}/{len(metas)} matches, {len(out)} games", file=sys.stderr)
    json.dump(out, open(ROOT / "scratchpad/ammo_league.json", "w"))
    print(f"wrote {len(out)} game rows -> scratchpad/ammo_league.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
