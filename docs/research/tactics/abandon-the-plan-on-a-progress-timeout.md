---
tactic: (B) THE CHEAPEST ABORT PREDICATE THERE IS — "nothing has happened for N rounds, throw the plan away." It reasons about the plan not at all, it is one comparison, and its own author says it is not sufficient on its own
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ProductionManager.cpp
origin: Steamhammer (StarCraft AI); with the same shape independently in Battlecode 2020 confused, Battlecode 2023 no thoughts head empty / 2025 confused, PurpleWave, and Overmind (Screeps)
evidence: documented
transfers: yes
---

## WHAT IT IS

The brief asked for a cheap abort predicate. This is the cheapest one the field has, and five
leagues have it.

**Steamhammer runs a watchdog on plan PROGRESS, not on plan content:**

> *"// We didn't make anything. Check for a possible production jam."*
> *"// Jams can happen due to bugs, or due to losing prerequisites for planned items."*

> *"the.now() > _lastProductionFrame + Config::Macro::ProductionJamFrameLimit"*

> *"// Looks very like a jam. Clear the queue and hope for better luck next time."*

The threshold, from `Steamhammer/Source/Config.cpp`:

> *"int ProductionJamFrameLimit = 360;"*

360 frames — about 15 seconds at tournament speed. `_lastProductionFrame` is stamped on every
successful production. When the timer fires, the whole plan is discarded via
`goOutOfBookAndClearQueue()`, whose comment reads *"// We have finished our book line, or are
breaking out of it early."* and which also stamps the timer again with the comment
*"_lastProductionFrame = the.now();       // don't immediately clear the "jam" again"* — a
hysteresis so the abort cannot re-fire on the next frame.

**Two named exemptions stop the watchdog from firing on legitimate stalls**, and they are the
expensive part: a zerg saving for mutalisks while a spire finishes, and being supply-maxed
(*"// We can't produce most likely because we're maxed. Great news!"*).

**The same shape, four more times, in four more leagues:**

- **Battlecode 2020, confused** — a deadline on a search, not on production:
  > *"If after 180 rounds it still doesn't see the enemy HQ, it gives up on the rush and joins
  > the rest of the miners and do normal miner stuff."*

  **Referent check.** *"it"* is the first spawned miner, which the team designates *"the
  rusher"*; the quote is the last item of that unit's numbered behaviour list.
- **Battlecode 2023 no thoughts head empty and 2025 confused** — a *progress-failure counter*
  rather than a clock, on pathing: their bots switch from Bellman-Ford to bug navigation after
  failing to make progress (2025 confused: *"switching to the latter if Bellman-Ford failed to
  make progress for three consecutive turns"*).
- **Overmind (Screeps)** — a timeout is a field on every task object:
  > *"timeout    : Infinity, 	// task becomes invalid after this long"*

  and it is ANDed into the validity check:
  > *"validTask = this.isValidTask() && Game.time - this.tick < this.settings.timeout;"*
- **PurpleWave** — two state-conditional timeouts on the same plan, in one line each:
  > *"if (duration > Seconds(45)() && state != Raiding && state != Evacuating) {
  > terminate("Expired (not raiding)"); return }"*

  i.e. **45 seconds if the plan has not yet reached its paying phase, 90 seconds absolute.**
  A plan that is still all cost and no return is given a much shorter leash.

## ⚠ THE CAVEAT THE SOURCE ITSELF SUPPLIES, AND IT IS NOT A FOOTNOTE

Steamhammer's own author, writing about production freezes:

> *"Steamhammer tries to mitigate these by timing out and clearing the queue if nothing has
> been produced for too long, but that is not enough to save the game against a strong
> opponent."*

**Referent check.** *"these"* refers to *"most remaining permanent deadlocks"*, described in
the preceding sentence as caused by bugs in the strategy boss, information manager, production
manager or building manager, or their interactions. And his diagnosis:

> *"Production freezes are one of the most serious classes of bugs in UAlbertaBot."*

> *"The underlying problem is that the software architecture is fragile."*

**So the progress timeout is a backstop, not a design.** It converts a permanent stall into a
15-second stall. Against a strong opponent, 15 seconds is still fatal.

## WHY IT MIGHT TRANSFER

- **It is one integer of state and one comparison, and it needs no store slot.** Per unit:
  `self._last_progress_round[ct.get_id()]`, stamped whenever the unit does the thing its plan
  exists to do. Per team: one store slot holding the round of the last global milestone.
- **It fits the one thing our engine punishes hardest.** Our units get 10 ms and can lose a
  turn silently to a CPU overrun; a plan that is stuck produces no exception, no error, and
  no signal at all. **A stuck unit here is invisible unless something is counting rounds.**
- **PurpleWave's state-conditional variant is the one to copy, not the flat one.** Our
  offensive plans have exactly its shape — a phase that is pure cost (walking a builder
  forward, buying a turret inside the enemy kill zone) followed by a phase that pays. A
  45-versus-90 split maps directly onto "has this plan started doing damage yet".
- **It gives the library's existing deadline files a general form.**
  [`abort-the-scout-on-a-deadline`](abort-the-scout-on-a-deadline.md) and
  [`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)
  are two instances; the general rule is *time-since-last-progress*, which is strictly better
  than *time-since-start* because it does not punish a plan that is working slowly.

## WHAT WOULD KILL IT

- **The author's own verdict above.** A watchdog is a symptom-suppressor. If our plans stall
  often enough for it to fire, the fix is upstream.
- **The exemption list is where the work is, and getting it wrong is worse than no
  watchdog.** Steamhammer needs two exemptions; ours would need at least one — *saving up*.
  A bot deliberately banking titanium for a sentinel is making no progress by any cheap
  measure, and our library's standing observation is that **we bank and do not spend**, so a
  naive progress watchdog would fire constantly on our current behaviour and thrash it.
- **17A's asymmetry applies.** Aborting is free for a mobile army and not free for us: a
  turret bought toward an abandoned plan is 30 titanium that cannot be recovered
  (`destroy()` refunds nothing). **A timeout that aborts after the money is spent has saved
  nothing** — which is exactly why PurpleWave's short leash is on the *pre-commitment* phase.
- **Sweep 15's warning about clocks stands, narrowed by 17A:** a clock is a poor ARMING
  trigger and a good DISARM/DEADLINE trigger. This is a disarm trigger, so it is on the right
  side of that line — but only if what it disarms is a state with no natural exit.

## BUILDER HOOK

Smallest test, measurement first: for each builder bot, stamp the round it last performed its
plan's defining action (built, attacked, healed, or moved closer to its target) and `print()`
`round - last_progress` once per 50 rounds. **Read the distribution off the replay text.** If
our units routinely sit at 30+ rounds of no progress, we have a stall class nobody has named
and the watchdog is worth building. If the tail is short, the road is closed for the price of
a print. Only then add the abort, and make it **state-conditional** in PurpleWave's shape —
a short leash before any titanium is committed, a long one after.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ProductionManager.cpp
- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/Config.cpp
- http://satirist.org/ai/starcraft/blog/archives/348-production-freezes.html
- https://battlecode.org/assets/files/postmortem-2020-confused.pdf
- https://battlecode.org/assets/files/postmortem-2025-confused.pdf
- https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/tasks/Task.ts
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Tactic/Missions/MissionDrop.scala

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
