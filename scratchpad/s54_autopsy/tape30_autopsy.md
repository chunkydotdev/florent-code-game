# SKALMAN v1 (`bots/_v600skalman1`) — DEATH-CAUSE AUTOPSY OF THE FOUNDING BASELINE TAPE

**Builder s54, 2026-08-21.** Read-only decode of `scratchpad/s54_fidtape/replays_tape30/*.replay26`
(30 files, 3.8 MB, local `.replay26`). Subject = **team A / side 0** in all 30, verified
independently of the filename (team 0 spawns exactly 4 builders at r0-r3 and stops — SKALMAN's
fixed-role chassis; team 1 spawns 5+, `_v542wave`'s `MAX_BUILDERS`). Companion to
`docs/research/FIDELITY-BASELINE-v600-2026-08-21.md`, which measured *whether the verbs fire*;
this measures *what kills us*.

Decoder: `tape30_deaths.py` + `tape30_analyse.py` (this scratchpad). No repo file touched, no
match fired.

---

## 0. INSTRUMENT — validated in both directions before any number below was trusted

### 0.1 Attribution method (replicated from the DOORWAVE decode)

`scratchpad/s54_doorwave_decode/doorwave_decode.py` established the damage-signature method;
this decoder reuses it verbatim in structure and adds the victim-resolution half:

* `FireTurret {from,to}` → victim = **UNIT on `to` if one stands there, else the BUILDING on `to`**
  (`tools/replay_schema.md` damage-target law). Shooter type looked up on `from`: **gunner = 7,
  sentinel = 18**.
* `BuilderAttack {id,target}` → victim = **the BUILDING on `target`, never the unit**. **peck = 2**.
* **Per-round shadow index**, the DOORWAVE fix: `removeEntity` is emitted BEFORE the killing
  blow's event inside the same round, so resolving a target against the live tile index alone
  drops exactly the killing event.

**Self-check, per death:** attributed damage in the death round must equal the summed NEGATIVE
`UpdateHp` deltas on that entity id in that round.

### 0.2 Both guards driven to the other verdict (a check that has never failed has not been seen to check)

| run | mismatches | deaths with no attributed source |
|---|---|---|
| **BASELINE** | **0 / 246** | 49 / 295 (all 49 are ENEMY launchers/barriers — their own `destroy`) |
| MUTANT: gunner damage 7→6 | **166 / 246** | 49 / 295 |
| CONTROL: shadow index OFF | 7 / 37 | **258 / 295** |

Perturbing the damage alphabet by one point breaks 166 of 246 checks; removing the shadow index
destroys 88% of all attribution. The instrument is sensitive to exactly the two things it claims
to resolve.

### 0.3 Cross-validation against the published fidelity read

Computed independently here, matching `tools/skalman_fidelity.py` numbers digit-for-digit:

* **M5b**: games with >4 distinct subject builder ids = **8 of 15 distinct games** = the doc's
  16/30. ✅
* **M7**: enemy forward gunners+sentinels **28 built, 6 removed** per 15 distinct games = the
  doc's **12/56**. (The doc's headline 17.8% is the games-as-units mean; the pooled ratio is 21.4%.) ✅

### 0.4 ⛔ ALARM — THE TAPE IS n=15, NOT n=30. THE SEED IS INERT.

Every `*_s11` / `*_s12` pair is the **same game**. Comparing all non-`BotOutput` updates
pairwise, in **15 of 15 map pairs** every `placeEntity`, `removeEntity`, `moveBuilderBot`,
`updateHp`, `fireTurret` and `builderAttack` is **byte-identical**; the only differing update
kind is `distributeResources` (4) — plus derived `updatePlayers` (6) on midgard alone.

```
auroraveil   updates=6709  diffs=249  kinds=[4]      icefloe    updates=5787  diffs=249  kinds=[4]
bifrost      updates=2452  diffs= 73  kinds=[4]      jotunheim  updates=26972 diffs=527  kinds=[4]
...           midgard    updates=2389  diffs=102  kinds=[4,6]   (15/15 pairs, no exceptions)
```

Death lists and birth lists hash identically in 15/15 pairs.

⇒ **Every combat, survivability and build metric on this tape has effective n = 15.** The
fidelity baseline's `±ci95` figures were computed games-as-units over 30 slots with each map
counted twice; the true half-widths are **~×1.41 wider**. This does not move any verdict in that
doc (the misses are enormous), but it must not be carried into a v601-vs-v600 comparison, where
a duplicated control is a fake denominator. **Vary the map pool or the seat, not the seed** —
with both bots deterministic and the maps fixed, the seed only perturbs resource-move ordering.

**All numbers below are over the 15 DISTINCT games** unless a denominator says otherwise.

---

## 1. Q1 — OUR HARVESTER DEATHS

| | value |
|---|---|
| harvesters built (subject) | **47** |
| alive at end | 14 |
| **died** | **33** |
| **killer class** | **gunner 33/33 (100%)** — 0 sentinel, 0 peck, 0 non-combat |
| killer standing position, d² to OUR core | **annulus 20-100: 33/33**; median **41**, range 26-45 |
| lifespan, build→death | **median 9 rounds** (quartiles 9 / 9 / 9; min 8, max 40) |
| **had ever delivered to the core (wired)** | **18.2% (6/33)** |
| had emitted ≥1 stack at all | 36.4% (12/33) |
| death round | median r122 |

**The killer position is the LOKI-BELTBREAK annulus signature, exactly.** `_v542wave`'s doctrine
plants a gunner in the **d² 20-100 annulus of the enemy core aimed at live belt**
(`bots/_v542wave/raid.py:927`, `main.py:2311`). Every one of our 33 harvester deaths came from a
gunner standing in that band. Not one came from a builder peck; not one from a sentinel.

### 1.1 The deaths are three rebuild loops, not 33 independent events

| map | tile | kind | deaths | span |
|---|---|---|---|---|
| icefloe | (3,11) | harvester | **22** | r17 → r338 |
| midgard | (3,9) | harvester | 6 | r48 → r94 |
| auroraveil | (6,7) | harvester | 4 | r54 → r82 |
| auroraveil | (7,7) | conveyor | 3 | r89 → r101 |

**32 of 33 harvester deaths sit on 3 tiles**, and all 33 fall in **3 of 15 games** (icefloe 22,
midgard 7, auroraveil 4). **8 distinct enemy shooter positions** account for all 42 of our
belt+harvester deaths; the top three account for 36 of them.

### 1.2 WORKED EXAMPLE — `icefloe_s11`, one gunner, twenty-two harvesters

Map 20×20, our core (1,16), theirs (17,2).

```
r5   THEM launcher  @(15,4)   d²_ourcore=313
r7   THEM launcher  @(11,8)   d²_ourcore=145
r9   THEM gunner id20 @(6,11) d²_ourcore=41   d²_theircore=185   <-- ANNULUS PLANT, forward
r10  THEM launcher  @(7,12)   d²_ourcore=41
...
r6   US harvester id14  @(3,11)     r17  id14  DIES  life=11  killer=gunner from=(6,11)
r63  US harvester id103 @(3,11)     r73  id103 DIES  life=10  killer=gunner from=(6,11)
r86  US harvester id129 @(3,11)     r95  id129 DIES  life= 9  killer=gunner from=(6,11)
r95  US harvester id137 @(3,11)     r104 id137 DIES  life= 9  killer=gunner from=(6,11)
   ... identical line 18 more times, every 9 rounds, to ...
r329 US harvester id387 @(3,11)     r338 id387 DIES  life= 9  killer=gunner from=(6,11)
```

**One gunner, planted at r9, never touched for the remaining 337 rounds, ate 22 harvesters
(440 Ti at base cost, more at scale) off a single ore tile.** The 9-round clock is the mechanism
in plain sight: harvester 30 HP ÷ 7 dmg = 5 shots at reload 1 ≈ 9-10 rounds including our build
cooldown. Every attributed peck/shot passes the `UpdateHp` self-check; the loop is not an
artefact.

### 1.3 The code defect this names

`bots/_v600skalman1/sk_roles.py:309 _harvester_action` has **no rebuild counter, no death memo,
no ban set** — it rebuilds on any adjacent home-half ore tile, forever.

The guard already exists **for conveyors only**, thirteen lines of docstring away:

> `sk_roles.py:437 _belt_action` — *"LEDGER V1 (the most expensive bug in the study: sixteen
> rebuilds of one conveyor at 6-round intervals into a stationary gun): a tile rebuilt
> `SK_REBUILD_ESCALATE` times WITHOUT SURVIVING stops being rebuilt and becomes a
> locate-the-shooter task. Rebuild #4 never happens."*

**We diagnosed this exact bug, wrote the fix, and applied it to the wrong building type.** The
conveyor path escalates at 3 (and the tape shows the conveyor loop stopping at 3 on
auroraveil (7,7) — the guard works where it is wired). The harvester path ran to **22**.

### 1.4 Supply-side note

**7 of 15 games we built ZERO harvesters** (fimbulwinter, holmgang, jotunheim, longhouse, paths,
stavkirke, yggdrasil). Per-game harvester builds: `[6,2,0,2,2,0,22,0,0,9,0,2,0,2,0]`. M1
connectivity's thin denominator is partly a supply problem, not only a survival one — though
under `R1000_IS_DEFEAT` this is instrumental, not scoring.

---

## 2. Q2 — OUR BUILDER-BOT (ROLE BODY) DEATHS

| | value |
|---|---|
| spawned (subject) | **81** across 15 games |
| **died** | **22** |
| killer class | **gunner 12, sentinel 10**, **peck 0** |
| **non-combat removals (no damage event in the death round)** | **0** ⇒ **ZERO exception deaths, zero self-destructs — ALARM CHANNEL CLEAN** |
| died in OUR half / THEIR half | **9.1% (2/22) / 90.9% (20/22)** |
| lifespan | median 44 rounds; death round median r129 |

### 2.1 By role — **HEURISTIC**, label it as such

Role is not observable in a replay (it is claimed on comms slots, which replays do not carry).
Inference used: SKALMAN claims **the lowest role id whose liveness beat is stale**
(`sk_roles.py:142 _claim_role`), and the first four bodies spawn r0-r3 in order, so role =
*spawn order, with a replacement taking the lowest currently-dead slot*. This is exact for the
opening four and approximate for replacements (the beat is stale-gated at `SK_BEAT_STALE = 3`,
so a body respawned within 3 rounds of a death could claim differently).

| inferred role | deaths | med life | died in our half | gunner | sentinel | peck |
|---|---|---|---|---|---|---|
| HOME_KEEPER | 2 | 86 | 2 | 2 | 0 | 0 |
| **CAGE_WALKER** | **15** | 41 | **0** | 6 | 9 | 0 |
| ORE_DENIER | 0 | — | — | — | — | — |
| SIEGE_ENGINEER | 5 | 49 | 0 | 4 | 1 | 0 |

**The forward roles are the mortality.** 20 of 22 bodies die in the enemy half, and the CAGE
WALKER alone is 15 of 22 (68%) — it marches the enemy ring under their home turrets and dies to
sentinel fire (9) more than to anything else. This is the mechanical driver behind M5b
(exactly-4 = 46.7%), M2b (0/30 seals — the walker rarely lives a full lap) and M5f/g/h (forward
roles rarely live long enough to register). ORE_DENIER never died in 15 games, consistent with
its `_under_attack` yield rule keeping it home.

### 2.2 Launcher displacement — real, and NOT lethal

**147 of our builders were thrown by enemy launchers** (theirs threw 92 of their own — the
`_v542wave` ferry). **0 of 147 died within 10 rounds of being thrown.** Concentrated in
glacierkeep (90) and jotunheim (31), the two longest games; median throw round r387.

⇒ **The crash-induction class does not work on us** — our own `is_tile_*` guards hold, exactly as
the CLAUDE.md note about mining our own bug fixes predicts. It is a **tempo tax on the forward
roles**, not a kill channel, and it should not be ranked as a survivability cause.

---

## 3. Q3 — OUR OWN TURRET DEATHS

| kind | built | died | median life | killers |
|---|---|---|---|---|
| gunner | **13** | **0 (0%)** | — | — |
| sentinel | 5 | 2 (40%) | 110 | enemy gunner ×2 |

* of ours, **FORWARD** (nearer their core): 5 built, 2 died, median life 110.
* of ours, **HOME RING** (d² ≤ 13 of our core): **12 built, 0 died.**
* turret builds per game: **median 1** (18 total across 15 games).
* **No replant loop** — nothing of ours dies often enough to need one.

**Our turrets are not the thing dying.** The problem is that there are almost none of them (1 per
game median) and they are all sited in one place — see §5.

---

## 4. Q4 — THE ENEMY KILL CHAIN (pooled medians, n=15 distinct games)

| event | median round | n games with the event |
|---|---|---|
| enemy builder first enters our half | **r8** | 15/15 |
| enemy plants first forward **LAUNCHER** | **r9** | 14/15 |
| enemy first shoots one of our **builders** | r36 | 8/15 |
| enemy first shoots one of our **harvesters** | r43 | 3/15 |
| enemy plants first forward **GUNNER/SENTINEL** | **r60** | 15/15 |
| **our core takes first damage** | **r90** | 15/15 |
| **our core dies** | **r180** | **14/15** |

Game length median **r188**. Our core destroyed in **14 of 15**. **We won 0 of 15.**
(The single survivor, jotunheim, ran to r1000 and lost on `titanium_collected` — a defeat twice
over under `R1000_IS_DEFEAT`.)

### 4.1 The annulus-ladder signature — confirmed exactly

Belt-piece kills by enemy turret fire, n=37: shooter standing d² to OUR core —

```
<=13 (on our door)   0
14-19                0
20-100  ANNULUS     37     <-- 37 of 37
>100                 0
shooter type: gunner 37 / 37
```

**Every belt kill comes from a gunner in the d²20-100 annulus.** This is `_v542wave`'s
LOKI-BELTBREAK plant, unmodified and unanswered.

### 4.2 What actually kills our core — and it is a different weapon entirely

Total damage landed on our core across 15 games: **9,126** (exceeds 15 × 500 because we heal it).

| source | damage | share | shooter d² to our core |
|---|---|---|---|
| **sentinel** | **9,126** | **100.0%** | **median 8, range 2-25** |
| gunner | 0 | 0% | — |
| builder peck | 0 | 0% | — |

Distinct core-damaging shooter positions per game (d² to our core):

```
auroraveil [5] · bifrost [4] · fimbulwinter [8,25] · glacierkeep [9] · helheim [13,25]
holmgang [4,4] · icefloe [25] · jotunheim [5,9] · longhouse [4,8,8] · midgard [25]
paths [9,9] · skald [2,9] · stavkirke [5,5] · valkyrie [4] · yggdrasil [8]
```

**One to three sentinels, planted point-blank on our door (median plant r120, range r40-r537),
do 100% of the damage that ends the game.** The beltbreak gunner shreds the economy; the
point-blank sentinel does the killing. **They are two separate mechanisms with two separate
counters, and v600 answers neither.**

---

## 5. Q5 — WERE OUR DEAD BELT TILES COVERED BY OUR OWN TURRETS?

Coverage computed geometrically from entity positions/types/facings at the exact death round
(gunner r²≤13 along facing ray, **obstacles ignored → an upper bound**; sentinel r²≤32 along
facing ray, which truly ignores obstacles).

| | value |
|---|---|
| our belt pieces destroyed | **42** (33 harvester, 9 conveyor, 0 splitter) |
| **inside a live turret's ACTUAL FIRING LINE at death** | **0.0% (0/42)** |
| inside a live turret's radius on ANY of 8 facings (rotate-if-you-could, loose bound) | 14.3% (6/42) |
| **no live turret of ours existed at all at that moment** | **54.8% (23/42)** |

| kind | died | ray-covered | any-facing | no turret alive |
|---|---|---|---|---|
| harvester | 33 | 0.0% (0/33) | 18.2% (6/33) | 66.7% (22/33) |
| conveyor | 9 | 0.0% (0/9) | 0.0% (0/9) | 11.1% (1/9) |

### 5.1 The siting mismatch, in one line

```
our 18 turrets, d² to our core:  [1,2,4,4,4,5,5,8,9,10,10,10, 26, 137,137, 377,377, 761]
our 42 dead belt tiles, d²:      median 26, range 1..36
dead belt tiles at d² > 13:      85.7% (36/42)
```

**Twelve of our eighteen turrets sit inside d²≤10 of our own core. 85.7% of the belt that dies
sits outside d²=13 — beyond the entire band our home turrets occupy.** The uncovered-belt-tile
gap that our tree publishes on store slot 5 b18-23 and never reads is not a partial gap: on this
tape it is **total**. #116's coverage-geometry finding applies to us at **0.0% coverage**.

---

## 6. Q6 — WHAT OUR DOOR ANSWERED (M7)

Scope = **gunner + sentinel only**, matching `tools/skalman_fidelity.py:113 TURRETS`.
(Enemy forward **launchers** excluded: 37 built, 24 removed, of which **21 with no damage event
at all** = their own `destroy`/resite, not our answer. Counting them would have inflated our
"removal rate" from 21% to 46% on their housekeeping.)

| | value |
|---|---|
| enemy forward turrets built (nearer OUR core than theirs) | **28** |
| **removed** | **21.4% (6/28)** — reconciles with the doc's 12/56 |
| **what removed those 6** | **our gunner fire 5, our builder peck 1** |
| median life of a removed forward turret | 7 rounds |
| **unanswered** | **22** |

### 6.1 The 22 unanswered — reachability, not intent

| | share of the 22 |
|---|---|
| EVER inside one of our live turrets' firing line | **4.5% (1/22)** |
| EVER inside a live turret's radius on any facing | 9.1% (2/22) |
| EVER orthogonally adjacent to one of our builders (peckable) | **27.3% (6/22)** |

⇒ **Roughly 73% of the unanswered forward turrets were never touchable by either instrument we
own** — not in a turret's line, not adjacent to a body, at any point in their lives.

By band and kind:

| | d²≤13 (our door) | d² 20-100 (annulus) |
|---|---|---|
| unanswered | **14** | 8 |
| removed | 6 | **0** |
| forward **gunners** built / unanswered | 4 / **4** | (all 4 sit in the annulus) |
| forward **sentinels** built / unanswered | 24 / **18** | |

**Every enemy forward gunner we ever faced — 4 of 4, including the icefloe beltbreaker that ate
22 harvesters — survived to the end of its game.** Our removals are 6/6 inside our own door ring;
we have removed **zero** turrets in the annulus, which is precisely where the economy-shredder
lives.

For the **25 turrets specifically identified as having damaged our core**: 6/25 ever in a firing
line, 7/25 ever peckable, 7/25 eventually removed (median life 7).

### 6.2 Where our damage budget actually goes — the barrier sink

| | total landed on an entity | on BARRIERS | on gunners+sentinels | on their core |
|---|---|---|---|---|
| our turret shots | 821 | **618 (75.3%)** | 33 | 92 |
| our builder pecks | 1,712 | **1,280 (74.8%)** | 35 | 366 |

*(our turret hit-breakdown: barrier 618, core 92, builder_bot 58, sentinel 33, launcher 20,
**gunner 0**; our peck breakdown: barrier 1,280, core 366, sentinel 31, conveyor 16, harvester 15,
gunner 4.)*

**Three quarters of everything we shoot and everything we peck lands on an enemy BARRIER.** We
are not short of damage output — we out-peck them 1,712 to 54 — we are spending it chewing
`_v542wave`'s barrier seal while the two turrets that are actually killing us stand untouched.

---

## 7. PER-GAME SUMMARY (15 distinct games; `_s12` is the same game — see §0.4)

| map | rnds | our harv built/dead | our builders born/dead | conveyors dead | our turrets built/dead | enemy fwd turrets built/removed¹ | their 1st fwd turret¹ | our core 1st dmg | our core dies |
|---|---|---|---|---|---|---|---|---|---|
| auroraveil | 325 | 6/4 | 7/3 | 5 | 2/1 | 5/2 | r7 | r265 | r324 |
| bifrost | 116 | 2/0 | 4/0 | 0 | 0/0 | 4/1 | r9 | r61 | r115 |
| fimbulwinter | 138 | 0/0 | 4/0 | 0 | 0/0 | 4/1 | r9 | r65 | r137 |
| glacierkeep | 593 | 2/0 | 10/6 | 0 | 3/1 | 4/2 | r9 | r538 | r592 |
| helheim | 463 | 2/0 | 10/7 | 0 | 0/0 | 4/1 | r7 | r434 | r462 |
| holmgang | 216 | 0/0 | 5/1 | 0 | 0/0 | 3/1 | r7 | r121 | r215 |
| **icefloe** | 347 | **22/22** | 6/2 | 1 | 0/0 | 4/1 | r9 | r292 | r346 |
| jotunheim | 1000 | 0/0 | 5/1 | 0 | 2/0 | 6/5 | r9 | r517 | — (r1000 loss) |
| longhouse | 166 | 0/0 | 4/0 | 0 | 2/0 | 7/4 | r10 | r47 | r165 |
| **midgard** | 97 | **9/7** | 4/0 | 3 | 2/0 | 3/0 | r40 | r41 | **r96** |
| paths | 112 | 0/0 | 4/0 | 0 | 1/0 | 3/1 | r9 | r61 | r111 |
| skald | 188 | 2/0 | 4/0 | 0 | 2/0 | 6/4 | r7 | r61 | r187 |
| stavkirke | 174 | 0/0 | 5/1 | 0 | 1/0 | 4/2 | r7 | r90 | r173 |
| valkyrie | 115 | 2/0 | 5/1 | 0 | 3/0 | 4/3 | r9 | r60 | r114 |
| yggdrasil | 276 | 0/0 | 4/0 | 0 | 0/0 | 4/2 | r11 | r179 | r275 |

¹ this column includes enemy forward **launchers**, whose removals are mostly their own resite —
the M7 gunner+sentinel figures are in §6, not here.

---

## 8. RANKED CAUSES OF THE SURVIVABILITY GAP

### CAUSE 1 — The harvester rebuild loop feeds the annulus gunner forever (33/33 harvester deaths)

**100% (33/33)** of our harvester deaths are annulus gunners at d² 26-45 of our core. **32 of 33
sit on three tiles**; median harvester lifespan is **9 rounds**; **81.8% (27/33) never delivered a
single stack to the core** before dying. One gunner in icefloe converted 22 rebuilds into 22 kills
over 321 rounds without being attacked once.

**The fix is already written and applied to the wrong entity.** `sk_roles.py:437 _belt_action`
carries the `SK_REBUILD_ESCALATE` ledger ("rebuild #4 never happens" — and it works: the
auroraveil conveyor loop stops at 3). `sk_roles.py:309 _harvester_action` has no counter, no memo
and no ban. **v601 plank: extend the belt ledger to harvester tiles, and route an escalated ore
tile into `_escalate_target`'s locate-the-shooter branch, which already exists.**

### CAUSE 2 — Zero belt coverage: our turrets defend the core ring, the belt dies outside it (0/42)

**0.0% (0/42)** of our destroyed belt pieces were inside any live turret of ours' firing line at
death — and that is with the gunner ray computed **ignoring obstacles**, i.e. an upper bound.
**54.8% (23/42)** died with no live turret of ours on the board at all. **85.7% (36/42)** of dead
belt tiles sit at **d² > 13**, outside the whole band where **12 of our 18** turrets are planted
(d² 1-10). We build **1 turret per game (median)** and put it on the core's doorstep.

**v601 plank: the uncovered-belt-tile gap our own tree publishes on store slot 5 b18-23 is never
read. Read it, and site a turret to cover the belt rather than the core ring.** The coverage
number to beat is literally zero.

### CAUSE 3 — The point-blank sentinel is the core-killer and 73% of them were never reachable

**100% of the 9,126 damage** ever landed on our core came from **sentinels standing at d² 2-25** —
zero from gunners, zero from pecks. **18 of 24 enemy forward sentinels were never removed**;
**4 of 4 forward gunners were never removed**. Of the 22 unanswered forward turrets, only
**4.5% (1/22)** were ever in one of our turrets' firing line and **27.3% (6/22)** ever adjacent to
one of our builders — **~73% were never touchable by any instrument we own**. Meanwhile
**75.3% of our turret fire (618/821) and 74.8% of our pecks (1,280/1,712) land on enemy
BARRIERS.**

**v601 plank: the door problem is a TARGET-SELECTION and REACH problem, not a volume problem.**
We out-peck them 1,712 to 54 and spend three quarters of it on barriers. Prioritise the turret
that is dealing core damage over the barrier in front of it, and give the door a weapon that
reaches d²20-100 (a sentinel, r²=32, is the only one of ours that does).

**Not a cause, and worth saying so:** launcher displacement (147 throws of our builders,
**0 deaths within 10 rounds**) and **exception deaths (0 of 22 builder deaths; 0 of ALL 94 subject
removals — 33 harvester, 22 builder, 14 barrier, 14 core destructions, 9 conveyor, 2 sentinel — carry
no attributed damage)**. Our guards hold. Do not spend v601 budget there.

---

## 9. CAVEATS

* **Self-play fixture.** The benchmark is our own retired line (`_v542wave` NOISE_OFF). Kill
  pressure here is v542wave's specific doctrine — annulus beltbreak gunner + point-blank
  sentinel + barrier seal. **A field opponent may kill us a different way.** What generalises is
  the *shape* of the failures (unguarded rebuild, zero belt coverage, unreachable core-killer),
  not the specific opponent tactic.
* **n = 15 distinct games, not 30** (§0.4). All pooled shares above carry a 15-game denominator.
  Seat A only.
* **The harvester finding rests on 3 games** (icefloe, midgard, auroraveil) — the other 12 either
  built no harvesters or lost none. The *mechanism* is unambiguous within those 3; the *rate* is
  not estimable from 3 clusters.
* **Role attribution is heuristic** (§2.1) — spawn order into lowest-free-role, exact for the
  opening four bodies, approximate for replacements.
* **Coverage geometry ignores obstacles for gunners**, so ray coverage is an upper bound; it
  reads 0/42 anyway. The "any-facing" column is the rotate-if-you-could ceiling, not achieved
  coverage.
* **Local replays carry no bot stdout** (`Traceback`, `GameError`, `Exception` all occur 0 times
  in the bytes), so exception deaths are inferred from *removal with no damage event in the death
  round*, not read directly. That channel reads **0 for our team** across all 15 games, and reads
  **49 for theirs** (enemy launcher/barrier self-destroys) — so the channel is live and capable of
  firing, which is what makes our zero meaningful.
