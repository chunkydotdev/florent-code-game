---
tactic: Cap the expensive emplacement at a hard count, and gate each one on choke geometry
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025, Just Woke Up (winners)
evidence: documented
transfers: yes
---

## WHAT IT IS

BC2025's winners fielded the season's expensive long-range static structure — the
**defense tower**, which SPAARK's postmortem describes as *"Defense tower: has longer
range and better attack damage"* (verified verbatim, `2025-spaark`) — under a rule with
**three simultaneous conjunctive conditions, one of which is a hard count cap of two**:

> *"we have less than 2 defense towers, the tower was in a choke point, determined by the
> fact that it had at least 1 wall on two opposite sides of the tower, and finally that
> the ruin was within 50 units squared of the center of the map"*

They are candid that the constants are not principled: *"These conditions might sound
kind of arbitrary, and they were, but that's what seemed to work best for us."*

**Two things make this the sharpest available answer to "how did strong competitors
weight few-expensive against many-cheap".** First, the field's baseline was **zero**:
*"Up to this point very few of the top teams used defense towers."* Second, the winner's
own answer was not "more" or "fewer" — it was **a small integer plus a geometry
predicate**. The count and the siting rule are the same decision.

**The choke test is the buildable part and it is trivially cheap:** *at least 1 wall on
two opposite sides of the tower.* That is a two-lookup local test, not a pathfinding
analysis, not a fitted map table.

## WHY IT MIGHT TRANSFER — against our ruleset

**The wall-pair test is directly implementable and costs almost nothing.** For a
candidate tile `p` and a facing axis, check `get_tile_env(p.add(NORTH)) == WALL and
get_tile_env(p.add(SOUTH)) == WALL` (and the E/W pair). Two `get_tile_env` calls per
axis, inside a 10 ms budget that we currently spend on much worse things.

**And the reason the test is worth more here than it was there is our gunner's blocking
rule.** A gunner's line *"stops at the first targetable tile (a builder bot or a
building) in its facing direction; empty tiles don't block it, but walls do"*
(`docs/reference/official-docs.md:242`). A corridor with walls on both flanks is exactly
the geometry in which a gunner's single-tile ray is not a weakness: **everything that
wants to reach the thing behind the gunner has to walk down the one line the gunner is
already pointing at.** The wall-pair predicate is a *gunner* siting rule in our ruleset
even though it was a *long-range tower* siting rule in theirs.

**The count cap transfers for a different reason than it did for them.** Ours is not a
scarcity of sites but the single global cost scale: each gunner or sentinel adds a flat
**+0.20** to the team-wide scale factor that multiplies **every** subsequent build cost
(`docs/game-model.md:393-402`, marked measured). Six of them doubles the price of our
economy. A hard cap is the cheapest possible expression of that.

**The distance-to-centre clause has a direct analogue and it points the opposite way
from our habit.** Theirs required the site be *near the map centre* — forward, contested
ground. Ours would be distance-to-*enemy-core*, and sweep 8 already found four
independent winners encoding forward-ness as **positive** with survival absent as a term.

## WHAT WOULD KILL IT

- **The cap number is theirs, not ours, and they say so.** `2` was tuned against BC2025's
  economy and map pool; it is not a transferable constant. What transfers is *that a cap
  existed and was small*, and that it was conjoined with a geometry test.
- **Our maps are 8x8 to 30x30 and symmetric; wall density is not guaranteed.** On an open
  map the wall-pair predicate may match zero tiles, in which case this rule builds
  nothing — which is a *behaviour*, not a bug, but it needs a stated fallback.
- **Confound, stated plainly:** BC2025 defense towers produced no economy while the cheap
  towers did, so "few defense towers" there is partly an economic decision. Our gunners
  and sentinels both produce nothing, so the economic half of their tradeoff does not
  exist here. **Do not import their ratio; import their *shape*.**
- The same postmortem's A/B result is already filed in
  [`../tactics/2026-08-09-sweep-7.md`](2026-08-09-sweep-7.md) — the defense-tower change
  **lost in self-play and won in the field**. That is a warning that this rule cannot be
  scored on a self-leg.

## BUILDER HOOK

The smallest test: a turret-siting predicate that requires a wall pair on one axis and
counts existing turrets of that type, refusing the build above a small cap `N`. Then the
measurement that decides whether it is worth keeping — **what fraction of our turret
builds currently sit on a tile with a wall pair on the firing axis?** If that fraction is
near zero, we have never once sited a turret on the geometry the winner required, and the
cheap version of this experiment is to make it non-zero before tuning any cap.
