# The LOKI arsenal, priced: one item verified, two opportunities that are far larger than we thought, three refutations

**Research arm, session 24, 2026-08-09.** Six candidate tricks for the LOKI line,
priced against **what real opponents actually do** in the 1,355 attributed ladder
games — not against the probe pool, which is dominated 87–90% by construction and
answers a different question.

**Version tag:** live **v92 "Eir dodge"** = `bots/_v115dodge`, py-tree md5
`54f5f746`, baseline **1562 @ 537, rank #31** (`elo_history.tsv`, 15:11 CEST).
Repo `25933f2`. Programme: `LINE: loki`, `PRIMARY_CURRENCY: core_kill_share`,
`KILL_WINDOW_RND: 250`.

**Corpus only. Zero replay downloads. Zero engine runs.**
Decoder: `docs/research/scripts/arsenal-2026-08-09/arsenal_decode.py` —
`dwell_decode.py` plus **seven documented additions** (§0.2) — **1,355 files,
0 errors, 34 s.**

---

## 0. Validation, because every number below rests on a reconstructed board

### 0.1 Inputs were FROZEN before the run

The keeper daemon appends live and grew `join.tsv` mid-run for two other agents
today, so the eight corpus tables were copied to a scratch directory **before any
analysis** and every number here reads that copy.

| frozen file | rows | md5 |
| --- | ---: | --- |
| `join.tsv` | 1,356 (1,355 + header) | `f3bc78bc58cc7682cf734c202620fe65` |
| `builds.tsv` | 84,454 | `7730f6b7b2424f493cb30ffae8746170` |
| `build_agg.tsv` | 135,936 | `5cf5e9eeeae0456e8347e05ba1af5105` |
| `econ.tsv` | 33,673 | `6bd71f9bd19c1f5b733e8521daec36ea` |
| `flow.tsv` | 61,867 | `44727ad1842a05a0b67f1c1f7a592a42` |
| `throws.tsv` | 90,478 | `fd68e6aef4767e14b2a3ba2bebe99b57` |
| `ladder_games.tsv` | 2,626 | `4f271033824b1d1b047b7292828dfd45` |
| `league_matches.tsv` | 27,074 | `f1610459534b6e61ce38d36f5549faed` |

Frozen **2026-08-09 14:54:25 CEST**. Archive at that moment: 6,791 `.replay26`
files, of which the 1,355 in `join.tsv` are attributed ladder games
(**2,710 team-sides**).

### 0.2 What was extended, and what was reused

Per the standing rule, I extended a preserved decoder rather than writing a new
one. The base is
`docs/research/scripts/side-lane-2026-08-09/dwell_decode.py`. **Reused verbatim:**
the board tracker (`placeEntity` with the rotate-re-emit guard, `moveBuilderBot`,
`removeEntity`, the two's-complement `updateHp` varint), the `ray()` envelope
geometry, the map/wall decode, and the multiprocessing driver. **Seven additions:**

1. **A1** — turret ray cover for **both** teams (dwell tracked only the enemy's),
   plus the **live blocked gunner line**.
2. **A2** — core-ring occupancy per team per round: the 12-tile Chebyshev-1 spawn
   ring (`CORE_SPAWNING_RADIUS_SQ = 2`) and the 8-tile orthogonal sub-ring, split
   by own-building / own-body / hostile-building / hostile-body, **and classified
   by what kind of thing is standing there**.
3. **A3** — map **ore tiles** (dwell needed only WALL), harvester build positions,
   ore side-of-map.
4. **A4** — the kidnap opportunity scan for rounds < 250.
5. **A5** — travel/reachability milestones from **observed builder positions**.
6. **A6** — `distributeResources` moves classified live, then tested against the
   tiles the opposing team's builders had **already** reached by that round.
7. **A7** — live unit count per team, so the 50-unit cap is excludable as a
   confounder in the spawn read.

### 0.3 Ten checks, run before any table was read

| check | result |
| --- | --- |
| V1 12-tile ring is exactly 12 tiles | **1,355 / 1,355 files** |
| V2 orthogonal sub-ring is exactly 8 tiles | **1,355 / 1,355** |
| V3 builders standing ON a core footprint tile (must be 0) | **0** |
| V4 throws detected | 31,569 |
| V5 a live launcher within **d²≤2** of the pre-throw tile | **31,569 / 31,569 = 100.000%** |
| V6 …and the landing tile within **d²≤26** of that launcher | **31,569 / 31,569 = 100.000%** |
| V7 stacks into a core × 10 == `econ.ti_collected_end` | **2,710 / 2,710 = 100.0000%** |
| V8 harvester builds == `build_agg.build_harvester` | **2,615 / 2,615 sides** |
| V9 builder spawns == `build_agg.build_builder_bot` | **2,710 / 2,710 sides** |
| V10 throw count == `corpus/throws.tsv` rows | 960 / 968 files |

**V5/V6 are load-bearing and they are exact.** They are the *first direct
measurement* in this repo of the launcher's two ranges: pickup is Chebyshev-1
(d²≤2) and the throw reaches d²≤26, on 31,569 real throws with zero exceptions.
Items 2 and 3 are built on that geometry.

**V7 failed at first, at 99.30%, and the failure was worth more than the check.**
My initial classifier credited a delivery to the team that *pushed* it. The engine
credits it to whoever **owns the destination core**: in
`13fc7fef…_game_2`, a *team-1* conveyor at (2,1) fed *team-0*'s core 148 times —
1,480 Ti donated to the enemy. Once the receiver is credited, the identity is
exact at 2,710/2,710. **A silent 0.7% gap named a real mechanic**; it is §6.

**V10 is the one non-exact check and I know why.** My throw detector fires on
Chebyshev > 1; `replay_throws.py` also counts a **diagonally adjacent**
displacement (a real throw, since builders move only cardinally). 8 of 968 files
differ, all in the direction of me under-counting, **76 of 31,645 throws
(0.24%)**. Throws are used only for V5/V6 validation, where an under-count cannot
create a false pass.

### 0.4 Rules taken as given, and one I re-derived

Taken as given from this session's probes: the core is one 2×2 entity with 12
Chebyshev-1 ring tiles of which 8 are orthogonal; build legality is stricter than
`is_tile_empty`; turret fire hits whatever unit stands on the target tile.
**Re-derived here from the engine source** rather than trusted:
`LAUNCHER_VISION_RADIUS_SQ = 26` and `CORE_SPAWNING_RADIUS_SQ = 2`
(`.venv/lib/python3.13/site-packages/fcode/_types.py:52,59`) — and both then
confirmed behaviourally by V6 and by §1.1.

---

## 1. THE FULL LOCK — the mechanism is confirmed at 4 million tile-rounds, and the configuration has never once occurred

### 1.1 What actually blocks a spawn — VERIFIED, and it is not what "occupied" suggests

Every ring tile, every round, classified by what stood on it at the **start** of
the round, against whether a builder spawned onto it that round. **16,368,264
ring-tile-rounds, 31,913 spawns.**

| ring tile occupant | tile-rounds | spawns onto it | per 1k |
| --- | ---: | ---: | ---: |
| EMPTY | 5,801,262 | 19,129 | **3.297** |
| own conveyor / splitter | 6,260,776 | 12,229 | **1.953** |
| **enemy** conveyor / splitter | 299,242 | 555 | **1.855** |
| own builder bot | 2,010,634 | 0 | **0.000** |
| **enemy builder bot** | **394,970** | **0** | **0.000** |
| wall / off-map | 538,048 | 0 | 0.000 |
| own gunner | 387,111 | 0 | 0.000 |
| own barrier | 201,139 | 0 | 0.000 |
| own launcher | 182,020 | 0 | 0.000 |
| own sentinel | 168,623 | 0 | 0.000 |
| enemy gunner | 102,698 | 0 | 0.000 |
| enemy barrier | 12,064 | 0 | 0.000 |
| enemy sentinel | 8,427 | 0 | 0.000 |
| enemy launcher | 1,250 | 0 | 0.000 |

**Zero-spawn classes pooled: 4,006,984 tile-rounds, 0 spawns.**

> **A BODY BLOCKS — 394,970 enemy-body tile-rounds and not one spawn.** This is
> the observational twin of the builder arm's live `_probe_jail` result today.
> Two independent instruments, one causal and one at scale, agree.
>
> **A CONVEYOR DOES NOT BLOCK, AND THIS IS THE PART THAT CHANGES THE DESIGN.**
> **12,784 of 31,913 spawns (40.1%) landed on a tile that already held a
> conveyor or splitter** — 555 of them on the *enemy's* conveyor. So "12 ring
> tiles occupied" is **not** a lock. A lock needs 12 tiles held by things a
> builder cannot stand on: bodies, barriers, harvesters, turrets, walls.

*Observational limit, stated:* zero spawns onto bodies is consistent with the
engine forbidding it **and** with bot logic never choosing it. The probe settles
causality; this table settles that it holds across the whole field at scale.

### 1.2 Has any core ever actually been ringed? — the honest answer is essentially no

Max **hostile** occupancy of the 12-tile ring, per team-side (n = 1,355 US +
1,355 THEM):

| ≥ k hostile ring tiles | US sides | | THEM sides | |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 932 | 68.78% | 627 | 46.27% |
| 3 | 266 | 19.63% | 227 | 16.75% |
| 6 | 23 | 1.70% | 62 | 4.58% |
| 8 | 5 | 0.37% | 25 | 1.85% |
| 10 | 1 | 0.07% | 10 | 0.74% |
| 12 | **0** | 0.00% | **1** | **0.07%** |

**Exactly one team-side of 2,710 ever had all 12 of its ring tiles held by the
enemy.** And splitting hostile occupancy by *what* was standing there:

| max hostile **bodies** on the 12-ring | sides | share |
| ---: | ---: | ---: |
| 0 | 1,246 | 45.98% |
| 1 | 1,016 | 37.49% |
| 2 | 360 | 13.28% |
| 3 | 65 | 2.40% |
| 4 | 18 | 0.66% |
| 5 | 1 | 0.04% |
| **6** | **4** | **0.15%** |

**The most bodies any team has ever had on an enemy ring is 6 of 12, four times
in 2,710 sides.** The high-occupancy cases in the first table are
**buildings**, not bodies — forward conveyor networks that grew up against an
enemy core over hundreds of rounds. The heal-and-delivery lock (all 8
orthogonals hostile) has happened **once**, on the THEM side.

### 1.3 What happened to those cores — ~~REFUTED~~ **CORRECTED: the original comparison was uncontrolled and its verdict is WITHDRAWN**

> ### ⚠ RETRACTION AND RE-CUT (same day, on the coordinator's catch)
>
> **Everything in §1.3a below is UNCONTROLLED and I no longer stand behind the
> verdict I drew from it.** The coordinator identified a selection effect I
> missed: **reaching high ring occupancy takes rounds — my own median lag is
> 168 — so a side cannot have been heavily ringed by r250 unless it survived
> long enough to be ringed.** The "died inside r250" cut therefore conditions on
> survival on the treated arm and not on the control arm. That is the shape this
> lane was burned by in s23, and it is exactly what happened here.
>
> **The numbers in §1.3a are left standing, marked, because they are correct as
> descriptions of the wrong quantity.** §1.3b–d are the conditioned re-cut.
> **The fast-kill inversion does NOT survive conditioning. It flips.**

#### 1.3a — THE ORIGINAL, UNCONTROLLED COMPARISON *(kept for the record; do not cite)*

All 30 team-sides that ever reached ≥8 hostile ring tiles, against the base rate:

| population | n | core died | inside r250 |
| --- | ---: | ---: | ---: |
| **sides reaching ≥8 hostile ring tiles** | 30 | 8 (**26.67%**) | 2 (**6.67%**) |
| all team-sides (base rate) | 2,710 | 952 (35.13%) | 527 (19.45%) |

**A heavily ringed core dies LESS often than an average core, and dies inside the
250-round kill window a third as often.** 24 of the 30 games ran the full 1,000
rounds. High ring occupancy in this corpus is a **marker of stalemate**, not of a
kill — it is what a forward economy pressed against a wall looks like after 300
rounds, and the median lag from first reaching ≥8 to core death, in the 8 cases
that died, is **168 rounds** — well outside the window.

The **bodies-only** cut is more encouraging and still not a kill path:

| max hostile bodies | sides | core died | died inside r250 |
| ---: | ---: | ---: | ---: |
| 0 | 1,246 | 31.54% | **23.68%** |
| 1 | 1,016 | 33.66% | 15.94% |
| 2 | 360 | 47.22% | 17.50% |
| 3 | 65 | 49.23% | 7.69% |
| 4 | 18 | 66.67% | 11.11% |
| 6 | 4 | 50.00% | 0.00% |

Bodies on the ring track **eventual** core death strongly (31.5% → 66.7%) and
**fast** core death inversely (23.7% → 7.7%). Sustained pressure is rare:
only **493 of 2,710 sides (18.2%)** ever spend a round at ≥3 hostile ring tiles,
and among those the median is **46 rounds**.

*(The "died inside r250" column above is the contaminated one. The eventual-death
column is not affected by the selection effect and survives the re-cut.)*

#### 1.3b — CONDITIONED ON *WHEN* THE RING WAS ACHIEVED

Same sides, split by the round at which they first reached k hostile ring tiles.
This is the table that exposes the artifact:

| k | achieved | n | core died | **died inside r250** | median lag to death |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3 | by r50 | 96 | 37.50% | 9.38% | 357 |
| 3 | by r100 | 90 | 38.89% | **27.78%** | 98 |
| 3 | by r150 | 60 | 56.67% | **31.67%** | 102 |
| 3 | by r200 | 56 | 51.79% | 16.07% | 149 |
| 3 | by r250 | 44 | 54.55% | 6.82% | 135 |
| 3 | **after r250** | **147** | 38.10% | **0.00%** | 48 |
| 4 | by r100 | 37 | 40.54% | **35.14%** | 49 |
| 4 | by r150 | 34 | 55.88% | **38.24%** | 94 |
| 4 | after r250 | 106 | 39.62% | 0.00% | 64 |

**There is the artifact, in one column.** For every k, the largest single bucket
is *"achieved after r250"* — 147 of 393 sides at k=3 — and those sides score
**0.00% died-inside-r250 by construction**, because you cannot die before r250
having first been ringed after it. The pooled §1.3a figure was mostly counting
that. **Against the 19.45% base rate, sides ringed to k=3 between r50 and r150
die inside r250 at 27.8–31.7%, and at k=4 at 35.1–38.2%.** Early ringing looks
*faster*, not slower.

#### 1.3c — ROUND-MATCHED CONTROL, BODIES ONLY

Treated = reached k hostile **bodies** by round R. Control = **alive at R, replay
runs past R, had not reached k by R.** Outcome is core death within 250 rounds
**of R**, so both arms run the same clock from the same instant; sides whose
replay ends before R+250 without a death are censored out of both arms.

| k | R | treated n | dead ≤R+250 | control n | dead ≤R+250 | ratio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 50 | 478 | 24.48% | 1,632 | 29.53% | **0.83** |
| 1 | 150 | 744 | 29.57% | 920 | 18.80% | **1.57** |
| 1 | 250 | 715 | 25.73% | 671 | 12.22% | **2.11** |
| 2 | 50 | 91 | 25.27% | 2,019 | 28.53% | 0.89 |
| 2 | 150 | 168 | 35.12% | 1,496 | 22.33% | 1.57 |
| 2 | 250 | 194 | 34.02% | 1,192 | 16.78% | **2.03** |
| 3 | 250 | 33 | 42.42% | 1,353 | 18.63% | **2.28** |
| 4 | 250 | 8 | 62.50% | 1,378 | 18.94% | 3.30 |

Matched, the direction is **positive and it strengthens with R** — roughly a
**2× ratio** by R=150–250. It is **null at R=50** (0.83–0.89), which is its own
finding: a body next to their core in the first 50 rounds predicts nothing,
because early adjacency is just a scout walking past.

#### 1.3d — THE PER-ROUND HAZARD — the quantity a bot can actually act on

Evaluated at **every round**, not once per game, so no selection effect can
reach it. Right-censored properly: a round contributes to horizon H only if the
death is observable within H (either it happened, or the replay runs H more
rounds); censored rounds are dropped from numerator **and** denominator rather
than being silently scored as survivals.

**P(this core dies within 25 rounds | hostile ring occupancy = j right now):**

| j | **rounds < 250** exposure | P(die ≤25) | 95% CI | | **all rounds** exposure | P(die ≤25) |
| ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 0 | 449,546 | **1.99%** | [1.95, 2.03] | | 1,028,929 | 1.28% |
| 1 | 59,405 | 4.14% | [3.98, 4.30] | | 142,478 | 3.44% |
| 2 | 22,172 | 5.81% | [5.51, 6.13] | | 58,893 | 4.67% |
| 3 | 9,332 | 5.48% | [5.03, 5.96] | | 35,792 | 4.01% |
| 4 | 3,421 | **8.07%** | [7.20, 9.03] | | 18,874 | 3.74% |
| 5 | 1,744 | 6.94% | [5.84, 8.23] | | 15,554 | 2.55% |
| 6 | 874 | 5.61% | [4.27, 7.33] | | 5,137 | 3.37% |
| 8 | 206 | **12.62%** | [8.76, 17.85] | | 3,040 | 2.57% |
| 11 | — | — | | | 1,491 | **0.00%** [0.00, 0.26] |

> **THE TWO COLUMNS POINT IN OPPOSITE DIRECTIONS, AND THAT IS THE WHOLE STORY.**
> Before r250, the hazard rises monotonically with ring occupancy: **1.99% → 8.07%
> at j=4, and 12.62% at j=8 — a 6.3× hazard ratio, CI-separated from the j=0
> cell.** Pooled over all rounds it *falls* above j=4 and reaches **exactly 0.00%
> at j=11 over 1,491 exposed rounds** — the stalemate signature. §1.3a averaged
> the two and reported the late one. **My original "ringing a core kills it
> slower" was an artifact of that mixing.**

**And now the bodies-only cut, which is the mechanism we can actually build:**

| j hostile **bodies** | rounds < 250 exposure | P(die ≤25) | 95% CI | P(die ≤50) |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 488,818 | **2.24%** | [2.20, 2.29] | 4.82% |
| 1 | 50,872 | **4.77%** | [4.59, 4.96] | 9.61% |
| 2 | 6,779 | 4.01% | [3.57, 4.51] | 9.13% |
| 3 | 654 | 2.91% | [1.87, 4.49] | 4.99% |

**This is the number LOKI-2 has to be built on, and it is much smaller than the
j=8 headline.** One hostile body on the ring **doubles** the 25-round core-death
hazard (2.24% → 4.77%, CIs disjoint). **The second body adds nothing (4.01%) and
the third is indistinguishable from baseline at n=654 exposed rounds.** The 6.3×
at j=8 comes from hostile **buildings** — forward economies grown over hundreds
of rounds — which is not a thing a bot can decide to do inside the kill window.

**Two causal warnings, both real.** (i) This is *observational*: a body standing
next to their core is also a **marker** that we are already winning the fight
there, so part of the 2× is reverse causation, and nothing here separates the two.
(ii) The exposure is dominated by j∈{0,1}; every cell at j≥3 is thin.

### 1.4 Verdict *(1d revised)*

* **1a — "a builder bot on a ring tile blocks a spawn": VERIFIED.**
  **2,405,604 body tile-rounds, 0 spawns** (own + enemy). The decisive number.
* **1b — "occupying 12 tiles locks the ring": REFUTED as stated.**
  **40.1% of all spawns land on a conveyor tile.** Occupancy is not blocking;
  only 8 of the 14 observed occupant classes block.
* **1c — the own-bodies full lock (12/12 held by our builders): NEEDS PROBE.**
  It has **never occurred** in 2,710 ladder sides — max ever is 6/12 bodies,
  n=4 — so the corpus cannot price its effect, only its absence. **Smallest
  probe that settles it:** LOKI parks builders on all 12 ring tiles of a
  stationary opponent's core and logs `get_unit_count()` for the victim each
  round; the claim is that their count stops rising. One match, no ladder
  exposure. *(The builder arm's `_probe_jail` run today already covers the
  9-of-12 case against a static victim; what is unpriced is 12/12 against a
  defender that steps off.)*
* **1d — "ringing a core kills it fast": ~~REFUTED~~ → my refutation is
  WITHDRAWN; the conditioned answer is a QUALIFIED YES.** The original 6.67%
  vs 19.45% comparison was uncontrolled (§1.3). Conditioned properly:
  **before r250 the 25-round core-death hazard rises monotonically with hostile
  ring occupancy, 1.99% → 12.62% at j=8 (6.3×)**, and the apparent inversion is
  entirely a post-r250 stalemate population. **But the buildable half of it —
  hostile bodies — is worth 2.1× at j=1 and nothing beyond j=1.**

> **The design consequence, revised.** The lock's value is still not *the lock*:
> 12/12 has never occurred, and bodies have never exceeded 6/12. What the
> conditioned data does support is narrower and more actionable than either of
> my earlier readings: **get one builder onto their ring and keep it there, early
> — that alone doubles the 25-round core-death hazard (2.24% → 4.77%) — and stop
> there, because the second body measures at 4.01% and the third at 2.91%.**
> Each body still removes one spawn slot for free (§1.1), which is a tempo tax
> worth having, but the marginal hazard argument for bodies 2–12 is absent from
> the data. **If LOKI-2 is "close the ring right now", the corpus supports the
> *right now* and not the *close*.**

---

## 2. KIDNAPPING — VERIFIED, and the opportunity rate is an order of magnitude above what we act on

The s22 LOKI-5 delta was *"measure the OPPORTUNITY RATE before measuring the
effect size."* This is that measurement.

For every round < 250 and every live enemy builder, I ask whether **we could have
built a launcher next to it**: an empty non-wall tile L with d²(L, their bot) ≤ 2
(the pickup range, V5-verified) that is **orthogonally adjacent to one of our own
live builders** — i.e. a tile we could actually have built on that turn.

| measure, rounds < 250 | US as kidnapper | THEM as kidnapper |
| --- | ---: | ---: |
| enemy-builder-rounds observed | 1,297,086 | 1,344,049 |
| some empty tile adjacent to it (upper bound) | 1,240,137 (95.61%) | 1,215,536 (90.44%) |
| **…that tile also adjacent to OUR builder** | **267,821 (20.65%)** | **276,075 (20.54%)** |
| **…and the same bot is still there next round** | **207,883 (16.03%)** | 210,838 (15.69%) |
| per game: rounds with ≥1 such opportunity | median **118**, p90 211 | median 118, p90 213 |
| per game: distinct enemy bots kidnappable | median **5**, p90 9, max 23 | median 5, p90 11 |
| games with ZERO opportunity | **0 / 1,355 (0.00%)** | 1 / 1,355 |
| launchers this side actually built before r250 | **866 (0.64 / game)** | 873 (0.64 / game) |

The "still there next round" row matters because **a turret cannot fire the round
it is built** (dwell §3: of 1,209 dwell-0 deaths, **0.0% were a turret built onto
a standing bot** — the youngest killer at a dwell-0 kill is one round old).
**16.03% of enemy-builder-rounds survive that filter.**

For scale on what we do today: in these same games we made **3,126 EXILE throws
before r250** (2.3/game) from 0.64 launchers/game — so the machine works; it is
the *placement* that is absent, exactly as the s22 note predicted
(*"we never build a forward launcher"*).

**Verdict — VERIFIED. Decisive number: 20.65% of enemy-builder-rounds before r250
have a launcher site we could physically have built on, and 0 of 1,355 games have
none.** The s22 reading that kidnapping "happens in 0% of median games" was about
throws we *made*, not opportunities we *had*; those are different quantities and
the second one is not scarce.

---

## 3. KIDNAP INTO FRIENDLY FIRE — the geometry is VERIFIED; the conversion NEEDS PROBE

Same scan, with the extra requirement that from that launcher tile L there exists
a legal throw target T with d²(L,T) ≤ 26, T passable, **and T on one of THEIR
live turret lines** — gunner lines reconstructed with blocking respected (the
live prefix up to the first occupied tile), sentinel lines as full rays, using
the `ray()` geometry that validated at 99.991% / 100.000% on 485,925 shots.

| rounds < 250, US as thrower | n | share of enemy-builder-rounds |
| --- | ---: | ---: |
| their turret **ray** reachable from some adjacent tile (upper bound) | 656,382 | 50.60% |
| their live **blocked line**, from any adjacent tile | 602,538 | 46.45% |
| **their live line, from a tile we could actually build on** | **130,490** | **10.06%** |
| our own live line, from a tile we could actually build on | 130,374 | 10.05% |
| per game: rounds with ≥1 such opportunity | median **55** | p90 137 |
| games with ZERO friendly-fire opportunity | **78 / 1,355** | 5.76% |

Per opponent (US side, opponents with n ≥ 15 games), the share of their
builder-rounds where we could throw them onto their own line ranges from
**0.66% (Focalground)** and **2.40% (farming_200s)** — both effectively
turretless against us — to **19.00% (Orizon)**, **18.20% (gsxWins)**,
**17.48% (The Bisons)** and **16.09% (0033)**. It is an opponent-conditional
play and the conditioning variable is simply *how many turrets they build*.

**Verdict — the OPPORTUNITY is VERIFIED at 10.06% of enemy-builder-rounds
(median 55 rounds per game, zero in only 5.8% of games). The CONVERSION is
NEEDS PROBE**, and the gap is behavioural, not geometric: I can prove their bot
would be standing on their gunner's line, and the engine is verified to hit
whatever unit stands on the target tile — but **whether their gunner then chooses
to fire is their bot's targeting logic, which no corpus geometry can answer.**
Smallest probe: one match against a turret-heavy opponent (Orizon, gsxWins) with
a single forward launcher that throws only onto their live gunner prefix, logging
`updateHp` on the thrown bot for the next 3 rounds. Note that throwing onto
**our** line is available at the same 10.05% rate and needs no assumption about
their behaviour at all — that is the safer first cut.

---

## 4. ORE POISONING — REFUTED as a kill path, and the two s22 records reconcile cleanly

### 4.1 How concentrated is opponent income? Not concentrated enough

Per opponent team-side that built at least one harvester (n = 1,272 THEM sides;
US shown as the control at n = 1,343):

| | THEM | US |
| --- | ---: | ---: |
| **distinct ore tiles harvested** | median **5**, mean 6.54, p90 14, max 31 | median 5, mean 6.82 |
| harvesters built | median 5, mean 6.97 | median 5, mean 7.56 |
| **top-1 tile share of their harvesters** | median **25.0%**, p90 50.0% | median 25.0% |
| top-3 tile share | median **60.0%** | median 60.0% |
| sides using exactly 1 tile | 96 (7.55%) | 41 (3.05%) |
| sides using ≤3 tiles | 463 (36.40%) | 432 (32.17%) |

Maps carry **mean 21.5 ore tiles (median 22)**, ~9.4 nearer each core. **Median
spare sites on their own side after everything they use: 11.** Per opponent, the
median distinct-tile count runs from **2 (Askar City, gsxWins)** to
**8 (CtrlAltDefeat)**; the big names sit at 5–7 (Lunds 6, KCM 7, Ouroboros 7,
Powerpuff 6, Memtrace 5).

### 4.2 Reachability — measured from observed travel, and it is NOT the blocker

First round a builder of the given side **stood orthogonally adjacent to an
enemy-side ore tile** (observed positions only; no straight-line estimate):

| side | reached at all | median | p10 | < r50 | < r100 | < r250 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| US | 1,229 / 1,355 (90.70%) | **r26** | r12 | 67.16% | 82.36% | 89.74% |
| THEM | 1,267 / 1,355 (93.51%) | **r19** | r5 | 73.87% | 85.68% | 92.40% |

Against that: **their first harvester lands at median r6 (p10 r2, p90 r13).**

### 4.3 Reconciling the two s22 records — both are right, about different things

* *"ore denial (works)"* (`docs/builder-method.md:24`, from the
  `bots/_probe_denial` engine probe with a restore control) is a **legality**
  claim: a 3 Ti barrier on an empty ore tile vetoes a 20 Ti harvester. **Nothing
  here touches it. It stands.**
* *"pre-emptive ore denial died on reachability"*
  (`docs/research/play-the-players-2026-08-09.md:32`) is about the **opening**
  tile. **My data confirms it exactly**: they open at median r6, we arrive at
  median r19–26. There is no version of that race we win.
* **Both records are silent on the middle case, and that is the one my numbers
  actually settle.** Enemy-side ore is reachable early enough — **68% of sides
  before r50, 83% before r100** — so *reachability is not what kills generic ore
  denial*. What kills it is **spare-site headroom**: they use a median of 5 tiles
  and have a median of **11 spare on their own side**, and their top-1 tile is
  worth only **25%** of their harvesters. Denying two tiles denies a quarter of
  a quarter.

**Verdict — REFUTED as a path to a core kill inside 250 rounds.** Decisive
number: **median 5 tiles used, median 11 spare, top-1 tile worth 25%.** This
independently reproduces the s22 LOKI-4 kill criterion ("five spare sites on the
median map") from a different instrument — harvester placements rather than a map
census — and it corrects the reason: **the s22 note blamed reachability; the
corpus says reachability is fine after r15 and the killer is redundancy.**
*Scope preserved:* this refutes generic and pre-emptive denial. It does **not**
touch "barrier an ore tile a forward gun already covers", which remains
unmeasured, per the standing warning label on the s22 refutations.

---

## 5. SPAWN STARVATION — REFUTED as a partial lever; only the complete lock has a clean zero

Spawns per core-round against the number of ring tiles **hard-blocked** at the
start of the round (blocked = anything from §1.1's zero-spawn list; conveyors
count as free, because they are). Rounds < 250, and rounds where the team was at
the 50-unit cap are **excluded**.

| hard-blocked ring tiles | core-rounds | spawns | spawns / round |
| ---: | ---: | ---: | ---: |
| 0 | 89,191 | 4,200 | 0.0471 |
| 1 | 138,469 | 5,785 | 0.0418 |
| 2 | 115,016 | 4,882 | 0.0424 |
| 3 | 79,515 | 2,641 | 0.0332 |
| 4 | 46,711 | 973 | **0.0208** |
| 5 | 27,530 | 404 | 0.0147 |
| 6 | 15,698 | 235 | 0.0150 |
| 7 | 15,505 | 387 | 0.0250 |
| 8 | 17,039 | 524 | 0.0308 |
| 9 | 9,702 | 248 | 0.0256 |
| 10 | 5,006 | 60 | 0.0120 |
| 11 | 1,577 | 36 | 0.0228 |
| **12** | **531** | **0** | **0.0000** |

**The relationship is not monotone and I will not dress it up.** It falls from
0.047 to 0.015 between 0 and 6 blocked and then **rises again** at 7–9. That
non-monotonicity is the confounder announcing itself: heavy blocking is mostly a
team's *own* mature infrastructure and correlates with a rich economy, which
raises spawn rate. **The only unconfounded cell is the last one — 531 core-rounds
with all 12 blocked and zero spawns** — and it is a definitional consequence of
§1.1, not new information.

**Verdict — REFUTED as a partial lever. Decisive number: blocking 4 of 12 halves
the observed spawn rate (0.0471 → 0.0208) but the curve is non-monotone above 6,
so the halving cannot be attributed to the blocking.** The core needs exactly one
free tile; partial occupation buys nothing you can bank. Only 12/12 is a lock,
and 12/12 is item 1c — NEEDS PROBE.

### 5.1 Phase-controlled re-cut — the confounder I flagged is NOT phase, and this strengthens the refutation

The hazard framing from §1.3d does not transfer here (spawning is a per-round
*action*, not a time-to-event), but the cheap version does: re-cut the same table
in **50-round bins**, so game phase is held fixed within each column. Spawns per
core-round, 50-unit-cap rounds excluded:

| hard-blocked | r0–50 | r50–100 | r100–150 | r150–200 | r200–250 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | **0.1277** | 0.0095 | 0.0226 | 0.0245 | 0.0262 |
| 2 | 0.1086 | 0.0111 | 0.0194 | 0.0200 | 0.0214 |
| 4 | 0.0401 | 0.0109 | 0.0168 | 0.0157 | 0.0209 |
| 6 | 0.0105 | 0.0112 | 0.0150 | 0.0123 | 0.0233 |
| 8 | **0.0996** | 0.0060 | 0.0148 | 0.0133 | 0.0165 |
| 10 | 0.0200 | 0.0068 | 0.0122 | 0.0095 | 0.0171 |

*(cells shown only where ≥300 core-rounds of exposure)*

**Holding phase fixed makes the relationship weaker, not stronger.** In r50–100
through r200–250 the rate is essentially **flat across every blocking level**
(0.010–0.011, 0.012–0.023, 0.010–0.025, 0.009–0.026) — blocking 10 of 12 ring
tiles moves the spawn rate by less than the bin-to-bin noise. The only column
with any gradient is **r0–50**, and it is exactly where the non-monotone bump
survives (0.0105 at 6 blocked, **0.0996** at 8). So the confounder is **not**
game phase; it is a distinct early sub-population — teams that wall their own
core in immediately and are also spawning hard.

**The §5 verdict is unchanged and now better supported: partial spawn starvation
is REFUTED, and phase was not the explanation.**

---

## 6. CONVEYOR SIPHON — not a rounding error, but it is off-currency

### 6.1 How much titanium actually flows

Per team-side per game (n = 1,355 each), from `distributeResources`, exact
against `econ.ti_collected_end` at 2,710/2,710:

| | US | THEM |
| --- | ---: | ---: |
| Ti delivered into own core, whole game | median **1,730**, mean 4,637, p90 13,800, max 31,350 | median 2,160, mean 4,595 |
| **Ti delivered before r250** | median **1,160**, mean 1,398, p90 3,040 | median **1,160**, mean 1,385 |
| conveyor/splitter hops inside own net, whole game | median 813, mean 3,028 | median 1,112, mean 3,277 |
| own-net hops before r250 | median 492, mean 794 | median 516, mean 875 |

### 6.2 How much of it we could physically touch

A hop counts as *reachable* if our builders had already stood on or orthogonally
next to its destination tile **by that round** (first-arrival time, not
end-of-game — the loose version inflated this to 90%).

| | US net | THEM net |
| --- | ---: | ---: |
| own-net hops on an enemy-reachable tile, whole game | 2,185,989 / 4,103,424 = **53.27%** | 1,679,354 / 4,440,882 = **37.82%** |
| **same, before r250** | 400,977 / 1,076,121 = **37.26%** | 227,488 / 1,185,481 = **19.19%** |
| into-core hops on an enemy-reachable tile | 47.42% | 23.51% |

### 6.3 And the engine already does it, by accident

The V7 failure named this: **titanium is credited to whoever owns the destination
core, regardless of which team's building pushed it.** It happens, and it is
rare:

| | US cores | THEM cores |
| --- | ---: | ---: |
| stacks banked from the OTHER team's network | 1,099 / 628,367 = **0.175%** | 838 / 622,604 = **0.135%** |
| games with any such donation | 7 / 1,355 (0.52%) | 12 / 1,355 (0.89%) |
| median donated, among those games | 600 Ti | 335 Ti |
| games pushing ≥1 hop onto the enemy's network | 556 (41.03%) | 593 (43.76%) |

**Verdict — NOT a rounding error, and still the wrong instrument for this
programme.** Decisive number: **19.19% of the opponent's in-flight titanium
before r250 moves across tiles our builders had already reached** (median 516
own-net hops per game; the 19.19% is over all 1,185,481 such hops, not a
per-game median). At 10 Ti a stack that is real
money. But the machinery-audit refutation still binds — a tap needs a completed
chain home, destructible along its length — and, more decisively for LOKI:
**the median opponent banks 1,160 Ti before r250 and the programme's currency is
a dead core, not their bank balance.** Halving their income does not kill a core
by round 250. Park it; it is an Eir-shaped idea on a Loki programme.

---

## 7. What this hands the builder, in priority order

1. **KIDNAP-ADJACENT PLACEMENT is the one to build.** 20.65% of enemy-builder-
   rounds before r250 sit next to a tile we could have built a launcher on, 16.03%
   persist a round, **and 0 of 1,355 games have none**. We build 0.64
   launchers/game and none of them forward.
2. **Throw onto OUR OWN line first, not theirs.** Same 10.05% availability, and
   it needs no assumption about the opponent's targeting logic. Their-line
   throwing (10.06%) is the same geometry with a behavioural bet attached, and it
   is worth 16–19% against Orizon / gsxWins / The Bisons / 0033 and ~1–2% against
   Focalground / farming_200s.
3. **Ring-parking: get ONE body there, EARLY, and keep it.** *(revised after
   the §1.3 re-cut — my first reading of this item was an uncontrolled
   comparison and is withdrawn.)* One hostile body on their ring **doubles the
   25-round core-death hazard (2.24% → 4.77%, CIs disjoint, 539k exposed
   builder-rounds)**. The second body measures 4.01% and the third 2.91% — there
   is no marginal case for bodies 2–12 in this data. Each body still removes one
   spawn slot for free (§1.1). **Do not build toward 12/12 on the strength of
   this corpus**, and treat the 2× as partly reverse causation (§1.3d).
4. **Do not build ore denial for the kill window.** Median 5 tiles used, 11 spare.
5. **Do not build partial spawn starvation.** Holding game phase fixed in
   50-round bins, the spawn rate is flat across every blocking level from r50
   onward (§5.1). Phase was not the confounder.
6. **Do not build the siphon for LOKI.** Real money, wrong currency.

---

## 8. Limits and approximations, each stated where it bites

* **"Reachable" in items 2 and 3 means our builder was orthogonally adjacent to
  the candidate tile.** It ignores action cooldown, the 20 Ti launcher cost, and
  the cost-scale multiplier. It is therefore an **upper bound on placement
  opportunity**, though a tight one — the binding constraint on the field is
  geometry, not 20 Ti.
* **Throw targets exclude any tile holding a building or a bot.** For a gunner
  that means I only count the *empty prefix* of its live line, never the terminal
  tile it is currently shooting. **This under-counts item 3**, since the verified
  friendly-fire incident (`010eb62d…_game_3`, r112) happened on a tile that held
  a conveyor.
* **Item 3 proves geometry, not outcome.** Whether their gunner fires at the bot
  we deliver is their bot's decision. Labelled NEEDS PROBE for exactly that.
* **The kidnap scan samples every round < 250, but a "kidnap opportunity" is a
  (round, bot) pair, not an independent trial.** A bot that stands still for 30
  rounds contributes 30. The per-game "rounds with ≥1 opportunity" and "distinct
  bots" columns are given precisely so the correlated version is visible.
* **Ring occupancy is evaluated at END of round** against the end-of-round board,
  the same convention as `dwell_decode.py`. A body that entered and left within
  one round is not counted — a mild under-count.
* **`ore_side` is assigned by which core is nearer**, with equidistant tiles
  (mean 1.0 per map) counted as neutral and excluded from both sides. Maps are
  symmetric by construction, so this is exact for reflection and rotation alike.
* **Item 1's blocking table is observational.** It cannot distinguish "the engine
  forbids it" from "no bot ever tried". The causal half comes from the builder
  arm's live probe today; this table supplies the scale.
* **Item 5's non-monotonicity is still unexplained**, but §5.1 rules out game
  phase as the cause. I did not build an economic control, and I am not
  asserting one.
* **§1.3's re-cut removes a selection effect; it does not establish causation.**
  The per-round hazard (§1.3d) is immune to *that* bias because it is evaluated
  at every round, but a body on their ring remains a **marker** of a fight we are
  already winning as well as a possible cause of the kill. Nothing in a corpus
  can separate those. The 2× is an upper bound on what parking a body buys.
* **§1.3d is right-censored explicitly**: a round contributes to horizon H only
  if the outcome is observable within H. Censored rounds are dropped from
  numerator and denominator. Without this, every replay's last H rounds would be
  scored as survivals and the hazard would read low — the same shape as the bias
  §1.3 was retracted for.
* **The corpus is not a random sample of the field** (corpus-howto trap 4). All
  THEM numbers mean "against us, in N archived matches"; per-opponent n is stated
  in every per-opponent table and ranges 15–130.
* **`oppver` is all-null** (trap 7), so nothing here is split by opponent version;
  an opponent that changed bots mid-window is pooled.
* **US figures span v89–v92**, since `join.tsv` covers several of our own
  versions. They are used as a control and a scale reference, never as a verdict.

---

## Provenance

Scripts, committed: `docs/research/scripts/arsenal-2026-08-09/` —
`arsenal_decode.py` (the extended decoder), `validate.py` (the ten checks),
`analyse.py` and `analyse2.py` (the tables above), `analyse3.py` (the §1.3
re-cut and §5.1), `diag.py` (the V7 root-cause probe). Outputs, in the session
scratchpad:
`ars_ring.tsv` 2,710 rows · `ars_kid.tsv` 2,710 · `ars_flow.tsv` 2,710 ·
`ars_trav.tsv` 2,710 · `ars_map.tsv` 1,355 · `ars_val.tsv` 1,355 ·
`ars_spawn.tsv` 75,215 · `ars_stile.tsv` 32,477 · `ars_ore.tsv` 17,480 ·
`ars_haz.tsv` 39,653 (the §1.3d hazard panel).

**§1.3's re-cut needed two decoder additions (A8), so the decoder was re-run on
the SAME frozen inputs**: first-reach rounds for hostile *bodies*, and the
right-censored per-round hazard panel; the spawn table's band column was
narrowed from 100- to 50-round bins for §5.1. All ten §0.3 checks re-passed
identically on the re-run (1,355 files, 0 errors).

Base decoder, its validation history and the four traps:
`docs/research/scripts/side-lane-2026-08-09/README.md`,
`docs/research/corpus-howto.md`. Prior records reconciled in §4.3:
`docs/builder-method.md:24`, `docs/research/play-the-players-2026-08-09.md:32,42-48`,
`docs/coordination.md:10466-10485, 10886-10905`. Prior records this extends in
§1: `docs/coordination.md:10587-10625` (s22 `_probe_prison`), `16394-16440`
(today's `_probe_jail`). Item 2's framing debt: `docs/coordination.md:11060-11078`
(the LOKI-5 delta that asked for an opportunity rate).
