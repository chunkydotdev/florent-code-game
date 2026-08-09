---
tactic: Get your magic numbers by reverse-engineering the macro of teams above you, not by tuning against your own pool
source: https://battlecode.org/assets/files/postmortem-2026-generalized-strokes-theorem.pdf
origin: Battlecode 2026 / Generalized Strokes Theorem (2nd place); corroborated by BC2020 The High Ground (4th), BC2025 The Kragle, BC2024 cout for clout
evidence: documented
transfers: yes
---
WHAT IT IS — **The second-place team of the most recent season publishes its entire macro
process, and the process is "copy upward".** It is the most procedurally explicit answer to (C)
in the corpus:

> *"I think that macro is best improved by scrimmaging against good teams, and copying what they
> do."* … *"we don’t try too hard to be original with our thoughts when it comes to macro."* …
> *"For the most part, we would queue scrims against teams above us on the leaderboard, reverse
> engineer their macro (which is much easier than reverse engineering micro, pathfinding, or
> communication), copy whatever strategy we gleaned, and if it made us better then we would keep
> it."*

And they name what it produced, which is the load-bearing part: *"This is how we arrived at our
strategy for forming Rat Kings on cheese mines, **our magic numbers for how many Baby Rats to
build and when to build more Baby Rats**, and many other parts of our macro."* They also weight
it against writing code: *"I suspect we spent far more time reviewing scrims than actually
writing code."*

**Three independent corroborations.** BC2020 The High Ground on the team that had just leapt 200
Elo clear of the field: *"we decided to shamelessly copy Java’s strategy"* … *"We pulled up some
replays of Java’s games"*. BC2025 The Kragle, having found a defect only by watching others:
*"Only after we started looking carefully at what other teams were doing did we notice that no
other team bothered having their bots refill on paint"*, generalised to *"Other teams beat your
bot for a reason, and the easiest way to improve is to copy what they do better than you."*
BC2024 cout for clout on the specific mechanism that was beating them: *"All the top teams
seemed to have XSquare’s attack micro, and our attack micro seemed to be holding us back. We
seemed to do OK against all the teams except XSquare, whose secret micro formula demolished us
over and over again. So we did the one logical thing that anyone would do: rob XSquare’s micro
and turn it against him"*.

**AND IT IS NOT A BATTLECODE HABIT — two other leagues converge on it independently, including the
exact act of lifting numeric constants.** Halite III's mlomb (*"The Halite 3 edition has ended and
I managed to get rank 18"*) wrote a replay analyser, pointed it at players above him, and shipped
the result as a hardcoded number:

> *"Averaging that infomation from top players and some tuning by hand I just hardcoded the max
> turn to spawn a ship in my bot."*

(`infomation` is his typo. The referent of *"that infomation"* is the per-player statistics his
`analyzer.js` extracted from batches of games; the named subjects in that section are `teccles`,
`Rachol` at rank 2, and `TheDuck314` at rank 1.) **He also records a copied rule that failed** — of
a spawn threshold reverse-engineered from teccles's winning games, *"I tried this strategy and it
didn't work for me."* CodinGame Spring 2021 supplies the behavioural rather than numeric version,
and it moved a whole league: *"Finished 150 legend with rules based bot. Main approach landed me
in gold. The thing that got me to legend was actually watching @reCurse games and synthesizing his
strategy into rules."* — with his own limit stated, *"there were obviously a lot of other
differences and behaviors that I didn't capture from watching his strategy"*, **and a documented
failure to replicate by someone attempting the same thing in the same thread**: *"I did something
quite similar, but could not reach Legend. I was stuck at #30 place in Gold."*

WHY IT MIGHT TRANSFER — **`transfers: yes`, and this is the one finding in the sweep that is
immediately actionable with assets we already hold.** **Four leagues now converge on it** —
Battlecode, Halite III, CodinGame and (via the nemesis-finding tooling below) Halite II. The claim it rests on is a *tractability*
claim — that **macro is the layer that reverse-engineers cheaply from replays**, far more cheaply
than micro or pathfinding. We have 3.8k decoded replays in `corpus/`, league-wide match listing
by team, and a query layer already built. The constants a bot's macro exposes to a replay decoder
are exactly the ones we currently derive from a dominated self-play pool: **build mix over time,
when the first turret goes up, harvester count at r50/r100, ammo conversion schedule, forward
placement distance.** Measuring those *on sporks, Clankers, not adgato, Pivot and Pantheon* is a
corpus query, not an experiment, and it is not subject to the 2× self-play inflation sweep 15
documented — because nothing is being A/B'd at all. It answers "what does 2100 Elo do at r30"
with an observation instead of a guess.

WHAT WOULD KILL IT — **Copying upward is documented to fail too — twice in this file's own sources
(mlomb's spawn threshold, BenPix's failed imitation) and again in the file filed beside it:** see
[`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md), where cout for clout
adopt two separate top-team strategies and discard both. The reason given elsewhere in the corpus
is that a strategy is load-bearing on the rest of the bot that carries it — BC2023 don't @ me:
*"you have to actively attempt to improve upon the “inspired” algorithm, or else it’ll never be
as good or better than the team that you took it from."* A second limit is specific to us: the
top of our league may be strong for reasons **not visible in a replay's build log at all** (CPU
efficiency, micro-level tile selection, targeting), in which case the decoder sees their
constants and misses their edge. And a third: adopting a top bot's build mix without its
defensive competence is exactly the sub-threshold aggression the heal arithmetic punishes 2.2:1.

**The tooling shape three competitors independently describe is worth copying too: a per-opponent
"nemesis" breakdown.** mlomb built one — *"Nemeses breakdown, you can see winrates/places against
specific players"* — and CodinGame's #4 Legend describes the same loop starting from a ladder stats
service: *"I looked at"* cgstats *"to find players that I'm constantly losing against"*, then
replay analysis, then a local batch run. **Our corpus already supports the first two steps.**

BUILDER HOOK — **The smallest test is a descriptive diff, not a plank.** Run the existing corpus
tooling to produce one table: our r0-50 / r50-150 build medians beside the same medians for each
of the five 1950+ teams, on comparable maps. Every cell where they differ from us by more than
their own between-game variance is a candidate constant, already ranked by size. That is a
read-only query against data we have, it produces a prioritised list rather than a single guess,
and per INDEX's standing conclusion the arena remains the only verdict on any of them.
