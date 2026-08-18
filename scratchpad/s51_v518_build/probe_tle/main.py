"""POSITIVE CONTROL for the timeout column: a bot that deliberately burns far
more than 10 ms in every run() call.  If the engine emits NOTHING for this bot,
then 'timeouts: 0' on a local fixture is a constant column, not a measurement."""
from fcode import Controller


class Player:
    def run(self, ct: Controller) -> None:
        x = 0
        for i in range(4000000):
            x += i * i
        return
