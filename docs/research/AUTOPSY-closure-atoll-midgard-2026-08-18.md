# AUTOPSY — why the collar never closes on atoll and midgard (s51, 2026-08-18)

*Banked by the builder s51 from the opus closure agent. Data: the 30 fired-config games in
`scratchpad/s51_evict_autopsy/` (no new games). Two independent instruments joined per game:
the bot's `FS DL` stderr series and a replay-derived occupancy tape of the enemy core's 8
orthogonal heal seats (built on `tools/replay_census.py` primitives). Six guards all driven
both ways incl. a mutation control and a 13/13 closing-game cross-instrument agreement; two
independently written attribution passes agree digit-for-digit. Artifacts:
`scratchpad/s51_closure_autopsy/` (parsers + 10 derived TSVs).*

## VERDICTS (one line each, agent's, ratified by the builder)
* **ATOLL — MIXED, behaviour-dominant.** Largest cause: enemy building placed on a seat AFTER
  our arrival (`BELT_POST`) = 6/9 closure-binding seats (4 conveyor + 2 SENTINEL the defender
  builds on its own heal seat); occupancy 50.1% of open-seat-rounds; worst attrition on the
  grid (0.77 of our seat-buildings destroyed per seal built). Funding: 0.2%.
* **MIDGARD — MIXED, geometry-dominant.** Largest cause: the defender's PRE-ARRIVAL
  ore-delivery belt on core-adjacent seats (`BELT_PRE`) = 14/27 closure-binding seats, in 6/6
  games. Second, separable, LAUNCHER-LINE: the ferry hop lattice terminates at dsq_core=13
  (outside FS_RING_DSQ=8) in 5/6 games — B-side arrival r78/123/187, producing 8 of the 11
  EMPTY never-denied seats.

## The load-bearing findings
1. **Hypothesis "geometrically unsealable seats" is FALSIFIED**: all 80 orth seats across the
   5 grid maps × 2 sides are in-bounds, non-wall, barrier-legal. atoll/midgard have the SAME
   static seat set as the maps that close 10/12.
2. **The map driver is ORE PROXIMITY**: nearest ore at chebyshev d=2 (atoll) / d=3 (midgard)
   of the enemy core forces the delivery belt to terminate ON heal seats → enemy-building
   occupancy 46-58% of open-seat-rounds vs 0-25% on closing maps. `can_build_barrier` refuses
   an occupied seat forever; `_fs_denied` correctly counts it open forever.
3. **ZERO of the 36 closure-binding seats on atoll+midgard were enemy-BODY-held ⇒ eviction
   converts none of them. The launcher is not the closure lever on these maps** (a launcher
   cannot throw a building).
4. **The belt-clearing race is structurally lost twice**: FS_CLEAR_MAX_PECKS=8 × 2 dmg = 16 <
   20 HP conveyor (one visit can never finish; clears when they DO land convert 100% — the
   verb works, the budget doesn't: atoll 163 pecks→9 tiles, midgard 54→1); and the defender
   heals the belted seat at +4/round vs our 2/round peck (HP ledger: dealt 24/healed 24 = net
   0, repeatedly).
5. **The `:1819` ferry-slot defect is real and does NOT cause the closure failure**: 12 in-ring
   ferry launchers, pickup envelope covers 0/8 seats in 12/12 cases (they land on the outer
   diagonal). A purpose-sited evictor could reach 4/8 seats (max over legal tiles, identical
   all maps); actual rung-2 evictors reach 1-2 — **siting at half ceiling**. Counterfactual on
   midgard: in-ring ferries covered 0/280 body-on-seat rounds; best-sited tile 279/280. But
   per finding 3, even a perfect evictor converts 0 closure-binding seats.
6. **Raider gaps are a symptom, not the mechanism** (12 + 1 seats lost across all gaps);
   **arrival latency on midgard-B is a hard defect** (terminal hop dsq 13, walk-in fails,
   replacements arrive r78-187). Other maps' arrival: atoll r5, drakkarfjord r11,
   glacierkeep r9, nordkap r5 — all in-ring hops.
7. **Instrument side-finding**: the bot's `orth_open` is biased HIGH (`_fs_denied` returns
   False on unreadable tiles; edge seats fall outside builder vision r²=20). It can only MISS
   a closure, never invent one — but `FS_PH_SEALED` and `_fs_salt_ok` gate on it.

## Fixture caveat (load-bearing)
The defender in all 30 games is `_v488beltbreak2` — our own bot. Ore-at-d≤3 is a durable MAP
fact; that THIS defender belts its own heal seats and heals them at +4/round is a property of
our chassis, not a field measurement. Whether the field belts its heal seats the same way
needs live legs (rule 6), unavailable under lock-in.

## Builder consequences (s51, routed to the v514 design gate)
* **Launcher-line, in scope now**: (i) ferry terminal hop must land within FS_RING_DSQ —
  measured cost 64-173 rounds on midgard-B; (ii) evictor siting to the max-coverage tile
  (4/8 reachable vs 1-2 actual); (iii) `:1819` counts only ROLED evictors. All three are
  DOUBLEFERRY-adjacent; spec after the relay probe lands.
* **Not launcher-solvable, for Magnus/queue**: the belt-on-seat race (peck budget one short ×
  heal-back at 2:1). Candidate shapes — clear-budget raise, sentinel-on-belt-link (RAYDISC
  family), or conceding closure on ore-adjacent-core maps in favour of the field's no-seal
  core-range-sentinel kill shape (0033 study discriminator) — are a NEW question, not this
  plank's iteration.
