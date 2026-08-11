---
tactic: The field treats "rounds spent producing nothing" as a TARGETING defect and fixes it by broadcasting a destination — never by shortening the deployment
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 The Kragle; Battlecode 2025 confused
evidence: documented
transfers: yes
---

## WHAT IT IS — arm (C), and it reframes our own metric

The Kragle devote a named section (*"Reducing Idle-Time"*) to exactly the
quantity our 54.55-rounds-per-forward-build number measures, and they state the
problem in allocation terms rather than survival terms:

> *"a robot-count lead means nothing if half of your robots are derping around."*

**Referent check.** The preceding sentences read *"Often, we'd find ourselves with
not just a resource lead, but a robot count lead. On paper, the team with more
robots is always at an advantage. However,"* — so "derping around" is their term
for units alive, deployed, and producing nothing. The figure caption in the same
section reads *"A gaggle of soldiers and splashers in the upper right derping
around far away from where they could be useful..."*

**Their fix is a shared destination, not a shorter deployment:**

> *"The bots having even a vague idea about where the battlefront was reduced their idle explore time massively."*

The preceding sentence names the channel: *"The easiest idea our team had for
reducing idle time was communicating battlefronts."* **The unit is not recalled.
It is told where to go.** confused, the same season, reached the same answer from
the other direction (*"redirecting long-inactive units to the opposite side of the
map center"*) — filed at
[`the-only-clock-the-field-runs-forward-is-an-idleness-timer`](the-only-clock-the-field-runs-forward-is-an-idleness-timer.md).

## WHY IT MIGHT TRANSFER — and it is the reframing the builder should take from this sweep

**"Rounds in enemy territory per structure placed" is an idle-time metric wearing
a dwell-time costume.** It rises for two structurally different reasons:

1. the unit stays too long after finishing — a **withdrawal** defect;
2. the unit is present but has no legal, valuable adjacent action — a
   **targeting** defect.

The whole field treats (2) as the live one, and (2) is the only one with a fix
that survives `PLAY_DEFENCE: never`. **This is a testable discrimination and it
requires no bot change:** a forward round in which `can_build_*` was true on some
adjacent tile and we did not build is a targeting failure; a forward round in
which no adjacent tile was legal is a positioning failure; a forward round after
the errand completed is a withdrawal failure. **Three different planks, and the
2.28x number does not say which.**

Our channel for The Kragle's fix already exists and is cheap for this shape: the
16-int store carries **one small non-negative integer** safely — the case this
library has repeatedly established
([`route-completeness-as-a-live-scalar`](route-completeness-as-a-live-scalar.md),
[`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)).
A packed forward-target position is exactly that, and the incumbent already packs
positions into slots (`SLOT_ENEMY_CORE`, `SLOT_THREAT`).

## WHAT WOULD KILL IT

* **The one-round write buffer.** A battlefront broadcast is a round stale by
  construction. For an immobile target (every building we can attack) that is
  harmless — the library's decay finding says memory of immobile targets needs no
  age term
  ([`retract-the-target-only-on-a-look-not-on-a-clock`](retract-the-target-only-on-a-look-not-on-a-clock.md)).
* The Kragle report this as *"massive"* improvement with **no number**, and they
  finished mid-field. `evidence: documented`, effect size unstated.
* If our raiders already share a target (they do, via the enemy-core slot), the
  cheap version of this is **already shipped** and the plank must be the finer
  one: a per-raider *seat*, not a team-wide front.

## BUILDER HOOK

Before building anything: split the forward-round population three ways
(legal-action-available-and-unused / no-legal-action / errand-already-complete).
**That single cut tells you which of three planks the 2.28x is, and it is a
corpus cut with zero bot risk.**
