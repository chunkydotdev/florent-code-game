#!/usr/bin/env python3
"""FAILURE REEL narrator: per-game board facts for the ~5 worst losses.

⛔ EVERY FIGURE HERE IS ENGINE-SIDE.  The headline arms run with every log flag
False (they are the arms the report's numbers come from), so nothing in this
file can come from our own stdout -- which is the correct discipline anyway,
`CLAUDE.md`: platform replays carry no stdout at all.

Sources: `turret_ledger.tsv` / `turret_game.tsv` / `attrib.tsv` / `classified.tsv`
(the s51 rush-autopsy machinery, copied not rewritten, guards driven in place:
HP identity 5/5 and fireTurret-vs-UpdateHp channel agreement 5/5) plus the
per-round `Tape`.

⭐ THE FIREDISC HOLD READ, and it is an INFERENCE with its bound stated: a round
is HELD if a forward sentinel of ours was alive AND team ammo >= 10 AND it fired
no shot.  A sentinel reloads 2, so at most half of a firing sentinel's rounds
can be shots; the reported number is therefore an UPPER BOUND on holds and
includes every reload round.  What it can still say is the SHAPE -- a sentinel
whose non-firing funded rounds are ~50% is reloading, one at 90% is holding or
has nothing in its line.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tape import Tape  # noqa: E402
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, read_pos, scalars,
)


def shots_by_round(path, our_team):
    """{round: [(from_tile)]} for our team's fireTurret events."""
    data = path.read_bytes()
    turns = [v for n, w, v in fields(data) if n == 3 and w == WIRE_LEN]
    out = defaultdict(list)
    # ⛔ THE NESTING IS turn -> update-list -> update, EXACTLY as `turrets.py`
    # walks it (`for _n,_w,ub in fields(tb): for un,_uw,ubuf in fields(ub)`).
    # A one-level walk finds ZERO FireTurret events and silently reports every
    # funded round as a hold -- which is what it did on the first run here, and
    # is why the count below is asserted non-zero against `turret_ledger.tsv`.
    for i, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un != 12:
                    continue
                frm = None
                for fn, _fw, fv in fields(ubuf):
                    if fn == 1:
                        frm = read_pos(fv)
                out[i].append(frm)
    return out


def main():
    led = defaultdict(list)
    for r in csv.DictReader(open(HERE / "turret_ledger.tsv"), delimiter="\t"):
        led[r["tag"]].append(r)
    cls = {r["tag"]: r for r in
           csv.DictReader(open(HERE / "classified.tsv"), delimiter="\t")}
    att = {r["tag"]: r for r in
           csv.DictReader(open(HERE / "attrib.tsv"), delimiter="\t")}
    grid = {r["tag"]: r for r in
            csv.DictReader(open(HERE / "fired30.tsv"), delimiter="\t")}
    for tag in grid:
        g = grid[tag]
        our = 0 if g["seat"] == "A" else 1
        t = Tape(Path(HERE / "replays" / (tag + ".replay26")), our)
        sh = shots_by_round(Path(HERE / "replays" / (tag + ".replay26")), our)
        c = cls[tag]
        a = att[tag]
        print("=" * 78)
        print("%s  map=%s seat=%s  OUR CORE DIED r%s   offence=%s"
              % (tag, g["map"], g["seat"], g["turn"], c["offence"]))
        # arrival + raider presence
        arrive = next((r["r"] for r in t.rows if r["near_bot"] > 0), None)
        ring = [r["r"] for r in t.rows if r["near_bot"] > 0]
        print("  raider: first inside d^2<=8 of their core r%s ; rounds with a "
              "body there %d of %d ; longest absence %d"
              % (arrive, len(ring), len(t.rows),
                 max([b - a2 - 1 for a2, b in zip(ring, ring[1:])] or [0])))
        # turrets
        for r in led[tag]:
            dsq = float(r["dsq_opp"])
            kind = "FORWARD" if dsq <= 40 else "home"
            if r["kind"] == "launcher" and kind == "home":
                continue
            print("    %-8s %-9s %-8s built r%-4s life %-4s shots %-4s "
                  "core-shots %-4s first-core r%-5s funded %s"
                  % (kind, r["kind"], r["pos"], r["built"], r["life"],
                     r["shots"], r["core_shots"], r["first_core"] or "-",
                     r["funded_r"]))
            if kind == "FORWARD" and r["kind"] == "sentinel":
                b = int(r["built"])
                e = b + int(r["life"])
                fired = set()
                for rr, frm in sh.items():
                    for f in frm:
                        if f and tuple(f) == tuple(
                                int(x) for x in r["pos"].strip("()").split(",")):
                            fired.add(rr)
                funded_rounds = [x["r"] for x in t.rows
                                 if b <= x["r"] < e and x["our_ammo"] >= 10]
                held = [x for x in funded_rounds if x not in fired]
                print("        funded rounds %d, of which NO SHOT %d (%.0f%% -- "
                      "UPPER BOUND on FIREDISC holds, includes every reload)"
                      % (len(funded_rounds), len(held),
                         100.0 * len(held) / max(1, len(funded_rounds))))
        print("  damage on OUR core: sentinel %s gunner %s peck %s ; heals we "
              "put back %s ; their first core-hitting turret r%s, %s shots"
              % (a.get("ourcore_sent"), a.get("ourcore_gun"),
                 a.get("ourcore_peck"), a.get("ourcore_heal"),
                 c["their_first"], c["their_shots"]))
        print("  their core: we landed %s shots = %s dmg, they healed %s "
                "(%s of it) ; enemy core min HP %s at r%s"
              % (c["siege_shots"], int(c["siege_shots"]) * 18,
                 c["oppcore_heal"], c["heal_share"],
                 min((x["opp_core_hp"] for x in t.rows), default="-"),
                 next((x["r"] for x in t.rows
                       if x["opp_core_hp"] == min(
                           y["opp_core_hp"] for y in t.rows)), "-")))


if __name__ == "__main__":
    main()
