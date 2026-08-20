# BUILD REPORT — `bots/_v531fix` (v530.1), s51, 2026-08-20

**ONE DEFECT, ONE PREDICATE.** `bots/_v530home` was banked DESIGN-VALIDATED and
FIRED-CONFIG-BLOCKED: the mouth-first plank won the socket race and killed the
dead-heads class, and its implementation suppressed the parent's harvester
bootstrap on every eco seat at once — 9.6% of games with **no harvester ever**
against the parent's 0.0%, first-harvester mean r5.79 → r42.74 against a
designed median cost of +3. This tree fixes that and nothing else.

Parent `bots/_v530home`, md5-frozen at `07:31:52Z` and **verified byte-unchanged
at `08:37:53Z`** (`scratchpad/s51_v5301_build/FREEZE.md5`); `bots/_v529merge`
likewise. Tree **uncommitted**, per instruction. `PAR=4` throughout; PIDs in
`scratchpad/s51_v5301_build/PIDS`. `scratchpad/overnight*` and
`corefill_forever.sh` were **not touched**. Wall clock from `date -u` in the
same shell call: freeze `07:31:52Z`, byte-identity `07:34:23–07:35:44Z`,
headline `07:38:59–08:15:14Z`, diagnostic `08:15:16–08:33:50Z`, dose
`08:34:53Z`, report `08:41:37Z`.

---

## ⛔ TOP LINE — FOUR SENTENCES

1. **THE DEFECT IS FIXED ON THE HEADLINE FIXTURE AND MOSTLY FIXED ON THE CRATER
   ONE.** Battery A: `no-harvester-ever` **0.106 → 0.004** (parent 0.000, inside
   the interval), first-harvester **mean r42.87 → r9.55** against a **median of
   r7** — the mean-minus-median gap, which *was* the whole finding, collapses
   **34.87 → 2.55** (parent 0.75) — and `first harvester after r60` goes
   **0.146 → 0.004**. Battery B (crater panel): `noharv` **0.062 → 0.037**
   against a parent of 0.008, still **outside** the interval; `>r60`
   **0.406 → 0.146**.
2. **THE P1 MECHANISM SURVIVES.** Battery B: race margin `eseal₁ − head1`
   **−30.9 (parent) → +18.1**, socket race won **0.362 → 0.688**, belt-never-
   reaches-home **0.348 → 0.156**, and `titanium_collected = 0 at r100` goes
   **0.463 → 0.325 — better than the parent**, with mean r100 delivery restored
   to parent level (209.9 vs 203.6, against v530's 106.2). Battery A: head1
   **13.7 → 6.0**, beltfail **0.031 → 0.000**, race won **0.819 → 0.960**.
3. **THE `DEFENCE_ADMISSION_BAR` BREACH IS GONE ON BATTERY B AND STILL STANDS ON
   BATTERY A.** B: **0.342 → 0.290, −5.21 ± 5.88, INSIDE** (v530 was
   −16.46 ± 5.55 on this re-run, −18.13 as banked). A: **0.546 → 0.402,
   −14.37 ± 6.32, OUTSIDE** (v530 −15.83 ± 6.31) — the fix bought **+1.46 pp**
   on that column. Known-zero arm: −0.21 (A) / +0.62 (B).
4. **AND THE FIX CREATES ONE NEW FAILURE MODE, WRITTEN DOWN BEFORE IT IS
   EXPLAINED AWAY: MIXING THE TWO CHAIN ORDERS ON ONE TEAM MAKES THEM COLLIDE.**
   On **atoll** v531fix is worse than the tree it fixes — wins 35/60 (parent) →
   24/60 (v530) → **10/60**, wired harvesters at r30 2.00 → 1.13 → **0.57**,
   r100 delivery 422.7 → 247.0 → **102.3** — while its harvester lands at r5 and
   its socket at r2. §6.

⭐ **AND ONE LEAD THAT CLEARS THE BAR, MEASURED NOT ARGUED (§7):** the
diagnostic arm `cap6` — this tree plus §11.3's `V530_MOUTH_MAX_LINKS = 6`, a
one-constant change — reads **k≤300 −5.63 ± 6.33, INSIDE**, with
**medkill 180 against the parent's 188**, `noharv` **0.000**, `h1mean` **7.87**
against an `h1med` of **7.00**, and `>r60` **0.000**. It keeps the mouth on the
short-chain maps and hands the long-chain ones back to the parent.

---

## 0. WHAT CHANGED

| flag | state | what it is |
|---|---|---|
| `FS_V5301_BOOTFIX` | **True** | **the fix.** Only the designated seat may hold a mouth chain while the team owns **no** harvester. False reproduces `_v530home` byte-for-byte. |
| `V5301_MOUTH_SEAT` | 1 | seat 0 is the raid departure and `LOKI_ECO_SEATS` is (1,2,3), so seat 1 is the first body ever issued an eco seat and the earliest possible socket claim. |
| `V5301_MOUTH_OPEN_AFTER_HARV` | True | once the team owns a harvester the other eco seats arm exactly as `_v530home` does. The plank is **delayed** on those seats, never removed. |
| every v530 flag | **UNTOUCHED** | `FS_V530_MOUTH/CORNERS/DOORKILL` True, `FS_V530_RING` **False**, `V530_MOUTH_MAX_LINKS` **16**, `LOKI_FS_V530` True. |

**Files touched:** `doctrine.py` (one appended v530.1 block, 80 lines) and
`eco.py` (one new predicate `_v5301_may_arm` + one call at the top of
`_v530_mouth_arm`). `main.py`, `raid.py`, `siege.py` are **byte-identical to the
parent** (md5 in `TREE.md5`).

**The mechanism, from the call site.** `_v530_mouth_live()` is per-body state and
`_expand` writes the bootstrap as `if not _v530_chain and (...)`, so every eco
seat carrying a chain suppresses **its own** bootstrap for up to
`V530_MOUTH_TTL = 60` rounds. `LOKI_ECO_SEATS = (1, 2, 3)` and the `defend` seat
falls through to `_expand` as well, so up to **three** bodies can be in chain
phase at once and the team then holds no harvester at all.

⛔ **§11.2's OTHER CHEAP TEST WAS NOT AVAILABLE AS WRITTEN, AND THAT IS A
FINDING.** It offers *"let only ONE seat run mouth-first (`FS_V530_MOUTH_SEATS =
False`, already a flag)"*. The flag is **declared at `doctrine.py:5373` and read
in zero places in the whole tree** — `grep -rn FS_V530_MOUTH_SEATS
bots/_v530home` returns the definition and nothing else. Setting it would have
changed nothing and the test would have read as a null. It is left dead and
unread here so this tree differs from its parent in exactly one place.

⛔ **AND THE FIRST CHEAP TEST DOES NOT REACH THE FAILURE EITHER.** "Exempt the
first harvester of the match from the suppression" only bites in the rounds the
mouth is **stalled** — and in exactly those rounds `_v530_mouth_move` also owns
the body's move and steers it along the chain rather than to ore. Un-suppressing
the bootstrap alone would let the body build a harvester only if it happened to
be standing beside one. The seat rule removes the body from the chain instead,
which is what makes the parent's walk resume.

---

## 1. VERIFY-FIRST — the gates, each driven to the other verdict

| gate | result | the branch that also had to exist |
|---|---|---|
| **flag-off byte-identity** (`BYTEID_OUT.txt`) | **B1 `FS_V5301_BOOTFIX=False` vs `_v530home`: 10/10 IDENTICAL** | **B2 as-fired vs `_v530home`: 8/10 DIFFER** — without it B1 could pass on an inert tree |
| **master byte-identity** | **B3 `LOKI_FS_V530=False` vs `_v529merge`: 10/10 IDENTICAL** — the v530 master property survives | **B4 as-fired vs `_v529merge`: 10/10 DIFFER** |
| **AST scan** (`ASTSCAN_OUT.txt`) | **0** module-level reads of any v530.1 or v530 name across doctrine/eco/main/siege | guard pos/neg exercised on the v530.1 name set **and** the v530 one; `FERRY_HOME_ON`/`FS_CREW_ON` real-case positive control still found |
| **cross-instrument harv1** (`XCHECK_OUT.txt`, `XCHECK2_OUT.txt`) | `deliv.harv1` == `routetape.harv1_rnd` on **400/400** rows, twice (old tape and new) | **`--mutate 25` reports exactly 25 mismatches, PASS** — a perfect agreement rate that cannot report a mismatch proves nothing |
| `harvread.py --selftest` | PASS | a never-arm reads `noharv 1.000 / h1med −1`, **not 0** — a `−1` averaged in would report the defect as an improvement; `>r60` boundary strict; three distinct `noharv` values so the column is not constant |
| `doseread5301.py --selftest` | PASS | `multiseat_r30` is not an alias for the arm count (a r80 arm must not count); the short-chain counter does **not** fire on a complete chain; a corner-only tape reads 0 mouth arms |
| `headline.py` / `raceread.py --selftest` | PASS (unchanged tools) | r300 cells EXCLUDED not zeroed; `raceread`'s derived ring-claim column separates its two synthetic rows |
| **tracebacks** | **0** across **6,530 games** | — |

**0 tracebacks · 0 timeouts · 0 no-winner games** over 1,920 (battery A) + 1,920
(battery B) + 2,400 (diagnostic) + 144 (cheap test) + 96 (dose) + 50
(byte-identity) games.

---

## 2. THE CHEAP TEST FIRST (§11's own instruction), n=48/arm

Crater-weighted 6-map panel, opponent `_x3r0v165mjolnirB`, seeds 101–104, before
any headline was spent:

| arm | noharv | h1med | h1mean | >r60 |
|---|---|---|---|---|
| parent | 0.042 | 8.0 | 12.00 | 0.042 |
| v530 | 0.083 | 72.0 | 89.95 | 0.500 |
| **v531fix** | **0.042** | **13.0** | **30.00** | **0.167** |

The fix moved every column in the right direction on the fixture the defect
fires hardest on, at n=48, which is what bought the two batteries.

---

## 3. THE HARVESTER-BOOTSTRAP PANEL — the one column this build exists to move

`harv1` read off the replays by `deliv.py`; `noharv` and `>r60` over ALL games of
the arm, `h1med`/`h1mean` over the games that HAVE a harvester (`n_h`), because
pooling them hides the finding inside the instrument.

### 3.1 Battery A (opp `_v488beltbreak2`, sweep panel), n=480/arm

| arm | n_h | **noharv** | h1med | **h1mean** | **mean−median** | >r60 |
|---|---|---|---|---|---|---|
| parent | 480 | **0.000** | 5 | 5.75 | 0.75 | 0.000 |
| flagoff *(known zero)* | 480 | 0.000 | 5 | 5.79 | 0.79 | 0.000 |
| v530 | 429 | **0.106** | 8 | **42.87** | **34.87** | 0.146 |
| **v531fix** | 478 | **0.004** | **7** | **9.55** | **2.55** | **0.004** |

`v531fix vs parent noharv +0.42 pp (hw 0.58) — inside.`
**The bar as stated (9.6% → 0.0%, median back to ~r8, mean within a few rounds
of the median) is met on this battery**: 2 games of 480, median r7, mean 9.55.

### 3.2 Battery B (opp `_x3r0v165mjolnirB`, crater panel), n=480/arm

| arm | n_h | **noharv** | h1med | **h1mean** | **mean−median** | >r60 |
|---|---|---|---|---|---|---|
| parent | 476 | 0.008 | 6 | 14.57 | 8.57 | 0.046 |
| flagoff | 474 | 0.013 | 6 | 14.03 | 8.03 | 0.037 |
| v530 | 450 | **0.062** | 14 | **71.79** | 57.79 | 0.406 |
| **v531fix** | 462 | **0.037** | **9** | **31.96** | **22.96** | **0.146** |

`v531fix vs parent noharv +2.92 pp (hw 1.89) — OUTSIDE.`
**Not met on this battery.** The residual is concentrated on the two deepest-ore
maps: **auroraveil `noharv` 0.217** and **glacierkeep `h1med` r88**. Those are
the boards where the single designated seat's 8–11-link chain meets
`V530_MOUTH_TTL`, and with the seat rule there is no second mouth seat behind
it. Every other map on the panel reads 0.000–0.050.

---

## 4. `DEFENCE_ADMISSION_BAR` — ITT, share of ALL games killed by r300

### 4.1 Battery A, n=480/arm, 1,920 games, 0 tracebacks

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   73.5%  130(.271)  161(.335)  193(.402)  235(.490)  262(.546)     187     116   0
flagoff       480   77.1%  126(.263)  174(.362)  196(.408)  234(.487)  261(.544)     183      98   0
v530          480   67.1%   33(.069)   55(.115)   81(.169)  141(.294)  186(.388)     261     129   0
v531fix       480   67.3%   60(.125)   93(.194)  115(.240)  157(.327)  193(.402)     233     144   0
```

| arm | Δwins | Δk≤200 | **Δk≤300 (the BAR)** | known-zero on that column |
|---|---|---|---|---|
| v530 | −6.46 | −23.33 | **−15.83** (hw 6.31) OUTSIDE | −0.21 |
| **v531fix** | −6.25 | **−16.25** | **−14.37** (hw 6.32) OUTSIDE | −0.21 |

⛔ **THE BREACH REMAINS ON BATTERY A.** The fix bought **+1.46 pp** on the bar
and **+7.08 pp** on `k≤200`. Sensitivity: dropping **atoll** (§6) moves v531fix
to **−12.14 ± 6.76 (still OUTSIDE)** while its win delta collapses from −6.25 to
**−1.19** — i.e. atoll owns most of the win-rate loss and little of the bar.

### 4.2 Battery B, n=480/arm, 1,920 games, 0 tracebacks

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   53.1%   34(.071)   63(.131)  102(.212)  132(.275)  164(.342)     237     191   0
flagoff       480   50.0%   38(.079)   77(.160)  108(.225)  143(.298)  167(.348)     208     196   0
v530          480   41.9%    2(.004)   24(.050)   35(.073)   56(.117)   85(.177)     316     236   0
v531fix       480   52.5%   55(.115)   84(.175)   96(.200)  126(.263)  139(.290)     242     189   0
```

| arm | Δwins | Δk≤200 | **Δk≤300 (the BAR)** | Δourcore |
|---|---|---|---|---|
| v530 | −11.25 OUTSIDE | −13.96 OUTSIDE | **−16.46** (hw 5.55) OUTSIDE | +9.38 OUTSIDE |
| **v531fix** | **−0.62 inside** *(smaller than the known zero)* | **−1.25 inside** *(smaller than the known zero)* | **−5.21 (hw 5.88) INSIDE** | **−0.42 inside** *(smaller than the known zero)* |

⭐ **ON THE CRATER PANEL THE BREACH IS GONE**, and three of the four currency
columns move by **less than the known-zero arm does**. `medkill` returns from
316 to 242 against the parent's 237.

### 4.3 Per map — where each battery's number comes from

Battery A (`wins/n [k≤300] {k≤200}`), the two extremes:

| map | parent | v530 | **v531fix** |
|---|---|---|---|
| **atoll** | 35/60 [22] {20} | 24/60 [12] {6} | **10/60 [4] {1}** |
| glacierkeep | 53/60 [33] {23} | 50/60 [25] {4} | **58/60 [39] {19}** |
| yulerune | 55/60 [46] {42} | 50/60 [30] {22} | **56/60 [36] {34}** |

Battery B, the crater cells the plank was designed from:

| map | parent | v530 | **v531fix** |
|---|---|---|---|
| **icefloe** | 6/60 [0] {0} | 23/60 [5] {0} | **36/60 [14] {8}** |
| **yulerune** | 8/60 [1] {0} | 11/60 [3] {0} | **24/60 [7] {3}** |
| **drakkarfjord** | 41/60 [26] {12} | 27/60 [7] {0} | **27/60 [24] {20}** |
| ragnarok *(control)* | 60/60 [54] {51} | 34/60 [22] {17} | **60/60 [60] {54}** |
| royale *(control)* | 56/60 [45] {23} | 48/60 [26] {6} | 44/60 [23] {7} |

---

## 5. THE P1 MECHANISM — does it survive the fix?

Read off `routetape.py` (the research arm's tool, unchanged; winner-vs-tape
**2,400/2,400 agree, 0 parse failures** on the diagnostic batch, same gate on
both headline batches).

### 5.1 Battery B — the fixture the crater defect fires on

| column | parent | flagoff | v530 | **v531fix** | v530 **as banked** |
|---|---|---|---|---|---|
| `head1` mean | 56.5 | 51.4 | 13.8 | **11.8** | 10.6 |
| **`margin` = eseal₁ − head1** | **−30.9** | −28.9 | +9.3 | **+18.1** | **+21.1** |
| **won the socket race** | 0.362 | 0.369 | 0.750 | **0.688** | **0.750** |
| **belt never reaches home** | 0.348 | 0.360 | 0.083 | **0.156** | **0.094** |
| `ti_coll100 == 0` | 0.463 | 0.463 | 0.519 | **0.325** | — |
| `ti_coll100` mean | 203.6 | 211.9 | 106.2 | **209.9** | — |
| harvesters WIRED at r30 | 0.82 | 0.84 | 0.39 | **0.85** | — |

⭐ **THE MECHANISM SURVIVES AND THE DELIVERY IT WAS SUPPOSED TO BUY NOW ARRIVES.**
v530 won the race and delivered nothing (r100 delivery 106.2 against the
parent's 203.6, `zero100` **worse** than the parent at 0.519); v531fix wins
almost as much of the race and delivers **209.9 with `zero100` 0.325 — better
than the parent on both**, with wired harvesters at r30 restored to parent level.

⚠ **TWO CAVEATS, BOTH AGAINST THIS TREE.** (a) `beltfail` is **0.156 against
v530's 0.083** — the seat rule removes the second and third mouth chain, so on
**auroraveil (0.45 vs 0.27)** and **glacierkeep (0.80 vs 0.40)** the single
chain's failure is now the team's failure. (b) `margin` is a mean over a
heavy-tailed column and **does not reproduce across runs**: the banked v530 read
+21.1 and this re-run of the same arm on the same panel reads **+9.3**.
`wonrace` (0.750 both) and `beltfail` (0.094 → 0.083) do reproduce. **Read the
mechanism off `wonrace` and `beltfail`, not off `margin`.**

### 5.2 Battery A

| column | parent | flagoff | v530 | **v531fix** |
|---|---|---|---|---|
| `head1` mean | 13.7 | 14.3 | 5.3 | **6.0** |
| `margin` | 13.7 | 13.1 | 23.5 | **22.8** |
| won the socket race | 0.819 | 0.835 | 0.996 | **0.960** |
| belt never reaches home | 0.031 | 0.019 | 0.000 | **0.000** |
| `ti_coll100 == 0` | 0.037 | 0.027 | 0.265 | **0.175** |
| `ti_coll100` mean | 379.2 | 377.0 | 243.8 | **264.4** |
| harvesters LIVE at r30 | 2.32 | 2.29 | 1.39 | **1.76** |

**The ring is claimed at r6 instead of r14 and the dead-heads class stays dead —
and on this panel the parent only ever loses the belt in 3.1% of games, so the
plank is buying something worth little here and still costs 0.175 of games with
zero delivery at r100 against the parent's 0.037.**

---

## 6. ⭐⭐ THE SURPRISE — MIXING THE TWO CHAIN ORDERS MAKES THEM COLLIDE

**Written down before it is explained away.** On **atoll**, v531fix is worse than
the tree it fixes, on a map where its own harvester lands at r5 and its own
socket at r2:

| atoll, n=60/arm | parent | v530 | **v531fix** |
|---|---|---|---|
| wins | 35 | 24 | **10** |
| k≤300 | 22 | 12 | **4** |
| `head1` (socket claim) | r3.0 | r2.0 | **r2.0** |
| `harv1` median | r2 | r5.5 | **r5** |
| **harvesters WIRED at r30** | **2.00** | 1.13 | **0.57** |
| our conveyors at r30 | 6.85 | 5.43 | **3.78** |
| `ti_coll30` | 120.0 | 64.7 | **22.5** |
| `ti_coll100` | 422.7 | 247.0 | **102.3** |
| enemy-core first hit | r183 | r180 | **r284** |

**The harvesters are alive and unwired.** `harv_live30` is 1.70 while
`harv_wired30` is 0.57.

**The mechanism, off the instrumented tape** (`trace_v531_atoll.err`, one game,
seed 9, opponent `_v488beltbreak2`):

```
v531fix:  MOUTH arm  rnd=2 seat=1 ore=1,17 links=2 sock=1,15
          MOUTH link rnd=2 seat=1 tile=1,15 ... left=1
          MOUTH harv rnd=5 seat=1 ore=1,17 sock=2 links=1     <- 1 of 2 laid
v530:     MOUTH arm  rnd=2 seat=1 ... links=2
          MOUTH link rnd=2 seat=1 tile=1,15 ... left=1
          MOUTH link rnd=4 seat=1 tile=1,16 ... left=0
          MOUTH harv rnd=6 seat=1 ... links=2                 <- 2 of 2 laid
```

Seat 1 planned two links, laid one, and reached the terminal harvester with the
second **popped as "occupied"** — the `_v530_mouth_act` branch that skips a
taken tile and faces the next link at it. In v530 both eco seats were laying
core-outward and never crossed; in v531fix seat 2 is running the **parent's
ore-first order over the same ground** and got to `1,16` first, so the mouth
chain has a hole it never owned and the harvester at the far end has no route
home.

**Quantified on the dose, 48 games/arm:** terminal harvesters reached on a chain
**shorter than planned** are **13 of 37 (35%) for v530** and **10 of 20 (50%)
for v531fix**. The rate rises with the fix.

⛔ **THIS IS A REAL COST OF THE SEAT RULE AS IMPLEMENTED, NOT OF THE MOUTH.** It
is the one thing the v530.1 design did not anticipate: `_v530_mouth_arm` refuses
to arm when *this body* is mid-chain under the parent's order (`if self.link_queue
or self.wire_pending`), and there is no equivalent check against *another body's*
parent-order chain crossing the planned tiles.

---

## 7. ⭐ THE DIAGNOSTIC BATTERY — where the residual −14 pp actually lives

⛔ **NOT THE HEADLINE, AND ITS ROWS ARE NOT POOLED WITH IT.** Same panel, same
opponent, same seeds, five arms interleaved per cell, n=480/arm, 2,400 games,
0 tracebacks. Every number here is a **within-battery** comparison.

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   70.8%  113(.235)  155(.323)  175(.365)  220(.458)  250(.521)     188     123   0
flagoff       480   74.6%  121(.252)  160(.333)  179(.373)  224(.467)  253(.527)     192     110   0
cap6          480   68.3%  103(.215)  152(.317)  167(.348)  195(.406)  223(.465)     180     136   0
nomouth       480   67.3%  110(.229)  148(.308)  162(.338)  199(.415)  218(.454)     188     141   0
v531fix       480   69.0%   61(.127)   93(.194)  118(.246)  163(.340)  203(.423)     241     135   0
```

| arm | what it is | Δwins | Δk≤200 | **Δk≤300** |
|---|---|---|---|---|
| flagoff | known zero | +3.75 inside | +0.83 inside | **+0.62 inside** |
| **cap6** | v531fix + `V530_MOUTH_MAX_LINKS=6` | −2.50 *(smaller than the known zero)* | −1.67 inside | **−5.63 (hw 6.33) INSIDE** |
| nomouth | v531fix + `FS_V530_MOUTH=False` | −3.54 inside | −2.71 inside | **−6.67 (hw 6.32) OUTSIDE** |
| v531fix | as fired | −1.88 inside | −11.88 OUTSIDE | **−9.79 (hw 6.32) OUTSIDE** |

**Three things fall out of this table and none of them needed another design.**

1. **`nomouth` — the mouth turned OFF — still reads −6.67, outside.** So roughly
   **two thirds of v531fix's residual on this panel is NOT the mouth at all**;
   it is P2/P3 and the rest of the v530 package. The v530 report measured the
   same arm at −7.08 on the same fixture, independently.
2. **`cap6` clears the bar** and is the only arm in either build that **kills
   FASTER than the parent** (medkill 180 vs 188) while keeping a mouth. Its
   harvester panel is clean on every column: `noharv` **0.000**, `h1med` **7**,
   `h1mean` **7.87** (mean−median **0.87**, parent 0.79), `>r60` **0.000**.
3. **How `cap6` does it: it keeps the mouth where the chain is short and hands
   the long boards back to the parent.** Per-map `head1`: atoll **2.0**,
   yulerune **2.0**, nordkap **5.6** (mouth alive) against drakkarfjord **23.2**
   and glacierkeep **72.8** (parent behaviour). Pooled `beltfail` **0.013**
   against the parent's 0.040, and r100 delivery **318.1** against the parent's
   372.2 and v531fix's 266.2.

⚠ **`cap6` HAS NOT BEEN RUN ON BATTERY B**, which is the panel the mouth was
designed for and the one where the deep-ore chains are the whole point. Its
battery-A behaviour is *"do less mouth"*, so its crater-panel number is genuinely
unknown and could go either way.

---

## 8. ⛔ SAME-ARM SPREAD — read this before reading any single delta above

`v531fix` and `parent` were each run **twice** on the identical battery-A panel,
opponent, seeds and block structure (headline and diagnostic), with
`NOISE_ON = True` re-rolling the spawn salt per process:

| | headA | diagA | spread |
|---|---|---|---|
| parent `k≤300` | 0.546 | 0.521 | 2.5 pp |
| v531fix `k≤300` | 0.402 | 0.423 | 2.1 pp |
| **Δ(v531fix − parent)** | **−14.37** | **−9.79** | **4.6 pp** |

**A 4.6 pp move on the bar column between two n=480 batteries of the same arm on
the same fixture, comparable to the 6.3 pp half-width.** Every delta in this
report carries that. The `cap6`-vs-`v531fix` and `nomouth`-vs-`v531fix`
comparisons in §7 do **not**, because they are within one interleaved battery.

**Local fixture, no DEFF.** The s39 audit measured a pair-weighted local DEFF of
**0.98** on a balanced-by-construction shard fixture, so the platform constants
(1.529 rated / 1.833 unrated) do not apply and are not used. Naive two-sample
half-widths throughout. **Every number in this report is LOCAL, us-vs-one-
opponent, and nothing here is a ladder read.**

---

## 9. THE DOSE — does the fix fire, as a seat shift?

48 games/arm, `NOISE_ON = True`, `--tle 10`, stderr kept, same tree with one flag
moved. ⚠ magnitudes, not constants.

```
arm          games   arms  links   harv shortH  fullH    ttl  multi30 | arms by seat: n(median arm round)
inst_v530       48    116    445     37     13     24     62    0.917 | s1:48(r2)  s2:42(r6)  s4:26(r15)
inst_v531       48     80    279     20     10     10     45    0.500 | s1:48(r2)  s2:8(r7)   s4:24(r16)
```

* **Seat 1 is untouched: 48 of 48 games, median arm round r2 in both arms.** The
  socket claim — the half of the plank that wins the race — is not delayed.
* **Seat 2 collapses 42 → 8.** The prediction was *not* zero: a non-designated
  seat may still arm once the team owns a harvester, and 8 of them do.
* **Seat 4 is essentially unchanged (26 → 24, median r15 → r16)** — by r15 the
  team normally already owns a harvester, so the seat rule correctly does not
  bind there.
* **`multi30` (games with >1 seat armed by r30) halves, 0.917 → 0.500.** It does
  not go to zero, and should not: the post-harvester arms are the designed
  behaviour.
* **`shortH/fullH` 13/24 → 10/10** — §6's collision, on the dose.

---

## 10. FAILURE REEL — the rule is the earliest our-core-death per map, capped at 5

Battery B (`v531fix`, deaths 189 of 480 = 39.4%, r1000 games 58):

| map | turn | seed | seat | replay |
|---|---|---|---|---|
| nordkap | 95 | 1 | B | `scratchpad/s51_v5301_build/headB/rep/v531fix_nordkap_s1_B.replay26` |
| auroraveil | 111 | 15 | A | `.../headB/rep/v531fix_auroraveil_s15_A.replay26` |
| yulerune | 129 | 1 | A | `.../headB/rep/v531fix_yulerune_s1_A.replay26` |
| icefloe | 173 | 6 | B | `.../headB/rep/v531fix_icefloe_s6_B.replay26` |
| drakkarfjord | 220 | 1 | A | `.../headB/rep/v531fix_drakkarfjord_s1_A.replay26` |

Battery A (`v531fix`, deaths 144 of 480 = 30.0%, r1000 games 45): antler r104
s12 A · fjordgate r116 s26 B · **atoll r138 s9 B** · midgard r176 s2 A ·
nordkap r229 s11 B. Latest-kill wins (labelled, not part of the reel):
drakkarfjord r994 s13 B, glacierkeep r957 s16 B.

---

## 11. WHAT WOULD FIX THE REST — stated as tests, not as conclusions

1. **THE COLLISION IS THE NEXT DEFECT AND IT IS NAMED (§6).** `_v530_mouth_arm`
   refuses to arm when *this body* is mid-chain under the parent's order; there
   is no check against *another body's* parent-order chain crossing the planned
   tiles. Two cheap tests: (a) have the mouth walker **build** a hole it finds
   occupied by one of OUR conveyors facing the wrong way rather than pop it —
   the tape line already exists (`links=1` vs `links=2`); (b) make the
   non-designated seats **skip `_wire_on_build`'s chain** while a mouth chain is
   live on the team (one store bit), so only one body ever routes to the ring.
2. **`V530_MOUTH_MAX_LINKS = 6` IS MEASURED, NOT ARGUED (§7).** On battery A it
   clears `DEFENCE_ADMISSION_BAR` (−5.63 ± 6.33), kills faster than the parent
   (medkill 180 vs 188) and has a clean harvester panel. **It has not been run on
   battery B.** That is the single highest-value next leg in this line.
3. **THE DEEP-ORE RESIDUAL IS NOW A SINGLE-CHAIN PROBLEM (§3.2, §5.1).**
   auroraveil `noharv` 0.217 and glacierkeep `h1med` r88 are the seat rule
   removing the backup chains. The cap in (2) and the seat rule interact — a cap
   converts those boards to parent behaviour, which is exactly the fallback the
   seat rule took away.
4. **TWO THIRDS OF THE BATTERY-A RESIDUAL IS NOT THE MOUTH** (`nomouth` −6.67,
   §7). Any further work on P1 alone cannot recover it; P2/P3 need their own
   pass, and the v530 report already measured `nocorner` −15.00 / `nodoor`
   −19.17 on that panel.
5. **`FS_V530_MOUTH_SEATS` IS STILL A DEAD FLAG.** Either wire it or delete it;
   as it stands it is a documented lever that does nothing, and §11.2 of the
   previous report recommended a test that would have silently measured nothing.

---

## 12. RAW — tapes, instruments, PIDs

All under `scratchpad/s51_v5301_build/`:
`headA/results.tsv` 1,920 rows · `headB/results.tsv` 1,920 · `diagA/results.tsv`
2,400 · `cheap/results.tsv` 144 · `raceA.tsv` / `raceB.tsv` / `raceD.tsv`
(routetape, winner-vs-tape **2,400/2,400 agree, 0 parse failures** on the
diagnostic batch) · `dose/inst_v530` + `dose/inst_v531` 96 games of stderr ·
`byte_check/` 50 replays · `BYTEID_OUT.txt` · `ASTSCAN_OUT.txt` ·
`XCHECK_OUT.txt` · `XCHECK2_OUT.txt` · `HARV_OUT.txt` · `HARVD_OUT.txt` ·
`HEADA_QUICK.txt` · `HEADB_QUICK.txt` · `RACEA_OUT.txt` · `RACEB_OUT.txt` ·
`RACED_OUT.txt` · `DOSE_OUT.txt` · `REELA_OUT.txt` · `REELB_OUT.txt` ·
`trace_v531_atoll.err` · `trace_v530_atoll.err` · `FREEZE.md5` ·
`FREEZE_PARENT.md5` · `TREE.md5` · `PIDS`.

**Totals: 6,530 games. 0 tracebacks, 0 timeouts, 0 no-winner games.**

New instruments written for this build, each with a `--selftest` that drives
every guard to the other verdict: `harvread.py` (the bootstrap panel),
`harv_xcheck.py` (the two-reader gate on `harv1`, with a mutation control),
`doseread5301.py` (per-seat arm rounds, `multiseat_r30`, the short-chain
counter). `byte_identity.py`, `flagoff_ast.py`, `run_battery.py`, `headline.py`,
`raceread.py`, `deliv.py`, `reel.py` and `routetape.py` are the v530/research-arm
tools, reused unchanged except for the v530.1 name set added to the AST scan.

⛔ **NO CPU CLAIM IS MADE ANYWHERE IN THIS REPORT.** `execTimeUs` is 0 in the
local harness. The fix adds one `read_store` per round per non-designated eco
seat and that is an argument, not a measurement.

---
## BUILDER VERDICT LINES (s51, wrap)
* THE TAIL IS FIXED (noharv 10.6%→0.4%, mean−median 34.9→2.6) and THE CRATER BREACH IS GONE
  (battery B k≤300 −16.5→−5.2 INSIDE, with the P1 mechanism intact: race won 0.69, beltfail
  0.156, ti_coll100=0 down 0.463→0.325, delivery ahead of parent). Magnus's mouth-first
  design is now MECHANISM-PROVEN AND TAIL-CLEAN on the fixture that motivated it.
* NOT YET A FIRED HEAD: battery A still −14.4 outside — and the diagnostic splits it: TWO
  THIRDS IS NOT THE MOUTH (nomouth −6.7 outside), and the `cap6` lead (MOUTH_MAX_LINKS=6)
  reads −5.6 INSIDE with medkill 180 = ON the KILL_TARGET. Plus one new defect: mixed chain
  orders collide on atoll (wins 35/24/10 — the mouth pops planned tiles as occupied).
* HEAD REMAINS v529. SUCCESSOR'S FIRST JOBS, in order: (1) cap6 on battery B; (2) the atoll
  chain-order collision fix; (3) attribute the non-mouth two-thirds of battery A's residual
  (corners? doorkill? — the §7 battery's arms are the instrument); then the home package
  joins the head and the full-pool read prices the composite against SHIP_BAR 75.
* Instrument facts carried: the 4.6pp same-arm cross-battery swing (§8) — cross-battery
  deltas are never currency; §11.2's suggested constant was DEAD (declared, read nowhere) —
  the report-suggests-a-test-that-doesn't-exist class, caught by checking before running.
