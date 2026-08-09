---
tactic: (D) THE PRICE TAG NOBODY PUTS ON A PLAN REPRESENTATION — the author of the most-documented Screeps AI profiled his own hierarchical planning layer and found rebuilding it each tick cost nearly as much as running the whole bot; making it persist cut CPU by over 40%
source: https://bencbartlett.github.io/blog/screeps-6-verifiably-refreshed/
origin: Overmind / Ben Bartlett (Screeps)
evidence: documented
transfers: yes
---

## WHAT IT IS

Overmind is a four-level hierarchy — Colony, Directive, Overlord, Task — and the most complete
open plan representation in any of the leagues this library sweeps. Its author's own account of
what that cost:

> *"Prior to some recent changes, Overmind had never been a terribly CPU-efficient bot. A major
> reason for this is its very hierarchical, object-oriented architecture, which heavily employs
> classes."*

The profiling result, and the fix:

> *"the caching changes have reduced CPU cost by over 40%!"*

**Referent check.** *"the caching changes"* are the new `refresh()` phase that replaces full
re-instantiation of the object hierarchy on all but every twentieth tick. **The number carries
its subject: it is the CPU cost of his own bot, measured by his own profiler on the Screeps
public servers, before versus after that change. There is no comparison bot and no win-rate
figure.**

**And the same author names where the abstraction stops working:**

> *"While they are good at most actions, they aren’t the most flexible design, so they are bad
> for more complex scenarios where multiple actions should be executed, such as healing and
> attacking at the same time while trying to maintain a certain range."*

**Referent check.** *"they"* is **Tasks** — the sentence directly follows his positive
assessment, *"Tasks are generally pretty good and minimize much of the decision-tree overhead
that many AI’s feature, since a creep only needs to request a new task when its old one becomes
invalid."* **So the same object that saves CPU on economy cannot express combat**, where
several actions must happen at once.

**He also deleted a layer outright.** From an earlier post in the same series:

> *"the first change you’ve probably noticed is that there are no more roles!"*

**Referent check.** *"roles"* are the per-creep-type Role classes that governed creep control
logic; they were folded into the new Overlord class. **(Glyph note: this string uses a CURLY
`’` in `you’ve`, and so does the Task quotation above — the sweep's discovery leg reported the
ASCII form for one of them and it does not grep. Both were corrected on re-verification.)**

## WHY IT MIGHT TRANSFER

- **It is the only CPU price tag on a plan representation anywhere in the sweep, and CPU is our
  hardest constraint.** 10 ms per unit per turn, and an overrun **silently discards that unit's
  turn** — no exception, no log. A representation whose construction costs as much as its
  execution is exactly the shape that produces silent turn loss.
- **The failure was in CONSTRUCTION, not in execution**, and that is the actionable half. His
  fix was to stop rebuilding the hierarchy every tick and refresh it instead. **Our engine
  gives us the analogous property for free: `run()` is called on the same `Player` object every
  round, so anything we build once stays built.** Rebuilding a per-unit object graph inside
  `run()` is the mistake, and it is easy to make in Python without noticing.
- **His combat caveat lands directly on our problem.** A task object says "do X to Y until Z".
  Our decisive moments are not like that: a builder next to a besieged core wants to heal *and*
  the team wants damage placed *and* the seat must stay occupied. **The library's own arithmetic
  — one heal repairs both a friendly bot and a friendly building on the same tile, 8.00 HP/Ti on
  a stacked tile — is precisely a "several things at once" situation.** A single-target task
  representation cannot express it.
- **Deleting the role layer is a second datapoint in the same direction as
  [`a-tournament-winning-bot-deleted-its-plan-representation`](a-tournament-winning-bot-deleted-its-plan-representation.md).**
  Two independent authors of two heavily-architected bots both removed a layer of their own
  plan hierarchy.

## WHAT WOULD KILL IT

- **Screeps' CPU model is nothing like ours.** Screeps gives a per-tick budget for the *whole
  colony* with a bucket that accumulates unused CPU; ours is per unit, per turn, with **no
  bucket** — the 5% rolling buffer is small and the penalty is losing that unit's turn.
  Cross-league CPU numbers do not transfer as numbers.
- **The 40% is a before/after on one bot with no control.** It is a genuine profiling result
  about a real cost; it is not evidence that hierarchies are bad, only that *rebuilding* one
  every tick was expensive for him.
- **JavaScript object construction versus Python's is a different cost curve**, and the Screeps
  global-reset model (the heap is cleared at unpredictable intervals) is a pressure we simply
  do not have. Our `Player` object survives the whole match.
- **Nothing here is about strength.** No win rate, no ladder position, no ablation. Evidence is
  `documented` for the cost, silent on the benefit.

## BUILDER HOOK

A profiling check, not a build, and it costs one line: at the top and bottom of `run()` for one
unit class, capture `ct.get_cpu_time_elapsed()` and `print()` the delta, plus the delta across
just the setup portion. **The deliverable is the ratio of setup to decision.** If our per-round
setup — rebuilding lists, dicts, or neighbourhood scans that could be cached on the `Player`
instance — is a large share of the budget, that is Overmind's bug in our code and it is fixable
without changing any behaviour. Our own measured 0.00% discarded-unit-turn rate says we are not
yet paying this, which makes it a cheap check with a likely-null result — worth doing once, and
worth re-doing before any expensive feature ships.

## SOURCES QUOTED IN THIS FILE

- https://bencbartlett.github.io/blog/screeps-6-verifiably-refreshed/
- https://bencbartlett.github.io/blog/screeps-0-a-brief-history-of-game-time/
- https://bencbartlett.github.io/blog/screeps-1-overlord-overload/

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
