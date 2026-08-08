#!/usr/bin/env python3
"""Replay turn-differ: compare two .replay26 files turn-by-turn and report the
first BEHAVIORAL divergence, ignoring the updatePlayers records (field 6 of
Update) which carry team store/balances and differ for boring reasons.

Part of the deterministic-paired measurement standard (docs/tooling.md):
identical-replay checks are the gold standard for "this edit didn't change the
games"; the first-divergence turn localizes where behavior actually changed.

Usage:
  .venv/bin/python tools/rdiff.py a.replay26 b.replay26

Promoted from the s15 builder scratchpad (validated 2026-08-08).
"""
import sys


def varint(b, i):
    r = 0
    s = 0
    while True:
        c = b[i]; i += 1
        r |= (c & 0x7F) << s
        if not c & 0x80:
            return r, i
        s += 7


def fields(b):
    i = 0
    n = len(b)
    while i < n:
        key, i = varint(b, i)
        fn, wt = key >> 3, key & 7
        if wt == 0:
            v, i = varint(b, i); yield fn, wt, v
        elif wt == 2:
            ln, i = varint(b, i); yield fn, wt, b[i:i+ln]; i += ln
        elif wt == 5:
            yield fn, wt, b[i:i+4]; i += 4
        elif wt == 1:
            yield fn, wt, b[i:i+8]; i += 8
        else:
            raise ValueError(f"wt {wt}")


def turns(path, drop=(6,)):
    b = open(path, "rb").read()
    out = []
    for fn, wt, v in fields(b):
        if fn == 3 and wt == 2:
            keep = []
            for ufn, uwt, uv in fields(v):
                if ufn != 1:
                    continue
                inner = list(fields(uv))
                if len(inner) == 1 and inner[0][0] in drop:
                    continue
                keep.append(uv)
            out.append(keep)
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: rdiff.py a.replay26 b.replay26")
    a, b = sys.argv[1], sys.argv[2]
    ta, tb = turns(a), turns(b)
    print(f"turns: {len(ta)} vs {len(tb)}")
    n = min(len(ta), len(tb))
    for i in range(n):
        if ta[i] != tb[i]:
            print(f"FIRST BEHAVIORAL DIVERGENCE at turn {i}")
            print("  A updates:", len(ta[i]), " B updates:", len(tb[i]))
            for j in range(max(len(ta[i]), len(tb[i]))):
                x = ta[i][j] if j < len(ta[i]) else None
                y = tb[i][j] if j < len(tb[i]) else None
                if x != y:
                    print(f"   idx {j}: A={x.hex() if x else None}\n            B={y.hex() if y else None}")
                    break
            return
    print("NO behavioral divergence (store/balance records excluded)"
          + ("" if len(ta) == len(tb) else f" up to turn {n}"))


if __name__ == "__main__":
    main()
