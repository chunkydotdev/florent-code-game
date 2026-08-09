---
tactic: Spawn smothering — seal the enemy core's spawn ring
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 Wololo (winner); independently Battlecode 2023 4 Musketeers (top seed)
evidence: documented
transfers: partial
---
WHAT IT IS — envelop the enemy base so it physically cannot spawn. Wololo built a
dedicated `burier` role: "completely envelop or 'bury' the opponent's EC in
units, such that it could not spawn units on any tiles", using a **one-tile-thick
layer** (thicker wastes units) and re-recruiting the moment a gap opens.
4 Musketeers: "Launchers... can crowd the HQ and kill anything that spawns, as
well as block most of the spawn locations", and crucially they **rotate around**
the base so departing units leave openings for arrivals.

WHY IT MIGHT TRANSFER — our core spawns at most one builder per turn on a tile
adjacent to its 2x2 footprint, so the legal spawn set is small and fixed.
Barriers are 3 Ti (+1% scale, the cheapest scaling in the game) with 30 HP.
**Verified in the engine type stubs: `destroy()` is ALLIED-ONLY.** So the
defender cannot remove our barrier cheaply — they must attack it at 2 dmg for
2 Ti, i.e. **15 attacks, 30 Ti and 15 builder-turns per 3 Ti barrier**, or spend
turret ammo they are already short of.

WHAT WOULD KILL IT — `can_spawn` legality is engine behaviour we have not
measured; if the core can spawn onto any tile in its r^2=8 action radius rather
than only the 12 footprint-adjacent tiles, the ring is far bigger and the
arithmetic changes. Also Battlecode PATCHED this exact tactic in 2023 by adding
passive damage in the HQ action radius — our spec mentions no such damage, but
our spec has known errors. **Measure the legal spawn set first.**

BUILDER HOOK — one local game against a passive opponent: ring the enemy core
with barriers and count its spawns. Cheap, decisive, no ship required.
