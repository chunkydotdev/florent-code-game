---
tactic: (A) HOW A MULTI-UNIT PLAN SURVIVES A UNIT DYING — the plan's steps name ROLES, and roles are filled by whoever currently holds them. Nothing in the plan ever refers to a specific agent
source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
origin: RoboCup CMUnited (Stone & Veloso 1999); Stardust (2nd AIIDE 2025); Battlecode 2021 wololo (7th)
evidence: documented
transfers: yes
---

## WHAT IT IS

Stone & Veloso's set-plays are multi-agent plans, and the indirection that makes them robust is
stated explicitly:

> *"set-play roles are not assigned to pre-determined agents; instead they are filled by
> whichever agent is filling the appropriate role in the team"*

**Referent check.** The sentence completes *in the team’s current formation* — the verified
literal span stops at `team` because the source uses a curly apostrophe in `team’s`. The preceding
sentence supplies the mapping: *"The locker-room agreement also includes a general function to
map roles in a formation to roles in a set-play"*. **So a plan step says "the left midfielder
does X", never "player 7 does X".**

**The same indirection is how the plan is restored after an interrupt** — the termination
condition says the agent *"should cease filling the set-play role and resume its normal
behavior"*, and "normal behavior" is defined by the formation role, which was never lost.

**Stardust implements the same idea as a greedy per-frame reassignment under a priority
order.** Its Strategist holds a list of `Play` objects, each declaring the units it wants
(`PlayUnitRequirement`: a count, a type, a position, a distance limit), and the assignment loop
reads:

> *"// Process each play"*
> *"// They greedily take the reassignable units closest to where they want them"*
> *"// This also makes them unavailable to later (lower-priority) plays"*

**So the plan states a requirement, not a roster**, and the roster is recomputed every frame
from whoever is alive and nearby. A unit's death removes it from `unitToPlay` and the next
frame's assignment fills the gap.

**UAlbertaBot's version is the cheapest of the three: a monotone ratchet.** Its squad
assignment rule is one line with a one-line comment:

> *"// make sure strictly less than so we don't reassign to the same squad etc"*

— a unit can only ever move to a **strictly higher**-priority squad, never back down. Combined
with `isSquadUpdateFrame()` returning true only when `getFrameCount() % 10 == 0`, roles persist
by construction: they can only escalate, and only every tenth frame.

**And Battlecode 2021's wololo made the role externally visible**, assigning it at build time
and broadcasting it through the unit's flag — *"my code assigned each unit a “role”, which
described the functional portion of the strategy which the unit helped to execute, and the
manner in which it did so."*

## WHY IT MIGHT TRANSFER

**Our engine makes agent-naming actively dangerous, and role-naming free.**

- **Entity ids are useless as stable names.** The library measured that ids come from **one
  global counter shared with resource stacks** — 97,455 of the id gaps are stack ids — so
  **id MAGNITUDE is meaningless** and only ordering carries information. A plan that stores
  "unit 4127 does step 3" stores a number that will be dead in twenty rounds and cannot be
  reconstructed.
- **A role is a predicate, and predicates cost nothing to re-evaluate.** "The builder nearest
  the enemy core", "the builder orthogonally adjacent to a damaged friendly building" — both
  are computable by any unit from its own getters, and both survive that unit dying.
- **Our units die constantly at exactly the moment a plan matters.** The library's own
  measurement: raider survival falls from 43 rounds to 6 at r150. **Any plan that names a
  specific builder is a plan with a 6-round expected lifetime.**
- **It is the missing piece for a plan-index store.**
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)
  puts the plan in code and one index in a slot. **Role indirection is what lets that work
  without any per-unit slot at all**: each unit reads the index, evaluates which role it
  currently fills, and executes that role's step. Zero additional bandwidth.
- **UAlbertaBot's monotone ratchet is the anti-thrash device that comes free with roles.** A
  role that can only escalate cannot oscillate.

## WHAT WOULD KILL IT

- **Role predicates need a tie-break, and ours cannot be resolved through the store.** If two
  builders both believe they are "the nearest to the enemy core", both execute the step. The
  store cannot arbitrate — writes are buffered a round and last writer wins, and the
  read-increment-write ticket idiom is **measured to collapse silently**. The safe tie-break
  here is the one the engine already gives us: **turn order is global entity-id ascending, 0
  inversions over 1,842,445 ordered pairs**, so "lowest id among candidates" is a total order
  every unit can compute identically from `get_nearby_units()` — *within vision*. Outside
  vision it cannot, and that is a real hole.
- **Our vision is the binding constraint, not our bandwidth.** Stone's agents hear a
  broadcast; Stardust's Strategist is a single global object with full information. **Our
  builder sees r²=20 and there is no global observer.** A role defined over the whole team is
  not evaluable by any unit.
- **Stardust's greedy reassignment is O(plays × units) every frame with full information.** Our
  equivalent runs inside 10 ms per unit with partial information, and a unit cannot see the
  assignment other units made until next round.
- **The measured evidence covers set-plays as a bundle, not role indirection alone** — see
  [`set-plays-were-ablated-and-set-plays-won`](set-plays-were-ablated-and-set-plays-won.md).
  Stone's *"Only Flexible Positions"* leg is the closest isolation and it tests flexible
  positioning, which is related but not identical.

## BUILDER HOOK

Smallest test, and it is a refactor with a measurable output: wherever the bot currently
decides "this specific builder is the forward one", replace the stored id with a **predicate
evaluated each round** — lowest-id builder within r²=20 of the target, say — and `print()` the
id it resolves to. **Count how often the resolved id changes and how often two units in the
same round both resolve to themselves.** The second count is the tie-break failure this file
warns about, and it is zero or it is not; either way it is answered for the price of a print.

## SOURCES QUOTED IN THIS FILE

- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Strategist.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/SquadData.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/CombatCommander.cpp
- https://battlecode.org/assets/files/postmortem-2021-wololo.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). `isSquadUpdateFrame()`'s body verifies as
`return BWAPI::Broodwar->getFrameCount() % 10 == 0;` in `CombatCommander.cpp`.
