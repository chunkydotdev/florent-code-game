#!/usr/bin/env python3
"""Encode maps/*.map26 into the bot's MAP_CODES packing — with the control
that makes the output trustworthy.

WHY THIS EXISTS (2026-08-13, s36). The organisers rotated to a 15-map pool and
NONE of the 10 new maps has a MAP_CODES/EXTRA_MAP_CODES entry, so
`known_map_for` returns None on all of them and every pathing/ore surface
degrades: measured 98.7-99.1% builder move-reversal livelock on midgard and 9
builder actions in 1,000 rounds (osc agent + osc_measure.py, this session).
The weekly-rotation entries in the table say "encoded from maps/*.map26 ...
round-trip verified" but THAT ENCODER WAS NEVER COMMITTED. This is it, rebuilt.

THE PACKING (from eco.py known_map_for, the decoder this must match):
  cell 0=empty 1=wall 2=ore, row-major; chars pack THREE cells base-3
  little-endian (val%3 first): val = c0 + 3*c1 + 9*c2, char=MAP_ALPHABET[val].
  Key = (w, h, ax, ay, bx, by) with (ax,ay) team-A core NW corner.

⛔ THE POSITIVE CONTROL (--selftest): encoding an OLD-pool map that already has
a hand-verified MAP_CODES entry (fjordgate 10x10, antler 14x18, drumlin,
nordkap, archipelago) must reproduce the existing string BYTE-FOR-BYTE. That
validates the env-int mapping, the packing order, the row order and the key in
one shot. A selftest that only round-trips its own output would validate
nothing but itself.

Usage:
  .venv/bin/python tools/map_encode.py --selftest
  .venv/bin/python tools/map_encode.py maps/midgard.map26 [...]  -> entries
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, packed_varints, WIRE_LEN  # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
MAP_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"


def parse_map26(path: Path):
    """-> (w, h, tiles[y][x] ints, [(team, x, y), ...])"""
    data = path.read_bytes()
    w = h = 0
    rows, cores = [], []
    for num, wire, value in fields(data):
        if num == 1 and wire != WIRE_LEN:
            w = value
        elif num == 2 and wire != WIRE_LEN:
            h = value
        elif num == 3 and wire == WIRE_LEN:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            rows.append(row)
        elif num == 4 and wire == WIRE_LEN:
            team, x, y = 0, 0, 0
            for cn, cw, cv in fields(value):
                if cn == 2:
                    team = cv
                elif cn == 3 and cw == WIRE_LEN:
                    d = {n: v for n, _w2, v in fields(cv)}
                    x, y = d.get(1, 0), d.get(2, 0)
            cores.append((team, x, y))
    if not (w and h and len(rows) == h and len(cores) == 2):
        raise SystemExit(f"{path}: malformed map (w={w} h={h} rows={len(rows)} cores={len(cores)})")
    return w, h, rows, cores


def encode(w, h, rows):
    cells = [rows[y][x] for y in range(h) for x in range(w)]
    if any(c not in (0, 1, 2) for c in cells):
        bad = sorted({c for c in cells if c not in (0, 1, 2)})
        raise SystemExit(f"unexpected env values {bad} — the 0/1/2 mapping assumption is WRONG, stop")
    out = []
    for i in range(0, len(cells), 3):
        tri = cells[i:i + 3] + [0] * (3 - len(cells[i:i + 3]))
        out.append(MAP_ALPHABET[tri[0] + 3 * tri[1] + 9 * tri[2]])
    return "".join(out)


def entry_for(path: Path):
    w, h, rows, cores = parse_map26(path)
    a = next((c for c in cores if c[0] == 0), cores[0])
    b = next((c for c in cores if c[0] == 1), cores[-1])
    return (w, h, a[1], a[2], b[1], b[2]), encode(w, h, rows)


def _load_table():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "d_", ROOT / "bots/_v187saltidle_f/doctrine.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.MAP_CODES), list(mod.EXTRA_MAP_CODES)


def selftest() -> int:
    codes, extra = _load_table()
    controls = ["fjordgate", "antler", "drumlin", "nordkap", "archipelago"]
    ok = True
    for name in controls:
        key, code = entry_for(ROOT / f"maps/{name}.map26")
        # EXTRA_MAP_CODES is a LIST because two 26x26 layouts share a key;
        # a control matches if it reproduces ANY entry under its key.
        pool = ([codes[key]] if key in codes else []) + \
               [c for k, c in extra if k == key]
        if not pool:
            print(f"  [FAIL] {name}: key {key} in NEITHER table — key format wrong")
            ok = False
        elif code in pool:
            print(f"  [ok] {name}: key {key}, code REPRODUCED byte-for-byte "
                  f"({len(pool)} candidate(s) under key)")
        else:
            print(f"  [FAIL] {name}: key {key} found, code MISMATCH "
                  f"(len {len(code)} vs {[len(c) for c in pool]})")
            ok = False
    # the negative: corrupting one cell must break the reproduction
    w, h, rows, cores = parse_map26(ROOT / "maps/fjordgate.map26")
    rows[0][0] = (rows[0][0] + 1) % 3
    key = (w, h, cores[0][1], cores[0][2], cores[1][1], cores[1][2])
    pool = ([codes[key]] if key in codes else []) + [c for k, c in extra if k == key]
    if encode(w, h, rows) in pool:
        print("  [FAIL] corrupted fjordgate STILL matches — the check cannot fail")
        ok = False
    else:
        print("  [ok] corrupted fjordgate does NOT match (the control can fail)")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for p in sys.argv[1:]:
        key, code = entry_for(Path(p))
        print(f'    ({", ".join(map(str, key))}): "{code}",  # {Path(p).stem}')
