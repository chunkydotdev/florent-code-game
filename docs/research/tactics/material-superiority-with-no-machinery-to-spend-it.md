---
tactic: AHEAD ON MATERIAL WITH NO MACHINERY TO SPEND IT — a 6th-place author's own post-mortem: the mid-game advantage existed, the code to convert it into a kill did not
source: https://www.kaggle.com/competitions/lux-ai-season-2/writeups/philipp-kostuch-some-notes-on-a-pure-logic-approac
origin: Lux AI Challenge Season 2 (2023) / Philipp Kostuch, 6th place, pure-logic bot
evidence: documented
transfers: yes
---
⚠ **TIER 2.** Read through a text proxy, **not diffed against Kaggle's original
HTML**. The string verifies verbatim against the local bytes.

WHAT IT IS — In his own list of what he would fix, a 6th-place finisher describes
holding a material lead he had no routine to convert:

> *"I should in theory be able to focus fire a single factory overwhelming it with 6+ Heavy before turn 500 and maybe taking out a factory early"*

The bullet's opening clause frames it as a standing advantage rather than a
possibility:

> *"advantage throughout the midgame, should use this to create attackers to disrupt ore mining (maybe even ice mining)"*

His writeup's own title concedes the same thing at the top level: *"lots of focus on
domestic admin, not enough on fighting"*.

**The structure is the finding.** The units were affordable. The advantage was
persistent. The target was identified. The *"globalised attack code structure"* — his
words — already existed to route them. What was missing was any part of the bot that
*decided to do it*. He finished 6th of 646 on economy alone and knew it.

Compare his neighbour in the same bullet list: *"often I find 6+ of them huddling
around an obviously beaten factory while the factory 1-over isnt delichened"* (his
typo). **Both failures are the same shape** — the force exists, and the allocator does
not point it at the win condition.

WHY IT MIGHT TRANSFER — This is 17A's central finding arriving from a fourth
independent direction, and it arrives as **self-diagnosis by a strong competitor**
rather than as an outside inference, which is a stronger evidence class than most of
what this library holds.

17A: *an economically-correct evaluator never finishes*, because the last increment of
kill progress has no economic return. Philipp is that evaluator describing itself. He
had superiority; his allocator kept finding domestic work with a positive return; the
attack never got scheduled. Steamhammer, Jay Scott's oddshrimp and BC2020's crunch all
say the same thing from the winners' side. **Four leagues, four authors, one shape.**

And the mapping onto our measured position is close to exact. The library's standing
context:

- **We bank and do not spend** — we end r200-300 holding more titanium than Ouroboros
  while buying a twelfth as much ammunition. That is the material superiority.
- **The economy is not our constraint at all** (sweep 8). That is the "advantage held
  throughout the midgame".
- **We die in the middle game** — conditional on a core kill, the chance it is ours
  rises 29% → 55% → 72% → 76%, and 353 games reach r1000. That is the missing
  conversion.
- **`sporks`, #1 at 2082, builds 1.99 gunners per side-game — we build 1.95.** We are
  not under-buying weapons. We are under-*directing* them.

The consequence is the one thing this file is for: **the gap is not resources and it
is not unit count. It is that no code path exists whose job is to spend a lead on the
win condition.** Every other file in this sweep proposes a lever; this one says the
missing part is a *decision*, and that a bot can be 6th in the world without it.

WHAT WOULD KILL IT — Two things.

1. **The claim is counterfactual and untested.** *"I should in theory be able to"* is
   the author's belief about a bot he did not build. He never ran it. It is evidence
   that a strong competitor **diagnosed** the gap, not evidence that closing it wins.
   Nothing here should be cited as "focus-firing early works".
2. **Our conversion may be genuinely harder rather than merely unscheduled.** His 6+
   Heavies were mobile, reassignable and could retreat. Our damage is immobile, must
   be placed inside the enemy kill zone, cannot retreat, and faces a 2.2:1 defensive
   edge (4.4:1 stacked). If our conversion attempts already happen and already lose,
   the diagnosis is execution and not accounting — and **the library has never
   separated those two readings.** That separation is the highest-value unrun cut in
   this sweep.

BUILDER HOOK — no bot change; run the separating cut. **In our own replays, count the
games where we held a material lead in the middle game (r150-400) and classify what we
did with it**: attempted an assault and lost it, attempted nothing, or converted. The
three buckets point at three different fixes, and the library currently assumes the
second without having counted. If bucket 2 dominates, Philipp's diagnosis is ours and
the fix is a scheduling term. If bucket 1 dominates, this file is a red herring for us
and should be marked so.
