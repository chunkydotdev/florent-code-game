# STANDING RULE — corefill futility gates (Magnus, 2026-08-13 s37)

**Authorization, verbatim intent:** *"if it's really bad at around 1000 runs
we should drop it for now. If it's not well above the 50% line at 2700 runs
we drop it too… say it is at most a 50.5% win rate, that's probably not
helping us significantly. It COULD be together with a combo, but alone it's
not worth applying."* Committed BEFORE any gate on a currently-running shard
is read (two-clock: this commit vs the gate reads' wall clocks).

## The gates (per shard, read ONCE each when n first crosses the boundary)

* **GATE-1000 (n ≥ 1000): drop if share < 48.0%** (~1.3σ below 50 at that
  n). Label: `FUTILITY-EARLY`.
* **GATE-2700 (n ≥ 2700, halfway): drop if share ≤ 50.5%.** Rationale: the
  final's informative edge is 51.33; finishing above it from ≤50.5 at
  halfway requires the second half to run ≥52.2 — buying 2,700 more games
  for that tail chance loses to re-spending the cores. Label:
  `FUTILITY-ALONE`.
* **Ablation arms** (GUNAXIS0-style, where LOW means the flag helps): at
  either gate, if the reading already determines the DECISION (keep the
  flag), drop with label `DECISION-REACHED` — precision beyond the decision
  is not bought.

## What a futility drop is NOT

Not a refutation. Rows are KEPT; the arm's dose evidence stands; the arm
remains a combo ingredient candidate (Magnus's own carve-out) and may be
re-queued inside a combo or after a redesign. The OB-F final bands govern
VERDICTS; these gates govern CORE ALLOCATION. A dropped arm's record line
carries the label, the n, and the share.

## Enforcement

The builder is WOKEN at each gate crossing (session watcher `gate_watch`;
the wake carries the numbers, the builder types the gate decision — the
watcher never decides). Session-tied; the wake path is carried in HANDOVER
at wrap until the durable in-corefill version is built (the existing D2
instrument-debt item).

## Applied to the board at commit time (declared before reading)

COMBO (n≈3900, past both gates before the rule existed — grandfathered,
finishes); GUNAXIS0 (n≈2300, GATE-2700 pending — ablation clause applies);
APPRLAUNCH (n≈2250, GATE-2700 pending). Gates bind all future shards from
their first row.
