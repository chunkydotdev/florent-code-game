import sys
from fcode import Controller, EntityType

VALS = [(1 << 30) | 12345, (1 << 31) | 999, (1 << 40) | 7,
        (1 << 62) | 3, -5, (1 << 63) - 1]


class Player:
    def __init__(self):
        self.i = 0

    def run(self, ct):
        try:
            if ct.get_entity_type() != EntityType.CORE:
                return
            rnd = ct.get_current_round()
            if rnd >= 2 * len(VALS):
                return
            k = rnd // 2
            if rnd % 2 == 0:
                v = VALS[k]
                try:
                    ct.write_store(0, v)
                    print("PROBE write ok", k, v, file=sys.stderr)
                except Exception as e:
                    print("PROBE write FAIL", k, VALS[k], type(e).__name__, e,
                          file=sys.stderr)
            else:
                try:
                    got = ct.read_store(0)
                except Exception as e:
                    print("PROBE read FAIL", k, type(e).__name__, e, file=sys.stderr)
                    return
                print("PROBE read", k, "want", VALS[k], "got", got,
                      "match", got == VALS[k], file=sys.stderr)
        except Exception as e:
            print("PROBE outer", type(e).__name__, e, file=sys.stderr)
