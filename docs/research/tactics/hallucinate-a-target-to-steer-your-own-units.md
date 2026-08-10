---
tactic: Write a FALSE sighting into your OWN comms to steer your own units — reuse the reactive layer instead of adding a mode
source: https://battlecode.org/assets/files/postmortem-2023-no-thoughts.pdf
origin: Battlecode 2023 / no thoughts head empty (HQ strategy); corroborated by Battlecode 2021 / wololo (map-edge mirror)
evidence: documented
transfers: yes
---
WHAT IT IS — **The one thing in this sweep that is both well-sourced and immediately
buildable, and it is deception pointed inward, not outward.** no thoughts head empty had a
normal enemy-reporting pipeline:

> *"Once a launcher spotted an enemy, it would attempt to write that location to the shared
> array. Nearby launchers would then travel to that locations."*

Rather than write a second, separate "go attack the enemy HQ" behaviour, their HQ **injected a
fake observation into that same pipeline**:

> *"periodically "bait" our team's launchers to enemy HQ locations. It did this by using our
> enemy reporting mechanism to "hallucinate" an enemy at the enemy HQ. Launchers would then
> respond as if there was an enemy there."*

(The referents: *"our team's launchers"* are their own attacking units; *"our enemy reporting
mechanism"* is the shared-array sighting channel quoted above; the *"enemy HQ"* is the real
opposing headquarters, so the location is true and only the presence of a target there is
false.) **The HQ lies to its own army so that the army's existing target-seeking code carries
it to the enemy base.**

**The same primitive appears independently in wololo 2021**, applied to exploration rather than
attack:

> *"If an explorer saw a map edge, it would pretend that the map edge was a mirror, and that it
> could sense another explorer (its reflection) on the other side, so that it would not judge
> areas off of the map to be unexplored and attempt to explore them."*

(The *"reflection"* is a phantom friendly unit that does not exist; it is fed into the same
repulsion field that real sensed explorers feed.) **Two top-flight teams, two different years,
same trick: manufacture a synthetic percept so an existing reactive rule produces the desired
behaviour, instead of writing a new branch.**

WHY IT MIGHT TRANSFER — **directly, and it is on-programme: the payload is "send the attackers
at the enemy core".** Our engine gives us every piece:

- We already have the channel — 16 integer slots, private per team, and this repo's
  `store-semantics-2026-08-09.md` has already characterised its buffering and its
  can't-represent-zero trap.
- We already have the geometry — the enemy core's position is derivable from map symmetry
  (rectangular, reflection or rotation), and `play-the-players-2026-08-09.md` measured that
  opening siting in this league is geometric rather than behavioural.
- The core is the natural liar: it never moves, it has the largest vision (r²=36), it is the
  only unit guaranteed alive, and `convert_ammo()` does not consume its action cooldown, so a
  store write costs it nothing it was using.

**The engineering argument is the real one, and it is the argument this library keeps arriving
at from other directions.** Our tactics corpus already says the winning representation is *no
stored plan* ([`the-modal-winning-representation-is-no-stored-plan`](the-modal-winning-representation-is-no-stored-plan.md))
and that a mode flag loses to a target chain
([`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md),
[`the-target-chain-ends-in-explore`](the-target-chain-ends-in-explore.md)). A synthetic sighting
is how you get a mode change **without** a mode: one writer, one slot, and every consumer's
existing "go to the reported threat" code does the rest. It also sidesteps the store's worst
failure mode — this repo measured five concurrent read-increment-write callers all leaving the
counter at +1 — because a hallucinated sighting is a **single-writer, idempotent, absolute
value**, not an accumulator.

WHAT WOULD KILL IT — **four things, and the third is ours specifically.**

1. **It is worthless if our attackers do not already have a "go to the reported enemy" rule.**
   The whole value is reuse; if the consumer has to be written from scratch, this is just a
   normal target slot with a confusing name and no advantage over one.
2. **The one-round write delay.** Our writes are visible only from the next round, so a
   hallucination is always at least one round stale. For a fixed target (the enemy core, which
   cannot move) that is irrelevant; for a moving target it is exactly the staleness that makes
   real sightings unreliable.
3. **A lie in a shared channel is indistinguishable from truth to every consumer, including the
   ones you did not mean to move.** This repo has already named the class — the
   `local-vision-gate-audit-2026-08-08.md` defect is *a durable decision gated on an unguarded
   local-vision sample*, and a fabricated sighting is that defect deliberately induced. If any
   defensive or recall logic reads the same slot, the hallucination will trigger it too, and 5
   Musketeers' documented oscillation ([`defence-recall-oscillation`](defence-recall-oscillation.md))
   is the shape of the resulting bug. **Give the synthetic sighting its own slot or its own tag
   bit; do not overload the real threat slot.**
4. **no thoughts head empty did not measure it.** The postmortem states the mechanism and gives
   no ablation, no win-rate delta, and no counterfactual. It is documented as *built by a strong
   team*, not as *shown to pay*.

BUILDER HOOK — smallest test, one unrated leg: **the core writes the symmetry-derived enemy-core
position into a dedicated store slot every round from round 0, and builder dispatch treats that
slot exactly like a real reported threat.** Falsifier: if median time-to-core-kill and
core_kill_share are unchanged, the attackers were already going there and the synthetic sighting
bought nothing — bank the null and stop. The variant worth a second leg is the *periodic* one no
thoughts actually shipped (*"periodically"*), i.e. alternate the slot between the real nearest
threat and the hallucinated core, so a single mechanism produces both defence-free harassment
and the finish.
