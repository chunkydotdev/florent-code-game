---
tactic: The largest documented leap over a top tier was made with zero information about that top tier
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (eventual winner), corroborated from the opposite side by BC2020 confused
evidence: documented
transfers: partial
---
WHAT IT IS — **The single largest strength jump in the Battlecode corpus, and the team that made
it had never played the field it jumped over.** Java Best Waifu, on the bot they uploaded three
days before the seeding tournament:

> *"we literally didn’t play any scrim game against any top bot (our Sprint submission was stuck
> way below) and we didn’t know the meta. However, when we woke up the next day our bot was first
> in the rankings with more than 200 elo than any other bot."*

The mechanism, discovered after the fact rather than designed: *"the meta by the time consisted
almost uniquely of rush bots (with some turtle bots as well), and our bot did really good against
both"* — their crunch beat the turtles and their early drone beat the rushers.

**confused corroborate independently from the receiving end**, and their surprise is the point:
*"What was most surprising was that they were not a rush bot like virtually every other top team,
but they were a lattice bot."*

**Two things follow, and they pull in opposite directions.** (1) **For (B): this is the strongest
"different in KIND" case in the corpus.** The field was rush-and-turtle; the bot that went 200
Elo clear was neither, and each of its two mechanisms happened to answer one of the field's two
strategies. (2) **For (C): it is a negative on opponent modelling.** They had no scrim data, no
meta knowledge, and no opponent model, and it did not cost them — because their edge was
**structural** (a composition that beats both dominant shapes) rather than **informational**.

WHY IT MIGHT TRANSFER — **It is the existence proof that the gap can be crossed in one step, and
it says what kind of step.** The road it points at is not "learn more about sporks"; it is
**"find the composition that beats what the whole top tier has in common"**. That is a
strategic-parity question we can attack with the corpus rather than with games: what do the five
1950+ teams *all* do, and what beats that? Our ruleset offers at least one structural asymmetry
of the right flavour — the **sentinel line ignores obstacles while the gunner line does not**, a
measured engine fact, meaning a defence built to blank gunners does not blank sentinels. Whether
the top of our league is homogeneous enough for a single answer to beat all of them is exactly
the measurement this file demands first.

WHAT WOULD KILL IT — **Three cautions, and the first is decisive on its own.** (1) **This is
survivorship in its purest form.** We hear from Java Best Waifu because their untested gamble
won; the postmortems of the teams whose untested gambles lost were never written. The corpus
cannot tell us the base rate, and sweep 15's measured negative — INDEX's *"NOBODY, ANYWHERE,
SEPARATED CAUSE FROM MARKER — and that is measured, not asserted."* — applies with full force. (2) **The mechanism was luck by their own account**:
they did not know the meta, so the counter-fit was accidental. Reproducing it deliberately is a
different and harder act than what they did. (3) Their leap happened in **an offence-dominant
season with cheap, mobile, continuously-producible damage**, which sweep 14 established is
precisely the precondition our ruleset lacks; our damage is immobile, must be paid for and cannot
retreat.

BUILDER HOOK — A homogeneity measurement, from the corpus, no bot change: across the five 1950+
teams, how similar are they to *each other* on the readable macro axes (opening build mix,
turret-to-economy ratio, forward placement distance, ammo conversion schedule)? **If they are
tightly clustered, one structural counter can in principle beat all of them and this file is
live. If they are as different from each other as they are from us, there is nothing common to
counter and the road is closed** — record that as a measured negative, which is the more likely
outcome and still worth having.
