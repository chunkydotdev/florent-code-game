---
tactic: Rushing units FLEE the defensive counter-unit and return when it is gone — do not trade with it
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 / Isaac Liao (wololo)
evidence: documented
transfers: yes
---
WHAT IT IS — One line in wololo's micro section, and it is the difference between
an all-in and a siege:

> *"rushing units fled from defensive politicians as soon as they were built by
> the opponent EC to avoid efficient multiple conversions/removals, and returned
> to bury the EC immediately once these defensive politicians were gone"*

Referent: "rushing units" are his muckrakers; "defensive politicians" are the
units the opponent's Enlightenment Center spawns specifically to clear them;
"these defensive politicians" in the second clause refers to the same units. The
attacker never fights the counter-unit. It waits it out.

WHY IT MIGHT TRANSFER — **Harder here than in the game it came from**, because of
a rule the field appears not to exploit: **a builder bot's attack cannot target
builder bots at all — only buildings.** So the enemy's builder bots are
*structurally incapable* of removing ours. The only thing that can kill our
forward builder is a turret, and turrets are:

- **immobile**, so the threatened set is a fixed, computable region;
- **ammo-gated**, and there is no passive ammo income — a defender at 0 ammo has
  a gunner that cannot fire, and `get_global_ammo()` is not visible for the enemy
  team, but *shots not taken* are observable;
- **facing-dependent** for gunner and sentinel, and a **sentinel cannot rotate at
  all** while a gunner rotation costs 10 Ti plus a full action cooldown.

So "flee and return" is not a chase in our game — it is stepping out of a fixed
line and back into it. The library already holds the raw material: `_bfs_direction`
puts turret tiles in `blocked` with no range or line-of-fire term
(`turret-threat-field.md`), and BC2020's winner maintained a runtime ±1 coverage
field rather than a table (`runtime-density-siting.md`). Retreat-and-return is
what that field is *for*.

WHAT WOULD KILL IT — (a) A **launcher** breaks it: it is facing-independent,
needs no ammo, and picks up an adjacent builder bot from either team and throws
it to any passable tile. Dodging a line does nothing against a grab. `Our games
against Kryptonite depended almost uniquely if our initial drone was able to
repel or capture their rush miner or not` (Java Best Waifu, BC2020) is the same
mechanic deciding a whole matchup — see `one-cheap-interceptor-decides-the-matchup`.
(b) Waiting costs rounds, and rounds are the scarce thing under a 250-round
target; a builder that spends 60 rounds orbiting a gunner has contributed
nothing to either currency. (c) Cardinal-only movement means the cheapest exit
from a diagonal line may be two moves, and moving is mutually exclusive with
acting.

BUILDER HOOK — Add a **line-of-fire term** to the existing turret-tile blocking
in `_bfs_direction`: a tile is dangerous only if a live enemy turret bears on it
given its facing and type (`can_fire_from(position, direction, turret_type,
target)` is the exact predicate the engine already exposes, and it ignores
ammo/cooldown so it is the conservative reading). Today the router blocks turret
tiles; it does not know a sentinel's line is one tile wide. That change alone
converts a blunt avoidance into retreat-and-return, and it is a routing edit, not
a strategy.
