---
tactic: The branch point is an achievement or a count of your own structures — not a round number
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 Just Woke Up (tournament winner) and Battlecode 2025 The Kragle (finalist)
evidence: documented
transfers: yes
---

## WHAT IT IS

Neither BC2025 finalist branches on the clock. Both branch on **a state their own bot
reaches**, which means the branch fires early on the games where they are ahead and late on
the games where they are not — self-pacing, with no tuned constant per map size.

**Just Woke Up (winner) — a count of your own structures:**

> *"If we had more than 5 towers placed on the map (that the soldier was aware of) they would
> start pathfinding towards any empty paint they sensed with the intention to fill it in."*

**Referent check.** "they" is the team's soldiers; the parenthetical *"(that the soldier was
aware of)"* is load-bearing — the gate reads a **per-unit local estimate**, not a global
truth. The stated reason is in the next sentence: *"This was intended to make it so we
wouldn't waste paint filling in random empty tiles in the early game, but once we had
sufficient map presence we would start increasing our paint coverage since that was one of
the win conditions for the game."*

**The Kragle — the branch closes when the first objective completes:**

> *"Until the soldiers finished the first ruin, they were in “opening mode.”"*

> *"On 90% of the test maps, the soldier pair would find an uncontested ruin and capture it
> before turn 20."*

(The trigger *content* — contested vs uncontested — is covered in
`the-trigger-rides-on-a-unit-already-going-there.md`; this file is about the **shape of the
branch point**.)

Their state machines are built to take state as input rather than a clock. Just Woke Up:

> *"we run a determineState function which uses our surroundings, resource levels, and
> previous states to decide what state our unit should be in"*

Note the third input — *previous states*. That is hysteresis, and it is the documented cure
for the oscillation failure recorded in `defence-recall-oscillation.md`.

## WHY IT MIGHT TRANSFER

**`KILL_WINDOW_RND: 250` is a round number, and our own ladder cut says it is not the binding
constraint** — 74.4% of our core-kill wins are already inside r250, holding at 71.4% against
opponents rated 1600+. What is scarce is the kill happening at all. A programme whose
constraint is *incidence*, not *speed*, wants a branch that fires on **readiness**, not on
the clock.

Milestone gates are also the cheapest thing in our engine, because the quantities are
already free getters on the calling unit:

- `get_unit_count()` — our living units including the core, compared to
  `GameConstants.MAX_TEAM_UNITS`.
- `get_global_resources()` and `get_global_ammo()` — bank and ammunition, the *"resource
  levels"* term.
- `get_nearby_buildings()` filtered by `get_entity_type()` — a **local** count of our own
  turrets, which is exactly Just Woke Up's *"(that the soldier was aware of)"* construction
  and needs no store slot, no cross-unit pooling, and no buffered-write latency.

And our own best runtime discriminator is already in this family. The core-kill cut's Tier-1
trigger is:

```
ammo_spent_so_far = (cumulative amount the core has passed to convert_ammo)
                    - ct.get_global_ammo()
```

— a running total of **our own** state, computed by one unit that never moves, available
every round from round 0 (`US_shot_w50`, AUC 0.64-0.68, worst Holm p 1.5e-07; correlation
with kill round −0.457). That is a milestone gate in Just Woke Up's exact idiom.

## WHAT WOULD KILL IT

- **A milestone gate on our own state cannot distinguish cause from marker any better than a
  clock can.** Firing a commitment when *we* are already shooting is, on the corpus evidence,
  reading a thermometer. See `nobody-separated-cause-from-marker.md`; only the arena can
  settle it.
- **A local count is a biased estimate of a global one**, deliberately so. Just Woke Up's
  soldiers act on what they can see; ours would too. A builder deep on the enemy half sees
  none of our turrets and would branch as though we had none.
- **Milestones that are never reached never fire** — the same failure as a trigger that never
  observes its condition, and it needs the same stop-loss (`abort-the-scout-on-a-deadline.md`).
- **The hysteresis term is essential, not decorative.** Without *"previous states"* in
  `determineState`, a threshold crossed near the boundary flips every round; our store's
  next-round visibility and last-writer-wins make cross-unit oscillation worse here than in
  the source game.

## BUILDER HOOK

Smallest test: take whichever Loki constant is currently expressed as a round number and
re-express it as `our_turret_count >= N` or as the core's `ammo_spent_so_far >= N`, with a
one-way latch (once opened, never closes) to supply the hysteresis. Measure
`core_kill_share` and `time_to_core_kill` against LOKI-(N−1), and log the round at which the
gate opened so the distribution of branch times can be read directly from the replay.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
