# ATTRIBUTION — what the KEEPER BODY does in the five carrying F1 cells (p11 dispatch arm vs control)

**GAME CONTEXT.** This is in-game analysis for the Florent Code League, a
sandboxed bot-vs-bot programming competition played on a simulated grid under
organiser-approved rules. Every "death", "kill", "shooter", "displaced",
"knocked out" below is an in-engine event between competing game bots — a piece
removed by the engine per its documented rules. Nothing here concerns real
systems, networks or people.

Commissioned by the research arm for QUEUE row #129 (builder-routed from the
plank-1.1 park, `docs/coordination.md` 2026-08-22T20:40:28Z). Read-only on
`bots/`; zero platform matches were played. Written 2026-08-22T20:55:49Z, repo
at `62479c86a`.

**This document attributes a mechanism per cell and stops there.** It contains
no build/no-build recommendation and no fix design — the third fix is the
builder's.

---

## PROVENANCE

| input | path (verbatim) |
| --- | --- |
| dispatch arm (plank 1.1) tapes | `scratchpad/s57_heim0/t_p11_f1/<cell>.replay26` (mtime 2026-08-22 22:35 local) |
| leash-only arm tapes | `scratchpad/s57_heim0/t_leash_f1/<cell>.replay26` (mtime 22:25 local) |
| control tapes | `scratchpad/s57_v630/t_ctrl_f1/<cell>.replay26` (mtime 20:48 local) |
| plank-1.0 composite arm (p14), for the banked cross-check | `scratchpad/s57_heim0/t_p14_f1/<cell>.replay26` |
| screen classifiers (reused, not re-implemented) | `scratchpad/s57_heim0/e46p1_lib.py` (`P1`, `cells_at`, `cheb_to_footprint`, `core_fp_heals`, `zone_chews`, `snaps`) |
| banked readout this must agree with | `scratchpad/s57_heim0/e46p11_readout.py` §1b, and `docs/coordination.md` 2026-08-22T20:40:28Z ("PLANK 1.1 VERDICT") |
| event walker under the classifiers | `scratchpad/s54_klad_lib.py` (`Game`) over `tools/replay_census.py` primitives |
| wire field numbers | `tools/replay_schema.md` (`BotOutput{id, stdout, execTimeUs, tled}` at :85) |
| damage-linked death convention | `tools/skalman_fidelity.py` — M7d `dmg_ids` (ids that ever took a negative `updateHp`) and its `strip_hp` mutation |
| arm source trees (read for semantics only) | `scratchpad/s57_heim0/arm_p11/`, `scratchpad/s57_heim0/arm_leash/`, `bots/_heim0demo/` |
| this analysis' script | session scratchpad `keeper_trace.py` + `run1..run19.py` (not committed) |

Interpreter: `.venv/bin/python` 3.13.7.

**Arm definition, read off the trees** (`diff -u arm_leash arm_p11`): `main.py`
and `sk_common.py` are identical; the only differences are
`sk_maps.py` `SK_FORTRESS False→True`, `SK_CITADEL False→True`,
`SK_IDLE_ACT_ALL False→True`, and a 16-line addition in `sk_roles.py`
`_citadel_answer` — the plank-1.1 medic yield
(`if self.role == SK_HOME_KEEPER and self.corefire_fresh(ct, rnd): return False`).
`SK_KEEPER_LEASH` is **True in both arms**. So every behavioural difference
between the leash arm and the p11 arm is the citadel dispatch family.

---

## METHOD

**The keeper body.** `e46p1_lib` has no keeper notion — it counts
core-footprint heals by team. The keeper is `SK_HOME_KEEPER = role 0`
(`arm_p11/sk_maps.py:2394`), claimed in `_claim_role`
(`arm_p11/sk_roles.py:355`) by the lowest role id whose liveness beat is unset
or stale (`SK_BEAT_STALE = 3`), which is also the re-claim path when a body is
knocked out. I model that from the wire: our builder bots in spawn order, each
taking the lowest role whose holder is unassigned or was removed ≥ 3 rounds
before its first turn. Identification succeeded in **all ten traces**
(5 cells × 2 arms) and is validated below.

**The heal channel.** `P1.core_fp_heals` verbatim (`HEAL` = `builderHeal`
update kind 15; healer team from the registry; target tile inside our own 2×2
core footprint). A *medic seat* is a tile orthogonally adjacent to a footprint
tile — the only tiles from which the engine permits that heal.

**Death cause.** M7d convention: a removal is DAMAGE-linked if the id ever took
a negative `updateHp`; I additionally report the tighter window form (negative
`updateHp` in the removal round or the one before). A removal with no damage
reads EXCEPTION-OR-SELF-DESTRUCT per the crash-census convention.

**Displacement (an enemy launcher relocating our body).** The engine records a
throw as a `moveBuilderBot` whose step exceeds one tile. Detector: `MOVE`
records with manhattan(from, to) > 1.

---

## VALIDATION — both directions, before any number below is quoted

**V1 — the leash≡control claim, verified harder than asked.** The brief asked
me to confirm the builder's `308 = 308` heal identity before leaning on leash
as the comparator. On these five cells the two tapes are **byte-identical**
(sha256): `icefloe_seatB 8dec0b9a…`, `holmgang_seatA 86dbde57…`,
`glacierkeep_seatB b5ccabcf…`, `skald_seatA 354d3d2f…`,
`stavkirke_seatA 00b721e3…` — control and leash agree hash-for-hash on all
five. (Across the whole F1 fixture only 19 of 30 cells are byte-identical, so
this is a property of these five cells, not of the arm.) **Consequently CTRL
and LEASH are the same trace on every cell in this document and I quote CTRL.**

**V2 — reproduction of the banked table (the stop-condition).** Per-cell
core-footprint heals, recomputed from the tapes:

| cell | CTRL | LEASH | **P11** | P14 (banked) |
| --- | ---: | ---: | ---: | ---: |
| icefloe_seatB | 90 | 90 | **0** | 0 |
| holmgang_seatA | 69 | 69 | **0** | 0 |
| glacierkeep_seatB | 51 | 51 | **0** | 0 |
| skald_seatA | 49 | 49 | **0** | 3 |
| stavkirke_seatA | 49 | 49 | **9** | 9 |
| **sum of the five** | **308** | **308** | **9** | **12** |

P11 reads `0/0/0/0/9` and p14 reads `0/0/0/3/9` — **exactly the banked
figures**. Arm totals over all 30 F1 cells: CTRL 398, LEASH 425, P11 288,
P14 273.

**V3 — keeper identifier, positive control.** In the control arm every single
core-footprint heal is performed by the modelled role-0 body: **308 of 308,
share 1.000**, and per cell 90/90, 69/69, 51/51, 49/49, 49/49 (ids 4, 3, 4, 3,
3).

**V4 — keeper identifier, mutation.** Attributing the same channel to role 1,
or to roles 2+3, returns **0 heals in every one of the five cells**. The
identifier discriminates; it does not merely pass.

**V5 — position track, sanity.** For the 308 control heals the tracked keeper
position sits at manhattan distance 1 from the healed tile in **306 of 308**
cases (the 2 exceptions are rounds carrying both a MOVE and a HEAL record,
where my walker applies the move first). Seat-occupancy counts below are
therefore reliable to ≲1%.

**V6 — death-cause classifier, mutation.** The only keeper removal in the ten
traces (holmgang_seatA P11, id 3, r142) types **DAMAGE** normally and flips to
**EXCEPTION-OR-SELF-DESTRUCT** when `updateHp` events are dropped — the
`skalman_fidelity --strip-hp` mutation, reproduced here. The classifier has
been seen to produce the other verdict. Both conventions agree on all ten
traces (ever-damaged ≡ window form).

**V7 — displacement detector, both directions.** Across all builder bots of
both teams on the ten tapes there are **151** long MOVE records. **151 of 151
(100%)** are consistent with a live launcher's engine geometry (pickup
d² ≤ 2 from the launcher, throw 1 ≤ d² ≤ 26 from it), and **0** occur with no
launcher alive on the board — the falsifier is empty.

**V8 — an instrument that does NOT exist here, stated so nobody re-derives it.**
`BotOutput.execTimeUs` and `.tled` are **0 in every row of every one of the ten
tapes** (720 rows for the icefloe keeper alone). The local runner does not
populate them, so **CPU-budget attribution is not available from these tapes** —
this is the exec-time sibling of the s54 stdout finding. What the rows *do*
establish is that `run()` was invoked for the keeper in every round it lived
(720 rows / 721 rounds) and never raised — an escaping exception would have had
the engine remove the unit.

---

## PER-CELL ATTRIBUTION

The carrying statistic, identical in shape across all five cells:

| cell | arm | keeper-alive rounds | rounds ON a medic seat | share | on seat **while our core was damaged** | core-fp heals |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| icefloe_seatB | CTRL | 721 | 186 | 25.8% | 165 | 90 |
| | **P11** | 722 | **1** | **0.1%** | **0** | **0** |
| holmgang_seatA | CTRL | 271 | 108 | 39.9% | 100 | 69 |
| | **P11** | 153 | **4** | **2.6%** | **0** | **0** |
| glacierkeep_seatB | CTRL | 192 | 64 | 33.3% | 63 | 51 |
| | **P11** | 222 | **1** | **0.5%** | **0** | **0** |
| skald_seatA | CTRL | 137 | 54 | 39.4% | 50 | 49 |
| | **P11** | 168 | **3** | **1.8%** | **0** | **0** |
| stavkirke_seatA | CTRL | 286 | 181 | 63.3% | 50 | 49 |
| | **P11** | 204 | 69 | 33.8% | **10** | **9** |

Outcomes, for orientation:

| cell | CTRL | P11 |
| --- | --- | --- |
| icefloe_seatB | loss, core removed r719 of 720 | loss, core removed r720 of 721 |
| holmgang_seatA | **WIN** by core takedown, our core survives | loss, our core removed r208 of 209 |
| glacierkeep_seatB | loss, core removed r190 of 191 | loss, core removed r220 of 221 |
| skald_seatA | **WIN** by core takedown, our core survives | loss, our core removed r166 of 167 |
| stavkirke_seatA | **WIN** by core takedown, our core survives | loss, our core removed r202 of 203 |

---

### 1. icefloe_seatB — **(d) PATHS AWAY**, and it is a stand-on-your-own-target deadlock

Keeper: id 4, role 0, born r0, **alive at the final round in both arms**; no
role churn (role 0 was never re-issued, unlike roles 1 and 3 which cycled
through 12 replacement bodies in the p11 tape).

| | CTRL | P11 |
| --- | --- | --- |
| keeper died | no | no |
| enemy-launcher relocations of the keeper | 31 | **3** |
| longest stationary run | 175 r at (16,3), **a medic seat**, 83 heals | **475 r at (16,8)** — cheb 5, an **ORE tile**, 0 actions |
| core-fp heals | 90 | 0 |
| moves / builder attacks | 289 / 46 | 101 / 42 |
| rounds with no wire action at all | 296 / 721 | **551 / 722** |

Trace. The p11 keeper works the core ring until r160 (stations at (16,4) cheb 1
and (16,4) again r144-160, chewing). At r161-164 it walks four tiles south to
**(16,8)** — an ORE tile at cheb 5 / d²=26 from the footprint — and **stays
there from r164 to r638, 475 consecutive rounds, emitting no move, no build, no
attack and no heal**. It is not boxed: all four neighbours (16,7), (16,9),
(17,8), (15,8) are EMPTY terrain with no building and no body at r200, r300,
r450 and r600. It is not displaced: only 3 launcher relocations touch it all
game, versus 31 in the control. Its `BotOutput` row is present every round, so
`run()` ran and returned without acting.

The tile is the tell. A builder cannot build on the tile it stands on — the
engine requires an orthogonally adjacent target — so a keeper whose economy
walk targets an ore tile and then *steps onto it* has a walk target equal to its
own position (`step_to` returns False, nothing to build, and `SK_IDLE_ACT_ALL`'s
new rung is gated on `free_neighbours == 0`, which is false here). The control
keeper never entered that state; it parked on the medic seat (16,3) for 175
rounds and healed 83 times from there.

Note for the record: d²=26 is **inside** `SK_LEASH_DSQ = 50`, so the keeper
leash's far-target fence does not reach this tile at all — consistent with the
leash arm being byte-identical to control here.

**Mechanism: (d) PATHS AWAY.** The body keeps role 0 and survives the whole
game, but from r164 it stands 5 tiles off the footprint where the heal verb is
not legal, and it never returns. Not (a): alive. Not (b): 3 relocations vs 31 in
control. Not (c): role 0 was never reassigned, and the body is not doing citadel
work either — it is doing nothing.

---

### 2. holmgang_seatA — **(d) PATHS AWAY first, then (a) DIES EARLY**, plus a 58-round vacant seat

Keeper: id 3, role 0, born r0. **Removed r142** (CTRL: alive at r270).

| | CTRL | P11 |
| --- | --- | --- |
| keeper lifetime | r0-270 (survives) | r0-**142**, replacement id 168 born r200 |
| rounds on a medic seat | 108 (two long stations at (0,1), 17 + 33 heals) | **4**, none while the core was damaged |
| core-fp heals | 69 | **0** |
| enemy-launcher relocations | 1 | **0** |
| keeper alive during our core's damage rounds | 40 / 40 | **5 / 28** |

Trace. Before it is ever touched, the p11 keeper has **already lost the
channel**: over 143 rounds of life it stands on a medic seat 4 times and on
none of them is our core damaged, so its heal count is 0 for reasons that have
nothing to do with its removal. It has one station ≥15 rounds (r18-35 at (4,2),
chewing an enemy barrier) and otherwise roams — 103 moves, 16 builder attacks,
12 builds, only 12 idle rounds. The control keeper, by contrast, parks on the
seat (0,1) at r124-141 and again r174-207 and heals 50 times from those two
stations alone.

The removal: negative `updateHp` of **−18** at r132, r137 and r142 (3 × 18 = 54
against 40 max HP). At r142 the wire carries `fireTurret from (8,7) to (8,4)`
and the keeper is standing on (8,4); the building at (8,7) is an **enemy
sentinel, entity id 35, built r14 and alive** — sentinel damage is 18. So the
cause is damage-linked and the shooter is identified on the wire.

Then the seat goes **vacant for 58 rounds**: no builder is spawned between r142
and r200, so no body can re-claim role 0. Replacement id 168 arrives r200,
lives 10 rounds, never reaches a medic seat, lands 4 builder attacks, and our
core is removed at r208.

**Mechanism: (d) PATHS AWAY, dominant — the channel is already zero across the
keeper's whole 143-round life — compounded by (a) DIES EARLY (damage-linked,
enemy sentinel id 35 at (8,7), r132/137/142) and a 58-round unstaffed keeper
seat.** Not (b): zero relocations. Not (c) in the role sense: role 0 was
re-issued exactly once, correctly, after the removal.

---

### 3. glacierkeep_seatB — **(c) ROLE CHURN in the dispatch sense: the citadel duty owns the body**

Keeper: id 4, role 0, born r0, **alive at the final round in both arms**. No
role churn: our four builders are the original four in both tapes.

| | CTRL | P11 |
| --- | --- | --- |
| rounds on a medic seat | 64 (station r91-153 at (14,25), 50 heals) | **1** |
| core-fp heals | 51 | **0** |
| keeper zone chews (our builder attack on an enemy building inside cheb 3) | 30, all at target cheb 1 | **40, of which 20 at target cheb 2** |
| stations ≥15 r | (14,24) cheb 2 → **(14,25) cheb 1 = medic seat** → (17,27) cheb 2 | **(12,23) cheb 3** adj. enemy sentinel, 20 attacks; **(17,25) cheb 2**, 20 attacks |
| median cheb while our core was losing HP | **1.0** (25 of 40 damage rounds at cheb ≤1) | **3.0** (0 of 28 damage rounds at cheb ≤1) |

Trace. This keeper is not idle and is not knocked out — it is **busy on the
citadel zone the whole game**. Its two long stations sit at cheb 3 and cheb 2,
each spent chewing (20 attacks apiece), and its zone-chew target distance moves
outward: in the control every one of its 30 zone chews is on a structure at
Chebyshev 1 from the footprint (i.e. on the ring, reachable from a medic seat's
neighbourhood); in p11 **half of the 40 are at Chebyshev 2**, which is the
citadel zone's reach and not the medic ring's. The core loses 28 HP-ticks and
the keeper is at median cheb 3 for all of them, never once at cheb ≤ 1.

**Mechanism: (c) the dispatch reassigns the duty.** The citadel zone
(Chebyshev 3 of the footprint) is strictly larger than the medic ring
(Chebyshev 1), so a body dispatched to the zone stands where the heal verb is
not legal. The body keeps the role-0 seat and performs zone work with it. A
secondary (d) component: the two stations are off-ring parking, not transit.

---

### 4. skald_seatA — **(d) PATHS AWAY**, a second ore-tile deadlock, with no citadel work to show for it

Keeper: id 3, role 0, born r0, **alive at the final round in both arms**.

| | CTRL | P11 |
| --- | --- | --- |
| rounds on a medic seat | 54 (station r64-113 at (7,3), **49 heals**) | **3** |
| core-fp heals | 49 | **0** |
| builder attacks (any) | 16 | **0** |
| zone chews | 1 | **0** |
| moves / idle rounds | 57 / 2 | 83 / **68** |
| stations ≥15 r | (8,8) cheb 6 chewing; **(7,3) cheb 1 = medic seat, 50 r** | (6,0) cheb 1 non-seat, 21 r, 0 actions; **(8,5) cheb 3, an ORE tile, 33 r, 0 actions** |
| median cheb while our core was losing HP | **1.0** (17 of 28 damage rounds at cheb ≤1) | **3.0** (0 of 28 at cheb ≤1) |

Trace. The p11 keeper never lands a single builder attack in 168 rounds, so it
is not doing citadel chew work; it walks (83 moves) and stands (68 idle
rounds), including 33 consecutive rounds parked on the **ore tile (8,5)** at
cheb 3 doing nothing — the same stand-on-your-own-target shape as icefloe, at a
shorter horizon. Its control twin reaches the medic seat (7,3) at r64 and
heals on 49 of the next 50 rounds. One launcher relocation touches it in each
arm, so displacement is not in play.

**Mechanism: (d) PATHS AWAY.** Role kept, body alive, never displaced, no
dispatch work performed — it simply spends the game off the ring, twice
terminating on a tile it cannot act from.

---

### 5. stavkirke_seatA — **(c) then (d): the body is pulled OFF a working medic seat mid-game and never returns**

Keeper: id 3, role 0, born r0, **alive at the final round in both arms**. This
is the only cell where the channel is non-zero (9 heals), and the wire shows
exactly when it stops.

| | CTRL | P11 |
| --- | --- | --- |
| rounds on a medic seat | 181 (station **r110-285 at (8,2)**, 47 heals) | 69 (station **r74-139 at (8,2)**, 9 heals — then gone) |
| core-fp heals | 49 | **9** |
| zone chews | 23 | **40** |
| stations after the seat | — (it never leaves) | **(13,5) cheb 3** r151-169; **(10,5) cheb 2** r175-203, 21 attacks |
| our core | survives, we win by core takedown at r285 | removed r202 |

Trace, round by round, from the p11 tape (core anchor (9,2)):

```
r134-139  keeper at (8,2)  ON SEAT   heals (9,2) every round   core HP 462→446
r140      keeper MOVES to (8,1)      OFF SEAT                  core HP 428
r141-151  keeper walks (8,0)→(9,0)→(10,0)→(11,0)→(11,1)→(12,1)→(12,2)
          →(12,3)→(13,3)→(13,4)→(13,5)   eleven consecutive MOVE rounds
          our core bleeds 428 → 338 across the walk, unhealed
r152-155  keeper attacks (12,5) — an enemy SENTINEL at Chebyshev 2 — 4 times
          core HP 338 → 302
r156      the sentinel is gone; the keeper stands on (13,5) idle
…         it never returns to a medic seat; our core is removed at r202
```

The control twin, over exactly the same rounds, sits on (8,2) and heals every
round: core HP **climbs** 406 → 470 across r134-150 while the p11 core falls
462 → 338.

**Mechanism: (c) the dispatch pulls the body off a working medic seat to a
zone target at Chebyshev 2-3, followed by (d) — it stations off-ring for the
remaining 60 rounds and the channel never resumes.** Not (a): alive at the
end. Not (b): zero launcher relocations in either arm.

---

## CROSS-CELL SUMMARY

**One thing is true in all five cells and it is positional, not lethal:
the keeper stops standing where the engine allows the heal.** On-seat share
collapses 25.8/39.9/33.3/39.4/63.3 % → 0.1/2.6/0.5/1.8/33.8 %, and
**on-seat-while-our-core-is-damaged goes 165/100/63/50/50 → 0/0/0/0/10.** The
heal totals are a deterministic consequence of that column, not an independent
fact.

| cell | keeper alive? | displaced? | role re-issued? | **attributed mechanism** |
| --- | --- | --- | --- | --- |
| icefloe_seatB | yes, all 722 r | 3 relocations (CTRL: 31) | no | **(d)** — 475-round freeze on ore tile (16,8), cheb 5, zero actions |
| holmgang_seatA | **no, removed r142** | 0 | once, after the removal, 58 r late | **(d) dominant** (0 heals across its whole life, 4 seat-rounds) **+ (a)** damage-linked, enemy sentinel id 35 at (8,7) |
| glacierkeep_seatB | yes, all 222 r | 9 relocations (CTRL: 4) | no | **(c)** — citadel duty owns the body; 40 zone chews, half at target cheb 2; median cheb 3 during every core-damage round |
| skald_seatA | yes, all 168 r | 1 (CTRL: 1) | no | **(d)** — 0 attacks, 68 idle rounds, 33-round freeze on ore tile (8,5), cheb 3 |
| stavkirke_seatA | yes, all 204 r | 0 | no | **(c) then (d)** — pulled off the seat at r140, 11-round walk to a cheb-2 sentinel, never returns |

**(b) DISPLACED is excluded as the mechanism in all five.** The keeper is
relocated by an enemy launcher 3, 0, 9, 1, 0 times in the p11 arm against
31, 1, 4, 2, 0 in the control — the arm with 308 heals is the arm with **more**
throws. The detector that says so is validated in both directions (V7).

**(a) DIES EARLY is a real but secondary mechanism in exactly one cell**
(holmgang), and even there the channel was already zero for the 142 rounds
before the removal.

**The two live mechanisms are (c) and (d), and they share a single geometric
cause.** The citadel zone is Chebyshev 3 of the core footprint; the medic ring
is Chebyshev 1. A body dispatched into the zone is, in general, standing on a
tile from which the heal verb is illegal — that is glacierkeep and stavkirke,
where the body is busy (40 chews each) and off-ring. Where the dispatch instead
leaves the body to the economy walk, the same tape shows it terminating on an
ore tile it cannot build from and freezing for hundreds of rounds — that is
icefloe (475 r) and skald (33 r), where the body is neither healing nor doing
citadel work. Parking is normal for this bot in **both** arms (44-79 % of
control keeper-rounds are stationary runs ≥15 r); what the dispatch arm changes
is **where** the park lands: in the control every one of the five keepers has a
long station with `seat = True` and heals from it (83/50/50/49/47 heals); in
p11 only stavkirke does, and it leaves at r140.

---

## SURPRISES / DISAGREEMENTS WITH THE BANKED FRAMING

1. **The banked note asks "died early? displaced? role churn?" — the answer in
   four of the five cells is "none of those".** The keeper is alive at the
   final round, holds role 0 uninterrupted, and is relocated less than in the
   control. The zero is a **standing-position** fact.
2. **Two of the five cells show the keeper doing no citadel work either.** In
   icefloe and skald the body is not chewing, not holding, and not healing — it
   is inert on an ore tile for 475 and 33 consecutive rounds with all
   neighbours free. Any account of these cells purely as "the dispatch spends
   the keeper's turn" does not fit: the dispatch would have produced attacks or
   moves, and the wire shows neither.
3. **The banked line says "three of five convert surviving cores (two CTRL
   WINS) into deaths" — the win count is three, not two.** holmgang_seatA,
   skald_seatA and stavkirke_seatA are all `WIN / core_destroyed` with our core
   surviving in the control, and all three are losses with our core removed in
   p11. (The "three of five convert surviving cores" half reproduces exactly.)
4. **`BotOutput.execTimeUs` / `tled` are identically 0 on every local tape.**
   Any future leg that plans to read a CPU-budget fact out of a local replay is
   planning on an instrument that does not exist here — the exec-time sibling
   of the s54 stdout correction. (What the rows do prove: `run()` was invoked
   every round the keeper lived and never raised.)

---

## LIMITS

* **The arms are different games from their first divergent round.** Only the
  code difference is controlled; the opponent's board is not. In stavkirke, for
  instance, the enemy sentinel at (12,5) and launcher at (8,5) exist in the p11
  tape and not in the control tape at r134. So "the citadel dispatch pulled the
  body off the seat" is an attribution of the **divergence** to the dispatch
  family (sound: leash ≡ control byte-for-byte on these five cells, so nothing
  else can have caused it), **not** proof that the proximate branch that emitted
  the r140 move was `_citadel_answer` rather than a pre-existing v628 branch
  reacting to a board that only the dispatch arm produced. Separating those two
  requires an instrumented local run, which this commission did not perform.
* **Five cells, one fixture, one seat each.** Nothing here is a population
  estimate; no design effect is applied and none should be — these are five
  named cells read individually, exactly as commissioned. The cross-cell
  summary is a description of these five traces.
* **The keeper identifier is a model of `_claim_role`, not a wire field.** It
  is validated at 308/308 on the control arm and driven to 0/308 under
  mutation, but there is no role tag on the wire; a tape where the claim order
  is disturbed in a way the model does not anticipate would be mis-attributed.
  No such disturbance appears in these ten traces (role 0 is re-issued exactly
  once, in holmgang, after a removal).
* **`corefire`-freshness in this document is a model** (our core took a
  negative `updateHp` within `SK_COREFIRE_TTL = 24`), not the store word the
  bots actually read; the store is not on the wire. It is used only for
  context, never for an attribution.
* **Two of the 308 control heal events could not be position-checked** (V5);
  seat-occupancy counts carry that ≲1% uncertainty.

---

## MECHANISM STATEMENTS

* **icefloe_seatB** — the keeper survives the whole game holding role 0 and
  **paths away**: from r164 it stands on the ore tile (16,8), Chebyshev 5 from
  the footprint, for 475 consecutive rounds with no move, build, attack or heal
  and all four neighbours free.
* **holmgang_seatA** — the keeper **paths away** for its whole 143-round life
  (4 seat-rounds, none while our core was damaged, so the channel is already
  zero), and is then **knocked out at r142 by damage** — three −18 ticks from
  the enemy sentinel id 35 at (8,7), the last one on the wire as
  `fireTurret (8,7)→(8,4)` onto its tile — leaving the keeper seat unstaffed
  for 58 rounds.
* **glacierkeep_seatB** — the keeper survives holding role 0 and its turns are
  **reassigned to the citadel duty**: 40 zone chews, half against structures at
  Chebyshev 2, from stations at Chebyshev 2-3; median Chebyshev 3 during every
  one of the 28 rounds our core lost HP, and one single round on a medic seat.
* **skald_seatA** — the keeper survives holding role 0, performs **no citadel
  work at all** (0 builder attacks in 168 rounds) and **paths away**: 68 idle
  rounds and a 33-round freeze on the ore tile (8,5) at Chebyshev 3.
* **stavkirke_seatA** — the keeper heals from the medic seat (8,2) until r139,
  is then **pulled off it** into an eleven-round walk (r140-151) to a
  Chebyshev-2 enemy sentinel it attacks four times while our core bleeds
  428 → 302 unhealed, and **never returns to the ring**; our core is removed at
  r202.
