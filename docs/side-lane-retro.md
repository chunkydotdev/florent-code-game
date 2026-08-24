# SIDE-LANE RETRO — the instrument. **v1.25** (2026-08-24; created v1 2026-08-10; the changelog below is the authority)

**Commissioned by Magnus, 2026-08-10, asked of all three arms.** The generic
session wrap is **lane-agnostic and is a FAILURE LOG** — it records what broke
and never asks whether the lane was worth having. This is the side lane's own
retro: eight questions a drift-watch/prereg-discipline lane must answer that the
wrap cannot.

**Run it at every wrap.** Every question is **measurable**, not a vibe — a retro
that cannot produce a number is an opinion with a template.

> **Versioning:** this file is the INSTRUMENT and carries a changelog at the
> bottom. Each run is a **separate dated instance** (`side-lane-retro-<date>.md`)
> that names the instrument version it ran. **Never edit a past instance** — the
> whole point is that runs are comparable, and an edited instance silently
> breaks the series (same rule the preregs and fixtures follow).

---

## Q1. CONSUMPTION — were flags ACTED ON, or filed?

**Why:** a flag nobody acts on is a cost with no benefit, and the lane produces
nothing else. **How:** count flags raised; of those, how many changed an
outcome, how many were acknowledged-and-dropped, how many were ignored.
**Name the outcome each one changed.**

**s28: ~15 to the builder, effectively all acted on same-session; 6 changed an
outcome. 2 deprioritised on Magnus's time directive and correctly stayed dropped.**

## Q2. LATENCY — did the flag beat the decision it bore on?

**Why: this is the lane's entire product.** The same flag after the decision is
a post-mortem. **How:** per outcome-changing flag, record the gap between the
flag and the action it prevented.

**s28: dose-gate flag ~40 min before the wrong stop would have fired; Amendment 7
before the leg decoded; decoder-validation before +0.017 was read as a plank
failure. All ahead.**

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — **this lane's characteristic failure**

**Why:** the side lane reads primaries and asserts. Research's failure mode is
relay fidelity; the builder's is treating a passing check as its own artefact.
**Ours is publishing a conclusion the primary would have contradicted, when
checking cost seconds.** **How:** count published claims later retracted where
the disconfirming evidence was available and cheap at the time.

**s28: THREE.** *"+64 doubles the reachable ceiling"* (band was already correct);
*"CORE_PAIRS contradicts the platform"* (tested against a FORMULA, not the
engine — the "fix" would have broken a live map); *"the builder edited a live
script"* (the pid had changed — a restart).

## Q4. DID MY OWN WATCH CATCH MY OWN WORK? — the auditor's blind spot

**Why:** a watch that audits three lanes and is blindest to itself is
structurally dangerous, because nobody else is auditing the auditor.
**How:** of my own misses, how many did **I** catch versus another lane?

**s28: 3 of 8 caught by the builder, not by me** (poll-time `ourver`, LOKI-16b's
missing n, the clobbered `PROGRAMME.md` fields). **The drift monitor fired on my
commits all day and never made a substantive catch on my own work.**

## Q5. FALSE POSITIVES — what did flagging cheaply cost?

**Why:** "flag cheaply and early" is standing policy and it is right — but the
price must be counted, not assumed to be zero. **How:** how many flags were
wrong, and did any wrong flag nearly cause harm?

**s28: 2 wrong.** The `CORE_PAIRS` flag was wrong AND **would have caused harm if
acted on** (breaking a live pool map) — the policy survives because the flag
carried both branches and a discriminating test, so it cost one decode instead
of one map.

## Q6. ⛔ STRUCK AT v1.3 AND REPLACED — see the v1.3 changelog. The question below is the ORIGINAL and is kept only so the series stays readable.

> **~~Q6. FAIRNESS — did I characterise another lane's conduct, and was it
> verified?~~** *(struck 2026-08-12 on the sunset clause: four consecutive runs
> at zero. Replaced by **Q6′** below, which covers the thing that actually did
> the damage.)*

**Why:** flags about *work* are cheap to correct; claims about *conduct* land in
a durable record about a colleague. **How:** count conduct claims; for each, was
it verified against the process, or inferred from an artefact?

**s28: one, and it was inferred from a commit timestamp and wrong.** Rule now
standing: **the bar for a conduct claim is what they DID, verified — never what
an artefact permits me to infer.** *(This rule SURVIVES the strike — it is why
the question went quiet, so retiring the question must not retire the rule.)*

## Q6′. CLAIMS ABOUT ANOTHER LANE — including relayed FIGURES about their output

**Why (the incident, s33):** Q6 asked only about *conduct* and went quiet for
four runs, while **the damage was done by a NUMBER.** I wrote *"61 files /
2 citations / **0 built arms**"* about the research lane into my s32 wrap, my s33
boot note, and messages to two lanes. **It was false** — seven tactics converted
into decision artefacts — the figure was **not mine**, it was **scoped to a
24-hour window**, and I repeated it a session later without re-deriving it. **A
conduct claim would have done exactly this much harm and Q6 could not see it.**

**How:** count every claim published about another lane's work or output —
characterisation OR figure. For each: **did I measure it, or relay it? If
relayed, does every repetition carry whose number it is and what window it
covered?**

**s33 baseline (retrofitted from the instance): one, and it was wrong** — the
*"0 built arms"* figure above. **Conduct claims: zero, fourth consecutive run.**

## Q7. WHAT DID I DECLINE, and was declining right?

**Why:** a lane with hard limits produces value by refusing as well as acting,
and refusals are invisible unless recorded. **How:** list them with the reason
and whether it held up.

**s28: three, all held.** Killing a leg runner myself (a blind kill mid-cycle
leaves the prototype live); editing `PROGRAMME.md` on my own relay of a directive
(the builder refused first and was right); every verdict, including two signed
to me.

## Q8. MECHANISATION — did any flag become a SCRIPT?

**Why:** this is the lane's only durable output. **Attention-level rules failed
under time pressure all day; script-level ones held.** A flag that stays prose
must be re-noticed forever. **How:** count flags that became enforced checks.

**s28: three** — `claim_check.py` (from a flag raised manually twice; caught a
fourth instance automatically hours later), the target-value gate built as a
SCRIPT rather than a template line, `oppver_window.py`. **These cannot rot.**

---

## THE LEDGER — close every run with it

> **Prevented: N. Caused: N. Nearly caused: N.**

**s28: prevented ~6 · caused 1** (clobbered machine-readable fields via a
read-modify-write race on a file another lane was editing) **· nearly caused 1**
(the `CORE_PAIRS` "fix").

---

## CHANGELOG

**v1 — 2026-08-10.** Created at Magnus's request after the research arm found the
generic wrap never asks whether a lane was useful. Questions derived from s28's
measured failures rather than invented: Q3 from three retracted claims, Q4 from
3-of-8 misses caught externally, Q6 from one wrong conduct claim, Q8 from the
attention-vs-script pattern that held all day. **First instance:
`docs/side-lane-retro-2026-08-10.md`.**

**BUMP RULES** (aligned with the other two arms' retros, landed the same hour):
**minor** = add or sharpen a question, or record a firing; **major** = only if
the lane's PREMISE changes (today: *the product is a flag that beats its
decision*); **deleting a question is a legitimate bump**, not a failure — a
question that has never discriminated is costing attention. **Every question
must carry the incident that created it; a question without an incident is a
preference wearing an instrument's clothes.**

**SUNSET CLAUSE, armed now: any question with ZERO firings after three runs is
struck at the next bump.** Q5 (false positives) and Q6 (fairness) are the ones
most likely to go quiet — if they do, that is information about the lane, not a
reason to keep asking.

**Known gap, honestly flagged:** every baseline above is **n=1**. A single
session's numbers set no norm — Q3's "three" and Q4's "3 of 8" are datapoints,
not thresholds, and **v2 should not treat them as targets until a second run
exists to compare against.**

---

## ⭐ v1.1 — **ROUTING: WHERE A FINDING GOES, WITHOUT WHICH THIS FILE IS THE TACTICS LIBRARY**

**Seeded by an incident in this instrument's OWN FIRST FIRING (s29), found when
Magnus asked "how do you handle actionable items from the retro?" — and the
answer was that nothing handled them.**

**THE DEFECT, measured on instance s29:** the retro produced three findings.
**One survived, and by luck** — per-artefact consumption happened to be written
into the WRAP as well, and the wrap's home (`coordination.md`) IS in the boot
sequence. **The other two died in the instance:** *"the output I would not
produce again is the sweep as one document"* and *"Q4 moved because I ran a
second instrument over my own claim, not because I was careful."*

**`docs/side-lane-retro.md` and its instances are NOT in `.claude/commands/sidelane.md`'s
boot path.** So a finding that stops here is unread by construction — **which is
exactly what this instrument's own premise condemns** (*"a cut nobody reads is
not neutral, it is a debit"*) and exactly the failure the tactics library died
of: 252 files, decision-path citation rate zero.

**⇒ EVERY FINDING IS ROUTED AT WRITE TIME, OR IT IS NOT A FINDING:**

| kind | route | test that it landed |
|---|---|---|
| **behaviour change** for the next session | **promote to `PROGRAMME-drift-watch-2026-08-09.md`** — that file IS booted | a successor reading only the boot path would act differently |
| **instrument change** (a question is blunt, missing, or dead) | **a version bump here**, per the rules above | the CHANGELOG names the incident |
| **a flag that should become a script** | **route to the builder AND a dated spec under `docs/research/`** | a `tools/` commit cites it |
| **observation only** | stays in the instance, **and is labelled `OBSERVATION — NOT ROUTED`** | nothing; this is the honest bucket |

**AN ITEM WITH NO ROUTE IS AN OBSERVATION, NOT AN ACTION, AND MUST SAY SO.**
The failure mode this closes is the comfortable one: writing *"next time I
will…"* in a document the next session never opens, which reads as
self-improvement and costs nothing to write.

**STANDING ASK, outside this lane's write surface:** `.claude/commands/sidelane.md`
should name the retro in the boot sequence. **This lane may not edit that file
— so until it does, ROUTING is the only mechanism, and it is the reason this
bump exists.**

## CHANGELOG — v1.1

**v1.1 — 2026-08-11 (MINOR: adds the routing rule, records firing 1).**
* **FIRINGS: 1. SUNSET CLAUSE NOT TRIGGERED** — every question produced
  something on instance s29 (`docs/retro-side-lane-2026-08-11-s29.md`).
* **Q4 moved off zero for the first time: 4 of 5 self-caught, against s28's 0 of
  8** — and the recorded mechanism is **running a second instrument over my own
  claim**, not diligence.
* **Q1 produced the finding the WRAP missed entirely: consumption is
  PER-ARTEFACT, not per-lane.** Every single-flag message was actioned within
  minutes; the six-finding sweep was consumed **2 of 6**, and the two left open
  were the LIVE defects.
* **Q3 came back FLAT (three published inferences, same as s28). That is the
  answer, not a failure of the question** — and one of the three was a flag
  alleging a units error while committing one.
* **The routing rule above is itself Q8 applied to this file:** the instrument
  asks whether flags became scripts, and had no mechanism for its own output.

## ⭐ v1.2 — **THE CHARACTERISTIC FAILURE HAS A SINGLE SHAPE NOW, AND TWO QUESTIONS ARE GOING QUIET**

**v1.2 — 2026-08-11 (MINOR: sharpens Q3, merges Q5's scope into it, arms Q6's
sunset, records firing 2). Instance: `docs/retro-side-lane-2026-08-11-s32.md`.**

* **FIRINGS: 2.** (s29 instance, s32 instance.)
* **⛔ Q3 IS THE WORST RECORDED AND IS NO LONGER VARIED: 4 published, and all
  four are ONE fault — INFERRED FROM AN ARTEFACT INSTEAD OF OPENING THE
  PRIMARY.** A `--stat` read as an audit · a docstring read as the code · an
  ALERT line read as the whole event · an arm file read as the holder.
  **⇒ Q3 is re-worded from "publishing a conclusion the primary would have
  contradicted" to name the mechanism: WHICH ARTEFACT STOOD IN FOR WHICH
  PRIMARY.** A count without the substitution is not actionable.
* **⭐ AND THE DIRECTION IS STABLE WITHIN A LANE AND DIFFERS BETWEEN LANES:
  mine ran 4-of-4 toward the COMFORTABLE reading** (a clean clearance, a defect
  that was someone else's, a smaller severity, a danger already passed);
  **s28's ran toward the DRAMATIC; the builder's s32 retro records mixed.**
  ⇒ **Q3 now asks for the DIRECTION as well as the count**, because a lane that
  knows its own attractor can check that side first.
* **⚠ Q5 HAS BECOME Q3's TAIL.** Both s32 false positives were Q3 instances.
  **Q5 is NOT struck** — it still counts the cost, and it caught the one
  near-miss — **but it is now scored as a SUBSET of Q3 and a future bump should
  decide whether it earns its own question.**
* **⚠ Q6 SUNSET ARMED FOR REAL.** Zero conduct claims this run; the clause says
  *any question with ZERO firings after three runs is struck at the next bump.*
  **This is its third quiet run. v1.3 strikes Q6 unless it fires**, and that will
  be information about the lane (conduct claims stopped being a hazard once the
  s28 rule landed), not a failure of the question.
* **⭐ Q8 JUMPED 3 → 6 AND THE CAUSE IS A PRACTICE, NOT AN EFFORT LEVEL: FLAG THE
  DEFECT WITH ITS FIX.** The startup refusal was a named option; the `tled` bar
  named the field, the file, the live column **and its positive control**.
  **A flag arriving with a buildable replacement gets built; a flag arriving as
  a criticism gets acknowledged.** Q8 now asks *"did the flag carry a fix?"*
  alongside *"did it become a script?"*
* **Q7 GAINED A NEW DECLINE TYPE worth counting separately: WITHHOLDING A
  COMPUTED NUMBER FROM THE PERSON ENTITLED TO IT** (the LOKI-29 effect direction
  at 8% of n, on that leg's own no-interim-peek rule, with the numbers offered
  if its owner ruled otherwise). Distinct from declining to ACT; it is declining
  to TELL, and it can be wrong in a way the others cannot.

## ⚠ v1.2.1 — **THE DIRECTION CLAIM DID NOT REPLICATE. A POINT BUMP, NOT A RUN.**

**v1.2.1 — 2026-08-12 (s33, mid-session). POINT bump: records one finding
against Q3 as it occurs.**

**⛔ THIS IS EXPLICITLY NOT A RETRO RUN, AND THE NUMBERING SAYS SO.** The retro
runs at wrap on Magnus's call, as a dated instance. **v1.2 armed Q6's sunset with
*"v1.3 strikes Q6 unless it fires"*, so calling this v1.3 would either strike Q6
on a count nobody has taken or silently break that clause.** Hence **v1.2.1**:
**FIRINGS remain 2 and the Q6 sunset clock is UNTOUCHED.** Recorded now rather
than at wrap because the routing rule says an instrument change is a version
bump, and a finding held for a wrap that may not be called this session is a
finding that dies in a session.

### THE FINDING — Q3's DIRECTION CLAIM IS CONTRADICTED BY ITS FIFTH INSTANCE

**v1.2 concluded:** *"the direction is stable within a lane and differs between
lanes — mine ran 4-of-4 toward the COMFORTABLE reading… a lane that knows its own
attractor can check that side first."*

**Instance 5, s33, 2026-08-12 05:0xZ, self-caught and published
(`fe9d4ca`): it ran DRAMATIC.** I specced an `elo_logger` selftest cell around a
*"duplicate poll double-counts `matches` and ARMS THE SLOT RULE EARLY"* hazard —
**a false stop-loss on the live holder** — and the hazard cannot exist:
`matches` is read absolute from the API and written verbatim, so a duplicate poll
appends a byte-identical row. **I invented a danger rather than dismissing one.**

⇒ **THE ADVICE IN v1.2 IS WEAKER THAN IT CLAIMS AND MUST NOT BE RELIED ON.**
*"Check the comfortable side first"* was drawn from **n=4 within one session**,
and the first out-of-session instance broke it. **A within-session run of four is
not a lane property; it is plausibly one session's mood.** Q3 keeps asking for
the direction — the data is worth having — but **a successor must not use the
direction as a PRIOR** until it has replicated across sessions.

**AND THE MECHANISM WAS UNCHANGED, WHICH IS THE PART THAT DID REPLICATE:**
*inferred from an artefact instead of opening the primary* — I reasoned from `k`
being a DIFFERENCE, a property of the READER, to an accumulation risk in the
WRITER, without opening the writer. **Five for five.** ⇒ **The MECHANISM is the
stable finding; the DIRECTION is not.** That distinction is the whole content of
this bump.

**⭐ AND IT HAPPENED ONE HOUR AFTER I PROMOTED D24, whose own watch form is
"open the primary".** Knowing a checklist does not execute it — the same lesson
the research arm recorded the same morning when they committed a
parallel-implementation defect inside the commit adding the test for it. **Two
lanes, one session, the same shape: the checklist prevents nothing; asking its
question prevents things.**

**SELF-CATCH LEDGER (Q4):** caught by me, before any lane built from it,
**~20 minutes after publishing** — by opening the writer while considering
whether to implement the cell. **The mechanism is again the one Q4 records: a
SECOND instrument over my own claim, not diligence.** Here the second instrument
was "go to build it".

### ⭐ CONJECTURE (not a finding, n=2, one session) — **THE ATTRACTOR MAY TRACK *HAVING A HYPOTHESIS*, NOT LANE IDENTITY**

**Proposed by the research arm, s33, from the pair of errors we each made within
the hour. It explains both, which "lanes have directions" does not.**

| lane | error | had a hypothesis? | direction |
|---|---|---|---|
| research | border/interior join on an invalid key: **+0.52pp, correct sign**, from a key that matched 4,300 of 9,372 rows by coincidence | **YES** — it was their own predicted channel | **toward the hypothesis** |
| side (me) | invented an `elo_logger` duplicate-poll hazard that **cannot exist** | **NO** — speccing cells cold for a file I had not opened | **toward the dramatic** |

⇒ **THE MODEL: errors made while DEFENDING a result run toward it; errors made
while SURVEYING run toward whatever is most alarming.** My four s32 instances were
all made while defending or dismissing something, which is why they read as a
stable "comfortable" direction — **the variable was not the lane.**

**THE TEST, so this is falsifiable rather than a story:** at the next retro,
classify each published error by **whether a hypothesis existed at the time**
before classifying its direction. **If the split is clean, Q3 should ask "did I
have a hypothesis?" instead of "which way did it run?"** — a question a lane can
answer *before* publishing, which the direction question cannot be.

**⛔ LABELLED AS CONJECTURE ON PURPOSE. n=2, across two lanes, in one session —
the same evidentiary weight as the v1.2 direction claim this file just retracted
one section above.** Recording it with its test rather than adopting it is the
whole lesson of that retraction: **a four-instance within-session pattern was
promoted to advice and broke on its first out-of-session case.** This one gets
written down and left to earn its place.

### ⭐ CONJECTURE UPDATE — the builder's s33 retro is the third lane's data, and it BOTH supports and refines it

**Their seven retractions, with direction, from `docs/builder-arm-retro.md`
(`411cc76`) — the first non-uniform direction any lane has recorded:**

| direction | instances |
|---|---|
| **toward their own plank** | the 4.75× gunner dose · *"the r13-20 window has nothing to hit"* · *"the heal absorbs it"* |
| **against their own plank** | *"GUNBORDER delivers 4× the border dose"* — it was **5.8×** |
| **against a teammate, wrongly** | told research their ferry cut was wrong, on a cut that pooled both teams and compared a lowercase column |

**TESTED AGAINST THE CONJECTURE** (*errors made while DEFENDING a result run
toward it; errors made while SURVEYING run toward whatever is most alarming*):
* **3 flattering** — all made while advancing their own plank. **Consistent.**
* **1 against a teammate** — made while attacking someone else's number, i.e.
  defending *"my cut is right"*, and it ran toward that. **Consistent.**
* **1 against their own plank** — the understated GUNBORDER dose. **A GENUINE
  COUNTER-EXAMPLE: a hypothesis existed and the error ran AGAINST it.**

**⇒ THE REFINEMENT, and it is what the counter-example buys: SEPARATE JUDGEMENT
ERRORS FROM ESTIMATOR ERRORS.** The GUNBORDER understatement was **not a
judgement** — it came from the biased dose counter, whose denominator shrank when
the treatment succeeded. **An estimator error takes its direction from the
ESTIMATOR'S bias, not from the author's hypothesis**, so it is outside the
conjecture's scope rather than against it. **On judgement errors the conjecture
is 4 for 4 across three lanes; on estimator errors it makes no prediction and
should not be asked to.**

**⚠ AND ONE ATTRIBUTION CORRECTION I OWE THEM:** *"the r13-20 window has nothing
to hit"* is listed among THEIR flattering errors. **I supplied that framing** —
my D27 flag offered *"against builders 1–2 kills, against a core noise"* without
opening `raid.py:415`, and their measurement followed it. **The direction is
shared, not theirs alone**, and a conjecture about who errs which way must not
silently absorb another lane's contribution into their column.

**STILL A CONJECTURE, now n=3 lanes.** The test at the next retro is unchanged
and now sharper: **classify each published error as JUDGEMENT or ESTIMATOR first,
then by direction.** If judgement errors keep tracking the hypothesis, Q3 should
ask *"did I have a hypothesis, and was this a judgement or an instrument?"* —
both answerable **before** publishing, which the raw direction question is not.

## ⭐ v1.3 — **FIRING 3 RECORDED · Q6 STRUCK AND REPLACED · AND THE INSTANCE THAT DEMANDED THIS BUMP SPENT A DAY UNTRACKED**

**v1.3 — 2026-08-12 (MINOR: records firing 3, executes Q6's sunset, replaces it
with Q6′). Instance: `docs/retro-side-lane-2026-08-12-s33.md`.**

**⛔ FIRST, THE DEFECT IN THIS FILE'S OWN PROCESS, because it is the same shape
as everything the instrument measures.** The s33 instance was **written at the
s33 wrap and never committed** — found untracked at the s34 boot, ~13 hours
later, by `git status`. **The instrument's changelog therefore still read
`FIRINGS remain 2` while a third run sat on disk**, and the v1.2.1 clause
*"v1.3 strikes Q6 unless it fires"* was pointing at a count that had already
moved. **An uncommitted retro instance is the untracked-load-bearing-number
defect this lane promoted into the drift watch (s29: the figure that killed
LOKI-17 and the figure that would have revived it were both outside version
control).** Committed at the s34 boot, **unedited** — *the instance is a past run
and past runs are never edited, so the lateness is recorded HERE and not in it.*
⇒ **ROUTED AS A BUMP RULE: a retro instance is committed in the same action that
writes it.** The wrap is not finished while the instance is untracked.

* **FIRINGS: 3.** (s29, s32, s33.) The Q6 sunset clock ran on runs, and the runs
  had happened.
* **⛔ Q6 STRUCK ON ITS OWN CLAUSE — four consecutive runs at zero conduct
  claims** (s28 one; s29, s32, s33 none). **That is information about the lane,
  not a failure of the question:** the s28 rule (*"the bar for a conduct claim is
  what they DID, verified"*) worked, and the hazard stopped recurring. **The RULE
  is retained above the strike so retiring the question does not retire it.**
* **⭐ Q6′ REPLACES IT, AND THE REPLACEMENT IS EARNED BY A MEASURED HARM RATHER
  THAN INVENTED:** the s33 instance found that the damage Q6 was built to catch
  arrived as **a relayed NUMBER about another lane's output** (*"0 built arms"*,
  false, not mine, scoped to a day, repeated across two sessions and two
  recipients) — **a class Q6 could not see.** Q6′ counts claims about another
  lane's work *or* output, and asks of each whether it was measured or relayed.
* **⚠ Q5 IS NO LONGER Q3's TAIL AND MUST NOT BE STRUCK.** v1.2 scored it as a
  subset of Q3 and flagged it for review. **s33 answers that: 5 wrong flags and
  TWO CAUSED HARM — the first time this lane caused rather than nearly caused**
  (MAGAZINE BURST's misdirected measurement; SURCH30's cancellation, killed
  ~2 minutes before the correction landed). ⇒ **Q5 stays, and the standing
  sentence *"a wrong flag costs a one-line reply"* is FALSE AS WRITTEN and must
  not be quoted unqualified.** The policy still nets out — 24 outcome-changing
  flags against 2 harms — but the price is no longer notional.
* **Q3 = 13, the worst recorded, and the count is not the finding.** The
  mechanism moved from s32's *inferred from an artefact instead of opening the
  primary* to **`A PROXY IS NOT THE CLAIM`** (promoted mid-session as D25, then
  broken twice more after promoting it). **Direction came back MIXED**, which is
  why v1.2's *"check the comfortable side first"* is already retracted at
  v1.2.1. **The MECHANISM replicates; the DIRECTION does not.**
* **Q8 = 10** (s28 3 → s32 6 → s33 10), same practice: **flag the defect with its
  fix.** s33 adds the second condition, learned from the two harms: **the fix
  must name what it was VERIFIED against** — both harmful flags carried buildable
  fixes and an unverified premise underneath.

**CARRIED FORWARD TO v1.4, unchanged and now with a third lane's data:** the
**JUDGEMENT-vs-ESTIMATOR conjecture** (v1.2.1 and its update). The test is fixed
in advance: **classify each published error as JUDGEMENT or ESTIMATOR first, then
by direction, and only then ask whether a hypothesis existed.** Standing at
4-for-4 on judgement errors across three lanes, with one estimator error
correctly out of scope. **It is still a conjecture and must not be used as a
prior.**

## ⚠ v1.3.1 — **SIX CLASSIFIABLE ERRORS IN ONE SESSION, THREE LANES. THE JUDGEMENT/ESTIMATOR SPLIT IS CLEAN AND THE CONJECTURE SURVIVES ITS FIRST REAL TEST.**

**v1.3.1 — 2026-08-12 (s34, mid-session). POINT bump: records conjecture data as
it occurs, per the v1.2.1 precedent. NOT A RETRO RUN — FIRINGS remain 3.**

**Recorded now rather than held for a wrap that may not be called, which is the
whole reason the point-bump mechanism exists.**

**THE TEST, fixed in advance at v1.2.1 and applied here for the first time:**
*classify each published error as JUDGEMENT or ESTIMATOR **first**, then by
direction.* **Classification rule, stated before the table so it cannot be bent
to fit: an ESTIMATOR error is one where the tool or computation produced a wrong
number the author read correctly; a JUDGEMENT error is one where the numbers were
right and the inference was wrong.**

| # | lane | error | kind | hypothesis? | direction |
|---|---|---|---|---|---|
| 1 | builder | *"the belt repair rate worsened MONOTONICALLY"* — its own series rises on the last two transitions | **judgement** | yes (the removal-line invoice) | **toward it** |
| 2 | research | `get_nearby_buildings` default read ACROSS from the neighbouring `get_nearby_tiles` row | **judgement** | yes (their census defect) | **toward it** |
| 3 | side (me) | specified `SHIPGATENULL` without opening the consumer; the cell I asked for could not be read | **judgement** | yes (my own flag's fix) | **toward it** |
| 4 | side (me) | *"not established anywhere I can find"* — a claim about where I had looked, wearing a claim about the repo | **judgement** | **no — surveying** | **toward the alarming** |
| 5 | research | unpooled Wald SE where the two-proportion test pools | **estimator** *(borderline, see below)* | yes | anti-conservative **by construction** |
| 6 | side (me) | execution guard printed `$?` after a pipe ending in `head` — a 0 that prints either way | **estimator** | no | n/a — a constant |

**⇒ ON JUDGEMENT ERRORS THE CONJECTURE IS 4 FOR 4 AND THE SURVEY BRANCH FIRED
FOR THE FIRST TIME.** Three errors made while DEFENDING a result ran toward it;
**#4 was made while SURVEYING and ran toward the alarming**, which is the branch
the conjecture predicted and had never yet observed in the same session as its
complement. **That is the first within-session contrast rather than a between-
session comparison** — and the between-session comparison is what broke the v1.2
direction claim.

**⛔ THE HONESTY PROBLEM WITH THIS TABLE, STATED RATHER THAN MANAGED: I
CLASSIFIED AFTER KNOWING THE DIRECTIONS.** The test says classify first, and for
these six that was not possible — they had already happened. **The obvious
failure mode is filing an inconvenient case as ESTIMATOR to protect the
conjecture, and #5 is exactly that case: choosing Wald over pooled IS a judgement,
and I have filed it as an estimator error on the grounds that its direction comes
from the formula's known bias rather than from the author's wish.** **That
reasoning is defensible and it is also precisely the move that would rescue a
false conjecture.** ⇒ **Flagged, not resolved. If #5 is judgement, the conjecture
is 5 for 5 and gains nothing it did not have; the point is that I cannot be the
one to decide it after the fact.**

⇒ **v1.4 MUST CLASSIFY AT PUBLICATION TIME, NOT AT RETRO TIME.** A one-line tag
on the error when it is retracted — **`KIND: judgement|estimator · HYPOTHESIS:
y/n`** — costs nothing and is the only version of this test that is not
retrospective. **Until that exists, this table is suggestive and must not be
cited as confirmation.**

## ⚠ v1.3.2 — **TWO MORE INSTANCES, AND THE FIRST WHERE I CAN NAME THE STATE I WAS IN BEFORE THE DIRECTION**

**v1.3.2 — 2026-08-12 (s34, mid-session). POINT bump. FIRINGS remain 3.**

**Both published, both on `QUEUE #30`, both within twenty minutes, both corrected
by peers — and both ran toward the row I was supporting.**

| # | claim | kind | hypothesis? | direction | caught by |
|---|---|---|---|---|---|
| 7 | *"`SENTINEL` → nothing"* in `raid.py` | **judgement** | yes (the row) | **toward it** | research (`:366` gives `GUNNER`/`SENTINEL` `pr=3`) |
| 8 | *"local self-play UNDERSTATES the plank"* | **judgement** | yes (the self-play-blindness rule) | **toward it** | builder (local 1.68 vs panel 0.48–0.84 ⇒ **OVERSTATES**) |

**#7 IS A SCOPE ERROR PUBLISHED AS A PROPERTY OF THE TREE.** I grepped **one
function** (`:500-527`), correctly found no sentinel branch, and wrote it as a
claim about the file. **Second time today I generalised from WHERE I LOOKED to
WHAT EXISTS** — the first was *"not established anywhere I can find"* about the
API default, six hours earlier, **which should have been the warning.**

**#8 IS THE UNIFIER FAULT, AND THE CIRCUMSTANCE IS THE FINDING.** I cited `#23`'s
**35.9% vs 57–80%** — *share of ALL turret builds*, 5,618 games, the six TOP
teams — to argue about *enemy forward SENTINELS per game* on a five-opponent
panel. Different quantity, different population; `#21` already records our
forward slot is **81% sentinel** while Pivot builds **10.77 gunners/game**.
**⛔ AND I COMMITTED IT INSIDE THE MESSAGE FLAGGING THE BUILDER FOR A POOLED
DENOMINATOR.** The flag was right. **I enforced the rule and broke it in the same
paragraph** — the repo's *"stating a rule in a document does not enforce it in
that document"*, turned on its enforcer.

**⭐ THE CONJECTURE REFINEMENT THIS BUYS, and it is the first thing here that
predicts rather than describes: the v1.2.1 model has two branches — DEFENDING
runs toward the result, SURVEYING runs toward the alarming. Both of these were
made while AUDITING SOMEONE ELSE'S NUMBER, which the model does not cover — and
both ran toward MY OWN conclusion, not toward the alarming.** The builder's s33
retro has the matching instance (*"against a teammate, wrongly"*, made while
attacking someone else's cut). ⇒ **AUDITING IS A DEFENDING STATE, NOT A SURVEYING
ONE: the auditor has a hypothesis — "the flag I am raising is correct" — and errs
toward it.** **That is a lane-specific hazard for THIS lane specifically, because
auditing is what it does all day.** Judgement errors now **6 for 6** across three
lanes.
⇒ **v1.4's tag should be `KIND · HYPOTHESIS · STATE(defending|surveying|auditing)`,
and `auditing` should be pre-registered as behaving like `defending`.**

## ⚠ v1.3.3 — **I CONCEDED TO A SESSION-LEVEL EXPLANATION AND ITS OWN NEXT DATA POINT FALSIFIES IT**

**v1.3.3 — 2026-08-12 (s34). POINT bump. FIRINGS remain 3.**

**THE CONCESSION, made to Magnus in-session:** the builder proposed that all four
lanes' errors today ran toward *"whatever row was being supported"*, i.e. **a
property of the SESSION, not of any lane** — and I relayed that as *"a better
explanation than the lane-specific one I'd just written."*

**⛔ IT IS NOT BETTER, AND THE DISCONFIRMATION ARRIVED IN THE BUILDER'S OWN NEXT
COMMIT (`eeef598`, minutes later): they OVER-WITHDREW.** The belt repair
denominator came back at **trunk share 89–95%, clear of the 74.9% threshold on
both sides**, so the `v104→v112` decline **survives** — a claim they had already
retracted. **Their words: *"this error of mine ran the OPPOSITE way from today's
other three."*** ⇒ **"every error today ran toward the supported row" was
falsified by the next instance, before I had finished relaying it.**
**I accepted a generalisation at n=4 within one session — which is EXACTLY the
fault v1.2.1 retracted the direction claim for, committed by me while holding the
retraction.**

**⭐ THE REFINEMENT THAT SURVIVES BOTH, and it absorbs the counter-example instead
of being broken by it: ERRORS RUN TOWARD WHATEVER HYPOTHESIS IS LIVE IN THE
AUTHOR'S HEAD AT THE TIME — their own row when defending it, THE CRITIQUE when
responding to one.** The over-withdrawal was made **while accepting a criticism**,
and it ran toward the criticism. That is the same mechanism, not an exception:
**the live hypothesis had changed owner.**

**⛔ AND THE HAZARD IN THAT SENTENCE, NAMED RATHER THAN MANAGED: a model that says
"errors run toward whatever you currently believe" is CLOSE TO VACUOUS.** It
explains every direction after the fact. **It earns its place only through the
one prediction it makes that the alternatives do not: THE DIRECTION SHOULD FLIP
WHEN THE AUTHOR'S LIVE HYPOTHESIS FLIPS — measurably, at the moment a correction
is accepted.** ⇒ **v1.4's tag becomes
`KIND · STATE(defending|surveying|auditing|conceding) · WHOSE HYPOTHESIS`, and
`conceding` is pre-registered to err TOWARD THE CRITIC.** If concession errors
run toward the author's original position instead, the model is wrong and should
be struck rather than patched again.

**LEDGER FOR THIS THREAD: three point bumps in one session (v1.3.1–v1.3.3), and
the instrument has been wrong once at each.** That is not a failure — **it is
what a conjecture under active test looks like** — but a successor should read
the sequence, not any single bump.

## ⭐ v1.3.4 — **ADOPT RESEARCH'S Q9: DID MY CORRECTIONS NEED CORRECTING? (mine: 3.) LAST POINT BUMP BEFORE A RUN.**

**v1.3.4 — 2026-08-12 (s34). POINT bump. FIRINGS remain 3. NO RETRO RUN HAS
BEEN CALLED** — the run fires on Magnus's word, and the research arm running
theirs is not that word.

**⛔ AND THIS IS THE FOURTH POINT BUMP IN ONE SESSION, WHICH IS ITSELF A SIGNAL:
an instrument edited more often than it is RUN is drifting toward being the
work instead of measuring it.** Recorded deliberately as the **last** bump before
a run; a successor seeing five should treat that as a defect in this lane, not a
sign of rigour.

**Q9 (adopted from `docs/research-arm-retro.md` v1.7): of the corrections I
published, how many needed correcting themselves?** **Why it belongs here more
than there: this lane's PRODUCT IS the correction, so a correction that is wrong
is a defect in the only thing it makes.**

**s34, MINE: THREE, and all three were caught by peers rather than by me.**
1. **`SHIPGATENULL` — wrong TWICE.** I specified a calibration cell without
   opening its consumer, then the fix I proposed (control-tree matching) still
   left the cell unreadable because IDENTIFICATION stayed name-based. **Two
   consecutive corrections, both right about the defect, both wrong about the
   fix.**
2. **The self-play direction.** I was about to publish that self-play
   **overstates** SALT; it **understates** it — I was pricing the CUT when the
   plank sells PREVENTION OF REPAIR. *(Caught before publishing, by opening the
   builder's retro instead of reasoning from a commit subject.)*
3. **The session-level explanation.** I relayed the builder's *"all errors today
   ran toward the supported row"* to Magnus as **better** than my lane-level
   account — **and their very next commit was an error running the other way.**

⇒ **THE PATTERN ACROSS ALL THREE IS ONE THING: I WAS RIGHT THAT SOMETHING WAS
WRONG AND WRONG ABOUT WHAT WOULD FIX IT.** The detection was sound every time;
the **prescription** failed. ⇒ **v1.4 should split the ledger: DETECTION accuracy
and PRESCRIPTION accuracy are different numbers and this lane is visibly better
at the first.** A flag that names a fix carries the authority of the detection
into a claim that has not earned it.

**⚠ AND THE ONE THAT IS NOT ON THIS LIST BECAUSE IT WAS NOT A CORRECTION AT ALL:
I printed my own execution guard and ran the tool in the same command**, so the
guard's result was never consumed. **Not a wrong correction — a check I performed
and did not act on**, which is the defect I flagged in three other instruments
today. **It belongs under Q4, and it is the cleanest instance of the auditor's
blind spot this session.**

## ⭐⭐ v1.4 — **FIRING 4. Q9 EARNS ITS PLACE ON ITS FIRST RUN, AND THE LEDGER SPLITS IN TWO.**

**v1.4 — 2026-08-12 (MINOR: records firing 4, promotes Q9 from adoption to a
question with a run behind it, splits the ledger). Instance:
`docs/retro-side-lane-2026-08-12-s34.md`.**

* **FIRINGS: 4** (s29, s32, s33, s34).
* **⭐⭐ THE HEADLINE, AND IT IS NEW: DETECTION AND PRESCRIPTION ARE DIFFERENT
  ACCURACIES AND THIS LANE IS VISIBLY BETTER AT THE FIRST.** All three Q9
  instances have one shape — **right that something was wrong, wrong about what
  would fix it.** ⇒ **the LEDGER now carries both numbers**, and *"prevented"*
  alone was hiding the failure. **Standing rule: a fix is specified against the
  CONSUMER, not against the artefact** — my `SHIPGATENULL` prescription failed
  twice on the same unasked question, *"can the consumer read this?"*
* **Q9 ADOPTED PERMANENTLY** (from `research-arm-retro.md` v1.7). It belongs here
  more than there: **this lane's product IS the correction, so a wrong correction
  is a defect in the only thing it makes.** Carries research's mechanism —
  **a correction inherits the authority of having been careful; the diligence is
  the disguise** — and the derived check: **re-run the ORIGINAL objection against
  the CORRECTED number before publishing.**
* **⭐ Q3 FELL 13 → 4, and the unifier is worth more than the drop: THREE OF THE
  FOUR ARE ONE SUBSTITUTION — a claim about THE SCOPE OF MY SEARCH published as a
  claim about THE WORLD.** One function → the file; my search → the repo; one
  population → the field. **Same fault, three costumes.** ⇒ **Q3 now asks WHAT
  WAS SEARCHED and WHAT WAS CLAIMED, as two fields.**
* **Q5: 3 wrong, ZERO harm** (s33 caused two). **The cause is structural and
  should be stated as the reason the policy survives: every flag shipped with
  BOTH BRANCHES AND A DISCRIMINATING TEST**, so a wrong flag cost a reply. The
  `bots/starter` flag named the experiment that would vindicate its author —
  **and it did, against my suspicion, in ninety seconds.**
* **Q6′: first clean run** — ~8 claims about peers, zero wrong, every relayed
  figure carrying its owner and window. **Conduct claims: fifth consecutive
  zero**, i.e. the s28 rule holds after the question measuring it was struck.
* **Q7 gained a new decline type: ADVISING AGAINST SOMEONE ELSE'S QUERY** (the
  per-opponent group-by, closed by an opponent-independent structural bound).
  **Declining to consume another lane's work is distinct from declining to act
  or to tell.**
* **⚠ Q4 WORSENED BY RATE (5 of 9 vs 6 of 13) and all four external catches were
  on ONE artefact.** The mechanism that caught all five self-catches is unchanged
  and is **not diligence: it is GOING TO USE THE THING.**

**⛔ A DEFECT IN THIS INSTRUMENT'S OWN USE, RECORDED AGAINST ITSELF: FOUR POINT
BUMPS IN ONE SESSION (v1.3.1–v1.3.4) AGAINST ONE RUN.** An instrument edited more
often than it is run is drifting toward being the work instead of measuring it.
**The point-bump mechanism exists so findings do not die waiting for a wrap
(v1.2.1) and that reason is still good — but four is past the useful edge.**
⇒ **v1.5 should cap it: at most TWO point bumps between runs; beyond that, hold
the finding for the instance.**

**CARRIED TO v1.5:** the conjecture, now with a **fourth state**. Tag errors
`KIND(judgement|estimator) · STATE(defending|surveying|auditing|conceding) ·
WHOSE HYPOTHESIS`. **`auditing` is pre-registered to behave like `defending`**
(s34: 4 of 4 ran toward the row I was auditing) and **`conceding` is
pre-registered to err TOWARD THE CRITIC.** **If concession errors run toward the
author's original position instead, the model is STRUCK, not patched** — it is
already close enough to vacuous that a second rescue would finish it.

**SUNSET WATCH:** Q1, Q2, Q8 have fired every run and are load-bearing. **Q5 has
now gone two runs without a harm** — if s35 is also clean, v1.5 should ask
whether it has become a subset of Q9 the way it once was of Q3.

## ⭐⭐ v1.5 — **FIRING 5. A NEW QUESTION EARNED BY A NEW FAULT, AND THE HEADLINE IS THAT KNOWING A DEFECT DOES NOT PREVENT COMMITTING IT.**

**v1.5 — 2026-08-13 (MINOR: records firing 5, adds Q10, caps point bumps, arms the
`conceding` sunset). Instance: `docs/retro-side-lane-2026-08-13-s35.md`.**

* **FIRINGS: 5** (s29, s32, s33, s34, s35).
* **⭐⭐ THE HEADLINE, AND IT IS ABOUT THE AUTHOR RATHER THAN THE QUERY: I FLAGGED A
  DEFECT AND THEN COMMITTED IT THREE TIMES IN THE NEXT ARTEFACT I BUILT.** At
  05:41Z I flagged `cores_idle` for re-implementing `queue_check`'s admission
  instead of calling it. Within two hours `tools/dash` re-derived three quantities
  the repo already computes and **disagreed with all three** — 13 STALLED vs
  DONE/DEAD, 4 queue rows vs 21, a **negative** tape age vs 4.4 min. **The rule was
  in my head, freshly written, in a message I had sent that hour, and it did not
  fire once.** What fired was cross-checking my output against the tool's.
  ⇒ **ROUTED AS A PRACTICE: when writing anything that computes a quantity another
  tool already computes, RUN BOTH AND DIFF THEM BEFORE COMMITTING — not as a test,
  as the act of writing it.** This is D31 turned on the author: **only a forced
  comparison prevents a known defect; knowing it does not.**
* **⭐ NEW — Q10. DID I ADDRESS THE CONCERN AS STATED, OR AS I RE-STATED IT?**
  Earned by a fault new to this lane and worse than its recorded one: **I restated
  the builder's reservation (optional stopping) as a weaker one (precision) and
  then reassured them about the weaker version** — offering a multiplicity
  correction against a fault a fixed-n z cannot see. **A scope error is merely
  wrong; this one is COMFORTING — it hands an author permission they did not ask
  for, on grounds they did not offer.** For a lane whose product IS the objection,
  that is the failure that matters most. **Q10 is answerable BEFORE publishing,
  which the direction question is not.**
* **⚠ Q3 = 5, mechanism replicating for the FOURTH run, and it reached a new axis:
  two of the five were claims about MY OWN CAPABILITY and MY OWN NOVELTY** (*"you
  have the match ids; I do not"*; the elo local-time *"find"* already solved in
  `freshness.py`). **The substitution is not confined to evidence — it reaches
  self-description.**
* **⛔ AND Q4's MECHANISM HAS A BLIND SPOT IT CANNOT REACH.** *Going to use the
  thing* caught 5 of 7 — but **a claim about someone else's inbox has no primary to
  open.** The fix there is not a better check, **it is not making the claim**.
* **Q5 STAYS, and v1.4's question is answered NO:** it is not a subset of Q9,
  because it caught a flag **dropped before publishing** (the borrowed-band
  suspicion), which Q9 cannot see since it never became a correction. **Two
  consecutive runs at zero harm.**
* **Q7 gained a fifth decline type: DECLINING TO INTERPRET A FAVOURABLE NUMBER**
  (v123 at +36.99, k=4, under a look schedule I had just proposed — reported as
  progress, not read). **The only decline of the six that constrained me rather
  than protecting someone else.**
* **Q8 = 6 in code + 2 promoted rules**, practice unchanged: *flag the defect with
  its fix, and name what the fix was verified against.*
* **THE LEDGER IS NOW ROUTINELY SPLIT: DETECTION 16/16 · PRESCRIPTION 14/16.**
  s34's finding holds — **this lane detects better than it prescribes**, and the
  gap is stable across two runs.

**⛔ POINT-BUMP CAP, ADOPTED AS v1.4 ASKED: at most TWO point bumps between runs.**
s34 ran four against one run. **This session ran ZERO** — every finding was held
for the instance or routed straight into a booted file. The mechanism still exists
for findings that would otherwise die in a session; **it is no longer the default.**

**⚠ THE `conceding` BRANCH IS UNTESTED FOR A SECOND ARMED RUN.** I conceded twice
this session and neither concession contained an error, so the branch
pre-registered to *err toward the critic* still has no data.
**⇒ IF IT IS STILL UNTESTED AT v1.6 IT IS STRUCK, NOT CARRIED.** v1.3.3 already
warned that a second rescue would finish this model; **an armed branch that never
fires is the vacuity it was accused of.**

**STANDING CAVEAT ON THIS RUN'S NUMBERS, conceded in the instance:** the meta lane
observed that this lane's consumption ledger was computed **because** a review of it
had been announced. **Self-measurement under observation.** The flags and consuming
commits are anchored in git; the timing of the count was not disinterested.

## ⭐⭐ v1.6 — **FIRING 6. THE `conceding` BRANCH IS STRUCK ON ITS OWN CLAUSE, AND THE LEDGER'S SPLIT REPLICATES A THIRD TIME.**

**v1.6 — 2026-08-13 (MINOR: records firing 6, executes the v1.5 sunset on the
`conceding` branch). Instance: `docs/retro-side-lane-2026-08-13-s36.md`.**

* **FIRINGS: 6** (s29, s32, s33, s34, s35, s36). Zero point bumps this session
  (cap is 2; second consecutive session at zero — findings held for the
  instance or routed straight to booted files).
* **⛔ THE `conceding` BRANCH IS STRUCK, as v1.5 pre-committed:** two sessions
  armed, zero firings. The direction-conjecture's remaining content — judgement
  errors run toward the live hypothesis, estimator errors take their
  instrument's bias — stays as a NOTE, not a model: no branch of it may be used
  as a prior, and no further branches are added. **A model that needed three
  rescues and then starved is done being patched.**
* **⭐ DETECTION 21/21 · PRESCRIPTION 19/21 — the split is now measured THREE
  runs running** (16/16·14/16 → 16/16·14/16 → 21/21·19/21). It is this lane's
  most stable property and the standing rule stands: **a fix is specified
  against the CONSUMER, and a count is specified against the WORLD, not the
  searcher's enumeration** (s36's single Q3 was scope-as-world again).
* **⭐ NEW MECHANISM RECORDED UNDER Q4, and it is the charter working in
  reverse: my past CERTIFICATIONS killed two other lanes' present errors**
  (phantom leg vs my match-info cert; the 10:47 clock vs my two-clock cert).
  A certification is not just a gate at its moment — it is a standing second
  instrument every later claim must survive. **This is the first session where
  the lane's stored artefacts, not its live attention, made the biggest
  catches.**
* **Q5 kept again:** third consecutive zero-harm run, and it caught a
  pre-publication kill Q9 cannot see. **Q10: first clean run since adoption.**
* **Q6′ standing form confirmed under fire:** two source-wrong relays, both
  attributed, both corrected in-channel — and the s36 falsifier episode adds
  the keeper sentence: *a disputed falsifier reading goes up regardless of who
  is right; procedure can be correct while the number is wrong for an hour.*

**SUNSET WATCH:** every surviving question fired this run. Nothing armed.

## ⭐⭐ v1.7 — **FIRING 7. THE DETECTION/PRESCRIPTION SPLIT INVERTS, AND Q3 GAINS THE PHANTOM-DEFECT FORM.**

**v1.7 — 2026-08-14 (MINOR: records firing 7, sharpens Q3). Instance:
`docs/retro-side-lane-2026-08-14-s37.md`.**

* **FIRINGS: 7** (s29, s32, s33, s34, s35, s36, s37). Zero point bumps, third
  consecutive session.
* **⭐⭐ THE HEADLINE: DETECTION 16/18 · PRESCRIPTION 14/14 — the split
  INVERTED.** Three runs measured perfect detection with lossy prescription;
  s37 took both losses on DETECTION, as **phantom defects** (flags on defects
  that did not exist), while every consumed prescription survived contact.
* **⇒ Q3 SHARPENED: the leading mechanism is now READING A PRIOR VERSION'S
  STRUCTURE AS THE CURRENT TREE'S, while auditing.** Both s37 instances
  pattern-matched a sibling/predecessor version (v200's guard layout; a
  remembered arm name) instead of reading the current artefact. **Practice,
  routed here because the retro is this failure's only instrument: before
  flagging a guard-class defect, read the guard's actual condition line in
  the tree being audited — not the version the pattern came from.** This is
  the arm-identity/symbol-identity class turned on the auditor.
* **Q4's stored-cert mechanism confirmed a second run** (the live CAL-3 table
  changing Magnus's answer; the single-build-site premise consumed by three
  preregs). **Six for six on independent re-derivations of certified counts.**
* **Q5: fourth consecutive zero-harm run.** Q6′: zero wrong relays. Q9: zero
  corrections needing correction — a first, and the other face of the
  inverted split.

## ⭐⭐ v1.8 — **FIRING 8. Q3 GAINS THE FRAME RULE, AND THE DOMAIN CHECK IS THE MEASURED SELF-CATCH MECHANISM.**

**v1.8 — 2026-08-14 (MINOR: records firing 8, sharpens Q3). Instance:
`docs/retro-side-lane-2026-08-14-s38.md`.**

* **FIRINGS: 8** (s29, s32, s33, s34, s35, s36, s37, s38). Zero point bumps,
  fourth consecutive session.
* **⭐⭐ Q3 SHARPENED — THE FRAME RULE: A WIRE FIELD IS IN THE PLATFORM'S
  FRAME, NOT OURS.** Both s38 published errors were raw platform fields read
  without normalizing the frame — scoreA/B without the SEAT, a match list
  without its WINDOW — and the session's two near-misses were the same class
  (git dates without the ZONE; a sha without checking the INPUT existed).
  **Practice: before any per-match/per-commit number leaves the lane, name
  the frame — seat, clock, units, window — and show the normalization.**
  This is the s30 winner_seat lesson generalised, committed twice by the
  lane that recorded it.
* **⭐ Q4's measured self-catch mechanism this run: the DOMAIN CHECK, 2-for-2**
  — both frame errors with an ILLEGAL reading (prereg postdating its fires;
  the empty-string sha) were caught pre-publish; both with merely PLAUSIBLE
  readings were published and caught externally. D31's asymmetry, now
  measured on this lane across one session: **prefer queries whose failure
  modes produce illegal values; treat plausible returns as unverified.**
* **Q5: fifth consecutive zero-harm run, and ZERO wrong flags** — s37's
  phantom-defect class produced nothing; the S3 read-the-condition-line
  practice prevented at least two would-be instances. **The s37 sharpening
  worked on its first full session.**
* **Q8: flag→rule compounding at the fastest recorded cadence** (same-hour,
  repeatedly); the panel template went four-amendments-needed → zero inside
  one session. **Detection ~19/22 · prescriptions all consumed (one rightly
  declined on operational grounds — the lens the auditor underweights).**

**SUNSET WATCH: nothing armed; every surviving question fired this run.**

## ⭐⭐ v1.9 — **FIRING 9. THE SPLIT'S ORIGINAL DIRECTION RETURNS, AND Q3 GAINS THE PROMOTER'S-FIRST-USE RULE.**

**v1.9 — 2026-08-14 (MINOR: records firing 9, sharpens Q3). Instance:
`docs/retro-side-lane-2026-08-14-s39.md`.**

* **FIRINGS: 9** (s29, s32, s33, s34, s35, s36, s37, s38, s39). Zero point
  bumps, fifth consecutive session.
* **⭐⭐ DETECTION ~21/23 · PRESCRIPTION ~14/18 — s37's inversion was the
  outlier; the lane's original property (detects better than it prescribes)
  is restored and now measured across five runs.** The compensation observed
  this session: consumers specified my fixes for me (the TLE executable
  split; the bracketed straddle guard) — the system routing around the
  lane's known weakness is acceptable; relying on it is not.
* **⭐ Q3 SHARPENED — THE PROMOTER'S-FIRST-USE RULE.** Both s39 published
  errors were instances of rules I had promoted HOURS earlier (the
  frame/clock note; the lagged-count note) — and the day produced four
  author-is-first-violator instances across three lanes, every one caught by
  a peer, none by its author. **A rule written from a failure is written by
  someone who has just demonstrated they are prone to it. Practice: after
  promoting any rule, treat your own NEXT use of its subject matter as the
  rule's first-application audit — run the check the rule prescribes on
  yourself, deliberately, before publishing.** (Research's v1.12 adopted the
  same question the same hour, independently — Q12 "did a rule I wrote today
  bind ME first?" — which is the cross-lane replication this bump cites.)
* **Q5: sixth consecutive zero-harm run**, and the s37 read-the-condition-line
  practice logged its second and third confirmed pre-publication saves.
* **Q7 logged the decline-to-tell class applied CORRECTLY for the first
  time** (withholding a seen result from a blinded author) — the v1.2 entry
  worried this decline could be wrong in a unique way; s39 shows its
  legitimate face.

**SUNSET WATCH: nothing armed; every surviving question fired this run.**

## ⭐⭐ v1.10 — **FIRING 10. THE RELAY→PRESCRIPTION CHAIN: A WRONG PRESCRIPTION TRAVELS INTO ANOTHER LANE'S ARTEFACT, AND THE ZERO-HARM STREAK ENDS THERE.**

**v1.10 — 2026-08-14 (MINOR: records firing 10, sharpens Q3 and Q9 with the
composite mechanism). Instance: `docs/retro-side-lane-2026-08-14-s40.md`,
committed in this same action.**

* **FIRINGS: 10** (s29, s32, s33, s34, s35, s36, s37, s38, s39, s40). Zero point
  bumps, sixth consecutive session.
* **⭐⭐ THE HEADLINE — A NEW COMPOSITE, NOT A NEW FAULT: RELAY → PRESCRIPTION →
  ANOTHER LANE'S COMMIT.** I inherited a peer's figure (*"CAL-8 is at 16 accepts /
  80 games"*) without re-deriving it, certified a read as legal on it, then issued
  a PRESCRIPTION citing it — and the prescription hardened the false number into a
  **false GROUND in the builder's `80edbcd`**. Two known faults chained: the Q6′
  relayed-figure class feeding the Q9 prescription class. **A relayed number that
  stays in a note is one lane's error; inside a prescription it acquires the
  authority of the detection and travels.** The re-derivation cost one `awk`.
  ⇒ **ROUTED as a behaviour change into `PROGRAMME-drift-watch-2026-08-09.md`
  (the booted file): A PRESCRIPTION THAT CITES A NUMBER RE-DERIVES THAT NUMBER
  FIRST.** v1.4's rule (*a fix is specified against the CONSUMER*) was satisfied
  and insufficient — **a fix is also specified against its own NUMBERS.**
* **⛔ Q5's ZERO-HARM STREAK ENDS AT SIX RUNS**, and it ended through a
  PRESCRIPTION rather than a flag. **The standing sentence *"a wrong flag costs a
  one-line reply"* is false as written for prescriptions** — this one cost another
  lane's commit. Q5 stays; its scope is now explicitly *flags AND the fixes
  attached to them*.
* **⭐ Q4's STORED-INSTRUMENT MECHANISM, THIRD RUN, AND THE CLEANEST INSTANCE YET:
  my own drift watch caught my own hash misattribution** — it emitted my commit
  and the builder's as adjacent lines with distinct hashes, four minutes after I
  armed it. **The catch required no suspicion**, which is the property attention
  cannot supply. 2 of 4 self-caught; the two misses were both figures one command
  away.
* **Q8 = 3 in one 26-minute session** (ARMED-echo code, PROVENANCE token in both
  charters, the six-check spec) — the best rate per unit time recorded. It
  finally rehomes the **bar-null assertion**, named as mechanisation candidate #2
  on 2026-08-10 and unbuilt for four days.
* **Q7 logged a rescope-working decline for the first time**: an analysis commit
  read once for its single in-scope clause and let go, per the 2026-08-13 narrowing.
* **DETECTION 8/9 · PRESCRIPTION 4/5 — the split holds for a sixth run.**

**SUNSET WATCH: nothing armed; every surviving question fired this run.**

**⚠ CARRIED TO v1.11, and it is an obligation rather than a conjecture:** the
`prereg_check.py` **forced-fail certification** is accepted and unrun (the draft
had not landed at wrap). **A certification offered and never performed is this
instrument's own Q8 failure mode** — a successor either runs it or records why not.



## ⭐⭐ v1.11 — **FIRING 11. THE SPLIT INVERTS A SECOND TIME, AND Q3 GAINS THE BORROWED-PREMISE FORM.**

**v1.11 — 2026-08-14 (MINOR: records firing 11, sharpens Q3, retires a settled
claim). Instance: `docs/retro-side-lane-2026-08-14-s41.md`, committed in this
same action.**

* **FIRINGS: 11** (s29, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41). Zero
  point bumps, seventh consecutive session.
* **⭐⭐ THE HEADLINE — Q3 GAINS A NEW FORM AND IT IS THE MOST EXPENSIVE ONE YET:
  THE BORROWED PREMISE. I CERTIFIED A FINDING WHOSE PREMISE I NEVER CHECKED.** I
  re-derived everything *around* another lane's claim — cell counts, the sign
  test, the robustness arithmetic, even a matched-composition correction nobody
  asked for — **and never asked whether its premise was true.** It was not: two
  team NAMES were one `teamId`, renamed mid-day.
  **Direction: toward the AUTHOR'S live hypothesis, not my own.** v1.3.2
  pre-registered `auditing` to behave like `defending` and it does — **but the
  hypothesis defended was the one I was auditing.** ⇒ **Practice, routed here
  because this is the failure's only instrument: when certifying someone else's
  FINDING, the first check is its PREMISE, not its arithmetic. Re-deriving a
  conclusion's numbers is not verification if the thing being claimed was never
  tested.** A certification inherits the authority of having been careful, and
  careful-about-the-wrong-half is the disguise.
* **⛔ RETIRE AS SETTLED: "this lane detects better than it prescribes."**
  **DETECTION 15/17 · PRESCRIPTION 17/17** — the second inversion in six measured
  runs (s37 was the first), and this one is harder: **every prescription survived
  contact, and two were IMPROVED ON by their consumers.** Both detection losses
  were premise-level. **The property is no longer stable and must stop being
  quoted as this lane's signature.** What replicates is the MECHANISM (Q3's
  substitution), never the ledger's direction.
* **⭐ Q5 EARNS ITS KEEP IN A NEW WAY: FOUR PHANTOM FLAGS KILLED BEFORE PUBLICATION**
  by the s37 read-the-condition-line practice — a tie asymmetry already stated in
  the prereg, a road closure that already had its 126 live games, an amendment
  already branch-symmetric, and a byte-identical guard that was the INVERSE of
  the incident it resembled. **Q5 has never before counted flags that did not
  happen; it should, because that is where the s37 sharpening pays.**
* **Q8 = 7, the best rate recorded**, and **v1.10's carried OBLIGATION IS
  DISCHARGED**: the forced-fail certification, *offered, accepted and unrun* at
  s40, was run — then **re-run three times as the tool changed under it**.
  ⇒ **Promoted with it: A CERTIFICATION OF ONE SIDE OF A COMPARISON CARRIES AN
  EXPIRY**, and a certified tool that changes expires its certification. Both
  bound me today.
* **Q4's stored-instrument mechanism, FOURTH consecutive run** — and the cleanest
  form yet: **my own certification harness proved MY OWN FIXTURE wrong**, not the
  tool it was built to audit.
* **Q9 = 2, and both were DETECTIONS rather than PRESCRIPTIONS — a first.**

**SUNSET WATCH: nothing armed; every surviving question fired this run.**

**⚠ CARRIED TO v1.12:** the `gate.py` wiring bundle is unwritten and carries four
of my accepted items (escape-flag tape, local-accepts WARN, CUT-SHORT consumer,
OB13 untracked-arm gap). **A successor certifies it against ONE diff, as the
builder asked — and re-runs the forced-fail harness first, because by then the
certification will have expired again.**

## ⚠ v1.11.1 — **THE LEDGER MEASURES THE INVERSE OF THIS LANE'S OUTPUT. A PEER HAD TO SAY IT.**

**v1.11.1 — 2026-08-14 (s42, mid-session). POINT bump. NOT A RETRO RUN — FIRINGS REMAIN 11**
and the v2.0 question below is **recorded, not executed**: a major bump requires a RUN, and runs
fire on Magnus's word. First point bump since v1.10; the cap is 2 and this session is at 1.

**Recorded now rather than held, per the v1.2.1 mechanism, because it would otherwise die in a
session — which is exactly the failure this instrument's own routing rule exists to stop.**

### THE FINDING — raised by the RESEARCH ARM, not self-caught (a Q4 datum in its own right)

Across one session this lane produced, by category:

| category | count | has a home in the ledger? |
|---|---:|---|
| flags **withheld** before publication (bad query, unverified premise) | 5 | ❌ |
| **phantom** flags killed pre-publication (defect did not exist) | 4 *(s41)* | ❌ |
| flags **corrected before consumption** (right defect, published, narrowed before anyone acted) | 1 | ❌ |
| **published errors** | 3 | ✅ — the only one counted |

**⇒ THE LEDGER COUNTS ONLY THE ERRORS THAT ESCAPED, IN A LANE WHOSE ENTIRE FUNCTION IS CATCHING
THINGS BEFORE THEY ESCAPE.** Research's formulation, and it is sharper than mine: *"a ledger that
counts only the errors that escaped, in a lane whose function is catching things before they
escape, is measuring the inverse of the lane's output."*

**THE PRIOR ATTEMPTS AT THIS ARE THE EVIDENCE IT IS A PREMISE PROBLEM AND NOT A MISSING COUNTER.**
v1.11 already noticed one third of it — *"Q5 has never before counted flags that did not happen; it
should, because that is where the s37 sharpening pays"* — and **recorded it as a note rather than
changing anything.** s41 logged four phantoms with no home. **Two runs have now observed the gap and
neither closed it, because each treated it as a missing tally under an existing question.**

### ⇒ THE PROPOSED v2.0 QUESTION — recorded for the next RUN to accept or reject

> **Q0. WHAT DID NOT HAPPEN BECAUSE THIS LANE WAS RUNNING?** Count, per session:
> flags withheld · phantoms killed pre-publication · flags corrected before consumption ·
> decisions changed before they were taken. **These are the product. Published errors are the
> DEFECT RATE ON the product, not the product.**

**Why this is a MAJOR bump and not another question:** the bump rules say *major = only if the
lane's PREMISE changes.* The premise on record is *"the product is a flag that beats its decision."*
**Today's evidence is that the product is mostly a flag that never becomes one** — and every
existing question (Q1 consumption, Q2 latency, Q5 false positives, Q9 wrong corrections) is
denominated in flags that WERE published. **All eight measure the visible tail of the output.**

⚠ **THE HAZARD IN ADOPTING IT, NAMED BEFORE ANYONE DOES:** *"things I chose not to say"* is
**self-reported and unfalsifiable**, and this lane already retracted one within-session pattern for
resting on n=4 of its own judgement (v1.2.1). **A withheld-flag count is trivially inflatable by a
lane that wants a good number, and no peer can audit it.** ⇒ **If Q0 is adopted it needs an
anchoring rule the other questions do not: a withheld flag counts ONLY if the check that killed it
left an artefact — a command run, a file opened, a message not sent but drafted.** Otherwise this
lane gets a metric it grades itself on, which is the one failure mode a drift watch cannot afford.

**SUNSET WATCH: unchanged. FIRINGS: 11. The v2.0 decision belongs to the next run.**

## ⭐⭐ v1.12 — **FIRING 12. THE DIRECTION MODEL INVERTS: SURVEYING, NOT AUDITING, IS THIS LANE'S HIGH-RISK STATE — AND Q0 IS ADOPTED ON ITS FIRST ANSWER.**

**v1.12 — 2026-08-15 (MINOR: records firing 12, adopts Q0, INVERTS v1.3.2's
pre-registered direction, sharpens Q3 and Q4). Instance:
`docs/retro-side-lane-2026-08-15-s42.md`, committed in this same action.**

* **FIRINGS: 12** (s29, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42).
  One point bump this session (v1.11.1), inside the cap of two.
* **⛔⛔ THE HEADLINE, AND IT OVERTURNS THIS INSTRUMENT'S OWN PRE-REGISTRATION.**
  v1.3.2 pre-registered **`auditing` to behave like `defending`**, on the reasoning
  that *"auditing is what this lane does all day."* **Measured on eight published
  errors: every alarming over-claim came while SURVEYING with no hypothesis —
  4 for 4** (a 53-shard false stall; a locked leg declared DEAD that was asleep;
  *"the fifteen never certified"*; an audit heading that unified three mechanisms
  into one). **The auditing errors were premise-misses, not over-claims.**
  ⇒ **SURVEYING IS THE HIGH-RISK STATE AND THE TELL IS THAT NOBODY ASKED ME TO
  LOOK.** A commissioned audit has a subject and a stopping point; a sweep has
  neither, and the alarming reading is the one that justifies the sweep.
* **⭐ Q3's MECHANISM IS NEW AND UNIFIES SIX OF THE EIGHT: I CHECKED THE SURFACE
  ADJACENT TO THE ONE THAT MATTERED.** A commit that did something adjacent · a
  comment instead of the code's history · the pulled MIRROR instead of the box,
  and never the SCHEDULE · my harness's COVERAGE LINE instead of the probe's
  ASSERTION EXPRESSIONS. **This is not "I did not check" — it is "I checked, one
  surface over", and it produces a PLAUSIBLE answer every time.** ⇒ **Q3 now asks
  WHICH SURFACE was read and WHICH ONE the claim is about.**
* **⭐ Q4's SELF-CATCH MECHANISM SHARPENS TO ITS MOST USABLE FORM YET: A SECOND
  INSTRUMENT IN THE SAME OUTPUT.** A `pgrep -fl` listing printed **for display**
  sat beside a count of `0` and contradicted it — **an ILLEGAL PAIR** — and caught
  three D33 instances I committed inside four minutes while verifying D33 on
  myself. ⇒ **PRINT THE EVIDENCE BESIDE THE VERDICT AND CHECK THEY AGREE.** Not
  suspicion; adjacency. **Q4 itself came back WORST RECORDED — ~2 self-caught of
  8, six caught by the builder** — which is what makes the mechanism worth having.
* **⭐ Q0 ADOPTED PERMANENTLY, on its first answer.** *What did not happen because
  this lane was running?* **12 withheld · 1 corrected before consumption**, against
  **8 published**. **The anchoring rule held: every withheld flag left an artefact**
  (a command run, a file opened, a source read) — **none self-reported**, which was
  the hazard v1.11.1 armed it against. **The lane's largest output category now has
  a home for the first time.**
* **⛔ Q9 = 2, and both were corrections OF MY OWN CORRECTIONS, both ALARMING, both
  milder in truth.** ⇒ **a correction published while surveying inherits the
  surveying direction** — Q3 one level up.
* **Q5: 12 withheld, the highest recorded; 2 wrong flags reached a peer.** ⚠ **And
  one of those was NET-POSITIVE and must be scored as such: SALTREF2-dead was the
  wrong CONCLUSION on a correct INSTRUMENT finding, and it produced two fixes.**
  ⇒ **a wrong conclusion pointing at a real gap is not the same object as a
  phantom, and the ledger should stop treating them as one.**
* **Q8 = 7 became code**, joint-best. **Q6′: one wrong relay**, and its lesson is
  that **"low harm, I told its originator" was luck** — the figure was already a
  headline to the principal.
* **DETECTION ~18/26 · PRESCRIPTION 7/7 CONSUMED, THREE IMPROVED BY CONSUMERS.**
  ⇒ **v1.11's retirement of *"detects better than it prescribes"* HOLDS: prescription
  is the stronger half two runs running.** The improvements were consumers'
  (MDE-inside-the-bar; OB17-as-check-not-obligation; reconstruction-over-anchoring),
  **which is the system routing around the lane's old weakness — acceptable, and
  still not something to rely on.**

**SUNSET WATCH: nothing armed; every surviving question fired.**

**⚠ CARRIED TO v1.13:** the **15 corruption cells owed in `prereg_cert_s41.py`**.
**The harness now reports `CERT: FAIL` until they exist — that is the honest state
and a successor must not read that FAIL as a defect in anything it certifies.**

## ⚠ v1.12.1 — **THE ADJACENT-SURFACE CHECK HAS A THIRD OUTCOME AND THE LEDGER HAS NO COLUMN FOR IT: IT REDIRECTS THE FLAG TO A BETTER ONE.**

**v1.12.1 — 2026-08-15 (s43, mid-session). POINT bump. NOT A RETRO RUN — FIRINGS REMAIN 12.**
First point bump of this session; the cap is 2. **Recorded now under the v1.2.1 mechanism because
the distinction dies with the session otherwise** — it currently exists only in messages to two
peers and in one coordination note that used the *wrong* framing for it.

### THE FINDING

v1.12 sharpened Q3 to *"I checked the surface adjacent to the one that mattered"* and v1.11.1 gave
Q5 a **phantoms-killed-pre-publication** counter. **Both treat the adjacent-surface check as
producing one of two outcomes: a flag, or nothing.** Measured on three instances today, it produces
**three**:

| # | the flag I had | what the adjacent check did | outcome |
|---|---|---|---|
| 1 | *"the dashboard is dead"* (HTTP 000) | `lsof` showed the listener is `:8787`; I curled `:8765` | **KILLED** — pure phantom |
| 2 | *"`fanout.sh`'s holder check accepts any holder"* | `:52` shows `fire()` DOES compare to `$want`; `gate()` is a CLI-liveness gate | **REDIRECTED** — found `INCUMBENT=104` hardcoded instead |
| 3 | *"rollback failure is unwatched"* (`HOLDER_ALERT` read by zero tools) | `holder_watch` IS running and polls the live platform | **REDIRECTED** — found it EXITS on first change, so a leg's own activation consumes it |

⇒ **IN 2 OF 3 THE CHECK DID NOT CANCEL THE FLAG, IT MOVED IT** — to a defect that was **more
specific, still real, and in both cases more consequential than the one I started with.** #3's
redirect is the clearest: *"an alert file nobody reads"* is cosmetic; *"the independent watch is
consumed at the instant the risk window opens"* is a live pre-leg hazard.

### ⇒ WHY THIS IS AN INSTRUMENT CHANGE AND NOT AN OBSERVATION

**Scoring a redirect as a phantom mis-prices the practice in the direction that would retire it.**
Q5 counts phantoms as *cost avoided*; a redirect is **cost avoided AND a better finding produced**,
and the second half is invisible. **A lane reading its own ledger would conclude the adjacent-surface
check mostly cancels its own work** — when today it converted two vague flags into two precise ones.
**That is an argument for checking MORE, and the current ledger cannot make it.**

⇒ **Q5 gains a third bucket: `KILLED` · `REDIRECTED` · `PUBLISHED-AND-WRONG`.** **Q0 counts
REDIRECTED under "what did not happen" only for the flag that died** — the flag that replaced it is
ordinary output and belongs in Q1. **The anchoring rule is unchanged and already satisfied: all
three redirects left artefacts** (an `lsof`, a `grep` of `fire()`, a `pgrep` of `holder_watch`).

**⚠ AND THE HONEST LIMIT, stated because this instrument has retracted a within-session pattern
before (v1.2.1, n=4):** **n=3, one session, one lane, and I classified after the fact.** The 2-of-3
rate is not a rate. **What earns the bucket is not the ratio — it is that the CATEGORY has no home,
which is a structural gap and does not need a sample size.** A successor should count the bucket and
must not quote 2-of-3 as a base rate.

## ⭐⭐ v1.13 — **FIRING 13. Q3's TARGET MOVES FROM EVIDENCE TO COLLEAGUES, v1.12's DIRECTION INVERSION FAILS TO REPLICATE, AND THE CARRIED DEBT IS DISCHARGED.**

**v1.13 — 2026-08-15 (MINOR: records firing 13, re-scopes Q3, retracts v1.12's state finding,
discharges the v1.12 carry). Instance: `docs/retro-side-lane-2026-08-15-s43.md`, committed in this
same action.**

* **FIRINGS: 13** (s29, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43). **Zero point
  bumps this session — one was considered and DECLINED because the finding was already durable in a
  booted file, which is the cap working as intended rather than an absence.**
* **✅ THE v1.12 CARRIED DEBT IS DISCHARGED.** The 15 corruption cells owed in `prereg_cert_s41.py`
  landed: **`COVERAGE 46/46 · CERT: OK`**, built by an `opus` subagent and **verified by me, not
  taken** — denominator independently recomputed at 46, and **mutation-tested: deleting one cell
  gives 45/46 and flips to `CERT: FAIL` against a clean control.** ⇒ *the OK is not
  OK-by-construction*, which is the only form of that claim worth making.
* **⛔⛔ v1.12's HEADLINE DOES NOT REPLICATE AND IS RETRACTED AS A PRIOR.** v1.12 measured *"surveying,
  not auditing, is this lane's high-risk state — 4 for 4 alarming while sweeping with no hypothesis"*
  and named the tell as *nobody asked me to look*. **s43: all five published errors were committed
  while AUDITING, four of five alarming.** ⇒ **the state does not predict; VOLUME OF AUDITING does.**
  **This is the third direction-model this instrument has proposed and had to withdraw** (v1.2's
  comfortable-reading, v1.3.3's session-level, now v1.12's surveying). ⇒ ⛔ **NO FURTHER DIRECTION
  MODEL. Q3 records the substitution and the direction as DATA and proposes no mechanism** — three
  retractions is enough evidence that the direction is not a stable property of anything.
* **⭐ Q3 IS RE-SCOPED ON A NEW AXIS, and it is the run's real finding: THE TARGET HAS MOVED FROM
  EVIDENCE TO COLLEAGUES.** Three of five published errors were claims about a PEER's work — a
  predecessor's HANDOVER, a peer's script, a peer's grep. **v1.12 found the mechanism (one surface
  over); s43 finds it now lands mostly on people.** ⇒ **Q3 now asks WHOSE WORK the claim was about,
  because a wrong claim about a colleague costs their attention and their record, not just mine.**
  **Q6′ and Q3 have converged and a future bump should consider merging them.**
* **⭐ Q4's BLIND SPOT IS NEW AND IS THE BEST SINGLE LESSON: I MEASURED A TREE WHILE AN AGENT WAS
  RESTORING IT.** True at 15:35:35Z, false 70 s later, **with an IN-FLIGHT note on the channel saying
  exactly what was being written.** ⇒ **a measurement of a moving base is a measurement onto a
  snapshot — my own diagnosis of the day's biggest incident, applied to me, unnoticed.**
  **ROUTED AS A PRACTICE: before measuring a shared artefact, check IN-FLIGHT for a writer.**
* **⭐ Q6′ GAINS A HARD RULE FROM A NEW FAILURE: PUSH-STATE IS PART OF ANY CLAIM THAT NAMES A HASH AT
  ANOTHER LANE.** I flagged `e53b83a1` at the builder; **it had never been pushed and would never
  exist for them.** My drift watch reads **local** `git log`. **Applied one hour later before naming
  `b25e58ac` — the only same-session repair of a Q6′ class this instrument has recorded.**
* **Q8 = 7 in code, joint-best**, practice unchanged (*flag the defect with its fix*), **and three
  times the consumer went past the ask** — most sharply `stack.py --batch`, which **deleted the
  failure class instead of fixing the instance.**
* **THE LEDGER: prevented ~11 · caused 0 · nearly caused 0. DETECTION ~19/24 · PRESCRIPTION 7/7,
  three improved by consumers.** ⇒ **v1.11's retirement of *"detects better than it prescribes"*
  holds a third run.**

**SUNSET WATCH:** every question fired. **Q3 and Q6′ are converging and v1.14 should decide whether
they are one question.**

**⚠ CARRIED TO v1.14:** nothing owed in code. **One open observation: the remote-snapshot half of the
control pin is unguarded and I DECLINED to escalate it, with reasoning stated so it can be
overruled** — if a remote result ever disagrees with a local one on the same plank, that is the first
thing to check.

## ⭐⭐ v1.14 — **FIRING 14. Q3's EIGHT INSTANCES COLLAPSE TO A SINGLE MECHANISM FOR THE FIRST TIME, AND Q6′ GAINS THE FLATTERING-CLAIM-ABOUT-SELF FORM.**

**v1.14 — 2026-08-16 (MINOR: records firing 14, unifies Q3, extends Q6′, adds Q9's ambiguity
form). Instance: `docs/retro-side-lane-2026-08-16-s44.md`, committed in this same action.**

* **FIRINGS: 14** (s29, s32–s43, s44). **Zero point bumps this session** — every finding was held
  for the instance or routed straight into `PROGRAMME-drift-watch-2026-08-09.md`, which is the cap
  working rather than an absence.
* **⭐⭐ THE HEADLINE: Q3 RECORDED EIGHT PUBLISHED ERRORS AND ALL EIGHT ARE ONE MECHANISM — I READ
  ONE SURFACE AND REPORTED A PROPERTY OF THE SYSTEM.** Previous runs found the substitution among
  several faults; **s44 is the first where nothing else appears.** Pairings for a poller · 7 shards
  for a board · one archive for an id's existence · an account list for the leg's accepts · a local
  write time for a platform field · one sawtooth sample for a steady state · a prereg's prose for
  running code · **a pronoun for what Magnus meant.**
  ⇒ **Q3's two fields (WHAT WAS SEARCHED / WHAT WAS CLAIMED) are now sufficient; the mechanism needs
  no further sharpening, only counting.**
* **⛔ THE WORST-SITED ERROR THIS INSTRUMENT HAS RECORDED: a DIRECTIVE ATTRIBUTION, VERBATIM, IN A
  BOOTED CHECKLIST** — I encoded Magnus's *"this should always be the case actually"* as a
  mechanisation directive when it answered a question about the wrap rule. **Retracted in three
  minutes because the row itself carried its reading as falsifiable.** ⇒ **PRACTICE: A DIRECTIVE IS
  NEVER ENCODED FROM A PRONOUN.** If the subject comes from context rather than being stated,
  confirm it — asking costs one message, guessing costs a false attribution nobody re-derives.
* **⭐ Q4's SELF-CATCH MECHANISM IS CONFIRMED AND ITS BLIND SPOT IS NOW EXACT.** All four saves came
  from an **ILLEGAL VALUE** (`0.00%` across 10,800 games; 4,755 rows in a 210-row window; a commit
  postdating the clock; a field ABSENT that I had read at boot). **Both errors that escaped to a
  peer returned PLAUSIBLE values.** ⇒ **the mechanism cannot see a plausible wrong answer, and that
  is the entire published set.** The counter-practice this earns: **prefer queries whose failure
  mode is illegal; treat a plausible return as unverified** (s38's domain check, now measured
  4-for-4 against 0-for-2).
* **⭐ Q6′ EXTENDS — THE FLATTERING CLAIM ABOUT SELF IS THE SAME OBJECT AS A CLAIM ABOUT A PEER.**
  Research characterised my retractions as *"six self-caught"*; the buckets say **5 published, 3
  self-caught, 2 needing a peer.** I re-derived and corrected it — **then had to correct it again
  when the builder repeated it into a wrap block.** ⇒ **Q6′ now counts favourable claims about THIS
  LANE, including ones a peer volunteers.** ⛔ **This direction is the more dangerous one: agreement
  about a person arrives as generosity and is socially expensive to test.**
* **⭐ Q9 = 3, and one is a NEW SHAPE worth the bump on its own** (research's formulation, their
  attribution): **A CORRECTION INHERITS THE AMBIGUITY OF THE THING IT CORRECTS.** I over-read a
  pronoun, struck it correctly, and drew an under-read from the strike — the same pronoun, resolved
  against a different nearby paragraph. **v1.4 recorded that a correction inherits the AUTHORITY of
  having been careful; it inherits the AMBIGUITY too.**
* **Q8 = 7 in code, joint-best — and one of them RETIRED THIS LANE from the leg**: the per-flip leak
  check I had been performing by hand is now the scheduler's, halting on any arm-played pairing.
  ⭐ **The best outcome available to this lane is a check that no longer needs it, and it happened.**
* **Q5: 5 killed pre-publication, 1 redirected, ZERO harm — with one near-miss** (a trap alarm that
  would have invited `kill -9`, the one signal that actually strands an arm). ⚠ **The standing
  sentence held only because the recipient audited it:** the attribution flag prompted a formal
  ruling on a defect that did not exist, and cost nothing solely because the builder read their own
  code rather than deferring. **"A wrong flag costs a one-line reply" is conditional on the reader.**
* **LEDGER: prevented ~11 · caused 0 · nearly caused 1. DETECTION ~22/30 · PRESCRIPTION 11/11
  consumed, 3 improved by consumers.** ⇒ **prescription is the stronger half a FOURTH run**, and
  this run at the widest margin. v1.11's retirement of the old signature stands.

**SUNSET WATCH: every surviving question fired. Nothing armed.**

**⚠ CARRIED TO v1.15 — one open, and it is not mine to close:** the **standing scope of the
builder-wraps-then-I-wrap rule** is recorded UNRESOLVED in `docs/two-session-protocol.md`, with
split provenance (builder→research verified in their window; builder→side-lane reported by me and
unverified by them). **Today's instance is resolved; whether it binds future side-lane sessions
awaits Magnus.** A successor must not read "unresolved" as "no wrap trigger exists".

**v1.15 — 2026-08-16 (MINOR: records firing 15, sharpens Q3 and Q4). Instance:
`docs/retro-side-lane-2026-08-16-s45.md`.**
* **FIRINGS: 15** (s29, s32–s44, s45). **Zero point bumps this session.**
* **Q3 SHARPENED — THE ENUMERATION IS PART OF THE QUESTION.** s45 tried to count its own published
  errors MECHANICALLY from commit subjects and got **9, wrong in both directions**: two non-errors
  captured (a pre-commitment registration; an amendment on new evidence) and three missed (corrected
  inside other commits, or in messages that never became commits). **The honest number, 10, required
  reading.** ⇒ **Q3 now asks for the ENUMERATION RULE alongside the count, and requires the count to
  be derived by reading rather than by grep.** *(Origin: research's own D36 instance-2 — "a count is
  only as wide as its enumeration rule" — landing on this lane inside the hour it was written up
  about them.)*
* **Q4 SHARPENED — SELF-CATCHES ARE NOT EVIDENCE OF SELF-AUDIT UNTIL THEY ARE CLASSIFIED BY VALUE.**
  s45 self-caught 4 of 10, and **all four were low-value**: two rendering failures visible as shell
  errors, one same-hour retraction, one post-publication catch. **Every SUBSTANTIVE error — scope,
  attribution, inference — needed a peer.** ⇒ **Q4 now asks not "how many did I catch?" but "how many
  of the ones that MATTERED did I catch?"** ⚠ **On that reading s45 scored 0.**
* **SUNSET WATCH: unchanged. FIRINGS: 15.** Both changes are behaviour-affecting, so the sunset
  clause does not engage.

## ⭐⭐ v1.16 — **FIRING 16. Q8 IS STRUCTURALLY BROKEN BY THE MOMENTUM RULE AND MUST SPLIT; Q3 RECORDS ITS FIRST *TENSE* ERROR; THE `KILLED` BUCKET EARNED ITS KEEP ON A LIVE SAFETY SWITCH.**

**v1.16 — 2026-08-16 (MINOR: records firing 16, splits Q8, adds Q3's second mechanism). Instance:
`docs/retro-side-lane-2026-08-16-s47.md`, committed in this same action.**

* **FIRINGS: 16** (s29, s32–s45, s47). **Zero point bumps this session.**
* **⛔⛔ THE HEADLINE, AND IT IS ABOUT THIS INSTRUMENT RATHER THAN THE LANE: Q8 COUNTS FLAGS THAT
  BECAME SCRIPTS, AND MAGNUS'S MOMENTUM RULE NOW STRUCTURALLY SUPPRESSES THAT COUNT.** *("every
  tooling that needs fix goes to the end of the session at wrap, unless it breaks something that
  makes our loop for finding better bots.")* **s47 scored `Q8 = 1` in code against `7` at s43/s44 —
  and three further flags were ADOPTED and deliberately DEFERRED** (parser divergence, the
  three-valued owner predicate, the remote-gap consequence). ⇒ **a successor reading `1` would
  conclude this lane's mechanisation collapsed. It did not; the queue moved.**
  ⇒ **Q8 NOW ASKS FOR TWO NUMBERS: `ADOPTED` and `BUILT`.** **A rule that changes when work lands
  invalidates any instrument that counts landings, and this is the first time an external directive
  has broken one of these questions.**
* **⭐ Q3 = 8, THE UNIFIER HOLDS A THIRD RUN — 6 of 8 are *a property of a SET reported from a PARTIAL
  VIEW of it*.** Its purest instance yet: **an ABSENCE in a list I never enumerated** (`SEALPECK` was
  floor-stopped 38 minutes before I published that all four arms were clear; the name still appears
  in the tool's output inside a 238-entry registry line, so a grep returns 1 either way).
  ⛔ **AND A SECOND MECHANISM, NEW: A TENSE ERROR.** *"≈7,950 games of fleet time"* was **arithmetically
  correct and described a STOCK** — games already played — **reported in the present tense as a
  FLOW.** ⇒ **Q3 has recorded scope errors for three runs; this is the first where nothing about the
  number was wrong and everything about its TENSE was.** **A successor checks both: what was
  searched, and WHEN the quantity was true.**
* **⭐ Q4 = 2 of 6 SUBSTANTIVE, against s45's 0 of 6** — the first movement since the question was
  sharpened. **Mechanism unchanged for a FOURTH run and it is still not diligence: GOING TO USE THE
  THING.** Both saves came from reaching for an artefact to use it (a carry-forward list; a
  cancellation ledger), **never from re-reading what I had written.** ⚠ **v1.14's blind spot
  re-confirmed: every peer-caught error returned a PLAUSIBLE value.**
* **⭐⭐ Q5's `KILLED` BUCKET JUSTIFIED ITSELF ON ONE CASE, and it is the most valuable thing in the
  run: I drove a live safety switch's ON state through an env hook that does not exist, got the
  "wrong" answer, and was one sentence from publishing *"the ON state is broken"* about the mechanism
  protecting the ladder slot.** Re-driven against the real parameter, it discriminated correctly.
  ⇒ **STANDING: A FAILED DRIVE OF MY OWN INSTRUMENT IS NOT A FINDING ABOUT THEIRS.** **v1.12 added
  this bucket because redirects had no home; s47 shows it also houses the class where the lane's
  product would have been a false defect claim on a live guard.**
* **Q9 = 0, the best recorded** (four corrections, none needing a second pass) — ⚠ **on a small
  denominator inflated by a high correction VOLUME. Not yet a trend.**
* **Q6′: conduct claims ZERO, ninth consecutive run.** Two relayed figures needed correction, both
  same-session. **v1.14's favourable-claim-about-self extension FIRED for the first time:** a peer
  volunteered that this lane's ledger tip was *"the single highest-leverage thing anyone handed them
  today."* **Logged as THEIR judgement about THEIR session, not adopted as a finding about this
  lane** — the checkable half (it falsified their cadence subject; it opened the predicate work) is
  separated from the ranking, which I cannot verify and did not accept.
* **LEDGER: prevented ~10 · caused 0 · nearly caused 1. DETECTION ~10/10 · PRESCRIPTION 4/5.**
  ⇒ **v1.11's retirement of *"detects better than it prescribes"* holds a FIFTH run.** **The single
  wrong prescription was the one recommendation I made about someone else's row** — right that `#79`
  was mis-stated, wrong that a radius extension fixes it.

**SUNSET WATCH: every surviving question fired. Nothing armed.**

**⚠ CARRIED TO v1.17 — one, and it is the Q8 split:** until Q8 reports `ADOPTED` and `BUILT`
separately, **every session run under the momentum rule will under-report mechanisation.** The next
run should also check whether `DEFERRED` items actually landed at their wrap, because **an adopted
flag that never gets built is exactly the routing debt D32 describes, wearing an acceptance.**

---

## ⛔⛔ v1.17 — **FIRING 17. Q8 IS BROKEN BY A DIRECTIVE FOR THE SECOND CONSECUTIVE SESSION; Q9 POSTS ITS WORST-EVER READING; AND v1.11's RETIREMENT OF "DETECTS BETTER THAN IT PRESCRIBES" IS ITSELF RETIRED.**

**v1.17 — 2026-08-17 (MINOR: records firing 17, re-breaks Q8, inverts the detection/prescription split). Instance: `docs/retro-side-lane-2026-08-17-s48.md`, committed in this same action.**

* **FIRINGS: 17** (s29, s32–s45, s47, s48). **Zero point bumps.**
* ⛔⛔ **HEADLINE — MAGNUS PROHIBITED THE MECHANISM THAT PRODUCED THIS SESSION'S BUILD COUNT, AT THE WRAP THAT CLOSED IT.** Verbatim: ***"NO tools should get fixed during the session, everything is fixed in the builders wrap"*** — **absolute, no carve-out.** **This lane's single largest mechanisation win came from re-tagging a flag `DEFER → NOW` under the momentum rule's exception; that exception no longer exists.** ⇒ **`Q8 BUILT` will read ~0 next session FOR A REASON.** ⭐ **v1.16 split Q8 because a directive suppressed it; v1.17 records that a directive has now removed the exception the split was calibrated against.** ⇒ **A QUESTION INVALIDATED BY DIRECTIVES IN TWO CONSECUTIVE SESSIONS IS NOT MEASURING WHAT IT THINKS IT MEASURES.**
* ⚠ **AND THE TAGGING CONSEQUENCE, EFFECTIVE IMMEDIATELY: `NOW` CAN NO LONGER MEAN "FIX THE TOOL NOW" — only "CHANGE BEHAVIOUR NOW"** (stop the unsafe action, add a constraint, hold a leg). **The hazard window stays open longer; that is Magnus's call and it is priced.**
* ⛔ **Q3 = 5 PUBLISHED**, far above any prior session — a working tree attributed to a commit · a bounded read whose answer sat two lines past the bound · `DOSE DELIVERED` off an n=24 control the registered n=120 inverted · a decode boundary adopted as a standing rule before it was checked · and a regime tally that was a numerator with no denominator, repeated to Magnus. **~7 more were KILLED pre-publication, every one by RE-DRIVING ON A SECOND SURFACE; every published one had a single surface behind it.**
* ⛔⛔ **Q9 = 5, THE WORST EVER RECORDED, AGAINST s47's ZERO.** Five corrections needed correcting, including **prescribing an attention-held rule for a disease I had just diagnosed as requiring a mechanism** (superseded by my own hand six minutes later) and **an arithmetic correction that was right, at the wrong layer, about a quantity that dissolved once its population was matched.** ⇒ **correction volume rose with flag volume, and correction-of-corrections rose faster.**
* ⛔ **THE DETECTION/PRESCRIPTION SPLIT INVERTS AND v1.11's RETIREMENT IS RETIRED: DETECTION ~9/9, PRESCRIPTION 2/6.** **Four of six prescriptions were IMPROVED ON DELIVERY by the owning lane** — a provenance line became a cell NAME, a note became a ledger COLUMN, two fix-shapes became KEY conventions. ⇒ ***"detects better than it prescribes" is true again, and the evidence is that the owning lane consistently found a more MECHANICAL form than the one proposed.***
* ⭐⭐ **Q6′ GAINS ITS WORST FORM: AN AUDIT RATIFIES WHAT IT DOES NOT TOUCH.** Correcting a peer's arithmetic while saying nothing about their population ENDORSED the population; the matched repair later reversed the sign. **Banked as `D21(f)`, two-sided, with research's mirror — *the corrected must not treat omission as ratification*.**
* ⛔⛔ **Q4's WORST ITEM IS SELF-INFLICTED AND STRUCTURAL: THIS LANE BROKE ITS OWN DRIFT-WATCH TABLE THREE TIMES**, same mechanism each time (a blank line terminating a markdown row, severing D21's source column). **The third break occurred while adding a clause about fixes being narrower than their defects.** ⭐ **The repair that held was structural — running the structure check IN THE SAME SHELL COMMAND as the edit.** ⇒ ***bind the verification to the mutation, not to the author's memory.***
* ⭐ **Q5's KILLED bucket is now the MAJORITY of this lane's checks (~7 of ~12), and pays at roughly 1:40** — two minutes per check against a lane's afternoon for one false defect claim on a live guard.
* ✅ **Q1 strongest on record: 26 peer commits cite this lane, consumption effectively total.** ✅ **Q6′ conduct claims ZERO, tenth consecutive run.**
* ⭐⭐ **AND THE SESSION'S REAL FINDING, WHICH IS ABOUT THIS INSTRUMENT'S SUBJECT: seven of the day's findings across all three lanes were ONE SHAPE — *the evidence's scope was smaller than the claim's* — arriving through claims, fixes, caveats, audits, tool citations and a monitoring set.** ⛔ **THIS LANE PRODUCED FIVE OF THEM, INCLUDING BREAKING THE ROW THAT DESCRIBES IT.** ⇒ **the checklist is not a description of other lanes' failures; it is a mechanism this lane demonstrates as readily as anyone, which is the strongest argument that it must be MECHANICAL rather than a matter of care.**

**⚠ CARRIED TO v1.18 — one, and it is Q8's SECOND directive-induced break:** **Q8 must stop counting `BUILT`**, because under an absolute wrap rule a mid-session flag cannot become a script. **Honest replacement: `ADOPTED` / `DEFERRED-WITH-A-HOME` / `CORRECTED-IN-RECORD`** — with this session's measurement rule for the third bucket: **a record correction counts only if it changed what a SUCCESSOR would read, not what a peer acknowledged in a message.**

**SUNSET WATCH: every surviving question fired. Nothing armed.**

---

## ⭐⭐ POST-WRAP ADDENDUM TO THE s48 ENTRY — written 2026-08-17T07:31:38Z, AFTER the retro above was banked

**Not a version bump: the instrument's questions are unchanged. This amends the s48 ANSWERS,
because the day's most consequential incident happened AFTER its own retro was written** — which is
itself a finding about running the retro at the wrap rather than at the close.

**THE INCIDENT.** At 07:16:27Z `corefill`'s guard refused: the incumbent/control tree
`bots/_v468kladturbo` had moved (`a9228ccb → 955ec186`) while **three certified arms wrote against
it**, via **uncommitted** edits `git log` could not see.

**WHAT MOVES IN THE ANSWERS:**

* ⛔ **Q3 = 6 PUBLISHED, not 5.** I published *"rows from 07:16:34Z onward measure plank + control-delta"*
  and committed it. **The edits were comment/docstring-only** — stripped-AST identical, which I then
  verified myself. **Retracted within ~7 minutes.** ⭐ **Cause is the session's own dominant shape a
  SIXTH time: I measured that the tree had MOVED and claimed what the movement MEANT.** The hash
  answers the first question and is silent on the second.
* ⛔⛔ **THE DETECTION/PRESCRIPTION SPLIT WIDENS TO ITS FINAL FORM: DETECTION ~10/10, PRESCRIPTION 2/7 —
  and the FIFTH prescription improved on delivery is the most costly one I gave all day.** I said
  `git checkout -- bots/_v468kladturbo/`. The builder **stashed** instead. **Both restore identical
  bytes; only the stash keeps the diff — and the diff is the ONLY artefact that could certify the
  window.** My fix would have converted *"certified clean"* into *"excise ~600 rows on suspicion."*
  ⇒ **banked as `D37` (quarantine, don't revert), and it is the sharpest evidence this file has for
  the rescoped charter's split: *name the defect, hand the fix to the owning lane.*** **The defect
  call was right and ~1 minute fast. The fix call was actively harmful.**
* ⭐ **Q5 (killed-before-publication) gains its best pay-off of the day, and it was the builder's kill,
  not mine** — their first naive `ast.dump` check flagged `eco.py` as changed. **Docstrings live in
  the AST; comments do not.** The stripped form is the correct instrument; the naive one manufactures
  a false positive on exactly the edit class at issue. **Recorded so the next lane does not re-derive it.**
* ⭐⭐ **A NEW Q6′ SHAPE, and it is the good direction: A GUARD'S FALSE ALARMS ARE ITS PREMIUM, AND THE
  NEAR-MISS PRICES THEM.** The firing statistic is the 2700-prefix, so **ROUTESCORE — the one arm that
  actually fired — was clean of the window anyway** (first in-window row 2743, 42 rows past the mark).
  **`BELTBREAK-EARLY` (2560) and `ODINVSSLEIP` (2078) would BOTH have straddled**, the latter by ~622
  rows ≈ **23% of its terminal decision set — and it is the Magnus-facing calibration cell.**
  ⇒ **the guard's value was realised on the arms that did NOT trip it.**
* ⭐ **AND ONE BACKWARD CLOSURE THAT SHORTENED THE SUCCESSOR'S INHERITANCE INSTEAD OF LENGTHENING IT.**
  My *"0 of 101 tapes"* clearance covered lie (a) only; the fix reported three. Audited lie (c)
  (`Winner: Draw` → CONTROL) across **1,150,322 banked rows: no signal** — cap C-share **40.98%
  [28.6, 53.3]** sits **BELOW** its 900–999 neighbour at **48.09%**, and a mis-scored draw can only
  push **ABOVE**. **No re-scoring owed.** ⇒ ***the strongest audit result is the one that REMOVES an
  obligation, and it only exists because the fix's scope was compared against the clearance's.***

**⇒ THE ADDENDUM'S OWN LESSON, carried to v1.18 alongside the Q8 item:** **the retro was written
before the day's largest finding.** **A wrap that runs the retro at wrap time cannot see a post-wrap
incident — so the retro needs an explicit AMEND path rather than a rewrite**, which is what this
section is. **The alternative, silently editing the s48 answers, would have destroyed the record of
what the lane believed at wrap time.**

## ⭐ v1.18 — **FIRING 18. Q8's REPLACEMENT BUCKETS SURVIVE THEIR FIRST RUN; Q3 POSTS ITS BEST READING WITH THE MECHANISM NAMED; THE PLAUSIBLE-VALUE BLIND SPOT CONFIRMS A THIRD TIME.**

**v1.18 — 2026-08-17 (MINOR: records firing 18, ratifies the Q8 bucket split, sharpens nothing). Instance: `docs/retro-side-lane-2026-08-17-s50.md`, committed in this same action.**

* **FIRINGS: 18** (s29, s32–s45, s47, s48, s50). Zero point bumps. *(s49: lane stood down by directive — recorded by research's s49 wrap D6, not a silent gap.)*
* **✅ Q8's v1.17 CARRY IS DISCHARGED ON ITS FIRST RUN: `ADOPTED 4 / CORRECTED-IN-RECORD 2 / BUILT 0` — and the zero reads as the wrap rule working, not as collapse.** The buckets are RATIFIED as the question's permanent form.
* **⭐ Q3 = 2 published, the best recorded (prior: 5-10), against ~4 killed pre-publication — and the discriminator is now stable across SIX runs: every kill came from a primary returning an ILLEGAL value; both escapes returned PLAUSIBLE ones (v1.14's blind spot, third confirmation).** The counter-practice stands: prefer queries whose failure mode is illegal; treat a plausible return as unverified.
* **⭐ Q5's REDIRECTED bucket produced the run's most valuable artefact again** — a dead stall-flag redirected to the heartbeat-never-terminal gap, now wrap debt with an accepted fix shape. Two runs, two redirect payoffs.
* **Q6′ conduct claims: ZERO, eleventh consecutive run.** Q9 = 0 re-corrections. Q7's four declines all held, one vindicated same-session (the unattributed c3d122b7).
* **SUNSET WATCH: every surviving question fired. Nothing armed.**

**⚠ CARRIED TO v1.19 — one:** both Q3 escapes this run were claims whose refuting fact **left no trace on my read surface** (an index state only an empirical drive could show; a file-level ordering the failed append never logged). The existing question asks what I looked at; **the next run should also ask: COULD my surface have shown the refutation at all — and if not, the claim needed the RELAYED-UNVERIFIED label, not a better look.**

## ⭐ v1.19 — **FIRING 19. THE CHARACTERISTIC ERROR HAS MOVED INTO THE LANE'S VERDICTS: BOTH PUBLISHED ERRORS WERE THE WORD "CLEAN". A CLEARANCE NOW NAMES ITS CHECKS.**

**v1.19 — 2026-08-20 (MINOR: records firing 19, discharges the v1.18 carry, adds the clearance rule). Instance: `docs/retro-side-lane-2026-08-20-s51.md`, committed in this same action.**

* **FIRINGS: 19** (s29, s32–s45, s47, s48, s50, s51). Zero point bumps across a three-day session with a ~36 h parked window.
* **⭐⭐ THE HEADLINE: Q3 = 2, both were AUDIT CLEARANCES, and both were the same defect — the word "clean" claiming the audit's whole domain while the work covered a checklist.** "Clean on every check" over a diff read as `+` lines only (a dropped field invisible by the reader's own filter); "CLEAN" on a queue admission whose CONSUMER could not read the row. **Both returned plausible values — the v1.14 blind spot's FOURTH confirmation — and both were caught by the peer whose own defect class they matched.**
  ⇒ **STANDING RULE, effective immediately and applied in this wrap's own REBOOT STATE: A CLEARANCE NAMES ITS CHECKS.** The publishable form is "clean on: [enumerated checks]", never bare "clean" — the enumeration makes a bounded clearance say its bound, which is D21's question answered at write time instead of at the retro.
* **✅ THE v1.18 CARRY IS DISCHARGED AND THE QUESTION IS KEPT:** both escapes' refuting facts WERE on an available surface (one command away each time), so the RELAYED-UNVERIFIED label was not owed — the carry's question ("could my surface have shown the refutation?") cleanly separated these from s50's unavailable-surface class. It stays as a Q3 sub-question.
* **Q8's bucket split holds a second run: ADOPTED 3 / CORRECTED-IN-RECORD 6 / BUILT 0** — the zero again reads as the wrap rule working. Q9 = 0. Q6′ conduct claims: ZERO, twelfth consecutive. Q5's REDIRECTED bucket paid a third straight run (the missing-final-row redirect).
* **Q4 on the sharpened form: 0 of 2 substantive self-caught.** The catches came from the peers whose defect classes matched the misses — recorded in the instance as the structural answer to the auditor's-blind-spot worry, and left there as OBSERVATION.

**SUNSET WATCH: every surviving question fired. Nothing armed. CARRIED TO v1.20: nothing owed in code; the clearance rule's first full-session test is the successor's.**

## ⭐ v1.20 — **FIRING 20. THE CLEARANCE RULE PASSES ITS FULL-SESSION TEST WITH TEETH, AND GAINS THE EXISTENCE-CHECK SUB-RULE; A NEW GAP CLASS NAMED: NOTHING CERTIFIES NON-FIRES.**

**v1.20 — 2026-08-21 (MINOR: records firing 20, adds two Q3/Q2 sub-rules). Instance:
`docs/retro-side-lane-2026-08-21-s52.md`, committed in this same action.**

* **FIRINGS: 20.** Two ships, five lock certs, ~12 flags all consumed, prevented 7 / caused 0.
* **⭐ THE v1.19 CLEARANCE RULE'S FULL-SESSION TEST: PASSED-WITH-TEETH.** Every clearance
  named its checks; the one escape was a WORD exceeding the enumeration ("manifest
  complete" over a table-shape check). ⇒ **SUB-RULE, effective now: a manifest/artifact
  clearance includes a SAMPLED EXISTENCE CHECK of referents before any completeness word.**
* **⭐ Q2's FIRST STRUCTURAL MISS: the hung fire-wake was detected 93 minutes late, from
  another lane's finding — this lane certifies FIRES and nothing certifies NON-FIRES.**
  ⇒ **SUB-RULE: every window-call GO arms a completion-deadline check (fire-confirmed or
  alarm within N minutes), the audit-side deadman.** *(The builder's wake-deadman is wrap
  debt #14; this is the matching lane-side habit.)*
* **Q3 = 3 (all corrected; one relayed figure repeated without re-derivation — the
  relayed-unverified label was owed). Q5 = 0 wrong flags. Q9 = 0. Conduct claims 0, 13th
  consecutive.**
* **Q8 buckets: ADOPTED 9 / CORRECTED-IN-RECORD 4 / BUILT 0** — the wrap rule working;
  report_lint.py reached the 3-failure promotion threshold and is a NAMED wrap debt.

**SUNSET WATCH: all questions fired. CARRIED TO v1.21: the two sub-rules' first
full-session test is the successor's.**

## ⭐ v1.21 — **FIRING 21. BOTH v1.20 SUB-RULES PASS THEIR FULL-SESSION TEST; THE CONCEDING PRE-REGISTRATION FIRES AND IS CONFIRMED; CERTIFICATES GAIN THE HEAD-CHECK.**

**v1.21 — 2026-08-21 (MINOR: records firing 21, ratifies the two v1.20 sub-rules, adds the
certificate HEAD-check, records the conjecture's first confirmed firing). Instance:
`docs/retro-side-lane-2026-08-21-s53.md`, committed in this same action.**

* **FIRINGS: 21.** ~12 flags, consumption effectively total; 11 certificates; prevented ~8 /
  caused 0 / nearly caused 1.
* **✅ BOTH v1.20 SUB-RULES RATIFIED ON A FULL SESSION:** existence-checks fired with teeth
  (RATIFY-F verified executed, not read off a subject line; digests re-derived 5/5 at two
  locks) and the non-fire deadman armed FOUR times with zero invisible windows — against
  s52's 93-minute hung wake, the class did not recur.
* **⭐⭐ THE CONCEDING PRE-REGISTRATION (v1.3.3) FIRED FOR THE FIRST TIME AND THE MODEL
  SURVIVES:** I certified a peer's verdict against my own already-published pre-flag,
  within minutes of reading their contrary artifact, without re-deriving the deciding
  test ("entirely") — the error ran TOWARD THE CRITIC exactly as pre-registered. n=1;
  recorded, not promoted. The working counter-practice, applied twice later the same
  session: before conceding to a contrary reading, RE-DERIVE THE DECIDING CLAUSE rather
  than re-weighing the readings.
* **⭐ NEW SUB-RULE, earned by three stale-at-publication certificates in one session: A
  CERTIFICATE'S WRITING SHELL RE-READS HEAD FOR NEWER ARTIFACTS ON ITS SUBJECT BEFORE THE
  PUSH.** One git-log line; zero stale certificates after adoption.
* **Q3 = 5 published (all corrected in-record), and the vocabulary class is new: twice the
  right substance carried the wrong VERDICT WORD (a "refuted" for an undosed mechanism; a
  "clean" certificate for a superseded verdict). The claims-split that ended it (two
  claims, two words) came from the peer — prescription remains the weaker half.**
* **Q8 buckets hold a third run: ADOPTED 6 / CORRECTED-IN-RECORD 5 / BUILT 0** — the wrap
  rule working; the reachability ratify line is the session's durable export (adopted by
  both lanes, executed in two locks the same day).

**SUNSET WATCH: every surviving question fired. CARRIED TO v1.22: the HEAD-check's first
full-session test; and Q2 should ask whether any deadman's PATTERN failed to match its
target commit (this session's window deadman would have false-fired at 16:08 had it not
been stopped — the grep matched neither the actual completion subject nor the disclosure
form; a deadman whose clear-condition cannot match reality is a non-fire alarm wearing a
fire alarm's clothes).**

## ⭐ v1.22 — **FIRING 22. THE DEADMAN-PATTERN SUB-CHECK RATIFIES; THE NEW RULE IS EARNED BY A CERTIFICATE THAT QUOTED INSTEAD OF RE-DERIVING.**

**v1.22 — 2026-08-22 (MINOR: records firing 22, ratifies the v1.21 Q2 carry, adds the re-derive rule). Instance: `docs/retro-side-lane-2026-08-22-s54.md`, committed in this same action.**

* **FIRINGS: 22.** ~14 flags, consumption effectively total; 6 certificates (DOORWAVE readout · founding chain · four first-contact windows incl. the campaign closure); prevented ~6 / caused 0 / nearly caused 1.
* **✅ THE v1.21 Q2 CARRY RATIFIES ON A FULL SESSION:** four bounded polls, every clear-condition matched the wire's actual completion form, both terminal states emitting — against s52's 93-minute hung wake and s53's would-have-false-fired deadman, the class is now two full sessions clean under the sub-check.
* **⭐⭐ THE HEADLINE RULE, earned by Q3#2: A CERTIFICATE RE-DERIVES EVERY NUMBER IT REPEATS — QUOTING A PARTY'S ARITHMETIC INSIDE A CERT LENDS IT THE CERT'S AUTHORITY WITHOUT THE CERT'S CHECKING.** The one broken clause in six certificates was the one place I pasted the builder's "≥5 kills the 20-min hypothesis" as my own rescue argument; everywhere I re-derived (Wilson, half-widths, bands, fnmatch, boundary reads), nothing broke across the whole session. Sub-rule of the clearance rule: the enumerated checks must each be MINE, or labelled relayed.
* **Q3 = 3 published (all corrected in-record), and the session's unifier is the re-derive gap in all three costumes:** the working tree quoted for the commit; the peer's arithmetic quoted for the window; the artifact's shape quoted for the pin. **Q9 = 1** (the paste-slip correction itself wrong — the auditor's-attractor case, pre-registered by v1.3.2, fired and was caught by the corrected party's own verification).
* **Q8 buckets hold a third run: ADOPTED 5 / CORRECTED-IN-RECORD 3 / BUILT 0** — the wrap rule working; the DEFF v3 text and the verified rate window landed in the always-loaded file at the batch with this lane's two-site/three-site verification run against the evidence commits.
* **OBSERVATION carried from the instance (not routed, stated for the successor):** eight consecutive clean builder waves — the lane's value this session was certifying absence-of-drift and keeping corrections honest, not flag volume.

**SUNSET WATCH: every surviving question fired. CARRIED TO v1.23: the re-derive rule's first full-session test; and Q1 should note whether the fire-side cert pattern (boundary/pins/exposure/leak enumerated per window) survives as the successor's template for the next live campaign.**

## ⭐ v1.23 — **FIRING 23. THE RE-DERIVE RULE RATIFIES ON ITS FULL-SESSION TEST — AND ITS COUNTEREXAMPLE IS THE SESSION'S ONE Q3, WHICH EARNS THE UNFILTERED-ENUMERATION SUB-RULE.**

**v1.23 — 2026-08-22 (MINOR: records firing 23, ratifies the v1.22 re-derive rule, adds
the unfiltered-enumeration/source-extraction sub-rule, rolls the template question).
Instance: `docs/retro-side-lane-2026-08-22-s55.md`, committed in this same action.**

* **FIRINGS: 23.** ~9 flags, consumption total, zero wrong flags; 7 certificates
  (adoption · powered read · decode-vs-bars · lock · disclosure-reversions ·
  correction-drive · audit-report spot-cert); prevented ~5 / caused 0 / nearly caused 0.
* **✅ THE v1.22 RE-DERIVE RULE RATIFIES:** every certificate re-derived what it
  asserted, and the session's ONE published error is precisely a number that skipped the
  full re-derivation — the rule's scope proven by its counterexample.
* **⭐ SUB-RULE (earned by Q3, adopted by both lanes the same hour): ENUMERATE WITH THE
  UNFILTERED INSTRUMENT.** Never publish a count read through head/tail or a quoted
  fragment; when re-deriving a claim about a pattern, extract the pattern from the
  source file by code — the quoted fragment is the claim, not the evidence. Four
  same-class instances in one session (two lanes), all caught by exactly this move.
* **Q5 = 0 wrong flags (best recorded) · Q6′ conduct claims 0, sixteenth consecutive ·
  Q9 = 0.** Q8 buckets hold a fourth run (ADOPTED 3 / CORRECTED-IN-RECORD 3 / BUILT 0).
* **ROLLED to v1.24:** the window-cert-template survival question (no live window fired —
  CRASHREP held pending the model decision; the template remains armed and untested this
  session).

**SUNSET WATCH: every surviving question fired except Q7 (one labelled decline — fired).
Nothing armed.**

## ⭐ v1.24 — **FIRING 24. THE UNFILTERED-ENUMERATION SUB-RULE RATIFIES; THE CERT GAINS THE BYTE-DIFF-OR-LABEL CLAUSE; STATE `certifying` PRE-REGISTERED.**

**v1.24 — 2026-08-22 (MINOR: records firing 24, ratifies the v1.23 sub-rule, adds one
clearance sub-clause, extends the v1.4 tag taxonomy). Instance:
`docs/retro-side-lane-2026-08-22-s56.md`, committed in this same action.**

* **FIRINGS: 24.** ~14 flags, 13 outcome-changing and consumed; ~28 certificates;
  prevented ~11 / caused 0 / nearly caused 0; conduct claims ZERO, seventeenth
  consecutive.
* **✅ THE v1.23 UNFILTERED-ENUMERATION SUB-RULE RATIFIES ON ITS FULL-SESSION TEST** —
  the truncation class did not recur where the rule was applied. ⚠ Both of the session's
  published errors are its NEIGHBOR class (partial-view: a two-site record read at one
  site; a config clause relayed inside a cert) — the sub-rule's wording covers counts,
  not sites; the site form is covered by the new clause below.
* **⭐ NEW SUB-CLAUSE OF THE CLEARANCE RULE (earned by Q3#2): AN ADOPTION CERT EITHER
  RUNS THE BYTE-DIFF AGAINST THE MEASURED ARM ITSELF OR LABELS ITS CONFIG CLAUSE
  RELAYED.** The builder's mechanical half (adoption commits byte-diff before the hash
  lands) is the paired rule; both landed the same hour as the incident.
* **⭐ STATE `certifying` ADDED to the v1.4 tag taxonomy, pre-registered to behave like
  `auditing`/`defending`** — a certificate's authority attaches to every clause in it,
  so an unverified clause inside a cert errs toward the cert's own thesis. One instance
  (s56 Q3#2); the pre-registration makes the next one classifiable at publication time.
* **Q8 buckets, fifth run: ADOPTED 6 / CORRECTED-IN-RECORD 3 / BUILT 0** — the wrap rule
  working; the six adoptions include three registration-template rules adopted by the
  owning lane same-day, the lane's best mechanisation-through-others session.
* **CARRY (THIRD ROLL, with a sunset condition): the window-cert template survival
  question** — no live window fired for a third consecutive session. **If s57 also fires
  none, the carry converts to OBSERVATION and stops rolling.**
* **OPEN, not this lane's to close: the weld-ledger enumeration rule** (certified count
  FIVE true welds; the sweep spec declares its own denominator or its success cannot be
  measured).

**SUNSET WATCH: every surviving question fired. Nothing armed.**

## ⭐ v1.25 — **FIRING 25 (SEASON END). A RIDER'S DIAL FIRES IN A REAL VERDICT — THE FULL FLAG LIFE-CYCLE RECORDED; THE STALE-KEYED-GUARD CLASS EARNS D39.**

**v1.25 — 2026-08-24 (MINOR: records firing 25; no questions changed). Instance:
`docs/retro-side-lane-2026-08-24-s58.md`, committed in this same action.**

* **FIRINGS: 25.** ~12 flags, consumption effectively total; ship-event certs (v213, v215),
  a slot incident's leak accounting, 4 window certs (w21, w22, w24 + the incident window);
  prevented ~8 / caused 0 / nearly caused 1. Conduct claims ZERO, 18th consecutive.
* **⭐ THE HEADLINE: the degenerate-opposite dial this lane flagged into iteration 12's
  registration FIRED in the w22 verdict and priced the exemption's cost** — the first
  recorded full life-cycle (flag → registration clause → fired dial → verdict sentence).
  The both-branches practice is confirmed at its strongest.
* **⛔ D39 ROUTED (behaviour change → the booted checklist): a version-keyed guard outlives
  its subject silently, then fires on everything.** Two instances inside one hour — the
  builder's v213 slot guard after the v215 ship, and THIS LANE'S own tape monitor with the
  identical stale key, caught in the same sweep before either fired. Every activation now
  sweeps running monitors for keys naming the displaced version.
* **Q3 = 2** (incomplete "corrected pool", peer-caught; ahead-of-check clause, self-caught) —
  both the partial-view family, both corrected same-hour. **Q5 = 0 wrong flags · Q9 = 1.**
* **The v1.24 carry discharges:** byte-diff-or-label exercised for real (v214 certified
  provenance-verified, explicitly not byte-verified); `certifying`-state tags used at
  publication time twice.

**SUNSET WATCH: every surviving question fired. Season end — the next boot, if any, is a new
era's; this instrument's 25-firing series closes with the league.**
