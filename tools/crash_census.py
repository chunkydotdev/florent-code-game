#!/usr/bin/env python3
"""Detect units destroyed by an UNCAUGHT EXCEPTION, from replay bytes alone.

WHY THIS EXISTS.  Per CLAUDE.md: if a unit's `run()` raises anything besides
a CPU timeout, the engine prints a traceback and PERMANENTLY destroys that
unit.  Replays do NOT contain the traceback text (verified: a positive
control run against `bots/_probe_crash` -- which crashes every builder bot
deliberately -- has zero occurrences of the sentinel string in the replay
bytes).  So the only usable signal is structural: a crashed unit VANISHES
from the entity stream with no damage event explaining why.

THE CLASSIFICATION RULE
========================
Every `removeEntity` update is bucketed by whether that entity ID ever had an
`updateHp` event (oneof field 5, `{id, delta}`) at ANY point in its life:

  * HAS an hp-delta event  -> "damage_death". Verified over a 40-file random
    archive sample (1,740 removals): the LAST hp-delta before removal lands
    in the SAME round as the removal 94.3% of the time (1,641/1,740), with a
    short lag tail (1-4 rounds, 14 cases; one 20-round outlier) -- so keying
    on "ever damaged", not "damaged same round", avoids manufacturing false
    crash-candidates out of that lag tail.
  * NEVER had an hp-delta event, AND is a kind that runs code each round
    (core / builder_bot / gunner / sentinel / launcher, per CLAUDE.md's
    units-vs-buildings table) -> "crash_candidate".
  * NEVER had an hp-delta event, AND is a buildings-only kind (harvester /
    conveyor / splitter / barrier, which never execute `run()`) ->
    "friendly_removed". These can only vanish via a friendly builder's
    (free, instant, undamaged) destroy() action -- never a crash, because
    there is no code to crash.

WHAT THIS CANNOT SEE (read this before trusting a crash_candidate count)
==========================================================================
The replay format has no dedicated event for `self_destruct()`, `destroy()`,
or `resign()` -- none of the 16 `Update` oneof kinds in
`tools/replay_schema.md` is one of those three actions; they all resolve to
a bare `removeEntity` with no preceding `updateHp`, EXACTLY the same wire
signature as a crash. Consequently `crash_candidate` is a conflation of:

  1. a genuine uncaught-exception crash (what this tool is trying to find),
  2. a builder bot voluntarily calling self_destruct() (builder_bot only),
  3. a friendly builder destroying an allied TURRET building with destroy()
     -- gunner/sentinel/launcher are buildings as well as units, so a friendly
     teardown of one's own turret is indistinguishable from that turret's own
     run() crashing,
  4. (core only) a resign() call, which destroys the team's own core.

This tool CANNOT separate those four from replay bytes alone. What it DOES
do to keep the false-positive class as narrow as possible:
  * buildings-only kinds (harvester/conveyor/splitter/barrier) are EXCLUDED
    from crash_candidate entirely and reported separately as
    friendly_removed, since they cannot execute code and so cannot crash --
    measured at 34/84 (40%) of all no-damage removals in the same 40-file
    sample, i.e. a meaningful share of "vanished with no damage" events are
    not even unit-kind and would have inflated a naive count.
  * self_destruct() only applies to builder bots and destroy() only removes
    BUILDINGS (never a builder bot, which isn't a building) -- so a vanished
    builder_bot is crash-or-self-destruct only (2-way ambiguity), while a
    vanished gunner/sentinel/launcher/core is crash-or-friendly-destroy(-or-
    resign, core only) (2- or 3-way ambiguity). Neither ambiguity is
    resolved further; both are reported as crash_candidate, honestly labelled.

A crashed unit's TLE'd sibling turns (`botOutput.tled=True`) are NOT the same
event -- a CPU timeout skips that turn without destroying the unit (per
CLAUDE.md) -- and this tool does not cross-reference `botOutput` at all, so
it has no way to tell "the exception happened this round" from "some earlier
round"; it only knows the round of the eventual, unexplained removeEntity.

USAGE
=====
    .venv/bin/python tools/crash_census.py replay.replay26 [more.replay26 ...]
    .venv/bin/python tools/crash_census.py replay_archive/                # a dir: all *.replay26 in it
    .venv/bin/python tools/crash_census.py 'replay_archive/*_game_1.replay26'  # a glob (quote it)
    .venv/bin/python tools/crash_census.py --json replay.replay26
    .venv/bin/python tools/crash_census.py --sample 300 --seed 1 replay_archive/
    .venv/bin/python tools/crash_census.py --selftest

Reuses the shared wire-level primitives from tools/replay_census.py
(`fields`, `parse_entity`, `WIRE_LEN`) -- the same reuse pattern as
tools/field_deaths.py and tools/corpus/replay_events.py. Does not hand-roll
a protobuf parser.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, parse_entity, WIRE_LEN  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TEAM_NAME = {0: "A", 1: "B"}

# Kinds that RUN CODE each round (CLAUDE.md: "run() is called once per round
# for every living unit ... the core and every builder bot, gunner, sentinel,
# launcher"). Only these can raise an uncaught exception and be destroyed
# for it.
UNIT_KINDS = {"core", "builder_bot", "gunner", "sentinel", "launcher"}
# Buildings-only kinds never execute run() -- they can only vanish via a
# friendly builder's destroy() action, never a crash.
BUILDING_ONLY_KINDS = {"harvester", "conveyor", "splitter", "barrier"}

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"  # OpenSverige, per tools/field_deaths.py


def census_file(path: Path) -> dict:
    """Walk one replay and classify every removeEntity.

    Returns a dict with 'file', 'rounds', and three event lists, each a list
    of (round, team, kind) tuples: 'crashes' (crash_candidate),
    'damage_deaths', 'friendly_removed'.
    """
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        raise ValueError(f"{path}: no battlecode.Map (field 1) -- not a replay?")

    # Cores are seeded from map.cores, never emitted via placeEntity (see
    # tools/replay_schema.md gotchas) -- must be pre-registered or a
    # core_destroyed removeEntity has nothing to resolve against.
    ents: dict[int, tuple[int, str]] = {}
    for num, _wire, value in fields(map_buf):
        if num == 4:
            cid = cteam = None
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    cid = cv
                elif cn == 2:
                    cteam = cv
            if cid is not None:
                ents[cid] = (cteam, "core")

    damaged: set[int] = set()
    crashes: list[tuple[int, int, str]] = []
    damage_deaths: list[tuple[int, int, str]] = []
    friendly_removed: list[tuple[int, int, str]] = []

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                  # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in ents:           # rotation re-emit guard
                            continue
                        ents[e.id] = (e.team, e.kind)
                elif unum == 5:                                 # updateHp
                    eid = None
                    for n2, _w2, v2 in fields(ubuf):
                        if n2 == 1:
                            eid = v2
                    if eid is not None:
                        damaged.add(eid)
                elif unum == 3:                                 # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        team_kind = ents.pop(rv, None)
                        if team_kind is None:
                            continue                              # removed before we ever saw it placed
                        team, kind = team_kind
                        if rv in damaged:
                            damage_deaths.append((rnd, team, kind))
                        elif kind in UNIT_KINDS:
                            crashes.append((rnd, team, kind))
                        else:
                            friendly_removed.append((rnd, team, kind))

    return {
        "file": path.name,
        "path": str(path),
        "rounds": len(turn_bufs),
        "crashes": crashes,
        "damage_deaths": damage_deaths,
        "friendly_removed": friendly_removed,
    }


def _team_counts(events: list[tuple[int, int, str]]) -> dict[str, int]:
    c = Counter(TEAM_NAME.get(t, f"?{t}") for _r, t, _k in events)
    return {"A": c.get("A", 0), "B": c.get("B", 0)}


# --- CLI plumbing -------------------------------------------------------------

def collect_paths(args: list[str]) -> list[Path]:
    paths: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.replay26")))
        elif any(ch in a for ch in "*?[]"):
            import glob as _glob
            paths.extend(sorted(Path(x) for x in _glob.glob(a)))
        else:
            paths.append(p)
    return paths


def print_file_report(result: dict, out) -> None:
    crashes_by_team = _team_counts(result["crashes"])
    if crashes_by_team["A"] == 0 and crashes_by_team["B"] == 0:
        return  # keep bulk runs readable: silent on files with zero crash candidates
    out.write(f"{result['file']}  ({result['rounds']} rounds)\n")
    for team_label in ("A", "B"):
        rounds = sorted(r for r, t, _k in result["crashes"] if TEAM_NAME.get(t) == team_label)
        if not rounds:
            continue
        kinds = Counter(k for r, t, k in result["crashes"] if TEAM_NAME.get(t) == team_label)
        kind_str = ", ".join(f"{k}x{n}" for k, n in sorted(kinds.items()))
        rounds_str = ", ".join(str(r) for r in rounds[:20]) + (" ..." if len(rounds) > 20 else "")
        out.write(f"    team {team_label}: {len(rounds)} crash_candidate(s) [{kind_str}] "
                  f"at rounds {rounds_str}\n")


def summarize(results: list[dict]) -> dict:
    total_crashes_a = total_crashes_b = 0
    total_damage_a = total_damage_b = 0
    total_friendly_a = total_friendly_b = 0
    files_with_crash = 0
    for r in results:
        c = _team_counts(r["crashes"])
        d = _team_counts(r["damage_deaths"])
        f = _team_counts(r["friendly_removed"])
        total_crashes_a += c["A"]
        total_crashes_b += c["B"]
        total_damage_a += d["A"]
        total_damage_b += d["B"]
        total_friendly_a += f["A"]
        total_friendly_b += f["B"]
        if c["A"] or c["B"]:
            files_with_crash += 1
    return {
        "files": len(results),
        "files_with_crash_candidate": files_with_crash,
        "crash_candidates": {"A": total_crashes_a, "B": total_crashes_b,
                              "total": total_crashes_a + total_crashes_b},
        "damage_deaths": {"A": total_damage_a, "B": total_damage_b},
        "friendly_removed_buildings": {"A": total_friendly_a, "B": total_friendly_b},
    }


# --- self-test -----------------------------------------------------------------

def _run_fcode(team_a: str, team_b: str, map_path: str, replay_out: Path, seed: int) -> None:
    fcode = ROOT / ".venv" / "bin" / "fcode"
    cmd = [str(fcode), "run", team_a, team_b, map_path,
           "--replay", str(replay_out), "--seed", str(seed)]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"fcode run failed ({' '.join(cmd)}):\n{r.stdout}\n{r.stderr}")


def selftest(out=sys.stdout) -> bool:
    """Regenerate the positive and negative controls fresh and validate.

    Positive: bots/_probe_crash (team A) vs bots/_v127loki10 (team B) --
    every team-A builder bot raises ValueError on its first turn, so team A
    MUST show many crash_candidates and team B ~0.
    Negative: bots/_v127loki10 against itself -- neither side should crash,
    so BOTH teams MUST show ~0.

    A detector that fires on the positive control but not the negative is
    the only passing shape; firing on both or neither is a broken detector.
    """
    with tempfile.TemporaryDirectory(prefix="crash_census_selftest_") as tmp:
        tmp = Path(tmp)
        pos_path = tmp / "pos.replay26"
        neg_path = tmp / "neg.replay26"
        out.write("selftest: generating positive control "
                   "(bots/_probe_crash vs bots/_v127loki10, seed 4242)...\n")
        _run_fcode("bots/_probe_crash", "bots/_v127loki10", "maps/fjordgate.map26", pos_path, 4242)
        out.write("selftest: generating negative control "
                   "(bots/_v127loki10 vs bots/_v127loki10, seed 4242)...\n")
        _run_fcode("bots/_v127loki10", "bots/_v127loki10", "maps/fjordgate.map26", neg_path, 4242)

        pos_r = census_file(pos_path)
        neg_r = census_file(neg_path)
        pos_c = _team_counts(pos_r["crashes"])
        neg_c = _team_counts(neg_r["crashes"])

        out.write("\n  SELF-TEST RESULT (crash_candidate counts)\n")
        out.write(f"  {'':28s}{'team A':>10s}{'team B':>10s}\n")
        out.write(f"  {'positive (probe_crash/loki10)':28s}{pos_c['A']:>10d}{pos_c['B']:>10d}\n")
        out.write(f"  {'negative (loki10/loki10)':28s}{neg_c['A']:>10d}{neg_c['B']:>10d}\n")

        ok = pos_c["A"] > 0 and pos_c["B"] == 0 and neg_c["A"] == 0 and neg_c["B"] == 0
        if ok:
            out.write("\n  PASS: fires on the positive control's known-crashing side only, "
                       "silent on both negative-control sides.\n")
        else:
            out.write("\n  FAIL:\n")
            if not (pos_c["A"] > 0):
                out.write("    - positive control team A should be > 0, got "
                          f"{pos_c['A']}\n")
            if not (pos_c["B"] == 0):
                out.write(f"    - positive control team B should be 0, got {pos_c['B']}\n")
            if not (neg_c["A"] == 0 and neg_c["B"] == 0):
                out.write(f"    - negative control should be 0/0, got "
                          f"{neg_c['A']}/{neg_c['B']}\n")
        return ok


# --- main -----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\nUSAGE\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("replays", nargs="*", help=".replay26 file(s), a directory, or a glob")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true",
                     help="regenerate positive+negative controls and validate; exit 1 on failure")
    ap.add_argument("--sample", type=int, default=None,
                     help="randomly sample this many files instead of running all of them")
    ap.add_argument("--seed", type=int, default=1, help="RNG seed for --sample (default 1)")
    args = ap.parse_args()

    if args.selftest:
        ok = selftest(sys.stdout)
        return 0 if ok else 1

    if not args.replays:
        ap.error("give at least one replay path/dir/glob, or use --selftest")

    paths = collect_paths(args.replays)
    if not paths:
        print("no .replay26 files matched", file=sys.stderr)
        return 1

    sampled = False
    if args.sample is not None and args.sample < len(paths):
        rng = random.Random(args.seed)
        paths = rng.sample(paths, args.sample)
        sampled = True

    results = []
    errors = []
    for i, p in enumerate(paths):
        try:
            results.append(census_file(p))
        except Exception as exc:                                   # noqa: BLE001
            errors.append((p.name, f"{type(exc).__name__}: {exc}"))
        if len(paths) > 200 and (i + 1) % 500 == 0:
            print(f"  ...{i + 1}/{len(paths)}", file=sys.stderr, flush=True)

    summary = summarize(results)
    summary["sample"] = sampled
    summary["sample_n"] = len(paths) if sampled else None
    summary["errors"] = len(errors)

    if args.json:
        payload = {
            "summary": summary,
            "files": [
                {"file": r["file"], "rounds": r["rounds"],
                 "crashes": [{"round": rr, "team": TEAM_NAME.get(t, t), "kind": k}
                             for rr, t, k in r["crashes"]],
                 "damage_deaths": _team_counts(r["damage_deaths"]),
                 "friendly_removed": _team_counts(r["friendly_removed"])}
                for r in results
            ],
            "errors": errors,
        }
        print(json.dumps(payload, indent=2))
        return 1 if errors else 0

    for r in results:
        print_file_report(r, sys.stdout)

    print("\n=== SUMMARY ===")
    denom = f"{summary['files']} files" + (" (RANDOM SAMPLE, not the population)" if sampled else "")
    print(f"population: {denom}")
    print(f"files with >=1 crash_candidate: {summary['files_with_crash_candidate']}")
    cc = summary["crash_candidates"]
    print(f"crash_candidates: team A={cc['A']}  team B={cc['B']}  total={cc['total']}")
    dd = summary["damage_deaths"]
    print(f"damage_deaths (for scale):        team A={dd['A']}  team B={dd['B']}")
    fr = summary["friendly_removed_buildings"]
    print(f"friendly_removed (buildings-only, never a crash): team A={fr['A']}  team B={fr['B']}")
    if errors:
        print(f"\n{len(errors)} file(s) failed to parse:", file=sys.stderr)
        for name, msg in errors[:20]:
            print(f"  {name}: {msg}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
