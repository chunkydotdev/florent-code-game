# BUILD REPORT — `bots/_v512ringladder` (reactive dodge + at-ring priority ladder), s50 2026-08-17

*Banked by the builder s50 from the opus build agent. Magnus's iteration 3: dodge-when-shot +
priority ladder (1 barriers / 2 evict / 3 clear-and-replace / 4 two sentinels outside the
ring). Parent `_v511sealonly`; flag `LOKI_FS_RING_LADDER` @ doctrine.py:2251 (False = v511,
verified); eco.py/raid.py byte-identical to parent; diff 63 lines main.py + 521 siege.py +
~180 doctrine. Census deltas (BELT-ON-SEATS-SURVEY) and P6 micro-probe applied in-flight.*

## Results — 5 maps × 6 reps × 2 pooled grids (n=60) vs `_v488beltbreak2`, local --tle 10

| | v512 (n=60) | v511 parent (n=30) |
|---|---|---|
| WINS | **22/60 (36.7%)** | 7/30 (23.3%) |
| — siege maps only (heart excl.) | 12/48 (25.0%) | 5/24 (20.8%) — within noise |
| — heart (now map-gated → incumbent play) | **10/12 (83%)** | 2/6 |
| our core-kills | 20 | 6 |
| kills ≤ r300 | **7/60** | 1/30 |
| r1000 (programme defeats) | 5/60 | 2/30 |
| orthogonal-8 CLOSED | **8/60 (13.3%)** ⛔ regression | 9/30 (30.0%) |
| full-seal rounds | 879 | 2,069 |
| seats cleared AND barriered | **39** (midgard 17; closures 3/12 vs 0/6) | 5 |
| raider sentinels built/alive/core shots | 68 / 34 / **2,913** | 3 / 3 / 84 |
| games with ≥2 sentinels | 19/60 | 0/30 |
| evictions (≥6-tile dumps) | 311 (68.8%) | 71 (64.8%) |
| ring deaths per body-round | **0.00669** | 0.01160 |

0 tracebacks/60; ladder priority inversions **0 of 732 logged firings** (in-bot `_fs_rung`
falsifier re-runs every higher rung's own predicate probe-mode after each firing).

## ⭐ P6 — ENEMY BODIES BLOCK BARRIERS (engine-answered, both verdicts)
`can_build_barrier` on a seat holding an enemy builder body, no building, affordable:
**FALSE 40/40**; empty-seat control **TRUE 383/383** (1,438 adjacency readings, 8 games).
⇒ **Eviction is a PRECONDITION of sealing on body-held seats** — Magnus's rung order (evict
at 2, before clears at 3) is engine-correct, and rung-1's failure on such tiles falls through
to rung 2 by design. All barriers-needed figures are optimistic by the body-held share.
Recorded siege.py:494. ROUTE TO ATLAS at wrap.

## Dodge — Magnus's rule, measured into its correct form
Ray-trigger (a located turret's line covers our tile — his literal "sentinel starts shooting")
ships ON. ⛔ The naive HP-drop trigger measured HARMFUL and ships OFF (`FS_DODGE_ON_HIT=False`):
n=60/arm — hit-trigger 93 deaths / 15 wins / 8 kills≤r300 vs ray-only **75 / 17 / 10** (every
column). Cause: an HP-drop dodge cannot break a line it cannot locate, and a ring-standing
body IS the denial — stepping off hands back a heal seat for nothing. Dodge memory shared with
the walker's blacklist (first smoke run: walker put the body straight back on the ray, dead
r19). Net survival: deaths/body-round 0.00669 vs parent 0.01160.

## Surprises
1. ⛔⛔ **First grid lost the collar to its own magazine**: v511's "live sentinel clears the
   reserve" rule + the ladder's dominant KILL phase converted every Ti above 8 into ammo with
   the collar open — closures 1/30, 1,187 shots vs **5,761 enemy on-core heals** (out-shooting
   a defender who heals it back). Fix: reserve floor `max(8, 8×barrier)`.
   **A COLLAR IS WORTH MORE THAN A MAGAZINE.**
2. **Collar and kill are in tension, measured**: closures 30%→13.3% while wins 23.3%→36.7% —
   the sentinel that wins games also pulls defender bodies onto the ring where (P6) they block
   barriers. Enemy on-core heals 0.5473/round vs 0.0923 (v511). Under R1000_IS_DEFEAT the kill
   wins the trade; the seal metric is no longer a free good.
3. **Most of the headline win delta is the MAP GATE** (heart 10/12 as incumbent); siege-maps
   delta 25.0 vs 20.8 is within noise at this n.
4. **NOISE_ON is brutal at n=30** (four near-identical arms spanned wins 7-9, deaths 27-48) —
   every selection here was made at n=60/arm; nothing on a single 30-game grid.

## Spec deltas applied
Just-cleared seats bypass the binary-seal wait (barrier lag 0 in every observed clear-seal
pair; census: 46.6% rebuild, median 3 rounds). Wall seats pre-denied + belt seats counted
open heal seats (both verified already-correct in parent). Map skip set encoded by
(w,h,core-anchors) — lighthouse/saga/moonrise/heart/snowflake/archipelago; midgard GO;
gate driven both ways (ON: 0 siege events on heart; OFF-mutant: 94).

## Deviations
FS_DODGE_ON_HIT ships OFF (measured, above) · no rung-4 jump-queue (the ladder buys the
sentinel on walking rounds naturally — 68 built) · peck cap per-visit ×4 visits (treadmill
guard) · dodge scoped to at-ring (dodging mid-ferry would exit the pickup envelope).

## Demos
- `demos/DEMO-midgard-ringladder-CLOSED.replay26` — **midgard CLOSES: orth-8 at r94, 3 belt
  seats cleared-and-barriered, WIN by core kill r337** (v511: 0/6).
- `demos/DEMO-midgard-ringladder-FASTKILL.replay26` — best end-to-end: **WIN r104**, two
  sentinels on different sides.

## Open items
- **Closure regression (13.3% vs 30%) unresolved** — likeliest lever: a SECOND BODY (collar
  and turret compete for one action), not more ladder tuning.
- CPU unmeasured locally (stub) + dodge adds a per-round attackable-tiles sweep — platform
  `match test` required before any ship; BLOCKED by lock-in, Magnus's call.
- P6 → atlas routing at wrap.
