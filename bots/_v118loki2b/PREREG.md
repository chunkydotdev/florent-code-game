# LOKI-2b — unrated probe vs Ouroboros (NOT a ship)

version: unrated probe only; the slot returns to v92 immediately after
dev_dir: bots/_v118loki2b
line: loki (PROGRAMME.md). Compared against LOKI-1 offline; against LIVE v92's
  own unrated baseline on the ladder fixture.

produces: A DEAD OUROBOROS CORE INSIDE r250 on maps where we currently do not
  win. Priced in core-kill wins on a fixed 5-map fixture. Time-to-core-kill is
  the mechanism check; win rate on 5 games is not a verdict at any n.

falsifier: zero core-kill wins on the fixture. Baseline v92 took 1 of 5 and that
  one was a r1000 tiebreak, so ANY core kill is signal and ZERO core kills with
  no improvement in loss length refutes the rush against this opponent.

treatment_occurrence: the rush arm requires a raider within d²<=50 of an enemy
  core tile before r60. VERIFIED locally: first forward plant moves r120 -> r21
  under the flag. Against Ouroboros specifically it is UNMEASURED, and that is
  the point of the run.

S5_unrated: THIS IS the unrated read. n=5. Recorded NOT-REFUTED (n=5), never
  `pass`. 47% power at n=10; at n=5 it is lower still and can only detect a
  gross effect. That is acceptable because the baseline is 1-4 with the single
  win at r1000: a core kill would be a state we have essentially never reached.

## WHY OUROBOROS AND WHY THIS IS THE RIGHT FIRST SUBJECT

- **Worst matchup we have**: 23/150 = 15.3% over the largest sample on the tape.
- **Pure GUNNER grind** — 7,831 gunner shots, ZERO sentinel. Their weapon is
  point-blank and therefore tile-contestable, unlike CAD's stand-off sentinels
  at d²=26 which nothing we own can reach.
- **ZERO launchers, ZERO throws.** They have no mechanism to contest a rush.
- **Static**: no new version in 373 matches, so an A/B against them stays valid.
- **We lose anyway.** At 15.3% the variance of an all-in is free.

## PRE-REGISTERED, BEFORE THE RUN

Fixture is **the same five maps as v92's baseline run** — saga, atoll,
lighthouse, eider, nordkap — NOT a fresh map set, so this is a genuine
before/after on one fixture rather than two different experiments.

**v92 BASELINE, measured 2026-08-09 (match 3c6d91d2): 1-4.**
  saga WIN @r1000 (tiebreak) · atoll LOSS @563 · lighthouse LOSS @1000 ·
  eider LOSS @521 · nordkap LOSS @279

**PREDICTION:** the rush converts LOSSES into CORE KILLS on the three maps where
Ouroboros currently kills us before r600 — **atoll (563), eider (521),
nordkap (279)**. It should NOT be expected to convert lighthouse (r1000
stalemate) and should NOT lose saga, which we win on economy.

**SEAT CAVEAT:** unrated flips seats. v92 played seat B in the baseline. If this
run draws seat A the comparison is seat-confounded and I will say so rather than
read the delta.
