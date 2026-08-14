# SWARM / MASS / BAIT-AND-AMBUSH — builder bodies in numbers and as sacrifices

**⚠ PARTIAL — written under a wrap call, 2026-08-14T18:00Z (`date -u`, same shell call as
`git log -1` → `e4111ce` @ 2026-08-14T20:00:16+02:00).** Survey-atlas contribution, one
family of a larger atlas. Read-only cut: no bot, arena, prereg or submission touched.
**Section 9 lists what remains unchecked** — several items are one grep away and were not
run.

**Scope of the family:** builder bodies used in numbers or as sacrifices — suicide swarms,
mass rushes at the core, bait bodies, rebuild-ambush, feeder targeting, body-as-shield,
`self_destruct()`, and the cost-scale economics of disposable bodies.

**Engine primitives this family runs on** (`CLAUDE.md`): body 40 HP · 30 Ti base ·
**+20% global additive scale each** · cardinal moves only · attack **2 Ti → 2 dmg on an
orthogonally adjacent BUILDING only** · heal 1 Ti → +4 HP · core 500 HP ·
MAX_TEAM_UNITS 50.

---

## 0. THE LOAD-BEARING FACT, VERIFIED — SCALE IS REFUNDED ON DEATH, INCLUDING BODIES

**The claim is true and multiply-sourced. The BUILDER-BOT half rests on a replay fit plus a
negative control, NOT on a direct probe — and that gap is stated here because three
separate docs queued the direct probe and nobody ever ran it.**

1. **Engine disassembly** — `docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md:154-159`:
   `get_scale_percent@0x11fb8` reads a **team-keyed** HashMap, *"its contribution removed
   when that team's **building** is destroyed"*. ⚠ The wording is **buildings-only**, and
   the same read carries the inverse warning: **destroying an ENEMY building lowers THEIR
   scale — it helps them.**
2. **⭐ THE BODY HALF — replay fit with a driven negative control**
   (`docs/research/gunner-vs-sentinel-pricing-2026-08-09.md:171`). The model
   `1 + .20·(bots+gunners+sentinels) + .05·harv + .10·launch + .01·(conv+split+barrier)`,
   **over LIVE entities**, matched **5,050 / 5,051 = 99.98%** of clean single-build rounds
   across 400 files (CATEG additive 17.05%, COMPOUND 9.78%).
   **TEETH, and this is what makes it evidence rather than a fit:** the `--corrupt=live`
   arm — *the same model with no decrement on death* — collapses to **50.66%**;
   `--corrupt=offset` collapses to 16.78%. **Builder bots sit inside the `.20` term**, so a
   dead builder's +20% is measurably gone.
   Corroborated independently at `docs/coordination.md:7396`: **9,689/9,689** clean
   single-build rounds match a single team-wide scale over CURRENTLY-LIVE entities, and
   **the cumulative model matched 0/4,310** on the rows where the two disagree.
3. **Timing — SAME-ROUND** (`bots/_probe_refund/main.py`, docstring is the spec):
   `SCALE 205.000 → 204.000` with the cost getters moving **inside the same `run()` call**
   ⇒ a builder can demolish and buy the replacement at the lower scale in one turn, and the
   discount is GLOBAL for the window. Magnitude honestly: a barrier/conveyor is +1% of BASE
   ≈ 0.3 Ti off a sentinel. It only pays on **+20%** entities — culling one surplus builder
   at scale 2.0 takes a sentinel **60 → 54**.
4. **Global-additive itself** — `bots/_probe_scale`: spawning ONLY builder bots drove scale
   100→200% and raised conveyor 3→6, harvester 20→40, launcher 20→40, **categories never
   built**; `observed == floor(scale × base)` for all 8 types every round.
5. ⛔ **`destroy()` CANNOT REACH A BODY.** Builder bots are units, not buildings; only
   `self_destruct()` does. **The direct probe — *"does `get_builder_bot_cost()` drop after
   `self_destruct()`?"* — was queued at `offensive-catalog-2026-08-09.md:64`,
   `multistep-plans-2026-08-09.md:256-262` and `loki-siege-spec-2026-08-09.md:395`, and was
   never run as its own probe.** `self_destruct` appears in exactly two bot trees ever:
   `bots/_probe_refund` (mentioned in the docstring, for the destroy contrast) and
   `bots/_v176idlecull` (§3 below).
6. **MAGNITUDE, BOTH DIRECTIONS — this is what makes disposable bodies "cheaper than they
   look" and also what has killed every plank built on it:**
   * `bots/_v176idlecull/main.py:308-317`: our scale runs **~377% and builder bots are 44%
     of it — 6.2/game × 20pp = 123pp, more than every turret combined** (sentinel 70 +
     gunner 30). Two culls = **−40pp** ⇒ every later build ~11% cheaper for the rest of the
     game.
   * Against that, `docs/coordination.md:7396`: **break-even on builder churn needs
     400–580 Ti built while the builder is dead** — self-defeating in most windows.
   * **And it runs symmetrically against feeder-killing:** `exchange-rates-2026-08-09.md:124`
     — ***"KILLING IS A REBATE; IMPRISONING IS NOT"***. A kill returns **−20% scale** to the
     victim, *"potentially exceeding the 30·S body destroyed"*, and
     **"never kill a capped opponent's builder — you are freeing their slot."**
     `docs/coordination.md:10661`: a 40 HP builder costs us **6 gunner shots = 24 Ti of
     ammo**; they replace it for ~30 Ti at 1 spawn/round ⇒ **straight builder attrition does
     not win.**

**⇒ ATLAS READING: the refund is REAL, SAME-ROUND, GLOBAL and largest on bodies (+20% each,
123pp of our 377%). Every plank built on it so far has died on MAGNITUDE, not mechanism
(§3, §4). And it is a two-edged fact: it makes OUR disposable bodies cheap and it makes
KILLING THEIR bodies a gift.**

---

## 1. SUICIDE-BODY RUSH
1. **Mechanism:** `self_destruct()` destroys the caller; **deals 0 damage** (engine;
   `self_destruct@0xe474`, self-only).
2. **STATUS: REFUTED BY RULE** — organiser nerf, *"removing builder self-destruct damage
   nerfs rushes"*.
3. **EVIDENCE:** `dirty-tricks-shortlist-2026-08-09.md:73`, `offensive-catalog-2026-08-09.md:82`
   ("Dead by rule, organiser-patched pre-inheritance"), `exchange-rates:145`.
4. **COUNTER-TECH:** n/a — nothing to counter.
5. **UNEXPLORED:** none. Closed by construction; do not spend a leg.

## 2. CHEAP-BUILDER SWARM / MASS RUSH AT THE CORE
1. **Mechanism:** buy N bodies at 30 Ti × scale, walk them at the core; each adds +20% to
   the one global additive factor.
2. **STATUS: REFUTED BY RULE + ARITHMETIC** (and separately refuted-INVERTED as a
   behaviour).
3. **EVIDENCE:** *"30 Ti + 20% scaling + 50-cap all anti-spam; **the 20th builder costs 958
   Ti**"* (`dirty-tricks-shortlist:74`, `offensive-catalog:83`). The cap is irrelevant to
   everyone: **median 8–9 units alive at r250, 0.0% of teams reach 45**
   (`docs/coordination.md` field census). Live builders are flat and symmetric —
   **US 4.57 @r100 / 5.16 @r200 vs THEM 4.44 / 5.20**
   (`spawn-budget-and-dispatch-2026-08-09.md:40`). Our own spawn budget is code-shaped, not
   game-shaped: `spawn_cap 5 → +REPLACEMENT_MAX 13 → +SURGE_EXTRA 18`, with **34.7% of games
   ending at exactly 5** lifetime spawns, median 8, mean 12.96, max 91.
   **"Builder kill-wave" is refuted and INVERTED**: spawns FALL into the kill window in every
   population **except US — we alone wave, 0.28 → 0.97** (`multistep-plans:§2 table`).
4. **COUNTER-TECH:** the field does not need one; the cost curve is the counter.
5. **UNEXPLORED:** nothing in the swarm direction. (QUEUE **#62 TINYECO62** — our opening
   spawns exactly 5 builders before the first harvester whether the map is 100 or 900 tiles
   — is the live descendant, and it points at FEWER bodies, not more; arena arm 51.0%,
   n=2,683.)

## 3. IDLE CULL — `self_destruct()` OUR OWN IDLE BODIES FOR THE REFUND (LOKI-48)
1. **Mechanism:** a builder idle ≥12 consecutive rounds with both cooldowns 0 self-destructs
   after r120, floor 6 living units — refunding its +20% to every subsequent build of every
   type.
2. **STATUS: BUILT, FIRED, REAL NEGATIVE — the largest measured negative in this family.**
3. **EVIDENCE:** `bots/_v176idlecull` (`doctrine.py:1520-1524`:
   `LOKI48_IDLE_CULL=True, IDLE_CULL_RNDS=12, IDLE_CULL_MIN_RND=120, IDLE_CULL_FLOOR=6`;
   logic at `main.py:308-336`). Arena arm vs `bots/_v171late160ammo`:
   **T = 33.5% (1,266 / 3,774)**, `scratchpad/overnight/IDLECULL.tsv` — launched
   2026-08-12T17:42:00Z, cancelled 20:04:22Z on request (`scratchpad/corefill_relaunch.log:235,377`),
   partial rows kept and readable. **Informative band at n=5,408 is 48.67–51.33**; the
   session's calibration cells passed that night (`NULL114 49.98`, `NEG114 36.32`) — this
   arm scored **below the intended negative control.**
   The PREMISE numbers were sound and are worth keeping: **25.76% of our builder-rounds are
   IDLE** with both cooldowns 0 and no verb emitted, and idle share is the SAME in wins
   (27.59%) ⇒ it is what our bot always does, not a losing-position artefact. **Nobody in
   the field does this:** across 25 live games, **86 undamaged GUNNER removals (turret
   walking) and just TWO undamaged builder-bot removals.**
4. **COUNTER-TECH:** none needed — the cost is self-inflicted. The in-tree hazard is named
   in the source comment: *"a dead builder cannot heal, peck, seal or rebuild, and our raid
   IS builders."*
5. **UNEXPLORED:** whether a **much smaller dose** (cull 1, very late, only with the raid
   ladder closed) sits anywhere above the band — the arm as fired had no dose ladder.
   ⚠ And the arm's control was `_v171late160ammo`, not the plain incumbent.

## 4. THE DESTROY-TO-PRUNE-SCALE FAMILY — QUEUE #27 (family note) AND #60 (live member)
1. **Mechanism:** demolish our OWN spent buildings so their contribution stops taxing every
   subsequent build. `destroy()` is free, no cooldown, unlimited per turn, allied buildings
   on an orthogonally adjacent tile only.
2. **STATUS: two refuted, one WITHDRAWN, one ⭐⭐⭐ QUEUED AND NEVER BUILT.**
   QUEUE **#27** exists as the family row *"read this before proposing a fourth"*:
   ```
   E-22.3   LOKI-2 destroy/scale-prune  REFUTED    median 2 prunes vs 300-590% scale
   LOKI-43  LAUNCHRENT                  WITHDRAWN  ~12pp of scale, ~24 Ti — below the band
   LOKI-48  IDLE CULL                   (see §3)   96pp of scale, 6.8 culls/game
   ```
   **The magnitude is the whole question in this family** — and LOKI-48, the one member
   whose magnitude was an order larger, is the one that measured 33.5%.
3. **EVIDENCE for the live member, QUEUE #60 "RENT, DON'T OWN":** Juusto ran **403 launchers
   in 110 games, 402 of them demolished at an age of exactly 2 rounds** (p25=median=p75=2),
   3-round cadence, **+132 Elo in 11.7 h** (`BOOK-juusto-2026-08-14.md:20,203`). Our own
   tree: **`ct.destroy(` and `ct.can_destroy(` appear ZERO times across all four modules**
   of `_v223sealrepair` (v140) — all 11 textual hits are comments, including `main.py:256`
   which **writes the mechanism down**: *"dies (destroying an entity removes its
   contribution), so surplus bank…"*. Our launcher DEATHs are enemy kills, not demolitions
   (v104 329/2125 · v114 59/333 · v125 76/371 · v140 1/17). **Why it is not the arm the s37
   sweep rejected:** that sweep's −6.34pp launcher premium (`LAUNCH0 − BOTH0`, n=5,408/arm)
   **IS the standing scale contribution of a launcher we KEEP** — a rented one pays none of
   it. **Limit in the row: the TITANIUM is not refunded, only the scale** (~73+ Ti/game at
   Juusto's rate, in the r0-50 window where our kill is bought).
   **The F30 API census prices the ceiling:** our v104 build mix is **+316% gross per game**
   (builder_bot 6.97×20% = +139.3 · sentinel 4.49×20% = +89.8 · harvester 5.78×5% = +28.9 ·
   conveyor 23.69×1% = +23.7 · gunner 0.78×20% = +15.7 · launcher 1.19×10% = +11.9 ·
   barrier 6.25×1% = +6.2), *"at +316% a 30 Ti sentinel costs 125 Ti"* — but
   **`destroy()` reaches ≈+59% of it, not +316%, because bodies are units.**
4. **COUNTER-TECH:** Juusto ships it against us today. Nobody counters it.
5. **UNEXPLORED:** the whole of #60 — first read should be the **SCALE CURVE**
   (`get_scale_percent()` at r50/r100/r150 vs control), never the win rate.

## 5. SPAWN-RING BODY COLLAR (Loki-3) — bodies parked on the enemy core's ring
1. **Mechanism:** a builder body standing on a core-adjacent tile makes `can_spawn(tile)`
   False; the core needs one free tile to spawn at all.
2. **STATUS: MEASURED — the blocking half VERIFIED, the "lock" REFUTED as stated, the
   buyable effect is ONE body. Shipped in BARRIER form, not body form.**
3. **EVIDENCE** (`loki-arsenal-pricing-2026-08-09.md:326-370,640-700`):
   * **1a VERIFIED: 2,405,604 body tile-rounds, 0 spawns** (own + enemy), of which
     **394,970 enemy-body tile-rounds and not one spawn.** Bodies block 1:1.
   * **1b REFUTED: occupancy ≠ blocking.** **40.1% of all spawns land on a conveyor tile**;
     only **8 of 14** observed occupant classes block.
   * **The buyable number — one body, and only one:** 25-round core-death hazard by hostile
     bodies on their ring, rounds < 250:
     `j=0 → 2.24% [2.20,2.29] (488,818 exposed) · j=1 → 4.77% [4.59,4.96] (50,872) ·
      j=2 → 4.01% (6,779) · j=3 → 2.91% (654)`.
     **One body DOUBLES the hazard, CIs disjoint. The second adds nothing, the third is
     baseline.** *"If LOKI-2 is 'close the ring right now', the corpus supports the RIGHT
     NOW and not the CLOSE."*
   * **Two labelled causal warnings:** observational — a body on their ring is also a
     **marker** that we are already winning there; **the 2× is an upper bound.**
   * **1c NEEDS PROBE: the own-bodies full 12/12 lock has NEVER occurred in 2,710 ladder
     sides — max ever 6/12, n=4.** `bots/_probe_jail` covered the 9-of-12 case vs a static
     victim; 12/12 against a defender that steps off is unpriced.
   * Earlier positive: a body on a ring tile → `can_spawn` false **1:1**, and a dumb
     park-bot **won 9/12** (`dirty-tricks-shortlist:45`).
   * ⚠ **`loki-arsenal-pricing:341` also records: "Do not build partial spawn starvation" —
     holding phase fixed in 50-round bins, the spawn rate is FLAT across every blocking
     level from r50 onward.**
4. **COUNTER-TECH:** the shipped collar is **barriers**, not bodies
   (`LOKI_BARRIER_SEAL_ON`, ablation-validated at **−10pp** when removed — one of our two
   biggest assets). `_v185collarvol` (LOKI-47 COLLAR VOLUME) was **cancelled on dose**:
   barriers moved **3.90 → 4.37/game, inside 1 SE**, and the diagnosis is
   ***"THE COLLAR IS OPPORTUNITY-LIMITED, NOT BUDGET-LIMITED — there are exactly eight
   seats"*** (`doctrine.py:1578-1585`); `LOKI_COLLARVOL_HOLD` is a measured null
   (3.88/g vs parent 3.90).
5. **UNEXPLORED:** (i) the **12/12 own-body lock probe** named above — one match, no ladder
   exposure, metric = the victim's `get_unit_count()` stops rising; (ii) whether ONE body
   deliberately parked early (the only supported dose) beats the barrier seat it would
   compete with — the two have never been run against each other.

## 6. BAIT BODIES (ammo-drain, interceptor saturation, honeypots)
1. **Mechanism:** stand something in front of their turret so they spend ammo on it. Bodies
   have 40 HP; barriers have 30 HP for 3 Ti.
2. **STATUS: REFUTED, with an exact carve-out — bodies are BAD bait, buildings are GOOD
   bait; and the whole drain channel is a POWERED NULL.**
3. **EVIDENCE:** *"Sharpest single number found: bodies are bad bait, buildings are good
   bait"* — a barrier costs 3 Ti and ~17 Ti of enemy ammo to remove (**5.6:1 for us**); a
   builder costs 30 Ti and ~22 Ti to kill (**0.74:1 — a losing trade**)
   (`multistep-plans:96-100`). `exchange-rates:143` restates it: **"Builder bots as ammo
   bait are 0.8:1, a loss. Barriers are the only profitable bait."** Our **11,895 corpus
   forward throws were spending 30 Ti bodies at negative exchange — that is why no drain
   ever accumulated.**
   **The drain pump itself is refuted on discriminating cuts** (598 games, 7
   building-shooters, `drain-discriminator-2026-08-09.md` via `loki-siege-spec:200-210`):
   their income delta **−2%, CI excludes any drain above ~11%**; they spend LESS ammo when
   offered bait; theoretical ceiling **0.49 Ti/rd = 5.1% of their income**; **placebo kills
   the win association — shots into EMPTY tiles (purest enemy waste) predict our WORST
   outcomes, −0.257.** Survivor: **healed share at fixed volume, +7pp win, p=0.045, via
   +1.69 Ti/rd to OUR economy** ⇒ *"heal what you already built, never build things to be
   shot."*
   **Interceptor-saturation bait is DEAD:** observed **min inter-throw gap is 1 round for
   every throwing opponent** (launch cooldown 1) — no capacity to saturate.
4. **COUNTER-TECH — and it runs in our favour:** seven-plus teams dump ammo into healed junk
   anyway. **One Ouroboros gunner put 677 shots = 2,708 Ti of ammo into a single healed 3-Ti
   conveyor**; Powerpuff 634, OopsGotYourElo 531, Leviathan 446, Lunds 428, KCM 427.
   **Dead vs Memtrace, Team 48, Askar, Banminary, Bisons, gsxWins, Focalground** (1–7%
   non-core building shots — nothing of ours is ever in their line).
5. **UNEXPLORED:** **panic-build inflation** — bait them into building a turret to add
   **+20% to THEIR scale** (the inverse of #60). Listed in `multistep-plans` P-D and never
   costed. Distinct from the refuted *"force them to heal"*, which inverts 2.2:1 against us.

## 7. BODY-AS-SHIELD / BLIND THEIR GUN WITH THEIR OWN BODY — QUEUE #10
1. **Mechanism:** a gunner's shot is a straight line that does NOT pierce; one body in the
   lane blanks it. Our launcher throws a **kidnapped enemy** builder onto the tile their own
   gunner is aiming through — 0 ammo, one throw, costs them a unit's turn AND their turret's
   output.
2. **STATUS: QUEUED, NOT SHIPPED (QUEUE #10, GREP PASS re-verified vs v140).** The barrier
   proxies have been screened; the body form has not.
3. **EVIDENCE — engine-probed, `turret-line-blocking-2026-08-09.md`:**
   * **GUNNER: BLOCKED.** Within-subject, same turret/facing/target, only the blocker
     changes: `can_fire` **True → False**; clear case landed −7 = `GUNNER_DAMAGE`.
   * **SENTINEL: PASSES THROUGH.** A real shot landed **−18 = `SENTINEL_DAMAGE`** through
     **our own builder bot AND our own barrier** on the line; pass-through friendlies took
     **zero** damage (builder 40→40, barrier 30→30). ⚠ **A friendly standing ON the TARGET
     tile IS hit, own team included** — the D1×S4 friendly-fire constraint.
   * **`get_attackable_tiles()` returns the target in BOTH the clear and blocked case — the
     raw pattern advertises coverage the gunner cannot deliver.** Site with
     `can_fire_from`, never the pattern getter.
   * ⛔ **STATED LIMIT AND IT IS THE PLANK'S FOUNDATION: "Enemy entities as blockers were
     NOT tested for either turret."** The gunner docstring says "builder bots and buildings"
     without qualifying team, so enemy blocking is **expected but unverified**.
   * Barrier-form proxies, corefill n=5,408 each: **GUNBLANK 52.11% (LOKI-26, 3 Ti barrier
     on an enemy gunner's axis) but GUNBLANKREP 50.30% on replication** — discovery run was
     chosen from 18 arms and is biased up. **GBNOSHIELD 51.02%** (LOKI-46: drop the
     shield-required clause; **measured, dropping it raises the dose 4.2×, 0.20 → 0.83
     barriers/game**, `doctrine.py:1563-1590`). ⛔ **GUNBLOCK was CANCELLED ON DOSE: ZERO ray
     barriers in 25 live games** against 4.68 enemy gunners/game — *"its 32% score is
     uninterpretable and I refused to read it."*
4. **COUNTER-TECH:** sentinel-armed opponents are immune to lane-blocking by construction —
   a sentinel ignores obstacles. Our own barrier collar has the same property against us
   (`_v185collarvol/doctrine.py:1214-1216,1332`: *"the collar blocks LOS so a GUNNER ray
   dies on our own wall… a Sentinel shoots THROUGH the seal into the Core"*).
5. **UNEXPLORED:** (i) **the enemy-blocker boolean** — one probe, and #10 cannot be built
   honestly without it; (ii) the decoder question is unsettled — `tools/loki9_facing.py`
   computes EXACT-RAY collinearity, the plank as written wants `ALIGNED_DEG=45` tolerance;
   **pick one and say which**; (iii) body-blocking with OUR OWN body (a shield in front of a
   valuable unit) is nowhere in the corpus and nowhere in the queue.

## 8. REBUILD-AMBUSH — QUEUE #13
1. **Mechanism:** after we destroy an enemy turret, their builder must walk back to that
   tile to rebuild it — a predicted arrival at a known tile, which this game almost never
   offers.
2. **STATUS: ⭐⭐ QUEUED, base rate MEASURED, never built** (GREP PASS re-verified vs v140:
   we keep no memory of a tile we destroyed and never revisit one).
3. **EVIDENCE — 15,958 of our turret-destructions:** **22.6% produce a rebuild EXACTLY on
   the destroyed tile within 25 rounds · 33.8% within d²≤2 · 42.5% within d²≤8.**
   Conditional on any rebuild: **35.2% land on the rubble, 52.6% within d²≤2.**
   ⇒ **~1 destruction in 4.4 produces a same-tile return.** ⛔ The row's first version quoted
   **65.0%**, which is P(they build a turret ANYWHERE) — a different quantity; the side lane
   caught it. **Our opponents rebuild in place far more than the top tier's do — 22.6% vs
   13.0% on-tile — so this is worth MORE to us than to them.**
4. **COUNTER-TECH:** the top tier already relocates rather than rebuilds in place (13.0%).
5. **UNEXPLORED — and the design fork is the whole row: NAME THE KILLING INSTRUMENT.**
   If the rebuilder is killed by **builder melee**, the ambush pays the cost that killed
   counterbattery — `_raid_act` returning True **RETURNS FROM THE TURN**, so every attack
   round is a spent move round (`_v150cbturret` measured **45.2%, core kills 0.82×**).
   If it is killed by **a turret already covering the rubble tile**, it is genuinely free —
   and the 22.6–33.8% band decides siting and payload at once. Neither branch has run.

## 9. FEEDER TARGETING — KILL/EVICT THE BUILDER THAT FEEDS THE TURRET — QUEUE #45
1. **Mechanism:** vs point-blank creepers the turret is a renewable resource and the 40 HP
   builder feeding it is not.
2. **STATUS: QUEUED, ITERATION 1 READ OUT — mechanism works, EXPOSURE-STARVED (dose bar NOT
   met). Iteration 2 forked to launcher eviction and is gated.**
3. **EVIDENCE:** LingLing40 v40 — **80 siege turrets, median d²=5 from OUR core, 45 at d²≤5,
   14 at d²≤2, 58 of 80 gunners**, walking a ladder tile-by-tile (r89→r112 in one game) with
   **rebuild latency 1–2 rounds**; team lazy v222 independently — **48 siege turrets, median
   d²=5, 31 at ≤5**. Two teams, one shape, map-controlled. ⇒ **every turret we kill is
   refunded before our next action; we are paying 2 Ti/swing into a renewable resource.**
   **DOSE (`docs/prereg/DOSE-feeder45-2026-08-13.md`, `bots/_v198feederfirst`,
   `LOKI_FEEDER_NEAR_DSQ=8`, fixture `bots/_probe_creeper`): FEEDER45 fired in 1 of 16
   games; off-branch control 0/4.** Cause (a) confirmed **by construction**:
   `get_gunner_target` offers no target choice, so feeder-first governs **SENTINELS only**,
   which are rarely sited at the creep arrival.
   **⭐ TWO ENGINE FACTS BANKED BY THAT LEG, and they close a road:**
   **builder melee CANNOT target an enemy builder bot** (`can_fire=False` on an adjacent
   enemy builder, **every occurrence**; predicate-level — ungated `fire()` untested), and
   **class attrs don't share across units.** Corroborated corpus-side:
   **20,929 builder-bot deaths with NO damage value of 2 anywhere** — *"builders never kill
   builders, empirically"* (`builder-death-attribution-2026-08-09.md`).
   ⇒ **THE ONLY ANTI-FEEDER TOOLS ARE TURRET FIRE AND LAUNCHER EVICTION.**
   Turret-side arm exists and is null: **HEALERFIRST (`bots/_v174healerfirst`,
   `LOKI46_HEALERS_FIRST=True`) = 50.80%, n=5,408**, **dose-CONFIRMED (30 vs 19 builder
   kills) with the recorded cost that explains the null — own sentinel losses 18 vs 13.**
   ⛔ **AND THE REBATE APPLIES HERE:** killing their feeder hands them **−20% scale** and
   frees a unit slot (§0.6) — which is exactly why iteration 2 prioritises **eviction at 0
   ammo** over the sentinel path's 30 ammo/feeder-kill.
   **TWO GATES, NOT ONE:** ablating `LAUNCHER_MIN_RND=160` (`doctrine.py:1536`) can null
   while `LAUNCHER_RESERVE=80` (`doctrine.py:965`) still starves the build — the Leviathan
   autopsy shows the bank **PINNED AT 12 Ti in exactly the sieged games**, where cost+80 is
   unreachable.
   **Named customers (s39):** **Bisons v8** — their entire damage output walks to our core
   as an **unescorted, melee-less builder at r25-33** on an opponent-blind script, and they
   have built **ZERO launchers in 892 archived games**; **0033** — **0 launchers in 2,307
   archived games** (opponents built 751 in the same files), builder standing in our spawn
   ring from **median r43 (p10 r13)**.
4. **COUNTER-TECH — the field runs the eviction half against US at scale:**
   `throws.tsv`, `ourver`≥125 — **Jython 32.9 throws of our builders per game over 125
   games · Focalground 24.7 over 55 · LingLing40 22.1 over 85; 8,274 total.** We are being
   farmed by a plank we already own the parts for. And the **camp class** out-trades our
   pecks 8:1 by healing (4 HP/Ti vs our 2 Ti for 2 dmg).
5. **UNEXPLORED:** eviction's mechanism metric is **NOT builder deaths** — it is
   **feeder-ABSENCE rounds near their siege turret / rebuild latency stretched off its
   1–2-round baseline.** (Do not cite the EXILE displacement signal, +0.265pp, as the
   mechanism — it measures vanish-undamaged, a different quantity.) A dose must log the
   **gate arithmetic per round** (bank vs cost+reserve vs round-gate) so a no-fire attributes
   to a named gate.

## 10. FORWARD EVICTION LAUNCHER — QUEUE #58 — ⛔ REFUTED AS DESIGNED, LIVE
1. **Mechanism:** station a launcher at THEIR core in the kill window and throw their
   heal/repair staff off the ring (pickup d²≤2, 0 ammo, no team check).
2. **STATUS: REFUTED ON A PINNED LIVE LEG, s40 2026-08-14T17:04Z. DO NOT REBUILD THIS
   APPLICATION.**
3. **EVIDENCE:** pinned vs `0033`, 5 matches / 25 games, pin id `353429e5`, `oppver`=v57 on
   all five, `ourver`=v144 on all five, **PIN ALARM CLEAN**. P1 registered at **>1.0
   evictions/game; MEASURED 0.04 — ONE eviction in 25 games, a 25× miss.**
   ⭐ **The attribution splits and that is what the leg bought: the PLANT fired and the THROW
   did not.** Launchers built/game **1.240 (31 across 9 of 25 games) vs v140's 0.341 —
   3.6×.** ⇒ **the binding constraint is PICKUP OPPORTUNITY, not planting:** 0033's builders
   never enter the d²≤2 envelope, which follows from their core-kill being **100% turret
   fire, `batk_core` = 0 in 246/246 archived games in EVERY era.** Local arm **EVICT58 49.2%,
   n=1,000**. Standing-launcher price for context (s37 sweep, n=5,408/arm):
   **LAUNCH0 52.77 · LATE160 51.42 · LATE80 50.74 · BOTH0 46.43 ⇒ −6.34pp premium, earlier
   monotonically worse.**
4. **COUNTER-TECH:** n/a — **the failure is OPPONENT-SHAPED**, not mechanism-shaped.
5. **⛔ SCOPE A READER MUST NOT COLLAPSE:** the **eviction MECHANISM is untouched** (three
   opponents run it against us at 22–33 throws/game), and **a HOME-side eviction launcher
   (#47's territory, vs opponents whose builders DO come forward) is a different question
   this leg says nothing about.** ⭐ **The asset that survives: the 3.6× plant rate
   LIVE-VALIDATES the conditional-launcher infrastructure** (approach trigger, cap-1 live
   census, Ti floor, forward siting) — any future launcher plank inherits a WORKING PLANT
   for free.

## 11. THE BODY AS A WEAPON (melee payload forward)
1. **Mechanism:** 2 Ti → 2 dmg on an orthogonally adjacent **building** only.
2. **STATUS: REFUTED WITH EXACT SCOPE — dead as a core-killer, dominant as a demolition
   channel.**
3. **EVIDENCE:** **1.00 HP/Ti — the weakest positive trade in the game**
   (`exchange-rates:20`; barrier 10.00 HP/Ti, heal 4.00, sentinel 1.80, gunner 1.75).
   **Builder melee is 3.0% of top-tier kill damage** (gunner 57.6% / sentinel 39.4%), and
   the **median builder attacks on a dying core is 0 in EVERY population**
   (`multistep-plans:§2`); `cad-core-kill:22` agrees at **0.2%**. ⇒
   ***"Builder-body anything forward: 0.74:1 as bait, 3% of kill damage as a weapon.
   Builders forward are couriers and constructors, never payloads."***
   **BUT — whole-archive census, 8,663 platform replays** (`building-attackers-2026-08-10.md:445`):
   `builder attack 2,372,822 events → core 17.32% · turret 17.72% · econ 59.82% · barrier
   3.81% · own-side 0.97% · empty 0.35%` ⇒ **the builder-attack channel carries the majority
   of all building damage in this league and is 81.4% non-core.** Bodies are demolition
   tools.
4. **COUNTER-TECH — ⭐ THE IMMUNITY THEOREM, and it is the hard ceiling on every mass-body
   assault** (`exchange-rates:64-80`, `[V]`-verified against `is_tile_passable` TY:345-348):
   builders **may stand on their own core**. Two healers on a 1×1 repair **8 HP/round for
   2 Ti** against the two attackers they leave room for dealing **4 dmg for 4 Ti** ⇒
   **net HP never falls, and since builders cannot attack builders the healers cannot be
   removed either.** On the 2×2 core: **four healers = +16/round against a theoretical
   maximum 16 dmg/round from all 8 ring tiles — exact standoff; a FIFTH healer makes the
   core mathematically unkillable by builders (20 vs 14), costing them 5 Ti/round against
   our 14. Only turrets and launchers break it.**
   Chain-sizing bound (`loki-siege-spec:350-362`): cap the turret file at **~3** — a
   6-sentinel file loses **5.4:1** (682 Ti ammo vs 298 Ti sentinels) against a maxed guard,
   while **N=2 already nets +7.3 HP/round against the MEASURED field detail (2.68 adjacent,
   10.7 HP/round)**. *"Two sentinels beat most of the ladder's actual defence; six lose to a
   theoretical maxed one — and the cap is rarely manned."* If an opponent DOES man it, the
   answer is **screen suppression, never a bigger file**: **96 Ti to clear four healers vs
   780–2,500 Ti to grind through them.**
5. **UNEXPLORED:** whether OUR OWN core is worth screening this way is a defence question
   under `DEFENCE_ADMISSION_BAR` and has never been put.

## 12. SACRIFICE-PREP (feed units to set up a commit)
1. **Mechanism:** spend bodies before a commit to buy position/scale/tempo.
2. **STATUS: CORPUS NULL.**
3. **EVIDENCE:** *"winner-side loss curves monotone, peak AFTER first contact; nothing spent
   up front"* (`multistep-plans:§2 table`, `:256`). The scale-deflation variant survives only
   as the un-run `self_destruct()` probe of §0.5.
4. **COUNTER-TECH:** n/a.
5. **UNEXPLORED:** the probe in §0.5.

---

## 13. TWO CROSS-CUTTING FACTS THIS FAMILY KEEPS TRIPPING OVER

* **OUR BODIES ARE NOT ABSENT WHEN WE LOSE** (`CORE-DEATH-BUILDER-STATE-2026-08-11.md`,
  4,504 games with exactly one core death). The "we throw our bodies away forward" thesis was
  pre-registered by the side lane and **fails on its own discriminator**: at T−1 our builders
  alive are **median 5.0 in BOTH losses and wins** (mean 4.43 loss vs 5.20 win — a 0.78-builder
  difference), with **0.38 builder deaths across the entire 40 rounds before our core falls**,
  only 16.8% of them forward. The one bias runs in the thesis's favour (losses run later,
  median T 201 vs 165) and it still fails.
* **OUR BODIES NEVER DIE UNDAMAGED, AND ONLY BECAUSE OF A `try/except`**
  (`undamaged-builder-deaths-2026-08-10.md`): **0 of 539** of our builder removals across 235
  v102 ladder games left with positive HP, against a **FIELD control of 2,636 / 25,466 =
  10.35%** in 12.53% of 4,870 games. Instrument shown to fire on our own rows (strip negative
  HP deltas → 539/539). ⇒ **their bodies are crash-fragile and ours are not** — the asymmetry
  every crash-induction plank in this family rests on.
  Attribution of our body deaths: **enemy gunner 82.0–83.2%, enemy sentinel 15.6–17.0%,
  own-turret friendly fire 0.12–0.14%**, with **63.2–65.3% of the killing gunners standing
  within d²≤32 of OUR OWN core** (`cover-and-dodge-cuts`, reproducing
  `builder-death-attribution` independently on a different join).

---

## 14. WHAT REMAINS UNCHECKED — the wrap cut this short

1. **The `self_destruct()` → `get_builder_bot_cost()` probe has still never been run.**
   It is the ONLY direct test of the body half of the scale refund; §0 rests on a replay
   fit + `--corrupt=live` control instead. **One match. Highest value-per-minute item here.**
2. **`docs/research/WHAT-WOULD-MOVE-THE-NEEDLE-2026-08-11.md` and
   `SLATE-five-experiments-kill-score-2026-08-11.md` were opened but only keyword-scanned** —
   neither yielded a family hit on the grep, and neither was read in full. If a bait/swarm
   idea is in them, it is not in this atlas.
3. **`IDEAS-head-to-head-2026-08-11.md` read only to line 60** (IDEA 1 and IDEA 2); the side
   lane's three ideas were not reached.
4. **`kill-timing-doctrine-2026-08-09.md` and `cad-core-kill-2026-08-09.md` were only
   spot-read.** The headline *"how many builders to kill a 500 HP core and in how many
   rounds"* is answered here only INDIRECTLY (immunity theorem + 3% melee share +
   `3 sentinels = 18 DPS ≈ 28 rounds through 500 HP` from `dirty-tricks-shortlist:28`).
   **A direct corpus count of builder-only core kills was NOT run.**
5. **QUEUE rows read in full: #10, #12, #13, #27, #42, #45, #52, #58, #60.** Rows **#47, #48,
   #51, #54, #62, #64** were seen only in the one-line index; #48 (parked-raider terminal
   idle) and #51 (aim the throw loop) are the two most likely to belong to this family and
   were not read.
6. **`IDLECULL`'s control was `_v171late160ammo`, not the plain incumbent** — the 33.5% is
   almost certainly a real negative given the margin, but the comparison was not re-based.
   **No DEFF correction was applied to any local number here** (per `CLAUDE.md`, local
   corefill reads pair-weighted DEFF 0.98, so naive bars are correct — but the platform-side
   numbers quoted in §9/§10 carry DEFF 1.529 rated / 1.833 unrated and this doc did NOT
   restate any of them.)
7. **`bots/_probe_camper`, `_probe_camper2`, `_probe_meleebot`, `_probe_sitter`,
   `_probe_victim`, `_probe_jail`, `_probe_prison`** were listed but not opened. `_probe_jail`
   /`_probe_prison` are the 12/12 spawn-lock and imprisonment probes and would settle §5's
   open item and §14.8 below.
8. **The imprisonment-by-barrier boolean was NOT tested and is the single cheapest untested
   exploit in this family.** `is_tile_empty` (`TY:341-343`) returns True if the tile *"has no
   building and is not a wall"* — **a builder bot does not make a tile non-empty.** If
   `can_build_barrier` inherits that literally, **a 3 Ti barrier can be built ON TOP OF a
   30 Ti enemy builder, and barriers are impassable — imprisoning it permanently: 10:1,
   refunds no scale (so it does NOT hand them the rebate a kill does), and it holds a
   `MAX_TEAM_UNITS` slot** (`exchange-rates:110-124`). It is **one boolean**. ⚠ And the
   corollary if it is true: parking our own bodies on our own ring is no defence.
9. **Enemy-entity-as-gunner-blocker** (§7) — untested, and QUEUE #10 cannot be built without it.
10. **No live or arena leg was fired for this atlas.** Everything above is corpus, source,
    prior probes and banked arena shards.
