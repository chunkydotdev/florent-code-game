# REPLAY STUDY — `lingling_40h` **v86**, 90 rated games, our v168/v174/v176/v179

**Move-mining loop, step 2 (STUDY).** Method contract: `docs/research/PLAYBOOK-move-mining-2026-08-16.md` §3.
Fresh replay-study agent, no inherited session context beyond the named inputs. Nothing committed by the
agent; **no bot edited, no match fired, no submission or activation touched, zero platform writes, zero
replay downloads** (all 90 replays were already in `replay_archive/`).

---

## PROVENANCE

**Clock.** `date -u` in the analysis shell: **2026-08-22T11:36:00Z**. Repo HEAD at study time:
`42f98b7adb5a13ce49d81f530e20a933456fbeef` (2026-08-22T13:27:33+02:00).

**Ground.** Opponent `lingling_40h`, **their version 86**. **All 90 archived rated ladder games we have
against that version** — 18 matches, 23 distinct maps. Selector:
`corpus/ladder_games.tsv` filtered on `opp == 'lingling_40h' AND oppver == '86'`.
Trigger ground (`tools/move_miner.py`, 2026-08-22 ~11:15Z): 90 unstudied MODERN games, our modern share
53.0% (n=100), their rating 1834 vs our 1797 (gap +37, a 5-0 pays +17.68 — inside the admissible band).
The ledger's last coverage of this opponent is their **v61** (25 versions back).

**Input files read (complete list, verbatim).**
* `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (method)
* `docs/research/REPLAY-STUDY-lingling40h-2026-08-17.md` (their v61 — **lineage only**, every carry-over
  tested with a measured v86 cut below)
* `docs/research/OPP-lingling40-profile-2026-08-13.md` (their v40 — same caveat)
* `docs/research/corpus-howto.md`, `tools/replay_schema.md`
* `corpus/join.tsv`, `corpus/meta_join.tsv`, `corpus/ladder_games.tsv`, `corpus/league_matches.tsv`
* `tools/corpus/replay_autopsy.py`, `tools/replay_census.py`, `tools/crash_census.py`
* `QUEUE.md` (exclusion list — §10 maps every piece onto an existing row or says why it is new),
  `PROGRAMME.md` doctrine as carried in `CLAUDE.md`
* `bots/_v622nestfall/` — **NOT read as a code anchor**, deliberately, and this matters: the 90 games in
  this pool were played by **Mjolnir v168/v174/v176/v179 (x3r0's holder line), not by the Skalman dev
  line that `_v622nestfall` heads.** Every "US" row below is a statement about **Mjolnir's behaviour**.
  No GREP against `_v622nestfall` is offered, because the tree that produced this behaviour is not that
  tree; the pieces in §10 carry a "GREP OWED" note instead of a fake pass.
* Decode harness: purpose-written single-pass event miner on `tools/replay_census.py` primitives
  (`fields`, `read_pos`, `parse_entity`, `scalars`, `parse_update_hp`) — no hand-rolled protobuf.

**⛔ VERSION BOUNDARY — and unusually for this corpus, it is clean.**
`corpus/league_matches.tsv` (authority on their timeline) has **v86 running 2026-08-20T09:32:59Z →
2026-08-22T11:01:10Z, 203 league matches**, with four brief prototype activations interleaved and rolled
back: **v88 (11 matches, 2026-08-20T15:52→19:12Z), v89 (2, 08-20T22:12→08-21T05:12Z), v90 (1,
08-21T21:41Z)**, plus a one-match v85 before it. **v86 is their standing holder and it is still live at
the last league row.** All 90 games in this pool are v86 on **two independent surfaces**:
`ladder_games.oppver == 86` and `meta_join.teamAVersion/teamBVersion == 86`, agreeing 90/90. **This is a
single-version pool, not a silently mixed one.** (We separately hold 5 rated games against their **v88**;
they are NOT in this pool and are not analysed here.)

**Population, denominator, clock, inline.** 90 rated ladder games · 18 matches · 23 maps · one opponent
version (v86) · our side v176 (60), v168 (20), v174 (5), v179 (5) · created 2026-08-20T14:52:59Z →
2026-08-22T10:41:10Z.

---

## 0. INSTRUMENT VALIDATION — RUN BEFORE ANY HEADLINE NUMBER, AND DRIVEN BOTH WAYS

**0.1 Seat.** `corpus/ladder_games.seat` is the WINNER's side, not ours (corpus-howto TRAP 7), and
`join.our_team` / `meta_join.us_side` / `ladder_games.won` all descend from the same `winnerSide`, so
cross-checking them is circular. **Our seat here is derived from the platform's own TEAM NAMES**
(`meta_join.teamAName/teamBName == 'OpenSverige'`), which is not winner-derived. It covers 90/90 and
agrees with `us_side` 90/90. Split: **seat A 45, seat B 45.**

**0.2 The reproduction, and the direction that must fail.** Decoding each replay independently and
predicting the `ladder_games.tsv` cells:

```
TRUE    seat: won 90/90   cond 90/90   turns 90/90
FLIPPED seat: won  0/90   cond 90/90   turns 90/90      <- the discriminating direction
```

The `won` column is not constant (49 wins / 41 losses), and the in-replay `winner` field is not constant
(46 team-B / 44 team-A), so the check has power in both directions; flipping the seat drives it to
**0/90**. `rounds - turns == 0` in 90 of 90 (no off-by-one).

**0.3 End-to-end geometry check (the schema's own cheapest one).** `DistributeResources` moves landing
on a Core footprint × 10 must equal that team's final `Player.titaniumCollected`:
**180 of 180 team-sides exact.** This validates footprint geometry, delivery detection and the field-4
decode simultaneously.

**0.4 CONTENT-DUPLICATE SHARE (required by the enumeration procedure).**
* **Byte-identical games: 0 of 90** (90 distinct sha256).
* **Structural-fingerprint duplicates** (map dims + wall count + the FULL ordered build sequence
  `(round, team, kind, x, y)` + round count + winner): **2 of 90 = 2.2%**, one pair —
  `8d9b178c-4d62-4b5c-b3c0-829262f7a09c_game_2` and `cc601b2f-a5e6-4f05-8af7-9f7f433cde14_game_5`
  (skald, our v176, seat B, 83 rounds, 45 builds, identical build stream; the files differ by 33 bytes,
  which is `BotOutput.execTimeUs` noise). **The pool is NOT duplicate-heavy** — nothing like the 17.3%
  found in BC's v47 field pool. But it is not zero either, and it is a direct symptom of §6's
  determinism finding.
* Same `(map, ourver)` cell repeats: 55 excess games of 90. Reported, not corrected for beyond the DEFF
  below.

**0.5 Intervals.** Cluster enumeration for this pool: **MATCH** binds (exactly 5 games per match, 18/18
matches). **OPPONENT** is fixed by construction (one opponent), so the applicable rated constant is the
**within-opponent** one, **DEFF = 1.366**. **MAP** does not compound with MATCH here — `(match, map)`
cells holding more than one game: **0 of 90** — so per-map cells carry no match clustering, but they are
tiny and are reported as **point estimates only**. **CONTENT-DUPLICATE** measured at 2.2% (§0.4), left
uncorrected and declared.
⇒ Pooled share **54.4% (49/90), ±12.0pp at DEFF 1.366 → [42.4, 66.5]**. **18 clusters is below
`cluster_ci.py`'s 30-cluster floor, so no claim in this study excludes anything on an interval.**

---

## 1. THE GROUND — WE ARE NO LONGER LOSING THE RACE, WE ARE LOSING SPECIFIC MAPS

**MEASURED (90 games, this cell).**

| | us (Mjolnir v168/174/176/179) | them (v86) |
|---|---|---|
| game share | **49/90 = 54.4%** [42.4, 66.5] | 45.6% |
| core kills | 48 | 39 |
| `titanium_collected` finishes | 1 win, 2 losses | — |
| **median kill round** | **r197.5** | **r200** |
| kills by r300 as a share of ALL 90 games (**timely-kill rate**) | **40/90 = 44.4%** | **33/90 = 36.7%** |
| games running past r300 | 17 of 90 | — |
| games reaching r1000 | 3 of 90 | — |
| core damage dealt (turret+melee ledger) | 51,804 (sentinel 51,804 · gunner 0 · melee 0) | 60,224 (**gunner 31,514** · sentinel 28,710 · melee 0) |
| titanium converted to ammo | 423.1 /game | 728.3 /game |
| builder attack events | 64.8 /game | 107.0 /game |
| builder heal events | 188.5 /game | 115.7 /game |
| titanium delivered to core (= `titanium_collected`) | median 775 /game | median 930 /game |

**⭐ THE LINEAGE HEADLINE: the race gap closed.** v61 (50 games, our v140/v152): our share **42.0%**,
our median kill **r223**, theirs **r129**, their timely-kill rate 48.0% against our 38.0%.
v86 (90 games, our v168–v179): our share **54.4%**, our median kill **r197.5**, theirs **r200**, our
timely-kill rate **44.4%** against their **36.7%**. **Both the share and the kill clock moved in our
favour, and the larger move is theirs slowing by ~70 rounds, not ours speeding up by ~25.** ⚠ Two
versions changed at once (their v61→v86 and our v152→v176 line change, which is also a change of BOT
LINEAGE, not just version) — **this is collinear and no causal attribution is available from this cell.
INFERENCE at best; both explanations fit.**

**⚠ Neither side is inside the programme's clock.** Our median kill r197.5 is inside r300 but our
**timely-kill rate is 44.4%** — i.e. **55.6% of games against this opponent do not end in a core kill by
r300**. Against `R1000_IS_DEFEAT` and the r300 bar, this cell is a coin-flip we are winning slightly, not
a cell we are killing.

---

## 2. v61 → v86: THE MEASURED CONTRAST (continuity was TESTED, not assumed)

Every row below is the same measurement run on both cells. **v61 column = the banked study's numbers;
v86 column = measured here.**

| behaviour | v61 (50 g) | **v86 (90 g)** | verdict |
|---|---|---|---|
| launchers built | 86 (1.72/g) | **129 (1.43/g)** | volume stable |
| **launcher siting: forward (d²_enemy < d²_own)** | **84/86 = 98%** | **1/129 = 0.8%** | ⭐ **REVERSED** |
| launcher `d²_enemy` median | **5** | **377** | reversed |
| launcher `d²_own` median | 423 | **4** | reversed |
| **their throws on our builders** | 918 (18.4/g), **64.7% picked up at d²≤8 of OUR core** | **2,011 (22.3/g), 0% at d²≤8 of our core; median d²(victim→OUR core) = 317** | ⭐ **the spawn-ring FARM is gone; it is now RAIDER EVICTION** |
| gunners at d²≤8 of our core | 71 of 89 (80%) | **63 of 461 (14%)** | share collapses, **absolute count is stable** |
| point-blank gunner core-shots/alive-round | 0.554 | **0.766** | ⭐ **rate UP 38%** |
| their first sentinel (median round) | r25.5 (48/50) | **r24 (74/90)** | stable |
| their first gunner (median round) | r49 (39/50) | **r17 (83/90)** | ⭐ **32 rounds earlier** |
| their first conveyor / harvester | r3 / r7.5 | **r6 / r4** | ore-first now, trunk-first before |
| their harvesters per game | 3.38 | **3.41** | stable |
| their ring-**sentinel** replacement latency after we kill it | 11 rounds | **median 1 round, 59% replaced** | ⭐ back to the **v40** figure (1–2 rounds) |
| their ring-**gunner** replacement latency | 69 rounds (23/31) | **median 56 rounds, 27% replaced (n=11)** | stable-ish |
| **their turret self-removal (no damage, no adjacent friendly builder)** | not measured | **541 in 90 games (6.0/game), in 88/90 games** | ⭐ **NEW — §3** |
| their CPU timeouts (`botOutput.tled`) | not measured | **750 turns in 25/90 games; ours 0** | ⭐ **NEW — §8** |

**⛔ CONSEQUENCE FOR THE BANKED v61 STUDY:** its **PIECE 4** ("an enemy launcher is not a threat type, so
it lives on our spawn ring until the game ends") and its **§5 / R3** launcher-farm cuts describe a
behaviour **this opponent no longer performs**. The v61 study's own §7 flagged exactly this as
"may have moved" off 5 v66 games against another team; **it has moved, and this is the 90-game
confirmation.** The v61 study's **PIECE 1** (point-blank core-sniper gunner) is the one that survives and
strengthens.

---

## 3. ⭐⭐⭐ THE RELOCATING DISPOSABLE GUNNER — THEIR HOME DEFENCE IS A TURRET THAT MOVES BY BEING REBUILT

**MEASURED.** Over 90 games they build **461 gunners and 293 sentinels**. **368 of the gunners and 244 of
the sentinels are removed before the game ends.** Of those removals, **350 gunners (95.1%) and 191
sentinels (78.3%) carry NO `updateHp` event in the entity's entire life** — the `tools/crash_census.py`
"crash_candidate" wire signature. **541 such removals across 90 games = 6.0/game, present in 88 of 90
games.** Median life of a self-removed home gunner: **8 rounds** (sentinel 6).

**They are not being killed, and they are not being torn down by a builder.** Four controls, each of
which produces the opposite verdict on data where it must:

1. **DAMAGE.** Their **buildings-only** removals — barrier 0/77, conveyor 0/170, harvester 0/9 — carry an
   HP event in **100%** of cases. So "no HP event" is not a decoder artefact that fires everywhere; the
   channel discriminates. (Our side: barrier 0/751, conveyor 0/284, harvester 0/157 — same.)
2. **`destroy()` REQUIRES AN ORTHOGONALLY ADJACENT FRIENDLY BUILDER.** Reconstructing every builder bot's
   tile per round from `placeEntity` + `moveBuilderBot`:
   **⭐ POSITIVE CONTROL that the detector CAN fire — OUR OWN launchers.** Mjolnir builds **358 launchers
   (median build round r5)** and self-removes 197 of them with no damage at **median life 1 round**;
   **187 of 197 = 94.9%** have a friendly builder orthogonally adjacent in the removal window, against
   **5 of 84 = 6.0%** for our launchers that died to damage. **A 16× separation. That is what a
   `destroy()` looks like on this instrument.**
   **THEIR turrets do not look like that: 143/350 = 40.9% (gunner) and 69/191 = 36.1% (sentinel) — flat
   against their own DAMAGE-death background of 38.9% and 34.0%.**
3. **MATCHED within-turret control (the strongest form).** For each self-removed turret, adjacency at the
   removal round vs adjacency at a **random other round of that same turret's life**:
   `THEM gunner nodmg — AT_REMOVAL 40.5% vs RANDOM_LIFE 55.7% (n=348)`;
   `THEM sentinel nodmg — 32.9% vs 57.6% (n=170)`.
   **Adjacency at the removal round is LOWER than baseline.** A `destroy()` explanation requires it to be
   ~100% and certainly higher than baseline. **Refuted.**
4. **FIRING.** **0 of 346** self-removed home gunners fired in their final two rounds, against **7 of 13
   (54%)** for their forward gunners that died to damage. The turret goes quiet, then vanishes.

**⇒ WHAT IT IS.** On the wire, `self_destruct()`, `destroy()` and an uncaught exception are all a bare
`removeEntity` with no preceding `updateHp` (`tools/crash_census.py` docstring). `destroy()` is refuted
above. **What remains is a SELF-removal: `self_destruct()` by the turret itself, or an uncaught exception
in its `run()`.** The regularity argues hard for the former — **0/346 die mid-burst, median life is a
tight 8 rounds, and 81% are followed by a new home gunner** — a crash would not be that tidy. **Labelled
INFERENCE; the two are not separable from replay bytes, and this study does not separate them.**

**⇒ WHAT IT IS FOR — the relocation, MEASURED.** For the 346 self-removed **home** gunners (d²_enemy>32):
* a new home gunner appears afterwards in **281 cases (81%)**,
* **median 15 rounds** later,
* **median d² = 10** from the vacated tile, **93% on a DIFFERENT tile**, 42% within d²≤8 of it.

**And the fleet is not idle while it lives.** Their home gunners (d²≥60 band) fire **5,447 shots over
9,556 alive-rounds = 0.570 shots/alive-round** — against **our** home sentinels' **0.013** and our home
gunners' **0.060**. **Zero of those 5,447 shots hit a core** (engine identity — gunner range r²=13), so
the shots are landing on our raiders, our ring barriers and our belts.

**⭐ THE READING.** `rotate()` costs 10 Ti and a cooldown and only turns a gunner in place. **They do not
rotate: they demolish and rebuild one tile over, ~4.1 home gunners per game, at a median cadence of
8 rounds up / 15 rounds down.** The by-product is that the **global additive cost scale is refunded on
every teardown** — this is exactly the mechanism `QUEUE #27` names ("destroy our own entities to refund
their contribution to the global additive cost scale"), being run continuously by a 1834-rated opponent
as its **primary base-defence doctrine**.

**⚠ SCALE ARITHMETIC — HONESTLY DOWNGRADED.** I built a titanium-tape scale estimator (single-build
rounds, no ammo conversion, passive corrected) and tested it against two competing predictions:
`PRED_LIVE` (destruction refunds) vs `PRED_EVER` (it does not). On the **discriminating subset where the
two differ**: THEM `LIVE 21.1% vs EVER 6.1%` (n=888), US `LIVE 34.1% vs EVER 8.7%` (n=2,211).
**LIVE beats EVER 3–4× in both arms, which is the right direction** — but an exact-match rate of 21–34%
is not a validated instrument (deliveries into the core contaminate the same delta), **so no absolute
scale figure from this study should be quoted.** The refund direction is already engine-established in
`CLAUDE.md`; this cut only fails to contradict it.

**ANCHORS (≥2 games, file + round).**
* `12c81217-1f85-4c5a-b7f7-e205ec32c739_game_1` (midgard, r259, our win, our v176, we are seat B; their
  core at (2,2)). Their home turret sequence, decoded: sentinel (2,0) r24→r34 · sentinel (2,4) r24→r39 ·
  gunner (5,3) r33→r41 · gunner (6,3) r43→r51 · gunner (0,3) r56→r67 · gunner (1,3) r63→r72 · sentinel
  (6,0) r73→r81 · sentinel (4,8) r95→r103 · gunner (1,4) r104→r117. **Nine home turrets, every one
  removed with no HP event, each after 3–7 shots.** Meanwhile their forward gunner at **(26,25) — one
  tile off our core at (26,26) — built r122, fires 136 shots and is never removed.**
* `80fcf20c-8f72-4217-9e0b-e010d8d1509d_game_2` (fimbulwinter, r1000, our loss, v176): **32** no-damage
  turret self-removals in one game.
* `619796f0-ce62-4a11-af90-a23c2639ecad_game_5` (auroraveil, r649, our win, v168): **20**.
* `b36f198a-ef65-457f-8f95-1d0f7422ecde_game_2` (auroraveil, r226, our win, v176): **16**.

---

## 4. THE SIEGE ASYMMETRY — WE ANSWER THEIR RING SLOWLY, THEY ANSWER OURS IN EIGHT ROUNDS

**MEASURED.** Structures planted inside d²≤8 of the OTHER team's core, and how they end:

| our structure on THEIR core ring | n | killed by damage | median rounds to death |
|---|---|---|---|
| **barrier** | **1,107** | **751 (68%)** | **8** |
| launcher | 107 | 83 (78%) | 15 |
| sentinel | 71 | 31 (44%) | 13 |

| their structure on OUR core ring | n | killed by damage | median rounds to death |
|---|---|---|---|
| barrier | 82 | 28 (34%) | 38.5 |
| **gunner** | **63** | **11 (17%)** | **35** |
| sentinel | 67 | 22 (33%) | 8.0 |

**CONTROL, and it runs the other way inside the same table.** Their ring **sentinel** dies at the same
rate and speed as our ring sentinel (33% / r8 vs 44% / r13) — so "we cannot kill things on a ring" is
false. **What we cannot kill is their ring GUNNER: 17% over 63 builds, median 35 rounds of life** — and
that gunner is the single largest source of damage to our core in the cell (§5).

**Their answer to our seal is fast and their replacement of our kills is faster.** Their ring **sentinel**
replacement after we destroy it: **13 of 22 (59%) replaced within d²≤8, median latency 1 round** — the
`QUEUE #45` / v40-profile figure, restored. **This falsifies the v61 study's R4 ("killing a v61 siege
turret buys real time, latency 69/11 rounds") for the SENTINEL at v86.** Their ring gunner replacement
stays slow (3 of 11, median 56 rounds).

**⇒ Counter-battery on their ring sentinel is refunded within one round. Counter-battery on their ring
gunner is not — and we are not doing it.**

---

## 5. THE POINT-BLANK CORE-SNIPER GUNNER — CONFIRMED, AND FASTER THAN AT v61

Per-turret `FireTurret` census, keyed by shooter tile, band = d² to the ENEMY core footprint. `alive` =
death round − build round + 1, survivors truncated at the game's round count. `core` = shots whose target
tile is inside the enemy core's 2×2 footprint.

| who | kind | d² band | n | alive-rnds | shots | **core-shots** | shots/rnd | **core-shots/rnd** |
|---|---|---|---|---|---|---|---|---|
| **them** | **gunner** | **0–9** | **63** | **5,579** | **4,484** | **4,273** | 0.804 | **0.766** |
| them | gunner | 9–20 | 4 | 479 | 248 | 229 | 0.518 | 0.478 |
| them | gunner | 20–33 | 3 | 35 | 26 | **0** | 0.743 | 0.000 |
| them | gunner | 33–60 | 25 | 259 | 154 | **0** | 0.595 | 0.000 |
| **them** | **gunner** | **≥60** | **366** | **9,556** | **5,447** | **0** | 0.570 | **0.000** |
| them | sentinel | 0–9 | 67 | 5,046 | 1,043 | 984 | 0.207 | 0.195 |
| them | sentinel | 9–20 | 43 | 1,791 | 642 | 541 | 0.358 | 0.302 |
| them | sentinel | 20–33 | 18 | 304 | 120 | 70 | 0.395 | 0.230 |
| them | sentinel | ≥60 | 132 | 1,628 | 404 | **0** | 0.248 | **0.000** |
| us | sentinel | 0–9 | 71 | 2,628 | 814 | 704 | 0.310 | 0.268 |
| us | sentinel | 9–20 | 100 | 6,087 | 1,306 | 1,166 | 0.215 | 0.192 |
| us | sentinel | 20–33 | 53 | 5,737 | 1,146 | 1,008 | 0.200 | 0.176 |
| **us** | **sentinel** | **≥60** | **52** | **9,040** | **118** | **0** | 0.013 | **0.000** |
| us | gunner | ≥60 | 39 | 5,382 | 324 | **0** | 0.060 | **0.000** |

**THE CONTROL THE PLAYBOOK ASKS FOR, and it runs the other way on both teams simultaneously.** At
**d²≥60 the core-shot column is EXACTLY 0** for 366 of their gunners over 9,556 alive-rounds, 132 of
their sentinels over 1,628, 39 of our gunners over 5,382 and 52 of our sentinels over 9,040 — while the
raw `shots` column in the same rows is 5,447 / 404 / 324 / 118, i.e. **not a constant column and not an
empty channel.** The zero is the engine's range identity (gunner r²=13, sentinel r²=32), not a property
of anyone's targeting code. **`QUEUE #94` re-confirmed on a fresh 90-game cell.**

**Their d²≤9 gunner is the best turret in the cell by a distance:** 0.766 core-shots per alive-round at a
**95.3% core share**, **29,911 core HP over 63 turrets = 475 core-HP per gunner**, and it lives a mean of
**88.6 rounds** against our forward sentinel's **37.0**. Its rate is **up 38% on v61** (0.554 → 0.766).

**⚠ THE COST SIDE IS NOT PRICED HERE.** The d²≤9 band alone fires 4,484 gunner shots × 4 ammo =
**17,936 Ti of ammunition across 90 games (199/game)** — and that is one band of five, against their
measured 728.3 Ti/game of total conversion. A prereg must price ammo and the +20% scale per gunner; this
line does not.

**ANCHORS.** `12c81217…_game_1` their gunner at (26,25), built r122, **136 shots**, our core at (26,26),
never removed. `12c81217…_game_2` (skald) their gunner at (10,12) r67, d²=5 from our core.
`5ff21e83-c77b-4d57-8357-2a14196de158_game_5` (skald) their gunners at (9,4) r204 d²=5, (9,1) r217 d²=1,
(9,3) r233 d²=2 — three point-blank plants in one game.

---

## 6. ⭐⭐⭐ WHERE OUR 54% COMES FROM — IT IS ALMOST ENTIRELY A CORE-DISTANCE SEGMENT

**MEASURED.** Our share by the map's core-to-core d² (a property of the map, constant across every game
on it — verified: area, core d², ore count and wall count are identical across all games sharing a map
name in this pool):

| core d² band | our share | maps in the band |
|---|---|---|
| **≤200 (cores close)** | **6/24 = 25.0%** | skald 144, holmgang 128, helheim 144, nordkap 144, royale 196, frostgate 196, antler 64, fjordgate 32 |
| 201–500 | **27/39 = 69.2%** | icefloe 452, auroraveil 256, stavkirke 256, fimbulwinter 452, longhouse 484, bifrost 400, paths 400, jotunheim 392, drumlin 338 |
| >500 | **16/27 = 59.3%** | midgard 1152, glacierkeep 576, yggdrasil 968, valkyrie 576, ragnarok 1152, drakkarfjord 976 |

**Seat is not the variable: seat A 24/45 = 53.3%, seat B 25/45 = 55.6%.** Area alone is weaker than core
distance: area≥676 → 16/27 = 59.3%, area<676 → 33/63 = 52.4%.

**Restricted to our current-era holder v176 (60 games), the segment sharpens: core d²≤200 → 2/17 = 11.8%,
core d²>200 → 27/43 = 62.8%.** (v168, 20 games: 4/6 and 11/14 — the older arm does NOT show the collapse.
n=6 in that cell; **no direction word is offered on it**.)

**Per-map, n≥3 (point estimates only — 18 clusters, below the interval floor):**
midgard **12/12** · stavkirke **7/7** · icefloe 7/8 · longhouse 3/3 · auroraveil 4/8 · fimbulwinter 2/6 ·
valkyrie 1/3 · paths 1/3 · glacierkeep 1/4 · yggdrasil 1/4 · helheim 1/5 · holmgang 1/6 ·
**ragnarok 0/3** · **skald 0/7**.

**⭐ SKALD IS THE CLEANEST DETERMINISTIC LOSS CELL WE HAVE AGAINST THIS OPPONENT.** 7 games, **0 wins**,
both seats (5 as B, 2 as A), all 7 ended `core_destroyed` against us, rounds 83/83/99/121/173/191/262.
The map is 16×16, core d²=144, 16 ore, 16 walls.
* **Our opening is IDENTICAL in all 7:** sentinel built r5, second sentinel r9, at the two mid-map tiles
  mirrored by seat ((8,7)+(8,6) or (8,8)+(8,9)).
* **Their opening is identical within seat groups:** sentinel r10 at d²=25 (3 games), or sentinels r15 at
  d²=9 and r17 at d²=5 (3 games).
* **First damage to our core lands at r15, r15, r16, r16, r16, r17 and r47.**
* Core-damage ledger over the 7 games: **THEM sentinel 2,952 + gunner 2,716 = 5,668 · US sentinel 1,602.
  We are out-damaged 3.5:1 on this map.**
* Three of the seven (`8d9b178c…_game_2`, `b36f198a…_game_1`, `cc601b2f…_game_5`) share the same opening
  build stream; **two of them are the structural-duplicate pair from §0.4 and finish at the identical
  round 83.** ⇒ **this cell is regression-testable in ONE game**, exactly like `QUEUE #101`'s team-lazy
  bad-map six.

---

## 7. THE FORGONE ACTION — 6,543 BUILDER-ROUNDS STANDING ON THEIR CORE RING DOING NOTHING

**SUBJECT: these are MJOLNIR v168/v174/v176/v179's builders, not the Skalman dev line's.**

**MEASURED.** Reconstructing every builder bot's tile per round and testing membership of the enemy
core's **orthogonal ring** (the 8 tiles orthogonally adjacent to the 2×2 footprint):

| | US (Mjolnir) | THEM (v86) |
|---|---|---|
| builder-rounds spent on the enemy core ring | **10,303** (in 86/90 games) | 1,732 (in 57/90 games) |
| **IDLE — no attack, heal, build or move that round** | **6,543 = 63.5%** | **164 = 9.5%** |
| heal | 1,970 = 19.1% | 79 = 4.6% |
| **attack** | 1,118 = **10.9%** | 431 = **24.9%** |
| build | 362 = 3.5% | 39 = 2.3% |
| move | 312 = 3.0% | 1,019 = 58.8% |

**IS "IDLE" REALLY "IDLE AND FREE"?** Yes, and it is an engine fact rather than an assumption.
Decoding `SetActionCooldown` (Update field 7) across the pool: **every one of 11,417 builder-bot cooldown
events carries value 1**, and a cooldown of 1 decrements to 0 at end of round — **so a builder bot is
action-free on every single round.** (Sentinels are always set to 2, gunners/launchers/core to 1 — the
column varies by kind, so it is not a constant-column artefact.) Reconstructed:
**idle-but-on-cooldown = 0 of 10,303**, and the control **"acted while on cooldown" = 0 of 3,760** on our
side and **0 of 1,568** on theirs, which is what a correct cooldown model must produce.

**WAS THE ACTION AFFORDABLE?** A builder melee costs 2 Ti. At those 6,543 idle-and-free ring rounds our
team titanium was **≥2 in 6,170 (94.3%)**, median bank 12 Ti. **The verb was affordable in 94% of them.**

**⭐ AND THE 1,118 ATTACKS THAT DO HAPPEN NEVER TOUCH THE CORE.** The core-damage ledger (§1) attributes
**0 builder-melee damage to either core, on both sides, in all 90 games** — every `BuilderAttack` target
tile in the pool falls outside the enemy core's 2×2 footprint. The instrument is not blind to melee: it
counts 5,828 of our attack events and 9,631 of theirs (64.8 and 107.0 per game). **So "our ring builder attacks" means it attacks
the barrier or belt next to the core, never the core.** (v61 measured 2 total damage in 50 games — same
direction, now exactly zero.)

**⛔ WHAT THIS IS NOT: "PECK THE CORE MORE".** `QUEUE #85` prices that and it prices badly — their
builders heal 115.7 times/game at +4 HP per 1 Ti, against our melee's 2 dmg per 2 Ti; that exchange is
4:1 against us and this cell does not overturn it. **The finding is that the ring builder emits NO VERB
AT ALL in 63.5% of the rounds it spends on the most valuable tile on the map**, which is
`QUEUE #70`'s ZERO-IDLE-AND-FREE mandate and `QUEUE #48`'s parked-raider terminal idle, measured against
a specific 1834-rated opponent for the first time. **Their side is the control and it runs the other way:
9.5% idle on the same tiles.**

**ANCHORS.** `20a19adb-54f8-4cfd-a464-5159b1a0085e_game_1` (midgard, r1000, our WIN on the tiebreak):
**1,799 idle-and-free ring rounds**, our builder #4 alone contributing **924** and #11 **875**.
`7f25466f-0863-446c-9f8a-6829ffe88054_game_3` (glacierkeep, r741, our loss): **1,201**, builder #3 = 689.
`47f7ddb3-4dee-4b99-b292-17ca5b96267e_game_3` (holmgang, r461, our win): **786**.

---

## 8. THEIR CPU TIMEOUTS — A REAL, ONE-SIDED SIGNAL WITH NO DEMONSTRATED CHANNEL

**MEASURED.** `botOutput.tled` turns: **THEM 750 across 25 of 90 games; US 0 across all 90.**
Concentrated: `14292e81-8365-446c-8c60-37e43be87006_game_1` (valkyrie, r247) **262**,
`20a19adb…_game_5` (valkyrie, r173) **173**, `f6f33970-b977-4a56-b420-ac1ef66c80ab_game_3`
(valkyrie, r156) **155** — **three valkyrie games hold 590 of the 750**, and valkyrie is a 900-area map.

**A CPU timeout does not destroy the unit** (CLAUDE.md) — it silently skips that turn. So this is lost
tempo, not lost units.

**⛔ AND IT DOES NOT PREDICT THE RESULT.** Our share in games with ≥1 of their TLEs: **14/25 = 56.0%**.
Without: **35/65 = 53.8%.** Flat. **Reported as a fail-to-exclude null and NOT restated as an exclusion**
— it closes nothing, per the DEFF direction clause.

**⇒ This is the `QUEUE #98` question (does OUR pressure cause their timeouts) with a second named
customer and a map concentration to aim it at, not an answer to it.**

---

## 9. REFUTED — RETAINED SO NOBODY RE-DERIVES THEM

**R1. "Their turrets vanish because their team ammunition hit zero and `fire()` raised."**
This is the obvious reading of `CLAUDE.md`'s self-audit item (`can_fire` returns True at 0 ammo; the check
lives in `finish_firing_turret` and RAISES, destroying the turret). **MEASURED AND DEAD.** Team ammunition
at the round of a no-damage removal: **their gunners median 18 (needs 4), ammo==0 in 12/350 = 3.4%;
their sentinels median 14 (needs 10), ammo==0 in 15/191 = 7.9%.** **The baseline** — 20 random rounds per
game per team, n=1,800 — **is ammo==0 8.6% of the time for them.** The removal rounds are at or BELOW the
background rate of being dry. Ammo exhaustion is not the mechanism.

**R2. "Their no-damage turret removals are ordinary `destroy()` teardowns by an adjacent builder."**
Refuted three ways in §3: the positive control (our launchers, 94.9% vs 6.0%) shows the detector fires
when a `destroy()` happens; their rate is at background; and the matched within-turret control has
adjacency **LOWER** at the removal round than at a random round of the same turret's life.

**R3. "The launcher spawn-ring farm is what this opponent does to us."** **v61's signature behaviour is
gone at v86: 1 of 129 launchers forward; 0 of 2,011 throws pick a victim up at d²≤8 of our core; median
d² from the pickup tile to OUR core is 317, median throw round r189.** They now throw our builders **off
their own base** — the eviction pattern their v66 games against `opensverige - plan B` hinted at. **Do
not build a plank against the farm; there is no farm.**
*(Throw census, this pool, attributed per corpus-howto trap 3 — 2,569 multi-tile `moveBuilderBot` events
resolved, 79 `UNATTRIB` (both teams' launchers in range) and 190 with no launcher in range, neither
guessed: **THEM→US 2,011 (22.3/game, 62/90 games, 34% land on a map border); US→THEM 323 (3.6/game,
35/90 games, 14% border, median d² from pickup tile to THEIR core = 8, 59% at d²≤8 — we are the ones
doing spawn-ring eviction now); US→US 235 (2.6/game, our own ferry).*)*

**R4. "They are crash-inducing us with border throws."** **34% of their 2,011 throws land on a map-border
tile** — the LOKI-14 geometry. **It does not fire on us: 0 of 91 of our builder-bot removals carry the
no-HP-event crash signature** (against 41 of 101 of their builder removals). **Our guard holds.** Same
verdict as the v61 study's R2, re-confirmed on 90 fresh games and a 2.2× larger throw volume. **Do not
spend a leg proving they cannot crash us.**

**R5. "Killing a v86 siege turret buys time."** True of their ring **gunner** (27% replaced, median 56
rounds). **FALSE of their ring SENTINEL: 13 of 22 replaced within d²≤8 at median latency 1 round.** The
v61 study's R4 said the opposite for sentinels (11 rounds) — **that has reverted to the v40 figure and
must not be quoted forward.**

**R6. "Their economy is the story."** No: harvesters 3.41/game against our 5.22, conveyors 21.6 against
our 29.7, and yet they deliver **more** titanium (median 930 vs our 775). Same conclusion as v40 and v61
— **do not spend a leg on their economy.** (Under `R1000_IS_DEFEAT` it is off-currency anyway; 3 of 90
games ended on `titanium_collected`.)

**R7. "The map cells are deterministic, so we can regression-test any of them in one game."** Only
partly. **Across the 18 `(map, seat, ourver)` cells holding ≥2 games, 0 of 18 produced an identical
(round, winner) pair in every game** — outcomes vary within a cell. **What IS stable is the WINNER on
most cells** (e.g. midgard seat B 4/4 winner=us at rounds 110/119/132/259; skald seat B 5/5 winner=them
at 83/83/99/121/173). **So a one-game regression test reads the WINNER reliably on the polar cells and
the CLOCK not at all.**

---

## 10. THE PIECES — each SMALL, ≥2 anchors, mapped onto QUEUE.md before it is offered as new

**Exclusion list built from `QUEUE.md` at study time.** Rows checked and deliberately not re-derived:
#5/#17/#38/#43 (crash & kidnap family), #27 (destroy-to-prune-scale NOTE), #28/#24 (launcher gates),
#45 (kill the feeder), #48/#70 (idle builders), #58/#59 (launcher offence/defence),
#82/#101/#103 (bad-map rows), #85 (core peck pricing), #87/#88 (no death-tile memory),
#90/#91/#93/#94 (gunner band family), #92 (first sentinel), #95 (opponent classification),
#96 (un-silence melee vs collar turrets), #98 (TLE-farm), #104 (don't feed the pump),
#117 (content-duplicate fingerprint).

---

### PIECE 1 — ⭐⭐⭐ **THE RELOCATING-GUNNER SHREDDER IS THE THING KILLING OUR RAIDERS, AND WE HAVE NO MEMORY OF IT**

**CHANGE.** Treat an enemy home gunner that has been torn down and rebuilt within d²≤10 of a vacated tile
as a **persistent, relocating threat**, not as a new building: carry a per-tile-neighbourhood threat
memory for the raider's approach path and for barrier/turret siting, so a raider does not walk the same
lane into the same gun's new seat.

**MECHANISM METRIC.** (a) our forward builder deaths within the r²≤13 envelope of a gunner built in the
last 20 rounds, per game; (b) our ring barrier median rounds-to-death (baseline **8**, 68% killed of
1,107); (c) our forward sentinel mean alive-rounds at d²≤9 (baseline **37.0** against their point-blank
gunner's **88.6**).

**FIXTURE THAT CAN RESOLVE IT.** Local both-ways battery first (memory on/off, same tree, same maps),
then an unrated pinned leg — `fcode match unrated <lingling_40h> --match <a v86 match id>` pins their v86
so the treatment is not confounded by their next bump. Their v86 has held since 2026-08-20T09:32Z.

**WHY NOW.** 366 of their gunners, 9,556 alive-rounds, **0.570 shots/alive-round, 0 core shots** — the
whole output of that fleet lands on our raiders and our seal. It is the mechanism behind §4's asymmetry
(our ring barriers die in 8 rounds, their ring gunner survives 35). **Nearest existing rows: #87
(no death-tile memory in turret siting — this is the same absence on the RAIDER PATH), #88
(belt-repair attrition memory — same class, different subsystem), #104 (don't feed the pump).**
**It is not covered by any of them: all three are keyed to a FIXED enemy turret; the finding is that this
opponent's turret MOVES by being rebuilt, so a per-tile memory misses it and a per-NEIGHBOURHOOD memory
does not.** ⛔ **GREP OWED** against the Skalman head `bots/_v622nestfall` before this is stocked — the
90 games were played by Mjolnir and no incumbent claim is made here.

**ANCHORS.** `12c81217…_game_1` r33–r117 (six home gunners, each 8–13 rounds, walking (5,3)→(6,3)→(0,3)→
(1,3)→(1,4)); `80fcf20c…_game_2` (32 self-removals); `619796f0…_game_5` (20).

---

### PIECE 2 — ⭐⭐⭐ **THE CLOSE-CORE SEGMENT: 6/24 AT d²≤200, AND 2/17 ON OUR CURRENT HOLDER**

**CHANGE.** A map-class branch on core-to-core d²: at d²≤200 our current opening (two mid-map sentinels
at r5 and r9) is measurably losing; the branch is to spend the first two turret purchases inside their
core's r²≤13 gunner band instead of mid-map, and/or to bring the first forward plant forward of their
r15 first-blood.

**MECHANISM METRIC.** round of first damage to THEIR core (baseline on skald: theirs lands on us at
**r15–r17**, ours is not measured before r47 in 1 of 7 games); our share in the d²≤200 band (baseline
**6/24 = 25.0%**, v176-only **2/17**); core-damage ratio on the band (baseline **1:3.5 against us** on
skald).

**FIXTURE.** `QUEUE #101`'s own design, ported: the polar cells are winner-stable (skald 0/7 both seats,
midgard 12/12), so a **one-game-per-cell regression battery** reads the winner; the clock does not
regress-test (R7). Then a pinned unrated leg on the close-core maps.

**WHY NOW.** This is where the whole 54.4% lives: **69.2% at d²201–500 and 59.3% at d²>500 against 25.0%
at d²≤200.** It is one branch, not a redesign. **Nearest rows: #82 (midgard — the WRONG polarity: midgard
is 12/12 FOR us against this opponent, so #82's premise does not transfer to this cell), #101 (team lazy
bad-map six — same shape, different opponent), #103 (midgard registration).** **New per-opponent
instance, and the first with a geometric predictor (core d²) rather than a map name list.**

**ANCHORS.** All 7 skald games listed in §6. `12c81217…_game_2` (r173), `8d9b178c…_game_2` (r83),
`cc601b2f…_game_5` (r83), `b36f198a…_game_1` (r99).

---

### PIECE 3 — ⭐⭐ **THE RING BUILDER HAS NO VERB — 63.5% IDLE-AND-FREE ON THE ENEMY CORE RING**

**CHANGE.** A terminal free verb for a builder standing on the enemy core's orthogonal ring — the
`QUEUE #70` fallback ladder, with the ring as its highest-value population. Candidate verbs in priority
order: seal an unsealed ring seat (barrier), body-occupy a spawn seat (spawn-tile denial is an open
road), heal the adjacent forward sentinel, and only then melee.

**MECHANISM METRIC.** idle-and-free builder-rounds on the enemy core ring, per game (baseline
**72.7/game**, 6,543 over 90 games, 86/90 games affected); their ring builders as the control
(**9.5% idle**).

**FIXTURE.** Local battery — the metric is decodable from any replay with no platform games.

**WHY NOW.** The population is huge, the cooldown objection is dead (all 11,417 builder cooldown events
are value 1 ⇒ a builder is free every round) and the affordability objection is dead (94.3% of those
rounds held ≥2 Ti). **This is `QUEUE #70` and `#48`, not a new row — it is stocked here as EVIDENCE for
them against a named 1834-rated opponent, and as the answer to the gsxWins study's "does the same cell
exist vs lingling" question: YES, and larger.** ⛔ **The verb choice must NOT default to core melee —
`#85` prices that at 4:1 against us and this cell agrees (their 115.7 heals/game).**

**ANCHORS.** `20a19adb…_game_1` (1,799 idle ring-rounds), `7f25466f…_game_3` (1,201),
`47f7ddb3…_game_3` (786).

---

### PIECE 4 — ⭐⭐ **THEIR RING SENTINEL IS REFUNDED IN ONE ROUND AND THEIR RING GUNNER IS NOT — SPLIT THE COUNTER-BATTERY TARGET**

**CHANGE.** Rank an enemy ring **gunner** above an enemy ring **sentinel** as a counter-battery target
(today they are ranked by generic turret priority).

**MECHANISM METRIC.** replacement latency after our kill, by kind (measured: sentinel **13/22 = 59%
replaced, median 1 round**; gunner **3/11 = 27%, median 56 rounds**); and the damage it denies (their
point-blank gunner = **475 core-HP per turret** at 0.766 core-shots/alive-round).

**FIXTURE.** Local first, then a pinned unrated leg vs their v86.

**WHY NOW.** It corrects a fact this repo currently holds the other way round: the v61 study banked
sentinel latency at 11 rounds and gunner at 69, which would rank the sentinel first. **At v86 the
sentinel is the refunded one.** **Nearest rows: #45 (kill the feeder, not the ladder — its "1–2 round
rebuild" premise is restored for sentinels and refuted for gunners), #96 (un-silence melee vs collar
turrets — this supplies the TYPE ordering that row does not carry), #93 (the mirror plank on our side).**

**ANCHORS.** §4's tables; `5ff21e83…_game_5` (three point-blank gunner plants r204/r217/r233 against a
263-round game).

---

### PIECE 5 — ⭐ **THE OPPONENT-SIDE EVIDENCE FOR `#27`: A 1834-RATED TEAM RUNS DESTROY-TO-PRUNE-SCALE AS ITS PRIMARY DEFENCE**

**CHANGE.** None on its own — this is a **note that upgrades an existing NOTE row.** `QUEUE #27` records
that two destroy-to-prune-scale planks "died on MAGNITUDE rather than mechanism". **Here is a magnitude
observation from outside our own tree: 541 self-removals in 90 games, 6.0/game, in 88/90 games, run
continuously by a team rated above us.**

**MECHANISM METRIC.** live scale-contributing entity count over time (model, from build/death events);
turret builds per game against turrets alive at end (**them: 461 gunners built / 93 alive; 293 sentinels
built / 49 alive**).

**FIXTURE.** Local — the scale model needs no games; the estimator built here is NOT validated enough to
quote absolute scale (§3's ⚠) and a proper one would read `get_scale_percent()` from an instrumented
local run.

**WHY NOW.** `#27` exists precisely so a fourth plank is not proposed blind. **This is the first field
evidence that the mechanism is load-bearing for somebody.** And Mjolnir already runs the same mechanism
on launchers (358 built, 197 self-removed at median life 1 round, 94.9% builder-adjacent) — **so the
mechanism is shipped on our side too, on a different entity type.**

---

## 11. WHAT I COULD NOT MEASURE, AND WHY

1. **`self_destruct()` vs an uncaught exception** for the 541 self-removals. Both are a bare
   `removeEntity` on the wire. §3 rules out damage and `destroy()`; it does not separate the last two,
   and no replay-only method can.
2. **Turret FACING.** I did not decode the `direction` field on `placeEntity`, so §5's in-band rows are
   about outcomes, not about aim. Outside d²≥60 range alone explains the zero.
3. **Absolute cost scale.** The titanium-tape estimator reaches only 21–34% exact agreement with its own
   prediction (§3 ⚠). Direction confirmed, magnitude not quotable.
4. **Who kills their ring gunner.** 11 of 63 die to damage; I did not attribute those 11 between our
   turret fire and our builder melee.
5. **Whether their throw destinations are chosen.** 2,011 throws, 34% on a border tile; I did not compute
   distinct destinations per launcher.
6. **Any interval that excludes anything.** 18 clusters, below `cluster_ci.py`'s 30-cluster floor. Every
   split here is a point estimate. **The two nulls (§8's TLE-vs-outcome, R7's determinism) are
   FAIL-TO-EXCLUDE claims and have not been restated as exclusions**, so they close nothing.
7. **A GREP against our current dev head.** The pool is Mjolnir's; `bots/_v622nestfall` did not play these
   games. Every piece in §10 carries **GREP OWED** and none claims an incumbent gap.
8. **Their v88.** We hold 5 rated games against it; they are outside this pool and unread.

---

## 12. SUMMARY FOR THE LEDGER

```
2026-08-22	lingling_40h	86	90	docs/research/REPLAY-STUDY-lingling40h-v86-2026-08-22.md
```

**The one-sentence answer to "what do they do".** They keep **one point-blank gunner on our core
footprint that fires 0.766 core-shots per round for 89 rounds**, and behind it they run a **disposable
home-gunner fleet that self-destructs every ~8 rounds and is rebuilt one tile over** — 5,447 shots into
our raiders and our seal, at a cost scale they refund on every teardown.

**The one-sentence answer to "why we are only at 54%".** Because **at core d²≤200 we are at 25% (11.8%
on v176) and everywhere else we are at 62–69%** — and because our builders spend **6,543 free rounds
standing on their core ring emitting no verb at all.**
