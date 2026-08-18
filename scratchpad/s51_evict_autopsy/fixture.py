#!/usr/bin/env python3
"""INSTRUMENT GUARD for parse.py -- drive the counter BOTH WAYS on synthetic
logs with hand-known answers, per case AND per branch.  A counter that has
never read nonzero has not been seen to count; a gate-attribution column that
has never produced each of its four verdicts has not been seen to attribute.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse_game  # noqa: E402

CASES = []


def case(name, err, out, **expect):
    CASES.append((name, err, out, expect))


# --- 1. THE ZERO CASE: raider at the ring 4 rounds, nothing happens ---------
case("all-zero", """FS GATE 0 sig (33, 33, (3, 3), (29, 29)) ok 1
FS DL 20 id 3 role seal orth 8 need 8 ebody 0 lau 0 ti 100 lcost 30 bar 5 obs 0 hist 0 pend 0
FS DL 21 id 3 role seal orth 8 need 8 ebody 0 lau 0 ti 100 lcost 30 bar 5 obs 0 hist 0 pend 0
FS DL 22 id 3 role seal orth 7 need 7 ebody 0 lau 0 ti 100 lcost 30 bar 5 obs 0 hist 0 pend 0
FS DL 23 id 3 role seal orth 7 need 7 ebody 0 lau 0 ti 100 lcost 30 bar 5 obs 0 hist 0 pend 0
""", "  Winner: base  (Core destroyed, turn 300)\n",
     evicts=0, evictor_r=-1, first_lau_r=-1, ring_rounds=4, dead_rounds=0,
     dead_first=-1, close_r=-1, g_obs=0, g_pend=0, g_fund=0, g_open=0,
     outcome="base", cond="Core_destroyed", end_r=300)

# --- 2. THE NONZERO CASE: 3 throws, an evictor build, a closure -------------
case("nonzero", """FS EVICTOR 55 at (12, 13) cov 7
FS DL 40 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
FS DL 41 id 3 role seal orth 4 need 4 ebody 2 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
FS DL 55 id 3 role seal orth 3 need 3 ebody 1 lau 1 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
FS EVICT 57 from (12, 12) to (0, 3)
FS EVICT 61 from (12, 14) to (0, 3)
FS EVICT 70 from (11, 13) to (29, 0)
FS DL 80 id 3 role seal orth 0 need 0 ebody 0 lau 1 ti 40 lcost 30 bar 5 obs 9 hist 3 pend 0
FS DL 81 id 3 role seal orth 0 need 0 ebody 0 lau 1 ti 40 lcost 30 bar 5 obs 9 hist 3 pend 0
""", "  Winner: v513_log  (Core destroyed, turn 120)\n",
     evicts=3, evictor_r=55, first_lau_r=55, ring_rounds=5, dead_rounds=2,
     dead_first=40, close_r=80, g_obs=0, g_pend=0, g_fund=0, g_open=2,
     outcome="v513_log", cond="Core_destroyed", end_r=120)

# --- 3. GATE ATTRIBUTION: one deadlock round per branch, all four present ---
# r10 obs 2 < 5                       -> g_obs
# r11 obs 9, pend 1                   -> g_pend
# r12 obs 9, pend 0, ti 30 < 30+12+4*5+6 = 68  -> g_fund
# r13 obs 9, pend 0, ti 200 >= 68     -> g_open
case("gates", """FS DL 10 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 2 hist 1 pend 0
FS DL 11 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 1
FS DL 12 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 30 lcost 30 bar 5 obs 9 hist 3 pend 0
FS DL 13 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
""", "  Winner: v513_log  (Core destroyed, turn 200)\n",
     evicts=0, evictor_r=-1, first_lau_r=-1, ring_rounds=4, dead_rounds=4,
     dead_first=10, close_r=-1, g_obs=1, g_pend=1, g_fund=1, g_open=1,
     outcome="v513_log", cond="Core_destroyed", end_r=200)

# --- 4. NEGATIVE CONTROL: an enemy body on a seat while we DO own a launcher
#        is NOT deadlock exposure.  Same lines as case 3 with lau 1.
case("lau-cancels", """FS DL 10 id 3 role seal orth 4 need 4 ebody 1 lau 1 ti 200 lcost 30 bar 5 obs 2 hist 1 pend 0
FS DL 11 id 3 role seal orth 4 need 4 ebody 3 lau 1 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 1
""", "  Winner: base  (Core destroyed, turn 90)\n",
     evicts=0, evictor_r=-1, first_lau_r=10, ring_rounds=2, dead_rounds=0,
     dead_first=-1, close_r=-1, g_obs=0, g_pend=0, g_fund=0, g_open=0,
     outcome="base", cond="Core_destroyed", end_r=90)

# --- 5. NEGATIVE CONTROL: ebody 0 with no launcher is NOT exposure either ---
case("ebody-cancels", """FS DL 10 id 3 role seal orth 4 need 4 ebody 0 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
""", "  Winner: base  (Core destroyed, turn 90)\n",
     evicts=0, dead_rounds=0, ring_rounds=1, g_open=0)

# --- 6. TWO BODIES, ONE ROUND: dedup by round, not by line -----------------
case("dedup", """FS DL 30 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
FS DL 30 id 9 role supp orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
""", "  Winner: base  (Core destroyed, turn 90)\n",
     ring_rounds=1, dead_rounds=1)

# --- 7. MUTATION: corrupt every DL tag -> the parser must read NOTHING -----
case("corrupt", """FS XL 30 id 3 role seal orth 4 need 4 ebody 1 lau 0 ti 200 lcost 30 bar 5 obs 9 hist 3 pend 0
FS EVICTX 40 from (1,1) to (2,2)
""", "  Winner: base  (Core destroyed, turn 90)\n",
     ring_rounds=0, dead_rounds=0, evicts=0)

# --- 8. r1000 tiebreak summary shape --------------------------------------
case("r1000", """FS DL 900 id 3 role seal orth 2 need 2 ebody 1 lau 0 ti 9 lcost 60 bar 8 obs 9 hist 3 pend 1
""", "  Winner: base  (Titanium collected, turn 1000)\n",
     dead_rounds=1, g_pend=1, end_r=1000, cond="Titanium_collected")


def main():
    fails = 0
    d = tempfile.mkdtemp(prefix="s51fix")
    for name, err, out, expect in CASES:
        ep = os.path.join(d, name + ".err")
        op = os.path.join(d, name + ".out")
        open(ep, "w").write(err)
        open(op, "w").write(out)
        got = parse_game(ep, op)
        bad = {k: (v, got.get(k)) for k, v in expect.items() if got.get(k) != v}
        if bad:
            fails += 1
            print("FAIL %-14s %s" % (name, bad))
        else:
            print("ok   %-14s %s" % (name, {k: got[k] for k in expect}))
    print("\n%d/%d cases pass" % (len(CASES) - fails, len(CASES)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
