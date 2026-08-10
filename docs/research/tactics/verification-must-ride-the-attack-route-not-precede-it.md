---
tactic: (A)/(C) A TEAM MEASURED THE COST OF CHECKING BEFORE COMMITTING AND IT WAS NEGATIVE ON THE CASES IT DID NOT NEED — "worse in cases when we would have guessed the right symmetry anyway, but more consistent overall". Two later teams removed the detour entirely by making the attack path and the observation path the same path
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 The High Ground (4th, seeding); Battlecode 2023 Gone Fishin'; Battlecode 2025 confused
evidence: documented
transfers: yes
---

## WHAT IT IS

There are exactly two ways to act on a belief you cannot verify from home: **verify first,
then go** (a detour) or **go, and verify en route** (free). Three Battlecode teams span both,
and one of them states the trade-off as a measured regression.

**1. Verify-first, with its cost named (BC2020 The High Ground).**

> *"our rush miner would first run to the middle of the map in an attempt to determine which
> of 3 possible symmetries the map was, and then rush toward the opponent."*

> *"This made our rush worse in cases when we would have guessed the right symmetry anyway,
> but more consistent overall."*

**Referent check.** *"This"* is the behaviour in the preceding sentence — routing the rush
miner via the map centre to determine symmetry before rushing. The quoted sentence opens
*"One thing that separated us from some other rush bots is that"*. **So the
author is reporting a deliberate variance-for-tempo trade, and reporting that the tempo half
of it is a real loss on the majority branch.** Their result that season: 2nd on the scrimmage
server overnight, eliminated 4th in the seeding tournament.

**2. Verify-en-route, arrived at by removing a dedicated scout (BC2023 Gone Fishin').** Their
own evolution is documented in one paragraph — first a dedicated scouting trip, then not:

> *"We first had a carrier that goes to the center of the map to scout for symmetry and then
> comes back to report."*

> *"After Sprint 2, even though carriers can run faster, we realized that having carriers
> scout is a waste of their potential to mine resources, which are especially important in
> the early game."*

> *"We then changed to having all launchers scout symmetry on the fly as they guess a base
> location and move to the base."*

**Referent check.** Launchers are BC2023's ranged combat unit — the attackers. *"the base"*
is the guessed enemy HQ. **The verification is performed by the attacking force, while it is
attacking, at zero tempo cost, and the guess is what it walks toward in the meantime.**

**3. And the strongest form: choose the route so the best observation post is ALREADY on the
way (BC2025 confused).**

> *"Soldiers defaulted to assuming rotational symmetry unless proven otherwise, directing
> them towards the map center initially."*

> *"This offered a strategic advantage, serving as the optimal location for determining the
> map’s symmetry while also minimizing the distance to potential enemy tower locations."*

**Referent check.** *"This"* is the default-plus-head-to-centre behaviour of the preceding
sentence. The claim is explicitly the conjunction of two properties of the same tile: best
disambiguation **and** minimum distance to the candidate targets. **The High Ground paid for
information with a detour; confused got the same information for free by choosing where
"forward" points.**

## WHY IT MIGHT TRANSFER

- **Our detour is priced, and it is the worst detour in this library.** A builder bot moves
  one **cardinal** step per move cooldown and cannot act on a moving turn. This sweep's own
  measurement (1-in-17 sample of the local `replay_archive/`, 598 replays, **18 unique maps**)
  puts the median Manhattan distance from our core to the enemy core at **24**, and the
  median maximum separation between the three symmetry candidates at **24** as well — equal in
  17 of 18 maps. **A verify-first detour to the centre is roughly half a traverse; a wrong
  guess is a full one.** Against a 250-round kill-window target and our own tape (before r200
  we go 277-148, 65.2%; after r200, 164-363, 31.1%), both are expensive and one is avoidable.
- **The confused-2025 construction is available to us and costs nothing.** The straight line
  from our core to the `Rot180` candidate passes through the map centre by construction — the
  centre *is* the midpoint of that segment. So "walk at the most likely candidate" and "walk
  through the best disambiguation point" are the same instruction here, exactly as they were
  for confused. There is no version of this we have to pay for.
- **It fixes the ordering error the library keeps making.** Our existing files
  [`abort-the-scout-on-a-deadline`](abort-the-scout-on-a-deadline.md) and
  [`the-scout-that-pays-for-itself`](the-scout-that-pays-for-itself.md) both assume a scout is
  a *separate* errand with its own budget. Gone Fishin' deleted the errand and kept the
  information. **The cheapest scout is the attacker's own eyes on the way to the target.**

## WHAT WOULD KILL IT

- **The information the en-route observer collects must actually be actionable, and ours is
  crippled.** Measured in this repo 2026-08-08 (`docs/game-model.md`): `get_tile_env()`,
  `is_tile_passable()` and `get_tile_building_id()` **raise `GameError: Position out of vision
  range`** for in-bounds tiles the unit cannot see. Every source here disambiguates symmetry
  by comparing terrain across the axis; **we can only compare tiles we have physically been
  near** (builder vision r²=20). A raider walking the centre line sees a corridor about 9
  tiles wide, and it must have *already seen* the mirrored tile on our own half to compare
  against. That is a real constraint none of the three sources had.
- **The High Ground's "more consistent overall" may be the right trade for a bot with the
  wrong prior, and the wrong trade for one with the right prior.** This sweep measured
  `Rot180` correct on **17 of 20 unique maps (85%)** in the local archive. At 85%, paying half
  a traverse to convert 15% of games is a bad deal; at 40% it would be a good one. **The trade
  is a function of the prior's hit rate, and the hit rate is a property of the organisers'
  generator, which we have sampled at n=20 maps from our own archive only.**
- **Consistency is not our currency.** The programme's primary is `core_kill_share` and its
  secondary is `time_to_core_kill`; a r1000 round is *"a defeat even if we by chance win it"*.
  The High Ground's stated gain is *variance reduction*, which our programme does not buy.
  **Read their sentence as evidence against the detour, not for it.**
- **A defensive reading of any of this is off-programme and should be discarded.** None of
  the three sources' best idea here is defensive, so nothing needs cutting on those grounds.

## BUILDER HOOK

Smallest test, and it is a routing change with no new state: point the forward walk at the
`Rot180` candidate (see
[`the-symmetry-candidate-set-is-the-commit-rule`](the-symmetry-candidate-set-is-the-commit-rule.md))
and **do not add any centre-detour**. Then measure, from the replay, the round at which our
first unit becomes adjacent to the true enemy core footprint, split by *whether the guess was
right*. The two distributions are the entire content of this file: the right-guess arm prices
the detour we avoided, and the wrong-guess arm prices what a detour would have bought. **Both
halves are needed — a single pooled number will average the trade away.**

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
- https://battlecode.org/assets/files/postmortem-2023-gone-fishin.pdf
- https://battlecode.org/assets/files/postmortem-2025-confused.pdf

Every quoted string above was verified verbatim by literal `grep -F` against the flattened
primary text (`pdftotext` then `tr -s ' \n\t\f\r' ' '`) during tactics sweep 20C
(2026-08-10 04:11 UTC, repo HEAD `a08669c`). The distance measurements are this sweep's own
instrument run against the local replay archive, population stated inline.
