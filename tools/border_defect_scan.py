#!/usr/bin/env python3
"""border_defect_scan.py -- which teams look like they have the OFF-MAP QUERY defect?

THE TARGET-SELECTION QUESTION, asked by Magnus s32: if we fire a border-throw
crash leg at live teams, WHICH teams? Aiming at a team that guards its neighbour
queries buys nothing, and we cannot read their source.

THE PROXY, and its logic. The defect is: a builder queries an off-map neighbour
tile, `get_tile_*` raises, the raise escapes `run()`, and the engine PERMANENTLY
destroys that unit. A team that HAS the defect will therefore already be losing
builders, with NO damage event, DISPROPORTIONATELY NEAR THE MAP BORDER -- in
ordinary play, without anyone throwing them. That is a signature we can read off
the wire for every team in the league.

⛔ WHY "CRASHES AT ALL" IS THE WRONG SCREEN, and this is the whole point of the
file. `docs/research/CRASH-INDUCTION-league-wide-2026-08-11.md` measured crashes
suffered per game and found r(rating, crashes) = -0.029 over 67 teams -- a team
can crash constantly for reasons that have nothing to do with map borders
(timeouts, bad indices, division by zero). **We do not want teams that crash. We
want teams that crash AT THE EDGE.** The discriminator is the BORDER SHARE of a
team's no-damage removals, benchmarked against where their builders actually
stand -- because a team whose builders live at the edge will die at the edge
without any defect at all.

⇒ REPORTED PER TEAM:
   nodmg/game        -- no-damage builder removals per game (the old, blunt screen)
   border_share      -- of those, the fraction on a border tile
   exposure          -- fraction of ALL that team's builder-rounds spent on a
                        border tile. THE BASELINE. Without it, border_share is
                        a statement about their pathing, not their error handling.
   LIFT              -- border_share / exposure. **This is the number to aim on.**
                        Lift ~1.0 = they die at the edge exactly as often as they
                        stand there ⇒ no evidence of the defect.
                        Lift >> 1.0 = standing at the edge is disproportionately
                        fatal for them ⇒ candidate.

⛔ WHAT THIS IS NOT. It is an ASSOCIATION on observational data, and a high lift
has at least three innocent explanations: border tiles are where fighting happens;
launchers throw bots to borders already; and a cornered bot is a dead bot. **It
selects a TARGET LIST to test, it does not establish the defect in anyone.** The
test is QUEUE #17 (local, both-ways) and then a live leg.

Read-only. Reads replays directly; writes nothing but its report.
"""
from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

REPO = HERE.parent
ARCHIVE = REPO / "replay_archive"
META = REPO / "corpus" / "meta_join.tsv"


def team_names() -> dict[str, tuple[str, str]]:
    """file -> (team0_name, team1_name). A=0, B=1."""
    out: dict[str, tuple[str, str]] = {}
    if not META.exists():
        return out
    with META.open() as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            a, b = (r.get("teamAName") or "").strip(), (r.get("teamBName") or "").strip()
            if a and b:
                out[r["file"]] = (a, b)
    return out


def scan(path: Path):
    """-> (per-team stats dict, ok). Never raises on shape."""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None, False
    w = h = None
    for num, _wr, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
    if not w or not h:
        return None, False

    def on_border(p) -> bool:
        return p[0] == 0 or p[1] == 0 or p[0] == w - 1 or p[1] == h - 1

    pos: dict[int, tuple[int, int]] = {}
    team: dict[int, int] = {}
    kind: dict[int, str] = {}
    damaged: set[int] = set()
    removed: set[int] = set()
    st = {0: defaultdict(int), 1: defaultdict(int)}

    for _rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, _rnd)
                        if e is None:
                            continue
                        if e.id not in team:
                            team[e.id], kind[e.id] = e.team, e.kind
                        pos[e.id] = e.pos
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        pos[eid] = to
                elif unum == 5:
                    for n2, _w2b, v2 in fields(ubuf):
                        if n2 == 1:
                            damaged.add(v2)
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1 or rv in removed:
                            continue
                        removed.add(rv)
                        t, k, p = team.get(rv), kind.get(rv), pos.get(rv)
                        if t is None or k != "builder_bot" or p is None:
                            continue
                        if rv in damaged:
                            st[t]["dmg_deaths"] += 1
                        else:
                            st[t]["nodmg"] += 1
                            if on_border(p):
                                st[t]["nodmg_border"] += 1
        # EXPOSURE: builder-rounds spent standing on a border tile. This is the
        # baseline that turns border_share into evidence rather than pathing.
        for eid, p in pos.items():
            if kind.get(eid) == "builder_bot" and eid not in removed:
                t = team.get(eid)
                if t is None:
                    continue
                st[t]["brounds"] += 1
                if on_border(p):
                    st[t]["brounds_border"] += 1
    return st, True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--min-games", type=int, default=25)
    args = ap.parse_args(argv)

    names = team_names()
    if not names:
        print("no meta_join team names", file=sys.stderr)
        return 2
    files = [p for p in ARCHIVE.glob("*.replay26") if p.name in names]
    random.Random(args.seed).shuffle(files)
    if args.limit:
        files = files[: args.limit]
    print(f"scanning {len(files)} replays (seed {args.seed})")

    agg: dict[str, defaultdict] = defaultdict(lambda: defaultdict(int))
    bad = 0
    for i, p in enumerate(files, 1):
        st, ok = scan(p)
        if not ok:
            bad += 1
            continue
        n0, n1 = names[p.name]
        for idx, nm in ((0, n0), (1, n1)):
            for k, v in st[idx].items():
                agg[nm][k] += v
            agg[nm]["games"] += 1
        if i % 100 == 0:
            print(f"  ...{i}/{len(files)}", end="\r", file=sys.stderr)

    rows = []
    for nm, s in agg.items():
        if s["games"] < args.min_games or s["nodmg"] < 5 or not s["brounds"]:
            continue
        share = s["nodmg_border"] / s["nodmg"]
        expo = s["brounds_border"] / s["brounds"]
        rows.append((share / expo if expo else 0.0, nm, s["games"], s["nodmg"],
                     s["nodmg"] / s["games"], share, expo))
    rows.sort(reverse=True)

    print(f"\nunreadable: {bad}   teams reported: {len(rows)}"
          f"   (>= {args.min_games} games and >= 5 no-damage builder removals)\n")
    print(f"{'LIFT':>6} {'team':<26} {'games':>6} {'nodmg':>6} {'/game':>7} "
          f"{'border%':>8} {'exposure':>9}")
    print("-" * 76)
    for lift, nm, g, nd, per, share, expo in rows[:25]:
        print(f"{lift:>6.2f} {nm[:26]:<26} {g:>6} {nd:>6} {per:>7.3f} "
              f"{share:>7.1%} {expo:>8.1%}")
    print("\n⇒ LIFT is border_share / exposure. ~1.0 means they die at the edge exactly")
    print("  as often as they stand there — NO evidence of the defect. >>1.0 is a")
    print("  CANDIDATE, not a finding.")
    print("⛔ Observational association. Border tiles are also where fighting happens,")
    print("  where launchers already throw bots, and where a cornered bot dies anyway.")
    print("  This selects a TARGET LIST. QUEUE #17 (local, both ways) is the test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
