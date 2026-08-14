# Counter router v2

Local-only challenger to deployed v141 (`bots/counter_router_v1`). It keeps the
same two-policy strategy, isolates modules under `n_*` / `o_*`, and selects a
deterministic spawn-order residue from the exact FNV-1a terrain fingerprint.
It does not inspect opponent identity or match outcomes.

Candidate discovery used a balanced eight-salt full-map sweep plus an
exhaustive 97-residue search on four initially resistant maps. The assembled
router was evaluated separately on non-overlapping seeds:

- Screen: 157-23, 87.22%, 180 games, zero errors
  (`counter_router_v2_screen`, seeds 23001-23006).
- Independent confirmation: 214-26, 89.17%, 240 games, zero errors
  (`counter_router_v2_confirm`, seeds 24001-24008).
- Combined: 371-49, 88.33%, 420 games.
- 10 ms safety matrix: 30/30 completed, zero errors
  (`counter_router_v2_tle10`, seed 25001, both player positions).

The user-supplied baseline artifact
`submission-6de0d8c0-c280-437d-8867-a6f5d53392ee` was verified identical to
`counter_router_v1` after normalizing line endings. A further artifact-specific
confirmation scored 209-31 (87.08%) over 240 fresh games with zero errors
(`supplied_baseline_v2_confirm`, seeds 37001-37008).

This candidate has not been submitted, uploaded, activated, or deployed.
