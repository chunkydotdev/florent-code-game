# BUILDER ARM RETRO — **v1** — run it at every wrap, before the process deltas

**VERSION HISTORY.** Amend by APPENDING a new version with its date and reason;
never edit a question in place, or a retro answered under v1 cannot be compared
with one answered under v2. *(Same rule the kill-speed scale learned the hard way
on 2026-08-10, when an in-place edit orphaned every earlier figure within the
hour.)*
* **v1 — 2026-08-10 (s28).** Created from that session's own evidence, at
  Magnus's instruction that each arm have its own retro.

**Why this is NOT the research retro.** That lane's premise is *"output is worth
what another lane consumes"*. **This lane does not produce analysis — it produces
DECISIONS: verdicts, ships, slot moves, bot edits, and the instruments the other
lanes read.** Its failure mode is not being unread. **It is being CONFIDENTLY
WRONG in a way that costs rating, spends a rate-limited budget, or writes a
number other lanes then build on.**

**ZERO FIRINGS AT BIRTH (D25). If two successive retros produce nothing that
changes behaviour, delete it rather than perform it.**

---

## The seven questions. Answer from artefacts — commits, logs, the platform — never from memory.

### 1. VERDICTS — did each one carry exactly what its interval supports?
List every verdict typed. For each: the bar, the measurement, and **the sentence
you were tempted to write instead**. A verdict that hedges when the data is clean
is as wrong as one that overclaims.
*s28: LOKI-14 refuted **against this panel** (not "crash induction is refuted");
LOKI-16 **unresolved**, not "failed"; PANEL-3 produced a panel **with its two
straddled cells disclosed**; the +0.017 **withdrawn** rather than reported as a
miss. Four verdicts, four scoped.*

### 2. WHAT I RETRACTED, AND WHICH DIRECTION THE ERROR RAN
Every correction, with its direction. **The diagnostic is whether the errors
point somewhere.**
*s28: five retractions, and **every one ran toward the work I wanted to do
next** — the null's scope, the MDE denominator, "displacement untouched", the
Ouroboros headline, the map axis. **None was a calculation error; each was a
check I did not run because its result would have been inconvenient.***

### 3. INSTRUMENTS — what did I change, and was each driven to BOTH verdicts?
Every tool built or edited. For each: does a committed record show it producing
the other answer? **And did any new instrument get trusted on its first output?**
*s28: 4 instrument inversions (sentinel 52.1% → 0/319 → 100%; two `undamaged`
definitions 91 events apart; the `CORE_PAIRS` symmetry claim; `ring_retention`
failing to reproduce LOKI-16 with a **sign flip**). **Every one was the
instrument, never the bot.** The only reliable catch: **run the new tool against
a number the old one produced.***

### 4. CLAIMS AHEAD OF THEIR RECORD
Every commit message or comment asserting a test. Does a committed artefact name
**that file**? `tools/claim_check.py` answers this mechanically — **run it.**
*s28: **three** claims committed ahead of their record, all caught by another
lane, none by me. Pattern: **run the check, watch it pass, treat the passing as
the artefact.***

### 5. THE SLOT AND THE HOLDER — what did activation actually cost?
Activations, rollbacks **verified on the platform** (never from a runner's log),
and **rated matches played by a non-incumbent**. Read per-match `ourver`, not the
poll-time tag.
*s28: 3 leaked rated matches, **−24.67 Elo**, invisible to `elo_history`'s
poll-time tag — falsifying the standing claim that prototype legs cost zero.
Prototype exposure held to **10 s per cycle** by the rate-limit inversion.*

### 6. WHAT THE BUDGET BOUGHT
Challenges fired vs banked vs abandoned, and **utilisation against the ceiling**.
A rate-limited resource left idle is a debit; one spent on a target that cannot
pay is worse.
*s28: ~78 unrated matches; **~a third went to legs later abandoned**; slot
utilisation measured at **57%** before the meter-driven fix. `target_value.py`
exists so this is asked BEFORE the leg — **and it only fires when someone runs
it.***

### 7. WHAT A SUCCESSOR CANNOT RECONSTRUCT
Anything true only in this session's head. **Monitors die with the session; so
does every intention.**
*s28: the HANDOVER state block went **17 points stale within two hours** of being
written "verified at wrap". A state block is an EXPIRY DATE, not a guarantee.*

---

## The one question that is not a list

**Did I make a decision today that the machinery could not have caught?**

*s28's answer, and it is why this retro exists: the crash leg passed **every check
this repo has** — pre-registered, 8 blind amendments, clean placebo, dose
delivered, controls both ways, lock cert clean — **and was aimed at four teams
where a perfect result paid 1.18 rating points.** The machinery inspects the
EXPERIMENT and never asks whether the QUESTION is worth answering.*

**If the answer is "no", say so plainly. A retro that finds a profound failure
every time is performing.**
