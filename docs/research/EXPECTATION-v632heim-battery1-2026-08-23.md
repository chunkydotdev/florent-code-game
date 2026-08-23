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
