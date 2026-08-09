---
tactic: (A)+(B) THE PLAN AS A PRIORITY QUEUE WHERE EVERY STEP CARRIES ONE BIT — "may the plan step over me?" — plus a non-destructive skip cursor that advances attention without deleting the step
source: https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/BuildOrderQueue.h
origin: UAlbertaBot (StarCraft AI); the same class lineage in Steamhammer and CommandCenter
evidence: documented
transfers: partial
---

## WHAT IT IS

The dominant multi-step plan representation across the whole StarCraft bot family is a
**priority queue of build items**, and the interesting part is one field on each item:

> *"bool blocking = false; // whether or not we block further items"*

**(Quoted from the whitespace-flattened source; the file aligns the comment with tabs.)**

The queue then exposes exactly one operation that reads it:

> *"// is the current highest priority item not blocking a skip"*

inside `BuildOrderQueue::canSkipItem()`. And the skip is **non-destructive** — it advances a
cursor (`numSkippedItems`), it does not remove anything, and `getHighestPriorityItem()` resets
the cursor to zero every time it is called. The consumer loop in `ProductionManager` reads:
if we can build the head, build it and remove it; **else if `canSkipItem()`, skip and try the
next**; else break.

**So a plan step carries its own answer to "is this a hard ordering constraint or a
preference?"**, set by whoever queued it. `queueAsHighestPriority(m, blocking)` and
`queueAsLowestPriority(m, blocking)` both take the bit as an explicit argument.

**The same architecture is what Steamhammer and CommandCenter inherited**, and the library's
other sweep-18 files record what each of them then did with it: Steamhammer added a jam
detector and a drop rule; CommandCenter added a recursive prerequisite repair and no
replanning at all.

## WHY IT MIGHT TRANSFER

`transfers: partial`, and the partiality is the honest part.

- **The transferable atom is the bit, not the queue.** Whatever multi-round intention we
  express, the useful question is per step: *if I cannot do this now, may the rest of the plan
  proceed without me?* Buying ammunition before a push is skippable. Standing on the tile the
  turret is going to occupy is not. **That is one boolean per step and it needs no
  structure.**
- **The non-destructive skip is the right default for us specifically.** Our costs rise
  monotonically with what we have built (one global additive team factor), so an unaffordable
  step this round may be affordable next round *only* if we did not spend in the meantime —
  and deleting the step means we forget we wanted it. A cursor keeps the intention and moves
  attention.
- **It is the structural counterpart of the abort files.** The bit answers "may I be stepped
  over"; [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md)
  answers "am I still valid"; [`drop-the-step-you-cannot-do-and-reorder-around-it`](drop-the-step-you-cannot-do-and-reorder-around-it.md)
  answers "what if I never become valid". Three orthogonal one-liners.

## WHAT WOULD KILL IT

- **A queue is exactly the object this sweep's strongest negatives are about.** Its
  maintainer calls head-of-line blocking the primary bug surface of the whole bot family —
  *"Production freezes are one of the most serious classes of bugs in UAlbertaBot."* — and
  the author of Locutus, the same lineage, wrote *"Longer-term I think I'm leaning towards not
  having a queue at all after the opening, and instead just deciding each frame what is most
  important to build."* **Filing the queue as a representation without filing that is
  dishonest, which is why this file is `partial`.**
- **StarCraft's build tree is deep and ours is flat.** Their queue exists because buildings
  have prerequisites and producers are scarce. **We have no prerequisites and no producers** —
  any builder bot can build any building on any adjacent legal tile — so most of what a build
  queue is *for* does not exist here.
- **Our per-turn cost is the wrong shape for a shared queue.** A team-level queue would have
  to live in the 16-integer store, where writes are buffered one round and **last writer
  wins**. Two builders popping the same item is not a hazard the source ever had to consider.
  A **per-unit** queue on the `Player` instance is safe; a team queue is not, without a single
  designated writer.
- **No measurement.** The `blocking` bit is a shipped design with no ablation anywhere.

## BUILDER HOOK

Not a queue. The smallest useful extraction is **the bit alone**: wherever the bot has a
multi-step intention expressed as a sequence of `if` branches, tag each branch as blocking or
skippable and make the non-blocking ones fall through instead of returning. Parity first —
with everything tagged blocking, behaviour must be byte-identical to today. Then flip the
obviously-skippable ones (ammo conversion, opportunistic heal) and measure whether idle
unit-turns fall, which `positions.tsv` and the round-level action decode already expose.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/BuildOrderQueue.h
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/BuildOrderQueue.cpp
- http://satirist.org/ai/starcraft/blog/archives/348-production-freezes.html
- http://satirist.org/ai/starcraft/blog/archives/531-Steamhammers-improved-queue-reordering.html

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
