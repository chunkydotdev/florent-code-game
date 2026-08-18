# BUILD REPORT (DRAFT) — `bots/_v520pincer` (the pincer), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v519cripple` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v520_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2`. Master
`LOKI_FS_V520`; False reproduces the parent (AST-scanned and byte-proved below). Scratch:
`scratchpad/s51_v520_build/`. PAR=4 on single-arm legs; the headline runs 3 arms × PAR 2 = 6
concurrent games. Recorded PIDs in `scratchpad/s51_v520_build/PIDS`. `scratchpad/overnight*`
and corefill untouched.*

*Diff vs parent: `doctrine.py` +254/−0, `siege.py` +619/−24, `main.py` +115/−6,
`raid.py` +14/−2, **`eco.py` BYTE-IDENTICAL (0/0)**. **6,708 games with a result row across
every leg; 0 tracebacks, 0 no-winners** (counted off the leg TSVs by header match, not by
directory). Parent freeze re-verified byte-for-byte at the end of the build. ⛔ Timeouts are NOT
reported — v518 finding 0 proved the local timeout column is a constant that cannot fire.*

## ⭐⭐⭐ THE ONE-PARAGRAPH READ

**v520 FIRED beats its parent by +6.20 pp game share, +10.47 pp on `KILL_TARGET`'s tracked
metric (k≤r200: 17.7% → 28.1%) and +9.19 pp on k≤r300, at n=1,404/arm, with a byte-identical
known-zero arm in the same blocks reading −0.43 / +0.07 / +1.64 pp.** Median kill 254 → 203;
`funded→kill` 91 → 71 rounds; our core destroyed 546 → 447. **The single-flag isolation says
the whole of it is CHANGE 1: `iPIN` alone reads +7.05 / +11.32 / +8.97 pp, while PRESENCE
(−2.56 pp wins) and GUNNEAR (−0.85 pp wins) are nulls.** The mechanism is measured, not
inferred: both riders land in the ring on opposite arcs (43/43 in-ring, gap 1), the seal rate
RISES in the two-body half of v520's games while it FALLS in both control arms', simultaneous
collar closure goes 31.7% → 43.9%, and NOBODY — v518's open item 1 — is cut 43% relative.
**And the failure reel returns the finding that reframes the plank: 0 of 119 enemy-core heal
rounds fell in a fully-sealed round, and one game held a genuine 43-round closure DISJOINT from
its own turret's life. Cumulative seals are not the currency; simultaneity × overlap with the
shot is.**

⚠ **THE ~4.7–5.6 pp SAME-CONFIG FALSE-POSITIVE FLOOR (v519 open item 2, measured three ways on
this exact grid) IS CARRIED BESIDE EVERY HEADLINE CLAIM BELOW.** This build's answer to it is
not an interval — it is a **KNOWN-ZERO ARM IN THE SAME BLOCKS**: `flagoff`
(`LOKI_FS_V520 = False`), proved byte-identical to the parent on 12 of 12 games with a
negative AND a positive control. Every contrast is reported twice: treatment-vs-parent, and
the known-zero-vs-parent that prices the fixture underneath it.

---

## WHAT WAS BUILT

**CHANGE 1 — THE PINCER (`FS_V520_PINCER`).** Magnus, ~09:2xZ, verbatim intent: two raiders,
*"one to the BACK one to the FRONT of the enemy core, so they can barrier from different
sides"*. Six parts:
* **the crew comes ON**, through a run-time read (`fs_crew_on()`), never a module-level
  reassignment — see the derived-default section;
* **the relay** (v514 change D, previously inert because `FS_CREW_ON` shipped False) now
  actually carries two riders on ONE chain;
* **the terminal split**: the last launcher throws rider 1 to the BACK arc and rider 2 to the
  FRONT arc, both before teardown (Magnus's relay rule);
* **the terminal launcher's tile is a CHOSEN site** (Magnus's mid-build refinement):
  (a) both arcs inside its d²≤26 throw envelope, then (b) heal seats inside its d²≤2 pickup
  envelope, then (c) the parent's distance key — (a) wins conflicts, and the conflict rate is
  reported;
* **arc-split sealing**: both bodies run the SEALER ladder and each takes its own arc's seats
  FIRST (not ONLY), published one-writer-per-body on the beat channel;
* **the dual-appointment race fixed** at the appointment layer (claim-and-readback).

**CHANGE 2 — PRESENCE (`FS_V520_PRESENCE`).** v518's twin reserve generalised: while a ring
seat reads dead **and has previously reported**, the Core raises its `convert_ammo` titanium
floor by a replacement body's own bar (builder + one ferry launcher + margin), capped and
TTL'd; and the spawn-budget door — which was reading the broken shared beat — is moved onto
the dedicated crew bits.

**CHANGE 3 — ANNULUS FLOOR (`FS_V520_GUNNEAR`).** v519's priced road: the beltbreak plant
floor d²20→8, **for the GUNFIRST call sites only** (`dsq_lo` keyword; the chassis raid
doctrine's own call site is untouched).

---

## ⭐⭐ CENTREPIECE — THE `KILL_TARGET` PANEL, n=1,404/arm, THREE ARMS CONCURRENT PER BLOCK

**39 blocks × 36 games**, 6 maps (the standard 5-map siege grid **plus yulerune**, the second
registered cripple cell, carried forward from v519's headline) × 3 seeds × 2 seats, vs
`bots/_v488beltbreak2`. All three arms run **inside the same block on the same seeds**
(`--seed` does not pin a game, v515 finding 1). A block counts only when **all three** arms
finished all 36 games.

| | **parent (`_v519cripple`)** | **v520 FIRED** | **flagoff — KNOWN-ZERO** |
|---|---|---|---|
| WINS | 809/1404 (57.6%) | **896/1404 (63.8%)** | 803/1404 (57.2%) |
| ≤r150 | 69 (0.049) | **264 (0.188)** | 75 (0.053) |
| **≤r180 (`KILL_TARGET` median mark)** | 168 (0.120) | **356 (0.254)** | 176 (0.125) |
| **≤r200 (TRACKED METRIC)** | 248 (0.177) | **395 (0.281)** | 249 (0.177) |
| ≤r250 | 349 (0.249) | **503 (0.358)** | 376 (0.268) |
| **≤r300 (ITT primary, `DEFENCE_ADMISSION_BAR`)** | 433 (0.308) | **562 (0.400)** | 456 (0.325) |
| **median kill round** | 254 | **203** | 245 |
| our core destroyed | 546 | **447** | 543 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v520 FIRED vs parent** | **+6.20 pp** (hw 3.61) **OUTSIDE** | **+10.47 pp** (hw 3.11) **OUTSIDE** | **+9.19 pp** (hw 3.54) **OUTSIDE** |
| **flagoff vs parent** *(byte-identical play)* | **−0.43 pp** (hw 3.66) inside | **+0.07 pp** (hw 2.82) inside | **+1.64 pp** (hw 3.44) inside |

⭐⭐ **READ THE SECOND ROW FIRST, BECAUSE IT IS THE THING v519 COULD NOT DO.** v519's known-zero
arm cleared its own interval at +4.70 pp on the tracked metric and forced the ~5 pp floor
caveat onto every claim in that report. **Here the known-zero arm — proved byte-identical on 12
of 12 replays — reads −0.43 / +0.07 / +1.64 pp at n=1,404/arm.** The false-positive floor did
not fire on this grid at this n, and the treatment's +10.47 pp on the tracked metric therefore
does not need to be discounted against it. ⚠ **That is a property of THIS grid at THIS n, not a
retraction of the floor**: the floor was measured at n=468-810 and this leg is ~3× that. Any
future claim at n≈450 still needs its own control arm.

### PER MAP — wins/234 [k≤300] {k≤200}

| map | parent519 | **v520 FIRED** | flagoff |
|---|---|---|---|
| atoll | 92 [30] {20} | **121 [73] {45}** | 98 [43] {24} |
| **drakkarfjord** | 148 [84] {62} | **214 [165] {154}** | 156 [96] {77} |
| glacierkeep | 191 [117] {72} | 185 [**137**] {**106**} | 197 [121] {60} |
| midgard ⚠ | 119 [68] {28} | 120 [55] {22} | 132 [79] {35} |
| nordkap | 154 [76] {45} | 157 [80] {50} | 126 [65] {35} |
| yulerune ⚠ | 105 [58] {21} | 99 [52] {18} | 94 [52] {18} |

⭐ **drakkarfjord is the map the DOUBLEFERRY probe named**: its as-built crew put body 2 at the
ring at **r197** (the lost-update defect) against a mechanical floor of r13. With the relay
carrying two riders on one chain it goes **148 → 214 wins and k≤200 62 → 154** — the single
largest map cell this line has moved.

⚠ **midgard and yulerune are the two `FS_V519_CRIPPLE_MAPS`, where MODESWITCH stands the whole
ferry-siege plank down — so v520's changes barely execute there and those two cells are an
INTERNAL CONTROL.** They read 119→120 and 105→99: flat and slightly negative. **That is the
right shape** (a change that acts only where the plank runs should move only those cells), and
it is also the honest place to note that the flagoff arm beat both on midgard (132) — a
one-draw cell difference, not a finding.

⚠ **glacierkeep LOSES 6 wins while gaining 20 k≤300 and 34 k≤200.** Under `KILL_TARGET` that is
the trade the programme asks for; under `WIN_RATE_IS_VERDICT: yes` it is a cost. It is one map
cell and is not a conclusion on its own.

### THE PHASE BUDGET — `phase.py`, replay-side, n=1,404/arm

Kill mark cross-checked against the grid TSV in all 4,212 games: **2 alarms in 4,212 (both in
the parent/flagoff arms, 0 in v520), and the `tsv_turn − walker_round` histogram is the single
value {1: …} in every arm.**

| arm | med ARRIVE | med SENT | med FUNDED | med KILL | arrive→sent | sent→funded | **funded→kill** | games w/ fwd sentinel |
|---|---|---|---|---|---|---|---|---|
| parent519 | 10.0 | 112.0 | 112 | 253 | 99.0 | **0** | **91.0** | 976/1404 |
| **v520 FIRED** | **14.0** ⛔ | **89** | 92.0 | **202.0** | **76** | **0.0** | **71** | **1069/1404** |
| flagoff *(known-zero)* | 10 | 112 | 112 | 244.0 | 92 | 0 | 88 | 943/1404 |

⭐ **`funded → kill` — the quantity v518 named as the binding constraint and v519 moved for the
first time (101.5 → 92) — moves again: 91 → 71 rounds (−22%), against a known-zero control at
88.** And the forward sentinel now lands at r89 instead of r112, in 1,069 of 1,404 games
instead of 976.

⛔ **THE COST IS ON THE FIRST ROW AND IT IS FOUR ROUNDS: median ARRIVE 10 → 14.** The lead body
waits for its crew mate before buying the first ferry link. **The build buys 23 rounds off SENT
and 20 off `funded→kill` with 4 rounds of arrival, and the arrival cost is real, not
rounding.**

---

## PER-CHANGE VERIFICATION — mechanism arms, zero-vs-nonzero

**8 arms × 36 games (6 maps × 3 seeds × 2 seats), every instrument ON, vs `_v488beltbreak2`.**
⛔ The win column of a mechanism arm is not read.

| arm | SPLIT | TERM | ARC claims | **ARC DUP** | PRES rounds | PLANT | body-2 arrivals |
|---|---|---|---|---|---|---|---|
| `mF` all on | 43 | 24 | 60 | **0** | 222 | 7 | 24/36, gap 1 |
| `mP` PINCER off | **0** | **0** | **0** | 0 | 258 | 3 | **0** (one body) |
| `mR` PRESENCE off | 45 | 27 | 58 | 0 | **0** | 7 | 24, gap 1 |
| `mG` GUNNEAR off | 45 | 21 | 49 | 0 | 208 | 9 | 24, gap 1 |
| `mS` SPLIT off | **0** | 32 | 67 | 0 | 171 | 8 | 24, gap 1 |
| `mT` TERMSITE off | 49 | **0** | 60 | 0 | 210 | 7 | 24, gap 1 |
| `mA` ARC_SEAL off | 43 | 36 | 71 | 0 | 304 | 7 | 24, gap 1 |
| `mOff` master off | 0 ⚠ | 0 ⚠ | 0 ⚠ | 0 ⚠ | 0 ⚠ | 0 ⚠ | 0 |

⚠ `mOff`'s instrument columns are **empty BY CONSTRUCTION** (the logs are gated on the master
flag) and are therefore VOID, not zero — the same caveat v518 and v519 recorded for their own
`mOff`. Only its behaviour is comparable. **Every other sub-flag drives its own instrument to
exactly zero and leaves the others standing**, which is the zero-vs-nonzero requirement met
per change rather than per build.

### 1(a) THE SPLIT DELIVERS, AND THE WALK IS MEASURED RATHER THAN ASSUMED

`mF`, 43 split throws: **arcs used {FRONT, BACK}, median landing d²=1 (i.e. ON a heal seat),
43 of 43 landings INSIDE the ring (d²≤8), median walk remainder 1, walk == 0 in 21 of 43.**

⭐ **The far arc is not the problem the design feared.** The mandate anticipated a 4-6-tile
core+ring span against a 5.1-tile envelope and asked for the walk to be measured where the far
arc is unreachable. Measured: **the far arc was reachable from the terminal launcher in every
throw taken** (`_v520_arcs_reachable` median 2 of 2 across 24 sitings), and the residual walk
is one tile or none.

**ARRIVALS** (`FS ARRIVE`, engine coordinates, both bodies):

| arm | body-1 median | body-2 median | gap median | gap ≤ 1 |
|---|---|---|---|---|
| `mF` (pincer) | **13** | **14** | **1** | 19/24 |
| `mG` | 13 | 14 | 1 | **24/24** |
| `mP` (one body) | **9** | — | — | — |
| `mOff` | 9 | — | — | — |

⛔ **THE COST IS REAL AND IT IS FOUR ROUNDS: the LEAD arrives at r13-14 with the crew on
against r9 with one body.** That is the muster (the lead waits for body 2 before buying the
first link, `FS_MUSTER_WAIT`). The probe's gap-1 relay result reproduces exactly (gap 1 in
19-24 of 24), so the second body is free once the first has paid for the muster.

### 1(b) ⛔⛔ THE TERMINAL-LAUNCHER SITING: OBJECTIVE (a) IS MET 24/24, OBJECTIVE (b) HAS A DOSE OF ~0 — AND THE REASON IS GEOMETRY, NOT SCORING

Magnus's refinement asked for the terminal launcher's tile to be chosen for (a) both arcs in
the throw envelope and (b) maximum heal-seat coverage in the pickup envelope, with (a) winning
conflicts and the conflict rate reported per map. All three were built. The measurement:

| | `mF` | `mR` | `mG` | `mA` |
|---|---|---|---|---|
| terminal sitings | 24 | 27 | 21 | 36 |
| **median arcs reachable** | **2** | **2** | **2** | **2** |
| **median seat coverage** | **0** | **0** | **0** | **0** |
| coverage ≥ 1 | 1/24 | 2/27 | 2/21 | 4/36 |
| coverage ≥ 2 | 0/24 | 0/27 | 0/21 | 0/36 |
| **(a)-vs-(b) conflicts** | **0** | **0** | **0** | **0** |

**THE CONFLICT RATE IS ZERO ON EVERY MAP, AND THAT IS NOT GOOD NEWS — IT IS THE SIGNATURE OF
AN EMPTY CHOICE SET.** The full siting tape (`grep TERM520`, `mF`):

| chosen tile d² to their core | sitings | legal candidates | coverage |
|---|---|---|---|
| 10 | 8 | **1** | 0 |
| 25 | 7 | 2 | 0 |
| 17 | 3 | **1** | 0 |
| 9 | 3 | 1-2 | 0 |
| 32 | 2 | **1** | 0 |
| **5** | 1 | 1 | **1** |

**TWO FACTS DECIDE IT, both arithmetic:**
1. **The choice set is a SINGLETON in 17 of 24 sitings.** A ferry body has ≤4 cardinal
   neighbours; the forward-progress filter (`d ≤ here`, never a launcher pointing home) plus
   `can_build_launcher` leaves one.
2. **A heal seat is at dsq_core = 1, so a tile whose d²≤2 pickup envelope touches one is at
   dsq_core ≤ 5.** The terminal link is bought from a body standing at dsq_core 9-32 — 3 to 6
   tiles out — because *the split throw is what covers the last stretch*. The one siting that
   landed at dsq_core 5 is also the one siting that scored coverage 1.

⇒ **The two objectives are not in tension on this chain; (b) is simply out of reach at the
tile where the terminal link is bought.** The coverage job belongs structurally to the
EVICTOR — the launcher a body buys once it is already at the ring, which v515's `FS_V515_REACH`
already sites for max coverage — and v514's `FS_EVICT_ROLED_ONLY` already stops a 0-coverage
ferry terminus from squatting the evictor slot. **The `FS_V520_TERM_NOTEAR` exemption is
therefore inert in ~96% of cases and correctly so:** a launcher covering nothing SHOULD tear
down, because it holds +10% of the one global additive scale for the rest of the match.

### 1(c) THE ARC CHANNEL — AND ITS ALARM DRIVEN TO THE OTHER VERDICT

`ARC_DUP` is the alarm: rounds in which a LIVE peer publishes MY arc after both claims have
settled, i.e. two bodies working one half. **It reads 0 in every shipped arm (mF/mR/mG/mS/mT/mA,
288 games).** That zero means nothing until the counter has been made to fire, so it was:

| arm | arc claims | claim-time collisions RESOLVED | **ARC_DUP** |
|---|---|---|---|
| shipped (`mF`) | 60 | 11 | **0** |
| `pDUP` — deconfliction disabled (`FS_V520_PROBE_NO_DECONFLICT`), 8 games | 18 | 0 | **506** |

⛔ **AND THE FIRST BUILD OF THIS FUNCTION FAILED THIS TEST, WHICH IS WHY IT IS IN THE TREE
THIS WAY.** The claim was originally re-derived from the body's position every round; the
first nordkap smoke read **11 collisions in one game with both bodies flipping arc as they
walked round the collar** — the two halves swapping owners mid-seal. *An assignment that
changes when you step is not an assignment.* The claim is now made ONCE, on arrival, and held.

### 1(d) THE DUAL-APPOINTMENT RACE — the crewconv flag, fixed and DRIVEN BOTH WAYS

The crewconv screen flagged it in 1 of 3 mechanism games: two live units both holding
`fs_body == 2`, both writing `FS_SUPP_SLOT`, the buffered store silently keeping the higher
entity id — the r197 class one level up, at the APPOINTMENT layer that v514's one-writer-per-
slot fix does not reach. The fix is claim-and-readback (claim only a FREE slot; verify next
turn; the loser leaves the plank rather than re-deriving `fs_body`, which would clobber the
SEALER's slot instead).

**Positive control `FS_V520_PROBE_DUAL_APPT`** forces a second opening seat to claim SUPPORT
in the same round, 8 games each:

| arm | APPT CLAIM | APPT BUSY | games with TWO live `fs_body == 2` ids |
|---|---|---|---|
| guard **ON** | 8 | **8** | **0 / 8** |
| guard **OFF** | — | — | **1 / 8** ⛔ (the crewconv defect, reproduced on demand) |

⇒ **the guard produces both verdicts, and it works by PREVENTION (8 BUSY refusals) rather than
by arbitration — the YIELD readback never had to fire.** In the shipped arms the race did not
occur naturally at all (0 BUSY, 0 YIELD in 288 games), which is worth stating plainly: **the
counter is armed and proven able to fire; on this fixture it did not.**

### 3 — GUNNEAR IS A SUBSTITUTION, NOT AN ADDITION

Plant counts look like a null (`mF` 7, `mG` 9), and the plant POSITIONS say why:

| arm | plants | body d² to their core at the plant |
|---|---|---|
| `mF` (GUNNEAR on) | 7 | **4, 9, 10, 10**, 25, 25, 25 |
| `mG` (GUNNEAR off) | 9 | 16, 16, 16, 16, 17, 17, 17, 64 |
| `mP` (one body, GUNNEAR on) | 3 | **4, 5, 10** |
| `mS` | 8 | **4, 5, 10, 10**, 16, 17, 20, 25 |

⭐ **The lowered floor produces a plant population the parent floor cannot: bodies at d² 4-10,
which is the `pBAND` probe's own d²=4-13 signature.** With the floor at 20 those plants are
illegal and the body plants later from d² 16-17 instead. **`FS_V519_GF_MAX_PLANTS = 1` per body
is what turns that into a substitution rather than an addition** — a body that plants near at
r9 cannot plant far at r16. ⇒ **change 3 moves the shredder NEARER, not MORE.** Its outcome
price is the isolation grid's job, below.

⭐ And the crew itself roughly **triples the plant count** (`mP` 3 → `mF` 7, `mG` 9): two
bodies crossing the annulus see twice the belt. That is a change-1 effect showing up in
change 3's instrument, and the isolation arms are what separate them.

---

## FLAG-OFF AUDIT

**Structural.** 21 guard expressions read `LOKI_FS_V520` (or `_v520_on()`, which is one
expression in one place) at RUN time: `main.py` 856 / 926 / 1235 / 1268 / 1283, `siege.py` 118
/ 247 / 799 / 949 / 963 / 1221 / 1356 / 1454 / 1463 / 1619 / 1713 / 1907 / 4441 / 4596 / 4713 /
4805. `raid.py`'s only change is a `dsq_lo=None` keyword whose default is the parent path.
`eco.py` is byte-identical.

**Three additions are NOT individually guarded, and each is disclosed rather than argued away:**
1. the `v520_*` state fields in `__init__` (written unconditionally, read only under a guard —
   the pattern v518/v519 used);
2. `_fs_state_at`'s new `& FS_RID_FIELD_MASK` on the rid read. Provably inert with the plank
   off (the rid is already WRITTEN `& 0xFFFF` and nothing else writes above bit 29), and the
   byte-identity test below covers it empirically;
3. `_fs_ferry_launcher`'s "an in-ring launcher never picks up an already-arrived body" skip.
   Unreachable with the plank off, because an in-ring launcher never enters that function at
   all — the exemption that lets it is itself guarded.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v520 flag):

```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v520 derived defaults: 0 []
v519 derived defaults (inherited, must also be 0): 0 []
v518 derived defaults (inherited, must also be 0): 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```

⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see
the known v515 hazard in this very file before its zero for v520 is believed.

### ⭐⭐ AND THE HAZARD THAT CONTROL POINTS AT IS THE ONE THIS BUILD HAD TO WALK PAST

`FERRY_HOME_ON` (doctrine.py:3011) is a module-level derived default reading `FS_CREW_ON`, and
this build's whole first change is *turning the crew on*. `mkarm.sh` APPENDS overrides, so
flipping `FS_CREW_ON` at the definition site leaves that derivation stale and slot 10 gets TWO
writers — the r197 lost-update class, confirmed live as `COLLISION:True` at the s51 06:24Z
crewconv pre-flight. **v520 therefore never assigns `FS_CREW_ON`.** It adds `fs_crew_on()`, a
run-time read, and replaces all 20 code read sites (5 in `main.py`, 14 in `siege.py`, 1 in
`raid.py`); `_ferry_home_on()` (v516 change 1c) consults it.

**`collide.py`, the mandatory pre-flight, driven to BOTH verdicts:**

| configuration | crew | home ferry | COLLISION | |
|---|---|---|---|---|
| v520 FIRED | True | **False** | **False** | PASS |
| v520 master OFF | False | True | False | PASS |
| **KNOWN-BAD control** (crew ON at the definition site, read-site fix disabled) | True | **True** | **True** ⛔ | PASS — *the detector is proved able to see the defect it exists for* |

**Behavioural.** The `flagoff` arm is not a separate leg — it is **the third arm of the
headline grid, in the same blocks, on the same seeds**, at the same n as the treatment. Its
numbers are in the panel above and it is the report's known-zero control.

**Byte-identity.** A win-rate comparison cannot settle a null at any n this fixture can afford
(v518 finding 2 caught a 4.6 pp separation at n=810/arm on byte-identical play), so the
question was asked directly: same seeds, randomness off — **ours AND the opponent's**
(`arms/eq_opp` = `_v488beltbreak2` + `NOISE_ON = False`; v518 measured that disabling our salt
alone pins nothing) — and the replay bytes diffed. 12 games, 6 maps × 2 seats:

```
NEGATIVE CONTROL  parent vs parent (same tree, two runs) : identical 12 / differing  0
TEST              parent vs FLAG-OFF                     : identical 12 / differing  0
POSITIVE CONTROL  parent vs v520 FIRED                   : identical  0 / differing 12
```
*(Re-run on the FINAL tree after the two verification probes were added: negative control and
test still 12/12 identical, positive control 0/6 identical on the three maps re-checked. The
probes are `-1`/`False` by default and the re-run proves the additions did not disturb the
flag-off path.)*

⇒ **THE FIXTURE IS DETERMINISTIC, THE INSTRUMENT CAN TELL TWO TREES APART, AND
`LOKI_FS_V520 = False` PLAYS `bots/_v519cripple`'s 12 GAMES BYTE FOR BYTE.** v519's flag-off
audit had the negative control but not the positive one; this adds it, because "identical"
only means something once the same test has produced "different".

---

*(remaining sections filled as the legs land)*

---

## ⛔ THE ECONOMICS GUARD — every prior crew-ON measurement, stated before the verdict

The mandate required this written down first, and it is the strongest argument against this
build:

| # | arm | fixture | n/arm | result | delta |
|---|---|---|---|---|---|
| 1 | `FS_CREW_ON=True` vs `False` | v513 chassis, same seeds, 3 blocks, fired config | 90 | 35/90 (38.9%) vs 49/90 (54.4%) | **−15.6 pp** (hw ≈14.5) |
| 2 | same decision, **matched-vintage** pair (the number of record per the side-lane audit) | v513, pre-move pool | 60 | 24/60 (40.0%) vs 32/60 (53.3%) | **−13.3 pp** (hw ≈17.9) |
| 3 | `FS_CREW_DENY_SEAT=False` (mechanism acquittal) | same | 60 | indistinguishable from the full crew | fail-to-exclude, ±17.9 pp |
| 4 | `crewconv-screen` (`FS_CREW_ON`+`FS_CREW_CONVERT`) | v515 carrier, interleaved | 450 | 208/450 (46.2%) vs 235/450 (52.2%) | **−6.0 pp** (hw 6.5); k≤300 −1.1 pp (null) |
| 5 | crewconv, nordkap cell (fastest support arrival) | ~30 | ~30 | k≤300 | **+12.3 pp FOR** |
| 6 | crewconv, midgard cell (slowest) | ~30 | ~30 | wins 16.7% → 6.7% | ≈ **−10 pp AGAINST** |
| 7 | **field prior**, MULTI vs SINGLE forward body | league-wide observational, 128,362 attacking sides | — | kill share | **+6.7 pp [+5.4, +8.0]** |
| 8 | field prior, **funding sub-cut** (≤1 harvester by r100) | same | — | kill share | **−2.6 ± 4.2 (NULL)** |

**Every local crew-ON measurement this line has is NEGATIVE, from −6.0 pp (n=450) to −15.6 pp
(n=90).** The only positive is observational, and its own funding sub-cut goes null-to-negative
in exactly the starved band the v513 crew arm occupied (median collected 380).

**THE PINCER'S CASE, stated as a hypothesis rather than a defence:** rows 1-4 all measured a
crew that was *funded badly and arrived slowly*. The research amendment of 06:36Z named the
moderator — **fund-AND-fast**, not fund-then-crew — and the DOUBLEFERRY probe measured the
arrival half at gap 1 in 26 of 30 games. **v520 is the first configuration in which both hold
at once AND the second body has a paying job (its own arc).** If the composite reads negative,
the single-flag isolation below is the deliverable, not an excuse.

---

## ⭐⭐ THE PINCER'S OWN METRIC — SEAL RATE, replay-side

*(`seatrate.py`, built on `s51_closure_autopsy`'s seat-occupancy machinery with its guards
running in place — seven guards, including a mutation control, a simultaneity control, a
zero-presence control that must return `None` rather than 0, an enemy-only control, and a
real-data team-swap positive control that moved `seats_sealed / atring_rounds / seal_rate`.)*

**Seal rate = seats denied per 100 rounds of at-ring presence.** The pincer thesis is that two
bodies on opposite arcs seal the closed curve in PARALLEL; if only the body count rose and
nothing sealed faster, this number is flat and the plank is dead.

| arm | n | seats sealed | **rate** | **closure (simultaneous)** | closure (cumulative) | at-ring rounds | 2-body share |
|---|---|---|---|---|---|---|---|
| flagoff *(known-zero)* | 1404 | 6.59 | 3.76 | 30.8% | 35.9% | 251.2 | 0.527 |
| parent519 | 1404 | 6.63 | 3.66 | 31.7% | 36.3% | 265.7 | 0.534 |
| **v520 FIRED** | 1404 | **6.99** | **4.07** | **43.9%** | **49.2%** | 291.8 | **0.755** |

⭐⭐ **THE DISCRIMINATING CUT, and it is the one that separates "more bodies" from "parallel
sealing": split each arm's games at its own median two-body share, and read the seal rate in
each half.**

| arm | median 2-body share | rate, LOW half | rate, HIGH half | |
|---|---|---|---|---|
| flagoff | 0.544 | 4.14 | **3.39** | **FALLS** |
| parent519 | 0.564 | 4.02 | **3.29** | **FALLS** |
| **v520 FIRED** | **0.976** | 3.82 | **4.31** | **RISES** |

**On both control arms, having a second body at the ring MAKES SEALING SLOWER. On v520 it makes
it faster. Same tape, same instrument, opposite signs at n=1,404/arm.** That is the pincer's
mechanism claim tested directly rather than inferred from the win column: two bodies on the
parent chassis get in each other's way; two bodies with arcs do not.

⚠ Honest read of the rate itself: +0.41 seats/100 rounds over the parent, on an at-ring
denominator that grew 266 → 292. **The movement that is not small is CLOSURE: 31.7% → 43.9% of
games reach a SIMULTANEOUSLY-sealed collar, against a known-zero control at 30.8%.** ⛔ And the
failure reel says that is the metric that was ever worth buying — see below.

---

## ⭐ NOBODY — v518's open item 1, re-measured replay-side

*(`nobody.py`. ⛔ It exists because **this grid's `.err` files carry no bot tape at all** — 0
`GAP518` lines — so `gapdecomp.py` is literally not runnable on it, and an instrument that
cannot see is byte-identical to one reading 100% NOBODY. The script REFUSES to print a
stderr-side share in that case rather than print 1.0. Cross-checked against the one fixture
that still carries `GAP518` (`s51_v518_build/gapbase`, 29 games, 7,740 window rounds): stderr
0.6481 vs replay-side 0.6227, contingency `{line+body 2539, line−body 185, noline+body 381,
noline−body 4635}` — the 185 line-without-body rounds (1.5%) are gapdecomp's own documented
end-of-round seam.)*

| arm | n | window len | **NOBODY (centre)** | **NOBODY (footprint)** | ≥1 body / window | ≥2 bodies | bought a fwd sentinel |
|---|---|---|---|---|---|---|---|
| flagoff *(known-zero)* | 1367 | 230.5 | 0.3572 | 0.2278 | 0.5548 | 0.2890 | 67.1% |
| parent519 | 1368 | 224.8 | 0.3540 | 0.2214 | 0.5720 | 0.2971 | 69.5% |
| **v520 FIRED** | 1404 | **196.0** | **0.2464** | **0.1261** | **0.6548** | **0.4081** | **76.1%** |

⇒ **NOBODY falls 35.4% → 24.6% (centre convention) and 22.1% → 12.6% (footprint — a 43%
RELATIVE cut), the window itself shortens 225 → 196 rounds, two-body presence rises 29.7% →
40.8%, and the share of games that ever buy a forward sentinel rises 69.5% → 76.1%.** The
known-zero arm sits AT or ABOVE the parent on every one of those columns, so the direction is
not fixture. **This is v518's open item 1 answered: the turret gap was raider ABSENCE, and the
absence is nearly halved.**

⛔ **THESE ARE NOT COMPARABLE TO v518's 50.4% AND THE REPORT SAYS SO RATHER THAN LETTING THE
NUMBERS SIT SIDE BY SIDE.** v518's figure is a stderr-side share on a different arm, a
different chassis and the "bought a forward sentinel" cut. What is comparable is the
ARM-TO-ARM movement above, measured by one instrument on one fixture.

⚠ **AND THE INSTRUMENT WORK TURNED UP TWO REAL DEFECTS IN THE MACHINERY IT COPIED**, both
disclosed rather than silently fixed:
1. `s51_closure_autopsy/{seattape,ferry}.py` seed the Cores from replay map **field 5, which
   does not exist** (the schema says `cores = 4`). In both originals that loop NEVER FIRED, so
   the "denied by our own Core" branch was unreachable. Harmless for the 8 orthogonal heal
   seats (disjoint from the 2×2 footprint), which is why it survived. Corrected in
   `ringwalk.py` and guarded by renumbering back to 5 on a real replay; **the originals were
   not edited** (out of scope).
2. **Two ring envelopes are in use and they are not the same set.** `Tape.near_bot` (hence
   `phase.py`'s marks and `gapdecomp`'s window) tests d²≤8 to the core CENTRE = 24 tiles;
   `siege.FS_RING_DSQ = 8` tests the footprint-aware `dsq_core` = 49 tiles, and that is the
   condition the bot's own tape fires under. A first draft asserted the replay-side share was a
   lower bound on the stderr share; **the join falsified it (0.7483 vs 0.6481)** and both
   conventions are now printed with the footprint one marked comparable.

---

## ⭐⭐⭐ FAILURE REEL — and it produced the build's biggest finding

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in EACH of the six
maps, for the `v520 FIRED` arm** — from 315 our-core-deaths in 972 rows over 27 blocks. One per
map is what stops the reel being six copies of one board. Ties: lowest block → lowest seed →
seat A; no tie occurred. Decoded with the s51 autopsy machinery **copied, not rewritten**
(`turrets.py` and `tape.py` md5-identical to the v519 copies), with `seatrate.py` and
`termcov.py` imported and called so the v520 facts come off the same instruments as the panel.

**GUARDS, all N/N:** HP identity 6/6 · fireTurret core-hits == −18 `UpdateHp` counts, both
teams, 6/6 · seatrate-vs-reel seat agreement 6/6 · per-round heal == crip's independent
`oppcore_heal` 6/6 · and a negative control on the one piece of new code (`heal_rounds`):
`midgard_s54_B` reads 432 as played and **0** team-flipped — the guard can fail.

| # | game | our core dead | class |
|---|---|---|---|
| 1 | `nordkap_s72_B` | r101 | NO_TURRET |
| 2 | `yulerune_s14_A` | r124 | NO_TURRET |
| 3 | `midgard_s54_B` | r145 | HEAL_OUTRUN |
| 4 | `atoll_s77_A` | r149 | NO_TURRET |
| 5 | `drakkarfjord_s17_A` | r217 | HEAL_OUTRUN |
| 6 | `glacierkeep_s37_A` | r431 | MAG_STARVED |

**NO NEW CAUSE TOKEN** — `NO_TURRET ×3, HEAL_OUTRUN ×2, MAG_STARVED ×1`, every one already in
`corpus/failure_reel.tsv`. Six rows appended to `corpus/failure_reel.tsv` (63 → 69 lines,
append-only, readback verified: 8 fields per row, all six replay paths resolve), with the six
replays copied out of the grid blocks into `reel/replays/` so the rows cannot rot.

### ⛔⛔⛔ THE FINDING, AND IT REFRAMES THE PINCER'S OWN HEADLINE METRIC

**Across all six games, 0 of 119 enemy-core heal rounds fell in a round where all 8 heal seats
were denied.** Two boards make it unarguable:
* **`drakkarfjord_s17_A`** denied **all 8 seats by r33** (seal rate 15.4/100 at-ring, ~2.5× the
  reel median) — **but never simultaneously**; peak 7 of 8, `closure_round = −1`. Their core
  bottomed at 482, and 468 of our 486 damage was healed back over 72 heal rounds, **every one
  of them in an unsealed round**.
* **`glacierkeep_s37_A`** held a genuine **43-round full closure, r28→r71** — and the forward
  sentinel did not go up until **r76, five rounds after the seal broke**. The seal window and
  the fire window are **DISJOINT**. They healed all 216 of our damage back over r128-r164,
  *entirely after our turret was already dead*.

⇒ **CUMULATIVE SEATS SEALED IS NOT THE QUANTITY THAT STOPS A HEAL. SIMULTANEITY × OVERLAP WITH
THE SHOT IS.** The pincer moves the cumulative number (6.61 → 6.87) and the simultaneous one
(27.8% → 43.5% of games) — and this reel says the second is the one that was ever worth buying,
and that even a real closure buys nothing if it does not overlap the turret's life.
**Proposed token if the builder wants it banked: `SEAL_SHOT_DISJOINT`.** It is NOT coined here;
the narratives sit under the existing tokens with the evidence attached.

### The other four, in one line each
* **`nordkap_s72_B`** — the presence plank fully delivered and bought nothing: **≥2 bodies in
  94 of 95 at-ring rounds, max 4 simultaneous** (best in the reel), 6 of 8 seats denied by r39,
  and **zero shots on their core**. The only sentinel sat at d²=184 and fired 0 shots in 87
  rounds. **Autopsy #2: siting, not presence.**
* **`yulerune_s14_A`** — the thinnest pincer (≥2 bodies in 29 of 99 ring rounds), 4 of 8 seats
  ever denied, all by buildings and none by a body; the shredder worked (50 shots, 12 enemy
  eco buildings) and the sentinel arrived r92 in our own half.
* **`atoll_s77_A`** — ⭐ **the terminal-launcher row: FOUR launchers of ours stood within d²≤2
  of a heal seat (coverage 1-2 each, against a best-reachable ceiling of 2), union alive 130 of
  149 rounds, and (13,0) survived 119 rounds at d²=2 of the footprint. It converted nothing:
  2 attributed throws, 9 turrets bought, 0 shots on their core.** Sited right, never used —
  and presence had collapsed (9 ring rounds of 149).
* **`midgard_s54_B`** — a real forward sentinel at d²=32 landed 24 shots = 432 damage and they
  healed **432** of it (ratio 1.000). 47 heal rounds r56-r102, **none in a fully-sealed round**;
  we peaked at 6 of 8 and the sixth seat was not taken until r121, nineteen rounds after the
  last heal. No launcher of ours was ever in throw range of the healer.

---

## HEAL-BACK AND THE COLLAR — `crip.py`, replay-side, n=1,404/arm

*(Guard: the TEAM-SWAP POSITIVE CONTROL re-reads one game with `our_team` flipped and must move
the columns. It does — all seven: `heal_back` None ↔ 0.2282, `opp_harv_built` 5 ↔ 3,
`oppcore_dmg` 0 ↔ 666, plus `opp_belt_built`, `fwd_gun_n`, `fwd_laun_n`, `collar_bar_n`.
Reported over games where damage was actually landed; a 0-damage game has no defined ratio and
pooling it as 0 would read as "they healed nothing".)*

| | parent519 | **v520 FIRED** | flagoff *(known-zero)* |
|---|---|---|---|
| **median heal-back** | **0.000** | **0.000** | **0.000** |
| share of games heal-back ≥ 0.90 | 18.3% | 18.4% | 15.6% |
| **collar barriers / game** | 15.12 | **17.07** | 14.67 |
| their belts built / game | 37.31 | 29.05 | 37.69 |
| their economy destroyed by us / game | 7.25 | 5.60 | 7.15 |
| **median first forward SENTINEL round** | 166.1 | **147.8** | 168.7 |
| **median first SHREDDER round** | 64.1 | **44.6** | 62.0 |
| median game length | 403.4 | **384.4** | 393.6 |

⛔⛔ **HEAL-BACK DOES NOT MOVE, AND AT n=1,404 THE MEDIAN IS 0.000 IN ALL THREE ARMS — THE
COLUMN THIS BUILD WAS EXPECTED TO PUSH IS A NULL.** The ≥0.90 share reads 18.3 / 18.4 / 15.6 %,
i.e. the treatment is indistinguishable from the parent and slightly *worse* than the
known-zero arm. **The failure reel explains exactly why and the two findings are the same
finding: 0 of 119 enemy-core heal rounds in the reel fell in a fully-sealed round, so a plank
that seals MORE seats without making the closure overlap the turret's life cannot move
heal-back.** *(v519's dramatic 0.99 → 0.00 was a TREATED-CELL number on the two MODESWITCH maps,
not a pooled one; the pooled parent median here is already 0.000 and there is nothing left to
take.)*

⭐ **WHAT DOES MOVE IS THE COLLAR-BARRIER COLUMN — THE PINCER'S OWN SIGNATURE — AND IT CARRIES
AN INTERNAL CONTROL**: +1.95 barriers/game over the parent and +2.40 over the known-zero arm,
concentrated exactly where the plank runs —

| map | parent / **v520** / flagoff |
|---|---|
| nordkap | 15.76 / **21.91** / 14.26 |
| drakkarfjord | 19.23 / **22.79** / 19.48 |
| glacierkeep | 18.92 / **21.49** / 18.50 |
| atoll | 12.29 / 11.78 / 13.32 |
| **midgard** *(plank stood down)* | 12.60 / **12.99** / 11.29 |
| **yulerune** *(plank stood down)* | 11.94 / **11.43** / 11.18 |

**The two cripple cells, where MODESWITCH turns the whole plank off, are FLAT (±0.5). The three
maps where the ferry runs longest gain 2.5-6 barriers a game.** That is a within-report control
the win column cannot provide.

### TERMINAL-LAUNCHER COVERAGE, replay-side — and it does NOT agree with the bot-side tape, for a reason

`termcov.py` censuses **every launcher of ours ever built within d²≤26 of the enemy core**, not
just the ferry's terminal siting:

| arm | launchers | coverage {0 / 1 / 2 seats} | **coverage ≥ 1** | median lifetime | ever launched | throws |
|---|---|---|---|---|---|---|
| flagoff | 1938 | 1073 / 160 / 705 | 44.6% | 1.0 | 83.8% | 14,243 |
| parent519 | 1920 | 1171 / 223 / 526 | 39.0% | 1.0 | 87.9% | 14,305 |
| **v520 FIRED** | 1978 | 974 / 283 / **721** | **50.8%** | **4.0** | 82.2% | **19,002** |

⛔ **THIS IS NOT THE SAME POPULATION AS THE 1-IN-24 BOT-SIDE NUMBER ABOVE AND THE TWO MUST NOT
BE POOLED.** `TERM520` counts only the FERRY's terminal siting decision; `termcov` counts the
whole in-envelope launcher population, evictors included. **Both are true: the terminal ferry
launcher almost never covers a seat, and the launcher population as a whole covers more under
v520 (39.0% → 50.8%) and lives four times longer (median 1 → 4 rounds).** The lifetime column
is the `FS_V520_TERM_NOTEAR` exemption plus the evictor ladder getting more rounds, and the
throw count rises 14.3k → 19.0k.

⛔ **AND ONE CORRECTION TO THE MANDATE'S OWN CEILING FIGURE.** The closure autopsy's *"a
purpose-sited evictor could reach 4 of 8 seats"* does not hold on this envelope: `termcov`'s
counterfactual best-site column reads **2 for all 5,836 launchers in all three arms** —
consecutive heal seats are d²=1 apart along an edge and d²=2 around a corner, so **2 is the
geometric maximum** for a d²≤2 pickup envelope. A constant column validates nothing, which is
why the script prints it flagged. **Read v520's coverage against 2, not against 4** — on that
denominator 721 of 1,978 launchers (36.5%) are at the geometric ceiling.

⚠ **THE ECONOMY COLUMNS ARE CONFOUNDED BY GAME LENGTH AND MUST NOT BE READ AS ATTRITION.**
"Their belts built" falls 37.3 → 29.1 and "their economy destroyed by us" ALSO falls 7.25 →
5.60 — in a fixture whose median game is **19 rounds shorter**. We are not destroying more of
their economy; we are ending the game before they build it. Stated because the opposite reading
is the tempting one.


---

## GATED CONTROL — archipelago vs `_v468kladturbo`, pooled n=72

⛔⛔ **AND THE FIRST THING TO SAY IS THAT THIS LEG IS NOT THE NULL-BY-CONSTRUCTION LEG IT WAS
DESIGNED TO BE, AND I FOUND THAT OUT BY CHECKING RATHER THAN BY ASSERTING IT.** archipelago's
signature is in `FS_MAP_SKIP`, so `_fs_gate` refuses and the ferry, the crew appointment, the
ring turn, the split, the presence reserve and both GUNFIRST call sites are all unreachable —
**but TWO `fs_crew_on()` read sites sit OUTSIDE the map gate** (`main.py:1000`, the spawn-
purpose anchor, and `main.py:1084`, the roster line that makes `FS_CREW_SEAT` a raider instead
of an eco expander). Both are the PARENT's structure — v520 only turns the flag that reaches
them on — but the consequence is real: **on a gated board v520 still spends seat 3 as a raider
rather than on the economy.** So this leg measures that, not nothing.

| draw | v520 | parent (`_v519cripple`) |
|---|---|---|
| seeds 1-18 | 23/36 (63.9%) · k≤300 17 (47.2%) · med 195 | 19/36 (52.8%) · k≤300 9 (25.0%) · med 303 |
| seeds 19-36 | 23/36 (63.9%) · k≤300 16 (44.4%) · med 166 | 25/36 (69.4%) · k≤300 17 (47.2%) · med 152 |
| **pooled n=72** | **46/72 (63.9%)** · k≤300 33 (45.8%) · med 180 | 44/72 (61.1%) · k≤300 26 (36.1%) · med 196 |

0 tracebacks, r1000 3 vs 3.

⚠ **THE TWO DRAWS DISAGREE IN SIGN ON BOTH COLUMNS** — wins +11.1 pp then −5.5 pp, k≤300
+22.2 pp then −2.8 pp — so the pooled +2.8 / +9.7 pp is the one-draw law, not a reading. **n=72
resolves nothing here and the report does not pretend otherwise.** What the leg does establish
is the absence of an alarm: nothing catastrophic happens on a board the plank cannot play.

---

## ⭐⭐ CHANGE 2 — PRESENCE, AND THE CAP IS MET BY A MECHANISM THE MANDATE DID NOT SPECIFY

**METHOD: v513's forced-death probe, reused verbatim** (`FS_V520_PROBE_KILL_RND = 60`, never
shipped): the SEALER self-destructs at r60 with the game otherwise untouched, so latency is a
measurement rather than a wait for a natural death that lands at a different round in every arm.
4 arms × 48 games (6 maps × 4 seeds × 2 seats). **BOTH ARMS CARRY THE PROBE** — `pKoff*` is the
SAME TREE with the pincer off, i.e. one body, so the comparison is on this chassis rather than
against a quoted number. v513's own figure (10 of 14 replaced, **median 90 rounds, 0 inside the
cap**) is the historical anchor and is quoted, not re-derived.
*(Reader guard, `latread.py --selftest`: a game with a kill and no later arrival reads
NEVER-REPLACED, not 0 and not dropped — dropping it flatters the median exactly where the plank
fails.)*

### (a) THE MANDATE'S OWN METRIC — replacement latency — IS A NULL

| arm | probe fired | REPLACED | median latency | **≤15 (Magnus's cap)** | ≤30 | never replaced |
|---|---|---|---|---|---|---|
| `pKon` pincer + presence | 31 | 8/31 | 120.5 | **0/31** | 1/31 | 23 |
| `pKonP` pincer, presence OFF | 30 | 7/30 | 130 | **0/30** | 0/30 | 23 |
| `pKoff` one body, presence ON | 23 | 6/23 | 330.5 | **0/23** | 0/23 | 17 |
| `pKoffP` one body, presence OFF | 24 | 9/24 | 245 | 1/24 | 1/24 | 15 |

⛔ **THE FUNDING RESERVE MOVES REPLACEMENT LATENCY BY NOTHING: `pKon` 120.5 / 8-of-31 against
`pKonP` 130 / 7-of-30 — the presence flag on and off, same tree, same seeds.** v513 named
FUNDING as the binding constraint and this build's answer to it measures a null on the quantity
it was built for. **0 of 31 inside the 15-round cap, exactly as v513 read 0 of 14.**

### (b) ⭐⭐ BUT THE THING THE CAP WAS ABOUT — A BODY AT THE RING — IS ACHIEVED, IN SIX ROUNDS

The latency metric asks *"when does a NEW body arrive?"*. For a two-body plank that is the
wrong question, and the tape says so:

| arm | probe games | **a body reports a RING phase AFTER the kill** | `FS PROMOTE` lines |
|---|---|---|---|
| `pKon` | 31 | **22 (71.0%)** | 28 |
| `pKonP` | 30 | 17 (56.7%) | 27 |
| `pKoff` one body | 23 | **6 (26.1%)** | 0 |
| `pKoffP` one body | 24 | 9 (37.5%) | 0 |

**And the promote latency is EXACTLY 6 ROUNDS in 26 of 26 games (`pKon`) and 23 of 23
(`pKonP`)** — it is `FS_CREW_STALE`, deterministic. The support notices the sealer's beat go
stale and takes the collar over the same round, because **it is already standing there**.

⇒ **MAGNUS'S ~15-ROUND CAP IS MET — at 6 rounds, 26/26 — BY ROLE-CONVERT OF A BODY ALREADY AT
THE RING, NOT BY THE FUNDED REPLACEMENT THE MANDATE SPECIFIED.** The two halves of change 2
therefore split cleanly: **the two-body half delivers the cap and roughly doubles post-death
ring presence (26-38% → 57-71%); the funding half is a null on its own metric.** That is the
per-change attribution the mandate asked for, and it points at `FS_V520_PRESENCE` as the flag
most likely to be worth turning OFF.

---

## ⭐⭐⭐ SINGLE-FLAG ISOLATION — n=468/arm, FOUR ARMS IN THE SAME BLOCKS ON THE SAME SEEDS

**Run regardless of the composite's sign** (the mandate makes per-change attribution the
deliverable either way; running it only when the composite disappoints would be a selection
rule on the analysis). Seeds 501-539, disjoint from the headline. Each arm is the FULL tree
with exactly one change left on.

| arm | n | wins | ≤r150 | ≤r180 | **≤r200** | **≤r300** | median kill | our core dead |
|---|---|---|---|---|---|---|---|---|
| parent519 | 468 | 58.1% | 0.041 | 0.115 | 0.171 | 0.314 | 263 | 186 |
| **`iPIN` — PINCER only** | 468 | **65.2%** | **0.212** | **0.252** | **0.284** | **0.404** | **204** | **143** |
| `iPRES` — PRESENCE only | 468 | 55.6% | 0.053 | 0.122 | 0.169 | 0.310 | 246 | 182 |
| `iGUN` — GUNNEAR only | 468 | 57.3% | 0.062 | 0.147 | 0.186 | 0.321 | 236 | 187 |

| contrast vs parent | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **`iPIN`** | **+7.05 pp** (hw 6.23) **OUTSIDE** | **+11.32 pp** (hw 5.37) **OUTSIDE** | **+8.97 pp** (hw 6.15) **OUTSIDE** |
| `iPRES` | −2.56 pp (hw 6.35) inside *(under the floor)* | −0.21 pp (hw 4.81) inside | −0.43 pp (hw 5.94) inside |
| `iGUN` | −0.85 pp (hw 6.33) inside *(under the floor)* | +1.50 pp (hw 4.91) inside | +0.64 pp (hw 5.96) inside |

⭐⭐ **CHANGE 1 IS THE ENTIRE EFFECT, AND THE ARITHMETIC IS NOT SUBTLE: `iPIN` ALONE
REPRODUCES THE COMPOSITE.** Composite (n=1,404) reads +6.20 / +10.47 / +9.19 pp; `iPIN` alone
(n=468) reads +7.05 / +11.32 / +8.97 pp. **Changes 2 and 3 contribute nothing measurable on
top, and change 2's point estimate on wins is NEGATIVE (−2.56 pp).**

⚠ **AND THE HONEST QUALIFIER: this leg has no known-zero arm of its own** (the headline's
`flagoff` is the control for the fixture, on different seeds), so at n=468 — the exact n at
which v519 measured its floor — **a single-flag delta under ~6 pp is a DIRECTION, not a
separation.** Both nulls sit under it. `iPIN`'s three numbers do not.

⇒ **THE PER-CHANGE VERDICT, and it lines up with the mechanism arms rather than contradicting
them:**
* **CHANGE 1 (PINCER) — CARRIES THE BUILD.** Every mechanism instrument moves (split 43/43
  in-ring, arcs claimed with a 0 alarm, seal rate rising in the two-body half where both
  controls fall, closure 31.7% → 43.9%, NOBODY −43% relative) and the outcome moves with them.
* **CHANGE 2 (PRESENCE) — NULL, AND ITS OWN MECHANISM METRIC IS ALSO NULL.** The funding
  reserve moves replacement latency by nothing (§ change 2(a)) and the isolation arm moves the
  outcome by nothing (and negatively on wins). **The cap Magnus set is met by change 1's
  role-convert, not by this.** ⇒ this is the flag to consider shipping OFF; the decision is
  the builder's.
* **CHANGE 3 (GUNNEAR) — NULL AT THIS DOSE, AND THE DOSE IS A SUBSTITUTION.** It fires (7-9
  plants per 36 games, r7-r17, from bodies at d² 4-10 which the parent floor forbids) and it
  moves the first-shredder round 64 → 45 pooled — but the outcome columns do not move. v519's
  road is now PRICED AND MEASURED rather than priced and unmeasured: **8 plants in 8 of 30
  games was the ceiling and it buys nothing on its own.**

---

## SURPRISES (written down before being explained away)

1. **⭐⭐⭐ 0 OF 119 ENEMY-CORE HEAL ROUNDS IN THE FAILURE REEL FELL IN A FULLY-SEALED ROUND —
   AND ONE GAME HELD A REAL 43-ROUND CLOSURE THAT DID NOT OVERLAP ITS OWN TURRET'S LIFE.**
   Nobody predicted that the collar's value would turn out to be a *scheduling* property. The
   pincer was built to seal MORE seats; the reel says the currency is **simultaneity × overlap
   with the shot**, and a plank can max the first metric and buy nothing.
2. **⛔ THE FAR ARC WAS NEVER THE PROBLEM.** The design (and this mandate) budgeted for a 4-6
   tile core+ring span against a 5.1-tile throw envelope and asked for the walk remainder to be
   measured. Measured: **43 of 43 split throws landed INSIDE the ring, median landing d²=1 —
   i.e. ON a heal seat — and the median walk remainder is one tile.** Both arcs were reachable
   from the terminal launcher in every siting.
3. **⛔⛔ THE TERMINAL LAUNCHER'S TILE IS NOT A CHOICE: the legal candidate set is a SINGLETON in
   17 of 24 sitings**, and every tile it can reach sits at dsq_core 9-32 where a d²≤2 pickup
   envelope cannot touch a seat at dsq_core 1. Magnus's objective (b) has a dose of ~0 and the
   (a)-vs-(b) conflict rate is 0 **because the choice set is empty, not because the objectives
   agree**.
4. **⭐ THE FIRST ARC IMPLEMENTATION THRASHED AND THE ALARM CAUGHT IT.** Re-deriving the arc
   from the body's position every round produced 11 "collisions" in one nordkap game with the
   two bodies swapping halves as they walked. *An assignment that changes when you step is not
   an assignment.*
5. **⭐⭐ MAGNUS'S 15-ROUND CAP IS MET AT 6 ROUNDS, 26/26 — BY THE WRONG MECHANISM.** The
   funded-replacement half of change 2 is a null on its own metric (0/31 inside the cap, median
   120.5, indistinguishable from the flag being off); the cap falls out of role-convert by a
   body that is already there.
6. **THE KNOWN-ZERO ARM READS −0.43 / +0.07 / +1.64 pp at n=1,404.** v519's read +4.70 pp on the
   tracked metric at n=468 and forced a ~5 pp caveat onto every claim in that report. Nobody
   predicted the floor would simply stop firing at 3× the n.
7. **⭐⭐ THE COMPOSITE IS ONE CHANGE. `iPIN` ALONE (n=468) READS +7.05 / +11.32 / +8.97 pp
   AGAINST THE COMPOSITE'S +6.20 / +10.47 / +9.19 pp AT n=1,404.** Two of the three changes
   contribute nothing, and one of them (PRESENCE) is negative on wins. A three-change build
   that turns out to be a one-change build is the outcome the single-flag isolation exists to
   find, and it was run on a positive composite rather than a disappointing one.
8. **CHANGE 3 IS A SUBSTITUTION, NOT AN ADDITION.** Lowering the annulus floor did not raise the
   plant count (7 vs 9 with the floor at 20) — it moved the plants from bodies at d² 16-17 to
   bodies at d² 4-10, because `FS_V519_GF_MAX_PLANTS = 1` per body makes near and far
   alternatives rather than additions.
9. **THE CREW ROUGHLY TRIPLES THE SHREDDER COUNT ON ITS OWN** (`mP` 3 → `mF` 7, `mG` 9): two
   bodies crossing the annulus see twice the belt. That is change 1 showing up in change 3's
   instrument.
10. **drakkarfjord k≤200 goes 62 → 154 of 234.** The map DOUBLEFERRY named — its as-built crew
   put body 2 at the ring at r197 against a floor of r13 — is the map that moves most.
11. **⛔ THE GATED BOARD IS NOT INERT FOR THIS BUILD.** Two `fs_crew_on()` read sites live
    outside the map gate, so on archipelago v520 still spends seat 3 as a raider instead of on
    the economy. Found by checking, not by asserting; the leg's own two draws then disagreed in
    sign on both columns.

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The headline is n=1,404/arm, not n≥450.** Blocks ran at ~40 s, so the extra power was
   nearly free — and given that v519's false-positive floor was measured at n=468, buying 3×
   the n was the cheapest way to find out whether the floor was an n effect. It was.
2. **The third arm is `flagoff`, not a second dose.** With a byte-identity proof behind it,
   `flagoff` is the strongest known-zero control available and it prices the fixture in the same
   blocks — which is exactly what v519 open item 2 asked any future claim on this grid to do.
3. **The single-flag isolation ran REGARDLESS of the composite's sign.** The mandate makes it
   the deliverable either way; running it only when the composite disappoints would be a
   selection rule on the analysis.
4. **A fourth and fifth mechanism arm (`mS` SPLIT-off, `mT` TERMSITE-off, `mA` ARC_SEAL-off)
   were added** so that the three parts of change 1 are separable, not just change 1 as a whole.
5. **Replacement latency is measured with BOTH arms carrying the probe**, one of them being the
   same tree with the pincer off, rather than against v513's quoted number on a different
   chassis.
6. **The reel carries six rows, not five** — one per map on a six-map grid, matching v519's
   convention.
7. **`nobody.py` had to be written** because this grid's `.err` files carry no bot tape at all,
   so `gapdecomp.py` is not runnable on it. Cross-checked against the one fixture that still
   carries `GAP518`.
8. **Timeouts are not reported** (v518 finding 0).

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⚠⚠ MAGNUS'S PRIORITY RULING 1 vs THE NOW-LIVE RING-SIDE SHREDDER — and this is the
   collision v519 flagged twice while it cost nothing, now costing something.** Ruling 1
   (2026-08-18 ~04:02Z) orders the collar sequence **barriers → launchers → sentinels**.
   `siege.py`'s rung 1'' inserts a shredder attempt ABOVE rung 1, and v519 could report the
   collision as worth zero because the clause never fired (0 plants in 356 attempts). **Change
   3 makes it fire: 7-9 plants in 36 games, at r7-r17, from bodies standing at d² 4-10 — i.e.
   ON THE COLLAR, taking a round from the barrier ladder.** The anchor for taking it is
   Magnus's own later variant (~05:07Z, verbatim intent: *"maybe there's some scenario where we
   can cripple them hard by an early gunner … while the offensive builders go and set up
   barriers around their core after the gunner is placed"*). **It is now a live ordering
   decision and it needs one.**
2. **⚠ THE ARC SPLIT REPLACES v513's VERB SPLIT, WHICH WAS A MEASURED DESIGN.** v513 gave the
   support a DIFFERENT verb set (evictor + late sentinel + body denial, never a barrier)
   precisely so the two bodies could not compete for the same round. v520 puts both bodies on
   the SEALER ladder and relies on the arc assignment to keep them apart. The two-body seal-rate
   cut supports it (the parent's rate falls in its high-two-body half, v520's rises) — but the
   old design's rationale was never refuted, only replaced, and `FS_V520_ARC_SEAL = False`
   restores it behind a flag.
3. **⚠ `FS_V520_PRESENCE` IS THE FLAG THIS REPORT WOULD TURN OFF, AND THAT IS A DECISION, NOT A
   FINDING.** Its funding half is a null on its own metric (§ change 2(a)) and it holds
   titanium back from `convert_ammo`; its seats half (the spawn-budget door moving onto the
   dedicated crew bits) is a correctness fix for a beat that was measurably the wrong one. They
   are separable (`FS_V520_PRES_SEATS`) and the isolation grid prices them together, not apart.
4. **⚠ `R1000_IS_DEFEAT` reads FAVOURABLE and is recorded as such**: median kill 254 → 203,
   k≤300 30.8% → 40.0%, our core destroyed 546 → 447. **`DEFENCE_ADMISSION_BAR` (r300
   non-regression, ITT) passes comfortably and in the favourable direction**, so per CLAUDE.md's
   DEFF clause it is an exclusion, not a fail-to-exclude, and needs no restatement.
5. **⚠ THE `SHIP_BAR` QUESTION IS NOT ANSWERED BY THIS REPORT AND MUST NOT BE READ INTO IT.**
   `SHIP_BAR` is 70% game share **vs the PROGRAMME INCUMBENT `bots/_v488beltbreak2` on the
   standard full-pool local fixture**. This leg is a 6-map grid against that incumbent and reads
   63.8% at n=1,404 — **a 6-map grid is explicitly named a non-arming read** in `PROGRAMME.md`.
   Nothing here authorises a ship conversation.

## OPEN ITEMS

0. **⭐⭐ THE REEL'S FINDING IS THE NEXT PLANK, AND IT IS NOT MORE SEATS.** Seal SIMULTANEITY and
   its OVERLAP WITH THE TURRET'S LIFE are the quantity; `seatrate.py` already emits
   `closure_round` (simultaneous) separately from `closure_cum_round` (cumulative), and the reel
   shows the two diverge. A plank that schedules the sentinel purchase INTO a live closure
   window — rather than buying it whenever the ladder reaches rung 4 — is the shape this points
   at. **`glacierkeep_s37_A` held a 43-round closure and bought its turret 5 rounds after it
   broke.**
1. **`FS_V520_PRESENCE`'s funding half is unpriced against its cost.** It measures a null on
   latency; what it costs in withheld ammunition is not measured here.
2. **The 4-round arrival tax (`FS_MUSTER_WAIT`) is unswept.** The lead waits for its crew mate;
   median ARRIVE 10 → 14. A shorter muster, or a muster that the lead can abandon on a signal
   rather than a timer, is one constant away.
3. **The terminal launcher cannot reach a coverage tile from where the last link is bought.**
   The coverage job belongs to the EVICTOR (v515 `FS_V515_REACH`), and this build did not touch
   it. The `FS_V520_TERM_NOTEAR` exemption is inert in ~96% of cases as a result.
4. **`FS_V520_SPLIT_MAX_RND`, `FS_V520_TERM_DSQ`, `FS_V520_PRES_TTL/CAP/MAX_RNDS` and
   `FS_V520_GF_DSQ_LO` are UNSWEPT.** `FS_V520_GF_RING_ONLY` ships False and is measurable.
5. **The dual-appointment race did not occur naturally in 288 games** (0 BUSY, 0 YIELD in the
   shipped arms); the guard is proved able to fire only under the forced probe. Whether the
   crewconv screen's 1-in-3 rate was carrier-specific is unresolved.
6. **glacierkeep loses 6 wins while gaining 34 k≤200** — the `KILL_TARGET`-vs-`WIN_RATE` trade,
   on one map cell.
7. **Two `fs_crew_on()` read sites sit outside the map gate** (`main.py:1000`, `:1084`),
   inherited structure now made reachable. On a gated board seat 3 becomes a raider instead of
   an eco expander, unmeasured except by the n=72 gated leg.
8. **Inherited and untouched:** every v519 open item except 0 (the annulus floor, taken here).

---

## ARTIFACTS

`scratchpad/s51_v520_build/` —
`arms/` (18: `parent` = a frozen copy of `_v519cripple`, `flagoff`, the eight mechanism arms,
the three guard-probe arms, the three isolation arms, the three determinism arms),
`grid/` (39 headline blocks × 3 arms, **all replays kept**),
`iso/` (13 blocks × 4 arms), `gated/` (2 draws × 2 arms), `lat/` (4 probe arms),
`mech/` (8 arms), `probe/` (the two guard positive-control batteries),
`eq/` (byte-identity + its negative AND positive controls),
`out/` (per-block instrument TSVs), `reel/` (6 replays + the copied autopsy machinery +
`NARRATE.txt` + `GUARDS.txt` + `ROWS.tsv`),
`crip_*.tsv`, `seatrate_*.tsv`, `termcov_*.tsv`, `nobody_*.tsv`,
`PARENT_FREEZE.md5`, `PIDS`.

**Instruments, each guarded both ways:**
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive
  control (2 hits, which is what makes the v520 zero mean something).
* `collide.py` — the slot-10 two-writer pre-flight, driven to BOTH verdicts including a
  reconstructed KNOWN-BAD configuration that must read `COLLISION: True`.
* `mechread.py --selftest` — a synthetic tape through every counter, a full mutation control
  (every counted line retagged → every column zero), a single-column mutation, and a malformed
  line that must be REPORTED as `PARSE_BAD` rather than swallowed.
* `latread.py --selftest` — four cases including never-replaced (must read NEVER, not 0) and an
  arrival BEFORE the kill (must not count).
* `seatrate.py --selftest` — seven guards incl. a mutation control, a SIMULTANEITY control
  (8 seats denied but never together ⇒ `closure_round = −1` while `closure_cum_round ≥ 0`), a
  zero-presence control returning `None` not 0, an ENEMY-ONLY control, and a real-data
  team-swap positive control.
* `termcov.py --selftest` — 22 guards incl. a channel census that must report an injected
  out-of-schema field, a launch-attribution control that returns AMBIGUOUS rather than
  silently ours, and a team-swap positive control.
* `nobody.py --selftest` — runs `gapdecomp.guard()` and `phase.guard()` **in place**, plus a
  mutation control, an inverted control, an empty-window control returning `None`, an
  enumerated two-envelope control, and a kill-clock offset assertion.
* `crip.py --control` — the TEAM-SWAP positive control; all seven columns move.
* `phase.py` — synthetic empty/known/ordering guards plus the real-data kill-mark cross-check
  against the grid TSV: **2 alarms in 4,212 games at a single consistent offset.**
* `reel/reel520.py` — the autopsy guards run in place (HP identity 6/6, fireTurret vs UpdateHp
  channel agreement 6/6 both teams) plus a negative control on its one piece of new code.
* `eq/` — the determinism test with a negative control (same tree twice) AND a positive control
  (parent vs FIRED must differ).

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* **v520 IS THE BUILD OF THE NIGHT AND THE EFFECT IS OUTSIDE EVERY INTERVAL AT n=1,404/arm:
  wins +6.20 (hw 3.61), k≤200 +10.47 (hw 3.11) to 28.1%, k≤300 +9.19 to 40.0%, median kill
  254→203, funded→kill 91→71 — with the byte-identical known-zero arm reading ≈0, so the
  ~5pp fixture floor did NOT fire.** Magnus's pincer is measured real: seal rate RISES with
  two bodies only in this arm, simultaneous closure 31.7→43.9%, NOBODY 22.1→12.6%.
* Isolation: the ENTIRE effect is the split (iPIN reproduces the composite); PRESENCE −2.56
  (null-to-negative; its own metric failed while role-convert meets Magnus's 15-round cap at
  6 rounds 26/26) and GUNNEAR −0.85 (null). ⇒ next parent's fired config = PINCER-ONLY;
  PRESENCE/GUNNEAR stay flagged OFF pending a better dose.
* Magnus's terminal-launcher eviction objective: honest zero — the split-capable tiles sit
  at dsq 9-32 where a d²≤2 pickup cannot touch a seat; and the true coverage ceiling is 2,
  not the autopsy's 4. Delivery (objective a) met 24/24. The eviction half of that idea needs
  a different body, not a better tile.
* ⛔ KNOWN DEFECT IN THE TREE, fix before it parents: two fs_crew_on() read sites outside the
  map gate (main.py:1000,:1084) leak crew behaviour onto gated maps.
* ⭐ THE REFRAME (routed to v521): pooled heal-back is now NULL in all arms — cumulative seals
  are not the currency; **the currency is closure-simultaneity OVERLAPPING the turret's funded
  life** (0/119 reel heal-rounds fell in a fully-sealed round; a real 43-round closure sat
  disjoint from its turret's life). v521 = seal-shot synchronization.
* KILL_TARGET panel: median 203 (target 180 — within reach for the first time), k≤200 28.1%
  (target 50%). SHIP_BAR explicitly not addressed (6-map grid is a non-arming read; the
  full-pool powered read comes when a config stabilizes).
