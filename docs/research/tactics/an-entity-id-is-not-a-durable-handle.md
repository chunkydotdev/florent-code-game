---
tactic: Three independent leagues converged on the same rule — a handle to a thing you saw stops resolving the moment you stop seeing it, so you must COPY the fields you need at sighting time. Measured on our engine: EVERY id-taking getter raises once the entity leaves vision, including for your own core
source: https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/UnitData.h
origin: UAlbertaBot (Dave Churchill, BWAPI/AIIDE); BWAPI itself; MIT Battlecode 2025 engine API
evidence: documented
transfers: yes
---
WHAT IT IS — the rule is written as a two-line comment at the top of UAlbertaBot's
remembered-unit struct, `UAlbertaBot/Source/UnitData.h:7-10`, verbatim:

```cpp
struct UnitInfo
{
    // we need to store all of this data because if the unit is not visible, we
    // can't reference it from the unit pointer
```

The struct then stores `unitID`, `lastHealth`, `lastShields`, `player`, `lastPosition`,
`type`, `completed` — flat copies, not a pointer chase. **The referent of "the unit
pointer" is the `BWAPI::Unit unit;` field declared four lines below the comment**, and
BWAPI's own header says why it cannot be dereferenced
(`bwapi/include/BWAPI/Unit.h:72-73`):

> *"@retval true If the unit exists on the map and is visible according to BWAPI."*
> *"@retval false If the unit is not accessible or the unit is dead."*

Battlecode states the same contract as a throw
(`battlecode25/engine/.../RobotController.java:231-232`, javadoc lines):

```java
     * @throws GameActionException if the robot cannot be sensed (for example,
     *                             if it doesn't exist or is out of vision range)
```

WHY IT MIGHT TRANSFER — **it is not a maybe. I measured our engine and it is the harshest
of the three.** `bots/_probe_oov_surface`, `maps/eider.map26`, seed 1: a builder records its
own core's id at round 1 while adjacent to it, then walks away. Every id-taking getter is
called under an individual guard at rounds 3, 25 and 60.

| round | builder position | `get_position(core_id)` | `get_hp` | `get_entity_type` | `get_team` | `get_max_hp` |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | (7,8), core at (7,9) | `Position(x=7, y=9)` | `500` | `CORE` | `Team.A` | `500` |
| 25 | (27,10) | **RAISE** | **RAISE** | **RAISE** | **RAISE** | **RAISE** |
| 60 | (27,19) | **RAISE** | **RAISE** | **RAISE** | **RAISE** | **RAISE** |

All raise `GameError: Entity out of vision range`. The r3 row is the positive control: the
same five calls on the same id return values when the entity is in sight, so the r25/r60
column is the check firing, not a dead call. Four builders on both teams, identical result.

**Three consequences that bind the Loki line directly:**

1. **`get_max_hp(id)` and `get_entity_type(id)` raise too.** These are *immutable* facts
   about an entity — the engine still refuses them. So there is no "safe subset" of id
   queries. **The id is worthless outside vision, full stop.**
2. **It applies to your OWN units, including your own core.** A raider that walks toward
   the enemy and then asks "where is home" dies. Any route-home or fallback logic must
   carry the core's `Position` as a value captured at spawn, never an id.
3. **It is the mechanism behind the sweep's headline number.** 7.08% of our graph walks
   exceed a builder's r²=20. A walk that resolves neighbours by id is not 7.08% wrong —
   it is 7.08% *fatal*, and the unit is gone for the rest of the match.

So the enemy core, once found, must be recorded as **coordinates**, and there is no way to
ask whether it is still there without sending something to look.

WHAT WOULD KILL IT —

- **Nothing about the measurement**; it is the shipped engine at `fcode` 2.3.6. What it
  does not tell you is whether the raise is per-unit-vision or per-team-vision. It is
  per-unit: builder 3 at (7,8) resolved its core while builder 4 at (19,8) — the mirrored
  enemy builder, same distance from *its* core — also resolved. Neither could see the
  other's.
- **The BWAPI comparison is weaker than it looks and I should not oversell it.** BWAPI
  returns `false` from `exists()`; it does not crash. Battlecode throws a catchable
  exception that costs 500 bytecodes. **Ours destroys the unit permanently.** The
  *representation* lesson transfers; the *severity* does not, and ours is worse.

BUILDER HOOK — a grep-checkable invariant, not a behaviour change: **no id may be stored on
`self` across turns.** Store `Position` and `EntityType` captured at sighting time instead.
The test is `grep -n "self\..*_id\b" bots/_v127loki10/*.py` returning nothing that survives
a turn boundary — and the falsifier is the r25 row above: if any stored id is read while
the entity is out of vision, that unit dies and the death shows up as a full-HP unit loss
in `docs/research/undamaged-builder-deaths-2026-08-10.md`.
