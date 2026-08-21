# tape602 AUTOPSY — what blocks the full seal, and why the belt still dies

**Read-only decode agent, builder s54, 2026-08-21.** Source:
`scratchpad/s54_fidtape/replays_tape602/*.replay26` — 30 games, `bots/_v602skalman`
vs the NOISE_OFF `_v542wave` copy, 15 pool maps × both seats (`*_A` = we are side 0,
`*_B` = side 1). No repo edits, no matches, no commits.

Decoders: `cage602.py` (this pass, built on the validated attribution law of
`scratchpad/s54_autopsy/tape30_deaths.py`), driver `run602.py`, aggregators
`q1.py` / `q1b.py` / `q2.py` / `gap.py` — all in this scratchpad directory.

⛔ **FIXTURE CAVEAT, carried into every number below.** ONE authored opponent, local
screen, 30 games. Per the standing rule this **prioritises**; it does not establish
field prevalence. Local balanced batteries read DEFF ≈ 0.98, so naive intervals are
approximately honest here — but 8-game cells are 8-game cells.

---

## 0. INSTRUMENT VALIDATION (every counter driven to the other verdict)

| guard | control | result |
|---|---|---|
| damage attribution | attributed damage in the death round == summed negative `UpdateHp` | **335/335 agree, 0 mismatches** |
| core-damage channel | independent second pass summing `UpdateHp` on each core id | **60/60 team-sides agree** |
| delivered-Ti channel | `titaniumCollected` (UpdatePlayers f4) vs `distributeResources` stacks × 10 | **30/30 agree** |
| "no-damage removal == our own `destroy()`" | any our-building removed at PARTIAL hp with no damage event would falsify it | **0/30 games show one** |
| team attribution on barriers | our barriers hugging our own core / their barriers hugging their own core must be ~0 | **0 and 0** (238 theirs-near-us, 94 ours-near-them) |
| `covered_at_death` (ray test) | relax the facing ray to an any-facing disc — the count must RISE | **belt 3/63 → 10/63, harvester 3/15 → 5/15** (not a constant column) |
| rebuild-ban counter | run the same counter on tape30, where the loop is documented to reach 22 | **tape30: maxPerTile 22, 6 tiles ≥3 builds, 6/6 BAN VIOLATIONS.** tape602: maxPerTile 2, 0/4 violations |
| belt-gap BFS | re-run with enemy barriers made passable — "unreachable" must collapse | **25 unreachable → 0; 33 land at exactly gap 1** (see §2.3) |

---

# QUESTION 1 — WHAT BLOCKS THE FULL SEAL

Headline: **0/30 full seals is not one blocker, it is three, and only the third is
about the walker.** Open seat count is 8/8 on all 30 games (no wall ever removes a
seat).

## 1.1 (a) Ever-built vs never-attempted

| | pooled (240 tile-slots = 8 × 30) | median/game |
|---|---|---|
| seal tiles our barrier was EVER built on | **103** (42.9%) | 4 of 8 |
| never attempted | **137** (57.1%) | 4 of 8 |
| ring builds total (incl. re-lays) | 110 | — |
| ring barriers LOST | 24 | — |
| max simultaneous held | — | **3 of 8** |
| games reaching max_held == 8 | **0/30** | — |
| games reaching max_held ≥ 7 | **1/30** (glacierkeep_A) | — |

## 1.2 The three blockers, decomposed

### BLOCKER 1 — the enemy's own delivery belt owns the ring. **Structural ceiling: median 5 of 8.**

Of the 137 never-attempted tiles, **91 were occupied by an enemy building — and the
kind census is 100% CONVEYOR: 18,381 tile-rounds, zero barriers, zero turrets,
zero anything else.** Their belt must terminate orthogonally adjacent to their core,
so those tiles are seal seats *by construction*.

* contested tiles (enemy building ever present): **median 3 of 8, mean 3.17**
* hard ceiling without eviction = open − contested: **median 5**
* our max_held: **median 3**

⇒ **The 8 → 5 half of the gap is not reachable by building. It is only reachable by
EVICTING their belt** — which is the thing the walker almost never does.

### BLOCKER 2 — the eviction interlock. **This is THE cause and it is a one-line gate.**

`_clear_tile` on the forward lap tile is gated `if not empty_seals`
(`sk_roles.py:1627`), and the off-lap eviction extension is gated
`here is None and not empty_seals` (`sk_roles.py:1672`). So **eviction is armed only
in a round where NO seal tile anywhere on the ring is empty.**

Measured per round over all 6,954 game-rounds:

* rounds with zero empty seal tiles (eviction ARMED): **539/6,954 = 7.75%**
* **games where it was NEVER armed: 24/30 (0.0% of their rounds)**
* games with ANY eviction attack: **6/30** — and they are exactly the games that had
  armed rounds. The predicate and the behaviour agree cell-for-cell.

**And when it does fire it works.** Attack counts are 10/10/10/10/8/20 — a conveyor is
20 HP against a 2-dmg peck, i.e. **exactly ten pecks per conveyor**. Those 6 games
killed 6 enemy ring conveyors, and **10 of 30 games reached max_held ≥ ceiling**;
glacierkeep_A reached **7 of 8, above its own 6-tile ceiling**, only because eviction
fired. In that game the enemy's `titanium_collected` finished at **0**.

The second gate, `_enemy_builder_adjacent` (`sk_roles.py:1814`), is **not** the
binding one: it covers only **2,829/18,381 = 15.4%** of contested tile-rounds
(per-tile median 9.0%; 0 of 95 tiles refused 100% of the time, 0 refused 0% — the
column genuinely varies). Real, secondary.

### BLOCKER 3 — the walker never gets there. **6 of 30 games.**

Lap tiles our builders ever stood on (of 12): **median 10.5, mean 9.07**. But six
games read 1, 2, 2, 3, 4, 5 — helheim_A, valkyrie_A/B, stavkirke_B, midgard_A/B —
and those are precisely the max_held 0/1 games. Where the lap runs it works; where
it doesn't, nothing else matters.

Of the **46 free-but-missed** tiles (never attempted, never enemy-occupied):
* **19/46** the walker was never on it nor adjacent → reachability
* **23/46** the walker STOOD on the tile (it cannot build under itself; the
  seal-behind rule then has to fire on the next step and did not)
* **25/46** had the tile empty, our builder orthogonally adjacent and bank ≥ 6 Ti —
  **356 pooled opportunity-rounds, median 6 per tile, max 48.** Funding is not the
  constraint.
* lap-index distribution is flat (7/3/5/4/6/7/8/6 across the 8 seal indices) —
  **no geometric bias; this is decision logic, not lap shape.**

## 1.3 (b) Built-then-lost: who removes our ring barriers

24 losses across 30 games. **All 24 are enemy turret kills** — sentinel 14, gunner 10.
**Zero self-demolitions, zero pecks.** (The `_escape` full-HP demolition residual does
not touch the ring; it does touch the belt — see §2.4.)

* re-lay latency: **median 7 rounds, mean 33.7, min 6, max 172; 0 of 7 within 2
  rounds** vs BC's 1.08-round barrier-after-clear.
* **17 of 24 losses were never re-laid at all.**

Loss rate is low (24 losses vs 110 builds) so this is a **third-order** blocker —
worth a line in a v603, never the headline.

## 1.4 (c) Eviction engagement on never-attempted tiles

* never-attempted tiles our walker ever attacked: **5/137**
* never-attempted tiles our builder was ever on or adjacent to: **104/137**
* contested tiles our builder was ever on or adjacent to: **81/95**; ever attacked:
  **7/95**

⇒ **The walker reaches the tile and refuses. The off-lap eviction extension is
present in the code and effectively dead on the tape** — it carries the same
`not empty_seals` gate that kills the on-lap path.

## 1.5 (d) THE SEAL-vs-WIN ANSWER — and it settles the doctrine question

**Damage dealt to the enemy core, pooled over all 30 games:**

```
{'sentinel': 14130}      ← 100.0%
```

**Zero pecks. Zero gunner. Zero launcher.** Symmetrically, damage to OUR core is
`{'sentinel': 13608}` — 100% sentinel both ways.

Cage state at the moment of each of our 6 kills (ours / enemy-held / empty of 8):

| game | kill round | seal state | max_held |
|---|---|---|---|
| bifrost_B | r169 | 4 / 3 / 1 | 4 |
| fimbulwinter_A | r140 | 5 / 2 / 1 | 5 |
| glacierkeep_A | r227 | 7 / 1 / 0 | 7 |
| **helheim_A** | r332 | **1 / 5 / 2** | 1 |
| **holmgang_B** | r282 | **1 / 4 / 3** | 3 |
| skald_B | r154 | 4 / 3 / 1 | 5 |

⇒ **THE KILL ARRIVES INDEPENDENT OF THE CAGE. It is the nest sentinel shooting past
an open ring, in every one of the six.** Two of the six killed with ONE ring tile
held. First damage on the enemy core lands at median r34 (range 16–120), median 2
shooter tiles per kill; our first sentinel goes up at median r31.

**SK_CAGE_FIRST has, as a side effect, switched off the walker's only damage
channel.** The rule puts the enemy core off the peck ladder *while seal tiles
remain* — and seal tiles remain in 30 of 30 games, because `sealed` can only reach
`SK_CAGE_ACCEPT = 7` if we evict their belt, which the interlock forbids. Enemy-core
pecks went 1,029 → **0**, and the build report booked that as a win. On this tape it
is the walker contributing nothing at all.

### What the cage IS worth, measured

The only live channel left is **denying their healers standing room**. Their core
absorbs a large heal tax:

* heal-tax (HP healed ÷ HP we dealt, over the window their core was under fire):
  **median 0.68**, range 0.00–0.91
* games with mean-held < 3: heal-tax **0.71**, wins **2/17**
* games with mean-held ≥ 3: heal-tax **0.49**, wins **4/10**

Suggestive, confounded (both move with how well the game went generally), n small.
**Report it; do not price a plank on it yet.**

The decisive cross-tab is different:

| | max_held ≤3 | max_held ≥4 |
|---|---|---|
| **≤1 sentinel built** | 0 wins / 8 | **0 wins / 6** |
| **≥2 sentinels built** | 2 wins / 8 | 4 wins / 8 |

**0 wins in 14 games with ≤1 sentinel, 6 in 16 with ≥2** (Fisher 2-sided
**p = 0.019**). **A good cage with one sentinel is 0 for 6.** The seal is at best a
multiplier on the gun; it is never a substitute for it.

---

# QUESTION 2 — BELT SURVIVAL

## 2.1 (a) Harvesters — **the tape30 rebuild loop is DEAD; the killer class survives**

| | tape30 | **tape602** |
|---|---|---|
| harvesters built | 94 | **91** |
| harvester deaths | 66 | **15 (16.5%)** |
| alive at end | 28 | **76** |
| max harvesters on one ore tile | **22** | **2** |
| ore tiles with ≥3 harvesters built | 6 | **0 of 86** |
| tiles reaching escalation (≥2 deaths) | 6 | 4 |
| **rebuild-into-banned-tile violations** | **6/6** | **0/4** |

**SK_HARV_ESCALATE holds, cleanly, and the control fires on tape30.** Harvester
deaths are 0.50/game (median 0).

**Killer class is unchanged: 15/15 harvester deaths are annulus gunners**, killer
standing d² to our core median **45**, range 26–100, **15/15 inside the d² 20–100
annulus**. Harvester lifetime when killed: median 10 rounds. The class persists; the
ban simply stops us feeding it.

## 2.2 (b) CONVEYOR deaths — **the mechanism has MOVED, and the plank is aimed at the old one**

63 belt deaths in 30 games (432 built, **14.6%** loss rate; median 1/game).

| killer | n | share |
|---|---|---|
| **THEIR builder PECK, standing d² ≤ 13 of OUR core** | **44** | **69.8%** |
| our own `destroy()` (no damage, full HP) | 10 | 15.9% |
| their gunner, annulus d² 20–100 | 9 | 14.3% |

All 44 pecks are **theirs** (team-split control run). Victim geometry:

* victim d² to OUR core: **median 1**; `d²≤4`: **53/63**, `5–13`: 2, `14–32`: 7, `>100`: 1
* **belt deaths on tiles that `_trunk_tiles()` EXCLUDES by `SK_TRUNK_DSQ = 13`:
  55/63 = 87.3%**

⇒ **SK_BELT_COVER is defined over "the trunk beyond d² 13 of our core" and 87.3% of
the belt dies inside that cut.** The plank is measuring and siting against the
tape30 killzone. The killzone moved to the terminus.

Coverage at death (victim inside a live facing-ray of one of our turrets):
**belt 3/63, harvester 3/15 — 6/78 = 7.7%, vs the 0/42 baseline.** Non-zero for the
first time; still ~nothing, and **only 2 of the 44 peck deaths were covered**, which
is the class that matters.

Belt re-lay: 19 of 63 losses were re-laid, **median latency 21 rounds**. 3 of 413 belt
tiles were built 3+ times (`SK_REBUILD_ESCALATE = 3` is not binding).

## 2.3 (c) Delivered-vs-died economics — **and the real M1 cause**

* Ti delivered to core: **median 245/game, mean 386** (wins median **585**, non-wins **180**)
* M1 directed connectivity at end: **19/76 = 25.0%** (undirected 24/76 = 31.6%) vs BC 81.4
* 66 of 76 alive harvesters emitted at least one stack; **only 19 have a route home**

**The M1 gap is NOT survival — 86% of the belt and 84% of the harvesters live to the
end. It is TERMINATION.** 0-1 BFS at end of game (0 to cross our live belt, 1 per tile
that would have to be built) from our core to each alive harvester:

```
gap 0 (complete): 29/76 = 38.2%   1-2 short: 10   3-5: 4   6-10: 5   >10: 3
UNREACHABLE (no buildable route exists at all): 25
```

**CONTROL — re-run the identical BFS with enemy barriers made passable:**

```
{0: 29, 1: 33, 2: 5, 3: 4, 4: 3}   ← unreachable: 0
```

⇒ **All 25 unreachable harvesters, and 33 harvesters in total, are exactly ONE
ENEMY BARRIER away from a complete route home.**

### THE MIRROR CAGE — the finding that ties both questions together

`_v542wave` runs the cage on **US**, and runs it better than we run it on them.

Barrier census at end of game, pooled over 30 games:

```
their barriers hugging OUR core   (d²≤8): 238
their barriers hugging THEIR core (d²≤8):   0
our  barriers hugging THEIR core  (d²≤8):  94
our  barriers hugging OUR core    (d²≤8):   0
```

On **our** 8 delivery tiles, at end of game:

| | enemy-held |
|---|---|
| **median** | **6.5 of 8** |
| 8 of 8 | 5 games |
| ≥4 of 8 | **26/30** |
| 0 of 8 | **0/30** |

against **our max_held median of 3** on theirs. Timeline: first enemy building on our
delivery ring at **median r11** (30/30 games), reaching 4/8 at **median r18**
(29/30). We do build a terminal conveyor in 28/30 games — and then lose it: 495 of
their pecks, **100% of their entire peck budget, land on our conveyors at our own
core.**

### And our own peck budget answers the wrong question

Builder-attack census, pooled, 30 games:

| our pecks | n | share |
|---|---|---|
| **their BARRIERS on OUR core ring** | **2,179** | **91.1%** |
| their conveyors on THEIR ring (the seal eviction) | 68 | 2.8% |
| their sentinels (all zones) | 84 | 3.5% |
| their gunners | 40 | 1.7% |
| **their CORE** | **0** | **0.0%** |
| **total** | **2,393** | |

| their pecks | n | share |
|---|---|---|
| **our conveyors at our own core** | **495** | **100%** |

We spent 2,179 pecks on their collar and destroyed **106** of it (a barrier is 30 HP =
15 pecks, so ~1,590 pecks were "productive" and ~589 lost to their re-heal/re-lay);
**238 collar barriers were still standing at the end.** They spent 495 pecks and took
our M1 from a possible 81% to 25%.

**We are outspending them 4.8:1 on melee and losing the exchange.** This is v602
residual #3 (`_threat_scan` counts a barrier as a home threat) at full size — but note
the target class is not wrong, the *race* is: 2 dmg/round against a 30 HP barrier they
re-lay at ~1 round is a race we cannot win by pecking alone.

## 2.4 Our own destroy()s

10 of 63 belt deaths are ours, at full HP, no damage event — lifetimes 9, 42, 56, 74,
276, 21, 45, 10, 12, 28. Consistent with the v602 residual #1 `_escape`
full-HP-demolition class plus belt re-plan churn. Small, real, unfixed.

## 2.5 (d) Did SK_BELT_COVER buy trunk guns?

**27 gunners in 30 games (0.90/game)** — `SK_DOOR_GUN_CAP = 2` is not binding, the
trigger is.

* sites, d² to our core: `≤4`: 1, `5–13`: 9, `14–32`: 10, `>32`: 7 — **median 20**
* the belt actually dies at `≤4`: **53**, `5–13`: 2, `14–32`: 7, `>32`: 1
* **ever fired: 18/27, 157 shots**
* victims: their builder_bot **79**, their launcher 40, their sentinel 24, their
  gunner 12, their conveyor 2
* **survived to end of game: 27/27. Zero gunners lost, all 30 games.**
* distinct enemy belt-killer tiles: 52; **killer removed during the game: 6**

⇒ **The guns are cheap, safe and effective at what they shoot — and they are sited a
ring too far out.** They shoot enemy builders 79 times, which is exactly the class
eating our belt, but at median d² 20 while 84% of the belt dies at d² ≤ 4.

### Sentinels, for contrast

48 built (median 2/game, range 0–4), **45/48 sited in the d² 14–32 band of their
core**, 46/48 ever fired, **875 shots, 785 of them into the enemy core**, 33/48
survived. The 15 that died were killed by enemy gunner (7) and sentinel (8), median
lifetime 13 rounds.

---

# RANKED v603 CANDIDATES

Ranked by **measured size of the channel × directness of the fix**. Every number is
from this tape (30 games, one authored opponent).

### 1. Fix the terminus, not the trunk — `SK_TRUNK_DSQ` inversion + terminus guard
**Channel: 87.3% of belt deaths (55/63) and 33 of 76 harvesters one tile from home.**
`_trunk_tiles()` excludes `d² ≤ 13` of our core; the belt dies at median d² 1. Include
the terminus in the cover set, and site the door gunner so its ray covers the
terminal conveyor and the tile their pecker must stand on. Evidence it is affordable:
our gunners are **27/27 survivors, 157 shots, 79 of them into enemy builder bots.**
Cost: a constant and a scorer term. Falsifier: `covered_at_death` for peck-class belt
deaths must rise from **2/44**; belt loss rate must fall from 14.6%.

### 2. Arm the eviction — drop the `not empty_seals` interlock
**Channel: the 8 → 5 half of the seal gap, in 24 of 30 games where eviction was never
once armed (7.75% of all rounds).** When armed it costs exactly ten pecks per conveyor
and converts: 6/6 games that armed it killed a ring conveyor, glacierkeep_A reached
**7/8 above its own 6-tile ceiling** and held the enemy to `titanium_collected = 0`.
Suggested form: allow eviction of a contested seal tile whenever the walker stands on
the lap with it forward AND the number of empty seals is below some small k (or
simply: prefer the empty tile, but never *forbid* the eviction). Falsifier: full seals
> 0/30; max_held median must exceed the 5-tile ceiling.

### 3. Buy the second sentinel — the only variable that separates wins from losses
**Channel: 0 wins in 14 games with ≤1 sentinel; 6 in 16 with ≥2 (Fisher p = 0.019).**
100% of all core damage in both directions is sentinel fire; median heal-tax on their
core is 0.68, and one sentinel at 9 dmg/round barely out-paces their ~3.9 HP/round of
healing. Two is the threshold. Games with ≥2 sentinels also delivered **440 Ti median
vs 120** — so this is partly downstream of candidates 1 and 4, but the direct lever
(spend the second 30 Ti on a sentinel before anything else) is available now.

### 4. Break the collar with something other than pecks
**Channel: 2,179 pecks (91.1% of our entire melee budget) spent on their collar; 106
killed, 238 still standing at end; their collar reaches 4/8 of our ring by r18.**
Pecking a 30 HP barrier at 2 dmg while they re-lay is a losing race, and it is
starving the seal eviction (68 pecks) and everything else. Options in cost order:
(a) route the belt terminus to a ring tile they have not sealed yet — they reach 4/8
at r18, not 8/8, and 3 of 8 are still empty at end in several games; (b) let a gunner
covering the ring kill the *builder* rather than pecking the *barrier*; (c) cap the
`_threat_scan` barrier-as-threat behaviour (v602 residual #3) so the budget goes
somewhere it can win.

### 5. Give the walker a damage channel back
**Channel: `SK_CAGE_FIRST` drove enemy-core pecks 1,029 → 0, and `sealed` never
reaches `SK_CAGE_ACCEPT = 7` in 30/30 games, so `_attack_enemy_core` is unreachable
via the accept path.** The build report banked the 0 as a win; on this tape the walker
contributes zero damage all game. Suggested form: make the accept bar reachable —
either lower `SK_CAGE_ACCEPT` to the measured ceiling (open − contested) rather than a
fixed 7, or re-admit the core to the ladder once the ceiling is met. Falsifier: peck
damage on the enemy core > 0 without kill-round regression past r300.

### 6. Fix the six games where the lap never runs
**Channel: 6/30 games with ≤5 of 12 lap tiles ever visited, all of them max_held 0–1.**
helheim_A, valkyrie_A/B, stavkirke_B, midgard_A/B. Diagnose as reachability, not
decision logic — separate from the 25/46 free-but-missed opportunity class.

### 7. Ring re-lay latency (third order)
24 ring losses, all enemy turret kills; **median re-lay 7 rounds, 17/24 never re-laid**
vs BC's 1.08. Small channel; a line, not a plank.

---

## Two engine/opponent facts worth banking

1. **`_v542wave` (NOISE_OFF) does NOT seal its own core — it seals OURS.** 238 of its
   barriers hug our core, **0** hug its own. The `_clear_tile` comment at
   `bots/_v602skalman/sk_roles.py:1813` attributes "the bulk of the 1,280 barrier
   pecks" to "`_v542wave`'s MAINTAINED seal" — on this tape the enemy buildings on
   *their* ring are **100% conveyor, 0 barriers** (18,381 tile-rounds). The barrier
   seal we are pecking is the one around **our own** core.
2. **The enemy's delivery conveyors are seal seats by construction.** Any cage
   doctrine that refuses to evict them has a hard ceiling of `8 − (their belt width)`,
   measured here at **median 5 of 8**.
