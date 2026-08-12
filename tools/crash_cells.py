#!/usr/bin/env python3
"""QUEUE #17 — DOES THE CRASH WEAPON ACTUALLY FIRE?  A LOCAL, BOTH-WAYS DRIVE.

THE QUESTION.  Our launcher throws a kidnapped ENEMY builder to a legal
MAP-BORDER tile, where THAT BOT'S OWN CODE queries a neighbour of its own
position, that neighbour is off-map, `get_tile_env` raises, the raise escapes
`run()`, and the engine permanently destroys the unit for the match (CLAUDE.md;
`docs/research/engine-source-crash-and-launcher-2026-08-10.md`).  314 kidnaps
were delivered in the LOKI-14 leg and NOBODY HAS EVER SEEN WHETHER THE CRASH
LANDED, because the platform strips stdout in 30,664 of 30,664 `BotOutput`
events.  Locally the engine prints the victim's traceback, which no live leg
can see.

⛔⛔ READ THIS BEFORE TRUSTING v1 OF THIS FILE, WHICH PUBLISHED A FALSE NEGATIVE.
v1 counted throws from OUR OWN `print()` ledger (`LOKI14 KIDNAP arm=…`).  That
ledger read **0 throws in all three cells**, so v1 stamped two cells UNDOSED and
then its summary printed **"THE WEAPON DOES NOT FIRE … the road closes"** — on a
run in which the weapon had fired 15 times.  TWO SEPARATE DEFECTS, and the
second is the dangerous one:
  1. **The dose was read off our own stdout instead of engine-side facts** —
     the exact mistake CLAUDE.md records against the LOKI-14 prereg ("Read arms
     from ENGINE-SIDE facts, never from our own stdout").  The throws were real;
     they simply did not travel through `_kidnap_done`.  Ground truth, seed 7102
     on antler (14x18): unit 14 sat at **(8,4)** at r=14 and at **(13,1)** at
     r=15 — a five-tile jump no builder can make, onto **x = w-1, a border
     tile** — and it raised and died there.
  2. **UNDOSED was allowed to fall through to "does not fire".**  A cell that
     never delivered the dose answers NOTHING; printing a road-closing verdict
     off it is strictly worse than printing nothing.
Both are fixed here: the dose is now measured from the VICTIM'S OWN position
trace, and UNDOSED is a terminal state that cannot reach a verdict.

HOW THE DOSE IS MEASURED NOW.  Each probe prints `pos=(x,y)` for itself every
round.  Between consecutive rounds a builder may move at most ONE cardinal step,
so any Chebyshev jump >= 2 is a LAUNCH — an engine-side fact about where the
unit actually is, independent of anything we claim to have done.  The
destination is then classified BORDER vs INTERIOR against the map's real
dimensions, parsed from the map header (not assumed to be 26x26 — `antler` is
14x18 and `meander` is 25x15, and the "map26" suffix is a filename, not a size).

THE CELLS.  Two of the three are forced-zero controls:

  (a) border arm ON  vs `_probe_border_raw`    -> MUST crash        (positive)
  (b) border arm ON  vs `_probe_border_guard`  -> MUST read ZERO    (the guard)
  (c) border arm OFF vs `_probe_border_raw`    -> the throw control

(b) isolates the unguarded query: if the guarded probe dies under the same
throws, the query is not what killed it.
⚠ (c) IS NOT A CLEAN ZERO AND MUST NOT BE READ AS ONE.  Measured: the arm-OFF
build ALSO lands builders on border tiles, because the incumbent exile ordering
already sorts destinations by **maximum distance from our own core**, and the
farthest reachable tiles are disproportionately edge tiles.  **Border throws are
not a LOKI-14 invention; we get them incidentally.**  So (c) answers the PLANK
question ("does the border ARM deliver MORE border throws than the incumbent
ordering?") and it is the BORDER-vs-INTERIOR contrast WITHIN a cell that answers
the MECHANISM question ("does landing on a border tile kill an unguarded bot?").

⛔ THE VICTIM PROBE HAD TO BE BUILT; #17's NOMINEE CANNOT SERVE.  #17 names
`bots/_probe_oov_raw`, which queries a FIXED far corner `Position(w-1, h-1)` —
in bounds, and identical wherever the unit stands.  POSITION-INVARIANT, so cells
(a) and (c) return the same answer by construction.  `_probe_border_*` query a
neighbour of SELF, which is the real field shape.  And the first draft of that
probe walked to the border unaided and died with no throw involved (seed 7001,
(20,0) on turn ~131) — both probes now refuse to step onto a border tile, so
every border arrival is a throw.

USAGE
    .venv/bin/python tools/crash_cells.py --games 24 --jobs 4
    .venv/bin/python tools/crash_cells.py --selftest
"""
from __future__ import annotations

import argparse
import concurrent.futures
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"

MAPS = ["hive.map26", "antler.map26", "atoll.map26", "meander.map26"]

CELLS = [
    # name,         ours,                  theirs,                     role
    ("A_ON_RAW",   "bots/_v131loki14",    "bots/_probe_border_raw",   "POSITIVE"),
    ("B_ON_GUARD", "bots/_v131loki14",    "bots/_probe_border_guard", "FORCED_ZERO"),
    ("C_OFF_RAW",  "bots/_v131loki14off", "bots/_probe_border_raw",   "ARM_CONTROL"),
]

RE_POS = re.compile(r"^B(?:RAW|GRD) r=(\d+) unit=(\d+) pos=\((\d+),(\d+)\)", re.M)


def map_dims(path: Path) -> tuple[int, int]:
    """Real (width, height) from the map header.

    ⛔ NOT inferred from the `.map26` suffix, which is a filename and not a
    size: antler is 14x18 and meander is 25x15.  Getting this wrong makes every
    border classification wrong in the direction of under-counting, which is
    the direction that manufactures a false negative.
    """
    b = path.read_bytes()
    if len(b) < 4 or b[0] != 0x08:
        raise ValueError(f"{path.name}: unexpected map header {b[:6]!r}")
    i = 1
    w = 0
    shift = 0
    while True:                       # varint
        w |= (b[i] & 0x7F) << shift
        if not b[i] & 0x80:
            i += 1
            break
        i += 1
        shift += 7
    if b[i] != 0x10:
        raise ValueError(f"{path.name}: unexpected height tag {b[i]:#x}")
    i += 1
    h = 0
    shift = 0
    while True:
        h |= (b[i] & 0x7F) << shift
        if not b[i] & 0x80:
            break
        i += 1
        shift += 7
    return w, h


def _crash_count(stderr: str, victim_dir: str) -> int:
    """Tracebacks raised INSIDE the victim's own main.py.

    Matched on the victim's file path AND `GameError`, so an exception from our
    tree, or a non-GameError, cannot be scored as a crash we caused.
    """
    needle = victim_dir.split("/")[-1] + "/main.py"
    n = 0
    for b in stderr.split("Traceback (most recent call last):")[1:]:
        head = b[:600]
        if needle in head and "GameError" in head:
            n += 1
    return n


def throws(blob: str, w: int, h: int) -> tuple[int, int]:
    """(border_throws, interior_throws), measured ENGINE-SIDE.

    A builder moves at most one cardinal step per round, so a Chebyshev jump of
    >= 2 between consecutive sightings of the same unit id is a LAUNCH.  Nothing
    here reads our own bookkeeping.
    """
    last: dict[int, tuple[int, int, int]] = {}
    border = interior = 0
    for rnd, uid, x, y in RE_POS.findall(blob):
        rnd, uid, x, y = int(rnd), int(uid), int(x), int(y)
        prev = last.get(uid)
        if prev is not None:
            pr, px, py = prev
            if max(abs(x - px), abs(y - py)) >= 2:
                if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                    border += 1
                else:
                    interior += 1
        last[uid] = (rnd, x, y)
    return border, interior


def run_game(cell, ours, theirs, mp, seed, tle):
    mpath = ROOT / "maps" / mp
    w, h = map_dims(mpath)
    cmd = [str(FCODE), "run", ours, theirs, str(mpath),
           "--seed", str(seed), "--tle", str(tle), "--replay", "/dev/null"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=ROOT)
    except subprocess.TimeoutExpired:
        return {"cell": cell, "map": mp, "seed": seed, "timeout": True}
    blob = (p.stdout or "") + (p.stderr or "")
    tb, ti = throws(blob, w, h)
    return {"cell": cell, "map": mp, "seed": seed, "timeout": False,
            "crashes": _crash_count(blob, theirs),
            "thr_border": tb, "thr_interior": ti}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=24, help="games PER CELL")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--tle", type=int, default=10)
    ap.add_argument("--seed0", type=int, default=7100)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    jobs = [(c, o, t, MAPS[i % len(MAPS)], a.seed0 + i, a.tle)
            for c, o, t, _r in CELLS for i in range(a.games)]
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run_game, *j) for j in jobs]
        for k, f in enumerate(concurrent.futures.as_completed(futs), 1):
            out.append(f.result())
            if k % 10 == 0:
                print(f"  ... {k}/{len(jobs)}", file=sys.stderr, flush=True)

    print("=" * 78)
    print("QUEUE #17 — CRASH CELLS.  Dose read ENGINE-SIDE from the victim's own")
    print("position trace, never from our stdout.  See the v1 defect in the docstring.")
    print("=" * 78)
    agg = {}
    for cell, ours, theirs, role in CELLS:
        rows = [r for r in out if r["cell"] == cell and not r["timeout"]]
        tmo = sum(1 for r in out if r["cell"] == cell and r["timeout"])
        tb = sum(r["thr_border"] for r in rows)
        ti = sum(r["thr_interior"] for r in rows)
        cr = sum(r["crashes"] for r in rows)
        cg = sum(1 for r in rows if r["crashes"] > 0)
        agg[cell] = dict(n=len(rows), tb=tb, ti=ti, cr=cr, cg=cg, role=role)
        print(f"\n{cell}  [{role}]   {ours}  vs  {theirs}")
        print(f"   games {len(rows)}" + (f"   TIMEOUTS {tmo}" if tmo else ""))
        print(f"   THROWS (engine-side)  border={tb}  interior={ti}")
        print(f"   CRASHES {cr} across {cg}/{len(rows)} games")
        if tb + ti == 0:
            print("   VERDICT: UNDOSED — no throw landed. This cell answers NOTHING.")
            print("            (It is NOT evidence the weapon is silent.)")
        elif tb == 0:
            print("   VERDICT: NO BORDER DOSE — throws landed, none on a border tile.")
        else:
            print(f"   VERDICT: DOSED — {tb} border arrivals, "
                  f"{cr/tb:.2f} crashes per border throw")

    print("\n" + "-" * 78)
    A, B, C = agg["A_ON_RAW"], agg["B_ON_GUARD"], agg["C_OFF_RAW"]
    if A["tb"] == 0:
        print("MECHANISM: UNRESOLVED — the positive cell never delivered a border")
        print("           throw. Nothing may be concluded about the weapon.")
    elif A["cr"] == 0:
        print("MECHANISM: REFUTED — border throws landed and the unguarded probe")
        print("           did NOT crash. The road closes.")
    elif B["cr"] > 0:
        print("MECHANISM: UNATTRIBUTABLE — the GUARDED probe crashed too, so the")
        print("           unguarded query is not what kills. Do not publish cell (a).")
    else:
        print("MECHANISM: CONFIRMED — border throws kill the UNGUARDED probe and")
        print("           leave the GUARDED one untouched under the same throws.")
    print()
    print(f"PLANK (does the border ARM add border throws over the incumbent?):")
    print(f"   arm ON  border/interior = {A['tb']}/{A['ti']}   arm OFF = {C['tb']}/{C['ti']}")
    if C["tb"] > 0:
        print("   ⚠ THE ARM-OFF BUILD ALSO LANDS BORDER THROWS — the incumbent exile")
        print("     ordering (farthest tile from our core) already produces them.")
        print("     The border arm's value is the DIFFERENCE, not the whole count.")
    print()
    print("⚠ SCOPE: this says nothing about what SHARE of the real field is")
    print("  vulnerable. We patched this in eco.py; most teams have not, and")
    print("  'most' is unmeasured. That needs the live leg.")
    return 0


def selftest() -> int:
    """Drive every predicate to BOTH answers. A check that has only produced one
    verdict has not been seen to check."""
    bad = 0

    def chk(name, got, want):
        nonlocal bad
        ok = got == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name:52s} got={got} want={want}")

    victim = "bots/_probe_border_raw"
    real = ('Traceback (most recent call last):\n  File "/x/bots/_probe_border_raw'
            '/main.py", line 54, in run\nfcode._types.GameError: Position out of bounds\n')
    ours = ('Traceback (most recent call last):\n  File "/x/bots/_v131loki14/raid.py"'
            ', line 9, in run\nfcode._types.GameError: Position out of bounds\n')
    wrong = ('Traceback (most recent call last):\n  File "/x/bots/_probe_border_raw'
             '/main.py", line 54, in run\nZeroDivisionError: x\n')
    chk("crash: no traceback -> 0", _crash_count("", victim), 0)
    chk("crash: one victim GameError -> 1", _crash_count(real, victim), 1)
    chk("crash: two -> 2", _crash_count(real + real, victim), 2)
    chk("crash: OUR OWN traceback not scored -> 0", _crash_count(ours, victim), 0)
    chk("crash: victim but not GameError -> 0", _crash_count(wrong, victim), 0)

    # Throw detector, on a 14x18 map (antler's real size).
    W, H = 14, 18
    step = "BRAW r=1 unit=4 pos=(5,5) alive\nBRAW r=2 unit=4 pos=(5,6) alive\n"
    chk("throw: a legal 1-step move is NOT a throw", throws(step, W, H), (0, 0))
    real_jump = "BRAW r=14 unit=14 pos=(8,4) alive\nBRAW r=15 unit=14 pos=(13,1) alive\n"
    chk("throw: the REAL seed-7102 jump -> border", throws(real_jump, W, H), (1, 0))
    inner = "BRAW r=1 unit=9 pos=(3,3) alive\nBRAW r=2 unit=9 pos=(7,8) alive\n"
    chk("throw: jump to an INTERIOR tile", throws(inner, W, H), (0, 1))
    twobots = step + real_jump
    chk("throw: per-unit tracking, mixed", throws(twobots, W, H), (1, 0))
    edge0 = "BRAW r=1 unit=2 pos=(6,6) alive\nBRAW r=2 unit=2 pos=(6,0) alive\n"
    chk("throw: y=0 counts as border", throws(edge0, W, H), (1, 0))
    # The size trap: (13,1) is border on 14x18 and INTERIOR on 26x26. If this
    # cell ever reads (1,0) the header parser has been bypassed.
    chk("throw: same jump on 26x26 is INTERIOR (size trap)",
        throws(real_jump, 26, 26), (0, 1))
    chk("guard probe's BGRD lines parse too",
        throws("BGRD r=1 unit=4 pos=(2,2) alive\nBGRD r=2 unit=4 pos=(9,9) alive\n",
               W, H), (0, 1))

    # Real map headers.
    for name, want in (("antler", (14, 18)), ("hive", (25, 25)),
                       ("atoll", (18, 18)), ("meander", (25, 15))):
        chk(f"map_dims({name})", map_dims(ROOT / "maps" / f"{name}.map26"), want)

    print("\n" + ("PASS: crash counter returns 0 and >0 on forced inputs; throw "
                  "detector separates a legal step from a launch, border from "
                  "interior, and fails the 26x26 size trap."
                  if not bad else f"FAIL: {bad} case(s)"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
