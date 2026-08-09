---
tactic: THE SCORE PAYS INCOME — the substance you are scored on also generates the resource you fight with, so a lead compounds without conversion
source: https://github.com/Lux-AI-Challenge/Lux-Design-S2 (ChangeLog.md v2.0.0 and docs/specs.md, local raw fetch)
origin: Lux AI Challenge Season 2 (2023) — organisers' changelog, official v2.0.0 release
evidence: documented
transfers: no
---
WHAT IT IS — Lichen is Lux S2's **scoring** substance: *"After 1000 turns, the
winner is whichever team has the most lichen value on the map."* At v2.0.0 the
designers made it pay income as well. Under "Major Engine Changes":

> *"Each tile of lichen owned and connected to a factory gives 1 power to the factory each turn"*

The spec carries the same rule in the factory's per-turn block —
*"Gain power equal to the number of connected [lichen tiles](#lichen)"*.

Two other v2.0.0 changes sit in the same block and point the same way:

> *"Weather is removed"*
>
> *"It takes 20 lichen to grow to new tiles instead of 10 now."*

Read together the direction is unambiguous. Weather was the shared random shock
that periodically compressed the gap between a strong and a weak agent; removing it
takes the noise out. Doubling the growth threshold makes the *first* lichen dearer.
And coupling lichen to power makes every point of score you already own pay for the
next one. **The scoreboard became a production asset, so being ahead is itself a
rate advantage** — a lead snowballs rather than being defended.

And the same patch gave the leader a way to *remove* score, not merely out-grow it:
*"any addition of rubble onto a tile with [Lichen](#lichen) on it will automatically remove all of the lichen on that tile."*

WHY IT DOES NOT TRANSFER — We cannot make our score pay income, because we do not
write the rules. Filed as `transfers: no` on the mechanic.

**But the structural comparison is worth stating precisely, because it is easy to
get backwards.** Our first tiebreak key is *"most titanium collected"* — a
**cumulative** quantity — and titanium is also the substance that pays for
everything we build. So in one direction the coupling Lux engineered already exists
here: economic strength raises key 1 automatically, with no conversion step, which
is a large part of why our economy-first bot wins **57.2% of the 353 games that
reach r1000**.

The direction that does *not* exist here is the one Lux actually built. Their lichen
pays **power**, i.e. score converts back into capability. Our key 1 is a *ledger*, not
a stock: titanium already delivered and already spent still counts for the tiebreak
and buys nothing further. **Being ahead on key 1 confers no rate advantage at all.**
That asymmetry is the honest reading, and it argues against, not for, treating our
tiebreak lead as self-reinforcing.

WHAT WOULD KILL IT — One unprobed engine fact decides how much of the above is real:
whether titanium physically delivered to the core is the *same* quantity as the
global pool that pays build costs, or a separate accounting line. `CLAUDE.md` says
titanium *"moves physically through the map … separate from the global pool used to
pay build costs"*, while `official-docs.md` names key 1 as *"most titanium
collected"*. If delivered titanium credits the pool, the coupling is tight and the
paragraph above is right; if key 1 is a counter that is incremented independently,
it is even more of a pure ledger. **Neither reading is verified here and neither is
claimed** — this is a builder probe, not a library fact.

BUILDER HOOK — none for the mechanic. One cheap probe falls out and is worth running
before anyone builds against key 1: **deliver a stack to the core in an isolated
match and read `get_global_resources()` on the same and the following round.** That
settles whether key 1 and the spending pool are one number, which several claims in
this library quietly assume in opposite directions.
