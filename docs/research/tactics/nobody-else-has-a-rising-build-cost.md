---
tactic: NEGATIVE — no league in this sweep prices the Nth structure higher than the first; they all use COUNT CAPS or flat costs instead
source: https://raw.githubusercontent.com/screeps/common/master/lib/constants.js and https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/game-configs.json
origin: Screeps (engine constants), Terminal (shipped config + decompiled engine), Battlecode 2019-2026 (22 official postmortems)
evidence: documented
transfers: no
---

## WHAT IT IS

Question (C), as the sweep brief put it, was *"did any league have superlinear structure costs, and what
did that do to doctrine?"* — on the reasonable assumption that Battlecode, Screeps or
Terminal would have a candidate mechanic. **They do not. The answer is a clean negative
across all three, and it changes what the rest of this library's cross-league evidence is
worth on this question.**

**Screeps — a per-level COUNT CAP, and a flat price.** From `screeps/common/lib/constants.js`
(re-verified from raw bytes):

```
CONSTRUCTION_COST: { ... "tower": 5000, "constructedWall": 1, "rampart": 1, ... }
CONTROLLER_STRUCTURES: { "tower": {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 6}, ... }
```

**Subject: `5000` is the energy construction cost of one tower, and it does not change;
the `{1: 0 … 8: 6}` map is the maximum number of towers allowed simultaneously at each
Room Controller Level 1-8.** The sixth tower costs the same 5,000 as the first — you
simply cannot build a seventh. A grep of the whole constants file for `scale` /
`multiplier` returns **zero**.

*(Where a rising curve does live in Screeps is rampart **hit points** —
`RAMPART_HITS_MAX: {2: 300000 … 8: 300000000}` — i.e. the many-cheap-vs-few-strong axis is
expressed as HP invested per barrier tile, not as a build-cost curve.)*

**Terminal — flat, full stop.** The shipped `game-configs.json` prices the wall at
`"cost1": 1.0` and the turret at `"cost1": 2.0` with no count term; the sweep leg grepped
the decompiled engine for every scaling idiom and got nothing, and the research arm
re-ran `grep -ci "costscal\|scalecost\|costmultiplier"` on the raw config → **0**.

**Battlecode — rising costs appear as a per-turn SPEND cap or as tiered upgrade prices,
never as a per-count price.** BC2022 capped spend (*"the most lead you could spend per
turn was 300, one soldier per Archon"*); BC2025 priced tower **levels** superlinearly
(1000 / 2500 / 5000) but each *new* tower at a fixed price. Neither is our mechanic.

## WHY IT MATTERS — against our ruleset

**Our mechanic is genuinely unusual, and the library should stop expecting to find
doctrine for it.** `docs/game-model.md:393-402` (marked measured): a single team-wide
`scale`, additive, `+1%` per conveyor/splitter/barrier, `+5%` per harvester, `+10%` per
launcher, `+20%` per builder bot / gunner / sentinel, multiplying **every** subsequent
build cost, and refunded when the entity dies.

Three consequences that no surveyed league has an analogue for:

1. **Cross-category contamination.** Building a builder bot makes our *conveyors* dearer.
   In every league surveyed, structure prices are independent of unit production.
2. **The tax is on COUNT, not on titanium.** A 3 Ti barrier costs +1% and a 30 Ti sentinel
   costs +20% — so scale per titanium spent is **0.0033** for a barrier against **0.0067**
   for a sentinel and **0.0100** for a gunner. **Cheap-and-numerous is only cheap if the
   cheap thing is also low-scale**, which for us is true of barriers and false of gunners.
3. **Destruction refunds it — including the enemy destroying it.** Sweep 6 already found
   the inverted consequence for attacking their builders; the same rule means our own
   turret losses partially self-heal our economy, which is a term no league's static
   defence doctrine contains.

## WHAT WOULD KILL IT

- **Coverage, stated honestly:** this negative covers Screeps, Terminal and the 22
  Battlecode postmortems on my disk. **Halite, Lux AI, CodinGame and the Kaggle games were
  not checked by me for this specific mechanic**; a parallel leg was tasked with them and
  its result must be read alongside this file before the negative is called complete.
- The Screeps and Terminal claims are `documented` from engine constants and shipped
  config. The Battlecode claim is weaker: it rests on 22 postmortems not *mentioning* a
  per-count cost, which is absence-of-evidence in prose, not a rules check.

## BUILDER HOOK

None. This is a **scope note on the library**: on the cost-scaling question specifically,
we have no external doctrine to borrow and the arena is the only instrument — the same
bound sweep 15 established for cause-versus-marker. Any cost-scaling rule we adopt is
ours, and must be derived from our own numbers rather than imported.
