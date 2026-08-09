---
tactic: What underdogs report as WASTED — adopted top-tier strategies that did not survive the transplant
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 / cout for clout; with BC2023 don't @ me and BC2022 5 Musketeers
evidence: documented
transfers: partial
---
WHAT IT IS — The brief asked what teams reported as **wasted**, not only what worked. This is the
answer, and it is the counterweight to
[`read-your-constants-off-a-stronger-bot`](read-your-constants-off-a-stronger-bot.md).

cout for clout adopted two separate strategies straight from the top of the ladder and discarded
both. On the first, and note the stated *reason* for adopting it:

> *"Because we idolize every single top team, we decided to try it as well. Although this
> strategy allowed us to place more traps, these traps were much less efficient, and it only did
> better against a few teams, so we got rid of it."*

(The referent of *"it"* is a levelling scheme they had just observed in *"a lot of top teams,
including buhg and Super Cow Powers"*.) On the second, adopted from the same source: *"Turns out,
using 3 ducks to sit on your spawn makes you lose just about every micro battle."*

**BC2023 don't @ me name the mechanism behind the failures:** *"you have to actively attempt to
improve upon the “inspired” algorithm, or else it’ll never be as good or better than the team
that you took it from."* A copied component competes against the original *plus* everything else
that team built around it.

**And the mirror-image warning for the other underdog road — the one-off exploit.** BC2022 5
Musketeers beat a much stronger team with a rule-edge trick: *"On one scrim, we faced Kryptonite,
who was a very highly ranked team. We sacrificed and got a sage, which proceeded to immediately
kill a nearby Archon. With the early lead, we took the game in only a few hundred rounds."* Their
verdict on it: *"However, we found this to generally be inconsistent"*, and a balance patch
retired it. BC2025 Just Woke Up's tower-flicker upset over *"an unbeatable God"* was likewise
*"promptly nerfed into the ground"*.

WHY IT MIGHT TRANSFER — **It puts a prior on both underdog roads at once.** Road one (copy the
top tier) fails when the copied piece was load-bearing on machinery we do not have; road two
(one-off exploit) produces real upsets and does not persist. Against our ruleset the first is the
sharper warning: the top of our league likely runs turret and healer densities tuned to a
**damage-to-repair ratio near the field's 2.79:1**, and importing their build mix into a bot
running **1.11:1** would buy the structures without the sustain that keeps them alive — which the
heal arithmetic prices at a 2.2:1 loss. The second warning is a schedule note for Loki: an exploit
found today should be assumed to have a **short life**, so its value is realised only if it is
shipped quickly.

WHAT WOULD KILL IT — **Both cases are single-team, single-season anecdotes with no control**, and
cout for clout's own conclusion elsewhere in the document is the *opposite* headline (*"Most
teams use the same ideas; it’s the execution of those ideas that make most of the difference"*) —
so the same team both copied successfully and copied wastefully, and reports no rule for telling
them apart in advance. **The one discriminator visible across the cases is testable, and it is
mine as inference, not sourced:** the copies that failed were ones whose *value depended on
surrounding competence* (efficiency of trap placement, winning micro battles), while the copies
that succeeded were **constants and orderings** — build ratios, when to expand, XSquare's micro
taken as a whole module. Our own patch of the game where copying is safest is therefore the same
one Generalized Strokes Theorem identified: **macro numbers, not behaviours.**

BUILDER HOOK — A rule rather than a plank: any constant lifted from a top-tier replay is shipped
**only if it does not also require a behaviour we have not measured ourselves as competent at.**
Concretely — copy their harvester or turret *count* at round N, do not copy a placement doctrine
whose value depends on micro we have never instrumented. And per the sweep-14 file
[`all-in-variance-is-a-ladder-tax`](all-in-variance-is-a-ladder-tax.md), any exploit-class plank
carries a shelf-life note in its own commit message.
