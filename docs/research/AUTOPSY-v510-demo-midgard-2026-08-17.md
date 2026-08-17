# AUTOPSY — v510 ferry-siege demo, midgard seed 21 (Magnus's top-3-mistakes question), s50

*Banked by the builder s50 from the opus replay-analysis agent. Source:
`demos/DEMO-midgard-ferrysiege.replay26` (30×30 midgard, we = team A core (2,2), incumbent
team B core (26,26), B wins core_destroyed r545). Decoded on `tools/replay_census.py` wire
primitives; scripts in the s50 session scratchpad `demo_autopsy/`.*

## Who carried the FS role
**Exactly one unit: builder id 3, r0-r268** (only entity emitting `_fs_draw_*`, 27 draws
r1-r122). ⛔ **The advertised raider replacement NEVER FIRED**: id 81 and id 5 drew zero FS
indicators; the core spawned no builder after r32. **277/545 rounds (50.8%) had no siege
raider at all.** (Contradicts build-report deviation 5's uncapped role-conversion claim.)

## Timeline (id 3)
ferry r1-r12 (6 hops, ~46 Manhattan tiles, all launchers self-destruct ≤1 round) → open ring
r13-r15 (sentinel r13, **first core damage r14**, first barrier r15) → clear+seal r16-r74
(30 pecks clearing 3 enemy conveyors off seats; 6 barriers; evict launcher r40; 2 more
sentinels; **enemy core 500→338 by r76, collar 7/8 by r74**) → **STALL r75-r268 (194 rounds,
142/194 strict A-B-A ping-pong, ONE action total)** → death r268 on a known-shot tile.

## TOP 3 MISTAKES (ranked by measured cost)

**1. IT ABANDONED THE PARK SEAT (28,27) — THE ONE TILE THE DEFENDER HEALED FROM.**
By design: `_fs_park_seat` (siege.py:249) picks it, `_fs_census` (siege.py:331) EXCLUDES it
from `needed` (can never be barriered), `_fs_denied` (siege.py:295) counts it denied only
while our body stands there. The raider stood on it once (r48), left (r49), never came within
d²=17 again. **51 of 59 enemy core-heal events were delivered from that tile; 234 HP restored
= 39.4% of the 594 damage we ever dealt.** The r264-r304 heal block took them 338→500 —
erasing the whole siege — and `orth_open ≥ 1` forever blocked FS_PH_SEALED (which also locks
mistake 3). **NEW vs build report** (which recorded the 7/8 symptom, not that the 8th IS the
park seat by design). Fix: occupy-park-seat as highest-priority idle action + count it open
unless stood on; or barrier all 8 and park on a diagonal.

**2. 194 IDLE ROUNDS ENDING IN DEATH ON A TILE IT HAD WATCHED GET SHOT.** r75-r268: one action
in 194 rounds; ping-pong within 15 tiles (73% strict A-B-A). `_fs_stand_target` (siege.py:774)
kept returning the park seat; `_nav` never got there (route ran through enemy sentinel
(29,28)'s corridor). The r264-r304 heal window went unopposed; then the raider stepped onto
(24,25) at 5 HP — a tile enemy sentinel (27,22) had fired on at r253/255/260/264 — and died
r268; **id 81 died on the same tile r288; three units lost on one tile to one turret.** The
raider ran at ≤8 HP for 222 rounds with no retreat and no heal. Related to but distinct from
build-report surprises 3/5. Fix: unreached-stand-target-for-N-rounds ⇒ re-plan (or ferry-hop
back); sentinel-shot-tile blacklist (gun-axis penalty covers gunners only, siege.py:995).

**3. THE MAGAZINE LOCK: 398 ROUNDS AT 2 AMMO WITH A PROVEN-ALIGNED SENTINEL STANDING.**
Team ammo = 2 from r70 to r467. Sentinel id131 (25,29): 7 core hits r59-r76, then **0 shots
for 391 rounds**, then 20 from r468 (once our own core came under fire and `under` dropped the
floor). Cause: the RING-phase reserve (main.py:469-486) prices sentinel + 12×barrier + margin;
at the ACTUAL live scale **2.58-3.08× (not the report's 1.7-2.5)** that floor is 191-230 Ti
vs a bank of mean 77 / max 177 — **0 of 376 rounds cleared it. Arithmetically unreachable.**
Their core sat at 338/500 for 188 rounds; 19 shots = 190 Ti would have finished it; passive
income alone over the window was ~940 Ti. **NEW as a measured lock** (build-report surprise 2
recorded the SEAL starving; the fix moved the starvation onto the MAGAZINE). Fix: price the
reserve against seats actually owed (1, not 12); clear it whenever a live sentinel has a legal
ray on a core tile.

## Honorable mentions
- 30 rounds / 60 Ti of 2-damage pecking to clear 3 conveyor-squatted seats (43% of the first
  70 rounds — and destroying their buildings LOWERS their cost scale).
- The eviction launcher was a treadmill aimed at the wrong side: 119 throws, **117 identical
  (26,24)→(25,20) 4-tile hops recycling the same 2 bots** (100% return rate, short-dump
  regime) — and its d²≤2 pickup can never reach the healer seat (28,27) at d²=8. It could not
  have stopped the healer even in principle.

## What it did right
The ferry worked exactly as specified and drew first blood: 6 hops r1-r12 (~3.8 tiles/round),
every launcher self-destructing on schedule, landing ON ring seat (28,26); sentinel r13, enemy
core damaged r14, 338/500 by r76, our core untouched until r453. Collar 7/8 by r74. **The
opening is not the problem; everything after r74 is.**

## Load-bearing for the loss (not asked, banked)
**The incumbent ran the same collar plank on US**: barriers on 6 of our 8 seats r48-r96 plus
2 corners, with our own conveyors holding the last 2 seats — and we issued **zero attacks and
zero destroy calls against any of it in 497 rounds.** (The home-side blindness is the
LOKI_QUIET_ON/intruder-filter family, queued post-plank with three prior derivations.)

## Routed
All three fixes + the replacement-never-fired defect + the conveyor-seat amendment forwarded
into the `_v511sealonly` build (in flight) at 2026-08-17T19:1xZ.
