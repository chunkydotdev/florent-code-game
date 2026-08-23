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
