---
tactic: Static defence must name the countervailing advantage the temporary safety bought — the positive form of our own admission bar, written by a ladder-bot author in 2017
source: http://satirist.org/ai/starcraft/blog/archives/353-turtle-strategies.html
origin: Jay Scott (satirist.org), author of the Steamhammer StarCraft bot; commentary on SSCAIT games
evidence: documented
transfers: yes
---

## WHAT IT IS

`PROGRAMME.md` acquired `PLAY_DEFENCE: not_at_the_kill_s_expense` and
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` on 2026-08-11. **The nearest thing
the literature has to a statement of that rule predates it by nine years, and it is
stated as a POSITIVE obligation rather than a negative bar.**

> *"Static defense can’t go attack; it costs resources and it offers initiative to the
> opponent."*

> *"In a well-played game, static defense has to pay for itself with a countervailing
> advantage: You have to use the temporary safety it brings to get ahead in economy"* …
> *"or to get ahead in tech, as when in ZvZ you make a sunken to tide yourself over
> until your spire finishes."*

**The two clauses are the whole tactic.** Defence is legitimate *only* as the purchase
of a window, and the purchase is only complete when you can name **what you spent the
window on**. A sunken colony that buys time for a spire is paid for; a sunken colony
that buys time for nothing is a loss.

**And he prices the OVERSHOOT with a specific integer, in a specific game.** The
referent below is the SSCAIT game Steamhammer vs KillAll: KillAll opened 9 pool and had
a build-order advantage over Steamhammer's 5 pool, then spent it on static defence.

> *"But instead of making a second hatchery to win with mass lings, or getting quick gas
> to win with mutalisks, KillAll turtled. It threw away its advantage."*

> *"You may want 1 sunken, because the 5 pooler starts making lings sooner and can be a
> little ahead. 5 sunkens are 4 too many and put KillAll behind despite its stronger
> opening."*

**One sunken is admissible; five is a loss — and the difference is not a doctrine, it is
a DOSE.** He adds a siting failure on top of the count failure: *"They are not well
placed; they don’t protect either the approaches or the mineral line."*

**The author himself drew the scope line our amendment draws**, in the comment thread
under the same article, replying to LetaBot's Terran counter-example:

> *"when you need static defense to survive until you can counter, it can hardly be
> called excess"*

The referent of *"it"* is static defence built to survive to a counter-attack — exactly
the r150–250 case our programme now admits, and explicitly distinguished by him from the
*"excess static defense"* the article is actually about.

## WHY IT MIGHT TRANSFER — against our ruleset

**Our two measured defensive negatives are the "1 sunken" case, not the "5 sunkens"
case.** s30 measured `home-turrets-off` at 433/1024 and `barrier-seal-off` at 399/1024 —
removing what we already ship COST us. Under this frame those are not evidence that
defence is good; they are evidence that our **current dose is at or below** the
countervailing-advantage point, and they say nothing about the next unit. **The dose
question is the only question, and no number in this repo answers it.**

**The countervailing advantage in our ruleset is nameable and short.** Our median kill
is r174 and our median death r187. The only thing a defensive spend can legitimately buy
is *the thirteen rounds between those two numbers*, and the thing it must buy them FOR is
a raid already in contact. **If a defensive build is placed at a round where no raider is
forward, there is no countervailing advantage to name and the build is KillAll's second
sunken.**

**And "it offers initiative to the opponent" has a literal cost here that StarCraft does
not have.** Every gunner or sentinel adds **+0.20 to the single global additive team
scale factor**, inflating the price of every subsequent build of every type — including
the conveyor line and the harvesters that fund the kill. A turret is not merely a
resource that cannot attack; it is a permanent tax on everything that can.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**This tactic IS a bar, and it is stricter than ours in one way and weaker in another.**

* **Stricter:** ours asks only that median kill round not RISE. His asks that the
  defensive spend produce a named, positive advantage. A build that leaves the kill round
  flat and buys nothing passes our bar and fails his.
* **Weaker:** his has no measurement attached at all — see
  [`nobody-in-the-field-has-ever-measured-the-kill-round`](nobody-in-the-field-has-ever-measured-the-kill-round.md).

**The operational form for a prereg:** a defensive plank must state, in one line, *what
the protected window is spent on*, and that thing must be an event that lands INSIDE the
window. "Our core survives longer" is not a countervailing advantage; "our forward
sentinel gets its 4th shot off" is.

**What would show it slowed the kill:** median round of enemy-core-death rising between
control and treatment arms on the same pinned panel. That is directly measurable off our
replays and needs no new instrument.

## WHAT WOULD KILL IT

* **It is a ladder observation, not an experiment.** No A/B, no n, no population. Its
  authority is that its author ships a bot and watches thousands of games; that is
  anecdote with a good prior, and under `PROGRAMME.md`'s point 6 it can **prioritise** a
  plank and cannot **retire** one.
* **StarCraft's static defence produces no income and neither do our turrets — but
  StarCraft's has no cost-scale externality.** The "offers initiative" argument transfers;
  the magnitude does not.
* **The dose numbers (1 vs 5) are Brood War ZvZ constants.** Import the *shape* — a small
  integer cap tied to a named purchase — not the integer.

## BUILDER HOOK

**The smallest thing that tests it is a REPORT, not a bot change.** Over our existing
replay corpus, for every defensive build we make (home gunner, home sentinel, barrier
seal), emit the round it was built and whether any of our builders was within the enemy
core's vision at that round. **The fraction of our defensive builds made while we have
NOTHING forward is the fraction that has no countervailing advantage to name.** If that
fraction is high, the dose experiment writes itself; if it is near zero, this road is
already closed by our own behaviour and should be recorded as such (which is the outcome
that killed the adjacent heal-idle plank in two minutes of grep).

**See also** [`turtling-persists-because-nobody-punishes-it`](turtling-persists-because-nobody-punishes-it.md),
which is drawn from a different passage of this same article and answers a different
question (why turtling is *prevalent* on a bot ladder). The two do not overlap.
