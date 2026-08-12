# RESEARCH ARM RETRO — **v1.7** — run it at every wrap, before the process deltas

**RETRO v1.2 · created 2026-08-10 (s28) · bumped twice 2026-08-11 (s29) · companion to `EXPERIMENT-METHOD-CHANGELOG.md`
(method v3.4) and to `two-session-protocol.md` rule 5.**

**Versioned on the same standard as the method: EVERY QUESTION CARRIES THE INCIDENT
THAT CREATED IT. A question without an incident is a preference; these are scars.**
The `*s28:*` lines under each question are not examples — they are the provenance,
and they are why the question is in the list. **Deleting the incident deletes the
question's licence to exist.**

**Why this exists, and why it is NOT the wrap.** The wrap (`two-session-protocol.md`
rule 5) is lane-agnostic and it is a **failure log** — it records what went wrong.
It never asks whether this lane was **useful**. Those are different questions and
only one of them makes the arm better for the builder and the side lane.

**The premise, stated bluntly so the retro has teeth: this lane's output is worth
exactly what another lane consumes. Everything else is cost** — context, tokens,
and the `doc:code churn` and `cross-lane analysis` signals that `audit_trigger`
fires on. A cut nobody reads is not neutral. It is a debit.

## ⭐ ROUTING — A FINDING IS ROUTED AT **WRITE TIME** OR IT IS NOT A FINDING

**This rule outranks every question below it, because without it the answers land
in a file nobody opens.** Each finding gets exactly one route, written beside it:

| kind of finding | route |
|---|---|
| **behaviour change** | **promote into a file that IS booted** — `docs/coordination.md`, or `docs/research/PROGRAMME-drift-watch-2026-08-09.md` |
| **instrument change** | a **version bump** of the instrument, with the incident |
| **a rule that should be a script** | hand it to the builder **and** write a dated spec — an unbuilt script is prose |
| **observation only** | it stays here, and **must label itself `OBSERVATION — NOT ROUTED`** |

**The failure this closes is the comfortable one:** writing *"next time I will…"*
in a document nobody reopens. **It reads as self-improvement and costs nothing to
write**, which is exactly why it accumulates.

**Measured, s29 2026-08-11 — the incident that created this rule.** This file was
bumped to v1.1 carrying three firings and the finding *"retractions reaching a
lane went 3 → 4"* — **the one number that got WORSE, and therefore the one a
successor most needed** — into a file that **no lane's boot sequence opened.**
The side lane found the same defect in theirs (three findings, one survived, and
only by luck: it had been duplicated into the wrap, whose home IS booted). An
audit the same day found **no lane named its arm retro at boot or at wrap** —
`builder.md`'s three "retro" mentions all pointed at the WRAP retro in
`coordination.md`, not at `docs/builder-arm-retro.md`.
**Fixed at the source on Magnus's direct instruction ("Act on it please"): all
three `.claude/commands/*.md` now name their arm retro in BOTH boot and wrap.**
**Applied to itself, this file's own premise — output is worth what another lane
consumes — indicts an unread retro before it indicts anything else.**

## HOW TO VERSION THIS FILE
* **A new question needs a NAMED INCIDENT from a real session** — a cut that went
  unread, a relay that moved a queue, a retraction that reached a lane. **Not a
  good idea, not a symmetry with the other lanes.** Same bar the method uses.
* **Bump MINOR (v1.x)** to add or sharpen a question, or to record a firing.
  **Bump MAJOR (v2.0)** only if the premise changes — i.e. if "output is worth what
  another lane consumes" stops being the thing this arm is optimising.
* **Every bump appends to the CHANGELOG below, citing the session and the incident.**
  A bump with no incident is the failure this file exists to catch, committed by
  the file itself.
* **DELETION IS A LEGITIMATE BUMP.** See the sunset clause.

## ⚠ SUNSET CLAUSE — D25 applied to this file
**A rule born from a failure has ZERO firings at birth by construction.** This file
has zero. **If two successive retros produce nothing that changes behaviour, DELETE
it rather than perform it** — and record the deletion as v-final in the changelog,
with what it failed to catch. **A retro nobody acts on is the same debit as a cut
nobody reads, which is the premise of the file turned on itself.**

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

### 7. DID I NAME A **CAUSE** WHEN I HAD ONLY MEASURED AN **EFFECT**?
**Count separately: effects measured, and causal labels attached to them.** For each
label, was it marked as an inference *in the same message that carried it*?
*s29 incident (the one that created this question): **three times in one session** the
effect was real, load-bearing and correctly measured, and the causal sentence wrapped
around it was wrong — "the race TIGHTENED" (a stale cutoff), "the launcher raid
DELIVERED NOTHING" (a mis-keyed denominator), "a REGRESSION in the shipped bot" (a
deliberate flag). **All three reached a lane. All three were withdrawn.** The habit
of marking inferences exists and fired unprompted for "conversion problem" the same
morning — **it simply did not fire on these three.***
**The derived check, mechanical rather than attitudinal: a causal sentence ships with
the word INFERENCE next to it, or it does not ship.** And: **a name introduced in a
document must cite the file and line implementing it, or be marked PROPOSED** —
`hold_any` was coined in my own adjudication for something no tool computes, and it
became the deciding call of an amendment before anyone checked.

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

## CHANGELOG

### v1.0 — 2026-08-10 (s28) — CREATED
**Incident that created the file:** Magnus asked whether a researcher-specific
retro existed. It did not — the wrap is lane-agnostic and the vault's daily retro
spans all projects, so **nothing anywhere asked what THIS arm should do
differently.** The s28 wrap (D33–D40) was audited against this and found to be a
pure failure log: **eight deltas, not one of which asks whether the lane was
useful.**

Questions seeded, each with its s28 incident:

| # | question | incident that created it |
|---|---|---|
| 1 | Consumption | **2 of 3 library sweeps spawned and never read.** The lane spent tokens and context on cuts that reached no decision. |
| 2 | Latency | The **carrier check beat the leg by ~25 minutes** and changed what fired; the identical work an hour later is archaeology. Value is a function of which side of the decision it lands on. |
| 3 | Relay fidelity | An agent wrote *"flat-to-slightly-up"* over **0.150 → 0.175 → 0.100 → 0.314**; I relayed **"flat — nothing we shipped touched it"**; the builder made it the queue headline; Magnus overturned it. **Payload right, summary wrong, queue moved.** |
| 4 | Own-checks-on-own-work | **Zero of my errors were caught by me.** All three were caught by a peer re-deriving my arithmetic or by Magnus asking about the board. |
| 5 | Declines | Declined almost nothing while `audit_trigger` fired on analysis-outpacing-decisions at **14.43**. |
| 6 | Per-lane delivery + retractions | **Three retractions reached a lane before I corrected them** (Ouroboros "flat", the meta_join-contaminated PANEL-3 pool, the false facing-decoder limit). |

**Closing line B seeded by:** *"an audit of the evidence is not an audit of the
codebase"* — written about another lane in the morning and **committed by me twice
the same afternoon** (asserting no facing decoder existed while `tools/loki9_facing.py`
ships; asserting we had never played `vjg`, whom we have played 8 times). **Both
were one `grep` away**, which is why the derived check is mechanical rather than
attitudinal.

**Firings: 0.** Sunset clause armed.

## The one metric worth tracking across sessions

**decisions changed ÷ subagent invocations.** Not documents produced, not cuts run,
not tokens spent. **If that ratio falls, the lane is drifting toward being a library
nobody reads — which is precisely what happened to `docs/research/tactics/`: 252
files, ~28k lines, and a decision-path citation rate of ZERO until Magnus ordered it
mined on 2026-08-10.**

### v1.1 — 2026-08-11 (s29) — MINOR: **+1 question, and the file's FIRST FIRINGS**

**Bump justified by a named incident, per this file's own bar.** Question 7 (cause
vs effect) is seeded by three s29 retractions in one session, all with the same
shape: **the measurement was right and the causal label was one step off, and all
three reached a lane before being withdrawn.**

**FIRINGS: 3.** The sunset clause is **disarmed** — this file changed behaviour on
its first real application:
1. **Q5 (declines)** fired at boot: `audit_trigger` was at 3/5 and the lane declined
   the library sweep outright, naming the 1.8% conversion rate as the reason. **The
   trigger closed to 1/5 by the wrap** (doc:code churn 1.06→0.99, cross-lane
   4.24→2.38).
2. **Q4 (own-checks-on-own-work)** moved off zero for the first time: one published
   error self-caught (the "race tightened" trend claim) plus **three broken
   instruments caught before publication** — a literal `Z` appended to a local
   timestamp, a `team` column that does not exist in `throws.tsv`, and an unquoted
   `--include=*.py` that returned exactly the zeros the hypothesis predicted.
3. **Q3 (relay fidelity)** was run and came back CLEAN, which is itself the finding:
   **this lane's failure mode moved.** s28's was compressing agent output; s29's was
   causal labelling on the lane's own analysis. **A retro that only asked s28's
   question would have returned "no defects" on a session with three retractions** —
   which is precisely why Q7 exists.

### v1.2 — 2026-08-11 (s29) — MINOR: **the ROUTING rule, and the file's own premise turned on the file**

**Incident:** v1.1 was bumped forty minutes earlier with three firings and the
finding *"retractions reaching a lane went 3 → 4"* **into a file no boot sequence
opened.** Found by the side lane auditing their own retro and checking all three
lanes' command files. **`research.md`: 0 mentions. `sidelane.md`: 0.
`builder.md`: 3, all of them the WRAP retro, none the arm retro.**

**Routed, not merely recorded** — which is the rule proving itself on its first
application:
* **behaviour change → promoted to a booted file.** `.claude/commands/research.md`
  gains boot step 8 (read this file, carry its open items) and an explicit WRAP
  SEQUENCE whose step 1 is *run the retro before the process deltas*.
  `sidelane.md` and `builder.md` fixed the same way, same commit.
* **instrument change → this bump.**
* **a rule that should be a script → BUILT:** `tools/name_check.py` mechanises
  D54. *And it failed its own motivating case on the first attempt* — v1 asked
  "does the name appear anywhere in our source?", passed a four-cell selftest,
  and returned CLEAN on the document that motivated it, because `hold_any`
  appears in `ring_read.py` inside a docstring saying the name means nothing.
  **A mention satisfied a test for existence; the tool reproduced the failure it
  was built to catch.** Fixed to require a definition site; that document is now
  selftest cell 5.

**FIRINGS: 4** (3 from v1.1, plus this one). Sunset clause remains disarmed.

**The durable lesson, and it is bigger than this file: the retro's premise —
"this lane's output is worth exactly what another lane CONSUMES" — applies to the
retro first.** An unread retro is not a neutral artefact. It is the same debit as
the tactics library it was written to diagnose.


### v1.3 — 2026-08-11 (s30) — MINOR: **the first session where this lane's own checks caught more than its peers did**

**Answered from the session's 133 commits and the cross-lane message log, not from
memory.**

**1. CONSUMPTION.** **CONSUMED (changed a decision):** gate 5a-bis → the builder
made LOKI-19 *not* claim the changed premise, and quoted my sentence as the reason.
Heal-response §11 → two roads dose-checked and killed before a window. Pooling
bias → promoted into HANDOVER as a panel rule and produced the Focalground
nomination. Ammo policy → their starvation hypothesis refuted and taped. Sweep 22
→ a D12 relabel in a booted file. Crash induction → a tape row. The `7,052 Ti`
correction → rescoped before it redirected the line. **PENDING:** forward
efficiency + its power audit; the LOKI-21 proposal. **UNREAD: none this session** —
every artefact was relayed and acknowledged.

**2. LATENCY.** Four arrived **before** the decision they bore on: 5a-bis (before
the read-out), the ammo precondition (before I proposed the idea it killed), the
`7,052` correction (before the redirect hardened), and **the power audit on my own
bar (before it was screened at n=64, where it would have been parked as noise)**.
**One arrived after: sweep 22's D12 over-closure**, which by then was in HANDOVER
and had to be corrected in a booted file. **Archaeology cost: one booted-file edit.**

**3. RELAY FIDELITY — FAILED ONCE, AND IT IS THE SAME COMPRESSION FAILURE AS s28.**
I relayed *"FIELD 42.77% gunner"* from `builder-death-attribution` without reading
to the disaggregation **in the same document**, which splits `FIELD_vsUS` (67.6%
sentinel — because *we* are the shooter) from `FIELD_pure` (64.4% gunner). The
honest gap was **+27.5pp, not the +49pp I sent.** **I compressed a document I had
not read to the bottom.** Caught by me, one hour later, while answering an
unrelated question.

**4. OWN-CHECKS — 4 SELF-CAUGHT vs 3 PEER-CAUGHT. The ratio inverted for the first
time.** Self: the sweep-22 estimator spread (−8.00 vs my −6.55); the invalid 1.01%
gunner-exposure control, **excluded pre-publication**; the `FIELD_vsUS` pooling;
**and the power audit that condemned my own bar.** Peer: the D12 over-closure
(side lane), LOKI-21 not being flag-sized (my own a–f agent), both gunner ideas
already tested (builder).

**5. DECLINES — the deliberate one is new and it is a direct consequence of being
burned.** After mis-pricing healer eviction twice, **I declined to name the
intervention three times** (forward efficiency, the opening build gap, builder
attrition) and handed measured gaps with the constants named instead. **A decline
that says "you have the tree" is cheaper than a wrong diff.**

**6. PER LANE.** *Builder:* numbers before decisions ×4, independent verification
×2, cheap kills ×3. *Side lane:* re-derivable primaries; they caught my worst
error and I caught none of theirs. **RETRACTIONS REACHING A LANE: FIVE** — "road
closed" on two offensive rows (also reached a booted file), the 42.77% pooling,
"the crash-induction surface", LOKI-21 "flag-sized", and my own bar's estimator.
**Worse than s29's four. But four of the five were self-caught and NONE was acted
on before withdrawal.**

**7. CAUSE vs EFFECT.** One firing: I called the field's 12.21% no-damage removals
*"the crash-induction surface"* — a weapon named from an effect — and retracted it
unprompted after measuring it. The habit fired correctly elsewhere ("target
availability is inference by elimination, not a measurement").

**FIRINGS: 4.** (1) Q5 produced three deliberate declines. (2) Q4 moved to
self-majority. (3) The routing rule put corrections in **booted** files twice —
the tactics-library banner and the rename banner — rather than in commit messages.
(4) Q3's discipline caught the sweep-22 number **before** it travelled, even though
it failed on the death-attribution document.

**THE ONE THING I WOULD NOT PRODUCE AGAIN:** the first bar on forward efficiency.
**Specifying a ratio without naming its aggregation was the single most expensive
sentence I wrote today** — it would have been screened at n=64 with an MDE of 129%
of level and parked as noise.

### v1.4 — 2026-08-11 (s31) — MINOR: **the session the lane became a GENERATOR, and the retraction count doubled because of it**

**Answered from the session's ~196 commits and the cross-lane message log, not from memory.**

**1. CONSUMPTION — the highest of any session, and nothing went UNREAD.**
**CONSUMED (changed a decision):** the forward-efficiency instrumentation retraction
(builder did not spend 880 games on a bar no harness could read) · the seat/map work
(builder withdrew *"the ruler is bent"*; **no past verdict repriced**) · the LOKI-27
comparator (**both mechanism rows inverted**; builder adopted the v104 control arm
instead) · sweep 23 (**no withdrawal threshold ported**) · dwell 1.30× (**builder had
not written a line of the arm**) · the hazard decomposition → **two counterbattery
arms built** · ring verification (**killed my own lead candidate before it was
queued**) · core-death builder state (**killed the side lane's survival thesis on its
own pre-registered branch, and became the evidentiary basis of `PROGRAMME.md`'s
amended defence field**) · idle/active split (**unblocked #2**) · version strength
(**Part A narrowed from 6 scorable pairings to 2**). **PENDING:** #13's tile numbers,
#12's polarity control. **UNREAD: none.**

**2. LATENCY — the best of any session. EVERY consumed item landed BEFORE its
decision.** The instrumentation retraction beat the 880-game run; the dwell
correction beat the arm being written; #3's withdrawal beat the build; Part A beat
the overnight read-out; the ring verification beat its own queueing. **Archaeology
cost this session: zero.**

**3. RELAY FIDELITY — run on the forward-attribution relay. CLEAN.** I carried the
agent's self-raised caveats (`B` is a range proxy ignoring facing/LOS; *"moved last
round"* is partly a response to danger) into the relay rather than dropping them.
**⇒ THE FAILURE MODE MOVED AGAIN: s28 was compressing agent output, s29 was causal
labelling, s31 is ARITHMETIC IN MY OWN ANALYSIS.** A retro asking only s28's question
would have returned "no defects" on a session with ten retractions.

**4. OWN CHECKS — 5 self-caught vs 6 peer-caught. THE RATIO WENT BACKWARDS from
s30's 4:3.** Self: the 5.11× side-set bug (numerator and denominator over different
side-sets — **the exact fault I had flagged in the LOKI-27 comparator two hours
earlier**); the `econ.tsv` `shots` near-miss (grepped first, repo already knew); the
`match list` display-vs-`createdAt` trap; **my own §3 map-set retraction, on the
control I should have run first**; a print bug reporting a +32.1pp lift as +0.3pp.
Peer: the vacuous saturated fit · `h2h.sh` not downstream of `arena.py` · **the
Goodharting of my own floor alarm** · #13's wrong quantity · #12's structural
confound · my `CLAUDE.md` replacement text reproducing the fault it fixed.

**5. DECLINES — four, and one was correctly REVERSED.** Declined the three-way state
split as aimed at the 17% half — **then reversed it when re-aimed at #2, which is the
right behaviour and worth distinguishing from flip-flopping**. Declined the position
decode that would have rescued a dead thesis (by agreement with its author). Listed
C5 **to rule it out** rather than pad. **Declined to loosen the queue matcher to hit
a number** — that would have been the same Goodhart the GREP gate exists to stop.

**6. PER LANE. ⛔ RETRACTIONS REACHING A LANE: TEN.** (instrumentation · the `h2h.sh`
code path · the map-set §3 · *"your null discriminates nothing"* · the saturated fit ·
2.28× dwell · the *"unexplained 2.3×"* · *"we go forward late"* · the
clearing-sign · #13's two-thirds.) **Up from 5 in s30 and 4 in s29.**
**The honest reading is not "worse work" — it is that the generator role published
far more load-bearing claims. The rate matters more than the count, and NINE OF TEN
were withdrawn before any lane acted.** The tenth (`h2h.sh`) reached a booted file
and was corrected there.

**⛔ AMENDED MINUTES AFTER THE WRAP, BY THE SIDE LANE, AGAINST A GENEROUS ERROR OF
MINE.** I closed to them with *"your lane caught my worst error today and I caught
none of yours."* **That is false, and a generous error in a wrap is still an error in
the record — it is the one kind a successor has no reason to re-check.** I caught at
least three:
1. **`76d704f`.** They had told the builder the forward-efficiency sizing could be
   repaired **free**, off the already-run 4,096-game screen. **My instrumentation
   retraction is what made them open the surface, and that claim died there** —
   otherwise a "free fix" enters a live plan budgeted against data that does not exist.
2. **The transit-vs-station cut refuted a premise they had amplified TO ME as the lead
   generator candidate** (*"the hazard lives in the traverse, so skip it"*), quoted
   from a booted note without opening its source. **That is the D22 fault committed by
   D22's author, and it was found while they were still recommending it.**
3. **My §3 retraction exposed that their audit had checked the three doors I offered
   and never asked whether the comparison was legal** — a finding about their own
   method, handed over by accident.
**⇒ THE HONEST SYMMETRY IS: I caught their worst error and they caught mine.**

**AND ONE THING THAT MAKES THE 5:6 RATIO INTERPRETABLE, recorded because a successor
will read it and could draw the wrong lesson.** *(Theirs, and explicitly NOT offered
as softening.)* **Self-caught vs peer-caught is not comparable across ROLES.** The
generator publishes far more load-bearing claims per hour than the auditor does, so
it has more to be caught at. **The raw ratio invites the conclusion that the generator
role degrades self-catching, when what it actually does is raise the denominator.**
⇒ **The ten retractions with nine withdrawn before any lane acted is the number that
describes THIS SESSION; the ratio describes THE JOB.** *(Corroboration: the side
lane's own Q3 hit 10 — their worst recorded — in the lane whose entire product is
checking other people's claims.)*

**7. CAUSE vs EFFECT — TWO FIRINGS, AND THE SECOND IS A NEW SHAPE.**
*"We go forward late into a matured turret field"* was a causal label on an effect —
**and I DID mark it INFERENCE in the document, then used it unmarked as a queue-row
headline.** ⇒ **A marker on the deliverable does not travel into the queue row, the
commit subject, or the relay.** *(This is the same defect as the `CLAUDE.md` ring
claim, committed by me, on my own text, the same day.)* Second: *"the late build
divergence is downstream of failing to clear"* asserted a causal **sign** that the
data contradicted — replacement means clearing MORE causes MORE builds.

**FIRINGS: 5.** (1) Q5 produced four declines including one refusal to game my own
instrument. (2) Q3's discipline carried agent caveats into relays intact. (3) The
routing rule put corrections into **booted** files four times — `CLAUDE.md`,
`coordination.md` ×2, and **all three `.claude/commands/*.md`**. (4) Q7 caught the
marker-does-not-travel defect. (5) **Q4 fired on my own arithmetic before publication
in the one case that would have been most expensive** — the 5.11× hazard.

**THE ONE THING I WOULD NOT PRODUCE AGAIN: the floor alarm as first written.** A
minimum count is a target, and I met it inside half an hour by admitting six items of
which three died on checks that had not yet run. **The alarm reproduced the exact
failure it was built to catch.** The GREP admission gate is the repair; the lesson is
that **an instrument whose output is a number the author is judged on must be
designed against its own author.**

---

# s32 RUN — 2026-08-11, wrap at 21:1xZ. **v1.4 → v1.5.**

**FIRINGS THIS SESSION: 2.** (The sunset clause needs two successive retros with
zero. This is not one of them.)

## FIRING 1 — ⭐ Q4 FIRED ON MY OWN WORK FOR THE FIRST TIME
Q4 asks whether any of my own checks caught my own errors. **It has read ZERO all
week.** Today it read **two**, and the mechanism was the same both times: **a
POSITIVE CONTROL returned 0.**
Verifying sweep 24's headline I ran my greps against **the wrong corpus** (a
scratchpad dated Aug 10, RoboCup/ICAPS PDFs). Every phrasing returned 0 — **which
looked exactly like confirming the negative.** On the right corpus my harness broke
differently (an unquoted file list passed 41 newline-separated paths as one
argument); every grep errored and `ZERO HITS ON ALL 20 PHRASINGS` printed anyway.
**`enemy` cannot be absent from 166k words of Battlecode postmortems, so a 0 there
is a statement about the INSTRUMENT.** Two false "verified absences" in five
minutes, both caught, neither published.
**ROUTE: behaviour change → already promoted into `docs/coordination.md` (booted).
The general form belongs in the tactics method block and is there:** *run the
positive control in the SAME command as the real grep.*

## FIRING 2 — ⛔ Q-NEW: **A CLOSURE DESERVES A HARDER READ THAN A FINDING, AND I GAVE IT THE SAME ONE**
I published *"the displacement channel is dead"* into `QUEUE.md` **within minutes**
of computing it. The side lane found **immortal-time bias** — a victim must be
alive at round R to be thrown, and *"alive"* includes *"has not yet been removed
undamaged"*, **which is the outcome**. Correcting it with risk-set matching
**REVERSED THE SIGN**: −0.080pp → **+0.265pp**, CI [+0.034, +0.496], ratio 2.50×.
**My selftest could not have caught it: every fixture row had identical timing in
both arms, so exposure and selection were equal BY CONSTRUCTION.** It asserted the
estimator *separates an effect from no effect* — true, and not the clause the
closure rested on. **The clause no assertion touches is where the defect was.**
**ROUTE: NEW QUESTION 7 BELOW (a version bump), plus the retraction promoted into
`coordination.md`, `QUEUE.md` #5 and the SPEC.**

## THE SIX QUESTIONS

**1. CONSUMPTION.** Cuts/relays this session and what each did:
* **sign-error correction** → **CONSUMED**, reached the builder before the
  read-out; it decided whether Amendment 1's *"stop screening for the week"* bar
  fired. Highest-value item of the day.
* **D79 third instance (tactics seed)** → **CONSUMED**, fixed; verified downstream
  by the side lane on sweep 25's output (bar present where load-bearing, absent
  where noise).
* **caveat pass, 12 files** → **CONSUMED**, produced QUEUE #14's second arm.
* **sweeps 24 + 25** → **PARTIALLY CONSUMED**: produced QUEUE #16 and #17. **But 61
  tactics files in 24h bought 2 citations and 0 built arms**, which is why the
  sweeps are stopped.
* **kidnap reader** → **CONSUMED then RETRACTED then re-consumed** as a
  prioritising signal.
* **`cite_check`, `kidnap_fate`, `border_defect_scan`, `target_value` floor** →
  instruments, not cuts. **`border_defect_scan` is UNRUN — a debit I am naming.**

**2. LATENCY.** The sign correction beat the read-out by ~20 minutes and **changed
what the bar did**. The retraction landed ~40 minutes after its own closure — **late
enough that the closure was already in `QUEUE.md`**, which is exactly the cost
Firing 2 is about. Everything else was pre-decision.

**3. RELAY FIDELITY.** Re-read: my relay of sweep 25's *"most buildable item"*.
The agent said *"NO NEW STORE SLOT NEEDED"*; I checked the tree, found **the store
is 16/16 full**, sized the exposure at **≤5.24%** of our side-games, and found the
proposed fix **unsound** (vision-scoped `live` substituted for a global mark).
**I did not pass the agent's framing through.** ✅ — and it is the first relay this
week where I caught the compression before it left.

**4. OWN CHECKS ON OWN WORK.** **TWO (see Firing 1).** Previous: zero.
**But both of my sign/bias errors were caught by the SIDE LANE, not by me** — so
the honest score is: my checks catch my *instruments*, my peers catch my
*inferences*.

**5. WHAT I DECLINED.** **Heal-idle staffing — declined, and it was right.** The
doctrine change reopened it; the admission grep found `_heal_core`,
`_heal_adjacent`, `heal_seats` and the `SLOT_UNDER` latch already shipped. **The
grep ran BEFORE the item counted, so it never became an item.** Also declined:
quoting a target list from `border_defect_scan` before driving it both ways.

**6. PER LANE.**
* **BUILDER** — got the sign correction before the read-out, QUEUE #16/#17 with
  greps run, the crash-weapon design, and the 1650 floor wired into the gate they
  must run. **Survived.**
* **SIDE LANE** — got re-derivable primaries every time; they re-derived my
  version-strength numbers and **found two defects I had missed**. That is the
  protocol working in the direction that costs me something.
* **MAGNUS** — one withdrawn finding (`ship_cadence` counts rollbacks as ships,
  so *"decisions per hour has fallen"* was unsupported) and one retraction. Both
  surfaced by me, unprompted.

## ⭐ NEW QUESTION 7 — added v1.5 on the incident above
**7. DID ANYTHING I PUBLISHED THIS SESSION CLOSE A ROAD? IF SO, WHAT WOULD HAVE
HAD TO BE TRUE FOR IT TO BE WRONG, AND DID ANY ASSERTION TOUCH THAT?**
*Incident (s32): the kidnap closure. Every control passed, the selftest passed, the
strata were matched — and the defect was in the ESTIMATOR'S SELECTION, which no
assertion touched. Name the quantity in one sentence, then ask which clause each
assertion covers. **The uncovered clause is where the defect will be.***
**A CLOSURE IS NOT A FINDING WITH A STRONGER ADJECTIVE. It removes a road from the
queue, so it must survive a harder read than the finding that motivated it.**

---

# RUN s33 — 2026-08-12T17:1xZ. **v1.6. FIRINGS: 4.**

**1. CONSUMPTION.** **CONSUMED (changed a decision):** LOKI-43 withdrawn on my 14× break-even arithmetic · LOKI-44 flagged under-band on 0.042 enemy-builder-deaths/game in r13–20 · `DELVSDEF`'s read made asymmetric on my 74.6%-of-inserts-before-r160 · `#20` demoted and `#21` re-split on my own archive cuts · `queue_check`, `keeper`, `target_value`, `replay_throws`, `replay_events` fixes all consumed · the `SessionStart` hook fixed on Magnus's authorisation. **PENDING:** `#23` forward placement (the strongest item, unbuilt). **UNREAD: none I can name** — unusual, and it is because the output contract changed from documents to queue rows.

**2. LATENCY. Strongest column this session.** LOKI-43, LOKI-44 and `DELVSDEF` were all reached **BEFORE the shard/numbers**. GUNBLANK was **AFTER** the verdict was recorded — archaeology, though it changed the reason on the record.

**3. RELAY FIDELITY.** Re-read the side lane's *"`GUNBLANKREP` is the ONLY replication"* against `corefill_work.txt`: **true for that worklist, and `GUNAXREP` exists from an earlier one.** I corrected it and the correction **strengthened** their D26 — replications have gone to high readers twice, not once. **Checked, not relayed.**

**4. DID MY OWN CHECKS FIRE ON MY OWN WORK? YES — 4 self-caught of 7 retractions**, against s28's zero. Self-caught: the v114 `RULE=held` flag (8 min), the 338-seed ~30× projection, the +78pp scale figure, `#26`'s own `GREP: TODO` padding the floor. **Caught by others: 3** — the `d2_enemy`-as-range misread (builder), `#20`'s population (side lane), the pooling argument (builder).

**5. DECLINED, AND ALL FOUR WERE RIGHT.** The boot tactics sweep (D86, my lane's own audit) · cut #4 rotation (**not decodable** — `events.tsv` carries only BUILD/DEATH; said so rather than inferring) · ~190 games/arm for the ferry rate (the failure mode that mattered was already excluded) · editing `HANDOVER.md`/`settings.json` on a peer's flag (both went to Magnus; he authorised one).

**6. PER LANE.** **BUILDER:** numbers before decisions, four times, and two batteries saved. **SIDE LANE:** re-derivable primaries; they reproduced my sd, my Clopper-Pearson and my base rate to the digit. **RETRACTIONS REACHING A LANE: 7** — s28 was 3, s29 4. **That is the worst number in this retro and it is not all bad: 4 were self-caught within minutes, and the rate rose because I published more, faster, in a lane that now writes queue rows instead of documents.**

**FIRINGS (4):** (a) Q4's *"run a second instrument over your own claim"* → the ceiling cell, the mutation tests, the recompute-on-the-fresh-table. (b) The routing rule → every finding this session landed in `QUEUE.md` or a tool, **not one standalone document**. (c) Q1's *"unread is a debit"* → the output contract changed *because* 313 tactics files bought 7 conversions. (d) Q5 → four recorded declines, all upheld.

**SUNSET: NOT ARMED.** Four firings.

**⭐ NEW QUESTION — Q8: DID I READ THE COLUMNS I ADDED?** *Incident: I added or hardened freshness reporting in four instruments today (`target_value`, `keeper`, `queue_check`, `replay_events`) and **read none of them**. `lg_age_min` — a column the side lane added this morning for exactly this — climbed 39.6 → 464.9 minutes in every row while all three lanes quoted the table it was flagging. The producer underneath was broken in my own surface (156 deferred keeper cycles). **Instrument-hardening is the easy half; a column is worth what someone reads.*** **This is D20's mirror and it is the defect none of today's fixes addresses.**

# ============================================================================
# RUN s34 — 2026-08-12T20:5xZ. **v1.7. FIRINGS: 5.** Answered from the day's
# artefacts (17 research commits, the cross-lane message log, and `git log`).
# ============================================================================

**SHAPE OF THE DAY: this lane produced almost no standalone analysis and almost
nothing but decisions.** Zero new documents in `docs/research/`. Every finding
landed in `QUEUE.md`, `docs/coordination.md`, or a tool. **That is the routing
rule working, and it is the first session where it held for 100% of output.**

## 1. CONSUMPTION — 11 CONSUMED, 3 PENDING, 1 NOT TAKEN (named)
**CONSUMED (another lane acted):** `#23` precondition → **builder cancelled the
cap dose without spending a game** · the claim-2 HOLD → **builder ran a probe
(`0686fdc`) instead of building on my assertion** · the census-fix HAZARD
(`get_nearby_buildings` RAISES, swallowed by `raid.py:472`) → **builder did not
write the wider-radius fix** · belt denominator bar (74.9%) → **builder measured
it and RESTORED their decline (`eeef598`)** · D43 pooled-turret sign inversion →
accepted, re-ranked · D45 stale 92% → **builder built `GUNAX0` (`339e608`) and
verified it independently via enemy turret mix** · D38 ammo flag → closed as a
negative, nothing further spent · `#29` trunk close → row demoted to leaf ·
`queue_check` uniqueness → built, **caught a live collision on its first run** ·
`#28` `LAUNCHER_RESERVE` → **queued tonight** · **the RANKING → acted on verbatim
(`9a5bf61`: cut `RUSHON`, cut one `GUNBLOCK`, add the `LAUNCHER_RESERVE` pair).**
**PENDING:** `#30`, `#31a`, `#14`.
**⚠ NOT TAKEN, and it is named rather than omitted: `#8` seat-relative scan
order.** I ranked it **second** among freed slots and it was not added — **it is
the only row on the board carrying an Elo estimate (~+7-14) and it has now gone
unbuilt for three sessions.** The stated reason is real (it changes an algorithm,
not a constant, so it costs BUILD time and the builder had cores rather than
time) — **but "the largest quantified prize is too expensive to build" is a
finding about our capacity, not about the plank, and it should stop being
re-ranked and start being scheduled.**

## 2. LATENCY — BEFORE on everything that mattered, and that is the whole value
`#23` precondition: **before**, builder's own words — *"it killed my plank before
I spent a game."* Claim-2 hold: **before by minutes** — they had already accepted
it and were queueing a plank on it. The census RAISES hazard: **before** they
wrote the fix. The ranking: **before** the overnight box filled. D45: **before**
`GUNAX0` was built.
**AFTER (archaeology, and it was on MY OWN work): the `#30` sizing.** 7.6% →
"4.6×" → 1.4× — **two of the three reached both peers before the third landed.**

## 3. RELAY FIDELITY — **ZERO SUBAGENTS SPAWNED THIS SESSION.** Nothing to diff.
**Named as a fact, not a virtue.** Standing permission exists and I used none: the
work was short focused cuts where a subagent adds relay risk without saving
context. **The compression failure this question exists for could not occur.**
**What I did instead was verify INBOUND relays, and both held:** the side lane's
pooled z's (**all three reproduced exactly**: -2.26 / +1.96 / +0.51) and the
builder's six trunk shares (**79.0 / 89.3 / 89.7 / 94.9 / 89.3 / 91.7, exact**).

## 4. ⭐⭐ OWN CHECKS ON OWN WORK — **~6 SELF-CAUGHT vs ~7 PEER-CAUGHT. NEAR PARITY, AGAINST s28's ZERO.**
**Self-caught:** the probe that silently returned `NoneType.__doc__` (caught
before reading anything into it) · the impossible cells in my own true-vs-census
table, which is what exposed the mixed population · **the 17-seats-of-8 count,
caught by its own structural maximum** · **withdrawing my own 28 "cap violations"
as proof after finding the second-producer confound myself** · closing my own
ammo flag as a negative · naming and then closing the loose-bound gap unprompted.
**Peer-caught:** the `get_nearby_buildings` premise · the undeclared denominator
switch · the era sample · the solvability bias · shares-vs-rate · the superseded
figure in the DECLARE line · pooled-vs-Wald.
⇒ **Q4 FIRES for the second session running, and this is the first time the two
counts are comparable.**

## 5. DECLINES — **SIX, ALL UPHELD**
Declined to decode the 595-replay backlog (would distort 8 running shards' CPU
timings) · declined to restart `keeper` (operational, builder's surface) ·
declined the per-opponent SALT timing group-by (**the 8-seat structure is
opponent-independent, so no timing result could reopen it — a saved query**) ·
declined to place the builder's `#32` in the fire order (their finding, their
placement) · declined to claim a SIZE on the ammo under-conversion before
measuring it · declined to edit the builder's `#32` row, relaying the estimator
fix instead.

## 6. WHAT EACH LANE GOT — **and FOUR retractions of mine reached a lane**
**BUILDER:** numbers before decisions (every one of the five above), a hazard that
would have cost units or produced a silent null, and a ranking they built from
verbatim. **SIDE LANE:** re-derivable primaries — they re-derived my z's, my trunk
shares and my seat figures, and **found real defects in three of them.**
**⚠ RETRACTIONS THAT REACHED A LANE: FOUR** — claim 2's premise (held before it
was built on), `#30`'s 7.6% sizing, the "4.6×", and the DECLARE-line figure.
**That is up from three in s28 and it is the honest cost of publishing fast.**

## 7. CAUSE vs EFFECT — **one causal label, marked as inference in the same message**
D45's *"consistent with LOKI-25 working"* shipped with **"the archive CANNOT
attribute it"** in the same paragraph, plus the backwards adjacent-version
contrast as the evidence for that. The forward-timing gap, the census leak and
the ammo mechanism were all published as **effects with no causal sentence
attached** — and the ammo one explicitly refused a size. **Q7 fires clean.**

## 8. ⭐ Q8 — **DID I READ THE COLUMNS I ADDED? YES, AND AT BOOT RATHER THAN AT WRAP.**
Read `lg_age_min` in `ship_watch.log` **before** quoting the table it guards —
125.4 minutes and climbing — which is what produced the `keeper` diagnosis. **And
read `queue_check`'s own first live output rather than trusting a green
selftest**, which is what caught the 3:1 noise floor (D48). **The question created
last session changed behaviour this session, which is the only evidence a retro
question is worth its line.**

---

**FIRINGS (5):** (a) **Q8 applied at boot**, not at wrap. (b) **Q5 → six recorded
declines, all upheld.** (c) **Q4 → near parity on self-catches for the first
time.** (d) **Q7 → the single causal label carried its inference marker inline.**
(e) **The routing rule → 100% of output landed in a booted file or a tool; ZERO
standalone documents.**

**SUNSET: NOT ARMED.** Five firings.

## ⭐⭐ NEW QUESTION — Q9: **DID MY CORRECTIONS NEED CORRECTING?**

*Incident, and it is the shape of the whole session: `#30`'s sizing was published
at **7.6%**, corrected by me to **"4.6× bigger"**, and then corrected AGAIN by the
side lane to **1.4× on the quantity that pays**. My D45 correction was about
applying the era rider to a population — **and the fix I shipped applied it to the
SHARE and not to the RATE the share was taken of.** Same with D41→D42: I fixed a
contaminated tile filter by trilateration and the sample I ran it on was an era
sample.*

**A CORRECTION INHERITS THE AUTHORITY OF HAVING BEEN CAREFUL, WHICH IS EXACTLY WHY
THE SECOND ERROR IS HARDER TO SEE.** Nobody re-audits the fix; the diligence is
the disguise. **Count separately: corrections issued, and corrections that were
themselves amended.** *s34: **3 of 6** — `#30`'s sizing (twice), D41's sample,
and the `queue_check` noise floor.*

⇒ **The derived check, mechanical rather than attitudinal: when you correct a
number, re-run the ORIGINAL objection against the corrected number before
publishing it.** *"Is my fix vulnerable to the thing that broke the original?"*
D45's fix was not — and that is the whole finding.
