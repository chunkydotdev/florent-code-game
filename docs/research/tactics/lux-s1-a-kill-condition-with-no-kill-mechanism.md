---
tactic: THE CONTROL CASE — a league whose rules contain a kill condition and no kill mechanism, so every game runs to the horizon on score
source: https://github.com/Lux-AI-Challenge/Lux-Design-2021 (specs.md and src/logic.ts, local raw fetch)
origin: Lux AI Challenge Season 1 (2021) — organisers' specification and engine source
evidence: documented
transfers: no
---
WHAT IT IS — Lux S1 has an elimination clause in its win conditions, written in
the same breath as its score fallback. From the organisers' spec (the markdown
link syntax is **literal in the raw file**, and is reproduced here rather than
cleaned, because that is what a re-grep must match):

> *"After 360 turns the winner is whichever team has the most [CityTiles](#CityTiles) on the map."*
>
> *"A game may end early if a team no longer has any more [Units](#Units) or [CityTiles](#CityTiles). Then the other team wins."*

The engine agrees. From `src/logic.ts`, the `matchOver` predicate, verbatim
including the comment:

> `// over if at least one team has no units left or city tiles`

and the test it guards:

> `if (game.getTeamsUnits(team).size + cityCount[team] === 0) {`

**And there is no way to make that count reach zero by force.** Machine-counted
over the whole S1 specification, case-insensitively and whitespace-flattened:
`attack` **0**, `damage` **0**, `combat` **0**, `kill` **0**, `health` **0**,
`weapon` **0**, `shoot` **0**, `hp` **0**. The only unit-on-unit interaction in
the ruleset is a collision, and it does *not* destroy anything:

> *"two units attempt to move to the same tile that is not a [CityTile](#CityTiles), this is considered a collision, and the move action is canceled."*

The only offensive verb in the game reduces a road:

> *"Pillage - Reduce the [Road](#Roads) level of the tile the unit is on by 0.5"*

Units and cities die **only** to their own unpaid upkeep:

> *"any city that fails to produce enough light will be consumed by darkness"*
>
> *"During the night, [Units](#Units) and Cities need to produce light to survive."*

So the elimination clause is reachable in principle and unreachable by any action
an opponent can take. **The stated objective is a score, and the spec says so
outright** — *"with the main objective to own as many [CityTiles](#CityTiles) as possible at the end of the turn-based game"*.

WHY IT DOES NOT TRANSFER — Nothing here is buildable. It is filed because it is
the **control case for sweep 17A's structural finding**, and controls are worth
more than tactics when the question is whether a finding is about us or about
game design generally.

17A concluded that *an economically-correct evaluator never finishes* because the
last increment of kill progress carries no economic return. Lux S1 is the limiting
case of that: the return is not merely zero, the **action does not exist**. And
the observed field behaviour is exactly what the theory predicts — the entire S1
meta, including its winner (see
[`they-made-the-resource-renewable-to-weaken-denial`](they-made-the-resource-renewable-to-weaken-denial.md)),
routed its aggression through *resource denial* rather than destruction, because
denial was the only aggression the rules permitted.

**Our position is strictly between Lux S1 and a normal RTS, and that is the useful
part.** We have a real kill mechanism — turrets, 500 core HP — but our tiebreak
keys (*"most titanium collected, then most harvesters, then most titanium stored"*,
`docs/reference/official-docs.md`) pay for economy and nothing pays for damage. So
we have the mechanism and not the incentive. Lux S1 had neither, and its games ran
to the horizon on score **by construction**; ours run to the horizon on score **by
choice of evaluator**. That distinction is the whole of 17A's finding, and this file
is the evidence that the two halves are separable.

WHAT WOULD KILL IT — Nothing; it is a rules fact, verified against both the spec
and the engine source independently. The only way it stops being a useful control
is if the *analogy* is being over-read: Lux S1's field had no choice, so its
convergence on economy is **not** evidence that economy is optimal where a kill is
available. Anyone citing this file as "even Lux converged on economy" is committing
that error. It shows the reverse — that a field with no kill mechanism looks like a
field with no kill *incentive*, which is why 17A's diagnosis is hard to falsify from
outcomes alone.

BUILDER HOOK — none. This file is a boundary marker, not a lever. The one thing it
argues for procedurally: **when a sweep reports "league X also won on economy",
check whether league X could kill at all before treating it as convergent evidence.**
Two of the four Lux sources in this sweep fail that check.
