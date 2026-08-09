---
tactic: (B) THE CHEAPEST RESUMABLE INTERRUPT IN THE CORPUS — two setters that differ by one line. One updates "where I was", the other deliberately does not, so the interrupted plan survives without a stack
source: https://www.outercloud.dev/blogs/battlecode-2026/
origin: Battlecode 2026, 3MiceWalkIntoABar (top-10 on the ranked ladder, qualified for the final tournament)
evidence: documented
transfers: yes
---

## WHAT IT IS

3MiceWalkIntoABar's units run a plain per-tick state machine:

> *"Behaviour within our bot was handled with an extremely simple state machine."*

> *"Essentially, every tick, a rat would check which state was stored within the state
> variable and execute code for that state."*

**And then one extra variable turns a mode flag into a resumable plan:**

> *"which could allow the bot to remember and later resume a state if it got interrupted by
> the"* … `fleeingCat` … *"state."*

**Referent check and a markup warning.** The full sentence as rendered reads *"We also stored
a previousState , which could allow the bot to remember and later resume a state if it got
interrupted by the fleeingCat state."* — `previousState` and `fleeingCat` are inline `<code>`
elements, so tag-stripping leaves a space before the comma and the surrounding words split
into separate greppable runs. The fragment quoted above is what verifies literally; the rest
is stated, not quoted.

**The mechanism is two methods on their controller class, and the difference between them is
one assignment:** `goToState(newState)` sets both `state` and `previousState`;
`goToStateTemporary(newState)` sets **only** `state`. So entering a temporary state does not
overwrite the record of what the unit was doing, and leaving it can restore that record.
(Their article shows both methods in a Java code block; the rendered HTML tokenises the code,
so the method bodies are described here rather than quoted.)

**The same team also built the measurement discipline this library keeps asking for:**

> *"We made sure that before we merged any changes, the tester gave us confidence that the
> change improved the win rate. We used a 95% confidence interval on the win rates to make
> this decision."*

and the reason they needed it:

> *"there was often enough local variation to make a bad change look as if it improved the
> bot"*

## WHY IT MIGHT TRANSFER

**This is the smallest possible answer to the failure the library has already filed twice, and
it costs one variable per unit and zero store slots.**

- **The failure is documented in our own bot, not just theirs.** BC2025 The Kragle's
  motivation for building a goal stack is the same event: *"Often, ruins would be abandoned
  when robots went back to get their paint refilled, since they were the only robot that knew
  it was in progress. After refilling paint, they would act as if they were a new soldier."*
  And our own mechanism probe measured our version of that interrupt: a builder orthogonally
  adjacent to a damaged core moves in **15.5% of rounds against 68.3% when the core is at full
  HP** — a 4.4× suppression on n = 143,812 samples. **The heal errand overwrites the plan and
  the plan is never resumed.**
- **It is strictly cheaper than the library's existing answer.**
  [`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md) documents two
  Battlecode finalists replacing a mode flag with a stack. **A stack is the right structure
  when interrupts nest. Ours do not** — the core-heal pull is a single, well-identified,
  self-terminating errand — so one extra variable buys the whole benefit at a fraction of the
  cost and cannot leak.
- **It sidesteps every hazard of our store.** `state` and `previous_state` live in a dict on
  the `Player` instance keyed by `ct.get_id()`. No slot, no one-round buffer, no
  last-writer-wins, no negative-write raise.
- **It gives us a second, honest option: mark the interrupt, not the plan.** A unit that is
  healing does not have to *forget* it was walking to a seat. That is the entire fix.

## WHAT WOULD KILL IT

- **`previous_state` is one level deep.** Two nested interrupts and the outer one is lost —
  which is precisely when the Kragle's stack becomes correct. If our interrupt set grows past
  one, this file is superseded.
- **A resumed plan may be stale.** The seat may have become illegal or lethal while the unit
  was healing. Resumption must re-validate — see
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md).
  Restoring a target without re-checking `can_build_*` reproduces the Lorem Ipsum bug (*"each
  time a target changed, the code was supposed to reset bugging"*).
- **Our units die, and per-instance state dies with them.** A builder killed mid-errand takes
  its `previous_state` with it; nothing else on the team knows what it was doing. Screeps
  solves this with a persistent `Memory` object; we cannot.
- **3MiceWalkIntoABar published no measurement of this specific mechanism.** Their 95% CI
  tester is real and they report using it on merges, but no before/after for `previousState`
  is given. Evidence is `documented` for the design.
- **And the cut this file must not overstate:** our own corpus already **refuted** the
  proposed defect around the core-heal pin (the `dsq 25` gate and 50-round latch); the pin is
  real, the binding threshold is orthogonal adjacency, recovery completes in ~10 rounds, and
  dispersal does not predict core kills within opponent. **So this is licensed as "the plan
  survives the interrupt", not as "this unlocks kills".**

## BUILDER HOOK

Two lines. Wherever a builder switches to the core-heal errand, write the abandoned target to
`self._prev_target[ct.get_id()]` instead of overwriting the target; when the core returns to
full HP, restore it **and re-validate with `can_build_*` before acting on it**. Parity first:
with no interrupt firing, behaviour must be byte-identical. Then measure the one number this
buys — **the share of forward builders that reach their original seat** — which
`positions.tsv` already decodes per round.

## SOURCES QUOTED IN THIS FILE

- https://www.outercloud.dev/blogs/battlecode-2026/
- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
- https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). **Method note: on this source, inline `<code>`
elements inject spaces into the surrounding prose after tag-stripping (`a previousState ,`),
so sentences containing identifiers must be quoted as fragments that stop at the code span.**
