# REPLAY STUDY: kladde chatte tville (och oss) v119 — 65 decoded games (2026-08-17)

## PROVENANCE

* **Agent:** fresh-context move-mining study agent (opus), no inherited session
  context. Commissioned by the research lane off the `tools/move_miner.py`
  trigger (kladde v119 scored 72.0, top of board, 65 of 65 modern games
  unstudied). Re-aimed mid-task by the commissioning lane to **lead with a
  plank-counter analysis** (four planks named below); the original brief was
  additive and is fully delivered.
* **Date of analysis:** 2026-08-17 (report written the same day; the ground's
  own clock is quoted inline everywhere it matters).
* **Inputs read:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md`,
  `docs/research/REPLAY-STUDY-0033-2026-08-16.md`,
  `docs/research/corpus-howto.md`, `tools/replay_schema.md`, `CLAUDE.md`,
  `tools/replay_census.py`, `tools/corpus/replay_events.py`,
  `corpus/join.tsv`, `corpus/ladder_games.tsv`, `corpus/events.tsv`,
  `corpus/league_matches.tsv`,
  `docs/research/ECO-STUDY-fast-connected-harvesters-2026-08-17.md`,
  `bots/_v468kladturbo/{main,eco,raid}.py` (incumbent GREP only — **no bot was
  edited, no arena run, no match fired, no submission touched**).
* **Decoder:** a round-by-round world walker built on `replay_census.py`'s
  primitives (`fields` / `read_pos` / `parse_entity`) — **no new byte-level
  decoding**. It replays every `placeEntity` / `moveBuilderBot` /
  `removeEntity` / `distributeResources` / `updateHp` / `updatePlayers` /
  `fireTurret` / `builderAttack` / `builderHeal` / `builderBuild` /
  `coreConvertAmmo` update and resolves every fire and attack target against
  **round-START occupancy** (the FireTurret ordering trap,
  `tools/replay_schema.md`), with unit-priority on turret fire and
  building-only on builder attacks (the damage-target law). Rotation re-emits
  are guarded (a build is the FIRST `placeEntity` carrying an id).
* **Decoder validation (the schema doc's end-to-end check):**
  `core_deliveries × 10 == Player.titaniumCollected` on **10 of 10 team-side
  pairs across 10 replays, 0 mismatches** — this validates map geometry, core
  footprint, and update handling in one number.
* **No reliance on our own `print()` output** anywhere. Every claim below is an
  engine-side fact (entity events, positions, fire events, HP, player state).

### Corpus queries actually run

```
awk on corpus/join.tsv                      -> the 65 files (opp ~ /kladde/ && oppver==119)
awk on corpus/join.tsv                      -> the 458-file same-era control (ourver in 152/155/157, opp != kladde)
awk on corpus/join.tsv                      -> the 60-file earlier-kladde pool (oppver 75..97)
join corpus/events.tsv x corpus/join.tsv    -> BUILD/DEATH per team per kind (first cut, 33 opponents)
corpus/ladder_games.tsv                     -> rated status, match ids, date range, record
corpus/league_matches.tsv                   -> kladde's version timeline (v119 first seen, still current)
scratchpad passes 1-9 over replay_archive/  -> everything measured below
```

## GROUND

**65 archived RATED LADDER games vs `kladde chatte tville (och oss)` v119**,
13 matches, **2026-08-15T22:32:59Z → 2026-08-17T06:52:59Z**, our versions
**v152 (40 games), v155 (20), v157 (5)**. All 13 match ids reconcile against
`corpus/ladder_games.tsv` (13/13). **Our record 31–34 (47.7%).** 61 of 65 end
`core_destroyed` (30 our core dies, 31 theirs); 4 reach r1000, all on
`titanium_collected`, **all four are losses**. 20,412 rounds total, mean 314,
median 258. v119 first appears in the league tape **2026-08-15T07:52:59Z** and
is still their current version at **2026-08-17T07:32:59Z**.

**THE CONTROL SET USED THROUGHOUT: 458 archived rated games from the SAME our-
versions (152/155/157) against every other opponent, 121,393 rounds.** This
holds OUR bot fixed and varies the opponent, which is the only way to attribute
a behaviour to *them* rather than to *us*. Where a number below has a "control",
this is it unless another is named.

⚠ **CLUSTERING.** 65 games = 13 matches; five games share a match, an opponent
and one ladder slice. Per `CLAUDE.md`, rated pooled DEFF = 1.529 (within-opponent
1.366), so effective n for any *share* here is ~43, not 65. **No confidence
intervals are attached anywhere in this report; everything is DESCRIPTIVE.** Any
bar built on these numbers must re-derive its own interval with the correction.
Event counts (thousands of fire/heal/attack events) are quoted as raw totals
with their denominators, not as estimates.

---

# PART A — DOES v119 COUNTER A PLANK WE ALREADY HOLD?

Verdicts for the four planks named by the commissioning lane.

## P1 — FORWARD ECONOMY-SHREDDER GUNNER in `20 ≤ d² < 100` of THEIR core

### `NO COUNTER OBSERVED` on the target geometry (MEASURED). `PLAUSIBLE COUNTER` on the platform's survival (EYEBALL-grade, n=12).

**Their belt sits IN the annulus, more than the field's does.**

| conveyor BUILD tiles, by d² from the builder's OWN core | inner `<20` | **annulus `20–100`** | outer `≥100` | median d² |
|---|---:|---:|---:|---:|
| **kladde v119** (n = 3,142 builds, 65 games) | 35.7% | **48.9%** (1,536) | 15.4% | 36 |
| same-era field control (n = 15,436, 458 games) | 48.3% | **35.8%** (5,526) | 15.9% | 25 |
| us, vs kladde (n = 3,629) | 39.6% | 43.1% | 17.3% | 29 |

**kladde's belt is 13.1 pp MORE exposed to the shredder annulus than the
field's.** Standing target density inside their annulus, measured live:
**17.5 conveyor tiles at r100** (n = 65 games), **26.0 at r200** (n = 41 games
still running), **29.8 at r300** (n = 23).

**And the belt is currently unmolested.** Their conveyors die **131 of 3,142
built (4.2%)** over 65 games — **only 23 of those to turret fire**. Ours die
**892 of 3,629 (24.6%)**. A shredder would be operating on virgin ground.

**The residual risk is the platform, not the targets.** 23.9% of their 156,780
turret-rounds sit inside the annulus of their own core, and **53.6% inside
`d² < 20`** — a sentinel at `d² < 20` with range r²=32 covers most of the inner
annulus. Direct evidence, our own forward gunners at `d² ≤ 100` of their core:

| our forward GUNNERS | n | died% | median life | shots/turret |
|---|---:|---:|---:|---:|
| vs kladde v119, built r0-60 | **5** | 100.0 | 16 | 24.40 |
| vs kladde v119, built r61-150 | **6** | 66.7 | 38.5 | 16.50 |
| control (field), built r0-60 | 21 | 57.1 | 50 | 21.71 |
| control (field), built r61-150 | 33 | 33.3 | 94 | 22.33 |

⚠ **n = 12 across 65 games. This is EYEBALL-grade and must not be quoted as a
rate.** What it shows directionally is worth the sentence: **life roughly halves
but shots-per-gunner barely moves** (24.4 / 16.5 vs 21.7 / 22.3). A gunner
reloads every round, so it converts a short life into shots; a sentinel
(reload 2) does not — see P2/P4, where our forward sentinel's output collapses
4.3x on the same ground.

⇒ **The plank's premise survives contact.** The counter to plan against is not
geometry, it is that a planted gunner inside their home-battery envelope has
roughly half the life it has against the field. Placement toward the OUTER half
of the annulus (`d² 50–100`, outside a home sentinel's r²=32 from `d² < 20`)
is the obvious first iteration and is **not measured here** — our n at that band
is 5.

## P2 — EARLY COMMITTED OPENING (forward turret up early, prereqs waived in r0-60)

### `MEASURED COUNTER` — but it is a counter to the OBJECT, not to the TIMING.

**Timing is NOT punished.** Their first turret rounds, 65 games:

| first turret | median | q25 | min | share by r30 |
|---|---:|---:|---:|---:|
| kladde v119 sentinel | 31 | 16 | 9 | 44.6% |
| kladde v119 gunner | 58 | 31 | 7 | 24.1% |
| control (field) sentinel | 38 | — | — | 42.1% |
| control (field) gunner | 29 | — | — | 54.4% |

kladde is marginally **earlier** than the field on sentinels and clearly
**later** on gunners. **A forward turret standing before ~r16 meets no kladde
turret in ~75% of games.**

**But r0-60 they are already a pure base-defence shooter.** Of their **576
turret shots in r0-60, TWO hit our core (0.3%)** — 282 at our sentinels, 110 at
our barriers, 79 at our harvesters, 64 at our conveyors, 32 at our builder bots,
7 at our gunners. In the *same* band we fire **317 of our 366 shots (86.6%) at
their core**.

**And the thing the early commitment builds is destroyed.** Our sentinels
planted at `d² ≤ 100` of their core:

| our forward SENTINELS, built r0-60 | n | died% | median life | shots/turret |
|---|---:|---:|---:|---:|
| **vs kladde v119** | **83** | **98.8** | **8** | **5.19** |
| control (field) | 430 | 59.5 | 45 | 22.25 |

⇒ An early forward sentinel returns **5.19 shots (93 dmg)** against kladde and
**22.25 shots (400 dmg)** against the field, for the same scaled price and the
same our-version. **The early-commitment plank is not counter-timed; its payload
is counter-killed.** If the plank's forward turret is a GUNNER rather than a
sentinel, P1's table applies instead and the collapse is much smaller.

## P3 — ECONOMY OPENING (harvesters + belt, gating when the raid may start)

### `NO COUNTER OBSERVED` to the opening's SPEED (MEASURED). A separate MEASURED sustained attrition that is not an opening counter.

**Speed: essentially tied.** First harvester median **r8 (us) vs r9 (them)**;
first conveyor **r10 (us) vs r1 (them)**; mean live harvester stock **5.18 vs
5.85**; mean live conveyor stock **37.39 vs 41.14**; deliveries **301.2 vs
357.7 stacks/game**. Their r0-60 pressure on our economy is real but small:
**151 builder attacks on our harvesters + 103 on our conveyors + 79 turret shots
at harvesters + 64 at conveyors = 397 events over 65 games (6.1/game)**, against
our **787 conveyor attacks and 0 harvester attacks** in the same band.

**The attrition is a MID-GAME fact, not an opening one.** Over the whole game
they put **1,325 builder attacks + 895 turret shots** into our harvesters and
kill **370 of our 724 (51.1%)**; they lose **1 of 448 (0.2%)**.
Control (field, same our-versions): our harvesters die **534 of 2,750 (19.4%)**,
the field's **18 of 2,371 (0.8%)**. **kladde is 2.6x the field at killing our
harvesters — and the field is 4x kladde at losing its own.**

⇒ The economy plank's *clock* is not counter-attacked. Its *stock* is, from
about r60 onward, and that pressure is what P3's raid-gating actually pays for.

## P4 — BUILDER-BODY RAID that walks to their core and builds turrets adjacent

### `MEASURED COUNTER`, and it is the sharpest number in the study.

**Arrival is NOT denied.** **401 of our builder bodies reached `d² ≤ 13` of
their core** across 65 games (6.2/game), spending **26,641 body-rounds** inside
that ring (410/game). Theirs into our ring: **73 bodies, 2,981 body-rounds**.
We get there, 5.5x more often than they do.

**What the raid BUILDS is shot at once.** Our sentinels planted at `d² ≤ 8` of
their core, n = 473:

| | n | died% | median life | shots/turret | ever hit | median rounds build→FIRST incoming hit | hit within 3 rounds |
|---|---:|---:|---:|---:|---:|---:|---:|
| **vs kladde v119** | **473** | **93.2** | **6** | 4.41 | **448 (94.7%)** | **1** | **85.3%** |
| control (field) | 529 | — | **18** | — | 292 (55.2%) | 2 | 68.8% |

⭐ **THE CONTROL RUNS THE OTHER WAY AND IT IS NOT SUBTLE: against the same-era
field, 237 of 529 (44.8%) of our siege plants are NEVER SHOT AT ONCE. Against
kladde v119, 448 of 473 (94.7%) are shot, at a median of ONE ROUND after the
build.** That is a standing battery already trained on the plant tile, not a
reaction.

**The mechanism, measured:** **53.6% of their 156,780 turret-rounds sit inside
`d² < 20` of their own core** — 84,034 turret-rounds of point defence — against
our 35.5% of 17,953. Their sentinels are sited at median **d² = 41 from their
OWN core** and d² = 145 from ours; ours at **d² = 386 from our own core and
d² = 13 from theirs**. **We park our siege ring inside their home battery.**

**The body itself is shot too:** **654 of their turret shots hit our builder
bots within `d² ≤ 8` of their own core** (10.1/game), 454 of them within
`d² ≤ 2`. Our builder bots die **7.18/game (2.29 per 100 rounds)**; control
**1.21/game (0.45 per 100 rounds)** — **5.1x**.

**The mirror image, same 65 games:** their forward sentinels at `d² ≤ 100` of
OUR core, built r0-60: **n = 44, 11.4% died, median life 121.5 rounds, 21.68
shots each.** Ours in the mirror position: **98.8% died, life 8, 5.19 shots.**

⇒ **The raid plank's arrival step works and its build step does not.** The
iteration this feeds is not "get there faster"; it is "what can a body build at
`d² ≤ 8` of a defended core that survives one round" — a barrier (3 Ti, 30 HP)
and a gunner (reload 1) both convert a one-round life better than a sentinel
(reload 2, 30 Ti base, 5.19 shots).

### Summary table

| plank | verdict | the number |
|---|---|---|
| P1 shredder gunner in `20≤d²<100` | **NO COUNTER (geometry)** / PLAUSIBLE (survival, n=12) | 48.9% of their 3,142 conveyor builds are in the annulus vs the field's 35.8%; their belt loses 131 of 3,142 (23 to fire) |
| P2 early committed opening | **MEASURED COUNTER** to the payload, not the clock | forward sentinel r0-60: 98.8% died / life 8 / 5.19 shots vs control 59.5% / 45 / 22.25 |
| P3 economy opening | **NO COUNTER** to the clock; measured mid-game attrition | first harvester r8 vs r9; harvesters die 370/724 (51.1%) vs control 534/2,750 (19.4%) |
| P4 builder-body raid | **MEASURED COUNTER** | 401 bodies arrive; 94.7% of 473 plants are hit at a median of 1 round; control 44.8% never hit at all |

---

# PART B — THE PIECES

Small, single-behaviour findings. Each is labelled MEASURED or EYEBALL, carries
its denominator, carries a control that must run the other way, and is sketched
against `R1000_IS_DEFEAT` / kill-before-r300.

## Piece 1 — ⭐ HEALING A 30–40 HP BUILDING UNDER TURRET FIRE BUYS NOTHING, AND IT IS ~30% OF OUR BUILDER ACTION BUDGET (MEASURED)

**CLAIM (one behaviour):** our builders heal small buildings that are under
turret fire; the heal does not change whether they die.

**THE ARITHMETIC (engine rules, not inference):** a heal is **+4 HP for one
builder action**. A gunner does **7 dmg on reload 1 = 7/round**; a sentinel does
**18 dmg on reload 2 = 9/round**. **One builder cannot hold any 30–40 HP
building against one turret, and two cannot hold it against a sentinel.**

**THE OUTCOME, our own units, 65 games — the discriminating table.** Among
entities that took **≥1 enemy TURRET hit**, bucketed by how many heals they
received:

| our entity | heal bucket | n | died% | median life | turret hits/entity |
|---|---|---:|---:|---:|---:|
| sentinel | 0 heals | 230 | **95.7** | **7** | 3.38 |
| sentinel | 3+ heals | 310 | **97.4** | **7** | 6.13 |
| harvester | 0 heals | 183 | 98.9 | 21 | 2.11 |
| harvester | 3+ heals | 93 | 98.9 | 8 | 4.43 |
| barrier | 0 heals | 122 | 99.2 | 12.5 | 2.36 |
| barrier | 3+ heals | 380 | 96.6 | 5 | 3.90 |
| **core (CONTROL)** | **3+ heals** | **29** | **62.1** | **279** | **35.0** |
| **their core (CONTROL)** | **3+ heals** | **62** | **45.2** | **265.5** | **51.26** |

⭐ **THE CONTROL RUNS THE OTHER WAY INSIDE THE SAME INSTRUMENT AND THE SAME
GAMES.** On a 500-HP core, heals demonstrably work: their core absorbs 51.26
turret hits, is healed, and survives 54.8% of the time over a median 265.5
rounds; heal HP replaces **70.9%** of the damage taken (41,632 healed / 58,716
dealt). On our 40-HP sentinels, heal HP replaces **28.0%** (10,640 / 37,974) and
the death rate is **97.4% healed vs 95.7% unhealed**. The instrument is not
saying "healing is bad"; it is saying **healing is HP-pool-dependent and we apply
it where the pool is too small.**

**THE VOLUME.** Heals landing on our own barriers / sentinels / harvesters:
**5,882 builder actions over 65 games = 90.5/game**, of which **4,677 (71.9/game)
went into an entity destroyed within 10 rounds**. Our total builder actions vs
kladde run ~305/game (153.5 heals + 45.7 attacks + 106.0 builds), so this is
**29.7% of our builder action budget, and 23.6% of it demonstrably bought
nothing.** Their comparable waste: **369 of 12,530 heals (2.9%)** died within 10
rounds; they spend **84.9% of their heal budget on their CORE** (10,408 of 12,259)
against our 21% (2,121 of 9,976).

**ANCHORS (file + round):**
* `acd6eb41-ccda-4c47-83a2-e60548e7b03d_game_3.replay26` (antler, ourver 152,
  r1000 loss): heals at **r19, r20, r21, r22** on one sentinel — **it died at
  r24**. 676 heals in this game went into entities dead within 10 rounds.
* `76966e35-f0f0-417d-9dbb-786ae244759f_game_1.replay26` (icefloe, ourver 152,
  746 turns, loss): heals at **r75, r76, r77, r78** on one sentinel — **died
  r80**. 386 such heals in this game.
* `b7e0bc88-117c-4c4c-b903-46b421c4ee7f_game_3.replay26` (drumlin, loss): heals
  at **r19, r20, r21** on a sentinel that died at **r21**; 284 in the game.
* `f6dd445c-fde3-4639-b7bd-e6e9553f793b_game_5.replay26` (glacierkeep, a WIN):
  heals **r170–r174** on a sentinel that died **r175**; 210 in the game — the
  behaviour is not confined to losses.

**GREP AGAINST THE INCUMBENT `bots/_v468kladturbo` (required before this becomes
a row):**
* `eco.py:468 _heal_adjacent` heals **any** damaged adjacent friendly building
  with **no enemy-turret-coverage gate**. Its own docstring states the
  justification: *"1 Ti for +4 HP against an enemy peck's 2 Ti for 2 dmg --
  eight to one on titanium."* **That is true against a BUILDER PECK (2 dmg/round)
  and false against a turret (7–9 dmg/round). The guard is specified against the
  wrong attacker.**
* `raid.py:325` ("HOLD THE COLLAR") repeats the same reasoning verbatim at the
  siege ring: *"a raider parked beside its own barriers out-repairs a pecker two
  to one on HP"* — this is the code path that produces the barrier and sentinel
  heals counted above, and the collar is exactly where kladde's home battery
  fires.
* Call sites: `main.py:601` (`_home_defend`), `main.py:544 / 603 / 806`
  (`_heal_core` — the productive one).
* **The Eir-6d `_ray_covers` / `_live_gun_covers` heal guard (built
  2026-08-07, `docs/coordination.md`) is NOT in the incumbent:** grep for
  `_ray_covers|_live_gun_covers` in `bots/_v468kladturbo/` returns **0 hits**.

**AGAINST OUR DOCTRINE:** this is a **pure reallocation with no new mechanism** —
~72 builder-actions/game freed into raid steps, plants, or belt. It has no
`titanium_collected` channel at all, so it is on-currency. It also serves P4
directly: the collar heals are spent at the exact spot where the plant dies.

⚠ **SCOPE / adjacency:** the CONVEYOR subset of this behaviour (1,444 heals,
48.6% dead within 10 rounds) overlaps queued **#73 (belt-cut repair)** and
**#88 (belt-repair attrition memory)**. The barrier / sentinel / harvester
subset (5,882 heals) is not covered by any row on the exclusion list.

⚠ **SELECTION CAVEAT, stated because it cuts against the claim:** entities get
healed *because* they are being hit, so the 3+ heal bucket is selected for taking
more fire (6.13 vs 3.38 turret hits on sentinels). The heals plainly absorb
*some* damage — the 3+ bucket survives ~1.8 extra hits at the same median life.
**What is not supported by anything here is that they change the outcome:
97.4% vs 95.7%.**

## Piece 2 — THEY SHOOT BUILDER BOTS ON PURPOSE, WITH SENTINELS, ON BARE TILES (MEASURED)

**CLAIM:** kladde v119's turret target ladder has a **builder-bot rung**; ours
effectively does not.

Turret fire hits the **unit** on a tile in preference to the building, so a hit
on a builder standing over a building is ambiguous. **The unambiguous cell is a
SENTINEL firing at a tile that holds a builder bot and NO building** — a
sentinel's line shot ignores obstacles, so it could have taken anything further
down the line and chose the bot.

| sentinel shots landing on an enemy builder bot, **bare tile** | total | per game |
|---|---:|---:|
| **kladde v119** (65 games) | **443** | **6.82** |
| us, vs kladde (65 games) | 12 | 0.18 |
| control: field opponents (458 games) | 264 | 0.58 |
| control: us, vs the field (458 games) | 503 | 1.10 |

**11.8x the field.** All builder-bot hits (both turret types, bare and
over-building): kladde **1,351 (20.8/game)** vs our **55 (0.85/game)**; field
control **1,968 (4.30/game)** vs our **2,219 (4.84/game)**.

**PAYOFF, and the control runs the other way on both sides:** our builder bots
die **467 in 65 games (7.18/game, 2.29/100 rounds)**; **329 of the 467 are
directly attributed to a fire event on the tile in the death round**. Field
control: **552 in 458 games (1.21/game, 0.45/100 rounds)**. Theirs die **10 in
65 games (0.049/100 rounds)** while the field's die **756 in 458 (0.62/100
rounds)** — **so our bot CAN and DOES kill enemy builders, 12.7x more often
against everyone else. The instrument registers the other verdict.**

**ANCHORS:** `25feefa5-7f51-4603-b2b1-c3f4a972a5ff_game_3.replay26` (frostgate,
loss) — 43 bare-tile bot shots, clustered at **r70, r71, r71, r72, r72, r73**
and again **r149–r157**. `acd6eb41-ccda-4c47-83a2-e60548e7b03d_game_3.replay26`
(antler, r1000 loss) — 38, at **r56, r70, r82–r91**, resuming **r388–r421**.
`76966e35-f0f0-417d-9dbb-786ae244759f_game_3.replay26` (yulerune, loss) — 33,
at **r84, r88, r92, r134–r148** (19 of our builder bots died in this game).

**AGAINST OUR DOCTRINE:** two-sided and both sides are on-currency.
*(a) Adopt:* a builder-bot rung above "empty ground" in our turret ladder kills
the raider that plants and the healer that repairs — this is the mechanism that
holds their core alive against us.
*(b) Defend:* our raider standing on a bare tile inside their home envelope is
the single cheapest thing they shoot; P4's plant sequence puts it there.

⚠ **Adjacency check:** the exclusion list carries #10 (blind their gun with
their own body), #93 (point-blank core-sniper gunner) and #30 (station scorer
blind to enemy sentinels). **A builder-bot rung in the turret target ladder is
not any of those** — it is a different target class from the 0033 study's
turret rung and belt rung.

## Piece 3 — OUR TARGET LADDERS HAVE NO HARVESTER RUNG AT ALL; THEIRS HAS TWO (MEASURED)

**CLAIM:** kladde spends 22.5% of its builder attacks and 13.8 turret shots per
game on harvesters. We spend **zero builder attacks** and **0.08 turret shots
per game**.

| harvester attacks, 65 games | builder attacks | turret shots | their/our harvester deaths |
|---|---:|---:|---:|
| **kladde v119 → our harvesters** | **1,325** (22.5% of their 5,883 builder attacks) | **895** (13.77/game) | our harvesters die **370 of 724 (51.1%)** |
| us → their harvesters | **0** (of 2,970) | **5** (0.08/game) | their harvesters die **1 of 448 (0.2%)** |

**CONTROL that runs the other way (458 field games, same our-versions):** we do
put **147 turret shots (0.32/game)** into field harvesters and the field loses
**18 of 2,371 (0.8%)**; field opponents put **2,682 builder attacks (5.86/game)**
into ours. **So the 0-of-2,970 builder-attack figure is a property of our code,
not of the decoder** — and it is the same fact the 0033 study's Piece-2
resolution found: `_salt_turn` is hardcoded to `(CONVEYOR, SPLITTER)`.

**THE TRADE, priced:** a harvester is **30 HP**. Two sentinel shots (36 dmg) kill
it for **20 ammo = 20 Ti**. It produces one 10-Ti stack every 4 rounds = 2.5
Ti/round. **Payback in 8 rounds.** Their builder-attack version is a *bad* trade
by comparison — 1,325 attacks × 2 Ti = 2,650 Ti spent to kill 46 harvesters by
melee — but it costs them almost nothing they need and it forces our heals
(Piece 1).

**ANCHORS:** `42e6b05a-e8b4-4b88-bb02-a45bd1623f86_game_2.replay26` (midgard,
loss) — 97 builder attacks on our harvesters. `f6dd445c-...c_game_5.replay26`
(glacierkeep, WIN) — 74. `f6dd445c-...c_game_4.replay26` (drumlin, WIN) — 67.
`5c832e98-189a-4a55-9167-c1c280155a8d_game_1.replay26` (valkyrie, loss) — 64.

**AGAINST OUR DOCTRINE — and this is where it needs care.** Killing harvesters
runs through `titanium_collected`, which is **off-currency**. It is admissible
only through its **ammo** channel, and that channel is real and measurable here:
they convert **1,359 Ti/game to ammunition** (2.09x our 651) off **357.7
delivered stacks/game**, i.e. ~38% of delivered titanium becomes the ammunition
that produces the 3,146 shots that kill our sentinels and the 1,351 that kill our
builders. **A harvester rung is an ammo-denial plank wearing an economy costume.**
It should be registered as such or not at all.

⚠ **Adjacency:** #7/#49 (ore-barrier denial) deny the *tile before the build*;
this is a rung in the *existing* attack/fire ladder against a *built* harvester.
Different mechanism, same target class.

## Piece 4 — INDEPENDENT CONFIRMATION OF 0033 PIECE 3 (COUNTER-BATTERY), AT A SHARPER RATIO (MEASURED — NOT A NEW PIECE)

Stated as a confirmation, per the brief's instruction, because it dominates the
game and a reader must not think it is missing.

| 65 games | shots at the ENEMY's gunners+sentinels | our/their turret deaths |
|---|---:|---:|
| kladde v119 → our turrets | **3,221** (49.6/game; 3,146 at sentinels + 75 at gunners) | our sentinels die **674 of 761 (88.6%)**, gunners **23 of 39** |
| us → their turrets | **329** (5.06/game; 280 + 49) | their sentinels die **35 of 527 (6.6%)**, gunners **7 of 198 (3.5%)** |

**9.8:1** overall, **11.2:1** on sentinels alone.
94.0% of our sentinel shots (3,262 of 3,470) go at their core;
**19.2% of theirs (1,327 of 6,915) do.** Their ladder spreads across our
sentinels (22.25/game), barriers (19.28), builder bots (12.55), harvesters
(10.15), conveyors (9.75).

**CONSEQUENCE, and it is the whole game:** mean live turret stock is **7.68 for
them and 0.88 for us** (156,780 vs 17,953 turret-rounds over 20,412 game-rounds)
— **even though we BUILD more sentinels than they do (11.71/game vs 8.11)**. We
buy the turrets; they keep them.

## Piece 5 — WE NEVER DEMOLISH ANYTHING; THEY BARELY DO; THE FIELD DOES (MEASURED, small)

Removals with no damage in the removal round (a `destroy()` or `self_destruct()`
signature): **US = 0 across all 523 games in both sets.** kladde v119 = 4
barriers. **Field control opponents = 160 conveyors, 107 gunners, 95 launchers,
92 barriers, 79 builder bots.** Destroying an own building **removes its cost-
scale contribution** (`CLAUDE.md`), so a spent forward turret is a permanent
price on every future build. Our live-stock scale works out to roughly **+182%
(scale ≈ 2.8)** against their **+323% (scale ≈ 4.2)**, computed from mean live
stock × the per-entity contributions — so they pay ~50% more per build and still
field 8.7x the turrets. **Flagged as context, not proposed as a plank:** the
0033 study already noted their belt demolition, and our own scale is the *low*
side of this comparison.

---

# PART C — MECHANISMS CHASED AND KILLED (do not re-derive)

**C1. "STAND THE SIEGE SENTINEL OFF FURTHER" — DEAD.** Our sentinel death rate
banded by build-distance to their core is **flat**: `d²≤8` 93.2% (n=473),
`9–13` 88.3% (n=60), `14–20` 91.7% (n=72), `21–32` 94.7% (n=95). **The control
runs the other way and proves the band variable is measurable:** THEIR sentinels
in the same bands vs OUR core read 4.5% / 23.5% / 38.1% / 22.7%. Distance is a
live variable; it simply does not move for us. A standoff-placement plank aimed
at kladde is dead.

**C2. "ADOPT THEIR AMMO POLICY" — DEAD, AND BACKWARDS.** They convert **2.09x**
more titanium to ammunition than we do (1,359 vs 651 Ti/game) yet they are the
**starved** side: mean ammo balance while owning a turret **6.3 (them) vs 57.3
(us)**; share of sentinel-rounds unable to afford a sentinel shot **51.3%
(n=111,101 sentinel-rounds) vs our 4.2% (n=14,369)**; share of turret-rounds
below 4 ammo **33.6% vs 1.2%**. **Per turret-round WE fire 3x more often (0.219
vs 0.074).** Control that proves the dryness instrument moves: on the same-era
field it reads **21.3% dry for us and 44.9% for the field** — so it is not
pinned. **Their shot volume comes from turret STOCK, not from ammo policy.**
The residual live observation, not a plank: our mean 57.3 banked ammo against
kladde is ~5.7 unfired sentinel shots of idle capital, and it is idle because we
have no turrets to fire it, not because we are thrifty.

**C3. "HEALS ARE HOPELESS WHENEVER INCOMING DPS > 4/ROUND" — INSTRUMENT
DISCARDED, IT FAILED ITS OWN CONTROL.** I built a per-heal classifier that
measured incoming damage in a 5-round window around each heal and flagged
`DPS > 4` as hopeless. It returns **67.4% hopeless for our CORE heals** vs
**8.2% of the same heals landing on a core that died within 10 rounds** — i.e.
it calls the one heal class that demonstrably works (Piece 1's control table)
hopeless. **The criterion measures "is the target under fire", not "is this heal
futile", because it ignores the target's HP pool and the number of simultaneous
healers.** Discarded; the outcome-based measures in Piece 1 are used instead.
**Recorded so nobody rebuilds it.**

**C4. "THEY BEAT US ON THE SAMESTOP OPENING WE COPIED" — NOT SUPPORTED IN THIS
DIRECTION; see Part D.** They have not improved it and we have nearly caught up.

**C5. Two things checked and found ABSENT rather than adversarial:** kladde v119
builds **ZERO launchers** in 65 games (we build 66, 1.02/game) and **ZERO
splitters** — as do we. Neither side uses the splitter. No kidnap defence
exists on their side because no kidnap threat exists from theirs.

---

# PART D — THE LINEAGE QUESTION

**"Has the kladde lineage we borrowed from moved on?"**

**What we borrowed, precisely:** `bots/_v468kladturbo` = *samestop × turbo ×
bodyaware* — "Magnus's kladde piece on the v152 family"
(`docs/coordination.md`, 2026-08-16T17:11:39Z). **SAMESTOP** is the eco plank:
build, do not move, build the other adjacent tile from the same stop
(`doctrine.py:1833-1877`, `LOKI_SAMESTOP_ON`).

**THE ARCHIVE CAN ANSWER THIS, and the answer is: ON THE PLANK WE BORROWED,
NO — THEY HAVE NOT MOVED. ON EVERYTHING ELSE, YES, SUBSTANTIALLY.**

### D1 — The borrowed plank itself: unchanged, and we have NOT passed them on it

Consecutive builds by the same builder in r0-100, gap = 1 round **and** from the
same tile (the samestop signature — note **every** gap-1 pair in the sample was
same-tile, so the two definitions coincide on this data):

| | pairs (r0-100) | **samestop share** |
|---|---:|---:|
| **kladde, earlier versions v75–v97** (60 games) | 2,203 | **10.49%** |
| **kladde v119** (65 games) | 2,848 | **10.78%** |
| **us, in the earlier games** (our v72–v125) | 2,368 | **2.11%** |
| **us, in the v119 games** (our v152/155/157) | 3,283 | **9.44%** |

⇒ **kladde's samestop rate moved 10.49% → 10.78% — flat.** Ours moved 2.11% →
9.44%, which is the shipped `#50`/SAMESTOP plank firing, exactly as the eco
study reported. ⚠ **A CORRECTION WORTH RELAYING:** the eco study records *"11.5%
against kladde's 9.2%"*. On **this** cut — the same 65 games, both sides, same
definition, r0-100 — the ordering is **kladde 10.78% ahead of our 9.44%**. The
two cuts differ (its populations are per-builder rates over its own rated
window), so this is not a contradiction of its instrument; it does mean the
claim *"we have moved to the top of the field on its own statistic"* **does not
hold head-to-head against the team the plank came from.** Both numbers are
MEASURED; they answer slightly different questions and the head-to-head one is
the one that answers *this* question.

### D2 — What v119 DID change (their side only, per 100 rounds, so game length cancels)

Earlier pool: kladde v75–v97, **60 archived games, 16,882 rounds** (our versions
72/102/104/125/152). Current: v119, **65 games, 20,412 rounds**.

| kladde's own behaviour | v75–v97 | **v119** | change |
|---|---:|---:|---|
| **barriers built /100r** | 0.27 | **1.85** | **+580%** |
| **barrier stock alive/round** | 0.23 | **3.00** | **+1200%** |
| sentinel stock alive/round | 2.89 | **5.44** | +88% |
| gunner stock alive/round | 2.38 | 2.24 | flat |
| **their sentinel deaths /100r** | 0.46 | **0.17** | −63% |
| **their gunner deaths /100r** | 0.35 | **0.034** | −90% |
| **their builder-bot deaths /100r** | 0.71 | **0.049** | −93% |
| **turret shots at OUR core /100r** | 19.4 | **6.9** | **−64%** |
| **turret shots at OUR turrets /100r** | 8.8 | **15.8** | **+80%** |
| turret shots at our builder bots /100r | 7.6 | 6.6 | −13% |
| ammo converted /100r | 422 | 433 | flat |
| core heals /100r | 47.4 | 51.0 | +8% |
| builder attacks on our harvesters /100r | 9.5 | 6.5 | −32% |

⚠ **CONFOUND, stated plainly:** our own bot changed across these eras too
(v72 → v152/155/157), so the *target-mix* rows are partly a function of what we
present. **The rows that are unambiguously their own decisions are the ones that
do not reference us: barriers built, barrier stock, sentinel stock, ammo
conversion, core heals.** Those say: **v119 added a barrier plank and doubled
its standing sentinel count.**

**THE ONE-LINE ANSWER:** *the kladde lineage has moved on, but not on the eco
plank we took from it. Their opening is the same; the v119 delta is DEFENSIVE
and TURRET-SIDE — a new barrier line, twice the standing sentinels, and a target
ladder that has rotated 64% of its fire off our core and onto our turrets. The
2026-08-16 study of them (had one existed) would have described a core-rush
shooter; v119 is a counter-battery base — its fire rate at our core is down 64%
and its fire rate at our turrets is up 80%.*

---

## APPENDIX — instruments, and what was done to try to break them

* **End-to-end geometry/update check:** `core_deliveries × 10 ==
  Player.titaniumCollected`, **10/10 replays, 0 mismatches**.
* **Fire attribution:** 0 unattributed fire events across all 523 games in both
  sets (`fire_unattrib = 0`) — every `FireTurret.from` resolved to a live turret
  of the firing team at round start.
* **Death attribution:** every death is classified `by_fire` / `by_batk` /
  `damaged_noattr` / `voluntary`. It produces **all four verdicts** on real
  data: e.g. our conveyors 559 by fire / 333 by melee; field opponents 160
  voluntary conveyor removals against **0 for us in 523 games** — a class the
  instrument only ever emits when it is really there.
* **A control was computed for every mechanism claim, and two of them ran the
  wrong way and killed the claim** (C1 standoff distance, C2 ammo policy). One
  instrument was **discarded for failing its own control** (C3).
* **Cross-instrument discrepancy found and resolved:** two of my passes
  disagreed by 312 on "conveyor heals". Cause: one pass attributes a heal by the
  **healer's** team, the other by the **target's**. Heals aimed at a tile
  carrying an ENEMY conveyor (our bot healing itself or a buddy standing there)
  land in different buckets. **Piece 1 uses the target-team-correct counts.**
  Verified by recomputing both ways on 20 files: inline and via-log counts agree
  exactly (506/381/447/296/420).
* **Not measured, and therefore not claimed:** whether a gunner planted in the
  OUTER half of the annulus (`d² 50–100` of their core) survives — our n at that
  band is 5. Whether their belt has redundant paths. Whether their barrier plank
  is the gunner plug of the 0033 study (only 19.4% of their 377 barriers are
  within `d² ≤ 13` of one of our turrets, against 66.3% of ours within `d² ≤ 13`
  of theirs — so it is **not** primarily a plug; what it is was not established).
