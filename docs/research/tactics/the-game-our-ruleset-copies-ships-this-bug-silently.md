---
tactic: NEGATIVE / GROUNDING — in Mindustry, the game our ruleset is mechanically modelled on, a conveyor facing nothing is silent by design. The consequences are cosmetic and there is no warning string anywhere in the game
source: https://raw.githubusercontent.com/Anuken/Mindustry/master/core/src/mindustry/world/blocks/distribution/Conveyor.java
origin: Mindustry (Anuken) — engine source and the complete localisation bundle, https://raw.githubusercontent.com/Anuken/Mindustry/master/core/assets/bundles/bundle.properties
evidence: documented
transfers: no
---

WHAT IT IS — our brief describes our failure as *"completely silent: no error, no
signal, the stack simply parks forever"*. **Mindustry is the same, in source.**

A conveyor caches what is in front of it at proximity-update time:

> *"next = front();"*

and its transfer function is a single guarded call that simply returns false
forever when there is nothing there:

> *"public boolean pass(Item item){"*

> *"if(item != null && next != null && next.team == team && next.acceptItem(this, item)){"*

> *"next.handleItem(this, item);"*

> *"return true;"*

> *"}"*

> *"return false;"*

> *"}"*

When items stop moving, a heat value ramps to 1 over 60 ticks:

> *"clogHeat = Mathf.approachDelta(clogHeat, 1f, 1f / 60f);"*

**and its only three consumers in the whole file are cosmetic or incidental**: the
drawn animation frame locks to 0 —

> *"int frame = enabled && clogHeat <= 0.5f ? (int)(((Time.time * speed * 8f * timeScale * efficiency)) % 4) : 0;"*

— the belt stops pushing units standing on it (*"if(!pushUnits || clogHeat > 0.5f || !enabled) return;"*),
and it stops making a sound (*"return clogHeat <= 0.5f;"* in `shouldAmbientSound`).
**No alert, no log, no cost.**

**And the absence is total, not merely undiscovered.** Grepping the game's entire
174,760-byte localisation bundle for `clog`, `not connected`, `no output`,
`nowhere`, `dead end` and `disconnected` returns **three lines**: two are network
connection strings (`disconnect = Disconnected.`, `disconnect.reason = Disconnected: {0}`)
and the third is flavour text on a different block:

> *"block.router.details = A necessary evil. Using next to production inputs is not advised, as they will get clogged by output."*

**There is no warning in Mindustry for a misrouted conveyor because there is no
warning string for one to use.**

WHY THIS IS FILED AS `transfers: no`, and why it is still worth a file:

- **There is no tactic here.** Mindustry has no competitive bot league, no
  postmortems, and no player practice that solves this. Nothing to import.
- **What it establishes is the SHAPE of our problem, from the closest possible
  upstream source.** Our silent failure is not an oversight in our organisers'
  engine — **it is inherited from a genre where it is the norm.** That is a real
  result for sub-question (C): *the reason nobody has a detection tactic is that no
  designer in this family ever provided a detection signal.*
- **And it bounds what a sweep can be expected to find.** My brief said a genuine
  negative here would mean *"our failure mode is structural to our ruleset with no
  external prior art"*. **The negative is half-true and this file is the half that
  holds: the SILENCE is structural and universal.** The other half is refuted —
  competitive leagues with breakable directed networks do exist, they did solve
  parts of it, and their answers are the rest of sweep 19.
- **One design fact does transfer, as contrast rather than tactic.** Factorio, in
  the same genre, ships **17 named alert types** including `train_no_path` and
  `pipeline_overextended` — **topology alerts for rails and for pipes, and none for
  belts.** Two designers, independently, decided a misrouted belt is the player's
  problem while a misrouted train is not. **Whatever the reason, it is not that the
  problem is unrecognised.**

WHAT WOULD KILL IT — nothing; it is a negative established from primary source with
an exhaustive string search. The one thing it does *not* establish: I read the
`Conveyor` block only. **A different Mindustry block, or the campaign UI, might
surface a clog indicator I did not find** — the bundle grep argues against it but
does not prove it, since an indicator could be drawn without a localised string.

BUILDER HOOK — none. This file exists so that no future session spends a sweep
looking for the Mindustry community's solution to our largest failure class.
**There isn't one.**
