# ECO STUDY — building CONNECTED harvesters faster

**Commissioned by Magnus, 2026-08-17, verbatim:** *"figure out how to build
connected harvestors and basically our eco even faster, we need to make it super
efficient."*

**Written by a builder-commissioned opus ECO STUDY agent, 2026-08-17 (`date -u`
at commission: `Mon 17 Aug 2026 04:32:31 UTC`), repo `5a1e652c`.**
**Instruments:** three fresh scratchpad decoders over `replay_archive/` +
`corpus/events.tsv` (10,141,801 rows) + `corpus/join.tsv` +
`corpus/unrated_games.tsv` + `corpus/meta_join.tsv`. **No games fired, no
platform window spent, nothing in the repo modified except this file.**

⚠ **COMMIT PROVENANCE:** the body of this file was swept into the tree by another
session's `commit -a` at **`304dc317`** while it sat staged, so its content is
recorded under that session's message rather than this study's. **This commit is
the study's own record of authorship** — nothing in the text changed between the
two.

**Baseline under study:** v155 "Sleipnir" = `bots/_v468kladturbo`
(samestop x turbo x bodyaware). Every mechanism below is an INCREMENT on that
tree, never on `_v223sealrepair`.

---

## 0. THE ONE-PAGE ANSWER

**Our FIRST delivery lands at the same round as the opponents we actually play
(r14 vs r14, paired in 245 games). Our delivery COST is ~40-50% higher, and our
economy takes twice as long to reach four standing harvesters as the field's
best (r20 vs r10, rank 14 of 55).** That is the finding, and it re-points the
commission: "make eco faster" is worth less than "make eco cheaper and more
complete", because under `R1000_IS_DEFEAT` economy is instrumental — it buys the
kill, and the thing it buys with is **cost scale**, which is the same currency
the sentinel is priced in.

Four MEASURED headlines, all v155, denominators inline:

1. **We wire 74.9% of the harvesters we build (1,295 / 1,730).** The opponents in
   *the same 245 games* wire **86.3% (990 / 1,147)** — from **4** harvesters a
   side against our **6**. **435 of our harvesters never got a route home**:
   20 Ti each and **+5% permanent cost scale each**, for zero titanium.
2. **We are the slowest wirer in the top eco set.** Median rounds from a
   harvester being built to its first adjacent conveyor: **us +2.25**, Pivot
   +2.05, Torsko +2.02, Bean counters +1.75, **O(1) +0.10, Hugging Farce
   −2.29** (their belt is laid *before* the harvester lands).
3. **Round at which four harvesters are standing: us r20 (rank 14 of 55),
   O(1) and Hugging Farce r10.** Not a map artefact — the ordering holds in
   every map-area class and our map mix matches the leaders'.
4. **Our first-delivery round predicts our first-sentinel round at slope
   1.17-1.18** (n=98 v155 rated games; within-map pooled slope 1.171 across 11
   maps, so the map is not the confound). Median first delivery r14 → median
   first sentinel r28-32. **Eco latency is not a tiebreak metric here; it is the
   clock on the kill recipe.**

**THE TOP THREE MECHANISMS (full ranked list with backing, risk and demo in §7):**

1. **M1 — COMMIT-BEFORE-YOU-DIG.** Never place a harvester without committing to
   its route, and let a builder ADOPT an orphaned chain. Attacks the 25.1%
   never-connected (2x the opponents' rate, and 0 of 1,730 were terrain-blocked).
2. **M2 — THE FREE ROUND.** ~26% of our eco-phase builder-rounds produce nothing
   (12.0% A→B→A oscillation + 13.8% idle that is **100% policy** — cooldowns 0,
   TLE 0.00%). The anti-oscillation guard already exists in this tree, for
   gunner rotation. It is a PORT, not a design.
3. **M3 — SCORE ORE BY ROUTE LENGTH, NOT DISTANCE.** Connect latency is **2.00
   rounds per route tile** and degrades worse than linearly past L ≈ 8; `_pick`
   sorts by Manhattan distance from the core and never scores the route. The CPU
   objection to a smarter picker is now dead and measured (p99 = 550 µs of a
   10,000 µs budget).

And one engine fact that bounds every mechanism in this document:

> **A SINGLE BUILDER CANNOT LAY A CONVEYOR CHAIN FASTER THAN ONE TILE PER TWO
> ROUNDS.** Builder move cooldown = 1 round, action cooldown = 1 round, and
> acting and moving are mutually exclusive within a round
> (`docs/reference/official-docs.md:1142-1143,1175,1189`). Build a tile, move,
> build the next. **0.5 tiles/round/builder is a hard floor, not a tuning
> parameter.** Everything that beats it needs MORE HANDS on the same chain —
> which is exactly what the field's fastest wirers are measured doing.

---

## 1. WHAT THE INCUMBENT ACTUALLY DOES (source read, `bots/_v468kladturbo`)

Per eco builder, per round, `EcoMixin._expand` (`eco.py:1655`) runs this ladder.
Action phase first (only if `get_action_cooldown() == 0`):

1. **`_samestop_fire`** (`eco.py:927`) — the conveyor armed last round, built
   without moving. Top priority.
2. **`_build_next_link`** (`eco.py:953`) — lay `link_queue[0]` if orthogonally
   adjacent. Pops the queue as it lays.
3. **Harvester** — if `_eco_spendable` and `harv < _eco_cap` (`ECO_CAP = 18`),
   build on ANY adjacent ore tile, in `DIR_DELTAS` order. **There is no route
   check, no wireability check and no affordability-of-the-belt check.** Then
   `_wire_on_build` (`eco.py:800`) plans the trunk and arms same-stop.
4. **`_l4_repair`** (`eco.py:1037`) — fill a one-tile HOLE with a feeder on one
   side and an acceptor on the other.
5. **Chain medic** — heal an adjacent damaged belt tile.

Then the move phase: multi-healer convergence → siphon denial → ore step-off →
**follow `link_queue`** → else `_pick` a new ore, with the SAMESTOP stop-tile
preference steering the builder onto `plan[0]`.

**SAMESTOP, precisely** (`doctrine.py:1833-1877`, `LOKI_SAMESTOP_ON = True`):
`_link_path(ct, ore)` returns the planned route home; `plan[0]` is orthogonally
adjacent to the ore and `plan[1]` to `plan[0]`. The builder is steered to STAND
on `plan[0]`, builds the harvester from there, and next round builds `plan[1]`
without moving. `plan[0]` itself is left EMPTY — the builder is standing on it —
and becomes an `_l4_repair` HOLE that gets filled once the builder steps off.
**Scale-neutral by construction: it changes WHEN and FROM WHERE two links go up,
never how many.**

**Roles** (`main.py:426-455`, `doctrine.py:1195-1211`): five opening builders,
unconditional. Seat 0 raids, **seats 1-3 are the economy**, seat 4 defends. Seat
3 defects to the raid the moment `SLOT_HARVESTERS >= ECO_NEED (3)` **and its
`link_queue` is empty** (`main.py:526-533`) — the only role transition in the
file, and it is chain-safe by that second clause.

**`PAVE_TRAIL_ON = False`** (`doctrine.py:528`) is deliberate and is a DIFFERENT
cadence: it drops a conveyor on the tile a builder just VACATED, **one structure
per MOVE**, uncapped, measured at 38.20 conveyors/game. SAMESTOP is per STOP.
Nothing in this report proposes re-enabling the per-MOVE trail; §5 says why the
per-MOVE form cannot buy tempo even in principle.

**Ore choice** (`_pick`, `eco.py:1183`): ores sorted by Manhattan distance from
our CORE, then striped `ordered[worker::workers]` with `workers = 4` (2 on maps
of area ≤ 220) and `worker = (role_n - 1) % workers`. **Distance to the core is
the only geometry term — the length of the route the builder will then have to
build is never scored.**

---

## 2. THE ENGINE ARITHMETIC — what any eco algorithm is allowed to achieve

These are rules-level facts (the carve-out in the LOKI directive point 6: the
game's own definition, not behavioural inference). Sources named.

* **Passability** (`docs/reference/official-docs.md:1150-1170`): CONVEYOR and
  SPLITTER tiles **are** bot-passable; ORE is passable; WALL, HARVESTER,
  BARRIER, turret and CORE tiles are not. ⇒ **a builder can walk along the belt
  it has just laid.** *(Verified on the wire in §4 — the organisers' doc is
  known-wrong in places and this fact is load-bearing.)*
* **Cadence:** move cooldown 1, action cooldown 1, mutually exclusive per round
  (`:1142-1143`, `:1175`, `:1189`). ⇒ **build-move-build = 2 rounds per tile per
  builder.**
* **Adjacency:** builds are orthogonal-only and never the builder's own tile
  (`:1189`). ⇒ **a builder standing on a straight chain can serve `t_{k-1}` and
  `t_{k+1}` but never `t_k`.**
* **Transit:** a conveyor holds at most one stack and moves it one tile per
  round (`get_stored_resource_id` returns ONE id; distribution runs once at end
  of round). ⇒ **a stack takes L rounds to cross an L-tile chain, and a shared
  trunk caps at 1 stack/round = 10 Ti/round.**
* **Back-pressure is LOSSLESS** (`bots/_probe_beltstall`, QUEUE `#66a`): a
  disconnected chain queues one stack per tile and holds them ~984 rounds
  unchanged; on connection every stack shifts and the harvester releases a fresh
  one immediately. **Nothing emitted is destroyed.**

### 2.1 THE RESULT THAT KILLS "PAVE THE WALK-OUT" ON PAPER

Let L = route length in tiles from the ore to the core ring, and assume the walk
out is ~L.

* **Harvester-first (what we do):** walk out L → build harvester at r=L → lay the
  chain harvester-end-first at 2 rounds/tile → complete at ~3L → the buffered
  lead stack delivers at **~3L+2**.
* **Pave-the-walk-out:** paving doubles the outbound walk to 2L → harvester at
  ~2L+2 → its first stack must then transit L tiles → **~3L+2**.

**IDENTICAL.** The chain-laying cost and the stack-transit cost trade off
exactly, because both run at the same rate against the same L. **This is why
QUEUE `#50`'s original walk-out arm was right to die, and it generalises: no
re-ORDERING of a single builder's work changes first-delivery round.** Only two
things do:

* **cut L** (shorter route: better ore choice, or reuse of an existing trunk), or
* **cut the 2 rounds/tile** (more builders on the same chain).

Two-builder pinch (one from each end) completes at ~2L and delivers at ~2.5L —
**saves ~0.5L**. Two builders leapfrogging from the harvester end complete at
~2L with the buffer already stacked behind the head — **saves ~L**. Three eco
builders on one chain: ~1.67L, **saves ~1.33L**. *(MODEL, labelled INFERRED; the
inputs are the MEASURED cadence and transit facts above.)*

---

## 3. OUR TIMELINE — MEASURED, v155

**POPULATION:** every replay in `replay_archive/` whose `ourver == 155` —
**110 rated games (`corpus/join.tsv`, 22 matches) + 135 unrated games
(`corpus/unrated_games.tsv`, 27 matches) = 245 team-sides from 49 matches.**
0 files missing, 0 files failed to parse. Both sides of every file were decoded,
so the 245 opponent sides are a PAIRED control on identical maps and identical
games. Era: v155 only; a v152 comparison is in §3.4.

**DECODER VALIDATION** (the check is allowed to fail, and was made to):
* Positive control — `own_core_deliveries * 10 == Player.titaniumCollected`:
  **1,430 / 1,430 team-sides, 0 mismatches** (v155 + v152, rated + unrated).
* Geometry mutation — core footprint shifted +1 in x: **50/50 → 5/50.** The
  geometry is load-bearing, not incidentally satisfied.
* Wrong-geometry control — 3x3 block instead of the 2x2 footprint: **2/50 pass.**
  The schema doc's 3x3 note is the visualiser's superset, NOT the delivery
  geometry. Use the 2x2 footprint.
* Connectivity cross-check, **both ways**: sides with ≥1 structurally connected
  harvester and >0 deliveries **1,355 / 1,356 (99.9%)**; sides with **0**
  connected harvesters and >0 deliveries **3 / 74 (4.1%)**, delivering 1, 2 and 6
  stacks — consistent with enemy stacks pushed into our core (a gift, per the
  guard-matrix ruling), not our own routes. The complement group behaves as
  required, so the connectivity claim discriminates.

### 3.1 Build and delivery clock (median [IQR], n = 245 sides)

| metric | US v155 | opponents, same 245 games |
|---|---|---|
| 1st harvester build round | **7** [5-9] | 6 |
| 2nd harvester | 10 [8-13] | — |
| 3rd harvester | 16 [11-19] | — |
| 4th harvester | 29 [20-44] | — |
| first conveyor round | 8 [6-10] | 6 |
| **first own-core delivery** | **14** [11-19] | 14 |
| **latency (1st delivery − 1st harvester)** | **8** [5-11] | 7 |
| harvesters built | **6** [4-9] | **4** |
| harvesters ever connected | **4** | **4** |
| conveyors built (total / by r50) | **35** / 20 | **24** / 17 |
| splitters built | 0 | 0 |
| builders alive r25 / r50 | **6** / 6 | **4** / 4 |
| delivered Ti by r25 / r50 / r100 / r150 / r200 | 60 / 220 / 490 / 650 / **790** | 70 / 220 / 460 / 630 / **670** |

**Read it straight: we buy 50% more harvesters, 46% more conveyors and 50% more
builders, and are level on delivered titanium until r150.** The extra spend
starts paying only past r150 — i.e. past the window `R1000_IS_DEFEAT` says the
game is supposed to be decided in.

**Ordering:** conveyor-before-harvester in **0 of 245** of our games (1 same
round, 244 conveyor-after). The opponents do it the other way in **73 of 231**.

### 3.2 THE 25% THAT NEVER GO HOME — the biggest single number in this study

**1,295 of 1,730 harvesters ever structurally connected = 74.9%.** Opponents in
the same games: **990 / 1,147 = 86.3%.** Median connect latency (connect round −
build round) **8 rounds** [3-15]; only 127 of 1,295 are connected at build (i.e.
built adjacent to the core).

| ordinal | built | ever connected | connect latency | d² to own core |
|---|---|---|---|---|
| #1 | 245 | 226 (92%) | 6 [3-9] | 18 [9-36] |
| #2 | 244 | 222 (91%) | 7 [4-10] | 25 [13-49] |
| #3 | 230 | 186 (81%) | 10 [6-18] | 37 [25-113] |
| #4 | 208 | 147 (71%) | 10 [7-18] | 50 [34-121] |
| #5 | 176 | 117 (66%) | 12 [8-22] | 61 [40-144] |
| #6 | 140 | 89 (64%) | 12 [4-20] | 85 [39-146] |

**The failure is monotone in distance and it is concentrated in harvesters #3-#6
— exactly the ones `_expand` builds with no route check at all.** 435 harvesters
× 20 Ti (at scale) **and +5% permanent cost scale each**, delivering nothing,
ever.

**Distribution of first delivery** (n = 245): ≤ r20 **73.9%**, ≤ r30 86.9%,
> r30 **9.0%**, > r50 **4.1%**, **NEVER 4.1% (10 sides)**. All ten
never-delivering sides built 2-3 harvesters and 5-20 conveyors and connected
none of them — **we laid belt that never reached home.** One of those ten ran the
full 1,000 rounds and lost on `titanium_collected` with zero delivered.

### 3.3 THE MECHANISM BEHIND THE UNWIRED SHARE IS NAMED IN OUR OWN SOURCE

`_l4_repair`'s docstring (`eco.py:1050-1062`) states it, from a 15-replay local
count: the belts it fires on are mostly **"DEAD HEADS: chains this bot abandoned
mid-walk, which `_build_next_link` never returns to because it pops its queue as
it lays it."** And `_l4_repair` deliberately does **not** fix them: *"A two-wide
hole has no side with both a feeder and an acceptor, so it is left alone; so is a
dead head with no acceptor in reach."*

⇒ **A dropped chain is unrecoverable by any machinery in the shipped tree.**
`link_queue` is per-builder instance state with no store slot and no hand-off, so
when a builder dies, converges on the core (`SLOT_UNDER` + `_core_shelled`),
diverts to siphon denial, or is displaced, its route dies with it. **That is a
CODE fact, MEASURED consequence in §3.2, and it is what mechanism M1 below
attacks.**

### 3.4 Era and surface splits (discipline, not decoration)

**v155 vs v152** (rated-only, to hold the surface fixed; 470 v152 sides,
94 matches): harv1 7 vs 7, first conveyor 8 vs 9, first delivery 15 vs 16,
latency 8 vs 9, connected 77.4% vs 75.6%, never-delivers 6.4% vs 5.0%.
**Same economy opening.** The opponent pools are also disjoint (v155 rated met
Juusto/Erebus/team lazy/kladde; v152 rated met HTTP 418/lingling_40h/kladde/0033)
so the one-round deltas are confounded with opponent mix and are NOT banked.

**Rated vs unrated (v155):** identical build timing (harv1 r7, first conveyor r8
both). Tails disagree in direction (never-delivers 6.4% rated vs 2.2% unrated;
first delivery > r30 6.4% rated vs 11.1% unrated) — read as noise, not a surface
effect.

⚠ **CLUSTERING:** these are team-sides and five games share a match, an opponent
and one ladder slice. 245 v155 sides = 49 matches. No CIs are attached anywhere
in this section; everything here is DESCRIPTIVE. Any bar built on these numbers
must be restated as an EXCLUSION and carry the rated DEFF (1.529 pooled / 1.366
within-opponent).

### 3.5 WHY THIS IS A KILL-CLOCK METRIC, NOT A TIEBREAK METRIC

Our **first sentinel lands at median r28** (n = 103 of 110 v155 rated games;
first gunner r86, first launcher r175). Our **delivered titanium at r25 is 60 Ti**
— roughly one sentinel at the scale five opening builders have already bought.

Regressing first-sentinel round on first-delivery round over 98 v155 rated games:
**slope +1.18, r = 0.403**; pooled WITHIN MAP across the 11 maps with ≥6 games:
**slope +1.171, n = 82.** By bucket: first delivery r10-14 → first sentinel r20
(n=35); r15-19 → r28 (n=28); r25-29 → r41.5 (n=10).

⚠ **OBSERVATIONAL, labelled INFERRED.** The map is excluded as the confound by
the within-map re-run, but early harassment is not: a game where our delivery is
late may be a game where we were being hit, which independently delays the
sentinel. **The slope is an upper bound on the causal effect, not the effect.**
It is quoted here to establish DIRECTION and rough magnitude — a round of
delivery latency is worth of order a round of first-sentinel delay — not to price
a plank.

### 3.6 THE 25% IS NOT ATTRITION — control run, and it came out the other way

The obvious alternative explanation for unwired harvesters is that the enemy
kills the builder mid-chain. **It is wrong.** Split the 245 v155 sides by the
number of OUR builder bots that died by r60 (`corpus/events.tsv` DEATH rows,
own team):

| our builder deaths by r60 | games | harvesters | ever connected |
|---|---|---|---|
| **0** | **209** | **1,521** | **74.9%** |
| 1 | 27 | 156 | 78.8% |
| 2 | 4 | 34 | 50.0% |
| 3+ | 5 | 19 | 84.2% |

**In the 209 games where we lost NO builder in the first 60 rounds, the connected
share is 74.9% — identical to the pooled figure.** ⇒ **the unwired quarter is an
ALGORITHM outcome, not an attrition outcome**, which is what makes it fixable in
code rather than in defence. *(The 2-death cell is n=4 games and carries no
weight.)*

---


## 4. THE FIELD'S BEST — MEASURED, league-wide

**POPULATION:** one pass over `corpus/events.tsv` (10,141,801 BUILD/DEATH rows)
→ 116,384 team-sides, **115,672 joined to `meta_join` metadata (99.4%)**;
43,972 ladder + 71,700 unrated. Seat attribution cross-checked against
`game_winner_side` on core-death rows: **47,932 consistent / 31 inconsistent /
312 unjoinable (99.94%)** — this is an INDEPENDENT check, not the winner-derived
`seat` column that TRAP 7 warns about.

**"r4" = first round at which built-minus-dead harvesters ≥ 4.** Medians are
CENSORED LOWER-MEDIANS (a side that never reaches 4 counts as +∞), so a team with
under 50% reach has no finite median: **55 of 72 qualifying teams have one.**

### 4.1 Headline table — recent era, map-controlled

Most-recent 200 sides per team, map-area class 500-700 (the modal class:
520/560/576/625/676). **n = 200 per team; all teams last seen 2026-08-14..17.**

| # | team | ver span | **r4** | reach | h1 | h2 | h3 | h4 | conv-first | elo |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | O(1) | 20-25 | **10** | 97% | 5 | 6 | 7 | 10 | 100% | 2038 |
| 2 | Hugging Farce | 35-41 | **10** | 100% | 5 | 7 | 9 | 10 | 100% | 1542 |
| 3 | Bean counters | 34-47 | **12** | 95% | 3 | 5 | 6 | 12 | 22% | 2087 |
| 4 | Pivot | 170-188 | 13 | 96% | 4 | 5 | 6 | 13 | 0% | 2076 |
| 5 | Torsko | 67-77 | 15 | 86% | 5 | 8 | 10 | 15 | 0% | 1580 |
| 8 | Ouroboros | 8-8 | 17 | 95% | 5 | 6 | 9 | 17 | 74% | 1422 |
| 11 | Leviathan | 67-76 | 19 | 99% | 3 | 7 | 17 | 19 | 64% | 1936 |
| 12 | Erebus | 108-127 | 19 | 85% | 3 | 4 | 11 | 19 | 0% | 1800 |
| 13 | sporks | 14-25 | 19 | 80% | 4 | 7 | 12 | 19 | 27% | 2058 |
| **14** | **OpenSverige** | **125-156** | **20** | **91%** | **6** | **8** | **10** | **20** | **0%** | **1817** |

**Rank 14 of 55.** Our first harvester r6 against the leaders' r3-5; our fourth
at r20 against r10; conveyors by r50 19 against Hugging Farce's 33.

**ERA DISCIPLINE, and it corrects a claim we could easily have made about
ourselves:** pooled over our whole archive (v64-156, 11,051 sides) our r4 reads
**53** and ranks 27/53. Held at area 500-700 it reads 35. **Restricted to the
most recent 200 sides (v125-156) it reads 20.** Our old versions were much
slower and pooling them manufactures a gap that is not there today. MEASURED;
the attribution of the gain to v125+ specifically is INFERRED.

Top-5 era re-run at area 500-700: **Hugging Farce 13→10, Bean counters 18→12,
O(1) 20→10 on their newest versions; Pivot stable at 13.** The leaders are still
improving. ⚠ **Ouroboros is STALE** — only v8 is archived while the platform
shows v33; do not treat its 17 as current.

**MAP CONTROL:** the ordering holds in every area class (<300 / 300-500 /
500-700 / >700), our median map area (520-625) matches the leaders', and on tiny
maps (<300) no team reliably reaches 4 harvesters because ore is scarce. **The
gap is not a map artefact.**

### 4.2 Belt topology of the top eco executors — where the tempo comes from

Recent 400 sides per team, area 500-700, rounds 0-60:

| team | conv@60 | harv@60 | components | **adj≤2rnd** | **max builds/rnd** | d² first→last conv | c1 at core | harv wired | **wire lag** | splitters |
|---|---|---|---|---|---|---|---|---|---|---|
| O(1) | 29 | 6 | 3 | **0.41** | **3** | 4→37 | **1.00** | 0.977 | **+0.10** | 0 |
| Hugging Farce | **36** | **10** | 4 | **0.48** | **3** | 13→37 | 0.04 | **1.000** | **−2.29** | 0 |
| Bean counters | 28 | 8 | 3 | **0.48** | **3** | 5→26 | 0.58 | 0.977 | +1.75 | 0 |
| Pivot | 22 | 7 | 3 | 0.68 | 2 | 13→29 | 0.01 | 0.970 | +2.05 | 0 |
| Torsko | 29 | 6 | 2 | 0.68 | 2 | 13→17 | 0.17 | 0.985 | +2.02 | 0 |
| **OpenSverige** | **20** | **5** | 3 | **0.69** | **2** | 13→**10** | 0.07 | **0.960** | **+2.25** | 0 |

Every row MEASURED. What it says:

1. **TRUNK-AND-SPUR IS UNIVERSAL. Nobody builds one line per harvester.** Median
   3 connected conveyor components against 5-10 harvesters
   (components/harvester 0.42-0.77). Our own 0.53 is normal. **This closes the
   "should we switch topology" question: we already have the field's topology.**
2. ⛔ **READ §6.5(d) BEFORE QUOTING THIS ROW — I OVERSTATED IT AND MEASURED IT
   DIRECTLY LATER.** The contiguity statistic below is real; the "single paving
   walk" reading of it is **not supported** by the direct count of distinct
   builders per chain (we are 2.11, mid-field). Kept here in its original form so
   the correction has something to correct.
   **THE STATISTIC:** `adj≤2rnd` (share
   of conveyor builds orthogonally adjacent to one built in the previous two
   rounds) splits the table cleanly in two: **us / Pivot / Torsko at 0.68-0.69
   with a MAX OF 2 conveyor builds in any one round — a single paving walk.
   O(1) / Hugging Farce / Bean counters at 0.41-0.48 with a MAX OF 3 — several
   fronts at once.** The fast group is not laying belt faster per builder; it
   has more builders laying at the same time. *(`adj-any` is 0.74-0.79 for
   everyone, so raw contiguity is NOT the discriminator — the two-round window
   is. That is the control that makes this reading mean something.)*
3. **WIRE LAG is where the harvester-first doctrine costs us.** Median rounds
   from a harvester build to its first adjacent conveyor: **Hugging Farce −2.29**
   (belt laid ahead of the harvester), **O(1) +0.10** (same round),
   Bean counters +1.75, Pivot/Torsko +2.02-2.05, **us +2.25 — the slowest in the
   set.**
4. **WE ARE THE ONLY TEAM WHOSE BELT DOES NOT EXTEND OUTWARD.** Median d² from
   own core, first conveyor → last conveyor in r0-60: O(1) **4→37**, Bean
   counters 5→26, Pivot 13→29, Hugging Farce 13→37 — and **us 13→10.** Our last
   early conveyor is CLOSER to our core than our first. That is the signature of
   belt laid inward from wherever a builder happened to be standing, rather than
   a trunk grown outward from a fixed root.
5. **BELT-FIRST vs HARVESTER-FIRST IS A REAL SCHOOL SPLIT, NOT A RANKING.**
   Belt-first: O(1) 100%, Hugging Farce 100%, 0033 100%, kladde 96%,
   Ouroboros 74%, Leviathan 64%. Harvester-first: Pivot 0%, Torsko 0%,
   Erebus 0%, **us 0.3%**. **Both schools appear at the top of the r4 table**
   (O(1) belt-first r10; Pivot harvester-first r13), and §2.1 explains why:
   ordering alone is transit-neutral. **Do not spend a leg on ordering.**
6. **SPLITTERS ARE DEAD LEAGUE-WIDE. 880 splitter builds across 115,672
   team-sides.** Only Tyvrets (0.63/side) and Team imeto (0.43/side) use them at
   all; Hugging Farce has 1 ever; O(1), Pivot, Pantheon, SmartFridge and we have
   **exactly 0**. **A conveyor already accepts from three sides and outputs to
   one, so merging needs no splitter — splitters only SPLIT, which an economy
   feeding one core never wants. Closed; do not spend a leg on splitter
   topology.**

**NOT MEASURABLE from `events.tsv`** (stated rather than estimated): conveyor
FACING is not a column, so trunk flow direction and mis-oriented belts cannot be
checked in this cut — `harv wired` here is a geometric adjacency proxy. The
structural route-existence claim in §3 comes from the replay decode, which does
read facing.

**POPULATION CAVEAT:** the pooled cut is 62% unrated, and most unrated sides are
our own panel legs, so field teams' samples skew toward "their active bot when we
challenged them". The ladder-only cut (43,972 sides) reproduces the same
top-of-table ordering, so this does not drive the result.

---

## 5. THE CURRENCY: WHAT OUR ECONOMY COSTS AT THE KILL-RECIPE CLOCK

**Method (mine, this study):** cost scale is ONE global additive team factor —
every build adds (conveyor/splitter/barrier +1%, harvester +5%, launcher +10%,
builder bot/gunner/sentinel +20%) and **destruction removes the contribution**
(CLAUDE.md, engine-confirmed s26 `bots/_probe_scale`). So scale at round T is
reconstructible from `corpus/events.tsv` as `100 + Σ(BUILD weights ≤ T) −
Σ(DEATH weights ≤ T)`. **POPULATION: the 110 v155 RATED games (`join.tsv`),
both sides — a paired comparison on identical maps.**

| | US v155 | opponents, same games |
|---|---|---|
| **NET cost scale at r22** | **252%** | **222%** |
| NET cost scale at r50 | 272% | 258% |
| builder bots built by r22 | **5.79** | **4.29** |
| harvesters built by r22 | 3.15 | 2.37 |
| conveyors built by r22 | 11.0 | 10.55 |
| sentinels built by r22 | 0.51 | 0.17 |

⚠ **INFERRED, and it is the load-bearing decomposition of this study:** the
r22 scale gap is **30 points**, and **1.5 extra builder bodies at +20% each is
30 points.** Conveyors are level; harvesters account for ~4. **The opening
builder count IS the scale gap.** *(Not a formal attribution — the weights are
additive so the arithmetic is exact, but the counterfactual "we would have the
same economy with fewer bodies" is NOT established here and is precisely what
QUEUE `#62` exists to test.)*

**What the 30 points cost at the recipe's own clock:** a sentinel at r22 costs
`30 × 2.52 = 75 Ti` for us and `30 × 2.22 = 66 Ti` for them. Our median
DELIVERED titanium at r25 is **60 Ti**. **We are paying a ~9 Ti surcharge on
the first sentinel out of a delivered budget of 60 Ti** — plus the ~54 Ti the
fifth body itself cost.

⛔ **AND THE PRIORS ON `#62` MUST TRAVEL WITH THIS NUMBER, because they cut the
other way:** 9 of 10 losses in the original fitting sample never spawned a
SIXTH builder — the floor was shown to matter UPWARD; `_v69bc` read −13 points
for RAISING the target, and **the downward direction is UNTESTED, not shown
safe**; and our measured early idle is LOW (3.31% at r10), so the case for
fewer openers is PRICE, never idleness. **This study adds the price in the
programme's own currency and changes nothing about the risk.**

⚠ **THE TENSION THIS CREATES, stated because a ranked list that hides it is
useless:** a multi-builder chain mechanism wants MORE hands, and this section
says our bodies are the scale gap. **Those pull in opposite directions only if
"more hands on the chain" means "more bodies bought".** It need not: we already
buy five and put **three** on the economy (seat 0 leaves to raid at once, seat 4
defends). The resolution proposed in §7 is REALLOCATION, not procurement — and
§6.5(d) deflates the multi-builder prize independently, so the tension is
smaller than it looks here.
---


## 6. THE GAP DECOMPOSITION

**Instrument:** the same validated decoder, extended (`eco_fu.py`; artifacts
`fu_harv.tsv`, `fu_side.tsv`, `fu_outage.tsv`, `fu_repair.tsv` in the session
scratchpad). 715 files / 1,430 team-sides; v155 = 245 US sides from 49 matches;
the `deliveries*10 == titaniumCollected` control holds **1,430 / 1,430**.

### 6.1 THE 2-ROUNDS-PER-TILE MODEL IS CONFIRMED ON THE WIRE

Route length **L** = 4-connected BFS distance from the harvester tile to the
nearest tile orthogonally adjacent to our core footprint, computed from the
replay's own `Map.rows` (so it needs no external map table).

**MEASURED: connect latency ≈ 2.00 rounds per tile of L** (Theil-Sen, plus
binned medians out to L = 6). Decomposed: **build phase ~1.6L, transit ~0.4L.**
**This is the §2 engine arithmetic reproduced on 1,730 harvesters, and it is the
single most important number in the study: our economy's clock is
`2 x route length`, and the route length is chosen by an ore picker that does not
score route length.**

⚠ **The linear model UNDERESTIMATES past L ≈ 8** — at L = 10 the measured median
is **32 rounds against the model's 20**. Long routes degrade worse than linearly
(the builder is diverted, the chain is abandoned, the route is re-planned).
**Do NOT quote the OLS slope of 4.29** — it is dragged by that tail and is not
the per-tile rate.

⭐ **AND THE CONTROL THAT KILLS THE INNOCENT EXPLANATION: 0 of 1,730 harvesters
were terrain-unroutable.** Every single unconnected harvester **had a legal route
home that it never got.** Not geometry. Not walls. Not ore placement.

### 6.2 WHERE THE ROUNDS AND THE TITANIUM GO — the ranked contributors

| # | contributor | size | how measured |
|---|---|---|---|
| **1** | **TIME-TO-CONNECT (the 2L build phase)** | **the binding constraint** | FU4: once a harvester is structurally connected, **delivered / connected-emission = 1.037, i.e. ~100% of emission reaches the core.** Trunk saturation **EXCLUDED** — 0 rounds at the entry-tile cap. Destruction is second-order in r0-100. **The whole shortfall is time-to-connect plus outages.** |
| **2** | **THE NEVER-CONNECTED 25%** | **435 / 1,730 harvesters; THEM 13.7% in the same files — we strand at 2x their rate** | median side sinks **1 harvester + 4 belt tiles = 43 Ti base, pre-scale**; the upper quartile carries **+9 to +13 PERMANENT cost-scale points** from builds that never delivered anything |
| **3** | **SINGLE-BUILDER SERIALISATION** | **the 2 in "2L"** | engine floor (§2); field discriminator measured (§4.2): the fast wirers run up to **3 conveyor builds per round** with `adj≤2rnd` **0.41-0.48**, we run a max of **2** at **0.69** — one paving walk |
| **4** | **ROUTE LENGTH L ITSELF** | d² to own core rises 18 → 85 from harvester #1 to #6, and the connected share falls 92% → 64% across the same ordinals | §3.2; `_pick` scores ore by distance-from-core only, never by route length (§1) |
| **5** | **BELT DEATHS (not repair rate)** | **we take 3.1x more belt deaths than the opponents in the same games — 1,654 vs 529** | FU5 |
| 6 | WALK TIME / build ORDER | **~0** | §2.1: re-ordering a single builder's work is transit-neutral; §4.2: both schools appear at the top of the r4 table |
| 7 | TRUNK SATURATION | **0** | FU4, explicitly excluded — 0 rounds at the entry-tile cap |
| 8 | BUILDER ATTRITION | **~0** | §3.6 control: 74.9% connected in the 209 games with zero builder deaths by r60 |

### 6.3 THE REPAIR PRIOR DOES NOT SURVIVE VERSION-PINNING — retained so nobody re-derives it

A pooled corpus cut had us as the field's worst belt repairer. **Paired within the
same games and pinned to version, it is a wash: US 10.6% vs THEM 15.0%
repaired within 10 rounds, and v152 actually BEAT its opponents (20.5% vs
16.6%).** A possible v155 regression (20.5 → 12.9) is **reported, not banked** —
the opponent pools are disjoint.

**Cuts are bimodal: the ones that get repaired are repaired fast (median 4
rounds), but 68.5% are NEVER restored.** ⭐ **THE REAL ASYMMETRY THE RATE HID IS
EXPOSURE, NOT RESPONSE: 1,654 belt deaths against 529 in the same games.**
Improving the repair RATE is optimising the smaller quantity by 3:1.
*(Instrument note: the hostile-vs-self-demolition classifier discriminates —
0 of 1,654 of ours were self-demolished, against 18.2% of THEM at v152 — so
"they get cut less" is not an artefact of them tearing down their own belt.)*

### 6.4 THE COST SIDE OF THE SAME GAP

**Cost scale at r25: US 254% [247-260] vs THEM 225% [202-247], and 147 of our
154 added points are ECO.** ⇒ **every turret we buy at r25 costs ~13% more than
the opponent's turret in the same game.** The economy does not merely consume
titanium; **it inflates the price of the thing the titanium is for.** This is why
the ranked list below is dominated by *fewer, better-sited, always-connected*
harvesters rather than by *more, faster* ones.

---

### 6.5 THREE PRIORS THIS STUDY KILLED, AND ONE OF MY OWN READINGS IT CORRECTS

**Instrument:** a third decoder (`walk.py`) replaying `moveBuilderBot` to track
every builder's position every round. Build attribution is **100% DIRECT** — the
wire carries `BuilderBuild {id, target}` (Update field 16), so no adjacency
inference was needed: **116,775 direct / 0 fallback / 0 unattributed.**
**POPULATIONS:** our v155 rated (110 sides, 58,154 builder-rounds), v155 unrated
(135 / 70,709), v152 and v140 for era, and the 160 most recent archived games for
each of 11 field teams. Rated and unrated never pooled.

#### (a) CONVEYOR PASSABILITY — CONFIRMED ON THE WIRE, not taken from the doc

1,569,491 builder-round snapshots across **400 replays / 80 teams**:

| building type on the builder's own tile | co-occurrences | tile-rounds | rate |
|---|---:|---:|---:|
| **conveyor** | **598,393** | 7,859,733 | **7.61%** |
| **splitter** | **95** | 3,357 | **2.83%** |
| harvester | **0** | 1,196,894 | 0.000% |
| barrier | **0** | 661,420 | 0.000% |
| gunner / sentinel / launcher | **0** | 814,133 | 0.000% |
| core | **0** | 1,161,704 | 0.000% |

**Zero across 3,834,151 impassable-type tile-rounds.** Controls: the positive
control fires (conveyor 598k); a decode control shows the same code path resolves
positions correctly for the zero kinds (**1,846/1,846 harvesters land on
`ENV_ORE_TITANIUM`; 0/3,529 buildings land on `ENV_WALL`**); two independently
written scripts agree on the builder-round count to the unit. **The organisers'
doc is right here. Builders walk the belt they lay — every mechanism in §7 may
rely on it.**

#### (b) ⛔ CPU TIMEOUT IS DEAD AS AN EXPLANATION FOR THE SHIPPED BOT

Our own `eco.py:29-31` cites *"1,102 builder TLEs in 212 rounds on midgard (61% of
builder turns)"* from a v125-era instrumented run. **On the platform:
0 TLEs in 1,268,678 builder-turns across v140 + v152 + v155, rated and unrated,
r0-200.**

**The instrument is allowed to come out the other way and does:** the same parser
reads ~1,270 TLE'd builder-turns on the field in the same window
(**lingling_40h 1.26% of builder-turns r0-100, Erebus 1.11% in r101-200**, plus
Jython, kladde, 0033). `execTimeUs` is non-zero in 100% of BotOutput events —
these are platform replays, no fill artefact — and every builder-round carries
exactly one BotOutput, so the denominator is complete.

**And the LOKI-TURBO rewrite is visible in the tape**, which is why the citation
was true once: our p90 execution time on maps of area > 625 was **8,150 µs at
v140 (82% of the 10,000 µs budget — one map-size step from mass TLE)** and is
**350 µs at v155, a ~23x reduction**; p99 headroom went 12.5% free → **94.5%
free**.

⇒ **Two consequences. (1) "Make eco cheaper per turn" was already paid, between
v140 and v152; it is not part of this gap. (2) A CPU BUDGET IS NO LONGER A REASON
TO REFUSE A SMARTER ECO DECISION** — with 94.5% of the per-turn budget free at
p99, a route-length term in ore selection (M3 below) is affordable in a way it
demonstrably was not at v140. *(Caveat carried: this cannot confirm or refute the
61% figure FOR v125 — one map, one local run. It establishes only that it does
not describe the bot we ship.)*

#### (c) OUR IDLE ROUNDS ARE 100% POLICY — not cooldown, not CPU

**13.8% of our v155 rated builder-rounds in r0-100 are IDLE** (8,043 of 58,154).
`setActionCooldown` / `setMoveCooldown` take **the value 1 and only 1** (14,713 of
35,398 emissions on our builders; zero at any other value), and **100% of our
IDLE builder-rounds had BOTH cooldowns at 0 (8,043 / 8,043)**. **0.00% of them
carry `tled`.** The complement check reads the other way where it should —
lingling_40h's IDLE rounds are **27x** more TLE-loaded than its non-IDLE rounds —
so the test discriminates. ⇒ **every idle builder-round is a free, unblocked,
un-timed-out round the policy chose not to use.** (QUEUE `#70`'s premise,
measured on the current tree.)

#### (d) ⛔ CORRECTION TO MY OWN §4.2 READING #2 — I overstated it

§4.2 reads the belt-contiguity statistic as *"the fast group has more builders
laying at the same time; we run a single paving walk."* **Measured directly, that
framing does not survive.** Distinct builders per ≥4-tile conveyor chain in
r0-100:

| | mean builders/chain | 1 builder | 5+ builders | mean chain tiles |
|---|---:|---:|---:|---:|
| **us v155 rated** (217 chains) | **2.11** | 38.7% | 0.0% | 13.9 |
| sporks | **3.10** | 22.3% | **20.7%** | 18.8 |
| 0033 | 2.65 | 16.3% | 5.3% | 15.7 |
| Torsko | 2.57 | 27.8% | 1.0% | **21.8** |
| kladde | 2.49 | 23.3% | 5.4% | 17.0 |
| **SmartFridge** | **1.45** | 54.6% | 0.0% | 16.2 |
| **lingling_40h** | **1.51** | 50.9% | 0.0% | 13.2 |
| **team lazy** | **1.52** | 60.5% | 0.0% | 10.6 |

**We are MID-FIELD at 2.11.** Six teams beat us; four are worse — including two
of the teams the study set out to copy. **The leaders' edge is the TAIL** (sporks
puts 5+ builders on 20.7% of its chains; we never exceed 4) **and TOTAL PAVING**
(Torsko lays 21.8-tile chains to our 13.9 and builds on **13.7% of its
builder-rounds against our 8.2%**).

⇒ **The multi-builder mechanism (`#66`) is REAL but its headroom is SMALLER than
the contiguity statistic implied. It is ranked accordingly in §7, below the two
mechanisms whose evidence is direct.** Both statistics are MEASURED; they answer
different questions, and the one that answers *this* question is the
builders-per-chain count. **Written down rather than quietly dropped, because the
contiguity reading is the more quotable of the two and would have been wrong.**

#### (e) THE 2-ROUNDS-PER-TILE FLOOR IS UNIVERSAL — nobody has a faster primitive

Median rounds between consecutive conveyor builds by the SAME builder, r0-100:
**2 for 16 of 17 populations** (Erebus is the sole outlier at 3). And **gap = 0
occurs 6 times in ~70,000 pairs (0.009%), never on our side** — one action per
builder-turn, confirmed on the wire.

⭐ **AND SAMESTOP IS FIRING, VISIBLY:** the g = 1 share (build, don't move, build
the other adjacent tile) went **1.0% at v152 → 11.5% at v155** — the largest
per-builder rate change in the table, against **kladde 9.2%, Torsko 6.5%, and ten
field teams at or below 3.3%.** **The shipped `#50` plank is not just present, it
has moved us to the top of the field on its own statistic.** *(This is the
observational confirmation `#50` was still owed.)*

#### (f) PER-SEAT — seat 4 is not a free front, but it is the worst walker we own

Spawn ordinal is a wire-visible proxy for seat (`main.py:426` assigns by first-run
order). **INFERRED mapping; the store is not readable from the wire** — but it
validates itself: **ordinals 0 and 5+ place exactly ZERO conveyors and ZERO
harvesters in r0-60 and sit at d² ≈ 180** (raiding), while ordinals 1-4 place all
2,458 conveyors and all 514 harvesters at d² 12-40.

| ord (seat) | BUILD% | MOVE% | IDLE% | conveyors | median d² to core | **OSC2 % of moves** |
|---|---:|---:|---:|---:|---:|---:|
| 0 (raider) | 6.9 | 70.2 | 8.5 | **0** | 184.5 | 6.3 |
| 1 (eco) | **16.5** | 72.0 | 4.4 | 875 | 18.5 | 18.9 |
| 2 (eco) | 13.6 | 70.6 | 4.8 | 710 | 20.5 | 18.8 |
| 3 (eco) | 11.4 | 68.0 | 9.1 | 550 | 40.5 | 7.8 |
| **4 (defender)** | **7.6** | 72.4 | 9.4 | **323** | **12.5** | **20.4** |
| 5+ | 2.1 | 77.8 | 9.0 | **0** | 182.5 | 8.9 |

**Seat 4 is NOT idle** (9.4%, same as seat 3) and it **already paves** (~2.9
conveyors + 0.7 harvesters per game). **But it spends 72.4% of its rounds moving
while sitting at d² = 12.5 from our own core — it is pacing in place, with the
highest oscillation of any seat.** ⇒ **the free capacity at the core end of the
trunk is not seat 4's idle time; it is seat 4's WASTED MOVEMENT** — roughly
**890 builder-rounds per 110 games** (0.204 x 0.724 of its rounds), on a body
already standing where the trunk's core end needs building.

#### (g) OSCILLATION — we are at field parity now, and the era shows why

A→B→A returns, as a share of builder-rounds, r0-100:

| | v140 rated | v152 rated | **v155 rated** | field median (11 teams) | best |
|---|---:|---:|---:|---:|---:|
| OSC2 | **20.5%** | 15.1% | **12.0%** | **10.0%** | **team lazy 2.1%, Torsko 5.2%** |

**Already halved between v140 and v155** (the v140→v155 drop on n ≈ 190k / 58k
builder-rounds is far outside any plausible DEFF inflation). **The remaining
12.0% is at field PARITY, not an outlier — the 12.0 vs 10.0 gap is NOT a
significant difference and must not be quoted as one.** But **team lazy at 2.1%
and Torsko at 5.2% bound the reachable headroom at roughly 7-10pp of ALL
builder-rounds**, and that headroom is real regardless of where the median sits.

### 6.6 AMENDMENT TO §6.3 — name the estimator, and repair is a STYLE variable

Two independent pipelines read the repair question and **both are correct because
they answer different questions. Any sentence quoting a repair number must name
its estimator:**

* **PER-GAME SIGN TEST** (paired within the same games — the estimator §6.3
  quotes): **a wash**, US 10.6% vs THEM 15.0% within 10 rounds, per-game signs
  21/23/14.
* **POOLED RATE** over the same games: a **consistent small deficit**, 12.2% vs
  17.9%.

Two-pipeline-replicated and safe to cite: **v152 OUT-repaired its opponents
(20.5% vs ~16%)**; the **belt-death asymmetry generalises to our whole history —
2.58x lifetime, 3.25x at v155**; and ⭐ **repair rate is a STYLE variable, not a
quality one: r(rating, repair rate) = −0.062, with Jython at 28% and sporks at
70%.**

⇒ **If belt repair or belt-death avoidance appears in a ranked list, it must be
justified by MEASURED OUTAGE TITANIUM and nothing else.** "The field repairs more
than we do" is not an argument — the field's repair rate does not predict the
field's rating. §7 ranks it on that basis.

---

## 7. RANKED MECHANISMS — by expected tempo gain per unit of implementation risk

**Ranking rule:** expected effect on **time-to-connect and on cost scale at the
r22-r28 sentinel clock**, divided by implementation risk against the shipped
tree. Every entry names (a) the change, (b) the measurement backing the expected
saving, (c) the interaction with SAMESTOP / TURBO / BODYAWARE, (d) how a
**one-game demo** verifies it FIRES (not that it works — that needs a screen).

⛔ **Nothing here is a prereg and nothing here is a verdict.** Expected savings
are **INFERRED** from MEASURED inputs; they are sizing, not predictions, and each
carries the clustering caveat (team-side rows share match and opponent; rated
DEFF 1.529 pooled / 1.366 within-opponent before any bar).

---

### ⭐ M1 — COMMIT-BEFORE-YOU-DIG: never place a harvester you have not committed to wiring, and adopt orphaned chains

**THE CHANGE.** Two halves, and the second is what makes the first safe.
1. **GATE the harvester build** in `_expand` (`eco.py:1676-1700`) on a
   *route commitment*: `_link_path` is already computed for the SAMESTOP stop-tile
   preference (`_samestop_plan`, `eco.py:852`, **cached per ore tile**), so the
   route is in hand *before* the build with no new BFS. Refuse the build when the
   route is longer than a budget (a `MAX_LINK_TILES` constant), or when the bank
   cannot cover `harvester + len(route) x conveyor` at current scale.
2. **ADOPT ORPHANED CHAINS.** An eco builder with an empty `link_queue` that sees
   a friendly harvester with no route home re-plans and lays the rest. Today
   `link_queue` is per-builder instance state with **no hand-off**, and
   `_l4_repair` explicitly refuses the case — its own docstring
   (`eco.py:1050-1062`) names them *"DEAD HEADS: chains this bot abandoned
   mid-walk, which `_build_next_link` never returns to because it pops its queue
   as it lays it."*

**BACKING.** **435 of 1,730 v155 harvesters (25.1%) never connect**, against the
opponents' **13.7% in the same 245 games** — we strand at **2x their rate**.
**0 of 1,730 were terrain-unroutable** (§6.1): every one had a legal route.
**Not attrition** — 74.9% connected in the 209 games with zero builder deaths by
r60 (§3.6). Median side sinks **1 harvester + 4 belt tiles = 43 Ti base,
pre-scale**; the upper quartile carries **+9 to +13 PERMANENT cost-scale points**
from builds that never delivered anything (FU2). At r25 our scale is **254% vs
their 225%**, of which **147 of our 154 added points are eco** (FU3).

**EXPECTED SAVING (INFERRED).** Closing half the gap to the opponents' 13.7%
recovers **~0.9 harvesters + ~4 belt tiles per game ≈ 45-70 Ti at scale**, and
**~5-6 cost-scale points**, arriving *before* the first sentinel. At the measured
r25 prices that is **most of one sentinel per game.** No delivery is lost by
refusing an unwireable site — by construction it delivered nothing.

**RISK / INTERACTION.** **Medium-low.** SAMESTOP is untouched (it reads the same
`plan`; if the gate refuses, no harvester is built and nothing is armed). TURBO
untouched. BODYAWARE untouched. ⚠ **The real risk is the gate firing too often
and shrinking the economy** — `ECO_CAP = 18` is an absolute integer and the gate
would bind below it on big maps. **Mitigation: budget the route in TILES, and
make the refusal a DEFERRAL (re-pick a nearer ore), never an abandonment.**
⚠ **Do not implement half 1 without half 2**: a gate alone leaves the existing
dead heads on the map.

**ONE-GAME DEMO THAT IT FIRED.** Decode one local game with `eco_timeline.py`
and read `n_harv_connected / n_harv_built`: the arm must show **no harvester with
a blank `connect_rnd`** whose BFS route length was inside the budget at build
time. Positive control: the same game on the parent must show at least one.
*(Do NOT plan to read a `print()` tag out of a platform replay — stdout is
stripped, 30,664/30,664.)*

---

### ⭐ M2 — THE FREE ROUND: kill the blind backstep, and give the idle builder a verb

**THE CHANGE.** Port the anti-oscillation guard that **already exists in this
tree for a different unit**: `rot_prev_dir` (`main.py:117` init, `main.py:791`
`if want == self.rot_prev_dir`, set at `:850` / `:867`) is a live A→B→A edge
guard — **on GUNNER ROTATION.** `_nav` (`eco.py:1458`) has no equivalent: it
counts a BACKSTEP as a successful move (`:1467`) and `self.stuck` increments only
when **all four** cardinals fail (`:1470`), so the escape hatch (`:1810`) can
never fire inside an oscillation. **This is a PORT with an in-tree template, not
a design** — and QUEUE `#54` is explicit that it must change NAVIGATION, not add
a third detector.

**BACKING.** **12.0% of our v155 rated builder-rounds are A→B→A oscillation**
(58,154 builder-rounds / 110 sides; 11.2% unrated), plus **13.8% IDLE that is
100% policy** — cooldowns 0 in **8,043 / 8,043** idle rounds and `tled` in
**0.00%** of them (§6.5c). Together **~26% of our eco-phase builder-rounds
produce nothing.** Bounds: **team lazy 2.1%, Torsko 5.2%** ⇒ **7-10pp of ALL
builder-rounds is reachable headroom.** **Seat 4 is the worst offender: 20.4% of
its moves are A→B→A while it sits at d² = 12.5 from our own core — ~890
builder-rounds per 110 games, on a body already standing on the trunk's core end**
(§6.5f). And build density is where this cashes out: **Torsko builds on 13.7% of
its builder-rounds against our 8.2%.**

**EXPECTED SAVING (INFERRED).** Converting even a third of the reachable
oscillation headroom into builds at our current 8.2% build rate is **~2-3
additional builds per builder per 100 rounds**; on the chain that is
**1-1.5 tiles = 2-3 rounds off time-to-connect per chain**, and it is the same
mechanism on every chain in the game rather than one.

**RISK / INTERACTION.** **LOW on blast radius, MEDIUM on precedent.** ⛔ **Two
detect-and-repick arms have already died (OSCLOCK 48.53, OSCLOCK2)** and the
home-lock report gives the source reason they could not have worked. **This is
NOT a third detector** — it is a move-legality guard inside `_nav` that refuses
the immediate reverse edge unless it is the only legal move. ⚠ **It touches
`_bfs_direction`'s consumer, which is the hand-merged TURBO x BODYAWARE block
(`eco.py:1236-1456`)** — the highest-risk file region in the tree, and
⛔ **CORRECTED 2026-08-17 (s48 wrap-fix): this sentence used to read *"`tools/
turbo_identity.py` exists precisely to assert that block's behaviour is
unchanged — run it"*, and `tools/turbo_identity.py` DOES NOT EXIST.** `ls` finds
no such file and `git log --all -- tools/turbo_identity.py` returns nothing, so
it has never been in this checkout in any commit; the name came in with x3r0's
v152 notes and was copied forward through ~25 bot trees and this study unread.
**THE INSTRUMENT THAT ACTUALLY COVERS THIS SEAM IS
`scratchpad/s48_flagoff.sh`** — replay-SHA-256 flag-off equivalence for the
whole bot's move sequence (not two functions in isolation), under the
`NOISE_ON=False` + `--tle 0` determinism precondition, with the flag-ON run as
its positive control. **Run that.** Driven 2026-08-17 over 8 cells: flag-off ==
base 8/8, flag-on != base 8/8.

**ONE-GAME DEMO THAT IT FIRED.** Replay one local game through `walk.py` and read
the OSC2 share of moves: the arm must land materially below the parent's ~20% on
the same seed and map, with the builder-round count identical. Negative control:
a corridor map where the only legal move IS the reverse — the guard must NOT fire
there, or it will lock builders in dead ends.

---

### ⭐ M3 — SCORE ORE BY ROUTE LENGTH, NOT BY DISTANCE FROM THE CORE

**THE CHANGE.** `_pick` (`eco.py:1196-1207`) sorts ore by
`abs(t.x - core.x) + abs(t.y - core.y)` — **straight-line Manhattan distance,
which is not the route the builder must then BUILD.** Score candidate ore by the
`_link_path` length instead (or by Manhattan plus a wall-penalty), and prefer the
ore whose route is shortest **after crediting tiles already covered by existing
belt** (which is M4's edge weighting; the two compose).

**BACKING.** **Connect latency is ~2.00 rounds per tile of BFS route length**
(Theil-Sen plus binned medians to L = 6, 1,730 harvesters) and **degrades worse
than linearly past L ≈ 8 — at L = 10 the measured median is 32 rounds against the
model's 20** (§6.1). And route length is exactly what deteriorates by ordinal:
d² to our core runs **18 → 25 → 37 → 50 → 61 → 85** for harvesters #1-#6 while the
ever-connected share falls **92% → 91% → 81% → 71% → 66% → 64%** (§3.2). ⭐ **The
CPU objection is now dead and measured: p99 execution time is 550 µs against a
10,000 µs budget — 94.5% free** (§6.5b). At v140, when p90 on big maps was
8,150 µs, this change would have been reckless. It is not now.

**EXPECTED SAVING (INFERRED).** Cutting median L by 2 tiles on harvesters #3-#6
is **~4 rounds of time-to-connect each**, and it moves those harvesters out of the
superlinear tail where the never-connect rate lives.

**RISK / INTERACTION.** **LOW-MEDIUM.** Purely a scoring change inside `_pick`;
the ore PARTITION across seats (which keeps builders off one deposit) is
preserved. ⚠ **Watch clustering: a route-length score pulls all seats toward the
same near cluster** — keep the `[worker::workers]` stripe, and note that our
stripe already wastes one of four lanes (eco seats are 1-3 → workers 0-2 of 4;
lane 3 is only ever worked by a stood-down raider). ⚠ Cost: one extra
`_link_path` per candidate ore; the cache is per-ore-tile, so bound the candidate
list.

**ONE-GAME DEMO THAT IT FIRED.** `eco_timeline.py` on one local game: the arm's
harvesters #3-#6 must have strictly lower median BFS route length than the
parent's on the same map and seed, with the same number of harvesters built.

---

### M4 — ROUTE THROUGH THE BELT WE ALREADY OWN (QUEUE `#78` mechanism (a))

**THE CHANGE.** `_link_path`'s flood is UNWEIGHTED: friendly belt tiles are
routable but not PREFERRED. Make an existing friendly conveyor/splitter tile
**cost 0** (0-1 BFS / deque-front insertion) so a new harvester's route merges
into the existing trunk instead of running a parallel line. `_build_next_link`
already pops occupied tiles, so a reused tile costs zero rounds and zero titanium.

**BACKING.** Sized already: **~8.9 conveyors/game saved (calibrated ~8.1) = ~7.2pp
of cost scale by r150 = ~78 Ti = ~0.8-1.3 extra turrets**
(`BELT-TOPOLOGY-CENSUS-2026-08-16.md`, our own 360 v140 ladder games, with a v104
out-of-sample read). And **fewer NEW tiles is directly fewer 2-round build
steps**, which the census did not claim but §6.1 licenses.
⭐ **THIS STUDY REMOVES ITS NAMED COUNTER-COST.** The census flagged that merging
pushes the busiest belt tile over its throughput ceiling in 126/360 games.
**FU4 measured trunk saturation on the current tree at ZERO rounds at the
entry-tile cap, and delivered/connected-emission at 1.037 — once a harvester is
connected, ~100% of its emission reaches the core.** We are nowhere near the
ceiling. *(That is an update to `#78`'s hedge, not a repeal: the census measured
the POST-MERGE busiest tile and this measures the PRE-MERGE one. The right form
is "the pre-merge network has no saturation to trade away", and the post-merge
ceiling still has to be watched in the screen.)*

**RISK / INTERACTION.** **MEDIUM.** It changes `_link_path`, which SAMESTOP reads
(`_samestop_plan` calls it verbatim, deliberately, so as not to invent a parallel
router) — so a change here silently changes SAMESTOP's stop tile too. **That is a
composition to state in the prereg, not a bug.** ⛔ **CORRECTED 2026-08-17 (s48
wrap-fix): this warning used to say *"`tools/turbo_identity.py` asserts
`_link_path` is behaviour-identical to LOKI's… the tool's expectation must be
updated"*. THAT TOOL DOES NOT EXIST AND NEVER DID** (`ls` finds nothing;
`git log --all --` on the path returns nothing) — so there was no expectation to
update, and the mitigation as written was unexecutable. **The live seam
instrument is `scratchpad/s48_flagoff.sh`, and the warning it earns is the
opposite shape: flag-ON runs of ROUTESCORE MUST differ from the base (that is
the harness's positive control, and this arm is exactly why), while its
flag-OFF run must still be byte-identical — which is what checks that the
`_link_path` change is confined to the flag.**

**ONE-GAME DEMO THAT IT FIRED.** One local game: total conveyors built must fall
while `n_harv_connected` holds, and at least one harvester's route must
demonstrably terminate on a pre-existing belt tile rather than at the core ring.

---

### M5 — MULTI-BUILDER CHAIN CREW (QUEUE `#66`) — real, but smaller than it looks

**THE CHANGE.** A second eco builder joins an existing chain instead of starting
its own. Deterministic split needs no negotiation: both builders compute the same
`_link_path` from the same harvester tile (pure function of map + core + ore), and
seat parity decides who works the harvester end and who works the core end.
⭐ **AND THE ROW'S NAMED BLOCKER IS FALSE — verified by hand here, not relayed:
`SLOT_DEFEND_BEAT = 13` (`doctrine.py:959`) is defined and NEVER read or written
anywhere in the tree** (0 hits outside `doctrine.py`; 0 raw-integer `read_store` /
`write_store` calls). **A crew channel needs neither an eviction nor a bit-pack.**

**BACKING, WITH ITS OWN DEFLATION.** The engine model says two builders halve the
2L build phase (§2.1). ⛔ **But we are already at 2.11 distinct builders per
≥4-tile chain — MID-FIELD** (§6.5d). Six teams beat us and four are worse,
including SmartFridge (1.45) and lingling_40h (1.51). **The leaders' edge is the
TAIL (sporks: 5+ builders on 20.7% of chains; we never exceed 4) and TOTAL PAVING
(Torsko 21.8-tile chains to our 13.9).** ⇒ **the prize is not "go from 1 to 2"; it
is "go from an accidental 2 to a deliberate 2-3 on the LONG chains only."**

**RISK / INTERACTION.** **MEDIUM-HIGH.** It is the largest behavioural change in
this list, it needs new shared state (however cheap), and its own row already
notes the long-haul segment {midgard, ragnarok, fjordgate} shares ground with
`#63` and SPAWNPOCKET. **Ranked below M1-M4 because M1 and M2 recover more
builder-rounds for far less machinery, and because M3/M4 shrink L, which shrinks
the very quantity this mechanism splits.** ⇒ **build M3/M4 first and re-measure:
if L falls enough, this row's prize falls with it.**

**ONE-GAME DEMO THAT IT FIRED.** `walk.py` on one local game: the target chain's
distinct-builder count must exceed the parent's, with the chain's completion round
strictly earlier on the same seed and map.

---

### M6 — FEWER OPENING BUILDERS (QUEUE `#62`) — the biggest scale lever and the riskiest

**THE CHANGE.** `LOKI_BASE_BUILDERS = 5` (`doctrine.py:1195`) is unconditional and
map-blind. Make the opening size a function of map area and delivered-Ti income.
**The scale-UP path above 5 already exists and is income-gated (`doctrine.py:97`);
nothing can start below the constant.**

**BACKING.** **The opening builder count IS the r22 scale gap: net scale 252% vs
the opponents' 222% in the same 110 rated games, and 1.5 extra bodies at +20% is
exactly 30 points** (§5). A sentinel at r22 costs us 75 Ti against their 66, out
of a **delivered budget of 60 Ti at r25** — plus the ~54 Ti the fifth body itself
cost.

⛔ **AND THE PRIORS RUN THE OTHER WAY, so this is ranked on RISK, not on size.**
9 of 10 losses in the original fitting sample never spawned a SIXTH builder — the
floor was shown to matter **UPWARD**; `_v69bc` read **−13 points for RAISING** the
target and **the downward direction is UNTESTED, not shown safe**; our measured
early idle is low at r10, so **the case is PRICE, never idleness**. ⚠ **And it
opposes M5 directly: fewer bodies is fewer hands on the chain.** ⇒ **Do not build
M6 and M5 in the same shard.**

**ONE-GAME DEMO THAT IT FIRED.** Trivial (count builder spawns before the first
harvester) — **which is exactly why this row needs a SCREEN, not a demo.** The
demo verifies nothing that is in doubt.

---

### M7 — BELT-DEATH AVOIDANCE — ranked last, and only on outage titanium

**THE CHANGE.** Route the trunk away from the lanes where it is being shredded
(a routing-cost term, not a repair rule) — this composes with M4's weighting.

**BACKING, AND ITS LIMIT.** **We take 3.1x more belt deaths than the opponents in
the same games (1,654 vs 529), and 2.58x lifetime / 3.25x at v155**
(two-pipeline-replicated). **68.5% of cuts are NEVER restored**, though the ones
that are get fixed fast (median 4 rounds). ⛔ **But the repair-RATE framing is
dead: paired per-game it is a wash (US 10.6% vs THEM 15.0%, signs 21/23/14) while
the pooled rate reads a small deficit (12.2% vs 17.9%) — name the estimator — and
`r(rating, repair rate) = −0.062` with Jython at 28% and sporks at 70%.**
**Repair rate is a STYLE variable, not a quality one.**

⇒ **This row may ONLY be justified by MEASURED OUTAGE TITANIUM, which this study
did not size** (`fu_outage.tsv` has the series; the Ti conversion was not
computed). **NOT MEASURED here: how many delivered stacks the 68.5% never-restored
cuts actually cost.** Compute that before anyone builds this.

⚠ **DEFENCE-CLASS.** Under `PLAY_DEFENCE: not_at_the_kill_s_expense` this carries
`DEFENCE_ADMISSION_BAR`: the r300 timely-kill share must not fall, **restated as
an EXCLUSION before the DEFF correction is applied** (a fail-to-exclude null here
would be laundered into a confident one otherwise).

---

## 8. ROADS THIS STUDY CLOSES — retained so nobody re-derives them

| road | status | evidence |
|---|---|---|
| **Pave-the-walk-out / belt-first vs harvester-first ORDERING** | **CLOSED — transit-neutral** | §2.1 arithmetic; and both schools sit at the top of the r4 table (O(1) belt-first r10, Pivot harvester-first r13) |
| **SPLITTERS in our economy** | **CLOSED — dead league-wide** | 880 splitter builds across 115,672 team-sides; O(1), Pivot, SmartFridge and we build exactly 0. A conveyor already accepts from 3 sides and outputs to 1, so merging needs no splitter |
| **Per-harvester lines vs one trunk** | **CLOSED — we already have the field's topology** | components/harvester 0.42-0.77 for every team measured; ours 0.53 |
| **CPU / TLE as an eco cost** | **CLOSED for the shipped bot** | 0 TLEs in 1,268,678 builder-turns (v140+v152+v155); instrument fires on the field (lingling_40h 1.26%) |
| **Trunk throughput saturation** | **CLOSED — 0 rounds at the entry-tile cap** | FU4; delivered/connected-emission = 1.037 |
| **Builder attrition as the cause of unwired harvesters** | **CLOSED** | 74.9% connected in the 209 games with zero builder deaths by r60 |
| **A faster walk-and-build primitive existing somewhere in the field** | **CLOSED** | median same-builder conveyor gap = 2 for 16 of 17 populations; gap = 0 occurs 6 times in ~70,000 pairs |
| **Terrain / ore placement as the cause of unwired harvesters** | **CLOSED** | 0 of 1,730 harvesters were terrain-unroutable |
| **"We run one paving walk, they run several"** | **RETRACTED — my own §4.2 reading** | we are 2.11 builders/chain, mid-field; §6.5d |
| **"We are the field's worst belt repairer"** | **RETRACTED — pooled-era artefact** | version-pinned and paired, it is a wash; v152 out-repaired its opponents |

## 9. WHAT WAS NOT MEASURABLE

* **Which harvester a given delivered stack came from.** `ResourceMove` carries
  `{from, to, resourceId}` for a single hop and stack ids are not traced end to
  end. This is why the headline latency is per-GAME and the per-harvester column
  is a route-EXISTENCE claim.
* **The comms store**, so the ordinal → seat mapping in §6.5f is INFERRED (it
  validates itself behaviourally: ordinals 0 and 5+ place zero eco buildings).
* **Which of the four cardinal moves `_nav` attempted and rejected**, and whether
  an IDLE round was a deliberate hold or a failed plan.
* **Conveyor FACING in `corpus/events.tsv`** — the field cut's "harvester wired"
  is a geometric adjacency proxy; only the replay decode reads facing.
* **Outage titanium** (M7's only admissible justification). The series exists in
  `fu_outage.tsv`; the conversion to delivered stacks was not run.

## 10. ARTIFACTS

All in the session scratchpad (nothing written into the repo but this file):
`eco_timeline.py` + `eco_harvesters.tsv` (8,415 rows) + `eco_curve.tsv` (1,430
rows) · `eco_fu.py` + `fu_harv.tsv` / `fu_side.tsv` / `fu_outage.tsv` /
`fu_repair.tsv` · `walk.py` + `main.tsv` / `main200.tsv` / `q1.tsv` + the control
scripts `ctrl.py` / `cool.py` / `seat.py` / `q1norm.py` · `pass1.py` +
`sides.tsv` (115,672 rows) + `table_recent200_area500_700.tsv`.
**Scratchpads die with the session — re-derivation instructions are in §3, §4 and
§6.5, and every population rule is stated in full.**

---

## AMENDMENT (builder s48, 2026-08-17 ~05:1xZ) — §3.5's slope: REPLICATED; its funding-physics reading: REFUTED

Two-decoder resolution (research's hybrid derivation, events.tsv y independently
decoded, join driven against a seat-swap control 1,405/1,405 vs 9.86%):
* **The number replicates on the like-for-like cell**: v155+rated+named-map
  reads **+1.164 (n=92, 13 maps)** against this report's +1.171 (n=82). It does
  **NOT generalise**: v152 same estimator +0.809 (n=333).
* ⛔ **The funding-physics mechanism is DEAD, by the pre-specified test**: if the
  slope were engine funding physics it must hold for OPPONENTS who gate
  sentinels on bank. Sentinel-led opponents (≥2.61 sent/game, 42 teams) read
  **−0.122 (n=237)**; the complement −0.039 (n=143). Composition does not
  rescue it. ⇒ the coupling is a property of **our v155 sequencing**, not of
  the game. Do NOT quote §3.5 as "eco latency IS the kill clock" — the
  supported form is "in v155, our sentinel timing tracks our delivery timing
  ~1:1; it did so less strongly in v152; the mechanism is our build order."
* Constraint for any decoupling arm: KLADLADDER (standing sentinel funding
  priority + reserve-floor waiver — a commitment-form decoupling) read 42.07%
  ± 1.73 at its n=3,121 interim vs Sleipnir. The commitment FORM of
  decoupling is heading for its registered falsifier; successor arms must
  take a different shape.

### AMENDMENT 2 (builder s48, ~05:2xZ) — the amendment above quoted the replication WITHOUT its interval; the interval unmakes the headline cell

Match-cluster bootstrap (2,000 resamples, clusters = MATCH id, seeded; research):
* **v155 cell (this report's headline): +1.164/+1.171 point, 92 sides from only
  22 MATCHES → 95% [−14.712, +1.846]. DOES NOT EXCLUDE ZERO.** The point
  estimate replicates across two decoders and is still a point estimate
  without a measurement behind it.
* **The only MEASURED cell is v152: +0.809 [+0.234, +1.019], 72 matches** —
  the association is established on the OLD bot only; the v155 coupling is
  UNMEASURED until the archive reaches an adequate match count (it will on
  its own as v155 accumulates rated games).
* The THEM-side funding-physics refutation (sentinel-led −0.122, n=237) is
  UNAFFECTED — it has the matches behind it.
* "Sleipnir raised the coupling" (0.809→1.164) is RETRACTED — intervals
  overlap over essentially their whole range.
⇒ Do not quote ANY v155 slope from this report. Method rule this bought
(research's, routed): any estimator off platform games gets a MATCH-cluster
bootstrap before being quoted — the DEFF constants are for shares; a slope
needs its own clustering treatment, and 92 games/22 matches is m̄=4.2.
