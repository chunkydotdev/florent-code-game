# BUILD REPORT (DRAFT) — `bots/_v517twin` (net-damage fire discipline + the twin), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v516teardown` FROZEN (chmod -R a-w) and re-verified untouched by md5
after every leg (`scratchpad/s51_v517_build/PARENT_FREEZE.md5`). Master `LOKI_FS_V517`; False
reproduces the parent (structurally audited + behaviourally measured). Diff vs parent:
doctrine +157/−0, main +86/−2, siege +392/−5, raid and eco UNTOUCHED (0/0).
**0 tracebacks, 0 timeouts, 0 no-winners in every leg** (1,350 headline + 216 gated + 360
flag-off + 120 mech games). Artifacts: `scratchpad/s51_v517_build/`.*

*⭐ MID-BUILD DIRECTIVE, folded in: `KILL_TARGET` (median kill ≤ r180; tracked metric = share of
ALL games killed by r200, baseline ~16.5%, target >50%; r300 stays the hard floor). No design
change was made in response — the kill-round CDF is reported against the r150/r180/r200/r300
marks below, and a **phase-budget readout** (ring-arrival → first-funded-turret → kill) was
built and is the most directive-relevant number in this document.*

---

## ⛔⛔ FINDING 0 — ENGINE FACT, NOVEL: A COMM-STORE SLOT IS **32 BITS UNSIGNED**, AND `write_store` **RAISES** OUTSIDE THAT RANGE

The v517 channel had to be packed into `SLOT_ROLE_N` alongside v516's beat, so the width was
probed before the packing was chosen rather than assumed
(`scratchpad/s51_v517_build/probe_store/`, one nordkap game, **positive control 12345 exact in
the same tape**):

```
STOREPROBE rnd  1 wrote 12345                match 1        <- POSITIVE CONTROL
STOREPROBE rnd  9 wrote 2147483647 (2^31-1)  match 1
STOREPROBE rnd 11 wrote 2147483648 (2^31)    match 1
STOREPROBE rnd 13 wrote 4294967295 (2^32-1)  match 1
STOREPROBE rnd 14 wrote 1099511627775 (2^40) exc WRITE:OverflowError
STOREPROBE rnd 20 wrote 2^63-1               exc WRITE:OverflowError
STOREPROBE rnd 24 wrote -1                   exc WRITE:OverflowError
STOREPROBE rnd 26 wrote -2147483648          exc WRITE:OverflowError
```

⇒ **A slot holds 0 .. 2**32−1. Every negative value and everything past 2**32−1 raises
`OverflowError` — and an exception escaping `run()` destroys that unit permanently.**
`CLAUDE.md` documents the store as "16 integer slots" with no width and no sign constraint;
this is the first measurement of either. **Consequence beyond this plank: any code that writes
a difference, a delta, or a signed offset into a slot is one negative value away from deleting
its own unit.** The v517 packing is bounded by construction and the composed word maxes at
exactly 4294967295.

**The packing this forced** (`SLOT_SENT_BEAT` = `SLOT_ROLE_N`, now full to the bit):

| bits | field | owner |
|---|---|---|
| 0-9 | role counter | v105, unchanged |
| 10-20 | beat1 = round+1 | v516 GLOBALSENT, unchanged |
| 21-24 | PEER stamp (≥2 forward sentinels) | v517 |
| 25-28 | VERDICT stamp (the net-damage clock) | v517 |
| 29-31 | NETCODE (bucketed net reading) | v517 |

21 bits were already committed, so the two v517 clocks are **mod-15 stamps, not round+1**.
That compression is the direct cause of surprise 1 below.

---

## ⛔ FINDING 1 — THE MANDATE'S FUNDING PREMISE IS FALSE AS SHIPPED, AND THE BUILD MEASURED IT MID-FLIGHT

The mandate's argument for change 2 is *"the savings buy the SECOND forward sentinel … the
bank is provably accumulating"*. On the first v517 smoke grid it is not:

```
TWINGATE517 207 atring 1 live 1 ti 16 ammo  0 cost 80 bought 1 orth 3
TWINGATE517 208 atring 1 live 1 ti 16 ammo 12 cost 80 bought 1 orth 2
...
TWINGATE517 231 atring 1 live 1 ti 16 ammo  0 cost 80 bought 1 orth 3
```

**Titanium PINNED AT 16 for twenty-five consecutive rounds of a live hold**, while ammunition
cycles 12→8→4→0 (other turrets burning it at 4/shot). The bank does not accumulate because,
with the magazine armed by v516 GLOBALSENT, the Core converts everything above `ti_floor` into
ammunition — and `main.py`'s **existing** second-sentinel hold-back (v513: *"Magnus asked for
TWO sentinels and rung 4 buys the second out of this bank"*) is gated on
`ammo >= FS_AMMO_TARGET // 2`, i.e. **150, which a starved magazine never reaches**.

⇒ **FIRE DISCIPLINE WITHOUT A FUNDING LINK SAVES AMMUNITION AND FUNDS NOTHING.** Change 2
therefore shipped in two parts: (a) the relaxed purchase gates the mandate specified, and
(b) `FS_V517_TWINBANK` — while a sentinel is HOLDING, the existing hold-back engages
regardless of the ammunition level. The precondition it drops ("don't starve the magazine") is
the one a holding turret provably cannot violate. Part (b) was not in the mandate and is the
only reason the bank moves at all (measured: 16→26, 56→66 with it on; 0 bank rounds in the
`FS_V517_TWINBANK = False` mutant).

---

## ⛔⛔ FINDING 2 — THE MANDATE'S FALSIFIER FOR CHANGE 3 IS ITSELF FALSE: THE PARENT IS **NOT** AT ZERO CONCURRENT SENTINELS

The mandate states the parent baseline as *"0 concurrent core-hitting sentinels in 6,094
rounds — ANY concurrent pair is the mechanism landing"* (from autopsy #3). Measured
replay-side on this build's own arms with the autopsy's own definition (a sentinel counts once
it has landed ≥1 shot on an enemy core tile), 30 games each:

| arm | core-hitting rounds | **concurrent (≥2) rounds** | games with any |
|---|---|---|---|
| `m1_fired` (all on) | 3,997 | **11** | 1 |
| `m1_off` (FIREDISC off — parent on this path) | 3,438 | **53** | 2 |
| `m2_off` (TWIN off) | 3,473 | **9** | 1 |
| `m2b_off` (TWINBANK off) | 2,788 | **44** | 2 |

**Every arm, including the ones that reproduce parent behaviour, shows concurrent
core-hitting sentinel rounds.** The autopsy's zero is a property of its 30-game draw, not a
structural fact about the parent. ⇒ **"any concurrent pair is the mechanism landing" cannot be
used as a falsifier**, and the twin has to be read as a DELTA against a concurrent parent arm
(headline table below), not against zero.

---

## HEADLINE — 5 siege maps, 15 blocks × 30, n=450/arm, THREE arms CONCURRENT per block, vs `_v488beltbreak2`

*(third arm = the FLAG-OFF tree, which is provably the parent on every path — the v516 gated
leg showed a same-config arm is the control a single draw cannot do without.)*

| | **v517 FIRED** | **v516 PARENT (concurrent)** | **v517 FLAG-OFF (concurrent)** |
|---|---|---|---|
| WINS | **244/450 (54.2% ±4.6)** | 248/450 (55.1% ±4.6) | 239/450 (53.1% ±4.6) |
| **kills ≤ r300 (ITT primary)** | **129/450 (28.7% ±4.2)** | 133/450 (29.6%) | 136/450 (30.2%) |
| **kills ≤ r200 (KILL_TARGET tracked metric)** | **72/450 (16.0%)** | 75/450 (16.7%) | 84/450 (18.7%) |
| our core destroyed | 186 | 182 | 192 |
| r1000 games | **40** | 69 | 55 |
| wins taken on the r1000 tiebreak | **20** | 49 | 36 |
| total core kills | **224** | 199 | 203 |
| median kill round | 262 | 217 | 220 |
| tracebacks / timeouts / no-winners | **0 / 0 / 0** | 0 / 0 / 0 | 0 / 0 / 0 |

**Δwins vs the concurrent parent −0.9 pp; Δk≤300 −0.9 pp; Δk≤200 −0.7 pp — all three INSIDE
the interval** (two-sample naive half-width ≈ 6.5 pp, and the one-draw law below makes even
that optimistic). Intervals are NAIVE and local: the s39 audit measured local pair-weighted
DEFF = 0.98, so the platform constants (1.53 / 1.83) do **not** apply and are not used.

**⭐ THE OUTCOME MIX MOVES THE SAME WAY v516 MOVED IT, ONLY FURTHER:** +25 core kills and −29
tiebreak wins against the parent, r1000 games 69 → 40, and **every extra kill lands after
r300** (301-500: 72 vs 40; >500: 23 vs 26). Under `R1000_IS_DEFEAT` that is the right
direction; under the r300 bar and the new `KILL_TARGET` it is not paid for.

### ⭐ KILL-ROUND CDF against the s51 `KILL_TARGET` marks (share of **ALL** games killed by R)

| arm | ≤r150 | **≤r180** | **≤r200** | ≤r250 | **≤r300** | ≤r400 | ≤r500 |
|---|---|---|---|---|---|---|---|
| **v517** | 24 (0.053) | **55 (0.122)** | **72 (0.160)** | 104 (0.231) | 129 (0.287) | 175 (0.389) | 201 (0.447) |
| v516 parent | 20 (0.044) | 51 (0.113) | 75 (0.167) | 114 (0.253) | 133 (0.296) | 165 (0.367) | 173 (0.384) |
| v517 flag-off | 23 (0.051) | 52 (0.116) | 84 (0.187) | 114 (0.253) | 136 (0.302) | 172 (0.382) | 183 (0.407) |

**Against the tracked metric (kills by r200, baseline ~16.5%, target >50%): v517 reads 16.0%,
the parent 16.7%, the flag-off 18.7%. All three sit ON the baseline and the spread between two
arms that are provably identical code (parent 16.7 vs flag-off 18.7) is larger than v517's
delta.** The median-kill target of r180 is not approached by any arm (262 / 217 / 220), and
**the whole three-arm CDF is flat below r250** — the curves only separate at r300+, where v517
is ahead and where the programme does not pay.

### ⭐⭐ PHASE BUDGET — where the rounds go (`phase.py`, n=450/arm, replay-side)

*Marks: ARRIVE = first round one of our builder bots is inside d²≤8 of the enemy core; SENT =
first round a forward sentinel of ours (d²≤40) is alive; FUNDED = first round such a sentinel
is alive AND team ammunition ≥10, i.e. the first round it could actually shoot (the SENTBEAT +
ammo join in replay coordinates); KILL = the round their core reaches 0. Kill mark cross-checked
against the grid TSV in all 1,350 games: **0 alarms, and the `tsv_turn − walker_round`
histogram is the single value {1: 626}** — a consistent 1-vs-0 indexing offset, not a mismatch.*

| arm | med ARRIVE | med SENT | med FUNDED | med KILL | **spawn→arrive** | **arrive→sent** | **sent→funded** | **funded→kill** |
|---|---|---|---|---|---|---|---|---|
| **v517** | 8 (444/450 games) | 88 (335) | 88 (335) | 261 (224) | 8 | **81** | **0** | 101.5 |
| v516 parent | 8 (440) | 88 (345) | 88 (344) | 216 (199) | 8 | **81** | **0** | 92 |
| v517 flag-off | 8 (443) | 89 (349) | 89.5 (348) | 219 (203) | 8 | **81** | **0** | 87 |

**⭐ TWO FINDINGS THE DIRECTIVE ASKED FOR, AND THEY POINT AT DIFFERENT PHASES:**

1. **`sent → funded` IS ZERO IN ALL THREE ARMS.** Funding is no longer a phase of this rush —
   v516's GLOBALSENT fix closed it, and this is the independent replay-side confirmation of
   that (the turret can shoot the round it exists, in the median game). **No further work on
   the magazine buys a round.**
2. **`arrive → sent` IS 81 ROUNDS AND IS IDENTICAL IN EVERY ARM.** A body is at their ring at
   r8 and the first forward sentinel does not exist until r88. **That single gap is 45% of the
   r180 target, and nothing in v516 or v517 touches it.** The post-turret phase
   (funded→kill, 87-101) is the other half. ⇒ **Reaching a median kill of r180 requires the
   turret ~50 rounds earlier, or the post-turret phase roughly halved — the ammunition path
   has nothing left to give.** (The 81-round gap is the salt/eco gate disjunction plus the
   purchase-reach defect, i.e. autopsy #2 and v516 change 3, which measured a mechanism-live /
   currency-null.)

**PER MAP** (wins/90, k≤300 in brackets) — v517 / v516 parent / flag-off:

| map | v517 | v516 parent | flag-off |
|---|---|---|---|
| atoll | **36/90 (k16)** | 38/90 (k 9) | 34/90 (k14) |
| drakkarfjord | **64/90 (k37)** | 64/90 (k35) | 55/90 (k34) |
| glacierkeep | 75/90 (k45) | **80/90 (k52)** | 80/90 (k51) |
| midgard | 18/90 (k 9) | **22/90 (k13)** | 20/90 (k10) |
| nordkap | **51/90 (k22)** | 44/90 (k24) | 50/90 (k27) |

**PER BLOCK (wins/30), v517 / parent / flag-off:** 19/21/16 · 17/20/17 · 13/13/14 · 20/15/17 ·
14/15/14 · 17/18/19 · 16/17/18 · 16/17/18 · 18/12/15 · 19/17/12 · 13/20/12 · 13/15/17 ·
18/14/16 · 14/16/19 · 17/18/15.
**The per-block spread is ±4 games on a mean of 16 and the three arms trade the lead
constantly. No n=30 or n=90 cut of this table is a conclusion.**

---

## PER-CHANGE VERIFICATION (every mutant driven, zero-vs-nonzero)

### 1 — FIREDISC (`FS_V517_FIREDISC`)

**(a) Instrument, both ways.** `FIREDISC517` stderr events over the 30-game mech grids:

| arm | FIREDISC rounds / games | hold rounds | code=HELD rounds | **first-contact violations** | TTL re-probes |
|---|---|---|---|---|---|
| `m1_fired` | **4,012 / 20** | 264 | 275 | **0** | 10 |
| `m1_off` mutant | **0 / 0** | 0 | 0 | 0 | 0 |
| `m2_off` | 3,485 / 22 | 493 | 513 | **0** | 20 |
| `m2b_off` | 2,907 / 20 | 306 | 318 | **0** | 12 |

Zero-vs-nonzero ✅. **⛔ THE CRITICAL FALSIFIER READS 0 IN ALL 10,404 INSTRUMENTED ROUNDS
ACROSS 90 GAMES: the discipline never held inside the fresh-contact window.** It is structural
(a verdict cannot exist until the W-shot buffer is full, and the TTL reset empties the buffer,
so a re-probe also gets its W free shots) — the counter exists so the code cannot drift off
that guarantee unnoticed.

**(b) ⭐ THE CHANNEL IS REAL — the published core-HP reading joined to the replay's own series,
with the negative controls in the same run** (`netjoin.py`, `m1_fired`, 4,012 published
readings over 20 games, all 20 with a VARYING enemy-core HP series so a flat series cannot
manufacture a match):

| join | rate |
|---|---|
| offset −2 | 0.1939 |
| offset −1 | 0.2792 |
| **offset 0 (the join under test)** | **0.6578** |
| offset +1 | 0.1112 |
| offset +2 | 0.0808 |
| bracket (start-of-round OR end-of-round value) | 0.7465 |
| **⛔ CROSS-ARM CONTROL — the same logs joined to a DIFFERENT arm's replays** | **0.0251** |

The offset profile peaks sharply at 0 and the cross-arm control collapses it 26× (0.658 →
0.025). **The sentinel is reading the true enemy-core HP.** The residual ~25% is the
mid-round sampling seam: the bot reads at its own turn and the replay row is end-of-round
state, so a core that is damaged *and* healed after our turn lands on neither value.

**(c) Ammunition actually withheld** (bot-side counters, per-game max summed):

| arm | held core shots | held **and funded** (≥10 ammo) | **ammo withheld** |
|---|---|---|---|
| `m1_fired` | 185 | 185 | **1,850** |
| `m1_off` mutant | **0** | **0** | **0** |
| `m2_off` | 395 | 395 | 3,950 |
| `m2b_off` | 275 | 275 | 2,750 |

⛔ The funded column is not decoration: `can_fire` returns TRUE at 0 ammo on this engine
(guard-matrix sweep), so an unfunded "saved shot" would be a shot that was never affordable.
Here every held shot was funded, which is itself the v516 GLOBALSENT fix showing through —
the magazine is armed under a firing turret now.

### 2 — TWIN (`FS_V517_TWIN`, `FS_V517_TWINBANK`)

**(a) Instrument, both ways.**

| arm | `TWINBANK517` rounds / games | `TWINGATE517` rounds / games |
|---|---|---|
| `m1_fired` | **540 / 2** | **225 / 1** |
| `m2_off` mutant (TWIN off) | **0 / 0** | **0 / 0** |
| `m2b_off` mutant (TWINBANK off) | **0 / 0** | 270 / 4 |
| `m1_off` (FIREDISC off) | 0 / 0 | 0 / 0 |

Both mutants drive their own signal to zero and leave the other alone: `m2b_off` still opens
the hold gate (270 raider-at-ring-during-hold rounds) but never banks. ✅

**(b) ⛔⛔ THE PURCHASE NEVER LANDS. `TWIN517` purchases made while the hold was live: 0 of 80
sentinel purchases across the four 30-game mech arms.** The relaxed gates were never the
binding constraint. Two ceilings, both measured:

1. **REACHABILITY.** `_fs_try_sentinel` is only ever called by a LIVING raider at the ring, and
   a raider is alive at the ring during a hold in **1 of 30 games (`m1_fired`) / 4 of 30
   (`m2b_off`)** — the autopsy's 63.4% raider-blindness arriving on the purchase side. A hold
   with no `TWINGATE` line in the same round is a hold nobody can spend.
2. **PRICE.** In the one reachable window the bank reads `ti 8..24` against `cost 78..86` for
   the whole 225 rounds, and by r868 `bought 2` — at which point the existing hold-back's own
   `SLOT_FWD_GUN < FS_SENTINEL_MAX` cap closes the bank. **`FS_V517_TWINBANK` stops the CORE
   spending the bank on ammunition; it does not stop the eco and the collar spending it**, and
   at ~2.5 Ti/round of passive income a ~85 Ti turret is ~34 rounds of complete abstinence
   away.

⇒ Change 2's mechanism is live and instrumented in both directions; **its currency is
unmeasurable at this power because the state it needs (living raider + hold + one sentinel's
price in the bank) co-occurred zero times in 120 games.** Reported, not explained away.

### 3 — CONCURRENCY, the twin's replay-side currency

Replay-side, the headline fixture, n=450/arm (`sentrace.py`; "hitting" = a sentinel that has
already landed ≥1 shot on an enemy core tile, the autopsy's own definition):

| arm | core-hitting rounds | **concurrent (≥2) rounds** | games with any | core shots | **shots per hitting-round** | dealt | healed | **heal-back share** | **NET damage per shot** |
|---|---|---|---|---|---|---|---|---|---|
| **v517** | 55,284 | **396 (0.00716)** | 30 | 16,163 | **0.2924** | 290,934 | 166,140 | **0.571** | **7.72** |
| v516 parent | 68,254 | 598 (0.00876) | 29 | 21,129 | 0.3096 | 380,322 | 272,438 | 0.716 | 5.11 |
| v517 flag-off | 64,408 | 393 (0.00610) | 20 | 19,710 | 0.3060 | 354,780 | 243,296 | 0.686 | 5.66 |

**THE TWIN: NULL, and the two same-code arms bracket it.** v517 reads 396 concurrent rounds
against the parent's 598 and the flag-off's 393 — **the parent and the flag-off, which are the
same code, differ by 205 on this column**, so v517's −202 vs the parent is inside the draw
spread. `FS_SENTINEL_MAX` was never reached in a way the plank caused: 0 of 80 mech purchases
were made under a hold.

**⭐⭐ THE FIRE DISCIPLINE'S CURRENCY, HOWEVER, MOVES — AND IT IS THE COLUMN THE AUTOPSY NAMED.**
v517 fires **24% fewer core shots** (16,163 vs 21,129) and the share of its damage healed
straight back falls **0.716 → 0.571**. Damage per shot is 18.00 in every arm (the engine's
number, and a check that the shot ledger is sound), so the whole movement is in the heal-back:

> **NET damage delivered per core shot: 7.72 (v517) vs 5.11 (parent) vs 5.66 (flag-off) —
> +51% against the parent, +36% against the flag-off, on 24% fewer shots and therefore 24%
> less ammunition.** Total net damage on enemy cores is nonetheless HIGHER: 124,794 vs 107,884.

⚠ **What that column cannot say:** it is a POOLED ratio over unequal siege time (v517 has 19%
fewer core-hitting rounds than the parent — itself inside the parent-vs-flag-off spread of
3,846 rounds), and it is not conditioned on the heal-matched state the discipline targets.
It is the strongest measurement in this build and it is still a pooled read.

---

## FLAG-OFF AUDIT

**Structural.** Every behavioural site is guarded by `LOKI_FS_V517 and FS_V517_<sub>` read at
RUN time (9 guard expressions across main.py and siege.py; the helper methods
`_fs_hold_live`, `_v517_twin_live`, `_v517_bank_open`, `_v517_sent_floor` all early-return the
parent's answer on the flags, so their read sites are equivalent to the parent's lines). The
only unguarded additions are the `v517_*` state fields, which are written but read only under
a guard, and the three log flags (default False). `raid.py` and `eco.py` are byte-identical to
the parent.

**NO NEW DERIVED DEFAULTS** — `flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v517 flag:
```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v517 derived defaults: 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```
⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see
the known v515 hazard in this very file before its zero for v517 is believed.

**Behavioural.**

Two INDEPENDENT fixtures compare `LOKI_FS_V517 = False` against an untouched copy of the
parent. Both arms share seeds inside each fixture; the fixtures use different seed ranges.

| | flag-off | v516 parent | Δ |
|---|---|---|---|
| **dedicated battery, n=180 each** (6 interleaved blocks, fresh seeds 103-120) | **95/180 (52.8%)** | 85/180 (47.2%) | **+5.6 pp** |
| **headline arms, n=450 each** (15 interleaved blocks, seeds 1-45) | **239/450 (53.1%)** | 248/450 (55.1%) | **−2.0 pp** |
| **POOLED n=630 each** | **334/630 (53.02%)** | 333/630 (52.86%) | **+0.16 pp** |

n=180 detail: kills 75 vs 68, k≤300 47 vs 40, our core destroyed 78 vs 78, r1000 27 vs 34,
median kill 241 vs 257, tracebacks 0/0. Per-block wins (flag-off/parent): 11/13 · 16/15 ·
15/16 · 18/11 · 16/17 · 19/13.

**⛔⛔ THE STRONGEST STATEMENT OF THE ONE-DRAW LAW THIS PROJECT HAS PRODUCED, AND IT IS ABOUT
CODE THAT IS PROVABLY IDENTICAL ON EVERY PATH: the same comparison reads +5.6 pp on one
fixture and −2.0 pp on another.** Each is inside its own naive interval (±10.3 pp at n=180,
±6.5 pp at n=450), so neither is an anomaly — but a report that had run only the n=180 battery
would have banked "the flag-off beats the parent by 5.6 points", and one that had run only the
headline would have banked the opposite. **Pooled at n=630 each the master flag reproduces the
parent to 0.16 pp.**

---

## GATED CONTROL — archipelago vs `_v468kladturbo`, pooled n=72 (two draws of 36)

archipelago's board signature `(26, 26, (5, 5), (19, 19))` is in `FS_MAP_SKIP`, so `_fs_gate`
refuses. Both v517 changes are siege-path and the whole v517 channel write sits INSIDE the
`_fs_map_gated` test that v516 factored out for exactly this reason, so all of it is
structurally unreachable here.

| draw | v517 | v517 flag-off | v516 parent |
|---|---|---|---|
| seeds 1-18 | 23/36 (63.9%) | 26/36 (72.2%) | 25/36 (69.4%) |
| seeds 19-36 | 29/36 (80.6%) | 26/36 (72.2%) | 27/36 (75.0%) |
| **pooled n=72** | **52/72 (72.2%)** | **52/72 (72.2%)** | **52/72 (72.2%)** |

**ALL THREE ARMS LAND ON EXACTLY 52/72.** k≤300 pooled: 35 / 39 / 40; median kill 192 / 181 /
200; 0 tracebacks. **No alarm.** And v516's own gated bar was 72.2% on this board, which all
three reproduce.

⚠ **The two-draw design was necessary and this leg proves it again: draw 1 alone reads
23/36 for v517 against the parent's 25/36 and would have been reported as a soft alarm; draw 2
reads 29/36 against 27/36 and would have been reported as a gain.** Same-config swings of
23→29 (v517) and 25→27 (parent) on 36 games.

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The verdict's ONE WRITER is elected by VISION, not by a published lowest id.** The mandate
   said *"if two sentinels exist, lowest-id-alive publishes"*. An id field does not fit: finding
   0 caps a slot at 32 bits and v516 had already committed 21 of them. What ships is a real
   lowest-id election wherever it is observable — a sentinel that can SEE a friendly forward
   sentinel with a lower id defers — with the SENTBEAT fallback the mandate told me to reuse:
   where the pair cannot see each other both publish, and both are reading the SAME enemy core
   HP, so the collision is between two honest values and the only consumer reads one bit of it.
2. **`FS_V517_TWINBANK` (change 2b) was added, and it is not in the mandate.** Finding 1: without
   it the plank saves ammunition and funds nothing. Sub-flagged and mutant-driven like the rest.
3. **The hold is scoped to the CORE shot, not to firing.** Suppressing every shot would also
   suppress fire at the HEALER, which is the one target 18 damage is unambiguously well spent on
   in a heal-matched state (a builder is 40 HP, so two shots remove one). The measured defect is
   ammunition poured into a 100.0% heal-back **on the core**; that is exactly what is skipped.
4. **`FS_V517_HOLD_TTL` re-probe added.** A held sentinel deals no damage, so its own window can
   never improve — an unqualified hold is ABSORBING and a defender who dies or stops healing
   would never be noticed. The cost is W shots per TTL (40 ammo / 24 rounds) against ~8 shots
   per 24 rounds unheld, i.e. a ~50% ammo cut in the held state rather than a shutdown.
5. **`FS_V517_FIREDISC` rides `FS_V516_GLOBALSENT`'s write.** The channel is packed into the same
   slot and written in the same call, so FIREDISC is only reachable while GLOBALSENT is True.
   Both ship True and the v517 mutant sits inside that block; documented rather than hidden.
6. **Mechanism arms are n=30, not ~15** — `run_grid` emits 5 maps × 3 seeds × 2 seats and a local
   game is ~2 s, so the extra 15 are free.
7. **Headline is THREE concurrent arms (v517 / v516 parent / v517 flag-off), not two.** The v516
   gated leg's false alarm was settled only by a same-config arm; carrying one in the headline
   costs one third of the machine and buys the draw control everywhere.

## SURPRISES (written down before being explained away)

1. **⛔ A 4-BIT MOD-15 STAMP PRODUCED A PERIODIC GHOST, AND THE REACHABILITY INSTRUMENT CAUGHT
   IT.** The first smoke grid emitted `TWINGATE517` in runs of FOUR spaced EXACTLY FIFTEEN
   ROUNDS APART (r110-113, r125-128, r140-143, r155-158, r170…) long after the sentinel that
   wrote the verdict had died — a stamp nobody rewrites reads age 0,1,2,3 once per wrap, for
   ever. Also visible as `live 0` on a line that claims a live hold. **Fixed by gating both
   mod-15 readers on v516's EXACT `beat1` field, and by having the publisher CLEAR the peer
   field when it sees nobody.** The general lesson is bigger than this plank: **a compressed
   wrapping clock has no "never" state after its first write, so it must always be paired with
   an exact liveness field.**
2. **The mandate's own falsifier for the twin was false** (finding 2): the parent is not at
   zero concurrent core-hitting sentinels.
3. **The funding premise was false** (finding 1): a hold does not accumulate a bank, because the
   Core converts the surplus to ammunition and other turrets burn it.
4. **Nothing in 120 mech games bought a sentinel under a hold** (change 2 (b)) — the relaxed
   gates were never the binding constraint; reachability and price are.
5. **⛔⛔ THE FLAG-OFF vs PARENT DELTA FLIPS SIGN BETWEEN TWO FIXTURES OF PROVABLY IDENTICAL
   CODE** (+5.6 pp at n=180, −2.0 pp at n=450, +0.16 pp pooled at n=630). Nobody predicted a
   sign flip on a null comparison; it is the cleanest available demonstration that a single
   local fixture under n≈500 cannot settle a delta of this size, and it should be cited the
   next time a plank is banked or killed on one battery.
6. **`sent → funded` IS ZERO IN ALL THREE ARMS** (phase budget). The magazine gap that v516
   was built to close is, replay-side, no longer a phase of the rush at all — the turret can
   shoot the round it exists, in the median game. That is a stronger confirmation of v516 than
   v516's own report had, and it also means the ammunition path has nothing left to give.
7. **`arrive → sent` is 81 rounds and IDENTICAL in all three arms.** A body is at their ring at
   r8 and the first forward sentinel does not exist until r88 — 45% of the r180 target spent
   before the weapon exists, untouched by anything in v516 or v517.

## OPEN ITEMS

0. **⭐ THE `KILL_TARGET` ITEM, AND THE PHASE BUDGET NAMES IT: the 81-round `arrive → sent`
   gap.** It is identical in all three arms (v517, v516, flag-off), it is 45% of the r180
   target, and it is the only phase in the rush that no shipped plank has moved. `sent →
   funded` is 0, so the ammunition path is exhausted; `funded → kill` (87-101) is the other
   half and is a heal-economics problem the fire discipline only dents. **Candidate roots,
   both already named by prior work and neither tested against the clock: the v515 gate
   disjunction (`salt-complete OR (conn2 AND round >= FS_SENT_RND_FLOOR)`, and
   `FS_SENT_RND_FLOOR = 60` is UNSWEPT — it is a hard floor sitting three quarters of the way
   through this gap), and the purchase-reach defect (autopsy #2 / v516 change 3, mechanism
   live, currency null).** A leg that reads the arrive→sent distribution against
   `FS_SENT_RND_FLOOR` is cheap and has not been run.
1. **The twin's real blocker is the RAIDER'S LIFE, not the turret's price.** `_fs_try_sentinel`
   can only be called by a living body at the ring. Every purchase-side plank in this line
   inherits that ceiling, and v516's SENTREACH null has the same root. A purchase path that does
   not require a raider (Core-side? a surviving sentinel cannot build) is the unexplored branch.
2. **`FS_V517_TWINBANK` stops only ONE consumer.** The eco and the collar keep spending while it
   banks. A hold-state spending freeze is the natural next lever and it collides with the
   harvester doctrine and with `E1_AMMO_FLOOR` — **flagged, not resolved.**
3. **`FS_V517_NET_W`, `FS_V517_NET_EPS`, `FS_V517_HOLD_TTL` and `FS_V517_BANK_TTL` are UNSWEPT.**
   W=4/EPS=2 were sized off the autopsy's exact-100.0% signature, not tuned. The hold rate that
   results (264-493 rounds per 30 games) is a consequence, not a target.
4. **The mid-round sampling seam** (verification 1b) costs ~25% of the join. If a future plank
   needs the net figure to be exact rather than directional, the sample has to be taken at a
   fixed point in the turn on both sides.
5. **Store-width finding 0 is a repo-wide audit item**, not a v517 item: any `write_store` of a
   signed quantity anywhere in the tree is one negative value from a permanent unit death.
6. Inherited and untouched: the v516 open items (chassis home-launcher purchase path,
   `FS_V516_HOLD_GENERAL` not inert, SENTREACH unmeasured, sentinel priced by live builder bots)
   and everything under them.

## ARTIFACTS

`scratchpad/s51_v517_build/` — `arms/` (4 mutant arms + `flagoff` + a frozen `parent516` copy),
`mech/` (4 arms × replays + logs + per-arm sentrace tapes), `grid/` (15 headline blocks × 3
arms), `gated/` (two draws × 3 arms), `fo/` (6 flag-off blocks × 2 arms),
`probe_store/` (the store-width probe tree and its tape), `smokegrid/` (the 30-game grid that
produced findings 1 and surprise 1).

**Instruments, each guarded both ways:** `sentrace.py` (synthetic concurrency controls + a
real-data core-HP identity guard, **mutation-tested: zeroing the heal column drives it from
30/30 to 16/30, so it has been seen to produce the other verdict**), `phase.py` (synthetic
empty/known/ordering guards + a real-data kill-mark cross-check against the grid TSV, 0 alarms
in 1,350 games at a single consistent indexing offset), `netjoin.py` (five-offset profile plus
a cross-arm negative control that collapses 0.658 → 0.025), `flagoff_ast.py` (three synthetic
controls plus the known-real FERRY_HOME_ON positive control), `summarise.py` (`--selftest`
asserts all-win / all-loss / mixed tapes separate on every column).

**Other:** `logagg.py`, `agg_sent.py`, `headline.py`, `mkarm.sh`, `run_grid.py`, four drivers
(`drive_mech.sh`, `drive_headline.sh`, `drive_gated.sh`, `drive_flagoff.sh`),
`PARENT_FREEZE.md5`, `TREE_FINAL.md5`, `PIDS`. Parent md5s re-verified untouched after the
final leg.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* v517 FIRED: NULL on wins (54.2 vs parent 55.1, inside interval) and OFF-TARGET on
  KILL_TARGET (median kill 262 vs the r180 goal — holds trade time for efficiency, backwards
  under the ratified target). NOT the next carrier as delivered.
* What survives: FIREDISC's efficiency is real (+51% net/shot, heal-back 0.716→0.571,
  +25 kills / −29 r1000s — programme-positive under R1000_IS_DEFEAT) and the TWIN's funding
  blockers are now measured (Core converts hold-savings to ammo above ti_floor; ammo≥150
  hold-back gate unreachable; raider-at-ring-during-hold rare). The doctrine tension
  (late kills: R1000_IS_DEFEAT values, KILL_TARGET does not) is REAL and recurring — flagged
  to Magnus twice now.
* ⭐ THE DECISIVE FINDING IS THE PHASE BUDGET: spawn→arrive 8 · **arrive→sentinel 81 (45% of
  the whole r180 budget, IDENTICAL in all three arms, untouched by any shipped plank)** ·
  sent→funded 0 (v516 confirmed replay-side) · funded→kill 87-101. Kills-by-r200 is flat
  ~16-19% in every arm ever measured — no build has moved it because none has attacked the
  81-round gap. FS_SENT_RND_FLOOR=60 sits unswept three-quarters through it.
* v518 = the gap: floor sweep {40,50,60} × arrival-path turret purchase, + the twin-reserve
  fix (hold state reserves Ti for sentinel #2 instead of converting to ammo — the flagged
  E1_AMMO_FLOOR collision handled as a bounded reserve, not a freeze). FIREDISC ships ON in
  v518 with a bounded hold (TTL) pending Magnus on the late-kill tension.
* Correction to FINDING 0: the 32-bit-unsigned store slot is NOT novel — engine-probed s50
  (BUILD-REPORT-v513siegecrew, probe_store; negative writes raise). The re-derivation
  happened because the s50 "ROUTE TO ATLAS at wrap" was never discharged — that routing debt
  is now real cost, twice probed; atlas routing added to the wrap list.
