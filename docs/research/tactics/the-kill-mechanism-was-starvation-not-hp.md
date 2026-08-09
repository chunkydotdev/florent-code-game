---
tactic: TRANSFERS: NO — Lux S2's base kill is resource starvation, not HP attrition, which is why its entire denial literature does not import
source: https://github.com/Lux-AI-Challenge/Lux-Design-S2/blob/main/docs/specs.md (local raw fetch)
origin: Lux AI Challenge Season 2 (2023) — organisers' specification
evidence: documented
transfers: no
---
WHAT IT IS — Lux S2 factories have no hit points and cannot be shot. They die from
running out of water, and the spec says so in one sentence, inside the factory's
per-turn resolution block:

> *"If there is no water left, the nuclear reactor that powers the factory will explode, destroying the factory and leaving behind 50 rubble on each of the 3x3 tiles."*

That is the whole kill mechanism, and it is confirmed by the same machine count as
Lux S1: over the S2 specification, case-insensitively and whitespace-flattened,
`attack` **0**, `damage` **0**, `combat` **0**, `kill` **0**, `health` **0**,
`weapon` **0**, `shoot` **0**, `hp` **0**. The elimination clause reads
*"If any team loses all of their factories, they automatically lose and the other
team wins."* — so **the only route to a decisive win in Lux S2 runs through the
opponent's water supply.**

This is the load-bearing fact about the whole Lux S2 corpus, and it is the reason
this file exists rather than being a footnote. Every S2 competitor's aggression —
ry_andy_'s ice conflicts, Tigga's ice camping, Philipp Kostuch's Heavy-count
superiority, adamslay's denial meta — is **the same single tactic in different
clothes: interpose your units between an enemy factory and its ice.** They are not
independent convergent evidence for denial. They are four accounts of the one
mechanism the rules make available.

WHY IT DOES NOT TRANSFER — Our core has **500 HP and no upkeep**. Machine-checked
over the whole of `docs/reference/official-docs.md` (80,439 characters, flattened):
`upkeep` **0**, `starv` **0**, `deplete` **0**, `exhaust` **0**, `runs out` **0**.
There is no documented mechanism by which any of our entities dies from want of a
resource, and no documented mechanism by which an ore tile is used up.

**So denial here cannot kill anything.** Cutting an opponent's titanium slows their
production; it does not begin a countdown. Their core sits at full HP indefinitely
with zero income, and the game ends on the clock with them behind on key 1 rather
than dead. That converts every Lux denial finding from **how to win** into **how to
win the tiebreak** — a real thing, but a categorically different thing, and the
conversion has to be made explicitly in every file or the claim inflates. (Those two
phrases are mine, not quotations.)

The second-order consequence is the one that bites the programme. Lux S2's denial
strategies **raised decisiveness** because denial and killing were the same action
there. Ours cannot: a bot that perfectly starves our opponent still has to walk up
to a 500 HP core and shoot it, through a healing screen that wins the attrition race
2.2:1. **Denial and finishing are two separate purchases here and only one of them
is documented anywhere in the Lux corpus.**

WHAT WOULD KILL IT — Any engine fact establishing that ore tiles deplete, or that
harvesters/conveyors degrade without input, would open a genuine starvation road and
make the S2 corpus directly transferable. The negative above is a *documentation*
negative — zero hits in the organisers' own reference — not an engine probe, and it
should be labelled that way by anyone citing it. A single arena probe (build a
harvester, run 1000 rounds, count stacks emitted) settles it.

BUILDER HOOK — none, and that is the point. This file is the discount factor for
every other Lux file in this sweep: **when a Lux writeup says "kill", read
"starve", and then ask what our equivalent purchase is.** In every case so far the
answer is *tiebreak key 1 or key 2*, never the core.
