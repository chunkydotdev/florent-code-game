---
tactic: The ancestor's API SILENTLY CLAMPS a too-large sense radius down to vision; ours RAISES. Any code ported from a Battlecode idiom that passes a generous radius "to be safe" is a unit-killer here, and it is the one difference most likely to be copied wrong
source: https://raw.githubusercontent.com/battlecode/battlecode25/master/engine/src/main/battlecode/common/RobotController.java
origin: MIT Battlecode 2025 engine API (`battlecode/battlecode25`, `master`) vs. the Florent Code League engine (`fcode` 2.3.6), measured
evidence: documented
transfers: no
---
WHAT IT IS — Battlecode's bulk-sense methods take a radius and defensively clamp it.
Verbatim, `engine/src/main/battlecode/common/RobotController.java:250-260` (javadoc lines;
the sentence is split across lines by `*` markers so it is reproduced with its own breaks):

```java
     * @param radiusSquared return robots this distance away from the center of
     *                      this robot; if -1 is passed, all robots within vision
     *                      radius are returned;
     *                      if radiusSquared is larger than the robot's vision
     *                      radius, the vision
     *                      radius is used
     * @return array of RobotInfo objects of all the robots you saw
     * @throws GameActionException if the radius is negative (and not -1)
```

**The only way to make it throw is a NEGATIVE radius.** Overshooting is free and documented
as free. So the safe Battlecode idiom is "ask for everything, let the engine clamp".

**On our engine that idiom kills the unit.** Measured, `bots/_probe_oov_surface`,
`maps/eider.map26`, seed 1, four builders (vision r²=20), each call individually guarded:

| call | result |
| --- | --- |
| `get_nearby_tiles(vr)` *(vr == `get_vision_radius_sq()` == 20)* | `OK` — 69 tiles |
| `get_nearby_tiles(vr + 1)` | **`GameError: dist_sq exceeds vision radius`** |
| `get_nearby_tiles(9999)` | **`GameError: dist_sq exceeds vision radius`** |
| `get_nearby_entities(9999)` | **`GameError: dist_sq exceeds vision radius`** |

The first row is the positive control: the boundary value is legal and returns a real
count, so `vr + 1` failing is the check firing at exactly the boundary, not the call being
broken.

WHY IT DOES NOT TRANSFER — **filed `transfers: no` because the tactic itself is a trap here,
and that is the useful result.** The reason to record it is that it is the single most
plausible way a well-intentioned port introduces a fatal bug:

- **Overshooting reads as defensive programming.** `get_nearby_tiles(9999)` looks like
  "give me everything you have" and in the ancestor league it *is* that. Here it is
  indistinguishable, at the call site, from a correct call — and it destroys the unit
  permanently.
- **It is worse than the tile queries because there is no mask for it.**
  `is_in_vision(pos)` guards the whole `get_tile_*` family
  ([legality mask](the-legality-mask-is-a-total-function.md)). There is **no** total
  predicate for "is this `dist_sq` acceptable" — you must compare against
  `get_vision_radius_sq()` yourself, and different unit types have different values
  (core r²=36, builder r²=20, gunner r²=13, sentinel r²=32, launcher r²=26). **A constant
  works for one unit type and kills another.**
- **The default argument is the safe one and should be the only one used.**
  `get_nearby_tiles()` with no `dist_sq` defaults to the vision radius, which is what the
  clamping behaviour would have given anyway.

WHAT WOULD KILL IT — nothing; it is measured on the shipped engine. The one caveat is that
I probed only builder bots (r²=20). The failure is on `dist_sq > get_vision_radius_sq()`, so
it should hold for every unit type, but the core (r²=36) and turrets are untested and a
hardcoded `20` would be wrong for them in the *other* direction — silently reading less
than they can see, which is a bug that does not announce itself.

BUILDER HOOK — a grep, not a feature: **no literal integer may be passed to
`get_nearby_tiles` / `get_nearby_entities` / `get_nearby_buildings` / `get_nearby_units`.**
Either omit the argument, or pass `min(want, ct.get_vision_radius_sq())`. Add it to the same
preflight check that catches `finally`
([load-time lint](the-finally-that-battlecode-relies-on-does-not-load-here.md)) — both are
static, both are cheap, and both fail in ways no ladder game will attribute correctly.
