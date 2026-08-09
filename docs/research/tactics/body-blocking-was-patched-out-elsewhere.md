---
tactic: Body-blocking construction is strong enough that Screeps patched it out — and our engine has no such patch
source: https://blog.screeps.com/2018/12/changelog-2018-12-14/
origin: Screeps (official changelog 2018-12-14), the official forum thread that preceded it, and the community wiki's statement of design intent
evidence: documented
transfers: yes
---

WHAT IT IS — **a ban is the strongest evidence a tactic worked, and this is a
ban.** In Screeps, standing a hostile creep on a tile prevented the owner
building there. Players used it against opponents who were in *safe mode* — the
game's invulnerability state — so a defender who could not be attacked still
could not rebuild. The official forum thread reporting it:

> *"In this replay you can see that I am in safe mode...and the enemy creeps do
> block my miner.They also block my carrier."*

and a top player's reply naming the scale of it in a competitive setting:

> *"they can also block construction sites, was a big issue in the beginning of
> the latest bot arena"*

The developers then removed the interaction. Official changelog, 2018-12-14:

> *"Hostile creeps don’t block building in safe moded rooms."*

The community wiki states the design intent behind safe mode in exactly these
terms — enemy bodies are made non-solid **specifically** so they cannot be used
as terrain:

> *"makes all enemy creeps unable to attack you and your structures as well as
> making them walkable, so they can not block access to parts of your base, or
> the exit"*

Screeps also hard-codes an anti-sealing rule into map geometry:

> *"your new walls may be built not closer than 2 squares to the room edges, and
> hostile creeps will still be able to enter the room and destroy your
> fortifications"*

*(docs.screeps.com/defense.html)*

**Two separate rules, both existing for no reason other than to stop players
sealing each other in.**

WHY IT MIGHT TRANSFER — **because our engine contains the un-patched version of
both rules, and we have measured it happening.**

| the rule Screeps added | our engine |
|---|---|
| enemy bodies become walkable in safe mode | **no safe mode exists**; a tile holding a builder bot is unbuildable by anyone, always — s24 probe `bots/_probe_prison`: `can_build_barrier = False` on a tile holding a standing bot even where `is_tile_empty = True` |
| walls may not be built within 2 tiles of the room edge | **no placement restriction of any kind** beyond orthogonal adjacency and tile emptiness — a chokepoint or a spawn ring may be sealed completely |
| enemy creeps can always enter and break fortifications | our barriers can only be removed at **2 damage for 2 Ti** by a builder, or by turret ammo; **`destroy()` is allied-only** |

And the exploit Screeps banned is already being run against us. Albert And
Einstein's launcher-thrown scout sits inside **our** core's 12-tile spawn ring
from turn 6-27 for **440/449 (98%), 628/641 (98%) and 163/169 (96%)** of turns in
three of five games (`docs/opponents.md:110-125`). Our own model note calls the
consequence plainly: *"one enemy body in the spawn ring paralyses a bot with no
answer to it, for free"* (`docs/game-model.md:306`).

**The decision-relevant reading is that this is not an exotic idea we would be
pioneering.** A different league found body-blocking strong enough to legislate
against, a top player called it *"a big issue"* in a bot arena, and a rated
opponent in *our* league runs it against us in nearly every game. What we do not
do is run it back.

WHAT WOULD KILL IT — 

1. **Screeps creeps are cheap and ours are not.** A blocking body there is a
   few hundred energy; ours is **30 Ti at +20% scale**. This is the argument for
   using **barriers** as the blocking material wherever the tile is vacant
   ([[minimum-cost-blockading-body]]) and bodies only where it is not.
2. **Our organisers may patch it too.** Battlecode added passive HQ-radius damage
   in 2023 specifically against enveloping. **Anything built on this should be a
   behaviour we can switch off, not a chassis we cannot un-build.**
3. **The blockade cuts both ways.** Sealing tiles blanks our own gunner lanes and
   removes our own builders' adjacency seats — [[the-blockade-blanks-your-own-guns]]
   is the premortem and should be read as part of this file, not after it.
4. **This is evidence of strength, not a design.** Screeps' arena is
   persistent-world and asynchronous; ours is a 1000-round match. **The ban tells
   us the mechanic matters; it does not tell us the seal is affordable inside
   250 rounds.** That number has to come from us.

BUILDER HOOK — **the cheapest decisive measurement in this family, and it is a
probe not a battery:** park one of our builder bots on a tile of the *enemy*
core's 12-tile spawn ring in a local game and read their core's spawn events.
`can_spawn` requires **passable, not empty** (`docs/tooling.md:220`, `:246`), so
the prediction is that the tile becomes unspawnable for them while our body
stands there. If that holds, the full seal is priced at ~12 objects and the
question becomes purely one of delivery.

Related: [[minimum-cost-blockading-body]] · [[press-them-onto-their-own-spawn]] ·
[[spawn-smothering]] · [[the-blockade-blanks-your-own-guns]] ·
[[pin-against-terrain]]
