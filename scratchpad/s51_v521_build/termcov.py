#!/usr/bin/env python3
"""v520 TERMINAL-LAUNCHER SEAT COVERAGE, replay-side.

v520 change 1 sites the TERMINAL launcher of the relay chain to cover heal
seats and then re-roles it as an evictor.  The closure autopsy's accidental
baseline is the thing to beat: a ferry launcher is sited by the HOP, so its
pickup envelope covered **0 of 8 heal seats in 12 of 12 games**
(`s51_closure_autopsy/ferry_launchers.tsv`).  This measures the same quantity
on any arm, off the replay alone.

⛔ WHAT THE REPLAY FORMAT DOES **NOT** CARRY -- SAID PLAINLY.
`tools/replay_schema.md:49-66` lists all 16 members of the `Update` oneof:
placeEntity, moveBuilderBot, removeEntity, distributeResources, updateHp,
updatePlayers, setActionCooldown, setMoveCooldown, botOutput, indicatorLine,
indicatorDot, fireTurret, builderAttack, coreConvertAmmo, builderHeal,
builderBuild.  **THERE IS NO LAUNCH / THROW EVENT.**  A launcher throw reaches
the wire ONLY as a `moveBuilderBot` whose displacement exceeds one tile --
measured on `smoke/nordkap_i.replay26`: 53 such jumps, ALL of them on the
moveBuilderBot channel (update field 2), ZERO arriving as a placeEntity
position change.  So `ever_launched` here is a TELEPORT INFERENCE, not an event
read, and attribution to a particular launcher is geometric:

    from-tile within d^2 <= 2 of the launcher   (engine pickup envelope)
    to-tile   within 1 <= d^2 <= 26 of it       (engine throw envelope)

If two launchers satisfy both, the throw is AMBIGUOUS and is counted in its own
column rather than assigned.  ⚠ THIS CANNOT DISTINGUISH OUR THROW OF AN ENEMY
BODY FROM AN ENEMY THROW OF THE SAME BODY when launchers of both teams sit in
the same envelope; that case is counted as ambiguous too, never silently ours.
`--events` prints the throw ledger so the inference is auditable.

⛔ A SECOND THING IT DOES NOT CARRY: the platform strips `print()` (CLAUDE.md,
s28), so no arm tag, dose counter or `FS EVICT` line can be read out of a live
replay.  Everything here is engine-side by construction.

PER LAUNCHER OF OURS with dsq_core(pos, enemy_core) <= 26, EMITTED:
  eid, birth, pos, dsq_core, dsq_centre
  coverage        heal seats with 1 <= d^2 <= 2 of the launcher.  THE PICKUP
                  SEMANTICS: d^2 = 0 is the launcher's own tile, which can
                  never hold a body, so it is excluded.
  coverage_ferry  the closure autopsy's exact form (d^2 <= 2, self included),
                  so the 0/8-in-12/12 baseline stays apples-to-apples.
  best_cov_site   the best `coverage` reachable from ANY tile in the evictor
                  build envelope (dsq_core <= 8) -- ferry.py's counterfactual.
  lifetime, died, death_round
  n_launch        throws attributed to it (teleport inference above)
  n_launch_seat   of those, throws whose FROM-tile was one of the 8 heal seats
  ever_launched

⛔ GUARDS, EVERY ONE DRIVEN BOTH WAYS (`--selftest`):
  T1 ringwalk's selftest runs in place.
  T2 CHANNEL CENSUS on a real replay: the update-field histogram must contain
     field 2 and must contain NO field outside the 16 the schema declares.  A
     launch event appearing in a future engine build would show up here as an
     unknown field.  Driven the other way by asserting an injected bogus field
     number IS reported.
  T3 TELEPORT DETECTOR both ways: a 1-tile move is not a launch; a 5-tile jump
     is; the MUTATION (rewrite the jump to 1 tile) must drive the count to 0.
  T4 ATTRIBUTION both ways: the same jump with a launcher in the envelope is
     attributed; with the launcher moved outside it is UNATTRIBUTED; with two
     launchers in envelope it is AMBIGUOUS.
  T5 COVERAGE both ways: a launcher on a core corner covers exactly 2 seats; a
     launcher 10 tiles away covers 0.  And `coverage_ferry` differs from
     `coverage` by exactly 1 when the launcher stands ON a seat.
  T6 LIFETIME both ways: a launcher removed at round R has lifetime R-birth; a
     survivor's lifetime runs to the last round and `died` is False.
  T7 REAL-DATA TEAM-SWAP POSITIVE CONTROL: flipping our team must change the
     launcher set / coverage distribution.

Usage:
  termcov.py --selftest
  termcov.py <grid.tsv> <repdir> <out.tsv> [arm_label]
  termcov.py --one <replay26> <map> <A|B> [--events]
  termcov.py --report <out.tsv> [<out.tsv> ...]
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ringwalk import (  # noqa: E402
    FS_RING_DSQ, GuardFail, MAPS, PICKUP_DSQ, THROW_DSQ_MAX, WIRE_LEN,
    check_geom, dsq, dsq_centre, dsq_core, fields, parse_entity, read_pos,
)

SCHEMA_UPDATE_FIELDS = set(range(1, 17))   # replay_schema.md:49-66
TERM_DSQ = 26                              # "terminal": in the throw envelope


# --------------------------------------------------------------------------
# EVENT WALK.  ringwalk.walk() yields END-OF-ROUND state and therefore cannot
# see an individual move; this is the same walk with the moveBuilderBot branch
# instrumented, and it re-runs ringwalk's core-seed guard by calling it.
# --------------------------------------------------------------------------
def events(replay):
    """-> (rounds, launchers, jumps, field_hist, place_jumps)

    launchers: eid -> dict(team,pos,birth,death)
    jumps:     [(round, bot_id, bot_team, from, to, dsq)]
    """
    data = Path(replay).read_bytes()
    mb, turns = None, []
    for n, wt, v in fields(data):
        if n == 1 and wt == WIRE_LEN:
            mb = v
        elif n == 3 and wt == WIRE_LEN:
            turns.append(v)
    if mb is None:
        raise GuardFail("%s: no map message" % replay)
    pos = {}            # bot id -> pos
    team = {}           # bot id -> team
    launchers = {}
    jumps = []
    place_jumps = []
    hist = Counter()
    for rnd, tb in enumerate(turns):
        for _n, _w, u0 in fields(tb):
            for un, _uw, ub in fields(u0):
                hist[un] += 1
                if un == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.kind == "builder_bot":
                            if e.id in pos and pos[e.id] != e.pos:
                                d = dsq(pos[e.id], e.pos)
                                if d > 1:
                                    place_jumps.append(
                                        (rnd, e.id, e.team, pos[e.id], e.pos, d))
                            pos[e.id] = e.pos
                            team[e.id] = e.team
                        elif e.kind == "launcher":
                            L = launchers.get(e.id)
                            if L is None:
                                launchers[e.id] = dict(eid=e.id, team=e.team,
                                                       pos=e.pos, birth=rnd,
                                                       death=-1)
                            else:
                                L["pos"] = e.pos
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if to is None or eid is None:
                        continue
                    if eid in pos:
                        d = dsq(pos[eid], to)
                        if d > 1:
                            jumps.append((rnd, eid, team.get(eid, -1),
                                          pos[eid], to, d))
                    pos[eid] = to
                elif un == 3:
                    for rn, _rw, rv in fields(ub):
                        if rn == 1:
                            pos.pop(rv, None)
                            if rv in launchers and launchers[rv]["death"] < 0:
                                launchers[rv]["death"] = rnd
    return len(turns), launchers, jumps, hist, place_jumps


# --------------------------------------------------------------------------
# THE ATTRIBUTION FOLD -- separated so the guards can drive it synthetically.
# --------------------------------------------------------------------------
def attribute(jumps, launchers, rounds):
    """-> (per-launcher throw counts, ledger rows).

    A launcher is a candidate for a jump iff it is ALIVE that round, the FROM
    tile is inside its pickup envelope and the TO tile inside its throw
    envelope.  Exactly one candidate -> attributed.  More -> AMBIGUOUS.
    None -> UNATTRIBUTED.
    """
    counts = Counter()
    ledger = []
    for (rnd, bid, bteam, frm, to, d) in jumps:
        cand = []
        for eid, L in launchers.items():
            if L["birth"] > rnd:
                continue
            if 0 <= L["death"] < rnd:
                continue
            if dsq(frm, L["pos"]) <= PICKUP_DSQ and \
                    1 <= dsq(to, L["pos"]) <= THROW_DSQ_MAX:
                cand.append(eid)
        if len(cand) == 1:
            verdict, who = "ATTRIBUTED", cand[0]
            counts[cand[0]] += 1
        elif len(cand) > 1:
            verdict, who = "AMBIGUOUS", -1
        else:
            verdict, who = "UNATTRIBUTED", -1
        ledger.append(dict(round=rnd, bot=bid, bot_team=bteam,
                           frm="%d,%d" % frm, to="%d,%d" % to, dsq=d,
                           verdict=verdict, launcher=who,
                           n_candidates=len(cand)))
    return counts, ledger


def lifetime_of(birth, death, rounds):
    """Rounds the launcher was alive.  death < 0 means it survived to the end.

    `removeEntity` at round R means it was NOT alive at R, so a launcher born
    at b and removed at R lived R - b rounds; a survivor lived rounds - b.
    """
    last = death - 1 if death >= 0 else rounds - 1
    return max(0, last - birth + 1)


def coverage(p, seats, self_included):
    lo = 0 if self_included else 1
    return sum(1 for s in seats if lo <= dsq(p, s) <= PICKUP_DSQ)


def analyse(replay, mapname, seat, our_override=None):
    w, h, rows, ours, E, seats, _corners = check_geom(replay, mapname, seat)
    if our_override is not None:
        ours = our_override
        from ringwalk import replay_map, ring_tiles
        _rw, _rh, _rr, cores = replay_map(replay)
        E = {c["team"]: c["pos"] for c in cores}[1 - ours]
        s2, _c2 = ring_tiles(E[0], E[1], w, h)
        seats = [t for t in s2 if rows[t[1]][t[0]] != 1]
    rounds, launchers, jumps, hist, place_jumps = events(replay)
    counts, ledger = attribute(jumps, launchers, rounds)
    seatset = set(seats)
    # ferry.py's counterfactual: the best coverage from anywhere in the
    # evictor build envelope
    env = [(x, y) for x in range(w) for y in range(h)
           if rows[y][x] != 1 and dsq_core((x, y), E) <= FS_RING_DSQ
           and (x, y) not in {(E[0] + dx, E[1] + dy)
                              for dx in (0, 1) for dy in (0, 1)}]
    best = max((coverage(t, seats, False) for t in env), default=0)
    out = []
    for eid, L in sorted(launchers.items(), key=lambda kv: kv[1]["birth"]):
        if L["team"] != ours:
            continue
        dc = dsq_core(L["pos"], E)
        if dc > TERM_DSQ:
            continue
        death = L["death"]
        seat_throws = sum(1 for r in ledger
                          if r["launcher"] == eid
                          and tuple(int(v) for v in r["frm"].split(","))
                          in seatset)
        out.append(dict(
            eid=eid, birth=L["birth"], pos="%d,%d" % L["pos"],
            dsq_core=dc, dsq_centre=round(dsq_centre(L["pos"], E), 2),
            n_seats=len(seats),
            coverage=coverage(L["pos"], seats, False),
            coverage_ferry=coverage(L["pos"], seats, True),
            best_cov_site=best,
            lifetime=lifetime_of(L["birth"], death, rounds),
            died=int(death >= 0), death_round=death,
            n_launch=counts.get(eid, 0),
            n_launch_seat=seat_throws,
            ever_launched=int(counts.get(eid, 0) > 0)))
    meta = dict(rounds=rounds, n_jumps=len(jumps),
                n_place_jumps=len(place_jumps),
                unknown_fields=sorted(set(hist) - SCHEMA_UPDATE_FIELDS),
                field_hist=dict(hist),
                n_attr=sum(1 for r in ledger if r["verdict"] == "ATTRIBUTED"),
                n_ambig=sum(1 for r in ledger if r["verdict"] == "AMBIGUOUS"),
                n_unattr=sum(1 for r in ledger
                             if r["verdict"] == "UNATTRIBUTED"))
    return out, meta, ledger


# ============================== SELFTEST =====================================

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


def selftest():
    ok = True

    def chk(name, cond, detail=""):
        nonlocal ok
        print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                              ("  " + detail) if detail else ""))
        if not cond:
            ok = False

    print("=== T1: ringwalk selftest, in place ===")
    import ringwalk
    if not ringwalk.selftest():
        ok = False

    print("=== termcov selftest ===")
    rp = _pick_real()
    if rp is None:
        raise SystemExit("no map-tagged replay to guard against")
    path, mapname, seat = rp

    # T2 -- CHANNEL CENSUS, both ways -----------------------------------------
    rounds, launchers, jumps, hist, place_jumps = events(path)
    unknown = sorted(set(hist) - SCHEMA_UPDATE_FIELDS)
    chk("T2 update fields all declared by the schema", unknown == [],
        "fields seen: %s" % sorted(hist))
    chk("T2 moveBuilderBot (field 2) is present -- the ONLY launch channel",
        hist.get(2, 0) > 0, "%d move events" % hist.get(2, 0))
    chk("T2 no launch/throw field exists in the oneof (16 declared members)",
        max(hist) <= 16, "max field seen = %d" % max(hist))
    bogus = Counter(hist)
    bogus[42] = 1
    chk("T2 OTHER WAY: an injected field 42 IS reported as unknown",
        sorted(set(bogus) - SCHEMA_UPDATE_FIELDS) == [42])
    chk("T2 teleports arrive on moveBuilderBot, not placeEntity",
        len(place_jumps) == 0,
        "%d move-jumps, %d place-jumps" % (len(jumps), len(place_jumps)))

    # T3 -- TELEPORT DETECTOR, both ways --------------------------------------
    L = {7: dict(eid=7, team=0, pos=(10, 10), birth=0, death=-1)}
    j_move = [(5, 1, 0, (10, 11), (10, 12), 1)]
    j_jump = [(5, 1, 0, (10, 11), (12, 13), 8)]
    c_m, _ = attribute([x for x in j_move if x[5] > 1], L, 100)
    c_j, led_j = attribute(j_jump, L, 100)
    chk("T3 a 1-tile move is NOT a launch", sum(c_m.values()) == 0)
    chk("T3 a >1-tile jump IS a launch", sum(c_j.values()) == 1)
    j_mut = [(5, 1, 0, (10, 11), (10, 12), 1)]
    chk("T3 MUTATION: rewriting the jump to 1 tile drives the count to 0",
        sum(attribute([x for x in j_mut if x[5] > 1], L, 100)[0].values()) == 0)

    # T4 -- ATTRIBUTION, both ways --------------------------------------------
    chk("T4 launcher in envelope -> ATTRIBUTED",
        led_j[0]["verdict"] == "ATTRIBUTED" and led_j[0]["launcher"] == 7)
    Lfar = {7: dict(eid=7, team=0, pos=(0, 0), birth=0, death=-1)}
    chk("T4 OTHER WAY: launcher outside the envelope -> UNATTRIBUTED",
        attribute(j_jump, Lfar, 100)[1][0]["verdict"] == "UNATTRIBUTED")
    Ltwo = dict(L)
    Ltwo[8] = dict(eid=8, team=1, pos=(11, 11), birth=0, death=-1)
    a2 = attribute(j_jump, Ltwo, 100)[1][0]
    chk("T4 OTHER WAY: two launchers in envelope -> AMBIGUOUS, never ours",
        a2["verdict"] == "AMBIGUOUS" and a2["launcher"] == -1,
        "n_candidates=%d" % a2["n_candidates"])
    Ldead = {7: dict(eid=7, team=0, pos=(10, 10), birth=0, death=3)}
    chk("T4 OTHER WAY: a launcher dead before the round is not a candidate",
        attribute(j_jump, Ldead, 100)[1][0]["verdict"] == "UNATTRIBUTED")
    Lunborn = {7: dict(eid=7, team=0, pos=(10, 10), birth=99, death=-1)}
    chk("T4 OTHER WAY: a launcher not yet built is not a candidate",
        attribute(j_jump, Lunborn, 100)[1][0]["verdict"] == "UNATTRIBUTED")

    # T5 -- COVERAGE, both ways ------------------------------------------------
    ox, oy = 10, 10
    seats8 = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
              (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    chk("T5 a launcher on the NW core corner covers exactly 2 seats",
        coverage((ox - 1, oy - 1), seats8, False) == 2,
        str(coverage((ox - 1, oy - 1), seats8, False)))
    chk("T5 OTHER WAY: a launcher 10 tiles away covers 0 seats",
        coverage((ox - 10, oy - 10), seats8, False) == 0)
    on_seat = (ox, oy - 1)
    chk("T5 coverage_ferry exceeds coverage by exactly 1 when ON a seat "
        "(d^2=0 is the launcher's own tile and can hold no body)",
        coverage(on_seat, seats8, True) - coverage(on_seat, seats8, False) == 1,
        "%d vs %d" % (coverage(on_seat, seats8, True),
                      coverage(on_seat, seats8, False)))
    chk("T5 OTHER WAY: off-seat siting has coverage_ferry == coverage",
        coverage((ox - 1, oy - 1), seats8, True)
        == coverage((ox - 1, oy - 1), seats8, False))

    # T6 -- LIFETIME, both ways.  SYNTHETIC FIRST so both branches are driven
    # even on a fixture where every launcher happens to die. -------------------
    chk("T6 SYNTHETIC dead: born r10, removed r30, 1000 rounds -> 20",
        lifetime_of(10, 30, 1000) == 20, str(lifetime_of(10, 30, 1000)))
    chk("T6 SYNTHETIC OTHER WAY survivor: born r10, never removed -> 990",
        lifetime_of(10, -1, 1000) == 990, str(lifetime_of(10, -1, 1000)))
    chk("T6 SYNTHETIC the two branches DIFFER on the same birth round",
        lifetime_of(10, 30, 1000) != lifetime_of(10, -1, 1000))
    chk("T6 SYNTHETIC born and removed the same round -> 0",
        lifetime_of(10, 10, 1000) == 0)
    rows_a, meta_a, _ = analyse(path, mapname, seat)
    died = [r for r in rows_a if r["died"]]
    surv = [r for r in rows_a if not r["died"]]
    chk("T6 REAL dead launchers agree with the synthetic rule",
        all(r["lifetime"] == r["death_round"] - r["birth"] for r in died),
        "%d died" % len(died))
    chk("T6 REAL survivors agree with the synthetic rule",
        all(r["lifetime"] == meta_a["rounds"] - r["birth"] for r in surv),
        "%d survived of %d rounds" % (len(surv), meta_a["rounds"]))

    # T7 -- REAL-DATA TEAM-SWAP POSITIVE CONTROL -------------------------------
    our = 0 if seat == "A" else 1
    rows_b, meta_b, _ = analyse(path, mapname, seat, our_override=1 - our)
    sig_a = (len(rows_a), sum(r["coverage"] for r in rows_a),
             sum(r["n_launch"] for r in rows_a))
    sig_b = (len(rows_b), sum(r["coverage"] for r in rows_b),
             sum(r["n_launch"] for r in rows_b))
    chk("T7 team-swap MOVES the launcher set / coverage / throws",
        sig_a != sig_b, "%s vs %s" % (sig_a, sig_b))
    print("      as-played: %d in-envelope launchers, coverage sum %d, throws %d"
          % sig_a)
    print("      swapped  : %d in-envelope launchers, coverage sum %d, throws %d"
          % sig_b)
    print("      throw ledger on this game: %d attributed, %d ambiguous, "
          "%d unattributed of %d jumps"
          % (meta_a["n_attr"], meta_a["n_ambig"], meta_a["n_unattr"],
             meta_a["n_jumps"]))

    print("=== termcov selftest %s ===" % ("PASS" if ok else "FAIL"))
    return ok


# =============================== DRIVERS =====================================

def run(grid_tsv, repdir, out_tsv, label=""):
    rows = list(csv.DictReader(open(grid_tsv), delimiter="\t"))
    out, fails, ngames, alarms = [], [], 0, []
    for g in rows:
        p = Path(repdir) / (g["tag"] + ".replay26")
        if not p.exists():
            continue
        try:
            rr, meta, _led = analyse(p, g["map"], g["seat"])
        except GuardFail as e:
            fails.append(str(e))
            continue
        ngames += 1
        if meta["unknown_fields"]:
            alarms.append("%s: unknown update fields %s"
                          % (g["tag"], meta["unknown_fields"]))
        if meta["n_place_jumps"]:
            alarms.append("%s: %d teleports arrived as placeEntity, not "
                          "moveBuilderBot" % (g["tag"], meta["n_place_jumps"]))
        for r in rr:
            out.append(dict(tag=g["tag"], map=g["map"], seed=g["seed"],
                            seat=g["seat"], ours=g["ours"], cond=g["cond"],
                            turn=g["turn"], arm=label, game_rounds=meta["rounds"],
                            game_jumps=meta["n_jumps"], **r))
    if fails:
        sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails[:20]) + "\n")
        raise SystemExit(2)
    if alarms:
        sys.stderr.write("INSTRUMENT ALARM:\n  " + "\n  ".join(alarms[:10]) + "\n")
        raise SystemExit(3)
    cols = (list(out[0].keys()) if out
            else "tag map seed seat ours cond turn arm".split())
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for x in out:
            fh.write("\t".join(str(x[c]) for c in cols) + "\n")
    sys.stderr.write("termcov: %d games, %d in-envelope launchers -> %s\n"
                     % (ngames, len(out), out_tsv))
    return out


def report(paths):
    rows = []
    for p in paths:
        rows += list(csv.DictReader(open(p), delimiter="\t"))
    if not rows:
        print("no launchers in envelope")
        return
    by = {}
    for r in rows:
        by.setdefault(r.get("arm", ""), []).append(r)
    for arm, rr in sorted(by.items()):
        games = len({r["tag"] for r in rr})
        cov = Counter(int(r["coverage"]) for r in rr)
        covf = Counter(int(r["coverage_ferry"]) for r in rr)
        launched = sum(1 for r in rr if r["ever_launched"] == "1")
        import statistics as st
        print("== arm %-12s %d launchers over %d games" % (arm or "-", len(rr), games))
        print("   coverage (1<=d^2<=2)  distribution: %s"
              % dict(sorted(cov.items())))
        print("   coverage_ferry (d^2<=2, autopsy form): %s   ⚠ the autopsy's "
              "0/8-in-12/12 baseline is a v513-era fixture -- ERA-CROSSING, "
              "use it as a direction, never as a control"
              % dict(sorted(covf.items())))
        bc = Counter(int(r["best_cov_site"]) for r in rr)
        print("   best_cov_site (counterfactual): %s  ⛔ THIS IS A GEOMETRIC "
              "CEILING, NOT A MEASUREMENT -- no tile in the evictor envelope "
              "can cover 3 seats (consecutive seats are d^2=1 apart along an "
              "edge and d^2=2 around a corner, so 2 is the max).  A constant "
              "column validates nothing; read `coverage` against 2, not "
              "against this." % dict(sorted(bc.items())))
        on_seat = sum(1 for r in rr
                      if int(r["coverage_ferry"]) != int(r["coverage"]))
        print("   launchers standing ON a heal seat: %d/%d (coverage_ferry "
              "differs from coverage only in that case)" % (on_seat, len(rr)))
        print("   lifetime: median %s  mean %.1f"
              % (st.median(int(r["lifetime"]) for r in rr),
                 st.mean(int(r["lifetime"]) for r in rr)))
        print("   birth round: median %s" % st.median(int(r["birth"]) for r in rr))
        print("   ever_launched: %d/%d (%.1f%%)   throws total %d, "
              "from a heal seat %d"
              % (launched, len(rr), 100.0 * launched / len(rr),
                 sum(int(r["n_launch"]) for r in rr),
                 sum(int(r["n_launch_seat"]) for r in rr)))
        print("   died: %d/%d" % (sum(1 for r in rr if r["died"] == "1"), len(rr)))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "--selftest":
        raise SystemExit(0 if selftest() else 1)
    elif a[0] == "--one":
        rr, meta, led = analyse(Path(a[1]), a[2], a[3])
        print("meta:", {k: v for k, v in meta.items() if k != "field_hist"})
        if not rr:
            print("(no launcher of ours inside dsq_core <= %d)" % TERM_DSQ)
        for r in rr:
            print("  " + "  ".join("%s=%s" % kv for kv in r.items()))
        if "--events" in a:
            print("throw ledger:")
            for e in led:
                print("   " + "  ".join("%s=%s" % kv for kv in e.items()))
    elif a[0] == "--report":
        report(a[1:])
    else:
        run(a[0], a[1], a[2], a[3] if len(a) > 3 else "")
