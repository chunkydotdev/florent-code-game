---
tactic: (A) THE MECHANICS OF FINISHING — two independent StarCraft bots encode target selection as an ordered fallback chain over REMEMBERED buildings, terminating in "explore until we find something"
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/CombatCommander.cpp
origin: Steamhammer and UAlbertaBot (StarCraft AI)
evidence: documented
transfers: partial
---
WHAT IT IS — Both bots answer "where do we attack" with a numbered priority chain,
written out as comments in the source. Steamhammer's, in `getAttackLocation`:

```
    // 1. If we haven't been able to attack, look for an undefended target on the ground, either
    // 2. Attack the enemy base with the weakest defense.
    // 3. Attack known enemy buildings.
    // 4. Attack visible enemy units.
    // 5. Attack the remembered locations of unseen enemy units which might still be there.
    // 6. We can't see anything, so explore the map until we find something.
```

UAlbertaBot's, in `getMainAttackLocation`, is the same chain shorter:

```
    // First choice: Attack an enemy region if we can see units inside it
    // Second choice: Attack known enemy buildings
    // Third choice: Attack visible enemy units that aren't overlords
    // Fourth choice: We can't see anything so explore the map attacking along the way
```

Three properties are worth naming. **Buildings outrank units** in both. **The chain
runs on memory, not vision** — UAlbertaBot's "second choice" iterates remembered
`UnitInfo` records and returns `ui.lastPosition` for the first that
`ui.type.isBuilding()`. And **the terminal case is a search**, not a hold:
UAlbertaBot's final fallback returns `Global::Map().getLeastRecentlySeenTile()`.

Steamhammer also carries a note beside its building rule that is entirely about the
finishing problem:

```
    // We assume that a terran can lift the buildings; otherwise, the squad must be able to attack ground.
```

WHY IT MIGHT TRANSFER — Partly, and it is worth being precise about which part,
because the obvious reading does not apply.

**The chain itself does not transfer.** Our win condition is a single 2×2 building
whose position is known from map symmetry in round 0. We do not have a "find the
last enemy remnants" problem; we have a "the target is well defended" problem. Six
priority levels for locating an objective are six levels we do not need.

**Two narrower things do transfer.**

First, **buildings outrank units, and memory outranks vision.** Our engine has no
enemy-unit memory at all — every getter is unit-scoped and live, and our only
persistent shared state is 16 integers. The field's converters all maintain a
remembered map of enemy *structures* and attack that. Our version is small and
already half-built: the library's `turret-threat-field` and `runtime-density-siting`
files hold the coverage side, and the builder's live code already puts turret tiles
in `blocked` in `_bfs_direction`. What is missing is the **positive** use — a
remembered target list, not just a remembered hazard list.

Second — and this is the one that pays — **the tiebreak-relevant analogue of
"hunt the last buildings" exists here and is unexploited.** Key 2 is harvesters
alive, a comparison. Harvesters sit on ore tiles, which are fixed terrain and
therefore enumerable from `get_tile_env` without any memory system at all. A
Steamhammer-style chain over *enemy harvester sites* is cheap, and unlike a core
assault it improves a tiebreak key we can actually reach. That is the
[`deny-production-not-units`](deny-production-not-units.md) target list, made
concrete.

WHAT WOULD KILL IT — The chain exists because StarCraft has fog of war over a large
map with liftable buildings and island bases. Our maps are 8×8 to 30×30, the core
is at the symmetric image of ours, and nothing moves except builder bots. The
problem the chain solves largely does not exist here, which is why this is
`partial` — the transferable residue is the *ordering principle* and the harvester
list, not the chain.

The memory point is also bounded hard by our engine: 16 unsigned integers, buffered
one round, **last writer wins**, and the read-increment-write idiom collapses
silently. Any remembered-target list must fit in a handful of slots with a
single designated writer. A list of "all enemy buildings" does not fit; a list of
"the two ore tiles we are denying" does.

BUILDER HOOK — Enumerate enemy-side ore tiles once at spawn from `get_tile_env`
(they are fixed and symmetric, so this is a one-time cost), publish two of them to
store slots as the current denial targets with one designated writer, and have idle
builders prefer them. That is the smallest version of "attack known enemy
buildings" this engine can hold, and unlike a core assault it is scored by a
tiebreak key.
