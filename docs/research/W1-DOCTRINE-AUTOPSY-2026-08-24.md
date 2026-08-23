# DOCTRINE WINDOW 1 — banked autopsy summary (full: w1diag_* scratch)

**GAME CONTEXT: in-game Florent Code League.**

v191, 15 games, 1-14 (gsxWins 0-5, Jython 0-5, Besvikomat 1-4; chassis
went 1-9 on the shared cells). THE DIAGNOSIS: the identity's gate is not
what lost — THE DELIVERY ECONOMY under it is. Median delivered 0.92
Ti/round vs the 2.1 barrel-replacement rate; the single win delivered
4.93 (the only real band burst + checkmate, ours untouched); two games
delivered 0.00 (the never-completed-belt class — SK_ROUTE_HOME's exact
object, refused on chassis currency, now vindicated for the identity).
Trigger: tail A (600 bank) 0/15 structurally dead (bank max = 470 in
14/15 — flow not stock); tail B fired 7/15 but EARLY (r19-71) onto banks
that evaporated (4/7 fires bought <=1 turret). Slot-8 b12 is a DEAD
cross-body channel (engineer-local latch never warms; 0/15 while the
core's fired 7). Death shape 12/15: pure sentinel siege on our core;
8/15 games we dealt ZERO core damage. The two r1000s dealt 1026-1512 and
were HEALED THROUGH (the medic-exile's future case). Iteration 2 (in
flight): SK_ROUTE_HOME ON + tail C (funded-held-3r, delivered-rate
passive-subtracted at replacement cost, free stability) + bounded
re-arm.

**INSTRUMENT DISCOVERY (permanent):** replay Player field 6 — the
schema's "undeclared 16-22 bytes" — decodes as the 16 comms-store slots
(16 packed varints, one-round write buffer). Positive control 15/15
(beat slots == round+1). Every bot's published store is now
wire-readable; w1diag_main.py carries the decode.
