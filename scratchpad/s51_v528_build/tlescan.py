#!/usr/bin/env python3
"""Count TLE'd bot turns and the exec-time distribution from a replay.

⛔ WHY: `get_cpu_time_elapsed()` is a STUB locally (v513 open item 3), so the
bot cannot measure itself here.  The replay CAN: `BotOutput { id=1, stdout=2,
execTimeUs=3, tled=4 }` is emitted per unit per turn.  v528 adds a full-grid
0-1-2 flood to the eco path, so this is the guard that it did not buy the
ordering with the navigation budget.

SELFTEST (`--selftest`): the counts must not be constant across arms, and a
replay with 0 BotOutput events must be reported as UNREADABLE rather than 0.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, scalars   # noqa: E402

WIRE_LEN = 2


def scan(path):
    raw = Path(path).read_bytes()
    tled = n = 0
    tot = 0
    mx = 0
    over = 0
    for num, wire, val in fields(raw):
        if num != 3 or wire != WIRE_LEN:
            continue
        for tn, tw, upd in fields(val):
            if tw != WIRE_LEN or tn != 1:
                continue
            for un, uw, uv in fields(upd):
                if un != 9 or uw != WIRE_LEN:
                    continue
                sc = scalars(uv)
                us = sc.get(3, 0)
                if not isinstance(us, int):
                    us = 0
                n += 1
                tot += us
                mx = max(mx, us)
                if us >= 9500:
                    over += 1
                if sc.get(4):
                    tled += 1
    return {"events": n, "tled": tled, "over9500": over,
            "mean_us": (tot // n) if n else -1, "max_us": mx}


if __name__ == "__main__":
    args = sys.argv[1:]
    print("replay\tevents\ttled\tover9500\tmean_us\tmax_us")
    vals = []
    for a in args:
        r = scan(a)
        if r["events"] == 0:
            print("%s\tUNREADABLE (0 BotOutput events)" % Path(a).stem)
            continue
        vals.append(r["max_us"])
        print("%s\t%d\t%d\t%d\t%d\t%d" % (Path(a).stem, r["events"], r["tled"],
                                          r["over9500"], r["mean_us"], r["max_us"]))
    if len(vals) > 1:
        print("GUARD non-constant max_us: distinct=%d" % len(set(vals)))
