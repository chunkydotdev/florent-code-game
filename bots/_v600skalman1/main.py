"""SKALMAN v1 (`_v600skalman1`) -- the founding tree of the Skalman line.

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

        # --- movement / targeting -------------------------------------
        self.tgt = None
        self.stuck = 0
        self.prev_pos = None          # displacement memory (renamed raid_prev)
        self.thrown_rnd = -1
        self._nav_key = None
        self._nav_tpl = None

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
        self.door_guns = 0            # COPY 6b answers bought (capped)

        # --- CAGE WALKER --------------------------------------------------
        self.lap_i = None
        self.cage_sealed = set()
        self.cage_best = 0
        self.cage_advance = -1
        self.melee_tile = None
        self.melee_since = -1

        # --- ORE DENIER ---------------------------------------------------
        self.deny_tile = None
        self.denied = 0
        self.denied_tiles = set()

        # --- SIEGE ENGINEER -----------------------------------------------
        self.nest_site = None
        self.nest_face = None
        self.nest_prepped = 0
        self.nest_turret = None       # (id, Position, born round)
        self.nest_deaths = {}         # V4: (x,y) -> round it killed a turret
        self.nest_lives = []
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
