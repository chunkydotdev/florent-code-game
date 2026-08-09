---
tactic: FAILURE MODE — the strike arrives after the window, or at a target that is no longer there
source: https://battlecode.org/assets/files/postmortem-2025-spaark.pdf
origin: Battlecode 2025 / SPAARK (finalists); Halite II rooklift; Liquipedia SC2 Photon Cannon Rush
evidence: documented
transfers: partial
---
WHAT IT IS — Three failure shapes that all reduce to the same thing: the attack's
cost is paid on departure and its payoff is evaluated on arrival.

**Arriving at nothing.** BC2025 SPAARK's splasher rush was aimed at enemy
structures under construction, and the counter-build simply finished first:
> *"When our splashers arrived at the opponent towers, there would be no ruins that
> were being built, making the splashers useless."*
The counter they name is pure compounding economy: *"Spam money towers to get 500
paint each, spawning more bots in exponential growth"*. Their own note that it was
a balance patch, not a tactic, that finally settled it: *"soldier rush was nerfed
after the sprint 2 balance changes that made your initial towers spawn at level
2"*.

**Arriving after the economic clock started.** Halite II rooklift, whose rush was
otherwise 1279-176:
> *"But if the enemy is docked, he will be producing ships soon and we will lose;
> so we must use more aggressive play, ignoring our theory."*
The safe engagement geometry (`no-lose-engagement-geometry.md`) is only
affordable *before* the defender's production begins; after that the attacker must
play unsafely, and that is where his losses came from.

**The target moves, or refunds.** Liquipedia SC2:
> *"Terran can also Lift off and move production buildings that may be in range of
> the Cannons, or even lift their initial Command Center and move it to another
> base so that the Protoss players initial Pylons and Cannons are useless."*
And the timing rule that exists purely to defeat a refund: place cannons only once
the target hatchery is near completion, because firing earlier *"would allow the
Zerg to cancel the Hatchery"*.

WHY IT IS `partial` FOR US — Two of the three do not transfer, and saying so is
the point of filing it.

- **Target relocation cannot happen here.** Every building is immovable and the
  core has a fixed 2x2 footprint. Our target is guaranteed to be where we found
  it. That is a real advantage over three of the four leagues in this sweep.
- **There is no build-cancel refund** in our ruleset to time around; `destroy()`
  is free and instant but returns only the cost-*scale* contribution, not
  titanium.
- **Arriving too late transfers completely, and is our measured problem.** The
  library's own instruments say *"everything about us breaks at r150"* and raider
  survival collapses 43 → 6 rounds; *"2.34% of forward throws at r200+ ever land
  a single attack on the enemy core."* SPAARK's failure and ours are the same
  failure.

The arrival cost is also worse here than in any source game, because our attacker
walks: builder bots move one **cardinal** step per move-cooldown, and moving is
mutually exclusive with acting. A diagonal traverse of a 30x30 map is ~58 moves,
during which the unit builds nothing, heals nothing and delivers nothing — and
during which the defender pays zero.

WHAT WOULD KILL THE FAILURE (i.e. the mitigations that exist) — (a) Do not send
the damage; send the *builder* and grow the damage on site
(`spawn-the-attack-at-the-target-not-a-march.md`). (b) Do not fire until the
threshold is met (`the-defenders-reserve-and-what-defeats-it.md`) — a strike that
opens early against a live reserve is the sub-threshold donation, not an early
kill. (c) Condition the commit on map area, which is a proxy for arrival time and
is free at round 0 (`map-size-decides-whether-the-rush-is-legal.md`).

BUILDER HOOK — Instrument arrival explicitly before designing around it: from the
corpus, per game, compute **round at which our first unit becomes adjacent to the
enemy core region**, split by map area. That single distribution decides whether
`KILL_WINDOW_RND: 250` is a tight target or an impossible one on large maps, and
it is measurable today with no bot change.
