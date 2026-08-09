---
tactic: What actually decided cheap-many vs expensive-few in two Battlecode seasons — the SIZE OF THE LUMP, under a snowball, and not range
source: https://battlecode.org/assets/files/postmortem-2022-5-musketeers.pdf
origin: Battlecode 2022, 5 Musketeers; corroborated three years later by Battlecode 2025, The Kragle
evidence: documented
transfers: partial
---

## WHAT IT IS

BC2022 offered exactly the choice this sweep is about: **soldiers** (cheap, many) against
**watchtowers** (expensive, tougher, higher damage). 5 Musketeers describe the two in the
same breath — soldiers *"have relatively small health and damage amounts, but they are
half the cost of a watchtower"*, while *"Watchtowers have more health and damage than
soldiers. A more expensive choice for combat, they are buff and tough, ready to defend
from large swarms of enemies."*

**The league's verdict was total, and it was not about range or damage:**

> *"no teams built any labs or sages, and very few teams built watchtowers. The games
> were won and lost with soldiers."*

The organisers then cut the prices, and it still did not move:

> *"It still wasn't worth it to build anything expensive."*

**Three years later a different team, reasoning about a different season, named the
mechanism independently.** The Kragle (BC2025):

> *"In 2022, watchtowers were weak since they were a large investment, which was a death
> sentence in that year's game since cheap units could snowball very quickly."*

**The deciding variable, as stated by both sources, is the SIZE OF THE COMMITTED LUMP
under a snowballing dynamic — not range, not damage, not upkeep, not line of sight.**
The expensive option loses because while you are paying for it you are behind, and being
behind compounds.

## THE CONDITIONAL THAT COMES WITH IT — and it is the more useful half

The same postmortem records where the expensive option *did* win:

> *"On small, high lead maps, watchtowers were vicious. Maxwell made the watchtowers into
> a checkerboard formation, and then later the watchtowers would rush the enemy as if
> they were soldiers."*

**Small map + rich map = the lump becomes affordable and the snowball has less room to
run.** This is the same map-conditioned shape wololo found in BC2021 and that sweep 7
matched to our own width curve. The formation named — *checkerboard* — is a spacing rule
for massed static structures, and it is the only one in this sweep's Battlecode reading
other than The High Ground's `d² ≥ 8`.

## WHY IT MIGHT TRANSFER — against our ruleset

**Our lumps are small, and that is the reason to be careful importing this.** A gunner is
20 Ti and a sentinel 30 Ti against a 500 Ti opening bank and 2.5 Ti/round passive income.
Nothing we can build is a "large investment" on the BC2022 scale (a watchtower was twice
a soldier; our sentinel is 1.5× a gunner and 1.0× a builder bot). **So the BC2022 result
should NOT be read as "avoid sentinels".**

**What does transfer is the snowball precondition, and we should check whether we have
it.** The lump only kills you if being behind compounds. Our engine's compounding
channels are: the single global cost scale (falling behind on economy makes *everything*
dearer), the ≤1 builder-spawn per turn rate cap, and the fact that a destroyed entity
refunds its scale contribution to the *owner* — so killing their builder makes their next
builder cheaper (already filed, sweep 6). **Our snowball is weak and partly
self-cancelling.** That is an argument that lump-aversion should bind *less* here than it
did in BC2022 — which points toward the sentinel, not away.

**And the map conditional transfers directly and is already half-built:** our own
measured win rate is 47.5% wide / 33.6% hive against better numbers narrow. BC2022's
"small, high-lead maps" is the same cell where the expensive static option paid.

## WHAT WOULD KILL IT

- **BC2022 watchtowers could MOVE.** The same postmortem says *"Their ability to move
  means you can surround and close in on an enemy as well"*, and describes them rushing
  *"as if they were soldiers"*. That is a materially different object from an immobile
  emplacement, and it weakens the analogy in the direction of making watchtowers *better*
  than our turrets, not worse. **Do not cite BC2022 watchtowers as pure static defence.**
- The Kragle quote is a **retrospective by a different team about a season they did not
  play in that postmortem** — it corroborates the mechanism's *statement*, not
  independently the *measurement*.
- BC2022's snowball came from cheap units killing units for resources; our builder bots
  **cannot attack enemy builder bots at all**, so the most direct snowball channel of
  that season does not exist here.

## BUILDER HOOK

None as a build change. The usable form is a **guard on our own reasoning**: before any
"go cheaper" proposal, state which compounding channel makes the lump expensive here and
what its measured magnitude is. If no channel can be named, the BC2022 result is not
evidence for the proposal. The one measurement that would make this concrete is the
elasticity of our own global scale factor — how much dearer, in titanium, our median game
gets per turret built.
