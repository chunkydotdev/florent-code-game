# SCREEN PREREG — mined ports: GBNS (C1/C5 ingredient) + L4REPAIR (S4)

**Committed before either shard's first heartbeat (two-clock).** Builder s37,
2026-08-14. Both planks ported from their v169-era trees onto `_v197mapcode`
by an opus agent (report in the session record; diffs match the original
plank footprints; flag-off controls driven to 0 both).

## Arms
* `bots/_v214gbns` — GBNOSHIELD (barrier on a visible enemy gunner's ray, no
  shield clause). Dose at port time: **fires in self-play (heart 12, hive 3,
  nordkap 1) and ZERO in 5 maps vs the creeper — the anti-ladder premise
  (mining C5) is DENTED at the dose level and is not claimed here; the
  self-play/general premise (C1's context) stands.** Screen = the general
  read.
* `bots/_v215l4repair` — L4REPAIR (rebuild cut conveyor trunks). Era-null
  VOID by fixture change (belts now die ~3/game in self-play vs ~0 in its
  era — the 9-game exposure cut, 2026-08-14). eco.py was byte-identical
  across the chassis gap, so this port is exact, not adapted. Dose at port:
  1-5 repairs/game self-play, flag-off 0. ⛔ Carries the #44 CPU caveat
  (local CPU instrument dead; platform chassis gate before any ship).

## Shards
`GBNS` seed 240000 · `L4REPAIR` seed 241000, both vs `_v197mapcode`,
n=5400, futility gates per RULE-futility-gates, D26 declared now: each
replicated iff final |share−50| ≥ 2.0pp (seeds 242000/243000, scored alone,
same-side pooling). Kill-round paired-seed reported for both.

## Not licensed
No combo claims (C1/C2/C5/C6 build only from finaled singles); no ship
implication (the hold governs); GBNS's anti-ladder story requires a
creeper-geometry dose fix before C5 is revisited.

## AMENDMENT A1 (ADD-only, 2026-08-14 ~08:3xZ — side-lane flag, s38 builder)
**The L4REPAIR shard declared above NEVER RAN.** The shard NAME collided
with a spent v116-era shard (`_v177l4repair` vs `_v169launchlate160`, seeds
125000+, finished 2026-08-13 01:32); corefill's launch-once marker from that
era silently blocked this prereg's line, and the name's TSV/board row
(51.28, n=5408) belongs ENTIRELY to the old experiment — attribute nothing
from it to the `_v215l4repair` port. **Renamed to `L4REPAIR2`** (same tree,
same control, same seed 241000, unchanged design); it launches on the next
free slot with a fresh marker/TSV. The coupling test's L4REPAIR prospective
prediction grades against L4REPAIR2's data only. Worklist-wide dup check
run: L4REPAIR was the only collision.
