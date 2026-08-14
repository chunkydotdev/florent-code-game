# Staged submission: v145 "Top Team Router v3"

- Version: 145
- Name: Top Team Router v3
- Uploader: x3r0
- Uploaded at: 2026-08-14T19:08:37Z
- Submission id: 024fe2ec-5d5a-4082-9fe3-26164bb42762
- Downloaded/staged: 2026-08-14T19:14:53Z (`date -u`), via
  `.venv/bin/fcode submission download 145`
- Zip contained 107 files (106 `.py` + the platform submission's own
  `README.md`, replaced by this file); all files land flat at
  `bots/_x3r0v145/*.py` — no top-level directory to flatten, entry point is
  `bots/_x3r0v145/main.py`.

## Compile check

`.venv/bin/python -m py_compile` run individually on all 106 `.py` files:
**ALL 106 FILES COMPILE OK**, zero failures.

## File listing (by role)

106 `.py` files = 24 policy modules x up to 4 files each, plus 8 router
modules, plus `main.py`:

- **24 policy families**, most with `{prefix}_doctrine.py`, `{prefix}_eco.py`,
  `{prefix}_main.py`, `{prefix}_raid.py` (24 doctrine, 24 eco, 24 raid, 25
  main — one extra `main.py` is the top-level entry point):
  `crb, crc, crg, d6, fc, gu, la, lc, se, t130` (single-map families) and
  `p07h/p07i, p22h/p22i, p24h/p24i, p25h/p25i, p37h/p37i, p85h/p85i,
  p92h/p92i` (paired h/i families, one pair per opening "salt").
- **8 router modules**: `main.py` (top-level entry), `base_router.py`,
  `cr_router.py`, `p07router.py`, `p22router.py`, `p24router.py`,
  `p25router.py`, `p37router.py`, `p85router.py`, `p92router.py`.
- Total line count across all `.py`: 110,184. Largest single files are the
  `*_doctrine.py` modules (each ~1,600-1,700 lines of constants/map tables).

## Structural facts (entry dispatch, no strategy commentary)

- `class Player` (entry point) lives in `main.py`, top level, lazy-inits
  `self.inner` on first call to `run()` and delegates every subsequent call
  to `self.inner.run(ct)` — same lazy-dispatch pattern as `_x3r0v143`.
- **Two-level router.** `main.py` is itself a thin dispatcher: it identifies
  the current map by a **terrain/core-position fingerprint** (own core +
  computed enemy core -> sorted position pair -> `SIGNATURES` lookup, with a
  `COLLISION_GRIDS` fallback that decodes the engine's packed ternary
  MAP_ALPHABET terrain string when the position-pair signature is
  ambiguous), then side (`A`/`B`, by whether the core matches the map's
  recorded `A_CORES` position). For 9 explicitly named maps
  (`antler, drakkarfjord, drumlin, frostgate, midgard, nordkap, ragnarok,
  royale, yulerune`) it picks a dedicated policy module per (map, side) from
  `WEAK_EXPERTS`; for every other map (or an unresolved fingerprint) it falls
  back to `base_router.Player`.
- `base_router.py` repeats the same fingerprint-and-side dispatch but at map
  granularity over the full known map pool (14 named maps in `OPENINGS`,
  10 in `SIGNATURES` + 4 more via `COLLISION_GRIDS`), each (map, side) cell
  routing to one of **7 "salt" sub-routers**: `p07router, p22router,
  p24router, p25router, p37router, p85router, p92router`.
- Each `p{NN}router.py` is a **third dispatch layer**: same fingerprinting
  again, but only splits on a `WEAK_GRIDS` terrain set (drumlin, nordkap,
  glacierkeep, plus a yulerune/frostgate disambiguation) to choose between
  its own `p{NN}h_main.Player` (fallback/default) and `p{NN}i_main.Player`
  (weak-map variant). `cr_router.py` follows the identical pattern one level
  under `main.py`'s `WEAK_EXPERTS["antler"]["B"]` etc., choosing among
  `crb_main` / `crc_main` (plus a `RICH_GRIDS` branch that monkey-patches
  `crb_main.LOKI_MAX_BUILDERS = 12` / `LOKI_RICH_EXTRA = 4` before
  instantiating it).
- **No opponent-identity or match-outcome inspection anywhere.** Every
  routing decision reads only: own entity type/position, nearby buildings
  (to find the core), the communication store slot holding the packed enemy
  core position, and public map dimensions/terrain. Multiple module
  docstrings state this explicitly ("does not inspect or identify the
  opponent"). This matches `_x3r0v143`'s router, which is a strict subset of
  this one (see below).
- **Map fingerprint constants**: `SIGNATURES` (dict keyed on
  `(width, height, sorted-core-position-pair) -> map name`),
  `COLLISION_GRIDS` (terrain-string -> map name, decoded from a packed
  base-N `MAP_ALPHABET` ternary encoding of `.`/`#`/`o` tiles, 3 cells per
  character), `A_CORES` (map name -> the position that counts as "side A").
  These constants recur (re-derived per router module from each policy's own
  `_doctrine.py`) rather than being centralized once.
- **Policy identities** (from each `_main.py` module docstring's first
  line): `crb/crg/fc/gu/la/t130 = "LOKI-1 (v105)"` (establishment-style raid
  baseline, with `fc/gu/la/t130` being raid-module variants of the same
  baseline — e.g. `fc_raid`, `gu_raid`, `la_raid`, `t130_raid`), `crc/lc =
  "LOKI-CHAMPION (d3)"` / `"LOKI-CHAMP"` (hungrier seal/salt/guns variant,
  "official WR ~53.7% vs baseline loki (n=600)" per docstring), `d6 =
  "LOKI-D6"` ("seal/salt floor 4 + surplus 140"), `se = "LOKI-SEAL2"`
  ("seal/salt floor 4 + fwd_ti_floor 10; RUSH off"). All 14 paired `p{NN}h`
  modules are `"LOKI-1 (v105)"` and all 14 `p{NN}i` modules are
  `"LOKI-CHAMPION (d3)"` — i.e. every salt router is a v105-vs-CHAMPION(d3)
  choice, only `main.py`'s `WEAK_EXPERTS` overrides bring in the other named
  variants (fc/gu/la/lc/se/d6/t130) on their 9 specific maps.
- Every policy's `_main.py` uses the same internal layering noted in its own
  docstring: `doctrine.py` (constants), `eco.py` (economy: harvester
  bootstrap, trunk chains, navigation, siphon hygiene — `EcoMixin`),
  `raid.py` (the offensive "collar"/forward-Sentinel/ferry package —
  `RaidMixin`), `main.py` (`class Player(EcoMixin, RaidMixin)`, dispatch by
  `ct.get_entity_type()`, one blanket try/except per the crash-safety note
  in every docstring).

## Comparison to `_x3r0v143`

`_x3r0v143`'s `main.py` is byte-for-byte the same dispatch shape as this
submission's `cr_router.py` (module names `n_*`/`o_*` there vs. `crb_*`/
`crc_*` here — same `WEAK_KEYS`, same `_decode_grid`, same `_weak_grids`,
same fallback-on-`None`-core comment). v145 is the same router family,
generalized: it wraps that single two-policy (v105-vs-CHAMPION-d3) map
router as one of 7 near-identical "salt" sub-routers (`p07`...`p92`) nested
under a new outer `base_router.py`, and adds a further outer layer
(`main.py`'s `WEAK_EXPERTS`) that swaps in 7 additional named policy
variants (`d6, fc, gu, la, lc, se, t130`) on 9 specific maps instead of the
plain v105/CHAMPION-d3 pair. No new mechanism versus v143 — same
fingerprint-by-core-position-pair-or-terrain-grid technique, replicated and
layered.
