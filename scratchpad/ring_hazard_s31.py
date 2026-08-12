#!/usr/bin/env python3
"""RE-DERIVATION of the inherited claim in CLAUDE.md:

    "one hostile body on the ring DOUBLES the 25-round core-death hazard,
     2.24% -> 4.77%, CIs disjoint"

READ-ONLY. Consumes replay_archive/*.replay26 + corpus/meta_join.tsv only.
Downloads nothing, runs no fcode, writes nothing outside scratchpad/.

WHAT IT MEASURES
----------------
For EVERY core in a replay (both teams, ours and third parties'), for every
round r at which that core is still alive:

  hostile(r)  = # of ENEMY builder bots standing on that core's 12-tile ring at
                the END of round r  (end-of-round snapshot, "standing", not
                "placed then lost" -- same convention as tools/ring_read.py)
  friendly(r) = same for the core's OWN builder bots  (polarity control)
  hp(r)       = the core's HP after all updateHp deltas in rounds <= r
  eb(r)/ob(r) = enemy / own builder bots within d^2 <= 36 of the core anchor
  et(r)/ot(r) = enemy / own turrets  (gunner|sentinel|launcher) within d^2 <= 36
  outcome     = 1 if the core is removed at some round D with r < D <= r+25

RING = the 8 orthogonal neighbours of the 2x2 footprint + the 4 diagonal
corners, clipped to map bounds, WALL tiles NOT dropped.  Byte-identical rule to
tools/ring_read.py:ring_tiles() -- imported from there, not re-implemented, so
this file inherits that decoder's 9-cell forced-answer selftest.

CENSORING.  A round r is in the risk set only if the outcome is OBSERVABLE:
either the core dies at some D in (r, r+25], or the replay runs at least to
round r+25.  Rounds whose window runs off the end of a replay in which the core
survived are DROPPED and counted (reported as the censored fraction).

CLUSTERING.  Core-rounds inside one game are massively correlated (one death
contributes up to 25 to the numerator).  Headline tables carry a game-clustered
bootstrap CI as well as the naive Wilson CI, and a per-round hazard (P(die at
exactly r+1 | alive at r)) alongside the 25-round window rate, because the
window rate's numerator is inflated by construction.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos, WIRE_LEN  # noqa: E402
from ring_read import ring_tiles                                     # noqa: E402

ARCHIVE = ROOT / "replay_archive"
OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"   # OpenSverige
W = 25                       # the claim's window
NEAR_D2 = 36                 # core vision radius^2, used for "local force"
TURRETS = ("gunner", "sentinel", "launcher")


# ---------------------------------------------------------------- decode ----

def _signed(v: int) -> int:
    """updateHp.delta is a 64-bit two's-complement varint (corpus-howto TRAP 2)."""
    return v - (1 << 64) if v >= (1 << 63) else v


def decode(path: Path):
    """-> (rounds, [percore, percore], parse_note) or None."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    map_buf, turn_bufs = None, []
    try:
        for num, wire, value in fields(data):
            if num == 1 and wire == WIRE_LEN and map_buf is None:
                map_buf = value
            elif num == 3 and wire == WIRE_LEN:
                turn_bufs.append(value)
    except Exception:
        return None
    if map_buf is None or not turn_bufs:
        return None
    w = h = 0
    cores = []
    try:
        for num, wire, value in fields(map_buf):
            if num == 1:
                w = value
            elif num == 2:
                h = value
            elif num == 4 and wire == WIRE_LEN:
                d = {n: v for n, _, v in fields(value)}
                cores.append({"id": d.get(1, 0), "team": d.get(2, 0),
                              "pos": read_pos(d[3])})
    except Exception:
        return None
    if len(cores) != 2 or {c["team"] for c in cores} != {0, 1}:
        return None
    cores.sort(key=lambda c: c["team"])
    ring = [ring_tiles(cores[t]["pos"], w, h) for t in (0, 1)]
    anchor = [cores[t]["pos"] for t in (0, 1)]
    cid = [cores[t]["id"] for t in (0, 1)]

    pos_of, team_of, kind_of = {}, {}, {}
    hp = [500, 500]
    death = [None, None]
    R = len(turn_bufs)
    # per-round series, per core team
    ser = [{k: [] for k in ("host", "frnd", "hp", "eb", "ob", "et", "ot")}
           for _ in (0, 1)]
    alive_to = [R, R]        # last round index at which the core is still alive

    for rnd, turn_buf in enumerate(turn_bufs):
        try:
            for _n, _w, ub in fields(turn_buf):
                for unum, _uw, ubuf in fields(ub):
                    if unum == 1:                      # placeEntity
                        for en, _ew, ebuf in fields(ubuf):
                            if en != 1:
                                continue
                            e = parse_entity(ebuf, rnd)
                            if e is None:
                                continue
                            pos_of[e.id] = e.pos
                            team_of[e.id] = e.team
                            kind_of[e.id] = e.kind
                    elif unum == 2:                    # moveBuilderBot
                        bid = to = None
                        for mn, _mw, mv in fields(ubuf):
                            if mn == 1:
                                bid = mv
                            elif mn == 2:
                                to = read_pos(mv)
                        if bid is not None and to is not None:
                            pos_of[bid] = to
                    elif unum == 3:                    # removeEntity
                        for rn, _rw, rv in fields(ubuf):
                            if rn != 1:
                                continue
                            pos_of.pop(rv, None)
                            team_of.pop(rv, None)
                            kind_of.pop(rv, None)
                            for t in (0, 1):
                                if rv == cid[t] and death[t] is None:
                                    death[t] = rnd
                    elif unum == 5:                    # updateHp {id=1, delta=2}
                        eid = dl = None
                        for hn, _hw, hv in fields(ubuf):
                            if hn == 1:
                                eid = hv
                            elif hn == 2:
                                dl = _signed(hv)
                        if eid is not None and dl is not None:
                            for t in (0, 1):
                                if eid == cid[t]:
                                    hp[t] += dl
        except Exception:
            return None

        # ---- end-of-round snapshot ----
        c_host = [0, 0]
        c_frnd = [0, 0]
        c_eb = [0, 0]
        c_ob = [0, 0]
        c_et = [0, 0]
        c_ot = [0, 0]
        for eid, p in pos_of.items():
            k = kind_of.get(eid)
            if k == "core" or k is None:
                continue
            tm = team_of.get(eid)
            if tm is None:
                continue
            bot = (k == "builder_bot")
            tur = (k in TURRETS)
            if not (bot or tur):
                continue
            for t in (0, 1):
                ax, ay = anchor[t]
                # d^2 measured from the NW footprint tile, cheap and consistent
                dd = (p[0] - ax) ** 2 + (p[1] - ay) ** 2
                near = dd <= NEAR_D2
                if bot and p in ring[t]:
                    if tm == t:
                        c_frnd[t] += 1
                    else:
                        c_host[t] += 1
                if near:
                    if bot:
                        (c_ob if tm == t else c_eb)[t] += 1
                    elif tur:
                        (c_ot if tm == t else c_et)[t] += 1
        for t in (0, 1):
            if death[t] is not None and rnd >= death[t]:
                if alive_to[t] == R:
                    alive_to[t] = death[t]      # first dead round
                continue
            s = ser[t]
            s["host"].append(c_host[t])
            s["frnd"].append(c_frnd[t])
            s["hp"].append(hp[t])
            s["eb"].append(c_eb[t])
            s["ob"].append(c_ob[t])
            s["et"].append(c_et[t])
            s["ot"].append(c_ot[t])

    return R, ser, death, [len(ser[t]["host"]) for t in (0, 1)], (w, h)


# ---------------------------------------------------------------- reduce ----

def hb(n):
    """hostile-body bucket label"""
    return str(n) if n <= 3 else "4+"


def durb(k):
    if k == 0:
        return "0"
    if k <= 5:
        return "1-5"
    if k <= 15:
        return "6-15"
    return "16-25"


def hpb(v):
    if v >= 500:
        return "500 (full)"
    if v >= 400:
        return "400-499"
    if v >= 250:
        return "250-399"
    if v >= 100:
        return "100-249"
    return "<100"


def fb(n):
    return str(n) if n <= 2 else "3+"


def reduce_game(fname, dec, pop_of_core):
    """-> dict of table-name -> {cell: [n, deaths]}, plus per-game T1/T2 rows."""
    R, ser, death, nlive, dims = dec
    out = Counter()                     # (table, cell, 'n'|'d') -> count
    pergame = Counter()                 # (table, cell, 'n'|'d') -> count, this game
    censored = 0
    for t in (0, 1):
        pop = pop_of_core[t]
        if pop is None:
            continue
        host = ser[t]["host"]
        frnd = ser[t]["frnd"]
        hpv = ser[t]["hp"]
        eb, ob, et, ot = ser[t]["eb"], ser[t]["ob"], ser[t]["et"], ser[t]["ot"]
        n_alive = len(host)             # rounds 0..n_alive-1 the core is alive
        D = death[t]                    # round index of removal, or None

        for r in range(n_alive):
            # --- outcome & censoring -----------------------------------
            if D is not None:
                dies = (r < D <= r + W)
                observable = True       # death inside or after window: known
                if not dies and D > r + W:
                    dies = False
                nxt = (D == r + 1)
            else:
                # core survives to the end of the replay at round R-1
                if r + W > R - 1:
                    censored += 1
                    continue
                dies = False
                nxt = False
                observable = True
            if not observable:
                continue
            hcell = hb(host[r])
            d = 1 if dies else 0

            def add(tab, cell):
                out[(tab, cell, "n")] += 1
                out[(tab, cell, "d")] += d
                if tab in ("T1", "T2"):
                    pergame[(tab, cell, "n")] += 1
                    pergame[(tab, cell, "d")] += d

            # T1: dose-response, by population
            add("T1", (pop, hcell))
            # per-round hazard (numerator = death at exactly r+1)
            out[("T1r", (pop, hcell), "n")] += 1
            out[("T1r", (pop, hcell), "d")] += 1 if nxt else 0
            # T2: duration -- how many of the LAST 25 rounds were occupied
            lo = max(0, r - W + 1)
            occ25 = sum(1 for j in range(lo, r + 1) if host[j] > 0)
            add("T2", (pop, durb(occ25)))
            if host[r] > 0:                      # duration GIVEN occupied now
                add("T2b", (pop, durb(occ25)))
            # T5: friendly-body polarity control
            add("T5", (pop, fb(frnd[r])))
            # T3: HP stratification
            add("T3", (pop, hpb(hpv[r]), hcell))
            # T4: local-force stratification
            add("T4", (pop, f"eb{min(eb[r],3)}", f"et{min(et[r],2)}",
                       f"ob{min(ob[r],3)}", hcell))
            # T8: round band
            add("T8", (pop, f"r{(r//200)*200}-{(r//200)*200+199}", hcell))
            # T10/T11/T12 -- THE MATCHED CONTRAST.  `eb` counts every enemy
            # builder within d^2<=36 of the core INCLUDING the ones on the ring,
            # so holding eb fixed and varying the ring count compares the SAME
            # AMOUNT OF ENEMY FORCE in different PLACES.  That is exactly the
            # manipulation the plank proposes ("do not walk the body off the
            # corner"), so it is the contrast the plank has to survive.
            occ01 = "on-ring" if host[r] else "near-only"
            ebk = f"eb{min(eb[r],4)}"
            etk = f"et{min(et[r],2)}"
            if eb[r] > 0:
                out[("T11", (pop, ebk, occ01), "n")] += 1
                out[("T11", (pop, ebk, occ01), "d")] += d
                out[("T10", (pop, hpb(hpv[r]), ebk, etk, occ01), "n")] += 1
                out[("T10", (pop, hpb(hpv[r]), ebk, etk, occ01), "d")] += d
                if host[r]:
                    out[("T12", (pop, hpb(hpv[r]), ebk, durb(occ25)), "n")] += 1
                    out[("T12", (pop, hpb(hpv[r]), ebk, durb(occ25)), "d")] += d
            # T6: NULL outcome -- death in (r+200, r+225]
            if D is not None:
                nulld = 1 if (r + 200 < D <= r + 225) else 0
                ok = True
            else:
                ok = (r + 225 <= R - 1)
                nulld = 0
            if ok:
                out[("T6", (pop, hcell), "n")] += 1
                out[("T6", (pop, hcell), "d")] += nulld
            # T7: LAG test -- predictor at r-k against the SAME outcome window
            if r >= 100:
                for k in (0, 10, 25, 50, 100):
                    out[("T7", (pop, k, hb(host[r - k])), "n")] += 1
                    out[("T7", (pop, k, hb(host[r - k])), "d")] += d
                # discordant pairs: now vs 50 ago
                now, ago = host[r] > 0, host[r - 50] > 0
                lbl = ("now&ago" if now and ago else
                       "now_only" if now else
                       "ago_only" if ago else "neither")
                out[("T7d", (pop, lbl), "n")] += 1
                out[("T7d", (pop, lbl), "d")] += d
        # T9: time-to-death profile (occupancy as a function of D - r)
        if D is not None:
            for r in range(n_alive):
                ttd = D - r
                if ttd <= 0:
                    continue
                band = ("1-25" if ttd <= 25 else "26-50" if ttd <= 50 else
                        "51-100" if ttd <= 100 else "101-200" if ttd <= 200
                        else "201+")
                out[("T9", (pop, "DIES", band), "n")] += 1
                out[("T9", (pop, "DIES", band), "d")] += 1 if host[r] > 0 else 0
        else:
            for r in range(n_alive):
                out[("T9", (pop, "SURVIVES", "all"), "n")] += 1
                out[("T9", (pop, "SURVIVES", "all"), "d")] += 1 if host[r] > 0 else 0
    return out, pergame, censored


# ------------------------------------------------------------------ meta ----

def load_meta():
    """file -> (our_seat|None).  Seat from teamAId/teamBId, NEVER us_side (TRAP 7)."""
    m = {}
    p = ROOT / "corpus" / "meta_join.tsv"
    with p.open() as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        ia, ib, ifile = hdr.index("teamAId"), hdr.index("teamBId"), hdr.index("file")
        for line in fh:
            c = line.rstrip("\n").split("\t")
            if len(c) <= max(ia, ib, ifile):
                continue
            if c[ia] == OUR_TEAM_ID:
                m[c[ifile]] = 0
            elif c[ib] == OUR_TEAM_ID:
                m[c[ifile]] = 1
            else:
                m[c[ifile]] = None          # third party
    return m


# ------------------------------------------------------------------ stats ---

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - hw), min(1.0, c + hw)


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{p:7.3%} [{lo:6.3%},{hi:6.3%}]  n={n:>9,} d={k:>8,}"


# ------------------------------------------------------------------- main ---

def work(args):
    fname, seat = args
    dec = decode(ARCHIVE / fname)
    if dec is None:
        return fname, None, None, 0
    # population of each core:
    #   seat is None  -> both cores are FIELD (third-party game)
    #   seat == s     -> core s is OUR core (we defend), core 1-s is THEIR core
    #                    (we are the aggressor on its ring)
    if seat is None:
        pop = ["FIELD", "FIELD"]
    else:
        pop = [None, None]
        pop[seat] = "US_DEFEND"
        pop[1 - seat] = "US_ATTACK"
    red, pergame, cens = reduce_game(fname, dec, pop)
    return fname, red, pergame, cens


def main(argv):
    limit = None
    seed = 11
    workers = os.cpu_count() or 4
    for a in argv:
        if a.startswith("--limit="):
            limit = int(a.split("=")[1])
        elif a.startswith("--seed="):
            seed = int(a.split("=")[1])
        elif a.startswith("--workers="):
            workers = int(a.split("=")[1])
    if "--geometry" in argv:
        return geometry_control()
    if "--validate" in argv:
        return validate(limit or 400, seed)

    meta = load_meta()
    files = sorted(p.name for p in ARCHIVE.glob("*.replay26"))
    print(f"archive: {len(files):,} .replay26 files; "
          f"{sum(1 for f in files if f in meta):,} have meta_join rows", flush=True)
    tasks = [(f, meta.get(f, "MISSING")) for f in files]
    # files with no meta row: population unknown -> excluded, but counted
    nometa = sum(1 for _f, s in tasks if s == "MISSING")
    tasks = [(f, s) for f, s in tasks if s != "MISSING"]
    if limit:
        random.Random(seed).shuffle(tasks)
        tasks = tasks[:limit]
    print(f"  {nometa:,} files have no meta_join row -> EXCLUDED (population unknown)")
    print(f"  decoding {len(tasks):,} files on {workers} workers ...", flush=True)

    TOT = Counter()
    GAMES = []                     # per-game T1/T2 counters, for cluster bootstrap
    nfail = ndone = 0
    censored = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for fname, red, pergame, cens in ex.map(work, tasks, chunksize=16):
            if red is None:
                nfail += 1
                continue
            ndone += 1
            censored += cens
            TOT.update(red)
            GAMES.append(pergame)
            if ndone % 2000 == 0:
                print(f"    ... {ndone:,} decoded", file=sys.stderr, flush=True)
    print(f"\nPARSE: {ndone:,} decoded, {nfail:,} FAILED "
          f"({nfail/max(1,ndone+nfail):.2%} of attempted)")
    tot_rounds = sum(v for (tab, _c, kk), v in TOT.items() if tab == "T1" and kk == "n")
    print(f"CENSORED core-rounds dropped (window runs off end of replay, core "
          f"alive): {censored:,}  = {censored/max(1,censored+tot_rounds):.2%} of "
          f"candidate core-rounds")
    report(TOT, GAMES)
    return 0


def cells(TOT, tab):
    """Cell table for `tab`, PLUS an 'ALL' population pooling the three."""
    out = defaultdict(lambda: [0, 0])
    for (t, cell, kk), v in TOT.items():
        if t != tab:
            continue
        out[cell][0 if kk == "n" else 1] += v
        if isinstance(cell, tuple) and cell and cell[0] in POPS3:
            out[("ALL",) + cell[1:]][0 if kk == "n" else 1] += v
    return out


POPS3 = ("FIELD", "US_ATTACK", "US_DEFEND")


def boot_ci(GAMES, tab, cell, B=400, seed=7):
    """Game-clustered bootstrap CI for the rate in one cell."""
    rows = [(g[(tab, cell, "n")], g[(tab, cell, "d")]) for g in GAMES]
    rows = [r for r in rows if r[0]]
    if not rows:
        return None          # e.g. the pooled 'ALL' row: per-game counters are
                             # keyed on the three real populations, so there is
                             # nothing to resample. Printed as n/a, never as 0.
    rng = random.Random(seed)
    N = len(rows)
    est = []
    for _ in range(B):
        n = d = 0
        for _i in range(N):
            a, b = rows[rng.randrange(N)]
            n += a
            d += b
        est.append(d / n if n else 0.0)
    est.sort()
    return est[int(.025 * B)], est[int(.975 * B)]


def report(TOT, GAMES):
    POPS = ["ALL", "FIELD", "US_ATTACK", "US_DEFEND"]
    BK = ["0", "1", "2", "3", "4+"]

    print("\n" + "=" * 88)
    print("(1)+(2)  25-ROUND CORE-DEATH RATE BY HOSTILE BODIES ON THE RING")
    print("         outcome = core removed at some D with r < D <= r+25")
    print("         rate is over CORE-ROUNDS; Wilson CI is NAIVE (ignores clustering)")
    print("=" * 88)
    c1, c1r = cells(TOT, "T1"), cells(TOT, "T1r")
    for pop in POPS:
        print(f"\n  {pop}")
        base = None
        n0, d0 = c1.get((pop, "0"), [0, 0])
        n1 = d1 = 0
        for bb in BK[1:]:
            a, c = c1.get((pop, bb), [0, 0])
            n1 += a
            d1 += c
        if n0 and n1:
            print(f"    >=1 vs 0 (the inherited claim's shape): "
                  f"clear {d0/n0:7.3%} -> occupied {d1/n1:7.3%}  "
                  f"x{(d1/n1)/(d0/n0):.2f}   n_clear={n0:,} n_occ={n1:,}")
        for b in BK:
            n, d = c1.get((pop, b), [0, 0])
            if not n:
                continue
            p, lo, hi = wilson(d, n)
            bc = boot_ci(GAMES, "T1", (pop, b))
            bs = (f"gameboot[{bc[0]:6.3%},{bc[1]:6.3%}]" if bc
                  else "gameboot[     n/a      ]")
            nr, dr = c1r.get((pop, b), [0, 0])
            if b == "0":
                base = p
            rel = f"  x{p/base:5.2f}" if base else ""
            print(f"    {b:>3} bodies  {p:7.3%} wilson[{lo:6.3%},{hi:6.3%}] "
                  f"{bs}  n={n:>9,} d={d:>8,}"
                  f"   per-round {dr/nr if nr else 0:7.4%}{rel}")

    print("\n" + "=" * 88)
    print("(3)  DURATION: 25-ROUND DEATH RATE BY HOW MANY OF THE LAST 25 ROUNDS")
    print("     THE RING WAS OCCUPIED BY >=1 HOSTILE BODY")
    print("=" * 88)
    c2 = cells(TOT, "T2")
    c2b = cells(TOT, "T2b")
    for pop in POPS:
        print(f"\n  {pop}   (all alive core-rounds)")
        for b in ["0", "1-5", "6-15", "16-25"]:
            n, d = c2.get((pop, b), [0, 0])
            if not n:
                continue
            bc = boot_ci(GAMES, "T2", (pop, b))
            bs = (f"gameboot[{bc[0]:6.3%},{bc[1]:6.3%}]" if bc
                  else "gameboot[     n/a      ]")
            p, lo, hi = wilson(d, n)
            print(f"    occupied {b:>5}/25  {p:7.3%} wilson[{lo:6.3%},{hi:6.3%}] "
                  f"{bs}  n={n:>9,} d={d:>8,}")
        print(f"  {pop}   RESTRICTED to rounds where the ring IS occupied NOW")
        print("           (isolates DURATION from PRESENCE -- this is the plank)")
        for b in ["1-5", "6-15", "16-25"]:
            n, d = c2b.get((pop, b), [0, 0])
            if not n:
                continue
            p, lo, hi = wilson(d, n)
            print(f"    occupied {b:>5}/25  {p:7.3%} wilson[{lo:6.3%},{hi:6.3%}]"
                  f"  n={n:>9,} d={d:>8,}")

    print("\n" + "=" * 88)
    print("CONFOUND A -- CORE HP STRATUM.  A core already low is about to die.")
    print("=" * 88)
    c3 = cells(TOT, "T3")
    for pop in POPS:
        print(f"\n  {pop}")
        print(f"    {'hp stratum':<12}" + "".join(f"{b+' bodies':>26}" for b in BK[:3]))
        for hs in ["500 (full)", "400-499", "250-399", "100-249", "<100"]:
            row = f"    {hs:<12}"
            any_ = False
            for b in BK[:3]:
                n, d = c3.get((pop, hs, b), [0, 0])
                if n:
                    any_ = True
                    row += f"{d/n:>10.3%} (n={n:>8,})"
                else:
                    row += f"{'-':>26}"
            if any_:
                print(row)

    print("\n" + "=" * 88)
    print("CONFOUND B -- LOCAL FORCE STRATUM.  Within (enemy bots near core,")
    print("enemy turrets near core, own bots near core), does ring occupancy")
    print("still predict death?   near = d^2 <= 36 of the core anchor")
    print("=" * 88)
    c4 = cells(TOT, "T4")
    for pop in POPS:
        print(f"\n  {pop}")
        print(f"    {'eb':<4}{'et':<4}{'ob':<4}" +
              "".join(f"{b+' bodies':>24}" for b in BK[:3]))
        for eb in range(4):
            for et in range(3):
                for ob in range(4):
                    key = (f"eb{eb}", f"et{et}", f"ob{ob}")
                    got = [(b, c4.get((pop, *key, b), [0, 0])) for b in BK[:3]]
                    if not any(n >= 2000 for _b, (n, _d) in got):
                        continue
                    row = f"    {eb:<4}{et:<4}{ob:<4}"
                    for _b, (n, d) in got:
                        row += (f"{d/n:>9.3%}(n={n:>7,})" if n else f"{'-':>24}")
                    print(row)

    print("\n" + "=" * 88)
    print("CONFOUND A+B COMBINED -- THE MATCHED CONTRAST, and the one the plank")
    print("has to survive.  `eb` = enemy builder bots within d^2<=36 of the core,")
    print("INCLUDING any standing on the ring.  Holding eb (and core HP, and enemy")
    print("turrets near the core) fixed and varying only WHERE those bots stand is")
    print("the plank's own manipulation: same body, ring tile vs one tile off.")
    print("=" * 88)
    c11 = cells(TOT, "T11")
    for pop in POPS:
        print(f"\n  {pop}   marginal on enemy-builders-near-core")
        for eb in range(1, 5):
            k = f"eb{eb}"
            n0, d0 = c11.get((pop, k, "near-only"), [0, 0])
            n1, d1 = c11.get((pop, k, "on-ring"), [0, 0])
            if n0 < 500 or n1 < 500:
                continue
            print(f"    {eb} enemy bots near   near-only {d0/n0:7.3%} (n={n0:>9,})"
                  f"   >=1 ON RING {d1/n1:7.3%} (n={n1:>9,})"
                  f"   x{(d1/n1)/(d0/n0) if d0 else float('nan'):5.2f}"
                  f"  abs {(d1/n1)-(d0/n0):+.3%}")
    c10 = cells(TOT, "T10")
    for pop in POPS:
        print(f"\n  {pop}   JOINT stratum (core HP x enemy bots near x enemy turrets near)")
        print(f"    {'hp':<12}{'eb':<5}{'et':<5}{'near-only':>24}{'>=1 on ring':>24}"
              f"{'ratio':>8}")
        for hs in ["500 (full)", "400-499", "250-399", "100-249", "<100"]:
            for eb in range(1, 5):
                for et in range(3):
                    k0 = (pop, hs, f"eb{eb}", f"et{et}", "near-only")
                    k1 = (pop, hs, f"eb{eb}", f"et{et}", "on-ring")
                    n0, d0 = c10.get(k0, [0, 0])
                    n1, d1 = c10.get(k1, [0, 0])
                    if n0 < 3000 or n1 < 3000:
                        continue
                    print(f"    {hs:<12}{eb:<5}{et:<5}"
                          f"{d0/n0:>13.3%}(n={n0:>7,}){d1/n1:>13.3%}(n={n1:>7,})"
                          f"{(d1/n1)/(d0/n0) if d0 else 0:>8.2f}")

    print("\n" + "=" * 88)
    print("THE PLANK'S OWN NUMBER -- DURATION, inside the matched stratum.")
    print("Rounds where the ring IS occupied now, split by how much of the last 25")
    print("it was occupied, holding core HP and enemy-bots-near-core fixed.")
    print("If retention pays, these rows rise. If not, the plank is not there.")
    print("=" * 88)
    c12 = cells(TOT, "T12")
    for pop in POPS:
        print(f"\n  {pop}")
        for hs in ["500 (full)", "400-499", "250-399", "100-249", "<100"]:
            for eb in range(1, 5):
                got = [(b, c12.get((pop, hs, f"eb{eb}", b), [0, 0]))
                       for b in ("1-5", "6-15", "16-25")]
                if not all(n >= 2000 for _b, (n, _d) in got):
                    continue
                row = f"    hp {hs:<11} eb{eb}  "
                for b, (n, d) in got:
                    row += f"{b}: {d/n:>7.3%}(n={n:>7,})  "
                print(row)

    print("\n" + "=" * 88)
    print("CONFOUND C -- LEAD/LAG.  Same outcome window (r, r+25].  Predictor")
    print("read at r, r-10, r-25, r-50, r-100 on a COMMON risk set (r >= 100).")
    print("An ACUTE CAUSE decays with lag; a MARKER of standing advantage does not.")
    print("=" * 88)
    c7 = cells(TOT, "T7")
    for pop in POPS:
        print(f"\n  {pop}    rate at >=1 hostile body vs 0, by predictor lag")
        for k in (0, 10, 25, 50, 100):
            n0, d0 = c7.get((pop, k, "0"), [0, 0])
            n1 = d1 = 0
            for b in BK[1:]:
                a, c = c7.get((pop, k, b), [0, 0])
                n1 += a
                d1 += c
            if not (n0 and n1):
                continue
            print(f"    lag {k:>3}   occ {d1/n1:7.3%} (n={n1:>9,})   "
                  f"clear {d0/n0:7.3%} (n={n0:>9,})   "
                  f"ratio x{(d1/n1)/(d0/n0) if d0 else 0:5.2f}   "
                  f"abs {(d1/n1)-(d0/n0):+.3%}")
    print("\n  DISCORDANT PAIRS (occupied now vs occupied 50 rounds ago):")
    c7d = cells(TOT, "T7d")
    for pop in POPS:
        print(f"    {pop}")
        for lbl in ("neither", "ago_only", "now_only", "now&ago"):
            n, d = c7d.get((pop, lbl), [0, 0])
            if n:
                print(f"      {lbl:<9} {fmt(d, n)}")

    print("\n" + "=" * 88)
    print("CONTROL 3 -- NULL OUTCOME.  Death in (r+200, r+225], which the ring")
    print("at round r cannot plausibly cause.  The effect must shrink toward null.")
    print("=" * 88)
    c6 = cells(TOT, "T6")
    for pop in POPS:
        n0, d0 = c6.get((pop, "0"), [0, 0])
        n1 = d1 = 0
        for b in BK[1:]:
            a, c = c6.get((pop, b), [0, 0])
            n1 += a
            d1 += c
        if n0 and n1:
            print(f"  {pop:<10} occ {d1/n1:7.3%} (n={n1:>9,})   "
                  f"clear {d0/n0:7.3%} (n={n0:>9,})   "
                  f"ratio x{(d1/n1)/(d0/n0) if d0 else 0:5.2f}")

    print("\n" + "=" * 88)
    print("CONTROL 2 -- TEAM POLARITY.  A core's OWN builder bots on its OWN ring.")
    print("If this shows the same hazard, the effect is 'bodies near a dying core'")
    print("i.e. a pure MARKER.")
    print("=" * 88)
    c5 = cells(TOT, "T5")
    for pop in POPS:
        print(f"  {pop}")
        for b in ["0", "1", "2", "3+"]:
            n, d = c5.get((pop, b), [0, 0])
            if n:
                print(f"    {b:>3} FRIENDLY bodies on own ring  {fmt(d, n)}")

    print("\n" + "=" * 88)
    print("SHAPE -- occupancy rate as a function of TIME TO DEATH, vs cores that")
    print("never die.  A 25-round-acting cause spikes late; a marker rises early.")
    print("=" * 88)
    c9 = cells(TOT, "T9")
    for pop in POPS:
        print(f"  {pop}")
        for band in ("201+", "101-200", "51-100", "26-50", "1-25"):
            n, d = c9.get((pop, "DIES", band), [0, 0])
            if n:
                print(f"    dies in {band:>7} rounds : ring occupied "
                      f"{d/n:7.3%} of those core-rounds  (n={n:>9,})")
        n, d = c9.get((pop, "SURVIVES", "all"), [0, 0])
        if n:
            print(f"    never dies          : ring occupied {d/n:7.3%} "
                  f"of those core-rounds  (n={n:>9,})")

    print("\n" + "=" * 88)
    print("ROUND-BAND STRATUM")
    print("=" * 88)
    c8 = cells(TOT, "T8")
    for pop in POPS:
        print(f"  {pop}")
        for lo in (0, 200, 400, 600, 800, 1000):
            band = f"r{lo}-{lo+199}"
            n0, d0 = c8.get((pop, band, "0"), [0, 0])
            n1 = d1 = 0
            for b in BK[1:]:
                a, c = c8.get((pop, band, b), [0, 0])
                n1 += a
                d1 += c
            if n0 and n1:
                print(f"    {band:<12} occ {d1/n1:7.3%} (n={n1:>8,})  "
                      f"clear {d0/n0:7.3%} (n={n0:>8,})  "
                      f"x{(d1/n1)/(d0/n0) if d0 else 0:5.2f}")


# ------------------------------------------------------- outcome validate ---

def validate(limit, seed):
    """CONTROL 4/5: is the OUTCOME VARIABLE (core removal round) right?

    Three independent cross-checks, each of which can come out the other way:
      a) our decoded core-death round vs corpus/events.tsv DEATH/core rows,
         which were produced by a DIFFERENT decoder (tools/corpus/*).
      b) the replay's own winCondition/winner fields: a game whose condition is
         `core_destroyed` MUST have exactly one core removed, and the survivor
         must be the winner.  A game ending on tiebreak must have ZERO.
      c) core HP at the round before removal must be small; a core removed
         while at 500 HP would mean the HP stream or the id mapping is wrong.
    """
    files = sorted(p.name for p in ARCHIVE.glob("*.replay26"))
    random.Random(seed).shuffle(files)
    files = files[:limit]
    want = set(files)
    ev = defaultdict(dict)             # file -> team -> round
    with (ROOT / "corpus" / "events.tsv").open() as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        i_f, i_e, i_r, i_t, i_k = (hdr.index(c) for c in
                                   ("file", "ev", "rnd", "team", "kind"))
        for line in fh:
            c = line.rstrip("\n").split("\t")
            if len(c) <= i_k or c[i_e] != "DEATH" or c[i_k] != "core":
                continue
            if c[i_f] in want:
                ev[c[i_f]][int(c[i_t])] = int(c[i_r])
    agree = dis = only_us = only_them = 0
    PAIRS = []
    cond_ok = cond_bad = 0
    hp_at_death = []
    hp_high = 0
    winner_ok = winner_bad = 0
    n = 0
    for f in files:
        p = ARCHIVE / f
        dec = decode(p)
        if dec is None:
            continue
        n += 1
        R, ser, death, _nl, _d = dec
        data = p.read_bytes()
        cond, winner = "", None
        for num, wire, value in fields(data):
            if num == 6 and wire == WIRE_LEN:
                cond = value.decode("utf-8", "replace")
            elif num == 4 and wire == 0:
                winner = value
        theirs = ev.get(f, {})
        for t in (0, 1):
            mine = death[t]
            th = theirs.get(t)
            if mine is not None and th is not None:
                PAIRS.append((mine, th))
                agree += (mine == th)
                dis += (mine != th)
            elif mine is not None:
                only_us += 1
            elif th is not None:
                only_them += 1
            if mine is not None:
                # HP at the last alive round for this core
                if ser[t]["hp"]:
                    v = ser[t]["hp"][-1]
                    hp_at_death.append(v)
                    hp_high += (v > 100)
        ndead = sum(1 for t in (0, 1) if death[t] is not None)
        if cond == "core_destroyed":
            cond_ok += (ndead == 1)
            cond_bad += (ndead != 1)
            if ndead == 1:
                dead_t = 0 if death[0] is not None else 1
                winner_ok += (winner is not None and winner == 1 - dead_t)
                winner_bad += (winner is None or winner != 1 - dead_t)
        elif cond:
            cond_ok += (ndead == 0)
            cond_bad += (ndead != 0)
    print(f"OUTCOME-VARIABLE VALIDATION over {n} replays\n")
    print("  (a) core-death round vs corpus/events.tsv (independent decoder)")
    print(f"      agree on round        : {agree}")
    print(f"      DISAGREE on round     : {dis}")
    print(f"      only this decoder saw : {only_us}")
    print(f"      only events.tsv saw   : {only_them}")
    print("\n  (b) winCondition consistency  (core_destroyed <=> exactly 1 core removed)")
    print(f"      consistent            : {cond_ok}")
    print(f"      INCONSISTENT          : {cond_bad}")
    print(f"      survivor == winner    : {winner_ok} ok / {winner_bad} bad")
    if hp_at_death:
        hp_at_death.sort()
        print("\n  (c) core HP at its last alive round (independent HP stream)")
        print(f"      n={len(hp_at_death)}  min={hp_at_death[0]} "
              f"med={hp_at_death[len(hp_at_death)//2]} max={hp_at_death[-1]}")
        print(f"      cores removed while still above 100 HP: {hp_high} "
              f"({hp_high/len(hp_at_death):.2%})")
    print("\n  MUTANT CONTROL -- check (a) must produce the OTHER verdict when the")
    print("  decoded death round is deliberately corrupted:")
    for shift in (0, 1, 7):
        a = sum(1 for m, t in PAIRS if m + shift == t)
        print(f"      death_round + {shift:>2}  ->  agree {a}/{len(PAIRS)} "
              f"({a/max(1,len(PAIRS)):.1%})")
    return 0


# --------------------------------------------------------- geometry check ---

def geometry_control():
    """CONTROL 1: print the ring of a real core on a real replay, by hand."""
    files = sorted(p.name for p in ARCHIVE.glob("*.replay26"))[:1]
    f = ARCHIVE / files[0]
    data = f.read_bytes()
    map_buf = None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
            break
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4 and wire == WIRE_LEN:
            d = {n: v for n, _, v in fields(value)}
            cores.append((d.get(1), d.get(2, 0), read_pos(d[3])))
    print(f"CONTROL 1 -- RING GEOMETRY, worked on a real replay")
    print(f"  file {files[0]}   map {w}x{h}")
    for cid, team, pos in cores:
        x, y = pos
        foot = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        ring = ring_tiles(pos, w, h)
        print(f"\n  core id={cid} team={team} anchor(NW of 2x2)={pos}")
        print(f"    footprint (4 tiles): {foot}")
        print(f"    ring ({len(ring)} tiles): {sorted(ring)}")
        # independent re-derivation: the 4x4 box minus the footprint
        box = {(x + a, y + b) for a in (-1, 0, 1, 2) for b in (-1, 0, 1, 2)}
        alt = {t for t in box - set(foot) if 0 <= t[0] < w and 0 <= t[1] < h}
        print(f"    independent re-derivation (4x4 box minus footprint, clipped):"
              f" {len(alt)} tiles, identical = {alt == set(ring)}")
        for t in ring:
            dmin = min((t[0] - fx) ** 2 + (t[1] - fy) ** 2 for fx, fy in foot)
            assert dmin in (1, 2), (t, dmin)
        print("    every ring tile has min d^2 to the footprint in {1,2}: OK "
              "(1 = orthogonal, 2 = diagonal corner)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
