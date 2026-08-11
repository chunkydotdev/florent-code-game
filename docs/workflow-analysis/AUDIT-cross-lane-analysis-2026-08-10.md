# AUDIT — cross-lane analysis: can the instruments support the decisions?

**Written 2026-08-10 15:18:43 CEST** (`date`, this shell call). **HEAD at audit time: `b5266ee`** (2026-08-10 15:17:54 +0200).

Short-lived audit session, spawned by `tools/audit_trigger.py` firing 2/5.
**Subject: the `cross-lane analysis` signal only — 14.43 = 303 new analysis docs / 21 decision rows.**
No stake in the build queue. Read-only: no bot edits, no batteries, no matches, no HANDOVER/PROGRAMME edits.

Prior art this is modelled on: `docs/workflow-analysis/v1-2026-08-08-measurement-power.md` (n=120 battery, 19% power).

---

## BOTTOM LINE

1. **The `cross-lane analysis` row is arithmetically broken and its 14.43 is not
   evidence of anything.** Its numerator is a 24-hour window; its denominator is
   a 50-row slice of `results.tsv` that spans **~42 hours** and gained **exactly
   one row** in the measured window. 49 of the 50 denominator rows predate the
   numerator window entirely. Worse, the decision records the project now writes
   — preregs and RESULT docs — **live in the numerator**: 25 of the 303 "analysis
   docs" are decision records. Every decision the project makes now increments
   the top of the fraction and never the bottom. **This row cannot return `ok`
   under the current recording convention, whatever the project does.**

2. **But there IS a real signal next to it, and the trigger missed it by
   averaging.** 217 of the 303 docs are one production line —
   `docs/research/tactics/`, the external-literature sweeps. Its citation rate
   into anything that produced a decision is **4/217 = 1.8%**. Everything else
   the project wrote in the same 24 hours cites at **69/86 = 80.2%**. The
   defect is not "analysis is outpacing decisions"; it is **one lane with a
   1.8% conversion rate and 23,658 lines of output in a day. Zero of the 13
   pre-registered planks cite it.**

3. **Analysis is being redone: four confirmed clusters, 9,134 lines, later docs
   not citing earlier ones.** The worst is the panel-selection cluster, where
   the 08-10 rebuild names "THE SELECTION TRAP" without noticing the 08-09
   fixture fell into it first. The repo diagnosed this exact failure on
   2026-08-09 (`PROGRAMME-drift-watch:35`, "D14"), specced the fix
   (`SCRIPTABLE-OPS-AUDIT:20`, `xcite.py`), marked it *"unbounded (not done)"*,
   and then produced four more redo clusters.

4. **The actual bottleneck is neither analysis volume nor decision rate. It is
   LEG RESOLUTION, and it is quantified below: the confirmatory test that came
   back p=0.303 had ~20% power against the effect it was built to confirm.**
   That is the same number, and the same failure, as the 2026-08-08 prior art —
   two days later, on a different instrument, found the same way.

---

## 1. CITATION RATIO — 73/303 = 24.1%, and the average hides everything

**Method** (checkable). Numerator set = `git log --since=24.hours
--diff-filter=A --name-only` filtered to `docs/**.md` → 303 files (matches the
trigger exactly). For each file, substring-search its basename and full path
across a **decision surface** defined before looking at results:

* `HANDOVER.md`, `PROGRAMME.md`, `CLAUDE.md`, `results.tsv`,
  `docs/coordination.md`, `docs/research-queue.md`, `docs/ship-gate.md`,
  `docs/strategy-log.md`, `docs/open-questions.md`
* every `docs/prereg/*.md`, `docs/PREREG*.md`, `docs/RESULT*.md`,
  `docs/research/RESULT-*.md`, `docs/research/PREREG*.md`, `docs/legs/*.md`
* every `.py`/`.md`/`.txt` under `bots/` and `tools/`
* the commit message of any 24h commit that touched `bots/`

A file counts as CITED if it is named in any of those. Script kept at
`scratchpad/cite.py`; raw per-file result at `scratchpad/cites.json`.

| population | cited | rate |
|---|---|---|
| **all 303** | 73 | **24.1%** |
| `docs/research/tactics/` (217) | **4** | **1.8%** |
| everything else (86) | 69 | **80.2%** |

**The four cited tactics files, and what cites them** — all four are cited by
`docs/coordination.md` and by nothing else. No tactics file is cited by any
prereg, any RESULT doc, `HANDOVER.md`, `PROGRAMME.md`, `results.tsv`, or any
commit that changed bot code:

* `docs/research/tactics/2026-08-09-sweep-15.md`
* `docs/research/tactics/copying-the-top-tier-is-not-free.md`
* `docs/research/tactics/optimise-the-win-condition-action-itself.md`
* `docs/research/tactics/the-defenders-reserve-and-what-defeats-it.md`

### The largest uncited cluster, sized

`docs/research/tactics/` is **252 files / 2.3 MB total, and it did not exist
three days ago** — `git log --diff-filter=A` on that directory returns
**181 files added 2026-08-09 and 71 added 2026-08-10, and nothing before.**
217 of them fall in the 24h window, and their filesystem mtimes confirm they
were genuinely *authored* in the window (10 files in the 08-09T15 hour, 45 in
the 08-09T22 hour, 26 in the 08-10T06 hour, and so on) — this is not a bulk
import of old work being miscounted by git.

Prose volume added in the 24h window, by area (`git log --numstat`):

| area | lines added |
|---|---|
| `docs/research/tactics` | **23,658** |
| `docs/research` (rest) | 18,876 |
| `docs/coordination.md` | 11,149 |
| `docs/archive` | 2,106 |
| `docs/prereg` | 1,587 |
| `HANDOVER.md` | 645 |
| `docs/workflow-analysis` | 367 |

**40% of the day's prose is the lane with a 1.8% citation rate.**

### And the provenance runs the other way too: 0 of 13 preregs

A second subagent (sonnet) traced provenance in both directions; I re-ran its
load-bearing greps. **Every one of the 13 preregs in `docs/prereg/` was read,
and none cites any tactics file, `tactics/INDEX.md`, or any sweep.** Verified:
`grep -licE 'research/tactics|tactics/INDEX|sweep-[0-9]' docs/prereg/*.md` → **0**.
Their stated origins are, without exception, one of: a direct read of the live
bot's own code (LOKI-9 facing → `main.py:529-579`; LOKI-10 → `_v124loki8/main.py:556-566`),
engine-binary disassembly (LOKI-14 → `engine-source-crash-and-launcher-2026-08-10.md`),
a research corpus cut (LOKI-10 → `binding-tile-cut-2026-08-10.md`), a prior
leg's own measured result, or a Magnus directive.

Searching all 252 basenames across 1,342 text files (excluding `.venv`, `.git`,
`replay_archive/`, and >1MB corpus data), **21 of 252 = 8.3% appear anywhere
outside the tactics directory** — the looser test, and it agrees with the 1.8%
decision-surface figure. **None appears in `bots/`, `tools/`, `PROGRAMME.md`,
`CLAUDE.md`, or `HANDOVER.md`.** Of the 21, **12 are referenced only by
`docs/research/D12-closure-sweep-2026-08-10.md`, which is an audit that flags
them for asserting closures with no cited evidence** — being referenced there
means being caught, not being used. Two more are cited by
`AUDIT-the-six-refuted-roads-2026-08-10.md`, one of them as *a stale figure the
INDEX had already corrected and the tactic file never received.*

`tactics/INDEX.md` has a status column (`INDEX.md:199`, the "wheel"), but its
values are **`SWEPT` / `RE-AIMED` / `HELD`** — sweep completion, not
consumption. There is no `actioned` / `queued` / `dead` state anywhere, and no
field linking a tactic to a plank. **In fairness, two wheel rows do claim a
produced artefact** (row 1 → `heal-arithmetic-2026-08-09.md`; row 7 → a probe
that found a latent buffered-store bug), so the yield is not literally zero —
but both outputs are further research docs, not planks, and neither reaches a
prereg.

**The library's traceable effect on the repo is reflexive: it is audited,
cross-referenced by other research docs, and used to correct its own prior
claims. It has not been cited as the origin of a build decision.**

### The second uncited cluster: re-derivation docs

13 of the 58 non-tactics `docs/research/` files added in the window are cited by
nothing. Named, because the pattern in them is consistent:

```
docs/research/AUDIT-baseline-read-2026-08-10.md
docs/research/BOOT-LOAD-AUDIT-2026-08-10.md
docs/research/D12-closure-sweep-2026-08-10.md
docs/research/EXPERIMENT-REGISTER-BACKFILL-2026-08-10.md
docs/research/RESULT-loki11-rush-reopen-2026-08-10.md
docs/research/SCRIPTABLE-OPS-AUDIT-2026-08-10.md
docs/research/crash-census-2026-08-10.md
docs/research/enemy-launcher-asymmetry-2026-08-09.md
docs/research/league-elo-refresh-2026-08-09.md
docs/research/plant-distance-from-source-2026-08-10.md
docs/research/prior-tracing-2026-08-10.md
docs/research/standing-context-rederived-2026-08-10.md
docs/research/unrated-fixture-hard-teams-2026-08-09.md
```

**28 of the 86 non-tactics docs (32.6%) contain an explicit self-disclaimer that
they will not change anything.** Grep pattern, so this is reproducible:
`read-only | not (mine|ours|this lane's) to (execute|fix|change) | no verdict |
verdicts are the builder | nothing (here|in this document) (edits|retracts|
changes) | trace and classify only | measure-and-report`. Verbatim examples:

* `standing-context-rederived-2026-08-10.md:6` — *"Measure-and-report only —
  **nothing here edits or retracts any other document.**"*
* `prior-tracing-2026-08-10.md:5` — *"Trace and classify only — nothing in this
  document edits or retracts any other document."*
* `AUDIT-baseline-read-2026-08-10.md:3` — *"**No verdicts here** — verdicts are
  the builder's."*
* `BOOT-LOAD-AUDIT-2026-08-10.md:5` — *"the cuts themselves are
  builder/command-file/HANDOVER edits and are **NOT this lane's to execute**"*

This is the mechanism by which uncited analysis accumulates, and it is a
**protocol consequence, not laziness**: `docs/two-session-protocol.md` correctly
forbids the research and side lanes from writing verdicts. The protocol has no
matching obligation on the receiving end — nothing requires the builder to
either action or explicitly kill a lane's finding, so a correct hand-off and a
dropped one look identical in the repo.

---

## 2. IS ANALYSIS BEING REDONE? — YES. Four confirmed clusters, 9,134 lines.

Delegated to a subagent (opus) which read the H1 + lead paragraph of all 180
`docs/research/*.md`, 13 `docs/prereg/*.md`, 7 `docs/workflow-analysis/*.md`,
22 `docs/*.md`, 2 `docs/legs/*.md` — tactics/ excluded — then built a basename
citation matrix. **I re-ran its load-bearing greps myself; all passed.** A
cluster counts as a REDO only if ≥3 docs answer one question across ≥2 dates
**and the later docs do not cite the earlier ones.**

### Cluster 1 — "Which opponents belong on the test panel, and what is our baseline?" — 1,627 lines

`unrated-fixture-hard-teams-2026-08-09.md` (73) → `unrated-campaign-plan-2026-08-09.md`
(93) → `v92-unrated-baseline-audit-2026-08-09.md` (176) →
`ouroboros-baseline-drift-and-unrated-legs-2026-08-09.md` (173) →
`per-opponent-gates-v102-2026-08-09.md` (437) →
`PREREG-live-unrated-baseline-2026-08-10.md` (160) →
`LOCK-CERT-live-unrated-baseline-2026-08-10.md` (153) →
`AUDIT-baseline-read-2026-08-10.md` (186) →
`PREREG-pinned-testbed-control-2026-08-10.md` (95) →
`PREREG-panel2-calibration-2026-08-10.md` (81).

The last five cite each other. **None of them cites any of the first five.**
Verified: `grep -ciE 'per-opponent-gates|gateable|unrated-fixture|hard-team|Powerpuff|Lunds'
docs/prereg/PREREG-panel2-calibration-2026-08-10.md` → **0**.
`unrated-fixture-hard-teams-2026-08-09.md` is cited by nothing in the repo.

**And this is the cluster that matters most, because the redo repeated the
original's error.** The 08-09 panel (Ouroboros / Lunds / KCM / CtrlAltDefeat /
Powerpuff) was selected as *"the five teams that beat us"*, explicitly targeting
cells where *"our baseline on these maps is ~0%"* — **a floor-selected fixture.**
The 08-10 panel was selected on rating proximity.
`PREREG-panel2-calibration-2026-08-10.md` then names **"THE SELECTION TRAP …
Selecting a fixture from a pooled-era number builds an instrument that cannot
move"** — without noticing that the previous day's fixture was selected on
0%-cells, which is the same defect. Likewise `per-opponent-gates-v102-2026-08-09.md`
headlines *"Zero cells are gateable. Not one."* and panel-2 headlines *"Three of
five cells are inert."* Same question, same class of answer, one day apart,
zero citation in either direction. **This is finding 3c arriving twice and being
learned neither time.**

### Cluster 2 — "How do the league's fast killers kill a core early?" — 2,581 lines

`kill-timing-doctrine-2026-08-09` (187), `kill-hazard-timing-2026-08-09` (140),
`top-tier-hazard-2026-08-09` (112), `early-kill-arsenal-2026-08-09` (144),
`core-kill-incidence-cut-2026-08-09` (620), then on 08-10
`league-fast-kill-mechanism` (399), `bisons-fast-kill-autopsy` (337),
`plant-distance-from-source` (145), `bisons-fast-kill` (497).

The four 08-10 docs contain **zero** references to the first four 08-09 docs.
The two Bisons docs are 6 and 9 minutes apart on the same object and neither
names the other. **The answers disagree on the load-bearing number:**
`early-kill-arsenal-2026-08-09` tabulates enemy sentinel plant distance at
d²=18/25/26/2 (a spread of 2→26); `league-fast-kill-mechanism-2026-08-10`
shipped the headline *"we plant at the edge, they plant inside range"*, which
`bisons-fast-kill-autopsy-2026-08-10` then **inverted the same morning**
(*"They stand further away than we do, not closer"*), and
`plant-distance-from-source-2026-08-10` voided the comparison entirely (our
forward emplacement is sentinel-only, `raid.py:389`; the d²=32 figure is the
range boundary reproducing itself via first-legal-site-wins, `raid.py:425-445`).
**The 08-09 doc that would have shown the field spread was never consulted.**

### Cluster 3 — "Which dirty tricks should we try, and which are dead?" — 2,867 lines

`exploit-queue-brief-2026-08-08` (189), `ptp-feasibility-2026-08-08` (437),
`exploit-triage-feasibility-2026-08-08` (629), `mechanic-bans-2026-08-09` (125),
`dirty-tricks-shortlist-2026-08-09` (110), `offensive-catalog-2026-08-09` (122),
`loki-arsenal-pricing-2026-08-09` (738), `AUDIT-the-six-refuted-roads-2026-08-10`
(248), `engine-guard-matrix-exploit-hunt-2026-08-10` (269).

**The sharpest instance in the repo: the side lane ranked the trick list at
15:07–15:22 and the research arm ranked it at 15:28, 21 minutes later, with zero
cross-citation.** Verified: `grep -ciE 'dirty-tricks-shortlist|offensive-catalog|mechanic-bans'
docs/research/loki-arsenal-pricing-2026-08-09.md` → **0**. Three items are the
same object under different names (launcher kidnap, spawn-ring denial, ore
denial) and the two lists reach **opposite verdicts** on two of them —
`offensive-catalog` lists spawn-ring denial and ore denial as **live**;
`loki-arsenal-pricing` marks both **REFUTED**. `AUDIT-the-six-refuted-roads-2026-08-10`
exists because of exactly this: its own headline is *"Establishing what each
rests on cost ~60 tool calls."* **That is the price of the missing citation,
paid in tool calls the next day.**

### Cluster 4 — "Can our instruments support the decisions being made?" — 2,059 lines

`v1-2026-08-08-measurement-power` (322), `v2-2026-08-08-gate-vs-ladder` (94),
`v5-2026-08-08-instrument-coverage` (179), `v5-instrument-coverage-2026-08-08`
(111), `instrument-audit-2026-08-08-late` (461), `instrument-audit-bands-2026-08-09`
(198), `instrument-sweep-close-2026-08-09` (113), `test-process-proposal-2026-08-09`
(153), `audit-2026-08-10-s27` (367), `SCRIPTABLE-OPS-AUDIT-2026-08-10` (61).

**This is the cluster this document joins, and it is on its fourth iteration.**
`instrument-audit-2026-08-08-late.md` and `audit-2026-08-10-s27.md` carry the
same question verbatim and were **spawned by the same tool** —
`tools/audit_trigger.py`, firing 2/4 on 08-08 and 2/5 on 08-10. The s27 audit
cites `v1-2026-08-08-measurement-power` (2 hits) but **`grep -c
'instrument-audit-2026-08-08' docs/workflow-analysis/audit-2026-08-10-s27.md` →
0** — the 461-line audit asking its exact question was not read. And v1's fix
never landed: `tools/arena.py:99` still reads `--seeds ... default=4`, which is
the exact 120-match underpowered default v1 was written to kill.

### Two same-day duplicates (fail the ≥2-dates bar, but are true redos)

* **"How many units leave the game to uncaught exceptions?" — 464 lines, 92
  minutes apart, no cross-citation** (verified: `grep -c` each way → 0/0).
  `undamaged-builder-deaths-2026-08-10.md` (04:51, 344 lines; classifier =
  removal at positive HP; us 0/539, third party 2,636/25,466 = 10.35%) and
  `crash-census-2026-08-10.md` (06:23, 120 lines; classifier = `removeEntity`
  with no `updateHp`; us 0 vs opponents 2,451 over 1,855 games). Two
  independently built instruments, same census. They agree — **but only the
  first records why we are at zero:** *"we are at zero because `run()` wraps
  everything in a blanket `try/except Exception`, not because our paths are
  vision-safe."* `CLAUDE.md` quotes the second's 2,451/1,855 figure as exploit
  evidence **without that caveat.**
* **"Does the slot-swap rule work?" — 320 lines, both 08-08.** This one is the
  *healthy* form: `v3-2026-08-08-swap-rule.md` names the research arm's
  reframing in its header. A handoff, not a redo. Worth keeping as the control.

### Refuted as redos (checked, not assumed)

The crash/launcher chain is **cumulative** — all 08-10 and citing forward
(`engine-guard-matrix` → `engine-source-crash-and-launcher`;
`crash-induction-targeting` → `undamaged-builder-deaths` + `idle-round-envelope`;
`PREREG-loki14` → `engine-source`). So is the "re-derive standing context"
cluster I suspected: `standing-context-rederived-2026-08-10.md` opens by naming
`prior-tracing-2026-08-10.md` as its companion and does *the remaining* claims.
Also cumulative: the titanium-delivery chain, the kill-game-split chain, the
heal chain. **My own suspicion list was wrong on two of four — the repeats are
not where the "AUDIT/re-derive" filenames are.**

### And the repo already named this failure, one day ago, and specced the fix

`docs/research/PROGRAMME-drift-watch-2026-08-09.md:35`:

> **D14 — A CLOSURE AND A POSITIVE RESULT ON THE SAME QUESTION MUST BE FORCED TO
> CITE EACH OTHER, or the library holds both indefinitely. … What was missing was
> any mechanism that makes two documents on one question meet. … It took an
> unrelated D12 sweep to notice, which is luck, not process.**

`docs/research/SCRIPTABLE-OPS-AUDIT-2026-08-10.md:20`:

> `| 5 | **D14 cross-citation flag** … | HYBRID | new xcite.py | unbounded (not done) | its only catch to date was "luck, not process" |`

**Diagnosed, named, specced, marked "unbounded (not done)", and then four more
redo clusters were produced.** The problem is not that the project cannot see
this. It is that seeing it produces another document.

---

## 3. IS THE BOTTLENECK ANALYSIS VOLUME? — NO. Two separate answers.

### 3a. The trigger's own arithmetic is broken. This part is a null.

`cross_lane_analysis()` computes
`docs_added_in_last_24h / decision_rows_in_last_50_tape_rows`.

**The two windows do not match, and the mismatch is not small.**

* `results.tsv` is 318 csv rows. `git log --since=24.hours --numstat -- results.tsv`
  returns **`added 1 deleted 0`** — the tape gained **one row** in the entire
  measured window, the LOKI-8 ship row at `4ad19ab`, 2026-08-09 20:38.
* Walking the tape backwards through git: the first commit at which
  `results.tsv` held ≤268 csv rows is `de8feb6`, **2026-08-08 21:02:10 +0200**.
  So the 50-row denominator window is **~42 hours wide**, and **49 of its 50
  rows were written before the 24h numerator window even opened.**

The docstring states the premise that makes the ratio meaningful: *"a decision
is still only recorded in one place."* **That premise is now false.** The
decision record moved into `docs/`:

* **11 preregs** committed on 2026-08-10 alone (`docs/prereg/PREREG-loki10..16`,
  `-confirm-pavetrail`, `-live-unrated-baseline`, `-panel2-calibration`,
  `-pinned-testbed-control`), 5 more on 2026-08-09
* **3 RESULT docs** on 2026-08-10, 3 on 2026-08-09
* **30 leg match ids** durably recorded in `docs/legs/LEG-MATCH-IDS-2026-08-10.md`
  (= 150 games)
* **25 of the 303 numerator files are themselves decision records** (every
  `PREREG*`, `RESULT*`, `LOCK-CERT*`, `QUARANTINE*`, `LEG-MATCH*` under `docs/`)

**So the row counts decisions as analysis.** It is structurally incapable of
reading `ok` as long as decisions are recorded as `.md` under `docs/` and the
tape is not written. Recomputed on a matched 24h window with decision records
moved to the denominator, and with the tactics library excluded:
`(86 − 25) / 25 = 2.44` — **below its own 4.0 threshold.** Include the tactics
library and it is `(303 − 25) / 25 = 11.1`, still tripping. **The verdict
therefore rests entirely on whether the tactics library counts — which is
finding 2 above, not the finding this row claims to make.**

Meanwhile the things that would show a project not deciding are all at session
highs. In the same 24 hours: **40 new bot directories** (`_v117loki2` through
`_v133loki16`, plus 8 `_probe_*` and 12 `_det_*`), **33 modified files under
`bots/` (+636/−495 lines of real edits, not copies)**, **+3,204 lines under
`tools/`**, 16 named planks LOKI-2..LOKI-16 built.

**On its stated question — "is the project producing analysis instead of
decisions?" — this row's answer is not trustworthy and its 14.43 should not be
quoted.**

### 3b. Ship cadence, now that the brief's correction has landed

The builder has since shown the red test was a **rotted fixture**, not a
miscalibrated check (`c347ec7`), and narrowed the reading: 8 `active_bot`
transitions in 24h = 0.38/hr, of which 4 are experiment round-trips, leaving
**4 durable activations = 0.19/hr**. I re-derived the whole tape independently
(reversal within 60 min = not durable):

| day | transitions | durable |
|---|---|---|
| 2026-08-06 | 6 | 6 |
| 2026-08-07 | 21 | 17 |
| 2026-08-08 | 19 | 18 |
| 2026-08-09 | 9 | 9 |
| 2026-08-10 (to 14:42) | 5 | **3** |

**The fall is real and it is ~4x.** But the calibration does not survive
contact with what changed:

| day | durable activations | preregs committed | RESULT docs | leg match ids recorded |
|---|---|---|---|---|
| 2026-08-08 | **18** | **0** | **0** | 0 |
| 2026-08-09 | 9 | 5 | 3 | 0 |
| 2026-08-10 | **3** | **11** | **3** | **30** |

**`ship_cadence`'s 0.5/hr threshold was calibrated on 2026-08-08 — the last day
on which shipping *was* the measurement instrument.** The tape's own row
`swap_loop_validated` records that method: *"THE SHIP-MEASURE-ROLLBACK LOOP IS
VALIDATED AND COSTS ZERO ELO"*, and `_v102thor-refuted` reads *"SHIPPED,
MEASURED, ROLLED BACK IN 5 MINUTES"*. Under that method every measurement
necessarily produced an activation, so activations/hour was a fair proxy for
decisions/hour. **The LOKI directive and the unrated-leg method replaced it:
`fcode match unrated` measures with the incumbent live, and only a CONFIRMED
plank earns an activation.** Activation rate fell 4x because the numerator of
"decision" moved, not because deciding stopped.

**On the builder's second-order question — is the durable-activation narrowing
right?** Yes as an accuracy fix, and I would take it. **It does not rescue the
threshold.** 0.5/hr encodes "one ship every two hours", which was the natural
rate of a method that shipped in order to measure and is not the natural rate of
a method that pre-registers, fires unrated, and ships on confirmation. If the
narrowing lands, the threshold has to be re-derived against 2026-08-10-and-later
days or the row will trip on correct behaviour every day from now on. **A row
whose threshold was tuned under a superseded method is the same failure family
as a fixture whose timestamps were tuned under a superseded clock.**

### 3c. THE REAL BOTTLENECK, and it is measurable

The three recorded failures in the brief are one failure. **Legs are being fired
at a session-record rate and are coming back unable to distinguish anything.**

`docs/prereg/PREREG-panel2-calibration-2026-08-10.md:14-20` decomposes the
pinned panel (I verified the same decomposition independently in
`docs/research/RESULT-loki11-rush-reopen-2026-08-10.md:330-334` and
`docs/coordination.md:26069-26072`):

| cell | record | range across 4 windows |
|---|---|---|
| The Bisons | 0/20 then 1/20 | **0 — floor** |
| Leviathan | 16/20 | **0 (4,4,4,4) — ceiling** |
| CtrlAltDefeat | 15/20 | 1 — ceiling |
| I Stone | 8/20 | 4 — live |
| gsxWins | 6/20 | 3 — live |

**Power arithmetic for the confirmatory test** (`docs/research/RESULT-confirm-pavetrail-2026-08-10.md`,
control n=150, arm n=100, two-sided Fisher at α=.05, control share 0.54):

```
MDE at 80% power                                  18.1 pp
power vs a TRUE 18pp effect (homogeneous cells)   80.3%
```

So on its face the leg was sized correctly — **its MDE (18.1pp) is its own
claimed effect (18pp) to one decimal.** That is the trap. Two independent
corrections both push the real power to ~20%:

**(i) Cell dilution.** If 3 of 5 cells cannot move, a true effect `d` on the two
live cells appears in the pooled number as `0.4 × d`:

| true effect on live cells | pooled | power |
|---|---|---|
| 18 pp | 7.2 pp | **20.0%** |
| 30 pp | 12.0 pp | 46.0% |
| **45 pp** | 18.0 pp | 80.3% |

**The effect this fixture can actually resolve at 80% power is 45pp on the live
cells.** Nothing in this game moves a core-kill share by 45pp.

**(ii) Winner's curse, which holds even if you reject (i).** The +18pp was a
*discovery* estimate from an n=100 v 100 leg reported at p=0.016. A
just-significant result at that n has a point estimate of ≈13.9pp, and the 80%
MDE there is 19.8pp — i.e. **the discovery estimate sits at or above the MDE by
construction, so it is upward-biased.** Sizing the confirmation at the discovery
point estimate therefore buys ≤50% power against the truth:

| true effect | power of the confirm arm |
|---|---|
| 5 pp | 12.1% |
| 7 pp | 19.1% |
| 9 pp (half the estimate) | **28.5%** |
| 12 pp | 46.0% |
| 15 pp | 64.5% |

**p=0.303 is not a surprising result. It is the expected output of a ~20-28%
powered test.** The prior art found 19% power on the n=120 arena battery on
2026-08-08. **This is 20% power on the live-unrated panel on 2026-08-10 — the
project rebuilt the same defect into the replacement instrument**, which is
exactly what `PREREG-panel2-calibration` says in its own words (*"That is D11
saturation — the defect we diagnosed in the self-authored ARENA — rebuilt into
the live fixture"*).

**One caveat I owe, against my own argument:**
`docs/research/RESULT-loki13-economy-suppression-2026-08-10.md:168,174` records
The Bisons at **1/20 control vs 4/20 treatment, +15pp at matched seats** — the
"floor" cell moved. So "range 0" is a statement about four control windows, not
a proof of inertness at n=20, and the dilution factor 0.4 is an assumption, not
a measurement. **Argument (ii) does not depend on it and reaches the same
place.**

**So: the honest answer to question 3 is that the trigger is measuring the wrong
thing — but the null is only on the trigger, not on the project.** Analysis
volume is not the bottleneck. Decision rate is not the bottleneck. **Resolution
is.** The project is spending its free-and-plentiful unrated windows on a
five-cell panel of which two carry the information, and it is writing
pre-registered bars (+18pp, +30pp) that the fixture cannot resolve. Every leg
fired against that fixture is pre-destined to a null, and a null on an
unresolvable fixture teaches nothing about the plank.

---

## 4. RECOMMENDATION — one change, ~30 minutes, checkable on data already on disk

**Add a per-opponent split and a computed MDE to `tools/leg_read.py:87 report()`.**

The tool **already collects the field it needs and throws it away.**
`collect()` at `tools/leg_read.py:76-86` builds `{"opp": opp, "seat": ..., "map":
..., "cond": ..., "we_won": ...}` per game. `report()` at
`tools/leg_read.py:117-122` prints a **seat mix** and a **per-map** split — and
**no per-opponent split of `core_kill_share` anywhere.** The decomposition that
finally exposed three inert cells was done by hand, into a prereg, *after* two
18pp claims had already failed on it.

And the resolution warning it does print is a **hardcoded string**, not a
computation — `tools/leg_read.py:168`:

```python
print("  NOTE: with n~25 per arm this resolves ~20pp at best. "
      "Do not read a small delta as a result.")
```

That line is a constant. It says the same thing at n=25 and at n=150, and per the
repo's own instrument rule a constant column validates anything.

**The change:**

1. In `report()`, add a per-opponent table: `opp | kills/n | share | seats`.
   ~8 lines, using `g["opp"]` which is already there.
2. Replace the hardcoded NOTE with a computed two-proportion MDE from the actual
   `a["n"]`/`b["n"]`: `MDE = 2.802 * sqrt(0.25*(1/n1 + 1/n2))`, printed next to
   the observed delta, plus the line **`cells with range 0 in this leg: <list>`**
   and an **effective-n** figure that drops them.
3. Print the pre-registered bar alongside it if the prereg path is passed, and
   say **`BAR BELOW MDE — THIS LEG CANNOT RESOLVE ITS OWN CLAIM`** when it is.

**Why this one and not a process rule:** it is the smallest change that converts
the failure mode from invisible to unmissable, it runs on `fcode match info`
(a read, no matches fired, no rate limit), and **it is checkable immediately
against data already recorded** — `docs/legs/LEG-MATCH-IDS-2026-08-10.md` holds
30 match ids across LOKI-13, LOKI-11 and the pinned n=50 control. Re-run the
patched tool on those and it must reproduce the panel-2 decomposition
(Bisons floor, Leviathan/CtrlAltDefeat ceiling, I Stone and gsxWins live) that
took a hand-analysis and two failed legs to find. **If it does not reproduce it,
the patch is wrong and you have lost 30 minutes.**

**What it changes about what gets decided:** today a null leg is written up as
"the plank did not separate". After this, a null leg prints its own effective n
and the effect size it could have detected, so the write-up is forced to be
either "the plank did not separate, and this leg could have seen 18pp" or "this
leg could only have seen 45pp, so nothing was tested". Those are different
decisions and the project currently cannot tell them apart at read time.

### Two things I am deliberately NOT recommending, and why

**Not `xcite.py` (the D14 cross-citation flag), even though finding 2 is its
exact use case.** It is already specified at `SCRIPTABLE-OPS-AUDIT-2026-08-10.md:20`
and already marked **"unbounded (not done)"**. Recommending a second time
something whose own spec says it has no bounded scope is how the first
recommendation died. If it is built, it should be built only as the three
mechanical signals the redo analysis actually measured, each of which is a
one-line filter: (a) the 81 research docs whose only citer is
`docs/coordination.md` or which are cited by nothing; (b) same-question doc
pairs written by different lanes within one hour — the two worst instances in
this repo are 21 minutes and 92 minutes apart; (c) any doc with **no `.md`
basename in its first 40 lines**, which is starting from zero by construction.
Anything beyond those three is the unbounded version again.

**Not a fix to `cross_lane_analysis()`.** Matching its windows would take 5
minutes, but the row would still be a proxy for a thing the project now records
in four places. **The honest move is to mute it** — treat it as unreadable
rather than as a 2/5 vote — until someone decides where a decision is recorded.
Note that its `--selftest` passes and will keep passing: the tripper feeds it 5
synthetic docs against 1 synthetic verdict row, which proves the row **can fire**
but says nothing about whether its two windows are the same window. **The file's
own docstring argues that an instrument never observed to fail is a claim, not
evidence. The dual also holds and is not covered: an instrument observed to fire
on a corrupted input has been shown to have teeth, not to have aim.**

---

## WHAT I DID NOT CHECK

* I did not verify the panel cell records against the platform — `leg_read.py`
  needs live `fcode` calls and the brief forbade firing anything. The cell table
  is taken from three in-repo sources that agree
  (`PREREG-panel2-calibration:14-20`, `RESULT-loki11-rush-reopen:330-334`,
  `coordination.md:26069-26072`).
* The citation test is a **substring match on basenames**. It will miss a doc
  whose content was absorbed into a decision without the filename being written
  down, and it cannot detect a doc that was read and correctly discarded. It is
  a floor on citation, not a ceiling. It also cannot credit a doc written after
  the decision it informed.
* `tools/preflight.py` — I read it and the identity bug is already fixed
  (`f4372dd`, flagged in `coordination.md:26691-26706`, ~2h from report to fix).
  I did not re-audit the fix; it is out of my subject.
* I did not evaluate whether any individual analysis doc is *correct*. This
  audit is about whether analysis reaches decisions, not about its quality — and
  the docs I read closely (`RESULT-confirm-pavetrail`, `PREREG-panel2-calibration`)
  are, if anything, unusually rigorous. **The panel-2 prereg had already
  diagnosed the bottleneck I am reporting, before I was spawned. That is worth
  saying plainly: the analysis found the problem; what it did not do is stop the
  legs that were still being fired against the broken fixture.**
