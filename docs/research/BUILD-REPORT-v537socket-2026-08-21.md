# BUILD REPORT — `bots/_v537socket` (v537), s52, 2026-08-21

**ONE PLANK: PUT A CONVEYOR ON ONE OF OUR OWN CORE DELIVERY SEATS BY r4,
UNCONDITIONALLY, BEFORE MJOLNIR'S COLLAR BRICKS IT.** Parent
`bots/_v536trustport`, md5-frozen at `03:00:27Z` and re-verified byte-unchanged
at `03:16:19Z` (`scratchpad/s52_v537_build/PARENT_FREEZE.md5`). The plank and
its verification design are both the crater diff study's
(`docs/research/DIFF-STUDY-v169-craters-2026-08-21.md`, §Q4 constraints 1-6 and
"the cheapest discriminating test").

This build wrote to `bots/_v537socket`, `docs/research/` and
`scratchpad/s52_v537_build/` only. No `tools/*` edit. `bots/_v488beltbreak2` is
mode-444 and was read, never written. Wall clock from `date -u` in the same
shell call each time: context read `02:59:50Z`, tree copy + parent freeze
`03:00:27Z`, instrument validation `03:01:56Z`, doctrine block `03:07:23Z`,
code `03:07-03:09Z`, identity battery `03:09:13-03:10:29Z`, mechanism battery
`03:12:22-03:17:41Z`, parent re-freeze `03:16:19Z`, raider-tempo battery
`03:20:43-03:28:37Z`, identity re-run on final bytes `03:32:24-03:33:54Z`.

---

## ⛔ TOP LINE — SIX SENTENCES

1. **THE DOSE IS DELIVERED EXACTLY AND WITHOUT VARIANCE: 600 of 600 games claim
   a Core delivery seat at ROUND 1**, across two independent 300-cell runs.
   Control `_v536trustport` claims at a median of r23 and **never claims at all
   in 340 of 600** of the same cells. Paired McNemar on the never-claim flip,
   run 1: **174 discordant cells, ALL ONE WAY, z = −13.19; zero reverse cells
   in either run.**
2. **THE MECHANISM MOVES ALL THE WAY DOWN THE CHAIN.** Games delivering any
   titanium **35 % → 77 %**; own seats held at end of game **0.36 → 2.01 of 8**;
   games ending with **zero** own seats **200/300 → 4/300**. Pooled wins
   **175/600 → 289/600 (+19.0 pp)** — ⚠ mechanism evidence, not a rate: §6.2
   measures this fixture re-running itself **7.4 pp apart**.
3. ⭐ **THE REGRESSION CAUSE IS NAMED AND CONTROLLED TO ONE FLAG, AND IT IS NOT
   A BUG IN v529merge — IT IS THE *ABSENCE* OF THE HOME PACKAGE'S `FS_V530_MOUTH`
   PLANK, WHICH IS ITSELF CAPPED AT 6 LINKS AND THEREFORE NEVER REACHES THE
   REAL CRATERS.** §2. v537's plank is the uncapped, route-free generalisation
   of it: MOUTH arms on 2 of these 5 maps, v537 on 5 of 5.
4. ⚠ **THE FALSIFIER CELL PASSES ON THE STUDY'S OWN WORDING AND THE COMMISSION
   PARAPHRASED IT BACKWARDS.** The study requires auroraveil's never-rate to
   fall to ~0 or the mechanism story is wrong; it falls **43.3 % → 0.0 %**. §5.
5. ⭐⭐ **THE SURPRISE, WRITTEN BEFORE IT IS EXPLAINED: THE PLANK COSTS GAMES ON
   EXACTLY THE CELLS THAT HAD NO DEFECT — and it REPLICATES.** On the two
   (map, seat) cells where the parent already claimed early — auroraveil seat A
   (r22) and drakkarfjord seat B (r23) — pooled over both runs v537 reads
   **83/120 against the parent's 110/120 (−22.5 pp)**, while the other eight
   cells read **206/480 against 65/480 (+29.4 pp)**. §6. **The one candidate
   mechanism (the r1 claim spends the ferry-siege raider's first turn) was
   built behind `FS_V537_RAIDER_CLAIMS`, fired in a 900-game three-arm battery,
   and REFUTED — moving the claim to r2 takes those cells from 40/60 to 16/60.
   No explanation is offered.**
6. ⚠ **NO CURRENCY CLAIM AND NO CPU CLAIM IS MADE HERE.** The win columns at
   n = 60/cell are **mechanism evidence**; the powered screen is the builder's.

---

## 1. THE PLANK AS BUILT

**Three functions in `eco.py` (+119 lines), one rung in `main.py` (+12), one
flag block in `doctrine.py` (+86). `raid.py` and `siege.py` are md5-identical
to the parent, and no parent line anywhere is removed or edited — the whole
changeset is additive** (`flagscan.py` §1, `OUT_flagscan.txt`).

| site | what |
|---|---|
| `eco.py:_v537_side` | which of the four sides of the 2×2 footprint a ring seat sits on |
| `eco.py:_v537_seat_pool` | `delivery_seats(...)` first, then the rest of `heal_seats(...)` |
| `eco.py:_v537_sockets_held` | how many ring seats hold **our own** belt building, **read from the engine every call** |
| `eco.py:_v537_socket_claim` | the action: `build_conveyor(seat, facing the core)` |
| `main.py:1556` | one rung: `if FS_V537_SOCKET and self._v537_socket_claim(ct, rnd): return` |

**Flags** (`doctrine.py`, LOKI-V537 block):

| flag | value | meaning |
|---|---|---|
| `FS_V537_SOCKET` | `True` | master. `False` == `bots/_v536trustport` unchanged |
| `FS_V537_BY_ROUND` | `4` | the claim window; their first plug lands r13-r16 |
| `FS_V537_MAX_SOCKETS` | `2` | never take more than 2 of 8 — the Core spawns on its ring |
| `FS_V537_SIDE_SPREAD` | `True` | seat #2 must be on a different side than seat #1 |
| `FS_V537_RAIDER_CLAIMS` | `True` | may the r0 body (the ferry-siege raider) spend its first turn on it — see §6 |
| `FS_V537_LOG` | `False` | off in competition |

### 1.1 Four design decisions, each with the reason it is not the other thing

**(a) THE RUNG SITS ABOVE EVERY ROLE DISPATCH AND BELOW EVERY EMERGENCY.**
It is ranked after the universal adjacent heal, the melee recall and the
door-turret answer, and before `_fs_turn` / `_raid` / `_defend` / `_expand`.
What it buys is a **clock**, so anything an eco verb can out-rank is too late.

**(b) NOTHING IS LATCHED AND NO STORE SLOT IS SPENT.** How many seats we hold
is re-derived from the engine on every call. A latch would keep reporting
"claimed" after they shoot the conveyor off the seat; a store slot would spend
1 of 16 on a fact the map already carries.

**(c) `_v537_seat_pool` COMPUTES `delivery_seats` FRESH RATHER THAN CALLING
`self._seat_ban()`.** ⛔ `_seat_ban` **memoises on first call**. Calling it at
r1 would freeze `seat_ban`/`seat_keep` to whatever ore knowledge that body
happens to hold and change downstream behaviour that has nothing to do with
this plank — a flag-on side-effect outside the plank's own claim.

**(d) THE TRUNK PLANNER IS NOT TOUCHED, AND THAT IS DELIBERATE.** The study's
constraint 2 says "build the trunk core-outward, not ore-inward". The trunk is
still planned and drained exactly as before; what changes is that its terminal
tile is **already ours** when it arrives, and `_build_next_link`'s own
`if occupied: pop` branch walks over it. **So the seat becomes the FIRST tile
of the trunk instead of the last, which is the whole of "core-outward" that the
measured defect needs** — the study measured our conveyor loss in the *middle*
of the trunk at **0 %** on both craters. §2 adds the evidence that the full
reversal was already tried on this line and capped itself out of the craters.

**Bounds are tested explicitly** (`0 <= x < mw and 0 <= y < mh`) before any
`get_tile_*`, because `is_in_vision` is a pure radius test and **is not** a
bounds guard (CLAUDE.md, corrected s50) — and a Core ring seat is exactly the
near-the-edge case where that bites.

---

## 2. THE REGRESSION DIAGNOSIS — one flag, single-variable control

**The defect as commissioned:** `_v529merge` (and therefore `_v536trustport`,
which is `_v529merge` + MAPTRUST) **never claims a seat in 68 % of yulerune and
33 % of icefloe games**, where `_v533home` and `_v534maptrust` claim at r2 in
100 % of the same cells. Reproduced on this build's own projection of the
study's 2,700-game tape (`ringcheck.py --tsv`, §7): yulerune v529merge **68 %**
never / 5 % win vs v534maptrust **0 %** / 50 %; icefloe **33 %** / 8 % vs
**0 %** / 37 % — the study's table, digit for digit.

### 2.1 The cause

**It is not a bug that `_v529merge` has. It is a plank that `_v533home` has and
`_v529merge` does not: `FS_V530_MOUTH`, the home package's MOUTH-FIRST BELT.**
It calls the *same* `_link_path` and simply reverses the plan, so the Core seat
is link **1** instead of link **N**:

```python
# bots/_v533home/eco.py:1183-1191   (absent from _v529merge / _v536trustport)
plan = self._link_path(ct, ore, xblock)
if not plan or len(plan) > V530_MOUTH_MAX_LINKS:
    self.mouth_done = True
    return False
self.mouth_queue = list(reversed(plan))
```

The parent order that both trees fall back to is the ore-end-first
reconstruction in `_link_path` (`eco.py:879-884` on this chassis) drained by
`_build_next_link`'s `link_queue[0]`, and the silent kill is this clause:

```python
if occupied:
    self.link_queue.pop(0)
    continue
```

— when the terminal seat is already **their** barrier, it is popped, the queue
empties, `_build_next_link` returns False, and **nothing re-plans it.** The
belt is permanently one 3-Ti link short of delivering.

### 2.2 The single-variable control (this is the load-bearing evidence)

`bots/_v533home` copied and **one constant flipped**, `LOKI_FS_V530 = True →
False`. yulerune seat A, seeds 1/2/3:

| tree | claims the seat | build tape |
|---|---|---|
| v533home, flag **ON** | **r2, 3 of 3** | r2 (3,8) · r4 (3,7) · r6 (3,6) · r8 (4,6) · r10 (5,6) |
| v533home, flag **OFF** | **NEVER, 3 of 3** | r6 (4,6) · r8 (5,6) · r9 (3,6) · r11 (3,7) — stops one short |

The OFF tape is byte-identical to `_v529merge`'s. **One flag accounts for the
entire regression.**

### 2.3 ⭐ AND THE FIX THE COMMISSION ASKED FOR IS NOT "PORT MOUTH" — MOUTH IS
CAPPED OUT OF THE CRATERS

`V530_MOUTH_MAX_LINKS = 6`: MOUTH refuses any plan longer than six links and
falls back to the parent's ore-first order. Nearest-ore Manhattan distance from
the Core footprint decides whether it arms at all:

| map | nearest ore | plan length | MOUTH arms? | observed, all three study arms |
|---|---|---|---|---|
| yulerune | 6 | 5 | **yes** | v533/v534 claim r2; v529 never |
| icefloe | 6 | 5 | **yes** | v533/v534 claim r3/r7; v529 66 % never (seat A) |
| auroraveil | — | 7-9 | **no** | all three identical (36 % never) |
| drakkarfjord | 9 | 8 | **no** | all three identical (52 % never) |
| glacierkeep | 11 | 10 | **no** | all three identical (83-90 % never) |

⇒ **Porting MOUTH would have fixed the two REGRESSION cells and left the three
REAL CRATERS exactly where they were.** v537's plank is MOUTH's idea with the
two gates that disqualified it removed: **no route-length cap and no route at
all** — it does not need a harvester, a plan, or an ore. It arms on 5 of 5 maps
and 300 of 300 games, at r1.

### 2.4 ⭐ THE SEAT ASYMMETRY, which the study did not name — two causes

The never-claim rate is not a map property, it is a **(map, seat)** property,
and the split is enormous: drakkarfjord **seat A 100 % never / seat B 6 %** in
*every* arm; auroraveil the exact mirror (**seat A 0 % / seat B 86 %**). Maps
are symmetric, so this is orientation-dependent code. Two independent causes
were isolated:

1. **drakkarfjord / glacierkeep — OUR code mirrors perfectly; THEIRS does
   not.** Our two tapes are exact mirrors round-for-round under the map's own
   180° rotation. What breaks the symmetry is **their** plug order:
   `raid_stations = core_corners(E) + heal_seats(E)` indexed by
   `stations[self.raid_slot % len(stations)]`, and `heal_seats` is a fixed
   **NW-anchored clockwise tuple** — index→tile is **not equivariant** under
   reflection or rotation. Their seal enters our ring on the tile our BFS
   terminates on, on seat A only.
2. **auroraveil — OUR OWN `_pick` ore partition is non-mirror-equivariant.**
   `eco.py:1710-1717` sorts ore by `abs(t.x - self.core.x) + abs(t.y -
   self.core.y)` — distance from the **anchor** (the NW tile of the 2×2), not
   from the footprint, so every mirror pair's distance shifts by ±1 **in
   opposite directions on the two sides of the Core** — then breaks ties on a
   **raw-coordinate hash** `(t.x*17 + t.y*31 + worker*7) % 97`, then deals
   `ordered[worker::workers]` round-robin, which turns a one-rank shift into a
   *different builder*. Measured: **0 of 6 maps** produce mirrored slices for
   all four worker seats.

⚠ **Neither is fixed by this build**, and neither needs to be for the plank to
work: v537 claims at r1 on **both** seats of all five maps (300/300). The
`_pick` anchor asymmetry is filed in §9 as its own plank — it is a general
correctness defect that happens to be *revealed* here, not caused here.

⚠ **One map fact:** **yulerune's ore set is NOT mirror-closed** under its own
symmetry. Part of yulerune's seat split is genuine map asymmetry on top of
everything above.

---

## 3. INSTRUMENT VALIDATION — before any number is read

**`scratchpad/s52_diffstudy/ringtime.py` is the study's instrument and ships
with NO `--selftest`.** This build supplies one (`ringcheck.py --selftest`,
PASS at `03:01:56Z`) and adds the seat-aware projection the test actually
reads. **The projection is the load-bearing step and it is the easy one to get
wrong**: a replay named `_A` has our arm as team 0 and `_B` as team 1, and
reading the wrong half would report the **opponent's** socket clock — which on
these maps is r2 on 15/15 maps, i.e. exactly the number a broken reader would
want to print.

Six guards, **each driven to both verdicts**:

| guard | driven the other way |
|---|---|
| G1 positive: the study's hand-counted board `glacierkeep_s10_A` reads plugmax **7**, own1 **−1**, deliv **0** | G2 |
| G2 other-verdict: `ragnarok_s10_A` reads own1 **≥ 0**, plugmax ≠ 7, deliv > 0 — the columns are not constant | G1 |
| G3 mutation: ring anchor shifted (+5,+5) → plugmax collapses on both fixtures; un-mutating restores **7** | itself |
| G4 cross-check vs the independent walk in `ringplug.py` on the shared quantity | both directions of the `own_end`↔`own1_r` agreement |
| G5 **seat projection**: seat A reads `a_*`, seat B reads `b_*`, and a **deliberately mis-seated read gives a different verdict** | the mis-seat mutant |
| G6 never-classifier returns **1** on glacierkeep and **0** on ragnarok | itself |

**And it was validated against a published independent read, not only against
itself:** projecting the study's own 2,700-row `ringtime.tsv` reproduces the
study's arm × map dose table digit for digit (yulerune v529merge 68 %/5 %,
icefloe 33 %/8 %, glacierkeep 83/90/83 %, drakkarfjord 50/57/50 %, auroraveil
36/36/35 %).

`mechtab.py --selftest` (PASS) drives the McNemar and cell aggregators both
ways on synthetic tapes: a perfect flip → `b=0 c=10 z=−3.16`; identical arms →
`b=0 c=0 z=0.00`; an all-claim tape → never 0 % / deliv 100 %; an all-never
tape → never 100 % / deliv 0 % / median claim `None`.

`rowdiff.py --selftest` (PASS) corrupts a pair that currently reads **0**
differences; all three mutants (`turn +1`, `ours` flipped, `ours_mined +1`)
move **exactly 1** row.

---

## 4. THE MECHANISM TEST

⚠ **This section is RUN 1 of two.** The identical fixture was re-run eight
minutes later with a third arm (§6.1); §6.2 pools both and reports how far the
win column moved between them. **The never-claim column is identical in both.**

`scratchpad/s52_v537_build/mech/`, `03:12:22-03:17:41Z`. Two arms
**interleaved** by `run_battery.py` (all arms of a cell adjacent, so they share
one wall-clock slice — v518 finding 2 measured a **4.6 pp false positive** from
pooling non-time-adjacent local fixtures). Opponent `bots/_x3r0v169mjolnir`,
the live holder tree. **5 maps × 30 seeds × 2 seats × 2 arms = 600 games**,
`PAR=6`, **0 tracebacks**.

⛔ **RUN LOCAL, NOT ON ws2, AND THE REASON IS THE INSTRUMENT.** `ringtime.py`
walks the **replay turn stream**; `tools/remote_battery.py` runs every game
with `--replay /dev/null` and has no flag to keep one. A remote battery cannot
carry this readout at all. ws1 was not touched (it returns ~04:00Z; this ran at
03:12Z).

**DEFF:** local screens are balanced-by-construction and read pair-weighted
DEFF = 0.98 (s39 audit), so naive intervals are used and are marginally
conservative. Both arms share every (map, seed, seat) cell, so the arm contrast
is **paired** and McNemar is the reported test.

### 4.1 Per map, per arm

| map | v537socket never% / med first claim / deliv>0 / win | v536trust never% / med first claim / deliv>0 / win |
|---|---|---|
| **glacierkeep** | **0.0 %** · **r1** · 43.3 % · 25/60 | 88.3 % · r356 · 8.3 % · 14/60 |
| **drakkarfjord** | **0.0 %** · **r1** · 100.0 % · 49/60 | 53.3 % · r23 · 46.7 % · 29/60 |
| **auroraveil** *(falsifier)* | **0.0 %** · **r1** · 81.7 % · 33/60 | 43.3 % · r22 · 56.7 % · 31/60 |
| **yulerune** *(regression cell)* | **0.0 %** · **r1** · 100.0 % · 29/60 | 71.7 % · r13 · 28.3 % · 5/60 |
| **icefloe** *(regression cell)* | **0.0 %** · **r1** · 58.3 % · 16/60 | 33.3 % · r88 · 30.0 % · 5/60 |
| **POOL n=300/arm** | **0.0 %** · **r1** · **76.7 %** · **152/300** | **58.0 %** · **r23** · **34.0 %** · **84/300** |

**300 of 300 v537 games claim at exactly r1** — the first-claim column has a
single value, no variance.

### 4.2 Paired McNemar

| map | never-claim flip: v537-only-never / v536-only-never / z | wins: v537-only / v536-only / z / Δ |
|---|---|---|
| glacierkeep | 0 / 53 / **−7.28** | 17 / 6 / +2.29 / **+18.3 pp** |
| drakkarfjord | 0 / 32 / **−5.66** | 27 / 7 / +3.43 / **+33.3 pp** |
| auroraveil | 0 / 26 / **−5.10** | 14 / 12 / +0.39 / **+3.3 pp** |
| yulerune | 0 / 43 / **−6.56** | 25 / 1 / +4.71 / **+40.0 pp** |
| icefloe | 0 / 20 / **−4.47** | 15 / 4 / +2.52 / **+18.3 pp** |
| **POOL** | **0 / 174 / −13.19** | 98 / 30 / +6.01 / **+22.7 pp** |

**Zero reverse cells on the mechanism, in all 300.** The study's Gate 1
falsifier — *"never% stays above 40 %, or `deliv>0` fails to rise from 11 %"* —
is refuted in both halves.

### 4.3 The chain below the claim

| quantity, per game | v537socket | v536trust |
|---|---|---|
| own Core seats held at end (of 8) | **2.01** | 0.36 |
| games ending with **zero** own seats | **4 / 300** | 200 / 300 |
| games delivering any titanium | **76.7 %** | 34.0 % |
| games ending at r1000 | **46** | 53 |
| games we won by destroying their Core | **134** | 76 |

### 4.4 ⚠ THE KILL-ROUND BAR, reported both ways because they disagree

`PROGRAMME.md`'s primary is the **timely-kill rate: the share of ALL games
ending in a core-kill by r300.**

| | v537socket | v536trust |
|---|---|---|
| **timely-kill rate (primary): our core-kills by r300 / ALL games** | **55/300 = 18.3 %** | 45/300 = 15.0 % |
| median kill round **conditioned on a kill** (diagnostic, carries a collider) | **r329** | r261 |

⇒ **The primary RISES (+3.3 pp) — the plank is not off-programme on the bar as
written.** The gross backstop (median crossing 300) *is* crossed, and the
reason is visible and is the collider the PROGRAMME names: v537 converts 58
games that v536 simply lost into kills, and the games it converts are the long
ones. ⚠ **This is a 5-map, one-opponent, local cut. The kill-round verdict is
the builder's powered screen, not this build's.**

---

## 5. THE FALSIFIER CELL — and the commission paraphrased it backwards

**The study's own words** (§Q4 constraint 6): *"AURORAVEIL IS THE BUILT-IN
FALSIFIER CELL, NOT A BONUS… A correct fix **must move auroraveil's never-rate
to ~0 as well**; if it fixes glacierkeep and leaves auroraveil at 36 %, the
mechanism story is wrong."*

**The commission's brief to this build states the opposite** — *"the study
predicts the plank does NOT recover it, so if it does, the mechanism story is
wrong."* The two readings imply opposite verdicts from the same number, so the
number is reported against **both**:

| | measured |
|---|---|
| auroraveil never-claim, control → treatment | **43.3 % → 0.0 %** (McNemar z = −5.10, 26 discordant, 0 reverse) |
| **verdict on the STUDY's stated falsifier** | **PASS — the mechanism story holds** |
| verdict on the commission's inverted paraphrase | would read as a surprise |

**This build follows the study**, which is the document that owns the
falsifier, is quoted verbatim above, and is internally consistent with its own
ρ = 0.925 socket-vs-win correlation. **The paraphrase is filed as a
discrepancy, not silently resolved.**

⚠ **But the falsifier's WIN column is the honest complication, and it is §6:**
auroraveil's never-rate went to zero and its win rate moved **+3.3 pp
(z = +0.39)** — by far the smallest of the five maps. **On auroraveil the
socket claim is necessary and not sufficient.** A pure ρ = 0.925 reading would
not have predicted that.

---

## 6. ⭐⭐ THE SURPRISE — the plank costs games where there was no defect

**Written down before it is explained.** Splitting by (map, seat) — which the
study did not do, and which §2.4 shows is where the whole structure lives:

| map, seat | control never% / win | v537 never% / win | Δ wins |
|---|---|---|---|
| yulerune A | **100 %** / 0/30 | 0 % / 8/30 | **+8** |
| drakkarfjord A | **100 %** / 1/30 | 0 % / 26/30 | **+25** |
| glacierkeep A | 83 % / 7/30 | 0 % / 18/30 | **+11** |
| yulerune B | 43 % / 5/30 | 0 % / 21/30 | **+16** |
| icefloe B | 0 % *(r88)* / 1/30 | 0 % / 13/30 | +12 |
| auroraveil B | 86 % / 5/30 | 0 % / 13/30 | **+8** |
| glacierkeep B | 93 % / 7/30 | 0 % / 7/30 | 0 |
| icefloe A | 66 % / 4/30 | 0 % / 3/30 | **−1** |
| **drakkarfjord B** | **6 % (r23)** / **28/30** | 0 % / 23/30 | **−5** |
| **auroraveil A** | **0 % (r22)** / **26/30** | 0 % / 20/30 | **−6** |

**The two cells where the plank LOSES are the two cells where the control
already claimed early and was already winning 87-93 %.** The pattern is
monotone in the defect: big gains where the control never claimed, a real cost
where it did.

**The candidate mechanism, and it is measurable rather than argued:** the claim
spends **one builder turn at r1**, and at r1 the only body alive is seat 0 —
the body `LOKI_FERRY_SIEGE` forks into **the raider**. On a map where the seat
was never at risk, that is one round of raid tempo bought for nothing. The
cost-cell replays are consistent with it: on auroraveil s8 seat A the parent
kills at **r156** while v537's game runs to **r417** and loses; on drakkarfjord
s8 seat B, **r243 → r723**.

⇒ **A sub-flag `FS_V537_RAIDER_CLAIMS` was added and the hypothesis was FIRED,
not assumed** — §6.1. **It was refuted.**

### 6.1 THE RAIDER-TEMPO ARM — hypothesis fired and REFUTED

`scratchpad/s52_v537_build/mech2/`, `03:20:43-03:28:37Z`. **Three arms
interleaved on the same grid — 5 maps × 30 seeds × 2 seats × 3 arms = 900
games**, same opponent, `PAR=6`, **0 tracebacks**. `v537noraid` is the shipped
tree with `FS_V537_RAIDER_CLAIMS = False`: the r0 raider does not claim, so the
first eco seat does it one round later.

| arm | claim round | never% | deliv>0 | wins /300 | vs control |
|---|---|---|---|---|---|
| `v537socket` (**ships**) | **r1** | 0.0 % | 77 % | **137** | +15.3 pp, z = +4.20 |
| `v537noraid` | **r2** | 0.0 % | 59 % | 124 | +11.0 pp, z = +2.60 |
| `v536trust` (control) | r24 | 55.3 % | 37 % | 91 | — |

| **THE TWO COST CELLS ONLY** (auroraveil A + drakkarfjord B) | wins /60 |
|---|---|
| `v536trust` | **56** |
| `v537socket` | 40 |
| `v537noraid` | **16** |

⛔ **REFUTED, and not marginally.** Moving the claim off the raider does not
recover the cost cells — it **more than doubles the loss there** (40 → 16 of
60) and costs 13 games overall. `v537noraid` vs `v537socket`: **−4.3 pp,
z = −1.01** pooled, i.e. worse and not distinguishable from noise pooled, but
**decisive on the cells the hypothesis was built to explain.**

⇒ **`FS_V537_RAIDER_CLAIMS` ships `True`, which is also the study's spec read
literally, and §6 stays UNEXPLAINED.** One candidate mechanism was named,
tested against a pre-stated prediction, and killed. Writing the surprise down
without an explanation is the correct end state here.

### 6.2 ⚠ THE COST REPLICATES; THE POOLED DELTA DOES NOT REPRODUCE TO BETTER
THAN ~7 pp

Two independent 300-cell runs of the **identical fixture, eight minutes apart**
(the shipped trees are `NOISE_ON`, so cells are not deterministic across runs):

| | v537socket | v536trust | Δ | never (v537 / v536) |
|---|---|---|---|---|
| `mech` 03:12-03:17Z | 152/300 (50.7 %) | 84/300 (28.0 %) | **+22.7 pp** | 0 / 174 |
| `mech2` 03:20-03:28Z | 137/300 (45.7 %) | 91/300 (30.3 %) | **+15.3 pp** | 0 / 166 |
| **POOLED, 600/arm** | **289/600 (48.2 %)** | **175/600 (29.2 %)** | **+19.0 pp** | **0 / 340** |

⚠ **The win delta moved 7.4 pp between two runs of the same fixture with
nothing changed.** That is this fixture's own reproducibility and it is the
reason §4's win columns are labelled mechanism evidence rather than a rate.
**The mechanism column did not move at all: 0 never-claims in 600 of 600.**

**And the cost cells replicate while the pool wobbles**, which is what makes §6
a finding rather than a stray cell:

| cut, POOLED over both runs | v537socket | v536trust | Δ |
|---|---|---|---|
| **the 2 cells the control already claimed on** | 83/120 (69 %) | **110/120 (92 %)** | **−22.5 pp** |
| **the other 8 cells** | **206/480 (43 %)** | 65/480 (14 %) | **+29.4 pp** |

**Both runs show the cost, at −11 and −16 games of 60.**

### 6.3 Kill-round, second run

| | v537socket | v537noraid | v536trust |
|---|---|---|---|
| **timely-kill rate (primary)** | **18.0 %** | 14.7 % | 15.3 % |
| median kill round (diagnostic) | r326 | r339 | r269 |
| games ending at r1000 | **32** | 57 | 42 |

The primary rises in **both** runs (18.3 %/18.0 % vs 15.0 %/15.3 %) and the
r1000 tail shrinks in both. The `noraid` arm is the one that would fail the
bar.

---

## 7. FLAG-OFF IS `bots/_v536trustport` — FOUR WAYS

### 7.1 Static (`flagscan.py`, `OUT_flagscan.txt`, **PASS**)

| check | result |
|---|---|
| `raid.py`, `siege.py` md5-identical to the frozen parent | **yes** |
| `main.py` / `eco.py` / `doctrine.py`: parent lines **removed or edited** | **0 / 0 / 0** (+12 / +119 / +86 added) |
| module-level defaults deriving from a v537 flag (the v515 finding-3 hazard) | **0 across the whole tree** |
| v537 flags never read anywhere (dead flags) | **0** |
| flag reads **outside** a function body | **0 of 6** |

The six read sites: `eco.py:623, 625, 638, 645, 656` and `main.py:1556`.

**Every guard is driven to both verdicts** — synthetic offender → 1 module-level
hit, cleaned → 0; offender read `in_function=False`, cleaned `in_function=True`.

⭐ **THE DEAD-FLAG POSITIVE CONTROL, AND IT FIRED FOR REAL.** A read-site
scanner that cannot say *"nobody reads this"* cannot certify *"everybody reads
this in a body"* — both verdicts come out of the same walk. The control builds a
synthetic tree with one flag defined and never read; the scanner must name it,
and must fall silent once it is wired up. **It then caught a live defect in this
build**: adding `FS_V537_RAIDER_CLAIMS` to the scanner's flag set without adding
it to the synthetic fixture made the whole run report **FLAGSCAN FAIL** while
every printed line above it read OK. The guard fired on a real change, not only
on a designed mutant.

### 7.2 Behavioural — 300 local NOISE_OFF identity games

`scratchpad/s52_v537_build/ident2/`, `03:32:24-03:33:54Z` — **re-run on the
FINAL bytes** after `FS_V537_RAIDER_CLAIMS` was added in §6.1; the first pass
(`ident/`, `03:09:13-03:10:29Z`) gave identical verdicts on the pre-sub-flag
tree. **Every bot in the fixture is NOISE_OFF, including the
opponent** (`opp_off` = `bots/_v488beltbreak2` with `NOISE_ON = False`). Maps
glacierkeep, drakkarfjord, auroraveil, yulerune, icefloe; seeds 1-5; both seats
= **50 cells per arm**. Compared on every column except `tag`, `arm` and
`winner` — ⛔ `winner` carries the winning bot's **directory name**, so it reads
`par_off` in one arm and `v537_off` in the other for the identical outcome;
`ours` (US/OPP/NONE) carries the same outcome team-neutrally and **is**
compared, as are `cond`, `turn`, `tracebacks`, `ours_mined`, `opp_mined`.

| arm | what it is |
|---|---|
| `par_off` | `_v536trustport`, NOISE_OFF |
| `par_twin` | a **byte-identical copy** of `par_off` — the fixture's determinism control |
| `v537_off` | `_v537socket`, NOISE_OFF, flag **ON** |
| `flagoff_off` | `_v537socket`, NOISE_OFF, `FS_V537_SOCKET = False` |
| `mut_off` | `v537_off` with `FS_V537_MAX_SOCKETS 2 → 8` |
| `win0_off` | `v537_off` with `FS_V537_BY_ROUND 4 → 0` |

| pair | shared cells | **rows differing** |
|---|---|---|
| `par_off` vs `par_twin` *(determinism control)* | 50 | **0** |
| `par_off` vs **`flagoff_off`** | 50 | **0** |
| `par_twin` vs `flagoff_off` | 50 | **0** |
| `par_off` vs `v537_off` | 50 | **50** |
| `flagoff_off` vs `v537_off` | 50 | **50** |
| **`win0_off`** vs `par_off` / vs `flagoff_off` | 50 | **0** |
| `win0_off` vs `v537_off` | 50 | **50** |

⭐ **`win0_off` IS THE DOSE PROOF AND IT IS A SINGLE INTEGER.** Setting
`FS_V537_BY_ROUND` to 0 closes the window before any builder can act and
reproduces the parent **exactly, 0 of 50**, while `= 4` differs in **50 of 50**.
One constant, both verdicts, on the tape that matters.

⚠ **`mut_off` IS A NULL MUTANT AND IS REPORTED AS ONE**: `FS_V537_MAX_SOCKETS
2 → 8` reads **0 of 50** against `v537_off`. **The cap never binds** — with
`FS_V537_SIDE_SPREAD` on and a four-round window, the plank claims two seats and
stops on its own. That is a finding about the plank, not a failed control; the
control that had to work is `win0_off`.

**Tracebacks: 0 in all 300 games**, all six arms. Every flag substitution is
applied **at the definition site**, never appended, and `mkarm.sh` prints each
arm's flag lines — **exit code is not the health signal, the flag line is.**

**Direct dose read on the same fixture** (`ringcheck.py` over the kept replays):
median first claim **r22 → r1** on every one of the five maps; own seats at end
**1.60 → 1.92**.

⚠ `_v488beltbreak2` never contests the ring, so **never-claim is 0 % in both
arms here** — this fixture measures *identity* and *dose*, not recovery. The
recovery fixture is §4, against Mjolnir.

---

## 8. FAILURE / WATCH REEL — D16

**This build has watchable games and they are named.** All under
`scratchpad/s52_v537_build/mech/rep/`; each row is a **paired cell** — same map,
same seed, same seat, same opponent version — so the two files differ only by
the plank.

| # | what to watch | treatment | control |
|---|---|---|---|
| 1 | **RECOVERED CRATER.** They plug 6-8 of our ring either way; we hold ours from r1 and deliver 171, they hold nothing and deliver 0 for a full 1000 rounds. | `v537socket_glacierkeep_s1_B` — claim **r1**, plugmax 6, deliv **171**, **WIN r651** | `v536trust_glacierkeep_s1_B` — **never**, plugmax 8, deliv **0**, LOSS at r1000 on `titanium_collected` |
| 2 | **THE FIRST-CLAIM SEQUENCE.** The r1 conveyor going down on the seat, nine rounds before their first plug at r5. | `v537socket_yulerune_s5_A` — claim **r1**, deliv 128, **WIN r182** | `v536trust_yulerune_s5_A` — **never**, deliv **0**, LOSS r227 |
| 3 | ⭐ **THE FALSIFIER / COST CELL.** Both arms claim; the parent claims at r21 and kills at r156, v537 claims at r1 and the game drags to r417 and is lost. **This is the §6 surprise on one screen.** | `v537socket_auroraveil_s8_A` — claim r1, deliv 181, **LOSS r417** | `v536trust_auroraveil_s8_A` — claim r21, deliv 35, **WIN r156** |
| 4 | **THE SECOND COST CELL**, same shape on a different map and the opposite seat. | `v537socket_drakkarfjord_s8_B` — claim r1, **LOSS r723** | `v536trust_drakkarfjord_s8_B` — claim r23, **WIN r243** |
| 5 | ⚠ **THE RESIDUAL.** We claim at r1 and *still* deliver zero: they take **7** of the other seats and the trunk never reaches the one we hold. **This is what the next plank is for.** | `v537socket_glacierkeep_s2_B` — claim r1, plugmax **7**, deliv **0**, LOSS | `v536trust_glacierkeep_s2_B` — never, deliv 0, WIN r261 |

**Re-run recipe for any cell:**
```
.venv/bin/fcode run bots/_v537socket bots/_x3r0v169mjolnir \
    maps/<map>.map26 --seed <n> --tle 10 --replay <path>
```
(swap the two bot arguments for a seat-B cell; `bots/_v536trustport` for the
control arm.)

---

## 9. MANIFEST + WHAT THIS BUILD DID **NOT** DO

### 9.1 Instruments — all under `scratchpad/s52_v537_build/`, none committed

| instrument | what it establishes | tape | selftest drives the other way |
|---|---|---|---|
| **`ringcheck.py`** | §3 — supplies the `--selftest` `ringtime.py` lacks, plus the seat-aware projection | — | 6 guards incl. the mis-seat mutant and the anchor-shift mutation |
| **`flagscan.py`** | §7.1 — bytes, module-level AST, read sites | `OUT_flagscan.txt` | offender/cleaned both ways; ⭐ dead-flag control both ways |
| **`rowdiff.py`** | §7.2 — row identity across arms | — | corrupts a **0-difference** pair; 3 mutants each move exactly 1 row |
| **`mechtab.py`** | §4 — the per-map table + paired McNemar | `OUT_mechtab.txt` | perfect flip / no-op / all-claim / all-never synthetic tapes |
| `mkarm.sh` | the six NOISE_OFF arms; prints every flag line rather than trusting `$?` | — | — |
| `mech_drive.sh` | run 1, 2 arms × 300 cells, replays kept | `mech.log`, `mech/` | — |
| `mech2_drive.sh` | run 2, 3 arms × 300 cells (adds `v537noraid`) | `mech2.log`, `mech2/` | — |

Supporting: `PARENT_FREEZE.md5`, `BASELINE_proj.tsv` (the study's 2,700-row
tape projected), `ident/`, `mech/`, `mech2/`, `arms/`, `trees/v537noraid`.
The regression-diagnosis scratch scripts are at
`scratchpad/s52_v537_build/{geom,walk,chainstop,plug,pickorder}.py` with the
instrumented trees `dbg529/` and `v533off/`.

### 9.2 Deferred — named, not hidden

1. ⛔ **ANY CURRENCY READ.** §4's win columns are mechanism evidence at
   n = 60/cell (hw ≈ ±12.6 pp). **The full-pool powered screen against
   `bots/_x3r0v169mjolnir` is the builder's** and is the study's Gate 3.
2. ⛔ **ANY CPU / TLE MEASUREMENT.** The claim adds up to 8 `get_tile_building_id`
   + type/team reads per builder turn **for four rounds only**, then costs
   nothing. Not measured against the 10 ms budget; no CPU claim is made.
3. ⭐ **THE `_pick` ANCHOR ASYMMETRY** (§2.4.2). `abs(t.x - self.core.x)` measures
   from the NW anchor rather than the footprint, and the tiebreak hashes raw
   coordinates — **0 of 6 maps produce mirrored ore slices**. A general
   correctness defect, revealed here, fixed nowhere. **This is the largest
   single item this build found and did not build.**
4. ⚠ **THE GLACIERKEEP RESIDUAL.** We now claim at r1 in 60/60 and still deliver
   nothing in **57 %** of glacierkeep games — they take 6-7 of the *other* seats
   and the trunk never reaches ours (reel row 5). The seat is necessary and not
   sufficient. Candidate next plank: protect the **approach**, not another seat.
5. ⚠ **NO RE-CLAIM AFTER DESTRUCTION.** The window is hard-closed at r4. If they
   shoot the conveyor off the seat at r200 we do not rebuild it. Deliberate —
   a re-claim loop is the tar-pit the study forbids — but unmeasured: end-state
   own-seat count is **2.01**, so it is not currently happening.
6. ⛔ **PORTING `FS_V530_MOUTH` ITSELF.** §2.3 shows it is capped out of the
   craters, so it was **not** ported. Whether MOUTH plus v537 beats v537 alone
   on the two short-haul maps is unmeasured.
7. ⛔ **`mkarm.sh` FOR READ-ONLY SOURCE TREES** — still worked around with
   `chmod -R u+w`, not fixed; `tools/*` edits were out of scope again (v536
   report §8.4 item 6, now two builds old).

---

## 10. HONEST LIMITS

* **The recovery fixture is 5 maps and ONE opponent version.** It is the right
  five (they hold 100 % of the study's recoverable games plus both regression
  cells) and the wrong denominator for a release verdict.
* **`n = 60` per (map, arm) cell** ⇒ half-width ≈ ±12.6 pp on a win share. The
  never-claim readout is what this test is powered for (a >10σ move); **the win
  columns are not, and the two cost cells at −5 and −6 games are inside noise
  individually** — what makes them worth §6 is that they are the *only* two
  cells whose control had no defect, which is a pattern, not a p-value.
* **The regression diagnosis is a source-level + single-flag-control result on
  LOCAL games.** Per directive point 6, that **prioritises** a road; it does not
  retire one. The plank's own recovery is measured against a live holder tree
  in 600 local games, which is still not a live-team leg.
* **The seat-asymmetry causes (§2.4) are diagnosed, not fixed**, and one of them
  is in *their* code and therefore outside our control entirely.
* **No claim is made that v537 ≥ v536 on the full pool.** Three of the fifteen
  pool maps were not touched by this build's fixture at all, and the plank
  spends a builder turn on **every** map, including the ten where the control
  already claims at r2-r8. §6 is the reason that sentence is in this section
  rather than in the top line.
