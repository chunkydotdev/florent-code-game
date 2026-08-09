---
tactic: Do not tune a threshold for economy-vs-military — simulate both branches forward at runtime and take the better one
source: https://raw.githubusercontent.com/Agade09/Agade-Ghost-in-the-Cell-Postmortem/master/Agade_GitC_Postmortem.md
origin: CodinGame Ghost in the Cell, Agade (1st place)
evidence: documented
transfers: partial
---

## WHAT IT IS

Agade won Ghost in the Cell and reports that he could find **no heuristic** for the
economy-versus-military decision, so he replaced the heuristic with a **runtime forward
simulation of both branches**:

> *"I play 20 turns of my AI with increasing enabled/disabled against my AI with increasing
> disabled. If my production is higher after 20 turns of increasing I play my AI in increasing
> mode, otherwise I disable increasing."*

> *"This led to a huge gain in win rate."*

**Referent check.** *"increasing"* is Ghost in the Cell's pure economy investment — spend 10
troops from a factory to raise its production by 1. *"my AI"* means his own decision policy,
run in simulation inside the turn, not an offline test. The problem it solves is stated in the
preceding sentences: *"I might have a safe, far from the frontline factory which greedily
thinks it can increase without any problems, whereas actually those 10 troops were needed for
battle, I then lose a factory and subsequently the game. I couldn't think of any good
heuristics for this so I decided on the following scheme"*

The same author uses a forward rollout to pick the *target* of a first-turn strike, while
leaving the *timing* unconditional:

> *"I send both my bombs on the first turn to any factory I believe the enemy will own within
> 10 turns."*

> *"I determine future owners by self playing 10 turns with no bombs and no increase."*

An independent arrival at the same idea, from Terminal: Correlation One competitors enumerate
attack candidates and score them by simulated outcome —

> *"we apply a value function which returns 3.5 * number_units_made_to_their_base +
> num_cores_damage_dealt. We take the max value of all of the simulations, and choose that to
> be our attacking strategy for the turn."*
>
> **NOT INDEPENDENTLY VERIFIED — see WHAT WOULD KILL IT.** This string was reported by a
> source-gathering subagent from a text-extraction proxy of a Medium article; Medium returns
> 403 to direct fetch and the Wayback API was rate-limiting at the time of this sweep. It is
> recorded here as an **unverified lead**, not as evidence, and nothing in this file depends
> on it.

## WHY IT MIGHT TRANSFER

The economy-versus-military decision is exactly our open question, and Agade's finding is that
**it does not have a good threshold** — he looked and did not find one. That is worth knowing
before we spend planks tuning constants.

Our engine makes a *closed-form* version of this unusually tractable, because our economy is
deterministic and small:

- A harvester emits one stack of `GameConstants.STACK_SIZE = 10` every 4 rounds, first stack
  immediately on build. Passive income is 10 titanium every 4 rounds, fixed.
- Costs are exact and queryable: `get_harvester_cost()`, `get_gunner_cost()`,
  `get_sentinel_cost()`, and scaling is a known multiplier per category.
- Ammunition converts 1:1 with titanium, once per team per turn.

So "titanium at round R if I build economy now" versus "titanium and damage at round R if I
build a turret now" is arithmetic, not simulation. The thing Agade needed 20 turns of rollout
for — because his opponent's troops were in flight — we can compute in closed form for the
economic half, and the military half reduces to the heal-versus-damage race the library has
already priced (heal 4.00 HP/Ti, best damage 1.80 HP/Ti, 8.00 HP/Ti on a stacked tile).

`transfers: partial`, and the reason is the budget.

## WHAT WOULD KILL IT

- **10 ms per unit per turn.** Agade's game had a per-turn budget across a handful of
  factories; we have up to 50 units each with their own 10 ms and a rolling 5% buffer, and our
  library measured Ouroboros discarding **26,356 unit-turns across 85 games (max 3,508 in one
  game)** to exactly this limit. A forward rollout of the full game state is not affordable —
  a closed-form economic comparison is.
- **A timeout is not an exception but it still loses the turn**, and an uncaught exception
  **permanently destroys the unit for the match**. Any simulation must be bounded by
  `get_cpu_time_elapsed()` checks, not by hope.
- **We do not see the enemy state a rollout would need.** There is no getter for enemy
  titanium or ammo; a rollout of "what will they own in 10 turns" is inference over inference.
  Agade could see the whole board; we cannot.
- **The Terminal corroboration is unverified** (above) and must not be cited as a second
  independent source until someone retrieves that page directly.

## BUILDER HOOK

Smallest test, and it is a *report* not a behaviour change: at one decision point, compute both
branches' closed-form titanium-at-r+40 and `print()` which one the arithmetic prefers alongside
what the bot actually did. Run one battery, then read the disagreement rate from the replay
text. If the bot already agrees with the arithmetic almost always, the road is closed for the
price of a print statement — which is the cheapest possible way to test a decision rule that
would otherwise cost a full plank.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/Agade09/Agade-Ghost-in-the-Cell-Postmortem/master/Agade_GitC_Postmortem.md
- https://medium.com/terminal-player-strategies/the-terminus-of-our-terminal-strategy-19c96da2acf5 (UNVERIFIED — 403 to direct fetch)

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
