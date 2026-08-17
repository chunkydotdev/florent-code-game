# REPLAY STUDY — `lingling_40h` **v61**, 50 rated games, our v140/v152

**Move-mining loop, step 2 (STUDY).** Method: `docs/research/PLAYBOOK-move-mining-2026-08-16.md` §3.
Fresh opus subagent, no inherited session context. Nothing committed by the agent; no bot edited,
no match fired, no submission touched.

---

## PROVENANCE

**Ground.** Opponent `lingling_40h`, **their version 61**. All **50 archived rated games** we have
against that version — **10 matches**, 14 distinct maps, `corpus/join.tsv` filtered on
`opp == lingling_40h AND oppver == 61`. Unusually for this corpus, all 50 were played by a
current-lineage bot of ours: **`ourver` 152 in 45 games (9 matches), `ourver` 140 in 5 games
(1 match)**. Our game share in the cell is **42.0% (21/50)**; all-time against them 38.7% (n=75).

⛔ **VERSION BOUNDARY — READ THIS BEFORE QUOTING ANYTHING BELOW AS "WHAT THEY DO".**
`corpus/league_matches.tsv` has them on **v61 from 2026-08-15T08:52Z to 2026-08-16T21:12Z
(110 league matches)**, then **v65 at 21:32Z (1 match)** and **v66 from 21:52Z (22 matches, current)**.
Our last game against them was 2026-08-16T19:32Z, i.e. **v61 was their last version we have met and
it is not their current one.** Every behavioural finding here is **LINEAGE evidence**, not a
description of the bot we will be paired against tomorrow. §7 is a cheap v61→v66 diff off the
league's own archived games and it finds one real doctrine change; treat findings that survive that
diff as more likely to transfer.

**Inputs read.**
* `corpus/join.tsv`, `corpus/ladder_games.tsv`, `corpus/league_matches.tsv`
* `corpus/events.tsv` (already-decoded BUILD/DEATH; 5,012 rows for these 50 files, 50/50 covered)
* `corpus/throws.tsv` (already-decoded launcher throws; 918 rows for these 50 files)
* `tools/corpus/replay_autopsy.py` run over all 50 replays — **100 core damage ledgers, `MATCH` on
  100 of 100** (the tool's own self-check: attributed damage must equal summed `UpdateHp` deltas)
* one purpose-written per-turret `FireTurret` census on `tools/replay_census.py` primitives
  (302 turrets) — **validated against the autopsy: its aimed-shot damage reproduces the autopsy's
  attributed damage exactly, 50 of 50 games**
* `tools/cluster_ci.py` for every interval
* incumbent tree read: `bots/_v468kladturbo/{main,eco,raid,doctrine}.py`
* prior art checked so it is not re-derived: `docs/research/OPP-lingling40-profile-2026-08-13.md`
  (their **v40**), `docs/research/REPLAY-STUDY-offensive-gunner-2026-08-17.md`, QUEUE.md rows #7,
  #23, #24, #28, #30, #40, #45, #47, #51, #58, #59, #69, #70, #85, #90, #91, #92.

**Known decoder artefact, stated so it is not mistaken for a finding.** `events.tsv` emits 28 `core`
DEATH rows for us and 22 for them against 26 core-losses and 21 core-wins in `join.tsv` — an
end-of-match cleanup `removeEntity` in a few replays. **No damage claim below uses DEATH counts**;
they all come from the self-checked autopsy ledger.

---

## 1. THE GROUND — WE LOSE THE RACE, WE DO NOT LOSE THE FIGHT

**MEASURED (50 games).**

| | us | them |
|---|---|---|
| core kills | 21 | 26 (+3 wins on `titanium_collected` at r1000) |
| **median kill round** | **r223** | **r129** |
| kills by r300, as a share of ALL 50 games (timely-kill rate) | **38.0%** | **48.0%** |
| first damage to the enemy core | r39 (in 45/50 games) | r33 (in 47/50) |
| **total damage dealt to the enemy core** | **37,296** | **67,296** — ratio **1.80** |
| core HP healed, per game | 1,045.7 | 516.6 |
| builder heal events, per game | 328.5 | 170.3 |
| titanium converted to ammo, per game | 555.3 | 844.7 |
| builder attack events, per game | 42.9 | 88.8 |

Split on game length: **we win 2 of 18 games that end by r140 and 19 of 32 that run past it.**
They are not out-playing us across a whole game — **they finish 94 rounds earlier than we do**, and
the games we lose are the ones that end before our clock runs out. Against `R1000_IS_DEFEAT` and the
`r300` bar this is the only number that matters in the cell.

Our game share, clustered: `42.0% [26.0, 58.0]` (cluster-bootstrap on `match`, 10 clusters).
⚠ **`cluster_ci.py` warns that 10 clusters is below its `EXCLUSION_MIN_CLUSTERS=30` floor and the
coverage error is not conservative in a predictable direction.** Every interval in this study
carries that warning; none of them is used to exclude anything.

### 1.1 `ourver` split (discipline rule 5)

| | games | matches | wins | our sentinels d²<33 / d²≥60 | their ring launchers/gunners per game |
|---|---|---|---|---|---|
| **v140** | 5 | 1 | **0 (0%)** | 5 / 1 | 2.00 / 2.20 |
| **v152** | 45 | 9 | 21 (47%) | 69 / 35 | 1.69 / 1.33 |

⛔ **The v140 cell is one match, all five games lost, all short (r69–r140).** Every per-game count in
it is truncated by game length and it cannot support a per-version claim in either direction.
**Every pooled number in this report is therefore effectively a v152 number** (45 of 50 games) and
should be read that way. Where a v140/v152 difference could matter I say so; I found none that
survives the n=5 caveat.

---

## 2. MEASURED OPENING PROFILE (50 games, `corpus/events.tsv`)

**First-build round (median, and in how many of 50 games it happens at all):**

| entity | THEM | US |
|---|---|---|
| builder bot | r0 (50/50) | r0 (50/50) |
| **conveyor** | **r3 (50/50)** | r9 (49/50) |
| harvester | r7.5 (50/50) | r7 (50/50) |
| sentinel | r25.5 (48/50) | r27.5 (48/50) |
| **launcher** | **r34 (44/50)** | **r165 (3/50)** |
| gunner | r49 (39/50) | r84 (12/50) |
| barrier | r67 (23/50) | r34 (48/50) |

**Builds per game:** harvester 3.38 vs our 5.04 · conveyor 24.02 vs 27.90 · builder 5.80 vs 6.74 ·
sentinel 2.04 vs 2.70 · **gunner 1.78 vs 0.30** · **launcher 1.72 vs 0.06** · **barrier 0.58 vs 6.18** ·
splitter 0 vs 0.

**Siting, `d²` to the ENEMY core (median over all builds of that kind):**

| | THEM | US |
|---|---|---|
| launcher | **5** (84/86 forward; 86/86 at d²≤8) | 458 (n=3) |
| gunner | **4** (71/89 at d²≤8) | 313 (0/15 forward) |
| sentinel | 18 (56/102 at d²<20) | 25 |
| barrier | 5 (n=29) | **4 (303 of our 309 barriers are at d²≤8 of THEIR core)** |

**The one-line reading.** Both teams siege the other's spawn ring, starting at the same round
(median first ring build r34 on both sides). **The kit differs completely: on our ring they plant
86 launchers + 71 gunners + 6 sentinels; on their ring we plant 303 barriers + 24 sentinels and
one launcher.** 92% of what we put on their doorstep is inert 3-Ti wall. 100% of what they put on
ours is a weapon or a machine.

**Their economy is smaller than ours and always has been** (3.38 harvesters/game to our 5.04,
matching the v40 profile's 3–4). Do not spend a leg on it — that was already the v40 conclusion and
v61 does not change it.

---

## 3. HOW THEY ACTUALLY KILL US

**MEASURED, `replay_autopsy.py`, 100/100 ledgers self-checked `MATCH`.**

| damage source | to OUR core | to THEIR core |
|---|---|---|
| **sentinel** | **52,776 (78.4%)** | **37,296 (100%)** |
| **gunner** | **14,518 (21.6%)** | **0** |
| builder melee | **2** (one landed hit in 50 games) | **0** |
| absorbed by a unit standing on the footprint | **0** | **0** |

**Neither side ever pecks a core** (this cell independently confirms the direction of QUEUE #85 from
the other side: their builders make 88.8 attacks per game and put 2 total damage on our core in 50
games — their melee goes into belts and turrets, not the core).

**Everything that scores is a turret, and 78.4% of what kills us is a sentinel.**

### 3.1 The productivity curve — and the control is that it is IDENTICAL on both teams

Per-turret `FireTurret` census, 302 turrets. `alive` = death round − build round + 1, survivors
truncated at `turns`. `core` = shots whose target tile is inside the enemy core's 2×2 footprint.

| who | kind | d²_enemy | n | alive-rnds | shots | core-shots | shots/rnd | **core-shots/rnd** |
|---|---|---|---|---|---|---|---|---|
| us | sentinel | 0–9 | 22 | 1,386 | 573 | 551 | 0.413 | **0.398** |
| us | sentinel | 9–20 | 32 | 2,501 | 792 | 768 | 0.317 | **0.307** |
| us | sentinel | 20–33 | 20 | 1,363 | 530 | 464 | 0.389 | **0.340** |
| us | sentinel | 33–60 | 14 | 2,269 | 336 | 289 | 0.148 | 0.127 |
| **us** | **sentinel** | **≥60** | **36** | **6,426** | **356** | **0** | 0.055 | **0.000** |
| them | sentinel | 0–9 | 6 | 965 | 334 | 286 | 0.346 | **0.296** |
| them | sentinel | 9–20 | 40 | 5,382 | 1,988 | 1,857 | 0.369 | **0.345** |
| them | sentinel | 20–33 | 22 | 2,165 | 864 | 762 | 0.399 | **0.352** |
| them | sentinel | 33–60 | 3 | 278 | 44 | 27 | 0.158 | 0.097 |
| **them** | **sentinel** | **≥60** | **18** | **2,940** | **55** | **0** | 0.019 | **0.000** |
| **them** | **gunner** | **0–9** | **58** | **3,746** | **2,074** | **2,074** | **0.554** | **0.554** |
| them | gunner | ≥60 | 14 | 1,537 | 196 | 0 | 0.128 | **0.000** |
| us | gunner | ≥60 | 13 | 1,182 | 78 | 0 | 0.066 | **0.000** |
| us | gunner | 33–60 / 9–20 | 1 / 1 | 112 / 3 | 9 / 1 | 0 / 0 | — | **0.000** |

**This is the control the playbook asks for and it runs the other way on the same instrument.**
The curve is not a property of our bot or theirs — **inside d²<33 the two teams' sentinels are
equally productive (us 0.361 shots/alive-round pooled, them 0.374)**, and **outside d²≥60 both teams
score EXACTLY ZERO core shots — 36 of our sentinels over 6,426 alive-rounds and 18 of theirs over
2,940, plus 27 gunners over 2,719, and not one core shot between them.** A sentinel's range is
r²=32; d²≥60 is out of range of the only target that scores, for anybody.

**We are not worse shooters. We are worse allocators.**
* Our sentinel fleet spends **6,426 of 13,945 alive-rounds (46.1%)** at d²≥60. Theirs spends
  **2,940 of 11,730 (25.1%)**.
* **13 of our 15 gunners sit at d²≥60 and have fired at an enemy core exactly 0 times in 1,182
  alive-rounds.** Their 58 point-blank gunners fire **0.554 core-shots per alive-round, with a
  core share of 100.0%.**

### 3.2 Exhibit — `06ae9d20-216f-40c0-9a51-0bfea4e39158_game_4` (frostgate 20×20, r277, our loss)

Cores A@(2,9) = us, B@(16,9) = them. Per-turret, decoded:

| turret | built | position | d²_enemy | shots | core-shots | fate |
|---|---|---|---|---|---|---|
| **our** sentinel #22 | r10 | (11,10) | 26 | 10 | **10** | killed r30 |
| **their** sentinel #29 | r12 | (7,9) | 25 | **130** | **129** | **alive at r277** |
| our sentinel #108 | r58 | (3,12) | 178 | 0 | **0** | survived |
| our sentinel #123 | r68 | (4,11) | 148 | 17 | **0** | killed r263 |
| our sentinel #146 | r84 | (1,11) | 229 | 0 | **0** | survived |
| our gunner #162 | r94 | (2,12) | 205 | 6 | **0** | survived |
| their sentinel #321 | r191 | (5,8) | 10 | 42 | **42** | survived |

Our core took **18 damage every second round from r13 to r276** — 3,078 total — while we healed it
+2,574 and lost anyway. **After our one forward sentinel died at r30 we bought four more turrets
(r58, r68, r84, r94) and produced zero core damage with any of them for the remaining 247 rounds.**
Their core took 180 damage total, all of it between r11 and r29.

Second exhibit, same shape: `6f8fcf68-afe1-46b9-8d9e-fe1e30be41ff_game_1` (nordkap, r104, our loss).
Their sentinel at (9,10) built **r10**, d²=16 from our core at (9,6); **our core's first damage lands
r11**, one round later; final ledger sentinel 612 + gunner 154 = 766, us dead at r104.

---

## 4. THE PIECES

Ranked by how much they would plausibly move our kill rate. Each is one behaviour, cited at ≥2 games
with anchors, with the control that must run the other way, and sketched against the incumbent.

### PIECE 1 — **THE POINT-BLANK CORE-SNIPER GUNNER AT d² ≤ 9** ⭐⭐⭐

**MEASURED.** 58 of their gunners sit at d²≤9 of our core. Over 3,746 alive-rounds they fire
**2,074 shots, of which 2,074 (100.0%) land in our core's footprint** — 0.554 core-shots per
alive-round, **14,518 damage = 21.6% of everything that has ever hit our core in this cell**.
Median build round r49, present in 39 of 50 games.

**CONTROL (runs the other way, same instrument, same team).** *Their own* gunners planted at d²≥60
— 14 of them, 1,537 alive-rounds — fire 0.128 shots/round and **0 core shots, ever**. Same bot, same
code, opposite verdict, so the reading is about the SITE and not about gunners. Second control:
*our* 13 home gunners, 1,182 alive-rounds, **0 core shots**. The band is what does it.

**Cost.** Their point-blank gunners live median 35 rounds (mean 72) against their sentinels' median
80 — the offensive-gunner study's "d²<10 halves the gunner's life" is confirmed here. It is still
the best titanium in the cell: **14,518 core damage over 58 gunners = 250 core-HP per gunner**, i.e.
12.5 core-HP per titanium at the 20 Ti base and ~7.8 at a 1.6× scale factor. ⚠ That arithmetic
ignores ammunition (4/shot × 2,074 shots = 8,296 Ti of ammo across 50 games, 166/game) and the
+20% scale each gunner adds — **a prereg must price both, not this line.**

**⛔ NOT COVERED BY QUEUE #90 / #91.** Both target the annulus **20 ≤ d² < 100**, and
`REPLAY-STUDY-offensive-gunner-2026-08-17.md:764` says in terms: *"d² < 20 is the sporks core-sniper
band and a different plank."* This is a second, independent user of that different plank, with a
measured output rate. **`lingling_40h` puts 71 of 89 gunners at d²≤8 and exactly 2 in the 20–100
annulus** — the field-wide annulus finding does not describe this opponent at all, and both
strategies work.

**GREP against the incumbent (`bots/_v468kladturbo`).** We have no forward-gunner path: 15 gunners
in 50 games, 13 at d²≥60, `d2_enemy` median 313, zero forward. The offensive-gunner study already
established the blocking predicate (`d² ≤ 32` plus the pre-scan bail `dsq_core(p, E) > 50`).

**Sketch.** One gunner, cap 1, planted by a raider that is *already standing on the ring* — see
PIECE 2 for why that raider is already there and already spending the money.

---

### PIECE 2 — **CONVERT ONE RING BARRIER INTO THE RING GUNNER: THE MONEY AND THE BUILDER ARE ALREADY THERE** ⭐⭐⭐

**MEASURED.** We build **309 barriers in 50 games and 303 of them are at d²≤8 of THEIR core**
(`d2_enemy` median 4), first at median r34, **4.78 of them already placed by r80**. That is
`raid.py:276`'s spawn-seat seal, and it means **our raider is standing on exactly the tile PIECE 1
needs, at exactly the round PIECE 1 needs, with an action to spend.**

At scale-1 prices 4.78 barriers ≈ 14 Ti against a gunner's 20 Ti base; by r80 in a real game the
scaled ratio is close to 1:1. **PIECE 1 is therefore a SWAP, not an addition** — which is the part
that matters, because every build adds to the single global additive scale factor and a barrier
(+1%) is a fifth of a gunner (+20%)... so the swap is *not* scale-neutral and must be priced as
+19% scale for −4 barriers. State that in the prereg rather than discovering it.

**CONTROL.** Their side of the same ring: 29 barriers total, 0.58/game, first at median r67 — they
spend on the ring too, but on weapons. Our barrier survival on their ring is 210/303 (69%) — the
barriers are not being destroyed, so their titanium is not being "recycled" into denial value; it
sits there.

**⛔ WHAT THIS IS NOT.** It is **not** "stop sealing". `PLAY_DEFENCE` aside, s30 measured
`barrier-seal-off` at 399/1024 — removing the seal cost us. The claim is about **the marginal ring
barrier beyond the seal**, and the prereg must hold seal count constant.

**GREP.** `raid.py:276` builds barriers to seal a free seat on the spawn ring; QUEUE #7's grep says
barriering an *ore* tile a forward gun covers is not shipped. Nothing in the tree converts a ring
seat into a turret site.

---

### PIECE 3 — **46% OF OUR SENTINEL ALIVE-ROUNDS ARE PARKED OUT OF RANGE OF THE ONLY TARGET THAT SCORES** ⭐⭐

**MEASURED.** 36 of our 124 decoded sentinels sit at d²≥60 of the enemy core. Over **6,426
alive-rounds they fired 356 shots — 0.055/round — and 0 of them at a core.** By rank within game:
the 1st home sentinel fires 0.064/round (20 games, 4,087 alive-rounds), the 2nd 0.058 (9 games), the
3rd 0.012, the 4th+ 0.015.

**CONTROL (runs the other way).** The same measurement on THEIR home sentinels: 18 turrets, 2,940
alive-rounds, 0.019 shots/round, 0 core shots. **Both teams' home sentinels are silent** — so the
zero is a property of the band, not of our targeting code. And inside d²<33 our sentinels shoot at
0.361/round against their 0.374, i.e. **we are within 4% of them wherever we are in range.**

**⛔ THIS IS NOT "DELETE HOME TURRETS".** s30 measured `home-turrets-off` at 433/1024 — a real
negative; removing defensive behaviour cost us. The finding is narrower and it is the honest one:
**the home sentinel's OFFENSIVE contribution is measured at exactly zero, so it must be justified on
defence alone, and the SECOND home sentinel is as silent as the first** (0.058 vs 0.064 shots/round).
The candidate is the marginal home sentinel, not the first one, and it carries
`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`.

**Anchor.** `06ae9d20…_game_4`: our r58 / r68 / r84 / r94 turrets, d² 178 / 148 / 229 / 205,
0 core shots between them in 247 rounds (§3.2). `f981275c…_game_5`, `7e1767c0…_game_5` show the
same post-forward-death fallback into home siting.

---

### PIECE 4 — **AN ENEMY LAUNCHER IS NOT A THREAT TYPE, SO IT LIVES ON OUR SPAWN RING UNTIL THE GAME ENDS** ⭐⭐

**MEASURED.** They plant **86 launchers, 84 of them forward, `d2_enemy` median 5** — i.e. on our own
spawn ring — at median round 34 (earliest r6), in 44 of 50 games. Survival of their kit inside
d²≤8 of our core:

| their ring kit | built | **we killed** | survived to end | median life |
|---|---|---|---|---|
| **launcher** | **86** | **3 (3.5%)** | **83** | 57 |
| gunner | 71 | **31 (43.7%)** | 40 | 30 |
| sentinel | 6 | 1 | 5 | 102 |
| barrier | 17 | 1 | 16 | 132 |

**CONTROL — the gunner, and it must run the other way, which it does.** Both sit in the *same* band
(d²≤8), both are enemy buildings orthogonally reachable by the builders we already have standing
there, both are cheap HP (gunner 25, launcher 30). **We kill the one that shoots at 43.7% and the one
that does not shoot at 3.5%.** The discriminator is "does it emit damage", not "can we reach it".

**And a second control that makes the number worth acting on: when we DO kill one, it is never
rebuilt — 0 of 3 replaced.** Their ring *gunner* replacement latency is median **69 rounds**
(23 of 31 replaced) and ring *sentinel* **11 rounds**. ⭐ **This is a real v40→v61 change: the v40
profile measured siege-turret replacement at 1–2 rounds** (`OPP-lingling40-profile-2026-08-13.md`
fact 3), i.e. counter-battery was futile then and is not now.

**CODE ANCHOR — the mechanism is one frozenset.**
* `main.py:58` — `CORE_THREAT_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))`.
  Used at `main.py:249` (the core's own threat sense) and `main.py:507` (the builder's).
  **An enemy LAUNCHER inside d²≤8 of our core never sets `SLOT_UNDER` / `SLOT_THREAT`.** The only
  other triggers are an enemy *builder* within d²≤16 (which walks away after the build) and our core
  *losing HP* — and a launcher deals no damage. **It is invisible to our "we are under attack"
  latch by construction.**
* `doctrine.py:1488` — `LOKI_QUIET_ON = True` (*"no builder melee: no core peck, no siphon hit, no
  counterbattery"*), which makes `_sabotage_prio` (`main.py:635`) return `False` unconditionally.
* The one path in the tree that ranks a LAUNCHER **above** turrets is `_raid_peck`
  (`raid.py:631`, `pr = 2` vs turrets' `pr = 3`) — and it is both quiet-gated (`raid.py:348-349`,
  `not LOKI_QUIET_ON`) and **raid-side only**: it is called at THEIR core, never at ours.
* Our turrets rank it fourth: `TURRET_PRIO` (`main.py:52`) puts LAUNCHER at 4, behind CORE, SENTINEL,
  GUNNER, BUILDER_BOT.

⇒ **In the live tree there is no code path by which an enemy launcher standing on our own spawn
ring can be attacked.**

⚠ **HONEST DOWNGRADE, AND IT IS WHY THIS IS RANKED 4TH AND NOT 1ST.** Splitting the 50 games on
*"did they plant a ring launcher by r50"* gives **42.1% (19 games, 9 clusters) vs 41.9% (31 games,
10 clusters) — a flat null.** Presence of the farm does not predict our loss in this cell. See §5
and §6.R3: the asymmetry is real and the mechanism is real, but its cost is not shown here.

---

### PIECE 5 — **THE FIRST SENTINEL IS THE WHOLE OPENING, AND IT IS A RACE WE ARE LOSING BY THREE ROUNDS AND SEVEN d²** ⭐

**MEASURED.** Their first sentinel lands at median **r25.5** (48/50 games) at `d2_enemy` median
**18**; ours at **r27.5** (48/50) at `d2_enemy` median **25**. First damage to our core follows at
median **r33**; to theirs at **r39**. In the two §3.2 exhibits their first sentinel is up at r10 and
r12 and first blood lands at r11 and r13.

Given §3.1's curve, the 25→18 siting gap is worth roughly nothing on shots/round (0.340 at 20–33 vs
0.345 at 9–20 — flat), so **the siting half of this is a null and I am reporting it as one.** What is
not flat is **survival of the first forward sentinel**: in `06ae9d20…_game_4` ours dies at r30 after
10 shots while theirs lives 265 rounds and fires 130. Across the cell, our sentinels at d²<33 hold
5,250 alive-rounds against their 8,512 — **62%** — with a *lower* death rate (27.4% of ours are
killed vs 37.3% of theirs). The alive-round deficit is therefore mostly **built later and fewer
forward**, not **killed faster**.

**Relation to QUEUE #92** (decouple the first sentinel from the eco clock): #92's premise holds
here — but **the binding deficit in this cell is the SECOND through FOURTH forward sentinel, not the
first**, which arrives within 2 rounds of theirs. Worth an amendment to #92 rather than a new row.

---

## 5. THE `#59` COST CUT, RUN ON THE POPULATION IT ASKED FOR — AND THE NULL SURVIVES

QUEUE **#59** ("DON'T GET FARMED") says in terms: *"the row earns a build only if the
length-controlled r0-150 metric finds a cost that the raw dose hides"*, and its own cut found no
cost, partly on the grounds that *"we BEAT both named users (… LingLing40 52.0%)"*. **This cell is
the harder population: `lingling_40h` v61, current-lineage bots, and we are at 42.0%.** I ran the
metric it specified.

**MEASURED.** 918 EXILE throws in 50 games — **100% of them theirs on our builders, 0 of ours on
theirs.** 94 distinct victims; median 4 throws per victim; **815 of 918 close as `RETHROWN`**, i.e.
the same builder comes back and is thrown again. **796 of 918 land on a map-border tile.**

**The pickup site is our own doorstep: `d2_before` (victim to OUR core) median 5, and 594 of 918
(64.7%) at d²≤8.** This is a spawn-ring farm, not a base-defence eviction.

**FIELD CONTROL, and it separates the two cleanly.** Same column, every opponent in the archive that
throws our builders at all:

| opponent | throws on us | **median d²(victim → OUR core)** | share at d²≤8 |
|---|---|---|---|
| Memtrace | 11,803 | 45 | 1.6% |
| Focalground | 9,543 | 72 | 1.2% |
| Powered by SmartFridge | 2,364 | 121 | 1.4% |
| gsxWins | 1,259 | 202 | 1.4% |
| OopsGotYourElo | 964 | 58 | 0.0% |
| Coreflood | 464 | 65 | 0.0% |
| Lunds Stallions | 1,845 | 13 | 30.8% |
| **`lingling_40h` (all versions)** | **2,124** | **10** | **37.7%** |
| **`lingling_40h` v61 (this cell)** | **918** | **5** | **64.7%** |

Ten of fifteen throwing opponents come out the other way — their launchers sit at their OWN core and
evict our raiders. **`lingling_40h` v61 is the field's most spawn-ring-directed launcher user, and
it is more so than its own earlier versions.** The instrument distinguishes the two cases; it is not
a constant column.

**Length-controlled metric (#59's own specification):**
* **12.51 evictions per 1,000 of our builder-rounds in r0–150** (500 throws over 39,982 builder-rounds,
  builder-rounds integrated from BUILD/DEATH).
* **54.5% of throws land before r150; median throw round r134.5.** #59's population read 39.9% before
  r150 and a median of r209. **On this cell the dose has moved forward of the decision window.**
* Split by outcome: 15.55 per 1,000 in games we lost vs 10.61 in games we won.

**VERDICT: #59's NULL SURVIVES.** The outcome split is inside the noise at 10 clusters, and the
cleaner test — **presence of a ring launcher by r50 — is a dead flat null (42.1% vs 41.9%)**. The
farm is large, one-directional, unanswered and permanent, and this cell still cannot show it costs
us games. **PIECE 4 stands on the code asymmetry and the 0/3 non-replacement, not on this cut.**

**Anchor for the treadmill, because the size is worth seeing once.**
`f981275c-7586-413a-9202-313496923404_game_3` (glacierkeep, r1000, our loss on `titanium_collected`):
**our builder #6 is thrown 175 times between r37 and r999, every single throw landing on the same
one border tile, 174 of them closing `RETHROWN`.** One of our builders spent 962 rounds on a
treadmill in a game decided on delivery volume.
Second anchor: `78f6f9bb…_game_2`, our builder #6 thrown 88 times, r38–r309.

---

## 6. REFUTED — RETAINED SO NOBODY RE-DERIVES THEM

**R1. "They body-block their own core footprint better than we do."** I hypothesised this off the
schema's damage-target law (a shot landing on a tile occupied by a unit hits the unit, not the core)
after my two decoders appeared to disagree by ~40%. **MEASURED: `absorbed` is empty in 100 of 100
core ledgers — zero absorption on either side in 50 games.** The apparent disagreement was a defect
in *my* autopsy-output parser (`(\d+)` failed to match `hp end -4`), not a real effect; once fixed,
the aimed-shot census and the self-checked ledger agree **exactly, game by game, 50 of 50**.
**Nobody in this cell defends a core with a body.** (Whether that is because they cannot — buildings
may block the tile — I did not establish; see §8.)

**R2. Crash-induction is being attempted on us and does not work.** **796 of 918 throws land on a
map-BORDER tile** — the exact LOKI-14 geometry, where the victim's own off-map query raises and the
engine destroys it permanently. **It does not fire on us: 19 victims died, and 0 of the 19 carry the
`vhp == 0` no-HP-event crash signature.** All 19 are combat deaths. Positive control that the
detector *can* fire: **745 `DIED`+`vhp==0` rows exist in `corpus/throws.tsv` archive-wide** out of
25,811 `DIED` rows. Our `eco.py` guard is holding. **This is a road already closed, re-confirmed;
do not spend a leg proving they cannot crash us.**

**R3. "The launcher farm is why we lose to them."** Presence of a ring launcher by r50:
**42.1% vs 41.9%.** Flat. (Interval unusable at 9–10 clusters; the point estimates are what is being
reported, and they are identical.)

**R4. "Their siege turrets are replaced in 1–2 rounds, so counter-battery is futile."** True of
their **v40** (`OPP-lingling40-profile-2026-08-13.md` fact 3, latencies `[1,1,1,1,1,2,2,5,…]`).
**FALSE of v61: ring gunner replacement latency median 69 rounds, ring sentinel 11, ring launcher
never (0 of 3).** Killing a v61 siege turret buys real time. This is a version delta, and it raises
the value of every counter-battery plank that was priced against v40.

**R5. "The field's productive gunner band (20 ≤ d² < 100) describes this opponent."** It does not:
**71 of 89 of their gunners are at d²≤8 and exactly 2 are in the 20–100 annulus**, and the
point-blank ones fire at 0.554 core-shots/alive-round with a 100.0% core share. The annulus finding
and this one are different planks aimed at different targets (belt attrition vs the core itself),
and `REPLAY-STUDY-offensive-gunner-2026-08-17.md:764` already says so.

**R6. "Their opening tempo is the story."** Their first conveyor lands at r3 in 50/50 games against
our r9, and their first harvester at r7.5 against our r7 — so they lay trunk before ore and we do
the reverse. **But their economy is strictly smaller than ours** (3.38 harvesters and 24.02
conveyors per game to our 5.04 and 27.90), and they win anyway. Same conclusion as the v40 profile:
**do not spend a leg on their economy.** Reported as a measured opening fact, not a piece.

---

## 7. v61 → v66: THE CHEAP DIFF OFF THE LEAGUE'S OWN GAMES

We have never played their v66. **`replay_archive/` covers 1 of their 23 v65/v66 league matches —
5 games, `f0104d6a-4410-427b-8524-5cfd0555bbae`, vs `opensverige - plan B`, 2026-08-16T23:52Z.**
It also covers **4 v61 matches against teams that are not us** (0033, Clankers, HTTP 418,
`kladde chatte tville`), 20 games, which gives an opponent-independent v61 baseline. Profiles below
are from `corpus/events.tsv`, no download.

**STABLE across v40 → v61 → v66 (these are the findings most likely to transfer):**
* First harvester r4–r12, first conveyor r3–r6, **zero splitters in every group**.
* **Early forward sentinel**: v61 r25.5 at d²18, v66 r20 at d²16.
* **Point-blank gunner at the enemy core**: v61 `d2_enemy` median 4–5, v66 median 5 (individual
  builds at d² 8, 5, 4, 1, 5). The core-sniper doctrine is intact.
* **Launcher volume**: 86 throws in the 5 v66 games (17.2/game) against 18.4/game on v61 — unchanged.

**CHANGED, and it is the one real doctrine move:**

| | v61 vs US (50 g) | v61 vs 4 other teams (20 g) | **v66 vs plan B (5 g)** |
|---|---|---|---|
| launchers | 86 | 64 | 6 |
| **forward (d²_enemy < d²_own)** | **84/86** | **64/64** | **0/6** |
| `d2_own` median | 423 | 369 | **4** |
| `d2_enemy` median | 5 | 5 | **150** |
| pickup `d²`(victim→own core) median | 5 | — | **221** |
| pickups at d²≤8 | 64.7% | — | **2.3%** |

**v61 planted 150 of 150 launchers forward, on five different opponents' spawn rings. v66 plants 0
of 6 forward — they are at their own core, and their throws now evict the opponent's raiders instead
of farming the opponent's spawns.**

⚠ **LIMITS, and they are severe: 5 games, ONE opponent, 6 launchers.** One of those five maps has
cores ~4 tiles apart, where "home" and "forward" coincide, so the effective sample is 4 games.
An adaptive siting rule (go home when the opponent raids hard) would produce the same table without
any version change, and `opensverige - plan B` raids differently from us. **Do not treat "v66 stopped
spawn-farming" as established.** What the diff *does* establish is that **PIECES 1, 3 and 5 rest on
behaviour that is stable across three of their versions, while PIECE 4's subject may have moved.**

---

## 8. WHAT I COULD NOT MEASURE, AND WHY

1. **Turret FACING.** I did not decode the direction field on `placeEntity`, so inside the productive
   band (d²<33) I cannot separate "sited so the core is not in the line" from "sited fine but has no
   target". Outside d²≥60 this does not matter — range alone (r²=32) explains the zero — but every
   in-band claim in §3.1 is about *outcomes*, not about facing.
2. **Who kills their ring turrets.** I have that we killed 31 of 71 ring gunners, but not whether
   our home sentinels (356 non-core shots) or our builders (42.9 attacks/game) did it. Without that,
   PIECE 3's defensive-value half is unpriced and the row cannot claim the home sentinel is idle —
   only that it is offensively silent.
3. **Ammunition over time.** `replay_autopsy` reports total titanium converted (us 555.3/game, them
   844.7) but I did not reconstruct the per-round ammo balance. So I cannot say whether our
   sentinels' 0.361 shots/alive-round inside the band is reload-limited, target-limited or
   **ammo-starved** — and ammo starvation would be a completely different plank from siting.
4. **Whether their launcher destinations are chosen or incidental.** In one game the same victim
   went to the same single border tile 175 times, which looks deliberate; I did not compute the
   distribution of distinct destinations per launcher across the cell.
5. **Any interval that excludes anything.** Ten matches is below `cluster_ci.py`'s 30-cluster floor
   and the tool says the coverage error is not conservative. Every split in this study is reported as
   point estimates. **The two nulls in §5 and §6.R3 are FAIL-TO-EXCLUDE claims and have not been
   restated as exclusions** (per the CLAUDE.md direction clause), so they close nothing on their own.
6. **v66 against us.** Zero games. §7 is 5 games against one other team and cannot be more than
   suggestive.
7. **Why the v140 arm went 0/5.** One match, all short losses. Nothing in it separates from v152
   at that n, and I did not attempt to.

---

## 9. SUMMARY FOR THE LEDGER

`2026-08-17  lingling_40h  61  50  docs/research/REPLAY-STUDY-lingling40h-2026-08-17.md`

**The one-sentence answer to "what do they do that beats us":** they put **every** turret inside
range of our core — a sentinel at d²9–20 by r25 and a gunner at d²≤8 by r49 — and they never buy a
turret that cannot shoot a core, while **46% of our sentinel alive-rounds and 87% of our gunners sit
at d²≥60 where the measured core-shot rate is exactly zero for both teams**. They kill at median
r129; we kill at median r223.
