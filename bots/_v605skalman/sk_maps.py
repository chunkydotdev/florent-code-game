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
SK_BLOCK_MEMO_TTL = 150   # FIX 2: a remembered blocker nobody has re-seen in N
                          # rounds is dropped.  ⛔ THE BACKSTOP FOR THE TILE THAT
                          # IS NEVER REVISITED: the vision drop above only fires
                          # where a body actually goes, and a building destroyed
                          # on the far side of the map would otherwise be
                          # believed forever.  It is a decay, not a refutation.
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
#  15    FREE                --                phase-2 amplify claims downward
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

# --- COPY 5, the nest band -------------------------------------------------
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
SK_NEST_PAIR_N = 2           # FIX 1: how many band sentinels the engineer keeps
                             # standing.  TWO, and the number is the measured
                             # threshold, not a taste: 0 wins / 14 games with
                             # <= 1 sentinel built, 6 wins / 16 with >= 2.
                             # ⛔ NOT THREE.  Every sentinel is +20% on the ONE
                             # global additive cost scale, and the tape's own
                             # >=2 cell is a 2-4 band whose median is 2.
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
SK_CYCLE_HIST_K = 12         # FIX 2: the position ring under SK_CYCLE_K.  Twelve
                             # entries detect any period k <= 6 with TWO full
                             # repeats, which is the evidence bar -- one repeat is
                             # a coincidence on a lap that legitimately revisits
                             # tiles.
SK_CYCLE_K_MAX = 6           # FIX 2: the longest period detected.  The measured
                             # livelocks are period 6-10; 6 is what 12 entries can
                             # carry at two repeats, and the longer ones contain a
                             # period-<=6 sub-pattern often enough that the commit
                             # window still breaks them (reported, not assumed).
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
SK_NEST_STUCK_ROUNDS = 60    # a nest site the engineer has not closed on in N
                             # rounds is unreachable; ban it and re-pick.  ⛔ The
                             # ban is what stops the re-pick oscillating: without
                             # it `_pick_nest` scores the same tile again next
                             # round, forever.

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
