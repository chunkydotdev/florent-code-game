---
tactic: (B) Repair and reroute are the SAME call with one cost constant changed — try hugging the surviving line first, then drop the penalty and let it go around
source: https://raw.githubusercontent.com/openttdcoop/ai-cluelessplus/master/roadbuilder2.nut
origin: CluelessPlus (Zuu), OpenTTD NoAI competitive AI; the escalation ladder is in https://raw.githubusercontent.com/openttdcoop/ai-cluelessplus/master/connection.nut
evidence: documented
transfers: yes
---

WHAT IT IS — the cheapest idea in sweep 19. CluelessPlus has no separate repair
algorithm. "Repair" is its ordinary route pathfinder with the price of new road
raised, so the search prefers to reuse whatever survived:

> *"pathfinder.cost.no_existing_road = repair_existing? 300 : 60; // default = 40"*

`RepairRoadConnection` then runs a two-rung ladder — repair mode with a small
budget, and on failure the *same* builder with the penalty removed and a doubled
budget:

> *"local repair = true;"*

> *"road_builder.Init(front1, front2, repair, 50000);"*

> *"// retry but without higher penalty for constructing new road"*

> *"repair = false;"*

> *"road_builder.Init(front1, front2, repair, 100000);"*

Each rung is run in **both directions**, because one-way connectivity is not
connectivity:

> *"connect_result = road_builder.ConnectTiles() == RoadBuilder.CONNECT_SUCCEEDED; // also make sure the connection works in the reverse direction"*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **Our second-largest actionable class is destroyed segments**, and the
  binding-tile cut says flatly *"We currently do not"* repair them and *"A single
  lost conveyor permanently disables its whole upstream line."* CluelessPlus's
  design says we do not need a repair subsystem — **we need the route function from
  [`make-the-route-a-primitive-not-an-authored-path`](make-the-route-a-primitive-not-an-authored-path.md)
  and one weight.**
- **Our weight already exists in the ruleset and it is not a fiction.** A conveyor
  costs 3 Ti *and* **+1% on the scale factor for every subsequent build of any
  category**, so preferring the surviving line is genuinely cheaper here, not just
  a heuristic. And rebuilding one destroyed tile in the middle of an intact line is
  the cheapest possible repair: one build, 3 Ti, one builder-round.
- **The two-rung structure matters more than the numbers.** It gives a bounded
  fallback: try the cheap local patch, and if the geometry has changed (our own
  turret is now standing on the route — 11.1% of our blocked mass) let the router
  go around instead of failing. **A single-mode repair would loop forever on
  exactly the class we most need to fix.**
- **Bidirectionality has a real analogue.** Ours is not two-way traffic but
  **facing coherence**: a chain can be walkable forward from the harvester and still
  not be pointed at the core, which is what `HEAD_TO_HEAD` (9.94%, field 1.57%) and
  `INTO_HARVESTER` (5.64%) are. **Checking the route from both ends is the cheap
  guard against both.**

WHAT WOULD KILL IT —

- **The constants are asserted, not derived — and this is the honest answer to
  sub-question (B) from the whole OpenTTD ecosystem.** Leg 1 grepped all seven AI
  codebases for measurement vocabulary and reports **no A/B, no cost accounting
  comparing repair against rebuild against reroute, and no recorded rationale for
  any tuned constant** — not the 300-vs-60, not the 50000-then-100000, not
  `MAX_REPATH_TRIES = 5`, not the three-month repair cooldown. **Import the shape;
  do not import a single number.** (The one place anyone *did* measure is Screeps —
  see [`repair-beats-rebuild-and-somebody-did-the-arithmetic`](repair-beats-rebuild-and-somebody-did-the-arithmetic.md)
  — and that measurement is about decay, not combat damage.)
- **We have no pathfinder cost API.** The elegance of CluelessPlus's version is
  that a library pathfinder exposes a tunable weight. Ours would be hand-written,
  so "one constant" becomes "one term in a hand-written scoring function", with all
  the ways that can be wrong.
- **⚠ And this whole plank sits in the INDEX's gated class.** Repairing damaged
  infrastructure cannot be measured in our arena: the standing prerequisite block
  records that the probe family fires 54,264 shots with 99.83% at our core, and
  `razer_probe` needs **26 attack events per building destroyed** against a league
  median near 10. **A repair line will look fantastic against a fixture that cannot
  break anything.** The ladder can see it; the arena cannot.

BUILDER HOOK — the smallest test is not a repair loop, it is a **preference term**:
when a builder must place a conveyor on a route, score candidate tiles with a
penalty for tiles that have never held a carrier, so a broken line is patched
before a parallel one is started. Gate the leg on the mechanism counter — *blocked
harvester-rounds whose binding tile is a destroyed-carrier tile* — not on Elo, and
run it on the ladder rather than the arena for the reason above.
