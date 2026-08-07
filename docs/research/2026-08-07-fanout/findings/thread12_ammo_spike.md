# Thread 12 — AMMO-SPIKE TRIGGER PRE-MORTEM

Read-only replay decode, 2026-08-07. Bot under study: `bots/_v72e2/main.py`
(ammo logic `:613-643`, turret fire path `:2554-2632`, hunt gate `:1457-1620`,
`HUNT_BAND_DSQ = 41` at `:94`).

Toolkit: `SCRATCH/toolkit/replay_lib.py`. Scripts written for this thread live in
`SCRATCH/thread12/` (`analyze.py`, `windows.py`, `final_windows.py`, `secondary.py`,
`killers.py`, `killers2.py`, `context.py`).

**Verdict up front: the spike trigger is a pre-mortem FAIL.** It would have fired on
20 windows across 8 games, on a median bank of **24 Ti**, and on **zero** of the
turrets that actually killed our core. The Ti we bank (2,782–7,178) is banked in
rounds where we own no turret and have no target; the rounds where a turret is dry
are rounds where the bank is 10–40 Ti. The two things never co-occur.

---

## 0. Geometry and reload, validated against the files

Attack sets were reconstructed from facing (spawn direction + every `placeEntity`
rotation update) and checked against every observed `FireTurret` in the 8 games:

| turret | ray | max offset seen | reload (modal gap between own consecutive shots) |
| --- | --- | --- | --- |
| sentinel | single-tile forward ray, pierces | dsq 32 (cardinal k=5 → 25, diagonal k=4 → 32) | **2** (109 of 176 gaps) |
| gunner | single-tile forward ray, stops at first blocker | dsq 9 cardinal k=3 / 8 diagonal k=2 (r²=13) | **1** (178 of 225 gaps) |

Zero misaligned shots for either type once rotation history is applied. Ammo
bookkeeping: `avail[r] = ammo_curve[r] + spent[r]` (post-convert, pre-shot);
`bank[r] = titanium_curve[r] + converted[r]` (pre-convert).

Same-round convert→fire is real but rare: across the 8 games there were **419
conversion rounds** and only **17** in which a turret then fired past its
pre-conversion ammo. The core usually runs after the turrets.

---

## 1. Per-game missed-spike windows

Definition used (the brief's): a turret of ours has an enemy entity in its actual
attack set ∧ team ammo < that turret's shot cost ∧ bank ≥ that shot cost.
"Would-have-killed" = `min(shots the reload allows in the window, (bank+ammo)//cost)
× dmg ≥ target HP`.

| game (id · g · map · opp) | dry rounds | windows | notes |
| --- | --- | --- | --- |
| `c2e57b46` g2 lighthouse · Lunds | 0 | **0** | 110 shots fired, never dry |
| `c2e57b46` g5 heart · Lunds | 11 | **2** | |
| `a5671738` g1 drumlin · CAD | 3 | **1** | |
| `a5671738` g4 heart · CAD | 0 | **0** | 121 shots, never dry-with-bank |
| `2cfcb658` g1 antler · Ouroboros | 0 | **0** | 18 target-rounds in 380 |
| `2cfcb658` g4 atoll · Ouroboros | 26 | **13** | 4 turrets simultaneously dry on one gunner |
| `706faea6` g3 hive · Ouroboros | 8 | **4** | all inside r25–46 |
| `17622ae0` g5 jackpot · Ouroboros | 0 | **0** | 18 target-rounds in 1000 |
| **total** | **48 obs** | **20** | 12 last ≥2 rounds, 9 last ≥3 rounds |

### The windows themselves

| # | game | round-span (dry) | our turret | target | HP | kill cost | ammo | **bank** | full-bank verdict | reality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | c2e57b46 g5 heart | r6 (1r; engagement r6–15) | sentinel #13 | **launcher #7** @(17,10) | 30 | 20 | 0 | **240** | KILL (afford 24 shots) | fired 5 later; #7 survived — but it **never threw a single builder of ours** (0 teleports in the file), so the kill is worth ~nothing |
| 2 | c2e57b46 g5 heart | r19–36 (10r) | sentinel #28 | builder #6 | 40 | 30 | 32 | 24 | KILL | died r37 anyway |
| 3 | a5671738 g1 drumlin | r390–395 (3r) | gunner #482 | **barrier #1201** | 30 | 20 | 0 | 39 | KILL | a 3-Ti barrier, 7 rounds before the game ended |
| 4 | 2cfcb658 g4 atoll | r255–259 (2r) | sentinel #323 | conveyor #500 | 20 | 20 | 16 | 22 | KILL | died r262 anyway |
| 5 | 2cfcb658 g4 atoll | r255 (1r) | sentinel #323 | builder #435 (2 HP) | 2 | 10 | 9 | 22 | KILL | died r256 anyway |
| 6 | 2cfcb658 g4 atoll | r271 (1r) | sentinel #229 / #517 | gunner #559 | 25 | 20 | 9 | 22 | no kill | died r272 anyway |
| 7 | 2cfcb658 g4 atoll | r271–287 (2r) | sentinel #323 | builder #470 | 40 | 30 | 29 | 22 | KILL | died r289 anyway |
| 8 | **2cfcb658 g4 atoll** | **r273–275 (3r)** | **sentinel #229, #517 + gunner #332, #347 (four turrets, all dry)** | **gunner #561** @(12,8) | 25 | 16–20 | 15 | **32** | **KILL** | died r276 anyway |
| 9 | 2cfcb658 g4 atoll | r287–291 (3r) | sentinel #229, #517 + gunner #332 | gunner #587 @(12,8) | 25 | 16–20 | 7–17 | 32 | KILL | died r292 anyway |
| 10 | 706faea6 g3 hive | r33–37 (4r) | sentinel #62 | conveyor #44 | 20 | 20 | 16 | 20 | KILL | survived |
| 11 | 706faea6 g3 hive | r33 / r37 (1r ea.) | sentinel #62 | builders #66 / #7 | 40 | 30 | 8 | 10–20 | no kill | survived |
| 12 | **706faea6 g3 hive** | **r35–36 (2r)** | sentinel #62 | **gunner #84** | 25 | 20 | 8 | 12 | KILL (afford exactly 2) | died r37 anyway |

Bank at the moment of the missed window: **median 24 Ti, max 240 Ti**. Sixteen of
the twenty windows sit on a bank of 10–39 Ti — one to four shots' worth, not a
"whole bank" at all.

**Deduplicated, 13 distinct target-episodes.** Eight of the thirteen targets died
within 1–5 rounds anyway; the spike would have bought 1–5 rounds of tempo. The five
that genuinely survived are: an inert enemy launcher, a 3-Ti barrier, one conveyor
and two builder bots. **Not one of the 20 windows is on a turret that was shelling
our core.**

---

## 2. Why: the killer was never in a line of fire

For each of the six `core_destroyed` losses, the enemy shooters that did the damage
(`killers.py`, `killers2.py`):

| game | killer | built | dsq to our core | shelled | dmg to our core | our damage back | **rounds it spent in ANY of our turrets' attack sets** | our Ti bank while it shelled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c2e57b46 g2 lighthouse | gunner #291 | r123 @(6,6) | **8** | r132–188 | **392** | **0** | **0** | 339 → 519 |
| c2e57b46 g2 lighthouse | sentinel #436 | r176 @(7,4) | 9 | r177–187 | 108 | 0 | **0** | 491 → 521 |
| c2e57b46 g5 heart | sentinel #101 | r65 @(12,10) | 16 | r66–159 | **720** | **0** | **0** | 113 → 499 |
| a5671738 g1 drumlin | gunner #1040 | r338 @(4,5) | **1** | r339–397 | 403 | 28 | **0** | 34 → 1 |
| a5671738 g1 drumlin | sentinel #29 | r11 @(9,8) | 13 | r12–84 | 396 | 40 | **0** | 94 → 44 |
| a5671738 g4 heart | sentinel #971 | r455 @(10,12) | 8 | r456–500 | 414 | **0** | **0** | **985 → 636** |
| a5671738 g4 heart | gunner #11 | r3 @(11,9) | 9 | r4–138 | 406 | 42 | **0** | 284 → 8 |
| **2cfcb658 g1 antler** | **gunner #180** | r73 @(8,14) | **2** | **r75–379** | **2135** | **0** | **0** | 246 → **679** |
| 2cfcb658 g4 atoll | gunner #623 | r306 @(16,1) | **2** | r308–489 | **1274** | **0** | **0** | 116 → **648** |
| 2cfcb658 g4 atoll | gunner #703 | r348 @(17,5) | 8 | r360–489 | 609 | 0 | **0** | 214 → 648 |

7,818 core damage taken from these shooters; 178 damage returned to them, all of it
from builder pecks. **Every one of them stood inside `HUNT_BAND_DSQ = 41`** (dsq
1–25, i.e. usually inside the core's own r²=36 vision) for the whole siege, and none
of them ever entered one of our turrets' rays.

Corroborating band census (`secondary.py`), enemy turrets inside dsq ≤ 41 of our
core that we never damaged at all:

- **antler `2cfcb658` g1: 16 enemy turrets in the band, 14 never touched.** Gunner
  #21 sat in the band for **375 of 380 rounds** and took 16 damage.
- **jackpot `17622ae0` g5: enemy gunner #280 sat in our band for 809 rounds and took
  zero damage** — while we banked **7,178 Ti**.
- atoll `2cfcb658` g4: 17 in band, 7 never touched (#623 = the core-killer, 184 band
  rounds, 0 damage).
- heart `c2e57b46` g5: sentinel #101, 95 band rounds, 0 damage, killed our core.

This is the same mechanism the session-12 solvency work already recorded on hive
("0 of 270 builder attacks landed within dsq ≤ 41 of our own core — turret-hunting
never engaged, ever"), now confirmed on five more maps and three more opponents.

## 2b. Where the big bank actually comes from

| game | max Ti | first r with Ti ≥ 2000 | rounds with **≥1 turret alive** | rounds with **zero turrets** | rounds with any target in a ray | last target round |
| --- | --- | --- | --- | --- | --- | --- |
| 706faea6 g3 hive | 4,024 | r595 | **22** | **978** | 22 | r46 |
| 17622ae0 g5 jackpot | 7,178 | r308 | **20** | **980** | 18 | r38 |
| 2cfcb658 g1 antler | 679 | — | 34 | 346 | 18 | r40 |
| 2cfcb658 g4 atoll | 653 | — | 378 | 112 | 111 | r318 |
| a5671738 g4 heart | 1,007 | — | 415 | 86 | 161 | r499 |

The 2,782–3,031-Ti-with-13-shots signature that motivated this thread is not an
ammo-scheduling state. On hive and jackpot our last turret dies at r47 / r39 and we
then spend **978 / 980 rounds with no turret at all**. No conversion trigger of any
design can fire in that state, because `convert_ammo` buys ammunition and we own
nothing that drinks it. The correct lever there is **build a turret / put a ray on
the shooter**, and it is a titanium-spend problem, not a titanium-conversion problem.

---

## 3. The trigger spec — what would have fired, precisely

Stated for completeness and because a later thread will ask. Recommendation:
**do not build it as a headline change**; if it ships at all it should ride along
with a line-of-fire fix, where it costs ~15 lines and cannot hurt.

### Condition

```
SPIKE ⟺  ∃ turret T of ours, alive, action-ready, with an enemy entity E on T's
         actual firing ray (sentinel: dsq(E,T) ≤ 32 along facing; gunner: first
         blocker along facing with dsq ≤ 13)
    ∧    global_ammo < cost(T)                      # 10 sentinel / 4 gunner
    ∧    global_ti - RESERVE ≥ cost(T)
```

Emission: **the turret is the only unit that can evaluate this** — the core's vision
is r² = 36 and it has no facing-ray knowledge of remote turrets. So `_turret()`
writes the demand; `_core()` pays it.

### Conversion size

```
want   = Σ over dry turrets with a live target of  K × cost(T)      # K = 3 shots
amount = min(want, global_ti - RESERVE)
convert if amount ≥ min_cost_on_the_wire  (4 if any gunner is dry, else 10)
```

`K = 3` is sized from the measured windows: median engagement length 4 rounds,
sentinel reload 2 → 2–3 shots is the whole physically-firable magazine. Anything
above that reproduces the refuted floor.

### Reserve (the economy/heal interaction)

The solvency finding is binding here: heal is 1 Ti and *healing stopped for 300
straight rounds on hive because titanium sat at 0–85*. So the reserve must dominate
the heal line, not the other way round:

```
RESERVE = 16                      # heal reserve, matches the siege-solvency package
        + (30 if under_siege else 0)   # one replacement builder while UNDER
```

i.e. **46 Ti under siege, 16 quiet.** This is strictly above the current
`ti_floor = 12` (`_v72e2:641`) and never below it, so the change can only make
conversion *more* conservative in the quiet phase — which is the direction both
refuted experiments say to move.

**And this is the pre-mortem's arithmetic problem.** Bank at the 20 measured
windows: `240, 39, 32×6, 24, 22×6, 20×2, 12, 10`. With `RESERVE = 16`, only **1 of
20** windows (heart g5 r6, bank 240) clears `bank − 16 ≥ 3 × 10`. With
`RESERVE = 46`, still 1 of 20. A reserve small enough to fire on the other 19 is a
reserve that re-creates the heal starvation that cost us hive.

### Anti-thrash guard

Windows flicker (a builder walks through a ray for one round). Guard:

- **Latch, not level.** Turret writes `round + 1` into the slot; core treats the
  demand as live while `round − stamp ≤ 3`. Cheap, and it survives the buffered
  write.
- **Cooldown.** At most one spike per `SPIKE_COOLDOWN = 8` rounds, tracked in the
  same slot's high bits. Twenty windows over 8 games means a correct
  implementation converts at most ~2–3 times per game; anything firing more often
  is thrashing.
- **Minimum window.** Do not spike on a 1-round sighting: the store write is
  buffered, so a spike is usable at r+1 at the earliest and only for turrets that
  run after the core (measured: that path works, 17 times in 419 conversions).
  9 of the 20 windows last ≥3 rounds; 8 do not and are unreachable by construction.

### State

Both slots the brief names are **write-only dead ends in `_v72e2` — verified**:
`SLOT_ECO_READY = 5` is written at `:615, :725, :1715, :1903` and never read;
`SLOT_LINKS_DONE = 9` is incremented at `:2352, :2368` and never read. Either can
carry the latch. Prefer **slot 9** (its two writers are in one builder method and
are trivially deletable; slot 5 has four writers spread across core, builder and
expand paths).

Packing: `value = round_stamp * 8 + dry_shot_units`, `dry_shot_units` = number of
4-Ti shot-equivalents demanded, capped at 7. One slot, one write per round, no
read-modify-write race between units (last writer in the round wins, and any writer
is a turret with a real target, so any winner is correct).

---

## 4. Rotation sink — a real leak, and it is bigger than the ammo one

`rotate()` costs **10 Ti and sets action cooldown to 1** (so the round after a
rotation the gunner cannot shoot). Counted from `placeEntity`-as-update events
(`r.rotations(team)`), which is the trap-5 path in the toolkit README.

| game | map | opp | **our rotations (Ti)** | their rotations (Ti) | our end Ti |
| --- | --- | --- | --- | --- | --- |
| `c2e57b46` g2 | lighthouse | Lunds | 14 (**140**) | 15 (150) | 519 |
| `c2e57b46` g5 | heart | Lunds | 0 (**0**) | 2 (20) | 499 |
| **`a5671738` g1** | **drumlin** | **CAD** | **325 (3,250)** | 8 (80) | **1** |
| `a5671738` g4 | heart | CAD | 66 (**660**) | 13 (130) | 636 |
| `2cfcb658` g1 | antler | Ouroboros | 0 (**0**) | 52 (520) | 679 |
| `2cfcb658` g4 | atoll | Ouroboros | 41 (**410**) | 48 (480) | 648 |
| `706faea6` g3 | hive | Ouroboros | 0 (**0**) | 2 (20) | 4,024 |
| `17622ae0` g5 | jackpot | Ouroboros | 0 (**0**) | 9 (90) | 7,178 |
| — 8-game total — | | | **446 (4,460 Ti)** | 149 (1,490 Ti) | |
| `8ed4d332` g4 (v61 **win**) | jackpot | Kladde | **378 (3,780)** | 0 (0) | 12 |

**Flag it. It is its own leak and it is first-order.**

- **drumlin `a5671738` g1: 3,250 Ti spun = 56.5% of our entire titanium income that
  game** (delivered 4,260 + passive 990 + starting 500 = 5,750). Total ammo
  converted all game: **364 Ti**. We ended the match on **1 Ti** and lost by core
  destruction with an enemy gunner at dsq 1. The rotation sink was **8.9× the whole
  ammo budget** it is supposedly competing with.
- `8ed4d332` g4 (the v61 win): 3,780 Ti = 47.7% of income, 3,450 of it from a single
  gunner #50 that fired 99 shots (396 Ti of ammo) while spending 3,450 Ti turning.
- Three of the eight games in this set exceed 300 Ti of spin; two exceed 3,000.

**It is a thrash, not a cost of doing business.** Per-turret decode:

| turret | game | rotations | Ti | A→B→A oscillations | modal gap | shots fired |
| --- | --- | --- | --- | --- | --- | --- |
| gunner #248 | drumlin | 128 | 1,280 | 48 | **1 round** (66×) | 13 (52 Ti of ammo) |
| gunner #203 | drumlin | 113 | 1,130 | 38 | 1 round (56×) | 14 |
| gunner #50 | 8ed4d332 g4 | 345 | 3,450 | 146 | 1 round (168×) | 99 |
| gunner #703 | heart g4 | 21 | 210 | 17 | 1 round (19×) | **0** |
| gunner #641 | heart g4 | 24 | 240 | 21 | 1 round (19×) | 4 |

Top transitions are literal reversals (`NORTH↔NORTHWEST` 13/10, `NORTH↔NORTHEAST`
12/11, `SOUTH↔NORTHEAST` 33/28). Mechanism is visible in `_v72e2:2626-2632`: with no
target on the ray, the gunner takes the nearest enemy entity in vision and rotates to
`p.direction_to(enemy)` — the nearest 45° compass bearing, which is **not** a test
that the target lands on the resulting ray. Off-axis targets therefore never become
shootable, the bearing flips as the target drifts a tile, and the gunner pays 10 Ti
+ one lost shot every round to chase it. `heart` g4 #703 is the pure case: 21
rotations, 210 Ti, zero shots ever fired.

The fix is one guard the API already provides and this file never calls in
`_turret()`: only rotate if `ct.can_fire_from(p, want, turret_type, target_pos)`
would actually put the target on the ray, plus a per-turret "no rotation within N
rounds of the last one" latch. Expected saving on this evidence: 3,000+ Ti on
drumlin-shaped games, ~400–700 Ti on the mid cases, and one restored shot per
suppressed rotation.

---

## 5. Cross-check against the two refuted floor experiments

`docs/strategy-log.md:1355-1375` (AMMO_BUFFER 20→50, confirm **45.3%** [39.3, 51.4])
and `:1276-1310` (demand-driven conversion on a threat timestamp, confirm **46.1%**
[40.1, 52.2]).

The honest reading is that the spike trigger is **not** mechanically the same lever —
and also that it does not escape the reason those failed. Not the same: the buffer
experiment raised a *standing* floor and paid the quiet-phase opportunity cost every
round of the match; the second one moved the floor *and* added a delayed burst, and
its own write-up admits it confounded a floor cut (20→10) with the burst, so the
burst was never isolated. A pure spike changes nothing in the quiet phase — the
target-present predicate is false there, so the quiet-phase floor is bit-identical to
today's `AMMO_FLOOR = 16`. That is a genuinely different intervention and the earlier
CIs do not bound it.

But the same *underlying fact* kills both, and this decode is what names it. The
second experiment's trigger was "any enemy unit within a sentinel's r²=32 vision" —
a proximity test. The spike trigger's is "an enemy on the firing ray" — a geometry
test. Proximity fires often and buys ammo for shots that cannot be taken (the r²=32
disc has ~100 tiles; the ray has 5). Geometry fires rarely and correctly. Measured
here: geometry fires on **20 windows in 8 games**, and at those moments the bank
holds a median of 24 Ti — one to three shots. So the spike is not the mechanism they
refuted, and it is *also* not worth much, for a reason neither experiment could see:
**we are not ammo-limited, we are line-of-fire-limited.** In 6 of 6 core-destroyed
losses the shooter that killed us never entered a single ray of ours, while we sat on
246–985 Ti. Both floor experiments and this spike are all downstream of a turret that
is pointed at the enemy; none of them creates one.

---

## Recommendation ordering, on this evidence

1. **Engage the band-41 shooter.** 7,818 core damage taken from turrets we returned
   178 damage to; every one inside the hunt band the whole time. This is the
   `HUNT_MIN_HEALERS`/eco-gate deadlock the solvency thread already isolated, now
   confirmed on 5 more maps. Highest value by an order of magnitude.
2. **Fix the gunner rotation thrash** (`_turret`, `can_fire_from` guard + latch).
   Up to 3,250 Ti/game recovered, and it restores suppressed shots. Cheap, local,
   measurable, and it is the *only* item in this thread that frees real titanium.
3. **Put a ray on the shooter on hive/jackpot** — 978/980 rounds with zero turrets
   alive on 4,024/7,178 banked Ti is a build problem, not an ammo problem.
4. **The ammo spike** — ride-along only, `RESERVE = 16 + 30·under`, K = 3, slot 9
   latch, 8-round cooldown. Expected effect on this corpus: ~2 windows per game
   converted, on a 24-Ti median bank, on targets that mostly died anyway. Do not
   spend a battery slot on it alone.
