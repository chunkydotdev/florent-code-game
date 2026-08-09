---
tactic: The canonical case for massing the cheap emplacement rests on three named advantages — and ALL THREE fail in our ruleset
source: https://web.archive.org/web/20241219090640/https://ageofempires.fandom.com/wiki/Tower
origin: Age of Empires series wiki (Tower); Factorio wiki (Gun turret / Laser turret) on the upkeep axis
evidence: documented
transfers: no
---

## WHAT IT IS

Asked why anyone builds many cheap towers instead of one strong structure, the largest
tower-defence-adjacent canon states the case in one place and enumerates it:

> *"towers have several key advantages that can make them useful. First, they are often
> available earlier than more powerful defensive structures. They can be much cheaper; for
> example, in Age of Empires II, the [Watch Tower…]"*

and the area argument, whose referent — *"one more powerful defensive structure"* — is
established in the preceding sentence as the Castle/Fort/Keep:

> *"that players can build several towers over a wider area for the cost of one more
> powerful defensive structure, thus defending a larger area from enemy attackers."*

**Three advantages, in the source's own order: EARLIER, CHEAPER, WIDER AREA. Damage is not
on the list, and neither is concentration.**

**Factorio adds the fourth axis that actually distinguishes its two turret tiers, and it
is upkeep type rather than range or damage.** Gun turret:

> *"Unlike laser turrets, they do not require power and can operate practically anywhere as
> long as they have sufficient ammunition. On the downside, this means that ammo must be
> periodically replenished."*

Laser turret:

> *"Laser turrets are an advanced defense building with longer range than the gun turret,
> laser damage, and use electricity to operate instead of ammo"*

## WHY IT DOES NOT TRANSFER — and this is the finding

**Run our two turrets against the three canonical advantages and every one of them
evaporates.**

| canonical advantage | our gunner vs sentinel |
|---|---|
| **Available earlier** | **FALSE.** Both are buildable by any builder bot from the first turn it is adjacent to a legal tile; there is no tech gate, no prerequisite structure, no research. The only gate is 20 Ti vs 30 Ti against a 500 Ti opening bank. |
| **Much cheaper** | **FALSE at the scale that matters.** 20 vs 30 base, and for *equal firepower* 324 vs 336 Ti at scale 1.0 — a 3.6% gap, with the gunner leaving the team scale 0.4 higher. See [`the-turret-mix-is-not-a-cost-decision`](the-turret-mix-is-not-a-cost-decision.md). |
| **Wider area for the same money** | **FALSE — neither turret covers an area.** Both fire a single-tile-wide ray in one fixed direction. Cardinally the gunner's ray is 3 tiles and the sentinel's 5; per titanium that is **0.150 vs 0.167 tiles/Ti**, i.e. the *expensive* one covers marginally more, not less. |
| *(Factorio's fourth axis: upkeep type)* | **N/A.** Both of ours draw from the same global ammunition pool at 0.5714 and 0.5556 Ti per point of damage — a 2.9% gap. There is no power/ammo distinction to exploit. |

**⇒ The entire published case for "mass the cheap one" is an argument about EARLINESS, PRICE
and AREA COVERAGE, and our ruleset supplies none of those three differences.** Whatever
explains the top tier's gunner-heavy core kills, it is not the reason the wider gaming
canon gives for massing cheap emplacements.

**This is the third independent route to the same conclusion in this sweep** — the
arithmetic route (`the-turret-mix-is-not-a-cost-decision`), the falloff route
(`range-buys-damage-elsewhere-and-buys-nothing-here`), and now the doctrine route. All
three say the same thing: **our two turrets are a sidegrade, not a tier, and the mix
question is geometric.**

## WHAT WOULD KILL IT

- **Area coverage is the one row that could be wrong in a way that matters**, because a
  gunner can *rotate* for 10 Ti and a sentinel cannot rotate at all. Over a long life a
  gunner's *effective* covered set is larger than its instantaneous ray. Nobody has priced
  that, and it is the strongest surviving mechanical argument for gunners in this sweep.
- The AoE wiki is a community wiki for a series spanning decades; it is `documented` as a
  statement of that canon's doctrine and carries no competitive evidence.
- The comparison table above uses our base costs and the measured scale model. If the
  scale model is wrong the second row moves; the first and third rows are pure rules facts
  and do not.

## BUILDER HOOK

**Price the rotation, because it is the last surviving asymmetry.** `rotate()` costs 10 Ti
and one cooldown round and is gunner-only. The question that would settle it: over the
life of our gunners, **how often would a re-aim have converted a blocked or empty ray into
a live target?** If the answer is "often", the gunner is a re-aimable asset worth its
premium in ammunition granularity and the top tier's mix has a mechanism after all. If it
is "never" — and we currently never rotate at all — then we have been buying a cheaper
turret and throwing away the only thing that makes it different.
