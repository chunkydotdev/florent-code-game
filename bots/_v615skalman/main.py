"""SKALMAN v614 (`_v614skalman`) -- TWO ROADS CLOSED, ONE INSTRUMENT RE-SCOPED.

⛔⛔ v614 IS `_v613skalman` BYTE-FOR-BYTE IN BEHAVIOUR.  `diff -r` against v613
is empty except for the comment blocks below, and the identity control is not an
argument from that diff: v614 at ship defaults reproduces the v613 SHIP tape
(`scratchpad/s54_v613/t_p134nb_*`) BYTE-IDENTICALLY, 30/30 replays on F1 and
30/30 on F2.  What v614 carries is a VERDICT and an INSTRUMENT, not a plank.

  ROAD 1, CLOSED -- SK_TUBE_FLOOR (PLANK 2 of v613).  Re-tested PAIRED with the
  ammo cushion it was accused of thinning.  It does not recover at any cushion.
  ROAD 2, CLOSED -- "the thin AMMO CUSHION is why the tube floor failed".  The
  cushion raise is NEGATIVE ON ITS OWN and it makes the tube floor's own
  mechanism WORSE: the S1->S2 funding wait it exists to shorten goes 995 ->
  1,276 -> 1,667 rounds as SK_AMMO_FLOOR goes 10 -> 20 -> 30 (F1, 30 games).
  The two planks pull in opposite directions on the same bank; there was never a
  cushion at which both could hold.  Full four-arm table: `scratchpad/s54_v614/`.
  INSTRUMENT -- S14 re-scoped to index ordering + the LIVE ship config, and the
  ancestor chain's dirty-control suite un-blinded (see `static_scan.py`).

--- INHERITED HEADER (v609; not refreshed by v610-v613) ---------------------

SKALMAN v609 (`_v609skalman`) -- THE GATE ON THE HOME ANSWER.

⛔ WHAT CHANGED FROM `_v608skalman`.  A DIAGNOSIS-FIRST wave with a narrow
mandate: resolve the three open cells the v608 verdict named, so the home
answer's admission can be decided.  Fixture throughout: 15 pool maps x both
seats = 30 games vs the NOISE_OFF `_v542wave` benchmark copy, seed pinned at 7
(map/seat vary, seed never).  ⚠ FIXTURE_OF_RECORD: one authored opponent on a
local screen PRIORITISES; it does not establish field prevalence.  No game-share
claim, no submit, no platform match.  Artefacts: `scratchpad/s54_v609/`.

  GATE B  SK_COUNTER_HP_MAX = 450    (⭐⭐ ON -- THE DECIDING FIX)  the ORE
          DENIER does not march at the gun until the core has absorbed THREE
          sentinel shots.  v608 marched on ALARM ROUND 1 at 96% core HP.
  GATE E  SK_COUNTER_SOFT_BODIES     (⭐ ON)  inside the counter-march ONLY, a
          builder body is priced (K=2) rather than walled, and the body HOLDS
          rather than sidesteps when the routed tile is plugged.
  GATE A  SK_COUNTER_YIELD_HOME      (⛔ OFF -- BUILT, MEASURED, COSTS A KILL)
  GATE D  SK_COUNTER_LIVE_TGT        (⛔ OFF -- BUILT, MEASURED, COSTS A KILL,
          alone AND on top of GATE E; the waste it removes was a SYMPTOM)

30 GAMES, THREE WAYS (v607 control -> v608 shipped -> v609 shipped; every tape
re-run on this chassis, never reused; the v607 control reproduces
`scratchpad/s55_v607/tape_FINAL` byte-for-byte in 30 of 30):

                        v607    v608    v609
  kills                  11      12      13
  by-r300 (PRIMARY)      10       9      10     <- RECOVERED
  median kill round     160     185     170
  our core dead          19      17      16
  builder deaths         23      30      29
  belt deaths            39      43      42
  unanswered streak med 26.5    13.0    13.0
  streaks >= 40 rounds   12       7       6
  pecks on a core-shooter 105    364     450
  M1 belt connectivity A 42.1   28.9    33.3
  Ti collected         12450   13880   14640

⭐ ITEM 1 -- THE DECIDING CELL, `icefloe_seatA` (v607 KILL r136, v608 our core
dead r129).  Traced round-by-round on both replays with a byte-identical
instrumented build.  THE CHAIN, AND IT IS SECOND-ORDER, WHICH IS WHY NO FENCE
OR RAY-CONFIRMATION ARM EVER TOUCHED IT:
  r37  enemy plants sentinel#64 @(5,16); r38 first core hit, 500 -> 482.
  r40  FIRST DIVERGENCE.  The denier (bot#8) abandons its route and marches --
       on alarm round ONE, at cfhp = 480, i.e. 96% core HP.
  r41  bot#8 steps (4,12)->(4,13) instead of (4,12)->(4,11).
  r42  THE FORK.  `_bfs_direction` pass 0 blocks builder bodies; (3,11) holds
       our own harvester#41 and (5,12)/(6,12) are walls, so (4,11) is THE ONLY
       GAP.  With bot#8 standing there the HOME KEEPER's shortest first step is
       WEST; with it vacated, EAST.  The keeper goes the other way.
  r43  the keeper's target flips to (6,11) -- an ore tile with an enemy gunner
       standing on it -- and r45-r57 it burns 13 turns pecking that gunner.
  r46+ NEVER BUILT: harvester#75 @(1,9), its entire route home (5 conveyors,
       r47-r58), four cage seals (r62-r69), and sentinel#125 @(17,8) at r95 --
       the gun that killed their core at r136 in v607.
  r58  bank hits 0 and stays there 35 rounds; titanium_collected 460 -> 140.
  r129 our core dies.
  ⛔ AND THE PECK BOUGHT ALMOST NOTHING: 4 pecks into sentinel#64, which our own
  gunner#65 was already killing -- it died at r48 instead of r49.  ONE ROUND.
  Cell total: 19 counter-pecks, 38 damage, ZERO turrets killed by pecking.

⭐ THE DOSE IS IN SENTINEL SHOTS ABSORBED BEFORE THE MARCH, AND IT IS A PLATEAU
(published HP is quantised by 4: 500 -> 480 -> 464 -> 446 -> 428):
    1 shot  (<= 480)     EXACT NULL, byte-identical to v608
    2 shots (472..464)   kills 13, by-r300 10
    3 shots (460..446)   kills 13, by-r300 10   <- 450 ships, the band's middle
    4 shots (440)        kills 13, by-r300 10
    6 shots (<= 400)     kills 12, by-r300 10
Both arms of the sweep were re-run on THIS chassis and reproduce the shape.
The gate does not disable the plank: pecks on a core-shooter go 364 -> 450.

⭐ ITEM 2 -- `bifrost_seatA`, THE REFUSAL, NOW NAMED.  The shooter WAS marked
(ray-confirmed rank 0 from r103), `corefire_fresh` held r105-r157 unbroken,
`_counter_target` returned (0,4) with the d^2 fence reading 5 of 100 every
round, the body was the ORE DENIER, and nothing above it stole the turn.  TWO
GATES IN SERIES REFUSED:
  4a THE ROUTER.  `step_to` returned True EVERY round -- so no stall detector
     this line owns can see it -- while the body held a period-10 orbit for 53
     rounds seven steps from its target with ZERO net displacement.  Cause:
     `_bfs_direction` pass 0 walls builder bodies and only runs the body-free
     pass 1 when pass 0 finds NO goal; pass 0 always found one via a 12-step
     detour.  One enemy body entering/leaving r^2=20 vision flipped the route's
     HOMOTOPY CLASS between two ADJACENT stances: from (3,8) the answer is EAST,
     from (4,8) it is WEST, forever.  GATE E fixes exactly this.
  4b THE SEAT.  Fixing 4a walks the denier to (0,6), ONE TILE from the seat, and
     it stops.  (0,4)'s only orthogonal neighbours are (0,3), (0,5) and (1,4);
     (1,4) is an enemy barrier, and an ENEMY BUILDER BOT occupies (0,5) for 50
     of the 53 alarm rounds.  A builder cannot attack a builder, so that seat
     cannot be cleared, and (0,3) needs a ~27-step tour the router never offers.
  ⇒ THE CELL REQUIREMENT IS STILL NOT MET (streak 55 -> 55, dead r157).  What
  changed is that the refusal is DIAGNOSED rather than open.

⭐ ITEM 3 -- THE M1 SEAT-A FALL, ATTRIBUTED TO TWO GAMES AND ONE MECHANISM.
42.1 -> 28.9 is `icefloe_seatA` (2/2 -> 0/1) and `jotunheim_seatA` (3/4 -> 0/4);
the other 13 cells are unchanged.  In BOTH, the new belt death is an ENEMY
BUILDER pecking a conveyor at d^2 1 of OUR CORE (icefloe r80, killer at (2,14);
jotunheim r163, killer at (7,5)) while the denier was away at the gun -- i.e.
the march IS paid for out of the home ring, as the v609 brief guessed.  GATE B
recovers icefloe outright (2/2) and M1 seat A returns to 33.3.  ⛔ THE RESIDUAL
IS ONE GAME AND IT IS NOT RECOVERED: `jotunheim_seatA` still ends 0/4, because
that game now runs to r265 rather than r197 (the kill lands at r264, still
inside r300) and the belt is read at a later, more degraded end state.

⛔ ITEM 3's OTHER CANDIDATE WAS BUILT AND IS A NEGATIVE.  GATE A -- "a body on
our own home ring outranks a gun five tiles out", which is the mechanism above
stated as a rule -- costs a kill (13 -> 12) at every fence tested (d^2 2, 8, 25)
and is shipped OFF.  The mechanism is real; the RESPONSE is not the answer.
Third time this line has had a confirmed mechanism invert on outcome.

ITEM 4 (measure only) -- THE FUNDING-WAIT REVISIT STAYS OPEN: 18 of 30 games
with S1->S2 funding-wait rounds, 1030 rounds total (v608 16/30, 937; v607 15/30,
783).  The bar (>= 5 of 30) is met for the third release running.  No allocation
arm was built: v606 refuted CUTTING door gunners and v607 refuted DEFERRING
them, and the brief holds that road closed.  ⚠ Part of the rise is length --
v609's games run longer than v607's -- and this counter is not length-normalised.

⛔ THE SHIP RULE, PRE-STATED BY THE BUILDER, AND WHICH BRANCH FIRED.
"v609 ships the home answer WITH its gate only if by-r300 >= 10 AND streak
median <= 20 AND no anatomy-cell regression."  Measured: by-r300 = 10, streak
median = 13.0, and the three cells v608 BROKE stay broken (auroraveil B 55 ->
23 -> 15, longhouse A 55 -> 14 -> 19, midgard A 55 -> 31 -> 27).
⇒ THE FIRST BRANCH FIRED: SK_COUNTER_PECK SHIPS ON, WITH ITS GATE.
THE BUILDER TYPES THE VERDICT.

--- the v608 header follows, unchanged ---

SKALMAN v608 (`_v608skalman`) -- THE HOME ANSWER.

⛔ WHAT CHANGED FROM `_v607skalman`.  Source: the v607 build report's item 5,
THE LOSS ANATOMY (`docs/research/BUILD-REPORT-v607skalman-2026-08-21.md`) and
its evidence in `scratchpad/s55_v607/`.  Fixture throughout: 15 pool maps x both
seats = 30 games vs the NOISE_OFF `_v542wave` benchmark copy, seed pinned at 7
(map/seat vary, seed never).  ⚠ FIXTURE_OF_RECORD: one authored opponent on a
local screen PRIORITISES; it does not establish field prevalence.  No game-share
claim, no submit, no platform match.  Artefacts: `scratchpad/s54_v608/`.

THE FACT: 19 of 19 losses die to ENEMY SENTINEL FIRE ON OUR CORE, and 13 of them
(the report's own table; its prose says 11) absorb exactly 504 sentinel damage
across exactly 28 shots.  We had never once contested it.

  SENSOR  SK_COREFIRE        (ON)  the CORE publishes "I am losing HP", the
          shooter tile when it can identify one, and its own HP, on slot 15 --
          the last free slot.  One writer.  ⛔ THE ALARM IS THE CORE'S OWN
          `get_hp()` FALL, not a geometric inference: a sentinel at d^2 <= 32 of
          a core TILE can sit at d^2 50 of the core ANCHOR, outside the core's
          own r^2=36 vision, so the shooter is a best-effort extra and every
          consumer degrades without it.  SK_COREFIRE = False is the whole wave's
          ablation identity and is BYTE-IDENTICAL to the v607 tape in 30 of 30
          replays.
  PLANK 1 SK_CORE_MEDIC      (⛔ OFF -- BUILT, MEASURED, A NULL THAT COSTS)
  PLANK 2 SK_COUNTER_PECK    (ON -- THE ONLY THING THIS WAVE SHIPS)  the ORE
          DENIER marches at the gun that is shooting our CORE and pecks it dead
          (40 HP / 2 damage = 20 builder-turns, and the shooter is inside its own
          r^2=32 of our core BY CONSTRUCTION, so this is a home verb), and the
          shooter is MARKED so SK_TARGET_PRIO's existing ladder prefers it for
          every turret shot and every adjacent peck.
  PLANK 3 SK_COUNTER_SENT    (⛔ OFF -- BUILT, MEASURED, AN EXACT NULL)
  SUB     SK_COUNTER_RAY_ONLY (OFF, and INERT on this fixture -- every shooter
          the tree ever identified was confirmed by its FACING RAY, so the
          disclosed reach-only fallback rung never fired.  The arm is identical
          to ship on all 30 replays.)
  ⛔⛔ NOT BUILT: `SK_RAY_BLOCK`, rung 1 of the commissioned ladder ("stand a
          body in the ray").  REFUTED BEFORE BUILD on an engine probe of our own
          (`docs/research/turret-line-blocking-2026-08-09.md`, gunner as the
          positive control): a SENTINEL's shot passes THROUGH entities in its
          line and does them ZERO damage (40 -> 40 through a builder bot, 30 ->
          30 through a barrier, full 18 onto the target), so there is nothing to
          absorb.  The s49 "a tile shot resolves against the builder on the tile"
          fact is TRUE and is about the TARGET tile -- which here is a CORE tile
          no builder can stand on.  Independently, the fixture opponent's own
          source picks its sentinel target by a strict priority ladder with
          CORE = 0 (best) and BUILDER_BOT = 3, so even the target-DIVERSION
          reading is a null by construction.  Full closure in sk_maps.py.

30 GAMES, v607 CONTROL -> v608 SHIPPED (the same fixture, re-run, never reused;
the v607 control tape reproduces `scratchpad/s55_v607/tape_FINAL` byte-for-byte
in 30 of 30):

  kills                    11 -> 12      our core dead        19 -> 17
  by-r300 (PRIMARY)        10 ->  9      median kill round   160 -> 185
  builder deaths           23 -> 30      belt deaths          39 -> 43
  sentinels built          61 -> 68      2nd-gun median round 60 -> 60
  LONGEST UNANSWERED-FIRE STREAK   max 140 -> 103 · median 26.5 -> 13.0 ·
                                   games at >= 40 rounds  12 -> 7
  pecks landed on a gun that had shot our core   105 -> 364

  ANATOMY CELLS -- four of the 504-damage class, chosen before the arms were run
  (`scratchpad/s54_v608/streak.py`, whose C1 control reproduces the v607 report's
  own table): longest unanswered streak, then the outcome.
    auroraveil seat B   55 -> 23   core dead r232 -> r259   (20 pecks at the gun)
    longhouse  seat A   55 -> 14   core dead  r94 -> r312   (22 pecks at the gun)
    midgard    seat A   55 -> 31   core dead  r95 -> r95    ( 5 pecks at the gun)
    bifrost    seat A   55 -> 55   core dead r157 -> r157   ( 0 pecks -- ⛔ CELL
      REQUIREMENT NOT MET, and it is not a reachability problem: the gun stands
      at (0,4) with our core at (2,5), d^2 5, on empty tiles, and our denier is
      alive for the whole game (our only loss is the core at r157).  The plank
      changed this game's play -- the final entity sets differ -- and never
      landed a peck.  That is the v609 diagnostic, not a shrug.)

⛔⛔ THE PRIMARY MOVED THE WRONG WAY AND IT IS ONE GAME.  by-r300 10 -> 9, and the
entire difference is `icefloe_seatA` (KILL r136 -> our core dead r129).  Every
other by-r300 kill survives, and the wave adds TWO kills that did not exist at
all (r524 on holmgang seat A, r605 on paths seat A -- both games where v607's
core simply died, at r203 and r243) and one that lands 33 rounds earlier
(yggdrasil seat B r401 -> r368), while stavkirke seat A stops dying at r673 and
survives the match.  Under
`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression` a fall in the timely-kill
rate is a REGRESSION on the stated bar, and it is reported as one rather than
argued around.  No tuning recovers it: RAY_ONLY, the march fence at d^2 50 and at
d^2 32 are all EXACT NULLS (identical on every column and every replay), because
the shooter is always ray-confirmed and always inside d^2 32 already.  THE
BUILDER TYPES THE VERDICT.

--- the v607 header follows, unchanged ---

SKALMAN v607 (`_v607skalman`) -- the v607 queue, and it is a ONE-FIX WAVE.

⛔ WHAT CHANGED FROM `_v606skalman`.  Source: the v606 build report's own v607
queue (`docs/research/BUILD-REPORT-v606skalman-2026-08-21.md`) + its evidence in
`scratchpad/s54_v606/`.  Fixture throughout: 15 pool maps x both seats = 30 games
vs the NOISE_OFF `_v542wave` benchmark copy, seed pinned at 7 (map/seat vary,
seed never).  ⚠ FIXTURE_OF_RECORD: one authored opponent on a local screen
PRIORITISES; it does not establish field prevalence.  No game-share claim, no
submit, no platform match.  Verification artefacts: `scratchpad/s55_v607/`.

  ITEM 1  SK_NEST_STUCK_FIX  (ON -- THE ONLY THING THIS WAVE SHIPS)  the nest
          stuck-guard's RE-ARM, which v606 diagnosed and did not fix.  Two
          halves: the clock no longer restarts when a re-site event re-picks the
          SAME tile, and the progress test is NET DISPLACEMENT from an anchor
          rather than per-round closest approach.  ⭐ THE PREDICTED EFFECT
          APPEARED: v606's sweep was NON-MONOTONE (25/40/60 -> by-r300
          10/9/10), v607's is 10/10/10 with median kill monotone in the constant
          (160/187/189.5).  The constant stays 25 on the stated ship rule
          (by-r300, then median).  On the primary it is a NULL: kills 11,
          by-r300 10, median 160, builder deaths 23 -- all identical to v606 --
          with 8 of 30 replays changed.  Shipped as a diagnosed correctness fix
          at zero measured cost, disclosed as a null.
  ITEM 2  SK_S2_PRIORITY     (⛔ OFF -- BUILT, MEASURED, A CLEAR NEGATIVE)
  ITEM 3  SK_BLOCK_MEMO_SCOPE (⛔ memo still OFF -- both conditional forms
          measured, both worse; the conditional split is REFUTED)
  ITEM 4  SK_STALL_NETDISP   (⛔ OFF -- the detector is validated, the COMMIT
          response is what costs; monotone dose curve in fire volume)
  ITEM 5  measure-only: the LOSS ANATOMY.  See the build report.

⛔⛔ THE HEADLINE IS ITEM 5, NOT ANY OF THE FIXES.  All 19 losses on the v606
tape die to ENEMY SENTINEL FIRE ON OUR CORE -- 19 of 19, zero gunner, ~zero
peck -- and in 11 of them the core takes exactly 504 damage, i.e. 28 sentinel
shots across exactly 54 rounds of UNINTERRUPTED fire that we never once break:
no heal, no body in the ray, no counter-kill.  Every plank in this wave was
aimed at our own navigation.  The thing that kills us is one enemy gun with a
clear line, and nothing in the tree contests it.

⛔ AND THE AXIS STILL HAS NOT MOVED: kills 11 and by-r300 10, unchanged across
v605, v606 and v607.  Four items were spent on it and four came back null or
negative.  That is the fact the v608 queue is built on.

--- the v604 header follows, unchanged ---

SKALMAN v604 (`_v604skalman`) -- v603 plus the four v604-queue NAV/STATE fixes.

⛔ WHAT CHANGED FROM `_v603skalman`.  Source: the v603 build report's own v604
queue (`docs/research/BUILD-REPORT-v603skalman-2026-08-21.md`) and the v603 lap
diagnosis (`scratchpad/s54_v603/diag/`).  Fixture throughout: 15 pool maps x both
seats vs the NOISE_OFF `_v542wave` copy.  ⚠ FIXTURE_OF_RECORD: one authored
opponent on a local screen PRIORITISES; it does not establish field prevalence.
Verification artefacts: `scratchpad/s54_v604/`.

  FIX 1  SK_DANGER_COST   (ON)   danger stops being a step-level PREFERENCE in
         `_nav` and becomes a PATH COST inside `_bfs_direction`: entering a tile
         a remembered enemy turret covers costs SK_DANGER_K = 6 extra steps.
         Implementation is Dial's algorithm over the existing padded byte grid
         (K + 2 circular buckets), sharing NAV_NODE_BUDGET and the one-per-call
         CPU probe with the plain flood, which still runs unchanged whenever no
         turret has been seen.  Verified against a heapq Dijkstra reference on
         395 random grids, 0 disagreements, with the control (flood K = 0 vs
         reference K = 6) producing 69 failures.  Ablation on the shipped
         chassis: kills 9 -> 8, and midgard_A's period-10 orbit 11 -> 74 rounds.
         `sk_common._danger_mask`, `_weighted_flood`, `_bfs_direction`, `_nav`.
  FIX 2  SK_CYCLE_K       (ON)   the position ring goes to 12 entries and any
         period k <= 6 with TWO full repeats is detected; on detection the body
         COMMITS to the target it is already walking toward for k + 2 rounds.
         The response is at the TARGET layer because the measured period-6-to-10
         orbits are two targeting authorities disagreeing, not a stepping bug.
         Ablation: midgard_A's longest orbit 11 -> 41 rounds (the cell fails).
         `sk_common.period_cycle`, `sk_roles._cycle_commit`.
  FIX 3  SK_ONE_CURSOR    (⛔ OFF -- BUILT, MEASURED, SHIPPED OFF).  One cage
         cursor owning seal / evict / lap-advance, advanced only on completion or
         a 20-round give-up.  It CLEARS the class-B cell it was built for
         (midgard_A 40 -> 0 rounds) and LOSES the game: 6 kills vs 9, median kill
         round r333 vs r275, eviction-armed rounds 3.3% vs 15.6%.  FIX 2 alone
         clears the same cell (11 rounds, under the 30-round bar), which is why
         both were built and separately flagged.  See the flag's own comment.
  FIX 4  SK_BELT_EST      (ON, and an EXACT NULL on this fixture -- read the
         next paragraph before believing anything about it).  `belt_built` stops
         being a per-body record of our own builds: vision now ADDS as well as
         removes, every belief carries an observation round, and the eight
         canonically-ordered terminus seats ride on slot 5 b24-31 so they survive
         body replacement.  `_belt_seed_store`, `_belt_seat_bits`, `belt_stale`,
         `_belt_watch`, `_belt_report`.

⛔⛔ THE FIX-4 FINDING, and it is about the v603 report rather than about v604's
code: **THE PREMISE DOES NOT OCCUR ON THIS FIXTURE.** v603 named "a replacement
keeper starts with an empty ledger" as the root cause of SK_COLLAR_ROUTE_GATE's
measured negative.  Measured over the 30-game tape: the HOME KEEPER dies in 2 of
30 games and **is replaced in 0 of 30** -- the seat counter never re-issues role
0 -- so no body ever runs with the empty ledger the fix repairs.  The estimator
is wired and its terminus word populates correctly (probed live on glacierkeep,
icefloe and bifrost), but `belt_est_adopted` and `belt_est_store` are 0 in every
game, and the ablation is byte-identical to the shipped tape in every column.
⇒ Kept ON as the correct world-model shape at zero measured cost, reported as a
NULL, and the honest consequence is banked: **v603's root-cause attribution for
the route gate is not established, because the mechanism it names is absent from
the fixture that measured the negative.**

⛔⛔ THE CLASS-A CELL STILL FAILS, AND THE CAUSE IS NOT THE ONE FIX 1 WAS AIMED
AT.  helheim_A reads lap-tiles-visited 1 of 12 in v603 AND in v604 -- the walker
tracks are identical, which is the first tell.  Traced live (`scratchpad/s54_v604/
dbg`, per-round `_nav` dump): from (7,5) the flood answers WEST toward a target at
(13,7), and it answers WEST **with the danger set forcibly emptied as well**, so
the danger term is not what is doing it.  The blocking set at that moment reads
`BARRIER (11,5) ours · BARRIER (10,6) ours · SENTINEL (10,4) ours`: helheim's only
throat between its two wall blocks is sealed **by our own siege nest and its prep
barriers**.  ⇒ CLASS A ON THIS MAP IS SELF-BLOCKADE, not turret avoidance.  The
tile-owner arbiter (design §4, ledger V2/V8) does not price "this build cuts the
walker's only route", and that is the v605 item, with this cell as its control.
It is NOT patched here: it needs the arbiter, not another movement flag, and a
fifth unbudgeted fix on a chassis that just moved is how ablations stop meaning
anything.

v605 QUEUE (evidence-priced, in order):
 1. The tile-owner arbiter must refuse a build that disconnects a live verb's
    route (control: helheim_A lap-tiles-visited, currently 1/12 in v603 and v604).
 2. The HOME KEEPER seat is never re-issued: the keeper dies in 2/30 games and is
    replaced in 0/30.  Either the seat should be re-claimable or FIX 4 has no
    premise -- decide it, do not leave both halves half-true.
 3. Median kill round r275 against KILL_TARGET r180.  `SK_DANGER_COST` off is
    r230 with one kill fewer; the exchange rate K = 6 is the tuning knob this fix
    exposes and it has been measured at exactly one value.
 4. M1 belt connectivity fell 41.9/34.4 -> 32.6/26.7 (seat A/B) across v603->v604
    with no plank aimed at it; attribute it before it is inherited.

--- the v603 header follows, unchanged ---

SKALMAN v603 (`_v603skalman`) -- v602 plus the tape602 KILL-LEVER fixes.

⛔ WHAT CHANGED FROM `_v602skalman`, and the doctrine change behind it.  Source:
`scratchpad/s54_autopsy602/tape602_autopsy.md` (30 game-sides, 15 pool maps x
both seats, one NOISE_OFF `_v542wave` opponent).  ⚠ FIXTURE_OF_RECORD: one
authored opponent on a local screen PRIORITISES; it does not establish field
prevalence.  Verification artefacts: `scratchpad/s54_v603/`.

THE HEADLINE THE TAPE FORCED: **100% of the 14,130 damage dealt to the enemy
core in 30 games was SENTINEL fire** -- zero pecks, zero gunner, zero launcher --
and we won 0 of 14 games with <= 1 sentinel against 6 of 16 with >= 2 (Fisher
2-sided p = 0.019).  ⇒ THE KILL LEVER IS SENTINEL COUNT.  The cage is a
healer-denial multiplier on the gun (heal-tax 0.49 at mean-held >= 3 vs 0.71
below it); it is not a damage channel and must not be sold seats to look for one.

  FIX 1  SK_NEST_PAIR        the siege engineer keeps TWO band sentinels
         standing, funded off COPY 7's own `need` arithmetic (no burst-bank).
         Ablation: sentinels 49 -> 34, >=2-share 53.3% -> 13.3%, sentinel shots
         1,144 -> 789, second-gun round 87 -> 180.  `_siege_engineer`,
         `_plant_gun`, `_nest_watch`, `_pick_nest`, `_nest_publish`.
  FIX 2  SK_TRUNK_NEAR       `_trunk_tiles()` EXCLUDED d^2 <= 13 of our own core
         and 87.3% of belt deaths happen inside it (victim d^2 median 1).  The
         cover set now carries the near trunk, the TERMINUS seats and the tiles
         a pecker must stand on.  Ablation: gunners 52 -> 27, near-trunk tiles
         covered at end 23/160 -> 5/139, belt deaths 34 -> 53, terminus deaths
         26 -> 41, peck-class deaths covered 5 -> 0.  `_trunk_tiles`,
         `_terminus_tiles`, `_cover_gun_action`.
  FIX 3  SK_EVICT_ARMED      the `not empty_seals` interlock is gone: eviction of
         an enemy building on a seal seat runs whenever the walker is at the ring
         with no BUILD action available, belt seats first and turrets last.
         Ablation: seal-seat attacks 366 -> 33, ring evictions 30 -> 1.
         `_evict_seal`, `_cage_walker`.
  FIX 4  SK_COLLAR_GUNS      stop the mass collar peck (91.1% of our melee
         budget, losing the exchange 4.8:1).  Ablation: collar pecks 359 ->
         1,544 per 30 games.  ⭐ The sub-flags matter and are separately
         ablatable: `SK_HOMEDEF_SKIP_BARRIER` (ON) carries essentially the whole
         reduction, `SK_COLLAR_ROUTE_GATE` (OFF, measured negative) does not.
         `_belt_evict`, `_route_gaps`, `_home_defence`.
  FIX 5  SK_CAGE_CEIL        ⛔ BUILT, MEASURED, SHIPPED OFF.  The dynamic accept
         bar works (rounds at/over bar 52 -> 1,062) and the outcome goes the
         other way (kills 8 -> 6).  See the flag's own comment.
  FIX 6  SK_LAP_ADJ_SEAL / SK_IDLE_ACT / SK_SPAWN_EXIT -- from the lap-stall
         diagnosis (`scratchpad/s54_v603/diag/`), which found THREE causes and
         not one: a danger-veto throat (1 of 6 games), a lap-advance livelock
         (4 of 6) and an enemy spawn-box (2 of 6).  Seal any adjacent empty seal
         seat, act when boxed, and never spawn into a zero-exit tile.
         Ablation: lapadj_off drops max_held median 3 -> 2 and raises belt deaths
         34 -> 57; spawnexit_off drops kills 8 -> 6; SK_IDLE_ACT is an exact NULL
         on this tape (the spawn fix pre-empts the box) and is kept as insurance.

--- the v602 header follows, unchanged ---

SKALMAN v602 (`_v602skalman`) -- v601 plus the tape601 NAVIGATION fixes.

⛔ WHAT CHANGED FROM `_v601skalman`.  Every number is from
`scratchpad/s54_autopsy601/tape601_autopsy.md` (v600: 15 distinct games seat A;
v601: 30 game-sides, both seats; one NOISE_OFF `_v542wave` opponent).  ⚠ One
local fixture, one opponent: FIXTURE_OF_RECORD makes this a PRIORITISATION, not
a field measurement.

  FIX 1  SK_CAGE_FIRST   the lap (seal behind / clear ahead / advance) now
         outranks `_peck_priority` inside `_cage_walker`, and the enemy CORE is
         off the walker's peck ladder while seal tiles are open.  v601 inserted
         the peck BETWEEN the seal and the advance; the core is adjacent to
         every seal tile by construction, so 92.6% (286/309) of walker lap
         actions became pecks, ring barriers/game fell 1.933 -> 0.767 and one
         walker parked 41 consecutive rounds losing a healing race 95:82.
         `sk_roles._cage_walker`, `_peck_priority(skip_core=)`.
  FIX 2  SK_DANGER_NAV   the movement layer reads `armed_memo` at last.  A tile
         a remembered enemy turret's RAY covers is taken only when no uncovered
         step exists.  fimbulwinter seat A: 42 bodies, 39 deaths, ALL on tile
         (7,6), all from one gunner at (8,7) we never touched.
         `sk_common._danger_tiles`, `_nav`.
  FIX 3  SK_CYCLE_BREAK  ⛔ CHASSIS CORRECTNESS, flagged for ablation only.
         A-B-A-B position shuttles are endemic (81.3%/97.9% of builder steps on
         fimbulwinter, 91.0%/72.7% on the v600 control); all four stavkirke
         seat-B builders sat in one for 1000 rounds and built nothing.  The step
         back is struck out, perpendiculars first, hold if neither.
         `sk_common._two_cycle_back`, `_nav`, `sk_roles._escape`.
  FIX 4  (no flag)       `_enemy_builder_adjacent` is FOOTPRINT-AWARE: the core
         is 2x2 and a heal on any of its four tiles heals all of it, so a healer
         beside a different core tile was invisible to the guard.  Plain bugfix.
  FIX 5  SK_SENSE_NAV    `_bfs_direction` fell back to greedy whenever
         `map_grid is None` -- 10 of 15 pool maps -- so navigation had NO wall
         knowledge there at all; and `_pick_nest` returned None on the same
         test, leaving the nest verb inert on two thirds of the pool.  Both now
         run off sensed terrain, every role sensing, with refutation halves.
         `sk_common._bfs_direction`, `sk_roles._pick_nest`, `_nest_site_watch`.
  FIX 6  (no flag)       `lattice_floor` applied unconditionally in `_drip`
         (96.8% -> 100% by construction).  `sk_core._drip`.

--- the v601 header follows, unchanged ---

SKALMAN v601 (`_v601skalman`) -- v600 plus three SURVIVABILITY planks.

⛔ WHAT CHANGED FROM `_v600skalman1`, and why each change exists.  Every number
below is from `scratchpad/s54_autopsy/tape30_autopsy.md` (n = 15 DISTINCT games;
the *_s11/_s12 pairs are byte-identical, the seed is inert).

  PLANK 1  SK_HARV_ESCALATE  the V1 rebuild ledger, extended from CONVEYOR
           tiles to HARVESTER tiles + killer inference published on slot 14.
           33/33 harvester deaths were annulus gunners; one gunner ate 22
           harvesters off one tile.  `sk_roles._harv_watch`,
           `_harvester_action`, `_infer_killer`, `_killer_report`.
  PLANK 2  SK_BELT_COVER     home-gun siting now scores (site, FACING) pairs
           and requires the facing RAY to cross live belt trunk beyond
           d^2 13.  0 of 42 dead belt pieces were in any firing line of ours.
           `sk_roles._door_action`, `_ray_cover`, `_cover_gun_action`.
  PLANK 3  SK_TARGET_PRIO    one strict target ladder for BOTH turret fire and
           builder pecks; a BARRIER is never a default target.  75.3% of our
           shots and 74.8% of our pecks landed on enemy barriers.
           `sk_roles._target_pri`, `_peck_priority`, `_turret`.
  BUGFIX   SK_ORE_SENSE      live-sensed ore.  7 of 15 games built ZERO
           harvesters because `map_ores` is empty on any map `known_map_for`
           cannot confirm (10 of the 15 pool maps) and nothing else ever walks
           a keeper to ore.  `sk_common._ore_scan` / `ore_list`.

--- the founding tree's own header follows, unchanged ---

SKALMAN v1 (`_v600skalman1`) -- the founding tree of the Skalman line.

Doctrine: `beancounters_replication_then_amplify` (PROGRAMME.md, 2026-08-21).
Phase 1 is REPLICATE THE MEASURED BASICS PROPERLY; phase 2 amplifies with our
own toolbox once the basics measure at parity.  `R1000_IS_DEFEAT` survives the
line change: the cage, the belt and the nest are MEANS -- core destruction is
the end.

Design: `docs/SKALMAN-DESIGN-2026-08-21.md`
Imports: `docs/research/SKALMAN-IMPORT-MANIFEST-2026-08-21.md`
Copy-spec: `docs/research/PLAYBOOK-beancounters-2026-08-21.md` §6

FILE MAP -- "which lines implement COPY N" is answerable per verb:

  sk_maps.py    map data + constants + the SK_* verb flags + the fresh store
                allocation; the VERBATIM map layer (MAPTRUST F1).
  sk_common.py  in_bounds, pack/unpack, the CPU guard, the displacement guard,
                the padded-BFS pathing, the tile-ownership arbiter (V2/V8),
                the target-HP-trend give-up rule (V7).
  sk_roles.py   COPY 8 role claim · COPY 8/#78 global belt + V1 escalation ·
                COPY 9 cage · COPY 1 ore denial · COPY 5 nest + V3/V4/V9 ·
                COPY 6+2 door and turret behaviour.
  sk_core.py    COPY 8 spawn plan · COPY 7 drip · COPY 6 threat publication.

WHAT v1 DELIBERATELY DOES NOT CONTAIN (design §5, so nobody greps for it):
no launchers · no ferry · no rush opening · no burst-bank funding · no
point-blank sentinel plants · no crash/kidnap toolbox · no CPU-denial anything
· no tiebreak-turtle branch.

⛔ SANDBOX AST CONSTRAINTS -- `finally:`, `except BaseException:` and
`except SystemExit:` are REJECTED BY THE VALIDATOR AT LOAD.  There are zero of
each in this tree and there must remain zero.  The wrapper below catches bare
`Exception`; SystemExit/KeyboardInterrupt derive from BaseException and
propagate automatically, which is both what the engine wants and the only thing
the validator permits.
"""

from fcode import Controller, Direction, EntityType, Environment, Position  # noqa: F401

from sk_core import CoreMixin
from sk_maps import SK_ROLES
from sk_common import CommonMixin
from sk_roles import RolesMixin


class Player(CommonMixin, RolesMixin, CoreMixin):

    def __init__(self):
        # --- identity / map (per-unit: module state is NOT shared between
        #     units -- one sub-interpreter each, engine-probed; the 16 store
        #     ints are the only channel and they lag one round) -------------
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.idx = 0
        self.seat = -1
        self.role = None
        self.role_parity = 0
        self.map_grid = None
        self.map_walls = set()
        self.map_ores = []
        # v601 BUGFIX (SK_ORE_SENSE): live-sensed ore, the fallback `_load_grid`
        # promised and never had.  `ore_scanned` makes each tile cost exactly
        # ONE get_tile_env over this unit's whole life, so the scan is bounded
        # by map area, not by rounds.
        self.sensed_ores = []
        self.sensed_ore_xy = set()
        self.ore_scanned = set()
        self.explore_i = 0
        self.explore_until = -1

        # --- movement / targeting -------------------------------------
        self.tgt = None
        self.stuck = 0
        self.prev_pos = None          # displacement memory (renamed raid_prev)
        self.thrown_rnd = -1
        self._nav_key = None
        self._nav_tpl = None
        # v607 ITEM 3: the two-slot nav template cache, keyed on whether the
        # blocker memo was consulted.  {bool: (key, template)}.
        self._nav_alt = {}
        # v602 FIX 3: the 4-entry position ring the 2-cycle detector reads, and
        # its counters.  ⛔ ON THE DISPLACEMENT GUARD'S CLEAR LIST (build rule
        # 5): it is a cross-round Position cache for a throwable body.
        self.pos_hist = []
        self.cycle_len = 0            # consecutive rounds the A-B-A-B held
        self.cycle_blocked = 0        # ... in which the break found no step
        self.cycle_escapes = 0        # capped demolition escapes used
        # v602 FIX 2: how many consecutive steps have been danger detours.
        self.danger_detour = 0
        self._danger_key = -1         # cache revision the set was built at
        self._danger_set = frozenset()
        # v604 FIX 1: the same set as a flat mask over the padded nav grid.
        # Keyed on (_danger_key, w2, h2) so it rebuilds only when the danger set
        # itself does -- the flood asks for it every call.
        self._dmask_key = None
        self._dmask = None
        # v604 FIX 2: the commit window a detected period-k cycle opens.
        self.cycle_k = 0              # newest detected period, 0 = none
        self.commit_until = -1        # round the target commitment expires
        # v607 ITEM 4: how many commit windows this body opened on a NET
        # DISPLACEMENT fire rather than a measured period.  Diagnostic only.
        self.stall_netdisp = 0
        self.commit_tgt = None        # the Position it commits to
        # v605 FIX 1 (SK_PATH_ARBITER): the route-level arbiter's state.
        # ⛔ NOT ON THE DISPLACEMENT GUARD'S CLEAR LIST, and that is the
        # deliberate half: build rule 5 clears caches that describe a place the
        # BODY no longer stands, and these describe the MAP.  A thrown body's
        # knowledge that tile (7,9) is the last throat is still true where it
        # lands.
        self._route_key = -1          # round the blocked grid was stamped for
        self._route_w2 = 0
        self._route_blocked = None
        self.path_veto = {}           # (x,y) -> round refused (expiring memo)
        self.path_vetoes = 0          # counter, for the ablation read
        # v605 FIX 2 (SK_BLOCK_MEMO): where an IMPASSABLE building has been
        # seen, keyed on the TILE -- the same durable fact `armed_memo` keeps,
        # for the same reason (a building is immovable), but consumed by the
        # nav template instead of by target selection.  ⛔ ALSO NOT ON THE
        # CLEAR LIST: it describes the MAP, not this body's place on it.
        self.block_memo = {}          # (x,y) -> round last seen blocking
        self._block_rev = 0           # bumped on membership change; template key

        # --- report-once latches --------------------------------------
        self.reported_cpu = False
        self.reported_error = False

        # --- sensing ---------------------------------------------------
        self.vis_enemy = []
        self.vis_friend = []
        self.enemy_harv = {}          # COPY 1 memory: (x,y) -> round last seen
        self.enemy_facing = {}        # COPY 2: enemy turret id -> (dx, dy)
        self.hp_memo = {}             # V7: target id -> (hp, round)
        self.give_up = {}             # V7: target id -> round we gave up
        # v601 PLANK 1/3: where enemy ARMED buildings have been seen, keyed on
        # the TILE and not the id -- a turret is immovable, so the tile is the
        # durable fact and it survives the entity leaving vision.
        self.armed_memo = {}          # (x,y) -> (EntityType, round last seen)
        # v602 FIX 2: the same fact keyed the same way for the DANGER TERM --
        # a turret's facing, so the movement layer can price a RAY not a disc.
        # `enemy_facing` is keyed on the entity id, which does not survive the
        # turret leaving vision; this is the tile-keyed twin.
        self.armed_facing = {}        # (x,y) -> (dx, dy)
        self._armed_rev = 0           # bumped on news; the danger cache key

        # --- HOME KEEPER ------------------------------------------------
        self.harv_tiles = set()
        self.belt_plan = {}
        self.belt_key = None
        self.belt_built = set()
        # --- v604 FIX 4: the belt ESTIMATOR's bookkeeping -------------------
        # `belt_built` stops being "tiles THIS BODY laid" and becomes "tiles we
        # believe carry one of ours", fed by vision and by the store.
        self.belt_seen = {}           # (x,y) -> round last OBSERVED present
        self.belt_term_bits = 0       # slot 5 b24-31 as last read/written
        self.belt_est_adopted = 0     # instrument: tiles adopted from vision
        self.belt_est_store = 0       # instrument: tiles adopted from the store
        self.belt_rebuilds = {}       # V1: (x,y) -> rebuild count
        self.belt_escalated = set()   # V1: tiles that became turret tasks
        self.belt_ban = set()
        self.belt_head = {}
        self.belt_cursor = None
        self.escape_ban = {}          # tile -> round the self-trap escape ends
        # --- v603 FIX 4: the collar peck ledger -----------------------------
        self.collar_pecks = {}        # tile -> pecks spent evicting an enemy
                                      # building off a planned belt tile
        self._gap_rnd = -1            # `_route_gaps` per-round memo
        self._gap_key = None
        self._gap_set = frozenset()
        # --- v610 PLANK 1: the DELIVERY SEAT ledger -------------------------
        # ⛔ KEYED ON (tile, occupant entity id), which is the whole fix:
        # `collar_pecks` above is keyed on the tile alone and never reset, so a
        # seat we clear once is conceded for the rest of the game the moment
        # they re-lay it (measured live, glacierkeep seat A r48 -> r146).
        self.seat_pecks = {}          # (x,y) -> (occupant id, pecks this episode)
        self.seat_peck_total = 0      # per-game bound on the whole plank
        self.seat_clears = 0          # instrument: pecks this plank landed
        self._seat_rnd = -1           # `_seat_targets` per-round memo
        self._seat_list = []
        # --- v611 SK_HOME_LAUNCHER (default OFF) ----------------------------
        # ⛔ PER-BODY STATE, and that is deliberate.  The keeper is the only
        # buyer and there is exactly one keeper role; publishing the site would
        # cost a store slot and slot 15 was the last free one (v608 took it).
        # A replacement keeper re-derives the site from the same inputs.
        self.hl_density = {}          # seat (x,y) -> rounds seen enemy-held
        self.hl_site = None           # Position: the chosen launcher tile
        self.hl_site_rnd = -1         # round the site was chosen (memo key)
        self.hl_banned = set()        # sites the treadmill bound retired
        self.hl_tries = 0             # rounds spent on the CURRENT site
        self.hl_gaveup = False        # the plank is done for this game
        self.hl_built = 0             # launchers this body has bought (<= MAX)
        self.hl_walk_rounds = 0       # instrument: keeper rounds spent walking
                                      # to the site (COST LINE 4)
        self.hl_throws = 0            # instrument: throws this LAUNCHER made
        self.door_guns = 0            # COPY 6b answers bought (capped)
        # --- v601 PLANK 1: the harvester half of the V1 rebuild ledger -------
        self.harv_deaths = {}         # (x,y) -> harvesters lost on that tile
        self.harv_ban = {}            # (x,y) -> round the ban expires
        self.harv_escalated = set()   # (x,y) -> a locate-the-shooter task now
        self.harv_killer = {}         # (x,y) -> Position of the inferred killer
        self.killer_pos = None        # newest inferred belt killer (published)
        self.killer_rnd = -1

        # --- CAGE WALKER --------------------------------------------------
        self.lap_i = None
        # --- v604 FIX 3: the ONE cage cursor -------------------------------
        self.cursor_kind = None       # 'seal' | 'evict' | 'lap' | None
        self.cursor_tile = None       # the (x, y) it owns
        self.cursor_since = -1        # round it was opened
        self.cursor_ban = set()       # tiles this body gave up on
        self.cage_sealed = set()
        self.cage_best = 0
        self.cage_advance = -1
        self.melee_tile = None
        self.melee_since = -1
        # v603 FIX 5: seal seats last SEEN carrying an ENEMY DELIVERY BELT
        # piece.  Remembered rather than re-sensed because the ceiling has to
        # stay stable when a seat leaves vision -- an unseen seat contributes to
        # neither `sealed` nor `empties`, and a ceiling that oscillates with
        # vision would flip the accept bar every time the walker turns a corner.
        self.cage_enemy = set()

        # --- ORE DENIER ---------------------------------------------------
        self.deny_tile = None
        self.denied = 0
        self.denied_tiles = set()

        # --- SIEGE ENGINEER -----------------------------------------------
        self.nest_site = None
        self.nest_face = None
        self.nest_prepped = 0
        self.nest_turret = None       # (id, Position, born round)
        # v603 FIX 1: the SECOND band sentinel, same tuple shape.  Two slots
        # rather than a list so `_nest_watch`'s per-turret V3/V4 bookkeeping
        # stays one branch per gun and the ablation is one flag.
        self.nest_turret2 = None
        self.nest_site2 = None        # the standing first site, while siting #2
        self.nest_deaths = {}         # V4: (x,y) -> round it killed a turret
        self.nest_lives = []
        # v602 FIX 5(b): sites refuted by vision (wall) or by the reachability
        # watchdog.  Without this set the re-pick oscillates on one tile.
        self.nest_bad = set()
        self.nest_best_d = None       # closest approach to the current site
        self.nest_since = -1          # round that closest approach was set
        # v607 ITEM 1: the NET-DISPLACEMENT half of the stuck guard.  `anchor`
        # is the tile the body has been sitting around; `anchor_rnd` the round
        # it was set.  Leaving a SK_NEST_STUCK_BOX box re-anchors, which is what
        # tells a slow walk from an orbit.  `prev_site` is the site last held,
        # so a re-pick returning the SAME tile does not restart the clock.
        self.nest_anchor = None
        self.nest_anchor_rnd = -1
        self.nest_prev_site = None
        self.stall_latched = False
        self.stall_shifted = False

        # --- v608 THE HOME ANSWER ------------------------------------------
        # CORE side (the sensor).  `core_hp_prev` is the whole detector: the
        # core is the only unit that can read its own HP, and a fall is the
        # alarm.  `cf_shooter` is a LATCH because a turret is a building and
        # cannot move -- the same durable-fact argument `armed_memo` runs on.
        self.core_hp_prev = None
        self.corefire_last = -1
        self.cf_shooter = None
        self.cf_shooter_rnd = -1
        # BUILDER side (the consumers).  `corefire_streak` is how many
        # consecutive rounds this body has seen a FRESH alarm; PLANK 3 spends on
        # it, so it is counted per body rather than published (11 bits are not
        # free and the keeper dies in 2 of 30 games).
        self.corefire_streak = 0
        self.core_heals = 0           # instrument: PLANK 1 heals landed
        self.counter_pecks = 0        # instrument: PLANK 2 pecks at the shooter
        self.counter_sents = 0        # PLANK 3 purchases (capped)
        self.march_ownskip = 0        # v612 FIX 1: pecks REFUSED because the
                                      # latched tile now holds one of OUR OWN
                                      # buildings (or its owner is unreadable)

        # --- v613 THE ANTI-APRON AXIS --------------------------------------
        # PLANK 1 (SK_APRON_DENY).  PER-BODY BELIEF, like every other memo in
        # this tree: the store has no free slot (v608 took the last one) and the
        # apron is a pure function of the core anchor, so a replacement keeper
        # re-derives the tile set and re-learns occupancy from its own vision
        # inside a few rounds.
        self._apron_cache = None      # the tile tuple, keyed on the anchor
        self._apron_key = None
        self.apron_ours = {}          # (x,y) -> round last seen carrying OURS
        self.apron_lost = {}          # (x,y) -> round it went empty = RELAY
        self.apron_relays = []        # rounds of relays, the rolling window
        self.apron_relay_total = 0    # per-game backstop
        self.apron_relaid = 0         # instrument: relays landed
        self.apron_losses = 0         # instrument: apron buildings lost
        # PLANK 2 (SK_TUBE_FLOOR) instruments.
        self.tube_noprep = 0          # turns the prep barriers were skipped
        self.tube_fund_waived = 0     # 1 once the ammo surcharge was waived
        self.tube_gap_relax = 0       # sites found ONLY at the relaxed spread
        # PLANK 3 (SK_PECK_FOCUS) instruments.
        self.peck_relaxed = 0         # pecks that skipped the V7 veto
        self.keeper_marches = 0       # keeper turns spent marching at a shooter
        self.keeper_holds = 0         # keeper turns spent HOLDING a peck seat
        # PLANK 4 (SK_PLUCK_AWARE) instruments.
        self.pluck_detours = 0        # marches routed to a launcher-safe seat
        self.pluck_retargets = 0      # distinct launchers marched at instead
        self.pluck_last = None

        # --- CORE ----------------------------------------------------------
        self.spawned = 0
        self.converts = 0

    # ------------------------------------------------------------------
    # entry -- VERBATIM `main.py:396-418` of `bots/_v542wave`, retargeted
    # ------------------------------------------------------------------

    def run(self, ct):
        # An exception escaping run() makes the engine PERMANENTLY delete this
        # unit for the rest of the match.  Catching it costs one round's
        # action instead; there is no situation where propagating is better.
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e == EntityType.GUNNER or e == EntityType.SENTINEL:
            self._turret(ct)
        elif e == EntityType.LAUNCHER:
            # ⭐ v611 SK_HOME_LAUNCHER.  Through v610 this branch did not exist
            # and the comment said so: "v1 ships zero launchers (design §3,
            # 'Ferry: NO in v1'); an unreachable branch is worse than none".
            # With SK_HOME_LAUNCHER False that is still true of the SHIPPED
            # tree -- the keeper never builds one, so this branch is never
            # reached and the flags-off tape is byte-identical to v610.
            self._launcher(ct)
