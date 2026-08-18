# BUILD REPORT (DRAFT) — `bots/_v521sync` (seal-shot synchronization), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v520pincer` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v521_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2`, and the freeze
re-verified byte-for-byte at the end of the build (9/9). Master `LOKI_FS_V521`; False reproduces
the v520-PINCER-ONLY configuration (AST-scanned and byte-proved below). Scratch:
`scratchpad/s51_v521_build/`. PAR=4 on single-arm legs; the headline runs 3 arms × PAR 4.
Recorded PIDs in `scratchpad/s51_v521_build/PIDS`. `scratchpad/overnight*` and corefill
untouched.*

*Diff vs parent: `doctrine.py` +241/−2, `main.py` +97/−2, `siege.py` +300/−15, **`raid.py` and
`eco.py` BYTE-IDENTICAL (0/0)**. **5,964 games with a result row across every leg; 0 tracebacks,
0 no-winners** (counted off the leg TSVs, not by directory). ⛔ Timeouts are NOT reported —
v518 finding 0 proved the local timeout column is a constant that cannot fire.*

---

## ⭐⭐⭐ THE ONE-PARAGRAPH READ

**THE MECHANISM FAILS AND THE INSTRUMENT BUILT TO JUDGE IT PRODUCES TWO FINDINGS WORTH MORE
THAN THE PLANK.** At n=1,080/arm against a byte-identical known-zero arm in the same blocks,
v521 FIRED reads **wins +1.48 pp (hw 3.97, inside)** and **`KILL_TARGET`'s tracked metric
k≤200 −7.04 pp (hw 3.77) OUTSIDE** — a real regression — with median kill **191 → 236**. The
known-zero arm reads +0.83 / +1.39 / −0.37, so the ~5 pp fixture floor did not fire and the
−7.04 is the build's own. The single-flag isolation names the culprit exactly: **the magazine
collar reserve (`iMAG`) carries the whole of it at −9.83 pp k≤200 / −7.48 pp k≤300, both
OUTSIDE**, while the three ladder reorders (`iLADDER`) and the gate fix (`iGATE`) are nulls; and
the phase budget traces the arithmetic end to end — **`funded → kill` 69 → 100 rounds** against a
known-zero control at 69. **THE TWO FINDINGS: (1) the mandate's premise is falsified — parent
OVERLAP is not ~0, it is 13.35 rounds/game with 39.9% of games above zero, and the reel's
"0 of 119" was a SELECTION ARTEFACT of picking our six worst games; (2) the reframe's THESIS is
nevertheless confirmed on the population — net core damage is 6.97 per OVERLAP round against
1.13 per non-overlap round, a 6× gap, stable across all three arms.** v521 raises sealed rounds
52.5 → 62.0 and lowers funded-turret rounds 65.8 → 59.3, and **OVERLAP does not move
(13.35 → 13.68 against a known-zero at 13.31).** The two halves cancel.

⚠ **THE ~4.7–5.6 pp SAME-CONFIG FALSE-POSITIVE FLOOR (v519 open item 2) IS CARRIED BESIDE EVERY
CLAIM BELOW**, and this build's answer to it is the same as v520's: a **KNOWN-ZERO ARM IN THE
SAME BLOCKS**, proved byte-identical to the baseline on 12 of 12 games with a negative AND a
positive control. Every contrast is reported twice.

---

## WHAT WAS BUILT

### FIRED-CONFIG CORRECTIONS (parent-config, not new mechanisms — they define the baseline)

**(i) THE FIRED CONFIG IS PINCER-ONLY.** `FS_V520_PRESENCE = False` and
`FS_V520_GUNNEAR = False` **at their definition sites**, per v520's isolation grid
(PRESENCE −2.56 pp wins with its own mechanism metric also null; GUNNEAR −0.85 pp and a
substitution rather than an addition). Code stays; the flags are the decision. Turning GUNNEAR
off also returns v520 doctrine collision 1 to a zero dose — with the annulus floor back at 20 the
ring-side shredder stops firing from d² 4-10 on the collar, so Magnus's priority ruling 1
(barriers → launchers → sentinels) is no longer being taken from.

**(ii) THE GATED LEAK IS CLOSED** (v520 open item 7). The two `fs_crew_on()` read sites outside
the map gate (`main.py:1000` spawn-purpose anchor, `main.py:1084` roster) now consult
`_fs_gate`. Site 2 needed the core resolved twenty lines earlier than the parent resolves it;
`_v521_core_resolve` hoists **the same scan**, idempotent, and the parent's
`if self.core is None: return` guard is deliberately left where it was so a body that cannot see
its Core still increments the role counter in the round the parent increments it.

### THE NEW MECHANISM — `FS_V521_SYNC`, FIVE CLAUSES, AND THE LAST TWO WERE DIAGNOSED RATHER THAN DESIGNED

* **1a NEAR** (`FS_V521_NEAR_CLOSE`) — turret ALIVE+FUNDED and 1 ≤ orth_open ≤ 2: rungs 1′
  (early sentinel) and 1″ (shredder) stand down, rung 1 (BARRIER) runs, **the seal WAIT is
  bypassed for rungs 2 and 3** (the two verbs that unblock a seat), and rung 4 is suppressed.
* **1b HOLD** (`FS_V521_HOLD`) — turret ALIVE and orth_open == 0: rungs 2 and 3 suppressed so the
  body stays on the collar; rung 4 kept, because a second turret raises damage *inside* a window
  that is already open.
* **1c BUYIN** (`FS_V521_BUYIN`) — closure NEAR-or-COMPLETE and NO turret: the sentinel purchase
  is promoted to the top of the ladder. **Every gate unchanged** — `_fs_sentinel_ok` still
  decides; only the round moves.
* **1d COLLARFIRST** (`FS_V521_COLLARFIRST`) — the Core's magazine floor holds the whole collar's
  price back while a turret is live and the collar reads open.
* **1e PHASE_HONEST** (`FS_V521_PHASE_HONEST`) — publish `FS_PH_KILL_OPEN` whenever a turret is
  live **and the collar reads open this round**, instead of only when it has never closed.

⛔ **THE SYMMETRIC-TRIGGER WALK WAS DESIGNED AND THEN DROPPED AS A DUPLICATE, AND THAT IS
RECORDED IN THE TREE RATHER THAN SHIPPED AS A FLAG NOBODY READS.** The mandate asks that a body
walk toward the sentinel site when the purchase is gated only by siting. `_fs_stand_target`
already does exactly that: v516 `FS_V516_SENTREACH` makes the reach station a walker preference
with its own patience timer and v518 `FS_V518_EARLY_REACH_FIRST` already promotes it above the
evictor's reach in precisely the state — no forward sentinel alive — that this clause would fire
in. A second preference on the same tiles is a second reading of one mechanism, not two
mechanisms, and no isolation grid could ever separate them. **v521 changes the ACTION ORDER
only. The walk is the parent's.**

---

## ⛔⛔⛔ HOW 1d AND 1e CAME TO EXIST — THE DOSE TEST THAT KILLED TWO DESIGNS BEFORE THE HEADLINE

This section is first because the process is the finding, and because two ladder designs were
built and discarded on measurement before a single headline game was played.

**THE INSTRUMENT: THE DETERMINISTIC DOSE TEST.** Same seeds, randomness off — ours *and the
opponent's* — baseline vs treatment, replay bytes diffed. **The share of deterministic games in
which the treatment plays a different game AT ALL.** It costs 36 games and it answers a question
no win column can: *does this change ever change anything?*

| design | atoll | drakkarfjord | glacierkeep | midgard | nordkap | yulerune | **total** |
|---|---|---|---|---|---|---|---|
| 1a/1b/1c, suppress rungs 2-4 under NEAR | 0/6 | 0/6 | 0/6 | 6/6 | 3/6 | 6/6 | **15/36** |
| 1a revised: bypass the WAIT for rungs 2-3 | 0/6 | 0/6 | 0/6 | 6/6 | 3/6 | 6/6 | **15/36** |
| **+ 1d COLLARFIRST** | 3/6 | 0/6 | 0/6 | 6/6 | 3/6 | 6/6 | **18/36** |
| **+ 1e PHASE_HONEST (as fired)** | **3/6** | **6/6** | **3/6** | 6/6 | 3/6 | 6/6 | **27/36** |

⛔⛔ **READ THE TOP ROW: 0 OF 18 GAMES CHANGED A BYTE ON THE THREE MAPS WHERE THE SYNC STATE
ACTUALLY FIRES.** midgard and yulerune are `FS_V519_CRIPPLE_MAPS` cells where the whole plank
stands down, so their 6/6 is the GATE FIX, not the mechanism. **A reorder that never changes the
chosen action is not a mechanism**, and the win column would have reported this as a clean null
at any n while the report claimed three working clauses.

**WHY IT WAS INERT — `_v521_why`, written to ask the question the rung tape could not answer.**
Per NEAR/HOLD round it emits the four candidate blockers, each read off the same predicate the
rung itself uses (`_fs_try_clear(probe=True)` for rung 3, so the counterfactual costs nothing).
The modal NEAR round, seed 7:

| map | modal NEAR round | count |
|---|---|---|
| drakkarfjord | `adj=0 blk=0 clr=0 ti=12 price=18` | 13 |
| glacierkeep | `adj=0 blk=0 clr=0 ti=14 price=20` | 71 |
| glacierkeep | `adj=0 blk=0 clr=0 ti=16 price=22` | 38 |
| nordkap | `adj=0 blk=0 clr=0 ti=16 price=14` | 28 |

**TWO BLOCKERS, NEITHER OF THEM ACTION SELECTION:**
1. **`adj = 0`** — the body is not orthogonally adjacent to any open seat. Rung 1 cannot fire
   because the builder is standing somewhere else. That is a WALK problem.
2. **`ti < price`** — the bank is below the remaining collar's price in essentially every round.

⭐⭐⭐ **AND BLOCKER 2 IS OURS.** `FS_MAG_REPAIR_BARRIERS = 2`, so with a live forward turret the
Core's conversion floor is `2 × bar` = **12-14 titanium at live scale** — which is exactly the
`ti` column above — against a collar asking 18-24. v513 change F **measured this equilibrium and
wrote it down in the same function**: *"THE BANK EQUILIBRATES TO EXACTLY `ti_floor` AND STAYS
THERE"*. ⇒ **THE FUNDED TURRET IS WHAT STARVES THE SEAL. The seal-shot disjointness is not only
a scheduling accident; it is partly caused by us.**

**AND THE PREMISE THAT LICENSED THE REPAIR ALLOWANCE IS FALSE ON THIS CHASSIS.** Its stated
argument is *"a sentinel only exists once the collar was CLOSED, so what the collar still needs
at KILL is a REPAIR allowance, not a fresh collar."* True under v513's salt-only gate. It stopped
being true at **v515**, whose `FS_V515_GATE_OR` eco disjunct buys a sentinel with the collar open
(`FS_PH_KILL_OPEN` exists for exactly that state), and at **v516**, whose GLOBALSENT beat arms
the branch off turret LIVENESS with no closure term at all.

**1e FOLLOWED FROM 1d BEING UNREACHABLE.** As published by the parent, `FS_PH_KILL` means
"a turret is alive" and `FS_PH_KILL_OPEN` means "a turret is alive AND THE COLLAR HAS NEVER
CLOSED" (`fs_sealed_rnd is None`). So a game whose collar closed once at r30 and broke at r34
publishes KILL for the next 900 rounds, and **every consumer that asks the phase "is the collar
shut?" is told YES on a board where it is open.** Measured: 1d alone changed **0 of 12**
deterministic games on drakkarfjord/glacierkeep. With the honest publish, 9 of 12.

---

## ⭐⭐ CENTREPIECE 1 — THE OVERLAP CURRENCY, n=1,080/arm, replay-side

*(`overlap.py`, eight guards driven to both verdicts — see ARTIFACTS. Funding is read **off the
wire**: update field 6 carries each team's scalars and field 7 is the ammunition balance, the
same channel `turrets.py` uses. No bot stdout is involved.)*

**OVERLAP = rounds in which the collar is SIMULTANEOUSLY sealed AND a forward turret of ours is
alive AND the magazine holds ≥ 10 ammunition.**

| arm | n | sealed_r | livefund_r | **OVERLAP_r** | ovl > 0 | seal_only_r | shot_only_r | **net dmg / overlap round** | net dmg / other round |
|---|---|---|---|---|---|---|---|---|---|
| v520-PINCERONLY (baseline) | 1080 | 52.46 | **65.79** | **13.35** | 39.9% | 39.11 | 52.44 | **6.974** | 1.133 |
| **v521 FIRED** | 1080 | **61.96** | **59.31** | **13.68** | 40.1% | **48.29** | **45.63** | 6.903 | 1.026 |
| flagoff *(known-zero)* | 1080 | 55.07 | 64.28 | 13.31 | 39.7% | 41.76 | 50.96 | 7.053 | 1.149 |

⭐⭐⭐ **FINDING 1 — THE MANDATE'S PREMISE IS FALSIFIED, AND THE FALSIFIER IS THE SAME INSTRUMENT
ON A DIFFERENT POPULATION.** The mandate states *"parent baseline ~0 [overlap] per the reel"*.
**It is 13.35 rounds per game, and 39.9% of games have overlap above zero.** v520's reel finding
(0 of 119 enemy-core heal rounds in a fully-sealed round) is a **SELECTION ARTEFACT**: the reel
selects the earliest our-core-death per map — our six *worst* games. Run on this build's own
reel, by the same convention, the same instrument returns **overlap_r = 0 in 6 of 6** (below).
**Same instrument, same convention, two populations, opposite answers.** Any plank priced against
the reel's zero was priced against the tail.

⭐⭐⭐ **FINDING 2 — AND THE REFRAME'S THESIS SURVIVES ITS OWN PREMISE BEING WRONG.** Net damage
on their core is **6.97 per OVERLAP round against 1.13 per non-overlap round — a 6× gap**, and it
reads 6.90 / 7.05 in the other two arms, i.e. it is a property of the state and not of the arm.
**The mandate predicted 4.8–9.0 and the measurement lands at 6.9–7.1.** Overlap rounds are worth
what the reframe said they were worth. What fails is only this build's attempt to buy more of
them.

⛔⛔ **FINDING 3 — THE TWO HALVES CANCEL EXACTLY, AND THAT IS THE BUILD'S EPITAPH.** v521 raises
sealed rounds **+9.50** and lowers funded-turret rounds **−6.48**; `seal_only` rises +9.18 and
`shot_only` falls −6.81. **OVERLAP moves +0.33 against a known-zero arm at −0.04.** The build
converts shot-only rounds into seal-only rounds. That is a lateral move on the currency and a
loss on the clock.

---

## ⭐⭐ CENTREPIECE 2 — THE `KILL_TARGET` PANEL, n=1,080/arm, THREE ARMS CONCURRENT PER BLOCK

**30 blocks × 36 games**, 6 maps (the standard 5-map siege grid plus yulerune) × 3 seeds × 2
seats, vs `bots/_v488beltbreak2`. All three arms run **inside the same block on the same seeds**
(`--seed` does not pin a game, v515 finding 1). A block counts only when all three arms finished
all 36 games; 30 of 30 did.

| | **v520-PINCER-ONLY (baseline)** | **v521 FIRED** | **flagoff — KNOWN-ZERO** |
|---|---|---|---|
| WINS | 714/1080 (66.1%) | 730/1080 (67.6%) | 722/1080 (66.9%) |
| ≤r150 | 235 (0.218) | 133 (0.123) | 264 (0.244) |
| **≤r180 (`KILL_TARGET` median mark)** | 302 (0.280) | 205 (0.190) | 317 (0.294) |
| **≤r200 (TRACKED METRIC)** | 336 (0.311) | **260 (0.241)** | 351 (0.325) |
| ≤r250 | 410 (0.380) | 356 (0.330) | 429 (0.397) |
| **≤r300 (ITT primary, `DEFENCE_ADMISSION_BAR`)** | 485 (0.449) | 448 (0.415) | 481 (0.445) |
| **median kill round** | **191** | **236** | 185 |
| our core destroyed | 312 | 299 | 310 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v521 FIRED vs baseline** | +1.48 pp (hw 3.97) inside | **−7.04 pp** (hw 3.77) **OUTSIDE** | −3.43 pp (hw 4.18) inside |
| **flagoff vs baseline** *(byte-identical play)* | +0.83 pp (hw 3.98) inside | +1.39 pp (hw 3.93) inside | −0.37 pp (hw 4.19) inside |

⛔⛔ **READ THE SECOND ROW FIRST. THE KNOWN-ZERO ARM IS CLEAN AT n=1,080 (+0.83 / +1.39 / −0.37),
SO THE −7.04 pp IS THE BUILD'S AND NOT THE FIXTURE'S.** `KILL_TARGET`'s tracked metric falls
from 31.1% to 24.1% and the median kill goes 191 → 236, past the r180 target and past the
baseline by 45 rounds.

⚠ **`DEFENCE_ADMISSION_BAR` — THE RESTATEMENT THE DEFF CLAUSE REQUIRES.** The r300 ITT primary
reads −3.43 pp with a half-width of 4.18, i.e. **a FAIL-TO-EXCLUDE, not a pass.** Per CLAUDE.md
that class must be restated as an exclusion before any correction is applied, and restated
(*"does the CI exclude a regression at r300?"*) **it does not**: the interval spans −7.61 to
+0.75. **This report does NOT claim v521 clears the admission bar; it claims the point estimate
is negative and the interval is uninformative at this n.** The tracked k≤200 metric is not
uninformative and it is negative.

### PER MAP — wins/180 [k≤300] {k≤200}

| map | baseline | **v521 FIRED** | flagoff |
|---|---|---|---|
| atoll | 101 [59] {36} | 107 [54] {28} | 117 [59] {32} |
| drakkarfjord | 171 [137] {130} | 170 [113] {**72**} | 168 [141] {134} |
| glacierkeep | 145 [101] {68} | **157** [107] {73} | 147 [118] {90} |
| midgard ⚠ | 89 [56] {27} | 90 [52] {23} | 90 [45] {15} |
| nordkap | 134 [89] {64} | 134 [82] {**45**} | 130 [84] {66} |
| yulerune ⚠ | 74 [43] {11} | 72 [40] {19} | 71 [34] {14} |

⭐ **drakkarfjord is where the regression lives: k≤200 goes 130 → 72 of 180** — the map v520 moved
most (62 → 154) is the map v521 gives back — with nordkap second (64 → 45). **Both are maps where
the plank runs longest.** midgard and yulerune are the `FS_V519_CRIPPLE_MAPS` internal control and
read flat (89→90 and 74→72 wins), which is the right shape for a change that acts only where the
plank runs, and it is corroborated by the mode-selector battery's 0-of-24 instrument reading on
both.

### THE PHASE BUDGET — `phase.py`, replay-side, n=1,080/arm

Kill mark cross-checked against the grid TSV in all 3,240 games: **1 alarm in 3,240** (in the
flagoff arm), and the `tsv_turn − walker_round` histogram is the single value `{1: …}` in every
arm.

| arm | med ARRIVE | med SENT | med FUNDED | med KILL | arrive→sent | sent→funded | **funded→kill** |
|---|---|---|---|---|---|---|---|
| baseline | 14.0 | 80.0 | 80 | 190.0 | 63.0 | 0 | **69.0** |
| **v521 FIRED** | 14.0 | 81.0 | 84 | **235.0** | 68.0 | 0 | **100.0** |
| flagoff *(known-zero)* | 14.0 | 76 | 76.5 | 184 | 63 | 0 | **69** |

⛔⛔ **THE WHOLE REGRESSION IS ONE CELL: `funded → kill` 69 → 100 ROUNDS (+45%), against a
known-zero control at 69.** Arrival, first-sentinel and first-funding are all unchanged. **The
turret is bought and funded on schedule and then takes half again as long to kill**, which is
precisely what holding `8 × bar + 6` back from `convert_ammo` instead of `2 × bar` does to the
shot cadence: the magazine's own comment prices this at *"the difference between a r114 kill and
a r184 one"*.

---

## ⭐⭐⭐ SINGLE-FLAG ISOLATION — n=468/arm, FOUR ARMS IN THE SAME BLOCKS ON THE SAME SEEDS

Run because the composite surprised. Seeds 501-539, disjoint from the headline. Each arm is the
FULL tree with exactly one change group left on.

| arm | n | wins | ≤r150 | ≤r180 | **≤r200** | **≤r300** | median kill | our core dead |
|---|---|---|---|---|---|---|---|---|
| baseline (v520-PINCER-ONLY) | 468 | 65.6% | 0.207 | 0.271 | 0.325 | 0.453 | 197 | 133 |
| `iLADDER` — 1a/1b/1c only | 468 | 65.8% | 0.188 | 0.248 | 0.278 | 0.412 | 211 | 131 |
| **`iMAG` — 1d/1e only** | 468 | 63.7% | **0.126** | **0.184** | **0.226** | **0.378** | **243** | 146 |
| `iGATE` — the gate fix only | 468 | 66.9% | 0.201 | 0.252 | 0.301 | 0.427 | 197 | 135 |

| contrast vs baseline | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| `iLADDER` | +0.21 pp (hw 6.08) inside | −4.70 pp (hw 5.88) inside *(under the floor)* | −4.06 pp (hw 6.35) inside |
| **`iMAG`** | −1.92 pp (hw 6.13) inside | **−9.83 pp** (hw 5.73) **OUTSIDE** | **−7.48 pp** (hw 6.31) **OUTSIDE** |
| `iGATE` | +1.28 pp (hw 6.06) inside | −2.35 pp (hw 5.94) inside | −2.56 pp (hw 6.36) inside |

⭐⭐ **THE MAGAZINE RESERVE IS THE ENTIRE REGRESSION AND IT IS OUTSIDE ITS OWN INTERVAL ON BOTH
KILL COLUMNS AT n=468.** Composite k≤200 −7.04; `iMAG` alone −9.83. **The ladder reorders and the
gate fix are nulls**, which is exactly what the deterministic dose test predicted before the
headline ran (`iLADDER`'s dose on the non-gated maps was 0/18).

⚠ **THE HONEST QUALIFIER: this leg has no known-zero arm of its own** (the headline's `flagoff`
is the control for the fixture, on different seeds), so at n=468 — the exact n at which v519
measured its floor — **a single-flag delta under ~6 pp is a DIRECTION, not a separation.**
`iLADDER` and `iGATE` sit under it. `iMAG`'s two kill columns do not.

---

## PER-CHANGE VERIFICATION — mechanism arms, zero-vs-nonzero

**9 arms × 36 games (6 maps × 3 seeds × 2 seats), every instrument ON, vs `_v488beltbreak2`.**
⛔ The win column of a mechanism arm is not read.

| arm | ring rounds | **NEAR** | **HOLD** | **BUYIN** | rungs | **r0′** | r1 | r2 | r3 | r4 | **magRes** | **gatefix** | PARSE_BAD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `mF` all on | 9435 | 533 | 1477 | 2146 | 842 | 15 | 507 | 27 | 291 | 2 | 1739 | 12 | 0 |
| `mSYNC` sync off | 8590 | **0** | **0** | **0** | 747 | **0** | 480 | 37 | 228 | 2 | 2673 | 12 | 0 |
| `mNEAR` | 13459 | **0** | 1207 | 2196 | 1067 | 20 | 725 | 32 | 283 | 7 | 4220 | 12 | 0 |
| `mHOLD` | 11436 | 913 | **0** | 2806 | 898 | 22 | 600 | 31 | 243 | 2 | 2362 | 12 | 0 |
| `mBUY` | 11344 | 522 | 1874 | **0** | 875 | **0** | 521 | 69 | 284 | 1 | 3258 | 12 | 0 |
| `mCOLLAR` | 7835 | 1062 | 1780 | 2273 | 622 | 20 | 368 | 14 | 219 | 1 | **0** | 12 | 0 |
| `mPHASE` | 13683 | 1598 | 2097 | 1560 | 1041 | 19 | 721 | 26 | 270 | 5 | 1597 | 12 | 0 |
| `mGATE` | 9834 | 565 | 1275 | 2268 | 988 | 16 | 649 | 23 | 297 | 3 | 2719 | **0** | 0 |
| `mOff` master off | 11216 | **0** | **0** | **0** | 684 | **0** | 457 | 38 | 186 | 3 | **0** | **0** | 0 |

⭐ **AND `mOff`'s ZEROES ARE REAL, NOT VOID — WHICH IS AN IMPROVEMENT ON v518/v519/v520, ALL OF
WHICH HAD TO RECORD THEIR `mOff` INSTRUMENT COLUMNS AS EMPTY BY CONSTRUCTION.** v521's log flags
are gated on themselves, not on the master, so with `LOKI_FS_V521 = False` the tape still emits
ring rounds (11,216) and rung fires (684) while every mechanism column reads exactly zero. The
denominator is visible, so the zero means something.

⛔ **`mPHASE` DRIVES `magRes` TO 1,597 RATHER THAN 0, AND THAT IS CORRECT, NOT A LEAK.** With the
honest phase off, the collar reserve is still reachable in the states the parent already
publishes as open (`KILL_OPEN` by never-having-sealed, and `RING`). The count falls because most
of its dose came from 1e — which is the dose test's 0-of-12 result restated.

⚠ `rung4` fires 1-7 times per 36 games in every arm. **The sentinel rung is effectively dead at
the bottom of this ladder**, which is a fact about the parent, not about v521, and it is why 1c's
promotion could not buy much.

---

## FLAG-OFF AUDIT

**Structural.** Every v521 guard expression reads `LOKI_FS_V521` (or `FS_V521_*`) at RUN time:
`main.py` at the two gate-fix sites and the magazine floor; `siege.py` at the sync read, the
three ladder clauses and the phase publish. `raid.py` and `eco.py` are byte-identical to the
parent.

**Two additions are not individually guarded, and each is disclosed rather than argued away:**
1. `_v521_sync_state` / `_v521_why` / `_v521_log` / `_v521_rung` are always *called* from
   `_fs_ladder_turn`; each returns/no-ops immediately under its own flag, and the byte-identity
   test below covers it empirically.
2. `_v521_core_resolve` is called only under `LOKI_FS_V521 and FS_V521_GATEFIX`.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v521 flag):

```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v521 derived defaults: 0 []
v520 derived defaults (inherited, must also be 0): 0 []
v519 derived defaults (inherited, must also be 0): 0 []
v518 derived defaults (inherited, must also be 0): 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```

⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see the
known v515 hazard in this very file before its zero for v521 is believed.

**`collide.py`, the mandatory slot-10 pre-flight, driven to BOTH verdicts — and with a row v520's
version did not need:**

| configuration | crew | home ferry | COLLISION | |
|---|---|---|---|---|
| v521 FIRED | True | False | False | PASS |
| v521 master OFF ≡ v520-PINCER-ONLY | True | False | False | PASS |
| **v520 master OFF (crew OFF, home ferry ON)** | **False** | **True** | False | PASS |
| **KNOWN-BAD control** (crew ON at the definition site, read-site fix disabled) | True | True | **True** ⛔ | PASS — *the detector is proved able to see the defect it exists for* |

⛔ **THE THIRD ROW WAS ADDED BECAUSE v521'S FLAG-OFF STATE IS A CREW-ON CONFIGURATION.** Turning
v521 off does not turn the crew off, so without that row the "crew OFF → home ferry ON" half of
the predicate would have gone untested in this build.

**Byte-identity — and it is a STRONGER test than v520's, because the baseline is an independently
constructed tree.** `arms/pinceronly` is `bots/_v520pincer` with the two flags turned off **at
their definition sites**, not a copy of the treatment with an override appended. 12 games,
6 maps × 2 seats, same seeds, randomness off — ours AND the opponent's:

```
NEGATIVE CONTROL  baseline vs baseline (same tree, two runs)  : identical 12 / differing  0
TEST              baseline vs v521 FLAG-OFF                   : identical 12 / differing  0
POSITIVE CONTROL  baseline vs v521 FIRED                      : identical  3 / differing  9
```

⇒ **`LOKI_FS_V521 = False` PLAYS THE v520-PINCER-ONLY BASELINE BYTE FOR BYTE, AND THAT ALSO
CERTIFIES FIRED-CONFIG CORRECTION (i)**: two separately built trees produce the same 12 games.
⚠ The positive control differs in 9 of 12, not 12 of 12 — the 3 identical cells are atoll and
drakkarfjord seat cells where the treatment happened to choose no different action at that seed;
the deterministic dose table above is the proper reading of that number and it is reported there
rather than hidden here.

**Behavioural.** The `flagoff` arm is not a separate leg — it is **the third arm of the headline
grid, in the same blocks, on the same seeds**, at n=1,080 (mandate asked ≥180).

---

## ⛔⛔ THE MODE-SELECTOR ASSERTION (coordinator request, s51) — BOTH STANDDOWN MECHANISMS, DRIVEN TO BOTH VERDICTS

**THE POINT, AND IT IS WHY THE ARCHIPELAGO LEG ALONE WOULD NOT HAVE ANSWERED IT: there are TWO
standdown mechanisms and they are different clauses of `_fs_map_gated`.** `FS_MAP_SKIP` (the
small-board / no-route gate, archipelago) and `FS_V519_CRIPPLE_MAPS` + `FS_V519_MODESWITCH` (the
mode selector, midgard and yulerune). The leaky read sites at `main.py:1000/:1084` are shared and
could bypass either.

**PER-GAME, n=24 per board, every v521 instrument ON. A single leaking game cannot hide in a
mean.**

| board | mechanism | n | games with SYNC521 | with MAG521 | with RUNG521 | with GATEFIX521 | tracebacks |
|---|---|---|---|---|---|---|---|
| **yulerune** | CRIPPLE | 24 | **0** | **0** | **0** | **24** | 0 |
| **midgard** | CRIPPLE | 24 | **0** | **0** | **0** | **24** | 0 |
| **archipelago** | GATED | 24 | **0** | **0** | **0** | **24** | 0 |
| **nordkap** | *neither — POSITIVE CONTROL* | 24 | **24** | **15** | **24** | **0** | 0 |

⇒ **ON BOTH CRIPPLE MAPS AND ON THE GATED MAP, NO v521 SIEGE-PATH CLAUSE FIRES IN ANY GAME, AND
THE CREW SEAT IS REFUSED IN ALL 24.** The assertion fires on the control board, so it has been
seen to produce the other verdict.

**AND THE BUILD-COUNT CENSUS AGREES** (`modeguard.py` — our launchers born far from our own core,
our buildings born inside the enemy ring envelope, our builder bodies that ever reach it; the
reference is the PURE CHASSIS, `LOKI_FERRY_SIEGE_ON = False`, because the chassis raid doctrine
builds forward things on every board and an absolute threshold would be a false alarm):

| board | arm | ferry_laun/game | collar_bld/game | fwd_body/game |
|---|---|---|---|---|
| yulerune | chassis / baseline / **v521** | 0.000 / 0.042 / **0.083** | 14.63 / 20.67 / **12.75** | 3.38 / 3.88 / **3.50** |
| midgard | chassis / baseline / **v521** | 0.000 / 0.042 / **0.375** ⚠ | 14.88 / 13.92 / **11.46** | 3.21 / 3.38 / **3.46** |
| archipelago | chassis / baseline / **v521** | 0.000 / 0.042 / **0.000** | 6.92 / 6.71 / **7.29** | 2.83 / 2.75 / **2.88** |
| **nordkap** *(control)* | chassis / baseline / **v521** | 0.042 / 2.000 / **2.292** | 20.92 / 18.58 / **25.96** | 4.96 / 3.83 / **4.83** |

⚠ **ONE RESIDUAL, DISCLOSED RATHER THAN SMOOTHED: on midgard the far-launcher column reads 0.375
against the chassis's 0.000, and the per-game distribution is `{0: 23, 9: 1}` — ONE GAME BUILT
NINE, which is a ferry-chain shape.** Three things are true about it and the third is why it is
an open item rather than an alarm: (a) the 9-launcher game does not reproduce (`NOISE_ON` is
live, v515 finding 1); (b) the instrumented battery shows **0 of 24 midgard games with any v521
siege clause**, so whatever built them, it was not the ferry-siege plank; (c) it is therefore
either the chassis raid doctrine's own launcher plank reached through a different economy, or an
inherited leak in a code path v521 does not touch. **Not resolved here.**

⛔ **AN EARLIER READING OF THIS TABLE AT n=6 SHOWED v521's `collar_bld` EXCEEDING THE CHASSIS ON
yulerune (21.5 vs 11.5) AND archipelago (14.8 vs 9.5) AND WOULD HAVE BEEN REPORTED AS AN ALARM.**
At n=24 both invert (12.75 vs 14.63; 7.29 vs 6.92). It is recorded because a 6-game cell on this
fixture is not a reading, and the first draft of this section believed it for ten minutes.

---

## GATED CONTROL — archipelago vs `_v468kladturbo`, pooled n=72

| draw | v521 | baseline (v520-PINCER-ONLY) |
|---|---|---|
| seeds 101-118 | 27/36 (75.0%) · k≤300 12 (33.3%) · med 300 | 28/36 (77.8%) · k≤300 17 (47.2%) · med 198 |
| seeds 119-136 | 25/36 (69.4%) · k≤300 18 (50.0%) · med 265 | 25/36 (69.4%) · k≤300 18 (50.0%) · med 202 |
| **pooled n=72** | **52/72 (72.2%)** · k≤300 30 (41.7%) · med 265 | 53/72 (73.6%) · k≤300 35 (48.6%) · med 200 |

0 tracebacks; r1000 5 vs 4. **The result is inside the baseline's gated band on wins (−1.4 pp),
which is the mandate's stated bar for correction (ii).** ⚠ On k≤300 the two draws disagree —
−13.9 pp then 0.0 pp — so the pooled −6.9 pp is the one-draw law, not a reading. **n=72 resolves
nothing on that column and this report does not pretend otherwise.**

### THE SEAT-3 FALSIFIER — and it comes back PARTIALLY, which is disclosed

The mandate's check is *"seat-3 raider spend gone"*. At the DECISION layer it is gone: the
`GATEFIX521` refusal fires in **24 of 24** games on all three standdown boards. At the OUTCOME
layer it barely moves:

| draw | arm | fwd_bodies/game | harvesters/game |
|---|---|---|---|
| d1 | baseline / **v521** | 2.81 / **2.53** | 6.61 / **5.36** |
| d2 | baseline / **v521** | 2.69 / **2.67** | 5.61 / **5.06** |

⛔ **THE SEAT ROLE CHANGES AND THE FORWARD-BODY COUNT DOES NOT, AND THE STRUCTURAL REASON IS
`LOKI_ECO_SEATS = (1, 2, 3)` MEETING A RAID DOCTRINE THAT RECRUITS INDEPENDENTLY.** With the gate
refusing, seat 3 falls through to `elif n in LOKI_ECO_SEATS: self.role = "expand"` — verified —
but `raid.py` decides per round whether the raid is open and replacement bodies join it
regardless of the crew seat, so removing one *issued* raider does not remove one *forward body*.
**And harvesters/game moves the WRONG WAY (−1.25, −0.55).** At n=36 per draw neither column is
resolvable; what the leg establishes is that the decision-layer fix works and that its downstream
economic story is **not** the one the mandate anticipated.

---

## HEAL-BACK AND THE COLLAR — `crip.py`, replay-side, n=1,080/arm

*(Guard: the TEAM-SWAP POSITIVE CONTROL re-reads one game with `our_team` flipped and must move
the columns.)*

| | baseline | **v521 FIRED** | flagoff *(known-zero)* |
|---|---|---|---|
| **median heal-back** | **0.000** | **0.000** | **0.000** |
| share of games heal-back ≥ 0.90 | 18.3% | 14.2% | 13.7% |
| **collar barriers / game** | 16.98 | **18.97** | 16.55 |
| damage we landed on their core / game | 621.1 | **593.9** | 639.1 |
| their belts built / game | 29.68 | 28.66 | 27.89 |
| their harvesters built / game | 5.86 | 5.64 | 5.70 |

⛔ **HEAL-BACK IS A NULL AGAIN, EXACTLY AS IN v520.** The median is 0.000 in all three arms and
v521's ≥0.90 share (14.2%) sits between the baseline (18.3%) and the known-zero arm (13.7%),
i.e. inside the fixture's own spread. ⭐ **What DOES move is the collar-barrier column —
+1.99/game over the baseline and +2.42 over the known-zero — which is the same +9.50 sealed
rounds the OVERLAP instrument measured, seen through a second channel.** And
**`oppcore_dmg` falls 621 → 594**, which is `funded → kill` +31 rounds seen through a third.
**Three independent channels, one story: more collar, less shooting.**

---

## FAILURE REEL — and it reproduces v520's finding on a build designed to prevent it

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in EACH of the six
maps, for the `v521 FIRED` arm**, across the 30 headline blocks. One per map is what stops the
reel being six copies of one board. Ties: lowest block → lowest seed → seat A; no tie occurred.
Replays copied to `reel/replays/` so the rows cannot rot.

| # | game | our core dead | n_seats | sealed_r | livefund_r | **overlap_r** | seal_only | shot_only | dmg/heal on their core | class |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `atoll_s89_B` | r144 | 8 | 0 | 0 | **0** | 0 | 0 | 0 / 0 | NO_TURRET |
| 2 | `drakkarfjord_s30_A` | r307 | 8 | 0 | 0 | **0** | 0 | 0 | 0 / 0 | NO_TURRET |
| 3 | `glacierkeep_s83_A` | r323 | 8 | **22** | **0** | **0** | **22** | 0 | 0 / 0 | **SEAL_SHOT_DISJOINT** |
| 4 | `midgard_s51_B` | r131 | 8 | 0 | **59** | **0** | 0 | **59** | 450 / 336, all non-overlap | HEAL_OUTRUN |
| 5 | `nordkap_s73_B` | r177 | 8 | 0 | **63** | **0** | 0 | **63** | **0** / 0 | NO_TURRET |
| 6 | `yulerune_s10_B` | r121 | 8 | 0 | 0 | **0** | 0 | 0 | 0 / 0 | NO_TURRET *(cripple cell)* |

⭐⭐⭐ **OVERLAP IS ZERO IN 6 OF 6, AGAINST A POPULATION MEAN OF 13.35 AND A POPULATION SHARE OF
39.9% ABOVE ZERO. THAT CONTRAST IS FINDING 1, MEASURED TWICE BY ONE INSTRUMENT.** The reel
convention selects the tail; the tail has no overlap; the population does. v520's reel finding
was true about the games it read and false about the bot.

⭐⭐ **ROWS 3 AND 4 ARE THE TWO HALVES OF THE DISJOINTNESS, SEPARATED FOR THE FIRST TIME.**
`glacierkeep_s83_A` held a simultaneously-sealed collar for 22 rounds with a funded turret alive
for **zero** of them (seal_only 22, shot_only 0). `midgard_s51_B` is the mirror: a funded turret
for 59 rounds with the collar never once sealed (shot_only 59, seal_only 0), 450 damage landed
and 336 healed straight back, **every point of it in a non-overlap round**. Row 3 is v520's
`glacierkeep_s37_A` reproduced on a different seed **under a build designed to prevent it**.

⚠ **ROW 5 IS THE ALARMING ONE AND IT IS NOT A FUNDING FAILURE.** A forward turret alive AND the
magazine holding ≥10 ammunition for **63 rounds**, and **zero damage on their core** in all 63.
AUTOPSY #2 (siting, not presence) in its purest form: bought, funded, and useless. No magazine
plank reaches that.

⛔⛔ **NEW CAUSE TOKEN COINED — `SEAL_SHOT_DISJOINT` — AND THAT IS A DECISION, NOT A FINDING.**
v520 proposed the token and explicitly did not coin it (*"It is NOT coined here"*). Row 3 is the
first game whose failure is not describable by any existing token — the collar closed, nothing
shot through it, and neither `NO_TURRET` (a turret existed in the match) nor `MAG_STARVED` (the
magazine was not the binding constraint) fits. **The builder may want to reject the coinage;
`corpus/failure_reel.tsv` is append-only and the row is there.** Six rows appended (69 → 75
lines, readback verified: 8 fields per row, all six replay paths resolve).

---

## SURPRISES (written down before being explained away)

1. **⭐⭐⭐ THE MANDATE'S PREMISE WAS A SELECTION ARTEFACT.** Parent OVERLAP is 13.35 rounds/game
   and 39.9% of games are above zero, not ~0. Nobody predicted that the reel's headline number
   would be a property of the *reel convention* rather than of the bot — and it is, demonstrably,
   because this build's own reel returns 0 of 6 on the same instrument.
2. **⭐⭐⭐ THE FUNDED TURRET IS WHAT STARVES THE SEAL.** Nobody predicted that the collar's
   failure to close under a live turret would turn out to be *caused by our own magazine floor*.
   `_v521_why`'s modal NEAR round is `ti=14 price=20`, and `ti` is pinned at exactly
   `FS_MAG_REPAIR_BARRIERS × bar`.
3. **⛔⛔ TWO LADDER DESIGNS WERE MEASURED INERT BEFORE A HEADLINE GAME WAS PLAYED.** 0 of 18
   deterministic games changed a byte on the three maps where the sync state fires. The win
   column would have called that a clean null at any n while the report claimed three working
   clauses.
4. **⛔⛔ `FS_PH_KILL` CONFLATES "A TURRET IS ALIVE" WITH "THE COLLAR IS SHUT".** A game whose
   collar closed once at r30 and broke at r34 publishes KILL for the next 900 rounds. Every
   consumer asking the phase whether the collar is shut has been getting the wrong answer, and
   the seal-shot disjointness has a *data* form as well as a scheduling one.
5. **⭐⭐ THE REFRAME'S THESIS IS CONFIRMED WHILE ITS PLANK FAILS.** 6.97 net damage per overlap
   round against 1.13 per non-overlap round, stable at 6.90 / 7.05 in the other two arms. The
   mandate predicted 4.8-9.0. **The currency is real; this build cannot buy it.**
6. **⛔ FIXING THE GATED LEAK CHANGES THE SEAT AND NOT THE FORWARD-BODY COUNT.** `LOKI_ECO_SEATS`
   contains 3 so the role genuinely changes, but `raid.py` recruits replacements independently,
   and harvesters/game moved the *wrong* way.
7. **⭐ `mOff`'s INSTRUMENT COLUMNS ARE REAL ZEROES FOR THE FIRST TIME IN FOUR BUILDS.** v518,
   v519 and v520 all had to record theirs as void-by-construction. Gating the log flags on
   themselves rather than on the master costs nothing and makes the master-off zero readable.
8. **⛔ A 6-GAME CELL PRODUCED A FALSE ALARM THAT SURVIVED TEN MINUTES.** The mode-selector
   census at n=6 showed v521 exceeding the pure chassis on two boards; at n=24 both inverted.
9. **⚠ ONE MIDGARD GAME IN 24 BUILT NINE FAR-LAUNCHERS** — a ferry-chain shape on a map where the
   instrumented battery shows 0 of 24 games with any siege clause. Unexplained.
10. **rung 4 fires 1-7 times per 36 games in EVERY arm.** The sentinel rung is effectively dead
    at the bottom of this ladder, which is why 1c's promotion could not buy much and is a fact
    about the parent.

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The headline is n=1,080/arm, not n≥900.** Blocks ran at ~26 s, so the extra power was free.
2. **Clauses 1d and 1e are not in the mandate.** The mandate specifies the ladder reorders
   (1a/1b/1c); those were built first, measured inert by the deterministic dose test, diagnosed
   with `_v521_why`, and 1d/1e are what the diagnosis produced. Reported as such, with the dose
   table for the discarded designs.
3. **The symmetric trigger's WALK half was dropped as a measured duplicate** of v516
   `FS_V516_SENTREACH` + v518 `FS_V518_EARLY_REACH_FIRST` — the mandate's own instruction
   ("measure, don't duplicate").
4. **Mechanism arms are 36 games each, not 15.** Games cost ~1.3 s; the extra power was free and
   the zero-vs-nonzero columns are stronger for it.
5. **The single-flag isolation ran REGARDLESS of the composite's sign** (v520's convention).
6. **The mode-selector battery is new** (coordinator request, s51) and carries its own positive
   control on nordkap.
7. **A new cause token was coined.** Flagged as a decision, not presented as routine.
8. **Timeouts are not reported** (v518 finding 0).

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⚠⚠ `FS_PH_KILL`'s SEMANTICS ARE A SHARED-CHANNEL CHANGE AND 1e MOVES THEM.** The magazine's
   `armed` term reads `SEALED <= ph <= KILL` and goes False at `KILL_OPEN`; only the v516
   GLOBALSENT disjunct keeps the magazine armed there, and `_fs_salt_ok` stops latching
   `fs_sealed_rnd` on an open collar. **Both of those are arguably corrections** — the salt latch
   exists to say the collar is shut — but they are changes to a channel five planks read.
   **1e is worth keeping even if 1d is dropped, and that is a separable decision this report does
   not take.**
2. **⚠⚠ `FS_MAG_REPAIR_BARRIERS = 2` IS NOW KNOWN TO BE PRICED AGAINST A PREMISE THAT DIED AT
   v515.** This report's answer to it (hold the whole collar) is measured at −9.83 pp on the
   tracked metric and should NOT be shipped. **But the premise is still false and the constant is
   still unswept.** The space between 2 and 8 barriers is untouched, and so is the option of
   holding the collar price only while `orth_open` is small rather than whenever it is nonzero.
3. **⚠ THE NEW TOKEN.** See the reel. `SEAL_SHOT_DISJOINT` is coined and appended; rejecting it is
   a one-line edit and the builder's call.
4. **⚠ `R1000_IS_DEFEAT` READS UNFAVOURABLE AND IS RECORDED AS SUCH**: median kill 191 → 236,
   k≤200 31.1% → 24.1%. **`DEFENCE_ADMISSION_BAR` (r300, ITT) is a FAIL-TO-EXCLUDE and is
   restated as an exclusion in the panel section rather than banked as a pass.**
5. **⚠ `SHIP_BAR` IS NOT ADDRESSED AND MUST NOT BE READ INTO THIS REPORT.** A 6-map grid is
   explicitly a non-arming read in `PROGRAMME.md`.

## OPEN ITEMS

0. **⭐⭐ THE CURRENCY IS CONFIRMED AND UNCLAIMED.** 6.97 net damage per overlap round against
   1.13 outside. **39.9% of games already have overlap; 60.1% have none.** The plank that moves
   that share is still unbuilt, and this report closes one road to it (magazine reserve) and
   measures another as inert (ladder reorder).
1. **⛔ `adj = 0` IS THE UNTOUCHED HALF OF THE DIAGNOSIS.** In the modal NEAR round the body is
   not orthogonally adjacent to any open seat. That is a WALKER question — `_fs_stand_target` —
   and no clause in this build addresses it. **It is the more promising of the two blockers
   precisely because nothing has tried it.**
2. **`FS_MAG_REPAIR_BARRIERS` is unswept between 2 and 8**, and the "hold the collar price only
   while orth_open is small" variant is unbuilt.
3. **`FS_V521_SYNC_NEAR` (2), `FS_V521_FUND_AMMO` (10), `FS_V521_BUYIN_MAX_RND` (400) and
   `FS_V521_HOLD_FUNDED` (False) are UNSWEPT.**
4. **The 9-far-launcher midgard game** is unexplained (§ mode-selector).
5. **The gate fix's downstream economics are unmeasured**: harvesters/game moved the wrong way at
   n=36/draw and `raid.py`'s independent recruitment means the seat change does not remove a
   forward body.
6. **rung 4 is effectively dead** (1-7 fires per 36 games in every arm), inherited and untouched.
7. **Inherited and untouched:** every v520 open item except 7 (the gated leak, closed here) and 0
   (the reframe, addressed and answered negatively).

---

## ARTIFACTS

`scratchpad/s51_v521_build/` —
`arms/` (pinceronly = the definition-site baseline, flagoff, chassis, the nine mechanism arms,
the three isolation arms, the eq/determinism arms, the instrumented and `why` arms),
`grid/` (30 headline blocks × 3 arms, **all replays kept**),
`iso/` (13 blocks × 4 arms), `gated/` (2 draws × 2 arms), `mech/` (9 arms),
`mode/` + `modeassert/` (the mode-selector battery, 4 boards × 3 arms + the per-game instrumented
battery), `eq/` (byte-identity + its negative AND positive controls + `eq/dose/`, the
deterministic dose test), `reel/replays/` (6 replays),
`overlap_*.tsv`, `crip_*.tsv`, `PARENT_FREEZE.md5`, `TREE_FINAL.md5`, `PIDS`.

**Instruments, each guarded both ways:**
* `overlap.py --selftest` — eight guards: ringwalk's own selftest in place, a known synthetic
  tape, a MUTATION control (strip the funding → overlap 0 and the damage moves to `net_out`), a
  SIMULTANEITY control (sealed and funded but never together → overlap 0 with both marginals
  positive — the reel's finding as a unit test), a ZERO-DENOMINATOR control returning `None` not
  0, an ENEMY-ONLY control, a real-data TEAM-SWAP positive control, and a CHANNEL CROSS-CHECK
  (−18 `UpdateHp` on the enemy core == `FireTurret` core hits). ⛔ G2's first draft asserted
  `funded_r == 4` and the guard caught the author's own arithmetic before any data was read.
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive
  control (2 hits, which is what makes the v521 zero mean something).
* `collide.py` — the slot-10 two-writer pre-flight, four configurations, both verdicts, including
  a reconstructed KNOWN-BAD form that must read `COLLISION: True`.
* `mechread.py --selftest` — a synthetic tape through every counter, a FULL mutation control
  (every counted line retagged → every column zero), a SINGLE-COLUMN mutation, and a malformed
  line that must be REPORTED as `PARSE_BAD` rather than swallowed.
* `modeguard.py --selftest` — a team-swap control that must move the columns and an ENVELOPE
  control (`ring_dsq = 0` must drive two columns to zero), plus the nordkap positive control on
  the assertion itself.
* `seat3.py --selftest` — team-swap plus an envelope control.
* `drive_eq.sh` — determinism with a negative control (same tree twice) AND a positive control
  (baseline vs FIRED must differ).
* `eq/dose/` — the deterministic dose test, which is this build's most load-bearing instrument
  and killed two designs.
* `phase.py` — synthetic empty/known/ordering guards plus the real-data kill-mark cross-check
  against the grid TSV: **1 alarm in 3,240 games at a single consistent offset.**
* `crip.py --control` — the TEAM-SWAP positive control.
* `_v521_why` (in-tree, `FS_V521_WHY_LOG`) — the counterfactual blocker tape, built because
  neither the win column nor the rung tape could say why a reorder was inert.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* **v521 SYNC composite: REJECTED — a real KILL_TARGET regression** (k≤200 −7.04 OUTSIDE,
  median 191→236, funded→kill 69→100), attributed cleanly to the magazine collar reserve
  (iMAG carries all of it; ladder reorders null). The sync clauses do not ship.
* **The overlap THESIS survives its own premise's falsification**: v520's "0/119" was a reel
  selection artifact (true parent overlap 13.35 rounds/game) — but net core damage is 6.97
  per overlap round vs 1.13 outside, a stable 6× gap. Overlap remains the currency; ladder
  reordering is not the lever.
* **The measured lever for v522**: our own magazine floor starves the seal — modal NEAR
  round reads ti=14 vs barrier price 20, the bank pinned at FS_MAG_REPAIR_BARRIERS×bar whose
  licensing premise died at v515. Fix the floor, not the ladder. PHASE_HONEST (1e) is a
  separable semantics fix five planks read — keep. Gate fix (ii) verified both mechanisms
  (cripple 0/24 siege clauses on yulerune/midgard — Magnus's replay observation confirmed
  by instrument — and gated 0/24) — keep.
* NEXT PARENT = v521 tree with SYNC OFF (= v520 pincer-only + leak fix + PHASE_HONEST).
* METHOD PROMOTED: the deterministic dose test (noise-off, same seeds, replay bytes diffed)
  killed two designs before a single headline game — adopt as a standard pre-headline gate
  for any behaviour clause. SEAL_SHOT_DISJOINT token: accepted as coined.
