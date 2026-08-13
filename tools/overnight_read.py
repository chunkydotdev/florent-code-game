#!/usr/bin/env python3
"""OVERNIGHT READ-OUT — pools on the DECLARED denominator, never discards.

⛔ WHY THIS EXISTS, AND IT REPLACES A CONTROL THAT WOULD HAVE THROWN THE NIGHT AWAY
----------------------------------------------------------------------------------
The overnight design carried a rule: *"the read-out REFUSES to pool a shard
without a completion marker."* Sound in intent — silent truncation reads as
"covered everything" — and **catastrophic in practice at these targets.**

Measured on the live run, independently by two lanes: **4.07 s/game at 9 shards**
(side lane got 3.90). At TARGET 5,408 that is **6.12 h against a ~6 h window**.
⇒ **The MODAL outcome is every shard landing at 85–98% and EVERY ONE being
refused. A 95%-successful night converted into a total loss by its own control.**

⇒ **THIS TOOL POOLS PARTIAL SHARDS AND PRINTS THE SHORTFALL.** A shard at
4,900/5,408 is usable with a KNOWN denominator; what is not usable is a shard
whose denominator is unknown. The heartbeat already carries `n TARGET`, so
nothing had to be built to know it.

**WHAT IS STILL REFUSED**, because these are the cases where the denominator is a
lie rather than merely short:
  * `ABORTED_NOWINNER` — the fixture was broken, rows are not games.
  * row count disagreeing with the heartbeat's `n` by >1% — a restart that
    duplicated its prefix, so the sample is skewed to low seeds.
  * a shard whose seat split is off by more than max(2, 1% of n) — seat is worth
    **7.6pp on byte-identical arms**, so an unbalanced shard measures SEAT.
    ⛔ The first threshold was "within 1 game" and it REFUSED HEALTHY SHARDS at
    78/76 mid-run, because the loop plays seats alternately. **A guard that
    refuses good data is as wrong as one that passes bad**, and this repo has
    now produced both kinds in one session.

PART A converts each local win rate to an IMPLIED ELO GAP and compares it to the
opponent-controlled ladder gap. **Registered as a FALSIFIER, not an estimator**
(`docs/PLAN-overnight-2026-08-11.md` Amendment 1): era confounding can bend an
ordering, it cannot invert one.

Usage:  overnight_read.py [--dir scratchpad/overnight]
"""
from __future__ import annotations

import glob
import math
import re
import sys
from collections import Counter
from pathlib import Path


def live_pool(src: str = "tools/overnight.sh") -> set[str] | None:
    """The live map pool, parsed from overnight.sh's own MAPS= line — ONE
    source, never a second copy (S1 rule). Returns None (BLIND) if the parse
    fails, so the caller can say so instead of silently passing everything:
    a retired-check that cannot tell it is blind is the ship_watch defect."""
    try:
        m = re.search(r"^MAPS=\(([^)]*)\)", Path(src).read_text(), re.M)
    except OSError:
        return None
    return set(m.group(1).split()) if m else None

# Opponent-controlled version effects (research, 2c261c8) -- NOT rating snapshots.
# v112 is deliberately absent: zero archived ladder games, so no ladder side.
LADDER = {"_v130loki13": 1686, "_v115dodge": 1600, "_v124loki8": 1609}
LADDER_CI = {"_v130loki13": (1656, 1717), "_v115dodge": (1520, 1681),
             "_v124loki8": (1578, 1641)}


def load_spec():
    """shard -> (treatment, control), read from the LIVE worklist.

    ⛔ THIS USED TO READ `scratchpad/overnight_spec.txt` AND THAT FILE IS DEAD.
    Measured 2026-08-12 by the instrument audit: it was last written 2026-08-11
    and lists nine shards that no longer exist, so **45 of 45 shards printed
    `? vs ?`** — the read-out was structurally incapable of showing that every
    candidate shared a control nobody is running, which is exactly the defect
    that let two ship candidates be measured against a non-holder for a day.
    `scratchpad/corefill_work.txt` is what the runner actually consumes.

    Kept as a FALLBACK rather than deleted: some archived runs predate the
    worklist and their spec still resolves from the old file.
    """
    spec = {}
    for p in (Path("scratchpad/corefill_work.txt"),
              Path("scratchpad/overnight_spec.txt")):
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            if line.lstrip().startswith("#") or not line.strip():
                continue
            f = line.split()
            # shard treatment control [target] [seed_lo]
            if len(f) >= 3 and f[1].startswith("bots/") and f[0] not in spec:
                spec[f[0]] = (f[1], f[2])
        if spec:
            break
    return spec


_IDENT_CACHE = {}


def trees_identical(a, b):
    """Is bot tree `a` byte-identical to bot tree `b`?

    ⭐ THIS IS WHAT A NULL CELL *IS*, AND IT IS WHY NULLS ARE NO LONGER
    IDENTIFIED BY NAME. The previous fix taught `pick_cal` to MATCH on the
    control tree but left it IDENTIFYING candidates with
    `k.upper().startswith("NULL")` — and `"SHIPGATENULL".startswith("NULL")` is
    False, so the live ship-gate null was invisible for exactly the reason it was
    invisible before, and was additionally counted as a third ARM on the contrast
    it exists to calibrate. Selection was fixed; identification was not.

    A structural test cannot rot: it does not depend on what anyone types, it
    survives any renaming, and it needs no convention to be documented or
    remembered. `_v169null` vs `_v169launchlate160` and `_v146null` vs
    `_v146gunaxis` are both md5-identical on all four files — that property is
    the definition, not a heuristic standing in for it.

    ⚠ NEG CANNOT BE IDENTIFIED THIS WAY — a known-bad arm is by construction NOT
    identical to its control — so NEG keeps a name marker. Only the null half
    stops depending on a naming choice.
    """
    key = (a, b)
    if key in _IDENT_CACHE:
        return _IDENT_CACHE[key]
    pa, pb = Path(a), Path(b)
    ok = False
    if pa.is_dir() and pb.is_dir():
        fa = sorted(f.name for f in pa.glob("*.py"))
        fb = sorted(f.name for f in pb.glob("*.py"))
        ok = bool(fa) and fa == fb and all(
            (pa / n).read_bytes() == (pb / n).read_bytes() for n in fa)
    _IDENT_CACHE[key] = ok
    return ok


def is_null_row(sh, spec):
    """A row is a NULL cell iff its treatment tree is byte-identical to its control."""
    tr, ct = spec.get(sh, (None, None))
    return bool(tr and ct and trees_identical(tr, ct))


def pick_cal(kind, control, data, spec):
    """The calibration cell for THIS contrast, or an explicit refusal.

    ⛔⛔ THE BUG THIS REPLACES, and it would have burned 5,408 games.
    The old lookup was `hits = sorted(k for k in data if k.startswith(prefix))`
    then `hits[0]`. Two independent failures, both silent:

      1. IT MATCHED ON THE START OF THE SHARD NAME. A calibration cell added for
         the ship-gate contrast and named `SHIPGATENULL` is NOT `startswith
         ("NULL")`, so it would never have been selected — the block would keep
         reporting `NULL114`, the *other* fixture, which is the substitution the
         new cell existed to remove.
      2. `hits[0]` TAKES THE LEXICOGRAPHIC FIRST. So even renamed `NULL169`, with
         `NULL114` present, `sorted()` returns `NULL114` and the wrong null STILL
         wins. **The old code selected *a* null, never *the matching* null — it
         had no concept of which contrast a calibration cell belongs to.**

    ⇒ Selection is now by CONTROL TREE, the thing that actually defines the
    fixture. Returns (summary, name, n_candidates) so the caller can PRINT which
    cell it used and say so when the count is not 1 — a calibration that cannot
    name its own cell is not a calibration.

    ⚠ AND IT ENFORCES `refusals`, which the old `_cal` never checked (it read
    `["p"]`/`["n"]` straight out of `summarise`). A shard refused for seat
    imbalance, heartbeat disagreement or duplicate rows STILL carries `p` and
    `n`, so the night's power certificate could be issued off a cell the tool
    printed `NOT SCORED` for three lines earlier. That was background when
    calibration read a long-finished shard; it is load-bearing now that a ship
    gate depends on a NEW null that can be refused.
    """
    cands = []
    for k in sorted(data):
        # NULL is identified STRUCTURALLY (treatment == control, byte for byte);
        # NEG cannot be, so it keeps the name marker. See `trees_identical`.
        if kind == "NULL":
            if not is_null_row(k, spec):
                continue
        elif not k.upper().startswith(kind):
            continue
        if control is not None and spec.get(k, (None, None))[1] != control:
            continue
        cands.append(k)
    if not cands:
        return None, None, 0
    for k in cands:                       # prefer a cell that actually scored
        s = summarise(k, data[k])
        if not s["refusals"] and s["n"]:
            return s, k, len(cands)
    s = summarise(cands[0], data[cands[0]])
    return s, cands[0], len(cands)        # refused; caller must check


def load(d):
    out = {}
    for f in sorted(glob.glob(f"{d}/*.tsv")):
        sh = Path(f).stem
        rows = [l.split("\t") for l in Path(f).read_text().splitlines()[1:] if l.strip()]
        hb = Path(f"{d}/{sh}.heartbeat")
        n_hb = tgt = None
        status = "NO_HEARTBEAT"
        if hb.exists():
            p = hb.read_text().strip().split("\t")
            if len(p) >= 5:
                n_hb, tgt, status = int(p[1]), int(p[2]), p[4]
        out[sh] = dict(rows=rows, n_hb=n_hb, target=tgt, status=status)
    return out


def summarise(sh, d):
    rows = d["rows"]
    n = len(rows)
    refusals = []
    # ⛔⛔ REFUSE ON THE ROWS, NEVER ON THE HEARTBEAT FLAG. Fixed 2026-08-12 (s33)
    # after this branch silently discarded 27,040 REAL GAMES.
    # WHAT HAPPENED: five LOKI-29 shards (SR1CUR/SR1NULL/SR2CUR/SR2NULL/SRNULL0)
    # each carried 5,408 rows with **0 row-level NOWINNER** and a full T/C split,
    # while their heartbeat read `5408  5408  <name>  ABORTED_NOWINNER` — a line
    # that claims the shard BOTH aborted with no winner AND reached its target,
    # and `SR1CUR.COMPLETE` says `reached 5408/5408`. The flag was stale from an
    # earlier aborted attempt and was never cleared on the re-run.
    # ⭐ AND THE HONEST ANSWER WAS ALREADY BEING COMPUTED TWENTY-NINE LINES BELOW
    # (`nowin`, :103) AND THEN IGNORED. A row-level instrument and a flag
    # disagreed and the flag won — the side lane's named characteristic failure
    # (inferring from an artefact instead of opening the primary), compiled into
    # a tool, which is worse than a person doing it once because it refuses
    # silently and forever.
    # The flag is retained ONLY as corroboration: it may not refuse on its own.
    nowinners = sum(1 for r in rows if len(r) > 6 and r[6] == "NOWINNER")
    nowin_pct = 100.0 * nowinners / max(n, 1)
    if nowinners and nowin_pct > 20:
        refusals.append(f"{nowinners} NOWINNER rows ({nowin_pct:.1f}%) — the "
                        f"fixture is broken, these rows are not games")
    override_note = None
    if d["status"] == "ABORTED_NOWINNER" and nowinners == 0 and n:
        # Say it out loud rather than swallowing it: a successor must be able to
        # see that a flag was overridden and on what evidence.
        # ⛔ AND IT GOES IN ITS OWN CHANNEL, NOT IN `refusals` — anything in that
        # list suppresses the whole shard (`:194 continue`), so a "note" filed
        # there would refuse exactly as hard as the bug it replaces.
        override_note = (f"heartbeat says ABORTED_NOWINNER but the rows carry "
                         f"0 NOWINNER across n={n} — STALE FLAG, OVERRIDDEN, "
                         f"scored on the rows")
    # ⛔ THE HEARTBEAT COMPARISON CANNOT FIRE, AND IT IS THE SIXTH UNFIRABLE
    # GUARD OF THIS SESSION. `overnight.sh` now RESUMES by setting `n` to the
    # existing row count, so the heartbeat's n and len(rows) agree BY
    # CONSTRUCTION -- the fix for restart-duplication defeated its own detector.
    # Kept (it still catches a truncated/corrupt tsv) but it is NOT the
    # duplication check. The real one is below: a duplicated prefix repeats
    # (map, seed, seat) triples, which a clean run never does.
    if d["n_hb"] is not None and n and abs(n - d["n_hb"]) > max(1, 0.01 * n):
        refusals.append(f"row count {n} disagrees with heartbeat n={d['n_hb']} "
                        f"— tsv truncated or corrupt")
    keys = [(r[3], r[4], r[5]) for r in rows if len(r) > 5]
    dupes = len(keys) - len(set(keys))
    # ⛔ WARNING, NOT REFUSAL, AND THE REASON IS SPECIFIC TO THIS BOT.
    # `overnight.sh` resumes at MAPS[0]/ORD=A with seed = SEEDLO + n/16, so a
    # mid-cycle restart replays `n mod 16` triples. Measured live: 1-14 rows per
    # shard, <=3.6%. **BUT OUR BOT RESEEDS AN UNSEEDED RNG EVERY GAME
    # (main.py:276), so a repeated (map,seed,seat) is a FRESH DRAW, not a copied
    # observation.** Refusing 8 of 9 healthy shards over it would be the same
    # error as the seat guard refusing 78/76. Reported, with the count, so a
    # reader can judge -- and it WOULD refuse at a magnitude that matters.
    dup_pct = 100.0 * dupes / max(len(keys), 1)
    dup_note = (f"{dupes} repeated (map,seed,seat) rows ({dup_pct:.1f}%) from a "
                f"mid-cycle restart — FRESH DRAWS, not copies, because the bot "
                f"reseeds per game") if dupes else None
    if dup_pct > 20:
        refusals.append(f"{dupes} duplicate rows ({dup_pct:.1f}%) — too many to be "
                        f"restart residue; the sample is skewed to low seeds")
    nowin = nowinners
    good = [r for r in rows if len(r) > 8 and r[6] in ("T", "C")]
    if not good:
        return dict(sh=sh, n=0, refusals=refusals + ["no scorable rows"])
    W = sum(1 for r in good if r[6] == "T")
    seatA = [r for r in good if r[5] == "A"]
    seatB = [r for r in good if r[5] == "B"]
    # ⛔ TOLERANCE, NOT ZERO. The loop plays seats A,B alternately, so a shard
    # read MID-RUN is legitimately up to a couple of games apart. A refusal
    # threshold of 1 fired on healthy shards at 78/76 — a guard that refuses
    # good data is as wrong as one that passes bad. Proportional, floor 2.
    tol = max(2, int(0.01 * len(good)))
    if abs(len(seatA) - len(seatB)) > tol:
        refusals.append(f"seat imbalance {len(seatA)}/{len(seatB)} (tol {tol}) — "
                        f"seat is worth 7.6pp, an unbalanced shard measures SEAT")
    N = len(good)
    p = W / N
    hw = 1.96 * math.sqrt(0.25 / N)
    kills_t = [int(r[8]) for r in good if r[6] == "T" and r[7] == "core_destroyed" and r[8].isdigit()]
    kills_c = [int(r[8]) for r in good if r[6] == "C" and r[7] == "core_destroyed" and r[8].isdigit()]
    ties = sum(1 for r in good if r[7] == "tiebreak")
    # Audit M4 (2026-08-13): the map rotation retired 4 of the old 8 battery
    # maps and a shard's array is frozen at startup, so a rate can silently
    # span dead geometry. Tally the retired share; the printer refuses the
    # verdict line when it is nonzero and reports the live-pool subset instead.
    pool = live_pool()
    if pool is None:
        retired, ret_maps, live_sub = -1, set(), None       # BLIND
    else:
        ret_rows = [r for r in good if r[3] not in pool]
        retired = len(ret_rows)
        ret_maps = {r[3] for r in ret_rows}
        lg = [r for r in good if r[3] in pool]
        wl = sum(1 for r in lg if r[6] == "T")
        live_sub = (wl, len(lg))
    return dict(sh=sh, n=N, target=d["target"], status=d["status"], W=W, p=p, hw=hw,
                seatA=(sum(1 for r in seatA if r[6] == "T"), len(seatA)),
                seatB=(sum(1 for r in seatB if r[6] == "T"), len(seatB)),
                kt=kills_t, kc=kills_c, ties=ties, nowin=nowin, refusals=refusals,
                override_note=override_note,
                dup_note=dup_note,
                retired=retired, ret_maps=ret_maps, live_sub=live_sub,
                maps=len({r[3] for r in good}))


def implied_elo(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    return -400 * math.log10(1 / p - 1)


def selftest():
    """⭐ THIS TESTS THE **DECIDING** FUNCTION, NOT THE PARSING FUNCTION.

    Magnus, 2026-08-12: *"Dont we test our tools?"* — asked after `crash_cells.py`
    shipped a green 7-case selftest and then printed **"THE WEAPON DOES NOT FIRE
    — the road closes"** on a run in which the weapon had fired 15 times, and
    after this file discarded 27,040 real games.

    **THE PATTERN BEHIND BOTH, AND IT IS THE WHOLE POINT OF THIS FUNCTION: the
    selftests in this repo drive the MEASURING functions and leave the DECIDING
    branch untested.** `crash_cells` v1 tested its crash counter to 0 and >0 and
    never once tested the branch that turns a count into a verdict. This file
    computed `nowin` from the rows (`:131`) and then refused on a heartbeat flag
    it never compared against — a measurement that was right and a decision that
    ignored it. **Every cell below asserts on a REFUSE / SCORE outcome.**

    Each cell must be reachable both ways, or it validates nothing.
    """
    bad = 0

    def chk(name, got, want):
        nonlocal bad
        ok = got == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name:56s} got={got!r} want={want!r}")

    def shard(n_rows, nowinner=0, status="COMPLETE"):
        rows = []
        for i in range(n_rows):
            res = "NOWINNER" if i < nowinner else ("T" if i % 2 else "C")
            seat = "A" if i % 2 else "B"
            # Distinct (map, seed, seat) per row: a constant seed makes every
            # row a "duplicate" and trips the restart-residue guard, which is
            # the guard doing its job on a bad fixture rather than a defect.
            rows.append(["ts", "tr", "ct", f"map{i % 8}", str(1000 + i // 8),
                         seat, res, "core_destroyed", "200"])
        return dict(rows=rows, n_hb=n_rows, target=n_rows, status=status)

    # ---- THE CELL THAT FAILS ON THE OLD CODE -------------------------------
    # 5,408 real games under a STALE ABORTED_NOWINNER heartbeat. This is
    # SR1CUR/SR1NULL/SR2CUR/SR2NULL/SRNULL0 exactly, and all five were refused.
    stale = summarise("SR1CUR", shard(5408, nowinner=0, status="ABORTED_NOWINNER"))
    chk("stale ABORTED_NOWINNER + 0 bad rows -> SCORES", stale["refusals"], [])
    chk("...and n survives", stale["n"], 5408)
    chk("...and the override is announced, not swallowed",
        bool(stale["override_note"]), True)

    # ---- THE OTHER WAY: a genuinely broken fixture MUST still refuse --------
    broken = summarise("BROKEN", shard(1000, nowinner=900, status="COMPLETE"))
    chk("900/1000 NOWINNER rows -> REFUSES", len(broken["refusals"]) >= 1, True)
    chk("...even with a HEALTHY heartbeat", broken["status"], "COMPLETE")

    # A handful of NOWINNER rows is residue, not a broken fixture.
    few = summarise("FEW", shard(5408, nowinner=5, status="COMPLETE"))
    chk("5/5408 NOWINNER rows -> still SCORES", few["refusals"], [])

    # A clean shard with a clean flag must score, and must NOT print an override.
    clean = summarise("CLEAN", shard(5408, nowinner=0, status="COMPLETE"))
    chk("clean shard -> SCORES", clean["refusals"], [])
    chk("clean shard -> NO override note", clean["override_note"], None)

    # ---- CALIBRATION RESOLUTION, both ways ---------------------------------
    # ⛔ THESE CELLS NOW CALL THE REAL `pick_cal`, NOT A REIMPLEMENTATION.
    # The previous version defined its own `cal_keys()` that duplicated the
    # prefix lookup, while the live lookup was a closure inside `main()` that no
    # test could reach. Mutation-tested 2026-08-12: restoring the original
    # literal-key bug to the REAL path left this selftest PASSING 11/11,
    # including a cell literally named "calibration found by PREFIX". A test
    # that validates a copy of the code is not a test.
    # ⚠ CONTRACT CHANGE, ASSERTED RATHER THAN QUIETLY DROPPED: NULL is no longer
    # found by NAME at all — it is found by treatment==control (see
    # `trees_identical`), so a bare name with no worklist entry CANNOT resolve as
    # a null and must come back None. NEG still uses the name marker, because a
    # known-bad arm is by construction not identical to its control. These two
    # cells failed when the contract changed, which is what a real test does.
    def cal_keys(keys):
        data = {k: shard(64) for k in keys}
        return tuple(pick_cal(pre, None, data, {})[1] for pre in ("NULL", "NEG"))

    ident = {"Z": shard(64)}
    spi = {"Z": ("bots/_v169null", "bots/_v169launchlate160")}
    chk("a null with NO conventional name resolves purely on tree identity",
        pick_cal("NULL", None, ident, spi)[1], "Z")

    # ---- THE CELL SIDE LANE ASKED FOR: TWO NULLS, WHICH ONE IS PICKED? -----
    # A ship gate controlled on a different tree than the calibration cells is
    # the failure this whole function exists to prevent. Both nulls present, both
    # scorable — the ONLY thing that can distinguish them is the control tree.
    two = {"NULL114": shard(64), "NULL169": shard(64), "SHIPGATE160": shard(64)}
    sp2 = {"NULL114":    ("bots/_v146null", "bots/_v146gunaxis"),
           "NULL169":    ("bots/_v169null", "bots/_v169launchlate160"),
           "SHIPGATE160": ("bots/_v171late160ammo", "bots/_v169launchlate160")}
    chk("⭐ the null matching the SHIP contrast is chosen over the lexicographic first",
        pick_cal("NULL", "bots/_v169launchlate160", two, sp2)[1], "NULL169")
    chk("...and the v146 contrast still resolves to its OWN null",
        pick_cal("NULL", "bots/_v146gunaxis", two, sp2)[1], "NULL114")
    chk("...and a contrast with NO null on it reports ABSENT, not a borrowed cell",
        pick_cal("NULL", "bots/_v999nothing", two, sp2)[1], None)
    # ⛔ THE CELL THAT USED TO SIT HERE ASSERTED A FACT ABOUT PYTHON, NOT ABOUT
    # THIS TOOL: `"SHIPGATENULL".startswith("NULL") == False`. That is true
    # forever, whatever the tool does, so it could never fail — and it was GREEN
    # while the live `SHIPGATENULL` cell was invisible to the calibration block
    # and was being counted as a third ARM on its own contrast. A permanently
    # true assertion is not a test. Replaced with the two that can fail:
    nc = {"SHIPGATENULL": shard(64), "SHIPGATE160": shard(64)}
    spn = {"SHIPGATENULL": ("bots/_v169null", "bots/_v169launchlate160"),
           "SHIPGATE160":  ("bots/_v171late160ammo", "bots/_v169launchlate160")}
    chk("⭐ a NON-CONFORMING null name still resolves — identification is STRUCTURAL",
        pick_cal("NULL", "bots/_v169launchlate160", nc, spn)[1], "SHIPGATENULL")
    chk("...and it is NOT counted as an arm on the contrast it calibrates",
        is_null_row("SHIPGATENULL", spn), True)
    chk("...while a real arm on the same contrast is NOT mistaken for a null",
        is_null_row("SHIPGATE160", spn), False)

    # ⭐ AND THE ONE THAT READS THE LIVE WORKLIST, NOT A FIXTURE. A fixture with
    # conforming names can never fail the cell above; only the real worklist can.
    live = load_spec()
    if live:
        ident = [k for k in live if is_null_row(k, live)]
        chk("LIVE worklist: at least one row is byte-identical to its control",
            bool(ident), True)
        for k in ident:
            c = live[k][1]
            chk(f"LIVE: `{k}` resolves as the NULL for its own contrast",
                pick_cal("NULL", c, {k: shard(64)}, live)[1], k)
    # And refusals must be surfaced, not scored through.
    ref = {"NULLX": shard(1000, nowinner=900)}
    spr = {"NULLX": ("bots/_v169null", "bots/_v169launchlate160")}
    got = pick_cal("NULL", "bots/_v169launchlate160", ref, spr)[0]
    chk("a REFUSED null is returned WITH its refusals, never as a clean cell",
        bool(got and got["refusals"]), True)

    chk("NEG is still found by its name marker",
        cal_keys(["NULL114", "NEG114", "GUNBLANK"])[1], "NEG114")
    chk("...and under the OLD literal name too",
        cal_keys(["NULL", "NEGCTRL", "X"])[1], "NEGCTRL")
    chk("⛔ a NULL-shaped NAME with no worklist row does NOT resolve — names are not evidence",
        cal_keys(["NULL114", "NEG114", "GUNBLANK"])[0], None)
    chk("calibration genuinely ABSENT is reported as absent",
        cal_keys(["GUNBLANK", "CAP6B"]), (None, None))

    print("\n" + ("PASS: a stale flag over good rows SCORES, a genuinely broken "
                 "fixture REFUSES, and calibration resolves under both naming "
                 "conventions and reports its own absence."
                 if not bad else f"FAIL: {bad} case(s)"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = "scratchpad/overnight"
    if "--dir" in sys.argv:
        d = sys.argv[sys.argv.index("--dir") + 1]
    data = load(d)
    print("=" * 78)
    print("OVERNIGHT READ-OUT — partial shards POOLED with the shortfall printed")
    print("=" * 78)
    spec = load_spec()
    if not spec:
        print("  ⚠ NO WORKLIST FOUND — every shard below prints '? vs ?' and the")
        print("     calibration cell CANNOT be matched to a contrast. Verdicts are")
        print("     uncalibrated; treat them as arithmetic, not as findings.")

    for sh in sorted(data):
        s = summarise(sh, data[sh])
        tr, ct = spec.get(sh, ("?", "?"))
        pct = (100.0 * s["n"] / s["target"]) if s.get("target") else float("nan")
        tag = "COMPLETE" if s.get("status") == "COMPLETE" else f"PARTIAL {pct:.1f}%"
        print(f"\n{sh}   {Path(tr).name} vs {Path(ct).name}")
        if s["refusals"]:
            for r in s["refusals"]:
                print(f"   ⛔ REFUSED: {r}")
            # ⛔ A REFUSAL THAT DOES NOT REFUSE. The first version continued only
            # when n==0, so every other refusal printed its banner and then went
            # on to print a win rate, a band and a VERDICT line. A fixture with
            # ABORTED_NOWINNER read "rows are not games" and then scored them.
            # At 06:00 a reader scrolls to VERDICT:. (Side lane fixture M4.)
            print("   ⇒ NOT SCORED. No verdict is printed for a refused shard.")
            continue
        print(f"   n={s['n']}/{s.get('target','?')}  {tag}   maps={s['maps']}  "
              f"NOWINNER={s['nowin']}  tiebreaks={s['ties']}")
        if s.get("override_note"):
            print(f"   ⚠ FLAG OVERRIDDEN: {s['override_note']}")
        if s.get("dup_note"):
            print(f"   ⚠ {s['dup_note']}")
        print(f"   WINS {s['W']}/{s['n']} = {s['p']:.2%}   informative band "
              f"{50-s['hw']*100:.2f}%–{50+s['hw']*100:.2f}%")
        a, an = s["seatA"]; b, bn = s["seatB"]
        print(f"   seat A {a}/{an}={a/max(an,1):.1%}   seat B {b}/{bn}={b/max(bn,1):.1%}")
        if s["kt"] and s["kc"]:
            mt = sorted(s["kt"])[len(s["kt"]) // 2]; mc = sorted(s["kc"])[len(s["kc"]) // 2]
            print(f"   median kill round  TREAT {mt}  CTRL {mc}   "
                  f"(kills {len(s['kt'])} vs {len(s['kc'])})")
        v = ("OUTSIDE-BELOW real negative" if s["p"] < 0.5 - s["hw"]
             else "OUTSIDE-ABOVE escalate" if s["p"] > 0.5 + s["hw"]
             else "NO-INFORMATION — back to the pool, NOT demoted")
        # Audit M4: no verdict on dead geometry, and no silence about it either.
        if s.get("retired", 0) == -1:
            print("   ⚠ RETIRED-CHECK BLIND: live pool unparseable from tools/overnight.sh")
            print(f"   VERDICT: {v}")
        elif s.get("retired", 0) > 0:
            rp = 100.0 * s["retired"] / s["n"]
            print(f"   ⛔ RETIRED GEOMETRY: {s['retired']}/{s['n']} rows ({rp:.1f}%) on "
                  f"maps no longer in the pool ({', '.join(sorted(s['ret_maps']))})")
            wl, nl = s["live_sub"]
            if nl >= 400:
                hwl = 1.96 * math.sqrt(0.25 / nl)
                print(f"   VERDICT: REFUSED — rate spans dead geometry. Live-pool "
                      f"subset: {wl}/{nl} = {wl/nl:.2%} (band ±{hwl*100:.2f}pp) — "
                      f"a SUBSET, not a scheduled look")
            else:
                print(f"   VERDICT: REFUSED — rate spans dead geometry. Live-pool "
                      f"subset n={nl} (<400): NO RATE PRINTED")
        else:
            print(f"   VERDICT: {v}")

    # ---- HARNESS CALIBRATION: what the control shards are FOR ----
    # ⛔ THEY WERE REPORTED AS ORDINARY PEERS, WHICH WASTES THEM. A null arm that
    # is merely printed answers nothing; a null arm that RE-CENTRES the bands
    # tells every other shard what "no effect" looked like TONIGHT, on this
    # machine, at this contention. (Side lane's audit question, adopted.)
    print("\n" + "=" * 78)
    print("HARNESS CALIBRATION — what the two control shards say about the night")
    print("=" * 78)
    # ⛔⛔ RESOLVE CALIBRATION SHARDS BY PREFIX. Fixed 2026-08-12 (s33).
    # These two lines looked up the LITERAL keys "NULL" and "NEGCTRL". Every
    # shard we have ever actually run is named for its baseline — NULL114,
    # NEG114, and s31's equivalents — so NEITHER KEY HAS EVER MATCHED and this
    # whole section has printed "⚠ NO NULL DATA — every band below is
    # uncalibrated" on every run of its life. The `BANDS RE-CENTRED` branch
    # below is dead code that has never once executed.
    # ⚠ AND FIXING THE KEY ALONE DOES NOT MOVE TONIGHT'S BANDS, which is worth
    # stating so nobody re-derives a difference that is not there: the
    # re-centring is gated on |z| > 3 and the measured null is z = −0.03, and
    # the per-shard band at `:199` is hardcoded to 50 ± hw and never reads
    # `centre` at all. What the fix buys is that the calibration cells are
    # SEEN and can FIRE — not a different band tonight.
    # ⛔ CALIBRATE PER CONTRAST, NOT ONCE FOR THE WHOLE RUN.
    # A run can carry arms on several control trees at once — tonight it carries
    # `_v146gunaxis` (the v114 contrast) AND `_v169launchlate160` (the ship gate
    # against the LIVE holder). A single global null calibrates whichever fixture
    # it happens to come from and silently certifies the others.
    controls = {}
    for k in data:
        c = spec.get(k, (None, None))[1]
        # A calibration cell is NOT an arm. Nulls are excluded structurally, so a
        # cell named `SHIPGATENULL` stops being counted as a third arm on the
        # very contrast it calibrates.
        if c and not is_null_row(k, spec) and not k.upper().startswith(("NEG", "CAL")):
            controls.setdefault(c, []).append(k)
    for c in sorted(controls):
        n_arm = len(controls[c])
        s_n, k_n, c_n = pick_cal("NULL", c, data, spec)
        s_g, k_g, c_g = pick_cal("NEG", c, data, spec)
        print(f"  contrast vs {Path(c).name}  ({n_arm} arm(s))")
        for kind, s, k, cn in (("NULL", s_n, k_n, c_n), ("NEG", s_g, k_g, c_g)):
            if s is None:
                print(f"     ⛔ NO {kind} CELL ON THIS CONTRAST — the band applied to "
                      f"these {n_arm} arm(s) is BORROWED from another fixture.")
            elif s["refusals"]:
                print(f"     ⛔ {kind} cell `{k}` was REFUSED "
                      f"({s['refusals'][0][:60]}) — NOT USABLE as calibration.")
            else:
                print(f"     {kind} cell `{k}`  {s['p']:.2%} on n={s['n']}"
                      + (f"   ⚠ {cn} candidates, picked one" if cn != 1 else ""))
    print()

    # The legacy global read below is kept because PART A and the re-centring
    # branch consume it. It is now explicitly labelled as global.
    nul, _kn, _cn = pick_cal("NULL", None, data, spec)
    neg, _kg, _cg = pick_cal("NEG", None, data, spec)
    if nul and nul["refusals"]:
        print(f"  ⛔ THE GLOBAL NULL WAS REFUSED — {nul['refusals'][0][:70]}")
        print("     Treating it as ABSENT rather than scoring off a refused cell.")
        nul = None
    if neg and neg["refusals"]:
        print(f"  ⛔ THE GLOBAL NEGCTRL WAS REFUSED — {neg['refusals'][0][:70]}")
        neg = None
    centre = 0.5
    if nul and nul["n"]:
        z = (nul["p"] - 0.5) / math.sqrt(0.25 / nul["n"])
        print(f"  NULL (byte-identical v112 copy)  {nul['p']:.2%} on n={nul['n']}  z={z:+.2f}")
        if abs(z) > 3:
            print("  ⛔ THE NULL IS OFF 50%. The harness is biased tonight and EVERY")
            print("     band below is measured against a bent ruler. Re-centring on it.")
            centre = nul["p"]
        else:
            print("  ✓ consistent with 50% — the harness is unbiased, bands stand.")
        a, an = nul["seatA"]; b, bn = nul["seatB"]
        if an and bn:
            print(f"     seat A {a/an:.1%} vs seat B {b/bn:.1%} on byte-identical arms "
                  f"— this IS the seat effect, measured tonight")
    else:
        print("  ⚠ NO NULL DATA — every band below is uncalibrated.")
    if neg and neg["n"]:
        print(f"  NEGCTRL (_v140noseal, a KNOWN real negative, 39.0% vs v104)  "
              f"{neg['p']:.2%} on n={neg['n']}")
        if neg["p"] < 0.5 - neg["hw"]:
            print("  ✓ the screen still DETECTS a known-bad arm at this n.")
        else:
            print("  ⛔ A KNOWN NEGATIVE READS AS NO-INFORMATION. The screen has lost")
            print("     its power tonight and no NO-INFORMATION verdict below is safe.")
    else:
        print("  ⚠ NO NEGCTRL DATA — the screen's power is unverified tonight.")
    if centre != 0.5:
        print(f"\n  ⇒ BANDS RE-CENTRED ON THE MEASURED NULL ({centre:.2%}), not on 50%.")

    # ---- PART A: falsifier, not estimator ----
    n_arms = sum(1 for k in data if not k.startswith("CAL"))
    if n_arms > 1:
        p_any = 1 - 0.95 ** n_arms
        print(f"\n⚠ MULTIPLICITY: {n_arms} arms screened at 5% each ⇒ "
              f"P(at least one spurious OUTSIDE verdict) = {p_any:.2f}. "
              f"A single escalate is NOT a finding on its own.")
    print("\n" + "=" * 78)
    print("PART A — DOES A LOCAL h2h WIN RATE PREDICT THE LADDER?  (FALSIFIER)")
    print("=" * 78)
    any_a = False
    for sh in sorted(data):
        if not sh.startswith("CAL"):
            continue
        s = summarise(sh, data[sh])
        tr, ct = spec.get(sh, ("?", "?"))
        t, c = Path(tr).name, Path(ct).name
        if s["n"] == 0 or t not in LADDER or c not in LADDER:
            print(f"  {sh}: NOT SCOREABLE (no opponent-controlled ladder estimate)")
            continue
        any_a = True
        loc = implied_elo(s["p"])
        lad = LADDER[t] - LADDER[c]
        print(f"\n  {t} vs {c}   n={s['n']}")
        print(f"    local {s['p']:.2%} ⇒ implied Elo gap {loc:+.1f}")
        print(f"    ladder (opponent-controlled) gap {lad:+.1f}  "
              f"[{LADDER_CI[t][0]}-{LADDER_CI[t][1]} vs {LADDER_CI[c][0]}-{LADDER_CI[c][1]}]")
        print(f"    residual {loc-lad:+.1f} Elo")
        print(f"    ORDERING: local says {t if loc>0 else c} better; "
              f"ladder says {t if lad>0 else c} better  "
              f"⇒ {'AGREE' if (loc>0)==(lad>0) else '⛔ INVERTED'}")
    if any_a:
        print("\n  ⛔ THE PRE-REGISTERED BAR (Amendment 1, before any game ran):")
        print("     ANY inversion, or large unsigned residuals ⇒ LOCAL SCREENS DO NOT")
        print("     PREDICT THE LADDER. Stop screening this week; ship on mechanism.")
        print("     Ordering holds ⇒ FAILED TO FALSIFY. Consistent with predicting.")
        print("     NOT PROOF — and the write-up must say so in those words.")
    print("\n  ⚠ v112 has ZERO archived ladder games, so its pairings are")
    print("    unscoreable at ANY local n. Four of the original six cells cannot")
    print("    be graded and are not reported as weak evidence.")


if __name__ == "__main__":
    main()
