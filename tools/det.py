#!/usr/bin/env python3
"""Deterministic-paired A/B: run two candidates against a fixed opponent on
identical (map, seed, seat) triples at --tle 0 and account game-level FLIPS
and identical-end-state rates. This is the other accepted shape for
holder/parent comparisons (docs/tooling.md), and the only one that resolves
small effects: only paired same-(map,seed,seat) flips separate signal from the
~10pp cross-batch spread.

PRECONDITION the script measures but does not enforce: all sides must be
deterministic — flip NOISE_ON=False in local COPIES of the bots first (never
edit the canonical bots/ dirs for this), and use a deterministic opponent
(bots/opp_v63 is the measured reference; bots/starter is NOT deterministic).
--tle 0 removes CPU-kill nondeterminism.

Interpretation caveat (docs/tooling.md): det per-map flips are chaos-bounded —
identity (0-flip) results are gold; small flip counts are butterfly-sensitive
and must not be over-read as attribution.

Usage:
  .venv/bin/python tools/det.py tagA=bots/parent tagB=bots/cand <opp_dir> [seeds=8] [map1,map2,...]

Env: DET_JOBS (default 6), DET_OUT (json dump path, default ./det_results.json).

Promoted from the s15 builder scratchpad (validated 2026-08-08); the s15
version's hardcoded dA/dU piece-U harness became this CLI.

CHANNEL CAVEAT on the tb column: counts "Traceback" in SHARED stderr; both
lineages' run() handlers print caught tracebacks without the unit dying, so
tb = caught-diagnostic prints from either side, NOT unit deaths. Attribute
via file paths in the traceback text before reading tb as crashes.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

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

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"


# ===========================================================================
# THE NEUTRALISE-THEN-COMPARE PROCEDURE (s47 wrap debt 17, 2026-08-16)
# ===========================================================================
# ⛔ THE FACT THIS ENFORCES, read off the incumbent's own source rather than
# argued: `bots/_v468kladturbo/main.py:399` is
#
#     self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0
#
# `random.Random()` takes NO ARGUMENT, so it seeds from the OS. The engine's
# `--seed` has never reached our spawn ordering. `NOISE_ON = True` therefore
# makes a run UNREPRODUCIBLE, and any flag-off or matched-pair local
# equivalence check run in that state is measuring the RNG, not the flag.
#
# ⛔ AND THE OTHER HALF, or the remedy destroys the battery it fixes:
# `NOISE_ON = False` on BOTH sides makes games DEGENERATE — s32 measured
# 1 distinct outcome across 6 distinct seeds on 3 of 4 maps, i.e. a 1,024-row
# battery carrying ~8-16 distinct games while every denominator still printed
# 1,024. False => identical, True => unpairable. Neither is free.
#
# THE PROCEDURE, in order, and step 3 is the one people skip:
#   1. COPY the bots. Never edit a canonical `bots/` dir for a measurement.
#   2. Set NOISE_ON = False in EVERY side, ours and the opponent's, and use a
#      deterministic opponent (bots/opp_v63 is the measured reference;
#      bots/starter is NOT). Run at --tle 0.
#   3. RUN tools/effective_n.py ON THE RESULT. Pinning the RNG is what CAUSES
#      seed degeneracy, so the pinned battery is exactly the one whose
#      effective n must be measured before any denominator is quoted.
#   4. If the design is POOLED rather than paired, do not pin at all — take
#      gate.py's `--pooled-not-paired` escape with a typed reason instead.
#
# This module now REPORTS the state at startup instead of silently assuming
# it. Report, not refusal: det.py is also used to MEASURE how nondeterministic
# a pair is, and a hard refusal would forbid its own diagnostic use. Set
# DET_REQUIRE_DETERMINISM=1 to turn the report into an exit-2 refusal.
NOISE_TRUE_MARK = "NOISE_ON = True"
NOISE_ANY_MARK = "NOISE_ON"
RANDOM_MARK = "random."


def _bot_sources(bot: Path) -> str:
    """Every top-level .py in a bot dir, concatenated. Same shape as
    gate.py::_src — deliberately, so the two cannot disagree about what
    'the bot's source' means."""
    try:
        return "\n".join(p.read_text(errors="replace")
                         for p in sorted(Path(bot).glob("*.py")))
    except OSError:
        return ""


def determinism_report(bots) -> list[str]:
    """One line per side that CANNOT be paired against. Empty list == clean."""
    bad = []
    for b in bots:
        s = _bot_sources(Path(b))
        name = Path(b).name
        if not s:
            bad.append(f"{name}: no readable *.py — cannot verify determinism")
        elif NOISE_TRUE_MARK in s:
            bad.append(f"{name}: NOISE_ON = True — spawn_salt reseeds from the OS "
                       f"every match and --seed does not reach it; this run is "
                       f"NOT PAIRED")
        elif NOISE_ANY_MARK not in s and RANDOM_MARK in s:
            bad.append(f"{name}: calls random.* and declares no NOISE_ON switch — "
                       f"a foreign or older lineage; pin its seed in a COPY or "
                       f"exclude it")
    return bad


def _print_determinism_banner(bots) -> None:
    bad = determinism_report(bots)
    if not bad:
        print("DETERMINISM: all sides pinned (no NOISE_ON = True, no unswitched "
              "random.*). Paired reading is licensed — still run "
              "tools/effective_n.py on the output, because PINNING is what "
              "causes seed degeneracy.", file=sys.stderr)
        return
    print("⛔ DETERMINISM: THIS RUN IS NOT PAIRED. Flips below measure the RNG, "
          "not the treatment:", file=sys.stderr)
    for line in bad:
        print(f"    {line}", file=sys.stderr)
    print("    Procedure: copy the bots, set NOISE_ON = False on EVERY side, "
          "rerun, then measure tools/effective_n.py — see this file's header. "
          "Set DET_REQUIRE_DETERMINISM=1 to make this a refusal.", file=sys.stderr)
    if os.environ.get("DET_REQUIRE_DETERMINISM") == "1":
        sys.exit(2)


def _selftest() -> int:
    """Drive determinism_report to BOTH verdicts on constructed bot dirs.

    A precondition check that has only ever seen the clean case has not been
    seen to check — and this one guards a claim (`the run is paired`) that is
    invisible in every number det.py prints."""
    import tempfile
    bad = 0

    def chk(label, got, want):
        nonlocal bad
        ok = got == want
        if not ok:
            bad += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<62} -> {got!r}"
              + ("" if ok else f" (want {want!r})"))

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        noisy = t / "_noisy"; noisy.mkdir()
        (noisy / "doctrine.py").write_text("NOISE_ON = True\n")
        (noisy / "main.py").write_text(
            "import random\nx = random.Random().randrange(97)\n")
        pinned = t / "_pinned"; pinned.mkdir()
        (pinned / "doctrine.py").write_text("NOISE_ON = False\n")
        (pinned / "main.py").write_text(
            "import random\nx = random.Random().randrange(97)\n")
        foreign = t / "_foreign"; foreign.mkdir()
        (foreign / "main.py").write_text("import random\nx = random.choice([1,2])\n")
        empty = t / "_empty"; empty.mkdir()

        chk("NOISE_ON = True side is REFUSED", len(determinism_report([noisy])), 1)
        chk("...and the line names the mechanism, not just the flag",
            "reseeds from the OS" in determinism_report([noisy])[0], True)
        chk("NOISE_ON = False side is CLEAN", determinism_report([pinned]), [])
        chk("unswitched random.* (foreign lineage) is REFUSED",
            len(determinism_report([foreign])), 1)
        chk("empty/unreadable dir is REFUSED, not waved through",
            len(determinism_report([empty])), 1)
        chk("a MIXED pair reports exactly the offending side",
            len(determinism_report([pinned, noisy])), 1)
        chk("...and an all-clean pair reports nothing",
            determinism_report([pinned, pinned]), [])

    # The LIVE control: the incumbent really does carry NOISE_ON = True, so the
    # True branch above is not testing a shape that never occurs.
    inc = ROOT / "bots" / "_v468kladturbo"
    if inc.exists():
        chk("LIVE CONTROL: the incumbent really is NOISE_ON = True",
            len(determinism_report([inc])), 1)
    else:
        print("  SKIP  live incumbent bots/_v468kladturbo not present")

    print("SELFTEST PASS" if not bad else f"*** {bad} cell(s) FAILED ***")
    return 1 if bad else 0


def play(job):
    tag, bot, opp, mp, seed, seat = job
    a, b = (bot, opp) if seat == "a" else (opp, bot)
    pr = subprocess.run([str(FCODE), "run", a, b, mp, "--seed", str(seed), "--tle", "0",
                         "--json", "--replay", "/dev/null"],
                        capture_output=True, text=True, cwd=ROOT)
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
                ti=res[f"{us}_titanium_collected"], oti=res[f"{them}_titanium_collected"],
                units=res[f"{us}_units"], bld=res[f"{us}_buildings"],
                tb=pr.stderr.count("Traceback"))


def main():
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(_selftest())
    if len(sys.argv) < 4:
        sys.exit("usage: det.py tagA=path tagB=path <opp_dir> [seeds] [map1,map2,...]\n"
                 "       det.py --selftest")
    ta, pa = sys.argv[1].split("=", 1)
    tb, pb = sys.argv[2].split("=", 1)
    opp = sys.argv[3]
    # PRECONDITION, REPORTED BEFORE ANY GAME RUNS. The docstring used to say
    # this script "measures but does not enforce" the precondition — which in
    # practice meant nobody checked it, and a flag-off contrast measured the RNG.
    _print_determinism_banner([pa, pb, opp])
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    mapsel = sys.argv[5].split(",") if len(sys.argv) > 5 else None
    maps = sorted((ROOT / "maps").glob("*.map26"))
    if mapsel:
        maps = [m for m in maps if m.stem in mapsel]
    jobs = []
    for mp in maps:
        for sd in range(1, seeds + 1):
            for seat in ("a", "b"):
                jobs.append((ta, pa, opp, str(mp), sd, seat))
                jobs.append((tb, pb, opp, str(mp), sd, seat))
    out = []
    workers = int(os.environ.get("DET_JOBS", "6"))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                out.append(r)
            if i % 50 == 0:
                print(f"\r {i}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    with open(os.environ.get("DET_OUT", "det_results.json"), "w") as f:
        json.dump(out, f)
    idx = {(r["tag"], r["map"], r["seed"], r["seat"]): r for r in out}
    keys = sorted({(k[1], k[2], k[3]) for k in idx})
    flips = []
    diffstate = []
    same = 0
    awins = bwins = n = 0
    for k in keys:
        A = idx.get((ta,) + k)
        B = idx.get((tb,) + k)
        if not A or not B:
            continue
        n += 1
        awins += A["win"]
        bwins += B["win"]
        if A["win"] != B["win"]:
            flips.append((k, A["win"], B["win"], A["ti"], B["ti"]))
        if (A["turns"], A["ti"], A["units"], A["bld"], A["win"]) == \
           (B["turns"], B["ti"], B["units"], B["bld"], B["win"]):
            same += 1
        else:
            diffstate.append((k, A["turns"], B["turns"], A["ti"], B["ti"]))
    if not n:
        sys.exit("no completed paired games")
    print(f"\npaired deterministic games: {n}")
    print(f"  {ta} wins {awins}/{n} = {awins/n:.1%}   {tb} wins {bwins}/{n} = {bwins/n:.1%}")
    print(f"  identical end-state (turns/ti/units/bld/winner): {same}/{n}")
    print(f"  outcome flips: {len(flips)}")
    for f in flips:
        print("    FLIP", f)
    print(f"  non-identical end-state games: {len(diffstate)}")
    for d in diffstate[:40]:
        print("    DIFF", d)
    print(f"  tracebacks across all games: {sum(r['tb'] for r in out)}")

    # DISTINCT-SHAPE COUNT (added 2026-08-08 s19, after this trap bit two legs
    # in one evening -- research's suggestion, and both bites were mine).
    #
    # SEED COUNT IS NOT SAMPLE SIZE. With NOISE_ON=False on both arms and a
    # deterministic opponent, the seed drives nothing that is still switched on,
    # so every seed on a given (map, seat) can produce the byte-identical game.
    # A leg reported as "120 paired games" can be ONE game replicated four times
    # per cell, and the header line looks exactly the same either way.
    #
    # Both bites tonight: the hive-fix effect leg read "4/4 seeds" on a 601-round
    # swing that was 1 distinct game; then the rescope-vs-wholesale leg looked
    # decisive at 4/4 seeds vs opp_v63 (1 shape) and evaporated at 15/16 shapes
    # vs opp_v78. Read the two numbers together or not at all.
    shapes = set()
    for k in keys:
        A = idx.get((ta,) + k)
        B = idx.get((tb,) + k)
        if not A or not B:
            continue
        shapes.add((k[0], k[2],
                    A["turns"], A["ti"], A["units"], A["bld"], A["win"],
                    B["turns"], B["ti"], B["units"], B["bld"], B["win"]))
    print(f"  DISTINCT paired shapes: {len(shapes)}/{n}   <-- your real replication")
    low_replication = len(shapes) * 2 < n
    if low_replication:
        print(f"    ** LOW REPLICATION: seeds are collapsing ({n} pairs -> {len(shapes)} "
              f"distinct). Do NOT read effect size off this leg alone; add an "
              f"opponent or turn noise on. **")

    # DELIVERED-TITANIUM DELTA (added 2026-08-08 s18, on a measured blind spot).
    # Flip accounting is blind to economy-only effects BY CONSTRUCTION: the
    # hive_freeze ablation doubled delivered titanium (5,260 -> 11,030) and 5x'd
    # standing buildings with ZERO outcome flips. The long-game census says
    # delivered titanium is the SOLE deciding metric in 219/219 full-length
    # ladder games -- 26.2% of all games, 36.7% under the v80 line -- so a
    # change that moves only economy moves the thing that decides a quarter of
    # our games while scoring exactly nothing here. Paired per (map, seed, seat),
    # so this is a reporting change over data play() already collects.
    # READ IT AS: "0 flips" means NO OUTCOME EFFECT MEASURED, never "no effect".
    deltas = []
    permap = {}
    for k in keys:
        A = idx.get((ta,) + k)
        B = idx.get((tb,) + k)
        if not A or not B:
            continue
        d = B["ti"] - A["ti"]
        deltas.append(d)
        permap.setdefault(k[0], []).append(d)
    if deltas:
        def _median(xs):
            # Average the two middle values on even n. The upper-middle pick is
            # actively misleading here: economy deltas are BIMODAL by nature --
            # the maps a plank touches move, every other map sits at exactly 0 --
            # so upper-middle reports the moved population's value as if it were
            # typical (measured: 6 zeros + 6 x +5770 printed "+5770", true +2885).
            s = sorted(xs)
            m = len(s) // 2
            return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2

        mean = sum(deltas) / len(deltas)
        moved_vals = [d for d in deltas if d]
        moved = len(moved_vals)
        # HEADLINE = mean + moved fraction. On a bimodal set the overall median
        # is nearly uninformative (it reports 0 whenever a plank touches fewer
        # than half the maps, which is the common case); mean-with-moved-count
        # reads correctly whether a plank touches one map or all fifteen.
        line = (f"  delivered-Ti delta ({tb} minus {ta}): mean {mean:+.0f}  "
                f"games moved {moved}/{len(deltas)}")
        if moved:
            line += (f"  [median over MOVED games {_median(moved_vals):+.0f}; "
                     f"median over all {_median(deltas):+.0f}]")
        print(line)
        rows = sorted(((sum(v) / len(v), m) for m, v in permap.items()),
                      key=lambda r: -abs(r[0]))
        for avg, m in rows[:6]:
            if abs(avg) >= 1:
                print(f"    ECON {m:14s} mean {avg:+.0f}")

    # Exit nonzero on seed collapse so chained scripts stop instead of reading
    # effect sizes off a leg with no real replication. A printed warning was
    # ignored twice in one evening (s19); a refusing exit cannot be (process
    # review 2026-08-09, rec 1: warnings become exit codes). Reading the
    # printout and proceeding anyway is still possible -- but now it is typed.
    if low_replication:
        sys.exit(2)


if __name__ == "__main__":
    main()
