# AUDIT — Map-keyed exposure in the head line (finals-on-unseen-maps question)

**Commissioned by:** builder s52, on Magnus's direct concern (2026-08-20, verbatim intent: "If we
are going to try and win the final that are on maps that havent been announced yet we might need
to make tactics that arent too hardcoded to the maps we see now").
**Method:** one read-only sonnet subagent over `bots/_v529merge` + `bots/_v531fix` (all five bot
files each); trees verified byte-identical on `doctrine.py`/`siege.py`/`raid.py` (v531fix =
v529merge + appended v530 block); every claim carries file:line. **No file modified.**
**Context facts:** the map pool rotated once already (10 of 15 changed, ~2026-08-10); the
Controller API has NO map-name getter, so all keying is on `(width, height, core-position)`
tuples and/or exact terrain fingerprints derived offline.

## Headline (ranked by exposure for an unseen finals map)

1. ⛔ **`known_map_for`'s SINGLETON SHORT-CIRCUIT is the most exposed mechanism** (eco.py:133,
   table doctrine.py:1110/1142, ~31 catalogued signatures): when exactly ONE catalogued map
   matches `(w,h,core)`, its stored grid is adopted with **ZERO terrain verification** (the
   sensed-tile check at eco.py:135-143 runs only at ≥2 candidates — and even then returns the
   closer KNOWN grid, never None). A finals map colliding on dims+core with any one of ~29
   singleton signatures **silently corrupts `map_walls`/`map_ores`/pathing templates for the
   whole match** — cached once, never re-verified (main.py:1352). Recurring dims
   (20×20/24×24/26×26/30×30) make this real, not theoretical.
2. ⛔ **`FS_MAP_SKIP` is NEVER grid-confirmed** (doctrine.py:2366; test at siege.py:506): 5
   loose `(w,h,core-pair)` tuples; a false hit permanently disables ferry-siege on the map with
   no tell. The `(26,26,(5,5),(19,19))` entry (snowflake AND archipelago, deliberate shared
   entry) uses a common map-gen margin convention — the likeliest accidental collision.
3. **Cripple gates (v519/v525) are grid-confirmed** (`LOKI_FS_V524`, siege.py:511-582) — a
   colliding new map coinflips between two WRONG stored grids, but the blast radius is bounded
   (stands the optional plank down; chassis plays normally). Mostly sane.
4. **`CORE_PAIRS`/`enemy_core_for`** (eco.py:82,97): table miss falls back to point-reflection —
   sane on every symmetric map, including maps absent from the table.
5. **Genuinely-unseen maps (no collision) degrade SANELY everywhere**: `known_map_for`→None
   routes to live-vision ore scan + spiral search (eco.py:1698,1742-1754), `_bfs_direction`
   falls back to cardinal step (eco.py:1810-1819), `FS_MAP_SKIP` miss = ferry-siege runs
   normally. **The unseen-map default posture is rush-everywhere-with-live-sensing — the
   FORCEALL-measured direction.** The hazard is FALSE MATCHING, not missing.
6. **`B8_ON`** (doctrine.py:442-455) is dead code — defined, never read. No exposure.

## Tuned-not-keyed constants (run everywhere, fitted to the current pool)

`FS_MIN_CORE_DSQ=72`/`FS_MIN_MAP_DIM=12` (fit to fjordgate/jackpot, doctrine.py:2341-2348) ·
`FS_V525_MIN_MAP_DIM=10`/`FS_V525_MIN_CORE_DSQ=32` (fjordgate's own values, doctrine.py:4818-19) ·
`V530_MOUTH_MAX_LINKS=16` ("pool's deepest crater ore is 11" — glacierkeep; a deeper finals ore
silently falls back to parent ordering) · `V530_MOUTH_MAX_RND=40` and `V530_CORNER_MAX_RND=120`
(timing fit to measured opponent arrivals on current pool maps). Lower severity: these run on any
map, but their justifications are pool-specific measurements, not geometry-derived rules.

## Fix directions (builder judgment, not part of the audit)

* **F1 (small, high value): extend the sensed-tile verification to the n==1 case** — the
  comparison code already exists; verify every match against visible terrain and return None on
  mismatch (falling into the sane live-sensing path). Kills exposure #1 with ~no new machinery.
* **F2: grid-confirm `FS_MAP_SKIP`** the way v524 confirms cripple grids (stored terrain
  fingerprints already exist as a pattern at siege.py:63-65).
* **F3 (policy): new map-conditional planks use geometric predicates or grid-confirmed
  signatures; every keyed list carries a REGISTERED unmatched-map default.**
* **Generalization battery** (separate leg): head vs incumbent on the 9 rotated-out era-1 maps +
  `maps/invented/` (9 authored maps, 8×8→30×30) — the in-pool vs out-of-pool share gap is the
  overfit number. Fixture exists; `run_battery.py` reaches subdirectory maps as
  `invented/<name>`.
