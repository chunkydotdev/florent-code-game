# AUTOPSY — v512 on glacierkeep/nordkap/atoll (24 games), s50 2026-08-17

*Banked by the builder s50 from the opus failure-autopsy agent. Batch: `_v512ringladder` vs
`_v488beltbreak2`, 3 siege maps × 8 games, local --tle 10, 0 tracebacks. Pooled 4/24 wins
(16.7% ± 14.9 naive — contains the grid's 25.0% siege figure), 19/20 losses = our core
destroyed (median r200), closures 2/24. Demos (local, gitignored): DEMO-nordkap-v512-LOSS
(r167), DEMO-glacierkeep-v512-LOSS (r446), DEMO-atoll-v512-WIN (kill r138). Raw data +
instruments in the s50 scratchpad `v512_failures/`. Representative-loss selection rule stated
in the agent report (modal-mechanism medoid, NOT the raw median game).*

## POOLED FAILURE-CAUSE RANKING (by measured cost)

**1. NEW — THE ENEMY PLANTS A SENTINEL AT OUR DOOR AND WE NEVER TOUCH IT: 0 of 40.**
100% of the 1,202 damage events on our core (21,636 HP, all 24 games) came from enemy
sentinels sited nearer OUR core than theirs (d² 4-37 from us). 40 such plants; our builders
attacked 0; 38/40 survived to game end. Median warning plant→our-death: 56 rounds (min 28,
n=19). A sentinel is 40 HP; two builders pecking kill it in 10 rounds; the Ti was there. Our
241 builder attacks went to conveyors (185), builders (23), enemy-RING sentinels (19), door
sentinels (0). Same family as the midgard "home-side blindness" + the three prior derivations
(Juusto 27.9%-vs-58.6%, Erebus L6, field-study counterplay) — NOW THE #1 MEASURED COST.

**2. NEW — `titanium_collected` = 0 IS A CONNECTIVITY BUG: THE BELT STOPS ONE CONVEYOR SHORT.**
Perfect separation 24/24: core-adjacent conveyor ⟺ tic>0 (13/13); none ⟺ tic=0 (0/11). In
8/11 zero games the belt terminus sits at Manhattan 2 from the core — ONE 3-Ti link missing.
Not attrition (harvesters die 6%, conveyors 7%). glacierkeep_g5: 9 stacks entered the pipe,
all 9 jammed at the dead end, 0 arrived in 447 rounds. Both-ways: enemy reads 142/166
arrivals in the same games; our wins read 201/173. The economy is winner-take-all (21/24 the
higher-tic side won; 8 games one side collected zero) and we never contest it. FS-side only
(the control's identical chassis connects fine) — suspicion: the 3-builder cap / role
dispatch starves the eco ordinal that finishes the belt (38/85 eco builders build NO
harvester/conveyor at all; 23 build nothing whatsoever).

**3. NEW (exactness) — THE HEALER CANCELS OUR SENTINEL FIRE 1:1, NOT PARTIALLY.** Pooled:
19,152 damage on their core, 16,962 healed (88.6%); in 13/21 games with any damage the cancel
is ≥99%, EIGHT EXACT TO THE HP (e.g. 1,530/1,530 across 85 shots over 320 rounds). Without
heal denial, sentinel fire nets zero — the kill REQUIRES the seal (or the healer's removal).

**4. KNOWN, NOT FIXED — THE MAGAZINE LOCK SURVIVED v512's REWRITE.** 3,495 of 4,519
live-sentinel rounds (77.3%) had under one shot of ammo; in 3,340 (73.9%) we simultaneously
held ≥10 unconverted Ti. glacierkeep_g5: ammo=1 for 200 consecutive rounds, 48-58 Ti in hand,
aligned sentinel standing.

**5. KNOWN, WORSE — RAIDER DIES, IS NOT REPLACED, AND THE DODGE PREVENTED NOTHING.** 23
raider deaths/24 games, ALL to enemy turrets (20 sentinel, 3 gunner) — ray-trigger dodge
prevented 0. Raider-absent: median 65% of loss rounds; 64.9% of all 4,434 enemy core-heals
were delivered while we had NO raider alive. Second raider in 5/24 games, 3 of them post-r120.

**6. NEW — HEALS COME FROM NEVER-BARRIERED SEATS, NOT A PARK SEAT.** 40.9% of heals from
seats we never barriered once; 37.6% before we arrived; 21.4% after our barrier died (124
placed, 41 destroyed, median lifetime 7 rounds). Seat-heal concentration 0.26-0.67 — the
midgard occupy-the-park-seat fix does NOT transfer; the problem is COVERAGE AND SPEED (⇒
second body).

**7. KNOWN — closure barely happens (2/24) and did not convert (both closures lost).**

**8. NEW — EVICTION FIRED ZERO TIMES IN 19/24 GAMES** (rung-2 starvation confirmed at scale —
the seal-wait exemption fix stands). The one high-count game (385 throws) is the pure 2-cycle
treadmill; it lost at r749 dealing 54 damage. Per P6, zero evictions ⇒ body-held seats
unsealable by construction.

**9. KNOWN — one-body contention**: raider logs 9 action-rounds of 48 alive (nordkap_g1), 14
of 129 (glacierkeep_g5). Forward sentinels 14 survived / 16 killed (12 by enemy sentinel).

## SPAWN PLACEMENT (Magnus's question) — measured, honest answer
RAIDER: placement costs ~1 walk tile / ~1 round (median extra 1 tile; the ferry absorbs it —
arrival median r7, already minimal for the separations; enemy-facing seat would save <1 hop).
ECO: +2.43 mean extra tiles (NOT the old chassis's +10.5; OPENFAST's number does not
transfer) — worth ~2 rounds. ⇒ purposeful spawns stay in v513 as a cheap polish, but the
measured eco defects that dominate are the MISSING LAST LINK (#2) and 38/85 idle eco builders.

## CONSEQUENCES FOR v513 (builder's routing)
Measured-cost order: (1) door-sentinel response — home builders peck the turret shelling our
core [needs Magnus's nod: touches home doctrine / the LOKI_QUIET family he owns; the audit was
already Magnus-approved as a proposal]; (2) belt last-link fix + eco-idle fix; (3) second body
+ rung-2 seal-wait exemption (covers #6/#8/#9); (4) magazine lock real fix (KILL-phase
conversion when an aligned sentinel exists, verified in-game this time); (5) replacement
dedicated store field + dodge rework (current dodge is measured ineffective); (6) purposeful
spawns (small, cheap, Magnus-requested).
