---
tactic: (C) THE ANSWER TO SUB-QUESTION (C), AND IT IS A NEGATIVE — I probed the open question and MODULE-LEVEL STATE IS NOT SHARED BETWEEN OUR UNITS. Every unit gets its own module namespace. There is no team-level map, no back channel, and no way to hand a new builder what an old one learned except 16 ints with a one-round lag
source: https://raw.githubusercontent.com/battlecode/battlecode23/master/engine/src/main/battlecode/common/GameConstants.java
origin: measured on the Florent Code League engine (`fcode` 2.3.6), against MIT Battlecode's shared-array design as the comparison case
evidence: documented
transfers: no
---
WHAT IT IS — `docs/research/predicate-feasibility-2026-08-10.md:437-439` listed this as the
open question that *"gates whether the store-and-memo design is buildable at all, and it is
one probe."* This is the probe.

`bots/_probe_modglobal` declares two module-level objects, a list and a dict, and has every
unit append its own `(team, id)` to the list and increment a counter in the dict on every
turn. If the module namespace were shared team-wide, unit N would see units 1..N-1.
`maps/eider.map26`, seed 1, same bot on both sides:

```
MODGLOBAL r=3 team=A unit=1  kind=CORE        BOX_n=4 TOUCHED=[('A', 1)]
MODGLOBAL r=3 team=A unit=3  kind=BUILDER_BOT BOX_n=3 TOUCHED=[('A', 3)]
MODGLOBAL r=3 team=A unit=5  kind=BUILDER_BOT BOX_n=2 TOUCHED=[('A', 5)]
MODGLOBAL r=3 team=A unit=7  kind=BUILDER_BOT BOX_n=1 TOUCHED=[('A', 7)]
```

**Every unit sees a `TOUCHED` list containing only itself.** Not team-wide, not
match-wide.

**The positive control is in the same four lines and is what makes this a measurement
rather than a dead column.** `BOX_n` is the *same* counter: it reads 4 for the core (which
has taken 4 turns), 3, 2 and 1 for builders spawned on successive rounds. **So the module
state demonstrably accumulates — across ROUNDS, within a unit.** The instrument can show
accumulation; it simply never shows it across units. A `TOUCHED` list that were always
`[self]` because the probe was broken would have shown `BOX_n=1` everywhere.

Cross-team leakage is also negative: team A units never see a `('B', …)` entry.

This is consistent with the engine's own internals — the shipped binary contains
`Py_NewInterpreterFromConfig` and the string `Failed to create subinterpreter for trial
load` — but the behaviour above is the evidence, not the inference.

WHY IT DOES NOT TRANSFER — **this is filed as `transfers: no` on purpose, because it is the
rule that kills a whole family of tactics that the comparable leagues all rely on.**

Battlecode's answer to (C) is a real shared blackboard: `SHARED_ARRAY_LENGTH = 64` values of
up to `(1 << 16) - 1` (`battlecode23/engine/src/main/battlecode/common/GameConstants.java:63,67`),
and the 2023 spec adds that *"Array values persist across turns; ie. they are not reset."*
That is 1024 bits, readable and writable the same turn. Four separate teams used it to
publish a team-wide symmetry conclusion
([symmetry](symmetry-is-the-only-free-information-about-the-unseen-map.md)).

**Ours is 16 ints, and I measured the edges too** (`bots/_probe_oov_surface`, same map and seed):
`read_store(15)` is fine; `read_store(16)` and `write_store(16, 1)` raise
`GameError: store index 16 out of range (0..16)` — note the engine's own message is
off-by-one, the usable range is 0..15. `write_store(0, -5)` and `write_store(0, 2**62)` both
raise **`OverflowError`, not `GameError`**, so the slot is an unsigned bounded integer and a
handler narrowed to `GameError` will not catch a bad write.

So the honest position for the builder is:

- **Any map knowledge a unit acquires dies with that unit.** A builder that scouts the
  enemy half and is then killed has taught the team nothing it did not publish into 16 ints.
- **Every newly spawned builder starts blind**, and there is no bulk transfer. The
  [tri-state terrain memory](the-winner-stored-a-tri-state-and-resolved-unknown-two-ways.md)
  is per-unit and must be rebuilt from scratch by each one.
- **Therefore prefer knowledge that can be RE-DERIVED locally over knowledge that must be
  COMMUNICATED.** Map symmetry is the ideal case: every unit can regenerate the candidate
  enemy-core positions from its own core's position with no comms at all, and only the
  *elimination* result needs a bit in the store. That asymmetry is why the symmetry plank
  survives this constraint and a shared terrain map does not.
- This aligns with, and now has a mechanism for, the existing
  [`the-blackboard-is-a-one-tick-bus-not-a-memory`](the-blackboard-is-a-one-tick-bus-not-a-memory.md):
  our 16 ints are not a memory because there is nothing else that could be one.

WHAT WOULD KILL IT — an engine version change. The probe is against `fcode` 2.3.6 in
`.venv`; re-run `bots/_probe_modglobal` after any upgrade. Also note the probe tests
module-level *mutation*; it does not test whether an expensive module-level *constant*
computed at import time is paid once per unit or once per match. That is a different
question, it is a CPU question, and CPU is not our binding constraint.

BUILDER HOOK — none needed; this is a constraint to design against, not a thing to build.
The one action it implies: **delete any design note that assumes units can share a
computed map**, and re-read the store-and-memo section of
`docs/research/predicate-feasibility-2026-08-10.md` with §9(2) now answered NO.
