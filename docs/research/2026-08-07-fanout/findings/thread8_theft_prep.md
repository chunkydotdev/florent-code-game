# Thread 8 — Top-8 single-game theft prep

Scout pass, 2026-08-07. Read-only. Targets: The Flotte Experience (1889, id `78b72cb2-…`),
Pivot (1985, id `20064efa-c6a9-4c46-acb7-3f7ea9f9b1c9`), team lazy (1900, id `648d1d5b-…`).
We are OpenSverige, ~1557.

## Headline

**The single most stealable pair is `The Flotte Experience` × `jackpot`.**
Flotte are **7W–31L (82% loss) on jackpot** over 38 games against 12 different opponents, and
**9 of those 31 losses are r1000 `titanium_collected` tiebreaks** — the largest count of
economy-tiebreak steals of any (target, map) pair in the entire dataset. That is our line's
mechanism, not a rush. Runner-ups: Flotte × moonrise (7 tiebreak steals) and Flotte ×
lighthouse (82% loss but core-kill flavoured).

Elo arithmetic that motivates this (game-share, Δ = 32×(games/5 − E)), at our 1557:

| target | E | 0–5 | 1–4 | swing per stolen game |
|---|---|---|---|---|
| Flotte 1889 | 0.1225 | −3.92 | **+2.48** | **+6.40** |
| Pivot 1985 | 0.0760 | −2.43 | **+3.97** | **+6.40** |
| team lazy 1900 | 0.1282 | −4.10 | **+2.30** | **+6.40** |

## Method / evidence base

- Source lists: `CACHE/team_flotte.json`, `team_pivot.json`, `team_lazy.json` — 100 most recent
  ladder matches each (window 2026-08-06T17:44 → 2026-08-07T10:13).
- **Drop-matches** (target conceded ≥1 game, i.e. score ≠ 5–0): Flotte 93/100, Pivot 85/100,
  team lazy 94/100. 247 unique match ids; **all 247 match-infos fetched, 0 failures**, cached
  under `CACHE/match_info/<id>.json`. 1360 games with map / winCondition / turnsPlayed.
- Because ≥93% of each target's matches are drop-matches, the per-map tables below are
  effectively their full recent record; the 5–0 conditioning bias is negligible.
- Per-map tables restricted to the **live 15-map pool** (antler, archipelago, atoll, drumlin,
  eider, fjordgate, heart, hive, jackpot, lighthouse, meander, moonrise, nordkap, saga,
  snowflake). `pinch`, on which we once beat Flotte, is retired — see caveat below.
- Working scripts + raw table dumps: `scratchpad/thread8/` (`analyze.py`, `maptable.py`,
  `offense.py`, `steals.py`, `rank.py`, `out_*.txt`, `games.json`).

### The "150+ points below" criterion cannot be met — and why that is fine

The matchmaker pairs these teams almost exclusively with 1700–2000 opponents. Across all 300
recent matches the largest rating gap in which a target dropped a game is **+221** (Pivot vs
Jython 1785, `9c37c0d8-0b4e-4e39-beff-d9ef5e7402d2`); for Flotte the max is **+142** (O(1)
1710, `51cc65d0-57be-418c-b639-07527dc544af`). There is simply no 1550-rated team in their
recent history to prove "a team our size can do it". The usable substitute is **mechanism
plus stealer weakness**: the best-evidenced steals come from static, low-iteration bots
(`O(1)` frozen at v7, `Besvikomat` at v16, `sporks` at v1, `Powered by SmartFridge` v28–34),
which is much stronger evidence that the hole is structural rather than skill-gated.

## Per-target drop tables (live pool only)

Format: W–L is the target's record; "r1000" is games that ran the full distance.

### The Flotte Experience — 233W–232L on pool maps

| map | W | L | loss% | median LOSS turn | loss winConditions | r1000 games |
|---|---|---|---|---|---|---|
| **jackpot** | 7 | **31** | **82%** | 440 | core_destroyed 22, **titanium_collected 9** | 9 |
| **lighthouse** | 6 | **28** | **82%** | 218 | core_destroyed 27, titanium_collected 1 | 3 |
| **moonrise** | 9 | 17 | 65% | 550 | core_destroyed 10, **titanium_collected 7** | 9 |
| drumlin | 14 | 21 | 60% | 373 | core_destroyed 20, titanium_collected 1 | 3 |
| fjordgate | 10 | 15 | 60% | 367 | core_destroyed 11, titanium_collected 3, titanium_stored 1 | 6 |
| eider | 16 | 21 | 57% | 244 | core_destroyed 21 | 1 |
| atoll | 12 | 14 | 54% | 306 | core_destroyed 13, titanium_collected 1 | 2 |
| saga | 15 | 14 | 48% | 414 | core_destroyed 10, titanium_collected 4 | 5 |
| archipelago | 16 | 13 | 45% | 381 | core_destroyed 12, titanium_collected 1 | 1 |
| snowflake | 17 | 12 | 41% | 222 | core_destroyed 12 | 0 |
| meander | 24 | 12 | 33% | 274 | core_destroyed 11, titanium_collected 1 | 7 |
| nordkap | 17 | 8 | 32% | 433 | core_destroyed 8 | 0 |
| antler | 19 | 8 | 30% | 248 | core_destroyed 7, titanium_collected 1 | 6 |
| hive | 24 | 9 | 27% | 220 | core_destroyed 8, titanium_collected 1 | 2 |
| heart | 27 | 9 | 25% | 287 | core_destroyed 7, titanium_collected 2 | 6 |

Flotte reach r1000 in 60/465 games (13%) and are **27W–33L once there** — they are a
below-even tiebreak team. They win by core kill ≤r200 in 28% of games.

### Pivot — 234W–212L on pool maps

| map | W | L | loss% | median LOSS turn | loss winConditions | r1000 |
|---|---|---|---|---|---|---|
| **fjordgate** | 5 | **25** | **83%** | **117** | core_destroyed 25 | 1 |
| **heart** | 8 | 22 | 73% | 221 | core_destroyed 20, titanium_collected 2 | 2 |
| meander | 10 | 15 | 60% | 275 | core_destroyed 15 | 1 |
| moonrise | 14 | 18 | 56% | 200 | core_destroyed 17, titanium_collected 1 | 3 |
| archipelago | 11 | 13 | 54% | 324 | core_destroyed 13 | 2 |
| lighthouse | 12 | 12 | 50% | 208 | core_destroyed 12 | 0 |
| atoll | 14 | 13 | 48% | 245 | core_destroyed 11, titanium_collected 2 | 3 |
| snowflake | 19 | 13 | 41% | 238 | core_destroyed 12, titanium_collected 1 | 2 |
| saga | 18 | 12 | 40% | 238 | core_destroyed 10, titanium_collected 2 | 5 |
| drumlin | 22 | 13 | 37% | 168 | core_destroyed 12, titanium_collected 1 | 2 |
| antler | 18 | 8 | 31% | 206 | core_destroyed 8 | 1 |
| hive | 19 | 8 | 30% | 178 | core_destroyed 8 | 0 |
| jackpot | 15 | 6 | 29% | 242 | core_destroyed 5, titanium_collected 1 | 7 |
| eider | 20 | 7 | 26% | 229 | core_destroyed 6, titanium_collected 1 | 3 |
| nordkap | 29 | 6 | 17% | 251 | core_destroyed 5, titanium_collected 1 | 1 |

Pivot's holes are **rush holes**: fjordgate median loss turn 117, and their weakest-opponent
drops are all fast core kills (`76c1debb-1b2a-4ffc-8665-15ad469bd2b5` g2 antler r49 and g4
fjordgate r74 to Powered by SmartFridge at 1790, gap +217). They are 21W–12L at r1000 — the
best tiebreak team of the three. **Not our mechanism.**

### team lazy — 239W–231L on pool maps

| map | W | L | loss% | median LOSS turn | loss winConditions | r1000 |
|---|---|---|---|---|---|---|
| **saga** | 8 | **25** | **76%** | 281 | core_destroyed 24, titanium_collected 1 | 1 |
| **moonrise** | 12 | **29** | **71%** | 310 | core_destroyed 27, titanium_collected 2 | 4 |
| nordkap | 12 | 16 | 57% | 309 | core_destroyed 14, titanium_collected 2 | 4 |
| drumlin | 15 | 19 | 56% | 267 | core_destroyed 17, titanium_collected 2 | 3 |
| jackpot | 13 | 16 | 55% | 280 | core_destroyed 14, titanium_collected 2 | 3 |
| heart | 13 | 13 | 50% | 290 | core_destroyed 11, titanium_collected 2 | 6 |
| snowflake | 19 | 18 | 49% | 271 | core_destroyed 18 | 2 |
| eider | 16 | 14 | 47% | 223 | core_destroyed 14 | 1 |
| atoll | 17 | 14 | 45% | 230 | core_destroyed 12, titanium_collected 2 | 3 |
| archipelago | 22 | 17 | 44% | 216 | core_destroyed 15, titanium_collected 2 | 2 |
| fjordgate | 21 | 14 | 40% | 204 | core_destroyed 12, titanium_collected 2 | 9 |
| antler | 18 | 12 | 40% | 227 | core_destroyed 11, titanium_collected 1 | 4 |
| lighthouse | 15 | 8 | 35% | 213 | core_destroyed 8 | 0 |
| hive | 19 | 10 | 34% | 319 | core_destroyed 10 | 0 |
| meander | 19 | 6 | 24% | 371 | core_destroyed 6 | 0 |

team lazy has the most below-them drops of the three (6 opponents ≥100 below beat them on
saga alone), e.g. `bd12da93-5866-49af-be73-2d048cafd0fa` — kladde (1799, gap +147) beat them
**1–4**, taking antler r354, moonrise r1000 tiebreak, snowflake r361, saga r231.

## Ranked stealable pairs

Scored on: repeated drops, drops to weaker teams, and **mechanism reachable by our line**
(economy/tiebreak grind or a chip-siege they mishandle — not "out-rush them").

| # | pair | record | evidence | mechanism | fit to our line |
|---|---|---|---|---|---|
| **1** | **Flotte × jackpot** | **7W–31L (82%)** | 12 distinct opponents; **9 r1000 titanium tiebreak steals**; median loss turn 440 | **r1000 economy tiebreak** | **best** — jackpot is our best pool map (6W–1L / 86%, `docs/opponents.md`) and `_v68si` already converted jackpot to a 16/16 sweep vs `flotte_probe` (`results.tsv:143`) |
| 2 | Flotte × moonrise | 9W–17L (65%) | 9 opponents; **7 r1000 tiebreak steals**; median loss turn 550 | r1000 economy tiebreak | good — our moonrise 3W–1L (75%); weakest stealer kladde 1816 (gap +88), `4ece8a7a-3a94-46a4-8e91-23502f849fd2` g2 |
| 3 | Flotte × lighthouse | 6W–28L (82%) | 12 opponents incl. O(1) 1682–1710 (×3) and Banminary 1702–1794 (×3) | mostly **core kill** (r73/79/81/81), 1 tiebreak | partial — `_v74e4` guards are 16/16 vs `flotte_probe` lighthouse (`results.tsv:156,158`), but the proven steal mechanism is a rush we don't have |

Deliberately **not** chosen: Pivot × fjordgate (5W–25L, 83%) is the single highest loss rate in
the dataset and has 5 stealers ≥100 below them — but the median loss turn is 117 and every one
of the 25 losses is `core_destroyed`. It is a pure rush hole, unreachable for us, and Pivot
ships a new version roughly hourly.

## #1 in detail: Flotte × jackpot — the mechanism

**jackpot is 16×16, 50 walls, 14 ore; cores at A(0,0) and B(14,14).**

### What Flotte do wrong there

Two replays decoded in full (`toolkit/replay_lib.py`), both with Flotte at seat B, **different
seeds and different Flotte versions**:

| | `96887bee…` g4 (Flotte v35, 1880) | `3bd204f7…` g4 (Flotte v33, 1790) |
|---|---|---|
| stealer | Powered by SmartFridge, **1759 (gap +121)** | Besvikomat, 1784 (gap +6) |
| **Flotte titanium delivered, whole game** | **120** | **80** |
| Flotte harvesters alive @r100→1000 | 1 → 1 | 0 → 0 |
| Flotte conveyors alive @r100→1000 | 1 → 1 | 0 → 0 |
| Flotte builder bots *built* | 4 | **40** (pure churn) |
| Flotte ammo held at r1000 | 3 | **100, unspent** |
| stealer titanium delivered | **2610** | **9760** |
| stealer harvesters / conveyors | **2 / 10** | 12 / 27 |

Flotte's jackpot economy is **flat from r100 to r1000**. They deliver 80–120 titanium in a
thousand rounds. They spend the game on a forward turret expedition and on re-spawning
builders that die (40 builder bots built in one game). SmartFridge won the tiebreak with a
**2-harvester, 10-conveyor** economy — a very low bar: 2610 vs 120, a 21× margin, and
Besvikomat's 9760 vs 80 is 122×.

### The exploitable determinism

Flotte's jackpot seat-B opening is **byte-identical across seeds and across versions v33→v35**:

```
r0  builder_bot @(14,13)     r4  harvester @(14,11)
r6  conveyor    @(14,12)     r15 launcher  @(11,14)
```

The same determinism holds on meander seat B across seeds `331886149` (v32,
`5c3899f9-633e-4ec8-8faa-29e90ca6e2ee` g2) and `1402563494` (v35,
`6e2109f0-5322-42b0-b833-d83c8c72cb93` g1): first gunner **r7 @(11,5)** in both, then the same
plant tiles `(10,5) (16,4) (10,2) (10,3)`, repeatedly adjacent to the enemy core (dist_sq 1–8
from a core at (11,3)). **Flotte's plant tiles are a per-(map, seat) constant.** That makes
pre-planted denial barriers or pre-positioned defence a precomputable table, not a reaction.

### The corroborating cross-reference in our own repo

- `docs/opponents.md`: jackpot is our **best pool map, 6W–1L (86%)** post-rotation.
- `results.tsv:143` (`_v68si`, saboteur intercept): "drumlin/**jackpot**/lighthouse converted
  to sweeps" vs `flotte_probe` — our instrument for exactly this pattern already sweeps jackpot.
- `results.tsv:142`: `flotte_probe` (md5 `ff968416b484405564106153a16955cf`) was built from a
  replay-extracted Flotte "strangulation" profile — earmarked saboteur, 3-harvester eco,
  state-triggered sentinel push. That is the same profile the wild replays show.

### The one real caveat

`results.tsv:141` (`rematch-flotte`, v52): we have already **survived Flotte to r1000 once
(on hive) and LOST the titanium tiebreak** — "ECONOMIC STRANGULATION remains; the unhunted
saboteur + heal titanium drain lose the long game." So surviving is not sufficient; the plan
needs an **economy floor**, not just a defensive one. The good news is how low the floor is on
jackpot specifically: anything above ~120 delivered wins. Note also that our one historical
game win over Flotte (`585fffc4-7497-4606-bd74-7206e3a5eb41` g5, `pinch`, r1000
titanium_collected) was against a **1533-rated** Flotte on a **retired map** — treat it as
mechanism colour only, not as current evidence.

### Refuted: the "Flotte-meander-only line of study"

The strategy frame's meander hypothesis (`docs/spitball.md:32`) does **not** survive contact
with the data, from two independent directions:

1. Flotte are **24W–12L (33% loss) on meander** — one of their *better* maps, 12th of 15 by
   loss rate.
2. meander is our line's **worst** map against the Flotte pattern: `flotte_probe` meander is a
   standing **0/16 residual** across four separate targeted fixes (`results.tsv:143,145,146,147`).

Meander should be dropped as the theft target and replaced with jackpot.

## Replays downloaded and characterized

All under `CACHE/replays/` (shared cache; `toolkit/fetch_replay.py` used for pacing).

| path | what it shows |
|---|---|
| `96887bee-bb90-4d1d-b9ce-8e93e19b6e04_g4.replay26` | **The key one.** SmartFridge 1759 (seat A) steals jackpot from Flotte v35 1880 by r1000 tiebreak, 2610 vs 120, with only 2 harvesters + 10 conveyors |
| `3bd204f7-2438-4a8c-b49c-b9a0e9f355c4_g4.replay26` | Besvikomat 1784 steals jackpot from Flotte v33 by r1000 tiebreak, 9760 vs 80; Flotte build 40 builder bots and 0 harvesters |
| `5c3899f9-633e-4ec8-8faa-29e90ca6e2ee_g2.replay26` | O(1) 1708 (frozen v7) steals meander from Flotte v32 by tiebreak, 1560 vs 380; O(1) lose **zero** builders, Flotte lose 3 |
| `5c3899f9-633e-4ec8-8faa-29e90ca6e2ee_g4.replay26` | O(1) steals lighthouse from Flotte by tiebreak **11220 vs 110**; O(1) besiege Flotte's core for 1000 rounds (6090 dmg) and cannot kill it — Flotte heal it — but Flotte's economy is 1 harvester / 3 conveyors all game |
| `6e2109f0-5322-42b0-b833-d83c8c72cb93_g1.replay26` | Besvikomat 1788 kills Flotte's core on meander at r218; Flotte economy dead by r200 (180 delivered), 24 conveyors vs 0 |
| `6e2109f0-5322-42b0-b833-d83c8c72cb93_g3.replay26` | Besvikomat steals drumlin by tiebreak 18060 vs 4430; Flotte build 17 sentinels and bank 1251 ammo instead of economy |

Generalized finding across all six: **Flotte have no economy scaling.** Their harvester count
never exceeds 3 and their conveyor count never exceeds 9 in any decoded game; every winner ran
10–116 conveyors. They convert the difference into turrets and banked ammo. If they do not
kill your core, they lose — and they are only 27W–33L at r1000.

## Version stability (weight recent matches accordingly)

| team | current | last change | changes in 16.5h window | read |
|---|---|---|---|---|
| **The Flotte Experience** | **v35** | 2026-08-07T03:34:31 (stable ~6.6h at window end) | 10 (v27→28→29→30→31→32→33→**32**→34→35; note the v33→v32 rollback at 02:55) | Active iterator, but **the jackpot and lighthouse holes persist unbroken across v27–v35**, so they are structural, not version artefacts. Their v35 window alone contains jackpot tiebreak losses (`96887bee` g4, `275c1350` g4) and lighthouse losses (`51cc65d0` g3, `584de603` g3, `298ed22a` g1, `b3bfe182` g2, `4ece8a7a` g5, `bdf8c994` g1). |
| **Pivot** | **v63** | 2026-08-07T09:54:02 (**19 minutes** before window end) | 11 (v54→55→56→57→**53**→58→59→60→61→62→63) | **Least trustworthy.** Ships roughly hourly, including a rollback to v53. Almost all Pivot drop data is from superseded versions; re-scout before acting on any Pivot-specific plan. |
| **team lazy** | **v88** | 2026-08-07T09:13:20 — but this was a *revert* back to v88 | 3 (v88 for 15.3h → v92 at 09:03 → back to **v88** at 09:13, a 10-minute excursion) | **Most trustworthy.** Effectively frozen at v88 for the whole window; their v92 was live for 10 minutes and reverted. Their saga (8W–25L) and moonrise (12W–29L) holes are current. |

## Suggested next actions (not taken — read-only pass)

1. Build a `jackpot`-specific unrated leg vs `flotte_probe` **at seat B and seat A separately**,
   measuring *titanium delivered at r1000* rather than win rate — the win condition we need is
   the tiebreak, and our probe already sweeps the map on core kills.
2. Refresh `flotte_probe` from `96887bee…_g4` (Flotte v35, current) — the existing probe md5
   `ff968416b484405564106153a16955cf` predates v27.
3. Encode the deterministic plant table for jackpot seat B (`(14,13)/(14,11)/(14,12)/(11,14)`
   opening) and meander seat B (first gunner r7 @(11,5)) as a pre-denial or pre-defence
   lookup — this is the "play the players" lever, and it costs no tempo because it is known
   before round 1.
4. Because the theft only needs an economy floor, consider a jackpot-conditional policy that
   refuses to trade builders after ~r150 and simply protects 2 harvesters + a short conveyor
   run to the core. SmartFridge won on exactly that.
