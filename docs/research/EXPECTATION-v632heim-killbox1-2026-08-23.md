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

## ARM 1 DISPOSITION + ARM 2 REGISTRATION (pre-tape, BUILDER s57)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**K3 AS REGISTERED IS REFUTED BY GEOMETRY, not by noise:** a launcher
inside our defensive band cannot throw to the enemy half (max throw ~5.1
tiles; 1,064/1,197 throws land in our half; presence integral +43.4% on
the F1 smoke, 21/30 cells). THE WORKING MECHANISM IS TIME-THEFT: raiders
alive but perpetually walking back — their in-half builds −8.2%, our eco
+33.8%, harv +56.7%, mined +29.6%, wins 12→14, intruder kills −35.3%
(the launcher lifts raiders OUT of our turrets' lines — the preservation
side-effect). COST: median length r258→r333, ≤r300 kills 7→6 — the
programme's binding direction. Per the never-tape-known-dead rule the
full grid is NOT spent on the refuted dose; per Magnus's iterate-mandate
the family routes forward.

**ARM 2 (SK_KILLBOX_EXEC, registered blind before its build): CONVERT
THE STOLEN TIME INTO TEMPO.** Three pieces: (1) THE EXECUTIONER — one
sentinel on the cell's ray (probe: targeted-tile, through-wall, 3 shots/
30 ammo); detained raiders are RETIRED, the chamber recycles, and the
presence integral falls the honest way — by deletion (this also restores
the intruder-kill column arm 1 suppressed). (2) INTERIOR CELL FALLBACK
(arm 1 coverage was 13/30 — back-edge geometry missing on half the
pool); the probe's interior 4-barrier form is the fallback, corners
preferred. (3) NOTHING ELSE CHANGES — the treadmill, siting and buy
stand as built.

**ARM 2 BARS:** K1 identity. K2 both tails (executions occur where
detentions occur; opportunity columns). K3' AMENDED DOSE, stated
honestly: enemy-builder RETIREMENTS in our half rise (deletion, not
displacement); their in-half builds fall; our eco holds arm 1's gain.
**K4' THE BINDING BAR — TEMPO: median game length and ≤r300 kills must
NOT regress vs t_b4_* baseline** (arm 1's r333 is the disease; the
execution + the battery latch consuming the +30% eco are the predicted
cure — latch fire-rounds reported as the coupling column). K5 guards vs
t_b4_* as arm 1's. Play-it-well line mandatory.
