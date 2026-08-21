#!/usr/bin/env python3
"""v541 INSTRUMENT #4 -- THE PAIRED READ, and the NOISE CONTROL that licenses it.

⛔⛔ THE REASON THIS FILE EXISTS IS A MEASURED INSTRUMENT FAILURE, NOT A STATS
PREFERENCE.  The first three v541 battery cells were run with the arms' shipped
`NOISE_ON = True`.  `main.py:1190` seeds a per-body `spawn_salt` from
`random.Random()` -- a FRESH generator with no seed -- so a real fcode game is
NOT reproducible.  Measured on the CONTROL, the frozen parent arm run twice
against the same opponent on the same maps, seeds, seat and host:

    vs _v488beltbreak2   run1 timely-kill 105/180 = 58.3%  median kill 179
                         run2             86/180 = 47.8%  median kill 202
                         SAME BOT ->      10.5pp and 23 rounds apart
    vs _x3r0v173mjolnir  run1              47/180 = 26.1%  median kill 261
                         run2              53/180 = 29.4%  median kill 273
    row-level:           177/180 and 176/180 rows differ (parent vs itself)

**EVERY EFFECT THIS BUILD WAS ABOUT TO CLAIM SAT INSIDE THAT SWING.**
`tools/remote_battery.py`'s own docstring already recorded the fact -- "Control:
NOISE_ON, same host, repeat run -> 11/12 and 12/12 rows differ" -- and the
determinism it certifies (0/12) is for NOISE_OFF arms only.  The error was
assuming the stub harness's NOISE_OFF poke reached the battery.  IT DOES NOT:
that poke is an in-process `setattr`, and the battery ships trees to fcode.

⇒ **A PAIRED BATTERY IN THIS REPO IS ONLY PAIRED IF EVERY TREE IN IT -- BOTH
ARMS *AND* THE OPPONENT -- HAS `NOISE_ON = False` ON DISK.**  With that done,
(map, seed, seat) is a genuine matched pair and the tests below are the right
ones.  Without it, the cell is two independent samples with a same-bot
half-width larger than any effect worth shipping.

WHAT IT COMPUTES, on the matched pairs:
  * NOISE CONTROL      -- rows on which the two tapes differ at all.  For an
                          A-vs-A pair this MUST be 0 or the cell is void; the
                          script refuses to print a verdict when it is not.
  * McNEMAR on TIMELY-KILL (core-kill win by r300, the PROGRAMME primary,
    ITT over ALL games).  The paired test, because the unpaired one throws
    away the pairing the fixture was built to create.
  * KILL-ROUND SHIFT   -- median, and the paired sign test over cells where
    both arms killed, which is the shape LOKI-SALT was refuted on.

    .venv/bin/python scratchpad/s52_v541_build/paired.py --selftest
    .venv/bin/python scratchpad/s52_v541_build/paired.py TREAT.tsv CONTROL.tsv
"""
from __future__ import annotations

import argparse
import math
import sys
import tempfile
from pathlib import Path

HDR = ("tag map seed seat ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()


def read(path):
    rows = {}
    for line in Path(path).read_text().splitlines():
        f = line.rstrip("\n").split("\t")
        if not f or f[0] == "tag" or len(f) < len(HDR):
            continue
        r = dict(zip(HDR, f))
        rows[r["tag"]] = r
    return rows


def timely(r):
    """The PROGRAMME primary, ITT: a core-kill win by r300, over ALL games."""
    return r["ours"] == "US" and r["cond"].startswith("Core destroyed") \
        and int(r["turn"]) <= 300


def killround(r):
    if r["ours"] == "US" and r["cond"].startswith("Core destroyed"):
        return int(r["turn"])
    return None


def by_cell(a_path, b_path):
    """⛔⛔ THE (map, seat) BREAKDOWN, AND IT IS NOT A NICETY -- IT IS THE ONLY
    HONEST DENOMINATOR THIS FIXTURE HAS.

    MEASURED on this build's own beltbreak2 cell: the treatment changed 18 of
    180 rows, and **ALL 18 ARE `midgard_*_B`** -- one map, one seat, 18 seeds.
    Worse, the seeds do not vary the result: parent r270, finisher r268,
    unconditional-redirect loss at r289, IDENTICALLY, seed after seed.

    ⇒ **WITHIN THE (map, seat) STRATUM THE INTRA-CLUSTER CORRELATION IS ~1, SO
    THE EFFECTIVE n FOR THAT EFFECT IS 1 CELL, NOT 18 GAMES.**  A McNemar or
    sign test over those 18 rows returns p = 0.0000 and that number is an
    artefact of counting one observation eighteen times.  CLAUDE.md's design-
    effect PROCEDURE says to enumerate the clusters and ask whether the stratum
    can hold more than one member; here it holds eighteen and they are copies.

    **SO THE GAME-LEVEL p-VALUES IN `render()` MUST NOT BE QUOTED WITHOUT THIS
    TABLE BESIDE THEM**, and the report quotes the CELL COUNT as the effect
    size.  This function is what makes that possible; it is not optional
    colour.
    """
    A, B = read(a_path), read(b_path)
    keys = sorted(set(A) & set(B))
    cols = ("ours", "cond", "turn", "ours_mined", "opp_mined")
    cells = {}
    for k in keys:
        key = (A[k]["map"], A[k]["seat"])
        d = cells.setdefault(key, {"n": 0, "diff": 0, "a_t": 0, "b_t": 0,
                                   "faster": 0, "slower": 0, "turns": set()})
        d["n"] += 1
        if any(A[k][c] != B[k][c] for c in cols):
            d["diff"] += 1
        d["a_t"] += 1 if timely(A[k]) else 0
        d["b_t"] += 1 if timely(B[k]) else 0
        ka, kb = killround(A[k]), killround(B[k])
        if ka is not None and kb is not None:
            if ka < kb:
                d["faster"] += 1
            elif ka > kb:
                d["slower"] += 1
            d["turns"].add((ka, kb))
    return cells


def render_cells(cells):
    live = {k: v for k, v in cells.items() if v["diff"]}
    print(f"  ── BY (map, seat) -- the stratum the effect actually lives in")
    print(f"     cells with ANY differing row: {len(live)} of {len(cells)}")
    for (m, s), v in sorted(cells.items()):
        if not v["diff"]:
            continue
        uniq = sorted(v["turns"])[:3]
        print(f"     {m:14s} seat {s}  rows {v['diff']:2d}/{v['n']:2d}  "
              f"timely A {v['a_t']:2d} B {v['b_t']:2d}  "
              f"faster {v['faster']:2d} slower {v['slower']:2d}  "
              f"kill(A,B) {uniq}")
    if live:
        print("     ⚠ EFFECTIVE n FOR THIS EFFECT = "
              f"{len(live)} (map,seat) CELL(S), not "
              f"{sum(v['diff'] for v in live.values())} games -- the rows "
              "inside a cell are near-copies (see by_cell's docstring).")
    return live


def _binom_two_sided(k, n):
    """Exact two-sided binomial p at q=0.5 -- no scipy in this venv."""
    if n == 0:
        return 1.0
    tot = 2.0 ** n
    def pmf(i):
        return math.comb(n, i) / tot
    obs = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs + 1e-15))


def analyse(a_path, b_path):
    A, B = read(a_path), read(b_path)
    keys = sorted(set(A) & set(B))
    out = {"n": len(keys), "unjoined": len(set(A) ^ set(B))}

    # noise control: any differing row at all
    cols = ("ours", "cond", "turn", "ours_mined", "opp_mined")
    out["rows_differ"] = sum(
        1 for k in keys if any(A[k][c] != B[k][c] for c in cols))

    # McNemar on the timely-kill primary
    b_only = sum(1 for k in keys if timely(A[k]) and not timely(B[k]))
    c_only = sum(1 for k in keys if timely(B[k]) and not timely(A[k]))
    out["a_timely"] = sum(1 for k in keys if timely(A[k]))
    out["b_timely"] = sum(1 for k in keys if timely(B[k]))
    out["disc_a"], out["disc_b"] = b_only, c_only
    out["mcnemar_p"] = _binom_two_sided(min(b_only, c_only), b_only + c_only)

    # kill round
    ka = sorted(v for v in (killround(A[k]) for k in keys) if v is not None)
    kb = sorted(v for v in (killround(B[k]) for k in keys) if v is not None)
    out["med_a"] = ka[len(ka) // 2] if ka else -1
    out["med_b"] = kb[len(kb) // 2] if kb else -1
    both = [(killround(A[k]), killround(B[k])) for k in keys
            if killround(A[k]) is not None and killround(B[k]) is not None]
    slower = sum(1 for x, y in both if x > y)
    faster = sum(1 for x, y in both if x < y)
    out["both_killed"] = len(both)
    out["slower"], out["faster"] = slower, faster
    out["sign_p"] = _binom_two_sided(min(slower, faster), slower + faster)
    return out


def render(na, nb, o):
    print(f"PAIRED READ   A={na}   B={nb}   matched cells n={o['n']}")
    if o["unjoined"]:
        print(f"  ⚠ {o['unjoined']} unmatched tags — not counted either way")
    print(f"  NOISE CONTROL        rows differing at all: "
          f"{o['rows_differ']}/{o['n']}")
    print("  ── PROGRAMME PRIMARY: timely kill (core-kill win by r300, "
          "ITT over ALL games)")
    pa = 100.0 * o["a_timely"] / max(1, o["n"])
    pb = 100.0 * o["b_timely"] / max(1, o["n"])
    print(f"     A {o['a_timely']:3d}/{o['n']} = {pa:5.1f}%     "
          f"B {o['b_timely']:3d}/{o['n']} = {pb:5.1f}%     "
          f"delta {pa - pb:+5.1f}pp")
    print(f"     McNemar  A-only={o['disc_a']}  B-only={o['disc_b']}  "
          f"p={o['mcnemar_p']:.4f}")
    print("  ── KILL CLOCK")
    print(f"     median kill round   A {o['med_a']}   B {o['med_b']}   "
          f"delta {o['med_a'] - o['med_b']:+d}")
    print(f"     paired sign test over the {o['both_killed']} cells both "
          f"killed:  A slower {o['slower']}  A faster {o['faster']}  "
          f"p={o['sign_p']:.4f}")
    return o


# ---------------------------------------------------------------------------
# SELFTEST -- every reported quantity driven to BOTH verdicts
# ---------------------------------------------------------------------------

def _tape(rows):
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
    fh.write("\t".join(HDR) + "\n")
    for r in rows:
        fh.write("\t".join(str(r[c]) for c in HDR) + "\n")
    fh.close()
    return fh.name


def _row(tag, ours="US", cond="Core destroyed", turn=150):
    return dict(tag=tag, map="atoll", seed=1, seat="A", ours=ours,
                winner="w", cond=cond, turn=turn, tracebacks=0,
                ours_mined=1, opp_mined=1)


def selftest():
    fails = []

    def chk(cond, msg):
        print(("  ok    " if cond else "  FAIL  ") + msg)
        if not cond:
            fails.append(msg)

    print("[1] IDENTICAL TAPES: zero noise, zero delta, p=1")
    base = [_row(f"t{i}") for i in range(10)]
    a = _tape(base)
    o = analyse(a, _tape(list(base)))
    chk(o["rows_differ"] == 0 and o["a_timely"] == o["b_timely"] == 10
        and o["mcnemar_p"] == 1.0 and o["sign_p"] == 1.0,
        f"differ={o['rows_differ']} timely={o['a_timely']}/{o['b_timely']} "
        f"mcnemar={o['mcnemar_p']} sign={o['sign_p']}")

    print("[2] THE OTHER VERDICT: A strictly better on the primary")
    b = [_row(f"t{i}", ours="OPP") for i in range(10)]
    o = analyse(a, _tape(b))
    chk(o["a_timely"] == 10 and o["b_timely"] == 0 and o["disc_a"] == 10
        and o["mcnemar_p"] < 0.01,
        f"A-only={o['disc_a']} B-only={o['disc_b']} p={o['mcnemar_p']:.5f} "
        "(expect 10 / 0 / <0.01)")

    print("[3] AND THE OTHER DIRECTION: A strictly WORSE")
    o = analyse(_tape(b), a)
    chk(o["disc_a"] == 0 and o["disc_b"] == 10 and o["mcnemar_p"] < 0.01,
        f"A-only={o['disc_a']} B-only={o['disc_b']} p={o['mcnemar_p']:.5f}")

    print("[4] r300 IS THE BOUNDARY, AND IT IS TESTED ON BOTH SIDES")
    o = analyse(_tape([_row("t0", turn=300)]), _tape([_row("t0", turn=301)]))
    chk(o["a_timely"] == 1 and o["b_timely"] == 0,
        "r300 counts as timely, r301 does not")

    print("[5] A WIN THAT IS NOT A CORE KILL IS NOT A TIMELY KILL")
    o = analyse(_tape([_row("t0", cond="Titanium collected (tiebreak)",
                            turn=1000)]), _tape([_row("t0")]))
    chk(o["a_timely"] == 0 and o["b_timely"] == 1,
        "a r1000 tiebreak win scores 0 on the primary (R1000_IS_DEFEAT)")

    print("[6] KILL-CLOCK SIGN TEST, both directions")
    slow = [_row(f"t{i}", turn=400) for i in range(9)]
    o = analyse(_tape(slow), a)
    chk(o["slower"] == 9 and o["faster"] == 0 and o["sign_p"] < 0.01,
        f"A uniformly slower: slower={o['slower']} faster={o['faster']} "
        f"p={o['sign_p']:.5f}")
    o = analyse(a, _tape(slow))
    chk(o["faster"] == 9 and o["slower"] == 0,
        f"A uniformly faster (the other verdict): faster={o['faster']}")

    print("[7] THE NOISE CONTROL ITSELF FIRES")
    o = analyse(a, _tape([_row(f"t{i}", turn=151) for i in range(10)]))
    chk(o["rows_differ"] == 10,
        f"ten changed rows are all seen: {o['rows_differ']}/10")

    print("[8] THE (map, seat) BREAKDOWN, DRIVEN BOTH WAYS")
    def _r(tag, m, seat, **kw):
        r = _row(tag, **kw); r["map"] = m; r["seat"] = seat; return r
    same = [_r(f"{m}_s{i}_{st}", m, st)
            for m in ("atoll", "midgard") for st in ("A", "B")
            for i in range(5)]
    c = by_cell(_tape(same), _tape(list(same)))
    chk(len(c) == 4 and all(v["diff"] == 0 for v in c.values()),
        f"identical tapes: {len(c)} cells, none differing")
    mut = [dict(r) for r in same]
    for r in mut:
        if r["map"] == "midgard" and r["seat"] == "B":
            r["turn"] = 999
    c = by_cell(_tape(same), _tape(mut))
    live = [k for k, v in c.items() if v["diff"]]
    chk(live == [("midgard", "B")] and c[("midgard", "B")]["diff"] == 5,
        f"an effect confined to ONE cell is reported as one cell: {live} "
        f"(the other verdict) -- 5 rows, 1 cell, which is the whole point")

    print("[9] UNMATCHED TAGS ARE REPORTED, NOT SILENTLY DROPPED")
    o = analyse(a, _tape(base[:6]))
    chk(o["n"] == 6 and o["unjoined"] == 4,
        f"n={o['n']} unjoined={o['unjoined']} (expect 6 / 4)")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}")
        for f in fails:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED -- primary, kill clock and noise control each "
          "driven to both verdicts")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    x = ap.parse_args()
    if x.selftest:
        return selftest()
    if not (x.a and x.b):
        ap.error("give two tapes, or --selftest")
    render(Path(x.a).stem, Path(x.b).stem, analyse(x.a, x.b))
    render_cells(by_cell(x.a, x.b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
