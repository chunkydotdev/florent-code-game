---
tactic: (B) THE CHEAPEST COMMITMENT DEVICE IN THE FIELD — do not build a state machine to stop a re-derived decision flip-flopping; add a constant to whatever you chose last time. Seven independent bots, five leagues, one line each
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/StrategyBossZerg.cpp
origin: Steamhammer, UAlbertaBot, PurpleWave, Stardust (StarCraft AI); TheDuck314 and mlomb (Halite III); TooAngel (Screeps)
evidence: documented
transfers: yes
---

## WHAT IT IS

Every bot below re-derives a decision from scratch every tick and stores **nothing but the
previous answer**. Commitment is then bought with a single constant. The forms differ; the
idea is identical.

**1. An additive incumbency bonus on a score — Steamhammer's tech choice.** The whole
`techScores` array is recomputed each time; the previously chosen target gets a bonus, tuned
per matchup, under a one-word comment:

> *"// Hysteresis."*

> *"techScores[int(_techTarget)] += 13;"* (Zerg vs Terran)
> *"techScores[int(_techTarget)] += 11;"* (Zerg vs Protoss)
> *"techScores[int(_techTarget)] += 4;"* (Zerg vs Zerg)

**Referent check.** `_techTarget` is the previously chosen tech unit; it is assigned in the
same file from an argmax over `techScores`. The comment `// Hysteresis.` appears three times
in the file, once immediately above each of these three lines. **The bonus is largest where
switching is most expensive (ZvT, +13) and smallest where it is cheapest (ZvZ, +4)** — a
matchup-tuned commitment strength, not one global constant.

**2. A multiplicative penalty on challengers — PurpleWave's unit recruitment.** From
`src/Planning/ResourceLocks/LockUnits.scala`:

> *"* (if (units.contains(candidate)) 1.0 else 1.5))"*

**Referent check.** `units` is the set the lock already holds. A unit not already recruited
must be **1.5× better** on the preference metric to displace one that is.

**3. A time lockout in one direction only — UAlbertaBot's engage/retreat.** From
`UAlbertaBot/Source/Squad.cpp`:

> *"// we should not attack unless 5 seconds have passed since a retreat"*

> *"int switchTime = 100;"*

**Referent check.** The guard applies only when `!retreat`, i.e. the 100-frame lockout is on
**retreat → attack**; attack → retreat flips immediately. Asymmetric by construction, and the
direction is: easy to abandon, hard to re-commit.

**4. A minimum dwell on a belief — Stardust's containment flag.** From
`src/Strategist/Strategist.cpp`:

> *"// Only change our minds after at least 5 seconds"*

> *"if (currentFrame - enemyContainedChanged < 120) return enemyContained;"*

**Referent check.** `enemyIsContained()` computes an expensive multi-clause predicate; the
first line of the function short-circuits to the **cached previous answer** for 120 frames
after the last change. So the belief has a floor on how often it can flip, independent of
what the world does.

**5. A wider exit than entry, on a distance — Steamhammer's base defence.** From
`Steamhammer/Source/CombatCommander.cpp`:

> *"const int baseDefenseRadius = 19 * 32;"*
> *"const int baseDefenseHysteresis = 10 * 32;"*
> *"// Start to defend when enemy comes within baseDefenseRadius."*
> *"// Stop defending when enemy leaves baseDefenseRadius + baseDefenseHysteresis."*

A Schmitt trigger on a spatial threshold, with the only state being *"does the squad already
exist"*.

**6. A low-pass filter instead of a threshold — Steamhammer's engage decision.** From
`Steamhammer/Source/Micro.h`:

> *"inline static const double attackDecay = 0.15; // for exponential moving average"*

One double per unit; time constant ≈ 1/0.15 ≈ 6.7 frames. This is the *symmetric* version:
it damps both directions rather than favouring one.

**7. A crude multiplier where there is no state at all — Halite III's 6th place.** From
`TheDuck314`'s README:

> *"the ships were way too eager to abandon the current square for a nearby richer square"*

> *"stay on the current square unless the target square has more than 3x the halite of the
> current square"*

and Halite III rank 18, `mlomb`, running the two-threshold band on a stored flag:

> *"the ship will be assigned to drop if it was previously assigned to drop or its halite is
> > DROP_THRESHOLD (970)"*
> *"also, if a ship has < 300 halite then it exits the dropping state (if it hasn't been
> overrided)"*

**Enter at 970, exit at 300, out of a 1000 maximum cargo.**

**8. And the same idea named as such in Screeps** — TooAngel's source comment:

> *"// Use hysteresis to prevent ping-pong:"*

with entry at `downgrade/10` and exit at `downgrade/9`, the looser threshold applying **only
if the creep is already at the controller** — i.e. the commitment discount is conditional on
being already committed.

## WHY IT MIGHT TRANSFER

**This is the highest ratio of shipped-evidence to implementation-cost in the whole sweep,
and it fits our engine better than it fits theirs.**

- **It needs no store slot.** Our `Player` object persists across rounds within a match, so
  `self._last_choice[ct.get_id()]` costs nothing and never touches the 16 integers — no
  one-round buffer, no last-writer-wins, no negative-write raise.
- **It is strictly cheaper than everything else the library has filed for the same disease.**
  `defence-recall-oscillation.md` records BC2022 5 Musketeers' *"This worked but led to an
  unfortunate oscillation problem"*. The library's existing answers are an arm/disarm band
  ([`arm-and-disarm-on-different-thresholds`](arm-and-disarm-on-different-thresholds.md)) and
  a goal stack ([`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md)).
  **The incumbency bonus is a third answer and it is one line.** It also generalises the
  arm/disarm file: an asymmetric band is the two-valued special case of adding a constant to
  the incumbent.
- **Our engine punishes indecision harder than any source here.** A builder bot's action and
  movement are **mutually exclusive** — a unit that changes its mind mid-round loses the round
  entirely. Every source above pays for a flip in efficiency; we pay for it in tempo.
- **The variety is itself the useful part**: additive on a score, multiplicative on a
  challenger, a one-directional time lockout, a minimum dwell on a belief, a wider exit
  radius, an EMA. Whichever of our decisions is thrashing, one of these shapes fits it, and
  none needs a new data structure.
- **Steamhammer's per-matchup tuning is the transferable refinement.** Commitment strength
  should scale with what abandoning costs. Ours is not uniform: abandoning a *walk* costs a
  round; abandoning a *purchase* costs the titanium permanently, because `destroy()` refunds
  nothing.

## WHAT WOULD KILL IT

- **A commitment bonus is indistinguishable from a bug when it is too large.** PurpleWave's
  own hysteresis file carries the warning in its design comments: it applies a floor *"to
  avoid systematically underweighing commitment and bleeding out"*, i.e. the author found the
  failure in both directions. A +13 that should have been +4 makes a bot that never adapts.
- **Nobody measured any of these constants against a control.** Every one is a shipped
  constant in a strong bot. Evidence is `documented` for the *design*, and **there is no
  effect size anywhere in this file.** The one adjacent measurement the sweep found is a
  *negative* about a related mechanism — see
  [`every-author-who-extended-the-plan-past-one-step-said-it-did-not-help`](every-author-who-extended-the-plan-past-one-step-said-it-did-not-help.md).
- **Importing the numbers is the error sweep 16 already filed** as
  [`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md). 13, 1.5, 100,
  120, 0.15, 3×, 970/300 are all tuned against other games. **The shape transfers; the
  constants do not.**
- **It cures thrash, not timidity.** 17A's structural finding is that an
  economically-correct evaluator never commits to an assault at all. An incumbency bonus makes
  a bot stick to whatever it already chose — including sticking to *not attacking*. **This
  file must not be read as a converter.**

## BUILDER HOOK

Smallest test, and it is a measurement before it is a change: pick the decision most likely to
be thrashing — the per-builder target seat — and, without changing behaviour, `print()` the
chosen target each round per unit id. **Count transitions per unit per game.** If a unit
changes target more than a handful of times per game, add one constant: a fixed bonus to the
previous target's score, held in a dict keyed by `ct.get_id()`, no store slot. Re-run the
transition count first (it must fall) and the battery second. **If the transition count is
already low, the road is closed for the price of a print statement** — which is the same
cheapest-possible-instrument pattern the library used in
[`decide-by-simulating-both-branches`](decide-by-simulating-both-branches.md).

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/StrategyBossZerg.cpp
- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/CombatCommander.cpp
- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/Micro.h
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/Squad.cpp
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Planning/ResourceLocks/LockUnits.scala
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Strategist.cpp
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
- https://mlomb.dev/blog/halite-iii-postmortem
- https://raw.githubusercontent.com/TooAngel/screeps/master/src/prototype_creep_resources.js

- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Information/Battles/Types/JudgmentModifiers.scala

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
