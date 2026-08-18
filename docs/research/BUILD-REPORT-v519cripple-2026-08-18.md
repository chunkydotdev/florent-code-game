# BUILD REPORT (DRAFT) — `bots/_v519cripple` (the cripple pair), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v518fastsent` FROZEN (`chmod -R a-w`, md5 in
`scratchpad/s51_v519_build/PARENT_FREEZE.md5`) together with `_v488beltbreak2`. Master
`LOKI_FS_V519`; False reproduces the parent (structurally audited, AST-scanned and
byte-proved below). Scratch: `scratchpad/s51_v519_build/`. PAR=4 on single-arm legs; the headline runs 3 arms × PAR 2 = 6 concurrent games,
the gated and byte-identity legs at PAR 3.
Recorded PIDs in `scratchpad/s51_v519_build/PIDS`. `scratchpad/overnight*` and corefill
untouched.*

*Diff vs parent: doctrine +151/−0 (comment + 10 constants), siege +144/−0, main +4/−0,
`raid.py` +15/−3 (one default-inert keyword argument), `eco.py` BYTE-IDENTICAL (0/0).
**2,650 games with a result row across every leg; 0 tracebacks, 0 no-winners** (counted off
the 77 grid TSVs by header match, not by directory).  ⛔ Timeouts are NOT reported — v518 finding 0 proved the
local timeout column is a constant that cannot fire.*

---

## ⛔⛔ FINDING 1 — CHANGE 1 (GUNNER-FIRST) DELIVERS A DOSE OF **ZERO**, AND THE REASON IS NOT THE ROUND GATE

The mandate's premise: *"the ferry chain crosses the beltbreak annulus (d²20-50) at ~r5-9;
the plant gate opens r10 … the raider PAUSES ONE HOP in the annulus and plants the shredder
at r10-12."* The instruction was to change **WHEN and WHO, never WHAT** — reuse
`_try_beltbreak_gunner`'s siting ladder, do not fork it. That is exactly what was built, and
it was measured before it was believed.

### (a) THE BEFORE TAPE — `GFBUDGET.txt`, 10 instrumented games, every ferry round r0-r40

`FS_V519_GF_LOG` prints one line per ferry round with the body's d² to the enemy core, the
bank, and the three prices. It is deliberately **outside** the behaviour flag, so the
baseline can be taken with the behaviour OFF (an instrument that only runs in the treatment
arm cannot measure a baseline).

| map | ferry rounds | rounds IN the annulus (20 ≤ d² ≤ 100) |
|---|---|---|
| nordkap | 4 | **r1 (d100), r2 (d100)** |
| atoll | 4 | **r3 (d72), r4 (d72)** |
| glacierkeep | 8 | **r5, r6 at d101 — one outside the band** |
| drakkarfjord | 10 | **r9 (d32), r10 (d32)** |
| midgard | 13-40 | **r9 (d85), r10 (d85)** |

⇒ **THE CROSSING IS r1-r10 AND `LOKI_BELTBREAK_RND` IS 10.** On three of five siege maps the
body is already at the ring before a plant is legal. The round IS a "when", so a v519
constant `FS_V519_GF_MIN_RND = 3` was added and passed to `_try_beltbreak_gunner` as
`rnd_floor` — a keyword whose default `None` is the parent path byte for byte.

### (b) WITH THE ROUND FIXED, THE FUNNEL SAYS THE ROUND WAS NEVER THE BLOCKER

30 instrumented games (5 siege maps × 3 seeds × 2 seats), the treatment on, every attempt
counted at the same call site (`scratchpad/s51_v519_build/DIAG2.tsv` + logs). **356 attempts,
0 plants.** The refusals, by the first gate that fired:

| refusal | count | what it means |
|---|---|---|
| **NORAY** | 142 | targets seen, but no legal (build tile, facing) with a clear ray **and** a build tile inside the d²≥20 annulus |
| **SILENT_PRESCAN** | 84 | body outside the band's ±24 pre-scan |
| **HARV** | 70 | **OUR** `SLOT_HARVESTERS` is still 0 (`LOKI_BELTBREAK_MIN_HARV = 1`) |
| **NOTGT** | 60 | **no enemy harvester, conveyor or splitter in the raider's vision at all** |
| PLANT | **0** | — |

Per map: glacierkeep and nordkap die on `HARV` (we have no harvester at r1-r6); atoll and
drakkarfjord die on `NOTGT` at r3-r10 (at d²=32-85 with builder vision r²=20, their belts do
not exist or are not visible yet); midgard dies on `NORAY` at the ring.

### (c) THE CEILING WAS PRICED WITH TWO NON-SHIPPED PROBE ARMS, NOT ASSERTED

| probe arm (30 games each) | change | plants |
|---|---|---|
| `pHARV` | `LOKI_BELTBREAK_MIN_HARV` 1 → 0 | **0** (HARV refusals convert into NOTGT/NORAY) |
| `pBAND` | …plus `LOKI_BELTBREAK_DSQ_LO` 20 → 8 | **8 plants in 8 of 30 games, at r9-r38, from a body at d²=4-13** |

⇒ **The productive shredder position for a siege body is the RING, not the annulus, and the
annulus floor is what forbids it.** Both probe changes are changes to the **WHAT** — the
siting rule — and are therefore outside this mandate. **They are the v520 routing item and
they are priced: 8/30 games is where the dose starts.**

⚠ The `pBAND` plants were confirmed **engine-side**: the replay-side gunner census reads
first-plant r10 and r11 on the two games whose `GF519 PLANT` stderr lines say r10 and r11.
Bot-side log and wire agree exactly. *(And `print()` — the `BB48 PLANT` line — never reaches
the local CLI stdout at all; it goes into the replay. The engine-side census is the only
instrument that would survive a platform leg.)*

**CHANGE 1 SHIPS AS BUILT, AT DOSE ZERO.** It is bounded (one plant per body, r3-r40, a
75-Ti collar floor), mutant-driven, and its null closes a road with numbers attached — the
v518 change-2 pattern. **Every headline number below is therefore change 2's**, and the
report says so rather than letting a two-change build take credit for one change.

---

## ⭐⭐ CENTREPIECE — THE `KILL_TARGET` PANEL, n=468/arm, THREE ARMS CONCURRENT PER BLOCK

13 blocks × 36 games, **6 maps** (the standard 5-map siege grid **plus yulerune**, the second
registered cripple cell — a MODESWITCH headline that omits half its treated population would
be measuring the change on one map) × 3 seeds × 2 seats, vs `bots/_v488beltbreak2`. All three
arms run **inside the same block on the same seeds** (`--seed` does not pin a game, v515
finding 1). A block counts only when **all three** arms finished all 36 games.

| | **parent (`_v518fastsent`, floor 60)** | **v519 FIRED** | **v519 MODESWITCH-OFF** |
|---|---|---|---|
| WINS | 204/468 (43.6%) | **289/468 (61.8%)** | 221/468 (47.2%) |
| ≤r150 | 26 (0.056) | 23 (0.049) | 23 (0.049) |
| **≤r180** | 44 (0.094) | **61 (0.130)** | 59 (0.126) |
| **≤r200 (tracked metric)** | 59 (0.126) | **98 (0.209)** | 81 (0.173) |
| ≤r250 | 88 (0.188) | **132 (0.282)** | 111 (0.237) |
| **≤r300 (ITT primary)** | 103 (0.220) | **165 (0.353)** | 128 (0.274) |
| **median kill round** | 262 | **241** | 221 ⚠ (collider — see below) |
| our core destroyed | 236 | **157** | 230 |
| r1000 games | 53 | 52 | 40 |

| contrast | Δ wins | Δ k≤200 | Δ k≤300 |
|---|---|---|---|
| **v519 FIRED vs parent** | **+18.16 pp** (hw 6.40) **OUTSIDE** | **+8.33 pp** (hw 4.79) **OUTSIDE** | **+13.25 pp** (hw 5.79) **OUTSIDE** |
| **msoff vs parent** *(known-zero)* | +3.63 pp (hw 6.38) inside | **+4.70 pp** (hw 4.57) **⚠ OUTSIDE** | +5.34 pp (hw 5.52) inside |

⛔ **READ THE SECOND ROW FIRST.** `msoff` differs from `parent` only by an inert change 1, so
it is a KNOWN-ZERO CONTROL — and it reads **+4.70 pp OUTSIDE its naive interval on the tracked
metric at n=468/arm.** That is v518 finding 2 firing again on this fixture. **The false-positive
floor here is ~5 pp; the treatment's +8.33 pp clears it, but not by the margin the interval
alone would suggest.** ⚠ **AND `median kill` IS A CONDITIONAL, i.e. a collider** (`msoff`'s 221
is computed over 198 kills, v519's 241 over 259). The ITT shares are the primary; the median is
a diagnostic.

### ⭐⭐ THE DECOMPOSITION THAT MAKES THE HEADLINE READABLE — treated cells vs untouched cells

| cut | parent | v519 FIRED | msoff | contrast |
|---|---|---|---|---|
| **TREATED {midgard, yulerune}** n=156 | 25 (16.0%) | **81 (51.9%)** | 25 (16.0%) | **FIRED vs msoff +35.90 pp (hw 10.51) OUTSIDE** · msoff vs parent **+0.00 pp** |
| ↳ k≤300 | 10 (6.4%) | **43 (27.6%)** | 16 (10.3%) | |
| **UNTOUCHED (4 maps)** n=312 | 179 (57.4%) | 208 (66.7%) | 196 (62.8%) | FIRED vs msoff +3.85 pp (hw 7.50) **inside** |

⭐ **ON THE CELLS THE CHANGE TOUCHES, THE KNOWN-ZERO CONTROL IS EXACTLY 0.00 pp AND THE
TREATMENT IS +35.90 pp. On the cells it does not touch, the treatment is inside its interval.**
That is the cleanest isolation this line has produced.

**COMPOSITION ARITHMETIC, and it accounts for the whole pooled number:** the treated cells are
156/468 = 33.3% of the grid; +35.90 × 0.333 = **+11.97 pp**, against a pooled +18.16 pp. The
residual +6.2 pp is the untouched-cell drift, which the known-zero control shows at
+5.45 pp on the same cells. ⇒ **MODESWITCH is worth ≈ +12 pp ON THIS GRID; the rest is
fixture.** MAPSEG predicted "+4-5 pp pooled by composition" against a 5-map denominator with
one treated cell — this grid has two treated cells at a third of the weight.

### PER MAP — wins/78 [k≤300] {k≤200}

| map | parent | **v519 FIRED** | msoff |
|---|---|---|---|
| atoll | 36 [10] {4} | 35 [15] {10} | 30 [9] {7} |
| drakkarfjord | 45 [29] {24} | 58 [33] {24} | 59 [38] {30} |
| glacierkeep | 64 [39] {15} | 63 [45] {28} | 67 [46] {24} |
| **midgard** | 17 [5] {2} | **48 [27] {12}** | 13 [8] {3} |
| nordkap | 34 [15] {9} | 52 [29] {15} | 40 [19] {12} |
| **yulerune** | 8 [5] {5} | **33 [16] {9}** | 12 [8] {5} |

⚠ nordkap moves 34 → 52 → 40 across three arms that play it identically. **No single map cell
of this table is a conclusion.**

### PER BLOCK wins/36 — parent / v519 / msoff
17/24/18 · 15/22/20 · 18/19/19 · 14/21/16 · 14/21/17 · 14/27/14 · 18/18/20 · 17/27/16 ·
22/21/15 · 13/23/17 · 12/23/17 · 18/22/18 · 12/21/14

### THE PHASE BUDGET — `phase.py`, replay-side, n=468/arm

Kill mark cross-checked against the grid TSV in all 1,404 games: **0 alarms, and the
`tsv_turn − walker_round` histogram is the single value {1: …} in every arm.**

| arm | med ARRIVE | med SENT | med FUNDED | med KILL | spawn→arrive | arrive→sent | sent→funded | **funded→kill** | games w/ fwd sentinel |
|---|---|---|---|---|---|---|---|---|---|
| parent | 9.5 | 81 | 81 | 261 | 9.5 | 71.5 | **0** | **101.5** | 327/468 |
| **v519 FIRED** | 10.0 | 108 | 108 | 240 | 10.0 | 96.0 | **0** | **92.0** | 338/468 |
| msoff | 9 | 84 | 84 | 218.5 | 9 | 74.0 | **0** | 97.0 | 343/468 |

⭐ **`funded → kill` — the quantity v518 named as the binding constraint — MOVES for the first
time in this line: 101.5 → 92.0 rounds (−9.4%).** `sent → funded` is 0 in all three arms
again (v516's fix, confirmed a fourth time). ⚠ `arrive → sent` GROWS 71.5 → 96, and **that is
a composition shift, not a slowdown — which was checked rather than argued:**

| cut | arm | med ARRIVE | med SENT | **arrive→sent** | **funded→kill** | games w/ SENT |
|---|---|---|---|---|---|---|
| **UNTOUCHED (4 maps)** | parent | 8 | 90 | **81.0** | **101.5** | 215 |
| | **v519 FIRED** | 8 | 96 | **87.5** | **93.0** | 242 |
| | msoff *(known-zero)* | 8 | 97 | **87.0** | 97.0 | 232 |
| **TREATED {midgard, yulerune}** | parent | 51 | 42 | −9.0 ⚠ | 103.0 | 112 |
| | **v519 FIRED** | 43 | 178 | 134.5 ⚠ | **75.5** | 96 |
| | msoff | 50 | 42 | −9.0 ⚠ | 92.0 | 111 |

⇒ **On the untouched maps `arrive → sent` is 87.5 (v519) against 87.0 (the known-zero arm) —
identical; the +6 vs the parent is the same fixture drift the rest of this report measures.
The siege lane did NOT slow down.** ⚠ On the treated cells the marks are not interpretable as
a siege budget at all (a NEGATIVE `arrive → sent` means a turret inside d²≤40 existed before
any builder of ours reached d²≤8 — chassis home-turret geometry on a small board), which is
exactly what "the plank stood down here" should look like. **`funded → kill` improves on both
cuts: 101.5 → 93.0 untouched and 103.0 → 75.5 treated.**

---

## ⭐⭐ HEAL-BACK — THE NUMBER THE MANDATE COMMISSIONED

`crip.py`, replay-side: healing landed on the ENEMY core / damage landed on it, the rush
autopsy's ledger method (UpdateHp deltas, +1..+4 heal, −18/−7/−2 damage). Reported over games
where damage was actually landed; a 0-damage game has no defined ratio and pooling it as 0
would read as "they healed nothing".

| | parent | **v519 FIRED** | msoff |
|---|---|---|---|
| **median heal-back (pooled, n=468/arm)** | 0.585 | **0.000** | 0.433 |
| share of games with heal-back ≥ 0.90 | 33.6% | **14.2%** | 28.7% |
| their harvesters built / game | 6.64 | 6.51 | 6.41 |
| their belts built / game | 42.0 | **36.8** | 38.5 |
| their economy destroyed / game | 5.43 | **7.04** | 4.81 |
| our shredders (gunner, d²≤100 of their core) / game | 0.80 | **1.11** | 0.80 |
| median first shredder round | 52 | **34** | 51 |

### AND THE SAME SPLIT AS THE HEADLINE, WHICH IS WHAT MAKES IT ATTRIBUTABLE

| cut | parent | **v519 FIRED** | msoff |
|---|---|---|---|
| **TREATED** median heal-back | 0.992 | **0.000** | 0.906 |
| **TREATED** share ≥ 0.90 | 58.6% | **13.5%** | 51.4% |
| **TREATED** their eco killed / built | 5.69 / 45.1 | **11.78 / 37.8** | 4.25 / 43.1 |
| UNTOUCHED median heal-back | 0.294 | 0.228 | 0.182 |
| UNTOUCHED share ≥ 0.90 | 20.7% | 14.5% | 17.7% |
| UNTOUCHED their eco killed / built | 5.30 / 40.5 | 4.68 / 36.2 | 5.09 / 36.1 |

⇒ **ON THE TREATED CELLS THE DEFENDER'S HEAL-BACK GOES FROM 0.99 (parent) AND 0.91 (the
known-zero control) TO 0.00, WHILE THE ENEMY ECONOMY WE DESTROY MORE THAN DOUBLES (4.25-5.69
→ 11.78 buildings/game) AND THEIR BELT COUNT FALLS 43-45 → 37.8.** The untouched cells move
by nothing. **The autopsy's third shape — cut the income that pays for the heals — is the one
that had never been built, and this is it measured.**

⚠ **HONEST READ OF THE MECHANISM:** on the treated cells the plank stands down, so we are
not "cutting their income while sieging" — we are **playing a different game there**, one
whose shredders arrive at r19-r38 instead of r41-r61 and whose damage on their core is lower
(mean 424 vs 499) but not healed back. The heal-back collapse is real and it is
**MODESWITCH's**, not GUNNER-FIRST's.

---

## PER-CHANGE VERIFICATION (every mutant driven, zero-vs-nonzero)

### 1 — GUNNER-FIRST (`FS_V519_GUNFIRST`)

**(a) The mechanism arms, n=36 each (6 maps × 3 seeds × 2 seats), all instruments on.**
⛔ The win column of a mechanism arm is not read.

| arm | GF519 ferry-round lines | **PLANTS** | MODE519 refusals | maps refused |
|---|---|---|---|---|
| `mF` (all on) | 159 | **0** | 89 | midgard, yulerune |
| `mG` (GUNFIRST off) | 161 | **0** | 93 | midgard, yulerune |
| `mM` (MODESWITCH off) | **462** | **0** | **0** | — |
| `mGate10` (`FS_V519_GF_MIN_RND = 10`) | 157 | **0** | 86 | midgard, yulerune |
| `mGFPOOR` (`FS_V519_GF_TI_FLOOR = 400`) | 158 | **0** | 86 | midgard, yulerune |
| `mOff` (master off) | 0 ⚠ | 0 | 0 | — |

⚠ `mOff`'s GF519 tape is **empty BY CONSTRUCTION** — the log is gated on the master flag — so
its instrument columns are void; only its behaviour is comparable (same caveat v518 recorded
for its own `mOff`). ⭐ `mM`'s **462** ferry-round lines against `mF`'s 159 is the MODESWITCH
signature seen from the other side: with the switch off, the two cripple cells run a ferry
again and the ferry-round tape triples.

**(b) The dose is zero in every arm, and the ceiling was priced with two NON-SHIPPED probes.**

| arm (30 games) | change | attempts | **plants** |
|---|---|---|---|
| treatment (`FS_V519_GF_MIN_RND = 3`) | — | 356 | **0** |
| `pHARV` probe | `LOKI_BELTBREAK_MIN_HARV` 1 → 0 | 353 | **0** |
| `pBAND` probe | …plus `LOKI_BELTBREAK_DSQ_LO` 20 → 8 | 310 | **8 in 8 games, r9-38, body at d²=4-13** |

Zero-vs-nonzero ✅ — but the non-zero arm is a **probe**, not the ship. The replay-side gunner
census is the independent confirmation: on the four untouched maps the first-shredder round is
unchanged between `v519` and `msoff` (glacierkeep r36 = r36, nordkap r16 = r16, drakkarfjord
r85 vs r83), i.e. change 1 moves nothing where change 2 is not acting.

**(c) BUDGET GUARD, driven to the other verdict on real data rather than asserted.**
`FS_V519_GF_TI_FLOOR = 75` is derived in `GFBUDGET.txt` as one more ferry link (launcher 34-38
at the crossing) plus the first collar (8 seats × barrier 5-6). Evaluated at every in-band
ferry round of the BEFORE tape (`GFGUARD.txt`):

| `FS_V519_GF_TI_FLOOR` | passes | refuses |
|---|---|---|
| 0 | 16 | 0 |
| **75 (shipped)** | **16** | **0** |
| 150 | 16 | 0 |
| 300 | 4 | 12 |
| **400 (`mGFPOOR`)** | 2 | **14** |

Bank at those rounds 216-434 Ti against a gunner at 28-35. ⇒ **the shipped floor is a RAIL,
not a dose; the predicate is shown to produce both verdicts.**

### 2 — MODESWITCH (`FS_V519_MODESWITCH`)

**(a) The behavioural signature, engine-side, zero-vs-nonzero.** Our forward launchers
(d²≤100 of THEIR core — the ferry chain) and our collar barriers (d²≤8), per game:

| map | parent | **v519 FIRED** | msoff |
|---|---|---|---|
| **midgard** | laun 3.32 / bar 9.08 | **laun 0.00 / bar 13.53** | laun 3.31 / bar 6.74 |
| **yulerune** | laun 4.45 / bar 10.41 | **laun 0.12 / bar 13.50** | laun 4.24 / bar 6.06 |
| atoll | 3.86 / 12.46 | 3.53 / 18.22 | 3.55 / 16.36 |
| drakkarfjord | 2.24 / 19.65 | 3.54 / 18.63 | 2.58 / 20.77 |
| glacierkeep | 2.18 / 22.83 | 2.18 / 17.83 | 2.36 / 18.76 |
| nordkap | 4.21 / 14.99 | 3.37 / 15.68 | 3.76 / 15.95 |

**The ferry goes to zero on exactly the two registered cells and nowhere else** — modeswitch-off
reproduces the siege on midgard (3.31 launchers/game) and yulerune (4.24) digit for digit
against the parent. ⚠ The yulerune residual **0.12 launchers/game is not a leak of the plank**:
yulerune is 20×20 with cores 14 apart, so the chassis' own home-launcher line lands inside a
d²≤100 radius of their core. The collar-barrier column is the confirmation — it does not fall,
because those barriers are the chassis' own, not the siege collar's.

**(b) The map signatures were read off the ENGINE, one game each, not from a map file**
(`FS GATE … sig …` with `FS_LOG` on, 2026-08-18):
`midgard (30, 30, (2, 2), (26, 26))` · `yulerune (20, 20, (2, 9), (16, 9))`. archipelago's
`(26, 26, (5, 5), (19, 19))` reads `ok 0` — the existing `FS_MAP_SKIP` — which is the positive
control that the signature form is the right one.

**(c) The list is a registered constant with its derivation in its comment**
(`doctrine.py` §2): MAPSEG's admission rule — a cell enters only if it clears its tape's
pooled mean by more than one half-width **on both axes**; {midgard, yulerune} clear by >2 on
both; ore distance was tested as a selector and refuted.

---

## FLAG-OFF AUDIT

**Structural.** Every behavioural site is guarded by `LOKI_FS_V519` **and** its own sub-flag,
read at RUN time — 4 guard expressions:
`siege.py:476` (MODESWITCH), `siege.py:1013` (GF log), `siege.py:1015` (GUNFIRST, ferry site),
`siege.py:1133` (the helper's own early return, which is the ONLY flag read covering the
ring site at `siege.py:1828` — deliberate: two call sites must not each carry their own copy
of the flag test).
The unguarded additions are the two `v519_gf_*` state fields (written in `__init__`, read only
under a guard) and `raid.py`'s `rnd_floor=None` keyword — default is the parent path.
`eco.py` is byte-identical to the parent.

**NO NEW DERIVED DEFAULTS** (`flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v519 flag):

```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v519 derived defaults: 0 []
v518 derived defaults (inherited, must also be 0): 0 []
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```

⛔ The real-case control is what makes the zero meaningful — the scanner is proved able to see
the known v515 hazard in this very file before its zero for v519 is believed.

**Behavioural.** Interleaved fixtures (both arms inside the same block), flag-off vs a frozen
copy of the parent, on the 6-map grid:

| fixture | seeds | flag-off | parent | Δ wins | Δ k≤300 |
|---|---|---|---|---|---|
| FO1, interleaved, n=180 each | 101-115 | 89/180 (49.4%) | 93/180 (51.7%) | −2.22 pp (hw 10.33) inside | +2.78 pp (hw 9.54) inside |
| FO2, interleaved, n=180 each | 301-315 | 92/180 (51.1%) | 79/180 (43.9%) | +7.22 pp (hw 10.32) inside | +3.33 pp (hw 9.01) inside |
| **pooled n=360 each** | | **181/360 (50.3%)** | 172/360 (47.8%) | **+2.50 pp (hw 7.30) inside** | **+3.06 pp (hw 6.57) inside** |

Also pooled: median kill 241 vs 244, our core destroyed 170 vs 175, r1000 29 vs 28,
tracebacks 0/0. ⚠ **The two fixtures disagree in SIGN on wins (−2.22 / +7.22) on code that
plays identically** — v517's sign-flip, reproduced. This is why the byte-diff below is the
verdict and the win rates are context.

**Byte-identity (v518's method, reused).** A win-rate comparison cannot settle a null at any n
this fixture can afford, so the question was asked directly: run both trees on the same seeds
with the randomness switched off — **ours AND the opponent's** (`arms/eq_opp` =
`_v488beltbreak2` + `NOISE_ON = False`; v518 finding 2 measured that disabling our salt alone
pins nothing) — and diff the replay bytes. 12 games, 6 maps × 2 seats:

```
NEGATIVE CONTROL  parent vs parent (same tree, two runs): identical 12 / differing 0
TEST              parent vs FLAG-OFF                    : identical 12 / differing 0
```

⇒ **THE FIXTURE IS DETERMINISTIC (the control proves the instrument can distinguish) AND
`LOKI_FS_V519 = False` PLAYS `bots/_v518fastsent`'s 12 GAMES BYTE FOR BYTE.** No win-rate
battery can make that claim, and the +2.50 / +3.06 pp above are shown to be exactly the
fixture noise this report measures three other ways.

---

## GATED CONTROL — archipelago vs `_v468kladturbo`, pooled n=72 (two draws of 36)

archipelago's signature is in `FS_MAP_SKIP`, so `_fs_gate` already refuses: MODESWITCH's extra
refusal is a no-op and GUNNER-FIRST's two call sites (`_fs_ferry_turn`, `_fs_ladder_turn`) are
never reached. **Both changes are structurally unreachable.**

| draw | v519 | parent (`_v518fastsent`) |
|---|---|---|
| seeds 1-18 | 23/36 (63.9%) | 20/36 (55.6%) |
| seeds 19-36 | 26/36 (72.2%) | 25/36 (69.4%) |
| **pooled n=72** | **49/72 (68.1%)** | **45/72 (62.5%)** |

k≤300 pooled: 35 (48.6%) vs 36 (50.0%); median kill 194 vs 175; 0 tracebacks. **No alarm on
the primary** — but ⚠ **the +5.6 pp win gap on a board where neither change can execute is the
one-draw law again, and it is the third independent instance of it in this report** (the
msoff known-zero at +4.70 pp, the untouched-cell drift at +5.45 pp, and this).

---

## FAILURE REEL — the six worst losses of the best arm

**SELECTION RULE, stated because it is a choice: the EARLIEST our-core-death in EACH of the
six maps, for the `v519 FIRED` arm** (the best arm on wins, 61.8%, and the shipped
configuration). One per map is what stops the reel being six copies of one board — the five
earliest deaths *overall* would again have been dominated by a single map family.

Decoded with the s51 autopsy machinery **copied, not rewritten** (`turrets.py`, `tape.py`,
plus this build's `crip.py`), so its guards ran in place: **HP identity 6/6, delta alphabet
clean, fireTurret core-hit counts == UpdateHp −18 counts for BOTH teams 6/6.** Everything
below is engine-side.

### 1. `nordkap_s8_A` — our core dead r112 — **NO_TURRET**
The raider held the ring for **100 of 112 rounds** — the best presence in the reel — and the
team still put **zero shots on their core**. Two sentinels were built (r10 at d²=130, r48 at
d²=242): both are HOME turrets, they fired 15 shots between them and not one landed on the
enemy core. Their first core-hitting turret opened at **r10** and delivered 31 shots.
**Known class (autopsy #2), and presence was not the blocker.**

### 2. `atoll_s4_B` — our core dead r114 — **NO_TURRET**
22 ring rounds of 114. Seven turrets built, **two of them beltbreak shredders (r20 at d²=58,
r62 at d²=40) that landed 29 shots on their economy** — the cripple half worked — but the one
sentinel went up at d²=132 (home) and their core took nothing. Their turret opened r59 with
28 shots, exactly one core's worth.

### 3. `yulerune_s36_A` — our core dead r132 — **NO_TURRET** — *a CRIPPLE-cell loss, and it shows what the mode costs*
MODESWITCH stood the plank down here, so there is no ferry (0 forward launchers) and the
chassis planted a shredder at **r19** which fired 31 shots. 99 ring rounds. **And their core
finished at 500 HP: we never threatened it.** Their two turrets opened at r69 and killed us
with 28 shots. **The cripple mode wins this cell 33/78 — but when it loses, it loses without
ever putting a shot on the core.**

### 4. `midgard_s15_A` — our core dead r146 — **NO_TURRET** — *the same shape on the other cripple cell*
Shredders at r37 and r53 (d²=60 and 32), 23 shots into their economy, 99 ring rounds, their
core untouched at 500 HP. The two sentinels we did buy sit at d²=1070 and d²=1352 — the far
side of our own half. Their turrets opened r109.

### 5. `drakkarfjord_s10_B` — our core dead r242 — **NO_TURRET**
86 ring rounds of 242, **eight turrets, zero shots on their core, zero shredders in the
annulus**, and their economy (9 harvesters + 100 belts) lost **nothing** all game. The two
sentinels are at d²=1014 and d²=1254; the one gunner that fired 110 shots is at d²=906 —
i.e. every weapon we bought was pointed at our own half.

### 6. `glacierkeep_s20_B` — our core dead r518 — **MAG_STARVED**
The one non-NO_TURRET row. A forward sentinel landed at (15,6), d²=12, **r80** and lived 87
rounds, putting 23 shots (414 damage) into their core — **and 252 of it was healed back
(0.609)**. Its funded share was **0.05**: the magazine was dry for 95% of its life. Their core
finished at 338 HP; their first core-hitting turret did not open until **r463**. **This is
autopsy #1 in its purest form and it is not fixed.**

**NO NEW CAUSE CLASS.** NO_TURRET ×5, MAG_STARVED ×1 — both already in
`corpus/failure_reel.tsv`. ⭐ **The distribution is the finding: five of the six worst losses of
our best arm never put a single shot on the enemy core, and in four of those a raider was
standing on the ring for 86-100 rounds.** That is v518's open item 1 (`NOBODY`) inverted — here
the body IS present and the money still goes into home turrets.

Rows appended to `corpus/failure_reel.tsv` (6, append-only).

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **The headline grid is SIX maps, not five.** yulerune is the second registered cripple cell;
   measuring MODESWITCH on a grid containing one of its two treated maps would have halved the
   treated population and made the composition arithmetic unreadable. The standard-5 subset is
   recoverable from the per-map table.
2. **A THIRD arm was defined as `msoff` (MODESWITCH off) rather than a second dose.** With
   change 1 at dose zero, `msoff` is both the isolation arm for change 2 and a **known-zero
   control** — and it is what caught this fixture's ~5 pp false-positive floor.
3. **`FS_V519_GF_MIN_RND` was added and is not `LOKI_BELTBREAK_RND`.** The BEFORE tape showed
   the crossing (r1-r10) and the parent gate (r10) do not overlap on 3 of 5 maps. The round is
   a "when", which the mandate scopes to this change; the siting rule is a "what", which it
   does not — and that boundary is exactly where the dose died.
4. **Two non-shipped PROBE arms (`pHARV`, `pBAND`) were run to price change 1's ceiling.** A
   null is worth more with the price of the road attached, and `pBAND` is what turns "it does
   not fire" into "it cannot fire without moving the annulus floor, and moving it is worth 8
   plants in 30 games".
5. **The reel carries six rows, not five** — one per map on a six-map grid.
6. **Timeouts are not reported** (v518 finding 0).

## SURPRISES (written down before being explained away)

1. **⛔⛔ THE FERRY IS FASTER THAN THE PLANT GATE.** Nobody predicted that the chain would cross
   the whole d²20-100 annulus by r10 on every siege map, and on nordkap by **r2**. The design
   note that routed this build assumed a ~r5-9 crossing meeting an r10 gate; the crossing is
   r1-r10 and on three maps it is over before the gate opens.
2. **⛔⛔ AND FIXING THE ROUND CHANGED NOTHING: 356 ATTEMPTS, 0 PLANTS.** The blocker is that at
   r1-r10 we have no harvester (70 refusals) and **their economy is not visible or does not yet
   exist** (60 refusals). "Cut their income" needs an income to cut.
3. **⭐ MODESWITCH IS 3-8× ITS PREDICTION ON THE TREATED CELLS.** MAPSEG's composition estimate
   was +4-5 pp pooled; the treated cells moved **+35.90 pp** and the pooled composition term is
   **+12 pp**. midgard 17/78 → 48/78 and yulerune 8/78 → 33/78.
4. **⭐⭐ THE DEFENDER'S HEAL-BACK ON THE TREATED CELLS COLLAPSES FROM 0.99 TO 0.00** while the
   enemy economy we destroy more than doubles. The autopsy predicted the direction; nobody
   predicted the magnitude, and the known-zero control on the same cells sits at 0.906.
5. **`funded → kill` MOVED FOR THE FIRST TIME (101.5 → 92.0)** — and it moved on BOTH cuts
   (101.5 → 93.0 on the untouched maps, 103.0 → 75.5 on the treated ones), which was not the
   prediction: standing the plank down on two maps was expected to move the pooled number by
   composition alone.
6. **⛔ THE KNOWN-ZERO CONTROL CLEARED ITS OWN INTERVAL ON THE TRACKED METRIC (+4.70 pp,
   hw 4.57).** v518 finding 2 said pooling non-time-adjacent fixtures manufactures separations;
   this grid is time-adjacent, interleaved, three arms per block — **and it still did it.**
7. **FIVE OF THE SIX WORST LOSSES OF THE BEST ARM NEVER PUT A SHOT ON THE ENEMY CORE**, with a
   raider on the ring for 86-100 rounds in four of them.
8. **The cripple cells' losses have a signature of their own: their core at 500 HP.** The mode
   that wins those cells wins them by attrition and economy, and when it loses it has not
   touched the core — which is `R1000_IS_DEFEAT`'s exposure, not `KILL_TARGET`'s.

## OPEN ITEMS

0. **⭐ CHANGE 1's ROAD IS PRICED, NOT CLOSED: the annulus floor is the lever.** `pBAND`
   (`LOKI_BELTBREAK_DSQ_LO` 20 → 8) produced 8 plants in 8 of 30 games from a body at d²=4-13.
   That is a **WHAT** change and needs its own mandate — including the question the current
   floor exists to answer (a gunner at d²<20 is in range of the core's defenders and reaches
   ring tiles our own collar occupies).
1. **The TREATED cells' phase marks are not interpretable as a siege budget** (negative
   `arrive → sent`, SENT before ARRIVE). A mode that does not siege needs its own marks —
   "first shredder", "first belt destroyed" — before its clock can be compared to the rush's.
   `crip.py` already emits the first of those.
2. **The false-positive floor on this fixture is ~5 pp and it is now measured three ways**
   (known-zero arm +4.70, untouched cells +5.45, gated board +5.6). Any future claim on this
   grid under ~6 pp needs a control arm in the same blocks, not an interval.
3. **`FS_V519_CRIPPLE_MAPS` has two members and the admission rule is >1 half-width on both
   axes.** MAPSEG's neutral band (8 maps) has never been tested for cells that would enter at a
   looser bar; and glacierkeep/ragnarok are rush-good, which this build does not exploit.
4. **The magazine starvation (autopsy #1) is untouched and still kills games** — reel row 6 is a
   forward sentinel at funded-share 0.05.
5. **`FS_V519_GF_MAX_RND`, `FS_V519_GF_MAX_PLANTS` and `FS_V519_GF_TI_FLOOR` are UNSWEPT** and
   cannot be swept meaningfully while the dose is zero.
6. **Inherited and untouched:** every v518 open item except 2 (the floor sweep, closed at 60).

## DOCTRINE COLLISIONS (flagged, NOT resolved — routing requested)

1. **⚠⚠ MAGNUS'S PRIORITY RULING 1 vs GUNNER-FIRST — and this build deliberately amends the
   ruling for one unit-round.** Ruling 1 (2026-08-18 ~04:02Z, coordination.md:71461) orders the
   collar sequence **barriers → launchers → sentinels**. `siege.py:1828` inserts the shredder attempt **above
   rung 1 (barrier)**, bounded to one plant per body, before r40, and only with the collar's
   own money still on the table. **The anchor for taking it is Magnus's own later variant
   (~05:07Z, coordination.md:71490), verbatim intent: *"maybe there's some scenario where we can cripple them hard by
   an early gunner … while the offensive builders go and set up barriers around their core
   after the gunner is placed"* — barriers AFTER the gunner is the ordering, in his words.**
   ⛔ **The amendment currently costs nothing because it never fires (0 plants in 30 games), so
   the collision is real in principle and worth zero in practice — but the moment open item 0's
   annulus change lands, this clause starts taking rounds off the collar and the ruling needs a
   decision.** This is the same shape v518 flagged for its change 2(a); it is now flagged twice.
2. **⚠ MAGNUS'S RULING 2 (the sentinel gate, ~04:07Z, coordination.md:71462) is untouched by this build** — `FS_SENT_RND_FLOOR`
   and the 2-connected-harvesters disjunction are the parent's, unchanged — **but MODESWITCH
   makes the ruling INAPPLICABLE on two maps**: with the plank stood down there is no siege
   sentinel to gate, and the chassis buys home turrets on its own schedule. A ruling that was
   written for "the first sentry" now has a population it does not cover.
3. **⚠ `R1000_IS_DEFEAT` vs what MODESWITCH actually buys.** The treated cells go 25 → 81 wins,
   and their k≤300 goes 6.4% → 27.6% — so the cells got *both* more wins and more timely kills.
   But the reel's two cripple-cell losses end with **their core at 500 HP**: the mode's failure
   mode is a game where we never threatened the core at all — and the r1000 count is FLAT
   (53 parent / 52 v519 / 40 msoff), so the mode is not buying its wins by stalling. Under `KILL_TARGET` the arm passes;
   under `R1000_IS_DEFEAT` the shape of its losses is worth a ruling before more cells are
   admitted to the list.
4. **⚠ `DEFENCE_ADMISSION_BAR` reads PASS, comfortably** — v519's timely-kill rate (k≤r300) is
   35.3% vs the parent's 22.0%, a RISE, on the ITT denominator. Recorded because the bar is
   scored as a fail-to-exclude claim and the correction direction matters (CLAUDE.md's DEFF
   clause): here it is an exclusion in the favourable direction and needs no restatement.

---

## ARTIFACTS

`scratchpad/s51_v519_build/` — `arms/` (16, incl. `parent` = a frozen copy of `_v518fastsent`,
`msoff`, `flagoff`, the six mechanism arms, the two probe arms and the three determinism arms),
`grid/` (13 headline blocks × 3 arms, **all replays kept**), `gated/` (2 draws × 2 arms),
`fo/` + `fo2/` (flag-off fixtures), `eq/` (the byte-identity test and its negative control),
`mech/` (6 arms), `gfbase/` + `GFBUDGET.txt` (the BEFORE budget tape), `diag2/`, `pHARV/`,
`pBAND/` (the ceiling probes), `reel/` (6 replays + the copied autopsy machinery + `NARRATE.txt`
+ `GUARDS.txt`), `crip_*.tsv`, `KILLPANEL.txt`, `PHASE_SPLIT.txt`, `GFGUARD.txt`, `MECH.txt`, `FLAGOFF.txt`, `EQ.txt`, `HEALPANEL.txt`, `SPLIT.txt`, `GATED.txt`,
`PARENT_FREEZE.md5`, `PIDS`.

**Instruments, each guarded both ways:**
* `crip.py` — the heal-back / income / signature instrument. **TEAM-SWAP POSITIVE CONTROL**: re-reading
  one game with `our_team` flipped must move the columns, and it does (`heal_back` 0.222 ↔ 0.998,
  `opp_harv_built` 2 ↔ 4, `oppcore_dmg` 648 ↔ 990, `fwd_laun_n`, `collar_bar_n`). `fwd_gun_n` was
  0 for both teams in that game, so it was driven separately on a `pBAND` replay (2 ↔ 1, first
  round r10 ↔ r200). Plus the autopsy's HP-identity guard, re-run: **468/468 games per arm**.
* `flagoff_ast.py` — three synthetic controls plus the known-real `FERRY_HOME_ON` positive control.
* `phase.py` — synthetic empty/known/ordering guards plus the real-data kill-mark cross-check
  against the grid TSV: **0 alarms in 1,404 games at a single consistent offset**.
* `headline.py` / `killpanel.py` — **block-completeness guard**: a block counts only when all three
  arms wrote all 36 rows (the writer flushes per game, so a half-block would otherwise pool
  silently and favour whichever arm got further).
* `summarise.py --selftest` — all-win / all-loss / mixed tapes separate on every column.
* `reel/reel519.py` — the autopsy guards run in place: HP identity 6/6, fireTurret vs UpdateHp
  channel agreement 6/6 (both teams).
* `eq/` — the determinism test and **its negative control** (the same tree run twice must produce
  identical replays before "identical" means anything).

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* _(to be typed by the builder)_

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* **MODESWITCH is the night's largest confirmed effect and it is CLEAN: +35.90pp on the
  treated cells {midgard, yulerune} against a known-zero control reading EXACTLY +0.00pp
  there; treated-cell heal-back 0.99→0.00; their economy destroyed 4.25→11.78/game;
  funded→kill 103→75.5 treated.** Honest pooled attribution: +12pp of the 6-map pooled move
  is MODESWITCH's (composition), the rest fixture drift — the ~4.7-5.6pp same-config
  false-positive floor (third measured instance) now caps what ANY single fixture read may
  claim, and is carried beside every headline from here on.
* v519 fired = the new head. Magnus's mode split, measured: play the gunner game where the
  gunner wins, the rush where the rush wins.
* GUNNER-FIRST: zero dose AS MANDATED (the ferry crosses the annulus before the r10 gate;
  356 attempts, 0 plants) — but the road is PRICED: annulus floor d²20→8 gives 8 plants in
  8/30 at r9-38. That is a "what" change → v520, where the ring-side priority clause
  (siege.py:1828, currently dead) goes live — Magnus's own gunner-first words anchor the
  priority amendment, flag stands.
* KILL_TARGET panel: k≤200 20.9% (from 16.5 baseline — first real movement), median 241,
  still far from r180/50%. The reel repeats NO_TURRET (5/6) — the presence/pincer build is
  aimed at exactly that.
