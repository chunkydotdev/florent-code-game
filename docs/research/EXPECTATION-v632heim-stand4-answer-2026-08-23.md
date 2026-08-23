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

## DISPOSITION — BUILT, VERIFIED, INERT; NO STRIKE (BUILDER s57)

The plank executed perfectly (identity 9/9, units 0 fails, synthetic
end-to-end control 12/12 bears) and bought nothing: 0 builds / 604 armed
rounds. Binding constraint measured to zero unexplained: TITANIUM DURING
SIEGE (bank 0-20 vs 75-85 live-scale sentinel; 127/138 engine refusals
unaffordable) plus funded-rounds/covering-seat-rounds disjointness.
KILLDIAG CF-2 corrected: its 30-Ti gate did not carry live scale. The
code stays built OFF; it becomes live the moment a pre-siege funding
posture or an earlier trigger exists (scale-up candidates, not this arm).

**ROUTES TO STAND ARM 5 — THE SIEGE PECK SWARM (registered here, blind):**
the one verb affordable in-window (2 Ti/peck; killdiag CF-3: 13/36
convertible at 20 sustained adjacent rounds vs the measured 11).
Mechanism: while corefire_fresh AND slot 15 names the shooter, up to
SK_SWARM_N (2-3) home bodies walk-to-adjacent and peck the shooter
STRUCTURE; medic never preempted; the dispatch exists ONLY inside killer
windows (SC's lesson: all-game pecking is ruinous; in-window the turn's
alternative is death). Bars: W1 identity; W2 seen-choosing both tails
(swarm rounds only in windows; opportunity columns); W3 direction:
sustained adjacent rounds per window rise vs measured 11 median, killer
suppressed/dead episodes rise, our-core death cells fall on >=2 fixtures;
W4 GRID-level <=r300 ITT non-fall (the b3f2diag power lesson);
W5 guards vs t_cs_* incl. eco (the SC failure mode watched: in-window
scoping is the load-bearing difference, measured by peck-round
distribution vs window rounds). Play-it-well line mandatory.
