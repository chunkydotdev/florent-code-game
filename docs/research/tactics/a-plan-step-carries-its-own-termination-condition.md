---
tactic: (A)+(B) THE PLAN OBJECT THE FIELD CONVERGED ON — trigger + behaviour + TERMINATION CONDITION, with the termination condition stored on the step itself rather than in the code that inspects it. Four independent arrivals, 27 years apart
source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
origin: RoboCup CMUnited (Stone & Veloso 1999); STEAM (Tambe, JAIR 1997); Overmind (Screeps); Stardust (StarCraft AI, 2nd AIIDE 2025)
evidence: documented
transfers: yes
---

## WHAT IT IS

Ask four different literatures what a multi-step plan is made of and they answer with the same
three-part object. The termination condition is the part that keeps being missed when people
implement this from memory, and it is the part that matters.

**1. RoboCup — the formal definition.** Stone & Veloso define a set-play as a **trigger** plus
a set of roles, each of which carries a **behaviour** and a **termination condition**:

> *"A trigger condition indicating the set of states in which the set-play is activated"*

> *"A termination condition indicating the set of states in which an agent should cease
> filling the set-play role and resume its normal behavior."*

**And their concrete instantiation gives the termination condition two disjuncts, one of
which is a timeout:**

> *"Each player leaves its set-play role to resume its former role either after successfully
> kicking the ball, or after a pre-specified, role-specific amount of time."*

**Referent check.** *"its former role"* is the role the player held in the team formation
before the set-play fired; the mechanism for restoring it is the formation itself, not a saved
variable — see
[`the-plan-names-a-role-not-a-unit`](the-plan-names-a-role-not-a-unit.md).
**Success OR timeout, per role. Nothing can be stranded in a plan whose success never
arrives.**

**2. Teamwork theory — the same triple, stated as three exit conditions.** Tambe's STEAM,
building on Cohen & Levesque's Joint Persistent Goal:

> *"a JPG guarantees that team members cannot decommit until p is mutually believed to be
> achieved, unachievable or irrelevant"*

> *"agents should monitor conditions that cause the team activity to be achieved or
> unachievable or irrelevant, and maintain the team activity at least until one of these
> conditions arises"*

**Referent check.** `p` is the team task; `JPG` is the Joint Persistent Goal the paper builds
on. **The commitment is defined by its termination test, not by a duration** —
achieved / unachievable / irrelevant — and the *"maintain … at least until"* clause is what
makes a locally-bad step survivable.

**3. Screeps — the same object, as code.** Overmind's `Task` base class documents itself as
this exact generalisation (**note: the doc comment wraps, so each fragment below is a separate
verified string; the reconstruction across the `*` continuation is stated, not quoted**):

> *"This generalizes the concept of "do action X to thing Y until"* … *"condition Z is met"
> and saves a lot of convoluted and duplicated code in creep logic."*

and

> *"the necessary logic for traveling to a target, performing a task, and realizing when a
> task is no longer sensible"* … *"to continue."*

**The termination test is split in two, and the split is the buildable part:**

> *"	 * Test every tick to see if task is still valid"* → `abstract isValidTask(): boolean;`
> *"	 * Test every tick to see if target is still valid"* → `abstract isValidTarget(): boolean;`

**`isValidTask` asks about the ACTOR — can I still do this. `isValidTarget` asks about the
WORLD — is this still worth doing.** Both are one-liners in every concrete instance. And the
dispatcher does the pop:

> *"	 * Test if the task is valid; if it is not, automatically remove task and transition to
> parent"*

> *"// Return if the task is valid; if not, finalize/delete the task and return false"*

> *"const isValid = this.parent ? this.parent.isValid() : false;"*

**4. StarCraft — the same object, in the bot that came 2nd at AIIDE 2025.** Stardust's `Play`
carries its own status, and the status *is* the termination condition:

> *"bool complete = false;"*
> *"std::shared_ptr<Play> transitionTo = nullptr;"*

consumed by the Strategist:

> *"// They signal interesting changes to the Strategist through their PlayStatus object."*
> *"// Handle play transition"*
> *"// This replaces the current play with a new one, moving all units"*
> *"// Erase the play if it is marked complete"*

**A plan declares its own completion and names its own successor.** Nothing outside the plan
needs to know when it is done.

## WHY IT MIGHT TRANSFER

- **The three-part object costs one tuple in Python and no store slots.** A mode entry is
  `(arm_predicate, act, terminate_predicate)`; the whole table is a module-level constant, so
  every unit holds it identically (see
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)).
- **Our library has been building the trigger half and skipping the exit half.**
  `arm-and-disarm-on-different-thresholds.md`, `local-force-count-is-the-engage-gate.md`,
  `branch-on-a-milestone-not-a-round-number.md` and `the-rush-cost-budget-gate.md` are all
  arming conditions. **Four independent literatures say the exit condition is a co-equal part
  of the object, and one of them (Stone) makes the timeout disjunct mandatory.**
- **The actor/world split maps onto our getters exactly, and both halves are cheap.**
  `isValidTask` for a builder heading to a forward seat: `get_hp() > threshold` and
  `get_action_cooldown() == 0`. `isValidTarget`: `can_build_gunner(seat, dir)` — which the
  engine already computes and which is **strictly stronger than `is_tile_empty`**, so it
  catches exactly the cases where the plan quietly became illegal.
- **It is the constructive complement to the goal stack the library already holds.**
  [`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md) documents
  BC2021 and BC2025 pushing and popping goals but records no *validity* test; that file's own
  "WHAT WOULD KILL IT" says **"A stack that is never popped is a memory leak with extra
  steps"**. Overmind's `isValid()` is the missing pop condition, and it recurses to the
  parent, so a dead child cannot pin the stack.
- **Re-validation on resume is required here for a reason the sources do not have.** A tile
  that was a good seat 40 rounds ago may now sit inside an enemy sentinel's line (r²=32,
  ignores obstacles). `isValidTarget` is where that check belongs.

## WHAT WOULD KILL IT

- **A termination condition that can never be observed is worse than no plan.** Our engine's
  vision is per-unit and limited (builder r²=20); a plan whose exit test depends on something
  the executing unit cannot see will never fire. Every predicate must be answerable from the
  *executing unit's own* getters or from the store.
- **`transitionTo` invites an infinite loop.** Stardust's plans name successors; two plans
  that name each other under complementary conditions will alternate forever. Combine with
  the minimum-dwell device in
  [`add-a-constant-to-the-incumbents-score`](add-a-constant-to-the-incumbents-score.md).
- **Overmind pays for this with real per-creep memory, serialised to a persistent JSON store;
  we have 16 buffered integers.** The per-unit half of it fits on the `Player` instance keyed
  by `ct.get_id()` and dies with the unit. **Anything two units must agree on cannot live
  there.**
- **None of the four measured the termination half in isolation.** Stone measured the whole
  set-play mechanism (see
  [`set-plays-were-ablated-and-set-plays-won`](set-plays-were-ablated-and-set-plays-won.md));
  the other three are shipped designs. Evidence is `documented` for the design.

## BUILDER HOOK

Smallest test, and it is a parity-preserving refactor before it is a feature: take one
existing multi-round behaviour in the bot (the forward-seat walk is the obvious candidate) and
give it an explicit `_still_valid(ct)` returning `can_build_<type>(seat, dir) and
get_hp() > floor`, plus a round-count timeout. **While the predicate is true, behaviour must
be byte-identical.** Then log how often it returns false and why. **The count of "the plan
was already illegal and the unit kept walking" rounds is the number this file exists to
produce** — and if it is zero, the road is closed cheaply.

## SOURCES QUOTED IN THIS FILE

- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
- https://arxiv.org/pdf/cs/9709101 (Tambe, *Towards Flexible Teamwork*, JAIR 7:83-124, 1997)
- https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/tasks/Task.ts
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Play.h
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Strategist.cpp

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). **Method note for the Overmind quotes: JSDoc block
comments put a ` * ` at the start of every continuation line, and that marker SURVIVES
whitespace flattening — so any quote spanning a line break inside a block comment fails the
literal grep even though the text is correct.** The two Overmind doc-comment quotes above are
therefore given as adjacent verified fragments with the join stated, not smoothed into one
string.
