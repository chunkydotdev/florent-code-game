#!/usr/bin/env python3
"""Pair-rounds aggregator (PREREG-LIVE-ROBUSTNESS FIRE GATE 4).
Input: list of (born, died_or_None, end_round) forward-tube records.
Output: (pair_rounds, any_rounds). GAME CONTEXT: in-game league analysis."""
def pair_rounds(tubes, end):
    cnt = {}
    for born, died in tubes:
        hi = end if died is None else died
        for r in range(born, hi):
            cnt[r] = cnt.get(r, 0) + 1
    pair = sum(1 for v in cnt.values() if v >= 2)
    any_ = len(cnt)
    return pair, any_
if __name__ == "__main__":
    # BOTH-VERDICT FIXTURES (gate 4's requirement):
    z = pair_rounds([(10, 20), (30, 40)], 100)      # disjoint -> 0 pair
    assert z == (0, 20), z
    p = pair_rounds([(10, 30), (20, 25), (24, None)], 40)  # overlap 20-24 & 24 onward
    # rounds 20-24 have 2; 24 has tubes (10,30)+(24,None)=2 ... compute expected: r20..24 from first two (20,21,22,23,24? died=25 -> hi=25 so r20..24), plus (24,None) adds r24..39; overlap r24..29 with (10,30)
    # verified by hand: pair rounds = r20..29 = 10
    assert p[0] == 10, p
    print("PAIRAGG BOTH VERDICTS OK:", z, p)
