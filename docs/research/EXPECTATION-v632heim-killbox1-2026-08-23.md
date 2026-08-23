# REGISTERED EXPECTATION — KILLBOX arm 1: EXILE + CORNER CELL (SK_KILLBOX)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All mechanics below are engine-probed
(kbprobe, commit 5d1dd5082, 10/10 steps PASS).**

**PROVENANCE:** BUILDER s57, committed before the build agent runs.
Magnus's signature-move mandate (PROGRAMME tail: iterate until it works,
strike-exempt; must handle r1-r5 launcher-relay rushes). Engine-stamped
facts: exact-tile throw, same-round position mutation, 0 ammo,
CONSECUTIVE-ROUND throws (no effective cooldown, 3 victims/launcher
measured); sealed pocket = no move/no build/no outside heal, only a
2-dmg peck beaten 2:1 by a 1-Ti jailer heal; sentinel executes the NAMED
tile through walls (parallel-addressable block); blind move() = engine
retires the unit in 1 round; full 2-chamber block 93 Ti but 44
build-rounds — TIME is the cost, so arm 1 leads with the launcher.
Baseline t_b4_* [alive 58 / deaths 49 / wins 37 / kills 20 / eco 34.77 /
harv 215; wins 12/10/15].

**ARM 1 (smallest rush-capable step), two pieces under one flag,
instrumented separately:**
1. **THE EXILE LAUNCHER** — built EARLY (opening, low scale) on the
   measured relay corridor toward our half (the prediction study's
   Baltsars/Mjolnir r1-r5 routes; siting read disclosed); any enemy
   builder entering pickup d²<=2 is thrown: to the CELL if one stands
   with an empty chamber, else MAX-DISTANCE toward their half
   (throw-back treadmill). Consecutive-round throws are legal —
   the rush case is the design case.
2. **THE CORNER CELL** — 2-3 barriers against map edge/corner near our
   core (probe: map walls are free walls), built opportunistically by a
   home body when bank allows; NO dedicated sentinel in arm 1 (execution
   is a later arm; detention + treadmill is the dose here). Jailer heal
   only if a home body is already adjacent-idle (no dedicated staffing).

**Bars:** K1 identity OFF ≡ t_b4_* 30/30 x3. K2 seen-choosing both
tails: throws occur when enemy builders enter pickup range (opportunity
column: enemy-builder-in-range rounds; never-throws and throw-at-nothing
both falsifiers); detentions counted (enemy builder rounds inside a
sealed chamber). K3 direction: enemy-builder rounds IN OUR HALF fall on
>=2 fixtures (the exile thesis — the raider-presence integral is the
registered dose); our delivered Ti rises (the eco consequence); enemy
structures built in our half fall. K4 GRID <=r300 ITT non-fall
(exclusion form). K5 guards: alive [58,-2] deaths [49,+4] eco
[34.77,-12%] harv [215,-10%]; launcher/barrier spend and scale delta
reported. Play-it-well line mandatory. Per the mandate a fail routes to
KILLBOX arm 2, never away.
