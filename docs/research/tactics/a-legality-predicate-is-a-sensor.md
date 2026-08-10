---
tactic: A can_*() legality predicate is a sensor — query it for information the vision API refuses to give
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 / cout for clout (credited in-text to teammate Chenyx)
evidence: documented (the source technique) / inference (the transfer, from our own API docs and this repo's 2026-08-08 vision measurement)
transfers: partial
---
WHAT IT IS — **The inverse of deception: instead of feeding the opponent a false percept, mine
the engine's own legality checks for a true one it never meant to give you.** cout for clout
needed to know whether an enemy was standing on their spawn pad — information that normally
costs a unit parked there permanently:

> *"to keep track of whether your flag was under attack using the rc.canSpawn() command. This
> can directly be exploited to detect if there's a duck on your spawn pad."*

> *"By keeping one duck permanently unspawned, and having other ducks communicate if they are
> stepping on the spawnpad, we can "magically" spawn reinforcements as soon as an enemy steps on
> our spawn pad."*

(Referents: *"your flag"* and *"our spawn pad"* are cout for clout's own; the *"duck"* detected
is an enemy one; the *"one duck permanently unspawned"* is the reserve whose `canSpawn` return
value is the sensor. The teammate's own units on the pad are excluded by the comms step, which is
what makes the residual `false` mean *enemy*.) **The predicate returns false for a reason, and
the reason is the reading.** The cost was one held-back unit instead of three parked ones, and
the postmortem prices that in Lanchester terms rather than in wins — **no measurement of the
resulting win-rate is given.**

WHY IT MIGHT TRANSFER — **the general form is exactly the kind of thing our programme wants
(free information, no unit committed), and our Controller is dense with `can_*` predicates.**
But the obvious version is already dead here, and it is worth writing down *why* so nobody
re-derives it.

**Killed:** the three tile getters do not fail informatively. This repo measured on 2026-08-08
(`docs/game-model.md`) that `get_tile_env()`, `is_tile_passable()` and `get_tile_building_id()`
**raise `GameError: Position out of vision range`** for an in-bounds tile the caller cannot see —
*"with the identical message as a genuinely off-map position, so the engine does not let you tell
the two apart."* A raise that is triggered purely by distance carries **zero** bits about
occupancy, and an uncaught `GameError` permanently destroys the unit. So the naive probe is not
merely uninformative, it is a landmine.

**Also killed:** the direct analogues of cout for clout's own trick. `can_spawn(position)` is
core-only over the action radius r²=8, which sits entirely inside the core's r²=36 vision.
`can_build_*()` requires an orthogonally adjacent tile. `can_fire(target)` is bounded by an
attack radius that equals the turret's vision radius for all three turret types (gunner 13,
sentinel 32, launcher 26). **None of these can see past what the unit already sees.**

**Not yet killed — and this is the whole reason the file exists.** Two predicates are documented
as reasoning about the map rather than about the caller:

- `can_fire_from(position, direction, turret_type, target)` — the official reference says it
  *"Uses current map occupancy/walls but ignores ammo and cooldown"* (`docs/reference/official-docs.md:437`).
  It is a **hypothetical** turret at an arbitrary `position`. A gunner's shot is blocked by
  obstacles; a sentinel's is not. **If this predicate answers for a `position`/`target` pair the
  caller cannot see, then the difference between a hypothetical-gunner and a
  hypothetical-sentinel query along the same line is a remote occupancy bit — a free, unit-free,
  ammo-free probe of ground we have no eyes on.**
- `can_launch(bot_pos, target)` — the reference requires `target` to be *"within throw range,
  bot-passable"* (`:446`). Whether it raises or returns `False` for an unseen target tile is
  unknown.

WHAT WOULD KILL IT — **one probe, and the likely outcome is that it dies.** The engine most
probably gates these on vision the same way it gates the tile getters, in which case the whole
idea is worth exactly the ten minutes it takes to find out. Two further ways it dies even if the
leak is real: (i) the information may be strictly inside what a sentinel at r²=32 already sees,
making it redundant on our map sizes (8x8 to 30x30); (ii) it is priced in *information*, and the
programme's currencies are core_kill_share and time_to_core_kill — **a leak only counts if it
changes where we send builders, not if it merely makes the bot better informed.**

BUILDER HOOK — a `bots/_probe_*` in the style of `_probe_scale`, ~20 lines, no arena time:
call `can_fire_from()` with a hypothetical GUNNER at a position far outside the caller's vision,
against a target behind a known wall, and the same call with SENTINEL. Record three outcomes per
call: raises `GameError`, returns `False`, returns `True`. **If it raises, close this file
permanently.** If it returns and the gunner/sentinel answers differ across a wall we planted, we
have a remote sensor and the follow-up question is whether it sees *units* or only *terrain* —
plant a builder bot on an otherwise clear line and re-run. Wrap every call in `try/except
GameError`: the failure mode being probed is the one that permanently destroys the probing unit.
