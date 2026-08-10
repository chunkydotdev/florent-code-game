---
tactic: (C) THE OBSERVATION-SIDE ABORT RULE — a remembered target is retracted ONLY when the unit can currently see its tile and the target is not there. Absence of evidence never retracts; evidence of absence always does. Two independent StarCraft bots implement exactly this, and both give IMMOBILE targets no decay term at all
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/UnitData.cpp
origin: Steamhammer (StarCraft AI, Jay Scott / UAlbertaBot lineage); PurpleWave (StarCraft AI, dgant)
evidence: documented
transfers: yes
---

## WHAT IT IS

The sweep asked for the observation side of aborting: *absence of evidence vs evidence of
absence*. Two long-lived StarCraft bots answer it identically, in code, and the answer is
the strong one — **only a LOOK retracts a belief.**

**Steamhammer.** The flag is named for the thing it means, and the function header states
the rule as a biconditional:

> *"// An enemy unit which is not visible, but whose lastPosition can be seen, is known"*
> *"// to be gone from its lastPosition. Flag it."*

**Referent check.** *"An enemy unit"* is any entry in the enemy `UnitData` map — Steamhammer
remembers every enemy unit it has ever seen; *"its lastPosition"* is the position stamped on
that remembered entry the last frame the unit was visible. The comment names the exact
conjunction: **not visible, AND its remembered tile IS visible.** The implementing line is
that conjunction and nothing else:

> *"else if (BWAPI::Broodwar->isVisible(BWAPI::TilePosition(ui.lastPosition)) && !ui.burrowed)"*
> *"ui.goneFromLastPosition = true;"*

**There is no age term in that condition.** The same rule is restated at the call site:

> *"// If we can see the last known location of a remembered unit and the unit is not there,"*

**And the belief is CONSUMED by the engage decision, not merely displayed.** Steamhammer's
force count for the combat simulator iterates remembered units and filters on exactly one
belief predicate:

> *"!ui.goneFromLastPosition &&"*

**Referent check.** That line is one conjunct of the filter inside
`InformationManager::getNearbyForce`, whose own comment is *"// Only returns units expected
to be completed."*; the surrounding conjuncts are `UnitUtil::IsCombatSimUnit(ui)`,
`ui.isCompleted()` and `ui.powered`. So a unit last seen 3 minutes ago, on a tile nobody has
looked at since, is **counted as present at its remembered position** when deciding whether
to fight.

**PurpleWave, independently, and it separates the mobile case from the immobile case
explicitly.** Its belief module is `Imagination.scala`, a six-state lattice
(`Visible, InvisibleBurrowed, InvisibleNearby, InvisibleMissing, Hypothetical, Dead`). The
building branch is the one that matters to us:

> *"// Buildings that can't move are either in the same place or dead"*
> *"unit.changeVisibility(?(shouldBeVisible, Visibility.Dead, Visibility.InvisibleNearby))"*

**Referent check.** `?(cond, a, b)` is PurpleWave's inline ternary (`Utilities.?`), so this
reads: *if the building's tiles are currently visible, it is Dead; otherwise it is
InvisibleNearby* — i.e. still believed to be exactly where it was. `shouldBeVisible` is
defined earlier in the same function and, for buildings, is footprint-wide, not anchor-tile:

> *"unit.tiles.exists(_.visible),"*

**An immobile target in PurpleWave has NO decay path whatsoever.** The only route from
"remembered building" to `Dead` is looking at one of its tiles and not finding it. The
timeout that exists elsewhere in the same function is explicitly not applied to it:

> *"// Assume units we haven't seen in a very long time are dead"*

is gated by `expectedSurvivalFrames`, whose default arm is

> *"else                                Forever()"*

## WHY IT MIGHT TRANSFER

**Every target our programme cares about is an immobile building.** The enemy core is a
fixed 2x2 footprint; harvesters sit on ore; conveyors, splitters, barriers, gunners,
sentinels and launchers are all buildings and all immovable. Builder attacks can only damage
buildings at all (2 Ti → 2 dmg, orthogonally adjacent). So **PurpleWave's building branch is
not one case of the rule for us — it is the whole rule**, and its decay term is `Forever()`.

- **It is nearly free to implement, and it needs no store slot.** The belief lives on the
  `Player` instance keyed by `ct.get_id()`: `self._believed = {(x, y): kind}`. Retraction is
  one test per round over the tiles the unit can actually see, which it is already
  enumerating via `get_nearby_tiles()`.
- **It is the correct default for the one query our engine punishes.** Our own instrument
  (`docs/game-model.md`, measured 2026-08-08) records that `get_tile_env()`,
  `is_tile_passable()` and `get_tile_building_id()` **raise `GameError: Position out of
  vision range`** for an in-bounds tile the caller cannot see, with the same message as a
  genuinely off-map position — *"so the engine does not let you tell the two apart"*.
  A `try/except` around a re-query is therefore **not** an observation — it tells you nothing
  about the world, only about your own vision. Steamhammer's rule says the `except` branch
  must leave the belief untouched. Our repo has measured what the other choice costs:
  `undamaged-builder-deaths-2026-08-10.md` shows a synthetic arm where an uncaught
  out-of-vision `get_tile_env()` removed the builder in **96/96** cases.
- **It converts the abort question into a cheap, local one.** "Should I turn around?" becomes
  "am I standing where I can see the tile, and is it empty?" — answerable from the executing
  unit's own getters, which is the constraint
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md)
  says every exit predicate must satisfy.

## WHAT WOULD KILL IT

- **Our targets are immobile but they are not immortal, and they are also RE-BUILDABLE.**
  StarCraft buildings do not respawn on the same tile mid-fight; ours do — `destroy()` is
  free and unlimited, and a defender can tear down and rebuild a turret on the same seat.
  So `Dead`-on-sight is correct, but a **`Dead` belief must itself be retractable on a later
  look**, which neither source needs. A one-way lattice would blind us to a rebuilt turret.
- **The core is the exception that makes the rest almost pointless.** A 2x2, 500 HP,
  never-moving, never-rebuilt core has a belief that is correct from round 0 forever. If the
  only target we commit to is the core, this file's machinery buys nothing over a constant —
  see the moot-ness argument in
  [`the-symmetry-candidate-set-is-the-commit-rule`](the-symmetry-candidate-set-is-the-commit-rule.md).
  Its value is entirely in the *secondary* targets: harvesters, conveyor lines, forward
  turrets — the things a Loki raid actually chews on when the core is walled.
- **Neither source measured this in isolation.** Both are shipped designs inside large bots;
  no ablation is reported. Evidence is `documented` for the design, not for a win delta.
- **Steamhammer only checks every 6th frame** (*"if (the.now() % 6 == 5)"*). Its stated
  grounds are a numbered comment list whose second item argues from the target's MOBILITY —
  the source line is split across two `//` continuation lines, so it is given here as two
  adjacent verified fragments with the join stated, not smoothed into one string:
  *"// 2. If the unit has only been gone from its location for a short time, it probably"*
  + *"//    didn't go far (though it might have been recalled or gone through a nydus)."*
  **That argument does not apply to buildings**, so their lazy sampling rate is not a
  precedent for sampling lazily here.

## BUILDER HOOK

Smallest test, and it is an instrument before it is a behaviour: give the raider a
per-unit dict of remembered enemy buildings, written on sight from `get_nearby_buildings()`,
and retracted **only** when the unit is currently seeing that tile and finds it gone. Then
`print()` two counters once per 100 rounds — `beliefs_held` and `beliefs_retracted_by_look`
— plus the count of rounds the unit spent walking toward a belief it later retracted. **If
retraction-by-look almost never fires, the whole belief layer is dead weight and the road
closes for the price of a print.** Only if it fires often is there a target worth
re-selecting on.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/UnitData.cpp
- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/InformationManager.cpp
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/ProxyBwapi/UnitTracking/Imagination.scala
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/ProxyBwapi/UnitTracking/Visibility.scala

Every quoted string above was verified verbatim by literal `grep -F` against the primary
source text during tactics sweep 20C (2026-08-10 04:11 UTC, repo HEAD `a08669c`). Quotes
from our own repo are cited to file and are internal measurements, not external sources.
