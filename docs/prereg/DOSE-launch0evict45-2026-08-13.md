# DOSE PREREG — LOKI-EVICT (#45, iteration 3): pre-built launcher as standing feeder-eviction

**Committed before any dose game (two-clock: this commit's git author time vs
run wall clocks in the readout).** Builder s37, 2026-08-13. Chain:
iteration 1 (`DOSE-feeder45`) — sentinel-only exposure, dose not met;
iteration 2 (`DOSE-siegelaunch45`) — reactive waiver provably cannot fire,
the sieged economy is the binding gate. ⇒ The launcher must EXIST before the
siege. Side lane's carry adopted as the bar's construction; research's
feed-interruption note carries forward as the next-stage metric.

## The plank

`bots/_v201launch0evict` = incumbent `_v197mapcode` + `LAUNCHER_MIN_RND
160→0` (one constant) + the `EVICT45` tag on the pre-existing exile path.
Replication-by-rule: the RULE from the LAUNCH0 screen (52.77 ±1.33 at
n=5408, cited as prioritising grounds only — D26 line owed if a ship case
ever leans on it), applied to the CURRENT incumbent, not the v161-era tree.
Bank at r0 is 500 vs a ~24 Ti launcher, so the iteration-2 binder (bank
never reaches price under siege) is bypassed by construction.

## Bars

Fixture `bots/_probe_creeper` unchanged (frozen). 8 games × {midgard,
frostgate}, seeds 993001-8, kept replays, per-tag `strings` counts.

1. **VALIDITY:** CREEP45 in ≥6 of 8 games per map.
2. **DOSE BAR (round-stratified by construction, per the side lane): `EVICT45
   at r<160` ≥1 in ≥half of games with CREEP45 plants.** The incumbent CANNOT
   build a launcher before r160 at all, so any r<160 eviction is
   treatment-caused with no waiver bookkeeping. r≥160 EVICT45 is reported but
   does not count toward the bar. **FALSIFIER: 0 r<160 EVICT45 across all
   valid games ⇒ the pre-built launcher still does not evict** — candidate
   causes in check order: (a) launcher never built even at MIN_RND=0 (other
   gates — SLOT latch, harvester<1, reserve 80 — check GATE-free arithmetic
   from the end-card/replay); (b) launcher built but feeders never inside
   pickup d²≤2 (siting mismatch: launcher sits by our core, ladder lands at
   d²≤5 of core — measure the gap); (c) exile path preconditions.
3. **TAG-ATTRIBUTION CONTROL (2 games, frostgate): a scratch copy with
   `LAUNCHER_MIN_RND=160` restored and the tag PRESENT** must print 0 r<160
   EVICT45 (r≥160 legacy throws disclosed, not violations).

## Not licensed

No currency claim. If the dose bar is met: corefill screen `LAUNCH0EVICT` vs
`_v197mapcode` (the scale-surcharge cost of the early launcher is exactly
what the screen prices; LAUNCH0's 52.77 says the premium was affordable in
its era, this screen says whether it still is), then the pinned live leg
with its own prereg. If the falsifier fires on (b), the next lever is
launcher SITING, not timing.

---

## READOUT (clock = this commit's git author time; runs 17:34:41-17:35:04Z,
## bar-3 control after; replays scratchpad/feeder45_dose/l0e_*, l0eoff_*)

**⛔ FIRST, A CITATION CORRECTION THAT OUTRANKS THE RESULT — research's HOLD,
which raced this dose and lost by minutes: THIS PREREG CITES LAUNCH0
BACKWARDS.** `LAUNCH0` = `_v161launch0` = **`LAUNCHER_CAP=0` — the
NO-launcher arm** (its own positive control: 0 throws in 12 games). Its
52.77% is the no-launcher arm WINNING; the family reads launcher premium =
LAUNCH0−BOTH0 = **+6.34pp for NOT paying**, earlier = monotonically worse,
reserve ablation negative. **Unconditional pre-build is screen-OPPOSED in
unsieged pooled games, not screen-backed.** The "replication-by-rule" framing
was therefore replication of a MISREAD rule — the constant I changed
(MIN_RND 160→0) was never LAUNCH0's constant. The dose below survives as
MECHANISM evidence only, and the arm does NOT proceed to a screen.

**BAR 1 — VALIDITY: PASS** (CREEP45 in 15/16; the one 0-plant game is the
treatment's own doing, see below).

**BAR 2 — r<160 EVICT45, as registered: NOT MET POOLED, MET ON FROSTGATE.**
Frostgate: 6 of 8 valid games evict (9-48 evictions/game). Midgard: 0 of 7
valid games. Pooled 6/15 — under ≥half. **FALSIFIER (0 everywhere)
DEFINITIVELY NOT FIRED: the road iteration 2 proved shut is OPEN when the
launcher pre-exists.** All 205 evictions are r<160; r≥160 = 0 everywhere.

**⚠ DENOMINATOR DEFECT IN MY OWN BAR, named for the next prereg: midgard
seed 993003 shows 18 evictions and 0 CREEP45 plants — the mechanism's
STRONGEST game (feeders evicted before they could ever plant) is EXCLUDED
from the bar's denominator because the bar conditions on plants, an outcome
the treatment suppresses.** A validity denominator must be a PRE-treatment
quantity (e.g. enemy builders entering our half), not a post-treatment one.
Collider by construction; the bar verdict above is still reported as
registered.

**BAR 3 — TAG-ATTRIBUTION CONTROL: PASS.** MIN_RND=160 restored, tag
present, 2 frostgate games: 0 r<160 EVICT45, 0 r≥160, plants 3/3.

**VERDICT (mechanism): a pre-existing launcher evicts point-blank feeders at
0 ammo, repeatedly, and in the best case prevents the ladder from forming at
all. The COST side is research's verified family read: paying for launchers
is expensive in pooled unsieged games.** ⇒ The two results point at exactly
research's combined row: **CONDITIONAL pre-build on APPROACH detection**
(build when creepers walk in, before the bank drains — iteration 2 proved
detection machinery fires), with the premium as the named hazard and
unsieged non-regression as a bar. `_v201launch0evict` goes no further;
iteration 4 builds from research's row when it lands. Map split noted for
that row: eviction fired on frostgate (small) and not midgard (900-area) —
launcher siting vs creep path likely differs by map class; worth a stratum
in the row's bars.
