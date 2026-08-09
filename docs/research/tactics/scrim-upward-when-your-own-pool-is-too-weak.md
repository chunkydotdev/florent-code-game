---
tactic: When your local pool is dominated, test ONLY against opponents above you — and automate requesting it
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 / wololo (peaked 4th); corroborated by BC2025 Just Woke Up (winner), BC2026 Generalized Strokes Theorem (2nd), BC2025 SPAARK
evidence: documented
transfers: partial
---
WHAT IT IS — **This is the field's answer to question (C), and it is not "nobody solved it".**
wololo describes our exact predicament — a bot that beats everything it can reach locally, so
local results carry no information — and states the remedy in one sentence:

> *"I had to test purely by requesting scrimmages against high-ranked teams with the autoaccept
> scrimmages option on"* … *"as my new strategy demolished the locally ranked competition"*

He also records the cost, in his own footnote: *"Such teams were sometimes difficult to find;
many top teams turned the option off to avoid being flooded with scrimmages."* And in his
acknowledgements he names the two teams whose *defences* he was permitted to practise against —
*"for the constant challenge of their strong defenses that they allowed me to freely play
against (by keeping the auto-accept scrimmages on)"* — adding *"I tested my strategies against
them very often, and they were instrumental in the development of my code."*

**Three other teams reach the same place independently.** BC2025 **Just Woke Up (the winner)**
built the automation: *"I created a script that would automatically log in to the battlecode
website and request to scrimmage with as many enemy teams as I chose."* BC2026 **Generalized
Strokes Theorem (2nd)**: *"we would queue scrims against teams above us on the leaderboard"*.
BC2025 **SPAARK**: *"Scrimmage analysis is still more important than raw win rate against old
bots."*

WHY IT MIGHT TRANSFER — **Our pool problem is the one wololo names, stated in our own
PROGRAMME:** *"the probe pool is dominated (both arms win 87-90%)"*, and INDEX adds that our
opening is a near-constant (CV 0.09) while the field's is 0.26. Sweep 15 established that
self-play A/B inflates effects by roughly 2× and that the BC2025 winner overrode its own A/B
twice on exactly this ground. **wololo closes the loop: the documented behaviour of someone in
our position is to stop generating local numbers and start acquiring games against the band
above.** For us the ladder itself is the instrument — INDEX's standing conclusion after sweep 15
is that *"The arena is the only instrument — and that is now a SOURCED conclusion rather than a
default."* We are live on that arena as OpenSverige. The transferable content is
the *selection rule*: **request games upward, deliberately, rather than reading whatever the
matchmaker hands us.**

WHAT WOULD KILL IT — **The mechanism is an organiser-provided feature, not a tactic, and it may
simply not exist in our league.** Battlecode's scrimmage system lets a team request a specific
opponent and lets opponents opt in via auto-accept; if our ladder only offers rating-banded
automatic matchmaking, the *selection* half is unavailable and only the *reading* half survives —
i.e. mine the games against strong opponents we already have rather than commission new ones.
Two further limits, both from inside this corpus: **BC2026 lorem ipsum's pipeline ends at
*"we then start scrimming a lot of teams within our rating range"*, which is the failure mode
this file warns against, from a team that did not escape it**; and probing a specific strong
opponent has a documented cost of its own — see
[`probing-the-target-teaches-the-target`](probing-the-target-teaches-the-target.md).

BUILDER HOOK — Do not build anything yet: **first check whether our ladder exposes any opponent
selection at all.** If it does not, the plank is analytic — stratify the existing replay corpus
by opponent rating and treat only the top-band games as the verdict set, accepting the smaller n
rather than the larger-but-uninformative dominated pool. That is a change to *which games we
count*, which is free, and it is the part of wololo's practice that survives without the feature.
