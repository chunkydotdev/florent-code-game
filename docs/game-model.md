# Game model

Ground truth about how the game works, transcribed from the official docs and tutorials
(scraped copies in [reference/](reference/)). Facts only — hypotheses go in
[strategy-notes.md](strategy-notes.md), things we're trying go in
[strategy-log.md](strategy-log.md).

Source: `game.code.florent.vc/docs/*` and `/tutorials/*`, scraped 2026-08-06. Facts marked
**[measured]** were verified in a local match on that date; everything else is as published.

## Platform

- **Language:** Python 3.12 or 3.13. **3.14 is not supported.** Pure Python only, no native
  extensions (`.so`, `.pyd`, `.dylib`, `.dll` are rejected outright).
- **CLI:** `pip install fcode`, then `fcode login`, `fcode starter`.
- **Entry point:** `main.py` defining a top-level class `Player` with `run(self, ct: Controller)`.
- **Local match:** `fcode run BOT_A BOT_B [MAP] [--seed N] [--tle MS] [--map-random]`
- **Replay:** `fcode watch replay.replay26` (browser visualiser).
- **Remote test:** `fcode match test BOT_A BOT_B [MAPS...]` — real ladder hardware
  (AWS Graviton3), enforces the time limit. Rate limited to 5 per 10 min per account.
- **Submit:** `fcode submit bots/starter`. Unlimited submissions, versioned, one active at a
  time (`fcode submission activate VERSION`).
- **Upload limits:** 5MB archive, 50MB decompressed, 500 files.

## Bot structure

The engine creates **one `Player` instance per unit** and calls its `run()` once per round for
that unit. All units share the same `run()`, so every bot starts by dispatching on
`ct.get_entity_type()`. Instance attributes persist for that unit's entire lifetime.

```python
from fcode import Controller, EntityType

class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            ...
```

Convention throughout the API: `can_X()` / `X()`. The `can_*` checks never raise; the action
methods raise `GameError` when illegal.

## Match structure

- **Grid:** rectangular, **8×8 to 30×30 tiles**. Symmetric. Drawn at random from the
  competition map pool per game. `(0,0)` is the **northwest** corner — x increases east,
  y increases **south**, so NORTH is `(0, -1)`.
- **Rounds:** 1000 max. `ct.get_current_round()` is **0-indexed**.
- **Turn order:** every living unit runs in **spawn order** — the Core always acts first.
  Resource changes made by one unit are **immediately visible** to the next unit that acts
  within the same round. (The comms Store is the exception — see below.)
- **Team A acts before Team B, every round, for every unit — and the mechanism of its
  advantage is now measured [2026-08-08].** Team A's Nth builder is always issued a unit ID
  exactly **one less** than Team B's Nth builder: zero exceptions across 10 instrumented
  matches on two maps (e.g. A = [3, 5, 9, 13, 19], B = [4, 6, 10, 14, 20]). Since units run in
  spawn order, seat A resolves its action first in every round of the match.
  **REFINED [2026-08-07, session-12 death census]:** the order is global ascending unit-ID, so
  the seat-A edge is **pairwise** (each A unit acts before its spawn-twin), NOT "every A action
  before any B action" — B's first builder acts before A's second, and any entity spawned later
  (e.g. a turret the opponent raises mid-match) acts **after** every earlier-spawned unit
  regardless of team. Measured in a fresh 71-death seat-B corpus: 35/71 dying builders had
  already acted in their death round; of the 36 that had not, 30 were on ordinary action
  cooldown (symmetric between seats). Decoder caveat discovered the same pass: within a round,
  a .replay26 update list is **not a strict temporal trace** (a killer's FireTurret event can
  serialize after its victim's RemoveEntity) — correlate per-round, never sequentially.
  **What that buys depends entirely on how much ore is contested.** On `archipelago`, where
  16% of the 38 ore tiles sit near the midline, seat A wins the same-round race for each
  contested tile, and a Harvester **blocks movement** — so the winner walls the loser out and
  immediately retargets deeper ore. Measured over 5 instrumented matches: **62 harvesters for
  A against 27 for B (2.3×)**, including **10 of A's built past the midline on B's side**,
  while B never crossed once. That is the whole ~78% seat-A share on that map, and every
  affected map is decided on economy, never on Core kills.
  The earlier reading — "an advantage on very small maps" (seat A 78% [61%, 89%] on 8×8 with
  `bots/probe_neutral`, 2026-08-06) — was the same effect seen through a proxy: small maps are
  simply maps where everything is contested. **Contested ore, not map size, is the variable.**
  Corroborating: `atoll` has 8 ore tiles with 50% contested and lands in a near-tie decided by
  the harvester tiebreak; `lighthouse` has 0% contested ore and shows no harvester gap at all.
  Implication: seat draw is worth real rating independently of skill, so **how the ladder
  assigns seats within a best-of-five is a first-order question**. Bot-side, the lever is
  contesting the midline earlier rather than accepting the split.
- **Seat assignment [answered 2026-08-08]: fixed for the whole best-of-five, and metadata
  `teamAName` is engine `TEAM_A` in every archived match.** 158 matches / 790 games:
  engine-A win tally equals `scoreA` in 158/158 (p = 1.4e-132 under a per-game seat coin),
  and 583 behaviourally stamped games put us on our metadata seat 583/583 with 0
  mixed-seat matches. Which team is listed A is an unbiased per-match coin flip
  (uncorrelated with rating, name, id, trigger). Therefore a match's five map draws all
  carry one seat: per-map deltas are seat-confounded at match granularity, and per-map
  rows built from few matches can be seat rather than bot.
  (`docs/research/bo5-seat-assignment-2026-08-08.md`; builder spot-check 2026-08-08:
  b5a37d0b/621b841e/4e0874d0 metas consistent with independently-verified seats.)
- **Seed amplification in local batteries [measured 2026-08-07]:** local seeds vary games
  only weakly (byte-identical replays observed across adjacent seeds), so a per-map arena
  row of N games contains far fewer distinct games — a "seat decides this map" row is
  effectively **~2 distinct games, not 2×seeds**. Consequences: Wilson intervals overstate
  confidence; a ±16-game per-map swing between candidates can be ONE knife-edge
  deterministic game amplified (measured: v55 vs `_v70cg` on snowflake — every knob subset
  of the candidate lost the same replicated seat-B game while the control won it, with
  mutually exclusive knob sets, ruling out any mechanism-level cause). Paired same-seed
  comparisons between candidates remain valid; treat per-map deltas on seat-decided maps
  as single-game evidence and weigh the POOLED rate plus mechanism explanations instead.
- **Tiles:** `EMPTY` (traversable), `WALL` (impassable, blocks LOS), `ORE_TITANIUM`
  (traversable, Harvester-buildable).
- **Series:** ladder matches are **best-of-five**. All five games always play to completion.

### Competition map pool — and the symmetry field is wrong [measured]

The live rotation is in `maps/*.map26` (weekly; re-census after every sync — `runbook.md` §2).
Census by parsing the protobuf tile grid, 2026-08-08: **15 maps**, areas **100–676**
(fjordgate 10×10 up to archipelago/snowflake 26×26), wall density **0.6%–30.8%**.

**Every one of the 15 declares `symmetry = 0` (rotational) in its file header, and for 6 of
them that is false.** Comparing tiles directly:

| actual tile-grid symmetry | maps |
| --- | --- |
| 180° rotational | archipelago, atoll, drumlin, fjordgate, hive, jackpot, lighthouse, saga, snowflake |
| mirror across a vertical axis (`x → W-1-x`) | eider, heart, moonrise |
| mirror across a horizontal axis (`y → H-1-y`) | antler, meander, nordkap |

Do not trust the declared field — verify against the tiles. This matters because the two
symmetries impose **different** invariants on bot logic: a rule can be perfectly equivariant
under 180° rotation and still be biased under reflection (rotation maps NE↔SW, reflection maps
NE↔NW), and 6 of 15 maps grade us on the reflection case.

`jackpot` has a Core footprint in the literal map corner — team A at `(0, 0)`, team B at
`(14, 14)` on a 16×16 grid — which is the extreme case for any code that uses the Core's
`get_position()` (the footprint's **NW corner**, not its centre) as a reference point.

### Win condition

Destroy the opponent's Core. Losing your Core ends the match immediately.

If neither Core dies by round 1000, tiebreakers in order:
1. most titanium **collected** — and collected means **delivered to the Core [measured]**;
   see Resource flow below
2. most **harvesters**
3. most titanium **stored**
4. coin flip

### Ladder Elo update [measured 2026-08-07]

**Δ = 32 × (games_won/5 − E)** with **E = 1/(1+10^((R_opp−R_us)/400))**, fit over 100
ladder matches with zero residual (a binary win/loss model fits badly: mean |resid| 3.65).
The platform scores **game share, not match outcome** — each of the 5 games in a match is
worth ±6.4 Elo independently of who takes the match. Consequences: per-game win rate (what
tools/arena.py's Wilson gate measures) is the exact ladder currency; converting any single
lost game pays the same whether it turns 0-5 into 1-4 or 3-2 into 4-1; against a much
stronger team (E < 0.20) stealing one game per match is already net-positive.

### CPU and failure modes

- **10 ms of CPU per unit per round**, plus a banked buffer of up to 5% of that (unused time
  banks, overuse is debited). Monitor with `ct.get_cpu_time_elapsed()` (microseconds).
- **`ct.get_cpu_time_elapsed()` appears inert under the local runner [measured 2026-08-08].**
  It read 0 both before and after a 500,000-iteration Python loop that `time.process_time()`
  measured at ~22 ms — 2.75× the whole budget — and returned zero non-zero deltas across
  ~55,000 sampled builder-rounds, with `--tle 10` passed. **Consequence: our CPU guard cannot
  be validated locally, and neither can a change's CPU cost.** Profile locally with
  `time.process_time()` instead, and treat `fcode match test` on real hardware (AWS Graviton3,
  limit enforced) as the only real verification before submitting anything CPU-heavy.
- Exceeding the limit **interrupts that unit for that round only** — `run()` is called fresh
  next round. Cheap.
- **An uncaught exception permanently removes the unit from the match.** It never acts again.
  This applies to `GameError` and anything else. Not recoverable.
- The local runner does **not** enforce the time limit unless you pass `--tle MS`. The ladder
  always enforces 10 ms.

## Units and buildings

Every entity has a `Team` (A or B) and an `EntityType`. Two overlapping categories:

- **Units** — Core, Builder Bots, turrets. Each runs your code every round and **costs CPU**.
- **Buildings** — everything immovable: Core, turrets, Conveyor, Splitter, Harvester, Barrier.

Core and turrets are both. Builder Bots are the only unit that isn't a building.
Conveyor/Splitter/Harvester/Barrier are the only buildings that aren't units.

**Unit cap: 50 living units per team**, including the Core and turrets. Buildings that aren't
units (harvesters, conveyors, splitters, barriers) don't count and consume no CPU.

### Core

| Property | Value |
| --- | --- |
| HP | 500 (**net 500-512 to kill; raw hits landed range 28 to 1206** — see below) |
| Footprint | 2×2 tiles |
| Vision r² | 36 |
| Spawn tiles | the 12-tile ring around the footprint **[measured]** |

- `ct.get_position()` returns the **NW corner tile** of the 2×2 footprint **[measured]**.
- **Spawnable tiles are exactly the 12-tile ring around the footprint** — every tile
  orthogonally or diagonally adjacent to any footprint tile, nothing else. Verified
  tile-by-tile with `can_spawn()` on 2026-08-06 (`bots/probe_spawn`) **[measured]**. This
  resolves the docs contradiction: r²=2 (rules page) measures from the *nearest footprint
  tile*, sqrt(8) (agents-md) is the distance from the *position corner* to the far ring
  corner. Neither is a radius rule — tiles at d²≤8 from the position that aren't ring tiles
  (e.g. two straight north of the corner) are rejected.
- **Trap:** scanning `pos.add(d)` over the 8 directions (the starter bot) reaches only 5 of
  the 12 legal tiles, and `get_nearby_tiles(dist_sq=2)` (every tutorial) only 6 — all on the
  N/W sides, because position is the NW corner. That is an absolutely oriented spawn set; it
  handed entire maps to one seat until fixed (see strategy-log 2026-08-06). Enumerate
  `get_nearby_tiles(dist_sq=8)` filtered by `can_spawn()` instead.
- **"28 Sentinel hits kills a Core" is only true when nobody heals, and healing dominates it
  utterly [measured 2026-08-08, 14 decoded ladder games].** Net HP to kill is a stable
  **500-512**, but the **raw number of hits landed ranged from 28 to 1206** — a 43× spread —
  because a builder heals **+4 HP for 1 Ti** and can do so every round. Two consequences worth
  keeping: an attacker cannot size a siege from the HP number alone, and **healing is the
  cheapest defensive lever in the game** at 0.25 Ti/HP against ~0.56 for any attacker.
  A siege that is not out-healing the defender is not making progress, however long it runs.
- Stationary. Cannot move or attack. Cannot be rebuilt.
- Its footprint is **never bot-passable, not even to its own team**.
- Abilities: spawn Builder Bots, convert ammo.

### Builder Bot

| Property | Value |
| --- | --- |
| HP | 40 |
| Cost | 30 Ti |
| Vision r² | 20 |
| Action range | orthogonally adjacent tile only — no radius |
| Move / action cooldown | 1 round each |

- The **only** mobile unit.
- **Passable to a builder:** EMPTY, ORE_TITANIUM (even before a Harvester is built),
  Conveyor and Splitter tiles **of either team**.
  **Impassable:** WALL, another Builder Bot, Harvester, Barrier, turret, and Core tiles —
  all of these for **either** team, including your own Core.
- Moves **cardinal only** (N/S/E/W). Diagonals raise `GameError`; `can_move()` returns False
  for them. Diagonals stay valid for turret facing and building orientation.
- Movement puts the unit on a 1-round cooldown.
- **Acting and moving are mutually exclusive per round.** A successful build/attack/heal
  blocks that round's move and vice versa. If `can_move()` is unexpectedly False, check
  `ct.can_act()` to tell "act-locked" apart from "blocked by terrain".
- **Builds only on an orthogonally adjacent tile** — never diagonal, never its own tile.
  `ct.destroy()` follows the same rule.
- `ct.fire(pos)` — orthogonally adjacent only, **damages buildings only**, 2 damage, 2 Ti.
  Not a way to attack enemy units. It's a sabotage tool.
- `ct.heal(pos)` — orthogonally adjacent only, **4 HP for 1 Ti**, heals a building and a
  friendly Builder Bot on the same tile in one call.
- `ct.destroy(pos)` — destroys an **allied** building on an orthogonally adjacent tile.
  Costs **no titanium and no action cooldown**, and is **unlimited per round** — the only
  action in the game that's completely free. It removes that entity's cost-scale
  contribution.
  **CORRECTED 2026-08-08 (s19): destroying a loaded Conveyor does NOT refund the stack —
  it INCINERATES it.** This paragraph previously claimed the resources in transit are
  returned to your balance, and that claim was false. Measured by the research arm:
  `destroy()` on a loaded conveyor credited **0 titanium in 191/191 clean cases**, against
  a positive control that credited 40,427/40,427. The false version made a
  "bucket-mining" exploit look feasible (destroy loaded belts for instant credit); it is
  not. Anything else in the docs or in a bot that cites the refund is wrong by the same
  measurement — grep before trusting.
- `ct.self_destruct()` — deals **zero** damage. Older docs claiming area damage are wrong.
  Only use: freeing unit-cap space or denying a bounty.

### Turrets

Stationary combat buildings, built by Builder Bots. Each runs your code every round (costs CPU
and a unit-cap slot). They fire from the **team-wide ammo balance** — they hold no ammo and
never need feeding by conveyor.

**Turrets do NOT fire on their own — you must call `ct.fire()` from their branch of `run()`.
[measured]** The turrets tutorial claims they "attack automatically once built"; that is wrong.
A full 1000-round match with Gunners built but given no code branch consumed **zero** ammo
while the balance climbed monotonically to 4640. (Caveat: we can't prove an enemy crossed a
firing line, but over 1000 rounds with builders wandering a 16×16 map it's near-certain.)
A turret with no code is a 20–30 Ti ornament that also eats a unit-cap slot and CPU.

| Turret | HP | Cost | Damage | Ammo/shot | Reload | Vision/attack r² | Rotate? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gunner | 25 | 20 Ti | 7 | 4 | 1 round | 13 | Yes (10 Ti, 1-round cooldown) |
| Sentinel | 40 | 30 Ti | 18 | 10 | 2 rounds | 32 | No (fixed at build) |
| Launcher | 30 | 20 Ti | — | — | 1 round | pickup r²=2, throw r²=26 | No facing at all |

- **Gunner** — single-tile-wide forward ray. Stops at the first targetable tile (Builder Bot or
  building), friend or foe. Empty tiles don't block; walls do block and aren't targetable.
  The only turret that can re-aim after being built.

**Tile enumeration is row-major in absolute map coordinates — y ascending, then x ascending —
and it does not depend on the querying entity [measured 2026-08-08].** This holds for both
`get_nearby_tiles()` (verified from a Core at two different corners and from three builders at
varied positions, `dist_sq` irrelevant) and `get_attackable_tiles()` (verified at all 8 turret
facings, 2 samples each). **Consequence, and it is a trap:** a turret loop that takes the
*first* occupied tile out of `get_attackable_tiles()` is scanning its own ray in an absolute
direction, so the near/far preference flips with facing — **N, NE, NW and W turrets engage the
farthest enemy on the line; E, SE, S and SW turrets engage the nearest.** Any "first hit wins"
scan over either method is absolutely oriented and belongs to the same bug class as the spawn
scan (see strategy-log 2026-08-06). Use a geometric criterion — nearest by
`distance_squared` — not enumeration order.
- **Sentinel** — same single-tile-wide line, but much longer reach and **never blocked** by
  walls or units in the way.
- **Launcher pickup ring is the FULL 8-NEIGHBOURHOOD [wild-measured 2026-08-08: 1,471/1,472
  throw events at d²≤2 of the launcher] — any avoidance/exposure logic must test d²≤2, never
  orthogonal adjacency.** (cad-fodder feasibility read.)
- **Launcher** — no damage, no ammo. Picks up an adjacent (incl. diagonal) Builder Bot **from
  either team** and throws it to any bot-passable tile within throw range (measured from the
  Launcher, not the bot).
  - **Used offensively on your OWN builder, this is a rush-delivery tool, and the field is
    already doing it [measured 2026-08-08, ladder replay `81d83bb5`, all 5 games].** Build a
    Launcher next to your own Core on turn 1, throw your own scout builder **6-8 tiles in one
    action**, and it walks the rest — arriving inside the enemy Core's 12-tile spawn ring by
    **turn 6-27 regardless of map size**. This kills the assumption that a large map buys time
    against aggression. The same opponent then parks that single builder in the ring for
    57-98% of the game: **Builder Bots are mutually impassable and cannot attack units**, so
    one enemy body in the spawn ring paralyses a bot with no answer to it, for free.
  - **Two distinct attacker archetypes are converged on at the top of the field** [measured
    2026-08-08, 9 decoded replays across 6 opponents rated 1323-1965]:
    **(a) "instant-Sentinel", turn 1-6** — the thrown builder *builds the forward Sentinel on
    arrival*, so the whole opening is **map-size-independent**. Seen in `sporks` (1923) and all
    five Albert And Einstein games. `sporks` killed a Core in **63 turns**, the fastest
    measured in this project.
    **(b) "forward-Gunner", turn 33-39** — a separate, slower lane, seen in `Pivot` (~1907-1965),
    `not adgato` (1897) and `Besvikomat` (1789): **three unrelated opponents converging tightly
    on the same timing.** Any rush-defense work has to cover both windows, not just the early one.

### Harvester

| Property | Value |
| --- | --- |
| HP | 30 |
| Base cost | 20 Ti |
| Output | 10 Ti every 4 rounds |
| Blocks movement | Yes |
| Blocks LOS | No |

- Built only on `ORE_TITANIUM`, by a Builder Bot standing orthogonally adjacent.
- **Outputs to an adjacent building only** — one of its 4 cardinal neighbours, round-robin by
  least-recently-used. If no neighbour can accept a stack, it goes **idle**: it doesn't waste
  titanium, it just won't produce the next stack until the current one is taken.
- **The round-robin is TEAM-BLIND [constructed experiment, 2026-08-08]:** an ENEMY conveyor
  adjacent to your harvester is a full-rank acceptor. Measured (10×10 probe map, scripted
  bots, per-stack trace): sole-enemy-acceptor → 49/49 stacks banked by the enemy;
  one acceptor per team → strict 50/50 alternation over 800 rounds, zero exceptions.
  Consequences: an unwired harvester beside an enemy belt is a 100% giveaway (the wild
  "adjacency siphon", 4.33% of all our mined stacks in the v75 window); wiring your own
  belt HALVES the drain but never stops it — removing the enemy belt is the only full
  stop. (_v89sh plank; eir8-production-read check 8; margin-decode lighthouse addendum.)
- First output happens **immediately on the round it's built**, not after 4 rounds.
- A Harvester with nowhere to deliver contributes **nothing**. Harvesting and delivery are
  separate problems.

### Conveyor / Splitter / Barrier

| | HP | Cost | Blocks movement | Blocks LOS |
| --- | --- | --- | --- | --- |
| Conveyor | 20 | 3 Ti | No | No |
| Splitter | 20 | 6 Ti | No | No |
| Barrier | 30 | 3 Ti | Yes | Yes |

- **Conveyor** — relays one stack (10 Ti) one tile per round, in a single direction fixed at
  build time. Cardinal facings only. **Accepts from any of its three non-output sides.**
  Holds 1 stack at a time.
- **Splitter** — input from **directly behind only**, output to any of the other **three**
  cardinal sides. Does **not** split a stack: each round it sends its whole stack (10 Ti) to
  whichever of the three outputs was used least recently, rotating through them.
- Conveyors and Splitters are **bot-passable** — you can walk on them (yours or the enemy's).
- **Barrier** — blocks movement and LOS, no facing. Cannot be placed on a wall tile.
  Cheap HP with no other function; use for choke points and funnelling.

### Resource flow

Titanium moves **physically** through the map in stacks of 10, separate from the global
balance you spend from. Harvesters → conveyors/splitters → Core is a purely economic pipeline;
turrets never hold or accept resources.

**Distribution happens once at end of round, after every unit has acted.**

Resources can be pushed onto an **opposing team's** conveyor network or Core — so a badly
aimed chain can feed the enemy, and their network is in principle divertible.

**Crediting is delivery-only [measured 2026-08-06, `bots/probe_credit`]:** the team balance
and the `titanium_collected` tiebreak counter move **only when titanium reaches the Core**.
A harvester with no acceptor produces nothing, and a harvester feeding a dead-end conveyor
chain contributes exactly as much — zero, over 990 measured rounds — while still costing its
20 Ti and +5% permanent scale. Unfinished chains are pure cost. (Also measured:
`can_build_conveyor()` permits a facing whose output points off the map.)

## Economy

- **Titanium is the only resource.** Single shared team balance, `ct.get_global_resources()`.
- **Starting balance: 500 Ti** (`GameConstants.STARTING_TITANIUM`) **[measured]** — a lot.
  That's 16 Builder Bots or 25 Harvesters at base cost, or 200 rounds of passive income,
  available at round 0. The opening is far richer than the income numbers alone suggest.
- **Passive income: 10 Ti every 4 rounds** (2.5/round), granted to the team directly — not
  tied to the Core or anything you build. Over a full 1000-round match that's ~2500 Ti.
- **Ammunition** is a separate team-wide balance, starts at **0**, with **no passive income**.
  The only source is the Core: `ct.convert_ammo(amount)` converts titanium 1:1.
  - At most **one conversion per team per turn**.
  - Usable the **same** turn.
  - Does **not** use the Core's action cooldown — never costs you a spawn.
  - No converting back.
- **Cost scaling:** `effective_cost = floor(scale × base_cost)` **[measured]**. Scale rises
  with **how much your team has built**, not with time — additively per entity, and it
  **decreases again when an entity is destroyed**. It never moves on its own between builds.

  | Entity built | Scale added |
  | --- | --- |
  | Conveyor, Splitter, Barrier | **+1%** each |
  | Harvester | **+5%** each |
  | Launcher | **+10%** each |
  | **Builder Bot**, Gunner, Sentinel | **+20%** each |

  `ct.get_scale_percent()` returns a **percentage** (100.0 at match start, not 1.0
  — the AGENTS.md doc says 1.0, which contradicts the API and the observed value)
  **[measured]**. Every `ct.get_*_cost()` already bakes the scale in — use those getters, and
  `GameConstants`, rather than hardcoding base costs.

## Global Communication Store

16 integer slots (0–15), shared by all your units, private to your team. All start at 0 and
accept any **non-negative** integer. Reading index ≥16 raises.

**Writes are buffered.** A write in round N becomes readable at the start of round N+1 —
not even to the unit that wrote it. This guarantees every unit sees a consistent snapshot for
the whole round regardless of execution order. Design the protocol around the one-round lag.

Note this is the opposite of resource changes, which *are* visible immediately within a round.

## Ladder & rating

- Elo, starting at **1500**, K-factor **32**.
- The outcome fed to Elo is the **fractional series score**, not just win/loss:
  a 3-2 series is 0.6; a 5-0 sweep is 1.0. **Dominant series move rating more than narrow ones.**

```
expected = 1 / (1 + 10^((ratingOpp - ratingUs) / 400))
outcome  = ourGames / (ourGames + theirGames)
delta    = 32 * (outcome - expected)
```

- Only ladder series are rated. `fcode match unrated` and `fcode match test` never affect Elo.
- Scheduler runs **every 10 minutes**; pairing is automatic after submission. First match after
  a new submission can take up to 10 minutes to appear.
- "Climbing" badge: ≥100 matches played and +100 rating within the last 6 hours.

## Controller API

Full method-by-method reference is vendored at
[reference/official-docs.md](reference/official-docs.md) (`docs/robot-api` section). Groups:
Movement · Building & Construction · Combat · Vision & Sensing · Unit Information ·
Communication Store · Resources & Economy · Map & Match · Debugging.

Worth knowing that these exist, since the tutorials never use them:
`get_attackable_tiles()`, `get_attackable_tiles_from()`, `can_fire_from()` (hypothetical
targeting — ignores ammo and cooldown), `is_tile_passable()`, `get_stored_resource()`,
`get_unit_count()`, `build()`/`can_build()` (generic), `rotate()`, `launch()`, `resign()`.

**Tile queries raise on anything outside current vision, not just off the map [measured
2026-08-08].** `get_tile_env()`, `is_tile_passable()` and `get_tile_building_id()` all raise
`GameError: Position out of vision range` for an in-bounds tile the unit cannot currently see —
with the *identical* message as a genuinely off-map position, so the engine does not let you
tell the two apart. `in_bounds()` is necessary but **not sufficient**. Anything that reasons
about ground a unit saw earlier must read a memo the bot maintains itself; re-querying is not
an option. Relatedly, `get_nearby_tiles(dist_sq=N)` **raises** when `N` exceeds the caller's
vision radius (`GameError: dist_sq exceeds vision radius`) — fine for the Core's `dist_sq=8`
against its r²=36, but not a knob to turn up freely.

`Position` and `Direction` are plain Python (`fcode/_types.py`); only the `Controller` is the
compiled engine. **`Position.direction_to()` is `atan2`-based and has no ties [measured
2026-08-08]** — every integer `(dx, dy)` lands strictly inside one of the 8 sectors, and a
400-pair sweep found zero equivariance failures under 180° rotation or either reflection. It
is safe to build symmetric logic on. `Direction` declares clockwise from north:
`NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST, CENTRE`.

**The comms store cannot represent a zero [measured 2026-08-08 — this one costs whole games].**
All 16 slots start at 0 and every value is a non-negative integer, so a slot holding 0 is
indistinguishable from a slot nobody has written. Coordinates therefore **must** be published
with an offset — the starter bot's `pack_pos()` reserves 0 correctly, but its raw
`write_store(SLOT_CORE_X, pos.x)` does not, and a Core at `(0, 0)` (jackpot has one) publishes
a position its own builders read as "no data". See the strategy log for what that costs.

Debug: `print()` is captured per round into the replay; `ct.draw_indicator_dot(pos,r,g,b)` and
`ct.draw_indicator_line(a,b,r,g,b)` draw overlays saved into the replay.

## Reading replays

`.replay26` is protobuf; the full recovered schema and the wire-level traps live in
[`tools/replay_schema.md`](../tools/replay_schema.md), consumed by `tools/replay_census.py`
(both protected — read and run them, never edit). Facts from it that are about **the game**
rather than the file format:

- **Rounds in a replay are 0-based: `turns[i]` IS round `i`.** The visualiser prepends an empty
  turn so its scrubber can show the pre-game state; that offset is a display artefact, not part
  of the file. Verified against `probe_credit`, which logs `ct.get_current_round()` as it acts.
- **Each team's opening Builder Bot is spawned by the bot, not the engine [measured].** A bot
  that never calls `spawn()` (`probe_idle`) emits no `placeEntity` at all and finishes with zero
  units. So **"first builder round" is a bot decision, not a constant** — do not read it as a
  fixed opening when comparing opponents.
- **Cores are never emitted as entity updates.** They exist only in the map header, so a parser
  must seed both at 500 HP before turn 0 or it will miss them entirely — and then `removeEntity`
  on a Core id, which is how a `core_destroyed` match ends, has nothing to remove.
- **One delivered stack is exactly 10 titanium, and delivery-only crediting is now confirmed a
  second way [measured].** `DistributeResources` moves whose destination lands on a Core
  footprint tile, counted over a whole match and multiplied by 10, equal that team's final
  `titaniumCollected` **exactly** — 56 team-sides across 28 replays, zero mismatches. That is
  also the cheapest end-to-end check that a replay parser's geometry is right.
- **Absent means zero:** `titaniumCollected` is simply omitted when a team banked nothing, so a
  team that never completes a delivery chain reads 0 — matching `fcode run --json`.
- `Replay.winCondition` (field 6) is present in real replays but **undeclared** in the
  visualiser's own schema, as is an unidentified `Player` field 6.

- **Determinism, measured end-to-end [2026-08-07, session-12 research fan-out, thread 1]:**
  a rated game is a pure function of (opponent, opp_version, map, our_version, our_seat) —
  mapSeed does NOT vary the game. Three byte-identical replay pairs on record, every decoded
  stream matching round-for-round: Ouroboros/atoll 227t (d0116d59… g5 = 89114461… g5),
  Lunds/hive 194t (b17d5862… g4 = 2b00ef7c… g5), Team48/lighthouse 805t (dcfe2cf0… g3 =
  8ce1c0d9… g2). Across all 1160 rated games: 4.74% strict-key re-pair rate, 48
  identical-fingerprint repeats, 19 of them re-LOST games (~61 Elo at +3.2/coinflip);
  89.6% of repeat groups fully reproducible. Forward EV of decision noise is small (~0.06
  Elo/game) at pool level BUT concentrates on the Ouroboros seat-lock (their-A/our-B every
  match; one atoll group had 4 identical copies). Consequence for LOCAL measurement: this is
  the mechanism behind the seed-amplification trap — seeds don't vary games, so per-map arena
  rows collapse to ~1 distinct game per seat. Bot-side entropy (see decision-noise piece)
  would make local batteries honest again at the cost of exact paired-seed reproducibility.
- **Engine-side nondeterminism, one source found [same thread]:** harvester OUTPUT ROUTING
  breaks ties non-deterministically across games — a fresh harvester with two valid adjacent
  acceptors (one per team) resolved differently in otherwise byte-identical games with zero
  preceding bot-decision divergence, cascading to a 99-round game-length difference
  (Ouroboros/drumlin group, forked r63; 5 of 48 repeat groups affected). Do not assume
  resource-pipeline topology ties are stable.

- **Turret mechanics [measured 2026-08-07, thread-12 replay validation]:** sentinel ray
  pierces (hits through occupied tiles) at dsq<=32, reload 2; gunner is first-blocker at
  dsq<=13, reload 1; same-round convert_ammo -> fire works in production (exercised in
  17/419 observed conversion rounds); zero misaligned shots across the corpus once
  rotation history is applied — the engine's facing model is exactly as documented.
