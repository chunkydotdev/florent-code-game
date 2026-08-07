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
