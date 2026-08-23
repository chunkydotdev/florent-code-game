# REGISTERED EXPECTATION — THE SENTRY (SK_SENTRY: presence-trigger + concentrated peck)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s57, committed before the build agent runs.
Inputs: MJAUT-double-autopsy-2026-08-23 (banked; R1+R2, the two
field-general recommendations): the 28-round damage-latch free window
(19/19 F2 killers inside the SK_DEMOLISH d²39 fence, 0 pecks in 17/19,
body+funds idle in 10/19), the 85%-bought kills (17.0/20 pecks spread
over 24 targets), the ~1:1 heal-lock on the 14.3% Mjolnir defends.
Baseline t_bg_* [11/10/19, wins 40].

**PIECES (one master SK_SENTRY, ablatable):**
1. SK_SENTRY_ALARM — a PRESENCE trigger: an enemy gunner/sentinel BUILD
   observed inside the d²<=39 fence arms the same answer ladder the
   corefire latch arms today (the existing verbs — counter-peck/
   demolish dispatch — get the earlier trigger, no new verbs). The read:
   get_nearby_buildings + type + team, on bodies already scanning.
   Both-tail: arms on plants (opportunity column), never arms on
   friendly/out-of-fence builds.
2. SK_SENTRY_FOCUS — commitment: once a turret target is engaged, the
   peck dispatch concentrates to the kill threshold (20) within a
   bounded window instead of spreading; HEAL-AWARE give-up: a target
   whose HP ledger shows ~1:1 heal-back over the last K pecks is
   abandoned (banked: feeding a heal-locked target is 4:1 their favour).

**Bars:** S1 identity OFF ≡ t_bg_* 30/30 x3. S2 both-tail seen-choosing
per piece (alarm arms in the window — the 28r reference; focus
concentrates — pecks-per-engaged-target vs 17.0 spread). S3 DOSE: the
free window falls (build-to-first-answer median vs 28r); killers
destroyed-before-first-core-shot rises vs ~0; per-target kill completion
vs 13/24. S4 CURRENCY: grid <=r300 ITT non-fall with rise hoped; F2's
column the focus (its 20 losses are the population). S5 guards vs t_bg_*
[alive 59,-2 / deaths 47,+4 / eco 37.30,-12% / harv 218,-10%] — the SC
lesson watched (in-window scoping: the alarm must not turn into all-game
pecking; out-of-window pecks byte-flat). Play-it-well line mandatory.
