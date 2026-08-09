---
tactic: The mechanism behind "many cheap beats few expensive" is TARGET-ACQUISITION RATE — the published theory says explicitly that it is not about range
source: https://cdn.aaai.org/ojs/12780/12780-52-16297-1-2-20201228.pdf
origin: Stanescu, Barriga & Buro, "Using Lanchester Attrition Laws for Combat Prediction in StarCraft", AIIDE-15
evidence: documented
transfers: yes
---

## WHAT IT IS

Question (B) of this sweep asked which variable decides a cheap-many / expensive-few mix.
The clearest answer in the literature is a sentence that most people quoting Lanchester
skip, and it rules out the intuitive candidate by name:

> *"The squared law is also known as Lanchester's Law of Modern Warfare and is intended to
> apply to ranged combat, as it quantifies the value of the relative advantage of having a
> larger army. However, the squared law has nothing to do with range – what is really
> important is the rate of acquiring new targets. Having ranged weapons generally lets
> your soldiers engage targets as fast as they can shoot, but with a sword or a pike to
> which the Linear Law applies one would have to first locate a target and then move to
> engage it."*

**The N² payoff for going numerous is conditional on every unit being able to acquire and
fire at a target every tick.** Range is only a proxy for that condition. Anything that
stops some of your units firing — facing, an obstructed line, an empty ammunition
balance, a queue for one target — knocks you back toward the **linear** law, where
doubling the count doubles your value instead of quadrupling it.

The same paper supplies the default per-unit value it uses before any learning:

> *"We start with a default value αi = dmg(i)HP(i) , where dmg(i) is the unit's damage per
> frame value and HP(i) its maximum number of hit points."*

*(This library already files the α = dmg × HP predicate as an attack/retreat gate in
[`lanchester-commit-gate`](lanchester-commit-gate.md). This file is a different claim from
the same paper and does not restate that one.)*

## WHY IT MIGHT TRANSFER — and it reframes the whole sweep

**Our turrets are precisely the case the passage warns about.** Both fire a single-tile
ray in a fixed facing; a gunner's ray *"stops at the first targetable tile"* including our
own bots and buildings; a gunner can rotate only for 10 Ti and a cooldown; a sentinel
cannot rotate at all. **So our acquisition rate is structurally low and structurally
variable**, which means the square-law bonus for massing turrets is one we may simply not
be collecting.

Run α = dmg × HP on our own two turrets, with the caveat that the paper's α is per *unit*
and ours are structures:

| | dmg/round | max HP | **α = dmg × HP** | α per titanium (base) |
|---|---|---|---|---|
| Gunner | 7 | 25 | **175** | 8.75 |
| Sentinel | 9 | 40 | **360** | **12.0** |

**On the field's own default value function, our sentinel is worth 2.06× a gunner and
1.37× a gunner per titanium.** That is the *opposite* of the direction the top tier's kill
mix points, and it is the sharpest single reason to distrust a naive "build more gunners"
reading. It also flags what would make the gunner right anyway: **α assumes the unit
fires.** A sentinel that never gets a target, or a gunner that always does, breaks the
comparison — which is exactly the acquisition-rate term the paper says is the real
variable.

**Practical form of the transfer, in my own words:** the question to ask of a turret is not
how far it reaches but **what fraction of rounds it will actually fire.** Ammunition is a term
in that fraction and we under-buy it badly; facing is a term and we set it once; line
obstruction is a term and it applies to gunners only.

## WHAT WOULD KILL IT

- **α = dmg × HP is stated as a starting point that the paper then LEARNS away from.** It
  is a prior, not a result, and the authors say so. Do not present the 175/360 table as a
  measured valuation — it is the field's default formula applied to our numbers by this
  sweep.
- **Lanchester assumes an open field and mutual fire.** A 500 HP core that deals no damage
  is not an army, and the defender-behind-a-choke case is not modelled — the same caveat
  `lanchester-commit-gate` already carries.
- **Our structures do not choose targets**; the ray hits the first thing on it. So
  "acquisition rate" for us is decided entirely at *build time* by placement and facing,
  which makes it a siting problem rather than a micro problem.

## BUILDER HOOK

**Instrument the firing fraction, because it is the term the theory says decides
everything and we do not have it.** Per turret, per game: rounds alive, rounds with a
legal target on the ray, rounds actually fired, and rounds blocked by ammunition. Sweep 7
established that the corpus can only give shots-per-turret-built; the per-turret series is
what would let us test whether our sentinels' 2× α advantage is being collected or thrown
away. If our turrets fire in a small minority of the rounds they are alive, **the mix is
not the problem and no ratio change will fix it.**
