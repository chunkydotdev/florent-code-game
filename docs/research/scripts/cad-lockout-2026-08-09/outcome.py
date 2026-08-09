#!/usr/bin/env python3
"""Game-level facts the per-round table does not carry: winner, win condition,
round count, and a MAP IDENTITY.

Map identity matters for the second question (is CAD's opening map-independent?).
Third-party CAD games have no map NAME anywhere on disk -- `join.tsv` only names
maps for our own ladder games -- so identity here is (width, height, md5 of the
terrain rows).  Games sharing that key are the same map; `analyse.py` back-fills
human names from `join.tsv` where our games pin them.

Emits: file, winner, wincond, rounds, mw, mh, mapkey
"""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, WIRE_LEN, WIRE_VARINT, packed_varints  # noqa: E402


def one(path: Path):
    data = path.read_bytes()
    map_buf, winner, wincond, nturns = None, None, "", 0
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            nturns += 1
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    w = h = 0
    rows = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            rows.append(row)
    dig = hashlib.md5(repr(rows).encode()).hexdigest()[:8]
    return winner, wincond, nturns, w, h, f"{w}x{h}:{dig}"


def main(pop_path, replay_dir, out_path):
    out = open(out_path, "w")
    out.write("file\twinner\twincond\trounds\tmw\tmh\tmapkey\n")
    for r in csv.DictReader(open(pop_path), delimiter="\t"):
        p = Path(replay_dir) / r["file"]
        if not p.exists():
            continue
        wn, wc, nt, w, h, key = one(p)
        out.write(f"{r['file']}\t{wn}\t{wc}\t{nt}\t{w}\t{h}\t{key}\n")
    out.close()


if __name__ == "__main__":
    main(*sys.argv[1:])
