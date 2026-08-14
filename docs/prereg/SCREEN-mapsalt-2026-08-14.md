# SCREEN PREREG — MAPSALT: x3r0's per-map spawn-salt table on the v140 chassis

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14.
Provenance: x3r0's v141 "Counter Router v1" (analyzed on his own request,
Magnus relaying: "he would like us to analyse his bot and see if it's
something to use"). Identification (sonnet agent, scratchpad/x3r0_v141/
v141_id.md): the tree itself is pre-v139 (stale map tables, no v140 knobs,
RICH_TI=400 in one chassis) — NOT adopted. **The extracted idea: a fixed
per-map spawn-salt table** (terrain-fingerprinted; two independent
colour-swapped 8-salt sweeps; his combined screen 348-72 = 82.9% — against
his own multisalt bot, echo-loop caveat on the NUMBER, not the mechanism).

## Arm
`bots/_v225mapsalt` = v140 + the salt table replacing the OS-entropy salt in
the core's spawn ordering (main.py only, 0 diff elsewhere). Adaptations,
both verified: **glacierkeep RE-KEYED** to our corrected table's grid
fingerprint (2948331259; his key hashed his stale grid — silent-default
trap caught pre-launch), drumlin control key reproduced his exactly
(2309041557). Unknown maps keep the original random salt. Control
`bots/_v223sealrepair` (v140). Coupling class: SELF-KNOWLEDGE (map-keyed
constants) ⇒ screen-trustworthy, the MAPCODE-precedent class.

## Declared caveats
1. **Salt values were tuned on x3r0's chassis** (v135/v134-line spawn
   contexts). Transfer is plausible (shared lineage; same ordering
   arithmetic) but not guaranteed — if the screen is flat, a LOCAL sweep on
   the v140 chassis is the follow-up, not a road closure (his sweep method
   is sound; his values might not be ours). Scout-tier shaped if the tier
   exists by then.
2. **Noise structure: the treatment side becomes deterministic on known
   maps** (the salt was the chassis's only OS-entropy source — #15's own
   finding). Game variance survives via the CONTROL side's NOISE_ON salt;
   effective-n is bounded by control-side entropy and is NOT the naive row
   count. Stated here so the final's band is read with that in mind; the
   D26 replication (fresh seeds, seed 275000) is the guard that matters.
3. His README's 82.9% is vs `multisalt_v2` (his bot) — used as motivation
   only; no number from it is banked anywhere.

## Design
`MAPSALT` vs `_v223sealrepair`, full 15-map POST-patch pool
(`overnight_pool26.sh` + pool26 dir), n=5400, seed_lo 274000, futility
gates per RULE-futility-gates, OB-F band 48.67–51.33. D26: replicate iff
|final−50| ≥ 2.0pp. Kill-round paired-seed rides. Per-map splits are the
real read (a per-map knob should pay per-map; salted maps vs unsalted
maps is the internal control — the 6 all-zero-salt maps should read ~50).

## Not licensed
No ship implication (v140 sitting, k=1). No claim about v141-the-tree
(analysis delivered to Magnus/x3r0 separately). Credit: the mechanism is
x3r0's; this screen only prices it on our chassis.

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
