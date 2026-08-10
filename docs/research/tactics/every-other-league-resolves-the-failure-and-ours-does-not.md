---
tactic: (A) THE STRUCTURAL ANSWER — in every league surveyed the ENGINE resolves a bot failure (eject, freeze, forfeit, remove), so there is nothing for an opponent to detect. Ours is the outlier: our failure is PARTIAL, SILENT and PERMANENT, and the match plays on
source: https://raw.githubusercontent.com/Lux-AI-Challenge/Lux-Design-S2/main/specs.md
origin: Lux AI S1/S2 specs; Halite II rules deep-dive (2017.halite.io via web.archive.org); Terminal (forum.c1games.com, C1Ryan, 2018, via web.archive.org); SSCAIT and BASIL ladder rules; Battlecode 2021 (Wololo postmortem) for the resumable-bytecode case
evidence: documented
transfers: yes — as the reason the detection question has no imported answer
---

WHAT IT IS — sweep 21 asked how competitors detected that an opponent had crashed, stalled
or gone passive. **In six of seven surveyed leagues the question cannot arise, because the
engine ends the ambiguity itself.** The rules say so, in each league's own words:

| league | what the engine does to a failed bot | verbatim |
| --- | --- | --- |
| **Halite II** | ejects it | *"Any bot that issues a malformed command or does not respond within the allotted time is ejected."* |
| **Lux AI S1** | freezes it after a 60 s overage bank | *"Upon using up all 60 seconds and going over the 3-second limit, your agent freezes and can no longer submit additional actions."* |
| **Lux AI S2** | freezes it **and awards the loss** | *"Upon using up all 60 seconds and going over the 9-second limit, the agent freezes and loses automatically."* |
| **Terminal** | retires the algo from the ladder | *"An algo that has ‘crashed out’ will not play any more matches."* |
| **SSCAIT** | immediate loss | *"A bot loses immediately under these conditions:"* … *"If it crashes."* |
| **BASIL** | loss, and the game still counts | *"A crash counts as a loss, unless both bots crash."* |
| **Battlecode 2021** | loses the turn, **resumes next round** | *"halt its code for the round and take no action, and proceed the next round where its code left off, losing one round’s worth of action."* |

*(The Terminal quote is Correlation One staff member C1Ryan replying in the official forum
thread "Computing time issues", 28 Dec 2018; the surrounding sentence establishes the
referent — "The reason we need to include time outs as a regular ‘crashing’ algo is so that
we can ‘crash out’ while loop algos, which are fairly common." Curly quotation marks are
the source's. The SSCAIT list continues "If it slows down the game significantly." with
explicit frame thresholds. Lux S1's limit is 3 s/turn and S2's is 9 s/turn; both banks are
60 s per game.)*

**The pattern is exceptionless in the surveyed set: a failure is ALL-OR-NOTHING and the
engine adjudicates it.** Either the whole agent is gone (Halite, Terminal), or the whole
agent stops (Lux), or the whole match ends (SSCAIT, BASIL), or nothing durable happened at
all (Battlecode 2021 resumes where it left off). **In none of them does a bot spend the
next 700 rounds playing on with a hole in it.** That is why 22 Battlecode postmortems
contain no opponent-failure detector — see
[`no-postmortem-in-twenty-two-detects-an-opponent-failure`](no-postmortem-in-twenty-two-detects-an-opponent-failure.md).

WHY IT MIGHT TRANSFER — because OUR engine is the exception, and this is the whole finding:

- **Our uncaught exception destroys ONE UNIT, permanently, and the team plays on.** That is
  a *partial* failure with no engine adjudication, no result change, and no announcement.
  **No surveyed league produces that state, so there is no imported detector to copy and
  none should be expected.** Anyone searching the field for "how did they detect it" is
  searching for something the field's rules made impossible.
- **Our CPU overrun is the other half and is also partial**: the unit's turn is silently
  discarded and the unit is fine next round. Closest to Battlecode 2021 — except Battlecode
  *resumes the same computation*, and we do not.
- **So the observable has to be built from OUR primitives, and it is a counting problem,
  not a copying problem.** The two candidate signatures both fall out of the engine facts
  we already measured: an enemy builder that **disappears while at full HP with no
  attacker adjacent** (exception), and an enemy unit that **holds a legal, obviously
  available action for N consecutive rounds** (overrun or hung state machine). Both are
  ours to define; neither has a precedent to lean on.
- **And the exploitation side is on-programme.** Loki wants the core dead by round 250.
  A verified hole in the enemy builder population is a reason to press the plant and the
  core, not a reason to bank. The defensive reading — "they are weak, so I can safely
  turtle" — is explicitly OFF-PROGRAMME and should not be built.

WHAT WOULD KILL IT —

- **The table is about ENGINE behaviour, not about what bots did with it**, and it should
  never be cited as evidence that detection is valuable. It is evidence that detection was
  *unavailable elsewhere*. Those are different claims and only the second is supported.
- **Partial failure may still be undetectable in practice for us.** A builder vanishing at
  full HP is also what `self_destruct()` looks like from outside, and our own reference
  lists self-destruct as a legal builder action with no damage dealt. **Any detector must
  survive that confound**, and until someone shows the two are separable from the outside,
  the signature is a hypothesis.
- **Vision is the binding constraint and it is small.** A builder bot sees r²=20 and the
  core r²=36. Watching an enemy builder for N consecutive rounds means keeping it in
  someone's vision for N consecutive rounds, which is itself a commitment of a unit that
  the programme would rather have pressing the core.

BUILDER HOOK — instrument first, and it is corpus work rather than a bot change: **we
already have the disappearance signature measured** (224 undamaged builder vanishings per
10,000 border-tile builder-rounds for four teams; 0 in 2,334,017 non-border builder-rounds;
six other teams 722,545 border rounds and zero). **The unbuilt half is the second
signature: in the replay corpus, does an enemy unit's action-idleness for N consecutive
rounds predict anything?** Cut it per team, and include the self-destruct control above.
If idleness carries no signal in the corpus, the detector half of this sweep is dead for
the price of a query and no bot code was written.

Related: [`the-unresponsive-opponent-repeats-its-last-action`](the-unresponsive-opponent-repeats-its-last-action.md) ·
[`the-stuck-counter-is-the-universal-primitive`](the-stuck-counter-is-the-universal-primitive.md) ·
[`battlecode-destroys-the-robot-too-and-its-own-spec-says-otherwise`](battlecode-destroys-the-robot-too-and-its-own-spec-says-otherwise.md)
