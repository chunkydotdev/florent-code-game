# The test pipeline: every instrument we own, in order, with skip-rules

**Side research lane, 2026-08-09, on Magnus's directive: "the builder keeps
forgetting unrated and test games — build a test process so we use all tools
available to us." PROPOSAL — the builder owns measurement and may adapt;
this formalizes what today's record shows we already paid for not having.**

## Why this document exists (two same-day incidents)

1. **ESCALATE**: D1's mechanism fired locally, but its r250 gate came back
   empty because the local pool is our own lineage, which never sustains a
   late multi-attacker siege — **the treatment condition cannot occur in the
   instrument that was used.** One unrated cycle (5 games, zero Elo) would
   have measured it against opponents who actually besiege. Unmeasured, not
   refuted, and a day's build produced no decision.
2. **SITE −6.7pp**: the day's largest effect was measured on the local
   arena, which this project REFUTED as a magnitude instrument (sweep 8's
   external corroboration: winners publish ~2× self-play inflation, with
   sign flips as tail risk). The number the queue now reasons from carries
   an uncorrected instrument label.

The pattern in both: **the local arena is frictionless and unrated has
ceremony, so local wins by default.** The fix is (a) an ordered pipeline
where the unrated stage is a named gate, and (b) removing the ceremony —
the scheduling constants that make unrated zero-cost are already measured
and just need to be in one place (§4).

## 1. The instrument inventory (measured properties, not vibes)

| # | instrument | answers | cost | hard limits (all measured, on the tape) |
|---|---|---|---|---|
| 1 | Rule arithmetic / engine docstrings | what CAN happen | free, instant | organisers' docs contain errors — verify against `fcode/` stubs |
| 2 | Engine probe (local `match test`) | one engine fact (boolean/number) | minutes | `match test` is local-vs-local — never an opponent-behaviour instrument |
| 3 | `tools/det.py` identity runs | refactor safety (0 flips = proof) | minutes | seed count ≠ sample size; det opponents must have NOISE_ON flipped in ALL sides; ~3 effective det opponents |
| 4 | Local arena, det pool | did the MECHANISM fire; ablation attribution; map-gated null-control seats | ~2,150 games/hr | **REFUTED for magnitude** (asserted v76>v84 at p=1e-11, ladder contradicted the sign). Dominated pool → near-zero backfire rate → "aggression is free" by construction. Load-sensitive: ONE battery at a time, subagents told "do not measure" |
| 5 | Local arena, punisher pool (`opp_v76`/`opp_v44`/`opp_v69`) | aggression questions the dominated pool cannot see | same | still our own code lineage — self-play inflation applies |
| 6 | **`fcode match unrated`** | REAL opponents: refutation vs the matched fixture; treatment-occurrence; production mechanism | 5 games/10 min ≈ 150/hr, **zero Elo** | plays the ACTIVE submission (→ needs the swap loop, §4); **can refute, can never confirm** (≥3-wins bar has 47% power at n=10; confirmation needs n≈40 ≈ holding the slot 4 gaps) |
| 7 | Ladder (rated) | the ONLY confirmation | Elo at risk | ship-gate rules; ~4-match hold minimum; keeper watches; rollback criteria pre-stated on the tape |
| 8 | Corpus production read (research arm) | did the mechanism run in production as designed | free, post-ship | needs replays to archive first; research-arm relay |

## 2. The pipeline (every build walks it top to bottom; skips are stated, never silent)

**S0 — PRE-REGISTER (before any code).** One block, filled in the build's
dev-dir README or the tape row: (a) what does this thing PRODUCE, and which
metric prices that product — currencies are output / denial / delivered-
objective / win-condition, **never survival or persistence** (sweep 8; the
SITE lesson); (b) the falsifier — what result kills it; (c) if the evidence
base is observational, the **placebo arm** — a treatment the hypothesis
says must point the OTHER way (the empty-tile control is the template);
(d) **the treatment-occurrence question: what game-state must occur for
this change to matter, and which instrument actually contains that state.**

**S1 — RULES.** Can this happen at all? (Free. The builder-bots-can't-kill-
builders check was available all day for the cost of a docstring.)

**S2 — ENGINE PROBE** if S0 assumed any engine fact not already probed.
One match, minutes. (Scale-decrement and `can_launch`-into-cell are still
open examples.)

**S3 — PARITY.** Flag OFF = byte-identical to parent (every rollback exact);
det identity run 0 flips where the change claims inertness.

**S4 — LOCAL MECHANISM BATTERY** (det pool, one battery at a time):
- Did the mechanism fire? (dispatch counts, metric movement)
- **Count the treatment occurrences.** If the triggering state occurred
  ~never, STOP: local cannot measure this flag — record "local:
  unmeasurable, pool lacks treatment condition" and go DIRECTLY to S5.
  (ESCALATE, named. This is a skip-rule, not a failure.)
- Every magnitude from this stage is written with the label **"local —
  direction only"**. A local magnitude may set priorities; it may not gate
  a ship or be quoted as an effect size.

**S5 — UNRATED FIDELITY PASS (the stage this document exists to protect).**
Hard rule: **no ship decision, positive or negative, on local numbers
alone — every build that reaches a ship decision has an unrated read or an
explicitly written one-line reason why not** (e.g. "pure refactor, parity
proof suffices"). The read itself, via the zero-Elo loop (§4): ship the
variant in a safe gap, fire the matched fixture, read the pre-registered
threshold, roll back. What S5 uniquely buys, per today:
- treatment-occurrence vs REAL opponents (does the state the flag targets
  exist on the ladder?)
- refutation at fixture baselines (v80 0-16 · v87 1-15 · Thor 1-9 on the
  hive fixture — pre-register the bar BEFORE firing)
- fresh replays of the variant vs real opponents → corpus → mechanism-in-
  production read without spending a rated match

**S6 — SHIP DECISION** per `docs/ship-gate.md` (parity + window + nothing
known-broken — unchanged). Tape row carries: baseline, rollback target +
bytes, pre-stated rollback triggers (magnitude-based, never sign), and the
S5 verdict line.

**S7 — FIELD WINDOW.** Hold ~4 gaps minimum (the confirmation arithmetic);
keeper armed; read at the pre-registered n, never at a favourable moment.

**S8 — PRODUCTION READ** (research arm): first class-relevant replays,
per-piece checks against the pre-ship baselines. Post-ship constants
re-extracted if the change touches early-game behaviour.

## 3. The forcing function (why this one won't be forgotten)

A checklist nobody reads is a log. Two mechanical hooks, builder's choice:
1. **The tape template.** The pre-ship tape row gains two mandatory fields:
   `S5_unrated:` (result, or the one-line skip reason) and
   `treatment_occurrence:` (local count / unrated count). An empty field is
   visible in a way a forgotten step is not — same design as the IN-FLIGHT
   registry, which works.
2. **`tools/preflight.py` (builder-owned if adopted):** ~30 lines — reads
   the dev-dir's pre-registration block, refuses to print the "ready to
   ship" line if S5 is empty, prints the current safe-gap countdown (from
   the :X2:43 schedule) so the unrated pass is one copy-paste away at the
   moment it's needed. The audit_trigger pattern, applied to shipping.

## 4. The zero-Elo unrated loop, operationalized (all constants measured)

The ceremony is the reason S5 gets skipped. It is four commands inside a
~4-minute window that recurs every 10 minutes:

- Scheduler is RIGID: rated slots at :X2:43 every 10.0 min (39 consecutive
  gaps measured); match completes ~:X8:30 → **safe gap ≈ 4:13, knowable in
  advance**.
- In the gap: `fcode submit <variant>` (auto-activates) → fire 5 unrated
  fixture matches (the 10-min rate limit) → `fcode submit <parent bytes>`
  (rollback needs no `activate`).
- Rated matches played by the variant: ZERO (validated 04:15-04:22 cycle,
  s22). Residual risk: a blocked rollback leaves the variant live ~1 rated
  match — real, bounded, on the tape.
- Batteries larger than 5: repeat across consecutive gaps (25 games/cycle
  ≈ 150/hr) or accept the fixture's n and pre-register accordingly.
- **While a variant is on unrated, the local arena is idle** — the two
  instruments don't contend; there is no throughput excuse.

## 5. Instrument-selection quick reference (tape a copy to the monitor)

| question | instrument |
|---|---|
| "can X happen?" | rules → engine probe (S1/S2) |
| "is my refactor inert?" | parity + det identity (S3) |
| "did the mechanism fire?" | local det battery (S4) |
| "does the triggering state even occur?" | count in S4; **if ~0, unrated (S5)** |
| "how big is the effect?" | **unrated direction first (S5), field for magnitude (S7). Local: never.** |
| "does aggression pay?" | punisher pool + unrated. Dominated pool: never. |
| "is it confirmed?" | ladder hold, ~4 gaps, pre-registered n (S7). Nothing else confirms. |
| "did it work in production?" | corpus read (S8, research arm) |

## 6. Immediately applicable backlog (the process, run on today's builds)

1. **ESCALATE → S5**: one unrated cycle vs siege-heavy fixture opponents
   (Lunds/CtrlAltDefeat/KCM are the measured besiegers) answers the r250
   gate that local structurally cannot.
2. **SITE → S5**: the −6.7pp magnitude is local; one unrated pass on the
   fixture re-prices the largest number in the current queue (prediction
   from the literature: it shrinks toward half; direction survives).
3. S2 backlog: scale-decrement probe; `can_launch`-into-cell probe.
