# Pricing the gunner against the sentinel — and the answer is neither

**Research arm, 2026-08-09.** The brief: *price the gunner against the sentinel under
our actual ruleset and our actual measured data, and say which one we are wrong
about.* **ZERO replay downloads** — everything below is on disk already.

> ## THE ANSWER IN THREE LINES
>
> 1. **On realised lifetime output the sentinel is the cheaper weapon in every
>    rating band, including ≥1900** — 0.652 Ti/damage-point against the gunner's
>    0.678 at ≥1900 (clean third-party, N=2,228 sentinels / 8,205 gunners).
>    **We are not wrong about which turret we prefer.**
> 2. **The "top tier kills with gunners" premise does not survive per-team
>    disaggregation.** Across 53 third-party teams, `corr(rating, gunner build
>    share) = −0.023` and `corr(rating, gunner kill share) = −0.025`. The pooled
>    53% is a **mixture of two incompatible doctrines** — Pivot (1956) kills 100%
>    gunner, Clankers (1984) kills 99.8% sentinel — and **no team sits at the
>    pooled value**. `MARKER.`
> 3. **What we are actually wrong about is where the sentinel stands.** Ours sit
>    at median d²=18 from our OWN core, 30.7% of them forward of midfield, firing
>    at **13.5% of their reload ceiling**. Every other measured sentinel-builder
>    puts them at d²=53-181 from home, 63.6-92.5% forward. **Same weapon, wrong
>    end of the map.**

---

## 0. VERSION TAG AND FROZEN INPUTS

| | |
| --- | --- |
| repo git sha at run | `2f29fd6` |
| `replay_archive/` at run | **8,143** `.replay26` (8,143 at close; 8,103 at freeze) |
| scripts | session scratchpad `gvs/` — **not committed** (see §7) |

The keeper daemon appends to `corpus/` every ~10 min, so every input was frozen
into a scratchpad before use and **every number below is read from the freeze**.

| artifact | rows | md5 |
| --- | ---: | --- |
| `meta_join_fresh.tsv` (regenerated offline by `tools/corpus/meta_attrib.py`) | **7,754** | `184cc483` |
| `full.turrets.tsv` (**new decoder**, one row per turret emplacement) | **114,149** | `b00fd00c` |
| `full.files.tsv` (**new decoder**, one row per file × team) | **15,508** | `88fc1a4d` |
| `killmix.tsv` (`killmix_decode.py` **reused unchanged**) | **15,508** | `b25e7997` |
| `scale_true.tsv` (**new probe**, clean single-build rounds) | **6,029** | `a300c8c1` |
| `corpus/econ.tsv`, `corpus/builds.tsv` | as committed | — |

`meta_attrib.py`'s own gates on this pull, all offline: **CHECK 1** seat+winner vs
`join.tsv` **1,630/1,630 = 100.0000%**; **CHECK 2** sidecar score/winner vs the
`winner` field inside each replay binary **1,554/1,554 = 100.0000%**.
Population: **7,754 attributed files = 2,198 clean ours + 5,431 clean third-party**
(`us_side == none AND related == none`), 125 files excluded as plan-B contaminated.
Both decoders ran with **0 errors** on all 7,754 files.

**Bands are on `ratingABefore` / `ratingBBefore` only.** `teamARating`/`teamBRating`
are live joins and are not touched anywhere in this cut.

### Populations, and the label each one carries

Method rule 5 says state the population inline. Three appear below and they are
**not interchangeable**:

- **`TP <band>`** — clean third-party side-games, banded on **that side's own**
  at-match `ratingBefore`. This is the clean field.
- **`FIELD-IN-OUR-GAMES`** — the opponent's side in our own 2,198 clean games.
  **This is not a field figure.** It is confounded by our matchmaking band and by
  whatever our bot induces opponents to do. It is reported only where it is the
  honest denominator for a vs-us comparison.
- **`US (OpenSverige)`** — our own side in those same 2,198 games.

**Correction carried forward, with its provenance.** The brief I was given quoted
*"the field builds 9.00 gunners"* and derived a 4.5× under-build. The coordinator
caught and corrected this mid-run: the 9.00 row in
`upward-pricing-top-tier-2026-08-09.md` §2.3 is labelled **"field, in our games"**,
n=2,053 — the `FIELD-IN-OUR-GAMES` population, not the clean field. I reproduce it
at **8.86** on my larger pull and it is used nowhere in this document's pricing.
The banded comparison is done against `TP ≥1900` (§4).

---

## 1. TEETH TEST — FOUR GUARDS, BOTH POPULATION BRANCHES, AND ONE STATISTIC THAT HAD NO TEETH

Rule: **prove teeth per GUARD, not per tool**, and per method rule 2, test **each
branch** of any filter that partitions the population. Every guard below was run
separately on 400 clean **ours** files and 400 clean **third-party** files.

| branch | guard | what it protects | TRUE | CORRUPTED | verdict |
| --- | --- | --- | ---: | ---: | --- |
| ours | **G1a** damage constants (swap 7↔18) | the entire Ti/dmg arithmetic in §3 | 0.9557 | **0.1000** | **PASS** |
| ours | **G1b** shooter-team ledger (flip team) | every per-team quantity in §4-§6 | 0.9557 | **0.0658** | **PASS** |
| ours | **G2** lifetime (ignore `removeEntity`) | survivability + amortisation in §3-§4 | 0.4707 | **0.0000** | **PASS** |
| ours | **G3** vs shipped `builds.tsv` (team-flip) | the census grain | 1.0000 | **0.1272** | **PASS** |
| third-party | **G1a** | " | 0.9302 | **0.0828** | **PASS** |
| third-party | **G1b** | " | 0.9302 | **0.0988** | **PASS** |
| third-party | **G2** | " | 0.4680 | **0.0000** | **PASS** |
| third-party | **G3** | " | 1.0000 | **0.0692** | **PASS** |

G1a/G1b statistic: share of file×team rows (with ≥50 observed damage) where
`pred_dmg / obs_dmg_dealt` is within ±10%. G3 compares my per-file×team turret
counts against `tools/corpus/replay_builds.py` — an **independently written,
shipped decoder** — and requires exact agreement; the teeth arm re-runs the same
comparison with the team index flipped.

> ### THE STATISTIC MATTERS AS MUCH AS THE GUARD.
> **My first version of G1b had no teeth and the guard was fine.** I scored
> `pred/obs` as a *pooled sum over both teams*. A team-swap of the ledger is an
> exact no-op in that sum: TRUE **1.0000**, CORRUPTED **1.0000**. Moving to a
> **per file × team** statistic collapsed it to **0.0658 / 0.0988**.
>
> This is the same shape as the prior session's G3 failure (a seat flip is nearly
> a no-op in top-vs-top games). **A symmetric corruption vanishes under a
> symmetric statistic.** Both readings are printed side by side in the tooling so
> the failure is visible rather than inferred.

**Second, independent validation, internal to the decoder.** `pred_dmg`
(= 7·gunner_shots + 18·sentinel_shots + 2·builder_attacks) versus `obs_dmg_dealt`
(the sum of negative `updateHp` on the other team's entities) over all 15,508
file×team rows: on the kill-mix restriction the pooled ratio is **1.0002** and
**`sh_other = 0` across all 15,508 rows** — every one of the shots landing on a
core footprint resolved to a live gunner or sentinel, none to an untracked tile.

**That zero is also a ruleset measurement, and it settles an ambiguity — see §2.4.**

---

## 2. THE RULESET, VERIFIED LINE BY LINE — AND TWO CORRECTIONS, ONE OF THEM LOAD-BEARING

Method rule 7: verify each constant against `docs/reference/official-docs.md` and
quote the line. I did. **Two things in the brief and one thing in the project's own
`CLAUDE.md` are wrong.**

### 2.1 What checks out

| claim | verdict | quoted source |
| --- | --- | --- |
| Gunner 25 HP / 20 Ti / dmg 7 / reload 1 / 4 ammo / r²=13 | ✅ | `official-docs.md:1391` — `Gunner \| 25 \| 20 \| 13 \| 13 \| 7 \| 4 \| 1` |
| Sentinel 40 HP / 30 Ti / dmg 18 / reload 2 / 10 ammo / r²=32 | ✅ | `official-docs.md:1392` — `Sentinel \| 40 \| 30 \| 32 \| 32 \| 18 \| 10 \| 2` |
| Sentinel out-damages gunner over time | ✅ | `:257` — *"it out-damages one over time: **18 every 2 rounds against 7 every round**"* |
| Sentinel is the cheaper one to run per damage point | ✅ | `:257` — *"**per point of damage a Sentinel is slightly cheaper to run than a Gunner**"* |
| Gunner's line is blocked by units and buildings | ✅ | `:242` — *"The line stops at **the first targetable tile (a builder bot or a building)** in its facing direction; empty tiles don't block it, but walls do"* — note it says *a* builder bot, i.e. **either team's**, so a gunner is blocked by its own screen |
| Sentinel ignores obstacles | ✅ | `:257` — *"unlike a Gunner's, is **never blocked by walls or units in the way**"* |
| Ammo has no passive income; core converts Ti 1:1 | ✅ | `:225` — *"Ammunition is produced at the Core by converting titanium 1:1 with convert_ammo()"* |
| Heal 1 Ti → +4 HP, 8 HP/Ti stacked, cap 2 | ✅ | `:1213` — *"Heals 4 HP for 1 Ti — **if a friendly Builder Bot is standing on a friendly building on the target tile, both are healed in the same call**"* |
| Builder attack: 2 Ti → 2 dmg, **buildings only** | ✅ | `:1201` — *"Builder Bots can attack **the building** on any orthogonally adjacent tile… **Costs 2 Ti per hit for 2 damage**"* |
| Gunner `rotate()` = 10 Ti + 1 cooldown; sentinel cannot rotate | ✅ | `:282` — *"Rotation costs exactly 10 Ti and triggers a 1-round action cooldown. **Sentinels and Launchers have no rotate()**"* |

### 2.2 CORRECTION 1 — cost scaling is **ONE GLOBAL ADDITIVE TEAM FACTOR**, and this is measured, not read

Both my brief (*"the Nth gunner costs `floor(1.2^(N-1) * 20)`"*) and the project's
own `CLAUDE.md` (*"every buildable entity's cost is floor(scale * base_cost), **per
category**"*) are wrong. The organisers' primary says:

> `official-docs.md:1353` — *"All build costs scale upward as you build more
> entities… Each conveyor/splitter/barrier built adds +1% to **your team's scale
> factor**, each harvester +5%, each launcher +10%, and each builder bot/gunner/
> sentinel +20%; destroying an entity removes its contribution again."*
>
> `official-docs.md:1421` — *"`effective_cost = base_cost × scale_factor`"*

Singular: **one factor, for the team, that every build feeds.** There is one
getter, `get_scale_percent()`, with no per-entity variant.

**I did not take the doc's word for it.** `updatePlayers` carries each team's
titanium balance every round. Isolating **clean rounds** — exactly one entity built
by team T and nothing else touching T's titanium (no heal, no builder attack, no
gunner rotate, no `convert_ammo`, no delivery to T's core) — makes the balance
delta *equal to the build cost*. Comparing that observed cost against the three
candidate models, on 400 files:

| model | exact match | |
| --- | ---: | --- |
| **GLOBAL additive** (`1 + .20·(bots+gunners+sentinels) + .05·harv + .10·launch + .01·(conv+split+barrier)`, live entities) | **5,050 / 5,051 = 99.98%** | ✅ |
| CATEG additive (per-category, as `CLAUDE.md` says) | 861 / 5,051 = 17.05% | ✗ |
| COMPOUND (`1.20^n`, as the brief says) | 494 / 5,051 = 9.78% | ✗ |

The residual is not noise: the 978 initially-mismatching rows were **all** exactly
−10 Ti and **all** on rounds ≡ 3 (mod 4) — the passive income tick, on a phase I had
excluded wrongly. Excluding `rnd % 4 == 3` instead leaves **one** mismatch in 5,051.
(Free byproduct: **passive titanium lands on rounds ≡ 3 mod 4.**)

Teeth on the probe, both arms collapsing: shifting the titanium series by one round
(`--corrupt=offset`) drops GLOBAL to **16.78%**; not decrementing on death
(`--corrupt=live`) drops it to **50.66%**.

**Why this is load-bearing for the question I was asked.** Because a *single* factor
multiplies both base costs:

> **the gunner : sentinel price ratio is pinned at 20:30 = 2:3 at every scale, in
> every game state, forever.** Turret choice cannot move it, and no build order can
> make a gunner relatively cheaper than it is at scale 1.0.

| +20% steps taken (every bot + gunner + sentinel **alive**) | scale | gunner Ti | sentinel Ti | builder bot Ti |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1.00 | 20 | 30 | 30 |
| 2 | 1.40 | 28 | 42 | 42 |
| 4 | 1.80 | 36 | 54 | 54 |
| 6 | 2.20 | 44 | 66 | 66 |
| 8 | 2.60 | 52 | 78 | 78 |
| 10 | 3.00 | 60 | 90 | 90 |
| 12 | 3.40 | 68 | 102 | 102 |
| 14 | 3.80 | 76 | 114 | 114 |
| 16 | 4.20 | 84 | 126 | 126 |

The brief asked *"where does each become uneconomic"*. **Under the true rule the
question has no per-turret answer** — there is no N at which the gunner becomes
uneconomic *relative to the sentinel*, because they inflate in lockstep. What the
table actually prices is something else, and more useful: **every builder bot you
keep alive raises the price of your next gunner by 4 Ti and your next sentinel by
6 Ti.** At the ≥1900 tier's 5.59 live bots that is a standing +112% on the scale
before a single turret is bought.

**And it re-prices the barrier.** A barrier is +1% to the *global* factor, so 20
barriers add +20% — **+6 Ti to every subsequent sentinel and +6 Ti to every
subsequent builder bot**. The per-category model hides this cost entirely. The
brief's "~8× HP/Ti ablative screen" is a scale-1.0 figure; at scale 2.6 a barrier
costs 7 Ti for 30 HP = **4.3 HP/Ti**, and it still only screens a sentinel, never a
gunner (`:242` above).

### 2.3 CORRECTION 2 — one brief claim is UNVERIFIED against the primary

The brief states the sentinel's line *"does not harm friendlies it passes through."*
**The official docs never say this.** `:257` says only that the line is *"never
blocked by walls or units in the way"* — blocking and damaging are different
claims, and the primary is silent on the second. I flag it rather than repeat it.
§2.4 gives the measured answer.

### 2.4 A ruleset fact the corpus settles that the docs leave open

Does a sentinel shot damage **everything** along its line, or exactly one target?
The docs are ambiguous. **The measurement is not.** If a shot hit multiple entities,
reconstructing damage as `18 × shots` would systematically **under**-predict
observed damage. It does not — it slightly **over**-predicts (pooled 1.0002 at the
core; per-row over-prediction is the expected signature of final-blow overkill
clipping). Combined with `sh_other = 0` across 15,508 rows:

> **MEASURED: one `fireTurret` event = exactly one target taking full nominal
> damage, for both turret types.** N = 15,508 file×team rows. A sentinel does not
> rake its line, and it therefore also does not damage friendlies standing in it.

---

## 3. THE ARITHMETIC, THREE WAYS, WITH ITS ASSUMPTIONS ON THE PAGE

### (a) Marginal / ammo only — near-parity, sentinel marginally ahead

Ammo is titanium (§2.1), so ammo cost *is* a titanium cost.

| | gunner | sentinel |
| --- | ---: | ---: |
| ammo per shot | 4 | 10 |
| damage per shot | 7 | 18 |
| **Ti per damage point** | **0.5714** | **0.5556** |

**Confirmed as stated in the brief.** The sentinel is **2.9% cheaper** per damage
point on ammo alone, and the organisers say so in prose (`:257`). Near-parity; on
its own this decides nothing.

**Assumption made explicit:** this prices a shot that *connects for full damage*.
§2.4 shows that assumption holds to 0.02% at the core.

### (b) Amortised over realised lifetime damage — sentinel wins in every band

This one needs measurement, not algebra. **New decoder**, one row per turret ever
placed: build round, death round, shots fired while alive at its tile, placement
geometry. Damage delivered = shots × nominal damage (validated in §2.4).

Price = `(base_cost + ammo × shots) / (damage × shots)`, at scale 1.0. **Per §2.2
the ratio between the two columns is scale-invariant**, so the comparison holds at
any game state even though the levels are scale-1.0 figures.

| population | gunner Ti/dmg | sentinel Ti/dmg | **ratio g/s** | N gunners | N sentinels |
| --- | ---: | ---: | ---: | ---: | ---: |
| TP <1550 | 0.7176 | 0.6316 | **1.136** | 20,526 | 5,240 |
| TP 1550-1699 | 0.7236 | 0.6651 | **1.088** | 13,851 | 2,937 |
| TP 1700-1799 | 0.7110 | 0.6768 | **1.051** | 8,380 | 3,926 |
| TP 1800-1899 | 0.6787 | 0.6541 | **1.038** | 5,608 | 718 |
| **TP ≥1900** | **0.6777** | **0.6520** | **1.039** | 8,205 | 2,228 |
| **TP ≥1700 pooled** | **0.6885** | **0.6650** | **1.035** | 22,193 | 6,872 |
| FIELD-IN-OUR-GAMES | 0.6819 | 0.6288 | 1.085 | 19,464 | 3,823 |
| **US (OpenSverige)** | 0.6919 | 0.6601 | **1.048** | 4,286 | 5,407 |

> **The sentinel is cheaper per damage point in every single band, including the
> band that supposedly proves the opposite.** The gunner is 3.9% more expensive at
> ≥1900 and 3.5% more expensive across ≥1700. The gap *narrows* with rating (13.6%
> at <1550 → 3.9% at ≥1900) but never crosses.

The underlying quantities, which are more interesting than the ratio:

| population | kind | N | shots/turret | **dmg/turret** | % never fire | med lifetime | % died | shots/live-round | **% of reload ceiling** |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TP 1700-1799 | gunner | 8,380 | 20.47 | 143.3 | 15.6% | 56 | 50.0% | 0.144 | 14.4% |
| TP 1700-1799 | sentinel | 3,926 | 13.75 | **247.5** | 15.3% | 46 | 42.8% | 0.114 | 22.7% |
| TP 1800-1899 | gunner | 5,608 | 26.64 | 186.5 | 7.6% | 61 | 50.4% | 0.214 | 21.4% |
| TP 1800-1899 | sentinel | 718 | 16.92 | **304.5** | 16.7% | 42 | 37.3% | 0.152 | 30.3% |
| **TP ≥1900** | gunner | 8,205 | 26.88 | 188.2 | 3.9% | 63 | 46.5% | 0.207 | 20.7% |
| **TP ≥1900** | sentinel | 2,228 | 17.28 | **311.0** | 3.9% | 74 | **23.5%** | 0.114 | 22.7% |
| TP ≥1700 | gunner | 22,193 | 24.40 | 170.8 | 9.2% | 60 | 48.8% | 0.183 | 18.3% |
| TP ≥1700 | sentinel | 6,872 | 15.23 | **274.1** | 11.8% | 55 | 36.0% | 0.117 | 23.4% |
| **US** | gunner | 4,286 | 23.71 | 166.0 | 8.3% | 47 | 55.6% | 0.120 | **12.0%** |
| **US** | sentinel | 5,407 | 15.94 | 286.8 | 11.2% | 92 | 45.7% | 0.068 | **13.5%** |

**The brief's survivability hypothesis is refuted in the direction it feared.** It
asked *"if gunners die fast, the amortised price collapses."* Gunners do die faster
— **46.5% of ≥1900 gunners are destroyed against 23.5% of sentinels**, and the
sentinel's median life is 74 rounds against the gunner's 63 — but that makes the
sentinel look **better**, not worse. There is no reading of the survivability data
that rescues the gunner.

### (c) Per-round throughput at a contested tile — the load-bearing question

The brief's framing: *7 dmg/round vs 9 dmg/round against a defender healing at
4 HP/Ti with an adjacency cap.* The core's 2×2 footprint has 8 heal-capable ORTH8
seats; each occupied seat restores 4 HP/round for 1 Ti (8 HP if a bot stands on a
building, `:1213`).

**At nominal rate**, the screen is weak:

| occupied seats | heal HP/rnd | gunners to break even | sentinels to break even |
| ---: | ---: | ---: | ---: |
| 0.451 *(Pantheon)* | 1.80 | 0.26 | 0.20 |
| 0.677 *(≥1900 band)* | 2.71 | 0.39 | 0.30 |
| 1.239 *(**OpenSverige**)* | 4.96 | 0.71 | 0.55 |
| 1.649 *(Clankers)* | 6.60 | 0.94 | 0.73 |
| 8.000 *(saturated)* | 32.00 | 4.57 | 3.56 |

*(Seat figures quoted from `upward-pricing-top-tier-2026-08-09.md` §3.1/§3.3. The
1.239 is **OpenSverige's own** mean occupied seats — copying the subject with the
number.)*

**But nobody fires at nominal rate.** Measured duty cycle is 12-23% of the reload
ceiling everywhere. Re-priced at *measured* throughput:

| population | gunner **effective** dmg/rnd | sentinel **effective** dmg/rnd | gunners needed to break OUR 4.96 HP/rnd screen | sentinels needed |
| --- | ---: | ---: | ---: | ---: |
| TP ≥1900 | 1.45 | **2.05** | 3.42 | **2.42** |
| TP ≥1700 | 1.28 | **2.11** | 3.87 | **2.36** |
| **US** | 0.84 | **1.22** | 5.90 | **4.05** |

> **This is the answer to "does either turret alone out-damage a healing screen".**
> **Neither does — not at N=1, and not at any realistic N below ~2.4.** Against our
> own collar a ≥1900 attacker needs **2.42 sentinels or 3.42 gunners** *continuously
> aimed at the core* just to reach net zero. That is the heal tax made mechanical,
> and it is why our core costs **1,588 damage points to destroy against the ≥1700
> tier's 1,031** (§5, reproduced at N=909 / N=1,694).
>
> **The sentinel needs ~30% fewer emplacements than the gunner to break the same
> screen, at every tier.** The reload disadvantage (0.5 shots/round ceiling) is
> already priced into these numbers via the measured duty cycle.

---

## 4. THE CORPUS MEASUREMENTS

### 4.1 Turret census and the under-build, against the band-appropriate row

| population | side-games | gunners/g | sentinels/g | launchers/g | rotations/g | shots/g | shots/turret |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TP <1550 | 4,780 | 4.29 | 1.10 | 0.24 | 7.12 | 108.0 | 20.03 |
| TP 1550-1699 | 1,985 | 6.98 | 1.48 | 0.92 | 21.87 | 153.5 | 18.15 |
| TP 1700-1799 | 1,780 | 4.71 | 2.21 | 0.93 | 7.43 | 126.7 | 18.33 |
| TP 1800-1899 | 805 | 6.97 | 0.89 | 0.35 | 8.17 | 200.7 | 25.54 |
| **TP ≥1900** | **1,512** | **5.43** | **1.47** | 0.09 | 8.34 | **171.3** | **24.83** |
| TP ≥1700 | 4,097 | 5.42 | 1.68 | 0.51 | 7.91 | 157.7 | 22.23 |
| *FIELD-IN-OUR-GAMES* | 2,053→**2,198** | *8.86* | *1.74* | *0.68* | *23.68* | *268.6* | *25.35* |
| **US (OpenSverige)** | **2,198** | **1.95** | **2.46** | 0.70 | 13.42 | **85.4** | **19.38** |

**Every load-bearing figure from `upward-pricing-top-tier-2026-08-09.md` §2.3
reproduces on this larger, independently regenerated pull** (their N=2,053 /
1,472 → mine N=2,198 / 1,512): ours 1.98/2.34 → **1.95/2.46**; ≥1900 5.36/1.49 →
**5.43/1.47**; 1700-1799 4.72/2.10 → **4.71/2.21**; field-in-our-games 9.00/1.78 →
**8.86/1.74**. The coordinator's correction is confirmed from the primary: the
9.00-class row is the in-our-games population.

**The under-build, derived against the band-appropriate row rather than taken:**
**1.95 vs 5.43 = 2.78× at ≥1900**, and **1.95 vs 4.71 = 2.42× at 1700-1799**. Not
4.5×. But §6 shows the whole comparison is against a mixture, and §4.4 shows what
the individual teams actually do.

### 4.2 Ammo: are we ammo-limited or emplacement-limited?

Per the coordinator's pre-registration at `4111640` — *confirms ammo-limited* if
our shots-per-built-turret is materially below the ≥1900 tier's **while** `ti_end`
is materially above; *refutes* if shots-per-turret is at or above theirs, or
`ti_end` at or below.

**The gunner/sentinel split was not available from `econ.tsv` (its `shots` column
is pooled). I wrote the decode, and it carries the §1 teeth test**, so this is
answered split, not pooled.

| population | ammo CONVERTED/g | ammo **SPENT**/g | converted − spent | **ammo_end** | **ti_end** |
| --- | ---: | ---: | ---: | ---: | ---: |
| TP 1700-1799 | 726.0 | 688.8 | 37.2 | 37.2 | 324.9 |
| TP 1800-1899 | 933.4 | 893.3 | 40.2 | 40.2 | 207.7 |
| **TP ≥1900** | **867.0** | **838.1** | **28.9** | **28.9** | **266.5** |
| TP ≥1700 | 818.8 | 784.1 | 34.7 | 34.7 | 280.3 |
| **US (OpenSverige)** | **727.5** | **577.0** | **150.5** | **150.5** | **1,694.5** |

*(Spent = 4·gunner_shots + 10·sentinel_shots from the new decoder; converted,
`ammo_end` and `ti_end` from `corpus/econ.tsv`.)*

> ### VERDICT: **REFUTED on the mechanism — we are EMPLACEMENT-limited, not ammo-limited.** `MECHANISM.`
>
> **The pre-registered surface partially triggers and I am disclosing that.** Our
> shots-per-built-turret is **19.38 against the ≥1900 tier's 24.83** (22% below),
> and our `ti_end` is **1,694.5 against their 266.5** (6.4× above). By the letter of
> the pre-registration that reads "confirms".
>
> **A third column not in the pre-registration contradicts the mechanism it names.**
> **We finish games holding 150.5 unspent ammunition against their 28.9** — 5.2×
> more. Ammunition we already bought and never fired. A team whose turrets are
> silent *because they cannot afford to shoot* does not end with five times the
> field's ammo reserve on top of 6.4× the titanium. **We convert 727.5 and spend
> 577.0; the ≥1900 tier converts 867.0 and spends 838.1.** They run their
> ammunition account down to the floor. We do not, and could have converted another
> 1,694 Ti besides.
>
> **The gap decomposes, and it is mostly emplacements.** Our 85.4 shots/side-game
> against their 171.3 is a shortfall of 85.9. Holding our own shots-per-turret
> fixed and giving us their turret count (6.90 vs our 4.41) recovers 133.7 shots —
> so **turret count explains 48.3 of the 85.9 gap (56%)** and duty cycle the
> remaining 37.6 (44%).
>
> **Standing finding, with its subject copied.** `docs/research/tactics/INDEX.md:458`
> — *"We end r200-300 holding more titanium than **Ouroboros** while buying a
> twelfth as much ammunition."* **The subject is Ouroboros specifically.** This cut
> extends the banking half of it to the clean third-party ≥1900 population, and
> **narrows the buying half**: against ≥1900 we convert 727.5 to their 867.0 —
> 0.84×, not a twelfth. **We do not under-buy ammunition against the top tier. We
> under-spend it, because we do not own enough turrets pointed at anything.**

### 4.3 Placement — and this is where our number is the outlier

| population | kind | N | med d²_own | med d²_enemy | **% forward** | **% ever hit an enemy core** |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| TP 1700-1799 | gunner | 8,380 | 81 | 20 | 62.6% | 32.8% |
| TP 1700-1799 | sentinel | 3,926 | 82 | 26 | 62.5% | 53.1% |
| **TP ≥1900** | gunner | 8,205 | 100 | 26 | **67.5%** | 19.6% |
| **TP ≥1900** | sentinel | 2,228 | 100 | 26 | **70.1%** | 46.1% |
| TP ≥1700 | gunner | 22,193 | 85 | 26 | 64.2% | 26.1% |
| TP ≥1700 | sentinel | 6,872 | 90 | 26 | 66.3% | 51.3% |
| **US** | gunner | 4,286 | 36 | **17** | 53.2% | **39.3%** |
| **US** | **sentinel** | **5,407** | **18** | **50** | **30.7%** | **41.4%** |

**Our gunners are fine.** They sit *closer to the enemy core* (d²=17) than the
≥1900 tier's (d²=26) and land on an enemy core more often (39.3% vs 19.6%). The
brief's suspicion that we mis-site our gunners is not supported.

**Our sentinels are the outlier.** Median d²=18 from our **own** core — roughly four
tiles from home — with only **30.7% forward of midfield**. Every other measured
population puts sentinels at d²_own 82-100 and 62-70% forward.

### 4.4 Per-team placement and duty — the table that changes the recommendation

| team | rating | kind | per side-game | med d²_own | med d²_enemy | % fwd | **% of reload ceiling** | **% ever hit enemy core** |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **sporks** | 2082 | gunner | 1.99 | 104 | 17 | 75.3% | 15.0% | 30.8% |
| **sporks** | 2082 | **sentinel** | **4.06** | 90 | 29 | 63.6% | 11.5% | 20.7% |
| Pantheon | 2002 | gunner | 6.80 | 100 | 37 | 64.5% | 11.3% | 11.0% |
| Pantheon | 2002 | sentinel | 1.68 | 125 | 32 | 67.7% | 22.4% | 38.0% |
| **Clankers** | 1984 | gunner | 0.44 | 17 | 181 | 10.2% | 11.4% | 1.1% |
| **Clankers** | 1984 | **sentinel** | **2.32** | **137** | 26 | **74.4%** | **46.4%** | **79.1%** |
| Pivot | 1956 | gunner | 7.93 | 146 | 26 | 77.3% | 19.0% | 21.8% |
| Jython | 1942 | gunner | 8.43 | 113 | 25 | 70.0% | 35.1% | 16.8% |
| not adgato | 1922 | sentinel | 0.79 | 113 | 25 | **92.5%** | 67.8% | **92.5%** |
| Erebus | 1905 | gunner | 8.56 | 74 | 34 | 59.6% | 25.8% | 27.7% |
| The Flotte Experience | 1889 | sentinel | 1.09 | 181 | 34 | 86.8% | **73.1%** | 88.7% |
| **US** | 1604 | gunner | 1.95 | 36 | 17 | 53.2% | 12.0% | 39.3% |
| **US** | 1604 | **sentinel** | **2.46** | **18** | **50** | **30.7%** | **13.5%** | 41.4% |

> **We are the only team in this table whose sentinels face the wrong way.** Ours
> are the only ones with median d²_enemy (50) *greater* than d²_own (18). Clankers
> — 1984-rated, 57.0% core-kill rate, **0.0% gunner kill share** — puts 2.32
> sentinels per game at d²_own 137, 74.4% forward, and **79.1% of them land a shot
> on the enemy core** at 46.4% of the reload ceiling. That is our own doctrine,
> executed forward, at 380 Elo above us.

---

## 5. KILL-MIX REPRODUCTION

`killmix_decode.py` **reused unchanged** from the prior session, re-run on 7,754
files. Damage points on a destroyed core, third-party, banded on the **victim**:

| population (VICTIM banded) | kills | gunner | sentinel | builder-melee | dmg/kill | pred/obs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TP victim <1550 | 1,226 | 47.3% | 46.4% | 6.2% | 995 | 0.9990 |
| TP victim 1550-1699 | 965 | 55.6% | 41.8% | 2.6% | 951 | 1.0005 |
| TP victim 1700-1799 | 794 | 50.9% | 46.7% | 2.4% | 1,096 | 1.0002 |
| TP victim 1800-1899 | 354 | 50.4% | 46.7% | 2.9% | 1,070 | 1.0003 |
| TP victim ≥1900 | 546 | 58.4% | 39.0% | 2.6% | 910 | 1.0002 |
| **TP victim ≥1700** | **1,694** | **52.9%** | **44.5%** | **2.5%** | **1,031** | 1.0002 |
| TP victim ≥1700, ≤r250 | 1,023 | 52.0% | 46.5% | 1.4% | 802 | 1.0002 |
| **OUR core is the victim** | 909 | 51.4% | 46.8% | 1.9% | **1,588** | 1.0001 |
| **WE are the killer** | 715 | **22.0%** | **70.2%** | 7.7% | 1,003 | 1.0000 |
| WE are the killer, ≤r250 | 524 | 19.1% | 77.2% | 3.7% | 720 | 1.0000 |

**The prior session's headline figures reproduce**: 53.1/44.4/2.5 → **52.9/44.5/2.5**
at N=1,694 (was 1,588); ours 22.7/69.2/8.1 → **22.0/70.2/7.7** at N=715 (was 653);
our core's 1,596 dmg/kill → **1,588**. Verified as instructed.

### 5.1 A subject error in the banding, worth naming

The prior document bands the kill mix on the **victim's** rating. *"How top-tier
cores die"* and *"what the top tier kills with"* are different questions and the
second is the one that licenses a build change. Re-cut on the **killer's** band:

| population (**KILLER** banded) | kills | gunner | sentinel | melee |
| --- | ---: | ---: | ---: | ---: |
| TP killer <1550 | 1,060 | 46.8% | 46.3% | 6.9% |
| TP killer 1550-1699 | 788 | 58.1% | 39.6% | 2.3% |
| TP killer 1700-1799 | 800 | **43.5%** | **53.4%** | 3.1% |
| TP killer 1800-1899 | 384 | **71.0%** | 28.2% | 0.8% |
| TP killer ≥1900 | 853 | 51.3% | 45.4% | 3.4% |
| TP killer ≥1700 | 2,037 | 51.6% | 45.6% | 2.8% |

**It is not monotone and it is not stable.** 43.5% gunner at 1700-1799, 71.0% at
1800-1899, 51.3% at ≥1900. A quantity that swings 27 points between adjacent bands
is not measuring a property of skill.

---

## 6. MECHANISM VS MARKER — THE ADJUDICATION

The brief pre-cleared one marker story (kill speed, dead in §2.2 of the prior doc)
and asked me to work the remaining four. I did, and then found a fifth that
subsumes them.

### 6.1 Distance / geometry — `MARKER REFUTED`

*Is the gunner share just "damage delivered from close to the core", which anything
short-ranged would produce once a kill is happening?*

Discriminator: for each team, compare its gunner share of **all** damage it dealt
against its gunner share of damage **on cores**. If geometry inflates the core
figure, core-share should systematically exceed all-share.

**It does not.** Across 61 teams: **median delta −1.3 pp, mean −4.7 pp**, and the
core gunner share *exceeds* the all-damage share in only **16 of 61** teams. The
gunner share on cores is if anything *lower* than a team's overall gunner reliance.
**Geometry does not manufacture the gunner share.** `MARKER REFUTED` — this one is
a real property of how those teams fight, not an artifact.

### 6.2 Survivability / selection — `MARKER REFUTED`

*Do we only see gunner damage from gunners that survived, and is the top tier's
gunner damage concentrated in a few long-lived emplacements?*

| population | kind | N | top-10% share of shots | top-25% | gini |
| --- | --- | ---: | ---: | ---: | ---: |
| TP ≥1900 | gunner | 8,205 | 57.0% | 78.4% | 0.691 |
| TP ≥1900 | sentinel | 2,228 | 49.0% | 73.9% | 0.644 |
| TP ≥1700 | gunner | 22,193 | 59.0% | 79.8% | 0.713 |
| TP ≥1700 | sentinel | 6,872 | 52.0% | 75.9% | 0.673 |
| US | gunner | 4,286 | 59.5% | 79.4% | 0.718 |
| US | sentinel | 5,407 | 58.5% | 80.4% | 0.719 |

Output is heavily concentrated for **both** turret types in **every** population
(gini 0.64-0.72) — and **our own concentration is indistinguishable from the top
tier's**. There is no differential selection effect to exploit. Also refuted
directly: §3(b) shows gunners are the ones that die more (46.5% vs 23.5% at ≥1900),
so survivor bias, if present, flatters the *gunner*, not the sentinel.

### 6.3 Reverse causation / affordability — `UNSEPARATED`

*Is a gunner what you can afford early, so a gunner-heavy mix marks "was ahead on
economy early"?*

The price gap is real but small and **fixed at 2:3 forever** (§2.2) — 10 Ti at
scale 1.0, 30 Ti at scale 3.0. Build timing at ≥1900: median gunner r95 (52.4% by
r100), median sentinel r124 (41.0% by r100). Gunners *are* laid earlier. But the
≥1900 band also has 5.59 live builder bots pushing the shared scale, so "afford"
is confounded with the whole build order.

**I cannot separate this with observational data.** Distinguishing "built a gunner
because it was cheaper *at that moment*" from "built a gunner because that is the
doctrine" needs a counterfactual price, which the corpus does not contain.
`UNSEPARATED.`

### 6.4 Confound with the killer's identity — `MARKER, DECISIVELY. THIS IS THE FINDING.`

*The ≥1700 population's gunner share might be driven by a handful of high-volume
teams. Check the per-team spread.*

Gunner share of damage on a destroyed **≥1700** core, by **killer** team, teams with
≥20 such kills:

| killer team | kills | gunner% | sentinel% | melee% | killer med rating |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pivot | 74 | **100.0%** | 0.0% | 0.0% | 1956 |
| Erebus | 94 | **100.0%** | 0.0% | 0.0% | 1905 |
| Powered by SmartFridge | 106 | 89.9% | 10.1% | 0.0% | 1694 |
| Besvikomat | 32 | 88.1% | 11.9% | 0.0% | 1768 |
| team lazy | 107 | 86.5% | 13.5% | 0.0% | 1816 |
| O(1) | 73 | 86.0% | 6.2% | 7.8% | 1769 |
| HTTP 418 | 82 | 68.6% | 31.4% | 0.0% | 1801 |
| Jython | 101 | 68.0% | 19.4% | 12.6% | 1942 |
| Lorem Ipsum | 83 | 50.6% | 44.3% | 5.2% | 1945 |
| not adgato | 77 | 43.0% | 53.6% | 3.4% | 1917 |
| The Flotte Experience | 98 | 42.9% | 57.1% | 0.0% | 1883 |
| **Pantheon** | 131 | **39.4%** | **60.6%** | 0.0% | **2002** |
| **sporks** | 151 | **39.3%** | **60.7%** | 0.0% | **2085** |
| Landers | 29 | 39.1% | 53.8% | 7.1% | 1718 |
| Coreflood | 32 | 29.8% | 61.4% | 8.8% | 1755 |
| kladde chatte tville | 64 | 15.6% | 84.1% | 0.3% | 1714 |
| Banminary | 21 | 12.0% | 88.0% | 0.0% | 1756 |
| 0033 | 67 | 10.2% | 89.8% | 0.0% | 1752 |
| Big O | 37 | 6.9% | 86.7% | 6.4% | 1792 |
| **Clankers** | 92 | **0.0%** | **99.8%** | 0.1% | **1990** |
| arsonist duck | 27 | 0.0% | 90.0% | 10.0% | 1724 |
| Focalground | 24 | 0.0% | 100.0% | 0.0% | 1758 |

**22 teams, median gunner share 41.1%, IQR 12.0-86.0%, range 0-100%.**
The distribution is **bimodal, not centred**: 9 of 22 teams above 50%, and the
mass sits at the extremes. **Exactly one of the 22 (Lorem Ipsum, 50.6%) lands
within 5 points of the pooled 52.9%** — the pooled figure describes essentially
no team that exists.

And the population-level test, across **53 third-party teams with ≥100 archived
side-games and ≥30 turrets** (full table in the tooling):

| correlation | value |
| --- | ---: |
| corr(rating, gunner **build** share) | **−0.023** |
| corr(rating, gunner **kill** share) | **−0.025** |
| corr(gunner kill share, **core-kill rate**) | **−0.105** |
| corr(gunner build share, gunner kill share) | +0.746 |
| **corr(rating, core-kill rate)** | **+0.767** |

> ### VERDICT: `MARKER.` The gunner-heavy kill mix carries **no information about strength**.
>
> Rating explains **nothing** of a team's gunner share (r = −0.02 on both build and
> kill share, n=53) and the gunner share slightly **anti**-correlates with the
> programme's own primary currency, core-kill rate (r = −0.11). What does track
> rating is core-kill rate itself, at **r = +0.767**.
>
> **The pooled "53% gunner at the top tier" describes no team that exists.** It is a
> mixture average over doctrines that are mutually exclusive: Pivot builds 7.93
> gunners and 0.03 sentinels per side-game; Clankers builds 0.44 and 2.32. Both are
> rated ~1970-1990. The ≥1900 band's 5.43 gunners/side-game spans **0.44 to 8.56
> across the eight teams that constitute it — a 19× range**.
>
> **And the single most important row: sporks, the #1 team on the ladder at 2082,
> builds 1.99 gunners per side-game. We build 1.95.** Its gunner *build* share is
> **32.9%**; ours is **44.2%**. **On gunners we are not under-built relative to the
> best team in the league — we are marginally over-built.** What sporks has that we
> do not is **4.06 sentinels per side-game against our 2.46**, placed forward.
>
> This is the s20 collar mistake in a new costume, and it would have failed the same
> way. *"Top teams have a thinner collar → garrison less"* was refuted 40/60. *"Top
> teams kill with gunners → build gunners"* rests on an aggregate that averages
> Clankers's zero with Pivot's hundred and lands on a number neither of them plays.

### 6.5 What the pooled figure was actually detecting

The gunner-heavy population is **not** the top of the ladder. It is the broad
1550-1900 middle (Powered by SmartFridge 1694, Besvikomat 1679, O(1) 1774, team
lazy 1816, HTTP 418 1801) plus two ≥1900 outliers (Pivot, Erebus). The ladder's
top three by rating — sporks 2082, Pantheon 2002, Clankers 1984 — average
**26.2% gunner** in their kill mix (unweighted mean of 39.3 / 39.4 / 0.0) against
the pooled 52.9%. **Weighting by side-games rather than by team is what produced
the inversion.**

---

## 7. WHAT I COULD NOT MEASURE, AND WHY

- **The engine was not probed.** `fcode_engine` is installed and exposes
  `run_game`, but `docs/two-session-protocol.md:138` reserves engine probes for the
  builder arm. §2.2's scale finding is therefore measured from **replay bytes**
  (99.98%, n=5,051) rather than confirmed against the engine directly. **A
  five-minute builder-arm probe would settle it to certainty and should be run
  before anything is built on it.**
- **Whether a sentinel damages friendlies in its line is settled only indirectly**
  (§2.4). The docs are silent; my evidence is that one-shot-one-target reconstructs
  observed damage to 0.02%. That is strong but it is inference, not a direct read.
- **"Damage delivered" is `shots × nominal damage`.** Validated at the core (§2.4)
  but not per-target elsewhere; a shot into a barrier and a shot into a core count
  the same in §3(b). The `% ever hit enemy core` column in §4.3-§4.4 is the partial
  correction, not a full one.
- **§6.3 (affordability) is `UNSEPARATED`** and I could not close it observationally.
- **Rotation cost is counted but not priced.** We rotate 13.42 times per side-game
  at 10 Ti each = **134 Ti/game**, against the ≥1900 tier's 8.34 (83 Ti). Real, but
  I did not fold it into §3(b) because I cannot attribute rotations to specific
  emplacements reliably enough. **Flagged as an open number, not reported as one.**
- **Duty cycle is measured over a turret's whole life**, including rounds when
  nothing was in its arc. It therefore conflates "no ammo", "no target", and "wrong
  facing". §4.2 separates out the ammo branch; it does not separate the other two.
- **Team-level rating is the median at-match `ratingBefore`**, so a team that
  climbed during the window is banded on its history.
- **The third-party pool is not a random sample of the league** — it is what the
  archiver happened to download. Per-team coverage runs 620 side-games (Powered by
  SmartFridge) down to 100. Every N is stated; §6.4's smallest cells are N=21-32 and
  the *pattern across 53 teams* is what carries the section, not any single row.
- **Scripts live in the session scratchpad and were not committed**, per the brief's
  one-file constraint. `corpus-howto.md` is explicit that this is how decoders get
  re-derived from scratch. **The `turret_econ_decode.py` and `scale_probe.py`
  grains are new and worth promoting into `tools/corpus/` — filing that as the
  adjacent issue rather than doing it here.**
- **I did not run the arena, submit, activate, probe the engine, or edit anything
  under `bots/` or `tools/`. No git commit.**

---

## 8. THE BUILDER HOOK, AND THE FALSIFIER

### 8.1 What NOT to build

**Do not build gunners on the strength of the 53% kill-mix inversion.** §6.4 is a
`MARKER` verdict on a correlation of **−0.02**, and against the ladder's actual top
team our gunner count is already at parity (1.95 vs 1.99). This plank should be
struck from the programme, not re-priced.

### 8.2 The smallest measurable change

> **Move the sentinel forward. Do not change the mix, the count, or the cost model.**
>
> Our sentinels are built at median d²=18 from our **own** core with **30.7%**
> forward of midfield and fire at **13.5%** of their reload ceiling. Clankers —
> 1984, **0.0% gunner**, 57.0% core-kill rate — builds 2.32 per game at d²_own 137,
> **74.4% forward**, **46.4% of ceiling**, with **79.1% landing a shot on the enemy
> core** against our 41.4%.
>
> **Smallest shippable version:** change the sentinel *siting predicate only* — the
> tile filter that currently prefers own-core adjacency — to prefer forward tiles at
> d²_enemy ≈ 26, matching the ≥1900 median. **No change to build counts, build
> order, ammo policy, or the gunner path.** One predicate.

**Why this is the smallest change with the largest measured lever:** it needs no new
titanium (we end games with 1,694.5 unspent), no new ammo (150.5 unspent), and no
new emplacements. It converts turrets we already build from 13.5% to a plausible
40-45% duty cycle, which is worth more than doubling the count would be at the
current cycle.

### 8.3 The discriminator that would falsify it

Priced in the programme's own currencies:

| | |
| --- | --- |
| **Primary** | `core_kill_share` — must **rise**. Forward sentinels are an offensive change; if the mechanism is real it converts to core kills. |
| **Secondary** | `time_to_core_kill` — should **fall** (our median as killer is r156). |
| **Mechanism check, and the real falsifier** | **sentinel duty cycle** (shots per live round) must rise from **0.068** toward the ≥1900 tier's **0.114**, and **`% of sentinels that ever land a shot on an enemy core`** must rise from **41.4%** toward Clankers's **79.1%**. Both are now directly measurable per-replay by the new decoder. |
| **Guard rail** | our core's cost-to-destroy (currently **1,588** damage points against the ≥1700 tier's 1,031) must not fall materially. Sentinels moved forward are sentinels not defending, and §3(c) says our collar already only forces an attacker to 2.42 sentinels. **If cost-to-destroy drops below ~1,300, the change is losing more than it wins.** |

> **The falsifier is sharp and it is a mechanism check, not an outcome check:** if
> forward siting lands and the **duty cycle does not move**, the "wrong end of the
> map" story is wrong and the real constraint is target availability or facing —
> and the whole §4.3/§4.4 reading should be withdrawn rather than re-tuned.

### 8.4 Currency note, as required

**One finding in this document is priced in a currency the programme does not use.**
§2.2's global-additive scale correction is a **cost-model** result. It changes what
every build costs in every plan and it has no `core_kill_share` reading at all.
**It should not be gated on the ladder — it should be handed to the builder arm as
a correction to `CLAUDE.md`, and confirmed with a five-minute engine probe first.**
The project's own documentation currently states the wrong scaling rule, and the
brief that commissioned this work inherited it.
