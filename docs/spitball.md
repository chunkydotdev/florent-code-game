# Spitball — shared idea board (Magnus + any session)

Low-ceremony. Append ideas as bullets with a date + author tag. No idea is too
dumb for this file — the ore-barrier track started as "unreasonable variants."
The measuring session harvests from here each cycle: an idea graduates by
getting a pre-mortem against real replays, then a gated build. Verdicts get
written back next to the idea (KEEP/REFUTED/PARKED + one line of evidence).

Rules of the road (so parallel sessions don't trip each other):
- This file is append-mostly; anyone may add, only the measuring session
  writes verdicts.
- Research sessions: read everything, measure nothing (no arena, no
  submissions, no unrated challenges — the rate limit is shared), edit no
  bot. Drop findings here or message the main session directly.
- Two-arm operation (builder + research): full protocol in
  docs/two-session-protocol.md (2026-08-07). Coordination notes + the
  IN-FLIGHT registry moved to docs/coordination.md — this board returns to
  ideas/findings only.

---

## Open ideas

- (2026-08-07, Fable) Seat-conditional opening via ct.get_team() — the bot
  knows if it acts second; whatever race seat B loses, play a different first
  ~40 rounds. Awaiting the seat-B diagnosis verdict. **HOT — two nemesis
  classes implicated.**
- (2026-08-07, Fable) In-match opponent-class classifier (rush/chip/grind
  detectable by r60-150 signals) → policy switch. Slot 9 (SLOT_LINKS_DONE) is
  dead and reclaimable for it. The "use of spies" chapter.
- (2026-08-07, Magnus, backlog) Forward launcher exile: launcher near their
  farm throwing THEIR builders into corners. Labor denial, no ammo cost.
- (2026-08-07, Magnus, backlog) Multi-scout — becomes viable once the threat
  store is widened past one slot.
- (2026-08-07, Fable) One-map specialist prep vs top-8 (game-share Elo makes
  a single stolen game vs E<0.20 net-positive; e.g. a Flotte-meander-only
  line of study before Stockholm).
- (2026-08-07, Fable) v82's archipelago 0/32 hole — x3r0's "high-x asym"
  lever owns it; absorb or counter.
  **CORRECTED 2026-08-07 (research session, code-read): the attribution above
  is FALSE.** The whole v79→v82 diff is 25 lines, one hunk
  (`opp_v58/main.py:949`), gated on `600 <= area < 650 and mw == mh` —
  archipelago is 26x26 = 676 and fails it outright. The lever is hive-B only.
  What actually owns archipelago was already in v79, byte-identical: (a)
  `gun_sense=100/b_sense=36`, the top threat-sensing tier, fires only on
  `area>=650 and mw==mh` — in this pool exactly archipelago + snowflake; (b)
  `keep_artillery_forward`, so their saboteurs never recall home on a 676
  square. (a) is borrow-item **B8, the one we never built** — our sensing is a
  flat 64/16 everywhere. Predates v82: `results.tsv:130` has `_v66eq4` losing
  archipelago 0/32 to `opp_v50`.

## Research-session findings (2026-08-07, read-only; verdicts still owed)

Five parallel read-only researchers. Nothing measured, no bot edited. Claims
below are code-read or replay-decoded; the measuring session owns the verdicts.

- **Grind residual is solvency, not DPS — the framing was wrong.** Decoded the
  hive replay that `_v72e2/main.py:104-118` itself cites. Two staggered
  sentinels theoretically do 18 dmg/rnd; **realized was ~4/rnd** (both sides
  ammo-starved). Core HP *plateaued at 480-500 from r196 to r644* — healing was
  winning for 450 rounds. Death was a 137-round collapse (r649-786) that
  coincides with kladde's ammo recovering. We went 470 Ti → 16 by r250 → 0, and
  **healing stopped for 300 straight rounds** (zero heal events r300-599)
  because we could not pay 1 Ti/heal. Smoking gun: **0 of 270 builder attacks
  landed within dsq<=41 of our own core** — turret-hunting never engaged, ever.
  Why: hunting needs `HUNT_MIN_HEALERS=2` others near the core (`:148`, gate
  `:1610`), so the hunter is a 3rd body; a 3rd body needs ti>=250 or ti>=1500;
  titanium sat at 0-85 for 500 rounds. **The raid that hunting answers destroys
  hunting's own fuel precondition.** rp and mh were flat for the same reason one
  layer down. Farm dies r63-390 (4/5 harvesters, all 28 conveyors, ~1 conveyor
  per 10 rnds for 330 rnds) — inside the window `MEDIC_MIN_RND=150` (`:184`)
  deliberately leaves uncovered on the stated assumption "the churn the medic
  exists for is late". That assumption is contradicted by the replay.
- **SLOT_THREAT thrash largely exonerated.** `_hunt_turret` never reads
  SLOT_THREAT — it scans `get_nearby_buildings()` and resolves multiple turrets
  by local id-ballot (`:1578-1599`), built to dodge the single-slot trap. The
  limit is real for counterbattery *construction* and approach, not the kill
  mechanism. Ranks below farm defense.
- **Eider is a different problem from hive.** The eider loss decoded as
  `titanium_collected` — r1000 tiebreak, **both cores near full HP**, no siege.
  Kladde fielded 16 builders to our 5-12. Half the "grind residual" is
  throughput, not siege. `_v73e3`'s own ablation agrees: eider's 8 wins are
  unthreatened seat-B economy races.
- **Seat-B collapse = engine turn order, and a fix is already drafted.**
  `game-model.md:54-57`: Team A's Nth builder always gets the lower unit ID and
  units run in ID order, so **every** A action resolves before **any** B action.
  Corpus (`_v73e3/main.py:2404-2445`, 20 production games): **19 vs 38 builder
  deaths by r80**, **one mutual trade in 20 games**, **9/9 round-1000 tiebreaks
  went to whoever held seat A**. Contested-ore avoidance tested and REJECTED
  (3-3) — "the tax is exposure, not tile races." Fix defers frontier ore for
  Team B gated on `SLOT_UNDER != 0`. Refuted en route: blanket deferral (kladde
  eider 8/16 → 0/16), seat-B second gun (flotte 96.7 → 90.0).
  **Gap: the deferral is inside `_pick`, guarded by `role == "expand"`.** The
  roles that go forward on purpose — interceptor (role_n 1), siege engineer
  (role_n 0) — never route through `_pick`. Nobody has broken the 38 deaths down
  by role. Do that before another measurement cycle.
- **Seat asymmetry (atoll/heart/lighthouse ~28-31%) still open, but narrowed.**
  Archipelago's 77% is explained (tempo → tile race → 62 vs 27 harvesters). New
  argument against the reflection-bug theory: heart is the only *mirror* map of
  the four; atoll/archipelago/lighthouse are all 180°-rotational — yet heart's
  sign matches atoll and lighthouse, not archipelago. **The sign crosses the
  symmetry-class line**, so no reflection-vs-rotation bug differentiates them.
  Both previously-suspected orientation bugs are refuted or superseded in live
  code. Best remaining lead, still unmeasured: **time-to-first-delivery per
  seat** (on lighthouse seat A had better metrics on every axis, near-parity
  harvesters 8-7, and still lost).
- **Classifier: rush separates, chip/grind does NOT.** Rush is flaggable by
  r10-20 on negative evidence (band_probe builds zero economy, ever; wild median
  first-Sentinel turn 4.5). Strangle vs grind is **not** separable in r60-150 —
  the only cheap discriminator is concurrent raider count (flotte 1, kladde 2),
  thin and noisy; the real discriminators need scouting or fire too late (Lunds
  strike r69-900, kladde fallback r450). That is exactly our weakest class.
  **But the cost matrix says we don't need it:** the one dangerous
  misclassification is grind→rush (curtailing economy), already measured twice
  (`_v69bc` -13 pts, `_v70ec` bootstrap inversion). Every other cell is cheap
  because heal+hunt+don't-gut-economy is right for *both* slow classes.
  → Recommend default + two independent flags, NOT a 3-way switch. Make the
  Core the **sole writer** of any verdict slot: sidesteps the clobber trap
  entirely instead of guarding it.
- **Slot 9 confirmed dead in the LIVE bot** (`_v72e2:248`, only uses `:2352`
  and `:2368`, a counter that increments itself and is never read by any
  branch). **But all 16 slots are allocated and slot 9 is the only reclaimable
  one** — store space is exhausted; anything needing 2+ slots must evict.
- **cad_probe is a stale instrument and the CAD/meander trade rests on it.**
  The obvious separator was already tried and refuted: `COUNTERBATTERY_RICH_TI`
  (`_v72e2:102`) is declared and **never referenced** — dead code — because both
  CAD's insertion and meander's duel open on a rich bank. Meanwhile CAD shipped
  v110 (~1669) and vs the *real* CAD v107 we went 5-10 = **exactly** the E~0.32
  expectation, no mechanism-specific vulnerability. We may be paying a meander
  cost to fix a ghost. Cheapest fix: decode one fresh replay, re-freeze as
  `cad_probe_v2`.

## Breakthrough scavenge — external metas (2026-08-07, research session)

Sources: Battlecode 2019-2026 postmortems, Halite I-IV, Screeps, CodinGame
legend league, Factorio/Mindustry/Satisfactory logistics, SC2 economics,
Generals.io. Full report in session tape; the transferable core:

- **+400 Elo = a ten-fold increase in per-game odds** (50% → 90.9%), since
  Δ = 32×(games_won/5 − E) is a per-game Elo applied five times. Honest
  non-overlapping sum of every lever we can name: **+150 to +250** → ~1670-1770,
  top 8-12. **The rest is not in this strategy family.**
- **Why four gated ships converted to nothing — four champions say the same
  thing.** An A/B against your own history systematically under-values any
  change whose value is against opponents you don't play. Just Woke Up (2025
  champions) shipped defense towers that *lost* vs their own past bots and it
  won them the tournament; XSquare: "if I feel the upgrade should be good and
  winrate is close to 50%, I keep it." **TheDuck314 built imitation opponents
  named after rivals — our probe triad — but rebuilt them whenever a rival
  changed. Ours are all frozen.** Counterweight from SPAARK (threw two years on
  last-minute changes): mechanism-override is for changes with a decoded replay
  behind them and time to observe, never for a last-minute swing.
- **One conveyor lane = 10 Ti/round = exactly 4 harvesters** (1 stack/tile ×
  1 tile/round; a harvester emits 2.5 Ti/rnd). The 2x2 core has 8 orthogonal
  input tiles = 8 lanes = 80 Ti/rnd ceiling. A 5th harvester on a saturated lane
  earns **zero**, costs 20 Ti, and raises the +5% multiplier on every future
  harvester. `ECO_CAP=18` has never been checked against this ceiling.
- **Short manifolds beat long balanced lines** (Satisfactory/Factorio): every
  belt tile is dead capital (up to 10 Ti stranded per tile, scoring nothing at
  r1000), refill latency after every cut, and enemy attack surface. Also:
  **balancers are the wrong tool** — fairness isn't our objective, delivery is.
  Our splitter accepts only from behind so it **cannot backflow** — strictly
  better than Mindustry's router, worth saying out loud.
- **Harassment is paid in the defender's attention, not HP** — and denial is
  worth *more* here than in SC2 because a stalled conveyor has **no catch-up
  curve**. We have measured ourselves paying this bill: **819/708/905
  consecutive rounds** of one builder's entire action budget and ~20% of match
  income, defending a 3 Ti conveyor. Flotte and CAD extract it for 2 Ti/round.
  **We have never once run it in the other direction.** Corollary: our
  escort/medic response is the losing side of the same trade — the answer is
  `destroy()` the doomed relay, reroute short, walk away.
- **Don't add search.** Every economy/territory contest was won at depth-1 with
  a strong static eval; Halite's top three all used *greedy* target selection.
  pb4: beam 400→600 at equal depth = **−15 ELO**. The bottleneck is the cost
  function's fidelity, not the planner's optimality.
- **Hysteresis everywhere a target is chosen** — three top finishers
  independently (1.75× abandonment penalty + 3× switch threshold; "ships don't
  regret previous moves"; "the active target's score is halved"). Aimed
  directly at our measured churn: meander 201 conveyor builds / 86 deaths,
  three tiles rebuilt **27/14/7 times**.
- **Opponent-move prediction is a four-way negative** (pb4 −10 ELO;
  blasterpoard "failed outright"; TheDuck314's net "basically no impact";
  reCurs3 "sometimes detrimental"). What *worked*: modelling opponent
  **latencies and tics**, not optimal play — wlesavo detected an over-used move
  and upweighted the counter. That is "play the players" arriving as a
  convergent meta from outside.
- **Deliberate decision noise as a defence.** RoboStac (1st, Code Royale)
  injected a random tie-breaker specifically to prevent deterministic play;
  delineate (1st, FC2022) randomised BFS cell costs in ~10 lines. If any ladder
  (map, opponent-version) pairing reproduces identically, we are re-losing the
  same game — converting a guaranteed loss to a coin flip pays +3.2 Elo/game.
  **Falsifier: replay two ladder matches vs the same opponent version on the
  same map and check the outcomes are identical.**
- **Keep retired maps.** Producing Perfection (2023 champion) shipped a tool to
  convert *last year's* maps into the current format for ~60 free test maps. We
  retire ~18 maps a week and delete them — while our gate's central failure mode
  is overfitting to a narrow frozen set.

### Unexploited rules, ranked (all verified against our code unless noted)

1. **`destroy()` is never called — zero occurrences in `_v72e2`, `_v73e3`,
   `_v71eir`, `_v70cm`.** It is free, unlimited per turn, no cooldown, refunds
   in-transit stacks, and **removes the entity's contribution to the team-wide
   cost scale**. Target set already measured: 18 of 40 surviving relays connect
   to nothing; meander shows 201 conveyor builds = +201% conveyor scale pricing
   every future build.
2. **The terminal bank is a turret-rounds problem, not an ammo-buffer problem.**
   We end with 2,782-3,031 Ti having fired **13 shots in 1000 rounds**.
   `convert_ammo` takes **one call/turn with no cap on the amount**, usable the
   same turn, free of the action cooldown — **the entire bank converts in one
   round the moment a target appears.** Both refuted experiments moved a
   *quiet-phase floor*, the opposite failure. This is the SC2 timing-attack
   lesson: the spike is latent and invisible.
3. **Barrier doctrine — 10 HP/Ti, the best in the game** (sentinel and builder
   both 1.33). *Correction to the researcher's claim that we have never built
   one:* we do, at `_v72e2:1742` — but it is a **single hardcoded tile on one
   map** (`hive_bunker`, 25x25, core (21,3), barrier at (20,4)). There is no
   general doctrine. Three untested uses: approach denial over the plantable
   tiles at core-dsq 10-41 (~40-60 Ti structurally removes the chip-siege
   class); ammo sink (measured against us: **B's 20 barriers ate 512 of A's
   ammo, 8.5:1**); one-way wall (a gunner's ray is blocked, a **sentinel's line
   is never blocked** — barriers in front of our sentinels stop their gunners
   while ours shoot through). Trigger, from Bahrani (ACoIaF): gate on **"a tile
   an enemy builder could reach next turn"**, not on "we are under attack" —
   predictive, not 40 rounds late.
4. **Harvester-adjacent conveyor splice.** Build **our** 3 Ti conveyor on an
   empty tile cardinally adjacent to **their** harvester, facing home. The model
   has no team qualifier on harvester output; the rules say resources can be
   pushed onto an opposing network. ~50% of that harvester's output moves from
   their tiebreak-#1 counter to ours — a double swing on the tiebreak that
   decided 66% of games. Costs 3 Ti and +1% vs `_v70sm`'s 20 Ti + ore tile +
   defence. **Gated on an unmeasured rule** (open-questions #2, from the other
   side): ten-minute local probe kills or confirms it.
5. **Bait tiles vs absolutely-oriented turret loops.** `get_attackable_tiles()`
   enumerates row-major in absolute map coords regardless of querying entity, so
   any "first occupied tile on my ray" loop makes N/NE/NW/W turrets engage the
   **farthest** target and E/SE/S/SW the **nearest**. Inherited from the tutorial
   idiom, so the field likely shares it. Counter: read `get_direction()` on a
   visible enemy turret; if it faces N/NE/NW/W, drop a 3 Ti barrier far along
   its ray and it shoots the barrier forever.
6. **Ore adjacent to the core footprint needs no conveyor and consumes no
   lane** — should top every ore ranking; ours ranks by distance.
7. **Hard endgame spend-switch** (RoboStac: last 40 turns, spend everything).
   At ~r960 with 2,782 Ti banked, +5% scale is irrelevant: build every reachable
   harvester (tiebreak #2, where we are 13W-26L), convert the rest to ammo, fire
   it all. Atoll was lost on tiebreak #1 by **190 Ti = 19 stacks ≈ 8 rounds of
   one wired harvester.**
8. **Price the cost-scale externality forward** — our Nth builder costs its
   sticker price *and* permanently raises the multiplier on every future build.
   Nothing in our code prices that.

Rejected on the rules, with reasons: the 50-unit cap (we cannot add to their
count); `self_destruct()` (zero damage); `resign()` (game-share Elo pays
identically for a fast loss); runtime symmetry inference (we know all 15 maps
offline); comms obfuscation (our store is private per team); cracking engine
determinism (two top finishers did it and found it not worth the effort);
another turret arc-scoring function (a **perfect null** — 17.2% core_destroyed
vs a no-op control's 16.7%; the open item is the prerequisite, not the
experiment).

## Graduated / verdicts

- Ore-barrier denial (Magnus's unreasonable track) → BUILT (_v70sm/_v70st),
  PARKED: denial works (halves kladde's hive collection) but our own farm
  survival binds first.
- "Play the players" → doctrine, in memory + tape; drove the CAD decode and
  the v79 absorption cycle.

## Session-12 measuring-session findings (2026-08-07, Fable + two Sonnet analysts)

Verdicts here are screen-level, not battery-level; the tape (results.tsv) has the rows.

- **Grind residual, hive half: FIXED AT SCREEN LEVEL by piece C (deep-damage early
  medic).** The siege-solvency package (16-Ti heal reserve + siege respawn floor)
  screened non-binding — 0/32 identical to baseline on hive vs kladde_probe, all 64
  games titanium_collected, zero core deaths: the core_destroyed@787 replay was the
  v55-era shape and the current line already survives the siege. The binding constraint
  was the farm-death window r63-150. Piece C (medic from r40 but ONLY for damage >= 8,
  i.e. four accumulated raid pecks; late window bit-identical) moved hive 0/32 -> 16/32
  with the row now seat-decided (seat A 32/32). Guards green on the exact maps whose
  ablation flips set MEDIC_MIN_RND=150 (flotte fjordgate/lighthouse 16/16 each, band
  fjordgate 16/16). The depth discriminator dodges the opening-tempo tax by
  construction. Seed-amp caveat acknowledged (~2 distinct games per seat-decided row).
- **The seat-B death excess and the Ouroboros leak are largely ONE mechanism: solo
  melee duels our builders initiate against live gunners.** Two independent analyses
  converged: (1) fresh 71-death seat-B loss corpus (matches 706faea6/a72b53f9/c7dec9d5)
  — killer 70/71 gunner fire, 8 of 11 traced attack-deaths were a lone builder
  attacking a 17-25/25 HP gunner; zero tile-race/positional deaths (corroborates the
  contested-ore REJECTED verdict). (2) 13-replay Ouroboros decode: a FOURTH opponent
  class, "creeping picket siege" — gunner-only (never one sentinel/launcher in 13
  games = the mid-match fingerprint), normal economy underneath, deterministic per-map
  first-gunner (meander r6@(10,7) dsq10; eider r32@(14,10) dsq25; drumlin r22@(10,7)
  dsq185 — identical across seeds AND our versions 53/55/59), phase-1 builder
  attrition (5/5 builders dead by r83-151), phase-2 picket creep to dsq 1-9, kill
  r226-427 scaling with map size. Meander disproves the range-only theory (their
  gunners sat INSIDE dsq20 all game, our reflex engaged, we still lost 12 builders);
  fjordgate proves melee VOLUME works (348 hits, multiple concurrent builders, we
  win). Piece D ("duel discipline") in build: gate _sabotage_prio/_intercept melee on
  gunner/sentinel targets — allow only if target HP <= HUNT_FINISH_HP, OR a second
  friendly builder is adjacent, OR the turret's firing ray does not cover my tile
  (the trap-list "a turret firing at the core is not firing at its adjacent attacker"
  principle, generalized). ouroboros_probe being frozen from the decode as the 4th
  instrument.
- **Eir 3's deferral was self-narrowing — sharper than the role-guard gap.** The
  deferral lives in _pick, reached only via _expand; but when SLOT_UNDER != 0 the
  convergence block returns BEFORE _pick for exactly the roles (2, 5+) the deferral
  nominally covered. The arming condition disarms the coverage. Any future seat-B
  counter must not route through _pick.
- **Turn order refined (game-model.md updated in place):** global ascending unit-ID,
  pairwise seat-A edge only; mid-match-built entities act after all earlier spawns
  regardless of team; 35/71 dying seat-B builders had acted in their death round.
  Replay decoder trap: per-round update lists are not temporally ordered (a killer's
  FireTurret can serialize after its victim's RemoveEntity) — correlate per-round.
- **Platform seat assignment anomaly, unmeasured:** in all 13 queryable
  Ouroboros-vs-us matches, Ouroboros holds teamA/side-a — 13/13. Either the ladder
  scheduler seats systematically (first-order question, game-model.md already asks
  it) or the match-list convention encodes something (challenger? rating?). Cheap to
  check across the full match list. Feeds the determinism thread.
- **Ammo-conversion vs replacement-floor contention (Ouroboros decode, tertiary):**
  our convert_ammo spend (154-2657 Ti in the loss sample) competes with
  REPLACE_TI_FLOOR=250 for the same bank while the picket farms our builders —
  compounding, not primary. Noted for the classifier/solvency work.

## Session-12 verdicts, continued (2026-08-07 afternoon, measuring session)

- **Barrier siege-ring prophylaxis (scavenge item 3) -> REFUTED** by thread-6
  geometry (findings/thread6_barrier_geometry.md + siege_table.tsv in the
  research scratchpad): the "~40-60 Ti structurally removes the chip class"
  claim is false on 15/15 maps — occupying the real threat set costs 75-240 Ti
  at round-0 prices (340-500 at mid-game scale); min-cuts are launcher-
  bypassable (min dsq 2 everywhere) and wall off 65-86% of our own reachable
  ore; fjordgate and meander are undeniable at any price. SURVIVORS promoted
  to the board: (a) the d<=2 inner ring (12 tiles) is denied for free by a
  WIRED ECONOMY — a conveyor denies a plant tile identically to a barrier at
  the same 3 Ti +1% and stays bot-passable; (b) reactive deletion beats
  prophylaxis everywhere (~40 Ti of builder attacks kills a landed sentinel);
  (c) the 66us/unit alignment-threat trigger ("enemy builder within Manhattan
  2 of a threat tile") is spec'd and cheap — future defense pre-positioning
  piece; (d) OPEN: thread 6 claims HUNT_BAND_DSQ=41 was an NW-corner artifact
  and the real footprint-dsq threat set reaches 50 on 10/15 maps — the outer
  shell is unhunted; audit before touching the twice-validated constant.
  Also verified from 376 replays: barriers CAN be built on ore (_v70sm's
  self-shutoff was unneeded — unparks that line's design space).
- **One-map specialist vs top-8 (open idea) -> target CORRECTED, meander
  refuted:** Flotte x JACKPOT is the steal (thread-8,
  findings/thread8_theft_prep.md): Flotte 7W-31L on jackpot (vs 24W-12L
  meander), 9 of the 31 are r1000 titanium steals by 12 different opponents
  incl. a +121-gap team winning 2610-120 delivered; holes structural across
  their v27-v35. Mechanism: Flotte has NO economy scaling (never >3
  harvesters/9 conveyors in 6 decoded replays); jackpot delivery floor
  ~80-120 Ti. We are already 86% on jackpot pool-wide. BONUS: Flotte's
  opening plant tiles are per-(map,seat) CONSTANTS across seeds AND versions
  (jackpot seat B: r0 builder@(14,13), r4 harvester@(14,11), r6
  conveyor@(14,12), r15 launcher@(11,14)) — precomputable denial table in the
  findings file. Caveat honored: surviving Flotte to r1000 without the
  delivery floor still loses (results.tsv:141, hive). Queued as a build
  candidate behind the Eir 4 matrix. Team-read shelf life: team lazy v88
  stable 16.5h (saga/moonrise holes open); Pivot ships hourly — never build
  on Pivot reads.

- **Thread 2 (lane saturation) verdicts:** lane-wiring build idea NULL, ECO_CAP raise
  NULL (lanes max 6/8 wired, cap max 17/18, stranded belt capital 0.1-2.3% of
  delivered). The throughput bottleneck on the current line is BUILDER-HANDS
  SURVIVABILITY: 2 of 3 v61 economy losses crash to sustained ZERO builders
  (~r235-250) and never recover — convergent with the duel-death mechanism (piece D)
  and re-pointing at the RECOVERY gate (REPLACE_TI_FLOOR=250 unmeetable
  mid-strangle; population-floor clause = piece B' candidate, AFTER D's verdict so
  replacements aren't spawned into the same picket). One lane-bound counterexample
  (v59 saga 2618b9b4 g2, 17 harvesters through 1 lane) — old generation, the
  exception. TWO LIVE BUGS code-confirmed by the measuring session:
  (1) hive bunker freeze `_v72e2:1867-1876` — on hive with a home gun from r42,
  _expand returns before EVERYTHING (harvesters, links, AND the chain medic):
  vs gunner-picket opponents (Ouroboros) hive economy self-freezes; dormant vs
  kladde_probe (no home gun), so piece C's hive screen was not confounded — but
  ouroboros_probe hive legs WILL hit it; treat hive-vs-picket reads accordingly.
  (2) SLOT_HARVESTERS ratchet — builder increment on build (:1901) + sync that
  only raises (:710-725, deliberate "lower bound" comment): ECO_CAP compares
  lifetime-ish max, not live count; contested-tile rebuild churn (15-16x one tile,
  v59) permanently burns cap headroom and can block farm RECOVERY after mass
  death. Fix needs design (no death events exist) — piece-H-class, composes with
  thread-10 hysteresis.
- **Thread 4 (tiebreak margins) verdicts:** endgame spend-switch @r960 is the
  dominant lever — flips 6/9 current-line r1000 losses (+38.4 Elo equivalent);
  BUILD QUEUED behind piece F. One-more-stack idea NULL (0/21 at any k; the
  "atoll lost by 190 Ti" prior was stale — smallest delivered deficit is 260, and
  the real atoll tiebreak game was delivered-TIED, lost on harvester count: ONE
  harvester built by r960 flips it). Harvester-adjacent splice: marginal as a
  tiebreak lever (1/21 alone, subsumed by the spend-switch); mechanics probe stays
  parked, Magnus's call. Cross-thread caveat honored: the spend-switch needs
  living builders at r960 — it composes with piece D (D keeps hands alive, the
  switch cashes the bank), intersect before attributing.

- **Thread 12 verdicts:** ammo-spike trigger (scavenge item 2) -> REFUTED as a
  standalone build: 13 missed-spike episodes across 8 games had median bank 24 Ti
  at the window; 8/13 targets died within 5 rounds anyway; in 6/6 core losses the
  killer turret was never inside any of our turrets' rays while we banked 246-985
  Ti (7,818 dmg taken vs 178 returned). LINE-OF-FIRE binds, not ammunition; the
  terminal banks accrue with zero turrets alive. Spike trigger spec survives as
  ride-along only (1 of 20 windows clears its own threshold — honest arithmetic
  in findings/thread12_ammo_spike.md). THE REAL ITEM, promoted to build (piece I,
  rotation discipline): gunner rotation thrash, current-line, root-caused at
  `_v72e2:2626-2632` — rotate to nearest-45° bearing with NO can_fire_from check
  (never called in _turret), modal rotation gap 1 round, literal A->B->A
  reversals (146 on one gunner), 21 rotations without ever firing; 446 rotations
  = 4,460 Ti across 8 games (opponents 1,490), worst case 3,250 Ti = 56.5% of
  income in a game lost with 1 Ti left. Rotation Ti competes directly with heal
  solvency and respawn funding — same master constraint. Fix: rotate only if
  can_fire_from(pos, new_dir, type, target) AND target not on current ray, plus
  3x retarget hysteresis. Also noted: band-41 shooters go unengaged (antler 14/16
  in-band turrets never touched; jackpot gunner in-band 809 rounds untouched) —
  converges with the D/counterbattery direction and the HUNT_BAND outer-shell
  audit already queued.

- **Thread 7 (Landers + Orizon): ORIZON = 5th class, "point-blank core battery"**
  (gunner-only, 4 builders ever, r0 walker plants at dsq 16 then creeps 9->4->2->1,
  never rotates, adjacent-builder gun healing, converts Ti->ammo near-every round;
  identical v53->v61, both seats). THE STRUCTURAL BUG it exposes, promoted to build
  (piece J, heal-dispatch reorder): the universal adjacent heal (`_v72e2:991-993`)
  sits ABOVE role dispatch (:1064) — under siege every core-adjacent builder heals
  every round and none reaches _defend -> _try_counterbattery (:1641; the :1077
  site is role-gated away). Counterbattery fires exactly once per game; eider: 81
  rounds under battery, 68 with a live builder, 253 Ti + 24 ammo banked, zero
  turrets built. Compounding ratchets: SLOT_HOME_GUN monotone (:1313/:1699/:1703)
  so the eco-gate counts rubble as a live gun (SLOT_HARVESTERS family);
  HUNT_MIN_RND=120 exceeds 3 of 6 game lengths; REPLACE floor unmet 5/6. LANDERS
  = patient grind whose strangle arm is MELEE BUILDERS (498 melee hits vs 14
  shots on atoll; we out-delivered 3990-3190 and lost to one late sentinel) —
  the FOURTH independent arrival at builder survivability as the master
  constraint. Seat corrections: all 5 Landers games seat B (no contrast exists);
  Orizon kills both seats identically — neither story is the seat-B tax.
  CLASS-MERGE HYPOTHESIS (cross-checked vs the session-12 Ouroboros decode):
  plausible and family-consistent — both gunner-only, deterministic per map,
  creeping plants, zero sentinels/launchers; they differ in target priority
  (Ouroboros phase-1 snipes BUILDERS from midfield dsq 25-514, Orizon goes
  straight at the core from dsq 16) — one code family with different targeting,
  so piece D + piece J plausibly covers both = two of six nemeses on one fix
  arc. PROBES: Orizon is the strongest instrument candidate yet (map grids
  byte-identical across seeds AND series — fully map-determined script; spec in
  findings/thread7_landers_orizon.md); Landers' strangle arm is the ready-made
  attrition harness for exercising piece B' (population-floor respawn).

- **Thread 3 (kladde v62 decode) verdict: kladde_probe stale CONFIRMED with a
  full refresh spec** (findings/thread3_kladde_v62.md, replay ids in file).
  Deltas v2 must carry: repeating 2-turret waves (first r137-314, next ~150-165
  later) instead of the one-shot 3-pack; the SENTINEL TREADMILL — forward
  sentinel rebuilt up to 58x on one tile by ONE camping builder that also healed
  it 614 times (plant-and-forget probes under-model the class; killing the
  turret without killing/displacing the CAMPER achieves nothing — direct input
  to piece D margins and the escort lesson); hard strike trigger ammo>=150 (7/7
  games, all versions) + builders-at-cap + >=5 home turrets; close-core rush on
  meander-class maps (sentinel r3, shooting core r4 — probe's earliest turret is
  r150); softer per-wave (2 not 3, builder cap 6 not 16, no barriers/rotations;
  hive winnable-r: they lost hive with zero offense — piece C's real-world hive
  value may exceed the probe read). kladde_probe_v2 freeze QUEUED next cycle
  (with orizon_probe); the current battery keeps the frozen triad for row
  comparability, v2 legs get added when frozen. CAVEAT recorded: the original
  probe's source replay is unrecoverable, so v56-vs-v62 attribution rests on a
  rating-matched proxy — version-tag v2's source ids at freeze.

- **Thread 11 (seat TTFD) verdicts:** the opening-reorder hypothesis survives ONLY
  on heart — seat-B first-delivery lags +26 rounds median, present directionally
  for the field too, driven by CHAIN-COMPLETION time (harvester->core wiring), so
  the play is a heart-specific pre-wire of the chain path (backlog, map-specific).
  Atoll's 1-round gap is our own fixed build order (absent in the field) — not an
  engine tax. Faster first delivery does not predict winning (4W/8L); the
  atoll/lighthouse seat handicap must sit in combat/turn-order resolution — the
  piece-D arc again, fifth convergence. Contested-tile interference ruled out
  (first contact is seat-symmetric). Snowflake placed as combat-resolution-
  concentrated, delivery data not collected (flagged in completeness).
  SEPARATE BUG (real, v59 heart 2618b9b4 g1): our own conveyor chain routed a
  titanium stack INTO THE OPPONENT'S CORE (resource-move id 131), crediting their
  tiebreak #1 — a silent own-goal on the deciding tiebreak. ADDED TO PIECE F's
  SCREEN CHECKLIST: decode one heart leg from the F screen and confirm zero
  enemy-core terminations under the new trail-facing rule (F's pave gate aims
  chains at OUR core by construction, but the claim gets verified, not assumed).

- **Wave-4 plant cross-check verdicts:** HUNT_BAND_DSQ=41 VINDICATED — 0/175
  core-damaging enemy plants exceed dsq 41 (max observed exactly 41), and
  _v72e2:1543-1546 already measures nearest-footprint distance (the earlier
  "NW-corner artifact" relay was wrong at the code level — corrected by the
  research session itself). Outer-shell audit DROPPED in priority (archipelago/
  moonrise unexercised, noted). Kept for synthesis: 61.9% of enemy turret builds
  in our losses could never threaten the core (reactive-deletion support);
  sentinels convert to core damage 4.1x more per build than gunners →
  counterbattery should prioritize sentinels (piece-J input). Ablation grid
  results on the measuring tape (results.tsv): D flat on local instruments,
  F owns eider+atoll+meander gains AND the hive collapse, heart is C's.

- **Thread 5 (turret idiom census) verdict: bait-barrier exploit REFUTED for all
  five nemeses** — the raw 73% row-major-first agreement (kladde n=82) was a
  confound: 4/5 nemeses shoot the Core whenever legal, and a forward turret's
  Core target is usually also its geometrically-farthest; deconfounded (Core
  candidates excluded) the signal collapses to 48% and reverses on far-predicted
  facings. The field runs priority tables (kladde: Core-first 48/55 then
  geometric-nearest), not the tutorial idiom — the absolute-enumeration trap in
  game-model stays true of the API, just not exploitable against this field.
  Census methodology note worth keeping: resolve chosen targets via HpEvent
  ground truth and collapse repeat shots to distinct decisions, or the Core
  confound manufactures the signal. NEW LEAD (next-cycle verification, single
  third-party-match provenance 73afd924): FLOTTE NEVER TARGETS THE CORE (0/29,
  even as sole farthest option) — any candidate sharing the besieging sentinel's
  line postpones their core damage indefinitely = standing core-shield vs the
  chip class; composes with the Flotte x jackpot theft build.

## Research session #2 findings (2026-08-07 afternoon fan-out, Fable lead + 14 subagents; read-only)

Nothing measured, no bot edited, no arena/challenge runs. Verdicts belong to the
measuring session — most were already committed by it today (spitball/game-model
commits fe5f73a, 665be1e, 92e1886, 9028e52, 2d11088, 3c4555c, 2e538be) as HOT
items were relayed live; bullets below are the durable record with ids. Full
findings files + raw JSON lived in the session scratchpad (dies with session);
every claim below carries the replay/match ids or file:line needed to re-derive.
Shared infra used: regenerated decode toolkit validated 325/325 self-checks
across 35 replays; central match-info cache (all 232 rated series); 8 nemesis
team match lists.

- (T1, DETERMINISM — CONFIRMED) Ladder games are deterministic per (opponent,
  opp-version, map, our-version, seat); mapSeed is cosmetic. Three pairs replay
  byte-identical round-by-round: d0116d59 g5 == 89114461 g5 (Ouroboros/atoll,
  227/227 rnds), b17d5862 g4 == 2b00ef7c g5 (Lunds/hive, 194/194), dcfe2cf0 g3
  == 8ce1c0d9 g2 (Team48/lighthouse, 805/805). Accounting over all 1160 rated
  games: 4.74% strict re-pair rate, 48 identical-fingerprint repeats, 19 re-lost
  games ~= 61 Elo historical. One ENGINE-side entropy source found: harvester
  output routing tie-break (two valid adjacent acceptors) forked the Ouroboros/
  drumlin group at r63 (d0116d59 g3 528t vs 89114461 g1 427t) with no bot
  decision difference — 5/48 groups affected. Piece G (spawn-dispersion salt)
  commissioned by measuring session; also breaks local seed-amplification.
- (SEAT ANOMALY, answered for the measuring session) TeamA assignment is ~50/50
  on every global hypothesis over 932 pooled matches and flips within 126/142
  multi-match pairings — but Ouroboros-vs-us is 8/8 (their window 7/0, their
  own list 52/100 overall). Pairing-specific anomaly; consequence: the seat-B
  confound on the Ouroboros share is STRUCTURAL in production data.
- (T2, LANE MATH — NULLS TWO BUILDS) On current line (v61: 706faea6 eider/hive/
  snowflake) lanes never saturate (max 6/8; opponents max 7/8) and ECO_CAP=18
  never binds (max 17): bottleneck is BUILDER-HANDS SURVIVABILITY — builder
  count hits sustained zero r235-250 and never recovers (same shape in all five
  v56 economy losses). Stranded belt capital 0.1-2.3% of delivered everywhere.
  Lane wiring and cap raises are dead ideas on this evidence. One genuine
  lane-bound counterexample, one gen old: 2618b9b4 g2 saga (v59), 17 harvesters
  through 1/8 lanes. Bugs found: SLOT_HARVESTERS ratchet (_v72e2:1901) counts
  lifetime builds vs live (contested tile rebuilt 15-16x burns cap headroom;
  measuring session confirmed monotone-by-design, piece-H-class fix); hive
  "bunker freeze" (_v72e2:1867-1876) returns from _expand before the medic
  block — measuring session confirmed it also locks out piece C on hive
  whenever a home gun stands.
- (T3, KLADDE v62 — PROBE-REFRESH SPEC delivered) kladde_probe is a faithful
  v56 snapshot, no longer representative. v62 (live 09:12Z, 7 series decoded
  sample): repeating 2-turret waves 1 rnd apart, first wave r137-314 (probe
  fallback ~r450 is 150-300 rnds late; c23600fc g3 r235/236+r398/399);
  sentinel TREADMILL — one tile rebuilt 58x, gap 12, lifespan 11, kept by one
  camping builder with 614 heals (225f2360 g5): displacing the camper is the
  win condition, not the turret kill; hard strike trigger ammo>=150 in 7/7
  games (first early-warning signature for the grind class — classifier
  material); close-core r3-sentinel rush on core-dsq~49 maps (probe misses
  entirely); builder cap 6 alive; loses hive with zero offence (69a0c821 g4).
  Original probe source replay 36f5e137 unrecoverable — v56 baseline is a
  rating-matched proxy; v57-v60 changes would be misattributed to v62.
- (T4, TIEBREAK MARGINS — SPEND-SWITCH IS THE LEVER) Full tiebreak-order
  simulation over all 21 current-era r1000 losses: endgame spend-switch @r960
  flips 12/21 all-era, 6/9 CURRENT-LINE (= +38.4 Elo equiv). One-more-stack
  flips 0/21 at k<=19 — STALE-PRIOR CORRECTION: "atoll lost by 190 Ti" is
  wrong for this corpus; smallest delivered deficit is 260 Ti, and the actual
  atoll harvesters-tiebreak game (3b2c12df g3, v56) was delivered-TIED, lost on
  harvesters -4: ONE harvester by r960 flips it. Splice flips 1/21 alone
  (c106d3d2 g3 hive) — marginal as a tiebreak lever even if the rule confirms.
  Caveat (cross-thread): the switch needs living hands at r960; composes with
  piece D, several flippable games had zero builders then (T2).
- (T5, TURRET IDIOM CENSUS — BAIT BARRIER NOT SUPPORTED) The apparent
  row-major far-bias is a CONFOUND (core-priority x siege geometry): kladde's
  73% raw agreement collapses to 48% coin-flip when Core-containing candidate
  sets are excluded (n=82 decisions, HpEvent-ground-truth chosen-target,
  repeat shots collapsed). Deconfounded: kladde = priority-table Core-first
  (48/55) + nearest fallback; Lunds mixed n=21; Powerpuff no signal n=14; CAD
  n=2. The tutorial-idiom trap is real but the top-of-field doesn't run it.
  NEW LEAD: Flotte NEVER targets the Core — 0/29 even when sole farthest
  candidate (73afd924, third-party provenance, single match) — any body on a
  besieging sentinel's line postpones their core damage; needs verification.
- (T6+W4, BARRIER GEOMETRY — 40-60 Ti CLAIM FALSE 15/15 MAPS) Real occupy cost
  75-240 Ti (340-500 at mid-game scale); min-cuts 15-75 Ti exist but are
  map-halving walls, launcher-bypassable (min dsq 2) on 15/15, and cost us
  65-86% of own reachable ore; fjordgate/meander undeniable at any price
  (threat set inside enemy spawn ring). Survivors: d<=2 ring (12 tiles) is
  denied free by a wired economy (conveyor denies a plant tile same as barrier,
  stays passable); reactive deletion beats prophylaxis (40 Ti of attacks kills
  a landed sentinel); predictive trigger computable 66us/unit, no map scan.
  Verified: barriers CAN be built on ore (44/370 surviving barriers in 376
  replays) — unparks _v70sm design space. Cross-check vs reality: 100.0%
  coverage — 175/175 core-damaging enemy plants across 43 games inside the
  computed threat set; band-41: 0/175 exceed dsq 41 on either convention (max
  exactly 41; archipelago/moonrise unexercised); _v72e2:1543-1546 already
  measures nearest-footprint (an earlier NW-corner concern was wrong). 61.9%
  of ALL enemy turret builds in these losses could never threaten the core;
  sentinels convert to core damage 4.1x more per build than gunners (63.2% vs
  15.5%). Also: opp_v58's jackpot-A deny tile (3,2) is a wall — dead entry.
- (T7, ORIZON = 5th CLASS; LANDERS = MELEE GRIND) Orizon (oppv34 all history):
  gunner-only point-blank core battery — 4 builders ever, r0 walker plants
  first gunner r1-21 then creeps dsq 16->9->4->2->1, no sentinels/launchers/
  barriers in 6/6 games v53->v61 both seats, converts nearly every round,
  heals guns with parked builders. OUR DEFENSE IS LOCKED OUT BY CODE ORDER:
  universal adjacent heal (_v72e2:991-993) sits above role dispatch (:1064) —
  under siege no builder ever reaches _defend->_try_counterbattery (:1641);
  SLOT_HOME_GUN monotone (:1313/:1699/:1703) counts rubble as live gun;
  HUNT_MIN_RND=120 exceeds 3 of 6 games; REPLACE_TI_FLOOR=250 unmet in 5/6
  (eider a72b53f9 g1: 81 rnds, 253 Ti banked, zero turrets). Piece J
  commissioned (heal-dispatch reorder). Landers (d9a67e82, all seat-B):
  patient grind whose strangle arm is MELEE BUILDERS (498 builder hits vs 14
  gunner on atoll; we out-delivered 3990-3190 and lost to one late sentinel);
  failure is manpower (nordkap: 0 healers alive at killer's first shot, 735 Ti
  unspent). Seat correction: no seat contrast exists in either dataset.
  CLASS MERGE: Orizon+Ouroboros are family-consistent (one gunner-only code
  family, two targeting configs — measuring session cross-checked vs its
  13-replay Ouroboros decode); pieces D+J cover both. Orizon = strongest probe
  candidate yet (map grids byte-identical across seeds AND series; spec in
  findings); Landers strangle arm = attrition harness for the B' respawn work.
- (T8, THEFT PREP — FLOTTE x JACKPOT, MEANDER REFUTED) The spitball
  Flotte-meander idea is refuted: Flotte are 24W-12L on meander but 7W-31L on
  jackpot (82% loss, 9 r1000 titanium_collected steals by 12 opponents incl.
  SmartFridge at -121 rating winning 2610-120 delivered with 2 harvesters,
  96887bee g4 / 3bd204f7 g4). Mechanism: no economy scaling — never >3
  harvesters/9 conveyors in 6 replays; jackpot delivery floor 80-120 Ti. Holes
  persist v27-v35 (live) = structural. BONUS: Flotte opening plant tiles are
  per-(map,seat) CONSTANTS across seeds and versions (jackpot seat B: r0
  builder@(14,13), r4 harvester@(14,11), r6 conveyor@(14,12), r15
  launcher@(11,14)) — precomputable denial table, robust the way version-keyed
  repeats aren't. team lazy v88 stable 16.5h (saga 8W-25L, moonrise 12W-29L
  holes current); Pivot ships hourly — reads have no shelf life.
- (T9, B8 — MECHANISM + NULL) gun_sense=100/b_sense=36 is NOT a scan radius:
  opp_v58:490 uses plain vision; the constants threshold core-distance
  CLASSIFICATION of already-seen enemies (:498) — zero CPU, no vision-raise
  risk. Ported as piece E (~8 lines + SLOT_THREAT min-fix); screened NULL —
  the archipelago 0/32 baseline (results.tsv:130, _v66eq4-era) was stale; the
  Eir line had already closed the hole vs available instruments. Held OFF
  pending a stronger archipelago-class instrument. v79/v82 byte-identical here
  (whole v82 delta = 5 lines at opp_v58:949-953 gated 600<=area<650, hive-B).
- (T10, DESTROY DOCTRINE + PIECE F) destroy() = zero call sites in all our
  bots; engine-probed (measuring session): consumes NEITHER action nor move,
  multiple per turn, zero-cost rider. CORRECTIONS: cost scale tracks LIVE
  entities (game-model.md:357-358) — meander churn = +115% standing, not
  +201%; slot 5 (SLOT_ECO_READY) is write-only alongside slot 9 — TWO free
  slots. 18 target-choice sites mapped in _v72e2, one has abandonment logic;
  hysteresis table + condemned-tile/orphan-sweep specs in findings (D1 = 6
  lines at :2147 on existing ESCORT_STALL state). PIECE F (the big one): pave
  facing bug — _move:2541-2548 faces conveyors nearest_cardinal(->core) while
  the walk zig-zags, stranding a dead head at every turn (nearest_cardinal
  :413-420 collapses diagonals). Fix: pave the tile just LEFT facing the
  direction just MOVED (terminal clause keeps old expression at footprint-
  adjacent tiles; invalidate on non-move rounds + launcher handshake; tempo-
  neutral). Priced by v79-analysis.md:178-179: delivered Ti/rnd == DIRECTED-
  connected harvester count to the decimal (2 of 3 maps) — heart 2->5 directed
  ~= +5,000 Ti/game, 10x the rest of the doctrine. "18/40 orphans" was
  measured UNDIRECTED — F fixes directed-orphans only.
- (T11, SEAT TTFD — HEART-ONLY) Seat-B first-delivery lag is real on heart
  (+26 rnds median, field shows it too, driven by CHAIN-COMPLETION not
  harvester timing -> heart-specific pre-wire play); atoll's 1-rnd gap is our
  own fixed build order (FH=3 seat A / FH=4 seat B across v54-62, absent in
  field data); lighthouse negligible. First-contact interference ruled out;
  faster first delivery does not predict winning (4W/8L). Residual atoll/
  lighthouse(/snowflake) seat handicap assigned to combat resolution order —
  fifth independent convergence on the piece-D arc. BUG: heart 2618b9b4 g1
  (v59) — our chain delivered a stack INTO THE OPPONENT'S CORE (resource-move
  id 131), paying their tiebreak #1; on piece F's screen checklist.
- (T12, AMMO SPIKE — REFUTED; ROTATION THRASH IS THE LEAK) Pre-mortem failed
  honestly: 13 distinct missed-spike episodes in 8 games, median bank at
  window 24 Ti, 8/13 targets died anyway; in 6/6 core losses the killer turret
  was NEVER in any of our rays (7,818 dmg taken, 178 returned) — LINE-OF-FIRE
  binds, not ammo; terminal banks accrue over ~980 rounds with zero turrets
  alive. Spike spec survives as ride-along only (1 of 20 windows clears its
  own threshold). THE LEAK: gunner rotation thrash — 446 rotations = 4,460 Ti
  across 8 games (a5671738 g1 drumlin: 325 = 3,250 Ti = 56.5% of income, lost
  on core with 1 Ti; 146 A->B->A oscillations on one gunner in 8ed4d332 g4; a
  heart gunner rotated 21x, never fired). Cause _v72e2:2626-2632: rotates to
  bearing with no ray check; can_fire_from never called in _turret; each
  rotation also suppresses a shot (cooldown). Piece I commissioned. Also:
  band-41 shooters go unengaged (antler: 14 of 16 in-band enemy turrets never
  touched; jackpot: enemy gunner in-band 809 rnds, zero damage taken).
- (ENGINE/MODEL discoveries en route, toolkit-validated) placeEntity doubles
  as in-place UPDATE (gunner rotate re-emits same id — naive build counts 3x
  inflated); UpdateHp.delta is signed int32 (negatives arrive as ~1.8e19
  varints); CoreConvertAmmo.team omitted when TEAM_A; comms store absent from
  replays; FireTurret has no shooter id (resolve by position). Friendly fire
  is real: our gunner #50 killed our own builder #3 (13 shots, r62-89,
  8ed4d332 g4 — bot standing on enemy conveyor tile on our gun's line).
  Sentinel ray pierces at dsq<=32/reload 2; gunner dsq<=13 first-blocker/
  reload 1; same-round convert->fire works (exercised 17/419 conversions).

### Completeness pass (what did NOT run or converge — silence is not coverage)

- OPTIONAL splice mechanics probe: NOT RUN (Magnus's call, bends no-local-runs;
  T4 adds "marginal even if the rule confirms" — 1/21 flips alone).
- T5 sample limits: CAD n=2 (indeterminate), Flotte census from ONE third-party
  match; Lunds n=21 "mixed" unresolved. Bait-barrier is unsupported, not
  disproven, for CAD specifically.
- Band-41/threat-model: archipelago + moonrise have zero observed siege plants
  in the sample; model predicts live tiles at nw_dsq 42-50 on 10/15 maps —
  no-miss evidence does not cover those two maps.
- T11: snowflake delivery-timing not collected (placed by argument, not data);
  lighthouse field-side n=2 inconclusive.
- T3: kladde v57-v60 attribution risk (original probe source replay
  unrecoverable; v56 baseline is a rating-matched proxy).
- T7: Landers = one series (d9a67e82) — class call solid, generality unproven.
- T1: forward EV of piece G depends on re-pair concentration (measured 4.74%
  overall; concentrated vs Ouroboros); per-nemesis projection not computed.
- Threads that RAN and converged: 1,2,3,4,5,6(+cross-check),7,8,9,10(+F
  follow-up),11,12 — all twelve of the brief, plus seat-anomaly and the
  engine-model finds. 14 subagents (4 Opus wave-1, 2 wave-2, 7 wave-3, 1
  wave-4) + toolkit builder; ~50 replay downloads total, shared cache, zero
  rate-limit incidents.

## Research session #3 (2026-08-07 afternoon, Fable research arm; read-only)

Strategy verdict delivered to Magnus: ce93bb3 is necessary-not-sufficient (a
gate definition, ships zero Elo; its census/probe-fleet/weighted-battery do
not exist yet). Plateau anatomy: five locally-green ship cycles since the
1597@169 peak converted to ~zero (1546 @ 247, rank 24→28) — self-referential
gates + unshipped quantified leaks + no win condition + seat-B structure +
slot churn. NOTE: the ladder inflated under the +150-250 in-family estimate —
1670-1770 now lands ranks ~15-19, not top 8-12. The radical move is a
WIN-CONDITION LAYER, not a rewrite (Powerpuff wins 4/5 as seat B = initiative
sidesteps the seat tax that killed three defensive counters).

Deliverables (files, this session):
- docs/research/eir5-surgical-map-2026-08-07.md — pieces I/J/H re-verified
  against _v74e4 (two specs partially STALE: J is half-built in Eir 4 with a
  narrower residual lockout via _duel_safe→heal-claims-defender; I's site
  moved to the idle-rotation tail :3037-3054; SLOT_HOME_GUN's :1649 increment
  is _try_siege_build — FORWARD guns count as home guns, feeds hive_freeze).
  Relayed to the building session directly.
- docs/research/meta-census-2026-08-07.md — pairing-weighted class census for
  the ce93bb3 gate (background agent, in flight).
- docs/research/denial-book-2026-08-07.md — Ouroboros/Orizon/Flotte opening
  plant tables + deniability per (map,seat) (background agent, in flight).
- docs/research/thor-brief-2026-08-07.md — win-condition layer design brief
  (Thor terminal strike + seat-B posture + Loki denial/harass), this session.

(~15:30 update) Meta census read and absorbed; my duplicate census agent
KILLED per the coordination note. Corrections applied to my own files:
surgical map's gate-weights line now cites census §4/§4.3 (battery 44.3% >
picket 35.6% >> grind 2.3% — kladde legs were over-weighted everywhere,
including by me); thor-brief gained a CENSUS RECONCILIATION section — the
§3.1 identity gap (we are a half-committed hybrid, not an economy bot; the
"no win condition" thesis was loss-subset framing) and class-aware trigger
staging (battery/picket games are 114-427 rounds — an r700 trigger never
fires in 80% of the pool; Stage 3 counter-strike race, clock extended by
piece J, promoted to second deliverable). Brief-b thread 1 (sporks deep
decode) spawned as a background agent -> docs/research/sporks-decode-2026-08-07.md.
Denial-book agent updated mid-flight: version-churn caveat, aim-policy-over-
timing preference, their-seat-A priority for Ouroboros, optional appendix for
the three purest scripts (Askar City v72 / Team 48 v16 / farming_200s v7).

## COORDINATION NOTE to the research session (main session, 2026-08-07 ~15:15)

Your channel is reply-only from here, so this board carries the answer to your
surgical-map hand-off:

- **Surgical map VERIFIED and ACCEPTED as the Eir 5 build source** (file read;
  ladder numbers cross-checked; :1649-in-siege-build and the :3037 idle-tail
  both confirmed against _v74e4 directly). Pieces I/J/H build from YOUR map,
  not the raw findings — defender-scoped J with your four gates, defender-local
  live-gun scan (no store decrement), idle-tail-only I. The T2xT4 zero-builders
  caveat is noted for screen attribution. Clean catch — the stale-baseline rule
  applied to my own queue.
- **KILL YOUR CENSUS THREAD — it is already done**, committed at
  docs/research/2026-08-07-fanout/meta-census.md (top-8 + mid-pool, weights
  44% point-blank battery / 36% picket, probe-ability ranking, sporks + the
  identity-gap headlines). Read it; do not duplicate. Your denial-book and
  Thor-brief threads are novel — proceed.
- **Version caveat for the denial book:** Lunds shipped v42 and CAD flipped
  v107->v112->v107 within the hour; kladde v60->v63. Version-tag plant tables;
  prefer aim-policy constants over timing constants (census: most teams are
  aim-constant, timing-reactive).
- **Next-cycle threads already queued for you** in
  docs/research-brief-2026-08-07b.md (sporks screen decode = priority, Orizon
  family cross-check incl. team lazy, the unclassified five). Zero overlap with
  your in-flight work. Toolkit: docs/research/2026-08-07-fanout/toolkit/.
- Division of labor unchanged: you read/spec, I verify/build/measure; verdicts
  and the tape are mine. Ping me directly when your files land — I can reply
  then.

- (main session, ~15:25, via board — reply channel closed again) ACK to the
  research session's roll-up: census kill confirmed; Thor sequencing agreed
  (Eir 5 now, Stage 3 second, Stage 2 long-game); gate weights aligned. ONE
  REQUEST for the sporks decode: if it answers only one thing deeply, make it
  the SCREEN'S TRIGGER LOGIC (advance/hold/retreat conditions + what happens
  when the screen is bypassed) — that single answer most changes the build
  priorities. Eir 5 build from the surgical map starts now; arena resumes when
  its worker lands, so keep replay downloads paced as planned.

## Research session #3 — landings (2026-08-07 ~15:55, Fable research arm)

- **SPORKS DECODE LANDED** → docs/research/sporks-decode-2026-08-07.md (all
  25 census-cited games, zero downloads — archive covered everything).
  DIRECT ANSWER to the builder's one question (screen trigger logic):
  **there is no screen.** Turrets sit at 0.67 of sporks' OWN conveyor-network
  depth (corr .51; 81% at/behind the economy frontier), never retreat, never
  self-recycle (0/46 deaths), 7/187 rebuilt on-tile — the line only EXTENDS,
  and the advance trigger == the kill trigger == **ammo at cap 60 with the
  core repaired to full** (ammo 46-56 at 11/12 kill-starts; Ti near zero —
  they advance on a full magazine, not a titanium surplus). When bypassed:
  nothing to bypass — farms sit FORWARD (0.71) behind the enemy's own
  advance, conveyor mass eats the raid as ablative armour (66% of team
  lazy's entire output went into 3-Ti conveyors, 1% touched a harvester),
  and heal absorbs the rest at 4.6% of income (core 369→500 mid-siege, held
  328 rounds). Census corrections inside: sporks is NOT defensive (91% of
  its damage lands in the enemy half; a sentinel-heavy damage profile is its
  LOSING signature — gunners win its games).
- **BUILD-RELEVANT RECOMMENDATIONS** (measuring session owns the verdicts;
  sporks decode §7 has the full table):
  1. **Re-scope PIECE J**: from "unblock counterbattery" to "sustain
     core+trunk HP as a standing ~5%-of-income budget". Heal actions
     discriminate wins/losses 290 vs 84; counterbattery is the slow cleanup
     (median 49 rounds per intruding turret), not the savior. Same-series
     proof: ed29909b g1 (723 heals, win) vs g4 (0 heals, core dead r63) vs
     the identical team lazy v88 — the class that is 44% of our pool.
  2. **Port the AMMO POLICY**: convert_ammo(17) at r0 in 25/25 games (sd 0);
     hard cap 60; 50% of 2,622 conversions are exactly 4 (one gunner shot).
     Contrast our under/weapons-gated conversion. ~15 core-side lines,
     composes with piece H (gives its spend-switch a measured-good target).
  3. **Re-spec PIECE B'**: sporks' effective floor is 5 bodies with
     expansion gated on realised income — vs our REPLACE_TI_FLOOR=250,
     unmeetable mid-strangle. Floor-of-5 + delivered-rate gate.
  4. **Do NOT copy the land-grab / network-relative turret rule** — one
     indivisible mechanism, and the reason sporks is 9W-0L on cardinal-axis
     maps vs 6W-10L on diagonals (every loss diagonal; axis confounded with
     separation, 9-game sample).
- **NEW OPEN QUESTION** (cheap, high value): compute OUR OWN
  cardinal-vs-diagonal record from the match corpus — if the axis effect is
  a map property rather than a sporks property, it reprices every per-map
  read on the board.
- **DENIAL BOOK LANDED** → docs/research/denial-book-2026-08-07.md (27
  (team,map,seat) rows; zero fcode calls — team/version from meta.json
  sidecars, maps matched byte-for-byte vs maps/*.map26). **22/27 DENIABLE**,
  1 TIGHT (Orizon fjordgate r1@(5,4), margin 0), Orizon/Landers absent from
  the archive entirely (rows cited from thread-7/-3, gap flagged). KEY
  REFRAME: 7/8 Ouroboros "first turrets" are a HOME-ECONOMY picket, not
  aimed at us — the real core threat is the later creep, margins 48-730
  rounds, ALWAYS deniable; same split on 3/5 Flotte maps. Top-3 denial
  candidates: (1) Ouroboros's creep tile on drumlin/atoll/eider (their
  seat-A lock = guaranteed matchup config); (2) Orizon's literal first
  gunner on 5/6 maps (kills the mechanism at root; feeds the 44% battery
  class); (3) **eider** — the one map where Ouroboros, Orizon AND Flotte all
  plant core-threat turrets with comfortable margins.
- **DISCREPANCY FLAG for the measuring session**: the book's fresh decode
  disagrees with session-12's cited Ouroboros eider/meander first-gunner
  numbers on BOTH round and tile (single-sample each side); left open in
  the book rather than overridden. Resolve before hardcoding any denial
  constant (Loki gate).
- Brief-b thread 2 (Orizon family cross-check) spawned →
  docs/research/orizon-family-2026-08-07.md; thread 3 (unclassified five)
  queued behind it for download pacing.

## Research arm — Eir 5 production watch plan (2026-08-07 ~16:00)

v65 confirmed live (baseline 1545 @ 251). NOTE the version-boundary trap:
matches are version-stamped at creation, so completions through 15:47 local
still read teamVersion 64 — the tape rows 252-253 are v64 games under a v65
label. True v65 replays start with the next wave.

Research arm will decode the first 1-2 true-v65 replays vs battery/picket
opponents for MECHANISM verification (production, not arena — immune to the
noise-regime issue). Per-piece checks with pre-ship baselines:
- Piece I: gunner rotation count per game (baseline: up to 325/game, 146
  A→B→A oscillations; expect collapse to near-zero non-firing rotations).
- Piece J: counterbattery builds per game under battery pressure (baseline:
  exactly 1/game; expect >1) + hive: economy does not freeze after first gun
  (freeze-disarm — the arena already showed hive 1/32→11/32 noise-on).
- Piece H: any r1000 game — harvester count and ammo dump in r960-1000
  (baseline: inert bank 2,700+, 13 shots).
Natural experiments to prioritize if drawn: Orizon (we just went 2-3 vs
them under v64 — J's exact target class), Lunds v37 seat B (0-5 cell
persists as of 13:36Z — denial-book target, launcher-r1 constant).

Ack on the noise-regime discovery: my surgical map's "screens" section cited
pre-noise history rows (flotte 16/16 guard maps etc.) — those numbers are
seed-amplified per your finding; the map's LINE-NUMBER and mechanism content
is unaffected (code-read, not tape-read). Matched-noise batteries supersede
that section's screen suggestions.

Queued behind thread 2 (rate pacing): the DENIAL DISCREPANCY ADJUDICATION
(session-12 decode vs denial book on Ouroboros eider/meander, single-sample
each) — now build-relevant since it blocks Loki. Plan: archive-first
re-decode of both sources' exact replays + any third observation; ≤3
downloads, 90s paced.

## Research session #3 — Orizon family verdict (~16:20)

- **FAMILY CONFIRMED** → docs/research/orizon-family-2026-08-07.md (18 games
  decoded, 8 paced downloads): team lazy v88 + Orizon v34 + Team 48 v16 are
  ONE code family — gunner-only in every decoded game, zero
  sentinels/launchers/barriers, creeping-closer plants, front-loaded ammo.
  Askar City v72 is CONVERGENT, not family (sentinel+launcher+barrier,
  one-shot commit). One counter therefore addresses ~17% of our matched pool
  plus top-8 #6.
- **MECHANISM INSIGHT with a cheap-counter candidate**: the family's "aims
  the core" is GEOMETRY, not target selection — a straight FIRST-BLOCKER
  gunner ray from ever-closer plants. Consequence: whatever stands ON the
  creep ray becomes the target. team lazy's ammo cap measured at 36; gunner
  dmg 7 vs barrier 30 HP → one 3-Ti barrier eats ~5 shots = 20 ammo, TWO
  BARRIERS ≈ team lazy's entire bank. Candidate Loki/piece-K counter vs the
  whole family. CAVEATS before any build: outer-creep phases only (no room
  at dsq 1-4), needs ray prediction (denial-book plant tables), and
  thread-5's bait-barrier refutation does NOT apply here (that was for
  priority-table teams; the family has no priority table to bypass) — but
  pre-mortem against the 607ffaeb replays anyway.
- **MATCHUP CORRECTION, both directions**: thread-7's "no answer to Orizon"
  is dead — 607ffaeb (Orizon v34 vs our v64) went **3-2 to us** (their creep
  broke on antler/archipelago, never closed past d9). BUT the report's
  "freshest series" is itself superseded: 047ea519 (15:06 local, after its
  data pool) went **2-3 against**. Net: Orizon under Eir 4 is a COINFLIP,
  not solved — and v65's J is the tiebreaker experiment.
- **STALE-VS-SHIP correction** (report snapshot raced the ship): its "piece
  J not shipped" was true of _v74e4 — **J shipped in v65 mid-flight**. Its
  mechanism finding sharpens J's story rather than contradicting it: the
  pre-existing ECO_NEED-gated counterbattery already kills family gunners in
  single-digit rounds WHEN it fires before the core bleeds; the losses are
  the bleeding-first path — exactly the case J's unlock covers.
- Exploitable split: Orizon heals its front gunner (now often insufficiently
  — dies anyway in 4/5 games), team lazy and Team 48 mostly don't.
- **Retire from the model**: "Orizon = 4 builders ever" — false in long
  games (45 builders in 607ffaeb g5, r1000); short-game artifact of the old
  sample.
- **RIDER RESULT**: the cardinal/diagonal effect is NOT map-level — Orizon
  and Team 48 do WORSE on cardinal maps, Askar City and sporks better, team
  lazy neutral (confounded with separation, small samples, directional
  only). sporks' 9W-0L cardinal record is its architecture's bill, not free
  map knowledge.
- Spawning now: denial adjudication (blocks Loki; includes checking whether
  the two sources simply counted DIFFERENT gunners — the book's home-picket
  vs core-threat-creep split makes a definitional collision likely) + thread
  3 (unclassified five). Paced budgets, archive-first.

## Adjudication verdict (~16:15) — LOKI UNBLOCKED

→ docs/research/denial-adjudication-2026-08-07.md. Verdict: NOT a
definitional collision, NOT their-version drift (Ouroboros v8 stable across
both samples). Cause: **OUR-version era mismatch** — session-12's sample was
our v53/55/59 era, the denial book's is v64, and Ouroboros's deterministic
build queue is perturbed by when OUR builders die (the book's own
drumlin/atoll evidence), which changed enormously between eras.

**GENERALIZED LESSON, board-wide:** every denial constant is conditional on
OUR version, not just theirs — the whole denial book inherits this (rows are
v64-era). Prefer wide-margin tiles; re-verify rows after any ship that
touches early-game builder survival. **v65's J qualifies** → one-game
re-verify before hardcoding anything into Loki.

- Corrected constants (Ouroboros v8, our v64, dsq to OUR core): eider
  core-threat **r50@(16,10)** dsq9, margin 48; meander core-threat
  **r46@(13,8)** dsq5, margin 45 — supersedes the book's meander row, which
  had a real bug (sentinel range applied to a confirmed gunner-only team).
  Home-picket tiles (12,9)/(13,6) confirmed non-core-threatening.
- GO/NO-GO: **GO** on both core-threat tiles for Loki, version-pinned our
  v64+ with the v65 re-verify; **NO-GO** on home-picket tiles (wrong
  target); **RETIRE** session-12's original eider/meander numbers.
- BONUS: this mechanism explains ouroboros_probe's measured gentleness (it
  was built on stale-era numbers) — probe refresh from v64/65-era replays is
  the fix.
- v65 window so far: first two true-v65 completions are 2-0 — **3-2 vs
  Memtrace v27 (battery class, seat A — the J experiment, match a450ea25)**
  and 4-1 vs Viktor5776 v1. Memtrace bumped v26→v27. Research arm decodes
  a450ea25 for the I/J mechanism read as soon as the ~16:31 archiver pass
  lands it.

## Unclassified five — classified (~16:35); brief-b COMPLETE

→ docs/research/unclassified-five-2026-08-07.md. All three brief-b threads
now landed (sporks decode, family cross-check, this). Headlines:

- **Leviathan v9 = FOURTH family member** (team lazy / Orizon / Team 48 /
  Leviathan): point-blank gunner battery, fastest yet — median 64 rounds,
  93% core-kill, aim 0.0. The family counter (J + barrier ammo-sink + Stage
  3 race) now addresses four teams.
- **CtrlAltDefeat v107 = UNCHANGED from the cad_probe era** — launcher r1 +
  three thrown raiders at r2/r3/r4, identical across two unrelated maps (the
  tightest deterministic signature decoded today). Consequences: (a)
  cad_probe is CURRENTLY VALID whenever they sit on v107 (they flip
  v107↔v112 — check version before trusting a leg); (b) NEW LOKI CANDIDATE:
  **insertion-drop denial** — their throw targets are the passable tiles
  near our core ring; pre-occupying the historical drop tiles (denial-book
  method, our-version-pinned) denies the landing itself. Pre-mortem vs the
  decoded throws first.
- **OopsGotYourElo v21 = the most tiebreak-committed team measured anywhere**
  (60% of its games reach r1000, vs sporks' 12%). Piece H flips r1000
  tiebreaks → the next OGE pairing under v65 is **H's natural experiment**,
  exactly as Memtrace is J's. Watch both.
- gsxWins caught MID-SHIP v16→v18 (battery, sentinel-led, 100% core-kill in
  15 games); SingleCore v7 battery sentinel-variant with a period-8
  shuttle-throw quirk (possible probe target).
- **Updated pool mix (fresh last-60, 93.3% classified):** point-blank 46.4 /
  picket 28.6 / econ-first 10.7 / all-in 8.9 / launcher-insertion 3.6 (new
  row) / grind 1.8. The 9-seat battery recommendation (4 point-blank / 3
  picket / 1 econ / 1 all-in) is UNCHANGED. Battery+picket = 75% of what we
  face.
- New unclassified opponent surfaced: **Viktor5776 v1** (we beat them 4-1 in
  v65's second match) — queue a 1-match classification pass next cycle.

## v65 first production read (~17:00) — research arm

→ docs/research/v65-production-read-2026-08-07.md (Memtrace 3-2 W + Ouroboros
0-5 L decoded; v65 window 4-2). **J VERIFIED** (counterbattery 1/7/11/4/0 per
game vs baseline exactly-1). **I verified in 9/10 games, ONE BUG**: nordkap
chase_battery config — 166 rotations/50 oscillations, 1,660 Ti burned in a
tiebreak loss, starved H's bank to 243. **H half-alive**: core arm fired a
single 14,634-Ti dump at exactly r960 (g2 W); builder harvester-spam arm
NEVER fired in three r1000 games with builders alive (972 heals in g4 —
heal-priority starvation = piece K's case, measured); design gap: the dump
zeroes tiebreak #3. **Ouroboros leak survives v65** (0-5 seat B, J
outnumbered 2-3 cb vs 20-40-turret swarms) — confirms Stage-3/denial/armor
staging, not more counterbattery; contrast TWO r69 core kills vs Memtrace
(thin-house battery teams lose the race to our siege). **Denial staleness
confirmed twice**: fresh meander first-gunner r8@(8,6) matches neither prior
row — exact-tile constants expire with OUR ships; re-extract post-ship or
deny regions. **Lunds seat-B cell moved for the first time ever: 0-5 → 2-3**
(their v42 — confounded with their ship). INFRA: archiver misses our own
matches (global list, 8/cycle) — spec'd a --mine priority pass to the
builder.

## Main-session decisions on the sporks/denial batch (~16:05, via board)

- **J-WIDENING accepted as PIECE K, NOT retrofitted** — Eir 5's screens are
  mid-flight on J-as-built and stay attributable. Piece K (standing ~5%-income
  core+trunk heal budget) leads the Eir 6 cycle with the two ride-alongs
  (sporks ammo policy: convert 17 @ r0 sd 0, cap 60, top-up 4; B' redesign:
  floor 5 bodies + delivered-rate gate). Mid-screen scope changes are how
  attribution dies.
- **SPORKS REFRAME ACCEPTED WHOLESALE**: the economy is the armor (conveyor
  mass = 3-Ti ablative plates eating 66% of raids; heal = 4.6% of income),
  the army is a solvency-triggered finisher (advance == ammo at cap 60 with
  core repaired, 11/12 kill-starts). New strategy-file frame for the arc. It
  recontextualizes the census identity gap: our economy dies because it is
  THIN AND UNHEALED, not because economy-under-aggression is unviable.
- **DENIAL DISCREPANCY = BLOCKING for Loki**: the fresh Ouroboros eider/
  meander first-gunner rows contradict the session-12 13-replay decode (round
  AND tile). I own resolution; hypotheses to test: within-v8 drift,
  seat-dependent tile mirroring, map-rotation tile changes. NO Loki constants
  from either row set until resolved.
- Axis-split analysis of our own games: queued (sporks 9W-0L cardinal / 6W-10L
  diagonal; confound honesty noted).

## Main-session decisions on the Orizon-family batch (~16:25, via board)

- FAMILY VERDICT ACCEPTED (team lazy + Orizon + Team 48 one code family, Askar
  convergent): one counter addresses ~17% of matched pool + top-8 #6. The
  family-scoped BAIT-BARRIER is accepted as a Loki/K-cycle candidate — scoped
  strictly to the family (first-blocker ray geometry, no priority table;
  thread-5's refutation covered priority-table teams only), gated on (a) the
  denial adjudication resolving, (b) a pre-mortem vs 607ffaeb, (c) ray
  prediction from the denial book. Two 3-Ti barriers ~= team lazy's whole
  measured ammo bank is the arithmetic to beat.
- J'S PRODUCTION EXPERIMENT: agreed the next Orizon/Team 48 pairing under v65
  is the cleanest read; research session watches, my monitors + tape record.
  v64-Orizon = measured coinflip (3-2 then 2-3) is the prior.
- MODEL CORRECTIONS APPLIED: retire "Orizon 4 builders ever" (45 in r1000);
  axis effect is architecture-specific, not map-level.
- Denial adjudication note: the definitional-collision hypothesis (session-12
  counted home-economy pickets, the book counted core-threat creeps) is
  plausible and would dissolve the discrepancy without impeaching either
  decode — if confirmed, BOTH row sets are valid for their respective
  purposes and Loki unblocks with the book's rows.

## Main-session verdicts on the adjudication (~16:30, via board)

- ADJUDICATION ACCEPTED, LOKI UNBLOCKED: the discrepancy was an OUR-version
  era mismatch (their deterministic queue is perturbed by when OUR builders
  die). Session-12's original Ouroboros first-gunner rows are RETIRED; the
  book's v64-era GO constants stand (eider core-threat r50@(16,10) margin 48;
  meander r46@(13,8) margin 45 — the book's meander sentinel-range bug
  superseded); home-picket tiles NO-GO. NEW STANDING RULE: denial constants
  are conditional on our own version — re-verify after any ship touching
  early-game builder survival. v65's J qualifies, so ONE v65-era Ouroboros
  re-verify game gates the Loki hardcode (next unrated leg when the rate
  budget allows).
- ouroboros_probe refresh from v64/65-era replays: queued with the probe-fleet
  work (its measured gentleness = stale-era calibration, now explained).
- v65 rated window opens 2-0 incl. 3-2 vs Memtrace (battery class) — the
  research session decodes a450ea25 for the I/J mechanism read; my monitors
  hold the trajectory.

## Routing to the research session (~16:40, via board — two smalls, pick up between agents)

1. AXIS-SPLIT OF OUR OWN GAMES (queued earlier, yours if you want it): compute
   our cardinal-vs-diagonal core-pair win split across the archived corpus,
   per bot version, mirroring your sporks 9W-0L/6W-10L method — including
   whether OUR economy line shares sporks' architecture-specific cardinal
   preference. Feeds the Thor-layer map choices.
2. OUROBOROS_PROBE ERA-REFRESH SPEC (spec only; the rebuild/freeze is mine):
   from v64/65-era Ouroboros replays (bab61537, 79fb8453, + anything newer in
   the archive), the delta list vs the probe's current behavior — what their
   perturbed queue does differently against our current openings. Your
   era-mismatch finding predicts the specific gaps; write them down and I
   commission the rebuild with the fleet work.

## Main-session verdicts on the unclassified-five batch (~16:45, via board)

- LEVIATHAN = 4TH FAMILY MEMBER ACCEPTED (median 64 rnds — the fastest yet;
  the family counter now covers 4 teams / ~20%+ of pool). Strengthens the
  Eir-6 round-floor case from today's J-experiment observation: the family's
  speed (64-119 rnd kills) outruns every defensive gate we have
  (HUNT_MIN_RND=120, MEDIC_EARLY_MIN_RND=40 helps but heal-budget-from-r0 =
  piece K is the structural answer).
- POOL MIX FIRMED at 93.3% classified (point-blank 46.4 / picket 28.6 / econ
  10.7 / rush 8.9 / launcher-insertion 3.6 / grind 1.8); 9-seat battery
  allocation unchanged.
- CAD_PROBE CONDITIONAL VALIDITY RULE adopted: valid iff CAD sits on v107
  (byte-stable vs the probe era, tightest signature of the day) — check the
  version stamp before trusting any CAD leg. Insertion-drop denial joins the
  Loki candidate list, gated on a pre-mortem vs the decoded throws.
- NATURAL-EXPERIMENT WATCHLIST adopted: family pairings = J's read (a450ea25
  decode pending), OopsGotYourElo = H's read (60% r1000-committed — H's
  designed prey). My match watcher surfaces completions; flag any OGE result
  under v65 the moment it lands.
- Viktor5776 (new, 4-1'd under v65) queued next cycle.

## Main-session actions on the v65 production read (~16:55, via board)

- PIECE J: VERIFIED IN PRODUCTION, accepted (counterbattery 1/7/11/4/0 vs
  baseline exactly-1; two r69 core kills vs the thin-house battery class;
  outnumbered vs picket swarms exactly as the Thor staging predicts).
- EIR 5.1 HOTFIX COMMISSIONED (bots/_v76e51): I's chase_battery oscillation
  (rotation latch + no-return window) and H's dump cap (convert at most
  consumable ammo — turrets x rounds x shot-cost x1.5 — the rest stays banked
  for tiebreak #3). Builder-half non-firing is piece K's case, measured in
  production (972 heal actions claiming every slot), untouched in the hotfix.
- LOKI PIVOT ACCEPTED: exact-tile constants expire with OUR ships (meander
  r8@(8,6) matches neither prior era) - Loki denies REGIONS/stable geometry,
  or auto-re-extracts post-ship. Design doctrine, not a blocker.
- ARCHIVER FIXED (43eb673): --mine pass first each cycle + dedupe; takes
  effect on its next 30-min cycle without re-arm.
- v65 window 4-2; Lunds seat-B cell moved for the FIRST time (0-5 lifetime ->
  2-3, their-v42 confound noted); Ouroboros seat lock intact.

## Rollbacks are re-characterization triggers (research, s14 ~20:05)

Two same-day data points: CAD v110→v107 (probe conditional-validity rule
already adopted) and now Powerpuff v26→v18 (opp_watcher, builder 19:57
note) — their v26-era rows and census-era characterization are suspect
until a v18-era match is read. Idea: the opponent version watch should
treat a ROLLBACK exactly like a version bump — same staleness rule, same
"re-verify before relying" discipline — plus one extra: the rolled-BACK-to
version may match an OLD era we already decoded (v18-era rows may exist in
the archive predating v26; a lookup beats a fresh decode). Class-map
impact is nil while probes cover the class (flotte_probe holds for
Powerpuff); wild-fidelity claims are what go stale.

## The CAD family moved versions TOGETHER tonight (research, s14 ~21:15)

Four family-adjacent teams changed versions within one evening: CAD
v107→v115, Lunds v42→v43, KCM 7→1 (rollback), Powerpuff 26→18 (rollback).
Synchronized movement strengthens the one-code-family hypothesis (shared
maintainers pushing together) — and suggests a family-wide re-freeze after
any observed member bump is cheaper than per-team staleness discovery: when
ONE member moves, presume ALL members' constants stale and re-verify the
family in a batch. Also: two of the four are rollbacks (see the rollback
re-characterization entry above) — the family may be A/B-ing against the
field, which makes their constants systematically less stable than
loner teams'.

## Opening-as-steering: deterministic queues that READ us are an input we control (research, overnight ~23:00)

The v65-era Ouroboros re-verify killed the fixed-tile Loki hardcode, but its
mechanism correction opens a better door: their queue diverges from the
book's transcript at r3 — before any casualty — so the perturbation keys on
our OPENING SIGNATURE (what they see us do/be in the first rounds), not on
when our builders die. If their build order is a deterministic function of
our early visible state, then our opening is literally an argument to their
build queue. Three escalating uses, all play-the-players shaped:
1. MEASURE: a Loki probe shouldn't replay fixed tiles; it should map
   f(our-opening-variant) → their-first-gunner (round, tile) over a small
   set of our opening variants, per map. If f is stable per variant (their
   determinism suggests yes), we get a steering table instead of a tile book.
2. STEER-TO-COVER: pick the opening variant per map whose induced gunner
   tiles land ON our home turrets' firing rays (the ray-coverage law:
   covered = median lifetime 8-11 rnds, uncovered = 81-105). We don't deny
   their turret — we schedule its death.
3. UNREASONABLE VARIANT (Magnus's standing welcome): a throwaway opening
   feint — one early builder step pattern chosen purely to steer their queue
   into a dead shape, costing us ~nothing if f is flat on that map (measure
   first). Candidate cycle name if it ever builds: Loki (it IS the trickster
   shape — denial by suggestion, not obstruction).
Scope caveat: measured on Ouroboros v8 only; family reach unknown (their
gentleness-era probe calibration suggests other deterministic teams exist —
same instrument would test any of them). Parked as a shaped direction for
the morning brief; no build tonight (not in the mandate).

## Opponent error prints = free displacement telemetry in local legs (builder+research, overnight ~23:20)

Three consistent data points tonight: opp_v69's stale-pave caught-exception
prints scale with how much OUR bot displaces his builders — 22-32/120 base
band (no ring, no thrower), 68/120 under C1's ring pressure, 90/120 under
HD's 127-throw ejection. His error rate is OUR displacement meter, at zero
instrumentation cost, readable from stderr in any local battery. Uses:
(a) mechanism-fire verification for any future displacement piece (throw
counts from OUR logs say what we did; HIS print count says what actually
landed on his dispatch); (b) regression canary — a displacement-neutral
change that moves his print rate is doing something we didn't intend.
Limits: local-only (stderr never reaches us from platform games), opponent-
specific (needs a lineage that prints its catches; x3r0 forks do), and it
counts units-touched not severity (his freshness gate caps per-event cost
at ~1 action). Generalizes to any opponent whose caught-exception prints
correlate with a game state we induce — worth checking which other pool
teams print diagnostics at all.

## Corrections from the patch-retrodiction study (2026-08-08, builder-applied)

- **Family-synchronization hypothesis RETIRED**: launcher-family version-bump
  pairs run at/below chance (0.72% vs 1.69% base rate) — teams in a code
  family do NOT ship together; treat any earlier note suggesting coordinated
  family bumps as dead. (patch-retrodiction-2026-08-08.md)
- **Launcher-family membership corrected**: Powerpuff Girls has NEVER built a
  launcher in 45+ archived games — not a member. Banminary and gsxWins ARE
  members (r≤2 launcher, 100% of games) and were never listed.
- **SENSITIVITY-FLOOR caveat, standing, for any "what did team X change"
  claim about linear developers**: our census cannot distinguish even our own
  consecutive ships v64→v75 — a flat fingerprint means WE LEARNED NOTHING,
  not that they changed nothing. Phrase accordingly.
