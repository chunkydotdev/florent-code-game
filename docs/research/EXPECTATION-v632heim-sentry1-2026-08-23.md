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

## V1 DISPOSITION + V2 REGISTRATION (blind, BUILDER s57)

V1: ALARM dose delivered (the 28r window cut to 8-9r-to-answer; F2
pecks-before-first-shot 7→21, destroyed 3→6) — and the guards breached
(alive 59→52 vs −2 bar; wins 40→35) with the mechanism traced: arming at
r7-8 pulls OPENING bodies off the economy. FOCUS: hard null by
construction (0/3,614 sweep pecks on turrets — _peck_priority above it
owns those AND already ships hp_trend_ok + gave_up; the march is
single-target) — R2 was incumbent behaviour, the grep-the-incumbent
lesson re-learned; piece DROPPED.

**V2 — ARM EARLY, STRIKE LATE (the window's tail):** the presence alarm
still stamps at the plant (b30 unchanged), but the ANSWER DISPATCH gates
on SK_SENTRY_FROM (registered default r20; the killer's first core shot
lands ~r34 median — the strike uses rounds 20-30 of the window, after
the opening economy is laid) OR earlier if the responding body is IDLE
(no build/harvest task — the opening never abandoned for the answer).
Bars: v1's dose columns must survive the delay (build-to-first-answer
<= ~20 acceptable, destroyed-before-first-shot the true dose); the
guards must return to envelope (alive [59,-2] the binding one); currency
grid non-fall, F2's loss population the target. Both-tail on the
dispatch gate (fires post-FROM / idle-early, never pulls a tasked
opening body pre-FROM).

## V2 DISPOSITION + V3 REGISTRATION (blind, BUILDER s57)

V2: the gate is clean (M9 ≡ ungated 3/3; refusals traced at bank 298+)
and the dose survives — but the 90-cell split census shows only 10 cells
ever gated: **the alive breach (51 vs [59,−2]) is post-r20 — the d²39
presence alarm is near-always fresh late-game (the #132 always-fresh
class in presence form), pulling home bodies at turrets that are not
killers.** Both autopsies: killers at median d²=5, 71.7% ≤13; the 39
fence chases everything.

**V3 — NARROW THE ALARM TO THE KILLING BAND: SK_SENTRY_DSQ 39 → 13.**
One constant. The FROM gate and idle lift stand (harmless, both-tailed).
Predicted: the dose concentrates on true killers (the F2 19 sit at
median 5), the late-game chase collapses, alive returns to envelope.
Bars: dose columns held on the ≤13 population (destroyed-before-first-
shot vs 6); alive-sum back within [59,−2]; currency grid non-fall; the
±4 floor governs win reads. Both-tail: turrets at d²14-39 UNANSWERED by
the presence path (the damage path still covers them), ≤13 answered.

## V3 VERDICT — ADOPTED (BUILDER s57): alarm at the killing band (DSQ 13)
+ FROM gate + idle lift; FOCUS dead. Dose held (build-to-answer 7r on
F2, spread 37.3→24.3, destroyed-before-first-shot held), alive-sum 58
within [59,−2], deaths 47 = base, wins 40 = 40 (kills −1, inside floor),
medians −4/−3/−8 — hardening + tempo grade, disclosed as outcome-flat at
the win column. Named trade: helheim_seatA's 14-32-band-only population
is given up to the damage path (20/36 vs 13/36 on the touched cells says
the trade pays). Banked engine fact: the 33-39 band cannot threaten the
core (sentinel reach r²=32) — the wide fence armed at harmless pieces.
**NEW BASELINE: the st3build_smoke tapes** [alive 58 / deaths 47 / wins
40 / kills 23; per-fixture wins from the smoke readout]. NEXT: the
3-seed CONFIRMATION BATTERY on this config (the standard's first run —
F3's bar claim + fresh denominators), then the unrated window.
