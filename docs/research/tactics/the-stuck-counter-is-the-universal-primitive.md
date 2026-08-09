---
tactic: (C) The one detector every league independently converged on — compare state to last tick, increment on identical, RESET ON ANY CHANGE, latch after N
source: https://raw.githubusercontent.com/marmotlab/flatland-challenge-neurips-2020/master/NewAgentInitObs.py
origin: MARMotLab-NUS (Flatland Challenge NeurIPS 2020, Round-1 winner); independently in Screeps — Traveler (https://raw.githubusercontent.com/bonzaiferroni/Traveler/master/Traveler.ts) and Overmind
evidence: documented
transfers: yes
---

WHAT IT IS — four independent implementations across two competitive leagues, all
the same eight lines. The Flatland round-1 winner's version, quoted whole:

> *"if self.time >2 and not self.env.dones[agent] and self.agents_stuck[agent][0] ==0 and agent in self.agents_activated:"*

> *"if self.old_info[agent][0] == my_pos and self.old_info[agent][1] == my_direction:"*

> *"self.agents_stuck[agent][1] +=1"*

> *"else :"*

> *"self.agents_stuck[agent][1] = 0"*

> *"if self.agents_stuck[agent][1] >100 or self.agents_stuck[agent][0] == 1 and not self.env.dones[agent] :"*

> *"self.agents_stuck[agent][0] = 1"*

**Three design decisions in those lines, and all three are deliberate:** the key
is `(position, direction)`, not position alone — an agent that turns in place is
not stuck; the counter **resets to zero on any change**, so it measures a
consecutive run rather than a total; and slot `[0]` is a **sticky latch** while
slot `[1]` is the resettable counter, so a verdict once reached is not re-litigated.

Screeps reached the same shape with a far smaller threshold. Traveler:

> *"private static isStuck(creep: Creep, state: TravelState): boolean {"*

> *"// didn't move"*

> *"const DEFAULT_STUCK_VALUE = 2;"*

and its response is **deliberately randomised**, which is the second transferable
detail:

> *"if (state.stuckCount >= options.stuckValue && Math.random() > .5) {"*

Overmind carries the identical constant with a comment naming the semantics —
`const DEFAULT_STUCK_VALUE = 2;		// Marked as stuck after this many ticks`.

**The counterweight, and it is filed here rather than buried, because it is the
strongest argument against the whole family.** The Flatland winners' ICAPS paper
says local reasoning is not enough:

> *"Deadlocks are essentially impossible to reason about locally."*

> *"The only way to prevent deadlocks is to reason globally about the trains."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **It is the cheapest possible instrument and we have the observable.** The
  conveyor analogue of `(position, direction)` is `get_stored_resource_id(id)` — a
  conveyor holding the same stack id two rounds running has not moved it. **One
  comparison, no map walk, no vision beyond the tile itself.**
- **Threshold 2 versus 100 is the interesting spread, and our ruleset picks a
  side.** Screeps creeps stall for a tick routinely, so 2 is aggressive; Flatland
  trains legitimately wait, so 100 is conservative. **Ours is neither: a carrier
  tile moves at most 1 stack per round with 0 exceptions in 40,363,446 tile-rounds,
  and a corked line never moves again.** So a small threshold — 3 to 5 rounds — is
  defensible here in a way it is not in either source, because there is no
  legitimate long stall in the corked case.
- **The reset-on-change rule is what makes it robust to saturation.** A busy line
  that moves a stack every round resets constantly and never latches. That is
  exactly the discrimination we need, since `DOWNSTREAM_MOVED` (real saturation) is
  0.1% at our median team-side and we must not spend builder-rounds on it.
- **The randomised response transfers for a reason unique to us.** Our unit turn
  order is **global entity-id ascending**, measured with 0 inversions over 1.8M
  ordered pairs — so **every builder reacting to the same signal reacts in the same
  order every round, deterministically.** A deterministic simultaneous reaction is
  how two builders end up laying two conveyors into each other. Traveler's coin
  flip is a cheap desynchroniser and we have a stronger reason for it than Traveler
  does.

WHAT WOULD KILL IT —

- **⚠ It needs cross-round memory and we have almost none.** The counter must
  persist per tile. Sixteen buffered unsigned ints cannot hold a per-tile map, and
  a builder that walks away loses its own history. **This is the binding objection
  and none of the four sources faces it** — they all have unbounded per-agent
  memory. A same-unit, adjacent-tile-only version is possible; a network-wide one
  is not.
- **`get_stored_resource_id` semantics are unprobed.** If stack ids are re-minted
  on each hop, "same id twice" means the opposite of what this file assumes. **Probe
  before building** — see the hook in
  [`detect-the-break-by-predicting-the-effect`](detect-the-break-by-predicting-the-effect.md).
- **And the ICAPS quote above is a direct challenge to the premise.** The winners
  of the league whose whole problem is deadlock say local reasoning cannot prevent
  it. **Their claim is about *prevention*, not detection** — a stuck counter detects
  a deadlock that has already happened, which is a weaker and achievable goal — but
  **anyone proposing a local rule that claims to *prevent* head-to-head conveyors
  should read that sentence first.** See
  [`forbid-the-opposing-claim-and-pay-for-it`](forbid-the-opposing-claim-and-pay-for-it.md)
  for the global alternative and its measured price.

BUILDER HOOK — a builder standing next to a conveyor records `(tile, stack_id)` in
a local dict on its own instance and increments on match. Latch at 3. **Do not try
to share it.** The latched tile becomes that builder's action target. Mechanism
counter: latches raised per game, and share of latched tiles whose forward walk
fails to reach the core — which cross-validates the detector against the terminus
walk for free.
