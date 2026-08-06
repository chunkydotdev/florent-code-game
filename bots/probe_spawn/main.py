"""Probe: settle the Core spawn-range contradiction (r^2=2 vs r^2=8).

docs/game-rules-core says spawn range r^2=2 ("adjacent ring, including
diagonals"); docs/agents-md says an action radius of sqrt(8). The two may even
describe the same 12-tile ring measured from different reference points (the
Core is 2x2 but get_position() returns a single tile), so rather than trust
either, this logs can_spawn() for every tile within dist_sq=20 of the Core's
position at round 0 -- wide enough to contain the spawnable set under any
reading -- then resigns so the match ends immediately.

Run:
    .venv/bin/fcode run probe_spawn probe_spawn maps/mid20.map26 --tle 10 2>&1 | grep SPAWNPROBE
"""

import sys

from fcode import Controller, EntityType


class Player:
    def run(self, ct: Controller) -> None:
        try:
            if ct.get_entity_type() != EntityType.CORE:
                return
            if ct.get_current_round() != 0:
                return
            pos = ct.get_position()
            print(
                f"SPAWNPROBE core_pos=({pos.x},{pos.y}) "
                f"map={ct.get_map_width()}x{ct.get_map_height()} "
                f"ti={ct.get_global_resources()}",
                file=sys.stderr,
            )
            for tile in ct.get_nearby_tiles(dist_sq=20):
                d2 = pos.distance_squared(tile)
                env = ct.get_tile_env(tile)
                bld = ct.get_tile_building_id(tile) is not None
                can = ct.can_spawn(tile)
                print(
                    f"SPAWNPROBE tile=({tile.x},{tile.y}) d2={d2} "
                    f"env={env.name if hasattr(env, 'name') else env} "
                    f"bld={bld} can_spawn={can}",
                    file=sys.stderr,
                )
            ct.resign()
        except Exception:
            import traceback

            traceback.print_exc(file=sys.stderr)
