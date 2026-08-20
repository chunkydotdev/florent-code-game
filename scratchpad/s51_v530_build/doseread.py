#!/usr/bin/env python3
"""Fold the v530 dose tapes: does each plank FIRE, and does its own ablation
drive its counter to zero?

One row per arm.  Counters are counts of the instrument lines the tree emits
under FS_V530_LOG:
  MOUTH arm   -- a body planned a core-outward chain
  MOUTH link  -- a conveyor laid mouth-first
  MOUTH harv  -- the terminal harvester, built LAST
  MOUTH ttl   -- a chain abandoned on the TTL (the bounded failure path)
  CORNER      -- a barrier on one of OUR OWN 4 diagonal ring corners
  DOORKILL    -- a shot taken under the door-launcher promotion

⛔ GUARDS, each driven to BOTH verdicts by --selftest:
  * a synthetic tape with lines present must count them;
  * the same tape with the lines removed must read 0 on every counter;
  * a tape carrying ONLY corner lines must read 0 mouth and nonzero corner,
    i.e. the counters must not be aliases of one another.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

PATS = {
    "mouth_arm": re.compile(r"^V530 MOUTH arm "),
    "mouth_link": re.compile(r"^V530 MOUTH link "),
    "mouth_harv": re.compile(r"^V530 MOUTH harv "),
    "mouth_ttl": re.compile(r"^V530 MOUTH ttl "),
    "corner": re.compile(r"^V530 CORNER "),
    "doorkill": re.compile(r"^V530 DOORKILL "),
    "ring": re.compile(r"^V530 RING "),
}
SOCK = re.compile(r"^V530 MOUTH link rnd=(\d+) seat=\d+ .* left=(\d+)")
HARV = re.compile(r"^V530 MOUTH harv rnd=(\d+) seat=\d+ ore=[-\d]+,[-\d]+ "
                  r"sock=([-\d]+) links=(\d+)")


def fold_text(text):
    out = defaultdict(int)
    socks, harvs, chains = [], [], []
    for line in text.splitlines():
        line = line.strip()
        for k, p in PATS.items():
            if p.match(line):
                out[k] += 1
        m = HARV.match(line)
        if m:
            harvs.append(int(m.group(1)))
            if int(m.group(2)) >= 0:
                socks.append(int(m.group(2)))
            chains.append(int(m.group(3)))
        out["tb"] += line.startswith("Traceback")
    out["_socks"] = socks
    out["_harvs"] = harvs
    out["_chains"] = chains
    return out


def fold_dir(d):
    tot = defaultdict(int)
    socks, harvs, chains = [], [], []
    n = 0
    for p in sorted(Path(d).glob("*.err")):
        n += 1
        o = fold_text(p.read_text(errors="replace"))
        for k in PATS:
            tot[k] += o[k]
        tot["tb"] += o["tb"]
        socks += o["_socks"]
        harvs += o["_harvs"]
        chains += o["_chains"]
    tot["games"] = n
    tot["_socks"] = socks
    tot["_harvs"] = harvs
    tot["_chains"] = chains
    return tot


def med(xs):
    if not xs:
        return -1
    s = sorted(xs)
    return s[len(s) // 2]


def main(base):
    arms = ["inst_v530", "inst_nomouth", "inst_nocorner", "inst_nodoor",
            "inst_ring", "inst_flagoff"]
    print("%-14s %6s %5s %6s %6s %5s %7s %9s %6s | %8s %8s %8s | %3s"
          % ("arm", "games", "Marm", "Mlink", "Mharv", "Mttl", "CORNER",
             "DOORKILL", "RING", "sock_med", "harv_med", "chain_md", "tb"))
    for a in arms:
        d = Path(base) / "dose" / a
        if not d.exists():
            print("%-14s  (missing)" % a)
            continue
        o = fold_dir(d)
        print("%-14s %6d %5d %6d %6d %5d %7d %9d %6d | %8s %8s %8s | %3d"
              % (a, o["games"], o["mouth_arm"], o["mouth_link"],
                 o["mouth_harv"], o["mouth_ttl"], o["corner"], o["doorkill"],
                 o["ring"], med(o["_socks"]), med(o["_harvs"]),
                 med(o["_chains"]), o["tb"]))


def selftest():
    live = ("V530 MOUTH arm rnd=1 seat=1 ore=5,5 links=4 sock=2,3\n"
            "V530 MOUTH link rnd=2 seat=1 tile=2,3 face=NORTH left=3\n"
            "V530 MOUTH link rnd=4 seat=1 tile=3,3 face=WEST left=2\n"
            "V530 MOUTH harv rnd=9 seat=1 ore=5,5 sock=2 links=4\n"
            "V530 CORNER rnd=6 seat=1 tile=1,1 held=1\n"
            "V530 CORNER rnd=8 seat=1 tile=4,1 held=2\n"
            "V530 DOORKILL SENTINEL rnd=88 at=7,7\n"
            "V530 MOUTH ttl rnd=70 seat=2 left=3\n"
            "V530 RING rnd=5 seat=3 tile=2,4 face=EAST n=1\n")
    dead = "nothing here\nsome other bot line\n"
    only_corner = "V530 CORNER rnd=6 seat=1 tile=1,1 held=1\n"
    a, b, c = fold_text(live), fold_text(dead), fold_text(only_corner)
    assert a["mouth_arm"] == 1 and a["mouth_link"] == 2 and a["mouth_harv"] == 1
    assert a["mouth_ttl"] == 1 and a["corner"] == 2 and a["doorkill"] == 1
    assert a["ring"] == 1 and c["ring"] == 0
    assert a["_socks"] == [2] and a["_harvs"] == [9] and a["_chains"] == [4]
    for k in PATS:
        assert b[k] == 0, "dead tape must read 0 on %s" % k
    assert c["corner"] == 1 and c["mouth_link"] == 0 and c["doorkill"] == 0, \
        "counters must not alias one another"
    # a reader blind to the ablation would report the same number twice
    assert a["corner"] != c["corner"]
    print("SELFTEST OK: a live tape counts every plank separately; a tape with "
          "the lines removed reads 0 on ALL SIX counters; a corner-only tape "
          "reads corner>0 and mouth=0/doorkill=0, so the counters are not "
          "aliases; sock/harv/chain parse out of the harvester line.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main(sys.argv[1] if len(sys.argv) > 1
         else "/Users/junghard/Projects/Work/florent-code-game/"
              "scratchpad/s51_v530_build")
