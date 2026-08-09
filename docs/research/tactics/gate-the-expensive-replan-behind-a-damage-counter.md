---
tactic: (B) Two independent Flatland winners gate full replanning behind an ACCUMULATED-DAMAGE COUNTER, not behind the disruption event — and one of them measured the net, not the gross
source: https://jiaoyangli.me/files/2021-ICAPS.pdf
origin: An_old_driver / Li, Chen, Zheng et al., "Scalable Rail Planning and Replanning: Winning the 2020 Flatland Challenge" (ICAPS 2021); independently in Mugurel-Ionut Andreica, "Winning Solution of the AIcrowd SBB Flatland Challenge 2019-2020", https://arxiv.org/pdf/2111.07876
evidence: documented
transfers: partial
---

WHAT IT IS — Flatland injects malfunctions that break a running plan. Both winners
answered the same way, and neither replans on the disruption.

**First response is HOLD, to preserve the ordering rather than the schedule:**

> *"MCP (Ma, Kumar, and Koenig 2017) avoids such deadlocks by stopping some trains to maintain the ordering with which each train visits each cell. It guarantees that all trains can reach their target cells within a finite number of timesteps."*

**Local repair is layered on top of hold, and it is scoped by intersection, not by
proximity:**

> *"When train ai encounters a new malfunction at some timestep, we collect all intersections that train ai visits in the future and then collect all trains that visit at least one of these intersections after train ai ."*

**And they measured it — twice, on two named fixtures.** Round 1:

> *"Empirically, adding the partial replanning technique reduced the flowtime on 261 instances, with an average reduction of 19.9%."*

Round 2 — and this is the line that makes the file worth filing, because it is a
**net** number after the repair's own runtime is charged:

> *"On our server, partial replanning consumed 1,965 seconds on these instances and improved their accumulated reward by 4.812. Eventually, we solved 2 fewer instances within 8 hours but improved the accumulated reward by 3.629."*

**Andreica arrived at the same architecture independently, gating the expensive
mode behind a counter of degradations rather than behind the event:**

> *"If the path update logic increased the maximum time when an agent reaches their destination (or the number of agents reaching their destination decreases), then a counter is increased. If this counter exceeds 3, then the path-regeneration logic is run in “full mode”"*

He also states, plainly, that he does not model future breakage at all:

> *"Please note that the shortest-path algorithm is always optimistic, meaning it doesn’t consider any future malfunctions when planning the agent paths (only the ongoing malfunctions are considered)."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **It is the same shape sweep 18 landed on from a different literature** —
  `classify-the-disruption-before-you-replan` and `abandon-the-plan-on-a-progress-timeout`.
  **A third and fourth independent instance, in a logistics competition, is
  meaningful corroboration that the shape is right and a queue is not.**
- **The 4.812 → 3.629 line is the discipline our own repair plank needs.** Repair
  won on the gross number and then gave back a quarter of it in runtime, costing
  two whole instances. **Our runtime currency is 10 ms per unit per turn and a turn
  that overruns is silently discarded** — so our version of "we solved 2 fewer
  instances" is "some builders did nothing that round, invisibly." **Any repair
  plank must be priced with `get_cpu_time_elapsed()`, not just with titanium.**
- **"Optimistic planning" licenses the simplest possible route builder.** Both
  winners plan as if nothing will break and fix it when it does. That is an
  argument against ever trying to route conveyors *around* likely enemy fire — a
  temptation our forward-turret data would otherwise invite.

WHAT WOULD KILL IT —

- **Their disruptions are transient and ours are permanent.** A Flatland
  malfunction ends; a destroyed conveyor does not come back on its own. **"Hold and
  preserve the ordering" has no analogue for us** — there is nothing to hold; the
  tile is gone. So the top rung of their ladder is inapplicable, and only the
  gating idea transfers.
- **Their budget is 8 hours of server time for a whole episode.** Ours is 10 ms per
  unit per round. **The absolute costs do not transfer at all; only the practice of
  charging them does.**
- **`transfers: partial` and not `yes` for one specific reason:** the counter they
  gate on counts *degradations of a plan they are holding*. **We hold no plan**, so
  the analogous counter has to be defined from scratch — most plausibly on our
  delivered-titanium EMA (see
  [`detect-the-break-at-the-till-not-on-the-line`](detect-the-break-at-the-till-not-on-the-line.md))
  — and that mapping is my inference, not theirs.

BUILDER HOOK — before any repair behaviour ships, add the accounting: log
`get_cpu_time_elapsed()` at the end of a builder's turn in games with and without
the repair branch, and report the delta in microseconds and in discarded turns.
**A repair plank whose CPU cost is unmeasured is the 4.812 without the 3.629.**
