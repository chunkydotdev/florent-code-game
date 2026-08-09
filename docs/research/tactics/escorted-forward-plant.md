---
tactic: The escorted forward plant — the turret is the anchor, the screen is the tactic
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (4th place), describing the field-wide "rush/turtle" archetype and the team Kryptonite
evidence: documented
transfers: partial
---

WHAT IT IS — Battlecode 2020's dominant early archetype **was literally this**:
walk a worker into the enemy base and build an offensive structure there. The
High Ground's taxonomy of the Sprint meta names it first:

> "Rush/turtle: Run a miner to the opponent's HQ, build a Design School and
> perhaps Net Gun, then bury the opponent's HQ with landscapers (See Figure 1.)."

The Net Gun is BC2020's immobile turret; the Design School is a forward
*production* building. So the plant was not one structure but a beachhead.

**The decisive detail is not the plant — it is what the planter did next.** THG
describe losing to it, and the mechanism they name is the screen, not the gun:

> "Kryptonite prioritized surrounding their own net gun over destroying our HQ,
> which often led to extended standoffs as we were unable to build drones and
> unable to bury their net gun."

THG's own siting discipline confirms the same asymmetry from the other side.
They ran hard placement constraints at home — net guns "at least 8 distance
squared away from each other", and "we would only build net guns in the
“corners” of the space inside our wall" — and then **suspended those
constraints near the enemy**: "we love offensive net guns".

**The canonical statement of why anyone does this is StarCraft's**, and it names
two payoffs, only one of which is about fighting. Liquipedia:

> "There are two main reasons why proxies are useful. First, proxies allow your
> attacking units to be built closer to the enemy, which will cut down on rush
> time and allow you to reinforce your army more quickly. Second, if placed
> correctly, proxies are unlikely to be scouted by the enemy, and this may give
> the player the element of surprise."

*(liquipedia.net/starcraft2/Proxy — community wiki.)* And the escort idea has an
even harder StarCraft form, where the planter **denies the removal instead of
fighting it**:

> "A typical adaptation of the Cannon Rush is to use [[Pylon]]s to completely
> wall off Cannons behind the mineral line. […] The idea is to make it impossible
> for the defending player to attack the Cannons with workers or melee units,
> while being able to completely deny mining in the main."

*(raw wikitext, brackets as in source.)* **Kryptonite's screen and the pylon wall
are the same move in two leagues**: the plant is made unremovable before it is
made dangerous.

WHY IT MIGHT TRANSFER — **because it is already being done to us, and it is our
largest single measured leak.** From `builder-death-attribution-2026-08-09.md`:
**65.3% of all our home builder deaths are an enemy gunner standing inside
d²≤32 of our own core**, median shooter→our-core d² = 20 (p25 13, p75 29). From
`gunner-plant-tiles-are-not-enumerable-2026-08-09.md`: **41.4% of enemy turrets
planted inside our band survive to the end of the game**, while the other 58.6%
die with a median lifetime of 14 rounds. That bimodality *is* Kryptonite's
standoff — a plant is either cleaned up almost at once or never.

The read-across for our own offence is narrower but real. **The forward road is
closed for us on four instruments — and every one of those instruments measured
an UNESCORTED plant.** Our own turrets planted in the enemy band die at 65.1%
with a 12-round median, i.e. *worse* than theirs die in ours. Kryptonite's claim
is that the forward turret is worth more as a garrison anchor than as a weapon,
and that the escort is what converts one into the other. **The escort is the
variable our refutation never manipulated.**

WHAT WOULD KILL IT — as an offensive change for us, several things, and they
are decisive enough that I am not proposing it:

1. The four-instrument refutation is about *outcomes*, and outcomes already
   integrate over whatever escorting we happened to do. This file offers a
   mechanism, not a reversal.
2. Our builder bots cannot damage enemy builder bots — but neither can theirs
   damage ours. An escort detail is only removable by turrets, which are
   immovable and were sited **before** the plant. That cuts symmetrically, and
   we are the side with the measured home-defence advantage (+11.4 / +16.6 /
   +22.3pp), i.e. the side with more to lose by leaving home.
3. `MAX_TEAM_UNITS = 50` and +20% scale per gunner/builder: an escorted plant is
   one gunner plus two or three builders committed away from home for the rest
   of the match.
4. **In StarCraft the plant is DISPOSABLE and here it is not.** Liquipedia's
   attacker discipline is "any that are near death should be cancelled to recoup
   75% of the mineral cost of construction", and Jay Scott names a whole cheap
   class — "low-cost harassment cannon rushes to cause distraction and delay
   (think 1 pylon and 1 cannon in a hard-to-hit location; the cannon can even be
   canceled before it finishes depending on what happens)". **We have no cancel
   and no refund**, and a built gunner raises our gunner scale by 20%
   permanently unless it dies. The cheap throwaway version of this tactic — the
   version most of the source material is actually about — **does not exist under
   our rules.**

**A note on why any of this is possible here at all.** Other leagues close the
question by *rule*. Screeps' `Room.createConstructionSite` returns
`ERR_NOT_OWNER | -1 | The room is claimed or reserved by a hostile player.`
(docs.screeps.com/api) — you cannot build in someone else's room, and mere
reservation suffices. Our ruleset has **no territorial build restriction of any
kind**, which is exactly why **6,515 enemy turret plants** (5,027 gunner, 1,380
sentinel, 108 launcher) are recorded inside our home band. The absence of that rule is the whole topic.

BUILDER HOOK — **none as an offensive change.** The usable half is a
measurement, and it is the same one [[sustained-plant-removal-race]] needs, so
it pays for two files at once:

> For each of the 6,407 enemy gunner/sentinel plants inside our home band, count enemy
> builder bots **orthogonally adjacent to the planted turret** in the 20 rounds
> following the plant, and cross that against membership in the **41.4%
> survive-to-end tail**. If escort predicts survival, denial and interdiction are
> correctly priced above removal; if it does not, the whole defensive half of
> this sweep is aimed at the wrong mechanism.

Feasibility caveat, stated rather than assumed: the corpus carries plants and
deaths as first-class rows, but **per-round enemy positions are not in the
corpus** (this is the same limit that forced sweep 3 to proxy intrusion by death
location). This measurement may need the replay tape, not the corpus.

Related: [[sustained-plant-removal-race]] · [[gunner-line-blinding]] ·
[[turret-threat-field]] · [[preemptive-escort-turret-premortem]] ·
[gunner plants are not enumerable](../gunner-plant-tiles-are-not-enumerable-2026-08-09.md)
