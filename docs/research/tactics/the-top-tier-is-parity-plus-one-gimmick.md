---
tactic: The top tier shares one general game plan and differentiates by exactly one mechanism each
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 / Just Woke Up (winner); with BC2024 cout for clout and BC2025 SPAARK on the "degree" side
evidence: documented
transfers: partial
---
WHAT IT IS — **The winner of BC2025 answers (B) with both halves in one sentence**, and it is the
most useful formulation found:

> *"While the general game plan was basically the same for all teams, the top teams all had some
> creative gimmicks in their bots that helped differentiate them, whether it was a rush strategy,
> tower flickering, defense towers, or some other whacky strategies, don't be afraid to try
> something different."*

**Base plan shared; one differentiating mechanism each.** Not "more of the same", and not "a
whole different kind of bot" — a common floor plus one thing nobody else is doing. The same
author is explicit that the *low-level* axis is not what separates the top: *"You can do well in
battlecode without any of these wild optimizations and algorithms"* (referent: the loop
unrolling, exotic pathfinding and bytecode tricks he has just listed as intimidating).

**Two sources land on the "degree" side and are filed here rather than opposite.** BC2024 cout
for clout: *"Most teams use the same ideas; it’s the execution of those ideas that make most of
the difference, only possible through careful analysis of scrimmages and your code."* BC2025
SPAARK: *"just taking all the game constants at face value is enough to be competitive with top
teams"*, and *"you can implement whatever macro the top teams are using and quickly rise to the
top"*.

**The reconciliation these three permit — and it is a reading, labelled as mine:** the shared
plan is *necessary and gettable* (copy it; SPAARK says it rises you to the top), and the gimmick
is what orders teams *within* the top. That is a two-stage model, and it says which stage we are
at matters enormously for what we should build.

WHY IT MIGHT TRANSFER — **It reframes our own measurement.** Our defensive shape is *more of the
same* as the mid-field's — collar occupancy 67.3% versus 53.2%. On this model that is stage one
executed hard, with **no stage two at all**, which is consistent with sitting at the top of the
mid-field and not above it. The PROGRAMME is already pointed at stage two by name — *"We need to
find good tricks we can use, poisonings, exploits, manipulations, anything that seems to have a
shot at killing teams in the first 250 rounds, and lean into that hard once we find it"* — so
this source is direct external support for the Loki directive's *shape*, independent of whether
any particular trick works. Note also that every gimmick the winner lists (rush, tower
flickering, defence towers) is **cheap and narrow**, not a rewrite.

WHAT WOULD KILL IT — **Two of the three gimmicks he names were rule-edge exploits that the
organisers then removed**, which bounds their shelf life; his own team's tower-flickering
experiment is described elsewhere in the same document as *"promptly nerfed into the ground"*.
More importantly, **a gimmick is only load-bearing on top of parity in the shared plan** — and
this library's standing arithmetic says our shared-plan parity is not established: we run a
damage-to-repair ratio of 1.11:1 against the field's 2.79:1, and INDEX's *"Everything about us
breaks at r150."* A differentiating trick bolted to a bot that loses the base game converts a narrow loss
into a variance-heavy one, which is exactly
[`all-in-variance-is-a-ladder-tax`](all-in-variance-is-a-ladder-tax.md). This file therefore
argues for stage two **and** says the corpus does not license skipping stage one.

BUILDER HOOK — Before choosing a gimmick, run the stage-one check: for each of the five 1950+
teams, is our *base* profile (economy curve, structure count, damage-to-repair ratio) at parity
on comparable maps, or behind? If behind, the reading of this file is "fix the shared plan
first". If at parity, the file says pick **one** narrow mechanism and commit — and per
[`read-your-constants-off-a-stronger-bot`](read-your-constants-off-a-stronger-bot.md), the
cheapest way to find candidates is to look at what each top team does that the other four do not.
