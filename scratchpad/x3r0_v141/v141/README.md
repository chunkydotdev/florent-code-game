# Counter router v1

Local-only challenger to `bots/multisalt_v2`. It preserves the two-policy
v137 wrapper but isolates its modules under `l_*` / `m_*` and selects a fixed
spawn-order salt from an exact FNV-1a terrain fingerprint. The router uses no
opponent identity or runtime match outcome.

The salt table was selected from two independent eight-salt sweeps, each
covering all 15 official maps in both player positions. It was then evaluated
as one assembled bot on fresh seeds:

- Screen: 152-28, 84.44%, 180 games, zero errors
  (`counter_router_v1_screen_fixed`, seeds 18001-18006).
- Independent confirmation: 196-44, 81.67%, 240 games, zero errors
  (`counter_router_v1_confirm`, seeds 19001-19008).
- Combined: 348-72, 82.86%, 420 games.
- 10 ms safety matrix: 30/30 completed, zero errors
  (`counter_router_v1_tle10`, seed 20001, both player positions).

This directory has not been submitted, activated, uploaded, or deployed.
