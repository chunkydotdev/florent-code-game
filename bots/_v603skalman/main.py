"""SKALMAN v603 (`_v603skalman`) -- v602 plus the tape602 KILL-LEVER fixes.

⛔ WHAT CHANGED FROM `_v602skalman`, and the doctrine change behind it.  Source:
`scratchpad/s54_autopsy602/tape602_autopsy.md` (30 game-sides, 15 pool maps x
both seats, one NOISE_OFF `_v542wave` opponent).  ⚠ FIXTURE_OF_RECORD: one
authored opponent on a local screen PRIORITISES; it does not establish field
prevalence.  Verification artefacts: `scratchpad/s54_v603/`.

THE HEADLINE THE TAPE FORCED: **100% of the 14,130 damage dealt to the enemy
core in 30 games was SENTINEL fire** -- zero pecks, zero gunner, zero launcher --
and we won 0 of 14 games with <= 1 sentinel against 6 of 16 with >= 2 (Fisher
2-sided p = 0.019).  ⇒ THE KILL LEVER IS SENTINEL COUNT.  The cage is a
healer-denial multiplier on the gun (heal-tax 0.49 at mean-held >= 3 vs 0.71
below it); it is not a damage channel and must not be sold seats to look for one.

  FIX 1  SK_NEST_PAIR        the siege engineer keeps TWO band sentinels
         standing, funded off COPY 7's own `need` arithmetic (no burst-bank).
         Ablation: sentinels 49 -> 34, >=2-share 53.3% -> 13.3%, sentinel shots
         1,144 -> 789, second-gun round 87 -> 180.  `_siege_engineer`,
         `_plant_gun`, `_nest_watch`, `_pick_nest`, `_nest_publish`.
  FIX 2  SK_TRUNK_NEAR       `_trunk_tiles()` EXCLUDED d^2 <= 13 of our own core
         and 87.3% of belt deaths happen inside it (victim d^2 median 1).  The
         cover set now carries the near trunk, the TERMINUS seats and the tiles
         a pecker must stand on.  Ablation: gunners 52 -> 27, near-trunk tiles
         covered at end 23/160 -> 5/139, belt deaths 34 -> 53, terminus deaths
         26 -> 41, peck-class deaths covered 5 -> 0.  `_trunk_tiles`,
         `_terminus_tiles`, `_cover_gun_action`.
  FIX 3  SK_EVICT_ARMED      the `not empty_seals` interlock is gone: eviction of
         an enemy building on a seal seat runs whenever the walker is at the ring
         with no BUILD action available, belt seats first and turrets last.
         Ablation: seal-seat attacks 366 -> 33, ring evictions 30 -> 1.
         `_evict_seal`, `_cage_walker`.
  FIX 4  SK_COLLAR_GUNS      stop the mass collar peck (91.1% of our melee
         budget, losing the exchange 4.8:1).  Ablation: collar pecks 359 ->
         1,544 per 30 games.  ⭐ The sub-flags matter and are separately
         ablatable: `SK_HOMEDEF_SKIP_BARRIER` (ON) carries essentially the whole
         reduction, `SK_COLLAR_ROUTE_GATE` (OFF, measured negative) does not.
         `_belt_evict`, `_route_gaps`, `_home_defence`.
  FIX 5  SK_CAGE_CEIL        ⛔ BUILT, MEASURED, SHIPPED OFF.  The dynamic accept
         bar works (rounds at/over bar 52 -> 1,062) and the outcome goes the
         other way (kills 8 -> 6).  See the flag's own comment.
  FIX 6  SK_LAP_ADJ_SEAL / SK_IDLE_ACT / SK_SPAWN_EXIT -- from the lap-stall
         diagnosis (`scratchpad/s54_v603/diag/`), which found THREE causes and
         not one: a danger-veto throat (1 of 6 games), a lap-advance livelock
         (4 of 6) and an enemy spawn-box (2 of 6).  Seal any adjacent empty seal
         seat, act when boxed, and never spawn into a zero-exit tile.
         Ablation: lapadj_off drops max_held median 3 -> 2 and raises belt deaths
         34 -> 57; spawnexit_off drops kills 8 -> 6; SK_IDLE_ACT is an exact NULL
         on this tape (the spawn fix pre-empts the box) and is kept as insurance.

--- the v602 header follows, unchanged ---

SKALMAN v602 (`_v602skalman`) -- v601 plus the tape601 NAVIGATION fixes.

⛔ WHAT CHANGED FROM `_v601skalman`.  Every number is from
`scratchpad/s54_autopsy601/tape601_autopsy.md` (v600: 15 distinct games seat A;
v601: 30 game-sides, both seats; one NOISE_OFF `_v542wave` opponent).  ⚠ One
local fixture, one opponent: FIXTURE_OF_RECORD makes this a PRIORITISATION, not
a field measurement.

  FIX 1  SK_CAGE_FIRST   the lap (seal behind / clear ahead / advance) now
         outranks `_peck_priority` inside `_cage_walker`, and the enemy CORE is
         off the walker's peck ladder while seal tiles are open.  v601 inserted
         the peck BETWEEN the seal and the advance; the core is adjacent to
         every seal tile by construction, so 92.6% (286/309) of walker lap
         actions became pecks, ring barriers/game fell 1.933 -> 0.767 and one
         walker parked 41 consecutive rounds losing a healing race 95:82.
         `sk_roles._cage_walker`, `_peck_priority(skip_core=)`.
  FIX 2  SK_DANGER_NAV   the movement layer reads `armed_memo` at last.  A tile
         a remembered enemy turret's RAY covers is taken only when no uncovered
         step exists.  fimbulwinter seat A: 42 bodies, 39 deaths, ALL on tile
         (7,6), all from one gunner at (8,7) we never touched.
         `sk_common._danger_tiles`, `_nav`.
  FIX 3  SK_CYCLE_BREAK  ⛔ CHASSIS CORRECTNESS, flagged for ablation only.
         A-B-A-B position shuttles are endemic (81.3%/97.9% of builder steps on
         fimbulwinter, 91.0%/72.7% on the v600 control); all four stavkirke
         seat-B builders sat in one for 1000 rounds and built nothing.  The step
         back is struck out, perpendiculars first, hold if neither.
         `sk_common._two_cycle_back`, `_nav`, `sk_roles._escape`.
  FIX 4  (no flag)       `_enemy_builder_adjacent` is FOOTPRINT-AWARE: the core
         is 2x2 and a heal on any of its four tiles heals all of it, so a healer
         beside a different core tile was invisible to the guard.  Plain bugfix.
  FIX 5  SK_SENSE_NAV    `_bfs_direction` fell back to greedy whenever
         `map_grid is None` -- 10 of 15 pool maps -- so navigation had NO wall
         knowledge there at all; and `_pick_nest` returned None on the same
         test, leaving the nest verb inert on two thirds of the pool.  Both now
         run off sensed terrain, every role sensing, with refutation halves.
         `sk_common._bfs_direction`, `sk_roles._pick_nest`, `_nest_site_watch`.
  FIX 6  (no flag)       `lattice_floor` applied unconditionally in `_drip`
         (96.8% -> 100% by construction).  `sk_core._drip`.

--- the v601 header follows, unchanged ---

SKALMAN v601 (`_v601skalman`) -- v600 plus three SURVIVABILITY planks.

⛔ WHAT CHANGED FROM `_v600skalman1`, and why each change exists.  Every number
below is from `scratchpad/s54_autopsy/tape30_autopsy.md` (n = 15 DISTINCT games;
the *_s11/_s12 pairs are byte-identical, the seed is inert).

  PLANK 1  SK_HARV_ESCALATE  the V1 rebuild ledger, extended from CONVEYOR
           tiles to HARVESTER tiles + killer inference published on slot 14.
           33/33 harvester deaths were annulus gunners; one gunner ate 22
           harvesters off one tile.  `sk_roles._harv_watch`,
           `_harvester_action`, `_infer_killer`, `_killer_report`.
  PLANK 2  SK_BELT_COVER     home-gun siting now scores (site, FACING) pairs
           and requires the facing RAY to cross live belt trunk beyond
           d^2 13.  0 of 42 dead belt pieces were in any firing line of ours.
           `sk_roles._door_action`, `_ray_cover`, `_cover_gun_action`.
  PLANK 3  SK_TARGET_PRIO    one strict target ladder for BOTH turret fire and
           builder pecks; a BARRIER is never a default target.  75.3% of our
           shots and 74.8% of our pecks landed on enemy barriers.
           `sk_roles._target_pri`, `_peck_priority`, `_turret`.
  BUGFIX   SK_ORE_SENSE      live-sensed ore.  7 of 15 games built ZERO
           harvesters because `map_ores` is empty on any map `known_map_for`
           cannot confirm (10 of the 15 pool maps) and nothing else ever walks
           a keeper to ore.  `sk_common._ore_scan` / `ore_list`.

--- the founding tree's own header follows, unchanged ---

SKALMAN v1 (`_v600skalman1`) -- the founding tree of the Skalman line.

Doctrine: `beancounters_replication_then_amplify` (PROGRAMME.md, 2026-08-21).
Phase 1 is REPLICATE THE MEASURED BASICS PROPERLY; phase 2 amplifies with our
own toolbox once the basics measure at parity.  `R1000_IS_DEFEAT` survives the
line change: the cage, the belt and the nest are MEANS -- core destruction is
the end.

Design: `docs/SKALMAN-DESIGN-2026-08-21.md`
Imports: `docs/research/SKALMAN-IMPORT-MANIFEST-2026-08-21.md`
Copy-spec: `docs/research/PLAYBOOK-beancounters-2026-08-21.md` §6

FILE MAP -- "which lines implement COPY N" is answerable per verb:

  sk_maps.py    map data + constants + the SK_* verb flags + the fresh store
                allocation; the VERBATIM map layer (MAPTRUST F1).
  sk_common.py  in_bounds, pack/unpack, the CPU guard, the displacement guard,
                the padded-BFS pathing, the tile-ownership arbiter (V2/V8),
                the target-HP-trend give-up rule (V7).
  sk_roles.py   COPY 8 role claim · COPY 8/#78 global belt + V1 escalation ·
                COPY 9 cage · COPY 1 ore denial · COPY 5 nest + V3/V4/V9 ·
                COPY 6+2 door and turret behaviour.
  sk_core.py    COPY 8 spawn plan · COPY 7 drip · COPY 6 threat publication.

WHAT v1 DELIBERATELY DOES NOT CONTAIN (design §5, so nobody greps for it):
no launchers · no ferry · no rush opening · no burst-bank funding · no
point-blank sentinel plants · no crash/kidnap toolbox · no CPU-denial anything
· no tiebreak-turtle branch.

⛔ SANDBOX AST CONSTRAINTS -- `finally:`, `except BaseException:` and
`except SystemExit:` are REJECTED BY THE VALIDATOR AT LOAD.  There are zero of
each in this tree and there must remain zero.  The wrapper below catches bare
`Exception`; SystemExit/KeyboardInterrupt derive from BaseException and
propagate automatically, which is both what the engine wants and the only thing
the validator permits.
"""

from fcode import Controller, Direction, EntityType, Environment, Position  # noqa: F401

from sk_core import CoreMixin
from sk_maps import SK_ROLES
from sk_common import CommonMixin
from sk_roles import RolesMixin


class Player(CommonMixin, RolesMixin, CoreMixin):

    def __init__(self):
        # --- identity / map (per-unit: module state is NOT shared between
        #     units -- one sub-interpreter each, engine-probed; the 16 store
        #     ints are the only channel and they lag one round) -------------
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.idx = 0
        self.seat = -1
        self.role = None
        self.role_parity = 0
        self.map_grid = None
        self.map_walls = set()
        self.map_ores = []
        # v601 BUGFIX (SK_ORE_SENSE): live-sensed ore, the fallback `_load_grid`
        # promised and never had.  `ore_scanned` makes each tile cost exactly
        # ONE get_tile_env over this unit's whole life, so the scan is bounded
        # by map area, not by rounds.
        self.sensed_ores = []
        self.sensed_ore_xy = set()
        self.ore_scanned = set()
        self.explore_i = 0
        self.explore_until = -1

        # --- movement / targeting -------------------------------------
        self.tgt = None
        self.stuck = 0
        self.prev_pos = None          # displacement memory (renamed raid_prev)
        self.thrown_rnd = -1
        self._nav_key = None
        self._nav_tpl = None
        # v602 FIX 3: the 4-entry position ring the 2-cycle detector reads, and
        # its counters.  ⛔ ON THE DISPLACEMENT GUARD'S CLEAR LIST (build rule
        # 5): it is a cross-round Position cache for a throwable body.
        self.pos_hist = []
        self.cycle_len = 0            # consecutive rounds the A-B-A-B held
        self.cycle_blocked = 0        # ... in which the break found no step
        self.cycle_escapes = 0        # capped demolition escapes used
        # v602 FIX 2: how many consecutive steps have been danger detours.
        self.danger_detour = 0
        self._danger_key = -1         # cache revision the set was built at
        self._danger_set = frozenset()

        # --- report-once latches --------------------------------------
        self.reported_cpu = False
        self.reported_error = False

        # --- sensing ---------------------------------------------------
        self.vis_enemy = []
        self.vis_friend = []
        self.enemy_harv = {}          # COPY 1 memory: (x,y) -> round last seen
        self.enemy_facing = {}        # COPY 2: enemy turret id -> (dx, dy)
        self.hp_memo = {}             # V7: target id -> (hp, round)
        self.give_up = {}             # V7: target id -> round we gave up
        # v601 PLANK 1/3: where enemy ARMED buildings have been seen, keyed on
        # the TILE and not the id -- a turret is immovable, so the tile is the
        # durable fact and it survives the entity leaving vision.
        self.armed_memo = {}          # (x,y) -> (EntityType, round last seen)
        # v602 FIX 2: the same fact keyed the same way for the DANGER TERM --
        # a turret's facing, so the movement layer can price a RAY not a disc.
        # `enemy_facing` is keyed on the entity id, which does not survive the
        # turret leaving vision; this is the tile-keyed twin.
        self.armed_facing = {}        # (x,y) -> (dx, dy)
        self._armed_rev = 0           # bumped on news; the danger cache key

        # --- HOME KEEPER ------------------------------------------------
        self.harv_tiles = set()
        self.belt_plan = {}
        self.belt_key = None
        self.belt_built = set()
        self.belt_rebuilds = {}       # V1: (x,y) -> rebuild count
        self.belt_escalated = set()   # V1: tiles that became turret tasks
        self.belt_ban = set()
        self.belt_head = {}
        self.belt_cursor = None
        self.escape_ban = {}          # tile -> round the self-trap escape ends
        # --- v603 FIX 4: the collar peck ledger -----------------------------
        self.collar_pecks = {}        # tile -> pecks spent evicting an enemy
                                      # building off a planned belt tile
        self._gap_rnd = -1            # `_route_gaps` per-round memo
        self._gap_key = None
        self._gap_set = frozenset()
        self.door_guns = 0            # COPY 6b answers bought (capped)
        # --- v601 PLANK 1: the harvester half of the V1 rebuild ledger -------
        self.harv_deaths = {}         # (x,y) -> harvesters lost on that tile
        self.harv_ban = {}            # (x,y) -> round the ban expires
        self.harv_escalated = set()   # (x,y) -> a locate-the-shooter task now
        self.harv_killer = {}         # (x,y) -> Position of the inferred killer
        self.killer_pos = None        # newest inferred belt killer (published)
        self.killer_rnd = -1

        # --- CAGE WALKER --------------------------------------------------
        self.lap_i = None
        self.cage_sealed = set()
        self.cage_best = 0
        self.cage_advance = -1
        self.melee_tile = None
        self.melee_since = -1
        # v603 FIX 5: seal seats last SEEN carrying an ENEMY DELIVERY BELT
        # piece.  Remembered rather than re-sensed because the ceiling has to
        # stay stable when a seat leaves vision -- an unseen seat contributes to
        # neither `sealed` nor `empties`, and a ceiling that oscillates with
        # vision would flip the accept bar every time the walker turns a corner.
        self.cage_enemy = set()

        # --- ORE DENIER ---------------------------------------------------
        self.deny_tile = None
        self.denied = 0
        self.denied_tiles = set()

        # --- SIEGE ENGINEER -----------------------------------------------
        self.nest_site = None
        self.nest_face = None
        self.nest_prepped = 0
        self.nest_turret = None       # (id, Position, born round)
        # v603 FIX 1: the SECOND band sentinel, same tuple shape.  Two slots
        # rather than a list so `_nest_watch`'s per-turret V3/V4 bookkeeping
        # stays one branch per gun and the ablation is one flag.
        self.nest_turret2 = None
        self.nest_site2 = None        # the standing first site, while siting #2
        self.nest_deaths = {}         # V4: (x,y) -> round it killed a turret
        self.nest_lives = []
        # v602 FIX 5(b): sites refuted by vision (wall) or by the reachability
        # watchdog.  Without this set the re-pick oscillates on one tile.
        self.nest_bad = set()
        self.nest_best_d = None       # closest approach to the current site
        self.nest_since = -1          # round that closest approach was set
        self.stall_latched = False
        self.stall_shifted = False

        # --- CORE ----------------------------------------------------------
        self.spawned = 0
        self.converts = 0

    # ------------------------------------------------------------------
    # entry -- VERBATIM `main.py:396-418` of `bots/_v542wave`, retargeted
    # ------------------------------------------------------------------

    def run(self, ct):
        # An exception escaping run() makes the engine PERMANENTLY delete this
        # unit for the rest of the match.  Catching it costs one round's
        # action instead; there is no situation where propagating is better.
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e == EntityType.GUNNER or e == EntityType.SENTINEL:
            self._turret(ct)
        # LAUNCHER has no arm: v1 ships zero launchers (design §3, "Ferry: NO
        # in v1").  An unreachable branch is worse than none -- if a launcher
        # ever appears on this team it is a bug, and it costs one idle unit
        # rather than a wrong behaviour.
