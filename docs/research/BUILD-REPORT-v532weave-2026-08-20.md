# BUILD REPORT — `bots/_v532weave` (v532), s52, 2026-08-20

**ONE DEFECT, ONE BAN SET — AND THE DEFECT IS NOT THE ONE THE BRIEF NAMED.**
`BUILD-REPORT-v531fix-2026-08-20.md` §6 measured that on **atoll** `_v531fix`
wins 10/60 against its parent's 35/60, with `harv_wired30` **0.57** against
**2.00**, and diagnosed it as *"seat 2 runs the PARENT's ore-first build order
over the same ground and occupies a planned mouth tile first"*. **That
diagnosis is falsified on the engine.** The collision is **P1 (the mouth chain)
against P2 (our own corner barriers)** — two v530 planks, on our own core ring,
one round apart. §1 is the falsification; the fix follows from it and is
14 functional lines.

Parent `bots/_v531fix`, **md5-frozen and verified byte-unchanged at
`09:20:22Z`** (`scratchpad/s52_v532_build/TREE.md5`) — this build never wrote to
`bots/_v531fix` or to `scratchpad/s51_v5301_build`, both of which were being
read by a running battery (PID 73841, `scratchpad/s52_diagB/drive_diagB.sh`,
alive throughout). `PAR=3` throughout (that battery held `PAR=4` on a 10-core
box); PIDs in `scratchpad/s52_v532_build/PIDS`. Wall clock from `date -u` in
the same shell call: probe `09:02:55–09:05:43Z`, tree final `09:08:20Z`,
byte-identity `09:10:09–09:12:22Z`, AST/read-site `09:12:47–09:13:22Z`, dose
`09:14:29–09:15:48Z`, atoll grid `09:16:38–09:19:27Z`, readout `09:19:55Z`,
report `09:21:16Z`.

---

## ⛔ TOP LINE — FOUR SENTENCES

1. **§6's MECHANISM IS WRONG AND THE REPLACEMENT IS DETERMINISTIC.** Instrumented
   `_v531fix`, atoll, 30 games, every occupied-pop classified: **58 benign**
   (our conveyor already facing the way we wanted — that tile carries the flow),
   **30 our own BARRIER**, **0 enemy anything**, **0 wrong-facing conveyor** —
   and **30 of 30** of those barrier tiles are a tile our own `V530 CORNER`
   line built **one round earlier**, in every game of the 30. The parent's
   ore-first chain does not hit this at all (52 pops over 10 games, **0** our
   barriers), because it plans *after* the barrier exists and `_link_path`
   already blocks it. **It is a plan-time race, not a build-order conflict.**
2. **THE FIX IS "PLAN AS IF THE CORNERS WERE ALREADY BUILT" AND THE DOSE READS
   ZERO.** Chains that reached their terminal harvester carrying a hole:
   **7 of 17 (41.2%) → 0 of 17 (0.0%)**, 48 games/arm, same tree, one flag
   moved. §6's own counter (`shortH`, which cannot go to zero because adoption
   is legitimate) reads **9/17 (52.9%) → 1/17 (5.9%)** with the control
   reproducing §6's ~50% as the positive control. **Our-own-barrier pops:
   9 → 0.**
3. **THE ATOLL RECOVERY IS MOST OF THE WAY BACK.** n=60/arm, interleaved,
   opponent `_v488beltbreak2`: wins **parent 30 · v531fix 19 · v532weave 27**;
   `harv_wired30` **2.00 · 0.62 · 1.70**; `ti_coll100` **422.8 · 133.0 ·
   349.3**. vs parent, `Δwins` **−18.33 pp (hw 17.28) → −5.00 pp (hw 17.85)**.
   **Mechanism check, not currency** — one map, one opponent.
4. **AND IT COSTS ALMOST NOTHING ELSEWHERE, WHICH IS ALSO A WARNING.** The
   fix changes the replay in **3 of 10 byte-identity cells** (atoll A, atoll B,
   yulerune B) and leaves the other 7 byte-identical — it bites exactly where a
   corner sits on the mouth's route. **That surgical scope is the reason no
   claim is made here about the `DEFENCE_ADMISSION_BAR` batteries: this build
   did not run them.**

⚠ **WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY (§7):** hole-class pop *events*
did **not** all disappear — 13 → 9 — and on **nordkap** they went **1 → 5**,
all on chains that never reached a harvester, all of them our own TURRETS and
enemy barriers rather than corners. n=3 games per cell. Unexplained.

---

## 0. WHAT CHANGED

| flag | state | what it is |
|---|---|---|
| `FS_V532_WEAVE` | **True** | **the fix.** `_v530_mouth_arm` plans its chain with the 4 diagonal core corners treated as WALL, when — and only when — `FS_V530_CORNERS` is the plank that will take them. False reproduces `_v531fix` byte-for-byte. |
| every v530.1 flag | **UNTOUCHED** | `FS_V5301_BOOTFIX` True, `V5301_MOUTH_SEAT` 1, `V5301_MOUTH_OPEN_AFTER_HARV` True. |
| every v530 flag | **UNTOUCHED** | `FS_V530_MOUTH/CORNERS/DOORKILL` True, `FS_V530_RING` **False**, `V530_MOUTH_MAX_LINKS` **16**, `LOKI_FS_V530` True. |

**Files touched:** `doctrine.py` (one appended v532 block, 70 lines: 69 comment
+ `FS_V532_WEAVE = True`) and `eco.py` (**+74 / −7** lines, of which **26 are a
stderr instrument behind `FS_V530_LOG`** and most of the rest are comment).
`main.py`, `raid.py`, `siege.py` are **byte-identical to the parent**
(`TREE.md5`).

**THE FUNCTIONAL CHANGE IS FOUR EDITS:**

1. `_link_path(self, ct, hpos)` → `_link_path(self, ct, hpos, extra_block=None)`.
   `extra_block` is an optional `(x, y)` set the flood treats as WALL, applied
   in **both** branches (the `map_grid` reverse-BFS and the unknown-map forward
   BFS), and **never applied to the start tile** — re-blocking the harvester's
   own tile would make the flood unreachable rather than re-routed. Default
   `None` is the parent flood exactly; every parent call site passes nothing.
2. `_v530_corner_act`'s corner-key computation factored out into
   `_v530_corner_key_set()`, so the planner and the builder read the corner set
   from one source of truth. Behaviour-preserving (and proved so in §2 C1).
3. `_v530_mouth_arm` passes `self._v530_corner_key_set() or None` when
   `FS_V532_WEAVE and FS_V530_CORNERS`.
4. The classified `MOUTH occ` stderr line, **behind `FS_V530_LOG` (False in the
   shipped default)** — the instrument that falsified §6, kept in the tree so
   the dose is reproducible from the shipped code rather than from a patch.

**WHY NOT THE OTHER TWO CANDIDATES.**

* **RESERVATION (publish the planned tiles through the comms store) is not
  available.** All **16** slots are already assigned in this tree
  (`SLOT_ROLE_N`…`SLOT_SIEGE`, plus the v-era aliases `SLOT_FWD_GUN`,
  `SLOT_FERRY_ID/RND`, `SLOT_RAID_N/LIVE`, `SLOT_BELTBREAK`, `SLOT_FS`,
  `SLOT_SENT_BEAT`), so a reservation channel means sharing bits with a live
  slot. And it could not work anyway: **store writes are buffered one round**,
  the mouth plans at r2 and the corner lands at r3, so a claim written at r2 is
  visible to the corner builder at r3 **at the earliest** — the same race, one
  layer down. The v530.1 doctrine block already records this argument for the
  seat rule (`V5301_MOUTH_SEAT`, "a claim written by seat 1 is not yet visible
  when seat 2 first runs"); it applies here verbatim.
* **ADOPT-OR-REFACE (v531fix §11.1(a)) fixes a case that does not occur.**
  **Adoption is already what the code does** — the occupied branch pops the
  tile into `mouth_prev`, so the next link is faced at it — and §1's 58
  conveyor pops show it working: **every one was already facing the way we
  wanted, and zero were wrong-facing.** The case it does not cover is a tile
  that cannot carry flow *at all*, and for a BARRIER "reface" means
  destroy-and-rebuild: 3 Ti, an action, and a standing fight with the plank
  that wants that tile (`_v530_corner_act` counts LIVE corners, so a destroyed
  one re-opens and is rebuilt). **Not planning through it costs nothing and
  cannot ping-pong.**

---

## 1. VERIFY-FIRST — THE DEFECT, MEASURED BEFORE ANYTHING WAS DESIGNED

Instrument: `scratchpad/s52_v532_build/probe531` = `_v531fix` + `FS_V530_LOG`
+ a `MOUTH occ` line naming the occupier's **owner, entity type, facing**, and
the facing the link was going to be built with. atoll, **30 games** (seeds
1–15 × both seats), opponent `bots/_v488beltbreak2`.

### 1.1 Every occupied-pop the mouth took, classified

| class | n | can it carry the chain's flow? |
|---|---|---|
| **OURS, CONVEYOR, `dir == want`** | **58** | **yes** — a conveyor accepts from 3 sides and outputs to the 4th; this tile is the link |
| **OURS, BARRIER** | **30** | **no** — a hole |
| OURS, CONVEYOR, wrong facing | 0 | — |
| enemy anything | 0 | — |

**30 of 30 barrier tiles are a tile a `V530 CORNER` line built one round
earlier** — corner at **r3**, mouth wants it at **r4**, in **every game of the
30**. Worked example, seed 1 seat A, verbatim:

```
V530 MOUTH arm  rnd=2 seat=1 ore=1,17 links=2 sock=1,15
V530 MOUTH link rnd=2 seat=1 tile=1,15 face=EAST left=1
V530 CORNER     rnd=3 seat=2 tile=1,16 held=1              <- P2 takes the tile
V530 MOUTH occ  rnd=4 seat=1 tile=1,16 mine=1 et=BARRIER dir=NONE want=NORTH
V530 MOUTH harv rnd=5 seat=1 ore=1,17 sock=2 links=1       <- 1 of 2 laid
```

Core anchored at (2,14) ⇒ corners {(1,13),(4,13),(1,16),(4,16)} — **(1,16) is a
corner**, and it is the only tile between the ore at (1,17) and the socket at
(1,15). The harvester at (1,17) ends the game with **no acceptor on any side**.

### 1.2 The control that makes it a diagnosis rather than an anecdote

Same instrument, a `PARENT occ` line on `_build_next_link`'s identical pop
branch, atoll, **10 games**: **52 pops, and not one of them is a barrier of
ours.**

| class | n |
|---|---|
| OURS, CONVEYOR | 41 |
| **ENEMY, BARRIER** | **9** |
| OURS, GUNNER | 1 |
| OURS, SENTINEL | 1 |
| **OURS, BARRIER** | **0** |

**That asymmetry is the whole mechanism.** `_link_path` already blocks friendly
non-`BELT_TYPES` buildings it can see, so a chain planned **after** the corner
exists routes around it by construction. The mouth is the **only** planner that
runs at r2, before its own team's r3 build. And the v530.1 seat rule is what
exposed it: under `_v530home` seat 2 was laying its own mouth chain at r2–r6
and never stood beside a corner; under the seat rule seat 2 is free, walks the
ring, and builds the corner that kills seat 1's chain. **v530 measured
`harv_wired30` 1.13 on atoll and v531fix 0.57 — the fix to one plank uncovered
the collision with another.**

---

## 2. THE GATES, EACH DRIVEN TO THE OTHER VERDICT

| gate | result | the branch that also had to exist |
|---|---|---|
| **flag-off byte-identity** (`BYTEID_OUT.txt`) | **C1 `FS_V532_WEAVE=False` vs `_v531fix`: 10/10 IDENTICAL** | **C2 as-fired vs `_v531fix`: DIFFER 3/10** — without it C1 could pass on an inert tree |
| **v530.1 chain byte-identity** | **C3 `WEAVE=False`+`BOOTFIX=False` vs `_v530home`: 10/10 IDENTICAL** | (C2 is the shared negative control) |
| **v530 master byte-identity** | **C4 `LOKI_FS_V530=False` vs `_v529merge`: 10/10 IDENTICAL** | — |
| **AST derived-default scan** (`ASTSCAN_OUT.txt`) | **0** module-level reads of any v532 / v530.1 / v530 / v528…v518 name across doctrine/eco/main/raid/siege | guard pos/neg exercised on the **v532** name set as well as the inherited ones; **`FERRY_HOME_ON`/`FS_CREW_ON` real-case positive control still found**; and a **deliberately dead `V532_DEAD_DERIVED = FS_V532_WEAVE and 7`** appended to a copy of doctrine.py is **CAUGHT** (`1 [(5703, 'V532_DEAD_DERIVED', 'FS_V532_WEAVE')] … RESULT: FAIL`) |
| **read-site scan** (`READSITE_OUT.txt`, new) | `FS_V532_WEAVE` **READ**, 1 site in `eco.py` | **real-case positive control: `FS_V530_MOUTH_SEATS` reads DEAD, 0 sites** — the v531fix §11.5 hazard, reproduced by the instrument that would catch it |
| `byte_identity532.py --selftest` | PASS | comparator driven to same / differ / empty-vs-nonempty |
| `dose532.py --selftest` | PASS (34 assertions) | `holeH` is not an alias for `shortH`; `holeH` counts CHAINS not EVENTS; a hole on a chain with no harvester counts in `occ_hole` and **not** in `holeH`; an ENEMY *same-facing* conveyor is still a hole; a stripped tape reads 0 on **every** counter, not just `arms` |
| `gridread.py --selftest` | PASS (18 assertions) | `medkill` **excludes** no-kill games rather than zeroing them (a r100 kill + a r1000 timeout reads 100, not 550); `k300` strict at r300/r301; the routetape join **MISSES** on a mutated tag (n=0) rather than silently averaging |
| `readsite.py --selftest` | PASS | a name read in a function PASSES; declared-never-read, read-only-at-module-level, and assignment-target-only all FAIL |
| **routetape winner-vs-tape** | **180/180 agree, 0 parse failures** | (the tool's own gate, unchanged) |
| **tracebacks** | **0** across **396 games** | — |

**Byte-identity, per cell (C2), because "3/10 differ" is a number that deserves
its subject:**

| map | seat A | seat B |
|---|---|---|
| **atoll** | **DIFF** | **DIFF** |
| **yulerune** | SAME | **DIFF** |
| drakkarfjord · glacierkeep · nordkap | SAME | SAME |

**The fix is active only where a corner sits on the mouth's route.** That is
the intended scope and it is also the honest ceiling on how much this change
can move any pooled column.

**Totals: 396 games** — probe 30 · parent-order probe 20 · byte-identity 70 ·
dose 96 · atoll grid 180. **0 tracebacks · 0 no-winner games.**

---

## 3. THE DOSE — planned-vs-laid chain integrity, 48 games/arm

Same tree, one flag moved, **identical instrument in both arms**:
`inst_531off` = `bots/_v532weave` with `FS_V532_WEAVE=False` (**byte-identical
to `bots/_v531fix`, proven by C1 at 10/10**) and `inst_532` = as fired. §6's own
dose panel exactly: 8 maps × 3 seeds × 2 seats. `NOISE_ON = True`, `--tle 0`.

```
arm          games   arms  links   harv  shortH  fullH  holeH occ_benign occ_hole   ttl multi30 | arms by seat: n(median arm round)
inst_531off     48     78    283     17       9      8      7         51       13    43   0.438 | s1:48(r2)  s2:9(r7)  s4:21(r17)
inst_532        48     73    285     17       1     16      0         45        9    40   0.396 | s1:48(r2)  s2:6(r8)  s4:19(r15)
```

⭐ **`holeH` — terminal harvesters reached on a chain carrying a hole — is
7/17 (41.2%) → 0/17 (0.0%).**

⛔ **AND `shortH` IS THE WRONG COUNTER, WHICH IS WHY IT IS PRINTED BESIDE IT.**
§6 counted "terminal harvesters reached on a chain SHORTER than planned" and
read 50% for v531fix. That counter conflates the 58 **benign** adoptions with
the 30 **holes**: a conveyor of ours already facing the right way carries the
flow, so a chain can be short and whole. **`shortH` therefore cannot reach zero
under any correct fix** — it reads **9/17 (52.9%) → 1/17 (5.9%)**, and its
control value reproduces §6's 10/20 (50%) as the **positive control** the brief
asked for.

**Occupied-pop classes, both arms, all 48 games:**

| class | `inst_531off` | `inst_532` |
|---|---|---|
| OURS, CONVEYOR, same facing (benign) | 51 | 45 |
| **OURS, BARRIER** | **9** | **0** |
| ENEMY, BARRIER | 2 | 5 |
| OURS, SENTINEL | 1 | 3 |
| OURS, GUNNER | 1 | 0 |
| ENEMY, SENTINEL | 0 | 1 |

**Our own barriers go to zero. What remains is exactly the classes the doctrine
block named as out of scope BEFORE the battery** — enemy buildings, and our own
turrets built on a planned tile after r2.

**Per map (`harv` / `shortH` / `holeH` / `occ_hole`):**

| map | `inst_531off` | `inst_532` |
|---|---|---|
| **atoll** | 6 / 6 / **6** / 7 | 5 / 1 / **0** / 0 |
| **icefloe** | 5 / 3 / **1** / 3 | 5 / 0 / **0** / 0 |
| nordkap | 3 / 0 / 0 / **1** | 3 / 0 / 0 / **5** |
| yulerune | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 |
| antler | 0 / 0 / 0 / 1 | 1 / 0 / 0 / 2 |
| auroraveil | 0 / 0 / 0 / 1 | 0 / 0 / 0 / 1 |
| drakkarfjord · glacierkeep | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 1 |

**The seat shift the v530.1 fix bought is untouched:** seat 1 arms in 48 of 48
games at median r2 in **both** arms, `multi30` 0.438 → 0.396.

⛔ **NO CPU CLAIM IS MADE FROM THIS DOSE.** `--tle 0` was chosen precisely so
that the stderr instrument, which is identical in both arms, could not make a
time limit bind differently between them. `execTimeUs` is 0 in the local
harness.

---

## 4. THE ATOLL VERIFICATION GRID — **MECHANISM CHECK, NOT CURRENCY**

n=60/arm (30 seeds × 2 seats), **one map**, opponent `bots/_v488beltbreak2`,
`NOISE_ON` as-is (True), `--tle 10`, three arms **interleaved inside each
block** so all three share the same wall-clock slice. 180 games, 0 tracebacks,
15 r1000 games.

```
arm            n   wins   wins% k<=300  medkill  ourcore
parent        60     30   50.0%     18      227       28
v531fix       60     19   31.7%      8      326       37
v532weave     60     27   45.0%     16      260       29
```

| column (routetape, n=60 each) | parent | **v531fix** | **v532weave** |
|---|---|---|---|
| `harv_live30` | 2.45 | 1.70 | **1.90** |
| **`harv_wired30`** | **2.00** | **0.62** | **1.70** |
| `conv_good30` | 4.00 | 3.22 | **3.87** |
| `ti_coll30` | 120.0 | 23.7 | **84.5** |
| **`ti_coll100`** | **422.8** | **133.0** | **349.3** |
| `head1_rnd` (socket claim) | 3.0 | **2.0** | **2.0** |
| `harv1_rnd` | 2.0 | 5.0 | **5.5** |

```
v531fix     vs parent  Dwins -18.33 pp (hw 17.28)  Dk<=300 -16.67 pp (hw 14.44)
v532weave   vs parent  Dwins  -5.00 pp (hw 17.85)  Dk<=300  -3.33 pp (hw 16.11)
```

⭐ **THE COLUMN THE DEFECT LIVED ON IS RECOVERED: `harv_wired30` 0.62 → 1.70
against a parent of 2.00**, and delivery at r100 goes **133 → 349** against a
parent of 423 — while the mouth's own half of the plank survives intact
(`head1_rnd` **2.0**, a round earlier than the parent's 3.0). `v531fix` vs
parent excludes zero on wins; `v532weave` vs parent does not.

⚠ **THREE THINGS THIS TABLE IS NOT.**
* **It is not currency.** One map, one opponent, n=60. `PROGRAMME.md`'s bars
  are not scored on it and none is claimed. The powered read is the builder's.
* **It does not reproduce §6's magnitudes and was never going to.** §6 read
  parent **35/60** and v531fix **10/60**; this re-run of the same arms on the
  same map with different seeds and a re-rolled spawn salt reads **30/60** and
  **19/60**. **The direction and the ordering reproduce; the magnitudes do
  not.** v531fix §8 measured a **4.6 pp same-arm swing at n=480**; at n=60 the
  half-width on a win share is **±17–18 pp**, which is larger than every delta
  in the table.
* **`harv1_rnd` moves the wrong way by half a round (5.0 → 5.5).** The corner
  ban can make the chosen route one link longer; that is the designed price of
  routing around a tile, and it is bought back many times over in `ti_coll30`.

---

## 5. AN UNDERPOWERED PANEL SIGNAL — recorded, not read

Folded from the DOSE stdout, so it is free: **48 games/arm over 8 maps**, at
`--tle 0` with the stderr instrument live in both arms.

```
arm              n   wins   wins% k<=300  medkill  ourcore
inst_531off     48     33   68.8%     22      201       12
inst_532        48     36   75.0%     18      269       10
```

⛔ **DO NOT READ THIS AS A KILL-SPEED REGRESSION.** n=48 gives a half-width of
roughly ±18 pp on a win share and ±19 pp on `k≤300`; **every cell here is
inside its own noise**, the fixture is `--tle 0` with logging on rather than
the standard battery, and 3 of the 8 maps contribute 6 games each. It is
recorded because the `medkill` 201 → 269 direction is the one
`DEFENCE_ADMISSION_BAR` cares about and it would be dishonest to leave it out
of a report that has the data on disk. **The bar is not scored here. It needs
a real battery.**

---

## 6. WHAT THE FIX CANNOT DO — stated before the battery, and still true after

The doctrine block names these in advance:

1. **An ENEMY building on a planned tile after r2 still pops as a hole.** 2 → 5
   events on the dose; 9 of them on the parent-order chains in §1.2. A
   different plank.
2. **One of our own TURRETS built on a planned ring tile after r2 does too.**
   1 → 3 events. Also a different plank.
3. **The ban is gated on `FS_V530_CORNERS`.** With P2 off there is no ban, which
   is correct — with P2 off there is no collision.
4. **A body that does not yet know where our core is gets no ban** — but
   `_v530_mouth_arm` already returns early in exactly that case, so the gap is
   unreachable.
5. **`FS_V530_MOUTH_SEATS` IS STILL A DEAD FLAG** (v531fix §11.5, unchanged).
   `readsite.py` now measures it: 0 read sites. Either wire it or delete it.

---

## 7. ⚠ THE SURPRISE — WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY

**Hole-class pop EVENTS did not all disappear: 13 → 9, and on nordkap they went
1 → 5.** All five are on chains that never reached a harvester (`holeH` = 0
there in both arms), and all are our own SENTINEL / GUNNER or an enemy BARRIER
at r12–r28 — mid-map, mid-game, on seats 2 and 4, nothing to do with a corner:

```
inst_532 nordkap:  r14 s2 (10,9) mine=1 et=SENTINEL   r28 s2 (10,8) mine=0 et=BARRIER
                   r28 s2 (10,9) mine=1 et=SENTINEL   r12 s2 (10,8) mine=1 et=SENTINEL
                   r28 s4 (9,8)  mine=0 et=BARRIER
inst_531off nordkap: r25 s4 (13,7) mine=1 et=GUNNER
```

**n is 3 games per cell and the classes are the ones §6-of-this-report lists as
out of scope**, so the most likely reading is that re-routing seat 1's chain
shifted which tiles seats 2 and 4 later plan through, and those met our own
turret line. **That is a guess. It is not measured and it is not explained.**
A second reading that cannot be excluded at this n is that the corner ban makes
some chains take a route with more turret exposure. Either way it did not reach
a harvester in any of the 48 games.

---

## 8. FAILURE REEL + MANIFEST

### 8.1 FAILURE REEL — atoll grid, `v532weave` arm

Selection rule (house convention, stated before looking): the **earliest
our-core-death on each map**, ties by lowest seed then seat A, capped at 5.
**This battery has ONE map**, so the rule degenerates to the 5 earliest
our-core-deaths on atoll — recorded as a deviation from the convention rather
than silently applied.

`v532weave`: deaths **29 of 60 (48.3%)**, r1000 games 5.
*(`parent` 28/60 with 3 r1000 · `v531fix` 37/60 with 7 r1000 — the arm this
build fixes dies most.)*

| map | turn | seed | seat | replay |
|---|---|---|---|---|
| atoll | 177 | 12 | A | `scratchpad/s52_v532_build/grid/rep/v532weave_atoll_s12_A.replay26` |
| atoll | 187 | 23 | A | `.../grid/rep/v532weave_atoll_s23_A.replay26` |
| atoll | 198 | 25 | A | `.../grid/rep/v532weave_atoll_s25_A.replay26` |
| atoll | 206 | 20 | B | `.../grid/rep/v532weave_atoll_s20_B.replay26` |
| atoll | 217 | 16 | B | `.../grid/rep/v532weave_atoll_s16_B.replay26` |

Labelled extension, **not** part of the reel — the other tail, which is the one
the kill-round bar binds on: latest-kill WINS are
`grid/rep/v532weave_atoll_s20_A.replay26` (**r951**) and
`grid/rep/v532weave_atoll_s23_B.replay26` (**r925**).

⚠ **The reel is the LEAST informative artefact in this build and the manifest
below is the most.** Every row above is a game the fix already improved on
average; the defect this build exists to kill leaves no trace in a
death-round list, because an unwired harvester loses a game slowly. **If one
replay is worth opening it is a `v531fix` row, for contrast:**
`grid/rep/v531fix_atoll_s12_A.replay26` is the same cell in the arm that still
has the hole.

### 8.2 MANIFEST — the 30 §1 classification games

Instrument `scratchpad/s52_v532_build/probe531` (= `_v531fix` + `FS_V530_LOG` +
the classified `MOUTH occ` line). Tapes at
`scratchpad/s52_v532_build/probe/atoll_<seed>_<seat>.err` (stdout `.out` beside
each), seeds **1–15 × seats A,B = 30 games**, opponent `bots/_v488beltbreak2`,
`--tle 10`, `NOISE_ON = True`. Full extraction in
`scratchpad/s52_v532_build/MANIFEST_S1.txt`.

⛔ **REPLAYS WERE NOT RETAINED FOR THESE 30.** `probe.sh` passed no `--replay`,
so each game's replay went to the repo-root default and was overwritten by the
next. **Exact re-run recipe** (deterministic to the extent shown below):
`OUT=<dir> SEEDS="<seed>" bash scratchpad/s52_v532_build/probe.sh`.

**Every one of the 30 games reads identically apart from the mirrored tile:**

| seat | corner tile | corner built | by seat | mouth pops it | links planned | links laid |
|---|---|---|---|---|---|---|
| **A** (15 games, seeds 1–15) | **(1,16)** | **r3** | 2 | **r4** | 2 | **1** |
| **B** (15 games, seeds 1–15) | **(13,1)** | **r3** | 2 | **r4** | 2 | **1** |

Verified over all 30 rows: a barrier pop is present in **30/30**, the barrier
tile is a **logged `V530 CORNER` build in 30/30**, and `corner_rnd < occ_rnd` in
**30/30**.

⛔ **AND A CONSTANT COLUMN VALIDATES ANYTHING, SO SAY WHY THIS ONE IS NOT
BLIND.** Every cell above being identical is a property of the **opening**, not
of the reader: the same instrument, on the same tapes, emitted **four distinct
classes** across the 88 pops (§1.1) and **four distinct classes** across the 52
parent-order pops (§1.2), and it separates `dir == want` from `dir != want`
inside the CONVEYOR class. A reader that could only ever print "BARRIER" would
have produced neither table. The constancy is the finding — atoll's ore at
(1,17)/(12,0) sits behind a corner on both seats, every seed.

### 8.3 MANIFEST — the §7 nordkap anomaly

⚠ **CORRECTION TO THE COUNT AS RELAYED: it is 5 hole-class EVENTS in 3 GAMES,
not 5 games.** The `occ_hole` column counts events; §7 quoted it as such and
the games behind it are enumerated here for the first time.

`inst_532` (as fired), nordkap, seeds 5321–5323 × seats A,B = 6 games:

| tape | rnd | seat | tile | occupier | class |
|---|---|---|---|---|---|
| `scratchpad/s52_v532_build/dose/inst_532/nordkap_5321_A.err` | 14 | 2 | (10,9) | **ours, SENTINEL** (dir NORTHEAST, want NORTH) | hole |
| `.../dose/inst_532/nordkap_5322_A.err` | 28 | 2 | (10,8) | **ENEMY, BARRIER** | hole |
| `.../dose/inst_532/nordkap_5322_A.err` | 28 | 2 | (10,9) | **ours, SENTINEL** (dir SOUTH, want NORTH) | hole |
| `.../dose/inst_532/nordkap_5323_A.err` | 12 | 2 | (10,8) | **ours, SENTINEL** (dir SOUTHEAST, want NORTH) | hole |
| `.../dose/inst_532/nordkap_5323_A.err` | 28 | 4 | (9,8) | **ENEMY, BARRIER** | hole |

**Control arm, same 6 cells** — `inst_531off` (= `_v531fix` byte-identically),
**1 hole event in 1 game**:

| tape | rnd | seat | tile | occupier | class |
|---|---|---|---|---|---|
| `.../dose/inst_531off/nordkap_5323_A.err` | 25 | 4 | (13,7) | **ours, GUNNER** (dir WEST, want WEST) | hole |

**Benign in both arms and therefore not part of the anomaly:** `rnd=9 seat=1
tile=(12,18) mine=1 et=CONVEYOR dir=WEST want=WEST` appears in
`nordkap_5321_B`, `nordkap_5322_B`, `nordkap_5323_B` of **both** arms —
identical text, so seat 1's chain on seat B is untouched by the fix on this
board.

**What the manifest adds to §7:** the rise is carried by **seat 2 on seat-A
games only** (3 of the 5 events, all our own SENTINEL at (10,8)/(10,9), r12–r28),
plus 2 enemy barriers. **Seat 1 — the seat the whole plank is about — is not
involved in a single one of them.** ⛔ **Still unexplained, and still n=3 games
per cell.** `harv`/`shortH`/`holeH` on nordkap are 3/0/0 in **both** arms, so
no chain that reached a harvester was affected either way.

⛔ **REPLAYS WERE NOT RETAINED FOR THE DOSE EITHER** (`dose532.sh` passes no
`--replay`). **Exact re-run recipe:**
`.venv/bin/fcode run scratchpad/s52_v532_build/inst_532 bots/_v488beltbreak2
maps/nordkap.map26 --seed 5322 --tle 0 --replay <path>` (swap the two bot
arguments for a seat-B cell; `inst_531off` for the control arm).

⚠ **NOT RETAINING THOSE REPLAYS IS A DEFECT OF THIS BUILD, NOT A PROPERTY OF
THE FIXTURE.** The one class of game a marker loop most wants to open is the
unexplained one, and it is exactly the class this build can only offer a
re-run recipe for. **Successor: pass `--replay` in `probe.sh` and
`dose532.sh`.**

---

## 9. RAW — tapes, instruments, PIDs

All under `scratchpad/s52_v532_build/`:
`probe/` 30 games of stderr (v531fix, classified `MOUTH occ`) ·
`probe2/` 20 games (adds the `PARENT occ` control on `_build_next_link`) ·
`byte_check/` 70 replays · `dose/inst_531off` + `dose/inst_532` 96 games of
stderr · `grid/results.tsv` 180 rows + `grid/rep/` 180 replays · `raceG.tsv`
(routetape batch, **180/180 winner-vs-tape agree, 0 parse failures**) ·
`BYTEID_OUT.txt` · `ASTSCAN_OUT.txt` · `READSITE_OUT.txt` · `DOSE_OUT.txt` ·
`DOSEPANEL_OUT.txt` · `GRID_OUT.txt` · `MANIFEST_S1.txt` (the §8.2 extraction,
all 30 rows) · `FINDING-defect.md` (the pre-design
falsification, written before any code was changed) · `TREE.md5` · `PIDS`
(DOSE 23610, GRID 31093) · `probe.sh` · `dose532.sh` · `grid_atoll.sh`.

Arms: `probe531`, `probe532`, `inst_531off`, `inst_532`, `grid_parent`,
`grid_v531fix`, `grid_v532`, and the byte-identity set `eq_opp`, `eq_v532`,
`eq_weaveoff`, `eq_bootoff`, `eq_masteroff`, `eq_v531`, `eq_v530`, `eq_parent`
— all built by `mkarm.sh` (definition-site overrides, never appends).

**New instruments written for this build, each with a `--selftest` that drives
every guard to the other verdict:** `dose532.py` (the hole-vs-benign classifier
and the `holeH` counter), `gridread.py` (the atoll grid fold + the routetape
join + the `.out` fold), `readsite.py` (every new name must be read at a call
site — the `FS_V530_MOUTH_SEATS` class), `byte_identity532.py` (the v532 arm
chain). `flagoff_ast.py` is s51's, extended with the v532 name set and its two
guards. `run_battery.py`, `mkarm.sh` and `deliv.py` are s51's, unchanged;
`routetape.py` is the research arm's (`scratchpad/s51_route/`), unchanged.

**⛔ NOTHING UNDER `bots/_v531fix` OR `scratchpad/s51_v5301_build` WAS
WRITTEN.** Instruments needed from there were **copied into
`scratchpad/s52_v532_build/` and the copies were run**; the `_v531fix` md5s in
`TREE.md5` at `09:20:22Z` match the ones read at `08:59Z`. `tools/*` was not
edited. `scratchpad/overnight*` and `corefill_forever.sh` were not touched.

**⛔ NO CPU CLAIM IS MADE ANYWHERE IN THIS REPORT.** `execTimeUs` is 0 in the
local harness and the dose ran at `--tle 0`. The fix removes work from the
opening (a shorter flood over a slightly smaller passable set) and adds none
per round; that is an argument, not a measurement.

---

## 10. HONEST LIMITS

1. **NO CURRENCY READ WAS RUN.** No battery A, no battery B, no
   `DEFENCE_ADMISSION_BAR`, no `KILL_TARGET`. The only pooled win numbers here
   are n=60 on one map and n=48 on the dose panel, and both are inside their
   own half-widths. **This build proves the mechanism is repaired; it does not
   price it.**
2. **THE ATOLL GRID DOES NOT REPRODUCE §6's MAGNITUDES** (parent 30/60 here vs
   35/60 there, v531fix 19/60 vs 10/60). Direction and ordering reproduce.
   §8 of the v531fix report is the reason and it applies to this table too.
3. **THE FALSIFICATION IN §1 IS ATOLL-ONLY FOR THE CORNER CLAIM.** 30 of 30 is
   deterministic *on atoll*; the 8-map dose confirms the class exists elsewhere
   (icefloe 1 holeH) but does not establish that every board's collision is a
   corner. **§6's claim about "another body's parent-order chain" was not
   observed anywhere in 50 instrumented games — 0 wrong-facing conveyor pops
   and 0 enemy pops on the mouth chain — but "not observed on atoll and 7 other
   maps" is not "cannot happen".**
4. **`shortH` 1/17 IS NOT ZERO.** One chain in `inst_532` still reached its
   harvester short — a benign adoption, `holeH` 0. Correct behaviour, recorded
   so the number is not read as a residual defect.
5. **THE `medkill` 201 → 269 IN §5 IS UNRESOLVED.** It is inside its interval
   at n=48 and the fixture is not a battery fixture. It is the one number in
   this report that would matter to `DEFENCE_ADMISSION_BAR` and it has not been
   measured properly.
6. **THE NORDKAP EVENT RISE (§7) IS UNEXPLAINED**, and §8.3 enumerates the 3
   games behind the 5 events without explaining them. Note the count
   correction there: **5 EVENTS in 3 GAMES**, not 5 games.
7. **THE PROBE AND DOSE REPLAYS WERE NOT RETAINED** (§8.2, §8.3) — neither
   runner passed `--replay`, so the 30 classification games and the 3 nordkap
   anomaly games exist only as stderr tapes plus a re-run recipe. **The one
   class a marker loop most wants to open is the one this build cannot hand
   over.** The atoll grid's 180 replays ARE on disk.
7. **`_v532weave` HAS NEVER PLAYED A LIVE TEAM.** Per `CLAUDE.md` point 6, a
   local battery may prioritise a plank and may not retire a road.
