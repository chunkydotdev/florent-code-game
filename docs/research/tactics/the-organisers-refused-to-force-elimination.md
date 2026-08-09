---
tactic: (D) NEGATIVE, AND THE REASON IS THE INTERESTING PART — numeric forced-elimination timers were proposed to organisers with concrete numbers and VETOED, on the stated ground that surviving without fighting is legitimate play
source: https://web.archive.org/web/20180115195925/http://forums.halite.io/t/addressing-the-desertion-meta-in-4-player-games/482
origin: Halite II (2017); organiser decision recorded at https://api.github.com/repos/HaliteChallenge/Halite-II/issues/246
evidence: documented
transfers: partial
---
WHAT IT IS — Halite II's community hit our exact complaint — games decided by
players who hid rather than contested — and asked the organisers for a rule that
would force decisiveness. The proposals, verbatim as three list items in the forum
thread:

> *"Loss triggered after not controlling any planet for X turns. (proposed X = 40)"*

> *"Loss triggered after not controlling any planet if the game is past Y turns. (proposed Y = 75)"*

> *"Rank 2 to 4 is determined by total number of ships produced."*

Referent: the thread is titled *"Addressing the desertion meta in 4 player games"*;
the "desertion meta" is players hiding surviving ships to outlast rivals instead of
contesting the board. The organisers opened GitHub issue #246 to track it. It was
**closed 2017-11-09T14:58:47Z, and the closing comment is the veto** (timestamps
match exactly), from `j-clap`:

> *"I veto any change related to this. Survival is part of the meta, and I think
> that if these guys can run away and ewirkerman can't, than that played into the
> meta."*

Referent: "this" is the set of proposed rule changes above — the two loss-trigger
timers and the ranking rework. (`than` for *then* is the author's typo, quoted as
written.) The day before, `lidavidm` had already framed the timers as the wrong
instrument:

> *"I'm hesitant to drastically rework the ranking criteria, but the loss trigger
> conditions feel like band-aids to me, so I'm willing to entertain a new set of
> criteria."*

Referent: "the loss trigger conditions" are the `X = 40` / `Y = 75` proposals.

And one competitor supplies the argument that the meta is self-limiting, which is
the substantive counter-case rather than an appeal to taste:

> *"The current rules encourage everyone to program running away when they are
> nearly dead.  Once everyone programs that, that programming becomes useless, as
> when winner takes over all planets, the game will end, & the tie breaker (most
> ships produced?) will be enforced anyways for the multiple survivors."*

(The double spaces after `dead.` and `useless,` are in the source.) `lidavidm`
confirms the mechanism it rests on: *"One of the victory conditions is to control
every planet; if you fully dock a ship to every planet, the game ends there,
regardless of the number of surviving bots."*

WHY IT MATTERS HERE — This is the counterweight to
[`a-rising-hazard-makes-every-game-decisive`](a-rising-hazard-makes-every-game-decisive.md).
BC2020 shows organisers *can* force decisiveness; Halite II shows another set of
organisers *declining to*, deliberately, when asked, with numbers on the table. So
"designers believed decisiveness was the lever" is **not** a safe generalisation —
the field is split, and at least one design team treats not-fighting as a
first-class strategy rather than a defect.

Our ruleset sits on Halite's side of that split: there is no elimination timer, no
anti-stalemate cut, and a full score tiebreak. That is a design position, not an
oversight, and it means **the programme's incidence target is our choice about how
to win, not an alignment with what the ruleset rewards.** Compare
[`organisers-legislate-the-endgame-and-name-the-incentive`](organisers-legislate-the-endgame-and-name-the-incentive.md):
StarCraft AI tournaments legislate the endgame hard; Halite refused to.

The second-order point is the more useful one for us. `mellendo`'s argument is that
the hiding meta collapses **because there is a second win condition that the leader
can reach unilaterally** — occupy every planet, and the game ends regardless of who
is still alive. **We have no such condition.** Killing the core is our only
unilateral terminator, and it is the one the arithmetic prices out of reach. So the
mechanism that Halite's organisers relied on to make the problem self-correcting
does not exist here.

WHAT WOULD KILL IT — Halite II was a **four-player free-for-all**, where "desertion"
means outliving two rivals — a mechanic with no counterpart in a two-team game. Our
tiebreak cannot be gamed by hiding, because our keys are titanium delivered and
harvesters alive, both of which require playing the economy. So the specific abuse
these organisers were asked to fix is not our abuse, and their reasoning about it
transfers less cleanly than the fact of the refusal.

BUILDER HOOK — none. This is a framing correction: the library should stop treating
"the field forces decisiveness" as established. Two leagues, opposite decisions,
both documented.
