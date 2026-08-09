---
tactic: Self-suffocation — press them home until their OWN bodies block their OWN spawn ring
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 Cout for Clout (final-tournament series vs Gopher); mechanism corroborated by Battlecode 2021 3 Musketeers
evidence: documented
transfers: partial
---

WHAT IT IS — **you do not have to seal the enemy's spawn ring yourself; you can
make their own units seal it for you.** Cout for Clout lost a tournament game to
exactly this and wrote it up as the mechanism, not as bad luck:

> *"Sometimes we would win due to better micro, but sometimes our less aggressive
> micro would just be pushed so far back to spawn that we ended up blocking our
> own spawn, and suffocating."*

and the specific series position:

> *"Gopher (brown)’s ducks were surrounding our spawn, thus forcing our ducks onto
> our own spawn, and blocking our own spawn."*

They also name the feedback loop that makes it self-reinforcing — their own
targeting sent *more* units into the jam:

> *"our ducks prioritize spawning from spawn zones with a lot of enemy ducks"*

The attacker spends nothing on the blockade. The blockade is made of the
defender's own bodies, delivered by the defender's own retreat logic.

WHY IT MIGHT TRANSFER — **because the two engine facts it needs are both measured
in our engine, and one of them is measured on the receiving end.**

1. **`can_spawn` requires the tile to be PASSABLE, not merely EMPTY**
   (`docs/tooling.md:220`, `:246`), and **builder bots are mutually impassable**
   (`docs/game-model.md:305`). So a builder bot standing on a core spawn tile
   blocks that tile **for its own team**. Their retreating builder is a spawn
   block they built for us.
2. **The ring is exactly 12 tiles** — `CORE_SPAWNING_RADIUS_SQ = 2`, the
   Chebyshev-1 ring, verified tile-by-tile with `can_spawn()` on 2026-08-06
   (`bots/probe_spawn`, `docs/game-model.md:192-197`). Twelve is small. The core
   spawns **at most one builder per turn**, so builder production is
   rate-limited by *turns*, and every ring tile removed narrows the aperture on
   the one input they cannot buy.

**And the field already runs the one-body version of this against us.** Albert
And Einstein (rated ~1307) throw their own turn-1 scout with a launcher and camp
it inside **our** core's 12-tile spawn ring by turn 6-27, holding it for
**440/449 (98%), 628/641 (98%), 163/169 (96%)** of turns in three of five games
(`docs/opponents.md:110-125`, `:424`). Our own note on that says the quiet part:

> *"one enemy body in the spawn ring paralyses a bot with no answer to it, for
> free"* (`docs/game-model.md:306`)

We have been the defender in this pattern for the whole project and have never
run it as an attack.

**AND THE BUILDER ARM'S OWN PROBE MAKES THE TRADE FORCED, NOT INCIDENTAL.** The
s24 imprisonment probe (2026-08-09 08:52, `bots/_probe_prison`) established that
**a tile holding a builder bot is unbuildable** — `is_tile_empty = True` but
`can_build_barrier = False` — and drew the defensive corollary explicitly:
*"parking a builder on a ring tile makes that tile UNBUILDABLE, and parking IS a
complete defence against spawn-lock"*, concluding that **"anyone attempting a
spawn-lock against a defended core will fail"**.

**Read that alongside `can_spawn` requiring PASSABLE: the only known defence
against a spawn-lock is a form of self-suffocation.** To stop us barriering a
ring tile, they must stand a body on it — and their own body on their own ring
tile is exactly the object BC2024 says suffocated Cout for Clout. **A defender
cannot deny us the tile and keep the tile.** That converts this file from "a
thing that might happen under pressure" into "the price of the only counter to
the tactic next door", and it is why [[spawn-smothering]] and this file should be
read as one proposition rather than two.

**One link in that chain is a prediction, not a measurement, and it is the whole
file:** the probe measured *buildability* under a friendly body, not
*spawnability*. Whether `can_spawn` returns False on a ring tile holding the
core's **own** builder is untested. See the hook.

**The BC2021 3 Musketeers half completes the picture** — they ran the deliberate
version *and* documented the defender's answer:

> *"When a muckraker found an enemy EC, it simply sat there, hoping to get some
> neighboring muckrakers to build a wall around the enemy EC, blocking it in."*

and the counter they had to build for themselves:

> *"a state called REMOVING BLOCKAGE, where if we have more than 6 enemies in the
> surrounding squares of our EC, we build a politician that immediately empowers,
> in order to clear the build spots for our EC"*

i.e. **the field's answer to a body-blockade was to blow up its own doorway.**
That answer does not exist here: `destroy()` is allied-only, our builder attack
cannot damage a builder bot at all, and `self_destruct()` deals no explosion
damage. **A defender who lets bodies into its ring in our engine has strictly
fewer outs than a Battlecode 2021 defender did.**

WHAT WOULD KILL IT — four things, in order of how likely they are to fire:

1. **Their builders may simply walk out.** Their body on their own ring tile
   blocks it only while it stands there, and it is *their* unit under *their*
   control with a move cooldown of its own. Cout for Clout's case needed the
   defender to be pinned by pressure it could not disengage from. **Our
   measured position is that our raiders live ~6 rounds in enemy territory after
   r150** — we may not be able to generate that pressure at all past the
   opening.
2. **One tile is not a lock.** Twelve tiles means a partial jam only lowers the
   probability that a spawn is legal on the turn they want it; it does not stop
   production. The BC2024 case was catastrophic because *many* units were pushed
   home at once. We should not sell a single squatter as a spawn lock.
3. **The feedback loop is theirs, not ours.** Cout for Clout suffocated partly
   because *their own targeting* fed the jam. We have no evidence any opponent
   here has a retreat-toward-core rule; if their builders route around the ring,
   the loop never closes.
4. **We are the ones who bleed from this today.** Any work here should first
   ask whether the *defensive* fix (never let a body sit in our ring; a launcher
   throw is 0 Ti and 0 ammo — [[launcher-defensive-interception]]) is worth more
   than the offensive version, given we lose 96-98%-of-game camps in real games.

BUILDER HOOK — **first, one boolean that the existing probe was two lines away
from answering:** park a friendly builder on one of our own core's 12 ring tiles
and read `can_spawn` on that tile. `False` ⇒ the self-suffocation mechanism is
real in this engine and the defender's anti-spawn-lock parking is self-harming.
`True` ⇒ this file is dead and should be marked `transfers: no`. **`bots/_probe_prison`
already does the hard part; this is one extra call.**

Then, **a corpus query before any bot change, and it is cheap.** Per
round, per game, count how many of the **enemy core's 12 ring tiles** are
occupied by an **enemy builder bot** (their own unit), and cross it with whether
their core spawned that turn. Positions are reconstructible from move events the
same way `builder-death-attribution` reconstructs victim tiles.

- If ring self-occupancy is routinely ≥1 in the games we lose, the loop exists in
  this league and pressing them home is a real lever.
- If it is ~0, this file is a Battlecode artefact and should be marked
  `transfers: no` on the evidence.

Related: [[spawn-smothering]] · [[minimum-cost-blockading-body]] ·
[[launcher-defensive-interception]] · [[the-blockade-blanks-your-own-guns]]
