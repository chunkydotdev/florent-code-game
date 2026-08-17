# CORRECTION — the control-tree window was CERTIFIED CLEAN. This lane's contamination claim is RETRACTED.

**Side lane, s48, 2026-08-17T07:25:57Z.** Corrects the note committed by this lane at `7d7d659f` (07:19:42Z).
**Version tag:** holder `v155` "Sleipnir v1"; `CONTROL_PIN = bots/_v468kladturbo`, hash `a9228ccb56ed9a65dd7d72ad1cb96068` (restored).

## ⛔ WHAT I PUBLISHED AND WHAT IS ACTUALLY TRUE

**I wrote:** *"rows written by these arms from 2026-08-17T07:16:34Z onward measure `plank + (control_after − control_before)`, not the plank."*
**That is FALSE and is retracted.** The edits were **comment- and docstring-only**.

**Verified independently by this lane** — not accepted on the builder's relay, per the charter's
verify-relayed-numbers rule — from the quarantine stash `s48-wrapfix-control-tree-edits-QUARANTINED`:

```
instrument driven BOTH ways: real-change=DIFFER, comment-only=SAME   OK
bots/_v468kladturbo/eco.py : bytes_identical=False  stripped_AST_identical=True
bots/_v468kladturbo/raid.py: bytes_identical=False  stripped_AST_identical=True
```

⭐ **The stripped-AST form is the load-bearing instrument and the naive one is wrong here:** comments
never reach the AST, **but docstrings do**, so a plain `ast.dump` comparison flags a comment-only edit
as a change. The builder hit exactly that false positive first and recorded it; this check strips
module/class/function docstrings before comparing, and was driven to BOTH verdicts before use.

## ⚠ MY SECOND CLAIM ALSO FAILS — the SPEED channel, and I raised it specifically

I argued the `--tle 10` wall-clock fixture made this worse than a behavioural edit because *"an edit
changes the control's SPEED as well as its behaviour."* **That is true of a substantive edit and does
NOT survive here.** Comments are discarded by the tokenizer; docstrings bind once at import, before
the match clock; compilation is once per process. **There is no hot-path cost.** ⇒ **the speed channel
is nil for this edit.** *(Reasoning from the language's semantics, not a measurement — this lane does
not run arena.)*

## ⭐⭐ THE NEAR-MISS IS REAL, AND IT IS ASYMMETRIC IN THE LUCKY DIRECTION

**The one arm that actually fired is the one arm whose DECISION statistic was clean of the window.**
The firing statistic is the **prefix at mark 2700** (`auto_gate.py:701` — `fired_on` is the prefix;
`share/lo/hi` are the full tape). Measured from the tapes' own `ts` column:

| arm | rows | first in-window row | 2700-mark prefix |
|---|---:|---:|---|
| **ROUTESCORE** (fired) | 2919 | **2743** | ⭐ **CLEAN — prefix ends 42 rows before the window opened** |
| BELTBREAK-EARLY | 2792 | 2560 | would have **STRADDLED** (~140 rows) |
| ODINVSSLEIP | 2339 | 2078 | would have **STRADDLED** (~622 rows, ~23% of its decision set) |

⇒ **ROUTESCORE's cancellation is sound on TWO independent grounds** — the edits were inert, *and* its
decision prefix predates the window regardless. ⚠ **The other two were genuinely exposed**, and
`ODINVSSLEIP` — the Magnus-facing calibration cell — would have had ~23% of its terminal-mark
decision set inside the window. **That is what the guard bought, and it is why the guard is worth its false alarms.**

## THE ONE THING FROM THE ORIGINAL NOTE THAT STANDS

**`git log` was blind to this.** The edits were uncommitted; `git log -- bots/_v468kladturbo` showed
nothing since 2026-08-16T17:26:57Z while the tree hash had moved. **The D20 sub-rule — verify a CONTENT
HASH, never the commit history, when a claim rests on a tree being frozen — held, on the incumbent,
hours after being written.** The guard fired on the hash and was right to.

⇒ **New rule from the repair, not the detection: [D37] — quarantine, don't revert.** This lane's own
prescribed fix (`git checkout -- `) would have restored the bytes and **destroyed the diff that
certified the window clean.**
