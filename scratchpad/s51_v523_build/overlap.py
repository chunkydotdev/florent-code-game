#!/usr/bin/env python3
"""v521 THE CURRENCY, MEASURED DIRECTLY -- OVERLAP(fully-sealed x turret alive
and funded), replay-side.

⛔ THE QUANTITY THIS EXISTS FOR, and it is v520's own reframe.  v520 bought more
seals (cumulative seats 6.63 -> 6.99, simultaneous closure 31.7% -> 43.9%) and
POOLED HEAL-BACK DID NOT MOVE (median 0.000 in all three arms).  Its failure reel
found why: across six games, 0 of 119 enemy-core heal rounds fell in a round
where every heal seat was denied, and one game held a genuine 43-round closure
that sat DISJOINT from its own turret's life.  So the metric is not seats and it
is not closure -- it is the number of rounds in which BOTH hold at once.

PER GAME, EMITTED:
  n_seats         legal heal seats (in-bounds, not wall).  8 in the open field.
  sealed_r        rounds with ALL n_seats denied by us (simultaneous, not
                  cumulative -- the two diverge and the reel is why we print
                  both)
  live_r          rounds with >= 1 FORWARD turret of ours alive (sentinel or
                  gunner within FWD_DSQ of their core centre)
  funded_r        rounds with our global ammo >= FUND_AMMO
  livefund_r      rounds with a forward turret alive AND funded
  ⭐ overlap_r    THE CURRENCY: sealed AND live AND funded, in the same round
  overlap_first   first such round, -1 if never
  ⭐ net_in       NET enemy-core HP change summed over OVERLAP rounds
                  (negative = we are winning HP).  dmg_in / heal_in are its two
                  halves.
  ⭐ net_out      the same over every other round.
  dmg_in/out, heal_in/out, and per-round means for both.
  Plus disjointness: seal_only_r (sealed, no funded turret) and
  shot_only_r (funded turret, collar not sealed) -- the two halves of the reel's
  finding, counted rather than narrated.

⛔ EVERY INPUT IS ENGINE-SIDE.  Seat denial comes from `ringwalk`'s entity walk
(the same machinery `seatrate.py` uses, guards running in place).  Turret
liveness comes from placeEntity/removeEntity.  FUNDING COMES OFF THE WIRE --
update field 6 carries each team's scalars and field 7 is the ammunition
balance, which is how `turrets.py` builds its own ammo series.  Core HP deltas
come from UpdateHp on the enemy core id.  No bot stdout is involved: platform
replays carry none (CLAUDE.md s28) and a local instrument that needed it would
not port.

⛔ GUARDS, EVERY ONE DRIVEN TO BOTH VERDICTS (`--selftest`):
  G1 `ringwalk`'s own selftest runs IN PLACE.
  G2 KNOWN SYNTHETIC TAPE -> exact expected row (overlap counted only where all
     three conditions hold in the same round).
  G3 MUTATION CONTROL: remove the funding on the overlap rounds; overlap_r must
     fall to 0 and net_in must move to net_out.  A folder that ignored the ammo
     column returns the same row.
  G4 SIMULTANEITY CONTROL: a tape where the collar is sealed and the turret is
     funded but NEVER IN THE SAME ROUND must read overlap_r = 0 with both
     sealed_r and livefund_r > 0.  This is the reel's finding as a unit test.
  G5 ZERO-DENOMINATOR CONTROL: a game with 0 overlap rounds must report
     net_in = None, not 0 -- pooling "never overlapped" with "overlapped and
     netted nothing" is the error that would make a dead plank look neutral.
  G6 ENEMY-ONLY CONTROL: a tape where only the ENEMY occupies the seats and owns
     the turrets must read sealed_r = 0 and live_r = 0.
  G7 REAL-DATA TEAM-SWAP POSITIVE CONTROL: re-reading one real replay with the
     team flipped must MOVE overlap_r / net_in / net_out.  A column that reads
     the same either way is reading nothing.
  G8 CHANNEL CROSS-CHECK on real data: the count of -18 UpdateHp deltas on the
     enemy core must equal the number of enemy-core sentinel hits counted from
     FireTurret destinations (`turrets.py`'s independent channel).

Usage:
  overlap.py --selftest
  overlap.py <grid.tsv> <repdir> <out.tsv> [arm_label]
  overlap.py --one <replay26> <map> <A|B>
  overlap.py --report <out.tsv> [<out.tsv> ...]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from ringwalk import (  # noqa: E402
    GuardFail, MAPS, check_geom, denied_by, dsq_centre, occupancy, replay_map,
    ring_tiles,
)
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos, scalars,
)

FWD_DSQ = 40          # a turret is FORWARD at this d^2 of their core centre
                      # (FS_SENT_BEAT_DSQ, so the replay-side and bot-side
                      # definitions cannot drift)
FUND_AMMO = 10        # one sentinel shot, from the engine's cost table
TURRET_KINDS = ("sentinel", "gunner")


# --------------------------------------------------------------------------
# THE FOLD.  Separated from the wire walk so the guards can drive it on
# synthetic tapes -- a fold that can only be exercised through a real replay
# cannot be driven the other way.
# --------------------------------------------------------------------------
def fold(tape, n_seats):
    """tape: [(round, n_denied, fwd_alive, ammo, core_delta)] per round."""
    sealed_r = live_r = funded_r = livefund_r = overlap_r = 0
    seal_only_r = shot_only_r = 0
    first = -1
    dmg = {"in": 0, "out": 0}
    heal = {"in": 0, "out": 0}
    for rnd, nden, alive, ammo, delta in tape:
        sealed = (n_seats > 0 and nden == n_seats)
        funded = ammo >= FUND_AMMO
        lf = bool(alive) and funded
        if sealed:
            sealed_r += 1
        if alive:
            live_r += 1
        if funded:
            funded_r += 1
        if lf:
            livefund_r += 1
        key = "out"
        if sealed and lf:
            overlap_r += 1
            key = "in"
            if first < 0:
                first = rnd
        elif sealed and not lf:
            seal_only_r += 1
        elif lf and not sealed:
            shot_only_r += 1
        if delta < 0:
            dmg[key] += -delta
        elif delta > 0:
            heal[key] += delta
    net_in = (dmg["in"] - heal["in"]) if overlap_r else None
    nonoverlap = len(tape) - overlap_r
    net_out = (dmg["out"] - heal["out"]) if nonoverlap else None
    return dict(
        n_seats=n_seats,
        rounds=len(tape),
        sealed_r=sealed_r,
        live_r=live_r,
        funded_r=funded_r,
        livefund_r=livefund_r,
        overlap_r=overlap_r,
        overlap_first=first,
        seal_only_r=seal_only_r,
        shot_only_r=shot_only_r,
        dmg_in=dmg["in"], heal_in=heal["in"], net_in=net_in,
        dmg_out=dmg["out"], heal_out=heal["out"], net_out=net_out,
        net_per_overlap=(round(net_in / overlap_r, 4)
                         if overlap_r else None),
        net_per_nonoverlap=(round(net_out / nonoverlap, 4)
                            if nonoverlap else None),
    )


# --------------------------------------------------------------------------
# THE WIRE WALK.  One pass, five channels: entities (seats + turrets), team
# scalars (ammo), and UpdateHp on the enemy core.
# --------------------------------------------------------------------------
def tape_for(replay, mapname, seat, our_override=None):
    _w, _h, _rows, ours, E, seats, _corners = check_geom(replay, mapname, seat)
    if our_override is not None:
        ours = our_override
        _rw, _rh, _rr, cores = replay_map(replay)
        E = {c["team"]: c["pos"] for c in cores}[1 - ours]
        s2, _c2 = ring_tiles(E[0], E[1], _w, _h)
        seats = [t for t in s2 if _rows[t[1]][t[0]] != 1]
    _rw, _rh, _rr, cores = replay_map(replay)
    ecore_id = {c["team"]: c["id"] for c in cores}[1 - ours]
    seatset = list(seats)
    Ectr = (E[0] + .5, E[1] + .5)

    data = Path(replay).read_bytes()
    mb, turns = None, []
    for n, wt, v in fields(data):
        if n == 1 and wt == WIRE_LEN:
            mb = v
        elif n == 3 and wt == WIRE_LEN:
            turns.append(v)
    ents = {}
    for c in cores:
        ents[c["id"]] = ("core", c["team"], c["pos"], 0)
    ammo = {0: 0, 1: 0}
    tape = []
    for rnd, tb in enumerate(turns):
        delta_sum = 0
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        ents[e.id] = (e.kind, e.team, e.pos, rnd)
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        k, t, _p, b = ents[eid]
                        ents[eid] = (k, t, to, b)
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                elif un == 5:
                    eid, d = parse_update_hp(ubuf)
                    if eid == ecore_id:
                        delta_sum += d
                elif un == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                ammo[tn - 1] = scalars(tv).get(7, 0)
        occ = occupancy(ents)
        nden = len(denied_by(occ, seatset, ours))
        alive = any(k in TURRET_KINDS and t == ours
                    and dsq_centre(p, E) <= FWD_DSQ
                    for (k, t, p, _b) in ents.values())
        tape.append((rnd, nden, alive, ammo[ours], delta_sum))
    return tape, len(seatset), ours, ecore_id


def analyse(replay, mapname, seat, our_override=None):
    tape, n, ours, _cid = tape_for(replay, mapname, seat, our_override)
    row = fold(tape, n)
    row["our_team"] = ours
    return row


# ============================== SELFTEST =====================================
def _mk(spec):
    """spec: list of (n_denied, alive, ammo, core_delta)."""
    return [(i, a, b, c, d) for i, (a, b, c, d) in enumerate(spec)]


def selftest():
    import ringwalk
    fails = []

    def chk(name, cond, detail=""):
        print(("  ok   " if cond else "  FAIL ") + name +
              (("  " + detail) if detail and not cond else ""))
        if not cond:
            fails.append(name)

    print("G1 ringwalk selftest, in place")
    try:
        ringwalk.selftest()
        chk("G1 ringwalk guards", True)
    except Exception as exc:                                  # noqa: BLE001
        chk("G1 ringwalk guards", False, repr(exc))

    print("G2 known synthetic tape")
    # r0: sealed, no turret        -> seal_only
    # r1: sealed, turret, ammo 20  -> OVERLAP, core -18
    # r2: sealed, turret, ammo 20  -> OVERLAP, core +4
    # r3: not sealed, turret, ammo -> shot_only, core -18
    # r4: sealed, turret, ammo 0   -> seal_only (UNFUNDED), core +4
    t = _mk([(8, 0, 0, 0), (8, 1, 20, -18), (8, 1, 20, 4),
             (5, 1, 20, -18), (8, 1, 0, 4)])
    r = fold(t, 8)
    chk("G2 overlap_r == 2", r["overlap_r"] == 2, str(r["overlap_r"]))
    chk("G2 overlap_first == 1", r["overlap_first"] == 1)
    chk("G2 seal_only_r == 2", r["seal_only_r"] == 2, str(r["seal_only_r"]))
    chk("G2 shot_only_r == 1", r["shot_only_r"] == 1)
    chk("G2 net_in == 18-4 == 14", r["net_in"] == 14, str(r["net_in"]))
    chk("G2 net_out == 18-4 == 14", r["net_out"] == 14, str(r["net_out"]))
    chk("G2 sealed_r == 4", r["sealed_r"] == 4)
    # ⛔ 3, NOT 4, AND THE GUARD CAUGHT THE AUTHOR'S OWN ARITHMETIC FIRST.
    # ammo is 20 in r1/r2/r3 and 0 in r0/r4, so THREE rounds are funded and the
    # r4 round is sealed-but-UNFUNDED -- which is the whole distinction this
    # instrument exists to make.  The first draft asserted 4 and failed.
    chk("G2 funded_r == 3", r["funded_r"] == 3, str(r["funded_r"]))
    chk("G2 livefund_r == 3", r["livefund_r"] == 3, str(r["livefund_r"]))

    print("G3 MUTATION CONTROL: strip the funding")
    t3 = _mk([(8, 0, 0, 0), (8, 1, 0, -18), (8, 1, 0, 4),
              (5, 1, 0, -18), (8, 1, 0, 4)])
    r3 = fold(t3, 8)
    chk("G3 overlap_r falls to 0", r3["overlap_r"] == 0, str(r3["overlap_r"]))
    chk("G3 net_in becomes None", r3["net_in"] is None)
    chk("G3 the damage moved to net_out",
        r3["net_out"] == (18 + 18) - (4 + 4), str(r3["net_out"]))

    print("G4 SIMULTANEITY CONTROL (the reel's finding as a unit test)")
    t4 = _mk([(8, 0, 0, -18), (8, 0, 0, 4), (3, 1, 40, -18), (2, 1, 40, 4)])
    r4 = fold(t4, 8)
    chk("G4 sealed_r > 0", r4["sealed_r"] == 2)
    chk("G4 livefund_r > 0", r4["livefund_r"] == 2)
    chk("G4 overlap_r == 0 anyway", r4["overlap_r"] == 0)
    chk("G4 overlap_first == -1", r4["overlap_first"] == -1)

    print("G5 ZERO-DENOMINATOR CONTROL")
    chk("G5 net_in is None, not 0", r4["net_in"] is None, repr(r4["net_in"]))
    chk("G5 net_per_overlap is None", r4["net_per_overlap"] is None)

    print("G6 ENEMY-ONLY CONTROL (fold level: nothing of ours denied or alive)")
    t6 = _mk([(0, 0, 0, -18)] * 5)
    r6 = fold(t6, 8)
    chk("G6 sealed_r == 0", r6["sealed_r"] == 0)
    chk("G6 live_r == 0", r6["live_r"] == 0)
    chk("G6 overlap_r == 0", r6["overlap_r"] == 0)

    rp = _pick_real()
    if rp is None:
        chk("G7/G8 real-data controls", False, "no real replay found")
    else:
        replay, mapname, seat = rp
        print("G7 REAL-DATA TEAM-SWAP POSITIVE CONTROL  (%s)" % Path(replay).name)
        a = analyse(replay, mapname, seat)
        b = analyse(replay, mapname, seat, our_override=1 - a["our_team"])
        moved = sum(1 for k in ("overlap_r", "sealed_r", "live_r",
                                "dmg_in", "dmg_out", "heal_out")
                    if a.get(k) != b.get(k))
        chk("G7 >= 2 columns move on the flip", moved >= 2,
            "moved=%d  a=%s b=%s" % (moved, a, b))
        print("G8 CHANNEL CROSS-CHECK: -18 UpdateHp vs FireTurret core hits")
        try:
            import turrets
            res = turrets.run(Path(replay), a["our_team"])
            fire_hits = sum(t["core_shots"] for t in res["turrets"].values()
                            if t["team"] == a["our_team"]
                            and t["kind"] == "sentinel")
            hp_hits = res["core_sent_hits"][1 - a["our_team"]]
            chk("G8 channels agree", fire_hits == hp_hits,
                "fire=%d hp=%d" % (fire_hits, hp_hits))
        except Exception as exc:                              # noqa: BLE001
            chk("G8 channels agree", False, repr(exc))

    print("\nSELFTEST", "PASS" if not fails else "FAIL %s" % fails)
    return 0 if not fails else 1


def _pick_real():
    for base in (HERE / "grid", HERE / "eq" / "dose", HERE / "smoke",
                 HERE.parent / "s51_v520_build" / "grid"):
        if not base.exists():
            continue
        for rp in sorted(base.rglob("*.replay26")):
            name = rp.stem
            parts = name.split("_")
            if len(parts) >= 3 and parts[0] in MAPS and parts[-1] in ("A", "B"):
                return str(rp), parts[0], parts[-1]
    return None


# =============================== DRIVERS =====================================
COLS = ["tag", "map", "seed", "seat", "ours", "turn", "n_seats", "rounds",
        "sealed_r", "live_r", "funded_r", "livefund_r", "overlap_r",
        "overlap_first", "seal_only_r", "shot_only_r",
        "dmg_in", "heal_in", "net_in", "dmg_out", "heal_out", "net_out",
        "net_per_overlap", "net_per_nonoverlap"]


def run(grid_tsv, repdir, out_tsv, label=""):
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    out = open(out_tsv, "w")
    out.write("\t".join(COLS) + "\n")
    n = bad = 0
    for r in rows:
        rp = Path(repdir) / (r["tag"] + ".replay26")
        if not rp.exists():
            bad += 1
            continue
        try:
            row = analyse(str(rp), r["map"], r["seat"])
        except GuardFail as exc:
            print("GUARDFAIL %s %s" % (r["tag"], exc), file=sys.stderr)
            bad += 1
            continue
        row.update(tag=r["tag"], map=r["map"], seed=r["seed"], seat=r["seat"],
                   ours=r["ours"], turn=r["turn"])
        out.write("\t".join("" if row.get(c) is None else str(row.get(c, ""))
                            for c in COLS) + "\n")
        n += 1
    out.close()
    print("%s: %d games, %d skipped -> %s" % (label or out_tsv, n, bad, out_tsv))


def _mean(vals):
    vals = [v for v in vals if v is not None]
    return (sum(vals) / len(vals)) if vals else None


def report(paths):
    print("%-14s %6s %8s %8s %8s %9s %9s %10s %10s" %
          ("arm", "n", "sealed", "livefund", "OVERLAP", "ovl>0", "ovl_1st",
           "net/ovl_r", "net/other"))
    for p in paths:
        rows = list(csv.DictReader(open(p), delimiter="\t"))
        if not rows:
            continue
        def col(c, cast=float):
            out = []
            for r in rows:
                v = r.get(c, "")
                out.append(cast(v) if v not in ("", None) else None)
            return out
        ovl = col("overlap_r")
        first = [v for v in col("overlap_first") if v is not None and v >= 0]
        print("%-14s %6d %8.1f %8.1f %8.2f %8.1f%% %9s %10s %10s" % (
            Path(p).stem, len(rows),
            _mean(col("sealed_r")) or 0.0,
            _mean(col("livefund_r")) or 0.0,
            _mean(ovl) or 0.0,
            100.0 * sum(1 for v in ovl if v and v > 0) / len(rows),
            ("%.0f" % _mean(first)) if first else "-",
            ("%.3f" % _mean(col("net_per_overlap")))
            if _mean(col("net_per_overlap")) is not None else "-",
            ("%.3f" % _mean(col("net_per_nonoverlap")))
            if _mean(col("net_per_nonoverlap")) is not None else "-",
        ))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        report(sys.argv[2:])
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        print(analyse(sys.argv[2], sys.argv[3], sys.argv[4]))
        return
    run(sys.argv[1], sys.argv[2], sys.argv[3],
        sys.argv[4] if len(sys.argv) > 4 else "")


if __name__ == "__main__":
    main()
