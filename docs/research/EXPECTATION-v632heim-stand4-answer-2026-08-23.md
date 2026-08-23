# REGISTERED EXPECTATION — STAND arm 4: THE ANSWER SENTINEL (SK_STAND_ANSWER)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s57, committed before the build agent runs. Plank:
THE STAND. Inputs: KILLDIAG-ring-blindness-2026-08-23 (banked; 22/36
conversion ceiling at the 30-Ti gate, 33/36 geometry-feasible, exonerated
roads listed), baseline t_cs_* [alive 53 / deaths 49 / wins 35 / kills 22
/ eco 35.80 / harv 212; wins 10/9/16].

**MECHANISM (the SMALLEST step per the small-steps directive):** when the
corefire latch is fresh AND slot 15 names a shooter tile, a home body
builds ONE sentinel at a covering seat — a seat whose build-time facing
ray bears on the shooter tile (can_fire_from is the engine's own
hypothetical-turret check — use it, not hand-rolled geometry) — funded
above the spawn reserve. One answer piece per siege episode; no re-siting,
no ring changes, no ammo machinery (all measured 0/36 or deferred).

**Bars:** A1 identity OFF ≡ t_cs_* 30/30 x3. A2 mechanism (seen-choosing,
both tails per the side-lane rider pattern): answer builds occur IN killer
windows (opportunity column: windows with funds; never-fired count and
degenerate always-build both falsifiers); the built piece's ray bears on
the shooter tile (traced). A3 direction: home-fire-on-killer cells rise vs
measured 1/36; killer suppressed-or-dead episodes reported; our-core death
cells fall on >=2 fixtures. A4 currency: <=r300 ITT non-fall (the stand
buys rounds for OUR kill — a slower game with equal kills is a fail).
A5 guards: alive [53,-2] deaths [49,+4] eco [35.80,-12%] harv [212,-10%];
ammo trajectory reported (the answer sentinel fires from the same pool —
10/shot; its shots compete with the hammer's). Play-it-well line
mandatory. Direction confirmed → scale-up candidates: second answer
piece, the greedy 4-seat ring re-site (out-of-sample form), builder-peck
assist. A fail routes to STAND arm 5.
