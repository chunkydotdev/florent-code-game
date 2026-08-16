# MAP-CONDITIONAL CEILING — does picking the best arm per map reach 60%?

**Written 2026-08-16T05:54:54Z (from `date -u`), research arm, repo HEAD `f7638f18`.**
**Data frozen 2026-08-16T05:33:34Z.** Several shards were still writing while this
ran — `CMB299` moved 4,470 → 4,500 games *between two runs of the same script* — so
every number below is computed against a frozen copy of the 44 headered shard tapes,
not the live files. Re-running against live tapes will move the last digit.

---

## THE ANSWER, FIRST

Three selectors, all cross-validated the same way (k=10 on seeds, 23 arms, all vs
`bots/_v223sealrepair`). **The bootstrap interval is the honest one** — it resamples
whole seeds and so carries selection variance, which the analytic interval omits.

| selector | naive oracle | **cross-validated** | analytic 95% @DEFF 0.98 | @DEFF 1.25 | **seed-cluster bootstrap 95%** | draws ≥60% | lift vs zero-interaction null |
|---|---|---|---|---|---|---|---|
| best uniform arm ("ship the board leader") | 55.24% | **53.50%** | — | — | [51.69, 56.77] | 0/200 | — |
| **MAP-conditional** (15 cells) | 60.79% | **57.04%** | [55.78, 58.30] | [55.61, 58.47] | **[54.21, 59.38]** | 2/200 | **+2.60pp**, p = 0.0149 |
| SEAT-conditional (2 cells) | 56.24% | **55.28%** | — | — | [52.15, 57.24] | 0/200 | +0.55pp, **p = 0.3632 (null)** |
| **(MAP, SEAT)-conditional** (30 cells) | 64.08% | **59.19%** | **[57.96, 60.42]** | **[57.80, 60.58]** | **[56.03, 60.93]** | **29/200** | **+4.96pp**, p = 0.0050 |

**OVERFITTING GAP: 3.75pp** for map-only (60.79 → 57.04) and **4.89pp** for
(map, seat) (64.08 → 59.19).

**NULL-SELECTION CONTROL — it came out the other way, exactly as required.** With all
23 arms **simulated identical** (same true per-cell profile, real cell sizes), the CV
estimate collapsed to the truth and the naive oracle did not:

| key set | truth | **CV** | CV bias | naive | **naive bias** |
|---|---|---|---|---|---|
| MAP only | 53.10% | 53.05% | **−0.047pp** | 58.10% | **+5.01pp** |
| SEAT only | 53.10% | 53.15% | **+0.053pp** | 54.94% | **+1.84pp** |
| (MAP, SEAT) | 53.10% | 53.09% | **−0.009pp** | 60.09% | **+6.99pp** |

**The naive read manufactures +5.0 to +7.0pp out of pure noise — most of the distance
from the board (55.24%) to Magnus's bar (60%). The cross-validated read manufactures
under a twentieth of a point.**

### DOES THIS ROUTE REACH 60%?

**MAP-CONDITIONAL ALONE: NO, clearly.** 57.04%, ~3pp short, upper bound 59.4%,
**2 of 200** bootstrap draws reach 60%. Zero of its 15 per-map winners survive a
multiplicity correction.

**(MAP, SEAT)-CONDITIONAL: NOT AT THE POINT ESTIMATE, BUT 60% IS NOT EXCLUDED.**
59.19% — **0.81pp short** — and **both** 95% intervals contain 60 ([57.96, 60.42]
analytic @0.98; [56.03, 60.93] bootstrap). **29 of 200** bootstrap draws (14.5%) reach
60%. This is a genuinely different answer from the map-only one and it is the finding
of this cut.

⛔ **AND THE BAR IS NOT MET EVEN IF THAT NUMBER IS RIGHT, FOR A REASON THE STATISTICS
CANNOT SEE.** Every figure here is *our share of local games against one control,
`_v223sealrepair`*. The cross-validation certifies generalisation **to new games
against that same bot on those same 15 maps** — nothing more. A per-(map, seat) edge
was *selected against v140's specific behaviour*, and there is no evidence it survives
contact with a different opponent. **Magnus's 60% bar is a ladder claim; this is a
one-opponent local number.** Per `CLAUDE.md` point 6, a local battery may prioritise
a road, never close or open one.

⚠ **AND THE SEAT TERM MAY NOT BE OURS TO SELL.** An independent cut the same morning
(`docs/research/SEAT-ASYMMETRY-HUNT-2026-08-16.md`) shows the seat advantage **flips
by map in byte-identical self-play** — 73.15% seat A on glacierkeep, 36.10% on
valkyrie — i.e. it is **our own compass-absolute code**, not the engine. My strongest
cell sits on exactly that map and seat. **Some unknown share of the +4.96pp is arm
selection routing around a bug we could instead fix.** See §10.

**bodyaware "turn the plank off on its bad maps": +0.24pp, not +0.34pp.**
Your estimate was right *for the naive form* (naive +0.33pp: 54.04% vs 53.70%, off on
auroraveil and icefloe). Cross-validated it is **+0.24pp (53.94%)**, and the whole
effect sits inside bodyaware's own ±0.93pp half-width at n=10,800. **The cheap idea is
dead.**

⛔⛔ **CORRECTION 2026-08-16 ~11:2xZ (research lane, on the MDE-convention audit). "DEAD" IS A
FAIL-TO-EXCLUDE REPORTED AS AN EXCLUSION, AND THIS FILE HEDGES A *LARGER* NULL CORRECTLY TWO LINES
LATER.** `+0.24pp` against a `±0.93pp` half-width is the interval **[−0.69, +1.17]**. It **does not
exclude zero** — and, decisively, **it does not exclude +1.0pp either.** ⇒ **A real one-point effect
is fully consistent with this data, so "the cheap idea is dead" is not supported by it.** The
supported sentence is: *"not resolvable at n=10,800; the interval admits everything from −0.7 to
+1.2."*
⭐ **AND THE SIZE MATTERS BEYOND THIS FILE: +1.0pp is EXACTLY the effect `QUEUE #77` is being sized
to detect.** This document declares dead an effect of the size another live row is spending games to
find. **The two cannot both be right, and the interval says which.**
⚠ **The internal inconsistency is the tell and it is in this file's own text: the +0.55pp null two
lines below is hedged correctly. The SMALLER estimate got the STRONGER word** — which is the shape
of a conclusion reached before the interval was consulted, not after. *(Per `CLAUDE.md`'s direction
clause: a fail-to-exclude must be RESTATED AS AN EXCLUSION before it is banked. It was not.)*


---

## 1. THE DATA, AND THE CONTROL-GROUP SPLIT

Tapes: `scratchpad/overnight/*.tsv` and `scratchpad/overnight-remote/*/*.tsv`.
**188 of 232 tape files carry no `# FIXTURE` header** (legacy tapes) and were dropped —
the header is the only in-band record of which control an arm was measured against,
and `scratchpad/corefill_work.txt` is not a substitute (1,190 lines spanning several
control eras).

**Control groups among the 44 headered tapes:**

| control | arms |
|---|---|
| **`bots/_v223sealrepair`** (v140) | **38** ← analysed |
| `bots/_probe_border_raw` | 3 (CRASHP, CRASHS, CRASHZ) |
| `bots/_probe_border_guard` | 1 (CRASHG) |
| `bots/_v146gunaxis` | 1 (NULL5400) |
| `bots/_x3r0v146` | 1 (V140VS146) |

Only the 38-arm `_v223sealrepair` group is analysed; nothing is compared across groups.

**Trim.** `tools/overnight.sh` runs a fixed cycle of 15 maps × 2 seats per seed, so a
seed is either a complete balanced 30-game cycle or a partial one. **Every arm is
truncated to complete seed-cycles**, which makes map balance and seat balance exact
for that arm *and for every split of it*. Without it, a shard stopped mid-cycle
over-weights the alphabetically-early maps.

**Two pools, both reported:**
* **PRIMARY — 23 arms, ≥ 179 complete seeds (≥ 5,370 games, ≥ 358 games/map).**
  Uniform cell sizes; this is the cut quoted above.
* **SENSITIVITY — 33 arms, ≥ 30 complete seeds (≥ 900 games)** — §6. Verdict identical.

Excluded from the primary pool: BODYBLK, CATSOLO, CMB294, CMB295, CMB298, CMB299,
G400g4, G401g5, G402g2, G403g2, G404g3, G405g3, SEALQ, SH286, SPAWNLKL.
`NOWINNER` rows in pool arms: **3**, dropped.

### The predicate, verified non-degenerate

`winner == 'T'` (treatment). **68,990 / 129,930 = 53.10%** over the 23-arm pool. A
broken predicate returns 0.00% or 100.00% — the first pass elsewhere scored
`winner == seat` and got a constant 0.00% across all 15 maps, which is exactly the
failure this line rules out.

**Seat check, and it is not a footnote: seat A 55.56% (n=64,965) vs seat B 50.64%
(n=64,965) — a 4.92pp gap.** Seat A means the treatment is passed to `fcode run`
first. The complete-cycle trim makes seat exactly balanced in every arm and every
split, so it biases nothing — but it is the largest single effect in this dataset and
it is why an unbalanced cut of these tapes measures seat, and why §4 exists.

### The prior reproduces exactly

`BODYAWR` (`bots/_v242bodyaware`, n=10,800): pooled **53.70%**, per-map range
**yulerune 57.50% → auroraveil 45.69%** (11.81pp), **chi² = 37.71, df = 14,
p = 0.000575** — digit-for-digit the figure in the brief.

---

## 2. THE SPLIT RULE, AND WHY IT IS NOT THE GAME INDEX

**⛔ The obvious split is wrong.** The runner emits games as
`for map in MAPS: for seat in (A, B)`, so **`game`-index parity IS seat parity** —
splitting even/odd game puts every seat-A game in one half and every seat-B game in
the other, across a 4.92pp seat effect.

**Split used: seed.** Seeds are consecutive integers, each contributing one complete
balanced cycle, so any partition of seeds preserves map and seat balance exactly.
Verified outcome-independent: **even seeds 52.795% (n=79,500) vs odd seeds 52.676%
(n=79,230)**; per-arm even−odd delta **mean +0.040pp, sd 1.971pp**.

**Estimator: k-fold CV on seeds, k=10, averaged over R ≥ 60 random partitions.**
k=2 selects on 50% of the data and is *pessimistic* about the deployed policy (which
would select on everything); k=10 selects on 90% and estimates that policy directly.
Stable across k for the map-only selector: 56.88% (k=2) · 56.94% (k=4) · 56.94% (k=10).

⚠ **One split is not a result, and the first pass learned this the hard way.** A single
k=2 split returned 53.69% to 56.89% depending only on the split *rule* (seed parity
55.27%, floor(seed/2) parity 56.75%, seed mod 4 56.75%, five mod-5 splits
55.27–56.89%). Everything reported is averaged over ≥ 60 random partitions;
partition-to-partition sd at k=10 is 0.35–0.45pp.

---

## 3. THE NAIVE ORACLE, AND WHY THE BOARD ITSELF IS OVER-READ

Best arm per map on all the data, scored on the same data — **60.79%, using 13
distinct arms**. Per map, against the board leader `MIX280mix4`:

| map | naive best arm | rate (n=360) | `MIX280mix4` | diff | z @DEFF 0.98 |
|---|---|---|---|---|---|
| antler | MIX280mix4 | 65.28% | 65.28% | +0.00pp | +0.00 |
| archipelago | CMB292 | 56.94% | 51.39% | +5.56pp | +1.51 |
| auroraveil | MIX284mix3 | 59.17% | 55.00% | +4.17pp | +1.14 |
| drakkarfjord | MIX285mix2 | 59.72% | 53.89% | +5.83pp | +1.60 |
| drumlin | SH289 | 60.28% | 48.89% | +11.39pp | **+3.12** |
| fjordgate | SH287 | 67.50% | 62.22% | +5.28pp | +1.50 |
| frostgate | MIX282mix5 | 64.72% | 58.33% | +6.39pp | +1.78 |
| glacierkeep | CMB291 | 58.06% | 49.17% | +8.89pp | **+2.43** |
| icefloe | CMB296 | 60.00% | 52.78% | +7.22pp | **+1.98** |
| midgard | MAXSTACK | 57.82% (n=358) | 52.50% | +5.32pp | +1.45 |
| nordkap | CMB296 | 63.06% | 59.44% | +3.61pp | +1.01 |
| ragnarok | BODYAWR | 55.97% (n=720) | 50.83% | +5.14pp | +1.61 |
| royale | MIX281mix4 | 63.89% | 56.67% | +7.22pp | **+2.01** |
| valkyrie | SH287 | 61.39% | 55.56% | +5.83pp | +1.61 |
| yulerune | CMB290 | 58.06% | 56.67% | +1.39pp | +0.38 |

4 of 15 clear |z| > 1.96 uncorrected. The selection ran over **15 × 23 = 345
comparisons**, Bonferroni threshold **|z| > 3.80**. **Zero of the fifteen clear it**
(max 3.12, drumlin). **Every individual per-map specialist in that table is
individually unproven.**

⛔ **AND THE BOARD'S OWN HEADLINE IS THE SAME KIND OF NUMBER.** `MIX280mix4` at 55.24%
is itself the **maximum over 23 arms** of a noisy 5,400-game estimate. Scored the same
honest way — pick the best uniform arm on 90% of seeds, score it on the held-out 10% —
**"ship the board leader" is worth 53.50%, not 55.24%.** The board headline carries
about **1.7pp of winner's curse**, which is not a defect of the map-conditional idea
but a fact about reading a 23-arm leaderboard.

**⇒ The gap to 60% is not +4.8pp. It is +6.5pp.** This also explains the two puzzles
in the brief with no new mechanism: the 55-class leaders differ by 0.17pp because they
are all draws from the top of the same noise distribution, and TRIO fails to beat
bodyaware because it is being compared against an inflated number.

---

## 4. SEAT — THE AXIS THE ORIGINAL HYPOTHESIS DID NOT NAME

Seat is knowable at runtime (`ct.get_team()`, and which core anchor we hold), so it is
as legal a conditioning variable as the map. Three key sets, everything else identical:

```
                    naive     CV k=10   bootstrap 95%      >=60%    paired lift (p)
MAP only  (15)      60.79%    57.04%    [54.21, 59.38]     2/200    +2.60pp (0.0149)
SEAT only ( 2)      56.24%    55.28%    [52.15, 57.24]     0/200    +0.55pp (0.3632)  <- NULL
MAP x SEAT (30)     64.08%    59.19%    [56.03, 60.93]    29/200    +4.96pp (0.0050)
```

**Seat alone is a null** (+0.55pp, p=0.36) and map alone is worth +2.60pp — **yet the
two together are worth +4.96pp, which is more than their sum.** That is a genuine
three-way arm × map × seat structure, and it has a mechanism: the maps are symmetric
by reflection or rotation, but **our bots are not** — direction iteration order,
first-choice build tiles and approach headings are all hardcoded, so the same arm on
the mirrored anchor of the same map is running a genuinely different plan.

**The per-arm seat split confirms real arm × seat variation:** mean A−B **+4.82pp**,
sd across the 23 arms **2.04pp**, range **+7.67pp (SH288) to −0.07pp (CMB296)**. The
per-arm 95% half-width on that difference is ±2.64pp, so the between-arm sd net of
measurement noise is ≈ **1.5pp** — real, but modest on its own, which is why the
seat-only selector reads null.

**The (map, seat) cells that carry it are the two largest in the whole study, and they
are the only cells in this document that survive multiplicity correction:**

| cell | arm | rate (n=180) | `MIX280mix4` | diff | z |
|---|---|---|---|---|---|
| **glacierkeep, seat A** | **CMB290** | **82.78%** | 61.67% | **+21.11pp** | **+4.65** |
| **drakkarfjord, seat B** | **SH288** | **65.00%** | 42.78% | **+22.22pp** | **+4.38** |
| fjordgate, seat B | MIX283mix5 | 66.11% | 51.11% | +15.00pp | +2.95 |
| drumlin, seat B | MIX282mix5 | 60.00% | 45.00% | +15.00pp | +2.91 |
| midgard, seat B | AWRLNCH | 53.63% | 39.44% | +14.19pp | +2.75 |
| archipelago, seat B | MIX285mix2 | 70.56% | 58.33% | +12.22pp | +2.47 |

12 of 30 cells clear |z| > 1.96 uncorrected. Bonferroni over **30 × 23 = 690**
comparisons needs **|z| > 3.97** — and **2 of 30 clear it**: `CMB290` on
glacierkeep/A (+21.11pp) and `SH288` on drakkarfjord/B (+22.22pp). **Those two cells
are the only individually-established map-conditional effects in this entire
dataset,** and they are the obvious targets for a confirmation leg.

---

## 5. THE CONTROLS — ALL FOUR, AND WHAT EACH RETURNED

### 5a. NULL-SELECTION, parametric: all arms simulated IDENTICAL

Every arm given the **same** true per-cell probability vector (the pool's own cell main
effect), with the **real** cell sizes. Any per-cell difference is noise by
construction, so the selection must buy nothing. Results in the table at the top:
**CV bias −0.047pp / +0.053pp / −0.009pp** for the three key sets; **naive bias
+5.01pp / +1.84pp / +6.99pp**. **The pipeline collapses to roughly the pooled mean, as
required, and the naive procedure does not.**

### 5b. NULL-SELECTION, real outcomes: zero-interaction additive bootstrap, PAIRED

Each arm keeps its measured strength and each cell keeps its measured difficulty;
**only the interaction is set to zero**. The same fold partition is applied to observed
and null so split noise cancels — this matters, because split noise is ±0.4pp and it is
what made the first pass ambiguous.

```
MAP only   (B=200): obs 56.97%  null 54.38%  LIFT +2.60pp (sd 1.13pp)    2/200 <=0  p=0.0149
SEAT only  (B=200): obs 55.29%  null 54.74%  LIFT +0.55pp (sd 1.29pp)   72/200 <=0  p=0.3632
MAP x SEAT (B=200): obs 59.24%  null 54.28%  LIFT +4.96pp (sd 1.10pp)    0/200 <=0  p=0.0050
```

Each null's CV sits at the honest best-uniform-arm value (~53.5–54.7%) — **under zero
interaction the per-cell selector buys nothing, as it must.**

### 5c. NULL-SELECTION, nonparametric: known-equivalent pseudo-arms

`BODYAWR` (n=10,800, one bot) carved by seed into k pseudo-arms — all truly identical.
*(This table is the k=2 repeated-split estimator; the k=10 estimator gives the same
picture at +0.83 / +0.46 / +2.11pp. Which k is used moves the residual by well under a
point and moves the naive bias not at all.)*

| k | games each | naive | naive bias | CV | CV bias |
|---|---|---|---|---|---|
| 5 | 2,160 (144/map) | 58.75% | **+5.05pp** | 53.93% | +0.23pp |
| 15 | 720 (48/map) | 66.25% | **+12.55pp** | 54.05% | +0.35pp |
| 33 | 300 (20/map) | 75.91% | **+22.21pp** | 54.47% | +0.77pp |

The residual CV bias here is *not* estimator bias — 5a proves that at ±0.05pp. It is
the shared-data noise of carving one tape into k pieces (at k=33 each eval cell is a
handful of games). This is the nonparametric sanity check; **5a is the control that
answers the question.**

### 5d. POSITIVE CONTROL — the test can come out the other way

A **known** per-cell advantage injected into the zero-interaction null (one designated
arm per cell), same paired statistic re-run.

| injected | MAP only | SEAT only | (MAP, SEAT) |
|---|---|---|---|
| +0.0pp | +0.20pp (se 0.25) | — | — |
| +2.0pp | +0.16pp | — | — |
| +4.0pp | +0.88pp | — | — |
| +6.0pp | **+2.88pp** | **+5.80pp** | **+2.10pp** |
| +10.0pp | +7.41pp | — | — |

*(The +6pp row is one run of all three key sets; the other MAP-only rows come from a
separate run of the same procedure — an independent repetition put MAP-only's +6pp
recovery at +3.18pp rather than +2.88pp, which is the scale of rep-to-rep noise here.)*

Zero injection returns zero; real effects are recovered. **Recovery is conservative and
gets worse as cells get smaller** — the 30-cell selector recovers only +2.10pp of an
injected +6pp because each cell holds half the games. ⚠ **Do not invert this into "the
true (map, seat) effect must therefore be ~+15pp":** the control injects the boost onto
a *randomly chosen* arm, usually a weak one that selection then has to find among 23,
whereas the real effects sit on already-strong arms and are far easier to find. The
control establishes **direction and non-degeneracy**, not a calibration curve.

---

## 6. SENSITIVITY — the 33-arm pool

Adding the nine small arms (down to 1,050 games) changes nothing material:

| | 23 arms | 33 arms |
|---|---|---|
| MAP only — naive / CV | 60.79% / 57.04% | 61.95% / 57.10% |
| MAP only — bootstrap 95% | [54.21, 59.38] | [53.05, 60.05] |
| MAP only — draws ≥60% | 2/200 | 4/120 |
| MAP only — paired lift | +2.60pp (p=0.0149) | +3.46pp (p=0.0083) |
| (MAP, SEAT) — naive / CV | 64.08% / 59.19% | 65.32% / 58.18% |
| (MAP, SEAT) — bootstrap 95% | [56.03, 60.93] | [54.01, 60.33] |
| (MAP, SEAT) — draws ≥60% | 29/200 | 5/120 |
| (MAP, SEAT) — paired lift | +4.96pp (p=0.0050) | +5.09pp (p=0.0083) |
| best-uniform-arm CV | 53.42–53.50% | 53.45–53.49% |
| identical-arm null, CV bias | −0.05 to −0.01pp | +0.10 / −0.17pp |

The small arms inflate the *naive* oracle (their noisier cells win more maxima:
overfitting gap 4.89pp → 7.14pp on the 30-cell selector) and leave the honest estimate
alone — itself a demonstration that the CV is doing its job.

---

## 7. WHAT A CONDITIONAL BOT WOULD ACTUALLY COST

**How many arms?** The shortlist is re-chosen inside every training fold, so these are
honest:

| arms in shortlist | MAP-conditional CV | (MAP, SEAT) CV |
|---|---|---|
| 1 (= ship the board leader) | 53.53% | 53.40% |
| 2 | 54.74% | 55.18% |
| 3 | 55.15% | 55.45% |
| 5 | 55.04% | 55.43% |
| 6 | 55.41% | 56.06% |
| 8 | 56.44% | 57.39% |
| 10 | — | 58.30% |
| 12 | 55.78% | 58.70% |
| 16 | — | 58.99% |
| **23 (all)** | **56.94%** | **59.27%** |

⛔ **The value only arrives with the whole library.** A three-arm switch — the
plausible engineering scope — is worth **55.15% / 55.45%**, i.e. it does not even
reach the naive 55.24% the board already claims. **Ten to sixteen arms are needed
before (map, seat) conditioning clears 58%.** Shipping that means one zip carrying
10–16 behavioural variants plus a dispatch table, inside the 10 ms/unit/turn budget.

**How stable are the picks?** Across random partitions a fold-set selects **19.0
distinct arms on average** (map-only), and a fold's pick agrees with the full-data pick
on only **74.3% of map slots**. **One slot in four would change with more data** — the
same instability the Bonferroni line reports, seen from the deployment side.

**Regularising does not rescue it.** Falling back to the globally-best arm unless a
cell arm beats it by > δ (k=10, 23 arms, map-only): δ=0.00 → 57.16%, 0.02 → 57.02%,
0.04 → 56.01%, 0.06 → 54.61%, 0.12 → 53.99%, 0.20 → 53.50%. The unregularised
selector is already the best of these; there is no δ that finds a smaller, more
trustworthy override set worth more.

### Can the tree read the map at runtime? YES — this is not the blocker

`bots/_v223sealrepair/eco.py:55` `known_map_for(w, h, own, ct)` keys `MAP_CODES` /
`EXTRA_MAP_CODES` on `(w, h, ax, ay, bx, by)` and returns the decoded terrain grid.
Checked against `maps/*.map26` for all 15 battery maps:

* **All 15 have a matching entry and none is stale** — every stored code decodes
  byte-for-byte to the current map file, so `known_map_for` never returns `None` on
  the current battery. *(This was a live risk: a prior session found map-keyed
  constants can go stale across ships. They have not here.)*
* **10 are uniquely named from the dimension key alone**: antler, auroraveil,
  drakkarfjord, drumlin, fjordgate, glacierkeep, icefloe, nordkap, royale, valkyrie.
* **5 are ambiguous by key but resolvable from sensed terrain** (candidate grids differ
  in 110–294 of 400–676 cells): the two documented collision pairs midgard/ragnarok and
  frostgate/yulerune, plus **an UNDOCUMENTED third collision — `archipelago` shares key
  `(26,26,5,5,19,19)` with `snowflake`**, which is not in the battery but still occupies
  an `EXTRA_MAP_CODES` slot and forces archipelago through the terrain-sensing path. It
  works today; the code's own commentary does not mention it. **Worth a comment fix
  regardless of what happens to this road.**
* Seat is trivially readable (`ct.get_team()` / own core anchor).

**⇒ Implementability is not what stops this. Effect size, arm count and opponent
generalisation are.**

---

## 8. STANDARDS AND CAVEATS

* **DEFF.** Local batteries are balanced-by-construction and read DEFF 0.98
  (`CLAUDE.md`, s39 audit). Because this analysis is *entirely about map interaction*,
  every analytic interval is also quoted at the **1.25** outlier constant. It changes
  no verdict: (map, seat) goes [57.96, 60.42] → [57.80, 60.58], both containing 60;
  map-only goes [55.78, 58.30] → [55.61, 58.47], neither containing 60.
  **Platform constants (1.529 / 1.833) are NOT used** — these are local games.
* **The bootstrap interval takes NO DEFF, deliberately.** It resamples whole seeds,
  i.e. it resamples the clusters themselves, so the correlation is already in the
  interval. Multiplying it by a design effect would count the same thing twice.
* **The analytic interval understates.** It treats eval cells as independent binomials
  and **omits selection variance**. The bootstrap is ~2× wider and is the one the 60%
  question should be read against.
* **Numbers carry subjects.** Every rate is *our treatment arm's share of local games
  against `bots/_v223sealrepair`*, on the 15-map battery under `--tle 10`, 23 arms,
  129,930 games. Not a ladder win rate, not a game-share against the field, and not
  against any live opponent.
* **Design-effect enumeration, per the standing procedure.** Clusters in this data:
  **MATCH** — does not exist locally (one row is one game; there are no 5-game
  matches). **OPPONENT** — a single fixed control, so the cluster is degenerate and
  absorbed rather than inflating. **SEED** — live, and handled *structurally*: the
  split, the fold assignment and the bootstrap all operate on whole seeds, never on
  games.
* **Exclusion vs fail-to-exclude.** The map-only "does not reach 60%" is stated as an
  **exclusion** (the interval excludes 60), so widening it makes the claim harder —
  the correct direction, and it survives at DEFF 1.25 and on the bootstrap. The
  (map, seat) verdict is deliberately **not** stated as an exclusion, because it is
  not one: 60 is inside both intervals. The **+4.96pp lift** claim excludes zero at
  p=0.0050 (0/200 null draws) and is the robust part; the **magnitude** of the point
  estimate is the fragile part.
* **⭐ IMMUNE TO THE CONTROL-TREE DRIFT, and it is worth stating.** The control tree was
  edited twice on 2026-08-15 while shards were writing (`tools/control_pin.py` exists
  because of it), so arms measured at different times faced slightly different
  controls. **That contaminates arm MAIN effects — the per-arm table — but it cannot
  manufacture arm × cell interaction**, because selection and evaluation here are both
  *within* an arm, and all 15 maps × 2 seats cycle inside every seed, so a control
  change at time T shifts all 30 cells of that arm equally. **The interaction findings
  survive the drift; the per-arm ranking is the part to distrust.**

---

## 9. WHAT THIS CLOSES AND WHAT IT OPENS

**DEPRIORITISED** (local evidence only; per `CLAUDE.md` point 6 a road is retired only
on live-game evidence):

1. **MAP-conditional arm selection is not a route to 60%.** 57.04%, ~3pp short,
   2/200 bootstrap draws reach 60%, 0 of 15 per-map winners survive multiplicity
   correction, and it needs the entire 23-arm library to get there.
2. **The bodyaware plank-off oracle is dead.** +0.24pp cross-validated (+0.33pp naive),
   inside its own ±0.93pp half-width. Your +0.34pp estimate was correct for the naive
   form; the honest form is smaller.
3. **Seat-conditioning alone is a null.** +0.55pp, p = 0.3632.

**OPENED, and this is the more useful half:**

4. **⭐ (MAP, SEAT) is the live candidate.** 59.19% cross-validated, lift +4.96pp over
   a zero-interaction null at p = 0.0050, 60% not excluded by either interval. It is
   the only cut here that gets within a point of the bar. **It needs 10–16 arms to
   deliver, only 2 of its 30 cells are individually established, and none of it has
   been tested against a second opponent.**
5. **⭐⭐ TWO CELLS ARE INDIVIDUALLY ESTABLISHED AND ARE THE CHEAPEST NEXT STEP:**
   **`CMB290` (`bots/_v290c3`) on glacierkeep seat A — 82.78% vs the board leader's
   61.67%, +21.11pp, z = +4.65** and **`SH288` (`bots/_v288sh2`) on drakkarfjord seat B
   — 65.00% vs 42.78%, +22.22pp, z = +4.38**. Both survive Bonferroni over all 690
   comparisons. A dedicated confirmation shard on those two cells is a small, targeted
   spend that would either hand us a real mechanism to generalise or kill the road
   properly.
6. **The board is over-read by ~1.7pp, so the gap Magnus's rule has to close is +6.5pp,
   not +4.8pp.** Any plank graded by "did it top the board" is being graded on a
   statistic paying ~1.7pp of pure selection bias.
7. **A 60% arm still has to come from a plank that does not exist yet.** Every honest
   estimator here — best uniform arm 53.5%, map-conditional 57.0%, (map, seat)
   59.2% — says the current library tops out below the bar unless the (map, seat)
   route both holds up and generalises past v140. **Stacking, mixing, and now
   switching among these planks have all been measured and all land in the 53–59
   band.**

---

## 10. CROSS-REFERENCE — A PARALLEL CUT SUPPLIES THE MECHANISM

`docs/research/SEAT-ASYMMETRY-HUNT-2026-08-16.md` (research arm, same morning,
written independently of this file and off a different fixture — nine byte-identical
self-play shards) lands on the same axis and **explains why the seat term is real**:

* The favoured seat **flips by map** — seat A wins **73.15% on glacierkeep** and
  **36.10% on valkyrie** in byte-identical self-play, a 37.06pp spread with only ~4%
  of the between-map variance attributable to sampling. **That rules out an engine
  turn-order property and indicts our own absolute-coordinate logic.**
* The named top site is `bots/_v223sealrepair/eco.py:868`
  (`side = 1 if (self.idx & 1) else -1`), whose parity is **seat-locked** — measured
  240/240 on entity-id parity — so seat A's builders run a clockwise-first pathfinder
  and seat B's a counter-clockwise-first one, permanently.

**This corroborates §4 from the other side and it also constrains what §9.4 is worth.**
The strongest cell I find is `CMB290` on **glacierkeep seat A at 82.78%** — and that
is the exact map/seat where byte-identical self-play already reads 73.15%. **So an
unknown share of the +4.96pp (map, seat) lift is our own compass bias being
side-stepped by arm selection rather than a strategic map specialisation.**

⇒ **The two roads are alternatives, not complements, and the other one is cheaper.**
That cut prices a global symmetry fix at **+1.48pp** and a per-map one at **+3.19pp**
(their stated **upper bounds**, and it records that two such fixes have already been
built and fired and delivered none of it). A code fix that removes the handedness
would be one change to one tree; the route priced in this document is a 10–16-arm
dispatch table. **If the symmetry fix lands, much of what the (map, seat) selector is
being paid for disappears — which is an argument for sequencing the fix first and
re-measuring this ceiling afterwards, not for building the switch.**

---

## APPENDIX — REPRODUCTION

Analysis scripts live in this session's scratchpad and run read-only against a frozen
snapshot; nothing in the repo was modified except this document.

```
mapcond2.py   loader, complete-cycle trim, 2-fold CV, nulls 1a/1b/2, per-arm and
              per-map tables, bodyaware plank-off oracle
mapcond3.py   k-fold CV (k=2,4,10), PAIRED null test, positive control
mapcond4.py   seed-cluster bootstrap CI, simulated-identical-arm null, shortlist facts
mapcond5.py   shortlist-size sweep, per-map z vs the board leader
mapcond6.py   key-set comparison: MAP only vs SEAT only vs (MAP, SEAT), full controls
mapcond7.py   (map, seat) shortlist sweep and per-cell z
ci.py         analytic DEFF intervals, bodyaware chi-square p-value
```

Env: `SNAP=<frozen tape dir>`, `MIN_SEEDS=179` (primary) or `30` (sensitivity),
`RSPLIT` / `NBOOT` / `NBOOT_CI` = repetition counts. Run under `.venv/bin/python`.

---

## ⛔⛔ ADDENDUM, SAME DAY ~11:0xZ — **THIS EXACT CONSTRUCT HAS ALREADY BEEN SHIPPED ON OUR OWN ACCOUNT AND REVERTED. THE FIELD DATUM THIS DOC SAYS IT CANNOT SUPPLY NOW EXISTS.**

**This doc's own limit reads: *"CV certifies new GAMES vs v140, not new OPPONENTS."* That limit is
no longer hypothetical — a teammate ran the experiment in production and the result is against us.**

**`bots/_x3r0v145/base_router.py:125-136`, read from staged source, verbatim:**
```python
pair  = tuple(sorted(((core.x, core.y), (enemy.x, enemy.y))))
label = SIGNATURES.get((w, h, pair))                                   # identify the MAP
if label is None:
    label = COLLISION_GRIDS.get(map_eco.known_map_for(w, h, core, ct))
side  = "A" if label and (core.x, core.y) == A_CORES[label] else "B"   # identify the SIDE
salt  = OPENINGS.get(label, {}).get(side, "92")                        # pick the OPENING
self.inner = ROUTERS[salt]()
```
⇒ **A `(map, side)` → opening → sub-bot router. That is this document's §"adding SEAT to the key",
built and shipped, arrived at independently from the other end.** `v146` documents its variant as
*"Official-map mixture of experts: v135 generally, v134 on preregistered weak maps"*, selected from a
**504-game tournament against three replay-derived opponent surrogates**, held out at **354/420 =
84.29%** — i.e. **it validated LOCALLY at least as convincingly as this doc's CV 59.19%.**

**THEN IT MET THE LADDER** (`ladder_games.ourver`, rated):
```
v145  ROUTER, 106 files    1/5    20.0%
v146  ROUTER,  85 files    7/20   35.0%
v147                       3/10   30.0%
   pooled routers         11/35   31.4%  [12.4, 50.4]
v152  SINGLE BOT         100/180  55.6%  [46.6, 64.6]
```
**Single bot beats the pooled routers by +24.2pp ± 21.0pp.** ⚠ **NOT ESTABLISHED — 5–20 games per
router version, bands of ±20–40pp, and this is the same small-n trap this repo names constantly.
What is unambiguous is the REVERSION: they abandoned a 110,000-line construct and went back to a
5,518-line single bot.**

⭐ **AND THE SIZE OF THAT CONSTRUCT IS THE OTHER WARNING THIS DOC SHOULD CARRY.** The routers are
**874 lines of 110,184 (v145) and 609 of 87,463 (v146) — 0.8% and 0.7%.** Everything else is a
FULL PREFIXED COPY of the base tree per variant. **This doc's caveat "it needs 10–16 arms" is, in
implementation terms, 10–16 duplicated trees plus a dispatcher** — and their twenty sub-bots were in
fact **two base variants across seven map-groups** (`p07h` vs `p22h` differ by **8 lines**).

### ⇒ WHAT THIS CHANGES ABOUT THIS DOC'S CONCLUSION
* **The measurement stands.** CV 59.19% [56.03, 60.93] vs v140 on the local fixture is unaffected;
  the null-selection control still fired, the overfitting gap is still 3.75pp.
* **The INFERENCE from it does not.** The one external test of this construct available anywhere —
  same account, same ladder, real opponents — reads **31.4%**.
* **Order of work is unchanged and now doubly supported: fix the seat asymmetry first.** It is a bug
  fix worth ~1.5–3pp for free, it does not require N duplicated trees, and part of the conditional
  lift was routing around it in the first place.
* ⚠ **The honest reading is NOT "map/side conditioning is refuted".** It is: **a local
  cross-validated 59.19% and a local held-out 84.29% BOTH failed to survive contact with the
  ladder** — which is a statement about how much any local validation of a SELECTION scheme is
  worth, and it applies to this document's own headline number first.
