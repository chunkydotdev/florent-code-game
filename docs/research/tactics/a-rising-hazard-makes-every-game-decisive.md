---
tactic: (D) THE STRONGEST DESIGNER LEVER FOUND — Battlecode 2020 removed the score fallback entirely and had the MAP kill the loser, so decisiveness was 100% by construction
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 (organisers "Teh Devs"), as documented by Java Best Waifu
evidence: documented
transfers: no
---
WHAT IT IS — Sweep 17A asked whether any league's organisers changed the rules to
raise the share of decisive games. Battlecode 2020 is the extreme answer: they did
not raise it, they made it **unity**, by deleting the score fallback and replacing
it with a global rising hazard.

> *"it wins if and only if the enemy HQ gets destroyed, which means that it gets
> either flooded or buried by landscapers"*

> *"The water increase is slow but exponential, which guarantees that the entire
> map will eventually flood (and therefore that the game will eventually end)."*

Referent: "The water" is BC2020's global water level, which rises every turn and
floods any tile below it that is adjacent to an already-flooded tile. Note both
halves of the design. The win condition is *only* HQ destruction — there is no
"more resources at the round limit". And termination is guaranteed not by a clock
but by an **environmental process that destroys bases**, so "survive to the end"
is not a strategy, it is a contradiction. The only defence is to out-build the
water (terraform a wall), and the only offence is to arrive before it does.

The consequence shows up as a *behavioural* fact in the same season: this is the
year the field converged on
[the crunch](the-crunch-is-a-rate-race-not-a-damage-race.md), a manoeuvre whose
entire purpose is converting an economic lead into a dead HQ. When there is no
points win available, every team writes conversion code.

WHY IT DOES NOT TRANSFER — We cannot change our rules, and our rules are the
opposite design. Our terminal condition is a **clock with a score fallback**
(round 1000 → titanium delivered → harvesters alive → titanium stored →
coinflip), and there is no hazard: a base that is never attacked is never in
danger. So *not converting* is a fully legitimate, engine-sanctioned outcome
here in a way it structurally was not in BC2020.

That is worth stating plainly because it reframes our measured surprise rather
than solving it. **Our low core-kill incidence is not, on this evidence, prima
facie a defect.** In the one league that made kills mandatory, kills happened
100% of the time; in leagues with a score fallback, the field's own postmortems
report seasons where *most* games were settled on tiebreak (see
[`the-map-decides-whether-anyone-can-win`](the-map-decides-whether-anyone-can-win.md)).
Combined with our own numbers — 353 games to r1000 and **57.2% won on tiebreak** —
the honest statement is that we have two roads to a win and are currently better
at the slower one. Raising incidence is worth pursuing, but the programme's
framing of a core kill as *the* currency is a choice about which road to invest
in, not something the ruleset forces.

WHAT WOULD KILL THIS READING — If our tiebreak win rate turns out to be
concentrated in the bands we already beat, and near-random or negative against
1900+ opponents, then the score road is not a second road at all against the
opponents that decide our rating, and the incidence framing is right after all.
This has not been cut by rating band. **It is the single cheapest measurement in
this sweep and it should be run before anything here is built on.**

BUILDER HOOK — none in the bot. One corpus query: our win rate in games reaching
r1000, cut by opponent rating band. If it holds up at ≥1900, the tiebreak is a
real second road and the abort rule in
[`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)
is worth building. If it collapses, that file's fallback is a trap and the
programme's kill-first framing is vindicated.
