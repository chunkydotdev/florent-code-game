# INSTRUMENT USABILITY REVIEW — 2026-08-15

**Written 2026-08-15T16:28:14Z (`date -u`) at `d5e0cf86`, branch `main`.**
**Question asked (Magnus):** *"we just had a few sessions that were super confused about how it
worked on opus. Can we see any big issues and can we make the system easier to use for lower
intelligence models than fable?"*

**Scope:** the instrument and documentation layer — not the bot, not the programme, not any verdict.
**Method:** every finding below was reproduced by running the command printed under it, on this tree,
today. Nothing here is inferred from the retros alone; the retros are cited only as corroboration
that the failure already happened in the field.

**⚠ ONE STANDING CAVEAT ON THIS DOCUMENT ITSELF.** It argues that dense prose is the problem, so it
is written in the style it recommends: one claim per line, a repro command per finding, no
retracted text kept inline. If a successor makes it longer, that is the defect recurring.

---

---

## ⭐ STATUS — UPDATED 2026-08-15T16:5xZ AFTER A FIX PASS

**LANDED (verified, each driven to both verdicts where it is a guard):**

| # | what shipped | verification |
|---|---|---|
| F1 | **`tools/now.py`** — the one canonical state block; holder from `fcode status`, control from `PROGRAMME.md`, age on every surface | selftest 8/8; degraded-`fcode` case goes **BLIND + rc 2** instead of inventing a holder |
| F2 | **`elo_history.tsv` migrated to UTC+`Z`**; `elo_logger.py` fixed; `freshness.py` made **marker-authoritative**; `audit_trigger`/`dash.serve` parsers corrected | 2,514/2,514 rows converted via `zoneinfo` (not a hardcoded −2), non-timestamp columns **byte-identical**, freshness now PASSES under both `assume_local` values; selftest 16/16 + mutation test proves the marker is load-bearing |
| F5 | **README rewritten as a router** — surface table, queue table, "do not read state from this file" | the three false claims removed |
| — | **`audit_trigger`: a cell that cannot evaluate is now `BLIND`/`UNKNOWN`/rc 2, not silently "ok"** | both verdicts: healthy → `OK` rc 0; injected fault → `UNKNOWN … Not a clean bill of health` rc 2 |
| — | **`now.py` wired into all three lane boot sequences** as step 0 | — |

**STILL OPEN:** F3 (`--help` contract), F4 (`tools/boot.py`), F6 (split `CLAUDE.md`),
F7 (rule audit), F8 (subjects on alarm rows — partially addressed), F9 (`tools/INDEX.md`),
F10 (`queue_check --next`).

**FOUND DURING THE FIX PASS, NOT IN THE ORIGINAL REVIEW** — see
`FLEET-AUDIT-2026-08-15.md` for the queue/poller audit: a **dead supervisor** that would have
idled the box overnight, a **duplicate canceller**, **double-logged** run logs that make one
runner look like two, and **four host-keys for two machines**.

---

## THE HEADLINE

**The system is optimised for a reader who can hold ~200k tokens of layered, self-correcting prose
and infer which of five surfaces answers a question. That is a real capability and Fable has it.
Everything below is what happens when the reader does not.**

The failure mode is **never** "the model could not find the tool". It is **"the model found a
surface, read it correctly, and it was the wrong surface"** — and the repo's own s43 side-lane retro
converged on exactly this independently:

> *"All five [published errors] are one surface adjacent to the right one."*
> — `docs/retro-side-lane-2026-08-15-s43.md` §Q3

**A weaker model does not make a different mistake. It makes the same mistake more often, and it
lacks the second instrument in the same output that currently catches ~half of them.**

⇒ **The fix is not more explanation. It is fewer places a question can be answered from, and tools
that refuse rather than rules that instruct.**

---

## FINDINGS, ORDERED BY WHAT THEY COST

### F1 ⛔ "WHAT IS LIVE RIGHT NOW" HAS FIVE ANSWERS AND THREE ARE CORRECT-FOR-A-DIFFERENT-QUESTION

The single highest-cost defect. Reproduced just now:

| surface | says | what it is actually for |
|---|---|---|
| `fcode status` | **v151, 1707, Emerald, #23** | ⭐ **the truth about the holder** |
| `corpus/ship_watch.log` | v151, 1707 | the **trend**; a 10-min poller, blind between polls |
| `elo_history.tsv` | 1707, v151 | the **rating tape**; tagged by version *active at poll time* |
| `corpus/ladder_games.tsv` | `ourver=140` | **per-match rated ground truth**; ~30 min behind live |
| `PROGRAMME.md: INCUMBENT` | `bots/_v223sealrepair` (v140) | the **CONTROL for the queue**, not the live bot |

```bash
.venv/bin/fcode status | head -8
tail -1 corpus/ship_watch.log; tail -1 elo_history.tsv
tail -1 corpus/ladder_games.tsv | cut -f2,4,5; grep -n INCUMBENT PROGRAMME.md | head -1
```

**All five are correct. None is wrong. Four of them will get you a wrong answer to "what is live".**
This bit the side lane in the final commit of s43 — a reboot state written off `ship_watch` inside
its poll gap, by the lane that had flagged that exact hazard twice the same day (`e19e1e97`).

⇒ **FIX — `tools/now.py`, one screen, no arguments.** Prints the canonical state block: holder from
`fcode status` (never a poller), control from `PROGRAMME.md`, rating trend from the tape, rated
ground truth from `ladder_games`, **each line labelled with the question it answers and its age.**
Boot sequences and HANDOVER's live block are then generated from it rather than typed. This is
~60 lines of code and it deletes the entire class.

---

### F2 ⛔ `elo_history.tsv` IS THE ONLY SURFACE ON LOCAL TIME, AND IT LOOKS LIKE UTC

`tools/monitors/elo_logger.py:69` writes `datetime.now().strftime("%Y-%m-%dT%H:%M")` — **local
(CEST), ISO-shaped, no `Z`.** Every other surface writes UTC with an explicit `Z`.

```
NOW UTC                        2026-08-15T16:27:09Z
elo_history.tsv newest         2026-08-15T18:23      <- LOCAL, reads as ~2h in the FUTURE
corpus/ship_watch.log newest   2026-08-15T16:22:34Z  <- UTC
corpus/ladder_games.tsv newest 2026-08-15T15:12:59.711Z
gate_invocations.tsv newest    2026-08-15T13:09:41Z
```

**2,510 of 2,510 rows carry no `Z`.** The project's own shared freshness helper already refuses it:

```bash
.venv/bin/python -c "import sys;sys.path.insert(0,'tools');from freshness import assert_fresh;from pathlib import Path;print(assert_fresh(Path('elo_history.tsv'),max_age_h=1))"
# CLOCK ERROR: elo_history.tsv newest row 2026-08-15T18:23 is 1.9h in the FUTURE.
```

**The tape can never pass a freshness assertion, and to anything that does not gate it always looks
the freshest surface in the repo.** It fails in the flattering direction.

⇒ **FIX — three steps, all small.** (1) `elo_logger.py:69` → `datetime.now(timezone.utc)` with `Z`.
(2) Backfill the 2,510 rows (−2h CEST, −1h CET before the DST boundary — check the boundary, do not
assume one offset for the whole tape). (3) Add to `tests/test_instruments.py` a check that **every
timestamp column in every tracked TSV ends in `Z`**, driven to both verdicts. One convention, mechanically enforced.

---

### F3 ⛔ `--help` IS A LOTTERY, AND ON MOST TOOLS IT RUNS THE TOOL AND PRINTS VERDICT-SHAPED OUTPUT

Probing an unknown tool with `--help` is the first thing any model does. Here is what it gets:

| tool | `--help` exit | what it printed |
|---|---|---|
| `gate.py` | 0 | proper usage ✅ |
| `queue_check.py` | 0 | proper usage ✅ |
| `prereg_check.py` | 0 | proper usage ✅ |
| `control_pin.py` | 0 | proper usage ✅ |
| `leg_read.py` | 0 | ⛔ **`LEG: no completed games`** — reads as a finding about a leg |
| `freshness.py` | 1 | ⛔ **`BLIND: --help has no parseable timestamp…`** — it analysed the flag |
| `plank_status.py` | 0 | ran the real report |
| `score.py` | 0 | ran |
| `effective_n.py` | 0 | ran a full corpus cut |
| `claim_check.py` | 1 | ran, scanned 22 files |
| `target_value.py` | 2 | ran |
| `mde.py` | 2 | usage-ish, wrong exit |

```bash
for t in leg_read freshness plank_status effective_n; do .venv/bin/python tools/$t.py --help; echo "exit=$?"; done
```

**40 of 84 tools have no `argparse` at all. 21 of those 40 write files or shell out** — so a probe
run is not read-only.

**This is the single most likely origin of "confused about how it worked".** The model asks a
harmless question, gets an authoritative-looking sentence back, and there is nothing in the output
saying *"this is not an answer, this is help text I do not implement."* `freshness.py --help`
literally emits the word `BLIND` — a verdict token this repo uses for real.

⇒ **FIX — two things, both mechanical.**
1. A shared preamble (`tools/lib/cli.py`) giving every tool a side-effect-free `--help` that prints
   docstring line 1 + usage, and **exits 0**.
2. A test in `tests/test_instruments.py`: for every `tools/*.py`, `--help` **exits 0**, prints a line
   starting `usage:`, and **creates/modifies no file** (snapshot the tree around it). Forced-fail
   fixture: a tool that ignores `--help` must make the test go red.

---

### F4 ⛔ THE MANDATED BOOT READ IS ~140k TOKENS, AND ONE MANDATED FILE IS ~960k ON ITS OWN

Measured on this tree:

| file | lines | ~tokens | boot status |
|---|---:|---:|---|
| `docs/coordination.md` | **57,429** | **~959,665** | "read the tail" — no machine-findable tail marker |
| `QUEUE.md` | 772 | ~80,047 | "read at boot and fire from the top" |
| `docs/research-arm-retro.md` | 1,491 | ~24,246 | read at boot (research) |
| `docs/builder-arm-retro.md` | 1,271 | ~19,351 | read at boot (builder) |
| `docs/side-lane-retro.md` | 1,194 | ~19,334 | read at boot (side lane) |
| `CLAUDE.md` | 721 | ~15,393 | auto-loaded every session |
| `PROGRAMME.md` | 598 | ~9,049 | read before HANDOVER |
| `HANDOVER.md` | 275 | ~4,990 | top block only |
| lane command file | ~113 | ~3,550 | the charter |

**Total repo markdown: 864 files, 15.4 MB.** `docs/research/` alone is 305 documents.

A builder boot done exactly as specified is **~140k tokens before the first useful action** — and the
two largest instructions (`coordination.md` tail, `QUEUE.md` top) are the two a weaker model is least
able to bound correctly. `builder.md:5` already says *"Tail = since the last wrap marker, or ~400
lines. NEVER the whole file (41k lines)"* — **the file has since grown to 57k lines and the guidance
still names 41k, which tells you prose cannot track this.**

⇒ **FIX — `tools/boot.py --lane <builder|research|sidelane>`, budget ≤ 8k tokens, no arguments to get
wrong.** It emits: the F1 state block · the last N coordination notes since the machine-detected wrap
marker · the top 3 queue rows with their bars and controls · open items from the lane's own arm retro
· any red boot check. **The charter stays prose; the state stops being prose.** Separately: rotate
`coordination.md` per session into `docs/coordination/<date>-s<N>.md` with a thin index — an
append-only 57k-line channel is not a channel.

---

### F5 ⛔ `README.md` — THE FIRST FILE A COLD AGENT OPENS — IS 9 DAYS STALE AND WRONG IN DECISION-CHANGING WAYS

Last touched 2026-08-06. It currently states:

* *"**Not yet registered on the platform** — application submitted, awaiting approval. No account
  means no ladder, no real map pool, no submissions; it's the only blocker."* — **we are live on the
  ladder with 1,048 rated matches.**
* *"Current best bot is **`bots/v4`** — 74.2% against starter"* — the incumbent is
  `bots/_v223sealrepair`; there are **565 bot directories.**
* *"`AGENTS.md` (and its copy `CLAUDE.md`) is the organisers' own context file"* — **inverted.**
  `AGENTS.md` is the generated copy *of* `CLAUDE.md` (its own header says so), and `CLAUDE.md` is now
  the project's primary directive with hundreds of lines the organisers never wrote.

**A model that trusts the README concludes we cannot submit and that our best bot is `v4`.** Nothing
in the file says it is stale; it reads as current and confident.

⇒ **FIX — replace the body with a router**: what this repo is, the three lanes, `tools/boot.py`, and
a table of *question → surface*. Add its freshness to the boot checks so it cannot rot silently
again.

---

### F6 ⚠ `CLAUDE.md` KEEPS ITS OWN RETRACTED TEXT INLINE, IN FULL, IN THE ALWAYS-LOADED FILE

16 passages in `CLAUDE.md` retract or amend earlier text in the same file. Three print the retracted
claim **in full**, under headings like:

> **THE ORIGINAL CLAIM, KEPT FOR THE RECORD:**
> **AND THE RATED COST IS ZERO, MEASURED.** …

```bash
grep -n -iE "CORRECTED|AMENDED|THIS (BULLET|CLAUSE|SAID|READ)|KEPT FOR THE RECORD" CLAUDE.md
```

**For a strong reader this is excellent provenance and I would not remove it from the repo.** For a
weaker one it is 61 KB in which live rules and dead rules are typographically identical — both bold,
both emphatic, both in the file that is loaded whether or not it is read carefully. The document also
carries **11 ⛔, 9 ⭐, 464 bold spans**: when everything is emphasised, emphasis stops routing
attention.

⇒ **FIX — split, do not delete.** `CLAUDE.md` becomes **current rules only**: imperative, one per
line, no retracted text, no history, target ≤ 250 lines. Everything struck out moves to
`docs/reference/DIRECTIVE-HISTORY.md`, linked once. **Rule: the always-loaded file states what is
true now; the archive states what we used to think.** The repo's own meta-lesson — *"a fact recorded
in a reference nobody boots and contradicted by the always-loaded file is a fact nobody has"* — is
satisfied, because the direction here is the safe one: the always-loaded file keeps the **live** fact
and exports the dead one.

---

### F7 ⚠ THE RULES ARE PROSE, AND THIS REPO HAS ALREADY MEASURED THAT PROSE RULES DO NOT BIND

`builder.md:34`, written by this project about itself:

> *"every prose-only rule in this repo has a recorded violation by its own author; the two durable
> surfaces are this file and tools that exit 1."*

Corroborated within the last 48 hours, all in `git log`:
* **Three forks of the control tree in one afternoon** (`55d8a451`, `3c7964bf`, `031a83cd`), with the
  rule against it written **between the first and the second**. Ended in a refusing tool
  (`control_pin.py`), not a discipline.
* **D28 committed by the lane that promoted D28** (`e19e1e97`) — stale-holder read, flagged by that
  same lane twice the same day.
* **`fleet_dispatch.py` built and never started** (`bd492636`) — 3h06m idle, remote workers idle 39 min.
* **`auto_gate --apply` armed and inert on nearly every live shard** (`1d1987c2`) while its summary
  read *"nothing is arithmetically dead"*.

**Every one of these is a strong model failing a prose rule it had read that day.** A weaker model
will fail them at a higher rate, and the difference between the two is not worth designing around —
**the tool that refuses works for both.**

⇒ **FIX — a rule audit with exactly three outcomes per rule.** Walk `CLAUDE.md`, `PROGRAMME.md` and
the three charters, and mark each rule: **`ENFORCED:<tool>`** (a tool exits nonzero) · **`ADVISORY`**
(explicitly not enforced — and say so, so nobody assumes cover) · **`TO ENFORCE`** (queued, with the
tool named). Print the tally at boot. **A rule with no tool and no `ADVISORY` label is the dangerous
middle**, because it reads as a guardrail and is not one.

---

### F8 ⚠ NUMBERS ARRIVE WITHOUT THEIR SUBJECT — OUR OWN ALARMS ATTRIBUTE A TEAMMATE'S ACTIVITY TO US

`tools/audit_trigger.py` runs on every builder boot. Today it prints:

```
[TRIP] ship cadence   0.41/hr   9 activations in the last 24h over ~22 active hours
```

**We activated zero times today.** The no-ship rule held all session; the activations were x3r0's
(v146–v151). The row **counts activations with no `ourver` filter and attributes them to us**
(`02a054e4`, `d5e0cf86`) — the same defect found the same morning in `slot_rule` on a different
instrument (`91eed50e`).

⭐ **This is the hardest class to catch, because the number is correct.** It is a true reading of the
wrong subject. `CLAUDE.md` already has the rule — *"Numbers carry subjects"* — and it is stated for
published statistics, not for our own alarms.

⇒ **FIX — extend the rule to instrument output and enforce it.** Every count a tool prints carries
its **subject, denominator and window inline** (`9 activations [ALL TEAMS, 24h] — ours: 0`). Add to
`tests/test_instruments.py` a check that each alarm row names its population. Immediate fix for
`audit_trigger`: split the activation count by uploader (already carried as HANDOVER item 10).

---

### F9 ⚠ 84 TOOLS, NO INDEX, AND THE NAMES DO NOT SAY WHAT THEY ANSWER

`tools/*.py` = 84, plus 18 corpus builders, 13 monitors, 5 dashboard, ~20 shell scripts.
**10 are mentioned in no document at all** (`border_defect_scan`, `choke_census`, `dodge_capture`,
`fixture_starvation`, `fwd_read`, `loki27_read`, `rentgun_drive`, `stub_engine`, `tune`,
`turret_selfkill_census`). Many of the rest appear only inside `QUEUE.md` — an 80k-token file, which
is not discoverability. `docs/tooling.md` names **6**.

Names like `peck_read`, `ring_read`, `fwd_read`, `det.py`, `dose.py`, `stack.py`, `pair.py` are
legible if you were there when they were written. **83 of 84 have a real module docstring** — the
knowledge exists, it is just not indexed.

⇒ **FIX — generate `tools/INDEX.md` from docstring line 1**, grouped by *question answered* (state ·
gating · corpus · legs/preregs · statistics · monitors), with each entry marked read-only or
mutating. Regenerate in the same test that enforces F3. Delete or `docs/archive/` the 10 orphans, or
give them a one-line reason to exist.

---

### F10 ⚠ THE QUEUE PRINTS 52 TRUNCATED ROWS AND NO NEXT ACTION

The `SessionStart` hook dumps 52 unblocked items, each cut mid-title, plus *"⚠ 28 counted row(s)
carry a legacy marker word in prose"* and *"⚠ GREP TREE UNNAMED (3 of 52)"*.

`queue_check.py` has `--floor` and `--selftest`. **There is no `--next`.**

The charter says *"read `QUEUE.md` and fire from the top"* — but the top is not shown, the ordering
is not stated in the output, and the file is ~80k tokens. **The first thing a session must decide is
the thing the tooling helps with least.**

⇒ **FIX — `queue_check.py --next`**: exactly one row, expanded, with its control, its bar, its
blocker status and the command that starts it. Hook prints that instead of 52 stubs; the full list
moves behind `--all`.

---

## THE SHORTLIST — IN ORDER

Ordered by (confusion removed) ÷ (effort). The first four are the ones I would do regardless of who
is reading the repo next.

| # | change | effort | removes |
|---|---|---|---|
| 1 | **`tools/now.py`** — one canonical state block, holder from `fcode status` | ~1h | F1 (five surfaces → one) |
| 2 | **UTC everywhere + a test** — fix `elo_logger.py:69`, backfill 2,510 rows | ~1h | F2 (a tape that reads from the future) |
| 3 | **`--help` contract + test** — side-effect-free, exit 0, `usage:` line | ~2h | F3 (probes that return false findings) |
| 4 | **`tools/boot.py`** — bounded boot context per lane | ~3h | F4 (~140k-token boot) |
| 5 | **README as router** + freshness check on it | ~1h | F5 (a confidently wrong first file) |
| 6 | **`queue_check.py --next`** | ~1h | F10 (no first action) |
| 7 | **Split `CLAUDE.md`** — live rules ≤250 lines, history exported | ~3h | F6 (live and dead rules look identical) |
| 8 | **`tools/INDEX.md`** generated from docstrings | ~1h | F9 (84 opaque tools) |
| 9 | **Rule audit** — ENFORCED / ADVISORY / TO ENFORCE | ~4h | F7 (prose that reads as a guardrail) |
| 10 | **Subjects on alarm rows** + test | ~2h | F8 (true readings of the wrong subject) |

---

## WHAT I AM NOT RECOMMENDING, AND WHY

**Do not simplify the programme, the bars, the DEFF corrections, or the prereg obligations.** None of
the confusion I found came from the statistics being hard. It came from **navigation** — which
surface, which clock, which file is current, what to do first. The rigour is the product; the
wayfinding is the defect.

**Do not delete the retros or the provenance.** They are why this review could be written from
artefacts instead of memory. Move them, index them, stop loading them at boot — do not lose them.

**Do not write more prose to fix prose.** Eight of the ten fixes above are code or a test. That ratio
is the point: this repo's own measured finding is that **a tool that exits nonzero binds and a
paragraph does not** — and that holds for strong readers too, which is why it is worth doing even if
every future session runs on Fable.

---

## HOW TO CHECK THIS REVIEW LATER

Every finding has a repro command inline. The two that will drift fastest:

```bash
# F2 — should print ok=True once fixed; today it prints a CLOCK ERROR
.venv/bin/python -c "import sys;sys.path.insert(0,'tools');from freshness import assert_fresh;from pathlib import Path;print(assert_fresh(Path('elo_history.tsv'),max_age_h=1))"

# F3 — should be silent once fixed; today it prints verdict-shaped text
for t in leg_read freshness plank_status effective_n; do .venv/bin/python tools/$t.py --help; done
```

**Not routed to any lane and not committed to any queue row — this is a review, not a decision.
Fix order is Magnus's call.**
