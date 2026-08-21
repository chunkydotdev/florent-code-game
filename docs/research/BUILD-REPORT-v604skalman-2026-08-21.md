# BUILD REPORT + READ — `bots/_v604skalman` (nav-cost planks)

**Builder s54, 2026-08-21 ~21:5xZ.** Copy of `_v603skalman` + 4 queue items; fresh opus
agent; artifacts `scratchpad/s54_v604/`. Outcome column re-verified by the builder (10
winner lines = 9 core-kills + 1 tiebreak, matching). Fixture = the authored NOISE_OFF
benchmark copy; no game-share claim; no submit; no platform matches.

## Shipped
* **SK_DANGER_COST ON** — danger as PATH COST (Dial's weighted flood, K=6, sharing
  NAV_NODE_BUDGET + CPU probe; step-veto off under the cost form, scan-enforced).
  Differential-tested vs a Dijkstra reference: 0/395 disagreements, control produces 69.
  yggdrasil worst case 475 µs ≈ 4.8% of budget (wall-clock proxy; platform test owed).
* **SK_CYCLE_K ON** — period-k (k≤6) cycle guard, 12-entry history, commit-on-detect.
* **SK_ONE_CURSOR ⛔ OFF, measured negative** (kills 9→6 with it on): the cursor commits
  to distant seats, keeps the ring open, and starves the eviction (armed 15.6%→3.3%).
  Same pattern as v603's cage-ceiling: mechanism confirmed, outcome inverted.
* **SK_BELT_EST ON, EXACT NULL** — correct and inert: **the premise does not occur (the
  keeper dies 2/30 and is REPLACED 0/30) ⇒ v603's root-cause attribution for the
  route-gate negative is NOT ESTABLISHED.** Route-gate re-tested at 30 games/setting:
  still OFF (kills =, delivery −4.8%).

## The read vs v603 (same fixture)
Kills **8→9** · by-r300 6→6 (the PROGRAMME-binding measure, flat) · our deaths 21→20 ·
median kill **r256→r275 (the r180 gap WIDENED; SK_DANGER_COST is the measured trade —
off gives r230 median but −1 kill and a 74-round failing cell)** · class-B midgard
livelock 40 rounds → 0 (cyclek alone suffices; ablations: dangercost_off 74r FAIL,
cyclek_off 41r FAIL) · eviction-armed 0.75%→15.6%, max_held 3→3.5 · ≥2-sentinel 56.7% ·
**M1 DOWN 41.9/34.4→32.6/26.7, belt deaths 34→46 — unexplained, v605 diagnosis item** ·
drip lattice 100% both seats · fastest kill yet r132.

## The structural find (v605 item 1, control cell = helheim_A)
**Class A is SELF-BLOCKADE, not turret avoidance:** helheim's only throat is sealed by
OUR OWN nest (2 barriers + a sentinel); the flood answers WEST even with the danger set
forcibly emptied. 1/12 lap tiles in v603 AND v604, byte-identical tracks. The fix is the
tile-owner arbiter extended to PATHS (the nest may not seal the walker's only route),
not a fifth movement flag.

## v605 queue
1. Arbiter-for-paths (helheim_A as the control cell). 2. M1/belt-death regression
diagnosis (34→46 under the new routing — diagnose before fixing). 3. SK_DANGER_K sweep
{2,4,6} — the speed-vs-safety knob, measured at one value so far. 4. Kill-speed: the
second sentinel lands median r95 vs BC's first at r21-58 — what gates the engineer's
departure (diagnose first). Standing owed: platform CPU match test before ANY exposure.
