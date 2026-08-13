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
