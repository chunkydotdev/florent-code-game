# BUILD REPORT + READ — `bots/_v606skalman` (the disengage release)

**Builder s54, 2026-08-21T22:49Z (`date -u` in the same shell).** Copy of
`_v605skalman` + the v606 queue; two fresh opus diagnosis agents (items 1 and 4);
artifacts `scratchpad/s54_v606/`. Fixture = the authored NOISE_OFF `_v542wave`
benchmark copy, 15 pool maps x both seats = 30 games, seed pinned at 7 (map/seat
vary, seed never). No game-share claim, no submit, no platform match.

## THE HEADLINE: the builder-death jump was one class, and it was pure loss
**SK_DISENGAGE** — a forward body at or below 22 HP stops taking `SK_DANGER_COST`'s
"the flood already priced the danger" waiver and gets the v603 step-level danger
veto back, with the detour budget barred from forcing it home. Alone it is
**−16 builder deaths and by-r300 10 vs 9**; the wave as a whole:

| | v605 (`tape_k6`) | **v606 (`tape_FINAL`)** |
|---|---|---|
| kills / 30 | 11 | **11** |
| **by-r300** (primary) | 10 | **10** |
| **median kill round** | 208 | **160** (target was 180) |
| our core dead | 18 | 19 |
| **builder deaths** | **51** | **23** |
| belt deaths | 45 | 39 |
| 2nd-gun median round | 89.5 | **60** (benchmark donor: 63) |
| M1 belt connectivity A/B | 34.9 / 27.3 | **42.1 / 34.5** |

## Item 1 — the 17 → 50 → 51 jump, diagnosed and priced
**ONE CLASS.** Per-death attribution on all three tapes (role column validated by
separation: true labels give HOME_KEEPER mean min-d² to enemy core 230 vs SIEGE
40; a shuffle collapses it to 9.5): CAGE_WALKER deaths **on the enemy core's lap**
14 → 36 → 34, killer **sentinel 11 → 41 → 40**. Zero home-band deaths, zero
no-damage removals, zero launcher throws, on every tape.
**Leave-one-out on the v605 chassis names the flag:** `SK_DANGER_COST` off →
botD 51→**25** (26 of the +34); `SK_CYCLE_K` off → 45 (6); `SK_BELT_EST` off →
byte-identical (0). The K dose curve 2/4/6/12 → 69/53/51/58 says **K=6 is already
that curve's minimum, so re-tuning K is not the fix.**
**THEY BUY NOTHING.** Controlling for game length over 150 games,
r(deaths per 100 rounds, kill) = **−0.003**, by-r300 **+0.016**. The arm-level
correlation with eviction-armed share (0.86) is carried by **one cell**:
stavkirke seat B holds 15 of v605's 51 deaths and 958 armed rounds in a
1000-round game. Drop it and the arm with **half** the deaths has **more** armed
share (8.57% vs 6.05%). An r1000 is a defeat; an eviction headline carried by one
is not a purchase. ⇒ **fix the exposure, keep the route.**
**The exposure:** zero of the 49 forward deaths came from full HP; the modal body
enters its killing round at exactly **4 HP** (38 of 49), after a median 6 rounds
at hp ≤ 22, **moving in 32 of 49**. And `ct.get_hp()` with no id occurred **0
times** in the whole v605 source — the tree had no self-HP awareness at all.

## Item 2 — the belt-into-turret-band growth: the exception BINDS
Census (per-BUILD, reproduces the v605 report's 9/6 exactly): v603 **0** band
builds, v604 **9** builds / 6 deaths, v605 **9 / 6** — **1 of 30 games**
(holmgang seat B), marginal death rate **66.7% vs 11.7% overall**.
**The plain band-avoid term is an EXACT NULL and the instrument says why.** A
print-instrumented copy (`dbg_band`; local replays keep bot stdout) shows the
band-free pass failing on **5 of 12 replans**, always on the same seat (5,10),
because `belt_ban` had escalated its short southern route away by r81 —
**"unless it is the only route to the ore" is literally true there.**
⇒ shipped with **SK_BELT_BAND_DROP**: when only some seats are reachable
band-free, plan those and **drop the rest**. On the v605 chassis that was band
builds 9→0, belt deaths 45→40, **titanium collected identical (12370)** — the
chain through their guns delivered nothing.
⛔ **On the SHIPPED chassis it is inert**: `bandavoid_off` and `banddrop_off` are
byte-identical to `tape_FINAL`, because the other fixes stop the belt entering
the band at all. Kept ON as a guard against a measured hazard, reported as a null
on this fixture.

## Item 3 — the block-memo hypothesis: CONFIRMED on cost, still OFF on currency
Pre-registered gate: a 3-arm probe on helheim seat A (memo off / TTL 150 / TTL
40), 30-game arm only if the oscillation breaks **without** the 76-death cost.
The v606 expiry is `SK_BLOCK_TTL = 40` (v605's 150 removed, not left beside it);
the re-observation half already existed in v605 and is not new.
**Probe, re-run on the FINAL chassis (the v603 chassis lesson): PASSES.** Orbit
run 58r → 18r, our total deaths 12 → 5, builder deaths 3 → 2. ⇒ arm bought.
**30-game arm:** kills **13** (+2), **by-r300 10 (tied)**, median kill **198**
(+38), our core dead 17 (−2), **builder deaths 23 — identical to ship, the 76-death
cost is GONE**, belt deaths 47 (+8).
**VERDICT: SHIPPED OFF, and it is the closest call of the wave.** The primary is
tied; the wave's stated closing target is median kill r180, which `tape_FINAL`
hits at 160 and this arm misses at 198; and **the +2 kills are exactly the late
class** — 13 kills with 10 by-r300 is 3 kills past r300 against ship's 1, and the
programme prices r300+ at 0.82 against us. The **hypothesis is confirmed** (the
death cost was the missing expiry) and it is a live v607 candidate, not a refuted
road. Fifth mechanism-works-outcome-loses case in this line — but the first where
the *cost* half was proved and removed.

## Item 4 — the two livelocks
**(a) paths seat A: NOTHING refuses the plant.** 189 engineer turns after S1: 187
`walk_cd0`, 1 plant, **0 plant refusals all game**; `can_build_sentinel` never
False; funding never bit; `path_arbiter_ok` is inert (`SK_PATH_ARBITER = False`).
The refusing predicate is **the adjacency test itself** — the plant branch is
never *reached*. Two sub-causes: **A1** bot 11, 63 turns in a period-8 orbit at a
fixed site with `nest_best_d` pinned at 13 — the `SK_NEST_STUCK_ROUNDS = 60` guard
was **5 rounds from firing** when the orbit self-broke, and it **re-arms from
inside the orbit**; **A2** bot 146, **105 turns** pinned on two tiles in a
five-tile dead-end, **37 of them with `free_neighbours == 0` and a free action**,
because `SK_IDLE_ACT` was wired into `_cage_walker` twice and **no other role**.
Shipped: **SK_IDLE_ACT_ENGINEER** and **SK_NEST_STUCK_ROUNDS 60 → 25**.
**(b) fimbulwinter: a ROLE-SCOPE problem, not threshold / slack / re-arm.**
`period_cycle()` had one caller (`_cycle_commit`) which had one caller
(`_cage_walker`). The 188-round period-6 orbit is an **ORE_DENIER**;
`period_cycle()` reads 6 on **151 of those 188 rounds** while `commit_until` is
−1 on **all 188** — no window ever opened, so nothing could expire. Shipped:
**SK_CYCLE_ALL_ROLES** (the hoist **and** the two denier consumers — the hoist
alone is a no-op, a window nobody reads changes nothing). Orbits: seat A 188r →
130r, **seat B 305r → 77r**, and both games kill faster (r212→r160, r225→r150).
⛔ **What it does not reach, stated so the tape is not over-read:** 341 of 985
orbit-rounds on the diagnosed cells (34.6%) are **constant-target** orbits — a
`_nav`/`_bfs_direction` defect — and freezing a target that never moved is a
no-op by construction.

## Nulls and negatives, all on the record
* **SK_CYCLE_K_MAX 6→10 (ring 12→20): built, measured, EXACT NULL, NOT SHIPPED.**
  `tape_cyclek6` is **byte-identical in all 30 replays** to the shipped tape. The
  seat-B period-10 orbits shortened under `SK_CYCLE_ALL_ROLES` with K_MAX still 6,
  and the orbit that survives on seat A is period **twelve** — outside 10 too.
  The v604 comment claimed longer orbits "contain a period-≤6 sub-pattern often
  enough"; that is now refuted (`period_cycle()` returns 0 on 133/167 and 110/138
  of those rounds), and the constant is still not the lever.
* **SK_IDLE_ACT_ENGINEER: live but a null on the primary** (by-r300 10 both,
  median 160 both). Shipped ON as a diagnosed correctness fix; disclosed.
* **SK_NEST_STUCK_ROUNDS sweep is NON-MONOTONE** — 25 / 40 / 60 → by-r300
  10 / **9** / 10, median 160 / 193 / 189.5, botD 23 / 45 / 26. A non-monotone
  sweep is evidence the fixture cannot resolve the constant, so this is a
  disclosed coin-flip resolved on the stated target: both 25 and 60 tie the
  primary at 10 by-r300, and 25 is the only value that reaches median r180.
  **Its disclosed cost is real: helheim seat A flips from WON r189 to a loss**
  (`neststuck60` wins that cell at r139). The **re-arm defect** the diagnosis
  found — `nest_best_d` resetting to None on a turret death and re-arming on the
  orbit's own minimum — is **NOT fixed** and is the v607 item.
* **ALLOCATION: the pre-registered trigger FIRED, and the obvious answer is
  refuted.** The builder's on-the-record call was *accept the cost scale; revisit
  only if funding-wait rounds > 0 in ≥ 5 of 30 games*. Measured with the v605
  decomposition's validated per-round bank ledger: **v605 17/30, v606 15/30**
  (pre-S1 1, S1→S2 15; 783 waiting rounds). ⇒ **REVISIT.** The first arm tried —
  `SK_DOOR_GUN_CAP 2 → 1` — is a **clear negative**: by-r300 **10 → 6**, kills
  11 → 9, median 196, while titanium collected balloons to 19,700 and the funding
  wait falls to 10/30. Cutting door gunners buys economy and sells the kill. The
  allocation question stays open with that road closed.

## Verification
Static **8/8 scans PASS, 20/20 dirty controls FIRE** (8 new v606 controls; S6's
v604 assertion was rewritten to pin the v606 carve-out exactly, and is driven
both ways — veto restored for everyone, and carve-out widened to everyone) ·
aliveness **12 games both seats, 0 tracebacks, 0 exception-removals**, injected
NameError control fires 8/8 · cells: helheim_A **lap 1/12 → 4/12 but the GAME
regresses** (disclosed above), midgard A/B PASS both, fimbulwinter orbits
188/305 → 130/77 with both games killing faster, paths_A the engineer now plants
**twice** (r42, r175) from **one** body instead of two · fidelity **per seat**
(both-seat dir under one `--side` mis-attributes): drip lattice **100.0/100.0**
(bar 97.3), M4 band 96.6/96.4, **point-blank 0/0**, M1 34.9/27.3 → **42.1/34.5** ·
per-shipped-flag ablations both ways, **all re-run on the exact shipped chassis**
(`tape_FINAL` is byte-identical to `tape_cyclek6`, so the earlier pass transfers,
and it was re-run anyway) · `summary.py --check` positive control OK (34 / 46) ·
CPU wall-clock 6 games 9.20s (v605) → 9.48s (v606), **0 engine timeouts** ·
**platform match test STILL OWED.**

## v607 queue
1. **The `nest_best_d` RE-ARM defect** (named by the item-4 diagnosis, not fixed):
   the stuck clock restarts from inside the orbit, which is why the threshold had
   to be halved instead of the guard being made to work. Fix the trigger
   (`period_cycle() != 0` sustained) rather than the constant.
2. **Constant-target orbits** — 34.6% of orbit-rounds, a `_nav`/`_bfs_direction`
   defect no commit window reaches.
3. **The block memo with expiry** (item 3): mechanism confirmed, death cost
   removed, +2 kills, loses on median. Re-test on a chassis whose median kill has
   more headroom, or find why it costs 38 rounds.
4. **helheim seat A** — the cell that regressed from a r189 win; attribute it to
   the stuck constant and decide whether the constant or the cell is wrong.
5. **ALLOCATION, still open**: the funding-wait trigger fired at 15/30 and door
   gunners are refuted as the thing to cut. The wait is S1→S2, 783 rounds.
6. **stavkirke seat B** — 39% of v605's builder deaths in one r1000 cell; it falls
   to 1 death under `dangercost_off`. Verify SK_DISENGAGE covers it.
7. Standing: platform CPU test owed.

## Progression on the fixture (identical opponent, 30 games)
kills 0→0→6→8→9→11→**11** · by-r300 —→—→5→6→6→10→**10** ·
median kill —→—→198→256→275→208→**160**.
FIRST-CONTACT GATE: **NOT MET** (11/30 does not beat the screen). The wave moved
the median kill 48 rounds and past its r180 target, and cut builder deaths by 55%,
without moving by-r300.
