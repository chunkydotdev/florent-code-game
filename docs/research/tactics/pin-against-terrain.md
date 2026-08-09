---
tactic: Pin against terrain — let the map be three walls of the cell
source: https://superflux.dev/blog/battlesnake-2018
origin: BattleSnake 2018, Kevin Klassen (superflux.dev) — his own competition writeup
evidence: documented (the principle) / inference (our geometry — by tactics sweep 11, this agent)
transfers: partial
---

WHAT IT IS — the same author whose full-encirclement trap this library already
cites reports that he **replaced** it with a cheaper version that leans on the
map:

> *"my snake would wrap around it, trapping it"*

then, the refinement:

> *"instead of surrounding the opponent snake, I would block it against a wall"*

> *"it could keep it against the wall for a long time, starving it"*

**The insight is a cost one: terrain you did not pay for is the cheapest wall in
any game.** A full box costs four sides; a pin against existing geometry costs
one or two.

WHY IT MIGHT TRANSFER — **our engine gives a builder bot only four escape
directions, and two classes of tile are free walls.**

- **Builder bots move in the four cardinal directions only** — `move(<diagonal>)`
  raises and `can_move(<diagonal>)` is False. So a cell is four tiles, never
  eight. [[throw-into-prebuilt-cell]] already prices a full box at **~12 Ti**
  (4 barriers at 3 Ti, +1% scale each).
- **`Environment.WALL` tiles are permanent and free.** A victim standing in a
  1-tile alcove needs **one** barrier, not four. On maps with wall structure this
  is a **4× discount** on the whole imprisonment family.
- **The enemy core's own 2×2 footprint is impassable to everything, including its
  own team** (`docs/game-model.md`). A builder standing on a tile orthogonally
  adjacent to their footprint already has **one or two** of its four exits
  blocked by their own core. Pinning a unit against the enemy's own core is
  cheaper than pinning it anywhere else on the map.
- **Our own barriers cannot be removed cheaply.** `destroy()` is allied-only, so
  the prisoner must chew 30 HP at **2 damage for 2 Ti** — 15 turns and 30 Ti per
  barrier — while a single healer restores **+4 HP for 1 Ti**, beating it 2× on
  rate and 2× on cost simultaneously.

**And the precondition imprisonment needs — a victim that stands still — is
measured in this league.** Albert And Einstein's camper (entity id 3, *never
rotated or replaced*) holds one tile in our spawn ring for **440, 628 and 163
consecutive-ish turns** across three games (`docs/opponents.md:110-125`). A unit
that does not move for four hundred turns can be walled at leisure, one barrier
per turn, by a single builder.

**Why imprison rather than kill:** killing an enemy builder **refunds their +20%
cost-scale contribution and frees one of their 50 unit slots**
([[displace-dont-kill]]). A jailed builder keeps taxing every future builder,
gunner and sentinel they buy, forever.

WHAT WOULD KILL IT — 

1. **BattleSnake's clock does not exist here.** Klassen's pin wins because
   snakes *starve*. **Our prisoner never starves** — it sits at full HP
   indefinitely and can still `heal`, `build` and `attack` any orthogonally
   adjacent tile. **We are not removing the unit; we are removing its mobility.**
   If the tile it is pinned on is a tile it wanted anyway — a spawn-ring seat, an
   ore tile, next to one of our conveyors — **we have jailed it in the place it
   was already attacking from and made things worse.** This is the single
   strongest argument against the tactic and it must be checked per target.
2. **Placement is the real cost, not the barriers.** Each barrier needs our
   builder **orthogonally adjacent to the target tile**, one per turn. A pin
   needing one barrier is one exposed builder-turn; a box is four, and the victim
   may leave in between.
3. **A launcher undoes it in one action.** Their launcher grabs an adjacent
   builder from either team and throws it to any passable tile — **including
   ours, and including out of a cell.** Any prisoner within r²=26 of an enemy
   launcher is on loan, not in jail.
4. **Terrain may not be there.** Map wall density is not uniform across the pool;
   on open maps the discount is zero and this reduces to
   [[throw-into-prebuilt-cell]] at full price.

BUILDER HOOK — **a corpus query, not a build, and it prices the whole family:**
for each enemy builder bot that stands on the same tile for **≥20 consecutive
rounds**, count how many of its four cardinal neighbours are already
`WALL`, an existing building, or enemy-core footprint. The distribution of that
count is the answer:

- mostly **3** ⇒ pins cost 3 Ti and one builder-turn, and this is a real tactic;
- mostly **0** ⇒ every jail is a full 12 Ti box under fire, and the family stays
  where [[throw-into-prebuilt-cell]] left it — gated on the unresolved
  `can_launch`-into-an-enclosed-cell question.

Related: [[throw-into-prebuilt-cell]] · [[displace-dont-kill]] ·
[[body-blocking-was-patched-out-elsewhere]] · [[minimum-cost-blockading-body]] ·
[[ratnapping-ignores-hp]]
