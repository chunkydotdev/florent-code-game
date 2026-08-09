---
tactic: Range-damage falloff — the one league that quantifies "cheap and close vs expensive and far", and why its answer does NOT transfer
source: https://raw.githubusercontent.com/screeps/engine/master/src/processor/intents/towers/attack.js
origin: Screeps — official engine source, official docs, and the community wiki
evidence: documented
transfers: no
---

## WHAT IT IS

Screeps is the only league in this sweep that puts a **number** on the cheap-close /
expensive-far tradeoff, and it does it inside a single structure type rather than
between two. A Screeps tower's damage decays linearly with range. From the engine
source (`src/processor/intents/towers/attack.js`, lines 32-39, verified verbatim by the
research arm as well as by the sweep leg):

```js
var range = Math.max(Math.abs(target.x - object.x), Math.abs(target.y - object.y));
var amount = C.TOWER_POWER_ATTACK;
if(range > C.TOWER_OPTIMAL_RANGE) {
    if(range > C.TOWER_FALLOFF_RANGE) {
        range = C.TOWER_FALLOFF_RANGE;
    }
    amount -= amount * C.TOWER_FALLOFF * (range - C.TOWER_OPTIMAL_RANGE) / (C.TOWER_FALLOFF_RANGE - C.TOWER_OPTIMAL_RANGE);
}
```

with the constants (`screeps/common/lib/constants.js`, lines 248-254, re-verified):

```
TOWER_ENERGY_COST: 10,
TOWER_POWER_ATTACK: 600,
TOWER_OPTIMAL_RANGE: 5,
TOWER_FALLOFF_RANGE: 20,
TOWER_FALLOFF: 0.75,
```

**Subjects attached, because a number carries a subject:** `600` is the *attack damage in
hit points* of one Screeps tower at Chebyshev range ≤ 5; `150` is that same tower's
damage at range ≥ 20. `10` is the *energy consumed per action*, and it does not vary with
range. So **the same structure, at the same price per shot, does 4× the damage close in
as far out**, on a flat −30 damage per tile between range 5 and range 20.

The official doctrine follows directly and is stated as an imperative
(`docs.screeps.com/defense.html`, re-verified):

> *"Always place towers as close to their potential targets as possible."*

## WHY IT MIGHT TRANSFER — and it is the negative that matters

**It does not transfer, and establishing that is the point of this file.** Our engine has
**no damage falloff at all.** A gunner deals 7 at range 1 and 7 at range 3; a sentinel
deals 18 at range 1 and 18 at range 5 (`docs/reference/official-docs.md:235-259`). Range
here is a **reach** parameter, never a **damage** parameter.

**Consequence, and it is decision-relevant:** every intuition of the form **the
long-range emplacement must be the stronger one** — this sweep's own wording, not a
quotation — imported from a falloff game is wrong here.
The sentinel's r²=32 buys exactly two things — **the ability to stand further back than a
builder bot can reach in one step, and the ability to touch a tile a gunner cannot
reach.** It buys **zero** extra damage. Anyone reasoning "expensive-far must hit harder"
is reasoning from Screeps or from tower-defence games, not from our rules.

**The mirror-image consequence is the one worth acting on.** If range buys no damage,
then the entire case for the sentinel over the gunner rests on *reach, obstacle-piercing
and toughness*, and the entire case for the gunner rests on *price, rotation and
front-rank placement* — see
[`the-turret-mix-is-not-a-cost-decision`](the-turret-mix-is-not-a-cost-decision.md) for
the arithmetic showing the two are within ~10% of each other on every titanium metric.

## WHAT WOULD KILL IT

Nothing kills the negative — it is a rules fact, checkable in one line of our own
reference doc. What *would* narrow it: if a future patch introduced falloff, or if
effective damage-per-round varies with range for a reason other than the damage number
(it does, indirectly: a turret further from the enemy is fired at less and healed more,
which is a *survival* effect and not a *damage* effect, and this library has already been
burned once by scoring turrets on survival — see
[`2026-08-09-sweep-8.md`](2026-08-09-sweep-8.md)).

## BUILDER HOOK

None in code. This is a **de-biasing note**: strike "longer range means stronger" from any
turret-choice heuristic, and require that any siting score which uses distance say
explicitly whether it is pricing *reach*, *survival*, or *forwardness* — three different
quantities that a single distance term silently pools.
