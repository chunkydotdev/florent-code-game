---
tactic: Three rival rules for when a worker switches to defence — peg-to-economy, siege-trigger, loiter-and-build-on-sight
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (4th) and Java Best Waifu (1st); Screeps official docs; Halite II / ReCurs3 (1st, as republished)
evidence: documented
transfers: partial
---

WHAT IT IS — the leagues that state a rule at all state one of exactly three, and
they are mutually incompatible. All three are worth writing down because we have
never chosen one on purpose.

**1. Peg defence to your economy count (a ratio, evaluated every round).** Java
Best Waifu, who won Battlecode 2020, tie unit production to economic-building
count with an explicit schedule:

> "Our bot would build one Landscaper and one Drone for each Vaporator built up
> to turn 1200, afterwards it would build 1 landscaper for every 2 drones
> (without taking into account the number of Vaporators)."

The High Ground apply the same idea as a *cap on defence* rather than a floor,
and it is the tightest rule found in this sweep:

> "we kept at least as many vaporators as we had net guns until we stopped
> building vaporators"

i.e. **defensive structures may never outnumber economic ones.** Both are
schedules, not threat responses.

**2. Build defence only when threatened (a trigger).** The Screeps official docs
state the opposite doctrine for defender creeps, and state the cost of getting it
wrong:

> "But note that building them continuously, even in peacetime, is a waste of
> resources. It’s better to construct them quickly during a siege."

**3. Loiter where defence will be needed, so the trigger is instant.** The High
Ground's actual implementation is a hybrid that removes the reaction latency from
rule 2 by pre-positioning the *workers*, not the structures:

> "Thus, we decided to direct our miners to try to run toward the enemy HQ
> location along our lattice, effectively making them be near the edge of the
> lattice and ready to build net guns at almost all times. We built net guns
> whenever we saw drones, but had a few restricting conditions: we kept at least
> as many vaporators as we had net guns until we stopped building vaporators, and
> we would usually build net guns at least 8 distance squared away from each
> other."

Halite II's winner made a fourth, orthogonal choice — **role exclusivity** —
scoping defence to threats against economy assets specifically:

> "For good or bad reasons, I decided a ship cannot be a candidate for both
> attack and defense at once. I thought it would be easier to balance priorities
> between colonizing vs fighting and attacking vs defending rather than
> everything at once, but cannot say whether it was better or not in the end. For
> defense, only enemy ships near an allied docked ship are considered."

*(quoted from ReCurs3's own postmortem text as republished at
`lakesidethinks.com/post/2018/10/halite2-strategy.html`, "Review for Top 3 Halite
2 Bots" — the original halite.io forum thread is no longer reachable, so this is
a republished primary and is labelled as such.)*

**And the trap in rule 2 is documented by the team that fell into it.** The High
Ground's economy stalled because a threat trigger, once fired, never cleared:

> "This messed up our build order as we had our HQ signal when rushed, and our
> miners stopped building vaporators when we were being rushed."

Their fix is a hard, unconditional resume, and it is worth quoting for its shape:

> "We also made a last-minute change to somewhat counter Kryptonite’s super
> annoying extended rushes: return to normal build order at round 400 whether we
> are being rushed or not. While hacky, this solution allowed us to win some
> games against them even when they had a net gun surrounded near our base"

WHY IT MIGHT TRANSFER — **because our own opening is a near-constant, and this is
the one place a constant is the wrong instrument.** Our r0-150 build medians are
identical in wins and losses; all measured variance is the opponent's. That means
whichever of these rules we are implicitly running, we run it unconditionally —
and rule 3 is the only one of the three that is *cheap and conditional at the
same time*, because the conditioning happens in worker positioning rather than in
production.

Rule 3 maps onto our ruleset almost verbatim and costs nothing to start:

- A builder's action range is one orthogonal tile, so **being in the right place
  is the entire cost of a fast turret**; there is no build-radius to lean on.
- `get_nearby_units()` on the enemy is our "whenever we saw drones".
- Our known objections to turrets are about *stock* (we lead the field in turret
  count in only 20.1% of games and every knob was neutral-to-negative), not about
  *latency* — and rule 3 is a latency change, not a stock change. **It is the one
  turret-shaped tactic left that has not been tested here.**

The High Ground's ratio cap is also a direct answer to the standing worry that
turret spend competes with tiebreak #1: "at least as many harvesters as turrets"
is expressible in our store in one slot and bounds the damage of any turret rule
we ship.

WHAT WOULD KILL IT — and the third is the one that should stop a naive import:

1. **Peg-to-economy assumes economic buildings are a good proxy for scale.**
   Ours are not symmetric: conveyors are 3 Ti at +1% and harvesters 20 Ti at +5%,
   so "one turret per harvester" and "one turret per conveyor" differ by an order
   of magnitude, and we out-build the field on conveyors by +13 per game. A ratio
   pegged to the wrong denominator would produce a turret spam this project has
   already refuted.
2. **The stall trap is real for us specifically.** We already have a documented
   failure mode of the same family (`orekeeper` freeze; the enemy builder parked
   on our conveyor causing 489 futile swings in one game). A threat trigger that
   suspends economy is exactly the input that produced The High Ground's stall,
   and their fix — an unconditional resume at a fixed round — is the cheapest
   insurance and should be written *at the same time as the trigger, not after*.
3. **Loitering costs delivery.** A builder standing near the frontier "ready to
   build net guns at almost all times" is a builder not moving titanium. In a
   game whose first tiebreak is cumulative delivery, and which we win 57.2% of at
   r1000, the loiter posture spends our winning asset. The High Ground's miners
   loitered *along their own lattice*, i.e. on the path they were already
   walking — the transfer only survives if our loiter tiles are on the delivery
   route, not off it.
4. Rule 2 in its pure Screeps form cannot transfer: their defender creeps spawn
   in a few ticks and ours are permanent buildings paying +20% scale forever.
   **A siege-triggered *turret* is a permanent purchase made on transient
   evidence** — the same objection recorded in [[runtime-density-siting]] and
   still unanswered.

BUILDER HOOK — take the **cap** before the **trigger**, because the cap is a
one-line safety rail and the trigger is a doctrine:

> Never build a gunner/sentinel if it would make our turret count exceed our
> living harvester count. (The High Ground's rule, denominated in the economic
> unit that actually scales at +5%.)

Then, if the loiter posture is tested, ship the resume with it:

> Any state that suspends normal economic build order must clear unconditionally
> after `R` rounds, regardless of whether the threat is still present.

The measurement that chooses between the three rules: **the distribution of
rounds between "first enemy builder seen in our home band" and "our first turret
built after it".** If that latency is large, rule 3 is the live lever and our
turret problem was never a stock problem. If it is already small, all three rules
are describing something we already do and this file is a filed negative.

Related: [[runtime-density-siting]] · [[fortify-on-idle]] ·
[[worker-fortified-turret-cell]] · [sweep 6](2026-08-09-sweep-6.md)

---

> ### ⚠ CAVEAT ADDED 2026-08-10 (research arm) — **"TURRET PRODUCTION WAS ALREADY REFUTED FOUR WAYS" IS UNSOURCED AS WRITTEN.**
>
> This file leans on that claim to set aside a whole knob. **No evidence is cited
> for it here, and none of the files carrying the claim cite a source for it**
> (`grep -c "](""` returns **0** markdown links in this file and in
> `worker-fortified-turret-cell.md`). **"Four ways" names a count without naming
> the four.**
>
> **This is the same failure class the index records for
> `THE FORWARD ROAD IS CLOSED`** — a closure repeated downstream until it reads as
> established, while nothing underneath it was ever re-checked. It may well be
> true; it is simply **not sourced where it is used.**
>
> **Under D12** (Magnus, 2026-08-10 — *"test everything in unrated games before we
> refute them"*) **an unsourced archive-era closure cannot retire a road.** Goes to
> the **bottom of the queue, not off it.** Whoever next touches turret production
> should either name the four instruments or drop the phrase.
