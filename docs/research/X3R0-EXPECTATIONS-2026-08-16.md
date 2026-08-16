# Declared BEFORE reading the full aggregate (2026-08-16, research arm)

Caveat on the discipline: a 20-file smoke sample was already run to validate the
decoder, so these are not fully blind. Where the smoke sample already moved me,
it is said so.

## CLAIM A — ammo held with no live turret

1. US `a_hold_noturret / a_hold` (share of our ammo-holding rounds with zero
   living gunner+sentinel): **20-50%**. Informed by smoke (one game read 57/102).
2. **DIRECTIONAL, discriminating: US share > THEM share.** The field buys turrets
   early and in volume; our bot converts to an ammo FLOOR before any gun exists.
   If THEM >= US this prediction is refuted and the phenomenon is not ours.
3. Absolute count of idle rounds across our 10,231-game population: **>> 1,056**.
   x3r0's number is therefore population-bound, not a like-for-like target.
4. `conv_noturret_amt` (titanium converted while holding zero turrets) is the
   decision-relevant magnitude and I expect it **non-zero and material**
   (>10 Ti/game on our side).
5. v152 (post-patch) should show a **LOWER** idle share than pre-patch versions
   if the patch does what it claims.

## CLAIM B — damaged-core rounds with an empty heal seat

6. "No friendly builder on ANY of the 8 core-adjacent seats" during a
   damaged-core round: **HIGH for us, >50%** — our builders raid forward.
7. The LITERAL reading ("at least one seat is empty and standable"): smoke
   showed 2/55 in one game because our own barrier/conveyor seal FILLS the
   seats. So I predict the literal reading is **LOW for us**, not ~100%, and
   that the two readings disagree violently. **If so, x3r0's 24% cannot be
   the literal reading.**
8. Control that must come out the other way: `b_hp_over_max_rounds` must be 0
   (a core never exceeds 500 HP). Non-zero = the HP tracker is broken.
9. Control: among games we LOST by core_destroyed, our `b_final_hp` must be
   low and `b_dmg` > 0; among games we WON, THEM's must be. A tracker that is
   stuck would give 500 on both sides.
