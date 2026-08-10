# LEG RECORD — OVERNIGHT BLEED-BAND COLLECTOR (s28)

`tools/night_collector.sh`. **NON-ACTIVATING**: v104 is the live incumbent and
stays live; the script contains **zero** `submission activate` calls (verified by
grep, count = 0). Therefore **it cannot leak a prototype onto the rated ladder
and there is nothing to roll back** — which is the property that makes it the
only arm safe to run for six hours with nobody watching.

## What it is for

**Ranks ~25-40 cost us −438.6 Elo across 58% of our match diet, and that number
has NO MECHANISM ATTACHED.** Nobody knows why we lose there. Six unattended
hours against the band produces per-opponent kill-speed score, what kills us and
in what round band, on which maps — **the input a morning plank needs, gathered
while nobody is awake to spend it.**

It also answers "should we kill earlier?" with data: **if median kill round
varies sharply by opponent, earliness is a matchup property, not a bot
property** — and that changes what the plank should target.

## Cells (9), us−110..us+15, from the freshest league tape

kladde +3 · farming_200s −1 · Lunds Stallions −28 · Landers −32 · I Stone −53 ·
gsxWins −70 · CtrlAltDefeat −72 · Team 48 −84 · Powerpuff Girls −96

## Holder-assert guard — MUTATION-TESTED ON THIS FILE

Third copy of the s27 D28 guard, and per the standing rule it carries its own
test rather than a sibling's citation:

```
$ INCUMBENT=999 OUT=/tmp/night_mut.txt zsh tools/night_collector.sh 1
exit=1
20:21:00Z NIGHT: ABORT -- expected v999, holder is 'v104 (Loki v2)'. Firing nothing.
/tmp/night_mut.txt: No such file or directory     <-- zero challenges fired
```

Exit code captured **without a pipe**. `corpus/FANOUT_ABORT` was written and then
deleted so a live monitor cannot read a test as a real alert; this record is its
trace.

**Why the guard matters more here than anywhere else:** for an attended arm a
broken assert costs one noticed abort. **For a six-hour unattended arm it is the
only thing between a version mix-up and a night of contaminated data nobody sees
until 06:00.**

## Pacing

Budget-driven off `tools/rate_budget.py`, not a fixed sleep — a flat sleep left
~40% of the rolling allowance idle when measured. **At ~15 challenges/hour over
six hours that is ~90 challenges / 450 games**, against the ~25 a session
typically banks.

## ⚠ FOR WHOEVER STARTS THE MORNING

**Stop this collector and wait out ONE FULL 20-MINUTE WINDOW before firing any
leg.** Rejected attempts count against the limit, so a leg started immediately
after it eats rejections and pays a pointless prototype activation per spin.
`.venv/bin/python tools/rate_budget.py` must read `a slot is free NOW` **after**
the collector is stopped, not before.
