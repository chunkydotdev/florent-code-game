# BUILD REPORT — `bots/_v515ecosalt` (door-off + A2 OR-gate + evictor reach), s51 2026-08-18

*Banked by the builder s51 from the opus build agent. Parent `bots/_v514ferrycrew` FROZEN
(verified untouched). Master `LOKI_FS_V515`; False reproduces the parent (behaviourally
verified after finding 3). Diff: doctrine +141, siege +254/−2, main +9. **3,687 grid games,
0 tracebacks/timeouts/no-winners.** Artifacts: `scratchpad/s51_v515_build/` (RESULTS.tsv,
21-block tapes, 12 arms, 5 mutant drivers, selftested summariser).*

## ⛔⛔ THREE FINDINGS THAT OUTRANK THE PLANK
1. **`--seed` DOES NOT PIN A GAME — the randomness is OURS.** `main.py:781` re-rolls
   `spawn_salt` from OS entropy once per match under NOISE_ON. Same tree/map/seed, five runs:
   win/loss/loss/r1000/loss. "Paired seeds" pairs the MAP, not the play. Measured spread:
   ±3-5 games per 30-block, up to 9 in 90 same-config. **Every single-draw n=90 separation in
   the v514 report sits inside this** (its naive intervals remain the right ones; its point
   estimates regress).
2. **The v514 door figure does not replicate at size — the SIGN does.** +18.9pp at n=90
   re-measured at **+7.1pp** (n=450, interleaved same-seeds) and +5.3pp vs the parent-door-off
   chassis (n=630). ~40% of the banked magnitude. *(Dated pointer appended to the v514
   report.)*
3. **The flag-off audit caught a defect in the flag-off MECHANISM:** a doctrine-level derived
   default is order-dependent under `mkarm.sh` (arm overrides append AFTER the derivation ran)
   — the master flag did not reproduce the parent, caught behaviourally, fixed by moving the
   door decision to the read site. **Generic hazard for every derived default under the house
   arm mechanism** (→ wrap debt list). Bonus: the constants-diff guard became a constant
   column after the fix (cannot see read-site planks) — its positive control was moved and
   re-driven.

## HEADLINE — 5 siege maps, 21 blocks × 30, n=630/arm, arms CONCURRENT per block
| | **v515 FIRED** | parent+door-off (baseline) |
|---|---|---|
| WINS | **335/630 (53.2%)** | 306/630 (48.6%) |
| kills ≤ r300 (ITT primary) | **182/630 (28.9%)** | 143/630 (22.7%) |
| our core destroyed | 295 | 324 |
| median kill round | 219 | 239 |

Δwins +4.6pp (half-width 5.5 — INSIDE); **Δk≤300 +6.2pp (half-width 4.8 — OUTSIDE, the one
separation that survives).** Early blocks read +15.6pp and decayed to +4.6 — the optimism
curve is on the record. Per map: **midgard 6%→23% (+17pp — v514's "unmoved" open item 3
MOVED; k≤300 0/54→10/54)**, drakkarfjord +14, atoll +12, **glacierkeep −12 (79 vs 91 — while
killing MORE by r300 there, 27/54 vs 14/54)**, nordkap −9. Gated recovery landed:
archipelago 26/36 (72.2%), the predicted number.

## Isolation (control = v514-as-delivered 43.3%, n=450/arm) — SUBADDITIVE
door-off only **50.4%** · gate-OR only **50.9%** · reach only 44.2% · composite 53.2% —
and on the interleaved n=180 block door-off ALONE (54.4%) beats the composite (48.9%).
Mechanism unknown; nothing here says which pair interacts.

## Per-change verification (all mutants driven)
* **Door:** fired 0 peck events/15 games vs mutant 413 events in 8/15 ✅.
* **Gate:** every fired first-sentinel ≥ r72 (floor 60 holds); atoll/midgard now BUY (v513:
  0/12); floor-0 mutant reproduces v514's r7-24 buying on exactly the belted maps; salt
  disjunct fires first on glacierkeep within 2 rounds of mutant timing; both disjuncts
  observed independently ✅.
* **Reach:** fix works as specified and is NOT the binding constraint — **the evictor is
  bought r6-20, BEFORE any seat is belted** (ceiling at build time: ucov≥2 available in only
  3/12 builds, 1 taken; mutant reproduces the parent's 3/9-never-2+ digit for digit).
  **Closure lever = purchase TIMING, not siting.** ⚠ near-null with a geometric reason,
  honestly read.

## ⚠ THE MAGAZINE/PHASE GAP (flagged, not resolved — the next big lever)
The floor-path sentinel on belted maps runs on the chassis's generic ~40-ammo magazine, not
the siege 300 (FS_PH_KILL_OPEN=5 is excluded from the siege magazine by construction;
measured: glacierkeep median 295 ammo vs midgard 36). Coupling naively would re-open the
v514 onlyA regression; the right shape is probably "arm the siege magazine when a FLOOR-PATH
TURRET EXISTS", not when the phase opens. Builder's next-iteration candidate #1.

## Open items
1. Magazine/phase gap (above). 2. Subadditivity unattributed. 3. Evictor purchase timing
(defer until unseal non-empty / free the slot). 4. FS_SENT_RND_FLOOR=60 unswept (only 0 and
60 measured). 5. glacierkeep/nordkap −12/−9 unattributed between gate and reach.
6. mkarm derived-default hazard (tooling → wrap). 7. Self-play fixture caveat, load-bearing
as ever. 8. Inherited: platform CPU test, _wire_tick, FS_CREW_CONVERT.

## BUILDER VERDICT LINES (s51, typed by the lane)
* v515 FIRED at **53.2% [50.4-56.0 naive] n=630 vs incumbent on the siege grid** — the best
  powered read the line has; the k≤300 primary (+6.2pp, outside interval) is the real gain;
  the win delta is inside noise.
* Distance to SHIP_BAR (70 full-pool): large. Named unexploited levers: magazine/phase gap,
  evictor timing, MODESWITCH (+4-5 by composition), GUNNER-FIRST (unpriced), subadditivity
  resolution (door-off-only config is a live simpler candidate: 50.4-54.4%).
* The v514 door number is revised: sign confirmed, magnitude ~+7pp not +18.9.
