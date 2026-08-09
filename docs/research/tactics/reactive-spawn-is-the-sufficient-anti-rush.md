---
tactic: FAILURE MODE — "just make more units when threatened" is the field's standard anti-rush, and it is reported as SUFFICIENT
source: https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf
origin: Battlecode 2026 / lorem ipsum; corroborated by Martin Rooijackers (LetaBot) on the StarCraft AI ladder and by BC2020 Java Best Waifu
evidence: documented
transfers: partial
---
WHAT IT IS — The most recent Battlecode postmortem available (2026) reports the
cheapest possible anti-rush and calls it sufficient against the whole class:

> *"The anti-rush code was essentially most just spawning more rats when in danger
> of the king getting rushed. It may seem trivial, but I found this to be
> sufficient against all rush bots."*

Referent: "rats" are that game's basic unit; "the king" is the base being
defended. He learned it by regression — the code was accidentally deleted:
> *"imagine my surprise when my bot all of a sudden was getting absolutely
> destroyed by some of my rush testing bots"*

**LetaBot** gives the same rule for StarCraft worker rushes, and states the
mechanism:
> *"The main key is to keep on building worker units no matter what."*
> *"with this your production of worker units will be at the same rate as your
> opponent, ensuring that you will always have numerical superiority with which
> you should be able to hold easily"*
Referent: "it", in the preceding sentence *"There are many ways to stop it"*, is
the **worker rush**, which is that section's heading. "with this" = the
keep-building-workers policy. He adds the warning that the *tempting* response is
the wrong one: *"Don't rush for a tier 1 combat unit, that only plays into the hand
of the one that worker rushes you."*

WHY IT MATTERS HERE — **Because in our ruleset the field's standard counter is
rate-capped in a way it is not in any of the source games, and that asymmetry is
the single strongest structural argument in the programme's favour that this
sweep found.**

The core *"spawns ≤1 builder bot/turn on the 12-tile Chebyshev-1 ring"*. There is
no second production building, no parallel factory, and `MAX_TEAM_UNITS = 50`.
A defender who reads a strike and decides to out-produce it can add **at most one
40 HP body per round**, and each one costs +20% more than the last. In BC2026 and
in StarCraft the defender could scale production with money; here they can only
scale it with **turns**, and turns are not purchasable. Sweep 2 already recorded
the same asymmetry from the other side — *"every healer permanently removed costs
them a full core-turn to replace, and a core-turn is not purchasable"* — this file
is the confirmation that the field's default counter is exactly the thing our
engine rate-limits.

WHY IT IS `partial`, NOT `no` — The rate cap does not make the defender helpless,
it changes *which* counter they use. Ours can instead:
- **Heal**, at 4.00 HP/Ti (8.00 on a stacked tile), which is not rate-limited by
  the core at all and is the measured field behaviour; and
- **Pre-build turrets**, which are buildings, not units, so a builder bot can add
  one per turn per builder without touching the core's spawn.
So "spawn more" is weak here, but "heal more" is strong here, and the field
already does the strong one. Do not read the rate cap as an open road.

WHAT WOULD KILL IT — If the field's builders are already at or near the tile-heal
adjacency cap around the core (~16 HP/round/tile; the library's maxed 2x2 figure
is 32 HP/round), then the spawn rate never binds because they never needed more
bodies. The measured field detail is **2.68 healers**, well under the cap — which
says the binding constraint on their defence today is *doctrine*, not the rule.
A strike that provokes them into filling the cap makes them stronger.

BUILDER HOOK — Corpus query, no bot change: for games where we attacked the enemy
core region before r250, measure the **enemy builder-bot count adjacent to their
core** at r-10 / r / r+10 / r+30 around our first attack. If it rises by more than
~1 per 3 rounds, they are converting spawn turns into defence and the rate cap is
binding in our favour; if it jumps fast, they are re-tasking existing builders and
the cap is irrelevant. This distinguishes the two readings above and it is the
prerequisite for sizing any strike.
