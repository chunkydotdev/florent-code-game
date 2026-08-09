---
tactic: (B) THE BEFORE/AFTER THAT SHOULD DECIDE HOW WE ABORT — replanning from scratch on every disruption produced a bot that restarted forever and lost the matchup; classifying disruptions and patching the plan in place for the cheap ones won it
source: http://satirist.org/ai/starcraft/blog/archives/327-reacting-to-build-order-disruptions.html
origin: Jay Scott / Steamhammer (StarCraft AI), 2017; contrasted with UAlbertaBot and CommandCenter, which take the two opposite extremes
evidence: documented
transfers: yes
---

## WHAT IT IS

Steamhammer inherited UAlbertaBot's policy: any disruption invalidates the plan, so replan.

> *"When it loses a building or a worker, it throws away the now-broken production plan and
> calculates a new one from scratch, using BOSS."*

**Referent check.** *"it"* is *"The live version of Steamhammer, when playing terran or
protoss"*, the subject of the sentence. BOSS is the build-order search inside UAlbertaBot,
which Steamhammer forked.

His verdict, immediately after:

> *"It’s not a very effective method."*

**(Glyph note: the source uses a curly `’`. The ASCII form `It's` does not appear on the page
— a literal grep for it returns nothing, which is the per-string glyph trap in action.)**

**The failure mode is a restart loop.** The author's narrative: Stone (an opponent bot)
SCV-rushes, kills a worker, BOSS replans from scratch and produces a long economic plan; then

> *"Then Stone kills another worker, the build is interrupted again, and BOSS says"*

— and the plan restarts. The outcome:

> *"Steamhammer terran rarely gets a marine out before Stone beats it."*

**The fix was not a better planner. It was to stop replanning for cheap disruptions:**

> *"But if a worker is lost in the opening, we can replace it, and try to stay as close as
> possible to the original opening."*

> *"Steamhammer protoss now defeats Stone smoothly. You have to watch closely to see when it
> deviates from its opening book."*

**And the classification survives in the shipped code today**, in
`Steamhammer/Source/ProductionManager.cpp`. Cheap disruption — patch in place:

> *"// We lost a worker in the opening. Replace it."*
> *"// This helps if a small number of workers are killed. If many are killed, you're toast anyway."*
> *"// Still, it's better than breaking out of the opening altogether."*

Expensive disruption — abandon the plan:

> *"// We lost a building other than static defense or supply. It may be serious. Replan from
> scratch."*

**The two extremes are both live in the field, from the same original author.** UAlbertaBot
still replans on *every* worker or building loss:

> *"// if it's a worker or a building, we need to re-search for the current goal"*

and CommandCenter never replans at all — its `onFrame` contains

> *"// TODO: if nothing is currently building, get a new goal from the strategy manager"*

as an unimplemented TODO. **Three bots, three policies: always replan, never replan, and
classify. The one that classifies is the one whose author reports the matchup flipped.**

## WHY IT MIGHT TRANSFER

- **Our engine hands us the disruption events for free.** We do not get an `onUnitDestroy`
  callback, but a unit's own `run()` can compare `get_unit_count()`, its remembered
  neighbour ids, and `get_global_resources()` against last round's values in one comparison
  each. The classification is the cheap part; the discipline is the point.
- **The classes are easy to name here and they are not symmetric.** Losing a *builder bot* is
  our "lost a worker" — replaceable at `get_builder_bot_cost()`, and our core can spawn one
  per turn. Losing a *harvester or a forward turret* is our "lost a building" — it changes a
  tiebreak key or removes committed damage, and the plan that assumed it is genuinely dead.
- **Our cost scale makes the restart loop worse than his.** Cost scale is **one global
  additive team factor** that every build feeds, so a plan that restarts and re-buys keeps
  raising the price of everything, including the turrets any future plan needs. **A restart
  loop here is not merely slow, it is inflationary.**
- **It is the missing half of the abort files.**
  [`abandon-the-plan-on-a-progress-timeout`](abandon-the-plan-on-a-progress-timeout.md) says
  *when* to abort; this says *how much* to abort. The field's answer is: the smallest amount
  that restores validity.

## WHAT WOULD KILL IT

- **The evidence is a narrative, not a measurement.** *"rarely gets a marine out"* and *"now
  defeats Stone smoothly"* carry **no game counts and no win rates**. Population is
  Steamhammer versus one named opponent. It is a strong, specific, first-hand before/after
  from a bot author, and it is not a controlled experiment.
- **Our plans may be too short for the distinction to matter.** StarCraft build orders are
  long chains with prerequisites; ours have none. If our longest commitment is three rounds,
  a full restart costs three rounds and the classifier is overhead.
- **Classification is another place to be wrong.** Calling a serious loss cheap leaves the
  bot executing a plan whose premise is gone — the failure
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md)
  exists to catch. The two files must ship together.
- **The same author's wider position is that the whole architecture was the problem** — see
  [`the-planners-only-promise-is-terminal-not-temporal`](the-planners-only-promise-is-terminal-not-temporal.md)
  and *"The underlying problem is that the software architecture is fragile."* This fix made
  a fragile design survivable; it did not make it good.

## BUILDER HOOK

Smallest test, and it is a rule rather than a mechanism: wherever the bot currently abandons a
multi-round intention, add a two-way branch — **if the thing we lost is replaceable this round
(a builder bot), replace it and keep the intention; otherwise drop the intention.** Log which
branch fires. **The count of "we dropped a plan over a replaceable loss" events is the number
this file predicts is non-zero**, and if it is zero the road is closed for the price of one
counter.

## SOURCES QUOTED IN THIS FILE

- http://satirist.org/ai/starcraft/blog/archives/327-reacting-to-build-order-disruptions.html
- http://satirist.org/ai/starcraft/blog/archives/348-production-freezes.html
- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ProductionManager.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/ProductionManager.cpp
- https://raw.githubusercontent.com/davechurchill/commandcenter/master/src/ProductionManager.cpp

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
