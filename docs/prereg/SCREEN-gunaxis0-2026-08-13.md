# SCREEN PREREG — #33: does `LOKI_GUNAXIS_PENALTY` do anything?

**Committed before the shard starts (two-clock: this commit's git author time
vs the shard's first heartbeat).** Builder s37, 2026-08-13.

## The arm

`bots/_v206gunaxis0` = incumbent `_v197mapcode` + `LOKI_GUNAXIS_PENALTY`
8→0 (one constant; the gun-axis station term becomes inert, all other
station scoring untouched). Shipped in v114 on a 92% figure that is stale
for the live tree (64.8% any-gunner); never ablated; the archive cannot
attribute it (v112→v114 contrast is confounded and runs backwards). Queue
row #33's declared resolution governs: **a real avoidance effect moves
gunner-covered forward builder deaths by ≥0.15/game off the 0.60/game
shipped baseline; smaller is inside battery noise.**

## Instrument and bars

Corefill shard `GUNAXIS0` vs `bots/_v197mapcode`, n=5400, standard OB-F
bands, seed base 226000, appended to the worklist now (starts when cores
free — DIGOUT finishes first).

* **CURRENCY (this screen):** game share vs incumbent, read ONLY at the
  shard's own boundaries per the corefill discipline. The ablation nulls
  screen-side if inside the final band 48.66-51.34 — which, for a flag whose
  removal was never tested, is itself the decision: an inside-band ablation
  means the flag is not paying for its complexity and #30/#31a stop being
  gated on it.
* **MECHANISM (deferred, named now so the deferral is a decision, not a
  drift):** gunner-covered forward builder deaths per game needs KEPT
  replays; corefill runs `--replay /dev/null`. A 32-game/arm kept-replay
  batch is the instrument when scheduled; the negative control from the row
  (sentinel-only deaths 0.32/game must NOT move) comes with it. The screen
  does not substitute for this read and this read does not gate the screen.

## Not licensed

No ship implication either direction without the mechanism read; the screen
alone cannot distinguish "flag inert" from "flag helps here, hurts there".
