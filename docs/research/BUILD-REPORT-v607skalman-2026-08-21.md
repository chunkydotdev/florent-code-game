# BUILD REPORT + READ — `bots/_v607skalman` (the one-fix wave)

**Builder s55, 2026-08-21T23:36Z (`date -u` in the same shell).** Copy of
`_v606skalman` + the v607 queue; two fresh opus measurement agents (items 4 and
5); artefacts `scratchpad/s55_v607/`. Fixture = the authored NOISE_OFF
`_v542wave` benchmark copy, 15 pool maps x both seats = 30 games, seed pinned at
7 (map/seat vary, seed never). No game-share claim, no submit, no platform match.

## THE HEADLINE IS ITEM 5, AND IT IS NOT A FIX

**All 19 losses die to ENEMY SENTINEL FIRE ON OUR CORE. 19 of 19. Zero gunner,
~zero peck.** And in **11 of the 19** the core takes exactly **504** damage —
28 sentinel shots at reload 2 — with a **first-hit-to-death window of exactly 54
rounds**. We stand in one enemy gun's line for fifty-four consecutive rounds and
never break it: no heal, no body in the ray, no counter-kill.

Every plank in this wave was aimed at **our own navigation**. The thing that
kills us is **one enemy gun with a clear line**, and nothing in the tree contests
it.

## THE OTHER HEADLINE: FOUR ITEMS, FOUR NULLS OR NEGATIVES

| | v606 (`tape_FINAL`) | **v607 (`tape_FINAL`)** |
|---|---|---|
| kills / 30 | 11 | **11** |
| **by-r300** (primary) | 10 | **10** |
| median kill round | 160 | **160** |
| our core dead | 19 | 19 |
| builder deaths | 23 | 23 |
| belt deaths | 39 | 39 |
| sentinels built | 60 (>=2 in 25) | 61 (>=2 in 25) |
| 2nd-gun median round | 60 | 60 |
| M1 belt connectivity A/B | 42.1 / 34.5 | **42.1 / 34.5** |

**8 of 30 replays changed; not one column did.** The axis the wave was called to
move — kill COUNT and by-r300 — is unchanged for the **fourth** release running
(v604 8/6, v605 9/6, v606 11/10, v607 11/10).

## Item 1 — the RE-ARM defect: FIXED, PREDICTION CONFIRMED, NULL ON THE PRIMARY

`SK_NEST_STUCK_FIX`, two halves in `_nest_site_watch` and its one caller:
* **the sticky re-arm** — a re-site event (`_nest_watch` on a turret death,
  `_plant_gun` on a success) drops `nest_site`, the engineer re-picks, and the
  v606 code restarted the clock **even when `_pick_nest` returned the same
  tile** — i.e. from inside the orbit. Now the clock survives an identical
  re-pick;
* **the progress test** — was per-round closest approach, which never fires on a
  persistent orbit and fires spuriously on a body walking AROUND a wall. Now it
  is **net displacement from an anchor tile**, re-anchored the moment the body
  leaves a `SK_NEST_STUCK_BOX` box. `SK_NEST_STUCK_FAR = 60` is kept as the
  backstop for the original UNREACHABLE-site case, which has a large net
  displacement by construction.

**⭐ THE PREDICTED EFFECT APPEARED — the sweep straightened out.**

| `SK_NEST_STUCK_ROUNDS` | 25 | 40 | 60 |
|---|---|---|---|
| v606 (broken re-arm) by-r300 | 10 | **9** | 10 |
| **v607 (fixed re-arm) by-r300** | **10** | **10** | **10** |
| v607 median kill | **160** | 187 | 189.5 |
| v607 kills | 11 | 11 | 12 |
| v607 builder deaths | 23 | 46 | 26 |

by-r300 is now flat and median kill is **monotone in the constant**. On the
stated ship rule (by-r300, then median) **25 stays**.

**⛔ THE CELL REQUIREMENT WAS NOT MET, and the honest reading is that the cell
answers to the CONSTANT, not to the re-arm.** helheim seat A wins at
`STUCK = 60` (r139) and loses at 25 and 40 — under the broken re-arm AND under
the fixed one. The 12th kill that 60 buys lands **past r300** (by-r300 stays
10), which the programme prices at 0.82 against us, and it costs 30 rounds of
median. So the trade is declined and the cell is banked as unresolved rather
than as fixed.

**Ablation, both ways, on the shipped chassis:** OFF is **byte-identical in all
30 replays** to the v606 shipped tape. The sub-constants are a dose curve, all
tying the primary at by-r300 10 / median 160: `BOX` 0 / 2 / 6 → 4 / — / 2
replays differing from ship, `FAR` 25 / 60 / 999 → 3 / — / **0**.
**⚠ DISCLOSED: `FAR` is INERT on this fixture** (999 is byte-identical to 60), so
the backstop is carried as a guarantee about the unreachable-site case and not
as a measured lever.

**Where it is visibly better:** paths seat A plants its second sentinel at
**r164 instead of r175**, from one body, with 5 builds instead of 4.

## Item 2 — PURCHASE ORDERING: mechanism works, outcome inverted, road closed

`SK_S2_PRIORITY` — inside the S1→S2 window only, and only while the engineer is
alive (read off `SK_SLOT_NEST`, which the engineer already published and which
until now **no consumer read**), the home keeper defers **door-gunner**
purchases and the ore denier defers its **non-seal (ore-denial) barriers**. The
drip, standing guns, the cage seal barrier, the engineer's own prep barriers,
the belt and the harvesters are untouched.
*(Role attribution corrected against the brief: the core buys no gunner — the
HOME KEEPER does — and the CAGE WALKER's only barrier IS the seal.)*

| on the v607 shipping chassis | OFF | ON |
|---|---|---|
| kills | 11 | **9** |
| **by-r300** | 10 | **8** |
| median kill | 160 | 150 |
| builder deaths | 23 | **37** |
| 2nd-gun median round | 60 | **53** |
| funding-wait games / rounds | 15/30, 783 | **14/30, 678** |

**It does exactly what it was built to do** — the second gun lands 7 rounds
earlier and 105 waiting rounds disappear — **and it costs two by-r300 and
fourteen builder deaths.**

**⭐ ATTRIBUTED, which is what makes the negative useful:**
* `SK_S2_DEFER_GUNS` alone reproduces the ON arm **byte-identically in all 30
  replays**;
* `SK_S2_DEFER_BARRIERS` alone is **byte-identical to OFF** — an exact null. Ore
  denial barriers are not what the engineer is waiting on;
* `SK_S2_PRIORITY_MAX` 120 → 60 is **byte-identical to ON**, so no deferral ever
  ran past 60 rounds and **the bound is not the problem**.

⇒ **SECOND ROAD CLOSED ON THE ALLOCATION QUESTION.** v606 refuted *cutting* door
gunners (`SK_DOOR_GUN_CAP` 2→1, by-r300 10→6); v607 refutes *deferring* them.
The funding wait is real, it is 678–783 rounds of S1→S2, and **it cannot be paid
for out of the home guns.**

## Item 3 — CONDITIONAL BLOCK-MEMO: the split is REFUTED

Three scopes, gated by a 3-game probe first (the v606 discipline):
`0 ALL` (v606's global form) / `1 FORWARD` (walker, engineer, denier) /
`2 FAR` (target d² > 50).

**The probe already said no.** On helheim seat A, **every** scope makes the game
end at **r135 with our core dead** instead of **r388 with our core dead**, and
lap coverage does not improve (4/12 → 3–4/12). fimbulwinter seat A is identical
under all four arms; seat B costs 18 rounds under scopes 0 and 1.

The 30-game arms were bought anyway (the fixture is free) and agree:

| arm | kills | by-r300 | median | builder deaths |
|---|---|---|---|---|
| control (ship) | 11 | **10** | 160 | 23 |
| scope 1 FORWARD | 11 | 9 | **198** | 28 |
| scope 2 FAR | 9 | 8 | 160 | 23 |

**The +38 median follows the memo wherever it is switched on.** The cost is not
carried by the home keeper's short routes and is not avoided by restricting the
memo to long ones. ⇒ **the conditional split is refuted**; the memo stays off.

**⛔ AND A METHOD CORRECTION THAT MATTERS BEYOND THIS ITEM.** v606's probe scored
this same cell as *"our total deaths 12 → 5"* **without normalising for game
length** — and the memo shortens that game from 388 rounds to 135. **Fewer deaths
in a third of the rounds is not fewer deaths.** The v606 probe's pass was partly
an artefact of that.

## Item 4 — NET-DISPLACEMENT STALL: detector validated, RESPONSE refuted

Constants were **measured, not taken from the brief** (`orbit_geom.py`, 30 games,
24 labelled period-k episodes of ≥30 rounds):
* **⛔ the brief's `box ≤ 2` is refuted by the brief's own headline cell** —
  fimbulwinter seat A bot 8 (ORE_DENIER, k=12, 130 rounds) has box **3** in
  **107 of 107** windows, so `max(dx,dy) ≤ 2` covers it **0%** of the time.
  Coverage by threshold: B1 8/24 · B2 16/24 · **B3 20/24** · B4 22/24.
* the two episodes B3 misses are 1-tile-wide **shuttles** with boxes of 8 and 10
  — no net-displacement threshold reaches them, the period detector does, so
  **both detectors stay**;
* the move test is nearly free (every episode moves ≥17 of 23) and its whole job
  is excluding standing-still: **0 pure standing-still fires at any M ≥ 8**,
  against **5,430** windows the box test alone would sweep in;
* overlap with the shipped period detector is **31.8%** — 68.2% of fires are new,
  and shipped k≤6 sees ≥half the windows of only 5 of the 24 episodes. **W=16 is
  rejected on measurement**: its episode count is non-monotone in M (24 at M=8,
  78 at M=12), while W=24/32 are stable.

Shipped constants: **W=24, BOX=3, MOVES=12, COMMIT=14.**

| arm | kills | by-r300 | median | builder deaths |
|---|---|---|---|---|
| control (ship) | 11 | **10** | 160 | 23 |
| netdisp BOX 3 | 9 | 8 | 160 | 29 |
| netdisp BOX 2 (fewer fires) | 11 | 9 | 170 | 25 |

**A MONOTONE DOSE CURVE IN FIRE VOLUME**, which is what makes this a readable
negative rather than a null: **the harm scales with how often the commit window
opens**, so it is the **response**, not the threshold, that costs. The census
warned of exactly this — **66 of 99 fire episodes land on a body that is
orbiting WHILE BUILDING** (lifetime action rate ≥ 0.05 acts/round). Freezing
that body's movement target is not free.
⇒ **v608: a period-free orbit needs a response that is not "commit to the current
target".** The detector is validated and stays in the tree behind an OFF flag at
zero cost.

## Item 5 — THE LOSS ANATOMY (measure only)

Instrument `scratchpad/s55_v607/loss_anatomy.py`, all four controls fired
(channel-classifier mutation drove all 4 verdicts; S2-overlap mutation drove
both; count cross-check against `summary.py`; won-games complement group differs
on all three probed columns). 826 core-damage events, 0 mis-attributed.

```
map+seat              ourdeath  channel   sent/gun/peck/oth nS born             S2ever S2stood   2nd  cage(H/E/O)
-----------------------------------------------------------------------------------------------------------------
auroraveil_seatB           232 sentinel           504/0/0/0  2 19,144              yes      no   144        6/1/1
bifrost_seatA              157 sentinel           504/0/0/0  2 25,39               yes     yes    39        3/2/3
glacierkeep_seatB          171 sentinel           810/0/0/0  2 27,37               yes     yes    37        6/2/0
helheim_seatA              387 sentinel           504/0/0/0  3 15,59,79            yes     yes    59        1/4/3
helheim_seatB              131 sentinel           504/0/0/0  1 15                   no      no     -        2/3/3
holmgang_seatA             203 sentinel          1044/0/0/0  2 19,28               yes      no    28        5/1/2
holmgang_seatB             673 sentinel          486/0/20/0  3 21,27,247           yes     yes    27        0/2/6
icefloe_seatB              262 sentinel           504/0/0/0  1 32                   no      no     -        5/2/1
jotunheim_seatB            180 sentinel           504/0/0/0  2 67,76               yes     yes    76        7/0/1
longhouse_seatA             94 sentinel           504/0/0/0  1 93                   no      no     -        5/1/2
longhouse_seatB            115 sentinel           504/0/0/0  2 65,79               yes     yes    79        4/4/0
midgard_seatA               95 sentinel           504/0/0/0  2 47,51               yes     yes    51        0/3/5
midgard_seatB               95 sentinel           504/0/0/0  2 51,92               yes     yes    92        0/3/5
paths_seatA                243 sentinel           900/0/0/0  2 42,164              yes      no   164        2/3/3
paths_seatB                137 sentinel           702/0/0/0  2 36,44               yes     yes    44        0/3/5
stavkirke_seatA            673 sentinel          2952/0/0/0  2 32,69               yes     yes    69        6/1/1
valkyrie_seatA             107 sentinel           504/0/0/0  2 34,48               yes     yes    48        1/4/3
valkyrie_seatB             118 sentinel           504/0/0/0  1 32                   no      no     -        2/4/2
yggdrasil_seatA            115 sentinel           504/0/0/0  2 41,46               yes     yes    46        3/1/4

AGGREGATE (LOST, n=19)   channel sentinel=19 · S2 stood yes=12 no=7 (ever built
  15/4) · our core died 19/19 · median death r157 · 2nd-sentinel median r51 ·
  cage at death median held=3 enemy=2 empty=3
AGGREGATE (WON,  n=11)   channel none=7 sentinel=4 · S2 stood yes=10 no=1 ·
  core died 0/11 · cage at end median held=7 enemy=1 empty=1
```

**What it says, in order of size:**
1. **ONE CHANNEL.** 19/19 sentinel. There is no second way we die on this
   fixture, so there is no second thing to defend against.
2. **NO CLOCK LOSSES AT ALL.** losses == our-core-dead == 19. The r1000 tail does
   not exist here; we die.
3. **THE 54-ROUND WINDOW.** 11 of 19 rows are exactly 504 damage = 28 shots, and
   in those the first-hit→death window is 54 rounds (52–63 across the class).
   **Fifty-four rounds of continuous fire on our core, never once interrupted.**
4. **S2 leans but does not decide:** S2 stood in 63% of losses vs 91% of wins;
   4 losses never built two sentinels at all (longhouse seat A built **one**, at
   r93, and died at r94).
5. **The cage is collapsed at death** — held 3 / enemy 2 / empty 3 in losses
   against 7/1/1 in wins, with four losses at held = 0.
6. **Outlier: stavkirke seat A** took **2,952** core damage over 164 events
   across a 615-round window before dying at r673. We healed and rebuilt through
   it for most of the game and still lost the race.

⚠ **n = 19 is fragile for a median:** one game (jotunheim seat B, r136→r180)
moves the loss-side median death round by 20 rounds between the v606 and v607
tapes. Do not lean on that median.

## Verification

Static **9/9 scans PASS, 34/34 dirty controls FIRE** (12 new v607 controls; the
v605 S7 assertion and its control were repaired — v607 added `use_memo` to the
nav-template cache key and **the stale anchor made one existing control fire for
the wrong reason**, which is exactly the failure a control battery is supposed to
catch in itself) · aliveness **12 games both seats, 0 tracebacks, 0
exception-removals**, injected-NameError control fires 8/8 with 8 no-damage
removals · **IDENTITY CONTROL: every v607 flag OFF is byte-identical to the v606
shipped tape in all 30 replays** — the refactor (nav-template signature, memo
scope, ring cap, two-slot cache) is provably inert when the flags are off ·
cells: helheim_A **still FAILS** (4/12, disclosed above), midgard A/B PASS both,
fimbulwinter orbits unchanged at 130r/77r with both games killing at r160/r150,
paths_A the engineer plants its second gun at **r164 (was r175)** from one body ·
fidelity **per seat**: drip lattice **100.0/100.0** (bar 97.3), M4 band
96.7/96.4, **point-blank 0/0**, M1 **42.1/34.5** (v606 parity) · per-shipped-flag
ablation both ways plus a 4-point dose curve on each sub-constant, all re-run on
the exact shipped chassis · `summary.py --check` positive control OK (34 / 46) ·
tape reproduced from the shipped tree after the docstring edit, **0/30 differ** ·
CPU wall-clock 6 games 8.95s (v606) → 9.02s (v607), **0 engine timeouts** ·
**platform match test STILL OWED.**

## v608 queue

1. **⭐ THE 54-ROUND WINDOW.** 19/19 losses are one enemy sentinel line, and in
   11 of them we absorb 28 consecutive shots without contesting it once. Cheapest
   candidates, in order of what the tape can already price: (a) **stand a body in
   the ray** — a sentinel's shot is a single-tile line and a builder body is a
   legal absorber; (b) **heal the core** — 1 Ti for +4 HP against 9 dmg/round is
   a losing rate alone but changes the 54 rounds into something longer while a
   counter is built; (c) **kill the gun** — 2 Ti/peck into 40 HP is 20 builder
   turns, and the tape says which body is nearest. Pick ONE and pre-register it.
2. **The response to a period-free orbit.** The netdisp detector is validated and
   its commit response is refuted with a monotone dose curve. Find a response
   that does not freeze a building body's target.
3. **The allocation question, now with two roads closed.** Cutting door gunners
   (v606) and deferring them (v607) both sell the kill. The remaining levers are
   the SECOND GUN'S COST (scale discipline elsewhere) or a different income.
4. **helheim seat A** — wins only at `SK_NEST_STUCK_ROUNDS = 60`, under both the
   broken and the fixed re-arm. It is the constant, not the guard. Decide whether
   that cell is telling us something about the map or about the constant.
5. **Constant-target orbits** — still 34.6% of orbit-rounds, still a
   `_nav`/`_bfs_direction` defect that no commit window reaches. Untouched by
   v607.
6. Standing: platform CPU test owed.

## Progression on the fixture (identical opponent, 30 games)

kills 0→0→6→8→9→11→11→**11** · by-r300 —→—→5→6→6→10→10→**10** ·
median kill —→—→198→256→275→208→160→**160**.
FIRST-CONTACT GATE: **NOT MET** (11/30 does not beat the screen). **This wave
moved nothing on the primary and spent four items finding that out** — three of
which came back with a mechanism confirmed and an outcome inverted, the sixth,
seventh and eighth such case in this line. The product of the wave is item 5.
