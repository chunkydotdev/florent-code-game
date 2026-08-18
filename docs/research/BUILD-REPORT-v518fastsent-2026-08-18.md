# BUILD REPORT (DRAFT) — `bots/_v518fastsent` (the 81-round gap), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v517twin` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v518_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2`, `_v515ecosalt`,
`_v513siegecrew`, `_v514ferrycrew`. Master `LOKI_FS_V518`; False reproduces the parent
(structurally audited, AST-scanned and behaviourally measured below). Scratch:
`scratchpad/s51_v518_build/`. PAR=4 (headline 4 arms × PAR 2). Recorded PIDs in
`scratchpad/s51_v518_build/PIDS`. `scratchpad/overnight*` and corefill untouched.*

*Diff vs parent: doctrine +204/−0 (comment + 8 constants), siege +252/−5, main +62/−0,
`raid.py` and `eco.py` BYTE-IDENTICAL to the parent (0/0).
**0 tracebacks and 0 no-winners in every leg — 3,576 games with a result row** (1,800
headline + 216 gated + 360 + 360 + 450 flag-off + 180 mechanism + 30 decomposition baseline +
180 determinism, plus the 1-game TLE probe). ⛔ **TIMEOUTS ARE NOT MEASURABLE ON THIS FIXTURE AND
"0 timeouts" HAS NEVER BEEN A MEASUREMENT — see finding 0.***

---

## ⛔⛔ FINDING 0 — "0 TIMEOUTS" IS A CONSTANT COLUMN ON EVERY LOCAL GRID THIS PROJECT HAS RUN

Every build report in this line, this one included, reports tracebacks and timeouts together.
Tracebacks are real: `run_grid.py` counts `Traceback` in stderr and the count moves. The
timeout column has never been able to move, and it was driven to the other verdict before it
was trusted:

`scratchpad/s51_v518_build/probe_tle/` is a two-line `Player` whose `run()` executes a
four-million-iteration loop — hundreds of times the 10 ms budget — fired against
`_v488beltbreak2` on glacierkeep with `--tle 10`:

```
  Winner: _v488beltbreak2  (Core destroyed, turn 127)
                   probe_tle    _v488beltbreak2
  Titanium     810 (0 mined)    69 (1160 mined)
  Units                    0                  8
stderr: 1 line, the pip upgrade notice.  stdout: no timeout, TLE, or interrupt string.
```

⇒ **The TLE is ENFORCED — the probe never completed a single `run()`, spawned nothing, mined
nothing — and it is NOT REPORTED.** There is no engine-side string to grep. Compounding it,
`ct.get_cpu_time_elapsed()` returns 0 under local `fcode run` (documented in this tree's own
`doctrine.py:1072`), so the bot cannot self-report either. **A local grid can only observe a
timeout as a behavioural anomaly (a unit that never acts), never as a count.** Every "0
timeouts / 0 tracebacks" line in v515–v517 is therefore one real measurement and one constant
column printed beside it. This report states tracebacks only.

---

## ⛔⛔ FINDING 1 — THE DECOMPOSITION REFUTES THE MANDATE'S PREMISE FOR CHANGE 2, BEFORE CHANGE 2 WAS BUILT

The mandate ordered the 81-round `arrive → sent` gap decomposed *first*, into gate-wait /
siting-wait / funding-wait / raider-busy-sealing, and routed change 2 off the rush autopsy's
#2: *"the raider seals first and only considers turret sites under its own hand late"*.

`FS_V518_GAPLOG` emits one line per RING round carrying the FIRST reason no forward sentinel
was bought that round, joined to the replay's own `arrive`/`sent` marks (`gapdecomp.py`;
codes and their test order are in `siege.py:_v518_gap_log`). Fired on a 30-game grid with the
v518 behaviour flags OFF — i.e. **parent behaviour with the instruments on** — vs
`_v488beltbreak2`:

### THE BEFORE TABLE (`GAPDECOMP_BEFORE.txt`), 18 games that bought a forward sentinel, 2,435 window rounds, median window 74.5

| code | rounds | share | what it means |
|---|---|---|---|
| **NOBODY** | 1,228 | **50.4%** | no raider of ours was taking a ring turn at all |
| **GATE** | 627 | **25.7%** | neither disjunct of the v515 sentinel gate was open |
| **FUND** | 460 | **18.9%** | a disjunct WAS open and the money test refused |
| DODGE | 90 | 3.7% | the round went to the dodge (rung 0) |
| SITE | 20 | 0.8% | no legal aligned site under the body's hand |
| **BUSY1 + BUSYW + BUSY23** | **7** | **0.3%** | **the collar took the action** |

⇒ **PRIORITY CONTENTION IS SEVEN ROUNDS IN 2,435. The collar is not what delays the turret.**
Changes 2(a) and 2(b) as mandated address **1.1%** of the phase they were built to move. They
still ship — bounded, sub-flagged, mutant-driven, and a measured null on a 1.1% ceiling closes
a road the autopsy left open — but they are not the plank and the report does not present them
as one.

**The `NOBODY` bucket is an ABSENCE and is bounded, not asserted.** A replay-side cross-check
counts the window rounds with no GAP518 line *that nevertheless had a builder bot of ours
inside d²≤8*: **103 of 1,228 (8.4%)** on this cut. **75 of the first 180 such rounds are the
one-round arrival seam** (the bot logs at ITS turn, the replay row is end-of-round state, so
the round a body first steps inside d²≤8 has no line); the rest are bodies inside d²≤8 that
were not taking a ring turn (`at_ring = fs_arrived and d <= FS_RING_HOLD_DSQ`, `siege.py:882`).
The residual is arm-dependent and is largest where the window is shortest — **51.8% of a much
smaller NOBODY count in the floor-0 arm**, where the median window is 54.5 rounds. **Read
NOBODY as an upper bound on "no raider at the ring"; its floor is ~48% of the window on the
parent cut.**

### AND THE OBVIOUS RETARGET WAS PRICED AND DROPPED BEFORE IT SHIPPED

`FUND` is `_fs_sentinel_ok`'s reserve, `ti >= len(needed)*bar + sen + floor`, and v517 already
carries the device that caps it (`FS_V517_TWIN_NEEDED_CAP = 2`, for the twin). A cap flag was
written into `doctrine.py`, priced against all 1,653 FUND rounds in the same tape by replaying
the reserve test at each capped value, and **removed again**:

| cap | FUND rounds the reserve test would have passed | share |
|---|---|---|
| 8 (parent) | 0 / 1,653 | 0.0% |
| 4 | 24 | 1.5% |
| 3 | 34 | 2.1% |
| 2 | 56 | 3.4% |
| 1 | 92 | 5.6% |
| **0 (collar term deleted entirely)** | **169** | **10.2%** |

**Median bank across FUND rounds is 41 Ti against a median sentinel price of 79.** The blocker
is not that the collar is holding the money; it is that **we do not have the turret's price**.
Deleting the reserve outright recovers 10.2% of FUND = **1.9% of the gap**. A plank measured
at 0.4% of its target before it runs is a plank that spends an arm to confirm arithmetic.

⇒ **What survives as addressable is `GATE` (25.7%), and `FS_SENT_RND_FLOOR` is the only
constant in it that has never been swept. That is change 1, and it is the centrepiece.**

---

## ⭐⭐ CENTREPIECE — THE THREE-POINT FLOOR DOSE-RESPONSE, n=450/arm, FOUR ARMS CONCURRENT PER BLOCK

15 blocks × 30 games, 5 siege maps × 3 seeds × 2 seats, vs `bots/_v488beltbreak2`. All four
arms run **inside the same block on the same seeds**, because `--seed` does not pin a game
(the spawn salt is re-rolled from OS entropy per match, v515 finding 1) — a shared seed buys
the map and the pairing only, and adjacency in time is what keeps machine load from separating
the arms. The three v518 arms are IDENTICAL except for `FS_SENT_RND_FLOOR`.

| | **parent (`_v517twin`)** | **v518 floor 60** | **v518 floor 45** | **v518 floor 30** |
|---|---|---|---|---|
| WINS | 237/450 (52.7%) | **240/450 (53.3%)** | 227/450 (50.4%) | 212/450 (47.1%) |
| **kills ≤ r300 (ITT primary)** | 125/450 (27.8%) | 132/450 (29.3%) | **139/450 (30.9%)** | 110/450 (24.4%) |
| **kills ≤ r200 (KILL_TARGET tracked)** | 72/450 (16.0%) | **82/450 (18.2%)** | 78/450 (17.3%) | 60/450 (13.3%) |
| **median kill round** | 261 | 240 | **237** | 259 |
| total core kills | 216 | 212 | 207 | 182 |
| our core destroyed | 195 | 191 | 202 | **227** |
| r1000 games | 39 | 47 | 41 | 41 |
| wins on the r1000 tiebreak | 21 | 28 | 20 | 30 |
| tracebacks | 0 | 0 | 0 | 0 |

**Deltas vs the parent, with two-sample naive half-widths** (local pair-weighted DEFF = 0.98,
s39 audit, so the platform constants 1.53/1.83 do **not** apply and are not used):

| arm | Δ wins | Δ k≤300 | Δ k≤200 |
|---|---|---|---|
| floor 60 | **+0.7 pp** (hw 6.5) | **+1.6 pp** (hw 5.9) | **+2.2 pp** (hw 4.9) |
| floor 45 | −2.2 pp (hw 6.5) | +3.1 pp (hw 5.9) | +1.3 pp (hw 4.9) |
| floor 30 | **−5.6 pp** (hw 6.5) | −3.3 pp (hw 5.7) | −2.7 pp (hw 4.6) |

**EVERY DELTA IS INSIDE ITS INTERVAL, floor 30's −5.6 pp only just.** ⚠ **Power, stated
honestly: at n=450/arm this fixture cannot resolve anything under ~6 pp on wins, and v517
demonstrated a SIGN FLIP between two fixtures of provably identical code at this size.** What
the table can support is the SHAPE — three points, monotone, and the shape is the same on
wins, on kills, and on our own deaths.

### KILL-ROUND CDF against the `KILL_TARGET` marks (share of **ALL** games killed by R)

| arm | ≤r150 | **≤r180** | **≤r200** | ≤r250 | **≤r300** | ≤r400 | ≤r500 |
|---|---|---|---|---|---|---|---|
| parent | 20 (0.044) | 51 (0.113) | 72 (0.160) | 103 (0.229) | 125 (0.278) | 177 (0.393) | 198 (0.440) |
| **floor 60** | 24 (0.053) | 52 (0.116) | **82 (0.182)** | 109 (0.242) | 132 (0.293) | 169 (0.376) | 189 (0.420) |
| floor 45 | 26 (0.058) | **60 (0.133)** | 78 (0.173) | 111 (0.247) | **139 (0.309)** | 167 (0.371) | 183 (0.407) |
| floor 30 | 28 (0.062) | 47 (0.104) | 60 (0.133) | 85 (0.189) | 110 (0.244) | 145 (0.322) | 161 (0.358) |

**Against the tracked metric (kills by r200, baseline ~16.5%, target >50%): 16.0 / 18.2 / 17.3
/ 13.3.** The median-kill target of r180 is not approached by any arm (261 / 240 / 237 / 259).
**Four more arms, and the r200 share is still in the 13–18% band every arm this line has ever
measured.**

### ⭐⭐ THE PHASE BUDGET — AND IT IS THE ANSWER TO THE MANDATE

`phase.py`, replay-side, n=450/arm. Marks: ARRIVE = first round a builder bot of ours is
inside d²≤8 of the enemy core; SENT = first round a forward sentinel of ours (d²≤40) is alive;
FUNDED = SENT and team ammunition ≥10; KILL = the round their core reaches 0. Kill mark
cross-checked against the grid TSV in all 1,800 games: **0 alarms, and the
`tsv_turn − walker_round` histogram is the single value {1: …} in every arm** — a consistent
1-vs-0 indexing offset, not a mismatch.

| arm | med ARRIVE | **med SENT** | med FUNDED | med KILL | spawn→arrive | **arrive→sent** | sent→funded | **funded→kill** | games with a fwd sentinel |
|---|---|---|---|---|---|---|---|---|---|
| parent (v517) | 8 | 91 | 91.5 | 258.5 | 8 | **82** | 0 | **97** | 331/450 |
| **floor 60** | 8 | 87 | 87 | 238.5 | 8 | **80.5** | 0 | **97** | 332/450 |
| floor 45 | 8 | 84 | 84 | 236 | 8 | **76** | 0 | **92** | 336/450 |
| **floor 30** | 8 | **71** | **71** | 257 | 8 | **64** | 0 | **112** | **352/450** |

**⭐ THE 81-ROUND GAP IS MOVABLE, AND MOVING IT DOES NOT BUY KILLS.** The floor drives
`arrive → sent` monotonically **82 → 80.5 → 76 → 64** (−18 rounds, −22%), pulls the first
forward sentinel from r91 to r71, and puts one on the board in **21 more games of 450**. And
`funded → kill` grows **97 → 97 → 92 → 112** — at floor 30 the post-turret phase absorbs the
whole gain and then some, which is why the median kill round moves 261 → 259 and the r200
share FALLS.

**`sent → funded` is 0 in all four arms**, replay-side, again. v516's fix is confirmed a third
time and the ammunition path has nothing left to give.

⇒ **THE GAP WAS NEVER THE BINDING CONSTRAINT ON THE KILL CLOCK. It is 45% of the r180 budget
and buying 18 rounds of it back changes the kill round by two.** The r180 target requires
`funded → kill` (92–112 rounds against a heal-matched defender) to move, and that is the heal
economics the autopsy priced at >2:1 against us.

### PER MAP (wins/90, k≤300 in brackets)

| map | parent | floor 60 | floor 45 | floor 30 |
|---|---|---|---|---|
| atoll | 31 (k14) | **47 (k19)** | 36 (k15) | 35 (k17) |
| drakkarfjord | **60 (k33)** | 60 (k35) | 52 (k33) | 44 (k24) |
| glacierkeep | 74 (k42) | 72 (k45) | 69 (k50) | **75 (k44)** |
| midgard | 15 (k8) | 10 (k5) | **17 (k10)** | 6 (k3) |
| nordkap | **57 (k28)** | 51 (k28) | 53 (k31) | 52 (k22) |

**PER BLOCK (wins/30), parent / f60 / f45 / f30:** 15/19/15/14 · 17/17/14/15 · 16/14/16/18 ·
13/17/13/13 · 14/13/19/12 · 14/20/15/17 · 18/18/13/13 · 18/15/16/14 · 12/14/15/13 ·
18/16/15/15 · 15/15/14/14 · 17/14/17/15 · 17/16/15/15 · 17/15/15/14 · 16/17/15/10.
**The four arms trade the lead constantly and no n=30 or n=90 cut of this table is a
conclusion.** atoll's 31 → 47 is the largest single cell in the report and it sits on n=90.

---

## PER-CHANGE VERIFICATION (every mutant driven, zero-vs-nonzero)

Mechanism arms are n=30 (5 maps × 3 seeds × 2 seats), every instrument on in every arm so the
tables are read off the same volume of trace. ⛔ **The win column of a mechanism arm is not
read: it ranges 30.0%–66.7% across six arms of the same family, which is the one-draw law and
nothing else.**

⚠ **AND THE INSTRUMENTED ARMS ARE NOT THE HEADLINE ARMS.** `GAP518` runs a *probed* sentinel
purchase scan every ring round. Local CPU is unmeasurable (finding 0), the platform TLE is
real, so behaviour under logs is not asserted identical to behaviour without them. Every
number in the headline comes from arms with all log flags False.

### 1 — THE FLOOR (`FS_SENT_RND_FLOOR`, no flag; swept as arms)

| arm | floor | games buying a fwd sentinel | window median | GATE% | FUND% | med SENT (replay) |
|---|---|---|---|---|---|---|
| gapbase (parent behaviour) | 60 | 18/29 | 74.5 | 25.7 | 18.9 | — |
| mF (v518 all on) | 60 | 20/29 | 76.0 | 35.2 | 16.5 | 84 |
| mE (EARLYSITE off) | 60 | 25/30 | 75 | 46.3 | 24.3 | 82 |
| **mFloor30** | 30 | 23/30 | **60** | 25.2 | **39.1** | **68** |
| **mFloor0** | 0 | **26/29** | **54.5** | 21.8 | 35.0 | **60** |

**⭐ THE MECHANISM IS EXACTLY WHAT THE DECOMPOSITION PREDICTED: the floor converts GATE rounds
into FUND rounds.** GATE falls and FUND rises as the floor drops, the window shortens
74.5 → 60 → 54.5, and the share of games that ever buy a forward sentinel rises 18/29 → 26/29.
**A lower floor does not conjure money; it moves the wait from "the gate is shut" to "the bank
is short".** `mFloor0` is also the v514 reproduction control — floor 0 is the configuration
that scored −14/60 in v514 — and it reproduces the early buying (min first-sentinel round
**r8**, against r57 for the parent).

### 2 — ARRIVAL-PATH TURRET SITING (`FS_V518_EARLYSITE`)

**(a) Instrument, both ways.** `EARLY518` fires when the first forward sentinel purchase is
taken ahead of rung 1:

| arm | EARLY518 events / games | sentinel purchases (`TWIN517`) |
|---|---|---|
| `mF` | **17 / 15** | 19 / 15 |
| `mE` mutant (EARLYSITE off) | **0 / 0** | 23 / 18 |
| `mR` (TWINRES off, EARLYSITE on) | **18 / 17** | 19 / 17 |
| `mFloor30` | 21 / 18 | 25 / 19 |
| `mFloor0` | 26 / 22 | 28 / 22 |

Zero-vs-nonzero ✅, and the clause is not marginal: **17 of `mF`'s 19 forward-sentinel
purchases were taken by the early path**, i.e. once the flag is on the first sentinel is
essentially always bought ahead of the collar rather than at rung 4.
⛔ **It is 1.13 firings per firing game, NOT "once per game"** — the clause re-opens whenever
a forward sentinel dies (`live <= FS_V518_EARLY_MAX_LIVE`), which is correct and is a
correction to this build's own first docstring.

**(b) And it moves nothing, exactly as the decomposition said it would not.** Replay-side
median SENT: `mF` 84 vs `mE` 82 vs the flag-off-behaviour `mOff` 86; median `arrive → sent`
76 / 75 / 77. *(⛔ Instrument note: `mOff` sets the MASTER flag False and `FS_V518_GAPLOG` is
gated on the master, so that arm's GAP tape is empty BY CONSTRUCTION — it reads 100% NOBODY
and its decomposition is void. Its phase numbers are replay-side and unaffected. The
parent-behaviour decomposition comes from `gapbase`, which keeps the master ON and turns only
the two behaviour sub-flags off.)* **A change that fires on 17 of 19 purchases and moves the mark by two rounds is
a change whose target was 0.3% of the phase.** The mandate's own instruction to decompose
first is what makes this a measured null instead of a hypothesis.

**(c) The displacement it costs the collar is bounded and was priced, not assumed.**
`_fs_sentinel_ok` reserves `len(needed) * barrier_cost + sentinel_cost` before returning True,
so every purchase this clause takes is one the whole remaining collar was already paid for.
What is skipped is the WAIT (`_fs_seal_pending`), never the funding.

### 3 — THE TWIN RESERVE (`FS_V518_TWINRES`)

**(a) Instrument, both ways.**

| arm | `TWINRES518` rounds / games | rounds the reserve BOUND (raised `ti_floor`) |
|---|---|---|
| `mF` | **286 / 5** | **286 / 286 (100%)** |
| `mR` mutant (TWINRES off) | **0 / 0** | 0 |
| `mFloor30` | 1,000 / 10 | 1,000 |
| `mFloor0` | 1,001 / 12 | 1,001 |

Zero-vs-nonzero ✅. `bind == rounds` on every line: the reserve is never a no-op raised
against a floor that was already higher.

**(b) ⭐ THE BANK ACCUMULATES — v517's "PINNED AT 16" IS FIXED.** v517's own finding was
*"titanium PINNED AT 16 for twenty-five consecutive rounds of a live hold"*. Measured here on
contiguous reserve windows of ≥5 rounds (`bankwatch.py`, guard driven both ways by swapping
the hold column):

| arm | reserve windows ≥5 rounds | **median Ti slope** | windows that REACHED the purchase bar |
|---|---|---|---|
| `mF` | 6 | **+0.89 Ti/round** | 1/6 |
| `mFloor30` | 21 | **+0.45 Ti/round** | **8/21** |
| `mFloor0` | 19 | **+0.67 Ti/round** | 4/19 |
| **pooled** | **46** | — | **13/46 (28%)** |

A worked window from `mF`, four consecutive rounds, ammunition falling while titanium climbs
(the reserve holding the bank while the turret burns the magazine):
```
TWINRES518 91 ti 34 ammo 137 sen 75 bar 7 res 95 floor 95 bind 2
TWINRES518 92 ti 54 ammo 127 sen 75 bar 7 res 95 floor 95 bind 3
TWINRES518 93 ti 54 ammo 127 sen 75 bar 7 res 95 floor 95 bind 4
TWINRES518 94 ti 74 ammo 117 sen 75 bar 7 res 95 floor 95 bind 5
```

**(c) THE TWO ARITHMETIC DEFECTS IN v517'S RESERVE, both visible without a game and both
fixed here** (`siege.py:_v518_twin_reserve`):
1. **v517's reserve is priced BELOW the bar it funds.** `FS_V517_TWINBANK` holds
   `ti_floor >= sen + FS_SENTINEL_TI_FLOOR` (= sen + 4) while the purchase under a hold tests
   `ti >= min(len(needed), 2) * bar + sen + 0` (= sen + 2·bar, and `bar` is 7–9 at the live
   2.6–2.9× scale). In this state `convert_ammo` is the marginal consumer, so the bank
   equilibrates to exactly `ti_floor` — v513 change F measured that equilibrium to the
   titanium. **A reserve 10–18 Ti under the bar parks the bank permanently just short of the
   purchase.** v518 reserves `sen + 2·bar + 6`.
2. **v517 reads a MONOTONE COUNTER for a LIVENESS question.** `SLOT_FWD_GUN` is written only
   as `read + 1` and never decremented. A team that bought two and lost one reads 2 and can
   never reserve for the replacement — the exact state v514 change B (resite-on-death) exists
   to serve. v518 reads the v516 beat (≥1 alive) minus the v517 peer stamp (≥2 alive).

**(d) ⛔ AND THE BANK IS NOT BEING DRAINED BY ANYTHING ELSE, MEASURED — WHICH KILLS v517'S OPEN
ITEM 2.** v517 flagged *"`FS_V517_TWINBANK` stops only ONE consumer; the eco and the collar
keep spending while it banks"*. The `TIWATCH518` tape carries the team's **cost scale** every
round, and every build adds a KNOWN additive increment to that one global factor
(barrier/conveyor/splitter +1, harvester +5, launcher +10, builder bot/gunner/sentinel +20
percentage points), so the round-over-round scale delta says what was bought without
instrumenting a single build site. Over the hold-round transitions:

| arm | hold-round transitions | ammo converted | **nothing built** | barrier/conveyor/splitter | harvester | builder/gunner/sentinel |
|---|---|---|---|---|---|---|
| `mF` (reserve on) | 150 | 159 Ti (1.06/rd) | **132 (88%)** | 14 | 5 | 0 |
| `mR` (reserve off) | 800 | 804 Ti (1.00/rd) | **747 (93%)** | 48 | 4 | 1 |

⇒ **In ~90% of hold rounds NOTHING IS BUILT. The other consumers are not the leak.** What
remains is arithmetic: income during a hold is ~2.5 Ti/round passive plus deliveries, the
conversion tap still takes ~1 Ti/round (the floor holds the bank AT the floor, it does not
close the tap), and the purchase bar is 89–102 Ti. **28% of reserve windows reach it.**

**(e) THE TWIN PURCHASE RATE MOVED OFF 0/80, BUT BARELY.** Sentinel purchases made while a
hold verdict was live: **5 across 180 mechanism games** (mF 0/19, mE 2/23, mR 0/19,
mFloor30 1/25, mFloor0 2/28), against v517's **0 of 80**. **The state is reachable now; it is
still rare.** ⚠ And the arm that produced the most is `mE`, which has the reserve ON and
EARLYSITE off, so this column does not attribute cleanly to the reserve at this n.

---

## FLAG-OFF AUDIT

**Structural.** Every behavioural site is guarded by `LOKI_FS_V518 and FS_V518_<sub>` read at
RUN time — 5 guard expressions across `main.py` and `siege.py`, listed in full:
`main.py:419` (TIWATCH), `main.py:740` (TWINRES), `main.py:823` (TICONV), `siege.py:1509`
(EARLYSITE purchase), `siege.py:1579` (GAPLOG), `siege.py:2349` (EARLYSITE walker term),
`siege.py:3198` (the reserve helper's own early return). The unguarded additions are the
`v518_*` state fields (written but read only under a guard), the `probe=False` keyword on
`_fs_try_sentinel` (default is the parent path; `probe=True` is reached only from the GAPLOG
instrument), and two unconditional CALLS to `_v518_gap_log` / `_v518_gap_mark` whose first
statement is the flag test. `raid.py` and `eco.py` are byte-identical to the parent.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v518 flag):
```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v518 derived defaults: 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```
⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see
the known v515 hazard in this very file before its zero for v518 is believed.

**⚠ DISCLOSURE: the tree was edited MID-HEADLINE and the edit was proved comment-only.** Two
docstring corrections (the "once per game" error in verification 2(a)) were applied to
`bots/_v518fastsent` at ~08:40Z while the headline's `f60` arm was running that tree directly.
Verified by AST equality with docstrings stripped against the pre-edit copy in
`arms/mF`: `siege.py` **True**, `main.py` **True**, `doctrine.py` **True**. No behavioural
byte changed.

**Behavioural.** Three fixtures on three seed ranges compared `LOKI_FS_V518 = False` against a
frozen copy of the parent. **Two are interleaved** (both arms inside the same block, at PAR 2);
the third re-uses the headline seeds against the headline's own parent arm and is therefore
**not time-adjacent**, which is stated because it is a weaker comparison.

| fixture | seeds | flag-off | parent | Δ wins | Δ k≤300 |
|---|---|---|---|---|---|
| FO1, interleaved, n=180 each | 203-220 | 111/180 (61.7%) | 105/180 (58.3%) | +3.3 pp (hw 10.1) | +5.0 pp (hw 9.8) |
| FO2, interleaved, n=180 each | 403-420 | 105/180 (58.3%) | 97/180 (53.9%) | +4.4 pp (hw 10.3) | +5.0 pp (hw 9.3) |
| FO3, NOT interleaved, n=450 each | 1-45 | 243/450 (54.0%) | 237/450 (52.7%) | +1.3 pp (hw 6.5) | +4.2 pp (hw 6.0) |
| **pooled n=810 each** | | **459/810 (56.7%)** | 439/810 (54.2%) | **+2.5 pp (hw 4.8, INSIDE)** | **+4.6 pp (hw 4.5, ⚠ OUTSIDE)** |

Also pooled: our core destroyed 338 vs 339, tracebacks 0/0, median kill 236 vs 257,
r1000 games 60 vs 79.

**⛔⛔ THE POOLED k≤300 DELTA IS OUTSIDE ITS NAIVE INTERVAL AND ALL THREE FIXTURES AGREE IN
SIGN, ON CODE THAT IS BYTE-IDENTICAL IN PLAY. THE PROOF IS IN THE NEXT SECTION AND IT IS THE
STRONGEST FLAG-OFF EVIDENCE THIS LINE HAS PRODUCED.**

### ⭐⭐ FINDING 2 — THE FLAG-OFF TREE PRODUCES 30 OF 30 BYTE-IDENTICAL REPLAYS, AND GETTING THERE FOUND A SECOND RANDOMNESS SOURCE

A win-rate comparison cannot settle a null at any n this fixture can afford, so the question
was asked directly: **run both trees on the same seeds with the randomness switched off and
diff the replay bytes.**

**Attempt 1 failed, and the failure is the finding.** With `NOISE_ON = False` set on OUR tree
in both arms, 29 of 30 replay pairs still differed — **and so did the NEGATIVE CONTROL, the
same arm run twice: 1 identical / 29 differing.** v515 finding 1 says *"`--seed` DOES NOT PIN A
GAME — the randomness is OURS"* (`main.py:781` re-rolls `spawn_salt` from OS entropy per match
under `NOISE_ON`). **The second half of that sentence is incomplete: the randomness is also the
OPPONENT'S.** `_v488beltbreak2` is our own bot family and carries the identical re-roll at
`bots/_v488beltbreak2/main.py:445`. **Disabling our salt alone pins nothing, and a determinism
test that skips its negative control would have read "29/30 differ ⇒ the flag-off is not the
parent" — the exact opposite of the truth.**

**Attempt 2, with the OPPONENT's salt disabled too** (`arms/eq_opp` = `_v488beltbreak2` +
`NOISE_ON = False`), 30 games, 5 maps × 3 seeds × 2 seats:

```
NEGATIVE CONTROL  parent vs parent (same tree, two runs): identical 30 / differing 0
TEST              parent vs FLAG-OFF                    : identical 30 / differing 0
```

⇒ **THE FIXTURE IS DETERMINISTIC (the control proves the instrument can distinguish), AND THE
FLAG-OFF TREE AND THE PARENT PLAY THE SAME 30 GAMES BYTE FOR BYTE.** `LOKI_FS_V518 = False`
reproduces `bots/_v517twin` exactly, on every path either tree took in 30 games across five
maps and both seats. No win-rate battery can make that claim.

⇒ **AND THEREFORE THE +4.6 pp POOLED k≤300 SEPARATION IS A FALSE POSITIVE, CAUGHT IN THE ACT.**
Two trees that play identically separated by 4.6 pp with a 4.5 pp naive half-width at n=810
each. ⚠ **The lesson is about POOLING, not about this build: pooling non-time-adjacent local
fixtures shrinks the naive interval faster than the salt variance shrinks, because the salt
draw is a per-MATCH cluster the naive formula does not model.** v515 measured the same-config
swing at ±3-5 games per 30-block and up to 9 in 90; +5.0 pp at n=180 is 9 games. **Every
pooled local interval in this line's reports — including this one's headline — should be read
with that in mind, and the s39 local DEFF of 0.98 was measured on a balanced-by-construction
shard fixture, not on pooled fixtures run hours apart.**

---

## GATED CONTROL — archipelago vs `_v468kladturbo`, pooled n=72 (two draws of 36)

archipelago's board signature `(26, 26, (5, 5), (19, 19))` is in `FS_MAP_SKIP`, so `_fs_gate`
refuses. Every v518 change is siege-path — the ladder, `_fs_stand_target`, and a Core branch
inside the `fs_live` siege block — so all of it is structurally unreachable here, **including
`FS_SENT_RND_FLOOR`, which is only read inside `_fs_sentinel_ok`.**

| draw | v518 floor 60 | v518 floor 30 | parent (`_v517twin`) |
|---|---|---|---|
| seeds 1-18 | 24/36 (66.7%) | 24/36 (66.7%) | 24/36 (66.7%) |
| seeds 19-36 | 26/36 (72.2%) | 29/36 (80.6%) | 26/36 (72.2%) |
| **pooled n=72** | **50/72 (69.4%)** | 53/72 (73.6%) | **50/72 (69.4%)** |

**The shipped arm lands on EXACTLY the parent's 50/72, and draw 1 is a three-way tie at
24/36.** k≤300 pooled: 37 / 43 / 38; median kill 175 / 171 / 180; 0 tracebacks. **No alarm.**

⚠ **floor 30 reads +4.2 pp pooled on a board where the constant it changes is never read —
which is a demonstration of the one-draw law, not a result.** Its own two draws are 24/36 and
29/36. The two-draw design earns its keep again.

---

## FAILURE REEL — the five worst losses of the best arm

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in each of the
five siege maps, for the `floor 60` arm** (the best arm on wins, 53.3%, and the shipped
configuration). ⛔ The five earliest core deaths *overall* are **all midgard, four of them
seat B** — the autopsy's known "midgard-B is a scripted loss" — so an unfiltered top-5 would
have been five copies of one board. One per map is what makes the reel a reel.

Decoded with the s51 rush-autopsy machinery, **copied not rewritten** (`tape.py`,
`summarise.py`, `attrib.py`, `turrets.py`, `classify.py` into `scratchpad/s51_v518_build/reel/`),
so its guards ran in place: **HP identity 5/5, delta alphabet clean, fireTurret core-hit counts
== UpdateHp −18 counts for both teams 5/5**. Board detail from the per-round `Tape` and
`turret_ledger.tsv`; `narrate.py` adds the hold read. **Everything below is engine-side — the
headline arms run with every log flag False, and platform replays carry no stdout at all.**

**⭐ THE FIREDISC HOLD READ, and its bound is stated:** a funded round with a live forward
sentinel and no shot from its tile. A sentinel reloads 2, so **50% is the pure-cadence
floor** — anything at 50% held nothing.

### 1. `midgard_s1_B` — our core dead r114 — **HEAL_OUTRUN** — *and it contains the FIREDISC answer*
No builder of ours was ever inside d²≤8 of their core in 114 rounds — **zero ring rounds** —
yet a forward sentinel went up at (6,6) at r42 and opened on their core at r43. It landed 26
shots (468 damage) and **they healed 464 of it, 99.1%**; their core bottomed at 254 HP at r91
and recovered. Their first core-hitting turret opened at r81 and put 28 shots = 504 damage
into our core, which is exactly its full HP: we died to one sentinel, on schedule, 33 rounds
after it opened. **The hold read is 46 non-firing funded rounds of 72 = 64%, against a 50%
reload floor — so roughly ten shots' worth of FIREDISC hold, ~100 ammunition, in the one reel
game where the discipline plausibly engaged. It bought nothing: the heal-back stayed at
99.1% and the bank it saved never became a second turret.** A held turret is a building; it
does nothing else with the round. **Known class (autopsy #3), and the v517 open question — what
the bot does during a hold — has the answer "nothing, and the held ammunition did not convert".**

### 2. `atoll_s2_B` — our core dead r128 — **NO_TURRET**
The raider reached d²≤8 at r47 and was there for **3 rounds of 128**. Three sentinels were
built — (12,5) r14, (10,4) r18, (11,3) r54 — and **all three are HOME turrets** (d² 166–204
from their core); they fired 26 shots between them and **not one landed on the enemy core**.
Their turret opened at **r13** and delivered 32 shots. **Known class (autopsy #2), in its
purest form: the money went into turrets, and every turret was pointed the wrong way.**

### 3. `nordkap_s36_B` — our core dead r172 — **NO_TURRET**
The raider arrived at r4 and held the ring for **65 of 172 rounds** — the best presence in the
reel — and still bought no forward sentinel. The one sentinel of the match is at (9,21), d²=210
from their core, i.e. home; it fired 43 shots at nothing that mattered. Two forward launchers
were built at r3 and r8 and each lived exactly 1 round (the ferry hop tearing down, working as
designed). Their turret opened at **r13**. **Known class (autopsy #2), and the interesting
half is that presence was NOT the blocker here — this is a `GATE`/`FUND` game with a live body
standing on the ring.**

### 4. `drakkarfjord_s28_A` — our core dead r180 — **TURRET_LOST** — *the closest loss in the reel*
The raider arrived r10, held the ring 58 of 180 rounds with a 15-round gap. Two home sentinels
went up at r39 and r47 (one of which fired **zero shots in 141 rounds** — a dud). The forward
sentinel finally landed at **(27,7), d²=6.5, r84**, opened at r85 and never died: **48 shots,
864 damage, heal-back 0.667, their core bottomed at 212 HP at r179 — one round before ours hit
zero.** Their turret opened at r125 and needed 28 shots. **The hold read is exactly 48 of 96 =
50.0%, the pure reload cadence: this sentinel held NOTHING and fired every round it could.**
**Known class, but the sharpest instance of the report's own centrepiece: we lost a race by
about 16 shots, and `arrive → sent` was 74 rounds.**

### 5. `glacierkeep_s38_A` — our core dead r376 — **NO_TURRET**
The raider arrived at r8 and was on the ring 28 of 376 rounds (longest absence 18). **Not one
sentinel of either kind was built all game** — the only turret we own is a home gunner at
(13,17) built r28 that fired 42 shots and hit their core zero times. Their first core-hitting
turret did not open until **r321**; we had 313 rounds of a completely uncontested board and
converted none of it. **Known class (autopsy #2) and it is the extreme point of the `NOBODY`
bucket: a 376-round game with 28 ring rounds.**

**NO NEW CAUSE CLASS.** All five fall into classes the rush autopsy already named
(NO_TURRET ×3, HEAL_OUTRUN ×1, TURRET_LOST ×1). ⭐ **The distribution is itself the finding:
three of the five worst losses of our best arm never put a single shot on the enemy core, and
in two of those a live raider was standing on the ring.** Threshold sensitivity: the
classification is unchanged across all nine (FUNDED_MIN, HEAL_MAX) combinations the classifier
sweeps.

Rows appended to `corpus/failure_reel.tsv` (5, append-only).

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The gap decomposition was run on 30 games, not 10.** A local game is ~2 s and `run_grid`
   emits 5 maps × 3 seeds × 2 seats; the extra 20 are free and the buy-games cut needs them
   (only 18 of 29 games buy a forward sentinel at all).
2. **A FOURTH change was written, priced and DELETED before it shipped** (`FS_V518_EARLYFUND`,
   the collar-reserve cap). Finding 1: it prices out at 0.4% of the gap. The mandate ordered
   the decomposition first; this is what the decomposition said. The pricing table is kept in
   `doctrine.py` §2(c) so the road stays closed with its numbers attached.
3. **TWO extra flag-off fixtures were added, and then a DETERMINISM TEST that outranks all
   three.** v517 surprise 5 measured a SIGN FLIP between two fixtures of identical code, so one
   battery cannot settle a null; three still could not (finding 2), and the byte-diff could.
   The determinism test is new to this line and it needed a new arm of the OPPONENT
   (`arms/eq_opp`) to work at all.
4. **`mFloor0` was added as a mechanism arm.** It is not one of the three headline doses; it is
   the v514 reproduction control (floor 0 is the configuration that scored −14/60) and the only
   way to read where `conn2` actually latches.
5. **The gated leg carries `floor 30` as its third arm rather than the flag-off tree.** Every
   v518 change is unreachable on a gated board, so the informative third arm is the one whose
   constant differs most.
6. **Timeouts are not reported** (finding 0). Reporting a column that cannot produce the other
   verdict would be reporting a constant.

## SURPRISES (written down before being explained away)

1. **⛔⛔ PRIORITY CONTENTION IS 7 ROUNDS IN 2,435.** The mandate's routing premise, the rush
   autopsy's #2, and this build's change 2 all point at the collar taking the action that
   should have bought the turret. It happens in 0.3% of the window. Nobody predicted a number
   that small.
2. **⭐⭐ THE 81-ROUND GAP IS MOVABLE AND MOVING IT DOES NOT BUY KILLS.** floor 30 buys back 18
   rounds of `arrive → sent` (82 → 64), puts a forward sentinel in 21 more games of 450, and
   the median kill round moves 261 → 259 while kills-by-r200 FALL 16.0% → 13.3%. `funded →
   kill` grows 97 → 112 and eats the whole gain.
3. **`EARLY518` fires on 17 of 19 purchases and the mark moves two rounds.** A change can be
   completely effective at what it does and still be a null, and this is the cleanest example
   the line has produced.
4. **The bank DOES accumulate under the corrected reserve** (+0.45 to +0.89 Ti/round, 13 of 46
   windows reach the purchase bar) — v517's "pinned at 16" was an arithmetic defect, not a
   fact about the game. **And the twin still almost never gets bought.**
5. **⛔ NOTHING IS BUILT IN ~90% OF HOLD ROUNDS.** v517 open item 2 assumed the eco and the
   collar were draining the bank the reserve was holding. Measured via the cost-scale delta:
   they are not. The leak is the conversion tap plus arithmetic.
6. **Three of the five worst losses of our BEST arm never put a shot on the enemy core**, and
   in `nordkap_s36_B` a raider held the ring for 65 rounds while doing it.
7. **`glacierkeep_s38_A`: 376 rounds, their first core-hitting turret at r321, and we built
   zero sentinels of any kind.** An uncontested board converted at zero.
8. **The local timeout column has never been a measurement** (finding 0), across four build
   reports that printed it.
9. **⛔⛔ A NULL COMPARISON BETWEEN TWO TREES THAT PLAY 30 OF 30 GAMES BYTE-IDENTICALLY READ
   +4.6 pp OUTSIDE ITS NAIVE INTERVAL AT n=810 EACH** (finding 2). Nobody predicted that
   pooling three flag-off fixtures would manufacture a separation the single fixtures did not
   have; it is the counterpart to v517's sign flip and it points the other way — v517 said one
   fixture cannot settle a null, this says pooling several does not fix it either.
10. **⛔ DISABLING OUR OWN SPAWN SALT DOES NOT PIN A GAME.** v515 finding 1 named the randomness
   as ours; the opponent carries the identical re-roll (`_v488beltbreak2/main.py:445`) and the
   negative control caught it — the same tree run twice differed in 29 of 30 games.

## OPEN ITEMS

0. **⭐ THE `KILL_TARGET` ITEM MOVES: it is `funded → kill`, not `arrive → sent`.** This build
   bought 18 rounds of the gap and the kill round did not move, because the post-turret phase
   grew to absorb it. 92–112 rounds from a funded forward sentinel to a dead core, against a
   defender who heals 0.67–0.99 of what one sentinel lands, is the whole remaining budget. The
   autopsy priced the exchange at >2:1 against us and named the three shapes that beat it
   (kill before the healers organise; 2× DPS briefly; **cut the income that pays for heals**).
   Only the third has never been built.
1. **`NOBODY` is 50.4% of the gap and no purchase-side plank can reach it.** v517 open item 1
   said the twin's blocker is the raider's life; this says the FIRST sentinel's is too. The
   reel's `glacierkeep_s38_A` (28 ring rounds in 376) and `atoll_s2_B` (3 in 128) are the
   extreme points.
2. **`FS_SENT_RND_FLOOR` is now SWEPT at four points {0, 30, 45, 60} and 60 is not beaten.**
   45 has the best k≤300 (30.9%) and the best median kill (237); 60 has the best wins (53.3%)
   and the best k≤200 (18.2%). All inside interval. **The dose-response is monotone in SENT
   and non-monotone in outcome — the honest read is that the optimum is at or above 60 and
   this fixture cannot separate 45 from 60.** A floor ABOVE 60 has never been tried.
3. **The reserve reaches its bar in 28% of windows and the twin is still ~0.** The next lever
   is the conversion tap itself (the floor holds the bank AT the floor and still leaks ~1
   Ti/round), or a purchase path that does not need a living raider — v517 open item 1,
   unchanged and now doubly implicated.
4. **`FS_V518_RES_MARGIN`, `FS_V518_RES_TTL` and `FS_V518_EARLY_MAX_LIVE` are UNSWEPT.** The
   first two inherit v517's values and reasoning; the third is 0 by construction of the change.
5. **⚠ POOLED LOCAL INTERVALS ARE A LIVE PROBLEM, not a v518 problem.** Finding 2 produced a
   4.6 pp false positive at n=810 on byte-identical play. The s39 local DEFF of 0.98 was
   measured on a balanced-by-construction shard fixture; nothing has measured a DEFF for
   POOLED, non-time-adjacent local fixtures, and this build's own headline pools 15 blocks.
   **Worth a side-lane measurement: re-run the flag-off byte-identical pair as many pooled
   30-blocks as it takes to get the empirical distribution of a known-zero delta.**
6. **The `NOBODY` residual (3.5–52% arm-dependent) bounds the decomposition's biggest bucket.**
   Tightening it needs the bot to log at the same point in the turn the replay row is taken —
   the same mid-round sampling seam v517 open item 4 records.
7. **Inherited and untouched:** every v517 open item except 2 (measured, closed) and the store
   -width audit item; the atlas routing debt named in v517's builder verdict lines.

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⚠⚠ MAGNUS'S PRIORITY RULING 1 vs `KILL_TARGET`.** Ruling 1 ordered the collar sequence
   **barriers → launchers → sentinels**, and `_fs_ladder_turn`'s docstring says rung 4 is
   *"bottom of the ladder BY DESIGN"*. The `KILL_TARGET` ruling (2026-08-18, same session)
   wants the first funded turret at **≤ r75** against a measured median of r87–91. On the round
   the gate opens those two point in opposite directions. **This build encodes
   sentinel-first-once-gate-open** (change 2(a)) and reports what it cost: **7 rounds of the
   window in 2,435 were collar-contended, so the collision is real in principle and worth
   almost nothing in practice.** The lane should still route it, because the *next* plank that
   wants the turret earlier will hit the same wall with a bigger dose.
2. **⚠ `R1000_IS_DEFEAT` vs `KILL_TARGET`, third session running.** floor 60 takes 28 wins on
   the r1000 tiebreak against the parent's 21 and floor 30 takes 30. Under `R1000_IS_DEFEAT`
   those are defeats we are being paid for; under `KILL_TARGET` they are the failure mode. The
   v517 report flagged this to Magnus twice; it is flagged a third time unresolved.
3. **⚠ THE `DEFENCE_ADMISSION_BAR` READS "PASS" FOR AN ARM THAT LOSES GAMES.** floor 30's
   timely-kill rate (k≤r300) is 24.4% vs the parent's 27.8% — a FALL, so it fails the bar. But
   floor 45 and floor 60 both RISE (30.9%, 29.3%) while floor 45 loses 2.2 pp of games. **A bar
   scored on the kill-share alone admits an arm that is behind on wins**; the intervals cover
   both, so nothing here is a violation, but the shape is worth a ruling before a build is
   banked on it.

---

## ARTIFACTS

`scratchpad/s51_v518_build/` — `arms/` (10: `parent` = a frozen copy of `_v517twin`, `flagoff`,
`f45`, `f30`, and six instrumented mechanism arms), `gapbase/` (the 30-game BEFORE grid with
replays + logs), `mech/` (6 arms × replays + logs), `grid/` (15 headline blocks × 4 arms, **all
replays kept**), `gated/` (2 draws × 3 arms), `fo/` + `fo2/` + `fo3/` (three flag-off
fixtures), `eq/` + `eq2/` (the determinism test and its negative control), `probe_tle/` (the timeout positive control), `reel/` (the failure-reel
workspace: 5 replays, the copied autopsy machinery, its output TSVs and `NARRATE.txt`).

**Instruments, each guarded both ways:**
* `gapdecomp.py` — synthetic known-histogram, hole, never-bought, never-arrived and empty-window
  guards, **plus a MUTATION control: rewriting every code to GATE must move the table** (it
  does: `{GATE:2, BUSY1:1, NOBODY:1, SITE:1}` → `{GATE:4, NOBODY:1}`), plus the replay-side
  `near_bot` cross-check that bounds the `NOBODY` bucket.
* `bankwatch.py` — a synthetic ti/hold series whose two medians must SWAP when the hold column
  is swapped (they do: 20/150 → 150/20).
* `logagg.py --selftest` — full / empty / v517-only tapes must separate on every column.
* `phase.py` — synthetic empty/known/ordering guards plus the real-data kill-mark cross-check
  against the grid TSV: **0 alarms in 1,800 headline games at a single consistent offset**.
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive
  control.
* `summarise.py --selftest` — all-win / all-loss / mixed tapes separate on every column.
* `probe_tle/` — the positive control that proved the timeout column cannot fire.
* `eq/` + `eq2/` — the determinism test and, decisively, ITS NEGATIVE CONTROL: the same tree
  run twice must produce identical replays before "identical" means anything. It read 1/30 in
  `eq/` (instrument blind) and 30/30 in `eq2/` (instrument sound), and only the second run's
  verdict is quoted.
* `reel/` — the s51 autopsy guards run in place: HP identity 5/5, delta alphabet clean,
  fireTurret vs UpdateHp channel agreement 5/5. ⛔ `narrate.py`'s shot walker **failed first**
  (a one-level protobuf walk found zero FireTurret events and reported every funded round as a
  hold, 100%); fixed to the two-level nesting `turrets.py` uses and re-read at 50–64%.

**Other:** `mkarm.sh`, `run_grid.py`, `headline.py`, four drivers (`drive_mech.sh`,
`drive_headline.sh`, `drive_gated.sh`, `drive_flagoff.sh` + `drive_flagoff2.sh` +
`drive_flagoff3.sh`), `chain.sh`, `chain2.sh`, `bankwatch.py`, `gapdecomp.py`, `logagg.py`,
`PARENT_FREEZE.md5`, `PIDS`. Parent md5s re-verified untouched after the final leg.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* v518: NULL on every currency (all arms inside interval; floor 60 = parent-equivalent stays
  the shipped setting). But the build BOUGHT ITS ANSWER: **earlier turrets do not buy kills —
  the gap moved 82→64 rounds and funded→kill grew 97→112 and ate it.** The KILL_TARGET
  binding constraint is now measured to be the HEAL ECONOMICS (funded→kill), not turret
  timing, not funding (v516 fixed), not siting priority (7/2,435 rounds — the raider-seals-
  first hypothesis is dead).
* The gap decomposition's real headline: **NOBODY (no raider at the ring) = 50.4% of the
  turret-gap window** — the midgard arrival/replacement residual is HALF the gap. Raider
  presence, not raider behaviour.
* Twin reserve: v517's two arithmetic defects fixed (reserve priced under the purchase bar;
  monotone-slot liveness), bank slope positive, twins 5/180 under hold vs 0/80 — mechanism
  finally alive, dose still small.
* Instrument corrections adopted: "0 timeouts" was a constant column in four reports (local
  TLE is silent and get_cpu_time_elapsed reads 0 — platform match test remains the ONLY CPU
  read); flag-off byte-identity is now PROVABLE (30/30 identical replays) and the first
  attempt's 29/30-differing-including-control caught the opponent-side salt re-roll fact.
* ROUTE: v519 = the heal-economics pair, both evidence-complete for hours — GUNNER-FIRST
  (income cut: heal costs them 1 Ti per +4HP; shred the belts that pay for it) + MODESWITCH
  (cripple cells {midgard, yulerune} — and the reel says all five worst losses were midgard).
  The NOBODY 50.4% raider-presence gap is v520's mandate.
* Doctrine collisions 1-3 carried to Magnus on the page.
