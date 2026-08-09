---
tactic: Heal cap and timeout — bound how long a unit may stay in the repair queue
source: https://battlecode.org/assets/files/postmortem-2022-5-musketeers.pdf
origin: Battlecode 2022 / 5 Musketeers (7th-8th overall), §4.2.2
evidence: documented
transfers: yes
---

WHAT IT IS — a measured account of the **repair queue eating the middle of the
map**, and the two-line fix. 5 Musketeers start from the same arithmetic we have:

> "One nice feature in this game is that damage is not permanent. A soldier can
> be healed by Archons, and Archons can be healed by builders. You can keep
> yourself alive for longer periods of time. And if you heal a soldier rather
> than make a new one, that saves a lot of lead."

They built the obvious greedy policy — always heal the lowest-HP unit — got good
results, and then watched it fail:

> "The problem is starvation. If you have two soldiers, one has 20 health, and
> the other has 10, the 10 will be healed. But what if by the time the 10 is
> full, another 10 comes? If this keeps happening, the 20 never gets healed. I
> saw replays where this would go on for a while, with soldiers just sitting at
> home waiting to be healed for over 1000 rounds. This was bad because since we
> had often nearly a dozen soldiers out of commission like this, it allowed our
> enemies to have more soldiers than us in the clash in the middle. They got the
> upper hand and slowly advanced on us."

Their conclusion is the transferable sentence:

> "Even though the soldier needed healing, it was more advantageous for them to
> just go into the fight and do their best, even if it meant death."

and the fix:

> "To resolve these issues, I added a heal cap and timeout to prevent too many
> soldiers from staying for too long. This strategy, coupled with good soldier
> micro changes, made us ranked 1st for several days."

Their Figure 5 is captioned *"Low health soldiers are huddling around the base to
be healed."*

WHY IT MIGHT TRANSFER — **because we have a photograph of that figure in our own
data.** 25.4% of our home-band builder deaths are on the heal seat next to our
core, lift **2.14** against the base area's own composition — the single most
over-represented tile class we have. Their failure was a queue that grew without
bound around a stationary healer; our heal seat is a stationary healer (the core
footprint, where the stacked 8.00 HP/Ti case lives) with builders queued on it.

The consequence 5 Musketeers report is the consequence we measure. They lost "the
clash in the middle". Our middle game is exactly where we die: conditional on a
core kill, the chance it is ours runs 29% → 55% → 72% → 76% across
r0-150/151-300/301-600/601-999 — we win the opening, we win the r1000 clock
(57.2% of 353 games), and we lose r150-600. **"Our units are alive but out of
commission at home" is a loss mechanism that leaves no trace in a
units-alive count**, which is exactly why five instruments could all break at
r150 without any of them naming the cause.

The rule is cheap and needs no new state: a per-unit round counter and a global
cap, both expressible in the 16-slot store or held per-unit in `self`.

WHAT WOULD KILL IT — three, and the first is the honest one:

1. **We have not shown our heal seat is a queue.** A high death share on the heal
   seat is equally consistent with "the heal seat is simply where the fighting
   is", which is the null the lift is supposed to control for — and 2.14 is a
   real lift, but a lift over the base area's composition, not over *time
   spent*. **The measurement this file needs is builder-rounds spent adjacent to
   the core, not deaths there.** Until that exists, the transfer is a hypothesis.
2. **Their healer was mobile and ours is not.** Their fix in §4.2.3 was to move
   the Archon toward the fight ("This became a very common strategy, with the
   majority of top teams having their Archons move"). **Our core cannot move**,
   so the half of their answer that removed the round trip is unavailable to us —
   only the cap-and-timeout half transfers. Our substitute for a mobile healer is
   that *any* builder can heal any adjacent tile, so repair can go to the work
   instead of the work coming home.
3. **Battlecode 2022 rewarded surviving units directly** (Archon survival was a
   tiebreaker), so their incentive to over-heal was structural. Ours is
   different: tiebreak #1 is titanium **delivered**, so a builder idling at the
   heal seat is losing the tiebreak we actually win on, which makes the case
   *stronger* here, not weaker.

BUILDER HOOK — two bounds, both cheap, both testable independently:

1. **Timeout.** A builder may spend at most `N` consecutive rounds in
   heal-or-wait state adjacent to the core; after `N` it must take a normal task
   regardless of its own or the core's HP. Start with N generous (say 20) so the
   change is a tail-cut, not a policy rewrite.
2. **Cap.** At most `M` builders may occupy heal-seat tiles at once; the
   `M+1`-th takes its next-best task. `M` has a principled floor from
   [[marginal-healers-per-structure]]: healers beyond `ceil(incoming/4)` are
   restoring HP into a cap and doing nothing.

Instrument first, ship second: **the distribution of consecutive rounds a builder
spends within one tile of the core, split by win/loss, in the r150-600 band.**
5 Musketeers' failure had a fat tail (units stuck "for over 1000 rounds"); if
ours has no tail, this file is a filed negative and the heal-seat lift means
something else.

Related: [[marginal-healers-per-structure]] · [[worker-fortified-turret-cell]] ·
[middle-game hazard](../middle-game-hazard-and-economy-2026-08-09.md)
