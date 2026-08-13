#!/usr/bin/env python3
"""Economy / ammo / CPU census — the streams nobody had read.

A field audit over 120 random archived replays found EIGHT unexploited Update
streams. This decoder takes the four that carry decisions:

  coreConvertAmmo (14)  exact titanium->ammo conversions, per team per round.
                        Turrets fire from the global ammo pool (gunner 4/shot,
                        sentinel 10/shot) and there is NO passive ammo income,
                        so this is the whole supply side of shooting.
  updatePlayers   (6)   per-round titanium / titaniumCollected / ammo, BOTH teams.
  botOutput       (9)   execTimeUs and the `tled` flag, per unit per round. A
                        TLE'd turn is silently lost -- 7,849 TLE events turned up
                        in the 120-replay sample.
  builderHeal(15)/builderBuild(16)  the rest of the builder action mix, so
                        "what did a builder turn buy" is finally complete.

Emits one row per file x team x round-band.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import guard_out, fields, WIRE_LEN, WIRE_VARINT  # noqa: E402


def band(r):
    return "r0-150" if r < 150 else "r150-200" if r < 200 else "r200-300" if r < 300 else "r300+"


BANDS = ("r0-150", "r150-200", "r200-300", "r300+")
COLS = ["file", "team", "band", "ammo_converted", "n_convert", "shots",
        "shots_gunner", "shots_sentinel",
        "heals", "builds", "attacks", "deliveries", "tled", "turns_run",
        "cpu_sum_us", "cpu_max_us", "ti_end", "ammo_end", "ti_collected_end"]


def census(path: Path, out):
    data = path.read_bytes()
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if not turn_bufs:
        return
    # entity -> team, so botOutput/heal/build rows can be attributed
    team_of: dict[int, int] = {}
    # ⭐ s36: FireTurret carries only {from, to} POSITIONS (schema line 94) — no
    # id, no team — which is why `shots` was a dead column (0 non-zero in
    # 195,020 rows; corpus_sanity.py:90 has documented it since s25). Attribute
    # by POSITION: turrets are buildings and do not move, so a pos->team map
    # built from placeEntity resolves the shooter exactly.
    pos_team: dict[tuple[int, int], int] = {}
    pos_kind: dict[tuple[int, int], int] = {}
    id_pos: dict[int, tuple[int, int]] = {}
    TURRET_FIELDS = {21: "gunner", 22: "sentinel"}
    acc: dict[tuple[int, str], dict] = {}

    def cell(t, b):
        k = (t, b)
        if k not in acc:
            acc[k] = dict.fromkeys(
                ("ammo_converted", "n_convert", "shots", "shots_gunner",
                 "shots_sentinel", "heals", "builds",
                 "attacks", "deliveries", "tled", "turns_run", "cpu_sum_us",
                 "cpu_max_us", "ti_end", "ammo_end", "ti_collected_end"), 0)
        return acc[k]

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        d, sub = {}, {}
                        for k, w2, v in fields(ebuf):
                            if w2 == WIRE_VARINT:
                                d[k] = v
                            elif w2 == WIRE_LEN:
                                sub[k] = v
                        if 1 in d:
                            team_of.setdefault(d[1], d.get(2, 0))
                        if 3 in sub:                            # Entity.position
                            pd = {k: v for k, w2, v in fields(sub[3])
                                  if w2 == WIRE_VARINT}
                            xy = (pd.get(1, 0), pd.get(2, 0))
                            pos_team[xy] = d.get(2, 0)
                            for fn in TURRET_FIELDS:
                                if fn in sub:
                                    pos_kind[xy] = fn
                            if 1 in d:
                                id_pos[d[1]] = xy
                elif unum == 3:                                 # removeEntity
                    d = {k: v for k, w2, v in fields(ubuf) if w2 == WIRE_VARINT}
                    xy = id_pos.pop(d.get(1), None)
                    if xy is not None:
                        pos_team.pop(xy, None)
                        pos_kind.pop(xy, None)
                elif unum == 14:                                # coreConvertAmmo
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    c = cell(d.get(1, 0), b)
                    c["ammo_converted"] += d.get(2, 0)
                    c["n_convert"] += 1
                elif unum == 9:                                 # botOutput
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    t = team_of.get(d.get(1))
                    if t is None:
                        continue
                    c = cell(t, b)
                    c["turns_run"] += 1
                    us = d.get(3, 0)
                    c["cpu_sum_us"] += us
                    if us > c["cpu_max_us"]:
                        c["cpu_max_us"] = us
                    if d.get(4):
                        c["tled"] += 1
                elif unum in (15, 16, 13):                      # heal / build / attack
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    t = team_of.get(d.get(1))
                    if t is None:
                        continue
                    c = cell(t, b)
                    c["heals" if unum == 15 else "builds" if unum == 16 else "attacks"] += 1
                elif unum == 12:                                # fireTurret
                    pd = None
                    for fn, fw, fv in fields(ubuf):
                        if fn == 1 and fw == WIRE_LEN:          # Pos from
                            pd = {k: v for k, w2, v in fields(fv)
                                  if w2 == WIRE_VARINT}
                            break
                    if pd is not None:
                        xy = (pd.get(1, 0), pd.get(2, 0))
                        t = pos_team.get(xy)
                        if t is not None:
                            cc = cell(t, b)
                            cc["shots"] += 1
                            k = pos_kind.get(xy)
                            if k == 21:
                                cc["shots_gunner"] += 1
                            elif k == 22:
                                cc["shots_sentinel"] += 1
                elif unum == 4:                                 # distributeResources
                    for _mn, _mw, _mv in fields(ubuf):
                        pass
                elif unum == 6:                                 # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn not in (1, 2):
                                continue
                            d = {}
                            for k, w2, v in fields(tv):
                                if w2 == WIRE_VARINT:
                                    d[k] = v
                            c = cell(tn - 1, b)
                            c["ti_end"] = d.get(1, 0)
                            c["ammo_end"] = d.get(7, 0)
                            c["ti_collected_end"] = d.get(4, 0)
    for (t, b), c in acc.items():
        out.write(f"{path.name}\t{t}\t{b}\t" +
                  "\t".join(str(c[k]) for k in COLS[3:]) + "\n")


def main(argv):
    guard_out(argv[0])
    out = open(argv[0], "w")
    out.write("\t".join(COLS) + "\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv[1:]):
        try:
            census(p, out)
        except Exception as exc:                                # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)-1} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(argv)-1} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
