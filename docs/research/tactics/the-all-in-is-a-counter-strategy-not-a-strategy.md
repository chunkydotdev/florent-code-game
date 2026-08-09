---
tactic: FAILURE MODE — an all-in is a COUNTER-strategy; run unconditionally it is a losing mixed strategy
source: https://forum.codingame.com/t/spring-challenge-2022-feedbacks-strategies/195736
origin: CodinGame Spring Challenge 2022 / UnicornP; Jay Scott and Martin Rooijackers (LetaBot) on the StarCraft AI ladder; Liquipedia SC2 Cheese; Battlecode 2019 Oak's Last Disciple
evidence: documented
transfers: yes
---
WHAT IT IS — Five independent sources, in four different leagues, say the same
thing: the all-in has no unconditional form. It is defined by what it beats.

**CodinGame Spring 2022, UnicornP**, on his own three-hero all-in, in his own
list of problems:
> *"This strategy specifically counters full-defense strategies. If there is even
> one attacker on my side of the field, this strategy loses."*
Referent: "this strategy" is his phase-1/2/3 plan — farm mana to 90, abandon
defence, converge, wind monsters into the enemy goal. He also states the pure
arithmetic failure alongside it: *"In phase 2, the heroes abandon defense and rush
towards a point about 6800 units from the opponent's base. This takes roughly 10
turns."* against a 12-turn defensive clock.

**Liquipedia SC2**, on cheese generally:
> *"The cheesing player is making a wager that the defending player will have some
> sort of oversight in his build."*

**Battlecode 2019 Oak's Last Disciple** wrote the cycle out explicitly:
> *"Rush > Greedier/Cheesier bots > Greedy/Cheesy bots > Eco bots > Rush"*
— a stated non-transitive loop, and their conclusion was to submit the *most
consistent* bot rather than the strongest counter.

**Jay Scott** put a number on the correct frequency, in a toy model he labels as
such:
> *"With good play, a rush opening loses to a safe opening but wins against a
> greedy opening."*
> *"then optimal play is to rush about 9% of the time and split the other 91% of
> games evenly between safe and greedy openings"*

**Martin Rooijackers (LetaBot)**, retiring his own rush bot from the SC ladder:
> *"This Saturday (28 January) will be the last time that my bot will go for a rush
> strategy. The reason for this is simple, rush strategies will stop working
> against almost all the top bots. Already most top bots can hold just about
> anything you can throw at them off 1 base."*
Referent: "this" = the fact stated in the preceding sentence, that this is the
last rush outing. He adds: *"So, with proper scouting, a bot should be able to stop
any rush build if it starts out with a safe build order."*

WHY IT MATTERS HERE — **This is the sharpest tension with `PROGRAMME.md`, and it
should be read as a design constraint on Loki, not an argument against it.** The
programme sets a currency (core-kill share inside r250) and a comparison
(LOKI-N vs LOKI-(N-1)). Nothing in it requires the strike to fire in every game.
The literature says the strike should fire *conditionally*, and every one of the
conversion files in this sweep supplies a candidate condition:
contested-ore (`rush-as-fallback-when-the-opening-is-denied`), map area
(`map-size-decides-whether-the-rush-is-legal`), and enemy launcher count
(`one-cheap-interceptor-decides-the-matchup`).

There is also one point that runs the *other* way and it is genuinely in the
programme's favour. Jay Scott, on the difference between bot and human ladders:
> *"Most bots play all-in cannon rushes to win outright (because they know bot
> opponents will often fall over). Most humans play pressure cannon rushes to set
> the enemy back so they can get ahead (because they expect that opponents will
> know how to react)."*
We are on a bot ladder against opponents with measured, fixed habits, and the
project's standing mandate is to play the players. Against a non-adapting field,
the outright-kill variant is the *documented correct choice* — which is exactly
what Magnus's directive asserts.

WHAT WOULD KILL IT — The ladder half-life. Liquipedia:
> *"Like most cheese, these builds are much easier to stop once a player has gained
> a familiarity with them. This is why many cheese builds surge in popularity on
> the ladder, only to disappear weeks later."*
Referent: "these builds" are the specific nuanced cheeses enumerated in the
preceding sentence, with "Like most cheese" generalising the claim. Our opponents
are bots that do not learn within a match — but their **authors** do, between
submissions. A Loki edge measured this week is not guaranteed to survive the
opponents' next upload, which argues for taking the rating fast rather than
polishing.

BUILDER HOOK — Do not build a "rush mode". Build a **fire-control predicate**:
`should_strike(ct) -> bool`, evaluated once and latched in a store slot, with the
candidate conditions above as its terms. Then the natural first battery is the
predicate's *base rate* — what fraction of games does it fire in, and is core-kill
share higher inside that subset than outside it? That is a measurement the
programme's currencies already support, and it costs one slot.
