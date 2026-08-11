---
tactic: Every dwell-limiting trigger the field actually shipped is a RESUPPLY trigger — and our builder has nothing to resupply
source: https://battlecode.org/assets/files/postmortem-2025-spaark.pdf
origin: Battlecode 2025 SPAARK; Halite III teccles (2nd) and TheDuck314 (3rd); Battlecode 2025 om nom, The Kragle
evidence: documented
transfers: no
---

## WHAT IT IS — the census, before the mechanisms

Sweep 23 read 23 Battlecode postmortems (128,679 words), PurpleWave's and
Steamhammer's forward-unit source, and the Halite III 2nd/3rd-place writeups,
asking one question: **what made a forward unit leave enemy territory?**

**Nearly every shipped answer is "the unit ran out of a carried consumable."**

| source | trigger | quoted |
|---|---|---|
| SPAARK (BC2025) | carried paint below a fraction of capacity | *"We made robots retreat to the nearest paint tower if they had less than 1/3 of their paint capacity."* |
| om nom (BC2025) | carried paint below an absolute floor | *"the soldiers went home unconditionally at around 50 paint to refuel."* |
| TheDuck314 (Halite III, 3rd) | cargo above a constant | *"Once a ship gets to 950 halite, it goes into Return mode and heads back to the nearest dropoff."* |
| teccles (Halite III, 2nd) | cargo above a constant, or opportunity cost | *"They start to return when either of the following happens:"* … *"The best score they get for any square is too high"* |
| The Kragle (BC2025) | carried paint | *"Our robots would spend about half of their lifetime traveling back to towers and waiting around towers for paint."* |
| 4 Musketeers / don't at me (BC2023) | HP, i.e. a consumable restored only at home | *"A launcher's state is set to fallback if it is not in combat, if they are less than half health, and if they have a fallback island."* |

The two exceptions in the whole sweep are Steamhammer's relief test and
PurpleWave's threat gate, filed separately
([`withdraw-when-relieved-or-when-the-job-became-impossible`](withdraw-when-relieved-or-when-the-job-became-impossible.md),
[`the-forward-unit-is-excluded-from-the-go-home-branch`](the-forward-unit-is-excluded-from-the-go-home-branch.md)).

## WHY IT DOES NOT TRANSFER — and this is the load-bearing result of the sweep

**Our builder bot carries nothing.** Run the entity list against the table above:

* **Titanium is a GLOBAL pool.** A builder standing on the far side of the map
  pays for a conveyor out of the same balance as one standing on our core. There
  is no cargo, no carry limit, no "return to bank the load". Every trip-home
  trigger in Halite is answering a question our rules do not ask.
* **There is no ammunition on a builder.** Turrets fire from a global pool and
  our builder's attack costs 2 Ti from that same global pool. Nothing to rearm.
* **HP is not restored at home.** Healing is `heal(position)` from an
  *orthogonally adjacent friendly builder*, +4 HP for 1 Ti — it is a **second
  builder standing next to the first**, and that is exactly as available in enemy
  territory as it is at our core. There is no home-only repair facility, so the
  BC2023 "fallback island" class has no object to name.
* **`PLAY_DEFENCE: never` removes the one remaining motive.** Preserving the unit
  is not a reason on this programme.

**⇒ There is no rule-level reason for our forward builder to go home, ever.** The
only motive our ruleset supplies for moving a builder *backwards* is that some
tile behind it is worth acting on more than any tile in front of it — which is a
**target-selection** statement, not a withdrawal statement.

## WHAT WOULD KILL IT

Two things would reopen the class and neither is currently true:

1. **A forward heal chain that cannot be staffed.** If in practice a lone raider
   cannot be healed because no second builder is ever adjacent, HP becomes a
   consumable restorable only where our builders cluster, and the BC2023 fallback
   predicate becomes live. **This is a measurable in-repo question and I did not
   run it** — see BUILDER HOOK.
2. **Builder-turn cost of the walk.** Act and move are mutually exclusive per
   turn, so travel is priced in forward actions. That makes the walk home
   expensive, which *strengthens* rather than weakens the verdict.

## BUILDER HOOK

**Do not port a withdrawal threshold.** The correct shape of the intervention on
our 2.28x dwell number is **not** "leave sooner" — it is "have somewhere to act
next", which is
[`the-idle-forward-unit-gets-a-destination-not-a-recall`](the-idle-forward-unit-gets-a-destination-not-a-recall.md).

**One measurement worth naming (I did not run it, per this sweep's scope):** over
our forward builders, what fraction of raider-rounds have a second friendly
builder orthogonally adjacent? If it is near zero, forward healing is
theoretical and item 1 above reopens.
