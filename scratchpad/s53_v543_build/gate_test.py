"""v543 EDGE-TRIGGER STATE-MACHINE TEST.

Drives `_v543_tick` over synthetic bank traces and asserts the verdict comes
out BOTH ways.  A gate that has never refused has not been seen to gate.
"""
import sys
sys.path.insert(0, sys.argv[1])
import doctrine as D
import main as M


class FakeCT:
    def __init__(self, ti=470, harv=3):
        self.ti = ti
        self.harv = harv

    def get_global_resources(self):
        return self.ti

    def read_store(self, i):
        assert i == D.SLOT_HARVESTERS
        return self.harv

    def get_id(self):
        return 7


def drive(trace, harv=3, master=True, plank=True):
    """trace: list of bank values, one per round starting at r0.
    Returns (fire_rounds, open_rounds)."""
    old_m, old_p = D.LOKI_FS_V543, D.FS_V543_BURST
    D.LOKI_FS_V543 = M.LOKI_FS_V543 = master
    D.FS_V543_BURST = M.FS_V543_BURST = plank
    try:
        import siege
        siege.LOKI_FS_V543 = master
        siege.FS_V543_BURST = plank
        p = M.Player()
        ct = FakeCT(harv=harv)
        fires, opens, prev = [], [], 0
        for rnd, ti in enumerate(trace):
            ct.ti = ti
            o = p._v543_tick(ct, rnd)
            if o:
                opens.append(rnd)
            if p.v543_fires > prev:
                fires.append(rnd)
                prev = p.v543_fires
        return fires, opens, p
    finally:
        D.LOKI_FS_V543, D.FS_V543_BURST = old_m, old_p
        import siege
        siege.LOKI_FS_V543, siege.FS_V543_BURST = old_m, old_p


FAILS = []


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("  " + detail if detail else ""))
    if not cond:
        FAILS.append(name)


# --- 1. THE OPENING-ENDOWMENT TRAP.  Bank starts at 470 and stays high.
#        A level test fires at r0.  The arm-from-below latch must not.
flat = [470] * 60
f, o, _ = drive(flat)
check("opening endowment never fires", f == [], "fires=%r" % f)

# --- 2. POSITIVE CONTROL: the same trace with the latch pre-armed by a dip.
#        Falls to 100 (arms), climbs back over 200 with income rising.
dip = [470, 400, 300, 200, 150, 100, 100] + [100 + 20 * i for i in range(1, 20)]
f, o, p = drive(dip)
check("crossing from below fires", len(f) == 1, "fires=%r" % f)
check("window opens for FS_V543_WINDOW rounds",
      f and o[-1] - f[0] >= min(D.FS_V543_WINDOW, len(dip) - 1 - f[0]),
      "fire=%r last_open=%r" % (f, o[-1] if o else None))

# --- 3. NEGATIVE CONTROL A: the bank crosses 200 but is FALLING (eco spend
#        not saturated -- income is not outrunning spend).
fall = [80, 600, 560, 520, 480, 440, 400, 360, 320, 280, 240, 210, 205, 202]
f, o, p = drive(fall)
check("falling bank does not fire", f == [], "fires=%r spent=%d" % (f, p.v543_spent))

# --- 4. NEGATIVE CONTROL B: rising bank, but no harvesters (no income).
f, o, p = drive(dip, harv=0)
check("no harvesters does not fire", f == [], "fires=%r noharv=%d" % (f, p.v543_noharv))

# --- 5. RE-ARM: two separate crossings produce two windows.
two = ([470, 300, 150, 100] + [100 + 15 * i for i in range(1, 12)]  # cross 1
       + [100] * 60                                                  # fall back
       + [100 + 15 * i for i in range(1, 12)])                       # cross 2
f, o, p = drive(two)
check("two crossings, two windows", len(f) == 2, "fires=%r" % f)

# --- 6. MAX_FIRES cap.
many = []
for _ in range(D.FS_V543_MAX_FIRES + 3):
    many += [50] * 10 + [50 + 30 * i for i in range(1, 8)] + [260] * 45
f, o, p = drive(many)
check("MAX_FIRES caps the windows", p.v543_fires == D.FS_V543_MAX_FIRES,
      "fires=%d cap=%d" % (p.v543_fires, D.FS_V543_MAX_FIRES))

# --- 7. FLAG OFF: the master disarms everything and touches no state.
f, o, p = drive(dip, master=False)
check("master off never fires", f == [] and o == [] and p.v543_rnd == -1
      and p.v543_hist == [], "rnd=%d hist=%r" % (p.v543_rnd, p.v543_hist))
f, o, p = drive(dip, plank=False)
check("plank off never fires", f == [] and o == [] and p.v543_rnd == -1,
      "rnd=%d" % p.v543_rnd)

# --- 8. HISTORY DEPTH: a body born mid-game cannot fire on round 1 of its life.
late = [250] * 30            # already above threshold, never seen below
f, o, p = drive(late)
check("never-seen-below never arms", f == [] and not p.v543_armed)

print()
print("FAILURES: %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
