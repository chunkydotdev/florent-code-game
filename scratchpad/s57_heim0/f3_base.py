"""f3_base.py -- F3 (Sleipnir v2 / rush-class) baseline readout.

GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition on a simulated grid under organiser-approved
rules. "core death"/"knocked out" = in-engine removal of a competing game bot's
piece per the engine's documented rules, nothing else.

Decoder: scratchpad/s54_klad_lib.Game (the validated event walker). No second
decoder is hand-rolled. Seat convention taken from scratchpad/s57_v630/e46_lib:
us = 0 for *_seatA.replay26, 1 for *_seatB.replay26.

Usage: .venv/bin/python scratchpad/s57_heim0/f3_base.py <tape-dir>
"""
from __future__ import annotations

import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "scratchpad")
sys.path.insert(0, "tools")
from s54_klad_lib import Game  # noqa: E402

R_BAR = 300


def log_line(path, prefix):
    for line in path.with_suffix(".log").read_text(errors="replace").splitlines():
        s = line.strip()
        if s.startswith(prefix):
            return s
    return ""


def main(tape):
    root = Path(tape)
    rows = []
    for p in sorted(root.glob("*.replay26")):
        us = 0 if p.stem.endswith("seatA") else 1
        g = Game(p)
        our_core = g.core_id(us)
        opp_core = g.core_id(1 - us)
        our_death = g.died.get(our_core)
        opp_death = g.died.get(opp_core)
        harv = sum(1 for rnd, kind, pl in g.ev
                   if kind == "BUILD" and pl[1] == us and pl[2] == "harvester")
        rows.append({
            "cell": p.stem,
            "rounds": g.rounds,
            "won": g.winner == us,
            "cond": g.wincond,
            "our_death": our_death,
            "opp_death": opp_death,
            "harv": harv,
            "alive300": our_death is None or our_death > R_BAR,
            "winner_line": log_line(p, "Winner:"),
        })

    n = len(rows)
    print(f"TAPE {root}   cells={n}")
    print()
    print(f"{'cell':<24}{'rnds':>6}{'res':>5}{'ourCoreDeath':>14}"
          f"{'oppCoreDeath':>14}{'harv':>6}  cond")
    for r in rows:
        print(f"{r['cell']:<24}{r['rounds']:>6}{('W' if r['won'] else 'L'):>5}"
              f"{str(r['our_death']):>14}{str(r['opp_death']):>14}"
              f"{r['harv']:>6}  {r['cond']}")
    print()

    alive = [r for r in rows if r["alive300"]]
    print(f"P(our core alive at r{R_BAR})        = {len(alive)}/{n}")
    at_bar = [r for r in rows if r["our_death"] == R_BAR]
    print(f"  (boundary: deaths exactly at r{R_BAR} = {len(at_bar)})")

    deaths = sorted(r["our_death"] for r in rows if r["our_death"] is not None)
    print(f"our-core death rounds ({len(deaths)}/{n} games): {deaths}")
    print(f"  median = {statistics.median(deaths) if deaths else 'n/a'}")
    print(f"  survivors (core never removed) = {n - len(deaths)}")

    hs = [r["harv"] for r in rows]
    print(f"our harvesters built per game: mean={statistics.mean(hs):.2f} "
          f"max={max(hs)} min={min(hs)} total={sum(hs)}")

    lens = sorted(r["rounds"] for r in rows)
    print(f"game length (replay turns): median={statistics.median(lens)} "
          f"min={lens[0]} max={lens[-1]}")

    print()
    print("win/loss x condition:")
    tab = Counter((("WIN" if r["won"] else "LOSS"), r["cond"]) for r in rows)
    for (res, cond), c in sorted(tab.items()):
        print(f"  {res:<5} {cond:<24} {c}")
    print(f"  TOTAL WINS  {sum(1 for r in rows if r['won'])}/{n}")

    print()
    print("by seat:")
    for seat, tag in ((0, "seatA"), (1, "seatB")):
        sub = [r for r in rows if r["cell"].endswith(tag)]
        w = sum(1 for r in sub if r["won"])
        a = sum(1 for r in sub if r["alive300"])
        print(f"  {tag}: wins {w}/{len(sub)}   alive@r{R_BAR} {a}/{len(sub)}")

    # DECODER CROSS-CHECK: the replay-derived result must agree with the
    # engine's own per-cell "Winner:" line (an independent channel).
    print()
    bad = 0
    for r in rows:
        wl = r["winner_line"]
        ours = "_v628compose" in wl.split("(")[0]
        if ours != r["won"]:
            bad += 1
            print(f"  MISMATCH {r['cell']}: decoded won={r['won']}  log={wl}")
    print(f"cross-check vs engine 'Winner:' lines: {n - bad}/{n} agree")


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main(sys.argv[1] if len(sys.argv) > 1 else "scratchpad/s57_heim0/t_ctrl_f3")
