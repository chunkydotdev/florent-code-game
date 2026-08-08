#!/usr/bin/env python3
"""Interleaved same-batch runner: every candidate plays a fixed opponent on the
SAME (map, seed, seat) grid inside one batch. This is one of the two accepted
shapes for holder/parent comparisons (docs/tooling.md): cross-batch 120-game
legs spread ~10pp same-binary, so deltas between separately-run batches are
not currency — interleave the variants or pair deterministically (tools/det.py).

Usage:
  .venv/bin/python tools/pair.py tag1=bots/cand1[,tag2=bots/cand2,...] <opp_dir> [seeds=4] [map1,map2,...]

Env: PAIR_TLE (default 10), PAIR_JOBS (default 5), PAIR_OUT (json dump path,
default ./pair_results.json).

Promoted from the s15 builder scratchpad (validated 2026-08-08); the s15
version's piece-U famine instrumentation was dropped as U-specific.

CHANNEL CAVEAT on the tb column: it counts "Traceback" occurrences in the
game's SHARED stderr. Both our lineage and x3r0's carry the v1-heritage
caught-exception handler that prints traceback.print_exc once per unit
lifetime WITHOUT the unit dying — so tb counts caught-diagnostic prints from
EITHER side, not unit deaths (theme-2 channel rule; same confusion as the
arena crash counter). Attribute via the file paths in the traceback text
before reading tb as crashes.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"


def play(job):
    tag, bot, opp, mp, seed, seat, tle = job
    a, b = (bot, opp) if seat == "a" else (opp, bot)
    cmd = [str(FCODE), "run", a, b, mp, "--seed", str(seed), "--tle", str(tle),
           "--json", "--replay", "/dev/null"]
    pr = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    res = None
    for line in reversed(pr.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except Exception:
                pass
    if res is None:
        return None
    us, them = ("a", "b") if seat == "a" else ("b", "a")
    return dict(tag=tag, map=Path(mp).stem, seed=seed, seat=seat,
                win=res["winner"].lower() == seat,
                turns=res["turns"], cond=res["win_condition"],
                ti_us=res[f"{us}_titanium_collected"], ti_them=res[f"{them}_titanium_collected"],
                units_us=res[f"{us}_units"], bld_us=res[f"{us}_buildings"],
                tb=pr.stderr.count("Traceback"))


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: pair.py tag=path[,tag=path...] <opp_dir> [seeds] [map1,map2,...]")
    cands = sys.argv[1].split(",")
    opp = sys.argv[2]
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    mapsel = sys.argv[4].split(",") if len(sys.argv) > 4 else None
    maps = sorted((ROOT / "maps").glob("*.map26"))
    if mapsel:
        maps = [m for m in maps if m.stem in mapsel]
    tle = int(os.environ.get("PAIR_TLE", "10"))
    workers = int(os.environ.get("PAIR_JOBS", "5"))
    jobs = []
    for mp in maps:
        for seed in range(1, seeds + 1):
            for seat in ("a", "b"):
                for c in cands:
                    tag, path = c.split("=", 1)
                    jobs.append((tag, path, opp, str(mp), seed, seat, tle))
    out = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                out.append(r)
            if i % 25 == 0:
                print(f"\r  {i}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    with open(os.environ.get("PAIR_OUT", "pair_results.json"), "w") as f:
        json.dump(out, f)
    for c in cands:
        t = c.split("=", 1)[0]
        rows = [r for r in out if r["tag"] == t]
        n = len(rows)
        if not n:
            print(f"{t:>8}: no completed games")
            continue
        w = sum(r["win"] for r in rows)
        long_ = [r for r in rows if r["turns"] >= 1000]
        lw = sum(r["win"] for r in long_)
        print(f"{t:>8}: {w}/{n} = {w/n:.1%}  | r1000 games {len(long_)} won {lw} "
              f"| tracebacks {sum(r['tb'] for r in rows)} "
              f"| median turns {sorted(r['turns'] for r in rows)[n//2]}")


if __name__ == "__main__":
    main()
