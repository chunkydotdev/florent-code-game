---
tactic: Fortify on idle — defence maintenance is the worker's DEFAULT task, not a scheduled one
source: https://docs.screeps.com/defense.html
origin: Screeps official documentation (Defense); rule form corroborated by Overmind (bencbartlett), the best-documented open-source Screeps AI
evidence: documented
transfers: partial
---

WHAT IT IS — Screeps is the one league where "workers maintain defensive
structures" is not an artefact of a dedicated repair unit: it is the **only** way
defensive HP exists at all. The official docs:

> "In the same way as walls, ramparts are built with 1 hit point initially and
> need to be fortified to a needed level by workers afterwards."

and, because the structure decays:

> "A rampart has another peculiarity: its superior defense abilities must be
> constantly maintained at a proper level. Every few ticks, a rampart loses a few
> hit points, so you should assign a worker to make sure that all your ramparts
> stand alert and don't wear off."

The engine constants make the worker the *efficient* buyer, not merely an
available one. From the official API constants — `REPAIR_POWER: 100`,
`REPAIR_COST: 0.01` — a worker buys **100 hits per energy**. The dedicated
defensive structure that can also repair, the tower, costs 10 energy per action
for "Repair effectiveness 800 hits at range ≤5 to 200 hits at range ≥20", i.e.
**80 hits per energy at best and 20 at worst.** The generalist worker beats the
purpose-built structure by 1.25× to 5×.

Overmind states the *scheduling* rule in the form that matters — repair is what a
worker does with time it would otherwise waste:

> "If there are ramparts within range 3 of the anchor below their target hits,
> the manager will be spawned with 32 WORK parts and will fortify the ramparts
> when it is idling."

Two things are being said at once: a **trigger** (a named structure class, within
a named radius of a named anchor, below a target HP) and a **priority** (idle
time only — the manager's primary logistics job is never displaced).

WHY IT MIGHT TRANSFER — because it answers our actual question in the right
shape. We are not asking "should we build more turrets" (refuted four ways); we
are asking **where our builders spend their exposed time**, and Screeps' answer
is *fortification is the residual, not a role*. Our builders have exactly the
right shape for that: heal is 1 Ti and one turn, costs nothing to interleave, and
`destroy()` and the cost getters mean no long-lived commitment is created.

The specific transfers:

- **Trigger by radius from an anchor, not by a global scan.** Overmind's rule is
  scoped to "range 3 of the anchor". Our equivalent is free: a builder already
  has `get_nearby_buildings(dist_sq)` and the core position. This keeps it inside
  the 10 ms budget, which a whole-map damaged-building scan would not.
- **Below target hits, not below max hits.** Overmind fortifies toward a *target*,
  not to full. Our HP caps make over-healing a literal waste of 1 Ti and a turn,
  so the same `hp < target` form is right here.
- **Idle-time only.** This is the guard that makes the tactic safe against the
  failure mode in [[heal-cap-and-timeout]]: a builder that has a delivery task,
  a harvester to plant, or a conveyor gap to close never gets pulled into repair.

WHAT WOULD KILL IT — and the first is a genuine disanalogy that must be stated
before any Screeps number is imported:

1. **Screeps structures decay; ours do not.** Rampart maintenance is mandatory
   there because of `RAMPART_DECAY_AMOUNT: 300` every `RAMPART_DECAY_TIME: 100`
   ticks. **Nothing in our ruleset loses HP without being attacked.** So the
   "constantly maintained" half does not transfer at all — only the
   *damage-response* half does, and a peacetime fortification loop here would be
   pure waste. Any import of this file that produces idle healing of undamaged
   buildings is a misread.
2. **Screeps has no HP ceiling worth speaking of** (ramparts run to 300k at RCL2
   and 300M at RCL8), so fortification is an unbounded sink for surplus energy.
   Our buildings cap at 20-40 HP and the core at 500. There is very little for
   surplus titanium to buy here — which is a real problem, because *we bank
   titanium and do not spend it.*
3. **Screeps' repair is remote-ish** (range 3 for a creep, whole-room for a
   tower). **Ours is strictly orthogonally adjacent and consumes the builder's
   move for the round.** Every HP we buy also buys a stationary, exposed body.
   That is the cost Screeps does not pay and it is precisely the cost our death
   attribution is measuring.
4. **Screeps has no turn-limit tiebreak on delivered resource.** Energy spent on
   ramparts is not energy subtracted from a scoreboard. Ours is.

BUILDER HOOK — **the residual-task rule, with no new production and no new
state:**

> After a builder has resolved its primary task for the round and would otherwise
> move or idle, if a friendly **turret** within `dist_sq ≤ 2` has
> `hp < max_hp` and we can afford 1 Ti, heal it.

That is a strictly-dominated-time change: it only fires on turns the builder was
going to spend on nothing. Ship it before anything in
[[worker-fortified-turret-cell]], which spends *scheduled* time.

The measurement that tells us whether it can even matter: **how many
builder-rounds per game are currently spent neither acting nor moving?** If that
number is near zero, the residual is empty and this file is a filed negative. If
it is large — and given that we bank titanium we never spend, it plausibly is —
then there is free repair capacity sitting in our bot right now.

Related: [[marginal-healers-per-structure]] · [[worker-fortified-turret-cell]] ·
[[defence-production-pegged-to-economy]]
