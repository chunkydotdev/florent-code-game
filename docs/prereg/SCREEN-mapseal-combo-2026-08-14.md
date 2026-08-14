# SCREEN PREREG — MAPSEAL combo: MAPFIX + SEALFLOOR0 vs v125 (Magnus's ask)

**Committed BEFORE the shard's first heartbeat (two-clock vs first TSV row).**
Builder s38, 2026-08-14. **Run on Magnus's direct instruction** ("Could you
run a combo of MAPFIX + SEALFLOOR0 against v125?"), which jumps the queue.
**Deviation noted rather than hidden: the house combo rule wants FINALED
singles first** (MAPFIX is past GATE-1000 at 55.93/n=1012; SEALFLOOR0 is at
~55.0/n=778, pre-gate). Attribution therefore comes later: the combo's final
is read AGAINST the singles' finals when they land (best-ingredient
comparison, the COMBO/v9 pattern), never as a standalone ship case.

## Arm
`bots/_v221mapseal` = v125 chassis + exactly three knobs:
* the two corrected post-patch map strings (valkyrie + glacierkeep, byte-
  identical to `_v218mapfix`'s),
* `LOKI_SEAL_TI_FLOOR 12 → 0` (byte-identical to `_v219sealfloor0`'s knob).
Verified: 6 changed doctrine lines vs `_v197mapcode` (3 old/new pairs),
eco/main/raid untouched. Control `bots/_v197mapcode`.

## Interaction prior (declared)
The mechanisms are near-disjoint (navigation data vs a raid budget
constant); the eco-combo suppression pattern (three planks sharing eco/raid
paths) does not apply structurally. Positive interaction is plausible on the
two patched maps (better navigation delivers raiders that then seal more).

## Design
`MAPSEAL` vs `_v197mapcode`, **full live 15-map pool on POST-PATCH geometry**
via `tools/overnight_pool26.sh` + isolated map dir (post-patch valkyrie;
`maps/` stays frozen for the concurrent shards — their era is pre-patch and
must stay internally consistent). This makes MAPSEAL the FIRST shard on the
as-of-today live pool; its numbers are era-labeled post-patch and do NOT
pool with any pre-patch shard, including MAPFIX's own 2-map screen and
SEALFLOOR0's 15-map pre-patch screen. n=5400, seed_lo 262000, futility
gates per RULE-futility-gates, OB-F final band 48.67–51.33. D26: replicate
iff |final−50| ≥ 2.0pp (seed 263000). Kill-round paired-seed rides.

## Read rules
1. Primary: pooled T-share vs the band; per-map splits reported (the two
   patched maps carry the MAPFIX half; the other 13 isolate SEALFLOOR0's).
2. Attribution at read time: combo vs each single's final (when landed) on
   comparable cells — the 13 unpatched maps vs SEALFLOOR0's final; the 2
   patched maps vs MAPFIX's final. A combo below its best ingredient is a
   suppression finding, not a ship case.
3. Coupling class: map half self-knowledge (full weight); seal half
   validated-asset tuning (s30 ablation transferred live). No live-haircut
   demotion applies, but the ship path still runs through the live surface
   per FIXTURE_OF_RECORD.

## Not licensed
No ship implication from this screen alone (hold + SHIP_SIT govern; the
correction-ship question is MAPFIX's packet, Magnus's call). No pooling
across geometry eras.

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
