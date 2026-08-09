---
tactic: (A) Dry-run the ENTIRE route before committing a single tile — and log "pathfinding was ok, building failed" as a distinct outcome
source: https://raw.githubusercontent.com/Yexo/AdmiralAI/master/road/routebuilder.nut
origin: AdmiralAI (Yexo), OpenTTD NoAI competitive AI; the API primitive is OpenTTD's own AITestMode (https://docs.openttd.org/ai-api/classAITestMode.html)
evidence: documented
transfers: partial
---

WHAT IT IS — my brief expected sub-question (A) to be **thin or absent**. It is
not. AdmiralAI's road route builder pathfinds, **test-builds the whole path**, and
only then builds it for real. The test-build is the same builder function run
under a scope object:

> *"function RouteBuilder::TestBuildPath(path)"*

> *"local test = AITestMode();"*

> *"return RouteBuilder.BuildPath(path);"*

(`routebuilder.nut` lines 106-110; the whole function body is three lines and is
quoted in full above.)

The commit point, `routebuilder.nut` lines 97-99, gates the real build on the test
build:

> *"if (RouteBuilder.TestBuildPath(path)) {"*

> *"if (RouteBuilder.BuildPath(path, endpoints)) return 0;"*

And when the two disagree, the AI says so in its own log — **pathfinding success
and construction success are treated as different facts**:

> *"AILog.Info("Building a route failed, but pathfinding was ok. Retrying " + num_retries);"*

The engine primitive that makes it free, from the organisers' own API reference —
the referent of *"Test mode"* is the `AITestMode` class the page documents:

> *"In Test mode all the commands you execute aren't really executed. The system only checks if it would be able to execute your requests, and what the cost would be."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The shape is exactly the terminus invariant the binding-tile cut prescribes**,
  arrived at independently by a competitive AI in a different game a decade
  earlier. `DEAD_END_GROUND` at 39.6% is what happens when you skip this step.
- **The distinction AdmiralAI logs is the one our failure hides.** In our engine
  `can_build_conveyor(pos, direction)` answers only whether the tile is legal, and it
  returns `True` for a conveyor pointing at empty ground. **There is no call that
  answers whether the build completes a route.** AdmiralAI's log line names precisely that gap:
  the path was findable, the build still did not produce a working route.
- **We can afford the check because our routes are short.** The binding-tile cut
  measures the median chain at **3 hops** from harvester output tile to binding
  tile, and the binding tile at Chebyshev **5** from our own core. A forward walk
  of a handful of tiles per candidate build is not a 10 ms problem.

WHAT WOULD KILL IT —

- **We have no `AITestMode`.** AdmiralAI gets a free, engine-exact simulation of an
  arbitrary command sequence. Our `can_build_*` predicates are per-tile and do not
  compose: nothing in the `Controller` will tell us whether a *sequence* of builds
  succeeds. **Any transfer must be a hand-written route model, and a hand-written
  model can be wrong in ways `AITestMode` cannot.**
- **A builder bot cannot build a whole route in one turn.** One build per turn,
  orthogonally adjacent only, with an action cooldown, and a bot that acts cannot
  also move that round. So the plan must survive across rounds in a unit whose
  only persistent shared memory is 16 buffered unsigned ints. **AdmiralAI's
  transaction is one function call; ours would be tens of rounds long, during which
  the enemy can shoot the partial line.** That is the real objection to this file
  and it is not answered here.
- **Vision.** `AITestMode` reasons over the whole map. A builder bot's vision is
  r²=20 and the core's is r²=36. **A route longer than one unit's vision cannot be
  validated end-to-end by that unit at all**, which is a hard bound on how far this
  idea reaches and points at the sibling file
  [`verify-connectivity-after-building-not-only-before`](verify-connectivity-after-building-not-only-before.md),
  whose method needs only local adjacency.

BUILDER HOOK — the smallest version, and it deliberately drops the "whole route"
ambition: **before placing a conveyor at `pos` facing `d`, walk forward from
`pos.add(d)` along friendly conveyor/splitter facings for up to K tiles and refuse
the build unless the walk reaches a core footprint tile, a harvester chain already
known good, or the edge of vision.** K = 6 covers the measured median-3-hop case
with headroom. The mechanism counter is the same one the LOKI-10 prereg already
uses: count conveyor builds whose forward walk terminates on empty ground — control
should be large, treatment should be zero. **Do not gate this leg on Elo**; the
binding-tile cut's §8 shows the outcome channel is closed in 93% of v102 games.
