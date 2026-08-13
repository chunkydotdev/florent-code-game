#!/usr/bin/env python3
"""Parked-raider detector, EXTENDED with per-bot-round CPU-time classification.

Base detector (unchanged logic, copied inline rather than imported so this file
stands alone next to v1): scratchpad/parked_raider.py — a PARKED RAIDER is one
of OUR builder bots spending >= MIN_PARK (default 100) CONSECUTIVE rounds
within d^2 <= 4 of the ENEMY core while performing ZERO actions.

EXTENSION (this file only): for every bot-round INSIDE a detected park run,
join the BotOutput event emitted that round for that bot id (Update field 9:
`BotOutput { int32 id = 1; string stdout = 2; uint32 execTimeUs = 3; bool tled
= 4; }`, per tools/replay_schema.md:85). stdout is stripped from platform
replays (CLAUDE.md), but id/execTimeUs/tled are not -- this reads only those.

CLASSIFICATION, thresholds are PARAMETERS not truths (--idle-us, --tle-us):
  IDLE_CHEAP : tled == 0 and execTimeUs <  idle_us   (default 1000)
  TLE        : tled != 0 or  execTimeUs >= tle_us    (default 9000)
  MID        : everything else
  MISSING    : no BotOutput event found for that (bot, round) at all -- kept
               as its own bucket, NOT folded into MID, so a join failure is
               visible rather than silently diluting the split.

Buffering strategy: botOutput events for the CURRENT round are parsed into a
dict once per round (outputs_this_round). While a bot is inside an active
near+silent streak we append (rnd, execTimeUs, tled) to a per-bot buffer; the
buffer is only kept until the streak breaks. If the streak reaches min_park it
is classified and folded into the game totals; otherwise the buffer is
dropped. This avoids holding a full game's BotOutput history in memory.

Entity-id note: BotOutput.id and placeEntity/moveBuilderBot ids share the same
namespace (tools/replay_census.py:397-402 already keys entities{} off the same
id straight from botOutput.id) -- this is not a new assumption, it is how the
one existing consumer of botOutput in this repo already reads it.
"""
from __future__ import annotations

import sys
import statistics
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

BUILDING_KINDS = {"conveyor", "splitter", "harvester", "barrier", "core",
                  "gunner", "sentinel", "launcher"}


def classify(exec_us, tled, idle_us, tle_us):
    if tled:
        return "TLE"
    if exec_us is None:
        return "MISSING"  # only reached if caller passes None through; see below
    if exec_us >= tle_us:
        return "TLE"
    if exec_us < idle_us:
        return "IDLE_CHEAP"
    return "MID"


def analyse(path: Path, our_team: int, min_park: int = 100,
            d2_max: int = 4, anchor: str = "foot", destroy_proxy: bool = True,
            idle_us: int = 1000, tle_us: int = 9000):
    """Return a per-game dict, or None if the file cannot be classified."""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None

    import hashlib
    maphash = hashlib.sha1(map_buf).hexdigest()[:10]
    cores, w, h = [], 0, 0
    for num, _w, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    corepos = {c["team"]: c["pos"] for c in cores}
    if len(corepos) != 2 or not (w and h):
        return None
    enemy = 1 - our_team
    ep = corepos[enemy]
    if anchor == "nw":
        anchors = [ep]
    else:
        anchors = [(ep[0] + dx, ep[1] + dy) for dx in (0, 1) for dy in (0, 1)]

    def near(p):
        return any((p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2 <= d2_max for a in anchors)

    pos = {}
    team = {}
    kind = {}
    alive = set()
    for c in cores:
        pos[c["id"]] = c["pos"]
        team[c["id"]] = c["team"]
        kind[c["id"]] = "core"
        alive.add(c["id"])

    run_len = {}
    run_start = {}
    run_buf = {}         # eid -> list[(rnd, execTimeUs|None, tled)]
    parks = []            # (eid, start_round, length)

    # classification totals for PARKED bot-rounds only
    cls_counts = {"IDLE_CHEAP": 0, "TLE": 0, "MID": 0, "MISSING": 0}
    cls_exec_values = []   # execTimeUs of parked rounds WITH a matched event

    bot_rounds = 0
    raider_rounds = 0

    nrounds = len(turn_bufs)

    def finish_run(bid, L, s):
        if L < min_park:
            run_buf.pop(bid, None)
            return
        parks.append((bid, s, L))
        buf = run_buf.pop(bid, [])
        for _rnd, exec_us, tled in buf:
            if exec_us is None and not tled:
                cls_counts["MISSING"] += 1
                continue
            c = classify(exec_us, tled, idle_us, tle_us)
            cls_counts[c] += 1
            if exec_us is not None:
                cls_exec_values.append(exec_us)

    for rnd, turn_buf in enumerate(turn_bufs):
        acted = set()
        removed_this_round = []
        outputs_this_round = {}   # eid -> (execTimeUs, tled)
        for _n, _w2, ubuf_outer in fields(turn_buf):
            for unum, _uw, ubuf in fields(ubuf_outer):
                if unum == 1:                               # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        pos[e.id] = e.pos
                        team[e.id] = e.team
                        kind[e.id] = e.kind
                        alive.add(e.id)
                elif unum == 2:                             # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        pos[eid] = to
                elif unum == 3:                             # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        removed_this_round.append(rv)
                elif unum in (13, 15, 16):                  # attack / heal / build
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            acted.add(av)
                            break
                elif unum == 9:                             # botOutput
                    bid_ = exec_us_ = None
                    tled_ = 0
                    for on, _ow, ov in fields(ubuf):
                        if on == 1:
                            bid_ = ov
                        elif on == 3:
                            exec_us_ = ov
                        elif on == 4:
                            tled_ = ov
                    if bid_ is not None:
                        outputs_this_round[bid_] = (exec_us_, tled_)

        if destroy_proxy:
            for rid in removed_this_round:
                if team.get(rid) != our_team or kind.get(rid) not in BUILDING_KINDS:
                    continue
                rp = pos.get(rid)
                if rp is None:
                    continue
                for bid in list(alive):
                    if kind.get(bid) != "builder_bot" or team.get(bid) != our_team:
                        continue
                    bp = pos.get(bid)
                    if bp is None:
                        continue
                    if abs(bp[0] - rp[0]) + abs(bp[1] - rp[1]) == 1:
                        acted.add(bid)

        for rid in removed_this_round:
            alive.discard(rid)

        for bid in list(alive):
            if kind.get(bid) != "builder_bot" or team.get(bid) != our_team:
                continue
            bot_rounds += 1
            p = pos.get(bid)
            if p is None:
                continue
            n = near(p)
            if n:
                raider_rounds += 1
            if n and bid not in acted:
                if bid not in run_len:
                    run_len[bid] = 0
                    run_start[bid] = rnd
                    run_buf[bid] = []
                run_len[bid] += 1
                run_buf[bid].append((rnd,) + outputs_this_round.get(bid, (None, 0)))
            else:
                L = run_len.pop(bid, 0)
                s = run_start.pop(bid, None)
                finish_run(bid, L, s)
        for rid in removed_this_round:
            L = run_len.pop(rid, 0)
            s = run_start.pop(rid, None)
            finish_run(rid, L, s)

    for bid, L in list(run_len.items()):
        finish_run(bid, L, run_start[bid])

    parked_bots = {b for b, _s, _L in parks}
    total_parked = sum(cls_counts.values())
    median_exec = statistics.median(cls_exec_values) if cls_exec_values else None
    return dict(
        file=path.name, rounds=nrounds, mw=w, mh=h, maphash=maphash, our_team=our_team,
        n_parked_bots=len(parked_bots),
        max_park_len=max((L for _b, _s, L in parks), default=0),
        first_park_round=min((s for _b, s, _L in parks), default=-1),
        total_parked_bot_rounds=sum(L for _b, _s, L in parks),
        total_raider_rounds=raider_rounds,
        total_bot_rounds=bot_rounds,
        parked_rounds_idle_cheap=cls_counts["IDLE_CHEAP"],
        parked_rounds_tle=cls_counts["TLE"],
        parked_rounds_mid=cls_counts["MID"],
        parked_rounds_missing=cls_counts["MISSING"],
        parked_rounds_exec_median=("" if median_exec is None else round(median_exec, 1)),
        _total_classified_check=total_parked,  # must equal total_parked_bot_rounds
    )


REF = ("/Users/junghard/Projects/Work/florent-code-game/replay_archive/"
       "4b039a9c-a02e-416a-9b30-61c710055bcb_game_%d.replay26")


def selftest() -> int:
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    # POSITIVE CONTROL: parked bots on the incident match must land ~200-280us,
    # tled=0, i.e. predominantly IDLE_CHEAP under the default thresholds.
    tot = {"IDLE_CHEAP": 0, "TLE": 0, "MID": 0, "MISSING": 0}
    exec_vals = []
    for g in range(1, 6):
        r = analyse(Path(REF % g), our_team=0)
        assert r["_total_classified_check"] == r["total_parked_bot_rounds"], \
            f"game_{g}: classified {r['_total_classified_check']} != parked {r['total_parked_bot_rounds']}"
        tot["IDLE_CHEAP"] += r["parked_rounds_idle_cheap"]
        tot["TLE"] += r["parked_rounds_tle"]
        tot["MID"] += r["parked_rounds_mid"]
        tot["MISSING"] += r["parked_rounds_missing"]
        print(f"    game_{g}: parked_rnds={r['total_parked_bot_rounds']} "
              f"idle={r['parked_rounds_idle_cheap']} tle={r['parked_rounds_tle']} "
              f"mid={r['parked_rounds_mid']} missing={r['parked_rounds_missing']} "
              f"median_exec={r['parked_rounds_exec_median']}")
    total_parked = sum(tot.values())
    idle_frac = tot["IDLE_CHEAP"] / total_parked if total_parked else 0
    check("POSITIVE: parked bot-rounds predominantly IDLE_CHEAP",
          total_parked > 0 and idle_frac > 0.9,
          f"{tot} frac={idle_frac:.3f}")

    # NEGATIVE CONTROL: non-parked "raider" bot-rounds (near enemy core, not
    # inside a completed park run) in the SAME games must NOT be predominantly
    # IDLE_CHEAP -- they include navigating bots actively acting/moving.
    neg_tot = {"IDLE_CHEAP": 0, "TLE": 0, "MID": 0, "MISSING": 0}
    for g in range(1, 6):
        neg = analyse_non_parked_raider_rounds(Path(REF % g), our_team=0)
        for k in neg_tot:
            neg_tot[k] += neg[k]
    neg_total = sum(neg_tot.values())
    neg_idle_frac = neg_tot["IDLE_CHEAP"] / neg_total if neg_total else 0
    print(f"    non-parked raider rounds: {neg_tot} frac_idle={neg_idle_frac:.3f}")
    check("NEGATIVE: non-parked raider bot-rounds NOT predominantly IDLE_CHEAP",
          neg_total > 0 and neg_idle_frac < 0.5,
          f"frac_idle={neg_idle_frac:.3f}")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}: {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED.")
    return 0


def analyse_non_parked_raider_rounds(path: Path, our_team: int, min_park: int = 100,
                                      d2_max: int = 4, anchor: str = "foot",
                                      idle_us: int = 1000, tle_us: int = 9000):
    """Control-only helper: classify bot-rounds that are near the enemy core
    but are NOT part of a completed (>=min_park) park run for that bot -- the
    "navigating raider" population used as the negative control. Kept
    separate from analyse() (which only buffers rounds that end up parked) to
    avoid paying this extra bookkeeping cost on the full 7,203-file sweep.
    """
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    cores, w, h = [], 0, 0
    for num, _w, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    corepos = {c["team"]: c["pos"] for c in cores}
    enemy = 1 - our_team
    ep = corepos[enemy]
    anchors = [(ep[0] + dx, ep[1] + dy) for dx in (0, 1) for dy in (0, 1)] if anchor != "nw" else [ep]

    def near(p):
        return any((p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2 <= d2_max for a in anchors)

    pos, team, kind, alive = {}, {}, {}, set()
    for c in cores:
        pos[c["id"]] = c["pos"]
        team[c["id"]] = c["team"]
        kind[c["id"]] = "core"
        alive.add(c["id"])

    run_len, run_start = {}, {}
    # per-bot-round record: (rnd, active, exec_us, tled) -- active = acted or moved
    all_near_rounds = {}  # eid -> list[(rnd, active, exec_us, tled)]
    parked_ranges = {}    # eid -> list[(start, end_exclusive)]

    for rnd, turn_buf in enumerate(turn_bufs):
        acted = set()
        moved = set()
        removed_this_round = []
        outputs_this_round = {}
        for _n, _w2, ubuf_outer in fields(turn_buf):
            for unum, _uw, ubuf in fields(ubuf_outer):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        pos[e.id] = e.pos
                        team[e.id] = e.team
                        kind[e.id] = e.kind
                        alive.add(e.id)
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        pos[eid] = to
                        moved.add(eid)
                elif unum == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        removed_this_round.append(rv)
                elif unum in (13, 15, 16):
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            acted.add(av)
                            break
                elif unum == 9:
                    bid_ = exec_us_ = None
                    tled_ = 0
                    for on, _ow, ov in fields(ubuf):
                        if on == 1:
                            bid_ = ov
                        elif on == 3:
                            exec_us_ = ov
                        elif on == 4:
                            tled_ = ov
                    if bid_ is not None:
                        outputs_this_round[bid_] = (exec_us_, tled_)

        for rid in removed_this_round:
            for bid in list(alive):
                if kind.get(bid) != "builder_bot" or team.get(bid) != our_team:
                    continue
                rp = pos.get(rid)
                bp = pos.get(bid)
                if rp is None or bp is None:
                    continue
                if team.get(rid) == our_team and kind.get(rid) in BUILDING_KINDS \
                        and abs(bp[0] - rp[0]) + abs(bp[1] - rp[1]) == 1:
                    acted.add(bid)
        for rid in removed_this_round:
            alive.discard(rid)

        for bid in list(alive):
            if kind.get(bid) != "builder_bot" or team.get(bid) != our_team:
                continue
            p = pos.get(bid)
            if p is None:
                continue
            n = near(p)
            if n:
                ev = outputs_this_round.get(bid, (None, 0))
                active = (bid in acted) or (bid in moved)
                all_near_rounds.setdefault(bid, []).append((rnd, active, ev[0], ev[1]))
            if n and bid not in acted:
                if bid not in run_len:
                    run_len[bid] = 0
                    run_start[bid] = rnd
                run_len[bid] += 1
            else:
                L = run_len.pop(bid, 0)
                s = run_start.pop(bid, None)
                if L >= min_park:
                    parked_ranges.setdefault(bid, []).append((s, s + L))
        for rid in removed_this_round:
            L = run_len.pop(rid, 0)
            s = run_start.pop(rid, None)
            if L >= min_park:
                parked_ranges.setdefault(rid, []).append((s, s + L))
    for bid, L in list(run_len.items()):
        s = run_start[bid]
        if L >= min_park:
            parked_ranges.setdefault(bid, []).append((s, s + L))

    counts = {"IDLE_CHEAP": 0, "TLE": 0, "MID": 0, "MISSING": 0}
    for bid, recs in all_near_rounds.items():
        ranges = parked_ranges.get(bid, [])
        for rnd, active, exec_us, tled in recs:
            if not active:
                continue  # not genuinely navigating (acting/moving) this round
            if any(s <= rnd < e for s, e in ranges):
                continue  # this near-round is part of a completed park; excluded
            if exec_us is None and not tled:
                counts["MISSING"] += 1
                continue
            counts[classify(exec_us, tled, idle_us, tle_us)] += 1
    return counts


COLS = ["file", "match", "game", "opp", "oppver", "ourver", "map", "maphash", "trig",
        "rounds", "our_team", "n_parked_bots", "max_park_len", "first_park_round",
        "total_parked_bot_rounds", "total_raider_rounds", "total_bot_rounds",
        "parked_rounds_idle_cheap", "parked_rounds_tle", "parked_rounds_mid",
        "parked_rounds_missing", "parked_rounds_exec_median"]


def main(argv):
    if "--selftest" in argv:
        return selftest()
    import csv
    man = Path(argv[0])
    arch = Path("/Users/junghard/Projects/Work/florent-code-game/replay_archive")
    out = sys.stdout
    out.write("\t".join(COLS) + "\n")
    bad = 0
    rows = list(csv.DictReader(man.open(), delimiter="\t"))
    for i, row in enumerate(rows):
        p = arch / row["file"]
        try:
            r = analyse(p, our_team=int(row["our_team"]))
            if r is None:
                bad += 1
                continue
            r.update(match=row["match"], game=row["game"], opp=row["opp"],
                     oppver=row["oppver"], ourver=row["ourver"], map=row["map"],
                     trig=row["trig"])
            out.write("\t".join(str(r[c]) for c in COLS) + "\n")
        except Exception as exc:  # noqa: BLE001
            bad += 1
            print(f"ERR {row['file']}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(rows)} ({bad} err)", file=sys.stderr, flush=True)
    print(f"done {len(rows)} files, {bad} errors/unclassifiable", file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
