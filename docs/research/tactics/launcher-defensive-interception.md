---
tactic: Defensive interception — the launcher as goalkeeper, not spear
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (4th place); field-wide "drone harass" by week 3
evidence: documented
transfers: yes
---

WHAT IT IS — Battlecode 2020's Delivery Drone is the closest published analogue to
our Launcher that exists: adjacent pickup, **either team**, place on a legal tile,
held unit frozen. The High Ground won a knife-edge series against the top rush team
because *"we happened to pick up and drown their rushing miner right as it was
reaching our base"*, and they name the cost of not doing it: *"Unlike many other
teams, we didn't keep a drone back to defend rushes, which made us weaker vs rush
teams."* By week 3, *"every top team, no matter what their strategy, now had a
drone harass."*

WHY IT MIGHT TRANSFER — **Our ruleset makes this stronger than theirs.** An enemy
builder inside our base can be answered in exactly two ways:

| answer | cost |
|---|---|
| turret fire | 40 HP builder = 3 sentinel shots (30 ammo) or 6 gunner shots (24 ammo) → **24-30 Ti of converted titanium** |
| **launcher throw** | **0 ammo, 0 titanium, facing-independent** |

and our own builder bots **cannot help at all** — a builder's attack hits buildings
only, never enemy builder bots. Crucially the **adjacency comes free**: an enemy
builder attacking one of our buildings *must* be orthogonally adjacent to it, which
is exactly the geometry a launcher needs. We do not have to chase anything.

It also compounds with the cost-scale rule (see [[displace-dont-kill]]): killing
that builder would *refund* their +20% scale and free one of their 50 unit slots.
Throwing it refunds nothing.

**And it points at the band the builder's 09:05 note measures as our single large
advantage — home defence, +11.4 / +16.6 / +22.3pp over the field.** This is the
rare tactic that reinforces a measured strength rather than opening a sixth
doctrine road.

WHAT WOULD KILL IT — If `launch` carries a long action cooldown, one launcher
cannot keep pace with several raiders. If raiders preferentially hit perimeter
buildings far from the launcher, it never gets a grab. Both are measurable before
any build.

BUILDER HOOK — **The smallest test in either sweep.** One launcher orthogonally
adjacent to the core footprint, one rule: *if any enemy builder bot is adjacent,
throw it to the farthest passable tile from our core.* Measure enemy damage dealt
to our core per game against current. No other change.

Prerequisite reads, both cheap and both gating every launcher tactic:
1. Is `can_launch` adjacency 4-way or 8-way?
2. Must the throw target be *reachable*, or merely `is_tile_passable`?
3. Does being thrown alter the thrown bot's action/move cooldown?

Related: [[displace-dont-kill]] · [[throw-into-prebuilt-cell]] ·
[sweep 3](2026-08-09-sweep-3.md)
