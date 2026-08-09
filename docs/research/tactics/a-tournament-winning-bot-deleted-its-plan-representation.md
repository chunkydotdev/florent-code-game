---
tactic: (D) A top-3 StarCraft bot deleted its entire declarative plan DSL — 221 files and 8,596 lines removed in two days — and its win rate a year later was unchanged
source: https://github.com/dgant/PurpleWave/commit/b0235feefe2e (and e7fa283f39db)
origin: PurpleWave / Dan Gant — 1st SSCAIT 2018-19 and 2019-20, 2nd AIIDE 2024, 3rd AIIDE 2025
evidence: documented
transfers: yes
---

## WHAT IT IS

PurpleWave's own architecture document describes a hierarchical plan tree, and it is the
most-cited public description of a top StarCraft bot's plan representation
(`https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Readme.md`):

> *"Decisions are structured roughly as a
> https://en.wikipedia.org/wiki/Hierarchical_task_network"*

> *"The strategy is specified as a tree of goals ("Plans"). A Plan may have a series of
> sub-goals, which it may attempt to fulfill one-at-a-time or all at the same time."*

> *"Plans have an implicit priority based on their structure in the goal tree. Higher
> priority plans get first dibs on the resources they need, while lower-priority plans may
> have to wait."*

> *"all resources are only made available to Plans via mutex locks"*

> *"When a Plan wants a unit to achieve a goal, it gives that unit an Intention."*

> *"The Intention is a very loose statement of purpose which, executed literally, would lead
> to fairly naive behavior."*

**⚠ THAT DOCUMENT IS STALE AND THE STALENESS IS THE FINDING.** `src/Readme.md` has **exactly
one commit in the repository's history, dated 2017-04-10** (GitHub commits API, path-filtered
— checked by this sweep). The architecture it describes was deleted in 2024.

**The deletion, from the GitHub commits API, two commits one day apart:**

| sha | date (author) | message | additions | deletions | files removed (as listed) |
|---|---|---|---|---|---|
| `b0235feefe2e` | 2024-10-22 | **`Deleted declarative gameplans!`** | 124 | **6,726** | 82 |
| `e7fa283f39db` | 2024-10-23 | **`Deleted declarative gameplan DSL!`** | 399 | **1,870** | 139 |

**Totals: 523 additions against 8,596 deletions, 221 files removed.** Among the files removed
by the second commit are the plan combinators themselves —
`src/Planning/Plans/Compound/If.scala`, `FlipIf.scala`, `Parallel.scala`, `Trigger.scala` —
and every per-matchup `GamePlans/**` class. A third commit the same day,
`9cfe4b3170d1`, reads **`Removed prioritization from scheduling. Removed priority from build
order logic.`** — i.e. the mutex/priority machinery the README describes went too.

**And it was built deliberately two years earlier.** The same repository's commit history
contains, on 2022-09-14, `Added new declarative syntax for strategies` and `Converted PvT/PvP
to declarative strategies`. **This is a build-then-delete cycle inside one top-tier bot.**

**What replaced it is straight-line imperative code re-run every planning tick.** The base
class is now 18 lines with no children and no completion concept
(`src/Planning/Plans/Plan.scala`), and gameplans are:

> *"abstract class GameplanImperative extends Plan with Modal with MacroActions"*

whose `onUpdate()` is a sequence of unconditional calls (`RequireEssentials()`,
`executeBuild()`, `autosupply()`, `doWorkers()`, `executeMain()`), gated only by

> *"final def isComplete: Boolean = completed || ! activated"*

**Did it cost anything? The organisers' own results files say essentially no.** Parsed by
this sweep from the AIIDE competition data (`results/results_summary_json.js` at
`davechurchill.ca/starcraft/aiide/results/<year>/`):

| competition | data timestamp | PurpleWave rank | win % | wins / games |
|---|---|---|---|---|
| AIIDE **2024** (pre-deletion) | `2024-10-22 [18:18:29]` | **2nd of 10** | **82.29** | 2,970 / 3,609 |
| AIIDE **2025** (post-deletion) | `2025-11-04 [20:00:41]` | **3rd of 11** | **82.95** | 2,826 / 3,407 |

**The 2024 results file is timestamped hours before the first deletion commit, so the 2024
entry is unambiguously the pre-deletion bot.** Win rate moved **+0.66pp**. The rank change is
accounted for by a different bot improving: Stardust went 74.19% → 83.71% over the same
interval.

## WHY IT MIGHT TRANSFER

- **It is the single strongest piece of evidence in the library against building a plan
  representation for its own sake.** An author who had one, who documented it publicly, and
  who was winning tournaments with it, deleted 8,596 lines of it and stayed in the top three.
- **It matches our own project's history exactly.** The library's standing observation is
  that *every gain on our current line came from removing a mechanism, never adding one.* This
  is the same result from the outside, in a stronger league, with the diff sizes public.
- **It is a warning about our own documents, not only his.** `src/Readme.md` has been quoted
  as current architecture for seven years while describing something deleted. **Our library
  should treat any architecture description that is not co-located with the code it describes
  as potentially stale, and check the commit history before citing it.** This sweep nearly
  filed the HTN description as a live finding.

## WHAT WOULD KILL IT

- **This is a before/after, not an ablation, and the confounds are large.** The 2024 and 2025
  fields differ (AutoPilot out; VOID and C0mputer in), the map pool may differ, and **every
  other bot also changed.** Nothing here establishes that the deletion was neutral *causally*
  — only that PurpleWave's aggregate win rate did not fall. Stone & Veloso's own line applies:
  *"Since competitions are not controlled experiments, their results are not presented as
  scientific validation of our individual techniques."*
- **The author gave no reason.** The commit messages are four and five words. There is no
  postmortem, no issue, no blog post found by this sweep explaining why. **Anything about
  motive is inference and is not claimed here.**
- **Deleting a DSL is not the same as deleting planning.** PurpleWave still re-derives a full
  multi-step production timeline every planning tick (`MacroSim`), still holds persistent
  `Production` objects across ticks, and still runs a genuinely persistent multi-step
  `MissionDrop` FSM. **What was deleted is the declarative composition layer, not the
  ability to act over multiple frames.** See
  [`the-blackboard-is-a-one-tick-bus-not-a-memory`](the-blackboard-is-a-one-tick-bus-not-a-memory.md).
- **Scala. Ten thousand lines of Scala DSL is a maintenance burden a hobbyist may drop for
  reasons unrelated to strength.** Our `main.py` is not carrying that cost, so the argument
  "it was deleted therefore it was worthless" does not follow.

## BUILDER HOOK

None to build. The usable form is a **prior for the next planning-shaped plank**: the field's
strongest bot deleted 8,596 lines of exactly this and lost nothing measurable. Any proposal
to add a plan-composition layer here should state, up front, what it does that a mode index
plus per-round arithmetic cannot — and the cheapest way to find out is the disagreement-rate
print in
[`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md).

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Readme.md
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Gameplans/All/GameplanImperative.scala
- https://api.github.com/repos/dgant/PurpleWave/commits/b0235feefe2e5... and .../e7fa283f39db... (commit messages, stats and file lists read from the GitHub API)
- https://davechurchill.ca/starcraft/aiide/results/2024/results/results_summary_json.js
- https://davechurchill.ca/starcraft/aiide/results/2025/results/results_summary_json.js

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). The standings tables were machine-parsed from the
organisers' own JSON data files, not read off a rendered page.
