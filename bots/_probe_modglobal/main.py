"""Sweep 20B probe: is MODULE-LEVEL state shared across a team's units?

`docs/research/predicate-feasibility-2026-08-10.md:438` lists this as open and
"one probe". `_probe_ident` settled that `Player` is one INSTANCE per unit; it
said nothing about the module namespace those instances live in.

Module globals below are touched by every unit. If unit N sees ids written by
units 1..N-1, the module namespace is shared team-wide and a team-level map is
free. Also records the team letter, so cross-TEAM leakage shows up too.
"""
import sys
from fcode import Direction, EntityType

TOUCHED = []          # every unit appends its own id here
BOX = {"n": 0}        # mutable module-level object, id() is masked but stable


class Player:
    def run(self, ct) -> None:
        try:
            uid = ct.get_id()
            r = ct.get_current_round()
            TOUCHED.append((ct.get_team().name, uid))
            BOX["n"] += 1
            if r < 6:
                print(
                    f"MODGLOBAL r={r} team={ct.get_team().name} unit={uid} "
                    f"kind={ct.get_entity_type().name:<11} "
                    f"BOX_n={BOX['n']} TOUCHED={sorted(set(TOUCHED))}",
                    file=sys.stderr,
                )
            if ct.get_entity_type() == EntityType.CORE and ct.get_action_cooldown() == 0:
                p = ct.get_position()
                for d in Direction:
                    if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                        ct.spawn_builder(p.add(d))
                        return
        except Exception as exc:
            print(f"MODGLOBAL ERROR {exc}", file=sys.stderr)
