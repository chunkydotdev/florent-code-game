#!/usr/bin/env python3
"""Aggregate one s48_demo_battery.sh transcript into seat-matched arm-vs-control
cells. Reads the transcript on stdin or from a path argument.

Each cell is (map, seed, seat): the arm's numbers from the treatment run and
the BASE's numbers from the base-vs-base control run on the same map, seed and
seat. That pairing is the point -- base-vs-base measured seat A at 5.6% A->B->A
and seat B at 41.3% on one map with identical code, so an unmatched comparison
reads the seat, not the plank.
"""
import re
import sys

BASE = "_v468kladturbo"


def main():
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    cells, cur, last = {}, None, None
    for line in src:
        m = re.match(r"### (\w+)\s+(\S+) seed=(\d+) \((.*)\)", line)
        if m:
            cur = (m.group(1), m.group(2), m.group(3))
            continue
        m = re.match(r"\s+(\S+) \(seat ([AB])\): harv_built=(\d+) connected=(\d+) "
                     r"\([\d.]+%\) median_connect_latency=(\S+) harv_by_r(\d+)=(\d+)", line)
        if m:
            last = (m.group(1), m.group(2), int(m.group(3)), int(m.group(4)),
                    m.group(5), int(m.group(7)))
            continue
        m = re.match(r"\s+moves=(\d+) A->B->A=(\d+)", line)
        if m and cur and last:
            cells.setdefault((cur[0], cur[1], cur[2], last[1]), {})[last[0]] = (
                int(m.group(1)), int(m.group(2)), last[2], last[3], last[5])
    ctrl, treat = {}, {}
    for (kind, mp, seed, seat), d in cells.items():
        for bot, v in d.items():
            if kind == "control" and bot == BASE:
                ctrl[(mp, seed, seat)] = v
            elif kind == "treat" and bot != BASE:
                treat[(mp, seed, seat)] = v
    tot = [0] * 10
    n = down = 0
    print(f"{'map':10s} {'sd':3s} {'st':2s} | {'osc arm':>8s} {'osc ctl':>8s} | "
          f"{'conn arm':>9s} {'conn ctl':>9s} | {'r25 arm':>7s} {'r25 ctl':>7s}")
    for k in sorted(treat):
        if k not in ctrl:
            continue
        a, b = treat[k], ctrl[k]
        n += 1
        oa = 100 * a[1] / a[0] if a[0] else 0
        ob = 100 * b[1] / b[0] if b[0] else 0
        down += oa < ob
        for i, v in enumerate((a[0], a[1], b[0], b[1], a[2], a[3], b[2], b[3], a[4], b[4])):
            tot[i] += v
        print(f"{k[0]:10s} {k[1]:3s} {k[2]:2s} | {oa:7.1f}% {ob:7.1f}% | "
              f"{a[3]:4d}/{a[2]:<4d} {b[3]:4d}/{b[2]:<4d} | {a[4]:7d} {b[4]:7d}")
    if not n:
        print("no cells parsed")
        return
    print()
    print(f"cells={n}  osc lower in {down}/{n}")
    print(f"POOLED oscillation  arm {100*tot[1]/tot[0]:5.1f}% ({tot[1]}/{tot[0]})   "
          f"ctl {100*tot[3]/tot[2]:5.1f}% ({tot[3]}/{tot[2]})")
    print(f"POOLED connect-rate arm {100*tot[5]/tot[4]:5.1f}% ({tot[5]}/{tot[4]})   "
          f"ctl {100*tot[7]/tot[6]:5.1f}% ({tot[7]}/{tot[6]})")
    print(f"POOLED harvesters by r25  arm {tot[8]}   ctl {tot[9]}")


if __name__ == "__main__":
    main()
