#!/usr/bin/env python3
"""CHOKE CENSUS — does the map pool ADMIT a blockade at all?

    .venv/bin/python tools/choke_census.py            # every map in maps/
    .venv/bin/python tools/choke_census.py --selftest # drives BOTH verdicts
    .venv/bin/python tools/choke_census.py --maps antler atoll

WHY THIS EXISTS (s44, 2026-08-15). Magnus put the session on launchers and asked
first whether they can be "positioned at a critical point and block passage,
thereby strangling any offense". **That is a question about TERRAIN before it is
a question about code.** A blockade plank on a map with no chokepoint is
`map_admits.py`'s dead denominator all over again — a cell that cannot express
the mechanism averages your effect toward zero and tells you nothing.

WHAT IT MEASURES. The MINIMUM VERTEX CUT between the two cores: the smallest
number of TILES you would have to occupy with buildings to make the enemy core
unreachable from ours. That number IS the price of a blockade, in buildings.

FOUR THINGS IT GETS RIGHT ON PURPOSE, each of which would otherwise flatter:

1. ⛔ 4-CONNECTED, NOT 8. Builder bots may only MOVE in the four cardinal
   directions (`move(<diagonal>)` raises; `can_move(<diagonal>)` is False). A
   diagonal-connected graph would report cuts that do not block anything,
   because a builder cannot use a diagonal step to escape one. This is the
   single assumption most likely to be got wrong, so it is stated here.

2. ⛔ VERTEX CUT, NOT EDGE CUT. We block by OCCUPYING TILES (a building sits on
   a tile). An edge cut answers a question nobody asked and is always <= the
   vertex cut, i.e. it flatters.

3. ⛔ THE CORES THEMSELVES ARE UNCUTTABLE (capacity infinity). Otherwise the
   trivial "cut" is to wall the core's own footprint, which we cannot build on.
   Core footprint is 2x2 and every tile of it is protected.

4. ⛔ ORE IS PASSABLE. `Environment.ORE_TITANIUM` is walkable terrain; only WALL
   blocks. Treating ore as blocked would invent chokepoints that do not exist.

WHAT IT DOES **NOT** SAY. It does not say a blockade is GOOD. A cut of k tiles
costs k buildings, each of which the enemy can attack (a builder does 2 dmg for
2 Ti; a launcher has 30 HP, a barrier 30, a conveyor 20), and every build raises
our own global cost scale. It also says nothing about whether we can REACH the
cut tiles in time to build them -- building requires an orthogonally adjacent
builder bot, so an unreachable cut is a fiction. Those are separate questions and
this tool deliberately refuses to answer them; it prices the GEOMETRY only.
"""
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, WIRE_LEN, WIRE_VARINT  # noqa: E402

WALL = 1
INF = 10**9


# ---------------------------------------------------------------- map loading
def parse_map(buf: bytes):
    """(w, h, rows, cores) from a .map26 buffer. cores = {team: (x, y)}.

    Core entries are {team (1), pos (3)} and PROTO3 OMITS ZEROS, so team A's
    core carries no team field at all. Defaulting to 0 rather than requiring
    presence -- map_admits.py records that requiring it silently drops exactly
    half the cores and then looks like missing DATA rather than a broken PARSE.
    """
    w = h = 0
    rows: list[list[int]] = []
    cores: dict[int, tuple[int, int]] = {}
    for num, wire, value in fields(buf):
        if num == 1 and wire == WIRE_VARINT:
            w = value
        elif num == 2 and wire == WIRE_VARINT:
            h = value
        elif num == 3 and wire == WIRE_LEN:
            for rn, _rw, rv in fields(value):
                # ⛔ THE WIRE-TYPE GUARD IS LOAD-BEARING, not defensive noise: a
                # row whose tiles are all zero encodes as a VARINT here, and
                # list()-ing an int raises. Without this the whole pool is
                # unparseable on the first all-EMPTY row.
                if rn == 1 and _rw == WIRE_LEN:
                    rows.append(list(rv))
        elif num == 4 and wire == WIRE_LEN:
            c_team, c_pos = 0, None
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c_team = cv
                elif cn == 3:
                    c_pos = read_pos(cv)
            if c_pos is not None:
                cores[c_team] = c_pos
    return w, h, rows, cores


# ------------------------------------------------------------------ max flow
def min_vertex_cut(w, h, rows, src_tiles, dst_tiles, protected):
    """Min number of tiles to remove to disconnect src from dst (4-connected).

    Node-splitting: every passable tile becomes in->out with capacity 1 (or INF
    if protected). Adjacency edges are INF. Max-flow value == min vertex cut.
    Returns (cut_size, cut_tiles).
    """
    def nid(x, y, side):
        return (y * w + x) * 2 + side          # side 0 = in, 1 = out

    n = w * h * 2 + 2
    S, T = n - 2, n - 1
    graph: list[dict[int, int]] = [dict() for _ in range(n)]

    def add(u, v, c):
        graph[u][v] = graph[u].get(v, 0) + c
        graph[v].setdefault(u, 0)

    for y in range(h):
        for x in range(w):
            if rows[y][x] == WALL:
                continue
            cap = INF if (x, y) in protected else 1
            add(nid(x, y, 0), nid(x, y, 1), cap)
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):   # CARDINAL ONLY
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and rows[ny][nx] != WALL:
                    add(nid(x, y, 1), nid(nx, ny, 0), INF)

    for (x, y) in src_tiles:
        add(S, nid(x, y, 0), INF)
    for (x, y) in dst_tiles:
        add(nid(x, y, 1), T, INF)

    flow = 0
    while True:                                     # Edmonds-Karp
        parent = {S: None}
        q = deque([S])
        while q and T not in parent:
            u = q.popleft()
            for v, c in graph[u].items():
                if c > 0 and v not in parent:
                    parent[v] = u
                    q.append(v)
        if T not in parent:
            break
        push, v = INF, T
        while parent[v] is not None:
            push = min(push, graph[parent[v]][v]); v = parent[v]
        v = T
        while parent[v] is not None:
            u = parent[v]
            graph[u][v] -= push
            graph[v][u] += push
            v = u
        flow += push
        if flow >= INF:
            return INF, []                          # cores adjacent/unseparable

    reach = set()                                   # residual reachability -> the cut
    q = deque([S]); reach.add(S)
    while q:
        u = q.popleft()
        for v, c in graph[u].items():
            if c > 0 and v not in reach:
                reach.add(v); q.append(v)
    cut = [(x, y) for y in range(h) for x in range(w)
           if rows[y][x] != WALL
           and nid(x, y, 0) in reach and nid(x, y, 1) not in reach]
    return flow, cut


# ------------------------------------------------------------------ analysis
def core_tiles(pos):
    """The core is a 2x2 footprint anchored at pos."""
    x, y = pos
    return [(x + dx, y + dy) for dx in (0, 1) for dy in (0, 1)]


def ring_of(tiles, w, h, rows):
    """The tiles orthogonally adjacent to a footprint -- a core's spawn ring."""
    ring = set()
    for (x, y) in tiles:
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and rows[ny][nx] != WALL \
               and (nx, ny) not in tiles:
                ring.add((nx, ny))
    return ring


def analyse(name, w, h, rows, cores, field_only=False):
    """field_only=True protects BOTH cores' spawn rings, so the reported cut is
    a chokepoint IN THE FIELD.

    ⛔ WHY THIS MODE EXISTS, and it is a correction to this tool's first output:
    the unconstrained min cut is almost always the 8 tiles around OUR OWN core,
    because a 2x2 footprint has exactly 8 orthogonal neighbours. That "cut" does
    disconnect the cores -- by SEALING US IN. It is self-imprisonment wearing a
    blockade's number, and it read `CUT 8, d(us) 1` on 12 of 23 maps before this
    mode existed. Sealing a spawn ring is a real and DIFFERENT mechanism (it is
    what spawn denial costs, against THEIR core); it is not passage blocking.
    """
    if len(cores) != 2:
        return None
    a, b = sorted(cores)
    at = [t for t in core_tiles(cores[a]) if 0 <= t[0] < w and 0 <= t[1] < h]
    bt = [t for t in core_tiles(cores[b]) if 0 <= t[0] < w and 0 <= t[1] < h]
    protected = set(at) | set(bt)
    rings = (ring_of(set(at), w, h, rows), ring_of(set(bt), w, h, rows))
    if field_only:
        protected |= rings[0] | rings[1]
    cut, tiles = min_vertex_cut(w, h, rows, at, bt, protected)
    passable = sum(1 for y in range(h) for x in range(w) if rows[y][x] != WALL)
    wallfrac = 1 - passable / (w * h)

    def mind(tile_set, pt):
        return min(abs(pt[0] - q[0]) + abs(pt[1] - q[1]) for q in tile_set)

    d_us = min((mind(at, t) for t in tiles), default=None)
    d_them = min((mind(bt, t) for t in tiles), default=None)

    # ⭐ THE LAUNCHER QUESTION, and it is the reason this tool exists rather than
    # a barrier-cost question: a launcher does NOT have to STAND on the cut. It
    # picks up any builder at d^2 <= 2 -- the 8 surrounding tiles -- and throws
    # it away. So a launcher BESIDE a chokepoint COVERS it: enemies that step in
    # are ejected, and our own builders walk through unimpeded, which a wall
    # cannot do. Count the passable tiles from which ONE launcher covers EVERY
    # cut tile. A single such tile turns a k-building wall into a 1-building
    # turnstile.
    cover = []
    if tiles:
        for y in range(h):
            for x in range(w):
                if rows[y][x] == WALL or (x, y) in protected:
                    continue
                if all(max(abs(x - tx), abs(y - ty)) <= 1 for (tx, ty) in tiles):
                    cover.append((x, y))
    return dict(name=name, w=w, h=h, cut=cut, tiles=tiles, wallfrac=wallfrac,
                d_us=d_us, d_them=d_them, area=w * h,
                ring_us=len(rings[0]), ring_them=len(rings[1]), cover=cover)


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    """BOTH VERDICTS. An open field must NOT report a cheap cut; a map with a
    deliberate 1-tile corridor MUST report exactly 1. A tool that has only ever
    said 'narrow' has not been seen to check."""
    fail = 0

    def grid(spec):
        return [[WALL if c == '#' else 0 for c in line] for line in spec]

    # (a) OPEN FIELD 9x9, cores at opposite corners -> cut must be well above 1
    open_rows = grid(["." * 9 for _ in range(9)])
    cut, _ = min_vertex_cut(9, 9, open_rows, core_tiles((0, 0)), core_tiles((7, 7)),
                            set(core_tiles((0, 0))) | set(core_tiles((7, 7))))
    print(f"  open field 9x9        cut={cut:<3} want>=4")
    if cut < 4:
        print("  FAIL: an open field reported a cheap cut"); fail = 1

    # (b) ONE-TILE CORRIDOR -> cut must be exactly 1
    corr = grid([
        ".........",
        ".........",
        "####.####",
        "#########".replace("#########", "####.####"),
        ".........",
        ".........",
        ".........",
        ".........",
        ".........",
    ])
    corr[2] = [WALL] * 9; corr[2][4] = 0          # a single gap in a full wall
    cut2, tiles2 = min_vertex_cut(9, 9, corr, core_tiles((0, 0)), core_tiles((3, 6)),
                                  set(core_tiles((0, 0))) | set(core_tiles((3, 6))))
    print(f"  1-tile corridor       cut={cut2:<3} want=1   at {tiles2}")
    if cut2 != 1:
        print("  FAIL: the corridor gap was not priced at 1"); fail = 1

    # (c) SEALED map -> already disconnected, cut must be 0
    sealed = grid(["........." for _ in range(9)])
    sealed[4] = [WALL] * 9
    cut3, _ = min_vertex_cut(9, 9, sealed, core_tiles((0, 0)), core_tiles((3, 6)),
                             set(core_tiles((0, 0))) | set(core_tiles((3, 6))))
    print(f"  sealed by a full wall cut={cut3:<3} want=0")
    if cut3 != 0:
        print("  FAIL: a sealed map did not read 0"); fail = 1

    print("SELFTEST PASS (open / narrow / sealed all discriminated)" if not fail
          else "SELFTEST FAIL")
    return fail


# ---------------------------------------------------------------------- main
def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--maps", nargs="*")
    ap.add_argument("--field", action="store_true",
                    help="protect both spawn rings: price a chokepoint IN THE "
                         "FIELD rather than the trivial self-seal")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    paths = sorted((ROOT / "maps").glob("*.map26"))
    if a.maps:
        want = set(a.maps)
        paths = [p for p in paths if p.stem in want]

    out = []
    for p in paths:
        w, h, rows, cores = parse_map(p.read_bytes())
        if not rows or len(cores) != 2:
            print(f"  {p.stem:<16} UNPARSEABLE (rows={len(rows)} cores={len(cores)})")
            continue
        r = analyse(p.stem, w, h, rows, cores, field_only=a.field)
        if r:
            out.append(r)

    out.sort(key=lambda r: (r["cut"], r["area"]))
    print(("FIELD CHOKEPOINTS (both spawn rings protected)" if a.field
           else "RAW MIN CUT (spawn rings cuttable -- the cheapest cut is usually "
                "SEALING OUR OWN CORE)") + "\n")
    print(f"{'map':<16}{'dims':>8}{'area':>7}{'wall%':>7}{'CUT':>6}"
          f"{'d(us)':>7}{'d(them)':>8}{'1-lnchr':>9}   verdict")
    for r in out:
        v = ("NO BLOCKADE (already split)" if r["cut"] == 0 else
             "⭐ CHOKEPOINT — blockable" if r["cut"] <= 3 else
             "narrow-ish" if r["cut"] <= 6 else
             "OPEN — blockade not admitted")
        cov = f"YES({len(r['cover'])})" if r['cover'] else "-"
        print(f"{r['name']:<16}{r['w']}x{r['h']:>5}{r['area']:>7}"
              f"{r['wallfrac']*100:>6.1f}%{r['cut']:>6}"
              f"{str(r['d_us']):>7}{str(r['d_them']):>8}{cov:>9}   {v}")

    if out:
        n = len(out)
        block = [r for r in out if 1 <= r["cut"] <= 3]
        mid = [r for r in out if 4 <= r["cut"] <= 6]
        print(f"\n  {len(block)}/{n} maps blockable at <=3 tiles; "
              f"{len(mid)}/{n} at 4-6; "
              f"{n - len(block) - len(mid)}/{n} open (>6).")
        print("  ⚠ GEOMETRY ONLY. This prices the cut in BUILDINGS; it does not "
              "say we can reach\n    those tiles in time, hold them, or that "
              "holding them is worth the scale inflation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
