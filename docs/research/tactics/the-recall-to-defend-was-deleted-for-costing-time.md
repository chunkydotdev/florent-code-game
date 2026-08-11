---
tactic: FAILURE MODE (arm C) — "pull the attackers home when the base is threatened" was tried in several forms by a semifinalist and DELETED, with the stated reason being time, not effectiveness
source: https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
origin: Battlecode 2023 don't @ me; corroborated by Battlecode 2022 5 Musketeers
evidence: documented
transfers: yes
---

## WHAT IT IS

The most common defensive plank in strategy games is the recall: when home is threatened,
bring the strike force back. **In this corpus it is tried repeatedly and it does not
survive, and the reported cause is TEMPO.**

> *"We cycled through several strategies involving HQ defense, such as having launchers
> regroup at HQ when enemy units are sighted"* … *"but ultimately we realized that falling
> back to defend HQs wasted far too much time, and rarely if ever gave us a competitive
> advantage."*

**Read the two clauses in order, because they are not the same claim.** *"wasted far too
much time"* is a **cost** finding — the travel is the price. *"rarely if ever gave us a
competitive advantage"* is a **benefit** finding — the defence, when it arrived, did not
matter. **They are the only author in the corpus to report both sides of the trade for a
defensive plank in the same sentence, even though neither side carries a number.**

**5 Musketeers (BC2022) reached the same place by a different route and their failure
mode is mechanical rather than economic** — already filed in full as
[`defence-recall-oscillation`](defence-recall-oscillation.md). Their first design wasted
units (*"after defending an attack, they sat around and did nothing"*); their second
design, recalling a fraction of the strike force on a distress beacon, *"led to an
unfortunate oscillation problem"*. **Together the two form the pattern: the naive recall
costs travel, the fixed recall costs stability, and the semifinalist who tried it hardest
deleted it.**

## WHY IT MIGHT TRANSFER — against our ruleset

**Our version of the recall is more expensive than theirs, for a rule-level reason.**
A builder bot **acts XOR moves** each turn. A BC2023 launcher travelling home still had
its attack available on arrival in the same tick-economy; our builder walking home spends
one *action* per tile of the journey, so the recall's price is denominated in exactly the
currency the kill is paid in. **On a 30x30 map a cross-map recall is tens of forward
actions, one-for-one.**

**And there is nothing at home that a returning builder is uniquely good at.** It cannot
damage an enemy builder (its attack targets an adjacent *building* for 2 Ti / 2 damage);
it can heal (+4 HP for 1 Ti to an adjacent friendly) and it can build. Both are things a
builder that never left could do. **The recall buys presence, not capability.**

**This is the same conclusion sweep 23 reached from the opposite direction and it is
worth noting the two arrived independently.**
[`every-withdrawal-trigger-in-the-field-is-a-resupply-trigger`](every-withdrawal-trigger-in-the-field-is-a-resupply-trigger.md)
found that every shipped dwell limiter in the field is keyed to a carried consumable, and
our builder carries none — so there is no *supply* reason to go home. **This file adds
that there is no *defensive* reason either, and it adds it from a team that tested it.**

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**The recall class fails the bar by construction and this is the clearest such case in
the sweep.** Its mechanism IS the removal of offensive presence for a number of rounds
equal to the travel time. There is no version of it whose kill-round cost is zero, and
the only open question is whether the survival return exceeds it. **don't @ me's answer
was that it did not, "rarely if ever".**

**⇒ Under the amended programme this road should be marked CLOSED-PENDING-EVIDENCE and
placed at the bottom of the queue, not reopened by the doctrine change.** The amendment
admits defence that does not slow the kill; a recall is the definition of defence that
does.

**What would show it slowed the kill, if anyone runs it anyway:** median kill round, and
beside it **mean rounds between a raider's consecutive forward actions** — the recall's
signature is a gap in forward action density that no other plank produces.

## WHAT WOULD KILL IT

* **Neither team reports a number.** Two qualitative deletions from strong teams is a good
  prior and not a refutation; under `PROGRAMME.md` point 6 a live leg would be needed to
  close the road properly. **This file prioritises, it does not retire.**
* **Their maps and ours differ in the variable that decides it.** BC2023 maps were large
  and their units fast relative to the map; our builders move one cardinal tile per turn
  on an 8x8–30x30 grid. **On our SMALLEST maps the travel cost is a handful of turns and
  the argument weakens considerably** — a map-width-conditional recall is the one form
  this file does not close, and `map-size-decides-whether-the-rush-is-legal.md` is the
  precedent for treating width as the discriminator.
* **A recall to a tile that is already on the raider's route home costs nothing extra.**
  [`commit-to-the-withdrawal-but-keep-working-en-route`](commit-to-the-withdrawal-but-keep-working-en-route.md)
  is the shape that survives, and it is not what either team tested.

## BUILDER HOOK

**None yet — deliberately.** The right next action is a grep, not a build: confirm that
the incumbent contains no recall-on-threat branch. If it does, this file is a candidate
DELETION with a measurable prediction (forward action density rises, kill round falls or
holds), which is far cheaper to test than an addition and is exactly the intervention
shape sweep 23 found three teams winning with.
