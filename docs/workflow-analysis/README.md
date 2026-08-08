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

## Entries

| # | date | question | headline |
|---|---|---|---|
| [v1](v1-2026-08-08-measurement-power.md) | 2026-08-08 | Can cheaper models build incrementally better bots? | Not yet — the standard n=120 leg has **19% power** at +5pp, on a machine that is ~95% idle. The blocked-estimator fix I expected to be the lever measured **1.06x**. |
| [v2](v2-2026-08-08-gate-vs-ladder.md) | 2026-08-08 | Does the local gate predict ladder Elo? | **Unanswerable on the current tape — 4 joinable ships, not 35.** Gate rows key on bot dir, ladder rows on version; the join was never recorded. One extra column fixes it. |
| [v3](v3-2026-08-08-swap-rule.md) | 2026-08-08 | What are the slot-swap rule's error rates? | **It is a timer, not a control.** A truly neutral holder trips it 50.4% at match 8, 96.6% by 20. A genuinely +60-Elo bot still trips it 78.6%. Post-trigger Elo is **positive**. Fix is a magnitude threshold at −1 sd, which keeps the one real rollback and kills both overridden ones. |
| [v4](v4-2026-08-08-map-pool.md) | 2026-08-08 | Does our local map pool match the ladder's? *(measured by the research arm)* | **Clean null — 100% of 2,891 archived ladder games are on local maps, drawn near-uniformly.** Closes a v2/v5 hypothesis; discharges `program.md`'s maps-are-ours warning; and forces the **A6** split: raising n works for stochastic confirms, and cannot work for deterministic screens. |

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

  **All three were caught by having an independently-derived number to
  contradict them — redundancy, not diligence.** That is an argument the
  two-arm structure works because the arms measure *overlapping* things, not
  because they partition cleanly. Worth weighing against the protocol's
  disjoint-surface design before anyone optimises the overlap away.

## Scripts

- `paired_vs_pooled.py` — runs the arena grid once, scores it pooled-binomial
  (what `arena.py`'s accept rule uses) and blocked-on-(map,seed), and reports
  the CI-width ratio plus the between-map variance decomposition. Read-only.
  `python paired_vs_pooled.py bots/<cand> bots/<opp> <seeds> <jobs>`
