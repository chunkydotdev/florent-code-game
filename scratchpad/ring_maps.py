#!/usr/bin/env python3
"""Name the leg's maps by EXACT TILE-ROW FINGERPRINT against maps/*.map26,
then give per-team core anchors and derived ring sizes.

Fingerprint = (width, height, tuple of every tile value in row order) taken from
the Map message. Cores/symmetry/entities are deliberately EXCLUDED from the
fingerprint so it is terrain only; the cores are then reported separately.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from replay_census import fields, read_pos, packed_varints, WIRE_LEN  # noqa
from ring_read import ids_from_file, ring_tiles, ARCHIVE, OUR_TEAM_ID  # noqa


def parse_map(buf: bytes):
    w = h = 0
    rows, cores = [], []
    for num, wire, value in fields(buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3 and wire == WIRE_LEN:
            tiles = []
            for tn, tw, tv in fields(value):
                if tn == 1:
                    tiles.extend(packed_varints(tv) if tw == WIRE_LEN else [tv])
            rows.append(tuple(tiles))
        elif num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(2, 0), read_pos(d[3])))
    return w, h, tuple(rows), cores


def map_from_replay(path: Path):
    data = path.read_bytes()
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            return parse_map(value)
    return None


def main():
    lib = {}
    for mp in sorted((ROOT / "maps").glob("*.map26")):
        w, h, rows, cores = parse_map(mp.read_bytes())
        lib[(w, h, rows)] = (mp.stem, cores)
    print(f"fingerprinted {len(lib)} map files from maps/*.map26\n")

    seen = defaultdict(Counter)     # mapname -> Counter of arm
    coreinfo = {}
    unmatched = Counter()
    for arm, f in (("loki16", "scratchpad/arm_loki16.txt"),
                   ("v104", "scratchpad/arm_v104.txt")):
        for mid in ids_from_file(Path(f)):
            for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
                w, h, rows, cores = map_from_replay(rp)
                hit = lib.get((w, h, rows))
                if hit is None:
                    unmatched[(w, h)] += 1
                    name = f"UNMATCHED_{w}x{h}"
                else:
                    name = hit[0]
                seen[name][arm] += 1
                coreinfo.setdefault(name, (w, h, cores))

    print(f"{'map (exact tile fingerprint)':<28}{'w x h':>9}{'loki16':>8}{'v104':>7}"
          f"   core anchors and ring sizes per team")
    for name in sorted(seen, key=lambda n: coreinfo[n][0] * coreinfo[n][1]):
        w, h, cores = coreinfo[name]
        parts = []
        for team, pos in sorted(cores):
            r = ring_tiles(pos, w, h)
            parts.append(f"team{'AB'[team]} core@{pos} ring={len(r)}")
        print(f"{name:<28}{f'{w}x{h}':>9}{seen[name]['loki16']:>8}"
              f"{seen[name]['v104']:>7}   {'   |   '.join(parts)}")
    if unmatched:
        print(f"\n  ** UNMATCHED fingerprints: {dict(unmatched)} — these did NOT "
              f"byte-match any maps/*.map26 terrain")

    # negative control on the fingerprint itself: perturb one tile, must miss
    probe = next(iter(lib))
    bad = (probe[0], probe[1],
           tuple([tuple([(probe[2][0][0] + 1) % 3] + list(probe[2][0][1:]))]
                 + list(probe[2][1:])))
    print(f"\n  FINGERPRINT CONTROL: flipping ONE tile of '{lib[probe][0]}' -> "
          f"{'MISSES (good)' if bad not in lib else '** still matches — fingerprint is not exact **'}")


if __name__ == "__main__":
    main()
