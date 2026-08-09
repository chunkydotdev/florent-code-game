---
tactic: (C/D) THE CROSS-LEAGUE PATTERN — in three independent codebases the exact check we need was written, found too expensive, and commented out. The authors say so in the file
source: https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/movement/Movement.ts
origin: Overmind (Screeps); ChooChoo (OpenTTD NoAI, https://raw.githubusercontent.com/mkonstapel/choochoo/master/aystar.nut); Factorio Learning Environment (https://raw.githubusercontent.com/JackHopkins/factorio-learning-environment/main/fle/env/tools/agent/connect_entities/client.py)
evidence: documented
transfers: partial
---

WHAT IT IS — three codebases, three games, three authors who reached the check we
want and switched it off. This is not a tactic to copy; **it is a prior on what the
check costs.**

**1. Overmind wrote model-based execution monitoring for movement and disabled it.**
The comment survives in the file, and so does the TODO admitting the gap:

> *"// // verify creep is in the location it thinks it should be in"*

> *"// 	if (!(creep.pos.x == x && creep.pos.y == y)) { // creep thought it would move last tick but didn't"*

> *"// TODO: repath if you are not on expected next position"*

That is exactly the predict-the-effect-and-compare-it-to-the-observation mechanism
that the robotics literature treats as the standard method — see
[`detect-the-break-by-predicting-the-effect`](detect-the-break-by-predicting-the-effect.md).
The best-known open Screeps bot wrote it and left it commented.

**2. ChooChoo wrote a self-crossing check into its pathfinder and disabled it, and
the author states the accepted cost in the same comment.** Quoting the reasoning
whole rather than in pieces, since it is the whole point:

> *"MK: this is very expensive for long paths, and can it ever even"*

> *"happen? Yes, it can; say you exit a narrow pass and need to turn"*

> *"left, but the only way to do so is to go forward, loop to the"*

> *"right and cross over yourself."*

> *"Is it bad if it happens? Not sure. For ChooChoo, worst case the"*

> *"route might jam and we sell the trains. I'd rather have the"*

> *"(very significant!) speed boost to pathfinding."*

The code that would have prevented the self-crossing is directly below it, entirely
commented out (`// local scan_path = path.GetParent();` … `// if (mismatch) continue;`).

**3. The Factorio Learning Environment names belts facing one another and does not
enforce it.** Two `match` arms, one line apart:

> *"pass  # raise Exception("Cannot rotate non adjacent belts to face one another")"*

WHY IT MATTERS — against OUR ruleset specifically:

- **It is the strongest available evidence that these checks are expensive rather
  than unknown.** Nobody failed to think of them. Three authors thought of them,
  wrote them, priced them, and removed them. **Any plank here should be budgeted as
  if it will be expensive, and measured against the 10 ms limit before it is
  measured against Elo.**
- **But two of the three prices do not apply to us, and that is the constructive
  half.** ChooChoo's cost is *"very expensive for long paths"* — a scan of the whole
  path so far, at every expansion of an A* search. **We are not running A*; our
  median chain is 3 hops and our binding tile sits at Chebyshev 5 from our own
  core.** Overmind's cost is per-creep per-tick across a colony; **ours would be per
  builder on adjacent tiles only.** FLE's is not a cost argument at all — it is a
  `pass`.
- **And ChooChoo's accepted worst case is not available to us.** *"worst case the
  route might jam and we sell the trains"* — the trains are the expensive, mobile
  thing and the track is cheap and permanent. **In our ruleset the polarity is
  reversed: the corked conveyor is permanent and free to the enemy, and it withholds
  the resource for the rest of the match.** The binding-tile cut prices one cork at
  ~78 stacks of withheld emission against one stack visibly stranded. **So the trade
  ChooChoo took explicitly does not transfer, and taking it here would be a mistake
  that looks like following the field.**

WHAT WOULD KILL THE OPTIMISM ABOVE — I am comparing *our estimated* cost against
*their measured* cost, and neither of ours is measured. ChooChoo's author at least
had a profiler; I have an argument from chain length. **If a route walk turns out to
cost real milliseconds per builder per round, this file becomes a warning rather
than a green light**, and the honest reading is that three people who did measure
decided against it.

BUILDER HOOK — measure the check before shipping the behaviour. `get_cpu_time_elapsed()`
is in the API: run the terminus walk from
[`verify-connectivity-after-building-not-only-before`](verify-connectivity-after-building-not-only-before.md)
inside a builder's turn, do nothing with the result, and log microseconds against
the 10,000 µs budget. **That is a one-line experiment that settles the objection
this entire file raises**, and it should be run before any of the (A) or (C) planks
are built.
