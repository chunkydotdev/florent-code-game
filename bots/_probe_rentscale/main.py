"""ENGINE PROBE — does DESTROYING our own building REMOVE its cost-scale contribution?

WHY. The "rented turret" plank (_v313rentgun) rests entirely on this: build a
turret, kill an enemy harvester with it, then `destroy()` it so we pay the Ti but
NOT the permanent +20% scale tax on every later build. CLAUDE.md asserts
"destruction removes the contribution" and the guard-matrix disassembly
(engine-guard-matrix-exploit-hunt-2026-08-10.md §4) says the same from
`get_scale_percent@0x11fb8`. Neither is an engine OBSERVATION of the removal.
`bots/_probe_scale` proved the ADDITION side only.

THE DISCRIMINATOR. One builder, one gunner (+20% — the largest single step
available, so it cannot hide under floor()).

  scale before build -> S0
  scale after  build -> S1   (expect S0 + 20)
  scale after destroy-> S2   REMOVAL   => S2 == S0
                             NO REMOVAL=> S2 == S1

SECOND QUESTION, also load-bearing for the plank: is `destroy` really free and
cooldown-free, i.e. can the builder destroy AND build in the SAME turn? The
probe destroys and then immediately attempts a barrier build in the same run().

Output to STDERR (console-only under `fcode run`).

    .venv/bin/fcode run bots/_probe_rentscale bots/_probe_victim --tle 0
"""
import sys

from fcode import Controller, Direction, EntityType

CARD = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def run(self, ct: Controller) -> None:
        try:
            k = ct.get_entity_type()
            if k == EntityType.CORE:
                self._core(ct)
            elif k == EntityType.BUILDER_BOT:
                self._bot(ct)
        except Exception as exc:
            import traceback
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    # one builder, once, then silence
    def _core(self, ct: Controller) -> None:
        if getattr(self, "_spawned", False):
            return
        if ct.get_action_cooldown() != 0:
            return
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                self._spawned = True
                return

    def _say(self, ct: Controller, tag: str) -> None:
        print(
            "PROBE r=%-3d %-16s scale%%=%-9.4f gun=%-3d sent=%-3d harv=%-3d conv=%-2d bar=%-2d ti=%d"
            % (
                ct.get_current_round(), tag, ct.get_scale_percent(),
                ct.get_gunner_cost(), ct.get_sentinel_cost(),
                ct.get_harvester_cost(), ct.get_conveyor_cost(),
                ct.get_barrier_cost(), ct.get_global_resources(),
            ),
            file=sys.stderr,
        )

    def _bot(self, ct: Controller) -> None:
        st = getattr(self, "_st", "init")
        rnd = ct.get_current_round()
        pos = ct.get_position()

        if st == "init":
            self._say(ct, "S0 pre-build")
            self._s0 = ct.get_scale_percent()
            if ct.get_action_cooldown() != 0:
                return
            for d in CARD:
                t = pos.add(d)
                if ct.can_build_gunner(t, Direction.NORTH):
                    self._gun = ct.build_gunner(t, Direction.NORTH)
                    self._gunpos = t
                    self._st = "built"
                    print("PROBE built gunner id=%d at %s r=%d"
                          % (self._gun, self._gunpos, rnd), file=sys.stderr)
                    return
            return

        if st == "built":
            self._say(ct, "S1 post-build")
            self._s1 = ct.get_scale_percent()
            self._st = "settle"
            return

        if st == "settle":
            # confirm it held for a round (scale is not transient)
            self._say(ct, "S1b hold")
            self._st = "destroy"
            return

        if st == "destroy":
            gp = self._gunpos
            if not ct.can_destroy(gp):
                print("PROBE !! can_destroy False at %s" % (gp,), file=sys.stderr)
                self._st = "done"
                return
            ct.destroy(gp)
            self._say(ct, "S2 post-destroy")
            self._s2 = ct.get_scale_percent()
            # SECOND QUESTION: destroy was free/cooldown-free -> can we still act?
            acted = "NO"
            if ct.get_action_cooldown() == 0:
                for d in CARD:
                    t = pos.add(d)
                    if ct.can_build_barrier(t):
                        ct.build_barrier(t)
                        acted = "YES(barrier @%s)" % (t,)
                        break
            print("PROBE same-turn-act-after-destroy=%s cd=%d"
                  % (acted, ct.get_action_cooldown()), file=sys.stderr)
            verdict = ("REMOVAL CONFIRMED" if abs(self._s2 - self._s0) < 1e-6
                       else ("NO REMOVAL" if abs(self._s2 - self._s1) < 1e-6
                             else "PARTIAL/OTHER"))
            print("PROBE VERDICT S0=%.4f S1=%.4f S2=%.4f -> %s"
                  % (self._s0, self._s1, self._s2, verdict), file=sys.stderr)
            self._st = "after"
            return

        if st == "after":
            self._say(ct, "S3 next-round")
            self._st = "done"
            return
