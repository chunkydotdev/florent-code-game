#!/usr/bin/env python3
"""Treatment-occurrence census for LOKI-3 (the kidnap plank).

WHY THIS EXISTS, AND WHY IT RUNS BEFORE THE BATTERY, NOT AFTER.
LOKI-2 committed to an opening whose recipe called for three forward turrets
and delivered ONE. The battery still ran, still produced numbers, and the
numbers were about a treatment that had never occurred. `preflight.py` now
demands a `treatment_occurrence:` line for exactly that reason; this is the
tool that fills it in for this plank.

It answers two questions per replay, both about OUR side only:

  1. Did we build a FORWARD launcher at all -- a launcher inside
     LOKI_KIDNAP_CENSUS_DSQ (50) of an enemy Core tile? That is the placement
     half, and it is the half the field never does (0.64 launchers/game,
     none forward).
  2. Did a forward launcher actually THROW an enemy builder? That is the
     conversion half. A launcher that is built and never throws is a 20 Ti
     ornament that also raised our launcher cost scale by 10%.

Reuses the validated geometry of replay_throws.py rather than re-deriving it:
a throw is a >1-tile moveBuilderBot, and the thrower is a launcher within
d^2 <= 2 of the pre-throw tile. Ambiguity (two launchers, or launchers from
both teams in range) is reported, never silently resolved -- an ambiguous
throw is counted in its own column so it cannot inflate the headline.

Usage:  .venv/bin/python tools/corpus/loki3_treatment.py <replay_dir> [--us-team 0|1|auto]

`auto` (default) infers our team per replay as the team whose bot dirs we
control cannot be read from the replay -- so instead it reports BOTH teams'
numbers side by side and leaves attribution to the caller, who knows the seat.
"""
from __future__ import annotations

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY THIS FILE NEEDED IT (measured 2026-08-16, s47). `tools/corpus/` sat
# OUTSIDE the help-contract sweep, which globbed `tools/*.py` only. Probed:
# 11 of 18 corpus tools violated the contract, and three of the failures are
# the dangerous classes the sweep exists to catch —
#   * `unrated_games.py --help` REWROTE corpus/unrated_games.tsv (1.1 MB)
#   * `ladder_meta.py`, `league_maps.py`, `league_matches.py`, `meta_attrib.py`
#     --help went to the NETWORK and ran until killed at 20 s
#   * `replay_autopsy.py --help` raised TypeError out of replay_census.fields()
# and the rest printed verdict-shaped text in this repo's own vocabulary
# ("no *.replay26 under --help", "sides loaded: 0 (from 0 matches) — --help").
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by build_corpus /
# keeper. Ungated, this would fire during that import and make the PARENT exit 0
# mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: the guard must not depend on what the host file
# happens to import, or on the order its imports appear in.
# ⛔ MUST SIT AFTER `from __future__ import ...`, which the language requires to
# be the first statement after the docstring.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import sys
from pathlib import Path

sys.path.insert(0, "tools")
sys.path.insert(0, "tools/corpus")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

# NOTE (s25): the first cut of this file hand-rolled its own entity decode and
# got TWO things wrong -- it read the kind as an integer enum in field 3, and
# the position from field 4. Entity kind is actually encoded by WHICH FIELD
# NUMBER is present (replay_census.KIND_FIELDS) and position is field 3. The
# result was a clean, plausible table of all-zeroes that would have been read
# as "the plank never fires". It is now on `parse_entity`, the same validated
# path replay_throws.py uses. Do not re-hand-roll this.
FWD_DSQ = 50          # LOKI_KIDNAP_CENSUS_DSQ
PICKUP_DSQ = 2        # V5-verified launcher pickup range


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def census(path: Path):
    data = path.read_bytes()
    turn_bufs = []
    map_buf = None
    for num, wire, v in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = v
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(v)
    if not turn_bufs or map_buf is None:
        return None
    # CORES COME FROM THE MAP BUFFER, NOT FROM TURN UPDATES. The second cut of
    # this file harvested cores from placeEntity and found NONE -- cores exist
    # from map init and are never re-placed -- so `ec` was always None, every
    # launcher scored "not forward", and the tool reported a confident
    # 0/24 (0.0%) for a plank that was in fact building forward launchers from
    # round 5. That is the corpus_sanity lesson in miniature: an all-zero
    # result is either a fact or an instrument that never fired, and this one
    # never fired. It now RAISES rather than returning zeros.
    cores = {}
    for num, _w, v in fields(map_buf):
        if num != 4:
            continue
        team, pos = 0, None
        for cn, _cw, cv in fields(v):
            if cn == 2:
                team = cv
            elif cn == 3:
                pos = read_pos(cv)
        if pos is not None:
            cores[team] = pos
    if len(cores) != 2:
        raise SystemExit(
            f"{path.name}: found {len(cores)} cores in the map buffer, expected 2. "
            "REFUSING to report occurrence numbers computed against a missing core "
            "-- that is how a working plank gets reported as 0%.")
    ents = {}          # id -> dict(team, pos, kind)
    built_fwd = {0: 0, 1: 0}      # forward launchers built, by team
    built_all = {0: 0, 1: 0}      # all launchers built, by team
    throws_fwd = {0: 0, 1: 0}     # enemy-builder throws BY a forward launcher
    throws_any = {0: 0, 1: 0}     # enemy-builder throws by any launcher
    ambiguous = {0: 0, 1: 0}
    first_fwd = {0: None, 1: None}

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ubuf_outer in fields(turn_buf):
            for unum, _uw, ubuf in fields(ubuf_outer):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id]["pos"] = e.pos
                            continue
                        ents[e.id] = dict(team=e.team, pos=e.pos, kind=e.kind)
                        if e.kind == "launcher":
                            built_all[e.team] += 1
                            ec = cores.get(1 - e.team)
                            if ec is not None and e.pos is not None and d2(e.pos, ec) <= FWD_DSQ:
                                built_fwd[e.team] += 1
                                if first_fwd[e.team] is None:
                                    first_fwd[e.team] = rnd
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None or e["pos"] is None:
                        continue
                    frm = e["pos"]
                    e["pos"] = to
                    if abs(to[0] - frm[0]) + abs(to[1] - frm[1]) <= 1:
                        continue                                # a walk, not a throw
                    cand = [o for o in ents.values()
                            if o["kind"] == "launcher" and o["pos"] is not None
                            and d2(o["pos"], frm) <= PICKUP_DSQ]
                    teams = {o["team"] for o in cand}
                    if len(teams) != 1:
                        if cand:
                            ambiguous[e["team"]] += 1
                        continue
                    tteam = cand[0]["team"]
                    if tteam == e["team"]:
                        continue                                # ferrying its own
                    throws_any[tteam] += 1
                    ec = cores.get(1 - tteam)
                    if ec is not None and any(d2(o["pos"], ec) <= FWD_DSQ for o in cand):
                        throws_fwd[tteam] += 1
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        ents.pop(rv, None)
    return dict(file=path.name, rounds=len(turn_bufs),
                built_all=built_all, built_fwd=built_fwd,
                throws_any=throws_any, throws_fwd=throws_fwd,
                ambiguous=ambiguous, first_fwd=first_fwd)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    d = Path(argv[0])
    files = sorted(d.glob("*.replay26"))
    if not files:
        sys.exit(f"no *.replay26 under {d}")
    rows = [r for r in (census(f) for f in files) if r]
    print(f"replays: {len(rows)}\n")
    hdr = f"{'file':<44} {'rnds':>5} {'fwdL(0/1)':>10} {'allL(0/1)':>10} " \
          f"{'thrFwd(0/1)':>12} {'thrAny(0/1)':>12} {'amb':>5} {'1stFwd':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['file'][:44]:<44} {r['rounds']:>5} "
              f"{r['built_fwd'][0]:>4}/{r['built_fwd'][1]:<5} "
              f"{r['built_all'][0]:>4}/{r['built_all'][1]:<5} "
              f"{r['throws_fwd'][0]:>5}/{r['throws_fwd'][1]:<6} "
              f"{r['throws_any'][0]:>5}/{r['throws_any'][1]:<6} "
              f"{r['ambiguous'][0] + r['ambiguous'][1]:>5} "
              f"{str(r['first_fwd'][0]) + '/' + str(r['first_fwd'][1]):>8}")
    n = len(rows)
    # SEAT ATTRIBUTION. pair.py names replays <tag>_<map>_<seed>_<seat>, and the
    # seat IS the team: seat a == team 0, seat b == team 1. Pooling both teams
    # into one percentage (the first cut of this summary) mixes US with the
    # OPPONENT and is meaningless -- our 25% and their 25% are different facts.
    us = [(r, 0 if r["file"].rsplit("_", 1)[-1].startswith("a") else 1) for r in rows]
    unknown = [r for r, _ in us if r["file"].rsplit("_", 1)[-1][0] not in "ab"]
    if unknown:
        raise SystemExit(f"cannot infer seat for {len(unknown)} replays "
                         f"(e.g. {unknown[0]['file']}) -- refusing to guess.")
    g_fwd = sum(1 for r, t in us if r["built_fwd"][t] > 0)
    g_thr = sum(1 for r, t in us if r["throws_fwd"][t] > 0)
    g_any = sum(1 for r, t in us if r["built_all"][t] > 0)
    firsts = sorted(r["first_fwd"][t] for r, t in us if r["first_fwd"][t] is not None)
    print(f"\nUS (seat-attributed), n={n} games")
    print(f"  games with >=1 launcher of any kind:   {g_any}/{n} ({100.0*g_any/n:.1f}%)")
    print(f"  games with >=1 FORWARD launcher:       {g_fwd}/{n} ({100.0*g_fwd/n:.1f}%)"
          f"   [PREREG bar >=50%]  {'PASS' if 100.0*g_fwd/n >= 50 else 'FAIL'}")
    print(f"  games with >=1 forward-launcher THROW: {g_thr}/{n} ({100.0*g_thr/n:.1f}%)"
          f"   [PREREG bar >=30%]  {'PASS' if 100.0*g_thr/n >= 30 else 'FAIL'}")
    if firsts:
        print(f"  first forward launcher round: median {firsts[len(firsts)//2]}, "
              f"min {firsts[0]}, max {firsts[-1]}, n={len(firsts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
