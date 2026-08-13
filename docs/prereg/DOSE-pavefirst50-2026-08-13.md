# DOSE PREREG — #50: conditional pave-first (Magnus's split, field-backed)

**Committed before any dose game (two-clock per readout).** Builder s37,
2026-08-13. Basis: research's #50 signature cut (top three teams pave-first
100%/99.6%/100%; we are 99.7% harvester-first, the outlier, n=7,169 sides)
+ Magnus's conditional, verbatim in spirit: a FORWARD spot must be claimed
fast; a NEUTRAL/BACK spot is set up faster through the belt.

## The arm
`bots/_v211pavefirst` = incumbent + `LOKI_PAVE_FIRST`: the pave-trail gate
(`SLOT_HARVESTERS >= 1`, eco.py:773) is waived when the walk target sits on
OUR half (symmetry anchor `enemy_core_for`); forward ore keeps
harvester-first. Tag `PAVE50` on each waived pave.

## Bars (fixture `_probe_sitter` — the opening is opponent-independent;
## 4 games × {midgard, frostgate}, seeds 996001-4, kept replays)
1. **DOSE:** PAVE50 ≥1 in ≥half of games AND the wire signature flips: our
   first CONVEYOR build round < first HARVESTER build round (autopsy events)
   in those games; the control (incumbent, same seeds) must stay
   harvester-first in ALL games (its 99.7% corpus signature, reproduced
   locally). FALSIFIER: 0 PAVE50 everywhere ⇒ gate/side-test wrong —
   instrument first.
2. **MECHANISM DIRECTION (reported, not a bar):** first-delivery round vs
   control per research's caveat — the authoritative latency read needs
   bank_trace per-round collected state and stays with research's cut.
3. **OFF-BRANCH (2 games):** flag-off copy, tag present: 0 PAVE50, signature
   stays harvester-first.

## Screen
`PAVEFIRST` vs `_v197mapcode`, n=5400, seed base 234000, queued at commit.
D26: replicated iff |share−50| ≥ 2.0pp, second shard 235000, scored alone,
same-side pooling only. Kill-round paired-seed non-regression rides along
(economy openings can shift kill timing; the bar catches it).

---

## READOUT — FALSIFIER FIRED, AND THE DIAGNOSIS RE-SPECIFIES #50

**Bar 1: 0 PAVE50 in 8/8 games; signature stays harvester-first (h r4-8,
c 2-3 rounds later) — as registered, instrument first.** The instrument is
fine; the PREMISE is absent: **harvester #1 lands at r4-8 because first ore
is near-adjacent on these maps — there is no walk for the pave gate to act
on.** The side-conditional pave-gate arm addresses a geometry that the
opening rarely presents.

**What the field's 100% pave-first signature must therefore mean: LOCAL
wire-first — the belt terminus is built BEFORE the harvester even at
close ore.** Geometric fact derived en route: an acceptor tile for site bp
is never orthogonally adjacent to the builder position that can build bp, so
wire-after always costs a repositioning (our c-h gap of 2-3 rounds) and
wire-first costs the same rounds in the other order. The entire payoff is
1-2 unwasted stacks per harvester (first emission lands on a live belt).
Also noted: `_has_acceptor` counts the CORE — core-adjacent harvesters waste
nothing, so the fix's scope is non-core-adjacent sites only.

**ROUTED: back to research/#50 as a re-specification** — the arm is an
approach re-sequencing (build terminus two tiles out, traverse it — builders
walk over conveyors — then place the harvester), not a pave-gate flip.
`_v211pavefirst` goes no further; its screen slot (234000) is WITHDRAWN from
the worklist before start. The dose replays carry the local baseline (c-h
gap 2-3 rounds, 8/8 games).
