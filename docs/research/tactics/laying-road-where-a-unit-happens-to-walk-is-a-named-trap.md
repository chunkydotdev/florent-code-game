---
tactic: (A/D) Placing infrastructure opportunistically where a unit happens to be is a NAMED community failure mode with a NAMED symptom — a huge network that is never used
source: https://raw.githubusercontent.com/glitchassassin/screeps-wiki/main/app/routes/_base%2B/_wiki%2B/Maturity_Matrix.mdx
origin: Screeps community wiki (renders at https://wiki.screepspl.us/Maturity_Matrix and .../Community_Communication); the live site is a React SPA serving one shell for every URL, so the source .mdx is the only greppable form
evidence: documented
transfers: yes
---

WHAT IT IS — the Screeps community has a name for a bot that lays road wherever
its units walk, and a name for what the result looks like. The trap, quoted whole:

> *"A common / some-what-a-trap solution to placing roads that often leads to what users call 'airports', by virtue of any given creep is walking to a common destination point it is possible to place construction sites as they walk then have creeps build them. While this seems like awesome easy-to-implement idea (and it is to some degree), pathfinding in screeps (unless made by the user elsewise) is non deterministic, so it is quite possible to have multiple paths due to a variety of situations such as creep obstructions or other such issues, that end up with massive road networks that are never used, or as seen from a user's view that look like airport runways."*

And the term itself, from the community-vocabulary page — the referent of *"An
airport"* is a user's room, stated in the sentence:

> *"An airport, is commonly used to refer to a user's room when they build overly sized road networks in their rooms which end up looking like airports/runways. The logic is mainly that 'more roads, less creep parts' without considering the cost/time in repairing the road network."*

The same wiki records the constructive alternative — plan routes to **merge** with
existing ones rather than each be individually shortest. Its referent is a newly
planned road compared against an existing one:

> *"Though the new road, may be shorter, using existing roads may be just as 'fast' for it, and for subsequent goals to use. Saving overall on repair cost."*

Overmind implements exactly that by discounting already-planned tiles in the
routing matrix (`RoadPlanner.ts:26`, `const EXISTING_PATH_COST = PLAIN_COST - 1;`).

WHY IT MIGHT TRANSFER — this is the closest thing in the sweep to a description of
our own measured behaviour, written by someone who had never heard of us:

- **The phrase *massive road networks that are never used* is our number.** We run **116
  conveyors to Viktor5776's 34 and collect less titanium**, and our surviving
  harvesters are **58.8% directed-connected against Viktor5776's 100.0%**. The
  binding-tile cut's headline — *"We lay 17.0pp more road than we point anywhere"* —
  is the airport, measured.
- **The named cause fits our engine too, for a different reason.** Screeps's cause
  is non-deterministic pathing producing many partial routes. Ours would be that a
  builder decides what to build from where it happens to be standing, with an
  orthogonal-adjacency build rule and one action per turn — so **the tile a builder
  can build on is a function of its walk, not of a route.** Different mechanism,
  identical signature.
- **The merge heuristic is directly buildable and cheap here.** Preferring to
  extend an existing chain over starting a new one costs a comparison, and every
  extra conveyor also costs **+1% on the scale factor for every future build of any
  kind**. Our cost model punishes redundant road harder than Screeps's does.

WHAT WOULD KILL IT —

- **This is a community wiki, not a competitor's postmortem.** It is an assertion
  about what "users call" something; **there is no measurement anywhere on that page
  that airports lose games.** Evidence class is `documented` because the text exists
  and says what it says — not because anyone proved the claim.
- **The analogy is behavioural, not mechanical.** Screeps roads are an
  optimisation (they halve MOVE parts); our conveyors are the *only* way titanium
  moves. **Over-building road in Screeps wastes upkeep; over-building conveyor here
  can actively cork the network.** So the transfer is one-directional: their warning
  applies to us and probably understates our cost. **Do not import their remedy's
  sizing.**
- **Our own diagnosis may be wrong about the cause.** The binding-tile cut can show
  that our lines do not terminate; it cannot show *why* our builder placed them.
  **"We are an airport" is my reading of the correspondence, not a measured claim
  about our code**, and it should be checked against the bot before it is acted on.

BUILDER HOOK — one comparison, no new state: **when a builder is about to place a
conveyor, prefer a tile that extends a chain already known to reach the core over a
tile that starts a new one**, and if neither is available prefer *not building* over
starting a stub. Mechanism counter: conveyors built per harvester delivered-to-core,
ours vs the field — we should be moving toward Viktor5776's 34, not away.
