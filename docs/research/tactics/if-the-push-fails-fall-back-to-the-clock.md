---
tactic: THE ONLY COMMIT/ABORT STRUCTURE THE FIELD ACTUALLY SHIPPED — abort on the push's FAILURE, not on a forecast, and have a named fallback state to abort INTO
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (finalist)
evidence: documented
transfers: yes
---
WHAT IT IS — Sweep 17A searched all 22 Battlecode postmortems for an
expected-value or threshold rule governing whether to attempt the kill
(see [`nobody-computes-whether-to-finish`](nobody-computes-whether-to-finish.md) —
there is none). This is the single thing the field shipped in its place, and it
is a **fallback**, not a gate.

The High Ground's problem was a mirror matchup that neither side could convert.
Their own words for the symptom are almost exactly our tiebreak/coinflip:

> *"both of our lattices and HQ would flood at round 1640, making games between
> us a coin flip"*

Referent: "us" is The High Ground and Java Best Waifu; the flood is BC2020's
global rising-water hazard, which destroys any unwalled base. Neither team built
a turtle wall, so if neither crunch succeeded, both HQs died to the water and the
result was arbitrary. Their fix, shipped in the last hours before the deadline:

> *"we decided that if our crunch failed we should run back with our remaining
> landscapers and raise our 7x7 wall until we flooded"*

Three properties are worth naming precisely, because they are what make this
different from a commit gate:

1. **The trigger is an observed failure, not a prediction.** Nothing forecasts
   whether the crunch will work. It is attempted, and *failure* is the signal.
2. **There is a named state to abort into**, with its own build order (raise the
   7x7 wall), not merely "stop attacking".
3. **The abort is a race against the clock, not against the enemy** — they raise
   the wall *until they flood*, i.e. they switch from trying to win to trying to
   satisfy the terminal condition.

The same postmortem shows the same team's other timing device, and it is worth
recording beside this because it is the *crude* version:

> *"return to normal build order at round 400 whether we are being rushed or not"*

They call this hacky in the same passage. It is a **disarm on a round number** —
precisely the pattern sweep 15 found no winning bot uses for *arming*, here used
for *disarming*, and used because a reactive state had no exit condition of its
own.

WHY IT MIGHT TRANSFER — Our fallback is far better than theirs: they aborted into
a coin flip, we abort into a tiebreak **we win 57.2% of** (353 games at r1000).
That asymmetry is the whole argument. A failed commit costs us the titanium spent
plus the delivery we did not make while spending it; an abort that restores
delivery converts a lost push into a 57.2% branch rather than a coin flip.

Our tiebreak keys make the fallback state concrete and cheap, which is the part
that is buildable today. Key 1 is **titanium delivered** (cumulative — a late
hoard scores zero), key 2 is **harvesters alive** at 20 Ti base and +5% scale,
key 3 is stored titanium. So the abort state is: stop converting titanium to
ammo, resume conveyor/harvester spend, and rebuild harvesters. All three are
things our bot already knows how to do; nothing new has to be written except the
transition.

And the trigger is available without any forecasting: **HP on the enemy core over
a window.** If our committed turrets have been firing for N rounds and the enemy
core's HP is not monotonically falling, the crunch has failed — the healers are
out-repairing us, which by the library's arithmetic means we are donating at
2.2:1 and every further shot makes it worse.

WHAT WOULD KILL IT — The fallback is only worth entering if the assets can
actually come home, and **ours cannot.** The High Ground's landscapers were
mobile and walked back. Our damage is immobile turrets built inside the enemy
kill zone; a sentinel that stops firing is not a saved asset, it is a dead asset
that has stopped paying. So the abort recovers only the *flow* (titanium no
longer converted to ammo), never the *stock*. That materially shrinks the value
of aborting late, and argues that the abort window must be early — which is an
argument for a short evaluation window N, not a generous one.

Second killer: aborting is only positive-EV while the tiebreak edge holds. Our
57.2% is measured against the field we have played. If it is much worse against
the top tier — and the library's upward-pricing note says our defensive edge is
*thinner* up there — then aborting against a 1900+ opponent may be aborting into
a losing branch, and the same rule would be wrong in the games that matter most.
That has not been measured by seat or by rating band and it should be before this
ships.

BUILDER HOOK — One store slot and one counter. Write the enemy core's HP into a
comms slot each round it is visible; when a siege is live, compare against the
value from N rounds ago. If it has not fallen by more than the arithmetic says
one round of our bearing turrets should deliver, set an ABORT flag in the store —
and have the core's ammo-conversion branch and the builders' build-priority
branch both read that flag. The flag is the whole feature; the two consumers
already exist.
