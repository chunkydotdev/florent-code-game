# PREREG — does the LOKI-2 committed opening pay as a function of MAP DISTANCE?

**Written and committed BEFORE the battery was launched.** Two-clock standard:
git author time on this file vs the battery's own start. Nothing below is
edited after numbers exist; results land in a separate dated doc.

## THE QUESTION, AND WHY IT IS DUE NOW

Queue item 4 — *the map/opponent gate on the rush*. I declined it in an earlier
session and set the release condition myself: **build it once the rush is
MEASURED, so it is a choice between two known quantities.** LOKI-2b has a
verdict, so my own condition is met and this is the test that decides whether
the gate is worth building at all.

**The arithmetic that motivates it is free and cannot be confounded.** The
corpus recipe LOKI-2 committed to is **three turrets planted by r22** (p25 r11).
A builder bot moves **one tile per round**. Core-to-core Manhattan distance
across our 15-map pool spans **5×**:

| band | maps | distance |
| --- | --- | --- |
| **SHORT (≤16)** | meander 7, antler 8, fjordgate 8, moonrise 9, eider 12, heart 12, nordkap 12, lighthouse 16 | arrival by ~r8–r17 |
| **LONG (≥24)** | atoll 24, drumlin 26, archipelago 28, jackpot 28, saga 28, snowflake 28, hive 36 | arrival ~r25–r37 |

**On `hive` (36) a raider cannot physically reach the enemy ring by r22, so the
recipe the rush commits to is unachievable there before the window closes** —
while the rush is still paying its price (harvester prerequisite waived, bank
floor cut 40 → 8, two seats leaving at once instead of one). A cost with no
possible benefit is the definition of a plank that wants a gate.

## PRE-REGISTERED PREDICTION

**An INTERACTION, not a main effect.** `LOKI2_RUSH_ON` improves
`core_kill_share` on the SHORT band and is **neutral-or-negative** on the LONG
band. That is the only result that justifies building a gate.

## METRICS — PRIMARY FIRST, and the secondary may not stand in for it

- **PRIMARY: `core_kill_share`** — share of games decided by `core_destroyed`
  in our favour. Reported **per band**, rush ON vs rush OFF.
- **SECONDARY: `time_to_core_kill`** — median turns on core-kill wins.
  **A secondary-only movement is NOT a pass** (D10). If share does not move,
  the plank is null however pretty the clock looks.
- Win rate is **not** a verdict (`WIN_RATE_IS_VERDICT: no`) and is reported
  only to show it did not collapse.

## FALSIFIERS — stated before the numbers, so they cannot become excuses

1. **Rush ON ≥ rush OFF on `core_kill_share` in BOTH bands** ⇒ no interaction,
   **the gate is not warranted and queue item 4 DIES.** I will record that and
   close the item rather than keep it open as a chore.
2. **Rush ON < rush OFF in BOTH bands** ⇒ the rush itself is the problem and
   the answer is to remove it, not gate it. That would be a verdict against
   LOKI-2, a plank already passed, and I will say so plainly.
3. **The bands do not separate** (overlapping intervals, no ordering) ⇒
   underpowered, recorded as NO VERDICT, not as support.

## CONFOUNDS, NAMED NOW

- **Band is confounded with map identity**, not just distance — 8 short maps and
  7 long ones are also different terrain, ore layouts and symmetry classes. The
  distance reading is the *hypothesis*; the interaction is what is measured. I
  cannot separate "distance" from "these particular maps" with 15 maps and will
  not claim to.
- **Self-play pool.** `*_probe` opponents are foreign imitations, not our own
  lineage (gate verified), but they are still not the ladder. Published
  amputation work puts ~2× inflation on self-play; these are proxies.
- **Paired determinism.** Same (map, seed, seat) triples, `--tle 0`, NOISE_ON
  False on both arms, gate CLEARED with **control equivalence identical 12/12**.
  Per-map flips are chaos-bounded: identity results are gold, small flip counts
  are butterfly-sensitive and must not be over-read as attribution.
- **This is an ABLATION, so the flags-off arm IS the parent.** There is no third
  variant; `--control` and `--parent` are deliberately the same dir.

## FIXTURE

`tools/det.py`, `_det_v118lokinorush` (rush OFF) vs `_det_v118loki2b` (rush ON,
the current best on the line), all 15 maps × 3 seeds × both seats, against two
distinct foreign archetypes: `ouroboros_probe` (pure gunner picket) and
`cad_probe` (sentinel siege). Reported per band and per opponent; **bands are
assigned from the table above, which is fixed by this document before any game
is played.**
