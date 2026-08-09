---
tactic: (A) THE FIELD'S BASELINE ANSWER, AND IT IS A NEGATIVE — across five leagues the modal winning representation is NO stored plan at all: a cost function recomputed over every unit × tile pair each turn, made to LOOK like a plan by shaping the score or by one crude constant
source: https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
origin: Halite III (teccles 1st, TheDuck314 6th, aidenbenner 7th, mlomb 18th); Lux AI S1 (Toad Brigade, 1st); RoboCup Gliders2012; Battlecode 2026 "food"; PurpleWave (StarCraft AI)
evidence: documented
transfers: yes
---

## WHAT IT IS

The sweep's sub-question (A) asked for the difference between a plan that **persists** and a
policy that **re-derives the same answer each turn**. The field's answer, by weight of
winners, is re-derivation — and it is worth having the evidence in one place so nobody has to
re-establish it.

**Halite III, top of the ladder.** The winner scores every candidate square for every ship,
every turn: *"For every non-returning ship, calculate a score for every square."* and *"Ships
claim their favourite targets (that is, the ones with the minimum score for the ship). Ships
which are nearer a target get priority over those further away."* The 6th place is identical
in shape: *"The main strategy code determines a "purpose" and "destination" for every ship."*
and *"every miner scores every square on the map, and sets its destination to be the square
with the best score"*. The 7th place upgraded the *assignment algorithm* rather than adding
memory: *"Let each tile on the grid and each ship be nodes that form two bipartitions in a
graph where the edges between the bipartitions are the cost of turtle X to go to square Y."*
solved by *"the Hungarian algorithm which finds a min cost max matching efficiently"* —
**re-solved from scratch every turn.**

**Lux AI Season 1's winner holds no plan at all.** Toad Brigade:
*"I opted instead to have a single network which issued commands for each worker, cart, and
city tile on all squares of the board simultaneously."*

**RoboCup has the trap case, and a 2012 team ran it.** Gliders2012's "tactics" look like plans
and are not: *"This approach does not impose tactics in a top-down fashion, selecting one
tactic and the sub-selecting the best action for the chosen tactic."* and *"Rather, all
feasible actions are considered, and tactics contribute to the"* evaluation. **Nothing is ever
adopted, so nothing can be abandoned.**

**Battlecode 2026's `food` re-derives its state every turn** from an ordered condition list,
with the author's stated aim *"My goal was to have as few states as possible."*

**And even PurpleWave — which had a declarative plan DSL and deleted it — re-derives its
production timeline every planning tick**, `MacroSim.simulate()` beginning with
`steps.clear()`.

**What substitutes for commitment is one of two things, and both are cheap:**
1. **A shaped score**, so re-derivation never regrets its predecessor — teccles' argument,
   filed separately in
   [`shape-the-score-so-a-re-derived-choice-never-regrets-the-last-one`](shape-the-score-so-a-re-derived-choice-never-regrets-the-last-one.md).
2. **One constant** — TheDuck314's 3×, mlomb's 970/300 band — filed in
   [`add-a-constant-to-the-incumbents-score`](add-a-constant-to-the-incumbents-score.md).

## ⚠ THE COUNTEREXAMPLE, AND IT IS A WINNER TOO

**Lux AI Season 2's 1st place persists everything.** ry_andy_'s Python agent —
*"This Python agent placed 1st out of 646 teams in"* Lux AI Season 2 — carries an explicit
cross-turn blackboard:

> *"# Only one role/goal per unit. Only saved here once per invocation."*
> *"self.roles = {} # {unit_id: serialized Role}"*

with roles serialised across turns, ~13 distinct role classes, a persisted route per unit, and
named `is_valid()` abort predicates and `from_transition_*` guards on each role. **So the modal
answer is re-derivation and the mode is not unanimous** — and the counterexample is the more
recent one.

## WHY IT MIGHT TRANSFER

- **It sets the correct default for us, and the default is the cheap one.** Before adding any
  persistence, the question is whether a shaped score plus one constant does the job — because
  that is what most of the winners shipped.
- **Every hazard our engine has is a hazard of storage.** 16 buffered integers, last writer
  wins, no cross-match memory, a permanent unit death on an uncaught exception, 10 ms per unit.
  **A policy that stores nothing pays none of those costs.**
- **Our per-unit scoring is already this shape.** `get_nearby_tiles(dist_sq)` plus a score is
  the exact Halite idiom, and our maps are 8×8 to 30×30 against Halite III's 32×32 to 64×64 —
  **smaller, so the full re-score is cheaper here than where it won.**
- **The Lux S2 counterexample tells us what the price of persistence is**, and it is not the
  storage: it is that **every persisted role needs an explicit validity predicate and explicit
  guarded transitions.** That is the tax, and it is the same tax
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md)
  describes.

## WHAT WOULD KILL IT

- **Halite III is a solitaire economy game with no defender's advantage and no buildings.** Its
  ships are cheap, mobile, and interchangeable; a wasted turn costs a turn. **Our damage is
  immobile, bought, and unrefundable.** The class of decision where re-derivation is safe —
  movement and target choice — is not the class where our games are decided.
- **Re-derivation is what an economically-correct evaluator does, and 17A established that an
  economically-correct evaluator never finishes.** A per-turn re-scoring bot prices every step
  by its own return and is therefore *correct* to refuse every step of an assault. **This file
  documents the field's default; it does not endorse it for our problem.**
- **The counterexample is more recent and in a game closer to ours** (Lux S2 has factories,
  buildings and a resource economy). One winner each way is not a consensus.
- **Gliders2012 placed 4th, not 1st**, and none of these authors ran the comparison; these are
  descriptions of what shipped, not ablations.

## BUILDER HOOK

None — this is the field's baseline, filed so a future session does not have to re-derive it.
Its operational form is a **question to ask of any persistence proposal**: *what does storing
this buy that a shaped score plus one incumbency constant does not?* If the answer is "it
survives an interrupt", the cheap version is
[`one-line-of-interrupt-that-remembers-what-it-interrupted`](one-line-of-interrupt-that-remembers-what-it-interrupted.md);
if it is "several units must agree", the cheap version is
[`one-writer-names-the-mode-and-the-rest-obey`](one-writer-names-the-mode-and-the-rest-obey.md).

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
- https://raw.githubusercontent.com/aidenbenner/halite3/master/README.md
- https://raw.githubusercontent.com/IsaiahPressman/Kaggle_Lux_AI_2021/main/README.md
- https://raw.githubusercontent.com/ryandy/Lux-S2-public/main/README.md
- https://raw.githubusercontent.com/ryandy/Lux-S2-public/main/luxry/strategy.py
- https://arxiv.org/pdf/1211.3882 (Prokopenko & Wang, *Gliders2012*)
- https://www.alext.app/Battlecode_Postmortem_2026.pdf
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Macro/Scheduling/MacroSim.scala

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
