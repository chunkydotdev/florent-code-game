# workflow-analysis — how we work, measured

A numbered series of analyses of **our own process**, not the bot. Started
2026-08-08 on Magnus's ask ("how can we upgrade our workflow to build
incrementally better bots with cheaper models?").

## Why this folder exists separately

It is deliberately outside both arms' write surfaces (`docs/two-session-protocol.md`):

- **not `docs/research/`** — that is the research arm's deliverable set, and it
  is about the *game*. This is about the *loop*.
- **not `tools/`** — Magnus-gated and permission-blocked, correctly.
- **not `results.tsv` / `HANDOVER.md`** — builder-owned tape.

Anyone may write here. Findings that change how the loop runs get relayed to
the arms via session message; they decide what lands in their own surfaces.

## The house rule for this series

**A process claim gets measured or it does not go in.** The failure mode this
folder was created to fight is the one v1 found: analysis that terminates in a
document instead of a decision. If an entry cannot name a number and a
falsifiable prediction, it is a spitball note, not a workflow analysis.

Corollary, and v1 is the worked example: **when the measurement refutes the
author's own leading hypothesis, that refutation is the headline.** v1's
elegant fix measured 1.06x and is written up as "do not build this."

## Method, so the next one is cheap

1. **State the hypothesis and the number that would refute it, before running.**
   Write it down first — v1's was "blocking on (map,seed) tightens the CI 3-5x;
   under 1.5x refutes."
2. **Measure on a real comparison, not a toy.** Two live bot versions with a
   known-ambiguous tape row is the best case: you learn about the instrument
   *and* re-decide a real row.
3. **Read-only, scratch-first.** Diagnostic scripts live here or in the session
   scratchpad. Do not edit `tools/`, bots, or the tape to run an analysis.
4. **Cost the recommendation in wall clock, on measured throughput.** "Raise n
   to 800" is only actionable next to "= 22 minutes on 6 cores." Measure the
   throughput in the same run; do not estimate it.
5. **Check the load.** Other sessions may be running batteries. Cap workers
   (`ListAgents` first) so the diagnostic does not distort what it measures —
   and report the core count alongside the timing.
6. **Ground external claims in primary sources and state the precondition.**
   Most "cheap models work" results carry a precondition (a trustworthy,
   high-throughput verifier). Citing the result without the precondition is
   how a paper gets misapplied.
7. **Relay, then let the arms decide.** This folder proposes. Builder ships.

## The one-line summary of the whole series

> **Tonight we took the deterministic opponent pool from 1 to 6 and the
> screening ceiling from 30 to 180 — and all six are our own lineage. 180 more
> observations of ourselves does nothing about a −493 Elo bleed concentrated in
> four opponents we cannot instrument.**
>
> **The cheap axis and the valuable axis are different axes.** Every
> measurement fix in v1–v4 is on the cheap one. v5 is the valuable one.

## Entries

| # | date | question | headline |
|---|---|---|---|
| [v1](v1-2026-08-08-measurement-power.md) | 2026-08-08 | Can cheaper models build incrementally better bots? | Not yet — the standard n=120 leg has **19% power** at +5pp, on a machine that is ~95% idle. The blocked-estimator fix I expected to be the lever measured **1.06x**. |
| [v2](v2-2026-08-08-gate-vs-ladder.md) | 2026-08-08 | Does the local gate predict ladder Elo? | **Unanswerable on the current tape — 4 joinable ships, not 35.** Gate rows key on bot dir, ladder rows on version; the join was never recorded. One extra column fixes it. |
| [v3](v3-2026-08-08-swap-rule.md) | 2026-08-08 | What are the slot-swap rule's error rates? | **It is a timer, not a control.** A truly neutral holder trips it 50.4% at match 8, 96.6% by 20. A genuinely +60-Elo bot still trips it 78.6%. Post-trigger Elo is **positive**. Fix is a magnitude threshold at −1 sd, which keeps the one real rollback and kills both overridden ones. |
| [v4](v4-2026-08-08-map-pool.md) | 2026-08-08 | Does our local map pool match the ladder's? *(measured by the research arm)* | **Clean null — 100% of 2,891 archived ladder games are on local maps, drawn near-uniformly.** Closes a v2/v5 hypothesis; discharges `program.md`'s maps-are-ours warning; and forces the **A6** split: raising n works for stochastic confirms, and cannot work for deterministic screens. **A7b resolved by measurement:** 5/5 candidates verified deterministic (72 matches, all 3 controls correct) — det pool 1 → 6, ceiling 30 → 180. |
| [v5](v5-2026-08-08-instrument-coverage.md) | 2026-08-08 | What fraction of our Elo bleed has a valid instrument? *(measured by the research arm)* | **0.0%.** Four opponents carry **82%** of a −493 gross bleed; every one is uninstrumented, retired, disclaimed or invalid. Both valid probes point at opponents we **beat**. Composes with v1: a 19%-power battery aimed at a population contributing ~0% of losses. |

### The three rules these bought

- **v1:** when the measurement refutes the author's own leading hypothesis,
  that refutation is the headline.
- **v2:** **state what a null would mean before running.** If "no signal" and
  "signal we cannot see" produce the same output, it is not yet a study.
- **v3:** **state what a wrong parse would look like.** Three decoder faults in
  one evening (proto3 omitting `TEAM_A=0`; map identity colliding on
  dimensions; field 1 meaning `width` in `.map26` but a `Map` submessage in
  `.replay26`) were each **silent, and each produced a plausible table** — no
  exception, no empty output, just a confidently wrong number. One would have
  published as "0% of archived games are on local-pool maps."

  **All were caught by having an independently-derived number to contradict
  them — redundancy, not diligence.**

  **Precise tally (research arm's own correction, and it is less flattering to
  them than my first version):** five faults caught on 2026-08-08. **Four were
  the research arm catching its own work** by cross-checking against its own
  earlier measurements — that is redundancy *within* one arm. **Exactly one was
  a genuine cross-arm catch** (the research arm catching this session's
  selection-bias claim about the probe fleet). **None was caught by an author
  re-reading their own work unaided.**

  So the lesson is **not** "two arms". It is *"keep independently-derived
  numbers around to contradict new ones"*, which one agent can do alone — and
  four of five catches did. Two caveats keep the structure worth something:
  within-arm redundancy dies with the session's context, and an agent with a
  *systematic* error will reproduce it in both derivations, where a second arm
  will not. Within-arm redundancy caught more here; between-arm is the stronger
  guarantee in principle. And per the research arm: tonight's redundancy was
  **accidental** — clean partition would have removed it by design. **Overlap
  has to be deliberate either way.**
- **v5b:** **a prediction can be right about its conclusion and wrong about its
  variable.** The builder pre-stated that hive and drumlin would be where we are
  killed fastest. Measured: drumlin **is** #1 of 15 (212 turns), hive is **#6**
  (246, mid-pack) — but hive is where we are killed most *often* (74%). Kill
  **rate** correlates with win% at **r = −0.84**; kill **speed** at only
  **+0.34**. The prediction reached the right maps through the wrong mechanism,
  and a confirm-on-conclusion would have banked the wrong causal story. **Check
  a prediction's variable, not just its verdict.**
- **v5:** **the archive cannot answer questions about the era before it started
  collecting.** The replay archiver was a session-12 decision, so every
  retrospective question has a hard floor around 2026-08-07 midday — verified:
  the oldest archived file is 7 Aug 12:31, and `band_probe`/`flotte_probe` were
  built 08-06, entirely outside the corpus. **Unlike the parser faults, this
  produces no wrong number** — it silently answers a narrower question than the
  one asked, with full confidence. Check the corpus floor against the question's
  time range before running any "when did X start" study. (Minor caution: the
  tape stamps local time and match metadata stamps UTC, so the exact boundary is
  ambiguous by a couple of hours; `tooling.md` records a related `createdAt`
  trap. The floor is real either way.)
- **v4:** **absence of a noise flag is not evidence of determinism.** It is a
  measured property. `bots/starter` carries no `NOISE_ON` symbol and is
  documented as non-deterministic — the standing counterexample. Corollary
  found the same way: a distinct-shape count near 1.0 on a supposedly
  deterministic leg means **the precondition is violated**, not that the leg is
  well-powered.

## Scripts

- `paired_vs_pooled.py` — runs the arena grid once, scores it pooled-binomial
  (what `arena.py`'s accept rule uses) and blocked-on-(map,seed), and reports
  the CI-width ratio plus the between-map variance decomposition. Read-only.
  `python paired_vs_pooled.py bots/<cand> bots/<opp> <seeds> <jobs>`
