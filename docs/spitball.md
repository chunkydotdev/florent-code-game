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
