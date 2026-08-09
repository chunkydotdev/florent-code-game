#!/usr/bin/env python3
"""TLE / CPU-budget census over the replay archive (read-only).

Why this exists
---------------
A turn that exceeds the 10ms per-unit CPU budget is **interrupted and silently
skipped** -- no crash, no traceback, no counter anywhere in our bot or in the
arena harness.  `builder-death-attribution-2026-08-09.md` (S4) records "2,681
timed-out turns in two replays of one match" in passing, and our worst measured
unit-turn is 12,967us against a 10,000us limit.  Neither number has ever been
followed up, and every plank this project has measured was measured on whatever
chassis those numbers imply.

`BotOutput` (Update field 9) carries `execTimeUs` (field 3) and `tled` (field 4)
for every unit-turn the engine ran.  stdout (field 2) is stripped from archived
replays, but these two are not.  So the archive can answer, exactly:

  * how often our units time out, per unit type and per round band
  * the same for the field, as a calibration baseline
  * the execTimeUs distribution, i.e. how much headroom is left before it bites

Output: one TSV row per (file, team, kind, band).  Join `file` -> our side via
`corpus/join.tsv` (`our_team`).

Usage:  .venv/bin/python tools/tle_census.py [--limit N] [--jobs N] [-o OUT.tsv]
"""
from __future__ import annotations

import argparse
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

BANDS = ((0, 100, "r0_99"), (100, 250, "r100_249"),
         (250, 500, "r250_499"), (500, 10 ** 9, "r500p"))


def band_of(rnd: int) -> str:
    for lo, hi, name in BANDS:
        if lo <= rnd < hi:
            return name
    return "r500p"


def decode(path: Path):
    """Return rows: (file, team, kind, band, turns, tled, exec_sum, exec_max, over10k)."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None

    team_of, kind_of = {}, {}
    for num, wire, value in fields(map_buf):
        if num != 4:
            continue
        cid = cteam = None
        for cn, _cw, cv in fields(value):
            if cn == 1:
                cid = cv
            elif cn == 2:
                cteam = cv
            elif cn == 3:
                read_pos(cv)
        if cid is not None:
            team_of[cid] = cteam or 0
            kind_of[cid] = "core"
    if len(team_of) != 2:
        return None

    # (team, kind, band) -> [turns, tled, exec_sum, exec_max, over10k]
    acc = {}
    for rnd, turn_buf in enumerate(turn_bufs):
        band = band_of(rnd)
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                     # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in kind_of:
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                elif unum == 9:                                   # botOutput
                    eid = exec_us = None
                    tled = False
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                        elif bn == 3:
                            exec_us = bv
                        elif bn == 4:
                            tled = bool(bv)
                    if eid is None:
                        continue
                    key = (team_of.get(eid, -1), kind_of.get(eid, "?"), band)
                    a = acc.get(key)
                    if a is None:
                        a = acc[key] = [0, 0, 0, 0, 0]
                    a[0] += 1
                    if tled:
                        a[1] += 1
                    if exec_us:
                        a[2] += exec_us
                        if exec_us > a[3]:
                            a[3] = exec_us
                        if exec_us > 10000:
                            a[4] += 1
    name = path.name
    return [(name, k[0], k[1], k[2], *v) for k, v in acc.items()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", default="replay_archive")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("-o", "--out", default="scratchpad/tle_census.tsv")
    args = ap.parse_args()

    files = sorted(Path(args.archive).glob("*.replay26"))
    if args.limit:
        files = files[: args.limit]
    print(f"{len(files)} replays, {args.jobs} jobs", file=sys.stderr)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    n_ok = n_bad = 0
    with open(args.out, "w") as fh:
        fh.write("file\tteam\tkind\tband\tturns\ttled\texec_sum\texec_max\tover10k\n")
        with Pool(args.jobs) as pool:
            for rows in pool.imap_unordered(decode, files, chunksize=8):
                if rows is None:
                    n_bad += 1
                    continue
                n_ok += 1
                for r in rows:
                    fh.write("\t".join(str(x) for x in r) + "\n")
    print(f"decoded {n_ok}, skipped {n_bad} -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
