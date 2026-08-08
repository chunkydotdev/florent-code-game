# v85hs mechanism read — did the designed mechanisms cause the flips?

**Deliverable of the research arm, 2026-08-08.** Measurement + attribution only.
The KEEP/ship verdict is the builder's.

| | |
|---|---|
| Candidate | `bots/_v85hs/main.py` md5 `33d1d94ddd94e30768fd16586c0b2414` (**33d1d94d**), 4,730 lines |
| Parent / holder | `bots/_v84g/main.py` md5 `cbb0b8b449110f89be9765028fbf8c54` (**cbb0b8b4**) — shipped as v73 "Eir 7" |
| b-rev (section 2) | `bots/_v85hsb/main.py` md5 `33a42f944fef7bc39b415fbed0fce5d6` (**33a42f94**) |
| Dirs code-read | `bots/_v85hs/`, `bots/_v84g/`, `bots/_v85hsb/` (full unified diffs, both directions) |
| Battery-side NOISE_OFF copies (read-only, builder scratchpad) | `_v84g_off` md5 `e15777ef`, `_v85hs_off` md5 `7615d72b`, `_v85hsb_off` md5 `95133000` |
| Corpus | 8 deterministic-paired pairs, 16 replays, `.replay26` wire format only (sidecars used for cross-checking, never as source) |
| Section 1 pairs | `archipelago_1_b`, `meander_1_a`, `lighthouse_4_a`, `jackpot_1_a`, `jackpot_1_b` (`g84_*` vs `h85_*`) |
| Section 2 pairs | `archipelago_1_a`, `saga_1_a`, `saga_1_b` (`hs_*` vs `hsb_*`) |
| Battery context (builder tape) | s1 slot bar h85 51.2%/480; s3 det-paired g84 120/240 = 50.0% vs h85 125/240 = 52.1%, 41 flips, 106/240 identical; hsb leg hs 52.1% vs hsb 58.8%, 16 flips, 184/240 identical |
| Live platform version at write time | v74 "mineguard" (x3r0) |
| Tools | `tools/replay_schema.md` (ground truth), `tools/rdiff.py` (first divergence), plus a purpose-built per-round state machine + HP-delta ledger written for this read (research scratchpad) |

---

# GATE SUMMARY — DISQUALIFIERS AND CLEARANCES (read first)

Written against the routing question: *does the decode supply the MECHANISM leg
of the hsb ship case (holder-parity + field-positive + mechanism)?*

## (a) DISQUALIFIER — hsb INHERITS the archipelago_1_b regression, cause and all

**Statement: YES, hsb carries the regression's cause in full. The cause is
`HS_SEAT_PROTECT`'s turret gate (`bots/_v85hs/main.py:3233`), which is base
`_v85hs` content that `_v85hsb` contains unchanged — and the b-rev's own gate
makes the underlying disarmament strictly *wider*, not narrower.**

Three independent confirmations that hsb does not escape it:

1. **Code.** `bots/_v85hsb/main.py` = `bots/_v85hs/main.py` + one hunk at
   `:1830-1843` (full diff verified; that hunk is the only difference).
   `HS_SEAT_PROTECT_ON = True` and the turret gate at `:3233` are identical in
   both. The r25 sentinel at (19,18) that the parent builds and the candidate
   refuses (§1.2) is refused by hsb for the same reason.
2. **The b-rev widens the exposure.** `_v85hsb`'s launcher gate uses the **full
   8-seat set with no delivery-terminus exemption** (its own comment says so).
   It removes one more class of own impassable building from the ring. Whatever
   garrison value the ring's own buildings have (§1.2 measures it), hsb gives up
   more of it than hs does.
3. **Measured, not inferred.** In `h85_archipelago_1_b` our only launcher is
   built r48 at **(18,13), off-seat** — so the b-rev gate never fires on that
   map/seat and hsb replays hs exactly. The builder's own `hsb_conf.out` det
   table agrees: **no archipelago seat-b row appears in either the flip list or
   the non-identical-end-state list**, i.e. hs and hsb produce identical end
   states on all 8 archipelago seat-b games. **hsb dies at r276/277 there too.**

Severity, stated honestly so the routing call is informed rather than blocked:

* The regression is **systematic, not stochastic** — `gate85.out` shows
  archipelago seat b flipping on **8 of 8 seeds**, core death r276-277 every
  time. It is a map/seat property, not a butterfly.
* The mechanism is **structural, not map-specific**: own-impassable seat-tile-rounds
  collapse 965 → 0 in every candidate-side game, and on archipelago-b that
  bought the opponent 21 → **194** builder-bot-rounds standing on our heal ring
  and **0 → 189** builder attacks on our core, ending with an enemy gunner
  planted on heal seat (20,18) at r175. Any opponent that melees the core ring
  can collect the same rent.
* **The field-relevance is not hypothetical.** The v73 production read already
  recorded that in its corpus A the seat blocker was *the opponent* — Leviathan
  plants a gunner on a core-orthogonal tile by r9-12 and rebuilds it. This plank
  hands that class of opponent a wider ring.
* **Counterweight the builder's bar already supplies:** the opponent in this
  corpus is the parent itself, and hsb's field battery is parity-vs-v74 with all
  four guards positive. So the regression is a *known, named, bounded* cost, not
  an unexplained one — but it is the candidate's own toggle, it is inherited,
  and it should be on the ship note rather than discovered later.

**Routing read: this is a disqualifier for "clean mechanism" framing, not
necessarily for shipping.** The honest sentence is *"the b-rev's own delta is
clean and positive; the base it sits on has a measured, named, systematic
regression on one map/seat class that the b-rev inherits and slightly widens."*

## (b) CLEARANCE — the archipelago_1_a stalemate → r202 kill IS mechanism-named

**Statement: I can name it, end to end, with every link measured. It is not a
butterfly cascade — but the confidence is split, and I am stating the split
rather than the headline.**

Chain (full detail §2.2): the gate moves our launcher off heal seat **(5,7)** to
(5,8), which does two measurable things —

* **Frees a delivery terminus.** In hs, (5,7) carries **0** delivery stacks for
  988 rounds because the launcher stands on it; in hsb it carries **29**, and
  hsb builds a conveyor on that exact tile at r97. Cumulative delivery by r200:
  **950 → 1,230 (+29%)**.
* **Shifts the throw geometry.** Both games throw saboteur `#9` exactly once;
  hs lands it at (8,11), hsb at **(9,11)** — one tile closer to the enemy core.

Downstream, both saboteurs run an identical script and hsb is **2 rounds** ahead
on the first forward gun (r76 vs r78) and **6 rounds** ahead on the second
(r106 vs r112); both builds are bank-gated (bank hits 4 in the build round in
both games), so the earlier funding is the delivery delta cashing in.
Enemy-core damage **940 → 1,218**; enemy core bottoms at 212 and heals back to
364 in hs, reaches **0 at r201** in hsb.

**Confidence split: mechanism-DIRECT on the placement and the delivery delta;
mechanism-PLAUSIBLE on the kill** (the amplification from one tile of throw
offset and ~30 Ti to a 278-damage swing is large). What rules out "butterfly" is
that **the same launcher→terminus mechanism reproduces independently on a second
map**: on `saga_1_a` the freed tile (3,4) carries **41 of hsb's 66 delivery
stacks (62%)** against 0 in hs, delivery rate **287 → 356/100r**, and the
forward sentinel at (14,14) — exactly sentinel range from the enemy core —
lands at **r38 instead of r165**. Two maps, same mechanism, same direction.

**The builder's stated hypothesis is PARTLY CONFIRMED and PARTLY WRONG.**
Confirmed: the ungated launcher did sit on a delivery terminus and the terminus
was wanted. Wrong: it did not block the economy — hs finished with **12,330**
titanium delivered against hsb's 1,250, and hsb won by killing the core, not by
out-banking. The economic effect is a *rate* effect early, not a blockade.

## (c) VARIANCE FLAG — the gate's economic effect is large, consistent in sign, and swings game length hard

| pair | delivery rate hs → hsb | game length hs → hsb |
|---|---|---|
| `archipelago_1_a` | cumulative by r200 **950 → 1,230 (+29%)** | 1000 (tiebreak loss) → **202 (kill)** |
| `saga_1_a` | **287 → 356 /100r (+24%)** | 233 (our core dead) → **185 (kill)** |
| `saga_1_b` | **1,055 → 1,538 /100r (+46%)** | 233 (kill) → **624 (kill)** |

* **Direction is consistent: positive in 3 of 3.** The "hsb slower with 9,600 vs
  2,460" framing on `saga_1_b` is a rate-vs-total artifact — hsb's delivery rate
  is 46% *higher*; the game simply ran 2.7× longer.
* **The genuine flag is game length, not economy.** The same 3-line gate turned
  a 1000-round game into a 202-round kill on one map and a 233-round kill into a
  624-round kill on another. Longer games mean more exposure to r1000 tiebreaks
  and to whatever the field does late; shorter games mean the opposite. **This
  is a variance-increasing change on match duration, in both directions**, and
  the ship note should say so.
* Magnitude is map-dependent (24-46%) and depends on whether the freed seat is a
  tile the conveyor network actually wants: on `saga_1_b` the freed tile (20,18)
  carried **no** deliveries in either variant, yet the rate still rose 46% — so
  part of the economic gain is *not* the terminus and is currently unexplained.
  That unexplained residue is the honest limit of the economic claim.

## What the decode supplies to the mechanism leg

| ask | supplied? |
|---|---|
| The b-rev's own delta has a named mechanism | **YES** — launcher off the seat ring, verified in 3 of 3 pairs, own-impassable seat-rounds 988/216/213 → 0, first divergence in each pair is literally the launcher's build target |
| That mechanism explains the positive flips | **YES for the placement and economy links; PLAUSIBLE for the kills** (§2.2-§2.4) |
| The base's toggles have a named mechanism | **YES, mixed sign**: ceiling lift mechanism-direct positive (`lighthouse`), seat protect positive on `meander` and **negative on `archipelago_1_b`**, heal detail **direct negative** on `jackpot_1_a` |
| Clean bill of health for the candidate as a whole | **NO** — see (a), plus §1.4, §1.9 |

---

## 0. INSTRUMENT NOTE THAT CHANGES HOW SECTION 1 READS

**The shared opponent in every pair of this corpus is the parent itself
(`_v84g_off`).** Established three independent ways:

1. The builder's own `hsb_conf.out` names it: *"det-paired hsb-vs-hs (vs
   `_v84g_off`)"*; `gate85.out` stage 3 is *"det-paired vs holder"*, and the
   holder on 2026-08-08 is v73 = `_v84g`.
2. `g84_jackpot_1_a.replay26` and `g84_jackpot_1_b.replay26` are **byte
   identical** (md5 `172fed60…`, `cmp` clean). On a 180°-symmetric map that is
   only possible if the two seats are the *same game* — i.e. both players are
   the same binary. Not a corpus defect: it is the seat-invariance of a mirror
   match. Same for `hs_saga_1_a` ≡ `hs_saga_1_b` (md5 `86e12726…`).
3. `hs_archipelago_1_a.replay26` ≡ `g84_archipelago_1_b.replay26` byte for
   byte — the hs-vs-parent seat-a game *is* the parent-vs-parent game, which
   requires the candidate to be behaviourally identical to the parent as team A
   on archipelago (no toggle fires there) **and** the opponent to be the parent.

Two consequences the builder should carry:

* **The section-1 control leg is a mirror self-play match, so its win rate is
  pinned at exactly 50% by construction** — for every `(map, seed)` the parent
  wins one seat and loses the other, because it is the same game recorded
  twice. `gate85.out` reports g84 at *exactly* 120/240 = 50.0%; that number is
  an artifact, not a measurement. The candidate's 125/240 = 52.1% is still a
  legitimate head-to-head figure (it is the same quantity as the 51.2%/480 slot
  bar), but **"the parent won this pair" carries no information beyond "this is
  the seat the mirror happens to award"**. On archipelago seed 1 the parent
  simultaneously "wins" seat b and "loses" seat a — in one game.
* Per-pair flip attribution is therefore *candidate-vs-parent head-to-head*
  attribution, not candidate-vs-field. It is still causally readable (single
  toggle chain, all-sides NOISE_OFF, `--tle 0`), which is what this read does.

---

## 1. SECTION 1 — the three shipped toggles (g84 → h85)

### 1.0 What is actually gated (code read, `bots/_v85hs/main.py`)

| Toggle | Call sites | Effect measured here |
|---|---|---|
| `HS_SEAT_PROTECT_ON` | turret scan `:3233`, `_try_harvester` `:3290`, `hive_bunker` barrier `:3332`, second harvester site `:3539`; `_seat_ban()` defined `:2705-2731` | fires on 2 of 5 pairs |
| `HS_HEAL_DETAIL_ON` | `_defend` no-threat fallback `:2277`, `_defend` come-home walk `:3444`, second come-home walk `:3658`; `_seat_seek_target` `:2766` | fires on 2 of 5 pairs |
| `POP_CEILING_LIFT_ON` | core spawn budget `:1691` | fires on 3 of 5 pairs |
| `HS_SEAT_BAN_CONVEYORS = False` | `_pave_ban()` `:2733` returns `None`, so `_link_path` `:3917/:3929/:4019`, `_link_step` `:4077` and both pave sites `:4307/:4333` are **unchanged from the parent** | confirmed inert: conveyors still land on BAN seats in every h85 game |

Reserved delivery seats reproduced exactly by importing the candidate's own
`heal_seats` / `delivery_seats` / `MAP_CODES` (atlas hit **exact** on all five
maps, verified against the replay's own tile grid):

| map / seat | core | seats | KEEP (delivery, exempt) | BAN |
|---|---|---|---|---|
| archipelago seat B | (19,19) | 8 | (20,18) (21,19) | (18,19) (18,20) (19,18) (19,21) (20,21) (21,20) |
| meander seat A | (11,3) | 8 | (10,3) (13,3) | (10,4) (11,2) (11,5) (12,2) (12,5) (13,4) |
| lighthouse seat A | (3,3) | 8 | (4,5) (5,4) | (2,3) (2,4) (3,2) (3,5) (4,2) (5,3) |
| jackpot seat A | (0,0) | **4** (corner core) | (2,0) (2,1) | (0,2) (1,2) |
| jackpot seat B | (14,14) | **4** (corner core) | (14,13) (15,13) | (13,14) (13,15) |

> **Corner-core note.** On jackpot the ring is 4 seats, not 8, and
> `HS_DELIVERY_SEATS = 2` therefore reserves **half the ring**. The plank's
> sizing was reasoned from an 8-seat ring; on corner cores it is a 50% ban, and
> jackpot is where the plank does its only measured damage (§1.4).

### 1.1 Per-pair summary

| pair | first divergence | what diverged | mechanism | outcome g84 → h85 | verdict |
|---|---|---|---|---|---|
| `archipelago_1_b` | **r25** | parent builds sentinel `#69` @(19,18) (BAN seat); candidate builds nothing, sentinel goes to (18,18) at r32 | `HS_SEAT_PROTECT` (turret gate `:3233`) | r1000 tiebreak win → **core death r277** | **mechanism-plausible, negative** — named channel, 252 rounds of amplification |
| `meander_1_a` | **r6** | parent builds sentinel `#17` @(12,5) (BAN seat); candidate's `#12` moves to (13,4) and heals the core one round earlier | `HS_SEAT_PROTECT` (turret gate) | core death r635 → **r1000 win** | **mechanism-plausible, positive** |
| `lighthouse_4_a` | **r124** | candidate spawns builder `#352` @(4,5); parent is frozen at exactly 13 lifetime spawns with bank 26 | `POP_CEILING_LIFT` | core death r259 → **r1000 win** | **mechanism-direct, positive** |
| `jackpot_1_a` | **r37** | builder `#11` at (2,2) walks to (1,2) (parent) vs (2,1) (candidate) — two equivalent free seats, different tie-break | `HS_HEAL_DETAIL` (`_seat_seek_target` → `free[0]`) | core-kill win r151 → **core death r149** | **mechanism-direct, negative** |
| `jackpot_1_b` | **r21** | builder `#8` at (11,13) steps to (11,14) (parent) vs (11,12) (candidate); no co-located build/spawn difference | `HS_HEAL_DETAIL` by elimination (only movement-changing toggle) | core death r150 → **r1000 win** | **butterfly-cascade-suspect** — thin mechanism content, 130-round gap |

### 1.2 THE ARCHIPELAGO REGRESSION — attribution

**Cause: `HS_SEAT_PROTECT` is a unilateral disarmament of the seat ring. Our own
impassable buildings on seats are not only a cost (they deny us +4 HP/round);
they are also the ring's garrison, and removing them let the opponent's melee
occupy it.**

The chain, all from replay-events, `h85_archipelago_1_b` vs
`g84_archipelago_1_b`:

1. **r25 — the gate fires.** Parent: `PLACE B sentinel #69 @(19,18) dir=NW`,
   built by builder `#12` (BUILD `#12 -> (19,18)`). (19,18) is a BAN seat, so
   the candidate's turret scan skips it; candidate's `#12` heals (20,19)
   instead and the counterbattery sentinel goes up **7 rounds later and one
   tile off the ring**, at (18,18) (corner-diagonal, `d²=2`, not a seat).
2. **The parent's seat turret lives 217 rounds** (`#69` r25→r242) and is
   replaced by gunner `#333` on the same tile at r252. Across the whole game
   the parent holds an own impassable building on a seat for **965 seat-tile-rounds**;
   the candidate for **0**.
3. **The ring goes to the enemy.** Enemy builder-bot-rounds standing on our
   eight seats: parent **21**, candidate **194** (190 distinct rounds).
4. **Which is how the core actually died.** Damage events on our core:

   | source | parent | candidate |
   |---|---|---|
   | enemy builder attacks on core footprint | **0** | **189** (`#3`: 124, `#9`: 65) → 378 HP |
   | enemy turret fire | 128 | 113 |
   | enemy turret **planted on our seat (20,18)** | none ever | gunner `#340` at **r175**, 100 shots |

   In the candidate, our conveyor `#55` on (20,18) is destroyed at r174 and the
   enemy builds a gunner on that exact heal seat at r175. In the parent the same
   conveyor dies at r81 and the enemy never plants there — the (19,18) sentinel
   covers the approach.
5. **Siege ledger.** Parent: one episode r21-r162, 870 damage, 155 heal actions,
   **ratio 0.71**, core recovers to 500 (net damage 288 < the 500 HP pool — a
   short-of-buffer survival, not a law violation; see §3.3). Candidate:
   r21-r31 ratio **0.95** (survives, law-consistent) then r88-r276, 1,120
   damage, 185 heal actions, **ratio 0.66**, 1.02 builders on seat per damage
   round with 5 free seats, bank median 13 — **core dead r277**.
6. **Not the ceiling lift, not the heal detail.** Candidate post-opening
   spawns: **1** (r73, bank 7). Parent: 9. The lift never fired here; the
   candidate died bank-starved with a broken economy (5 harvesters vs 17, 29
   conveyors vs 67).

**Candidate causes tested and excluded.** *Heal detail pulling builders off
economy*: in the aligned window r21-r162 both variants show the identical
1.17 builders-on-seat and identical latency 2 — no pull. *Ceiling lift
overspending the bank*: one extra spawn all game. *Pure butterfly*: rejected —
the divergence is a gated build site, and the mechanism's fingerprint (own
impassable seat-rounds 965 → 0, enemy seat-rounds 21 → 194) is still legible at
the moment of death 252 rounds later. The one honest caveat is the 252-round
gap: I call it **mechanism-plausible**, not mechanism-direct.

**Generality check.** This is not a one-map accident. Own-impassable-on-seat
tile-rounds collapse to ~0 in *every* candidate-side game (0, 82, 0, 0, 0) and
are large wherever the gate does not fire (965, 666, 216, 213, 988). The
seat ring being permanently open to enemy melee is a structural property of the
plank, not of archipelago.

### 1.3 The two positive flips — did the designed mechanism do it?

**`lighthouse_4_a` — YES, mechanism-direct, and it is the CEILING LIFT.**
The parent stops spawning at exactly **13 lifetime builders** = `spawn_cap 5` +
`REPLACEMENT_MAX 8`, at r116, with bank 32. The candidate's first divergence is
the very next spawn, r124 `builder_bot #352 @(4,5)`, at bank 26 — the same bank
band the parent was still spawning at. Ceiling, not titanium, was binding.
Candidate reaches 52 lifetime spawns. The flip lands inside the *same siege
episode*, which is what makes this one direct:

| aligned window r124-r139 | parent | candidate |
|---|---|---|
| core damage | 112 | 91 |
| heal actions | 14 | 25 |
| **heal/damage ratio** | **0.50** | **1.10** |
| arrival latency (first dmg → first heal) | 5 | **1** |
| builders on seat / damage round | 1.00 | **2.23** |
| population (max / mean) | 7 / 7.0 | 9 / 8.25 |

Extended to r124-r259 (the parent's death window): ratio **0.33 → 1.07**,
on-seat **0.65 → 2.00**. Parent's second episode r195-r258 is the idle-bank
death the plank was written against — ratio **0.21** with bank median **986**
and peak **1,290**. Candidate: three episodes, ratios **1.03 / 0.95 / 1.14**,
all on the survive side of the bimodal law, core at 500 HP at r1000.

**`meander_1_a` — YES but it is SEAT PROTECT, and the lift only arrives at r443.**
r6: parent's builder `#12` builds sentinel `#17` @(12,5) (BAN seat); the
candidate's `#12` moves to (13,4) instead and **heals the core at r7 instead of
r8**. From there the candidate's economy runs and the parent's does not:

| | parent | candidate |
|---|---|---|
| harvesters (rounds) | 2 (r5, r9) | 15 (r5, r9, **r100**, r277, r312, …) |
| titanium delivered | **140** total | 290/230/290/500/500/1080/1400/2000/1990/1990 per 100r = **10,270** |
| lifetime spawns | 5 (all opening; bank-starved, 0 post-opening) | 49 (first post-opening **r443**, bank 10) |
| siege | one episode r5-**r634**, 5,040 dmg, ratio **0.90**, dead r635 | r5-r50 ratio 0.93, r98-r184 ratio 0.97, then never shelled again |

The parent is pinned for 630 rounds at ratio 0.90 — squarely in the bimodal
dead zone — and finally loses. The candidate breaks the siege by r184. The
ceiling lift is *not* the driver: it fires 259 rounds after the parent already
died. **Attribution: seat protect (positive here), ceiling lift a passenger.**

Aligned-window, population-controlled (both at 5 builders): r5-r50 on-seat
**1.25 → 2.35**, latency **3 → 2**; r5-r184 on-seat **1.72 → 2.02**, latency
**3 → 2**.

### 1.4 `jackpot_1_a` — the race lost by one round, and it is HEAL DETAIL

The one-round difference has a name. Both games run identically to r36. At
**r37** builder `#11`, standing at (2,2), has two free seats at equal walking
distance: (1,2) and (2,1). The parent's pre-plank target is `self.core`, which
`_bfs_direction` expands to (1,2). The candidate calls `_seat_seek_target`,
which returns `free[0]` after sorting by `(manhattan, y, x)` — the `y` tie-break
picks **(2,1)**.

What that costs, measured over the identical episode r36-r149:

| | parent | candidate |
|---|---|---|
| `#11` seat-rounds / heal actions | (1,2): 110 / **106** | (2,1): 111 / **108** |
| second healer | `#7` on (2,1): 37 rounds / **36 heals** | `#9` on (1,2): 9 rounds / **9 heals** |
| total core heal actions | **142** | **117** |
| heal/damage ratio | **0.58** | **0.48** |
| builders on seat / damage round | 1.27 | 1.02 |
| core at end | **90 HP, enemy core killed r150** | **dead r149, enemy core at 24 HP** |

The primary healer simply swapped seats — no gain. The loss is the **second**
healer: in the parent `#7` holds (2,1) for 37 rounds; in the candidate that
seat is taken and `#7`/`#9` never converge on the vacated (1,2), managing 9
rounds. −25 heal actions = −100 HP, and the core dies with the enemy core at
24 HP, four rounds (7 HP/round of gunner fire) from the win.

Two contributing observations:
* `_seat_seek_target`'s cap (`if seekers >= len(free): return None`) reverts a
  unit to pre-plank behaviour whenever the local seeker count meets the free-seat
  count. On jackpot free-seat median is **3** (of 4), so the cap fires often and
  the *second* seeker is the one it silences.
* `_free_seats` has **no threat awareness**: it sorts by walking distance and
  fixed seat order only. The seat it chose, (2,1), is inside an enemy gunner's
  ray — enemy gunner `#340` @(4,1) built r145 fires at (2,1) at r146 (1 event,
  7 HP; minor here, but the exposure is systematic).

### 1.5 `jackpot_1_b` — read, and flagged

Divergence r21 is a single movement step by builder `#8` ((11,13)→(11,14)
parent, →(11,12) candidate) with no co-located build, spawn or heal difference.
By elimination it is `HS_HEAL_DETAIL` (the only toggle that changes movement),
but the step is *away* from the seat ring and I cannot name the branch. The
outcome (core death r150 → r1000 win) arrives 130 rounds later.
**Classified butterfly-cascade-suspect** per the instrument note.

The pair is still worth its place in the corpus for one reason: **the parent
leg contains the canonical convergence failure the plank was designed against.**
`g84_jackpot_1_b` r79-r150: **504 damage over 72 damage rounds, ZERO core heals,
0 of 72 damage rounds with any of our builders on a seat, 4 free seats
(the whole ring), bank 22-59** — money available, seats open, no healer ever
arrived. Core dead r150. That is the v73 read's "B g2 / B g4" pattern
replicating exactly. The candidate on the same map/seat was simply never
besieged after r23, so it is an absence of the failure, **not a demonstrated fix**.

### 1.6 THE CONVERGENCE ANSWER

**HS_HEAL_DETAIL does NOT fix arrival. It changes OCCUPANCY, and the sign is
map-dependent.**

Population-controlled aligned windows (identical builder counts in both legs,
so the effect is aiming, not bodies):

| window | pop (max/mean) | on-seat/dmg-round g84 → h85 | latency g84 → h85 | ratio g84 → h85 |
|---|---|---|---|---|
| archipelago r21-r31 | 5/5.0 = 5/5.0 | 1.71 → **2.29** | 2 → 2 | 0.73 → **0.95** |
| archipelago r21-r162 | 5/5.0 vs 6/5.63 | 1.17 → 1.17 | 2 → 2 | 0.71 → 1.33 |
| meander r5-r50 | 5/5.0 = 5/5.0 | 1.25 → **2.35** | 3 → **2** | 1.01 → 0.93 |
| meander r5-r184 | 5/5.0 = 5/5.0 | 1.72 → **2.02** | 3 → **2** | 0.96 → 0.99 |
| jackpot_1_a r36-r149 | 5/4.79 vs 5/4.75 | 1.27 → **1.02** | 2 → 2 | 0.58 → **0.48** |
| lighthouse r124-r139 | 7/7.0 vs 9/8.25 *(not controlled — lift)* | 1.00 → 2.23 | 5 → **1** | 0.50 → 1.10 |

Findings:

1. **Latency was never the binding constraint in this corpus.** In 7 of the 8
   measured episodes it is 1-3 rounds in *both* variants. The only large latency
   (parent lighthouse: 5 and 30) sits in the one window where population is
   *not* controlled — it is a bodies effect, not an aiming effect.
2. **What the mechanism actually moves is staffing count** — builders standing
   on a seat per damage round: +34% (archipelago), +88% (meander), −20%
   (jackpot). Two of three population-controlled improvements, one regression.
3. **The v73 failure mode — "builders never arriving, zero-heal siege with free
   seats and a live bank" — appears once in this corpus and it is in the
   PARENT** (`g84_jackpot_1_b`, 0/72). The candidate never faced the same siege,
   so this corpus **does not demonstrate that the plank fixes it**. It shows the
   plank raises staffing when staffing is already ≥1, which is a different
   quantity from converting a 0 into a 1.
4. **The reason to be careful about #2:** the seat chooser is greedy, distance-
   ordered and threat-blind, and its cap silences the *second* seeker exactly
   when free seats are scarce. On a 4-seat corner core that is the difference
   between two staffed seats and one (§1.4).

### 1.7 Seat builds — every own placement on a heal seat, all 16 games

Own **impassable** buildings (harvester / barrier / turret / launcher) landing
on a seat — the only thing the gate is supposed to stop:

| game | placements on a seat | which gate should have fired |
|---|---|---|
| `g84_archipelago_1_b` | r25 sentinel (19,18) BAN; r252 gunner (19,18) BAN | (parent — no gate) |
| `h85_archipelago_1_b` | **none** | gate held |
| `g84_meander_1_a` | r2 sentinel (11,5) BAN; r6 sentinel (12,5) BAN | (parent — no gate) |
| `h85_meander_1_a` | **r2 sentinel (11,5) BAN** | **`_try_siege_build` — UNGATED, see §1.9** |
| `g84/h85_lighthouse_4_a` | none / none | — |
| `g84/h85_jackpot_1_a`, `g84/h85_jackpot_1_b` | none | — |
| `hs_archipelago_1_a` | **r12 launcher (5,7) KEEP-exempt** | terminus exemption (§1.8) |
| `hs_saga_1_a` | **r17 launcher (3,4) BAN** | `_try_build_launcher` — UNGATED in hs |
| `hs_saga_1_b` | **r20 launcher (20,18) BAN** | `_try_build_launcher` — UNGATED in hs |
| `hsb_*` (all three) | **none** | b-rev gate held |

Conveyors keep landing on BAN seats in every candidate game (h85 meander r520
(12,5), r522 (11,5), r555 (12,2); h85 archipelago r19 (19,21) etc.) — correct
and intended, `HS_SEAT_BAN_CONVEYORS = False`. Verified inert.

### 1.8 hive_bunker residual — REPORT

* **Terminus-exempt impassable build on a heal seat: YES, one, and it is a
  launcher, not a barrier.** `hs_archipelago_1_a` r12: `launcher #29 @(5,7)`,
  where (5,7) is one of the two KEEP delivery seats. `_seat_ban()` exempts the
  termini, so nothing stopped it — except that in hs the launcher site is not
  gated at all, so the exemption was not even needed. The b-rev's full-8-seat
  launcher gate closes it (§2).
* **Zero harvesters were built on a KEEP seat** in any of the 16 games.
* **The `(20,4)`-class hive case is UNTESTED by this corpus.** No `hive` map is
  present, and **no barrier of any kind was built in any of the 16 games** —
  the `hive_bunker` path at `:3308-3339` never executed. The residual the
  builder flagged remains open; this read neither confirms nor clears it.

### 1.9 NEW RESIDUAL — a second, ungated turret build site

`_try_siege_build` (`bots/_v85hs/main.py:2560-2591`) builds sentinels and
gunners and **never consults `_seat_ban()`**. It is the forward-siege planner,
so it is usually far from home — but on meander it is not:

```
r2  PLACE A sentinel#9 @(11,5) dir=S      # (11,5) is a BAN seat of core (11,3)
r3  FIRE (11,5) -> (11,10)                # …firing at the enemy CORE — a siege gun
```

Built in **both** variants at r2. It cannot be the gated counterbattery scan:
at r2 the nearest enemy is at (11,10), `d² = 36` against builder vision
`r² = 20`, so no threat is visible and `:3233` cannot run. It is
`_try_siege_build`, and it cost the candidate one of its eight seats
(82 own-impassable seat-tile-rounds) on the very map the plank otherwise wins.

The corollary is uncomfortable and worth stating plainly: on meander that
ungated seat turret sits on the ring for ~80 rounds and the candidate *wins*,
while on archipelago the gate removes the equivalent turret and the candidate
*loses*. See §1.2.

### 1.10 Spawns and the ceiling lift

| game | lifetime spawns | post-opening | bank at post-opening spawns (med / min / max) | lift attributable? |
|---|---|---|---|---|
| `g84_lighthouse_4_a` | **13** = cap 5 + REPLACEMENT_MAX 8 | 8, last r116 | 27.5 / 9 / 34 | ceiling binding, bank not |
| `h85_lighthouse_4_a` | 52 | 47, first extra **r124 at bank 26** | 31 / 0 / 6,740 | **YES — direct** |
| `g84_meander_1_a` | 5 | 0 | — | bank binding (140 Ti delivered all game) |
| `h85_meander_1_a` | 49 | 44, first **r443 at bank 10** | 31 / 10 / 617 | yes, but 259 rounds after the parent died |
| `g84_jackpot_1_b` | 5 | 0 | — | — |
| `h85_jackpot_1_b` | 16 | 11 (r248…) | 342 / 0 / 1,395 | yes |
| `g84_archipelago_1_b` | 14 | 9 | 1,359 / 19 / 1,396 | — |
| `h85_archipelago_1_b` | 6 | **1** (r73, bank 7) | — | **no — lift never fired in the regression** |
| `g84/h85_jackpot_1_a` | 5 / 5 | 0 / 0 | — | no |

The lift's titanium cost is bounded by its own bank gate and shows no
overspend: the median bank *at* a lifted spawn is 31 Ti, i.e. the clause fires
exactly when a scaled builder is affordable and not otherwise. **No evidence
the lift overspent the bank in any game**, including the regression.

---

## 2. SECTION 2 — THE HSB DELTA (the 3-line launcher seat gate)

`bots/_v85hsb/main.py` = `_v85hs` + one gate at `:1830-1843` inside
`_try_build_launcher`, using the **full 8-seat set** (deliberately *not*
`_seat_ban()`, so the ≤2 delivery termini get no exemption). Verified by full
diff: that hunk is the only difference between the two files.

### 2.0 Corpus note

`hs_saga_1_a.replay26` ≡ `hs_saga_1_b.replay26` (md5 `86e12726…`) and
`hs_archipelago_1_a.replay26` ≡ `g84_archipelago_1_b.replay26` (md5
`2c42ffee…`). Cause is §0: **on saga and on archipelago seat A the candidate is
behaviourally identical to the parent, so the hs leg there IS the parent mirror
match.** Not a defect. It also means the hs leg of these three pairs is a clean
parent baseline.

### 2.1 The launcher placements — mechanism-direct in all three pairs

| pair | hs launcher | hsb launcher | first divergence |
|---|---|---|---|
| `archipelago_1_a` | **r12 @(5,7) — KEEP delivery seat, `d²=1` from core** | r13 @(5,8), off-seat, `d²=4` | **r12**: hs's `#11` acts (builds), hsb's `#11` moves to (5,7) and builds at (5,8) the next round |
| `saga_1_a` | **r17 @(3,4) — BAN seat, `d²=1`** | r17 @(3,6), off-seat, `d²=2` | **r17**: `builderBuild #11 → (3,4)` vs `→ (3,6)` |
| `saga_1_b` | **r20 @(20,18) — BAN seat, `d²=1`** | r20 @(21,19), off-seat, `d²=4` | **r20**: `builderBuild #12 → (20,18)` vs `→ (21,19)` |

Own-impassable seat-tile-rounds across the game: **988 → 0**, **216 → 0**,
**213 → 0**. The gate does exactly and only what it says.

### 2.2 `archipelago_1_a` — the marquee flip. Hypothesis: **PARTLY CONFIRMED, and the stated causal chain is wrong.**

The builder's hypothesis was *"the ungated launcher sat on a delivery terminus
(blocking economy/delivery), and the gate freed it"*.

**Confirmed half — it did sit on a terminus, and the terminus was wanted.**
Delivery stacks entering the core, by source tile:

| | hs (launcher on (5,7)) | hsb |
|---|---|---|
| (7,5) BAN seat | 738 | — |
| (4,5) BAN seat | 248 | 48 |
| (5,4) BAN seat | 247 | 48 |
| **(5,7) KEEP seat** | **0 — occupied by launcher `#29` for 988 rounds** | **29** |
| cumulative delivered by r100 / r150 / r200 | 450 / 700 / **950** | 480 / 860 / **1,230** |

hsb builds a conveyor on (5,7) at r97 — the exact tile hs's launcher was
standing on — and runs **+29% cumulative delivery through r200**.

**Refuted half — the win did not come through economy, and "blocking delivery"
overstates it.** hs finished the 1000-round game with **12,330** titanium
delivered (a steady 1,500/100r) against hsb's 1,250 in 202 rounds; hs's economy
was never crippled, it just started ~30 Ti behind. hsb won by **killing the
enemy core at r201**, not by out-banking.

**The chain that actually produced the kill**, traced end to end:

1. Gate → launcher at (5,8) instead of (5,7) → **the launcher's throw geometry
   shifts one row south**. Both games throw saboteur `#9` once: hs r39
   (4,6)→(8,11) `d²=41`; hsb r40 (4,7)→**(9,11)** `d²=41` — one tile closer to
   the enemy core.
2. Both saboteurs then run the identical script (attack (20,15) r59-r68, build
   a forward gun at (21,17), grind (23,16)). hsb is **2 rounds ahead** at the
   first forward gun (r76 vs r78) and **6 rounds ahead** at the second (r106
   vs r112). Both builds are bank-gated — bank drops to 4 in the build round in
   both games — and hsb's bank runs ahead exactly as much as its delivery does.
3. Enemy-core damage: hs **940** over 128 rounds from 4 turrets; hsb **1,218**
   over 163 rounds from the same 4 turrets **plus 20 direct builder attacks by
   `#9`**, which hs's `#9` never delivered (it died at r242).
4. Enemy core HP: hs bottoms at **212 (r162)** and heals back to **364** by
   r200 → r1000 tiebreak loss 12,330 vs 13,570. hsb reaches **0 at r201**.

**Confidence: mechanism-direct on the placement and the delivery delta;
mechanism-plausible on the kill.** The amplification from a 1-tile throw offset
to a 278-damage swing is large, and the +30 Ti at r100 is a thin margin for a
2-round funding gain — but the chain is continuous, every link is measured, and
there is no unexplained jump. *An offensive outcome from a defensive gate is
surprising on its face; the reason it is not magic is that the gated object is a
LAUNCHER — the one building in this file whose position determines where our
saboteur lands in the enemy half.*

### 2.3 `saga_1_a` — death r233 → kill r185

hs's launcher at **(3,4)** is impassable, on a BAN seat, and orthogonally
adjacent to the core, so it closes one of the four cardinal exits from the core
ring as well as costing a seat. hsb's (3,6) leaves both open.

| | hs | hsb |
|---|---|---|
| own impassable on seat | 216 tile-rounds | **0** |
| free seats (median, during siege) | 5 | **6** |
| our forward sentinel @(14,14) *(`d²=32` to the enemy core — exactly sentinel range)* | **r165** | **r38** |
| enemy-core damage | 202 over 13 rounds, first at r166 | **1,026 over 57 rounds, first at r39** |
| delivery rate | 287 /100r | **356 /100r**, of which **41 of 66 stacks arrive through (3,4)** — the tile hs's launcher occupied |
| siege r55-r184 | 1,080 dmg, 252 heals, ratio 0.93, on-seat 2.07 | 1,345 dmg, 257 heals, ratio 0.76, on-seat 1.99 |
| outcome | core dead **r233** | core **183 HP**, enemy core killed **r185** |

Here the "launcher blocked a delivery terminus" hypothesis is **cleanly
confirmed**: (3,4) carries 62% of hsb's deliveries and 0 of hs's. The 127-round
swing in the forward sentinel is the offensive channel and is a large
amplification of a 2-tile placement change — **mechanism-plausible**.

Note the heal ratios move the *wrong* way (0.93 → 0.76) and hsb still wins:
it wins the race rather than the siege. Consistent with the bimodal law's known
scope (§3.3): hsb's core absorbed 1,345 damage with 1,028 healed — net 317,
inside the 500 HP pool — and the siege was interrupted by the kill.

### 2.4 `saga_1_b` — both win; the economy delta

hs's launcher at **(20,18)** (BAN seat, `d²=1`); hsb's at (21,19), off-seat.
Delivery *sources* are the same three BAN-seat tiles in both, so here the
launcher did **not** block a used terminus — yet:

| | hs | hsb |
|---|---|---|
| titanium delivered | 2,460 in 233 rounds = **1,055 /100r** | 9,600 in 624 rounds = **1,538 /100r** (+46%) |
| harvesters | 10 | 14 |
| lifetime spawns | 5 (0 post-opening) | 13 (8 post-opening; ceiling lift, banks 42-2,729) |
| own impassable on seat | 213 tile-rounds | 0 |
| enemy-core damage | 1,750 over 98 rounds | 5,278 over 297 rounds |
| outcome | win r233 | win r624 |

The r23 saboteur throw again lands one tile closer in hsb ((20,19)→(16,16)
vs (21,20)→**(17,16)**, `d²` 25 → 32). The headline "hsb slower" is a framing
artifact: hsb's *rate* of delivery is 46% higher; it simply took a longer road
to the same core kill. **Mechanism-direct on the placement; the 391-round
outcome-length difference is amplification and should not be read as a
strategic slow-down.**

### 2.5 hsb section — what the gate does NOT do

Population-controlled staffing is essentially unmoved by the launcher gate, as
expected for a placement-only change: `saga_1_a` r55-r184 on-seat 2.07 → 1.99,
latency 1 → 1; `archipelago_1_a` r41-r137 on-seat 1.32 → 1.41, latency 1 → 1,
free-seat median 6 → 7. **The gate buys one seat and one tile of throw
geometry; it does not touch convergence.**

---

## 3. SELF-CHECKS

### 3.1 Parser validation — 10/10 and 20/20

Purpose-built decoder validated against `fcode run --json` sidecars on all 16
replays before any measurement: winner **16/16**, turn count **16/16**,
win condition **16/16**, and the `core_deliv × 10 == titaniumCollected`
end-to-end geometry check **32/32 team-sides, 0 mismatches** (the check
`tools/replay_schema.md` names as the cheapest proof a parser's geometry and
update handling are right). Map atlas cross-check: the candidate's own
`known_map_for` grid matched the replay's decoded tile grid **exactly on all
five maps**, so the reserved-seat sets in §1.0 are the ones the bot actually
computed, not an approximation.

### 3.2 HP-delta ledger — 0 unexplained damage events in 14 games

Every negative `updateHp` delta was matched, in engine order with live
positions and 2×2 core footprints, against the same round's `fireTurret`
targets and `builderAttack` targets:

| game | neg HP events | fire-attributed | attack-attributed | both | **unexplained** |
|---|---|---|---|---|---|
| g84/h85 `archipelago_1_b` | 386 / 746 | 257 / 118 | 129 / 418 | 0 / 210 | **0 / 0** |
| g84/h85 `meander_1_a` | 481 / 1,992 | 321 / 497 | 160 / 949 | 0 / 546 | **0 / 0** |
| g84/h85 `lighthouse_4_a` | 645 / 2,858 | 266 / 1,027 | 362 / 1,810 | 17 / 21 | **0 / 0** |
| g84/h85 `jackpot_1_a` | 224 / 211 | 159 / 151 | 55 / 50 | 10 / 10 | **0 / 0** |
| `h85_jackpot_1_b` | 1,197 | 217 | 972 | 8 | **0** |
| hs/hsb `archipelago_1_a` | 386 / 389 | 257 / 208 | 129 / 139 | 0 / 42 | **0 / 0** |
| hs/hsb `saga_1_a` | 582 / 377 | 144 / 150 | 438 / 227 | 0 / 0 | **0 / 0** |
| `hsb_saga_1_b` | 1,257 | 341 | 916 | 0 | **0** |

Damage magnitudes are exactly {2, 7, 18} everywhere = builder attack / gunner /
sentinel; heal magnitudes {1,2,3,4} = the +4 heal clipped at max HP.

**Damage-target law — re-verified and SCOPED.** Across 13 games, classifying
every `fireTurret` target tile by what stood on it:

| target tile held | outcome | n |
|---|---|---|
| a unit only | unit took the damage | **2,893** |
| a unit **and** a building | **unit hit, building untouched** | **128** |
| a unit and a building | building hit, unit untouched | 17 *(start-of-round occupancy snapshot; the unit moved within the round)* |
| a building only, no unit | **building took the damage** | **1,056** (45 no-op) |
| nothing | no damage | 122 |

Builder attacks damaged a builder bot **0 times in 14 games** (5,990 building
hits, 0 bot hits). So the project law holds in the case it was written for
(co-located: 128:17 in favour), and the scope clarification for the next
decoder is: **turret fire hits the tile's unit when there is one, and the
building when there is not** — it is not inert against undefended buildings.
Reading it as "turrets never damage buildings" would have mis-attributed 1,056
events in this corpus alone.

### 3.3 Bimodal-law check (heal actions × 4 / episode damage; ≥0.94 survives, ≤0.86 dies)

18 substantive episodes measured (episode = damage rounds separated by ≤30
quiet rounds, matching the v73 read's segmentation):

| game | episode | ratio | outcome | law |
|---|---|---|---|---|
| `h85_archipelago_1_b` | r21-r31 | 0.95 | survived | ✔ |
| `h85_archipelago_1_b` | r88-r276 | 0.66 | **dead r277** | ✔ |
| `h85_meander_1_a` | r5-r50 / r98-r184 | 0.93 / 0.97 | survived | ✔ (0.93 is inside the 0.86-0.94 gap) |
| `g84_meander_1_a` | r5-r634 | 0.90 | **dead r635** | gap case, resolved to death |
| `g84_lighthouse_4_a` | r124-r139 / r195-r258 | 0.50 / 0.21 | dead r259 | ✔ |
| `h85_lighthouse_4_a` | r124-r254 / r383-r403 / r965-r983 | 1.03 / 0.95 / 1.14 | survived | ✔ |
| `g84_jackpot_1_a` | r36-r149 | 0.58 | survived (won the race r150) | ✘ interrupted |
| `h85_jackpot_1_a` | r36-r149 | 0.48 | **dead r149** | ✔ |
| `g84_jackpot_1_b` | r79-r150 | **0.00** | **dead r150** | ✔ |
| `g84_archipelago_1_b` | r21-r162 | 0.71 | survived | ✘ buffer case |
| `hs_saga_1_a` | r55-r232 | 0.72 | **dead r233** | ✔ |
| `hsb_saga_1_a` | r55-r184 | 0.76 | survived (won the race r185) | ✘ interrupted |

**14 of 18 on the correct side; 2 exceptions are siege interruptions** (we
killed their core first — the same exception class as the v73 read's A g5), and
**2 are buffer cases** worth a note for the law's owner: `g84_archipelago_1_b`
(ratio 0.71, survived) has *net* damage 870 − 582 = 288, comfortably inside the
500 HP pool, and `hsb_saga_1_a` (0.76) has net 317. **The threshold predicts
death only once the episode's net damage exceeds the core's HP buffer**; short
or low-total sieges survive well below 0.94. Both prior corpora's episodes are
long enough that the distinction never surfaced. Recommend the law be stated
with the buffer caveat.

Two additional gap-zone data points (0.86 < r < 0.94, previously empty): 0.90
→ death, 0.93 → survival. The gap is narrowing from both sides and is
consistent with a threshold near 0.92.

### 3.4 Determinism verification

`tools/rdiff.py` on all 8 pairs. Every pair is **byte-identical (excluding the
`updatePlayers` records) from turn 0 up to the reported first divergence**,
which is what the paired instrument requires:

| pair | identical through | diverges at |
|---|---|---|
| `archipelago_1_b` | turns 0-24 | **r25** |
| `meander_1_a` | turns 0-5 | **r6** |
| `lighthouse_4_a` | turns 0-123 | **r124** |
| `jackpot_1_a` | turns 0-36 | **r37** |
| `jackpot_1_b` | turns 0-20 | **r21** |
| `archipelago_1_a` (hs/hsb) | turns 0-11 | **r12** |
| `saga_1_a` (hs/hsb) | turns 0-16 | **r17** |
| `saga_1_b` (hs/hsb) | turns 0-19 | **r20** |

Cross-checks: `g84_jackpot_1_a` vs `g84_jackpot_1_b` → *no behavioural
divergence over all 151 turns* (same game, both seats — §0); `hs_saga_1_a` vs
`hs_saga_1_b` likewise; `hs_archipelago_1_a` vs `g84_archipelago_1_b` → `cmp`
identical. All three are the self-play signature, and all three are consistent
with the det tables rather than contradicting them.

### 3.5 Channel discipline

Every count in this document is from **replay-events** (`.replay26` wire
format), named with game and rounds. Sidecar `.json` was used only for the
validation in §3.1 and never as a source. `print()` output: both lineages carry
exactly one `print(` call site (`_v85hs:1414`, `_v84g:1205`), a caught-exception
diagnostic; **zero botOutput stdout records appear in any of the 16 replays**,
so there is no bot-log channel in this corpus and stderr is invisible per the
decode law. `placeEntity` re-emissions on an existing entity id were tracked
separately as rotations and **none occurred** in any game (no gunner rotations
in this corpus). Launcher throws were identified as `moveBuilderBot` with
`d² > 1`: 1, 1, 2, 7, 2, 2 across the games that had them, all with a launcher
within `d² ≤ 2` of the origin tile.

---

## 4. Open items handed back to the builder

0. **Ship-note items** (from the gate summary): hsb inherits the
   archipelago-seat-b regression 8/8 (its own gate never fires there); the
   b-rev's positive flips are mechanism-named on two independent maps; the gate
   is variance-increasing on match duration in both directions; part of the
   `saga_1_b` +46% delivery rate is not explained by the freed terminus.
1. **`_try_siege_build` (`:2560-2591`) is an ungated turret build site** and it
   does put sentinels on heal seats (h85 meander r2, (11,5)). If seat
   protection is meant to be a property of the file rather than of four call
   sites, this is the fifth.
2. **The seat ring's garrison value is unpriced.** §1.2 measures it: own
   impassable seat-rounds 965 → 0 bought enemy seat-rounds 21 → 194 and 189
   builder attacks on our core. Any revision of the plank should decide
   explicitly whether an own turret on a seat is a cost or a wall.
3. **`_free_seats` is threat-blind and the seeker cap silences the second
   healer.** §1.4 is the whole jackpot loss in one tie-break.
4. **The hive `(20,4)` barrier residual is still untested** — no barrier was
   built anywhere in this corpus and no hive map is in it.
5. **Instrument**: the section-1 control leg is self-play and pinned at exactly
   50%. If the parent leg is meant to be a control, it needs a third-party
   opponent; if it is meant to be head-to-head, the "flip" vocabulary should
   say so.
6. **Bimodal law**: add the HP-buffer caveat (§3.3) before the threshold is
   used as a survival oracle on short sieges.
