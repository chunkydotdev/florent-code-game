---
tactic: (A) THE CONSTRUCTIVE ANSWER TO "PERSIST OR RE-DERIVE" — the Halite III winner got plan-like behaviour with no stored plan by proving his scoring function monotone, so a changed mind never wastes the previous move
source: https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
origin: Halite III (2018), teccles — 1st place
evidence: documented
transfers: yes
---

## WHAT IT IS

The Halite III winner recomputes every ship's target from scratch every turn. He does not
store a plan. He lists the properties he wanted from his target-scoring algorithm, and the
second one is a **regret-freeness argument**:

> *"It is pretty consistent between turns."*

> *"If nothing changes with enemies between these turns, its new target is usually (but not
> always) be T'. However, it will always be true that X' is closer to T' than X - so even if
> we've changed target, we don't regret the previous move."*

**Referent check, and it matters because the quote is dense with variables.** The
demonstrative *"It"* refers to his own **mining square-scoring algorithm**; the sentence
immediately before the list reads *"This algorithm has a few properties I think are useful,
and which other algorithms I tried early did not have all of:"*. The setup sentence
immediately preceding the quoted one defines the symbols: *"In particular, lets say a ship
is at X, selects a target T, moves towards T to X', and picks a new target T'."* So `X` is
the ship's position, `T` the target it picked, `X'` its position after one step toward `T`,
and `T'` the target it picks *next* turn. The claim is that the step taken toward the
abandoned target still made progress toward the new one.

**The same author's mechanism for the one role where stickiness matters is stated, and it is
still not a stored plan** — it is a rule plus a per-turn re-test:

> *"When ships start to return towards a dropoff or a shipyard, they carry on until they get
> there."*

> *"Every turn, a ship which is returning considers instead stopping and mining."*

The 6th-place bot arrived at the crude version of the same idea — a **multiplicative
threshold** rather than a proof:

> *"the ships were way too eager to abandon the current square for a nearby richer square"*

> *"stay on the current square unless the target square has more than 3x the halite of the
> current square"*

**Referent check.** *"the ships"* are TheDuck314's own miners; the first quote is his
description of the failure that the second quote's rule fixes. Source:
`https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md`. He also states
the architecture that makes the rule necessary: *"The main strategy code determines a
"purpose" and "destination" for every ship."* — recomputed each turn, not stored.

## WHY IT MIGHT TRANSFER

This is the answer to the sweep's central question that costs us **nothing**: no store slot,
no per-unit state, no serialisation, no CPU.

- **Our engine's whole hostility to persisted plans evaporates if the plan is not needed.**
  16 unsigned integers, buffered a round, last writer wins, no cross-match memory, a
  permanent unit death on an uncaught exception — every one of those hazards is a hazard of
  *storage*. A monotone score has no storage.
- **Our geometry makes the monotonicity argument easier than Halite's, not harder.** Builder
  bots move one cardinal step per round on a small grid. If a seat-scoring function is a
  monotone-decreasing function of Chebyshev/Manhattan distance to the seat plus a
  slowly-varying term, then a step toward seat A is a step toward the whole neighbourhood of
  A, and re-targeting to a nearby B is free. **Our current turret-seat and forward-throw
  scoring is not written this way and nobody has checked whether it is regret-free.**
- **It is a cheaper fix for the same disease the library already filed.**
  `defence-recall-oscillation.md` records BC2022 5 Musketeers' *"This worked but led to an
  unfortunate oscillation problem"*. The library's existing answers are hysteresis bands
  (`arm-and-disarm-on-different-thresholds`) and a goal stack
  (`the-goal-stack-beats-the-mode-flag`). **Score shaping is a third answer and it is the
  only one with no state at all** — and TheDuck314's 3× rule shows the degraded version
  (one constant) is also available.
- **17A's structural finding is not violated.** A regret-free score still prices each step,
  so it does *not* by itself redeem a locally-bad step. It removes *thrash*, not *timidity*.
  Those are different problems and this file only claims the first.

## WHAT WOULD KILL IT

- **Halite III has no defender's advantage and no immobile assets.** A Halite ship that
  changes its mind loses at most a turn of movement. Our damage is bought, immobile, and
  cannot be un-bought — `destroy()` is free but refunds nothing. **For a build decision
  there is no "we don't regret the previous move": the previous move was 30 titanium spent
  on a tile.** So the argument transfers to *movement and target selection*, and does not
  transfer to *purchase*.
- **Our score is not a pure function of distance.** Enemy sentinel lines (r²=32, ignoring
  obstacles) and the cost scale — one global additive team factor that every build raises —
  make the value of a seat depend on things that move and on our own spending. Monotonicity
  would have to be checked, not assumed, and the check is the work.
- **teccles measured nothing here.** He states the property as a design goal and reports
  that earlier algorithms lacked it; there is no ablation. Evidence is `documented` for the
  *design*, not for the *effect*.
- **The same author's negative is filed beside this** — see
  [`every-author-who-extended-the-plan-past-one-step-said-it-did-not-help`](every-author-who-extended-the-plan-past-one-step-said-it-did-not-help.md).
  He is not arguing that plans are unnecessary in general; he is reporting that in his game
  the shaped score beat the plans he tried.

## BUILDER HOOK

Smallest test, and it changes no behaviour: instrument the existing target-selection for one
unit class. Each round, log `(chosen_target, distance_to_chosen, distance_to_previous_target)`
via `print()`. **Count the rounds where the unit moved and the new target is *further* than
the old one was before the move** — that is the literal regret event. If the count is near
zero, our score is already regret-free and there is nothing here. If it is high, we have
found an oscillation source with a print statement, and the fix is one distance term, not a
store slot.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
