# IS THE SHIP BAR REACHABLE BY THE PROCESS THAT GENERATES OUR ARMS?

**Research arm, read-only analyst. Data cut `2026-08-16T08:31:10Z` (`date -u`), HEAD `97669852`.**
Independent re-derivation from the shard corpus. `tools/overnight_read.py` was run once to
learn the corpus layout and then **not used for any number in this document** — every figure
below comes from a fresh parse of the raw `scratchpad/overnight*/**.tsv` tapes.

⚠ **THE BOARD IS LIVE.** Shards were still writing rows at the cut (`G401g5` 08:20:13Z,
`SEATSPAWN` 08:21:45Z). Re-derive before quoting these numbers tomorrow.

---

## 0. THE TWO BARS BEING PRICED

| bar | source | operative form |
|---|---|---|
| **60.0%** | `PROGRAMME.md:28` `X3R0_SLOT_RULE`, re-priced by Magnus 2026-08-16 ~05:2xZ | point ≥60.00 **and** 95% CI-lo ≥58 |
| **70.0%** | Magnus, in-session 2026-08-16, verbatim: *"we will need to score 70% winrate against v140 to have any shot at the top at all, 60% is just a step in the right direction"* | same construction |

**The ±2pp clause is slack and I verified it rather than repeating it.** Solving the Wilson
interval numerically: at n=5,400 the measured share needed for CI-lo ≥58 is **59.316%**, which
is below 60.00. **So the point estimate binds at both bars** (at the 70 bar, CI-lo ≥68 needs
69.244%, again below 70.00). `PROGRAMME.md`'s own reading — *"the binding term is the 60"* — is
correct.

**This document prices the bars. It does not argue with them.** Magnus set 60 directly and has
now named 70 as the target; a statistic can say which road reaches a bar and has nothing to say
about whether the bar is right.

---

## 1. THE POPULATION, AS A RULE (condition A4)

**One observation = one ARM: one treatment tree, all its games against the v140 control pooled.**

The v140 control is the tree `bots/_v223sealrepair` (`PROGRAMME.md: INCUMBENT`, and
`results.tsv:365` — *"v140's full tree vs its v218 parent"*). Verified by md5:
`61bba628fa8a41bd9e4602d45e780aeb`.

### Inclusion rule
Every shard tape under `scratchpad/overnight/` and `scratchpad/overnight-remote/*/`, content-
deduplicated, whose control resolves to `bots/_v223sealrepair`.

Control resolution: the `# FIXTURE` header line where present (it records what actually ran),
else the worklist registry — `scratchpad/fleet_queue.tsv`, `scratchpad/corefill_work.txt`,
`scratchpad/vps/**`, `scratchpad/overnight-remote/*/worklist.txt`.

* **249 tape files on disk → 232 after content-dedup.** `scratchpad/overnight-remote/work-server-1/`
  and `scratchpad/overnight-remote/worker@work-server-1/` are the same files under two paths
  (md5-identical); counting both would have double-weighted every ws1 arm.
* **⟦CONTROL A⟧ header-vs-worklist control disagreements: 0 of 53 shards where both exist.** A
  disagreement would mean the registry is lying about what ran; the check can fire and did not.
* **⟦CONTROL A2⟧ 12 shards resolve no control at all** and are dropped — named, not silently:
  GUNAXREP, GUNAXTB, PAVEFIRST, SR1CUR, SR1NULL, SR2CUR, SR2NULL, SRNULL0, V141VS140R, LNCHMAX,
  SALTREF2, NULL140.

### Exclusions, each stated and counted (from 93 v140-control shards)

| rule | shards removed | why |
|---|---|---|
| **E1** treatment is an x3r0 artifact | **2** (V141VS140, V140VS152) | not produced by *our* arm-generating process |
| **E2** structural NULL cell (treatment tree byte-identical to control) | **0** on this control | calibration, not an arm |
| **E3** fixture-corrupt: NOWINNER rate >1% | **12** | see §1.1 |
| **E4** ran on <15 pool maps | **4** (SPKT64P 2 maps, TINYECO62 3, SEATFULL 10, RUSH72 1) | different fixture (A5) |
| **E5** n<100 | **3** (G417g4 52, SEATSPAWN 43, and one in-flight) | in flight, not yet a screen |
| | **72 shards KEPT → 59 arms** | |

**⛔ E5 IS SET AT 100, NOT 200, SPECIFICALLY TO KEEP `SEALQ`.** `_v265sealquiet` was auto-killed
at n=157 reading **25.48%** (`results.tsv:392`). A completed-arms-only or n≥200 filter drops it
and truncates the population from below — the exact hazard named in A4. It is **in** the primary
population. So are `bodyblk-autostop` (`_v262bodyblock` 47.26%), `spawnlkl-autostop` (49.72%),
`cmb294/295-autostop`, `catsolo-autostop` and `sh286-autostop`. **The primary population contains
every killed and auto-stopped arm on this control.**

**Residual truncation I cannot remove, stated as a hazard rather than a fix:** auto-stop fires
*because* a reading is low, so a stopped arm's recorded point estimate is biased low relative to
its true value (optional stopping at a lower boundary). This pushes the mean DOWN (distance to
the bar UP) and the SD UP (distance DOWN). The §2 sensitivity table brackets it.

### 1.1 Identifying the corrupted batch (E3) — how, not assertion

The signature is a **NOWINNER rate above ~1% against 0.00% on every full-speed shard.** The
12 excluded shards read 1.14–8.86% NOWINNER and every one of them last wrote between
**05:36Z and 08:13Z today**: ECOPAVE 3.92, ECOSCK4 5.13, ECOSCK6 3.42, ECOSIPC 5.13, ECOSIPH 8.86,
G402g2 2.56, G403g2 1.47, G404g3 1.14, G405g3 1.75, G414g4 3.85, G415g4 2.53, F232COLLARM(partial)
18.10. Meanwhile `CMB296`, `CMB298`, `CMB299`, `G400g4`, `G401g5`, `G406g3`, `ECOSIPHR` all
completed 5,400 games in the same window at **0.00%**.

The 1% figure is not mine: it is the pre-existing abort threshold in the runner
(`if n>=200 && nowin*100 > n -> ABORT`, `docs/coordination.md:56031`). The mechanism is on the
record at `docs/coordination.md:62863` — seven local shards running at background QoS (pri=4,
E-cores, ~1/40 remote speed). **The instrument-level point: the abort check runs at launch only,
so it never tripped on shards that degraded mid-run.**

Note `F232COLLARM` appears twice — the throttled partial (172 games, 18.10% NOWINNER) is
excluded, its clean full run (5,400, 0.00%) is kept. Exclusion is per **shard**, not per arm.

### 1.2 ⟦CONTROL C — the one that must come out the other way⟧

If the local fixture can manufacture a 60, a **byte-identical-tree** cell would sometimes show
it. Nine structural NULL cells exist across the whole corpus (treatment tree md5 == control tree
md5, identified structurally, not by name):

| cell | n | share | 95% CI |
|---|---|---|---|
| NULL114 | 5,408 | 49.98 | [48.65, 51.31] |
| NULL123 | 2,602 | 48.58 | [46.66, 50.50] |
| NULL125 | 5,400 | 51.04 | [49.70, 52.37] |
| NULL5400 | 5,400 | 49.94 | [48.61, 51.28] |
| NULLSALT | 5,408 | 51.09 | [49.76, 52.42] |
| SHIPGATENULL | 5,408 | 49.56 | [48.22, 50.89] |
| NULL140B | 5,385 | 50.88 | [49.55, 52.22] |
| NULLHOST (ws1) | 400 | 49.00 | [44.13, 53.89] |
| NULLHOST (ws2) | 400 | 52.00 | [47.11, 56.85] |

**Range 48.58–52.00; every interval covers 50.00; none comes within 4pp of 58, let alone 60.**
The fixture does not generate a 60 from nothing. A constant column would have validated
anything; this one moves and lands where it must.

### 1.3 A5 — fixture mismatch, and what the permanent benchmark costs

Magnus has fixed v140 as the benchmark permanently (*"If we move our benchmark bot all the time
all our experiments end up unusable"*). That makes non-v140 rows **permanently** non-comparable,
not merely awkward. The cost, counted:

* **93 of 232 deduped shards (40%) are on the v140 control — 307,136 games of 818,267 (37.5%).**
* The other **139 shards / ~511k games** sit on `_v197mapcode` (33), `_v146gunaxis` (32),
  `_v169launchlate160` (21), `_v171late160ammo` (8), `_v178salt` (7), `_v218mapfix` (5),
  unresolved (12) and x3r0 artifacts. **None of them is a draw from the process this bar governs**,
  and under a permanent benchmark none of them ever will be.
* Verified per row, not assumed: control comes from each tape's own header or its registry row.

---

## 2. THE ARM-GENERATING DISTRIBUTION

**n_arms = 59.** One observation = one arm's pooled measured game share against the v140 control
on the local screen.

```
mean      50.60 %
SD (obs)   4.31 pp
median    50.68 %
min       25.48 %   (_v265sealquiet, SEALQ, killed at n=157)
max       55.24 %   (_v280mix4, MIX280mix4, n=5,400)
```

Random-effects (DerSimonian–Laird, share scale): **μ = 50.96 %, τ (between-arm) = 2.49 pp**,
Q = 787.3 on 58 df, mean within-arm SD = 1.09 pp.

**Empirical distribution (all 59 arms, 1pp bins):**

```
25-26  #           1     (SEALQ 25.48 — killed arm, kept per A4)
41-42  #           1     (siegelaunch 41.98)
45-46  #           1
47-48  #####       5
48-49  #####       5
49-50  ##########  10
50-51  ########     8
51-52  ######       6
52-53  ######       6
53-54  ###          3
54-55  ##########  10
55-56  ###          3     <- ceiling: 55.24, 55.20, 55.07
------------------------------------------------  total 59
>= 58  0        >= 60  0        >= 70  0
```

### 2.1 σ-distance to the bars — my derivation

The σ-distance is **(bar − centre) / σ**. Two defensible σ choices, reported side by side.

| population | n | mean | SD_obs | μ_RE | τ_RE | **60: obs σ** | **60: RE σ** | **70: obs σ** | **70: RE σ** |
|---|---|---|---|---|---|---|---|---|---|
| **P0 all arms** | 59 | 50.60 | 4.31 | 50.96 | 2.49 | **2.18** | **3.63** | **4.50** | **7.64** |
| P0 minus SEALQ | 58 | 51.03 | 2.77 | — | — | 3.24 | — | 6.86 | — |
| n≥1,000 | 55 | 51.09 | 2.73 | — | — | 3.26 | — | 6.92 | — |
| n≥2,700 (gate mark) | 45 | 51.62 | 2.51 | — | — | 3.34 | — | 7.32 | — |
| n≥5,000 completed | 41 | 51.94 | 2.35 | 51.93 | 2.21 | 3.43 | 3.65 | 7.68 | 8.17 |
| **SINGLE-plank (A2)** | 26 | 49.14 | 2.38 | 49.13 | 2.20 | **4.56** | **4.94** | **8.75** | **9.48** |
| **MULTI-plank (A2)** | 33 | 51.75 | 5.11 | 52.39 | 2.00 | **1.61** | **3.80** | **3.57** | **8.80** |

**Which σ I lead with, and the defence the brief demands.** I lead with the **random-effects τ**,
because the question is *what does the process produce*, and that is a statement about the
distribution of arms' **true** values, not of their measurements. Using τ rather than SD_obs
**grows** the distance in most cells, so it needs defending:

1. **The inflation being removed is genuinely small.** Mean within-arm measurement SD is
   **1.09 pp** against τ = **2.49 pp**. Measurement noise contributes about
   (1.09/2.49)² ≈ 19% of the variance of the observed points on the pooled cut, and only
   (0.64/2.21)² ≈ 8% on the completed cut. **The correction is real but modest**, and on the
   completed cut it moves 60 from 3.43σ to 3.65σ — 0.2σ.
2. **In one cell it goes the other way and I am not hiding it.** On **all arms** SD_obs (4.31) is
   *larger* than τ (2.49) — because SD_obs is dominated by SEALQ at 25.48% (n=157) while DL
   down-weights that arm by its variance. And on **MULTI** arms SD_obs is 5.11 vs τ 2.00, same
   cause. **In those cells the observed-SD reading is the flattering one for reachability**
   (1.61σ to 60 on MULTI!), and it is flattering for a bad reason: an outlier fattening a tail
   the process does not actually have up there.
3. **Both readings agree on the verdict on every cut.** The narrowest honest distance to 60
   anywhere in the table is **1.61σ** and it is the artefact above; the credible band is
   **3.2–3.7σ pooled, 4.9σ single-plank**. The narrowest to 70 is **3.57σ**, same artefact,
   credible band **6.9–8.8σ**.

### 2.2 How many arms have ever cleared

* **≥60.0%: 0 of 59.** Ever, on this control, at any n.
* **≥58.0% (the CI-lo condition read as a point): 0 of 59.**
* **≥70.0%: 0 of 59.**
* Highest ever measured: **55.24%** (`MIX280mix4`). Second: 55.20 (`SH287`). Third: 55.07
  (`MIX281mix4`).
* **Stated as an exclusion, not a fail-to-exclude** (per the standing rule): the board leader's
  95% CI is **[53.91, 56.56]** — it **excludes 58** and **excludes 60**. And the fitted RE
  distribution's **99th percentile of TRUE arm value is 56.76%** (all arms) / **57.04%** (multi
  arms) / **54.25%** (single-plank); its **99.9th percentile is 58.66 / 58.57 / 55.93**. So on
  the all-arm fit, **99% of the true arm values this process draws are excluded from 58 and
  above**, and 70 is not within the 99.9th percentile of anything.

### 2.3 Board maximum vs shipping value — verified, and I disagree with the registered number

The distinction is real and I confirm it: **55.24 is a max over 59 arms, not an estimate of any
arm's value.** But the registered correction is **too large.**

| method | assumption | leader's honest value | curse |
|---|---|---|---|
| registered in `HANDOVER`/`coordination.md:60604` | "23 arms at ±1.33pp ⇒ E[max] ≈ +1.7pp" | **53.50%** | +1.74pp |
| my EB shrinkage, all-arm prior | μ=50.96, τ=2.49, se=0.68 ⇒ shrink 0.931 | **54.95%** | +0.29pp |
| my EB shrinkage, multi-arm prior | μ=52.39, τ=2.00, se=0.68 ⇒ shrink 0.897 | **54.95%** | +0.29pp |
| my conditional simulation, all-arm prior | 400k draws, keep max_measured = 55.24±0.20, report E[θ of that arm] | **54.63%** | +0.61pp |
| my conditional simulation, multi-arm prior | same | **54.85%** | +0.39pp |
| *my τ=0 counterfactual* | *all 59 arms identical* | *51.65%* | *+3.59pp* |

**Where the 53.50 comes from and why I do not accept it.** The `E[max of N at ±1.33pp]`
arithmetic is the **τ = 0** calculation — it prices how far the max of N *identical* arms strays
above their common truth. **τ = 0 is falsified on this board: Q = 787.3 on 58 df.** τ is
2.0–2.5 pp against a measurement SE of 0.68 pp, i.e. **between-arm signal is ~3.5× measurement
noise**, so the arm that tops the board is mostly the genuinely best arm and only marginally the
luckiest. My τ=0 counterfactual reproduces a large curse (+3.6pp) — confirming the *arithmetic*
of the registered figure while rejecting its *premise*.

⭐ **Independent corroboration I found only after deriving this:**
`docs/workflow-analysis/AUDIT-2026-08-16-instruments-vs-decisions.md` Q2 says the registered
+1.7pp *"is overstated ~4.7x; shrinkage fit gives selection bias 0.37pp"*. **0.37pp against my
0.29–0.61pp.** Two independent shrinkage fits land in the same place. **The 53.50 currently in
`HANDOVER.md` and `coordination.md` is over-corrected by roughly 1.1–1.4pp; the leader's honest
value is ~54.6–55.0% and the gap to 60 is ~+5.0 to +5.4pp, not +6.5pp.**

⚠ **This makes the near-term picture slightly BETTER than the record says and changes nothing
about the verdict** — see §5. Flagging the direction because a correction that flatters us needs
more scepticism, not less.

---

## 3. PROBABILITY A NEWLY GENERATED ARM CLEARS (condition A3)

**⛔ A3 IS RIGHT AND I AM STATING THE ANSWER UNDER PROTEST OF ITS OWN PRECISION.** σ is a
distance. Converting +3.6σ (let alone +7.6σ) into a frequency requires a tail shape that
**59 points cannot establish**. Everything in this section is **conditional on the fitted
Gaussian random-effects model** — `θ_i ~ N(μ, τ²)`, `p̂_i | θ_i ~ Binomial(n_i, θ_i)` — and is
**not a fact about the world.** The distribution has a heavy LEFT tail (SEALQ at 25.48, a broken
arm rather than a bad one) and no observed right tail at all; a Gaussian is a convenience there,
not a finding. **Read the ratios as order-of-magnitude, and read the σ-distances as the result.**

Operative thresholds, solved numerically at n=5,400: clearing the **60 bar** requires a measured
**60.00%** (the CI-lo≥58 clause binds at 59.32 and is therefore slack); clearing the **70 bar**
requires **70.00%** (CI-lo≥68 binds at 69.24).

| reference class | bar | P(arm's TRUE value ≥ bar) | P(arm MEASURES ≥ bar, i.e. clears) | ≈ 1 in N arms |
|---|---|---|---|---|
| **all arms** (μ 50.96, τ 2.49) | 60 | 1.4 × 10⁻⁴ | **2.3 × 10⁻⁴** | 4,300 |
| | 70 | 1.1 × 10⁻¹⁴ | **6.3 × 10⁻¹⁴** | 1.6 × 10¹³ |
| **single-plank** (μ 49.13, τ 2.20) | 60 | 3.9 × 10⁻⁷ | **1.1 × 10⁻⁶** | 880,000 |
| | 70 | ~10⁻²⁰ | ~10⁻²⁰ | — |
| **multi-plank** (μ 52.39, τ 2.00) | 60 | 7.1 × 10⁻⁵ | **1.5 × 10⁻⁴** | 6,500 |
| | 70 | ~10⁻²⁰ | ~10⁻²⁰ | — |

**(a) TRULY ≥60 vs (b) MEASURING ≥60 — the distinction the brief asks for, and it is small here.**
P(measures) exceeds P(truly) by only **~1.6× at the 60 bar** (2.3e-4 vs 1.4e-4). **Measurement
luck is not a meaningful route to this bar** at n=5,400, because se = 0.68pp is small next to the
6–9pp the arm must travel. A bar cleared by luck would be a different problem; this is not one.
The audit's independent figure agrees — a true-55.24 arm reads ≥60 with probability 5.8e-13.

⚠ **The one place luck DOES matter is the reverse direction: 50% power at the bar's own value.**
An arm whose true value is exactly 60.00 qualifies with probability **0.50**, and no re-test rule
is registered anywhere. That is a property of the gate, not of the process, and it is not mine to
change.

---

## 4. THE FIVE DISBELIEF CONDITIONS

### A1 — STATIONARITY: **FIRES, and it resolves into A2**

Median split of the 59 arms by last-write timestamp, at **2026-08-15T19:24:54Z**:

```
earlier half  n=29  mean 49.40 %
later   half  n=30  mean 51.75 %
shift               +2.35 pp = +0.55 pooled SD   ->  FIRES (threshold 0.5 SD)
```

**But the shift is COMPOSITION, not improvement.** Decomposed within class:

```
within SINGLE-plank arms:  earlier 49.88 -> later 48.41   =  -1.47 pp
within MULTI-plank arms:   earlier 51.44 -> later 52.04   =  +0.60 pp
composition:  earlier 10/29 = 34 % multi   ->   later 23/30 = 77 % multi
```

⇒ **The line got better at the pooled level by shifting from single planks to conjunctions,
not by getting better at either.** Single-plank arms got *worse* over the window. So the pooled
mean is non-stationary, and the honest response is not to reweight toward recent arms — it is to
report the two classes separately, which §2 does. **The class-conditional distributions are the
stationary objects; the pooled one is a mixture with a moving mixing weight.**

### A2 — CONJUNCTIONS: **the population contains them, they are displaced, and the finding is scoped accordingly**

**Classifier, and it took two attempts.** My first attempt counted how many of the four modules
(`main/raid/eco/doctrine`) an arm touches. **It failed its own validation**: it called
`_v253catapult`, `_v273sentshell`, `_v262bodyblock` MULTI, and all three are documented **solo
pure-raid planks** (`docs/coordination.md:58098`). A raid plank naturally touches three modules.

**The classifier I used instead is structural containment:** an arm is MULTI if the set of lines
it adds/changes against the v140 control **strictly contains** the change-set of at least one
other screened arm. This validates on every documented case:

```
bodyaware   contains 0  -> SINGLE  (documented 1 plank)     ✓
spawnlock   contains 0  -> SINGLE  (documented solo)        ✓
catapult    contains 0  -> SINGLE  (documented solo)        ✓
sentshell   contains 0  -> SINGLE  (documented solo)        ✓
bodyblock   contains 0  -> SINGLE  (documented solo)        ✓
rnd1        contains 0  -> SINGLE                           ✓
awrlnch     contains bodyaware, rnd1        -> MULTI  (documented bodyaware+homeearly)  ✓
awrspawn    contains bodyaware, awrlnch,... -> MULTI  (documented bodyaware+spawnlock)  ✓
trio        contains bodyaware, awrlnch,... -> MULTI  (documented 3-plank)              ✓
mix4        contains trio, mix3, mix2,...   -> MULTI  (documented "four planks")        ✓
catrnd1     contains rnd1                   -> MULTI  (catapult+rnd1)                   ✓
```

**Containment is sufficient but not necessary** — `CMB294`/`CMB295` are named combination arms
whose components were never screened separately, so they contain nothing. I therefore union
containment with the **named combinatorial families** (MIX, CMB, TRIO, AWRLNCH, AWRSPAWN,
RNDSPAWN, CATRND1, SH287/288/289, G4xx). **Sensitivity: containment-only gives SINGLE=27 /
MULTI=32 against SINGLE=26 / MULTI=33; the single-plank mean moves 49.14 → 49.20 and the
σ-distance to 60 moves 4.56 → 4.59.** The classification choice does not carry the result.

**The displacement is large and it is the headline of this section:**

```
SINGLE-plank arms   n=26   mean 49.14  (mu_RE 49.13, tau 2.20)  max 54.23  ->  60 is +4.94 sigma (RE)
MULTI-plank arms    n=33   mean 51.75  (mu_RE 52.39, tau 2.00)  max 55.24  ->  60 is +3.80 sigma (RE)
displacement        +2.61 pp of observed mean   /   +3.26 pp of mu_RE
```

⛔ **CONSEQUENCE FOR WORDING, HONOURED THROUGHOUT THIS DOCUMENT: the strongest form of the
finding is "60 is not reached by SINGLE PLANKS." The general form is weaker** — conjunctions
have moved the mean 2.6pp and every one of the 9 best arms on the board is a conjunction. §4.6
prices how much further that road can go.

### A3 — σ IS A DISTANCE: **honoured**

The result is stated as a distance in §2.1. Every frequency in §3 names the distribution it
rests on and is presented as conditional on it. No claim of "will not happen" appears anywhere.

### A4 — POPULATION SELECTION: **not truncated from below; the truncated variant is shown for contrast**

The rule is in §1 and the excluded set is counted there. Specifically:

* `SEALQ-KILLED` **25.48%** — **IN** (E5 set at n≥100 for exactly this reason).
* `bodyblk-autostop` **47.26%** — **IN** (n=3,574).
* `spawnlkl-autostop` 49.72, `cmb294` 50.68, `cmb295` 48.27, `catsolo` 49.54, `sh286` 48.75 — all **IN**.
* 6 single-plank arms have a 95% CI entirely **below** 50 and all 6 are **IN**.

**What a completed-arms-only filter would have done, measured:** the n≥5,000 cut has n=41,
mean **51.94** (+1.34pp) and SD **2.35** (−1.96pp) against P0. It is exactly the shape A4
predicts — mean up, SD down — and it moves the observed-SD distance to 60 from 2.18σ to 3.43σ.
Both cuts are in the §2.1 table and neither changes the verdict.

### A5 — FIXTURE MISMATCH: **verified per row; §1.3 counts the cost**

Verified per shard from its own `# FIXTURE` header or its registry row, never assumed. **40% of
the corpus is on-fixture; 60% is permanently off it** under the fixed-benchmark ruling.

⚠ **One fixture caveat I owe the reader, and it cuts against ALL of the above:** every number
here is **one control (v140), one local battery, our own maps and our own opponent-of-record.**
`FIXTURE_OF_RECORD` is `live_unrated`. The local screen is what the bar is written against, so
it is the right surface for *this* question — but a distribution measured against a single fixed
opponent says nothing about the ladder, and the head-to-head step (gate 2) is measured on a
different contrast entirely.

### 4.6 DEFF (local exemption, applied correctly)

Local corefill/arena is balanced-by-construction and reads pair-weighted **DEFF = 0.98
(ρ = −0.020)** across 124 shards. **I applied DEFF = 1.0 throughout** — no widening. Applying the
platform constants (1.529 rated / 1.833 unrated) would inflate these intervals 24–35% for
correlation that is not present locally.

**Checked for the outlier case (arms with strong map interaction, ~1.25):** the two Bonferroni-
surviving map×seat cells on record are `CMB290`/glacierkeep/A and `SH288`/drakkarfjord/B
(`coordination.md:60637`). Both arms are in my population. Re-running the leader-vs-bar exclusion
at DEFF = 1.25 widens `MIX280mix4`'s half-width from ±1.33 to ±1.48pp, giving [53.76, 56.72] —
**still excludes 58 and 60.** No conclusion in this document depends on the DEFF choice.

---

## 5. ⭐ MECHANISM: HOW BIG IS A PLANK, AND DO PLANKS COMPOSE?

This is where the useful answer lives, and it is a harder finding than the σ-distance.

### 5.1 The size distribution of single-plank effects

26 single-plank arms, effect measured as (share − 50):

```
 +4.23  _v229dest14b        n=  378   <- CI [49.19,59.19], straddles 50: NOT confirmed
 +4.10  _v242bodyaware      n=16,200  <- CI [53.33,54.87], CONFIRMED
 +1.61  _v259rnd1           n=10,800  <- CI [50.67,52.55], CONFIRMED
 +0.49  _v228dest14a   +0.44 _v234retire60   +0.40 _v225mapsalt   +0.14 _v250homeearly
 -0.06  _v232collarmedic  ... 18 arms straddling 50 ...
 -2.38  _v254collarseal   -2.39 _v238sealfloor6   -2.74 _v262bodyblock
 -2.86  _v226nestshot     -4.46 _v232sealtempo    -8.02 _v200siegelaunch
```

```
mean single-plank effect          -0.86 pp
positive                          7 of 26
95% CI entirely above 50          2 of 26   (bodyaware +4.10, rnd1 +1.61)
95% CI entirely below 50          6 of 26
95% CI straddling 50 (null)      18 of 26
```

⇒ **The base rate of finding a plank worth ≥ +4pp is 1 in 26 screens.** The base rate of finding
any confirmed positive at all is 2 in 26.

### 5.2 Do planks compose? Documented decompositions only

I used only decompositions stated on the record (`coordination.md`, s45 items 2–8) rather than
inferring components from my containment graph — containment finds *any* subset, which produced
a meaningless table on the first pass.

| combination | observed | sum of parts | **obs − sum** | se(obs) |
|---|---|---|---|---|
| AWRLNCH = bodyaware + homeearly | +3.95 | +4.24 | **−0.29** | 0.68 |
| AWRSPAWN = bodyaware + spawnlock | +4.58 | +3.82 | **+0.75** | 0.64 |
| RNDSPAWN = rnd1 + spawnlock | +1.87 | +1.33 | **+0.54** | 0.68 |
| **TRIO = bodyaware + rnd1 + spawnlock** | **+4.35** | **+5.43** | **−1.09** | 0.65 |
| CATRND1 = catapult + rnd1 | +0.96 | +1.15 | **−0.20** | 0.43 |

**At two planks, composition is roughly additive** — the four 2-plank residuals are −0.29, +0.75,
+0.54, −0.20 against se ≈ 0.65, i.e. scattered around zero. **At three planks it turns
sub-additive**: TRIO realises 79.9% of its parts' sum, and its −1.09pp shortfall is 1.7 se.

**And the board-level version of the same statement is much starker.** The additive stock of the
**two confirmed-positive** single planks is **+5.71pp → 55.71%**. The best combination anyone has
built measures **+5.24pp → 55.24%**. Counting all seven *nominally* positive single planks the
naive sum is **+11.42pp → 61.42%**, against +5.24 observed — **a realisation ratio of 0.46**.

⇒ ⭐ **THE CONFIRMED POSITIVE PLANK STOCK IS ESSENTIALLY ALREADY HARVESTED.** The board leader
at 55.24 is within 0.5pp of the additive sum of every plank we have confirmed. **The conjunction
road has not stalled because conjunctions do not work — it has stalled because there is almost
nothing left to conjoin.**

### 5.3 What that implies for the two bars — the arithmetic, stated as arithmetic

Working from the leader's honest value of ~54.8% (§2.3):

```
gap to 60:  +5.2 pp     gap to 70:  +15.2 pp
new bodyaware-sized (+4.10pp) planks needed, IF PERFECTLY ADDITIVE:   60 -> 1.3     70 -> 3.7
                                             at TRIO's 0.80 realisation:  60 -> 1.6     70 -> 4.5
base rate of a >= +4pp plank in this process:                        1 in 26 single-plank screens
=> expected single-plank screens to source them:                      60 -> ~40      70 -> ~120
```

⚠ **And that arithmetic is OPTIMISTIC in a way I want on the record.** It assumes the *next*
+4pp plank composes with `bodyaware` at 80%, when the one 3-plank datum we have already shows
the shortfall growing with plank count, and the four best conjunctions on the board (55.24,
55.20, 55.07, 54.65) are separated by less than their own measurement error — **the board max has
been flat for ~17 arms**. A saturating curve fitted to that would not reach 60 at any plank count.

⇒ **The gap to 70 does NOT decompose into a sum of tuning steps.** +15.2pp is ~3.7 more
discoveries the size of the single best thing this process has ever found, composed at a rate the
board says is falling. **That is a mechanism-level statement, not a sample-size one:** more draws
from the current generator changes the *number* of arms near 52–55, not the *ceiling* near 55.

### 5.4 ⭐ THE SURPRISE, FLAGGED BEFORE IT IS EXPLAINED

**Conjunctions raise μ by +3.26pp but LOWER τ, from 2.20 (single) to 2.00 (multi).** I did not
expect that and it is the opposite of the intuition that combining planks opens up the upside.
On the RE scale the multi-plank class is **3.80σ** from 60 against the single-plank class's
**4.94σ** — an improvement, but far less than the +2.6pp mean shift alone would buy, precisely
because the class is *tighter*.

**Conjunctions move the cloud; they do not fatten its tail.** Written down before explaining it
away, per the standing rule. If it survives re-measurement it is the most important structural
fact on this board, because it says the conjunction road buys a better *typical* arm and not a
better *best* arm — which is the opposite of what a search for one 60-clearing arm needs.

---

## 6. RECONCILIATION WITH `AUDIT-2026-08-16-instruments-vs-decisions.md`

Opened only after the derivation above was complete, per the brief.

| claim | audit | me | agree? |
|---|---|---|---|
| ±2pp clause is slack; gate reduces to point ≥60 | CI-lo≥58 binds at 59.29 | binds at **59.316** | **yes** (0.03pp apart; they used n=5,408, I used 5,400) |
| σ-distance of the 60 bar | **+4.64σ** (27-arm board, mean 53.02, between-arm sd 1.507) | **+3.63σ** all arms / **+3.65σ** completed / **+4.94σ** single-plank (RE) | **differ — see below** |
| arms ever ≥60 | (implicit: none) | **0 of 59** | yes |
| winner's curse | registered +1.7pp overstated ~4.7×; shrinkage gives **0.37pp** | **0.29–0.61pp**; leader honest **54.6–55.0** | **yes, and independently** |
| false qualification by luck | true-55.24 reads ≥60 with p = 5.8e-13 | P(measures) only 1.6× P(true) at the bar | yes, same conclusion |
| board max flat 16.5h / 17 arms | yes | consistent: top four within measurement error | yes |
| corrupted batch | 7 local shards at pri=4, NOWINNER 1.5–8.1% vs 0.00% full-speed | **12 shards excluded at >1% NOWINNER**, 1.14–8.86%, all 05:36–08:13Z | yes (I catch 12 because I count the G4xx partials and the throttled `F232COLLARM` half) |

### Where I differ, and why

**Their population is 27 arms with mean 53.02; mine is 59 with mean 50.60.** A board whose mean
is 53.02 cannot contain siegelaunch (41.98), sealtempo (45.54), bodyblock (47.26), pinrnd1
(47.59), collarseal (47.62) or SEALQ (25.48) in any weight. **Their board looks truncated from
below — precisely condition A4** — most likely a completed-and-scored board rather than every arm
the process emitted. My nearest comparable cut (n≥5,000, 41 arms) reads mean **51.94**, still
1.1pp below theirs.

**Their σ is 1.507pp; my τ is 2.21–2.49pp.** Truncation from below removes the low arms, which
cuts the variance. **The two errors partly cancel**: their higher mean shortens the distance,
their smaller σ lengthens it, net +4.64σ against my +3.63σ.

**Verdict on the 4.64:** ⭐ **I do not reproduce it, and the disagreement is about population and
estimator, not about arithmetic.** My equivalent figures are **3.6σ on the full arm population**
and **4.9σ on single planks only** — 4.64 sits between them, which is what you would expect from
a board that has dropped its worst arms. **On the question actually asked, the difference is
immaterial: 3.6σ and 4.6σ are both "no arm this process has ever produced is in the neighbourhood,
and 0 of 59 have cleared."** I would not bank 4.64 as a number; I would bank the ordering.

**And I explicitly do not endorse their `1 in 560,000`** — that is the frequency conversion A3
warns against, on 27 points, at +4.64σ. My own equivalents (§3) carry the same warning and are
stated as conditional on a fitted Gaussian.

**Separately: `HANDOVER.md`/`coordination.md`'s 53.50 shipping value should be corrected to
~54.8%.** Two independent shrinkage fits (the audit's 0.37pp and my 0.29–0.61pp) say the +1.74
correction over-shoots because it assumes τ=0 on a board with Q=787 on 58 df. **This is a
routing item for the builder, not something I can write.**

---

## 7. THE HONEST FRAMING: IS GRIND A PHASE OR A CEILING?

**GRIND is not a phase we are waiting out. It is the correct steady state of a process whose
output distribution does not overlap the bar.**

The precise statement, scoped as A2 requires:

1. **60 is not reachable by SINGLE PLANKS.** +4.94σ on the RE fit, 0 of 26 arms above 54.23,
   99th percentile of true single-plank value **54.25%**. Drawing more single planks is not a
   route to the slot, and this is the strongest and best-supported claim in the document.
2. **60 is not reachable by the CONJUNCTION process AS CURRENTLY RUN.** +3.80σ, 0 of 33 arms
   above 55.24, 99th percentile of true multi-plank value **57.04%**. The road is *better* than
   single planks and it is **not** open — and §5.4 says why: conjunctions raise the mean without
   widening the tail.
3. **70 is not reachable by anything on this board.** +7.6σ to +8.8σ; the naive additive sum of
   *every* nominally positive plank we have ever found is **61.42%**, and the realised value of
   that stock is 55.24%. **70 is not a longer grind on the current generator; it is a different
   generator.**

### What would have to change — three roads, priced

Magnus set the bars; my job is which road reaches them.

**(A) A BETTER ARM-GENERATING PROCESS.** This is the only road the data endorses for 70. The
generator currently emits arms centred at μ≈51 with τ≈2.2 — it is a **tuning** process (constant
flips and small mechanism variants on a fixed chassis) and it has already found its two winners
in 26 tries. Reaching 70 needs **effects of a size this generator has never produced once**, not
more draws from it. What that means concretely:
* **Fix the seat asymmetry first.** `coordination.md:60604` measures **+6.28pp on byte-identical
  self-play**, z=16.24, n=66,572, localised to `main.py:289`'s spawn-ring hash. **That is larger
  than every plank we have ever shipped, it is our own bug, and it is not on my board because it
  is not an arm.** A bug of that size sitting inside the chassis means the generator's ceiling is
  partly self-imposed. This is the single highest-value item I can see and it is already
  commissioned.
* **Then re-measure, do not bank both.** The (map,seat)-conditional CV lift of +4.96pp is partly
  arm selection routing around that same bug; banking the fix and the conditional lift
  double-counts.
* **Mechanism-level rather than parameter-level candidates.** The exploit class in the standing
  directive — crash-induction, spawn denial, launcher kidnap — is the only family in this repo's
  history that could plausibly produce a step of the size §5.3 requires, because its effect is
  *removing an enemy unit permanently* rather than shifting an economy constant. The current
  generator is not sampling from that space; `dose-homeearly`-style probes show the mechanism
  fires but map-conditionally (162 of 183 throws on one map).

**(B) A DIFFERENT FIXTURE.** The bar is written against v140 on the local screen, and Magnus has
fixed that permanently — correctly, since a moving benchmark makes every experiment unusable.
**But nothing about a 60% share vs v140 is a claim about the ladder**, and the pipeline's step 2
(head-to-head vs the current slot holder) is measured on a contrast that is currently
**UNMEASURED** — the only read is the fixture-broken `V140VS152` shard I excluded under E3
(n=230, 1.71% NOWINNER, 58.26% of decided, ±6.4pp). **If v152 really sits near 58 vs v140, an arm
at exactly 60 is at rough parity with the holder and the head-to-head is the real gate, not the
threshold.** That shard should be re-run clean before anyone prices the pipeline off the 60 alone.
This is the cheapest thing on this list and it is a *measurement* gap, not a strategy change.

**(C) THE BAR.** Not mine, not discussed. Both numbers came from Magnus directly and pricing them
is the whole content of this document.

### What GRIND is actually buying, stated fairly

At the fleet's ~52 full-n arms/day, the process is **not** searching for a 60 — it is mapping the
52–55 region at ever finer resolution. That is not worthless: it is how `bodyaware` and the
conjunction lift were found, and §5.2's base rate (1 in 26) is only knowable because the grind
produced 26 single planks. **But the marginal arm now buys a tighter estimate of a ceiling we can
already state to ±1pp, and the two bars sit 5 and 15pp above it.** ⇒ **The next unit of effort is
worth more spent on the seat-asymmetry fix, on a clean head-to-head read, and on
mechanism-class rather than parameter-class candidates, than on arm number 60.**

---

## 8. REPRODUCTION

Working scripts are in the session scratchpad (not checked in). The derivation is four steps and
each is re-runnable from the primary tapes:

1. Parse every `scratchpad/overnight/*.tsv` and `scratchpad/overnight-remote/*/*.tsv`;
   content-dedup by md5 (249 → 232).
2. Resolve control per shard: `# FIXTURE` header, else `scratchpad/fleet_queue.tsv` /
   `corefill_work.txt` / `vps/**` / `overnight-remote/*/worklist.txt`. Keep
   `control == bots/_v223sealrepair` (93).
3. Apply E1–E5 (§1) → 72 shards; pool by treatment tree → **59 arms**.
4. Wilson intervals per arm; DerSimonian–Laird for μ and τ; EB shrinkage and a 400k-draw
   conditional simulation for the winner's curse; structural containment against the control
   tree for the single/multi split.

**Controls that fired:** header-vs-registry control agreement (0 disagreements, can fire);
9 structural NULL cells all landing 48.6–52.0 with every CI covering 50 (must not reach 60, and
does not); the τ=0 counterfactual reproducing the registered +1.7pp curse and thereby locating
the disagreement in its premise rather than its arithmetic; the first plank classifier being
**rejected** because it failed its own validation against three documented solo planks.
