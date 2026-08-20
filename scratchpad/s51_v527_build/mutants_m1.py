#!/usr/bin/env python3
"""v527 M1 GUARD MUTANTS -- every guard on the bunker swap driven BOTH WAYS.

⛔ WHY IN-PROCESS AND NOT ON GAMES.  The deterministic game fixture
(`NOISE_ON=False` both sides, `--tle 0`) produced **0 bunker fires in 30 cells**
while the same tree fires 3-5 times in 24 NOISE_ON games -- the armed state is
reached 5,814 times there and the ECONOMY GATE refuses all 3,732 of the asks.
A mutant battery on that fixture would read 0 against 0 and "prove" nothing:
every arm would agree because none of them ever reaches the mutated line.
So the guards are driven directly, which is the only form in which a
NEGATIVE arm can be distinguished from an UNREACHED one.

THE STANDARD THIS MEETS (CLAUDE.md, Instruments): each guard is driven to BOTH
verdicts, per guard, per branch.  A guard that has only ever returned one answer
has not been seen to check.

  CONTROL      everything satisfied                       -> MUST FIRE
  MUT-GATE     `_fs_sentinel_ok` False (funded, gate shut) -> MUST NOT FIRE
  MUT-FUNDS    gate open, bank below cost+floor            -> MUST NOT FIRE
  MUT-MAG      gate open, funded, magazine empty           -> MUST NOT FIRE
  MUT-ARMED    gate open, funded, armed, but NOT trapped
               and collar wide open                        -> MUST NOT FIRE
  MUT-CAP      everything satisfied, per-body cap spent    -> MUST NOT FIRE
  MUT-NOSITE   everything satisfied, no adjacent barrier   -> MUST NOT FIRE
  MUT-NOFIRE   everything satisfied, `can_fire_from` False -> MUST NOT FIRE
  RESEAL       fires, but `can_build_sentinel` refuses on
               the freed tile -> the barrier MUST be back
               in the SAME turn (zero open-seat rounds)

Usage: .venv/bin/python3 scratchpad/s51_v527_build/mutants_m1.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bots/_v527collar"))

from fcode import Direction, EntityType, Position  # noqa: E402
import doctrine as D  # noqa: E402
from siege import SiegeMixin  # noqa: E402

# The body stands at (5,5).  Its EAST neighbour (6,5) carries OUR BARRIER --
# the swap candidate.  The enemy core footprint is at (8,5).
BODY = Position(5, 5)
BARRIER = (6, 5)
CORE = Position(8, 5)


class FakeCT:
    """Only the calls `_v527_bunker_swap` actually makes."""

    def __init__(self, **kw):
        self.ammo = kw.get("ammo", 100)
        self.ti = kw.get("ti", 1000)
        self.movecd = kw.get("movecd", 0)
        self.canmove = kw.get("canmove", False)
        self.has_barrier = kw.get("has_barrier", True)
        self.can_fire = kw.get("can_fire", True)
        self.can_build_sent = kw.get("can_build_sent", True)
        self.fwd_gun = kw.get("fwd_gun", 0)
        self.acts = []

    # --- reads
    def get_move_cooldown(self):
        return self.movecd

    def can_move(self, d):
        return self.canmove

    def get_global_ammo(self):
        return self.ammo

    def get_global_resources(self):
        return self.ti

    def get_sentinel_cost(self):
        return 30

    def get_barrier_cost(self):
        return 3

    def get_current_round(self):
        return 100

    def get_id(self):
        return 7

    def read_store(self, s):
        return self.fwd_gun

    def write_store(self, s, v):
        self.acts.append(("store", s, v))

    def get_tile_building_id(self, t):
        if (t.x, t.y) == BARRIER and self.has_barrier:
            return 99
        return None

    def get_team(self, bid):
        return "US"

    def get_entity_type(self, bid):
        return EntityType.BARRIER

    def get_nearby_buildings(self):
        return []

    def can_fire_from(self, bp, facing, kind, target):
        return self.can_fire

    # --- mutations
    def can_destroy(self, t):
        return True

    def destroy(self, t):
        self.acts.append(("destroy", (t.x, t.y)))

    def can_build_sentinel(self, bp, facing):
        return self.can_build_sent

    def build_sentinel(self, bp, facing):
        self.acts.append(("sentinel", (bp.x, bp.y)))

    def can_build_barrier(self, t):
        return True

    def build_barrier(self, t):
        self.acts.append(("barrier", (t.x, t.y)))


class Body(SiegeMixin):
    """A SiegeMixin with only what the swap touches."""

    def __init__(self, gate=True, floor=0):
        self.team = "US"
        self.mw = self.mh = 20
        self.enemy = CORE
        self.fs_sentinels = 0
        self.fs_my_sents = []
        self._gate = gate
        self._floor = floor

    # the collaborators the swap consults, stubbed at their own boundary
    def _fs_sentinel_ok(self, ct, ti, needed, orth_open):
        return self._gate

    def _v517_sent_floor(self, ct):
        return self._floor, 0

    def _fs_gun_axis(self, ct):
        return set()

    def _v527_defended(self, ct, bx, by):
        return False

    def _fs_draw_dot(self, *a):
        pass

    def _fs_draw_line(self, *a):
        pass


def attempt(name, body, ct, orth_open=0):
    fired = body._v527_bunker_swap(ct, CORE, BODY, 100, [], orth_open, ct.ti)
    kinds = [a[0] for a in ct.acts]
    return {
        "name": name, "returned": bool(fired),
        "sentinel": "sentinel" in kinds,
        "destroyed": "destroy" in kinds,
        "barrier_back": "barrier" in kinds,
        "acts": ct.acts,
    }


def main():
    assert D.LOKI_FS_V527 and D.FS_V527_BUNKER, "plank is off; nothing to test"
    rows, ok = [], True

    # CONTROL -- trapped, gate open, funded, magazine full
    rows.append(attempt("CONTROL", Body(gate=True),
                        FakeCT(ammo=100, ti=1000), orth_open=0))
    # each guard driven to its REFUSING value, everything else at CONTROL
    rows.append(attempt("MUT-GATE", Body(gate=False),
                        FakeCT(ammo=100, ti=1000)))
    rows.append(attempt("MUT-FUNDS", Body(gate=True, floor=0),
                        FakeCT(ammo=100, ti=10)))
    rows.append(attempt("MUT-MAG", Body(gate=True),
                        FakeCT(ammo=D.FS_V527_MAG_SHOTS * 10 - 1, ti=1000)))
    # not trapped AND collar wide open -> not armed
    rows.append(attempt("MUT-ARMED", Body(gate=True),
                        FakeCT(ammo=100, ti=1000, canmove=True),
                        orth_open=D.FS_V527_BUNKER_NEAR + 3))
    rows.append(attempt("MUT-NOSITE", Body(gate=True),
                        FakeCT(ammo=100, ti=1000, has_barrier=False)))
    rows.append(attempt("MUT-NOFIRE", Body(gate=True),
                        FakeCT(ammo=100, ti=1000, can_fire=False)))
    # per-body cap
    b = Body(gate=True)
    b.v527_bunker_n = D.FS_V527_BUNKER_MAX
    rows.append(attempt("MUT-CAP", b, FakeCT(ammo=100, ti=1000)))

    print("%-12s %8s %9s %10s %12s" %
          ("arm", "fired", "sentinel", "destroyed", "barrier_back"))
    for r in rows:
        print("%-12s %8s %9s %10s %12s" %
              (r["name"], r["returned"], r["sentinel"], r["destroyed"],
               r["barrier_back"]))

    ctl = rows[0]
    if not (ctl["returned"] and ctl["sentinel"] and ctl["destroyed"]):
        print("FAIL: the CONTROL did not fire -- the harness proves nothing")
        ok = False
    for r in rows[1:]:
        if r["returned"] or r["sentinel"] or r["destroyed"]:
            print("FAIL: %s fired or mutated the board" % r["name"])
            ok = False

    # THE FLICKER BOUND, driven as its own case: the build is refused on the
    # freed tile, so the barrier must be back in the SAME turn.
    print()
    rs = attempt("RESEAL", Body(gate=True),
                 FakeCT(ammo=100, ti=1000, can_build_sent=False))
    print("RESEAL   acts:", rs["acts"])
    if not (rs["destroyed"] and rs["barrier_back"] and not rs["sentinel"]):
        print("FAIL: the reseal fallback did not restore the barrier")
        ok = False
    else:
        print("RESEAL  PASS -- destroy then barrier, same turn, 0 open rounds")

    # ⭐⭐ THE HARNESS'S OWN FALSIFIER: break the plank, the CONTROL must flip.
    # ⛔ AND IT MUST BE PATCHED IN `siege`, NOT IN `doctrine`.  siege.py does
    # `from doctrine import *`, which BINDS the constants into siege's own
    # namespace at import; rebinding `doctrine.FS_V527_BUNKER` afterwards
    # changes nothing siege reads.  The first version of this falsifier did
    # exactly that and reported PLANK-OFF FIRED -- a HARNESS artefact, not a
    # bot defect (the shipped bot takes the value at import, so a doctrine
    # `False` really does gate it).  Recorded because a falsifier that fails
    # for its own reasons is worth exactly as little as one that never fails.
    import siege as S
    print()
    for flag in ("FS_V527_BUNKER", "LOKI_FS_V527"):
        was = getattr(S, flag)
        setattr(S, flag, False)
        neg = attempt("OFF:" + flag, Body(gate=True),
                      FakeCT(ammo=100, ti=1000))
        setattr(S, flag, was)
        print("%-22s fired: %s   (must be False)" % (flag + " = False",
                                                     neg["returned"]))
        if neg["returned"]:
            print("FAIL: %s does not gate the swap" % flag)
            ok = False

    print("\nRESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
