# BUILD REPORT — `bots/_v514ferrycrew` (Magnus rulings 1+2, autopsy fixes, relay port), s51 2026-08-18

*Banked by the builder s51 from the opus build agent (agent's draft, builder-ratified framing).
Parent `bots/_v513siegecrew` FROZEN (read-only throughout). Master flag `LOKI_FS_V514`; False
reproduces the parent. Diff vs parent: doctrine +214, siege +746, main +71, eco +8, raid +10.
**2,166 local games, 0 tracebacks.** All grids `--tle 10`, PAR=4, vs `bots/_v488beltbreak2`
unless stated. Artifacts: `scratchpad/s51_v514_build/` (grids, arms via mkarm.sh, mechanism
logs, runner).*

## ⛔⛔ TWO FINDINGS THAT OUTRANK THE PLANK

**1. THE COMPOSITE AS SPECIFIED MEASURES NEGATIVE; CHANGE A (RULING 2 AS LITERALLY ENCODED) IS
THE DOMINANT TERM.** Single-flag isolation (n=60/arm, same seeds; control = master ON, all four
sub-flags OFF = 37/60): A-only **23/60** (re-draw 27/60); A-only with the magazine left on
v513's salt gate 32/60; B-only 37; C-only 33; D-only 32. Mechanism (surprise 3): **the
2-connected-harvesters condition is satisfied at r7-24 on 4 of 5 maps — in practice change A
REMOVES the turret gate rather than re-timing it**, reproducing v510's unguarded-turret failure.
The eco stands up faster than the ferry finishes. If a re-timing is wanted the lever is the
harvester minimum / a round floor / a delivery-count bar, not the mechanism.

**2. THE GATED-MAP CRATER IS v513's DOOR-TURRET RESPONSE (change B, `FS_HOME_TURRET_RESPONSE`),
ISOLATED EXACTLY — AND THE REGISTERED FIRST SUSPECT (C/H CHASSIS) IS REFUTED.** archipelago
(plank never runs), n=36/arm, same seeds, vs `_v468kladturbo`: v512 **26/36 (72.2%)** · v513
**13/36 (36.1%)** (reproduces the shard's direction) · v513+door-off **26/36 — exact recovery,
digit for digit** · v514 with C+H off 13/36 — no recovery. Pooled gated n=60/arm: v512 39,
v513 23, v514 26, B+C+H-off 42; v513-vs-v512 −26.7pp exceeds the 17.9pp half-width.
**AND the flag swings the siege maps for v514 too**: v514 as delivered 36/90 → **53/90 with
door-off** (+18.9pp, outside the 14.6pp interval), while the parent is indifferent (51→50).
Untested mechanism hypothesis (labelled a guess): door pecks spend home actions + 2 Ti/peck
from a bank v514's earlier turret has already tightened. The flag ships at the parent's True —
disabling an inherited shipped plank is Magnus's call (it is HANDOVER decision item 6, which
now carries two measurements).

## HEADLINE — 5 siege maps × 6 reps × 3 blocks, n=90/arm, paired seeds, FIRED config
⚠ Gated-map regression INVISIBLE here by construction (siege maps only). Parent row is a
CONCURRENT re-run (banked 49/90; re-run 51/90 — vintage stable).

| | v514 as delivered | **v514 + door-off** | v513 parent | v514 flag-off | all-sub-off |
|---|---|---|---|---|---|
| WINS | 36/90 (40.0%) | **53/90 (58.9%)** | 51/90 (56.7%) | 48/90 | 56/90 |
| kills ≤ r300 (ITT) | 12/90 | **27/90** | 25/90 | 28/90 | 31/90 |
| our core destroyed | 51 | 33 | 36 | 36 | 33 |
| median kill round | 309 | 233 | 218 | 250 | 280 |

v514-as-delivered vs parent: −16.7pp wins, −14.4pp k≤300 — **real negative, outside the
interval**. Door-off vs parent: within noise. Same-config draw swing on this fixture: 4/60;
block swing up to 10/30. H2h vs parent as opponent: 33/60.

## Per-change verification (all mutants driven; full table in the agent transcript-of-record)
A: 0/13 purchases with conn bit clear vs bypass-mutant 11/16 pre-condition ✅; **sentinel now
exists in 11/15 mechanism games incl. atoll 3/3, midgard 2/3 (v513 fired: 0/12 on those maps)
— the headline mechanism** ✅. B: resite median d²=9, 2/43 same-tile vs mutant median 0,
97/119 same-tile ✅; 57/57 deaths detected vs mutant 0 ✅; 0 post-loss builds on observed rays ✅.
C: denial counted (covden 26 midgard) but evictor reaches **1 of the 4-seat ceiling** — reach
bug, see surprise 4 ⚠; collar STILL never closes on atoll/midgard ⚠. D: one-writer-per-slot
kills the r10 self-promotion (0/15 vs 15/15 in the two-writer mutant — the probe's r197
signature); arrivals b1/b2 r9-16 off-midgard, gap ≤2 in 12/15 ✅; two-rider links 46/129 vs the
probe's 78/78 (probe sacrifices not shipped — seat 3 kept, LOKI_FERRY_ON kept) ⚠.
Flag-off: structural (29 sites conjoined with the master; 3 equivalent-by-inspection rewrites
named for audit) + behavioural n=90 (48/90 vs parent's 51/90, inside swing).

## "Connected", as detected, and its failure mode
`conn` := SLOT_HARVESTERS ≥ 2 AND a MOUTH (friendly conveyor on a core delivery seat facing
the footprint, or splitter); `deliv` := the mouth seen holding a stack ≥ once
(FS_SENT_DELIV_REQ=True). Does NOT prove both harvesters are routed (v513 open item 5,
`_wire_tick` orphaning, untouched) — **the gate errs toward opening**, measured open r7-24.
Published on SLOT_ECO_READY (was 3-writes-0-reads DEAD in the parent) with the Core as sole
writer.

## Deviations (measured)
1. **FS_V514_MAGGATE=False ships** — magazine keeps the salt rule, only the turret moves to
   the eco gate (onlyA 27/60 coupled vs 32/60 decoupled; a KILL-phase floor drop at r24-40
   with an open collar converts the collar's bank into pre-seal fire). New phase
   FS_PH_KILL_OPEN=5.
2. `_fs_denied` had NO launcher clause in the parent (the brief's "verify it" premise was
   false) — added in `_fs_census`; first form wrong (dropped covered seats from the work
   queue), corrected (onlyC 30/60 → 33/60): coverage removes a seat from orth_open, leaves it
   in the work queue; counts only enemy-building-occupied seats.
3. Relay ships without the probe's sacrifices → two-throw compliance 36% vs probe 78/78;
   FERRY_HOME_ON reassignment inert in fired config.
4. FS_CREW_ON stays False; FS_CREW_CONVERT untouched/unmeasured; D largely inert in fired
   config except FS_HOP_RING_FIRST.
5. midgard hold-station candidate NOT attempted (budget went to the composite regression).
6. C/H kept strictly flag-severable; measured worth ~+14 games/90 on siege maps, ~0 gated.

## Surprises
1. Gated regression = door-turret response, exact isolation (above).
2. Door response free for parent on siege, −17 games for v514 there — interaction real,
   mechanism a guess.
3. Magnus's gate opens r7-24 — not a gate as encoded.
4. **The evictor can only ever SEE 4 tiles** — `_fs_try_evict_launcher` scores only the tiles
   orthogonally adjacent to wherever the raider stands; no siting objective reaches the
   4-seat ceiling until `_fs_stand_target` prefers stations whose neighbour is the
   max-coverage tile. Reach bug, not preference bug.
5. Two-writer defect reproduces r10 in 15/15 with relay off — one writer per slot removes it.

## Open items
1. **FS_HOME_TURRET_RESPONSE — Magnus decision, now with two measurements** (gated +36pp on
   parent; siege +18.9pp on v514; free for parent on siege). Changes how the SIEGECREW tape
   reads.
2. **Change A re-timing** — Magnus's ruling measured −14/60 as encoded because it opens too
   early; lever = a real bar (harvester min / round floor / delivery count).
3. midgard unmoved (1/18 all arms; belted seats, launcher can't throw buildings).
4. Evictor reach (stand-target preference) — unbuilt.
5. Platform CPU `match test` owed before any ship talk (v514 adds per-round core seat scan).
6. FS_CREW_CONVERT + midgard first-envelope residual still open.

## BUILDER VERDICT LINES (s51, typed by the lane)
* v514 AS DELIVERED: REAL NEGATIVE on the siege grid (−16.7pp vs parent, outside interval) —
  not a candidate.
* v514 + door-off: parity with parent on siege maps + the gated recovery — **the live
  candidate config**, pending Magnus on the door flag and on change A's re-timing.
* The door-turret isolation REFUTES the chassis-drift (C/H) suspicion registered in
  siegecrew-final — correction row appended to results.tsv.

---
*DATED NOTE (s51, later the same session): the door-off magnitude in finding 2 (+18.9pp at
n=90) re-measured at +7.1pp (n=450) / +5.3pp (n=630) in the v515 build's interleaved arms —
SIGN CONFIRMED, MAGNITUDE ~40% of banked. Same session also quantified the fixture's one-draw
spread (±9/90 same-config): this report's naive intervals were the right ones; treat its point
estimates as regressing. See BUILD-REPORT-v515ecosalt-2026-08-18.md findings 1-2.*
