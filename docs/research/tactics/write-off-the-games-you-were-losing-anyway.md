---
tactic: Specialise into the subset of the game where the strength gap is smallest, and concede the rest deliberately
source: https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf
origin: Battlecode 2026 / Lorem Ipsum (solo competitor; seed 36 → 55 → 14, qualified for the MIT finals)
evidence: documented
transfers: partial
---
WHAT IT IS — **The clearest statement of an underdog *policy* in the corpus, and it is a policy
about which games to lose.** Lorem Ipsum shipped an aggressive unconditional build ramp knowing
it was wrong on one whole map class, on an explicit ground:

> *"What my testing noticed is that games on closed maps generally were ones I was already going
> to loose, so I made the (risky) decision to implement this with hopes that it would give me a
> significant edge on open maps."*

He also names the axis on which the rating gap actually bit him, and it is not maps as such:
*"my bot seemed to do well on open maps with plenty of cheese with less influence from the
opposing side, whereas they generally did not do well in situations where there was head to head
combat (specifically with teams higher rated than me)"*. The specialisation then decided his
qualification: against a higher seed, *"their bot often beat ours on more combat designed maps,
where we would consistently beat them in larger open maps with a lot of cheese"*, and the match
fell his way because *"3 of which were maps where there was less interaction, which came to our
advantage giving us the win, and qualifying us for the final tournament at MIT"*.

**The reasoning is a dominated-option argument, not a gamble.** Effort spent making the
already-lost games closer buys nothing; the same effort spent widening the margin in winnable
games converts them. That is the underdog's version of the standard advice, and it inverts the
usual instinct to fix the worst matchup first.

WHY IT MIGHT TRANSFER — **We are the party with a large dominated set and we have never named
it.** Against a 360-500 Elo gap, some fraction of our games against the top band are unwinnable
on any plank we could ship this week; effort that improves those is spent for nothing. The
policy says the first act is a *partition*: which games against strong opponents are actually
close, and what do they have in common? INDEX already gives one candidate axis in our favour —
**353 games reached r1000 and we won 57.2%**, i.e. we are *strong* in the long-game/tiebreak
regime and weak in the middle. That is exactly the shape lorem ipsum exploited: he leaned into
*"less interaction"* and away from head-to-head combat, which is where being outclassed shows up
most. The direct analogue here is leaning on **titanium delivered**, the first tiebreak key, in
matchups where the mid-game kill is not available — and it costs no new mechanism.

WHAT WOULD KILL IT — **Three limits, and the second is in tension with our own directive.**
(1) He could not choose maps and neither can we; the policy only pays if the favourable class is
a large enough share of the pool, and his qualification is explicitly attributed in part to luck
(*"We got lucky in said qualifying match"*). (2) **It runs against `KILL_WINDOW_RND: 250`.** The
regime this file says we are strong in is the one the PROGRAMME is steering away from — the clock
— and PROGRAMME is Magnus's call, not this library's. **The file is filed as evidence about what
underdogs did, not as an argument to change the directive**; the transferable half that does *not*
conflict is the partition step, which is diagnostic and directive-neutral. (3) Deliberately
conceding a map class is irreversible within a submission and its cost is paid every game of that
class — with the rating loss visible immediately and the gain only where the favourable class
appears.

BUILDER HOOK — The partition, from the corpus, before anything else: against the 1900+ band,
split our games into **close** and **not close** (by final resource differential, or by whether
the game reached r600) and ask what distinguishes them — map size, ore density, core distance,
seat. **The output is a definition of our winnable set.** Nothing is shipped from this; it tells
us which games any future plank should be evaluated on, which is the same instrument
[`scrim-upward-when-your-own-pool-is-too-weak`](scrim-upward-when-your-own-pool-is-too-weak.md)
asks for, applied one level finer.
