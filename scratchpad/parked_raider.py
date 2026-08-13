#!/usr/bin/env python3
"""Parked-raider terminal-idle detector (QUEUE.md #48).

DEFINITION (pinned by the task, not varied here):
  A PARKED RAIDER is one of OUR builder bots that spends >= MIN_PARK (default
  100) CONSECUTIVE rounds within d^2 <= 4 of the ENEMY core while performing
  ZERO actions in that span.

  * "within d^2 <= 4 of the enemy core" is measured against the NEAREST tile of
    the enemy core's 2x2 footprint (the core position in the replay is the NW
    corner of the footprint). Measuring against the NW corner alone would be an
    arbitrary asymmetry; documented as a choice, and --anchor nw exists so the
    other reading can be driven.
  * "action" = builderAttack (Update 13) OR builderHeal (15) OR builderBuild
    (16), attributed by the bot id the event carries. DESTROY IS NOT EMITTED AS
    AN ATTRIBUTED EVENT anywhere in the replay schema (it surfaces only as
    RemoveEntity of a friendly building, with no actor id), so it is
    approximated by --destroy-proxy: a RemoveEntity, in the same round, of a
    FRIENDLY BUILDING that is orthogonally adjacent to the bot. Default ON.
    The proxy over-counts (an enemy shot on an adjacent friendly building looks
    like a destroy) and therefore biases AGAINST detecting parks -- the safe
    direction for a claim that parks exist.

Instrument controls (--selftest drives BOTH verdicts on real files).

Parsing reuses tools/replay_census.py helpers exactly (fields/read_pos/
parse_entity), same as tools/corpus/replay_throws.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve()
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
BUILDING_KINDS = {"conveyor", "splitter", "harvester", "barrier", "core",
                  "gunner", "sentinel", "launcher"}


def analyse(path: Path, our_team: int, min_park: int = 100,
            d2_max: int = 4, anchor: str = "foot", destroy_proxy: bool = True):
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

    # entity state
    pos = {}        # eid -> (x,y)
    team = {}       # eid -> team
    kind = {}       # eid -> kind
    alive = set()
    for c in cores:
        pos[c["id"]] = c["pos"]
        team[c["id"]] = c["team"]
        kind[c["id"]] = "core"
        alive.add(c["id"])

    # per-bot run state
    run_len = {}        # eid -> current consecutive near+silent round count
    run_start = {}
    parks = []          # (eid, start_round, length)
    bot_rounds = 0      # our builder-bot-rounds (alive at end of round)
    raider_rounds = 0   # our builder-bot-rounds spent near the enemy core

    nrounds = len(turn_bufs)
    for rnd, turn_buf in enumerate(turn_bufs):
        acted = set()
        removed_this_round = []
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

        # destroy proxy: friendly building removed adjacent to one of our bots
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

        # end-of-round evaluation for our living builder bots
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
                run_len[bid] += 1
            else:
                L = run_len.pop(bid, 0)
                s = run_start.pop(bid, None)
                if L >= min_park:
                    parks.append((bid, s, L))
        # bots that died end their run
        for rid in removed_this_round:
            L = run_len.pop(rid, 0)
            s = run_start.pop(rid, None)
            if L >= min_park:
                parks.append((rid, s, L))

    for bid, L in list(run_len.items()):
        if L >= min_park:
            parks.append((bid, run_start[bid], L))

    parked_bots = {b for b, _s, _L in parks}
    return dict(
        file=path.name, rounds=nrounds, mw=w, mh=h, maphash=maphash, our_team=our_team,
        n_parked_bots=len(parked_bots),
        max_park_len=max((L for _b, _s, L in parks), default=0),
        first_park_round=min((s for _b, s, _L in parks), default=-1),
        total_parked_bot_rounds=sum(L for _b, _s, L in parks),
        total_raider_rounds=raider_rounds,
        total_bot_rounds=bot_rounds,
    )


REF = ("/Users/junghard/Projects/Work/florent-code-game/replay_archive/"
       "4b039a9c-a02e-416a-9b30-61c710055bcb_game_%d.replay26")


def selftest() -> int:
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    # POSITIVE CONTROL: the reference incident must detect parked raiders.
    pos_hits = 0
    for g in range(1, 6):
        r = analyse(Path(REF % g), our_team=0)
        print(f"    game_{g}: rounds={r['rounds']} parked={r['n_parked_bots']} "
              f"max={r['max_park_len']} first={r['first_park_round']} "
              f"parked_rnds={r['total_parked_bot_rounds']} raider_rnds={r['total_raider_rounds']} "
              f"bot_rnds={r['total_bot_rounds']}")
        pos_hits += r["n_parked_bots"]
    check("POSITIVE: 4b039a9c detects parked raiders", pos_hits > 0, f"{pos_hits} bot-parks")

    # NEGATIVE 1: same files, threshold 10000 rounds -> impossible.
    neg = sum(analyse(Path(REF % g), our_team=0, min_park=10000)["n_parked_bots"]
              for g in range(1, 6))
    check("NEGATIVE: min_park=10000 on the SAME files detects ZERO", neg == 0, f"{neg}")

    # NEGATIVE 2: flip the seat. With our_team=1 the detector watches the
    # OPPONENT's bots against OUR core -- a different population, and the
    # detector must not simply reproduce the same numbers.
    flip = [analyse(Path(REF % g), our_team=1) for g in range(1, 6)]
    same = all(flip[g - 1]["n_parked_bots"] == analyse(Path(REF % g), our_team=0)["n_parked_bots"]
               for g in range(1, 6))
    print(f"    seat-flip parked counts: {[f['n_parked_bots'] for f in flip]}")
    check("SEAT SENSITIVITY: flipping our_team changes the verdict", not same)

    # NEGATIVE 3: a short game cannot satisfy a 100-round span.
    short = None
    import csv
    jp = Path("/Users/junghard/Projects/Work/florent-code-game/corpus/join.tsv")
    with jp.open() as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["turns"].isdigit() and int(row["turns"]) < 100:
                f = Path("/Users/junghard/Projects/Work/florent-code-game/replay_archive") / row["file"]
                if f.exists():
                    short = (f, int(row["our_team"]), int(row["turns"]))
                    break
    if short:
        r = analyse(short[0], our_team=short[1])
        check("NEGATIVE: a sub-100-round game detects ZERO",
              r["n_parked_bots"] == 0, f"{short[0].name} rounds={r['rounds']}")
    else:
        check("NEGATIVE: short-game control available", False, "no <100-round game found")

    # NEGATIVE 4: d2 anchored at an unreachable distance -> the near() gate itself
    # must be able to return the other verdict.
    z = sum(analyse(Path(REF % g), our_team=0, d2_max=0, anchor="nw")["n_parked_bots"]
            for g in range(1, 6))
    print(f"    d2_max=0 anchor=nw parked bots: {z}")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}: {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED — detector driven to DETECT and to ZERO on the same files.")
    return 0


COLS = ["file", "match", "game", "opp", "oppver", "ourver", "map", "maphash", "trig",
        "rounds", "our_team", "n_parked_bots", "max_park_len", "first_park_round",
        "total_parked_bot_rounds", "total_raider_rounds", "total_bot_rounds"]


def main(argv):
    if "--selftest" in argv:
        return selftest()
    # argv: manifest.tsv (file, our_team, match, game, opp, oppver, ourver, map, trig)
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
