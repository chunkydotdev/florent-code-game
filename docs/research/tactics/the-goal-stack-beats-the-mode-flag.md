---
tactic: Store the interrupted plan on a stack so a unit resumes it — the field's fix for mode-flag thrash
source: https://battlecode.org/assets/files/postmortem-2021-musketeers.pdf
origin: Battlecode 2021 3 Musketeers (finalist) and Battlecode 2025 The Kragle (finalist)
evidence: documented
transfers: yes
---

## WHAT IT IS

Two finalists, four years apart, independently replaced a single "current mode" variable with
a **stack**, and both name it as a large improvement.

**3 Musketeers (BC2021)**, on the machinery around their rush commitment:

> *"In order to keep track of what triggered our entrance into a specific state, we made use
> of a stack, dubbed the stateStack."*

> *"We set up a state called saving for rush, from which we entered a rushing state when we
> had enough money to build our rush politician."*

**Referent check.** The surrounding sentences give the reason for the stack explicitly: *"We
needed to store the state that we were in before saving for rush, so that after we build our
rush politician (which took higher priority than everything else), we could pop off the state
stack and resume previous duties."* The stack exists so a **high-priority interrupt does not
destroy the plan it interrupted**.

**The Kragle (BC2025)**, arriving at the same structure from the failure side:

> *"We decided to use a stack for the goals, giving robots a lot more choice in their
> intended actions on goals."*

**Referent check.** The failure it fixes is stated immediately before: *"Often, ruins would
be abandoned when robots went back to get their paint refilled, since they were the only
robot that knew it was in progress. After refilling paint, they would act as if they were a
new soldier."* A single goal variable was overwritten by the refill errand and the original
objective was silently dropped. Their verdict: *"This ended up being a huge improvement, and
we will definitely be bringing an enhanced version of this back in future years."*

The 3 Musketeers quote also supplies a clean example of a **resource-threshold trigger**:
`saving_for_rush → rushing` fires on *"when we had enough money"* — the commitment is gated
on the bank reaching the purchase price, and the saving state is itself a mode that suppresses
other spending. That is the same object as BC2020 confused's rush-cost surcharge, recorded in
`the-rush-cost-budget-gate.md`, expressed as a state rather than a price.

## WHY IT MIGHT TRANSFER

This is the constructive answer to a failure this library already filed. Sweep 14's
`defence-recall-oscillation.md` records BC2022 5 Musketeers' *"This worked but led to an
unfortunate oscillation problem"*, and notes it is **worse here**: our store is buffered to
next round, last writer wins, and acting and moving are mutually exclusive so a unit that
flips its mind loses the round entirely.

Our engine makes the stack version unusually attractive:

- **A per-unit stack lives in instance state and never touches the store.** No slot, no
  next-round latency, no last-writer-wins, and no risk of the negative-write raise that
  permanently destroys a unit. `run()` is called per unit per round on the same `Player`
  object, so a dict keyed by `ct.get_id()` is the whole implementation.
- **Our interrupts are exactly the ones the sources describe.** A builder walking to a
  forward seat gets interrupted by "the core is damaged, heal it" — and our own mechanism
  probe measured how violent that interrupt is: a builder orthogonally adjacent to a damaged
  core moves in **15.5% of rounds against 68.3% when the core is at full HP**, a 4.4×
  suppression on n = 143,812 samples, with the opponent's builders at only −0.152 in the same
  window. **That is our code, and it is the Kragle's abandoned-ruin failure exactly** — the
  errand overwrites the plan and the plan is never resumed.
- The cut's verdict on that pin is worth carrying alongside: the pin is real but the
  *proposed defect* (`dsq 25` gate, 50-round latch) was **refuted** — the binding threshold is
  orthogonal adjacency, recovery completes in ~10 rounds, and dispersal does not predict core
  kills within opponent. So a goal stack here is not licensed as "the fix that unlocks kills";
  it is licensed as "the plan survives the interrupt", which is a different and smaller claim.

## WHAT WOULD KILL IT

- **A stack that is never popped is a memory leak with extra steps.** Both sources pop on
  completion of the interrupting goal; a goal whose completion condition can never be
  observed pins the unit forever — the same disease as a mode flag, one level deeper.
- **Stale goals.** A tile that was a good turret seat 40 rounds ago may now be inside an enemy
  sentinel's line (r²=32, ignores obstacles). Resumption must re-validate with
  `can_build_*` / `can_fire_from`, not just replay the stored target.
- **CPU and memory.** Per-unit state across up to 50 units, every round, inside 10 ms each —
  cheap, but our library records three opponents with conditional compute blow-ups and it is
  the kind of structure that grows.
- **Neither source measured it against a mode-flag control.** Both report it as a large
  improvement; neither ran the comparison. Evidence is `documented` for the *design*, not for
  the *effect size*.

## BUILDER HOOK

Smallest test: wherever a Loki builder abandons a target to service the core-heal interrupt,
push the abandoned target and pop it when the core returns to full HP (recovery is
essentially complete within ~10 rounds, per the corpus). Parity first — with no interrupts
firing, behaviour must be byte-identical. Then measure whether forward builders reach their
original seat more often; `positions.tsv` already decodes builder position per round.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2021-musketeers.pdf
- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
