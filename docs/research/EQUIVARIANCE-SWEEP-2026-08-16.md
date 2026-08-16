# EQUIVARIANCE SWEEP of bots/_v223sealrepair — every seat-asymmetric decision site

**Produced:** 2026-08-16 (builder s45, sonnet subagent, static analysis; written after the
seat bug at main.py:289 was measured at +4.84pp of a +6.28pp byte-identical-self-play seat
effect). **Purpose:** enumerate sibling defects — code whose DECISIONS depend on absolute
coordinates, absolute compass order, or absolute iteration order, and therefore behave
differently per seat on mirrored maps. This is a PLANK-CANDIDATE LIST, not a verdict.

## Ranked live sites (decision-changing, fixable)

1. **main.py:289 spawn-ring hash** — MEASURED (+4.84pp of the effect); FIXED in
   `_v450seatspawn` (queued as SEATSPAWN). The template fix: fold candidate offsets
   through the own-map-half sign before hashing; canonical tiebreak.
2. **raid.py:819 `_pick_raid_station`** — `(s.x*17+s.y*31+slot*7)%97, s.y, s.x` score
   tiebreak decides which of ~12 stations around the ENEMY core each raider claims.
   Gates the collar doctrine; per-raider, every rescan. Fix: hash `(s−E)` enemy-relative
   with the sign fold.
3. **eco.py:780 ore-tile assignment** — same hash pattern orders same-distance ore tiles
   AND buckets them per worker (`ordered[worker::workers]`). Frequent. Fix: hash
   `(t−core)` with the fold.
4. **eco.py:159-180 `delivery_seats`** — heal_seats enumerates N,NE,E,… from literal
   North regardless of seat; ties break "north-most" absolutely. Feeds `seat_ban`,
   consulted every turn downstream.
5. **eco.py:392-431 `_link_path` multi-source BFS** — the goal SET's CPython iteration
   order (a function of absolute coordinate hashes) decides which equidistant core-side
   the trunk terminates at. Fix: explicit seat-canonical list before the queue.
6. **main.py:58/313 + eco.py:803 ore-search fallback spiral** — angle seed 0 = literal
   East. Rare path (no-ore-in-vision only). Named untreated in the loki29 prereg.
7. **raid.py:900-943 launcher throw-site sort** — stable sort over a fixed
   west-first/north-first sweep decides distance ties for exile/ferry throws. The
   doctrine's signature move.

## Engine-order sites (LOW confidence, not unilaterally fixable)
main.py:173-186 (core threat latch takes engine's first enemy) and main.py:749-755
(turret fire fallback) — first-match over `get_nearby_entities()`; the engine's
enumeration order is confirmed row-major only for `get_attackable_tiles()` (the
sentinel-fire fix's own comment). Fixable by re-ranking with explicit keys, not by
reordering the engine.

## Already measured / ruled out
* **CARDINALS fixed-order family = SR1NULL** (loki29 prereg, Amendments 3/4):
  inconclusive at SE≈1.97pp, NOT proven inert; ~30 sites enumerated in the sweep
  transcript. Not re-proposed.
* **main.py:718-748 sentinel fire priority** — already fixed for exactly this class
  (its comment documents the row-major hazard). Positive control.
* **eco.py:53 `enemy_core_for` fallback** — point-reflection formula, symmetric by
  construction.

## Genuinely NEW, unmeasured, never enumerated before
**The DIRECTIONS (8-way) first-match family:** eco.py:1112 (`_expand` harvester
placement), eco.py:1232 (ore-adjacent retarget), main.py:573 (counterbattery facing,
nested inside a CARDINALS loop — double-absolute). Not covered by SR1NULL.

## Not determinable statically (owed to a measurement pass, not more grepping)
Whether entity-ID parity (`idx & 0xFF` at eco.py:868/main.py:313) correlates with seat
(engine ID-assignment order); whether `get_nearby_*` getters share the row-major order;
how often `_link_path` BFS ties actually occur in live play.

## Design consequence (builder)
SEATSPAWN (site 1 alone) is rung 1 and is queued. **Rung 2 = `_v455seatfull`**: sites
1-5 + 7 under ONE toggle (`LOKI_SEATCANON_FULL`), flag-off byte-equivalent, so the
SEATSPAWN-vs-SEATFULL contrast isolates "the rest of the family" (expected small: the
residual is ~1.4pp of the 6.28) while SEATFULL-vs-control measures the family ceiling.
Engine-order sites and the DIRECTIONS trio excluded from rung 2 (different fix class;
candidates for rung 3 if rung 2 pays).
