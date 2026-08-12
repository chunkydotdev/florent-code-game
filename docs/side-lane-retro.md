# SIDE-LANE RETRO — the instrument. **v1** (2026-08-10)

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
