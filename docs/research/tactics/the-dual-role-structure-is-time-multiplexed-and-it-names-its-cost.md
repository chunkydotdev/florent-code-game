---
tactic: The field's answer to "one structure, two roles" is TIME-MULTIPLEXING, not compromise siting — and the team that shipped it lists the exact vulnerability it opens
source: https://raw.githubusercontent.com/nknguyenhc/Terminal-Lostkids/main/README.md
origin: Terminal (Correlation One / Citadel), APAC region, team Lostkids — 3rd place overall, shortlisted to the final round
evidence: documented
transfers: partial
---

## WHAT IT IS

Arm D asked how anyone with a dual-purpose defensive investment decided placement so one
role did not compromise the other. **Lostkids' answer is that they did not solve it by
placement at all. They solved it in TIME: the same wall structure is a seal on some turns
and a gate on others, switched by two live booleans.**

> *"Opening and closing the entrances depending on whether the algorithm is attacking and
> whether the enemy is attacking."*

The structure's defensive job is to funnel — *"the structure maximises the exposure of our
turrets on enemy's units, thereby maximising damage on enemy's units"* — and its offensive
job is to let their own mobile units out. Those are incompatible in space and compatible
in time.

**And they publish the price in their own Weaknesses section, which is why this file
exists rather than a generic "dual-purpose is good" note:**

> *"Our defense opens up the side when we are attacking, which also means it is vulnerable
> against enemies using same side attack."*

**That is the complete accounting: the dual-role structure is defensively sound except in
exactly the window when it is doing its offensive job, and an opponent who attacks the
side we are attacking through gets in for free.** Nobody else in the corpus names the
cost of dual-purposing at all.

**A second Lostkids line makes the structure cheap to hold rather than cheap to build:**

> *"Refund weak walls and turrets and replace with new walls and turrets."*

They report the effect as consistency rather than power: *"Our structure performs
consistently well due to the refund actions, which ensures that our walls can withstand
enemy units' damage on movement."*

## WHY IT MIGHT TRANSFER — against our ruleset

**We have the primitive and it is unusually strong here.** `destroy(building_pos)` on an
allied building from an orthogonally adjacent tile is **free, has no cooldown, and is
unlimited per turn**. A barrier is 3 Ti and +1% scale, and **destruction removes the
contribution** — so opening and re-sealing a barrier gate costs 3 Ti and one builder turn
per re-seal, with the scale contribution returning to where it started. **A time-
multiplexed seal is not merely possible in our ruleset; it is nearly free, which is not
true in Terminal where refunds are partial.**

**The role conflict Lostkids solved is one we demonstrably have.** s30 measured
`barrier-seal-off` at 399/1024 — the seal is paying — while `R1000_IS_DEFEAT` and the
kill window demand our raiders get OUT. **A seal that is a wall when nothing of ours is
crossing it and a gate when something is, is the shape that serves both, and the state it
needs is one bit.**

**The two booleans have direct readings.** *"whether the algorithm is attacking"* is a
store slot our raid code can already set; *"whether the enemy is attacking"* is a live
look, `get_nearby_units()` filtered by team, at the core.

**What does NOT transfer is the turret half.** Lostkids' funnel exists to route enemies
past turrets. Our gunner's line stops at the first targetable tile, so **our own barrier
is an obstruction to our own gunner** — the library already carries this as
[`the-blockade-blanks-your-own-guns`](the-blockade-blanks-your-own-guns.md). A sentinel
ignores obstacles and does not have the problem. **So the funnel role is sentinel-only
here and the gate role is barrier-only, and combining them is a different design from
theirs.**

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**This is the strongest structural claim in the sweep for clearing the bar, and it is
also the one most likely to fail it in an unexpected direction.**

* **Why it should clear:** the defensive structure is already built. Multiplexing adds no
  new build, no new scale contribution, and its OFFENSIVE state exists precisely to stop
  the defence delaying our own exit. If our raiders currently walk around a seal, the
  gate strictly *reduces* time-to-contact.
* **Why it might fail anyway, and this is the falsifier to pre-register:** each open/close
  cycle costs **a builder turn to destroy and a builder turn plus 3 Ti to rebuild**, and
  those turns come from a builder standing at our own perimeter — i.e. a builder that is
  not forward. **A multiplexer that thrashes costs more builder-turns than the walk it
  saved.** The cost is bounded by cycle count, so the cycle count must be capped and
  reported.

**What would show it slowed the kill:** median kill round rising, with **gate cycles per
game** and **median round of our first forward build** printed beside it. If gate cycles
are high, it is thrash; if the first forward build is LATER in treatment, the gate is
being held shut when it should be open.

## WHAT WOULD KILL IT

* **Terminal is not our game.** It is a lane-based tower defence with a fixed 28x28 arena,
  a two-currency economy and no mobile builder; the transfer is at the level of the DESIGN
  PATTERN (one structure, two states, switched on live booleans), not any mechanic.
* **Their own weakness clause is the honest killer.** If our opponents attack along the
  lane our raiders leave by — and our raiders leave by the shortest line to their core,
  which is also the shortest line from it — **the open state and the threat direction are
  positively correlated**, which is worse than random. Lostkids report exactly this and
  rank high anyway *"because not many people use redirection against scout spams"*, i.e.
  their exposure went unpunished by their field. **Ours is a field where our core dies in
  46.3% of games.**
* n = one team, one league, self-reported placement (3rd, APAC). No ablation.

## BUILDER HOOK

**Smallest test: make the existing barrier seal one-bit conditional.** A store slot set by
the raid layer meaning "one of ours needs to cross the perimeter this round"; the
perimeter builder destroys the single barrier on the crossing tile when the bit is set and
rebuilds it when it clears. **One slot, one `destroy`, one `build_barrier`, no new entity
type and no net scale change.**

**Cheaper diagnostic to run first:** over our corpus, how many builder-turns per game do
our own units currently spend routing AROUND our own barriers? **If that number is small,
the gate saves nothing and the whole plank is dead before it is written** — which is the
outcome to hope for at this price.
