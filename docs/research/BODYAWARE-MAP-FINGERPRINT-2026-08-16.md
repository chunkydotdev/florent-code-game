# ⛔ THE `bodyaware` MAP FINGERPRINT IS **NOT EXPLAINED** BY ANY MAP PROPERTY WE CAN MEASURE — AND THE CONTROL PROVES THE METHOD CANNOT TELL

**Research arm, 2026-08-16T05:26Z.** Zero games fired; everything below is off
disk. Fixture read: `scratchpad/overnight/BODYAWR.tsv`
(header `treatment=bots/_v242bodyaware control=bots/_v223sealrepair
planned_n=10800 start=2026-08-15T00:03:28Z runner=tools/overnight.sh`,
mtime `2026-08-15T11:42:05Z`, last row `2026-08-15T09:42:05Z` — the shard is
**complete**, 10,800 data rows, not a live tape).

---

## 0. THE THREE ANSWERS, UP FRONT

1. **DOES ANY MAP PROPERTY EXPLAIN THE SPREAD? NO.** **26 properties tested,
   ZERO have a 95% CI excluding zero.** The best is `ore_frac` at
   **r = −0.472, 95% CI [−0.793, +0.053]** — it does not clear.
2. **HOW MANY PROPERTIES, AND THE MULTIPLICITY:** **k = 26**. Chance of at least
   one spurious hit at p<0.05 under a pure null is
   **1 − 0.95²⁶ = 0.736** — we would expect ~1.3 false positives and **we got
   zero**. A permutation null on `max|r|` over all 26 properties puts the
   observed maximum at **P = 0.608** — i.e. **the best correlation we found is
   WEAKER than the median best correlation that pure noise produces** (null
   median `max|r|` = 0.507 vs observed 0.472).
3. **WHAT THE CONTROL DID — AND THIS IS THE FINDING THAT GOVERNS THE WHOLE
   DOCUMENT: ⛔ THE NEGATIVE CONTROL FIRED.** The **alphabetical index of the map
   name** — a property that cannot possibly relate to a pathfinding change —
   correlates at **r = +0.525, 95% CI [+0.018, +0.817], which EXCLUDES ZERO**.
   **It outranks all 26 real properties.** A meaningless label beat every piece
   of real geometry on this dataset.

4. **⭐ AND THE ONE THING THAT *IS* RESOLVED — A BLIND PREDICTION WAS
   REFUTED (§7B).** A subagent given **only the two source trees**, forbidden all
   results, predicted from the code that the effect is driven by **local bot
   density** and would therefore be **largest on small maps and null on the
   30×30s**. Measured: **30×30 group 55.67% vs area ≤ 400 group 52.78%,
   difference +2.89 pp, 95% CI [+0.76, +5.02] — the OPPOSITE SIGN, interval
   excluding zero.** The congestion story the plank was built on is the one
   hypothesis here that is actually **dead**.

> ### ⭐ THE VERDICT
> **The 11.8pp spread is REAL (chi² = 37.7143, df = 14, p = 0.000575, reproduced
> below) but it is NOT explained by map size, shape, wall density, ore density,
> core separation, path length, detour, chokepoint structure, or symmetry
> class.** At n = 15 maps this analysis **cannot distinguish a true predictor
> from a nonsense one**, and the alphabetical control is the proof. **No story is
> offered here because the data does not support one — except the one that was
> pre-specified and came out backwards (§7B).**
>
> **The fingerprint remains UNEXPLAINED. `bodyaware` still ships on its 53.70%,
> which §6 confirms is unbiased — we simply do not know why it works.**

---

## 1. REPRODUCTION AND THE PREDICATE CONTROL (do this before trusting any cell)

**The predicate matters and a degenerate one is invisible.** `winner` is
**`T`/`C`** (treatment/control), *not* a seat letter; `seat` is `A`/`B`
separately.

| predicate | returns | status |
|---|---:|---|
| `winner == 'T'` (**used**) | **5800 / 10800 = 53.7037%** | matches the briefed pooled figure exactly |
| `winner == seat` (the known trap) | **0 / 10800 = 0.00%** | **degenerate — reproduced deliberately to show the failure is visible** |

Column values as read: `winner ∈ {T:5800, C:5000}`, `seat ∈ {A:5400, B:5400}`,
`cond ∈ {core_destroyed:10112, tiebreak:688}`, 15 maps × 720 games, and all 30
`(map, seat)` cells hold **exactly 360** games — **balanced by construction**.

### Per-map win share — reproduces the briefed table to the digit

Per-cell 95% half-width at n = 720 is **±3.65pp**.

| map | share % | 95% CI | z vs pooled | |
|---|---:|---|---:|---|
| yulerune | 57.50 | [53.89, 61.11] | +2.04 | nominal only |
| valkyrie | 56.67 | [53.05, 60.29] | +1.59 | |
| drakkarfjord | 56.11 | [52.49, 59.74] | +1.30 | |
| ragnarok | 55.97 | [52.35, 59.60] | +1.22 | |
| frostgate | 55.28 | [51.65, 58.91] | +0.85 | |
| glacierkeep | 55.00 | [51.37, 58.63] | +0.70 | |
| midgard | 54.58 | [50.95, 58.22] | +0.47 | |
| royale | 54.58 | [50.95, 58.22] | +0.47 | |
| antler | 54.03 | [50.39, 57.67] | +0.17 | |
| nordkap | 53.89 | [50.25, 57.53] | +0.10 | |
| fjordgate | 53.06 | [49.41, 56.70] | −0.35 | |
| drumlin | 52.22 | [48.57, 55.87] | −0.80 | |
| archipelago | 51.67 | [48.02, 55.32] | −1.10 | |
| icefloe | 49.31 | [45.65, 52.96] | −2.37 | nominal only |
| **auroraveil** | **45.69** | [42.06, 49.33] | **−4.31** | **survives Bonferroni k=15** |

**chi² = 37.7143, df = 14, p = 0.000575.** Under a pessimistic DEFF 1.25:
chi² = 30.171, **p = 0.00723**. Both reproduce the briefed values.
*(Per the standing rule, local balanced-by-construction fixtures read
pair-weighted DEFF = 0.98, so the naive figure is the correct primary and the
1.25 line is a stress test, not the headline.)*

---

## 2. WHERE THE MAP PROPERTIES CAME FROM — and the parser's positive control

Properties are computed from the **actual map files** `maps/*.map26`, not
inferred from replays. The parser is `tools/map_encode.py::parse_map26`, and it
carries its own validation which I **ran rather than assumed**:

```
[ok] fjordgate: key (10,10,2,2,6,6), code REPRODUCED byte-for-byte
[ok] antler / drumlin / nordkap / archipelago: REPRODUCED byte-for-byte
[ok] corrupted fjordgate does NOT match (the control can fail)
SELFTEST PASS
```

⇒ the env-int mapping, packing order, row order and core keys are all confirmed
against hand-verified entries, **and the corruption negative fires**, so an
"[ok]" here is not vacuous.

This is strictly better than the `corpus/events.tsv` route suggested in the
brief (`mw`/`mh` and core-separation from `DEATH` rows): the map files give
**exact** wall/ore layout and **exact** core coordinates with no replay-coverage
gap, so `events.tsv` was not needed and the corpus-coverage caveats do not apply.

---

## 3. THE FULL PROPERTY TABLE — k = 26, none clears

Pearson r against per-map treatment share, Fisher-z 95% CI, n = 15.
Spearman shown as a monotone cross-check.

| # | property | Pearson r | 95% CI | Spearman | CI excludes 0? |
|---|---|---:|---|---:|---|
| 1 | `ore_frac` | −0.472 | [−0.793, +0.053] | −0.648 | no |
| 2 | `openness` (mean passable orth. neighbours) | +0.417 | [−0.121, +0.766] | +0.399 | no |
| 3 | `npass` (passable tile count) | +0.401 | [−0.139, +0.758] | +0.456 | no |
| 4 | `area` | +0.362 | [−0.185, +0.737] | +0.401 | no |
| 5 | `wall_frac` | −0.348 | [−0.730, +0.200] | −0.404 | no |
| 6 | `passable_frac` | +0.348 | [−0.200, +0.730] | +0.404 | no |
| 7 | `h` | +0.335 | [−0.214, +0.723] | +0.414 | no |
| 8 | `maxdim` | +0.335 | [−0.214, +0.723] | +0.414 | no |
| 9 | `diag` | +0.325 | [−0.225, +0.718] | +0.401 | no |
| 10 | `mean_layer` (mean BFS frontier width) | +0.318 | [−0.232, +0.714] | +0.272 | no |
| 11 | `w` | +0.307 | [−0.244, +0.708] | +0.421 | no |
| 12 | `D2` (core separation²) | +0.272 | [−0.279, +0.688] | +0.279 | no |
| 13 | `path_len` (BFS core-surface to core-surface) | +0.228 | [−0.322, +0.663] | +0.282 | no |
| 14 | `D` (core separation) | +0.223 | [−0.327, +0.660] | +0.279 | no |
| 15 | `ore_dist_mean` | +0.204 | [−0.344, +0.649] | +0.236 | no |
| 16 | `detour` (`path_len` / free-space path) | +0.201 | [−0.347, +0.647] | +0.127 | no |
| 17 | `path_free` (free-space path length) | +0.164 | [−0.380, +0.624] | +0.085 | no |
| 18 | `sym_rot180` | +0.142 | [−0.399, +0.610] | +0.033 | no |
| 19 | `ore` (count) | −0.135 | [−0.606, +0.405] | −0.217 | no |
| 20 | `ore_dist_norm` | −0.132 | [−0.604, +0.408] | −0.048 | no |
| 21 | `bottleneck` (min BFS frontier width) | +0.100 | [−0.434, +0.583] | +0.021 | no |
| 22 | `choke_frac` (frac. passable tiles with ≤2 nbrs) | −0.053 | [−0.551, +0.472] | +0.009 | no |
| 23 | `sym_mirror` | −0.036 | [−0.538, +0.485] | +0.046 | no |
| 24 | `aspect` (max/min dim) | +0.034 | [−0.487, +0.537] | −0.139 | no |
| 25 | `D2_over_area` | +0.019 | [−0.498, +0.526] | +0.100 | no |
| 26 | `D_over_diag` | +0.002 | [−0.511, +0.514] | +0.100 | no |
| — | **CONTROL: `alphabetical index`** | **+0.525** | **[+0.018, +0.817]** | — | **⛔ YES — the control fires** |

### The underlying geometry (so the table can be audited)

| map | w×h | area | wall_frac | ore | openness | D | path_len | detour | sym |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| yulerune | 20×20 | 400 | 0.070 | 14 | 3.570 | 14.00 | 25 | 2.273 | rot180 |
| valkyrie | 30×30 | 900 | 0.069 | 16 | 3.618 | 24.00 | 23 | 1.095 | mirror |
| drakkarfjord | 30×30 | 900 | 0.082 | 16 | 3.661 | 31.24 | 40 | 1.000 | rot180 |
| ragnarok | 30×30 | 900 | 0.109 | 26 | 3.496 | 33.94 | 44 | 1.000 | rot180 |
| frostgate | 20×20 | 400 | 0.150 | 20 | 3.682 | 14.00 | 11 | 1.000 | mirror |
| glacierkeep | 30×30 | 900 | 0.076 | 24 | 3.721 | 24.00 | 21 | 1.000 | both |
| midgard | 30×30 | 900 | 0.073 | 16 | 3.664 | 33.94 | 44 | 1.000 | rot180 |
| royale | 20×20 | 400 | 0.110 | 16 | 3.573 | 14.00 | 19 | 1.727 | both |
| antler | 14×18 | 252 | 0.071 | 12 | 3.521 | 8.00 | 5 | 1.000 | mirror |
| nordkap | 20×26 | 520 | 0.142 | 22 | 3.543 | 12.00 | 9 | 1.000 | mirror |
| fjordgate | 10×10 | 100 | 0.100 | 6 | 3.289 | 5.66 | 4 | 1.000 | rot180 |
| drumlin | 25×25 | 625 | 0.006 | 30 | 3.820 | 18.38 | 22 | 1.000 | rot180 |
| archipelago | 26×26 | 676 | 0.308 | 38 | 3.359 | 19.80 | 26 | 1.083 | rot180 |
| icefloe | 20×20 | 400 | 0.085 | 20 | 3.552 | 21.26 | 26 | 1.000 | rot180 |
| auroraveil | 20×20 | 400 | 0.175 | 16 | 3.370 | 16.00 | 17 | 1.308 | mirror |

⚠ **`detour` is near-degenerate**: 11 of 15 maps are exactly 1.000. It has
almost no discriminating power and its r should not be read as a measurement of
anything.

---

## 4. THE CONTROLS, IN FULL — one of them fired, and that is the point

**Standing rule: a check that has never produced the other verdict has not been
seen to check.** Three controls were run, chosen so that each *can* fail.

### 4.1 NEGATIVE CONTROL — ⛔ **FIRED (this is a real result, not a pass)**

| control | r | 95% CI | verdict |
|---|---:|---|---|
| **alphabetical index of map name** | **+0.525** | **[+0.018, +0.817]** | **NON-NULL — control FAILED** |
| map-name character length | −0.066 | [−0.559, +0.462] | null (as expected) |

The alphabetical index is a property of the *filename*. It cannot influence a
pathfinding change. It nonetheless produces a correlation that **excludes zero**
and is **stronger than all 26 real properties**. Mechanically it is an accident:
`auroraveil` (the worst cell) sorts 3rd and `valkyrie`/`yulerune` (two of the
best) sort 14th and 15th.

⇒ **Any "significant" single correlation on this dataset would have been
indistinguishable from this artefact.** Had a real property come in at
r ≈ 0.5, reporting it as a mechanism would have been an error of exactly this
shape.

### 4.2 POSITIVE CONTROL — the instrument is not stuck on "null"

A synthetic property constructed as `share + N(0, 0.5pp)` returns
**r = +0.993, CI [+0.978, +0.998]** — non-null. ⇒ the correlation machinery
**does** detect a real relationship of this size at n = 15 when one exists. The
nulls in §3 are not an always-null instrument.

### 4.3 PERMUTATION NULL on `max|r|` — calibrates the whole 26-property sweep

20,000 shuffles of the 15 win shares against the fixed property matrix:

```
observed max|r| over 26 properties = 0.472
permutation null: median max|r| = 0.507 , 95th pct = 0.727
P(max|r| >= observed | no relationship) = 0.608
```

⇒ **the best result from a 26-property sweep is at the 39th percentile of pure
noise.** This is the cleanest single statement in the document.

---

## 5. THE NOISE CEILING — how much signal was ever available

| quantity | value |
|---|---:|
| observed between-map variance | 8.682 pp² (sd **2.95 pp**) |
| binomial sampling variance at n = 720 | 3.472 pp² (sd 1.86 pp) |
| implied **true** between-map variance | 5.210 pp² (sd **2.28 pp**) |
| signal fraction of observed variance | **0.600** |
| **max attainable \|r\| against a perfect predictor** | **0.775** |

⇒ **40% of the observed 11.8pp spread is sampling noise.** Even a property that
*perfectly* captured the true map effect would top out near r = 0.78 here. This
does not rescue any result in §3 — but it means a modest true relationship
(r_true ≈ 0.4–0.5) would have been **undetectable** at this n, so §3 is
**"not detected"**, not **"proven absent"**. See LIMITS.

---

## 6. ⭐ THE SURPRISE — WRITTEN DOWN BEFORE EXPLAINING IT AWAY

The commissioned question was about maps. **The dominant structure in this
fixture is not the map — it is `seat` × `map`, and it is ~4× larger.**

| map | sym | T% @ seat A | T% @ seat B | seat-A advantage | z |
|---|---|---:|---:|---:|---:|
| **glacierkeep** | both | **78.61** | **31.39** | **+47.22 pp** | **14.47** |
| fjordgate | rot180 | 66.67 | 39.44 | +27.22 | 7.61 |
| icefloe | rot180 | 60.56 | 38.06 | +22.50 | 6.20 |
| royale | both | 43.61 | 65.56 | −21.94 | −6.06 |
| archipelago | rot180 | 41.94 | 61.39 | −19.44 | −5.32 |
| antler | mirror | 61.11 | 46.94 | +14.17 | 3.85 |
| midgard | rot180 | 61.67 | 47.50 | +14.17 | 3.86 |
| drumlin | rot180 | 59.17 | 45.28 | +13.89 | 3.77 |
| nordkap | mirror | 60.28 | 47.50 | +12.78 | 3.47 |
| drakkarfjord | rot180 | 51.39 | 60.83 | −9.44 | −2.56 |
| ragnarok | rot180 | 60.28 | 51.67 | +8.61 | 2.34 |
| auroraveil | mirror | 49.72 | 41.67 | +8.06 | 2.18 |
| valkyrie | mirror | 53.06 | 60.28 | −7.22 | −1.96 |
| yulerune | rot180 | 56.94 | 58.06 | −1.11 | −0.30 |
| frostgate | mirror | 55.83 | 54.72 | +1.11 | 0.30 |

**9 of 15 maps have a Bonferroni-surviving seat asymmetry.** Mean |seat bias| =
**15.3 pp**, max **47.2 pp** — against a total map spread of **11.8 pp**.
SD across the 30 `(map, seat)` cells is **9.91 pp** vs **2.95 pp** across maps.

**AND THE MAPS ARE PROVABLY SYMMETRIC**, so the map cannot be the cause. Checked
directly on the tile grids and the core coordinates:

```
glacierkeep 30x30 coreA=(14,2) coreB=(14,26) | tiles rot180+mirH+mirV all True | cores map onto each other
royale      20x20 coreA=(9,16) coreB=(9,2)   | tiles rot180+mirH+mirV all True | cores map onto each other
```

`glacierkeep` is **exactly symmetric under a vertical mirror in both terrain and
core placement**, and still hands seat A a **47pp** edge. **A perfectly symmetric
map cannot produce a seat advantage; therefore this asymmetry is in OUR CODE**
(the natural suspect being a fixed compass tie-break order — `CARDINALS` and the
`order` list in the very step-chooser this plank edits — which resolves ties the
same absolute direction regardless of which end you start from).

**THIS DIRECTLY ANSWERS AN EXPLICITLY OPEN QUESTION.**
`docs/research/SEAT-AND-MAP-ASYMMETRY-2026-08-11.md` §3R-d leaves the cause of
the local seat effect **OPEN** and asks, verbatim, *"does the self-play seat
asymmetry track the map at all?"* — **Yes, and enormously**: from −21.94pp to
+47.22pp across the 15-map pool. That doc's battery ran the **old 8-map pool**
(`antler atoll drumlin fjordgate heart hive meander nordkap`) and its pooled
figure was 54.13% (an 8.26pp seat edge); the per-map magnitudes on the **current
15-map pool** are new here and are up to 5.7× that.

**TWO THINGS THIS DOES *NOT* MEAN — stated so the finding is not over-read:**
1. **The 53.70% headline is NOT biased.** The design is seat-balanced at exactly
   360 games per `(map, seat)` cell, which cancels the seat advantage in the
   marginal. This is consistent with §2 of the 2026-08-11 doc. **No verdict gets
   repriced.**
2. **This design CANNOT separate the treatment's seat bias from the control's.**
   With only two bots in a zero-sum pairing, `T%@A − T%@B` is algebraically a
   single number per map that both bots share. Separating them requires **T-vs-T
   and C-vs-C mirror games**, which this shard does not contain.

**And it does not explain the fingerprint either:** `|seat bias|` vs treatment
share is **r = −0.145, CI [−0.612, +0.397] — null.** It is a *separate and
larger* phenomenon, not the answer to the commissioned question.

---

## 7. LIMITS — read these before quoting anything above

1. **n = 15. This is the binding constraint.** Every CI in §3 is wide enough to
   contain both "no effect" and "a substantial effect". **Nothing here proves a
   property is irrelevant; it proves we could not detect it.**
2. **The negative control fired.** At this n the method demonstrably produces
   CI-excluding-zero results from meaningless inputs. **This is the strongest
   caveat in the document and it applies to any future single-property claim on
   these 15 cells**, including any made by another lane.
3. **40% of the observed spread is sampling noise** (§5); max attainable |r| is
   **0.775**. A true r of ~0.45 would be missed roughly half the time.
4. **Only MONOTONE relationships were tested.** Pearson and Spearman are both
   blind to a **peaked** relationship — and §8 argues from the code that the
   expected relationship *is* peaked (benefit requires bodies to block *and* an
   alternative route to exist; both extremes give zero). **A non-monotone true
   effect would appear in this table as r ≈ 0.** No quadratic was fitted, because
   adding curvature to 15 points after seeing 26 nulls is exactly the overfitting
   the commission warned against; it is instead pre-registered as the next cut
   (§9).
5. **No multi-predictor regression was run**, deliberately. With n = 15 and
   k = 26 candidates any multivariate fit is unidentifiable.
6. **Properties are correlated with each other** (`area`/`w`/`h`/`diag`/`npass`
   are near-collinear), so the 26 tests are **not** 26 independent looks — the
   0.736 family-wise figure is an upper bound, and the permutation null in §4.3
   is the honest calibration because it preserves the property correlation
   structure.
7. **`detour` is near-degenerate** (11/15 identical) and `sym_*` are binary with
   few distinct levels — low-variance predictors whose r is unstable.
8. **Feature-set boundary.** These are *global* geometry summaries. **Ore
   layout topology, per-tile wall arrangement, spawn-adjacent local geometry and
   corridor structure near each core are NOT captured** by any of the 26. The
   null in §0 is a null **about this feature set**, and §6 shows the data has
   large structure living at exactly the level this feature set averages over.
9. **One fixture, one control bot, local only.** Per the standing rule this is a
   LOCAL balanced fixture (pair-weighted DEFF 0.98), so intervals are naive-correct
   here — but **none of this has live-game backing** and under
   *"a refutation without live-game backing is a hypothesis"* this document
   **closes no road**.
10. **§7B refutes a DIRECTION, not the plank.** The falsified claim is *"the
    benefit comes from crowding on small maps"*. It does **not** say `bodyaware`
    fails to work, and it does **not** identify what replaces the story. Under
    limit 9 it is also local-only, so per the standing rule it **prioritises**
    away from the density road without **retiring** it.
11. **The 30×30 result is itself unexplained and should not become the new
    story.** "Bigger maps do better" is a *description* of §7B's contrast, not a
    mechanism, and `area` alone still does not clear in §3 (r = +0.362, CI spans
    zero). Do not let a refuted prediction get quietly replaced by its mirror
    image.

---

## 7B. ⭐⭐ THE ONE PRE-SPECIFIED TEST — A **BLIND** PREDICTION FROM THE CODE, AND IT CAME OUT **BACKWARDS**

**This is the most informative result in the document**, because unlike §3 it is
not a fishing expedition: it is a single directional claim, fixed in advance.

**Provenance, which is what gives it its weight:** a subagent was given *only*
the two source trees and instructed to predict which map properties should make
the plank matter more or less, **explicitly forbidden from reading
`scratchpad/`, `docs/research/`, or any results**. Its prediction was returned
before any correlation in §3 was shown to it.

**ITS RANK-1 PREDICTION, verbatim in substance:** the trigger is bodies inside a
**fixed** vision disc (r²=20), so the governing quantity is **local bot density =
bots / free tiles**. With `LOKI_MAX_BUILDERS = 11` per side, it computed a ~14×
occupancy spread and concluded:

> *"Composite ranking of maps where I expect the largest positive delta: 12×8 >
> fjordgate/10×10 > 21×8 > 11×16 > moonrise, 12×12, 16×12. **Smallest / null: all
> four 30×30s, the 24×24s, drumlin, hive, meander.**"*

⇒ **Predicted: effect DECREASING in map area.** Measured:

| group (pre-specified by the blind prediction) | maps | share | |
|---|---|---:|---|
| **30×30 — predicted SMALLEST/NULL** | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | **55.67%** (2004/3600) | |
| **area ≤ 400 — predicted LARGEST** | antler, auroraveil, fjordgate, frostgate, icefloe, royale, yulerune | **52.78%** (2660/5040) | |
| **difference (big − small)** | | **+2.89 pp** | **95% CI [+0.76, +5.02], z = 2.66** |

**The sign is inverted and the interval excludes zero.** The five 30×30 maps —
predicted to be the null cells — rank **2, 3, 4, 6, 7 of 15**. `fjordgate`
(10×10, the smallest map in the pool, the only cell below the `area ≤ 220`
threshold, and the one map appearing in the prediction's *top* list) lands at
**53.06%, rank 11 of 15**. The `area` correlation in §3 agrees in sign
(**r = +0.362**, i.e. *bigger* is better).

> **⇒ THE BOT-DENSITY / CONGESTION STORY — the most natural reading of the code,
> and the one the plank was built on — IS THE ONE THING HERE THAT IS ACTUALLY
> REFUTED.** Whatever `bodyaware` is doing, it is **not** paying off through
> "small crowded maps have more collisions".

⚠ **Two honest caveats.** (a) The 900-vs-≤400 threshold is mine; the prediction
named map shapes, not a cutoff, and the three mid-area maps (nordkap 520,
drumlin 625, archipelago 676) sit at 53.89 / 52.22 / 51.67 — i.e. *also* below
the 30×30 group, so the contrast is not knife-edge, but the exact number depends
on the split. (b) This is one test, but it was read **after** the 26 in §3; its
protection comes from the prediction being fixed beforehand, not from being
first.

### 7C. A HAZARD THAT WOULD HAVE INVALIDATED EVERYTHING — checked and CLEARED

The same blind read flagged (its Rank 7) that `_bfs_direction` returns early when
`self.map_grid is None`, and `map_grid` is only populated by `known_map_for` on
an **exact `(w, h, ax, ay, bx, by)` match** against `MAP_CODES` /
`EXTRA_MAP_CODES`. **On an unlisted map the treatment is byte-identical to the
control**, so any missing map would be a structurally-null cell diluting the
whole fingerprint — and this pool was rotated on 2026-08-13, when
`tools/map_encode.py`'s own docstring records that **none of the 10 new maps had
entries**.

Verified directly against `bots/_v242bodyaware/doctrine.py`:

```
all 15 fixture maps: in_table=True, exact_code_match=True  (byte-for-byte)
MISSING/INERT maps: NONE -- the plank is live on all 15
treatment table == control table?  MAP_CODES: True   EXTRA_MAP_CODES: True
```

⇒ **No cell is inert, and the lookup tables are identical between the two arms**,
so the tables are not themselves a confound. The heterogeneity in §1 is a real
difference in *behaviour*, not a mix of live and dead cells.

---

## 8. HYPOTHESIS — ⚠ **NOT MEASURED.** What the code diff suggests

> **EVERYTHING IN THIS SECTION IS CONJECTURE FROM READING THE SOURCE.** It is
> separated from §§1–7 because none of it is tested here. Do not cite it as a
> finding. **Note that §7B has already refuted the most obvious such
> conjecture**, which is the standing reason to distrust this section.

**`eco.py` is the ONLY source file that differs** (`diff -rq` over the two
directories: `main.py`, `raid.py`, `doctrine.py` are byte-identical; the rest is
`__pycache__`). The change is confined to one BFS step-chooser
(`bots/_v242bodyaware/eco.py`, the block tagged `# BODYAWARE (#63)` around
lines 813–905).

**The mechanism, precisely:**
* A `bodies` set is built from `get_nearby_entities` — every `BUILDER_BOT`,
  **both teams**, **within this unit's vision only** (r²=20). It is *local*
  avoidance, not global.
* The whole goal-selection + BFS is wrapped in `for _pass in (0, 1)`.
  **Pass 0** searches with `blk = blocked | bodies`; **pass 1** retries with
  `blk = blocked` (body-free). Pass 1 is skipped entirely when `bodies` is empty,
  so **with no bots in vision the treatment is byte-equivalent to the control**.
* Fallthrough on both `not goals` and BFS exhaustion is `continue` → retry
  body-free; final fallback is the control's `p.cardinal_direction_to(target)`.

**WHAT THIS PREDICTS, AND WHY THE MEASURED NULL IS CONSISTENT WITH IT:**

1. **The effect should be PEAKED in openness, not monotone.** On a **1-wide
   corridor**, a blocking body makes pass 0 find nothing, pass 1 reproduces the
   control exactly ⇒ **effect ≈ 0**. On a **wide-open field**, bodies almost
   never block the desired step ⇒ **effect ≈ 0**. The gain lives at
   **intermediate** openness where a detour exists *and* is needed. **A peaked
   relationship reads as r ≈ 0 in §3** — which is what `openness` (+0.417),
   `choke_frac` (−0.053) and `bottleneck` (+0.100) all did.
2. **The right density variable is BOTS PER UNIT CORRIDOR, not map area.** The
   trigger is bots-in-vision, and vision is a **fixed** r²=20 disc. So the
   governing quantity is **local bot density inside a fixed-radius disc**, which
   global `area`/`wall_frac` do not measure at all — a plausible reason every
   global property came back null.
3. **A candidate cost, which may be what `auroraveil` is.** Two BFS passes double
   worst-case work under the same `steps % 64` CPU guard, and pass 0 can burn the
   budget before pass 1 ever runs — degrading to raw
   `cardinal_direction_to`, i.e. **worse than the control**. Separately, body
   avoidance is computed against **this round's** positions while bots move, so a
   detour can be chosen around a body that has already left.
   **Weakly consistent with the data:** `auroraveil` is the **only** map where the
   treatment kills markedly *slower* (median turns **T 199 vs C 159, +40**),
   and it sits at 2nd-lowest `passable_frac` (0.825) and 3rd-lowest `openness`.
   ⛔ **But this is NOT evidence:** across the 15 maps, median-turn-delta vs win
   share is r = −0.626 **only with `auroraveil` included**, and collapses to
   **r = −0.254, CI [−0.691, +0.320] (null) when it is dropped**. The
   relationship *is* `auroraveil`; it is a restatement of the outlier, not an
   explanation of it. **Pooled kill round is non-regressed: median T 214 vs
   C 216 (−2).**

---

## 9. WHAT WOULD ACTUALLY TEST THIS — the next cut, pre-registered in form

The fingerprint is not in global map geometry, so **stop regressing on map
summaries**. Three cuts, in value order:

1. **⭐ MEASURE THE DOSE, DON'T CORRELATE THE MAP.** The plank's trigger is
   observable: **how often does pass 0 differ from pass 1?** Instrument a local
   arena build to count, per game, (a) rounds where `bodies` was non-empty,
   (b) rounds where pass 0 returned a *different* direction than pass 1 would
   have, (c) rounds where pass 0 failed and fell through. **Regress the per-map
   win share on the per-map DOSE (b), not on geometry.** A plank whose dose is
   near-zero on `auroraveil` and high on `yulerune` explains the fingerprint
   directly; a flat dose refutes the whole mechanism story. ⛔ Note the standing
   rule that `print()` is stripped from platform replays — **this must be a LOCAL
   counter**, not a replay read.
2. **PRE-REGISTER THE PEAKED FORM — but note the linear density story is already
   dead (§7B).** A monotone "more crowding ⇒ more benefit" reading is refuted
   with the wrong sign. What survives is the *peaked* form of §8.1 (zero benefit
   at both extremes), which is **not** ruled out by §7B and which no test here
   could have seen. The honest test is a **pre-registered** single-predictor
   quadratic in measured local bot density, with the sign of the curvature
   **and** the location of the peak stated in advance. Written down *before*
   fitting, that is one test, not a 27th look. **If cut 1 shows the dose itself
   is flat across maps, skip this — the mechanism is elsewhere.**
3. **SPLIT THE SEAT CONFOUND (independent value, §6).** Run T-vs-T and C-vs-C
   mirror shards on `glacierkeep` (the 47pp cell). That separates the two bots'
   seat biases, which this design algebraically cannot, and **a compass-order
   tie-break that hands one seat 47pp is a far larger lever than the 3.7pp plank
   this document was commissioned to explain.**

**And the meta-rule this exercise earned:** with 15 cells, **run the nonsense
property first**. If it clears, the sweep cannot answer the question, and that is
worth knowing before 26 correlations get written down.
