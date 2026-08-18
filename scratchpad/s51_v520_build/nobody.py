#!/usr/bin/env python3
"""v520 THE NOBODY SHARE, RE-MEASURED ENTIRELY REPLAY-SIDE.

`s51_v518_build/gapdecomp.py` decomposes the [arrive, sent) window by the
bot's own `GAP518` stderr lines and calls a window round with NO line
`NOBODY` -- no raider of ours taking a ring turn.  That number is not portable:
it depends on an stderr instrument that differs between arms (v520's arms carry
different tapes, and a flag-off arm may carry none), so a NOBODY difference
between arms can be an instrument difference rather than a fact about raiders.

⛔ THIS FILE ANSWERS THE SAME QUESTION WITH NO STDERR AT ALL.  Same window,
same radius, engine-side only:

  window   [arrive, sent), or [arrive, last] when a forward sentinel is never
           bought -- `phase.marks`, unchanged, imported not copied.
           arrive = first round a BUILDER BOT of ours is inside d^2 <= 8 of the
                    enemy core CENTRE  (`Tape.near_bot`)
           sent   = first round a SENTINEL of ours is inside d^2 <= 40
                    (`Tape.near_sent`)
  ge1      window rounds with >= 1 of our builder bots inside d^2 <= 8
  ge2      window rounds with >= 2   -- the pincer's second body, in the same
           coordinates, so "two bodies at the ring" is a measured column
  NOBODY   1 - ge1/window

⭐⭐ TWO RING ENVELOPES LIVE IN THIS REPO AND THEY ARE NOT THE SAME SET.  Found
by running `--join` against the one fixture that still carries the stderr tape
(`s51_v518_build/gapbase`, 29 games, 7,740 window rounds): NOBODY(stderr) read
0.6481 while NOBODY(replay) read 0.7483 -- the replay-side number came out
HIGHER, which the first draft of this file had asserted was impossible.  The
cause is a convention collision, not a bug in either instrument:

  * `Tape.near_bot` (and therefore `phase.marks`, `gapdecomp`'s window and the
    `ge1` column above) tests d^2 <= 8 to the 2x2 core CENTRE  -> 24 tiles.
  * `siege.py`'s `FS_RING_DSQ = 8` -- the condition the bot's own GAP518 line
    is emitted under -- tests `dsq_core`, the FOOTPRINT-AWARE minimum over the
    four core tiles                                            -> 49 tiles.
  Enumerated on a 22x22 board around a core at (10,10): the footprint envelope
  STRICTLY CONTAINS the centre one (25 tiles are in footprint-only, 0 tiles are
  in centre-only).  So a body can be taking a ring turn, and logging, while
  `near_bot` reads 0 -- 776 such rounds in that fixture.

⇒ `ge1_fp` / `nobody_fp` carry the FOOTPRINT convention alongside, and it is
`nobody_fp` -- not `nobody` -- that is comparable to a GAP518 tape.  The window
itself stays on the centre convention because that is `gapdecomp`'s window and
this file exists to be comparable to it.  Every column says which it used.

⛔ THE ONE THING THIS IS NOT.  gapdecomp's NOBODY is "no raider TOOK A RING
TURN"; this one is "no raider was INSIDE THE RADIUS at end of round".  They
differ by exactly the seam gapdecomp already documents (its cross-check counts
NOBODY rounds that nevertheless had near_bot > 0 and calls <=5% the known
seam: the bot logs at ITS turn, the replay row is end-of-round state).  So the
replay-side number is a LOWER bound on gapdecomp's NOBODY, never a drop-in
replacement, and `--join` prints both side by side when an arm has stderr.

⛔ COPIED, NOT REWRITTEN.  `Tape` is `s51_v519_build/reel/tape.py` (identical to
`s51_rush_autopsy/tape.py`, diffed); `marks` is `phase.py`; the window contract
and its guard are `s51_v518_build/gapdecomp.py`, whose `guard()` RUNS IN PLACE
in the selftest below.

⛔ GUARDS, EVERY ONE DRIVEN BOTH WAYS (`--selftest`):
  N1 gapdecomp.guard() runs in place -- the window contract (known histogram,
     the hole is counted not dropped, never-bought uses [arrive,last],
     never-arrived is dropped, and its mutation control).
  N2 phase.guard() runs in place -- the marks (-1 vs 0, known rounds, order).
  N3 KNOWN SYNTHETIC TAPE -> exact window / ge1 / ge2 / share.
  N4 MUTATION CONTROL: zero every near_bot -> share must go to 1.0 and ge1/ge2
     to 0.  A fold that ignored the column would return the same row.
  N5 INVERTED CONTROL: near_bot >= 2 everywhere -> share 0.0 and ge2 == window.
  N6 EMPTY-WINDOW and NEVER-ARRIVED controls: a zero-length window has share
     None (not 0), a never-arrived game is dropped AND counted.
  N7 REAL-DATA TEAM-SWAP POSITIVE CONTROL: re-reading one replay with the
     seat->team assignment flipped must MOVE the window and the share.
  N8 REAL-DATA CROSS-CHECK: `kill` from the Tape must agree with the grid
     TSV's `Core destroyed` turn on games we won (phase.py's own real-data
     guard, run here on every game rather than asserted).

Usage:
  nobody.py --selftest
  nobody.py <grid.tsv> <repdir> <out.tsv> [arm_label]
  nobody.py --report <out.tsv> [<out.tsv> ...]
  nobody.py --join <grid.tsv> <repdir> <logdir>     (vs gapdecomp's stderr)
"""
from __future__ import annotations

import csv
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scratchpad/s51_v519_build/reel"))   # tape.py
sys.path.insert(0, str(ROOT / "scratchpad/s51_v518_build"))        # gapdecomp
from tape import Tape  # noqa: E402
from phase import marks  # noqa: E402

NEAR_DSQ = 8      # Tape.near_bot's radius, CENTRE convention -- do not restate

# ⛔ TWO CLOCKS, AND THEY ARE OFF BY ONE.  `run_grid.py:41` scrapes `turn` out
# of the CLI's `Winner: X (cond, turn N)` line, which is 1-INDEXED; the replay
# turn stream (and `get_current_round()`) is 0-INDEXED.  Measured on grid block
# b1, all three arms: 42 core-kill wins (parent 13, v520 15, flagoff 14) and
# grid_turn - replay_round == 1 in 42 of 42, offset histogram {1: 42} in every
# arm separately.  So the cross-check asserts the OFFSET, and any
# game with a different offset is an instrument alarm rather than a row.
KILL_OFFSET = 1


# --------------------------------------------------------------------------
# THE FOLD.  Takes the Tape rows so the guards can drive it on synthetic ones.
# --------------------------------------------------------------------------
def fold(rows, near_fp=None):
    """-> dict, or None when the game never arrived (dropped AND counted).

    near_fp: optional {round: n bots inside the FOOTPRINT envelope}; when given
    the ge1_fp / nobody_fp columns are filled, otherwise they are None.
    """
    a, s, _f, k = marks(rows)
    if a < 0:
        return None
    last = rows[-1]["r"] if rows else 0
    end = s if s >= 0 else last + 1
    window = max(0, end - a)
    near = {r["r"]: r["near_bot"] for r in rows}
    ge1 = sum(1 for r in range(a, end) if near.get(r, 0) >= 1)
    ge2 = sum(1 for r in range(a, end) if near.get(r, 0) >= 2)
    out = dict(arrive=a, sent=s, kill=k, last=last, window=window,
               ge1=ge1, ge2=ge2,
               nobody=(round(1.0 - ge1 / window, 4) if window else None),
               two_body_share=(round(ge2 / window, 4) if window else None),
               bought_sentinel=int(s >= 0),
               ge1_fp=None, ge2_fp=None, nobody_fp=None)
    if near_fp is not None:
        g1 = sum(1 for r in range(a, end) if near_fp.get(r, 0) >= 1)
        g2 = sum(1 for r in range(a, end) if near_fp.get(r, 0) >= 2)
        out["ge1_fp"] = g1
        out["ge2_fp"] = g2
        out["nobody_fp"] = round(1.0 - g1 / window, 4) if window else None
    return out


def near_footprint(replay, our_team):
    """{round: n of OUR builder bots with dsq_core(pos, enemy core) <= 8}.

    The bot's OWN ring test (`siege.FS_RING_DSQ`), footprint-aware -- a
    strictly larger envelope than `Tape.near_bot`.  Built from ringwalk, whose
    guards run in place.
    """
    from ringwalk import FS_RING_DSQ, dsq_core, replay_map, walk
    _w, _h, _r, cores = replay_map(replay)
    E = {c["team"]: c["pos"] for c in cores}[1 - our_team]
    out = {}
    for rnd, ents in walk(replay):
        out[rnd] = sum(1 for (k, t, p, _b) in ents.values()
                       if k == "builder_bot" and t == our_team
                       and dsq_core(p, E) <= FS_RING_DSQ)
    return out


# ============================== SELFTEST =====================================

def _rows(near, rounds=100, sent_at=None, kill_at=None):
    out = []
    for i in range(rounds):
        out.append({"r": i, "near_bot": near(i),
                    "near_sent": 1 if (sent_at is not None and i >= sent_at) else 0,
                    "our_ammo": 0,
                    "opp_core_hp": 0 if (kill_at is not None and i >= kill_at)
                    else 500})
    return out


def _pick_real():
    from ringwalk import MAPS
    for d in (HERE / "grid", HERE.parent / "s51_v519_build" / "grid"):
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.replay26")):
            tag = p.stem
            m = next((m for m in MAPS if tag.startswith(m)), None)
            s = tag.rsplit("_", 1)[-1]
            if m and s in ("A", "B"):
                return p, m, s
    return None


def selftest():
    ok = True

    def chk(name, cond, detail=""):
        nonlocal ok
        print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                              ("  " + detail) if detail else ""))
        if not cond:
            ok = False

    # N1 / N2 -- the borrowed guards, RUN IN PLACE ----------------------------
    print("=== N1: gapdecomp.guard(), in place ===")
    import gapdecomp
    if not gapdecomp.guard():
        ok = False
    print("=== N2: phase.guard(), in place ===")
    import phase
    if not phase.guard():
        ok = False

    print("=== nobody selftest ===")

    # N3 -- known synthetic tape ----------------------------------------------
    # arrive r20 (near_bot goes 1), sent r60.  Window = 40 rounds [20,60).
    # near_bot: 1 on [20,30), 0 on [30,40) (the hole), 2 on [40,60).
    def near(i):
        if 20 <= i < 30:
            return 1
        if 40 <= i:
            return 2
        return 0
    r = fold(_rows(near, 100, sent_at=60, kill_at=80))
    chk("N3 window == 40 [arrive 20, sent 60)",
        (r["arrive"], r["sent"], r["window"]) == (20, 60, 40), str(r))
    chk("N3 ge1 == 30 (10 single-body + 20 two-body)", r["ge1"] == 30,
        str(r["ge1"]))
    chk("N3 ge2 == 20", r["ge2"] == 20, str(r["ge2"]))
    chk("N3 NOBODY share == 1 - 30/40 == 0.25", r["nobody"] == 0.25,
        str(r["nobody"]))
    chk("N3 two_body_share == 0.5", r["two_body_share"] == 0.5,
        str(r["two_body_share"]))
    chk("N3 kill mark recovered", r["kill"] == 80, str(r["kill"]))

    # N4 -- MUTATION CONTROL ---------------------------------------------------
    rowsm = _rows(near, 100, sent_at=60, kill_at=80)
    for x in rowsm:
        if x["r"] >= 20:
            x["near_bot"] = 0
    rm = fold(rowsm)
    chk("N4 mutation: zeroing near_bot after arrive drops the game entirely "
        "(no arrive) -- the marks read the same column",
        rm is None, str(rm))
    # a milder mutation that keeps arrive but empties the rest of the window
    rowsm2 = _rows(near, 100, sent_at=60, kill_at=80)
    for x in rowsm2:
        if x["r"] > 20:
            x["near_bot"] = 0
    rm2 = fold(rowsm2)
    chk("N4 mutation: one arrival round only -> ge1 1, ge2 0, share 0.975",
        (rm2["ge1"], rm2["ge2"], rm2["nobody"]) == (1, 0, 0.975), str(rm2))
    chk("N4 mutation MOVED the row (a near_bot-blind fold would not)",
        rm2["nobody"] != r["nobody"])

    # N5 -- INVERTED CONTROL ---------------------------------------------------
    ri = fold(_rows(lambda i: 2 if i >= 20 else 0, 100, sent_at=60))
    chk("N5 inverted: two bodies every round -> share 0.0 and ge2 == window",
        (ri["nobody"], ri["ge2"], ri["window"]) == (0.0, 40, 40), str(ri))
    chk("N5 OTHER WAY: the N3 tape did NOT read 0.0", r["nobody"] != 0.0)

    # N6 -- EMPTY-WINDOW and NEVER-ARRIVED ------------------------------------
    r0 = fold(_rows(lambda i: 1 if i >= 20 else 0, 100, sent_at=20))
    chk("N6 arrive == sent -> window 0 and share None, not 0",
        (r0["window"], r0["nobody"]) == (0, None), str(r0))
    chk("N6 never arrived -> dropped (None), not a zero row",
        fold(_rows(lambda i: 0, 100, sent_at=60)) is None)
    rnb = fold(_rows(lambda i: 1 if i >= 20 else 0, 100, sent_at=None))
    chk("N6 never bought a sentinel -> window runs to the last round",
        (rnb["sent"], rnb["window"], rnb["bought_sentinel"]) == (-1, 80, 0),
        str(rnb))

    # N9 -- THE TWO RING ENVELOPES, enumerated and driven both ways ----------
    from ringwalk import dsq_core, dsq_centre
    o = (10, 10)
    fp = {(x, y) for x in range(22) for y in range(22)
          if dsq_core((x, y), o) <= 8}
    ct = {(x, y) for x in range(22) for y in range(22)
          if dsq_centre((x, y), o) <= 8}
    chk("N9 the CENTRE envelope is 24 tiles, the FOOTPRINT one 49",
        (len(ct), len(fp)) == (24, 49), "%d / %d" % (len(ct), len(fp)))
    chk("N9 footprint STRICTLY CONTAINS centre (0 centre-only tiles)",
        ct < fp and not (ct - fp), "%d footprint-only tiles" % len(fp - ct))
    chk("N9 OTHER WAY: a named tile is in footprint and NOT in centre",
        (12, 13) in fp and (12, 13) not in ct,
        "dsq_core=%d dsq_centre=%.2f" % (dsq_core((12, 13), o),
                                         dsq_centre((12, 13), o)))
    chk("N9 OTHER WAY: a tile outside BOTH is outside both",
        (0, 0) not in fp and (0, 0) not in ct)
    r_fp = fold(_rows(lambda i: 1 if i >= 20 else 0, 100, sent_at=60),
                {i: 1 for i in range(0, 100)})
    r_nofp = fold(_rows(lambda i: 1 if i >= 20 else 0, 100, sent_at=60))
    chk("N9 nobody_fp is filled when the footprint pass is supplied",
        r_fp["nobody_fp"] == 0.0 and r_fp["ge1_fp"] == 40, str(r_fp["nobody_fp"]))
    chk("N9 OTHER WAY: it is None (not 0) when the pass is NOT supplied",
        r_nofp["nobody_fp"] is None and r_nofp["ge1_fp"] is None)

    # N8a -- THE KILL-CLOCK OFFSET, driven both ways synthetically -----------
    rk = fold(_rows(lambda i: 1 if i >= 20 else 0, 100, sent_at=60,
                    kill_at=80))
    chk("N8a a grid turn of 81 against replay round 80 is the KNOWN offset 1",
        81 - rk["kill"] == KILL_OFFSET, "offset %d" % (81 - rk["kill"]))
    chk("N8a OTHER WAY: a grid turn of 85 is NOT the known offset (would alarm)",
        85 - rk["kill"] != KILL_OFFSET, "offset %d" % (85 - rk["kill"]))
    chk("N8a OTHER WAY: equal clocks (turn 80) would also alarm",
        80 - rk["kill"] != KILL_OFFSET)

    # N7 -- REAL-DATA TEAM-SWAP POSITIVE CONTROL ------------------------------
    rp = _pick_real()
    if rp is None:
        print("  [skip] N7: no map-tagged replay available")
    else:
        path, _m, seat = rp
        our = 0 if seat == "A" else 1
        a = fold(Tape(path, our).rows)
        b = fold(Tape(path, 1 - our).rows)
        if a is None or b is None:
            chk("N7 team-swap MOVES the window/share",
                (a is None) != (b is None),
                "one side never arrived: as-played=%s swapped=%s"
                % (a is not None, b is not None))
        else:
            moved = [k for k in ("arrive", "sent", "window", "ge1", "nobody")
                     if a[k] != b[k]]
            chk("N7 team-swap MOVES the window/share", len(moved) >= 2,
                str(moved))
            print("      as-played (team %d): %s" % (our, a))
            print("      swapped   (team %d): %s" % (1 - our, b))

    print("=== nobody selftest %s ===" % ("PASS" if ok else "FAIL"))
    return ok


# =============================== DRIVERS =====================================

def run(grid_tsv, repdir, out_tsv, label=""):
    from collections import Counter
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    out, dropped, alarms = [], 0, []
    offsets = Counter()
    for g in rows:
        p = Path(repdir) / (g["tag"] + ".replay26")
        if not p.exists():
            continue
        our = 0 if g["seat"] == "A" else 1
        t = Tape(p, our)
        r = fold(t.rows, near_footprint(p, our))
        if r is None:
            dropped += 1
            continue
        # N8b THE NESTING GUARD.  The footprint envelope strictly contains the
        # centre one, so ge1_fp >= ge1 in EVERY game.  A violation means the
        # two walkers disagree about which team or which core is ours.
        if r["ge1_fp"] is not None and r["ge1_fp"] < r["ge1"]:
            alarms.append("%s: ge1_fp %d < ge1 %d -- the envelopes are nested "
                          "the other way, the walkers disagree"
                          % (g["tag"], r["ge1_fp"], r["ge1"]))
        # N8 REAL-DATA CROSS-CHECK, on every game rather than asserted once
        won_by_kill = (g["ours"] == "US"
                       and g["cond"].startswith("Core destroyed"))
        if won_by_kill:
            off = int(g["turn"]) - r["kill"]
            offsets[off] += 1
            if off != KILL_OFFSET:
                alarms.append("%s: replay kill r%s vs grid turn %s (offset %d, "
                              "expected %d)"
                              % (g["tag"], r["kill"], g["turn"], off,
                                 KILL_OFFSET))
        if (not won_by_kill) and r["kill"] >= 0:
            alarms.append("%s: replay says enemy core died at r%s but the grid "
                          "does not call it our core-destroyed win (%s/%s)"
                          % (g["tag"], r["kill"], g["ours"], g["cond"]))
        out.append(dict(tag=g["tag"], map=g["map"], seed=g["seed"],
                        seat=g["seat"], ours=g["ours"], cond=g["cond"],
                        turn=g["turn"], arm=label, **r))
    if alarms:
        sys.stderr.write("INSTRUMENT ALARM (kill cross-check):\n  "
                         + "\n  ".join(alarms[:20]) + "\n")
        raise SystemExit(3)
    if not out:
        raise SystemExit("no games with an arrival in %s" % repdir)
    cols = list(out[0].keys())
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for x in out:
            fh.write("\t".join("" if x[c] is None else str(x[c])
                               for c in cols) + "\n")
    sys.stderr.write("nobody: %d games (%d never arrived, dropped and counted)"
                     " -> %s\n  kill cross-check: %d core-kill wins, grid-turn "
                     "minus replay-round offsets %s (all must be %d)\n"
                     % (len(out), dropped, out_tsv, sum(offsets.values()),
                        dict(offsets), KILL_OFFSET))
    return out, dropped


def report(paths):
    rows = []
    for p in paths:
        rows += list(csv.DictReader(open(p), delimiter="\t"))
    by = {}
    for r in rows:
        by.setdefault(r.get("arm", ""), []).append(r)
    print("%-14s %5s %9s %10s %10s %9s %9s %9s" %
          ("arm", "n", "window", "NOBODY_c", "NOBODY_fp", "ge1/win", "2body",
           "bought%"))
    for arm, rr in sorted(by.items()):
        wins = [int(r["window"]) for r in rr]
        nb = [float(r["nobody"]) for r in rr if r["nobody"]]
        nbf = [float(r["nobody_fp"]) for r in rr if r.get("nobody_fp")]
        tb = [float(r["two_body_share"]) for r in rr if r["two_body_share"]]
        g1 = sum(int(r["ge1"]) for r in rr)
        wsum = sum(wins)
        bought = sum(int(r["bought_sentinel"]) for r in rr)
        print("%-14s %5d %9.1f %10.4f %10.4f %9.4f %9.4f %8.1f%%" %
              (arm or "-", len(rr), st.mean(wins),
               st.mean(nb) if nb else -1,
               st.mean(nbf) if nbf else -1,
               (g1 / wsum) if wsum else -1,
               st.mean(tb) if tb else -1,
               100.0 * bought / len(rr)))
    print("\n  NOBODY_c  = 1 - (window rounds with >=1 of our builder bots "
          "inside d^2<=8 of the enemy core CENTRE) / window -- gapdecomp's "
          "own radius.\n  NOBODY_fp = the same on the FOOTPRINT envelope "
          "(siege.FS_RING_DSQ, 49 tiles vs 24); THIS is the one comparable to "
          "a GAP518 stderr tape.\n  Per-game means; ge1/win is the "
          "round-weighted pool on the centre radius.  Window = [arrive, sent) "
          "or [arrive, last] when no forward sentinel is ever bought.")


def join(grid_tsv, repdir, logdir):
    """Print the replay-side share beside gapdecomp's stderr NOBODY."""
    import gapdecomp
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    n_line = n_win = n_nb_err = n_nb_rep = n_nb_fp = 0
    seen = 0
    cell = {"line+fp": 0, "line-fp": 0, "noline+fp": 0, "noline-fp": 0}
    for g in rows:
        p = Path(repdir) / (g["tag"] + ".replay26")
        if not p.exists():
            continue
        our = 0 if g["seat"] == "A" else 1
        t = Tape(p, our)
        fp = near_footprint(p, our)
        r = fold(t.rows, fp)
        if r is None:
            continue
        gap = gapdecomp.read_gap(Path(logdir) / (g["tag"] + ".err"))
        end = r["sent"] if r["sent"] >= 0 else r["last"] + 1
        inwin = sum(1 for x in range(r["arrive"], end) if x in gap)
        for x in range(r["arrive"], end):
            k = ("line" if x in gap else "noline") + \
                ("+fp" if fp.get(x, 0) >= 1 else "-fp")
            cell[k] += 1
        seen += 1
        n_win += r["window"]
        n_line += inwin
        n_nb_err += r["window"] - inwin
        n_nb_rep += r["window"] - r["ge1"]
        n_nb_fp += r["window"] - r["ge1_fp"]
    if not seen:
        print("no games")
        return
    print("games %d  window rounds %d" % (seen, n_win))
    if n_line == 0:
        # ⛔ A BLIND INSTRUMENT AND A 100% NOBODY ARE BYTE-IDENTICAL HERE.
        # Refuse the number rather than print 1.0000.
        print("  stderr GAP518 lines in window : 0 -> ⛔ NO STDERR TAPE IN THIS "
              "ARM.  gapdecomp is NOT RUNNABLE here and NOBODY(stderr) is "
              "REFUSED, not reported as 1.0 -- a blind instrument and a 100% "
              "NOBODY are the same bytes.  This is the reason nobody.py exists.")
    else:
        print("  stderr GAP518 lines in window : %d  -> NOBODY(stderr) = %.4f"
              % (n_line, n_nb_err / n_win))
    print("  replay CENTRE    ge1 rounds   : %d  -> NOBODY(replay,centre) = %.4f"
          % (n_win - n_nb_rep, n_nb_rep / n_win))
    print("  replay FOOTPRINT ge1 rounds   : %d  -> NOBODY(replay,fp)     = %.4f"
          "   <-- THE COMPARABLE ONE (same envelope the GAP518 line fires in)"
          % (n_win - n_nb_fp, n_nb_fp / n_win))
    print("  2x2 contingency, window rounds: %s" % cell)
    print("  ⛔ CENTRE vs FOOTPRINT: `Tape.near_bot` tests d^2<=8 to the core "
          "CENTRE (24 tiles); `siege.FS_RING_DSQ` tests the FOOTPRINT-aware "
          "dsq_core (49 tiles) and is what the GAP518 line fires under.  The "
          "footprint envelope strictly contains the centre one, so "
          "NOBODY(centre) >= NOBODY(fp) always.  Compare a stderr tape ONLY to "
          "NOBODY(replay,fp).  `line-fp` rounds (a line with no body inside "
          "even the footprint envelope) are the residual seam and are the "
          "cell to watch.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "--selftest":
        raise SystemExit(0 if selftest() else 1)
    elif a[0] == "--report":
        report(a[1:])
    elif a[0] == "--join":
        join(a[1], a[2], a[3])
    else:
        run(a[0], a[1], a[2], a[3] if len(a) > 3 else "")
