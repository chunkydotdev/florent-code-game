# BUILD REPORT (DRAFT) — `bots/_v522floor` (the magazine floor stops starving the seal), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v521sync` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v522_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2`, and the freeze
re-verified byte-for-byte at the end of the build (9/9, `2026-08-18T13:13:41Z`). Master
`LOKI_FS_V522`; False reproduces the parent AS CONFIGURED (AST-scanned and byte-proved below).
Scratch: `scratchpad/s51_v522_build/`. PAR=4 on single-arm legs; the headline runs 3 arms × PAR 4.
Recorded PIDs in `scratchpad/s51_v522_build/PIDS`. `scratchpad/overnight*` and corefill
untouched.*

*Diff vs parent: `doctrine.py` +272/−2, `main.py` +114/−1, `siege.py` +115/−0, **`raid.py` and
`eco.py` BYTE-IDENTICAL (0/0, md5 equal to the freeze)**. **7,332 games with a result row across
every leg, plus 365 replay-only determinism/dose games; 0 tracebacks, 0 no-winners** (counted off
the leg TSVs, not by directory). ⛔ Timeouts are NOT reported — v518 finding 0 proved the local
timeout column is a constant that cannot fire.*

---

## ⭐⭐⭐ THE ONE-PARAGRAPH READ

**THE MECHANISM WORKS, ITS CURRENCY DOES NOT MOVE, AND THE INSTRUMENT THAT WAS PROMOTED TO GATE
THIS BUILD TURNS OUT TO BE ABLE TO SCORE A DOSE FOR A CLAUSE THAT PLAYS AN IDENTICAL GAME.**
At n=1,080/arm against a byte-identical known-zero arm in the same blocks, v522 FIRED reads
**wins +0.00 pp (hw 3.94)**, **`KILL_TARGET`'s tracked k≤200 −0.28 pp (hw 3.92)** and **k≤300
+0.65 pp (hw 4.20)** — all inside, median kill **196 → 193**, `funded → kill` 69 → 73 against a
known-zero control at 72. On its own currency, **OVERLAP moves +0.18 rounds/game (hw 2.33)
against a known-zero arm that moved +2.01 in the same blocks** — i.e. the fixture's same-config
noise on that column is an order of magnitude larger than the treatment. **v522 is a
well-controlled NULL.** The mechanism is not inert: it BINDS 432 times in 36 instrumented games,
the mechanism arms drive every column to a real zero with a visible denominator, and the
store-blind dose test reads **15 of 36 changed games (12 of 18 on the maps where the plank runs)**.
**THE THREE FINDINGS THAT OUTLIVE THE PLANK: (1) `.replay26` SERIALISES THE PRIVATE COMMS STORE,
so v521's promoted deterministic dose test scores a full dose for a clause that only writes a
different number into a store slot — proved here, 167 differing bytes across 5 games, EVERY ONE a
varint differing by exactly `+2048 = 1 << FS_PHASE_SHIFT`, with the files identical in length and
not one game event changed; (2) a PRE-HEADLINE REACHABILITY CENSUS moved the mechanism's
publish→bind conversion from **13% to 96%** by naming two defects nothing else would have caught —
the Core's own funding re-check killed 100 of 100 glacierkeep NEAR rounds, and the Core was blind
to body 2's publish channel in 60 of 69 nordkap publishes; (3) the 6× OVERLAP damage gap
REPLICATES A THIRD TIME (**7.33 net per overlap round against 1.19 outside**, and 7.04 / 6.50 in
the other two arms).**

⚠ **THE ~4.7–5.6 pp SAME-CONFIG FALSE-POSITIVE FLOOR (v519 open item 2) IS CARRIED BESIDE EVERY
CLAIM BELOW**, and this build's answer to it is v520's and v521's: a **KNOWN-ZERO ARM IN THE SAME
BLOCKS**, proved byte-identical to the baseline on 12 of 12 games with a negative control. Every
contrast is reported twice. A second known-zero arm was added to the isolation leg **after** the
first isolation leg produced a 6.41 pp reading that the second leg did not reproduce.

---

## WHAT WAS BUILT

### FIRED-CONFIG CORRECTIONS (parent-config, not new mechanisms — they define the baseline)

**(i) `FS_V521_SYNC = False` at its definition site.** The v521 verdict: the three ladder
reorders were measured INERT by the deterministic dose test (0 of 18 games on the maps where the
sync state fires) and `iLADDER` read +0.21 pp wins / −4.70 pp k≤200, both under the floor. Code
stays; the flag is the decision.

**(ii) `FS_V521_COLLARFIRST = False` at its definition site.** The v521 verdict's one measured
rejection: `iMAG` (1d+1e) carried the whole composite regression at **−9.83 pp k≤200 / −7.48 pp
k≤300, both OUTSIDE at n=468**, with `funded → kill` 69 → 100.

**(iii) `FS_V521_PHASE_HONEST` and `FS_V521_GATEFIX` STAY ON**, per the builder's verdict lines
("PHASE_HONEST is a separable semantics fix five planks read — keep"; "gate fix … keep").

### THE NEW MECHANISM — `FS_V522_FLOOR`, ONE CLAUSE, THREE LINES OF ARITHMETIC

While closure is **NEAR** (1 ≤ `orth_open` ≤ `FS_V522_NEAR` = 2) and a **funded forward turret is
alive**, the Core's conversion floor rises from the repair allowance
`FS_MAG_REPAIR_BARRIERS × bar` to the seal's actual price `FS_V522_SEATS × bar + FS_SEAL_MARGIN`,
capped at `FS_V522_FLOOR_CAP` (40) and TTL'd at `FS_V522_MAX_RNDS` (150) rounds of BINDING per
match. It releases the round the collar shuts, the turret dies, or the raider stops publishing —
all three change the published phase.

**THE CHANNEL, AND IT COSTS NO NEW SLOT AND NO NEW WRITER.** The Core owns `convert_ammo` and has
no eyes at the enemy ring, so exactly one bit of state has to cross. It rides the phase field
`_fs_publish` already stamps into each body's own word, as **`FS_PH_KILL_NEAR = 6` — the last free
code in a 3-bit field** (0-5 taken, 7 = `FS_PH_DEGRADE`). It is a strict REFINEMENT of
`FS_PH_KILL_OPEN`: every round that publishes 6 would have published 4 or 5 under the parent.

**PUBLISH-IF-BINDING (`FS_V522_BIND_IF`).** The raider publishes only when the remaining seal
price actually exceeds the allowance the Core would otherwise hold
(`orth_open × bar + FS_SEAL_MARGIN > FS_MAG_REPAIR_BARRIERS × bar`). This makes the reserve exact
rather than conservative **and keeps the channel change off the rounds the mechanism does not act
on** — the unpaid-risk half of v521 doctrine collision 1.

**THE TWO REACHABILITY CORRECTIONS** (`FS_V522_CORE_FUND = False`, `FS_V522_CREW_READ = True`)
were **measured into existence before the headline** and are documented in their own section
below, not smuggled in here.

---

## ⛔⛔⛔ THE INSTRUMENT FINDING, AND IT COMES FIRST BECAUSE IT CHANGES HOW THE DOSE TEST READS

**v521 promoted the deterministic dose test — same seeds, randomness off on BOTH sides, baseline
vs treatment, replay bytes diffed — as a standard pre-headline gate, on the strength of its having
killed two designs.** This build ran it as instructed, and its own control refused to pass.

`FS_V522_PHASE_ONLY` is a shipped mutant that publishes `FS_PH_KILL_NEAR` in exactly the rounds
the fired build does and **never raises the floor**. On a nine-site enumeration of every consumer
of the phase channel it was predicted BYTE-IDENTICAL to the parent. **It differed in 5 of 12.**

Rather than explain that away, the divergence was decomposed with a probe
(`FS_V522_PROBE_NOPUB`, which performs every engine read `_v522_near_publish` performs and then
publishes nothing), because there were exactly two candidates: the two extra engine calls (which
cost CPU microseconds, and this tree has CPU-budget gates), or the phase value.

| contrast | what it isolates | identical / differing (12 deterministic games) |
|---|---|---|
| parent vs **PROBE** | the two extra engine reads | **12 / 0** — the reads are free |
| **PROBE** vs **CHAN** (`PHASE_ONLY`) | the phase VALUE | **7 / 5** |
| **CHAN** vs **FIRED** | ⭐ **THE FLOOR ITSELF** | **7 / 5** |

**AND THEN THE 5 DIFFERING GAMES WERE OPENED.** Files identical in length; **167 differing bytes
in total; every one of them a varint whose value differs by exactly `+2048`**, which is
`(6 − 5) << FS_PHASE_SHIFT`:

```
atoll_B         same_len=True  ndiff=  5  distinct varint deltas = [2048]
drakkarfjord_A  same_len=True  ndiff= 19  distinct varint deltas = [2048]
drakkarfjord_B  same_len=True  ndiff=  8  distinct varint deltas = [2048]
glacierkeep_A   same_len=True  ndiff=110  distinct varint deltas = [2048]
nordkap_A       same_len=True  ndiff= 25  distinct varint deltas = [2048]
```

Corroborated on a second channel: with `FS_LOG` on, the two arms' full stderr tapes are
**byte-identical once the phase-change log line is excluded**, and the games end with the same
winner on the same turn (`Core destroyed, turn 88`).

⇒ **`.replay26` SERIALISES THE TEAM'S PRIVATE COMMS STORE. THE DETERMINISTIC DOSE TEST DIFFS
REPLAY BYTES, SO IT CANNOT DISTINGUISH "THE BOT PLAYED A DIFFERENT GAME" FROM "THE BOT WROTE A
DIFFERENT NUMBER INTO A STORE SLOT".** A clause that only publishes state scores a **full dose**
on an instrument whose entire purpose is to answer *does this change anything?*

**THE FIX IS ONE LINE OF DESIGN, NOT A NEW TOOL: make the dose baseline an arm that writes the
SAME store word and does nothing else.** That is what `FS_V522_PHASE_ONLY` is, and the
store-blind dose below is measured against it.

⛔ **A SECOND, SMALLER CORRECTION TO THE SAME METHOD: `--seed` DOES NOT VARY A NOISE-OFF GAME, SO
THE DOSE TEST'S n IS ~3× SMALLER THAN ITS DENOMINATOR SAYS.** Measured on 12 (map, seat) cells ×
3 seeds with both sides' noise off: **11 of 12 cells produced ONE distinct stderr tape across
seeds 7/11/23** — same winner, same turn, byte-identical tape. (One cell, drakkarfjord B, produced
two, so the seed is not perfectly inert.) The replay FILES still differ across seeds — the seed
itself is serialised — which is exactly the trap: **the seed changes the replay bytes without
changing the game, so a "36-game" dose table is ~12–14 distinct games.** v521's `0/18` and `15/36`
should be read against ~6 and ~12–14.

---

## ⛔⛔ THE PRE-HEADLINE REACHABILITY CENSUS — THE DESIGN CHANGED TWICE ON MEASUREMENT

**36 instrumented games (6 maps × 3 seeds × 2 seats, noise off both sides, `MAG522` + `PH522` on)
were run before a single headline block**, in v521's own idiom. The first tape read **45 binds
against 348 rounds in which the Core READ the NEAR code — a 13% conversion** — and named both
causes.

**DEFECT 1 — THE CORE'S OWN FUNDING RE-CHECK KILLED 100 OF 100 GLACIERKEEP NEAR ROUNDS.**

```
MAG522 201 ph 6 on 1 near 1 fund 0 ttl 1 ti 16 ammo  8 bar 8 want 22 floor 16 bind 0
MAG522 589 ph 6 on 1 near 1 fund 0 ttl 1 ti 14 ammo  0 bar 7 want 20 floor 14 bind 0
   (fund, ttl, want>floor) histogram over all 100 NEAR rounds: {('0','1','want>floor'): 100}
```

Every one failed on `fund = 0` at `ammo` 8 or 0, while the RAIDER's publish-time check had passed
at ≥ 10 in the round before. **The two reads are one round apart and the turret FIRES in
between** — a sentinel shot costs 10 and the magazine cycles 10 → 0 every reload. So `ammo ≥ 10`
read on the Core is not *"the turret is funded"*, it is *"the magazine has a spare shot after the
one it just took"*, and it stands the plank down in precisely the state it exists for.
⇒ `FS_V522_CORE_FUND = False`: the funding term MOVES to the read that measures it (the raider
still refuses to publish below `FS_V522_FUND_AMMO`); it is not deleted.

**DEFECT 2 — THE CORE WAS BLIND TO BODY 2.** `_fs_state` reads `SLOT_FS`, body 1's word; body 2
publishes into `FS_SUPP_SLOT` (v514 change D, one writer per slot). Measured by body tag:
**nordkap 60 of 69 publishes from body 2; glacierkeep 68 of 269; drakkarfjord 12 of 20.**
⇒ `FS_V522_CREW_READ = True`: the Core reads the NEAR code off every slot a crew body publishes
into (`_fs_crew_slots`), **with a freshness test the `SLOT_FS` path does not have**, so a dead
body's last word cannot pin the floor.

**THE CENSUS RE-RUN AFTER BOTH CORRECTIONS** (12 games, noise off, one seed — the seed being
inert is established above):

| game | PH522 pub | Core read NEAR | **BIND** |
|---|---|---|---|
| atoll_A | 0 | 0 | 0 |
| atoll_B | 5 | 5 | **5** |
| drakkarfjord_A | 19 | 16 | **16** |
| drakkarfjord_B | 5 | 4 | **4** |
| **glacierkeep_A** | 110 | 108 | **108** *(was 0)* |
| glacierkeep_B | 0 | 0 | 0 |
| midgard_A / _B ⚠ | 0 | 0 | 0 |
| **nordkap_A** | 25 | 24 | **24** *(was 1)* |
| nordkap_B | 0 | 0 | 0 |
| yulerune_A / _B ⚠ | 0 | 0 | 0 |
| **TOTAL** | **164** | **157** | **157** |

⇒ **publish → bind conversion 13% → 96%.** midgard and yulerune (`FS_V519_CRIPPLE_MAPS`) read
zero, which is the shape a standdown must have.

⛔ **BOTH CORRECTIONS WERE MADE BEFORE ANY HEADLINE GAME AND BOTH ARE FLAGGED, so each is its own
isolation arm rather than a silent widening.** Neither loosens a gate: (1) moves a term, (2) reads
a channel a peer body already writes.

---

## THE PRE-HEADLINE DOSE GATE — STORE-BLIND, AND IT PASSES

Baseline = `FS_V522_PHASE_ONLY` (writes the identical store word, never raises the floor), so
this table measures **the floor and nothing else**.

| map | changed / cells |
|---|---|
| atoll | 3 / 6 |
| **drakkarfjord** | **6 / 6** |
| **glacierkeep** | **3 / 6** |
| midgard ⚠ *(cripple)* | **0 / 6** |
| **nordkap** | **3 / 6** |
| yulerune ⚠ *(cripple)* | **0 / 6** |
| **TOTAL** | **15 / 36** |

**The mandate's gate is ≥ 1 of 18 on the maps where the plank runs; the reading is 12 of 18.** The
naive (non-store-blind) dose against the parent reads the same 15/36 — which is a coincidence of
this build's cell pattern and not a reason to trust the naive form.

⚠ Under the seed correction above, `15/36` is ~5 of ~12–14 distinct games.

---

## ⭐⭐ CENTREPIECE 1 — THE OVERLAP CURRENCY, n=1,080/arm, replay-side

*(`overlap.py`, eight guards driven to both verdicts — `--selftest` PASS, see ARTIFACTS. Funding
is read **off the wire**; no bot stdout is involved.)*

**OVERLAP = rounds in which the collar is SIMULTANEOUSLY sealed AND a forward turret of ours is
alive AND the magazine holds ≥ 10 ammunition.**

| arm | n | sealed_r | livefund_r | **OVERLAP_r** | ovl > 0 | med ovl 1st | **net dmg / overlap round** | net dmg / other round |
|---|---|---|---|---|---|---|---|---|
| parent (baseline) | 1080 | 55.9 | 67.6 | **12.19** | 38.9% | 85 | **7.33** | 1.19 |
| **v522 FIRED** | 1080 | 54.1 | 61.9 | **12.37** | 37.4% | 81 | 7.04 | 1.21 |
| flagoff *(known-zero)* | 1080 | 62.0 | 67.6 | **14.20** | 39.2% | 102 | 6.72 | 1.12 |

| contrast | Δ OVERLAP rounds/game | half-width 95% | verdict |
|---|---|---|---|
| **v522 FIRED vs baseline** | **+0.178** | 2.329 | inside |
| **flagoff vs baseline** *(byte-identical play)* | **+2.006** | 2.426 | inside |

⛔⛔ **FINDING 1 — THE BUILD IS A NULL ON ITS OWN CURRENCY, AND THE KNOWN-ZERO ARM IS WHAT MAKES
THAT STATEMENT WORTH ANYTHING.** The treatment moved OVERLAP by **+0.18 rounds/game**; a
byte-identical arm in the same blocks on the same seeds moved it by **+2.01**. **The
same-config noise on this column at n=1,080 is roughly eleven times the treatment effect.**
Anything read off OVERLAP at this n and below ±2.4 rounds/game is unreadable, and that is a
property of the fixture, not of this plank.

⭐⭐ **FINDING 2 — THE 6× GAP REPLICATES A THIRD TIME AND IS NOW THE MOST STABLE NUMBER THE LINE
HAS.** Pooled net damage on their core per OVERLAP round against per non-overlap round:
**7.33 / 1.19 (parent), 7.04 / 1.21 (v522), 6.50 / 1.12 (flagoff)** — against v521's
**6.97 / 1.13** on a different baseline and different seeds. **Overlap rounds are worth ~6× a
non-overlap round; nothing anyone has built moves the share of them.**

⚠ **FINDING 3 — THE TREATMENT'S SIGN ON THE TWO MARGINALS IS NOT THE ONE THE DESIGN PREDICTS,
AND IT IS REPORTED RATHER THAN SMOOTHED.** v522 lowers `sealed_r` 55.9 → 54.1 and `livefund_r`
67.6 → 61.9. The design buys BARRIERS with titanium that would otherwise have become ammunition,
so a small fall in funded-turret rounds is expected; a fall in SEALED rounds is not. Both sit
inside the known-zero arm's own excursion (which moved `sealed_r` the other way, 55.9 → 62.0), so
**the honest reading is that neither marginal is resolvable here**, and the collar-barrier count
in the heal-back section agrees (15.97 vs 16.88 vs 17.17).

---

## ⭐⭐ CENTREPIECE 2 — THE `KILL_TARGET` PANEL, n=1,080/arm, THREE ARMS CONCURRENT PER BLOCK

**30 blocks × 36 games**, 6 maps (the standard 5-map siege grid plus yulerune) × 3 seeds × 2
seats, vs `bots/_v488beltbreak2`. All three arms run **inside the same block on the same seeds**
(`--seed` does not pin a game, v515 finding 1). A block counts only when all three arms finished
all 36 games; **30 of 30 did**.

| | **parent (baseline)** | **v522 FIRED** | **flagoff — KNOWN-ZERO** |
|---|---|---|---|
| WINS | 733/1080 (67.9%) | 733/1080 (67.9%) | 724/1080 (67.0%) |
| ≤r150 | 247 (0.229) | 241 (0.223) | 217 (0.201) |
| **≤r180 (`KILL_TARGET` median mark)** | 301 (0.279) | 302 (0.280) | 282 (0.261) |
| **≤r200 (TRACKED METRIC)** | 343 (0.318) | **340 (0.315)** | 318 (0.294) |
| ≤r250 | 422 (0.391) | 424 (0.393) | 395 (0.366) |
| **≤r300 (ITT primary, `DEFENCE_ADMISSION_BAR`)** | 485 (0.449) | 492 (0.456) | 452 (0.419) |
| **median kill round** | **196** | **193** | 213 |
| our core destroyed | 300 | 306 | 312 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v522 FIRED vs baseline** | **+0.00 pp** (hw 3.94) inside | **−0.28 pp** (hw 3.92) inside | **+0.65 pp** (hw 4.20) inside |
| **flagoff vs baseline** *(byte-identical play)* | −0.83 pp (hw 3.95) inside | −2.31 pp (hw 3.89) inside | −3.06 pp (hw 4.18) inside |

⛔⛔ **READ THE SECOND ROW FIRST, AS IN v521 — BUT THE CONCLUSION IS THE OPPOSITE ONE.** The
known-zero arm moves **more** on every column than the treatment does (−0.83 / −2.31 / −3.06
against +0.00 / −0.28 / +0.65), and its median kill is 17 rounds off the baseline's on
byte-identical play. **v522 changes the kill clock less than the fixture's own noise does.**

⚠ **`DEFENCE_ADMISSION_BAR` — THE RESTATEMENT THE DEFF CLAUSE REQUIRES.** The r300 ITT primary
reads **+0.65 pp with a half-width of 4.20**, i.e. a FAIL-TO-EXCLUDE with a positive point
estimate. Per CLAUDE.md that class must be restated as an exclusion before any correction is
applied, and restated (*"does the CI exclude a regression at r300?"*) **it does not**: the
interval spans −3.55 to +4.85. **This report does NOT claim v522 clears the admission bar; it
claims the point estimate is positive, the interval is uninformative at this n, and the
known-zero arm's own r300 excursion (−3.06 pp) is five times larger than the treatment's.**
⛔ Local fixture: the s39 audit measured a pair-weighted local DEFF of 0.98, so the platform
constants (1.529 rated / 1.833 unrated) do not apply and are not used.

### PER MAP — wins/180 [k≤300] {k≤200}

| map | parent | **v522 FIRED** | flagoff |
|---|---|---|---|
| atoll | 109 [62] {36} | 109 [63] {36} | 103 [55] {34} |
| drakkarfjord | 164 [135] {123} | **168** [142] {133} | 166 [133] {127} |
| glacierkeep | 148 [108] {83} | 147 [109] {**76**} | 149 [104] {79} |
| midgard ⚠ | 96 [58] {32} | **104** [63] {**26**} | 92 [51] {22} |
| nordkap | 135 [83] {52} | 129 [76] {55} | 127 [70] {39} |
| yulerune ⚠ | 81 [39] {17} | 76 [39] {14} | 87 [39] {17} |

⭐ **THE INTERNAL CONTROL IS THE ONE THAT SHOULD WORRY THE READER, AND IT IS REPORTED AS SUCH.**
midgard and yulerune are `FS_V519_CRIPPLE_MAPS` cells where **0 of 24 games fire any v522 clause**
(assertion below), so those two rows are *by construction* pure fixture noise — and they move
96 → 104 and 81 → 76, i.e. **±8 wins in 180 with a dose of exactly zero.** That is the floor,
measured in this very table, and it is larger than every difference in the four rows that could
be real.

### THE PHASE BUDGET — `phase.py`, replay-side, n=1,080/arm

Kill mark cross-checked against the grid TSV in all 3,240 games: **1 alarm in 3,240** (flagoff
arm), and the `tsv_turn − walker_round` histogram is the single value `{1: …}` in every arm.

| arm | med ARRIVE | med SENT | med FUNDED | med KILL | arrive→sent | sent→funded | **funded→kill** |
|---|---|---|---|---|---|---|---|
| parent | 13.5 | 85.0 | 88 | 195.0 | 70.5 | 0 | **69.0** |
| **v522 FIRED** | 13.5 | 88 | 91 | **191.5** | 71 | 0 | **73** |
| flagoff *(known-zero)* | 14.0 | 92.0 | 96.0 | 212 | 76.0 | 0 | **72.0** |

⭐ **THE CELL v521 DIED ON IS FLAT.** v521's whole regression was `funded → kill` **69 → 100**
against a known-zero at 69. v522 reads **73 against a known-zero at 72** — the design goal of
holding one barrier's worth rather than a whole collar is met on the exact instrument that
condemned the previous dose.

---

## ⭐⭐ SINGLE-FLAG ISOLATION — TWO LEGS, AND THE SECOND EXISTS BECAUSE THE FIRST HAD NO CONTROL

### LEG 1 — n=468/arm, four arms in the same blocks, seeds 501-539 (disjoint from the headline)

| arm | n | wins | ≤r150 | ≤r180 | **≤r200** | **≤r300** | median kill | our core dead |
|---|---|---|---|---|---|---|---|---|
| parent (baseline) | 468 | 65.2% | 0.188 | 0.222 | 0.269 | 0.410 | 219 | 144 |
| `iCOREFUND` — the Core's funding re-check back ON | 468 | 66.2% | 0.222 | 0.301 | 0.329 | 0.457 | 185 | 135 |
| `iCREW` — the crew-slot read OFF | 468 | 67.3% | 0.216 | 0.284 | 0.327 | 0.481 | 192 | 127 |
| `iNOPHASE` — **the parent with `FS_V521_PHASE_HONEST` OFF** | 468 | **71.6%** | 0.231 | 0.288 | 0.316 | 0.451 | 195 | 110 |

| contrast vs baseline | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| `iCOREFUND` | +1.07 pp (hw 6.08) inside | +5.98 pp (hw 5.87) OUTSIDE *(under the floor)* | +4.70 pp (hw 6.35) inside |
| `iCREW` | +2.14 pp (hw 6.06) inside | +5.77 pp (hw 5.86) inside | +7.05 pp (hw 6.37) OUTSIDE |
| **`iNOPHASE`** | **+6.41 pp** (hw 5.96) **OUTSIDE** | +4.70 pp (hw 5.83) inside | +4.06 pp (hw 6.34) inside |

⛔⛔ **THIS LEG IS NOT READ AS THREE EFFECTS, AND THE REASON IS ON ITS FACE: ALL THREE ARMS BEAT
THE BASELINE ON EVERY COLUMN, AND THE BASELINE'S OWN MEDIAN KILL (219) IS 23 ROUNDS OFF ITS
HEADLINE VALUE (196 AT n=1,080).** That is the signature of a low baseline draw. The leg had **no
known-zero arm of its own**, which is exactly the gap v519 open item 2 exists to warn about, so a
second leg was run rather than a paragraph written.

### LEG 2 — n=468/arm, **WITH A BYTE-IDENTICAL KNOWN-ZERO ARM**, seeds 801-839

| arm | n | wins | ≤r180 | **≤r200** | **≤r300** | median kill | our core dead |
|---|---|---|---|---|---|---|---|
| parent (baseline) | 468 | 69.2% | 0.263 | 0.293 | 0.447 | 217 | 125 |
| **`parentB` — THE SAME TREE, second copy (KNOWN-ZERO)** | 468 | 66.0% | 0.271 | 0.303 | 0.400 | 200 | 130 |
| `iNOPHASE` | 468 | 67.5% | 0.261 | 0.293 | 0.427 | 205 | 125 |
| `v522` FIRED | 468 | 68.6% | 0.282 | 0.314 | 0.442 | 201 | 133 |

| contrast vs baseline | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **`parentB` (KNOWN-ZERO)** | **−3.21 pp** (hw 6.00) | **+1.07 pp** (hw 5.86) | **−4.70 pp** (hw 6.33) |
| **`iNOPHASE`** | **−1.71 pp** (hw 5.96) | +0.00 pp (hw 5.83) | −1.92 pp (hw 6.36) |
| `v522` FIRED | −0.64 pp (hw 5.93) | +2.14 pp (hw 5.89) | −0.43 pp (hw 6.37) |

⛔⛔ **`iNOPHASE` DOES NOT REPRODUCE. +6.41 pp THEN −1.71 pp, OPPOSITE SIGNS ACROSS TWO DRAWS, AND
IN THE DRAW THAT HAS A CONTROL IT MOVES LESS THAN THE CONTROL DOES (−1.71 against −3.21).** The
one-draw law applies and the leg-1 reading is withdrawn as a draw artefact. **What survives is
that v521's clause 1e is STILL not isolated to a resolution anyone should ship on** — two draws at
n=468 with an ~5 pp floor cannot separate it, and that is a doctrine item, not a finding.
⭐ And v522 reads −0.64 / +2.14 / −0.43 beside a known-zero at −3.21 / +1.07 / −4.70 — **a second
independent confirmation of the headline null, on seeds disjoint from it.**

---

## PER-CHANGE VERIFICATION — mechanism arms, zero-vs-nonzero

**7 arms × 36 games (6 maps × 3 seeds × 2 seats), both instruments ON, vs `_v488beltbreak2`.**
⛔ The win column of a mechanism arm is not read. `mechread.py --selftest` PASS on five guards
including a full mutation, a single-column mutation, a FIELD mutation and a malformed line that
must be REPORTED.

| arm | ph_lines | **ph_pub** | ph_body2 | mag_lines | **mag_near** | mag_fund | **mag_bind** | PARSE_BAD |
|---|---|---|---|---|---|---|---|---|
| `mF` all on | 1554 | **447** | 264 | 4579 | **432** | 729 | **432** | 0 |
| `mFLOOR` FS_V522_FLOOR off | 1732 | **0** | **0** | 3917 | **0** | 1892 | **0** | 0 |
| `mCHAN` PHASE_ONLY | 4022 | 503 | 269 | 6243 | 1257 | 1859 | **0** | 0 |
| `mFUND` CORE_FUND back on | 2036 | 387 | 186 | 2888 | 334 | 1350 | **258** | 0 |
| `mCREW` CREW_READ off | 1752 | 233 | 175 | 3903 | **92** | 1442 | **92** | 0 |
| `mBIND` BIND_IF off | 1213 | **853** | 471 | 3489 | 577 | 1367 | **505** | 0 |
| `mOff` master off | 932 | **0** | **0** | 3257 | **0** | 964 | **0** | 0 |

⭐ **`mOff`'s AND `mFLOOR`'s ZEROES ARE REAL, NOT VOID.** Both log flags are gated on themselves
rather than on the master, so with `LOKI_FS_V522 = False` the tape still emits **932 PH522
eligibility lines and 3,257 MAG522 magazine rounds** while every mechanism column reads exactly
zero. The denominator is visible, so the zero means something — v521 achieved this for the first
time and this build keeps it.

⭐ **`mCHAN` IS THE CHANNEL/MECHANISM SEPARATION AS A UNIT TEST:** it publishes 503 times and the
Core reads NEAR 1,257 times, and it BINDS **zero**.

⭐ **BOTH REACHABILITY CORRECTIONS ARE CONFIRMED AT THE MECHANISM LEVEL, NOT ONLY AT THE CENSUS:**
`mFUND` takes binds 432 → **258** (−40%) and `mCREW` takes the Core's NEAR reads 432 → **92**
(−79%) while still showing 175 body-2 publishes it cannot see.

⚠ **`mCHAN`'s `mag_near` (1,257) IS ~3× `mF`'s (432), AND THAT IS THE MECHANISM WORKING, NOT AN
ALARM.** With the floor never raised the collar stays one barrier short, so NEAR windows persist;
with it raised they close. It is the clearest positive signal in the build and it does not survive
into any outcome column.

---

## ⛔⛔ THE STANDDOWN ASSERTION — CRIPPLE **AND** GATED, WITH A POSITIVE CONTROL

**PER-GAME, n=24 per board, every v522 instrument ON. A single leaking game cannot hide in a
mean.** archipelago is played vs `bots/_v468kladturbo`, the other three vs `_v488beltbreak2`.

| board | mechanism | n | games with a NEAR **publish** | with the Core **reading** NEAR | with a **BIND** | tracebacks |
|---|---|---|---|---|---|---|
| **yulerune** | CRIPPLE | 24 | **0** | **0** | **0** | 0 |
| **midgard** | CRIPPLE | 24 | **0** | **0** | **0** | 0 |
| **archipelago** | GATED | 24 | **0** | **0** | **0** | 0 |
| **nordkap** | *neither — POSITIVE CONTROL* | 24 | **15** | **15** | **15** | 0 |

⇒ **ON BOTH CRIPPLE MAPS AND ON THE GATED MAP, NO v522 CLAUSE FIRES IN ANY GAME.** The assertion
fires on the control board, so it has been seen to produce the other verdict.

---

## FLAG-OFF AUDIT

**Structural.** Every v522 branch reads `LOKI_FS_V522` (and its own sub-flag) at RUN time:
`siege.py` at the publish and the crew-slot read; `main.py` at the magazine floor and the two
phase-parity sites. `raid.py` and `eco.py` are byte-identical to the parent (md5 equal to the
freeze).

**Two additions are not individually guarded, and each is disclosed rather than argued away:**
1. `_v522_near_publish` is always *called* from the phase block; it returns immediately unless the
   master is on or its own log flag is set, and the byte-identity test below covers it
   empirically (and the PROBE arm proves its engine reads cost nothing).
2. `_v522_crew_near` is called only under `FS_V522_CREW_READ` inside the master-gated block.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v522 flag):

```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v522 derived defaults: 0 []
v521 derived defaults (inherited, must also be 0): 0 []
v520 derived defaults (inherited, must also be 0): 0 []
v519 derived defaults (inherited, must also be 0): 0 []
v518 derived defaults (inherited, must also be 0): 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```

⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see the
known v515 hazard in this very file before its zero for v522 is believed.

**`collide.py`, the mandatory slot-10 pre-flight, driven to BOTH verdicts:**

| configuration | crew | home ferry | COLLISION | |
|---|---|---|---|---|
| v522 FIRED | True | False | False | PASS |
| v522 master OFF ≡ the v521-verdict parent | True | False | False | PASS |
| v520 master OFF (crew OFF, home ferry ON) | False | **True** | False | PASS |
| **KNOWN-BAD control** (crew ON at the definition site, read-site fix disabled) | True | True | **True** ⛔ | PASS — *the detector is proved able to see the defect it exists for* |

**Byte-identity — and the baseline is an INDEPENDENTLY CONSTRUCTED tree.** `arms/parent` is
`bots/_v521sync` with `FS_V521_SYNC` and `FS_V521_COLLARFIRST` turned off **at their definition
sites**, not a copy of the treatment with an override appended. 12 games, 6 maps × 2 seats, same
seeds, randomness off — ours AND the opponent's:

```
NEGATIVE CONTROL  parent vs parent (same tree, two runs)   : identical 12 / differing  0
TEST              parent vs v522 FLAG-OFF                  : identical 12 / differing  0
CHANNEL CONTROL   parent vs v522 PHASE_ONLY                : identical  7 / differing  5   *(see below)*
POSITIVE CONTROL  parent vs v522 FIRED                     : identical  7 / differing  5
```

⇒ **`LOKI_FS_V522 = False` PLAYS THE PARENT-AS-CONFIGURED BYTE FOR BYTE**, two separately built
trees producing the same 12 games.
⛔ **THE CHANNEL CONTROL'S 5 DIFFERING GAMES ARE NOT BEHAVIOURAL AND THAT IS PROVED, NOT
ASSERTED** — 167 differing bytes, all `+2048` varints, files identical in length, stderr tapes
identical modulo the phase-change log line, same winner on the same turn. See the instrument
section.

**Behavioural.** The `flagoff` arm is not a separate leg — it is **the third arm of the headline
grid, in the same blocks, on the same seeds**, at n=1,080 (mandate asked ≥180).

---

## ⛔ MANDATE STEP 0 — THE BASELINE VS A v520-PINCER-ONLY + LEAKFIX REFERENCE

Run before anything else, 12 deterministic games, noise off on both sides. The reference arm is
the same tree with `FS_V521_PHASE_HONEST` additionally False, so the contrast isolates v521
clause 1e and nothing else.

```
NEGATIVE CONTROL  v520ref vs v520ref : identical 12 / differing  0
TEST              v520ref vs parent  : identical  8 / differing  4
```

**NOT byte-identical, and the mandate anticipated exactly this: PHASE_HONEST changes a published
channel.** The two arms differ by **one module-level constant**, read at **one site**
(`siege.py:999`), whose only effect is the value assigned to `phase`. So by construction every
behavioural difference propagates through the phase channel — the four sites that separate
`FS_PH_KILL` (4) from `FS_PH_KILL_OPEN` (5) are `eco.py:408`, `main.py:612/639/1130` and
`siege.py:4318`, all of them range tests bounded above by `FS_PH_KILL`, plus `main.py:701`
(`fs_ph == FS_PH_KILL`). **Documented, not waived**; and `iNOPHASE` in both isolation legs is the
outcome-side read of the same question (see above — it does not resolve).

---

## HEAL-BACK AND THE COLLAR — `crip.py`, replay-side, n=1,080/arm

*(Guard: the TEAM-SWAP POSITIVE CONTROL re-reads one game with `our_team` flipped and must move
the columns.)*

| | parent | **v522 FIRED** | flagoff *(known-zero)* |
|---|---|---|---|
| **median heal-back** (n=835/826/822 games with a defined ratio) | **0.000** | **0.000** | **0.000** |
| mean heal-back | 0.266 | 0.264 | 0.243 |
| share of games heal-back ≥ 0.90 | 11.5% | 12.7% | 10.5% |
| **collar barriers / game** | 16.88 | **15.97** | 17.17 |
| damage we landed on their core / game | 638.2 | **593.5** | 606.8 |
| their core healed / game | 306.3 | 270.4 | 276.8 |
| damage landed on OUR core / game | 361.9 | **399.4** | 368.3 |
| their belts built / game | 28.31 | 28.42 | 28.80 |
| their harvesters built / game | 5.68 | 5.75 | 5.72 |
| first forward sentinel (round) | 66.3 | 64.3 | 64.6 |

⛔ **THE COLLAR-BARRIER COLUMN DOES NOT MOVE THE WAY THE DESIGN PREDICTS.** v522 is supposed to
buy barriers with titanium the magazine would have taken, and it builds **fewer** (15.97 vs
16.88), with the known-zero arm at 17.17 — i.e. the treatment and the control straddle the
baseline and the column is not resolvable at this n. ⚠ `ourcore_dmg` rises 361.9 → 399.4 against a
known-zero at 368.3, which is the largest single movement in this table and is **unexplained**;
`oppcore_dmg` falls 638 → 594 against a known-zero at 607. Neither is separable from the control's
own excursion, and neither is claimed.

---

## FAILURE REEL — and it reproduces v521's finding about the CONVENTION

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in EACH of the six
maps, for the `v522 FIRED` arm**, across the 30 headline blocks. Ties: lowest block → lowest seed
→ seat A; no tie occurred.

| # | game | our core dead | **overlap_r** | sealed_r | livefund_r | class |
|---|---|---|---|---|---|---|
| 1 | `atoll_s45_B` | r144 | **0** | 0 | 0 | NO_TURRET |
| 2 | `drakkarfjord_s18_A` | r377 | **0** | 0 | 0 | NO_TURRET |
| 3 | `glacierkeep_s40_A` | r206 | **0** | **22** | 0 | **SEAL_SHOT_DISJOINT** |
| 4 | `midgard_s65_A` | r135 | **0** | 0 | **55** | HEAL_OUTRUN *(cripple cell)* |
| 5 | `nordkap_s78_B` | r146 | **0** | 0 | **109** | AUTOPSY #2 — bought, funded, useless |
| 6 | `yulerune_s16_B` | r108 | **0** | 0 | 0 | NO_TURRET *(cripple cell)* |

⭐⭐⭐ **OVERLAP IS ZERO IN 6 OF 6 AGAIN, AGAINST A POPULATION MEAN OF 12.37 AND A POPULATION SHARE
OF 37.4% ABOVE ZERO.** v521 established that the reel convention selects the tail and the tail has
no overlap; **this build reproduces it on a different arm, a different baseline and different
seeds. The convention is overlap-blind as a property of the convention.**

⭐ **ROW 3 IS v520's `glacierkeep_s37_A` AND v521's `glacierkeep_s83_A` FOR THE THIRD TIME**: a
simultaneously-sealed collar held for 22 rounds with a funded turret alive for **zero** of them.
Three builds have now been aimed near this failure and none has moved it.
⭐ **ROW 5 IS v521's ROW 5 AGAIN**: a forward turret alive and funded for **109 rounds** and the
core dead at r146. No magazine plank reaches that.

### REEL EXTENSION (mandate) — the 2 LATEST-KILL WINS

The mandate notes the reel convention is overlap-blind and asks for the other tail. These are
extension rows, labelled, and are **not** folded into the six.

| game | kill round | **overlap_r** | sealed_r | livefund_r | net damage in |
|---|---|---|---|---|---|
| `nordkap_s56_A` | r925 | **36** | 232 | 378 | 252 |
| `atoll_s47_B` | r892 | **0** | 0 | 100 | — |

⭐ **AND THE EXTENSION EARNS ITS PLACE ON ITS FIRST OUTING.** The latest-kill win carries
**overlap 36 with 232 sealed rounds and 378 funded-turret rounds** — the two windows overlapped
for 15% of the sealed time and the kill still took 925 rounds. **A game can have the most overlap
in the build and still be a near-defeat**, which is a fact the reel's own six rows (all zero)
could never have shown, and it is a caution against reading OVERLAP as a sufficient statistic for
the kill clock.

⛔ **NO NEW CAUSE TOKEN IS COINED.** Row 3 is `SEAL_SHOT_DISJOINT`, accepted as coined by the s51
builder verdict. `corpus/failure_reel.tsv` is **not** appended by this build — the builder may
want the six rows in it; the selection rule and the replays are recorded in
`scratchpad/s51_v522_build/` so the append is a one-liner if wanted.

---

## SURPRISES (written down before being explained away)

1. **⭐⭐⭐ `.replay26` SERIALISES THE PRIVATE COMMS STORE, SO THE PROMOTED DOSE TEST SCORES A FULL
   DOSE FOR A CLAUSE THAT PLAYS AN IDENTICAL GAME.** Nobody predicted that the method v521
   promoted as a standard gate could be satisfied by a store write. Proved: 167 differing bytes
   across 5 games, every one a `+2048` varint, files identical in length, tapes identical, same
   winner on the same turn.
2. **⭐⭐ `--seed` DOES NOT VARY A NOISE-OFF GAME (11 of 12 cells), BUT IT DOES CHANGE THE REPLAY
   BYTES.** So a dose table's denominator is ~3× its distinct-game count, and the seed column is
   a trap on any byte-diff instrument.
3. **⭐⭐⭐ THE CORE'S OWN FUNDING RE-CHECK — THE MOST OBVIOUS SAFETY GUARD IN THE DESIGN — KILLED
   100 OF 100 GLACIERKEEP NEAR ROUNDS.** The magazine cycles 10 → 0 on every sentinel reload, so
   `ammo >= 10` read one round after the raider's own check measures "a spare shot", not
   "funded". A guard written to prevent v521's failure mode reproduced v521's failure mode.
4. **⭐⭐ THE CORE HAS NEVER READ BODY 2's PUBLISH CHANNEL, AND ON NORDKAP THAT IS 60 OF 69
   PUBLISHES.** `FS_SUPP_SLOT` has existed since v514; every Core-side consumer of the phase
   reads `SLOT_FS` only. This build fixes it for its own term and **leaves `_fs_salt_ok`'s
   identical asymmetry untouched** (see doctrine collisions).
5. **⛔⛔ THE KNOWN-ZERO ARM MOVED `OVERLAP` BY +2.01 ROUNDS/GAME AND THE MEDIAN KILL BY 17 ROUNDS,
   ON BYTE-IDENTICAL PLAY, AT n=1,080.** The currency this build exists to move has a noise floor
   ~11× the treatment effect. Any future plank priced against OVERLAP needs either a much larger
   n or a paired design.
6. **⛔ THE CRIPPLE-MAP ROWS OF THE HEADLINE PANEL MOVE ±8 WINS IN 180 WITH A DOSE OF EXACTLY
   ZERO** (0 of 24 games fire any clause). The internal control measures the floor inside the
   headline table itself.
7. **⛔ THE FIRST ISOLATION LEG SAID `iNOPHASE` WAS +6.41 pp OUTSIDE; THE SECOND, WITH A
   KNOWN-ZERO ARM, SAID −1.71 pp.** Two draws, opposite signs. The leg without a control was
   uninterpretable and would have been reported as a finding by any convention that does not
   demand one.
8. **⭐ THE MECHANISM'S CLEAREST POSITIVE SIGNAL IS IN A MUTANT.** `mCHAN` (floor never raised)
   shows the Core reading NEAR **1,257** times against `mF`'s **432** — NEAR windows persist when
   the collar stays one barrier short and close when it does not. The mechanism visibly does its
   job and none of it reaches an outcome column.
9. **⚠ v522 BUILDS FEWER COLLAR BARRIERS THAN THE PARENT (15.97 vs 16.88)** — the opposite of the
   design's prediction, though the known-zero arm (17.17) straddles it.
10. **⚠ `ourcore_dmg` RISES 361.9 → 399.4** against a known-zero at 368.3. Unexplained; the
    largest single movement in the heal-back table.

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The headline is n=1,080/arm, not n≥900.** Blocks ran at ~31 s, so the extra power was free.
2. **The channel is a new PHASE CODE, not a new store field.** Every slot in the 16-slot store has
   an owner and `SLOT_FS`'s 32 bits are fully packed (beat 0-10, phase 11-13, rid 14-29, v520 arc
   30-31); the phase field's last free code was the only zero-cost channel. The blast radius was
   enumerated (9 consumers), the 2 that separate 5 from 6 are behind `FS_V514_MAGGATE` (ships
   False) and were extended anyway, and the enumeration was then **measured** with the
   `FS_V522_PHASE_ONLY` mutant.
3. **The floor prices `FS_V522_SEATS` (= NEAR) seats, not the exact `needed_seats`.** The channel
   carries NEAR-ness, not a count. `FS_V522_BIND_IF` is what makes the approximation harmless: at
   one seat open the seal price already sits at or under the repair allowance on every scale where
   `bar ≥ 6`, so that state is not published at all.
4. **Two design changes were made BEFORE the headline** on the reachability census
   (`FS_V522_CORE_FUND`, `FS_V522_CREW_READ`). Both are flagged, both have isolation arms in the
   mechanism battery, and the pre-correction tape is reported beside the post-correction one.
5. **A SECOND isolation leg was run** because the first had no known-zero arm and all three of its
   treatment arms moved the same way.
6. **The gated control leg vs `_v468kladturbo` is folded into the standdown assertion** rather
   than run as a separate win-rate leg: v522 does not touch the gate, and the assertion (0 of 24
   games with any clause on archipelago) is the stronger statement.
7. **Mechanism arms are 36 games each, not 15.** Games cost ~1.3 s.
8. **`corpus/failure_reel.tsv` is not appended** (see the reel).
9. **Timeouts are not reported** (v518 finding 0).

---

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⛔⛔ THE DETERMINISTIC DOSE TEST NEEDS ITS CAVEAT PROMOTED WITH IT.** v521's builder verdict
   promoted it as *"a standard pre-headline gate for any behaviour clause"*. As run against a
   plain baseline it **cannot distinguish a behaviour change from a store write**, and its n is
   ~3× smaller than its denominator. **The fix is one line — the dose baseline must be an arm that
   writes the same store word** — but the promotion as written does not say so, and the next
   build that publishes state will get a green gate for nothing.
2. **⚠⚠ `_fs_salt_ok` CALLS THE `SLOT_FS` PHASE "THE CREW'S SHARED ANSWER" WHILE READING ONE
   BODY'S WORD.** This build measured that gap at 60 of 69 publishes on nordkap and fixed it for
   its OWN term only. The salt gate — which decides whether a sentinel may be bought at all — has
   the same asymmetry and is untouched here. **It is a bigger lever than anything v522 does.**
3. **⚠⚠ `FS_V521_PHASE_HONEST` IS STILL UNISOLATED AFTER TWO LEGS.** v521 kept it on a
   separability argument; leg 1 read +6.41 pp, leg 2 read −1.71 pp beside a known-zero at
   −3.21 pp. It ships in the parent config and nobody has a resolution on it.
4. **⚠ `FS_MAG_REPAIR_BARRIERS = 2` IS STILL PRICED AGAINST A PREMISE THAT DIED AT v515, AND
   v522's ANSWER IS A NULL.** v521 measured the "hold the whole collar" answer at −9.83 pp;
   v522 measures the "hold one more barrier while closure is NEAR" answer at −0.28 pp. **The
   constant is still unswept between 2 and 8**, and both endpoints of the design space are now
   occupied by a rejection and a null.
5. **⚠ `R1000_IS_DEFEAT` READS NEUTRAL**: median kill 196 → 193, k≤200 31.8% → 31.5%, both inside
   a known-zero arm that moved further. **`DEFENCE_ADMISSION_BAR` (r300, ITT) is a
   FAIL-TO-EXCLUDE and is restated as an exclusion in the panel section rather than banked as a
   pass.**
6. **⚠ `SHIP_BAR` IS NOT ADDRESSED AND MUST NOT BE READ INTO THIS REPORT.** A 6-map grid is
   explicitly a non-arming read in `PROGRAMME.md`.

---

## OPEN ITEMS

0. **⭐⭐ THE CURRENCY IS CONFIRMED FOR A THIRD TIME AND STILL UNCLAIMED.** 7.33 net damage per
   overlap round against 1.19 outside; **37.4% of games have overlap, 62.6% have none.** Three
   builds (v520, v521, v522) have now aimed at that share and none has moved it. **The next plank
   should probably not be a magazine plank** — the magazine has been the lever twice, at opposite
   doses, and the answers are a rejection and a null.
1. **⛔ `adj = 0` IS STILL THE UNTOUCHED HALF OF v521's DIAGNOSIS.** The other blocker in the modal
   NEAR round is that the body is not orthogonally adjacent to any open seat. v521 did not address
   it; v522 fixed only the money. **It is now the ONLY half of that diagnosis left, which raises
   its priority rather than lowering it.**
2. **⛔ THE OVERLAP INSTRUMENT'S NOISE FLOOR IS ±2.4 ROUNDS/GAME AT n=1,080** (measured on a
   byte-identical arm). Either a paired/blocked design or a much larger n is needed before any
   plank can be judged on this column.
3. **`FS_V522_NEAR` (2), `FS_V522_SEATS` (2), `FS_V522_FUND_AMMO` (10), `FS_V522_MAX_RNDS` (150),
   `FS_V522_FLOOR_CAP` (40) and `FS_V522_BIND_IF` (True) are UNSWEPT.** `mBIND` shows BIND_IF off
   raises publishes 447 → 853 and binds 432 → 505; its outcome cost is unmeasured.
4. **The TTL came close to binding at least once**: glacierkeep_A recorded 108 binds against a
   ceiling of 150. A map where the NEAR window is chronic could hit it, and nothing measures what
   happens after it does.
5. **`ourcore_dmg` +37.5/game in the treatment arm is unexplained** (§ heal-back).
6. **Inherited and untouched:** every v521 open item except 2 (the repair-barrier constant,
   addressed and answered with a null) — in particular the 9-far-launcher midgard game, the gate
   fix's downstream economics, and rung 4 being effectively dead.

---

## ARTIFACTS

`scratchpad/s51_v522_build/` —
`arms/` (parent = the definition-site baseline, parentB = its known-zero copy, v520ref, flagoff,
phaseonly, the seven mechanism arms, the three leg-1 isolation arms, iNOPHASE, and the
determinism/dose/channel arms), `grid/` (30 headline blocks × 3 arms, **all replays kept**),
`iso/` (13 blocks × 4 arms), `iso2/` (13 blocks × 4 arms incl. the known-zero),
`mech/` (7 arms), `modeassert/` (4 boards × 24 games), `eq/` (byte-identity + its negative,
channel and positive controls), `base/` (mandate step 0), `chan/` (the channel decomposition +
the code-5 substitution), `dose/` (both dose runs), `near2/` (the reachability census),
`overlap_*.tsv`, `crip_*.tsv`, `PARENT_FREEZE.md5`, `TREE_FINAL.md5`, `PIDS`, `out/` (every
driver log).

**Instruments, each guarded both ways:**
* `overlap.py --selftest` — eight guards including a MUTATION control, a SIMULTANEITY control, a
  ZERO-DENOMINATOR control returning `None` not 0, a real-data TEAM-SWAP positive control and a
  CHANNEL CROSS-CHECK (−18 `UpdateHp` on the enemy core == `FireTurret` core hits). **PASS.**
* `mechread.py --selftest` — five guards: a synthetic tape, a FULL mutation (every column 0), a
  SINGLE-COLUMN mutation, a FIELD mutation (`bind 1` → `bind 0` must zero that column alone), and
  a malformed line that must be REPORTED as `PARSE_BAD`. **PASS.**
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive control
  (2 hits, which is what makes the v522 zero mean something). **PASS.**
* `collide.py` — the slot-10 two-writer pre-flight, four configurations, both verdicts, including
  a reconstructed KNOWN-BAD form that must read `COLLISION: True`. **PASS.**
* `phase.py --guard` — synthetic empty/known/ordering guards plus the real-data kill-mark
  cross-check against the grid TSV: **1 alarm in 3,240 games**, histogram single-valued per arm.
* `crip.py --control` — the TEAM-SWAP positive control.
* `drive_eq.sh` — determinism with a negative control (same tree twice), a CHANNEL control and a
  positive control.
* `drive_chan.sh` + `FS_V522_PROBE_NOPUB` — **the channel decomposition, this build's most
  load-bearing instrument**: it separated the extra engine reads from the phase value from the
  floor, and it is what exposed the store serialisation.
* `drive_dose.sh` / `drive_dose2.sh` — the deterministic dose test, naive and **store-blind**.
* `reel.py` — the reel and its mandate extension, with the selection rule in the docstring.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* **FS_V522_FLOOR: NULL, exemplary controls** (every column inside the known-zero arm's own
  movement; binding raised 13%→96% by the pre-headline census and STILL null — the floor was
  not the constraint). Ships OFF/indifferent.
* **THE HEAD NUMBER: the current config (pincer + leakfix + PHASE_HONEST, sync off) reads
  733/1080 = 67.9% [±2.8] vs the incumbent, median kill 196 (TARGET 180 NEARLY MET), k≤200
  31.8%, k≤300 44.9%.** Cross-run caveat: v520's run read 63.8 — the ~5pp fixture floor
  spans the gap, so the honest head estimate is 64-68 on this fixture. SHIP_BAR still needs
  the full-pool powered read.
* **THE NEXT LEVER IS NAMED AND IT IS BIG: body-2 blindness.** The Core never reads the
  second raider's slot (60/69 nordkap publishes lost — FS_V522_CREW_READ flagged), the
  funding re-check measures "a spare shot" not "funded" (ammo cycles 10→0 per reload —
  FS_V522_CORE_FUND flagged), and `_fs_salt_ok` carries the same body-2 blindness UNFIXED —
  the pincer's second arc may not count toward SEALED at all. v523 = the blindness trio.
* Instrument facts adopted: **.replay26 serialises the private comms store** (deterministic
  dose tests need a same-store-write baseline — the promoted method's caveat promoted with
  it); `--seed` does not vary noise-off games (dose denominators ÷3); OVERLAP's noise floor
  ±2.4 r/g makes it a diagnostic, not a verdict metric (the r925 win with overlap 36 is the
  cautionary case). The 6× overlap damage gap replicated a third time (7.33 vs 1.19).
