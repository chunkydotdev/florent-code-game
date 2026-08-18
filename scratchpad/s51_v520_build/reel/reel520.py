#!/usr/bin/env python3
"""v520 FAILURE REEL: board facts for the six earliest our-core deaths of the
v520 arm, one per map.

⛔ COPIED MACHINERY, GUARDS RUN IN PLACE.  `turrets.py` (fireTurret channel),
`tape.py` (per-round board) and `crip.py` (UpdateHp ledger) are byte-identical
copies of the s51 v519-build instruments (md5 verified 2026-08-18: tape.py
4a92277e5fdb2901a7d7509ad2dbee45, turrets.py 8b895711245b80e5f0d816b2904f1962,
crip.py 89f7bd3e7db362d1d9a4686e528f9709); this file only joins them and prints,
exactly as `scratchpad/s51_v519_build/reel/reel519.py` did.  The two channel
guards it re-runs per game:
  * HP IDENTITY: 500 + sum(UpdateHp deltas on our core) must land in (-18, 0]
    for a destroyed core (damage is not clamped, so the killing blow overshoots
    by at most one sentinel hit).
  * CHANNEL AGREEMENT: our sentinels' fireTurret core hits must equal the count
    of -18 UpdateHp deltas on THEIR core, both directions, every game.

⭐ NEW FOR v520 -- three pincer-specific board facts, all engine-side, computed
with `seatrate.py` / `termcov.py` (the v520 instruments, imported and CALLED,
not re-implemented; both carry their own driven-both-ways selftests):
  * TWO-BODY PRESENCE: rounds with >=1 and with >=2 of OUR builder bots inside
    d^2 <= 50 of the enemy core (seatrate.ATRING_DSQ, CENTRE convention), plus
    the MAX simultaneous count -- folded here from seatrate.tape_for's own
    per-round tape, because seatrate.fold reports the >=1/>=2 shares only.
  * HEAL-SEAT DENIAL: how many of the enemy core's 8 orthogonal heal seats we
    ever denied (our building on the tile, or our builder body standing on it
    -- seattape's D|d alphabet), the round the LAST of those seats was first
    denied, and both closure columns.  n_seats is REPORTED, not assumed: a wall
    or a border can make it fewer than 8.
  * TERMINAL-LAUNCHER COVERAGE: whether a launcher of ours ever stood within
    1 <= d^2 <= 2 of a heal seat (the engine pickup envelope, own tile excluded
    because a body cannot stand there), and the number of rounds the union of
    such launchers was alive.

⛔ EVERYTHING BELOW IS ENGINE-SIDE.  The headline arms run every log flag False
and platform replays carry no stdout at all (CLAUDE.md, s28).

⭐ SELECTION RULE -- A CHOICE, NOT A DISCOVERY.  The EARLIEST our-core-death in
EACH of the six maps, for the `v520` arm of the headline grid
(`scratchpad/s51_v520_build/grid/b*/v520.tsv`), so the reel is not six copies of
one board.  "Our core died" = row with ours == "OPP" and cond starting
"Core destroyed"; "earliest" = lowest `turn`.  Ties break lowest block, then
lowest seed, then seat A.  Selected from 315 our-core-deaths in 972 v520 rows
across 27 blocks; NO tie occurred on any of the six maps.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
import seatrate  # noqa: E402
import termcov  # noqa: E402
import turrets  # noqa: E402
from crip import analyse, summarise  # noqa: E402
from tape import Tape  # noqa: E402
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_update_hp,
)


def heal_rounds(path, our_team):
    """Rounds in which the ENEMY core took a +1..+4 UpdateHp delta.

    ⚠ NOT copied machinery -- the only new code in this file.  It is the same
    wire walk crip.py does, kept per-round instead of summed, so the seal can
    be crossed against the heal.  GUARDED against crip.py's independent
    summation below: the HP it totals must equal `oppcore_heal` exactly.
    """
    data = path.read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"id": 0, "team": 0}
            for cn, _cw, cv in fields(v):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
            cores.append(c)
    opp_core = {c["team"]: c["id"] for c in cores}[1 - our_team]
    rounds, total = [], 0
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 5:
                    eid, d = parse_update_hp(ubuf)
                    if eid == opp_core and 1 <= d <= 4:
                        rounds.append(rnd)
                        total += d
    return sorted(set(rounds)), total

# tag, map, seat, turn (our core's death round, from the grid tsv), source block
GAMES = [
    ("nordkap_s72_B", "nordkap", "B", 101, "b24"),
    ("yulerune_s14_A", "yulerune", "A", 124, "b5"),
    ("midgard_s54_B", "midgard", "B", 145, "b18"),
    ("atoll_s77_A", "atoll", "A", 149, "b26"),
    ("drakkarfjord_s17_A", "drakkarfjord", "A", 217, "b6"),
    ("glacierkeep_s37_A", "glacierkeep", "A", 431, "b13"),
]
FUNDED_MIN, HEAL_MAX, KILL_SHOTS = 0.25, 0.80, 28

print("v520 FAILURE REEL -- arm bots/_v520pincer vs bots/_v488beltbreak2, "
      "headline grid scratchpad/s51_v520_build/grid/b1..b27")
print("SELECTION (a CHOICE, not a discovery): the EARLIEST our-core-death in "
      "EACH of the six maps for the v520 arm -- one board per map, so the reel "
      "is not six copies of one board.")
print("  our-core-death = grid row with ours == 'OPP' and cond starting "
      "'Core destroyed'; earliest = lowest `turn`; ties break lowest block, "
      "then lowest seed, then seat A.")
print("  drawn from 315 our-core-deaths in 972 v520 rows across 27 blocks; "
      "NO tie occurred on any of the six maps.")
print("CLASS THRESHOLDS (v519's, unchanged): FUNDED_MIN=%.2f HEAL_MAX=%.2f "
      "KILL_SHOTS=%d -> NO_TURRET / MAG_STARVED / HEAL_OUTRUN / TURRET_LOST"
      % (FUNDED_MIN, HEAL_MAX, KILL_SHOTS))
print()

fails, ident, classes = [], 0, []
for tag, mp, seat, turn, blk in GAMES:
    our = 0 if seat == "A" else 1
    p = HERE / "replays" / (tag + ".replay26")
    r = turrets.run(p, our)
    T = r["turrets"]
    for lbl, team in (("our", our), ("opp", r["opp"])):
        fired = sum(x["core_shots"] for x in T.values()
                    if x["team"] == team and x["kind"] == "sentinel")
        hp = r["core_sent_hits"][1 - team]
        if fired != hp:
            fails.append("%s %s: fireTurret %d != UpdateHp %d"
                         % (tag, lbl, fired, hp))
    a = summarise(analyse(p, our))
    calc = a["ourcore_hp_calc"]
    if not (-18 < calc <= 0):
        fails.append("%s: HP identity %d not in (-18,0]" % (tag, calc))
    else:
        ident += 1
    tp = Tape(p, our)
    ring = sum(1 for row in tp.rows if row.get("near_bot"))
    ours = [t for t in T.values() if t["team"] == our]
    siege = [t for t in ours if t["core_shots"] > 0]
    theirs = [t for t in T.values() if t["team"] == r["opp"]]
    their_siege = [t for t in theirs if t["core_shots"] > 0]
    shots = sum(t["core_shots"] for t in siege)
    life = sum(t["life"] for t in siege)
    funded = sum(t["funded_r"] for t in siege)
    dealt = shots * 18
    fs = funded / life if life else 0.0
    hs = a["oppcore_heal"] / dealt if dealt else 0.0
    if shots == 0:
        cls = "NO_TURRET"
    elif fs < FUNDED_MIN:
        cls = "MAG_STARVED"
    elif hs >= HEAL_MAX:
        cls = "HEAL_OUTRUN"
    elif shots < KILL_SHOTS:
        cls = "TURRET_LOST"
    else:
        cls = "TURRET_LOST"
    classes.append(cls)

    # ---- v520 facts 1 & 2: two-body presence and heal-seat denial ----------
    sr_tape, n_seats, sr_our, ecore = seatrate.tape_for(p, mp, seat)
    if sr_our != our:
        fails.append("%s: seatrate team %d != reel team %d" % (tag, sr_our, our))
    max_bodies = max((nb for _r, _d, _k, nb in sr_tape), default=0)
    sr = seatrate.fold(sr_tape, n_seats)
    max_den = max((len(d) for _r, d, _k, _n in sr_tape), default=0)
    full = [rr for rr, d, _k, _n in sr_tape if n_seats and len(d) == n_seats]
    hr, htot = heal_rounds(p, our)
    if htot != a["oppcore_heal"]:
        fails.append("%s: per-round heal %d != crip oppcore_heal %d"
                     % (tag, htot, a["oppcore_heal"]))
    # ---- v520 fact 3: terminal-launcher heal-seat coverage -----------------
    tc_rows, tc_meta, _led = termcov.analyse(p, mp, seat)
    cov = [x for x in tc_rows if x["coverage"] > 0]
    alive = set()
    for x in cov:
        last = (x["death_round"] - 1 if x["death_round"] >= 0
                else tc_meta["rounds"] - 1)
        alive |= set(range(x["birth"], last + 1))

    print("=" * 78)
    print("%s  (%s seat %s, grid %s)  OUR CORE DEAD r%d   CLASS %s"
          % (tag, mp, seat, blk, turn, cls))
    print("  ring rounds (a builder of ours inside d^2<=8 of their core): "
          "%d of %d" % (ring, turn))
    print("  OUR turrets: %d total | core-hitting %d | shots on their core %d "
          "(%d dmg) | funded share %.2f"
          % (len(ours), len(siege), shots, dealt, fs))
    print("  their core: dealt %d healed %d  HEAL-BACK %.3f | their core HP end %d"
          % (a["oppcore_dmg"], a["oppcore_heal"], hs, a["oppcore_hp_calc"]))
    print("  our beltbreak shredders (gunner, d^2<=100 of their core): %d "
          "first r%s | our fwd sentinels %d first r%s"
          % (a["fwd_gun_n"], a["fwd_gun_first"], a["fwd_sent_n"],
             a["fwd_sent_first"]))
    print("  their economy: %d harvesters + %d belts built, %d of it destroyed"
          % (a["opp_harv_built"], a["opp_belt_built"], a["opp_eco_killed"]))
    print("  THEIR core-hitting turrets: %d, first opened r%s, %d shots on us"
          % (len(their_siege),
             min((t["first_core"] for t in their_siege), default=None),
             sum(t["core_shots"] for t in their_siege)))
    print("  our forward launchers %d, collar barriers %d"
          % (a["fwd_laun_n"], a["collar_bar_n"]))
    print("  [v520] TWO-BODY PRESENCE (our builders, d^2<=50 of their core): "
          ">=1 in %d rounds, >=2 in %d (share %s), MAX simultaneous %d"
          % (sr["atring_rounds"], sr["atring2_rounds"],
             sr["two_body_share"], max_bodies))
    print("  [v520] HEAL SEATS DENIED: %d of %d legal seats, first r%s last r%s "
          "(%d by building, %d by body) | closure r%s cumulative r%s | "
          "seal rate %s per 100 at-ring rounds"
          % (sr["seats_sealed"], n_seats, sr["first_seal"], sr["last_seal"],
             sr["sealed_by_bldg"], sr["sealed_by_body"], sr["closure_round"],
             sr["closure_cum_round"], sr["seal_rate"]))
    print("  [v520] SEAL vs HEAL: max seats denied simultaneously %d; rounds "
          "with ALL %d denied %d (r%s..r%s); enemy-core heal rounds %d "
          "(r%s..r%s), of which %d fell in a fully-sealed round"
          % (max_den, n_seats, len(full),
             full[0] if full else None, full[-1] if full else None,
             len(hr), hr[0] if hr else None, hr[-1] if hr else None,
             len(set(hr) & set(full))))
    print("  [v520] TERMINAL LAUNCHER within d^2<=2 of a heal seat: %s "
          "(%d of %d of our launchers in the throw envelope; union alive %d "
          "rounds; best coverage reachable from the evictor envelope %s seats)"
          % ("YES" if cov else "NO", len(cov), len(tc_rows), len(alive),
             tc_rows[0]["best_cov_site"] if tc_rows
             else "n/a - no launcher of ours in the envelope"))
    for x in tc_rows:
        print("        launcher id%-4d %-7s born r%-4d dsq_core %-4d cover %d "
              "(ferry-form %d) life %-4d throws %d (%d from a seat)"
              % (x["eid"], x["pos"], x["birth"], x["dsq_core"], x["coverage"],
                 x["coverage_ferry"], x["lifetime"], x["n_launch"],
                 x["n_launch_seat"]))
    for t in sorted(ours, key=lambda x: x["built"])[:8]:
        print("     %-9s %-8s built r%-4d died %-5s life %-4d d2opp %-5d "
              "shots %-3d core %-3d" % (t["kind"], str(t["pos"]), t["built"],
                                        t["died"], t["life"], t["dsq_opp"],
                                        t["shots"], t["core_shots"]))
print("=" * 78)
print("CLASS DISTRIBUTION over the 6 reel games: "
      + ", ".join("%s %d" % (c, classes.count(c))
                  for c in sorted(set(classes))))

# ⭐ NEGATIVE CONTROL for the ONE new guard in this file.  The other three
# guards are the v519/v520 instruments' own, already driven both ways there;
# `heal_rounds` is new code, so it is driven to the OTHER verdict here: read
# with the team flipped it must DISAGREE with crip's oppcore_heal on a game
# where the two teams' cores were healed by different amounts.  A guard that
# has never produced the other verdict has not been seen to check.
_ctl_tag, _ctl_mp, _ctl_seat, _ctl_turn, _ctl_blk = GAMES[2]  # midgard_s54_B
_ctl_p = HERE / "replays" / (_ctl_tag + ".replay26")
_ctl_our = 0 if _ctl_seat == "A" else 1
_ctl_ref = summarise(analyse(_ctl_p, _ctl_our))["oppcore_heal"]
_ctl_flip = heal_rounds(_ctl_p, 1 - _ctl_our)[1]
if _ctl_flip == _ctl_ref:
    fails.append("NEGATIVE CONTROL: flipped-team heal total %d equals the "
                 "as-played %d -- the guard cannot fail" % (_ctl_flip, _ctl_ref))

if fails:
    sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails) + "\n")
    raise SystemExit(2)
sys.stderr.write("negative control on %s: as-played oppcore_heal %d, "
                 "team-flipped %d -- guard CAN fail\n"
                 % (_ctl_tag, _ctl_ref, _ctl_flip))
sys.stderr.write("guards OK: HP identity %d/%d, fireTurret vs UpdateHp "
                 "channel agreement %d/%d, seatrate team agreement %d/%d, "
                 "per-round heal vs crip oppcore_heal %d/%d\n"
                 % (ident, len(GAMES), len(GAMES), len(GAMES),
                    len(GAMES), len(GAMES), len(GAMES), len(GAMES)))
