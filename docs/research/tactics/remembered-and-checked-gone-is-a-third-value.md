---
tactic: (A) THE OTHER HALF OF THE ANSWER TO (A) — the StarCraft bots that DO remember mutable things all invented the same extra value: "I went back and looked, and it was not there". PurpleWave carries six visibility states including a purely hypothetical one. But this is the family our engine can least afford
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/UnitData.h
origin: Steamhammer (Jay Scott, BWAPI), UAlbertaBot (Dave Churchill), PurpleWave (Dan Gant — 1st SSCAIT 2018-19 and 2019-20)
evidence: documented
transfers: partial
---
WHAT IT IS — Battlecode's winners
[refuse to remember anything mutable](the-winner-stored-a-tri-state-and-resolved-unknown-two-ways.md).
The StarCraft family does the opposite, and the interesting part is the vocabulary it needed
to do it safely.

**Steamhammer's remembered-unit struct carries the timestamp AND an explicit "checked, gone"
flag** (`Steamhammer/Source/UnitData.h:7-19`, verbatim, tabs as in source):

```cpp
struct UnitInfo
{
    // Keep track of units which are out of sight.

    int             unitID;
    int				updateFrame;
    int             lastHP;
    int             lastShields;
    BWAPI::Player   player;
    BWAPI::Unit     unit;
    BWAPI::Position lastPosition;
    bool			goneFromLastPosition;   // last position was seen, and it wasn't there
    bool			burrowed;               // believed to be burrowed (or burrowing) at this position
```

`goneFromLastPosition` is set **only on re-observation** — the fog never promotes to "gone".
And the code documents the error it knowingly accepts (`UnitData.cpp:321-325`):

```cpp
        // It may have burned down, or the enemy may have chosen to destroy it.
        // Or it may have been destroyed by splash damage while out of our sight.
        // NOTE A terran building could have lifted off and moved away while out of our vision.
        //      In that case, we mistakenly drop it.
        //      Not a serious problem; we'll re-add it when we see it again.
```

**UAlbertaBot, the ancestor Steamhammer forked, has neither field** — its `UnitInfo`
(`UAlbertaBot/Source/UnitData.h:12-20`) is `unitID`, `lastHealth`, `lastShields`, `player`,
`unit`, `lastPosition`, `type`, `completed`, and **no timestamp at all** (verified by reading
the whole struct). So the timestamp is Steamhammer's addition, not the family baseline.

**PurpleWave goes furthest: six named states, one of which was never observed at all**
(`src/ProxyBwapi/UnitTracking/Visibility.scala`, the complete file, verbatim):

```scala
package ProxyBwapi.UnitTracking

object Visibility extends Enumeration {
  val
    Visible,
    InvisibleBurrowed,
    InvisibleNearby,
    InvisibleMissing,
    Hypothetical,
    Dead
    = Value
}
```

WHY IT MIGHT TRANSFER — partially, and the boundary is sharp.

- **The vocabulary is right and we currently lack it.** "Never seen", "seen and remembered",
  "went back and it was gone" are three genuinely different states, and a bot that collapses
  the third into the first will re-scout forever. For the Loki line the relevant instance is
  the enemy core: *found at P* and *checked P, not there* must be distinguishable, or a raid
  re-targets a cleared location.
- **`Hypothetical` is the state our
  [symmetry plank](symmetry-is-the-only-free-information-about-the-unseen-map.md) produces**,
  and PurpleWave names it as a first-class member of the same enum as `Visible`. That is the
  design precedent for treating a *predicted* enemy core position as a real entry in the
  model rather than a special case.
- **The "accepted error, documented in a comment" discipline is directly usable.** Our
  equivalent: a remembered enemy building may have been destroyed by its own team, or built
  over. Writing down which errors we accept is free and is what stops a repair loop from
  chasing them.

WHAT WOULD KILL IT — and this is most of the file:

- **The cost model that makes this affordable in StarCraft does not exist here.** BWAPI
  hands the bot a persistent per-player `UnitData` object shared by the whole AI. **We have
  no such thing:** [module-level state is not shared between our units](the-sixteen-ints-really-are-the-only-channel.md),
  so every builder would keep its own `goneFromLastPosition` table and none of them could
  tell the others. A "gone" fact learned by the builder that walked there **cannot be
  published** except as bits in 16 ints, one round late.
- **And the unit that learned it usually dies.** In our game the thing that goes and looks
  is a 40 HP builder in the enemy half. StarCraft scouts survive to report; ours frequently
  do not, so the memory's expected lifetime is short and the reconciliation problem is
  unsolvable with our channel.
- **Steamhammer's staleness reasoning is written for a real-time game with frame counts and
  unit production estimates** (`completeBy`, `isCompleted()` predicting completion by
  extrapolation). Porting the *reasoning* would be a large build for a currency the
  programme does not price. **Port the vocabulary, not the machinery.**
- **PurpleWave's placings are for StarCraft tournaments, not a Battlecode-like league**, and
  none of the three sources gives an ablation showing the remembered-unit layer was worth
  anything. `transfers: partial` rests on the design argument, not on measured value.

BUILDER HOOK — one value, not a system: give the enemy-core belief three states —
`UNKNOWN`, `PREDICTED(pos)` (from symmetry), `CLEARED(pos)` (a friendly unit had `pos` in
vision and no enemy core was there) — and spend **one store slot** publishing which
prediction index has been cleared. That is the minimum that stops two raids walking to the
same empty corner, and it is testable as `time_to_core_kill` on the maps where the first
prediction is wrong.
