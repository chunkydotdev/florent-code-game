# Game model

Ground truth about how the game works, transcribed from the official docs and tutorials
(scraped copies in [reference/](reference/)). Facts only — hypotheses go in
[strategy-notes.md](strategy-notes.md), things we're trying go in
[strategy-log.md](strategy-log.md).

Source: `game.code.florent.vc/docs/*` and `/tutorials/*`, scraped 2026-08-06. Nothing here is
verified against a running match yet — the platform account isn't set up.

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
- **Tiles:** `EMPTY` (traversable), `WALL` (impassable, blocks LOS), `ORE_TITANIUM`
  (traversable, Harvester-buildable).
- **Series:** ladder matches are **best-of-five**. All five games always play to completion.

### Win condition

Destroy the opponent's Core. Losing your Core ends the match immediately.

If neither Core dies by round 1000, tiebreakers in order:
1. most titanium **collected**
2. most **harvesters**
3. most titanium **stored**
4. coin flip

### CPU and failure modes

- **10 ms of CPU per unit per round**, plus a banked buffer of up to 5% of that (unused time
  banks, overuse is debited). Monitor with `ct.get_cpu_time_elapsed()` (microseconds).
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
| HP | 500 |
| Footprint | 2×2 tiles |
| Vision r² | 36 |
| Spawn range r² | 2 (adjacent ring incl. diagonals, not the footprint) |

- Stationary. Cannot move or attack. Cannot be rebuilt.
- Its footprint is **never bot-passable, not even to its own team**.
- Abilities: spawn Builder Bots, convert ammo.

### Builder Bot

- The **only** mobile unit.
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
- `ct.self_destruct()` — deals **zero** damage. Older docs claiming area damage are wrong.
  Only use: freeing unit-cap space or denying a bounty.

### Turrets

Stationary combat buildings, built by Builder Bots. Each runs your code every round (costs CPU
and a unit-cap slot). They fire from the **team-wide ammo balance** — they hold no ammo and
never need feeding by conveyor.

| Turret | HP | Cost | Damage | Ammo/shot | Reload | Vision/attack r² | Rotate? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gunner | 25 | 20 Ti | 7 | 4 | 1 round | 13 | Yes (10 Ti, 1-round cooldown) |
| Sentinel | 40 | 30 Ti | 18 | 10 | 2 rounds | 32 | No (fixed at build) |
| Launcher | 30 | 20 Ti | — | — | 1 round | pickup r²=2, throw r²=26 | No facing at all |

- **Gunner** — single-tile-wide forward ray. Stops at the first targetable tile (Builder Bot or
  building), friend or foe. Empty tiles don't block; walls do block and aren't targetable.
  The only turret that can re-aim after being built.
- **Sentinel** — same single-tile-wide line, but much longer reach and **never blocked** by
  walls or units in the way.
- **Launcher** — no damage, no ammo. Picks up an adjacent (incl. diagonal) Builder Bot **from
  either team** and throws it to any bot-passable tile within throw range (measured from the
  Launcher, not the bot).

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
- First output happens **immediately on the round it's built**, not after 4 rounds.
- A Harvester with nowhere to deliver contributes **nothing**. Harvesting and delivery are
  separate problems.

### Conveyor / Splitter / Barrier

- **Conveyor** — relays one tile per round in a single direction fixed at build time.
  Cardinal facings only.
- **Splitter** — input from directly behind, output to any of the other **three** cardinal
  sides. Does **not** split a stack: each delivery goes whole (10 Ti) to whichever connected
  side was used least recently, so multiple outputs take turns.
- Conveyors and Splitters are **bot-passable** — you can walk on them (yours or the enemy's).
- **Barrier** — blocks movement and LOS, no facing.

## Economy

- **Titanium is the only resource.** Single shared team balance, `ct.get_global_resources()`.
- **Passive income: 10 Ti every 4 rounds** (2.5/round), granted to the team directly — not
  tied to the Core or anything you build. Over a full 1000-round match that's ~2500 Ti.
- **Ammunition** is a separate team-wide balance, starts at **0**, with **no passive income**.
  The only source is the Core: `ct.convert_ammo(amount)` converts titanium 1:1.
  - At most **one conversion per team per turn**.
  - Usable the **same** turn.
  - Does **not** use the Core's action cooldown — never costs you a spawn.
  - No converting back.
- **Cost scaling:** every build cost scales with **how much your team has built**, not with
  time. Starts at 100%, increases **additively** per entity built, and **decreases again when
  something is destroyed**. It never moves on its own between builds.
  - Harvester: **+5%** each
  - Gunner: **+20%** each · Sentinel: **+20%** each
  - `ct.get_scale_percent()` reads it; every `ct.get_*_cost()` already bakes it in.

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

Debug: `print()` is captured per round into the replay; `ct.draw_indicator_dot(pos,r,g,b)` and
`ct.draw_indicator_line(a,b,r,g,b)` draw overlays saved into the replay.
