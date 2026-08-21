# BUILD REPORT — `bots/_v601skalman` (survivability iteration, autopsy-grounded)

**Builder s54, 2026-08-21 ~18:0xZ.** Copy of `_v600skalman1` + three flag-gated planks +
one bugfix, each designed against a RANKED MEASURED CAUSE from
`scratchpad/s54_autopsy/tape30_autopsy.md`. Built by a fresh opus agent; verification
artifacts at `scratchpad/s54_v601/`. No submit, no platform matches, no game-share claim.

## Planks (each single-flag ablatable, ablations DRIVEN — table below)

* **SK_HARV_ESCALATE** (cause 1, 33/33 harvester deaths): the belt rebuild-escalation
  ledger extended to harvester tiles (N=2, priced for 20 Ti; 60-round ban, lifted on
  killer-confirmed-dead); killer inferred geometrically and PUBLISHED on slot 14 (one
  writer). Escalation fenced to d²≤100 so the keeper's home-role signature survives.
* **SK_BELT_COVER** (cause 2, 0/42 coverage): gun siting scores (site, facing) pairs and
  requires the facing RAY to cross live trunk beyond d²13; reads the slot-5 b18-23
  uncovered-gap word v600 published and never read. Sub-flag `SK_BELT_COVER_TRIGGER`
  (disclosed extension): the keeper may buy a trunk gun when a belt killer is located,
  inside the unchanged SK_DOOR_GUN_CAP=2 — siting alone had ~1 turret/game to act on.
* **SK_TARGET_PRIO** (cause 3, 75% of fire on barriers): one strict target ladder for
  guns and pecks — core-damagers/harvester-killers first, turrets, harvesters, and
  barriers ONLY when path-blocking; pecks skip enemy-builder-attended targets (the
  DOORWAVE healing-race lesson), guns don't.
* **SK_ORE_SENSE** (bugfix, flagged for ablation only): **the zero-harvester root cause —
  `known_map_for` returns None on 10 of 15 pool maps** (measured by re-encoding every
  map vs MAP_CODES), and the keeper's ore walk was the ONLY grid consumer with NO live
  fallback despite `_load_grid`'s docstring promising one. Fix: sensed-terrain ore scan +
  belt planning ungated from the grid (unseen = passable, vision-corrected) +
  `_belt_evict` for occupied planned tiles (permanent belt stall measured on stavkirke).

## Verification (agent, both-ways throughout; builder review of the tables)

AST 5/5 + forbidden forms 0 + undefined globals 0 (DIRTY controls fire) · 6 aliveness
games, 6 maps, both seats: 0 tracebacks, 0 exception-channel removals · zero-mined games
**5/6 → 0/6**, total mined 340 → 5,700 · pooled fire discipline: shots on barriers
44.4% → **0.0%**, pecks 83.3% → **6.4%** · drip lattice 96.8% (61/63; both off-lattice
calls are amount 6 on the can't-afford path — pre-existing, one-line v602 fix named).

| flag off | its signature ON → OFF |
|---|---|
| SK_HARV_ESCALATE | rebuilds into ≥2-death tiles 0.0% (0/11) → 21.4% (3/14) |
| SK_BELT_COVER | trunk-ray coverage 7.5% → 0.0% |
| SK_TARGET_PRIO | shots on barriers 0.0% → 43.2% |
| SK_ORE_SENSE | trunk-tile-rounds 1340 → 666 |

⚠ **Plank 2's briefed signature ("was the dead piece covered") is a COLLIDER** — it
conditions on death, which plank 1 prevents; replaced by the death-independent
trunk-tile-rounds-in-ray metric (0.0% → 8.3%, ablates cleanly). **Planks 1+2 are
coupled** (plank 2 consumes plank 1's killer word).

## Open items this build creates (v602 surface)

1. **`_pick_nest` returns None when `map_grid is None` ⇒ the SIEGE ENGINEER plants NO
   forward turret on 10 of 15 pool maps** — the nest verb has been silently inert on
   2/3 of the pool since founding; same root-cause family, outside this brief.
2. Drip lattice one-liner (`lattice_floor` unconditional).
3. stavkirke keeper wall-pocket parking (pre-existing navigation).
4. Door self-trap guard was added mid-build after a measured full-HP-gunner demolition
   (holmgang r70); the no-damage removal channel went 1 → 0.
5. ⚠ **KILL-ROUND HAZARD for the screen: fimbulwinter went r138 → r1000 (tiebreak).**
   The economy fix lengthens games; `R1000_IS_DEFEAT` makes that a defeat. The fidelity
   tape's outcome distribution is reported with the round numbers, and any v601 adoption
   read carries the kill-round column.
6. Platform CPU `match test` owed before ANY exposure (local CPU reads 0, thrice-known).
