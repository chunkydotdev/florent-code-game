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

## Q6. FAIRNESS — did I characterise another lane's conduct, and was it verified?

**Why:** flags about *work* are cheap to correct; claims about *conduct* land in
a durable record about a colleague. **How:** count conduct claims; for each, was
it verified against the process, or inferred from an artefact?

**s28: one, and it was inferred from a commit timestamp and wrong.** Rule now
standing: **the bar for a conduct claim is what they DID, verified — never what
an artefact permits me to infer.**

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
