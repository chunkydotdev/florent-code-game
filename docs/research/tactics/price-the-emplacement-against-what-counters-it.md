---
tactic: Price a static emplacement against the cheapest thing that beats it — and pick the fight where THEY have to buy the dearer object
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020, Java Best Waifu (champions); independently the same arithmetic from confused (BC2020, high-school 2nd)
evidence: documented
transfers: yes
---

## WHAT IT IS

BC2020's static defensive structure was the **Net Gun** — *"Can shoot drones, killing
them in one shot"*, immobile, small vision radius. The counter-object was the
**Fulfillment Center**, which produces the drones.

**The champions ran the matchup as a price comparison and steered the game toward the
branch where the opponent had to buy the more expensive object.** Java Best Waifu, on
being rushed:

> *"We would always start building a Fulfillment Center (if we didn't have one already).
> If the opponent decides to build a Net Gun to counter it, they would have to spend 100
> soup more than us, otherwise we can spawn Drones and drown the enemy Landscapers."*

**Referent check, because the number needs its subject:** the *"100 soup more"* is the
price gap between **their Net Gun** and **our Fulfillment Center** — the defender's static
emplacement versus the attacker's producer of the unit it counters. The move is not
"build the cheap thing"; it is **make the opponent's only answer cost more than your
threat did.**

confused, in the same season, states the same arithmetic from the other side of a
bracket, with the raw prices:

> *"in the maps where both of us were able to rush, we were more likely to win because
> building a net gun was 250 while building a drone factory was 150, leaving us more
> advantageous in economy"*

**Subjects: 250 is the Net Gun's cost, 150 the drone factory's, both in soup, both in
BC2020.** Two independent teams, one of them the season's champion, reduced the
static-defence question to *relative price against the counter*, and neither mentioned
range, damage or survivability when doing so.

## WHY IT MIGHT TRANSFER — against our ruleset

**We have never once written down the price of the answer to our own turrets, and it is
computable in one line.**

- A **gunner** costs 20·s to build and has 25 HP. A builder bot removes it at 2 damage
  for 2 Ti from an orthogonally adjacent tile — and, crucially, **off the firing axis it
  takes zero damage back** (sweep 7). So the answer to a gunner costs the attacker
  **25 Ti of attack spend and 13 builder-turns**, against our 20·s to build it.
- A **sentinel** is 40 HP: **40 Ti and 20 builder-turns**.
- A **barrier** is 30 HP for 3 Ti: **30 Ti and 15 builder-turns to remove a 3 Ti
  object** — the 10:1 that sweep 7 already found, and the reason the barrier screen is
  the only structure in our list whose price ratio is lopsided in our favour.

**Read as Java Best Waifu would read it: our turrets are priced at roughly 1:1 against
their own removal, and our barriers at 10:1.** The exchange-rate argument therefore says
almost nothing about gunner-vs-sentinel (their removal prices, 25 and 40, track their
build prices, 20 and 30, almost exactly) and says a great deal about **screening**.

**And the steering half transfers too.** The champions did not just compare prices — they
*forced the branch*. Our analogue: build the thing whose only answer is the object our
opponent is worst at buying. Our field measurably under-buys ammunition; a threat whose
only answer is turret fire is therefore expensive for them specifically.

## WHAT WOULD KILL IT

- **Healing breaks the price comparison in the defender's favour and this library already
  knows it.** Heal is 4.00 HP/Ti (8.00 stacked), the best damage source is 1.80 HP/Ti, so
  every "cost to remove" figure above is a *floor* that a single healer can lift without
  bound up to the adjacency cap. The BC2020 arithmetic had no repair term; ours must.
- **BC2020's Net Gun one-shot its target.** Ours chip. A one-shot emplacement's price
  comparison is much cleaner than a damage-over-time one's, and the analogy should not be
  pushed past the *method* (price the counter) to the *conclusion*.
- Neither source validated the price rule against win rate — it is doctrine stated by
  winners, which is the evidence class this library has already bounded (sweep 15).

## BUILDER HOOK

A one-off computation, not a code change, and it fits in a comment block: for each
buildable of ours, the titanium the opponent must spend to remove it and the builder-turns
it costs them, **with a healer term**. If any of our structures prices worse than 1:1
un-healed, we are subsidising the opponent every time we build it. The follow-up that
would make it live: prefer, at equal role, whichever structure has the higher
removal-cost-to-build-cost ratio — which on the numbers above is the barrier, by an order
of magnitude, and is why the ablative screen keeps reappearing in this library.
