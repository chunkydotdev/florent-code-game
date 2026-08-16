# ⭐⭐ THE HURT SEAT **FLIPS BY MAP** — SO IT IS OUR CODE, NOT THE ENGINE — AND THE INVARIANT IS **COMPASS-ABSOLUTE, NOT SEAT-ABSOLUTE**

**Research arm, 2026-08-16T05:49Z** (`date -u`, same shell; repo head `37fa53c6`
2026-08-16T07:48:38+02:00). **Zero games fired.** Everything below is off disk:
nine byte-identical local shards, the incumbent source tree, and the map files.

---

## 0. THE FIVE ANSWERS, UP FRONT

1. **CONSISTENT OR MAP-DEPENDENT? ⭐ MAP-DEPENDENT, AND IT FLIPS.** On the
   current 15-map pool, byte-identical self-play runs from **seat A 73.15% on
   `glacierkeep`** to **36.10% on `valkyrie`** — a **37.06 pp spread**, 7 maps
   Bonferroni-favouring seat A and **2 Bonferroni-favouring seat B**. Only
   **4%** of the between-map variance is sampling noise (observed 263.6 pp²,
   binomial 10.9 pp², **true sd 15.9 pp**). ⇒ **it is our map-keyed /
   absolute-coordinate logic, not an engine turn-order property.**
2. **POOLED NULL SEAT GAP:** **seat A 52.96%, gap +5.92 pp, n = 13,402**
   (95% CI on the share [52.11, 53.81], z = +6.86) on the **current 15-map pool**
   measured only in the shards that ran that pool. Over **all nine identity
   shards and all 19 maps, n = 35,034: seat A 53.31%, gap +6.62 pp, z = +12.39.**
3. **⭐ THE SHARPER STATEMENT, AND IT IS THE ONE THAT INDICTS THE CODE: the
   favoured pole is a COMPASS DIRECTION, not a seat.** On the five maps whose
   cores are separated **north–south**, the **NORTHERN core wins 58.39%**
   (n = 4,468, z = +11.22). On the five **east–west** maps the **EASTERN core**
   wins 51.90% (z = +2.54). `NS-ness of the core axis` vs the seat gap reads
   **r = +0.583, permutation P = 0.019 (20,000 shuffles)** — and the nonsense
   control that FIRED on the `bodyaware` fingerprint (alphabetical index) reads
   **r = −0.216 here, i.e. it does NOT fire.** **North and East are the first two
   entries of `CARDINALS` and `DIRECTIONS`.** *(HYPOTHESIS — see §7 limits.)*
4. **⭐⭐ TOP CODE SITE — and it is not the one the queue names:**
   **`bots/_v223sealrepair/eco.py:868`**, `side = 1 if (self.idx & 1) else -1`,
   which sets the **handedness of the BFS neighbour expansion** — i.e. which way
   a builder rounds an obstacle — from `self.idx = ct.get_id() & 0xFF`
   (`main.py:312`). **MEASURED on 120 replays / 240 team-instances: the engine
   issues entity ids globally in creation order and the parity is SEAT-LOCKED —
   builder #1 matches its team's parity 240/240 (100.0%), builder #2 240/240
   (100.0%), core id 1 = team 0 and id 2 = team 1 in 120/120.** ⇒ **seat A's
   opening builders run a clockwise-first pathfinder and seat B's run a
   counter-clockwise-first pathfinder, in every game, permanently, under every
   move of every builder of every round.** Runners-up: **`main.py:289`** (the
   spawn-candidate ring sorted on an absolute-coordinate hash — the one component
   MEASURED to carry gap, §4) and **`eco.py:97-104` `nearest_cardinal`**, which
   is **non-equivariant under 180° rotation** (2 of 8 directions violate) and
   governs **every trunk conveyor's facing**.
5. **UPPER BOUND OF A SYMMETRIC FIX:** a single global fix that raised the worse
   seat to the better seat's standard is worth **+1.48 pp** win share
   (≈ +10.3 Elo). A **per-map** fix that also captured the sign flips is worth
   **+3.19 pp** (noise-shrunk; +3.22 pp raw). **These are UPPER BOUNDS, not
   forecasts** — §6 states why, and §4 records that the two fixes we have
   actually built and fired **did not deliver any of it.**

> ### ⛔ THE RESULT THAT SHOULD CHANGE THE NEXT LEG
> **`QUEUE #8`'s declared fixture HAS been run — on 2026-08-11, as `SR1NULL` /
> `SR2NULL` against the contemporaneous `SRNULL0` — and the mean per-map |seat
> gap| did not move: 10.02 pp → 9.02 pp → 9.06 pp.** The row says the
> both-sides-seat-relative null "has never been run". It has. **Canonicalising
> `CARDINALS` alone is measured NOT to be the driver** (its share reads
> **−3.00 pp, 95% CI [−6.86, +0.86]** — consistent with zero and *nominally the
> wrong sign*). The one partition component that clears its own pre-registered
> 3.9 pp bar is the **SPAWN SORT: +4.84 pp, 95% CI [+0.98, +8.70], z = 2.46** —
> site #2 in §3. **Rewrite `main.py:289` and `eco.py:868`, not `doctrine.py:26`.**

---

## 1. THE INSTRUMENT — nine byte-identical shards, and the predicate driven to its known failure

`winner` is **`T`/`C`** (treatment/control), **not** a seat letter; `seat` is the
seat the **treatment** occupied (`tools/overnight.sh:138-140` — `ORD == A` runs
`fcode run $TREAT $CTRL`, `ORD == B` runs `$FC run $CTRL $TREAT`). Therefore

```
A-win  iff  (seat == 'A' and winner == 'T') or (seat == 'B' and winner == 'C')
```

**PREDICATE CONTROL, run because the brief names the trap:**

| predicate | returns | status |
|---|---:|---|
| `winner == seat` (the trap) | **0 / 45,850 = 0.0000%** | **degenerate — reproduced deliberately** |
| the predicate above (**used**) | 24,398 / 45,850 = **53.2126%** | **non-degenerate** |

### The nine cells, and why each one is an identity cell

Every arm pair below was verified **byte-identical on all four source files by
md5** (`main.py`, `eco.py`, `raid.py`, `doctrine.py`). The repo's convention is a
**renamed** copy, because `tools/overnight.sh:68-77` refuses identical basenames.

| shard | arms | scan order | maps | n |
|---|---|---|---:|---:|
| `NULL114` | `_v146null` = `_v146gunaxis` | ABSOLUTE | old 8 | 5,408 |
| `NULL5400` | `_v146null` = `_v146gunaxis` | ABSOLUTE | **current 15** | 5,400 |
| `NULL123` | `_v196null187` = `_v187saltidle_f` | ABSOLUTE | **current 15** | 2,602 |
| `NULL125` | `_v198null125` = `_v197mapcode` | ABSOLUTE | **current 15** | 5,400 |
| `NULLSALT` | `_v195nullcell` = `_v178salt` | ABSOLUTE | old 8 | 5,408 |
| `SHIPGATENULL` | `_v169null` = `_v169launchlate160` | ABSOLUTE | old 8 | 5,408 |
| `SRNULL0` | `_v148null` = `_v148ferryfirst` | ABSOLUTE | old 8 | 5,408 |
| `SR1NULL` | `_v151seatrel` = `_v151null` | **SEAT-RELATIVE (CARDINALS)** | old 8 | 5,408 |
| `SR2NULL` | `_v152seatrel2` = `_v152null` | **SEAT-RELATIVE (CARDINALS + spawn sort)** | old 8 | 5,408 |

*(`SR1NULL`/`SR2NULL` are byte-identical copies of the **fixed** bot — confirmed
against `docs/prereg/PREREG-loki29-seat-relative-scan-2026-08-11.md:309-310`,
which specifies them as "`_v151seatrel` vs byte-identical copy". The on-disk
byte-identity is intentional, not tree rot. `scratchpad/loki29_spec.txt` names
the arms; `SRNULL0` is the contemporaneous untreated null added by the side lane
so the partition is measured in one harness state.)*

**⚠ The incumbent `bots/_v223sealrepair` carries NO seat canonicalisation**
(`grep -c SEAT_RELATIVE_SCAN` = 0; `orient_cardinals` = 0 call sites). The
seven ABSOLUTE shards are therefore the right population for "what the shipping
bot does".

### CONTROLS THAT MUST COME OUT FLAT — all four did

| control | result | verdict |
|---|---|---|
| games per seat (balanced by construction) | A = 17,517, B = 17,517, **delta 0** | **FLAT ✅** |
| unbalanced `(map, seat)` cells | **0 of 38** | **FLAT ✅** |
| treatment share in identity cells (must be ~50%) | 17,576 / 35,034 = **50.168%** | **FLAT ✅** |
| median game length by treatment-seat label | A = 232, B = 232 | **FLAT ✅** |
| tiebreak games by treatment-seat label | 2,130 / 2,171, z = −0.63 | **FLAT ✅** |

**And a control that CAN fire and did not:** splitting every `(shard, map)` cell
into two halves **by seed** gives **χ² = 71.6 on df = 62, ratio 1.15** — i.e.
inside a cell the fixture is essentially binomial. This is the control that makes
§3 mean something, and it is reported before §3 uses it.

**Standing rule applied:** local balanced-by-construction fixtures read
**pair-weighted DEFF = 0.98**, so the naive intervals above are the correct
primary and no platform constant is imported.

---

## 2. THE SEAT GAP, POOLED AND PER MAP

### 2.1 Pooled

| cut | n | seat-A share | gap (A−B) | z |
|---|---:|---:|---:|---:|
| all 19 maps, 7 ABSOLUTE shards | 35,034 | 53.31% ± 0.52 | **+6.62 pp** | +12.39 |
| **current 15-map pool, shards that ran it** | **13,402** | **52.96% ± 0.85** | **+5.92 pp** | **+6.86** |
| current 15-map pool, any shard | 24,218 | 55.00% | +10.01 pp | +15.58 |
| the 4 RETIRED maps only (`atoll heart hive meander`) | 10,816 | 49.52% | −0.96 pp | −1.00 |

⛔ **Do not quote the 55.00% row.** It pools shards that ran the old 8-map set,
so `antler`/`drumlin`/`fjordgate`/`nordkap` (all A-favouring) carry 7 shards each
while the other 11 maps carry 3 — the map mix, not the bot, produces the extra
3 pp. **The 13,402-game row is the map-balanced estimate and is the headline.**

### 2.2 ⭐ PER MAP — THE HURT SEAT FLIPS

Current 15-map pool, `NULL5400 + NULL123 + NULL125`, n = 894 per map (892 on
three). Bonferroni k = 15 ⇒ |z| > 2.128.

| map | n | seat-A % | gap | z | favours |
|---|---:|---:|---:|---:|---|
| **glacierkeep** | 894 | **73.15** | **+46.31** | **+13.85** | **A** |
| nordkap | 894 | 58.50 | +17.00 | +5.08 | A |
| fjordgate | 894 | 57.72 | +15.44 | +4.62 | A |
| midgard | 894 | 57.27 | +14.54 | +4.35 | A |
| auroraveil | 894 | 56.71 | +13.42 | +4.01 | A |
| drumlin | 894 | 55.82 | +11.63 | +3.48 | A |
| antler | 894 | 54.03 | +8.05 | +2.41 | A |
| drakkarfjord | 894 | 53.47 | +6.94 | +2.07 | – |
| frostgate | 894 | 52.13 | +4.25 | +1.27 | – |
| icefloe | 894 | 51.23 | +2.46 | +0.74 | – |
| royale | 892 | 50.45 | +0.90 | +0.27 | – |
| ragnarok | 892 | 49.55 | −0.90 | −0.27 | – |
| yulerune | 892 | 47.53 | −4.93 | −1.47 | – |
| **archipelago** | 894 | **40.72** | **−18.57** | **−5.55** | **B** |
| **valkyrie** | 892 | **36.10** | **−27.80** | **−8.30** | **B** |

* **7 maps favour seat A, 2 favour seat B, 6 not significant.**
* heterogeneity about the pooled mean **χ² = 354.5 on df = 14**.
* mean |gap| **12.88 pp**; spread **37.06 pp**.
* **Noise decomposition:** observed between-map variance of the gap 263.64 pp²,
  binomial component 10.86 pp² ⇒ **true between-map sd = 15.90 pp. 96% of the
  spread is real.**

⇒ **A CONSISTENT SEAT WOULD MEAN ENGINE OR HARNESS. THIS IS NOT CONSISTENT. IT
IS OURS.** This closes the question left explicitly open at
`docs/research/SEAT-AND-MAP-ASYMMETRY-2026-08-11.md` §3R-d.

**Two independent reasons the engine is excluded, so this does not rest on the
flip alone:**
1. §3R-a of that same document: **third-party games, 177,618 of them, read seat
   A 50.137% ± 0.233 pp.** There is no engine-level seat advantage to inherit.
2. **The favoured pole here is a COMPASS direction (§2.3), and the engine cannot
   know the compass** — it knows only which team is which. A seat-keyed engine
   bias could not produce "north wins on north–south maps and east wins on
   east–west maps".

### 2.3 ⭐ THE COMPASS FRAMING — and it is what points at the code

Re-expressing each map's result in terms of **which pole of the core-separation
axis wins**, rather than which seat:

| map | seat-A → enemy | gap (A) | winning pole |
|---|---|---:|---|
| glacierkeep | SOUTH | +46.31 | **N** |
| nordkap | SOUTH | +17.00 | **N** |
| fjordgate | SOUTHEAST | +15.44 | NW |
| midgard | SOUTHEAST | +14.54 | NW |
| auroraveil | SOUTH | +13.42 | **N** |
| drumlin | SOUTHEAST | +11.63 | NW |
| antler | SOUTH | +8.05 | **N** |
| drakkarfjord | EAST | +6.94 | W |
| frostgate | EAST | +4.25 | W |
| icefloe | EAST | +2.46 | W |
| royale | NORTH | +0.90 | S |
| ragnarok | SOUTHEAST | −0.90 | SE |
| yulerune | EAST | −4.93 | **E** |
| archipelago | SOUTHEAST | −18.57 | SE |
| valkyrie | EAST | −27.80 | **E** |

| grouping | n | share | z |
|---|---:|---:|---:|
| **NORTH pole**, on the 5 pure N–S maps | 4,468 | **58.39%** | **+11.22** |
| EAST pole, on the 5 pure E–W maps | 4,466 | 51.90% | +2.54 |

Per-map north-pole shares: `glacierkeep 73.2 · nordkap 58.5 · auroraveil 56.7 ·
antler 54.0 · royale 49.6`.

**CORRELATION AND ITS CONTROLS** (n = 15 maps, Pearson on the gap):

| predictor | r | verdict |
|---|---:|---|
| **NS-ness of the core axis** | **+0.583** | permutation **P = 0.0193** (20,000 shuffles) |
| **CONTROL — alphabetical index of the map name** | −0.216 | **does NOT fire** ✅ |
| CONTROL — map area | −0.040 | does not fire ✅ |

⭐ **The alphabetical control is the one that FIRED on the `bodyaware`
fingerprint** (`docs/research/BODYAWARE-MAP-FINGERPRINT-2026-08-16.md` §4.1,
r = +0.525, CI excluding zero) **and it is null here.** That is why this
correlation is worth more than the 26 in that document — the same n = 15, the
same maps, the same method, and this time the nonsense property stays quiet
while the structural one clears a permutation null.

⚠ **STILL A HYPOTHESIS, and the counter-evidence is stated in the same breath:**
`midgard` and `ragnarok` have **identical core anchors** ((2,2)/(26,26) on 30×30)
and read **+14.54** and **−0.90**. Core geometry alone does not determine the
sign — terrain interacts. And `frostgate` (E–W) favours the WEST pole, against
the east-pole grouping. **What is established is that the asymmetry is real,
large, map-dependent and ours. That its axis is the compass order in
`CARDINALS`/`DIRECTIONS` is the leading reading, not a finding.**

### 2.4 ⭐⭐ THE KILLER CONTROL — THE PER-MAP BIAS MOVES WHEN **WE** CHANGE CODE

If the per-map seat bias were a property of the map or the engine, it would be
**constant across our own chassis versions**. It is not.

| comparison | χ² | df | ratio | reading |
|---|---:|---:|---:|---|
| **within a cell**, split into seed halves | 71.6 | 62 | **1.15** | the fixture is essentially binomial |
| **between shards, same map** | **344.9** | **43** | **8.02** | **7.0× the within-cell ratio** |

Worked examples (seat-A % for the same map, different ABSOLUTE-order chassis):

| map | shards | min | max | swing |
|---|---:|---:|---:|---:|
| drakkarfjord | 3 | 42.5 | 78.2 | **35.7 pp** |
| heart | 4 | 47.9 | 70.4 | **22.5 pp** |
| royale | 3 | 40.7 | 62.5 | 21.8 pp |
| ragnarok | 3 | 40.6 | 60.3 | 19.7 pp |
| atoll | 4 | 34.2 | 51.8 | 17.6 pp |

**A map cannot change its geometry between our releases. This is the single
strongest own-evidence in the document that the asymmetry lives in our tree —
and it also warns that any per-map seat measurement is chassis-specific and goes
stale.**

*(⚠ The shards also differ in seed range, date and shard-contention level. The
seed-half control above shows seed draw does not add dispersion **inside** a
cell; it does not fully exclude a between-shard contention effect. The
`SRNULL0`/`SR1NULL`/`SR2NULL` trio in §4 was run the same night at the same
contention and still shows large per-map swings, which is a second, weaker
argument against the contention reading.)*

### 2.5 WHEN THE ADVANTAGE APPEARS — the opening, not the endgame

Current 15-map pool identity cells, n = 13,402:

| segment | n | seat-A share | z |
|---|---:|---:|---:|
| **kill before r250** | 6,280 | **54.14%** | **+6.56** |
| kill r250–499 | 3,070 | 51.21% | +1.34 |
| kill r500+ | 954 | 47.59% | −1.49 |
| tiebreak (r1000) | 3,098 | 53.97% | +4.42 |

⇒ **the seat advantage is an OPENING effect** that either converts into a fast
kill or into an economy lead that survives to the tiebreak. It is absent from
long grinds. **That is where the spawn-tile and ore-assignment sites live**, and
it is a pre-registrable prediction for any fix: *a fix that works should move the
`<r250` cell and leave the `r500+` cell alone.*

On `glacierkeep` alone the same shape is extreme: **80.72% seat A among sub-250
kills** (z = +9.70), and median kill round **246 for seat A against 336 for seat
B** — seat A on that map kills **90 rounds sooner**.

---

## 3. PART A — WHERE THE ASYMMETRY IS IN THE CODE

Read on `bots/_v223sealrepair/` (the incumbent, v140). **The tree contains no
seat canonicalisation of any kind:** `SEAT_RELATIVE_SCAN` = 0 occurrences,
`orient_cardinals` = 0 call sites. Every scan order, tie-break and hash below is
expressed in **absolute map space**.

Ranked by how much behaviour each governs. **MEASURED** means driven to the other
verdict in this session; everything else is **HYPOTHESIS** — a `file:line` that
*could* break symmetry is not evidence that it *does*.

### #1 — `bots/_v223sealrepair/eco.py:868` — BFS HANDEDNESS IS SEAT-LOCKED BY ENTITY-ID PARITY ⭐⭐⭐⭐

```python
# main.py:312
self.idx = ct.get_id() & 0xFF
# eco.py:866-874, _bfs_direction
side  = 1 if (self.idx & 1) else -1
order = [desired, CARDINALS[(i + side) % 4], CARDINALS[(i - side) % 4], desired.opposite()]
```

* **Governs:** the neighbour-expansion order of the pathfinder — the first-step
  tie-break on **every equal-distance route**, for every builder role (raid
  approach, ore approach, link approach, healer convergence). All `_nav` traffic
  funnels through it (`eco.py:901`), called from `eco.py:1088, 1180, 1224, 1242`,
  `raid.py:207`, `main.py:486, 680, 686`.
* **Runs:** every move, every builder, every round. **The highest-frequency site
  in the tree.**
* **⭐ MEASURED, and this is the fact that promotes it above everything else.**
  Decoded 120 replays (`scratchpad/**/*.replay26`) with `tools/replay_census.py`:

  | | matches its team's parity |
  |---|---:|
  | core | **120 / 120** — id 1 is always team 0, id 2 always team 1 |
  | builder #1 | **240 / 240 = 100.0%** |
  | builder #2 | **240 / 240 = 100.0%** |
  | builder #3 | 228 / 240 = 95.0% |
  | builder #4 | 189 / 232 = 81.5% |
  | builder #5 | 155 / 218 = 71.1% |

  Ids are issued globally in creation order and the engine runs core id 1 before
  core id 2, so while both cores spawn on the same rounds (the opening
  `LOKI_BASE_BUILDERS = 5` are unconditional) the parity is **deterministically
  opposite between seats**. It decays only once the two teams' spawn cadences
  diverge. ⇒ **In 100% of games, seat A's first two builders take `side = +1`
  and seat B's take `side = −1`: the two seats run mirror-image pathfinders.**
* **Why that is a symmetry break:** `CARDINALS = [N, E, S, W]` is a clockwise
  cycle, so `(i+1)` is clockwise and `(i−1)` counter-clockwise. A **rot180** map
  transform *preserves* handedness, so symmetry requires both seats to use the
  **same** `side`; they use opposite. *(On a **mirror** map the transform
  reverses handedness, so opposite `side` is what symmetry requires — the site is
  accidentally correct there.)*
* **⛔ THE DIRECTIONAL TEST THIS PREDICTS CAME OUT BACKWARDS — recorded before it
  is explained away.** The mechanism above predicts a **larger** seat gap on
  rot180-only maps than on mirror-only maps. Classifying all 15 current maps by
  which transform maps terrain **and** core A onto core B:
  **rot180-only (n=8) mean |gap| = 9.43 pp; mirror-only (n=5) mean |gap| =
  14.10 pp; difference −4.68 pp, permutation two-sided P = 0.296** (50,000
  shuffles). Dropping the `valkyrie` outlier the difference is −1.25 pp.
  ⇒ **The test does not support the prediction and does not refute it at n = 13
  maps. The site is asymmetric by measurement; that it DRIVES the win gap is
  HYPOTHESIS.**
* `eco.py:874`'s `else: order = CARDINALS` is a second, absolute fallback on the
  same function.
* Two further `idx`-keyed seat-locked quantities ride the same defect:
  `eco.py:802` `r = 3 + (round // 30) + (self.idx % 5)` (explore radius) and
  `eco.py:1062` `(rnd + self.idx) % SIPHON_SCAN_EVERY` (**the two seats scan for
  siphon targets on different rounds**).

### #2 — `bots/_v223sealrepair/main.py:289-290` — THE SPAWN-CANDIDATE SORT ⭐⭐⭐

```python
cands.sort(key=lambda sp: ((sp.x * 17 + sp.y * 31 + self.n * 13 + self.spawn_salt) % 97,
                           sp.y, sp.x))
```

* **Governs:** the tile **every** builder bot spawns on (5–11 per game), from
  round 0. Spawn tile decides who reaches which ore first and which way each body
  walks — the root of the whole opening.
* **Runs:** once per spawn, on the Core's turn.
* **MEASURED non-equivariant:** seat A's sorted candidate list, mapped through
  the map's symmetry transform, mismatches seat B's in **12 of 12** cases across
  4 real `CORE_PAIRS` anchors × 3 spawn indices, **differing at position 0 every
  time**. Example (`10×10`, A=(1,1), B=(7,7), n=0): A's first candidate reflects
  to (8,8); B's first candidate is (8,5).
* **MEASURED to carry the largest identified share of the gap** (§4:
  **+4.84 pp, CI [+0.98, +8.70]**).
* ⚠ **THE TWO AUDITS DISAGREED HERE, AND THE TAPE SETTLES IT.**
  `main.py:286-288` draws `spawn_salt = random.Random().randrange(97)` from OS
  entropy **independently per team** (`NOISE_ON = True`, `doctrine.py:474`). One
  audit read that as "noise, symmetric in expectation — not a cause"; the other
  measured the 12/12 non-equivariance above. **The salt only rotates the cut
  point in a cyclic order whose *spacing* is fixed by absolute coordinates, so
  the two seats sample different permutation families — and §4 measures the
  component at +4.84 pp, CI [+0.98, +8.70]. It is a cause.** *(The salt does mean
  the bias is partly randomised in the shipped bot, so +4.84 pp is a LOWER bound
  on what the site could carry if it were deterministic.)*

### #3 — `bots/_v223sealrepair/eco.py:97-104` — `nearest_cardinal` IS NOT EQUIVARIANT ⭐⭐⭐

```python
NORTH: NORTH,  NORTHEAST: EAST,  EAST: EAST,   SOUTHEAST: EAST,
SOUTH: SOUTH,  SOUTHWEST: SOUTH, WEST: WEST,   NORTHWEST: WEST,  CENTRE: NORTH
```

* **MEASURED broken under 180° rotation**, independently re-derived here:
  `NC(rot(NE)) = SOUTH` but `rot(NC(NE)) = WEST`; `NC(rot(SW)) = EAST` but
  `rot(NC(SW)) = NORTH`. **2 of 8 directions violate under rot180**; the audit
  also found violations under mirror-x and mirror-y. **It is broken under every
  symmetry class the current map pool uses.**
* **Look at the table itself:** the four diagonals collapse to **EAST ×2,
  SOUTH ×1, WEST ×1, NORTH ×0**. It is not a rounding rule; it is an arbitrary
  absolute-compass preference.
* **Governs:** the **facing of every trunk-link conveyor** (`eco.py:574, 576`,
  with a bare `f = Direction.NORTH` fallback at `:578`) — i.e. the economic
  backbone — and the facing a Gunner pays 10 Ti to rotate to (`main.py:842`).
* **Runs:** every conveyor build; every gunner rotate.
* **This is the cheapest fix on the list and the second-largest surface.**

### #4 — `bots/_v223sealrepair/eco.py:780` + `main.py:366-369` — ORE ASSIGNMENT ⭐⭐

```python
ordered = sorted(self.map_ores, key=lambda t: (abs(t.x-self.core.x)+abs(t.y-self.core.y),
                                               (t.x * 17 + t.y * 31 + worker * 7) % 97))
assigned = ordered[worker::workers] or ordered
```

* The **distance** term is core-relative and correct. **The tie-break is the same
  absolute hash as #1**, and equal-distance ore tiles are the *common* case on a
  symmetric map. `ordered[worker::workers]` then **strides** the list, so one
  hash flip **re-partitions ore between all four workers.**
* `self.map_ores` is itself built row-major in absolute coordinates
  (`main.py:366-369`).
* **Governs:** the entire economy layout — which builder goes to which ore.
* **Runs:** list built once; consumed every round a builder needs a target.
* Consistent with §2.5 (the effect is an opening effect).

### #5 — `bots/_v223sealrepair/raid.py:742` and `raid.py:819` — RAID ARRIVAL GEOMETRY ⭐⭐

```python
742:  return stations[self.raid_slot % len(stations)]          # stations = corners + seats
819:  k = (score, (s.x * 17 + s.y * 31 + self.raid_slot * 7) % 97, s.y, s.x)
```

`raid_slot` is a store counter and **is** seat-symmetric — but `stations` is an
absolute list relative to the enemy anchor
(`[NW, NE, SW, SE, N-l, N-r, E-t, E-b, S-r, S-l, W-b, W-t]`), so **index 0 is the
NW corner for BOTH seats.** Symmetry requires seat B's slot-0 raider to take the
*image* tile — index 3 under rot180, 2 or 1 under a mirror. It takes index 0 on
every map class. `:819` is the near-phase tie-break: the same absolute hash as #2
and #4, then `s.y, s.x` — **a hard north-then-west preference**, and `score` ties
constantly because its components are small integers.
**Governs:** the raid's arrival geometry, which `raid.py`'s own docstring says
the line wins on. **Runs:** every round per raider until `near`, then every
`LOKI_RAID_RESCAN = 6` rounds.
⇒ **All three `x*17 + y*31` hashes (`main.py:289`, `eco.py:780`, `raid.py:819`)
are one construction and need one rewrite: hash the offset from OUR core, not
the absolute tile.**

### #6 — `bots/_v223sealrepair/eco.py:1112` — HARVESTER SITING, NORTH-FIRST ⭐⭐

```python
for d in DIRECTIONS:            # [N, NE, E, SE, S, SW, W, NW]
    ...  if ok: ct.build_harvester(bp); ...; break
```

First-match-wins over the absolute 8-direction list, so a builder standing beside
two ore tiles **always takes the northern one**. **Runs:** every round per eco
builder with `cooldown == 0` and enough Ti. On the five N–S maps this means the
north-seated team builds harvesters **away from** the enemy and the south-seated
team builds them **toward** the enemy — same code, opposite exposure. **This is
the single most direct mechanism available for §2.3's north-pole result and it
has not been tested.**

### #7 — `bots/_v223sealrepair/eco.py:436` and `eco.py:468` — CONVEYOR ROUTE GEOMETRY ⭐⭐

`_link_path`'s BFS expands `for d in CARDINALS` and takes **first writer wins**
on `parent[key]`, so among equal-length routes the absolute scan order picks the
shape. **Governs:** the geometry of every trunk conveyor run from a harvester to
the core (`:436` known-map branch, `:468` sensed fallback). **Runs:** once per
harvester built, plus `_wire_tick` retries. Pairs with #3 (`nearest_cardinal`
sets the facing of each tile the route lays).

### #8 — `doctrine.py:25-26` — `DIRECTIONS` and `CARDINALS`, consumed first-match-wins ⭐

```python
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]   # N, NE, E, SE, S, SW, W, NW
CARDINALS  = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
```

Consumed by 20+ first-match-wins scans. The highest-governance consumers found:
`main.py:563` (counterbattery build tile), `main.py:573` (counterbattery turret
**facing**, over all 8 directions), `main.py:650` (launcher build tile), and the
`eco.py` scan sites re-verified at the shifted line numbers recorded in
`QUEUE #8` (`333, 394, 436, 468, 514, 845, 975, 1082, 1146, 1200`).

⛔ **This is the site `QUEUE #8` names as THE fix, and §4 measures its share as
consistent with zero.** It is real, it is genuinely asymmetric, and it is **not
where the win rate is.** Keep it on the fix list for correctness; do not price a
leg on it.

### #9 — `bots/_v223sealrepair/eco.py:802-807` + `main.py:313` — THE EXPLORE SPIRAL ⭐

```python
main.py:313  self.ang = (self.idx % 8) * (math.pi / 4)   # ang == 0 means ABSOLUTE EAST
eco.py:802   r = 3 + (ct.get_current_round() // 30) + (self.idx % 5)
eco.py:803   self.ang = (self.ang + 0.65) % (2 * math.pi)
```

Asymmetric three ways: the **seed angle** is `idx`-keyed and therefore seat-locked
by the same measured parity as #1 (seat A's openers get `ang ∈ {3,5,7,1,3}·π/4`,
seat B's `{4,6,0,2,4}·π/4` — a systematic 45° offset); the sweep always advances
**+0.65 rad**, but a mirror transform requires it to reverse; and the radius `r`
is `idx % 5`, also seat-locked. `int()` truncation toward zero is itself
asymmetric about the core. **Governs:** where a builder wanders when no known or
visible ore is available.

### #10 — `main.py:725-746` — TURRET LINE TARGETING ⭐

`if prio < best_prio` over `ct.get_attackable_tiles()`, whose ordering is
**row-major absolute**. Strict `<` means the first tile of the best priority
class wins, so two enemies of the same type on one ray resolve **absolutely**.
The docstring at `main.py:719-722` claims priority is "geometric/typed instead" —
**the key has no geometric term.** Runs every round, every turret; highest call
volume on the list, but each decision is small.

### #11 — `doctrine.py:1110-1172` — `MAP_CODES` DISAMBIGUATION IS SEAT-DEPENDENT ⭐

The lookup key `(w, h, ax, ay, bx, by)` is correctly seat-independent
(`eco.py:59` accepts `own` matching either anchor). **But four keys carry two
candidate grids each** — `(26,26,5,5,19,19)`, `(28,20,7,9,19,9)`,
`(20,20,2,9,16,9)`, `(30,30,2,2,26,26)` — and the disambiguator (`eco.py:76-84`)
scores candidates **against the calling unit's own vision**, resolving ties by
table insertion order. **The two seats see different regions, so they can adopt
different terrain models of the same match** (and the Core at `main.py:165` and a
builder at `main.py:360` can disagree within one team). **INFERRED**, not
measured — cheap to confirm by logging the chosen grid index per seat.
⚠ Note `(26,26,5,5,19,19)` is **archipelago** and `(30,30,2,2,26,26)` is
**midgard/ragnarok** — three of the four ambiguous keys are maps in the
significant-or-anomalous set (archipelago −18.57; midgard +14.54 vs ragnarok
−0.90 on identical anchors). **That coincidence is the most interesting untested
lead in this document.**

### #12 — THE LONG TAIL — 20+ further first-match-wins loops, each governing one narrow choice

`eco.py:333` (which damaged neighbour a defender heals) · `eco.py:674, 697, 715,
728` (`_l4_repair`: which trunk hole is relaid and **which way the relaid
conveyor faces**) · `eco.py:751-754, 906-907` (sidestep when the BFS direction is
blocked; `(i±1)` rotations are rot180-safe but **mirror-unsafe**, and `:906`'s
`else 0` default is absolute NORTH) · `eco.py:1146` (chain medic) · `eco.py:1200`
(ore step-off) · `eco.py:1232` (opportunistic ore re-target, north-first over all
8) · `eco.py:169, 179, 276` (`(y, x)` and `heal_seats`-index tie-breaks that
decide which 2 of 8 delivery seats are kept and which 6 are **banned for
harvester building** via `_seat_ban`, `HS_SEAT_PROTECT_ON = True`) ·
`eco.py:125` `nearest_core_tile` (ties resolve by `core_tiles` order, which
**reverses** under rot180) · `eco.py:1024` (siphon target ties resolve by entity
id) · `raid.py:271-280` (which seat of a corner gets collared first) ·
`raid.py:296, 317` (buddy heal, collar repair) · `raid.py:456, 489, 544` (salt
mark / salt the corpse / deny rebuild seat) · `raid.py:599-624` (`_raid_peck`
uses `if pr >= best_pr: continue`, so ties go to `CARDINALS` order) ·
`raid.py:672-689` (forward Sentinel build tile **and** which enemy core tile it
aims at) · `raid.py:925, 943` (launcher throw destination and ferry landing —
`sorted(..., reverse=True)` does **not** reverse ties, so both resolve to the
most north-west candidate for both seats).

### #13 — `CORE_PAIRS` (`doctrine.py:1081-1103`) — 8 of 31 entries are NOT point reflections

`(21,8,0,6,19,6)`, `(28,20,2,8,24,8)`, `(14,18,2,2,2,14)`, `(20,26,2,2,2,22)`,
`(25,15,0,0,0,13)`, `(21,21,2,2,2,17)`, `(11,16,0,0,9,0)`, `(25,15,11,3,11,10)`.
The table maps both directions so this is not itself a site — **but any
canonicalisation fix must DERIVE the per-map transform rather than assume point
reflection.** The fallback at `eco.py:53` assumes point reflection, so on an
unknown **mirror** map the enemy anchor is wrong, and **wrong differently for
each seat**.

**⭐ THE SYMMETRY-GROUP CENSUS, because it sizes the fix.** Decoding all 43
`MAP_CODES` + `EXTRA_MAP_CODES` grids and testing each transform against the
terrain: **22 rot180-only · 9 mirrorX-only · 8 mirrorY-only · 3
rot180+mirrorX+mirrorY · 1 rot180+transpose+antitranspose.** ⇒ **17 of 43 pooled
maps are HANDEDNESS-FLIPPING (mirror-only).** On the current 15-map pool the
split is **8 rot180-only · 5 mirror-only · 2 both** (`glacierkeep`, `royale`).
**A canonicalisation that only ROTATES (like `orient_cardinals`) is correct on
the rot180 maps and wrong on the 17 mirror maps** — any real fix must derive the
per-map transform and carry a **reflection flag**, exactly as `_v152seatrel2`'s
`seat_flip_for` does for the spawn hash.

### Checked and CLEAN — so nobody re-audits them

* `main.py:535, 546` — `min(distance_squared)` returns a **number**; the distance
  multiset is symmetric.
* `main.py:649` — `heal_seats(...)` consumed into a **set**; order-insensitive.
* `main.py:292, 494, 567, 654` — `0 <= x < mw` bounds checks; symmetric.
* `main.py:492` `_sabotage_prio` — absolute `CARDINALS` tie-break, but **inert**:
  `LOKI_QUIET_ON = True` (`doctrine.py:1488`) returns before the fire.
* `eco.py:679-681` `LOKI_L4_OWN_HALF_ONLY` — uses
  `g.distance_squared(self.core) > g.distance_squared(self.enemy)`, a **relative**
  half test. **The one comparison in the tree that got it right**, and the model
  for how the others should be written.
* `Position.direction_to` / `cardinal_direction_to` are themselves equivariant
  (0 violations over a 13×13 offset grid under rot180, mirror-x and mirror-y;
  `cardinal_direction_to` would break under **transpose**, and exactly one pooled
  map has transpose terrain symmetry — but it also has rot180, so that is not a
  live channel). **`nearest_cardinal` is the sole break in that chain.**
* `doctrine.py` holds no executable logic beyond `:25-26` and the data tables.
* `eco.py:53 enemy_core_for` fallback `(w-2-x, h-2-y)` — wrong on a mirror map
  absent from `CORE_PAIRS`, but **symmetrically wrong** (verified algebraically:
  seat B's fallback is the exact image of seat A's). Not a seat-asymmetry site.
* `eco.py:84 known_map_for` `min(candidates, key=mismatch)` — on genuinely
  symmetric terrain both seats compute identical mismatch counts. *(This is the
  clean path; #11 is about the cases where the counts are computed against the
  unit's own vision instead.)*
* `eco.py:176` delivery-seat centre score `abs(2*s.x-(mw-1)) + abs(2*s.y-(mh-1))`
  — invariant under all four transforms. The asymmetry at that site is purely in
  the tie-breaks (#12).
* `eco.py:394, 845, 856` (BFS goal sets), `eco.py:513, 605`, `raid.py:575, 834`
  (`any()`/count over `CARDINALS`), `raid.py:140, 153, 190, 668, 710, 720`
  (`min` over **values**), `raid.py:422` (strict core-distance comparison) — all
  order-independent or relative. Clean.
* `eco.py:940` `PAVE_TRAIL_ON` use — **dead**: `doctrine.py:528` sets it `False`.

---

## 4. ⛔ THE DECLARED `QUEUE #8` FIXTURE HAS BEEN RUN, AND THE NAMED FIX DID NOT WORK

`QUEUE.md` row 8 states the byte-identical null with **both sides** seat-relative
"has never been run". **It was run on 2026-08-11T18:39→22:57Z**, as `SR1NULL`
(CARDINALS only) and `SR2NULL` (CARDINALS + spawn sort), against `SRNULL0` — a
contemporaneous untreated null added by the side lane specifically so every term
is measured in one harness state.

| shard | treatment | n | seat-A | **gap** | **mean per-map \|gap\|** |
|---|---|---:|---:|---:|---:|
| `SRNULL0` | none (absolute order) | 5,408 | 52.61% | **+5.21 pp** | **10.02 pp** |
| `SR1NULL` | CARDINALS canonicalised | 5,408 | 54.11% | **+8.21 pp** | **9.02 pp** |
| `SR2NULL` | CARDINALS + spawn sort | 5,408 | 51.68% | **+3.37 pp** | **9.06 pp** |

**The partition, using the estimators the prereg declared (Amendment 3), with the
SEs it declared (Amendment 4: a component must carry ≥3.9 pp to be individually
distinguishable from zero):**

| component | estimator | value | 95% CI | verdict |
|---|---|---:|---|---|
| **CARDINALS share** | `SRNULL0 − SR1NULL` | **−3.00 pp** | [−6.86, +0.86] | **consistent with zero** (and nominally the wrong sign) |
| **spawn-sort share** | `SR1NULL − SR2NULL` | **+4.84 pp** | [+0.98, +8.70] | **CLEARS the 3.9 pp bar**, z = 2.46 |
| **residue** | `SR2NULL` | +3.37 pp | [+0.65, +6.09] | non-zero |

* The prereg **pre-declared** that a true-zero share reads negative half the
  time and must be reported as *consistent with zero*, never as harmful. That is
  what is done above for CARDINALS.
* The spawn-sort share is the **largest of three selected after the fact**;
  Bonferroni over 3 needs |z| > 2.39 and it reads 2.46 — **it survives, barely.**
* **The per-map dispersion did not shrink on either arm** (10.02 → 9.02 → 9.06,
  and the between-map sd actually *rose* on `SR2NULL` to 12.45 pp). At n = 676
  per map cell the SE on a per-map gap is ≈ 3.85 pp, so the MDE on a mean-|gap|
  change is roughly **±2.7 pp** — a 1 pp move is invisible. **What is
  established is "no detectable reduction", not "no reduction".**
* **The compass structure survived both fixes.** North-pole share on the three
  N–S maps in that pool: `SRNULL0` 53.01% → `SR1NULL` **56.11%** → `SR2NULL`
  **55.52%**. Canonicalising the scan order did not remove the north preference.

⇒ **The next seat leg should treat `main.py:289` + `eco.py:780` + `raid.py:819`
(one shared hash construction) and `eco.py:97` (`nearest_cardinal`) as the
treatment, and `doctrine.py:26` as already-tested-and-null.**

---

## 5. THE `s43 SEAT_RELATIVE` SELFTEST — IT PASSES, AND HERE IS EXACTLY WHAT IT ASSERTS

`tests/test_seat_relative.py`, run with `.venv/bin/python tests/test_seat_relative.py`
(no pytest in the venv):

```
SEAT_RELATIVE_SELFTEST: PASS (11/11 maps canonicalise under treatment, 0 under the shipped order)
```

Four treatment cells all `[ok]`, and — the part that matters — **the negative
cell fires**: the shipped absolute `[N,E,S,W]` canonicalises on **0 of 11** maps,
because it reflects to `[S,W,N,E]`, a different list.

**WHAT IT ASSERTS:** that `orient_cardinals` makes the two seats' `CARDINALS`
lists exact point reflections of each other; that the result stays a 4-cycle (so
`eco.py`'s `(i±1) % 4` "perpendicular" arithmetic is not silently turned into
"opposite"); that it is idempotent over 50 calls; and that the `abs(dx)>=abs(dy)`
tie-break is itself reflection-invariant.

**⛔ WHAT IT DOES NOT ASSERT, AND THIS IS THE POINT:**
1. It tests **`bots/_v151seatrel/doctrine.py`**, not the incumbent. **The
   incumbent does not contain the function at all.**
2. It asserts a property of **`CARDINALS` only**. It does not touch `DIRECTIONS`,
   the three `x*17 + y*31` hashes, `nearest_cardinal`, the row-major `map_ores`
   list, or the `MAP_CODES` disambiguator. **Porting `orient_cardinals` into the
   incumbent would fix site #5 and nothing else** — and §4 measures site #5's
   share as consistent with zero.
3. It asserts **canonicalisation**, not **outcome**. A green selftest here says
   the plank is correctly built; it says nothing about whether it wins games.

---

## 6. THE UPPER BOUND OF A SYMMETRIC FIX

**⛔ The brief's literal phrasing — "raise the disadvantaged seat to the
advantaged seat's level" — is internally inconsistent in self-play**, where
`A% + B% ≡ 100` by construction; raising B to A's level would give 53.31 + 53.31.
The honest translation is a **strength** statement.

Pooled current-15 identity cells: seat A 52.96% ⇒ **our own two seats differ by
20.6 Elo**. A fix that lifted the worse seat to the better one raises our average
strength by **half** of that, because half our games are in each seat.

| fix | mean Elo gained | **win share, vs a fixed opponent** | **on a T-vs-C board shard** |
|---|---:|---:|---:|
| **single global seat-symmetry fix** | +10.3 | **+1.48 pp** | **+1.48 pp** |
| **per-map fix, capturing the sign flips** (raw) | +23.0 | +3.22 pp | +3.22 pp |
| **per-map fix, noise-shrunk** *(shrink factor 0.959)* | +22.0 | **+3.19 pp** | **+3.19 pp** |

*(The board figure is derived independently and agrees: on each map, T@good-seat
is unchanged and T@bad-seat rises to 50%, giving `T = mean_maps[(g + 50)/2]`
where `g = max(q, 1−q)` — 53.19% shrunk, 53.22% raw.)*

**HOW TO READ THESE:**
* **They are UPPER BOUNDS in the strict sense** — they assume the *entire*
  measured gap is a removable code deficit and that the fix costs nothing.
  §4 is the empirical warning: two fixes were built and fired and delivered
  **none** of it.
* **The pooled +1.48 pp is the safe number.** The per-map +3.19 pp requires a fix
  that is right on **every** map including the two that flip, which is a strictly
  harder engineering problem than "canonicalise the scan order".
* **Against the board:** ceiling **55.24%**, Magnus's bar **60%**, gap **+4.8 pp**.
  Even the per-map upper bound lands at **~58.4%** — **the seat fix does not
  reach 60 on its own.** It is the largest *free* move on the board (no new
  mechanism, no strategic risk) but it is not the whole gap, and a leg that is
  priced as if it were will miss.

---

## 7. LIMITS — read before quoting anything above

1. **LOCAL ONLY. No live-game backing.** Under the standing rule
   (*"a refutation without live-game backing is a hypothesis"*), **this document
   closes no road.** It prioritises.
2. **The compass/axis reading (§2.3) is a HYPOTHESIS at n = 15 maps.** The
   `bodyaware` fingerprint proved that a nonsense property can clear at this n.
   The alphabetical control staying null here is genuine reassurance, and
   `midgard` vs `ragnarok` (identical anchors, opposite signs) is genuine
   counter-evidence. Both are recorded.
3. **Every code site is a HYPOTHESIS about *outcome* unless marked MEASURED.**
   What is MEASURED here is (a) **entity-id parity is seat-locked**, 240/240 on
   builders #1 and #2 across 120 replays, and core id 1 = team 0 in 120/120;
   (b) the spawn-sort ring order is non-equivariant, 12/12; (c)
   `nearest_cardinal` is non-equivariant under rot180 (2 of 8, independently
   re-derived); (d) the pooled map symmetry census, 43 maps; and (e) the
   spawn-sort *component* carries +4.84 pp (§4). **Everything else is
   "asymmetric by inspection", which is not the same as "moves the win rate".**
   ⛔ **In particular, site #1 is the best-evidenced *asymmetry* on the list and
   its one directional prediction (bigger gap on rot180 maps than mirror maps)
   came out BACKWARDS at P = 0.296.** Written down here rather than dropped,
   because that is the same shape as `BODYAWARE`'s §7B and it is the honest state
   of the mechanism question.
4. **Chassis staleness.** §2.4 shows the per-map bias moves by up to 35.7 pp
   between our own releases. **The per-map table in §2.2 is a property of the
   `v104`/`v123`/`v125`-era chassis that ran those shards, not of
   `_v223sealrepair`.** No identity null has been run on the incumbent. **That is
   the cheapest missing measurement in this document** and it is a
   pure-throughput ask.
5. **The `SR*` trio ran the RETIRED 8-map pool**, four of whose maps
   (`atoll heart hive meander`) are no longer in the pool — and that retired
   subset reads **−0.96 pp, i.e. no seat gap at all**. §4's partition is
   therefore measured on a map set only half of which we still play.
6. **`NOISE_ON = True`** means each team draws its own `spawn_salt` from OS
   entropy, so identity self-play is not deterministic. This is variance, not
   bias, and the `QUEUE #8` rider is right that pinning it False would measure a
   bot we do not run (and collapses `antler` to one distinct game). It does mean
   the spawn-order asymmetry is partly *randomised* in the shipped bot — which
   makes the measured +4.84 pp share a **lower** bound on what the site could
   carry if it were deterministic.
7. **DEFF.** Local balanced-by-construction fixtures read pair-weighted
   **0.98**; naive intervals are used throughout and are marginally
   conservative. The within-cell seed-half control (ratio 1.15) is the
   session-local check that this holds on these particular tapes. **No platform
   constant was imported.**
8. **Between-shard confound.** §2.4's shards differ in chassis *and* in seed
   range, date and contention. The seed-half control removes the seed reading;
   contention is not fully excluded.

---

## 8. WHAT TO DO NEXT — in value order

1. **⭐ Run a byte-identical null on `_v223sealrepair` itself, on the current
   15-map pool.** No identity cell exists for the shipping bot. Everything in §2.2
   is measured on older chassis and §2.4 proves that matters. **Free, one shard.**
2. **⭐⭐ THE CHEAPEST ONE-LINE ARM ON THE BOARD: make the BFS handedness
   seat-relative** (`eco.py:868`). Today `side` is `self.idx & 1`, a bit that is
   MEASURED seat-locked 240/240 on the opening builders. Replacing it with a
   handedness derived from `core → enemy` plus the map's reflection flag makes
   the two seats' pathfinders mirror images *of each other* instead of *of
   symmetry*. It touches one expression and it sits under every builder move of
   every round. **Fire it as a both-sides-identical null against §8.1.**
3. **⭐ Build ONE arm that rewrites all three `x*17 + y*31` hashes to hash the
   offset from our own core** (`main.py:289`, `eco.py:780`, `raid.py:819`),
   **makes `nearest_cardinal` core-relative** (`eco.py:97`), and **makes the raid
   station index seat-relative** (`raid.py:742`). These are one class and one
   rewrite. **Pre-register the prediction from §2.5: the `<r250` cell moves, the
   `r500+` cell does not.**
4. **Log the `MAP_CODES` disambiguator's chosen grid index per seat** on
   `archipelago` and `midgard`/`ragnarok` (§3 #11). If the two seats adopt
   different terrain models of the same match, that is a *different* and larger
   bug than a scan order, and it is a five-minute check.
5. **Amend `QUEUE #8`:** its declared fixture has been run (§4); the CARDINALS
   component reads consistent with zero; the spawn sort is the component that
   cleared; and the row's premise — "order the scan by `cardinal_direction_to`" —
   is a **rotation**, which is correct on 26 of 43 pooled maps and wrong on the
   17 mirror-only ones (§3 #13). The row's `~+7–14 Elo` estimate should be
   restated as **+1.48 pp (~+10 Elo) pooled / +3.19 pp per-map, as an upper
   bound**, with §4 as the measured warning that a fix need not collect it.
6. **Do NOT re-derive the seat effect from a T-vs-C board shard.** With two bots
   in a zero-sum pairing, `T%@A − T%@B` is one number both bots share
   (`BODYAWARE-MAP-FINGERPRINT-2026-08-16.md` §6.2). The byte-identical null is
   the only design that isolates it, and nine of them already exist.
