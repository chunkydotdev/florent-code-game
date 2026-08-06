# Strategy log

The point of this file: in a ladder game, the thing that compounds is knowing which changes
moved the rating and which didn't. Memory is unreliable and the ladder is noisy — write it down.

**One entry per deployed bot version.** Write the hypothesis *before* deploying, the result
*after* the ladder has settled. Keep dead ends — a documented failure is worth as much as a win.

Rules of thumb:
- Change one meaningful thing per version, or you can't attribute the result.
- Give the ladder enough matches to be meaningful before calling it. Note the sample size.
- If the result surprises you, that's a fact for [game-model.md](game-model.md), not a tweak.

---

## Template

### v0 — name

- **Date deployed:**
- **Commit / tag:**
- **Hypothesis:** what we believe and why we believe it
- **Change:** what's actually different from the previous version
- **Predicted effect:** stated before deploying, so we can be wrong on the record
- **Result:** rating before → after, over N matches
- **Read:** did the hypothesis hold? what did we learn regardless?
- **Next:** what this points at

---

<!-- newest entries at the top, below this line -->

### Discard on the pooled number, but the per-map split is the finding — reactive home defense

- **Date:** 2026-08-08 · challenger `bots/ladder1`, primary gate `bots/opp_v44`
- **Hypothesis (pre-registered above):** our defense is scheduled off *our own* economy and never
  off the *enemy's* behaviour, so adopting v44's vision-triggered emergency battery — threat
  detection decoupled from harvester count — should close the gap to v44.
- **Result: 40.6% [36.3%, 45.1%], n=480, 0 crashes either side.** The `aug7` baseline against
  the same opponent is **40.8% [32.5%, 49.8%]**. Statistically indistinguishable. **Discard
  against the primary gate.**
- **And the pooled number is the least informative thing in the run.** The per-map split is
  **violently bimodal**, not flat (`ladder1` wins, out of 32 per map):

  | wins big | | collapses | |
  | --- | --- | --- | --- |
  | antler | **27** | hive | **0** |
  | lighthouse | **22** | atoll | **3** |
  | archipelago | **20** | snowflake | **3** |
  | heart | **20** | jackpot | **6** |
  | moonrise | **19** | drumlin | **7** |
  | | | meander | **9** |

  **A 0-for-32 is structural, not variance.** And `core_destroyed` came in at **120/480 = 25%**
  against this bot's usual **~17%** house rate, so the mechanism is unambiguously *engaging* —
  it is not a null. Something in it is worth a great deal on five maps and catastrophic on six,
  and averaging those into 40.6% describes neither.
- **Leading hypothesis, not yet confirmed:** economy starvation on ore-poor maps. **`atoll` has
  8 ore tiles and `hive` 12 — the two lowest in the 15-map pool** — and both collapsed, while
  ore-rich maps did fine. Diverting a builder or spending on ammo costs proportionally far more
  where there is little ore to work. This converges with the ammo arithmetic logged below:
  sustained defense **requires** delivered income, and where income is thin, defense eats the
  economy that pays for it.
- **Caveat recorded honestly:** the diff runs to ~159 changed lines, which is large for one
  mechanism, and it has not yet been confirmed that a second behaviour did not creep in
  alongside the trigger. If it did, the bimodality is unattributable between them. Diagnosis
  requested; **do not build on this result until that question is answered.**
- **What to do with it:** do **not** average this away. The five maps at 60-84% are a real
  signal. The next move is to find what distinguishes them from the six that collapse — the
  ore-density hypothesis is testable directly — and gate a variant that keeps the mechanism
  where it pays. A map-conditional defense trigger is a legitimate follow-up, but note the
  standing caution that per-map tuning has a **one-week shelf life** on a weekly rotation, so
  prefer a rule keyed to a *measurable map property* (ore count, ore density) over a map list.

### Finding — we out-collected them 4880 to 0 and still lost, to three units we never touched

- **Date:** 2026-08-08 · from a 9-replay batched digest across 6 opponents rated 1323-1965
  (full tables in [opponents.md](opponents.md)); no code change
- **The single most damning game in the archive:** an Albert And Einstein match in which we
  finished **4880 titanium collected to their 0** — total economic dominance — and **lost
  anyway**, to **3 units that were never reinforced, over 985 turns**. Not a rush that
  overwhelmed us. Three static pieces that sat there for the entire game while we had no way to
  remove them.
- **The gap this exposes is not defense, it is "clear the siege".** We can out-economy the top
  of the field and still lose, because `aug7` has **no mechanism that removes an established
  enemy emplacement**. It has no offense at all (no enemy-Core tracking, no movement toward it,
  no `fire()` sabotage, no forward turrets), so once a siege is planted, every remaining round
  is spent accumulating a tiebreak we will never reach. **Building more defense does not fix
  this; only the ability to attack a static target does.** `ct.fire()` from a builder — 2 damage
  for 2 Ti against buildings, orthogonally adjacent — is the cheapest tool we already have and
  have never used.
- **Two attacker archetypes, converged on independently across the top of the field:**
  - **"instant-Sentinel", turn 1-6.** The Launcher-thrown builder **builds the forward Sentinel
    on arrival**, so the opening is **map-size-independent**. Seen in `sporks` (1923) and all
    five AAE games. `sporks` killed a Core in **63 turns** — the fastest in this project's
    history. **This supersedes the turn 4-15 calibration target; the real number is turn 1-6.**
  - **"forward-Gunner", turn 33-39.** A separate, slower lane — `Pivot` (~1907-1965),
    `not adgato` (1897) and `Besvikomat` (1789), **three unrelated opponents converging tightly**.
    Rush defense must cover both windows, not just the early one.
- **Ring-camping is correlated with wins, not causal** — do not over-invest in blocking as a
  mechanism, and note this agrees with the local probe, where the blocker never once decided a
  game.
- **Model correction, flagged loudly:** the Core's **raw** hit-count-to-kill range widens from
  28-136 to **28-1206**, while net HP holds at 500-512. Healing dominates siege arithmetic by up
  to 43×. Now in [game-model.md](game-model.md).

### Telemetry correction — v40's ladder record was much better than we logged

- **Date:** 2026-08-08 · from `fcode match list --mine --json`, fully paginated, 181 matches
  (107 rated + 74 unrated) with per-match `teamAVersion`/`teamBVersion`, `eloDelta`,
  `ratingBefore`
- **Supersedes the earlier entry below that read "v40 played exactly one ladder series."** That
  was an artefact of reconstructing an activation timeline by hand. With real version
  attribution: **v40 ("aug7-sentinel-economy", our line) is 8W-1L, net Elo +35.24 — the
  strongest well-sampled version the team has.** Current team rating **1233.34, rank #50/103**.
- **v44 ("florent-v58") has only 2 rated series, both wins** (+14.34), and is **undefeated on
  the rated ladder**. Everything we know about v44 losing comes from the **unrated** bucket,
  where it is **0W-4L with all 20 games ending `core_destroyed`**.
- **Read carefully, because this cuts against a claim made earlier today.** The local arena says
  `opp_v44` beats `aug7` 59/41 over 120 matches — well powered, and it stands. The ladder
  samples (9 series vs 2) are far too small to contradict it. What they *do* say is that our
  line has not been outperformed on the ladder, and that **v44's only observed losses are to
  the rush archetypes above** — which is exactly the weakness our current lane targets.
- **Method note that earned its keep:** `--mine --json` carries per-match version attribution
  directly. **Never reconstruct an activation timeline by hand again** — doing so produced a
  wrong entry in this log within the same day.

### Measurement — the first rush baseline says 95%, and the number is not the finding

- **Date:** 2026-08-08 · `bots/rush_probe` v1, 240 matches vs `aug7`, 0 crashes either side
- **Headline:** **`aug7` beats `rush_probe` 95.0% [91.5%, 97.1%]**. Control: `starter` beats it
  **93.3%** — while hemorrhaging **221 units** to its own unguarded `is_tile_empty` crash bug.
  An all-in rush loses to a *crashing* economy bot.
- **⚠ Read the direction of these numbers carefully — this one has already been misread once.**
  `arena.py` reports the **first-named bot's** win rate, and the runs were
  `arena.py aug7 rush_probe` and `arena.py starter rush_probe`. So **95.0% and 93.3% are the
  DEFENDER's win rates. The rusher lost both, badly.** Inverted, these numbers read as "the
  meta threat is quantified and severe", which is the opposite of what was measured and would
  send the next session optimising against a threat level nobody has established yet. **The
  meta threat is NOT yet quantified.** What is quantified is that *this* probe — all-in,
  walk-in, ammo-starved — is harmless. A faithful probe does not exist yet.
- **Do not read this as "we are safe from rushes."** A real 1306-rated opponent beat us **0-5,
  all five by `core_destroyed`**. The probe and the ladder disagree, so the probe is wrong, and
  its own diagnostics say exactly how. A cross-tab of *who died* is what made this legible:
  - **rush_probe's own Core died in 22 matches; `aug7`'s in 5.** Going all-in leaves zero home
    defense, and on small maps `aug7`'s purely defensive Sentinels reach far enough to kill it
    (fjordgate 7/8).
  - **On 7 of 15 maps neither Core died in 1000 rounds** — three Sentinels cannot close 500 HP
    even completely unopposed.
  - When it does win it is **100% `core_destroyed`, 0% economic** — Sentinels are the only lever
    that ever wins a rush; the spawn-ring blocker never decides a game.
- **Why three Sentinels stall, and it is the most useful thing here: it is ammo, not damage.**
  A Sentinel firing on its 2-round cooldown burns **5 Ti/round**; three is **~15 Ti/round**
  against **2.5 Ti/round** of passive income. Stripped of economy, the probe can fire about a
  sixth of the time, so its theoretical ~27 dmg/round never arrives.
  **Therefore the real meta is economy-PLUS-rush, not all-in rush.** Albert And Einstein spent
  four builders on a Launcher and turrets *and* still ran enough economy to sustain fire. This
  is a genuine correction to how we framed the threat.
- **Second defect: walk-only delivery under-tests big maps by an order of magnitude.** Measured
  first-Sentinel turn ran **3-4 on fjordgate (10×10)** but **24-56 on drumlin (25×25)**, against
  an observed ladder benchmark of **turn 4-15 regardless of map size** — because the top
  execution throws its own builder 6-8 tiles with a **turn-1 Launcher**.
- **Next:** two probe modes — walked-sentinel (common meta) and launcher-insertion (top meta) —
  **both with enough economy to sustain ammo, and both keeping 1-2 home Sentinels**, since a
  probe that suicides measures its own fragility rather than our defense.
- **Method note worth keeping:** the win rate was the least informative number in this run. The
  who-died cross-tab and the per-map "neither Core died" count are what turned a misleading 95%
  into a specific, fixable list of three defects. When a result contradicts a real-world
  observation, instrument the disagreement rather than believing the cleaner number.

### Intel — a hole in our own team's active bot, on small maps

- **Date:** 2026-08-08 · from the `opp_v44` source read (full addendum in
  [opponents.md](opponents.md) under `florent-v58`)
- v44's emergency-defense battery — the mechanism we are adopting — is **disabled on maps with
  `w * h <= 120`**. **`fjordgate` is 10×10 = 100** and falls below the gate, leaving only a
  slower `harvesters >= 1` fallback to cover it.
- Worth logging twice over: it is a known weakness in the strongest bot on our own team, and it
  will be inherited by **anyone who copies this pattern**. Our own port must **not** replicate
  the gate; `fjordgate` is the per-map row where that difference should show up.

### Hypothesis, pre-registered — defended economy farms a converged-rush field

- **Date:** 2026-08-08 · **written before the measurement exists**, which is the point of writing
  it down. Experiment in flight as `bots/ladder1`; probe in flight as `bots/rush_probe`.
- **The field observation this rests on** (Magnus, from replay watching, high confidence): **the
  sentinel rush is the COMMON ladder opening, including among high-Elo teams.** Not one team's
  quirk. Canonical execution, decoded from series `81d83bb5`: builder turn 0, **Launcher turn 1
  next to their own Core**, own scout thrown 6-8 tiles in one action, camped in our Core's spawn
  ring by turn 6-27, **3-4 Sentinels 1-4 tiles from our Core, first landing turn 4-15**, four
  builders total.
- **Why this changes the evaluation set, not just the strategy.** Our entire local opponent pool
  — `starter`, `opp_v39`, our own lineage — is passive. **Every "early aggression doesn't pay"
  result this project has produced was measured against a field in which nobody ever attacks.**
  Those results are not wrong, but they answered a question about a distribution we do not play
  against. `aug7` vs `rush_probe` is therefore likely **the most ladder-predictive local number
  available**, and it does not exist yet.
- **The claim:** a bot that keeps its economy-first shape but defends *reactively* does not
  merely survive the rush — it **profits** from a field that has converged on it. Three measured
  facts favour the defender, conditional on the defense triggering early enough:
  1. **Healing costs 0.25 Ti/HP** (+4 HP for 1 Ti) against **~0.56 Ti/HP** for any attacker.
     Attrition against a healed target is a losing trade at every level; 2 builders out-heal a
     Gunner, 3 out-heal a Sentinel.
  2. **Sentinels cannot rotate** — facing is fixed at build time. A rush emplacement covers one
     line forever, so approaching off its axis turns 30 Ti of enemy investment into furniture.
  3. Every rush Sentinel costs the attacker **+20% cost scale permanently**, and scale never
     decays. A failed rush is not a neutral trade; it is a tax on everything they build after.
  So the rusher's investment is front-loaded, irreversible, and cheap to blunt — while ours is
  an economy that keeps compounding.
- **Our actual defect, and it is not "too little defense":** defense is scheduled off *our*
  economy and never off the *enemy's* behaviour. `_try_build_sentinel` is gated on 3 harvesters
  **and** on a builder happening to be within dist²≤18 of the Core. In the decoded series our
  first Sentinel landed at **turn 436** and **turn 81** with the harvester gate met at turn
  22-28, and one game never met the gate at all — zero defense, 28 unmitigated hits.
- **The change being tested:** reactive home defense — defend immediately when an enemy is
  visible near our Core, regardless of harvester count. **Purely additive by construction.**
- **Predictions, stated now:** a **no-op (~50%) against the passive pool**, because nobody
  approaches our Core early there; a **material gain against `rush_probe` and `opp_v44`**. If
  both halves hold, the change is not a patch on a weakness — it is a counter to the median
  opponent. **If the passive-pool half comes back materially negative, the change is not
  additive and the implementation is wrong, not the hypothesis.**
- **Accept rule for this lane:** clear the normal Wilson gate against `opp_v44`, **and**
  materially improve against `rush_probe`, **and** not collapse against `starter`/`opp_v39` —
  we still climb through a mostly passive field and must not overfit to rushers.

### Finding — we sometimes deliver exactly zero titanium on maps with no (0,0) Core, and nobody has explained it

- **Date:** 2026-08-08 · two independent observations converging, no code change yet
- **The observation:** `titanium_collected` comes out at **exactly 0** in games where the
  economy visibly exists. This is the same signature as the jackpot (0,0) Core bug — but on
  maps with no Core at the origin, so it is a **different, unexplained failure**.
  1. **From a ladder replay** (`81d83bb5`, vs Albert And Einstein, our own v40): games 1
     (`heart`) and 4 (`hive`) finished **0 collected for both sides**, while game 1 had
     **5 harvesters and 99 conveyors** built. Resource movement *did* occur — 33 and 12
     `distributeResources` events — so stacks were flowing and never arriving. The analyst
     specifically ruled out the enemy blocker denying our delivery tiles: we built conveyors on
     every Core-adjacent delivery tile, early, in every game, with no enemy builder on those
     tiles at build time.
  2. **From local instrumentation**, independently: on `heart`, **3 of 5** `aug7`-vs-`aug7`
     matches ended with **both sides at exactly 0 collected**, decided on the harvester
     tiebreak. `heart` was already one of the four unexplained seat-asymmetry maps and was
     flagged as "a different phenomenon" before the replay evidence existed.
- **Why this matters more than it looks:** crediting is delivery-only (measured, game-model.md),
  **78% of our games are decided on the titanium tiebreak**, and this failure mode zeroes the
  scoring quantity outright. It is not a small inefficiency — it is the economy not existing.
  A trail conveyor whose output side faces *into* the harvester will refuse that harvester's
  stack, and a chain that dead-ends carries stacks that are never credited; both were logged as
  residual unmeasured questions in the 2026-08-07 conveyor work, and this is what they look like
  when they bite.
- **Why it has stayed hidden:** it is invisible in a win rate — when *both* sides zero out, the
  game still resolves on a tiebreak and the pooled number moves by nothing.
- **Next, and this is the highest-value diagnostic left:** instrument whether a given
  harvester's stack ever reaches the Core, per match, per map — the open question
  "do the conveyor chains our builders lay actually complete a path to the Core?" has been open
  since 2026-08-07 and now has two independent pieces of evidence that the answer is sometimes
  no. `heart` is the map to run it on, because it fails ~60% of the time there.

### Intel — the launcher-assisted rush, and what actually kills us

- **Date:** 2026-08-08 · full decode of ladder series `81d83bb5`, all 5 games, no code change
- **The series:** Albert And Einstein (**1306.8**) vs OpenSverige (**1222.8**), **0-5**, ELO
  −12.21. **All five games ended `core_destroyed`.** In every game with a non-zero economy
  reading, **we out-collected them** — and lost anyway.
- **Their opening, identical turn-for-turn in all five games:** Builder Bot turn 0 → **Launcher
  turn 1, next to their own Core** → their own scout builder thrown **6-8 tiles in a single
  action** → that builder walks in and is **camped inside our Core's spawn ring by turn 6-27**,
  where it stays for **57-98% of the game**. Then **3-4 Sentinels built 1-4 tiles from our
  Core**, from turn 4-15. Total investment: exactly **4 builders**, spawned turns 0-3.
- **Verdict — the sentinels kill us, not the blocker.** 5 of 5 `core_destroyed`, 0 of 5 on any
  economy tiebreak; the Core always died first, so the blocker never got to decide anything.
  Net HP to kill our Core was 502-512 every game.
- **But the blocker is not free for us either, and the mechanism is worth naming.** Our defense
  gate (3 harvesters) was met around turn 22-28 in games 1 and 2, yet our first Sentinel did not
  land until **turn 436** and **turn 81** respectively — against near-instant responses in the
  games where ring occupancy was lower. Game 4 never met the gate at all (stuck on 1 harvester,
  zero defense, 28 unmitigated hits). Whether that is the blocker tying up our builders or our
  own build order deprioritising turrets **is not separable from this data** — it is a question,
  not a conclusion.
- **Two model corrections fell out of the decode**, both now in game-model.md:
  - **The Launcher is a rush-delivery tool**, and a large map no longer buys time. We knew
    Launchers throw builders; we had never seen one used to deliver a rush on turn 1.
  - **"28 hits of −18 kills a Core" is only true when nobody heals.** Our builders *do* heal the
    Core (+4 HP for 1 Ti, exactly as documented), offsetting **4-79%** of incoming damage; raw
    hit counts ran **28 to 136**. Only the net ~504 held constant. That is real active defense
    our bot already performs and which nothing in our own docs had noticed.
- **Read:** every "early aggression doesn't pay" result this project has ever produced was
  measured against `starter`, `opp_v39` and our own lineage — **a pool in which nobody ever
  rushes**. The 1300+ band does. That is a structural blind spot in the evaluation set, not a
  strategic conclusion, and it is why `bots/rush_probe` now exists.

### Telemetry — v40's ladder window, and the bar moving out from under us

- **Date:** 2026-08-08 · platform reads only, no code change
- **v40 ("aug7-sentinel-economy", `a9d81a1`) — the whole ladder record it ever produced:**
  rating **1182 → ~1222**, ending its window at roughly **104 matches played / ~1214 rating**,
  rank around **#52-53 of 103**, crossing from Unranked into **Bronze**. Then x3r0 activated
  **v44 ("florent-v58") at ~13:00**, so **every ladder result after that measures their bot,
  not ours.** Attribute segments accordingly; do not read the team's later trajectory as
  evidence about `aug7`.
  **Exact slot timeline** (it flipped twice, so segment carefully): v40 active until ~13:00 →
  **v44** from ~13:00 → v40 briefly re-activated for roughly **one series** (around match ~105,
  rating ~1221) → **v44** again from ~15:15, after the 59/41 head-to-head was confirmed.
  A 13:16 UTC snapshot during that window read rating **1221.23**, rank **#50 of 103**, 105
  matches, last-10 5W-5L. **Standing team norm from here: the active slot follows arena
  measurement** — a candidate that beats `opp_v44` takes the slot, with the numbers attached.
- **The sample is thinner than the match count suggests.** The team ran **42 submission
  versions in ~16 hours** across several people, and **v40 played exactly one ladder series**
  (`1018bf11`, a 3-2 win over Leviathan). The 97-match history is mostly other people's bots.
  A per-replay observation is only evidence about the version that played it — a lesson that
  cost us a wrong conclusion this session (see the opponents.md correction).
- **Trust `fcode match list`, not `fcode status`'s "Last 10".** Status reported 3W-7L;
  reconstructing the real last ten series three independent ways gives **6W-4L** every time,
  while the `rating` field in the same response is current.
- **Where we actually lose: fights.** Across 485 games, **`core_destroyed` is 15W-74L (17%)**
  against **51% on the titanium tiebreak**. Against `1337` it is **0W-17L** on Core kills over
  17 games, with kills landing anywhere from turn 188 to 737 — sustained pressure, not a rush.
  Worst map on the current rotation: **`saga` 2W-8L**.
- **What the top of the ladder builds.** Unrated scouting replay `91d77721` against **Pivot**
  (#1, ~1947): **12 harvesters, 39 conveyors, 17 Gunners, zero Sentinels**, out-collecting us
  **3170 to 810**. Our bot switches builders to defense at `TARGET_HARVESTERS = 3` and then
  builds Sentinels with no cap — a local probe counted **116 sentinels across 10 matches, 66 in
  one**, at +20% cost scale each. **We are running roughly a quarter of the winning economy and
  spending the difference on fights we lose 17% of.**
- **And the bar moved.** Our own teammate's active bot, `opp_v44`, **beats `aug7` — 40.8%
  [32.5%, 49.8%] over 120 matches**, 0 crashes both sides, **38 `core_destroyed`**. Its version
  names ("ammo-gunner", "gunners-before", "gunner-deadzone") say the line is **Gunner-focused**,
  which sits directly against our own measured Sentinel-first result (68.4% [62.4%, 73.7%]).
  That result was obtained against a **passive** opponent pool; v44 was evolved against live
  ladder opponents. **`opp_v44` is therefore the primary confirm opponent from here on** — a
  keep must clear the Wilson gate against it, with `aug7` retained for lineage attribution and
  `starter`/`opp_v39` as no-collapse checks.
- **Read:** the honest summary of this session's ladder position is that our accepted local
  improvements are real and measured, and simultaneously our bot is no longer the strongest bot
  on our own team. The single largest gap is not a bug — it is that we cap economy at 3
  harvesters and cannot win a Core fight.

### Discard — wall-aware BFS pathfinding, and it is worst exactly where it should have been best

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/aug7` at `3cfa588`
- **Hypothesis:** the incumbent walks greedily — a productive cardinal at random, then the
  perpendiculars, then the reverse, giving up on a target after 3 stuck rounds. In a concave
  wall pocket that wanders. The rotation has five maps at ≥19% wall density (archipelago 30.8%,
  saga 28.5%, lighthouse 25.0%, heart 21.8%, jackpot 19.5%) and they are among our weakest.
  **Predicted: the walliest maps gain most, the near-empty ones (drumlin 0.6%, meander 2.1%,
  eider 3.9%) stay flat.**
- **Change:** bounded BFS over a per-unit memo of **walls only** (buildings excluded, since they
  come and go; never-seen tiles optimistically passable), node cap 200 counted on expansions,
  path cached and recomputed only when absent / target changed / consumed, neighbour order
  shuffled at every expansion, and the incumbent's greedy walker retained as the fallback when
  BFS exhausts its budget. `_try_move` still performs the step, so trail-laying is unchanged.
- **CPU:** profiled with `time.process_time()` over ~55,000 builder-rounds — p50 71 µs, p99
  1398 µs, **worst case 3785 µs** against the 8000 µs guard. (Node cap 300 measured 5813 µs and
  was rejected as too tight.) Comfortably affordable; CPU was not the problem.
- **Result:** screen 45.6% [35.7%, 55.8%] (n=90). **Confirm 45.8% [41.4%, 50.3%] (n=480) — no
  verdict, therefore discard.** 0 crashes both sides.
- **Read — the prediction did not merely fail, it inverted.** On the five walliest maps the
  challenger scored **57/160 = 35.6%**; on the other ten, **163/320 = 50.9%**, a dead heat. Its
  three worst maps in the whole run are **archipelago 11/32, lighthouse 8/32, saga 10/32** — the
  three walliest. A change that is neutral everywhere and specifically bad on exactly the maps
  it targeted is not noise; it is a mechanism pointing the other way.
  The best-supported explanation is that **the greedy walker's meandering is exploration, and
  the shortest path is not.** Target selection is unchanged and picks the nearest *visible*
  ore, so what a builder sees determines what it can go build. Detouring around a wall sweeps
  vision across ground a straight line never touches, and it lays trail conveyor over a wider
  footprint. On wally maps the detours are longest — which is exactly where the BFS bot gives up
  the most incidental discovery. Consistent with the development measurement that the BFS build
  produced *more* buildings (94.5 vs 76.7) yet still lost: it was building more efficiently in a
  smaller explored region.
- **Next:** do not retry shortest-path movement as a movement change. If it is retried at all it
  has to come with a **separate** exploration mechanism (systematic frontier targeting rather
  than nearest-visible-ore plus random walk), and that is a `_pick_target` experiment, not a
  `_move_toward_target` one. Kept in `bots/_dev_bfs` and portable.

### Finding — seat A acts first for every unit, and on contested-ore maps that is worth 2.3× the harvesters

- **Date:** 2026-08-08 · instrumented diagnosis, `bots/_diag_seat`, 30 matches, no code change
- **Question:** four maps show large seat asymmetries with identical bots on both sides —
  archipelago ~77-88% for seat A, atoll ~21-31%, heart ~31%, lighthouse ~28%. None is the (0,0)
  Core bug and the NW-corner-reference hypothesis was already refuted.
- **First result, and it reframed the search:** all four are decided on **economy**, never on
  Core kills, and never on unit attrition — the losing seat often has *more* units alive.
- **archipelago is explained.** Engine unit IDs show **team A's Nth builder always has an ID
  exactly one less than team B's Nth** — zero exceptions over 10 instrumented matches on two
  maps. Units run in spawn order, so **seat A resolves first in every round of the match**. On
  archipelago 16% of the 38 ore tiles sit in the contested band near the midline; a Harvester
  blocks movement; so seat A wins each same-round race for a contested tile and then physically
  walls seat B out of it while retargeting deeper ore. Measured: **62 harvesters for A against
  27 for B (2.3×)**, **10 of A's built on B's side of the midline**, B crossing **zero** times,
  and a 1.9× collected-titanium gap that the harvester ratio accounts for. Both sides find ore
  through `_pick_target` at ~99%, and B actually reaches its *first* harvester sooner — so this
  is not a vision or targeting difference. It is the compounding of contested-tile races.
- **The other three, honestly:** `atoll` has only 8 ore tiles with 50% contested, and lands in a
  near-tie decided by the harvester tiebreak — consistent. `lighthouse` has **0% contested ore**,
  harvesters come out 8-7, and seat B still wins both instrumented matches *despite* worse
  movement metrics on every axis (more stuck events, more move failures, 20× more
  random-exploration fallback). **Unresolved** — the likely axis is trail *completion* rather
  than harvester count, which nobody has ever instrumented. `heart` is stranger still: 3 of 5
  matches ended with **both sides at exactly 0 collected**, decided on the harvester tiebreak.
  **Unresolved, and a different phenomenon.**
- **Also refuted along the way:** the sentinel far-vs-near targeting bias was a tempting
  secondary explanation (atoll: seat A 75% far-class facings vs seat B 80% near-class). It is
  not driving this. Across **625 captured sentinel-fire events, zero were suboptimal** — rays
  essentially never held 2+ enemies at once. Lighthouse settles it outright: seat A had the
  *good* facing profile there and lost anyway.
- **Read:** this upgrades a fact in game-model.md rather than adding a bug to fix. The seat-A
  edge was recorded as "an advantage on very small maps"; it is really **an advantage
  proportional to how much ore is contested**, and small maps were a proxy for that. The
  bot-side lever, if there is one, is contesting the midline earlier instead of accepting the
  split — which is an economy-expansion question, not a fairness bug.

### ACCEPT — conveyor facing by dominant axis: 57.9%, and the reason it won is not the reason we tried it

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/_incumbent` = `a9d81a1`.
  **Promoted into `bots/aug7`.**
- **Hypothesis, stated before measuring:** `nearest_cardinal()`'s diagonal table (NE→N, SE→E,
  SW→S, NW→W) is a **chirality rule** — each diagonal snaps to its clockwise-preceding cardinal
  — so it survives a 180° rotation and **inverts under both mirrors, on all four diagonals**.
  Six of the fifteen maps in the rotation are mirrors, which no previous audit exercised
  because the old invented pool was all-rotational. Its one live call site is the trail
  conveyor's facing in `_try_move`, and that trail is the only thing that ever delivers our
  titanium. **Predicted effect: the six mirror maps' seat splits move toward 50%.**
- **Change (one):** a new `cardinal_toward(src, dst)` picks the cardinal by comparing `|dx|`
  and `|dy|` on the real delta, breaking an exact-diagonal tie at random. `nearest_cardinal`
  and the dead `_try_build_conveyor_toward_core` left untouched, for attribution.
- **Results:** screen 53.3% [43.1%, 63.3%] (n=90). **Confirm 57.9% [53.5%, 62.3%] (n=480) —
  the lower bound clears 50%, so this is an accept.** Regression vs `opp_v39` 65.8%
  [59.6%, 71.5%] (n=240), above the `aug7` reference of 65.0% [57.8%, 71.6%]. **0 crashes for
  the challenger across all 1,004 matches.**
- **And the hypothesis was wrong.** Two independent reads say so:
  - The mirror-map self-play diagnostic (192 matches) is **mixed, not a repair**: antler
    31.2%→40.6% and eider 43.8%→53.1% improved, moonrise barely moved, but **meander
    56.2%→37.5% and heart 43.8%→21.9% got worse**, and heart is now the only mirror map the
    harness flags as seat-decided.
  - In the confirm, the split that mattered went the wrong way: the challenger took
    **176/288 = 61.1%** on the nine **rotational** maps against **102/192 = 53.1%** on the six
    **mirror** maps. If mirror-equivariance were the mechanism, that ordering would be
    reversed.
- **Read:** what actually paid is the part of the change nobody was arguing about. Snapping an
  already-quantised 8-way `Direction` throws away the magnitudes — a delta of (−2, −3) is
  mostly north, but it lands in the NORTHWEST sector and the table sent it WEST. Comparing
  `|dx|` and `|dy|` just points the trail at the Core, and that pays wherever trails are long
  and terrain is awkward: the biggest per-map gains are **archipelago 24/32 (30.8% walls),
  snowflake 24/32, saga 23/32 (28.5% walls)**. The equivariance argument was the reason we
  looked at the function; it was not the reason the change won. **Both facts are worth keeping:
  a correct hypothesis is not required for a correct change, but reporting the win without the
  refuted mechanism would leave the next session tuning the wrong lever.**
- **Next:** the mirror asymmetry itself is therefore **still unfixed and still real**, and heart
  is now the sharpest example of it. Do not treat this accept as having closed queue item 2.

### No-verdict, escalated not discarded — the (0,0) Core store fix repairs the map and the gate can't see it

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/_incumbent` = `a9d81a1`
- **Hypothesis, stated before measuring:** publishing the Core's position with a +1 offset so
  that store slot 0 keeps meaning "unwritten" will restore delivery for a team whose Core sits
  at (0,0), repairing `jackpot` from a guaranteed seat-A loss to a fair map. **Predicted pooled
  effect: about +1.7 points** — a full repair of one map out of fifteen moves that map from
  ~50% to ~75% head-to-head (we win it outright in the seat the incumbent throws away, and play
  it evenly in the other), which is 25 points on 1/15 of the pool. **That is below what a
  480-match confirm can resolve, and it was written down before the run.**
- **Change (one, minimal):** `_run_core` writes `pos.x + 1` / `pos.y + 1`; `_read_core_pos`
  requires `x > 0 and y > 0` and subtracts the offset. Comments rewritten to explain the trap.
  Nothing else in the file touched.
- **Results:**

  | run | n | result |
  | --- | --- | --- |
  | mechanism, 6 single matches on jackpot | 6 | team A `titanium_collected` **0/0/0/0/0/0 → 4970 / 2480 / 4970 / 4960 / 2480 / 4970** |
  | jackpot mirror seat split | 48 | **0/48 = 0.0% [0%, 7%] → 22/48 = 45.8% [33%, 60%]** |
  | screen vs incumbent | 90 | 56.7% [46.4%, 66.4%] — survived |
  | **confirm vs incumbent** | **480** | **51.5% [47.0%, 55.9%] — no verdict** |
  | regression vs `opp_v39` | 240 | 62.5% [56.2%, 68.4%], clears 50%; reference `aug7` 65.0% [57.8%, 71.6%] — overlapping, no regression |

  0 crashes for the challenger in every run (opp_v39: 382). Confirm per-map: **jackpot is the
  challenger's best map at 25/32 = 78.1%**, the only map that moved, and **no map regressed**.
- **Verdict under the standing rule: no verdict, therefore not promoted.** The incumbent stays
  `bots/aug7` at `a9d81a1`. The change is preserved at `bots/_fix_core00/` rather than deleted.
- **Why it is being escalated instead of dropped on the floor.** Everything the accept rule was
  built to reject is absent here, and everything it was built to protect is satisfied:
  - The a-priori prediction was **+1.7 points**; the measurement came back **+1.5**. This is not
    a change that "looked good and shrank" — it landed on its stated number.
  - The mechanism was measured directly rather than inferred from the win rate: a team's
    `titanium_collected` moved from **exactly zero** to normal, and the map's mirror seat split
    moved from 0/48 to 45.8%. Those are p-values in the 1e-14 range, not coin flips.
  - The pooled gate is simply the wrong instrument for a defect confined to 1 map in 15. It is
    not that the evidence is weak; it is that 480 matches over 15 maps cannot resolve two
    points, and no achievable sample would — halving the interval needs ~2000 matches, and it
    would still straddle 50%.
  - This project has already made this call once, deliberately: **v2's CPU guard was kept on a
    no-verdict** (`results.tsv`: *"no-verdict as predicted for an inert-locally change; kept as
    ladder insurance"*), and [HANDOVER.md](../HANDOVER.md) states the rule outright — *the
    accept gate is for strategy changes, not insurance changes*. A guard against a measured
    total-failure mode is the same category.
  Promoting it is nonetheless a human decision, not the loop's: it changes the submission
  candidate. **Recommended: apply.** Whether the pooled gate should be extended with an explicit
  per-map correctness clause is a program.md question for Magnus.
- **What the confirm's per-map table also says:** with the (0,0) bug removed, `jackpot`'s seat
  split is *still* skewed (28.1% seat A) because the **incumbent** on the other side is still
  broken there — which is the correct signature, and a reminder that a head-to-head seat column
  measures both bots at once. The maps still flagged with both bots healthy — archipelago 78%,
  atoll 28%, heart 31%, lighthouse 28%, fjordgate 75% — are **untouched by this fix** and are
  the open work.

### Finding — a Core at (0,0) is invisible to its own builders, and it costs the whole map

- **Date:** 2026-08-08 · found by chasing the `jackpot` seat wipeout; the first hypothesis was
  wrong and the measurement that refuted it is what pointed at the real one
- **The claim:** on `jackpot`, whose team-A Core sits at **(0, 0)**, team A delivers
  **exactly zero titanium for the entire match**, every match, in every bot we have. Not
  "less" — zero.
- **The evidence, in the order it arrived:**
  1. Mirror audit: seat A **0/16** on jackpot (see the audit entry below). Repeated in a
     second run at 0/8, and again at 0/48 — **0 for 104** in total, across three different
     bot generations (`aug7`, `probe_neutral`, and a modified `aug7`).
  2. `probe_neutral` — v1 with every absolute-direction bias removed, a different code
     generation — reproduces it exactly (0/32), and **all 32 games ended on
     `titanium_collected`**. So the deficit is economic, and it is not aug7-specific.
  3. Six single matches, `aug7` vs `aug7` on jackpot, reading the end-of-match JSON:
     `a_titanium_collected` = **0, 0, 0, 0, 0, 0**, against `b_titanium_collected` ≈ 4950.
     Team A ends with 4–8 buildings against team B's 39–96, and a final balance of ~2500 —
     which is 500 starting titanium plus 1000 rounds of passive income, i.e. team A spent
     almost nothing all game because it never earned anything.
- **The mechanism, and it is three lines of code:**
  ```python
  ct.write_store(SLOT_CORE_X, pos.x)          # the Core publishes 0 and 0
  ...
  if x > 0 or y > 0:                          # ...and no builder ever believes it
      self.core_pos = Position(x, y)
  ```
  All 16 comms slots start at 0 and hold non-negative integers, so **0 is indistinguishable
  from "nobody has written this yet"**. A Core at the origin publishes its position and every
  builder on that team reads it as no-data, for the whole match. Three things are gated on
  `core_pos is not None`: laying the trail conveyor in `_try_move` — **which is the only thing
  that ever delivers our titanium** (the dedicated harvester conveyor is verified dead code,
  see the entry below) — building sentinels, and heading home in `_pick_target`. Team A
  therefore builds harvesters that idle with nowhere to output, lays no conveyors, builds no
  sentinels, and collects nothing. The existing comment even flags the ambiguity and resolves
  it the wrong way: *"we skip storing (0, 0) unless the core really is there"* — the one case
  it doesn't handle is the Core really being there.
- **The whole field has this bug.** It is inherited verbatim from the organisers' shipped
  starter bot (`bots/starter/main.py:230`). Measured directly: `starter` vs `starter` on
  jackpot, seat A finishes with `titanium_collected` **0**, `units` **0**, `buildings` **1** —
  the bare Core. See [opponents.md](opponents.md); this is exploitable metagame information,
  not just our own bug.
- **The hypothesis this replaced, and why the refutation was worth its CPU.** The first
  candidate was that `get_position()` returns the 2×2 footprint's **NW corner**, which is not
  a rotation-equivariant reference point — the centre sits half a tile SE, so every
  core-relative gate is displaced by a fixed offset that does not rotate with the map. On
  jackpot the arithmetic looked damning: 5 legal tiles inside the return-home gate for seat A
  against 12 for seat B, ~11 sentinel sites against ~30. It was wrong. A build with both gates
  measured to the footprint centre instead (`bots/_diag_core`, integer-exact in doubled
  coordinates) moved **nothing**: jackpot 0/48 (unchanged), archipelago 72.9% vs 77.1%, atoll
  20.8% vs 31.2%, fjordgate 64.6% vs 66.7% — all within noise of the incumbent. Plausible
  arithmetic about a real asymmetry, and the asymmetry simply wasn't binding. The refutation
  is what forced the question "why is *collected* exactly zero rather than merely lower",
  which is the question that has only one answer.
- **What this does not explain.** `archipelago` (seat A 77%) and `atoll` (seat A 21%) are
  still unexplained and are **not** this bug — neither has a Core at the origin. They are the
  next thing to chase, and they are worth more in aggregate than jackpot was.
- **Method note:** the win rate could never have found this. A pooled metric over 15 maps
  shows a total wipeout on one of them as a couple of points of drag. The instruments that
  found it were the **per-map mirror seat table** and the **end-of-match JSON's per-team
  `titanium_collected`** — a process metric, not an outcome metric. When an outcome is
  extreme and stable (0 for 104), stop running more matches and go read the state.

### Measurement — mirror seat audit of the real rotation: one map is a 0/16 wipeout, and it is ours

- **Date:** 2026-08-08 · measurement only, **no code change**, no accept/discard
- **Why:** the per-map seat split of a bot against *itself* is this project's standing
  regression test for orientation bias (strategy-notes.md). Every previous audit ran on the
  eight invented maps, which were all rotational and mostly small. The pool has since cut over
  to the real 15-map competition rotation, so the test had to be re-run on the distribution we
  are actually graded on. A second motive: an earlier non-mirror run had flagged `jackpot`
  (~8% seat A), `heart` (~83%) and `atoll` (~17%), but that data was contaminated — the two
  sides were different bots, so a seat split and a strength difference are not separable.
  A mirror run separates them by construction.
- **Setup:** `arena.py aug7 aug7 --seeds 8 --jobs 8` — 15 maps × 8 seeds × 2 orderings =
  **240 matches**, identical code on both sides. Under a fair map and an orientation-neutral
  bot every row should sit near 50%.
- **Result — pooled:** seat A **124/240 = 51.7%** [45.4%, 58.0%]. **0 crashes.** Win
  conditions: `titanium_collected` 188 (78.3%), `core_destroyed` 40 (**16.7%**), `harvesters`
  7, `titanium_stored` 5. The harness reads a no-op as a coin flip, so the sanity check passes;
  and the `core_destroyed` rate reproduces the invented pool's null-control 16.7% **exactly**,
  which is a useful invariant — the Core-kill rate is a property of this bot, not of the pool.
- **Result — per map** (seat A share, Wilson 95%):

  | map | seat A | flag |
  | --- | --- | --- |
  | **jackpot** | **0/16 = 0.0%** [0%, 19%] | **decisive** (two-sided p = 3.1e-5; survives Bonferroni over 15 maps, p_adj = 4.6e-4) |
  | archipelago | 14/16 = 87.5% [64%, 97%] | suggestive (p = 4.2e-3, p_adj = 0.063) |
  | fjordgate | 12/16 = 75.0% [51%, 90%] | nominal only (p = 0.077, p_adj = 1.0) |
  | atoll | 4/16 = 25.0% [10%, 49%] | nominal only (p = 0.077, p_adj = 1.0) |
  | antler | 5/16 = 31.2% | not flagged |
  | heart | 7/16 = 43.8% | not flagged |
  | the other 9 | 8–11/16 | not flagged |

  Fifteen simultaneous 95% intervals produce ~0.75 false flags by chance, so read the p-values,
  not the flag column. Only `jackpot` is decisive; `archipelago` is worth a look; `fjordgate`
  and `atoll` are what a 15-map audit looks like when nothing is wrong.
- **Verdict on the contaminated flags:** `jackpot` **confirmed and worse than reported** (~8%
  → 0%). `atoll` confirmed in direction only, and not significant once you count the
  comparisons. `heart` (~83%) is **refuted** — 43.8% [23%, 67%], no detectable seat effect.
  That is the value of the mirror design: one of three "findings" was an artefact of comparing
  two different bots.
- **Read:** `jackpot` is 16×16 and **tile-grid-exact 180° rotationally symmetric** (verified by
  parsing the `.map26`; cores A=(0,0), B=(14,14), footprints map onto each other exactly under
  the rotation). A fair map plus identical bots plus 0/16 leaves only one conclusion:
  **the bot handicaps itself in seat A.** This is not an engine effect — the known engine
  first-mover edge favours seat A, and this is the opposite sign. It is the same bug class the
  v3/v4 work was built to kill, surviving in a place that audit never reached, because the
  invented pool had no corner Core.
  The leading mechanism, from reading the code rather than from measurement: the Core publishes
  `ct.get_position()`, the footprint's **NW corner tile**, and every builder treats that single
  tile as "where the Core is". The footprint's centre is at corner + (0.5, 0.5), so the corner
  carries a fixed (−0.5, −0.5) offset **that does not rotate with the map**. On jackpot it
  points off-map for seat A and into open ground for seat B. Hand-counting the two gates that
  consume it: tiles at d²≤8 (the return-home gate) number **5** for seat A against **12** for
  seat B; at d²≤18 (the sentinel-build gate) roughly **11** against **30**. Seat A's builders
  are being told to crowd into less than half the space and have a third of the legal turret
  sites.
- **Next:** diagnosed separately before any fix is gated (see the corner-Core entry). Note the
  size of the prize is bounded: jackpot is 1/15 of the pool, so even a perfect repair is worth
  ~2 points of pooled win rate — below what a 480-match confirm can resolve. The per-map seat
  table, not the pooled win rate, is the instrument that can see this class of bug, and that is
  an argument for running this audit every time the rotation changes.

### Diagnostic — aug7 on the real map rotation: 69.6%, not 80.5%, and still crash-free

- **Date:** 2026-08-07 · diagnostic only, **not** an accept/discard run and not a metric change
- **Why:** the real rotation landed in `maps/new-maps/` (f71614e) mid-session, while the
  parallel experiments were already running on the eight invented maps. Cutover is a
  between-tags operation ([runbook.md](runbook.md) §2), so the right move was to leave the
  metric alone and measure the gap explicitly rather than guess at it.
- **Setup:** `arena.py aug7 starter --maps maps/new-maps/*.map26 --seeds 8 --jobs 8`, n=224.
  Passing explicit paths means no protected file was touched and the standing metric is
  unchanged.
- **Result:** **69.6% [63.3%, 75.3%]** vs the invented pool's **80.5% [75.2%, 84.9%]** —
  intervals barely overlap, so the edge is genuine but roughly 11 points thinner than our
  headline. **0 crashes in 224 matches** (starter: 355), including `jackpot`'s literal corner
  Core and the five maps at ≥14% wall density. Weakest: `hive` 6/16, `archipelago` 8/16,
  `atoll`/`jackpot` 9/16. An earlier n=56 pass read 57.1%; that was noise, use n=224.
- **Read:** the two things this lineage was actually built on — crash-freedom and
  direction-neutrality — **transfer to the real distribution intact**, which is the outcome
  that mattered most and was genuinely in doubt (a corner Core is exactly the case the
  full-ring spawn scan was written for). What does not transfer is the size of the margin: a
  meaningful part of our 80.5% was earned against maps we invented, on which starter's
  weaknesses are presumably over-exposed. Treat 69.6% as the honest pre-ladder expectation.
- **Next:** re-baseline properly after cutover, and re-run the aimed-sentinel experiment
  specifically — a Sentinel's wall-ignoring line is worth much more at 30.8% wall density than
  at our inventions', so that null was arguably answered on the wrong distribution. Per-map
  tuning has a one-week shelf life given the weekly rotation; robust-across-maps changes keep
  their priority permanently.

### Finding — the harvester's first conveyor has never been built, in any version, ever

- **Date:** 2026-08-07 · found as a side-observation while discarding the conveyor-chain
  experiment; verified independently before being believed
- **The claim:** `_try_build_conveyor_toward_core` — the function that gives each newly built
  harvester its output conveyor toward the Core — is **dead code**, and has been since the
  organisers' shipped starter bot. The identical line is in `bots/starter/main.py:286`,
  `bots/v4/main.py:375` and `bots/aug7/main.py:379`, i.e. the entire lineage.
- **Verification:** instrumented copy (`bots/_probe_conv`), single matches across mid20,
  large30, hsym16, duel16. **24 calls, 0 legal, 0 conveyors built.** Target tile was the
  builder's own tile 18 times (`dist_sq=0`), diagonal or 2 steps away the other 6.
- **Cause — a grid-parity fact worth remembering:** `can_build_conveyor(pos, facing)` requires
  `pos` to be orthogonally adjacent to **the acting builder**, not to the harvester. The
  builder stands orthogonally adjacent to the harvester `H` (build requires that), and the
  code targets another orthogonal neighbour of `H`. The grid graph is bipartite, so **two
  tiles one step apart share no common orthogonal neighbour**: the target is either the
  builder's own tile (explicitly disallowed) or not adjacent to the builder. Always illegal.
  Generalised: **a builder adjacent to a building it just placed can never build anything
  orthogonally touching that building — it must move first.** This constrains every
  build-adjacent-to-a-building idea we might have, not just this one.
- **Why it has not hurt us — measured, not assumed.** `_try_move` lays a conveyor on the tile
  *ahead* before stepping onto it, so a builder is usually standing on a conveyor, and its own
  tile *is* orthogonally adjacent to the harvester it then builds. Instrumented across all 8
  maps, 3–4 seeds each, 30 matches: **264 harvesters built, 263 (99.6%) had an orthogonally
  adjacent friendly conveyor**, 233 of them by the earliest measurable round (the round after
  the build). One miss, on duel16. 0 lost, 0 unresolved.
- **Conclusion: do not fix it.** The bug is real, permanently non-firing, and completely
  masked. Deleting or repairing the function would change nothing measurable, and a change
  that cannot move the metric is not worth the risk of touching the submission candidate.
  This is the rare case where the correct action on a verified bug is to write it down and
  walk away.
- **Residual, unmeasured:** adjacency is necessary but not *sufficient* for delivery — a
  conveyor whose output side faces into the harvester won't accept from it. The probe measured
  presence, not accept-side correctness. Trail conveyors face toward the Core and harvesters
  round-robin across neighbours, so this is unlikely to bite, but it is a distinct question
  if anyone pushes further.
- **Note on the field:** anyone who started from the organisers' starter bot has inherited
  this same dead function. See [opponents.md](opponents.md).

### Discard — aimed sentinel placement is a perfect null, and the null is the finding

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** a sentinel is 30 Ti + a 20% scale tax — the most expensive irreversible
  decision the bot makes — and its whole value is *(position, facing)*, since it fires an
  unblockable line. The incumbent takes the first legal adjacent tile and faces
  `direction_to(core).opposite()`, i.e. the builder's incidental standing position picks the
  arc. `can_fire_from()` / `get_attackable_tiles_from()` exist precisely to evaluate a
  placement before paying for it, and nothing in the tutorials or our lineage uses them.
- **Change:** score all legal (≤4 adjacent tiles × 8 facings) pairs and build the best.
  Score per covered tile = proximity to our Core + alignment with the corridor toward the
  inferred enemy Core (point-reflection of our Core through the map centre), with tiles
  already inside an existing friendly sentinel's arc down-weighted to 0.4. Ties broken by
  shuffled iteration. `_run_sentinel` targeting deliberately left unchanged.
- **Result:** screen **56.2% [42.3%, 69.3%]** (n=48) — survived, leaning positive. Confirm
  **50.0% [43.9%, 56.1%]**, exactly 128–128 (n=256), 0 crashes both sides. **No verdict,
  therefore discard.**
- **Read:** this is a stronger null than the win rate alone shows, and that is the point.
  `core_destroyed` came in at **44/256 = 17.2%** against the null-change control's
  **16/96 = 16.7%** — the change produced *no detectable effect at all* on the one axis it was
  specifically designed to move. That distinguishes "didn't clear the bar" from "did nothing",
  and the two call for different follow-ups.
  The likely structural reason, per the runner's read: by the time a builder reaches the
  sentinel gate it has navigated to within dist²≤8 of the Core, where the tiles are already
  occupied by our own economy build-out — so the candidate set frequently collapses to a
  single legal position and the scorer only refines facing among options that were already
  narrow. **This was not instrumented** — no count of how often the scorer picked differently
  from the incumbent — so the mechanism is inference, not measurement.
- **Next:** do **not** try another arc-scoring function first; the flat `core_destroyed` rate
  says arc quality isn't the binding constraint. The cheap prerequisite is to instrument how
  many legal (position, facing) pairs a builder actually has at the sentinel gate. If that
  number is usually 1, the real lever is *where sentinels get built at all* (reserving tiles,
  or building them further out on the approach) and every arc experiment downstream of it is
  measuring nothing.
- **Method note:** the screen read 56.2% and the confirm read 50.0% — a textbook illustration
  of why the screen cannot promote and why "the number went up" is not an accept rule.

### Discard — deliberate harvester-to-Core conveyor chains cost more builder-rounds than they earn

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the highest-ceiling idea available. Crediting is delivery-only (measured,
  game-model.md): a harvester whose path to the Core never closes earns exactly zero, on the
  balance *and* on tiebreak #1. The incumbent has no deliberate chain-building at all — only
  incidental conveyors dropped on tiles a builder happens to walk over. Conveyors are also the
  cheapest thing in the game on cost-scale (+1% vs +20% for a builder bot), so plumbing should
  be cheap where builder-rounds are the real expense.
- **Change:** a per-builder state machine that, after placing a harvester, takes over that
  builder entirely until the chain is done: greedy staircase route toward the Core (axis with
  more distance remaining, ties random), each link's facing recomputed from its own position
  so corners stay connected, terminating on the Core / an existing building / a 200-round cap.
- **Result:** screen **54.2% [40.3%, 67.4%]** (n=48), confirm **45.3% [39.3%, 51.4%]**
  (n=256), 0 crashes both sides. **No verdict, therefore discard.**
- **Read:** the cost is builder-rounds, not titanium. Laying a chain runs ~2 rounds per tile
  (walk, then build) and monopolises one of only ~5 builders for potentially dozens of rounds,
  against an opponent spending those same rounds finding and building more harvesters. The
  `core_destroyed` rate (42/256 = 16.4%) sat right on the null-change control's 16.7%, so
  nothing about the game's character changed — this was purely an economic trade, and it lost.
  **The chains were never verified to complete**, so strictly this refutes "dedicate builders
  to plumbing", not "complete chains are worthless" — those come apart only if completion is
  measured, which it wasn't.
- **Next:** the same session's dead-code finding above (harvesters may already be served by
  incidental trail conveyors) is the cheaper way at the same underlying question, and is being
  measured directly rather than inferred. Third discard in a row for the shape "spend
  builder-rounds or economy on something else" — that pattern is now very well evidenced.

### Discard — demand-driven ammo conversion loses the same way a bigger buffer did

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (three hypotheses run concurrently in scratch dirs `bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the AMMO_BUFFER 20->50 discard refuted a bigger *standing* buffer, not
  better-*timed* conversion. `convert_ammo()` is usable the same turn and costs no action
  cooldown, so ammo can in principle be raised on demand: hold near-nothing while quiet, burst
  when a threat appears. Named as the explicit follow-up in that discard's "Next".
- **Change:** new store slot 4 carries a threat timestamp. Sentinels scan
  `get_nearby_units(dist_sq=get_vision_radius_sq())` (r²=32, same as their attack radius, so
  strictly earlier warning at no extra reach) and write `round + 1` on seeing any enemy unit.
  The Core reads it and targets 40 ammo (4 sentinel shots) if the sighting is <=5 rounds old,
  else 10 (one shot). Conversion still gated on `harvester_count >= TARGET_HARVESTERS` and
  still reserves a builder bot's cost before converting, both unchanged from the incumbent.
- **Result:** screen **41.7% [28.8%, 55.7%]** (n=48) — survived by the letter of the rule, and
  coincidentally the identical figure to the AMMO_BUFFER=50 screen. Confirm **46.1%
  [40.1%, 52.2%]** (n=256), 0 crashes both sides — **no verdict, therefore discard**.
- **Read:** two independent ammo-timing levers have now failed in the same direction, which
  makes this a pattern rather than one data point: at this bot's strength, ammo scheduling is
  not where the wins are. The experiment confounded two changes it shouldn't have — it both
  *lowered the quiet-phase floor* (20 -> 10) and *added a delayed burst*, so it cannot separate
  "holding too little ammo when first contact happens" from "the burst arrives a round late
  because store writes are buffered". On the mix: this session ran a **null-change control**
  (byte-identical copy of aug7 vs aug7, n=96) which gives the first real baseline for the
  win-condition mix — `core_destroyed` **16/96 = 16.7%**. Against that, the ammo run's
  **28/256 = 10.9%** is a *reduction* in decisive combat outcomes, and the H2 run in the same
  session sat at 17.2%, i.e. right on the control. So the cut ammo floor does look like it
  suppressed core kills — the CIs overlap at the edge (control [10.4%, 25.5%] vs
  [7.7%, 15.4%]) so this is suggestive, not established. Note also the mix is pooled across
  **both** bots in a match, so it can never be attributed to the challenger alone.
- **Next:** if ammo is ever revisited, the clean version is baseline held at 20 (identical to
  the incumbent) with a burst added *on top*, which isolates the burst from the floor cut.
  Low priority: two discards deep, the prior should now be that this lever is worth little.
  The general lesson generalises further than ammo — **an experiment that changes a floor and
  adds a mechanism at once is one experiment producing zero attributable answers.**

### Discard — lowering the small-map defense trigger also loses

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** strategy-notes.md's map-size section: a 14x area range (8x8-30x30) probably
  needs branched strategies, and small maps favour rushing since economy has no time to
  compound. Tried the cheapest version: switch to sentinel-building at 1 harvester instead of
  3 on maps <=150 tiles (tiny8 64, small12 144 -- 2 of 8 maps).
- **Change:** `target_harvesters(ct)` returns 1 below the area threshold, 3 above it. Used at
  both call sites (sentinel-build gate, navigate-to-core gate). Everything else unchanged.
- **Result:** screen vs incumbent: **35.4%, CI [23.4%, 49.6%] — refuted** (upper bound just
  under 50), discarded without a confirm run.
- **Read:** same mechanism as the scout-first discard just above, in miniature — cutting
  harvesters from 3 to 1 forfeits ~2 harvesters' worth of economy (each ~2.5 Ti/round once
  delivering) in exchange for a slightly earlier sentinel, and the economy loss outweighs the
  earlier defense even on the smallest maps. Combined with the scout-first result, this is a
  second, independent data point that this bot's economy-first shape is robust across the map
  size range — "small map = rush" from strategy-notes.md is not supported so far, at least not
  via this lever.
- **Next:** map-size branching on *something other than the harvester trigger* remains
  untested (e.g. sentinel placement radius, spawn aggressiveness, MAX_BUILDERS) if this is
  revisited. Lower priority now given two discards in a row on the small-map-rush thesis.

### Discard — scout-first before building is a decisive loser

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** open-questions.md asked whether "scout first, build later" (dodging early
  scale tax, per strategy-notes.md) beats building immediately — flagged explicitly as
  worth testing rather than assuming, against the official docs' opposite advice.
- **Change:** gate `_try_build_harvester` on `ct.get_current_round() >= SCOUT_ROUNDS` (20).
  Nothing else built (harvesters, sentinels) for the first 20 rounds either, since sentinels
  are already gated on harvester count.
- **Result:** screen vs incumbent: **8.3%, CI [3.3%, 19.6%] — decisively refuted**, discarded
  without running confirm (upper bound nowhere near 50%).
- **Read:** settles the open question outright, and confirms harvester ROI dominance
  (strategy-notes.md: payback ~8-12 rounds) beats the scale-tax-avoidance argument by a wide
  margin at 20 rounds. The official docs' "build aggressively early" was right about the
  direction, if not the reasoning given. Scale tax matters at the margin (which harvester to
  build, not whether/when to start) — it doesn't justify sitting on your hands.
- **Next:** the scale-tax discipline from strategy-notes.md (don't over-build builder bots,
  `destroy()` obsolete infrastructure) is a different claim than "delay everything" and isn't
  refuted by this result. Worth keeping separate in future tests.

### Discard — raising AMMO_BUFFER for sentinels backfired

- **Date:** 2026-08-07 · tested against the sentinel-first aug7 commit (a9d81a1), not v4
- **Hypothesis:** AMMO_BUFFER=20 was tuned for gunners (4 Ti/shot -> 5 shots buffered); a
  sentinel at 10 Ti/shot only gets 2 shots of reserve at the same number. Raising it to 50
  (5 shots, matching gunner's shot-count buffer) should sustain fire better in a fight.
- **Change:** `AMMO_BUFFER = 20` → `50`. Nothing else.
- **Result:** screen 41.7% [28.8%, 55.7%] (not clearly refuted by the letter of the screen
  rule, but already trending down); confirm **45.3%, CI [39.3%, 51.4%] — no-verdict**,
  leaning negative. Discarded, `git reset --hard`.
- **Read:** the mechanism assumed sustained-fire fights are common enough that a bigger
  buffer pays for itself. More likely what actually happens: most of the match nothing is in
  range, so a bigger buffer just means more Ti parked as idle ammo instead of building
  harvesters/sentinels/conveyors during the quiet phases — exactly the failure mode
  strategy-notes.md already called out for the starter bot's fixed top-up. Bigger ≠ better
  once the buffer covers a couple of shots; the quiet-phase opportunity cost dominates.
- **Next:** an adaptive buffer (top up more only when an enemy is actually visible) is the
  more promising version of this idea, per strategy-notes' "adaptive ammo" note — a fixed
  buffer at any size trades against economy growth. Left for a future experiment.

### aug7 — Sentinel-first defense: the untested strategy-notes guess held, hard

- **Date:** 2026-08-07 · `bots/aug7`, built on v4 · **Not yet submitted** (no platform account)
- **Hypothesis:** [strategy-notes.md](strategy-notes.md) flagged Sentinel as strictly better
  than Gunner for a static base defender (more dmg/round, better Ti-per-damage, more HP,
  2.5x the attack radius, unblockable by walls/units) except for 10 Ti lower entry cost and
  re-aimability — neither of which matters once a turret is placed and never moves. Marked
  "untested guess, needs a real A/B" in the notes.
- **Change:** one conceptual swap. `_try_build_gunner`/`_run_gunner` → sentinel equivalents
  at the same trigger point (`harvester_count >= TARGET_HARVESTERS`), same facing-away-from-
  core logic, same 18-tile-from-core placement gate, same `AMMO_BUFFER = 20`. The only new
  code: sentinels have no `get_gunner_target()`-style helper, so targeting scans
  `get_attackable_tiles()` for the first tile holding an enemy unit or building and fires
  there.
- **Result:**
  - **Screen vs v4 (48 matches): 64.6% [50.4%, 76.6%]** — 5 `core_destroyed` wins appeared
    where the v4-only baseline essentially never had any.
  - **Confirm vs v4 (256 matches): 68.4%, CI [62.4%, 73.7%] — clears the accept gate outright.**
  - 0 crashes both sides. Win conditions shifted hard: 24 `core_destroyed` (up from a
    background rate near zero), plus more `titanium_collected` wins too — sentinels aren't
    just killing cores, they're also denying enemy economy better.
- **Read:** the derivation held, and by a wide margin — this isn't a marginal tuning win,
  it's the biggest single-change jump since v1's crash fix. Best explanation: r²=32 vs r²=13
  means a sentinel covers a conveyor approach a gunner simply can't see, and the unblockable
  line means enemy builder bots can't screen it by standing in front of infrastructure.
  Reinforces the notes' broader point that the tutorials' Gunner-first framing is actively
  wrong for this game, not just suboptimal.
- **Next:** aug7 is now the strongest bot measured. Continue the loop from here — the ammo
  buffer (20 Ti = 2 sentinel shots) was left untouched for attribution; worth its own
  experiment now that sentinels are the default (open-questions.md: adaptive ammo).

### v4 — full direction-neutralisation: the fairness fix turned out to be a strength fix

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account) · **Current best**
- **Hypothesis:** v3's ring spawn removed only part of the measured seat bias (mid20 mirror
  0/32 → 28%, not 50%); carrying over the rest of probe_neutral's neutralisations — randomised
  movement tie-break, randomised ore-scan tie-break, shuffled build/heal scans — should finish
  the job. Expected mostly a fairness change, neutral-to-slightly-positive on win rate.
- **Change:** v2's CPU guard + the complete neutralisation set from probe_neutral. One
  conceptual change vs v3: "remove the remaining absolute-direction tie-breaks".
- **Result:**
  - **vs v3: 60.9%, CI [54.8%, 66.7%], 256 matches — clears the accept gate outright.**
  - vs starter: **74.2%, CI [68.5%, 79.2%]** (v1 was 59.4%), 0 crashes vs 535, tiny8 32/32.
  - Mirror seat split: mid20 53.1%, small12 46.9% — **fair**. tiny8 84.4% — engine effect,
    expected, unfixable.
- **Read:** the surprise is the raw strength gain. Best explanation: v1's fixed tie-breaks
  made every builder chase the *same* first-enumerated target, colliding and shadowing each
  other; randomising de-correlates them into better map coverage. (Also: on biased maps, half
  of all games were previously started from the handicapped seat.) A fairness argument found
  a play-quality bug — absolute-direction habits were costing games everywhere, invisibly.
- **Next:** v4 is the submission candidate. On approval: re-baseline on the real pool before
  any tuning (runbook.md).

### v3 — full-ring spawn only: the decomposition step

- **Date:** 2026-08-06 · superseded by v4 the same day
- **Hypothesis:** the NW-corner spawn scan is the dominant cause of the seat wipeouts.
- **Change:** v2 + spawn candidates = whole 12-tile ring (random choice), nothing else.
- **Result:** mirror mid20 seat A 0/32 → **28.1%** [16%, 45%] — most of the wipeout, not all
  of it. vs v2: 52.0% [45.8%, 58.0%], no-verdict (expected: the fix only pays on the map
  class that exposes the handicap). 0 crashes.
- **Read:** ring spawn is necessary but not sufficient; the residual bias lives in the other
  absolute-direction tie-breaks. Kept only as the attribution step for v4.

### Experiment — seat bias dissected: it was mostly us, and partly the engine

- **Date:** 2026-08-06 · `bots/probe_neutral` (v1 with every absolute-direction bias removed)
- **Design:** if the seat-A wipeouts survive direction-neutralisation in a mirror, they're
  the engine's; if they vanish, they were ours.
- **Result (mirror, 32 matches/map):** mid20 0/32 → **53.1%** and small12 → 46.9% — *ours*.
  tiny8 → **78.1% [61%, 89%] seat-A**, confirmed at 84.4% in the v4 mirror — *the engine's*:
  a genuine first-mover advantage on the 8×8 map that survives full neutralisation.
- **Mechanism found on the way:** `get_position()` is the Core footprint's NW corner, so the
  starter bot's `pos.add(d)` spawn scan reaches only the N/W sides of the legal 12-tile ring
  (`bots/probe_spawn`, tile-by-tile). One seat spawned toward the map corner, the other
  toward the centre, every game.
- **What this changes:** (1) absolute-direction habits are a class of bug, not a style choice
  — audit for them; (2) on tight maps, seat draw is real regardless of bot quality → find out
  how the ladder assigns seats within a best-of-five; (3) our mirror-fairness check (arena
  per-map seat split) is now a standing regression test for reintroduced direction bias.

### Experiment — titanium is credited on Core delivery, and only then

- **Date:** 2026-08-06 · `bots/probe_credit` / `probe_credit_nc` / `probe_idle`
- **Design:** one harvester + one dead-end conveyor (facing away from the core, output onto
  empty ground / off-map), then idle; core logs the balance every round. NC variant: no
  conveyor at all. Passive-only slope is 2.5 Ti/round; a credited harvester would add 2.5.
- **Result:** both variants, 990+ rounds: balance slope **exactly 2.500**,
  `a_titanium_collected` **0**. A dead-end chain and no chain are *identical*: zero.
- **Read:** **"titanium collected" = titanium delivered to the Core.** The tiebreak-#1
  counter and the spendable balance both move only on delivery. An unrouted harvester
  contributes nothing to tiebreak #1 or #3 and no income — it pads tiebreak #2 (harvester
  count) while costing 20 Ti and +5% permanent scale. Chain completion isn't an optimisation,
  it's the whole game. This also closes the loop on the starter bot's economics: its walking
  trails of toward-core conveyors evidently do deliver (balance reconciliation matches), so
  hypothesis (c) from open-questions held.
- **Aside, measured:** `can_build_conveyor()` permits a facing whose output is off-map.

### v2 — CPU-budget guard: bail at phase boundaries, not mid-statement

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** exceeding 10 ms CPU silently truncates the unit's round mid-statement —
  wasted round, possibly half-updated instance state. v1 never approaches the limit locally,
  so the guard should be inert here; its value is ladder hardware (Graviton3, unknown relative
  speed) and future heavier strategy code. Predicted before measuring: no local effect,
  vs v1 reads no-verdict ≈50%.
- **Change:** `_cpu_exhausted()` checks `get_cpu_time_elapsed()` ≥ 8000 µs between builder
  phases (priority: build > heal > move > share); first trip per unit reported to stderr.
  Nothing else.
- **Result:** vs v1: **52.0%, CI [45.8%, 58.0%]**, 256 matches, no-verdict — as predicted.
  vs starter: 56.6% [50.5%, 62.6%] (v1's edge retained). 0 crashes. Guard confirmed never to
  trip locally (zero CPU-GUARD lines across a full instrumented match).
- **Read / rule note:** program.md's gate (lower bound > 50%) is for changes claiming to
  improve play; applied to insurance changes it would auto-discard all of them. Accept rule
  used here, stated in advance: keep unless refuted (upper bound < 50%) or crashes appear.
  Deliberate, documented deviation — not a precedent for strategy changes.

### v1 — robustness only: don't let units delete themselves

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** the starter bot's uncaught exceptions are its single biggest weakness. The
  engine permanently deletes a unit on any escaping exception, so every crash is a unit lost
  for the rest of the match — not a skipped turn.
- **Change:** two things, nothing else.
  1. `run()` wraps a `_dispatch()` in `try/except Exception`, reporting only the first
     traceback per unit to stderr (so a per-round bug can't flood the log or eat the 10 ms
     CPU budget formatting tracebacks).
  2. New `in_bounds()` helper, checked in `_try_move()` before touching the engine.
     `_move_toward_target()` tries up to four directions, and tile queries like
     `is_tile_empty()` **raise** off-map rather than returning False — so every bot standing
     on an edge tile was rolling the dice on its own life.
- **Predicted effect:** large. Stated before measuring.

**Result — 256 matches (8 maps × 16 seeds × both seat orderings):**

| | v1 | starter |
| --- | --- | --- |
| Wins | **152** | 104 |
| Win rate | **59.4%**, 95% CI [53.3%, 65.2%] | — |
| Crashes | **0** | **515** |

Lower bound clears 50%. **Keep.**

**Read:** the hypothesis held, but the effect is *smaller than the crash count suggests*.
515 crashes over 256 matches is ~2 units lost per match per side — real, but with typical
end-of-match unit counts of 5–13 it's usually a wound rather than a kill. The exception is
small maps: on `tiny8` v1 went **31/32**, where losing two bots is losing the whole economy.
So the crash bug's cost scales inversely with map size.

**Worth not over-reading:** per-map splits here are 32 matches each, so their intervals are
±17 points. v1's apparent loss on `vsym16` (13/32) is well inside noise. Only the pooled
verdict is solid.

**New evidence on the seat question:** on `mid20`, seat A lost **0/32** — and v1 took exactly
the 16 of those where it happened to be seat B. Seat decided that map regardless of which bot
sat in it. Since v1 doesn't crash at all, this rules out "crashes cause the seat effect" and
points at an engine/layout interaction. `small12` behaves the same way (2/32). The earlier
`tiny8` wipeout, by contrast, has now vanished (46.9%) — that one *was* crash-driven.

**Next:** v1 is the new baseline. Real strategy changes should wait for `fcode maps sync`;
tuning against eight invented maps risks fitting the wrong distribution. Remaining robustness
work that's distribution-independent: a CPU-budget guard using `ct.get_cpu_time_elapsed()`.

### Baseline — shipped starter bot, measured locally

- **Date:** 2026-08-06
- **Not a submission** — this is the reference opponent everything else gets measured against.
  `bots/starter/main.py` is left exactly as `fcode starter` generated it, on purpose.
- **Setup:** mirror matches, `--tle 10`, on six self-generated maps spanning the pool's
  8×8–30×30 range (see [tooling.md](tooling.md)).

**Results — 5 mirror matches, one per map:**

| Map | Winner by | Units left (A / B) | Mined (A / B) |
| --- | --- | --- | --- |
| tiny8 | Harvesters (tiebreak) | 0 / 5 | 0 / 0 |
| small12 | Titanium collected | 0 / 10 | 0 / 4960 |
| duel16 | Titanium collected | 1 / 7 | 2480 / 2470 |
| mid20 | Titanium collected | 3 / 11 | 2470 / 2480 |
| wide30x14 | Titanium collected | 4 / 13 | 4960 / 2640 |
| large30 | Titanium collected | 12 / 11 | 7450 / 4980 |

**What this establishes:**

1. **Every match went to the round-1000 tiebreak. 6 of 6.** No Core was ever destroyed, in a
   mirror match or otherwise. This is strong support for the economy-first read in
   [strategy-notes.md](strategy-notes.md) — the tiebreak *is* the win condition in practice,
   and its first key is titanium collected.
2. **The shipped starter bot crashes constantly**, 2–9 uncaught `GameError: Position out of
   bounds` per match. Each one **permanently deletes that unit**. Two matches ended with a
   side on **zero units and zero titanium mined** — a total economic wipeout caused entirely
   by its own bug, not by the opponent.
3. Identical bots produce wildly asymmetric outcomes (0 units vs 10) purely from where the
   crashes happened to land. Variance in this game is enormous; **one match proves nothing**.
   Any future comparison needs many matches across many maps and seeds.

**The bug:** `bots/starter/main.py:391` calls `ct.is_tile_empty(next_pos)` without a bounds
check. `next_pos` is off the map whenever a builder is on an edge tile, and the call raises.
`run()` has no `try/except`, so the exception escapes and the engine deletes the unit forever.

**Next:** our v1 is the starter bot plus (a) a top-level `try/except` in `run()` and (b) a
bounds check before that call. Nothing else. If the baseline read is right, that alone should
be a large improvement, and it isolates a single change so the result is attributable.

---

### Seat matters enormously on some maps — measured, cause unknown

- **Date:** 2026-08-06
- **Setup:** `tools/arena.py starter starter`, 16 mirror matches per map (8 seeds × both
  seat orderings), `--tle 10`.

With **identical bots on provably symmetric maps**, the team that acts first (seat A) wins:

| Map | seat A wins | 95% CI |
| --- | --- | --- |
| tiny8 | **0 / 16** | [0%, 19%] |
| small12 | **0 / 16** | [0%, 19%] |
| mid20 | **0 / 16** | [0%, 19%] |
| duel16 | 9 / 16 | [33%, 77%] |
| large30 | 9 / 16 | [33%, 77%] |
| wide30x14 | 10 / 16 | [39%, 82%] |

Three maps are fair. Three hand the win to the second mover **every single time**.

**Ruled out:** map asymmetry. The generator's output was verified tile-by-tile — every map is
exactly symmetric under its declared transform (`asym=0`), with equal ore near each core.

**Not yet known:** whether this is (a) an engine turn-order advantage that only bites on
certain layouts, or (b) the starter bot's absolute-direction bias — it closes the x-gap before
the y-gap and scans `CARDINALS` in a fixed order, so under 180° rotation it genuinely plays
differently from the other seat. A symmetry-type probe was inconclusive: horizontal-mirror
gave 29%, vertical-mirror 54%, and the six rotational maps split 3 fair / 3 wipeout.

**What this changes right now, regardless of cause:**

1. **Never evaluate on a single seat ordering.** On half these maps it would produce a
   perfectly confident, completely wrong answer. `tools/arena.py` plays both orderings
   always, and reports seat split per map rather than pooled.
2. **Pooled statistics lie here.** The 96-match aggregate read 20.8% seat-A — a number that
   describes none of the six maps. Always decompose.
3. **Suspect absolute-direction logic in our own bot.** Whatever the cause, a bot whose
   behaviour depends on which way is "east" is a bot that plays two different games depending
   on which corner it spawns in. Prefer core-relative reasoning to map-absolute reasoning.
