"""Sitting-duck probe (s57): does NOTHING every turn. Fixture for demos that
need the opponent to survive passively (e.g. showcasing a late-phase siege).
In-game Florent Code League fixture."""


class Player:
    def run(self, ct) -> None:
        return
