---
tactic: (D) FOUR TEAMS DELETED A MULTI-STEP ROUTINE AND GOT BETTER — including a Battlecode finalist who found half its units' lifetimes were spent executing a go-and-come-back errand that no other top team bothered with
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 The Kragle; Battlecode 2023 don't @ me (7th); Battlecode 2021 wololo (7th); Overmind (Screeps)
evidence: documented
transfers: yes
---

## WHAT IT IS

**1. The Kragle deleted the refill errand.** Their units had a multi-step routine: run out of
paint, walk back to a tower, wait, walk out again.

> *"Our robots would spend about half of their lifetime traveling back to towers and waiting
> around towers for paint."*

> *"Only after we started looking carefully at what other teams were doing did we notice that
> no other team bothered having their bots refill on paint."*

**Referent check.** *"we"* is team The Kragle; the section is titled *Reducing Idle-Time*. The
sentence before the first quote states the consequence in their own words: the robots *"would
spend about half of their lifetime in an idle state, not contributing anything."* The
replacement is to let units die and be rebuilt.

**2. don't @ me deleted a central assignment planner.**

> *"We ended up removing the entire HQ assignment system, detached well assignment decisions
> from the HQ, and placed it entirely onto the carriers."*

**Referent check.** *"We"* is team don't @ me (7th, BC2023). The preceding sentences give the
trigger: a rules update let HQs spawn 5 units in one turn, which made their assignment
procedure unviable *"unless carriers waited near the HQ until they received their command"*.
**A centre that hands out tasks was replaced by each unit deriving its own assignment — and
that was the improvement.**

**3. wololo deleted a multi-unit coordination plan.**

> *"I later removed the relay chain behavior because it would cause my explorers to have
> trouble splitting their focus to target multiple locations at once."*

**Referent check.** *"the relay chain behavior"* is his explorers' scheme for relaying target
information back to home Enlightenment Centres, described in the same bullet.

**4. Overmind deleted its role layer** — *"the first change you’ve probably noticed is that
there are no more roles!"* — folding all creep control logic into a single Overlord class. See
[`the-planning-layer-cost-as-much-cpu-as-executing-it`](the-planning-layer-cost-as-much-cpu-as-executing-it.md).

## ⚠ AND THE SAME TEAM ADDED A GOAL STACK FOR THE OPPOSITE REASON

The Kragle is the team the library already quotes for *"We decided to use a stack for the
goals"*. **The new context this sweep found is what forced it, and it is the same errand:**

> *"Often, ruins would be abandoned when robots went back to get their paint refilled, since
> they were the only robot that knew it was in progress. After refilling paint, they would act
> as if they were a new soldier."*

**So one team both (a) built a goal stack because the refill errand destroyed their units'
plans, and (b) later deleted the refill errand entirely once they noticed nobody else ran it.**
The second fix subsumes the first. **The cheapest solution to an interrupt that wrecks your
plans may be to delete the interrupt.**

## WHY IT MIGHT TRANSFER

- **We have a candidate errand with the same shape and it is measured.** Our builders' movement
  is suppressed 4.4× when adjacent to a damaged core — **15.5% of rounds against 68.3% at full
  HP, n = 143,812**. That is our refill errand: a locally-correct routine that consumes unit
  lifetime. **Nobody has ever asked what our bot's win rate is with it disabled.**
- **The Kragle's method is the transferable part, not their conclusion.** They found it by
  *watching what the top teams did not do*, which the library already holds as
  [`measure-what-the-top-tier-never-does`](measure-what-the-top-tier-never-does.md) — and this
  is that method producing a concrete, large win in a strong team's own account.
- **It matches our project's whole history.** Every gain on our current line came from removing
  a mechanism. Four independent teams in three leagues report the same direction.
- **don't @ me's finding is a direct warning about the plan-index design.**
  [`one-writer-names-the-mode-and-the-rest-obey`](one-writer-names-the-mode-and-the-rest-obey.md)
  proposes the core as a single designated writer. **don't @ me removed exactly that pattern
  because units ended up waiting on the centre.** Our store's one-round buffer makes waiting
  the default failure: any unit that acts only after reading a slot is a unit that idles a
  round. **The mode index must be advisory, never a permission.**

## WHAT WOULD KILL IT

- **None of the four measured it.** The Kragle report their own replay observation and a
  qualitative verdict (*"It cuts down on robot idle time, and allows robots to perform longer
  tasks at the cost of chips."*); don't @ me and wololo report a change and a reason. **No
  win rates, no game counts, no controls.**
- **Deleting an errand is only right when the resource it services is cheap to replace.** The
  Kragle's replacement for refilling is dying and being rebuilt, which works because their
  units were cheap. **Ours are not: builder bots cost `get_builder_bot_cost()` at +20%
  scaling, and cost scale is one global additive team factor, so churning units raises the
  price of the turrets we need.** The arithmetic is genuinely different here and it points the
  other way.
- **Our heal errand is not obviously the same object.** Healing is our measured strength —
  4.00 HP/Ti against a best damage of 1.80 HP/Ti, 8.00 on a stacked tile — and the library's
  standing reading is that **home defence is our measured asset (+11.4 / +16.6 / +22.3pp over
  the field)**. Deleting the thing we are best at because a Battlecode team deleted an
  unrelated errand would be the crudest possible misreading of this file.
- **Selection bias again.** Teams write up the deletions that worked.

## BUILDER HOOK

The measurement first, and it is a corpus cut rather than a bot change: **compute the share of
our builder-bot lifetime spent in the core-heal pin**, using the same instrument that produced
the 15.5%/68.3% split, and compare it against the top tier's equivalent. If our units spend a
Kragle-sized fraction of their lives on an errand the top tier does not run, that is the
finding. Only then is an ablation warranted, and it must be an ablation — the errand disabled,
everything else byte-identical — because the library's own history says a proxy metric will
mislead here.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
- https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
- https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
- https://bencbartlett.github.io/blog/screeps-1-overlord-overload/

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
