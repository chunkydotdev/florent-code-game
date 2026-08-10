# RESEARCH ARM RETRO — run it at every wrap, before the process deltas

**Why this exists, and why it is NOT the wrap.** The wrap (`two-session-protocol.md`
rule 5) is lane-agnostic and it is a **failure log** — it records what went wrong.
It never asks whether this lane was **useful**. Those are different questions and
only one of them makes the arm better for the builder and the side lane.

**The premise, stated bluntly so the retro has teeth: this lane's output is worth
exactly what another lane consumes. Everything else is cost** — context, tokens,
and the `doc:code churn` and `cross-lane analysis` signals that `audit_trigger`
fires on. A cut nobody reads is not neutral. It is a debit.

**Created 2026-08-10 (s28), from that session's own evidence. It has ZERO firings
at birth (D25) and must earn its place — if two successive retros produce nothing
that changes behaviour, delete it rather than performing it.**

---

## The six questions. Answer them from the day's artefacts, not from memory.

### 1. CONSUMPTION — of what I produced, what changed a decision?
List every cut, sweep and relay. Mark each **CONSUMED** (another lane acted on it),
**PENDING**, or **UNREAD**. **Unread is a debit and gets named, not omitted.**
*s28 baseline: carrier check → the leg fired on it. Reachability → the panel was
rebuilt. Autopsy → the plank. Library mining: **1 of 3 consumed, 2 unread.***

### 2. LATENCY — did it arrive BEFORE or AFTER the decision it bore on?
**Before = full value. After = archaeology.** This is the single highest-leverage
number in the retro, because the same analysis is worth wildly different amounts
depending on which side of the decision it lands.
*s28: the carrier check beat the leg by ~25 minutes and changed what fired. The
same work an hour later would have been a footnote.*

### 3. RELAY FIDELITY — re-read ONE relay against its source agent output.
**This lane's unique failure mode.** The builder writes code and the side lane
audits commits; **this arm is the only one that compresses agent output at scale**,
and the compression is invisible to everyone downstream.
*s28: an agent wrote "flat-to-slightly-up" over quartiles 0.150 → 0.175 → 0.100 →
**0.314**. I relayed **"flat — nothing we shipped touched it."** The builder made it
the queue headline. The payload was right; the summary was wrong; the queue moved.*
**Pick one relay at random and diff it against the source. Every time.**

### 4. DID ANY OF MY OWN CHECKS FIRE ON MY OWN WORK?
Count: errors I caught in my own output vs errors caught by a peer or by Magnus.
**If the answer is zero again, this lane is only checking outward and is half an
instrument.**
*s28: **zero.** Every error of mine was caught by a peer re-deriving my arithmetic
or by Magnus asking a question about the board.*

### 5. WHAT DID I DECLINE TO MEASURE, AND WAS THAT RIGHT?
**A recorded decline is a deliverable** (prior-session D26). With `audit_trigger`
firing on analysis-outpacing-decisions, a declined cut is often worth more than a
delivered one, and it stays cheap to overturn.
*s28: I declined almost nothing, and should have. Two library sweeps were spawned
that nobody has read.*

### 6. WHAT DID I HAND EACH LANE, AND DID IT SURVIVE?
Per lane, because they need different things:
* **BUILDER** needs numbers **before** decisions, independent verification of their
  own claims, and cheap kills for bad ideas. *(s28: verified their MDE, their Elo
  formula, their target-value gate; killed a carrier panel and a Bisons regression
  before either reached a decision.)*
* **SIDE LANE** needs **re-derivable primaries** and my errors surfaced early, so
  their audit is not built on sand. *(s28: they re-derived my reachability figures
  to the digit — and caught a sentence of mine that conflated two statistics.)*
**Count retractions separately.** *s28: three of mine reached a lane before I
corrected them.*

---

## Two standing lines to close on

**A. Which of today's outputs would I not produce again?** Name it. This is the
only question that shrinks the lane, and every other question grows it.

**B. What did a peer catch that my own process should have?** Not to apologise —
to convert into a check. *s28: "an audit of the evidence is not an audit of the
codebase" was written about someone else in the morning and committed by me twice
in the afternoon (asserting a decoder did not exist while we ship one; asserting we
had never played a team we have played 8 times). **Both were one `grep` away.
The check that would have fired is: before asserting a capability or a history is
absent, grep for it.***

---

## The one metric worth tracking across sessions

**decisions changed ÷ subagent invocations.** Not documents produced, not cuts run,
not tokens spent. **If that ratio falls, the lane is drifting toward being a library
nobody reads — which is precisely what happened to `docs/research/tactics/`: 252
files, ~28k lines, and a decision-path citation rate of ZERO until Magnus ordered it
mined on 2026-08-10.**
