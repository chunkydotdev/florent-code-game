"""breakin_watch's k must count MATCHES, not tape rows.

CAUGHT LIVE 2026-08-11 on v114, ~40 minutes after it shipped: the guard printed
"v114 reached k=8; slot rule is armed. Break-in watch standing down." while the
platform reported 768 -> 770 matches -- k was 2 -- and the rating had already
fallen 1689 -> 1677. `elo_logger` polls every ~5 min, so `k = len(mine)` made the
stop-loss for a fresh ship DISARM ON A CLOCK rather than on evidence, inside the
exact window its own docstring calls unguarded.

A guard that stands down before it can fire is the same defect as one that never
fires, so all three outcomes are forced below.
"""
import sys
FAILS = []
def k_of(rows):
    """The fixed rule, isolated: difference of the cumulative match column."""
    try:
        return int(rows[-1][2]) - int(rows[0][2]) + 1
    except (IndexError, ValueError):
        return 0

def chk(name, got, want, forced_by):
    ok = got == want
    print(f"  [{'ok' if ok else 'FAIL'}] {name:<46} got={got} want={want}")
    if not ok:
        print(f"         forced by: {forced_by}"); FAILS.append(name)

# the live v114 case: 8 poll rows, 2 real matches
live = [("t","1689","768","v114"),("t","1686","769","v114"),("t","1677","770","v114"),
        ("t","1677","770","v114"),("t","1677","770","v114"),("t","1677","770","v114"),
        ("t","1677","770","v114"),("t","1677","770","v114")]
chk("8 poll rows / 2 matches -> k=3, NOT 8", k_of(live), 3,
    "THE LIVE BUG. len(rows)=8 disarmed the guard 40 min after the ship; the "
    "match column says 768->770. (3 = the 2 deltas plus the match that made row 1.)")
chk("...and therefore does NOT stand down", k_of(live) >= 8, False,
    "standing down at k=3 leaves a fresh ship with no automated stop-loss at all")

# a genuinely finished break-in
done = [("t","1689","768","v114"), ("t","1700","778","v114")]
chk("768 -> 778 -> k=11 stands down", k_of(done) >= 8, True,
    "THE POSITIVE CELL. If this never fires the guard runs forever and the slot "
    "rule never takes over -- a guard that cannot COMPLETE is also broken")

# unparseable column must stay ARMED, never fall back to len()
bad = [("t","1689","-","v114"), ("t","1677","-","v114")]
chk("unparseable match column -> k=0 (stay armed)", k_of(bad), 0,
    "falling back to len(rows) IS the bug; an unreadable column must fail SAFE, "
    "and safe here means armed")

print()
if FAILS:
    print(f"BREAKIN_K: FAIL ({len(FAILS)}) -> {FAILS}"); sys.exit(1)
print("BREAKIN_K: PASS (under-count, non-stand-down, genuine stand-down, unparseable)")
