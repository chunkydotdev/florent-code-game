# replay toolkit

Full-timeline decoder for `.replay26` + a shared, rate-limit-polite fetcher.
Stdlib only. **Always use `/Users/junghard/Projects/Work/florent-code-game/.venv/bin/python`** (system python3 is 3.14 and unsupported).

```
SCRATCH=/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad
$SCRATCH/toolkit/replay_lib.py       # the library (also a CLI: prints summary + self-checks)
$SCRATCH/toolkit/fetch_replay.py     # cached downloader (CLI + importable `fetch()`)
$SCRATCH/replay_cache/replays/       # shared replay cache: <matchId>_g<N>.replay26
$SCRATCH/replay_cache/match_info/    # shared `fcode match info --json` per series
```

Parse cost: ~0.15–0.25 s for a 1000-round replay. Just load them; no need to cache parses.

## 30-second start

```python
import sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad/toolkit")
from fetch_replay import fetch
from replay_lib import load_replay, game_meta, delivered_curve, first_delivery_round, entity_census

mid = "8ed4d332-2968-453e-a23e-bb4c1f83f28e"
meta = game_meta(mid, 4)          # {'mapName','mapSeed','turnsPlayed','winnerSide','winCondition',
                                  #  'our_side':0/1, 'our_side_name':'A', 'opponent', 'we_won', ...}
r = load_replay(fetch(mid, 4))    # downloads only if not already cached
us = meta["our_side"]

print(r.width, r.height, r.n_rounds, r.winner_name, r.win_condition)
print(delivered_curve(r, us)[-1], first_delivery_round(r, us))
print(entity_census(r)["A"]["built"])
```

CLI sanity pass on any file:

```
.venv/bin/python $SCRATCH/toolkit/replay_lib.py <file.replay26> [more...]   # summary + all self-checks
.venv/bin/python $SCRATCH/toolkit/fetch_replay.py <match_id> 1 2 3 4 5      # or --all
```

## Structures

`load_replay(path, *, keep_bot_output=True, keep_indicators=False, keep_cooldowns=False, attribute_damage=True)` → `Replay`.

**Map / outcome:** `r.width`, `r.height`, `r.tiles[y][x]`, `r.walls` (set of `(x,y)`), `r.ore`,
`r.cores` (`[{'id','team','pos'}]`), `r.core_pos(team)`, `r.core_id(team)`, `r.core_footprint(team)` (2x2 set),
`r.env(x,y)` / `r.env_name(x,y)`, `r.n_rounds`, `r.winner` (0/1/None), `r.winner_name`, `r.win_condition`.
`team` anywhere accepts `0/1` or `"A"/"B"` (`norm_team`).

**Entity timeline:** `r.entities` = `{id: Entity}`, every entity that ever existed.

```
Entity(id, kind, team, spawn_round, spawn_pos, max_hp, hp, direction, death_round, pos,
       path=[(round,(x,y))], hp_events=[(round, delta, hp_after)])
  .alive_at(rnd)   spawn_round <= rnd < death_round   (death_round None == survived)
  .pos_at(rnd)     position at end of that round, None if not alive
  .team_name  .direction_name  .is_building  .lifespan(n_rounds)
```
`kind` ∈ `core, builder_bot, harvester, conveyor, splitter, barrier, gunner, sentinel, launcher`.
Queries: `r.entities_of(team=, kind=, alive_at=)`, `r.first_build(team, kind)` → `(round, pos)`,
`r.state_at(rnd)` → `{id: (kind, team, pos, True)}`.

**Events, indexed by round:** `r.rounds[i]` is a `RoundEvents` for round `i` (index IS the round).

| field | records |
| --- | --- |
| `.builds` | `Build(round, id, kind, team, pos, direction, hp, max_hp)` — genuinely new entities only |
| `.entity_updates` | `EntityUpdate(round, id, kind, team, pos, direction, prev_direction, hp)` — `placeEntity` re-emitted for a LIVE id (gunner `rotate()`); see traps |
| `.moves` | `Move(round, id, team, frm, to)` |
| `.deaths` | `Death(round, id, kind, team, pos, age)` |
| `.hp` | `HpEvent(round, target_id, target_kind, target_team, target_pos, delta, hp_after, source_kind, source_id, source_team, source_pos)`; `.damage` / `.heals` filter by sign |
| `.fires` | `Fire(round, frm, to, shooter_id, shooter_kind, shooter_team, ammo_cost)` |
| `.builder_actions` | `BuilderAction(round, kind='attack'\|'heal'\|'build', id, team, frm, target)` |
| `.convert_ammo` | `ConvertAmmo(round, team, amount)` |
| `.resource_moves` | `ResourceMove(round, frm, to, resource_id, to_core_team)` |
| `.bot_output` | `BotOutput(round, id, team, stdout, exec_time_us, tled)` |
| `.indicators` | `Indicator(...)` — only if `keep_indicators=True` |
| `.action_cooldowns` / `.move_cooldowns` | `(id, value)` — only if `keep_cooldowns=True` |

Logs across the whole game: `r.damage_log(team=, dealt=True, target_kind=)`, `r.heal_log(team=)`,
`r.bot_output_log(team=, contains=, tled_only=)`, `r.tle_rounds(team)`, `r.rotations(team=)`.

**Per-team per-round curves** (all length `n_rounds`, index == round):

| call | meaning |
| --- | --- |
| `r.titanium_curve(t)` | global titanium balance — **exact**, from `updatePlayers` (present every round), not a proxy |
| `r.ammo_curve(t)` | global ammo balance |
| `r.ti_collected_curve(t)` | engine's own `titaniumCollected` (the round-1000 tiebreaker stat) |
| `r.delivered_curve(t)` | cumulative Ti delivered into own core (core-footprint deliveries x10) |
| `r.deliveries_curve(t)` | same, in stacks |
| `r.count_curve(t, kind)` | alive count of `kind` at end of each round |
| `r.ammo_spent_curve(t)` | cumulative ammo spent on shots (gunner 4, sentinel 10, launcher 0) |
| `r.damage_dealt_curve(t)` / `r.damage_taken_curve(t)` | **per-round, not cumulative** |
| `r.core_hp_curve(t)` | core HP per round (seeded at 500, 0 after death) |

Helpers: `delivered_curve(r, t)`, `first_delivery_round(r, t)`, `entity_census(r)`
(→ `{'A': {built, lost, alive, first_build, titanium, titanium_collected, ammo, delivered,
first_delivery_round, ammo_spent, damage_dealt, damage_taken, tle_rounds}, 'B': {...}}`),
`load_match_info(match_id)`, `game_meta(match_id, game)`.

Self-checks: `r.check_delivery()`, `r.check_ammo()`, `r.check_all()` → `{name: (ok, detail)}`.

## Traps

1. **`turns[i]` IS round `i`, 0-based.** The visualiser's scrubber prepends a fake turn — that offset is not in the file. `r.rounds[i].round == i`.
2. **Cores are never emitted as `placeEntity`.** They exist only in `map.cores`; seeded here at 500/500 HP at round 0. A Core's `position` is the **NW corner of its 2x2 footprint** — use `core_footprint()`, not `core_pos()`, for any tile test. Damage aimed at a core lands on any of the 4 tiles, so `HpEvent.target_pos` for a core is the NW corner while the shot's `to` may be a different footprint tile (attribution handles this).
3. **`UpdateHp.delta` is a signed `int32`** → negatives arrive as 10-byte varints ≈ `1.8e19`. `signed()` fixes it. `tools/replay_census.py` never parsed this field, so the trap is not in `replay_schema.md`. Half of all HP updates are negative.
4. **proto3 omits defaults, so absent means zero.** `Entity.team` absent == `TEAM_A`; `CoreConvertAmmo.team` absent == `TEAM_A`; `Pos.x`/`Pos.y` absent == 0 (so `(0,0)` is a zero-length message); `titaniumCollected` / `resourcesCollected` / `ammo` absent == 0. Never test "field present" for these.
5. **`placeEntity` doubles as an in-place UPDATE.** A gunner `rotate()` re-emits the whole entity with the **same id, same position, new direction**. Counting those as builds inflates turret counts (measured: 6 vs 2 gunners in one file). This library routes them to `.entity_updates` / `r.rotations()`; roll your own at your peril. Not documented in `replay_schema.md`.
   Rotation is also a **titanium sink worth auditing** (`rotate()` costs 10 Ti + 1 cooldown): in `8ed4d332…` g4 our side made **378 gunner rotations** — 345 of them by a single gunner (#50) — i.e. ~3780 Ti, roughly half of that team's whole titanium income, spent spinning two turrets.
6. **One delivered stack is 10 Ti**, and core-footprint deliveries x10 equals `titaniumCollected` exactly. That is the parser self-check — `r.check_delivery()`.
7. **`mapSeed` is platform metadata, not in the replay.** `.replay26` carries the concrete tile grid but no seed and no map name. Get those from `game_meta(match_id, game)` / `SCRATCH/replay_cache/match_info/<id>.json`. Local `fcode run` seeds are unrelated to ladder `mapSeed`s — never join on a bare integer seed across the two.
8. **`Replay` carries no team names or ids.** Only `Team A`/`Team B`. Which side is OpenSverige comes from match_info — use `game_meta(...)["our_side"]`. Do not assume A is us.
9. **The store (`write_store`) is NOT in the replay.** There is no update kind for it; the 16 comms slots are invisible. The only bot-internal channel is `print()` → `BotOutput.stdout`. Opponent stdout is visible too (usually empty).
10. **Damage attribution is a heuristic**, not a field in the file: `FireTurret` carries `from`/`to` but **no shooter id**, so the shooter is resolved by looking up which building stood on `from` that round, and each `HpEvent` is greedily matched to a same-round `Fire`/`BuilderAttack`/`BuilderHeal` whose target tile equals the target's position. 100% of damage events attributed across all 3 validation replays, and `check_ammo()` reconciles exactly — but treat `source_*` as strong inference, not ground truth.
11. **Friendly fire is real and shows up in the curves.** `damage_dealt_curve(t)` includes damage a team did to itself, so `dealt(A) != taken(B)` in general. Validated case (match `8ed4d332…` game 4, we are side A): our own gunner #50 at (12,12) shot our own builder bot #3 at (11,13) on rounds 62–89, 13 hits, 56 damage, **killing it** at r89. The bot was standing on an enemy conveyor tile — builder bots and buildings can share a tile, and the gunner's line shot took the bot, not the conveyor. Worth checking on every game.
12. **`replay.replay26` in the repo root is volatile** — other agents' local runs overwrite it. Don't cite it as a stable artefact; it changed content mid-session during this build.
13. **Entity ids are not reused** in any file checked (`check_all` asserts it), but builder-bot spawn is a *bot decision* — a team that never spawns emits no `placeEntity` at all.

## Recipes

```python
# delivered curve + when the economy actually started
d = r.delivered_curve("A"); first_delivery_round(r, "A")

# economy shape: harvesters/conveyors alive over time
r.count_curve("A", "harvester"), r.count_curve("A", "conveyor")

# entity census (built / lost / alive / first-build per kind, both teams)
entity_census(r)

# damage log: everything team B dealt to our core
[h for h in r.damage_log(team="B", target_kind="core")]

# who killed what, when
[(d.round, d.kind, d.id, d.pos) for ev in r.rounds for d in ev.deaths if d.team == 0]

# opening: first 20 rounds of builds
[(b.round, b.kind, b.team, b.pos) for ev in r.rounds[:20] for b in ev.builds]

# turret aggression: shots per round, and rotations
sum(len(ev.fires) for ev in r.rounds), len(r.rotations("B"))

# time-to-first-<thing>
r.first_build("B", "sentinel")     # (round, pos) or None

# our own debug prints (and TLEs)
r.bot_output_log(team=us, contains="setup="); r.tle_rounds(us)

# batch over a whole series
for g in range(1, 6):
    m = game_meta(mid, g); rr = load_replay(fetch(mid, g))
    print(g, m["mapName"], m["we_won"], rr.delivered_curve(m["our_side"])[-1])
```

## Validation results

Run: `.venv/bin/python $SCRATCH/toolkit/replay_lib.py <files>`

| replay | delivery x10 == titaniumCollected | ammo converted-spent == final | unknown top/turn/update/entity fields | id reuse | HP in bounds | damage attributed | winner vs dead core |
| --- | --- | --- | --- | --- | --- | --- | --- |
| repo `replay.replay26` (25x15, 257 rounds, B/core_destroyed) | **PASS** A 16x10=160, B 97x10=970 | **PASS** A 194-170=24, B 798-782=16 | PASS (none) | PASS | PASS | 363/363 | PASS |
| `8ed4d332…_g1` (saga, 24x24, 114 rounds, B/core_destroyed) | **PASS** A 23x10=230, B 50x10=500 | **PASS** A 84-80=4, B 647-592=55 | PASS (none) | PASS | PASS | 211/211 | PASS |
| `8ed4d332…_g4` (jackpot, 16x16, 1000 rounds, A/titanium_collected) | **PASS** A 492x10=4920, B 270x10=2700 | **PASS** A 2666-2658=8, B 447-416=31 | PASS (none) | PASS | PASS | 475/475 | PASS |

Cross-checks against independent sources, all exact:

- **vs `tools/replay_census.py`** (the reference decoder) on all 3 files: end-of-game per-type counts for both teams, core deliveries, first-build round+position per kind, winner, win condition, round count — **PASS** on every field. (Before the gunner-rotation fix this cross-check caught a real bug: 6 gunners counted vs 2 actual.)
- **vs platform `match info` metadata** for `8ed4d332…` g1 and g4: parsed `n_rounds` == `turnsPlayed`, `winner_name` == `winnerSide`, `win_condition` == `winCondition` — **PASS** both.
- **Ammo conservation** (`converted − spent == engine's final ammo`) is an *independent* end-to-end check on turret-shooter resolution and per-turret ammo costs; exact on all 6 team-sides.

**Fleet-wide run:** all self-checks were then run over every replay other agents had pulled into the shared cache
(**35 files**, ladder maps 10x10 → 28x20, both win conditions, 74–1000 rounds):
**325 PASS / 0 FAIL**, and **26 650 / 26 650 damage events attributed** with a known source. No unknown top-level
fields, turn fields, update kinds or entity kinds appeared in any of them — `replay_schema.md`'s message tree is
complete as far as the current engine goes (with the two additions in traps 3 and 5 above).

An earlier snapshot of the repo `replay.replay26` (25x25, 1000 rounds, B/titanium_collected) also passed every check before another agent's run overwrote the file.
