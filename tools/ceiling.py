#!/usr/bin/env python3
"""Price a change in the CEILING METRIC: core-kill rate and time-to-kill.

Why this exists (2026-08-08, session 20). The ladder census found that the
strong field ends ~90-100% of its games by CORE KILL at a median of ~120-250
turns, while OpenSverige ends 73% that way at a median of 312 and lets 28% of
games run to r1000. Every local instrument this project owns prices a plank in
WIN RATE (arena.py), FLIPS and DELIVERED TITANIUM (det.py). None of them can
see the ceiling metric at all — arena.py collects `win_condition` but prints it
pooled across both bots and never records `turns`, so "did this plank make us
kill cores faster?" has been unanswerable locally for the whole project.

This tool answers exactly that and nothing else. It is NOT a replacement for
arena.py: it does not adjudicate "is A better than B". Read it alongside arena,
not instead of it. A plank that raises win rate by grinding longer is a plank
that wins locally and loses to the field, and only this tool can tell you.

WHY IT IS A SEPARATE FILE: tools/arena.py is deny-listed for edits in
.claude/settings.json — the shared instrument is deliberately frozen so that
every verdict on the tape stays comparable. Adding a field to it would silently
re-baseline years of legs. So the ceiling metric lives here instead.

COUPLING WARNING: the `fcode run` invocation below is a deliberate byte-for-byte
copy of arena.play()'s command (arena.py:49-53) so that the two tools play the
SAME games. If arena's command ever changes, change this one in lockstep or the
two instruments stop being comparable.

Usage:
  .venv/bin/python tools/ceiling.py bots/_v99mag bots/opp_v76 --seeds 4
  .venv/bin/python tools/ceiling.py bots/_v99mag bots/opp_v76 --maps hive drumlin
"""
import argparse
import json
import math
import statistics
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"

# Reuse arena's Wilson interval verbatim so intervals on the two reports mean
# the same thing.
sys.path.insert(0, str(ROOT / "tools"))
from arena import wilson  # noqa: E402

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


def play(job):
    """One match. Returns winner/condition/turns, or None if the match failed."""
    bot_a, bot_b, map_path, seed, tle = job
    # See COUPLING WARNING in the module docstring before touching this.
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

    seat = result["winner"].lower()
    return {
        "winner": bot_a if seat == "a" else bot_b,
        "map": Path(map_path).stem,
        "condition": result.get("win_condition"),
        "turns": result.get("turns"),
    }


def metrics(name, rows):
    """Every number this tool reports for one bot, as data rather than print().

    Split out from report_bot so it is testable — see tests/test_instruments.py.
    The collider fixed on 2026-08-08 lived in this arithmetic and shipped because
    the arithmetic was welded to a print statement and could not be asserted on.
    """
    wins = [r for r in rows if r["winner"] == name]
    kills = [r for r in wins if r["condition"] == "core_destroyed"]
    n = len(rows)
    kill_ids = {id(r) for r in kills}
    # Censored: turns if THIS bot killed, else 1000. Denominator is every match.
    censored = sorted(r["turns"] if id(r) in kill_ids else 1000 for r in rows)
    return {
        "wins": wins,
        "kills": kills,
        "n_wins": len(wins),
        "n_kills": len(kills),
        "n_total": n,
        "kill_rate": len(kills) / n if n else 0.0,
        "conversion": len(kills) / len(wins) if wins else 0.0,
        "censored_median": statistics.median(censored) if censored else 0.0,
        # Conditional on having killed. A COLLIDER — never compare across bots.
        "kills_only_median": statistics.median([r["turns"] for r in kills]) if kills else None,
    }


def report_bot(name, rows, n_total):
    """Core-kill rate and time-to-kill for one bot, over every match it played."""
    m = metrics(name, rows)
    wins, kills = m["wins"], m["kills"]
    n_w, n_k = m["n_wins"], m["n_kills"]

    lo, hi = wilson(n_k, n_total)
    print(f"  {name}")
    print(f"    wins                {n_w}/{n_total} = {n_w / n_total:.1%}")
    # The ceiling metric. Denominator is ALL matches, not wins: a bot that wins
    # rarely but always by core kill is a different animal from one that wins
    # often by tiebreak, and dividing by wins hides exactly that difference.
    print(f"    CORE-KILL RATE      {n_k}/{n_total} = {n_k / n_total:.1%}   "
          f"95% CI [{lo:.1%}, {hi:.1%}]")
    if n_w:
        print(f"      (= {n_k / n_w:.0%} of its own wins)")
    # CENSORED kill-time: turns if THIS bot killed, else 1000. This is the
    # number to compare across bots.
    #
    # Why not the median over kills only (which is what this tool printed until
    # the instrument audit of 2026-08-08 caught it): conditioning on "we killed"
    # makes the statistic a COLLIDER. A bot that converts MORE games to kills
    # earns its extra kills on the hard, slow games, so improving kill rate
    # DRAGS THE CONDITIONAL MEDIAN UP and the tool reports the improvement as a
    # regression. Measured on a real leg: adding 3 slow kills moved kill rate
    # 25%->30% while the conditional median read 24 turns WORSE.
    #
    # Censoring at 1000 fixes the sign because the denominator is every match
    # either way. A bot that kills in under half its games reads 1000 — that is
    # honest, not a defect: its median game genuinely does not end in a kill.
    med = m["censored_median"]
    tag = "  (censored — >=half its games are not kills)" if med >= 1000 else ""
    print(f"    censored kill-time  median {med:.0f}{tag}")
    if kills:
        turns = sorted(r["turns"] for r in kills)
        # Kept for description only. NEVER compare this across bots — see above.
        print(f"    (of kills alone     median {statistics.median(turns):.0f}   "
              f"fastest {turns[0]}   slowest {turns[-1]}   COLLIDER, do not compare)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bot_a")
    ap.add_argument("bot_b")
    ap.add_argument("--maps", nargs="*", default=None)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--tle", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=0)
    args = ap.parse_args()

    maps_dir = ROOT / "maps"
    if args.maps:
        maps = [maps_dir / f"{m}.map26" if not m.endswith(".map26") else Path(m)
                for m in args.maps]
    else:
        maps = sorted(maps_dir.glob("*.map26"))
    if not maps:
        sys.exit("no maps found")

    jobs = []
    for mp in maps:
        for seed in range(1, args.seeds + 1):
            # Both orderings, exactly as arena does — seat is not symmetric.
            jobs.append((args.bot_a, args.bot_b, str(mp), seed, args.tle))
            jobs.append((args.bot_b, args.bot_a, str(mp), seed, args.tle))

    import os
    workers = args.jobs or max(1, (os.cpu_count() or 4) - 2)
    print(f"{len(jobs)} matches — {len(maps)} maps x {args.seeds} seeds x 2 orderings, "
          f"{workers} parallel\n")

    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                results.append(r)
            print(f"\r  {i}/{len(jobs)}", end="", flush=True)
    print("\n")

    if not results:
        sys.exit("every match failed to produce a result")

    n = len(results)
    a, b = args.bot_a, args.bot_b

    print("  CEILING METRIC — how games END, not who wins them\n")
    report_bot(a, results, n)
    if b != a:
        print()
        report_bot(b, results, n)

    # The field comparison that motivated this tool.
    kills = [r for r in results if r["condition"] == "core_destroyed"]
    full = [r for r in results if (r["turns"] or 0) >= 1000]
    lo, hi = wilson(len(kills), n)
    print(f"\n  BOTH SIDES POOLED (compare against the ladder census)")
    print(f"    games ended by core kill   {len(kills)}/{n} = {len(kills) / n:.1%}   "
          f"95% CI [{lo:.1%}, {hi:.1%}]")
    if kills:
        t = sorted(r["turns"] for r in kills)
        print(f"    median turns of those      {statistics.median(t):.0f}")
    print(f"    games reaching r1000       {len(full)}/{n} = {len(full) / n:.1%}")
    print(f"    top-tier ladder reference  ~90-100% core kill, median ~120-250 turns")
    print(f"    OpenSverige ladder ref     73% core kill, median 312 turns")

    print(f"\n  win conditions (all matches)")
    for cond, c in Counter(r["condition"] for r in results).most_common():
        print(f"    {cond}: {c}")

    # Core-kill rate is strongly map-dependent for the same reason win rate is,
    # so never read the pooled number alone.
    print(f"\n  by map (pooled core-kill rate, both sides)")
    for mp in sorted({r["map"] for r in results}):
        rows = [r for r in results if r["map"] == mp]
        k = [r for r in rows if r["condition"] == "core_destroyed"]
        med = f"{statistics.median([r['turns'] for r in k]):.0f}" if k else "—"
        print(f"    {mp:<14} {len(k)}/{len(rows)} = {len(k) / len(rows):>5.0%}   "
              f"median turns {med}")


if __name__ == "__main__":
    main()
