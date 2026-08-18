#!/usr/bin/env python3
"""s51 CLOSURE autopsy -- why `orth_open == 0` is never reached on atoll/midgard.

Joins two independent instruments per game:
  * the REPLAY TAPE (seattape.tape) -- ground truth end-of-round occupancy of
    the enemy core's 8 orthogonal heal seats;
  * the bot's own FS DL stderr series -- what the raider SAW and what the
    funding/gate state was in that round.

Outputs, into this directory:
  seat_tape.tsv       one row per (game, round) with the 8-seat code string
  seat_life.tsv       one row per (game, seat) -- how the seat spent the siege
  closure_attrib.tsv  one row per game -- open-seat-round attribution
  dl_join.tsv         DL <-> tape agreement audit (the both-ways guard)

ATTRIBUTION RULE (stated once, applied uniformly, precedence top-down).
The unit is a SEAT-ROUND: one open orthogonal seat in one round in which the
raider was at the ring (a DL line exists).  Every open seat-round is assigned
to exactly ONE cause, first match wins:

  1 ENEMY-BUILDING  the seat carries an enemy building (conveyor/splitter/
                    turret/barrier).  Unbuildable and `_fs_denied`-open.
  2 ENEMY-BODY      an enemy builder bot stands on it (P6 squat).
  3 OUR-BUILDING    one of OUR conveyors/splitters sits on it (open by
                    `_fs_denied`, still unbuildable) -- self-inflicted.
  4 STARVED         seat is EMPTY and buildable, but the bank that round was
                    below one barrier (`ti < bar`).
  5 GATED           seat is EMPTY and buildable, bank >= 1 barrier, but the
                    binary seal gate was not open (`ti < need*bar + margin`).
  6 REACHABLE       seat is EMPTY, buildable, funded, gate open -- the raider
                    simply had not got to it (walk time / one-build-per-round /
                    adjacency).

Overlap is reported explicitly (a seat-round can satisfy 1 and 4 at once);
`closure_attrib.tsv` carries both the precedence-assigned counts and the raw
non-exclusive marginals.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from seattape import tape  # noqa: E402

LOGS = ROOT / "scratchpad/s51_evict_autopsy/logs"
FS_SEAL_MARGIN = 6

DL = re.compile(
    r"^FS DL (\d+) id (\d+) role (\S+) orth (\d+) need (\d+) ebody (\d+) "
    r"lau (\d+) ti (\d+) lcost (\d+) bar (\d+) obs (\d+) hist (\d+) pend (-?\d+)")
SEAL = re.compile(r"^FS SEAL (\d+) tile \((\d+), (\d+)\) n (\d+)")
CLEAR = re.compile(r"^FS CLEAR (\d+) tile \((\d+), (\d+)\) peck (\d+)")
EVICT = re.compile(r"^FS EVICT (\d+) from \((\d+), (\d+)\) to \((-?\d+), (-?\d+)\)")
EVICTOR = re.compile(r"^FS EVICTOR (\d+) at \((\d+), (\d+)\) cov (\d+)")
THROW = re.compile(r"^FS THROW (\d+) from \((\d+), (\d+)\) to \((\d+), (\d+)\)")
HOPB = re.compile(r"^FS HOPBUILD (\d+) at \((\d+), (\d+)\) lch \((\d+), (\d+)\)")


def read_log(path):
    """-> dict with dl {round: rec}, seals, clears, evicts, evictors, throws."""
    dl, seals, clears, evicts, evictors, throws, hops = {}, [], [], [], [], [], []
    with open(path, errors="replace") as fh:
        for line in fh:
            if not line.startswith("FS "):
                continue
            m = DL.match(line)
            if m:
                g = [int(x) if x.lstrip("-").isdigit() else x
                     for x in m.groups()]
                rec = dict(rnd=g[0], uid=g[1], role=g[2], orth=g[3], need=g[4],
                           ebody=g[5], lau=g[6], ti=g[7], lcost=g[8],
                           bar=g[9], obs=g[10], hist=g[11], pend=g[12])
                # one line per body; keep the FIRST (the sealer acts first)
                dl.setdefault(rec["rnd"], rec)
                continue
            for rx, sink in ((SEAL, seals), (CLEAR, clears), (EVICT, evicts),
                             (EVICTOR, evictors), (THROW, throws), (HOPB, hops)):
                m = rx.match(line)
                if m:
                    sink.append(tuple(int(x) for x in m.groups()))
                    break
    return dict(dl=dl, seals=seals, clears=clears, evicts=evicts,
                evictors=evictors, throws=throws, hops=hops)


def games():
    for p in sorted(LOGS.glob("v513_log-*.err")):
        stem = p.stem                      # v513_log-<map>-s<seed>-<seat>
        parts = stem.split("-")
        yield stem, parts[1], int(parts[2][1:]), parts[3], p


def main():
    tape_rows, life_rows, attrib_rows, join_rows = [], [], [], []
    for game, mapname, seed, seat, errp in games():
        rp = LOGS / f"{game}.replay26"
        seats, corners, trows = tape(rp, mapname, seat)
        log = read_log(errp)
        dl = log["dl"]
        by_round = {r: (s, d) for r, s, d in trows}
        nrounds = len(trows)

        # -- both-ways guard: DL orth vs tape orth at r-1 -------------------
        agree = disagree = 0
        for r, rec in sorted(dl.items()):
            prev = by_round.get(r - 1)
            if prev is None:
                continue
            t_open = sum(1 for c in prev[0] if c not in "Dd")
            if t_open == rec["orth"]:
                agree += 1
            else:
                disagree += 1
        join_rows.append(dict(game=game, map=mapname, dl_rounds=len(dl),
                              agree=agree, disagree=disagree,
                              agree_pct=round(100.0 * agree / max(1, agree + disagree), 1)))

        # -- seat life --------------------------------------------------------
        ring_rounds = sorted(dl)
        life = {i: defaultdict(int) for i in range(len(seats))}
        for r in ring_rounds:
            prev = by_round.get(r - 1)
            if prev is None:
                continue
            for i, c in enumerate(prev[0]):
                life[i][c] += 1
        for i, t in enumerate(seats):
            d = life[i]
            tot = sum(d.values())
            life_rows.append(dict(
                game=game, map=mapname, seat=seat, tile=f"{t[0]},{t[1]}",
                ring_rounds=tot,
                ours_block=d["D"], ours_body=d["d"], enemy_bldg=d["E"],
                enemy_body=d["b"], our_conv=d["o"], empty=d["."],
                closed_pct=round(100.0 * (d["D"] + d["d"]) / max(1, tot), 1)))

        # -- attribution ------------------------------------------------------
        cause = defaultdict(int)
        marg = defaultdict(int)
        seat_cause = {i: defaultdict(int) for i in range(len(seats))}
        open_seat_rounds = 0
        min_open = 99
        close_r = -1
        for r in ring_rounds:
            prev = by_round.get(r - 1)
            if prev is None:
                continue
            rec = dl[r]
            code = prev[0]
            t_open = sum(1 for c in code if c not in "Dd")
            if t_open < min_open:
                min_open = t_open
            if t_open == 0 and close_r < 0:
                close_r = r
            bar = rec["bar"] or 3
            need = rec["need"]
            funded_one = rec["ti"] >= bar
            gate_open = rec["ti"] >= need * bar + FS_SEAL_MARGIN
            for i, c in enumerate(code):
                if c in "Dd":
                    continue
                open_seat_rounds += 1
                if c == "E":
                    k = "1_enemy_bldg"
                elif c == "b":
                    k = "2_enemy_body"
                elif c == "o":
                    k = "3_our_bldg"
                elif not funded_one:
                    k = "4_starved"
                elif not gate_open:
                    k = "5_gated"
                else:
                    k = "6_reachable"
                cause[k] += 1
                seat_cause[i][k] += 1
                # non-exclusive marginals
                if c == "E":
                    marg["m_enemy_bldg"] += 1
                if c == "b":
                    marg["m_enemy_body"] += 1
                if c == "o":
                    marg["m_our_bldg"] += 1
                if not funded_one:
                    marg["m_starved"] += 1
                if not gate_open:
                    marg["m_gated"] += 1
                if c == "." and funded_one and gate_open:
                    marg["m_reachable"] += 1

        # attrition signature: how many times orth_open ROSE across ring rounds
        rises = falls = 0
        prevv = None
        for r in ring_rounds:
            pr = by_round.get(r - 1)
            if pr is None:
                continue
            v = sum(1 for c in pr[0] if c not in "Dd")
            if prevv is not None:
                if v > prevv:
                    rises += v - prevv
                elif v < prevv:
                    falls += prevv - v
            prevv = v
        # barrier deaths on seats: our 'D' -> non-D transitions
        bar_deaths = 0
        seatset = set(range(len(seats)))
        pcode = None
        for r, s, _d in trows:
            if pcode is not None:
                for i in seatset:
                    if pcode[i] == "D" and s[i] != "D":
                        bar_deaths += 1
            pcode = s
        attrib_rows.append(dict(
            game=game, map=mapname, seat=seat, seed=seed,
            ring_rounds=len(ring_rounds), open_seat_rounds=open_seat_rounds,
            min_orth=min_open if min_open < 99 else -1, close_r=close_r,
            orth_rises=rises, orth_falls=falls, our_seat_bldg_lost=bar_deaths,
            seals=len(log["seals"]), clears=len(log["clears"]),
            evicts=len(log["evicts"]), evictors=len(log["evictors"]),
            throws=len(log["throws"]),
            **{k: cause.get(k, 0) for k in
               ("1_enemy_bldg", "2_enemy_body", "3_our_bldg", "4_starved",
                "5_gated", "6_reachable")},
            **{k: marg.get(k, 0) for k in
               ("m_enemy_bldg", "m_enemy_body", "m_our_bldg", "m_starved",
                "m_gated", "m_reachable")}))

        for r, s, d in trows:
            tape_rows.append(dict(game=game, map=mapname, round=r,
                                  seatcode=s, diagcode=d,
                                  orth_open=sum(1 for c in s if c not in "Dd")))

    def dump(name, rows):
        if not rows:
            return
        cols = list(rows[0].keys())
        with open(HERE / name, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
        print(f"wrote {name}  ({len(rows)} rows)")

    dump("seat_tape.tsv", tape_rows)
    dump("seat_life.tsv", life_rows)
    dump("closure_attrib.tsv", attrib_rows)
    dump("dl_join.tsv", join_rows)


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main()
