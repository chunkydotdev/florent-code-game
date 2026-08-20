#!/usr/bin/env python3
"""v535 build instrument #4 -- FOLD THE DOSE TAPES, PER MAP CLASS.

Counts, per arm and per map, the stderr instrument lines the trees emit:
  CORNER   -- `V530 CORNER ...`, one per barrier actually built on one of OUR
              four diagonal core-ring corners
  V535GATE -- `V535GATE rnd=.. id=.. refuse=..`, one per unit that ASKED the
              gate (v535 arm only; the parent cannot emit it)

and prints the table the dose claim is made from:

    arm  class  map  games  corners  corners/game  gate_asks  refuse_asks

⛔ DRIVEN BOTH WAYS (`--selftest`).  Three synthetic tapes:
  1. a tape WITH corner lines            -> nonzero corner count
  2. the same tape with them REMOVED     -> exactly 0
  3. a tape carrying ONLY V535GATE lines -> 0 corners, nonzero gate asks
     (the two counters must not be aliases of one another)
plus a Traceback tape, which must be reported (a dose read off a tape full of
tracebacks is a dose read off a dead bot).

  .venv/bin/python .../doseread.py [--selftest]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORNER = re.compile(r"^V530 CORNER ")
GATE = re.compile(r"^V535GATE rnd=(\d+) id=(-?\d+) refuse=(\d)")
TB = re.compile(r"^Traceback")

REFUSING = {"archipelago", "midgard"}


def fold_text(text):
    o = defaultdict(int)
    for line in text.splitlines():
        line = line.strip()
        if CORNER.match(line):
            o["corner"] += 1
        m = GATE.match(line)
        if m:
            o["gate"] += 1
            o["refuse"] += int(m.group(3))
        if TB.match(line):
            o["tb"] += 1
    return o


def fold_dir(d):
    """{(map): counters} plus a per-GAME index for the paired comparison."""
    per_map = defaultdict(lambda: defaultdict(int))
    per_game = {}
    for p in sorted(Path(d).glob("*.err")):
        stem = p.stem                      # <map>_<seed>_<seat>
        mp = stem.rsplit("_", 2)[0]
        o = fold_text(p.read_text(errors="replace"))
        for k in ("corner", "gate", "refuse", "tb"):
            per_map[mp][k] += o[k]
        per_map[mp]["games"] += 1
        per_game[stem] = o["corner"]
    return per_map, per_game


def report(root=None):
    root = Path(root or (HERE / "dose"))
    arms = sorted(p.name for p in root.iterdir() if p.is_dir())
    if not arms:
        print("no dose tapes under %s" % root)
        return 1
    idx = {}
    print("%-11s %-8s %-13s %5s %8s %7s %6s %7s %4s"
          % ("arm", "class", "map", "games", "corners", "c/game",
             "gate", "refuse", "tb"))
    for arm in arms:
        per_map, per_game = fold_dir(root / arm)
        idx[arm] = per_game
        for mp in sorted(per_map):
            c = per_map[mp]
            cls = "REFUSE" if mp in REFUSING else "run"
            print("%-11s %-8s %-13s %5d %8d %7.2f %6d %7d %4d"
                  % (arm, cls, mp, c["games"], c["corner"],
                     c["corner"] / max(1, c["games"]), c["gate"],
                     c["refuse"], c["tb"]))
        # class totals
        for cls, sel in (("REFUSE", REFUSING), ("run", None)):
            g = cc = 0
            for mp, c in per_map.items():
                inref = mp in REFUSING
                if (cls == "REFUSE") != inref:
                    continue
                g += c["games"]; cc += c["corner"]
            print("%-11s %-8s %-13s %5d %8d %7.2f"
                  % (arm, cls, "== TOTAL ==", g, cc, cc / max(1, g)))

    # --- the PAIRED per-game comparison, which is the positive control ----
    if len(arms) == 2:
        a, b = arms
        common = sorted(set(idx[a]) & set(idx[b]))
        same_run = diff_run = same_ref = diff_ref = 0
        detail = []
        for k in common:
            mp = k.rsplit("_", 2)[0]
            eq = idx[a][k] == idx[b][k]
            if mp in REFUSING:
                same_ref += eq; diff_ref += (not eq)
            else:
                same_run += eq; diff_run += (not eq)
                if not eq:
                    detail.append((k, idx[a][k], idx[b][k]))
        print("\nPAIRED PER-GAME CORNER COUNTS  (%s vs %s), NOISE_OFF" % (a, b))
        print("  RUNNING boards : %d of %d games IDENTICAL, %d differ"
              % (same_run, same_run + diff_run, diff_run))
        print("  REFUSING boards: %d of %d games differ, %d identical"
              % (diff_ref, same_ref + diff_ref, same_ref))
        if detail:
            print("  running-board mismatches: %s" % (detail,))
    return 0


SYN_WITH = """V530 CORNER rnd=3 seat=1 tile=4,4 held=1
V530 CORNER rnd=5 seat=2 tile=6,4 held=2
V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=2 sock=3,3
V535GATE rnd=2 id=11 refuse=0
"""
SYN_WITHOUT = """V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=2 sock=3,3
V535GATE rnd=2 id=11 refuse=0
"""
SYN_GATEONLY = """V535GATE rnd=2 id=11 refuse=1
V535GATE rnd=2 id=12 refuse=1
"""
SYN_TB = """Traceback (most recent call last):
V530 CORNER rnd=3 seat=1 tile=4,4 held=1
"""


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    a = fold_text(SYN_WITH)
    check("mutant 1 tape WITH corner lines counts them", a["corner"], 2)
    check("mutant 1 also sees the gate line", a["gate"], 1)
    b = fold_text(SYN_WITHOUT)
    check("mutant 2 same tape, corner lines removed -> 0", b["corner"], 0)
    check("mutant 2 still sees the gate line (not an alias)", b["gate"], 1)
    c = fold_text(SYN_GATEONLY)
    check("mutant 3 gate-only tape: 0 corners", c["corner"], 0)
    check("mutant 3 gate-only tape: 2 gate asks", c["gate"], 2)
    check("mutant 3 gate-only tape: 2 REFUSE verdicts", c["refuse"], 2)
    check("mutant 3 the gate counter can also read 0 refusals",
          fold_text(SYN_WITH)["refuse"], 0)
    d = fold_text(SYN_TB)
    check("mutant 4 traceback tape is REPORTED", d["tb"], 1)
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    raise SystemExit(report(sys.argv[1] if len(sys.argv) > 1 else None))
