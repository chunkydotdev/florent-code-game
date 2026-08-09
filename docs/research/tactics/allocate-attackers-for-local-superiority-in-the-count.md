---
tactic: ALLOCATE ATTACKERS FOR LOCAL SUPERIORITY IN THE COUNT — assign by "do I outnumber this target's defenders", not by target value or by an even spread
source: https://www.kaggle.com/competitions/lux-ai-season-2/writeups/philipp-kostuch-some-notes-on-a-pure-logic-approac
origin: Lux AI Challenge Season 2 (2023) / Philipp Kostuch, 6th place, pure-logic bot
evidence: documented
transfers: partial
---
⚠ **TIER 2.** Read through a text proxy, **not diffed against Kaggle's original
HTML**. All strings verify verbatim against the local bytes.

WHAT IT IS — A 6th-place pure-logic bot's assignment rule for its attack force,
stated as an explicit ordering of preferences:

> *"allocation of attack robots to factories is done giving preference to achieving superiority in Heavy counts over the defenders"*

The full sentence continues *"and then to balance numbers across factories, moderated
by the distance to the target factories"*, so the ordering is: **local superiority
first, spread second, distance as a modifier.** The preceding clause in the same
bullet list shows the same instinct applied to withholding units — his robots stay
inactive until enough are available, *"this is done to preserve power in the attack
force and not get into their own way"*.

Two things are being claimed. First, the decision variable is a **count of the
heaviest unit class, locally, against that specific target's defenders** — not global
force ratio, not target value, not aggregate advantage. Second, **self-interference
is a first-class cost**: units that cannot contribute are worse than absent, so they
are held back rather than committed.

WHY IT MIGHT TRANSFER — This is a **fifth** independent league converging on the same
shape the library already holds in
[`local-force-count-is-the-engage-gate`](local-force-count-is-the-engage-gate.md), and
it converges on a **count**, not a ratio — which is exactly the distinction sweep 15's
outstanding RTS packet flagged as the thing to check. The convergence therefore
strengthens that file rather than duplicating it.

Both halves have mechanical purchase here.

**Local superiority.** INDEX states the crack in our 2.2:1 defensive edge exactly
once and in these terms: *"our defender's heal is adjacency-capped at ~16 HP/round per
tile while the attacker's damage on that tile is capped only by titanium"* —
**concentration, not more damage.** Philipp's rule is that concentration is a
*scheduling* decision made per target, and that the correct comparison is against
*that target's* servicing detail rather than against the enemy's total force. Ours is
measurable: the field's home builders cluster next to their own turrets at 32.3%
(lift 5.04). The number of bodies servicing a given emplacement is observable at
runtime through vision, so a "do I exceed this tile's repair rate" gate is buildable
without any new information channel.

**Self-interference is a bigger cost for us than for him**, and this is where the
transfer sharpens rather than weakens. His robots got in each other's way
positionally. Ours do so *mechanically*: a gunner's line **stops at the first
targetable tile including our own bodies**, so 17B's blunt formulation applies —
**two gunners in file are one gunner and one 20 Ti barrier.** His "do not get into
their own way" is a soft preference; ours is a hard rule with a price tag.

WHAT WOULD KILL IT — The `partial` is doing real work here.

1. **His units were mobile and reassignable; our damage is immobile.** He could
   compute superiority, discover it was insufficient, and redirect. A sentinel placed
   for local superiority against a target that then gets three more healers is a
   stranded 30 Ti asset that also permanently raised our global cost scale. **The rule
   assumes cheap reallocation, and we have none.**
2. **Superiority must be computed against the RIGHT denominator, and this library has
   already got that wrong once.** The sentinel-file economics were sized against
   **2.68 adjacent builders** believed to be a field figure that was actually **our
   own**; third-party re-derivation gives **2.13 at 3+ attackers, 1.57 at 1**. Anyone
   building a superiority gate must take the denominator from the *observed defenders
   of that specific tile at that moment*, which is what Philipp's rule actually says,
   and not from any pooled average.
3. It is one competitor's stated design, not a measured result. He finished 6th and
   his own writeup title concedes *"not enough on fighting"*.

BUILDER HOOK — The smallest testable form, and it needs no new sensing: before
committing the *next* unit of damage to a target tile, count friendly damage-per-round
bearing on that tile against the number of enemy builder bots orthogonally adjacent to
it (each worth up to 16 HP/round of repair, doubled on a stacked tile). Commit only if
incident damage exceeds it; otherwise hold the purchase. **Gate the purchase, not the
shot** — an already-built turret should always fire.
