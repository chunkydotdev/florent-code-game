# REGISTERED EXPECTATION — STAND arm 3: SEAT CLEAR-OUT (SK_SEAT_CLEAR re-screen)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. The attack verb is the engine's
documented builder action against an opposing bot's in-game structures.**

**PROVENANCE:** BUILDER s57, committed before the work runs. Plank: THE
STAND arm 3 (also serves THE ROUTE: same enemy-barrier-on-our-seats
class). Inputs: stand2 disposition (THEIR barriers hold 3.60/8 heal seats
during sieges, corrected census ssbuild_ownclass.py), diag431 (401/627 F1
idle-adjacent target-rounds are enemy barriers on OUR delivery seats;
destroyable-episode accounting 19/42 F1, 12/22 F2, 8/23 F3), queue #133.
Baseline t_cs_* [alive 53 / deaths 49 / wins 35 / kills 22 / eco 35.80 /
harv 212; wins 10/9/16].

**MECHANISM:** the existing SK_SEAT_CLEAR path (built for enemy barriers
on our seats, never screened on the post-WG/NS/CS tree). The build agent
first READS the existing implementation and the reasons it shipped OFF,
adapts minimally (the play-it-well form: pecks land where bank and
adjacency allow — the chew-persist adoption already removed the give-up
binder for keepers), and discloses every change.

**Bars:** T1 identity OFF ≡ t_cs_* 30/30 x3. T2 mechanism: enemy-barrier-
on-our-seat episodes destroyed rises vs the diag431 destroyable baseline;
seat-tile occupancy by THEIRS falls vs 3.60/8 (corrected instrument).
T3 execution quality: pecks landed / (idle-adjacent rounds x bank-allowed)
reported. T4 currency: <=r300 ITT non-fall; stand heal-rounds reported
(freed seats should feed CS). T5 guards: alive [53,-2] deaths [49,+4]
eco [35.80,-12%] harv [212,-10%]. A fail routes to STAND arm 4.
