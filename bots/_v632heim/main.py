"""SKALMAN v618 (`_v618skalman`) -- THE SEAT-DEFENCE PACKAGE, BUILT IN FULL,
MECHANISM CONFIRMED ON EVERY PLANK, AND REFUTED ON ALL FOUR.

⛔⛔ v618 SHIPS BEHAVIOURALLY IDENTICAL TO `_v617skalman`.  All four planks and
the rider are `False`, and the identity is not an argument from a diff: v618 at
ship defaults reproduces a freshly-run v617 F1 tape BYTE-IDENTICALLY, 30 of 30
games, with the comparator driven to the other verdict on the same call
(v617 vs the package: 0 of 30 the same).  What v618 carries is a VERDICT, four
flags for any future re-test, and one repaired ancestor instrument.

THE QUESTION.  The measured hardest problem on this line: the enemy collar
lands on our eight delivery seats at median r11, the mirror cage holds 6.5 of 8
from r11 in 30/30 games, and 180 of the 220 enemy barriers standing at end of
game sit on one of OUR seats.  THREE BUILDER-TURN ANSWERS WERE ALREADY REFUTED
(v603's unbounded collar peck, v610's SK_SEAT_CLEAR, the launcher axis x3), all
naming the same cause: THE KEEPER'S TURN IS THE SCARCE RESOURCE.  Magnus's
design put the question to the OTHER instrument -- *"deal with it using
turrets ... not efficient that a builder pecks for 15 rounds"*.

THE ANSWER, and it is the cleanest negative this line has produced, because
EVERY MECHANISM COLUMN MOVED THE WAY THE DESIGN PREDICTED AND THE CURRENCY WENT
THE OTHER WAY.  F1 = 30 games vs the NOISE_OFF `_v542wave` copy, seed pinned,
map/seat varying; control = v617 = 14 kills / by-r300 12.

                                  kills  by-r300  medkill   seat POSS(us/them)
  v617 control                      14      12      201       0.136 / 0.660
  PLANK 1  SK_SEAT_CLAIM            12       8      267       0.438 / 0.487
  PLANK 2  SK_HOME_GUNNER           12       5      315       0.086 / 0.655
  PLANK 3  SK_GUN_ROUTEBLOCK         7       6      178       0.105 / 0.611
  PLANK 4  SK_SEAT_HEAL             14      12      201       0.136 / 0.681
  RIDER    SK_PECK_DEMOTE           14      12      201       (byte-identical)
  THE PACKAGE (all five)             7       6      205       0.386 / 0.481

  POWERED (two batteries, 900 games/arm each, NOISE_ON `_v542wave`,
  15 maps x 30 seeds x 2 seats; naive intervals -- the platform DEFF does NOT
  apply, see `scratchpad/s54_v618/powered.py` for the cluster enumeration):
      v617 control    share 0.3556 [0.3243, 0.3868]   by-r300 26.9%
      THE PACKAGE     share 0.2922 [0.2625, 0.3219]   by-r300 16.8%
        DELTA share   -6.33pp  95% CI [-10.65, -2.02]  <- EXCLUDES ZERO
        DELTA by-r300 -10.11pp 95% CI [-13.90,  -6.32] <- EXCLUDES ZERO
      v617 control    share 0.3778 [0.3461, 0.4095]   by-r300 26.4%
      PLANK 4 ALONE   share 0.3556 [0.3243, 0.3868]   by-r300 27.6%
        DELTA share   -2.22pp  95% CI [ -6.67, +2.23]
        DELTA by-r300 +1.11pp  95% CI [ -2.99, +5.21]
  ⛔⛔ AND THE CONTROL CALIBRATES THE INSTRUMENT, WHICH IS THE READ THAT
  DECIDES PLANK 4.  THE SAME v617 TREE, MEASURED TWICE ON THIS FIXTURE AT
  n=900, READS 0.3556 AND 0.3778 -- A **2.22pp SAME-BOT SWING**, because the
  powered opponent is the NOISE_ON `_v542wave` and the engine seed does not
  pin its RNG (the LOCAL F1/F2 fixtures use the NOISE_OFF copy and ARE
  bit-deterministic, which is why the identity controls are byte-exact).
  PLANK 4's entire point estimate is exactly one same-bot swing.  ⇒ THE SHIP
  RULE'S +/-1.5pp BAR IS FINER THAN THE FIXTURE'S OWN REPRODUCIBILITY AT
  n=900 AND CANNOT BE ADJUDICATED AT THIS n.  Both control runs sit inside the
  v614 baseline class 35.78% [32.68, 38.88], so the level is right; the
  RESOLUTION is not.  Successor item: a powered read intended to adjudicate a
  1.5pp bar needs either the NOISE_OFF opponent or ~4x the n.

⭐ PLANK 1 IS THE FINDING.  WE CAN TAKE THE SEATS.  Possession triples
(0.136 -> 0.438), theirs falls 17.3pp, their landing episodes on our seats fall
6.9 -> 5.3 per game, and the bait works exactly as designed: 114 of our 203
claimed seat pieces are chewed to death, ~10 pecks each, i.e. ~38 ENEMY
BUILDER-TURNS PER GAME committed to our own door.  AND WE STILL LOSE THE TIMELY
KILL (by-r300 12 -> 8).  The exchange is not turn-for-turn: their builders are
many and cheap at our door, our keeper is ONE body, and 6.8 conveyors a game is
+6.8% on the ONE GLOBAL ADDITIVE cost factor that prices every later build.

⭐⭐ PLANK 3 IS THE SHARPEST NUMBER OF THE WAVE, AND IT IS AN OPPORTUNITY COST
MEASURED DIRECTLY OFF THE WIRE.  Turret shots by victim, 30 games:
      control   core 1,452   barrier     0
      PLANK 3   core   924   barrier 1,353
1,353 shots into collar barriers bought 528 FEWER shots into their CORE --
3,696 HP, i.e. SEVEN AND A HALF ENEMY CORES' WORTH.  Ammunition is titanium 1:1
and the drip is need-based, so a barrier in a turret's ray is not a free shot,
it is a converted harvester.  ⛔ AND THE ROTATION IS MOST OF IT: with
SK_HOME_GUN_ROTATE off the same plank reads 13 kills / by-r300 11 instead of
7 / 6.  v601 already refused to spend 10 Ti and a round of cooldown turning to
face a barrier; PLANK 3's carve-out re-introduced exactly that error.

⭐ PLANK 2 INVERTS ITS OWN ADVERTISEMENT.  The home gunner does what T19 says:
enemy builder deaths 63 -> 88 (+40%), income Ti/game 483 -> 550 (+14%).  It
STILL costs the timely kill -- by-r300 12 -> 5, median kill 201 -> 315 -- and
the shape is the v615/v616 launcher finding repeated on a new entity: a +20%
scale surcharge landing BEFORE the kill machinery is funded.  ⛔ AND ITS
ROTATION GOES THE OTHER WAY FROM PLANK 3's: rotating a home gun toward a LIVE
threat helps (rotate-off reads 8 kills, not 12).  Rotation is not the defect;
rotating at a BARRIER is.

PLANK 4 is a MEASURED ZERO and is the only plank that reached the powered gate:
real dose (48 heal events on our seats, heals/game 0.8 -> 1.3), F1 kills 14 = 14,
by-r300 12 = 12, defeats 16 = 16, all 12 named F1 cells unmoved, F2 8 kills vs 7.
It ships OFF on three grounds and none of them is the noisy point estimate
alone: (1) no measured gain on EITHER local fixture's currency; (2) its powered
delta is one same-bot swing wide in a fixture that cannot resolve the bar; and
(3) its own DOORWAVE guard has NEVER produced its other verdict on the engine --
`seat_heal_refused` read 0 in every probed game -- so shipping it would ship a
live verb whose safety clause is verified only in the static battery.
Shipping a zero to carry an unverified guard is a trade with no upside.  ⛔ THE RIDER IS A NIL DOSE AND IS LABELLED ONE: its tape is
byte-identical to the control in 30/30 games, because `_belt_evict`'s peck path
already requires a route-gap tile and no home turret of ours ever BEARS on one.
It is not a null result; it is a verb that never fires on this chassis.

⛔ THE PACKAGE MOVES 12 OF THE 12 NAMED F1 CELLS.  A targeted fix moves few
cells; this is the v613 SK_APRON_BELT_PREF signature -- a high-variance rewrite
rather than an aimed change -- and it is recorded as such.

INSTRUMENT REPAIR, and it is INSTANCE SEVEN of the "a text anchor is not the
thing you think it is" class: the ancestor dirty-control harness
(`s54_v613/static_scan.py:mutate`) has always taken a METHOD NAME and has never
used it -- it substituted the first occurrence anywhere in the file.  v618's
`_seat_claim_action` legitimately contains two lines S15 anchors on, so two
ancestor controls silently mutated the WRONG METHOD and the suite reported
itself broken.  `scratchpad/s54_v618/static_scan.py` scopes the substitution to
the named method's AST span, which makes every ancestor control stricter.
⛔ AND THE FIRST CUT OF THAT REPAIR WAS INERT for the same reason one level up:
it patched the module that DEFINES the scans (v613) rather than the module
whose `main` RUNS them (v610).  Caught by its own control-of-the-control.

Artefacts: `scratchpad/s54_v618/`.  ⚠ FIXTURE_OF_RECORD: F1/F2 are authored
opponents on a local screen and PRIORITISE; the 1,800-game powered read is the
same arena, not the ladder.  No submit, no platform match.

--- INHERITED HEADER (v614; not refreshed by v615-v617) ---------------------

SKALMAN v614 (`_v614skalman`) -- TWO ROADS CLOSED, ONE INSTRUMENT RE-SCOPED.

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
        # --- THE ROUTE, ARM 1 (SK_ROUTE_HOME) -------------------------------
        # ⛔ UNCONDITIONAL, like every other attribute in this constructor: a
        # flag-gated attribute is how a masters-ON tape dies on AttributeError
        # in a branch nobody exercised OFF, and an escaping exception destroys
        # the unit permanently.  All seven are inert while the flag is False.
        self._rt_key = None           # `_route_missing` memo key
        self._rt_links = {}           # (x,y) -> rank, 0 = core-ward terminal
        self._rt_ring = None          # the core's spawn ring, memoised
        self.route_tgt = None         # ((x,y), first round) the walk is on
        self.route_bans = 0           # stall bans spent (<= SK_ROUTE_BAN_MAX)
        self.route_builds = 0         # instrument: links this arm laid
        self.route_walks = 0          # instrument: turns spent walking at one
        self.route_spawn_refused = 0  # instrument: spawn-reserve refusals
        self.route_siege_refused = 0  # instrument: siege-deferral refusals
        # --- v610 PLANK 1: the DELIVERY SEAT ledger -------------------------
        # ⛔ KEYED ON (tile, occupant entity id), which is the whole fix:
        # `collar_pecks` above is keyed on the tile alone and never reset, so a
        # seat we clear once is conceded for the rest of the game the moment
        # they re-lay it (measured live, glacierkeep seat A r48 -> r146).
        self.seat_pecks = {}          # (x,y) -> (occupant id, pecks this episode)
        self.seat_peck_total = 0      # per-game bound on the whole plank
        self.seat_clears = 0          # instrument: pecks this plank landed
        # --- v632 HEIMDALL PLANK 2: the DEMOLITION SWEEP ledger -------------
        # ⛔ UNCONDITIONAL, like every other attribute in this constructor.  A
        # flag-gated attribute is how a masters-ON tape dies on AttributeError
        # in a branch nobody exercised OFF -- and an escaping exception
        # destroys the unit permanently.  Same (tile, occupant id) keying as
        # `seat_pecks` above, for the same measured reason.
        self.demo_pecks = {}          # (x,y) -> (occupant id, pecks this episode)
        self.demolishes = 0           # instrument: pecks this sweep landed
        self.demo_walks = 0           # instrument: turns the DENIER spent
                                      # WALKING toward a sweep target it could
                                      # not reach (the s57 redesign's own
                                      # channel -- Z3 failed with no walk in
                                      # the plank at all, so this counter is
                                      # what makes the new path visible in a
                                      # readout separately from `demolishes`)
        self.demo_pick = None         # ((x,y), bid) of the current pick
        self.demo_seats = None        # frozenset of our 8 delivery seats (memo)
        self._seat_rnd = -1           # `_seat_targets` per-round memo
        self._seat_list = []
        # ⭐ s57 THE STAND, arm 3 (SK_SEAT_CLEAR_ADJ).  The SAME per-round memo,
        # untruncated: `_seat_walk` reads `_seat_list` (top SK_SEAT_CLEAR_N) and
        # `_seat_clear` may read this one.  ⛔ CREATED UNCONDITIONALLY, for the
        # engine reason every block in this file states: a flag gates BEHAVIOUR,
        # never the EXISTENCE of state -- a field created only under a flag is
        # how a flag-off arm raises AttributeError inside `run()`, and the
        # engine then PERMANENTLY DESTROYS that unit for the rest of the match.
        # It is written only inside `_seat_targets`, below that method's own
        # `if not SK_SEAT_CLEAR` return, so it stays EMPTY on every
        # SK_SEAT_CLEAR-off arm -- which makes it an OFF-IDENTITY WITNESS as
        # well as the widened aim's input.  Bounded by 8 (the seats are the
        # eight orthogonal neighbours of our 2x2 core footprint).
        self._seat_all = []
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
        # --- s57 THE KILLBOX, ARM 1 (SK_KILLBOX, default OFF) ---------------
        # ⛔ UNCONDITIONAL FIELDS.  A flag gates BEHAVIOUR, never the EXISTENCE
        # of state: a field created only under a flag is how a flag-off arm
        # raises AttributeError inside `run()`, and the engine then PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Every counter below
        # therefore reads 0 (or its null sentinel) on every OFF arm, which also
        # makes them OFF-IDENTITY WITNESSES.
        # ⛔ PER-BODY STATE, and the engine forces it: every unit gets its OWN
        # `Player` instance (kbprobe surprise 1), so the keeper's counters and
        # the launcher's counters live on different objects and are NEVER
        # summed in-bot.  The trace reads them per unit and aggregates offline.
        self._kb_cands = None         # memo: the pure-geometry chamber list
        self.kb_site = None           # Position: the chosen launcher tile
        self.kb_site_rnd = -1         # round the site was chosen
        self.kb_banned = set()        # sites the give-up bound retired
        self.kb_tries = 0             # rounds spent on the CURRENT site
        self.kb_gaveup = False        # the plank is done for this game
        self.kb_built = 0             # launchers this body has bought (<= MAX)
        self.kb_built_rnd = -1        # instrument: round the launcher landed
        self.kb_walk_rounds = 0       # instrument: keeper rounds spent walking
        self.kb_seals = 0             # instrument: seal barriers this body laid
        self.kb_cell_pos = None       # the chamber this body is building at
        self.kb_cell_done = False     # its seals all stand
        self.kb_cell_off = False      # the cell half gave up for this game
        self.kb_cell_miss = 0         # consecutive rounds with no viable
                                      # candidate (the give-up's clock)
        self.kb_plan_rnd = -1         # per-round memo of `_kb_cell_plan`
        self.kb_plan = None
        self.kb_cell_built_round = -1 # instrument: round the cell completed
        self.kb_throws_cell = 0       # instrument: throws INTO the chamber
        self.kb_throws_tread = 0      # instrument: throws onto the treadmill
        self.kb_opportunity = 0       # instrument: rounds this launcher had an
                                      # enemy builder inside its pickup disc
        self.kb_detain_rounds = 0     # instrument: rounds an enemy builder was
                                      # observed inside a SEALED chamber
        self.kb_escapes = 0           # instrument: occupant gone AND the seal
                                      # was broken -- a real way out
        self.kb_vanish = 0            # instrument: occupant gone with the seal
                                      # INTACT -- retired in place, not an
                                      # escape.  ⛔ THE SPLIT IS THE HONEST FORM
                                      # OF THE REGISTERED `kb_escapes` FIELD:
                                      # kbprobe STEP5a/5b measured that a
                                      # sealed body cannot move at all, so a
                                      # disappearance from an intact chamber is
                                      # a retirement (its own unguarded move()
                                      # raising, per STEP7) and reporting it as
                                      # an "escape" would invert the sign.
        self.kb_occ = {}              # chamber (x,y) -> occupant id last seen
        # --- s57 THE KILLBOX, ARM 2 (SK_KILLBOX_EXEC) ------------------------
        # ⛔ SAME PER-BODY RULE AS ARM 1, and here it is load-bearing twice
        # over: the EXECUTIONER's counters live on the SENTINEL's own `Player`
        # instance and the seat/build counters live on the KEEPER's, so the two
        # halves of this arm are never summed in-bot at all.  Every one of them
        # reads its null on an OFF arm, which makes them OFF-IDENTITY
        # WITNESSES as well as instruments.
        self._kb_cands_interior = False  # the memoised chamber list came from
                                      # the INTERIOR fallback, not the back edge
        self.kb_exec_seat = None      # Position: the chosen sentinel seat
        self.kb_exec_face = None      # Direction: chosen AT BUILD (a sentinel
                                      # cannot rotate -- seat and facing are one
                                      # decision, kbprobe STEP2)
        self.kb_exec_cell = None      # the chamber that seat covers
        self.kb_exec_off = False      # the executioner half gave up this game
        self.kb_exec_miss = 0         # consecutive rounds with no viable seat
        self.kb_exec_plan_rnd = -1    # per-round memo of `_kb_exec_seat_pick`
        self.kb_exec_built = 0        # sentinels this body bought (<= EXEC_MAX)
        self.kb_exec_built_rnd = -1   # instrument: round the executioner landed
        self.kb_execs = 0             # ⭐ instrument: SHOTS this sentinel fired
                                      # at a chamber tile
        self.kb_exec_opp = 0          # instrument: the OPPORTUNITY denominator
                                      # -- rounds an enemy builder sat in a
                                      # chamber inside this tube's raw attack
                                      # pattern.  Shots with no opportunity
                                      # rounds, and opportunity rounds with no
                                      # shots, are BOTH falsifiers.
        self.kb_retired_in_cell = 0   # ⭐ instrument: an occupant left a chamber
                                      # whose seal was INTACT.  kbprobe
                                      # STEP5a/5b: a sealed body cannot move at
                                      # all, so this is a RETIREMENT.
        self.kb_retired_shot = 0      # ... of which this sentinel had actually
                                      # fired at that occupant.  The honest
                                      # attribution split: the rest are the
                                      # peel (kbprobe STEP7, their own
                                      # unguarded move() raising).
        self.kb_retire_rounds = 0     # instrument: summed rounds from the
                                      # occupant's FIRST observed round in the
                                      # chamber to its retirement
        self.kb_recycles = 0          # instrument: a chamber that held an
                                      # occupant, emptied, and held ANOTHER --
                                      # the recycling column
        self.kb_cell_interior_built = 0   # instrument: 1 if the completed cell
                                      # came from the INTERIOR fallback list
        self.kb_exec_occ = {}         # chamber (x,y) -> (occupant id, first
                                      # round seen, shots we put into it)
        self.kb_exec_used = set()      # chambers that have held an occupant at
                                      # least once (the recycle detector)
        self.kb_exec_plan = None      # per-round memo of `_kb_exec_seat_pick`
        # --- ARM 2 ADDENDUM (CAPACITY BEFORE EXECUTION) ----------------------
        self.kb_det_by_cell = {}      # chamber (x,y) -> detained rounds, the
                                      # launcher's residency integral SPLIT
        self.kb_occ_by_cell = {}      # chamber (x,y) -> occupied rounds, the
                                      # sentinel's own split of the same thing
        self.kb_full_rounds = 0       # ⭐ rounds in which EVERY sealed chamber
                                      # was occupied -- capacity BINDING, which
                                      # is what the recycler exists to relieve
        self.kb_sealed_seen = 0       # sealed chambers this tube saw last round
        self.kb_exec_latched = 0      # shots taken because the LATCH held, not
                                      # because the overload gate opened
        self.kb_block_form = 0        # ⭐ HOW MANY CHAMBERS ACTUALLY STOOD when
                                      # the executioner was bought: 2 = the
                                      # prebuilt block, 1 = the DISCLOSED
                                      # single-chamber fallback on a board whose
                                      # geometry cannot carry a partner.  The
                                      # coverage split is measured, not assumed.
        # --- s57 THE KILLBOX, ARM 3 (SK_KILLBOX_FAST) ------------------------
        # ⛔ ALL INSTRUMENT, NO BEHAVIOUR: every field below is written under an
        # `SK_KILLBOX_FAST` conjunction and read by nothing that decides
        # anything, so an OFF arm leaves them at these values for ever.
        self.kb_fast_sites = 0        # live build sites this body last owed --
                                      # the walk budget's multiplier (PIECE 2)
        self.kb_fast_budget = 0       # ... and the budget that came out of it
        self.kb_fast_cell_cost = 0    # ⭐ PIECE 3, COUNT 1: barriers the chosen
                                      # site's cheapest reachable chamber needs
                                      # (2 = the map corner this piece is for)
        self.kb_fast_axis_loss = 0    # ⭐ PIECE 3, COUNT 2: perpendicular offset
                                      # GIVEN UP for it, against the site arm 2's
                                      # key would have taken (0 = no trade bound)
        self.kb_fast_alt_cost = 0     # ... and what that arm-2 site would have
                                      # reached, so the trade has both sides
        self.kb_fast_site_moved = 0   # 1 if the two keys named different tiles
        self.kb_fast_yield = 0        # rounds this body yielded the seat walk to
                                      # a nearer friendly body (PIECE 1)
        self.kb_fast_buys = 0         # launcher buys made from the BUYER's rung
        self.kb_fast_steps = 0        # steps the BUYER's rung spent walking
        self.kb_fast_spawned = 0      # ⭐ PIECE 5 (CORE ONLY): extra opening
                                      # builders this core has spawned
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
        # ⭐ v619 PLANK 1 (SK_NEST_N3): the THIRD band sentinel, same tuple
        # shape.  It stays None for the whole game when the flag is off -- no
        # code path assigns it -- so `_nest_live()` reduces to v618's
        # two-term expression and the flag off is an exact identity.
        self.nest_turret3 = None
        # ⭐⭐ v632 HEIMDALL PLANKS 8+9 (SK_ROTATE): the FOURTH band sentinel,
        # same tuple shape.  The rotation battery is SK_ROTATE_WANT = 4 tubes
        # and `_nest_slots()` must be as wide as the target or the floor can
        # never be met -- see the note there.  It stays None for the whole game
        # on every SK_ROTATE-off arm (no path assigns it, because
        # `_nest_slots()` is then at most three long), so every count,
        # promotion and compaction reduces to v619's on v619's inputs.
        self.nest_turret4 = None
        self.nest_site2 = None        # the standing first site, while siting #2
        # ⭐⭐ v617 ITEM 1 (SK_TEAM_TUBES) -- FORWARD-TUBE SELF-HEARTBEAT state,
        # and it lives on the TURRET's own module namespace, not the engineer's.
        # That is the fix in one line: the fact "two tubes stand" stops being a
        # builder's memory of what it built and becomes each tube's own report
        # that it is still running.
        self.tube_fwd = None          # None = undecided, True/False = latched
        self.tube_seat = None         # 0 or 1, claimed once off slot 7
        self.nest_deaths = {}         # V4: (x,y) -> round it killed a turret
        self.nest_lives = []
        # ⭐⭐ s57 BARRELS ARM 2 (SK_BARREL_GUARD) -- PER-BODY STATE.  Every unit
        # gets its own `Player`, so all of this is per body and none of it is a
        # team fact; the two team facts the arm reads (tubes standing, home
        # bodies alive) are existing STORE reads, not fields.
        # GAME CONTEXT: in-engine bookkeeping for our own pieces in the Florent
        # Code League, a sandboxed bot-vs-bot competition.
        self.bg_out = False           # the medic body is re-tasked forward
        self.bg_out_n = 0             # re-task EPISODES (rising edges)
        self.bg_out_rnd = -1
        self.bg_rounds = 0            # rounds spent under the re-task
        self.bg_walk = 0
        self.bg_seen = 0              # rounds a damaged forward tube was seen
        self.bg_heal_rounds = 0       # rounds standing orthogonally beside one
        self.bg_heals = 0             # heals actually delivered
        self.bg_poor = 0              # heal refused by the bank floor
        self.bg_idle = 0
        self.bg_clear = 0             # idle rounds already out of the way
        self.bg_yield = 0             # idle rounds that stepped aside
        self.bg_recall_rounds = 0     # rounds under the release path
        self.bg_recall_steps = 0
        self.bg_home_n = 0            # releases that reached home
        # the security read's three terms, BOTH TAILS, per term
        self.bg_sec_yes = 0
        self.bg_sec_no_fire = 0
        self.bg_sec_no_turret = 0
        self.bg_sec_no_body = 0
        self.bg_no_tube = 0           # claim refused: no forward tube stands
        # (b) succession
        self.bg_succ_rounds = 0
        self.bg_succ_low = 0          # refused: fewer than SK_BG_SUCC_LIVE
        self.bg_succ_rearm = 0
        self.bg_succ_site = 0
        self.bg_succ_nosite = 0
        self.bg_succ_prep = 0
        self.bg_succ_hold = 0
        self.bg_succ_walk = 0
        # (c) the site guard
        self.bg_site_on = 0           # picks the guard applied to
        self.bg_site_off = 0          # ... and picks it declined (the opening)
        self.bg_cover_n = 0           # tiles in the covered set, summed
        self.bg_cover_guns = 0        # opposing turrets consulted, summed
        self.bg_site_covered = 0      # chosen sites that ARE covered anyway
        self.bg_site_clear = 0        # ... and chosen sites that are not
        self.bg_confirm_ok = 0        # can_fire_from agreed with the pattern
        self.bg_confirm_bad = 0       # ... and disagreed
        self.bg_ban = {}              # (x,y) -> round the bounded ban expires
        self.bg_ban_n = 0             # ban EVENTS (a knockout with a bearer)
        self.bg_ban_tiles = 0         # tiles banned, summed over events
        self.bg_site_relax = 0        # picks that had to drop the ban
        # (3) the facing instrument -- no logic, both arms
        self.bg_face = {}             # (x,y) -> True if the face is cardinal
        self.bg_plant_card = 0
        self.bg_plant_diag = 0
        self.bg_life_card = 0
        self.bg_life_card_n = 0
        self.bg_life_diag = 0
        self.bg_life_diag_n = 0
        # v626 PLANK A state: clear-clock is a cross-round position cache
        # (build rule 5 -> also on _clear_plans); cleared-once memory is about
        # the ENEMY's re-lay at a fixed tile and persists like nest_deaths.
        self.nest_clear_tile = None
        self.nest_clear_since = -1
        self.nest_cleared_once = set()
        self.nest_clears = 0          # instrument
        self.nest_clears_own = 0      # instrument
        self.nest_pb_life = 0         # instrument (PLANK B fires)
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
        # ⭐ v632 PLANK 7 (SK_APRON_MESH).  UNCONDITIONAL, like every other attr
        # in this file: a flag gates BEHAVIOUR, never the existence of state --
        # otherwise the flag-off tree carries a latent AttributeError one edit
        # away.  `mesh_tiles` is read by `_belt_evict` on every occupied planned
        # tile whether the plank is on or off, so an empty set here IS the
        # off-identity.
        self.mesh_tiles = set()       # the seats THIS body added to belt_plan
        self.mesh_planned = 0         # instrument: mesh tiles ever planned
        self.mesh_spawn_refused = 0   # instrument: refused by the spawn reserve
        # PLANK 2 (SK_TUBE_FLOOR) instruments.
        self.tube_noprep = 0          # turns the prep barriers were skipped
        self.tube_fund_waived = 0     # 1 once the ammo surcharge was waived
        self.tube_gap_relax = 0       # sites found ONLY at the relaxed spread
        # v622 (SK_GAP_RELAX_SOLO / SK_NEST_EXHAUST_PB) instruments.
        self.nest_exhaust_pb = 0      # sites found ONLY by the point-blank retry
        # ⭐⭐ s57 THE BATTERY, ARM 1 (SK_BATTERY_WANT) instruments.  All four
        # stay 0 for the whole game on every SK_BATTERY_WANT-off arm (the only
        # writer family is `_battery_open` / `_battery_rearm`, reached only
        # under `if SK_BATTERY_WANT:` at the one gate), which is what makes
        # them the OFF-identity witness as well as the arm's dose meter.
        # ⛔ THE REFUSAL TAPS ARE THE POINT, NOT THE FIRE COUNT: a ceiling that
        # has never been seen to REFUSE has not been seen to limit anything, so
        # `batt_unfunded` (purse short of the bar) and `batt_ceiling` (book
        # full at the ceiling) are the two verdicts an arm report must show
        # alongside `batt_open`.
        self.batt_open = 0            # engineer rounds the hold was skipped
        self.batt_unfunded = 0        # ... refused: purse below `_battery_bar`
        self.batt_ceiling = 0         # ... refused: ledger already at ceiling
        self.batt_rearm = 0           # spent sites freed for the next plant
        # ⭐⭐ s57 THE BATTERY, ARM 2 (SK_BATTERY2) state + instruments.
        # ⛔ INITIALISED UNCONDITIONALLY, like every other flag-gated block in
        # this file and for the same reason: an AttributeError escaping run()
        # destroys the unit permanently, so a flag-gated __init__ is how a
        # flag-gated attribute becomes a flag-gated death.  All of them stay at
        # these values for the whole game on every SK_BATTERY2-off arm (their
        # only writers sit under `if SK_BATTERY2 ...`), which makes them the
        # OFF-identity witness as well as the arm's dose meter.
        # (a) THE LEDGER FIX.
        self.batt2_seen = {}          # tid -> last round the HP was READ
        self.batt2_phantom = 0        # get_hp exceptions REFUSED as deaths
        self.batt2_expired = 0        # ... and refusals denied by the TTL
        self.batt2_live_lift = 0      # rounds the TEAM census beat this book
        # (b) THE BURST RULE.  ⛔ BOTH VERDICTS ARE TAPPED: a hold that has
        # never been seen to RELEASE and an escape that has never been seen to
        # FIRE have not been seen to do anything.
        self.batt2_hold_since = None  # round the current funding hold began
        self.batt2_holds = 0          # funding holds begun
        self.batt2_hold_rounds = 0    # engineer-rounds spent holding
        self.batt2_burst_ready = 0    # rounds the PAIR bar was already clear
        self.batt2_burst_off = False  # the escape has fired (latched)
        self.batt2_escape = 0         # round+1 the escape fired; 0 = never
        # (c) THE ECO-READY LATCH.
        self.batt2_ring = []          # the last W POSITIVE purse deltas
        self.batt2_sum = 0            # their sum (kept incrementally)
        self.batt2_last_bank = None   # previous purse sample
        self.batt2_last_ammo = None   # previous ammunition sample (the
                                      # converted-titanium half of income)
        self.batt2_last_rnd = -1      # round of the previous sample
        self.batt2_eco_since = None   # round the latch FIRED (None = never)
        self.batt2_eco_block = 0      # opens refused: economy below the bar
        self.batt2_eco_cold = 0       # opens refused: fewer than WARM samples
        self.batt2_eco_miss_rnd = -1  # s57 HAMMER V2: the refusal taps' own
                                      # per-round de-duplicator.  Stays -1 on
                                      # every SK_HAMMER_PRIO-off arm (its only
                                      # writer is `_b2_eco_tick`, reachable
                                      # only under `not SK_HAMMER_PRIO or ...`)
        # ⭐⭐ s57 SK_HAMMER_PRIO -- THE SPEND-LADDER INVERSION: state +
        # instruments.  ⛔ INITIALISED UNCONDITIONALLY, like every other
        # flag-gated block in this file and for the same reason: an
        # AttributeError escaping run() destroys the unit permanently, so a
        # flag-gated __init__ is how a flag-gated attribute becomes a
        # flag-gated death.  All of them stay at these values for the whole
        # game on every SK_HAMMER_PRIO-off arm (their only writers sit under
        # `if SK_HAMMER_PRIO ...`), which makes them the OFF-identity witness
        # as well as the arm's dose meter.
        # ⛔ BOTH VERDICTS ARE TAPPED ON EVERY BRANCH.  A gate never seen to
        # REFUSE has not been seen to gate; a gate never seen to RELEASE has
        # not been seen to be bounded; a sticky that never covers a relapse is
        # decoration.  Hence the pairs: held/off, episodes/released,
        # latched/relapse, belt_ext/belt_rep.
        # V2 AMENDMENT (the unconditional readiness evaluation).  BOTH
        # VERDICTS: `eval` is rounds the question was ASKED (zero would mean
        # the new call site never runs) and `fire` is round+1 of the latch fire
        # taken AT THAT SITE (0 = never there).
        self.hammer_eco_eval = 0      # ENGINEER: rounds `_b2_eco_ready` was
                                      # asked unconditionally
        self.hammer_eco_fire = 0      # ... round+1 the latch fired HERE
        self.hammer_pub = 0           # ENGINEER: rounds b12 was published
        self.hammer_latched = False   # READER: the wire has been seen set
        self.hammer_lag = -1          # ... the round it was FIRST seen
        self.hammer_relapse = 0       # ... rounds the wire read 0 after that
        self.hammer_cold = 0          # ... reads refused: latch not yet fired
        self.hammer_held = 0          # RUNG-refusals (an UPPER BOUND, not a
                                      # dose -- `_fund_refuse`'s own caveat)
        self.hammer_rounds = 0        # DISTINCT rounds with a refusal
        self.hammer_last_rnd = -1     # ... its de-duplicating clock
        self.hammer_first = -1        # round of the FIRST deferral (the
                                      # seen-choosing column: never in the
                                      # opening)
        self.hammer_off = 0           # rungs released: the pair stands
        self.hammer_episodes = 0      # deferral episodes begun (re-arms on
                                      # pair loss)
        self.hammer_released = 0      # episodes ENDED by the pair standing
        self.hammer_deferring = False # the current episode's state
        self.hammer_site = {}         # site -> refusals, so the readout can say
                                      # WHICH spend was deferred
        self.hammer_belt_ext = 0      # belt tiles skipped as EXTENSION
        self.hammer_belt_rep = 0      # belt tiles passed as REPAIR
        self.hammer_term_leak = 0     # LEAK 1: the SK_TERM_FIRST rung took the
                                      # turn while the inversion was armed
        self.hammer_seat_leak = 0     # LEAK 2: `_seat_claim_action` did
        # ⭐⭐ V2.1 AMENDMENT -- THE BOUNDED ESCAPE (SK_HAMMER_HOLD).  Same
        # unconditional-init rule as the block above and the same both-verdict
        # discipline: a bound never seen to FIRE is not a bound, and a bound
        # never seen to RE-ARM is a match-long disarm wearing an episode's
        # name.  All of these stay at these values on every OFF arm (their
        # only writers are `_hammer_watch` / `_hammer_escape` / the sticky
        # branch of `_hammer_armed`, all unreachable under `not
        # SK_HAMMER_PRIO`), so they are OFF-identity witnesses too.
        self.hammer_esc = False       # the escape has RELEASED this episode
        self.hammer_esc_fired = 0     # ... how many times it fired (episodes
                                      # ended by the BOUND rather than by the
                                      # pair standing)
        self.hammer_esc_rnd = 0       # ... round of the LAST firing, +1, so 0
                                      # means NEVER
        self.hammer_esc_pass = 0      # ... rungs allowed BECAUSE of it (the
                                      # dose the bound gives back)
        self.hammer_esc_rearm = 0     # RE-ARM EDGES seen: a tube loss or a
                                      # latch-relapse ENTRY.  An upper bound on
                                      # re-arms that mattered (`push_res_rearm`
                                      # has the same shape and caveat).
        self.hammer_live = -1         # last observed STANDING TUBE COUNT (0-2);
                                      # -1 so the very first watch cannot read
                                      # as a fall
        self.hammer_wire_cold = False # the published latch bit read 0 on the
                                      # last sticky check (the relapse EDGE's
                                      # own state)
        self.hammer_relapse_in = 0    # relapse ENTRIES -- distinct from
                                      # `hammer_relapse`, which is relapse
                                      # ROUNDS.  The re-arm runs on entries.
        self.hammer_relapse_seen = 0  # ... the watch's own high-water mark
        self.hammer_holds = 0         # hold RUNS started (the clock's episodes)
        self.hammer_hold_since = None # round the current run started
        self.hammer_hold_last = -1    # ... last round counted, so several rungs
                                      # in one round tick the run once
        self.hammer_hold_rounds = 0   # ROUNDS spent inside a run, once per round
        # PLANK 3 (SK_PECK_FOCUS) instruments.
        self.peck_relaxed = 0         # pecks that skipped the V7 veto
        self.keeper_marches = 0       # keeper turns spent marching at a shooter
        self.keeper_holds = 0         # keeper turns spent HOLDING a peck seat
        # PLANK 4 (SK_PLUCK_AWARE) instruments.
        self.pluck_detours = 0        # marches routed to a launcher-safe seat
        self.pluck_retargets = 0      # distinct launchers marched at instead
        self.pluck_last = None
        # --- v619 THE KILL SIDE: state + instruments ------------------------
        # PLANK 3 (SK_TUBE_RELIGHT).
        self.relight_since = None     # round the count last fell below target
        self.relight_n = 0            # relights begun
        self.relight_rounds = 0       # engineer-rounds spent below target
        self.relight_prep_credit = 0  # prep turns saved by reusing standing cover
        self.relight_phantom = 0      # get_hp exceptions REFUSED as deaths (a)
        # PLANK 5 (SK_RENT).
        self.rent_belt = 0            # orphaned belt tiles swept
        self.rent_prep = 0            # abandoned prep barriers swept
        self.rent_offplan = {}        # (x,y) -> round first seen off-plan
        self.rent_prebuy = 0          # sweeps that ran in a pre-purchase round

        # --- v620: THE TWO SUCCESSOR ITEMS ---------------------------------
        # ⛔ EVERY ONE OF THESE IS INITIALISED UNCONDITIONALLY, exactly as the
        # v619 block above is, and for the same reason: an AttributeError
        # escaping `run()` destroys the unit permanently, and a flag-gated
        # `__init__` is how a flag-gated attribute becomes a flag-gated death.
        # PLANK 1 (SK_TUBE_FLOOR2) -- the pre-prepped NEXT site.
        self.preprep_site = None      # Position of the site being pre-prepped
        self.preprep_n = 0            # barriers laid on it so far
        self.preprep_done = 0         # sites fully pre-prepped this game
        self.preprep_used = 0         # times a pre-prep was consumed by a re-site
        self.floor_hold = 0           # engineer-rounds held AT the floor
        # PLANK 2 (SK_RENT_EARLY).
        self.rent_turn_rnd = -1       # round the per-TURN destroy budget belongs to
        self.rent_turn_n = 0          # destroys already spent this turn
        self.rent_resite = 0          # sweeps taken at re-site time (a)
        self.rent_early_age = 0       # orphans admitted by the relaxed clock (b)
        self.rent_steps = 0           # 1-step detours taken (c)

        # --- v618 THE SEAT-DEFENCE PACKAGE ---------------------------------
        # PER-BODY STATE throughout, for the reason every memo in this tree is
        # per-body: the store has no free slot (v608 took the last one) and
        # every one of these quantities is either a pure function of the core
        # anchor (the seats) or a bound this body owns (its own claims, its own
        # heals).  A replacement keeper re-derives the seat set exactly and
        # re-learns occupancy from its own vision inside a few rounds.
        # PLANK 1 (SK_SEAT_CLAIM).
        self.seat_claims = 0          # claims this body has laid (<= MAX)
        self.seat_claimed = {}        # (x,y) -> round we laid ours there
        self.seat_claim_refused = 0   # instrument: claims the spawn reserve
                                      # refused (the guard's own firing count)
        # PLANK 2 (SK_HOME_GUNNER).
        self.home_guns = 0            # home gunners bought (<= SK_HOME_GUN_MAX)
        self.home_gun_walks = 0       # instrument: keeper rounds spent walking
                                      # to the site -- the plank's only
                                      # RECURRING cost, counted like the
                                      # launcher arm's was
        self.home_gun_site = None     # Position, memoised per round
        self.home_gun_rnd = -1
        self.rotations = 0            # PER TURRET: rotations this gun has spent
        # PLANK 3 (SK_GUN_ROUTEBLOCK) instruments.
        self.rb_shots = 0             # shots this turret put into a collar
                                      # barrier (the AMMO COLUMN's numerator)
        # PLANK 4 (SK_SEAT_HEAL).
        self.seat_heals = 0           # heals landed on a claimed seat
        self.seat_heal_veto = set()   # tiles PLANK 4 refused THIS ROUND, so the
                                      # generic `_heal_action` below it cannot
                                      # walk into the race the guard just
                                      # refused.  Cleared every keeper turn.
        self.seat_heal_veto_rnd = -1
        self.seat_heal_refused = 0    # instrument: the guard's firing count
        # THE RIDER (SK_PECK_DEMOTE).
        self.peck_demoted = 0         # pecks refused because a gun bears

        # --- v632 HEIMDALL PLANK 1: THE CITADEL DISPATCH -------------------
        # ⛔ UNCONDITIONAL, exactly as the v619/v620 blocks above are and for
        # the same reason: an AttributeError escaping `run()` makes the engine
        # PERMANENTLY delete this unit, so a flag-gated `__init__` is how a
        # flag-gated attribute becomes a flag-gated death.  `SK_CITADEL` is
        # False in the shipped config and these four still initialise.
        # PER-BODY, like every other memo in this tree: the store has no free
        # slot (v608 took the last one) and the citadel writes NO slot at all --
        # it is a READER of slot 2, whose one writer is still the CORE.
        self.citadel_tgt = None       # (x,y) of the intruder tile this body has
                                      # latched, or None when disengaged
        self.citadel_since = -1       # round the latch above was taken (the
                                      # SK_CITADEL_GIVEUP clock)
        self.citadel_blocks = 0       # instrument: turns spent HOLDING ground
                                      # beside an enemy body (the body-block,
                                      # which must be measured and never assumed)
        self.citadel_walks = 0        # instrument: turns spent closing on one

        # --- v632 HEIMDALL PLANK 3 -- THE TURRET RING (SK_FORT_RING) --------
        # ⛔ UNCONDITIONAL, like every other attribute in this __init__: a
        # field created only under a flag is how an OFF arm raises
        # AttributeError inside `run()` and the engine PERMANENTLY DESTROYS
        # the unit.  With SK_FORT_RING False these are allocated and never
        # read -- the identity is carried by the CALL-SITE conjunction.
        self.fort_sents = 0           # axis sentinels bought (<= SK_FORT_RING_SENT)
        self.fort_guns = 0            # flank gunners bought (<= ..._GUNNERS)
        self.fort_ring_bought = 0     # instrument: ring turrets, all kinds
        self.fort_flank = 0           # sign of the first flank gunner's cross
                                      # about the core-to-core axis; 0 until one
                                      # stands, which is what makes the flank
                                      # term inert for the FIRST gunner
        self.fort_ring_site = None    # Position, memoised per round (walk half)
        self.fort_ring_rnd = -1
        self.fort_ring_walks = 0      # instrument: keeper rounds spent walking
                                      # to a ring site -- the plank's only
                                      # RECURRING cost, counted the way the
                                      # launcher and home-gun arms counted
                                      # theirs
        self._fort_lane_cache = None  # the lane tile list, cached on the core
        self._fort_lane_key = None    # and enemy anchors (both fixed for the
                                      # match)
        self.fort_ammo_banked = 0     # CORE instrument: titanium converted by
                                      # the early ammo clock (`_fort_ammo_bank`)

        # --- v632 HEIMDALL PLANK 5 -- THE SECOND ECO BODY (SK_FORT_WALKER_ECO)
        # ⛔ UNCONDITIONAL, like every other attribute in this __init__ and for
        # the same engine reason: a field created only under a flag is how an
        # OFF arm raises AttributeError inside `run()`, and the engine then
        # PERMANENTLY DESTROYS the unit for the rest of the match.  With
        # SK_FORT_WALKER_ECO False this counter is allocated and stays 0 --
        # the three publisher gates it counts are unreachable by any body but
        # role 0 today, which is exactly why it is the identity witness.
        # ⭐ IT IS THE PLANK'S OWN R5 INSTRUMENT, NOT DECORATION.  The study's
        # named failure is SILENT: a lost buffered write leaves no trace in the
        # store and no exception anywhere.  This counter is the gate's refusal
        # tap -- 0 on every OFF arm, and strictly > 0 on an ON arm the moment
        # the second body reaches a publisher rung.  A gate that has never been
        # seen to refuse has not been seen to work.
        self.eco_pub_blocked = 0      # publisher rungs (slots 4/5/14) refused
                                      # because this body is not the HOME KEEPER

        # --- v632 HEIMDALL PLANKS 8+9 -- THE r300 ROTATION (SK_ROTATE) -------
        # GAME CONTEXT: in-engine state for the Florent Code League's simulated
        # grid -- which builder-bot turn this piece runs after round 300.
        # ⛔ UNCONDITIONAL, like every other attribute in this __init__ and for
        # the same engine reason: a field created only under a flag is how an
        # OFF arm raises AttributeError inside `run()`, and the engine then
        # PERMANENTLY DESTROYS the unit for the rest of the match.  With
        # SK_ROTATE False every one of these is allocated, `rot_on`/`rot_body`
        # are re-set to False on every builder round, and the four counters
        # stay 0 -- which is exactly what makes them the identity witnesses.
        self.rot_on = False           # the phase is open (rnd >= SK_PHASE_ROUND)
        self.rot_body = False         # ...and THIS body is one of the raiders
        self.rot_stage = False        # THE COMMUTE: a raider inside
                                      # [SK_ROTATE_PRESTAGE, SK_PHASE_ROUND).
                                      # Mutually exclusive with `rot_body`
        self.rot_staged = False       # the one-shot re-home latch: the phase-1
                                      # nest site is dropped on the FIRST
                                      # prestage round so the re-pick runs under
                                      # the role-parity half split
        self.rot_stage_walks = 0      # commute rounds spent by this body -- the
                                      # redesign's cost instrument, and the
                                      # denominator for its arrival gain
        self.chest_blocked = 0        # THE WAR CHEST's refusal tap
                                      # (SK_ROTATE_CHEST_FROM): discretionary
                                      # keeper purchases stood down in
                                      # [250, 300) so the battery is affordable
                                      # at the flip.  0 on every SK_ROTATE-off
                                      # arm -- the window predicate's first
                                      # term is the master -- which is what
                                      # makes it the identity witness as well
                                      # as the dose counter
        self.rot_plants = 0           # sentinels planted by this body since the
                                      # flip.  Drives the first battery's
                                      # clustering AND is the plant-rate
                                      # instrument (§8b's binding constraint)
        self.rot_pub_blocked = 0      # HAZARD (a)'s refusal tap: publisher rungs
                                      # (slots 7/8/12) refused because this body
                                      # is not the ORIGINAL siege engineer.  The
                                      # failure it prevents is SILENT -- a lost
                                      # buffered write leaves no trace and no
                                      # exception -- so a gate never seen to
                                      # refuse has not been seen to work.  0 on
                                      # every OFF arm, > 0 the moment the second
                                      # raider reaches a publisher rung.
        # --- v632 HEIMDALL -- THE FUNDING PRIORITY (SK_ROTATE_FUND) --------
        # ⛔ UNCONDITIONAL, for the reason the rotation block above states: a
        # field created only under a flag is how an OFF arm raises
        # AttributeError inside `run()`, and the engine then PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Both stay 0 on every
        # SK_ROTATE-off and SK_ROTATE_FUND-off arm, which is what makes them
        # the identity witnesses as well as the dose instruments.
        self.fund_drip_held = 0       # CORE tap: rounds the ammo drip's
                                      # conversion was CLAMPED by the sentinel
                                      # floor (`_fund_floor`).  Counts only
                                      # rounds where the clamp actually bit --
                                      # the drip had money it would otherwise
                                      # have converted.
        self.fund_verb_held = 0       # KEEPER tap: rounds the discretionary
                                      # peck/heal rungs were refused.  ⚠ An
                                      # UPPER BOUND on turns diverted, not a
                                      # dose -- the refusal is evaluated before
                                      # the verb looks for a target, so a round
                                      # with nothing to peck still counts.  See
                                      # `_fund_refuse`.
        self.rot_preps_skipped = 0    # prep barriers NOT built post-flip (the
                                      # r374 -> r336 demo finding)
        self.rot_pecks_skipped = 0    # `_attack_enemy_core` entries suppressed
                                      # post-flip ("no pecking, we only watch
                                      # our sentinels work")
        # --- v632 HEIMDALL PLANK 10 -- BATTERY SURVIVAL (SK_ROTATE_GUARD) ---
        # ⛔ UNCONDITIONAL, for the reason every other attr in this file is: a
        # flag gates BEHAVIOUR, never the EXISTENCE of state.  A field created
        # only under a flag is how a flag-off arm raises AttributeError inside
        # `run()` -- and the engine then PERMANENTLY DESTROYS that unit for the
        # rest of the match.  Both stay 0 on every SK_ROTATE-off and every
        # SK_ROTATE_GUARD-off arm, which is what makes them the OFF-IDENTITY
        # WITNESSES as well as the dose instruments.
        self.guard_heals = 0          # rung (b) DOSE: heals actually landed on
                                      # a damaged neighbour (tube or screen)
                                      # while inside the band.  ⚠ A dose, not
                                      # an effect -- the survival read is tube
                                      # life and battery concurrency; this only
                                      # says the verb fired.  v630.1 exists
                                      # because the v630.0 form read 1 in 60
                                      # games, so a near-zero here is the
                                      # FALSIFIER for the placement, not a null
                                      # for the plank.
        self.guard_seats = 0          # rungs (a)+(c) OCCUPANCY: body-rounds
                                      # spent STANDING on a front seat (the
                                      # screen, and the tile the heal reaches
                                      # from).  Counts stands, not arrivals --
                                      # a walk toward the seat is not yet a
                                      # screen.

        # --- s57 THE PUSH (SK_PUSH, default OFF) ---------------------------
        # ⛔ UNCONDITIONAL FIELDS, for the engine reason every block in this
        # file states: a flag gates BEHAVIOUR, never the EXISTENCE of state.  A
        # field created only under a flag is how a flag-OFF arm raises
        # AttributeError inside `run()`, and the engine then PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Every counter below
        # reads 0 (or its null sentinel) on every OFF arm, which makes each of
        # them an OFF-IDENTITY WITNESS as well as an instrument.
        # ⛔ PER-BODY STATE, and the engine forces it: every unit gets its OWN
        # `Player` instance (kbprobe surprise 1), so the WARDEN's build
        # counters, the LAUNCHER's throw counters and the ENGINEER's succession
        # counters live on three different objects and are never summed in-bot.
        # --- PIECE 1, the pair reserve -------------------------------------
        self.push_res_held = 0        # rounds a gated rung was REFUSED.  ⚠ AN
                                      # UPPER BOUND ON TURNS DIVERTED, not a
                                      # dose: the refusal is evaluated before
                                      # the verb looks for a target, so a round
                                      # with nothing to build still counts
                                      # (`_fund_refuse`'s own caveat, verbatim).
        self.push_res_pass = 0        # ... and rounds it was ALLOWED with the
                                      # reserve armed.  The pair is the
                                      # instrument: a gate that has only ever
                                      # returned one verdict has not been seen
                                      # to gate.
        self.push_res_off = 0         # rounds the reserve was RELEASED because
                                      # the pair stands (the other tail).
        self.push_res_site = {}       # gated rung name -> refusals, so "which
                                      # spend did the reserve actually stop" is
                                      # a measured answer per site rather than
                                      # a pooled number.
        self.push_res_bar = 0         # the last bar computed, for the trace.
        # --- PIECE 1, V2 AMENDMENT (b): the bounded escape + the half-bar ---
        # ⛔ UNCONDITIONAL, for the engine reason the block above states.  All
        # seven read 0 / False / -1 on every OFF arm, so they are OFF-IDENTITY
        # WITNESSES as well as instruments.
        self.push_res_live = -1       # last observed STANDING TUBE COUNT (0-2).
                                      # -1 is "never looked", so the first look
                                      # can never read as a tube DEATH.
        self.push_res_esc = False     # the bounded escape has RELEASED the
                                      # reserve for THIS EPISODE
        self.push_res_esc_n = 0       # ... how many times it fired (an escape
                                      # never seen to fire has not been seen to
                                      # protect anything -- `batt2_escape`'s own
                                      # rule)
        self.push_res_esc_rnd = 0     # ... round of the LAST firing, +1, so 0
                                      # means NEVER (`batt2_escape`'s encoding)
        self.push_res_esc_pass = 0    # ... and rounds a buy was allowed BECAUSE
                                      # of it -- the escape's own dose, kept
                                      # apart from `push_res_off` so the two
                                      # release tails can be told apart
        self.push_res_rearm = 0       # times a tube DEATH re-armed the reserve
        self.push_res_holds = 0       # hold RUNS started (the clock's episodes)
        self.push_res_hold_since = None  # round the current run started
        self.push_res_hold_last = -1  # ... last round counted, so the several
                                      # calls a round cannot inflate the clock
        self.push_res_hold_rounds = 0 # ROUNDS spent inside a run, once per round
        self.push_res_ready = 0       # rounds the purse ALREADY cleared the bar
                                      # (the clock's other verdict)
        # --- PIECE 2, the warden -------------------------------------------
        self._push_cands = None       # memo: the pure-geometry site list
        self.push_done_seen = False   # a friendly launcher already stands in
                                      # the enemy band (the team-wide bound,
                                      # read off vision because the store has
                                      # no free slot -- v611's own measured
                                      # second-launcher defect)
        self.push_scan0 = False       # the launcher's first building scan is
                                      # done (before it, every building looks
                                      # NEW and the activity sensor would call
                                      # the whole board active)
        self.push_site = None         # Position: the chosen launcher tile
        self.push_site_rnd = -1       # round it was chosen
        self.push_site_seats = 0      # heal seats its pickup disc covers
        self.push_banned = set()      # sites the give-up bound retired
        self.push_tries = 0           # rounds spent on the CURRENT site
        self.push_gaveup = False      # the PLANT half is done (the heal half
                                      # is not -- they give up separately)
        self.push_built = 0           # launchers this body bought (<= 1)
        self.push_built_rnd = -1      # instrument: round the launcher landed
        self.push_walk_rounds = 0     # instrument: warden rounds spent walking
        self.push_heals = 0           # DOSE: barrel heals actually landed
        self.push_heal_rounds = 0     # rounds the warden STOOD on a barrel seat
        self.push_station_walk = 0    # rounds spent walking BACK to the battery
                                      # with nothing damaged in sight (the
                                      # stationing half of PIECE 2c)
        self.push_barrel_seen = 0     # rounds a damaged forward barrel was in
                                      # this body's vision (the heal's own
                                      # opportunity denominator)
        # --- PIECE 2b (V3), the warden as an ADDITIONAL body ---------------
        # ⛔ UNCONDITIONAL, for the engine reason this block states: a flag
        # gates BEHAVIOUR, never the EXISTENCE of state.  All ten read 0 /
        # False / -1 on every OFF arm, which makes each of them an
        # OFF-IDENTITY WITNESS as well as an instrument.
        self.push_w2 = False          # THIS BODY is the dedicated warden (set
                                      # in `_claim_role`, once, for life)
        self.push_w2_born = -1        # ... and the round it claimed that seat
        self.push_w2_arrive = -1      # round it first stood INSIDE THE BAND
                                      # (SK_TUBE_BAND_DSQ of their core) -- the
                                      # commute's own column
        self.push_w2_rounds = 0       # rounds it ran its own turn
        self.push_w2_fall = 0         # ... of which the PLANT half produced
                                      # nothing and fell through to the medic
        self.push_w2_idle = 0         # ... and of which it reached the idle
                                      # rung (on station, nothing damaged)
        self.push_w2_clear = 0        # ... idle rounds it was ALREADY out of
                                      # the engineer's build menu
        self.push_w2_yield = 0        # ... and idle rounds it STEPPED OFF it.
                                      # ⛔ BOTH TAILS, because a yield rule
                                      # never seen to refuse is not a rule.
        self.push_stn_i = 0           # THE BAND PATROL's current stop (0 = the
                                      # toward-our-core station v1 shipped)
        self.push_stn_dwell = 0       # ... rounds spent AT that stop with no
                                      # barrel in vision (travel never ticks)
        self.push_stn_moves = 0       # ... and stop changes actually made --
                                      # the patrol's own dose column
        # --- PIECE 2b (V3), THE CORE's own half ----------------------------
        self.push_w2_spawned = 0      # ⭐ CORE ONLY: dedicated warden bodies
                                      # this core has spawned (bounded by
                                      # SK_PUSH_W2_N -- the `live` census
                                      # cannot bound it, see the rung)
        self.push_w2_rnd = -1         # ... and the round of that spawn
        self.push_w2_arm = 0          # CORE: rounds the push-time trigger held
        self.push_w2_poor = 0         # ... of which the bank floor refused.
                                      # BOTH TAILS of the affordability read.
        # --- PIECE 2, the launcher unit's own turn -------------------------
        self.push_opp = 0             # rounds with ANY opposing builder inside
                                      # the pickup disc (the throw denominator)
        self.push_opp_active = 0      # ... of which the sleeping-dogs rule
                                      # called ACTIVE
        self.push_sleep = 0           # ... and of which it left ALONE.  ⛔ BOTH
                                      # TAILS ARE COUNTED because the rule is
                                      # only a rule if it has been seen to
                                      # refuse.
        self.push_throws = 0          # throws executed
        self.push_throw_border = 0    # ... of which landed on a MAP BORDER tile
        self.push_throw_d2 = 0        # ... summed throw d^2, for the median's
                                      # cross-check (the trace carries each)
        self.push_active = {}         # opposing builder id -> round last seen
                                      # WORKING (the sleeping-dogs memo)
        self.push_core_hp = -1        # their core's HP as of last round, the
                                      # HEAL detector's own baseline
        self.push_seen_b = set()      # opposing building ids already seen, so a
                                      # NEW one names a builder that just built
        # --- PIECE 3, the engineer forward ---------------------------------
        self.push_quiet_yes = 0       # rounds the post-security gate PASSED
        self.push_quiet_no = 0        # ... and rounds it REFUSED (both tails)
        self.push_succ_rearm = 0      # spent sites freed for succession
        self.push_succ_site = 0       # succession sites actually picked
        self.push_succ_walk = 0       # succession rounds spent walking
        self.push_succ_hold = 0       # succession rounds spent standing at the
                                      # prepared site (the overlap itself)
        self.push_succ_prep = 0       # prep barriers laid ahead of the need

        # --- v632 SURVIVAL FAMILY, PLANK A -- WALK-TERMINAL GUARDS ----------
        # (SK_WALK_GUARDS; audit `docs/research/AUDIT-walk-terminals-
        # 2026-08-22.md`, the three EXPOSED sites.)
        # ⛔ UNCONDITIONAL, like every other attribute in this file and for the
        # engine reason the block above states: a flag gates BEHAVIOUR, never
        # the EXISTENCE of state.  A field created only under a flag is how a
        # flag-OFF arm raises AttributeError inside `run()`, and the engine then
        # PERMANENTLY DESTROYS that unit for the rest of the match.  All six
        # stay 0 on every SK_WALK_GUARDS-off arm, which is what makes them the
        # OFF-IDENTITY WITNESSES as well as the dose instruments.
        # ⭐ THE PAIRING IS THE INSTRUMENT, NOT EITHER HALF.  `wg_state_*`
        # counts rounds the DEADLOCK STATE occurred (this body standing on its
        # own walk target); `wg_fire_*` counts rounds a step ACTUALLY EXECUTED
        # out of it.  state == 0 means the guarded terminal never arose in that
        # cell -- an honest conditional vacuum, reported as such, not a
        # success; state > 0 with fire == 0 means the escape was reached and
        # could not move, which is the boxed-body case and a real refusal.
        self.wg_state_deny = 0        # `_ore_denier` -> `_deny_target` (row 24)
        self.wg_fire_deny = 0
        self.wg_state_esc = 0         # `_escalate_target` branch 2 (row 6b)
        self.wg_fire_esc = 0
        self.wg_state_def = 0         # `_home_defence` slot-2 walk (row 30)
        self.wg_fire_def = 0
        # ⭐⭐ 4.2 -- THE PER-(SITE, TILE) BAN STATE.  `(site, x, y) -> round the
        # ban ends`, mirroring `escape_ban` one block up (tile -> round, read as
        # `.get(key, -1) > rnd`).  UNCONDITIONAL for the same engine reason as
        # every counter above: only `_walk_escape` writes it and `_walk_escape`
        # is reachable only under SK_WALK_GUARDS, so it stays EMPTY on every
        # flag-off arm -- and every reader is written `if self.wg_ban and ...`,
        # so an OFF arm pays one truthiness test and never a dict lookup inside
        # the ore patrol loop.
        self.wg_ban = {}

        # --- v632 SURVIVAL FAMILY -- THE NAV-STALL DETECTOR (SK_NAV_STALL) --
        # ⛔ UNCONDITIONAL, for the engine reason every block in this file
        # states: a flag gates BEHAVIOUR, never the EXISTENCE of state.  A field
        # created only under a flag is how a flag-OFF arm raises AttributeError
        # inside `run()`, and the engine then PERMANENTLY DESTROYS that unit for
        # the rest of the match.  Every counter here stays 0 and `ns_ban` stays
        # EMPTY on every SK_NAV_STALL-off arm -- only `_ns_tick`/`_ns_escape`
        # write them and both are reachable only under the flag -- which is what
        # makes them the OFF-IDENTITY WITNESSES as well as the dose instruments.
        self.ns_run = 0        # consecutive stall rounds RIGHT NOW (the counter
                               # the detector compares against SK_NAV_STALL_N)
        self.ns_stall = 0      # DOSE: total rounds this body was counted as
                               # stalled (alive, in a walk, no verb, no tile
                               # change, not arrived).  ⚠ An observation, not an
                               # effect -- the effect read is `ns_fires`.
        self.ns_fires = 0      # ESCAPES EXECUTED: rounds a forced cardinal step
                               # actually moved this body out of a stall.  Also
                               # the rotation offset of the escape's direction
                               # order, so repeated fires do not re-pick the
                               # same neighbour.
        self.ns_boxed = 0      # fires where NO legal step existed (the boxed
                               # body).  state>0 with fires==0 and boxed>0 is a
                               # real refusal, not a vacuum -- the WG pairing
                               # lesson, kept.
        self.ns_refused = 0    # `step_to` calls REFUSED because the requested
                               # target is under a live nav-stall ban.  This is
                               # the ban's own dose: a ban nobody reads is a
                               # counter that never moves.
        self.ns_walk = False   # per-ROUND scratch: this body asked the walk
                               # executor for a step this round
        self.ns_tgt = None     # per-ROUND scratch: the last target `step_to`
                               # was given this round (the ban's subject)
        self.ns_stepped = False  # per-ROUND scratch: one escape attempt per
                               # round, no more
        # tile -> round the ban ends.  Read as `.get((x, y), -1) > rnd`, the
        # verbatim read pattern of `escape_ban` and `wg_ban`.
        self.ns_ban = {}

        # --- v632 SURVIVAL FAMILY -- THE CHEW-CLOCK RE-KEY (SK_CHEW_REKEY) --
        # ⛔ UNCONDITIONAL, for the engine reason every block in this file
        # states: a flag gates BEHAVIOUR, never the EXISTENCE of state.  A field
        # created only under a flag is how a flag-OFF arm raises AttributeError
        # inside `run()`, and the engine then PERMANENTLY DESTROYS that unit for
        # the rest of the match.  `chew_clock` stays EMPTY and all three
        # counters stay 0 on every SK_CHEW_REKEY-off arm -- only `_chew_ok` and
        # `_chew_prune` write them and both are reachable only under the flag --
        # which makes them the OFF-IDENTITY WITNESSES as well as the dose
        # instruments.  Same (tile, occupant id) keying as `demo_pecks` and
        # `seat_pecks`, for the same measured reason.
        self.chew_clock = {}    # (x,y) -> (occupant bid, episode start, last
                                # touch).  Bounded by SK_CHEW_CLOCK_MAX (and by
                                # the map area by construction -- the key is the
                                # tile, the occupant re-keys in place).
        self.chew_rearms = 0    # DOSE: chew episodes ARMED (new tile, or a new
                                # occupant on a tile we already chewed).  The
                                # (b)-half of the defect and the (a)-half both
                                # land here.
        self.chew_declines = 0  # rounds the re-keyed clock declined -- the SAME
                                # occupant past SK_CAGE_MELEE_GIVEUP.  This is
                                # the give-up still doing its job.
        self.chew_pruned = 0    # entries dropped by the bound (expected 0).

        # --- v632 SURVIVAL FAMILY, PLANK B -- THE LEASHED KEEPER'S DUTY -----
        # (SK_LEASH_DUTY, conjoined with SK_KEEPER_LEASH at the call site.)
        # Same unconditional rule and the same reason.  All three stay 0 on
        # every SK_LEASH_DUTY-off arm AND on every SK_KEEPER_LEASH-off arm.
        self.duty_state = 0           # rounds the keeper was LEASHED and the
                                      # economy walk found NO in-range target
                                      # (the registered state column)
        self.duty_holds = 0           # of those, rounds it HELD a core-adjacent
                                      # seat (already in position)
        self.duty_steps = 0           # of those, rounds it STEPPED toward one

        # --- v632 SURVIVAL FAMILY -- WORK AT A HELD POST (SK_KEEPER_WORK) ---
        # Same unconditional rule and the same engine reason as the block above:
        # a flag gates BEHAVIOUR, never the EXISTENCE of state.  All six stay 0
        # on every SK_KEEPER_WORK-off arm -- `_keeper_work` is their only writer
        # and it is reachable only under the flag -- which makes them the
        # OFF-IDENTITY WITNESSES as well as the dose instruments.
        self.kw_holds = 0             # DENOMINATOR: rounds this body finished a
                                      # keeper turn alive with action cooldown 0,
                                      # no verb and no tile change (the held
                                      # post).  An observation, not an effect.
        self.kw_heals = 0             # EFFECT: work heals actually emitted
        self.kw_heals_core = 0        # of those, on a CORE footprint tile
        self.kw_partial = 0           # of those, a 1..3-missing (partial) heal
        self.kw_bots = 0              # of those, reached a friendly BUILDER BOT
                                      # that carries no building (the class
                                      # `_heal_action` structurally cannot heal)
        self.kw_held = 0              # work verbs stood down by the spend cap
                                      # (floor or SK_ROTATE_FUND) WITH a real
                                      # target already in hand -- a refusal of a
                                      # verb, not a blind tick

        # --- CORE ----------------------------------------------------------
        self.spawned = 0
        self.converts = 0

        # --- s57 LEVER 1 -- THE CONVERSION POLICY (SK_AMMO_PUSH) -----------
        # ⛔ UNCONDITIONAL, like every other attribute in this __init__ and for
        # the same engine reason: a field created only under a flag is how an
        # OFF arm raises AttributeError inside `run()`, after which the engine
        # PERMANENTLY DESTROYS that unit for the rest of the match.  Both stay
        # 0 on an OFF arm -- `_ammo_push` is unreachable behind the flag test
        # in `_core` -- which is what makes them the identity witness.
        self.push_converts = 0        # CORE instrument: rounds the push spent
                                      # the team's one conversion IN ADDITION
                                      # to what the drip would have converted
        self.push_ti = 0              # ... and the titanium it moved

        # --- s57 LEVER 2 -- THE HEAL-STAND (SK_CORE_STAND) -----------------
        self.stand_rounds = 0         # BUILDER instrument: rounds this body
                                      # found the stand ARMED (the reachability
                                      # witness for the gate lift; the heals
                                      # themselves land on `self.core_heals`,
                                      # which the pre-existing `_core_medic`
                                      # already counts)

        # --- s57 THE STAND, ARM 2 -- HEAL-SEAT CLEARING (SK_STAND_SEATS) ---
        # ⛔ UNCONDITIONAL, for the same engine reason as the block above: a
        # field created only under a flag is how an OFF arm raises
        # AttributeError inside `run()`, after which the engine PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Every one of these
        # stays at its initial value on an OFF arm -- `_stand_seat_sweep`
        # returns 0 on its first line -- which is what makes them the identity
        # witness rather than a behaviour change.
        self.stand_clears = 0         # BUILDER instrument: seats this body
                                      # opened (capped by SK_STAND_SEATS_MAX)
        self.stand_clear_cls = [0, 0, 0]   # ... by safety class: plain barrier
                                      # / apron-or-door barrier / spent belt
        self.stand_seat_refused = 0   # adjacent held seats the safety order
                                      # REFUSED -- the other verdict, counted
        self.stand_seat_free = 0      # sum of known-free seats over
        self.stand_seat_rounds = 0    # ... the rounds this body sampled them,
                                      # i.e. the census's 1.54/8, live
        self.stand_flow = {}          # (x,y) -> round a stack was last seen on
                                      # a seat belt piece

        # --- s57 THE STAND, ARM 4 -- THE ANSWER SENTINEL (SK_STAND_ANSWER) ---
        # ⛔ UNCONDITIONAL, for the same engine reason as the two blocks above:
        # a field created only under a flag is how an OFF arm raises
        # AttributeError inside `run()`, after which the engine PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Every one of these
        # stays at its initial value on an OFF arm -- `_stand_answer_action`
        # returns on its first line -- which is what makes them the identity
        # witness rather than a behaviour change.
        #
        # THE SEEN-CHOOSING COLUMNS, and they are laid out so both tails are
        # readable off one line: `stand_answer_eps` is how many siege episodes
        # this body saw the trigger armed for, `stand_answer_funded_eps` is how
        # many of those it could also AFFORD (the OPPORTUNITY denominator), and
        # `stand_answers` is how many it bought.  answers == 0 with funded_eps
        # high is the NEVER-FIRED falsifier; answers == funded_eps with the
        # refusal counters at 0 is the DEGENERATE-ALWAYS falsifier.
        self.stand_answers = 0        # sentinels this body actually built
        self.stand_answer_eps = 0     # distinct episodes seen armed
        self.stand_answer_funded_eps = 0   # ... of those, episodes with funds
        self.stand_answer_windows = 0      # armed ROUNDS (the dose, not the n)
        self.stand_answer_have = 0    # rounds refused: this episode is answered
        self.stand_answer_covered = 0 # rounds refused: one of OURS already bears
        self.stand_answer_unfunded = 0     # rounds refused on the funding bar
        self.stand_answer_noseat = 0  # armed+funded rounds with no covering
                                      # seat orthogonally adjacent to this body
        self.stand_answer_lane_refuse = 0  # seats refused for sitting in the
                                      # shooter's own lane onto our core -- the
                                      # OTHER verdict of the lane branch, which
                                      # is what makes that branch measurable
        self._sa_seen_ep = -1         # episode keys, per body (see the flag)
        self._sa_funded_ep = -1
        self._sa_done_ep = -1
        self._sa_face_key = None      # the shooter's lane-facing cache
        self._sa_faces = ()
        self.stand_watch = {}         # (x,y) -> round this body first watched
                                      # it; a tile we have not watched is not a
                                      # quiet tile
        # --- s57 THE STAND, ARM 5 -- THE SIEGE PECK SWARM (SK_STAND_SWARM) ---
        # ⛔ UNCONDITIONAL, for the same engine reason as every block above: a
        # field created only under a flag is how an OFF arm raises
        # AttributeError inside `run()`, after which the engine PERMANENTLY
        # DESTROYS that unit for the rest of the match.  Every one of these
        # stays at its initial value on an OFF arm -- `_stand_swarm_action`
        # returns on its first line -- which is what makes them the identity
        # witness rather than a behaviour change.
        #
        # THE SEEN-CHOOSING COLUMNS, laid out so BOTH TAILS are readable off one
        # line.  `swarm_windows` is the OPPORTUNITY DENOMINATOR (armed rounds
        # that reached the rung at all); `swarm_dispatch` is how many of those
        # the rung actually spent.  dispatch == 0 with windows high is the
        # NEVER-FIRED falsifier.  dispatch == windows with every refusal counter
        # at 0 is the DEGENERATE-ALWAYS falsifier -- and `swarm_windows` is
        # itself bounded by the trigger, so peck rounds vs armed rounds is the
        # direct measurement of the in-window scoping that arm 3's STRIKE makes
        # load-bearing.
        self.swarm_windows = 0        # armed ROUNDS this body reached the rung
        self.swarm_eps = 0            # distinct siege episodes seen armed
        self.swarm_dispatch = 0       # ... rounds it handed the turn to the march
        self.swarm_pecks = 0          # pecks that LANDED on the shooter tile
        self.swarm_adj_rounds = 0     # armed rounds with THIS body on the ring
        self.swarm_holds = 0          # ... of those, rounds seated with no verb
        self.swarm_nowalk = 0         # dispatched, off-ring, step did not execute
        self.swarm_full = 0           # rounds refused: the ring is at SK_SWARM_N
        self.swarm_stalled = 0        # rounds refused: this body's walk has not
                                      # improved its distance to the shooter for
                                      # SK_SWARM_STALL rounds (the 55-round
                                      # auroraveil loop is what this counts)
        self.swarm_capped = 0         # rounds refused: episode peck budget spent
        self.swarm_dead_release = 0   # rounds RELEASED: the named tile holds no
                                      # enemy building any more -- the
                                      # release-on-dead path, counted so it is
                                      # not merely asserted
        self.swarm_throws = 0         # BUILDER instrument, no answer attached:
                                      # times their launcher threw this body
                                      # while it was a dispatched swarm body
        self.sw_relax = False         # the scoped ledger-V7 escape (see
                                      # `_counter_march`).  Written ONLY inside
                                      # `_stand_swarm_action`; False on every
                                      # round of every OFF arm.
        self._sw_seen_ep = -1         # episode keys, per body (arm 4's key)
        self._sw_peck_ep = -1
        self._sw_pecks = 0            # pecks spent in `_sw_peck_ep`
        self._sw_last_rnd = -999      # last round this body was dispatched
        self._sw_walk_ep = -1         # the walk-progress bound's episode key,
        self._sw_best = 1 << 30       # the best Manhattan distance this body has
        self._sw_stall = 0            # reached in it, and the non-improving run

        self.stand_gate_rnd = -1      # the round the sweep last read the seat
        self.stand_gate_free = 0      # census, and what it read -- so
                                      # `_stand_station` (movement, later in the
                                      # same turn) does not pay the 8 reads
                                      # twice.  -1 can never equal a live round,
                                      # so a body whose sweep did not run this
                                      # turn stations for nothing.

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
