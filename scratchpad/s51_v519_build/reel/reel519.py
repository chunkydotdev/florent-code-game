#!/usr/bin/env python3
"""v519 FAILURE REEL: board facts for the six worst losses of the best arm.

⛔ COPIED MACHINERY, GUARDS RUN IN PLACE.  `turrets.py` (fireTurret channel),
`tape.py` (per-round board) and `crip.py` (UpdateHp ledger) are the s51
rush-autopsy / v519 instruments, unmodified; this file only joins them and
prints.  The two channel guards it re-runs per game:
  * HP IDENTITY: 500 + sum(UpdateHp deltas on our core) must land in (-18, 0]
    for a destroyed core (damage is not clamped, so the killing blow overshoots
    by at most one sentinel hit).
  * CHANNEL AGREEMENT: our sentinels' fireTurret core hits must equal the count
    of -18 UpdateHp deltas on THEIR core, both directions, every game.
⛔ EVERYTHING BELOW IS ENGINE-SIDE.  The headline arms run every log flag False
and platform replays carry no stdout at all.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
import turrets  # noqa: E402
from crip import analyse, summarise  # noqa: E402
from tape import Tape  # noqa: E402

GAMES = [
    ("nordkap_s8_A", "nordkap", "A", 112),
    ("atoll_s4_B", "atoll", "B", 114),
    ("yulerune_s36_A", "yulerune", "A", 132),
    ("midgard_s15_A", "midgard", "A", 146),
    ("drakkarfjord_s10_B", "drakkarfjord", "B", 242),
    ("glacierkeep_s20_B", "glacierkeep", "B", 518),
]
FUNDED_MIN, HEAL_MAX, KILL_SHOTS = 0.25, 0.80, 28

fails, ident = [], 0
for tag, mp, seat, turn in GAMES:
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
    print("=" * 78)
    print("%s  (%s seat %s)  OUR CORE DEAD r%d   CLASS %s"
          % (tag, mp, seat, turn, cls))
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
    for t in sorted(ours, key=lambda x: x["built"])[:8]:
        print("     %-9s %-8s built r%-4d died %-5s life %-4d d2opp %-5d "
              "shots %-3d core %-3d" % (t["kind"], str(t["pos"]), t["built"],
                                        t["died"], t["life"], t["dsq_opp"],
                                        t["shots"], t["core_shots"]))
if fails:
    sys.stderr.write("GUARD FAIL:\n  " + "\n  ".join(fails) + "\n")
    raise SystemExit(2)
sys.stderr.write("guards OK: HP identity %d/%d, fireTurret vs UpdateHp "
                 "channel agreement %d/%d\n" % (ident, len(GAMES),
                                                len(GAMES), len(GAMES)))
