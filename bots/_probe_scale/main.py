"""ENGINE PROBE — is the cost scale ONE GLOBAL team factor, or PER CATEGORY?

WHY. `CLAUDE.md` (the organisers' doc, which this repo already documents as
carrying known errors) describes cost scaling per category: "conveyors/splitters/
barriers +1% each, harvesters +5% each, launchers +10% each, builder bots/
gunners/sentinels +20% each". The research arm inferred from 5,051 clean
single-build rounds of replay titanium that the truth is ONE GLOBAL ADDITIVE
team factor (99.98% exact match, vs 17.05% for per-category), and that the
organisers' own primary says "increases additively" against "your team's scale
factor" — singular. That is replay-byte inference. This is the engine probe.

THE DISCRIMINATOR. Spawning builder bots touches ONLY the builder/gunner/
sentinel category. Nothing else is built. So:

  * PER CATEGORY  -> get_conveyor_cost(), get_harvester_cost() and
                     get_launcher_cost() must stay FLAT while gunner/sentinel/
                     builder rise.
  * ONE GLOBAL    -> every cost rises together, each as floor(scale * base).

+20% per builder bot makes the signal large enough to see through the floor(),
which is why the probe spawns builders rather than conveyors: one conveyor is
+1%, and floor(1.01 * 3) is still 3, so the cheap entities cannot resolve it.

`get_scale_percent()` returning a SINGLE number is itself evidence for one
factor; the probe prints it so the reading is not resting on that alone.

Output goes to STDERR, which is console-only (print() is captured into the
replay instead). Run:

    .venv/bin/fcode run bots/_probe_scale bots/_probe_victim --tle 0
"""
import sys

from fcode import Controller, Direction, EntityType

BASE = {
    "conveyor": 3, "splitter": 6, "harvester": 20, "barrier": 3,
    "gunner": 20, "sentinel": 30, "launcher": 20, "builder": 30,
}


class Player:
    def run(self, ct: Controller) -> None:
        try:
            if ct.get_entity_type() != EntityType.CORE:
                return                      # builders do NOTHING; only their
                                            # existence is the treatment
            self._core(ct)
        except Exception as exc:            # never let the probe self-destruct
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _core(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        if rnd > 12:
            return

        costs = {
            "conveyor": ct.get_conveyor_cost(),
            "splitter": ct.get_splitter_cost(),
            "harvester": ct.get_harvester_cost(),
            "barrier": ct.get_barrier_cost(),
            "gunner": ct.get_gunner_cost(),
            "sentinel": ct.get_sentinel_cost(),
            "launcher": ct.get_launcher_cost(),
            "builder": ct.get_builder_bot_cost(),
        }
        scale = ct.get_scale_percent()
        units = ct.get_unit_count()

        # Print the observation AND, for each entity, what a single global scale
        # of `scale` would predict. If the two columns agree for entities in
        # categories we never built, the per-category model is dead.
        pred = {k: int((scale / 100.0) * v) for k, v in BASE.items()}
        cols = " ".join(f"{k}={costs[k]}/{pred[k]}" for k in BASE)
        print(f"PROBE r={rnd:<3} units={units} scale%={scale:<8.3f} "
              f"ti={ct.get_global_resources():<5} {cols}", file=sys.stderr)

        # Spawn a builder bot every round we can afford one. ONLY builder bots.
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < costs["builder"]:
            return
        pos = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            tgt = pos.add(d)
            if ct.can_spawn(tgt):
                ct.spawn_builder(tgt)
                return
