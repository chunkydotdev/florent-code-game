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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bot")
    # CONTROL = current incumbent (v112 = _v148ferryfirst as of 2026-08-11).
    # Move this on every ship; a stale control measures the wrong contrast.
    ap.add_argument("--ctrl", default="bots/_v146gunaxis")  # v114, shipped 19:14Z
    ap.add_argument("--kind", default="sentinel")
    ap.add_argument("--games", type=int, default=24)
    ap.add_argument("--maps", nargs="*", default=MAPS)
    a = ap.parse_args()

    tmp = Path(tempfile.mkdtemp(prefix="dose_"))
    T, C = Counter(), Counter()
    per_t, per_c = [], []          # PER-GAME values — the band needs the spread
    n = 0
    seed = 0
    print(f"DOSE  {a.bot}  vs  {a.ctrl}   kind={a.kind}   SERIAL", flush=True)
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
            n += 1
            if n % 4 == 0:
                tb = T[f"fwdbuild_{a.kind}"] / n
                cb = C[f"fwdbuild_{a.kind}"] / n
                print(f"  {n}/{a.games}  fwd {a.kind}/game  TREAT {tb:.2f}  "
                      f"CTRL {cb:.2f}", flush=True)
            rp.unlink(missing_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not n:
        print("DOSE_RESULT: NO GAMES")
        return
    print(f"\nDOSE  n={n} games (both seats)")
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
    main()
