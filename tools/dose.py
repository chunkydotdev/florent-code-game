#!/usr/bin/env python3
"""SERIAL DOSE CHECK — does the arm actually DO the thing? Local, minutes.

WHY THIS EXISTS, AND WHY IT IS THE BOTTLENECK TOOL
--------------------------------------------------
Magnus, 2026-08-11: *"do we actually make ANY progress? We haven't had a new bot
in over a day."* Correct: v104 has held the slot ~29 h, ~19 arm trees built, zero
shipped. Three arms hold positive point estimates (best-fit 524/1024, cap6
519/1024, ferry-first 518/1024) and the ship rule needs only **(a) a positive
point estimate, (b) A VERIFIED MECHANISM, (c) no programme breach.** **(b) is the
only thing missing, and nothing in this repo could produce it locally.**

  * `tools/arena.py:53` runs with `--replay /dev/null`.
  * `tools/h2h.sh:66-67` passes NO `--replay`, so every game overwrites the
    `fcode.toml` default `replay.replay26` — one file, last game wins.
  * `tools/mech_battery.py` keeps replays but decodes only builder deaths/spawns.

So: unique replay path per game, decode with the SHIPPED `replay_events.py`
(cleared on both the rotate-suppression and post-death-id-reuse branches by the
side lane, s31), report the counts the plank claims to move.

⛔ SERIAL, NOT PARALLEL. D65, measured 2026-08-11: a 16-game PARALLEL dose check
reported the heal arm at 268 heals/game vs control 108 — the OPPOSITE of a
3-game serial check, and both were wrong. Parallel `fcode run` produces
incoherent counts. This runs one game at a time, on purpose, and it is why the
tool is slow.

⛔ AND A DOSE CHECK CAN KILL A SHIP. `_v139heal` was the JOINT-TOP arm at
524/1024 with a permissive ship rule and a free slot; seed-matched serial dosing
showed it healing 461.5/game against the control's 132.8 — **3.5x MORE, the exact
opposite of the plank.** A positive point estimate is not a mechanism.

BOTH SEATS ALWAYS PLAYED — a one-seat result is a seat measurement, not an arm
measurement (h2h.sh's rule, same reason).

Usage:
  dose.py <botdir> --kind sentinel --games 24 [--maps ...] [--ctrl bots/_v130loki13]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
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
PY = ROOT / ".venv" / "bin" / "python"
EVENTS = ROOT / "tools" / "corpus" / "replay_events.py"
MAPS = ["antler", "atoll", "drumlin", "fjordgate", "heart", "hive", "meander", "nordkap"]


def decode(replay: Path):
    """BUILD/DEATH rows -> per-team counters. Uses the SHIPPED decoder."""
    import io
    import importlib.util
    spec = importlib.util.spec_from_file_location("replay_events", EVENTS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    buf = io.StringIO()
    mod.census(replay, buf)
    out = {0: Counter(), 1: Counter()}
    for line in buf.getvalue().splitlines():
        f = line.split("\t")
        if len(f) < 9:
            continue
        ev, team, kind = f[1], int(f[3]), f[4]
        d2o, d2e = int(f[7]), int(f[8])
        fwd = d2e < d2o
        if ev == "BUILD":
            out[team][f"build_{kind}"] += 1
            if fwd:
                out[team][f"fwdbuild_{kind}"] += 1
        elif ev == "DEATH":
            out[team][f"death_{kind}"] += 1
            if fwd:
                out[team][f"fwddeath_{kind}"] += 1
    return out


def _incumbent_ctrl() -> str | None:
    """CLASS A, s48 wrap — DERIVE THE CONTROL, DO NOT EMBED IT.

    This used to be `--ctrl default="bots/_v146gunaxis"` with the comment "Move
    this on every ship; a stale control measures the wrong contrast." Nobody
    moved it: at the s48 wrap the default named v114 while the incumbent was
    `bots/_v468kladturbo`, so any hand-run omitting --ctrl was silently dosing
    against a control ~11 ships stale. A comment instructing a human to maintain
    a constant is the failure mode, not the fix — `tools/fleet_dispatch.py` was
    converted for exactly this reason (a50f27ef). Reads PROGRAMME.md's INCUMBENT
    through control_pin, the one authority.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from control_pin import incumbent
        p = incumbent()
    except Exception:
        return None
    if p is None:
        return None
    try:
        return str(p.relative_to(Path(__file__).resolve().parent.parent))
    except ValueError:
        return str(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bot")
    ap.add_argument("--ctrl", default=None,
                    help="control tree; default = PROGRAMME.md's INCUMBENT, read live")
    ap.add_argument("--kind", default="sentinel")
    # ⛔⛔ CLASS B, s48 wrap — A TOOL CONSUMED BY PRE-REGISTRATIONS MAY NOT PICK
    # ITS OWN SAMPLE SIZE. `--games` had `default=24`. On 2026-08-17 a prereg
    # registered n=120 and the battery was invoked without `--games`; the tool
    # ran 24 and said nothing, so the registered size and the executed size
    # differed with no artefact anywhere recording it. That is the same shape as
    # a registered method that is not executable — except silent, because 24
    # games print exactly the same verdict vocabulary as 120.
    # ⇒ THERE IS NO DEFAULT ANY MORE. Either say which n you registered
    # (`--registered N`, which STAMPS the number into every verdict line and
    # reports any shortfall against it), or declare the run unregistered
    # (`--games N`). Passing both is a REFUSAL unless they agree.
    ap.add_argument("--games", type=int, default=None,
                    help="sample size for an UNREGISTERED exploratory run")
    ap.add_argument("--registered", type=int, default=None, metavar="N",
                    help="the n written into the pre-registration; stamped into "
                         "the output and checked against what actually ran")
    # ⛔ debt 20, s48: dose.py:157 unlinked every replay after decoding and had
    # no retain flag, but the registered S1 seat-band read on both SEALSENT
    # preregs consumes THE REPLAYS. A registered read whose inputs the tool
    # deletes is a registered read that cannot be executed.
    ap.add_argument("--keep", default=None, metavar="DIR",
                    help="retain every replay in DIR instead of deleting it "
                         "(required by any registered read that decodes replays)")
    ap.add_argument("--maps", nargs="*", default=MAPS)
    # ADD-ONLY (builder s48). Off by default; changes NO existing computation.
    # WHY: the printed band covers `fwdbuild_<kind>` ONLY, because that is the
    # quantity the tool's DOSE_RESULT verdict is about. A brief that also puts
    # an EXCLUSION bar on builder deaths (e.g. "death diff CI-upper < +0.35")
    # cannot be answered from the printed means -- a mean has no interval. This
    # dumps the per-game paired values so the same paired-difference arithmetic
    # the band already uses can be applied to any decoded key.
    ap.add_argument("--tsv", default=None,
                    help="also write per-game paired counts to this TSV")
    a = ap.parse_args()

    # ---- CLASS B GATE: refuse to invent a sample size, and refuse a contradiction.
    if a.games is None and a.registered is None:
        print("⛔ dose.py REFUSES to pick a sample size for you.\n"
              "   Pass --registered N (the n written into the pre-registration) "
              "or --games N (an explicitly unregistered exploratory run).\n"
              "   There is no default: a tool consumed by preregs that silently "
              "runs a different size than registered produces a result nobody "
              "can tell apart from the registered one.", file=sys.stderr)
        return 2
    if (a.games is not None and a.registered is not None
            and a.games != a.registered):
        print(f"⛔ dose.py REFUSES: --games {a.games} contradicts --registered "
              f"{a.registered}. Say one number, not two.", file=sys.stderr)
        return 2
    if a.registered is not None:
        a.games = a.registered
    if a.ctrl is None:
        a.ctrl = _incumbent_ctrl()
        if a.ctrl is None:
            print("⛔ dose.py REFUSES: no --ctrl given and PROGRAMME.md's "
                  "INCUMBENT could not be read. Refusing to guess the control "
                  "tree — a wrong control measures the wrong contrast silently.",
                  file=sys.stderr)
            return 2
        print(f"  control derived from PROGRAMME INCUMBENT: {a.ctrl}", flush=True)
    _reg = (f"REGISTERED n={a.registered}" if a.registered is not None
            else f"UNREGISTERED n={a.games}")

    keep_dir = None
    if a.keep:
        keep_dir = Path(a.keep)
        keep_dir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="dose_"))
    T, C = Counter(), Counter()
    per_t, per_c = [], []          # PER-GAME values — the band needs the spread
    per_game = []                  # ADD-ONLY: full per-game rows for --tsv
    n = 0
    seed = 0
    print(f"DOSE  {a.bot}  vs  {a.ctrl}   kind={a.kind}   SERIAL   {_reg}"
          + (f"   KEEP -> {keep_dir}" if keep_dir else ""), flush=True)
    try:
        while n < a.games:
            m = a.maps[(n // 2) % len(a.maps)]
            seat = n % 2                       # BOTH SEATS ALWAYS PLAYED
            if seat == 0:
                bots, ti, ci = [a.bot, a.ctrl], 0, 1
            else:
                bots, ti, ci = [a.ctrl, a.bot], 1, 0
            if n % 2 == 0:
                seed += 1
            rp = tmp / f"g{n}.replay26"
            r = subprocess.run(
                [str(FCODE), "run", bots[0], bots[1], f"maps/{m}.map26",
                 "--seed", str(seed), "--replay", str(rp)],
                capture_output=True, text=True, cwd=ROOT)
            if not rp.exists():
                print(f"  !! no replay for game {n} ({m} seed {seed})", flush=True)
                n += 1
                continue
            d = decode(rp)
            T.update(d[ti])
            C.update(d[ci])
            per_t.append(d[ti][f"fwdbuild_{a.kind}"])
            per_c.append(d[ci][f"fwdbuild_{a.kind}"])
            if a.tsv:
                _keys = [f"build_{a.kind}", f"fwdbuild_{a.kind}",
                         "death_builder_bot", "fwddeath_builder_bot",
                         f"death_{a.kind}", f"fwddeath_{a.kind}"]
                row = {"game": n, "map": m, "seed": seed, "seat": seat}
                for k in _keys:
                    row["T_" + k] = d[ti][k]
                    row["C_" + k] = d[ci][k]
                per_game.append(row)
            n += 1
            if n % 4 == 0:
                tb = T[f"fwdbuild_{a.kind}"] / n
                cb = C[f"fwdbuild_{a.kind}"] / n
                print(f"  {n}/{a.games}  fwd {a.kind}/game  TREAT {tb:.2f}  "
                      f"CTRL {cb:.2f}", flush=True)
            if keep_dir is not None:
                # RETAIN, don't delete. Name carries everything the S1 seat-band
                # read needs to pair a replay back to its cell without a
                # side-file: game index, map, seed, and which seat the TREATMENT
                # played. A bare g<N>.replay26 would need this tool's loop
                # re-derived to be readable.
                rp.replace(keep_dir / f"g{n:04d}_{m}_s{seed}_treatseat{seat}.replay26")
            else:
                rp.unlink(missing_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if keep_dir is not None:
            _kept = len(list(keep_dir.glob("*.replay26")))
            print(f"  KEPT {_kept} replays in {keep_dir}", flush=True)

    if a.tsv and per_game:
        cols = list(per_game[0].keys())
        with open(a.tsv, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in per_game:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
        print(f"  per-game TSV -> {a.tsv}  ({len(per_game)} rows)", flush=True)

    if not n:
        print("DOSE_RESULT: NO GAMES")
        return
    print(f"\nDOSE  n={n} games (both seats)   {_reg}")
    if a.registered is not None and n != a.registered:
        # The whole point of --registered: the gap between what was registered
        # and what ran is stated IN the result, not left to whoever compares the
        # prereg page against the log later.
        print(f"  ⛔ SHORTFALL: {n} games ran against {a.registered} REGISTERED. "
              f"This result is NOT the registered read; say so wherever it is "
              f"banked.")
    keys = [f"build_{a.kind}", f"fwdbuild_{a.kind}",
            f"death_builder_bot", f"fwddeath_builder_bot"]
    print(f"  {'quantity':<28}{'TREAT':>9}{'CTRL':>9}{'ratio':>9}")
    for k in keys:
        t, c = T[k] / n, C[k] / n
        rr = (t / c) if c else float("nan")
        print(f"  {k+'/game':<28}{t:>9.2f}{c:>9.2f}{rr:>9.2f}x")
    tb, cb = T[f"fwdbuild_{a.kind}"] / n, C[f"fwdbuild_{a.kind}"] / n

    # ⛔⛔ THE BAND. FIRST VERSION OF THIS TOOL SAID `elif tb > cb: DOSE
    # DELIVERED` — AN UNSIZED BAR, WITH NO THRESHOLD, IN THE TOOL WRITTEN TO
    # ENFORCE SIZED BARS. It printed "DOSE DELIVERED" for cap6 on 1.58 -> 1.67
    # (1.05x) at n=24, which is noise. Caught 2026-08-11 by reading the tool's
    # own first output. Same defect as LOKI-27's "INSERT -> RISES" and
    # fwd_read's bare `db < 0`, committed a third time by the person fixing the
    # first two. **A direction is not a bar.**
    #
    # PAIRED: both arms play the SAME game, so the per-game DIFFERENCE is the
    # unit and its sd is what sizes the band.
    import statistics
    diffs = [t - c for t, c in zip(per_t, per_c)]
    sd = statistics.pstdev(diffs) if len(diffs) > 1 else 0.0
    se = sd / (len(diffs) ** 0.5) if diffs else 0.0
    band = 2 * se
    obs = tb - cb
    print(f"\n  paired diff {obs:+.3f}/game   sd(diff) {sd:.2f}   "
          f"2*SE = {band:.3f}   n={n}")
    mde_pct = (band / cb * 100) if cb else float("nan")
    print(f"  INFORMATIVE BAND: |diff| >= {band:.3f}/game "
          f"({mde_pct:.0f}% of the control level)")

    if cb == 0 and tb == 0:
        print(f"\n  DOSE_RESULT: INERT — neither arm builds a forward {a.kind}. "
              f"The plank's precondition is absent in this fixture.")
    elif obs >= band:
        print(f"\n  DOSE_RESULT: DOSE DELIVERED — forward {a.kind} "
              f"{cb:.2f} -> {tb:.2f}/game, outside the band. "
              f"Mechanism runs in the CLAIMED direction.")
    elif obs <= -band:
        print(f"\n  DOSE_RESULT: ⛔ MECHANISM INVERTED — forward {a.kind} "
              f"{cb:.2f} -> {tb:.2f}/game, outside the band the WRONG way "
              f"(the _v139heal outcome). DISQUALIFIED.")
    else:
        print(f"\n  DOSE_RESULT: NO INFORMATION — {cb:.2f} -> {tb:.2f}/game is "
              f"INSIDE the band. This is NOT a delivered dose and NOT a "
              f"refutation. Buy more n, or the plank is near-inert here.")


if __name__ == "__main__":
    # ⛔ The refusals above return 2 and MUST reach the shell — a battery script
    # that reads `$?` would otherwise see 0 on a refusal and run on.
    raise SystemExit(main() or 0)
