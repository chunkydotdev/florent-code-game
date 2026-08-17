# LEG DECODE PLAN — ferry-siege live leg (pre-drafted BEFORE any leg fires)

**RESEARCH s50, 2026-08-17 ~18:5xZ.** Purpose: if Magnus rules live-leg for `_v510ferrysiege`, these are the decode questions, committed before the data exists so the read cannot be shaped by it. Treatment cells vs the round-2 baseline cells (farming_200s / not adgato / The Bisons / gsxWins — same fixture, same holder era). **This is a decode SPEC, not a tool; scripts get written at decode time under whatever budget then applies.**

## D1 — THE PARTIALLY-SEALED REGIME (the one cell no study measured; local 13/13 games sat in it)
Per game: per-round orthogonal-8 occupancy curve of OUR seal on their ring; defender heal-rate, heal-staffing, and clearing actions AS A FUNCTION of occupancy 0→8, using the **within-game paired form** (same game, different occupancy states — the Juusto study's confound-resistant control), never the pooled form. Deliverables: (a) does the binary law hold in OUR hands (0 heals at 8/8, mechanical); (b) is the partial-state elevation (0.75→1.23/rd shape) provocation or intensity-confound — a leg where WE control seal timing partially de-confounds this for the first time; (c) defender clearing rate per occupancy state vs their Q1 baseline column (field study: farming_200s 0.6% / not adgato 1.4% / Bisons 0.8% / gsxWins ~24-31% P≤25) — **did the near-free-seal teams stay near-free under a REAL directed seal, or was their 0.6% an artifact of incidental barriers?** (The field study's own limit #1: the us-attacking gap could not separate placement from reaction.)

## D2 — FERRY MECHANICS vs the two reference implementations
Taxi cycle length per hop (spec: 2 rounds; Juusto's 3 cost r8→r41); hops per insertion; arrival round (Jython bench: d²≤8 by r6, adjacent r8); raider death count + replacement latency (the SPOF fix working?); launcher self_destruct execution rate (bench 99.7-100%) and scale-neutrality (cost-scale % before/after relay).

## D3 — SEAL GEOMETRY
Tile order actually executed (NEAR-first like Juusto, or spec order); time-to-4/6/8; 8/8 achieved? (local v510 read 0/13, best 7/8 — ⚠ AMENDED 19:2xZ: those 13 were per-map singles and local `--seed` at NOISE_ON is NOT deterministic (builder's v511 fixture law), so 0/13 is 13 one-draw cells, not a rate; v511's 30-game paired grids read barriers-only 9/30 closures — the leg's first binary question stands); far-pair latency (Juusto's stall point); diagonal timing vs the kill-window rule; corner-birth escape rate when orthogonals close (Juusto's defenders escaped via 41.4% corner births).

## D4 — EVICTION (first live data for the element the field runs at 1.2%)
Throws: victim pickup tiles vs the camping distribution (geometry study: 88.6% pre-camped); dump distance achieved (≥6-tile rule; bench: >5.5 tiles ⇒ 33.4% return / median 33 rounds — measure OUR victims' return rates against that curve); launcher siting (reactive-after-~5-heals? ON ring tiles?); 1-vs-2 launcher interception realized vs the 70.5/86.5% adaptive benchmarks; any crash-signature deaths (expected ~0 vs these targets; Erebus excluded from the leg).

## D5 — THE SENTINEL LINE
Build round + d² (bench r75/d²9 Jython, r46/d²16 Juusto); lifetime under fire (field bench: median 8 rounds, 80% turret-killed) and replacement latency; share of enemy-core damage (bench 95-100%); zero-sentinel kill check (bench 0/37, 1/257).

## D6 — OUTCOME + HYGIENE
Kill round distribution vs same-opponent baseline cells (this is the primary treatment-vs-baseline read, same-era by design); win condition mix; **self-cleanup audit: OUR own-blocker destructions must be 0** (field defect: 24.9% of seal breaks are the besieger's own); spawn denial realized (defender spawns/1,000 rounds under our partial and full seals vs the 25.2→0.2 bench, with the affordability control).

## READ RULES (carried from the day's studies)
Cells split by oppver ALWAYS (band churns; team lazy fields unreleased builds unrated). Panel semantics on baselines (unpinned); if the leg itself is a treatment leg it PINS. Per-game event counts are censuses (no DEFF); cross-cell shares carry DEFF 1.833. Snapshot corpus/*.tsv before any join (keeper mid-write hazard). Every subagent anchor opened or labelled RELAYED-UNVERIFIED.
