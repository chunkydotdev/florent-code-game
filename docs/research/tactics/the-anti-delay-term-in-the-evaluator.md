---
tactic: (B) A CHEAP EVALUATOR TRICK THAT PUNISHES STALLING — run the next few turns with both sides doing nothing before scoring, so a move that merely POSTPONES damage scores no better than one that takes it
source: https://raw.githubusercontent.com/robostac/cg-code-royale-postmortem/master/README.md
origin: CodinGame Code Royale / robostac (1st place)
evidence: documented
transfers: partial
---
WHAT IT IS — The winner of a 200-turn kill-condition contest lists, as the first
bullet of his final evaluation function:

> *"First run two turns of simulation (with both queens doing nothing). This helped
> avoid moves that were just delaying (eg kiting knights round an empty site)."*

Referent: "This" is the two free-running simulation turns prepended to the
evaluation; "moves that were just delaying" are moves whose apparent value comes
from postponing a bad outcome rather than preventing it.

The mechanism is simple and worth stating plainly: if you score a position
immediately, any move that pushes the damage one turn further out scores better
than one that accepts it. Letting the world run forward with no input first
collapses that difference — a merely-postponed loss has already happened by the
time the score is taken.

He built it because he could see the failure mode in his own games, and in the same
postmortem he names the numeric knob he added for the same reason:

> *"The enemy hp was divided by 10 to encourage aggressive tower placement but
> discourage trading hp"*

> *"This division was added later after seeing a lot of games lost by 1 hp due to
> failed trades."*

Referent: "This division" is dividing the enemy queen's HP by 10 in the evaluation.
(The first of those two strings is already in this library from sweep 8; it is
repeated here with its second sentence, which sweep 8 did not carry and which is
the part that says *why*.)

WHY IT MIGHT TRANSFER — The principle applies; the implementation does not, and the
gap matters.

**We cannot run a simulation.** 10 ms per unit per turn, in Python, with no engine
access — there is no forward model to roll. So the literal trick is out.

**But the failure mode it corrects is measurable in our own state, cheaply.** Our
version of "a move that merely delays" is any spend that improves our position
against *this round's* threat without changing whether the siege resolves — most
obviously healing a besieged structure. Healing at 4.00 HP/Ti is the highest-return
action in the game *per round*, which is precisely why it dominates: it always
scores well locally and it never ends anything. A bot that greedily takes the
best-scoring action each round will heal forever and finish nothing, and that is a
1-round-horizon artifact, not a real preference.

The cheap analogue is a **trend test rather than a simulation**: compare a
structure's HP now against its HP N rounds ago from a store slot. If it is flat, the
healing is postponing, not winning, and should stop counting as progress. That is
the same instrument the abort rule in
[`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)
needs, pointed at our own structures instead of the enemy's — and one store slot
serves both.

WHAT WOULD KILL IT — In our ruleset, postponement is sometimes *exactly* the right
move: our terminal condition is a clock we win 57.2% of the time, so delaying until
round 1000 is a win condition, not a stall. robostac's contest had the same
structure and he still wanted the term — but he was 1st with a bot that could
finish, and we are not. Encoding an anti-delay term when delay is our winning road
would be trading our best branch for a worse one; see
[`the-grinder-is-a-legitimate-strategy`](the-grinder-is-a-legitimate-strategy.md).

The narrower and safer claim, and the one this file should be read as making: the
anti-delay test belongs on **offensive** actions only — it should stop us pouring
titanium into a siege that is going nowhere, and should never be applied to our own
defensive healing.

BUILDER HOOK — One store slot holding a besieged structure's HP from N rounds ago,
and one comparison. Flat HP under sustained fire means the heal is treading water;
that is the signal to stop spending on the exchange and take one of the two named
alternatives (abort to the clock, or raise the damage rate above the adjacency cap).
