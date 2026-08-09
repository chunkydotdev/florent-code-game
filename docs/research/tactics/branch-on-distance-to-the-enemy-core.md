---
tactic: The earliest branch anyone reports is on distance and passability to the enemy base — available at round 0, no scouting
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 wololo (finalist, the season's dominant rush bot) and Battlecode 2023 4 Musketeers (finalist)
evidence: documented
transfers: yes
---

## WHAT IT IS

Two finalists, two seasons apart, both with substantially fixed openings, name the **same**
first branch variable — and it is not an enemy behaviour. It is **map geometry**.

**wololo (BC2021)**, after his pure rush was defeated on large maps:

> *"Thus it was extremely important to judge the distance and passability between my EC and
> my opponent’s to determine whether to rush and bury or to turtle with a defended slanderer
> economy"*

> *"I let my ECs dynamically transition between rushing and turtling depending on context"*

**Referent check.** "my EC" is his own Enlightenment Center (his base); "my opponent's" is
theirs. "context" is expanded in the same sentence: *"betting that I’d be nimble enough to
still overwhelm the opponent with my rush on small maps, and yet turtle harder than my
opponent on larger maps."*

**4 Musketeers (BC2023)**, describing the point at which their previously constant build
ratio became conditional:

> *"We wait until we’ve taken a first guess at where the enemy HQ is. If it’s close, then we
> need to build a lot of launchers, or else we’ll die. If it’s not close, then we have time
> to build adamantium carriers and build up our supply before we need to start getting mana
> for launchers."*

Note the wording — *"a first guess"*, from map symmetry, not from a scout arriving. The same
paragraph adds a second, cheaper geometric conditional using map size directly:

> *"If we see a mana well but no adamantium well, and it’s a small map, then the adamantium
> well is probably hard to get to, maybe tucked away in a corner."*

## WHY IT MIGHT TRANSFER

This is the direct answer to (C) — *among teams with fixed openings, what varied after the
opening and on what signal* — and it is the cheapest possible signal in our ruleset:

- **The enemy core's position is derivable at round 0** from `get_map_width()`,
  `get_map_height()`, our own core position, and the fact that maps are *"symmetric by
  reflection or rotation"*. No unit has to travel; nothing has to be scouted; there is no
  store latency.
- **Passability is readable without travel too**, at least locally: `get_tile_env(pos)`
  over `get_nearby_tiles()` and the map dimensions bound how open the lane is.

And the library's standing context already predicts this is our gap. Sweep 6's single
qualification to its verdict that *"our constant is DEFENSIBLE"* is:

> *"The one qualification — an opening unconditional on MAP GEOMETRY — is a documented
> failure mode, and our own width gradient is it."*

This sweep supplies the mechanism the field actually used against that failure mode, from
two independent seasons. It also sits precisely on the boundary of what our own core-kill
cut could see: **map area tested null** as a discriminator of core kills, and all six robust
features *held under map stratification* (15 maps, 87-110 games each). That is not a
contradiction — the cut asked *"does map predict our kills"* (no), while this asks *"should
our PLAN be conditional on map"* (the field says yes). A signal can be null as a predictor
of outcome and still be the correct thing to condition a decision on, if the current bot
does not condition on it at all.

## WHAT WOULD KILL IT

- **Our maps are 8x8 to 30x30 — a smaller dynamic range than either source's map pool**, and
  the size effect may not clear the noise floor. `map-size-decides-whether-the-rush-is-legal`
  (sweep 14) has the same caveat from the same evidence family.
- **wololo's own conclusion cuts against the aggressive branch**, and the organisers'
  behaviour is the reason: the BC2021 final tournament featured *"mostly large maps"*, and
  BC2025's Kragle warns that finals maps get *"larger and slower"*. A geometry branch tuned
  to reward rushing on small maps is tuned for the part of the pool that tournaments
  systematically under-weight.
- **Distance is not the binding constraint here that it was there.** Their rushes were
  carried by cheap mobile damage; ours cannot be (sweep 14's central qualification). A short
  map shortens the *travel*, but the thing that arrives is still a builder that deals 2 dmg
  for 2 Ti and cannot touch enemy builders. Shortening the walk does not create the
  precondition we lack.
- **Symmetry inference can be wrong.** Our own docs say maps are symmetric by reflection *or*
  rotation; a first guess that picks the wrong one sends the branch the wrong way, and BC2023
  Gone Fishin' spent real engineering on symmetry elimination for exactly this reason.

## BUILDER HOOK

Smallest test: compute `d² from our core to the mirrored/rotated candidate enemy core` at
round 0 in the core's own instance state, and split one existing constant on it — the most
obvious being how early the first turret goes forward, or the `KILL_WINDOW`-relevant
commitment. One number, no store slot, no scouting, computable before any unit has moved.
Then measure `core_kill_share` on the small-map and large-map halves of the pool
**separately** — a branch whose whole claim is that the right answer differs by map must be
read that way or it will average to null.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
- https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
