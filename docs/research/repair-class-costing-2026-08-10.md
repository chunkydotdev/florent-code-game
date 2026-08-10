# Costing the four titanium-delivery repair classes

**Research arm, session 28. Decoded 2026-08-10. Direct successor to
`binding-tile-cut-2026-08-10.md`, which established the four classes and ranked them by
share-of-blocked-tiles. That ranking was never a costing, and its regrouped table
over-counts (its four prescription rows claim 74.5pp against parents holding 53.50pp,
×1.393). The §1 CLASS table it rests on is exact; the ORDER was not established.**

**Population: 210 v102 LADDER games, `related == none`, our side. Seat and version read
from `replay_archive/*.meta.json` (`teamAId`/`teamAVersion`), never from `winnerSide` —
TRAP 7 does not apply. Frozen file list: `pop_v102.tsv`, sha256 `343464a500f989e9…`
(the archive grew 205→210 mid-session; an unfrozen denominator would have moved under
the numbers). Fixture: LADDER. No downloads. No bot, arena or prereg touched.**

---

## 0. The answer in five lines

**Costed on net titanium per game, the order does NOT change.** Unterminated lines,
destroyed segments, facing incoherence, self-blocking — in that order, 411 / 182 / 130 /
102 net Ti per game. My pre-stated expectation was that it would change; it did not.

**But the order flips completely on return-on-spend** (∞ / 95× / 38× / 12×), and
**the naive version of class 1 — "complete every unterminated line" — is net NEGATIVE at
−223 Ti/game.** It only wins once the builder completes the *corking* ends and leaves the
rest alone.

**86% of our unterminated line-ends carry zero blocked titanium.** They are decorative.
**One end per game carries 91% of that game's unterminated loss** (median), costs a median
**22 Ti** to finish, and returns a median **174 Ti**.

---

## 1. THE TABLE

**Subject: our side. Population: 210 v102 ladder games. Denominator: all 210 games unless
a column says otherwise. Fixture: LADDER. Unit: titanium per game.**

| class | defect Ti/game | …of which priced | fix Ti/game | net Ti/game | return | top-1 / top-3 / top-5 | games affected |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| **1 unterminated lines** *(corking ends only)* | 464 | **448** | **38** | **+411** | **11.9×** | 9.4% / 24.8% / 38.5% | 123/210 (59%) |
| 1′ *same, completing **every** end* | 464 | 458 | 681 | **−223** | 0.7× | — | 209/210 |
| **2 destroyed segments** | 254 | **187** | **5** | **+182** | **38×** | 18.0% / 40.9% / 51.7% | 68/210 (32%) |
| 2′ *same, rebuilding **every** broken tile* | 254 | 254 | 45 | +209 | 5.7× | — | 135/210 |
| **3 facing incoherence** | 132 | **132** | **1.4** | **+130** | **95×** | 31.0% / 52.2% / 62.2% | 30/210 (14%) |
| **4 self-blocking** (own turret on own route) | 102 | **102** | **0** | **+102** | **∞** | 22.2% / 47.7% / 64.2% | 35/210 (17%) |
| — harvester with no output ever built | 148 | *(fix folded into class 1)* | — | — | — | 11.6% / 25.6% / 33.7% | 209/210 |
| — enemy building / enemy net blocks the line | 154 | *not ours to fix* | — | — | — | 17.0% / 31.1% / 44.2% | 69/210 |
| — genuine saturation | 15 | *nothing to fix* | — | — | — | 32.4% / 71.5% / 84.4% | 60/210 |

Fix Ti is the **profitable-subset** cost: only sites whose blocked mass exceeds their own
repair price. **"…of which priced" is the defect mass that has a costable repair site** —
net and return are computed on that column, not on the defect column, so the two are never
differenced across different populations. Concentration tails are on **net Ti/game of the
profitable subset**. `top-1` = share carried by the single worst game.

**Read the tails before the means.** Classes 3 and 4 are four-to-five-game phenomena
(top-3 ≈ 50%, affected 14–17% of games). Class 1 is the only one that is *general*:
59% of games, top-1 9.4%. That difference matters more than the 411-vs-102 gap.

**Per affected game** (defect only): unterminated 594 Ti, destroyed 575 Ti, facing 892 Ti,
self-block 593 Ti. All four are roughly the same size *when they fire*; they differ in how
often they fire.

---

## 2. Where these numbers come from, and the budget they close

**Unit of analysis: one blocked harvester-round** — a round in which one of our harvesters
was due to emit (r ≥ last emission + 4, or ≥ its build round before its first) and did not.
Each is walked downstream along conveyor facings to the most downstream tile that also did
not move; that tile is the **binding tile** and is classified by what its own output tile
is. Weight 1.0 per blocked harvester-round, split evenly across distinct binding tiles.
Conversion: 4 blocked rounds = one missed 10 Ti emission slot → **2.5 Ti per blocked
harvester-round** (the parent's clock, inherited).

**The emission budget closes to 4.7%, and the closing term is an independently guarded
number:**

```
  harvester-alive-rounds                245,805
  potential emission @ 2.5 Ti/round     614,512 Ti
  blocked   (this instrument)           266,532 Ti   43.4%
  delivered to our core (ti_ok guard)   319,190 Ti   51.9%
  residual (in flight / stranded)        28,790 Ti    4.7%
```

**We lose 43% of everything our harvesters were entitled to emit, and it is not lost at the
core face — 0.00% of it is.** The `delivered` line is not a modelled quantity: it is
`ResourceMoves` landing on our core footprint × 10, which **equals `Player.titaniumCollected`
in 210 of 210 games**.

### Binding-tile distribution, v102 our side (106,613 blocked harvester-rounds)

| class | share | Ti/game |
| --- | ---: | ---: |
| `DEAD_END_NEVER_BUILT` — line ends on ground nothing was ever built on | **36.57%** | 464 |
| `DEAD_END_DESTROYED` — a carrier stood there and was destroyed | **14.79%** | 188 |
| `NO_OUTPUT_NEVER` — harvester never given a receiving neighbour | 11.64% | 148 |
| `ENEMY_BUILDING` | 8.14% | 103 |
| `SELF_BLOCK` — our own turret/barrier is the terminus | **8.01%** | 102 |
| `FACING_HEAD_TO_HEAD` — two of our conveyors point at each other | **7.12%** | 90 |
| `NO_OUTPUT_DESTROYED` | 5.26% | 67 |
| `ENEMY_NET` | 4.03% | 51 |
| `FACING_HARVESTER` — line points at a harvester (never accepts) | **3.26%** | 41 |
| `DOWNSTREAM_MOVED` — genuine saturation | 1.18% | 15 |
| `CORE_ENTRY` | 0.003% | 0 |
| `FACING_WALL` / `FACING_OFFMAP` / `CYCLE` | **0.00%** | 0 |

**This resolves the parent's open item #5.** `NO_OUTPUT_BUILT` (its 15.9%) conflated siting
and repair; split here it is **11.64% never-built vs 5.26% destroyed** — 69% siting, 31%
repair. Folded into the classes accordingly.

**v102 is not the round-1000 economy the parent measured.** Median game is **187 rounds**;
13 of 210 reach round 1000; 197 end `core_destroyed`. Total loss is 1,269 Ti/game here
against the parent's 7,767 Ti/game on round-1000 sides — the *rate* is comparable, the
game is six times shorter. **Do not compare the absolute Ti figures across the two
documents; compare the shares.**

---

## 3. Class 1 — UNTERMINATED LINES. The fix is only worth it if you aim it.

**Census (structural pass every 10 rounds, deduplicated by (conveyor tile, output tile)
over the whole game):**

| measure | value |
| --- | --- |
| distinct unterminated line-ends per game | **11.2** (median 9) |
| segments from the end to a core-adjacent tile (BFS through passable, non-building tiles) | median **5**, q1 3, q3 9, max 38 |
| ends with no route to the core at all | 18 / 2,348 = **0.8%** |
| cost to complete **all** of them | **681 Ti/game**, recovering 458 → **net −223** |
| **ends carrying ZERO blocked titanium** | **2,013 / 2,348 = 86%** |

**That is the whole finding for this class.** Completing every unterminated end costs more
than it recovers (spend 681, recover 458, **net −223 Ti/game**). Completing only the ends
that actually cork a fed harvester costs **38 Ti/game** and recovers **448** — the same
recovery for one eighteenth of the spend.

**The 200 profitable ends:**

| measure | value |
| --- | --- |
| ends | 200, in **123 of 210 games (59%)**; median **1** per affected game, max 5 |
| segments each | median **3** (q1 2, q3 6, max 22) |
| titanium to complete each | median **22 Ti** at the live scale of that round |
| titanium recovered each | median **174 Ti** |
| first seen at round | median **30** |
| share of a game's unterminated mass on its single worst end | median **91.3%** (n=160) |

**One tile. Three conveyors. Twenty-two titanium. Round 30.** That is the shape of the
largest single defect class in our economy.

**The discriminator a builder can actually compute** is the same one the measurement uses:
walk upstream from the dead end; if the chain reaches a friendly harvester, the end is live.
That predicate is cheap and it is the difference between +411 and −223.

---

## 4. Class 2 — DESTROYED SEGMENTS. We never repair, and we never self-destruct.

| measure | value |
| --- | --- |
| our carriers destroyed per game | **4.8** (median 2; 135/210 games) |
| …**by enemy damage** | **1,017 / 1,017 = 100%** |
| …**by our own `destroy()`** | **0** |
| **how long a break stays broken** | median **103 rounds**, q1 40, q3 238, mean 193 |
| **ever repaired** (a friendly carrier rebuilt on that tile) | **16.7%** |
| titanium to rebuild one, at the live scale | median 8 Ti (final-scale median 3.00 → 9 Ti) |
| fix cost, rebuilding **every** broken tile | 45 Ti/game (recovers 254 → net +209) |
| fix cost, **profitable subset** (122 of 328 dead-end sites) | **4.9 Ti/game** (recovers 187 → net +182) |

**A break lasts more than half of a median v102 game** (103 rounds against a median game of
187). Five sixths are never repaired at all. This is the class where the defect is not a
design error but an *absence*: there is no repair loop.

**The 0/1,017 self-destroy figure is not a constant column — the control fires.** The same
damage flag on the *opponents'* carriers reads **122 removals with no damage ever recorded**
(and 75 undamaged gunners, 19 launchers, 11 barriers). **Other teams call `destroy()` on
their own logistics; we never do.** A flag that reads 0 on our side and 122 on theirs is
discriminating, not dead.

---

## 5. Class 3 — FACING INCOHERENCE. Verify the rule before costing the fix.

**The brief's suspicion is correct and I can quote the line.**

> `official-docs.md:275` — *"Only the Gunner can rotate after placement:"*
> `official-docs.md:282` — *"Rotation costs exactly 10 Ti and triggers a 1-round action
> cooldown. Sentinels and Launchers have no rotate() — their orientation (or lack of one)
> is fixed for their lifetime."*

**There is no `rotate()` for a conveyor anywhere in the API surface.** A conveyor's
direction is set at build time (`official-docs.md:1265`, *"Direction | Set at build time"*)
and the only way to change it is destroy-and-rebuild. So the fix is priced as:

> `official-docs.md:1225` — destroy *"costs no titanium and does not use the action cooldown
> — you can destroy any number of allied buildings this way in a single round"*
> `official-docs.md:1304` — *"This returns any resources currently in transit on that tile to
> your team's balance."*

**Fix cost of one facing defect = one scaled conveyor, `floor(scale × 3)`, and nothing
else.** Destroy is free, refunds any held stack (+10 Ti), and removes that conveyor's +1%
from the scale — which the rebuild puts straight back, so the scale is unchanged across the
operation. **The original ranking never priced this and it turns out to be the cheapest fix
in the document: 1.4 Ti/game for 130 Ti/game recovered.**

| kind | sites | defect Ti/game | fix Ti/game |
| --- | ---: | ---: | ---: |
| `HEAD_TO_HEAD` — two of our conveyors face each other | 42 | **90.3** | 1.6 |
| `HARVESTER` — a conveyor faces a harvester | 148 | 41.4 | 5.7 |
| `WALL` / `OFFMAP` | **0** | 0 | 0 |

**We never point a conveyor into a wall or off the map — 0 of 106,613 blocked rounds.** The
mass is head-to-head pairs, which are 22% of the sites and 69% of the loss. **The 42
head-to-head pairs cost 90 Ti/game and cost 1.6 Ti/game to fix.** That is a 56× return on
the single narrowest intervention in this document, and it is concentrated: 14% of games,
top-1 game 31%.

---

## 6. Class 4 — SELF-BLOCKING, and a correction to the plank that was chosen

| measure | value |
| --- | --- |
| standing (our conveyor → our turret/barrier) pairs | 99, in 71/210 games |
| forward builds — turret/barrier planted onto an already-faced tile | **87 (0.414/game)**, 42/210 games |
| defect cost | **102 Ti/game**, 593 Ti per affected game (35 games) |
| fix cost | **0 Ti** — the turret costs the same on another tile |
| by turret kind (defect Ti/game) | **launcher 49.6**, sentinel 40.2, gunner 10.2, barrier 1.7 |

**The 0.414 forward builds/game reproduces the prior document's 0.424/game on 125 games,
now on 210 — the two instruments agree to 2.4%.**

### The correction, and it matters for LOKI-10

**The refusal reaches 35.0% of this class's titanium, not 70%.**

| | pairs | Ti/game | share of class mass |
| --- | ---: | ---: | ---: |
| turret built onto an already-faced tile — **the refusal catches this** | 64 | **35.6** | **35.0%** |
| conveyor built later, aimed at an existing friendly turret — **it cannot** | 35 | **66.1** | **65.0%** |

The prior read measured the split **by event count** (70% forward in v102) and it was right
about events. **By titanium the split inverts: the 35 reverse pairs carry nearly twice the
mass of the 64 forward ones.** A perfectly firing LOKI-10 recovers ~36 Ti/game, not ~102.
That is still free — fix cost 0 — but it is the smallest of the four fixes by a factor of
eleven, and **the leg should not be read as a test of "our own turrets cork our own lines".**

**The refusal's mirror image — "do not build a conveyor whose facing lands on a friendly
turret" — is the same predicate, also free, and carries 65% of the mass.** It is not in the
plank.

---

## 7. The reordering — or its absence

**Pre-stated expectation (coordinator's, recorded before the decode): the order changes.**

| ranking basis | order |
| --- | --- |
| binding-tile-cut §2 (share of blocked mass) | unterminated · destroyed · **facing** · self-block |
| **net Ti/game, profitable subset (this doc)** | **unterminated (411) · destroyed (182) · facing (130) · self-block (102)** |
| net Ti/game, fix-everything | **destroyed (209) · facing (124) · self-block (102) · unterminated (−223)** |
| **return on titanium spent** | **self-block (∞) · facing (95×) · destroyed (38×) · unterminated (12×)** |
| generality (share of games where the fix does anything) | unterminated (59%) · destroyed (32%) · self-block (17%) · facing (14%) |

**On the ranking the prescription actually meant — net titanium, fixing what is worth
fixing — the order is unchanged.** The faulty arithmetic happened not to matter. That is
the contrary result the brief asked to be made visible, and it is the one that came back.

**On every other basis the order moves, and one of them reverses it outright.** The two
that should change what gets built:

1. **Class 1 is negative if executed naively.** "Never leave a line unterminated" as an
   unconditional invariant loses 223 Ti/game. The invariant has to be *"never leave a line
   that a harvester feeds unterminated"*.
2. **Classes 3 and 4 are nearly free.** Together they are 234 Ti/game for 1.4 Ti/game of
   titanium. They rank last on size and first on price, and nothing about them competes for
   builder actions with class 1.

**What I would build first: class 1, aimed.** Not because of the ordering — the ordering is
close and the tails are wide — but because it is the only class that fires in a majority of
games (59% vs 14–32%) and the least tail-carried (top-1 9.4% vs 18–31%). A fix that lands
in three games out of five is worth more than an equal-sized fix that lands in one out of
seven, and no per-game mean shows that.

---

## 8. Instrument validation — three corruptions, each of which fires differently

**Same 210 games in every column.**

| | **clean** | `scramble` (rotate every conveyor facing 90°) | `silence` (drop every resource move after r200) | `scale` (conveyor scale weight 1%→2%) |
| --- | ---: | ---: | ---: | ---: |
| blocked harvester-rounds | 106,613 | 106,613 | **162,566** | 106,613 |
| **scale-ledger PASS** | **3,696** | 3,696 | 3,696 | **1,754** |
| **scale-ledger FAIL** | **0** | 0 | **699** | **1,942** |
| `DEAD_END_NEVER_BUILT` | 36.57% | **48.15%** | 26.12% | 36.57% |
| `DEAD_END_DESTROYED` | 14.79% | **0.16%** | 9.95% | 14.79% |
| `SELF_BLOCK` | 8.01% | **0.76%** | 5.71% | 8.01% |
| `FACING_HEAD_TO_HEAD` | 7.12% | **0.49%** | 4.70% | 7.12% |
| `FACING_WALL` | 0.00% | **10.29%** | 0.00% | 0.00% |
| `FACING_OFFMAP` | 0.00% | **2.02%** | 0.00% | 0.00% |
| `CORE_ENTRY` | 0.003% | 0.00% | **30.25%** | 0.003% |

**`scramble` is the load-bearing test for the classification** and **`scale` is the
load-bearing test for the pricing** — and they fire on disjoint columns, which is the point.
Rotating facings leaves the build ledger untouched (3,696/3,696 still pass) while inverting
every class share; corrupting one scale weight leaves the classification bit-identical while
halving the ledger. **Neither could have produced the other's result.** `silence` proves the
walk is reading the move stream: with nothing moving, 30% of blocked rounds resolve at the
core face, against 1 in 30,000 clean.

### The scale model: 3,696 / 3,696 exact, and it settles the passive-income phase

**This is the first decoder in the repo to price a build at the live scale.** The
forward-census stated *"I did not model the live scale — that needs the engine's cost
category rule, which I could not establish from the replay"*. The rule is in the docs
(`official-docs.md:1421`, `effective_cost = base_cost × scale_factor`; `:1424`, the additive
per-category weights) and the ledger is in the replay, so the scale is integrable from our
own `placeEntity`/`removeEntity` stream.

**Test: rounds where our team made exactly one build and nothing else that touches
titanium** (no attack, no heal, no rotation re-emit, no `convert_ammo`, no delivery, no
removal). On those rounds `Player.titanium` must move by exactly
`−floor(scale_before × base_cost) + passive`.

```
  3,696 isolated build rounds        3,696 exact        0 mismatches
```

**Byproduct, stated because it was an assumption I got wrong first:** passive income lands
on rounds **r ≡ 3 (mod 4)**, not r ≡ 0. Assuming r ≡ 0 gave 71% agreement and the residual
was exactly 10 Ti every time — which is how the phase was found. **The scale model was
never wrong; my income phase was.**

### The acceptance model, probed rather than assumed

Every `ResourceMove` in all 210 games, by what stands on the destination tile:

```
  conveyor  448,208        core  73,416
  splitter, harvester, gunner, sentinel, launcher, barrier, empty tile:   0
```

**521,624 of 521,624 resource moves land on a conveyor or a core.** Turrets, barriers and
harvesters never accept a stack — so a conveyor facing one *is* a terminus, which is what
`SELF_BLOCK` and `FACING_HARVESTER` rest on. **We build no splitters at all in v102**, so
nothing here says anything about them.

### Site-level attribution closes

The structural census (which produces the fix costs) and the round-by-round walk (which
produces the defect costs) are separate passes. They must agree on which tile carries the
mass:

```
  DEAD_END_NEVER_BUILT   walk 97,459 Ti   sites 96,104 Ti    98.6% captured
  DEAD_END_DESTROYED     walk 39,413 Ti   sites 39,303 Ti    99.7%
  SELF_BLOCK             walk 21,350 Ti   sites 21,340 Ti   100.0%
  FACING (all kinds)     walk 27,664 Ti   sites 27,664 Ti   100.0%
```

The 1.4% class-1 shortfall is defects that existed only between two structural samples.

---

## 9. What I could not cost

1. **The brief's calibration point measures a different quantity from mine, and it should
   not be used as one.** `forward-census-treadmill-2026-08-10.md`'s **421 Ti per affected
   game in 11.9% of games** is the **build spend on excess forward turrets** (builds beyond
   the 3rd by one builder, priced at base cost). It is not the delivery loss from turrets
   corking conveyor routes. My class-4 figure — **593 Ti per affected game in 17% of
   games** — is the *delivery* loss and is a different measurement of a different
   population. **They are the same order of magnitude by coincidence, and I could not use
   one to calibrate the other.** The brief's instruction to reproduce something compatible
   with 421 Ti was not executable as written.
2. **Second-order recovery is not modelled.** Fixing one class may expose another binding
   tile downstream. Saturation is 1.18% here so the headroom exists, but the recovered
   figures are "the mass behind this tile", not "the mass that would arrive".
3. **Stranded stacks are not recovered in any figure.** The 4.7% residual (28,790 Ti) sits
   in the network at game end. Completing a line delivers some of it; I did not attribute it.
4. **Fix costs are one-shot.** A repaired conveyor can be destroyed again — 16.7% of breaks
   were ever rebuilt, and I did not model the repeat cost of a repair loop under fire, which
   for class 2 is the whole question.
5. **`NO_OUTPUT_DESTROYED` (67 Ti/game) has no fix cost.** Its binding tile is the
   harvester, not a conveyor, so the BFS-to-core that prices class 1 does not apply. It is
   counted in the class-2 defect column and absent from the class-2 fix column, which makes
   class 2's return an over-estimate by up to 26%.
6. **The `dmg` flag cannot distinguish "our `destroy()`" from "enemy killed it in one shot
   whose `updateHp` was emitted after the `removeEntity`"** — the known FireTurret ordering
   trap, applied to HP. The 122-undamaged control on the opponents' side shows the flag has
   teeth, but a systematic ordering bias would suppress *our* self-destroys too. I read
   0/1,017 as "we do not destroy our own carriers"; the weaker reading, "we do so far less
   often than opponents", is also supported and is all that is needed.
7. **13 of 210 games reach round 1000.** Nothing here describes a long economy, and the
   parent's round-1000 figures are not comparable in absolute Ti.
8. **Structural sampling is every 10 rounds.** Defects shorter-lived than that are missed
   from the fix-cost census (1.4% of class-1 mass, by §8's attribution check). The bias is
   toward persistent defects, which is the correct bias for costing a repair.
9. **The BFS prices a straight completion through currently-passable tiles.** It does not
   model an enemy contesting the route, does not re-price if the route is blocked later, and
   allows reuse of existing friendly carriers at zero cost. 0.8% of ends had no route at all
   and are excluded from both columns.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session: `repair_cost.py` (decode + walk +
scale ledger, ~470 lines against `tools/replay_census.fields`), `run_cost.py` (population
driver + corruption arms), `analyse.py` / `analyse2.py` (aggregation, marginal payoff).
Frozen population list `pop_v102.tsv`. Load-bearing decisions:

- **Seat and version from `.meta.json`, never `winnerSide`.** 210 v102 ladder games,
  `related == none`; the archive grew from 205 during the session and the list was frozen
  and hashed before any headline was computed.
- **Live scale is integrable from the replay** and was validated to 3,696/3,696 before any
  fix cost was quoted. Passive income lands on r ≡ 3 (mod 4).
- **`receives()` is the whole model**: a core footprint tile always accepts; a conveyor
  accepts unless the pusher stands on its output tile; a splitter accepts only from its
  back. Probed against 521,624 real moves with zero exceptions.
- **A conveyor cannot be rotated** (`official-docs.md:275,282`) — facing fixes are priced as
  destroy-and-rebuild, and `destroy()` is free with a stack refund
  (`official-docs.md:1225,1304`).
- **Rotation re-emits are guarded** (TRAP 3): a build is the FIRST `placeEntity` carrying an
  id; re-emits update facing and are counted as rotations for the ledger.
- **`econ.tsv:deliveries` (TRAP 8) was not used.** Deliveries are counted from
  `DistributeResources` (update field 4) directly, per `tools/core_entry.py`, and guarded
  against `Player.titaniumCollected` — 210/210.
