# PREREG — LOKI-29 SEAT-RELATIVE SCAN ORDER

**Author:** builder arm, s32. **Committed:** 2026-08-11, before the query in §4
has been run even once. **Two-clock standard applies:** this file's git author
time must precede the timestamp on the analysis output, and §4 exists precisely
so that a free archive test is not fitted after the fact.

---

## 1. THE CHANGE, named to the constant

`bots/_v151seatrel` vs the live tree `bots/_v148ferryfirst` (v112). Two files:

* `doctrine.py:26` — `CARDINALS = [NORTH, EAST, SOUTH, WEST]`, a **fixed
  absolute order**, consumed by 20+ **first-match-wins** scans across
  `main.py` (`:480 :551 :617`), `eco.py` (`:330 :391 :433 :465 :511 :682 :812
  :919 :975 :1029`) and `raid.py` (`:271 :296 :317 :349 :422 :558`).
* new `doctrine.orient_cardinals(core, enemy)` rotates that list **in place** so
  the scan starts at the cardinal facing the enemy Core, **preserving the
  clockwise 4-cycle**; called once per Core turn from `main.py:156`.

**In place, not rebound**: all three modules do `from doctrine import *`, which
binds the list *object* into three namespaces. Rebinding `doctrine.CARDINALS`
would leave all three pointing at the old list and change nothing.

**The cycle must survive the rotation** because `eco.py:588-590`, `:703-711` and
`:743-744` take `CARDINALS[(i±1) % 4]` as *the two perpendiculars of `desired`*.
A non-rotational reorder silently turns "perpendicular" into "opposite" at three
live sites. A rotation cannot. This is asserted in the fixture, not argued.

## 2. WHY — the premise, measured three times on three populations

| source | population | seat A |
|---|---|---|
| research, algebraic, off the nine-arm screen | screen arms | 54.126% |
| side lane, byte-identical arms | self-play | 53.91%, z=3.54 |
| **this session's overnight NULL shard** | **byte-identical, n=4693** | **52.6% vs B 45.8%** |

and the same A>B ordering appears in **all seven** of tonight's shards. A
third-party bot on the same 8 maps reads 51.76% (n.s.), so maps account for
~1.8pp and the residual is ours. **Half of every game is played on the wrong
side of a self-inflicted gap.**

## 3. ⛔ WHAT THIS PLANK IS *NOT*, STATED BEFORE ANY RESULT

**Closing the seat gap is direction-neutral by construction.** In a byte-identical
null the two seats' rates must average 50%; canonicalising them makes both seats
play *the same way*, and nothing in that argument says which way. If both seats
converge on the WORSE seat's behaviour, the currency **falls**.

⇒ **The mechanism bar (§5) and the currency bar (§6) are separate, and clearing
the mechanism bar is NOT a ship argument on its own.** Any write-up that reports
a closed seat gap as if it were a win rate is wrong.

## 4. ⭐ THE FREE FALSIFIER — RESOLVED OFF DATA THAT ALREADY EXISTS, BEFORE ANY NEW GAME

If the absolute scan order is what produces the seat gap, then **the favoured
seat is the one whose enemy lies EARLIER in `[NORTH, EAST, SOUTH, WEST]`** — and
which seat that is **is a property of the map**, not of the seat.

Real Core anchors, read off the `.map26` protobuf `Map.cores` and cross-checked
against two live replays (15/15 pool maps, NW corner of the 2x2, both seats):

| map | coreA | coreB | A's enemy dir | rank | B's enemy dir | rank | **PREDICTED FAVOURED SEAT** |
|---|---|---|---|---|---|---|---|
| atoll | (2,14) | (14,2) | EAST | 2 | WEST | 4 | **A** |
| drumlin | (5,5) | (18,18) | EAST | 2 | WEST | 4 | **A** |
| fjordgate | (2,2) | (6,6) | EAST | 2 | WEST | 4 | **A** |
| heart | (7,9) | (19,9) | EAST | 2 | WEST | 4 | **A** |
| hive | (2,20) | (21,3) | EAST | 2 | WEST | 4 | **A** |
| antler | (6,4) | (6,12) | SOUTH | 3 | NORTH | 1 | **B** |
| meander | (11,3) | (11,10) | SOUTH | 3 | NORTH | 1 | **B** |
| nordkap | (9,6) | (9,18) | SOUTH | 3 | NORTH | 1 | **B** |

**PREDICTION, committed here: on the byte-identical NULL shard
(`scratchpad/overnight/NULL.tsv`, n≈4693, ~587 games/map), seat A's win rate is
ABOVE 50% on atoll, drumlin, fjordgate, heart and hive, and BELOW 50% on antler,
meander and nordkap.**

**WHY THIS IS A REAL TEST AND NOT A RESTATEMENT OF THE POOLED NUMBER — the
inversion is the whole point.** The pooled seat gap (A 52.6%) is equally
consistent with a *turn-order* advantage, which is the obvious rival explanation
and one we cannot change. **But turn order is CONSTANT across maps: it would push
every map the same way and can NEVER produce an inversion on a predicted subset.**
So:

* **8/8 or 7/8 in the predicted direction ⇒ the CARDINALS story is supported and
  turn order is ruled out as the sole cause.**
* **A pattern that does not invert — seat A above 50% on all or nearly all 8 —
  ⇒ THE PREMISE OF THIS PLANK IS WRONG.** The gap is turn order or something
  else, the arm cannot fix it, and **LOKI-29 is withdrawn without spending a
  single game.**
* 6/8 or fewer, mixed: unresolved; falls back to §5.

**Under the null of no relationship, P(8/8) = 1/256 and P(≥7/8) = 9/256 = 0.035.**
Per-map n≈587 gives a per-map SE of ~2.1pp, so a map whose true rate is 50.0%
lands on the wrong side of the line about half the time — **this test has real
power against a LARGE per-map effect and little against a small one.** It is
therefore run as a **falsifier**, not as a confirmation: a clean inversion is
strong evidence; a failure to invert is what actually resolves it.

**GATE, per the standing rule that a resolution table covers every GATE and not
only every BAR:** the query must return **8 maps each with n ≥ 400**. If any map
is short, that map is reported and excluded, and the denominator of the
count-of-8 changes with it.

## 5. MECHANISM BAR — the seat gap itself

Fixture: byte-identical null, `_v151seatrel` vs a byte-identical copy of it,
same harness and same 8 maps as tonight's NULL shard, **n = 5,408** (a multiple
of 16 = 8 maps × 2 seats, so seat/map balance is exact).

* **Control, already measured tonight:** |seat A − seat B| = **6.8pp** (52.6/45.8).
* **BAR: the absolute seat gap falls below 3.0pp.**
* Per-seat n = 2,704 ⇒ SE on the gap ≈ 1.9pp. A fall from 6.8pp to ~0 is ~3.5 SE;
  **a fall to 3.0pp is ~2 SE and is the most this n can honestly ask for.**

## 6. CURRENCY BAR — `PRIMARY_CURRENCY: game_share`

Fixture: `_v151seatrel` vs `_v148ferryfirst`, n = 5,408, same harness.
`WIN_RATE_IS_VERDICT: yes`, and the ship rule is a positive point estimate + a
verified mechanism + no programme breach.

* **Report game share with the `overnight_read.py` informative band.** At
  n=5,408 that band is ≈ [48.6%, 51.4%].
* **This is an OFFENSIVE/correctness plank, not a defensive one, so
  `DEFENCE_ADMISSION_BAR` does not apply.** Median kill round is reported anyway
  as a non-regression *observation*, not a bar.

## 7. WHAT WOULD MAKE ME WITHDRAW IT

1. §4 fails to invert ⇒ withdrawn immediately, no games spent.
2. §5 bar missed with §6 also below 50% ⇒ the canonicalisation converged both
   seats on the worse behaviour; withdrawn.
3. Any traceback from the arm in a smoke run. *(Checked: 0 tracebacks, and note
   `main.py:116` swallows exceptions into a one-shot stderr report, so "the game
   ran" is NOT evidence of correctness — the dose was verified positively
   instead, see §8.)*

## 8. DOSE, ALREADY VERIFIED ON THE ENGINE

One live game on antler, both seats instrumented at `orient_cardinals`:

```
core=(6,12) enemy=(6,4)  order=[NORTH, EAST, SOUTH, WEST]
core=(6,4)  enemy=(6,12) order=[SOUTH, WEST, NORTH, EAST]
```

Exact point reflections of each other, 0 tracebacks. Probe removed; tree diff is
`doctrine.py` + 6 lines of `main.py`. Fixture `tests/test_seat_relative.py`
drives **both** verdicts: 11/11 maps canonicalise under treatment, **0/11 under
the shipped absolute order** (the negative cell — without it a check that passes
on everything looks correct).

## 9. KNOWN LIMITATION, RECORDED BEFORE THE RESULT

**meander's anchors are NOT a point reflection** — (11,3)/(11,10) on 25x15,
where reflection would give (12,10). The rotation still puts the enemy first for
both seats there (the anchors differ only in y, so the two enemy directions are
still exact opposites), but the **handedness of the two perpendiculars is not
canonicalised on that map.** 1 of 8 battery maps. `fcode maps list` labels
meander `rotational`; the anchor geometry says otherwise, and **a CLI label is
not ground truth about anchor geometry** — I asserted the CLI version first and
it was wrong.
