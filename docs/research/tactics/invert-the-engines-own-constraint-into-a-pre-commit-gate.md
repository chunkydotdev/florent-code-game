---
tactic: (A) The engine SILENTLY TRUNCATES an over-long route and deletes the leg that brings the resource home — two top bots independently defended by inverting the engine's own formula into a pre-launch gate
source: https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/helpers.py
origin: Kaggle "Kore Fleets" (2022) — organisers' engine source; the defence is from qihuazhong's 4th-place bot and the upstream bot it forked
evidence: documented
transfers: partial
---

WHAT IT IS — the only other competitive league in this sweep where a route is
**accepted, mutated, and then silently fails to deliver.** In Kore a fleet is
launched with a flight-plan string whose maximum length depends on the number of
ships. The engine's notion of validity is charset-only:

> *"# this checks the validity of a flight plan"*

> *"def is_valid_flight_plan(flight_plan):"*

> *"return len([c for c in flight_plan if c not in "NESWC0123456789"]) == 0"*

**Nothing checks whether the plan returns to a shipyard.** And an over-long plan is
not rejected — it is cut:

> *"max_flight_plan_len = Fleet.max_flight_plan_len_for_ship_count(shipyard.next_action.num_ships)"*

> *"if len(flight_plan) > max_flight_plan_len:"*

> *"flight_plan = flight_plan[:max_flight_plan_len]"*

**Truncation removes the END of the plan — which is the leg that brings the fleet
home.** The client-side helper only prints:

> *"flight plan will be truncated: flight plan for "*

**The defence, in two independent codebases: invert the engine's own formula and
gate on it before launching.** The 4th-place bot carries both directions of the
constraint side by side —

> *"def max_flight_plan_len_for_ship_count(ship_count: int) -> int:"*

> *"return math.floor(2 * math.log(ship_count)) + 1"*

> *"def min_ship_count_for_flight_plan_len(flight_plan_len: int) -> int:"*

> *"return math.ceil(math.exp((flight_plan_len - 1) / 2))"*

— and `min_fleet_size` becomes a hard filter across the whole bot, canonically
`if num_ships < plan.min_fleet_size(): continue`. **The same two functions appear
in the upstream bot it forked**, i.e. two codebases converged on turning the
engine's silent constraint into an explicit precondition.

**PREMISE CORRECTION, made by leg 3 against my own brief and recorded here so it
does not propagate.** I wrote that an exhausted plan "may never return to a
shipyard". The Kore board wraps, and the organisers' rules say the opposite in the
general case: *"Strategy Tip: Due to the board wrapping, fleets sent out from the
shipyard straight in any direction will return to that shipyard."* **A drifting
fleet is lost only when its straight line misses a shipyard** — wrong column, not
off the map. The loss is real; my mechanism was wrong.

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The failure shape is ours exactly: accepted, no error, resource never arrives.**
  Outside Kore, leg 3 found this shape in no other bot-programming league.
- **The transferable move is a habit, not an algorithm: find the engine constraint
  that silently changes your intent, and encode its inverse as a precondition.**
  Ours is not a length budget — it is **orthogonal adjacency to the core footprint**.
  `can_build_conveyor` will happily approve the last tile of a chain that ends
  diagonally next to the core, and that chain *"delivers nothing, forever, with no
  error"*. **The inverse constraint is trivial to write and nothing in our bot
  writes it.**
- **`get_*_cost()` is the same idea already accepted in our codebase**, so the
  pattern is not foreign: prefer asking the engine what it will do to hardcoding
  what you think it will do.

WHAT WOULD KILL IT —

- **Kore's route is a string; ours is a graph of placed buildings.** A flight plan
  is a compressed command tape validated once at launch. Our conveyors are
  persistent, individually destructible, and modified by two teams over 1000 rounds.
  **The defence Kore's bots use — check once, before commit — is exactly what our
  ruleset makes insufficient**, because our route can become invalid after it was
  valid. That is why this is `partial` and not `yes`.
- **Kore has no repair and no detection, by construction, and leg 3 verified why:**
  only shipyards receive actions and a launched fleet cannot be re-commanded, so
  the bots replace monitoring with deterministic forward simulation. **Kore
  therefore contributes nothing to sub-questions (B) or (C)** and should not be
  cited for them.
- **No published measurement of kore lost to bad plans exists.** Leg 3 ran the real
  engine and produced one — a 20-ship fleet stranded 7,185.3 kore over 399 steps
  where a 21-ship fleet returned — but **that is one seeded board simulated by a
  subagent, not a competitor's result, and it is `inference`.** I did not re-run it.

BUILDER HOOK — write the inverse constraint down as one predicate and put it in the
route function: **`delivers(pos)` is true only if `pos` is orthogonally adjacent to
a friendly core footprint tile.** Then the terminus check in
[`verify-connectivity-after-building-not-only-before`](verify-connectivity-after-building-not-only-before.md)
has a correct base case, which is the part most likely to be got wrong by someone
who has read the CLAUDE.md table and assumed adjacency includes diagonals.
