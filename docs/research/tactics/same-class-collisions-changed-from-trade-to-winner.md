---
tactic: THE DESIGNER'S FIX — same-class combat changed from mutual destruction to a winner-takes-the-tile rule, so a fight produces a survivor instead of a trade
source: https://github.com/Lux-AI-Challenge/Lux-Design-S2 (ChangeLog.md v2.0.0 and docs/specs.md, local raw fetch)
origin: Lux AI Challenge Season 2 (2023) — organisers' changelog, official v2.0.0 release
evidence: documented
transfers: no
---
WHAT IT IS — The clearest designer statement in this haul about making combat
produce winners rather than trades. Under `### v2.0.0`, "Major Engine Changes",
the before and after are written in the same bullet:

> *"When handling collisions, if two units of the same weight class move onto the same tile, previously they both were destroyed."*
>
> *"all units with less power are destroyed and the unit with the most power in the collision loses half of the power of the unit with the 2nd most power"*

The shipped spec states the same rule twice over, once for the cross-class case and
once for the same-class case:

> *"Heavy robots that end their turn on a square with only other light robots will destroy all the light robots and leave the single heavy robot unaffected."*
>
> *"If multiple units move onto the square, then the unit with the most power survives. Moreover, that unit loses power equal to half the power of the unit with the second most power in the collision."*

The shape is worth naming precisely. **Before**: engaging a peer costs you your
unit and costs them theirs — a pure trade, and a trade is never worth taking when
you are ahead. **After**: engaging a peer costs you a *fraction of a stock you can
regenerate* (power) and costs them the whole unit. The designers converted the
price of aggression from a capital loss into an operating expense, which is what
made attacking a positive-sum move for the stronger side.

WHY IT DOES NOT TRANSFER — Our engine has no unit-on-unit collision resolution to
change, and we cannot change it if it had. More decisively: **builder bots cannot
attack builder bots at all**, so the entire class of interaction this patch governs
is absent from our ruleset. There is no version of this we can build.

**The residue is a diagnosis, not a tactic, and it is the reason the file is filed
rather than dropped.** Lux S2 pre-2.0.0 is our position expressed in a different
currency. Our attrition arithmetic — healing 4.00 HP/Ti against a best damage of
1.80 HP/Ti, a **2.2:1 defender's edge**, rising to 4.4:1 on a stacked tile — means
every titanium-symmetric exchange we initiate is worse than a trade: it is a
donation. Lux's designers looked at exactly that incentive and concluded the fix was
a **rules change**, because they could see no bot-side answer. They were the only
party who *could* fix it.

That is a real constraint on our programme, and it should be read alongside
[`pay-for-the-capture-with-no-economic-return`](pay-for-the-capture-with-no-economic-return.md).
17A's answer is a deliberately un-economic term in the evaluator; Lux's answer was
to change the economics. **Only one of those two is available to us**, and this file
is the evidence that the designers of a comparable league did not believe the first
one was sufficient on its own.

WHAT WOULD KILL IT — The `transfers: no` is killed only if our engine turns out to
have a same-tile contest we have not measured. The library's engine facts say the
opposite: builder attacks target buildings on an orthogonally adjacent tile, and the
one displacement primitive (the launcher) is measured to produce **displacement plus
at most one shot, never a kill** (~1 throw in 200). There is no contested-tile
mechanic to exploit.

The *residue* would be killed by a measurement showing our exchanges are not in fact
symmetric — i.e. that concentration beats the 2.2:1 in practice. INDEX already states
the crack: **the defender's heal is adjacency-capped at ~16 HP/round per tile while
the attacker's damage on that tile is capped only by titanium.** If that holds, we
have a bot-side answer Lux's designers did not have, and this file's pessimism is
overstated.

BUILDER HOOK — none directly. The transferable question it poses is narrow and
answerable from the corpus with no bot change: **in our own core-kill games, was the
killing sequence ever a symmetric exchange, or is every one of them a concentration
that beat the per-tile heal cap?** If it is always the latter, the "trade" framing is
the wrong model of our combat entirely and this file's analogy should be retired.
