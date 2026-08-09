---
tactic: Execution monitoring — detect a silent failure by predicting the action's effect and comparing it to what you observe
source: https://www.diva-portal.org/smash/get/diva2:136255/FULLTEXT01.pdf
origin: Abdelbaki Bouguerra, "Robust Execution of Robot Task-Plans: A Knowledge-based Approach", Örebro Studies in Technology 32, Örebro University, 2008 (PhD thesis) — surveying the mobile-robotics execution-monitoring literature
evidence: documented
transfers: partial
---

WHAT IT IS — the academic answer to sub-question (C), and it is a **named
sub-discipline** rather than a trick. The thesis states the problem in the same
terms our binding-tile cut states ours:

> *"The aim of plan execution monitoring is to detect anomalous situations that might lead to execution failure."*

and

> *"execution monitoring is a prerequisite for recovering from unexpected situations"*

The **dominant mechanism in that literature is model-based**: you write down what
the action was supposed to do, you observe what actually happened, and you flag
the divergence.

> *"Most plan execution monitoring approaches in mobile robotics use action models to compare the explicit effects of actions to what is observed as a result"*

*(That sentence continues across a page break in the source — see the method note
below. The clause after the break reads "of executing those actions", but the
extractor injects the page number and the running chapter header between the two
halves, so the full sentence can never be grepped as one string and is deliberately
not quoted as one here.)*

The thesis names the alternative and is explicitly dismissive of it — the
alternative is what we currently do:

> *"hard-coded procedures are implemented to monitor specific conditions of interest"*

The referent of *"Other approaches"* in the sentence that string comes from is
execution monitoring in plan-based robotic architectures; the thesis's own
contribution is the model-based/probabilistic branch, not the ad-hoc one.

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **Our failure is exactly the class this literature exists for: the action
  succeeded, the engine raised nothing, and the world silently did not change.**
  `build_conveyor` returns an id. `can_build_conveyor` said yes. The stack parks
  forever. There is no error path to catch, so a `try/except` bot is structurally
  blind — and 85.2% of our binding tiles are in that state.
- **The action model is trivial to write here, because the rules are arithmetic.**
  A harvester's model is *one stack every 4 rounds*. A conveyor's model is *the
  stack on me at round r is not the stack on me at round r+1*. A route's model is
  *the chain from this tile reaches a core footprint tile by following facings*.
  All three are cheap predicates over information the `Controller` already exposes.
- **The `Controller` already ships the observation channel for the cheapest of the
  three, and we do not read it.** `get_stored_resource_id(id)` returns the id of the
  stack a conveyor is holding, and the organisers' reference states these ids are
  *"distinct from entity IDs"*. **A conveyor whose `get_stored_resource_id` returns
  the same non-`None` value on two consecutive rounds has not moved its stack.**
  That is a one-line staleness check per observed tile, and it fires on every one
  of the `DEAD_END_*`, `HEAD_TO_HEAD` and `INTO_HARVESTER` classes — 68.6% of our
  blocked mass — **without needing to know why**. It does not distinguish a cork
  from genuine saturation (`DOWNSTREAM_MOVED`, 14.3% pooled / 0.1% median), which
  is the correct behaviour anyway: both are worth a builder's attention.
- **⚠ The `get_stored_resource_id` staleness detector is MY INFERENCE from the
  API reference, not a sourced tactic and not probed.** Nobody in the surveyed
  literature did this; it is the transfer, not the finding. It needs an engine
  probe before anyone sizes anything on it: specifically, whether a stack retains
  its id across a conveyor-to-conveyor push (if ids are re-minted per hop the check
  inverts, and if they are re-minted per round it is useless).

WHAT WOULD KILL IT —

- **The 16-slot store cannot carry a map.** Model-based monitoring in the source
  literature assumes an agent with unbounded memory of its own predicted state.
  Ours is 16 unsigned ints, buffered one round, last-writer-wins. **So the monitor
  must be local to whichever unit can see the tile** — it cannot be a global
  network health model, and a builder that walks away loses its own history.
  A monitor that needs to persist state across rounds for a specific tile has
  nowhere to put it.
- **10 ms per unit per turn.** A full revalidation of every route every round for
  every builder is not affordable. The literature's model-based monitors run on
  robots with seconds per decision. Any transfer has to be a per-tile predicate
  evaluated on tiles a unit is already standing next to, not a network sweep.
- **The evidence class is wrong for a strong claim.** This is a robotics thesis,
  not a competitive league. It documents that the *problem* is named and that a
  *family* of solutions exists. **It does not show anyone winning a game with one**,
  and it contains no measurement transferable to our economics. Anyone quoting this
  as "the field solved detection" is over-reading it — the field *named* detection.

BUILDER HOOK — the smallest thing that would test it, in order of cost:

1. **Probe first, build second (engine probe, not a plank):** does a titanium stack
   keep the same `get_stored_resource_id` when it moves one tile along a conveyor
   chain? Three rounds of a two-conveyor line answers it. **Everything below is void
   if the answer is no.**
2. **Instrument-only, no behaviour change:** have builder bots `print()` the id and
   round for any conveyor in `get_nearby_buildings()` holding a stack, and diff the
   replay. This produces a live in-game measurement of stalled-tile incidence that
   can be compared directly against the binding-tile cut's 85.15% — an independent
   third instrument on the same fact, at zero risk.
3. **Only then:** let a builder that observes the same stack id twice on an adjacent
   conveyor treat that tile as the highest-priority action target. Note the
   binding-tile cut's finding that a median of **3 tiles carries 80% of a team-side's
   blocked mass** — so this does not need to run often to pay, which is the same
   reason the CPU objection above is survivable.

---

**Method note, for the library's trap list — this source produced a NEW one.**
`pdftotext` emits the page number and the running chapter header **inside** a
sentence that straddles a page boundary. The library's existing fix (flatten `\f`
and `\r`) removes the *whitespace* of the page break but not the *furniture*, so a
quote spanning the break still cannot be grepped as one literal string — and the
failure looks identical to a fabrication. Here the injected text is
`11 12 CHAPTER 2. BACKGROUND AND RELATED WORK` plus a figure caption. **The
correct response is the existing no-elision rule: split into two quotes or quote
only the pre-break span.** It is *not* to paper over the gap with an ellipsis,
which is what a hurried author would do and which would have made the string
unverifiable forever.
