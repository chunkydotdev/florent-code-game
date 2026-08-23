# REGISTERED EXPECTATION — STAND arm 2: HEAL-SEAT CLEARING (SK_STAND_SEATS)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

**PROVENANCE:** BUILDER s57, committed before the build agent runs. Plank:
THE STAND (three-plank lock). Inputs: the ahbuild seat census (during
siege windows only **1.54 of 8** core heal seats are free; **2.63 hold
OUR OWN buildings** — apron/door barriers, belt termini; 10 of 46 siege
cells have NO free seat), baseline t_cs_* [alive 53 / deaths 49 / wins 35
/ kills 22 / eco 35.80 / harv 212; wins 10/9/16].

**MECHANISM:** a medic cannot heal from a seat our own barrier occupies.
`destroy` on an allied building is free, unlimited, no cooldown. Under
siege (the CS arm's own honest trigger), a home body clears ONE owned
non-load-bearing building from a heal seat the medic needs — never a
turret, never a belt piece currently carrying resource flow toward the
core (operationalization to the build agent, disclosed), never more than
needed to seat the stand.

**Bars:** S1 identity OFF ≡ t_cs_* 30/30 ×3. S2 mechanism: free-seat
share during siege rises vs measured 1.54/8; stand heal-rounds rise vs
t_cs_* threatened-cell baseline (measured at readout). S3 execution
quality (play-it-well): heals landed / (siege rounds x achievable rate)
reported both arms. S4 currency: ≤r300 ITT non-fall per fixture. S5
guards: alive-sum [53,−2] deaths [49,+4] eco [35.80,−12%] harv [212,−10%];
the destroyed-building count and scale-refund side effects reported.
Adoption per bars; a fail routes to STAND arm 3, never to a new plank.
