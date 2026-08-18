# BUILD REPORT (DRAFT) — `bots/_v523eyes` (the team's gates learn to see the second raider), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v522floor` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v523_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2` and
`_x3r0v161gungnir`, and the freeze re-verified byte-for-byte at the end of the build
(**13/13, `2026-08-18T14:15:59Z`**). Master `LOKI_FS_V523`; False reproduces the parent AS
CONFIGURED (AST-scanned and byte-proved below). Scratch: `scratchpad/s51_v523_build/`. PAR=4 on
single-arm legs; the headline runs 3 arms × PAR 4. Recorded PIDs in
`scratchpad/s51_v523_build/PIDS`. `scratchpad/overnight*` and corefill untouched.*

*Diff vs parent: `doctrine.py` +210/−1, `main.py` +79/−6, `siege.py` +425/−4, **`raid.py` and
`eco.py` BYTE-IDENTICAL (0/0, md5 equal to the freeze)**. **6,900 games with a result row across
every leg (grid 3,240 + isolation 2,340 + Gungnir 936 + mechanism 288 + standdown 96), plus 168
replay-only determinism/dose games (eq 60 + dose 108, the eq leg run TWICE — once mid-build and
once against the final tree); 0 tracebacks, 0 no-winners** (counted off
the leg TSVs, not by directory). ⛔ Timeouts are NOT reported — v518 finding 0 proved the local
timeout column is a constant that cannot fire.*

---

## ⭐⭐⭐ THE ONE-PARAGRAPH READ

**THE BLINDNESS IS REAL, THE FIX WORKS AT THE MECHANISM, AND THE WHOLE OF THE HEADLINE'S APPARENT
REGRESSION LIVES ON TWO MAPS WHERE THE PLANK IS PROVED BYTE-IDENTICAL TO ITS PARENT.**
At n=1,080/arm against a byte-identical known-zero arm in the same blocks, the pooled panel reads
**wins −2.13 pp (hw 3.98)**, **k≤200 −2.96 pp (hw 3.88)**, **k≤300 −3.52 pp (hw 4.18)** — all
inside, all negative. **Split on dose, that pooled number stops being one number.** On the four
maps where the ferry-siege actually runs, **wins −0.14 pp (hw 4.38)** against a known-zero arm at
−1.81 pp: FLAT. On the two `FS_V519_CRIPPLE_MAPS` cells — where the standdown assertion measures
**0 of 24 games with any v523 clause on each board**, and where the deterministic fixture proves
v523 plays **byte-identical games to the parent (midgard 2/2, yulerune 2/2 cells)** — **wins
−6.11 pp (hw 7.29)**. ⛔ **A −6.11 pp movement on a subpopulation with a DOSE OF ZERO AND A
BYTE-IDENTITY PROOF is the fixture floor measured inside the headline table, and it is larger than
anything the treatment does where it can act.** The mechanism is not inert: the crew-merged
closure verdict **raises the SEALED rate by +10.18 pp within the fired arm (26.1% → 36.3% of
7,536 at-ring rounds) against +0.00 pp in two known-zero arms with visible denominators**, the
Core's merged phase read wins off body 2's slot **1,384 times in 31,583 reads**, and the corrected
funding predicate **flips the verdict on 292 of 3,749 questions (7.8%)**.
**THE THREE FINDINGS THAT OUTLIVE THE PLANK: (1) the store-blind dose test reads 9 of 36 cells
against a naive 18 of 36 — HALF THE NAIVE DOSE IS PURE CHANNEL, 9 cells whose replay files are
byte-identical between the store-only baseline and the fired build while differing from the parent
in 3,576 bytes at identical file length; (2) `--seed` inertness is independently corroborated —
the three seeds of each pure-channel cell produced IDENTICAL differing-byte counts (6/6/6,
966/966/966, 220/220/220), which is only possible if the same game was played; (3) the failure
reel is overlap-blind for the FOURTH consecutive build (0 of 6 rows, population mean 12.11).**

⚠ **THE ~4.7–5.6 pp SAME-CONFIG FALSE-POSITIVE FLOOR (v519 open item 2) IS CARRIED BESIDE EVERY
CLAIM BELOW.** This build's answer is v520/v521/v522's — a **KNOWN-ZERO ARM IN THE SAME BLOCKS**,
proved byte-identical to the baseline on 12 of 12 games with a negative control — plus, new here,
a **ZERO-DOSE SUBPOPULATION INSIDE THE HEADLINE ITSELF** whose byte-identity is separately proved.
Every contrast is reported twice.

---

## WHAT WAS BUILT

### FIRED-CONFIG CORRECTION (parent-config, not a new mechanism — it defines the baseline)

**`FS_V522_FLOOR = False` at its definition site.** The s51 builder verdict on v522: *"NULL,
exemplary controls (every column inside the known-zero arm's own movement; binding raised 13%→96%
by the pre-headline census and STILL null — the floor was not the constraint). Ships
OFF/indifferent."* Code stays; the flag is the decision. `FS_V521_SYNC` and
`FS_V521_COLLARFIRST` were already False; `FS_V521_PHASE_HONEST` and `FS_V521_GATEFIX` stay on.

### THE MANDATE'S DIAGNOSIS, CONFIRMED AT THE SOURCE BEFORE ANYTHING WAS WRITTEN

v522's report banked two measurements and one unfixed doctrine collision, all of one shape — **a
team-wide question answered off ONE body's word or ONE round's snapshot**:

* *"THE CORE HAS NEVER READ BODY 2's PUBLISH CHANNEL, AND ON NORDKAP THAT IS 60 OF 69 PUBLISHES."*
* Doctrine collision 2: *"`_fs_salt_ok` CALLS THE `SLOT_FS` PHASE 'THE CREW'S SHARED ANSWER' WHILE
  READING ONE BODY'S WORD … It is a bigger lever than anything v522 does."*
* *"THE CORE'S OWN FUNDING RE-CHECK … KILLED 100 OF 100 GLACIERKEEP NEAR ROUNDS"* — `ammo >= 10`
  read one round later measures a spare shot, not funding.

**ROOT-CAUSED, AND THE ROOT CAUSE IS A MISSING MERGE, NOT A TYPO.** `_fs_census` counts
`orth_open` over the whole 12-ring **"from live vision"**, and `_fs_denied`'s own docstring states
its failure direction: *"Unreadable (out of vision) counts as NOT denied, which is the
conservative direction."* Under the v520 PINCER the two bodies stand on **opposite arcs by
construction** (`_v520_claim_arc`, sticky claim, deconflicted) and each seals its own arc first
(`FS_V520_ARC_SEAL`). So *"is the orthogonal-8 closed?"* is answered by ONE body about a curve the
OTHER body is half-way round — and the answer that reaches every consumer is **body 1's**, because
`_fs_state` reads `SLOT_FS`. ⇒ **THE PINCER'S SECOND ARC CAN SEAL PERFECTLY AND NEVER COUNT.**

### CHANGE 1 — `FS_V523_SALTEYES`: the closure census sees both raiders

Two sub-clauses, each separately flagged:

* **`FS_V523_SALT_UNION`** — the literal fix for doctrine collision 2. `_fs_salt_ok` reads the
  phase off **every slot a ferry-siege body publishes into** (`_fs_crew_slots()`), with **the
  freshness test the `SLOT_FS` path does not have**. ⛔ Monotone: a union over a superset of slots
  can only ADD a "sealed" verdict, so the gate opens earlier or identically, never later. With the
  crew off, `_fs_crew_slots()` is `(SLOT_FS,)` and this is the parent read character for character.
* **`FS_V523_ARC_UNION`** — the merge the pincer needs. A body whose OWN arc's seats are all denied
  while the ring is not publishes **`FS_V523_ARC_CLOSED = 3`**. A reader declares the ring closed
  only when **BOTH arcs** are attested by fresh words. ⛔ Both, never one — a single arc-closed word
  sealing the ring would be the same defect with the sign reversed.
* **`FS_V523_PHASE_SEALED`** — the phase machine PUBLISHES the merged verdict as `FS_PH_SEALED`.
  Without this the merge is invisible to every consumer that reads the CHANNEL rather than calling
  the predicate, which is most of them — and the SEALED-rate could not move.

**THE CHANNEL COSTS NO NEW SLOT, NO NEW WRITER AND NO NEW BIT.** The publish word is beat 0-10,
phase 11-13 (**all eight codes taken**: 0-6 plus `FS_PH_DEGRADE = 7`), rid 14-29, arc 30-31 — 32
bits, fully packed, and a store slot is an unsigned 32-bit integer (s50 probe). **The ARC field's
value 3 is the only unused encoding left anywhere in the word.** A body may only publish it after
it has CLAIMED an arc; the claim is sticky for the body's life; the two bodies are deconflicted
onto different arcs. **So a reader holding arc X knows a peer publishing 3 holds the complement.**
⛔ A reader holding NO arc cannot resolve it and therefore does not credit it — a real, bounded
blind spot, stated rather than hidden, and it is why change 2 merges PHASES (which need no such
inference) while change 1 merges ARCS on the raider, where the arc is known.

⛔ **AND THE DECONFLICTION READ WAS FIXED WITH IT.** `_v520_arc_at` is used by `_v520_claim_arc` to
detect a collision and to yield, and its DUP alarm *must be zero*. Overloading the two bits without
touching that read would have made the alarm **go silent for exactly as long as the peer was doing
well** — an alarm that stops firing when the plank starts working is worse than no alarm. It now
maps the closed code back to an identity.

### CHANGE 2 — `FS_V523_CREWREAD`: the Core's consumers read both slots

`_v523_crew_phase` returns the **best fresh phase across `_fs_crew_slots()`**, and the Core's three
consumers use it instead of `_fs_state(ct)`: the **magazine arming term** (the 60/69 nordkap
measurement's own site), the **budget / replacement door**, and the **spawn collar reserve**.

⛔ **"BEST" IS A RANK, NOT A MAXIMUM.** `FS_PH_DEGRADE = 7` is the highest integer and the LOWEST
state; ranking by `>` would let one body's terminal refusal outrank a live body's KILL. The order
is written out in `FS_V523_PH_RANK`.
⛔ **AND THE BEAT RETURNED IS THE WINNING SLOT'S OWN**, not `SLOT_FS`'s — every consumer that tests
staleness tests the freshness of the word it is about to believe. Returning body 1's beat beside
body 2's phase would have been a new instance of the very defect being fixed.

### CHANGE 3 — `FS_V523_COREFUND`: "funded" means funded

`_v523_funded(ct, shots, ti_floor)` asks whether **the magazine plus the convertible bank covers
`FS_V523_FUND_SHOTS` (2) sentinel shots**, instead of whether the magazine happens to hold one
right now. A sentinel shot costs 10 on a 2-round reload, so the magazine cycles 10 → 0 every reload
and an instantaneous `ammo >= 10` is False for half of every cycle **by construction**. Titanium
converts 1:1, at most once per team per turn, usable the same turn and without the core's action
cooldown — so bank above the reserve IS ammunition one round out, and counting it is arithmetic.
It returns **(sustained, spare_shot)** so every caller can log the DISAGREEMENT rather than only
the verdict.

⛔⛔ **AND THE HONEST THING ABOUT CHANGE 3 COMES FIRST, NOT IN A FOOTNOTE: ITS NAMED SITE IS INSIDE
A BLOCK THE PARENT'S OWN VERDICT SHIPS OFF.** The funding re-check lives in the v522 magazine-floor
block, gated on `FS_V522_FLOOR`, which the v522 builder verdict ships **False**. ⇒ **In the fired
v523 configuration change 3 is REACHED ONLY WHEN AN INSTRUMENT FLAG OPENS THE SITE, so the shipped
composite is a DUO, not a trio.** Rather than smuggle it into the composite by turning the parent's
rejected floor back on, it is measured two ways: the mechanism arms force the site open
(`FS_V522_MAG_LOG = True`) and read the flip rate, and **`iFLOORFUND` is a dedicated isolation arm
that turns `FS_V522_FLOOR` back on ON TOP of the corrected predicate** — which is the only
configuration in which change 3 can pay.

---

## ⭐⭐ CENTREPIECE 1 — THE `KILL_TARGET` PANEL, n=1,080/arm, THREE ARMS CONCURRENT PER BLOCK

**30 blocks × 36 games**, 6 maps (the standard 5-map siege grid plus yulerune) × 3 seeds × 2 seats,
vs `bots/_v488beltbreak2`. All three arms run **inside the same block on the same seeds** (`--seed`
does not pin a game, v515 finding 1). A block counts only when all three arms finished all 36
games; **30 of 30 did**.

| | **parent (baseline)** | **v523 FIRED** | **flagoff — KNOWN-ZERO** |
|---|---|---|---|
| WINS | 730/1080 (67.6%) | 707/1080 (65.5%) | 718/1080 (66.5%) |
| ≤r150 | 236 (0.219) | 218 (0.202) | 227 (0.210) |
| **≤r180 (`KILL_TARGET` median mark)** | 302 (0.280) | 282 (0.261) | 286 (0.265) |
| **≤r200 (TRACKED METRIC)** | 343 (0.318) | **311 (0.288)** | 320 (0.296) |
| ≤r250 | 418 (0.387) | 381 (0.353) | 413 (0.382) |
| **≤r300 (ITT primary, `DEFENCE_ADMISSION_BAR`)** | 492 (0.456) | 454 (0.420) | 485 (0.449) |
| **median kill round** | **198** | **211** | 217 |
| our core destroyed | 291 | 321 | 309 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v523 FIRED vs baseline** | **−2.13 pp** (hw 3.98) inside | **−2.96 pp** (hw 3.88) inside | **−3.52 pp** (hw 4.18) inside |
| **flagoff vs baseline** *(byte-identical play)* | −1.11 pp (hw 3.96) inside | −2.13 pp (hw 3.89) inside | −0.65 pp (hw 4.20) inside |

### ⛔⛔⛔ AND NOW SPLIT IT ON DOSE, BECAUSE THE POOLED ROW IS TWO POPULATIONS

midgard and yulerune are `FS_V519_CRIPPLE_MAPS`: `_fs_gate` refuses the board, the ferry-siege
degrades, and **no v523 clause can fire**. That is not asserted — it is measured twice below (the
standdown assertion, 0 of 24 games per board; and the deterministic fixture, where v523 is
**byte-identical to the parent on all 4 midgard/yulerune cells**).

| population | n/arm | arm | wins | k≤200 | k≤300 | median kill |
|---|---|---|---|---|---|---|
| **RUNS** (atoll, drakkarfjord, glacierkeep, nordkap) | 720 | parent | 551 (76.5%) | 295 (0.410) | 387 (0.537) | 162 |
| | 720 | **v523 FIRED** | **550 (76.4%)** | 275 (0.382) | 365 (0.507) | 177 |
| | 720 | flagoff *(known-zero)* | 538 (74.7%) | 287 (0.399) | 394 (0.547) | 168 |
| **ZERO-DOSE** (midgard, yulerune) | 360 | parent | 179 (49.7%) | 48 (0.133) | 105 (0.292) | 261 |
| | 360 | **v523 FIRED** | **157 (43.6%)** | 36 (0.100) | 89 (0.247) | 253 |
| | 360 | flagoff *(known-zero)* | 180 (50.0%) | 33 (0.092) | 91 (0.253) | 281 |

| population | contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|---|
| **RUNS** | v523 vs base | **−0.14 pp** (hw 4.38) inside | −2.78 pp (hw 5.05) inside | −3.06 pp (hw 5.16) inside |
| **RUNS** | flagoff vs base | −1.81 pp (hw 4.44) inside | −1.11 pp (hw 5.07) inside | +0.97 pp (hw 5.15) inside |
| **ZERO-DOSE** | v523 vs base | **−6.11 pp** (hw 7.29) inside | −3.33 pp (hw 4.69) inside | −4.44 pp (hw 6.48) inside |
| **ZERO-DOSE** | flagoff vs base | +0.28 pp (hw 7.30) inside | −4.17 pp (hw 4.62) inside | −3.89 pp (hw 6.50) inside |

⛔⛔ **FINDING 1 — THE HEADLINE'S NEGATIVE SIGN COMES FROM THE HALF OF THE GRID WHERE THE PLANK
CANNOT ACT, AND THAT IS PROVED, NOT ARGUED.** On the maps where the plank runs, v523 is **−0.14 pp
on wins** — flatter than the known-zero arm's own −1.81 pp. On the two cells where the dose is
**exactly zero by two independent measurements**, it is **−6.11 pp**. v522 measured this cell class
at ±8 wins in 180; this build measures **−22 wins in 360**, i.e. the floor is at least as large as
v522 said and this time it happens to point one way. **Nothing in the pooled row survives that
split as a claim about the treatment.**

⚠ **FINDING 2 — WHAT DOES NOT GO AWAY ON THE SPLIT IS THE KILL CLOCK.** Restricted to the
runs-maps, k≤200 reads **−2.78 pp (hw 5.05)** and k≤300 **−3.06 pp (hw 5.16)** — both inside, both
negative, and the known-zero arm reads **−1.11 / +0.97** there, i.e. it does NOT straddle the
treatment on k≤300. Median kill on the runs-maps moves **162 → 177** against a known-zero at 168.
**This is the one column where the treatment's excursion exceeds the control's in the same
direction, and it is reported as such rather than dismissed.**

⚠ **`DEFENCE_ADMISSION_BAR` — THE RESTATEMENT THE DEFF CLAUSE REQUIRES.** The r300 ITT primary
reads **−3.52 pp pooled / −3.06 pp on the runs-maps**, i.e. a NEGATIVE point estimate inside its
half-width. Per CLAUDE.md a fail-to-exclude must be restated as an exclusion before any correction
is applied. Restated (*"does the CI exclude a regression at r300?"*) **it does not** — the
runs-maps interval spans −8.22 to +2.10. **This report does NOT claim v523 clears the admission
bar. It claims the point estimate is negative, the interval is uninformative at this n, and the
known-zero arm's own r300 excursion (+0.97 pp on the same maps) points the other way.**
⛔ Local fixture: the s39 audit measured a pair-weighted local DEFF of 0.98, so the platform
constants (1.529 rated / 1.833 unrated) do not apply and are not used.

### PER MAP — wins/180 [k≤300] {k≤200}

| map | parent | **v523 FIRED** | flagoff |
|---|---|---|---|
| atoll | 108 [64] {39} | **113** [63] {39} | 110 [61] {27} |
| drakkarfjord | 165 [135] {128} | 165 [138] {123} | 171 [144] {133} |
| glacierkeep | 150 [105] {77} | 147 [97] {68} | 127 [101] {69} |
| midgard ⚠ *(zero dose)* | 98 [59] {32} | 93 [59] {27} | 103 [55] {22} |
| nordkap | 128 [83] {51} | 125 [67] {45} | 130 [88] {58} |
| yulerune ⚠ *(zero dose)* | 81 [46] {16} | **64** [30] {9} | 77 [36] {11} |

⭐ **THE yulerune ROW IS THE INTERNAL CONTROL AND IT IS THE LARGEST SINGLE MOVEMENT IN THE TABLE.**
81 → 64 wins in 180, on a board where the standdown assertion measures 0 of 24 games with any v523
clause AND the deterministic fixture measures v523 byte-identical to the parent on both seats.
**A −17-win swing with a dose of exactly zero, in the headline table itself.**

### THE PHASE BUDGET — `phase.py`, replay-side, n=1,080/arm

Kill mark cross-checked against the grid TSV in all 3,240 games: **0 alarms in 3,240**, and the
`tsv_turn − walker_round` histogram is the single value `{1: …}` in every arm.

| arm | med ARRIVE | med SENT (n games) | med FUNDED | med KILL | arrive→sent | sent→funded | **funded→kill** |
|---|---|---|---|---|---|---|---|
| parent | 14.0 | 88.0 (838) | 88.0 | 197 | 72.0 | 0 | **69.0** |
| **v523 FIRED** | 14.0 | 88 (811) | 90.0 | 210 | 69 | 0 | **67** |
| flagoff *(known-zero)* | 13.5 | 88.0 (826) | 88.0 | 215.5 | 72.0 | 0 | **75.0** |

⭐ **THE CELL v521 DIED ON IS FLAT.** v521's whole regression was `funded → kill` 69 → 100 against
a known-zero at 69. v523 reads **67 against a known-zero at 75**.
⚠ **AND THE ONE MARGINAL THAT MOVES AGAINST THE DESIGN IS THE SENTINEL COUNT.** The salt gate is
supposed to open EARLIER and more often; instead **811 games have a forward sentinel against the
parent's 838** (known-zero 826). Unexplained, and it is the shape a *"the merged SEALED arms the
magazine sooner, which spends titanium the sentinel purchase needed"* story would have — but that
story is not measured here and is not claimed.

---

## ⭐⭐ CENTREPIECE 2 — THE SEALED-RATE, WHICH IS WHAT THIS BUILD ACTUALLY CHANGES

**8 mechanism arms × 36 games** (6 maps × 3 seeds × 2 seats), all four v523 instruments ON plus
`FS_V522_MAG_LOG` (to reach change 3's site), vs `_v488beltbreak2`. ⛔ **The win column of a
mechanism arm is not read.** `mechread523.py --selftest` **PASS** on six guards including a FULL
mutation, a SINGLE-COLUMN mutation, a FIELD mutation, a malformed line that must be REPORTED, and
an EMPTY tape that must be distinguishable from a parse failure.

`GAIN` is the mechanism's own dose: **merged% − own%**, i.e. the share of at-ring rounds in which
the CREW's merged census called the ring closed and this body's own eyes did not. It is a
**within-arm** contrast, which is the only valid one here — the arms play different games, so
`ph_lines` differs and raw counts are not comparable across rows.

| arm | ph_lines *(denominator)* | own% | merged% | **GAIN pp** | sealpub% | arc-closed publishes | union-answered salt gates |
|---|---|---|---|---|---|---|---|
| **`mF` all on (FIRED)** | 7,536 | 26.1 | **36.3** | **+10.18** | 20.2 | **1,341** | **1,138** |
| `mSALT` SALTEYES off | 8,855 | 17.0 | 17.0 | **+0.00** | 6.2 | **0** | **0** |
| `mUNION` SALT_UNION off | 7,777 | 32.5 | 33.5 | +1.02 | 18.4 | 1,273 | 127 |
| `mARC` ARC_UNION off | 8,043 | 33.9 | 52.7 | +18.79 | 29.1 | **0** | 2,360 |
| `mPHS` PHASE_SEALED off | 11,131 | 34.5 | 46.4 | +11.93 | **8.3** | 1,272 | 1,754 |
| `mCREW` CREWREAD off | 6,860 | 29.6 | 39.3 | +9.71 | 14.4 | 871 | 784 |
| `mFUND` COREFUND off | 8,647 | 32.5 | 48.9 | +16.38 | 21.2 | 1,405 | 2,014 |
| **`mOff` master off** | 9,196 | 24.0 | 24.0 | **+0.00** | 7.3 | **0** | **0** |

| arm | Core phase reads *(denominator)* | body-2 slot WON | win% | funding questions *(denominator)* | **flip%** |
|---|---|---|---|---|---|
| **`mF` all on (FIRED)** | 31,583 | **1,384** | 4.38% | 3,749 | **7.79%** |
| `mSALT` | 27,342 | 1,117 | 4.09% | 3,074 | 8.56% |
| `mUNION` | 30,760 | 1,733 | 5.63% | 3,759 | 7.64% |
| `mARC` | 22,904 | 1,049 | 4.58% | 2,393 | 8.40% |
| `mPHS` | 34,909 | 1,336 | 3.83% | 4,485 | 7.11% |
| **`mCREW` CREWREAD off** | **0** | **0** | 0.00% | 3,654 | 6.87% |
| **`mFUND` COREFUND off** | 29,813 | 376 | 1.26% | **0** | **0.00%** |
| **`mOff` master off** | **0** | **0** | 0.00% | **0** | **0.00%** |

⭐ **`mOff`'s AND `mSALT`'s ZEROES ARE REAL, NOT VOID.** Every log flag is gated on itself rather
than on the master, so with `LOKI_FS_V523 = False` the tape still emits **9,196 PH523 at-ring
records** while every mechanism column reads exactly zero and `merged% == own%` to the digit.
**The denominator is visible, so the zero means something.**

⭐ **EACH SUB-FLAG IS ISOLATED AT THE MECHANISM.** `mSALT` zeroes the arc publishes, the union
gates AND the gain together. `mARC` zeroes the arc publishes alone (the salt union carries on, at
2,360 gates). `mUNION` collapses the union gates 1,138 → 127 while the arc publishes survive.
`mPHS` keeps the merge (gain +11.93) and suppresses the PUBLISH (sealpub 8.3% against `mF`'s
20.2%) — the channel/mechanism separation as a unit test. `mCREW` zeroes both Core columns.
`mFUND` zeroes both funding columns.

⛔⛔ **AND THE ONE READING THAT SHOULD WORRY THE READER IS `mUNION` vs `mF`: THE ARC MERGE IS
REACHABLE BUT MASKED.** `arc_credit` — a peer's arc-closed word actually being believed — reads
**0 in the fired arm and 79 in `mUNION`**. The salt-union disjunct is evaluated first and
short-circuits, so in the shipped configuration **the arc channel is published 1,341 times and
credited zero times.** The pincer merge this build was written for is present, proved reachable in
a mutant, and **carries none of the fired arm's effect**. ⇒ **The whole of `SALTEYES`'s measured
gain in the fired config is the SALT_UNION half — the crew-slot read — and the arc half is dead
weight until the ordering is inverted or the union is made to require both.**

---

## THE PRE-HEADLINE DOSE GATE — STORE-BLIND, AND THE STORE-BLIND FORM CHANGES THE ANSWER

Baseline = `FS_V523_STORE_ONLY` (publishes every v523 word the fired build publishes; no consumer
acts on it), so this table measures **behaviour and nothing else**. 6 maps × 3 seeds × 2 seats,
randomness off on BOTH sides.

| map | **naive** (parent vs fired) | ⭐ **store-blind** (store-only vs fired) |
|---|---|---|
| atoll | **3 / 6** | **0 / 6** |
| drakkarfjord | 6 / 6 | **6 / 6** |
| glacierkeep | 6 / 6 | **3 / 6** |
| midgard ⚠ *(cripple)* | 0 / 6 | **0 / 6** |
| nordkap | **3 / 6** | **0 / 6** |
| yulerune ⚠ *(cripple)* | 0 / 6 | **0 / 6** |
| **TOTAL** | **18 / 36** | **9 / 36** |

⛔⛔ **HALF THE NAIVE DOSE IS PURE CHANNEL, AND THIS BUILD PROVES IT MORE DIRECTLY THAN v522 DID.**
The 9 cells where naive says CHANGED and store-blind says same were opened. **All 9 are identical
in length to the parent's replay; 3,576 bytes differ in total; and the fired replay is
BYTE-IDENTICAL to the store-only replay** — so the difference from the parent is, by construction,
the store words and nothing else. v522 established this by decomposing varint deltas; here the
structural identity does it outright.

⭐⭐ **AND IT INDEPENDENTLY CORROBORATES THE `--seed` FINDING WITHOUT BEING DESIGNED TO.** The
differing-byte counts within each cell family are **identical across all three seeds** — atoll B
6/6/6, glacierkeep B 966/966/966, nordkap A 220/220/220. Three seeds cannot produce the same
byte-count on three different games. ⇒ **The seed is inert and the same game was played, exactly as
v522 measured on 11 of 12 cells.**

⇒ **DENOMINATORS, STATED HONESTLY:** 36 cells are **~12 distinct games**; the 24 non-cripple cells
are **~8 distinct games**. The store-blind reading of **9 of 36 cells is ~3 of ~12 distinct games**
(9 of 24 on the maps where the plank runs is ~3 of ~8). **The mandate's gate is ≥ 1 of 18 on the
maps where the plank runs; the reading is 9 of 24 cells.**

---

## ⛔⛔ THE STANDDOWN ASSERTION — CRIPPLE **AND** GATED, WITH A POSITIVE CONTROL

**PER-GAME, n=24 per board, every v523 instrument ON. A single leaking game cannot hide in a
mean.** archipelago is played vs `bots/_v468kladturbo`, the other three vs `_v488beltbreak2`.

| board | mechanism | n | games with a **merged gain** | with an **arc-closed publish** | with an **arc credit** | with a **union salt gate** | with a **body-2 phase win** | PARSE_BAD |
|---|---|---|---|---|---|---|---|---|
| **yulerune** | CRIPPLE | 24 | **0** | **0** | **0** | **0** | **0** | 0 |
| **midgard** | CRIPPLE | 24 | **0** | **0** | **0** | **0** | **0** | 0 |
| **archipelago** | GATED | 24 | **0** | **0** | **0** | **0** | **0** | 0 |
| **nordkap** | *neither — POSITIVE CONTROL* | 24 | **19** | **23** | **2** | **19** | **13** | 0 |

⇒ **ON BOTH CRIPPLE BOARDS AND ON THE GATED BOARD, NO v523 CLAUSE FIRES IN ANY GAME.** The
assertion fires on the control board on all five columns, so it has been seen to produce the other
verdict. 0 tracebacks across all 96 games.

⛔ **CHANGE 2's COLUMN IS COUNTED SEPARATELY AND IS NOT ASSERTED ON THE SAME GROUND.** The Core
reads the phase on every board; what the gate controls is whether a second ferry-siege body exists
to publish into `FS_SUPP_SLOT` at all. Its zero is a CONSEQUENCE, not a definition, and conflating
the two would let a real leak in the siege clauses hide behind a correct zero in the Core's.

---

## ⭐⭐ SINGLE-FLAG ISOLATION — WITH A KNOWN-ZERO ARM IN LEG 1, NOT LEG 2

v522's leg 1 had no control, all three of its treatment arms beat the baseline on every column,
and its one "OUTSIDE" reading (+6.41 pp) reversed sign (−1.71 pp) in a second draw that did have
one. That lesson is applied rather than re-learned. **n=468/arm, 13 blocks, 5 arms in the same
blocks, seeds 801-839 (disjoint from the headline).**

| arm | n | wins | ≤r180 | **≤r200** | **≤r300** | median kill | our core dead |
|---|---|---|---|---|---|---|---|
| parent (baseline) | 468 | 66.2% | 0.276 | 0.308 | 0.429 | 199 | 134 |
| **`parentB` — THE SAME TREE, second copy (KNOWN-ZERO)** | 468 | 66.2% | 0.256 | 0.297 | 0.419 | 201 | 142 |
| `iSALT` — change 1 ALONE | 468 | **69.0%** | 0.254 | 0.303 | 0.425 | 216 | 126 |
| `iCREW` — change 2 ALONE | 468 | 65.4% | 0.246 | 0.280 | 0.404 | 222 | 141 |
| `iFLOORFUND` — change 3 on its ONLY live path | 468 | 67.9% | 0.274 | 0.306 | 0.415 | 218 | 129 |

| contrast vs baseline | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **`parentB` (KNOWN-ZERO)** | **+0.00 pp** (hw 6.06) | **−1.07 pp** (hw 5.88) | **−1.07 pp** (hw 6.33) |
| `iSALT` | +2.78 pp (hw 6.00) inside | −0.43 pp (hw 5.90) inside | −0.43 pp (hw 6.34) inside |
| `iCREW` | −0.85 pp (hw 6.08) inside | −2.78 pp (hw 5.84) inside | −2.56 pp (hw 6.32) inside |
| `iFLOORFUND` | +1.71 pp (hw 6.02) inside | −0.21 pp (hw 5.91) inside | −1.50 pp (hw 6.33) inside |

⭐ **THE KNOWN-ZERO ARM BEHAVED, WHICH IS WHAT MAKES THE REST READABLE:** +0.00 / −1.07 / −1.07.
**Every treatment arm is inside on every column.** The ordering — `iSALT` +2.78 and `iCREW` −0.85
on wins, `iCREW` worst on both kill columns — is the direction the composite's runs-map split also
points, but at n=468 with an ~5 pp floor **nothing here separates and none of it is claimed.**

⭐ **`iFLOORFUND` IS THE ONLY MEASUREMENT OF CHANGE 3 THAT MEANS ANYTHING**, and it reads
**+1.71 pp wins / −0.21 pp k≤200 / −1.50 pp k≤300, all inside**. ⇒ v522's floor, re-measured on
top of a funding predicate that no longer stands it down for half of every reload cycle, is still
a null. **Both endpoints of that design space are now occupied by a rejection (v521, −9.83 pp), a
null (v522), and a null with the predicate fixed (v523).**

---

## ⭐ THE GUNGNIR PAIR (Magnus directive, mid-build) — INTERLEAVED, NOT SEPARATE RUNS

**13 blocks × 36 games = n=468/arm, both arms in the SAME blocks on the SAME seeds** (seeds
403-439, disjoint from the headline and from the isolation leg), vs `bots/_x3r0v161gungnir`. This
is what makes the delta drift-proof rather than leaning on the earlier separate-run 55.6% read.

| | **parent-as-configured** | **v523 FIRED** |
|---|---|---|
| WINS | 227/468 (48.5%) | **245/468 (52.4%)** |
| ≤r150 | 35 (0.075) | 35 (0.075) |
| ≤r180 | 52 (0.111) | 55 (0.118) |
| **≤r200** | 78 (0.167) | 73 (0.156) |
| **≤r300** | 141 (0.301) | 133 (0.284) |
| **median kill** | **241** | **256** |
| our core destroyed | 229 | 206 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v523 FIRED vs parent** | **+3.85 pp** (hw 6.41) inside | −1.07 pp (hw 4.71) inside | −1.71 pp (hw 5.83) inside |

### PER MAP vs Gungnir — wins/78 [k≤300] {k≤200}

| map | parent | **v523 FIRED** |
|---|---|---|
| atoll | 40 [26] {7} | 43 [25] {9} |
| drakkarfjord | 73 [66] {52} | 69 [51] {39} |
| glacierkeep | 43 [6] {1} | 42 [1] {0} |
| midgard ⚠ *(cripple)* | 27 [14] {6} | **25** [17] {10} |
| **nordkap** | 25 [14] {7} | **41** [26] {8} |
| yulerune ⚠ *(cripple)* | 19 [15] {5} | **25** [13] {7} |

⭐ **THE CRIPPLE CELLS ARE THE LIVE QUESTION AND THEY MOVED IN OPPOSITE DIRECTIONS.** The v520
screen measured 47% (midgard) and 37% (yulerune) vs Gungnir; this pair reads midgard 34.6% → 32.1%
and yulerune 24.4% → 32.1% on a dose of exactly zero. **Opponent-specific mode calibration remains
open, and this leg cannot settle it: the two cells disagree, and both sit on a subpopulation where
v523 is byte-identical to its parent.** What the pair does establish is that the cripple cells are
**much worse against Gungnir than against `_v488beltbreak2`** (32% vs 44-50%), which is a
calibration question about `FS_V519_CRIPPLE_MAPS` and not about this build.

⚠ **nordkap 25 → 41 (+16 wins in 78) IS THE LARGEST SINGLE CELL MOVEMENT IN THE BUILD** and it
sits on a runs-map with a live dose — but the yulerune row shows the same grid producing +6 with
no dose at all, so **it is reported and not claimed.**

⛔ **CAVEATS, CARRIED WITH THE NUMBER:** Gungnir is a **teammate's bot, not the field**; a 6-map
grid is explicitly a **non-arming read** in `PROGRAMME.md`; and `SHIP_BAR` is not addressed by any
table in this report.

---

## ⭐⭐ THE OVERLAP CURRENCY, n=1,080/arm, replay-side

*(`overlap.py`, eight guards driven to both verdicts — `--selftest` PASS, including a MUTATION
control, a SIMULTANEITY control, a ZERO-DENOMINATOR control returning `None` not 0, a real-data
TEAM-SWAP positive control and a CHANNEL CROSS-CHECK. Funding is read **off the wire**; no bot
stdout is involved.)*

**OVERLAP = rounds in which the collar is SIMULTANEOUSLY sealed AND a forward turret of ours is
alive AND the magazine holds ≥ 10 ammunition.** ⛔ `sealed_r` here is **GROUND TRUTH off the wire**
(all seats denied), not our published phase — which is exactly why it is the right control on a
build that changes who SEES closure rather than whether closure happens.

| arm | n | sealed_r | livefund_r | **OVERLAP_r** | ovl > 0 | **net dmg / overlap round** | net dmg / other round |
|---|---|---|---|---|---|---|---|
| parent (baseline) | 1080 | 60.0 | 69.7 | **13.15** | 39.8% | **7.23** | 0.67 |
| **v523 FIRED** | 1080 | 60.4 | 66.6 | **12.11** | 35.7% | **7.79** | 0.63 |
| flagoff *(known-zero)* | 1080 | 52.6 | 69.9 | **14.13** | 40.1% | 6.66 | 0.68 |

| contrast | Δ OVERLAP rounds/game | half-width 95% | verdict |
|---|---|---|---|
| **v523 FIRED vs baseline** | **−1.044** | 2.067 | inside |
| **flagoff vs baseline** *(byte-identical play)* | **+0.975** | 2.431 | inside |

⭐ **FINDING 3 — GROUND-TRUTH CLOSURE DOES NOT MOVE AND THAT IS THE DESIGN WORKING, NOT FAILING.**
`sealed_r` reads 60.0 → 60.4 in the treatment against **52.6 in the known-zero arm** (a −7.4
excursion on byte-identical play). v523 changes **who can see a closure**, not how many closures
happen, so a flat ground-truth `sealed_r` beside a **+10.18 pp rise in the PUBLISHED SEALED rate**
is exactly the signature the design predicts — and the two are measured on completely separate
instruments (replay wire vs stderr tape).

⭐ **FINDING 4 — THE 6× OVERLAP DAMAGE GAP REPLICATES A FOURTH TIME, AND WIDER.** Pooled net damage
on their core per OVERLAP round against per non-overlap round: **7.23 / 0.67 (parent), 7.79 / 0.63
(v523), 6.66 / 0.68 (flagoff)** — ratios of **10.8×, 12.4×, 9.8×**, against v522's 6.2× and
v521's 6.2× on different baselines and seeds. **The direction is now four-for-four; the magnitude
is fixture-dependent and should be quoted as "roughly an order of magnitude", not as 6×.**

⚠ **FINDING 5 — OVERLAP's NOISE FLOOR IS CONFIRMED AT ±2.1–2.4 ROUNDS/GAME AT n=1,080** (measured
on a byte-identical arm, which moved +0.98). The v522 open item stands unchanged: **this column is
a diagnostic, not a verdict metric.**

---

## HEAL-BACK AND THE COLLAR — `crip.py`, replay-side, n=1,080/arm

*(Guard: the TEAM-SWAP POSITIVE CONTROL re-reads one game with `our_team` flipped and must move the
columns — it moved 7 of them: `heal_back`, `opp_harv_built`, `opp_belt_built`, `fwd_gun_n`,
`oppcore_dmg`, `fwd_laun_n`, `collar_bar_n`.)*

| | parent | **v523 FIRED** | flagoff *(known-zero)* |
|---|---|---|---|
| **median heal-back** (n=836/805/820 games with a defined ratio) | **0.000** | **0.000** | **0.000** |
| mean heal-back | 0.255 | 0.265 | 0.261 |
| **collar barriers / game** | 17.83 | **15.99** | 16.26 |
| damage we landed on their core / game | 605.5 | 592.4 | 610.8 |
| their core healed / game | 275.8 | 270.5 | 281.8 |
| damage landed on OUR core / game | 339.6 | **366.9** | **386.5** |
| their belts built / game | 28.27 | 29.05 | 28.44 |
| their harvesters built / game | 5.65 | 5.80 | 5.77 |
| first forward sentinel (round) | 136.5 | 140.3 | 136.9 |

⚠ **THE COLLAR-BARRIER COLUMN FALLS AGAIN AND FOR THE SECOND BUILD RUNNING NOBODY HAS AN
EXPLANATION.** 17.83 → 15.99, with the known-zero arm at 16.26 — the control and the treatment
both sit ~1.7 below the baseline, so the column is not resolvable at this n and the movement is
**shared with a byte-identical arm**. v522 saw the same shape (16.88 → 15.97, known-zero 17.17).
⚠ `ourcore_dmg` rises 339.6 → 366.9 **against a known-zero at 386.5, which moves FURTHER** — so
unlike v522, this build's largest heal-back-table movement is straddled by its own control.

---

## FLAG-OFF AUDIT

**Structural.** Every v523 branch reads `LOKI_FS_V523` (and its own sub-flag) at RUN time:
`siege.py` at the arc publish, the arc decode, the salt gate, the phase machine, the merge and the
funding predicate; `main.py` at the three Core consumers and the v522 funding re-check. `raid.py`
and `eco.py` are **byte-identical to the parent (md5 equal to the freeze)**.

**Two additions are not individually guarded, and each is disclosed rather than argued away:**
1. `_fs_census` records `self.v523_open_seats` **unconditionally**. It is a pure assignment to an
   attribute nothing else reads; gating it would make the flag-off tree take a different path
   through the hot loop for no behavioural reason. **The byte-identity test below is the proof of
   that claim, not this sentence.**
2. `_v523_crew_phase` and `_v523_funded` are always *called*; each returns the parent's value
   verbatim unless its own flag is set.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v523 flag):

```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v523 derived defaults: 0 []
v522 derived defaults (inherited, must also be 0): 0 []
v521 derived defaults (inherited, must also be 0): 0 []
v520 derived defaults (inherited, must also be 0): 0 []
v519 derived defaults (inherited, must also be 0): 0 []
v518 derived defaults (inherited, must also be 0): 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```

⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see the
known v515 hazard in this very file before its zero for v523 is believed.

**`collide.py`, the mandatory slot-10 pre-flight, driven to BOTH verdicts:**

| configuration | crew | home ferry | COLLISION | |
|---|---|---|---|---|
| v523 FIRED | True | False | False | PASS |
| v523 master OFF ≡ the v522-verdict parent | True | False | False | PASS |
| v520 master OFF (crew OFF, home ferry ON) | False | **True** | False | PASS |
| **KNOWN-BAD control** (crew ON at the definition site, read-site fix disabled) | True | True | **True** ⛔ | PASS — *the detector is proved able to see the defect it exists for* |

**Byte-identity — and the baseline is an INDEPENDENTLY CONSTRUCTED tree.** `arms/parent` is
`bots/_v522floor` with `FS_V522_FLOOR` turned off **at its definition site**, not a copy of the
treatment with an override appended. 12 games, 6 maps × 2 seats, same seeds, randomness off —
ours AND the opponent's. **Re-run against the FINAL tree at the end of the build:**

```
NEGATIVE CONTROL  parent vs parent (same tree, two runs)   : identical 12 / differing  0
TEST              parent vs v523 FLAG-OFF                  : identical 12 / differing  0
STORE CONTROL     parent vs v523 STORE_ONLY                : identical  6 / differing  6   *(store bytes — see the dose section)*
POSITIVE CONTROL  parent vs v523 FIRED                     : identical  6 / differing  6
```

⇒ **`LOKI_FS_V523 = False` PLAYS THE PARENT-AS-CONFIGURED BYTE FOR BYTE**, two separately built
trees producing the same 12 games.
⛔ **AND THE 6 IDENTICAL CELLS IN THE POSITIVE CONTROL ARE NOT A WEAKNESS — THEY ARE THE ZERO-DOSE
POPULATION.** Both midgard cells and both yulerune cells are among them, which is the byte-level
half of the standdown proof used in the headline split above.

**Behavioural.** The `flagoff` arm is not a separate leg — it is **the third arm of the headline
grid, in the same blocks, on the same seeds**, at n=1,080.

---

## FAILURE REEL — and the convention is overlap-blind for the FOURTH build

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in EACH of the six
maps, for the `v523 FIRED` arm**, across the 30 headline blocks. Ties: lowest block → lowest seed →
seat A; no tie occurred.

| # | game | block | our core dead | **overlap_r** | sealed_r | livefund_r | class |
|---|---|---|---|---|---|---|---|
| 1 | `atoll_s34_B` | 12 | r114 | **0** | 0 | 0 | NO_TURRET |
| 2 | `drakkarfjord_s17_A` | 6 | r338 | **0** | 0 | **5** | NO_TURRET *(5 funded rounds, no closure)* |
| 3 | `glacierkeep_s75_A` | 25 | r316 | **0** | 0 | **31** | **SEAL_SHOT_DISJOINT** |
| 4 | `midgard_s11_B` | 4 | r132 | **0** | 0 | **58** | HEAL_OUTRUN *(zero-dose cell)* |
| 5 | `nordkap_s73_B` | 25 | r142 | **0** | 0 | 0 | NO_TURRET |
| 6 | `yulerune_s11_B` | 4 | r140 | **0** | 0 | 0 | NO_TURRET *(zero-dose cell)* |

⭐⭐⭐ **OVERLAP IS ZERO IN 6 OF 6 AGAIN, AGAINST A POPULATION MEAN OF 12.11 AND A POPULATION SHARE
OF 35.7% ABOVE ZERO.** v521, v522 and now v523 have reproduced this on different arms, different
baselines and different seeds. **The convention is overlap-blind as a property of the convention,
and it should be treated as a known instrument limitation rather than re-discovered a fifth time.**

⭐ **ROW 3 IS THE SAME FAILURE FOR THE FOURTH BUILD** (v520 `glacierkeep_s37_A`, v521
`glacierkeep_s83_A`, v522 `glacierkeep_s40_A`): a funded turret alive for **31 rounds** with
**zero** simultaneously-sealed rounds. Four builds have now been aimed near it and none has moved
it.

### REEL EXTENSION (mandate) — the 2 LATEST-KILL WINS

Extension rows, labelled, **not** folded into the six.

| game | kill round | **overlap_r** | sealed_r | livefund_r |
|---|---|---|---|---|
| `midgard_s65_A` ⚠ *(zero-dose cell)* | r957 | **0** | 0 | **50** |
| `yulerune_s40_A` ⚠ *(zero-dose cell)* | r952 | **0** | 0 | **56** |

⛔ **AND THE EXTENSION FAILS TO REPRODUCE v522's ONE INTERESTING ROW.** v522's latest-kill win
carried overlap 36 with 232 sealed rounds; both of this build's carry **overlap 0**, and **both
land on cripple cells** — i.e. on this arm the latest-kill tail is the *mode-standdown* tail, not
the *seal-shot* tail. **The extension's value is therefore arm-dependent, which is itself a caution
about reading it as a fixed instrument.**

⛔ **NO NEW CAUSE TOKEN IS COINED.** `corpus/failure_reel.tsv` is **not** appended by this build;
the selection rule and the replays are in `scratchpad/s51_v523_build/` so the append is a one-liner
if the builder wants the six rows in it.

---

## SURPRISES (written down before being explained away)

1. **⭐⭐⭐ THE ARC MERGE — THE HALF THIS BUILD WAS NAMED FOR — IS PUBLISHED 1,341 TIMES AND
   CREDITED ZERO TIMES IN THE FIRED CONFIG.** `arc_credit` reads 0 in `mF` and **79 in `mUNION`**.
   The salt-union disjunct is checked first and short-circuits. The pincer merge is present,
   reachable and proved in a mutant, and it carries **none** of the fired arm's effect.
2. **⛔⛔ THE HEADLINE'S ENTIRE NEGATIVE SIGN LIVES ON TWO MAPS WHERE v523 IS BYTE-IDENTICAL TO ITS
   PARENT.** −6.11 pp on 360 zero-dose games against −0.14 pp on 720 dose-bearing ones. The pooled
   row (−2.13 pp) is a weighted average of a null and a fixture artefact.
3. **⭐⭐ THE STORE-BLIND DOSE HALVES THE NAIVE ONE (9/36 vs 18/36), AND THE PROOF IS STRUCTURAL
   THIS TIME:** in all 9 pure-channel cells the fired replay is byte-identical to the store-only
   replay while differing from the parent in 3,576 bytes at identical file length.
4. **⭐⭐ THE `--seed` INERTNESS FELL OUT OF THE DOSE DATA WITHOUT BEING LOOKED FOR.** Identical
   differing-byte counts across all three seeds of every pure-channel cell (6/6/6, 966/966/966,
   220/220/220). Three seeds cannot give one byte-count on three different games.
5. **⚠ THE SALT GATE OPENS MORE OFTEN AND FEWER GAMES GET A FORWARD SENTINEL.** 811 games with a
   sentinel against the parent's 838 (known-zero 826), while the published SEALED rate rose
   +10.18 pp. Unexplained; the shape of a *"the magazine arms sooner and spends the purchase"*
   story, which is not measured here.
6. **⛔ GROUND-TRUTH `sealed_r` MOVED −7.4 ROUNDS/GAME IN THE KNOWN-ZERO ARM (60.0 → 52.6) ON
   BYTE-IDENTICAL PLAY**, against +0.4 in the treatment. The control's excursion on the marginal
   is 18× the treatment's.
7. **⚠ THE 6× OVERLAP DAMAGE GAP IS ~11× ON THIS FIXTURE.** 7.23/0.67, 7.79/0.63, 6.66/0.68. The
   direction is four-for-four; the number quoted as "6×" in three previous reports is not stable.
8. **⚠ AGAINST GUNGNIR, nordkap MOVES +16 WINS IN 78 AND yulerune MOVES +6 WITH ZERO DOSE.** The
   largest cell movement in the build sits beside a zero-dose cell moving a third as far.
9. **⛔ THE MANDATE'S THIRD SITE WAS ALREADY DISARMED BY THE PARENT'S OWN VERDICT.** Change 3's
   predicate is correct, flips 7.8% of the questions it is asked, and sits inside a block
   `FS_V522_FLOOR = False` never enters. The shipped composite is a duo.
10. **⭐ THE COLLAR-BARRIER FALL REPLICATES v522's EXACTLY** (17.83 → 15.99 here, 16.88 → 15.97
    there) — and in both builds the known-zero arm sits between or below the treatment. Two builds
    with different mechanisms produced the same movement on the same column, which suggests the
    column tracks something neither plank controls.

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The composite ships as a DUO, not a trio.** Change 3's site is unreachable in the fired
   config (§ change 3). It is measured in the mechanism arms (flip rate) and in a dedicated
   isolation arm (`iFLOORFUND`), and is not claimed in the headline.
2. **The isolation leg is ONE leg with a known-zero arm, not two legs.** v522 ran a second leg
   because the first had no control; that control is in leg 1 here, and `parentB` read
   +0.00/−1.07/−1.07, so a second draw would have been buying power for arms that are all inside
   by a wide margin.
3. **`FS_V523_PROBE_NOARC` was built and not fired.** The store-only baseline turned out to be
   sufficient — the fired/store-only byte identity in the pure-channel cells decomposes the channel
   outright, so the extra probe would have separated a contribution already proved to be the whole
   difference.
4. **Mechanism arms are 36 games each, not 15.** Games cost ~1.3 s.
5. **The Gungnir pair is n=468/arm, not ≥450 exactly** — 13 blocks × 36 was the nearest block
   boundary above the bar.
6. **Timeouts are not reported** (v518 finding 0).
7. **`corpus/failure_reel.tsv` is not appended** (see the reel).
8. **The headline is n=1,080/arm** (mandate asked ≥1,080); blocks ran at ~28 s.

---

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⛔⛔ THE ZERO-DOSE SUBPOPULATION SHOULD BE A STANDING PART OF THE HEADLINE, NOT A FOOTNOTE.**
   This build's grid contains 360 games per arm in which the treatment is **byte-identical to the
   baseline** and which moved **−6.11 pp on wins**. Pooling them with the dose-bearing games turned
   a null into an apparent regression. **Every future 6-map headline that includes
   `FS_V519_CRIPPLE_MAPS` cells has this property and none of the previous reports split on it.**
   The cheapest fix is to report the runs-map row first and the pooled row second.
2. **⚠⚠ THE ARC CHANNEL IS SHIPPED, PUBLISHED AND NEVER READ.** 1,341 publishes, 0 credits, because
   an earlier disjunct short-circuits. Either invert the ordering (arc first, salt-union as the
   fallback), or require both arcs in every path and let the salt-union only *contribute* an arc.
   **As shipped, `FS_V523_ARC_UNION` is a channel with no consumer and one CPU cost.**
3. **⚠⚠ THE DETERMINISTIC DOSE TEST'S CAVEAT HELD — AND THE NAIVE FORM WOULD HAVE DOUBLED THIS
   BUILD'S DOSE.** v522 promoted the store-blind form; this build is the first to run it as the
   gate from the start and it read **9/36 against a naive 18/36**. The promotion should now carry
   the number, not only the warning.
4. **⚠ `_fs_denied` COUNTS AN UNREADABLE TILE AS *NOT DENIED* AND CALLS THAT "THE CONSERVATIVE
   DIRECTION".** It is conservative for the WALK and anti-conservative for the CENSUS, which is the
   defect v523 works around at the read sites rather than fixing at the source. **The source fix —
   a per-seat denial channel — needs a slot nobody has.**
5. **⚠ `R1000_IS_DEFEAT` READS NEUTRAL-TO-NEGATIVE ON THE KILL CLOCK.** Runs-map median kill
   162 → 177 against a known-zero at 168; k≤200 −2.78 pp; k≤300 −3.06 pp. All inside, none
   excluded. **`DEFENCE_ADMISSION_BAR` (r300, ITT) is a fail-to-exclude with a NEGATIVE point
   estimate and is restated as an exclusion in the panel section rather than banked as a pass.**
6. **⚠ `SHIP_BAR` IS NOT ADDRESSED AND MUST NOT BE READ INTO THIS REPORT.** A 6-map grid is
   explicitly a non-arming read in `PROGRAMME.md`, and the Gungnir pair is a teammate fixture.

---

## OPEN ITEMS

0. **⭐⭐ THE MECHANISM WORKS AND ITS CURRENCY DOES NOT PAY — FOR THE THIRD BUILD RUNNING.** v521
   moved the ladder and lost; v522 moved the floor and read null; v523 moves the SEALED rate
   +10.18 pp and reads flat on the maps where it runs. **The published-closure channel has now been
   attacked from three directions and the kill clock has not improved once.** The next plank should
   probably not be a closure-channel plank.
1. **⛔ `adj = 0` IS STILL THE UNTOUCHED HALF OF v521's DIAGNOSIS** (the body is not orthogonally
   adjacent to any open seat). v522 fixed the money, v523 fixed the eyes, and **nobody has fixed
   the geometry.** It is now the only half left.
2. **⛔ THE ARC MERGE NEEDS ONE ORDERING CHANGE TO BE TESTABLE AT ALL** (collision 2). Until then
   `FS_V523_ARC_UNION`'s outcome contribution is unmeasured, not null.
3. **`FS_V523_FUND_SHOTS` (2), `FS_V523_ARC_STALE` (6), `FS_V523_FUND_BANK` (True) and
   `FS_V523_PH_RANK`'s placement of DEGRADE are UNSWEPT.**
4. **The sentinel-count fall (838 → 811 games) is unexplained** and is the one marginal whose
   direction contradicts the design.
5. **The zero-dose cells are ~44-50% win rate vs `_v488beltbreak2` and ~32% vs Gungnir.**
   `FS_V519_CRIPPLE_MAPS` was calibrated against one opponent and the Gungnir pair says the mode
   choice may be opponent-specific. **That is a calibration leg, not a plank.**
6. **Inherited and untouched:** every v522 open item except 0 and 2 (the OVERLAP noise floor,
   confirmed here at ±2.1) — in particular the TTL question, the unswept `FS_MAG_REPAIR_BARRIERS`,
   and rung 4 being effectively dead.

---

## ARTIFACTS

`scratchpad/s51_v523_build/` —
`arms/` (parent = the definition-site baseline, parentB = its known-zero copy, flagoff, storeonly,
the eight mechanism arms, the three isolation arms, and the determinism/dose arms), `grid/`
(30 headline blocks × 3 arms, **all replays kept**), `iso/` (13 blocks × 5 arms), `gung/`
(13 blocks × 2 arms), `mech/` (8 arms), `modeassert/` (4 boards × 24 games), `eq/` (byte-identity +
its negative, store and positive controls), `dose/` (naive and store-blind), `overlap_*.tsv`,
`crip_*.tsv`, `PARENT_FREEZE.md5`, `TREE_FINAL.md5`, `PIDS`, `out/` (every driver log).

**Instruments, each guarded both ways:**
* `mechread523.py --selftest` — **six** guards: a synthetic tape, a FULL mutation, a SINGLE-COLUMN
  mutation (which must leave every other column UNCHANGED), a FIELD mutation, a malformed record
  that must be REPORTED as `PARSE_BAD`, and an EMPTY tape that must be distinguishable from a parse
  failure. **PASS.**
* `modeguard523.py` — the standdown assertion, per game, with nordkap as the positive control on
  all five columns.
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive control
  (2 hits, which is what makes the v523 zero mean something). **PASS.**
* `collide.py` — the slot-10 two-writer pre-flight, four configurations, both verdicts, including a
  reconstructed KNOWN-BAD form that must read `COLLISION: True`. **PASS.**
* `overlap.py --selftest` — eight guards including a MUTATION control, a SIMULTANEITY control, a
  ZERO-DENOMINATOR control returning `None` not 0, a real-data TEAM-SWAP positive control and a
  CHANNEL CROSS-CHECK. **PASS.**
* `phase.py --guard` — synthetic guards plus the real-data kill-mark cross-check against the grid
  TSV: **0 alarms in 3,240 games**, histogram single-valued per arm.
* `crip.py --control` — the TEAM-SWAP positive control, 7 columns moved.
* `drive_eq.sh` — determinism with a negative control (same tree twice), a STORE control and a
  positive control; **re-run against the FINAL tree**.
* `drive_dose523.sh` — the deterministic dose test, naive **and store-blind**, with the
  pure-channel decomposition.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* v523: **currency NULL with a proven-live mechanism** (SEALED +10.18pp vs +0.00 in two
  known-zero arms; plank-map wins −0.14 vs known-zero −1.81; the pooled −2.13 dissolves onto
  byte-identical cripple cells = drift). NOT adopted as head. Decisions on the agent's three:
  (1) the arc-merge channel ships with no consumer — DROP the publish in the next build
  rather than carry a dead channel (mUNION proves it wireable if a future plank wants it);
  (2) the duo framing accepted, change 3 stays inert-flagged; (3) the kill-clock caution is
  real (k≤300 −3.06 vs known-zero +0.97) — restated-exclusion DEFENCE_ADMISSION does not
  clear, one more reason not to adopt.
* **THE PATTERN, three builds running: seal-axis mechanisms move, wins do not.** Sealing —
  even correctly counted — is not converting. The paying levers tonight were pincer,
  modeswitch, funding, door-off; the seal/overlap axis has absorbed three builds for zero
  currency. The axis is parked pending a genuinely different conversion idea.
* Gungnir pair: +3.85 inside interval, nordkap +16/78 the standout; cripple cells ~32% vs
  Gungnir confirms opponent-specific mode calibration as a standing open item.
* **ROUTE — THE FULL-POOL READ IS NOW THE BLOCKING QUESTION.** Every number tonight is 6-map;
  SHIP_BAR 75/80 is denominated FULL-POOL, where gated maps play chassis-vs-itself (~50) and
  the pool composition will pull the pooled number well under the 6-map 64-68. Before any
  further mechanism hunting: the head config (bots/_v522floor as configured) goes through the
  standard full-pool powered shard vs Sleipnir v2 — prereg, BARS, corefill — to learn the
  TRUE distance to the bar.
