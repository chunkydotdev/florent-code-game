# Meander zero-delivery: naming the owner

Research arm, 2026-08-08 17:20 CEST. Repo HEAD `2ef0aa1`.

Companion read (foundation, read first): `docs/research/fjordgate-collapse-owner-2026-08-08.md`.
That note established fjordgate-B (zero harvesters ever) and meander (harvesters
r5/r6, zero delivery) are different defects. This note owns the meander side.

**Version tags** (md5 re-verified this session)

| thing | path | md5 |
| --- | --- | --- |
| live v80 "Eir 9b" | `bots/_v89sh/main.py` | `e12f85855654e9e78227582d0dc15d4b` |
| staged head (arm `w`) | `bots/_v93w/main.py` | `52b1f306266ac77997e07e7f35a66f5b` |
| reserve-fix variant (arm `wb`) | `bots/_v93wb/main.py` | `b835132aff45200bcfc5f78bf41988ab` |
| frozen opponent | `bots/cad_probe/main.py` | `6d0e955f96de1f0d11f93db573ade458` |

All line cites are **`bots/_v93w/main.py`** unless stated otherwise.

**Discriminator bundle** (read-only):
`/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/284161ab-b59c-40d1-b62e-89fea0a300d9/scratchpad/fjord_disc/`
— 24 meander games across arms `w`/`woff`/`wb` x 2 seats x 6 seeds vs `cad_probe`,
plus the FB build's `arm_fb`/`arm_fboff` set. Every meander cell is
seed-invariant (all 6 seeds byte-identical rounds/Ti in `disc_results.json` and
`instruments.json`), so the per-cell decodes below use seed 1 and represent the cell.

**Board facts** (replay Map decode): meander is 25x15, cores A(11,3) / B(11,10)
— anchors share x=11, footprints share columns x=11-12 (the sentinel lane).
24 ore tiles, only 8 walls. The map is exactly mirror-symmetric under y -> 14-y
(all 24 ore tiles and both core footprints map onto each other). Replay
`Direction` enum is 1-based (1=N..8=NW), verified against cad's delivering belt.

**Outcome shape being explained** (from `disc_results.json` / `instruments.json`,
identical across seeds): every one of the 36 meander games (w/woff/wb/fb/fboff x
2 seats) latches `SLOT_UNDER` to exactly `[[0,0],[4,2]]` — first nonzero read r4,
value 2, never any other value, never releases. arm_w seat A: first harvester r5,
0 Ti, dead r185-186. arm_w seat B: first harvester r6, 0 Ti, **wins 6/6 at r517**.
arm_woff seat A: 0 Ti, dead r274-281. arm_woff seat B: first delivery **r17**,
1,640-2,830 Ti, W4/6. arm_wb: both seats 0 Ti. arm_fb/fboff meander = byte-identical
to arm_w (186/517 rounds, same Ti) — the in-flight FB build's own det set confirms
its pre-statement that it leaves meander unchanged.

---

## Q1 — The chain-completion failure

### Verdict

**Harvesters get built and belts get laid; every belt is then severed at exactly
one tile — a tile that was on the planned link path when `_link_path` planned it
and that a turret (ours or cad's) occupied before the linker reached it. The
owning code is `_build_next_link`, `:4822-4823`: `if
ct.get_tile_building_id(tile) is not None: self.link_queue.pop(0); continue` —
ANY building on the planned tile is popped as a completed link.** The file
documents this defect about itself at `:519-521` ("_build_next_link treats an
occupied tile as a completed one ... so the site is never cleared and never
re-routed"). The rest of the belt is built on both sides of the blocker, stacks
freeze against it, harvester output backpressure-stalls, and delivery is zero
forever. Titanium does not vanish: it piles up 3-4 stacks deep on the dead belt —
and on seat A the second harvester's output is siphoned wholesale by cad's
adjacent belt.

There is no repair path: re-planning only ever happens for a *new* harvester
(`_wire_on_build:4593-4610`, `_wire_tick:4636-4659`), `_has_acceptor:4620-4631`
declares the old harvester "served" because a conveyor is adjacent (the dead
belt), and a *new* harvester is money- and labour-blocked under the permanent
latch (below). Chain building itself is owned by `_expand:4063` ->
`_build_next_link:4812`, with the money gate at `:4813`
(`_eco_spendable(conveyor_cost)`).

### Evidence (arm_w, seed 1; conveyor facings converted from the 1-based enum)

**Seat A** (core (11,3)). Two chains:

- Chain 1: harvester r5 (16,6); conveyors (16,5)W r7, (15,5)W r9, (14,5)W r11 —
  then a **gap at (13,5)**, then (13,4)W r28 feeding core tile (12,4). (13,5) got
  **our own defender's counterbattery sentinel at r5** (build event `(5, id11,
  (13,5))`; id11 is the 5th spawn = role_n 4 defend; `_try_counterbattery`'s
  bleeding waiver was open — first core damage r4). (14,5) outputs W into the
  sentinel, which never accepts. Stack-move endpoints on this belt, whole game:
  (16,5):3, (15,5):2, (14,5):1 — three stacks entered, froze, and the harvester
  stopped producing. The tile (14,4) was never built, confirming the plan ran
  through (13,5).
- Chain 2: harvester r11 (7,6); conveyors (8,6)E r16, (9,6)E r20, (10,6)E r40,
  (11,6)N r44 — then the terminal seat **(11,5) is never built** (cad raiders
  camp the lane at (10,4)/(10,5)/(9,6); cad's gunner takes (11,5) itself at r56,
  after which `:4822` pops it as "complete"). Worse: cad ran its own conveyor to
  (6,6)/(7,7), orthogonally adjacent to our harvester (7,6), and the engine's
  distribution handed our output to it: **29 of 38 total stacks our harvesters
  emitted went onto cad's belt** ((6,6):25 + (7,7):4), feeding cad's 96 decoded
  core deliveries (cad collected 1,450 on this seat).

**Seat B** (core (11,10)). One chain: harvester r6 (16,11); conveyors (16,12)W r8,
(15,12)W r10, (14,12)W r12, (13,12)W r14 — the terminal seat **(12,12) got cad's
gunner at exactly r16**, the round our linker would have built it (in arm_woff we
build (12,12) ourselves at r16). Popped as complete; belt dead-ends into the
gunner. Stack endpoints: (16,12):4, (15,12):3, (14,12):2, (13,12):1 — four stacks
frozen, 4 total harvester outputs in 517 rounds, `dist moves to_our_core = 0`.

**The "18 buildings at 0 Ti" on meander-A decoded**: 20 non-core builds = **16
conveyors + 2 harvesters + 2 sentinels** (18 alive at death). Not a turret spam:
6 of the conveyors are the two severed chains, the rest pave-trail. So meander-A
*attempts* the full economy and is severed at one tile per chain — explicitly
different from fjordgate-B's three-sentinels-and-nothing-else.

**Why no harvester #3 ever (the recovery path)**, measured:

- Money: bank median 10 (A) / 12 (B); rounds with bank >= 20: 18/186 (A), 90/517
  (B). The sinks under the permanent latch: the Core ammo drip — `ti_floor = 12
  if (under or weapons)` at `:2024`, drip `:2032-2035` — converted 162 Ti (A) /
  **978 Ti (B, feeding the grind sentinel)**; melee attacks 119 (A) / 185 (B) x 2
  Ti. Post-r120 `_eco_spendable:2226-2231` demands `cost + 16`.
- The `wb` natural experiment repeats fjordgate's off-by-a-few: arm_wb holds the
  bank at 20-37 for 101/101 rounds post-r120 (median 27, max 37) and builds a
  **byte-identical** build list to arm_w — zero new harvesters. Scaled harvester
  cost after 2 built = 22; 22 + 16 = 38 > the measured max 37.
- Labour: in wb-A the surviving expanders squat **on** ore at (6,0), (6,14),
  (19,1) from ~r60 to r180+ (ORE step-off is gated to wall-dense maps,
  `ORE_STEPOFF_MIN_WALLS = 80` at `:163`; meander has 8 walls, so the gate is
  shut and an on-ore park is permanent), one is parked at (15,7) adjacent to no
  ore, and the saboteur is permanently melee-recalled (`:2676-2692`, meander is
  not in `keep_artillery_forward`) by cad's raiders camping (10,4)/(10,5) inside
  d²<=20 of our core all game. Note (6,0) is adjacent to ore (6,1): even the
  squatters had buildable seats during the 24 funded rounds (bank >= 22,
  r40-120) — the funded windows and the parked-labour windows demonstrably
  coexist, so both gates bind at different times; the wb ceiling proves money
  alone can't clear it post-r120.

### Confidence

**High** on the severed-chain mechanism and its file:line owner — the gap tile,
the blocker's arrival round, the frozen stack counts, and the never-again
delivery are all decoded per game, and `:519-521` documents the pop rule's
consequence in the author's own words. **High** on the no-recovery loop (wb
arithmetic 37 vs 38 measured; `_has_acceptor` source-read). **Medium** on the
exact weighting of money vs labour for harvester #3 pre-r120 — both gates are
measured present; which binds on a given round was not decoded round-by-round.

### What would change the answer

- A decode showing `link_queue` was already empty before the blocker arrived
  (would move seat A's chain-1 severance from the pop rule to the planner; the
  never-built (14,4) makes this unlikely).
- An arm with the pop rule fixed (re-plan on foreign blocker) that still fails
  to deliver — would promote the money/labour legs from recovery-blockers to
  primary owner.

---

## Q2 — The r4 UNDER=2 latch

### Verdict

**True positive. The FT plank fires on a real ferry and works exactly as
designed; the defect is entirely in the response, and the response is not even
`2`-specific.** Three separately decoded facts:

1. **The trigger is genuine.** cad_probe places its launcher r1 ((11,8) seat A /
   (11,6) seat B) and throws its own raiders at our core ring: decoded builder
   jumps r2, r4, r6 -> (10,4) [seat A] and (10,10), (10,10), (9,10) [seat B] in
   every arm. `ferried()` arithmetic (`:1291-1305`, footprint-measured from the
   *enemy* anchor, `FERRY_SLACK = 0` `:916`): the r2 landing spot is dx+dy = 7
   from cad's footprint, 7 > 2+2 — a bot that provably did not walk there. Write
   sites `:1834-1836`/`:1854-1855` (core scan) and `:2376-2379` (builder scan,
   no distance gate inside vision) buffer the write; first read r4 = 2 in 36/36
   games. Consistent with the plank's claimed wild precision 1.000.
2. **The permanence is owned by the plain proximity re-trigger, not the ferry.**
   The ferry test arithmetically cannot re-fire late (dx+dy is bounded by the
   map, rnd+2 grows without bound; the r6 throw already fails 7 > 8). What
   re-arms `SLOT_ATK_RND` every round is `:1837` (enemy gunner/sentinel within
   anchor-measured d² <= 64): cad's opening push parks sentinels at (10,3) d²=1
   and (9,4) d²=5 [seat A] / (10,11) and (10,9) both d²=2 [seat B] — and a
   RemoveEntity scan over the full games shows **zero enemy sentinel removals**
   (we destroy nothing near home; snapshots r100/r200/r300 show them standing).
   The 50-round decay window `:1858-1869` therefore never opens once, in 500+
   rounds. Meander is also in the companion's turret-trigger map class (enemy
   *home* ring at anchor d² 36/25 <= 64), so even a passive cad would pin it.
3. **Value 2 has no distinct consumer.** Grep over the file: every read of
   `SLOT_UNDER` outside the write sites tests `!= 0` or truthiness (`:2228`,
   `:2616`, `:2624`, `:2644`, `:2887`, `:3578`, `:3876`, `:4180`). The widened
   0/1/2 latch is trigger-only by design (comment `:903-905`). So "latched at 2"
   is behaviorally identical to "latched at 1": the damage is the generic
   under-siege mode — ammo drip to floor 12 (`:2024`, `:2032-2035`), siege
   reserve +16 on all economy spending past r120 (`:2226-2231`), converge
   (`:4180-4194`), melee recall (`:2676-2692`), counterbattery waiver
   (`:3748-3764`) — held on for the whole match.

The one write-site nuance, same as the companion's: the replay records no store
writes, so core scan vs builder scan as *first* writer is not distinguishable
from the data; both fire on the same sighting and write the same value. The
first-read-r4 timing is consistent with the sighting landing r3 on both seats.

### Confidence

**High** on all three legs: the throws, the ferry arithmetic, the parked
sentinels' distances and permanence, and the consumer grep are each direct
measurements or single-line source reads.

### What would change the answer

- A cad_probe variant with no launcher that still produces `[[4,2]]` (would mean
  a false positive path exists; none was found).
- Any `SLOT_UNDER == 2`-specific consumer added since `_v93w` (re-grep on the
  builder's head before reusing this claim).

---

## Q3 — The seat split

### Verdict

**The map is exactly mirror-symmetric; the split is manufactured by our own
seat-asymmetric opening (absolute-direction spawn/site/path choices), which puts
seat A's only economy chain through the contested lane and seat B's along the
safe back row — and then by what occupies each chain's critical tile, which is
the only thing OS changes.** Seat B's 6/6 "grind win" is a real core kill: our
OS standoff sentinel shoots the enemy core down the shared x=12 column for 500
rounds.

### Evidence

**Our opening is not mirror-symmetric.** Spawns r0-r4: seat A (10,4), (13,5),
(12,2), (12,5), (13,4) — the lane-facing ring; seat B (13,12), (12,12), (11,12),
(10,9), (13,10) — the back row (the mirror of (10,4) is (10,9), which seat B
reaches 4th, not 1st). Consequence: seat A's first harvester lands r5 on
lane-side ore (16,6) and its link path approaches the core through **(13,5)**,
one tile from the lane; seat B's lands r6 on back-row ore (16,11) with the path
along row 12, touching contested ground only at the terminal seat (12,12).

**What blocks each path** (the Q1 mechanism, applied per seat):

| arm | seat A blocker of (13,5) | seat B blocker of (12,12) | seat B delivery |
| --- | --- | --- | --- |
| `w` (OS on) | our counterbattery sentinel, r5 | cad gunner, r16 (ties our linker's r16) | never |
| `woff` (OS off) | cad gunner, r6 | **none — we build it r16** | **r17** |
| `wb` | our counterbattery sentinel, r5 | cad gunner, r16 | never |

Seat A's critical tile is occupied by r5-r6 in *every* arm — by us (OS on: the
defender's counterbattery sentinel under the bleeding waiver) or by cad (OS off:
its first counter-gunner, which sites reactively and takes the best free
core-adjacent seat). That is why OS-off does **not** restore seat A. Seat B's
critical tile is contested only in the OS-on arms: with our OS sentinel standing
at (12,9), cad's first counter-gunner arrives r16 at (12,12) — winning the race
against our r16 link build; with OS off, cad's first gunner arrives r28 and
takes **(12,9) itself** (the vacated OS tile), and our chain completes at r16,
first delivery r17, 1,640 Ti (seed 1; W4/6 across seeds).

**The OS walker exists on both seats** (OS gate `os_gate_open:1271-1288` is
seat-symmetric here: anchor-to-anchor d² = 49 <= `OS_D_SQ_MAX` 49, exact core
pairing). Walker tracks (instruments): seat B's role-0 walks (13,12)->(13,9) and
plants r4 at (12,9); seat A's role-0 walks (10,4)->(11,5), **stalls at (11,5)
r2-r10** — next to cad's thrown raiders landing at (10,4)/(10,5) — and plants
late, r11, at (12,5) (the `OS_HOMEDEF_EXEMPT` hold window `:2675` names exactly
this loitering-builder constraint).

**The grind-win mode decoded** (all 6 arm_w seat-B seeds identical): winner=B,
`win_condition = core_destroyed`, r517 — not tiebreakers. Our sentinel (12,9)
faces N; enemy core tile (12,4) is 5 tiles up the column, d²=25 <= 32, and
sentinel shots ignore obstacles. 93 core-damage events from r5, fed by the ammo
drip (978 Ti converted — effectively the whole match's passive income; bank
median 12). The same sentinel strangles cad's economy in the lane: cad collects
130 on seat B vs 1,450 on seat A, which is why cad's gunner push never kills us
there (5 damage events on our core, vs 44-86 on seat A where cad's push ends us
r185-281).

### Confidence

**High** on the blocker table, the OS delta, and the win-condition decode (all
direct replay measurements, seed-invariant). **Medium** on the *root* of our
opening asymmetry being absolute-direction scan order — the asymmetric spawns
and picks are measured, the specific line (core spawn `for d in DIRECTIONS` /
`_pick` tie-breaks) is inferred from the companion's established pattern, not
instrumented per-line. **Low-medium** on attributing cad's r16-vs-r28 gunner
timing to our OS sentinel specifically — it is the only difference between the
arms, but cad's internal siting logic was not source-decoded here.

### What would change the answer

- A `woff`-style arm with the counterbattery build suppressed for r0-r10 on seat
  A: if (13,5) stays free and the chain completes, seat A's collapse is fully
  reduced to the blocker mechanism; if cad takes the tile anyway (as in woff),
  seat A needs the path re-plan fix, not an opening tweak.
- Decoding cad_probe's gunner-siting code would settle the r16/r28 attribution.

---

## Q4 — Wild transfer

### Verdict

**The zero-delivery shape is essentially absent in the wild: 5/79 wild meander
games ever, 1/11 in the v77+ era (where `SLOT_UNDER=2` exists), and 0/2 in
v77+-era games against wild CAD — both of which delivered by r17-r18. The probe
matchup is the trigger, not the map.** The one modern wild zero (v78 vs Landers)
is the same defect family and proves the shape *can* fire in the wild — against
an opponent that parks shelling turrets near our core.

### Evidence

Archive scan (read-only): all `replay_archive/*.replay26` with OpenSverige in
the meta, filtered to 25x15 maps — every hit has cores (11,3)/(11,10), i.e.
meander: **79 games, v64-v80, 30+ distinct opponents**. Instrumented each for
first harvester, first delivery, total collected:

- **Zero-delivery: 5/79** — v65 A vs Team 48 (288r), v68 B vs Team 48 (381r),
  v69 A vs CtrlAltDefeat (277r), v72 B vs SmartFridge (275r), v78 A vs Landers
  (524r). Three of five predate v77 (latch values 0/1 only), so the shape
  predates the FT plank and cannot be blamed on it.
- **v77+ era: 11 games, 1 zero.** The other 10 delivered r15-r49 (median ~21),
  collected 60-26,510.
- **Wild CAD on meander: 4 games.** v69 seat A: zero (277r). v74 seat B:
  delivery r18, 4,330 Ti. **v77 seat A: delivery r17** (390 Ti, won r103).
  **v79 seat A: delivery r18** (2,440 Ti, won r218). So the exact era whose
  probe games go 0-for-24 on delivery went 2-for-2 against the real opponent.
- **P6 caveat, confirmed and widened** (decode of the v79 game,
  `b4287ac4..._game_3`): wild CAD there is **version 117** and opens with *no
  launcher, no throws before r84, no forward sentinels, and never damages our
  core at all* (0 damage events in 218 rounds; its first turret is a home
  gunner). Our v79 shelled *its* core from r2 and ran an 8-harvester economy.
  The probe's frozen opening — permanent launcher + r2-r6 raider throws + r3-r5
  forward sentinels parked at d² <= 5 + early counter-gunners — is the entire
  physics of the collapse and does not match the current wild CAD.
- **The wild v78 zero decoded** (`a3e6dd54..._game_3`, vs Landers, seat A): same
  signature family — Landers parks a gunner at (10,6) (anchor d²=10) and shells
  our core continuously from r12 (145 damage events; latch never releases), both
  our chains stop 1-2 tiles short of the core seats ((13,2) never built; (13,5)
  only at r60, its successor (13,4) never), 0 delivery, cad-style siphon of our
  output by enemy belts, and 35 counterbattery gunner rebuilds at one tile
  (10,1) — the under-siege mode converting income to turret churn.

### Confidence

**High** on the counts (deterministic scan + instrument over the full archive).
**Medium** on "trigger is the probe opening" as a causal claim — supported by
2/2 v77+ wild-CAD deliveries and the v117 decode, but the archive holds no
v93w-vs-wild-CAD meander game, and wild CAD v117 is a different bot from
whatever cad_probe was frozen from.

### What would change the answer

- Any new wild meander game vs current CAD with our v80+: a delivery by ~r20
  would close the question; a zero would transfer the defect to the wild and
  raise its priority sharply.
- More Landers-class opponents (park-and-shell) appearing in the pool — the v78
  game shows the shape needs only "turret parked inside d²<=64 + continuous
  shelling", which is not CAD-specific.

---

## Fix-design implications

The builder owns fixes. The in-flight FB build touches fjordgate only and its
det set reproduces meander byte-identically — this read is input to a separate
future plank. Options the evidence directly supports, with risk surfaces; no
tuning beyond thresholds already in the file.

**M1. Re-plan on foreign blocker in `_build_next_link` (`:4822-4823`) — the
direct Q1 owner.** Pop-as-complete is only sound when the occupier is a friendly
conveyor/splitter (or the core); for anything else, drop the plan and re-plan
from `link_source` — the file already uses exactly this self-healing idiom two
paragraphs down (`:4840-4843`, HS ban clause: "dropping the plan is the
self-healing answer ... skipping one tile would leave a chain permanently
severed at that gap"). `_link_path`'s decoded branch already blocks foreign
buildings when planning (`:4487-4490`), so a re-plan routes around the blocker
by construction. *Risk:* a fully-enclosed core input set loops plan/fail —
needs a bounded retry; BFS cost is already CPU-gated (`:4500`).

**M2. Keep our own turrets off planned link tiles.** Seat A's arm_w severance
was self-inflicted: the defender's counterbattery sentinel (r5, (13,5)) landed
on the just-planned path. The HS seat-ban idiom (`lban`, `:2256-2262`) is the
in-file precedent; the link plan is per-unit state, so this needs the path (or
at least the core input seats) published or approximated. *Risk:* constrains
emergency turret siting exactly while shelled; must not regress the
counterbattery waiver's own measured meander case (`:3748` docstring).

**M3. `_has_acceptor` (`:4620-4631`) counts a dead-end belt as service.** Any
M1-class fix should also decide whether "adjacent conveyor" is enough or the
belt must reach the core; adjacency is the reason a severed harvester is never
re-wired. *Risk:* a real path check is new machinery; scope it with M1, not
separately.

**M4. The money leg is the companion's B/C, unchanged, plus meander's two extra
drains.** wb re-proves the off-by-a-few (bank ceiling 37 vs needed 38 = cost 22
+ `SIEGE_HEAL_RESERVE_TI` 16): conversion-floor fixes alone cannot clear
`_eco_spendable:2226-2231`. Meander adds (a) the ammo drip as an *unbounded*
sink while a grind sentinel keeps firing (978 Ti on seat B), and (b) melee
recall + on-ore squatting (`ORE_STEPOFF_MIN_WALLS = 80` gates step-off OFF on
this 8-wall map) as labour sinks. The companion's B (bootstrap exemption) and C
(reachable `_defend` bootstrap) apply verbatim.

**M5. OS on meander is a measured trade, not a defect.** OS-on seat B = 6/6
wins at r517 with zero economy (and it strangles cad's economy 130 vs 1,450);
OS-off seat B = real economy, 4/6. OS is not what breaks seat A (broken in all
arms). Any OS change is a vs-field battery question — flagged, not recommended.

**Interaction to flag:** M1 fixes *delivery on the probe det set*; Q4 says the
wild exposure today is small (1/11 modern wild games). The wild payoff of M1 is
insurance against the Landers park-and-shell class, which already exists in the
pool. The latch-response items (M4, companion B/C/E) are shared with fjordgate
and are where the two notes' evidence stacks.

---

## Self-checks

| claim | how verified |
| --- | --- |
| meander 25x15, cores (11,3)/(11,10), 24 ore, 8 walls, mirror-symmetric y->14-y | replay Map block decode; symmetry checked over all ore tiles + core anchors |
| replay Direction enum is 1-based | cad's seat-A belt decodes to a consistent into-core flow only under 1-based (e.g. (11,9) raw 5 = S outputs into core tile (11,10), 96 measured arrivals) |
| all 36 meander games latch `[[0,0],[4,2]]`, never release | `instruments.json` (36 rows printed, identical) |
| seed-invariance of every meander cell | `disc_results.json` + `instruments.json`: all 6 seeds per cell identical rounds/Ti/transitions |
| seat A chain gap at (13,5); sentinel there r5 built by 5th-spawned unit | build-event decode (`BuilderBuild` id x round x target) + spawn-order decode; (14,4) never built |
| our sentinel = (13,5) occupier in arm_w/wb; cad gunner r6 in woff; (12,12) cad gunner r16 in arm_w seat B; we build (12,12) r16 in woff | PlaceEntity decode per game |
| frozen stacks 3-4 deep; 38 (A) / 4 (B) harvester outputs; 29/38 of seat A's output onto cad's belt; `to_our_core = 0` | `DistributeResources` decode filtered to moves originating on our belt/harvester tiles |
| 18 buildings @ death = 16 conv + 2 harv + 2 sentinels built, minus losses | build-kind Counter + RemoveEntity + `disc_results.json` `a_buildings` |
| pop rule text and its self-description | source read `:4812-4857`, `:519-521` |
| no repair path (`_wire_on_build`/`_wire_tick`/`_has_acceptor`) | source read `:4593-4659` |
| bank medians 10-12; wb 20-37 for 101/101 rounds post-r120, max 37; builds byte-identical wb vs w | `UpdatePlayers` per-round decode; build-list equality |
| harvester cost 22 after 2 built; +16 reserve = 38 | cost-scale rule (project CLAUDE.md) + `SIEGE_HEAL_RESERVE_TI = 16` `:433`, `HUNT_MIN_RND = 120` `:412` |
| ammo totals 162/978/418/1025/191/198; attacks 119-366 | `CoreConvertAmmo` / `BuilderAttack` decode per game |
| `ti_floor = 12` under latch; drip mechanics | source read `:2024-2039` |
| cad throws own raiders r2/r4/r6; landing spots; `ferried()` arithmetic 7 > rnd+2 for r2/r4, fails r6 | MoveBuilderBot jump decode (>1 tile) + hand arithmetic on `:1301-1305` |
| cad forward sentinels at anchor d² 1/5 (A), 2/2 (B), never removed | PlaceEntity + full-game RemoveEntity scan filtered to enemy turrets + snapshots r100-r300 |
| ferry cannot re-fire late | `dx+dy <= 38` on a 25x15 map < rnd+2 for rnd >= 37 |
| `SLOT_UNDER == 2` has no distinct consumer | grep: all reads `:2228,:2616,:2624,:2644,:2887,:3578,:3876,:4180` are `!= 0`/truthy |
| OS gate open both seats (49 <= 49, exact pairing) | source `:1271-1288`, `OS_D_SQ_MAX = 49` `:1107`; anchor arithmetic (10-3)² |
| walker stall (11,5) r2-r10 seat A; plant r4 seat B | instruments `walker_track` + build events |
| seat-B win = core kill via (12,9)N sentinel, d²=25, 93 damage events, r517, 6/6 | replay `winner`/`winCondition` + FireTurret/UpdateHp decode; `disc_results.json` all seeds |
| cad collected 130 (B) vs 1,450 (A) | `disc_results.json` raw fields |
| FB arms reproduce meander byte-identically | `fb_results.json` (186/517 rounds, 0/1450 and 130/0 Ti — equal to arm_w) |
| 79 wild meander games; 5 zero-delivery; 1/11 v77+; wild-CAD 4 games with v77+ 2/2 delivered | archive meta join + Map-block dims filter + per-game instrument (script `wild2.py`, session scratchpad) |
| wild CAD v117 opening: no launcher, no early throws, 0 damage to our core | decode of `b4287ac4..._game_3` |
| v78-vs-Landers zero decoded as same family | decode of `a3e6dd54..._game_3` |
| melee recall active on meander (not in `keep_artillery_forward`) | source read `:2657-2692` (dims list excludes 25x15) |
| `ORE_STEPOFF_MIN_WALLS = 80`; squatters (6,0)/(6,14)/(19,1) parked r60-r180+ | source `:163`; per-round position decode of wb-A |
| md5s and repo HEAD | `md5 -q` this session; `git rev-parse` = `2ef0aa1` |

**Scope note.** Research-arm read: no bot edits, no arena runs, no platform
contact. Only this file written. Inputs: the builder arm's fjord_disc bundle,
`replay_archive/`, and `bots/_v93w` (+ named siblings) on disk. Decode scripts
(`mdec.py`, `mdec2.py`, `wildscan.py`, `wild2.py`) live in this session's
scratchpad, built on `tools/replay_census.py` per `tools/replay_schema.md`
(UpdateHp deltas decoded as 64-bit two's complement).
