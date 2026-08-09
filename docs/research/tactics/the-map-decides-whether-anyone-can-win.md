---
tactic: DECISIVENESS IS PARTLY A MAP PROPERTY — on some maps the field reports 100% of matches reaching the round limit, decided by who hoarded rather than who built
source: https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
origin: Battlecode 2023 / 4 Musketeers (finalist)
evidence: documented
transfers: yes
---
WHAT IT IS — 4 Musketeers, describing named maps from BC2023's tournament pool
(Jail, Walmart, Potions), report the failure mode our incidence cut is looking at,
at 100% rate, attributed entirely to terrain:

> *"The result was that every single match went to 2000 rounds and went to
> whichever team happened to stockpile resources rather than build more things."*

Referent: "The result" is of the immediately preceding sentence — on the map
Jail, the spawn-toward-the-wells opening that *every* team used left units stuck
behind walls. And the generalisation, in the same section:

> *"There were far too many maps where nothing happened for 2000 rounds."*

The team repeats the complaint in their closing reflection, where it is aimed at
the design rather than the season:

> *"Watching matches go to a 2000 round tiebreaker because neither team could get
> past all the walls is not fun."*

Two distinct claims are being made and they should not be blurred. The first is
that **map geometry can drive decisiveness to zero** — not lower it, zero it.
The second is subtler and is the one worth building on: when it does, **the
tiebreak key decides which non-play wins**. BC2023's key was resource stock, so
the winner was *"whichever team happened to stockpile resources rather than build
more things"* — the tiebreak actively rewarded not playing.

WHY IT MIGHT TRANSFER — Directly, on both claims.

**On the first:** our maps are 8x8 to 30x30 and contain WALL tiles that block
building and movement. Builder bots move only in the four cardinal directions, so
wall geometry bites harder here than in a game with diagonal movement. If our
core-kill incidence is a mixture over map classes with some classes at or near
zero, then the aggregate incidence number is a statement about the *draw*, and an
incidence A/B unblocked on map class measures the draw rather than the change.
This is the measurement consequence of
[`the-designers-lever-was-the-map-pool`](the-designers-lever-was-the-map-pool.md),
stated as a bot-facing fact rather than an organiser-facing one.

**On the second — and this is the piece that is genuinely good news for us.** Our
tiebreak keys are, in order: titanium **delivered** to core (cumulative), then
harvesters **alive**, then titanium **stored**. Only the third key is a stock. Our
primary key is a **flow**, and a flow cannot be won by declining to play — it is
won by running the pipeline. BC2023's degenerate incentive (hoard, don't build) is
therefore *not* our degenerate incentive, and the library's standing complaint
that *"we bank and do not spend"* is a defect against our own first tiebreak key
as well as against the kill. The two roads to a win agree with each other here
more than the programme's framing suggests: **more titanium moving through the
pipeline serves key 1 and pays for the ammo that serves the kill.** What they
disagree about is *stored* titanium, which serves only key 3 and is the weakest
key we have.

WHAT WOULD KILL IT — 4 Musketeers give no numbers, only "every single match" on
three named maps, from a competitor with a grievance about map design. The 100%
is an assertion, not a count. And BC2023's map sizes (20x20 to 60x60) and its
current/cloud anomalies are not our terrain model; the transferable part is
"terrain can zero decisiveness", not any specific threshold.

The second claim would be killed by a measurement showing our delivered-titanium
key is nearly always decided by round ~300 anyway, in which case late pipeline
throughput buys nothing and the flow/stock distinction is academic. That has not
been checked.

BUILDER HOOK — Two corpus cuts, no bot change:
1. Core-kill incidence by map area and wall-tile fraction (shared with
   [`the-designers-lever-was-the-map-pool`](the-designers-lever-was-the-map-pool.md)) —
   does a zero-incidence map class exist for us?
2. In our 353 r1000 games, which tiebreak key actually decided them — key 1
   (delivered), key 2 (harvesters), key 3 (stored), or the coinflip? If key 1
   decides most of them, the abort state in
   [`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)
   is aimed correctly. If the coinflip is doing real work, we are closer to The
   High Ground's r1640 problem than we think.
