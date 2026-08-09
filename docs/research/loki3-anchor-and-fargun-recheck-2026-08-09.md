# LOKI-3 forward anchor: the ASK answered, and a re-check of the instrument that closed the forward road

**Research arm, session 23, 2026-08-09 09:09 CEST (from `date`).**
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"**, rating **1589**,
**501 matches, rank #29 of 113** (`fcode status`, 09:0x). Code read:
`bots/_v107loki3/main.py` md5 `321c635b`, `bots/_v107loki3/doctrine.py` md5
`ce8ddd5e`. Corpus: `corpus/` at commit `a1bd423`, synced 08:5x (archive 4,071
replays, 4,031 decoded, join 1,230 rows, reconciliation 100.0000%).

Commissioned by the builder as an explicit ASK: *re-derive the 116-146 vs 56-82
forward-distance band independently, and give the DISPERSION, not just the
median.*

**Everything below is free-metadata + already-archived replays. Zero downloads.**

---

## 0. TL;DR

| # | claim | status |
|---|---|---|
| 1 | The `116-146 vs 56-82` anchor justification is a metric mismatch | **CONFIRMED** — independently, before I saw the builder's 307d550 |
| 2 | Field forward-only sits at d² **170-200**, ours at **66-81** | **CONFIRMED**, reproduces the builder's replacement numbers |
| 3 | The pooled d² gap is **partly a map-mix artifact** | **NEW** — map-matched, the gap is far smaller |
| 4 | `LATE_FORWARD_NUM/DEN = 2/5` would have **disabled the arm on 11/15 maps**, not relocated it | **NEW — the specified test was a false-negative trap** |
| 5 | The field places at along-axis fraction **t ≈ 0.82**; our constant is **0.60** | **NEW** — the knob is already at the field's p10 |
| 6 | FARGUN-COVERAGE's `d2_own > 110` cut is **map-heterogeneous**; normalised, the gap **halves** and *"our best stratum < their worst"* **does not survive** | **NEW — amends magnitude, not direction** |

**I am not asking for the forward-road verdict to be reopened.** It rests on
three instruments and I only touch one. But claim 6 means that instrument is
weaker than the note states, and the sentence the builder called *"the line that
settles it"* is an artifact of the cut. That belongs in the tape before a
successor quotes it.

---

## 1. Method, pinned to the code rather than to a memory of it

`_late_band_ok` (`main.py:2547-2557`) defines the population exactly:

```python
do = bp.distance_squared(self.core)
...
return bp.distance_squared(self.enemy) <= do      # FORWARD  <=>  d2_enemy <= d2_own
```

which is **identical to the `side` column in `corpus/builds.tsv`**. Distances are
to the Core *anchor*, which is what `d2_own` already is. So the corpus and the
gate speak the same units — no translation, no assumption.

**Validation before extension.** I reproduced the published census table
(`late-game-doctrine-2026-08-09.md` §3) from the corpus first. If that had not
reproduced, nothing downstream would be worth reading:

| band | who | published n / med | **mine** n / med |
|---|---|---|---|
| r0-150 | THEM | 3,449 / 25 | 6,056 / 29 |
| r0-150 | US | 1,711 / 25 | 3,636 / 25 |
| r150-200 | THEM | 841 / 61 | 1,257 / 65 |
| r150-200 | US | 257 / 18 | 491 / 20 |
| r200-300 | THEM | 1,346 / 56 | 1,885 / 58 |
| r200-300 | US | 267 / 20 | 515 / 20 |
| r300+ | THEM | 2,894 / 82 | 3,936 / 74 |
| r300+ | US | 380 / 22 | 830 / 20 |

Medians land within 8; n roughly doubles because the corpus has grown
(join 1,165 → 1,230 files) and the keeper keeps decoding. **Pipeline validated.**

---

## 2. The metric mismatch — confirmed, and here is exactly where it came from

- **`56-82`** is the **`median d² to OWN core`** column of that census, which
  pools **FORWARD *and* HOME** turret builds. Home turrets sit at median d²
  **13-20**. Roughly half the field's late turrets are home turrets, so they drag
  the pooled median down to 56-82.
- **`116-146`** is the LOKI-3 arena flag matrix's **`med d2_own`**, which is
  **FORWARD-only**.

So the anchor was justified by comparing **our forward-only** statistic against
**the field's forward-and-home-pooled** statistic. The builder reached this
independently in commit `307d550`; I reached it from the corpus before reading
that commit. **Two independent derivations, same conclusion.**

Like-for-like, FORWARD-only, d² to own core:

| band | US n | US med | IQR | THEM n | THEM med | IQR |
|---|---|---|---|---|---|---|
| r150-200 | 170 | **81** | 253 | 711 | **193** | 232 |
| r200-300 | 179 | **80** | 200 | 1,026 | **170** | 212 |
| r300+ | 178 | **66** | 216 | 2,079 | **200** | 202 |
| **r150+ pooled** | **527** | **80** | **229** | **3,816** | **193** | **216** |

**The direction is the opposite of the one that motivated the change.** The
field's forward guns sit *further* from their own core than ours, and further
than LOKI-3's arena 116. Lowering 3/5 → 2/5 moves away from the field, not onto it.

### The dispersion the ASK asked for — and it is enormous

`IQR ≈ 216`, p10 = 45, p90 = 410 for the field's late forward builds. **An order
of magnitude, so no single d² constant can land this distribution.** But that is
the wrong parameterisation to judge the knob by, because the knob is not a
distance — see §4.

---

## 3. NEW: the pooled comparison is partly a map-mix artifact

Core separation `d²_cores` is **exactly constant per map** (verified: each map
yields exactly one value across all games), ranging **32 (fjordgate) → 650
(hive)** — a **20× spread**. And our late forward builds are not drawn from the
same maps as the field's:

| map | d²cores | US % of our fwd builds | THEM % of theirs | skew |
|---|---|---|---|---|
| meander | 49 | 15.0% | 6.6% | **+8.4** |
| moonrise | 81 | 8.9% | 3.2% | **+5.7** |
| antler | 64 | 8.3% | 4.1% | +4.2 |
| heart | 144 | 8.7% | 4.7% | +4.0 |
| … | | | | |
| archipelago | 392 | 4.0% | 8.6% | −4.6 |
| hive | 650 | 2.8% | 7.6% | −4.7 |
| snowflake | 392 | 3.2% | 9.7% | **−6.5** |

**We build our late forward guns on small maps; the field builds theirs on big
ones.** Pooling across maps then compares different games.

Map-matched (median of per-map median placement fraction, 12 maps with n≥20 both
sides): **US 0.750 vs THEM 0.827, delta −0.077**, and **we are further forward
than the field on 4 of 12 maps**. The 2.5× pooled d² gap is largely composition.

---

## 4. NEW, and the sharpest result: `2/5` would have turned the arm OFF

The knob is **not a distance**. `_late_anchor` (`main.py:2500-2501`) computes

```python
ax = core.x + (enemy.x - core.x) * num // den
```

i.e. it places the anchor at **fraction t = num/den along the core axis**. So
`d2_own ≈ (num/den)² · d²_cores` — a *fraction*, which is why it produces a
20×-varying d². **That parameterisation is correct** and the field's behaviour
confirms it (§5): the field is fraction-like, not distance-like.

But `_late_band_ok` **gates on FORWARD, i.e. `t ≥ 0.5`**, while the anchor knob
can be set below 0.5. **The two are parameterised inconsistently.** At
`num/den = 2/5`, t = 0.40 — on our *own* side of the midline. Every candidate
tile there fails `d2_enemy <= d2_own`, and `_late_turret_build:2605` applies that
gate per candidate with **no fallback**:

```python
if not self._late_band_ok(bp):
    continue
```

The along-axis gap from a t=0.40 anchor to the midline is `(0.5 − 0.40)·D` tiles,
against a builder's **1-tile** build reach:

| map | d²cores | gap to midline at 2/5 | arm at 2/5 |
|---|---|---|---|
| fjordgate | 32 | 0.57 tiles | partial |
| meander | 49 | 0.70 | partial |
| antler | 64 | 0.80 | partial |
| moonrise | 81 | 0.90 | partial |
| lighthouse | 128 | 1.13 | **DISABLED** |
| nordkap/eider/heart | 144 | 1.20 | **DISABLED** |
| atoll | 288 | 1.70 | **DISABLED** |
| drumlin | 338 | 1.84 | **DISABLED** |
| saga/snowflake/jackpot/archipelago | 392 | 1.98 | **DISABLED** |
| hive | 650 | 2.55 | **DISABLED** |

**11 of 15 maps: the recruit walks to the anchor and can never build.** Turret
count would collapse toward zero in the late band, and since LATE_TURRET-at-home
measured ratio 0.32 against forward's 1.96, the leg would have read as *"the
forward anchor doesn't matter"* — **a false negative produced by geometry, not by
strategy.**

This is precisely the failure the code's own comment at `:2544` warns about for a
*different* constant: *"would exceed anything reachable and would silently
disable the whole arm rather than relocate it."* **The same trap exists on the
knob next to it and is not guarded.**

*This is now moot for shipping — the road is closed. It is not moot as
machinery, and machinery is where the queue just went.*

---

## 5. NEW: where the field actually places, in the knob's own units

Exact, no approximation. With `D² = d²_cores` known per map:

```
d2_own   = t²·D² + h²
d2_enemy = (1−t)²·D² + h²
  ⇒  t = (1 + (d2_own − d2_enemy)/D²) / 2        (exact)
```

| population (r150+, FORWARD) | n | p10 | p25 | **MED** | p75 | p90 |
|---|---|---|---|---|---|---|
| **US** | 527 | 0.57 | 0.67 | **0.78** | 0.89 | 1.00 |
| **THEM (field)** | 3,816 | 0.61 | 0.69 | **0.82** | 0.99 | 1.12 |

- **`LATE_FORWARD_NUM/DEN = 3/5` → t = 0.60, already at the field's p10.**
- The proposed **`2/5` → t = 0.40 is below the field's entire p10–p90 range.**
- Values on the field's band: **4/5 (0.80) or 5/6 (0.833)**; 3/4 (0.75) and 7/8
  (0.875) sit inside its IQR.

**And t is stable across maps** — per-map field medians run 0.71–1.12, clustered
0.75–0.88, against a 20× swing in raw d². **So a single fraction constant *can*
land the distribution.** The parameterisation was never the problem; the value
and the justification were.

Two shape findings the on-axis anchor cannot express:
- **Off-axis offset**: the field's forward turrets sit a median **2.1 tiles off
  the core axis** (p90 5.7); ours **1.0** (p90 3.0). A pure axis anchor is a
  narrower placement than the field's.
- **t > 1 happens** (field p90 = 1.12; fjordgate median 1.12) — turrets placed
  *beyond* the enemy core. `num//den` with num ≤ den cannot produce this at all.

---

## 6. NEW: re-check of FARGUN-COVERAGE, the instrument that closed the road

**Validation first.** Reproducing the builder's absolute cut `d2_own > 110`:

| stratum | builder | **mine** |
|---|---|---|
| COVERED US | 253 / 43.1% | 249 / **43.8%** |
| COVERED FIELD | 2,087 / 68.6% | 2,075 / **68.8%** |
| ALONE US | 825 / 32.6% | 829 / **32.4%** |
| ALONE FIELD | 1,530 / 44.7% | 1,542 / **44.6%** |

**Reproduced within noise. The builder's numbers are correct as computed.**

**The problem is the cut, not the arithmetic.** `d2_own > 110` is absolute, but
core separation varies 20×, so the same threshold selects utterly different
tactical positions:

| map | d²cores | t at d²=110 | what "far" means there |
|---|---|---|---|
| fjordgate | 32 | 1.85 | **past the enemy core** |
| meander | 49 | 1.50 | **past the enemy core** |
| antler | 64 | 1.31 | **past the enemy core** |
| moonrise | 81 | 1.17 | **past the enemy core** |
| lighthouse–heart | 128–144 | 0.87–0.93 | deep forward |
| atoll–archipelago | 288–392 | 0.53–0.62 | **mid-field** |
| hive | 650 | 0.41 | **our own half** |

On hive, a "far gun" is in **our own half**. On meander it is **past their core**.

**And the two samples are drawn from different maps.** Of 1,078 US far guns,
**13** are on the four maps where d²>110 means "deep forward" (lighthouse,
nordkap, eider, heart) — the field has **535** there. Our far stratum is 89%
big-map (where the cut means mid-field); the field's is spread.

### Re-run with the map-invariant cut

| cut | COVERED gap US−FIELD | ALONE gap US−FIELD | US covered | FIELD alone |
|---|---|---|---|---|
| **absolute d²>110** | **−25.0pp** | −12.2pp | 43.8% | 44.6% |
| normalised t>0.50 | **−12.7pp** | −7.2pp | **51.2%** | 39.0% |
| normalised t>0.65 | **−13.6pp** | −8.1pp | **49.0%** | 38.1% |
| normalised t>0.75 | −18.2pp | −16.1pp | **45.6%** | 40.6% |

**Two things change and one does not.**

1. **The gap is real and survives.** Our forward guns do die faster than the
   field's at every cut. **The direction of the verdict is unaffected.**
2. **The magnitude roughly halves** at the t>0.5 and t>0.65 cuts (−25.0pp →
   −12.7/−13.6pp).
3. **The specific sentence does not survive.** *"Our BEST far-gun stratum
   (covered, 43.1%) is still worse than the field's WORST (alone, 44.7%)"* —
   called *"the line that settles it"* — **reverses under every normalised cut**:
   ours-covered 51.2% / 49.0% / 45.6% against field-alone 39.0% / 38.1% / 40.6%.
   Our best stratum **beats** their worst once the comparison is map-invariant.

**Mechanism of the artifact**: the absolute cut discarded most of our forward
guns (n 249 → 670 covered under t>0.50), keeping mainly our big-map ones, and
compared them against the field's all-map population.

### What I am and am not claiming

**I am not claiming the forward road should reopen.** The verdict rests on three
instruments; the arena null (n=360) — **now known to be a SELF-PLAY pool mislabelled FIELD, so it is unmeasured rather than null** — and the `:1434` wide-map step function are
untouched by this and both point the same way. **The honest amendment is: the
third instrument shows a gap about half the stated size, and its headline line is
a cut artifact.**

**Limits of my own re-check, stated so they are not re-inherited:**
- Coverage is not randomly assigned — the builder's confound, inherited intact.
- Survival is confounded by whether we were winning that game; neither read
  controls for it.
- Build↔death matching pairs FIFO on `(file, team, kind, x, y)`; a rebuilt tile
  could mis-pair. Not audited.
- Censoring: builds within 50 rounds of game end are dropped, which biases toward
  longer games.
- `THEM` = our ladder opponents, mostly 1500-1700. The `opp≥1700` forward sample
  is only **n=192** — the actual top of the field is thin here, and the archive
  is dominated by our own games (corpus-howto trap #4).

---

## 7. What I would do with this

1. **Nothing on the anchor.** The road is closed on independent evidence and I
   have no result that reopens it.
2. **Record §4 as a machinery defect**, since the queue just moved to machinery:
   *the anchor knob accepts values its own band gate forbids, and the failure is
   silent.* One assert, or clamp `num/den ≥ 1/2`, and the trap is gone. It is the
   same class as the four defects already queued.
3. **Amend the FARGUN note in place** with §6, per the standing rule that a
   deliverable found overstated gets amended by its author rather than argued
   about. The direction stands; the magnitude and the headline line do not.
4. **Retire "median d² to own core" as a comparison statistic** in favour of the
   along-axis fraction t, which is map-invariant, is the unit the constant is
   already written in, and would have made both errors impossible to state.

*Process note for the tape: the builder's standing check — "before a number
becomes a decision, name the population it is about" — is the right rule, and
§6 shows it needs a companion. **Naming the population is not enough if the
threshold that defines it is not commensurable across the population.** Both of
today's errors and this one are the same shape: a cut that means different things
in different cells.*
