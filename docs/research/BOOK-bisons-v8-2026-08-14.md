# THE BISONS v8 — OPPONENT BOOK (research s39, 2026-08-14 ~09:3xZ)

Magnus-flagged; builder wire facts verified at the platform channel by the
agent, h2h table independently re-derived by research from ladder_games.tsv
(exact match). Full method + 13 scripts in the session scratchpad
(`bisons_eras.py` … `valk_diff.py`); 20/20 paced replay downloads folded
into replay_archive/. Population/denominator inline on every figure.

## The headline
**v8 is a step change, not a recovery, and their 1727 rating UNDERSTATES
them.** Era table (982 league matches): v7 collapsed −284 Elo in 20 h at
36.5% game share; v8 runs **75.8% game share, 86.8% match wins, +317 Elo**
since 08-13T19:52Z. Above-band scalps: Coreflood 1726 (5-0), arsonist duck
1753 & 1734 (4-1 both), Jython 1743 (4-1), Big O 1741 lost 0-5 to them
earlier eras aside. **They over-perform Elo-expected game share by +24-29pp
in EVERY opponent band including 1700+** (17/25 games vs mean-1739
opposition; implied true strength ~1870 as a point estimate, 95% band
~1740-2050 — INFERENCE, n=25). Gap to us ~38 pts and closing at
+11..+18/match. **On this evidence they pass THROUGH our band, not into it.**

## What v8 is (30 decoded games, field-only cuts)
- **Crash hypothesis REFUTED**: 0 unexplained Bisons-side unit removals in
  426 archived games across v4-v8 (instrument live: 25 opponent-side
  candidates in the same files). TLE 0.00/game, cpu_max 2.4ms of 10ms.
  **CPU denial is not a lever on them.**
- **The change is FORWARD-SENTINEL DOSE, not tempo**: forward turrets/game
  3.00 (v4) → 1.91 (v7) → **4.57 (v8)**; sentinels 4.43/game vs 16 gunners
  total; first forward turret at median r30-34 in EVERY era. Ammo pump:
  980 converted/game, 174 shots/game. 91.9% of turret builds are forward,
  median d²=10 from the enemy core (3.2 tiles; 40 builds at d²≤5).
- **Binary outcome**: 21/21 wins are core kills (median r71, min r46); 9/9
  losses kill nothing. 204/205 rated v8 games end core_destroyed.
  `ti_collected_end` 92/game — the economy exists to feed ammo.
- **They build ZERO launchers and ZERO barriers in 892 archived games
  (v4-v8), and ~zero builder melee in v8.**
- **Opponent-blind deterministic opening to ~r30**: tile-exact identical
  build sequences across different opponents per (map, side) — first
  divergence is always the first turret. Nothing we do before r30 changes
  their script.

## Per-map (205 rated v8 games)
100% ragnarok (14/14) · 100% valkyrie (8/8) · 93% glacierkeep · 91% nordkap
· 88% yulerune · 87% drumlin · 82% midgard … **25% drakkarfjord (2/8) — the
one structural hole**: both decoded drakkarfjord games show ZERO conveyors
by r60 (vs 8-19 elsewhere) and late first turret (r43/46) — their economy
script produces no route home on that geometry (INFERENCE, n=2+2/8).
Small maps are the soft tier (fjordgate 55%, antler 62.5%).
**Overlap hazard: our two worst new maps (midgard 31%, ragnarok 42%) are
two of their three best (82%, 100%). Drakkarfjord is our only edge
(−22.8pp).**

## Map-table facts (load-bearing beyond this book)
- **`mapSeed` does NOT vary terrain**: every game on a map name has an
  identical tile hash across seeds (30 v8 games/15 maps + 250 of ours).
  **Tile-exact hardcoded map tables are fully viable in this league.**
- **The platform patched valkyrie + glacierkeep between 06:52:59Z and
  07:12:59Z today** (valkyrie: ore (6,14),(23,14)→WALL; 8 walls opened).
- ⚠ **`maps/valkyrie.map26` is STALE (pre-patch hash)** — any local work on
  valkyrie runs the wrong map. glacierkeep's local file is current.
- Their tables-vs-sensing: **insufficient n** (post-patch: valkyrie 1/1,
  glacierkeep 1/2; their harvesters sat on both-era ore tiles so the test
  had no power). Circumstantial for runtime derivation (14/14 ragnarok
  within ~24h of the map appearing) — INFERENCE, not measured.

## Pairing book vs us
- H2H by their era (145 rated games, re-derived exactly): v2 76.7% us …
  **v4 31.7% us** … **v7 0/5 — we lost five straight to their WORST
  version, cores down at r53-78.** **v8: never met.**
- **The measured counter is NEST REMOVAL**: their dose is identical in
  wins and losses (4.6 fwd turrets either way); defenders who tear the
  nest down win (field removal rate in their losses 66%; Besvikomat 9/9,
  Jython 6/6). **We remove 15-17%, in wins and losses alike** (20 decoded
  h2h games) — our wins came from out-racing, and v8 doubled the dose
  since. We have the capability (batk 58.9/game in v134-era decode); it is
  a TARGETING problem.
- **Out-racing is now losing math**: their median kill r71 vs our recent
  medians 133-176.
- **The Loki angle, unspent**: every point of their damage needs an
  unescorted, melee-less builder to walk to our core and stand there from
  ~r25-33 — and they have never built a launcher. **A home launcher is
  uncontested against the most predictable kidnap target on the ladder**
  (routes into #45/#38; their opening is opponent-blind so the ambush
  window is free).
- They are band-admissible at 1727 if a leg wants them (payout at fire
  time per target_value).

## Routing
Evidence appended to QUEUE #3 (clear-more-enemy-turrets: the 66%-vs-15%
removal gap is its sharpest demand-side number yet) and #45 (kill the
builder: the nest-builder as named customer). Stale valkyrie map file →
builder, urgent. mapSeed/table facts → this book + tape. Profile feeds #39.
