---
tactic: A commit trigger needs three parts — an arm condition, a separate disarm condition, and a cohesion precondition
source: https://shummie.github.io/Halite-2-Shummie/
origin: Halite II, Shummie (3rd place) — the most explicitly specified engagement trigger found in any league
evidence: documented
transfers: yes
---

## WHAT IT IS

Shummie's bot carries a global boolean, `rush_mode`, and the postmortem publishes the exact
conditions that set and clear it. It is the closest thing in any comparable league to a
complete, quotable answer to *"what was in the trigger?"*.

**Arm (2-player), three conditions ANDed:**

> *"If it’s been less than 16 turns, the enemy has no docked ships, then look at the distance
> between each of our ships and each enemy ships. If it’s less than 11 * MAX_SPEED away, we
> activate rush mode."*

**Referent check.** *"docked"* means committed to economy — a docked Halite II ship mines and
cannot fight. So condition 2 is literally a read of whether the enemy has started their economy.
The three terms are: **a round gate**, **an enemy-economy read**, and **a distance gate**.

**A cohesion precondition, added last, because a split fleet made the trigger fire wrongly:**

> *"we only activate rush mode if all of our ships are within 3 * MAX_SPEED from each other."*

**Referent check.** The preceding sentences describe the failure: *"once in a while, I might
have a ship fly to the center and the other two ships fly away from the center. The enemy
might do the same. In this situation, I don’t actually want to activate the rush mode."*

**Disarm, stated separately from arm — and in the 4-player rule the two thresholds are
deliberately different:**

> 2-player: *"We deactivate rush mode if the enemy’s closest ship is more than 11 * MAX_SPEED
> away from us."* (same 11× as the arm condition — symmetric)
>
> 4-player: *"If the enemy is within 7 * MAX_SPEED of us, then we activate rush mode."* and
> *"We deactivate rush mode if our rush target is dead, if the enemy’s closest ship is more
> than 10 * MAX_SPEED from us, or we find a closer enemy that isn’t our rush target."*
> (**arm at 7×, disarm at 10× — an explicit hysteresis band**)

And the author's own note on how these numbers were arrived at, which is the honest part:

> *"I fiddled around with the numbers here so many times it’s not even funny."*
> *"At the end, I decided to go with a much less rush happy bot."*

## WHY IT MIGHT TRANSFER

Three structural pieces, each of which maps onto something we have and do not use.

1. **The enemy-economy term is the same construct our own cut identified.**
   *"the enemy has no docked ships"* is a binary read of whether their economy has come up —
   and our corpus cut's largest effect is exactly that (`THEM_ti_collected_end_w50`, AUC 0.32),
   with a runtime proxy in **their conveyor count** (70.1% of their early conveyors are inside
   one builder's r²=20 of their own core). Independent arrival at the same trigger content
   from a completely different game.

2. **The hysteresis band is the cure for the failure this library already filed.**
   `defence-recall-oscillation.md` records BC2022 5 Musketeers' *"This worked but led to an
   unfortunate oscillation problem"*, and notes it is worse here — our store is buffered to
   next round and last writer wins, so two units can hold contradictory beliefs for a whole
   round. **Arming and disarming on the same threshold guarantees chatter at the boundary;
   arming at a tighter threshold than you disarm at makes chatter impossible.** This costs
   one extra constant.

3. **The cohesion precondition is the anti-piecemeal rule our arithmetic demands.**
   With healing at 4.00 HP/Ti against a best damage of 1.80 HP/Ti (8.00 HP/Ti on a stacked
   tile), damage arriving in pieces is a 2.2:1 donation. *"only activate rush mode if all of
   our ships are within 3 * MAX_SPEED from each other"* is that rule stated as a gate rather
   than as a hope, and `mass-before-contact-by-following-the-first-mover.md` is the mechanism
   that would satisfy it here.

## WHAT WOULD KILL IT

- **The constants are Halite II's and are admittedly hand-fiddled**, by the author's own
  statement. Nothing here licenses importing 11× or 16 turns; what transfers is the
  **three-part structure**, not the numbers.
- **Halite II ships are mobile damage.** Their "rush" is a fleet flying at an undocked
  opponent; ours would be an immobile turret bought and placed. A disarm condition that says
  *"the enemy moved away, stop rushing"* has no analogue for a building that cannot be
  un-built for a refund — our `destroy()` is free but returns nothing.
- **Our engine has no cheap fleet-cohesion query.** `get_nearby_units(dist_sq)` is per-unit
  and vision-limited (builder r²=20), so a global "are all our builders within X of each
  other" check needs the store, one round of latency, and a single-writer discipline.
- **Shummie's own conclusion is that less rushing was better** (*"a much less rush happy
  bot"*), consistent with `the-all-in-is-a-counter-strategy-not-a-strategy.md`.

## BUILDER HOOK

Smallest test: whatever Loki constant currently decides commitment, split it into two —
`ARM_AT` and `DISARM_AT`, with `DISARM_AT` strictly looser — and add a one-line cohesion
precondition on the number of our builders within a fixed radius of the commit point. Then
log the number of arm/disarm transitions per game. **If a single-threshold version transitions
more than a handful of times per game, the oscillation failure is live in our bot and this
plank pays for itself before it changes any outcome.**

## SOURCES QUOTED IN THIS FILE

- https://shummie.github.io/Halite-2-Shummie/

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
