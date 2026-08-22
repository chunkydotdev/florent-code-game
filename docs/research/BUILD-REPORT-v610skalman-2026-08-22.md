# BUILD REPORT + READ — `bots/_v610skalman` (the belt-termination wave)

**Builder s54, 2026-08-22T02:02Z (`date -u` in the same shell).** Copy of
`_v609skalman` + the v610 commission (belt-termination axis). Artefacts
`scratchpad/s54_v610/`. Fixture = the authored NOISE_OFF `_v542wave` benchmark
copy, 15 pool maps × both seats = 30 games, seed pinned at 7 (map/seat vary,
seed never). No game-share claim, no submit, no platform match, no commit.

---

## 0. THE RE-VERIFY CENSUS, FIRST, BEFORE ANY CODE

New instruments, both built for this wave and both driven to the other verdict:
`scratchpad/s54_v610/census.py` (**5/5 controls fire**) and
`scratchpad/s54_v610/seatlife.py`. Run on the v609 SHIPPED tape, re-derived in
this shell from the committed tree (`tape_v609base`, which reproduces v609's
published read exactly: kills 13, by-r300 10, median 170, core-dead 16, M1
33.3/34.5, waits 18/30).

**THE BRIEF'S PREMISE HOLDS. THE CLASS HAS NOT MATERIALLY MOVED IN FIVE
VERSIONS.**

| | tape602 (v602) | **v609 tape** |
|---|---|---|
| **ONE-BARRIER CLASS** (blocked → exactly gap 1 with enemy barriers passable) | 33/76 = **43.4%** | 26/68 = **38.2%** |
| gap 0, route home complete | 29/76 = 38.2% | 31/68 = **45.6%** |
| one-build-from-home TOTAL (incl. own-gap) | — | 30/68 = **44.1%** |
| enemy-held delivery seats at end | median 6.5 of 8 | **median 6.5 of 8** |
| first enemy building on a seat | median r11 | **median r11**, 30/30 games |
| games ending with a clear seat ring | 0/30 | **0/30** |

⛔ **ONE OPERATIONAL CORRECTION TO THE tape602 WORDING, and it matters because
the wrong form reads 0 on every tape.** "One barrier from a complete route" is
**not** `gap>0 → gap 0` under the control — the barrier's own tile still costs
one build once it is cleared. The correct counter is `blocked → exactly gap 1`.
Written the first way this census read **0/68**; written correctly it reads
26/68 and reproduces tape602's form. The first version of my own instrument had
this bug and the control battery is what exposed it.

**AND TWO FACTS THAT NAIL #73's PREMISE:**
* **180 of the 220 enemy barriers standing anywhere on the board at end of game
  (81.8%) sit on OUR EIGHT DELIVERY SEATS.**
* the seat kind census is **42,458 barrier tile-rounds, 142 sentinel, ZERO
  conveyor** — an enemy barrier on a delivery seat can never qualify as
  repairable, only as clearable.

### ⭐ AND THE CAUSE IS A TRIGGER, NOT A BUDGET AND NOT A HEALING RACE

Per-episode seat lifecycle, same 30 games:

```
206 enemy occupancy episodes on our 8 seats            (6.9/game)
we EVER peck                       25 of 206  = 12.1%
on seats we ever touch we peck     78.1% of episodes AND KILL THEM
distinct seats ever pecked         0.80/game of a median 8;  ZERO in 12/30 games
⇒ 84.5% of episodes sit on a seat the tree never once considers
```

**The verb works. It is never aimed.** `_belt_evict` can only fire on a tile
that is in `belt_plan` AND orthogonally adjacent to the keeper, and the
single-source planner terminates on ONE seat per chain.

### ⛔ TWO HYPOTHESES MEASURED AND REFUTED BEFORE WRITING A LINE

1. *"`belt_ban` closes the seats and the plan re-routes into nothing."*
   Instrumented live on glacierkeep seat A — the 8/8-held, 3-harvesters-
   unreachable game: **`belt_ban` is EMPTY for all 201 rounds** and the planner
   re-plans exactly 3 times. **REFUTED.**
2. *"`SK_COLLAR_PECK_CAP` is a per-TILE lifetime ledger, so a re-laid barrier is
   unattackable."* **True as a mechanism** and visible in that same trace: we
   spend exactly 15 pecks on seat (13,2), kill it r48, seal it r49; they kill
   our seal r145 and **re-lay at r146**, and the tile is never contested again.
   **But it is 8 of 206 episodes (3.9%) tape-wide and its complement control
   reads the SAME attack rate (12.5% vs 12.1%). REFUTED AS THE DOMINANT CLASS**
   — fixed anyway, because it binds the moment the trigger widens.

### PLANK 3 (SK_RELAY_SEAL): NOT BUILT — NULL BY INCUMBENT GREP

The brief conditioned it on this read and the read says no. After an enemy
building on one of our seats dies, **OUR seal stands at median latency 1 round
(15/17 within 1r)**. Their re-lay after our seal dies is **also median 1
(16/17)**. We already deny the re-lay race at the speed the plank was going to
buy, and the exchange is symmetric. Flag exists, greppable, **no code behind
it** — asserted by a static scan with its own dirty control.

---

## 1. THE HEADLINE: ONE PLANK SHIPS, ONE IS A CLEAR NEGATIVE

Every arm below is 30 games on the shipped chassis, re-run and never reused.

| arm | kills | **by-r300** | med kill | core-dead | belt D | bot D | Ti |
|---|---|---|---|---|---|---|---|
| v609 base **= all-flags-off (byte-identical, 30/30)** | 13 | **10** | 170 | 16 | 42 | 29 | 14,640 |
| **v610 SHIP (PLANK 2 only)** | **14** | **11** | 188.5 | 16 | 40 | 29 | 12,940 |
| PLANK 1 ON (both planks) | 11 | **7** | 272 | 17 | 32 | 41 | 12,750 |
| PLANK 1 alone | 11 | **7** | 272 | 18 | 31 | 41 | 14,300 |
| SK_SEAT_GUNS ON (turret half) | 12 | **9** | 194 | 16 | 34 | 25 | 15,530 |

---

## 2. PLANK 2 — SK_TERMINATE: SHIPPED, AND ITS EFFECT IS ONE FULLY-ATTRIBUTED GAME

`_route_gaps` already named the tiles that are the SOLE missing link on a live
harvester's route home; its only consumer was `SK_COLLAR_ROUTE_GATE`, shipped
OFF since v603, so the set was computed every round and thrown away. Two halves:
the belt runs **before** `_harvester_action` while a one-gap tile exists
(`SK_TERM_FIRST`), and the keeper's walk target prefers a one-gap tile
(`SK_TERM_MOVE`).

**by-r300 10 → 11, kills 13 → 14, core-dead 16 → 16.**

⭐ **SIX REPLAYS DIFFER AND THE WHOLE GAIN IS ONE CELL: stavkirke seat A goes
from a r1000 TIEBREAK to a CORE KILL AT r294** — a programme-defined defeat
(`R1000_IS_DEFEAT`) converted into a by-r300 win. **A +1 on n=30 is not
separable from noise and this report does not claim otherwise; what makes it
bankable is that the mechanism, the cell and the sign all agree and the
footprint is inspectable.**

⛔ **TWO APPARENT COSTS, BOTH ARTEFACTS OF THAT SAME GAME, both checked rather
than asserted:**
* **median kill +18.5 is NOT a slowdown.** It is a r294 kill being *added* to a
  13-kill population. Of the kills that already existed, one moved 4 rounds
  faster (skald B r122→r118) and one 7 slower (auroraveil A r170→r177).
* **delivered Ti −1,700 is stavkirke alone** (2,470 → 700), because that game now
  ends 705 rounds earlier. Verified per game: the five changed cells sum to
  **exactly** the −1,700 tape delta, and every other changed game is flat or up
  (helheim B dies 25 rounds earlier and still collects MORE: 110 → 120).

**DISCLOSED:** helheim seat B, already a loss, dies 25 rounds earlier
(r169 → r144).

**⭐ ATTRIBUTION — the ACTION half carries the plank:**

| arm | kills | by-r300 | med |
|---|---|---|---|
| both halves (ship) | 14 | 11 | 188.5 |
| `SK_TERM_FIRST` alone (MOVE off) | 14 | **11** | 185.0 |
| `SK_TERM_MOVE` alone (FIRST off) | 13 | **10** | 177 |

**The movement half is an outcome NULL on this fixture and ships ON anyway,
said plainly:** it is the reach half of a plank whose action half pays, every
primary column ties, M1 seat A is marginally better with it (34.2 vs 33.3), and
one authored opponent is not where a reach mechanism would show. **It is the
first thing to cut if this plank is re-priced.**

---

## 3. PLANK 1 — SK_SEAT_CLEAR: MECHANISM CONFIRMED, OUTCOME INVERTED, SHIPPED OFF

The line's **seventh** case of this shape and the clearest one yet.

**IT DOES EXACTLY WHAT IT WAS BUILT TO DO.** Every plank-level signature moves
the right way:

| signature | v609 / ship | **PLANK 1 ON** |
|---|---|---|
| our pecks on our own delivery seats | 329 | **1,347** (4.1×) |
| enemy barriers left on our seats at end | 180 | **162** |
| enemy-held seats at end | median 6.5 | **6.0** |
| belt deaths | 42 | **31** |
| **M1 belt connectivity A/B** | 33.3 / 34.5 | **36.8 / 37.1** (the best this line has read) |
| one-barrier class | 38.2% | **29.6%** |
| funding-wait GAMES | 18/30 | **15/30** |

**AND IT COSTS THREE KILLS AND FOUR BY-R300**, plus: builder deaths 29 → 41,
alive harvesters 68 → 54, unanswered-streak median (v608's own plank) 13 → 19,
total funding-wait ROUNDS 1,030 → 1,471.

**THE DOSE CURVE SAYS THE COST IS THE RESPONSE, NOT THE VOLUME — a STEP, not a
gradient**, which is what makes this a readable negative rather than a tuning
failure:

| dose | by-r300 | kills |
|---|---|---|
| plank OFF | **11** | 14 |
| `SK_SEAT_CLEAR_N = 1` | 6 | 8 |
| `SK_SEAT_PECK_TOTAL = 45` | 7 | 9 |
| `SK_SEAT_PECK_TOTAL = 90` (designed) | 7 | 11 |

**Any amount of aiming the keeper at the collar costs the same four by-r300.**

**THE PRICE, NAMED: the keeper's TURN is the scarce resource, not the seat.**
1,018 extra pecks are 1,018 keeper turns not spent building, healing or
answering. This is v603's 2,179-peck collar arithmetic returning at 1,347 **even
with the N=2 and 90-peck bounds binding**.

⇒ **THIRD ROAD CLOSED ON THE COLLAR.** v603 killed the *unbounded* peck; v610
kills the **bounded, aimed, per-episode-budgeted** peck. **The delivery seats
cannot be bought with builder turns at any price we can pay.** Code stays in the
tree, flagged, one line from live, every sub-constant ablatable — a future wave
that can clear a seat **without spending a keeper turn** inherits a validated
aim.

### The turret half (`SK_SEAT_GUNS`), priced on its own — the R1000 trade in miniature

`_target_pri` scores a BARRIER at 0 and `_turret` skips `pri <= 0`, so **no gun
of ours has ever fired at a seat-blocking barrier**; the docstring's "barriers
are only attacked by the verb whose PATH they block" is true of pecks and has no
counterpart in the turret path at all. Priced on the shipped chassis (the flag
is independent of `SK_SEAT_CLEAR`):

**ON: belt deaths 40 → 34, Ti 12,940 → 15,530, builder deaths 29 → 25 — and
by-r300 11 → 9, with the ammo-armed share halved 8.81% → 4.41%.** The guns
genuinely protect the belt and the ammo they burn is the drip's second sentinel,
which is the kill. **Trade declined on the stated currency: economy is
instrumental, it never scores.**

---

## 4. SHIP RULE — WHICH BRANCH FIRED

Stated bar: `by-r300 ≥ 10 AND M1(worse seat) ≥ 40 AND funding-wait games ≤ 12/30`.

| | bar | v610 ship | met |
|---|---|---|---|
| by-r300 | ≥ 10 | **11** | ✅ |
| M1, worse seat | ≥ 40 | **33.3** | ❌ |
| funding-wait games | ≤ 12/30 | **18/30** | ❌ |

**FULL SUCCESS NOT MET. THE FALLBACK BRANCH FIRED: "ship the subset of planks
that maximises by-r300."** That is PLANK 2 alone (11), against the base (10) and
against PLANK 1 (7).

**AND THE TWO MISSED BARS ARE NOW EXPLAINED RATHER THAN OPEN.** M1 is
structurally capped by the collar: the one-barrier class is 26–27 of 68 and
PLANK 2 cannot touch it, because a tile an enemy barrier occupies cannot be
built on — it must be cleared, and PLANK 1 is the measured proof that clearing
it with builder turns costs more than it returns. **The funding-wait revisit and
the M1 gap are the same problem wearing two hats, and both now have a named
mechanism and a closed road rather than an open question.**

---

## 5. VERIFICATION

* **Static 12/12 scans PASS, 72/72 dirty controls FIRE** (13 new v610 controls).
  ⭐ **One control came back BROKEN and caught a hole in the SCAN, not in the
  tree**: "move the seat walk above `_medic_seat`" left the original call site
  in place, so the ordering regex still matched. Fixed by asserting `_seat_walk`
  has **exactly one** call site — the control battery catching itself.
* **IDENTITY CONTROL: every v610 flag OFF is byte-identical to the v609 shipped
  tape in all 30 replays.** The refactor is provably inert with the flags off.
* **Aliveness: 12 games both seats, 0 tracebacks, 0 exception-removals**;
  injected-NameError control fires (8 tracebacks, 8 no-damage builder removals).
* **Fidelity per seat** (seats split into manifests — a both-seat dir under one
  `--side` mis-attributes half the games): drip lattice **100.0/100.0** (bar
  97.3) · M4 forward point-blank **0.0/0.0** · M4 sentinel point-blank
  **0.0/0.0** · M1 **34.2/33.3**.
* **Named cells, v609 → v610, all 12 checked:** icefloe seat A **kill r136
  HELD** (the v609 recovery survives) · helheim A r387 · midgard A/B r95/r113 ·
  fimbulwinter A/B kills r160/r150 · bifrost A r157 (still the named structural
  refusal) · longhouse A r297 · paths A r605 — **all unchanged**. Two changed:
  **stavkirke A r1000-tie → kill r294** and helheim B r169 → r144 (disclosed).
* **Loss anatomy unchanged: 16/16 sentinel**, median death r200.0, S2 stood in
  12/16. **No home-answer regression**: unanswered-streak median 13.0 (v609
  13.0), max 95, ≥40 in 6.
* **Per-plank ablations both ways on the exact shipped chassis**, plus a 3-point
  dose curve on PLANK 1 and a half-by-half split of PLANK 2.
* `summary.py --check` positive control OK (34 / 46).
* **Tape reproduced from the shipped tree after the last docstring edit:
  `tape_FINAL2` vs `tape_ship`, 0/30 differ.**
* **CPU wall-clock, 6 games: 10.53 s (v609) → 10.75 s (v610), 0 engine
  timeouts** in the 30-game tape. **Platform CPU test STILL OWED.**

⚠ **FIXTURE CAVEAT on every number here:** ONE authored opponent, local screen,
30 games. Local balanced batteries read DEFF ≈ 0.98 so naive intervals are
approximately honest, but a +1 on a 30-cell bar is not a resolvable difference
and is not claimed as one.

---

## 6. v611 QUEUE

1. **⭐ THE COLLAR NEEDS A VERB THAT IS NOT A BUILDER TURN.** Three roads are now
   closed on the delivery seats (v603 unbounded peck, v610 bounded/aimed peck,
   v610 turret fire on the stated currency), and the aim is validated: 180/220
   enemy barriers stand on our 8 seats, the class is 26/68 harvesters, and the
   mechanism moves M1 to the best figure this line has read. **The open
   candidate is the LAUNCHER: `can_launch` has no team check and no vision
   guard, pickup d² ≤ 2, throw 1 ≤ d² ≤ 26, 0 ammo — and their collar builder
   stands adjacent to our seats by construction.** Removing the *layer* costs no
   keeper turn at all. This is also the only remaining Loki-class road on this
   axis.
2. **M1 is capped by the collar, not by the planner** — closed as a belt
   question. Do not spend another wave on route planning until (1) resolves.
3. **The funding-wait revisit (18/30, 1,030 rounds) is the same problem.** Both
   spending arms are measured negative (v606 cutting door guns, v607 deferring
   them) and income is capped by the collar. **The remaining lever is the second
   gun's COST — the scale discipline flagged as v605's item 6 and never taken.**
4. **`SK_TERM_MOVE` is an outcome null on this fixture** — re-price it, or cut
   it, on the next fixture that has more than one opponent.
5. **helheim seat B dies 25 rounds earlier under PLANK 2** — small, already a
   loss, unexplained.
6. Standing: platform CPU test owed.

---

## 7. PROGRESSION ON THE FIXTURE (identical opponent, 30 games)

```
kills     0 → 0 → 6 → 8 → 9 → 11 → 11 → 12 → 13 → 14
by-r300   — → — → 5 → 6 → 6 → 10 → 10 →  9 → 10 → 11
med kill  — → — →198→256→275→208→160→160-185→170→188.5*
                                        (* a r294 kill ADDED, not a slowdown)
```

**FIRST-CONTACT GATE: NOT MET** (14/30 does not beat the screen). by-r300 is at
its highest reading of the line. **The product of this wave is the closed road:
the delivery seats are the measured bottleneck, they are worth clearing, and
they cannot be cleared with the verb we have.**
