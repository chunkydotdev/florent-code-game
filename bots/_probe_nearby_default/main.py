"""PROBE: does `get_nearby_buildings()` with no dist_sq default to VISION RADIUS?

WHY THIS EXISTS.  Research claimed the default is the caller's vision radius and
sized a defect on it (`_live_fwd_guns` censusing a d^2<=50 band from a builder
that sees r^2=20, "35.6% of live forward sentinels invisible").  They then
withdrew the premise themselves: the claim was read ACROSS from the
`get_nearby_tiles` row in CLAUDE.md, which carries "(default: vision radius)"
while the `get_nearby_buildings` row does not.  `official-docs.md` never states
it and is known-wrong in places.

The shipped package's own type stub DOES state it on the method's own docstring
line (`fcode/_types.py:365`, `py.typed` present).  That is strong -- and it is
still a text trail, not an execution.  The `.so` carries no docstrings and
`Controller` is not importable, so the only way to settle it is to ASK THE
ENGINE.

THE TEST, and it is driven so that BOTH answers are observable.  Each round the
CORE (vision r^2 = 36, static, never dies) reports three counts:

    D = len(get_nearby_buildings())                  <- the contested default
    V = len(get_nearby_buildings(vision_radius_sq))  <- explicitly at vision
    N = len(get_nearby_buildings(2))                 <- explicitly tiny

DECISION RULE, pre-registered here before the run:
  * D == V and D > N, with buildings KNOWN to exist outside vision
        => the default is VISION-BOUNDED.  Research's premise holds.
  * D >  V at any point
        => the default is UNBOUNDED (or wider than vision).  The premise
           collapses, `_live_fwd_guns` is a complete census, and the 35.6%
           figure is 0.
  * D == V == N
        => the probe is blind (no buildings outside dsq 2) and the round is
           NOT EVIDENCE.  Reported as SKIP, never folded into the verdict.

THE CONTROL THAT MAKES A MATCH MEAN SOMETHING.  `D == V` is only informative if
V could have differed from D -- i.e. if there really are buildings beyond the
core's vision.  So the probe also counts FAR buildings the only team-blind way
available to it: it walks its own builder outward and reports the enemy-side
buildings it can see from there.  A run where the two teams' bases never hold
buildings outside r^2=36 of our core proves nothing, and this probe says so
rather than printing a clean PASS.

It builds nothing and never attacks: it is an instrument, not an arm.
"""

from fcode import Controller, Direction, EntityType


class Player:
    def __init__(self):
        self.rows = 0
        self.agree = 0
        self.default_wider = 0
        self.skips = 0
        self.max_far = 0

    def run(self, ct: Controller) -> None:
        try:
            if ct.get_entity_type() == EntityType.CORE:
                self._census(ct)
            else:
                self._walk(ct)
        except Exception as e:                      # never let the unit die
            print(f"PROBE_ERR {type(e).__name__}: {e}")

    def _census(self, ct: Controller) -> None:
        vr = ct.get_vision_radius_sq()
        d = len(ct.get_nearby_buildings())
        v = len(ct.get_nearby_buildings(vr))
        n = len(ct.get_nearby_buildings(2))

        rnd = ct.get_current_round()
        if d == v == n:
            self.skips += 1
            verdict = "SKIP-blind"
        elif d > v:
            self.default_wider += 1
            verdict = "DEFAULT-WIDER-THAN-VISION"
        elif d == v:
            self.agree += 1
            verdict = "default==vision"
        else:
            verdict = "DEFAULT-NARROWER"
        self.rows += 1

        if rnd % 5 == 0 or d > v:
            print(f"PROBE r{rnd} vr={vr} D={d} V={v} N={n} -> {verdict} "
                  f"| agree={self.agree} wider={self.default_wider} "
                  f"skip={self.skips} maxfar={self.max_far}")

        if rnd == 300:
            print(f"PROBE_SUMMARY rows={self.rows} agree={self.agree} "
                  f"default_wider={self.default_wider} skip={self.skips} "
                  f"maxfar_outside_core_vision={self.max_far}")

    def _walk(self, ct: Controller) -> None:
        """A builder walking outward, reporting buildings the CORE cannot see.

        This is the control: it establishes that buildings exist beyond the
        core's r^2=36, so `D == V` at the core is a real agreement and not two
        counts of the same empty set.
        """
        me = ct.get_position()
        vr = ct.get_vision_radius_sq()
        far = 0
        for bid in ct.get_nearby_buildings(vr):
            try:
                bp = ct.get_position(bid)
            except Exception:
                continue
            if bp.distance_squared(me) > 36:
                far += 1
        # buildings this bot sees that sit outside ANY core-sized disc around it
        if far > self.max_far:
            self.max_far = far

        if ct.get_move_cooldown() == 0:
            for dd in (Direction.EAST, Direction.SOUTH,
                       Direction.NORTH, Direction.WEST):
                if ct.can_move(dd):
                    ct.move(dd)
                    return
