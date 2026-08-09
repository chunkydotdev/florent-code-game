# Builder-process review: the loop works when it's mechanical, decays when it's prose

**Side lane, 2026-08-09, on Magnus's directive: "investigate systematic builder
processes — how does the builder work, and is there anything process-wise we can
improve for the next session?" PROPOSALS ONLY — every recommendation below
touches builder-owned surfaces (method docs, tools, tape) or needs Magnus's
call; nothing here is a directive to either arm.**

**Version tag:** written while live = v91 "Eir 9c hivethaw" (`bots/_v100hf`,
tree `4558be91`), ladder 1575 @ 520 rank #30. Sources: primary reads of
`builder-method.md`, `ship-gate.md`, `.claude/commands/builder.md`,
`two-session-protocol.md`, `tools/gate.py`, `tools/audit_trigger.py`,
`test-process-proposal-2026-08-09.md`, tape structure, live monitor `ps`; plus
a commissioned full-history evidence sweep (opus subagent, read-only, s17–s24
across coordination.md/HANDOVER/workflow-analysis/tooling) whose four most
load-bearing claims I re-verified by hand against the primaries before use
(builder-method coverage grep = 0 hits; ship-gate.md:16,:57; instrument-audit
:226-231; elo_logger.py:98). Builder self-report was requested (msg 1658d201)
and is PENDING — will be relayed as an addendum, labelled as self-report.

---

## 1. How the builder actually works (the loop as practiced)

Five layers, in execution order:

1. **Boot** — `.claude/commands/builder.md:3-8`: HANDOVER top block →
   coordination tail (IN-FLIGHT + open items) → `ps` the monitor fleet →
   `tools/audit_trigger.py` → continue the queue. The s24 boot executed all
   five with zero deviation — the most disciplined boot on the record.
2. **The working unit is a PLANK, not a session** — name it → IN-FLIGHT
   register → pre-register threshold + confounds in a *pushed* commit → build
   a flagged variant of the live chassis → paired battery with a flags-off
   control → verdict note + inline `*Process delta:*` → tape row →
   occasionally ship.
3. **Method** — `builder-method.md` (s22): the evidence ladder
   `rule → probe → code → corpus → arena → field`, claim labels
   (code-fact / measurement / hypothesis), arena-is-safety-not-doctrine,
   composite-first ablation, delegate-but-never-the-verdict.
4. **Ship** — `ship-gate.md` + amendment: parity + window + nothing-known-
   broken; rollback as the control; windows as the scarce resource.
5. **Wrap (Magnus-called only)** — deltas synthesised into coordination.md,
   HANDOVER successor block, push, **name the wake path or state there is
   none**, relay live subagent output.

Session cadence: ~1–3 h per session against a ladder feeding **5.79
matches/hr** — one session spans less than two evaluation windows. Boot/wrap
overhead is a large fixed fraction of every session. Anything that shrinks
re-learning pays out at ~24 sessions and counting.

## 2. What the record shows: three cost concentrations

The sweep produced a 69-incident ledger (s17–s24, classes: instrument /
scope / coordination / wake / hygiene / decay / duplication). Full ledger in
the sweep transcript; the concentrations:

**#1 — The instrument was never examined** (dominant, not close).
Every arena battery in project history was self-play (`bots/opp_v*` = our own
prior versions; discoverable by a 4-minute grep; ~1,500–1,860 games/day
through it), while a foreign pool (`bots/*_probe`) sat on disk unused —
pointed at it once, ESCALATE's trigger condition appeared 1,625× vs **zero**
in our lineage. TLE was never enforced (1,860 games at `--tle 0` vs a real
10ms limit our worst turn exceeds by 30%). The standard n=120 leg has 19%
power; 0.0% of the Elo bleed had a valid instrument. The builder's own
sentence: *"Every methodological rule I wrote today was aimed at the ANALYSIS.
None of them asked what the instrument was."*

**#2 — The evaluation window is structurally too small, and rules keep being
written as if it weren't.** 46 slot runs, mean 6.9 matches, median 5, only 27%
ever reached the 8 the swap rule needs — *the safety rule has been unable to
arm on 73% of everything ever shipped*. An 8-match window resolves ≥9.2
Elo/match against an all-version spread of 12.0. Downstream: the −40.92-Elo
blind window (pre-registered evaluation point, no wake path attached), a
rollback trigger that flipped 20 minutes later, and a v90-rollback "recovery
read" that closed ~5 points over its line — under one match's swing, stated
honestly by the builder. `instrument-audit-2026-08-08-late.md` named two
internally consistent options (cap ship cadence, or stop calling the slot
evaluated); **the project chose neither and runs both**.

**#3 — Rules written in prose are broken by their own authors, inside the same
session.** The builder diagnosed it itself: NOISE_ON error diagnosed → written
into coordination.md → relayed as a lesson → **repeated two hours later**.
Delta-zero recurred three consecutive wraps despite each wrap naming it.
Working-range check written, nearly skipped on the next build. Timestamp drift
one hour after flagging the same bug in someone else's work.

## 3. The central finding: rule half-life depends on the surface it lands on

On this repo's evidence, a rule's durability is a function of **where it is
written**, and only two surfaces hold:

| surface | evidence | half-life |
| --- | --- | --- |
| wrap note / HANDOVER top block / auto-memory | delta-zero ×3; NOISE_ON repeat; seed-collapse repeat; commit-race fix invisible to unbooted sessions | **~one session** |
| `.claude/commands/builder.md` (the file that IS the boot) | delta-zero **stopped** the wrap sequence landed there; s22=17, s23=16 inline deltas | durable |
| a tool that exits 1 (`gate.py`, `corpus_sanity.py`, `tests/test_instruments.py`) | NOISE_ON and self-play now impossible to miss *when the tool runs*; corpus_sanity found a dead tiebreak-#1 column on its first run | durable **when called** |

**And the caveat that defines the s25 opportunity: none of the tools have a
caller.** `gate.py` is invoked by convention, not by `arena.py`;
`corpus_sanity.py` is in no query path; `tests/test_instruments.py` (25 real
assertions, 0.06s) has no runner — no CI, no hook, no boot step. Every
"tool-enforced" fix is one un-typed command from being skipped, and the gates
carry escape flags (`--allow-self-play`, `--skip-tle`). The instrument-check
layer exists; it is simply not wired into the paths that need it.

## 4. Ranked improvements for s25

Ordered by (evidence weight × cheapness). Owner tags: **[B]** builder adopts
or adapts, **[M]** Magnus decides.

1. **[B] Give the tools callers.** The cheapest hardening with the strongest
   evidence base (cost centre #3). Concretely: (a) add
   `tests/test_instruments.py` + `corpus_sanity.py` to the builder boot
   sequence in `.claude/commands/builder.md` — the surface proven durable;
   (b) make `gate.py` the *documented sole entry* to a battery (a one-line
   wrapper script that gates then fires would do it — builder's design call);
   (c) `det.py`'s distinct-shape warning becomes a non-zero exit below a
   floor. Escape flags stay — an escape *typed* is a decision on the record,
   which is the whole point.
2. **[B] Decide `test-process-proposal-2026-08-09.md` — and if adopted, adopt
   its forcing functions, not just its prose.** The S0–S8 pipeline is the
   direct answer to cost centre #1 (instrument selection was ad hoc through
   ESCALATE and SITE). Its two hooks — mandatory `S5_unrated:` /
   `treatment_occurrence:` tape fields and a ~30-line `preflight.py` that
   refuses "ready to ship" — are exactly the two surfaces §3 shows to be
   durable. Adopted as prose only, §3 predicts a one-session half-life.
3. **[M→B] Reconcile the safety rule to ONE statement, then implement it.**
   Four incompatible versions circulate: ship-gate.md's sign rule ("must not
   drift"), elo_logger.py:98's implementation of it, s19's "CHANGE ADOPTED:
   magnitude (2sd), never sign", s23's quoted "≤0 after 3 matches". Meanwhile
   `workflow-analysis/v3` measured the sign rule as a timer, not a control
   (neutral holder trips 50.4% by match 8; a genuinely +60-Elo bot trips
   78.6%). The magnitude fix was announced adopted and implemented nowhere.
   This is the entire control on shipping fast — it cannot be four things.
   Magnus picks the statement; the builder writes it into ship-gate.md AND
   elo_logger.py in the same commit.
4. **[B] Bring the READ-FIRST doc up to date with the largest finding the
   project has made.** `builder-method.md` contains zero mentions of gate.py,
   audit_trigger, corpus_sanity, `match test`, unrated, self-play, or opp_v
   (grep-verified). The self-play discovery, foreign pool, TLE gap, and the
   four s23 scope rules (what does it PRODUCE / working range / name the
   population / pre-register the rescue) live only in HANDOVER's top block —
   which the next wrap pushes down into the 1,946-line archive. One §-sized
   edit; prevents the flagship process discovery from decaying on schedule.
   Same commit: fix ship-gate.md's refuted founding premise (the −57 Elo
   window contained **ten slot changes**, not zero ships —
   instrument-audit:226-231) and the unverified 50-100× CPU figure (:57) —
   both still live in a policy doc.
5. **[B] The gate↔ladder join: one column.** Gate rows key on bot directory,
   ladder rows on version; 4 of 61 gate rows are joinable. "Does the local
   gate predict ladder Elo?" — the question that validates the entire loop —
   is unanswerable on the current tape. Specified in `workflow-analysis/v2`,
   unimplemented. One column on the ship row.
6. **[B] Fix `audit_trigger`'s note:verdict classifier.** `baseline` and
   `ship` rows are decisions; excluding them inflates the ratio ~2.4×
   (measured; re-derived on the current window: the 1.53 both arms saw
   becomes materially lower corrected). The tripwire that summons audits
   should not itself be miscalibrated — and its 1.53 has now tripped twice
   with nothing consuming it (**[M]**: who acts on a FIRE, given s23
   retrospectively judged it right?).
7. **[B] Move the two machine-scoped rules into the repo.** The commit-race
   fix (stage own files, verify HEAD, never re-commit) and wrap-vs-daily-note
   separation exist only in auto-memory — invisible to any session booting
   without it. One line each in builder.md's boot/wrap sequences.
8. **[M] The window-arithmetic decision from `instrument-audit`.** Two
   internally consistent options were named (cap ship cadence ~0.75/hr so
   windows can arm, or drop the 8-match evaluation claim and lean fully on
   corpus + unrated for post-ship reads). Running both halves means every
   ship's "evaluation" is partly fictional. This is a policy call, not a
   measurement gap — the measurement exists.
9. **[M] Update `two-session-protocol.md` for the real topology.** The doc
   says "one research arm at a time, never a third peer"; a third lane
   demonstrably operates under Magnus's commission with its pattern stored in
   auto-memory only. Codify the third-lane contract (append-only
   coordination, own-files-only commits, no bot/arena/verdict surface) or
   retire the lane.

## 5. What already works — do not fix

- **The boot sequence** (s24 executed it perfectly) and the **wrap sequence**
  — the latter is the single most effective process fix on record.
- **`gate.py`'s check design** — each check maps to a real incident; the
  pattern (incident → mechanical refusal) is the house style now. It needs
  callers, not redesign.
- **Pre-registration discipline for thresholds** — held well across s19–s24
  (the failures were scope, not thresholds).
- **The cross-lane adversarial review before build** — killed two harmful
  builds pre-build on 08-09 and refuted queue #1's premise before a line of
  code (the tile-repeatability test: learned tiles +3.8pp over random-in-band,
  negative at shippable sizes). Keep the discriminating-cut + placebo-arm
  exchange.
- **Push-every-commit and timestamp-from-`date`** — both held after adoption.

## 6. Open calls for Magnus (collected from above)

1. Safety-rule statement (rec 3) — which of the four is THE rule?
2. Window arithmetic (rec 8) — cap cadence, or drop the evaluation claim?
3. audit_trigger consumption (rec 6) — who acts on a FIRE?
4. Topology codification (rec 9) — third lane in the protocol doc, or not?
5. Standing from s23, still open: the lane call on scratchpad engine probes,
   and the second-hand "unrated/test games" directive (builder is acting on
   its merits, not its provenance — needs your confirm either way).

## Provenance

Evidence sweep: opus subagent, read-only, commissioned 12:2x CEST 2026-08-09,
69-incident ledger with file:line cites (coordination.md line numbers as-read
at ~15,099 lines; the file grows). Hand-verified before use: builder-method
coverage grep (0 hits), ship-gate.md:16 ("ZERO ships") and :57 (50-100×),
instrument-audit-2026-08-08-late.md:226-231 (ten slot changes),
elo_logger.py:98 (`net5 <= 0`), absence of any test runner (no CI dir, no
hooks, no crontab entry). Tape row-kind distribution sampled directly
(last 200: 56 verdict / 32 note / 25 baseline / 17 screen / 15 caveat …).
Monitor fleet verified live via `ps` at 12:21: keeper pid 13765 (up 3h31) +
four watcher loops (since 08-08 22:22). Builder self-report pending at
commit time; will be relayed as an addendum when it arrives.

---

## Addendum (12:5x CEST): the builder's self-report — labelled as such, verbatim in substance

The builder answered the three process questions (msg exchange 1658d201 →
reply). Recorded as self-report, not measurement; where it disagrees with the
sweep's evidence, both are stated.

**1. Wall-clock, the builder's ranking.** (1) **Rebuilding instruments that
should already exist** — in one session: a TLE census, a per-round CPU
decoder, a paired/pooled re-pricer, a replay-keeping battery runner. The
builder's headline, converging independently on the sweep's I34:
**`tools/arena.py` runs every match with `--replay /dev/null` — no local
battery in project history has ever produced a decodable replay**, so every
mechanism question was routed to the ladder corpus and waited hours. The
builder rates this one default as costlier than everything else combined.
(2) Boot reading — large but mostly defensible; the HANDOVER top block was
load-bearing within the first hour of s24. (3) Cross-lane message volume —
valuable (the COVER refutation saved a build) but roughly as expensive as
building, per the builder's own guess. (4) Wrap — cheap exactly when deltas
were appended inline. (5) Pre-registration — ~10 min, paid back same-day.
Note the divergence from the review's assumption: battery babysitting is NOT
a top cost (one command, ~6 min return).

**2. What gets skipped under pressure, the builder's own list.**
(a) Process-delta-with-the-verdict, "every time" — the builder confirms this
is why wrap is expensive and why delta-zero ×3 exists. (b) Verifying a peer's
number against primaries when the reasoning looks sound — the exact inversion
the protocol warns against. (c) Same-day instance: ran `md5 main.py` on
multi-file bots — the trap named in the builder's own read-first doc §8 —
and was one message from publishing a false "three planks never tested"
conclusion; the verification step caught it. The builder's summary of its own
failure mode: *the rule I skip is the one in my own read-first document,
about the tool I am using at that moment.* This is the strongest first-person
confirmation of the review's §3 (surface-dependent half-life) on record.

**3. The pending decision is now MADE: adapt-trimmed.** The builder adopts
the forcing functions (S5 tape fields, `preflight.py` as an exit-code gate
wired into builder.md) and explicitly declines the S0–S8 prose pipeline,
with a rationale the review endorses and §3 predicts: *"a rule that is
documented and not followed is worse than an absent rule, because it makes
the record look like a process we're running."* If a stage cannot be
expressed as an exit code, it does not get written down. — This closes the
s23 open item (test-process adopt/adapt).

**Follow-ups claimed by the builder:** a `random.`-call grep added to
`gate.py`'s determinism check (found: `rush_probe` makes 10 `random.` calls
in its hot path while the exclusion list names only `cad_probe`); the
`--replay /dev/null` default; the builder-method.md maintenance pass going
forward (on top of §10/§11 as landed in 5312e92). The builder also
independently endorsed the slot-as-stop-loss re-scope before reading the
implemented amendment ("at ±18/match, eight matches cannot evaluate
anything").
