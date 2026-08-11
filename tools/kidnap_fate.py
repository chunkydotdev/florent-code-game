#!/usr/bin/env python3
"""kidnap_fate.py -- what happens to an ENEMY builder after WE throw it?

WHY THIS EXISTS.  `corpus/throws.tsv` records **36,275 throws of enemy builder
bots by us** and its victim-fate column `life` is the sentinel **-1 in 36,275 of
36,275**.  The cause is one line: `tools/corpus/replay_throws.py:134` adds a
record to `active` only `if kind == "INSERT"`, and only `active` records ever get
`close()` called -- so the decoder follows OUR OWN ferried bots and never follows
the enemy bots we eject.  The column works (3,133 of our own throws lived >3
rounds, 523 died within 3); it is blank for exactly the population the plank is
about.

WHAT IT MEASURES.  For every EXILE (we throw an enemy builder), the victim's fate:
  * `rounds_survived`   -- rounds between the throw and the victim's removeEntity
  * `no_damage_removal` -- removed with NO updateHp ever seen for that entity.
    Same signature `tools/crash_census.py` uses; this is a per-ENTITY join of that
    detector onto the throw stream rather than a new decoder.

⛔ THE CONTROL IS THE WHOLE EXPERIMENT, AND IT IS MATCHED.  An unmatched contrast
reports that builders near map borders die more.  That is true, it is geometry,
and it is not the plank.  Each thrown victim is matched to enemy builders of the
SAME FILE, alive at the SAME ROUND, not thrown, and bucketed by distance-to-their-
own-core -- so the comparison holds map, game phase and position constant and
varies only "was it thrown".

⛔ WHAT A RESULT DOES **NOT** MEAN.  `no_damage_removal` is a CONFLATION, and
`crash_census.py`'s own header says so: it cannot separate a genuine uncaught
exception from a `self_destruct()` (measured at ~40% of no-damage removals in a
40-file sample).  An elevation is an ASSOCIATION between being thrown and
vanishing without damage.  Under rule 6 it may PRIORITISE a live leg; it may not
CLOSE the road on its own.

DECISION RULE -- pre-committed in `docs/research/SPEC-kidnap-victim-fate-2026-08-11.md`
BEFORE this script was written:
  * thrown arm elevated over matched control  => displacement channel pays,
    a live leg is justified (target band already gated: 5-0 pays +12.5..+21.5)
  * no elevation at this n                    => the channel is dead at any dose
    a leg could deliver; QUEUE #5 drops below #7. A real close, zero rated cost.

DRIVEN BOTH WAYS: `--selftest` builds two synthetic fixtures -- one where thrown
victims always vanish undamaged, one where they never do -- and asserts the
estimator separates them.  A checker that has never returned the other verdict has
not been seen to check.
"""
from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "corpus"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

REPO = HERE.parent
ARCHIVE = REPO / "replay_archive"
META = REPO / "corpus" / "meta_join.tsv"

SIDE = {"a": 0, "b": 1}
NEAR, MID = 32, 128  # distance-to-own-core buckets (d^2)


def us_side_map() -> dict[str, int]:
    """file -> which team index is US. Only files where we played."""
    out: dict[str, int] = {}
    if not META.exists():
        return out
    with META.open() as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            s = SIDE.get((r.get("us_side") or "").strip().lower())
            if s is not None:
                out[r["file"]] = s
    return out


def d2(a, b) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def bucket(dist: int) -> str:
    return "near" if dist <= NEAR else ("mid" if dist <= MID else "far")


def analyse(path: Path, us: int) -> list[dict]:
    """One row per ENEMY builder-bot life, thrown or not. Never raises on shape."""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return []

    corepos: dict[int, tuple[int, int]] = {}
    for num, _w, value in fields(map_buf):
        if num == 4:
            # ⛔ proto3 OMITS default-valued fields, so team 0's `team` field is
            # ABSENT from the wire -- the first core arrives as {id, pos} with no
            # team at all. Defaulting cteam to None and requiring it dropped team
            # 0 on every replay, left corepos with one entry, and returned zero
            # rows with zero errors: a silent empty that looks exactly like "the
            # measurement found nothing". Default to 0, which IS the wire's
            # meaning of absent.
            cteam, cpos = 0, None
            for cn, _cw, cv in fields(value):
                if cn == 2:
                    cteam = cv
                elif cn == 3:
                    cpos = read_pos(cv)
            if cpos is not None:
                corepos[cteam] = cpos
    if len(corepos) < 2:
        return []
    enemy = 1 - us

    pos: dict[int, tuple[int, int]] = {}
    team: dict[int, int] = {}
    kind: dict[int, str] = {}
    damaged: set[int] = set()
    born: dict[int, int] = {}
    thrown_at: dict[int, int] = {}       # victim eid -> round WE threw it
    removed: dict[int, int] = {}
    nrounds = len(turn_bufs)

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, update_buf in fields(turn_buf):
            for unum, _uw, ubuf in fields(update_buf):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id not in team:
                            team[e.id], kind[e.id], born[e.id] = e.team, e.kind, rnd
                        pos[e.id] = e.pos
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is None or to is None:
                        continue
                    frm = pos.get(eid)
                    pos[eid] = to
                    # A THROW is a >1-tile displacement in a single update.
                    # Same geometry replay_throws.py uses; not re-derived.
                    if frm is not None and d2(frm, to) > 1 and team.get(eid) == enemy:
                        thrown_at.setdefault(eid, rnd)
                elif unum == 5:                                  # updateHp
                    for n2, _w2b, v2 in fields(ubuf):
                        if n2 == 1:
                            damaged.add(v2)
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1 and rv not in removed:
                            removed[rv] = rnd

    rows = []
    for eid, t in team.items():
        if t != enemy or kind.get(eid) != "builder_bot":
            continue
        rem = removed.get(eid)
        thr = thrown_at.get(eid)
        # Reference round: the throw for the treated arm, birth for the control.
        # Matching is done on the round the clock starts, so the arms are compared
        # at the same game phase rather than over whole lifetimes.
        p = pos.get(eid)
        rows.append({
            "file": path.name,
            "eid": eid,
            "thrown": 1 if thr is not None else 0,
            "born_rnd": born.get(eid, 0),
            "thrown_rnd": thr if thr is not None else -1,
            "removed_rnd": rem if rem is not None else -1,
            "survived_to_end": 0 if rem is not None else 1,
            "undamaged": 1 if eid not in damaged else 0,
            "no_damage_removal": 1 if (rem is not None and eid not in damaged) else 0,
            "dist_bucket": bucket(d2(p, corepos[enemy])) if p else "unk",
            "rounds": nrounds,
        })
    return rows


def summarise(rows: list[dict], naive: bool = False) -> dict:
    """RISK-SET MATCHED contrast.

    ⛔ THE BIAS THIS EXISTS TO REMOVE, found by the side lane against the FIRST
    version of this estimator, which had already been published as a closure.
    A victim must be ALIVE at round R to be thrown -- and "alive" includes "has
    not yet been removed undamaged", WHICH IS THE OUTCOME. So the thrown arm was
    conditioned on not having crashed, while controls were clocked from BIRTH and
    were not. **The thrown group was depleted of crash-prone bots BY
    CONSTRUCTION, and the depletion runs in exactly the direction of the finding.**
    The old design could not distinguish "throwing does not cause crashes" from
    "bots that survive long enough to be thrown were never going to crash".
    Compounding it, the outcome was a LIFETIME property, so the pre-throw portion
    of a victim's life sat inside the outcome window -- a period during which the
    throw cannot have caused anything.

    THE FIX, and it is the standard one for immortal time: for each throw at round
    R, admit as controls only enemy builders ALIVE AND NOT YET REMOVED AT R, and
    define the outcome for BOTH arms as **removed-undamaged strictly AFTER R**.
    Both arms then share one clock and one risk set.

    `naive=True` reproduces the OLD biased estimator, so the selftest can drive
    the difference rather than assert it.
    """
    by_file: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_file[r["file"]].append(r)

    tn = td = cn = cd = 0
    used = 0
    for _f, rs in by_file.items():
        thrown = [r for r in rs if r["thrown"] and r["dist_bucket"] != "unk"]
        for v in thrown:
            R = v["thrown_rnd"]
            if naive:
                pool = [c for c in rs if not c["thrown"] and c["dist_bucket"] == v["dist_bucket"]
                        and c["born_rnd"] // 100 == R // 100]
                out_v = v["no_damage_removal"]
            else:
                # RISK SET: not thrown, born before R, still alive at R.
                pool = [c for c in rs
                        if not c["thrown"]
                        and c["dist_bucket"] == v["dist_bucket"]
                        and c["born_rnd"] <= R
                        and (c["removed_rnd"] == -1 or c["removed_rnd"] > R)]
                out_v = 1 if (v["removed_rnd"] > R and v["undamaged"]) else 0
            if not pool:
                continue                                # no risk set -> excluded
            used += 1
            tn += 1
            td += out_v
            for c in pool:
                cn += 1
                cd += (c["no_damage_removal"] if naive else
                       (1 if (c["removed_rnd"] > R and c["undamaged"]) else 0))
    tp = td / tn if tn else float("nan")
    cp = cd / cn if cn else float("nan")
    return {
        "strata_used": used, "strata_total": len(rows),
        "thrown_n": tn, "thrown_nodmg": td, "thrown_rate": tp,
        "ctrl_n": cn, "ctrl_nodmg": cd, "ctrl_rate": cp,
        "delta_pp": (tp - cp) * 100 if tn and cn else float("nan"),
    }


def _row(f, eid, thrown, born, thr, rem, undam, bucket_="mid"):
    return dict(file=f, eid=eid, thrown=thrown, born_rnd=born, thrown_rnd=thr,
                removed_rnd=rem, survived_to_end=0 if rem != -1 else 1,
                undamaged=undam,
                no_damage_removal=1 if (rem != -1 and undam) else 0,
                dist_bucket=bucket_, rounds=400)


def _fixture(always: bool) -> list[dict]:
    """Thrown victims vanish undamaged always / never. Timing held equal."""
    rows = []
    for f in range(30):
        for i in range(4):
            rows.append(_row(f"f{f}", i, 1, 40, 50, 60, 1 if always else 0))
            rows.append(_row(f"f{f}", 100 + i, 0, 40, -1, 60, 0))
    return rows


def _fixture_immortal() -> list[dict]:
    """⭐ THE CELL THAT CATCHES THE BIAS — specified by the side lane.

    TRUE EFFECT IS ZERO. Every bot has the same constant per-round hazard of
    vanishing undamaged. But victims can only be THROWN if they survived to r50,
    while controls are observed from birth at r0 -- so controls accumulate crash
    events in r0..50 that victims could never have had.

    A NAIVE (birth-clocked, whole-life-outcome) estimator MUST read NEGATIVE here.
    The RISK-SET estimator MUST read ~ZERO, because it only counts events after
    the throw round and only admits controls still alive at that round.
    """
    rows = []
    for f in range(60):
        # controls: half die undamaged EARLY (r10-40), before any throw happens
        for i in range(6):
            rows.append(_row(f"f{f}", 200 + i, 0, 0, -1, 10 + i * 5, 1))
        # controls: the rest survive past r50 and then die damaged
        for i in range(6):
            rows.append(_row(f"f{f}", 300 + i, 0, 0, -1, 120, 0))
        # victims: alive at r50 by construction, then die damaged (true effect 0)
        for i in range(4):
            rows.append(_row(f"f{f}", i, 1, 0, 50, 120, 0))
    return rows


def selftest() -> int:
    rc = 0
    print("SELFTEST 1 — the estimator must separate an effect from no effect.")
    hi, lo = summarise(_fixture(True)), summarise(_fixture(False))
    print(f"  all-thrown-vanish  : thrown {hi['thrown_rate']:.1%} vs ctrl {hi['ctrl_rate']:.1%}"
          f"   delta {hi['delta_pp']:+.1f}pp")
    print(f"  none-thrown-vanish : thrown {lo['thrown_rate']:.1%} vs ctrl {lo['ctrl_rate']:.1%}"
          f"   delta {lo['delta_pp']:+.1f}pp")
    ok1 = hi["delta_pp"] > 50 and abs(lo["delta_pp"]) < 1e-9
    print("  ✅ PASS" if ok1 else "  ⛔ FAIL")

    print("\nSELFTEST 2 — IMMORTAL-TIME BIAS. True effect is ZERO; victims are")
    print("  alive-at-r50 by construction while controls are watched from birth.")
    fx = _fixture_immortal()
    nv, rs = summarise(fx, naive=True), summarise(fx, naive=False)
    print(f"  NAIVE  (birth-clocked, whole-life outcome): delta {nv['delta_pp']:+.2f}pp"
          f"   <- must be NEGATIVE, i.e. the bias is real and reproducible")
    print(f"  RISK-SET (post-throw window, alive-at-R)  : delta {rs['delta_pp']:+.2f}pp"
          f"   <- must be ~ZERO, i.e. the fix removes it")
    ok2 = nv["delta_pp"] < -5 and abs(rs["delta_pp"]) < 1.0
    print("  ✅ PASS — the biased estimator fails this cell and the fixed one survives it."
          if ok2 else
          "  ⛔ FAIL — either the bias does not reproduce or the fix does not remove it.")

    if not (ok1 and ok2):
        print("\n⛔ DO NOT TRUST THIS TOOL'S OUTPUT.")
        rc = 1
    else:
        print("\n✅ Both cells pass.")
    return rc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=400, help="replays to scan (0 = all)")
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--out", default="", help="write per-victim rows to this TSV")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    us = us_side_map()
    if not us:
        print("no meta_join / no us_side — cannot identify our side", file=sys.stderr)
        return 2
    files = [p for p in ARCHIVE.glob("*.replay26") if p.name in us]
    random.Random(args.seed).shuffle(files)
    if args.limit:
        files = files[: args.limit]
    print(f"scanning {len(files)} of our replays (seed {args.seed})")

    rows, bad = [], 0
    for i, p in enumerate(files, 1):
        try:
            rows.extend(analyse(p, us[p.name]))
        except Exception:
            bad += 1
        if i % 50 == 0:
            print(f"  ...{i}/{len(files)}", end="\r", file=sys.stderr)

    s = summarise(rows)
    thrown_rows = [r for r in rows if r["thrown"]]
    print(f"\nenemy builder lives seen : {len(rows)}   of which THROWN by us: {len(thrown_rows)}")
    print(f"unreadable replays       : {bad}")
    print(f"matched strata used      : {s['strata_used']} of {s['strata_total']}"
          f"   (a stratum counts only if it holds BOTH arms)")
    print("\nNO-DAMAGE REMOVAL, matched on (file, distance bucket, 100-round band):")
    print(f"  THROWN   {s['thrown_nodmg']:>6} / {s['thrown_n']:<6} = {s['thrown_rate']:.2%}")
    print(f"  CONTROL  {s['ctrl_nodmg']:>6} / {s['ctrl_n']:<6} = {s['ctrl_rate']:.2%}")
    print(f"  DELTA    {s['delta_pp']:+.2f} pp")
    print("\n⚠ no_damage_removal CONFLATES an uncaught exception with self_destruct()"
          "\n  (~40% of no-damage removals in crash_census's own 40-file sample).")
    print("⚠ An elevation is an ASSOCIATION. Under rule 6 it may PRIORITISE a live"
          "\n  leg; it may NOT close the road on its own.")

    if args.out:
        with open(args.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {len(rows)} rows -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
