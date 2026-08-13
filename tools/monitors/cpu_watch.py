#!/usr/bin/env python3
"""CPU-CEILING WATCH — the #44 monitor (s36): our max per-turn CPU on GRAND
maps, read off archived platform replays, alarm at >9,200µs.

WHY 9,200 IS MEANINGFUL AND NOT A GUESS. The bot self-caps at
CPU_BUDGET_US=8000 (doctrine.py:1076) checked every 64 BFS steps, producing a
measured ceiling of ~8,750-8,804µs (budget + inter-check overshoot) in a
55µs-tight cluster across games/units/rounds. Anything above 9,200 therefore
means the guard's check interval coarsened or an UNGUARDED path grew — an
unambiguous structural signal either way (research @8badc07, resolution
@62fee2d). The engine kills a turn at 10,000.

LOCAL BLINDNESS IS THE REASON THIS EXISTS: get_cpu_time_elapsed() reads 0
under local `fcode run` (doctrine.py:1072), so no local test can catch a CPU
regression — platform replays are the only instrument.

Standing rules honored: reports the newest-scanned-replay AGE (a monitor that
reads files reports their freshness); prints BLIND, never silence, when it
cannot scan; state in corpus/cpu_watch_state.json (seen files); alert file
corpus/CPU_ALERT. Selftest drives BOTH verdicts on a real archived replay.

Usage:
  .venv/bin/python tools/monitors/cpu_watch.py            # one scan pass
  .venv/bin/python tools/monitors/cpu_watch.py --selftest
Arm:  while true; do .venv/bin/python tools/monitors/cpu_watch.py; sleep 1800; done
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, WIRE_LEN  # noqa: E402

ARCHIVE = ROOT / "replay_archive"
STATE = ROOT / "corpus" / "cpu_watch_state.json"
ALERT = ROOT / "corpus" / "CPU_ALERT"
THRESHOLD_US = 9200
GRAND_AREA = 676  # >676 = the class where the guard ceiling lives

OUR_TEAM = "OpenSverige"


def scan_replay(path: Path) -> tuple[int, int] | None:
    """(our_max_exec_us, map_area) or None if unparseable."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    mw = mh = 0
    team_of: dict[int, int] = {}
    our_seat = None
    meta = path.with_name(path.name.split("_game_")[0] + ".meta.json")
    if meta.exists():
        try:
            m = json.loads(meta.read_text())
            if m.get("teamAName") == OUR_TEAM:
                our_seat = 0
            elif m.get("teamBName") == OUR_TEAM:
                our_seat = 1
        except Exception:
            pass
    if our_seat is None:
        return None
    mx = 0
    rnd = -1
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            d = {n: v for n, _w, v in fields(value) if not isinstance(v, bytes)}
            mw, mh = d.get(1, 0), d.get(2, 0)
        elif num == 3 and wire == WIRE_LEN:
            rnd += 1
            for un, uw, uv in fields(value):
                if un != 1 or uw != WIRE_LEN:
                    continue
                for en, ew, ev in fields(uv):
                    if en == 1 and ew == WIRE_LEN:
                        for e2n, e2w, e2v in fields(ev):
                            if e2n == 1 and e2w == WIRE_LEN:
                                e = parse_entity(e2v, rnd)
                                if e is not None and e.id not in team_of:
                                    team_of[e.id] = e.team
                    elif en == 9 and ew == WIRE_LEN:
                        d = {n: v for n, _w, v in fields(ev)}
                        if team_of.get(d.get(1, 0)) == our_seat:
                            mx = max(mx, d.get(3, 0))
    return mx, mw * mh


def main(threshold: int = THRESHOLD_US) -> int:
    if not ARCHIVE.is_dir():
        print("CPU_WATCH: BLIND — replay_archive/ missing")
        return 0
    seen = set()
    if STATE.exists():
        try:
            seen = set(json.loads(STATE.read_text())["seen"])
        except Exception:
            seen = set()
    reps = sorted(ARCHIVE.glob("*.replay26"), key=lambda p: p.stat().st_mtime)
    if not reps:
        print("CPU_WATCH: BLIND — no replays in archive")
        return 0
    newest_age_min = (time.time() - reps[-1].stat().st_mtime) / 60
    new = [p for p in reps if p.name not in seen]
    worst, worst_file, scanned = 0, None, 0
    for p in new[-200:]:
        r = scan_replay(p)
        seen.add(p.name)
        if r is None:
            continue
        mx, area = r
        if area <= GRAND_AREA:
            continue
        scanned += 1
        if mx > worst:
            worst, worst_file = mx, p.name
    STATE.write_text(json.dumps({"seen": sorted(seen)[-5000:]}))
    line = (f"CPU_WATCH: {scanned} new GRAND replay(s), worst our-max "
            f"{worst}µs (threshold {threshold}), newest replay {newest_age_min:.0f}m old")
    if worst > threshold:
        msg = (f"*** CPU CEILING BREACH *** our max turn {worst}µs > {threshold} "
               f"in {worst_file} — the 8000µs guard is no longer holding "
               f"(coarsened interval or unguarded path). Engine kills at 10,000.")
        print(msg)
        ALERT.write_text(msg + "\n")
        return 1
    print(line + " — OK")
    if ALERT.exists():
        ALERT.unlink()
    return 0


def selftest() -> int:
    # Drive BOTH verdicts on a real archived GRAND replay with a known our-max
    # (~8,7xx: the b9f3fab5 30x30 games measured 8,750-8,757 this session).
    cands = sorted(ARCHIVE.glob("b9f3fab5-*_game_3.replay26")) or \
        sorted(ARCHIVE.glob("*.replay26"))
    ok = True
    got = None
    for p in cands:
        r = scan_replay(p)
        if r and r[1] > GRAND_AREA and r[0] > 0:
            got = (p.name, r[0])
            break
    if got is None:
        print("SELFTEST: no scannable GRAND replay with exec times — UNTESTED (not a pass)")
        return 1
    name, mx = got
    print(f"  fixture {name}: our max {mx}µs")
    fires = mx > 8000        # threshold below the known ceiling MUST fire
    holds = not (mx > 9200)  # the real threshold must NOT fire on the known ceiling
    print(f"  [{'ok' if fires else 'FAIL'}] threshold 8000 fires on the fixture")
    print(f"  [{'ok' if holds else 'FAIL'}] threshold 9200 holds on the fixture")
    ok = fires and holds
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
