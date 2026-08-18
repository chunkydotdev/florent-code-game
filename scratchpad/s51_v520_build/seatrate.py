#!/usr/bin/env python3
"""v520 THE PINCER'S CENTREPIECE METRIC -- SEAL RATE, replay-side.

The pincer thesis: two raider bodies ride one relay chain and are thrown to
OPPOSITE ARCS of the enemy core, so the 8 orthogonal heal seats are sealed IN
PARALLEL instead of one body walking the ring.  If that is true the seats-per-
round-of-presence goes UP; if only the body count went up and nothing sealed
faster, the rate is flat and the plank is dead.  This measures exactly that.

⛔ COPIED, NOT REWRITTEN.  Seat geometry, the D|d denial alphabet, the
occupancy fold and the turn-stream walk are `ringwalk.py`, which is
`s51_closure_autopsy/{seattape,ferry}.py` with their guards running in place
(plus the field-4 Core-seed correction documented there).

PER GAME, EMITTED:
  n_seats            legal seats: in-bounds AND not wall (`_fs_ring12`).  8 in
                     the open field; a wall or a border can make it fewer, and
                     "closure" then means all of THOSE.  Reported, never
                     assumed.
  seats_sealed       seats EVER denied by us (our barrier/harvester/gunner/
                     sentinel/launcher/core on the tile, or our builder body
                     standing on it) -- seattape's D or d.
  first_seal / last_seal   round of the first / last seat's FIRST denial.
  closure_round      first round on which ALL n_seats are denied
                     SIMULTANEOUSLY.  -1 = never.
  closure_cum_round  first round at which the CUMULATIVE ever-denied set
                     reaches n_seats.  The two differ whenever a seal is lost
                     and retaken, and reporting only one of them is how a
                     leaky seal reads as a closure.
  atring_rounds      rounds with >= 1 of our builder bots within d^2 <= 50 of
                     the enemy core (CENTRE convention -- reel/tape.py's, so
                     this is comparable to near_bot / phase.marks).
  atring2_rounds     rounds with >= 2.  THE TWO-BODY PRESENCE SHARE, so a
                     two-body vs one-body seal-rate cut is computable off this
                     same tape with no second run.
  seal_rate          seats_sealed per 100 rounds of at-ring presence.
                     None (blank) when atring_rounds == 0 -- a game where no
                     body ever reached the ring has NO rate, and calling it 0
                     would pool "never went" with "went and failed".
  sealed_by_bldg / sealed_by_body   the channel of each seat's FIRST denial.

⛔ GUARDS, EVERY ONE DRIVEN BOTH WAYS (`--selftest`):
  G1 ringwalk's own selftest runs in place (geometry, occupancy precedence,
     the D|d alphabet, the field-5 core-seed bug, the wrong-map refusal).
  G2 KNOWN SYNTHETIC TAPE -> exact expected row.
  G3 MUTATION CONTROL: delete the last seat's denial; seats_sealed must fall
     and BOTH closure columns must go to -1.  A folder that ignored the seat
     column would return the same row.
  G4 SIMULTANEITY CONTROL: a tape where all 8 seats are denied but never in
     the same round must give closure_round = -1 and closure_cum_round >= 0.
  G5 ZERO-PRESENCE CONTROL: atring_rounds = 0 -> seal_rate is None, not 0 and
     not a ZeroDivisionError.
  G6 ENEMY-ONLY CONTROL: a tape where only the ENEMY occupies the seats must
     give seats_sealed = 0.  An instrument that counted "any occupant" reads 8.
  G7 REAL-DATA TEAM-SWAP POSITIVE CONTROL: re-reading one real replay with the
     seat->team assignment flipped must MOVE seats_sealed / atring_rounds /
     seal_rate.  A column that reads the same either way is reading nothing.

Usage:
  seatrate.py --selftest
  seatrate.py <grid.tsv> <repdir> <out.tsv> [arm_label]
  seatrate.py --one <replay26> <map> <A|B>
  seatrate.py --report <out.tsv> [<out.tsv> ...]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ringwalk import (  # noqa: E402
    GuardFail, MAPS, check_geom, denied_by, dsq_centre, occupancy, walk,
)

ATRING_DSQ = 50          # presence envelope, CENTRE convention


# --------------------------------------------------------------------------
# THE FOLD.  Deliberately separated from the wire walk so the guards can drive
# it on synthetic tapes -- a fold that can only be exercised through a real
# replay cannot be driven the other way.
# --------------------------------------------------------------------------
def fold(tape, n_seats):
    """tape: [(round, denied_set, denial_kind_map, n_bots_at_ring)] per round.

    denial_kind_map: seat -> 'bldg' | 'body' for the seats denied this round.
    """
    first = {}
    kind = {}
    closure = -1
    closure_cum = -1
    atring = atring2 = 0
    ever = set()
    for rnd, den, kinds, nbots in tape:
        if nbots >= 1:
            atring += 1
        if nbots >= 2:
            atring2 += 1
        for s in den:
            if s not in first:
                first[s] = rnd
                kind[s] = kinds.get(s, "bldg")
        ever |= den
        if closure < 0 and n_seats > 0 and len(den) == n_seats:
            closure = rnd
        if closure_cum < 0 and n_seats > 0 and len(ever) == n_seats:
            closure_cum = rnd
    sealed = len(first)
    rate = (100.0 * sealed / atring) if atring else None
    return dict(
        n_seats=n_seats,
        seats_sealed=sealed,
        first_seal=min(first.values()) if first else -1,
        last_seal=max(first.values()) if first else -1,
        closure_round=closure,
        closure_cum_round=closure_cum,
        atring_rounds=atring,
        atring2_rounds=atring2,
        two_body_share=(round(atring2 / atring, 4) if atring else None),
        seal_rate=(round(rate, 3) if rate is not None else None),
        sealed_by_bldg=sum(1 for v in kind.values() if v == "bldg"),
        sealed_by_body=sum(1 for v in kind.values() if v == "body"),
        seat_first_rounds=",".join(str(first.get(s, -1)) for s in
                                   sorted(first)) if first else "",
    )


def tape_for(replay, mapname, seat, our_override=None):
    """Build the per-round tape from a replay.  our_override flips the team
    for the G7 positive control."""
    _w, _h, _rows, ours, E, seats, _corners = check_geom(replay, mapname, seat)
    if our_override is not None:
        ours = our_override
        # the ENEMY core moves with the flip -- read it off the replay
        from ringwalk import replay_map
        _rw, _rh, _rr, cores = replay_map(replay)
        E = {c["team"]: c["pos"] for c in cores}[1 - ours]
        from ringwalk import ring_tiles
        s2, _c2 = ring_tiles(E[0], E[1], _w, _h)
        seats = [t for t in s2 if _rows[t[1]][t[0]] != 1]
    seatset = list(seats)
    tape = []
    for rnd, ents in walk(replay):
        occ = occupancy(ents)
        den = denied_by(occ, seatset, ours)
        kinds = {}
        for s in den:
            kinds[s] = "body" if occ[s][0] == "builder_bot" else "bldg"
        nbots = sum(1 for (k, t, p, _b) in ents.values()
                    if k == "builder_bot" and t == ours
                    and dsq_centre(p, E) <= ATRING_DSQ)
        tape.append((rnd, den, kinds, nbots))
    return tape, len(seatset), ours, E


def analyse(replay, mapname, seat, our_override=None):
    tape, n, ours, E = tape_for(replay, mapname, seat, our_override)
    row = fold(tape, n)
    row["rounds"] = len(tape)
    row["our_team"] = ours
    row["enemy_core"] = "%d,%d" % E
    return row


# ============================== SELFTEST =====================================

S8 = [(10, 1), (11, 1), (12, 2), (12, 3), (11, 4), (10, 4), (9, 3), (9, 2)]


def _mk(rounds, denials, bots):
    """denials: {round: [(seat, kind)]}, bots: {round: n}."""
    out = []
    for r in range(rounds):
        d = denials.get(r, [])
        out.append((r, {s for s, _k in d}, {s: k for s, k in d},
                    bots.get(r, 0)))
    return out


def selftest():
    ok = True

    def chk(name, cond, detail=""):
        nonlocal ok
        print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                              ("  " + detail) if detail else ""))
        if not cond:
            ok = False

    # G1 -- ringwalk's guards run IN PLACE, not re-implemented ----------------
    print("=== G1: ringwalk selftest, in place ===")
    import ringwalk
    if not ringwalk.selftest():
        ok = False

    print("=== seatrate selftest ===")

    # G2 -- known synthetic tape -> exact row ---------------------------------
    # 8 seats.  Seats seal one per round from r5; all 8 are held from r12.
    den = {}
    held = []
    for i, s in enumerate(S8):
        held.append((s, "body" if i < 3 else "bldg"))
        for r in range(5 + i, 30):
            den.setdefault(r, [])
        den[5 + i] = list(held)
    for r in range(5, 30):
        den[r] = list(held[:min(8, max(0, r - 4))])
    bots = {r: (2 if 8 <= r <= 20 else 1) for r in range(3, 25)}
    t = _mk(30, den, bots)
    row = fold(t, 8)
    chk("G2 seats_sealed", row["seats_sealed"] == 8, str(row["seats_sealed"]))
    chk("G2 first_seal/last_seal", (row["first_seal"], row["last_seal"]) == (5, 12),
        "%s/%s" % (row["first_seal"], row["last_seal"]))
    chk("G2 closure_round == 12 (all 8 simultaneous)", row["closure_round"] == 12,
        str(row["closure_round"]))
    chk("G2 closure_cum_round == 12", row["closure_cum_round"] == 12,
        str(row["closure_cum_round"]))
    chk("G2 atring_rounds == 22, atring2 == 13",
        (row["atring_rounds"], row["atring2_rounds"]) == (22, 13),
        "%s/%s" % (row["atring_rounds"], row["atring2_rounds"]))
    chk("G2 seal_rate == 8/22*100 = 36.364", row["seal_rate"] == 36.364,
        str(row["seal_rate"]))
    chk("G2 channel split 3 body / 5 bldg",
        (row["sealed_by_body"], row["sealed_by_bldg"]) == (3, 5),
        "%s/%s" % (row["sealed_by_body"], row["sealed_by_bldg"]))

    # G3 -- MUTATION CONTROL --------------------------------------------------
    den3 = {r: [x for x in v if x[0] != S8[7]] for r, v in den.items()}
    row3 = fold(_mk(30, den3, bots), 8)
    chk("G3 mutation: dropping one seat lowers seats_sealed",
        row3["seats_sealed"] == 7, str(row3["seats_sealed"]))
    chk("G3 mutation: BOTH closure columns go to -1",
        (row3["closure_round"], row3["closure_cum_round"]) == (-1, -1),
        "%s/%s" % (row3["closure_round"], row3["closure_cum_round"]))
    chk("G3 mutation: the row MOVED (a seat-blind folder would not)",
        row3 != row)

    # G4 -- SIMULTANEITY CONTROL ---------------------------------------------
    den4 = {5 + i: [(s, "bldg")] for i, s in enumerate(S8)}   # one at a time
    row4 = fold(_mk(30, den4, bots), 8)
    chk("G4 all 8 sealed but never together -> closure_round -1",
        row4["closure_round"] == -1, str(row4["closure_round"]))
    chk("G4 ...and closure_cum_round == 12", row4["closure_cum_round"] == 12,
        str(row4["closure_cum_round"]))
    chk("G4 OTHER WAY: the G2 tape (held) DID report a closure",
        row["closure_round"] == 12)

    # G5 -- ZERO-PRESENCE CONTROL --------------------------------------------
    row5 = fold(_mk(30, den, {}), 8)
    chk("G5 no presence -> seal_rate is None, not 0",
        row5["seal_rate"] is None and row5["atring_rounds"] == 0,
        "rate=%s" % row5["seal_rate"])
    chk("G5 OTHER WAY: with presence the rate is a number",
        isinstance(row["seal_rate"], float))
    chk("G5 two_body_share is None at zero presence",
        row5["two_body_share"] is None)

    # G6 -- ENEMY-ONLY CONTROL, through the real denial alphabet --------------
    occ_enemy = {s: ("barrier", 1) for s in S8}
    occ_enemy[S8[0]] = ("builder_bot", 1)
    chk("G6 enemy-only occupancy denies 0 of 8 for us",
        len(denied_by(occ_enemy, S8, 0)) == 0)
    occ_ours = {s: ("barrier", 0) for s in S8}
    chk("G6 OTHER WAY: the same tiles held by US deny 8 of 8",
        len(denied_by(occ_ours, S8, 0)) == 8)
    occ_conv = {s: ("conveyor", 0) for s in S8}
    chk("G6 our CONVEYOR on a seat is NOT a denial (seattape 'o')",
        len(denied_by(occ_conv, S8, 0)) == 0)

    # G7 -- REAL-DATA TEAM-SWAP POSITIVE CONTROL ------------------------------
    rp = _pick_real()
    if rp is None:
        print("  [skip] G7: no map-tagged replay available")
    else:
        path, mapname, seat = rp
        a = analyse(path, mapname, seat)
        our = 0 if seat == "A" else 1
        b = analyse(path, mapname, seat, our_override=1 - our)
        moved = [k for k in ("seats_sealed", "atring_rounds", "seal_rate",
                             "closure_cum_round", "first_seal")
                 if a.get(k) != b.get(k)]
        chk("G7 team-swap MOVES the columns", len(moved) >= 2, str(moved))
        print("      as-played (team %d): sealed=%s atring=%s rate=%s closure_cum=%s"
              % (a["our_team"], a["seats_sealed"], a["atring_rounds"],
                 a["seal_rate"], a["closure_cum_round"]))
        print("      swapped   (team %d): sealed=%s atring=%s rate=%s closure_cum=%s"
              % (b["our_team"], b["seats_sealed"], b["atring_rounds"],
                 b["seal_rate"], b["closure_cum_round"]))

    print("=== seatrate selftest %s ===" % ("PASS" if ok else "FAIL"))
    return ok


def _pick_real():
    for d in (HERE / "grid", HERE / "smoke",
              HERE.parent / "s51_v519_build" / "grid"):
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.replay26")):
            tag = p.stem
            m = next((m for m in MAPS if tag.startswith(m)), None)
            s = tag.rsplit("_", 1)[-1]
            if m and s in ("A", "B"):
                return p, m, s
    return None


# =============================== DRIVERS =====================================

def run(grid_tsv, repdir, out_tsv, label=""):
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    out, fails = [], []
    for g in rows:
        p = Path(repdir) / (g["tag"] + ".replay26")
        if not p.exists():
            continue
        try:
            r = analyse(p, g["map"], g["seat"])
        except GuardFail as e:
            fails.append(str(e))
            continue
        out.append(dict(tag=g["tag"], map=g["map"], seed=g["seed"],
                        seat=g["seat"], ours=g["ours"], cond=g["cond"],
                        turn=g["turn"], arm=label, **r))
    if fails:
        sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails[:20]) + "\n")
        raise SystemExit(2)
    if not out:
        raise SystemExit("no replays matched %s" % repdir)
    cols = list(out[0].keys())
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for x in out:
            fh.write("\t".join("" if x[c] is None else str(x[c])
                               for c in cols) + "\n")
    sys.stderr.write("seatrate: %d games -> %s\n" % (len(out), out_tsv))
    return out


def report(paths):
    import statistics as st
    rows = []
    for p in paths:
        rows += list(csv.DictReader(open(p), delimiter="\t"))
    if not rows:
        raise SystemExit("no rows")
    by = {}
    for r in rows:
        by.setdefault(r.get("arm", ""), []).append(r)
    print("%-14s %5s %8s %9s %9s %9s %8s %9s" %
          ("arm", "n", "sealed", "rate", "closure", "clos_cum", "atring", "2body"))
    for arm, rr in sorted(by.items()):
        sealed = [int(r["seats_sealed"]) for r in rr]
        rate = [float(r["seal_rate"]) for r in rr if r["seal_rate"]]
        clo = [r for r in rr if int(r["closure_round"]) >= 0]
        cum = [r for r in rr if int(r["closure_cum_round"]) >= 0]
        atr = [int(r["atring_rounds"]) for r in rr]
        tb = [float(r["two_body_share"]) for r in rr if r["two_body_share"]]
        print("%-14s %5d %8.2f %9.2f %8.1f%% %8.1f%% %8.1f %9.3f" %
              (arm or "-", len(rr), st.mean(sealed),
               st.mean(rate) if rate else -1,
               100.0 * len(clo) / len(rr), 100.0 * len(cum) / len(rr),
               st.mean(atr), st.mean(tb) if tb else -1))
    print("\n  rate = seats sealed per 100 rounds of at-ring presence "
          "(>=1 of our builder bots within d^2<=50 of the enemy core, CENTRE "
          "convention).  closure = all legal seats denied SIMULTANEOUSLY; "
          "clos_cum = cumulative ever-denied set reaches all legal seats.")
    # the two-body vs one-body cut, off this same tape
    print("\n  TWO-BODY CUT (games split at median two_body_share):")
    for arm, rr in sorted(by.items()):
        vals = [(float(r["two_body_share"]), float(r["seal_rate"]))
                for r in rr if r["two_body_share"] and r["seal_rate"]]
        if len(vals) < 4:
            print("    %-12s n=%d -- too few games with presence" % (arm, len(vals)))
            continue
        med = st.median(v for v, _ in vals)
        lo = [s for v, s in vals if v <= med]
        hi = [s for v, s in vals if v > med]
        print("    %-12s median 2-body share %.3f | rate lo-half %.2f (n=%d) "
              "hi-half %.2f (n=%d)" %
              (arm, med, st.mean(lo) if lo else -1, len(lo),
               st.mean(hi) if hi else -1, len(hi)))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "--selftest":
        raise SystemExit(0 if selftest() else 1)
    elif a[0] == "--one":
        r = analyse(Path(a[1]), a[2], a[3])
        for k, v in r.items():
            print("%-20s %s" % (k, v))
    elif a[0] == "--report":
        report(a[1:])
    else:
        run(a[0], a[1], a[2], a[3] if len(a) > 3 else "")
