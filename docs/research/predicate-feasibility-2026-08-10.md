# Sizing the upstream walk — is the "finish unterminated lines, AIMED" predicate affordable?

**Research arm, session 28. Decoded 2026-08-10. Direct successor to
`repair-class-costing-2026-08-10.md`, which priced the plank at +411 Ti/game against −223
executed naively, and named the discriminator — *walk upstream from a dead end; if the chain
reaches a friendly harvester, finish it* — without sizing it.**

**Population: 220 v102 our-side LADDER replay files, 44 matches, `related == none`. Seat and
version read from `replay_archive/*.meta.json` (`teamAId` / `teamAVersion`), never from
`winnerSide` — TRAP 7 does not apply. Frozen file list `pop_v102.tsv`, sha256
`443a2442d2a0247b6bdd427990549b8444cbe421f7b1c9da26c51a1ed6b07733` (the archive stands at
9,599 `.replay26`; it grew 210→220 v102 files since the costing froze its list, so the two
denominators are close but not identical and are never differenced). Median game 187 rounds;
58,165 rounds decoded, 0 errors. Fixture: LADDER. No downloads. No bot, arena, prereg or
coordination file touched.**

**Seat verified behaviourally, not by any winner-derived field**: our-side `builderAttack`
= **0** across all 220 files against **12,815** on the opponents' side — LOKI-8's silenced-melee
fingerprint, the independent check `corpus-howto.md` prescribes for TRAP 7.

---

## 0. The four numbers, and the verdict

**Subject: our conveyor network. Population: 220 v102 our-side ladder games. Unit: one
dead-end evaluation — one dead end, walked once, at one topology-change round. Denominator:
49,409 evaluations over 8,427 topology-change rounds in 220 games. Fixture: LADDER.**

| # | question | answer |
| --- | --- | --- |
| **1** | **chain length upstream from a dead end** | **median 0 hops, p90 4, p99 11, MAX 31** — nodes visited median 1, p90 5, p99 14, **MAX 34** |
| **2** | **dead ends per topology change / per game** | **median 4 per change** (p90 13, p99 25, MAX 31); **median 107 evaluations and 22 distinct sites per game** |
| **3** | **cycle reachability from a dead end** | **0.0000% (0 / 49,409) for an acceptance-checked walk — 2.22% (1,096 / 49,409) for the naive one** |
| **4** | **topology changes per game** | **median 37 events** (33 builds + 2 removals), landing in **median 32 rounds**; **65.2% of them before round 100** |

**Affordability at the one-walk-per-topology-change cadence: YES, by three orders of
magnitude, and CPU is not the thing that should worry anyone.**

Timed on the real topologies, enumerating every dead end and walking every one of them costs
**median 15.6 µs, p90 59.8 µs, p99 113.4 µs, MAX 436.6 µs** of a **10,000 µs** per-unit budget.
The worst topology-change round in 220 games spends **4.4%** of one turn.

**And the cadence question the brief asked me to settle is moot: neither term dominates,
because both are negligible.** One walk per change is 38 change-rounds × 15.6 µs ≈ **0.6 ms of
CPU per GAME**. The rejected design — every builder, every turn — is ~2,197 our-unit-turns per
game × 15.6 µs ≈ **34 ms per game**, i.e. still *median 15.6 µs and worst-case 437 µs inside any
single turn*, because the cost is per-turn, not cumulative. **The sweep-19 store design is
correct for other reasons; it does not need a CPU argument, and I would not make one.**

**What should worry someone is §6.** `docs/game-model.md:449`, measured in this repo on
2026-08-08: `get_tile_env()`, `is_tile_passable()` and `get_tile_building_id()` **raise
`GameError: Position out of vision range`** for an in-bounds tile the caller cannot see, and an
uncaught `GameError` **permanently destroys the unit for the rest of the match**. **7.08% of the
walks measured here do not fit inside a builder's r²=20** — 3,498 walks in **123 of 220 games**.
**The predicate's binding constraint is vision, not CPU, and the failure mode is a dead builder
rather than a lost turn.**

**And §7 is the one that touches the +411.** The stated discriminator passes **46.5%** of
unterminated ends on the population that reconciles to the costing's census, against the
costing's **8.5% profitable**. **It is 5.5× wider than the subset +411 was priced on.**

---

## 1. Chain length — the tail is short, and the median is zero

**Definition.** From a dead-end carrier tile, step to every friendly carrier that pushes into
it, then to their feeders, and so on until nothing is left. **Depth** is the longest upstream
hop count; **nodes** is how many carrier tiles the walk touches, which is the quantity that
costs. The walk stops at a friendly harvester (that is the verdict) or at a carrier nobody
feeds.

**The costing's "the corking end sits ~3 conveyors from the core" is a distance to the SINK and
is not reused here. This walk goes the other way and the numbers are different.**

| measure | n | median | p90 | p99 | MAX | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **depth (hops), per evaluation** | 49,409 | **0** | 4 | 11 | **31** | 1.16 |
| **nodes visited, per evaluation** | 49,409 | **1** | 5 | 14 | **34** | 2.28 |
| depth, per distinct site (6,221) | 6,221 | 1 | 6 | 15 | 31 | 2.04 |
| nodes, per distinct site | 6,221 | 2 | 7 | 18 | 34 | 3.13 |
| **short-circuit nodes** (stop at first harvester — what a real predicate does) | 49,409 | **1** | 4 | 12 | **32** | 2.07 |
| short-circuit depth | 49,409 | 0 | 3 | 8 | 31 | 0.97 |

**60.2% of evaluations have no upstream feeder at all** — the dead end is a single conveyor
with nothing behind it, and the walk terminates on its first step. **7.3% reach depth ≥ 5 and
1.5% reach depth ≥ 10.**

**The worst case in 220 games is 34 nodes at depth 31.** A per-turn budget is blown by the
worst case, so that is the number to budget against, and 34 nodes is not a budget event: it
times at **24.8 µs** for the single most expensive dead end observed.

**Split by verdict, because they cost differently:**

| | n | median nodes | p90 | p99 | MAX |
| --- | ---: | ---: | ---: | ---: | ---: |
| verdict **LIVE** (chain reaches a friendly harvester) | 14,661 (29.7%) | 2 | 7 | 17 | 32 |
| verdict **DECORATIVE** | 34,748 (70.3%) | 1 | 3 | 8 | 15 |

**A "no" is cheaper than a "yes"**, because a decorative end usually has nothing upstream of
it at all. The expensive walks are the ones that pay.

**Restricted to GROUND-class dead ends — the completable ones, 37,742 of 49,409 (76.4%)** —
depth median 0 / p90 3 / p99 12 / MAX 31, nodes median 1 / p90 4 / p99 14 / MAX 32, LIVE 30.1%.
**The completable subset is not the expensive subset.**

---

## 2. How many dead ends must be considered

| measure | n | median | p90 | p99 | MAX | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **dead ends per topology-change round** | 8,427 | **4** | 13 | 25 | **31** | 5.86 |
| …of which GROUND (completable) | 8,427 | 3 | 10 | 18 | 22 | 4.48 |

**Per game** (denominator: 220 games; concentration on the per-game total, per method rule 1):

| per-game aggregate | total | mean/game | median | top-1 | top-3 | top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| dead-end **evaluations** (= walks) | 49,409 | 224.6 | **107** | 6.9% | 16.6% | 23.8% |
| distinct dead-end **sites**, all classes | 6,221 | 28.3 | 22 | 2.5% | 6.4% | 10.0% |
| distinct **GROUND** sites | 6,013 | 27.3 | 21 | 2.5% | 6.5% | 10.1% |

**These are flat distributions — no game carries the result.** The worst single game is 6.9%
of the evaluations. That is unlike almost every other figure this session and it is worth
saying plainly: **this one is general, not tail-carried.**

**What the predicate actually walks, per change: median 4 dead ends × median 1 node = 8 nodes
at the median change round** (measured directly, not multiplied): nodes walked per change round
median **8**, p90 33, p99 64, **MAX 93**.

### Cross-instrument reconciliation with the costing census — and why my count is 2.4× larger

The costing doc censused **11.2 unterminated ends per game (median 9)** from a **structural pass
every 10 rounds**, deduplicated by (conveyor tile, output tile). I census **27.1 per game
(median 21)**. That is a 2.4× gap between two documents about the same bot, and it is a
**cadence** difference, not a disagreement:

| cadence | distinct GROUND ends never built on | mean/game | median | q1 | q3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| **every 10 rounds — the costing's cadence** | 2,489 | **11.31** | **9** | 6 | 14 |
| every topology-change round — the plank's cadence | 5,955 | 27.07 | 21 | 12 | 33 |

**11.31/game against the costing's 11.2/game, and median 9 against median 9 — two decoders
written in different sessions against different questions agree to 1.0%.** That is the strongest
validation in this document, and it also isolates exactly what the extra 16 ends per game are:
**transient ends of a line still being laid**, invisible to a 10-round structural sample and
squarely visible to a predicate that fires on every build. **A predicate triggered by builds
meets 2.4× the dead ends the costing census implied.** It is still 4 per change and still
cheap — but the count that should be quoted for this plank is 27, not 11.

---

## 3. Cycles — how often the naive version would have failed

**This decides nothing.** A visited set is three lines against an unbounded loop inside a 10 ms
budget with no exception and no signal; no rate could make omitting it correct, and that call
was settled before this measurement existed. **What follows is only how often the naive version
would actually have hung.**

| walk | cycle encountered | rate |
| --- | ---: | ---: |
| **STRICT** — feeders filtered by whether the target would actually accept the push | **0 / 49,409** | **0.0000%** |
| **NAIVE** — "anything pointing at me is upstream of me" | **1,096 / 49,409** | **2.2182%** |

**The 0.0000% is structural, not luck, and the proof is short enough to state.** A conveyor has
exactly one output tile, so the "points at" relation has out-degree 1 — the set of tiles that
reach a given tile is a tree unless the start tile is itself on a cycle. A dead end is by
definition a tile whose push is refused, so it cannot be on a *flowing* cycle. **With conveyors
only, an acceptance-checked upstream walk from a dead end cannot cycle.** The premise is
measurable and holds here: **our v102 builds 0 splitters in 220 games**, and a splitter (three
outputs) is the only carrier in the game that breaks the out-degree-1 argument. **If a future
bot builds splitters, the proof lapses and the 0.0000% lapses with it.**

**The 2.22% is head-to-head pairs**, and it is exactly the population the binding-tile cut
warned would not transfer. Two conveyors facing each other are 9.9% of the parent cut's
*binding tiles* and 7.12% of v102's blocked *mass*; as a **reachability rate from a dead end
under the naive walk** they are **2.22% of evaluations** — a third quantity, on a third
denominator, and the brief was right that the first two do not answer it.

**It is heavily tail-carried, unlike everything in §2:**

| | total | games > 0 | median/game | top-1 | top-3 | top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| naive-cyclic walks per game | 1,096 | **17 / 220** | 0 | **27.4%** | **54.6%** | **69.0%** |

**92% of games would never have hit it, and five games carry 69% of it.** That is the shape
that makes a missing guard survive testing and then kill a ladder run: **the naive predicate
would have looked fine in 203 of 220 games.**

**Measured directly rather than argued**: run without a visited set under a 5,000-node cap
(against a maximum legitimate walk of 34 nodes, a 147× margin), the naive walk blows the cap on
**1,096 / 49,409** — the same 1,096 — and the strict walk blows it on **0 / 49,409**. **The
unguarded naive predicate does not truncate or degrade; it does not terminate.**

---

## 4. How often the topology changes

**Unit: one `placeEntity` that is the FIRST appearance of an entity id (TRAP 3) of our conveyor
or splitter, or one `removeEntity` of same. 220 games, 58,165 rounds.**

| per-game aggregate | total | mean/game | median | top-1 | top-3 | top-5 | games > 0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **carrier build + remove events** | 9,752 | 44.3 | **37** | 2.5% | 6.6% | 10.0% | 219/220 |
| …builds | 8,714 | 39.6 | 33 | 2.2% | 5.8% | 9.1% | 219/220 |
| …removals | 1,038 | 4.7 | 2 | 5.6% | 14.3% | 20.3% | 138/220 |
| **rounds in which topology changed** | 8,427 | 38.3 | **32** | 2.6% | 6.5% | 10.0% | 219/220 |

**16.77 events per 100 rounds pooled; median 20.15 per 100 rounds per game.** Events and rounds
are nearly 1:1 (44.3 vs 38.3), so **a per-round recompute costs essentially the same as a
per-event one** — and since store writes are buffered and visible only next round, **per-round
is the correct granularity anyway**, not an approximation.

**By round band** (denominator: 9,752 events):

| band | events | share | per game |
| --- | ---: | ---: | ---: |
| **r0–100** | 6,355 | **65.2%** | 28.89 |
| r100–200 | 1,990 | 20.4% | 9.05 |
| r200–300 | 855 | 8.8% | 3.89 |
| r300–500 | 382 | 3.9% | 1.74 |
| r500+ | 170 | 1.7% | 0.77 |

**Two thirds of all topology change happens before round 100** — which is also where the costing
found the profitable ends first appear (median round 30). The walk's cadence is front-loaded
into exactly the phase where a builder has the least spare titanium and the most competing
actions.

---

## 5. Affordability, timed rather than argued

**The pure-Python graph work, timed on the real topologies at all 8,427 topology-change rounds
of the frozen population** (enumerate every dead end from the full team map, then walk every one
of them to a verdict):

| | median | p90 | p99 | MAX |
| --- | ---: | ---: | ---: | ---: |
| **µs per topology-change round** (all dead ends) | **15.6** | 59.8 | 113.4 | **436.6** |
| µs per dead end | 3.8 | 6.7 | 12.0 | 24.8 |

**Against 10,000 µs. The worst change round in 220 games is 4.4% of one turn.**

**Our current headroom, measured rather than assumed** — `BotOutput.execTimeUs` for our units
across the same 220 games, **483,337 unit-turns**:

```
  median   118 us      p90  1,186 us      p99  5,392 us
  p99.9  6,488 us      MAX  8,355 us      TLE flag fired 0 times
  1.648% of our unit-turns already exceed 5,000 us; 0.0002% exceed 8,000 us
```

**The worst turn we have ever taken is 8,355 µs, and the worst walk is 437 µs.** Stacking them
gives 8,792 µs — inside the budget, with a 12% margin, and that is the pessimal composition of
two maxima that need not co-occur. **At the p99 turn (5,392 µs) the walk is 2% of what is left.**

**Which term dominates: neither, and the honest answer is that this was never the risk.** The
one-walk-per-change design costs **~0.6 ms of CPU per game**; the rejected per-builder-per-turn
design costs the same *per turn* (15.6 µs median, 437 µs worst) and only accumulates across a
game in a way that no budget measures. **If the store design is chosen it should be chosen for
the reason in §6 — a single walker with a memo can see what a builder cannot — not for CPU.**

**What this timing does NOT include, and it is the part I cannot measure.** These figures are
pure Python over materialised dicts. A real implementation reads the map through the
`Controller`, and **per-Controller-call cost is engine-side and not recoverable from replays.**
What I can count is the calls: materialising the local index a vision-limited builder needs is
**1 `get_nearby_buildings()` + ~4 getters per building in vision** = **median 81, p90 141, p99
189, MAX 241 calls**. **At 1 µs/call that is noise; at 40 µs/call the MAX alone is the whole
budget.** **Settling it needs an engine probe (`get_cpu_time_elapsed()` around a call loop), and
that is a builder-arm instrument, not a replay one.**

---

## 6. The constraint is vision, and the failure mode is a destroyed unit

**`docs/game-model.md:449`, measured in this repo 2026-08-08:**

> `get_tile_env()`, `is_tile_passable()` and `get_tile_building_id()` all raise
> `GameError: Position out of vision range` for an in-bounds tile the unit cannot currently see —
> with the *identical* message as a genuinely off-map position, so the engine does not let you
> tell the two apart. `in_bounds()` is necessary but **not sufficient**.

**And per `CLAUDE.md`: an uncaught exception other than the timeout destroys that unit
permanently for the rest of the match.** A timeout costs one turn; this costs the builder.

**Measured: for each walk, the maximum d² from every walked node to the best legal tile a
builder could stand on while building at the dead end's output tile** (the four orthogonal
neighbours of the target, excluding walls and occupied tiles; the minimum over those candidates
of the maximum over walked nodes).

| | median | p90 | p99 | MAX |
| --- | ---: | ---: | ---: | ---: |
| max d², walk node → best builder standing tile | **2** | 17 | **97** | **325** |

| viewer | share of walks entirely inside its vision |
| --- | ---: |
| **builder bot, r² = 20** | **92.92%** |
| launcher, r² = 26 | 94.82% |
| sentinel, r² = 32 | 95.14% |
| core, r² = 36 (measured from the standing tile) | 95.71% |
| **the CORE itself, r² = 36 measured from a core footprint tile** | **53.67%** |

**7.08% of walks — 3,498 of 49,409 — cannot be executed by the builder that would act on them.**

| | total | games > 0 | median/game | top-1 | top-3 | top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| out-of-vision walks per game | 3,498 | **123 / 220** | 1 | 12.8% | 23.7% | 32.7% |

**It fires in 56% of games** — not a tail phenomenon, though the volume is tail-carried.
Restricted to GROUND-class (completable) dead ends the fit is **93.94%**, so the exposure is
**6.06%** there.

**Three consequences, in order of how much they change the build:**

1. **The walk must be wrapped, or written to stop at the vision boundary.** A bare recursive
   walk on `get_tile_building_id()` will destroy a builder in roughly one game in two. The
   cheapest correct form is to guard every tile read with `is_in_vision(pos)` and treat "cannot
   see" as **"unknown", not as "no feeder"** — because treating it as no-feeder converts 7% of
   live ends into decorative ones, which is a silent wrong answer rather than a crash.
2. **The core cannot be the single walker.** Only **53.67%** of walks fit inside r²=36 from a
   core tile, and the core is the one unit that never moves and could safely hold a whole-map
   memo. **The natural home for the store-writing walk cannot see half of what it must walk.**
3. **The store design assumes a memo the game may not provide.** The 16-slot store cannot hold a
   conveyor map, and *"anything that reasons about ground a unit saw earlier must read a memo the
   bot maintains itself"* (same measured note). Per `official-docs.md:1725`, **the engine creates
   one `Player` instance per unit**, so instance state is per-unit and cannot be that memo.
   Whether *module-level* state is shared across a team's units in one interpreter is **not
   documented, not measured, and not used anywhere in `bots/_v100hf/main.py`.** **If module
   globals are not shared, no unit in the game can hold the map this design needs, and the walk
   must be local-and-guarded rather than global-and-published.** **This is a one-probe question
   and it gates the design more than any number in this document.**

---

## 7. The discriminator is 5.5× wider than the subset +411 was priced on

**This is not a re-costing and I did not re-cost. It is a selectivity measurement on the
population that reconciles to the costing's own census (§2: 11.31 vs 11.2 ends/game, median 9
vs 9), which is the only fair place to compare.**

```
  ends (GROUND, never built on, every-10-round cadence)      2,489    = 11.31/game
  ...passing the stated discriminator (chain reaches a
     friendly harvester at any sample)                       1,158    =  46.5%   5.26/game
  ...the costing's PROFITABLE subset (blocked mass exceeds
     its own repair price)                                     200/2,348 = 8.5%   0.95/game
```

**The predicate the +411 rests on passes 46.5% of unterminated ends. The subset the +411 was
computed over is 8.5%.** They are not the same set and the ratio is **5.5×**.

**Why the gap is real and not a definitional artefact.** "Reaches a harvester" is a
*topological* test — is anything feeding this line. "Profitable" is an *economic* test — does
the mass behind this end exceed the titanium to finish it. **Every profitable end is live; most
live ends are not profitable**, because a fed line can still be carrying almost nothing (the
costing's own finding: 86% of ends carry zero blocked titanium, and one end per game carries
91% of that game's unterminated loss).

**What this does to the plank's price, stated as an inference and labelled as one.** The costing
priced completing *all* 2,348 ends at **681 Ti/game** and the profitable 200 at **38 Ti/game**.
If the builder completes the 46.5% the discriminator admits, the spend lands between those
anchors and much nearer the top — crudely 0.465 × 681 ≈ **~317 Ti/game** — while recovery is
bounded above by the **458 Ti** the costing says *all* ends recover. **That is a net in the low
hundreds at best, not +411, and the extra 4.3 ends per game are by construction the low-mass
ones: they cost like the profitable ends and recover far less.**

**I am not putting a number on the corrected net.** Pricing a completion needs the costing's
BFS-to-core at the live scale, which is its instrument, not mine. **What I can say with a
measurement behind it is that "walk upstream, if it reaches a harvester, finish it" is not the
selector that produced +411, and the plank as specified will spend several times the 38 Ti/game
it was costed at.** **If the +411 is load-bearing for the queue order, the discriminator needs a
mass term — and the costing already found the one that would do it: one end per game carries
91% of the loss, so "finish the single largest live end" is a far tighter rule than "finish
every live end", and it fits in one store slot.**

---

## 8. Instrument validation — the traversal was corrupted and the alarm required

**Method rule 4, applied to a walk: it must terminate on a synthetic cycle and REPORT it,
rather than hang or silently truncate.** A hand-built synthetic suite (`test_walk.py`, 22
assertions, all passing) with the load-bearing cases:

| case | required behaviour | result |
| --- | --- | --- |
| straight 5-conveyor line fed by a harvester | depth 4, nodes 5, verdict LIVE | PASS |
| same line, harvester removed | verdict DECORATIVE, nodes unchanged | PASS |
| **head-to-head pair** | strict: partner is *not* a feeder, no cycle, terminates | PASS |
| **head-to-head pair, naive walk** | **cycle REPORTED**; **unguarded run blows the cap** | PASS |
| head-to-head pair, strict unguarded | terminates | PASS |
| **4-cycle with a splitter feeding a tail** | **cycle REPORTED; unguarded blows the cap** | PASS |
| 4-cycle of pure conveyors, tail pointing in | walk correctly finds nothing (cycle points away) | PASS |
| wide fan-in, 3 feeders on one tile | depth 1, nodes 4 | PASS |

**The cap-blowing tests are the ones that matter**: the guard is not decorative, and the
unguarded walk is demonstrably non-terminating rather than merely slow.

**Three corruption arms over the full 220-game population, each firing on a disjoint column:**

| | **clean** | `cycle` (inject a 2-cycle and a 4-cycle at r50) | `scramble` (rotate every one of our conveyor facings 90°) | `nofeed` (delete every harvester from the topology) |
| --- | ---: | ---: | ---: | ---: |
| dead-end evaluations | 49,409 | 56,511 | **179,280** | 49,409 |
| GROUND share | 76.39% | 66.46% | **69.57%** | 76.39% |
| chain depth p90 / MAX | 4 / 31 | 3 / 23 | **1 / 13** | 4 / 31 |
| **verdict LIVE** | **29.7%** | 30.1% | 20.6% | **0.0%** |
| **NAIVE cycle rate** | **2.22%** | **15.57%** | **0.19%** | 2.22% |
| STRICT cycle rate | 0.0000% | **0.0000%** | 0.0000% | 0.0000% |
| unguarded naive blowups | 1,096 | 8,800 | 338 | 1,096 |

**`nofeed` is the load-bearing test for the verdict column** — it drives LIVE from 29.7% to
**exactly 0.0%** while leaving every other column **bit-identical**, which proves the verdict
depends on the harvester set and on nothing else. **`scramble` is the load-bearing test for the
topology read** — it leaves the harvester set untouched and inflates dead ends 3.6× while
collapsing chain depth, which is what shattering the facings must do. **`cycle` is the
load-bearing test for the cycle detector** — 2.22% → 15.57%, 7× — and note it drives the naive
rate *up* while `scramble` drives it *down* to 0.19%, because uniform rotation destroys
head-to-head pairs (both members rotate the same way). **No single corruption could have
produced another's result.**

**And the negative control that could have embarrassed me: `STRICT cycle rate` is 0.0000% in
every arm including the one that injects real cycles.** That is not a dead column — it is the
§3 proof holding under adversarial input, and the *naive* column in the same rows shows the
detector fires. A guard that reads 0 everywhere is exactly the shape of TRAP 8, so it is stated
next to the column that discriminates rather than alone.

**Splitter check, because the acyclicity proof depends on it**: our v102 builds **0 splitters in
220 games**. The proof's premise is measured, not assumed.

---

## 9. What I could not measure

1. **Per-Controller-call cost.** Everything in §5 is pure-Python timing on materialised dicts.
   The call count is bounded (median 81, MAX 241 per local index) but the per-call price is
   engine-side. **`get_cpu_time_elapsed()` around a call loop in an arena probe is the
   instrument; I did not run one, and a replay cannot answer it.**
2. **Whether module-level state is shared across a team's units.** §6(3). The docs say one
   `Player` instance per unit and say nothing about the module. **This gates whether the
   store-and-memo design is buildable at all**, and it is one probe.
3. **The corrected net titanium for the plank.** §7 measures selectivity (46.5% vs 8.5%) and
   bounds the spend crudely between the costing's own 38 and 681 Ti/game anchors. **Pricing the
   completions needs the costing's BFS-at-live-scale, which is its instrument.**
4. **Second-order dead ends.** Completing an end creates a new terminus one tile further on; the
   walk from *that* tile is not modelled, and a repair loop would re-evaluate it next change.
   Every figure here is the cost of one pass over the topology as it stands.
5. **The `sites` dedup keeps the largest observation of each site, not a union.** The per-site
   depth/nodes columns in §1 and the 46.5% in §7 are therefore "at that site's largest
   observation" / "ever live at any sample", not exact lifetime maxima. The per-*evaluation*
   columns are exact and are what the affordability verdict rests on.
6. **v102 is not a long economy.** 13-ish of 220 games reach round 1000; median game 187 rounds;
   65.2% of topology change is before round 100. **Nothing here describes what the walk costs in
   a 1000-round game**, where the network is larger and the chains are presumably longer. The
   parent cut's round-1000 population would answer it and is a different decode.
7. **Enemy carriers are excluded from the graph entirely.** A stack pushed onto an enemy network
   is a leak, not a chain (`replay_census.py`'s standing convention). `CONVEYOR_ENEMY` appears
   only as a *dead-end class* (3.20% of evaluations), never as a walked node.
8. **The vision figures assume the walking unit is the builder that would act.** If the walk is
   done by some other unit standing elsewhere, §6's 92.92% does not apply and the geometry must
   be re-measured for that unit. **The core case I did measure, and it is worse: 53.67%.**
9. **Diagonal conveyor facings.** The walk computes the output tile as `pos + delta(direction)`
   for all 8 directions, so a diagonal facing is handled — but the game's "accepts from 3 sides,
   outputs to the 4th" wording implies cardinals, and I did not census whether any of our
   conveyors ever carry a diagonal facing. The acceptance model is the costing's, probed there
   against 521,624 real moves with zero exceptions.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session: `walk.py` (topology integration, dead-end
enumeration, strict and naive walks, cycle detection, three corruption arms, ~380 lines against
`tools/replay_census.fields`), `test_walk.py` (the synthetic-cycle suite), `bench.py` (timing +
Controller-call counting), `recon.py` / `sel.py` (cadence reconciliation and selectivity).
Frozen population `pop_v102.tsv`. Load-bearing decisions:

- **Seat and version from `.meta.json`, never `winnerSide`** (TRAP 7), and **verified
  behaviourally**: our-side `builderAttack` 0 vs 12,815.
- **A build is the FIRST `placeEntity` carrying an id** (TRAP 3), and the guard was checked
  rather than assumed: **2,736 re-emits across the 220 files, and all 2,736 are gunners — 0
  conveyors, 0 splitters, 0 of any other kind.** Counting every `placeEntity` would therefore
  have inflated no figure in this document, but the guard is kept because that is a property of
  v102's behaviour, not of the format.
- **`econ.tsv` was not used** (TRAPs 5, 8). Everything is decoded from the replay binaries.
- **The acceptance model is inherited from `repair-class-costing-2026-08-10.md`'s appendix** —
  a core footprint tile always accepts; a conveyor accepts unless the pusher stands on its
  output tile; a splitter accepts only from its back — where it was probed against 521,624 real
  resource moves with zero exceptions. **Reusing it rather than re-deriving it is deliberate:
  §3's whole result turns on it, and a second hand-rolled acceptance model would have been the
  more likely error.**
- **The unguarded-walk cap is 5,000 nodes against a maximum legitimate walk of 34** — a 147×
  margin, so a cap blow is non-termination and not a long walk.
