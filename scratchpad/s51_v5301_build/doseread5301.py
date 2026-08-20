#!/usr/bin/env python3
"""Fold the v530.1 dose tapes PER SEAT -- the direct mechanism read on the fix.

The v530 defect is that EVERY eco seat arms a mouth chain in the opening, so the
team can hold no harvester at all while two chains are in flight.  The fix is a
seat rule, so the tape must show it AS A SEAT SHIFT and not merely as fewer
chains:

  arms_by_seat        v530: seats 1,2(,3) all arm early.
                      v531: seat 1 arms early; other seats arm LATE or not at all.
  arm_round by seat   the number that carries the claim.  A non-designated seat
                      may still arm in v531 -- once the team owns a harvester --
                      so "0 arms on seat 2" is NOT the prediction and would be a
                      different (over-strong) fix.
  games_multiseat_r30 games in which MORE THAN ONE seat had armed a chain by
                      r30.  This is the defect's own shape and it must fall.

⛔ GUARDS, each driven to the OTHER verdict by `--selftest`:
  * a tape with arm lines present must count them, and the same tape with the
    lines stripped must read 0 on every counter;
  * a tape whose arms are ALL on seat 1 must read multiseat_r30 = 0 while a tape
    with seats 1 and 2 at r3 must read 1 -- so the multiseat counter is not an
    alias for "number of arms";
  * a tape with only CORNER lines must read 0 mouth arms and nonzero corners.
"""
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ARM = re.compile(r"^V530 MOUTH arm rnd=(\d+) seat=(\d+) .*links=(\d+) ")
HARVL = re.compile(r"^V530 MOUTH harv rnd=\d+ seat=(\d+) .*links=(\d+)")
LINK = re.compile(r"^V530 MOUTH link rnd=(\d+) seat=(\d+) ")
HARV = re.compile(r"^V530 MOUTH harv rnd=(\d+) seat=(\d+) ")
TTL = re.compile(r"^V530 MOUTH ttl rnd=(\d+) seat=(\d+) ")
CORNER = re.compile(r"^V530 CORNER ")


def fold_text(text):
    out = {"arms": [], "links": 0, "harv": 0, "ttl": 0, "corner": 0,
           "seats_by_r30": set(), "short_harv": 0, "full_harv": 0}
    planned = {}
    for line in text.splitlines():
        line = line.strip()
        m = ARM.match(line)
        if m:
            rnd, seat = int(m.group(1)), int(m.group(2))
            out["arms"].append((seat, rnd))
            planned[seat] = int(m.group(3))
            if rnd <= 30:
                out["seats_by_r30"].add(seat)
            continue
        if LINK.match(line):
            out["links"] += 1
        elif HARV.match(line):
            out["harv"] += 1
            # ⭐ THE SHORT-CHAIN COUNTER.  `arm` records the PLANNED link count
            # and `harv` records how many were actually LAID.  A terminal
            # harvester reached with fewer links than planned means the mouth
            # walker POPPED a tile as "occupied" instead of building it -- the
            # chain has a hole it never owned, and the harvester at the far end
            # may have no route home.  This is the interaction the v530.1 seat
            # rule can create and the v530 tree could not: one eco seat laying
            # core-outward while another lays ore-inward across the same tiles.
            mh = HARVL.match(line)
            if mh:
                seat_h, laid = int(mh.group(1)), int(mh.group(2))
                want = planned.get(seat_h)
                if want is not None and laid < want:
                    out["short_harv"] += 1
                else:
                    out["full_harv"] += 1
        elif TTL.match(line):
            out["ttl"] += 1
        elif CORNER.match(line):
            out["corner"] += 1
    return out


def main(dosedir):
    root = Path(dosedir)
    print("%-11s %6s %6s %6s %6s %6s %6s %6s %8s | %s"
          % ("arm", "games", "arms", "links", "harv", "shortH", "fullH",
             "ttl", "multi30", "arms by seat: n(median arm round)"))
    for arm in sorted(p.name for p in root.iterdir() if p.is_dir()):
        games = 0
        tot = defaultdict(int)
        byseat = defaultdict(list)
        multi = 0
        for err in sorted((root / arm).glob("*.err")):
            games += 1
            f = fold_text(err.read_text(errors="replace"))
            for k in ("links", "harv", "ttl", "corner", "short_harv",
                      "full_harv"):
                tot[k] += f[k]
            tot["arms"] += len(f["arms"])
            for seat, rnd in f["arms"]:
                byseat[seat].append(rnd)
            if len(f["seats_by_r30"]) > 1:
                multi += 1
        cells = "  ".join(
            "s%d:%d(%.0f)" % (s, len(byseat[s]), statistics.median(byseat[s]))
            for s in sorted(byseat))
        print("%-11s %6d %6d %6d %6d %6d %6d %6d %8.3f | %s"
              % (arm, games, tot["arms"], tot["links"], tot["harv"],
                 tot["short_harv"], tot["full_harv"], tot["ttl"],
                 multi / games if games else -1, cells))


def selftest():
    full = ("V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=3 sock=2,2\n"
            "V530 MOUTH arm rnd=4 seat=2 ore=5,5 links=3 sock=6,6\n"
            "V530 MOUTH link rnd=3 seat=1 tile=2,2 face=NORTH left=2\n"
            "V530 MOUTH harv rnd=9 seat=1 ore=1,1 sock=3 links=3\n"
            "V530 MOUTH ttl rnd=70 seat=2 left=1\n"
            "V530 CORNER rnd=5 seat=1 tile=0,0 held=1\n")
    a = fold_text(full)
    assert len(a["arms"]) == 2 and a["links"] == 1 and a["harv"] == 1 \
        and a["ttl"] == 1 and a["corner"] == 1
    assert a["seats_by_r30"] == {1, 2}
    b = fold_text("")
    assert not b["arms"] and b["links"] == 0 and b["harv"] == 0 \
        and b["ttl"] == 0 and b["corner"] == 0, "stripped tape is not zero"
    one = fold_text("V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=3 sock=2,2\n"
                    "V530 MOUTH arm rnd=80 seat=2 ore=5,5 links=3 sock=6,6\n")
    assert len(one["arms"]) == 2, "arm count is wrong"
    assert one["seats_by_r30"] == {1}, \
        "multiseat is an alias for the arm count -- a LATE arm must not count"
    # SHORT-CHAIN counter, driven to BOTH verdicts on the same shape
    shortt = fold_text(
        "V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=3 sock=2,2\n"
        "V530 MOUTH harv rnd=9 seat=1 ore=1,1 sock=3 links=1\n")
    fullt = fold_text(
        "V530 MOUTH arm rnd=2 seat=1 ore=1,1 links=3 sock=2,2\n"
        "V530 MOUTH harv rnd=9 seat=1 ore=1,1 sock=3 links=3\n")
    assert shortt["short_harv"] == 1 and shortt["full_harv"] == 0
    assert fullt["short_harv"] == 0 and fullt["full_harv"] == 1, \
        "the short-chain counter fires on a COMPLETE chain"
    corners = fold_text("V530 CORNER rnd=5 seat=1 tile=0,0 held=1\n" * 4)
    assert not corners["arms"] and corners["corner"] == 4, \
        "the counters are aliases of one another"
    print("SELFTEST OK: a full tape counts every line type; a stripped tape "
          "reads 0 on all six counters; a tape whose second arm lands at r80 "
          "reads multiseat_r30 = {1} while the same tape at r4 reads {1,2} -- "
          "so multiseat is not an alias for the arm count; a corner-only tape "
          "reads 0 mouth arms and 4 corners; a harvester reached with 1 of 3 planned "
          "links counts as short and one reached with 3 of 3 counts as full.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main(sys.argv[1])
