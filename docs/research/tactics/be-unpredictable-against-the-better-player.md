---
tactic: A #15 bot held a 66% record against the eventual champion by refusing to be deterministic
source: https://forum.codingame.com/raw/199055/13
origin: CodinGame Fall Challenge 2022 / arturgo (legend #15) vs delineate (1st); with AIIDE 2019 BananaBrain and CodinGame Spring 2020
evidence: documented
transfers: partial
---
WHAT IT IS — **The single cleanest "weaker bot beats stronger bot, repeatably, by a named
mechanism" result in the sweep.** The post opens *"AI of arturgo, legend #15"*, and states:

> *"I'm not very good at designing scoring functions, but that gave me #15, and a 66% win rate
> against delineate"*

**delineate won that contest** — verified independently from a different post in the same thread:
*"Congratulations Delineate for your victory. You lead the race from the beginning to the very
end."* So a **15th-place** bot, by its own author's account a weak evaluator, held a **66% record
against the champion**. The mechanism is a mixed strategy — approximate the Nash equilibrium over
moves and sample from it — and his stated reasoning is the rock-paper-scissors argument:

> *"To win a game like that, we can't be deterministic, for example, if you always play Paper,
> you'll be beaten by a player who always plays Scissors."*

**Corroboration on the mechanism from a different league.** AIIDE's BananaBrain (#1 in 2022 and
2023) varies its opening even among openings that already win 100%, and Jay Scott frames the value
as problem-count rather than as weakness: *"Unpredictably playing one of several strong
openings sets the opponent two problems (“what is this fiend doing, and then how do I live through
it?”)"* … *"which must both be solved, more than twice as difficult."*

**And the ladder property that makes any of this possible — non-transitivity, stated by someone
who tuned for it deliberately.** CodinGame Spring 2020, cegprakash: *"I feel my rank (100+) is not
justified considering I had 55-60% win rate against rank 40-50 bots."* … *"My bot was fine tuned
to beat better bots and not weaker bots."* **A ladder rating is a summary of a non-transitive
tournament, so a positive record against a specific stronger opponent is not a contradiction in
terms.**

WHY IT MIGHT TRANSFER — **It is the mechanism that makes the underdog's position winnable in
principle**, and it sits underneath several other files in this sweep: wololo's tax works because
the top tier's response was *deterministic*
([`their-defensive-reflex-fires-unconditionally`](their-defensive-reflex-fires-unconditionally.md));
Gonny's deletion works because the top tier's behaviour was *predictable*
([`measure-what-the-top-tier-never-does`](measure-what-the-top-tier-never-does.md)). **This file is
the same coin from our side: our own determinism is the surface they exploit, and INDEX measures
it — our opening's CV is 0.09 against the field's 0.26.** We are, on the one axis anyone has
measured, the most predictable participant in the comparison.

Our engine also happens to make a mixed opening nearly free. Cost scaling, spawn ring, and the
16-slot store are all deterministic, but nothing forbids the core from sampling among two or three
*equally-priced* opening branches — and INDEX's confirmed **id-ascending turn order** means the
choice can be made once, by the core, and read consistently by every unit that round.

WHAT WOULD KILL IT — **Four things, and the fourth is the serious one for our ruleset.**
(1) **arturgo's game was simultaneous-move**; ours is sequential with a fully deterministic,
measured turn order. The rock-paper-scissors argument is strongest under simultaneity, and its
force here is reduced rather than eliminated (the relevant uncertainty for us is *across* games,
not within a turn).
(2) **A 66% record is one number from one contest**, and the same corpus warns that isolated wins
over a #1 mean little in a high-variance game — Gonny: *"so any decent bot can easily win a couple
games against #1"*.
(3) **Randomisation costs expected value against weaker opponents**, which is most of our pool.
cegprakash's own post is a complaint about exactly that trade landing him at 100+.
(4) **Randomising an opening in OUR game is asymmetrically dangerous, because the defender's edge
is 2.2:1 (4.4:1 stacked).** A mixed strategy that sometimes plays a commitment we cannot support
is not variance, it is a donation — sweep 14's `all-in-variance-is-a-ladder-tax` and the
sub-threshold-aggression arithmetic both apply. **Any mix must be over branches that are each
individually sound**, which is exactly what BananaBrain does (it mixes among openings that already
win) and is *not* what "add a coin flip" means.

BUILDER HOOK — Before building a mixer, measure whether determinism is being exploited at all:
**in our games against the 1900+ band, is their behaviour in the first 50 rounds conditional on
ours, or identical across games?** If their opening is invariant, they are not reading us and
unpredictability buys nothing. If it varies with what we do, we are being read, and the cheapest
counter is a *two-branch* opening chosen by the core at round 0 from a per-game seed, where **both
branches are ones we already ship and neither is a commitment we cannot support.**
