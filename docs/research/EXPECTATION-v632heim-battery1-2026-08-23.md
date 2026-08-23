# REGISTERED EXPECTATION — BATTERY arm 1: THE LIVE CEILING (SK_BATTERY_WANT)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s57, committed before the build agent runs. Plank:
THE BATTERY (three-plank lock). Inputs: STUDY-battery-execution-2026-08-23
(banked; achievable 4.0 vs achieved 2.0 in win cells, gate sk_roles.py:7208
want=2), baseline t_cs_* [alive 53 / deaths 49 / wins 35 / kills 22 / eco
35.80 / harv 212; wins 10/9/16].

**MECHANISM:** raise the LIVE tube ceiling — the nest machinery keeps
planting past 2 when the purse clears the bot's own surcharge bar
(sk_roles.py:8608 form: cost + SK_AMMO_SENTINEL x (live+1) + floor), up to
SK_BATTERY_WANT (registered default 4, the doctrine's number). Affordability
-gated per plant, so loss cells (achievable 2.5) self-limit — the flag
converts surplus into barrels, never starves the base (spawn reserve
untouched).

**Bars:** B1 identity OFF ≡ t_cs_* 30/30 x3. B2 mechanism: peak-concurrency
distribution shifts right in cells with purse headroom (win-class cells
reach 3-4); rounds at conc>=3 rise vs measured 0-median baseline. B3
execution quality: achieved/achievable peak ratio (the study's sim, re-run)
rises vs 2.0/4.0 win-cell baseline. B4 currency: gross HP/round on their
core rises toward the 4.5 band in conc>=2 cells (study: wins 6.31 battery-up
HP/r); <=r300 ITT non-fall per fixture. B5 guards: alive-sum [53,-2],
deaths [49,+4], eco [35.80,-15% — barrels compete with eco, disclosed],
harv [212,-10%]; wins/kills with per-fixture splits (10/9/16). Play-it-well
line mandatory in the verdict. A fail routes to BATTERY arm 2 (burst rule),
never to a new plank.

## DISPOSITION — BUILT, VERIFIED, NULL-WITH-MECHANISM; NO ADOPTION, NO STRIKE (BUILDER s57)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

The arm is correct (32 unit controls x2 trees, OFF byte-identity 3/3,
tracer inertness measured, mutation controls both directions) and moves
1/60 cells, 0 outcome sums. B2's own falsifier fired the honest way: the
gate is REACHABLE but NOT BINDING — the engineer's ledger reads live>=2
for ~1 round/cell (median open window 3 rounds), 204/222 plants occur at
ledger-live 0, and MUT-A (bar removed entirely) changes nothing — money
is not the constraint. Best case fully funded (bank 441-510 vs bar 136,
10 open rounds) is byte-identical: the OFF arm re-picks the same tile.

**EXECUTION-QUALITY LINE:** executed as designed against the wrong gate.
No strike. **The study's 62/90-at-ceiling and this build's ledger read
measure different quantities** (wire concurrency vs the engineer's book;
the book under-reads because SK_TUBE_FLOOR2 ships False and out-of-vision
tubes book as dead) — tension banked, not resolved.

**ROUTES TO BATTERY ARM 2:** (a) the burst rule (withhold plant #1 until
two funded at the :8608 surcharge — attacks plant RATE, the measured
binder: the open window is shorter than the walk to a MIN_GAP=8 site);
(b) SK_TUBE_FLOOR2 ON (fix the ledger under-read so live tubes are
booked alive). SK_BATTERY_WANT stays built at 0 — it becomes live the
moment arm 2 lengthens the window it needs.

**ARM 2 RESHAPED BY DOCTRINE (Magnus's eco-ready ruling, encoded in
PROGRAMME.md the same hour):** arm 2 = (a) SK_TUBE_FLOOR2 ON (the ledger
under-read fix), (b) the burst rule at the surcharge bar, AND (c) the
ECO-READY latch — the battery's growth beyond the standing pair keys on a
live funding signal (bank + income trend covering ~2.5-3 Ti/round ammo +
barrel replacement), not on r300 and not on mere gate-affordability at
one instant. Registered fully before the arm-2 build fires.

**SIDE-LANE RIDER, CONSUMED (arm-2 registration requirement, the
always-fresh lesson applied prospectively):** the eco-ready latch carries
BOTH-DIRECTION bars on its fire-round distribution as a registered
column — median, p10, and never-fired count per fixture. Falsifier LOW:
never-fires ⇒ no hammer ever lands, r1000 defeats by construction.
Falsifier HIGH: fires at spawn-adjacent rounds ⇒ the latch degenerated to
always-true and the "hammer" is the rush the doctrine forbids. The latch
must be SEEN choosing rounds — distribution spread across cells with
different economic trajectories, calibrated against the banked 2.5-3
Ti/round sustain rate. The arm-2 build discloses the predicate's read and
the readout scores the distribution before any outcome column.

## ARM 2 DISPOSITION (BUILDER s57) + ARM 3 REGISTRATION

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

Arm 2 per piece: **(a) ledger CONFIRMED** (live>=2 engineer-rounds
46→2,880 F1 / 102→3,876 F2; phantom plants at ledger-0 nearly halved) —
and its honesty REMOVES the accidental replant loop that was producing
the old conc>=3 rounds (1,185→0) with by-r300 kills 13→9 on the smoke:
the fix and the ceiling must ship together. **(b) burst NULL, measured**
(first-pair gap unchanged; escapes fire 13/30 — money absent at plant-1
time; piece dropped). **(c) eco latch FALSIFIED AS REGISTERED — the LOW
tail fired (1/60) and the build agent STOPPED per the rider.** Named
cause: the barrel-replacement term double-counts (the plant gate already
prices the next barrel). EXECUTION-QUALITY: all three pieces executed as
designed; (c) is a bar-spec defect, not a weld. No strike.

**ARM 3 (SK_BATTERY2 with the corrected latch), registered BEFORE the
edit:** the bar becomes ammo-term-only at 3.0 Ti/round (the diagnostic
showed it CHOOSES on F1/F2 — that derivation is POST-HOC on those tapes,
so the both-tail bars re-bind on the FULL grid including F3, which no
latch analysis has seen: fire-round median/p10/never-fired per fixture,
LOW = never-fires, HIGH = p10 at the warm-up floor). Burst stays OFF
(dropped). Ledger + ceiling-4 ship under the master flag as arm 2 built
them. Bars otherwise as arm 2's: peak-concurrency right-shift where
funded, duty, currency <=r300 ITT non-fall, guards vs t_cs_*.

## ARM 3 READOUT SCORE (BUILDER s57) — LATCH PASSES BOTH TAILS; ONE BAR FAILS; DIAGNOSTIC BEFORE VERDICT

Latch: fires 4/7/7 cells, p10 53/48/59 (all above the warm-up floor),
median 82-145 — SEEN CHOOSING, the side-lane rider's column clean.
Guards: alive 59(+6, campaign high), deaths 47(−2), eco −2.5%, harv
+4.2%. Wins-sum 41(+6) — F1 10→14 (timely: kills 5→9), F2 9→11, F3 16
held — the first outside-noise win movement of the campaign (SC's −4 and
prior deltas all sat inside DEFF noise; +6 does not). **FAILED BAR: F2
≤r300 ITT −0.167 (kills 8→3)** with the anomalous signature duty+0.019 /
gross+0.141 / wins+2 all rising while kills fall, two F2 gains arriving
as r1000 conversions (programme-defeats). Per the rule no adoption past a
failed bar; per the arm's value the fail gets DIAGNOSED, not routed away:
which F2 cells lost their timely kills, and is the mechanism the latch
diverting mid-game titanium on the income-fragile fixture, the honest
ledger suppressing the mid-range replant (conc≥3 rounds −322 there), or
divergence shuffle. Verdict types on the diagnosis.

## ARM 3 F2 DIAGNOSTIC (banked; scripts b3f2diag_*) — AND A REGISTRATION-VS-CODE GAP

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**⛔ THE GAP: `SK_BATTERY2_BURST` SHIPS TRUE against the arm-3
registration's "burst dropped."** It fires (5/90 cells, exactly +20-round
plant-1 holds on the identical tile, wire-confirmed) and is the sole
mechanism-attributable F2 kill loss (longhouse_seatA r256 kill → r557;
their core untouched at the base kill round, gross shortfall 1,368).
PROCESS DELTA banked for the wrap: the builder committed after report
without asserting every SUB-flag against the registration — the
arm-verification step now includes a sub-flag-vs-registration assert.

**THE F2 COLLAPSE IS CHURN, NOT A MECHANISM:** per-cell — 2 lost-kill
cells with byte-identical turret streams (SHUFFLE), 1 never-had-a-pair,
1 got MORE barrels and lost anyway, 1 burst-hold, 1 genuine
ledger-suppression. Discordant cells: F2 6/1 (p=0.125 pre-DEFF), GRID
10/10 (p=1.0), grid ITT exactly +0.0000. LATCH-DIVERSION REFUTED
structurally (live<want exits before the latch is consulted) and on the
wire (conversion FELL 2.1%; income clears the bar from r20 everywhere).
The ledger's conc>=3 suppression lands 91% in cells with no kill either
way; kept-kill cells show the ceiling PAYING (holmgang_seatB 3rd barrel
95r earlier, kill 74r earlier). Confound check: single-plank contrast
proven (identity tape byte-identical 30/30; seat-clear masters False in
both).

**ARM 4 (registered here, blind to its tapes):** (1) SK_BATTERY2_BURST →
False — the registered state, one constant; (2) ledger stays honest;
(3) eco-ring warmth persisted across engineer turnover (batt2_eco_cold
was the real consult-blocker where money and site were both open) —
smallest form first: seed/persist the ring, constants disclosed;
(4) THE CURRENCY BAR RE-REGISTERED AT GRID LEVEL per the DEFF direction
rule: grid <=r300 ITT non-fall (restated as exclusion), per-fixture
columns reported not gated — a 30-cell per-fixture count with 7
discordant cells cannot resolve +-5 and fails only as noise.
