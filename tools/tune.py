#!/usr/bin/env python3
"""CEM tuner for bot constants, driven by arena win rate against a fixed opponent.

Why CEM and not gradient anything: the objective is a noisy win rate from whole
matches (identical bots have finished 0-units vs 10), the parameter space is ~8
scalars, and evaluations are expensive (~1 min per 60-match screen). The
cross-entropy method with per-generation ranking tolerates exactly this: noise
averages out across generations, and no single lucky screen can do more than
nudge the sampling distribution.

What it does:
  1. Reads a params spec (JSON): module-level constants in the base bot's
     main.py, with ranges. See tools/tune_params.json.
  2. Each generation, samples POP candidate parameter vectors from clipped
     normals, materialises each as bots/_tune_<i> (text substitution of the
     `NAME = value` lines), and screens each against the opponent via arena.py.
  3. Ranks by win rate, refits mean/sigma to the elite quartile, repeats.
  4. Final winner gets a full confirm run, plus no-collapse checks against the
     guard opponents — a tuned bot that overfits its tuning opponent and folds
     against the field is a discard, per program.md.

The tuner NEVER edits the base bot, the harness, or maps/ — candidates live in
bots/_tune_* and are deleted afterwards. Accept/activation decisions stay with
the humans; this prints numbers.

Usage:
  .venv/bin/python tools/tune.py BASE_BOT OPPONENT \
      [--spec tools/tune_params.json] [--gens 12] [--pop 12] \
      [--screen-seeds 2] [--confirm-seeds 16] [--jobs 0] \
      [--guards starter opp_v39] [--maps ...]

Every generation is appended to results.tsv-adjacent log tune_log.tsv (kept
untracked, like results.tsv): generation, candidate params, screen rate.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON = ROOT / ".venv" / "bin" / "python"
ARENA = ROOT / "tools" / "arena.py"

RATE_RE = re.compile(r"win rate: ([0-9.]+)%\s+95% CI \[([0-9.]+)%, ([0-9.]+)%\]")


def load_spec(path: Path) -> list[dict]:
    spec = json.loads(path.read_text())
    for p in spec:
        assert {"name", "lo", "hi", "type"} <= set(p), f"bad spec entry: {p}"
        assert p["type"] in ("int", "float")
    return spec


def materialise(base_src: str, params: dict[str, float], dest: Path) -> None:
    """Write a candidate bot: base main.py with constant lines substituted."""
    src = base_src
    for name, value in params.items():
        pattern = re.compile(rf"^{name} = .*$", re.MULTILINE)
        if not pattern.search(src):
            raise SystemExit(f"constant {name} not found as a module-level assignment")
        src = pattern.sub(f"{name} = {value!r}", src, count=1)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "main.py").write_text(src)


def arena(bot_a: str, bot_b: str, seeds: int, jobs: int, maps: list[str]) -> tuple[float, float, float] | None:
    """Run arena, return (rate, lo, hi) for bot_a, or None on failure."""
    cmd = [str(PYTHON), str(ARENA), bot_a, bot_b, "--seeds", str(seeds)]
    if jobs:
        cmd += ["--jobs", str(jobs)]
    if maps:
        cmd += ["--maps", *maps]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    m = RATE_RE.search(proc.stdout)
    if not m:
        print(proc.stdout[-500:], file=sys.stderr)
        return None
    return tuple(float(g) / 100 for g in m.groups())


def sample(spec, mean, sigma, rng):
    out = {}
    for p in spec:
        v = rng.gauss(mean[p["name"]], sigma[p["name"]])
        v = max(p["lo"], min(p["hi"], v))
        out[p["name"]] = round(v) if p["type"] == "int" else round(v, 3)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base")
    ap.add_argument("opponent")
    ap.add_argument("--spec", default="tools/tune_params.json")
    ap.add_argument("--gens", type=int, default=12)
    ap.add_argument("--pop", type=int, default=12)
    ap.add_argument("--elite", type=float, default=0.25)
    ap.add_argument("--screen-seeds", type=int, default=2)
    ap.add_argument("--confirm-seeds", type=int, default=16)
    ap.add_argument("--jobs", type=int, default=0)
    ap.add_argument("--guards", nargs="*", default=["starter"],
                    help="opponents the winner must not collapse against")
    ap.add_argument("--maps", nargs="*", default=None)
    ap.add_argument("--seed", type=int, default=0, help="tuner RNG seed")
    args = ap.parse_args()

    spec = load_spec(ROOT / args.spec)
    base_src = (ROOT / "bots" / args.base / "main.py").read_text()
    rng = random.Random(args.seed)
    log = (ROOT / "tune_log.tsv").open("a")

    # Initial distribution: mean at the base bot's current values, sigma = range/4.
    mean, sigma = {}, {}
    for p in spec:
        m = re.search(rf"^{p['name']} = ([0-9.]+)$", base_src, re.MULTILINE)
        mean[p["name"]] = float(m.group(1)) if m else (p["lo"] + p["hi"]) / 2
        sigma[p["name"]] = (p["hi"] - p["lo"]) / 4

    best = None  # (rate, params)
    for gen in range(1, args.gens + 1):
        scored = []
        for i in range(args.pop):
            params = sample(spec, mean, sigma, rng)
            name = f"_tune_{i}"
            materialise(base_src, params, ROOT / "bots" / name)
            r = arena(name, args.opponent, args.screen_seeds, args.jobs, args.maps)
            rate = r[0] if r else 0.0
            scored.append((rate, params))
            print(f"gen {gen} cand {i}: {rate:.1%}  {params}", flush=True)
            log.write(f"{gen}\t{i}\t{rate:.4f}\t{json.dumps(params)}\n")
            log.flush()
        scored.sort(key=lambda t: -t[0])
        elite = scored[: max(2, int(args.pop * args.elite))]
        if best is None or elite[0][0] > best[0]:
            best = elite[0]
        # Refit mean/sigma to the elite; floor sigma so exploration never dies.
        for p in spec:
            vals = [e[1][p["name"]] for e in elite]
            mu = sum(vals) / len(vals)
            var = sum((v - mu) ** 2 for v in vals) / len(vals)
            mean[p["name"]] = mu
            sigma[p["name"]] = max(var ** 0.5, (p["hi"] - p["lo"]) / 20)
        print(f"== gen {gen} done. elite mean rate {sum(e[0] for e in elite)/len(elite):.1%}, "
              f"mean={ {k: round(v, 2) for k, v in mean.items()} }", flush=True)

    # Final confirm of the best candidate seen, plus guard checks.
    print(f"\nBest screened candidate: {best[0]:.1%}  {best[1]}", flush=True)
    materialise(base_src, best[1], ROOT / "bots" / "_tune_best")
    r = arena("_tune_best", args.opponent, args.confirm_seeds, args.jobs, args.maps)
    print(f"CONFIRM vs {args.opponent}: rate={r[0]:.1%} CI [{r[1]:.1%}, {r[2]:.1%}]"
          + ("  -> clears the gate" if r[1] > 0.5 else "  -> no verdict / not better"), flush=True)
    for g in args.guards:
        rg = arena("_tune_best", g, 8, args.jobs, args.maps)
        print(f"GUARD vs {g}: rate={rg[0]:.1%} CI [{rg[1]:.1%}, {rg[2]:.1%}]"
              + ("  COLLAPSE — discard" if rg[2] < 0.5 else "  ok"), flush=True)

    print("\nCandidate left in bots/_tune_best (params above). Cleaning the rest.")
    for d in (ROOT / "bots").glob("_tune_[0-9]*"):
        shutil.rmtree(d)
    log.close()


if __name__ == "__main__":
    main()
