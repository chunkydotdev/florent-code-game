"""KILLBOX PROBE — team B (the victim team). IN-GAME Florent Code League probe.

Both bots in this probe are ours. B walks designated builders into team A's
launcher pickup range and then runs the TRAP assertions from inside the sealed
chambers of A's two-chamber cell block (P=(20,7), Q=(20,9), column x=20).

  STEP5a can_move on all 4 cardinals          -> expect all False
  STEP5b blind move() inside try/except       -> log the exception TYPE (contained)
  STEP8  build-escape: can_build_* on every adjacent tile -> expect all False;
         can_fire on an adjacent barrier      -> expect True (the only exit verb)
  STEP5c peck the W barrier                   -> expect legal, 2 damage, 2 Ti
  STEP9  jailer race: keep pecking while A heals the same barrier -> HP must net-RISE
  STEP5d heal-through-wall from an outside B builder -> can_heal(P) False
  STEP7  PEEL: victim3 calls move() UNGUARDED -> the engine must retire it

ALL output on stderr (stdout is a dead channel locally, CLAUDE.md s54 correction).
Terrain is embedded: get_tile_env RAISES `Position out of vision range` (run-1 finding).
"""
import sys
from collections import deque

from fcode import Controller, Direction, EntityType, Position

CARD = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)

WALLS = frozenset([(4, 4), (4, 5), (4, 6), (4, 7), (4, 10), (5, 7), (5, 10), (6, 7),
                   (6, 10), (7, 7), (8, 11), (8, 12), (8, 13), (9, 4), (9, 5), (9, 6),
                   (10, 10), (10, 11), (10, 12), (10, 13), (10, 16), (10, 17), (10, 18),
                   (10, 19), (11, 8), (11, 10), (11, 19), (12, 8), (12, 10), (12, 19),
                   (13, 8), (13, 10), (13, 19), (16, 10), (16, 19), (16, 21), (17, 10),
                   (17, 19), (17, 21), (18, 10), (18, 19), (18, 21), (19, 10), (19, 11),
                   (19, 12), (19, 13), (19, 16), (19, 17), (19, 18), (19, 19), (20, 23),
                   (20, 24), (20, 25), (21, 16), (21, 17), (21, 18), (22, 22), (23, 19),
                   (23, 22), (24, 19), (24, 22), (25, 19), (25, 22), (25, 23), (25, 25),
                   (25, 24)])

P = (20, 7)
Q = (20, 9)
RACE_WALL = (19, 7)
A_BUILT = frozenset([(20, 4), (20, 6), (20, 8), (20, 10), (19, 7), (21, 7),
                     (19, 9), (21, 9), (24, 7)])
BAIT = (25, 7)            # d^2 = 1 from A's launcher at (24,7)
STAGE = (26, 11)
CADENCE_PROBE = False   # flip to True to force back-to-back throws (cadence probe)
BAIT2 = (24, 6)
STAGE2 = (27, 13)
HEAL_ROUTE = [(26, 5), (21, 5), (21, 6)]   # (21,6) is orth-adjacent to A's wall (21,7)
HEAL_HOLD_UNTIL = 80          # A finishes building ~r65; do not body-block its builder
CORE_TILES = {(26, 26), (27, 26), (26, 27), (27, 27)}
RACE_ROUNDS = 26


def L(ct, *a):
    print("[B r%d]" % ct.get_current_round(), *a, file=sys.stderr)


class Player:
    def __init__(self):
        self.order = []
        self.roles = {}
        self.seen = {}
        self.tphase = {}
        self.ucount = None
        self.race_start = None
        self.race_trace = []
        self.race_done = False
        self.pecks = 0
        self.heal_done = False
        self.peel_logged = False
        self.hp_last = {}
        self.hroute = {}
        self.retired_flag = False
        self.prev_wall_hp = None

    # ---------- pathing ----------
    def blocked(self, x, y):
        return ((x, y) in WALLS or (x, y) in CORE_TILES or (x, y) in A_BUILT
                or (x, y) in (P, Q))

    def step_dir(self, ct, start, goal):
        w, h = ct.get_map_width(), ct.get_map_height()
        prev = {start: None}
        q = deque([start])
        found = False
        while q:
            cur = q.popleft()
            if cur == goal:
                found = True
                break
            cx, cy = cur
            for d in CARD:
                dx, dy = d.delta()
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in prev:
                    continue
                if (nx, ny) != goal and self.blocked(nx, ny):
                    continue
                prev[(nx, ny)] = cur
                q.append((nx, ny))
        if not found:
            return None
        node = goal
        while prev[node] != start:
            node = prev[node]
        dx, dy = node[0] - start[0], node[1] - start[1]
        for d in CARD:
            if d.delta() == (dx, dy):
                return d
        return None

    def walk(self, ct, goal):
        pos = ct.get_position()
        here = (pos.x, pos.y)
        if here == goal:
            return True
        if ct.get_move_cooldown() != 0:
            return False
        d = self.step_dir(ct, here, goal)
        if d is None:
            L(ct, "PATH-FAIL %s -> %s" % (here, goal))
            return False
        if ct.can_move(d):
            ct.move(d)
        return False

    # CROSS-UNIT STATE: the engine gives EVERY UNIT ITS OWN Player instance
    # (measured run 3), so roles and flags travel through the comms store:
    #   slots 0..3 = builder entity ids in spawn order (index == role)
    #   slot 4     = victim1 has finished the jailer race
    #   slot 5     = both victim1 and victim2 have been retired
    ROLES = ("victim1", "healer", "victim2", "victim3")

    def role_of(self, ct, uid):
        for i in range(4):
            if ct.read_store(i) == uid:
                return self.ROLES[i]
        return None

    # ---------- entry ----------
    def run(self, ct: Controller) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            try:
                self.core(ct)
            except Exception as e:
                L(ct, "CORE-EXC", type(e).__name__, e)
            return
        if kind != EntityType.BUILDER_BOT:
            return
        uid = ct.get_id()
        role = self.role_of(ct, uid)
        if role is None:
            return
        pos = ct.get_position()
        here = (pos.x, pos.y)

        if role == "victim3" and here in (P, Q):
            # ------- STEP 7, THE PEEL: UNGUARDED move(). Must escape run(). -------
            if not self.peel_logged:
                self.peel_logged = True
                L(ct, "STEP7 victim3 %d is in chamber %s; can_move(N)=%s move_cd=%d "
                      "— calling move(NORTH) UNGUARDED now"
                  % (uid, here, ct.can_move(Direction.NORTH), ct.get_move_cooldown()))
            ct.move(Direction.NORTH)        # deliberately unprotected
            return

        if ct.get_current_round() % 100 == 0:
            L(ct, "HB %s %d at %s move_cd=%d act_cd=%d store=%s"
              % (role, uid, here, ct.get_move_cooldown(), ct.get_action_cooldown(),
                 [ct.read_store(i) for i in range(6)]))
        try:
            self.act(ct, uid, role, here)
        except Exception as e:
            L(ct, "EXC-LEAK role=%s uid=%d %s %s" % (role, uid, type(e).__name__, e))

    def act(self, ct, uid, role, here):
        if role == "victim1":
            if here in (P, Q):
                self.trap(ct, uid, here)
            else:
                self.walk(ct, BAIT)
            return
        if role == "healer":
            i = self.hroute.get(uid, 0)
            if i >= 1 and ct.get_current_round() < HEAL_HOLD_UNTIL:
                return          # hold off A's construction corridor
            if i < len(HEAL_ROUTE):
                if self.walk(ct, HEAL_ROUTE[i]):
                    self.hroute[uid] = i + 1
                return
            self.heal_test(ct, uid)
            return
        if role == "victim2":
            if here in (P, Q):
                self.trap(ct, uid, here)
            elif CADENCE_PROBE:
                self.walk(ct, BAIT2)
            elif ct.read_store(4) == 1:
                self.walk(ct, BAIT)
            else:
                self.walk(ct, STAGE)
            return
        if role == "victim3":
            if ct.read_store(5) == 1:
                self.walk(ct, BAIT)
            else:
                self.walk(ct, STAGE2)
            return

    # ---------- core ----------
    def core(self, ct):
        n = ct.get_unit_count()
        if n != self.ucount:
            L(ct, "UNIT-COUNT %s -> %d (round %d)" % (self.ucount, n, ct.get_current_round()))
            self.ucount = n
        if len(self.order) == 4 and n <= 3 and not self.retired_flag:
            self.retired_flag = True
            ct.write_store(5, 1)
            L(ct, "both victims retired (unit_count=%d incl. core) -> store[5]=1, "
                  "victim3 released for the peel" % n)
        if len(self.order) >= 4 or ct.get_action_cooldown() != 0:
            return
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = ct.get_position().add(d)
            try:
                ok = ct.can_spawn(t)
            except Exception:
                ok = False
            if ok:
                bid = ct.spawn_builder(t)
                self.order.append(bid)
                idx = len(self.order) - 1
                role = self.ROLES[idx]
                ct.write_store(idx, bid)
                L(ct, "spawned %s id=%d at (%d,%d) -> store[%d]=%d"
                  % (role, bid, t.x, t.y, idx, bid))
                return

    # ---------- the trap ----------
    def trap(self, ct, uid, cell):
        ph = self.tphase.get(uid, 0)
        r = ct.get_current_round()
        pos = ct.get_position()
        race_wall = (cell[0] - 1, cell[1])   # this chamber's WEST barrier

        if ph == 0:
            L(ct, "STEP4-VERIFY victim %d position=(%d,%d) == chamber %s -> PASS | "
                  "tile_builder_bot_id=%s hp=%d/%d move_cd=%d action_cd=%d"
              % (uid, pos.x, pos.y, cell,
                 ct.get_tile_builder_bot_id(Position(*cell)),
                 ct.get_hp(), ct.get_max_hp(), ct.get_move_cooldown(),
                 ct.get_action_cooldown()))
            res = {}
            for d in CARD:
                n = pos.add(d)
                res[d.name] = (ct.can_move(d), ct.is_tile_passable(n), ct.is_tile_empty(n))
            allf = all(not v[0] for v in res.values())
            L(ct, "STEP5a per-cardinal (can_move, passable, empty): %s -> %s"
              % (res, "PASS (all can_move False)" if allf else "FAIL"))
            self.tphase[uid] = 1
            return

        if ph == 1:
            if ct.get_move_cooldown() != 0:
                return
            caught = None
            try:
                ct.move(Direction.NORTH)
                caught = ("NO-EXCEPTION", "move succeeded")
            except Exception as e:
                caught = (type(e).__name__, str(e))
            L(ct, "STEP5b blind move(NORTH) -> exception %s (%s) | still at (%d,%d) -> %s"
              % (caught[0], caught[1], ct.get_position().x, ct.get_position().y,
                 "PASS (raised, contained, unit survives)"
                 if caught[0] != "NO-EXCEPTION" else "FAIL"))
            self.tphase[uid] = 2
            return

        if ph == 2:
            # ---- STEP 8: BUILD-ESCAPE CHECK ----
            rows = {}
            for d in CARD:
                n = pos.add(d)
                rows[d.name] = dict(
                    barrier=ct.can_build_barrier(n),
                    conveyor=ct.can_build_conveyor(n, Direction.NORTH),
                    gunner=ct.can_build_gunner(n, Direction.NORTH),
                    harvester=ct.can_build_harvester(n),
                    launcher=ct.can_build_launcher(n),
                    fire=ct.can_fire(n),
                )
            no_build = all(not v[k] for v in rows.values()
                           for k in ("barrier", "conveyor", "gunner", "harvester",
                                     "launcher"))
            can_peck = all(v["fire"] for v in rows.values())
            for k, v in rows.items():
                L(ct, "STEP8 %-5s %s" % (k, v))
            L(ct, "STEP8 build-escape: every can_build_* on all 4 adjacent tiles False "
                  "-> %s | can_fire on all 4 barriers True -> %s | own tile "
                  "can_build_barrier(self)=%s"
              % ("PASS" if no_build else "FAIL", "PASS" if can_peck else "FAIL",
                 ct.can_build_barrier(pos)))
            self.tphase[uid] = 3
            return

        if ph == 3:
            if ct.get_action_cooldown() != 0:
                return
            wp = Position(*race_wall)
            bid = ct.get_tile_building_id(wp)
            if bid is None:
                L(ct, "STEP5c FAIL no building at %s" % (race_wall,))
                self.tphase[uid] = 4
                return
            hp0, ti0 = ct.get_hp(bid), ct.get_global_resources()
            ok = ct.can_fire(wp)
            if ok:
                ct.fire(wp)
                self.pecks += 1
                L(ct, "STEP5c peck barrier%s id=%d: can_fire=True, hp %d->%d (dmg=%d, "
                      "expect 2) ti %d->%d (cost=%d, expect 2) action_cd_after=%d -> %s"
                  % (race_wall, bid, hp0, ct.get_hp(bid), hp0 - ct.get_hp(bid),
                     ti0, ct.get_global_resources(), ti0 - ct.get_global_resources(),
                     ct.get_action_cooldown(),
                     "PASS" if hp0 - ct.get_hp(bid) == 2 else "FAIL"))
            else:
                L(ct, "STEP5c FAIL can_fire(barrier)=False")
            self.tphase[uid] = 4
            return

        if ph == 4 and cell != P:
            self.tphase[uid] = 5
            return
        if ph == 4:
            # ---- STEP 9: JAILER RACE (this victim keeps pecking; A heals) ----
            wp = Position(*race_wall)
            bid = ct.get_tile_building_id(wp)
            if bid is None:
                self.tphase[uid] = 5
                return
            hp = ct.get_hp(bid)
            # Trigger on an OBSERVED HP RISE: a fixed threshold races with the
            # jailer's heal (A acts before B in a round) and never fires.
            if self.race_start is None and self.prev_wall_hp is not None \
                    and hp > self.prev_wall_hp:
                self.race_start = r
                L(ct, "STEP9 race window OPEN at r%d: barrier hp ROSE %d->%d, so A's "
                      "jailer is healing the tile this bot is pecking"
                  % (r, self.prev_wall_hp, hp))
            self.prev_wall_hp = hp
            if self.race_start is not None:
                self.race_trace.append((r, hp))
            if ct.get_action_cooldown() == 0 and ct.can_fire(wp):
                ct.fire(wp)
                self.pecks += 1
            if self.race_start is not None and r >= self.race_start + RACE_ROUNDS:
                hps = [t[1] for t in self.race_trace]
                stuck = {d.name: ct.can_move(d) for d in CARD}
                L(ct, "STEP9 JAILER RACE r%d..r%d: barrier hp %d -> %d (net %+d, "
                      "min=%d max=%d) after %d total pecks | trace=%s"
                  % (self.race_start, r, hps[0], hps[-1], hps[-1] - hps[0],
                     min(hps), max(hps), self.pecks, self.race_trace))
                L(ct, "STEP9 verdict: heal outruns peck -> %s | victim still trapped "
                      "(can_move %s) -> %s"
                  % ("PASS" if hps[-1] > hps[0] else "FAIL", stuck,
                     "PASS" if not any(stuck.values()) else "FAIL"))
                ct.write_store(4, 1)
                L(ct, "STEP9 store[4]=1 -> victim2 released toward the second chamber")
                self.race_done = True
                self.tphase[uid] = 5
            return

        # ph >= 5: idle; report hp changes so the execution is visible from B's side
        hp = ct.get_hp()
        if self.hp_last.get(uid) != hp:
            L(ct, "victim %d in %s hp=%d" % (uid, cell, hp))
            self.hp_last[uid] = hp

    # ---------- STEP 5d ----------
    def heal_test(self, ct, uid):
        if self.heal_done:
            return
        pos = ct.get_position()
        occ_p = ct.get_tile_builder_bot_id(Position(*P))
        if occ_p is None:
            return
        self.heal_done = True
        pp = Position(*P)
        wp = Position(21, 7)
        can_p, can_w = ct.can_heal(pp), ct.can_heal(wp)
        d2 = pos.distance_squared(pp)
        L(ct, "STEP5d healer %d at (%d,%d): can_heal(P%s)=%s [d2=%d, orth-adjacent=%s] "
              "| can_heal(enemy barrier (21,7))=%s -> %s"
          % (uid, pos.x, pos.y, P, can_p, d2, d2 == 1, can_w,
             "PASS (both False — no heal reaches into a sealed chamber)"
             if (not can_p and not can_w) else "FAIL"))
