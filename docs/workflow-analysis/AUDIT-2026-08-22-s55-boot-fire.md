# AUDIT 2026-08-22 — s55 boot fire: can the instruments support the decisions?

**Short-lived audit session, opus, read-only. No stake in the build queue.**
Triggered by `tools/audit_trigger.py` FIRING 2/6 at the builder's s55 boot,
2026-08-22 ~09:50Z. Prior art: `docs/workflow-analysis/` 2026-08-08 (19%-power
finding) and 2026-08-16 (`AUDIT-2026-08-16-instruments-vs-decisions.md`).
Wall clock for every reading below: `date -u` = **2026-08-22T09:54:49Z**;
re-run of the trigger at 09:56Z reproduced the fire with the numerator one
lower (32 → 31) as a doc aged out of the window.

Live reading at audit time:

```
  [  ok] note:verdict ratio   0.00       0 analysis rows / 6 decision rows (last 50)
  [  ok] doc:code churn       0.23       12565 prose / 54268 code   [20h .186 · 24h .233 · 28h .275]
  [TRIP] ship cadence         0.35/hr    8 activations in the last 24h over ~23 active hours
  [  ok] stuck planks         0          0 KEEP-dev mentions in the last 60 tape rows
  [TRIP] cross-lane analysis  31.00      31 new analysis docs / 0 decision rows ADDED
  [  ok] delegation drought   0.00       0 decision blocks / 0 spawn announcements (24h)
```

---

## HEADLINE — and it is not the day-shape question I was asked to settle

**Both tripped cells were diagnosed as broken by the s53 audit session 20.6 hours
before this fire, routed to the wrap-debt list, and carried through a full wrap
cycle unrepaired.** `docs/coordination.md:72231` names them by number — **L1
`results.tsv` SCHEMA FORK** ("broke audit_trigger's decision denominators") and
**L3 audit_trigger delegation cell dead** ("selftests validate against frozen
fixtures, live formats drifted") — plus the ship-cadence gauge, which that
session already characterised as *"a broken gauge either way"* on a 9-of-14-days
trip record. They were routed to WRAP DEBT at `docs/coordination.md:72402` under
Magnus's no-inline-fix rule, appear as successor-queue item 4 at
`HANDOVER.md:123-125` (HIGH), and `git log -- tools/audit_trigger.py` shows
**zero commits since 2026-08-15T20:59** — seven days, and the last one was a
repo-wide `--help` sweep, not a change to any counter.

⇒ **The trigger has now spent a second short-lived audit session on the same
three cells.** That is a cost the audit mechanism imposes on itself: the alarm
that summons an auditor is consuming the audit budget re-deriving known-broken
readings.

**And the second headline is the one the numbers actually settle.** A full
enumeration of the window (delegated, opus, read-only; anchors below) found
**96 distinct decisions**, of which **2 reached `results.tsv` — 2.1%.** One of
those two is schema-forked and the other is uncommitted, so **the tape captured
zero decisions in a machine-readable form in 24 hours.**

⇒ **The `cross-lane analysis` cell's stated meaning is REFUTED and its alarm is
nonetheless correct.** 96 decisions against 31 analysis docs is **3.1 decisions
per document** — analysis is not outpacing decisions, it is trailing them 3:1.
What the cell has actually detected is that **`results.tsv` has been abandoned as
the decision surface.** It reads `31.00` where the honest ratio is `0.32`: a
~97× error, in the alarming direction, on a cell whose threshold is 4.0.

The day-shape caveat I was asked to weigh is **refuted as an explanation** (§A2:
the cell also tripped at T-2, T-3, T-5 and T-7, three of which predate the
SKALMAN founding) — but so is the cell's own diagnosis.

---

## (a) VERDICT ON EACH TRIPPED SIGNAL

### A1 — `ship cadence` 0.35/hr → **INSTRUMENT-BLIND**

The cell cannot answer the question it is asked. Four independent defects, all
measured, three of them new to this audit.

**(i) It counts rollbacks as decisions — a 2× inflation, measured.** The eight
"activations" in the window decompose into **one genuine holder change and three
prototype fire-and-rollback cycles**:

```
2026-08-21T09:59Z  v175 -> v176     genuine holder promotion
2026-08-21T12:30Z  v176 -> v177  \
2026-08-21T14:45Z  v177 -> v176  /  one prototype window (2h15m)
2026-08-21T15:55Z  v176 -> v178  \
2026-08-21T16:00Z  v178 -> v177   >  one 10-minute window = THREE "activations"
2026-08-21T16:05Z  v177 -> v176  /   (v178 held exactly ONE 5-min poll row)
2026-08-22T05:04Z  v176 -> v179  \
2026-08-22T06:04Z  v179 -> v176  /  one prototype window (1h)
```
Holder occupancy over the 288 rows in the window: **v176 246 rows (85.4%), v177
28, v179 12, v178 1, v175 1.** The submit→fire→rollback pattern is the procedure
CLAUDE.md mandates for unrated legs; the cell scores each half of it as a
separate decision. `tools/audit_trigger.py:229` is the transition counter.

**(ii) Its numerator has the wrong SUBJECT — it counts a shared account.** The
side lane established this the previous day: of the 8 transitions in that
window, **2 were ours** (`docs/coordination.md:72450`, "SHARED-ACCOUNT SUBJECT
DISCIPLINE, three surfaces one day"). x3r0 shares the account and holds the slot
by Magnus's ruling (`PROGRAMME.md: X3R0_SLOT_RULE`). The cell divides a
whole-account numerator by an **our-git-log** denominator
(`tools/audit_trigger.py:243-246`). Numbers carry subjects; this ratio has two.

**(iii) NEW — the numerator is a lower bound with a measured miss.** The four
first-contact accepts at **2026-08-22T08:24:06-08Z carry `ourver=180`**
(`docs/coordination.md:72684`). **`elo_history.tsv` contains the string `v180`
zero times in 288 in-window rows** (median poll gap 5.0 min, max 6.0). The
poller sampled at 08:19/08:24/08:29/08:34 and read `v176` at every one. So a
version that the platform's own match records show as ours-at-fire never
appeared on the activation tape at all — either the window was shorter than the
5-minute poll, or `ourver` and `active_bot` do not bind the same way (which is
the **version-binding semantics UNRESOLVED** debt at `HANDOVER.md:132`, the
Torsko row). Either way the cell's numerator is a sampled lower bound presented
as a count.

**(iv) The denominator saturates, so it penalises long days.** `active_hours` is
*distinct clock hours containing ≥1 commit*, bounded at 24. Recomputed over 14
consecutive 24h windows off `elo_history.tsv` and `git log`:

| window | rate | activations / active hours | verdict |
|---|---|---|---|
| T-0 | 0.30 | 7 / 23 | TRIP |
| T-1 | 0.53 | 10 / 19 | ok |
| **T-2** | **2.00** | **14 / 7** | **ok** |
| T-3 | 0.09 | 1 / 11 | TRIP |
| T-4 | 0.32 | 6 / 19 | TRIP |
| T-5 | 0.56 | 10 / 18 | ok |
| T-6 | 0.24 | 4 / 17 | TRIP |
| T-7 | 0.50 | 11 / 22 | ok |
| T-8 | 0.43 | 9 / 21 | TRIP |
| T-9 | 0.31 | 5 / 16 | TRIP |
| T-10 | 0.36 | 5 / 14 | TRIP |
| T-11 | 0.38 | 6 / 16 | TRIP |
| T-12 | 0.30 | 7 / 23 | TRIP |
| T-13 | 0.82 | 18 / 22 | ok |

**TRIPPED 9 of 14.** This independently reproduces the s53 figure digit-for-digit
(`docs/coordination.md:72402`, "the 9-of-14-days trip record"). Note T-2: **14
activations over 7 active hours reads `2.00` and healthy**, while T-0's 7 over 23
reads `0.30` and trips. Today the repo committed **255 commits across 23 distinct
hours, single author** — genuine round-the-clock work, not automation pollution,
so the denominator is honest *for T-0*; but a gauge whose healthiest reading in
two weeks comes from its shortest working day is measuring day length, not
decision output.

**Verdict: INSTRUMENT-BLIND.** A cell that trips on 64% of days, counts a shared
account, doubles every rollback and demonstrably missed an activation in this
very window cannot carry the sentence "decisions per hour has fallen". *I am
deliberately not claiming the underlying question is answered either way* — the
s53 session found that de-polluting the subject drives it to 0.11/hr, i.e.
**deeper** into trip. The honest statement is that **this cell cannot resolve it**
and no other instrument in the repo is aimed at it.

### A2 — `cross-lane analysis` 31.00 → **REAL PROBLEM, reached through an INSTRUMENT-BLIND cell**

The denominator is broken in two independent ways. **Both were repaired for by
correcting them, and the trip survived — which is what makes today different
from the s53 reading.**

**Defect 1 — the schema fork silences the decision counter.**
`results.tsv` forked to an undocumented 9-field form at commit `8b88b67b5`
(2026-08-20T19:34:29+02:00). Seven rows are in it, at **`results.tsv:515-521`**
(`homepool-final`, `homepool-final-addendum`, `v535pool-final`, `v529pool-final`,
`v536pool-final`, `v537pool-final`, `newpool-baseline-anchor`). In the 7-field
header form field 6 is `status`; in the 9-field form field 6 is `ci_low`. So
`tools/audit_trigger.py:372` reads `f[5]` and gets the strings `65.19`, `67.60`,
`71.38`, `70.86`, `74.30`, `50.61`, `-` — **none of which are in `DECISION_KINDS`**
(`tools/audit_trigger.py:317`). Six full-pool **n=5,400 verdicts** were banked on
2026-08-20/21 and the decision counter read **zero**. The builder knows: the
anchor row carries `SCHEMA FLAG: 9-field de-facto form (fork since 8b88b67b5,
repair = wrap debt)` inline.

**Defect 2 — NEW, and larger: `DECISION_KINDS` has not tracked the tape's own
vocabulary.** `tools/auto_gate.py:173-175` states the rule in a box: *"EVERY STOP
WRITES A results.tsv ROW TYPED `cancellation`, NEVER `verdict`"* — established
2026-08-15 by the SEALQ disclosure, because operational cancellation and verdict
are different objects. **`cancellation` is not in `DECISION_KINDS`.** Status
counts over the whole tape (521 rows):

| status | n | in DECISION_KINDS? |
|---|---|---|
| verdict | 89 | yes |
| **cancellation** | **71** | **no** |
| keep | 70 | yes |
| note | 48 | (analysis) |
| discard | 30 | yes |
| **probe** | **29** | **no** |
| baseline | 25 | yes |
| gate | 20 | yes |
| **no-verdict** | **19** | **no** |
| **screen** | **17** | **no** |
| caveat | 15 | (analysis) |
| info | 14 | (analysis) |
| **hold** | **10** | **no** |
| ship / refuted | 8 / 8 | yes |
| **dose / correction** | **8 / 8** | **no** |
| **negative** | **6** | **no** |
| **cert / calibration / inert / frozen / …** | 3/2/2/2/… | **no** |

**In the last 50 tape rows: 28 `cancellation`, 6 `verdict`, 4 `negative`, 3
`correction`, 2 `calibration`, 7 schema-forked.** The two decision counters
recognise **6 of 50 rows (12%)**. The single most common row type on the recent
tape — written by an automated tool, on a rule adopted seven days ago — is scored
as a non-decision. This is a decision-vocabulary drift the instrument never
tracked, and it is *not* on the s53 defect list; it is new here.

**Defect 3 — uncommitted rows are structurally invisible.** The newest tape row,
`v543pool-autostop-1000` (typed `cancellation`), is **in the working tree
uncommitted** as of this audit — written by `auto_gate.py --apply` at
2026-08-21T15:15:38Z, ~18.7 hours ago. `tools/auto_gate.py` writes the row and
does not commit it; both counters read `git log`
(`tools/audit_trigger.py:363-365`), so an uncommitted decision can never count.
(This also breaches the standing "push every commit immediately" practice.)

**NOW THE CORRECTION, and it is why this cell reads REAL PROBLEM.** Recomputed
across ten consecutive 24h windows, with the strict counter beside a
schema-and-vocabulary-agnostic *net rows added* count:

| window | analysis docs | dec_rows (strict, as shipped) | net tape rows added (any kind) | ratio as shipped |
|---|---|---|---|---|
| **T-1 (this fire)** | **31** | **0** | **1** | **31.00 TRIP** |
| T-2 | 17 | 0 | 6 | 17.00 TRIP |
| T-3 | 13 | 1 | 1 | 13.00 TRIP |
| T-4 | 7 | 2 | 2 | 3.50 ok |
| T-5 | 32 | 3 | 21 | 10.67 TRIP |
| T-6 | 23 | 20 | 77 | 1.15 ok |
| T-7 | 24 | 2 | 12 | 12.00 TRIP |
| T-8 | 59 | 29 | 54 | 2.03 ok |
| T-9 | 18 | 8 | 9 | 2.25 ok |
| T-10 | 5 | 6 | 6 | 0.83 ok |

**The T-2 row is the schema fork caught in the act: six substantive n=5,400
verdicts banked, strict counter zero.** But **T-1 is not that case.** In the last
24 hours `results.tsv` was touched by **exactly one commit** (`a97a365c6`,
2026-08-21T15:48:02+02:00, adding the 9-field `newpool-baseline-anchor` row) plus
one uncommitted `cancellation`. Under **every** reading I can construct:

* as shipped: 31 / 0 → **31.00**
* schema-corrected (count the 9-field row): 31 / 1 → **31.00**
* schema + vocabulary + uncommitted corrected: 31 / 2 → **15.50**
* …and excluding the 11 `BUILD-REPORT-*` files from the numerator (they are the
  record of *building*, not analysis): 20 / 2 → **10.00**

**Every one clears the 4.0 threshold.** Compare s53, where the same correction
took the cell from 15/0 to 8/4 = 2.0 = `ok` (`docs/coordination.md:72231`). **The
correction rescued that fire and does not rescue this one.**

**Defect 4 — and it inverts the cell's meaning.** The numerator counts *any*
`.md` added under `docs/` outside `MANDATED_PROSE`. **25 of the 31 carry
disposition language** (VERDICT / REFUS / DEFER / WITHDRAWN / PROMOTED / ROUTE:).
The `*-READ-*` and `DECODE-*` docs **are the readout documents** —
`docs/research/POWERED-READ-v614-2026-08-22.md:11-16` is a gate-cleared n=900/arm
table with CIs and dispositions; `docs/research/TRANSFER-READ-v612-mjolnir-2026-08-22.md`
carries the transfer verdict. ⇒ **A decision that is fully written up increments
the numerator by 1 and the denominator by 0 — it makes the "analysis is
outpacing decisions" alarm LOUDER.** The cell's own remedy (excluding
`MANDATED_PROSE` and retros, `tools/audit_trigger.py:307-310`) was built for
exactly this class and stops one file short of the readout documents.

**Verdict: REAL PROBLEM — MISDIAGNOSED BY THE CELL THAT FOUND IT.** The
condition is genuine, persistent (5 of the last 7 daily windows), and *not*
what the cell's `why` string says. See §A3 for the number that settles it.
**The caveat I was asked to weigh — "a founding day legitimately produces many
analysis docs" — is REFUTED as an explanation: the cell also tripped at T-2,
T-3, T-5 and T-7, and T-3/T-5/T-7 predate the SKALMAN founding.** The founding
day made a three-day-old condition worse; it did not create it.

### A3 — the day-shape question, settled: 96 decisions, 2 on the tape

A full enumeration of `docs/coordination.md`, `HANDOVER.md` and `git log` across
the window (delegated read, opus, read-only; per-decision anchors in that agent's
table, spot-checked by me below) found **96 distinct decisions** — dispositions
that changed what the project does next. **The window is the opposite of
decision-poor.** It contains a ship and a rollback, five Magnus rulings, a line
founding, a queue re-scope of 140 rows, 21 bot-tree verdicts (v600→v621), a
completed 15-cell first-contact campaign, and a full wrap batch.

**Machine-readable capture: 2 of 96 = 2.1%.**

| decision | `results.tsv` row | status field |
|---|---|---|
| NEWPOOL-BASELINE anchor readout | `results.tsv:521` | **9-field row — field 6 is `50.61`, a CI-lower, not a status** |
| V543POOL trend-floor stop | `results.tsv:522` | `cancellation` — **UNCOMMITTED, working tree only, ~18.7h** |

⇒ **Both of the two are invisible to the counters anyway** (one by schema, one by
vocabulary-and-git-window). **The machine-readable capture of the window is
effectively ZERO, and that is not a counting artefact — it is the tape.**

Verified by me directly, not delegated:
`grep -ci skalman results.tsv` → **0**; `grep -ciE 'doorwave|kladdedose'` → **0**;
`grep -cE 'v6[0-2][0-9]'` → **0**. Twenty-one bot trees, a 20/20-fired locked leg,
and a four-version verdict cascade left **no row**.

**The one surface that worked is `PROGRAMME.md`** — 8 commits in the window
(verified: `git log --since=24.hours -- PROGRAMME.md | wc -l` = 8), carrying 7
distinct decisions into parsed fields (`INCUMBENT`, `SHIP_BAR`, `NEXT_LINE`,
`STEALTH_PREDROP_RIDER`, `NEXT_LINE_SCREEN_LADDER`, `NEXT_LINE_EXPERIMENTS`).
**But all 7 are Magnus rulings or line declarations. No experimental verdict of
any kind reached a parsed field.** The repo has a working machine-readable
decision surface for *directives* and none for *findings*.

**And the brief's hypothesis is confirmed with a number.** Of the 96:

* **25 pure refusals or deferrals** + **3 mixed** = **28 (29%)** carry a
  refusal-or-deferral component.
* **13 of the 15 refusals are a lane withdrawing or amending its OWN previously
  banked claim** — one of them (`coordination.md:72728`) withdrew a finding
  banked **nine minutes earlier**.
* **Zero of the 28 appear on `results.tsv`.**

The tape's tail vocabulary is `verdict` / `keep` / `cancellation` / `correction`.
The era's modal non-affirmative dispositions — *"MECHANISM CONFIRMED AT NIL DOSE,
UNRESOLVED as a plank"* (`coordination.md:72646`), *"REFUSED as inseparable from
control-choice noise"* (`:72713`), *"verdict sentences are this lane's when it
lands"* (`:72706`) — **have no row type, and the three that exist (`no-verdict`
19, `hold` 10, `inert` 2) are scored as non-decisions by both counters.**

⇒ **The 0-decision-rows signal IS structurally blind to the modal verdict type of
the current era, exactly as the commissioning brief suspected — AND the surface
is genuinely unwritten.** Both halves are true, and they compound: the lanes
stopped writing to a tape that would not have recorded most of what they decided.

### A4 — TWO CELLS THAT READ `ok` AND SHOULD NOT BE TRUSTED

**`delegation drought` 0.00 → INSTRUMENT-BLIND, reading healthy.** It reported
**0 decision blocks / 0 spawn announcements**. The last 2,500 lines of
`docs/coordination.md` (a 72,826-line file) contain **11** headers matching its
`^\s*#.*ISO-8601Z` pattern, spanning 2026-08-17 to 2026-08-22; **7 fall inside
the 24h window** (`docs/coordination.md` tail lines 1817, 1849, 2079, 2081, 2110,
2424, 2454 of the tail slice). It matched **none** of them on either regex. The
cause is measurable: its window is `lines[i:i+3]` (`tools/audit_trigger.py:426`)
and this repo's wrap headers wrap across 4-6 lines — the s53 wrap block's
**"NINE fresh-opus agents commissioned, nine completed, nine banked"** sits at
header+4 and is invisible to the spawn regex. It also reads only the file's tail
slice, while the builder's in-session decision blocks use a `--- ISO ⭐⭐` prefix
rather than `#` and match neither pattern.

**`0/0` evaluates to `0.00` and prints `ok`.** This is precisely the defect the
module's own `main()` was hardened against at `tools/audit_trigger.py:565-573`
(*"A CELL THAT COULD NOT EVALUATE IS UNKNOWN, NOT NOT-TRIPPED"*) — the guard
catches **exceptions** and does not catch **a cell that found nothing to
measure**. This is L3 from the s53 audit, still live, and it means the fire
today was 2/6 when a functioning delegation cell would have made it 2/5-that-ran
plus one BLIND.

**`note:verdict ratio` 0.00 → reads correctly today, but on 12% of the data.**
Same `DECISION_KINDS` and same schema fork (`tools/audit_trigger.py:83-91`):
6 of the last 50 rows are classified at all. Analysis genuinely was 0
(`note`/`caveat`/`info` all zero in the tail), so the `ok` is not wrong — but the
cell has ~1/8 of its intended visibility and would not notice the condition it
exists to catch.

---

## (b) INSTRUMENT-vs-DECISION MISMATCHES THE LANES SHOULD FIX

Ordered by how much a wrong reading costs, with anchors. **These are instrument
repairs, not queue items — I have no stake in and make no claim about the build
queue.**

**M0 — THE BINDING ONE: `results.tsv` captured 2 of 96 decisions (2.1%), and
both of those are unreadable by the counters.** §A3. This is not an instrument
bug — it is a surface that the lanes have stopped writing to, while continuing
to make ~96 decisions a day. **Every counter repair below is worth less than
this one**, because a perfectly-tuned counter over an empty tape still reads
zero. Two sub-parts, and they need different fixes:
* **the tape has no row type for a refusal or a deferral** — 28 of 96 decisions
  (29%) carry one, and the era's modal dispositions (nil-dose refusal, refused-
  as-inseparable, verdict-withheld-pending-decode) have nowhere to land; and
* **`PROGRAMME.md` demonstrates the working pattern** — 8 commits, 7 decisions
  into parsed fields, in the same window. It captures *directives* and no
  *findings*. Whatever makes that surface get written could be extended.

**M1 — `DECISION_KINDS` does not contain `cancellation`, which an automated tool
writes as the tape's second-most-common row type.**
`tools/audit_trigger.py:317` vs `tools/auto_gate.py:173-175`. 71 rows all-time,
28 of the last 50. Also missing: `screen` (17), `no-verdict` (19), `hold` (10),
`negative` (6), `correction` (8), `cert` (3), `inert`/`frozen` (2/2). **The
repair is not "add words" — it is to decide which of these ARE dispositions and
make the tape and the counter agree**, because `no-verdict` and `inert` are
arguably the era's modal decision and `probe` (29) arguably is not.

**M2 — `results.tsv` schema fork, rows 515-521, silencing both decision
counters.** `results.tsv:515-521` (9 fields) vs the 7-field header at
`results.tsv:1`; consumer at `tools/audit_trigger.py:372` and `:83-91`.
Already HIGH wrap debt at `HANDOVER.md:124`; **this audit adds that the cost is
not cosmetic — it zeroed the decision denominator on the day six n=5,400
verdicts landed (§A2, T-2).** Note `tools/auto_gate.py:1620` asserts `len(f)==7`,
so the schema fork is also un-asserted debt inside a second tool.

**M3 — `delegation drought` reads `0/0` as healthy.**
`tools/audit_trigger.py:426` (3-line window vs 4-6-line wrapped headers),
`:409` (tail-2500 slice), `:431` (`decisions/(spawns+1)` → 0 when both are 0).
**A cell that matched 0 of 7 in-window headers on both regexes must report
BLIND, not `ok`.** The `main()` blind-handling at `:565-594` already has the
right vocabulary; the cell needs to raise or return a sentinel rather than a
number.

**M4 — the cross-lane numerator counts readout documents as analysis.**
`tools/audit_trigger.py:307-310`. 25 of the 31 in-window docs carry disposition
language; 11 are `BUILD-REPORT-*`. **Publishing a decision currently makes the
"no decisions" alarm louder.** Simplest honest repair: either exclude
`BUILD-REPORT-*`/`*-READ-*`/`DECODE-*` from the numerator, or count a readout
document as a decision on the denominator — but **not neither**, which is the
current state.

**M5 — `ship_cadence` conflates ship, fire and rollback, and mixes subjects.**
`tools/audit_trigger.py:229` (transition count), `:243-246` (our-git-log
denominator against a shared-account numerator). Plus the new §A1(iii) finding:
`ourver=180` at `docs/coordination.md:72684` against **0 occurrences of `v180` in
288 in-window `elo_history.tsv` rows**. A 5-minute poller cannot count
sub-5-minute activation windows, and the fire→rollback procedure produces them
by design.

**M6 — `auto_gate.py` writes decision rows it does not commit.** The
`v543pool-autostop-1000` row has been uncommitted ~18.7h. Any git-windowed
consumer is blind to it, and it breaches "push every commit immediately".

**M7 — the s54-era instruments carrying this week's headline corrections live in
`scratchpad/` without controls, while the mature `tools/` instruments are
properly driven.** (Delegated read; anchors below are the sub-agent's, spot-check
before acting.)
* **Verdict-bearing decision queued on an instrument that does not exist:** the
  **KILL_TARGET re-anchor proposal to Magnus** and the first-contact cell
  verdicts both wait on `docs/research/DECODE-firstcontact-v180-2026-08-22.md`
  (`HANDOVER.md:42-44`, `docs/coordination.md:72640`) — **no such file**. The
  decoder `scratchpad/s54_fc_decode.py` (324 lines) ran clean on 65 games
  (65/65 on `turns_ok`/`cond_ok`/`won_ok`) but has **no selftest, no mutant, no
  negative control** — a 65/65 pass that has never come out the other way is a
  constant column by this repo's own standing rule.
* **A practice adopted repo-wide with no tool behind it:** CLAUDE.md now requires
  every powered grid to carry a duplicate control and every cut over a
  deterministic opponent to state whether it checked for content duplicates.
  **Content-level fingerprinting exists nowhere in `tools/`** (QUEUE.md:723,
  issue #117, open); the duplicate-control arm is a manual convention
  (`grep -n 'duplicate' scratchpad/s54_v620/*.py` → zero hits); and
  `scratchpad/s54_v620/pool.py:15-18` + `powered.py:4-14` — **the scripts that
  will run the next powered grid — still enumerate two clusters and still quote
  DEFF 0.98 "naive intervals stand"**, the exact enumeration
  `scratchpad/s54_v620/mapdeff.py:2-8` was written to supersede. **A reader who
  follows CLAUDE.md's four-cluster procedure and then runs `pool.py` gets the old
  answer.** Logged as unbuilt debt at `scratchpad/s54_wrap_debts.md` item 11.
* **`mapdeff.py` has only ever reported 4.57.** No homogeneous-arms control, so
  the DEFF estimator behind the ×2.14 interval inflation **has never been seen to
  return ≈1.0**. Same class: `scratchpad/s54_v620/cmp_tape.py`'s docstring
  instructs the *operator* to drive it both ways rather than doing so in code —
  and records a false-negative it already suffered.
* **The tape30 byte-identical pair detector does not exist as banked code.** The
  finding sits at `scratchpad/s54_autopsy/tape30_autopsy.md:54-70`; **no file
  implements the pairwise comparison.** That matters because the amendment at
  `docs/research/FIDELITY-BASELINE-v600-2026-08-21.md:3-17` **retroactively halved
  n on a published baseline** — a verdict-bearing correction whose instrument is
  not reproducible.
* **Cosmetic but the named class:** `tools/skalman_fidelity.py:53,61,73`
  documents `--selftest` three times; argparse does not implement it (the drive
  lives in `tools/skalman_fidelity_selftest.py`). *"A fact recorded in a
  reference and contradicted by the thing itself."*

---

## (c) CLEAN BILLS — surfaces I looked at and did NOT find wrong

A clean bill is information, so these are stated with what was checked.

1. **`tools/audit_trigger.py --selftest` PASSES 6/6, both directions.** All six
   rows fire on a corrupted input, and both `_MUST_STILL_TRIP` quiet-direction
   fixtures pass (the whole-file-rewrite case and the prose-'agent' case). **The
   selftest is not the problem — and that is itself the lesson: every defect in
   §A/§B is a LIVE-FORMAT drift that a frozen fixture cannot see.** This is
   exactly the s53 L3 wording ("selftests validate against frozen fixtures, live
   formats drifted") and it generalises past the delegation cell to `DECISION_KINDS`
   and the schema fork.
2. **`doc:code churn` is healthy and its stability rule is working.** 0.186 /
   0.233 / 0.275 at 20h/24h/28h — consistently and comfortably below 1.0, no
   window-phase sensitivity. The s30 re-spec (three-window agreement +
   `MANDATED_PROSE` exclusion) is doing its job; 12,565 prose vs 54,268 code
   lines over 255 commits.
3. **`stuck planks` = 0.** No plank parked in KEEP-dev in the last 60 rows. Clean.
4. **The activation tape is FRESH, not stale.** Newest `elo_history.tsv` row
   2026-08-22T09:55Z against a wall clock of 09:56Z; 288 rows in the window,
   median poll gap 5.0 min, max 6.0. The failure in §A1(iii) is a **sampling
   resolution** limit, not a stalled monitor — the repo's own "a monitor that
   reads a file must report freshness" hazard is NOT present here.
5. **The commit denominator is honest work, not automation.** 255 commits, 23
   distinct hours, **single author** — I checked specifically for round-the-clock
   bot commits inflating `active_hours` and found none.
6. **The `results.tsv` prose is not corrupted.** One historical 13-field row
   (`results.tsv:236`, `tle-headroom`) from the known tab-mangling incident,
   already caught by readback at the time; 513 of 521 rows are clean 7-field. The
   fork is a deliberate undocumented extension, not damage.
7. **The mature `tools/` selftest culture is real and I could not fault it.**
   ~70 of 103 `tools/*.py` expose a runnable selftest. `tools/cluster_ci.py` ships
   a deliberate mutant (`:204-205`) whose injection flips the verdict (interval
   0.3000 → 0.1300, 57% collapse) and carries a documented fix for a near-miss
   where the mutant was bound at def-time and monkeypatching would not have been
   seen — **a selftest that was itself audited.** `tools/skalman_fidelity_selftest.py`
   passes 20 metrics + 5 structural guards with a wrong-side column that breaks
   the band on 11 of 20 metrics and a conveyor-stripped negative control that
   names its own failure mode. **The gap in §M7 is generational — `scratchpad/`
   vs `tools/` — not cultural.**
8. **The s53 audit's own claims held up under re-derivation.** I recomputed the
   9-of-14-days ship-cadence trip record independently and reproduced it exactly,
   and confirmed the schema fork's row range and originating commit. **This audit
   found no error in the previous audit** — only that its findings were not acted
   on.
9. **`PROGRAMME.md` is a HEALTHY machine-readable decision surface** and is the
   counter-example that makes M0 actionable rather than despairing: 8 commits and
   7 decisions into parsed fields in the same 24 hours, `tools/gate.py` reading
   it, and the "edit only on an explicit Magnus directive" rule holding. Its gap
   is scope (directives yes, findings no), not health.
10. **The lanes are NOT failing to decide, and I checked specifically for that**
   because it is the failure mode the trigger names. 96 decisions, 21 bot-tree
   verdicts, a completed campaign, five rulings encoded within minutes of being
   given, and a refusal culture strong enough that **13 of 15 refusals are a lane
   withdrawing its own claim** — one nine minutes after banking it. **On the
   question the audit was commissioned to ask, the decision-making is in better
   shape than its instruments are.**

**What I looked for and did not find:** a power defect of the 2026-08-08 class
(the batteries in this window are n=900/arm and n=5,400, and `cluster_ci.py`
enforces the enumeration); a stale-tape blindness in the monitors; a fabricated
or constant column in the tripped cells' inputs; and any sign that the trigger's
thresholds themselves have drifted (they have not been touched since 2026-08-13).

---

## PROVENANCE / LIMITS

* Every number is from the working tree at 2026-08-22T09:54-10:0xZ. Recomputations
  ran on `.venv/bin/python` against `results.tsv`, `elo_history.tsv` and `git log`
  in this repo; the 14-window and 10-window tables are my own code, not the
  trigger's output, and import `tools/audit_trigger.py`'s own `DECISION_KINDS` and
  `MANDATED_PROSE` so they cannot drift from it.
* **All game-related figures quoted are LOCAL-fixture or platform-record reads
  made by other sessions and are cited, not re-derived.** This audit measured the
  *process surfaces*, not the bot.
* §A3 and §M7 are delegated reads (two opus sub-agents, read-only). **§A3's
  load-bearing claims were spot-checked by me against primaries** — the three
  zero-greps, the 8 `PROGRAMME.md` commits, the two tape rows' field structure
  and the uncommitted status all reproduce. The **96** and the **28 (29%)** are
  the agent's enumeration and classification; the *count* is a careful read of a
  72,826-line file, not a mechanised extraction, so treat it as ±a few rather
  than exact. **Nothing in this report's verdicts turns on the exact figure** —
  the finding is 2-of-~100, not 2-of-exactly-96. §M7's anchors are the agent's
  and should be spot-checked before acting on them.
* **Not committed, per the commissioning brief.** Left for the builder to review.

## TWO RECOMMENDATIONS

**R1 — the decision surface, not the counters (M0).** The lanes are making ~96
decisions a day and recording 2 of them somewhere a tool can read. **Repairing
`DECISION_KINDS` and the schema fork without fixing that would produce a
well-calibrated instrument pointed at an empty tape** — and would arguably make
things worse, because the cell would then read `ok` while capture stayed at 2%.
The two concrete sub-problems are stated in M0: the tape has no row type for the
29% of decisions that are refusals or deferrals, and `PROGRAMME.md` shows in the
same window what a surface that *does* get written looks like. **I make no
recommendation about which fix — that is a lane call, and I have no stake in it.**

**R2 — a broken cell in the trigger is not ordinary wrap debt.** The three cells
were correctly diagnosed on 2026-08-21, correctly routed under Magnus's
no-inline-fix rule, and correctly carried into the successor queue — and the
process still produced a second audit session on the same defects 20.6 hours
later. **This is debt that spends the audit budget.** Either the trigger's own
repairs get an exemption from the no-inline-fix rule, or a cell a prior audit has
named as broken should be **muted with its finding printed inline** until
repaired, so the next fire is carried by cells that still measure something. As
shipped, a known-broken cell keeps voting — and today two of them outvoted the
four that work.
