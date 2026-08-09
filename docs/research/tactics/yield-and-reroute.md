---
tactic: Yielding — concede the covered ground and move the thing it threatens
source: http://satirist.org/ai/starcraft/blog/archives/748-cannon-rush-reactions.html
origin: Jay Scott (author of the Steamhammer Brood War bot), "cannon rush reactions", 2019-01-23; corroborated by Liquipedia StarCraft II (community wiki)
evidence: documented
transfers: partial
---

WHAT IT IS — the fifth answer to an enemy structure in your base, and the one
that never appears in a highlight reel: **do not contest the covered tiles at
all.** Jay Scott, writing specifically about bot behaviour against cannon
rushes, states the whole family as a ladder of goals:

> "In defending a cannon rush, you have a series of goals. 1. It's best if you
> can prevent cannons from finishing, or at least hit them while they are few and
> can be defeated efficiently. 2. If the cannons finish, you need to put a brake
> on it so the situation doesn't grow worse. Mitigate the threat. 3. Ultimately,
> you want to restore your freedom of movement or your access to a denied area."

Yielding is how you buy time between rungs 2 and 3, and he gives it as a
positive rule rather than a concession:

> "If the cannons deny something vital, you have to replace it. If you can't mine
> enough because your main mineral line is under attack, expand. If a critical
> building is under attack, you may want to start a replacement before it dies."

with the matching micro rule — **stop feeding the covered ground**:

> "Don't try to mine a mineral patch that is in cannon range; do mine any patches
> that are out of range. Don't try to build a building, or land a floating
> building, in cannon range."

**Terminal has the sharpest version of all, because it is a decision NOT to
rebuild.** Griffin Keglevich, writing up his university team's strategy on
Correlation One's own Medium publication:

> "we don't want to rebuild the attacked wall, since it will inevitably fall
> without mitigating an attack"

> "If this is the case, and there is no path that exists from the enemy to shoot
> pings into our undefended corner, then we will forego the re-building of our
> defence so that we don't give them free cores of damage."

*(medium.com/terminal-player-strategies/the-terminus-of-our-terminal-strategy-19c96da2acf5,
via Wayback — competitor writeup on the official publication.)* **Note the
condition attached**: they yield the ground only after checking that yielding it
does not open a path to something that matters. Yielding is gated, not passive.

Liquipedia records the fully-yielding version as standard for one race:
"Terran can also [[Lift off]] and move production buildings that may be in range
of the Cannons, or even lift their initial [[Command Center]] and move it to
another base so that the Protoss players initial Pylons and Cannons are useless."
*(raw wikitext, brackets as they appear in the source)*

WHY IT MIGHT TRANSFER — **because our win condition rewards throughput, not
ground.** 353 of our games reached round 1000 and we won 57.2% of them, and the
first tiebreak key is **cumulative titanium delivered**. In a game decided on
delivery, a planted gunner that covers a stretch of conveyor is denying
*throughput*, and throughput can be re-routed while ground cannot be cheaply
retaken. A conveyor is 3 Ti at +1% scale — the cheapest re-route in the game,
and far cheaper than the ammo stream [[sustained-plant-removal-race]] prices for
killing the thing.

Three concrete yields exist under our rules, in increasing cost:

| yield | cost | notes |
|---|---|---|
| **spawn away from it** — the core's spawn ring is the 12-tile Chebyshev-1 ring (s23 probe); pick the tile outside the gunner's facing line | **0 Ti** | pure siting, no build |
| **re-route the conveyor run** around the covered tiles | 3 Ti/tile, +1% | delivery is slower but continues |
| **rebuild the threatened building elsewhere before it dies** (Jay Scott's rung) | full cost + scale | only worth it for a harvester feeder, not for the tile |

And the counterpart to "don't mine in cannon range" is already the builder hook
of [[turret-threat-field]] — the two files are the same principle applied to
movement and to economy respectively.

WHAT WOULD KILL IT — and one of these is measured and awkward:

1. **They are planting ON our network, so moving it may just move the target.**
   97.2% of the tiles the enemy plants on are tiles we also build on. A re-route
   that stays inside our band re-offers the same class of tile.
2. **Our core cannot move**, so the deepest yield in the StarCraft playbook
   (lift the Command Center) has no analogue at all. What is threatened most —
   the 2×2 core and the builders healing on its footprint — is exactly what
   cannot relocate.
3. **Harvesters cannot relocate** either: they are legal only on ore tiles, which
   are fixed. Only the path from harvester to core is mobile.
4. On a small map a gunner's r²=13 covers a large fraction of the width — on an
   8×8 map there may simply be no route outside it. Our known width gradient
   (sweep 6: an opening unconditional on map geometry is a documented failure
   mode) says any rule here must be width-conditional.

BUILDER HOOK — **take the free rung first, and measure before buying any other.**

Free rung, zero titanium: when the core spawns a builder, prefer a spawn tile of
the 12 that is **not** in `get_attackable_tiles_from(...)` of any enemy gunner in
the core's r²=36 vision. This is a tie-break inside an action we already take
every turn.

The measurement that decides the rest, and it is a corpus query rather than a
battery: **what fraction of our conveyor tiles sit inside a planted enemy
gunner's attack pattern, and for how many rounds?** If it is small, yielding is
irrelevant to delivery and this file is a filed negative. If it is large, it
explains a delivery deficit we have never attributed, and re-routing is the
cheapest lever in the sweep.

Related: [[turret-threat-field]] · [[sustained-plant-removal-race]] ·
[[standoff-removal-outranging]]
