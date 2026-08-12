#!/usr/bin/env python3
"""LOKI-16 MECHANISM read: enemy-spawn-ring occupancy, from archived replays.

READ-ONLY. Downloads nothing. Consumes replay_archive/<matchId>_game_<N>.replay26
plus <matchId>.meta.json (for the seat, which is NEVER assumed).

RING DEFINITION -- the same 12 tiles the bot itself derives
(bots/_v133loki16/eco.py: heal_seats + core_corners, clipped to map bounds):
a Core's `position` is the NW corner of its 2x2 footprint {(x,y),(x+1,y),
(x,y+1),(x+1,y+1)}; the ring is the 8 orthogonal neighbours of that footprint
plus the 4 diagonal corners.

OCCUPANCY = END-OF-ROUND SNAPSHOT. A body counts for round r if it is standing
on a ring tile after every update in turns[r] has been applied. That is
"standing, not placed-then-lost" by construction.

Usage: python3 scratchpad/ring_read.py scratchpad/arm_loki16.txt [more.txt ...]
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

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"   # OpenSverige
ARCHIVE = ROOT / "replay_archive"


def ids_from_file(p: Path) -> list[str]:
    out = []
    for line in p.read_text().splitlines():
        if '"matchId"' in line:
            out.append(json.loads(line[line.index("{"):])["matchId"])
    return out


def ring_tiles(anchor, w, h):
    x, y = anchor
    seats = [(x, y - 1), (x + 1, y - 1), (x + 2, y), (x + 2, y + 1),
             (x + 1, y + 2), (x, y + 2), (x - 1, y + 1), (x - 1, y)]
    corners = [(x - 1, y - 1), (x + 2, y - 1), (x - 1, y + 2), (x + 2, y + 2)]
    return frozenset(t for t in seats + corners
                     if 0 <= t[0] < w and 0 <= t[1] < h)


def decode(path: Path, our_team: int):
    """-> dict of per-game ring metrics, or None if unparseable."""
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
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(2, 0), read_pos(d[3])))
    enemy = [pos for team, pos in cores if team != our_team]
    if len(enemy) != 1:
        return None
    ring = ring_tiles(enemy[0], w, h)

    pos_of, team_of, kind_of = {}, {}, {}
    # per-round series
    n_bodies = []                 # our builder bots standing on enemy ring
    per_bot_tile = defaultdict(list)   # (botid, tile) -> [rounds]
    per_bot_any = defaultdict(list)    # botid -> [rounds on any ring tile]
    bld_tiles_per_round = []      # our BUILDINGS on distinct enemy ring tiles

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:            # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                elif unum == 2:          # moveBuilderBot
                    bid, to = None, None
                    for mn, mw_, mv in fields(ubuf):
                        if mn == 1:
                            bid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if bid is not None and to is not None:
                        pos_of[bid] = to
                elif unum == 3:          # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            pos_of.pop(rv, None)
        # --- end-of-round snapshot ---
        c = 0
        btiles = set()
        for eid, p in pos_of.items():
            if team_of.get(eid) != our_team or p not in ring:
                continue
            if kind_of.get(eid) == "builder_bot":
                c += 1
                per_bot_tile[(eid, p)].append(rnd)
                per_bot_any[eid].append(rnd)
            elif kind_of.get(eid) not in (None, "core"):
                btiles.add(p)
        n_bodies.append(c)
        bld_tiles_per_round.append(len(btiles))

    def episodes(series_map):
        out = []
        for _k, rounds in series_map.items():
            run = 1
            for a, b in zip(rounds, rounds[1:]):
                if b == a + 1:
                    run += 1
                else:
                    out.append(run)
                    run = 1
            out.append(run)
        return out

    rounds = len(turn_bufs)
    occupied = [r for r, c in enumerate(n_bodies) if c > 0]
    return {
        "rounds": rounds,
        "winner": winner,
        "ring_size": len(ring),
        "seat_rounds": sum(n_bodies),
        "cover_rounds": len(occupied),
        "coverage": len(occupied) / rounds if rounds else 0.0,
        "first_arrival": occupied[0] if occupied else None,
        "cov_lt250": (len([r for r in occupied if r < 250]) / min(250, rounds)
                      if rounds else 0.0),
        "simul_hist": Counter(n_bodies),
        "max_simul": max(n_bodies) if n_bodies else 0,
        "tile_episodes": episodes(per_bot_tile),
        "bot_episodes": episodes(per_bot_any),
        "bld_ring_tiles_mean": (sum(bld_tiles_per_round) / rounds) if rounds else 0.0,
        "bld_ring_tiles_end": bld_tiles_per_round[-1] if bld_tiles_per_round else 0,
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
        # VALIDATION: replay-side winner tally must reproduce the platform's
        # scoreA. If seat mapping (replay Team 0 == platform teamA) were wrong
        # this is where it breaks.
        seat_check.append((mid, wins_a, meta["scoreA"], n, meta["scoreB"]))
    return games, per_opp, seat_check


def pct(xs):
    xs = sorted(xs)
    if not xs:
        return "n/a"
    q = lambda f: xs[min(len(xs) - 1, int(f * len(xs)))]
    return (f"n={len(xs)} min={xs[0]} p25={q(.25)} med={statistics.median(xs):.0f} "
            f"p75={q(.75)} p90={q(.90)} max={xs[-1]} mean={statistics.mean(xs):.1f}")


def report(label, games, per_opp, seat_check):
    print(f"\n{'='*78}\n=== {label}  (n={len(games)} games, "
          f"{len(seat_check)} matches) ===\n{'='*78}")
    bad = [s for s in seat_check if s[1] != s[2] or s[3] != 5]
    print(f"  SEAT/PARSE VALIDATION: replay winner tally == platform scoreA in "
          f"{len(seat_check)-len(bad)}/{len(seat_check)} matches"
          + ("" if not bad else f"  ** MISMATCH: {bad}"))
    vers = Counter((g["ourver"], g["opp"], g["oppver"], g["seat"]) for g in games)
    print("  our_ver / opponent / opp_ver / seat  -> games")
    for k, v in sorted(vers.items()):
        print(f"    v{k[0]:<4} {k[1]:<22} oppv{k[2]:<4} seat {k[3]}  {v}")

    occ = [g for g in games if g["first_arrival"] is not None]
    print(f"\n  -- TREATMENT OCCURRENCE (measured BEFORE retention) --")
    print(f"    games with >=1 of our bodies STANDING on an enemy ring tile "
          f"at end of any round: {len(occ)}/{len(games)} = {len(occ)/len(games):.1%}")
    fa = [g["first_arrival"] for g in occ]
    print(f"    first-arrival round: {pct(fa)}")
    gl = [g["rounds"] for g in games]
    print(f"    game length (rounds): {pct(gl)}")

    print(f"\n  -- RETENTION --")
    cov = [g["coverage"] for g in games]
    print(f"    ring-body COVERAGE (fraction of game rounds with >=1 body): "
          f"mean {statistics.mean(cov):.3f}  median {statistics.median(cov):.3f}"
          f"  min {min(cov):.3f} max {max(cov):.3f}")
    cov250 = [g["cov_lt250"] for g in games]
    print(f"    coverage restricted to rounds <250: mean "
          f"{statistics.mean(cov250):.3f}  median {statistics.median(cov250):.3f}")
    sr = [g["seat_rounds"] for g in games]
    print(f"    SEAT-ROUNDS per game (sum over rounds of bodies on ring): {pct(sr)}")
    te = [e for g in games for e in g["tile_episodes"]]
    print(f"    per-(bot,tile) HOLD EPISODES, consecutive rounds: {pct(te)}")
    be = [e for g in games for e in g["bot_episodes"]]
    print(f"    per-bot ring episodes (any ring tile), consec rounds: {pct(be)}")
    longest = [max(g["tile_episodes"]) if g["tile_episodes"] else 0 for g in games]
    print(f"    LONGEST single-tile hold per game: {pct(longest)}")
    lfrac = [(max(g["tile_episodes"]) / g["rounds"]) if g["tile_episodes"] else 0.0
             for g in games]
    print(f"    longest single-tile hold / game length: mean "
          f"{statistics.mean(lfrac):.3f} median {statistics.median(lfrac):.3f}")

    print(f"\n  -- SIMULTANEITY (prereg spec is ONE body) --")
    hist = Counter()
    tot = 0
    for g in games:
        hist += g["simul_hist"]
        tot += g["rounds"]
    for k in sorted(hist):
        print(f"    {k} bodies on ring: {hist[k]:>7} rounds = {hist[k]/tot:6.2%}")
    occ_rounds = tot - hist[0]
    if occ_rounds:
        mean_when_occ = sum(k * v for k, v in hist.items()) / occ_rounds
        print(f"    mean bodies GIVEN >=1 present: {mean_when_occ:.2f}")
    ms = [g["max_simul"] for g in games]
    print(f"    max simultaneous bodies per game: {pct(ms)}")

    print(f"\n  -- COST SIDE (prereg: body-for-barrier trade) --")
    bt = [g["bld_ring_tiles_end"] for g in games]
    print(f"    distinct enemy-ring tiles holding OUR building at game end: {pct(bt)}")
    btm = [g["bld_ring_tiles_mean"] for g in games]
    print(f"    ...time-averaged over the game: mean {statistics.mean(btm):.2f}")

    print(f"\n  -- PER OPPONENT --")
    print(f"    {'opponent':<24}{'n':>4}{'occ':>7}{'cover':>8}{'seatR':>8}"
          f"{'medEp':>7}{'maxSim':>8}")
    for opp in sorted(per_opp):
        gs = per_opp[opp]
        o = len([g for g in gs if g["first_arrival"] is not None])
        c = statistics.mean(g["coverage"] for g in gs)
        s = statistics.median(g["seat_rounds"] for g in gs)
        eps = [e for g in gs for e in g["tile_episodes"]]
        m = statistics.median(eps) if eps else 0
        sim = statistics.mean(g["max_simul"] for g in gs)
        print(f"    {opp:<24}{len(gs):>4}{o/len(gs):>7.0%}{c:>8.3f}{s:>8.0f}"
              f"{m:>7.0f}{sim:>8.2f}")
    return {"cov": statistics.mean(cov), "cov250": statistics.mean(cov250)}


if __name__ == "__main__":
    res = {}
    for f in sys.argv[1:]:
        fp = Path(f)
        games, per_opp, sc = run_arm(fp)
        res[fp.name] = report(fp.name, games, per_opp, sc)
    if len(res) == 2:
        (na, a), (nb, b) = res.items()
        print(f"\n{'='*78}\n=== MECHANISM DELTA {na} minus {nb} ===")
        print(f"  ring-body coverage      {a['cov']:.3f} - {b['cov']:.3f} = "
              f"{a['cov']-b['cov']:+.3f}   [prereg MECHANISM BAR: >= +0.08]")
        print(f"  coverage rounds <250    {a['cov250']:.3f} - {b['cov250']:.3f} = "
              f"{a['cov250']-b['cov250']:+.3f}")
