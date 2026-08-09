---
tactic: (B) The one place anyone actually MEASURED repair versus rebuild — it is 2x in favour of repair, and the right policy is per structure class, not global
source: https://patch-diff.githubusercontent.com/raw/screeps/docs/pull/60.diff
origin: Screeps — pull request #60 to the official docs repo, "Remote mining article" by slowmotionghost, opened 2017-08-23. VERIFIED VIA THE API AS STILL OPEN AND NEVER MERGED (state "open", merged false). The upkeep constants table is from the community wiki source, https://raw.githubusercontent.com/glitchassassin/screeps-wiki/main/app/routes/_base%2B/_wiki%2B/Useful_Constants.mdx
evidence: documented
transfers: partial
---

WHAT IT IS — sub-question (B) asked whether anyone measured which pays. **One
person did the arithmetic and published it.** The rebuild side:

> *"If we were to not repair the container and rebuild it every time it completely decayed, it would mean and investment of 5000 energy every 5000 ticks (250000 hits divided by 5000 hit decay, then multiplied by 100 for decay frequency) or 1 energy per tick, as well as loss from energy decay during downtime."*

The repair side, and the conclusion:

> *"Repairing costs 1 energy for 100 hits([`REPAIR_POWER`](/api/#Constants)), meaning repair costs 50 energy to cover the decay, every 100 ticks, at a cost of 0.5 energy per ticks. While there is still an initial investment to build the container, repairing it is clearly the cheapest method of collecting energy."*

> *"Rebuilding is always more expensive than repair."*

For roads specifically, the same document prices upkeep against the alternative it
buys out:

> *"The cost to repair a road per tick is 1 energy every 1000 ticks (on plain terrain), which is significantly lower than the body part costs of the extra MOVE parts, so while harder to implement, roads are generally a worthwhile investment."*

**And the community's closed form shows the answer is not one number but a table.**
From the wiki's *"Average energy per tick upkeep cost"* rows:

> *"| | 0.001* | `const ROAD_UPKEEP = ROAD_DECAY_AMOUNT / REPAIR_POWER / ROAD_DECAY_TIME;` |"*

> *"| | 0.15* | `const ROAD_UPKEEP_TUNNEL = (ROAD_DECAY_AMOUNT * CONSTRUCTION_COST_ROAD_WALL_RATIO) / REPAIR_POWER / ROAD_DECAY_TIME;` |"*

**A plain road and a tunnel road differ by 150x in upkeep**, so the same
repair-everything policy is correct for one and ruinous for the other. The dissent
is on the wiki too — the referent of *"the roads"* is the roads described in the
preceding clause of the same sentence:

> *"If you have roads, you don't need as many MOVE parts. Roads speed creep movement by a factor of 2, meaning only half as many MOVE parts are required. Roads are especially important in swamps, which are 5 times slower than plain land and 10 times slower than roads. However, the roads must be maintained, so a few players decide not to keep up roads."*

WHY IT MIGHT TRANSFER —

- **It answers (B) in the affirmative and that was not expected.** The library can
  now say: *somebody measured, and repair won by 2x on decay.*
- **The structural lesson is the one to carry, not the ratio: policy per class.**
  Our classes are not plain-vs-tunnel but **conveyor (20 HP, 3 Ti) vs harvester
  (30 HP, 20 Ti) vs turret**. A conveyor is 3 Ti and heals at 4 HP per Ti, so
  restoring a 10-HP-damaged conveyor costs ~2.5 Ti against 3 Ti to rebuild it —
  **those are close enough that our answer may genuinely differ from Screeps's, and
  the crossover is computable from the ruleset.**
- **Our engine has a third option Screeps does not: `destroy()`.** The organisers'
  reference says destroying a conveyor *"returns any resources currently in transit
  on that tile to your team's balance"*, it costs nothing, uses no action cooldown,
  and it **removes that entity's contribution to the cost scale.** So for us
  "rebuild" can be *destroy-then-build*, which refunds the corked stack and the
  scale. **Nobody in this sweep had that primitive; the arithmetic here does not
  price it.**

WHAT WOULD KILL IT —

- **⚠ PROVENANCE, stated first because it is easy to over-read.** This is an
  **unmerged pull request**, open since 2017 and never accepted into the official
  Screeps docs. It is a community author's arithmetic on a public artifact — it is
  not an organisers' statement, and nobody ratified it. `evidence: documented`
  attaches to *the text exists and says this*, not to *the game's maintainers agree*.
- **Wrong damage model.** Screeps upkeep is **deterministic decay** — a known
  amount every known interval. Ours is **enemy fire**: bursty, targeted, and it can
  remove a conveyor from 20 HP in three gunner shots before any repair lands. **A
  crossover derived from decay does not transfer to combat damage**, and the correct
  reading of this file for us is the *method* (compute cost-per-tick of each policy
  and compare) rather than the *result*.
- **Our heal is not a repair pack.** Heal is 1 Ti for +4 HP on **all** friendly
  entities on an orthogonally adjacent tile, and the library's standing arithmetic
  makes it 4.00 HP/Ti (8.00 on a stacked tile). That changes the comparison in our
  favour relative to Screeps and is not accounted for above.
- **And the gate applies.** As with
  [`repair-versus-reroute-is-one-pathfinder-constant`](repair-versus-reroute-is-one-pathfinder-constant.md),
  any repair plank is in the INDEX's untestable-in-the-arena class until a
  building-attacking opponent is in the pool.

BUILDER HOOK — **do the arithmetic for our ruleset before writing any repair code**,
because it is a spreadsheet, not an experiment: for a conveyor at HP *h*, compare
`(20 - h)/4` Ti of healing against `get_conveyor_cost()` plus the scale delta of
destroy-then-build, and find the crossover *h*. If it lands near full HP, repair is
never right for conveyors and the whole class collapses into "rebuild fast", which
is a much simpler plank. **That calculation is free and it decides whether any of
this is worth building.**
