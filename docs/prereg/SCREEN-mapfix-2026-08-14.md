# SCREEN PREREG — MAPFIX: post-patch valkyrie + glacierkeep map codes

**Committed BEFORE the shard's first heartbeat (two-clock; side lane certifies
against the TSV's first row).** Builder s38, 2026-08-14, patch-driven (Magnus
reported the organisers' Aug-14 patch note; both changes verified on the wire
this morning: valkyrie sha OUTDATED locally, glacierkeep re-encoded from the
sha-current file differs from the shipped table).

## The defect being corrected (measured, not asserted)
`EXTRA_MAP_CODES` in the v125 chassis (`_v197mapcode/doctrine.py:1165,1170`,
byte-identical in x3r0's v134 artifact) disagrees with the live platform
terrain on BOTH 30x30 maps:
* **valkyrie, 10 tiles**: 8 near-core walls REMOVED (the patch note's
  "blocking builder bots near the core"), and **1 ore tile per side is now a
  WALL** — (6,14) d²=16 from core A, (23,14) d²=9 from core B. The stale grid
  feeds `_bfs_direction` (routes through the new real wall — the exact
  livelock class MAP_CODES exists to prevent) and `map_ores` (harvester
  planner targets a phantom ore tile beside the core).
* **glacierkeep, 9 tiles**: the center ore cluster (13-15,13 area) is gone;
  ore redistributed to (2,15)/(9,15)/(20,15)/(27,15). The bot contests a
  phantom center ore and ignores 4 real ore tiles.

## Arms
* Treatment `bots/_v218mapfix` — v125 chassis + the two corrected code
  strings, NOTHING else (`diff -r` = 2 lines in doctrine.py).
* Control `bots/_v197mapcode` — the stale table.
* **Dose evidence, both ways, run pre-launch:** decoding each tree's table at
  the four probe tiles: OLD reads valk(6,14)='o' (5,14)='#' glac(14,13)='o'
  (2,15)='.'; NEW reads '#'/'.'/'.'/'o' — each tree produces the other
  verdict at every probe.

## Design
* **Maps: valkyrie + glacierkeep ONLY**, POST-PATCH geometry, served from an
  isolated scratchpad map dir so `maps/` stays frozen mid-shard (three shards
  are mid-fill; `maps/glacierkeep.map26` already flipped at 07:01:09Z —
  boundary noted for their reads; `maps/valkyrie.map26` stays pre-patch until
  a shard boundary). Runner: `tools/overnight_mapfix.sh` (overnight.sh with
  MAPS/MAPDIR overrides + seed divisor 4, committed alongside this prereg).
  Games on the other 13 maps would pit identical trees — pure noise — hence
  the restriction.
* **n=2160** (540 cycles x 2 maps x 2 seats), seed_lo 250000, shard `MAPFIX`.
* Futility gates per RULE-futility-gates (GATE-1000 binds; 2700 exceeds
  target). Informative band at n=2160: **47.90–52.10**.
* Kill-round paired-seed rides along (the mechanism predicts faster kills on
  these maps via unblocked paths + real ore).

## Read rules / bars (declared before data)
1. Primary: pooled T-share on the 2-map pool vs the band, per-map splits
   reported (the two maps carry different defect mechanisms).
2. **OUTSIDE-ABOVE** ⇒ the correction is a real local positive on the changed
   maps; goes to Magnus as the v125-restore-target candidate (correction
   class, same family as the original MAPCODE ship). **The ship/slot call is
   his; the hold stance governs.**
3. **NULL/inside** ⇒ the stale grid costs nothing measurable locally: the
   correction demotes to hygiene (fold into the next natural ship), and the
   "stale map data is urgent" road closes at screen level.
4. Coupling class: **SELF-KNOWLEDGE (map data)** — screen-trustworthy at full
   weight per the s38 coupling rule; MAPCODE itself is the class's validated
   precedent (screened 73.27, paid +137 live).
5. #44 CPU caveat: chassis unchanged, table size identical — no new TLE risk;
   platform chassis gate still applies before any ship.

## Not licensed
No ship implication (hold governs; v135 currently holds the slot and is not
ours). No claim about v134/v135's live valkyrie/glacierkeep games — that is
the wire-prediction/decode lane's surface. No pooling with any 15-map shard.

## Target-value line (template requirement)
Local screen, zero live exposure ⇒ payout gate N/A.
