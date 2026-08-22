"""SKALMAN v1 -- map data, constants and the verbatim map layer.

⛔ PROVENANCE.  Everything between the two IMPORT banners below is a VERBATIM
lift from the frozen benchmark `bots/_v542wave` per
`docs/research/SKALMAN-IMPORT-MANIFEST-2026-08-21.md` §8 steps 1-2:

  * `doctrine.py:1078-1172`  -> CORE_PAIRS / MAP_ALPHABET / MAP_CODES /
                                EXTRA_MAP_CODES (95 data lines)
  * `eco.py:82-223`          -> enemy_core_for, _CHAR3, _GRID_CACHE,
                                _decode_grid, the deliberately-no-memo
                                doctrine comment, _maptrust_pick (F1) and
                                known_map_for
    ⛔ CUT at eco.py:224-234 -- the `FS_V534_MAPTRUST = False` legacy branch
       is DELETED, not carried dead (manifest §1.5: it IS the v123
       wrong-grid-adoption bug).  The `if FS_V534_MAPTRUST:` guard goes with
       it; F1 is unconditional here.
    ⛔ F2 (`FS_MAP_SKIP` / `_fs_v534_skip_grids`, siege.py:66-86) is NOT
       imported (manifest §1.3, siege-only).  What survives is the PATTERN,
       re-applied at every SKALMAN per-map gate: a coarse (w,h,anchor)
       signature hit is a CANDIDATE, never a conclusion; confirm against the
       decoded grid; no match => run the default.  SKALMAN v1 has exactly one
       such gate (`known_map_for` itself) and it already works this way.

⛔ RENAME: `FS_V534_MIN_TILES` -> `SK_MAP_MIN_TILES`, `LOKI_TELEPORT_DSQ` ->
   `SK_TELEPORT_DSQ` (manifest §8.1).  No `SLOT_*` name is imported: all
   sixteen benchmark slots are occupied and five are multi-field packed
   (manifest §5.1), so the SK_SLOT_* allocation below is fresh.
"""

from fcode import Direction, EntityType, Environment, Position   # noqa: F401

# ===========================================================================
# 1.  DOCTRINE VERB FLAGS -- one flag per COPY verb, all default ON.
#     Ablation identity: flipping exactly one flag to False must reproduce the
#     no-verb signature on exactly one fidelity metric.  Read at the READ SITE,
#     never captured into a module-level derived default (manifest §5.3.3 --
#     the r197 lost-update class came from a derived default evaluated at
#     import).
# ===========================================================================
SK_ROLES = True      # COPY 8  four builders r0-r3, fixed roles for the game
SK_BELT = True       # COPY 8/#78  globally planned, terminated home belt
SK_DRIP = True       # COPY 7  need-based ammo drip at the core
SK_CAGE = True       # COPY 9  enemy-ring cage: nearest-empty first, lap, 7/8
SK_ORE_DENY = True   # COPY 1  harvester-death -> barrier-on-T + pre-emptive
SK_NEST = True       # COPY 5  band siting d^2 14-32, barriers then the gun
SK_DOOR = True       # COPY 6+2  home-ring clearance, sited off their axis

# --- v601 SURVIVABILITY PLANKS (s54 tape30 autopsy, ranked causes 1-3) ------
# Each is single-flag ablatable and defaults ON.  Provenance for every number
# quoted below: `scratchpad/s54_autopsy/tape30_autopsy.md`, n = 15 DISTINCT
# games (the *_s11/_s12 pairs are byte-identical; the seed is inert).
SK_HARV_ESCALATE = True   # PLANK 1 / CAUSE 1.  33/33 harvester deaths were
                          # annulus GUNNERS at d^2 26-45 of our core; median
                          # lifespan 9 rounds; 81.8% never delivered a stack;
                          # ONE gunner ate 22 harvesters off ONE tile over 321
                          # rounds.  The SK_REBUILD_ESCALATE ledger existed for
                          # CONVEYORS only (_belt_action) and was missing from
                          # _harvester_action -- we wrote the fix and applied it
                          # to the wrong entity type.
SK_BELT_COVER = True      # PLANK 2 / CAUSE 2.  0 of 42 dead belt pieces were
                          # inside any live turret of ours' firing line at
                          # death (and that ray is computed IGNORING obstacles,
                          # i.e. an upper bound).  12 of our 18 turrets sit at
                          # d^2 1-10 of our own core while 85.7% of the belt
                          # that dies sits at d^2 > 13.
SK_TARGET_PRIO = True     # PLANK 3 / CAUSE 3.  100% of the 9,126 damage landed
                          # on our core came from enemy SENTINELS at d^2 2-25;
                          # ~73% of unanswered enemy forward turrets were never
                          # touchable; 75.3% of our turret shots (618/821) and
                          # 74.8% of our pecks (1,280/1,712) landed on enemy
                          # BARRIERS.  We out-peck them 1,712 to 54 and spend
                          # three quarters of it on a wall.
# --- v602 NAVIGATION / ORDERING FIXES (s54 tape601 autopsy, §"WHAT A v602 -----
#     WOULD FIX", ranked by measured cost).  Every number quoted below is from
#     `scratchpad/s54_autopsy601/tape601_autopsy.md`, n = 15 DISTINCT v600 games
#     (seat A) vs 30 v601 game-sides (seats A and B), one NOISE_OFF `_v542wave`
#     opponent.  ⚠ Local fixture, one opponent: this PRIORITISES the fix, it does
#     not establish field prevalence (FIXTURE_OF_RECORD).
SK_CAGE_FIRST = True      # FIX 1 / CAUSE 1.  `_peck_priority` was inserted
                          # BETWEEN the seal-behind and the lap advance, and the
                          # enemy CORE footprint is orthogonally adjacent to
                          # EVERY seal tile by construction -- so from any seal
                          # tile the peck fired every round, returned, and the
                          # lap advance was never reached.  92.6% (286/309) of
                          # v601 walker lap ACTIONS were pecks against 7.4%
                          # barrier builds (v600: 31.0% / 69.0%); ring barriers
                          # per game 1.933 -> 0.767; worst single-tile dwell
                          # 10 -> 42/55 rounds.  The lap now takes priority and
                          # the walker pecks only when it has NO lap action.
SK_DANGER_NAV = True      # FIX 2 / CAUSE 2.  `self.armed_memo` has recorded
                          # every seen enemy turret TILE since v601 and NO MOVER
                          # EVER READ IT.  fimbulwinter seat A: 39 builder deaths
                          # on ONE tile (7,6), 100% of them from ONE gunner at
                          # (8,7) whose NW ray covers exactly {(7,6),(6,5)}; we
                          # inflicted 0 damage on it in 1000 rounds and walked 42
                          # bodies into it.  A remembered turret's covered tiles
                          # are now forbidden while any safe step exists.
SK_CYCLE_BREAK = True     # FIX 3.  ⛔ NOT A PLANK -- CHASSIS CORRECTNESS, flagged
                          # only so it can be ablated.  Share of builder steps
                          # that revisit the tile two back: 81.3% / 97.9%
                          # (fimbulwinter A/B), 91.0% / 72.7% (v600 control) --
                          # endemic, both bots, both seats.  `cardinal_direction_to`
                          # breaks ties horizontally and `_nav`'s fallback offers
                          # the opposite step, so a wall on the desired side
                          # produces an infinite A-B-A-B shuttle: all four
                          # stavkirke seat-B builders sat in one for 1000 rounds
                          # and built NOTHING.
SK_SENSE_NAV = True       # FIX 5(a).  `_bfs_direction` returned greedy whenever
                          # `map_grid is None` -- 10 of the 15 pool maps -- so on
                          # those maps navigation had NO WALL KNOWLEDGE AT ALL.
                          # Same root-cause family as the SK_ORE_SENSE bugfix:
                          # `_load_grid` promises "every consumer falls back to
                          # live sensing" and the FLOOD had no such fallback
                          # either.  Sensed walls (`map_walls`, filled by
                          # `_ore_scan`) now feed the flood; unseen = passable.
SK_ORE_SENSE = True       # ⛔ NOT A PLANK -- A PLAIN BUGFIX, flagged only so it
                          # can be ablated apart from the three planks.  7 of 15
                          # tape games built ZERO harvesters.  Root cause: when
                          # `known_map_for` returns None (10 of the 15 pool maps
                          # have no confirmed catalogue entry) `self.map_ores`
                          # is EMPTY, and `_home_keeper_move`'s ore loop is the
                          # ONLY thing that ever walks a keeper to ore -- so the
                          # keeper targets its own core and never sees an ore
                          # tile again.  `_load_grid`'s docstring promises "every
                          # consumer falls back to live sensing"; for ore there
                          # was no such fallback.  This adds one.

# --- v603 KILL-LEVER / TERMINUS FIXES (s54 tape602 autopsy) -----------------
#     `scratchpad/s54_autopsy602/tape602_autopsy.md`, n = 30 game-sides (15 pool
#     maps x both seats) of `bots/_v602skalman` vs the NOISE_OFF `_v542wave`.
#     ⚠ ONE authored opponent, local screen: this PRIORITISES each fix, it does
#     not establish field prevalence (FIXTURE_OF_RECORD).  The tape's headline is
#     the doctrine change these five encode: ALL 14,130 points of damage dealt to
#     the enemy core in 30 games were SENTINEL fire (zero pecks, zero gunner),
#     and we won 0 of 14 games with <=1 sentinel against 6 of 16 with >=2
#     (Fisher 2-sided p = 0.019).  THE KILL LEVER IS SENTINEL COUNT.  The cage is
#     a healer-denial multiplier on the gun, never a damage channel of its own.
SK_NEST_PAIR = True       # FIX 1 / autopsy candidate 3 -- THE KILL LEVER.  The
                          # siege engineer builds a SECOND band sentinel once the
                          # first is standing and the drip's own `need` covers two
                          # shots.  Measured: 48 sentinels in 30 games (median 2),
                          # 875 shots, 785 of them into the enemy core; one
                          # sentinel at 9 dmg/round barely out-paces the median
                          # 0.68 heal-tax their core absorbs, two does not.
                          # ⛔ NO BURST-BANK: the funding rhythm stays the drip
                          # (COPY 7).  The second gun waits on `need` arithmetic,
                          # not on a hoard.
SK_TRUNK_NEAR = True      # FIX 2 / autopsy candidate 1 -- THE EXCLUSION IS
                          # INVERTED.  `_trunk_tiles()` excluded d^2 <= 13 of our
                          # own core and 55 of 63 belt deaths (87.3%) happen
                          # INSIDE that cut; victim d^2 to our core has median 1.
                          # The killer class is THEIR BUILDER PECK at d^2 <= 13
                          # (44/63 = 69.8%), and our trunk gunners are 27/27
                          # survivors with 79 of their 157 shots already landing
                          # on enemy builder bots.  So the cover set now includes
                          # the NEAR trunk and the TERMINUS seats (the delivery
                          # tiles orthogonally adjacent to our core footprint),
                          # weighted where the deaths are.
SK_EVICT_ARMED = True     # FIX 3 / autopsy candidate 2 -- THE ONE-LINE INTERLOCK.
                          # `_clear_tile` was gated `not empty_seals`, so eviction
                          # was ARMED in 539 of 6,954 game-rounds (7.75%) and
                          # NEVER ONCE in 24 of 30 games.  The 8 -> 5 half of the
                          # seal gap is only reachable by eviction: 91 of the 137
                          # never-attempted seal tiles carried an enemy building
                          # and the kind census is 100% CONVEYOR (18,381
                          # tile-rounds, zero barriers).  When it did fire it
                          # converted -- exactly ten pecks per 20 HP conveyor,
                          # 6/6 games that armed it killed one, and glacierkeep_A
                          # reached 7 of 8 (above its own 6-tile ceiling) and held
                          # the enemy to titanium_collected = 0.
SK_COLLAR_GUNS = True     # FIX 4 / autopsy candidate 4 -- STOP THE MASS COLLAR
                          # PECKING.  2,179 of our 2,393 pecks (91.1%) went into
                          # their barriers on OUR core ring; 106 died, 238 were
                          # still standing at the end, and we out-spent them 4.8:1
                          # on melee while losing the exchange (their 495 pecks
                          # took our harvester->core connectivity from a possible
                          # 81% to 25%).  2 dmg/round into a 30 HP barrier they
                          # re-lay in ~1 round is not a race we can win.  The
                          # answer is FIX 2's terminus guns killing the BUILDER
                          # that lays it; the peck survives only where it is the
                          # binding gap, with a budget.
SK_CAGE_CEIL = False      # ⛔ FIX 5 / autopsy candidate 5 -- BUILT, MEASURED,
                          # AND SHIPPED OFF.  The mechanism claim is CORRECT and
                          # reproduces both ways: with it ON, rounds at/over the
                          # accept bar go 52 -> 1,062 over 30 games and games
                          # reaching it 2/30 -> 5/30, so `_attack_enemy_core` is
                          # no longer dead code.  THE OUTCOME GOES THE OTHER WAY:
                          # ON gives 6 kills / 4-by-r300, OFF gives 8 kills /
                          # 6-by-r300 on the same 30 games.  ⭐ AND THE AUTOPSY
                          # ITSELF PREDICTS THIS ONCE THE TWO FINDINGS ARE READ
                          # TOGETHER: walker pecks are 0.0% of all core damage
                          # (14,130 of 14,130 is sentinel fire), while the cage's
                          # measured worth is HEALER DENIAL -- heal-tax 0.49 at
                          # mean-held >= 3 against 0.71 below it.  Re-admitting
                          # the core to the peck ladder buys 2 damage a round and
                          # SELLS the seal work that multiplies an 18-damage gun.
                          # The candidate asked for the walker's damage channel
                          # back; the tape's answer is that the walker does not
                          # have one and should not be sold seats to look for it.
                          # Left in the tree, flagged, one line from live.
                          # ---- the original FIX 5 rationale, unchanged ----
                          # THE ACCEPT BAR WAS
                          # UNREACHABLE.  `sealed` cannot pass 8 - (their belt
                          # width) without eviction, measured ceiling median 5 of
                          # 8, so `sealed >= SK_CAGE_ACCEPT = 7` was FALSE in
                          # 30/30 games and every post-seal behaviour behind it --
                          # `_attack_enemy_core` included -- was dead code.
                          # SK_CAGE_FIRST drove enemy-core pecks 1,029 -> 0 and
                          # the v602 build report banked that as a win; on this
                          # tape it is the walker contributing no damage at all.
                          # The bar becomes the MEASURED ceiling.
SK_LAP_ADJ_SEAL = True    # FIX 6(a) -- FROM THE LAP-STALL DIAGNOSIS (s54 v603
                          # diag, `scratchpad/s54_v603/diag/`).  The six games
                          # where the lap never ran are THREE causes, not one,
                          # and the shared one (4 of 6) is a LAP-ADVANCE
                          # LIVELOCK: the walker reaches the ring, the forward
                          # lap tile is blocked -- by an enemy BODY in midgard_A
                          # for 41 straight rounds, by OUR OWN fresh seal in
                          # midgard_B for 14 -- the one-step detour is
                          # immediately undone by the off-lap nearest-empty-seal
                          # pool, and the result is a period-6-to-10 limit cycle
                          # that SK_CYCLE_BREAK (period 2, SK_CYCLE_HIST = 4)
                          # cannot see.  ⭐ THE CHEAP HALF, and it is also what
                          # the tape602 autopsy's §1.2 measured from the other
                          # side: `_seal_tile` was only ever called on the tile
                          # BEHIND, so a walker standing beside an empty seat it
                          # was not walking away from never built on it -- 25 of
                          # the 46 free-but-missed tiles had our builder
                          # orthogonally adjacent and the bank funded, 356 pooled
                          # opportunity-rounds, median 6 per tile, max 48.
                          # Now: seal-behind first (ledger V2 is unchanged and
                          # still has priority), then ANY orthogonally adjacent
                          # empty seal seat EXCEPT the forward lap tile, on-lap
                          # and off-lap alike.  The forward exclusion is what
                          # keeps V2 true -- a builder cannot stand on its own
                          # building, so sealing the tile we are about to step
                          # onto is how the doctrine we replicate self-demolished
                          # 74% of its lost ring barriers.
SK_IDLE_ACT = True        # FIX 6(b) -- A BODY WITH NO LEGAL MOVE MUST ACT.
                          # stavkirke_B body 58: born r140 boxed by an enemy
                          # LAUNCHER, two enemy BARRIERS and our own core
                          # footprint -- 0 moves, 0 builds, 0 pecks, 0 heals for
                          # 860 rounds.  icefloe_A body 218 is the identical
                          # shape for 227 rounds, so this is a repeated
                          # engine-legal spawn-box, not one map's quirk.  When
                          # the walker has no free neighbour at all, an adjacent
                          # enemy building of ANY type -- barrier included -- is
                          # "the path the current action needs", which is exactly
                          # `_clear_tile`'s carve-out, so it is peckable.
SK_SPAWN_EXIT = True      # FIX 6(c) -- NEVER SPAWN INTO A ZERO-EXIT TILE.
                          # `_spawn_plan` took the first direction `can_spawn`
                          # accepted, with no free-neighbour test; both boxed
                          # bodies above were born that way.  Two-pass the
                          # direction loop, preferring a tile with an exit.

# --- v604 NAVIGATION / TARGETING FIXES (s54, the v603 build report's queue) --
#     Provenance: `docs/research/BUILD-REPORT-v603skalman-2026-08-21.md` §"v604
#     queue", each item priced by the v603 diagnosis in
#     `scratchpad/s54_v603/diag/` (throat.py, why_no_lap.py) and by the tape602
#     autopsy.  ⚠ Same one-opponent local fixture: these PRIORITISE, they do not
#     establish field prevalence (FIXTURE_OF_RECORD).
SK_DANGER_COST = True     # FIX 1 / v604 queue 1 -- CLASS A THROAT.  ⛔ THE v603
                          # DANGER TERM IS A STEP PREFERENCE, NOT A PATH TERM,
                          # AND THAT IS WHY IT CANNOT CROSS A COVERED ROW.
                          # `_nav` split the four candidate steps into safe/risky
                          # and took `safe + risky`, so ANY legal step off the
                          # covered tile beat the step the flood asked for.  At a
                          # throat whose only route runs through a covered row the
                          # body therefore steps sideways, the flood asks for the
                          # same forward step next round, and the pair repeats:
                          # the bounded detour counter buys ONE forward step every
                          # SK_DANGER_DETOUR_MAX rounds and then resets.  Measured
                          # (v603 diag, helheim_A): the walker stood 40 rounds at a
                          # throat with the lap tile orthogonally adjacent.
                          # ⇒ danger moves INSIDE `_bfs_direction` as a PATH COST:
                          # entering a covered tile costs SK_DANGER_K extra steps,
                          # so a K-step detour is taken and a 20-step one is not,
                          # and a route that has NO danger-free variant is still a
                          # route.  `_nav` then follows the flood without
                          # re-ranking.  SK_DANGER_NAV still gates the danger set
                          # itself; SK_DANGER_COST = False restores the v603 veto
                          # form exactly (that is the ablation identity).
SK_CYCLE_K = True         # FIX 2 / v604 queue 2 -- CLASS B STALLS, THE CHEAP
                          # GUARD.  SK_CYCLE_BREAK sees PERIOD 2 only
                          # (SK_CYCLE_HIST = 4) and the measured lap livelock is
                          # PERIOD 6 TO 10 (v603 diag: midgard_A 41 straight
                          # rounds, midgard_B 14).  The ring extends to
                          # SK_CYCLE_HIST_K = 12 entries and any period k <= 6
                          # with two full repeats is detected.  ⛔ THE RESPONSE IS
                          # NOT A STEP CHANGE, because the cycle is not a stepping
                          # bug: it is TWO TARGETING SYSTEMS DISAGREEING (the lap
                          # skip-ahead and the off-lap nearest-empty-seal pool
                          # re-pick each other's detour away every round).  On
                          # detection the walker COMMITS to its current movement
                          # target for k + 2 rounds and the off-lap pool cannot
                          # re-pick inside that window.
SK_ONE_CURSOR = False     # ⛔ FIX 3 -- BUILT, MEASURED, AND SHIPPED OFF.  The
                          # MECHANISM claim is confirmed: with the cursor ON the
                          # class-B livelock cell is clean (midgard_A's longest
                          # period-k orbit 40 rounds -> 0).  THE OUTCOME GOES THE
                          # OTHER WAY on the same 30 games: ON gives 6 kills /
                          # 3-by-r300 / median kill r333, OFF gives 9 kills /
                          # 6-by-r300 / median r275.  ⭐ AND THE CHEAP GUARD IS
                          # WHY IT COSTS NOTHING TO DROP: with SK_ONE_CURSOR off
                          # and SK_CYCLE_K on, midgard_A's longest orbit is 11
                          # rounds -- under the 30-round bar -- so FIX 2 ALONE
                          # clears the cell FIX 3 was built to clear.  Splitting
                          # them was the point of building both.
                          # ⛔ WHY IT LOSES, read off `_cage_survey`: the cursor
                          # holds ONE objective for up to SK_CURSOR_GIVEUP rounds,
                          # and the seal seat it commits to is chosen from tiles
                          # currently IN VISION.  Eviction-armed rounds (no empty
                          # seat anywhere) run 15.6% with the cursor off against
                          # 3.3% with it on: committing to a distant empty seat
                          # keeps the ring nominally "open" and starves
                          # `_evict_seal`, which is the verb v603 measured as the
                          # only route to the 8->5 half of the seal gap.  The
                          # cursor is a correct answer to the livelock and a wrong
                          # answer to the cage.
                          # ---- the original FIX 3 rationale, unchanged ----
                          # v604 queue 3 -- CLASS B STALLS, THE STRUCTURAL
                          # REPAIR, flagged SEPARATELY from FIX 2 on purpose: the
                          # tape has to be able to say whether the cursor alone
                          # suffices.  `_cage_walker` carried TWO targeting
                          # authorities that disagree by construction -- the lap
                          # skip-ahead (`for k in range(1, 12)`) and the
                          # nearest-empty-seal pool at the bottom, which runs
                          # whenever the body is off-lap OR the skip-ahead found
                          # nothing.  ONE cursor now owns the objective (seal seat
                          # / eviction / lap advance); it is advanced only on
                          # COMPLETION or after SK_CURSOR_GIVEUP rounds, and the
                          # nearest-empty-seal pool becomes an INPUT to the choice
                          # rather than a mid-route override.
SK_BELT_EST = True        # FIX 4 / v604 queue 4 -- `belt_built` SURVIVES BODY
                          # REPLACEMENT.  It was a per-unit set of OUR OWN BUILDS
                          # (design build rule 6: module state is not shared
                          # between units), so a replacement keeper started with an
                          # empty ledger and every chain read as many-gapped --
                          # which is exactly when SK_COLLAR_ROUTE_GATE refuses, and
                          # is the v603 report's named root cause for that gate's
                          # measured negative.  Three additive parts:
                          #   (a) VISION ADDS, not only removes.  `_belt_watch`
                          #       already dropped a planned tile seen EMPTY; it now
                          #       also adopts a planned tile seen to carry a
                          #       FRIENDLY conveyor/splitter.  A keeper walking the
                          #       trunk re-derives the chain it did not lay.
                          #   (b) a CONFIDENCE round per tile, decayed on
                          #       non-observation (SK_BELT_EST_TTL).  A stale
                          #       PRESENT belief is kept but reported; the decay
                          #       drives (c) rather than deleting belief, because
                          #       deleting it is the failure that makes a keeper
                          #       walk at tiles that are already built.
                          #   (c) the 8 TERMINUS SEATS on the belt word, slot 5
                          #       b24-31 (one writer: keeper).  ⚠ AS-BUILT
                          #       DEVIATION: the brief asks for a bit per PLANNED
                          #       tile; slot 5 has 8 free bits and a plan can hold
                          #       30+, and a plan index is NOT body-independent
                          #       (the plan is recomputed per body).  The 8 tiles
                          #       orthogonally adjacent to our own core footprint
                          #       ARE canonically ordered and body-independent, and
                          #       they are where the collar fight happens (median
                          #       6.5 of 8 enemy-held at end of game).  So the
                          #       store carries the terminus, vision carries the
                          #       rest.
SK_BELT_EST_STALE_BUILT = True
                          # FIX 4, the DIRECTION of the decay, separated because it
                          # is a judgement and it must be priceable.  A tile whose
                          # newest PRESENT observation is older than
                          # SK_BELT_EST_TTL counts as BUILT for the gap walk.
                          # ⛔ THE OTHER DIRECTION IS THE BUG WE ARE FIXING: an
                          # unknown tile counted as MISSING is what makes a chain
                          # read many-gapped, and `_route_gaps` fires only on a
                          # chain with EXACTLY ONE gap.  Optimism here makes the
                          # gate fire MORE, which is the direction the v603
                          # negative says is wrong to suppress.

# ---------------------------------------------------------------------------
# v605 -- the s54 v605 queue (build report `_v604skalman`, 2026-08-21)
# ---------------------------------------------------------------------------
SK_PATH_ARBITER = False   # ⛔ FIX 1 -- BUILT, MEASURED, AND SHIPPED OFF: AN
                          # EXACT NULL, and the null REFUTES THE FINDING THAT
                          # COMMISSIONED IT.
                          # * OUTCOME: `tape_only_patharb` is IDENTICAL to
                          #   `tape_all_off` (== the v604 baseline) on every
                          #   column of the 30-game fixture -- 9 kills, 6 by-r300,
                          #   median kill 275, 46 belt deaths, 50 builder deaths,
                          #   13,440 Ti. Not "within noise": the same numbers.
                          # * MECHANISM: instrumented on the control cell
                          #   (helheim seat A), the gate ran 250 times and refused
                          #   ZERO. Every call returned "still reachable".
                          # * WHY -- AND THIS IS THE PART THAT MATTERS. The v604
                          #   report said helheim's ONLY throat is sealed by our
                          #   own nest. It is not. Flooding the map terrain with
                          #   our builds replayed in order, the core->enemy-ring
                          #   BFS distance is 13 before any build and 13 after the
                          #   whole nest cluster (barrier (11,5), barrier (10,6),
                          #   sentinel (10,4)); it reaches 15 only at r48 and stays
                          #   there. THE SOUTHERN ORE CORRIDOR (row 11) IS OPEN ALL
                          #   GAME. There is no last-route cut to refuse, so a
                          #   last-route arbiter has nothing to do.
                          # ⇒ The class-A stall is NOT a connectivity failure. It
                          #   is the vision-local flood described under
                          #   SK_BLOCK_MEMO below. The code stays in the tree,
                          #   flagged and scanned, because the premise is sound for
                          #   a genuinely single-throat map; it is off because on
                          #   this pool it buys two floods per candidate build and
                          #   changes nothing.
                          #
                          # --- what it does when it is on, unchanged ---------
                          # THE ARBITER, EXTENDED FROM
                          # BODIES TO ROUTES.  ⛔ THE DEFECT, AS REPORTED IN v604
                          # AND REFUTED ABOVE.  NOT
                          # THEORISED: on helheim seat A the cage walker visited
                          # 1 of 12 lap tiles in BOTH v603 and v604 with
                          # byte-identical tracks, and the v604 diagnosis found
                          # the map's ONLY THROAT sealed by OUR OWN NEST (two
                          # prep barriers plus the band sentinel).  The flood
                          # answered WEST even with the danger set forcibly
                          # emptied, so it is not a turret-avoidance failure and
                          # no fifth movement flag reaches it: the ROUTE was
                          # gone.
                          #   `free_neighbours` is the same discipline one level
                          # down -- it refuses a build that leaves a BODY with no
                          # step.  This refuses a build that leaves the TEAM with
                          # no route from our core to the enemy core.
                          #   Cheap form, in three parts:
                          #   (a) a LOCAL CUT PRE-FILTER (`_ring_runs`): a tile
                          #       can only disconnect 4-connected space if its
                          #       8-ring of passable neighbours falls into >= 2
                          #       circular runs.  O(8) grid reads, and it is
                          #       conservative in the safe direction -- it never
                          #       misses a real cut, it only over-nominates.
                          #       This is what keeps the flood off the hot path.
                          #   (b) ONE reachability flood our-core -> enemy-core
                          #       with the candidate tile marked blocked;
                          #   (c) only if that FAILS, a second flood WITHOUT the
                          #       tile.  Refuse only when the route existed
                          #       before and does not after -- a route already
                          #       lost is not this build's fault, and blaming it
                          #       would freeze every build behind the cage seal.
                          # ⛔ CONVEYORS AND SPLITTERS ARE NOT GATED, and that is
                          # an engine fact, not a shortcut: a builder bot walks
                          # onto a friendly conveyor tile (measured s54 on
                          # glacierkeep, `sk_common._bfs_direction` note), so a
                          # belt build cannot close a route.  The gate covers the
                          # five IMPASSABLE kinds only (barrier, harvester,
                          # gunner, sentinel, launcher).
                          # ⚠ THE BLOCKED SET IS WHAT THIS BODY CAN SEE plus the
                          # walls it knows: an unseen tile reads passable, so the
                          # test FAILS OPEN.  That is the correct direction for a
                          # veto (a false refusal costs a plank; a false pass
                          # costs what we already have) and it is why the builder
                          # that lays the seal -- which stands beside it and sees
                          # its own prior barriers -- is the one that can catch it.
SK_PATH_ARBITER_BUDGET = 900
                          # node budget for ONE reachability flood.  A 26x26 pool
                          # map is 676 tiles, so this settles the whole board and
                          # the cap is a runaway guard, not a tuning knob.  Budget
                          # exhaustion FAILS OPEN (allow the build), same as the
                          # CPU probe.
SK_BLOCK_MEMO = False     # ⛔ FIX 2 -- BUILT, MEASURED, AND SHIPPED OFF, A REAL
                          # NEGATIVE.  ⭐ THE MECHANISM IS CONFIRMED AND THE
                          # OUTCOME IS INVERTED -- the same shape as v603's
                          # cage-ceiling and v604's one-cursor, and it is the
                          # third time this line has bought a correct diagnosis
                          # and a worse bot.
                          # 30-game fixture, single-flag leave-one-out on the
                          # SHIPPING chassis (SK_NEST_EXIT on):
                          #     memo OFF   kills 11  by-r300 10  median kill 208
                          #                our core dead 18  builder deaths 51
                          #     memo ON    kills  9  by-r300  7  median kill 224
                          #                our core dead 20  builder deaths 76
                          # ⇒ it costs 2 kills, 3 by-r300 (the PROGRAMME-binding
                          # measure), 16 rounds of median kill, and +25 builder
                          # deaths.  It DOES do what it was built to do -- the
                          # helheim oscillation breaks and the walker reaches the
                          # enemy half -- so this is not a broken fix, it is a fix
                          # whose price is higher than its product.
                          # THE LIKELY REASON, stated as the hypothesis it is: a
                          # remembered blocker is a COMMITMENT.  The flood stops
                          # re-testing a tile it walked past once, so a body
                          # detours around buildings that have since died and
                          # around ground it could have crossed -- and the +25
                          # builder deaths say the longer routes are through
                          # worse ground.  Not tested; a v606 item, not a claim.
                          # --- what it does when it is on, unchanged ----------
                          # THE ACTUAL CLASS-A MECHANISM, and
                          # it is NOT the one the v604 report named.  Traced on
                          # the control cell (helheim seat A, r23-430, our own
                          # instrumented copy printing pos/target/flood answer
                          # every round):
                          #   at (7,5) `_bfs_direction` answers WEST -- CORRECT,
                          #     because our barrier (11,5) sits at d^2 16 <= 20
                          #     and is IN VISION, so the flood sees the east
                          #     pocket is shut;
                          #   at (6,5) it answers EAST -- because (11,5) is now
                          #     at d^2 25 > 20, OUT OF VISION, and the flood has
                          #     NO MEMORY OF BUILDINGS.  The pocket reads open.
                          # The body then walks east, re-sees the barrier, is
                          # told WEST, and repeats: 155 rounds on (6,5) and 154
                          # on (7,5) out of 407, one tile apart.
                          # ⛔ THE ASYMMETRY IS THE BUG.  `map_walls` is
                          # CUMULATIVE (`_ore_scan` adds and never removes), so
                          # TERRAIN is remembered -- but a BUILDING is read fresh
                          # from `get_nearby_entities` every call and forgotten
                          # the moment it leaves the disc.  Two floods one step
                          # apart therefore run on different maps.  `armed_memo`
                          # already keeps exactly this kind of memory, keyed on
                          # the TILE because a building is immovable; this is the
                          # same memory for the five IMPASSABLE kinds, and it
                          # feeds the nav template rather than the target picker.
                          # THE FORGETTING HALF IS NOT OPTIONAL: a tile inside
                          # the vision disc with no blocker on it is DROPPED in
                          # the same pass, at zero extra API cost, because a
                          # blocker there would have been in the entity list we
                          # just read.  A phantom wall is the failure mode this
                          # would otherwise introduce.
                          # ⛔ v606 ITEM 3: the TTL constant that used to live
                          # here (`SK_BLOCK_MEMO_TTL = 150`) is SUPERSEDED by
                          # `SK_BLOCK_TTL` below and has been removed rather than
                          # left beside its replacement -- two decay constants on
                          # one dict is how the wrong one gets read.
SK_NEST_EXIT = True       # FIX 3 / v605 queue 4 -- THE ENGINEER'S OWN EXIT, and
                          # it is a BUG FIX, not a plank: it removes an idle wait
                          # with no protective function, which is exactly the
                          # thing the v605 queue asked the kill-speed
                          # decomposition to look for.
                          # ⛔ WHAT THE DECOMPOSITION FOUND (v604 tape, 30
                          # game-sides, per-round bank ledger reconciled to 0
                          # residual rounds across 7,302 rounds).  The second
                          # sentinel's median r95 is NOT travel and NOT funding
                          # before the first gun: born r3, first move r5,
                          # band-adjacent median r21, prep 2 rounds, FIRST PLANT
                          # median r31.5 with a funding wait of ZERO in 29 of 30
                          # games.  The whole gap is S1 -> S2 (median 74 rounds),
                          # and 9 of 30 games contribute 1,059 idle rounds
                          # because the engineer is WALLED IN by its own two prep
                          # barriers plus its own sentinel from the round after
                          # S1 until it dies.  All nine never plant a second gun.
                          # ⛔ AND WE ARE ALREADY FASTER THAN THE BENCHMARK ON
                          # THE FIRST GUN (median r32 vs their r37 -- the "r21-58"
                          # in the queue is their spread, not their median).  The
                          # gap is the SECOND gun: theirs r63, ours r95, and
                          # their edge is that they DO NOT TRAVEL (their sentinels
                          # sit at median d^2 17 from their OWN core, so gun 2
                          # goes up beside gun 1). That is a doctrine question,
                          # not a constant; the boxed engineer is the free half
                          # and it is the only half fixed here.
                          # The other named component -- the second gun costing a
                          # median 80 Ti at a 268% cost scale our own 4 builders
                          # (+80) and 2 door gunners (+40) built -- is FILED, NOT
                          # FIXED: it is an allocation doctrine change, not a
                          # constant with no function.
SK_PATH_ARBITER_MEMO = 40 # rounds a refused site stays refused without re-running
                          # the flood.  ⛔ NOT PERMANENT: the board changes (a
                          # barrier dies, an enemy building is evicted) and a
                          # permanent ban is the ledger-V4 mistake.  It is a CPU
                          # memo with an expiry, not a `nest_bad`-style refutation
                          # -- except at the nest plant, where the caller ALSO
                          # writes `nest_bad` so `_pick_nest` re-sites instead of
                          # re-offering the same tile every round.

# ---------------------------------------------------------------------------
# v606 -- the s54 v606 queue (build report `_v605skalman`, 2026-08-21)
# ---------------------------------------------------------------------------
SK_BELT_BAND_AVOID = True # ITEM 2 -- THE BELT MUST NOT WALK INTO THEIR GUNS.
                          # SK_DANGER_COST (v604) re-shaped the routes bodies
                          # take and, through `_belt_parents`' shortest-path
                          # tree, grew the TRUNK into the enemy turret band.
                          # ⛔ MEASURED FIRST, on the three shipped tapes with
                          # `scratchpad/s54_v606/d2_band.py` (per-BUILD count,
                          # which reproduces the v605 report's 9/6 exactly):
                          #   v603  0 band builds, 0 band deaths, 0/30 games
                          #   v604  9 band builds, 6 band deaths, 1/30 games
                          #   v605  9 band builds, 6 band deaths, 1/30 games
                          # -- one cell, holmgang seat B, and EVERY piece that
                          # entered the band died.  Marginal death rate in the
                          # band is 6/9 = 66.7% against 45/385 = 11.7% overall.
                          # THE FIX IS THE SHAPE ALREADY IN `_plan_belt`: the
                          # planner already runs a two-pass cascade (avoid ore,
                          # then allow it if a harvester would otherwise have no
                          # route home, because a harvester with no route home is
                          # worth zero forever).  Band avoidance is a THIRD pass
                          # in front of that cascade, relaxed on exactly the same
                          # condition, so the "only route to the ore" exception is
                          # honoured by construction rather than asserted.
                          # ⛔ WITH THE FLAG OFF THE CASCADE COLLAPSES TO THE v605
                          # TWO-PASS FORM BYTE FOR BYTE -- that is what makes the
                          # ablation single-source.
SK_BELT_BAND_DROP = True  # ITEM 2, the half that BINDS.  The plain band-avoid
                          # term above is an EXACT NULL on this fixture and the
                          # instrument says why: in the one cell that carries the
                          # regression (holmgang seat B) `belt_ban` had escalated
                          # the harvester's SHORT route away by r81, so the band
                          # really was the only route left and the guard relaxed
                          # exactly as designed -- measured with
                          # `scratchpad/s54_v606/dbg_band` (a print-instrumented
                          # copy; LOCAL replays keep bot stdout): 5 of 12 replans
                          # relaxed, always on the same missing seat (5,10), with
                          # belt_ban = {(7,10),(8,8),(8,9),(8,11)} severing the
                          # direct southern chain.  ⇒ "unless it is the only route
                          # to the ore" is TRUE HERE, so the exception the v606
                          # item asked us to measure BINDS, and avoidance alone
                          # cannot move the number.
                          # THIS FLAG IS THE DOCTRINE ANSWER TO THAT: when only
                          # SOME seats are reachable band-free, plan those and
                          # DROP the rest rather than laying a chain through their
                          # guns.  Never drops the last seat.
SK_BELT_BAND_DSQ = 32     # the band is the SENTINEL reach r^2=32 measured from
                          # the ENEMY core footprint -- the same 32 that bounds
                          # our own nest siting (SK_NEST_DSQ_MAX), because it is
                          # the same weapon on the other side of the board.

SK_BLOCK_MEMO_EXPIRY = True
                          # ITEM 3 -- THE BLOCK MEMO, RE-TESTED WITH EXPIRY.
                          # ⛔ THIS FLAG IS DEAD CODE WHILE `SK_BLOCK_MEMO` IS
                          # False; it exists so the expiry can be ablated
                          # SEPARATELY from the memo it decays, which is the only
                          # way the v606 arm can be attributed (memo-on-long-TTL
                          # vs memo-on-short-TTL vs memo-off).
SK_BLOCK_TTL = 40         # ITEM 3 -- the memo's decay, in rounds.
                          # v605 built SK_BLOCK_MEMO, confirmed the MECHANISM
                          # (two floods one step apart ran on different maps
                          # because the flood had no building memory) and shipped
                          # it OFF because the OUTCOME inverted: 9 kills / 7
                          # by-r300 / median r224 / 76 builder deaths against
                          # 11 / 10 / r208 / 51.  The v605 report filed the
                          # hypothesis rather than claiming it: *a remembered
                          # blocker is a COMMITMENT, so bodies detour around
                          # buildings that are already dead*.  This is the test of
                          # that hypothesis and nothing else -- the memo decays
                          # after N rounds without a re-sighting AND is cleared
                          # the moment the tile is re-observed empty.
                          # ⛔ 40, not the v605 SK_BLOCK_MEMO_TTL of 150: 150 is a
                          # DECAY FOR A TILE NOBODY REVISITS (the v605 comment
                          # says so in as many words) and it is far longer than
                          # any detour is worth.  40 is ~2 cage laps.
                          # ⛔ SK_BLOCK_MEMO is the parent flag: with it OFF this
                          # constant is dead code, which is why the ablation runs
                          # the pair and not the TTL alone.
                          # ⛔ THE OTHER HALF OF "EXPIRY" WAS ALREADY IN v605 AND
                          # IS NOT NEW HERE, and saying so is the difference
                          # between a test and a claim: `_block_update`'s FORGET
                          # branch has always dropped a remembered tile that is
                          # inside the vision disc and absent from the entity
                          # scan.  What v605 did NOT have is a decay short enough
                          # to matter -- 150 rounds on a 1000-round match, and the
                          # detour it commits to is precisely the case where the
                          # body never comes back into vision of the tile to clear
                          # it.  So v606 changes ONE number and re-runs.
SK_BLOCK_TTL_V605 = 150   # PROVENANCE ONLY -- the v605 value, kept as a named
                          # number so the ablation arm that reproduces v605's
                          # memo-on tape does not hardcode a literal.
SK_BLOCK_MEMO_SCOPE = 1   # ⛔ v607 ITEM 3 -- ALL THREE FORMS MEASURED, MEMO
                          # STILL SHIPPED OFF (`SK_BLOCK_MEMO` above).  30-game
                          # arms on the v607 shipping chassis, control = that
                          # chassis (kills 11 / by-r300 10 / median 160 / botD 23):
                          #   scope 1 FORWARD  kills 11  by-r300  9  median 198
                          #                    botD 28  -- the SAME +38 median
                          #                    v606 measured for the global form,
                          #                    and one by-r300 worse.
                          #   scope 2 FAR      kills  9  by-r300  8  median 160
                          #                    botD 23  -- two kills and two
                          #                    by-r300 worse at no median gain.
                          # AND THE 3-GAME PROBE THAT GATED THEM SAID SO FIRST:
                          # on helheim seat A every scope (0/1/2) makes the game
                          # end at r135 with our core dead instead of r388 with
                          # our core dead, and lap coverage does NOT improve
                          # (4/12 -> 3-4/12).  ⇒ THE CONDITIONAL SPLIT IS
                          # REFUTED: the memo's cost is not carried by the home
                          # keeper's short routes and it is not avoided by
                          # restricting it to long ones.  The +38 median follows
                          # the memo wherever it is switched on.
                          # ⛔ AND A METHOD NOTE, because it changes how the v606
                          # probe should be read: that probe scored "our total
                          # deaths 12 -> 5" on this same cell WITHOUT normalising
                          # for game length, and the memo shortens the game from
                          # 388 rounds to 135.  Fewer deaths in a third of the
                          # rounds is not fewer deaths.
                          # --- the form definitions, unchanged -----------------
                          # v607 ITEM 3 -- THE CONDITIONAL FORMS.  v606 left the
                          # memo as a CONFIRMED MECHANISM with an inverted
                          # outcome: with the expiry the +25 builder deaths are
                          # GONE (23, identical to ship) and it buys +2 kills,
                          # but it costs +38 rounds of median kill and both extra
                          # kills land past r300, which the programme prices at
                          # 0.82 against us.  ⇒ the question v607 asks is not
                          # "does the memo work" (it does) but "is its cost
                          # separable from its product".
                          #   0  ALL      -- v606's global arm, the measured -38.
                          #   1  FORWARD  -- walker / engineer / denier only.  The
                          #                  HOME KEEPER's routes are short and it
                          #                  is the belt logistics that pay a
                          #                  stale commitment.
                          #   2  FAR      -- any role, target beyond
                          #                  SK_BLOCK_MEMO_DSQ.  Long routes need
                          #                  memory, short ones need freshness.
                          # ⛔ DEAD CODE WHILE `SK_BLOCK_MEMO` IS False, exactly
                          # like the expiry flag above.  The parent stays the ship
                          # decision; this only says WHICH form a memo-on arm is.
SK_BLOCK_MEMO_DSQ = 50    # v607 ITEM 3, scope 2's threshold.  d^2 > 50 is beyond
                          # every builder's own vision (r^2 = 20) and beyond the
                          # sentinel band (r^2 = 32) -- i.e. a target the body
                          # cannot see and must route to blind, which is the case
                          # the memo was built for.  Below it the body can see the
                          # ground it is crossing and freshness beats memory.

SK_DISENGAGE = True       # ITEM 1 -- THE BUILDER-DEATH JUMP, AND IT IS ONE CLASS.
                          # 17 (v603) -> 50 (v604) -> 51 (v605), unexplained
                          # through two releases.  ⛔ ATTRIBUTED, per death, on
                          # all three tapes with the validated damage-signature
                          # decoder (`scratchpad/s54_v606/d1_deaths.py`; role
                          # column validated by separation -- true labels give
                          # HOME_KEEPER mean min-d^2-to-enemy-core 230 vs SIEGE
                          # 40, a shuffle collapses it to 9.5):
                          #   CAGE_WALKER deaths ON THE ENEMY CORE'S LAP
                          #     14 -> 36 -> 34, killer SENTINEL 11 -> 41 -> 40.
                          #   Zero home-band deaths, zero no-damage removals,
                          #   zero launcher throws, on every tape.
                          # LEAVE-ONE-OUT ON THE v605 CHASSIS names the flag:
                          #   SK_DANGER_COST off  botD 51 -> 25  (26 of the +34)
                          #   SK_CYCLE_K     off  botD 51 -> 45  (6)
                          #   SK_BELT_EST    off  byte-identical (0)
                          # and the K dose curve 2/4/6/12 -> 69/53/51/58 says
                          # K=6 is already that curve's minimum, so RE-TUNING K
                          # IS NOT THE FIX.
                          # ⛔ AND THE DEATHS DO NOT BUY THE EVICTION PRESSURE
                          # THEY APPEARED TO.  Per-game, controlling for game
                          # length, r(deaths per 100 rounds, kill) = -0.003 and
                          # by-r300 +0.016 over 150 games.  The arm-level
                          # correlation with armed-round share (0.86) is carried
                          # by ONE CELL: stavkirke seat B holds 15 of v605's 51
                          # deaths and 958 armed rounds in a 1000-round game.
                          # Drop it and the arm with HALF the deaths has MORE
                          # armed share (dangercost_off 8.57% vs ship 6.05%).
                          # An r1000 is a defeat under the programme; an eviction
                          # headline carried by one is not a purchase.
                          # ⇒ FIX THE EXPOSURE, KEEP THE ROUTE.
                          # WHAT THE EXPOSURE IS: zero of the 49 forward deaths
                          # came from full HP.  The modal body enters its killing
                          # round at exactly 4 HP (38 of 49) -- it has already
                          # eaten two sentinel hits (40 -> 22 -> 4) and stood for
                          # the third -- with a median 6 rounds spent at hp <= 22
                          # first, MOVING in 32 of 49.  And the tree has no
                          # self-HP awareness at all: `ct.get_hp()` with no id
                          # occurs 0 times in the whole v605 source.
SK_DISENGAGE_HP = 22      # ITEM 1: a forward body at or below this HP stops
                          # paying the cost form's "the flood already priced the
                          # danger" waiver and gets the v603 STEP-LEVEL danger
                          # veto back -- one sentinel hit (18) from dead is the
                          # bar, which is why it is 22 and not a fraction.
                          # ⛔ IT DOES NOT STALL, and that matters because the
                          # step-level veto was removed for causing a 40-round
                          # stand: `_nav` still tries `safe + risky`, so a body
                          # whose every neighbour is covered still moves.  The
                          # only thing that changes is the ORDER, and the detour
                          # budget stops forcing a hurt body back into the ray.
                          # ⛔ FORWARD ROLES ONLY (cage walker, siege engineer):
                          # 49 of the 51 deaths are theirs, and a HOME KEEPER
                          # that will not stand in a covered tile is a home
                          # defence that will not defend.
SK_IDLE_ACT_ENGINEER = True
                          # ITEM 4(a) -- THE ENGINEER GETS THE CLAUSE THE WALKER
                          # HAS HAD SINCE v603.  `SK_IDLE_ACT` ("a body with no
                          # legal move must act") is wired into `_cage_walker`
                          # TWICE and into no other role.  ⛔ MEASURED, paths seat
                          # A, bot 146: 105 turns pinned on two tiles {(0,10),
                          # (0,11)} in a five-tile dead-end at x=0 -- sealed by
                          # map wall, our OWN core footprint, and their collar
                          # barriers -- of which 37 turns had `free_neighbours ==
                          # 0` AND a zero action cooldown.  A hundred free
                          # actions burned by a body that could have chewed the
                          # wall in front of it.  Same verb, same V7 give-up,
                          # same healing-race guard as the walker's copy.
SK_CYCLE_ALL_ROLES = True # ITEM 4(b) -- THE PERIOD-K DETECTOR RUNS FOR ONE ROLE
                          # OUT OF FOUR, AND THAT IS THE WHOLE REASON A 188-ROUND
                          # PERIOD-6 ORBIT SURVIVES IT.  Not the threshold, not
                          # the slack, not the re-arm: `period_cycle()` has one
                          # caller (`_cycle_commit`), which has one caller
                          # (`_cage_walker`).  ⛔ MEASURED, fimbulwinter seat A,
                          # bot 8 (ORE_DENIER, NOT a walker): 188 rounds orbiting
                          # {(5,4),(5,5),(6,4),(6,5)}, `period_cycle()` reads 6
                          # on 151 of them, and `commit_until` is -1 for every
                          # one -- no window ever opened, so nothing could expire.
                          # The competing authority is the same two-target shape
                          # the fix was written for: targets alternate (3,0) for
                          # 125 rounds and the enemy core for 63, with
                          # `_home_defence` consuming 126 of the 188 turns.
                          # ⛔ HOISTING THE CALL ALONE IS A NO-OP AND THE FIX SAYS
                          # SO: a window nobody CONSUMES changes nothing, so this
                          # flag carries BOTH halves -- the call moves to the
                          # shared dispatch and `_ore_denier` gains the consumer,
                          # placed ABOVE `_home_defence` because that branch is
                          # one of the two authorities being arbitrated.
                          # ⛔ WHAT IT DOES NOT REACH, stated so the tape is not
                          # over-read: 341 of 985 orbit-rounds on the five
                          # diagnosed cells (34.6%) are CONSTANT-target orbits --
                          # a `_nav`/`_bfs_direction` defect, not a targeting one
                          # -- and freezing a target that never moved is a no-op
                          # by construction.

# ---------------------------------------------------------------------------
# v607 (s55) -- ITEM 2: ALLOCATION ARM 2, PURCHASE ORDERING
# ---------------------------------------------------------------------------
SK_S2_PRIORITY = False    # ⛔ v607 ITEM 2 -- BUILT, MEASURED, AND SHIPPED OFF.
                          # A CLEAR NEGATIVE on the primary, and the mechanism
                          # WORKED: 30-game fixture, on the v607 shipping chassis
                          # (item 1 only), against that chassis as control --
                          #   OFF  kills 11  by-r300 10  median 160  botD 23
                          #        2nd-gun median r60  funding-wait 15/30 (783r)
                          #   ON   kills  9  by-r300  8  median 150  botD 37
                          #        2nd-gun median r53  funding-wait 14/30 (678r)
                          # ⇒ it buys the second gun 7 rounds earlier and takes
                          # 105 waiting rounds out, and it costs TWO by-r300 and
                          # FOURTEEN builder deaths.  Deferring the door gunner
                          # is deferring the answer to what is already shooting
                          # at our door, and the tape says our bodies pay for it.
                          # ⭐ ATTRIBUTED, and this is the part worth keeping:
                          # `SK_S2_DEFER_GUNS` alone reproduces the ON arm
                          # BYTE-IDENTICALLY in all 30 replays, and
                          # `SK_S2_DEFER_BARRIERS` alone is BYTE-IDENTICAL to the
                          # OFF arm.  The whole effect -- product and cost -- is
                          # the gunner deferral; the ore-denial barrier deferral
                          # is an EXACT NULL, so barrier scale is not what the
                          # engineer is waiting on.
                          # ⛔ AND THE BOUND IS NOT THE PROBLEM:
                          # SK_S2_PRIORITY_MAX 120 -> 60 is byte-identical to the
                          # ON arm, i.e. no deferral ever ran past 60 rounds.
                          # ⇒ SECOND ROAD CLOSED ON THE ALLOCATION QUESTION (the
                          # first was v606's door-gun cap 2 -> 1).  Cutting door
                          # gunners and DEFERRING door gunners both sell the kill;
                          # the funding wait is real and is not paid for out of
                          # the home guns.  v608 item: the wait is 678-783 rounds
                          # of S1->S2 and the money has to come from somewhere
                          # else -- or the second gun has to cost less.
                          # --- what it does when it is on, unchanged -----------
                          # v607 ITEM 2 -- THE SECOND ARM ON THE ALLOCATION
                          # QUESTION v606's counter FORCED OPEN, and the first
                          # arm (`SK_DOOR_GUN_CAP 2 -> 1`) is already REFUTED:
                          # by-r300 10 -> 6, kills 11 -> 9, Ti collected up to
                          # 19,700.  Cutting door gunners buys economy and sells
                          # the kill, so this arm does not CUT anything -- it
                          # REORDERS.
                          # THE MEASURED WAIT (v606 `fundwait.py`, the validated
                          # per-round bank ledger): funding-wait rounds > 0 in
                          # 15 of 30 games, and the class is S1->S2 in 15 of
                          # them (pre-S1 in 1), 783 waiting rounds pooled.  The
                          # engineer stands band-adjacent, able to plant, with
                          # the bank BELOW the sentinel cost -- while door
                          # gunners (+20% scale EACH, and the scale is ONE GLOBAL
                          # ADDITIVE factor that reprices the sentinel too) and
                          # ore-denial barriers (+1% each) are being bought.
                          # ⇒ INSIDE THE S1->S2 WINDOW ONLY, and only while the
                          # engineer is alive: the home keeper defers DOOR GUNNER
                          # purchases and the ore denier defers its NON-SEAL
                          # (ore-denial) barriers.  Everything else is untouched:
                          # the ammo drip, guns already standing, the cage SEAL
                          # barrier, the engineer's own prep barriers, the belt
                          # and the harvesters -- eco is the ammo line and the
                          # ammo line is what the sentinel fires.
                          # ⛔ ROLE ATTRIBUTION, CORRECTED AGAINST THE BRIEF: the
                          # brief said "the core defers door gunners and the
                          # walker defers non-seal barriers".  In this tree the
                          # core buys no gunner (the HOME KEEPER does, via
                          # `_door_action`/`_cover_gun_action`) and the CAGE
                          # WALKER's only barrier IS the seal (`_seal_tile`); the
                          # non-seal barrier verb is the ORE DENIER's
                          # `_deny_barrier`.  Same two purchases, correct owners.
SK_S2_DEFER_GUNS = True   # v607 ITEM 2, ATTRIBUTION SUB-FLAGS.  The arm defers
SK_S2_DEFER_BARRIERS = True
                          # TWO purchase classes and they are not the same
                          # decision, so a single flag would have produced one
                          # number and no attribution.  Dead code while
                          # SK_S2_PRIORITY is False, exactly like the memo scope.
SK_S2_PRIORITY_MAX = 120  # v607 ITEM 2 -- THE DEFERRAL IS BOUNDED, and it has to
                          # be.  The window opens on the FIRST gun's published
                          # round and shuts SK_S2_PRIORITY_MAX rounds later even
                          # if the second gun never lands, because "the engineer
                          # is alive" is not "the engineer can site" -- when
                          # `_pick_nest` returns None the engineer attacks the
                          # core instead and an unbounded defer would be pure
                          # loss for a purchase that is never coming.  A guard
                          # with no expiry is the v605 block-memo defect wearing
                          # a different hat.

# ---------------------------------------------------------------------------
# v607 (s55) -- ITEM 4: THE NET-DISPLACEMENT STALL DETECTOR
# ---------------------------------------------------------------------------
SK_STALL_NETDISP = False  # ⛔ v607 ITEM 4 -- BUILT, MEASURED, AND SHIPPED OFF.
                          # The DETECTOR is right and the RESPONSE is what fails.
                          # 30-game arms on the v607 shipping chassis (control:
                          # kills 11 / by-r300 10 / median 160 / botD 23):
                          #   BOX 3 (the measured value)  kills 9  by-r300 8
                          #                               median 160  botD 29
                          #   BOX 2 (fewer fires)         kills 11 by-r300 9
                          #                               median 170  botD 25
                          # ⇒ A MONOTONE DOSE CURVE IN FIRE VOLUME, which is what
                          # makes this a readable negative rather than a null:
                          # the harm scales with how often the commit window
                          # opens, so it is the COMMIT RESPONSE that costs, not
                          # the threshold.  Freezing the movement target of a
                          # body that is orbiting-while-building is not free --
                          # the census warned of exactly this (66 of 99 fire
                          # episodes land on a body whose lifetime action rate is
                          # >= 0.05 acts/round).
                          # ⇒ v608: a period-free orbit needs a response that is
                          # not "commit to the current target".  The detector
                          # itself is validated and stays in the tree behind this
                          # flag, at zero cost while it is off.
                          # --- the detector, unchanged -------------------------
                          # v607 ITEM 4 -- A SECOND ORBIT NET, PERIOD-FREE.
                          # ⛔ NOT a wider k: v606 measured SK_CYCLE_K_MAX 6->10
                          # as an EXACT NULL (30 byte-identical replays) and the
                          # surviving orbit is period TWELVE.  That road is shut.
                          # Constants set by measurement, not by the brief --
                          # see `netdisp_stall()` for the full census.
SK_STALL_W = 24           # window length, in rounds.  W=16 REJECTED on
                          # measurement: its episode count is NON-MONOTONE in the
                          # move threshold (24 episodes at M=8, 78 at M=12 --
                          # a stricter trigger fragmenting one fire into many),
                          # while W=24 and W=32 are stable (17/15/15).
SK_STALL_BOX = 3          # max(dx, dy) of the window's bounding box.  ⛔ 3, NOT
                          # the brief's 2: B2 covers 16 of 24 labelled episodes
                          # and MISSES the item's own headline cell
                          # (fimbulwinter seat A, k=12, box 3 in 107 of 107
                          # windows).  B3 covers 20 of 24 for 1.9x the fire
                          # volume; B4 buys 2 more for another 1.6x and is not
                          # worth it.
SK_STALL_MOVES = 12       # moves required inside the window.  This is the
                          # STANDING-STILL exclusion and nothing else -- a body
                          # that is not moving is `stuck`, which has its own
                          # counter and its own answer.  Measured: 0 pure
                          # standing-still fires at every M >= 8, against 5,430
                          # windows the box test alone would sweep in.  Every
                          # labelled orbit moves >= 17 of 23, so M costs no true
                          # positives anywhere in 8..16.
SK_STALL_COMMIT = 14      # rounds the commit window stays open on a netdisp
                          # fire.  The period detector sizes its window to the
                          # period it measured; this one has no period, so it
                          # takes the measured worst case (12) plus
                          # SK_CYCLE_COMMIT_SLACK -- "strictly longer than the
                          # orbit" is the property `_cycle_commit` is built on.

# ---------------------------------------------------------------------------
# v608 (s54) -- THE HOME ANSWER.  Every plank below answers ONE measured fact.
# ---------------------------------------------------------------------------
# THE FACT (v607 build report item 5, `loss_anatomy.py`, 826 core-damage events,
# 0 mis-attributed, all four controls fired): 19 of 19 losses on this fixture
# die to ENEMY SENTINEL FIRE ON OUR CORE -- zero gunner, ~zero peck -- and in 11
# of the 19 the core absorbs exactly 504 damage = 28 shots across a
# first-hit-to-death window of exactly 54 rounds.  Fifty-four rounds of
# continuous fire on our core that we never once interrupt: no heal, no counter,
# nothing.  Losses == our-core-dead == 19, so there is no clock tail here at all.
#
# ⛔⛔ RUNG 1 OF THE COMMISSIONED LADDER -- `SK_RAY_BLOCK`, "stand a body in the
# ray" -- IS REFUTED BEFORE BUILD AND IS NOT IN THIS TREE.  It is written down
# here, under the name it was commissioned by, so that a future grep finds the
# CLOSURE rather than the idea.  Two independent reasons, one of them a
# rules-level engine fact and therefore inside CLAUDE.md's explicit carve-out
# from "roads close only on live games":
#   1. THE ENGINE.  `docs/research/turret-line-blocking-2026-08-09.md`, a probe
#      with the gunner as its positive control (control PASSED: a friendly
#      barrier flips can_fire_from GUNNER True -> False):
#        * a SENTINEL's shot IGNORES entities in the line -- 18 damage landed
#          through a friendly BUILDER BOT *and* a friendly BARRIER onto the
#          target tile, and
#        * the pass-through friendlies took ZERO damage (40 -> 40, 30 -> 30).
#      A body in the ray therefore absorbs NOTHING from a sentinel.  The s49
#      fact the commission cites ("a tile shot resolves against the BUILDER BOT
#      on the tile, either team") is TRUE and is about the TARGET tile only --
#      and the target tile here is a CORE tile, which no builder bot can stand
#      on.  The two facts are consistent; only one of them is about blocking.
#      (It would work against a GUNNER, which IS blocked -- and 0 of 19 losses
#      are gunner damage.)
#   2. THE FIXTURE.  The opponent's own source
#      (`scratchpad/s54_fidtape/opp_v542wave_noiseoff/main.py:2258-2277`) picks
#      its sentinel target by a strict priority ladder, `TURRET_PRIO`, in which
#      CORE = 0 (best) and BUILDER_BOT = 3.  A body standing anywhere in the
#      line is never preferred.  So even the target-DIVERSION reading of the
#      plank -- which is a behavioural claim about the opponent and not an
#      engine fact -- is a null BY CONSTRUCTION on the fixture the leg would be
#      measured on.
# ⇒ the interruption verbs that remain are HEAL and COUNTER-KILL, and the ladder
#   below is those two, cheapest first.  Reported, not silently substituted.

SK_COREFIRE = True        # THE SENSOR, and it is the reason the other two
                          # planks can be cheap.  The CORE is the only unit that
                          # knows its own HP every round, so it -- not a builder
                          # guessing from geometry -- publishes "we are being
                          # shot" on SK_SLOT_COREFIRE.  ⛔ THE ALARM IS THE
                          # DAMAGE, NOT THE SHOOTER: the shooter tile is a BEST
                          # EFFORT extra (a sentinel at d^2 <= 32 of a core TILE
                          # can sit at d^2 50 of the core ANCHOR, i.e. outside
                          # the core's own r^2=36 vision, on a diagonal), and
                          # every consumer degrades to "heal" when it is absent.
                          # OFF is the ablation identity for the whole wave: the
                          # word reads 0 forever and all three planks are inert.
SK_COREFIRE_TTL = 24      # rounds the alarm stays FRESH after the last observed
                          # HP fall.  ⛔ IT HAS TO BE LONGER THAN THE HEAL CYCLE
                          # OR THE PLANK OSCILLATES: one medic is +4/round
                          # against 9, so the core still falls and the alarm
                          # re-arms every round -- but TWO medics (+8) can net
                          # the fall to ~1/round and a short TTL would then read
                          # "safe", disengage both, and re-open the stream.
                          # 24 is the opponent's own hold TTL (FS_V517_HOLD_TTL),
                          # i.e. the longest quiet a disciplined shooter takes
                          # before it re-probes.

SK_CORE_MEDIC = False     # ⛔ PLANK 1 -- BUILT, MEASURED, AND SHIPPED OFF.  It
                          # does exactly what it was built to do and buys
                          # nothing.  30-game arms (control = v607: kills 11,
                          # by-r300 10, our-core-dead 19, botD 23):
                          #   ALONE          kills 10  by-r300 9  core-dead 19
                          #                  core heals 694 -> 1214, longest
                          #                  unanswered streak UNCHANGED at 140
                          #   ON TOP OF P2   kills 12  by-r300 9  core-dead 17
                          #                  -- IDENTICAL to PLANK 2 alone on
                          #                  every outcome column, for +9
                          #                  builder deaths (30 -> 39) and
                          #                  +329 core heals (294 -> 623)
                          # ⇒ the heal RATE is real and the exchange is still
                          # lost: +4/round against 9 is a slower death, and a
                          # seated keeper is a keeper not laying belt.  The one
                          # thing it measurably moves is the streak MEDIAN
                          # (13 -> 11) and one game out of the >=40 class -- two
                          # rounds of median kill, for nine bodies.  Declined.
                          # ⛔ AND IT CORRECTS THE PREMISE IT WAS COMMISSIONED
                          # ON.  The v607 report says we "never heal our core";
                          # measured on its own tape, v607 lands 694 core heals
                          # across 30 games.  `_heal_action` was already picking
                          # the core whenever the keeper happened to stand
                          # beside it.  What was missing was never the verb.
                          # --- the plank, unchanged, for the ablation ---------
                          # ⭐ PLANK 1 -- HEAL THE CORE.  1 Ti -> +4 HP against
                          # one sentinel's 9 HP/round takes the 54-round window
                          # to ~100 rounds; a SECOND medic takes it to ~500.
                          # ⛔ THE VERB ALREADY EXISTED AND WAS NEVER REACHED.
                          # `_heal_action` heals the most-damaged adjacent
                          # friendly building and would already pick a 500-HP
                          # core over anything else -- it is ordered BELOW the
                          # door, the peck and the belt, and the keeper is
                          # standing on a belt tile when the core is being shot.
                          # So this plank is POSITIONING + ORDERING, not a new
                          # engine call, which is why it is the cheap rung.
SK_MEDIC_TI_FLOOR = 12    # the drip is never starved for the medic: heal only
                          # while the bank is strictly above this.  10 = one
                          # sentinel shot of ammo (SK_AMMO_FLOOR); 12 leaves the
                          # 2 Ti a peck also costs.
SK_MEDIC_HELP_HP = 200    # the ORE DENIER joins as SECOND medic only below this
                          # core HP.  One medic is a losing race (net -5/round)
                          # and two is a near-stall (net -1); the second body is
                          # bought late because it is bought out of the denial
                          # verb, which is the plank that opens the lane.
SK_MEDIC_SEAT_DSQ = 25    # how far a body will walk to take a medic seat.  The
                          # keeper's measured forward-action share is 0.000 and
                          # that property is load-bearing -- this fence keeps it.

SK_COUNTER_PECK = True    # ⭐ PLANK 2 -- MARCH THE DENIER AT THE GUN.  40 HP at
                          # 2 damage a peck is 20 builder-turns and 40 Ti, and
                          # the shooter is at d^2 <= 32 of a core tile BY
                          # CONSTRUCTION (that is the sentinel's own reach), so
                          # this is a HOME-AREA verb, not a raid.
                          # ⛔ WHY IT IS NEW WHEN LEDGER V5 ALREADY MARCHES THE
                          # DENIER: V5 marches it at SK_SLOT_THREAT_POS, which is
                          # the NEAREST enemy building on our ring -- a collar
                          # barrier or their builder, essentially never the gun
                          # that is 5 tiles out killing the core.  This plank
                          # re-points the same march at the CORE-DAMAGER, and
                          # widens V5's own trigger to the corefire alarm so it
                          # still runs when the shooter sits outside the core's
                          # vision and the under-attack latch never sets.
SK_COUNTER_RAY_ONLY = False   # ⛔ SUB-FLAG FOR ATTRIBUTION, and it is here
                          # because the shooter identification has THREE rungs
                          # and only two of them are observations.  Rungs 0/1
                          # walk the turret's actual FACING RAY onto our
                          # footprint; rung 2 accepts a SENTINEL whose REACH
                          # covers a core tile with no readable facing -- the
                          # 19/19 prior standing in for a fact we could not
                          # read.  True drops rung 2, so the difference between
                          # the two arms IS the cost (or the value) of the
                          # inferred rung, measured rather than argued.
SK_COUNTER_PECK_DSQ = 100 # fence on the march, in d^2 of OUR core.  Same fence
                          # and same reason as `_escalate_target`'s (v601 PLANK
                          # 1): the annulus this answers is d^2 <= 32, so the
                          # fence costs the plank nothing and cannot turn a home
                          # role into a raider.

# ======================================================================
# v612 -- THE ONE NAMED BUGFIX OF THIS WAVE.  DEFAULT ON.
# ======================================================================

SK_MARCH_TEAMCHECK = True # ⭐⭐ v612 FIX 1 -- THE LATCHED MARCH TILE IS
                          # VERIFIED ENEMY-OWNED AT FIRE TIME.
                          # ⛔ THE DEFECT, PRE-EXISTING SINCE v608 AND LOCATED
                          # BY A DRIVEN PROBE (v611 build report §5, not by
                          # inspection): `_counter_target` returns a TILE that
                          # was remembered when an enemy turret stood on it.
                          # `armed_memo` is tile-keyed and outlives the entity
                          # by design (v601 PLANK 1 -- a turret is a building
                          # and cannot move).  When the turret dies and OUR OWN
                          # relay is later laid on that tile, `_counter_march`
                          # walks up and pecks it: `can_fire` is team-blind and
                          # nothing downstream stops it.  23 pecks into our own
                          # conveyor/harvester across the v611 tape.
                          # ⛔ WHY IT IS NOT `SK_COUNTER_LIVE_TGT` (GATE D).
                          # GATE D invalidates a latch whose tile is EMPTY, is
                          # gated on `is_in_vision` at TARGET-SELECTION time,
                          # and was MEASURED WORSE ALONE (v609: the freed body
                          # goes and wastes its turns on a live tile instead).
                          # This guard fires at the moment of the SHOT, on a
                          # tile the body is orthogonally adjacent to -- so the
                          # read cannot fail for vision reasons -- and it
                          # refuses exactly one thing: damaging our own
                          # building.  The two are separately ablatable and
                          # GATE D stays OFF.
                          # False = v611's behaviour, and it is the DIRTY
                          # CONTROL for this wave: with it off the own-pecks
                          # come back.

SK_HOMEDEF_TEAMCHECK = True  # ⭐ v612 FIX 1b -- THE SAME DEFECT AT ITS SIBLING
                          # SITE, FOUND BY THE SAME DRIVEN PROBE AND SHIPPED
                          # DEFAULT OFF BECAUSE IT WAS NOT COMMISSIONED.
                          # ⛔ WHAT THE PROBE FOUND.  With FIX 1 on, the v612
                          # launcher-ON tape still carries 10 own-pecks -- ALL
                          # of them yggdrasil seat B r81-90 into our conveyor at
                          # (26,24) -- and the call site is NOT
                          # `_counter_march`.  It is LEDGER V5 (`_home_defence`,
                          # the `ct.fire(threat)`), marching at
                          # SK_SLOT_THREAT_POS: a TILE published by the CORE
                          # when it last saw an enemy there.  Store writes are
                          # buffered a round and the slot is never cleared, so
                          # the body arrives at a tile that our own relay has
                          # since taken, and pecks it.  Identical class to FIX
                          # 1, different slot.
                          # ⛔ DEFAULT OFF, AND THE REASON IS THE WAVE'S
                          # IDENTITY, NOT DOUBT ABOUT THE BUG: this wave was
                          # commissioned as ONE named fix, and both guards are
                          # provably INERT on the shipped chassis anyway (the
                          # driven probe reads 0 own-fires from either site
                          # across the 30-game SK_HOME_LAUNCHER=False tape).
                          # The measured arm is `hlonfix2`; the builder types
                          # the verdict on promoting it.

# ======================================================================
# v609 -- THE GATES ON PLANK 2.  All default OFF: with every flag below at
# its default this tree is BYTE-IDENTICAL to the v608 shipped tape, which is
# the wave's identity control.
#
# WHY THERE ARE GATES AT ALL.  v608's counter-peck bought kills 11->12,
# our-core-dead 19->17 and an unanswered-streak median 26.5->13, and paid
# by-r300 10->9 -- ONE game, `icefloe_seatA` (kill r136 -> our core dead
# r129).  The v609 diagnosis (build report) attributes the M1 seat-A belt
# fall 42.1->28.9 to exactly TWO games, and in BOTH of them the new belt
# death is an ENEMY BUILDER pecking a conveyor at d^2 1 of OUR CORE while the
# denier is away at the gun (icefloe r80 killer at (2,14), jotunheim r163
# killer at (7,5)).  That is the mechanism these gates are aimed at: the
# march is not free, it is paid for out of the home ring.
# ======================================================================

SK_COUNTER_YIELD_HOME = False  # v609 GATE A -- THE NEAR EMERGENCY OUTRANKS
                          # THE FAR ONE.  v608 placed the counter-peck ABOVE
                          # ledger V5 unconditionally, so a body chewing our
                          # belt one tile from the core loses the arbitration
                          # to a gun five tiles out.  With this on, the march
                          # stands down (and V5 answers) while the published
                          # home threat sits within SK_COUNTER_YIELD_DSQ of
                          # our core.  Barriers are excluded on v603 FIX 4's
                          # own argument -- a barrier does not chew anything.
SK_COUNTER_YIELD_DSQ = 8  # how close the home threat must be to outrank the
                          # gun.  d^2 8 is the core's own action ring plus a
                          # diagonal; both measured belt-killers stood at
                          # d^2 4.
SK_COUNTER_HP_MAX = 450   # ⭐⭐ v609 GATE B -- THE DECIDING FIX OF THIS WAVE.
                          # An HP CEILING on the march: 0 = OFF (v608's
                          # behaviour, the denier marches on the first scratch).
                          # Read off the alarm word's own quantised HP field
                          # (CF_HP_UNIT = 4), so the real quantity is HOW MANY
                          # SENTINEL SHOTS THE CORE ABSORBS BEFORE THE DENIER IS
                          # SPENT: 500 -> 480 -> 464 -> 446 -> 428 as published.
                          # ⛔ WHY.  Traced on icefloe seat A: the v608 march
                          # fires at round 40 on ALARM ROUND 1 at cfhp = 480 --
                          # 96% core HP -- to answer a sentinel our own gunner
                          # #65 was already killing (the 4 counter-pecks bought
                          # its death ONE round earlier).  The cost was
                          # second-order and enormous: the denier vacating (4,11)
                          # was the only gap in a wall/harvester line, which
                          # flipped `_bfs_direction` for the HOME KEEPER from
                          # WEST to EAST at r42, which put the keeper on an ore
                          # tile occupied by an enemy gunner, which cost 13 turns
                          # of pecking and then the second harvester (r46), its
                          # entire route home (r47-r58), four cage seals and the
                          # r95 siege sentinel that killed their core at r136 in
                          # v607.  titanium_collected 460 -> 140, bank at 0 for
                          # 35 rounds, our core dead r129.
                          # ⭐ THE DOSE IS IN SHOTS AND IT IS A PLATEAU:
                          #   1 shot  (<=480)      EXACT NULL, byte-identical
                          #   2 shots (472..464)   kills 13, by-r300 10
                          #   3 shots (460..446)   kills 13, by-r300 10  <- ship
                          #   4 shots (440)        kills 13, by-r300 10
                          #   6 shots (<=400)      kills 12, by-r300 10
                          # 450 is the middle of the 3-shot band, i.e. "the core
                          # has lost 10% before we sell a builder-turn for it".
                          # It does NOT disable the plank: 16 of 17 alarm games
                          # still peck (94.8% of pecks retained).

SK_COUNTER_LIVE_TGT = False  # v609 GATE D -- INVALIDATE A DEAD SHOOTER TILE.
                          # `armed_memo` is TILE-keyed and never cleared when
                          # the tile is OBSERVED EMPTY, and `_counter_march`
                          # only checks `get_tile_building_id` once ADJACENT --
                          # so on icefloe seat A the denier marched at (5,16)
                          # for 24 rounds (r49-r73) after the sentinel there
                          # died at r48, ping-ponging adjacent/not-adjacent.
                          # ⛔ MEASURED ALONE IT IS WORSE, NOT BETTER (arm_live,
                          # the diagnosis agent's own control): the cell loses at
                          # r152 instead of r129, because a body that stops
                          # wasting turns on a dead tile goes and spends them on
                          # a LIVE one.  The waste was a symptom; GATE B is the
                          # disease.  Measured again on top of GATE B below.

SK_COUNTER_SOFT_BODIES = True   # ⭐ v609 GATE E -- PRICE BUILDER BODIES INSTEAD OF
                          # REFUSING THEM, SCOPED TO THE COUNTER-MARCH ONLY.
                          # ⛔ THE MEASURED DEFECT (bifrost seat A trace): the
                          # denier held a period-10 orbit for 53 rounds (r105-
                          # r157) seven steps from its target with ZERO net
                          # displacement, and `step_to` returned True EVERY
                          # round -- so no stall detector this line owns can see
                          # it.  `_bfs_direction` pass 0 blocks builder bodies of
                          # both teams and only runs the body-free pass 1 when
                          # pass 0 finds NO goal; pass 0 always found one, via a
                          # 12-step detour.  One enemy body entering/leaving the
                          # r^2=20 vision flipped the route's HOMOTOPY CLASS
                          # between two adjacent stances: from (3,8) the answer
                          # is EAST, from (4,8) it is WEST, forever.
                          # THE FIX, three parts, all fenced to this flag and to
                          # `nav_soft_bodies` (set only around the counter-
                          # march's own `step_to`): price bodies at K=2 through
                          # the existing Dial's flood rather than walling them;
                          # HOLD instead of sidestepping when the routed tile
                          # holds a body (the sidestep locks into exact antiphase
                          # with a shuttling body -- measured, 30 rounds at zero
                          # progress one tile from the seat); and let the hold
                          # OWN the turn so the lower authority does not drag the
                          # body away.  A builder body is a 1-round obstacle, not
                          # a wall -- the same argument v604 used for danger.
                          # ⛔ IT DOES NOT FIX bifrost seat A, and the trace says
                          # why: that cell is TWO gates in series.  (0,4)'s only
                          # peck seats are (0,3) and (0,5); (1,4) is an enemy
                          # barrier, and an ENEMY BUILDER BOT sits on (0,5) for
                          # 50 of the 53 alarm rounds.  A builder cannot attack a
                          # builder, so the seat cannot be cleared, and (0,3)
                          # needs a ~27-step tour the router never considers.
                          # THE CELL REQUIREMENT IS STILL NOT MET; what changed
                          # is that the refusal is now NAMED rather than open.

SK_COUNTER_SENT = False   # ⛔ PLANK 3 -- BUILT, MEASURED, AN EXACT NULL, SHIPPED
                          # OFF.  ALONE it reproduces the v607 outcome on every
                          # column (kills 11, by-r300 10, our-core-dead 19,
                          # longest unanswered streak 140) and moves two
                          # sentinels; ON TOP OF PLANK 2 it moves two sentinels
                          # (73 -> 75) and nothing else.
                          # ⇒ THE GATE IS ALMOST NEVER OPEN IN TIME.  It needs
                          # SK_COUNTER_RNDS = 20 rounds of UNBROKEN alarm AND an
                          # identified shooter AND a spare sentinel's bank -- and
                          # PLANK 2 breaks the alarm long before 20 rounds
                          # accumulate (the shipped streak median is 11).  The
                          # two planks are ANTAGONISTIC by construction: the
                          # cheap rung starves the expensive one's trigger.
                          # That is a real finding about the ladder's shape and
                          # it is why rung 3 is not simply "rung 2 with money".
                          # --- the plank, unchanged, for the ablation ---------
                          # ⭐ PLANK 3 -- THE COUNTER-BATTERY, and the expensive
                          # rung: only after the cheap rungs have run for
                          # SK_COUNTER_RNDS and the same threat is still there.
                          # A sentinel CANNOT ROTATE (COPY 2), so a gun sited off
                          # their axis is fighting something that physically
                          # cannot shoot back, and 3 shots x 18 = 54 kills its
                          # 40 HP.  Sentinel, not gunner: reach r^2=32 vs 13, and
                          # the shooter is by construction at the edge of that.
SK_COUNTER_RNDS = 20      # rounds the alarm must have been continuously fresh
                          # before the purchase opens.  ~10 sentinel shots: long
                          # enough that a one-off peck or a stray shot never buys
                          # a 30-Ti turret and a +20% cost-scale step.
SK_COUNTER_SENT_CAP = 1   # ⛔ ONE, AND IT DOES NOT SPEND THE DOOR-GUN BUDGET.
                          # v606 refuted CUTTING door gunners (SK_DOOR_GUN_CAP
                          # 2->1, by-r300 10->6) and v607 refuted DEFERRING them
                          # (by-r300 10->8): they are load-bearing and this plank
                          # must not become a third way of selling them.  So the
                          # counter-battery carries its own cap and its own
                          # reserve, and the arm that measures it is its own flag.
SK_COUNTER_SENT_RESERVE = 20  # bank left standing after the buy, so the purchase
                          # cannot eat the drip's next conversion outright.
                          # ⚠ DISCLOSED DEVIATION FROM THE COMMISSION: the
                          # counter-battery plants NO prep barriers.  The
                          # engineer's prep barriers exist to buy a FORWARD gun a
                          # few rounds of life inside their answer; this gun
                          # stands inside our own ring under our own door guns,
                          # and every barrier is +1% on the ONE GLOBAL ADDITIVE
                          # cost scale that reprices the engineer's second band
                          # sentinel -- the exact purchase v607 measured as the
                          # thing we are waiting on.

# ---------------------------------------------------------------------------
# v610 -- THE BELT-TERMINATION AXIS.
#
# THE RE-VERIFY CENSUS (scratchpad/s54_v610/census.py + seatlife.py, run on the
# v609 SHIPPED tape, 30 games, 5/5 instrument controls fired).  Every number
# below is from that tape, not from tape602:
#
#   * ONE-BARRIER CLASS: 26 of 68 alive harvesters (38.2%) are BLOCKED at end
#     of game and land at EXACTLY gap 1 the moment enemy barriers are made
#     passable -- i.e. clear one enemy barrier, lay one conveyor, and that
#     harvester is delivering.  tape602 read 33/76 = 43.4%.  ⇒ THE CLASS HAS
#     NOT MATERIALLY MOVED across five versions.  With the 4 own-gap
#     harvesters, 30 of 68 (44.1%) are ONE BUILD from home.
#   * 180 of the 220 enemy barriers standing on the whole board at end of game
#     (81.8%) sit on OUR EIGHT DELIVERY SEATS.
#   * the seat kind census is 42,458 barrier tile-rounds against 142 sentinel
#     and ZERO conveyor -- #73's premise exactly: an enemy barrier on a
#     delivery seat can never qualify as REPAIRABLE, only as CLEARABLE.
#   * the mirror cage is unchanged: enemy-held median 6.5 of 8 at end, first
#     enemy building on a seat at median r11, and 0 of 30 games ever end clear.
#
# ⭐ AND THE CAUSE IS A TRIGGER, NOT A BUDGET AND NOT A HEALING RACE.
# Per-episode seat lifecycle over the same 30 games:
#     206 enemy occupancy episodes on our seats (6.9/game)
#     we EVER peck 25 of them = 12.1%
#     on the seats we ever touch we peck 78.1% of episodes AND KILL THEM
#     we touch 0.80 distinct seats per game of a median 8; ZERO in 12/30 games
#     ⇒ 84.5% of episodes sit on seats the tree never once considers.
# The verb works; it is never aimed.  The reason is structural: `_belt_evict`
# can only fire on a tile that is IN `belt_plan` and orthogonally adjacent to
# the keeper, and the single-source planner terminates on ONE seat per chain,
# so seven of eight seats are invisible to it for the whole game.
#
# ⛔ TWO HYPOTHESES MEASURED AND REFUTED BEFORE ANY CODE WAS WRITTEN, because
# both were plausible and both would have aimed the wave somewhere useless:
#   (1) "`belt_ban` closes the seats and the plan re-routes into nothing" --
#       instrumented live on glacierkeep seat A (the 8/8-held, 3-unreachable
#       game): `belt_ban` is EMPTY for all 201 rounds and the planner re-plans
#       exactly 3 times.  REFUTED.
#   (2) "`SK_COLLAR_PECK_CAP` is a per-TILE lifetime ledger, so a re-laid
#       barrier is unattackable" -- TRUE as a mechanism and visible in that
#       same trace (we spend exactly 15 pecks on (13,2), kill it at r48, seal
#       it at r49, they kill our seal at r145 and re-lay at r146, and the tile
#       is never contested again) -- but it is only 8 of 206 episodes (3.9%)
#       tape-wide, and its complement control reads the SAME attack rate
#       (12.5% vs 12.1%).  REFUTED AS THE DOMINANT CLASS, fixed anyway below
#       because it BINDS the moment the trigger is widened.
# ---------------------------------------------------------------------------
SK_SEAT_CLEAR = False     # ⛔⛔ v610 PLANK 1 -- BUILT, MECHANISM CONFIRMED,
                          # OUTCOME INVERTED, SHIPPED OFF.  THE LINE'S SEVENTH
                          # CASE OF THIS SHAPE AND THE CLEAREST ONE YET.
                          # 30-game arms on this chassis, PLANK 2 held ON:
                          #   PLANK 1 OFF : kills 14 · by-r300 11 · med 188.5
                          #                 · builder deaths 29 · belt deaths 40
                          #   PLANK 1 ON  : kills 11 · by-r300  7 · med 272
                          #                 · builder deaths 41 · belt deaths 32
                          # ⭐ IT DOES EXACTLY WHAT IT WAS BUILT TO DO.  Our
                          # pecks on our own delivery seats go 329 -> 1,347
                          # (4.1x); enemy barriers left standing on our seats at
                          # end fall 180 -> 162; enemy-held drops from a median
                          # 6.5 of 8 to 6.0; belt deaths fall 42 -> 31; M1 RISES
                          # (33.3/34.5 -> 36.8/37.1, the best belt connectivity
                          # this line has read); and the one-barrier class falls
                          # 38.2% -> 29.6%.  Every plank-level signature moves
                          # the right way.
                          # ⛔ AND IT COSTS THREE KILLS AND FOUR BY-R300, and the
                          # dose curve says the cost is the RESPONSE, not the
                          # volume -- by-r300 reads 7 at TOTAL=45, 7 at TOTAL=90
                          # and 6 at SK_SEAT_CLEAR_N=1, against 11 with the plank
                          # off.  A STEP, NOT A GRADIENT: any amount of aiming
                          # the keeper at the collar costs the same four.
                          # THE PRICE, NAMED: the keeper's TURN is the scarce
                          # resource, not the seat.  1,018 extra pecks are 1,018
                          # keeper turns not spent building, healing or
                          # answering -- builder deaths 29 -> 41, alive harvesters
                          # 68 -> 54, and the unanswered-streak median (v608's
                          # own plank) regresses 13 -> 19.  This is v603's
                          # 2,179-peck collar arithmetic returning at 1,347 even
                          # WITH the N=2 and 90-peck bounds binding.
                          # ⇒ THIRD ROAD CLOSED ON THE COLLAR: v603 killed the
                          # unbounded peck, v610 kills the BOUNDED, AIMED,
                          # per-episode-budgeted peck. The delivery seats cannot
                          # be bought with builder turns at any price we can pay.
                          # Left in the tree, flagged, one line from live, with
                          # every sub-constant ablatable -- the mechanism is
                          # sound and a FUTURE wave that can clear a seat without
                          # spending a keeper turn (a gun, a launcher throw)
                          # inherits a validated aim.
                          # ORIGINAL DESIGN NOTE: the eight tiles orthogonally
                          # adjacent to our core footprint stop being "whatever
                          # the belt plan happens to route through" and become a
                          # standing clear-target for the HOME KEEPER's action
                          # ladder AND its movement target.
                          # The eight tiles orthogonally adjacent to our core
                          # footprint stop being "whatever the belt plan happens
                          # to route through" and become a standing clear-target
                          # for the HOME KEEPER's action ladder AND its movement
                          # target.  An enemy BUILDING on a seat is pecked
                          # (barrier 30 HP = 15 pecks, conveyor 20 = 10) with the
                          # guards this line has already paid for, listed on
                          # their own constants below.
SK_SEAT_CLEAR_N = 2       # ⛔ HOW MANY SEATS ARE CONTESTED AT ONCE, AND THE BOUND
                          # IS THE WHOLE SAFETY ARGUMENT.  v603 measured what
                          # happens without one: 2,179 pecks (91.1% of our entire
                          # melee budget) into their collar, 106 barriers killed,
                          # 238 still standing at the end, out-spent 4.8:1 and
                          # losing.  We do not need eight seats -- we need ONE
                          # PER LIVE CHAIN, and the chains merge by construction
                          # in `_plan_belt`.  Two is one per chain plus one.
SK_SEAT_PECK_CAP = 15     # 30 HP barrier / 2 dmg.  ⭐ PER EPISODE, NOT PER TILE:
                          # the ledger is keyed on (tile, occupant entity id) and
                          # a NEW enemy building on the same seat is a NEW
                          # contest with a fresh budget.  `collar_pecks` is keyed
                          # on the tile alone and never reset, which is why the
                          # glacierkeep seat is conceded from r146 to the end of
                          # the game.  A cap that fires still bans, so a seat we
                          # genuinely cannot win is still abandoned.
SK_SEAT_PECK_TOTAL = 90   # per-GAME bound on the whole plank, in pecks.  Six
                          # barriers' worth.  This is the backstop that keeps a
                          # per-episode budget from re-creating v603's 2,179.
SK_SEAT_GUN_RACE = True   # THE HEALING-RACE EXCEPTION.  `_enemy_builder_adjacent`
                          # refuses a peck whose target a live enemy body can heal
                          # (+4 HP for 1 Ti against our 2 dmg -- a race we lose).
                          # It stays refused UNLESS one of OUR live turrets covers
                          # the tile, in which case pecks plus 7-or-18 damage a
                          # round beat +4.  Flag it separately: it is the only
                          # place this wave re-opens a guard the tree closed.
SK_SEAT_GUNS = False      # ⛔ THE TURRET HALF, BUILT AND SHIPPED OFF PENDING ITS
                          # OWN ARM.  `_target_pri` scores a BARRIER at
                          # SK_PRI_BARRIER = 0 and `_turret` skips `pri <= 0`, so
                          # NO gun of ours has ever fired at a seat-blocking
                          # barrier -- the docstring's "barriers are only attacked
                          # by the verb whose PATH they block" is true of pecks
                          # and has no counterpart in the turret path at all.
                          # Turning it on costs 20 ammo per barrier (5 gunner
                          # shots) against a drip whose whole job is funding the
                          # second sentinel, and v601 measured 618 of 821 turret
                          # shots landing on barriers as a DEFECT.
                          # ⛔ ARM RUN ON THE SHIPPED CHASSIS (this flag is
                          # INDEPENDENT of SK_SEAT_CLEAR -- the turret branch
                          # reads only this one -- so it was priced on its own
                          # rather than on the PLANK-1-on chassis):
                          #   OFF (ship): kills 14 · by-r300 11 · med 188.5
                          #               · belt deaths 40 · builder deaths 29
                          #               · Ti 12,940 · ammo-armed 8.81%
                          #   ON        : kills 12 · by-r300  9 · med 194
                          #               · belt deaths 34 · builder deaths 25
                          #               · Ti 15,530 · ammo-armed 4.41%
                          # ⭐ AND IT IS THE R1000_IS_DEFEAT TRADE IN MINIATURE:
                          # the guns DO protect the belt (deaths 40 -> 34, Ti
                          # +2,590, our bodies live longer) and the ammo they burn
                          # halves the armed share, which is the drip's second
                          # sentinel, which is the kill.  We decline the trade on
                          # the stated currency: economy is instrumental, it never
                          # scores.  Ablatable, one line from live, and the right
                          # flag to revisit if the ammo bill is ever paid
                          # elsewhere.
SK_TERMINATE = True       # ⭐ v610 PLANK 2, THE ONE THING THIS WAVE SHIPS -- A
                          # ONE-GAP CHAIN IS A COMPLETION TASK.  `_route_gaps`
                          # already names the tiles that are the SOLE missing
                          # link on some live harvester's route home; until now
                          # its only consumer was SK_COLLAR_ROUTE_GATE, which is
                          # shipped OFF, so the set was computed every round and
                          # thrown away.  30 of 68 alive harvesters on the v609
                          # tape are one build from delivering.
                          # MEASURED, 30 games, this flag the only difference:
                          #   OFF: kills 13 · by-r300 10 · med 170 · core-dead 16
                          #   ON : kills 14 · by-r300 11 · med 188.5 · core-dead 16
                          # ⭐ AND THE EFFECT IS ONE GAME, FULLY ATTRIBUTED --
                          # which is the honest way to read a +1 on n=30 rather
                          # than a claim the fixture cannot support.  Six replays
                          # differ; the whole gain is **stavkirke seat A, a r1000
                          # TIEBREAK converted into a CORE KILL AT r294**, i.e. a
                          # programme-defined defeat (R1000_IS_DEFEAT) turned
                          # into a by-r300 win.
                          # ⛔ TWO APPARENT COSTS, BOTH ARTEFACTS OF THAT SAME
                          # GAME, and both checked rather than asserted:
                          #   * median kill +18.5 is NOT a slowdown -- it is a
                          #     r294 kill being ADDED to a 13-kill population.
                          #     Of the kills that existed before, one moved 4
                          #     rounds faster and one 7 slower;
                          #   * delivered Ti -1,700 is stavkirke alone
                          #     (2,470 -> 700), because that game now ends 705
                          #     rounds earlier. Every other changed game's Ti is
                          #     flat or UP.  Verified per game: the five changed
                          #     cells sum to exactly the -1,700 tape delta.
                          # DISCLOSED: helheim seat B, already a loss, dies 25
                          # rounds earlier (r169 -> r144).
SK_TERM_FIRST = True      # the ACTION half: while a one-gap tile exists, the belt
                          # runs BEFORE `_harvester_action`.  A new harvester with
                          # no route home is worth exactly zero forever; the
                          # conveyor that connects an existing one is worth its
                          # whole future output.
                          # ⭐ ATTRIBUTION: THIS HALF CARRIES THE WHOLE PLANK.
                          # With the movement half OFF it still reads 14 / 11 /
                          # 185.0 -- the ship arm on the primary.
SK_TERM_MOVE = True       # the MOVEMENT half: the keeper's walk target prefers a
                          # one-gap tile over the nearest unbuilt planned tile.
                          # ⛔ AN OUTCOME NULL ON THIS FIXTURE, SHIPPED ON ANYWAY
                          # AND SAID SO PLAINLY: alone it reads 13 / 10 / 177,
                          # tying the control on every primary column.  It ships
                          # because it is the reach half of a plank whose action
                          # half pays, it costs nothing measurable (M1 seat A
                          # 34.2 with it, 33.3 without; every other column ties),
                          # and a fixture of one authored opponent is not where a
                          # reach mechanism would show.  It is the first thing to
                          # cut if this plank is ever re-priced.
SK_RELAY_SEAL = False     # ⛔ v610 PLANK 3 -- NOT BUILT.  NULL BY INCUMBENT GREP,
                          # AND THE BRIEF CONDITIONED IT ON EXACTLY THIS READ.
                          # Measured on the v609 tape: after an enemy building on
                          # one of our seats dies, OUR seal stands at median
                          # latency 1 round (15 of 17 within 1, 15 of 17 within
                          # 2).  We already deny the re-lay race at the speed the
                          # plank was going to buy.  THEIR re-lay after our seal
                          # dies is also median 1 (16 of 17 within 1), so the
                          # exchange is symmetric and there is nothing to win by
                          # acting faster.  The flag exists so the claim is
                          # greppable; there is no code behind it.

# ===========================================================================
# 1.z  v611 -- SK_HOME_LAUNCHER: THE COLLAR VERB THAT IS NOT A BUILDER TURN
# ---------------------------------------------------------------------------
# ⛔⛔ THIS WHOLE BLOCK IS A MEASURED ARM, DEFAULT OFF, AND THE DEFAULT IS NOT A
# VERDICT.  v610 closed the THIRD builder-turn road on our eight delivery seats
# (v603 unbounded peck, v610 bounded/aimed peck, v610 turret fire on the stated
# currency) and named the price in one line: THE KEEPER'S TURN IS THE SCARCE
# RESOURCE.  180 of the 220 enemy barriers standing at end of game sit on our 8
# seats; the mirror cage reaches a median 6.5 of 8 from r11 in 30 of 30 games;
# the one-barrier class is 26-27 of 68 alive harvesters.  The aim is validated
# and the verbs we own cannot pay for it.
#
# THE MECHANISM (engine facts, CLAUDE.md, `can_launch@` guard-matrix sweep):
# a LAUNCHER is 20 Ti base / +10% scale / HP 30 / vision-attack r^2=26, and it
# is FACING-INDEPENDENT.  `can_launch(bot_pos, target)` has NO TEAM CHECK and NO
# VISION GUARD: it picks up a builder bot FROM EITHER TEAM at pickup d^2 <= 2
# (the 8 neighbours) and throws it to any PASSABLE tile at 1 <= d^2 <= 26
# MEASURED FROM THE LAUNCHER.  0 ammo, cooldown += 1, POSITION-ONLY MUTATION.
# THE TARGET IS THE ENEMY COLLAR-LAYING BUILDER: to build a barrier on one of
# our delivery seats it must stand orthogonally adjacent to that seat, so it
# comes to us by construction.  Removing the LAYER costs no keeper turn at all.
#
# ⛔ WHAT THIS ARM IS NOT.  It is not aimed at the crash class (throwing a body
# to a map border so its own code raises off-map and the engine destroys it
# permanently).  That class is APPROVED and it is deliberately NOT the design
# here -- the throw target is chosen for DISPLACEMENT DISTANCE.  Any exception
# death observed post-throw is recorded as an observation, never as a target.
#
# ⛔ AND THE FIXTURE IS NOT NAIVE ABOUT LAUNCHERS.  `_v542wave`, the benchmark
# we screen against, SHIPS THEM AND FERRIES ITS OWN BUILDERS WITH THEM (probed
# on the v610 tape: auroraveil seat A, `launcher` planted team-B (9,15) r5 and
# (10,9) r7, their own builder 4 thrown (10,16)->(10,10), d^2=36, r6).  So the
# tape ALREADY contains d^2>1 builder jumps that are THEIRS, and any throw
# instrument that reads "big jump = our throw" is wrong before it is run.
# ===========================================================================
SK_HOME_LAUNCHER = False   # ⭐⭐ v615: FLIPPED ON.  THIS IS THE ARM.  Through v614
                          # this was False and the tree was byte-identical to the
                          # shipped chassis with it off (identity control, 30/30
                          # on v611).  The gate that kept it off was a PHASE
                          # boundary, and Magnus opened it 2026-08-22
                          # (PROGRAMME `NEXT_LINE_EXPERIMENTS`, verbatim: "You're
                          # free to experiment as much as you want, but a win at
                          # r1000 is still a loss and we dont want to build a
                          # rush bot").  v615 measures the arm IN COMBINATION
                          # with the anti-apron planks shipped since v611 --
                          # peck-focus, pluck-aware, the apron relay, the
                          # disengage guard and the home answer's HP gate --
                          # which is the untested cell: v611 measured the
                          # launcher ALONE, on a chassis that had none of them.
                          # ⛔ THE IDENTITY CONTROL IS NOW THE **OFF** ARM, and
                          # OFF must be byte-identical to the v614 tape.
                          # ⛔ AND `R1000_IS_DEFEAT` BINDS THIS ARM SPECIFICALLY:
                          # the launcher's measured effect is to buy ECONOMY, and
                          # an arm that converts losses into r1000 stalls is a
                          # NEGATIVE by the ruling even if every fidelity column
                          # improves.  The r1000 count is a PRIMARY here.
SK_HOME_LAUNCHER_MAX = 1  # ⛔ ONE.  A launcher is a BUILDING: immovable, it eats
                          # a tile forever, it counts against MAX_TEAM_UNITS=50
                          # and EVERY build adds +10% to the ONE GLOBAL ADDITIVE
                          # cost factor that inflates every later build of every
                          # type.  v600's first local game bought six gunners at
                          # +20% each and starved every other verb; the launcher
                          # is cheaper per unit and the same failure is one
                          # missing cap away.
SK_HL_MIN_ROUND = 10      # rounds before the keeper may spend the turn.  The
                          # collar's first enemy building lands at median r11 and
                          # reaches 4 of 8 by median r18, so a site chosen at r0
                          # is chosen with ZERO occupancy evidence and a site
                          # chosen at r30 is chosen after the cage is shut.  10 is
                          # the reading, not a tuning result -- dosed 0 / 10 / 25.
SK_HL_SITE_DSQ = 9        # site search domain: tiles within this d^2 of OUR core
                          # FOOTPRINT.  The launcher is a HOME building and the
                          # keeper's measured forward-action share is 0.000; that
                          # property is load-bearing (it is why only 2 of 22 body
                          # deaths were keepers) and this fence is what preserves
                          # it.  A delivery seat is d^2=1, its layers stand at
                          # d^2 <= 4, so 9 covers every pickup seat with a ring to
                          # spare.
SK_HL_SITE_MIN_COVER = 2  # ⛔ THE BRIEF'S BAR, VERBATIM: the site must have
                          # pickup reach (d^2 <= 2) to AT LEAST TWO seat-adjacent
                          # tiles.  A one-tile launcher is a 20 Ti +10% building
                          # that answers one approach lane out of eight.
SK_HL_THROW_MIN_DSQ = 16  # ⛔ THE BRIEF'S SECOND BAR: the site must have throw
                          # options at least this far out, toward the ENEMY half.
                          # A throw of d^2 4 is a free round back for them.
SK_HL_THROW_MAX_DSQ = 26  # ENGINE BOUND, not a choice (`can_launch`: 1 <= d^2
                          # <= 26 measured from the LAUNCHER).
SK_HL_PICKUP_DSQ = 2      # ENGINE BOUND, not a choice (pickup d^2 <= 2).
SK_HL_RESERVE = 40        # bank left standing after the buy.  The funding waits
                          # are already 18 of 30 games / 1,030 rounds and the
                          # drip's second sentinel IS the kill; a launcher that
                          # buys itself out of a sentinel has bought the wrong
                          # thing.  (Launchers use NO ammo, so the drip's need
                          # arithmetic is untouched -- only the bank is.)
SK_HL_PROBE_CAP = 12      # ⛔ CPU FENCE.  `get_nearby_tiles(26)` is ~80 tiles and
                          # each `can_launch` probe is an engine call; the throw
                          # picker sorts and then probes at most this many.  10 ms
                          # per unit per turn, and an overrun truncates run()
                          # mid-statement.
SK_HL_DROP_RING_DSQ = 13  # ⛔ NEVER DROP A VICTIM ON OUR OWN DOORSTEP.  A throw
                          # that lands their collar-layer inside our home ring has
                          # moved it from one of our seats to another one.  Same
                          # constant as SK_HOME_RING_DSQ, named separately so the
                          # ablation can drive it.
SK_HL_SITE_GIVEUP = 12    # ⛔⛔ THE TREADMILL BOUND, AND IT IS A MEASURED FIX,
                          # NOT A PRECAUTION.  The first cut memoised the site
                          # for the whole game and never re-validated it.  In
                          # 11 of 30 games the launcher was never built and the
                          # keeper walked at the dead site FOREVER: fimbulwinter
                          # seat B spent 656 KEEPER ROUNDS walking at (15,16)
                          # with `can_build_launcher` False 324 times, and that
                          # game is one of the six kills the arm lost.  That is
                          # v610's "the keeper's turn is the scarce resource"
                          # returning in a new hat, inside the very arm built to
                          # avoid it.  After this many rounds of walking or
                          # refused builds on one site, the site is BANNED and
                          # re-picked.
SK_HL_SITE_TRIES = 2      # ... and after this many banned sites the plank gives
                          # up FOR THE GAME.  A bounded search that never
                          # terminates is the same defect with more steps.
SK_HL_SEAT_DENSITY = False  # ⭐⭐ v615: FLIPPED OFF -- THE GEOM FORM IS THE ARM'S
                          # BASE, on the v611 measurement below and on the v611
                          # report's own v612-queue item 2 ("if the arm is ever
                          # priced again, price it OFF first").  The v615 brief
                          # names the GEOM variant explicitly; the density term
                          # is not re-litigated here, it is simply not shipped.
                          # (original comment, kept because it carries the read)
                          # site scoring weights each seat by the rounds we have
                          # OBSERVED an enemy building on it (the "mirror cage
                          # concentrates" term).  False = pure geometry, which is
                          # the control that says whether the density read buys
                          # anything at all.
                          # ⛔⛔ AND THE CONTROL SAYS IT DOES NOT.  MEASURED, 30
                          # games, treadmill-fixed chassis: DENSITY ON reads
                          # kills 10 / by-r300 9 / Ti 21,310; DENSITY OFF (pure
                          # geometry) reads kills 12 / by-r300 11 / Ti 22,270 --
                          # better on EVERY primary column, and by-r300 ties the
                          # OFF control exactly.  The designed value is kept as
                          # the default so the arm is reported as designed and
                          # the ablation carries the finding; a +2 on a 30-cell
                          # bar is not a resolvable difference and is not claimed
                          # as one.  IF THIS ARM IS EVER ADOPTED, THIS FLAG IS
                          # THE FIRST THING TO RE-PRICE.
SK_HL_TEAM_CHECK = True   # ⛔⛔ THE ENGINE HAS NO TEAM CHECK ON `can_launch` AND
                          # THIS IS THE ONLY THING BETWEEN US AND FERRYING OUR OWN
                          # KEEPER INTO THE ENEMY HALF.  It exists as a FLAG only
                          # so the guard can be driven to the other verdict in an
                          # ablation (arm `hl_noteam` -- a DIRTY control, never a
                          # candidate).  Nothing may ship with this False.
SK_HL_AFTER_S2 = False    # ⭐⭐ v616 -- THE ONLY ARM OF THIS WAVE, AND IT IS THE
                          # v615 REPORT'S OWN LEAD INVERTED.  v615 measured the
                          # launcher buying income and then spending the thing
                          # the income was for: the +10% scale surcharge lands at
                          # the launcher's MEDIAN BUILD ROUND r16, BEFORE either
                          # forward tube exists, and the S1->S2 funding wait blew
                          # out 995 -> 1,618 rounds (+63%) with two-tube games
                          # falling 24 -> 17 -- while the SAME arm drove the
                          # pre-S1 wait to ZERO (28 -> 0) and moved every parity
                          # column our way (Ti +48.6%, one-barrier class halved,
                          # apron possession +2.5pp).  The report's sentence:
                          # "the economy converts at S1 and not at S2 ... spend
                          # the Ti BEFORE the surcharge lands."
                          # ⇒ TRUE  = the keeper may buy the launcher ONLY while
                          #           BOTH forward tubes STAND (`_two_tubes`,
                          #           slot 7 b21 = NEST_SITE2_BIT, republished on
                          #           every forward-turret death by `_nest_watch`
                          #           so it is a fact about NOW, not a latch).
                          #           The surcharge then lands AFTER the kill
                          #           machinery is funded.
                          #   FALSE = v615's immediate form (buy at the first
                          #           affordable round >= SK_HL_MIN_ROUND).
                          # ⛔ IT GATES THE WALK AS WELL AS THE BUY, and that is
                          # not scope creep -- `_hl_walk_target` already refuses
                          # to walk at a buy it cannot make ("DO NOT WALK AT A
                          # BUY WE CANNOT MAKE.  A keeper standing beside an
                          # unaffordable tile is the v610 cost in a new hat").
                          # A gate on the buy alone would spend keeper walk
                          # rounds from r10 for a build that cannot happen until
                          # r68, which is the same defect the tree already names.
                          # ⚠ DISCLOSED, and it is the arm's own risk: `_two_tubes`
                          # is False in the ~20% of games that never reach two
                          # tubes, so in those games THE LAUNCHER IS NEVER BOUGHT
                          # AT ALL.  That is deliberate -- a game with no second
                          # tube has no kill machinery for the surcharge to be
                          # late to -- but it means the ON-afterS2 arm delivers a
                          # SMALLER DOSE than ON-immediate, and any read of its
                          # mechanism columns must carry that denominator.
                          # ⚠ AND IT IS A SUB-GATE, NOT A MASTER: it does nothing
                          # unless SK_HOME_LAUNCHER is True.
SK_HL_VICTIM_SEAT_ONLY = False  # True restricts pickups to builders that are
                          # orthogonally adjacent to one of OUR eight delivery
                          # seats -- the strict collar-layer form.  False also
                          # throws any other enemy builder that wanders into
                          # reach.  Default False because a builder inside d^2 2
                          # of a home launcher is at our door either way; the True
                          # arm prices whether the wider trigger dilutes the dose.

# ===========================================================================
# 1.85  v618 -- THE SEAT-DEFENCE PACKAGE  (Magnus, in-session 2026-08-22)
# ===========================================================================
# THE MEASURED PROBLEM, in one paragraph and it is the line's hardest.  The
# enemy COLLAR lands on OUR eight delivery seats at median r11; the mirror cage
# holds 6.5 of 8 from r11 in 30/30 games; 180 of the 220 enemy barriers standing
# at end of game sit on one of OUR seats (v610 census, re-verified on a
# re-derived v609 tape).  THREE BUILDER-TURN ANSWERS HAVE BEEN MEASURED AND ALL
# THREE ARE NEGATIVE -- v603's unbounded collar peck (2,179 pecks, 238 of their
# barriers still standing), v610's SK_SEAT_CLEAR (mechanism FULLY confirmed --
# seat pecks x4, M1 to the line's best 36.8/37.1, one-barrier class 38 -> 30% --
# and by-r300 7/7/6 at EVERY live dose against 11 off), and the launcher axis
# (three refutations: immediate, nil-dose, real-dose).  THE FINDING THEY SHARE:
# **THE KEEPER'S TURN IS THE SCARCE RESOURCE.**  Every answer that spends it
# loses more than the seat is worth.
#
# MAGNUS'S DESIGN, verbatim on the direction: *"deal with it using turrets ...
# not efficient that a builder pecks for 15 rounds"*.  Four planks, and the
# unifying property is that NONE of them is a sustained builder-turn spend:
#   1  SEAT PRE-CLAIM   -- 8 builds, ONCE, in the first ~30 rounds, on tiles the
#                          belt wanted anyway.  Occupancy is EXCLUSIVE (the
#                          engine requires an EMPTY tile to build), so a claimed
#                          seat cannot receive their barrier at all.
#   2  THE HOME GUNNER  -- ONE permanent turret, bought EARLY at low scale.  The
#                          playbook's own T19 "one home gunner, always", the
#                          verb BC ships at 2.4x the field rate and we have
#                          never fully built.
#   3  GUN ROUTEBLOCK   -- turret fire, not pecks, on the route-blocking collar
#                          barrier: 5 shots / 20 ammo against 15 pecks / 30 Ti
#                          AND 15 keeper turns.  The exchange inverts.
#   4  SEAT HEAL        -- 1 Ti / +4 HP cancels two peckers, at home, where we
#                          have the shorter supply line.
# Plus PECK DEMOTION: a builder peck at a collar barrier is refused on any tile
# a live gun of ours BEARS on -- v610's cap, tightened by the thing that
# replaces it.
#
# ⛔ THE CONVEYOR IS BAIT AND THAT IS PRICED, NOT OVERLOOKED (Magnus raised it
# in the same breath as the design).  20 HP falls to ten 2-damage pecks; the
# claim buys a TEN-ROUND STANDING COMMITMENT from an enemy builder at our door,
# which is exactly where planks 2 and 4 make it fatal.  A claim without the gun
# is a gift; the package is the plank, the flags are for attribution.

# --- PLANK 1 -- SK_SEAT_CLAIM ----------------------------------------------
SK_SEAT_CLAIM = False     # ⛔⛔ PLANK 1 -- BUILT, MECHANISM FULLY CONFIRMED,
                          # AND SHIPPED OFF.  F1 30 games: seat possession
                          # 0.136 -> 0.438 (ours) and 0.660 -> 0.487 (theirs),
                          # their landing episodes on our seats 6.9 -> 5.3 per
                          # game, 114 of our 203 claimed seat pieces chewed to
                          # death at ~10 pecks each = ~38 ENEMY BUILDER-TURNS a
                          # game committed to our own door -- THE BAIT WORKS
                          # EXACTLY AS DESIGNED.  AND by-r300 12 -> 8, Ti/game
                          # 483 -> 450.  The exchange is not turn-for-turn:
                          # their builders are many and cheap at our door, our
                          # keeper is ONE body, and 6.8 conveyors a game is
                          # +6.8% on the ONE GLOBAL ADDITIVE cost factor.
                          # (original note follows)
                          # The keeper lays OUR conveyor on an EMPTY
                          # delivery seat, facing INTO the footprint, inside the
                          # early window -- before their layer lands.
                          # ⛔ ZERO WASTE BY CONSTRUCTION: a delivery seat is a
                          # belt TERMINUS tile and the facing the claim picks is
                          # the facing `_plan_belt` would pick.  BFS from the
                          # core makes a seat's parent a CORE TILE, so the plan's
                          # `_card(cur - prev)` for that tile is "into the core"
                          # -- the same direction `_seat_face` returns.  When the
                          # belt arrives, `_belt_evict` sees one of OURS on a
                          # planned tile and records it as BUILT.
SK_SEAT_CLAIM_UNTIL = 30  # ⛔ THE WINDOW, IN ROUNDS, AND IT IS THE PLANK'S WHOLE
                          # COST FENCE.  The collar lands at median r11 and 4 of
                          # 8 seats are theirs by median r18; a claim laid at
                          # r200 is not a pre-claim, it is `_apron_action` in a
                          # new hat and it spends the scarce good.  After this
                          # round the plank is silent for the rest of the game.
SK_SEAT_CLAIM_ENEMY_FIRST = True  # ⭐ THE SITING RULE, AND IT IS THE DESIGN'S
                          # OWN ("site by measured collar-landing geometry").
                          # Their layer walks in from THEIR core, so the seats
                          # on the enemy-facing faces are the ones that get
                          # taken and the far-side seats are the ones we would
                          # be claiming against nobody.  Rank by distance to the
                          # ENEMY anchor, nearest first.  False = nearest-to-us
                          # first, which is arrival order and claims the wrong
                          # half whenever the budget binds.
SK_SEAT_CLAIM_MAX = 8     # per-GAME bound, in claims.  Eight is every seat; the
                          # spawn reserve below is what makes the EFFECTIVE bound
                          # seven or fewer.  Every bounded verb in this tree
                          # carries a game total as well as a window.
SK_SEAT_CLAIM_WALK = True # the MOVEMENT half.  Without it the action fires only
                          # where the keeper already stands, which is the 12.1%
                          # the v610 census measured for the peck form.
SK_SEAT_CLAIM_WALK_DSQ = 8  # ⛔ THE DETOUR FENCE.  The keeper only walks at a
                          # seat it is already this close to.  A seat is d^2 <= 2
                          # from our own footprint, so this keeps the claim inside
                          # the home lap and never competes with the harvester
                          # walk -- the v610 lesson says the cost of this class of
                          # plank is measured in keeper ROUNDS, not in titanium.
SK_SEAT_CLAIM_SPAWN_RESERVE = 1   # ⛔⛔ THE ENGINE HAZARD, AND IT IS SPECIFIC.
                          # `_spawn_plan` offers the core `p.add(d)` for the 8
                          # DIRECTIONS from the ANCHOR: three of those are the
                          # footprint itself, FOUR are delivery seats (N, NE, W,
                          # SW of the anchor) and exactly ONE is a corner that is
                          # not a seat.  Claim all four and a replacement builder
                          # can only be born on that corner -- which is a WALL on
                          # some maps.  Builder deaths run 29/30 games on the F1
                          # tape, so a blocked replacement is not a corner case.
                          # This many anchor-adjacent tiles must remain spawnable
                          # AFTER the claim, or the claim is refused.
                          # ⚠ AN UNREADABLE TILE COUNTS AS NOT-SPAWNABLE, i.e.
                          # the guard fails toward REFUSING the claim.

# --- PLANK 2 -- SK_HOME_GUNNER ---------------------------------------------
SK_HOME_GUNNER = False    # ⛔⛔ PLANK 2 -- BUILT, MEASURED, SHIPPED OFF, AND
                          # IT INVERTS ITS OWN ADVERTISEMENT.  The gun does the
                          # job T19 claims: enemy builder deaths 63 -> 88
                          # (+40%), income Ti/game 483 -> 550 (+14%).  It still
                          # costs the timely kill -- by-r300 12 -> 5, median
                          # kill 201 -> 315 -- and the shape is the v615/v616
                          # launcher finding on a new entity: a +20% scale
                          # surcharge landing BEFORE the kill machinery is
                          # funded.  ⛔ NOTE THE ROTATION GOES THE OTHER WAY
                          # FROM PLANK 3's: with SK_HOME_GUN_ROTATE off this
                          # arm reads 8 kills, not 12.  Rotating at a LIVE
                          # threat helps; rotating at a BARRIER is the defect.
                          # (original note) THE PLAYBOOK'S T19 FORM, "one home
                          # gunner, always".  ⛔ THIS IS NOT v610's SK_SEAT_GUNS
                          # AND THE DIFFERENCE IS THE WHOLE PLANK: that one was
                          # REACTIVE (bought at threat time, at whatever cost
                          # scale the game had reached, on the R1000-trade shape
                          # that got it declined).  This one is bought ONCE,
                          # EARLY, at low scale, sited by the MEASURED collar
                          # geometry, and it stands for the rest of the game.
SK_HOME_GUN_MAX = 1       # ⛔ ONE.  A gunner is +20% on the ONE GLOBAL ADDITIVE
                          # cost factor and it inflates every later build of
                          # every type.  The first local v600 game bought six
                          # and starved every other verb; that is why every
                          # turret verb in this tree is capped.
SK_HOME_GUN_MIN_ROUND = 10  # not before this round: the four builders are
                          # spawned r0-r3 and each is +20%, so a gunner bought
                          # at r4 is bought at a scale the economy has not yet
                          # earned.  The collar lands at median r11.
SK_HOME_GUN_MAX_ROUND = 120 # ... and not after this one.  Past here the buy is
                          # reactive, which is the form already measured and
                          # declined.  A window, not a floor: the plank either
                          # lands early or does not land.
SK_HOME_GUN_RESERVE = 40  # bank left standing after the buy.  Same constant the
                          # launcher arm used, for the same reason: the funding
                          # waits are 18/30 games and a purchase that empties the
                          # bank pays for itself out of the belt.
SK_HOME_GUN_SEPARATE_CAP = True   # ⛔ DISCLOSED DESIGN CHOICE, FLAGGED SO IT CAN
                          # BE DRIVEN THE OTHER WAY.  True = the home gunner has
                          # its OWN cap and does NOT spend SK_DOOR_GUN_CAP, so
                          # the door answer survives the plank.  False = it
                          # spends the door budget, i.e. the plank re-times an
                          # existing purchase instead of adding one.  The ON form
                          # buys strictly more turrets and therefore strictly
                          # more cost scale; the ablation prices that.
SK_HOME_GUN_ROTATE = True # the gunner may ROTATE (10 Ti, cooldown 1) toward the
                          # active threat side.  Gunners can; sentinels cannot.
SK_HOME_GUN_ROT_CAP = 6   # ⛔ BUDGET-CAPPED, per turret per game.  10 Ti and a
                          # round of cooldown each; ledger V7's lesson is that an
                          # unbounded re-aim is how 38 rounds and 152 Ti went
                          # into a target being healed faster than we damaged it.

# --- PLANK 3 -- SK_GUN_ROUTEBLOCK ------------------------------------------
SK_GUN_ROUTEBLOCK = False # ⛔⛔ PLANK 3 -- BUILT, MEASURED, SHIPPED OFF, AND
                          # IT CARRIES THE SHARPEST NUMBER OF THE WAVE, read
                          # straight off the wire as turret shots by victim
                          # over 30 F1 games:
                          #     control   core 1,452   barrier     0
                          #     PLANK 3   core   924   barrier 1,353
                          # 1,353 shots into collar barriers bought 528 FEWER
                          # shots into their CORE = 3,696 HP = SEVEN AND A HALF
                          # ENEMY CORES.  Ammunition is titanium 1:1 and the
                          # drip is need-based, so a barrier in a ray is not a
                          # free shot, it is a converted harvester.  Kills
                          # 14 -> 7.  ⛔ AND THE ROTATION IS MOST OF IT: with
                          # SK_HOME_GUN_ROTATE off the same plank reads 13/11
                          # instead of 7/6.  v601 already refused to spend 10 Ti
                          # and a cooldown turning to face a barrier; this
                          # plank's carve-out re-introduced that exact error.
                          # (original note) `_target_pri` scores a BARRIER 0 and 0
                          # is never fired at, so NO GUN OF OURS HAS EVER SHOT A
                          # COLLAR BARRIER -- 180 of them stand on our delivery
                          # seats at end of game.  A barrier on a delivery seat
                          # IS path-blocking (it is the tile between a harvester
                          # and the core) and the gun does 7 against a peck's 2.
                          # ⛔ SCORED AT SK_PRI_OTHER = 1, i.e. ABOVE IDLE AND
                          # BELOW EVERYTHING ALIVE.  A builder body in the same
                          # ray is SK_PRI_BODY = 2 and still wins -- killing the
                          # LAYER is worth more than killing what it laid, and a
                          # turret that prefers the barrier is a turret that lets
                          # the layer re-lay it.  v610's SK_SEAT_GUNS scored the
                          # same class at SK_PRI_HARVESTER = 3, ABOVE the body;
                          # that is the one substantive difference and it is
                          # separately ablatable below.
SK_ROUTEBLOCK_PRI = 1     # the rank.  1 = SK_PRI_OTHER (ship).  3 recovers
                          # v610's SK_SEAT_GUNS ordering exactly, for the arm.
SK_ROUTEBLOCK_ADJ = True  # widen from "on a delivery seat" to "on OR orthogonally
                          # adjacent to a delivery seat, inside the apron".  The
                          # census's laying positions are 15 distinct tiles, not
                          # 8: a barrier one tile off the seat still blocks the
                          # chain that feeds it.
SK_ROUTEBLOCK_DSQ = 5     # ... and `inside the apron` is SK_APRON_DSQ's own 5,
                          # in d^2 of our core FOOTPRINT.  Same constant, same
                          # census, deliberately not a second number.

# --- PLANK 4 -- SK_SEAT_HEAL -----------------------------------------------
SK_SEAT_HEAL = False      # ⛔ PLANK 4 -- BUILT, MEASURED, SHIPPED OFF AS A
                          # MEASURED ZERO.  REAL DOSE (48 heal events on our
                          # seats over 30 games, heals/game 0.8 -> 1.3) and the
                          # headline does not move: kills 14 = 14, by-r300
                          # 12 = 12, defeats 16 = 16, and all 12 named F1 cells
                          # unchanged.  ⚠ ITS OWN GUARD IS UNTESTED IN A LIVE
                          # TAPE: `seat_heal_refused` read 0 in every probed
                          # game, so the DOORWAVE pecker-count clause has never
                          # produced its other verdict on the engine.  It is
                          # driven both ways in the STATIC battery only.
                          # (original note) While one of OUR buildings on a delivery
                          # seat is losing HP, the keeper heals it: 1 Ti for +4
                          # against a peck's 2, i.e. ONE heal cancels TWO
                          # peckers.  This is DOORWAVE's healing race with the
                          # sides swapped -- at OUR core it is the enemy walking
                          # the long supply line, not us.
SK_SEAT_HEAL_MAX = 60     # per-GAME bound, in heals.  60 Ti is two harvesters;
                          # the plank has to stay cheaper than what it protects.
SK_SEAT_HEAL_TI_FLOOR = 12  # never heal the bank below this.  Same floor the
                          # core medic uses, for the same reason: the drip is
                          # never starved by a heal.
SK_SEAT_HEAL_PECK_MAX = 2 # ⛔⛔ THE DOORWAVE LESSON AS A CONSTANT, AND IT IS THE
                          # GUARD THAT KEEPS THIS PLANK FROM BEING THAT DEFEAT
                          # AGAIN.  +4 a round cancels exactly two 2-damage
                          # peckers.  With THREE enemy builders on the tile the
                          # race is arithmetically lost and every round spent is
                          # a round not spent on something that dies.  Heal only
                          # while the peckers are at or below this ...
SK_SEAT_HEAL_GUN_RACE = True  # ... OR while a live gun of ours covers the tile,
                          # because then the round's damage is 7 (or 18) on our
                          # side too and the race flips regardless of the count.
                          # ⛔ THE PERMISSIVE (rotatable-disc) COVER TEST, the
                          # same `_seat_covered` v610 used and for the same
                          # stated reason: being optimistic here is the direction
                          # that lets the exception FIRE, which is why it is
                          # behind its own flag.
SK_SEAT_HEAL_WALK = True  # the MOVEMENT half -- ONE step, never more.  "if
                          # adjacent or 1 step away" is the design's own wording
                          # and it is also the cost fence: a heal is worth a step,
                          # it is not worth a tour.

# --- THE RIDER -- PECK DEMOTION --------------------------------------------
SK_PECK_DEMOTE = False    # ⛔⛔ THE RIDER -- BUILT AND SHIPPED OFF AS A **NIL
                          # DOSE**, AND THAT IS THE LABEL, NOT A NULL RESULT.
                          # Its F1 tape is BYTE-IDENTICAL to the control in 30
                          # of 30 games and `peck_demoted` read 0 in every
                          # probed game.  The cause is structural, not a bug:
                          # `_belt_evict`'s peck path already requires the tile
                          # to be a `_route_gaps` one-gap tile, and no home
                          # turret of ours ever BEARS on such a tile.  A verb
                          # that cannot fire has not been tested; it has been
                          # skipped.  (original note) v610's cap tightened by the
                          # thing that replaces it.  A BUILDER peck at an enemy
                          # building on/near a delivery seat is REFUSED whenever
                          # one of our live turrets actually BEARS on that tile:
                          # the gun does 7 a round for 4 ammo and the keeper's
                          # turn is the scarce good the last three refutations
                          # all named.
                          # ⛔ THE STRICT BEARING TEST, NOT THE DISC.  `_gun_bears`
                          # asks `can_fire_from(turret pos, ITS ACTUAL FACING,
                          # its type, q)` -- refusing an action needs certainty,
                          # and the permissive disc form would refuse pecks on
                          # tiles no gun can currently reach at all.  That is the
                          # opposite polarity from `_seat_covered`, deliberately:
                          # an optimistic test is right when it ADMITS a plank and
                          # wrong when it VETOES one.


#      one of them answering a MEASURED row of the tapemj anatomy
#      (`scratchpad/s54_anatomy_mj/tapemj_anatomy.md`, 30 games vs the NOISE_OFF
#      Mjolnir baseline; 19 losses, 48 enemy core-shooters).
#
#      THE MEASURED PROBLEM, in one paragraph.  Their kill channel is 19/19
#      SENTINEL and it is POINT-BLANK: 28 of 48 shooters (58.3%) sit at d^2 <= 5
#      of our own core footprint, 36 of 48 survive to the end of their game, and
#      our own turrets are planted at d^2 <= 8 of THEIR core exactly 0 times in
#      30 games.  We delivered 1,053 HP into those 48 targets and killed 12 --
#      MISALLOCATED, not insufficient.  Their heals cancel our core damage in 14
#      of 19 losses (`healed == dealt` to the point); every one of the 7 wins
#      reads `dealt - healed` = 500-512, i.e. exactly one core.
# ===========================================================================

# --- PLANK 1 -- SK_APRON_DENY ---------------------------------------------
SK_APRON_DENY = True      # ⭐ PLANK 1, THE HIGHEST MEASURED LEVERAGE.  The d^2
                          # <= 5 apron around OUR core gets the seat-ownership
                          # treatment.  ⛔ AND THE VERB IS **RELAY**, NOT
                          # OCCUPANCY -- that distinction is the plank, and it is
                          # refuted-in-advance otherwise: on `helheim_B` our
                          # conveyor at (14,6) is destroyed at r56 and THEIR
                          # SENTINEL IS BUILT ON THAT SAME TILE AT r58.  A static
                          # seal is a two-round delay; a relay is a contest.
                          # BC's own T8 relay latency (1.08 rounds) is the spec.
SK_APRON_DSQ = 5          # the apron, in d^2 of our core FOOTPRINT.  5 and not
                          # 8 because the census is 28 of 48 at <= 5 against 29
                          # of 48 at <= 8: the ninth ring buys one shooter and
                          # 20 more tiles.
SK_APRON_RELAY_CAP = 2    # ⛔ THE BUDGET, AND IT IS THE v610 LESSON WRITTEN AS A
                          # CONSTANT: the keeper's turn is scarce and the belt
                          # duty has to survive the plank.  At most this many
                          # relays inside any SK_APRON_WINDOW rounds.
SK_APRON_WINDOW = 20      # the rolling window the cap is measured over.
SK_APRON_RELAY_TOTAL = 30 # per-GAME backstop, in relays.  v603's unbounded
                          # collar peck reached 2,179 actions; every bounded
                          # verb in this tree carries a game total as well as a
                          # rate, and this is that.
SK_APRON_BELT_PREF = False # ⛔ SUB-FLAG, BUILT, MEASURED, AND SHIPPED OFF --
                          # AND IT IS THE HALF THAT CARRIED THE WHOLE OF PLANK
                          # 1's EFFECT, IN BOTH DIRECTIONS.  With it ON, PLANK 1
                          # alone reads F1 by-r300 9 (control 11, gate FAILED),
                          # median kill 188.5 -> 267.5, and 8 of the 12 named F1
                          # cells MOVE -- a high-variance rewrite of the belt,
                          # not a targeted fix.  With it OFF the same plank
                          # reads F1 15 kills / by-r300 11 and moves ZERO named
                          # cells.  It also carried PLANK 1's only F2 gain
                          # (kills 9 vs 7), which is two games on a 30-game
                          # deterministic fixture and is NOT separable from
                          # noise at that n.  A tie-break inside a BFS is not
                          # supposed to be the largest behavioural lever in a
                          # wave; that it is, is the finding.
                          # (original note: SUB-FLAG: the belt PLAN prefers apron parents at
                          # equal BFS depth, so an occupied apron tile is a
                          # denied plant seat for free (the tile was going to
                          # carry a conveyor anyway).  Separately ablatable
                          # because it is the only half that touches the belt.

# --- PLANK 2 -- SK_TUBE_FLOOR ---------------------------------------------
SK_TUBE_FLOOR = False     # ⛔⛔ v614: ROAD CLOSED.  RE-TESTED AS THE PAIR THE
                          # v613 verdict commissioned (SK_TUBE_FLOOR x
                          # SK_AMMO_FLOOR in {10, 20, 30}, 30 games per cell,
                          # both fixtures) AND IT DOES NOT RECOVER AT ANY
                          # CUSHION.  F1 by-r300, gate 12:  ctrl 12 · tube@10
                          # 11 · floor20 alone 8 · tube@20 8 · tube@30 6 ·
                          # floor30 alone 6.  Not one arm reaches the gate, and
                          # the two treatment axes are MONOTONE DOWNWARD in the
                          # cushion.  ⛔ THE PAIR IS INTERNALLY CONTRADICTORY,
                          # and the funding-wait counter says so in one line:
                          # the S1->S2 wait this plank exists to shorten reads
                          # 995 rounds at the shipped cushion, 1,165-1,276 at
                          # 20 and 1,653-1,667 at 30.  A thicker cushion raises
                          # the very surcharge (10*(live+1) + SK_AMMO_FLOOR)
                          # that the waiver was written to duck, and raises the
                          # drip's per-round `need` besides -- so it takes the
                          # bank from the second gun with one hand while the
                          # waiver hands it back with the other.  There was no
                          # cushion at which both could hold.  DO NOT RE-OPEN
                          # THIS WITHOUT A NEW MECHANISM: the cushion axis is
                          # spent.  (v613's original note, which stands:)
                          # ⛔ PLANK 2 -- BUILT, MEASURED, AND SHIPPED OFF.  A
                          # REAL NEGATIVE ON BOTH FIXTURES, and the mechanism
                          # it targets DID move: the S1->S2 funding wait fell
                          # from 18/30 games (1,068 rounds) to 16/30 (976), and
                          # F2's tube2 share rose 0.321 -> 0.340.  The currency
                          # went the other way -- F1 by-r300 11 -> 10 and F2
                          # kills 7 -> 6 alone; on the full chassis REMOVING it
                          # recovered F1 8 -> 10 and F2 7 -> 9.  Read straight:
                          # the second tube arrives sooner and CHEAPER (no prep
                          # barriers, a thinner ammo cushion) and a thinner
                          # cushion is what the drip surcharge was defending.
                          # v603's arithmetic survives its own re-test.
                          # (kept ON below: ⭐ PLANK 2.)  THE SECOND TUBE IS A MEASURED WIN
                          # PRECONDITION ON BOTH FIXTURES: 6 of 7 wins vs
                          # Mjolnir reach two simultaneous forward turrets
                          # (median r56) and 8 of 19 losses never reach two at
                          # all; the home fixture's own SK_NEST_PAIR read Fisher
                          # p = 0.019.  `SK_NEST_PAIR` already WANTS two.  This
                          # plank removes the three things that stop it landing.
SK_TUBE_NOPREP = True     # (a) while below the floor, the prep barriers are
                          # SKIPPED: two builder turns and 6 Ti in front of a
                          # gun we do not have.  COPY 5's prep is priced for a
                          # gun that will stand for a while, not for the
                          # replacement of a tube whose absence is the loss.
SK_TUBE_FUND = True       # (b) while below the floor, the SECOND gun's ammo
                          # surcharge drops from 10*(live+1)+10 = 30 to
                          # SK_TUBE_FUND_AMMO.  ⛔ THE SURCHARGE IS v603's DRIP
                          # ARITHMETIC AND IT IS CORRECT IN GENERAL -- it is
                          # waived only inside the window where the pair does not
                          # yet stand, i.e. exactly where the anatomy says the
                          # game is decided.
SK_TUBE_FUND_AMMO = 10    # one sentinel shot of cushion, not three.
SK_TUBE_GAP_RELAX = True  # (c) while below the floor and the banded search
                          # returns NOTHING, retry with SK_NEST_PAIR_MIN_GAP
                          # relaxed to SK_TUBE_GAP_MIN.  On the small maps
                          # (holmgang 12x12, skald 16x16) the 8-d^2 spread can
                          # empty the band outright, and an unspread second tube
                          # beats no second tube -- 18 HP/round is the plank.
SK_TUBE_GAP_MIN = 2       # the relaxed spread: adjacent-but-not-stacked.

# --- v622 -- THE BAND-EXHAUSTION FALLBACKS (DIAG-siteless-decomposition) ---
SK_GAP_RELAX_SOLO = False # ⭐ v622 PLANK 1 -- UN-WELD THE GAP RELAX FROM THE
                          # FLOOR.  The v613 retry above is guarded by
                          # `SK_TUBE_FLOOR and SK_TUBE_GAP_RELAX`, and the
                          # shipped head carries SK_TUBE_FLOOR = False (the
                          # v614 road closure) -- so the relax has been DEAD
                          # CODE in every shipped configuration since v614,
                          # while paths_seatA (F1)
                          # spent 265 terminal rounds with up to 8 gap-blocked
                          # candidates recoverable every round.  ON: the retry
                          # arms on `taken` alone.  OFF is an exact identity
                          # (the original conjunction is unchanged).
SK_NEST_EXHAUST_PB = True # ⭐ v622 PLANK 2, SHIPPED ON -- LAST-RESORT POINT-
                          # BLANK ON A FULLY EXHAUSTED BAND.  Screen evidence
                          # (deterministic F1/F2, s55): F1 14->15/30 with all
                          # 28 quiet cells turn-identical (icefloe_seatB loss
                          # r698 -> WIN r437, EXHPB fired r284 = the exhaustion
                          # round); F2 8->8/30, 29 cells identical, one loss
                          # delayed r386->r485.  Fires only when the band scan
                          # returns nothing, so cells with a live band are
                          # untouched BY CONSTRUCTION AND BY MEASUREMENT.
                          # (Original rationale follows.)
                          # v622 PLANK 2 -- LAST-RESORT POINT-BLANK ON A
                          # FULLY EXHAUSTED BAND.  The v1 point-blank ban
                          # (SK_NEST_POINT_BLANK) priced close plants against
                          # in-band plants ("die 30% faster").  This retry runs
                          # ONLY when the band scan -- including the relax, if
                          # armed -- returned NOTHING, where the alternative it
                          # is priced against is ZERO tubes forever: icefloe_
                          # seatB paid 383 siteless rounds and the core at
                          # r698; paths_seatA 265 rounds and a r1000 tiebreak.
                          # OFF is an exact identity (new branch, new flag).

# --- PLANK 3 -- SK_PECK_FOCUS ---------------------------------------------
SK_PECK_FOCUS = True      # ⭐ PLANK 3, SHIPPED ON.  1,053 HP delivered into 48 shooter
                          # turrets, 450 healed back, 12 killed: the damage was
                          # SPREAD.  Peck CONCENTRATION -- every pecking body on
                          # the SAME tile -- plus a relaxed ledger-V7 veto once
                          # two of our bodies are on it.
SK_PECK_FOCUS_DSQ = 8     # the relax applies only to a shooter this close to
                          # OUR core.  A point-blank sentinel is worth committing
                          # to regardless of its heal trend; a far one is not.
SK_PECK_FOCUS_BODIES = 2  # ⛔ THE ARITHMETIC THE RELAX RESTS ON, AND IT IS
                          # MEASURED, NOT ASSUMED: two adjacent bodies are
                          # 4 dmg/round against one healer's +4.  The measured
                          # heal rate on their apron shooters is 450 HP over 48
                          # shooters' whole lifetimes (~0.16 HP/shooter-round, so
                          # well under one healer's continuous +4), which is why
                          # the bar is 2 and not 3.  If a re-measurement puts
                          # healers-per-apron-shooter at >= 1.5 continuous, this
                          # relax is wrong and the flag comes off.
SK_PECK_FOCUS_KEEPER = True  # the HOME KEEPER joins the march when the shooter
                          # is inside SK_PECK_FOCUS_DSQ.  Without this half only
                          # ONE body (the ORE DENIER) ever marches, so "two
                          # bodies adjacent" is unreachable and the relax can
                          # never fire -- the two halves are one plank.

# --- PLANK 4 -- SK_PLUCK_AWARE --------------------------------------------
SK_PLUCK_AWARE = True     # ⭐ PLANK 4, SHIPPED ON.  1,153 of our builder bots were thrown
                          # across 30 games and every one was an enemy kidnap
                          # (we build no launchers).  On `midgard_B` the SAME
                          # body is thrown off the SAME seat at r15, 21, 27, 33,
                          # 39, 45, 51, 57 -- every six rounds, from the only
                          # seat that reaches the sentinel.  Rank peck seats by
                          # distance from live enemy launchers.
SK_PLUCK_DSQ = 2          # ENGINE BOUND, not a choice: a launcher's pickup disc
                          # is d^2 <= 2 measured from the launcher.
SK_PLUCK_RETARGET = True  # ... and when EVERY orthogonal seat of the shooter is
                          # inside a live launcher's disc, march at the LAUNCHER
                          # instead.  It is a 30 HP BUILDING that cannot defend
                          # itself: 15 pecks, and its removal frees every seat it
                          # covers.  Their launcher positions are on the wire
                          # (`armed_memo` already keys LAUNCHER -- it is in
                          # ARMED_TYPES).
SK_PLUCK_MEMO_TTL = 60    # rounds a remembered enemy LAUNCHER tile still counts
                          # as live for the seat ranking.  A launcher is a
                          # building and cannot move, but it can die, and a
                          # permanently-feared ghost seat is a permanent detour.

# --- PLANK 5 -- SK_CORE_MEDIC_RIDER (gated on PLANK 2) ---------------------
SK_CORE_MEDIC_RIDER = False # ⛔ PLANK 5 -- BUILT, MEASURED, AND SHIPPED OFF AS
                          # AN EXACT NULL, demonstrated THREE independent ways:
                          # `p5only` reproduces the control on F2 column for
                          # column (30/30 cells, every instrument identical);
                          # `no5` reproduces the full chassis on F1 to the digit
                          # (11 kills / by-r300 8 / medkill 241); and
                          # `p1nb345` reproduces `p134nb` on BOTH fixtures.  The
                          # gate is the reason: it needs TWO TUBES STANDING and
                          # OUR CORE UNDER FIRE in the same round, and the tape
                          # says those two co-occur almost never.  The plank is
                          # correct and its precondition is empty.
                          # (original note: A RIDER, NOT A PLANK.  v608's
                          # medic is SHIPPED OFF (`SK_CORE_MEDIC = False`) and the
                          # anatomy says WHY it had to be: in 14 of 19 losses
                          # their core is at 500/500 when ours dies, so rounds
                          # bought for our core have NO CONSUMER.  With the tube
                          # floor standing they do.  This flag re-arms the medic
                          # verbs ONLY while (two tubes stand) AND (our core is
                          # under fire) -- read off SK_SLOT_NEST b21, which the
                          # engineer already publishes and which v607's
                          # `_s2_pending` already reads.
                          # ⛔ IT DOES NOT SET SK_CORE_MEDIC.  That flag stays
                          # False so the UNCONDITIONAL medic remains off and the
                          # two are separately ablatable.
                          # ⭐⭐ v617 RETRACTION OF THE v613 VERDICT ABOVE: THE
                          # "EXACT NULL / EMPTY PRECONDITION" READING IS
                          # WITHDRAWN AS A READER DEFECT.  The precondition was
                          # not empty; the READER was broken (`SK_TEAM_TUBES`
                          # below).  The three reproductions are all real and
                          # all consistent with a gate that never opened, which
                          # is what a nil-dose looks like.  v617 re-measures the
                          # rider against the FIXED reader; until that reads
                          # out, this flag is UNRESOLVED, not null.

# --- v617 ITEM 1 -- SK_TEAM_TUBES: THE PAIR BIT BECOMES A TEAM FACT --------
SK_TEAM_TUBES = True      # ⭐⭐ v617 -- A BUGFIX WITH AN ABLATION FLAG, DEFAULT
                          # ON.  `_two_tubes` (the gate under BOTH
                          # SK_HL_AFTER_S2 and SK_CORE_MEDIC_RIDER) read slot 7
                          # b21, which `_nest_publish` sets only when ONE BODY
                          # holds BOTH `nest_turret` AND `nest_turret2`.
                          # MEASURED (v616 probe, 6 games): the bit was set in
                          # 8.4% of core-rounds against a replay ground truth
                          # of 35.5% -- 5 of 51 publishes held a pair.  A
                          # PER-BODY LEDGER WEARING A TEAM FACT'S NAME.
                          # ⛔ TWO MECHANISMS, and the second is the bigger one:
                          #   (a) ENGINEER TURNOVER.  The role is claimed off a
                          #       beat; the successor body starts with an EMPTY
                          #       ledger and re-publishes a single-tube word
                          #       while two tubes stand.
                          #   (b) `get_hp(id)` RAISES FOR ANY ENTITY OUTSIDE THE
                          #       CALLER'S VISION and the error is
                          #       INDISTINGUISHABLE from a destroyed id (471 of
                          #       471 probes, `docs/research/BUILD-REPORT-
                          #       v516teardown-2026-08-18.md`).  `_nest_watch`
                          #       reads exactly that and calls the exception
                          #       DEAD -- so the moment the engineer walks off
                          #       tube 1 to plant tube 2, tube 1 is booked dead,
                          #       `nest_turret2` is promoted into `nest_turret`
                          #       and the pair bit CANNOT be set.  The band is
                          #       d^2 14-32 around THEIR core and a builder sees
                          #       r^2=20, so this is the normal case, not a rare
                          #       one.
                          # ⛔ THERE IS NO ID-BASED LIVENESS CHANNEL IN THIS
                          # ENGINE (same probe).  The substitute is the one that
                          # report named: A TURRET IS A UNIT, so `run()` is
                          # called for it every round it lives and stops the
                          # round it dies -- THE SENTINEL IS ITS OWN HEARTBEAT.
                          # v617 gives each FORWARD sentinel a seat (0 or 1) and
                          # a 10-bit absolute beat in slot 7, and `_two_tubes`
                          # becomes "both seats beat recently".
                          # ⛔⛔ HOW SLOT 7 GETS MORE THAN ONE WRITER WITHOUT
                          # BREAKING THE ONE-WRITER RULE -- AND THE FIRST
                          # ANSWER WAS WRONG, MEASURED.  The first cut said
                          # "every writer is read-modify-write on a disjoint bit
                          # field, so a collision costs staleness, not a value".
                          # THAT IS FALSE ON A BUFFERED STORE AND THE PRODUCER
                          # PROBE CAUGHT IT BEFORE ANY VERDICT: the RMW read
                          # returns LAST round's word, not the write pending
                          # this round, so two writers in one round both merge
                          # into the SAME stale snapshot and the loser's field
                          # is dropped EVERY round, not once.  Measured on
                          # helheim seat A: seat 0's beat FROZE at round 80 and
                          # never moved again while its tube stood to r371,
                          # because seat 1 wrote after it every single round.
                          # The fixed bit read 0.6% against ground truth 33.7%
                          # -- a producer that looked plausible and was inert.
                          # ⇒ THE WRITERS ARE PHASE-SEPARATED INSTEAD.  Writer w
                          # writes only on rounds with `rnd % SK_TUBE_PHASES ==
                          # w`: seat 0 phase 0, seat 1 phase 1, the ENGINEER
                          # phase 2.  NO TWO SLOT-7 WRITERS EVER SHARE A ROUND,
                          # so there is exactly one writer per round and the
                          # rule is met in its strongest form.  A seat is
                          # refreshed every 3 rounds, so a LIVE tube's beat is
                          # never older than the staleness bound -- exact, not
                          # a margin.  (⛔ THAT BOUND IS NOT NAMED-AND-VALUED IN
                          # THIS COMMENT ON PURPOSE: writing `FLAG = 3` in prose
                          # gives a text-anchored mutation control a second
                          # place to land, and it landed there -- the FIFTH time
                          # a comment has defeated a scan on this line.)
                          # The fields the sentinels take (b0-9, b22-31) were the
                          # site/dx/dy DIAGNOSTICS, which have ZERO consumers in
                          # this tree (grepped: written in `_nest_publish`, read
                          # nowhere).  `_s2_pending`'s reads (b10-20 born, b21)
                          # are UNTOUCHED, so that plank's behaviour is identical
                          # with the flag either way.
                          # ⛔ FALSE ⇒ v616 EXACTLY: no sentinel writes, the
                          # engineer publishes the old site/dx/dy word, and
                          # `_two_tubes` reads b21.  That is the identity
                          # control.
SK_TUBE_BEAT_MASK = 0x3FF # 10 bits.  ABSOLUTE round+1, not modular: MAX_TURNS
                          # is 1000 and 1000 < 1023, so the field holds every
                          # legal round and 0 still means "never" (manifest
                          # §5.3.5's rule, met with 10 bits instead of 11
                          # because the last round+1 is 1000, not 2000).
#     ⭐ v619 MOVED SK_TUBE_SEAT_FIELDS / SK_TUBE_PHASES / SK_TUBE_STALE.
#     They are no longer independent constants: the slot-7 layout, the writer
#     schedule and the staleness bound are all FUNCTIONS of how many tubes the
#     engineer keeps standing, and v619 makes that number a flag (SK_NEST_N3).
#     Three hand-set constants that must agree with a fourth is exactly the
#     shape the v617 first cut failed in, so they are DERIVED in one place --
#     see section 2.9 at the end of this file.  A seat still writes on every
#     PHASES-th round; the store is still buffered one round; STALE is still
#     PHASES exactly (lower reads a LIVE tube as dead, higher only delays
#     noticing a dead one, and a dead tube reads alive for <= STALE+2 rounds).
SK_TUBE_BAND_DSQ = 32     # a sentinel is a FORWARD TUBE iff it sits within this
                          # d^2 of the ENEMY core footprint.  ⛔ THIS IS THE
                          # GROUND TRUTH'S OWN DEFINITION, copied deliberately:
                          # `scratchpad/s54_v613/anat613.py` BAND_MAX = 32, the
                          # column the fix is verified against.  It equals
                          # SK_NEST_DSQ_MAX by construction (that is where
                          # `_pick_nest` puts them).

# ===========================================================================
# 2.  STORE ALLOCATION -- FRESH (design doc §7).  ONE WRITER PER SLOT.
#     Writes are buffered one round, so two writers in one round is a silent
#     lost update (manifest §5.3.3: it has bitten the benchmark twice, live).
#     Beats are ABSOLUTE round+1 in >= 11 bits (MAX_TURNS=1000 < 2047), never
#     modular, so 0 unambiguously means "never" (manifest §5.3.5).
# ---------------------------------------------------------------------------
#  slot  name                writer            contents
#   0    SK_SLOT_SEATS       each new builder  b0-7 seat counter (see note)
#   1    SK_SLOT_UNDER       CORE              b0-10 under-attack round+1
#   2    SK_SLOT_THREAT_POS  CORE              pack_pos of newest home threat
#   3    SK_SLOT_ENEMY_CORE  CORE              pack_pos, 0 = unset
#   4    SK_SLOT_HARV        HOME KEEPER       harvester ratchet (monotone)
#   5    SK_SLOT_BELT        HOME KEEPER       b0 conn · b1-11 rnd+1 · b12-17 n
#                                              · b18-23 belt tiles no live home
#                                                turret covers (design §2.8b)
#   6    SK_SLOT_CAGE        CAGE WALKER       b0-4 sealed · b5-15 advance rnd+1
#   7    SK_SLOT_NEST        SIEGE ENGINEER    b0-9 site+1 · b10-20 plant rnd+1
#                                              · b21 site2 set · b22-26 dx+15
#                                              · b27-31 dy+15   (v603 FIX 1)
#        ⭐ v617 SK_TEAM_TUBES=True RE-LAYS b0-9 and b22-31 (the site/dx/dy
#        DIAGNOSTICS, zero consumers) as TWO FORWARD-SENTINEL BEATS, seat 0 and
#        seat 1, each an absolute round+1 in 10 bits.  Writers become the SIEGE
#        ENGINEER (b10-20, b21) **and** each forward sentinel (its own seat
#        field) -- the one-writer rule is met in the form that actually matters,
#        ONE WRITER PER FIELD, with every write a read-modify-write.  See the
#        SK_TEAM_TUBES flag note for why a collision cannot lose a value.
#   8    SK_SLOT_DRIP        SIEGE ENGINEER    b0-5 fwd gunners · b6-11 fwd sents
#   9    SK_SLOT_STALL       SIEGE ENGINEER    b0-10 rnd+1 · b11-16 deaths ·
#                                              b17 branch · b18-23 mean life
#  10    SK_SLOT_BEAT_0      role-0 body       b0-10 alive beat round+1
#  11    SK_SLOT_BEAT_1      role-1 body       "
#  12    SK_SLOT_BEAT_2      role-2 body       "
#  13    SK_SLOT_BEAT_3      role-3 body       "
#  14    SK_SLOT_KILLER      HOME KEEPER       b0-9 pack_tile(inferred belt
#                                              killer) · b10-20 rnd+1 of that
#                                              inference · b21-26 escalated
#                                              harvester tiles   (v601 PLANK 1)
#  15    SK_SLOT_COREFIRE    CORE              v608: b0-10 round+1 our core last
#                                              LOST HP · b11-20 pack_tile of the
#                                              identified shooter (0 = unknown)
#                                              · b21-27 our core HP // 4 ·
#                                              b28 shooter is a SENTINEL
#
#  NOTE on slot 0: the seat counter has four writers over the match but never
#  two in one ROUND -- the core spawns at most one builder per round (a spawn
#  costs its action cooldown), so each claim is separated by >= 1 round and the
#  buffered-write hazard cannot arise.  That is the whole argument; if v1 ever
#  spawns two builders in one round this slot needs re-designing.
# ===========================================================================
SK_SLOT_SEATS = 0
SK_SLOT_UNDER = 1
SK_SLOT_THREAT_POS = 2
SK_SLOT_ENEMY_CORE = 3
SK_SLOT_HARV = 4
SK_SLOT_BELT = 5
SK_SLOT_CAGE = 6
SK_SLOT_NEST = 7
SK_SLOT_DRIP = 8
SK_SLOT_STALL = 9
SK_SLOT_BEAT = (10, 11, 12, 13)      # indexed by role id
SK_SLOT_KILLER = 14                  # v601 PLANK 1, writer: HOME KEEPER
SK_SLOT_COREFIRE = 15                # v608, writer: CORE.  THE LAST FREE SLOT.

SK_STORE_MASK = 0xFFFFFFFF   # write_store raises OverflowError outside 0..2**32-1
SK_BEAT_MASK = 0x7FF         # 11 bits: round+1 up to 2047 > MAX_TURNS
SK_BEAT_STALE = 3            # a live body beats every round and the store lags
                             # exactly one, so a live beat is never older than
                             # 1; 3 gives two rounds of slack for a lost turn.

# --- roles -----------------------------------------------------------------
SK_HOME_KEEPER = 0
SK_CAGE_WALKER = 1
SK_ORE_DENIER = 2
SK_SIEGE_ENGINEER = 3
SK_ROLE_NAMES = ("HOME_KEEPER", "CAGE_WALKER", "ORE_DENIER", "SIEGE_ENGINEER")
SK_N_ROLES = 4

# --- movement / navigation (doctrine.py:26, 1912-1916 -- verbatim) ---------
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
DELTA = {d: d.delta() for d in Direction}
CARD_DELTAS = tuple(DELTA[d] for d in CARDINALS)
DIR_DELTAS = tuple(DELTA[d] for d in DIRECTIONS)
CARD_OPPOSITE = (2, 3, 0, 1)
NAV_NODE_BUDGET = 4096

# Entity types the navigation flood treats as impassable (eco.py:59-63).
BFS_BLOCKING_TYPES = frozenset((
    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
    EntityType.HARVESTER, EntityType.BARRIER,
))
BELT_TYPES = frozenset((EntityType.CONVEYOR, EntityType.SPLITTER))
TURRET_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))
# v601 PLANK 3: the ARMED set for TARGET SELECTION.  Wider than TURRET_TYPES on
# purpose -- TURRET_TYPES is "what can shoot at us and what we count as OUR
# turrets" and must stay two-membered (the drip prices gunner/sentinel ammo off
# it); a LAUNCHER cannot shoot but the tape shows 37 of them planted forward at
# a median r9, and displacing our forward roles is a tempo tax worth answering.
ARMED_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL,
                         EntityType.LAUNCHER))

# --- budgets and thresholds ------------------------------------------------
# doctrine.py:1076.  ⚠ ct.get_cpu_time_elapsed() reads 0 under local
# `fcode run` even with --tle, so this guard is a NO-OP in every local screen
# (manifest §4.2 / design build rule 7): a local battery is un-CPU-tested and a
# platform `match test` is mandatory before any exposure.
CPU_BUDGET_US = 8000
SK_TELEPORT_DSQ = 4          # doctrine.py:1486, renamed.  A per-turn position
                             # jump of d^2 > 4 proves a launcher threw us.
SK_MAP_MIN_TILES = 8         # doctrine.py:5388, renamed.  Verified tiles below
                             # which known_map_for refuses to adopt at all.

# --- COPY 7, the drip ------------------------------------------------------
SK_AMMO_GUNNER = 4           # ammo per gunner shot (CLAUDE.md entity table)
SK_AMMO_SENTINEL = 10        # ammo per sentinel shot
SK_AMMO_FLOOR = 10           # V10's NAMED FLOOR: one sentinel shot of cushion,
                             # so a cost-scale shock or a burst of repairs
                             # cannot silently cancel next round's shot.
                             # ⛔⛔ v614: SWEPT AND HELD AT 10.  The v613 verdict
                             # named a thin cushion as the suspect behind PLANK
                             # 2's failure, so 20 (two sentinel shots) and 30
                             # were tested BOTH with the tube floor and ALONE --
                             # the floor-alone arms being the disentangling
                             # control, without which a pair gain could not be
                             # told from a cushion gain.  RESULT: THE CUSHION
                             # RAISE IS NEGATIVE ON ITS OWN.  F1 by-r300 12 ->
                             # 8 (floor 20) -> 6 (floor 30), monotone, and the
                             # second tube arrives LATER not sooner (tube2 share
                             # 0.382 -> 0.335 -> 0.298).  ⚠ ONE HONEST COUNTER-
                             # READING, BANKED RATHER THAN EXPLAINED AWAY: on F2
                             # (Mjolnir) the SAME raise reads kills 7 -> 10 at
                             # floor 20, with tube OFF as well as ON, i.e. the
                             # F2 gain belongs to the cushion and not to the
                             # pair.  It is 3 games on a 30-game deterministic
                             # fixture and it costs 4 by-r300 games on the
                             # verdict surface, so it does not ship -- but it is
                             # the only cell in this wave that moved our way and
                             # it is written down.


# --- COPY 5, the nest band -------------------------------------------------
# --- v626 -- COPY 5's ACTUAL clearance verb (T7/T8 on OUR plant tile) -------
SK_NEST_CLEAR = True         # ⭐ v626 PLANK A: the engineer evicts an ENEMY
                             # building standing ON its chosen band site instead
                             # of orbiting into a PERMANENT nest_bad ban (the
                             # second-largest kill clause in both DIAG-siteless
                             # band-exhaustion cells; _nest_scan never tests
                             # occupancy).  Reuses _clear_tile's guard doctrine:
                             # enemy-builder-adjacent refusal + hp-trend, and
                             # bans a RE-LAID tile on its second clear (the
                             # SK_COLLAR_GUNS re-run test).  OFF = exact identity.
SK_NEST_CLEAR_GIVEUP = 12    # rounds of chew per site before banning -- caps the
                             # spend at 24 Ti/site; NOT 20 (SK_CAGE_MELEE_GIVEUP):
                             # 15 turns exceeds the S1->S2 window (median r56).
SK_NEST_CLEAR_OWN = True     # ALLIED building on the site: destroy() -- free, no
                             # cooldown, same-turn build (engine-probed).
SK_NEST_PB_LIFE = False       # ⭐ v626 PLANK B: COPY 5's dependency in the only
                             # in-game-readable currency -- point-blank admitted
                             # only where the OPPONENT has demonstrably failed to
                             # clear our forward tubes (mean nest life >= R over
                             # >= N deaths).  EXPECTED INERT on every measured
                             # cell (our tubes live 9-14): a registered-null
                             # encoding; firing on a fixture is itself a finding.
SK_NEST_PB_LIFE_N = 2        # evidence floor (zero deaths reads mean_life 99)
SK_NEST_PB_LIFE_R = 26       # the band's own median life (PART-v47 §6.9)
SK_NEST_DSQ_MIN = 14         # inside sentinel reach (r^2=32), outside every
SK_NEST_DSQ_MAX = 32         # gunner's (r^2=13).  Diagonal-max d^2=32 preferred.
SK_NEST_POINT_BLANK = False  # ⛔ v1: point-blank (d^2<=13) plants are FORBIDDEN
                             # until ring clearance measures at parity
                             # (PLAYBOOK COPY 5's dependency).
SK_NEST_PREP_BARRIERS = 2    # barriers 1-4 rounds before the gun

# --- COPY 9, the cage ------------------------------------------------------
SK_CAGE_ACCEPT = 7           # accept 7 of 8; the eighth tile is not the plank.
                             # ⛔ v603 FIX 5: this is now the CEILING of a
                             # DYNAMIC bar (`SK_CAGE_CEIL`), not the bar itself --
                             # the reachable maximum is 8 minus the seats their
                             # own delivery belt must occupy, measured median 5.
                             # SK_CAGE_CEIL = False restores the fixed 7, which is
                             # the ablation identity and the v602 behaviour.
SK_CAGE_MELEE_GIVEUP = 20    # rounds of chewing one occupied ring tile

# --- V1 / V4 / V7 / V9 ledger constants ------------------------------------
SK_REBUILD_ESCALATE = 3      # V1: a tile rebuilt 3x without surviving becomes
                             # a locate-the-shooter task, never rebuild #4
SK_DEATH_MEMO_ROUNDS = 400   # V4: per-tile turret death memory lifetime
SK_HP_TREND_WINDOW = 8       # V7: rounds a target may fail to trend down
SK_STALL_ROUNDS = 60         # V9: seal not advanced in N rounds ...
SK_STALL_LIFETIME = 10       # ... AND forward turret lifetime below M
SK_PREEMPT_ORE_ROUND = 60    # COPY 1 pre-emptive half opens ~r60
SK_HOME_RING_DSQ = 13        # "our ring": what counts as planted on our door
SK_DOOR_GUN_CAP = 2          # ⛔ COPY 6b is an ANSWER, not a turret economy.
                             # Uncapped, the first local game bought six gunners
                             # (+20% cost scale each) and starved every other
                             # verb; two is one answer plus one replacement.

# --- v601 PLANK 1 constants (SK_HARV_ESCALATE) -----------------------------
SK_HARV_REBUILD_ESCALATE = 2 # ⛔ NOT 3.  The belt ledger's 3 is priced for a
                             # 3 Ti conveyor; a harvester is 20 Ti at scale 1.0
                             # and the tape's median harvester lived 9 rounds
                             # with 81.8% never delivering a stack, so rebuild
                             # #3 into a located killzone is 20 Ti bought at a
                             # measured 18.2% chance of ever paying anything.
SK_HARV_BAN_ROUNDS = 60      # how long an escalated ore tile stays off the
                             # build list.  Lifted EARLY if the inferred killer
                             # is confirmed dead.  On icefloe this turns 22
                             # rebuilds over 321 rounds into at most ~7.
SK_KILLER_GUNNER_REACH = 13  # gunner r^2 -- a straight-line shooter that could
SK_KILLER_SENT_REACH = 32    # sentinel r^2    have reached the dead tile.

# --- v601 PLANK 2 constants (SK_BELT_COVER) --------------------------------
SK_TRUNK_DSQ = 13            # "belt TRUNK" = a live belt/harvester tile beyond
                             # d^2 13 of OUR core.  85.7% (36/42) of the belt
                             # that died sat outside this radius, and 12 of our
                             # 18 turrets sat inside d^2 10.
SK_BELT_COVER_TRIGGER = True # ⛔ SUB-FLAG, DISCLOSED AS AN EXTENSION OF THE
                             # BRIEF.  The siting change alone can only act when
                             # `_door_action` already fires, i.e. when an enemy
                             # turret stands on our own ring -- and the tape
                             # bought a median of ONE turret per game, so the
                             # plank's own signature would have stayed at the
                             # 0/42 baseline for want of any turret to re-site.
                             # This sub-flag lets the HOME KEEPER buy a
                             # trunk-covering gunner when PLANK 1 has LOCATED a
                             # belt killer, WITHIN the unchanged
                             # SK_DOOR_GUN_CAP.  Turn it off to get the
                             # siting-only form the brief specifies.

# --- v601 PLANK 3 constants (SK_TARGET_PRIO) -------------------------------
SK_PRI_CORE = 6              # strict target ordering, both for OUR turret fire
SK_PRI_MARKED = 5            # and for BUILDER PECKS.  A BARRIER scores 0 and 0
SK_PRI_TURRET = 4            # is never a default target -- barriers are only
SK_PRI_HARVESTER = 3         # ever attacked by the verb whose PATH they block
SK_PRI_BODY = 2              # (cage-lap eviction, home-ring clearance), which
SK_PRI_OTHER = 1             # is where 1,280 of our 1,712 pecks went.
SK_PRI_BARRIER = 0

# --- v602 FIX 2 constants (SK_DANGER_NAV) ----------------------------------
SK_DANGER_GUNNER_REACH = 13  # gunner attack r^2 -- its ray, not a disc
SK_DANGER_SENT_REACH = 32    # sentinel attack r^2 (it ignores obstacles)
SK_DANGER_DETOUR_MAX = 6     # ⛔ THE VETO IS BOUNDED, AND IT HAS TO BE.  A pure
                             # "never enter a covered tile" rule can starve a
                             # verb: fimbulwinter's throat (rows 5-6, x 5-9) is
                             # walled north and south, so the ONE route east
                             # runs through the covered pair {(7,6),(6,5)} and a
                             # walker that always detours never reaches the ring
                             # at all.  After this many consecutive detour steps
                             # the body takes the direct step anyway -- 2 rounds
                             # in a gunner's ray costs one 7-damage shot at
                             # reload 2, against the 6 shots the v601 2-cycle
                             # absorbed on that same tile.
# --- v602 FIX 3 constants (SK_CYCLE_BREAK) ---------------------------------
SK_CYCLE_HIST = 4            # position ring: A-B-A-B needs exactly 4 entries
SK_CYCLE_ESCAPE_ROUNDS = 12  # a 2-cycle this old, with the perpendicular break
SK_CYCLE_ESCAPE_BLOCKED = 4  # ALSO blocked this many times, is a boxed-in body
SK_CYCLE_ESCAPE_CAP = 2      # ... and it may buy its way out at most twice.
                             # ⛔ THE CAP IS LEDGER V8: `destroy` is free and
                             # unlimited, which is exactly how the doctrine we
                             # replicate reached 893 builds on one tile.
# --- v602 FIX 5(b) constants (nest siting without a catalogue grid) --------
# --- v603 constants --------------------------------------------------------
#     ⭐ v619 MOVED SK_NEST_PAIR_N -- it is now derived from SK_NEST_N3 in
#     section 2.9, because the slot-7 layout and the writer schedule are
#     functions of it and a second hand-set copy could disagree with them.
#     v603's original note, kept because it is the claim v619 re-prices:
#     "TWO, and the number is the measured threshold, not a taste: 0 wins / 14
#     games with <= 1 sentinel built, 6 wins / 16 with >= 2.  ⛔ NOT THREE.
#     Every sentinel is +20% on the ONE global additive cost scale, and the
#     tape's own >=2 cell is a 2-4 band whose median is 2."
SK_NEST_PAIR_MIN_GAP = 8     # FIX 1: the second site must sit at least this d^2
                             # from the first.  Two sentinels on adjacent tiles
                             # share one answering gunner's ray and one prep
                             # barrier cluster; the band is 14-32 wide enough to
                             # spread them.
SK_TRUNK_TERM_WEIGHT = 6     # FIX 2: a TERMINUS seat (planned belt tile
                             # orthogonally adjacent to our core footprint) is
                             # worth this much in the ray scorer.  53 of 63 belt
                             # deaths sit at d^2 <= 4 of our core; the weight is
                             # what makes a covering facing beat a far-trunk one.
SK_TRUNK_SEAT_WEIGHT = 2     # FIX 2: the tile a PECKER must stand on -- an
                             # orthogonal neighbour of a terminus seat -- is the
                             # thing we actually want to kill (their builder dies
                             # to 2 gunner shots).  Lower than the seat itself so
                             # a facing that covers both wins.
SK_COLLAR_ROUTE_GATE = False # ⛔ FIX 4's ROUTE-BLOCKING HALF, SHIPPED OFF, AND
                             # THE REASON IS A MEASURED NEGATIVE, NOT A DOUBT.
                             # The brief's gate is "peck a collar barrier only
                             # where it currently blocks the delivery route",
                             # implemented as `_route_gaps` (the autopsy's
                             # one-barrier-from-home BFS).  On the 30-game tape
                             # it fires far too rarely and the cost is the belt:
                             # with the gate ON, collar pecks fall 2,158 -> 366
                             # and DELIVERED TITANIUM falls with them (auroraveil
                             # A 1,150 -> 420, bifrost A 2,470 -> 400), max_held
                             # median 2.5 -> 2.0 and kills 7 -> 6 with by-r300
                             # 4/30 -> 2/30.  ⭐ THE PECKS WERE BUYING DELIVERY:
                             # the terminus barrier is the tile between a
                             # harvester and the core, and clearing it is what
                             # makes `titanium_collected` non-zero.  The gate's
                             # own failure mode is visible in its inputs --
                             # `belt_built` is PER-UNIT state (design build rule
                             # 6), so a replacement keeper starts with an empty
                             # ledger and every chain reads as many-gapped, which
                             # is exactly when the gate refuses.
                             # ⇒ The BUDGET half below ships ON; this half stays
                             # in the tree, flagged and measurable, for a v604
                             # that fixes the gap estimator first.
SK_HOMEDEF_SKIP_BARRIER = True
                             # FIX 4's THIRD half, separated because the arms say
                             # it is the one that MOVES the collar number: with
                             # the whole of FIX 4 off, collar pecks are 1,773 over
                             # 30 games; with only the route gate off they are
                             # 351.  ⇒ almost the entire 2,158 -> ~400 reduction
                             # is `_home_defence` no longer melee-ing a BARRIER
                             # published on slot 2 as the home threat, NOT the
                             # belt branch.  The v602 residual #3 named the right
                             # site.
# --- v604 constants --------------------------------------------------------
SK_DANGER_K = 6              # FIX 1: extra STEPS charged for entering a tile a
                             # remembered enemy turret covers.  ⛔ THE UNITS ARE
                             # STEPS, WHICH IS WHAT MAKES THE NUMBER ARGUABLE
                             # RATHER THAN A TASTE: a covered tile is worth
                             # crossing iff the danger-free detour is LONGER than
                             # K.  A gunner at reload 1 lands ~1 shot of 7 while
                             # we cross one tile, a sentinel at reload 2 lands ~9
                             # every other round; a builder has 40 HP.  K = 6 is
                             # deliberately the same magnitude as v603's
                             # SK_DANGER_DETOUR_MAX so the two forms are
                             # comparable, and it is the one number this fix
                             # exposes to tuning.
SK_DANGER_MAXCOST = 250      # FIX 1: the weighted flood's distance array is a
                             # bytearray (255 = unreached).  A route costing more
                             # than this is not a route we want -- the flood
                             # abandons it and the caller falls back to the greedy
                             # step, exactly as the node budget already does.
SK_CYCLE_HIST_K = 12         # FIX 2 / v606 ITEM 4(b): the position ring under
                             # SK_CYCLE_K.  It must hold 2k to detect period k
                             # with TWO full repeats, which is the evidence bar --
                             # one repeat is a coincidence on a lap that
                             # legitimately revisits tiles.  12 = 2 x
                             # SK_CYCLE_K_MAX.  (A 20-entry ring for K_MAX 10 was
                             # built and measured; see the null recorded there.)
SK_CYCLE_K_MAX = 6           # FIX 2 / v606 ITEM 4(b).  ⛔ THE PARENTHESIS BELOW
                             # WAS THE ASSUMPTION IT SAID IT WAS NOT, AND IT IS
                             # NOW REFUTED.  It read: "the longer ones contain a
                             # period-<=6 sub-pattern often enough that the commit
                             # window still breaks them (reported, not assumed)".
                             # MEASURED on fimbulwinter seat B: bot 9 (ORE_DENIER,
                             # 167 rounds) and bot 4 (HOME_KEEPER, 138 rounds) are
                             # BOTH period 10, and `period_cycle()` returns 0 on
                             # 133/167 and 110/138 of those rounds -- there is no
                             # period-<=6 sub-pattern to catch.
                             # ⛔ AND WIDENING IT TO 10 (with the ring at 20) WAS
                             # MEASURED AND IS AN EXACT NULL, so it is NOT
                             # SHIPPED: `tape_cyclek6` vs `tape_SHIP3` read
                             # kills 11/11, by-r300 10/10, median kill 160/160,
                             # builder deaths 23/23, and every named cell
                             # identical.  The fimbulwinter orbits that DID
                             # shorten (seat B 305r -> 77r) shortened under
                             # SK_CYCLE_ALL_ROLES with K_MAX still 6, and the one
                             # that survives on seat A is period TWELVE -- outside
                             # 10 as well.  The class is real and the constant is
                             # not the lever; 6 stays until something measures.
SK_CYCLE_COMMIT_SLACK = 2    # FIX 2: the commit window is k + this, so the body
                             # holds one target for strictly longer than the cycle
                             # that was detected.
SK_CURSOR_GIVEUP = 20        # FIX 3: rounds a cage-walker cursor may hold one
                             # objective before it is abandoned and the tile
                             # banned for this body.  Matches
                             # SK_CAGE_MELEE_GIVEUP so a cursor cannot outlive the
                             # melee it is there to enable.
SK_BELT_EST_TTL = 120        # FIX 4: rounds after which a PRESENT observation of
                             # a planned belt tile is stale.  Generous on purpose
                             # -- the keeper's own lap around the trunk is the
                             # refresh mechanism and it is not fast.
SK_COLLAR_PECK_CAP = 15      # FIX 4: 30 HP barrier / 2 dmg per peck = 15.  A cap
                             # that FIRES is the healing race lost -- the tile is
                             # then banned and the belt re-routes, which is the
                             # autopsy's option (a) reached by ledger rather than
                             # by a second planner.
SK_CORE_PECK_HEALGUARD = True
                             # FIX 5's disclosed extension: the walker refuses to
                             # peck the enemy core while an enemy builder stands
                             # beside the footprint (the healing race).  Separate
                             # flag because it SUPPRESSES the only damage channel
                             # FIX 5 exists to re-open, so it has to be priced on
                             # its own rather than ride the ceiling change.
SK_CAGE_ACCEPT_MIN = 3       # FIX 5: the dynamic accept bar never drops below
                             # this.  If they hold six of eight seats the cage is
                             # not "complete", it is lost, and declaring victory
                             # on 2 sealed tiles would put the core back on the
                             # peck ladder for nothing.
SK_NEST_STUCK_ROUNDS = 25    # v606 ITEM 4(a1): 60 -> 25.  ⛔ THE GUARD WAS FIVE
                             # ROUNDS FROM FIRING AND THAT IS NOT A GUARD.
                             # MEASURED, paths seat A, bot 11: 63 turns (r47-109)
                             # in a period-8 nav orbit over four tiles at a FIXED
                             # site (16,12), `nest_best_d` pinned at 13, and the
                             # orbit self-broke at r110 -- 55 rounds into a
                             # 60-round clock.  Worse, the clock RE-ARMS from
                             # inside the orbit: `nest_best_d` resets to None when
                             # a nest turret dies and then re-arms on the ORBIT'S
                             # OWN minimum, restarting the count.  25 clears every
                             # legitimate walk on this tape (observed first-plant
                             # legs are r15/r28/r42/r47) and it is 25 rounds of NO
                             # IMPROVEMENT, not 25 rounds of walking.
                             # a nest site the engineer has not closed on in N
                             # rounds is unreachable; ban it and re-pick.  ⛔ The
                             # ban is what stops the re-pick oscillating: without
                             # it `_pick_nest` scores the same tile again next
                             # round, forever.
                             # ⭐ v607 ITEM 1 RE-SWEPT IT under the corrected
                             # re-arm; the value shipped is set from that sweep
                             # and the numbers are in the build report.
SK_NEST_STUCK_FIX = True     # v607 ITEM 1 -- THE RE-ARM, NOT THE CONSTANT.
                             # v606 named this defect and shipped a halved
                             # threshold instead of fixing it; the disclosed cost
                             # was helheim seat A flipping from a r189 WIN to a
                             # loss, and a NON-MONOTONE sweep (25/40/60 ->
                             # by-r300 10/9/10), which is the signature of a
                             # trigger that fires for the wrong reason.
                             # TWO CHANGES, both in `_nest_site_watch` and its
                             # one caller:
                             #  (a) the clock no longer restarts when a re-site
                             #      event re-picks THE SAME TILE (the "re-arms
                             #      from inside the orbit" half);
                             #  (b) the progress test is NET DISPLACEMENT from
                             #      an anchor tile, not per-round closest
                             #      approach -- a body that has travelled is
                             #      walking, a body that has not is orbiting
                             #      whatever its period.
                             # OFF restores the v606 verb byte-for-byte.
SK_NEST_STUCK_BOX = 2        # v607 ITEM 1(b): Chebyshev half-width of the box
                             # the body must stay inside for the stuck clock to
                             # keep running.  Leaving it re-anchors the clock.
                             # 2 is the measured span of the orbit class this
                             # guard is aimed at (see the build report's orbit
                             # geometry census); a straight walk leaves it in
                             # three steps.
SK_NEST_STUCK_FAR = 60       # v607 ITEM 1: THE BACKSTOP, and it is not optional.
                             # The guard was built for an UNREACHABLE site, and a
                             # body that wanders widely without ever closing has
                             # a LARGE net displacement -- the box test alone
                             # would never fire on it.  60 is the v606
                             # pre-change constant, kept so the swept value only
                             # ever moves the ORBIT trigger and never removes the
                             # original guarantee.

# ===========================================================================
# 2.9  v619 -- THE KILL SIDE.  Four planks, one flag each, cheapest first.
# ---------------------------------------------------------------------------
# WHY THIS WAVE AND NOT ANOTHER.  Both fixtures' anatomies say the same thing
# in the same arithmetic: we win iff `dealt - healed` on their core reaches one
# core (500-512 in 7 of 7 wins on tapemj, 0-54 in 14 of 19 losses), 100% of the
# damage that gets there is SENTINEL fire, and the strongest correlate of a win
# is HOW MANY TUBES STAND AT ONCE (Fisher p = 0.019 on F1; 6 of 7 wins reach two
# on F2).  v615/v616/v617/v618 closed FOUR independent defensive/economic axes
# in a row (launcher, tube-floor, cushion, the seat package) -- their builders
# are cheap and local, our purchases are global and singular.  The one purchase
# class that survives that closure is the TUBE ITSELF, because the tube IS the
# kill.  So every plank here buys tube-rounds and nothing else.
# ===========================================================================

# --- PLANK 1 -- SK_NEST_N3: the tube-count axis, N = 2 -> 3 ----------------
SK_NEST_N3 = False           # ⛔⛔ BUILT, DOSED, MEASURED AT POWER, SHIPPED OFF
                             # BY THE WAVE'S OWN PRE-STATED TIE-BREAK -- and the
                             # mechanism finding is worth more than the flag.
                             # LOCAL F1 (30 games) it PASSES: by-r300 12 -> 13,
                             # all 12 named cells kept plus holmgang_seatB at
                             # r267, band discipline intact (M4b/M4d point-blank
                             # 0/0 both seats, lattice 100.0).  F2 kills 7 -> 6.
                             # POWERED, head to head against SK_RENT alone over
                             # TWO independent 900-game grids that contained
                             # both arms: -1.44pp and -1.00pp, POOLED
                             # **-1.22pp game share [-4.36, +1.92]** at n=1800
                             # a side, by-r300 -0.06pp.  The CI includes zero,
                             # but the sign agrees across grids and the rule
                             # said "maximise powered share among passers", so
                             # the rule selects SK_RENT alone.
                             # ⭐⭐ WHY IT BOUGHT SO LITTLE, MEASURED ON THE
                             # ENGINE AND NOT INFERRED -- THIS IS THE FINDING:
                             # an instrumented copy logged every forward-tube
                             # purchase with the engineer's own `live` count.
                             # Over 30 F1 games, 69 purchases: **60 at live=0,
                             # 9 at live=1, ZERO at live=2.**  The engineer's
                             # ledger NEVER HOLDS TWO TUBES AT PLANT TIME, so a
                             # target of three is never the reason for a single
                             # build.  N=3's entire effect is that `live >= want`
                             # stops being reachable, i.e. it deletes the
                             # HOLD-STATION state -- it is a "never stop siting"
                             # flag wearing a tube-count flag's name, and the
                             # wire agrees: three tubes stand in 4.5% of rounds
                             # against 0.8%, on +2 sentinels over 30 games.
                             # ⛔ AND THE LEDGER IS WHY, WHICH TIES IT TO PLANK
                             # 3: with SK_RELIGHT_TRUEDEATH on, the same probe
                             # reads 38/26/1 -- live=1 purchases nearly triple
                             # -- because `get_hp` raising out of vision stops
                             # being read as a death.  A REAL third tube needs
                             # the corrected ledger AND a target the corrected
                             # ledger can chase; neither half pays alone, and
                             # that pair is the successor item.
                             # ⛔ WHAT IS KEPT: the whole mechanism, one flag
                             # from live.  The derived slot-7 re-lay, the third
                             # seat, the compaction in `_nest_watch` and S24''s
                             # writer-set arithmetic all ship, exercised by the
                             # N=2 branch and driven both ways by the battery.
                             # (original note kept below for the record)
                             # ⭐ THE COUNT IS THE CORRELATE, SO MOVE THE COUNT.
                             # v603 set SK_NEST_PAIR_N = 2 and its own comment
                             # said "NOT THREE ... every sentinel is +20% on the
                             # ONE global additive cost scale".  That objection
                             # was priced against a bot whose problem was paying
                             # for defence; it is re-priced here against the
                             # thing the ledger says decides the game.  THE
                             # ARITHMETIC: a standing tube is 18 dmg on reload 2
                             # = 9 HP/round.  Two clear their core's median heal
                             # tax; a third adds +9 HP/round SUSTAINED for as
                             # long as it stands, against +20% charged ONCE at
                             # purchase.  ceil(500/18) = 28 shots is one core;
                             # three tubes reach it in 19 rounds of joint uptime
                             # instead of 28.
                             # ⛔ WHAT IT COSTS AND WHERE: the +20% is on the ONE
                             # GLOBAL ADDITIVE factor, so it taxes every LATER
                             # purchase of every type -- the exact mechanism that
                             # sank v618's P1.  The difference is the consumer:
                             # v618 spent scale on barriers that bought no core
                             # damage; this spends it on the only entity that has
                             # ever produced core damage in this line.
                             # ⛔ FALSE ⇒ v618 EXACTLY (N = 2, two seats at
                             # b0-9/b22-31, the engineer owning slot-7 phase 2).
                             # The derived block below is the whole difference.

# --- PLANK 2 -- SK_S2_HASTE: the S2 arrival round --------------------------
SK_S2_HASTE = False          # ⛔⛔ BUILT, DOSED, MEASURED AND SHIPPED OFF -- AND
                             # THE PREMISE ITSELF IS FALSIFIED, WHICH IS WORTH
                             # MORE THAN THE FLAG.  F1, 30 games, against the
                             # control: kills 14 -> 7, by-r300 12 -> 6, our core
                             # dead 15 -> 19.
                             # ⭐ AND THE S2 CLOCK BARELY MOVED, which is the
                             # finding: MEDIAN S2 ARRIVAL 68.0 -> 69.0 rounds
                             # (`anat613`, the instrument of record for that
                             # column), with the UPPER QUARTILE tightening
                             # 117 -> 92.  ⛔ TWO CAVEATS, both stated because
                             # they cut against the plank's own story: the
                             # median is over the games that REACH two tubes
                             # (24 control, 23 haste), so an arm that loses its
                             # slowest game is flattered by censoring; and a
                             # SECOND instrument (`anat619`) reads 76 -> 69 on
                             # the same tapes purely because it takes the lower
                             # of the two middle values on an even sample.
                             # ⇒ THE HONEST READ: the tail moved, the median did
                             # not, and the outcome collapsed anyway.  The
                             # decomposition that put the whole gap on TRAVEL
                             # does not survive: the engineer is not mainly
                             # walking the band.
                             # ⛔ AND THE MECHANISM OF THE HARM IS ON THE WIRE:
                             # our builder bots THROWN went 207 -> 298 and the
                             # thrown-off-a-shooter-seat column went 0 -> 26.
                             # Siting the second tube next to the first puts the
                             # engineer inside their launcher's pickup disc and
                             # their collar, which is the one thing the four-axis
                             # closure says not to walk into.  THE BAND'S SPREAD
                             # IS NOT A GEOMETRY PREMIUM, IT IS DISPERSION UNDER
                             # A KIDNAPPER.  The split arm confirms it is the
                             # SCORING half, not the same-round half: haste with
                             # SK_S2_HASTE_SAME_ROUND off reads 7 kills /
                             # by-r300 6 / F2 5, i.e. identical harm.
                             # (original note kept below for the record)
                             # ⭐ THE MEASURED GAP: median S2 arrival r68 on F1
                             # against the donor's r63, and the engineer's own
                             # decomposition put ZERO of it on FUNDING.  What is
                             # left is TRAVEL + PREP.  v617's launcher funnel
                             # named ADJACENCY as that axis's blocker; the tube
                             # analogue is that `_nest_scan`'s score is
                             # `(d == BAND_MAX and diagonal, d, -dist to us)` --
                             # PROXIMITY IS THE LAST KEY, so after S1 plants the
                             # engineer routinely walks the whole band to a
                             # far diagonal tile for a geometry premium worth
                             # less than the rounds it costs.
                             # TWO CHANGES, both inside the follow-up pick only:
                             #   (a) the site is chosen the SAME ROUND S1 is
                             #       planted, from beside S1, instead of a round
                             #       later -- "chosen before leaving S1's
                             #       neighbourhood", literally;
                             #   (b) the follow-up score leads with PROXIMITY,
                             #       with the old keys as tie-breaks.  The band
                             #       (d^2 14-32) and the pair gap are UNCHANGED,
                             #       so band-only discipline and the point-blank
                             #       ban are untouched -- this reorders inside
                             #       the legal set, it does not widen it.
                             # ⛔ FIRST TUBE UNCHANGED: with no tube standing
                             # there is nothing to be near, so S1's pick is
                             # byte-identical and the flag off is an exact
                             # identity everywhere.
SK_S2_HASTE_SAME_ROUND = False  # ⛔ OFF WITH ITS MASTER: a rider left on
                             # under a refuted master is a config that
                             # misrepresents itself, and S26(f) refuses it.
                             # (a).  Split from the master so the two halves
                             # can be ablated apart -- (a) is worth at most one
                             # round per tube and (b) is worth the walk, and a
                             # single flag could not tell us which paid.

# --- PLANK 3 -- SK_TUBE_RELIGHT: replant latency (LEDGER V3's budget) ------
SK_TUBE_RELIGHT = False      # ⛔⛔ BUILT, DOSED, MEASURED, SHIPPED OFF -- AND IT
                             # IS THE MOST INSTRUCTIVE RESULT OF THE WAVE,
                             # BECAUSE THE BUG IT FIXES WAS LOAD-BEARING.
                             # F1, 30 games: kills 14 -> 15 and our core dead
                             # 15 -> 13 (both better), but by-r300 12 -> 10 and
                             # the median kill round 201 -> 265.  Under
                             # DEFENCE_ADMISSION_BAR that is off-programme: it
                             # buys survival and total damage at the kill's
                             # expense.  The sub-split says (a) IS the whole
                             # effect -- TRUEDEATH alone reads 14 / by-r300 10 /
                             # medkill 265, and adding (b)+(c) changes nothing.
                             # ⭐⭐ WHY, off the wire, and it inverts the
                             # premise: dealt 26,800 -> 32,420 and healed
                             # 18,184 -> 24,036, i.e. NET IS FLAT (8,616 ->
                             # 8,384) while the game gets longer -- and
                             # SIMULTANEOUS TWO-TUBE SHARE FALLS 0.382 -> 0.296.
                             # v618's defect (booking an out-of-vision tube dead)
                             # was ACCIDENTALLY THE ENGINE OF THE TUBE COUNT: a
                             # ledger that keeps forgetting its tubes keeps
                             # planting new ones, and the anatomy's own
                             # correlate is SIMULTANEOUS TUBES, not correct
                             # bookkeeping.  Fixing the ledger without raising
                             # the target is a pure loss.  ⇒ THE FIX IS NOT
                             # WRONG, ITS PARTNER IS MISSING: it belongs with a
                             # target the corrected ledger can still chase (a
                             # standing-tube FLOOR, not a plant COUNT), which is
                             # the successor item this plank hands up rather
                             # than a flag to flip.
                             # (original note kept below for the record)
                             # ⭐ V3 SAYS A DEAD TUBE IS AN IMMEDIATE RE-SITE
                             # DECISION.  It is coded that way and it still
                             # loses rounds, in three places this plank names:
                             #  (a) ⛔ THE DEATH TEST IS THE v617 ENGINE FACT,
                             #      UNFIXED ON THE WRITER SIDE.  `_nest_watch`
                             #      books a tube DEAD when `get_hp(tid)` raises
                             #      -- and that exception is INDISTINGUISHABLE
                             #      from "outside this body's vision" (471 of
                             #      471 probes).  The engineer walks to the
                             #      SECOND site and a builder sees r^2 = 20, so
                             #      a live tube is booked dead as a matter of
                             #      routine: the V4 death memo bans its tile,
                             #      `nest_lives` feeds `_stall_check` a short
                             #      lifetime, and the ledger `live` count is
                             #      wrong in the direction that spends turns.
                             #      v617 fixed the READER (`_two_tubes` reads
                             #      the seats' own beats); this fixes the
                             #      ENGINEER'S LEDGER with the same instrument:
                             #      an exception is a death only when the TEAM
                             #      BEAT COUNT has actually fallen below what
                             #      the ledger holds.  Otherwise it is silence,
                             #      and silence is not evidence.
                             #  (b) PREP REUSE.  A re-site resets
                             #      `nest_prepped` to 0 and the engineer spends
                             #      SK_NEST_PREP_BARRIERS whole turns rebuilding
                             #      cover that, on a relight, usually still
                             #      stands.  Standing allied barriers within
                             #      d^2 <= 4 of the new site are COUNTED, so a
                             #      relight is 30 Ti plus a walk.
                             #  (c) NO DISCRETIONARY DETOUR WHILE DOWN.  With
                             #      the count below target and a death on the
                             #      books, the engineer does not spend the turn
                             #      pecking the enemy core when siting fails --
                             #      it closes on the band so the next pick
                             #      succeeds from nearer.
                             # ⛔ FALSE ⇒ v618: exception means dead, prep
                             # always rebuilt, `_attack_enemy_core` unchanged.
SK_RELIGHT_TRUEDEATH = False # (a) alone.  ⭐⭐ THIS SUB-FLAG EXISTS BECAUSE THE
                             # PROBE SAID SO, NOT FOR TIDINESS.  `probe_p1` (6
                             # games, F1) instruments the engineer at
                             # `live >= 2` and printed NOTHING -- zero lines in
                             # six games -- while the WIRE says two of our
                             # forward sentinels stand simultaneously in 38.2%
                             # of rounds.  THE ENGINEER'S OWN LEDGER NEVER
                             # HOLDS A PAIR, because (a) books every
                             # out-of-vision tube dead.  ⇒ PLANK 1 (N = 3) IS
                             # UNREACHABLE WITHOUT (a): a third tube cannot be
                             # wanted by a ledger that never reaches two.  The
                             # two planks are not independent and this flag is
                             # how that is measured rather than asserted.
SK_RELIGHT_PREP = False      # (b) alone: the prep-barrier credit.
SK_RELIGHT_CLOSE = False     # (c) alone: no discretionary detour while down.
SK_RELIGHT_PREP_DSQ = 4      # (b): a standing allied barrier within this d^2 of
                             # the site counts as one prep.  4 = the same disc
                             # `_prep_barrier` builds into, copied so the credit
                             # cannot count cover the builder would not have
                             # built.

# --- PLANK 5 -- SK_RENT: rent, do not own (Magnus, mid-wave) ---------------
SK_RENT = True               # ⭐ SCALE IS A RENT, NOT A PURCHASE -- ENGINE-
                             # PROBED THIS WAVE (`scratchpad/s54_v619/
                             # probe_destroy`, helheim r3-r4, both seats):
                             #   * `destroy` on an adjacent ALLIED building does
                             #     NOT touch the action cooldown (0 before, 0
                             #     after TWO destroys in one round) and is
                             #     unlimited per turn;
                             #   * the same body could still BUILD that turn
                             #     (the build then set cooldown = 1 -- the
                             #     counter-case that makes the 0s meaningful);
                             #   * `get_scale_percent()` fell 183 -> 182 -> 181
                             #     on two barrier destroys and rose 181 -> 182
                             #     on the rebuild.  THE +1% CONTRIBUTION IS
                             #     REFUNDED IN FULL.
                             # ⇒ a building we no longer use is charging us its
                             # scale contribution on EVERY later purchase, and
                             # handing it back is free in turns.  A tube costs
                             # 30 x scale; sweeping ten orphaned conveyors before
                             # the S3 purchase is 10% of base off that tube and
                             # off everything after it.
                             # ⛔ THE DEFINITION OF "SPENT" IS THE WHOLE PLANK
                             # AND IT IS DELIBERATELY NARROW.  Exactly two
                             # classes qualify:
                             #   (a) a BELT conveyor/splitter on a tile that is
                             #       NOT in the current `belt_plan` -- an orphan
                             #       left by a TERMINATE reroute;
                             #   (b) a BARRIER within d^2 <= 4 of an ABANDONED
                             #       nest site (in `nest_bad` or in the V4 death
                             #       memo) and NOT within that radius of the LIVE
                             #       site.
                             # Everything else is refused, by type and by
                             # arbiter: never a harvester, never a turret, never
                             # the core, never a tile `tile_owner` gives to
                             # another verb (so cage/door/deny barriers -- the
                             # load-bearing strangle -- are structurally out of
                             # reach, not merely unlisted), and never anything
                             # within SK_RENT_COVER_DSQ of a live enemy turret,
                             # where a barrier is cover rather than debt.
                             # ⛔ FALSE ⇒ v618: no sweep, no refund.
SK_RENT_COVER_DSQ = 8        # never sweep a building this close to a LIVE enemy
                             # turret -- at d^2 <= 8 a barrier is soaking shots
                             # that would otherwise land on a body or a tube, and
                             # its 1% is the cheapest cover in the game.
SK_RENT_MIN_ROUND = 20       # no sweeping before this round.  The early belt is
                             # laid and re-laid while the plan is still settling
                             # (`_belt_watch` revises it), and an orphan at r6 is
                             # usually a plan that has not converged rather than
                             # debt.
SK_RENT_ORPHAN_AGE = 25      # a belt tile must have been off-plan for this many
                             # rounds before it counts as an orphan.  ⛔ THIS IS
                             # THE GUARD AGAINST THE THRASH LEDGER V8 NAMES: the
                             # plan re-routes, we demolish, it re-routes back and
                             # we rebuild at 3 Ti and +1% a lap.  Off-plan must
                             # be a STATE, not an instant.
SK_RENT_PRE_BUY = True       # the ordering bonus: while the engineer is short of
                             # its tube target and inside one purchase of
                             # affording the next one, the sweep runs FIRST --
                             # the refund lands on the round the tube is bought,
                             # which is the only round it is worth anything.
SK_RENT_MAX_PER_TURN = 2     # destroys per body per turn.  The engine allows
                             # unlimited (probed above); this is a CPU and
                             # blast-radius bound, not an engine one.

# --- PLANK 4 (MEASURE-ONLY) -- the dealt-healed ledger ---------------------
# No flag: it is an off-tree instrument (`scratchpad/s54_v619/ledger.py`) that
# reads the wire.  A measure-only plank that needed a flag in the shipped tree
# would be a behaviour change wearing an instrument's name.

# ===========================================================================
# v620 -- THE TWO SUCCESSOR ITEMS v619's DEEP FINDING NAMED
# ===========================================================================

# --- v620 PLANK 1 -- SK_TUBE_FLOOR2: the STANDING-tube floor ---------------
SK_TUBE_FLOOR2 = False       # ⭐⭐ THE PARTNER v619's PLANK 3 ASKED FOR, AND THE
                             # ONLY REASON IT IS A SEPARATE FLAG FROM
                             # SK_TUBE_RELIGHT IS THAT THE PAIR HAS TO BE
                             # ABLATABLE APART.  v619 measured, instrumented:
                             # the engineer's OWN plant ledger held live = 0 on
                             # 60 of 69 tube purchases and live = 2 on ZERO of
                             # them, while the WIRE says two forward sentinels
                             # stand simultaneously in 38.2% of rounds.  The
                             # ledger has never been the thing that decided a
                             # purchase; the DEFECT was (`get_hp` out of vision
                             # raises == dead), and repairing that defect ALONE
                             # (SK_RELIGHT_TRUEDEATH) cut two-tube share
                             # 0.382 -> 0.296 and F1 by-r300 12 -> 10, because
                             # the misread was ACCIDENTALLY SUSTAINING TUBE
                             # PRESSURE through a replant loop.
                             # ⇒ THE HONEST SIGNAL IS ONLY SHIPPABLE WITH A
                             # TARGET IT CAN CHASE.  This flag makes the
                             # engineer's want/have comparison a TEAM fact read
                             # off v617's phase-separated slot-7 beats (the
                             # producer measured within 2pp of replay ground
                             # truth) instead of its own plant ledger:
                             #   * team-live < SK_TUBE_FLOOR2_N  ->  planting
                             #     the deficit tube is the engineer's TOP
                             #     action (band rules unchanged, prep reused
                             #     when intact if SK_RELIGHT_PREP is on);
                             #   * team-live >= SK_TUBE_FLOOR2_N  ->  NO further
                             #     tube purchase.  This is the half that closes
                             #     the accidental replant loop, and it is the
                             #     half that costs money if the beats undercount.
                             # ⛔ FALSE ⇒ v619: `live = self._nest_live()`, the
                             # plant ledger, character for character.
SK_TUBE_FLOOR2_N = 2         # the floor.  TWO, and it is not a free parameter:
                             # 100% of the 14,130 damage dealt to their core
                             # across 30 games was sentinel fire, 0 wins in 14
                             # games with <= 1 forward sentinel vs 6 wins in 16
                             # with >= 2 (Fisher p = 0.019), and v619's N = 3
                             # arm was measured and REFUTED at power.  The floor
                             # restates the number the line already ships
                             # (SK_NEST_PAIR_N); it changes WHERE THE COUNT
                             # COMES FROM, not what it is.
SK_TUBE_FLOOR2_GRACE = 6     # ⛔⛔ THE BIRTH GRACE, AND IT IS A CORRECTNESS
                             # REQUIREMENT, NOT A TUNING KNOB.  A tube planted
                             # at round r does not run until r+1, writes its
                             # seat only on its own phase residue
                             # (rnd % SK_TUBE_PHASES == seat, so up to
                             # SK_TUBE_PHASES-1 = 2 more rounds) and slot writes
                             # are BUFFERED one round -- so a freshly planted,
                             # perfectly healthy tube is INVISIBLE to the team
                             # count for up to 1 + 2 + 1 = 4 rounds.  Without a
                             # grace the floor reads the deficit it just filled
                             # and buys a SECOND replacement: the exact loop
                             # this plank exists to close, reintroduced from the
                             # other side.  6 = 4 + 2 rounds of margin.
                             # ⛔ HOW IT IS APPLIED MATTERS AS MUCH AS ITS
                             # VALUE.  Inside the grace the engineer falls back
                             # to `max(team, own ledger)`, i.e. it may only
                             # OVER-count; outside it, the team beats rule
                             # alone.  Over-counting delays a replant by at most
                             # GRACE rounds; under-counting buys a tube we
                             # already have.  This plank is about the second
                             # failure, so the grace fails toward the first.
SK_TUBE_LATENCY_SOLO = True # ⭐ v627/v628 -- un-weld the latency half from the
                             # closed floor road (fifth weld instance; see the
                             # v627 tree for the full record).  Admits STAGE/
                             # PREPREP alone in the live>=want hold state; no
                             # floor semantics.
SK_TUBE_FLOOR2_PREPREP = False   # THE OTHER HALF OF "no further purchases":
                             # at or above the floor the engineer does not idle
                             # beside the newest tube (v619's `hold`), it picks
                             # the NEXT band site and lays its prep barriers
                             # WITHOUT planting the gun.  When a tube does die,
                             # the replacement is a walk and 30 Ti instead of a
                             # walk, two builder turns and 30 Ti.
                             # ⛔ SPLIT FROM ITS MASTER because it is the only
                             # part of PLANK 1 that SPENDS anything (2 barriers
                             # = 6 Ti and +2% of scale, paid speculatively), and
                             # a plank whose spending half is welded to its
                             # saving half cannot be priced.
SK_TUBE_FLOOR2_STAGE = True # ⭐⭐ THE PROBE'S OWN SUCCESSOR, BUILT INSIDE THE
                             # WAVE BECAUSE THE REFUSAL PARTITION NAMED IT.
                             # Instrumented over 30 F1 games, the CONTROL's
                             # engineer-rounds under SK_NEST partition as:
                             # HOLD 1,126 · NOSITE 648 · NOFUND 150 · BOUGHT 67.
                             # It is SITE-limited (9.7 siting refusals per
                             # purchase), not target-limited and not
                             # funding-limited -- so a FLOOR, which can only
                             # ever REFUSE a purchase, has no opposite side to
                             # pay for what it costs.  And the pair arm shows
                             # where the cost lands: HOLD rises to 2,724, of
                             # which 1,538 are rounds the LEDGER thought were
                             # below target (195 at led=0, 1,343 at led=1) --
                             # rounds v619's engineer spent WALKING TOWARD THE
                             # NEXT BAND SITE and v620's spends standing beside
                             # a tube that is already fine.
                             # ⇒ THE BROKEN LEDGER WAS NOT BUYING TUBES, IT WAS
                             # BUYING PRE-POSITIONING, and it got it for free.
                             # This flag buys the same thing deliberately: at or
                             # above the floor the engineer picks the NEXT band
                             # site and WALKS to it -- and builds nothing.  No
                             # barrier, no gun, no Ti, no scale.  It is
                             # SK_TUBE_FLOOR2_PREPREP with the spending removed,
                             # which matters because pre-prep measured WORSE
                             # than plain holding on the plank's own down-clock
                             # (downR 1,236 vs 926).
SK_TUBE_FLOOR2_PREPREP_MAX = 1   # how many NEXT sites may be pre-prepped at
                             # once.  ONE: the speculative spend is bounded by
                             # construction, and a second pre-prep would be
                             # cover for a hole two tubes deep, which is a state
                             # the floor is supposed to make unreachable.

# --- v620 PLANK 2 -- SK_RENT_EARLY: the refund must land BEFORE the buy ----
SK_RENT_EARLY = False        # ⭐ v619's ITEM 2, AND IT IS A TIMING PLANK WITH
                             # NO NEW VERB.  SK_RENT ships and works -- the
                             # engine probe confirmed the economics point for
                             # point (destroy touches no cooldown, is unlimited
                             # per turn, and refunds the scale contribution in
                             # full, 183 -> 182 -> 181) -- but v619 measured the
                             # SWEEP MEDIAN at r119 against S2 at r76, and
                             # `scaleS2` did not move.  A refund that lands
                             # after the purchase it was meant to cheapen has
                             # priced nothing.  Three sub-flags, each a distinct
                             # reason the sweep is late:
                             #   (a) SK_RENT_EARLY_RESITE -- ORDERING.  The
                             #       sweep runs at the TOP of the turn, before
                             #       `_nest_watch` books the death that puts the
                             #       dead site into `nest_deaths`.  So on the
                             #       one round the engineer is still STANDING at
                             #       the abandoned site, its preps are not yet
                             #       classifiable as spent -- and by the next
                             #       round it has walked.  The fix is a second,
                             #       TARGETED sweep at re-site time.
                             #   (b) SK_RENT_EARLY_AGE -- THE ORPHAN CLOCK.
                             #       The general clock (25 rounds) is right in
                             #       general -- off-plan must be a STATE, not an
                             #       instant -- and it is what pushes the first
                             #       belt sweep past S2.  Relaxed to
                             #       SK_RENT_EARLY_AGE_N inside, and ONLY
                             #       inside, the pre-floor window.
                             #   (c) SK_RENT_EARLY_STEP -- the 1-STEP DETOUR.
                             # ⛔ FALSE ⇒ v619: sweep timing unchanged.
SK_RENT_EARLY_RESITE = False # (a) alone.  A targeted sweep of the ABANDONED
                             # site's own prep disc, taken in the same round the
                             # re-site decision is made, while the body is still
                             # adjacent to it.  Same `_rent_class` arbiter, same
                             # refusals, same per-turn cap -- only the position
                             # scanned and the round it is scanned on are new.
SK_RENT_EARLY_AGE = False    # (b) alone.
SK_RENT_EARLY_AGE_N = 8      # (b): the relaxed clock, in rounds.  8, not 0:
                             # `_belt_watch` revises the plan and LEDGER V8's
                             # thrash (re-route, demolish, re-route back,
                             # rebuild at 3 Ti and +1% a lap) is a real cost.  8
                             # is long enough that a single revision cycle
                             # cannot open the window and short enough that an
                             # orphan created at r30 is swept before an S2 at
                             # r76.
SK_RENT_EARLY_WINDOW = True  # (b)'s SCOPE, and it is the guard that keeps the
                             # relaxed clock from becoming a global loosening:
                             # the relax applies only while the team tube count
                             # is BELOW the floor, i.e. exactly where a refund
                             # is about to be read by a sentinel purchase.  With
                             # this False the relax is unconditional -- kept as
                             # the WIDENED-DEFINITION MUTANT that must degrade,
                             # never as a shipping option.
SK_RENT_EARLY_STEP = False   # (c) alone.  ⛔⛔ THE ONLY PART OF THIS PLANK THAT
                             # SPENDS A TURN, AND THE FOUR-AXIS CLOSURE IS WHY
                             # IT IS BOUNDED THREE WAYS RATHER THAN ONE.  A
                             # sweep candidate on a DIAGONAL (d^2 <= 2) is one
                             # cardinal step from being destroyable; the body
                             # takes that step, loses its move for the turn, and
                             # sweeps next round.  It is NEVER a walk target:
                             #   * diagonal only -- one step, or nothing;
                             #   * SK_RENT_STEP_BUDGET detours per BODY per
                             #     GAME, hard-capped;
                             #   * only inside the pre-floor window, where the
                             #     refund has a buyer.
                             # If it still loses, it loses as a bounded
                             # experiment and the other two sub-flags are
                             # unaffected.
SK_RENT_STEP_BUDGET = 4      # (c): detour steps per body per game.  FOUR.  At
                             # 1% a barrier and 1% a belt tile this buys at most
                             # 4% of scale off the next purchase; a fifth would
                             # be worth ~0.3 Ti on a 30 Ti sentinel and cost a
                             # whole builder move.

# --- DERIVED: the slot-7 layout, which is a FUNCTION of the tube count -----
# ⛔⛔ WHY THIS IS DERIVED AND NOT THREE MORE HAND-SET CONSTANTS.  Slot 7 is 32
# bits and v617's layout spends all of them: b0-9 seat 0, b10-20 the engineer's
# plant round, b21 its pair bit, b22-31 seat 1.  A THIRD 10-bit seat does not
# fit beside them -- 3 x 10 + 11 + 1 = 42 > 32 -- so the third tube is not a
# constant change, it is a RE-LAY, and the re-lay has to come with the writer
# schedule or the measured 291-round freeze comes straight back.
#   N = 3:  b0-9 seat 0 · b10-19 seat 1 · b20-29 seat 2 · b30-31 unused.
#           THE ENGINEER STOPS WRITING SLOT 7 ALTOGETHER, so there are exactly
#           THREE writers and SK_TUBE_PHASES stays 3 -- one residue each, one
#           writer per round, the rule met in its strongest form.
#           WHAT THAT COSTS: b10-20 (the plant round) and b21 (the pair bit)
#           stop being published.  Their ONLY reader is `_s2_pending`, which
#           returns False on its first line unless SK_S2_PRIORITY -- and that
#           flag is False in the shipped config and in every arm of this wave
#           (v607 measured it a clear negative).  The static battery asserts
#           that dependency rather than trusting this sentence.
#   N = 2:  v618's layout, unchanged, engineer on phase 2.
# ⛔ SK_TUBE_STALE STAYS DERIVED: a seat writes every SK_TUBE_PHASES rounds and
# the store is buffered one round, so a live beat is at most PHASES rounds old.
# PHASES is 3 either way, so STALE is 3 either way and the S24(f) inequality
# (STALE >= PHASES) is met with no margin, exactly as v617 argued it.
if SK_NEST_N3:
    SK_NEST_PAIR_N = 3
    SK_TUBE_SEAT_FIELDS = (0, 10, 20)
    SK_TUBE_ENG_SLOT7 = False
else:
    SK_NEST_PAIR_N = 2
    SK_TUBE_SEAT_FIELDS = (0, 22)
    SK_TUBE_ENG_SLOT7 = True
SK_TUBE_PHASES = len(SK_TUBE_SEAT_FIELDS) + (1 if SK_TUBE_ENG_SLOT7 else 0)
SK_TUBE_STALE = SK_TUBE_PHASES

# ===========================================================================
# 3.  IMPORT BANNER (verbatim) -- doctrine.py:1078-1172, map data
# ===========================================================================

# Competition-map Core anchors.  Several maps are mirror-symmetric rather than
# 180-degree symmetric, so ``(w-2-x, h-2-y)`` is not generally the enemy Core.
# The fallback keeps the bot usable on an unknown map.
CORE_PAIRS = (
    (18, 18, 2, 14, 14, 2), (26, 26, 3, 22, 21, 2),
    (21, 8, 0, 6, 19, 6), (16, 16, 2, 11, 12, 3),
    (12, 12, 1, 8, 9, 2), (20, 20, 2, 15, 16, 3),
    (25, 25, 2, 20, 21, 3), (16, 16, 0, 0, 14, 14),
    (28, 20, 2, 8, 24, 8), (14, 18, 2, 2, 2, 14),
    (24, 24, 2, 2, 20, 20), (24, 24, 2, 11, 20, 11),
    (16, 12, 4, 5, 10, 5), (22, 22, 2, 17, 18, 3),
    (10, 10, 1, 1, 7, 7), (20, 26, 2, 2, 2, 22),
    (12, 8, 0, 6, 10, 0), (25, 15, 0, 0, 0, 13),
    (21, 21, 2, 2, 2, 17), (11, 16, 0, 0, 9, 0),
    (24, 24, 2, 19, 20, 3),
    # Additional current ladder arenas recovered from submitted match replays.
    (21, 8, 5, 3, 14, 3), (26, 26, 5, 5, 19, 19),
    (10, 10, 2, 2, 6, 6), (16, 16, 3, 3, 11, 11),
    (14, 18, 6, 4, 6, 12), (20, 26, 9, 6, 9, 18),
    # Current weekly rotation, absent from the tables above (found 2026-08-06:
    # without these, known_map_for returns None and _plan_siege is disabled on
    # 5 of the 15 pool maps). eider and heart share dims AND anchors; their
    # terrain lives in EXTRA_MAP_CODES for runtime disambiguation.
    (28, 20, 7, 9, 19, 9), (25, 15, 11, 3, 11, 10),
    (25, 25, 5, 5, 18, 18), (24, 24, 4, 4, 18, 18),
)

# Exact competition terrain, packed three base-3 cells per character
# (empty=0, wall=1, ore=2).  The public map pool is fixed and downloadable;
# knowing its walls prevents greedy bots from walking into dead ends while the
# rotational fallback below still supports unseen maps.
MAP_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"
MAP_CODES = {
    (18, 18, 2, 14, 14, 2): "AAAAAGAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAANNAAAABJAAAATCAAAASLAAAABJAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAGAAAAA",
    (26, 26, 3, 22, 21, 2): "AAAAGAAACAAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAGAACASAACAAAAAAAAAAAAAAAAAAJNNNNNAMNNNNEAAAAAAAAAAAAAAAAAAACAGAACASAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAACAASAAAAA",
    (21, 8, 0, 6, 19, 6): "JSBDJCBVKDQDKFDJDADBDBAAAAAJBVJABFJANMKENAADJABDAADCGSDA",
    (16, 16, 2, 11, 12, 3): "AADAAAAJAACGABCAAGDAAAAJAAAAABAAAAAAAMNTAAAAAGNNAAAAAAAABAAAADAAAAJSAAACBSACADAAAAJAAA",
    (12, 12, 1, 8, 9, 2): "AAAGAAGAAAAAAAAAAAAAASBAAJCAAAAAAAAAAAAAAGAAGAAA",
    (20, 20, 2, 15, 16, 3): "AAAAAAAAAAAAYASAAACAAAAAAAAAADAAAAAADAAAAAADAAAAAADAAAJACDAAEJACDAAAJACDJBAJACDAAAJAAAAAAJAAAAAAJAAAAAAJAAAAAAAAAAACAAGAYAAAAAAAAAAAAA",
    (25, 25, 2, 20, 21, 3): "AAAAAAAAJABDJABDAAAAAAAAAAAASAAAAAAAAAAAAABDJABDAAAAAAAAAAAASAAGAACAAAAAAAADJABDJABAAAAAAAAAAAAGAACAAAAAAAAAAACASAAAAAAAAAAAAABDJABDJAAAAAAAAACASAAGAAAAAAAAAAAAJABDJABAAAAAAAAAAAAGAAAAAAAAAAAAJABDJABDAAAAAAAAA",
    (16, 16, 0, 0, 14, 14): "ASBJYAAAABGJJEASAAJAASDADMAJAJABEBEEMAAJCAAAAFAAMJKBKBBDADAMJAJGAADAAGAJEDSABAAAYDAHAA",
    (28, 20, 2, 8, 24, 8): "AAAAAAAAAAAGAAAAGAAAAAAAAAAAAANNNNNBAAAAAAAAAAACBAAAAADGABAAAAAABAAAAAAAAAAAAAAAAAAAAAAGYSAAAAAAGGGGAAAAAAAAAAAAGAAAAAAASADAAAAAADAABAAAAADAAAAAAAAAAAAMNNNNEAAAAAAAAAAAAACAAAACAAAAAAAAAAA",
    (14, 18, 2, 2, 2, 14): "AAAAAASAAAAAACAAAAAAAAAAAAAAAAIAAAAASMNBNNNNJNEAAASAAYAAAAAAAAAAAAAAAAAAASAASAAAAAAA",
    (24, 24, 2, 2, 20, 20): "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJBAAAAAIAASCAAAIAAYCAAAAAAAAAAAAAAAAAAAAAAAAAAJASCABAAJASCABAAAAAAAAAAAAAAAAAAAAAAAAAASIAAYAAASCAAYAAAAAJBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    (24, 24, 2, 11, 20, 11): "AAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAGAAAAAAGAAAJBAAAAAALTAAAAAAJBAAAAAAJBAAAAAAJBAAAAAAJBAAAAAALTAAAAAAJBAAAGAAAAAAGAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAA",
    (16, 12, 4, 5, 10, 5): "AAAAAGAAAAYADABSJBMAEABAAJAAAAAAAAAAAABAAJAMAEJBCJADAIAAAAGAAIAA",
    (22, 22, 2, 17, 18, 3): "AAAAAAAAAAAAAGCAAAAAAAAAAAAAAAAAMAAAAAAPBAAAAAAAAEAAAAAAMCAAAAAMAAAAAAPBAAAASAAAAAAAGAAAAAWAAAAAAMAAAAAAOAAAAAAJBAAAAAAAAWAAAAAAMAAAAAAAAAAAAAAAAAAUAAAAAAAAAAAAAA",
    (10, 10, 1, 1, 7, 7): "AAAAAGAAAAAASASAAAGAGAAAAAASAAAAAA",
    (20, 26, 2, 2, 2, 22): "AAAAAAAASAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAAAAAAAAGAAACAAASAAAMEMNNJNNBNNEMNNJNNBNNEMNNJNAAACAAAACAASAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAASAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (12, 8, 0, 6, 10, 0): "NMNAEJMABCJASGCGGSGCABSJAEBMANEN",
    (25, 15, 0, 0, 0, 13): "AAJEAAAAAAA0AAAAAAAAAAAAAAAJEAAAAAAANAAAAGAAMBAAASWRNNNBANNNNNNNANNZONNNAJNAAJEAAAACAANAAAAGAAMBAAAAAAAAAAAAAAA0AAAAAAAMBAAAA",
    (21, 21, 2, 2, 2, 17): "AAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAACAGASAAAAAAAANJNQNBNAAAAAAAACAGASAAAAAAAAGAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (11, 16, 0, 0, 9, 0): "AMBAADAAABAJAJAJABADJAABDAFAVJAADDAAKAAAEAAJBAADB0JJ0ZFJNNA",
    (24, 24, 2, 19, 20, 3): "AAAAAAAAAAAAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJNNBAAAAJAABAAAAJYCBAAAAJAAAAAAAAAABAAAAJSIBAAAAJAABAAAAJNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAAAAAAAAAAAA",
    # Current weekly rotation (meander, drumlin, saga), encoded from
    # maps/*.map26 with the same packing and round-trip verified.
    (25, 15, 11, 3, 11, 10): "ACCAAAAAAAGAAASAAAGAAAASAACAAAZAAAAAAAEAAACAJAAAAAAAGAAGAAAAAAAAAAAAACAACAAGAABAAAAAAAAAEAAASAAAJIAAASAAAAACAAGAAASAASSAAAAAA",
    (25, 25, 5, 5, 18, 18): "AAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAASAAAAGAAAAUAAAAACAGAAAAAAAAAAACASAAAAAAYAAASAAAACAAJCAADJAAAFAAACAAAGAAAYAAAAAAGAACAAAAAAAAAASAACAAAAGCAAASAAAAGAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAAAA",
    (24, 24, 4, 4, 18, 18): "ENNBCMAMBNJBAAAACAAAAAAAEADAAMCMEADGJNNMEADAJNNMBAJBYIAABNJBSACAEAESAMAMEAWGAMAMBAACJKDJAASAIGAJBAGYACAABDKBSAAJEAEAGOAMEAEACMAMASACJBNJAAYIJBAJENNBADAMENNBGDAMESEAADAMAAAAAAASAAAAJBNJEAESJNNM",
}

# Some ladder arenas are absent from the downloaded public pool.  Two 26x26
# layouts intentionally share dimensions and Core anchors, so this stays a list
# and is disambiguated from the builder's visible terrain at runtime.
EXTRA_MAP_CODES = (
    ((21, 8, 5, 3, 14, 3), "JABAJABDDDGDDDJAAAAABDAAAAADGAAAAAGAAAUAAAJJAGABBHDDADDP"),
    ((26, 26, 5, 5, 19, 19), "ENNEANNENJEMBJNNKBSAAAAMAMEAEACAAAJBAAAAAAAMAAAGCMAMZBJEGNNENJAMBJNNKNCMYAAAAGEAESGSAAJBJBIAJBJBAGASAJAJAMASADAAAAAJAGAMADADAGASAAEAEASCEAEAAGSGJBJTAAAAYMAOENNEANADMKNNTJEAZNAMAUAAAMAAAAAAAAEAAAACJBJNAMAAAAGAENNEANJEMKNNBJNNKB"),
    ((26, 26, 5, 5, 19, 19), "AAAAAAAAAACAAAAAAGGAJADAAAAAMEANBACAAAAAJBASAAAAGJBAGAAGAAMTAJAAAAJJBAFABAABJSABABADSDSMAABJAAEAASAAAAAASAAAAAASAGAAAAAAGAAAAAAGAAJBADABAMGJGJAABABGDABAABJCAEDAAAADAGNAASAASAAESAAAAGAAEAAAAAACANBJNAAAAAJADASSAAAAAAACAAAAAAAAAA"),
    ((10, 10, 2, 2, 6, 6), "DAFAAAFASBAAABAAAAAABAAAHAJCAAJCJA"),
    ((16, 16, 3, 3, 11, 11), "ENAAJEMBAAEAASNMEASMBNAACAJBAAAMHJAAAAAAACYACAAAAAADSNAAAAEAACAMBNGAJNMHAAJBAANJEAAMKB"),
    ((14, 18, 6, 4, 6, 12), "ABAFAAGABAASJGAAABCAAJAAJADAAAAAASDAAAAAAAAAAAASDAAAAAAAADABAAAJAAAADGAAGDCAGABADAPA"),
    ((20, 26, 9, 6, 9, 18), "NBJAAMEAAAAAAAAAGAAGAAAAAAJADAAJAMEBAAMNTLAAABJADAAPAAAAAAAAAAAAAAJNADASNBAGSAAAGAAUAAACASGAAAAGSAAANBJAAOEAAAAAAAAAAAAABJAASBJYDAAJAMEBAAMNBJAAABAAAAAAAAAAGAAGAAAAAAJNADAANB"),
    # eider and heart (current rotation): same dims and Core anchors, so both
    # live here and known_map_for disambiguates from sensed terrain.
    ((28, 20, 7, 9, 19, 9), "AAACAACAAAGAAAAAAGAAAAAAAAAAAAASAGAAASAAJBJBAACAAJBAMAAAAALTAGECAAAABAAJAAAAAAGICAAAAAAAAAAAAAAAAGGAAAAACAAAAAGAACASCIAACAAAOAAWAAAAAJAAJAAAAAAJADAAAGAAAAAAAAGAAACAGAAAAAAAAAAAAAAAAAAAAAA"),
    ((28, 20, 7, 9, 19, 9), "AAAAAAAAAAAAACSAAAAAAAAAAAAAAAAMAMAAAAAAMBJEAAAAANW0NEAAAJNNBNNEAAANNAANNAAADAAAAABAAAAAAAAAAAABAAAAJAACAAAAAAAGANNBAANNBAMNNBJNNEAJANWSNEJAATANCOBGBALAJBJBATAADAEAEABAASJEAJEGAYAGSGGCGAI"),
    # ============ 2026-08-13 POOL ROTATION (s36): the 10 NEW maps ============
    # Encoded by tools/map_encode.py (COMMITTED this time; the weekly-rotation
    # encoder never was). Selftest reproduces 5 old-pool entries byte-for-byte.
    # TWO COLLISION PAIRS share dims+anchors and rely on the sensed-terrain
    # disambiguation that already serves eider/heart and the two 26x26s:
    #   midgard/ragnarok (30,30,2,2,26,26) - frostgate/yulerune (20,20,2,9,16,9).
    # No key equals any pre-existing entry, so behaviour on every previously
    # known map is unchanged BY CONSTRUCTION (exact-key candidate filter).
    ((20, 20, 9, 1, 9, 17), "AAAAAAAAAAAAASAAAAAGAAAAAAJBMEJNABMNBNNAACAAAGAASAACAMEANBJNAAAIAAAAASCAAMEANBJNAACAGAASAAAACAMNBNNAEJNANBDAAAAAASAAAAAGAAAAAAAAAAAAAA"),  # auroraveil
    ((30, 30, 2, 24, 26, 4), "AABBAAAAAAAABBAAAAAASAAAAAAAAAAABTAAAAAAAABNBAAAAAAANBBAAAAAAAABACAAAAAGAABAAAAAAAABNEAAAAAAANEDAAAASAAADDCAAAAAAAAAAAAAAAAADMAAAAAAAAMAASAAAAAAAAAASAACAAAAAAAAAACAAEAAAAAAAAEDAAAAAAAAAAAAAAAAASDDAAACAAAADMNAAAAAAAMNJAAAAAAAAJAAGAAAAASAJAAAAAAAAJJNAAAAAAAJNJAAAAAAAALJAAAAAAAAAAACAAAAAAJJAAAAAAAAJJAA"),  # drakkarfjord
    ((20, 20, 2, 9, 16, 9), "NBAAAMNNAAAANEAAAAAJBAAAAADACAASAAGANBSAAAJNAAAAAJBAAAAAAAAAAAU0GAAASYICAAAAAAAAAAAAAAAAAJBAAAGANBSAAGJNACJAAAAAAEAAAAAJNBAAAMNNAAAANB"),  # frostgate
    ((30, 30, 14, 2, 14, 26), "NDAAAAAADNEDAAAAAADMBCAAAAAASJSEAAAAAAMCEBAAAAAAJMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAEMAAAAAAAJAABAAAAAAJAABAAASAACSCSAACSAACSCSAACAAAJAABAAAAAAJAABAAAAAAAEMAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAJMSEAAAAAAMCBCAAAAAASJEDAAAAAADMNDAAAAAADN"),  # glacierkeep
    ((20, 20, 1, 16, 17, 2), "AAAAAAACSAAAAAAJBAAAAEDSAASAAAAAAAAAAMAAAGACDAAMAAAEAAMAAUSAGDAEAAAAAJBJSAGGCAMAAJBAAMAAJACSAAAMAAAAAAAAAAGAAGJJBAAAAEAAAAAAGACAAAAAAA"),  # icefloe
    ((30, 30, 2, 2, 26, 26), "AAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAASAAAAAAADABAAAAAAADABAAAAAASDABAAAAAAAMEAAAAAAAAAAJEAAAAAACGAAAAAAAAMBMEMEAAASAJDAADAAAAAJDAADAAAAAJDAADAAAAAAASCAAAAAAAASCAAAAAAADAADBAAAAADAADBAAAAADAADBACAAAMEMEJEAAAAAAAAGSAAAAAAMBAAAAAAAAAAMEAAAAAAAJADCAAAAAAJADAAAAAAAJADAAAAAAACAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAA"),  # midgard
    ((30, 30, 2, 2, 26, 26), "AAAAAAAAAAAAAAAAAAAAAAOAAAAAAAADDADAJBAAJAAADAAAMAAGAEAAAAAAAAABAMAJAAAABAAJAJACJBAAJBAJAAABAJAAMAADAAAAAADAAAAJBAAADAAAAAAANEAEEAJJAAZRBDAGAASAYIAAAAAAAAYIACAAGADJZRAABBAMMAMNAAAAAAADAAAJBAAAADAAAAAADAAEAABAJAAABAJBAAJBSABABAAJAAAABAEAJAAAAAAAAAMAGAAEAAADAAABAAJBADADDAAAAAAAAWAAAAAAAAAAAAAAAAAAAAAA"),  # ragnarok
    ((20, 20, 9, 16, 9, 2), "AAAAAAAAAAAAAAIAAASCSCAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAMEMNNJNBBBADDMJJAABBNEMNNJNAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAIAIAAASCAAAAAAAAAAAAAA"),  # royale
    ((30, 30, 2, 14, 26, 14), "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAJBAACAAAAADDAAAAAAAABJAAAAAAAJAABAAASAADAADAACAAAEAAMAAAAAJCAASBAAAAAAAAAAAAAAKAAAAKAAAMDAAAADEAADAAAAAADAAABSAACJAAAABSAACJAAADAAAAAADAAMDAAAADEAAAKAAAAKAAAAAAAAAAAAAGJBAAJBGAAAAEAAMAAASAADAADAACAAAJAABAAAAAAABJAAAAAAAADDAAAAAASAJBACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),  # valkyrie
    ((20, 20, 2, 9, 16, 9), "AAAAAAAAAAAAAACAYAAAAPAAJCAAJAABAAAJADAAAALJGAAAAJBAAAAAMAAAAAAEAAAAAJBAAAAAMAAAAAAEAAAASDDCAAAJADAAAABADAAAFAAVAAAAYAACAAAAAAAAAAAAAA"),  # yulerune
)

# ===========================================================================
# 4.  IMPORT BANNER (verbatim) -- eco.py:82-223, the map layer.
#     CUT: eco.py:224-234 (the FS_V534_MAPTRUST=False legacy branch) deleted.
# ===========================================================================

def enemy_core_for(w, h, own):
    """The enemy Core anchor, from map symmetry alone.

    GENERIC BY CONSTRUCTION (LOKI-1 constraint 4): CORE_PAIRS is a table of
    map dimensions and Core anchors -- terrain, not opponents -- and the
    fallback is the plain point reflection of our own anchor.  Nothing here
    can go stale when an opponent ships a new version.
    """
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))



# LOKI-TURBO.  The base-27 map decode ran `MAP_ALPHABET.index(ch)` (a linear
# scan of a 27-character string) once per character and then rebuilt every row
# cell-by-cell in a Python genexp -- 900 cells per candidate grid, on the FIRST
# TURN OF EVERY UNIT, which is exactly where loki_analysis.md 5.2 saw the
# first-turn spike.  Each code character expands to a fixed 3-character run, so
# the expansion is a dict lookup and one str.join; the finished grid is then
# memoised, because up to eleven builders decode the same map in one match.
_CHAR3 = {
    ch: (".#o"[i % 3] + ".#o"[(i // 3) % 3] + ".#o"[(i // 9) % 3])
    for i, ch in enumerate(MAP_ALPHABET)
}
_GRID_CACHE = {}


def _decode_grid(code, w, h):
    key = (code, w, h)
    grid = _GRID_CACHE.get(key)
    if grid is None:
        flat = "".join([_CHAR3[ch] for ch in code])[:w * h]
        grid = tuple(flat[y * w:(y + 1) * w] for y in range(h))
        _GRID_CACHE[key] = grid
    return grid


# ⭐ v534 MAPTRUST.
#
# ⛔ THERE IS DELIBERATELY NO MEMO HERE, AND THE FIRST DRAFT OF THIS FIX HAD
# ONE.  It cached "grids definitively refuted" under the key (w, h, our
# anchor), on the argument that terrain is static so a refutation can never
# un-happen.  That argument is correct about a BOARD and wrong about a KEY:
# (w, h, anchor) is exactly the thing this whole build exists because it does
# not identify a map.  `test_f2.py` caught it on the one FS_MAP_SKIP map that
# is IN THE CURRENT POOL -- playing snowflake refuted archipelago's grid under
# the shared (26,26,(5,5)) key, and the next archipelago board in the same
# process then verified against an empty candidate set and came back unknown,
# silently turning archipelago's skip OFF.  A cache keyed on a colliding
# signature reintroduces the collision bug inside the collision fix.
#
# WITHOUT THE MEMO THE COST STILL SITS IN THE RIGHT PLACE, because the loop
# EXITS the moment the last candidate dies: a board that does not match is
# rejected after the first disagreeing tile, and the full sweep is paid only
# when it SUCCEEDS -- once per unit, after which the caller caches the grid and
# stops asking.  Re-verifying on every ask is also what buys opportunistic
# re-verification as a unit's vision widens, for free.


def _maptrust_pick(candidates, w, h, own, ct):
    """v534 F1 -- adopt a catalogued grid only if VISIBLE terrain confirms it.

    Replaces the parent's two unverified adoptions:
      * `len(candidates) == 1` short-circuited straight to the stored grid
        with ZERO terrain checks, so any unseen map colliding on
        (width, height, core anchor) with a catalogued singleton silently
        corrupted map_walls/map_ores/pathing for the whole match;
      * the >=2 path returned the CLOSER stored grid, never None, so a
        colliding map still adopted whichever catalogue entry it resembled
        least badly.
    Both now return None on mismatch, which every caller already routes to the
    live-sensing fallback (main.py's map_grid stays None and the ore scan /
    spiral search run; siege's v524 confirmation reads "unknown" and does not
    cripple).
    """
    if ct is None:
        # No controller, no terrain, no trust.  (Unreachable in this tree --
        # all three call sites pass ct -- kept explicit rather than falling
        # back to the unverified adoption this fix exists to remove.)
        return None
    live = candidates
    try:
        tiles = ct.get_nearby_tiles()
    except Exception:
        return None
    seen = 0
    for tile in tiles:
        x, y = tile.x, tile.y
        # ⛔ EXPLICIT BOUNDS TEST.  `get_nearby_tiles` is documented in-bounds,
        # but `is_in_vision` was documented as a bounds guard too (s50 probe)
        # and is not; an off-map index here would raise out of run() and
        # destroy the unit permanently.
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        try:
            env = ct.get_tile_env(tile)
        except Exception:
            continue
        char = "#" if env == Environment.WALL else ("o" if env == Environment.ORE_TITANIUM else ".")
        seen += 1
        keep = [g for g in live if g[y][x] == char]
        if len(keep) == len(live):
            continue
        # A disagreement.  Only trust it if the tile carries no building --
        # cheap because it costs one engine call per MISMATCH, never per tile.
        # ⛔ WHY THE GUARD EXISTS: `get_tile_env` is documented as TERRAIN and a
        # harvester sits ON an ore tile rather than replacing it, but this
        # function is asked at ANY round by a unit whose core resolved late, and
        # a build that did change what a tile reads would otherwise refute the
        # CORRECT grid.  One engine call on the rare path buys that out.
        try:
            occupied = ct.get_tile_building_id(tile) is not None
        except Exception:
            occupied = True
        if occupied:
            continue
        live = keep
        if not live:
            return None
    if seen < SK_MAP_MIN_TILES:
        # A degenerate ask (no vision yet).  Adopting on ~nothing is the very
        # thing this fix removes; the caller retries next round.
        return None
    return live[0]


def known_map_for(w, h, own, ct=None):
    candidates = []
    for (mw, mh, ax, ay, bx, by), code in tuple(MAP_CODES.items()) + EXTRA_MAP_CODES:
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        candidates.append(_decode_grid(code, w, h))
    if not candidates:
        return None
    return _maptrust_pick(candidates, w, h, own, ct)

# ===========================================================================
# END IMPORT BANNER.  Everything below this line is SKALMAN-original.
# ===========================================================================

# ============================================================================
# HEIMDALL v0 DEMO (2026-08-22, Magnus: "I want reels on this bot as soon as
# possible") — DEMO-GRADE dispatch override for the FORTRESS DOCTRINE
# (PROGRAMME.md): all builders home until r300, then two raiders + sentinels.
# ⛔ NOT A PLANK. No identity discipline, no screens claimed — a watchable
# prototype while the design study cuts the real plank set. The known demo
# compromises: multiple bodies run the keeper turn (single-writer-per-slot is
# violated; buffered last-write-wins absorbs most of it), and the phase flip
# re-uses the existing cage-walker + siege-engineer verbs untuned.
# ============================================================================
HEIM_DEMO = True             # master demo flag (whole tree is the demo)
HEIM_FLIP_ROUND = 300        # Magnus: "until round 300 our entire focus is eco"
# HEIM DEMO (Magnus, watching the showcase reel: "Why is our raiders putting
# barriers, they just need to put down sentinels and if they go down they need
# to put up new ones on other spots") — siege raiders skip the COPY 5 prep
# entirely: sentinels only. Re-siting on death already exists (death memo bans
# the dead tile 400r, V3 re-site picks a new band spot). Tail override: last
# assignment wins at import.
SK_NEST_PREP_BARRIERS = 0
