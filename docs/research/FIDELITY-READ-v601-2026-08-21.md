# FIDELITY READ — `bots/_v601skalman` tape601 vs the v600 baseline

**Builder s54, 2026-08-21 ~18:4xZ.** Fixture: v601 vs the NOISE_OFF `_v542wave` copy,
15 pool maps × BOTH SEATS = 30 distinct games (seed pinned — inert for a deterministic
pair; the corrected fixture rule applied). Gate CLEARED (subject-vs-fixture escape typed).
Comparator: `FIDELITY-BASELINE-v600-2026-08-21.md` (effective n=15, riders apply).
Raw: `scratchpad/s54_fidtape/t601_{A,B}_fidelity.json`, replays_tape601/. **Mechanism
read only; the only outcome numbers are the kill-round column, reported as required by
the v601 build report's own hazard flag.**

## What the planks delivered (per seat A / B, vs v600 baseline)

* **SUPPLY (SK_ORE_SENSE): DELIVERED POOL-WIDE.** Harvesters built **75 (41+34) vs 28**;
  survivors 16/75 vs 4/28; M1 connectivity 19.5 / 23.5 vs 14.3 (CIs overlap — the gain
  is in the denominators, the survival RATE is still far from 81.4).
* **MORTALITY (SK_HARV_ESCALATE): direction right.** Exactly-4-builders 60.0 / 73.3 vs
  46.7; builders median 4 vs 5. ⚠ One seat-A game spawned **42 distinct builders** — a
  respawn storm exists somewhere; flagged for autopsy.
* **FIRE DISCIPLINE (SK_TARGET_PRIO): DELIVERED** (build verification: shots on barriers
  44.4→0.0%, pecks 83.3→6.4%; corroborated here by the shot-volume collapse below).
* **NEST/CLEARANCE: no change.** M4 volumes tiny (4/4 and 5/6 in-band; the nest is still
  grid-gated — the v602 `_pick_nest` item); M7 14.4 / 7.7 vs 17.8 (flat-to-worse, thin).

## What moved the WRONG way, stated plainly

* **DRIP VOLUME COLLAPSED: converts median 8 / 6 (42 / 38 Ti) vs v600's 24 (166 Ti).**
  The verb itself is fine (lattice 100% / 97.8%, above the 97.3 bar) — the CONSUMER
  disappeared: need-based drip + guns that no longer spam barriers + still almost no
  turrets = almost no ammo need. **The fire-discipline plank exposed that our shot volume
  was mostly barrier spam; what remains is honest and small.**
* **CAGE VOLUME COLLAPSED: 20 / 23 barriers built vs 40 on tape30's 15 DISTINCT games**
  (⛔ corrected s54 ~19:0xZ — this line first said "vs 80", double-counting the s11/s12
  duplicate pairs; ring barriers/game 1.933 → 0.767, ×0.4, the collapse stands on the
  corrected denominator). Ring share 50.0 / 56.5 vs 72.5. **CAUSE FOUND by the tape601
  autopsy (scratchpad/s54_autopsy601/): `_peck_priority` inserted at
  `_cage_walker` sk_roles.py:1534 — the enemy core scores top priority and is adjacent
  to EVERY seal tile, so the walker parks and pecks the core (276 of 286 lap pecks)
  instead of lapping; 92.6% of lap actions redirected, and the 41-round glacierkeep
  peck-park lost the healing race 95 heals to 82 pecks because `_enemy_builder_adjacent`
  is tile-local on a 2×2 core.**
* **OUTCOMES (the build report's hazard, confirmed): we killed their core 0/30. Our core
  died 27/30, median ~r120 (range 88-314). The other 3 games (fimbulwinter A+B,
  stavkirke B) ran to r1000 tiebreaks — nominal wins, DEFEATS under `R1000_IS_DEFEAT`.**
  The economy planks convert some fast losses into stalls, not into kills.

## The iteration verdict (fidelity axis — no game-share, no currency claim)

Planks delivered their registered mechanisms (supply pool-wide, mortality direction,
fire discipline) and the phase-1 gap has **moved, not closed**: survivability is no
longer the sole binding constraint — **the tree has no kill instrument.** Almost no
turrets, no nest on 10/15 maps, clearance flat, and a drip with nothing to feed. The
strangle half is beginning to exist; the kill half does not.

**v602 surface, in order:** (1) `_pick_nest` sensed-terrain fix — the engineer must plant
on all 15 maps (the build report's one-line candidate + stuck-engineer guard); (2) the
cage-volume collapse autopsy, then fix; (3) a drip CONSUMER: turrets that fire at real
targets, sited per SK_BELT_COVER and the nest band — the freed economy (5,700 mined in
the build battery) must buy the kill, per the programme (economy is instrumental, it
never scores); (4) the 42-builder respawn-storm game.
