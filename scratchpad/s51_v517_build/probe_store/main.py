"""STORE-WIDTH PROBE (s51 v517 build).

Question: how wide is a comm-store slot on this engine?  The v517 net-damage
channel wants to pack role(10) + beat1(11) + beat2(4) + hold(4) [+ a net field]
into SLOT_ROLE_N.  29 bits fits any plausible width; anything past 31 does not,
and a silent truncation would corrupt the beat the magazine reads.

Method: on round r the Core writes VALUES[i]; on round r+1 it reads the slot
back and prints WROTE/READ.  Writes are buffered by exactly one round, so the
read on r+1 is the value written on r.  ⛔ POSITIVE CONTROL IN THE SAME TAPE:
the first value is 12345, which MUST come back exactly -- if that row is wrong
the instrument is broken and no truncation row means anything.
"""
import sys

from fcode import Controller, EntityType

VALUES = [
    12345,                 # <- POSITIVE CONTROL
    (1 << 20) - 1,
    (1 << 29) - 1,
    (1 << 30) - 1,
    (1 << 31) - 1,
    1 << 31,
    (1 << 32) - 1,
    (1 << 40) - 1,
    (1 << 53) - 1,
    (1 << 62) - 1,
    (1 << 63) - 1,
    1 << 63,
    -1,
    -(1 << 31),
    -(1 << 63),
]
SLOT = 9


class Player:
    def __init__(self):
        self.i = 0
        self.pending = None

    def run(self, ct: Controller) -> None:
        if ct.get_entity_type() != EntityType.CORE:
            return
        rnd = ct.get_current_round()
        if self.pending is not None:
            try:
                got = ct.read_store(SLOT)
                exc = ""
            except Exception as e:
                got, exc = None, type(e).__name__
            print("STOREPROBE rnd", rnd, "wrote", self.pending,
                  "read", got, "match", 1 if got == self.pending else 0,
                  "exc", exc, file=sys.stderr)
            self.pending = None
        if self.i < len(VALUES) and rnd % 2 == 0:
            v = VALUES[self.i]
            self.i += 1
            try:
                ct.write_store(SLOT, v)
                self.pending = v
            except Exception as e:
                print("STOREPROBE rnd", rnd, "wrote", v,
                      "read", None, "match", 0,
                      "exc", "WRITE:" + type(e).__name__, file=sys.stderr)
