---
tactic: THE ANSWER TO (A) AND (B) — finishing is a separate SKILL with its own predicate and its own production policy, and the bots that reliably convert implement it as a discrete mode switch, not a preference
source: http://satirist.org/ai/starcraft/blog/archives/842-Steamhammer-cant-finish-the-game.html
origin: Steamhammer / Jay Scott (StarCraft AI, SSCAIT/AIIDE); code at https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/StrategyBossZerg.cpp
evidence: documented
transfers: yes
---
WHAT IT IS — The single most on-point source this sweep found, and it is a bot
author writing a whole post about our exact problem. The title is
*"Steamhammer can’t finish the game"* — curly apostrophe in the source; the ASCII
form does not appear on the page. The opening paragraph:

> *"Finishing off the enemy just means destroying all their buildings. It sounds
> simple, but it is a sophisticated skill, and there are a lot of ways to go
> wrong. Steamhammer has a number of special provisions for quickly finding the
> last enemy remnants, but small loopholes persist and occasionally a game slips
> through one."*

And, on its own line in the same post: *"Finishing off the enemy can be hard."*

The named mechanism is a **mode switch on a cheap boolean predicate**:

> *"One of Steamhammer’s special game-finishing skills is that it makes mutalisks
> to chase down the residue of the enemy. The condition is, if the enemy has no
> known bases and no known anti-air units, then Steamhammer will tech to mutalisks
> and make mutas its primary unit. The mutas scout faster than ground units, and
> can find floating buildings and island bases that ground units can’t reach."*

That predicate exists in the source as a named function, and it is four guard
clauses over *remembered* information — no search, no simulation:

```
bool StrategyBossZerg::enemySeemsToBeDead() const
```
with the guards, verbatim as comments in the body, in order:
`// The enemy starting position has not been found.` /
`// The enemy still owns a base.` /
`// The enemy may be able to defeat us on the ground.` /
`// The enemy still has an anti-air unit.` — and on success
`// Enemy has no known bases or anti-air units and appears to have no winning chances.`
Its two consumers in the tech planner are commented
`// Special case: Tech to mutas to finish off the enemy.` and
`// Special case: Make mutas to finish off the enemy.`

And the header comment states the intent, which is the part worth copying:

```
// The enemy is toast, and all we have left to do is to eradicate the surviving enemy buildings.
```

**Did it work?** The author's own verdict, in the same post that catalogues its
failures: *"That is a lot of flaws, and yet Steamhammer rarely fails to finish a
game!"* And a second bot author, krasi0, in the comment thread:
*"To me, finishing the enemy off completely seems like a basic and crucial skill
which makes a bot much more robust."*

WHY IT MIGHT TRANSFER — Three structural properties import cleanly, and none of
them costs CPU we do not have.

**1. The predicate is over remembered facts, not a search.** Ours would be the
direct analogue: enemy core located, enemy harvester count zero (or below a
threshold), our committed damage in place, no enemy turret bearing on the
approach. Every one of those is already readable — `get_nearby_buildings`,
`get_entity_type`, `can_fire_from` — and all four fit in the 16-slot store as a
single flag written by whichever unit can see the answer.

**2. The switch REPLACES the production policy rather than competing with it.**
This is the part our bot does not do. Our damage assets are bought out of the
same titanium pool, by the same build-priority code, as conveyors and harvesters.
Steamhammer's finisher **short-circuits the whole tech/unit-mix planner to one
unit type**. The transferable version is a build-priority override, not a new
weight.

**3. Steamhammer's documented failure is exactly the failure of a weight.** The
author's post-mortem of the lost game:

> *"In this case, Steamhammer had the wrong unit mix; to make zerglings and
> ultralisks when all enemies were in the air was no good. The mutalisk rule
> should make mutalisks only, not mix them with other units. The scourge might
> have understood that when only floating buildings are left, they are good
> targets."*

Referent: "the mutalisk rule" is the `enemySeemsToBeDead()` switch quoted above;
"the scourge" are Steamhammer's own anti-air suicide units. **A blended policy
produced a bot that was maxed out, could win every fight, and still could not
kill two buildings.** Against our 2.2:1 defensive arithmetic, a blended finisher
is worse than none.

WHAT WOULD KILL IT — Steamhammer's predicate keys on *the enemy having no bases
left* — a state that only exists after you have already won. Our core is present
from round 0 and is the *first* thing you would attack, so the analogous
predicate has to be about **our readiness**, not their collapse, and that is a
much harder thing to get right. This is a real disanalogy and it should not be
smoothed over: their finisher is a mop-up, ours would be an assault.

Second, the author names a cost we cannot pay:
*"In the worst case, Steamhammer would need to be able to destroy some of its own
units to clear supply to make mutalisks to finish off the enemy. And that’s a
high-end skill that I am in no hurry to add."* Our equivalent is destroying our
own conveyors and harvesters to free titanium and unit slots for a finisher —
which would trade directly against tiebreak keys 1 and 2. The abort rule in
[`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)
is the reason that trade is dangerous here in a way it was not for Steamhammer.

BUILDER HOOK — Write `enemy_seems_beatable()` as four booleans over already-read
state, publish it to one store slot, and have exactly one consumer: the build
priority. While the flag is false, nothing changes. While it is true, turret
purchases outrank conveyor purchases unconditionally. That is a single flag and a
single branch, and it is measurable directly as core-kill incidence.
