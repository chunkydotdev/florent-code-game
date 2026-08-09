---
tactic: NEGATIVE — no competitive league in this sweep has friendly units blocking their own side's ranged attack, so there is no doctrine to import
source: https://raw.githubusercontent.com/screeps/engine/master/src/processor/intents/towers/attack.js and https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/game-configs.json
origin: Battlecode 2019-2026 (22 postmortems), Screeps (engine source), Terminal (decompiled engine + starter kit), CodinGame Code Royale (official referee), Lux AI S1/S2, Kaggle Kore, StarCraft/BW & SC2 (Liquipedia), Age of Empires, Factorio, Warcraft III
evidence: documented
transfers: no
---

## WHAT IT IS

Our gunner's shot is blocked by our own bots and buildings; our sentinel's is not. Question
(D) asked where else that exists. **Answer: in none of the competitive leagues this
library draws on.** The negative is worth filing because it bounds what the rest of the
library can tell us about turret formations.

**The evidence, source by source:**

| league | friendly blocking of own fire? | how established |
|---|---|---|
| Battlecode 2019-2026 | **no** | greps over all 22 postmortems for `friendly fire`, `line of sight`, `blocks their own`, `obstruct`, `hitting our own` return nothing on this mechanic |
| Screeps | **no — there is no line-of-sight check at all** | the engine's tower attack path computes only Chebyshev range; docs say a tower *"Can be targeted to any object in the room"* |
| Terminal | **no** | targeting is a rasterised disc with no intervening-tile term; a turret shoots straight through your own walls |
| Code Royale | **no** | the referee's `Tower.act()` picks the nearest enemy creep by distance; no obstruction test exists |
| Lux S1/S2, Kaggle Kore | **vacuous** | no ranged attack mechanic |
| StarCraft/BW, SC2, AoE, WC3, Factorio | **no** | the RTS leg found zero mentions of a friendly unit obstructing a friendly shot across Liquipedia's static-defence, cannon, sunken and turtle articles |

**Everything those canons call "blocking" is one of two other things**, and the
distinction is the point of this file:

- **(ii) friendly-fire SPLASH** — Siege Tank, Lurker, Mangonel, Dwarf Fortress ballista
  arrows (*"Ballista arrows may hit any units in any square that the head passes through"*
  — they pierce and continue, they are not stopped). **Our sentinel's line explicitly does
  not harm friendlies, so we do not have this.**
- **(iii) MOVEMENT blocking** — walling, sim city, creep blocking, Terminal's mazes
  (the Terminal leg's summary of the engine source, not a quotation from Correlation One:
  **your walls block your own units' movement but never your own turrets' fire**),
  Screeps' `OBSTACLE_OBJECT_TYPES` including `"creep"`, Code Royale's collision/shove
  model. **We have this too, and it is a different lever.**

**Our mechanic is (i) only, and (i) alone.** The closest analogue in Battlecode's own
corpus is BC2021's malott fat cats reserving the distance-1 ring around a target for their
strongest units — *"This would guarantee that our units would not obstruct each others
when attacking"* — but the referent there is **positional crowding for an adjacency-capped
attack**, category (iii), not a blocked line. It is filed here so nobody later mistakes it
for a precedent.

## WHY IT MATTERS

**Three consequences, all of them about how to read the rest of this library:**

1. **Every formation, spacing and massing rule imported from those leagues was designed
   under a no-friendly-blocking assumption**, and therefore silently over-states how well
   massing works for our gunners. The High Ground's `d² ≥ 8`, Screeps' tower clustering,
   Terminal's turret lines and BC2022's checkerboard were all written by people whose
   turrets could not blind each other.
2. **The one asymmetry we have is genuinely ours to exploit**, in both directions: our own
   line discipline is a cost nobody else pays, and the enemy's gunners can be blanked by a
   3 Ti barrier — which this library already files as
   [`gunner-line-blinding`](gunner-line-blinding.md) and
   [`the-blockade-blanks-your-own-guns`](the-blockade-blanks-your-own-guns.md).
3. **The two usable layout precedents are outside the competitive canon entirely** —
   Dwarf Fortress's stagger rule and RimWorld's blocking/non-blocking mix, both filed in
   [`stagger-the-file-so-each-gun-clears-the-one-ahead`](stagger-the-file-so-each-gun-clears-the-one-ahead.md).
   That is the whole external supply.

## WHAT WOULD KILL IT

- **The Battlecode limb is absence-of-evidence in prose.** 22 postmortems not mentioning a
  mechanic is weaker than a rules check; the Screeps, Terminal and Code Royale limbs are
  engine-source checks and are strong.
- **Coverage is not exhaustive.** Halite, AI Challenge, and most of CodinGame's catalogue
  were not swept for this. A league with projectile travel (Total Annihilation's lineage
  was raised by the RTS leg, with the mechanic documented but **no formation doctrine
  attached**) could still supply a precedent.
- A negative of this kind gets weaker every time someone searches for it and stops early.
  **What would settle it is a league with an explicitly ray-blocked turret; none was
  found.**

## BUILDER HOOK

None. This is a **library scope note**: on friendly line-blocking we are on our own, and
any layout rule we adopt must be derived from our own probes rather than borrowed. That
is the same bound sweep 15 reached for cause-versus-marker and this sweep reached for
cost scaling in
[`nobody-else-has-a-rising-build-cost`](nobody-else-has-a-rising-build-cost.md) — three
independent questions on which the external library is now known to be silent.
