#!/usr/bin/env python3
"""Analysis over scratchpad/dv_tl.ndjson.  Read-only."""
import json, statistics as st
from collections import Counter, defaultdict

POPS = json.load(open('scratchpad/dv_pops.json'))
BY = {p['file']: p for p in POPS}
TL = {}
for line in open('scratchpad/dv_tl.ndjson'):
    r = json.loads(line)
    TL[r['file']] = r

def teams(fn):
    """Return (attacker_team, victim_team) where attacker = diverge / us as appropriate."""
    p = BY[fn]
    if p['pop'] == 'DV_THIRD':
        dv = 0 if p['dv_side'] == 'a' else 1
        return dv, 1 - dv
    us = 0 if p['us_side'] == 'a' else 1
    return us, 1 - us          # caller decides orientation

def q(v):
    v = sorted(v)
    if not v: return None
    n = len(v)
    def pct(p):
        i = min(n - 1, max(0, int(round(p * (n - 1)))))
        return v[i]
    return (pct(0), pct(.25), pct(.5), pct(.75), pct(1.0))

def fmt(v, label='', unit=''):
    x = q(v)
    if x is None: return f'{label}: n=0'
    return (f'{label}: n={len(v)} min={x[0]}{unit} p25={x[1]}{unit} '
            f'MED={x[2]}{unit} p75={x[3]}{unit} max={x[4]}{unit}')
