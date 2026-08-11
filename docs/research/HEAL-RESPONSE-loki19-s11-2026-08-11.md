# THE HEALING RESPONSE — LOKI-19 §11 REPRODUCED ON A SECOND DECODER, AND ITS CAUSAL LABEL CHANGED

**Research arm, s30, 2026-08-11. Commissioned by the builder arm off the LOKI-19
read-out (`888d699`) §11, with the question stated by them: *is the healing
TRIGGERED by the peck, or is it a level difference that would show up against any
pressure?* Our live version: v104. Population: the 100 LOKI-19 games (50 control
v104 / 50 treatment v108), decoded from `replay_archive/`.**

**ANSWER, in one line: LEVEL, predominantly. They answer DAMAGE with healing, and
they were already doing it to our turrets — the peck-specific excess is 1.41x, not
the effect. And the finding that survives is bigger than the peck and worse for
us: they heal back ~76% of our TURRET core damage too.**

---

## 1. THE INSTRUMENT, AND WHY A SECOND ONE WAS WORTH BUILDING

`scratchpad/hp_ledger.py` measured §11 by summing **positive `UpdateHp` deltas**
on the enemy core. `scratchpad/heal_read.py` walks a **different wire field** —
`Update{builderHeal{id, target}}`, field 15 — which additionally carries **who
healed and in which round**, which is what makes the trigger-vs-level question
answerable at all.

The two paths are joined by an identity the engine gives for free: a heal is
**+4 HP to all friendly entities on the target tile**, so for heals aimed at the
core footprint `4 x (heal events) == (sum of positive HP deltas)`, **except where
a heal is clipped by max HP** — in which case the left side is strictly larger.

**ON REAL DATA: 55 of 100 games satisfy the identity EXACTLY. All 45 discrepancies
run in the licensed direction (`4 x heals - HP delta` has min 0, max 392, never
negative).** That one-sidedness is the check: a decoder reading the wrong field,
the wrong team, or the wrong footprint would produce two-sided noise.

### Selftest: 6 cells, every answer forced by construction

| cell | what it forces |
|---|---|
| A quiet game | no events at all → every counter 0 (catches a decoder that invents) |
| B heal targeting | 7 heals on the footprint, 3 off it → 7 and 10 |
| C team attribution | 5 heals **by our bot at their footprint** → theirs 0, ours 5 |
| D side symmetry | same replay decoded as the other team → the counts mirror |
| E first-peck round | an off-footprint swing at r5 must not set `first_peck=9` |
| F cross-path identity | 4 heals **and** the +4 HP deltas, plus one −18 → separates the two fields |

`HEAL_READ_SELFTEST: PASS` (6/6).

### Mutation test — a suite that has never failed has not been seen to check

| mutation | caught by |
|---|---|
| drop the team check on heals | C and D (their heals become 5, ours 0) |
| count any attack as a peck | E (`our_pecks` 2→3, `first_peck` 9→5) |
| read the HP delta as unsigned | F (`ecore_pos` reads **18446744073709551614**) |

**M3 is `hp_ledger`'s original bug reproduced deliberately** — and it announces
itself the same way, by absurdity rather than by being wrong-but-plausible.

**⚠ HONEST LIMIT OF SYNTHETIC FIXTURES: the selftest encodes field 15 with my own
encoder and decodes it with my own decoder, so it cannot confirm that field 15 IS
`builderHeal`.** The non-circular anchor for that is the identity result above on
real replays — heal-event counts times four match independently-decoded HP deltas
in 55/100 games and never exceed them in the wrong direction.

---

## 2. §11 REPRODUCES — AND ON THE HP FIELD THAT IS A REIMPLEMENTATION CHECK, NOT AN INDEPENDENT ONE

| quantity | builder (`hp_ledger`) | this decoder |
|---|---:|---:|
| damage to their core, rise | +342.7/game | **+342.7** |
| their healing, rise | +370.1/game | **+370.1** |
| net core damage | **−27.4**/game | **−27.3** |
| median healing, control → treatment | 23 → 287 | **23 → 287** |

**Stated plainly because it would be easy to oversell: `ecore_pos`/`ecore_neg` are
the SAME wire field `hp_ledger` used.** Agreement there proves the arithmetic and
the sign handling, not the phenomenon. **The independent corroboration is §1's
identity on field 15.**

---

## 3. THE ANSWER: LEVEL, PREDOMINANTLY

### 3a. The control arm has ZERO pecks by construction — so its healing is a response to turret damage alone

Regressing healing on core damage **across games within each arm**:

| arm | marginal HP healed per HP dealt | pearson r | n |
|---|---:|---:|---:|
| **CONTROL** (turret damage only) | **0.763** | 0.858 | 50 |
| **TREATMENT** (turret + peck) | 0.908 | 0.961 | 50 |
| between-arm marginal (the peck's own coefficient) | 1.080 | — | — |

**Peck-specific excess: 1.080 / 0.763 = 1.41x.** Real, and not the effect. **They
already heal back three quarters of every HP our turrets remove.**

### 3b. The within-game "heals follow pecks" structure is mostly a timing artefact

Heals in the 5 rounds after a peck vs all other rounds: **6.27x**. That looks like
a reflex. **It is not, and the placebo is what shows it:** transplanting each
treatment game's peck schedule onto a control game of the **same cell** — where no
peck exists — reproduces **4.93x**.

**⇒ 79% of the apparent lag effect is *when in a game heals happen*, not the peck.
The peck-attributable excess in the lag structure is 1.27x.**

### 3c. Per-cell discipline: the pooled marginal is only defined in three cells

| cell | ΔDamage | ΔHealing | marginal | control-arm baseline |
|---|---:|---:|---:|---:|
| Askar City | +903.1 | +861.3 | **0.954** | 0.431 |
| Landers | +333.6 | +308.8 | **0.926** | 0.858 |
| Powered by SmartFridge | +167.2 | +164.2 | **0.982** | 0.342 |
| Lunds Stallions | −15.5 | +62.6 | *undefined* | 0.149 |
| farming_200s | −12.0 | +97.9 | *undefined* | 0.474 |

**In the two cells where the peck did not raise core damage, the ratio is a
division by noise and means nothing** — the pooled 1.080 is carried by three
cells. Those three agree at **0.93–0.98**, which is the stronger result: where the
peck lands, they heal back **93–98% of it**.

---

## 4. THE FINDING THAT SURVIVES IS NOT ABOUT THE PECK

**A heal is the cheapest HP in this game, and it beats every damage source we own:**

| action | price | Ti per HP |
|---|---|---:|
| **builder heal** | 1 Ti → +4 HP | **0.250** ← the defender |
| sentinel shot | 10 ammo → 18 dmg | 0.556 (2.2x worse) |
| gunner shot | 4 ammo → 7 dmg | 0.571 (2.3x worse) |
| **builder peck** | 2 Ti → 2 dmg | **1.000 (4.0x worse)** |

*(Ammo is bought from titanium 1:1 by `convert_ammo`, so the units are comparable.)*

**A damage race against a healing defender is unwinnable on titanium at ANY weapon
mix we have.** The peck is merely the worst instrument for a problem the whole
arsenal already has.

**And in builder-rounds the peck's case is arithmetically hopeless:** their builder
standing on the core heals **4 HP per turn** and keeps doing whatever else it
would; ours pecks **2 damage per turn** and **loses its move** (acting and moving
are mutually exclusive). **One healer neutralises two peckers and pays no
positional price.**

---

## 5. ⭐ THE LEVER: HEALING IS THROUGHPUT-CAPPED, AND THEY RUN ALMOST NO HEALERS

A heal is **per builder, per turn**. So their maximum sustainable defence is
`4 HP x (builders adjacent to their core) x round` — a hard ceiling, not a budget.
Measured, per game:

| arm | distinct core-healers | **peak simultaneous** | 90th-pct simultaneous | rounds with a heal |
|---|---:|---:|---:|---:|
| CONTROL | 1.08 | **0.86** | 0.84 | 46.8 |
| TREATMENT | 2.48 | **1.54** | 1.36 | 127.1 |

**Max ever observed in 100 games: 4 simultaneous healers.** Per cell (treatment):
Askar 2.50 peak, Landers 2.10, farming 1.20, Lunds 1.00, SmartFridge 0.90.

**So their realised heal throughput is ~6 HP/round typical and ~16 HP/round at the
ceiling.** Against that: one sentinel is **9 HP/round** (18 dmg, reload 2). **Two
sentinels on the core footprint = 18 HP/round, which exceeds even the 4-healer
ceiling.**

**⇒ The binding quantity is BURST versus their healer count — not cumulative
damage.** Cumulative damage is exactly what a 0.76 heal coefficient eats.

**Two roads this points at, neither of which is the peck:**
1. **Concentrate damage above their heal ceiling** rather than spreading it —
   sustained sub-ceiling damage is converted to titanium for them at 0.25 Ti/HP.
2. **Remove the healers instead of out-damaging them.** Their healer must stand
   **orthogonally adjacent to their own core**. Our launcher picks up an **enemy**
   builder at d² ≤ 2 and throws it 1 ≤ d² ≤ 26, for **0 ammo**, with no team check
   — the approved kidnap class. **A healer displaced off the footprint is 4 HP/round
   of defence removed at zero ammo cost**, and the cap makes each one worth a fixed,
   knowable amount.

---

## 6. WHAT THIS IS NOT

**This prioritises roads. It closes none.** `FIXTURE_OF_RECORD: live_unrated` and
rule 6 (*a refutation without live-game backing is a hypothesis*): everything above
is a decoder cut over 100 already-played unrated games. **No leg has tested burst
concentration or healer removal, and this document must not be cited as though one
had.**

**Specific things NOT established:**
* **No causal attribution on the wire.** The wire carries no "why". §3 separates
  level from trigger by a **placebo and a control arm**, which is inference from
  design, not attribution from the data. **INFERENCE, labelled.**
* **The 0.763 control slope is a cross-game regression**, so it mixes "games where
  we did more damage" with "games where they healed more" — the arms' random
  assignment is what licenses the between-arm comparison, not the within-arm slope.
* **The ~1.5 peak healer count is a property of these five opponents at these
  versions**, and §8 of the prereg already showed one of them is a moving target.
* **The Ti-per-HP table is engine arithmetic, not a measurement** — it is a
  rules-level fact from `CLAUDE.md`, and it is the one thing here that needs no
  live test.

## 7. REPRODUCE IT

```
.venv/bin/python scratchpad/heal_read.py --selftest   # 6 forced cells
.venv/bin/python scratchpad/heal_read.py --leg        # -> scratchpad/heal_leg.json
```
Mutation recipes for the three catches in §1 are `sed` one-liners over
`scratchpad/heal_read.py`; each must turn the selftest to FAIL.
