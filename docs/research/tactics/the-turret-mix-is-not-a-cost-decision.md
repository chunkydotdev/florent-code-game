---
tactic: The gunner/sentinel mix is not a cost decision — the arithmetic, re-derived, puts them within ~10% on every titanium metric
source: docs/reference/official-docs.md:235-259 and docs/game-model.md:393-407 (both marked measured against the live engine)
origin: research arm, sweep 17b, 2026-08-09 — own derivation from our own measured rules, not a foreign league's doctrine
evidence: inference
transfers: yes
---

## WHAT IT IS

The sweep brief that produced this file supplied the arithmetic as *"a gunner's shot
costs 4 Ti of ammo for 7 dmg (1.75 Ti/dmg) and a sentinel's costs 10 Ti for 18 dmg (0.556
Ti/dmg)"* and characterised the gunner as *"higher-DPS-per-round"*. **Re-derived, two of
those three statements are wrong, and the correction changes the conclusion.**

### 1. Ammunition price of damage — the two turrets are within 3% of each other

Ammunition is bought from titanium 1:1 at the core, and there is no other source.

| | ammo/shot | damage/shot | **Ti per damage** | damage per Ti of ammo |
|---|---|---|---|---|
| Gunner | 4 | 7 | 4/7 = **0.5714** | 1.750 |
| Sentinel | 10 | 18 | 10/18 = **0.5556** | 1.800 |

`1.75` is **damage per titanium**, not titanium per damage; the brief's two figures were
quoted in opposite units and are not comparable as written. The correct comparison is the
bolded column: **the sentinel is 2.9% cheaper per point of damage delivered.** That is
the whole ammo-efficiency gap, and it is nearly nothing.

### 2. Damage per round — the SENTINEL is higher, not the gunner

`docs/reference/official-docs.md:257`: *"18 every 2 rounds against 7 every round"* —
sentinel **9/round**, gunner **7/round**. The gunner is the *lower*-DPS turret. (This
same figure has been mis-stated in our own docs before: sweep 10 found `docs/v79-analysis.md`
carrying a gunner rate that was 2× low, and corrected it in place.)

### 3. Build cost per unit of standing damage — the gunner wins, by 14%

At scale `s`, gunner `20s`, sentinel `30s`.

- Gunner: `20s / 7` = **2.857 s** titanium per point of damage/round
- Sentinel: `30s / 9` = **3.333 s** titanium per point of damage/round

### 4. Total titanium to deliver D damage from one turret, and the break-even

- `G(D) = 20s + 0.5714 D`
- `S(D) = 30s + 0.5556 D`
- `S(D) < G(D)` ⟺ `10s < 0.01587 D` ⟺ **D > 630·s damage**

**At s = 1.0 a sentinel repays its build premium only after 630 damage from that one
turret; at a mid-game s = 2.0, after 1,260.** For scale, the measured cost of killing a
≥1700-rated team's core is **1,019 damage** and of killing ours **1,596** (both figures
are *damage dealt to the core*, from the corpus cut the brief cites — the 1,019 is
theirs, the 1,596 ours). **One sentinel does not repay its extra 10 Ti inside a whole
core's worth of damage at typical scale.**

### 5. The cost scale is ONE GLOBAL NUMBER, and it taxes count, not type

`docs/game-model.md:393-402` (marked **measured**): `effective_cost = floor(scale ×
base_cost)`, one team-wide `scale` that rises **additively** — conveyor/splitter/barrier
+1%, harvester +5%, launcher +10%, **builder bot / gunner / sentinel +20% each** — and
falls again on destruction. The project CLAUDE.md's phrasing *"rises as you build more of
**that category**"* is not what the measured model says; there is a single
`get_scale_percent()`.

Two consequences, and neither is what "self-taxing" intuition suggests:

- **The +20% is identical for a gunner and a sentinel.** Cost scaling therefore cannot
  discriminate between them at all. It discriminates against **turret count**, and
  against **builder bots**, which pay the same +20% as a turret.
- Because the increment is flat per entity while the base costs differ, the scale tax
  *per titanium spent* is **0.0100 scale/Ti for a gunner and 0.00667 for a sentinel** —
  massing the cheap unit costs 50% more scale per titanium of turret. Per unit of
  damage/round it is 0.0286 vs 0.0222, a **28.6% penalty on the gunner**.

**Worked example — equal firepower, 63 damage/round, starting from scale s₀:**

| | count | build cost | scale left behind |
|---|---|---|---|
| Gunners | 9 | `180·s₀ + 144` (324 Ti at s₀=1, 504 at s₀=2) | +1.80 |
| Sentinels | 7 | `210·s₀ + 126` (336 Ti at s₀=1, 546 at s₀=2) | +1.40 |

Gunners are cheaper to buy at every realistic scale (they cross at s₀ = 0.6, below the
1.0 floor) and get *relatively* cheaper as `s` rises — but they leave the whole team's
future build costs **0.4 scale** higher, which on our own measured build mix (we build 59
conveyors a game) is real money.

## WHY IT MATTERS — the conclusion

**On build cost, ammo cost, HP per titanium and cost-scale externality, a gunner and a
sentinel are within roughly 10% of each other, and the two biggest gaps point in
opposite directions.** There is no titanium argument for either mix. So:

> **If the top tier's gunner-heavy core-kill mix (53.1% gunner / 44.4% sentinel against
> our 22.7 / 69.2) is a real mechanism rather than a marker, the mechanism is NOT
> economic. It has to be geometric — reach, firing line, rotation, or where the turret
> can be planted.**

That is a strictly narrower search space than "should we build more gunners", and it is
the single most useful thing this sweep produced. The geometric candidates are
enumerated in
[`a-gunner-kill-is-a-clear-line-not-a-doctrine`](a-gunner-kill-is-a-clear-line-not-a-doctrine.md).

## WHAT WOULD KILL IT

- **The scale model.** Everything in §5 rests on `docs/game-model.md` being right that
  there is one global additive scale. It is marked measured, but this sweep did **not**
  re-probe it. If the scale is per-category after all, §5's conclusion survives anyway
  (gunner and sentinel would then be in the *same* category — the doc groups them — and
  the tax would still not discriminate), but the "massing gunners doubles the price of
  our economy" clause dies.
- **Rebuild churn.** The break-even in §4 assumes one turret delivering D damage. A
  turret that dies and is rebuilt pays the build cost again, which favours the *cheaper*
  build — pushing further toward the gunner, not away.
- **Ammo lumpiness.** At a low ammo balance a 4-cost shot is available when a 10-cost
  shot is not. Our own measurement is that we under-buy ammunition badly (we hold more
  titanium than Ouroboros at r200-300 while buying a twelfth as much ammo), so this
  granularity effect is probably live for us and is not priced above.

## BUILDER HOOK

Two cheap ones, in cost order:

1. **Free — stop treating turret choice as a budget question in any comment, doc or
   heuristic.** Any rule of the form "we can't afford sentinels" or "gunners are the cheap
   option" is contradicted by the table above.
2. **Cheap — instrument the geometry instead.** At every turret build, log the
   straight-line distance to the enemy core and whether the firing line to it is clear.
   If our gunners are being planted where the line is blocked, the mix question answers
   itself without a single A/B game.
