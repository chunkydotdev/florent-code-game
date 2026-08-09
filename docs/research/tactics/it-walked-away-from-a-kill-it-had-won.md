---
tactic: THE CONVERTER GAP, OBSERVED BY THE AUTHOR — a 2nd-place bot released a target it was already winning against, because nothing in its priority system priced "this one is nearly dead"
source: https://www.kaggle.com/competitions/lux-ai-season-2/writeups/tigga-yet-another-logic-bot
origin: Lux AI Challenge Season 2 (2023) / Tigga, 2nd place
evidence: documented
transfers: yes
---
⚠ **TIER 2.** Read through a text proxy (the local artifact carries the proxy's
`Title:` / `URL Source:` / `Markdown Content:` header), **not diffed against Kaggle's
original HTML**. The string verifies verbatim against the local bytes; byte-identity
with what Kaggle served is not established.

WHAT IT IS — In his own list of things his bot does wrong, the 2nd-place finisher
records a bot that **abandoned a won kill**:

> *"For example, I've seen it stop camping the ice of a factory with very low water where camping it would have killed the factory."*

The context is his section on *"better attack/defend priorities"*, of which he says
*"It's not really focussed enough right now."* The example is his own illustration of
that failure, not a separate complaint.

Note exactly what this is. It is **not** a bot that lost a fight, was outplayed, or
mistimed an attack. It is a bot that had already paid the whole cost of an assault —
the units were in position, the camp was established, the target was at *"very low
water"* — and then **reallocated them away one step before the payoff**, because its
priority function scored the camping units against alternative uses each turn and
never scored the fact that the target was about to die.

That is 17A's structural finding restated from the inside by a top-2 competitor. **A
per-turn allocator that reprices its units every turn will withdraw from any assault
whose payoff is discontinuous**, because the marginal round of camping is worth
nothing until the last one is worth everything. The only fix is a term that survives
the reallocation — a latch, a mode, or a sunk-progress bonus — which is the same
prescription 17A extracted from Steamhammer's `enemySeemsToBeDead()` and BC2020's
crunch.

WHY IT MIGHT TRANSFER — This is the most directly applicable item in the Lux haul,
because it is a **control-flow** finding, not a mechanics finding, and control flow
is portable across rulesets in a way that starvation kills are not.

Our version of the camping unit is the forward turret and the builder detail that
services it. The library's measured facts say we do exactly what Tigga describes:
**everything about us breaks at r150** on five independent instruments, raider
survival collapses 43 → 6 rounds, forward placement falls off, and we *"bank and do
not spend"*. Those are the signature of an allocator that stops paying for an
in-progress assault the moment the per-round return looks bad — which, under a 2.2:1
defensive edge, it always does.

And the cost of the error is **larger** for us than for him, because our assault
capital is immobile. A Lux camping robot that is reassigned still exists and still
mines. Our forward sentinel that stops being serviced **dies**, and its 30 Ti and its
contribution to the one global cost scale are gone. **Withdrawal is not free here;
it is the most expensive way to lose the titanium we already spent.**

The transferable rule is narrow and cheap: **once an assault is under way, the
decision to continue must not be re-derived from the same per-turn economics that
would never have started it.** Latch it, and gate the *exit* on evidence — the target
healing back up, the detail dying — rather than on the marginal round looking
unprofitable.

WHAT WOULD KILL IT — Two things.

1. **We may not have the bug.** Tigga's is an observation about *his* bot. Ours may
   never start assaults at all, in which case there is nothing to abandon and the
   fix is upstream. The r150 breakage pattern is consistent with both readings and
   the library has never separated them. **This is the cut that decides whether this
   file is actionable or moot.**
2. **A latch is a hazard under our arithmetic.** A committed attack that cannot be
   re-evaluated is exactly the 2.2:1 donation the library warns about, and 17A's
   `if-the-push-fails-fall-back-to-the-clock` exists because our tiebreak road is the
   one we actually win. The correct object is a latch **with an evidence-gated exit**,
   not a latch. Building the first without the second would be a clean regression.

BUILDER HOOK — Corpus, and it is small: **find every sequence in our replays where an
enemy structure dropped below one round of our incident damage and survived, and
classify what our units did on the following round** — kept firing, retargeted, or
left. If retarget-and-leave is common, we have Tigga's bug exactly and the latch is
the cheapest fix in the library. If the sequences barely exist, the problem is that we
never get there, and this file should be re-pointed at initiation instead.
