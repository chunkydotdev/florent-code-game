# PLANK DODGE — pre-registration and result

version: v92 (candidate)
dev_dir: bots/_v115dodge
parent: bots/_v100hf (v91, tree 4558be91, submission 9850f196)
treehash: 37450121
pre-registered: docs/coordination.md, 2026-08-09 12:50 CEST, commit 87fe371
  (pushed BEFORE the battery fired)

produces: TITANIUM COLLECTED PER 1,000 ROUNDS — an outcome currency, and the
  only number this plank is claimed to move. Builder deaths per 1k rounds is
  reported strictly as the MECHANISM check that the change did the thing it
  says; it carries no verdict weight on its own. The distinction is the s23
  SITE lesson, where a true, confound-controlled persistence statistic licensed
  the day's worst change: a thing that exists to be spent is not measured by
  whether it persists. If collected/1k rounds had not moved, fewer deaths would
  have been a cost, not a benefit.

falsifier: (1) mechanism — variant does NOT show fewer builder deaths on a sign
  test over informative paired fixtures at p<0.05; (2) length artefact —
  deaths per 1k ROUNDS flat once game length is divided out, i.e. the drop is
  just shorter games; (3) economy — titanium collected falls; (4) stop —
  any crash on the variant arm, or win rate down >5pp at discordance >=10%.

treatment_occurrence: The triggering state is "a visible enemy gunner or
  sentinel whose covered tiles intersect a route this builder would otherwise
  take". LOCAL: fires in all four battery opponents — the mechanism moved in
  every one (deaths/1k rounds 2.07->1.77 clanker, 4.40->2.65 flotte,
  5.27->2.69 kladde, 23.42->16.00 ouroboros), so the treatment demonstrably
  occurred rather than being a dead flag. NOT-OCCURRING in band_probe and
  orizon_probe, which produce ZERO builder deaths in either arm — excluded
  from the battery for that reason, and named here so the pool is not read as
  four-of-six generating the effect when it is four-of-six SELECTED for it.
  UNRATED: pending — `match unrated` has no bot selector and plays the ACTIVE
  submission, so the occurrence count against real opponents can only be taken
  after activation.

S5_unrated: **RUN. NOT-REFUTED (n=10).** Two unrated matches against the two
  REAL teams whose imitations carry the effect in the local pool, chosen so the
  read tests transfer rather than just adding n:
    Ouroboros (rating 1592, above us)   `cd9701bb`  **3-2 to us**
    Lunds Stallions (rating 1541)       `e7b913eb`  **2-3 to them**
    combined **5-5**.
  At n=10 this has 47% power for win rate, so it is recorded **NOT-REFUTED
  (n=10)** and never `pass`. It rules out a gross regression against real
  opponents; it cannot confirm the plank. Of note but NOT claimed: 3 of our 5
  wins came on Titanium Collected at r1000, consistent with the corpus fact
  that our tiebreak record (56.9%) beats our core-kill record (46.4%).

## RESULT (foreign pool; LOCAL, DIRECTION ONLY)

Battery: 4 opponents x 8 maps x 3 seeds x 2 seats x 2 arms = 384 games.
Pool: clanker/flotte/kladde/ouroboros_probe — imitations of real teams, 0-1 of
4 of our signatures. `cad_probe` AND `rush_probe` excluded (both call
`random.` in the hot path; HANDOVER names only cad — corrected this session).
Gate: CLEARED. Control equivalence 12/12. Real-engine `match test` vs parent:
4-1, real TLE enforced, no crash.

| | control | variant |
|---|---|---|
| builder deaths / game | 5.97 | **3.08** |
| deaths r0-99 / r100-249 / r250-499 / r500+ | 1.01 / 1.27 / 1.69 / 1.99 | 0.78 / 0.96 / **0.69** / **0.65** |
| deaths per 1k rounds | 10.79 | **5.89** |
| deaths per spawned builder | 0.483 | **0.294** |
| crashes | 0 | 0 |
| win rate | 82.8% | 87.0% |

- **Mechanism PASSES:** variant fewer deaths in 72 informative fixtures, more
  in 26, tied 39 — two-sided sign test **p = 3.7e-06**.
- **Length artefact REFUTED as the explanation:** deaths per 1k rounds falls in
  **all four** opponents, as does deaths per spawned builder.
- **Economy:** the pre-stated criterion was written as a LEVEL (median collected)
  and it FIRED — 2710 -> 2590. **The criterion was mis-specified by me**: game
  length is downstream of the treatment (the variant wins faster), so comparing
  collected levels across different-length games is not a valid comparison.
  Rate-normalised, collected per 1k rounds is **UP in all four opponents**
  (11896->11907, 11233->12524, 8019->9179, 11019->11466). Both readings are
  recorded; I am not deleting the one that fired.
- **Win rate +4.17pp, discordance 10.4%, paired p=0.074 / pooled p=0.25 — NOT
  significant.** Directionally positive. It is not the verdict and is not
  quoted as one.
- **Adverse, reported:** kladde win rate 42/48 -> 36/48 (-12.5pp) while its
  deaths fell. Unexplained.
- **The effect is dominated by one opponent:** ouroboros carries 887 of 1,146
  control deaths (77%). It is an imitation measured 86 pts over-confident
  against its real class. **Magnitude does not transfer; direction is what
  this pool can support.**
- **Band split is LATE-weighted** (r500+ -68%, r0-99 -23%), which is what I
  pre-registered as my reading against research's home-transit bound, on the
  grounds that ~half our builder deaths are FORWARD and nobody had bounded
  those. Research subsequently measured forward transit at 20.3% (48.0% at
  r<=100) versus home's 5.9%, and corrected the pooled bound to 13.5%.

## CPU

Added pass is a second BFS over the same graph, node-capped at 220, run only
when the danger set is non-empty, cached per round per unit. CPU-GUARD trips
(8,000us of the 10,000us budget): **0 for both arms across 6 games vs the
heaviest opponent** — equal, but low sensitivity, since neither arm tripped.
`execTimeUs` is **not recorded by the local engine** (only the platform's), so
the real CPU read is the remote `match test`, which passed with TLE enforced.
Residual risk acknowledged, not eliminated.
