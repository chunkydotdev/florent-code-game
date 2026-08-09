# LOKI-8 (v124) — raiders stop going home. The next removal in the same family.

version: unrated benchmark only. **NOT for the ladder** — Magnus holds that
  approval and reaffirmed it ("No ladder yet").
dev_dir: bots/_v124loki8
line: loki. **COMPARE_AGAINST `_v123loki7` (v98)** on the identical fixture —
  5 short maps × 3 real opponents, n=15.

produces: **CORE-KILL SHARE, by returning to MOVEMENT the rounds a raider
  currently spends going home.** Two paths pull a raider back: the universal
  adjacent heal (which returns before `_raid` is ever called) and the
  raiders-only melee recall. Research measured the heal pin directly — a
  builder beside a DAMAGED core moves on **15.5%** of rounds vs **68.3%** at
  full HP (n=143,812), opponent control −0.152, so it is our code and not the
  game. The core is still healed: expanders and the dedicated defender keep
  both paths.

falsifier: **core-kill share at or below LOKI-7's 13/15 = 86.7%.** Also
  refuting: a material drop in WIN rate. `SLOT_UNDER` latches 50 rounds off any
  enemy turret near our core, so this removes raiders from home defence for
  long stretches against a shelling opponent. **Win rate is not the verdict,
  but a bot that loses its own core faster ultimately kills fewer of theirs**,
  and I will not wave that away by pointing at the primary currency.

treatment_occurrence: **NOT separately verified — this is a removal of a block,
  so it only occurs in games where the block would have fired.** If the leg
  reads null I will decode raider position-vs-home before concluding the change
  does nothing. Today already produced two versions of this error: LOKI-6's
  fixes measured null with occurrence unverified, and LOKI-QUIET verified the
  treatment it CODED rather than the one the experiment required.

S5_unrated: **this IS the unrated read**, same fixture as every arm in
  `docs/RESULT-loki-iterations-2026-08-09.md`.

## LIMITS

- **n=15, directional.** LOKI-7 vs LOKI-5 is already p=1.0 — the line's recent
  steps are within noise of each other, and LOKI-8 will most likely also land
  inside that band. **The comparison that is significant is against EIR
  (LOKI-7 p=0.0078), not against the previous iteration.**
- **Seats cannot be controlled**; they have varied per leg.
- **The whole line is measured on SHORT maps.** LOKI-5 drops 80% → 60% on the
  long band. Whatever LOKI-8 reads here, it is a short-map number.
