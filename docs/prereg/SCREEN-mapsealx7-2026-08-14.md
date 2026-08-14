# SCREEN PREREG — MAPSEALX7: the MAPSEAL combo vs x3r0's v137 (benchmark)

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14,
on Magnus's direct ask ("also run mapseal against X3r0's latest bot").

## What this is (and is not)
A **local head-to-head BENCHMARK** on the as-of-today live pool:
`bots/_v221mapseal` (v125 + corrected map tables + SEAL_TI_FLOOR 0) vs
`bots/_x3r0v137` (the pulled v137 artifact staged verbatim: MoE router,
b_=rc8.5/ECORAID default, c_=v134 on {drumlin, nordkap, glacierkeep}).
It is NOT the plank's verdict surface — `COMPARE_AGAINST:
previous_line_iteration` keeps MAPSEAL's verdict on the vs-v125 shard.

## Facts established pre-launch (this morning's tape)
* v137 has NO map correction: both chassis carry stale pre-patch tables
  (grep-verified). Its ROUTER is unaffected (stale-decoded runtime grid
  matched against stale-decoded WEAK_GRIDS — internally consistent), so
  routing works as x3r0 designed; the NAVIGATION carries the defect, and
  valkyrie routes to the b_/ECORAID chassis (not in WEAK_KEYS).
* Expected edges therefore: MAPSEAL should over-perform on valkyrie
  (corrected tables vs wall-walk) and glacierkeep; the other 13 maps read
  the chassis matchup (v125-family + seal knob vs the ECORAID family).

## Design
`MAPSEALX7`, **n=2700** (benchmark sizing, band ±1.88 at final), seed_lo
264000, full 15-map POST-PATCH pool via `overnight_pool26.sh` + the pool26
map dir (same era as MAPSEAL's vs-v125 shard; pools with nothing
pre-patch). Futility gates apply (GATE-1000 <48 stops buying precision —
"v137 is simply better here" is a legitimate early exit). Per-map splits
reported; per-map = per-chassis attribution on v137's side (router is
terrain-keyed, so map name → chassis for free).

## Read rules
Descriptive benchmark + per-map splits. No ship inference in either
direction (a local head-to-head between two experimental trees; the
eco-family's local-vs-live divergence caveat applies to v137's side of the
board — its README's own fixture class). Slot decisions stay Magnus's/x3r0's.

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
