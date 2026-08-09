---
tactic: Funnel, don't seal — shape the approach instead of covering it (Terminal's maze doctrine)
source: https://forum.c1games.com/t/regarding-maze-algos/472 (via Wayback); https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/game_state.py
origin: Terminal (Correlation One / Citadel) — 2018 forum meta and 2026 competition entries; the placement rule is from Correlation One's own starter kit
evidence: documented
transfers: partial
---

WHAT IT IS — two results from **Terminal**, the closest structural analogue to
our game that exists: immobile structures placed on a grid, where the entire meta
is placement.

**First, the negative — and it is the cleanest answer this sweep found to half
the question.** In Terminal **you cannot plant anything in enemy territory at
all.** Correlation One's own starter kit enforces it:

```python
correct_territory = location[1] < self.HALF_ARENA
...
    fail_reason = fail_reason + " Location in enemy territory."
```

and the `can_spawn` docstring states it as a rule (the typo "To units," is in the
original):

> "To units, we need to be able to afford them, and the location must be
> in bounds, unblocked, on our side of the map, not on top of a unit we can't
> stack with, and on an edge if the unit is mobile."

The same half-map gate applies to **removal and upgrade**, not only placement.
**So the entire offensive half of this sweep's question does not exist in
Terminal** — everything Terminal has to teach is about defence.

*(Provenance caveat, stated rather than hidden: the official rules page
`terminal.c1games.com/rules` is unretrievable — it 302s live and in every Wayback
capture — so the strongest primary available is C1's own code, not rules prose,
and engine-side enforcement is inferred from the client helper.)*

**Second, the positive.** Terminal's defensive doctrine is not walling, it is
**shaping**. Destrolas, 2018, the canonical statement:

> "In Terminal you can't control directly unit pathing. However, building a maze
> (or any wall with a small gap in it) lets you control both your own and your
> enemy's units' pathing. Combined with the fact that emps outrange destructors,
> with enough pathing control you can get an enormous amount of "free" damage. So
> using full-length walls with small gaps basically gives you an extra entire
> dimension of control."

And the discipline that makes it work — kkroep, on blocking paths:

> "I actually never block of the entire path for the opponent, as I find it much
> more easy to control where the opposing units go if you leave the options open."

**Sealing is the mistake; the deliberate gap is the tool.** Competition entries
eight years later state the same geometry — srj-42's India 2026 entry: "Defense
is built around a **funnel geometry**: angled wall arms channel all enemy units
into a central kill zone packed with turrets."

And the ranking, kkroep again, on beating a maze:

> "Successfully setting up a structure like that is a win condition: once it is up
> you win almost guaranteed. Easier to prevent the maze from going up than to
> combat a full maze."

WHY IT MIGHT TRANSFER — two reasons, one general and one specific to our turret
problem:

1. **"Easier to prevent than to combat" is now a third independent league**
   reaching the ranking in [[sustained-plant-removal-race]]. Battlecode 2020's
   cookie, Screeps' damage-vs-heal check, Terminal's maze: all three say the
   entrenched structure is answered before it exists, never after.
2. **It reframes what our barriers are for.** Our instinct — from
   [[spawn-smothering]] and from the refuted tile table — is to *cover* tiles.
   Terminal's field says covering is the expensive brittle version and shaping is
   the cheap one: leave a gap, and put the gap where your turrets already point.
   **That is precisely the fix for the s23 corollary that gunners and sentinels
   want opposite geometry.** A gunner's line is blocked by our own buildings, so
   it needs a clear lane; a funnel manufactures exactly one clear lane and denies
   every other approach. The barrier spend stops being cover and starts being
   aiming.

WHAT WOULD KILL IT — and the first is load-bearing enough that nothing should be
built before it is checked:

1. **Terminal's mobile units path automatically. Ours are opponent code.** A
   funnel only funnels if the enemy builder's navigation is naive enough to be
   steered. This is not a field-wide property — it is a per-opponent one, which
   makes it a *play-the-players* question rather than a doctrine question.
2. **Terminal punishes total walls with a rule we do not have.** A Terminal
   mobile unit whose path is fully blocked self-destructs onto your structures.
   That rule is *why* "leave a gap" is correct there. **We have no such rule**, so
   the discipline may be an artefact of their ruleset rather than a general truth.
   Do not import it blind. *(Distinct mechanic note: Terminal's `self_destruct`
   is a mobile-unit rule about blocked pathing and has nothing to do with its
   structure remove/refund.)*
3. **A barrier funnel funnels us too.** Our builders may co-occupy only a
   conveyor, splitter, or the allied core, and 97.2% of the tiles the enemy plants
   on are tiles we build on.
4. **Terminal mazes are reshapeable every turn and ours are permanent.** Official
   `game-configs.json` gives every structure `"refundPercentage": 0.75,
   "turnsRequiredToRemove": 1` — they can dissolve and re-lay the maze each turn.
   We have no refund. A funnel we get wrong is a funnel we live with for 1000
   rounds.

BUILDER HOOK — **the measurement first, because kill condition 1 decides
everything else:**

> Take the three opponents that hurt us most at home (Ouroboros, Lunds Stallions,
> Powerpuff Girls) and ask whether their raiders' approach tiles **shift when our
> building layout shifts**. If their approach is invariant to our layout, they are
> not routing around us and no funnel will ever work. If it moves, the funnel is
> worth pricing.

That is a corpus question, not a battery, and it doubles as an opponent-model
probe of exactly the kind the play-the-players mandate asks for. It is also the
only idea in this sweep that would convert our *existing* barrier spend from
cover into aim.

Related: [[gunner-line-blinding]] · [[sustained-plant-removal-race]] ·
[[runtime-density-siting]] · [[spawn-smothering]]
