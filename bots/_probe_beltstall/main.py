"""ENGINE PROBE (QUEUE #66a) -- when a harvester's dead-end conveyor chain
SATURATES (every conveyor tile holding a stack), does the harvester STALL
(emission pauses, resumes when space frees up -- lossless) or DISCARD
(emissions past saturation are gone -- lossy)?

DESIGN. The core computes a chain plan at round 0 (it has vision r^2=36 and
does pure arithmetic, no game actions beyond the normal spawn) and publishes
it through the communication store; the single builder bot just executes it:
walk to an ore tile, build a harvester, then build a straight conveyor chain
leading away from it.

TWO MODES, selected by the BELTSTALL_MODE env var ("treatment" default, or
"control"):
  - treatment: the chain is a genuine DEAD END -- 3 conveyors in a straight
    line pointing AWAY from our own core, never connected to any acceptor.
    This is the condition under test.
  - control: the chain is the SHORTEST straight/L-shaped path from an ore
    tile near our own core INTO our own core's footprint (the last conveyor
    faces a core tile). This proves the instrument can see a stack actually
    depart the chain and land in the core (get_global_resources() rising),
    so a static reading in the treatment is a finding, not a broken probe.

OBSERVATION. Every round after the chain is complete, print (stdout -- kept
by local `fcode run`, unlike platform replays):
    BELT r=<round> mode=<mode> chain=[id_or_-, ...] distinct_head=<n> gres=<v>
  chain[i] is the stack id currently on chain conveyor i (index 0 = the
  conveyor adjacent to the harvester, the "head"), or '-' if empty.
  distinct_head is the cumulative count of DISTINCT stack ids ever observed
  on chain[0] -- the STALL/DISCARD discriminator (see file docstring on the
  reporting side): if the harvester stalls, the same id sits at the head
  once the belt is full and the running distinct-count freezes; if it
  discards, the count keeps climbing every ~4 rounds even with the belt
  full (a new id displaces the old one at the head with nowhere for the old
  one to go).

Run:
    BELTSTALL_MODE=treatment .venv/bin/fcode run bots/_probe_beltstall bots/_probe_beltstall maps/frostgate.map26 --seed 1 --tle 10
    BELTSTALL_MODE=control   .venv/bin/fcode run bots/_probe_beltstall bots/_probe_beltstall maps/antler.map26   --seed 1 --tle 10
"""
import os
import sys
from collections import deque

from fcode import Controller, Direction, EntityType, Environment, Position

CARDS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
DIR_CODE = {Direction.NORTH: 0, Direction.EAST: 1, Direction.SOUTH: 2, Direction.WEST: 3}
CODE_DIR = {v: k for k, v in DIR_CODE.items()}
CHAIN_LEN = 3

SLOT_CORNER = 0
SLOT_ORE = 2
SLOT_CHAIN_TILE0 = 3   # 3,4,5
SLOT_CHAIN_DIR0 = 6    # 6,7,8
SLOT_CHAIN_LEN = 9
SLOT_READY = 10


def pack_pos(pos: Position) -> int:
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    if val == 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def nearest_cardinal(dx: int, dy: int) -> Direction:
    if abs(dx) >= abs(dy):
        return Direction.EAST if dx >= 0 else Direction.WEST
    return Direction.SOUTH if dy >= 0 else Direction.NORTH


DELTA_TO_DIR = {d.delta(): d for d in CARDS}


def bfs_first_step(ct: Controller, start: Position, target: Position,
                    avoid: set[Position]) -> Direction | None:
    """Shortest-path first step from `start` to a tile orthogonally adjacent to
    `target`, staying within vision and avoiding walls/buildings/`avoid`.

    A straight-line greedy walk oscillates forever when an obstacle (e.g. the
    harvester we just built) sits directly between the builder and its next
    target -- observed empirically as an infinite 2-tile bounce. BFS over the
    small, vision-bounded local area is cheap and avoids that class of bug
    entirely.
    """
    if start.distance_squared(target) == 1:
        return None  # already adjacent
    visited = {start}
    parent: dict[Position, Position] = {}
    queue = deque([start])
    goal = None
    while queue:
        cur = queue.popleft()
        if cur != start and cur.distance_squared(target) == 1:
            goal = cur
            break
        for d in CARDS:
            nxt = cur.add(d)
            if nxt in visited or nxt == target or nxt in avoid:
                continue
            try:
                if not ct.is_in_vision(nxt):
                    continue
                if not ct.is_tile_passable(nxt):
                    continue
            except Exception:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            queue.append(nxt)
    if goal is None:
        return None
    cur = goal
    while parent[cur] != start:
        cur = parent[cur]
    dx, dy = cur.x - start.x, cur.y - start.y
    return DELTA_TO_DIR.get((dx, dy))


def get_mode() -> str:
    try:
        m = os.environ.get("BELTSTALL_MODE", "treatment")
    except Exception:
        m = "treatment"
    return m if m in ("treatment", "control") else "treatment"


class Player:
    def __init__(self):
        self.mode = get_mode()
        # core state
        self.corner: Position | None = None
        self.planned = False
        self.spawned = False
        # builder state
        self.phase = "init"          # init -> goto_ore -> build_harvest -> goto_chain -> build_chain -> observe
        self.harvester_pos: Position | None = None
        self.chain_tiles: list[Position] = []
        self.chain_dirs: list[Direction] = []
        self.chain_index = 0
        self.chain_ids: list[int] = []
        self.distinct_head_ids: set[int] = set()
        self.saturation_round: int | None = None
        self.stuck_rounds = 0
        # resumption sub-test: after the belt has sat saturated for a while,
        # extend the dead end by one tile and see whether/when a fresh id
        # appears at the head -- tests whether the harvester "remembers" a
        # produced-but-blocked stack (resumes fast) vs. just resumes on its
        # normal 4-round schedule once room exists.
        self.observe_count = 0
        self.extended = False
        self.extend_started_round: int | None = None
        self.EXTEND_AFTER = 60

    def run(self, ct: Controller) -> None:
        try:
            if ct.get_entity_type() == EntityType.CORE:
                self._core(ct)
            elif ct.get_entity_type() == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as exc:
            print(f"BELT ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    # ---------------------------------------------------------------- CORE

    def _core(self, ct: Controller) -> None:
        if self.corner is None:
            self.corner = ct.get_position()

        if not self.planned:
            self._plan_chain(ct)
            self.planned = True

        if not self.spawned and ct.get_action_cooldown() == 0:
            p = ct.get_position()
            for d in Direction:
                if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                    ct.spawn_builder(p.add(d))
                    self.spawned = True
                    return

    def _plan_chain(self, ct: Controller) -> None:
        corner = self.corner
        footprint = [corner, corner.add(Direction.EAST), corner.add(Direction.SOUTH),
                     corner.add(Direction.SOUTHEAST)]
        ore_tiles = [t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM]
        if not ore_tiles:
            print(f"BELT CORE PLAN FAIL: no ore in vision at round 0", file=sys.stderr)
            return

        if self.mode == "control":
            # pick the ore tile with the shortest Manhattan path to the nearest
            # footprint tile, so the chain into the core stays inside our budget.
            best = None
            for t in ore_tiles:
                f0 = min(footprint, key=lambda f: abs(f.x - t.x) + abs(f.y - t.y))
                dist = abs(f0.x - t.x) + abs(f0.y - t.y)
                if best is None or dist < best[0]:
                    best = (dist, t, f0)
            dist, H, f0 = best
            if dist < 1 or dist - 1 > CHAIN_LEN:
                print(f"BELT CORE PLAN WARN: control chain len {dist - 1} outside budget "
                      f"(H=({H.x},{H.y}) f0=({f0.x},{f0.y})) -- attempting anyway", file=sys.stderr)
            # L-shaped path from H to f0: walk dx first, then dy.
            path: list[Position] = []
            cur = H
            dx = f0.x - H.x
            step = 1 if dx > 0 else -1
            for _ in range(abs(dx)):
                cur = Position(cur.x + step, cur.y)
                path.append(cur)
            dy = f0.y - H.y
            step = 1 if dy > 0 else -1
            for _ in range(abs(dy)):
                cur = Position(cur.x, cur.y + step)
                path.append(cur)
            # path now ends at f0 (the core tile itself); conveyors go on
            # every tile EXCEPT the final one.
            conveyor_tiles = path[:-1]
            dirs = []
            prev = H
            for i, tile in enumerate(conveyor_tiles):
                nxt = path[i + 1]  # next tile in the full path (conveyor or f0)
                dirs.append(nearest_cardinal(nxt.x - tile.x, nxt.y - tile.y))
            chain_tiles = conveyor_tiles[:CHAIN_LEN]
            chain_dirs = dirs[:CHAIN_LEN]
            print(f"BELT CORE PLAN control H=({H.x},{H.y}) f0=({f0.x},{f0.y}) "
                  f"chain={[(t.x, t.y) for t in chain_tiles]} dirs={[d.name for d in chain_dirs]}",
                  file=sys.stderr)
        else:
            # treatment: dead end, straight line AWAY from our own core.
            best = None
            for t in ore_tiles:
                d2 = t.distance_squared(corner)
                if d2 <= 8:
                    continue  # exclude direct-handoff confound (matches _probe_harvest)
                if best is None or d2 < best[0]:
                    best = (d2, t)
            if best is None:
                # fall back to the farthest tile we can see rather than fail outright
                best = max(((t.distance_squared(corner), t) for t in ore_tiles), key=lambda x: x[0])
                print(f"BELT CORE PLAN WARN: no ore with d2>8, falling back to farthest", file=sys.stderr)
            _, H = best
            away = nearest_cardinal(H.x - corner.x, H.y - corner.y)
            dx, dy = away.delta()
            chain_tiles = [Position(H.x + dx * i, H.y + dy * i) for i in range(1, CHAIN_LEN + 1)]
            chain_dirs = [away] * CHAIN_LEN
            print(f"BELT CORE PLAN treatment H=({H.x},{H.y}) away={away.name} "
                  f"chain={[(t.x, t.y) for t in chain_tiles]}", file=sys.stderr)

        ct.write_store(SLOT_CORNER, pack_pos(corner))
        ct.write_store(SLOT_ORE, pack_pos(H))
        for i in range(CHAIN_LEN):
            if i < len(chain_tiles):
                ct.write_store(SLOT_CHAIN_TILE0 + i, pack_pos(chain_tiles[i]))
                ct.write_store(SLOT_CHAIN_DIR0 + i, DIR_CODE[chain_dirs[i]])
            else:
                ct.write_store(SLOT_CHAIN_TILE0 + i, 0)
        ct.write_store(SLOT_CHAIN_LEN, min(len(chain_tiles), CHAIN_LEN))
        ct.write_store(SLOT_READY, 1)

    # ------------------------------------------------------------ BUILDER

    def _builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()

        if self.phase == "init":
            if ct.read_store(SLOT_READY) != 1:
                return  # plan not visible yet (store writes land next round)
            self.harvester_pos = unpack_pos(ct.read_store(SLOT_ORE))
            n = ct.read_store(SLOT_CHAIN_LEN)
            self.chain_tiles = []
            self.chain_dirs = []
            for i in range(n):
                t = unpack_pos(ct.read_store(SLOT_CHAIN_TILE0 + i))
                d = CODE_DIR[ct.read_store(SLOT_CHAIN_DIR0 + i)]
                self.chain_tiles.append(t)
                self.chain_dirs.append(d)
            self.phase = "goto_ore"

        avoid = set(self.chain_tiles)
        if self.harvester_pos is not None:
            avoid.add(self.harvester_pos)

        if self.phase == "goto_ore":
            self._advance(ct, self.harvester_pos, avoid, on_arrive=self._try_build_harvester)
            return

        if self.phase == "goto_chain":
            target = self.chain_tiles[self.chain_index]
            self._advance(ct, target, avoid, on_arrive=self._try_build_chain_tile)
            return

        if self.phase == "goto_extend":
            # Keep printing the per-round reading while walking to the
            # extension tile, so a blocked/failed extend never truncates the
            # primary saturation observation stream.
            self._observe(ct)
            target = self.chain_tiles[self.chain_index]
            self._advance(ct, target, avoid, on_arrive=self._try_build_chain_tile)
            return

        if self.phase == "observe":
            self._observe(ct)
            return

    def _try_build_harvester(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        if ct.can_build_harvester(self.harvester_pos):
            hid = ct.build_harvester(self.harvester_pos)
            print(f"BELT r={ct.get_current_round()} mode={self.mode} "
                  f"HARVESTER BUILT id={hid} at ({self.harvester_pos.x},{self.harvester_pos.y})",
                  file=sys.stderr)
            if not self.chain_tiles:
                # ore was directly adjacent to the core footprint (control only) --
                # no conveyor needed, the harvester hands off straight to the core.
                self.phase = "observe"
                print(f"BELT r={ct.get_current_round()} mode={self.mode} "
                      f"CHAIN EMPTY (direct harvester-to-core handoff) ids=[]", file=sys.stderr)
            else:
                self.phase = "goto_chain"
                self.chain_index = 0

    def _try_build_chain_tile(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        tile = self.chain_tiles[self.chain_index]
        d = self.chain_dirs[self.chain_index]
        if ct.can_build_conveyor(tile, d):
            cid = ct.build_conveyor(tile, d)
            self.chain_ids.append(cid)
            print(f"BELT r={ct.get_current_round()} mode={self.mode} "
                  f"CONVEYOR[{self.chain_index}] BUILT id={cid} at ({tile.x},{tile.y}) facing={d.name}",
                  file=sys.stderr)
            self.chain_index += 1
            if self.chain_index >= len(self.chain_tiles):
                self.phase = "observe"
                print(f"BELT r={ct.get_current_round()} mode={self.mode} "
                      f"CHAIN COMPLETE ids={self.chain_ids}", file=sys.stderr)
            else:
                self.phase = "goto_chain"

    def _advance(self, ct: Controller, target: Position, avoid: set[Position], on_arrive) -> None:
        p = ct.get_position()
        if p.distance_squared(target) == 1:
            on_arrive(ct)
            return
        # not adjacent yet -- BFS a step closer, avoiding chain/harvester tiles.
        # (A greedy "nearest cardinal" walk oscillates forever when an obstacle
        # like the just-built harvester sits on the straight path -- see the
        # bfs_first_step docstring.)
        if ct.get_move_cooldown() != 0:
            return
        step = bfs_first_step(ct, p, target, avoid)
        moved = False
        if step is not None and ct.can_move(step):
            ct.move(step)
            moved = True
        if moved:
            self.stuck_rounds = 0
        else:
            self.stuck_rounds += 1
            if self.stuck_rounds % 20 == 0:
                print(f"BELT r={ct.get_current_round()} mode={self.mode} "
                      f"STUCK at ({p.x},{p.y}) heading to ({target.x},{target.y}) "
                      f"for {self.stuck_rounds} rounds (bfs_step={step})", file=sys.stderr)

    def _observe(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        ids = []
        for cid in self.chain_ids:
            try:
                sid = ct.get_stored_resource_id(cid)
            except Exception:
                sid = None
            ids.append(sid)
        if ids and ids[0] is not None:
            self.distinct_head_ids.add(ids[0])
        all_full = all(i is not None for i in ids)
        if all_full and self.saturation_round is None:
            self.saturation_round = rnd
            print(f"BELT r={rnd} mode={self.mode} SATURATION FIRST OBSERVED "
                  f"ids={ids}", file=sys.stderr)
        gres = ct.get_global_resources()
        chain_str = [i if i is not None else "-" for i in ids]
        print(f"BELT r={rnd} mode={self.mode} chain={chain_str} "
              f"distinct_head={len(self.distinct_head_ids)} gres={gres} "
              f"extended={self.extended}")

        # Resumption sub-test (treatment dead ends only -- control already
        # flows). Once we've held a stable saturated read for EXTEND_AFTER
        # rounds, extend the dead end by one tile and watch whether/when a
        # fresh id shows up at the head, relative to the round count.
        self.observe_count += 1
        if (self.mode == "treatment" and not self.extended and all_full
                and self.observe_count >= self.EXTEND_AFTER and self.chain_tiles):
            last_tile = self.chain_tiles[-1]
            last_dir = self.chain_dirs[-1]
            dx, dy = last_dir.delta()
            new_tile = Position(last_tile.x + dx, last_tile.y + dy)
            self.chain_tiles.append(new_tile)
            self.chain_dirs.append(last_dir)
            self.chain_index = len(self.chain_tiles) - 1
            self.extended = True
            self.extend_started_round = rnd
            self.phase = "goto_extend"
            print(f"BELT r={rnd} mode={self.mode} EXTEND START target=({new_tile.x},{new_tile.y})",
                  file=sys.stderr)
