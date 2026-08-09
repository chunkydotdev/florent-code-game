---
tactic: (A) HOW TO RUN A SEARCH THAT DOES NOT FIT IN ONE TURN — an anytime search resumed across turns with a per-turn millisecond budget, a hard deadline counted in turns, a cheap fallback plan, and the whole thing inside a try/catch
source: https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/BOSSManager.cpp
origin: UAlbertaBot / BOSS (Build Order Search System), Dave Churchill
evidence: documented
transfers: partial
---

## WHAT IT IS

BOSS is the one genuine *planner* in the StarCraft bot family — it searches for a build
sequence achieving a goal. It cannot finish inside one frame, so the harness is built around
that fact, and the harness is the transferable part.

**The search is anytime and resumed, not restarted:**

> *"// tell the search to keep going for however long we have this frame"*

> *"// give the search at least 5ms to search this frame"*

> *"// call the search to continue searching"*
> *"// this will resume a search in progress or start a new search if not yet started"*

**Two budgets, on two different clocks.** Per frame, from `Config.cpp`:
`int BOSSTimePerFrame = 30;` — and the caller in `ProductionManager::update()` carries the
comment *"// 30 ms per search update"*. Across frames, from
`UAlbertaBot_Config.txt`: `"BOSSFrameLimit" : 160,` — enforced as

> *"bool searchTimeOut = (BWAPI::Broodwar->getFrameCount() > (m_previousSearchStartFrame + Config::Macro::BOSSFrameLimit));"*

**So: at most 30 ms of search per frame, and if no answer inside 160 frames, give up.**

**A fallback ladder, not a failure:**

> *"// so try another naive build order search as a last resort"*

and if even that throws,

> *"// and if that search doesn't work then we're out of luck, no build orders forus"*

(the typo `forus` is the author's) — after which it returns an empty build order rather than
crashing.

**And the whole search call sits inside an exception guard:**

> *"// catch any errors that might happen in the search"*

**Meanwhile the previously found plan stays in force.** `performBuildOrderSearch()` in
`ProductionManager.cpp` only installs a new build order when one exists —
`if (buildOrder.size() > 0)` — and otherwise starts or continues a search. **The bot never has
"no plan" while thinking.**

## WHY IT MIGHT TRANSFER

`transfers: partial` — the *harness* transfers cleanly, the *thing it is a harness for* is what
sweep 18's negatives are about.

- **Our budget is 10 ms per unit per turn and an overrun silently discards that unit's turn.**
  There is no way to ask for more. **The only way to afford an expensive computation here is
  to spread it across turns**, and this is the field's worked example of doing that.
- **The two-clock structure maps directly.** Per-turn: guard the loop with
  `ct.get_cpu_time_elapsed()` against a budget well under 10,000 µs. Across turns: a deadline
  counted in rounds, after which you take whatever you have. **Both numbers are ours to
  choose and both are cheap to enforce.**
- **The exception guard is not optional here, it is existential.** In StarCraft a thrown
  exception is a caught exception. **In our engine an uncaught exception permanently destroys
  that unit for the rest of the match.** Any speculative computation must be inside a
  `try/except` that falls back to the previous plan — and the fallback ladder above is the
  shape to copy: best answer, cheap answer, no answer, never a crash.
- **Keeping the old plan while computing a new one is the property that makes an expensive
  decision safe.** It costs one field on the `Player` instance.
- **This is the only affordable form of anything that looks like search here**, and it is the
  precondition for the one search shape the field found that worked — a single choice point
  over a handful of authored options (see
  [`the-htn-planner-lost-every-game-to-a-scripted-rush`](the-htn-planner-lost-every-game-to-a-scripted-rush.md)).

## WHAT WOULD KILL IT

- **The planner this harness serves is the one its own maintainer wanted to delete.** *"Of
  course I intend to drop BOSS when I get that far."* Filing the harness must not smuggle in
  the planner — see
  [`the-planners-only-promise-is-terminal-not-temporal`](the-planners-only-promise-is-terminal-not-temporal.md).
- **Our budget is per unit, not per team, and that breaks the analogy in an awkward place.**
  BOSS is one search for one bot. Ours would be one search per unit, or one search on one
  designated unit whose result the others read through the 16-slot store with **one round of
  latency and last-writer-wins.** A search spread over 20 rounds and published through a
  buffered slot is a plan that is 21 rounds stale when consumed.
- **State changes under a resumed search.** BOSS re-searches on unit loss precisely because a
  plan computed against a stale state is wrong. Any resumed computation here needs the same
  invalidation, which is
  [`classify-the-disruption-before-you-replan`](classify-the-disruption-before-you-replan.md).
- **We have nothing that needs 160 frames of search.** Our buildings have no prerequisites, our
  costs are closed-form, and our economy is arithmetic rather than simulation — the library
  established that in
  [`decide-by-simulating-both-branches`](decide-by-simulating-both-branches.md). **The honest
  reading is that this is a solution to a problem we do not currently have**, filed so that if
  we ever do, we do not invent the harness badly.
- **No measurement.** The budgets 30 ms and 160 frames are shipped constants with no published
  sensitivity analysis.

## BUILDER HOOK

None to build now. What is immediately usable is the **defensive half**: any block in our bot
that could plausibly be expensive should be (a) bounded by an explicit
`ct.get_cpu_time_elapsed()` check rather than by hope, and (b) wrapped so that a thrown
exception degrades to last round's answer instead of destroying the unit. That is a code
review, not a plank, and the library already records three opponents with conditional compute
blow-ups — Ouroboros discarding **26,356 unit-turns across 85 games, max 3,508 in one game** —
so the failure mode is real in this league even though it has never been ours.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/BOSSManager.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/ProductionManager.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/Source/Config.cpp
- https://raw.githubusercontent.com/davechurchill/ualbertabot/master/UAlbertaBot/bin/UAlbertaBot_Config.txt
- http://satirist.org/ai/starcraft/blog/archives/531-Steamhammers-improved-queue-reordering.html

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
