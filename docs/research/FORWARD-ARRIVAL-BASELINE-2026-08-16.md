# FORWARD-ARRIVAL BASELINE — the number a live `bodyaware` leg has to move

**Written 2026-08-16T05:04:05Z** (`date -u`, same shell call). Repo git sha `821db857`.
**Corpus build:** `corpus/manifest.json` `built_utc = 2026-08-16T04:49:16Z`, 51,902 archived
replays, `join.tsv` 4,120 rows, join reconciliation `agree_rate = 1.0`.
**Population:** OUR RATED LADDER GAMES ONLY — the 4,115 archived replays that `join.tsv`
maps to one of our ladder matches (824 matches, 49 distinct opponents, **created
2026-08-07 .. 2026-08-16**). Every table below is us-only in that sense and says so.
**Scripts (scratchpad, session-local):** `fwd_arrival.py` (extract) · `fwd_analyse.py`
(cuts) · `fwd_extra.py` (geometry controls) · `fwd_leg.py` (leg cost) · `fwd_era.py`
(era-matched). Run on `.venv/bin/python` (repo venv; **no numpy — all fits are stdlib
3×3 Cramer**).

---

## SUMMARY — five lines

1. **The 3.3× does NOT reproduce as an arrival-TIME ratio.** The QUEUE #63 figure is a
   **lock-rate ratio** (builder-rounds in a 2-tile nav oscillation, ours 35.6% vs theirs
   10.9% on midgard, `BOOK-worst-maps-2026-08-14.md` §17) — *not* a time and not a
   distance. On forward-arrival latency the midgard penalty is **1.71× (median 89 vs 52
   rounds) / +22.1 rounds paired mean**, n=78 games. **1.71×, not 3.3×.**
2. **A same-order analogue DOES reproduce, and it is the same KIND of statistic (a rate
   ratio): our FAILURE-TO-ARRIVE rate on midgard is 3.75× theirs** — 19.2% [12.0, 29.3]
   vs 5.1% [2.0, 12.5], McNemar exact **p = 0.0192** on 4 us-only / 15 them-only
   discordant games. That is the honest correspondence: same map, same direction, same
   order of magnitude, **different quantity**.
3. **It is MIDGARD, not "long maps", and not even the whole #63 segment.** midgard
   +22.14 rounds (opponent-clustered sign-flip **p = 0.0176**); **ragnarok +5.80,
   p = 0.3334 — null**; the two-map segment +14.18, p = 0.0144, carried by midgard alone.
4. **The map-AREA cut requested in the brief is the wrong axis and returns a NULL** —
   area ≥900: **+1.77 rounds, p = 0.7551**. Its own same-size control
   {valkyrie, glacierkeep} runs the **OTHER WAY** (−11.21 rounds, we are FASTER,
   p = 0.0365). The `#63` row already warned against the 900-area class; this measures it.
5. **Censoring (no forward build all game, d ≤ D/3): US 14.5% (597/4,115), THEM 21.9%
   (900/4,115) pooled** — but on midgard it INVERTS to US 19.2% / THEM 5.1%. Nothing is
   imputed and nothing is dropped; censored games are carried as +∞ and the median is
   reported only where arrival >50%.

**POOLED, WE ARE THE FASTER SIDE.** Across all 4,115 paired games our median `t_forward`
is **31 vs their 46 rounds (0.67×)**, paired mean **−17.03 rounds** (sign-flip
permutation: **p < 0.0001** clustered at MATCH, **p = 0.0434** clustered at OPPONENT — the
conservative one still excludes zero). The
midgard penalty is a **local reversal of a global advantage**, and that is the shape a
live leg must be designed around.

---

## 1. METHOD, AND THE ONE PIECE THAT HAD TO BE DERIVED

`corpus/events.tsv` carries **`BUILD` and `DEATH` only** (6,795,311 + 2,028,030 rows;
verified `cut -f2 | sort | uniq -c`). There are no per-round unit positions, so a
*stall rate* is not measurable here and none is claimed. **Forward-arrival latency is a
proxy for the same underlying quantity — how long it takes a builder to get somewhere —
and it is measurable because a BUILD is positional evidence that a body arrived.**

**TRAP 1 (`corpus-howto.md`) — team index.** `join.tsv.our_team` is the only thing that
says which replay-internal team index is ours. It is used everywhere below; team 0 is
**never** assumed to be us. Control C4 tests it behaviourally (§5).

**TRAP 7 — `seat`.** The winner-derived seat column is **not used anywhere in this
document.** (In the current build the column is named `winner_seat`, which is at least
honestly named; it is still unused here.)

### Threshold, and why it is derived rather than chosen

`d2_enemy` is a squared distance in *tiles*, so a fixed cut-off would mean something
different on a 16×16 and a 30×30 map. I recover the **actual core-to-core separation `D`
per replay file** and express the threshold as a fraction of it.

**Recovery is exact, not fitted.** For any build at `(x,y)`,
`d2_own − x² − y² = −2a·x − 2b·y + (a²+b²)` is **linear in x and y**, so three
non-collinear builds determine the own-core reference tile `(a,b)` exactly; the same
system on `d2_enemy` gives the enemy core. Both teams' rows give two independent
estimates of each core.

* **max least-squares residual across all 4,115 files: 0.0. Median: 0.0.**
* **Disagreement between the two independent estimates of the same core: 0.0 in
  8,230 of 8,230 rows.**
* `D²` takes only **16 distinct values** in the whole pool — separation is a property of
  the map, and the recovered values line up one-to-one with map names (§3).

**PRIMARY THRESHOLD: a build is FORWARD iff `d2_enemy ≤ D²/9`, i.e. within `D/3` of the
enemy core** — the "nearer third of the approach". `t_forward` is the round of a team's
first such build. Sensitivity at `D/2` (midline) and `D/4` (doorstep) is in §6; the
midgard sign and rough magnitude survive all three.

**Censoring.** A team with no forward build all game is **censored, not dropped and not
imputed**. Medians are taken over the full distribution with censored = +∞, which is
well defined whenever arrival >50% and is printed as `None` otherwise (that is why
`fjordgate`'s opponent median reads `None` — they arrive in only 45.0% of games there).
Observed-only medians are printed alongside for transparency and are **biased optimistic
by construction**.

**Administrative censoring is shared.** A game that ends at r70 truncates BOTH sides
identically. The paired within-game design absorbs it exactly; the marginal medians do
not, which is a further reason the paired difference is the primary statistic.

---

## 2. CUT 1 — US vs OPPONENT, PAIRED WITHIN GAME

*Population: our rated ladder games, 2026-08-07..2026-08-16, n = 4,115 paired games
(both sides present in 4,115 of 4,115 files). Threshold d ≤ D/3.*

| | US | THEM |
|---|---|---|
| arrive at all | **85.5%** (3,518/4,115) | **78.1%** (3,215/4,115) |
| censored (never forward) | **14.5%** (597) | **21.9%** (900) |
| median `t_forward` (censored=+∞) | **31** | **46** |
| median, observed only | 27.0 | 33 |
| deepest build by r150, as fraction of `D` | **0.143** | 0.222 |
| deepest build by r250 | **0.132** | 0.202 |
| deepest build, end of game | **0.125** | 0.182 |

Discordant games: **770 we-arrive-they-don't vs 467 the reverse** (McNemar exact
p < 0.0001).

**Paired difference (2,748 games where both arrived): median −5.0 rounds.**
* match-clustered mean **−21.64 ± 6.68** (k = 811 matches; measured ICC 0.289,
  **DEFF 1.69**)
* opponent-clustered mean **−17.53 ± 16.54** (k = 47 opponents) — still excludes zero
* sign-flip permutation, 20,000 reps: **p < 0.0001** clustered at MATCH,
  **p = 0.0434** clustered at OPPONENT

**⇒ Does "3.3×" reproduce? NO, in every unit in which it could be read.**
* **as a ratio of times:** pooled **0.67× in our FAVOUR**; midgard **1.71×** against us.
* **as a ratio of depths:** pooled we finish **0.125·D** from their core against their
  **0.182·D** — again in our favour.
* **as a ratio of failure rates:** pooled **0.66× in our favour**; **midgard 3.75×
  against us** — the only cell where anything of that magnitude exists.

---

## 3. CUT 2 — BY MAP AREA, AND WHY IT IS THE WRONG AXIS

*Same population. `mw*mh` from `events.tsv`.*

| area class | n games | arrive US | arrive THEM | median tf US | THEM | ratio | paired mean (match-clustered) | sign-flip p (**opponent**-clustered) |
|---|---|---|---|---|---|---|---|---|
| small ≤196 | 442 | 72.2% | 56.3% | 55.5 | 191.5 | **0.29** | −17.38 ± 24.52 | 0.5363 |
| mid 197–899 | 3,319 | 86.5% | 80.1% | 28 | 41 | **0.68** | −23.67 ± 6.74 | 0.0276 |
| large ≥900 | 354 | 92.4% | 86.7% | 44.0 | 50.0 | **0.88** | **+2.45 ± 8.58** | **0.7551** |

*(All p above are Monte-Carlo over 20,000 sign flips; re-running under a different seed
moves them by ≲0.006 — e.g. the large cell reads 0.7551/0.7551 on two seeds.)*

**The large-map cell is a NULL.** If "long maps" meant "area ≥900", QUEUE #63 would be
refuted outright. It does not: the row's own segment note says *"explicitly NOT
900-area: valkyrie and glacierkeep read 77%/73% and are among our BEST cells despite
being the same size."* **That is now measured rather than asserted** — see §4.

### Cut 2b — by recovered core separation `D` (terciles)

| tercile | n | median tf US | THEM | ratio | paired median | paired mean (match-clustered) | opp-clustered p |
|---|---|---|---|---|---|---|---|
| short (D < 12.00) | 1,175 | 44 | 158 | 0.28 | −5.0 | −22.44 ± 16.79 | 0.1544 |
| mid (12.00 ≤ D < 19.80) | 1,411 | 25 | 32 | 0.78 | −3.0 | −8.54 ± 7.71 | 0.4268 |
| long (D ≥ 19.80) | 1,529 | 32 | 43 | 0.74 | −5.0 | −26.36 ± 6.83 | 0.0059 |

**Terciles also fail to isolate it** — the long tercile is dominated by the
`D = 19.80` maps (archipelago/jackpot/saga/snowflake, 896 games) where we are *faster*.

### Cut 2c — by exact separation (D² has only 16 values; cells with n ≥ 30)

| D | n | maps | arrive US | arrive THEM | tf US | tf THEM | ratio | paired median |
|---|---|---|---|---|---|---|---|---|
| **33.94** | **151** | **midgard, ragnarok** | 87.4% | 88.7% | **70** | **52** | **1.35** | **+6.0** |
| 31.24 | 62 | drakkarfjord | 95.2% | 91.9% | 46.5 | 58.0 | 0.80 | −0.5 |
| 25.50 | 205 | hive | 92.2% | 90.7% | 33 | 42 | 0.79 | −8.5 |
| 24.00 | 141 | glacierkeep, valkyrie | 96.5% | 82.3% | 32 | 37 | 0.86 | −3.0 |
| 21.26 | 74 | icefloe | 100.0% | 94.6% | 32.0 | 36.5 | 0.88 | −2.5 |
| 19.80 | 896 | archipelago, jackpot, saga, snowflake | 94.6% | 89.6% | 28.0 | 40.0 | 0.70 | −7.0 |
| 18.38 | 266 | drumlin | 93.2% | 92.1% | 27.0 | 27.5 | 0.98 | −2.0 |
| 16.97 | 207 | atoll | 96.1% | 89.4% | 20 | 29 | 0.69 | −4.0 |
| 16.00 | 64 | auroraveil | 87.5% | 79.7% | 30.0 | 62.0 | 0.48 | −19.5 |
| 14.00 | 210 | frostgate, royale, yulerune | 94.8% | 77.6% | 26.0 | 44.0 | 0.59 | −9.5 |
| 12.00 | 664 | eider, heart, nordkap | 73.9% | 77.0% | 32.5 | 26.0 | 1.25 | +0.5 |
| 11.31 | 218 | lighthouse | 77.1% | 66.1% | 33.5 | 99.0 | 0.34 | −10.5 |
| 9.00 | 193 | moonrise | 76.2% | 71.0% | 55 | 41 | 1.34 | −1.0 |
| 8.00 | 297 | antler | 84.2% | 62.0% | 21 | 110 | 0.19 | −2.0 |
| 7.00 | 218 | meander | 68.8% | 53.7% | 86.0 | 405.5 | 0.21 | −5.0 |
| 5.66 | 249 | fjordgate | 69.1% | 45.0% | 56 | *censored* | n/a | −24.0 |

**Separation is monotone in nothing.** The only cell where we are meaningfully slower
than the opponent we are playing is the top row, and one of its two maps carries it.

---

## 4. THE FINDING — IT IS MIDGARD, AND IT SURVIVES OPPONENT CONTROL

*Sign-flip permutation, 20,000 reps, clustering the flip at OPPONENT (see §5 for why
the MATCH cluster is dead inside a map cell and the OPPONENT cluster is not).*

| cut | n games | paired | k_opp | arrive US | arrive THEM | mean diff (rounds) | median | p |
|---|---|---|---|---|---|---|---|---|
| **midgard** | 78 | 59 | 20 | **80.8%** | **94.9%** | **+22.14** | +20.0 | **0.0176** |
| ragnarok | 73 | 56 | 19 | 94.5% | 82.2% | +5.80 | −1.0 | 0.3334 |
| segment {midgard, ragnarok} | 151 | 115 | 23 | 87.4% | 88.7% | +14.18 | +6.0 | 0.0144 |
| **CTRL900 {valkyrie, glacierkeep}** | 141 | 111 | 24 | 96.5% | 82.3% | **−11.21** | −3.0 | **0.0365** |
| off-segment (new pool) | 994 | 766 | 32 | 94.2% | 82.4% | −13.58 | −5.0 | 0.0480 |
| area ≥900 (new pool) | 354 | 280 | 28 | 92.4% | 86.7% | +1.77 | +1.0 | 0.7551 |

**Failure-to-arrive rate — the statistic that is formally comparable to a lock RATE ratio:**

| cut | n | US never forward | THEM never forward | **ratio** | discordant us-only/them-only | McNemar exact p |
|---|---|---|---|---|---|---|
| ALL | 4,115 | 14.5% [13.5, 15.6] | 21.9% [20.6, 23.2] | 0.66× | 770 / 467 | <0.0001 |
| **midgard** | 78 | **19.2% [12.0, 29.3]** | **5.1% [2.0, 12.5]** | **3.75×** | 4 / 15 | **0.0192** |
| ragnarok | 73 | 5.5% [2.2, 13.3] | 17.8% [10.7, 28.1] | 0.31× | 13 / 4 | 0.0490 |
| segment | 151 | 12.6% [8.2, 18.8] | 11.3% [7.1, 17.3] | 1.12× | 17 / 19 | 0.8679 |
| CTRL900 | 141 | 3.5% [1.5, 8.0] | 17.7% [12.3, 24.9] | 0.20× | 25 / 5 | 0.0003 |
| area ≥900 | 354 | 7.6% [5.3, 10.9] | 13.3% [10.1, 17.2] | 0.57× | 47 / 27 | 0.0265 |

(Wilson intervals, naive — see §5 for the DEFF enumeration that licenses that.)

**⇒ 3.3× (lock rate) vs 3.75× (failure-to-arrive rate) on the same map. MEASURED as a
convergence of two rate ratios; INFERRED, not measured, that they share a mechanism** —
`events.tsv` has no positions, so nothing here can show a locked builder failing to
arrive. That link is exactly what a live leg would buy.

**⚠ ragnarok breaks the segment.** It is slower on time (+5.80, null) while *better* on
failure rate (0.31×, we fail less). **Treating {midgard, ragnarok} as one segment
averages a real effect with a null and halves the dose** — 14.18 rounds instead of 22.14.

### Is it the map or the opponent mix? Difference-in-differences

Per opponent, (paired diff on midgard) − (paired diff off midgard), **both arms
restricted to the post-2026-08-13 pool so era is matched** (see §7 — every midgard game
in the archive is from 08-13 onward):

| opponent | n_mid | n_off | DiD (rounds) |
|---|---|---|---|
| team lazy | 4 | 64 | +82.80 |
| Erebus | 4 | 45 | +55.15 |
| Coreflood | 5 | 41 | +49.42 |
| LingLing40 | 3 | 23 | +45.04 |
| kladde chatte tville (och oss) | 2 | 18 | +44.44 |
| lingling_40h | 5 | 35 | +42.80 |
| arsonist duck | 5 | 60 | +33.10 |
| 0033 | 4 | 71 | +29.18 |
| Juusto | 2 | 39 | +24.45 |
| HTTP 418 | 7 | 53 | +22.04 |
| diverge | 5 | 54 | +20.41 |
| gsxWins | 2 | 42 | +16.02 |
| Jython | 3 | 47 | −7.86 |
| Big O | 2 | 63 | −18.60 |

**MEAN DiD +31.31 ± 13.44 rounds (k = 14 opponents, excludes zero); 12 of 14 opponents
slower-on-midgard.** The penalty is **not** an opponent-mix artefact: it appears
*within* opponents, against the same bots we out-arrive everywhere else.

---

## 5. CONTROLS — every one had to be able to come out the other way

**C1 — geometry against ground truth.** A dying core emits a `DEATH` row carrying its own
`d2_enemy`, which IS `D²`. Fitted `D²` vs that value: **3,554 core deaths, exact match
3,554/3,554 (100.0000%), max |error| 0.**

**C1b — CORRUPT-INPUT, because a zero residual is a constant column and a constant
column validates anything (`corpus-howto.md` TRAP 8).** On 80 (file, team) cells:

| input | max residual: min / median / max | cells with resid > 0 |
|---|---|---|
| clean | 0 / 0 / 0 | 0/80 (expected) |
| `d2` column shuffled within the cell | 16.88 / 196.73 / 1160.59 | **80/80** |
| **one build displaced by exactly one tile** | 0.774 / 0.978 / 4.938 | **80/80** |

**The fit detects a ONE-TILE error in a single build out of hundreds. The zero is a
verdict, not a dead column.**

**C2 — LABEL SHUFFLE (the primary "must come out the other way").** Randomising which
side is "us", 200 reps:

| statistic | observed | shuffled mean | shuffled range |
|---|---|---|---|
| paired median diff, all games | **−5.0** | +0.018 | [−1.0, +1.0] |
| median ratio us/them, all games | **0.674** | 1.003 | [0.921, 1.086] |
| paired median diff, segment | **+6.0** | −0.150 | [−7.0, +7.0] |

**It collapses to zero, and it collapses to zero in the RATIO too.** ⚠ **Honest caveat:
the segment's +6.0 sits INSIDE the shuffle envelope at n=151** — which is why the segment
verdict in §4 rests on the clustered permutation (p = 0.0144) and on the DiD, not on the
median.

**C3 — a metric that CANNOT differ between the two teams, plus its complement.**

* game length (`turns`), paired diff: **min 0, max 0, mean 0.000000** — flat, as it must be.
* same pipeline, builds/game (a metric that CAN differ): **median +8.0, mean +12.18** —
  **not** flat.

**Both verdicts observed. A pipeline that returned 0 for everything would be caught here.**

**C4 — is `join.tsv.our_team` actually us?** (TRAP 7 says winner-derived columns must be
checked *behaviourally*, and cross-checking `our_team` against `won`/`us_side` is
circular because they descend from the same `winnerSide`.) Per game, pooled over 4,115
games:

| entity | US /game | THEM /game | ratio |
|---|---|---|---|
| gunner | **1.36** | **5.27** | **0.26** |
| sentinel | 3.26 | 2.12 | 1.54 |
| conveyor | 41.49 | 30.63 | 1.35 |
| barrier | 4.02 | 2.52 | 1.60 |
| harvester | 6.69 | 5.34 | 1.25 |
| builder bot | 9.27 | 8.08 | 1.15 |
| launcher | 0.72 | 0.68 | 1.06 |

**The gunner column is the fingerprint and it is unambiguous.** Our line is documented as
gunner-poor (QUEUE #25: *"Lorem Ipsum … 11.64 gunners (6.3× ours)"*; #67: field baseline
2.20 gunners/game) and the US side reads **1.36 vs the field's 5.27**. A coin-flip
`our_team` would return ≈1.00 on every row. It does not. **⚠ The launcher ratio (1.06×)
would have been a WEAK check on its own — recorded so nobody reuses it.**

**C5 — dead-column sweep on every field consumed.** `D2` 16 distinct · `nbuild` 303 ·
`turns` 651 · `deep_end` 116 · `tf_third` 406 (6,733 non-null) · `tf_half` 308 ·
`tf_quarter` 451 · `n_launcher` 25 · `n_conveyor` 246.
**⛔ TWO CONSTANT COLUMNS, SAID LOUDLY: `resid` and `disag` are identically 0.0 in
8,230 of 8,230 rows.** They are diagnostics of the geometry fit, not evidence, and
**C1b is the reason their zero is allowed to mean anything.** No claim in this document
rests on either.

**Design-effect enumeration.** Clusters present: **MATCH** and **OPPONENT**.
* Games per match: **min 1, max 5, mean 4.99** over 824 matches — the MATCH cluster is
  real in a pooled cut.
* **(match, map) cells holding more than one game: 0 of 4,115** ⇒ **inside a per-map cell
  the MATCH cluster DIES** (a 5-game match uses 5 different maps — the `CLAUDE.md` worked
  example, reproduced here on this pool).
* **(opponent, map) cells holding more than one game: 598 of 752, mean 5.47 games/cell**
  ⇒ **the OPPONENT cluster SURVIVES.** All per-map inference above is therefore clustered
  at OPPONENT, never naive.
* For the POOLED paired contrast I report the **measured** ICC rather than importing a
  constant: ICC 0.289, **DEFF 1.69** at the match level; the opponent-clustered mean is
  given beside it and is the conservative one.
* ⚠ **The `CLAUDE.md` platform constants (1.529 rated / 1.366 within-opponent) are NOT
  applied here.** They are design effects for *game-outcome shares*. This is a
  **within-game paired** contrast in which both sides come from the same game, so the
  shared-game component of the correlation is differenced out by construction; the
  residual clustering is what I measured above. Importing the outcome-share constant on
  top of that would double-count.
* ⚠ **Direction check (`CLAUDE.md` "fail-to-exclude" clause).** The two claims stated as
  nulls — **area ≥900 (p = 0.7551)** and **ragnarok (p = 0.3334)** — are fail-to-exclude
  claims and are therefore the ones a wider interval would flatter. Restated as
  exclusions: **the area ≥900 cell EXCLUDES a penalty as large as midgard's** (raw paired
  mean +1.77; match-clustered **+2.45 ± 8.58**, opponent-clustered **+2.11 ± 23.31** — the
  +22.14 midgard effect is outside the match-clustered band and at the edge of the far
  wider opponent-clustered one at k=28), and **ragnarok
  EXCLUDES it too** (+5.80, opponent-clustered ±14.78). Those exclusions are what the
  document banks; "no effect at all" is **not** claimed for either.

---

## 6. THRESHOLD SENSITIVITY

*All paired games / segment {midgard, ragnarok}.*

| threshold | ALL arrive US/THEM | ALL tf US/THEM | ALL ratio | ALL paired med | SEG arrive US/THEM | SEG tf US/THEM | SEG ratio | SEG paired med |
|---|---|---|---|---|---|---|---|---|
| d ≤ D/4 | 78.2% / 65.4% | 40 / 89 | 0.45 | −7 | 87.4% / 87.4% | 70 / 53 | 1.32 | +5 |
| **d ≤ D/3** | 85.5% / 78.1% | 31 / 46 | **0.67** | **−5.0** | 87.4% / 88.7% | 70 / 52 | **1.35** | **+6** |
| d ≤ D/2 | 93.6% / 91.3% | 24 / 27 | 0.89 | −2 | 92.1% / 95.4% | 61 / 48 | 1.27 | +9.5 |

**The sign is stable in every cell at every threshold**; only the magnitude moves, in the
expected direction (a laxer threshold compresses both sides toward the early game).

---

## 7. CUT 3 — BY ERA (`join.tsv.ourver`), AND THE POOL BREAK THAT SITS ON TOP OF IT

⛔ **THE MAP POOL CHANGED ON 2026-08-13 AND IT IS COLLINEAR WITH THE VERSIONS ASKED FOR.**
Ten maps — **auroraveil, drakkarfjord, frostgate, glacierkeep, icefloe, midgard,
ragnarok, royale, valkyrie, yulerune** — appear **only** in games created on/after
2026-08-13; **zero** maps are old-pool-only. **All 78 midgard games in the entire archive
are from 2026-08-13..2026-08-16.** Every version cell below (v125/v139/v140/v152) also
lies entirely inside the new pool, so version and pool do not confound *each other* —
but neither can be separated from "the era in which midgard exists at all".

*All cells below are new-pool; cells under n = 30 games are refused outright.*

| ourver | n games | paired | arrive US | arrive THEM | tf US | tf THEM | ratio | mean diff | opp-clustered p |
|---|---|---|---|---|---|---|---|---|---|
| v125 | 305 | 226 | 92.1% | 81.3% | 32 | 43 | 0.74 | +4.73 | 0.5774 |
| **v139** | **40** | 33 | 92.5% | 90.0% | 27.5 | 36.0 | 0.76 | +1.91 | 0.8445 |
| v140 | 360 | 287 | 96.1% | 83.6% | 27.0 | 45.0 | 0.60 | **−14.92** | **0.0277** |
| v152 | 155 | 133 | 99.4% | 86.5% | 28 | 41 | 0.68 | **−28.08** | **0.0059** |

**The pooled arrival trend is monotone and it is ours:** our failure-to-arrive rate falls
**v125 7.9% → v140 3.9% → v152 0.6%**, while the opponents' sits flat at 18.7% / 16.4% /
13.5%. **By v152 we effectively always get forward** (1 censored game in 155).
⚠ **v139 (n = 40) is reported but is a thin cell** — it clears the n ≥ 30 bar by 10 games
and its interval spans everything; read it as "not inconsistent", never as a point.

**Era × segment:**

| cell | n | paired | arrive US | arrive THEM | tf US | tf THEM | ratio | mean diff | median | p |
|---|---|---|---|---|---|---|---|---|---|---|
| v125 × {midgard, ragnarok} | 46 | 37 | 87.0% | 93.5% | 87.5 | 46.5 | **1.88** | **+25.22** | +35.0 | **0.0139** |
| v140 × {midgard, ragnarok} | 53 | 37 | 86.8% | 83.0% | 76 | 53 | **1.43** | +16.08 | +6.0 | 0.0626 |
| v139 × segment | 8 | — | — | — | — | — | — | — | — | **REFUSED (n<30)** |
| v152 × segment | 20 | — | — | — | — | — | — | — | — | **REFUSED (n<30)** |

**The segment penalty is present in v125 and weaker-but-not-excluded in v140, and the
version that fixed everything else (v152) HAS NO SEGMENT DATA.** That is the single
biggest hole in this baseline and it is a hole a live leg fills directly.

---

## 8. WHAT A LIVE LEG WOULD HAVE TO MOVE, AND WHAT IT WOULD COST

**BASELINE TO BEAT — midgard, our rated ladder games, 2026-08-13..2026-08-16:**

```
n = 78 games (59 with both sides arriving), 20 distinct opponents
paired t_forward difference   mean +22.14   median +20.0   sd 53.1 rounds
arrival share                 US 80.8%   THEM 94.9%
failure-to-arrive ratio       3.75x   (15/78 vs 4/78)
depth at end (frac of D)      US 0.059   THEM 0.066   <- NOTE: we finish DEEPER, just later
```

**⭐ THE MOST DECISION-RELEVANT NUMBER: +22.14 rounds, the paired midgard arrival gap
(n = 59 paired games, 20 opponents, opponent-clustered sign-flip p = 0.0176; era-matched
per-opponent DiD +31.31 ± 13.44).** That is what `bodyaware` has to erase.

**Power, on the naive-plus-per-map-DEFF band (DEFF ≈ 1.07, the `CLAUDE.md` per-map value,
consistent with the cluster enumeration in §5):**

| effect to detect | delta | n paired midgard games, 80% power / 5% two-sided | ×1.07 DEFF |
|---|---|---|---|
| close the whole gap | +22.1 rounds | 45 | **48** |
| halve the gap | +11.1 rounds | 181 | **193** |

⛔ **AND HERE IS THE COST, WHICH IS THE REAL FINDING FOR THE FIRE ORDER: the map is not
selectable, so those 48 games are 48/0.0678 ≈ 710 GAMES.** Midgard is **6.78% of the
new-pool rated ladder (78 of 1,150 games created ≥2026-08-13)** and **1.44% all-time
(78 of 5,425)**. At **5 games per unrated match** that is **~142 matches**, and at the
platform's **5 matches / 20 minutes** that is **~9.5 hours of continuous window** for the
whole-gap read — and **~38 hours** for the halve-the-gap read.

**Three ways out, in cost order — none of which this document can choose between:**
1. **Score the LOCAL board on midgard specifically.** The `bodyaware` local screen already
   holds n = 10,801 (53.70% vs control); a map-restricted re-read costs zero games and is
   the natural first move, but per point 6 of the programme a local screen **prioritises**
   and cannot **close**.
2. **Widen the dial from midgard to "arrival gap anywhere it is positive".** Off-midgard
   we are already the faster side, so this is a *non-regression* dial, not a treatment
   dial — and non-regression is a fail-to-exclude claim that must be restated as an
   exclusion before it is banked (§5).
3. **Accept ~710 games.** Free, per the standing directive, but it is 9.5 hours of window.

---

## 9. LIMITS — what is MEASURED and what is INFERRED

**MEASURED here:**
* Core positions and separation per replay (exact, residual 0, validated against 3,554
  core-death rows and against two corruption tests).
* `t_forward` and build depth per team per game, and their paired within-game contrast.
* Arrival and censoring rates, with Wilson intervals and exact McNemar on discordant pairs.
* The map-area null, the CTRL900 reversal, the era trend, the map-pool break.

**INFERRED, NOT MEASURED:**
* **That the arrival gap is caused by nav locks.** `events.tsv` carries BUILD and DEATH
  only — **no positions, no cooldowns, no moves** — so *no stall or lock rate exists in
  this document*, and the 3.75× failure ratio is only *consistent with* the 3.3× lock
  ratio. Same map, same sign, same order; **different instrument, different quantity.**
* **That `bodyaware` would move it.** Nothing here touches the plank. This is a baseline.

**FURTHER LIMITS:**
* **Us-only, rated-only.** 4,115 games are OUR ladder games. `join.tsv` maps only 4,120
  of 51,902 archived replays; the other 47,782 are unrated and other teams' games and are
  **not** in any table here. Per `corpus-howto.md` TRAP 4, "the opponent does X" always
  means "against us, in N archived games" — every N is printed.
* **The opponent's version is not pinned or read in this cut.** `join.tsv.oppver` exists
  but was not used; opponents shipped freely across the 9-day window and the DiD absorbs
  only their *average* level, not their timeline. A treatment leg must pin
  (`fcode match unrated <team> --match <past_match_id>`).
* **midgard n = 78 games / 20 opponents / 4 days.** The DiD rests on opponents with as
  few as 2 midgard games each. This is a *prioritising* baseline, not a closing one.
* **The two-map segment is not homogeneous** (§4). Any prereg that writes
  `SEGMENT: {midgard, ragnarok}` is buying a diluted dose; midgard is the cell with the
  effect.
* **`t_forward` is bounded by game length**, and our games are shorter than the pool
  median on the segment (184 vs 208 turns). The pairing removes this exactly for the
  paired difference; it does **not** remove it from the marginal medians, which is why the
  paired difference is primary throughout.
* **A build at `d2_enemy == 0`** (on the enemy core's own tile) occurs in 4 of 4,115 games
  and **all 4 are `cond == core_destroyed`** — i.e. the tile freed up after the kill. It
  affects only the `deep_end` column and never `t_forward`.
* **`fjordgate`'s opponent median is `None`, not missing data** — their arrival rate there
  is 45.0%, below 50%, so the censored median is genuinely undefined. Printing a number
  there would require imputation and none was done.
