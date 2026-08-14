# SCREEN PREREG — SEALREPAIR: SEALFLOOR0 + L4REPAIR on the v139 chassis

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14,
on Magnus's direct instruction ("maybe a MAPSEAL + L4REPAIR?"), which jumps
the queue. **Deviation noted as with MAPSEAL: the house combo rule wants
finaled singles; SEALFLOOR0 is at 56.1/n=1716 and L4REPAIR2 at 54.6/n=1011,
neither finaled.** Attribution at read time against both singles' finals.

## Arm and control (class rule applied: chassis-matched on the LIVE incumbent)
* Treatment `bots/_v223sealrepair` = the v139 tree + `LOKI_SEAL_TI_FLOOR
  12→0` + the LOKI-L4 trunk-repair machinery (patch-applied from
  `_v215l4repair`'s diff; verified vs the v139 tree: 66 doctrine + 173 eco
  lines, main/raid untouched, `_l4_repair` present, floor=0, map strings
  identical to v139's).
* Control `bots/_v218mapfix` (v139). Both sides carry the map correction —
  the contrast isolates seal+repair jointly on the corrected chassis, so a
  positive final IS ship-shaped without re-basing.

## Interaction prior (declared)
Seal (raid-side, enemy core, barrier budget) and repair (eco-side, home
trunks, conveyor budget) are structurally disjoint; the shared resource is
the titanium bank, thinned from both ends (floor-0 seals + repair spends).
Suppression, if any, should appear as under-performing BOTH singles.

## Design
`SEALREPAIR` vs `_v218mapfix`, **full 15-map POST-PATCH pool** via
`overnight_pool26.sh` + the pool26 map dir (v139-era fixture; pools with
MAPSEAL's era only in map-geometry terms, never in shares — different
control). n=5400, seed_lo 268000, futility gates per RULE-futility-gates,
OB-F band 48.67–51.33. D26: replicate iff |final−50| ≥ 2.0pp (seed 269000).
Kill-round paired-seed rides. MAPSEALX7 cancelled on Magnus's call (rows
kept, n≈800, its subject v137 no longer holds any slot) — this shard takes
the freed capacity.

## Read rules
1. Pooled share vs the band; per-map splits (the 13 unpatched maps carry
   most of the contrast; on the 2 patched maps both sides navigate
   correctly, isolating seal+repair there too).
2. Attribution: vs SEALFLOOR0's final (13-map comparable cells) and
   L4REPAIR2's final; combo below best ingredient = suppression finding.
3. Coupling: seal = validated-asset tuning (s30 ablation transferred);
   repair = self-knowledge/logistics with an era-dependent dose (belt-cut
   rate is opponent-driven — mild coupling, stated). Ship path through the
   live surface per FIXTURE_OF_RECORD; SHIP_SIT governs (v139 sitting).

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
