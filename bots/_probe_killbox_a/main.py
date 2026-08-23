"""KILLBOX PROBE — team A (the executioner). IN-GAME Florent Code League probe.

Both bots in this probe are ours; every term below is an in-engine mechanic.

TWO-CHAMBER CELL BLOCK on maps/midgard.map26 (30x30, core A 2,2 / core B 26,26),
colinear on ONE sentinel ray down column x=20 facing SOUTH:

        (20,4)  S   sentinel, facing SOUTH
        (20,5)      open
        (20,6)  #   barrier
        (20,7)  P   chamber 1        d2(S,P)=9
        (20,8)  #   SHARED barrier
        (20,9)  Q   chamber 2        d2(S,Q)=25   (both <= 32 = sentinel r2)
        (20,10) #   barrier
   side walls: (19,7) (21,7) (19,9) (21,9)      -> 7 barriers total
   launcher L=(24,7): d2->P = 16, d2->Q = 20    (both <= 26 throw range)
   jailer post (18,7): orthogonally adjacent to the W wall (19,7), OFF the ray

Steps 1-7 = the base choreography; 8 build-escape, 9 jailer race, 10 the ray
question (does the sentinel hit the TARGETED tile or the FIRST body on the ray).

ALL output on stderr (stdout is a dead channel locally, CLAUDE.md s54 correction).
ENGINE FACT learned in run 1: get_tile_env/get_tile_* RAISE
`GameError: Position out of vision range` outside the unit's vision, so terrain
is embedded here rather than probed.
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
                   (23, 22), (24, 19), (24, 22), (25, 19), (25, 22), (25, 23), (25, 24),
                   (25, 25)])

P = (20, 7)
Q = (20, 9)
SENT = (20, 4)
SENT_FACE = Direction.SOUTH
LAU = (24, 7)
JAIL = (18, 7)
BAIT = (25, 7)
CADENCE_PROBE = False   # flip to True to force back-to-back throws (cadence probe)
BAIT2 = (24, 6)
RACE_WALL = (19, 7)          # the barrier the trapped bot pecks / the jailer heals
RACE_TRIGGER_HP = 16
CORE_TILES = {(2, 2), (3, 2), (2, 3), (3, 3)}

# (waypoint to stand on, what to build there)
STEPS = [
    ((19, 4), ("sentinel", SENT, SENT_FACE)),
    ((19, 6), ("barrier", (19, 7), None)),
    ((19, 8), ("barrier", (19, 9), None)),
    ((20, 11), ("barrier", (20, 10), None)),
    ((21, 10), ("barrier", (21, 9), None)),
    ((21, 6), ("barrier", (21, 7), None)),
    ((21, 8), ("barrier", (20, 8), None)),
    ((20, 5), ("barrier", (20, 6), None)),
    ((23, 7), ("launcher", LAU, None)),
    (JAIL, None),
]


def L(ct, *a):
    print("[A r%d]" % ct.get_current_round(), *a, file=sys.stderr)


class Player:
    def __init__(self):
        self.built = set()
        self.step = 0
        self.spawned = False
        self.sent_id = None
        self.launch_round = None
        self.launches = []        # (round, victim_id, chamber)
        self.cd_trace = []
        self.shots = 0
        self.ray_probe_done = False
        self.pocket_start = None
        self.pocket_end = None
        self.build_cost = 0
        self.occupants = {}       # chamber -> victim id
        self.race_heals = 0
        self.race_log = []
        self.peel_victim = None
        self.peel_round = None
        self.peel_done = False
        self.exec_target = None   # chamber currently being executed
        self.kill_log = []        # (victim, chamber, shots, rounds)
        self.exec_start = None
        self.phase = "build"
        self.peel_armed = False
        self.peel_note = False
        self.seal_audit = False

    # ---------- pathing ----------
    def blocked(self, x, y):
        return ((x, y) in WALLS or (x, y) in self.built or (x, y) in CORE_TILES
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

    # ---------- entry ----------
    def run(self, ct: Controller) -> None:
        kind = ct.get_entity_type()
        try:
            if kind == EntityType.CORE:
                self.core(ct)
            elif kind == EntityType.BUILDER_BOT:
                self.builder_turn(ct)
            elif kind == EntityType.SENTINEL:
                self.sentinel_turn(ct)
            elif kind == EntityType.LAUNCHER:
                self.launcher_turn(ct)
        except Exception as e:
            L(ct, "EXC in %s: %s %s" % (kind, type(e).__name__, e))

    # ---------- core ----------
    def core(self, ct):
        if ct.get_current_round() == 0:
            L(ct, "map %dx%d scale=%.2f%% ti=%d ammo=%d | COSTS barrier=%d sentinel=%d "
                  "launcher=%d builder=%d"
              % (ct.get_map_width(), ct.get_map_height(), ct.get_scale_percent(),
                 ct.get_global_resources(), ct.get_global_ammo(),
                 ct.get_barrier_cost(), ct.get_sentinel_cost(), ct.get_launcher_cost(),
                 ct.get_builder_bot_cost()))
        if ct.get_global_ammo() < 150 and ct.can_convert_ammo(150):
            ct.convert_ammo(150)
            L(ct, "ammo converted -> ammo=%d ti=%d"
              % (ct.get_global_ammo(), ct.get_global_resources()))
        if not self.spawned and ct.get_action_cooldown() == 0:
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
                    self.spawned = True
                    L(ct, "spawned builder id=%d at (%d,%d) ti=%d scale=%.2f%%"
                      % (bid, t.x, t.y, ct.get_global_resources(), ct.get_scale_percent()))
                    return

    # ---------- builder ----------
    def builder_turn(self, ct):
        pos = ct.get_position()
        here = (pos.x, pos.y)
        if self.step >= len(STEPS) - 1 and here == JAIL:
            return self.jailer(ct)
        wp, job = STEPS[self.step]
        if here != wp:
            if ct.get_move_cooldown() != 0:
                return
            d = self.step_dir(ct, here, wp)
            if d is None:
                L(ct, "PATH-FAIL %s -> %s" % (here, wp))
                return
            if ct.can_move(d):
                ct.move(d)
            return
        if job is None:
            self.step += 1
            return
        if ct.get_action_cooldown() != 0:
            return
        what, tgt, extra = job
        tp = Position(tgt[0], tgt[1])
        ti0 = ct.get_global_resources()
        sc0 = ct.get_scale_percent()
        if what == "barrier":
            if self.pocket_start is None:
                self.pocket_start = ct.get_current_round()
            if not ct.can_build_barrier(tp):
                L(ct, "STEP1 FAIL can_build_barrier%s=False from %s" % (tgt, here))
                self.step += 1
                return
            bid = ct.build_barrier(tp)
            self.built.add(tgt)
            got = ct.get_tile_building_id(tp)
            et = ct.get_entity_type(got) if got is not None else None
            ok = (got == bid and et == EntityType.BARRIER)
            cost = ti0 - ct.get_global_resources()
            self.build_cost += cost
            L(ct, "STEP1 barrier%s id=%d verify tile_building_id=%s type=%s hp=%d -> %s "
                  "| cost=%d scale %.2f->%.2f"
              % (tgt, bid, got, et, ct.get_hp(bid), "PASS" if ok else "FAIL",
                 cost, sc0, ct.get_scale_percent()))
            if len({(20, 6), (20, 8), (20, 10), (19, 7), (21, 7), (19, 9), (21, 9)} & self.built) == 7:
                self.pocket_end = ct.get_current_round()
                for name, cell in (("P", P), ("Q", Q)):
                    seal = []
                    for d in CARD:
                        n = Position(cell[0], cell[1]).add(d)
                        try:
                            b2 = ct.get_tile_building_id(n)
                            seal.append(b2 is not None
                                        and ct.get_entity_type(b2) == EntityType.BARRIER)
                        except Exception as ex:
                            seal.append("OOV:%s" % type(ex).__name__)
                    L(ct, "STEP1 SEAL %s%s n/e/s/w=%s passable=%s empty=%s -> %s"
                      % (name, cell, seal, ct.is_tile_passable(Position(*cell)),
                         ct.is_tile_empty(Position(*cell)),
                         "PASS" if all(x is True for x in seal) else "UNVERIFIED"))
                L(ct, "STEP1 cell block rounds %s..%s (%d rounds), 7 barriers"
                  % (self.pocket_start, self.pocket_end,
                     self.pocket_end - self.pocket_start + 1))
        elif what == "sentinel":
            pre_p = ct.can_fire_from(tp, extra, EntityType.SENTINEL, Position(*P))
            pre_q = ct.can_fire_from(tp, extra, EntityType.SENTINEL, Position(*Q))
            tiles = ct.get_attackable_tiles_from(tp, extra, EntityType.SENTINEL)
            L(ct, "STEP2 PRE can_fire_from(S%s,%s,SENTINEL,P)=%s Q=%s | P_in_pattern=%s "
                  "Q_in_pattern=%s pattern_n=%d -> %s"
              % (tgt, extra.name, pre_p, pre_q, Position(*P) in tiles,
                 Position(*Q) in tiles, len(tiles),
                 "PASS" if (pre_p and pre_q) else "FAIL"))
            L(ct, "STEP2 pattern=%s" % ([tuple(t) for t in tiles],))
            if not ct.can_build_sentinel(tp, extra):
                L(ct, "STEP2 FAIL can_build_sentinel=False from %s" % (here,))
                self.step += 1
                return
            sid = ct.build_sentinel(tp, extra)
            self.sent_id = sid
            self.built.add(tgt)
            cost = ti0 - ct.get_global_resources()
            self.build_cost += cost
            L(ct, "STEP2 sentinel id=%d at %s facing=%s hp=%d cost=%d scale %.2f->%.2f"
              % (sid, tgt, ct.get_direction(sid).name, ct.get_hp(sid), cost,
                 sc0, ct.get_scale_percent()))
        elif what == "launcher":
            if not ct.can_build_launcher(tp):
                L(ct, "STEP3 FAIL can_build_launcher=False from %s" % (here,))
                self.step += 1
                return
            lid = ct.build_launcher(tp)
            self.built.add(tgt)
            cost = ti0 - ct.get_global_resources()
            self.build_cost += cost
            L(ct, "STEP3 launcher id=%d at %s d2->P=%d d2->Q=%d hp=%d cost=%d "
                  "scale %.2f->%.2f"
              % (lid, tgt, Position(*tgt).distance_squared(Position(*P)),
                 Position(*tgt).distance_squared(Position(*Q)),
                 ct.get_hp(lid), cost, sc0, ct.get_scale_percent()))
            L(ct, "BUILD-COMPLETE round=%d total_build_ti=%d (+150 ammo) ti_left=%d "
                  "scale=%.2f%% ammo=%d"
              % (ct.get_current_round(), self.build_cost, ct.get_global_resources(),
                 ct.get_scale_percent(), ct.get_global_ammo()))
            self.phase = "hunt"
        self.step += 1

    # ---------- step 9: the jailer ----------
    def jailer(self, ct):
        if not self.seal_audit:
            self.seal_audit = True
            for name, cell in (("P", P), ("Q", Q)):
                seal = []
                for d in CARD:
                    n = Position(cell[0], cell[1]).add(d)
                    try:
                        b2 = ct.get_tile_building_id(n)
                        seal.append((tuple(n), b2, b2 is not None
                                     and ct.get_entity_type(b2) == EntityType.BARRIER))
                    except Exception as ex:
                        seal.append((tuple(n), "OOV", type(ex).__name__))
                L(ct, "STEP1 SEAL AUDIT %s%s from jailer post %s: %s | passable=%s "
                      "empty=%s -> %s"
                  % (name, cell, JAIL, seal, ct.is_tile_passable(Position(*cell)),
                     ct.is_tile_empty(Position(*cell)),
                     "PASS" if all(x[2] is True for x in seal) else "FAIL"))
        wp = Position(*RACE_WALL)
        bid = ct.get_tile_building_id(wp)
        if bid is None:
            return
        hp = ct.get_hp(bid)
        if self.race_heals == 0 and hp > RACE_TRIGGER_HP:
            return                       # damage sub-phase: let them chew it down
        if ct.get_action_cooldown() != 0:
            return
        if hp >= ct.get_max_hp(bid):
            self.race_log.append((ct.get_current_round(), hp, "at-max"))
            return
        ok = ct.can_heal(wp)
        ti0 = ct.get_global_resources()
        if not ok:
            L(ct, "STEP9 FAIL can_heal(own barrier %s)=False from %s" % (RACE_WALL, JAIL))
            return
        ct.heal(wp)
        self.race_heals += 1
        hp1 = ct.get_hp(bid)
        self.race_log.append((ct.get_current_round(), hp, hp1))
        if self.race_heals <= 3:
            L(ct, "STEP9 heal#%d barrier%s hp %d->%d (+%d) ti %d->%d action_cd=%d"
              % (self.race_heals, RACE_WALL, hp, hp1, hp1 - hp, ti0,
                 ct.get_global_resources(), ct.get_action_cooldown()))
        if self.race_heals == 12:
            hps = [r[1] for r in self.race_log]
            L(ct, "STEP9 JAILER RACE over %d heals: barrier hp trace %s | first=%d "
                  "last=%d net=%+d -> %s"
              % (self.race_heals, self.race_log, hps[0], hp1, hp1 - hps[0],
                 "PASS (heal outruns peck)" if hp1 > hps[0] else "FAIL"))

    # ---------- launcher (steps 3-4, 7) ----------
    # CROSS-UNIT STATE: the engine gives EVERY UNIT ITS OWN Player instance
    # (measured run 3), so team coordination goes through the comms store.
    #   slot 0 = number of launches performed (0..3); 3 == PEEL ARMED, no shots.
    def launcher_turn(self, ct):
        r = ct.get_current_round()
        cd = ct.get_action_cooldown()
        if self.launch_round is not None and r <= self.launch_round + 10:
            self.cd_trace.append((r, cd))
        pp, qq = Position(*P), Position(*Q)
        occ_p = ct.get_tile_builder_bot_id(pp)
        occ_q = ct.get_tile_builder_bot_id(qq)
        for name, cell, occ in (("P", P, occ_p), ("Q", Q, occ_q)):
            was = self.occupants.get(name)
            if was is not None and occ is None:
                self.occupants[name] = None
                if was == self.peel_victim:
                    L(ct, "STEP7 PEEL RESULT: victim %d thrown into %s at r%d called "
                          "move() UNGUARDED and is GONE at r%d (%d rounds later); "
                          "sentinel shots fired during the peel = 0 -> PASS"
                      % (was, name, self.peel_round, r, r - self.peel_round))
                    L(ct, "SUMMARY launches (round, victim, chamber)=%s | launcher "
                          "action_cd after each launch, per round=%s"
                      % (self.launches, self.cd_trace))
                else:
                    L(ct, "chamber %s freed at r%d (victim %d gone)" % (name, r, was))
            elif occ is not None:
                self.occupants[name] = occ
        n = len(self.launches)
        if n >= 3:
            return
        if cd != 0:
            return
        if n == 0:
            target, tname = (pp, "P") if occ_p is None else (None, None)
        elif n == 1:
            target, tname = (qq, "Q") if occ_q is None else (None, None)
        else:
            if occ_p is not None or occ_q is not None:
                return
            target, tname = pp, "P"
        if target is None:
            return
        mine = ct.get_team()
        for uid in ct.get_nearby_units(2):
            try:
                if ct.get_team(uid) == mine:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                vp = ct.get_position(uid)
            except Exception:
                continue
            if (vp.x, vp.y) not in ((BAIT if not CADENCE_PROBE else BAIT), BAIT2 if CADENCE_PROBE else BAIT):
                continue
            # PEEL must be armed a round early: store writes are buffered, and the
            # sentinel must already see "3" before the victim lands.
            if n == 2 and not self.peel_armed:
                self.peel_armed = True
                ct.write_store(0, 3)
                L(ct, "STEP7 arming peel: wrote store[0]=3 (visible next round), "
                      "holding the throw one round so the sentinel is silent")
                return
            d2pick = ct.get_position().distance_squared(vp)
            d2throw = ct.get_position().distance_squared(target)
            ok = ct.can_launch(vp, target)
            L(ct, "STEP4 can_launch(ENEMY builder %d @(%d,%d) -> %s%s)=%s | "
                  "d2_pickup=%d d2_throw=%d passable(target)=%s -> %s"
              % (uid, vp.x, vp.y, tname, (target.x, target.y), ok, d2pick, d2throw,
                 ct.is_tile_passable(target), "PASS" if ok else "FAIL"))
            if not ok:
                return
            ammo0 = ct.get_global_ammo()
            ct.launch(vp, target)
            self.launches.append((r, uid, tname))
            self.launch_round = r
            after = ct.get_tile_builder_bot_id(target)
            np_ = ct.get_position(uid)
            L(ct, "STEP4 launch #%d SAME ROUND: tile_builder_bot_id(%s)=%s "
                  "victim_pos=(%d,%d) launcher_action_cd_after=%d ammo %d->%d -> %s"
              % (len(self.launches), tname, after, np_.x, np_.y,
                 ct.get_action_cooldown(), ammo0, ct.get_global_ammo(),
                 "PASS" if (np_.x, np_.y) == (target.x, target.y) else "FAIL"))
            self.occupants[tname] = uid
            if len(self.launches) < 3:
                ct.write_store(0, len(self.launches))
            else:
                self.peel_victim = uid
                self.peel_round = r
                L(ct, "STEP7 PEEL victim %d is in %s; sentinel disarmed via store[0]=3"
                  % (uid, tname))
            return

    # ---------- sentinel: steps 6 + 10 ----------
    def sentinel_turn(self, ct):
        r = ct.get_current_round()
        launches = ct.read_store(0)
        pp, qq = Position(*P), Position(*Q)
        try:
            vp = ct.get_tile_builder_bot_id(pp)
            vq = ct.get_tile_builder_bot_id(qq)
        except Exception:
            return
        if launches >= 3:
            if not self.peel_note:
                self.peel_note = True
                L(ct, "STEP7 sentinel sees store[0]=3 at r%d -> HOLDING FIRE "
                      "(total shots this match so far = %d)" % (r, self.shots))
            return
        if launches < 2:
            return
        if ct.get_action_cooldown() != 0 or ct.get_global_ammo() < 10:
            return
        w6 = ct.get_tile_building_id(Position(20, 6))
        w8 = ct.get_tile_building_id(Position(20, 8))
        # ---- STEP 10: both chambers occupied -> the ray question ----
        if vp is not None and vq is not None and not self.ray_probe_done:
            tiles = ct.get_attackable_tiles()
            cfp, cfq = ct.can_fire(pp), ct.can_fire(qq)
            hp_p0, hp_q0 = ct.get_hp(vp), ct.get_hp(vq)
            hw6, hw8 = ct.get_hp(w6), ct.get_hp(w8)
            L(ct, "STEP10 BOTH chambers occupied (P: victim %d hp=%d | Q: victim %d "
                  "hp=%d). live pattern=%s | can_fire(P)=%s can_fire(Q)=%s -> %s"
              % (vp, hp_p0, vq, hp_q0, [tuple(t) for t in tiles], cfp, cfq,
                 "PASS" if (cfp and cfq) else "FAIL"))
            self.ray_probe_done = True
            if not cfq:
                return
            ct.fire(qq)
            self.shots += 1
            np_ = ct.get_tile_builder_bot_id(pp)
            nq_ = ct.get_tile_builder_bot_id(qq)
            hp_p1 = ct.get_hp(np_) if np_ is not None else None
            hp_q1 = ct.get_hp(nq_) if nq_ is not None else None
            hit_q = (nq_ is None) or (hp_q1 is not None and hp_q1 < hp_q0)
            hit_p = (np_ is None) or (hp_p1 is not None and hp_p1 < hp_p0)
            verdict = ("TARGETED-TILE (the far chamber took it, the near body did not)"
                       if hit_q and not hit_p else
                       "FIRST-BODY-ON-RAY (the near body absorbed a shot aimed past it)"
                       if hit_p and not hit_q else
                       "BOTH-BODIES-HIT" if hit_p and hit_q else "NEITHER-HIT")
            L(ct, "STEP10 fired at Q with P occupied: victim@P hp %s->%s | victim@Q "
                  "hp %s->%s | wall(20,6) %d->%d | wall(20,8) %d->%d -> VERDICT %s"
              % (hp_p0, hp_p1, hp_q0, hp_q1, hw6, ct.get_hp(w6), hw8, ct.get_hp(w8),
                 verdict))
            return
        if not self.ray_probe_done:
            return
        # ---- STEP 6: execution, nearest occupied chamber first ----
        if vp is not None:
            tgt, tname, vid, wall = pp, "P", vp, w6
        elif vq is not None:
            tgt, tname, vid, wall = qq, "Q", vq, w8
        else:
            return
        if self.exec_target != tname:
            self.exec_target = tname
            self.exec_start = (r, self.shots)
        hw0 = ct.get_hp(wall)
        hp0 = ct.get_hp(vid)
        ok = ct.can_fire(tgt)
        if self.exec_start[1] == self.shots:
            L(ct, "STEP6 can_fire(%s)=%s THROUGH the sealed wall (barrier hp=%d) at "
                  "victim %d hp=%d -> %s"
              % (tname, ok, hw0, vid, hp0, "PASS" if ok else "FAIL"))
        if not ok:
            return
        ct.fire(tgt)
        self.shots += 1
        still = ct.get_tile_builder_bot_id(tgt)
        hp1 = ct.get_hp(still) if still is not None else None
        L(ct, "STEP6 shot#%d at %s: victim hp %s->%s (dmg=%s) | wall hp %d->%d | "
              "ammo=%d sentinel_cd_after=%d occupied=%s"
          % (self.shots, tname, hp0, hp1,
             (hp0 - hp1) if hp1 is not None else "RETIRED",
             hw0, ct.get_hp(wall), ct.get_global_ammo(), ct.get_action_cooldown(),
             still is not None))
        if still is None:
            k = self.shots - self.exec_start[1]
            self.kill_log.append((vid, tname, k, r - self.exec_start[0] + 1))
            L(ct, "STEP6 victim %d in %s RETIRED after %d sentinel shots over %d "
                  "rounds; tile_builder_bot_id(%s)=None -> PASS"
              % (vid, tname, k, r - self.exec_start[0] + 1, tname))
            self.exec_target = None
