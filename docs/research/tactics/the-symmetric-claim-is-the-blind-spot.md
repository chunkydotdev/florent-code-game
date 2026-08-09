---
tactic: (D) The named blind spot of every occupancy-based check — two agents claiming the SAME EMPTY tile in the SAME step each see no conflict, and both proceed
source: https://raw.githubusercontent.com/flatland-association/flatland-baselines/main/flatland_baselines/deadlock_avoidance_heuristic/README.md
origin: Flatland deadlock-avoidance heuristic, an official flatland-association baseline, credited in-README to aiAdrian
evidence: documented
transfers: yes
---

WHAT IT IS — the baseline's rule is a lookahead over currently-occupied cells:

> *"Do not enter/move if there is no free space between my path and any oncoming train's path. (A train is oncoming if it is on my path and running towards me)."*

**And its authors document, under a heading of their own, exactly where it fails**:

> *"A genuine merge conflict at a switch is not detected ahead of time. If two agents approach the same switch from different arms and are both about to move into the switch cell in the same time step, neither currently occupies that (still empty) cell, so the opposition check finds no conflict for either of them and issues MOVE_FORWARD for both."*

> *"Similarly, two agents approaching each other through switches at both ends of a single-track segment with no passing loop and no alternative route between them will permanently deadlock at their own switch cell -- one step short of ever entering the shared segment between the switches."*

and a third, about lookahead depth rather than simultaneity (typo *"a long"* is in
the source and is quoted as-is):

> *"The method does not propagate the required capacity a long the train's route."*

The baseline's own fix is an opt-in pairwise check over **only the agents acting
this step**, `entering_prevention=True`, documented as being there *"to check for
agents entering at the same time leading to a deadlock"*.

WHY IT MIGHT TRANSFER — I think this is the most likely explanation for our 6x,
and it is testable:

- **Our `HEAD_TO_HEAD` is 9.94% against a field 1.57%, and the binding-tile cut
  calls it *"close to a live bug"*.** A conveyor pointing at empty ground is legal;
  a conveyor pointing at another conveyor that points back is legal for *each* of
  them at the moment it is placed. **Two of our builders, each running the same
  `can_build_conveyor` check on the same round, can each be individually correct and
  jointly wrong.** That is this blind spot exactly.
- **And our engine makes it *worse* than Flatland's version, because our writes are
  buffered.** The store is *"visible only from the next round"*, so two builders
  cannot coordinate within a round through it at all. **Any within-round agreement
  is impossible by construction** — the only coordination channel is the world state
  itself.
- **But our engine also hands us the fix Flatland does not have.** Unit turn order
  is **global entity-id ascending**, measured at 0 inversions over 1,842,445 ordered
  pairs. **So the two builders do not act simultaneously — the lower-id one acts
  first, and its conveyor is already on the map when the higher-id one runs its
  check.** The symmetric case therefore *cannot* arise from turn order; it can only
  arise if the second builder's check does not look at what the first just built.
  **That makes this a code question with a definite answer, not a race.**

WHAT WOULD KILL IT —

- **⚠ This is a HYPOTHESIS about our 6x, not a measurement of it.** The binding-tile
  cut counts head-to-head pairs at end of game; it does not record whether the two
  conveyors were built in the same round or years apart. **The corpus can settle
  this and has not been asked.** Until it is, the causal story here is mine and
  should be labelled as such wherever it is repeated.
- **The alternative explanation is duller and at least as likely:** our builders
  never check the *destination* tile's facing at all, in which case the pairs form
  across many rounds and turn order is irrelevant. **That would make
  [`forbid-the-opposing-claim-and-pay-for-it`](forbid-the-opposing-claim-and-pay-for-it.md)
  the complete fix and this file merely interesting.**
- **Flatland is single-team and has no construction**, so the mapping from "two
  trains claiming a switch" to "two builders claiming a facing" is an analogy. It is
  a close one, but the mechanism it names (occupancy checks are blind to
  simultaneous claims) is what transfers, not the setting.

BUILDER HOOK — **a corpus cut before any code**, and it is cheap because the
instrument already exists: for every head-to-head pair in our replays, record the
build rounds of the two conveyors and the ids of the builders that placed them.
**Same round → the simultaneity story; different rounds → the no-check story.** The
two diagnoses want different fixes, and the decode that separates them is a
histogram of one number.
