# SCREEN PREREG — #51 aimed throw: `_v222aimthrow` (exile that kills)

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14.
Queue #51, re-specified by research's 483b5bcd decode: the exile loop is a
PERFECT denial engine (100.0% action-denial across 259 inter-throw
intervals) that converts to ZERO damage — modal pad d²=16 from our own
sentinel FACING AWAY, ammo parked at 24 (2 sentinel shots) while a
40-HP builder kill needs 3 (30 ammo).

## The arm (one mechanism: exiled victims die; two co-requisite legs)
`bots/_v222aimthrow` = v125 chassis + `LOKI_AIMEDTHROW_ON` gating:
* **raid.py exile sort**: throw sites ON a friendly sentinel's firing line
  (line computed from facing, r²≤32, single-tile — the sentinel shoots
  through obstacles by design) outrank all others; within/without the ray
  set, farthest-from-core ordering unchanged. Empty ray ⇒ byte-equivalent
  ordering to v125 (verified by unit check both ways).
* **main.py ammo**: floor 30 while a launcher is latched (SLOT_LAUNCHER)
  and any weapon exists — 3 sentinel shots = one exiled-builder kill.

## Dose evidence and the declared gap
Sort-key unit check both ways (on-ray promoted; empty-ray = v125 order);
imports/flag plumbing verified; flag guards make flag-off structurally
identical. **GAP, declared: no engine-level throw-to-ray dose pre-launch**
(a live exile needs an enemy builder at our launcher — opponent-dependent).
A kept-replay spot check (throw destinations vs sentinel rays, victim HP
after landing) is OWED at the read if the final is outside the band in
either direction, before any mechanism sentence.

## Coupling class (declared)
**OPPONENT-COUPLED** — exile frequency depends on enemy builders walking
into our launcher (the LOKI-19 arrival-precondition lesson); self-play
arrival rates differ from live. The screen is therefore harm-gate +
directional; a value claim needs the live surface per the s38 rule.

## Design
`AIMTHROW` vs `_v197mapcode`, standard 15-map pool (pre-patch era fixture,
consistent with concurrent shards, era-labeled), n=5400, seed_lo 266000,
futility gates per RULE-futility-gates, OB-F band 48.67–51.33. D26:
replicate iff |final−50| ≥ 2.0pp (seed 267000). Kill-round paired-seed
rides. Runner: standard overnight.sh via the filler.

## Not licensed
No ship implication (SHIP_SIT: v139 sitting). No claim on ferry-path
throws (the aimed change touches the EXILE block only).

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.

## AMENDMENT A1 (ADD-only, ~09:3xZ, side-lane flag pre-certified; shard at
## n<50, unread)
Explicit, not implied: this screen's contrast is v125-chassis vs
v125-control — correct for the MECHANISM read (chassis-matched; a v139
control would confound the map correction into it). **Any SHIP case
re-bases on the v139 chassis vs v139** — "beats the incumbent" cannot be
banked from this number.
