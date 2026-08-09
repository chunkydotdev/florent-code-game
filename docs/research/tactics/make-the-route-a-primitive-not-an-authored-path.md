---
tactic: (A) Two independent codebases answered "how do you stop misrouted belts" by DELETING hand-routing — you name the endpoints and a pathfinder lays the line
source: https://raw.githubusercontent.com/Anuken/Mindustry/master/core/assets/bundles/bundle.properties
origin: Mindustry (Anuken) — the game our ruleset is mechanically modelled on; and the Factorio Learning Environment (Hopkins, Bakler, Khan, arXiv 2503.09617), an LLM-agent benchmark, https://raw.githubusercontent.com/JackHopkins/factorio-learning-environment/main/fle/env/tools/agent/connect_entities/client.py
evidence: documented
transfers: partial
---

WHAT IT IS — neither codebase tries to *detect* a badly routed belt. Both remove
the ability to author one.

**Mindustry ships it as a game setting**, and the two strings are the whole
feature:

> *"setting.conveyorpathfinding.name = Conveyor Placement Pathfinding"*

> *"hint.conveyorPathfind = Hold [accent][[L-Ctrl][] while dragging conveyors to automatically generate a path."*

**The Factorio Learning Environment removed hand-laying from its agent API
entirely.** Its `connect_entities` tool documents what it takes care of — the
referent of *"the tool"* is the connect-entities tool the page documents, and the
list appears under the line *"For each connection type, the tool handles:"*:

> *"- Resource requirements verification"*

> *"- Connection point validation"*

It carries a feasibility pre-check that builds nothing:

> *"if dry_run:"*

> *"return {"*

> *""number_of_entities_required": total_required_entities,"*

> *""number_of_entities_available": entities_available,"*

and it fails loudly rather than laying a partial line:

> *"exception_message = "Failed to connect entities. Please reposition entities or clear potential blockages""*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **It is the same conclusion the binding-tile cut reached from our own tape**, by
  a completely different route: *"not fewer lines, not more lines, not different
  lines"* — and then, with the source's own emphasis on the adjective, terminated
  ones. Two game codebases and one agent benchmark all decided
  the fix belongs at *authoring* time.
- **Our builder is an agent with a per-tile API, which is exactly the shape FLE
  judged unworkable for an agent.** We call `build_conveyor(pos, direction)` one
  tile at a time and nothing composes those calls into a route. **The transferable
  move is to write our own `connect(harvester_pos, core_pos)` and never call
  `build_conveyor` from anywhere else.** That is a refactor, not a strategy, and it
  is the kind of change that removes a failure class rather than reducing it.
- **The `dry_run` split is the piece worth stealing verbatim in spirit:** the same
  code answers both the feasibility question and the do-it question, so the two answers
  cannot drift apart. Our `can_build_*` / `build_*` pairs already have that
  discipline at the tile level; nothing has it at the route level.

WHAT WOULD KILL IT —

- **Neither source is a competitive league.** Mindustry has no bot tournament;
  FLE is an LLM-agent benchmark. **This file is a design convergence, not evidence
  that anyone won anything with it.** The competitive-league versions of the same
  idea are in
  [`test-build-the-whole-route-before-laying-one-tile`](test-build-the-whole-route-before-laying-one-tile.md)
  and [`an-incomplete-path-must-commit-nothing`](an-incomplete-path-must-commit-nothing.md);
  prefer those as evidence and this as corroboration.
- **Both pathfind in one call. We cannot.** A route here takes one build per
  builder per turn, and the enemy gets to shoot the half-built line. **Nothing in
  either source addresses a route that takes twenty rounds to lay.**
- **FLE's own case shows the primitive is not sufficient.** The paper reports its
  agents still failed on topology (see
  [`agents-check-entities-and-not-topology`](agents-check-entities-and-not-topology.md)),
  *with* `connect_entities` available. A route primitive removes one failure class;
  it does not make an agent competent at logistics.
- **⚠ And FLE's belt code names our exact bug and then declines to enforce it.**
  In `client.py` the two `match relative_pos:` arms at lines 879 and 882 read
  `pass  # raise Exception("Cannot rotate non adjacent belts to face one another")`
  — **the check for belts facing one another is written, commented out, and left as
  a bare `pass`.** So even the codebase that solved authoring did not solve
  head-to-head. That is the third instance of the same pattern in this sweep; see
  [`the-strongest-detector-was-written-and-then-disabled`](the-strongest-detector-was-written-and-then-disabled.md).

BUILDER HOOK — a refactor with a mechanical acceptance test and no strategy
content: **route all conveyor placement through one function that takes a source
and a sink**, and make `build_conveyor` unreachable from anywhere else in the bot.
Acceptance: `grep -c "build_conveyor" main.py` should be 1. Then the terminus
invariant has exactly one place to live, which is the precondition for every other
file in this sweep.
