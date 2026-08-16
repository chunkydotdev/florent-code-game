# CERTIFICATION — DOES OBSERVING TWO LEG GAMES COMPROMISE `LEG-fieldcal-2026-08-16`?

**Certifying lane:** SIDE LANE, s45. **Routed by RESEARCH, who declined to rule on the grounds that
they own the leg's pooled readout — a ruling that one's own future instrument is uncompromised is
the shape nobody should accept, however careful. Correct refusal.**

**THE FACTS, as established by research and re-verified here:**

    59f4d2bc -> scratchpad/arm_fieldcal_A_HTTP_418.txt     arm A (v140)  viewed 10:54:06Z
    91a87b64 -> scratchpad/arm_fieldcal_A_The_Bisons.txt   arm A (v140)  viewed 11:34:30Z
    clock2 = 2026-08-16T06:25:40.381Z   -> both are ACCEPTED CELLS of the live leg, post-clock2

---

## VERDICT: **NO BREACH. THE CELLS STAND. THE LEG IS UNAFFECTED.** One prospective condition (§D).

## A. THE LOCKED TEXT DOES NOT GOVERN OBSERVATION, AND I CHECKED RATHER THAN ASSUMED

**`LEG-fieldcal-2026-08-16.md` contains NO clause forbidding or conditioning the VIEWING of leg
games.** Its blindness obligation is **§13, and it governs AMENDMENTS**: *"Amendments must be
ADD-ONLY and blind to the leg's data."* ⇒ **Pre-registration protects against ANALYSIS CHOICES made
after seeing data. It does not require that no human ever sees a game**, and no registered object —
estimator, bar, horizon, cells, pins, falsifier — is conditioned on observation.

## B. NOTHING REGISTERED POSTDATES THE VIEWING — the decisive check, and it is arithmetic

    only amendment to this leg, LOCKED       2026-08-16T08:39:05Z
    first viewing                            2026-08-16T10:54:06Z    (+2h15m LATER)
    prereg/amendment files added since       ZERO

⇒ **Every registered object predates both viewings by more than two hours.** **There is no rule that
COULD have been chosen after seeing this data, because no rule was chosen after it.**

## C. §9.3 VOIDING DOES NOT REACH THIS

**§9.3 voids a cell on a PIN MISMATCH** — decoded `oppver` ≠ registered `theirver`. **It is an
instrument-integrity clause about which opponent build was played.** ⇒ **Observation is not a
voiding trigger under any registered clause, and inventing one now would be adding an obligation to
a locked document after the fact.**

## D. WHAT IS EXPOSED, AND THE ONE CONDITION THAT FOLLOWS

* ✅ **ARM B WAS NEVER VIEWED.** The registered primary is a CONTRAST — the sign of
  `share_T − share_C` per cell. ⇒ **the primary's unit was never observed; half a difference is not
  the difference.**
* ⚠ **Arm A's outcomes in two cells WERE observed, including a 49-round loss — and the secondary
  (pooled ITT RMST₃₀₀) is a function of turns.** **One game's turn count was seen directly.**
  **That is 1 of a planned 1,200 games, in the arm that is the CONTROL.**
* ✅ **No analysis was contingent on it.** Nobody proposes stopping, extending, re-weighting or
  re-scoping, and the planks derived are mechanism observations orthogonal to what the leg measures.

**⇒ THE PROSPECTIVE CONDITION, and it is the only thing this ruling changes: ABSTENTION-BASED
BLINDNESS IS NO LONGER AVAILABLE TO ANYONE WHO VIEWED THESE GAMES.** Any future amendment must
either be **STRUCTURALLY blind** — as the catch-up rule was, its selection domain guaranteeing the
absence of a result — **or be authored by someone who did not view.** ⛔ *"I did not look"* is now a
claim that would be false for at least one participant, and an amendment resting on it would be
unsound even if its content were fine.

## E. NOT THE QUESTION, STATED SO THE RULING IS NOT DISTORTED BY IT

**Magnus's access is not at issue and research was right to exclude it explicitly.** He is the
principal and may look at anything he owns. **The question is solely whether the LEG'S REGISTRATION
is affected by having been observed — a property of the leg, not of the observer.** It is not.

## F. ⭐ AND THE DISCLOSURE IS ITSELF THE PROTECTION

**This leg's observation history is now on the record with match ids, arms, and wall-clock times.**
⇒ **A leg whose observation is documented is in a strictly better position than one where nobody
checked** — any future reader can assess it against the registered rules instead of assuming.
**The builder flagged it as a possible tangent; research checked rather than weighed; the certifier
ruled. That sequence is why this is a note and not a wound.**

## G. THE WORKFLOW GAP — AGREED, AND IT IS THE MORE VALUABLE HALF

**Nothing warns that a match id belongs to a live registered leg.** It was caught by **recognising an
opponent NAME — human recall, not a tool.** ⇒ **a one-line lookup (*is this match id in any
`arm_fieldcal_*` ledger?*) at the moment a replay is opened** would have said so. **Cheap, and the
same shape as every guard fixed today: checkable at the point of use rather than dependent on
someone remembering.** ✅ **Routed to the BUILDER now that the ruling exists** — and the ruling tells
it what to say: **not "do not open this" but "this is a leg accept, arm A; abstention-blindness is
forfeit from here."**
