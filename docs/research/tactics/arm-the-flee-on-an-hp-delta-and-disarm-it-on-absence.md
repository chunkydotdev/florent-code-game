---
tactic: Arm the forward unit's flee on an HP DELTA (I lost HP since last turn), disarm it on the absence of a threat — never on an HP threshold
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ScoutManager.cpp
origin: Steamhammer (Jay Scott), Brood War AI — `ScoutManager::drawScoutInformation`/`moveGroundScout`
evidence: documented
transfers: yes
---

## WHAT IT IS

Steamhammer's forward worker does **not** flee at a health fraction. It flees on
the *derivative*:

> ```
> if (scoutHP < _previousScoutHP)
> ```
> ```
> _scoutUnderAttack = true;
> ```

and it stops fleeing on a **different, event-shaped** condition:

> ```
> if (!_workerScout->isUnderAttack() && !enemyWorkerInRadius())
> ```

**Referent check.** `scoutHP` is `_workerScout->getHitPoints() + _workerScout->getShields()`
recomputed each frame and then stored into `_previousScoutHP`; the disarm block
sets `_scoutUnderAttack = false`. `enemyWorkerInRadius()` returns true for an
enemy worker within 300 pixels of the scout. So: **armed by damage taken, cleared
only when nothing is currently hitting it and no enemy worker is near** —
an arm/disarm pair on two different signals, which this library already has a
file for in the general case
([`arm-and-disarm-on-different-thresholds`](arm-and-disarm-on-different-thresholds.md)).

Separately, the *forward work* has an absolute floor, not a fraction:

> ```
> _workerScout->getHitPoints() + _workerScout->getShields() > 20
> ```

That gates harassing an enemy worker. Below 20 the unit keeps circling the enemy
base — it does **not** go home. **The health term governs which forward job it
does, not whether it stays forward.**

## WHY IT MIGHT TRANSFER — and note that we have already built the primitive, on the wrong unit

`bots/_v135loki18/main.py:99,176-178` already carries exactly this construct:

```
self.last_hp = None
...
if self.last_hp is not None and hp < self.last_hp:
    under = True
self.last_hp = hp
```

It sits under a comment reading `--- Core-only accounting ---` and feeds
`SLOT_UNDER`, i.e. **it is wired to the core as a defensive latch and is not
available to the raider.** The per-unit `Player` instance evidently persists
across rounds (the same class also keeps `self.raid_stalls`), so the mechanism
costs three lines on the builder path and no store slot.

Why the delta beats a threshold *here specifically*: a builder has 40 HP, a
gunner does 7 and a sentinel 18. A sentinel hit is 45% of the unit in one round.
**A fractional threshold is sampled too coarsely to be a useful trigger at that
damage granularity** — by the time an `hp < 0.5 * max_hp` test fires, the second
shot decides the outcome, not the branch. A delta fires on the *first* shot, and
it identifies something a threshold cannot: **that a turret has line on this
tile**, which is a fact about the tile and worth writing down.

## WHAT WOULD KILL IT

* **Healing makes the delta noisy in both directions.** A friendly heal (+4) can
  mask a gunner shot (−7) within one round; the sign of the delta is then a
  statement about the *net*, not about incoming fire. Steamhammer has no
  equivalent because Brood War workers are not healed mid-scout.
* If the `Player` instance is ever per-team rather than per-unit, `self.last_hp`
  is being written by every unit in turn and the comparison is garbage. The
  incumbent's use of it suggests per-unit, **but this is worth one probe before
  it is trusted on the raider** — the incumbent's use is on the core, of which
  there is exactly one, so it cannot distinguish the two cases.

## BUILDER HOOK

Move the three lines from the core branch to the builder branch and let the
raider set a per-unit `hit_this_round` flag. **Do not attach a retreat to it
yet** — the first use is to mark the tile as covered by a turret and pick a
different adjacent build target, per
[`the-forward-unit-is-excluded-from-the-go-home-branch`](the-forward-unit-is-excluded-from-the-go-home-branch.md).
