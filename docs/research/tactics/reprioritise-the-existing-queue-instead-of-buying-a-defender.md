---
tactic: The champion's anti-rush bought NO new structure — it reordered the production queue it already had, and it named the tempo price in the same sentence
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 Just Woke Up (winners)
evidence: documented
transfers: yes
---

## WHAT IT IS

Arm A of sweep 24 asked for a defensive purchase whose MECHANISM and PRICE are stated
together. **This is the cleanest one in the corpus, and the mechanism is not a purchase
at all — it is a reordering.**

Just Woke Up were knocked out of a tournament by a pure rush on their starting towers
(*"managed to beat us 3-0 by purely rushing down our starting towers, destroying our
money tower and making it so that no matter how many ruins we paint there's no chance we
can build a new tower to get back into the game"*). Their answer for the next tournament:

> *"we added defensive logic when our towers get rushed down by enemy soldiers"*

> *"We did this by making our towers prioritize spawning moppers whenever they sensed
> enemy soldiers in range."*

**No new building. No new unit type. A conditional reordering of the spawn priority a
tower already had.** And the price, in the very next clause — the flattened PDF injects
the page number `14` mid-sentence, so it is quoted in two spans:

> *"Although this could sometimes set us back in terms of building other towers, having
> our starting"* [`14`] *"tower have a chance of not dying was way more important and
> allowed us to successfully defend some rush attacks in the qualifier tournament."*

**Read the price precisely: the cost is not resources, it is EXPANSION FOREGONE.** The
spawn that goes to a defensive unit is a spawn that did not go to the unit that would
have built the next tower. That is a tempo cost denominated in actions, and they name it
as the thing they knowingly accepted.

**They did not measure it.** The justification is a ranking (*"way more important"*) and
an anecdote (*"allowed us to successfully defend some rush attacks"*), never a number —
consistent with [`nobody-in-the-field-has-ever-measured-the-kill-round`](nobody-in-the-field-has-ever-measured-the-kill-round.md).

## WHY IT MIGHT TRANSFER — against our ruleset

**The shape maps almost exactly, and it maps onto the one resource we are actually short
of.** Our constraint is not titanium; it is **builder-turns** — act and move are mutually
exclusive per turn, and the core spawns at most one builder per turn on its own r²=8
ring. Every defensive plank the library has considered so far adds a BUILD (a turret, a
barrier, a seal), which pays twice: once in titanium and once in the +0.20 or +0.01 it
adds to the single global additive scale factor, which inflates every subsequent build of
every type. **A reordering pays neither.**

**Three concrete reorderings exist in our incumbent's decision path, all of them free of
new entities:**

1. **Core spawn placement.** The core already chooses which ring tile to spawn on. Under
   contact, choosing the tile *toward* the threat is a reordering, not a purchase.
2. **Builder action selection.** A builder already ranks build / attack / heal / destroy.
   Promoting `heal` on an adjacent damaged friendly under contact costs 1 Ti and the
   turn, and buys +4 HP — no scale contribution at all (healing is not a build).
3. **`convert_ammo` — and this one is genuinely free of tempo.** It is *"at most once per
   team per turn, usable the same turn, and it does not use the core's action cooldown"*.
   **A defensive ammo top-up is the only defensive spend in our entire ruleset that costs
   zero actions and zero scale.** If a defensive plank must be bought at all, this is the
   cheapest possible currency to buy it in, and the reason is a rule, not a measurement.

**And the trigger they used is one we can compute for free.** *"whenever they sensed
enemy soldiers in range"* is `get_nearby_units(dist_sq)` filtered by `get_team()` — a
live look, no memory, no store slot. Our core's vision is r²=36 and every turret has one.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**This is the class of defensive plank MOST likely to clear the bar, and the reason is
structural rather than empirical.** A reordering consumes a decision that was going to be
made anyway; it cannot add a build, cannot add scale, and therefore cannot inflate the
cost of the raid it is supposed to protect. Its entire cost is the difference in value
between the action taken and the action displaced.

**What would show it slowed the kill, concretely:** median enemy-core-death round rising
between arms, together with a fall in **forward builds per game** — because the only
channel by which a spawn-priority change can slow our kill is by diverting builder-turns
away from forward work. **Both numbers must be reported; the kill round alone cannot
distinguish "the plank is expensive" from "the panel drifted".**

**The honest failure case to pre-register:** in our ruleset the displaced action is often
a *forward* build rather than a *home* build, because our raiders are the units in
contact. Just Woke Up displaced expansion; we would be displacing the attack itself.
**That asymmetry is the reason this file is not a recommendation to ship, and it must be
in the prereg's falsifier.**

## WHAT WOULD KILL IT

* **Their tower is a SPAWNER; our turrets are not.** A BC2025 tower produces units. Our
  gunners and sentinels produce nothing and only the core spawns builders, ≤1/turn. **So
  the literal transfer — "the threatened structure makes a defender" — is available to
  our CORE alone, and to nothing else.** Do not write it as a turret behaviour.
* **A mopper is a counter-unit; our builder is not.** Their reordering produced a unit
  that specifically degrades the attacker. Our builder's attack is 2 Ti for 2 damage on an
  orthogonally adjacent BUILDING — it cannot damage an enemy builder at all. **Our
  reordering can buy HP (heal) or a body (block), never damage.** That is a materially
  weaker version of the same move and the file should not be read as promising theirs.
* **Anecdotal, n unstated, no ablation.** Prioritises; retires nothing.

## BUILDER HOOK

**Smallest test: one branch in the core's existing spawn-tile chooser.** When
`get_nearby_units()` contains an enemy builder inside the core's vision, prefer the
spawn tile nearest that unit; otherwise unchanged. **Zero new entity types, zero scale
delta, one predicate.** Score it on median kill round AND forward builds per game AND
core-death rate, on unrated legs against live teams — never on our own `*_probe` arena,
for the population reason that nearly cost Just Woke Up the title.

**Cheaper still, and worth running first:** measure how often our core spawns a builder
in a round when an enemy unit is already inside its vision. If that number is near zero,
the branch never fires and the plank is untestable before it is written.
