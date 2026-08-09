---
tactic: (B)+(C) THE ONLY MEASURED RECOVERY NUMBERS IN THE SWEEP — retry-in-place resolved 22% of failures, and a precondition timeout aborted 422 stuck actions whose distribution then localised the fault
source: https://kbsg.rwth-aachen.de/~hofmann/papers/icaart21-goal-reasoning-rcll.pdf
origin: Carologistics, "Multi-Agent Goal Reasoning with the CLIPS Executive in the RoboCup Logistics League", ICAART 2021
evidence: documented
transfers: partial
---

WHAT IT IS — the RoboCup Logistics League routes workpieces through a production
chain with mobile robots. It is the one source in sweep 19 that both **repairs** and
**detects** and **publishes numbers for each**.

**Repair, measured.** The sentence straddles a two-column split around a figure, so
it is quoted as two spans rather than elided into one:

> *"Execution Monitoring. We first consider retrying failed actions. There were 134 plan executions that"*

> *"contained at least one action retry; 22 % of those resolved the problem such that the respective goal was successful."*

**Detection, measured — and this is the one I would put in front of a builder:**

> *"Execution monitoring also aborted 422 actions that were stuck, because preconditions were not met until a timeout threshold was reached. 83 % of those stuck actions concern machine assembly steps, indicating a malfunctioning MPS or a misplaced workpiece."*

**Fixture, stated because both numbers are meaningless without it** — from the
paper's evaluation section: *"We evaluate the performance of our approach based on
both competitive and test games, providing data from three robots that accumulated
a total running time of about 36 hours."* Deliveries in that window were *"33 C0,
3 C1 and 6 C2 deliveries"*. So: three robots, 36 hours, competitive plus test games,
one team's own logs. **Not a controlled comparison of repair against rebuild — there
isn't one anywhere in this sweep.**

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The detector is a PRECONDITION TIMEOUT, not a throughput monitor, and that is
  the cheapest correct shape for us.** "This action's preconditions were not met for
  N ticks, so abort it" maps onto "this harvester has been due to emit for N rounds
  and has not". It needs no baseline, no EMA, and no comparison against history —
  unlike [`detect-the-break-at-the-till-not-on-the-line`](detect-the-break-at-the-till-not-on-the-line.md),
  which needs all three.
- **The second sentence is the part that generalises furthest: the DISTRIBUTION of
  the aborts localised the fault.** 83% on one step type told them where the problem
  was. **That is precisely what our binding-tile cut did offline** — it classified
  1.8 million blocked harvester-rounds and found 39.6% on one class. **A bot that
  latched stall reasons into a store slot could do a coarse version of that live**,
  and it is the only route in this sweep from "something is wrong" to "this is what
  is wrong" that a bot could execute itself.
- **22% is a sobering and useful number for sizing.** Retry-in-place is not a fix,
  it is a partial recovery. **Anyone budgeting builder-rounds for repair should
  assume most attempts do not resolve the goal**, which argues for cheap repair
  attempts over expensive ones and matches
  [`gate-the-expensive-replan-behind-a-damage-counter`](gate-the-expensive-replan-behind-a-damage-counter.md).

WHAT WOULD KILL IT —

- **⚠ The 22% is NOT "repair beats rebuild".** The quoted sentence says that of the plan executions which contained at least one
  retry, 22% ended with the goal succeeding — a success rate for retrying, **with no
  alternative arm.** **There is no rebuild comparison in
  the paper and quoting it as one would be exactly the wrong-referent failure this
  library keeps catching.**
- **Their failures are physical and stochastic** — grippers, workpiece detection,
  machine malfunctions. Ours are **structural and permanent**: a destroyed conveyor
  does not succeed on retry. **So a plain "retry the action" policy is close to
  worthless here**; what transfers is the *monitoring* half, not the retry half.
- **One team's own logs, no control arm, no seed control, self-reported.** The
  evidence class is `documented` because the paper says it; it is not an experiment
  on the question we are asking.
- **The precondition-timeout idea needs per-action state across rounds**, which our
  16 buffered ints cannot hold at any useful granularity. **The same objection that
  bounds every (C) plank in this sweep bounds this one.**

BUILDER HOOK — the harvester version, which needs no memory at all because the
engine keeps the clock: a harvester emits every 4 rounds. **A builder adjacent to a
friendly harvester can observe whether any of its orthogonal neighbours changed
stack id over 5 rounds; if not, that harvester is stalled.** Latch a coarse *reason*
(no output built / output is a dead end / output is a friendly building) into a
store slot as a small integer and log it. **Then compare the live distribution
against the binding-tile cut's 39.6 / 15.9 / 13.2 / 9.9 — a third instrument on the
same fact, from inside the game rather than from the tape.**
