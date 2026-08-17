#!/usr/bin/env python3
"""LOKI-SEALPIERCE demo instrument: SHOT-LEVEL attribution for seat Sentinels.

Reads a LOCAL .replay26 and answers, per shot fired by one of OUR Sentinels
that is seated on the enemy Core's ring (dsq_core <= BAND):

    round · from · to · victim kind/team · THROUGH-CORE? · hp delta on the
    victim · hp delta on the enemy CORE in the same round

and then rolls that up into the four rungs the plank claims:

    MOUTH  enemy belt orthogonally adjacent to their Core footprint
    APRON  enemy belt within BELT_DSQ of their Core
    HEALER enemy builder bot orthogonally adjacent to their Core
    CORE   their Core (the default rung)
    OTHER  anything else

⛔ THE JITTER CONTROL, because "the belt died and we had shot at it" is not
attribution.  Every shot is scored against a JITTERED source: the same shot
list, but each `to` displaced by a fixed (+1,0) offset.  A metric that counts
the same number of MOUTH hits under jitter is not reading the geometry it
claims to read -- it is counting shots.  The jitter row must come out LOWER.

THROUGH-CORE is computed from the ray itself: the target is strictly farther
from the shooter than some enemy Core tile lying on the open segment between
them (same row/column/diagonal, monotone).  That is the engine-side fact the
whole plank rests on, so it is measured per shot rather than assumed.

Usage:
    .venv/bin/python scratchpad/sp_shots.py REPLAY --team A|B [--band 2]
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import replay_census as RC  # noqa: E402

BELT = {"conveyor", "splitter"}
# Wire enum for Direction is 1-INDEXED (0 is unspecified/absent).  Confirmed
# twice on `bots/_probe_pierce`'s replay, where the Sentinel built facing EAST
# decodes as 3 and the conveyor built facing WEST decodes as 7.
DELTAS = {1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
          5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
SENTINEL_RSQ = 32


def dsq_core(pos, foot):
    return min((pos[0] - c[0]) ** 2 + (pos[1] - c[1]) ** 2 for c in foot)


def between(frm, to, foot):
    """Enemy Core tiles on the OPEN segment frm->to (8-way ray), or []."""
    dx, dy = to[0] - frm[0], to[1] - frm[1]
    n = max(abs(dx), abs(dy))
    if n == 0:
        return []
    if dx % n or dy % n:          # not a clean 8-way ray
        return []
    sx, sy = dx // n, dy // n
    out = []
    for k in range(1, n):
        q = (frm[0] + sx * k, frm[1] + sy * k)
        if q in foot:
            out.append(q)
    return out


def far_tiles(pos, dirint, foot, w, h):
    """The ray tiles BEYOND the enemy Core, i.e. what the pierce buys.

    Same definition the bot uses (`_pierce_site_term`): walk the facing ray out
    to r^2=32, find the farthest enemy Core tile on it, keep everything past
    that.  Empty when no Core tile is on the ray at all.
    """
    d = DELTAS.get(dirint)
    if d is None:
        return []
    ray = []
    for k in range(1, 7):
        q = (pos[0] + d[0] * k, pos[1] + d[1] * k)
        if not (0 <= q[0] < w and 0 <= q[1] < h):
            break
        if (q[0] - pos[0]) ** 2 + (q[1] - pos[1]) ** 2 > SENTINEL_RSQ:
            break
        ray.append(q)
    last = -1
    for i, q in enumerate(ray):
        if q in foot:
            last = i
    return [] if last < 0 else ray[last + 1:]


def rung(kind, team, pos, our, foot, belt_dsq):
    if team == our:
        return "OTHER"
    if kind in BELT:
        d = dsq_core(pos, foot)
        if d <= 1:
            return "MOUTH"
        if d <= belt_dsq:
            return "APRON"
        return "OTHER"
    if kind == "builder_bot" and dsq_core(pos, foot) <= 1:
        return "HEALER"
    if kind == "core":
        return "CORE"
    return "OTHER"


def analyse(path: Path, our: int, band: int, belt_dsq: int, jitter=(0, 0)):
    data = path.read_bytes()
    tbs = [v for n, w, v in RC.fields(data) if n == 3 and w == RC.WIRE_LEN]
    rep = RC.Replay(path, track_flow=False)
    foot = rep.core_footprint(1 - our)
    our_foot = rep.core_footprint(our)

    ent = {}          # id -> [team, kind, pos]
    # ⛔ TWO POSITION MAPS, NOT ONE, AND THIS WAS A REAL SUPPRESSION BUG.  A
    # builder bot WALKS OVER buildings, so a single pos->id map is clobbered by
    # any bot that steps onto a belt and then UNMAPPED when it steps off.
    # Measured on the antler demo: an enemy conveyor on their core mouth at
    # (7,14) was killed by our seat Sentinel in two shots (hp -18, -18, then
    # RemoveEntity) and the one-map decoder scored BOTH shots "empty" -- it
    # deleted exactly the evidence the plank exists to produce.  Resolution
    # order mirrors the bot's own ladder: building first, then bot.
    pos2bld = {}
    pos2bot = {}

    def _pos(q):
        return pos2bld.get(q, pos2bot.get(q))
    # ⛔ CORES ARE NOT PlaceEntity EVENTS -- they arrive in the MAP message, and
    # the first turn's updates start at the first spawned builder (id 3).  A
    # decoder that only reads PlaceEntity therefore has no Core in it at all,
    # and every Core shot scores "empty": measured here as 17 of 17 seat shots
    # vanishing before this was seeded.  Their footprint is 2x2 and the map
    # carries only the NW corner, so all four tiles are mapped.
    for c in rep.cores:
        x, y = c["pos"]
        ent[c["id"]] = [c["team"], "core", (x, y)]
        for q in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
            pos2bld[q] = c["id"]
    seat = {}         # id -> pos, our Sentinels seated on their ring
    shots = []
    hp_by_round = []
    kills = defaultdict(int)
    belt_deaths_hit = 0
    rebuild_tiles = defaultdict(int)   # tile -> enemy belts built there
    rekilled_tiles = set()
    hit_tiles = set()
    last_hit_round = {}
    tled = 0
    opp = defaultdict(int)
    live_seat_rounds = defaultdict(int)

    for rnd, tb in enumerate(tbs):
        hp = defaultdict(int)
        shot0 = len(shots)
        for _n, _w, upd in RC.fields(tb):
            for un, _uw, ub in RC.fields(upd):
                if un == 1:                                   # placeEntity
                    for en, _ew, eb in RC.fields(ub):
                        if en != 1:
                            continue
                        e = RC.parse_entity(eb, rnd)
                        if e is None or e.pos is None:
                            continue
                        ent[e.id] = [e.team, e.kind, e.pos]
                        if e.kind == "builder_bot":
                            pos2bot[e.pos] = e.id
                        else:
                            pos2bld[e.pos] = e.id
                        if e.kind == "core":
                            # ⛔ A Core is 2x2 and PlaceEntity carries only its
                            # NW corner.  Without this, every shot aimed at one
                            # of the other three tiles resolved to "empty" --
                            # which is the CORE rung, i.e. the default the
                            # plank is measured against, silently zeroed.
                            x, y = e.pos
                            for q in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
                                pos2bld[q] = e.id
                        if e.team != our and e.kind in BELT:
                            rebuild_tiles[e.pos] += 1
                        if (e.team == our and e.kind == "sentinel"
                                and dsq_core(e.pos, foot) <= band):
                            seat[e.id] = (e.pos, e.direction)
                elif un == 2:                                 # move
                    eid = to = None
                    for mn, _mw, mv in RC.fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = RC.read_pos(mv)
                    if eid in ent and to is not None:
                        old = ent[eid][2]
                        if pos2bot.get(old) == eid:
                            pos2bot.pop(old, None)
                        ent[eid][2] = to
                        pos2bot[to] = eid
                elif un == 3:                                 # remove
                    for rn, _rw, rv in RC.fields(ub):
                        if rn != 1:
                            continue
                        info = ent.pop(rv, None)
                        if info:
                            if pos2bot.get(info[2]) == rv:
                                pos2bot.pop(info[2], None)
                            if pos2bld.get(info[2]) == rv:
                                pos2bld.pop(info[2], None)
                            if info[0] != our and info[1] in BELT:
                                kills["enemy_belt_removed"] += 1
                                if rnd - last_hit_round.get(info[2], -99) <= 1:
                                    kills["belt_killed_by_seat"] += 1
                                    belt_deaths_hit += 1
                                    if rebuild_tiles.get(info[2], 0) > 1:
                                        rekilled_tiles.add(info[2])
                            if info[0] != our and info[1] == "builder_bot" \
                                    and rnd - last_hit_round.get(info[2], -99) <= 1:
                                kills["healer_killed_by_seat"] += 1
                elif un == 5:                                 # updateHp
                    sc = RC.scalars(ub)
                    if 1 in sc:
                        hp[sc[1]] += _signed(sc.get(2, 0))
                elif un == 9:                                 # botOutput
                    sc = RC.scalars(ub)
                    if sc.get(4):
                        tled += 1
                elif un == 12:                                # fireTurret
                    # ⛔ RESOLVED INLINE, NOT DEFERRED TO THE END OF THE ROUND.
                    # A killing shot is followed IN THE SAME ROUND by the
                    # victim's RemoveEntity, so a pass that resolves fires
                    # after the round has already forgotten the victim: the
                    # first cut scored every KILLING shot as "empty" -- i.e.
                    # it dropped exactly the shots the plank is about.
                    frm = to = None
                    for fn, _fw, fv in RC.fields(ub):
                        if fn == 1:
                            frm = RC.read_pos(fv)
                        elif fn == 2:
                            to = RC.read_pos(fv)
                    if frm is None or to is None:
                        continue
                    sid = _pos(frm)
                    if sid not in seat:
                        continue
                    tgt = (to[0] + jitter[0], to[1] + jitter[1])
                    vid = _pos(tgt)
                    if vid is None or vid not in ent:
                        shots.append([rnd, frm, tgt, "empty", -1, False, "empty", None])
                        continue
                    vteam, vkind, vpos = ent[vid]
                    shots.append([rnd, frm, tgt, vkind, vteam,
                                  bool(between(frm, tgt, foot)),
                                  rung(vkind, vteam, vpos, our, foot, belt_dsq),
                                  vid])
                    if vteam != our and vkind in (BELT | {"builder_bot"}):
                        last_hit_round[vpos] = rnd
                        hit_tiles.add(vpos)
        hp_by_round.append(hp)
        for s in shots[shot0:]:           # attach this round's net hp delta
            s[7] = hp.get(s[7], 0) if isinstance(s[7], int) else 0

        # OPPORTUNITY CENSUS.  The ladder can only bite when something of
        # theirs is standing on the far side of their own Core; with an empty
        # far side the plank is inert BY DESIGN and the replay is identical to
        # the parent's.  So count the rounds where the opportunity EXISTED,
        # separately from the shots that took it -- otherwise a zero cannot be
        # told apart from a plank that does not work.
        for sid, (spos, sdir) in seat.items():
            if sid not in ent:
                continue
            live_seat_rounds[sid] += 1
            # COUNTERFACTUAL: would ANY legal facing from this same seat have
            # had a belt behind their Core this round?  Without it, a low
            # opportunity count cannot be told apart from a bad facing choice
            # -- and the facing IS one of the things this plank changes.
            for alt in DELTAS:
                hit = False
                for q in far_tiles(spos, alt, foot, rep.width, rep.height):
                    vid = _pos(q)
                    if vid is not None and vid in ent and ent[vid][0] != our \
                            and ent[vid][1] in BELT:
                        hit = True
                        break
                if hit:
                    opp["far_belt_rounds_bestfacing"] += 1
                    break
            for q in far_tiles(spos, sdir, foot, rep.width, rep.height):
                vid = _pos(q)
                if vid is None or vid not in ent or ent[vid][0] == our:
                    continue
                if ent[vid][1] in BELT:
                    opp["far_belt_rounds"] += 1
                    if dsq_core(q, foot) <= 1:
                        opp["far_mouth_belt_rounds"] += 1
                    break
                if ent[vid][1] == "builder_bot" and dsq_core(q, foot) <= 1:
                    opp["far_healer_rounds"] += 1
                    break

    return dict(rep=rep, foot=foot, our_foot=our_foot, seat=seat, shots=shots,
                opp=opp, live_seat_rounds=live_seat_rounds,
                kills=kills, hp=hp_by_round, tled=tled,
                rekilled=rekilled_tiles, rebuilds=rebuild_tiles,
                hit_tiles=hit_tiles)


def _signed(v):
    """UpdateHp.delta is a plain int32; negative values arrive as a 10-byte
    two's-complement varint, which `fields` already returns as a huge positive.
    """
    if v > (1 << 31):
        return v - (1 << 64)
    return v


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("replay")
    ap.add_argument("--team", choices=["A", "B"], required=True)
    ap.add_argument("--band", type=int, default=2)
    ap.add_argument("--belt-dsq", type=int, default=8)
    ap.add_argument("--shots", type=int, default=20, help="shot lines to print")
    args = ap.parse_args()

    our = 0 if args.team == "A" else 1
    r = analyse(Path(args.replay), our, args.band, args.belt_dsq)
    j = analyse(Path(args.replay), our, args.band, args.belt_dsq, jitter=(1, 0))

    rep = r["rep"]
    print("replay      %s  %dx%d  rounds=%d  winner=%s cond=%s"
          % (args.replay, rep.width, rep.height, rep.rounds,
             "AB"[rep.winner] if rep.winner is not None else "?", rep.win_condition))
    print("our team    %s   their core footprint %s" % (args.team, sorted(r["foot"])))
    print("seat Sentinels (dsq_core <= %d): %s" % (args.band, r["seat"]))
    print("tled bot-turns in replay: %d" % r["tled"])

    tot = defaultdict(int)
    for (_rnd, _f, _t, _k, _tm, crossed, rg, _hp) in r["shots"]:
        tot[rg] += 1
        if crossed:
            tot["THROUGH_CORE"] += 1
    jt = defaultdict(int)
    for (_rnd, _f, _t, _k, _tm, crossed, rg, _hp) in j["shots"]:
        jt[rg] += 1

    print("\nSEAT-SENTINEL SHOTS  n=%d" % len(r["shots"]))
    for k in ("MOUTH", "APRON", "HEALER", "CORE", "OTHER", "empty", "THROUGH_CORE"):
        print("   %-13s %4d      jitter(+1,0): %4d" % (k, tot[k], jt[k]))
    print("   CONTROL: jitter MUST be lower on MOUTH+APRON -> %s"
          % ("PASS" if (jt["MOUTH"] + jt["APRON"]) < (tot["MOUTH"] + tot["APRON"])
             else "FAIL/none-fired"))

    print("\nOPPORTUNITY (rounds a seat Sentinel was alive with something of "
          "theirs on the FAR side of their own Core)")
    print("   live seat-Sentinel rounds   %d" % sum(r["live_seat_rounds"].values()))
    for k in ("far_belt_rounds", "far_belt_rounds_bestfacing",
              "far_mouth_belt_rounds", "far_healer_rounds"):
        print("   %-26s %d" % (k, r["opp"][k]))

    print("\nKILL LEDGER")
    for k in sorted(r["kills"]):
        print("   %-24s %d" % (k, r["kills"][k]))
    print("   belt tiles REBUILT by them after a seat kill: %d %s"
          % (len(r["rekilled"]), sorted(r["rekilled"])))

    print("\nFIRST %d SEAT SHOTS  (hp_delta is the victim's NET hp change that "
          "round -- confounded by their own heals/our pecks, diagnostic only)"
          % args.shots)
    for s in r["shots"][:args.shots]:
        rnd, frm, to, kind, tm, crossed, rg, dhp = s
        print("   r=%-4d %s -> %s  %-11s team=%s  through=%-5s  rung=%-6s hp_delta=%s"
              % (rnd, frm, to, kind, tm, crossed, rg, dhp))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
