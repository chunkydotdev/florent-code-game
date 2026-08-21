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
SK_CYCLE_BREAK = False     # FIX 3.  ⛔ NOT A PLANK -- CHASSIS CORRECTNESS, flagged
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
SK_CAGE_ACCEPT = 7           # accept 7 of 8; the eighth tile is not the plank
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
