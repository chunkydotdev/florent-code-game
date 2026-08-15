#!/usr/bin/env python3
"""Core-entry throughput, read straight off `DistributeResources`.

WHY. A cut reported "a NEW HARD ENGINE CEILING: 1 stack per core-entry tile per
round, 0/3,582 violations, max exactly 1.000" -- and in the same breath that
everyone runs those tiles at 25% utilisation. Those two facts fight: if the
tiles sit at a quarter of capacity the ceiling is almost never approached, so
zero violations is close to zero evidence that a ceiling exists. Absence of a
violation you never gave the engine a chance to commit is the same shape as a
stop-loss that cannot fire and a constant column that validates anything.

So this conditions on OPPORTUNITY instead of counting violations: it reads every
`ResourceMove` and asks how many landed on the SAME core footprint tile in the
SAME round.

RESULT (60 LOKI-8 arena games, 87,933 ResourceMoves, 13,706 into a core tile):

    1 entry  : 12,642 tile-rounds
    2 entries:    532 tile-rounds        <- the "ceiling" is not 1
    max observed: 2

**THE 1-PER-TILE-PER-ROUND CEILING IS REFUTED.** Two is common: 4.0% of
core-tile-rounds. Whether a HIGHER ceiling exists is UNRESOLVED here and this
tool cannot settle it, because our own supply may simply never present three
stacks to one tile in one round -- exactly the reasoning that makes the original
claim unsafe, applied to my own.

CONSEQUENCE, and it strengthens rather than weakens the cut it corrects: any
utilisation figure computed against a capacity of 1 is overstated by at least
2x. If entry tiles read 25% against capacity 1, they are at most 12.5% against
the measured 2 -- so "the binding constraint is INSIDE the network, not at core
entry" gets stronger, while "build more entry tiles" gets weaker.

NOTE this is the first decoder in the repo to read update field 4.
`replay_econ.py` loops over it and passes, which is why `econ.tsv:deliveries` is
all-zero and documented KNOWN-DEAD in `corpus_sanity.py`.

    .venv/bin/python tools/core_entry.py <replay-or-dir> [...]
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, WIRE_LEN      # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)


def _core_tiles(anchor):
    x, y = anchor
    return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


def analyse(path: Path):
    data = Path(path).read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    if mb is None:
        return None
    cores = {}
    for n, w, v in fields(mb):
        if n == 4 and w == WIRE_LEN:
            team, pos = 0, None
            for cn, cw, cv in fields(v):
                if cn == 2:
                    team = cv
                elif cn == 3 and cw == WIRE_LEN:
                    pos = read_pos(cv)
            if pos is not None:
                cores[team] = tuple(pos)
    if len(cores) < 2:
        return None
    tiles = {t: _core_tiles(a) for t, a in cores.items()}
    hist, moves, core_moves = collections.Counter(), 0, 0
    for tb in turns:
        dest = collections.Counter()
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un != 4:                       # DistributeResources
                    continue
                for mn, mw, mv in fields(uv):
                    if mn != 1 or mw != WIRE_LEN:  # ResourceMove
                        continue
                    to = None
                    for rn, rw, rv in fields(mv):
                        if rn == 2 and rw == WIRE_LEN:
                            to = read_pos(rv)
                    if to is None:
                        continue
                    moves += 1
                    tt = tuple(to)
                    for ts in tiles.values():
                        if tt in ts:
                            dest[tt] += 1
                            core_moves += 1
        for c in dest.values():
            hist[c] += 1
    return hist, moves, core_moves


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: core_entry.py <replay-or-dir> [...]", file=sys.stderr)
        return 2
    paths = []
    for a in args:
        p = Path(a)
        paths.extend(sorted(p.rglob("*.replay26")) if p.is_dir() else [p])
    tot, moves, core_moves, games = collections.Counter(), 0, 0, 0
    for p in paths:
        r = analyse(p)
        if r is None:
            continue
        h, m, c = r
        tot.update(h)
        moves += m
        core_moves += c
        games += 1
    print(f"games {games}  ResourceMoves {moves}  into a core tile {core_moves}")
    for k in sorted(tot):
        print(f"  {k} entries into one core tile in one round : {tot[k]:8d}")
    if tot:
        print(f"MAX observed: {max(tot)}   "
              f"({'ceiling of 1 REFUTED' if max(tot) > 1 else 'no violation seen'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
