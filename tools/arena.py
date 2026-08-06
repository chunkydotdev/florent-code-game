#!/usr/bin/env python3
"""Run two bots against each other many times and report who's actually better.

Why this exists: a single match proves nothing here. Identical bots have been
measured finishing 0-units vs 10 purely on variance. Any "is v2 better than v1?"
question needs tens of matches across several maps before the answer means anything.

What it does:
  - plays every (map x seed) pairing in BOTH seat orderings, because Team A acts
    first every round and that is not a symmetric advantage
  - runs matches in parallel
  - counts uncaught-exception crashes per bot, attributed by traceback path
  - reports a win rate with a Wilson 95% interval, and refuses to call a winner
    when the interval still straddles 50%

Usage:
    python3 tools/arena.py starter starter                 # measure the noise floor
    python3 tools/arena.py v1 starter --seeds 8            # is v1 better than baseline?
    python3 tools/arena.py v1 starter --maps duel16 mid20 --seeds 20 --jobs 8
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"


def wilson(wins: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% confidence interval for a win rate. Honest about small samples."""
    if n == 0:
        return (0.0, 1.0)
    p = wins / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def play(job):
    """One match. Returns (winner_bot_name, map, seed, crashes_by_bot, detail)."""
    bot_a, bot_b, map_path, seed, tle = job
    cmd = [
        str(FCODE), "run", bot_a, bot_b, map_path,
        "--seed", str(seed), "--tle", str(tle), "--json", "--replay", "/dev/null",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)

    result = None
    for line in reversed(proc.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                result = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    if result is None or "winner" not in result:
        return None

    # Attribute crashes by which bot's source path appears in each traceback.
    crashes = Counter()
    for block in proc.stderr.split("Traceback (most recent call last)"):
        if "Error" not in block:
            continue
        for name, seat in ((bot_a, "a"), (bot_b, "b")):
            if f"bots/{name}/" in block:
                crashes[seat] += 1
                break

    seat = result["winner"].lower()  # "a" or "b"
    winner = bot_a if seat == "a" else bot_b
    return {
        "winner": winner,
        "seat": seat,
        "map": Path(map_path).stem,
        "seed": seed,
        "bot_a": bot_a,
        "bot_b": bot_b,
        "condition": result.get("win_condition"),
        "crashes": dict(crashes),
        "collected": (result.get("a_titanium_collected"), result.get("b_titanium_collected")),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bot_a")
    ap.add_argument("bot_b")
    ap.add_argument("--maps", nargs="*", default=None, help="map names (default: all in maps/)")
    ap.add_argument("--seeds", type=int, default=4, help="seeds per map per ordering (default 4)")
    ap.add_argument("--tle", type=int, default=10, help="per-turn CPU limit in ms (default 10)")
    ap.add_argument("--jobs", type=int, default=0, help="parallel matches (default: cores-2)")
    args = ap.parse_args()

    maps_dir = ROOT / "maps"
    if args.maps:
        maps = [maps_dir / f"{m}.map26" if not m.endswith(".map26") else Path(m) for m in args.maps]
    else:
        maps = sorted(maps_dir.glob("*.map26"))
    if not maps:
        sys.exit("no maps found — run: python3 tools/make_map.py")

    jobs = []
    for mp in maps:
        for seed in range(1, args.seeds + 1):
            # Both orderings: Team A acts first, so seat matters.
            jobs.append((args.bot_a, args.bot_b, str(mp), seed, args.tle))
            jobs.append((args.bot_b, args.bot_a, str(mp), seed, args.tle))

    workers = args.jobs or max(1, (__import__("os").cpu_count() or 4) - 2)
    print(f"{len(jobs)} matches — {len(maps)} maps x {args.seeds} seeds x 2 orderings, {workers} parallel\n")

    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                results.append(r)
            print(f"\r  {i}/{len(jobs)}", end="", flush=True)
    print("\n")

    if not results:
        sys.exit("every match failed to produce a result")

    a, b = args.bot_a, args.bot_b
    wins = Counter(r["winner"] for r in results)
    n = len(results)
    crashes = Counter()
    for r in results:
        for seat, count in r["crashes"].items():
            crashes[r[f"bot_{seat}"]] += count

    if a == b:
        # Mirror match: names collide, so nothing is attributable by name.
        # The only meaningful signal is the seat split.
        print(f"  mirror match: {a} vs itself, {n} matches")
    else:
        print(f"  {a}: {wins[a]} wins        {b}: {wins[b]} wins        ({n} matches)")
    if a != b:
        lo, hi = wilson(wins[a], n)
        print(f"  {a} win rate: {wins[a]/n:.1%}   95% CI [{lo:.1%}, {hi:.1%}]")
        if lo > 0.5:
            print(f"  --> {a} is better. The interval clears 50%.")
        elif hi < 0.5:
            print(f"  --> {b} is better. The interval clears 50%.")
        else:
            need = math.ceil(n * ((hi - lo) / 0.10) ** 2)
            print(f"  --> No verdict: the interval still straddles 50%. "
                  f"Roughly {need} matches would halve it.")
    print(f"\n  crashes (uncaught exceptions, each one permanently kills a unit):")
    if a == b:
        print(f"    {crashes[a]} total (not attributable — both seats are the same bot)")
    else:
        for bot in dict.fromkeys([a, b]):
            print(f"    {bot}: {crashes[bot]}")

    print(f"\n  win conditions:")
    for cond, c in Counter(r["condition"] for r in results).most_common():
        print(f"    {cond}: {c}")

    # Seat bias is strongly map-dependent, so ALWAYS report it per map. The pooled
    # number is misleading: maps where seat A goes 0/16 average against fair maps
    # and produce a middling figure that describes none of them.
    print(f"\n  by map (seat A = acts first; with identical bots this should sit near 50%):")
    for mp in sorted({r["map"] for r in results}):
        rows = [r for r in results if r["map"] == mp]
        sa = sum(1 for r in rows if r["seat"] == "a")
        lo, hi = wilson(sa, len(rows))
        flag = "" if lo <= 0.5 <= hi else "   <-- seat decides this map"
        line = f"    {mp:<12} seatA {sa}/{len(rows)} = {sa/len(rows):>5.1%} [{lo:.0%}, {hi:.0%}]{flag}"
        if a != b:
            line += f"    {a} {sum(1 for r in rows if r['winner'] == a)}/{len(rows)}"
        print(line)

    seat_a = sum(1 for r in results if r["seat"] == "a")
    print(f"\n  seat bias pooled: {seat_a}/{n} = {seat_a/n:.1%} — read the per-map rows "
          f"above instead, this average hides the split.")
    print("  Every pairing is played in both orderings, so seat cancels out of the "
          "win rate regardless.")


if __name__ == "__main__":
    main()
