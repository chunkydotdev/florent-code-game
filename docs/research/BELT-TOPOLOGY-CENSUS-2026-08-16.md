# QUEUE #78 mechanism (a): sizing the trunk-merge prize before anyone writes a bot tree

**Research arm, 2026-08-16 13:0xZ (`date -u`), repo `d1bbdfd0`.**
**Instrument:** `tools/belt_merge_prize.py` (new, this cut). Free corpus cut — no
games fired, no platform window spent.

---

## 0. THE ONE-LINE VERDICT

**The prize is REAL but SMALL, and it lands almost exactly ON the "one extra
turret" bar rather than comfortably above it.** On our current tree's own 360
ladder games: **~8.9 conveyors/game saved (calibrated ~8.1), = ~7.2pp of cost
scale by r150, = ~78 Ti freed, = ~1.25 extra gunners in the MEAN game and
0.90 in the MEDIAN game.** 47% of games buy a whole extra gunner by r150; 29%
buy a whole extra sentinel. An out-of-sample run on an older tree/map pool
(v104, 510 games) returns **0.82 extra gunners** — so the honest band is
**0.8-1.3 turrets at the kill window, i.e. approximately one.**

**And the plank carries an unpriced counter-cost that this cut can see:
merging pushes the busiest belt tile over its throughput ceiling in 126/360
games against 76/360 today.** See §6. That is the thing a build must measure,
not the conveyor count.

---

## 1. POPULATION — the enumeration rule, with its count

**RULE:** every row of `corpus/join.tsv` whose `ourver == "140"`.
**COUNT: 360 games. 360 of 360 have BUILD/DEATH rows in `corpus/events.tsv`.
0 dropped by any filter.**

Why this population and not another:

* **v140 = `bots/_v223sealrepair`** (`corpus/version_trees.tsv`, submit_clean
  auto-record, 2026-08-14T11:37:38Z) — **the exact tree whose `_link_path` is
  the subject.** These are the belts the defect actually built.
* `join.tsv` is **ladder-only**: verified `|join ∩ unrated_games| = 0` over
  4,190 / 6,046 rows. No rated/unrated pooling; and nothing here is a win-rate
  denominator, so the `meta_join` trap does not apply.
* **The seat is not the winner-derived one (TRAP 7).** `join.our_team` was
  cross-checked against `meta_join.us_side`, which is derived from
  `teamAName == "OpenSverige"` and is therefore independent of `winnerSide`:
  **4,185 agree / 4,185 testable, 0 disagree.**
* **EXCLUDED and why:** the 1,143 UNRATED v140 games in `meta_join`.
  `corpus/unrated_games.tsv` carries only `map_w`/`map_h`, **no map name**, so
  their wall/ore geometry cannot be resolved. Excluding them costs breadth, not
  validity — and it is stated rather than silently absorbed.
* **OUT-OF-SAMPLE:** the same rule with `ourver == "104"` (`bots/_v130loki13`,
  the OLD 25-map pool) → **510 games**, reported in §7 as a robustness read.

Maps in the v140 cell (15, the current pool): ragnarok 29, antler 28,
auroraveil 28, royale 27, glacierkeep 26, icefloe 25, frostgate 25, yulerune 24,
midgard 24, fjordgate 23, nordkap 22, drakkarfjord 22, valkyrie 21, drumlin 18,
archipelago 18.

---

## 2. CURRENT STATE (characterisation — no prediction was registered for these)

| quantity, OUR team, v140, n=360 | mean | median |
| --- | --- | --- |
| conveyor+splitter BUILD events / game | **33.5** | 28 |
| distinct belt TILES built / game | **32.4** | — |
| harvesters built / game | **6.32** | — |
| game length (turns) | 257 | 184 |
| **modelled cost scale at r150** | **304.2%** | 295.0% |
| **modelled cost scale at r250** | **319.1%** | 301.5% |

**Games alive at the cutoffs: 234/360 at r150, 111/360 at r250.** Any r250 figure
is therefore a statement about the *long half* of our games; r150 is the honest
kill-window read (our median kill is r174).

**⚠ `scale_percent` IS A MODELLED PROXY, NOT A CORPUS COLUMN.** The corpus has no
scale field. It is reconstructed per game from our team's BUILD/DEATH event
stream using the additive rule (`conveyor/splitter/barrier +1%`, `harvester +5%`,
`launcher +10%`, `builder_bot/gunner/sentinel +20%`, destruction removes the
contribution) — the rule is engine-confirmed in `CLAUDE.md` via `bots/_probe_scale`,
but **this reconstruction of it has no independent ground truth in the corpus and
should be read as a proxy.** Its plausibility check: 6.9 builder bots (+138%) +
3.4 sentinels (+68%) + 33.5 conveyors (+33.5%) + 6.3 harvesters (+31.5%) +
7.0 barriers (+7%) ≈ +290% gross, less deaths → ~300%. It reconciles.

**The single most important consequence of a ~300% scale: a conveyor costs
`floor(3.04 × 3) = 9 Ti`, not 3.** Belt is three times its sticker price at the
kill window, which is most of why this plank has any prize at all.

**Split by map size class** (area = w×h):

| class | n | observed belt | modelled BASE belt |
| --- | --- | --- | --- |
| small (<200) | 23 | 7.9 | 9.2 |
| mid (200-499) | 157 | 27.2 | 29.4 |
| big (≥500) | 180 | 42.3 | 44.8 |

**EXPECTED, and confirmed:** big maps carry longer belts and, in §5, a bigger prize.

---

## 3. THE COUNTERFACTUAL — and what it deliberately is NOT

**⭐ THE DESIGN CONSTRAINT: THE MODEL IS THE PROPOSED FIX, NOT PERFECTION.**
Three arms, all replayed on the real map geometry (`maps/*.map26` via
`tools/map_encode.parse_map26`) and, critically, **in the harvesters' real build
order taken from `corpus/events.tsv` (`rnd`, `x`, `y`)** — the planner is online
and cannot see future harvesters.

| arm | goal set | order |
| --- | --- | --- |
| **BASE** | core ring only (`core_tiles × CARDINALS`, = the 8 heal seats) | online, real order |
| **MERGE** *(the estimate)* | core ring **∪ our live belt tiles at that moment** | online, real order |
| **PRIM** *(bound only)* | core ring ∪ tree-so-far, attaching the cheapest harvester next | **offline, order-free, most-generous obstacle set** |

Faithful details, read off `bots/_v223sealrepair/eco.py`:

* BFS runs **outward from the goals** and stops at the harvester, then walks the
  parent chain back — the shape of the `map_grid` branch at `:391`, including
  the `CARDINALS` order N,E,S,W.
* `blocked` = walls ∪ ore (except the harvester's own tile) ∪ the 4 core tiles ∪
  our live non-belt buildings. **Friendly belt is traversable, never blocked** —
  that is the defect. `_pave_ban()` is `None` in the shipped tree
  (`HS_SEAT_BAN_CONVEYORS = False`, `doctrine.py:646`), so no seat ban applies.
* **Conveyor accounting is identical in every arm:** `_build_next_link` pops a
  planned tile that already carries a building rather than rebuilding it, so
  `new = |path \ laid|`, then `laid |= path`. **This is why BASE already merges
  by ACCIDENT** — and it is why the estimate below is a delta over an already
  partly-merged baseline rather than over a naive one.
* Flow accounting (§6) follows the same rule: a stack entering an existing belt
  tile follows *that tile's* route home, because the crossed conveyor is never
  reoriented.

**⛔ PRIM IS REPORTED AS A BOUND AND NEVER AS THE ESTIMATE.** It is an offline
Prim-style Steiner heuristic — not the Steiner optimum (that is NP-hard), and our
planner is neither offline nor order-free.

---

## 4. INSTRUMENT VALIDATION — five controls, three of which can fail

**C1 GEOMETRY (per game, blocking).** For every BUILD row, the recomputed
d²(build tile, map-file core anchor for that team) must equal the corpus
`d2_own`; and every harvester must land on an **ORE** tile of the map file.
A wrong map name or a team-index slip fails this loudly.
**RESULT: 360/360 games pass, 0 dropped.** This is the check that licenses using
map-file walls and ore as the planner's obstacle set.

**BASE-ARM CALIBRATION (the one that matters most).**
Modelled BASE belt **35.8** tiles/game vs **32.4** observed distinct belt tiles —
**ratio 1.10**, i.e. the model lays 10% more belt than we really did.
**TILE-SET AGREEMENT: 10,935 / 11,676 observed belt tiles (93.7%) are tiles the
BASE model independently predicted**; conversely 10,935 / 12,887 (84.9%) of
modelled tiles were really built. **A model reproducing 93.7% of the actual belt
tile-for-tile is measuring our planner, not a planner of its own invention.**
⇒ **The headline delta is also reported CALIBRATED by 0.906 (= 32.4/35.8).**

**C2 SINGLE-HARVESTER — the must-come-out-the-other-way control.** In a game with
exactly ONE harvester there is no live belt to merge into, so the saving is zero
*by construction*. **n = 5 such games; non-zero saving in 0. PASS.**
(Two-harvester games, n = 25, mean saving 1.40 — so the instrument is not simply
dead at low n.)

**C3 HAND CASE.** Synthetic open 11×11, core at (5,5), harvesters at (1,5) and
(9,5) — opposite sides, no merge available. **BASE = 5, MERGE = 5, per-line
[3,2] both arms. PASS: the model reproduces the actual laid path when no merge
exists.**
**C3b MIRROR.** Same grid, harvesters stacked at (1,5) and (1,6) — a merge is
available. **BASE = 6, MERGE = 4. PASS: the instrument does find a saving when
one exists**, so C3's null is a measurement and not an inability.

**C4 TIE-BREAK SENSITIVITY.** Equal-length shortest paths make the goal-set
iteration order matter. Re-running 60 games with the goal order shuffled under
3 seeds: **deterministic 9.65/game vs shuffled 10.72 / 10.85 / 10.15, spread
0.70.** ⇒ **the deterministic (sorted) tie-break is the CONSERVATIVE one**;
tie-breaking accounts for at most ~1.2 conveyors/game of the delta, and in the
direction that makes our estimate smaller, not larger.

**AND THE INSTRUMENT RETURNS NO SAVING OFTEN: 61 of 360 games (17%) show
exactly zero.** A model that always finds a prize has not been shown to measure
one; this one abstains in a sixth of the population.

---

## 5. THE DELTA, IN THREE CURRENCIES

### (a) conveyors saved per game

| arm | mean | median | max | zero-saving games |
| --- | --- | --- | --- | --- |
| **GREEDY MERGE — THE ESTIMATE** | **8.91** | 6 | 64 | 61/360 |
| calibrated (×0.906, §4) | **8.07** | — | — | — |
| OFFLINE PRIM — **BOUND ONLY** | 9.07 | — | — | — |

= **24.9% of the BASE belt.**

**⭐ THE MOST DECISION-RELEVANT NUMBER IN THIS SECTION IS THE GAP BETWEEN THE
ESTIMATE AND THE BOUND: 8.91 vs 9.07.** The greedy, online, order-constrained fix
captures **98%** of what an offline order-free heuristic gets. **There is no
second, cleverer version of this plank worth building** — mechanism (a) as
specified is essentially the whole road. (Caveat: PRIM is a heuristic, not the
Steiner optimum, so the true offline ceiling is somewhat above 9.07.)

By map size class — **EXPECTED bigger prize on bigger maps, CONFIRMED**:

| class | n | BASE | saved | PRIM bound |
| --- | --- | --- | --- | --- |
| small (<200) | 23 | 9.2 | **1.48** | 1.70 |
| mid (200-499) | 157 | 29.4 | **7.20** | 7.33 |
| big (≥500) | 180 | 44.8 | **11.34** | 11.53 |

By game length: <150 turns (n=126) 5.75 saved · 150-249 (n=123) 9.46 · ≥250
(n=111) 11.87.

### (b) converted to SCALE

Each conveyor is **+1 percentage point** on the global additive factor,
permanently. Counting only harvesters routed **by the cutoff round**:

| cutoff | conveyors saved | **scale delta** |
| --- | --- | --- |
| r150 | mean 7.22 (median 5.0, p25 1.0, p75 10.8) | **−7.22 pp** |
| r250 | mean 8.33 (median 6.0, p25 1.2, p75 12.0) | **−8.33 pp** |

Against a modelled 304.2% at r150, that is a **2.4% relative** reduction in the
price of everything.

### (c) ⭐ WHAT THAT BUYS AT THE KILL WINDOW — the only currency that counts

Titanium freed = (conveyors never built, at their real ~9 Ti price) + (the
cheaper `floor(scale × base)` on every subsequent build).

**At r150 — mean 78.2 Ti freed, median 50.5 Ti:**

| turret | price now | price after | Δ price | **extra affordable (mean / median)** | share of games buying ≥1 |
| --- | --- | --- | --- | --- | --- |
| gunner | 60.2 Ti | 58.8 Ti | −1.4 | **1.25 / 0.90** | **47%** |
| sentinel | 90.7 Ti | 88.6 Ti | −2.1 | **0.83 / 0.60** | **29%** |
| launcher | 60.2 Ti | 58.8 Ti | −1.4 | **1.25 / 0.90** | **47%** |

**At r250 — mean 91.0 Ti freed, median 54.5 Ti:** gunner 1.33/0.91 (48% buy ≥1),
sentinel 0.88/0.60 (31%), launcher 1.33/0.91.

**⛔ NOTE WHERE THE PRIZE ACTUALLY COMES FROM, because it changes what a build
should optimise: ~65 of the 78 Ti is simply NOT PAYING FOR 7.2 CONVEYORS AT 9 Ti
EACH. The scale channel proper — every other build getting cheaper — is worth
only ~13 Ti, about 1.4 Ti off a gunner.** QUEUE #78 states the currency as scale;
the measurement says the currency is **mostly the direct build cost**, with scale
a ~17% garnish. The plank is still worth what it is worth, but a prereg that
denominates its bar in `get_scale_percent()` alone is measuring the small half.

**IS THE FREED TITANIUM SPENDABLE, OR DOES IT SIT IN AN IDLE BANK?** This is the
question that could have killed the plank, and it does not. Our own `econ.tsv`
`ti_end` for these 360 games: **r0-150 median 44 Ti held (p25 12, mean 58);
r150-200 median 50; r200-300 median 54.** We are titanium-constrained through the
entire kill window — we do not bank. **78 Ti freed is ~1.8× the median bank at
r150, and it will be spent.**

**A SECOND, UNPRICED CURRENCY WORTH MORE THAN IT LOOKS: 7.2 fewer conveyor
builds by r150 is 7.2 BUILDER-TURNS returned** (build and move are mutually
exclusive per turn). Magnus's own replay marker on match `59f4d2bc` g3 said
exactly this — *"would have saved us 2 conveyor and build rounds for a builder"*.
This cut does not price builder-turns and a build should.

---

## 6. ⛔ THE COUNTER-COST THIS CUT CAN SEE, AND IT IS NOT IN THE QUEUE ROW

A conveyor holds one stack and moves at most **1 stack/round**; a harvester emits
**1 stack / 4 rounds**. ⇒ **a shared tile saturates once more than 4 harvester
lines route through it**, and beyond that the merged trunk throttles delivery.
(Rules-level inference from out-degree 1 + single held stack — per the standing
rule this PRIORITISES a concern, it does not close or open a road.)

Measured on the flow routes of both arms:

| | BASE | **MERGE** |
| --- | --- | --- |
| busiest tile, harvester lines through it (mean) | 3.29 | **4.27** |
| busiest tile (max over games) | 14 | **17** |
| **games with a tile carrying >4 lines** | **76/360 (21%)** | **126/360 (35%)** |
| distinct terminal tiles (belt entries) | 3.29 | 2.25 |

**Merging takes 50 additional games over the saturation threshold and cuts the
number of independent belt entries from 3.3 to 2.3.** It also concentrates the
belt: one lucky enemy peck on a shared trunk now orphans several harvesters at
once instead of one. **⇒ A build must carry a throughput guard — e.g. refuse a
merge onto a tile already carrying ≥3 lines, falling back to the core ring — and
the prereg's falsifier should be delivery, not conveyor count.**

Two further optimisms in the estimate, both stated because they push the same
way:
1. **Acceptor side is unmodelled.** A conveyor accepts from 3 sides and outputs
   to the 4th; a merge arriving on the output side is illegal. Rare for a
   perpendicular branch, but non-zero → the estimate is slightly high.
2. Harvester **deaths and belt rebuilds** are not replayed; the belt is treated as
   monotonically growing.

---

## 7. OUT-OF-SAMPLE: v104, the old tree and the old 25-map pool (n = 510)

Same rule, `ourver == "104"` (`bots/_v130loki13`).

| | v140 (n=360) | v104 (n=510) |
| --- | --- | --- |
| observed belt / game | 33.5 | 25.8 |
| BASE modelled | 35.8 | 29.0 |
| tile-set agreement | 93.7% | 89.3% |
| **saved / game** | **8.91** | **5.33** |
| PRIM bound | 9.07 | 5.64 |
| zero-saving games | 61/360 (17%) | 137/510 (27%) |
| scale delta @ r150 | −7.22 pp | −4.36 pp |
| Ti freed @ r150 | 78.2 | 48.6 |
| **extra gunners @ r150** (aggregate ratio, mean-Ti / mean-price; §5's 1.25 is the per-game mean of the ratio) | **1.30** | **0.82** |
| games over saturation, BASE → MERGE | 76 → 126 | 108 → 154 |

**The prize is map-pool and tree dependent by roughly 1.7×.** The current pool is
the favourable end of that band. Both arms agree on the sign, on the congestion
direction, and on the near-coincidence of greedy with the offline bound.

---

## 8. DOES IT REACH THE KILL? — the plain verdict

**Yes, barely, and the honest way to state it is: this plank buys approximately
ONE extra turret at the kill window, with a 0.8-1.3 band across tree and map
pool, and it buys it in fewer than half the games individually (47% for a
gunner, 29% for a sentinel).**

That is **not** the decisive negative the task allowed for — it clears the "less
than one extra turret" bar in the mean, on the current map pool, and the freed
titanium is demonstrably spendable rather than banked. But it is close enough to
that bar that the following should govern any build:

1. **SCOPE IT SMALL.** It is a goal-set edit inside one function
   (`eco.py:391`, one `raw_goals.update(live_belt_tiles)`), plus a throughput
   guard. If the diff grows past that, the prize does not justify it.
2. **THE FALSIFIER IS DELIVERY AND KILL ROUND, NOT CONVEYOR COUNT.** Conveyor
   count will fall — the model already says so with 93.7% tile fidelity, and
   re-measuring it live buys nothing. What is unknown is whether the concentrated
   trunk throttles delivery (§6) or whether the extra gunner lands before r300.
   Under `DEFENCE_ADMISSION_BAR` the primary is the **timely-kill rate by r300**.
3. **PREFER BIG MAPS FOR THE DOSE.** 11.3 conveyors saved on maps ≥500 tiles vs
   1.5 on maps <200 — an arm restricted to the big half has ~7.7× the dose of the
   small half, and the current pool is 180/360 big.
4. **DO NOT BUILD A SMARTER VERSION.** Greedy-online captures 98% of the offline
   order-free heuristic. Retro-merging, demolition (#60), and global replanning
   are all chasing the last 2%.

**RUN `tools/target_value.py` BEFORE THE PREREG.** This cut sizes the mechanism;
it says nothing about whether the opponents a leg would be aimed at can pay for
it.

---

## 9. REPRODUCING THIS

```bash
.venv/bin/python tools/belt_merge_prize.py --versions 140 --controls
.venv/bin/python tools/belt_merge_prize.py --versions 104            # out-of-sample
.venv/bin/python tools/belt_merge_prize.py --versions 140 --json out.json
```

Inputs: `corpus/join.tsv`, `corpus/events.tsv`, `corpus/econ.tsv`, `maps/*.map26`.
Runtime ~2 min for 360 games (the PRIM arm dominates). Nothing is written outside
the `--json` path.
