#!/usr/bin/env python3
"""Paired battery that KEEPS its replays, and reads the mechanism out of them.

Why this exists
---------------
`tools/arena.py` runs every match with `--replay /dev/null`. So no local
battery this project has ever run produced a decodable replay, and every
mechanism question -- did the bot actually DO the thing? -- has had to be
answered from the ladder corpus, which lags by hours and cannot see a variant
that was never shipped. That gap is why planks keep being judged on win rate
at n=300, where the MDE is ~11pp pooled: the only readable number is the one
that cannot resolve the effect.

This runs the same paired design as arena.py -- variant and control over an
identical (map, opponent, seat, seed) fixture -- but writes each replay to
disk and then decodes the metric that the change is actually supposed to move.

builder-method S2 is the rule this serves: pre-register THE METRIC ONLY THE
CHANGE CAN MOVE, not a whole-bot metric. Win rate here is a SAFETY arm (did
this break anything?), never the verdict.

Decoded per game, per team: builder-bot deaths by round band, builder-bot
spawns, and end-state economy. Deaths are `removeEntity` on an id that
`placeEntity` introduced as a builder_bot -- the same event pair `dc_decode`
validated to 99.45% against the HP ledger, without the attribution layer,
because "how many died and when" needs no shooter.

Usage:
  .venv/bin/python tools/mech_battery.py \
      --variant bots/_det_v115dodge --control bots/_det_v115off \
      --opponents bots/orizon_probe bots/ouroboros_probe \
      --maps atoll hive --seeds 3 --jobs 5 -o scratchpad/dodge
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, parse_entity, WIRE_LEN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"
BANDS = ((0, 100, "r0_99"), (100, 250, "r100_249"),
         (250, 500, "r250_499"), (500, 10 ** 9, "r500p"))


def band_of(rnd):
    for lo, hi, name in BANDS:
        if lo <= rnd < hi:
            return name
    return "r500p"


def decode_deaths(path: Path):
    """-> {team: {band: deaths}}, {team: spawns}. Builder bots only."""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None, None
    team_of, is_bot = {}, set()
    deaths = defaultdict(Counter)
    spawns = Counter()
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in team_of:
                            continue
                        team_of[e.id] = e.team
                        if e.kind == "builder_bot":
                            is_bot.add(e.id)
                            spawns[e.team] += 1
                elif unum == 3:
                    rid = None
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rid = rv
                    if rid in is_bot:
                        deaths[team_of[rid]][band_of(rnd)] += 1
    return deaths, spawns


def play(job):
    arm, arm_path, opp, map_path, seed, seat, tle, outdir, keep_replays = job
    a, b = (arm_path, opp) if seat == "a" else (opp, arm_path)
    stem = f"{arm}__{Path(opp).name}__{Path(map_path).stem}__{seed}__{seat}"
    rp = Path(outdir) / "replays" / f"{stem}.replay26"
    rp.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(FCODE), "run", a, b, map_path, "--seed", str(seed),
           "--tle", str(tle), "--json", "--replay", str(rp)]
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
    our_seat = seat
    ourwin = result["winner"].lower() == our_seat
    crashes = 0
    for block in proc.stderr.split("Traceback (most recent call last)"):
        if "Error" in block and f"{Path(arm_path).name}/" in block:
            crashes += 1
    row = {
        "cell": arm, "opp": Path(opp).name, "mp": Path(map_path).stem,
        "tb": seed, "seat": seat, "ourwin": ourwin,
        "cond": result.get("win_condition"), "turns": result.get("turns"),
        "crashes": crashes,
        "collected": result.get("a_titanium_collected") if seat == "a"
        else result.get("b_titanium_collected"),
    }
    deaths, spawns = decode_deaths(rp)
    if deaths is not None:
        # Team index 0 is seat A, 1 is seat B, matching the engine's own order.
        ours = 0 if seat == "a" else 1
        for _lo, _hi, nm in BANDS:
            row[f"deaths_{nm}"] = deaths[ours][nm]
        row["deaths_total"] = sum(deaths[ours].values())
        row["spawns"] = spawns[ours]
    if not keep_replays:
        rp.unlink(missing_ok=True)  # decoded; the bytes are not the deliverable
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--opponents", nargs="+", required=True)
    ap.add_argument("--maps", nargs="*")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--tle", type=int, default=10)
    ap.add_argument("-o", "--out", default="scratchpad/mech")
    ap.add_argument("--keep-replays", action="store_true",
                    help="keep the decoded replays for a second pass "
                         "(tools/dodge_capture.py reads them)")
    args = ap.parse_args()

    maps_dir = ROOT / "maps"
    maps = ([maps_dir / f"{m}.map26" for m in args.maps] if args.maps
            else sorted(maps_dir.glob("*.map26")))
    arms = [("variant", args.variant), ("control", args.control)]
    jobs = [
        (arm, path, opp, str(mp), seed, seat, args.tle, args.out, args.keep_replays)
        for arm, path in arms
        for opp in args.opponents
        for mp in maps
        for seed in range(args.seeds)
        for seat in ("a", "b")
    ]
    print(f"{len(jobs)} matches — {len(maps)} maps x {len(args.opponents)} opponents "
          f"x {args.seeds} seeds x 2 seats x 2 arms, {args.jobs} parallel", file=sys.stderr)

    Path(args.out).mkdir(parents=True, exist_ok=True)
    rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                rows.append(r)
            if i % 20 == 0:
                print(f"  {i}/{len(jobs)}", file=sys.stderr)
    outp = Path(args.out) / "full.json"
    outp.write_text(json.dumps(rows, indent=1))
    if not args.keep_replays:
        shutil.rmtree(Path(args.out) / "replays", ignore_errors=True)
    print(f"{len(rows)} games -> {outp}", file=sys.stderr)

    # ⛔⛔ RECONCILE REQUESTED AGAINST RETURNED, PER ARM. ADDED s44 2026-08-15.
    # `play()` returns None for a game with no winner (:117) and the collector
    # silently skips it (:180) -- so a failed game leaves the DENOMINATOR rather
    # than counting as a loss. Both totals were already printed, ~15 lines apart,
    # and NOTHING SUBTRACTED THEM: not invisible, UNRECONCILED.
    # ⛔ AND IT MUST BE PER ARM, which is the whole point: a failure concentrated
    # in ONE arm -- the case that biases a comparison -- moves the battery-wide
    # total by exactly as much as one split evenly between them.
    # MEASURED THE SAME DAY: _v255homemax ran 10.00% NOWINNER (20/200) on a
    # remote shard while every local battery of it read 32/32 = 100% on both
    # arms. `tools/overnight.sh:137-148` had this right all along -- it writes a
    # NOWINNER ROW, increments n, and ABORTS past 1% -- so the shard runner found
    # the defect its sibling could not see. That asymmetry is the exact shape
    # overnight.sh:50-53 already warns about: one runner hardened, the sibling
    # left with the original behaviour.
    want = Counter()
    for j in jobs:
        want[j[0]] += 1
    got = Counter(r["cell"] for r in rows if "cell" in r)
    missing = {a: want[a] - got.get(a, 0) for a in want}
    if any(missing.values()):
        print("⛔ GAMES DROPPED — a dropped game leaves the denominator, it is NOT a loss:",
              file=sys.stderr)
        for a in sorted(want):
            m = missing[a]
            mark = "   <-- DROPPED" if m else ""
            print(f"     {a:<10} requested {want[a]:>4}  returned {got.get(a,0):>4}"
                  f"  dropped {m:>3}{mark}", file=sys.stderr)
        print("   ⚠ AN ARM-CONCENTRATED DROP BIASES EVERY COMPARISON BELOW. "
              "Treat this run as UNSCORABLE until the cause is known.", file=sys.stderr)
    else:
        print(f"reconciled: requested == returned on every arm "
              f"({', '.join(f'{a} {want[a]}' for a in sorted(want))})", file=sys.stderr)

    # Mechanism first, win rate second -- deliberately in that order.
    print("\nMECHANISM (the metric only this change can move)")
    print(f"  {'arm':9s} {'games':>6s} " + " ".join(f"{n:>10s}" for _l, _h, n in BANDS)
          + f" {'total':>8s} {'spawns':>7s} {'crash':>6s}")
    for arm in ("control", "variant"):
        s = [r for r in rows if r["cell"] == arm]
        if not s:
            continue
        cells = " ".join(
            f"{sum(r.get(f'deaths_{n}', 0) for r in s) / len(s):10.2f}"
            for _l, _h, n in BANDS)
        print(f"  {arm:9s} {len(s):6d} {cells} "
              f"{sum(r.get('deaths_total', 0) for r in s) / len(s):8.2f} "
              f"{sum(r.get('spawns', 0) for r in s) / len(s):7.2f} "
              f"{sum(r['crashes'] for r in s):6d}")
    print("\nSAFETY ARM (win rate; underpowered by construction at this n — not the verdict)")
    for arm in ("control", "variant"):
        s = [r for r in rows if r["cell"] == arm]
        if s:
            w = sum(1 for r in s if r["ourwin"])
            print(f"  {arm:9s} {w}/{len(s)} = {100 * w / len(s):.1f}%   "
                  f"median collected {sorted(r['collected'] or 0 for r in s)[len(s) // 2]}")
    print("\nRun tools/reprice.py on the JSON for the paired/pooled split.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
