# AMMOFLOOR (`_v501ammofloor`) — S0 block

Parent / control: `bots/_v468kladturbo` (PINNED; this tree is a fresh copy, never
an edit of it). One plank, one flag (`LOKI_AMMOFLOOR_ON`), one dose knob
(`LOKI_AMMOFLOOR_DOSE`). Rationale, pricing and the full swept curve are in
`doctrine.py`, block `LOKI-AMMOFLOOR`.

produces: TURRET PURCHASES the ammunition drip currently outbids — turret builds
per game and forward sentinels per game, bought out of bank that `convert_ammo`
would otherwise have spent. Priced on the DELIVERED OBJECTIVE, the share of all
games ending in a core-kill by r300 (`PROGRAMME.md` timely-kill / ITT), with mean
ammunition held, shots fired and dry-turret rounds as the paid-for cost. Not
priced on survival, harvesters-alive or any r1000 tiebreak key.

falsifier: (a) timely-kill-by-r300 falls versus the control with the 95% interval
excluding 0 — this fired for dose 3 (-27.5pp +-6.5 NOISE_OFF, -19pp +-8
NOISE_ON) and dose 3 is disqualified; or (b) the dose is not delivered, i.e.
`af_bind` / floor-regime counts are unchanged from control — this fired for dose
1 (0 of 120 cells changed on every metric) and dose 1 is dead.

treatment_occurrence: local, control arm, mean per game over 240 deterministic
cells — 107.8 rounds in which the drip wanted a top-up, of which the floor was
already binding in 37.1; floor == 12 in 57.7, floor == 46 (E1) in 49.3, floor ==
52 (unarmed branch) in 0.8. At the shipped dose 4 the raised floor is in force
for 120.1 rounds/game and `af_bind` rises +26.0 +-8.2 in 237 of 240 cells.
Unrated count: NOT YET MEASURED — no unrated leg has been fired for this plank.

S5_unrated: REQUIRED, NOT DONE. The local panel is eight old versions of our own
lineage and the control wins 97.9% of 240 games, so the fixture is saturated and
a BENEFIT is undetectable on it by construction; only the mechanism reads carry.
Local screening killed doses 1, 2, 3 and 5 and selected dose 4 by minimising a
measured cost rather than by demonstrating a gain. Per LOKI directive point 6
this arm cannot confirm or close the road; the read has to come from
`fcode match unrated <team_id>` against live teams, pinned per the treatment-leg
rule, before any ship claim.
