# REPLAY STUDY — farming_200s v19 (move-mining trigger fire, 2026-08-21)

**STATUS: COMPLETE.** Banked incrementally per the playbook's BANK-EARLY rule.
Every claim is labelled **MEASURED** (counted from decoded events), **EYEBALL**
(seen, not yet counted), **INFERENCE** (mechanism, reasoned not measured), or
**GREPPED** (read out of the incumbent tree at a cited file:line).

---

## EXECUTIVE SUMMARY — read this first

**WHAT THEY ARE.** farming_200s v19 is a **door-sentinel bot**, not a farming
bot. Across 60 archived rated games it builds **zero gunners and zero launchers**,
and **96 of 96 sentinels it builds are planted inside d²≤32 of OUR core** (median
d²=13, median round 32.5). It **never melees a core** (0 in 130 games across
v15/v18/v19). The plant is carried by a single builder that walks a straight
~1-tile/round run-in and is exposed for a **median 9 rounds** first. After the
plant, **625 of 625 of their barriers across 130 games ring OUR core's heal
seats** and none ring their own. They have **no home-defence trigger at all**
(54/60 games place nothing defensive after our units arrive at their core).

**WHY IT MATTERS.** **32 of 32 of our core deaths in those 60 games were preceded
by such a plant; 0 of 32 were not.** It is their only kill channel. **We kill
21.9% of them; 75 of 96 are still standing when the game ends**, and when we do
kill one they fail to replant **14 times in 21**.

**THE GAP.** The incumbent `bots/_v542wave` (live v177) **contains the exact
counter-verb, complete, and ships it switched off**: `_door_turret_turn`
(`main.py:1708`) is disabled by `FS_V515_DOOR_OFF = True` (`doctrine.py:3132`).
**The evidence that switched it off was measured entirely against our own bots**,
which the tree's own doctrine block states verbatim — and `CLAUDE.md` point 6
says that is a hypothesis, not a refutation. This is the **first live opponent
measured whose entire kill channel sits inside that verb's trigger band.**

**THE OTHER GAP.** We build ~4 launchers a game at **median r5**, sited **median
d²=128 from our own core** — forward with the raid — so **only 7 of 96 walkers
were ever inside pickup range and 0 of 96 plants were prevented by a throw.**
Our throwing machine runs at median round 131 against a median plant at r32.5.

**THE ASK.** Two amendments to existing `QUEUE.md` rows (#96; #17/#5/#38) and one
new candidate, all in §8 and §9. No new organiser question is needed.

**PROVENANCE.** Fresh move-mining replay-study agent (opus), commissioned
2026-08-21 by the research arm. Method:
`docs/research/PLAYBOOK-move-mining-2026-08-16.md`. Corpus discipline:
`docs/research/corpus-howto.md` (traps 1–8 respected; no hand-rolled decoder).

**GROUND.** farming_200s v19 — the trigger fired at 65 unstudied MODERN games of
65 (raw 65/65 on this version). Our modern-era game share vs them 50.9% (n=110).
Rating gap +0 at commission (them 1845, us 1826); a 5-0 pays +16.00. Their
current league version IS v19, confirmed 2026-08-21T12:41Z.

**INPUTS** (all pre-decoded corpus tables; **zero platform matches, zero replay
downloads** — every v19 replay that exists was already in `replay_archive/`):
`corpus/ladder_games.tsv`, `corpus/join.tsv`, `corpus/events.tsv`,
`corpus/builds.tsv`, `corpus/build_agg.tsv`, `corpus/econ.tsv`,
`corpus/throws.tsv`, `corpus/flow.tsv`, and the incumbent tree
`bots/_v542wave/` (read directly for every GREP claim).

**CORPUS FRESHNESS.** Newest row in `corpus/ladder_games.tsv` is
`2026-08-21T12:41:10.123Z`; wall clock at study start `2026-08-21T12:58:24Z`
(`date -u`, same shell) — the tape is **~17 minutes old**, one pairing cadence.
Not blind.

**POPULATION AND ITS HOLE, stated once and applying to every replay-derived
number below.** `ladder_games.tsv` records **65 rated games in 13 matches**
against farming_200s v19. **`replay_archive/` holds 60 of those 65** — the five
games of the `2026-08-20T18:32:59Z` match (a 3-2 for us) have no archived
replay. **So every ladder-metadata figure is over n=65 and every replay-derived
figure is over n=60, and they are labelled accordingly.** The missing match was
a WIN for us, so the replay set is very slightly biased against us (28/60 =
46.7% in replays vs 31/65 = 47.7% in metadata).

**CLUSTERING.** Every share below is a GAME share; games cluster in matches of 5
sharing opponent version and ladder slice. Confidence intervals use the rated
pooled **DEFF = 1.529** (`CLAUDE.md`). Per-MAP cuts use **DEFF ≈ 1.07** (match
cluster dies — 5 games of a match are 5 different maps; opponent cluster
survives), per the enumeration procedure in `CLAUDE.md`.

⛔ **ONE CORRECTION TO THE COMMISSION, made before anything is built on it.**
The brief says *"they went 3-2 and 2-3 and 2-3 against our v176/v177 line
today"*. The rated tape does not say that. Today's six farming_200s matches, read
off `corpus/ladder_games.tsv` (`created >= 2026-08-21`), are:

| created (Z) | our version | result |
|---|---|---|
| 02:32:59 | v172 | **4-1** |
| 04:32:59 | v173 | 2-3 |
| 06:32:59 | v174 | **3-2** |
| 07:52:59 | v174 | 1-4 |
| 10:12:59 | v176 | 1-4 |
| 11:12:59 | v176 | 2-3 |

**13-17 in games (43.3%), six matches, and NO v177 match against them exists
yet.** The brief's three-match summary is neither today's tape nor the v176-only
tape (v176 alone is 3-7). Nothing below rests on the brief's version of the day;
it rests on the table above.

---

## 0. HEADLINE — THEY CHANGED DOCTRINE AT v19 AND IT IS A SINGLE MOVE

**MEASURED.** Our record against farming_200s by their version
(`ladder_games.tsv`, all rated games, n=255 across 12 versions):

| their version | games | our game share | med turns | our kills | their kills |
|---|---|---|---|---|---|
| v7 | 40 | 75.0% | — | — | — |
| v9 | 25 | 36.0% | — | — | — |
| v11 | 20 | 35.0% | — | — | — |
| **v15** | **45** | **55.6%** | 175 | 25 | 20 |
| **v18** | **25** | **60.0%** | 298 | 13 | 10 |
| **v19** | **65** | **47.7%** (60 replays: 46.7%) | 186 | 26 | 32 |

**THE ONE MOVE.** Their turret doctrine, from `corpus/events.tsv` BUILD rows,
per game:

| their version | games | **gunners** | **sentinels** | **launchers** | harvesters | conveyors | builder bots | barriers |
|---|---|---|---|---|---|---|---|---|
| v15 | 45 | **0.00** | 1.62 | **0.00** | 2.84 | 9.20 | 6.89 | 4.38 |
| v18 | 25 | **7.32** | 0.28 | **0.00** | 4.00 | 14.16 | 7.44 | 4.56 |
| **v19** | **60** | **0.00** | **1.60** | **0.00** | 2.65 | 9.20 | 6.65 | 5.23 |

⇒ **v18 was a gunner bot. v19 reverted to v15's sentinel-only bot.** Zero
gunners in 60 of 60 v19 games; **zero launchers in 130 of 130 games across
v15+v18+v19.**

**CONTROL — the same counter run on OUR side must come out the other way, and
does.** In the same 60 v19 games we built **27 gunners** and **217 launchers**
(`build_agg.tsv`, an independently-written decoder, agrees digit-for-digit:
THEM gunner 0 / launcher 0, US gunner 27 / launcher 217). A zero here is a
finding, not `econ.tsv`'s dead-column class (corpus-howto traps 5, 6, 8).

**SECOND CONTROL, because a per-version zero could be a version-tag artefact:**
v18 — the same opponent, the same decoder, the same 25-game slice — returns
**183 gunners**. The counter can produce a non-zero on their side.

---

## 1. WHAT THEIR v19 ACTUALLY DOES — THE DOOR-SENTINEL BOT

### 1.1 Every sentinel they build is a plant NEXT TO OUR CORE (MEASURED)

From `corpus/builds.tsv` (per-build geometry), their 96 v19 sentinels:

| cut | v15 (73 sentinels) | **v19 (96 sentinels)** |
|---|---|---|
| forward-sited (`d²_enemy < d²_own`) | 91.8% | **95.8%** |
| median d² to **OUR** core | 13 (≈3.6 tiles) | **13 (≈3.6 tiles)** |
| median d² to **THEIR OWN** core | 153 | **333 (≈18.2 tiles)** |
| **within d² ≤ 32 of OUR core** | **73/73 = 100%** | **96/96 = 100%** |
| within d² ≤ 20 of OUR core | 89.0% | 84.4% |
| within d² ≤ 32 of THEIR OWN core | — | **9/96 = 9.4%** |
| median build round | r22 | **r32** |
| games with ≥1 such plant | — | **55/60 = 91.7%** |

**MEASURED, and it is the whole bot:** *every single sentinel farming_200s v19
builds is planted inside sentinel range of our core.* Their own base is
**turret-free in 60 of 60 games** — 9 of 96 sentinels sit within d²≤32 of their
own core, and those 9 are plants on maps where the two cores are close.

**MECHANISM (INFERENCE from the engine rules, not measured here):** a sentinel
is dmg 18, reload 2, range r²=32, and its line **ignores obstacles**. A 500 HP
core is 28 shots. Planted at r32 at d²=13, one sentinel with a fed magazine is a
complete core-kill engine and nothing we build in the way stops the line.

### 1.2 They never melee a core (MEASURED, 130/130 games)

`build_agg.tsv` metric `batk_core`: **THEM = 0 in v15 (45 games), v18 (25) and
v19 (60) — 130 of 130.** Their builder melee is real (`batk` 35.9/game in v19)
but it is spent on our conveyors, launchers and barriers, never on our core.
**CONTROL:** the same column on OUR side in the v15 era reads **63** — the
column is live and discriminates.

⇒ **Their ONLY core-kill channel is the forward sentinel.** Which the next
number closes:

### 1.3 32 of 32 of our core deaths were preceded by a plant. 0 of 32 were not. (MEASURED)

Over the 60 archived v19 games:

* our core died **32** times; **32/32** had a their-sentinel planted at d²≤32 of
  our core **before** the death. **0/32** without one.
* median lag **plant → our core death = 146 rounds** (q1 81, q3 252, min 45).
* games where they got **no** in-range plant: **5**, and we **won all 5** (5/5).
  Games where they did: 55, we won 23 (41.8%).
* in the 32 games we lost, **32/32** had a plant (100%); in the 28 we won,
  23/28 (82.1%).

⚠ **n=5 on the no-plant arm. This is a DIRECTION, not an established effect** —
5/5 with DEFF=1.529 has a lower bound well under 50%. What IS established at
n=60 is the necessity direction: **no plant has ever preceded one of our core
deaths in this matchup.**

### 1.4 AND WE ALMOST NEVER KILL IT (MEASURED — this is the exploitable gap)

`corpus/events.tsv` DEATH rows for their sentinels:

| | v15 (45 games) | **v19 (60 games)** |
|---|---|---|
| sentinels they built | 73 | **96** |
| **we killed** | 21 (28.8%) | **21 (21.9%)** |
| **survived to game end** | 52 | **75 (78.1%)** |
| median lifetime when killed | 32 rounds | **74 rounds** |
| **never replanted after we killed it** | 10/21 | **14/21 (66.7%)** |
| median replant latency when they did | 33 rounds | **34 rounds** |

**READ THAT TOGETHER WITH 1.3.** The single object that is necessary for every
core death we suffer in this matchup sits three tiles from our core for **74+
rounds** and we remove it in **fewer than one game in four** — and when we do
remove it, they **fail to replace it two thirds of the time**.

**DIRECTIONAL, NOT ESTABLISHED:** games where we killed ≥1 forward sentinel more
than 2 rounds before the end (n=15) we won **60.0%**; where we killed none
(n=45) we won **42.2%**. Difference **+17.8pp against a two-arm 95% half-width
of 36.1pp (DEFF=1.529)** — **does not clear**, and it carries an obvious
reverse-causality confound (killing it takes time; those games are 50 rounds
longer at the median). Quoted so the next leg knows the effect size to power
for, **not** as evidence.

**ARTEFACT CONTROL on the death counter:** of the 21 their-sentinel deaths, the
rounds-before-game-end distribution is `1, 3, 54, 72, 78, 88, 93, 103, 112, 135,
140, 150, 156, 160, 166, 174, 203, 221, 818, 830, 878` — only **1 of 21** is
within 2 rounds of the end, so these are real kills and not end-of-game removal
artefacts. The 15-vs-45 split above already excludes that one.

### 1.5 The race, and what actually flipped the cell (MEASURED)

Core-death rounds from `events.tsv`, all archived games:

| their version | our median kill | their median kill | **our timely-kill rate (≤r300, ALL games denom)** | theirs |
|---|---|---|---|---|
| v15 (n=45) | **r153** | r192 | **53.3%** | 31.1% |
| v18 (n=25) | r198 | r319 | 36.0% | 16.0% |
| **v19 (n=60)** | **r192** | **r178** | **31.7%** | **45.0%** |

**We used to be 39 rounds faster than them; we are now 14 rounds slower.** Both
halves moved: our median kill slid **r153 → r192** and theirs sharpened
**r192 → r178**.

⚠ **CONFOUND, named rather than waved at: our chassis changed too.** The v15
games are our v155-era line; the v19 games span our v162–v176. Within their v19
our per-chassis cells are n=5–20 and noisy (v168 n=20 55%, v176 n=10 30%,
v172 n=5 80%), so **this table cannot separate "their v19 got faster" from "our
v162–176 line got slower"**. The one thing it does establish is that in the
CURRENT cell they win the race, which is what a leg has to fix.

### 1.6 Economy: they are not actually a farming bot (MEASURED)

`econ.tsv` `ti_collected_end`, median per game: **THEM 315, US 405** in v19
(THEM 280 / US 440 in v15). They build **2.65 harvesters/game** to our 3.30 and
**9.2 conveyors** to our 20.9. Their ammunition conversion is **380 Ti/game
median** against our 311 — i.e. **more of their smaller income goes into the
magazine than ours does**, which is consistent with a one-sentinel bot that only
has to feed one gun. **The name is misleading; treat them as a rush bot.**

### 1.7 What they take off us (MEASURED, deaths per game, v19, n=60)

| | OURS | THEIRS |
|---|---|---|
| launcher | **2.35** (of 3.62 built = **65% killed**) | 0.00 |
| conveyor | 3.48 | 0.38 |
| builder bot | 0.78 | 0.90 |
| barrier | 0.02 | 1.32 |
| **sentinel** | **0.00 (of 103 built)** | 0.35 |
| harvester | 0.23 | 0.32 |

**MEASURED:** they kill **65% of our launchers** and **0 of our 103 sentinels**.
**CONTROL:** their sentinel deaths are 0.35/g, so the "our sentinel deaths" cell
is a live column reading a true zero, not a dead column.
**INFERENCE (mechanism, not measured):** our launcher is the piece that must
stand adjacent to enemy bodies to do its job (pickup is d²≤2), it has 30 HP
against a sentinel's 40, and their entire melee budget (`batk` 35.9/game) plus
one obstacle-ignoring sentinel line is pointed at exactly that band. **Our
kidnap engine is the thing they are actually killing.**

---

## 2. THE KIDNAP TREADMILL — WE ALREADY THROW THEM 28 TIMES A GAME AND IT KILLS 7

**MEASURED**, `corpus/throws.tsv`, their v19 (n=60 games):

| | count | per game |
|---|---|---|
| throws by us of **their** builders (EXILE) | 1,708 | **28.47** |
| of those, landed on a **map-border** tile | 161 | **9.4%** |
| victim fate `RETHROWN` (we threw the same bot again) | 1,547 | **90.6%** |
| victim fate `DIED` | **7** | **0.4%** |
| throws by us of **our own** builders (INSERT) | 273 | 4.55 |
| INSERTs that `reached` the target | 93/273 | 34.1% |
| INSERT median post-throw life | — | **6 rounds** (v15: 12) |
| INSERT `core_atk` sum | **0** | — |

**THIS IS A TREADMILL, MEASURED.** 90.6% of our exiles are re-throws of a bot we
already exiled: the throw does not kill, the bot walks back, we spend another
launcher turn. **28.5 throws a game convert into 7 deaths across 60 games.**
Meanwhile the border-landing rate — the crash-induction dose — is **9.4%**, down
from 13.8% against their v15.

**AND THE THING THE TREADMILL IS NOT DOING:** §1.1 says their offense is
delivered by a builder that walks to d²≈13 of our core and plants. We throw
their builders 28 times a game and their plant still lands in **55 of 60 games**
at a median of **r32**. **Volume is not the constraint; selection is.** (Whether
any of those 1,708 throws ever hit the walker specifically is the one question
this section cannot answer from `throws.tsv` alone — it is measured in §4.)

---

## 3. CPU — THEY RUN AT 7x OUR BUDGET AND THE CEILING IS REAL

**MEASURED**, `econ.tsv` `cpu_max_us` / `tled`, per round-band:

| their version | band | games | **TLE events** | games with ≥1 TLE | **their cpu_max median (µs)** |
|---|---|---|---|---|---|
| v15 | r0-150 | 45 | 13 | 1 | 6,665 |
| v18 | r0-150 | 25 | 4 | 3 | 8,699 |
| **v19** | **r0-150** | **60** | **152** | **6** | **7,099** |
| v19 | r150-200 | 40 | 51 | 2 | 1,498 |
| v19 | r200-300 | 28 | 66 | 1 | 1,822 |

**OUR cpu_max across the same 60 games peaks at 2,743 µs with ZERO TLE events.**
Theirs peaks at **10,511 µs** — the budget is 10,000 µs plus a rolling 5% buffer,
so **they are hitting the ceiling exactly.**

⛔ **DO NOT READ THIS AS BROAD CPU PRESSURE — I nearly did.** The 269 v19 TLEs
are concentrated in **6 of 60 games** (one game, `20b341f9…` on **antler**,
contributes **214**); **median TLE per game is 0** and 54/60 games have none.
Correlation between our total builds and their TLE count is **r = −0.125
(n=60)** — i.e. **nothing**, and in the wrong direction for a "flood their vision"
theory. Correlation with game length is **r = +0.019**.

**WHAT IS ESTABLISHED:** in the **median** v19 game their busiest unit-turn in
r0-150 costs **7,099 µs of a 10,000 µs budget — 71% — against our 900 µs.**
They have ~2.9 ms of headroom in the median game and zero in 6 of 60.
**WHAT IS NOT ESTABLISHED:** any lever of ours that moves it. The 12 blow-up
games across all versions cluster on **glacierkeep (3), valkyrie (5), antler
(1)** — an EYEBALL pattern at n=12, offered as a place to look, not a finding.
**And the sign is not in our favour on the tape we have:** of the 6 v19 TLE
games we won 2 and lost 4.

---

## 4. PER-MAP (MEASURED, small n — DEFF ≈ 1.07 applies, match cluster dies)

Their v19, maps with n≥3 archived games:

| map | n | our wins | share | their 1st sentinel (med round) | their cpu_max | med turns |
|---|---|---|---|---|---|---|
| antler | 4 | 0 | 0.0% | **r7** | 10,505 | 248 |
| midgard | 4 | 0 | 0.0% | r45 | 7,782 | 117 |
| ragnarok | 3 | 0 | 0.0% | r51 | 6,167 | 98 |
| glacierkeep | 4 | 1 | 25.0% | r36 | **10,511** | 315 |
| fjordgate | 3 | 2 | 66.7% | **r2** | 6,281 | 181 |
| drumlin | 4 | 3 | 75.0% | r22 | 7,084 | 175 |
| valkyrie | 5 | 4 | 80.0% | r28 | 10,508 | 307 |
| auroraveil | 6 | 5 | 83.3% | r20 | 10,077 | 174 |
| icefloe | 7 | 6 | 85.7% | r29 | 8,481 | 198 |

**Every cell is n≤7. Nothing here is significant on its own.** Pooled across ALL
their versions (n≥8 per map) the two cells that stand out are **royale 0/9** and
**nordkap 4/14 (28.6%)** against **yulerune 10/11** and **valkyrie 8/9**.
**EYEBALL, flagged for a pooled cut later, not a finding.** Note the plant round
does **not** order the win column (fjordgate r2 → we win; midgard r45 → we lose),
so "they plant early therefore we lose" is **not** what the map table shows.

---

## 5. THE INCUMBENT — WHAT `bots/_v542wave` (live v177) ACTUALLY DOES ABOUT THIS

Every line below was opened. Flag VALUES were confirmed by **importing the
module** rather than reading the assignment, because this tree's own doctrine
warns that arm construction APPENDS overrides to the end of `doctrine.py` and a
read-the-assignment check is order-dependent (`doctrine.py:3205-3215`,
`doctrine.py:6050`). Command run:
`.venv/bin/python -c "import sys; sys.path.insert(0,'bots/_v542wave'); import doctrine as d; ..."`.

| flag | file:line | **effective value** |
|---|---|---|
| `LOKI_QUIET_ON` | `doctrine.py:1687` | **True** |
| `LOKI_FS_CREW` | `doctrine.py:2594` | True |
| `FS_HOME_TURRET_RESPONSE` | `doctrine.py:2653` | True |
| `LOKI_FS_V515` | `doctrine.py:3113` | **True** |
| **`FS_V515_DOOR_OFF`** | **`doctrine.py:3132`** | **True** |
| `FS_DOOR_DSQ` | `doctrine.py:2654` | **40** |
| `FS_CLEAR_RING_ON` | `doctrine.py:2485` | True |
| `HUNT_BAND_DSQ` | `doctrine.py:163` | 41 |
| `FS_EVICT_ON` / `FS_DUMP_MIN_OWN_DSQ` / `FS_DUMP_FAR_DSQ` | `doctrine.py:2433,2441` | True / 100 / 36 |

### 5.1 ⛔ THE DOOR-TURRET RESPONSE IS SHIPPED OFF, AND ITS OFF-SWITCH RESTS ON AN ALL-OURS FIXTURE

`_door_turret_turn` (`bots/_v542wave/main.py:1708`) is the tree's **only** verb
that melees an enemy turret standing near our own core. Its docstring
(`main.py:1711-1719`) states the mechanism exactly: *"quiet exists because 2
damage a round buys nothing against a 500 HP core, and a 40 HP sentinel is the
object where 2 damage a round FINISHES."*

It is switched off in the shipped build at `main.py:1734-1735`:

> ⛔ **AMENDED 2026-08-21T13:56Z (research lane, s53): both `main.py:1734-1735` cites in
> this document are WRONG — the enforcement is `main.py:1729-1730`. Settled by opening
> the file after the DOORWAVE drafter flagged that this study and the not-adgato study
> disagreed on the line (`:1729-1730` there — correct). Lines 1732+ are the raider/role
> and Ti-floor checks. The quoted code below is real; only its line number is off.
> Nothing else rests on the cite: the flag name, its value, and the doctrine anchor
> (`doctrine.py:3132`) are unaffected. Second cite at the CANDIDATE A GREP carries this
> same correction by reference.**

```python
if LOKI_FS_V515 and FS_V515_DOOR_OFF:
    return False
```

Both flags are True (table above), so **the verb returns before doing anything
in every game we have played against farming_200s v19.**

**AND THE OFF-SWITCH'S OWN DOCTRINE BLOCK SAYS WHAT IS WRONG WITH IT**
(`doctrine.py:3118-3131`, verbatim):

> *"the evidence that turned this off is a DOUBLE measurement on ONE chassis
> pair and both halves carry the same fixture caveat: **every game in both was
> played against `_v488beltbreak2`, our own bot**, so 'the field plants door
> turrets and we should ignore them' is NOT what was measured."*

That caveat is the exact hazard `CLAUDE.md` consequence 3 names — *"`bots/*_probe`
is a fixture WE authored and it lies in a known direction"* — and `CLAUDE.md`
point 6 — *"a refutation without live-game backing is a hypothesis, not a
refutation."* **The two measured grids (+36pp on `_v468kladturbo`, +18.9pp on
`_v488beltbreak2`) closed the road on OUR OWN BOTS.**

**AND THE NUMBER THAT MAKES THAT CAVEAT BINDING RATHER THAN PEDANTIC:
`FS_DOOR_DSQ = 40`, and 96 of 96 of farming_200s v19's sentinels are inside it
(§1.1). Their median plant is d² = 13 — a THIRD of the trigger band.** This is
the first live opponent we have measured whose **entire** core-kill channel
(§1.2, §1.3) is precisely the object `_door_turret_turn` exists to remove.

### 5.2 The other three melee paths are all pointed somewhere else (GREPPED)

* **`_sabotage_prio`** (`main.py:1830`) — melees the best adjacent enemy
  building and `SABOTAGE_PRIO` (`main.py:47-52`) ranks `GUNNER`/`SENTINEL` at
  priority **0**, i.e. first. It is dead at `main.py:1858-1859`:
  `if LOKI_QUIET_ON: return False  # QUIET: counterbattery melee silenced`.
* **`FS_CLEAR_RING_ON`** (`doctrine.py:2485`, used at `siege.py:4165`) pierces
  QUIET only for *"an ENEMY BUILDING STANDING ON A RING TILE"* — **THEIR** core's
  heal ring. Wrong end of the map.
* **`FS_V541_*`** (`doctrine.py:6044-6067`, used at `siege.py:4351-4409`,
  `raid.py:421,478`) un-silences the **on-seat core peck at the ENEMY core**.
  Also wrong end of the map.

⇒ **MEASURED-BY-READING: there is no live path in the shipped v177 tree that
attacks an enemy turret planted next to our own core.**

### 5.3 What we DO answer the plant with: a counterbattery TURRET, not a kill

`_try_counterbattery` (`main.py:1883`) reads `SLOT_THREAT` and buys a
turret whose ray already contains the threat. `SLOT_THREAT` **is** written for
their sentinel — both the core (`main.py:449-453`) and the builder
(`main.py:1431-1437`) publish it under
`et in CORE_THREAT_TYPES and d <= 64`, and `CORE_THREAT_TYPES` is
`frozenset((EntityType.GUNNER, EntityType.SENTINEL))` (`main.py:60`). So we
**see** the plant and **answer it by spending 30+ Ti on our own turret plus 10
ammo a shot**, rather than 2 Ti a peck against 40 HP.

**That is consistent with the tape:** we build 1.72 sentinels/game against them
and lose **0 of 103** of them (§1.7), while killing **21.9%** of theirs (§1.4).
The counterbattery survives; it just does not finish the job.

### 5.4 The home EXILE throw exists, is fired 28x a game, and does not aim at the border

`raid.py:1390-1424`, clause 1 *"EXILE"*, is the home-defence throw: any enemy
builder at `d² ≤ 2` of one of our launchers is picked up. Its **team filter is
correct** (`raid.py:1408`, `if ct.get_team(eid) == self.team: friendly_bots.append(...)`;
the enemy branch falls through to the throw). Its **destination policy** is:

```python
self._launch_far = sorted(
    sites, key=lambda t: t.distance_squared(self.core), reverse=True)   # raid.py:1413-1414
```

— **farthest from OUR core, and nothing else.** Compare the siege-layer evictor
`_fs_evict` (`siege.py:6684`), which explicitly ranks border tiles second
(`siege.py:6737-6739`, `border = 1 if (t.x == 0 or t.y == 0 or …)`) and whose
own docstring calls it *"the approved crash channel rides along for free"*
(`siege.py:6695-6697`).

⇒ **GREPPED ASYMMETRY: the forward evictor prefers the border; the home exiler
does not.** And the home exiler is where the farming_200s walker gets picked up.
Measured consequence, §2: **9.4% of our 1,708 exiles landed on a border tile and
7 of 1,708 victims died.**

Placement facts that matter for any candidate: our launchers go up **early
(median r5)** and **56 of 60 games have ≥1 of our launchers inside d² ≤ 40 of
our own core** — the same band their plant lands in. **We already own a body in
the right place.**

---

## 6. QUEUE CROSS-CHECK — WHAT IS ALREADY STOCKED (read before drafting rows)

`QUEUE.md` was grepped directly. **Absence control:** the token
`QQZZXNEVERAPPEARS7` returns **0** in `QUEUE.md` and **0** in
`bots/_v542wave/main.py`, so a zero from this grep is a real zero. *(⚠ note for
future audits: `ZZQXNOTATOKEN`, the repo's usual absence control, is **written
into `QUEUE.md` 16 times** as documentation of past audits and is therefore no
longer usable as a control against that file.)*

| token | hits in QUEUE.md |
|---|---|
| `door` | 3 (one is the relevant row) |
| `FS_V515` / `DOOR_OFF` / `_door_turret` | **0 / 0 / 0** |
| `farming_200s` | 3 (all incidental — a destroy-rebuild rate, a first-build-round table, a peak-bank table; **no row is about this opponent**) |

**The relevant stocked row is `QUEUE.md` #96** — *"REMOVE THE TURRET THAT IS
GRINDING US — un-silence builder melee against COLLAR/SIEGE TURRETS
specifically"*. **Its premise has moved and nobody has noticed.**

### ⭐ STALENESS FINDING ON #96 — THE ROW IS NO LONGER A BUILD, IT IS A FLAG FLIP

#96's GREP cell was run **2026-08-18 against `_v488beltbreak2`** and concludes,
verbatim: ***"No turret-attack path exists anywhere in the tree."***

**That was true then and is FALSE against the live control.** Measured by
grepping four trees for `_door_turret_turn`, with the absence control above:

| tree | `_door_turret_turn` occurrences | `FS_HOME_TURRET_RESPONSE` | `FS_V515_DOOR_OFF` |
|---|---|---|---|
| `_v488beltbreak2` (#96's anchor) | **0** | absent | absent |
| `_v512ringladder` | 0 | absent | absent |
| `_v514ferrycrew` | **2** | `= True` | absent (verb **ON**) |
| **`_v542wave` (live v177)** | **6** | `= True` | **`= True` (verb OFF)** |

⇒ **The carve-out #96 asks to be BUILT already exists, complete, with its own
trigger band (`FS_DOOR_DSQ = 40`), its own anti-treadmill cap
(`FS_DOOR_MAX_RNDS = 40`), its own Ti floor (`FS_DOOR_TI_FLOOR = 6`) and a
beacon fallback — and is disabled by ONE boolean.** #96's line anchors have also
drifted: it cites `_nearest_home_intruder` at `main.py:624-631`; in `_v542wave`
it is `main.py:1800-1817` (and its `EntityType.BUILDER_BOT`-only filter at
`main.py:1806-1807` is still exactly as #96 describes — **that half of the row's
grep is intact**).

**CONSEQUENCE FOR THE LEG DESIGN, which is the point of saying it:** #96 as
written proposes *"local paired screen vs control first, then a pre-registered
unrated leg — 0033 pinned"*. A flag flip needs no build step and no local screen
to establish the verb runs; and **farming_200s v19 is a strictly better first
live opponent than 0033 for this specific question** (§7).

---

## 7. THE EXPLOITABLE HABITS, RANKED

Ranked by (measured size of the habit) × (our measured failure to punish it) ×
(how cheap the change is). Every rank carries its own falsifier.

### RANK 1 — THE DOOR SENTINEL IS THEIR ONLY GUN AND WE HAVE THE VERB SWITCHED OFF

**The habit (MEASURED):** 96 of 96 sentinels planted inside d²≤32 of our core
(§1.1); zero gunners, zero launchers (§0); zero core melee in 130/130 games
(§1.2); **32 of 32 of our core deaths preceded by a plant, 0 of 32 without**
(§1.3).
**Our failure (MEASURED):** we kill **21.9%** of them; **75 of 96 survive to the
end of the game**; when we do kill one they **fail to replant 14 times in 21**
(§1.4).
**The lever (GREPPED):** `FS_V515_DOOR_OFF = False`. One boolean,
`doctrine.py:3132`.
**Why the off-switch does not bind here (this is the crux):** the doctrine block
that flipped it says its evidence is *"every game in both was played against
`_v488beltbreak2`, our own bot"* (`doctrine.py:3118-3131`). Under `CLAUDE.md`
point 6 that is a hypothesis, not a refutation — and farming_200s v19 is the
**first live opponent measured whose entire kill channel sits inside
`FS_DOOR_DSQ`**.
⚠ **HONEST COUNTER, stated because the row must not be cheap:** the off-switch
was **+36pp and +18.9pp on two independent grids**, and the mechanism guess in
the doctrine (*"door pecks spend home actions and 2 Ti/peck out of a bank the
earlier turret has already tightened"*) is opponent-independent — it could bite
here too. **The leg must therefore be a real two-arm test, not a re-enable.**

### RANK 2 — WE THROW THEM 28 TIMES A GAME AND KILL 7; THE HOME EXILE HAS NO BORDER SELECTOR

**The habit (MEASURED):** they walk a builder to our door and plant; they have
**no launcher of their own in 130/130 games**, so the pickup exchange is
one-way.
**Our failure (MEASURED):** 1,708 exiles → **90.6% RETHROWN, 9.4% border,
0.4% died** (§2).
**The lever (GREPPED, and it is a PORT not an invention):** `raid.py:1413-1414`
sorts destinations by distance from our core only; `siege.py:6737-6739` — in the
same tree, for the same verb — already ranks border tiles second and its
docstring calls it *"the approved crash channel rides along for free"*
(`siege.py:6695-6697`). **One tree, two evictors, one of them aims at the border.**
**Cross-refs:** `QUEUE.md` #17, #5, #38 all own the border-throw question. **This
study refreshes their GREP against the live control:** #38's *"NO border-tile
selector"* claim is **still true of the home exile (`raid.py:1413`) and now FALSE
of the siege evictor (`siege.py:6737`)** — those rows' anchors predate
`_fs_evict`. **Do not stock a fourth row; refresh those three.**

### RANK 3 — THEIR CPU CEILING (LOOK, DO NOT SPEND A LEG YET)

**The habit (MEASURED):** their busiest unit-turn costs **7,099 µs of a 10,000 µs
budget in the median r0-150 band, against our 900 µs**, and they hit the ceiling
(10,505-10,511 µs) in **12 games across all versions** (§3).
**Why it is RANK 3 and not RANK 1:** **we have no measured lever.** Correlation
between our build volume and their TLE count is **r = −0.125 (n=60)** — nothing,
and the wrong sign. The blow-ups are **6 of 60 games** with a median of **0**.
And of those 6 we **lost 4**.
**NOT ADMISSIBLE AS A ROW YET.** A row needs a mechanism metric that names what
WE do; this has none. What it justifies is a cheap read, not a leg: find the
trigger inside `20b341f9…` (antler, 214 TLEs) before proposing anything.

### REFUTED IN PASSING — RETAINED SO NOBODY RE-DERIVES THEM

1. **"They plant early on maps where we lose."** ✗ The per-map table (§4) orders
   the other way as often as not — fjordgate median plant **r2** and we win 2/3;
   midgard **r45** and we lose 4/4.
2. **"Flood their vision with cheap barriers to push them over the CPU cliff."**
   ✗ `r = −0.125` between our total builds and their TLE count across 60 games.
   Not supported, and negative.
3. **"They got better at v19."** ✗ Their v19 is a **revert to their v15 doctrine**
   (§0), and against their v15 we ran **55.6%** with a **39-round kill-speed
   advantage**. The turret table is nearly identical between v15 and v19
   (sentinels 1.62 vs 1.60, conveyors 9.20 vs 9.20, builders 6.89 vs 6.65). **The
   cell moved without their doctrine moving**, which points at our v162–v176 line
   as at least a co-cause — and §1.5's chassis cells are too small to settle it.
4. **"Our launcher is winning the exchange because they have none."** ✗ We lose
   **65% of our launchers (2.35 of 3.62 built per game)** and **0 of 103
   sentinels** (§1.7). The piece they cannot counter is the piece dying most.

---

## 8. CANDIDATE QUEUE ROWS (DRAFTS — research admits, this study does not)

⚠ **`QUEUE.md` was NOT edited by this study.** These are drafts in the repo's
column format (`| # | plank | GREP | mechanism metric | fixture | why now |`).

**TARGET BAND** (commission-supplied, `tools/target_value.py` **must be re-run at
prereg time**, not copied from here): `farming_200s, gap +0 (them 1845 / us 1826),
5-0 pays +16.00, reachable YES`. For contrast the same gate scored the s28 crash
leg's whole target set at **under +1.18** — **this opponent pays 13x that.**

### CANDIDATE A — **AMEND `QUEUE.md` #96, do not stock a new row**

> **change** · Set `FS_V515_DOOR_OFF = False` (`bots/_v542wave/doctrine.py:3132`)
> — one boolean — re-enabling `_door_turret_turn` (`main.py:1708`), the tree's
> only verb that melees an enemy turret standing inside `FS_DOOR_DSQ = 40` of our
> own core. **NO new code.** #96 currently proposes building this carve-out;
> **it is already built.**
>
> **GREP (run 2026-08-21 against the LIVE control `bots/_v542wave`, every anchor
> opened, absence control `QQZZXNEVERAPPEARS7` = 0 in `main.py` and in
> `QUEUE.md`)** · ⛔ **#96's cell — *"No turret-attack path exists anywhere in the
> tree"*, run 2026-08-18 against `_v488beltbreak2` — IS NOW FALSE.**
> `_door_turret_turn` occurrences: `_v488beltbreak2` **0** → `_v514ferrycrew` **2**
> (`FS_HOME_TURRET_RESPONSE = True`, no off-switch) → `_v542wave` **6** with
> `FS_V515_DOOR_OFF = True` (`doctrine.py:3132`) and `LOKI_FS_V515 = True`
> (`doctrine.py:3113`), so the verb returns at `main.py:1734-1735`. Flag values
> confirmed by **importing `doctrine`**, not by reading the assignment, per the
> tree's own append-order warning (`doctrine.py:3205-3215`). **STILL TRUE from
> #96:** `LOKI_QUIET_ON = True` (`doctrine.py:1687`); `_nearest_home_intruder`
> filters to `EntityType.BUILDER_BOT` only, so a planted sentinel is never an
> "intruder" (**line drift: `main.py:1800-1817`, not `:624-631`**);
> `_sabotage_prio` ranks turrets priority 0 (`main.py:47-52`) and is dead at
> `main.py:1858`. **The other two QUIET carve-outs are aimed at the ENEMY core,
> not ours:** `FS_CLEAR_RING_ON` (`siege.py:4165`), `FS_V541_*`
> (`siege.py:4351`, `raid.py:421`).
>
> **mechanism metric** · **their forward-sentinel median lifetime and kill share**
> (engine-side, `corpus/events.tsv` BUILD/DEATH on their `sentinel` rows filtered
> to `d²_enemy ≤ 32`). Control arm baseline is measured and pre-registered here:
> **21 of 96 killed (21.9%), median lifetime 74 rounds, 75/96 alive at game end,
> across 60 games.** Charge the cost side explicitly — **builder-rounds spent on
> the door and Ti spent at 2/peck** — because #96's own 4:1 melee objection is
> the thing that has to be priced (40 HP sentinel = 20 pecks = 40 Ti). PROGRAMME
> primary alongside: **ITT timely-kill rate (share of ALL games ending in a
> core-kill by r300; control = 31.7% over 60 games)** and game share.
>
> **fixture that can resolve it** · **A pinned two-arm unrated leg vs
> farming_200s: `fcode match unrated <team> --match <past_v19_match_id>`**
> (`docs/fcode-cli.md:330`) so both arms meet v19 — mandatory here because they
> have shipped 12 versions and v18→v19 was a **total turret-doctrine flip**
> (§0), so an unpinned leg is measuring their release schedule.
> ⛔ **NOT a local screen and NOT our own probes:** the off-switch's entire
> evidence base is `_v488beltbreak2`/`_v468kladturbo` — **our own bots** — and
> re-running the same fixture class cannot answer a question the fixture class
> created. ⛔ **POWER: a 25-game window has a same-bot swing of 12pp and an MDE
> of ~39pp** (`CLAUDE.md`); the effect this must resolve on the mechanism metric
> is a lifetime/kill-share move, not a win rate — **pre-register the window
> count needed on the mechanism metric and pool**, and do not write a currency
> verdict off one window.
>
> **why now** · **This is the first LIVE opponent whose entire core-kill channel
> is the exact object the disabled verb removes.** 96/96 of their sentinels are
> inside `FS_DOOR_DSQ`; **32/32 of our core deaths in 60 games were preceded by
> one and 0/32 were not**; we kill 21.9% of them and they fail to replant
> **14 of 21** times we do. They are at **parity rating (+0 gap) and a 5-0 pays
> +16.00** — 13x the s28 crash leg's whole target set. And the off-switch is a
> road closed on our own fixture, which `CLAUDE.md` point 6 does not permit.
> ⚠ **The counter, kept in the row:** the off-switch measured **+36pp and
> +18.9pp** on two grids, and its mechanism guess (door pecks spend home actions
> and bank) is **opponent-independent**. **Two arms or nothing.**

### CANDIDATE B — **AMEND the GREP cells of `QUEUE.md` #17, #5 and #38; stock nothing new**

> **change** · Give the HOME exile the border preference the SIEGE evictor
> already has: `raid.py:1413-1414` sorts throw destinations by
> `distance_squared(self.core), reverse=True` and **nothing else**, while
> `siege.py:6737-6739` — same tree, same verb class — ranks
> `border = 1 if (t.x == 0 or t.y == 0 or t.x == w-1 or t.y == h-1)` as the
> second key, with a docstring calling it *"the approved crash channel rides
> along for free"* (`siege.py:6695-6697`). **A port of eight lines, not a new
> mechanism** — and therefore inside the approved class with no new organiser
> question (the class ruling: a new TRIGGER needs no new question).
>
> **GREP (run 2026-08-21 vs `_v542wave`)** · #38's cell asserts *"EXILE …
> throw to the site FARTHEST from our core, `raid.py:900-932`; **NO border-tile
> selector, no map-area keying**"*. **HALF-STALE: the claim is still TRUE of the
> home exile (now `raid.py:1390-1424`, sort at `:1413`) and is now FALSE of the
> tree as a whole** — `_fs_evict` (`siege.py:6684`) was added since those rows
> were stamped and **does** select for border. #17's *"`bots/_v148ferryfirst/raid.py`
> has zero `border`/`edge` references"* is likewise superseded: `_v542wave` has
> them, in `siege.py`. **All three rows' pointers are ≥2 incumbents behind.**
>
> **mechanism metric** · **border-landing share of our EXILE throws**
> (`corpus/throws.tsv` `border` column) and **enemy builder removals with no
> preceding damage event** (`tools/crash_census.py` / `tools/kidnap_fate.py`
> risk-set form). Control baseline pre-registered from this study: **vs
> farming_200s v19, 161 of 1,708 exiles (9.4%) land on a border tile; victim
> fate DIED = 7 of 1,708 (0.4%); RETHROWN = 1,547 (90.6%).**
>
> **fixture that can resolve it** · #17's LOCAL both-ways dose check remains the
> stated precondition and is unchanged (`_probe_oov_raw` must crash,
> `_probe_oov_guard` must not, border-arm-off must not). **What this study adds
> is the live target for the step after it:** farming_200s has **zero launchers
> in 130/130 games**, so the pickup exchange against them is one-way and
> uncontested — the cleanest live cell on the board for a border-dose read.
>
> **why now** · The treadmill is measured and it is enormous: **28.5 exiles per
> game converting to 0.4% victim deaths**, against a mechanism whose whole value
> is the death. And the fix is a **copy of code already in the same tree**.
> ⚠ **Rank it BELOW Candidate A.** #5's own history says the displacement
> channel is at best weakly positive (**+0.265pp, 95% CI [+0.034, +0.496],
> 17 and 13 events**) and that **only 2.62% of enemy-builder removals are
> no-damage at all** — the ceiling is small even if it fires. Candidate A moves
> the object that causes **100% of our core deaths in this cell**.

### NOT ADMISSIBLE — stated so it is not silently dropped

* **CPU denial (§3).** No lever measured; `r = −0.125` between our build volume
  and their TLE count. A row needs a mechanism metric naming what WE do.
* **Map-conditioned play (§4).** Every v19 map cell is n≤7. `royale 0/9` and
  `nordkap 4/14` pooled across their versions are EYEBALL. **Pool first.**

---

## 4A. THE WALKER — A PER-ROUND POSITION WALK (delegated measurement, controls below)

**PROVENANCE.** Measured by a dedicated opus decoding agent on the same 60
replays, built on `tools/replay_census.py` primitives (`fields`, `read_pos`,
`parse_entity`, `packed_varints`) — **no hand-rolled protobuf parser**. Scratch
code under `scratchpad/f2/{walk.py,analyse.py,report.py,reportE.py}`. It was
given §1.1's figures as GIVEN, and **blindly reproduced them from a different
code path** (96 plants in 55 of 60 games, median d² 13, median plant round 32.5
vs my 32) before measuring anything new.

**Attribution rule:** the planting builder is read off the engine's own
`builderBuild` update (schema field 16, `{id, target}`), **not** guessed from
adjacency. **96 of 96 plants attributed, 0 UNATTRIB**, and **96 of 96 are
DISTINCT bots — no bot ever planted twice.**

### 4A.1 The trip: a slow, straight, ~9-round-exposed run-in (MEASURED, n=96 plants)

| quantity | min | q1 | **MED** | q3 | max |
|---|---|---|---|---|---|
| approach round (first inside d²≤100 of our core) | 1 | 7 | **18.5** | 36 | 228 |
| first inside d²≤32 | 1 | 16.5 | **26** | 44 | 237 |
| plant round | 2 | 20 | **32.5** | 51 | 242 |
| **WINDOW: d²≤100 → plant** | 1 | 7 | **9 rounds** | 14 | 100 |
| **WINDOW: d²≤32 → plant** | 1 | 2 | **4 rounds** | 6 | 91 |
| walker age at plant | 1 | 18 | **29.5** | 48 | 102 |

Median d² to our core, k rounds before the plant (n falls as walkers pre-date
their own spawn): `k=0:13 · 1:13 · 2:17 · 3:25 · 4:29 · 5:40 · 6:50 · 7:61 ·
8:65 · 9:82 · 10:85 · 12:104 · 15:148 · 20:260`. **A monotone ~1 tile/round
run-in.**

**The window is a walking-speed constant, not a map constant** — above ~10 tiles
of core separation it does not move:

| core separation | plants | games | med window (d²≤100) | med window (d²≤32) | med plant round |
|---|---|---|---|---|---|
| ≤10 tiles | 11 | 7 | **3** | 3 | r5 |
| 10–20 | 34 | 19 | **11** | 4 | r22 |
| >20 | 51 | 29 | **10** | 4 | r45 |

⚠ **On close-core maps there is NO window** (11 plants, median 3 rounds). On
10x10 `fjordgate` their bot is at d²=13 on **r1** and the sentinel is up on
**r2**. Any interception plank must state that it does nothing on this map class.

### 4A.2 They approach in a ±4-tile CONE, not on the axis (MEASURED, n=96)

Frame: +X = unit vector from THEIR core to OUR core, origin at our core.

| within ±k lateral tiles | at the d²≤100 crossing | at the plant tile |
|---|---|---|
| ±1 | 37/96 (39%) | 43/96 (45%) |
| **±2** | **44/96 (46%)** | 58/96 (60%) |
| ±3 | 53/96 (55%) | 76/96 (79%) |
| **±4** | 55/96 (57%) | **92/96 (96%)** |

Median |lateral| is **3.0 tiles at the crossing** and **2.0 at the plant tile**.
Signed side: **L 48 / R 37 / on-axis 11 — no handedness bias.**
⇒ **A single-tile ambush on the core-to-core axis catches under half of them. A
±4 cone catches 96% — but only at the plant, by which time the sentinel exists.**

### 4A.3 ⭐ WE HAVE THE COUNTER-TOOL AND IT IS ON THE WRONG SIDE OF THE MAP (MEASURED)

| | |
|---|---|
| walkers EVER inside launcher pickup range (d²≤2) of a live launcher of ours | **7 / 96 (7.3%)**, in 6/60 games |
| median rounds pickup-able, across all 96 | **0** (q3 = 0) |
| walkers with no live launcher of ours anywhere during their window | 21/96 |
| our launchers per game / build round | med **4** / med **r5** |
| **our launcher d² to OUR OWN core** | q1 34, **med 128**, q3 338, max 1205 |

Walker's closest approach to any live launcher of ours: **d²≤2 in 7/96 · ≤4 in
18 · ≤8 in 26 · ≤13 in 36 · ≤26 in 41.**

**CROSS-CHECK against `corpus/throws.tsv` (independently written decoder), and
it is a genuine other-verdict test — it could have shown many walkers thrown:**
our throws of enemy bots in these games land at **median round 131** (q1 65,
q3 229) while the median plant is **r32.5** — **our throwing machine runs ~100
rounds after the walker has already planted.** Only **5 of 96 walker bot-ids**
ever appear as a bot we threw (6 events). Of those 6: **3 came AFTER the plant**;
the other 3 landed on bots that **walked back and planted anyway.**

⇒ **MEASURED: 0 of 96 forward sentinel plants were prevented by a launcher
throw** — against 161 distinct enemy bots thrown in the same 60 games, so the
tool works and is simply aimed elsewhere. **The cause is SITING, not timing or
capability.**

### 4A.4 How the walker dies (MEASURED)

Plant-identified walkers are **selected on having planted**, so "killed before
the plant" is **0/96 by construction** — the agent flagged this rather than
reporting the tautology. The honest cohort is *every enemy builder that entered
d²≤100 of our core*, **n=212 over 60 games**:

| | |
|---|---|
| went on to plant | 96/212 (45.3%) |
| **non-planters killed** | 21/116 (**18.1%**) |
| **planters killed, at any time** | 23/96 (**24.0%**) |
| planters alive at game end | **73/96 (76.0%)** |
| rounds plant → walker death (n=23) | q1 19, **med 35**, max 471 |

**We kill about one in five of everything that walks into our half.**

### 4A.5 ⭐⭐ THE SECOND HALF OF THE PLANT: THEY COLLAR OUR CORE

**The walker does not stop at the sentinel. 69 of 96 keep building** (median 2
further builds, max 13).

**MEASURED, and I verified this independently from `corpus/events.tsv` after the
agent reported it, because it reframes the matchup:**

| version | their barriers | **at d² ≤ 5 of OUR core** | at d² ≤ 5 of THEIR OWN core | median build round |
|---|---|---|---|---|
| v15 | 197 | **197/197 = 100%** | 0 | r87 |
| v18 | 114 | **114/114 = 100%** | 0 | r64 |
| **v19** | **314** | **314/314 = 100%** | **0** | **r81** |

d²-to-our-core histogram, v19: `d²=1: 77 · d²=2: 79 · d²=4: 77 · d²=5: 81`.
**Those four values ARE the orthogonal-8 ring of a 2x2 core footprint — the heal
seats.** 625 of 625 barriers across 130 games, zero exceptions.

⇒ **farming_200s does not merely snipe our core. It plants an obstacle-ignoring
sentinel at d²≈13 and then DENIES OUR HEAL SEATS with a barrier ring.**

**INFERENCE (mechanism, not measured here):** that is why §1.3's median lag from
plant to our core's death is **146 rounds** rather than the ~84 a continuously
firing sentinel would need. The sentinel out-damages our healing only once the
seats are gone; the collar is the second half of the kill.

⛔ **AND IT IS A MIRROR OF OUR OWN PLANK, WHICH IS THE CONTROL THAT MAKES THE
READING NON-CIRCULAR:** the same counter on OUR barriers reads **370 of 392
(94.4%) at d²≤5 of THEIR core, median round r30**. **Both bots collar. We collar
51 rounds earlier.** So "barriers near a core mean a collar" is not an
interpretation I imposed on their data — it is the identical signature our own
seat-seal produces, measured by the same instrument in the same games.

### 4A.6 THEY HAVE NO HOME-DEFENCE TRIGGER AT ALL (MEASURED, n=60)

Arrival = first round any entity of ours is within d²≤32 of THEIR core.
**60/60 games have one, at median round 6** (q1 4, q3 10).

| | d²≤32 arrival |
|---|---|
| games with a home barrier/turret build BEFORE arrival | **0/60** |
| games with a home barrier/turret build AFTER arrival | 6/60 |
| **games where they NEVER build one after arrival** | **54/60 (90%)** |
| latency when it does happen (n=6) | med 4 rounds |

Their whole-game build mix within d²≤32 of their own core, all 60 games:
`builder_bot 399 · conveyor 374 · harvester 79 · sentinel 9 · barrier 5`.
**An economy footprint with no defensive component.**

⚠ **NOT RESOLVABLE, and the agent said so rather than substituting a number:**
the clean spawn-cadence control (arrival ≥ r20, so the 20-round pre-window is
not truncated by game start) has **n=2**. The flat 2.95 → 2.92 spawns-per-20-rounds
figure across the arrival boundary is computed on windows **clipped at r0 for
most games** and is not claimed as a reaction measurement. **What IS established
at n=60 is the build side: 54/60 zero post-arrival home defence.**

### 4A.7 CONTROLS ON THE POSITION WALK — stated verbatim

| control | result |
|---|---|
| per-(file, team, kind) BUILD and DEATH counts vs `corpus/events.tsv` (independent decoder) | **BUILD 649/649 cells agree; DEATH 306/306 agree** |
| walker-ID run on **OUR** sentinel builds (must find builders — we build sentinels) | **fired correctly: 73 of our forward plants in 45/60 games, 73/73 attributed, 0 UNATTRIB** |
| **corruption control** — shift every ENTITY position by (+5,+5), cores fixed | **FIRED HARD: plants 96→22, games with a plant 55→19, med window 9→19, med plant d² 13→25, pickup-able walkers 7→3** |
| ⚠ **discarded first attempt at that control** — shifted cores by the same vector | **left every figure byte-identical (a relative-distance no-op). Recorded because a shift-both control would have "passed" while checking nothing.** |
| attribution driven to a second independent method (position adjacency vs `builderBuild`) | **agree 96/96**; adjacency alone was **ambiguous in 12/96** (two candidate builders) — the engine channel resolves all 12 |
| `throws.tsv` cross-check as an other-verdict test | **could have shown many walkers thrown; shows 5/96 against 161 distinct enemy bots thrown in the same files** |
| barrier-ring finding re-derived by me from `corpus/events.tsv`, plus the complement group (our own barriers) | **314/314 theirs at d²≤5 of our core; 370/392 ours at d²≤5 of theirs — the counter discriminates and is not constant** |

### 4A.8 ANCHORS (file + round)

1. **`082a0792-5d31-4c42-b122-f2bb13a60d08_game_3.replay26`, their bot #8** —
   the longest exposure of all 96. Enters d²≤100 at **r11**; we throw it at
   **r13** and again at **r59** (`throws.tsv`, `vfate` RETHROWN then ALIVE_END);
   it is **pickup-able on rounds 83, 86, 87, 88, 89, 90, 94, 95, 96** — nine
   separate rounds — and still plants sentinel #120 at d²=16 on **r104**, then
   survives to game end.
2. **`082a0792-…_game_1.replay26`, their bot #5** — the typical trip, fully
   legible: d² to our core `122 (r42) → 101 → 104 → 85 → 68 → 53 → 53 → 40 → 29
   → 20 → 13 (r52) → plant r53` at d²=18. **8 rounds inside d²≤100, 3 inside
   d²≤32.**
3. **`1a0abf13-c253-48cf-aa8b-4152039d476f_game_2.replay26`, their bot #8** —
   approach r17, inside d²≤32 at r21, **plants at d²=2, orthogonally adjacent to
   our core footprint, on r27**; the walker lives until r318.
4. **`37aad00c-…_game_1`, `1a0abf13-…_game_3`, `9eb16b87-…_game_1` (10x10
   `fjordgate`, cores 5.66 tiles apart)** — their bot is at d²=13 on **r1**, the
   sentinel is up on **r2**. In `37aad00c` we threw that exact bot at **r4**, two
   rounds after it had already planted. **The no-window map class.**
5. **`64f98d75-5027-49a6-a968-c627dc519420_game_4.replay26`, their bot #209** —
   thrown by us at **r221**, walks back, re-enters d²≤100 at **r228**, plants at
   **r242**. A throw that was in range and did not prevent the plant.

---

## 9. RANKING REVISED AFTER §4A, AND ONE MORE CANDIDATE

§4A changes two things in §7 and adds one row. **§7 stands as written except
where amended here.**

### 9.1 RANK 2 IS RE-CAUSED: our launcher problem is SITING, and it is measured

§7 RANK 2 blamed the *destination* of our throws (no border selector). §4A shows
the destination is **almost irrelevant to the walker**, because **only 7 of 96
walkers were ever inside pickup range at all** and **0 of 96 plants were
prevented**. The cause is that our launchers go up at **median r5** at **median
d² 128 from our own core** — forward with the raid — while the entire walker trip
happens in **our** half and is over by **r32.5**.

**Candidate B (border selector) is NOT withdrawn** — it is a cheap in-tree port
and it governs the 1,708 throws we *do* make. But **it cannot be the plank that
stops the plant**, and a prereg that claims it will is claiming something §4A
already measured as false. **Re-labelled: Candidate B is a crash-channel dose
plank (#17/#5/#38 family), not an anti-plant plank.**

### 9.2 ⭐ NEW — CANDIDATE C: THE COLLAR MIRROR IS MISSING

**The habit (MEASURED, and I re-derived it from `corpus/events.tsv` myself):**
**625 of 625 of their barriers across 130 games sit at d² ≤ 5 of OUR core** —
the orthogonal-8 heal ring — **and 0 of 625 near their own** (§4A.5). In v19:
314 of 314, median round **r81**, after the sentinel lands at r32.5.
**Complement-group control:** our own barriers read **370 of 392 (94.4%) at d²≤5
of THEIR core, median r30** — the same signature, so the instrument
discriminates and the reading is not an interpretation imposed on their data.

**Our failure (GREPPED, live control `bots/_v542wave`):**
* `FS_DOOR_TYPES = frozenset((GUNNER, SENTINEL, LAUNCHER))` — `doctrine.py:2662`,
  value confirmed by import; used at `main.py:1682`. **BARRIER is not in it**, so
  even with `FS_V515_DOOR_OFF = False` the door verb walks past all 314.
* `FS_CLEAR_RING_ON` (`doctrine.py:2485`, `siege.py:4165`) is the tree's clearance
  verb for *"an ENEMY BUILDING STANDING ON A RING TILE"* — **THEIR** ring only.
* `_sabotage_prio` would rank a barrier (priority 5, `main.py:47-52`) but is dead
  under `LOKI_QUIET_ON` at `main.py:1858`.
⇒ **We have a ring-clearance doctrine, fully written, pointed at exactly one end
of the map. There is no path in the shipped tree that removes an enemy building
from our own heal seats.**

> **change** · Extend the existing ring-clearance carve-out to OUR ring: an enemy
> building standing on one of our core's orthogonal-8 heal seats gets the peck,
> under the same caps the tree already uses for the mirror
> (`FS_CLEAR_MAX_PECKS = 8` per tile, `doctrine.py:2198`; `FS_REBUILD_MAX = 3`,
> `doctrine.py:2493`). A barrier is 30 HP = 15 pecks = 30 Ti.
>
> **GREP** · as above — `FS_DOOR_TYPES` excludes `BARRIER` (`doctrine.py:2662`,
> import-confirmed); `FS_CLEAR_RING_ON` is scoped to the enemy ring
> (`siege.py:4165`); `_sabotage_prio` silenced (`main.py:1858`). **No path
> exists.** Absence control `QQZZXNEVERAPPEARS7` = 0 in all four bot files.
>
> **mechanism metric** · **enemy buildings resident on our core's orthogonal-8,
> per round, integrated over the game** (engine-side, `events.tsv` BUILD/DEATH
> at d²≤5 of our core). Control baseline pre-registered from this study: **314
> planted, median r81, and our recorded removals of them are the 1.32/game
> `barrier` DEATH rows in §1.7 — i.e. they are being removed by something already,
> and the leg must first establish BY WHAT before crediting a new verb.**
> Secondary: **our core's healed-HP per round while collared** (this is the
> INFERENCE in §4A.5 and the leg is what would convert it).
>
> **fixture** · **Pinned unrated leg vs farming_200s v19**, same design as
> Candidate A and **naturally run as a third arm of it** — the two planks act on
> the same object (their door installation) at different times (r32 sentinel,
> r81 barriers) and a shared control arm prices both.
>
> **why now** · It is the second half of the only kill channel they have, it is
> **100% deterministic across 130 games and three of their versions**, and the
> counter-doctrine is **already written for the mirror case**. ⚠ **Rank BELOW
> Candidate A**: the sentinel is necessary for the kill (32/32, §1.3) and the
> collar is, on current evidence, an accelerant whose contribution is
> **INFERRED, not measured**.

### 9.3 The verb's own docstring already described this opponent

`main.py:1655-1664` — the docstring of `_door_turret`, quoting the v512 autopsy:

> *"40 were planted, our builders attacked NONE of them, and 38 of 40 were still
> standing at the end of the game. Median warning from plant to our core's death:
> 56 rounds. A sentinel is 40 HP and a builder peck is 2 damage for 2 titanium —
> two bodies finish it in ten rounds, and the bank held the titanium every time."*

**This study is that measurement repeated against a LIVE OPPONENT rather than a
fixture:** 96 planted, **75 of 96 standing at game end**, **median warning 146
rounds** (§1.3), and we killed 21.9% (§1.4). **The numbers are the same shape and
the warning is 2.6x longer.** The v512 version came from our own arena; this one
did not. Under `CLAUDE.md` point 6 that is the difference between a hypothesis
and a live-backed finding — and it is the whole "why now" for Candidate A.

---

## 10. LEDGER ROW (DRAFT — this study did NOT edit the ledger)

`docs/research/move-mining-ledger.tsv` header is
`date\topp\toppver\tgames_covered\tdoc` and existing rows are tab-separated with
`games_covered` counting the games the study read. **This study read the 60
archived v19 replays plus the v15 (45) and v18 (25) eras as comparison ground.**
Matching the file's convention of one row per (opp, version) covered:

```
2026-08-21	farming_200s	19	60	docs/research/REPLAY-STUDY-farming200s-v19-2026-08-21.md
2026-08-21	farming_200s	15	45	docs/research/REPLAY-STUDY-farming200s-v19-2026-08-21.md
2026-08-21	farming_200s	18	25	docs/research/REPLAY-STUDY-farming200s-v19-2026-08-21.md
```

⚠ **`games_covered` for v19 is 60, not the trigger's 65** — five games
(`2026-08-20T18:32:59Z`) have no archived replay and were read only through
ladder metadata. **If the trigger's coverage arithmetic is keyed to 65 it will
re-fire on this opponent at 5 games**, which is below its own ≥20 threshold, so
this is safe but worth knowing.

---

## 11. WHAT WOULD FALSIFY THIS STUDY'S CENTRAL CLAIM

The central claim is: **farming_200s v19's entire core-kill channel is a forward
sentinel plant plus a heal-seat collar, and the shipped v177 tree has no live
verb that removes either.**

It is falsified by any one of:
1. A v19 game in which **our core dies with no their-sentinel inside d²≤32 of it**
   (currently 0 of 32).
2. A v19 game in which **their `batk_core` is non-zero** (currently 0 of 130
   games across three versions).
3. Finding a live code path in `bots/_v542wave` that melees an enemy turret or an
   enemy building inside our core's heal ring — i.e. showing that
   `FS_V515_DOOR_OFF`, `FS_DOOR_TYPES` or `LOKI_QUIET_ON` do not gate what §5.2
   and §9.2 say they gate. **The flag values were confirmed by import, not by
   reading assignments**, so this would have to be a path I did not find rather
   than a value I misread.
4. A pinned two-arm leg in which the door response is ON and their forward
   sentinels' median lifetime **does not fall** from the pre-registered control
   of **74 rounds / 21.9% killed / 75 of 96 alive at end**.

**(4) is Candidate A. The study is written so that the leg can refute it.**

---

## 12. COORDINATION NOTE — another lane is in this subsystem RIGHT NOW

Observed while auditing the tree (not a finding about the opponent):
`bots/_probe_peck_a/` and `bots/_probe_peck_b/` were created at
**2026-08-21 15:15–15:16** local (`ls -la`), i.e. **during this study**, and
`bots/_probe_doorlaunch/` (2026-08-20 08:17) documents a *"door-launcher kill …
TARGETING rule"* keyed to a constant `V530_DOOR_DSQ`. **Candidates A and C land
on the same subsystem the builder lane appears to be probing.** Whoever admits
these rows should reconcile with that work before a leg is designed — in
particular, `_probe_doorlaunch`'s own docstring already states the fixture
caveat this study exists to escape: *"FIXTURE, NOT AN OPPONENT, AND IT LIES IN A
KNOWN DIRECTION."*
