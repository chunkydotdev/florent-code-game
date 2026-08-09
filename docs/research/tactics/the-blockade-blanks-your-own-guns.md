---
tactic: Premortem — your own blockade blanks your own attack, and here it also shoots your own units
source: https://battlecode.org/assets/files/postmortem-2021-musketeers.pdf
origin: Battlecode 2021 3 Musketeers ("muckraker dispersion"); Battlecode 2023 4 Musketeers (rotation for the same reason)
evidence: documented
transfers: yes
---

WHAT IT IS — **the failure mode every besieging team hits second.** 3 Musketeers
built a body-blockade around the enemy base, then found the blockade had stopped
their own kill:

> *"our rush politicians would have trouble destroying enemy ECs if the EC was
> surrounded by our hunter muckers"*

Their fix was an explicit unblocking behaviour:

> *"muckraker dispersion, where muckrakers move away from politicians when they
> read the flag and see that it is rushing a base"*

4 Musketeers hit the same wall in 2023 and solved it by keeping the ring in
motion rather than static:

> *"launchers crowding an enemy base will rotate around it, attacking any enemies
> they find along the way"*

and note the second-order benefit — the rotation is what lets reinforcements in:

> *"it creates openings in the direction we originally came from, allowing more
> launchers to join our circle"*

**Two independent top teams, two years apart, both had to write code whose only
job was to undo their own blockade.**

WHY IT MIGHT TRANSFER — **it transfers harder here than in either source game,
because in our engine the interference is not just blocking — it is damage.**
Three measured engine facts stack:

1. **A gunner's line is blocked by our own bots and buildings** (s23 probe,
   `docs/research/turret-line-blocking-2026-08-09.md`; the gunner was the
   positive control and `can_fire_from` flipped **True → False** with a friendly
   barrier in the lane). **Every barrier we plant on the enemy's spawn ring is a
   permanent blank spot in one of our own gunner lanes**, and 83.8% of the home
   turret deaths we inflict and suffer are gunner-shaped.
2. **Turret fire hits whatever unit stands on the target tile, own team
   included** — verified in our own replays, not inferred
   (`docs/research/builder-death-attribution-2026-08-09.md`, and the toolkit's
   validated case: our own gunner #50 shot our own builder bot #3 on **rounds
   62-89, 13 hits, 56 damage, killing it**, because the bot was standing on an
   enemy conveyor tile in the lane). A besieging builder that steps into our own
   turret's line does not merely block it — **it eats the shot and the ammo.**
3. **Our builders must be orthogonally adjacent to act.** Every ring tile we fill
   with a barrier is a tile our own healer, our own attacker and our own follow-up
   builder can no longer stand on. A sealed 12-tile ring seals *us* out of the
   core's orthogonals too — and the 8 orthogonals are the only tiles the core can
   be healed from or delivered into.

**The exception, and it is the one that matters for the 250-round programme:**
a **sentinel's** line passes straight through friendly entities and does not harm
them (s23 probe: 18 damage landed through a friendly bot *and* a friendly
barrier). So **a blockade is compatible with a sentinel siege and incompatible
with a gunner siege.** That is a doctrine-level split, not a tuning detail.

WHAT WOULD KILL IT — this is a premortem, so what "kills" it is evidence the
interference does not bind:

- If a Loki siege is **sentinel-only** by construction, fact 1 never fires and
  this file only costs a comment. [[sentinel-file-stacking]] already establishes
  the sentinel file is legal; this is the reason to prefer it.
- If our blockade objects are placed on the **diagonal** ring tiles only (4 of
  the 12), they block spawns without occupying any of the 8 orthogonals our own
  builders need — a cheap partial that keeps our access. **Untested, and it is
  the most interesting unexplored geometry in the family.**
- Rotation (the 4 Musketeers answer) is unavailable to us for barriers — a
  barrier cannot move. It *is* available for bodies, at 30 Ti and +20% each
  ([[minimum-cost-blockading-body]]).

BUILDER HOOK — **one guard, written before the first blockade plank, not after:**
before placing any denial object, reject the tile if it lies in
`get_attackable_tiles_from(pos, dir, GUNNER)` of one of **our own** standing
gunners. That is a pure-function check against turrets we already track, costs no
store slot and no map table, and it is exactly the code 3 Musketeers and 4
Musketeers both had to retrofit under tournament pressure.

Related: [[minimum-cost-blockading-body]] · [[press-them-onto-their-own-spawn]] ·
[[spawn-smothering]] · [[gunner-line-blinding]] · [[sentinel-file-stacking]] ·
[turret line blocking probe](../turret-line-blocking-2026-08-09.md)
