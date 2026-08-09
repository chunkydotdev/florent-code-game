---
tactic: THE FIELD EXPECTS ITS OWN KILL RATE TO FALL — a finalist's forecast that, given more time, the fully-formed defence would have become dominant and offence would have stopped working
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (finalist)
evidence: documented
transfers: partial
---
WHAT IT IS — By week 3 of BC2020, a defensive formation called the *cookie* had
appeared, and The High Ground record two things about it: that a completed one
could not be broken, and that they expected it to take over the game.

> *"When the cookie was fully set up as in Figure 6, it was almost impossible to
> break through, even if you terraformed to the other team. The only way to stop
> these teams was to harass them enough that they couldn’t get their cookie up."*

> *"cookies would be the dominant strategy as defense would prevail over offense"*

Referent and scope, because the second quote is a conditional and reads stronger
without its clause: the full sentence begins *"We think that if the tournament had
run a few more weeks,"* — a figure caption interrupts it in the PDF text, which is
why the tail is quoted separately. So this is a **forecast**, explicitly
counterfactual, made by a finalist about a season that ended before it could be
tested.

The unbreakability half is not a forecast; it is a report, and the *"even if you
terraformed to the other team"* clause matters — it says the defence held against
the strongest available approach, not merely against a bad one. The stated counter
is denial before completion, which the library already holds three independent
times ([`funnel-not-seal`](funnel-not-seal.md),
[`sustained-plant-removal-race`](sustained-plant-removal-race.md)). What is new
here is the **trend claim**.

WHY IT MIGHT TRANSFER — This is the field's own version of our unifying fact, and
it arrives with a direction attached. Our arithmetic (healing 4.00 HP/Ti against a
best damage of 1.80 HP/Ti, 2.2:1 to the defender, 4.4:1 on a stacked core tile)
says the defensive equilibrium is not an accident of the current meta but a
property of the numbers. The High Ground's forecast says that in a comparable
league, the *same drift* was visible to a finalist in real time and was expected
to complete.

The consequence for the programme is uncomfortable and worth stating: **if the
field's defence is still improving, our core-kill incidence is a moving target
moving away from us.** Sweep 16's measurement is consistent with this — the top
tier's defensive collar is *thinner* than ours (40.6% at ≥1900 against our 66.5%),
which reads at first as them defending less, but pairs naturally with them
defending *better per unit spent*. Either way, an incidence gain measured against
today's field should be expected to decay, and an A/B that shows +X pp on the
current ladder is not a promise of +X pp in a month.

It also sharpens where to spend. Every source in this sweep that reports a defence
being beaten reports it beaten **before completion**, never after. Our version of
"before completion" is the r0-150 window in which our build medians are a
near-constant and the field's are not — which is where
[`the-crunch-is-a-rate-race-not-a-damage-race`](the-crunch-is-a-rate-race-not-a-damage-race.md)'s
clearance phase would have to live if it is to live anywhere.

WHAT WOULD KILL IT — It is a counterfactual forecast by one team about a
tournament that did not happen, and it was **not** borne out in the visible
record: BC2020 was won by a terraform/attack bot, and the very next thing the same
postmortem describes is the field inventing crunch improvements. A forecast that
defence will win, made in a season that offence won, is weak evidence on its own.
It is filed because it agrees with an *independent* arithmetic argument in our own
ruleset, not because the forecast is authoritative.

The trend claim also has an obvious falsifier available in our own data and nobody
has run it: **core-kill incidence over calendar time on our ladder.** If the
field's kill rate against us has been flat for weeks, the decay is not happening
here and this file is a curiosity.

BUILDER HOOK — none in the bot. One corpus cut: core-kill incidence (ours and
against us) plotted against replay date, and against opponent rating band. Flat
means ignore this file; falling means every incidence gain needs a decay budget
and the ship gate should stop treating a one-shot A/B as durable.
