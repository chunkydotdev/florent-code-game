#!/usr/bin/env python3
"""FINE-BAND shot / ammo / builder-action census, for the core-kill incidence cut.

WHY THIS EXISTS
---------------
`corpus/build_agg.tsv` and `corpus/econ.tsv` carry `shot`, `batk`, `batk_core`,
`ammo_converted` and the titanium snapshots -- but only in the coarse band
`r0-150`. The core-kill incidence cut needs a LANDMARK at r50 and r100, i.e. a
feature window that CLOSES BEFORE the outcome is plausibly determined (our
median core-kill lands at r151, so an "r0-150" feature is contemporaneous with
the outcome and is useless as a discriminator).

So this re-decodes ONLY the joined ladder files at 25-round granularity.
`corpus/events.tsv` already carries every BUILD and DEATH per round with
positions, so this decoder deliberately does NOT re-emit those.

TRAPS OBSERVED (see docs/research/corpus-howto.md):
  * placeEntity is re-emitted on gunner rotate -> a build is the FIRST
    placeEntity for an entity id. Guarded below (`ents` membership check), which
    matters here because we track positions to attribute fireTurret.
  * econ.tsv's `shots` and `deliveries` columns are all-zero (declared, never
    incremented). This decoder counts shots the way replay_builds.py does --
    fireTurret keyed by the shooter's CURRENT position matching a live
    gunner/sentinel -- and never touches `deliveries`.
  * updateHp.delta is a two's-complement varint. Not used here at all;
    builderAttack (Update field 13) is used instead.

Usage: fineband_econ.py OUT.tsv FILE [FILE ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

BAND_W = 25
LAST = "r150+"


def band(r: int) -> str:
    if r >= 150:
        return LAST
    lo = (r // BAND_W) * BAND_W
    return f"r{lo}-{lo + BAND_W}"


COUNTERS = ("shot", "batk", "batk_core", "ammo_converted", "n_convert",
            "heals", "bbuilds", "attacks", "tled", "turns_run")
SNAPS = ("ti_end", "ammo_end", "ti_collected_end")
COLS = ["file", "team", "band", *COUNTERS, *SNAPS]


def census(path: Path, out) -> None:
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    cores = []
    for num, _w, value in fields(map_buf):
        if num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        return
    corepos = {c["team"]: c["pos"] for c in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: (c["team"], "core") for c in cores}
    pos = {c["id"]: c["pos"] for c in cores}
    # turret id -> position index, so fireTurret can be attributed by position
    acc: dict[tuple[int, str], dict] = {}

    def cell(t, b):
        k = (t, b)
        if k not in acc:
            acc[k] = dict.fromkeys(COUNTERS + SNAPS, 0)
        return acc[k]

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                         # rotation re-emit
                            pos[e.id] = e.pos
                            continue
                        ents[e.id] = (e.team, e.kind)
                        pos[e.id] = e.pos
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos and to:
                        pos[eid] = to
                elif unum == 3:                                  # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        ents.pop(rv, None)
                        pos.pop(rv, None)
                elif unum == 12:                                 # fireTurret
                    frm = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                    if frm is None:
                        continue
                    for eid, (t, k) in ents.items():
                        if k in ("gunner", "sentinel") and pos.get(eid) == frm:
                            cell(t, b)["shot"] += 1
                            break
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    ent = ents.get(aid)
                    if ent is None or tgt is None:
                        continue
                    t = ent[0]
                    c = cell(t, b)
                    c["batk"] += 1
                    c["attacks"] += 1
                    if tgt in foot[1 - t]:
                        c["batk_core"] += 1
                elif unum == 14:                                 # coreConvertAmmo
                    d = {}
                    for k2, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k2] = v
                    c = cell(d.get(1, 0), b)
                    c["ammo_converted"] += d.get(2, 0)
                    c["n_convert"] += 1
                elif unum == 9:                                  # botOutput
                    d = {}
                    for k2, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k2] = v
                    ent = ents.get(d.get(1))
                    if ent is None:
                        continue
                    c = cell(ent[0], b)
                    c["turns_run"] += 1
                    if d.get(4):
                        c["tled"] += 1
                elif unum in (15, 16):                           # builderHeal / builderBuild
                    d = {}
                    for k2, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k2] = v
                    ent = ents.get(d.get(1))
                    if ent is None:
                        continue
                    c = cell(ent[0], b)
                    c["heals" if unum == 15 else "bbuilds"] += 1
                elif unum == 6:                                  # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn not in (1, 2):
                                continue
                            d = {}
                            for k2, w2, v in fields(tv):
                                if w2 == WIRE_VARINT:
                                    d[k2] = v
                            c = cell(tn - 1, b)
                            c["ti_end"] = d.get(1, 0)
                            c["ammo_end"] = d.get(7, 0)
                            c["ti_collected_end"] = d.get(4, 0)
    for (t, b), c in acc.items():
        out.write(f"{path.name}\t{t}\t{b}\t" +
                  "\t".join(str(c[k]) for k in COLS[3:]) + "\n")


def main(argv):
    out = open(argv[0], "w")
    out.write("\t".join(COLS) + "\n")
    bad = 0
    files = argv[1:]
    for i, p in enumerate(Path(x) for x in files):
        try:
            census(p, out)
        except Exception as exc:                                 # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 250 == 0:
            print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
