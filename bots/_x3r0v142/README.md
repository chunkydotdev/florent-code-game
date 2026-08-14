# Counter router v3

Local-only challenger to `bots/counter_router_v2`. It preserves the same
two-policy strategy, isolates modules under `p_*` / `q_*`, and selects a fixed
spawn-order residue using an exact FNV-1a terrain fingerprint. It reads no
opponent identity or match outcome.

Discovery used sparse full-map sweeps, exhaustive 97-residue searches on hard
maps, multi-seed searches on parity/unstable maps, and a 20-game deep midgard
finalist test. Fitting games are excluded from the headline evaluation.

Out-of-sample results against `counter_router_v2`:

- Screen: 162-18, 90.00%, 180 games, zero errors
  (`counter_router_v3_screen4`, seeds 34001-34006).
- Independent confirmation: 216-24, 90.00%, 240 games, zero errors
  (`counter_router_v3_confirm`, seeds 35001-35008).
- Combined: 378-42, 90.00%, 420 games.
- 10 ms safety matrix: 30/30 completed, zero errors
  (`counter_router_v3_tle10`, seed 36001, both player positions).

Twelve official maps are deterministic wins under the evaluated matchup;
antler, archipelago, and nordkap are 50/50 parity maps across swapped seats.

This candidate has not been submitted, uploaded, activated, or deployed.
