# SIDE-LANE RETRO — INSTANCE s29, 2026-08-11

**Instrument: `docs/side-lane-retro.md` v1.** **FIRST FIRING** (it was created at
the s28 wrap with zero firings and an armed sunset clause). **This is a separate
dated instance; the instrument itself is not edited by it.** Answers are from the
session's own artefacts, not from memory.

---

## Q1. CONSUMPTION — were flags ACTED ON, or filed?
**~14 flags to the builder, 2 to research. Twelve changed an artefact the same
session**, each named: LOKI-17 stopped · LOKI-19 Amendments 1/2/3 · the panel's
5th cell replaced with Landers · `ring_read.py` tracked + selftested and its
broken twin made to refuse · `rate_budget` fail-closed · `unrated_run`'s numeric
guard, bounded pairing wait and recorded abort test · `plank_status.py` ·
`freshness.py` · research's Part 5 withdrawal · research's Part 8/10 boundary
correction · the adjudication's `hold_any` fix.

**⛔ THE EXCEPTION IS THE ONE THAT MATTERS: the SWEEP was consumed 2 of 6.**
F5 and F6 were fixed; **F1–F4 sat untouched for three hours and two of them are
the LIVE defects** (`audit_trigger` disarmed on every builder boot;
`oppver_window` certifying D18 off a stale tape). **Consumption is not a lane
average — it is per-artefact, and the artefact with the most findings had the
worst rate.** A six-finding document competes with itself for attention.

## Q2. LATENCY — did the flag beat the decision it bore on?
**Before the decision: LOKI-17's dead primary** (builder: *"within one commit of
activating"*) · **the arrival premise** (control window 1 fired, treatment arm
had ZERO games) · **the undefined `materially`** (zero treatment games) ·
**`claim_check`'s empty silence** (before the runner's first real use) ·
**`unrated_run`'s untested abort branch** (before its first live run).
**After: one.** The **pairing clock** was derived *after* the v108 submit — pure
archaeology on that incident — **but it converted the incident into a forward
control that has since passed a live test.** Archaeology that produces a control
is not the failure mode this question hunts.

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — this lane's characteristic failure
**THREE published, identical to s28's count. No improvement in rate.**
1. **Flag 1**: *"the bar was sized on a retired decoder's output."* False — the
   two figures were two GRANULARITIES of one decoder, and **I had compared a
   per-tile calibration number to an any-builder measurement: the exact units
   fault I was alleging.**
2. **`any-builder = hold_any`** relayed to two recipients. The `+0.137` is
   `bot_episodes`, a third quantity. **My subagent reported V1/V3; I supplied
   the names, by position.**
3. **"We shipped the losing arm of an unfinished probe"** — written into a
   committed doc, then struck: the adoption **was** evidenced (12/15, p=0.025).

**TWO MORE WERE CAUGHT PRE-PUBLICATION, AND NEITHER BY CARE:** an exit code read
**after a pipe** (`$?` was `tail`'s), and **absence of v108 from a corpus that
had not yet ingested the window**. **Both were caught by a hard bound — a
documented promise and a timestamp — not by reading harder.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?
**s28: ZERO of 8. s29: FOUR of FIVE.** Flag 1 (caught by my own blind
replication), the unfinished-probe framing (caught by chasing my own question),
and both near-publications. **Only the `hold_any` label was caught by another
lane.** **This question moves off zero for the first time** — and the mechanism
was not diligence, it was **running a second instrument over my own claim**.

## Q5. FALSE POSITIVES — what did flagging cheaply cost?
**Two wrong, both cheap, and one was net-POSITIVE.**
* **`breakin_watch` "down, unrepaired"** — it had **EXITED BY DESIGN** at k≥8 per
  its own handoff clause. I read a completed handoff as a failure. Cost: one
  reply. **I checked the process and not its contract.**
* **Flag 1** — wrong reasoning, **but it forced a check that could only have hurt
  the result, before the read-out rather than after.** The calibration is
  defensible now rather than merely unchallenged. **A wrong flag that forces the
  right check is the policy working, not failing.**

## Q6. FAIRNESS — did I characterise another lane's conduct?
**One opportunity, and the s28 rule held.** The night collector died mid-cycle
with a session reboot 20 minutes earlier — a matching clock and a tempting story.
**I labelled it a hypothesis, said the cause was unrecoverable, and refused to
assert it.** The builder had killed it deliberately per HANDOVER. **Last session I
published exactly this shape and had to retract; this session the rule was
already written and it worked.**

## Q7. WHAT DID I DECLINE, and was declining right?
**Five, all held.** The night-panel read (assigned to research — declined to
duplicate a decode) · calling the fire/hold decision on LOKI-19 (gave three
options and a preference, refused the call) · editing research's adjudication
(routed the one-line fix to its owner) · asserting the collector's cause of
death · **running `MAIN=999` myself — the abort test carries the exact risk it
tests, and it is the builder's surface.**

## Q8. MECHANISATION — did any flag become a SCRIPT?
**SIX SCRIPTS AND A SPEC. s28 was three.**
`plank_status.py` (D14's second firing) · `freshness.py` (F1/F2/F4 grouped into
one bug) · `rate_budget` fail-closed second blind state · `unrated_run.sh`'s
numeric guard + bounded pairing wait + recorded abort test · `ring_read.py
--selftest` (**11 forced cells, and I verified by mutation that it FAILS**) ·
`corpus_sanity`'s conditional-dead extension · plus **`SPEC-mutation-harness`**,
commissioned by Magnus directly off the sweep.

---

## THE LEDGER — decisions changed ÷ subagent invocations

**2 subagents. Decisions changed: LOKI-17 stopped · LOKI-19 re-framed through
three amendments and a cell swap · LOKI-16b read out and cleared · the ring
decoder swapped and its predecessor retired · the queue reordered (launcher
chains demoted behind the peck plank).** **Both agents' findings are committed,
not left in session memory.**

## WHICH OUTPUT WOULD I NOT PRODUCE AGAIN — the only question that SHRINKS the lane
**The six-finding sweep document, as one document.** Its two live findings are
still open three hours later while every single-flag message was actioned within
minutes. **A finding's chance of being fixed appears to fall with the number of
findings shipped beside it.** Next time: **ship the two live ones as their own
message and let the rest be a document.**

## WHAT DID A PEER CATCH THAT MY PROCESS SHOULD HAVE
**The builder found WHY LOKI-17 was queued at all.** I proved its primary could
not move — a correct and narrower answer. **They asked why a withdrawn plank was
live in HANDOVER**, which is the question that generalised, produced
`plank_status.py`, and would have caught it without any decoder audit.
**I audited the instrument the decision rested on; they audited the decision.**

## INSTRUMENT VERDICT — v1's first firing
**Q4 moved off zero for the first time and Q1 caught a defect the wrap missed
entirely** (per-artefact consumption). **Q3 recorded no improvement, which is
the answer, not a failure of the question.** **Sunset clause: NOT triggered —
every question produced something. FIRINGS: 1.**
