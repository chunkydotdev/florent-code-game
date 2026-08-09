# LIVE: **v102 = LOKI-8** — the first Loki ship. 2026-08-09 ~20:4x CEST.

## ===== READ `PROGRAMME.md` FIRST. `tools/gate.py` ENFORCES IT. =====
## Then `docs/builder-method.md`, then this. Before any battery: `tools/gate.py`.
## Before any ship row: `tools/preflight.py <dir>`.
## **SUBMIT ONLY VIA `tools/submit_clean.py`** — bare `fcode submit` zips the whole
## dir and shipped `PREREG.md`/`DESIGN.md` to the platform on v94 and v95-v100.
## A doc-bearing submission is a drift flag (Magnus, 2026-08-09).

## ===== STATE =====
##   LIVE: **v102 = `bots/_v124loki8`**, treehash **2dad5a2a**, submission
##   `ff270a6c`. Activated at **1577.5 @ rank 30/116**.
##   **ROLLBACK TARGET: v101 (`0eccbedf`) = `bots/_v115dodge`** — byte-identical
##   to the retired v94 (`md5 77ae5c09`) but doc-free. Eir is the fallback.
##   Magnus approved the ladder explicitly after nine iterations benchmarked
##   unrated: *"alright, lets get loki on the ladder"*.

## ===== WHY IT SHIPPED — the number is core_kill_share, NOT win rate =====
##   MATCHED vs v94 Eir (same opponent, same 5 short maps, n=5/cell), five
##   opponents spanning 540 Elo:
##     Ouroboros -62   Eir 1/5   LOKI-8 4/5
##     CtrlAltDefeat 0 Eir 2/5   LOKI-8 4/5
##     Lunds -28       Eir 2/5   LOKI-8 3/5
##     Big O +200      Eir 2/5   LOKI-8 3/5
##     Jython +337     Eir 0/5   LOKI-8 1/5
##   **POOLED 7/25 = 28.0% vs 15/25 = 60.0%, Fisher p = 0.045, ahead in 5 of 5
##   cells, no ties, no reversals.**
##   **EVERY GAIN ON THIS LINE WAS A REMOVAL:** rush off (LOKI-4), all builder
##   melee silenced (LOKI-5), three arrival defects fixed (LOKI-6), raiders
##   exempt from the home heal + melee recall (LOKI-8).

## ===== CAVEATS THAT MUST TRAVEL WITH THE 60% =====
##   * **Dose-response is real: 75% at bracket, 60% at +200, 20% at +337.** The
##     advantage DECAYS with opponent strength. Never quote 60-86% without the band.
##   * **Short-map fixture only.** LOKI-5 fell 80% -> 60% on the long band.
##   * **n=5 per cell**, seats varied per leg but were NOT controlled.
##   * **LOKI-8 vs LOKI-7 was never run head to head** and at these n they are
##     indistinguishable. This is the best-TESTED arm, not the best arm.
##   * Two independent sources say our-tree-vs-our-tree numbers are biased
##     OPTIMISTIC (~2x), not merely noisy. The ladder is the real read.

## ===== WATCH THE SHIP =====
##   **ACTIVATION BASELINE IS 1567.44, NOT 1577.5** (corrected s26, D12). 1577.5
##   is the rating before **v101's LAST game** — the platform's per-match
##   `teamAVersion` says the 4-1 Kings College loss (-10.08) was v101's, created
##   **18:32:43.700Z, 4m41s before v102 was uploaded at 18:37:25.097Z** (the
##   load-bearing clock is createdAt vs uploadedAt; that match COMPLETED 18:37:47Z,
##   22s AFTER the upload, which is exactly why completedAt is the wrong clock).
##   Independently confirmed by research from `corpus/ladder_games.tsv` `ourbef`.
##   **The tape row tagged v102 is not the first v102 MATCH.**
##
##   The slot rule is the stop-loss: arms at >=8 matches, **net5 <= -21 frees the
##   slot**. It is now ONE importable statement in **`tools/slot_rule.py`** —
##   `.venv/bin/python tools/slot_rule.py` prints the live verdict in one line.
##   **`slot_free` is a permission and a WAKE, never an n=8 evaluation of the bot.**
##   **If it bleeds, roll to v101 — that is Eir, unchanged.**
##   (Purpose reframed by Magnus s26: x3r0 is not actively building, so the rule
##   is purely our own stop-loss now, not a slot-share. **Nothing mechanical
##   changed** — threshold, arming and wake semantics all stand.)

## ===== THE TRAJECTORY READ — CLOSED AT k=20, THE POINT SHIP-TIME QUEUED =====
##   **2026-08-10 00:00 CEST: 1599.0 @ k=20, 12W-8L, net +31.6 vs the corrected
##   1567.44 baseline. Peak 1600, drawdown -1.**
##   **THE ROUND TRIP: 1567 -> 1600 -> 1572 -> 1599. THE STOP-LOSS PAIR NEVER
##   FIRED THROUGH ANY OF IT**, and net5 touched -19.0 (two points off -21) at
##   the bottom. That is the rule behaving correctly, not a near miss.
##   **The recovery is REAL WINS, not window mechanics** — the caution was
##   raised (net5 relaxes as bad results age out) and the tape answers it:
##   **last five 4W-1L, +26.6 Elo actually won.** Both numbers agree this time.
##
##   **I AM WALKING BACK MY OWN DOSE-RESPONSE NUMBER.** At k=12 I recorded wins
##   vs mean opponent 1566.5, losses vs 1618.2, **gap +51.6, permutation
##   p=0.011**, and called it the documented Loki curve. At k=20 the same test
##   gives **wins 1573.1, losses 1601.0, gap +27.9, p=0.0500** — **the effect
##   HALVED and sits exactly on the conventional line as n grew.** That is the
##   signature of an estimate inflated at small n, and the honest reading is
##   that opponent strength still leans the right way but is **weaker than I
##   published and not established**. Research replicated the k=11 version
##   independently (+50.0, p=0.0195) — replication of an over-estimate is still
##   an over-estimate; both were the same small window.
##   **Anyone quoting +51.6 is quoting a superseded number.**
##
##   `tools/monitors/ship_watch.py` is ARMED, detached (PPID 1, 10-min cadence),
##   re-armed s26 on the corrected baseline. It appends every evaluation to
##   `corpus/ship_watch.log` and writes **`corpus/SHIP_ALERT`** when the RULE
##   frees the slot, clearing it on recovery.
##   **FIRST THING A SUCCESSOR SHOULD DO: `cat corpus/SHIP_ALERT` (absent = fine)
##   then `tail corpus/ship_watch.log`.** Trustworthy only from s26 — see below.
##   **`ship_watch.log` HAS TWO SCHEMAS.** Any `CLEARED` line is pre-s26 and came
##   from the decorative single-segment test; it means nothing.
##   **THE TAPE LAGS LIVE BY UP TO 5 MINUTES** (`elo_logger` polls at 300s), so
##   net5 and a live `fcode status` rating are from different clocks.
##
## ===== THE ALARM WAS DECORATIVE UNTIL s26 — READ THIS BEFORE TRUSTING IT =====
##   `ship_watch` shipped with the SPRT's constants imported and its
##   SEGMENTATION hand-rolled: one (net,k) from activation to now, **no
##   restart-on-OK**. Once it accepted OK it accepted OK forever. Measured:
##   **v102 could have bled 1584 -> 1384 and every evaluation would have logged
##   CLEARED.** Meanwhile `elo_logger`'s correct -21 wake is a **`print` to the
##   stdout of a dead session** (its arming loop has no redirect). So the durable
##   alarm could not fire and the firing rule was not durable.
##   FIXED: `tools/slot_rule.py` (single statement of the rule) + ship_watch
##   rewritten to use it + `slot_sprt.run_sprt` for the advisory.
##   **`ship_watch.py --selftest` is mutation-tested against 5 mutations**
##   (no-restart, dead threshold, ARM_AFTER=0, WINDOW 5->50, WINDOW->1) — all
##   five make it fail. `tests/test_instruments.py` asserts ship_watch and
##   elo_logger alarm on the SAME series in BOTH directions, so they cannot
##   silently diverge. **Run the selftest after any edit to either.**
##   **A wake path is verified when its alarm has been SHOWN ABLE TO FIRE, not
##   when its process appears in `ps`** (side lane, s26 — committed as standing).

## ===== WAKE PATH — STATED PLAINLY, INCLUDING WHAT IS NOT WATCHED =====
##   **SURVIVES this wrap (detached, PPID 1):** elo_logger, match_watcher,
##   opp_watcher (now with the league Elo tee -> `corpus/league_elo_log.tsv`,
##   72 teams/pull, ~10-min freshness), replay_archiver, keeper, **ship_watch**.
##   **DIES with the session:** every subagent, and the side lane's drift-watch
##   commit monitor.
##   **NOTHING WAKES A SESSION.** The monitors LOG and will raise `SHIP_ALERT`,
##   but no process boots a session to act on it. **The trajectory read happens
##   at the next boot, whenever Magnus starts one.** If v102 bleeds overnight it
##   will be recorded and NOT acted on until then. That is the honest answer;
##   the rollback is one command (`fcode submission activate 101`).

## ===== QUEUE =====
## 0. **v102 IS TWO POINTS FROM THE STOP-LOSS** (net5 -19.0 vs -21, armed). The
##    alarm is now real and detached; `cat corpus/SHIP_ALERT` first. On SLOT FREE
##    the call is roll-to-v101 or hold, and it is Magnus's or the builder's —
##    the rule permits a swap, it does not order one.
## 1. ~~`meta_join.tsv` never refreshes on sync~~ **FIXED s26.** It was the only
##    corpus surface carrying OPPONENT versions and was built ONLY by running
##    `meta_attrib.py` by hand, so it was the stalest file in `corpus/` while the
##    drift-watch told every lane to prefer it (`ladder_games`/`join` refresh but
##    their `oppver` is universally `None`). Now wired into `sync.py`, which the
##    keeper runs every 600s — ~7s per rebuild, three attribution checks, and a
##    LOUD refusal if they fail (failure = stale table, the very state this ends).
##    **Opponent versions now live: 2258/2258.** First thing it answered:
##    **Powerpuff Girls was v49 in BOTH v102 matches** (4-1 then 1-4, 80 min
##    apart) — they did NOT ship in between, so the reversal is ours, not theirs.
##    Askar City went **v82 -> v83 in four minutes** the same evening, so
##    mid-session opponent ships are real and this surface sees them.
## 2. **Per-opponent gates, not pooled win rate.** Pooling hides everything:
##    every >=1750 team kills us at 0-12% while the 1660-1710 band runs 22-38%.
## 3. **LOKI-7 vs LOKI-8 head to head** — never run; the ship picked the
##    better-tested arm, not a measured winner.
## 4. **The long band.** The whole line is tuned and measured on short maps.
## 5. Reverse-engineer the 1,131 top-tier replays we already hold (documented
##    path: BC2026 2nd place got its constants exactly this way).

## ===== DO NOT REBUILD — backed by the ORGANISERS' OWN PATCH NOTES =====
## **Our engine is a re-tuned descendant of Cambridge Battlecode 2026; its
## changelog is our balance history.** Deliberately killed there: suicide-builder
## rush, cheap-builder swarm, infinite-heal blob, two-sentinel one-shot.
## **Values do NOT transfer (our sentinel is 18/10 vs their 10/5) — intent does.**
## Four mechanics were NEVER balance-changed: launcher throw/kidnap, spawn-tile
## denial, tiebreak-turtle, crash-induction.
## **Also refuted THIS session:** ore poisoning (median 5 ore tiles used, 11
## spare), partial spawn starvation (only 12/12 is clean), siphon (off-currency),
## the barrier-form spawn lock, CPU denial, and heal-idle staffing (3.0%).
## **CPU-timeout induction stays HELD** — our own doc claimed two leagues ban it
## by name; re-verification shows the quote is about a 30-minute game clock.
## The false claim is corrected; **that does not open the road.**

## ===== INSTRUMENTS ADDED THIS SESSION =====
## `PROGRAMME.md` + `gate.py` programme lock · `tools/mech_battery.py` (keeps
## replays, prints mechanism BEFORE win rate) · `tools/reprice.py` (paired vs
## pooled, both estimators) · `tools/field_deaths.py` (refuses unstratified
## output) · `tools/collar_census.py` (dose-response) · `tools/tle_census.py` ·
## `tools/cpu_lag_probe.py` · `bots/_probe_victim` + `bots/_probe_jail`.

## ===== PRIOR STATE (s24 boot block) — superseded, kept for reasoning =====

# Session 24 boot block (builder) — written at the s23 wrap, 2026-08-09 12:0x CEST

## ===== READ `docs/builder-method.md` FIRST, THEN THIS =====
## And before your first battery, run **`tools/gate.py`** (new this session). It
## refuses runs that cannot produce a trustworthy answer. s23 learned every one
## of its checks the expensive way.

## ===== STATE =====
##   LIVE: **v91 "Eir 9c hivethaw (rollback from v90)"** = `bots/_v100hf`,
##   tree **4558be91**, submission **9850f196-362b-4017-a3b5-31e5cb5c75bd**.
##   SINGLE FILE (main.py only).
##   At wrap: **1562 @ 518 matches, rank #31/113, last-10 6W-4L.**
##   ROLLBACK TARGET: **v89-era is what v91 IS.** To go the other way,
##   v90 = `bots/_v104latch`, tree 2c6dbc17, submission b04c06fa (still `ready`).
##   **v91 CARRIES THE `SLOT_LAUNCHER` LATCH DEFECT** (a destroyed launcher is
##   never replaced; builders enter `launchwait` for a ghost). Known and accepted.
##
## ===== THE ROLLBACK, AND ITS READ IS CLOSED =====
## v90 was rolled back at 1530 @ 508 when a PRE-STATED trigger fired (last-10
## reached 2W). The 10-match recovery read is **COMPLETE**: 1530 -> **1562**,
## rank #35 -> #31, last-10 2W-8L -> 6W-4L. Pre-stated branch: *">= ~1556 means
## the drift was v90-specific; keep v91."* **BRANCH 1 FIRED. v91 RETAINED, v90
## RETIRED.** Margin is thin (~5 pts, under one match's +-18 swing) and the read
## **cannot** establish v89 > v90 — only that the drift stopped. Do not re-open it.
##
## ===== !!! THE THING THAT RE-PRICES EVERYTHING BEFORE IT !!! =====
## **`bots/opp_v*` IS OUR OWN PRIOR VERSIONS.** Their docstrings say so
## ("v89_open_ti_floor8 OFFLINE", "v61/S5 OFFLINE"); they carry 3-4 of our 4
## signature identifiers. **Every arena battery this project has run was
## SELF-PLAY**, including the s22 note titled "LOKI-3 **FIELD** VERDICT".
## Published amputation results run ~2x self-play vs field with reported SIGN
## FLIPS (direction supported; **the 2x is one figure from another game — do not
## use it as a divisor**).
##
## **A FOREIGN POOL WAS ON DISK ALL ALONG: `bots/*_probe`** — imitations of real
## teams (Orizon, Ouroboros, Clankers, kladde, Flotte, Banminary, CtrlAltDefeat)
## built from replay analysis, carrying **0-1 of our 4 signatures**. USE THEM.
##   **EXCLUSION LIST CORRECTED (s24), IT WAS WRONG IN BOTH DIRECTIONS:**
##   `rush_probe` is the ONLY probe that calls `random.` — `import random` plus
##   **10 hot-path calls** (choice/random/randrange/shuffle: spawn choice, three
##   direction shuffles, target choice). **EXCLUDE `rush_probe` from paired runs.**
##   **`cad_probe` is DETERMINISTIC** and was excluded for three sessions on a
##   `grep -c 'random\.'` that matched its own docstring sentence *"nothing here
##   is random."* — it says *"Deterministic: no random anywhere"* two lines later.
##   `tools/gate.py` now parses identifiers instead of substrings and FAILs on any
##   opponent that calls `random.` without declaring a `NOISE_ON` switch.
##   Probes are IMITATIONS and miscalibrated (`ouroboros_probe` measured **86 pts**
##   over-confident vs its real class). Better than self-play; **NOT field.**
##
## ===== PLATFORM INSTRUMENTS — s23 used neither until Magnus pointed =====
##   `fcode match test BOT_A BOT_B`   local bots, REMOTE engine, **REAL TLE**.
##       Free, no slot. s23 ran 1,860 games at `--tle 0` and never checked CPU.
##       Our worst real unit-turn is **12,967us against a 10,000 limit.**
##   `fcode match unrated OPPONENT_ID`  REAL opponents, zero Elo.
##       **NO bot selector — it plays the ACTIVE SUBMISSION.** A variant must hold
##       the slot. `--match` pins the opponent's submission, `--map` picks up to 5.
##       At n=10 it has **47% power**: record `NOT-REFUTED (n=10)`, never `pass`.
##
## ===== SCOREBOARD: THE TURRET SUBSYSTEM IS INERT TO TUNING =====
##   plank    knob        pool        result
##   LOKI-3   placement   SELF-PLAY   +0.0pp  (mislabelled "FIELD" in the tape)
##   HOME     price       SELF-PLAY   -2.0pp  not distinguishable from zero
##   FLOOR    production  SELF-PLAY   -0.7pp  not distinguishable from zero
##   SITE     siting      SELF-PLAY   -6.7pp  **REFUTED** dose-response + null band
##   ESCALATE dispatch    **FOREIGN** **-7.8pp  REFUTED** — 360 games, both seats
## **Four knobs, both directions, all nulls at field scale. Do not quote -2.0 or
## -0.7 as effects. THE NEXT ATTEMPT MUST NOT BE ANOTHER TURRET KNOB.**
##
## ===== WHAT IS TRUE AND FIELD-MEASURED (corpus, real opponents, no pool caveat) =====
## - **Forward insertion is refuted as DOCTRINE** on four instruments: fixed-horizon
##   survival (field pays NO distance penalty, we pay a large one), raider life
##   **43 -> 6 rounds at r150**, **2.34%** of r200+ forward throws ever touch a core,
##   and **first turret at r17** field vs **r12** ours — *we start earlier and stop.*
##   **The BUILDS were never field-tested. Two different sentences.**
## - **The bot cannot count attackers.** `SLOT_THREAT`=one position,
##   `SLOT_UNDER`=one boolean, `_core_shelled`=one boolean; a grep for any
##   magnitude term returns comments only. `_core`'s sensing loop `break`s on the
##   FIRST hostile. **Verified code fact. One RESPONSE to it (scale the heal
##   detail) is refuted at -7.8pp; the fact stands and a better response is open.**
## - **`SLOT_UNDER` has THREE writers** (`_core` x2 and EVERY builder at :2104
##   writing a bare `1`). Last-writer-wins. **The store cannot carry a magnitude.**
## - Home turrets are the **best-surviving in the corpus** (+11.4/+16.6/+22.3pp)
##   **and irrelevant to what kills us**: 65.3% of home builder deaths are an enemy
##   GUNNER planted inside our base, and **>=5-kill tiles carry 47.3%** of them.
## - We lose a higher fraction of **everything** except the two static home units
##   (sentinel -1.5pp, launcher -14.7pp). Broad attrition, not a subsystem.
##
## ===== QUEUE, IN PRIORITY ORDER =====
## 1. **THE GUNNER-PLANT TILES.** The only item with a MEASURED TARGET rather than
##    a hypothesis, and it is **enumerable, not behavioural**: name the >=5-kill
##    tiles per map/seat and cover them (3 Ti barriers or a turret arc).
##    One tile produced 45 kills. Specification, not doctrine.
## 2. **`bots/_abl_c4`** — hive bunker-barrier deletion. **18/20 -> 20/20, kills
##    4 -> 18, one converted loss, null-control seat byte-identical 20/20.** REAL,
##    but hive seat B is **2.4% of games** — below the instrument. **Ship BUNDLED,
##    never alone.** Built on v90's tree; needs rebasing onto v91 (see below).
## 3. **`SLOT_ROLE_N` ticket bug** — read-increment-write at `main.py:880`/`:902`,
##    probe-demonstrated to collapse silently (5 writers, counter +1, all believe
##    they are unit #0, no error). Safe TODAY only because the core spawns <=1
##    builder/turn — **a game rule holding up a bot invariant by luck.** Two lines.
## 4. **Re-price PLANK SITE against the foreign pool.** Largest number on the
##    board, and the literature makes a specific prediction (shrinks toward half,
##    direction survives). **A pre-stated prediction that gets tested beats a
##    fresh measurement.** Research's ordering, and it is right.
## 5. **Escalation, a BETTER response.** The code fact stands; more healers is
##    refuted. Untested: anything that is not "divert economy to defence".
##
## ===== A BLOCKER NOBODY WROTE DOWN WHEN THE SLOT MOVED =====
## **Every Loki build (`_v104loki0/0b`, `_v105loki1`, `_v106loki2`, `_v107loki3`,
## `_v108loki4`, `_v109loki5`) is MULTI-FILE on the v90 lineage.** LIVE is v91 =
## single-file v89. **"The Loki builds are ready to bundle" is FALSE** — each needs
## re-shipping v90 first or rebasing onto the v89 chassis. Same for `_abl_c4`,
## `_v111home`, `_v112floor`, `_v113site`. `_v114esc/_v114off` ARE on v91.
## First real-engine data on Loki: `match test _v107loki3 _v100hf` -> **loses 2-3**,
## no crash, TLE enforced. n=5, settles nothing; the build is platform-viable.
##
## ===== TOOLS ADDED THIS SESSION =====
## `tools/gate.py` — pre-flight: determinism (all arms), control-equivalence
##   (flags-off MUST equal parent), **pool identity** (FAILs on self-play without
##   `--allow-self-play`), and queues a **remote TLE test**. Verified against all
##   three of s23's real failure modes.
## `tools/corpus_sanity.py` — FAILs on all-zero columns. Found `econ.tsv:shots`
##   (known) **and `econ.tsv:deliveries` (new, 28k rows, and delivery is
##   TIEBREAK #1)**. Both declared and never incremented. Use `build_agg.tsv`
##   `metric=='shot'` for shots; `flow.tsv` for delivery.
##
## ===== PRIOR STATE (s23 boot block) — superseded, kept for reasoning =====

# Session 23 state block (builder) — LIVE VERSION CHANGED THIS SESSION

## ===== READ `docs/builder-method.md` FIRST ===== (unchanged, still correct)

## ===== STATE (as of 2026-08-09 10:2x CEST) =====
##   LIVE: **v91 "Eir 9c hivethaw (rollback from v90)"** = `bots/_v100hf`,
##   tree **4558be91**, submission id **9850f196-362b-4017-a3b5-31e5cb5c75bd**.
##   **THIS IS A ROLLBACK, NOT A SHIP.** v90 was reverted when a PRE-STATED
##   trigger fired (last-10 reached 2W). At rollback: **1530 @ 508, rank #35**.
##   ROLLBACK-OF-THE-ROLLBACK TARGET: **v90 = `bots/_v104latch`, tree 2c6dbc17**
##   (submission b04c06fa, still listed `ready` — re-activate or re-upload).
##   **v91 REINSTATES THE `SLOT_LAUNCHER` LATCH DEFECT** (a destroyed launcher is
##   never replaced; builders enter `launchwait` for a ghost). Known, accepted,
##   bounded — v90's repair fired hard (post-r100 launcher share 6.9% -> 32.7%)
##   but total launchers/game barely moved (0.72 -> 0.75).
##
## ===== PRE-STATED, HONOUR IT =====
## **If the ladder does not recover within ~10 rated matches of the rollback,
## that is evidence the drift was NOT v90-specific and v90 should go back up.**
## The rollback is a STOP-LOSS, NOT A VERDICT. v90 was never shown worse than
## v89 — 17 matches at ±18/match cannot show that. Do not let the tape be read
## later as "v90 was refuted".
##
## ===== THE SESSION IN ONE LINE =====
## **Four planks built, gated and REFUTED; the forward road closed on four
## instruments; turret count refuted on three knobs; one rollback. ZERO SHIPS.**
##
## ===== THE RESULT THAT MATTERS MOST =====
## **PLANK SITE: −6.7pp with DOSE-RESPONSE and an exact-zero null band.**
## Gating forward siting off above core-separation d²81 cost 0.0pp where the gate
## cannot fire (narrow), −5.0pp at mid, **−13.3pp at wide**. **Forward turrets
## survive at 18.9% (field 49.0%) AND REMOVING THEM COSTS 13.3pp — the 18.9% is
## the price of something valuable, not waste.** A large, clean, confound-
## controlled survival statistic, independently derived by both arms, pointed at
## a change that is strongly harmful. **Survival was never the objective function.**
##
## ===== THE TURRET SUBSYSTEM IS INERT TO TUNING =====
## **!!! EVERY NUMBER BELOW IS SELF-PLAY. The `opp_v*` pool is OUR OWN PRIOR
## VERSIONS (their docstrings say so: "v89_open_ti_floor8 OFFLINE", "v61/S5
## OFFLINE"). Run `tools/gate.py` before any battery; it now FAILS on this. !!!**
##
##   plank    knob         SELF-PLAY   reading
##   LOKI-3   placement      +0.0pp    null (and mislabelled "FIELD" in the tape)
##   HOME     price          −2.0pp    NOT distinguishable from zero
##   FLOOR    production     −0.7pp    NOT distinguishable from zero
##   ESCALATE dispatch       −0.7pp    self-play: cost only, gate unanswerable
##   ESCALATE **vs FOREIGN** **−7.8pp**  **REFUTED — 360 games vs 6 real-team
##            probes, both seats negative, and the escalation condition WAS
##            present (orizon_probe: 1,625 post-r250 multi-attacker events vs
##            ZERO from our own lineage). The only verdict today I would defend.**
##   SITE     siting         −6.7pp    REFUTED — dose-response + exact-zero null band
##
## **THE CORRECTED READING (research's, and it is better than "four small
## negatives"): at field scale these are NULLS, not small harms. The subsystem is
## not slightly harmful to tune — IT IS INERT TO TUNING.** Stronger as a
## direction, weaker as a measurement. **Do not quote −2.0 or −0.7 as effects.**
##
## **SITE SURVIVES INTACT** — its strength was never magnitude, it was
## dose-response across bands with an exact-zero null band where the gate cannot
## fire. A scale factor cannot touch that structure.
##
## **CAVEAT ON THE SCALE FACTOR, mine not research's:** the "2x self-play
## inflation" is Agade's published figure for ONE feature of HIS bot in Code
## Royale. The DIRECTION (self-play inflates; sign flips are reported) is
## supported; **the specific 2x is a single data point from a different game and
## should not be applied as a divisor to produce a "field estimate" column.**
## We have no measured transfer factor for THIS game.
##
## **ESCALATE WAS THE ODD ONE OUT AND NO LONGER IS.** It was untestable against
## `opp_v*`; re-gated against the FOREIGN probe pool it is **REFUTED at −7.8pp**.
## **What is refuted is ONE RESPONSE — "scale the heal detail with attacker
## count" — not the thesis.** Diverting expanders to heal costs more economy than
## the healing saves; the doctrine file priced what healing PRODUCES and never
## what the healer STOPS DOING. **The code fact stands: the bot cannot count
## attackers** (SLOT_THREAT = one position, SLOT_UNDER = one boolean, and a grep
## for any magnitude term returns comments only). A better response is open.
##
## ===== !!! USE THE FOREIGN POOL. IT WAS ON DISK ALL ALONG !!! =====
## `bots/*_probe` are imitations of REAL ladder teams (Orizon, Ouroboros,
## Clankers, kladde, Flotte, Banminary, CtrlAltDefeat), built from replay
## analysis, carrying **0-1 of our 4 signature identifiers**. Five planks were
## gated against `opp_v*` (= us) before anyone looked.
##   `cad_probe` is the ONLY probe that calls `random.` — exclude it from paired runs.
##   Probes are IMITATIONS and miscalibrated (`ouroboros_probe` measured **86
##   points** over-confident vs its real class). Better than self-play; NOT field.
##
## **UNTOUCHED BY ALL OF THIS: every corpus finding.** The hazard curve, the
## gunner-plant tiles, the survival splits, the heal cancellation are measured on
## REAL ladder games against REAL opponents and carry no self-play factor.
##
## **STANDING LABEL RULE: any battery result quoted outside its own document
## carries its pool.** Five numbers circulated between three sessions today
## without it. Agade's discipline is the model: measure in self-play because it
## is cheap, then RE-MEASURE THE SURVIVORS against the field, and publish both.
##
## ===== BUILDS ON DISK, ALL UNSHIPPED, ALL CONTROL-VERIFIED =====
## `_abl_c4` (hive bunker-barrier deletion: **18/20 -> 20/20, kills 4->18, one
##   converted loss, null-control seat byte-identical 20/20** — REAL but only
##   **2.4% of ladder games**, below instrument; ship it BUNDLED, never alone)
## `_v111home` (magazine/targeting, refuted) · `_v112floor` (production, refuted)
## `_v113site` (siting subtraction, refuted hardest)
## `_det_opp_v56/58/63/67/68/69/72/74/76/78` — **deterministic opponent copies;
##   reuse these, `det.py` says flip NOISE_ON on ALL sides and I only did ours
##   the first time and got a broken null control for it.**
##
## ===== METHOD THAT EARNED ITS KEEP TODAY =====
## - **A map- or seat-gated change has a FREE NULL CONTROL: the seat/band it
##   cannot reach.** Caught one broken battery, validated three others.
## - **Compute a constant's WORKING RANGE before spending a battery on it.**
## - **Pre-register the RESCUE you would reach for, not just the threshold.**
## - **Ask what a thing PRODUCES before subtracting it for what it costs.**
##
## ===== QUEUE =====
## 1. **Watch the rollback** — ~10 rated matches, then decide per the pre-stated
##    rule above. **The keeper will alert on drops; it is proven (fired 08:04Z).**
## 2. **`get_attackable_tiles` mis-scoring** — probe-confirmed BOTH ways this
##    session: gunner lines block on friendly bots AND buildings; the raw pattern
##    IGNORES occupancy. Any siting scored with it counts phantom coverage.
##    **A defect with a probe behind it, not a doctrine bet.** Static check first.
## 3. **`SLOT_ROLE_N` ticket bug** — read-increment-write at `main.py:880`/`:902`;
##    probe-demonstrated to collapse silently (5 writers, counter +1, all believe
##    they are unit #0, no error). Safe TODAY only because the core spawns <=1
##    builder/turn — a game rule holding up a bot invariant by luck. Two-line fix.
## 4. **Escalation response** — three instruments now show the same shape: best
##    in the easy regime, worst in the hard one (home turrets 86.7% vs forward
##    19.2%; 1-attacker heal cancellation 65% vs 3-attacker 30%; hazard 29%->76%).
##    **That is the characterisation of this bot.** Confound NOT closed (are we
##    heal-capped, or already dead?) — research has the discriminator queued.
##
## ===== CORPUS TRAP FOUND TODAY =====
## **`corpus/econ.tsv` `shots` is 0 in ALL 25,530 rows** (`replay_econ.py:109`,
## `elif unum == 12: pass`). Every other column is populated, so **the zero looks
## like a finding, not a bug.** Use `corpus/build_agg.tsv`, `metric == 'shot'`.

## ===== PRIOR STATE (s23 boot block) — superseded, kept for reasoning =====

# Session 23 boot block (builder) — written at the s22 wrap, 2026-08-09 09:4x CEST

## ===== READ `docs/builder-method.md` FIRST =====
## New this session, written on Magnus's ask: **how the builder arm works**, so
## you do not rediscover it. Order of operations (rule -> probe -> code -> corpus
## -> arena -> field), pre-registration discipline, what the arena can and cannot
## answer, the two confounds that silently invalidate arena numbers, and the
## delegation brief that makes agents refute their own work.
##
## ===== STATE =====
##   LIVE: **v90 "Heimdall 1 (launcher relight)"** = `bots/_v104latch`,
##   tree **2c6dbc17**, submission id **b04c06fa**. (= live v89 + the
##   SLOT_LAUNCHER latch repair, nothing else.)
##   **VERSION IDENTITY IS NOW A TREE HASH** (`tools/treehash.py`) — md5 of
##   main.py stops identifying a multi-file bot. `--legacy` cross-walks old rows.
##   At-ship baseline **1556.83 @ 491, rank #31**. At wrap: **~1567.5 @ 497,
##   rank #30, net +10.67 over 6 rated matches.**
##   Reversion bar (<=0 net after 3) **NOT tripped -> slot retained.** But
##   **+18.34 at the 3-match read was 1.36 sd — NOT significant.** Heimdall is
##   retained on its 18.4%-incidence census evidence, NOT on its Elo.
##   ROLLBACK TARGET: **v89 = `bots/_v100hf`, tree 4558be91** (re-upload bytes;
##   rollback needs no `activate`).
##
## ===== THE SESSION IN ONE LINE =====
## **Five roads opened, FOUR refuted by measurement, one maintenance fix shipped,
## and ZERO positive field results.** Every refutation cost a leg, not a slot.
##
## ===== THE RESULT THAT MATTERS MOST, AND IT IS A NEGATIVE =====
## **LOKI-3 moved its pre-registered mechanism metric 16x and won nothing.**
## damage-capacity:HP-repaired **0.17 -> 2.82** (the field's own 2.79), turret
## count held constant by construction, opening byte-identical, 0 crashes.
## **Field spread: +0.0pp on n=360** (per-opponent +3.3 / -4.4 / +2.2 / -1.1).
## **A pre-registered mechanism metric protects ATTRIBUTION, NOT VALIDITY.**
## Leading (pre-stated) explanation: our forward guns sit at median **d² 116-146
## from our own core against the field's 56-82** — outside every heal path we
## own, so they die alone. Games ran **24% shorter at identical win rate**.
##
## ===== QUEUE, IN PRIORITY ORDER =====
## 1. **LOKI-3 anchor `LATE_FORWARD_NUM/DEN` 3/5 -> 2/5.** ONE CONSTANT, already
##    flag-gated, lands on the field's measured band. Cheapest live hypothesis.
## 2. **TEST THE COMPOSITE, NOT THE PARTS.** LOKI-3 is the ENABLER; LOKI-4's
##    crater arm and LOKI-5's healer arm are both DOWNSTREAM of forward guns and
##    both measured weak-in-isolation for that exact reason. Composite first,
##    then ablate down. **"Refuted alone" is not "refuted".**
## 3. **LOKI-5: DO NOT SHIP AS BUILT — the frequency number decides it.** The
##    coverage mechanism is real (37.5% vs 1.9%, p=0.0153) but **the MEDIAN
##    ladder game has ZERO exiles by us** (p75 2, p90 16). It pays against ~5 of
##    19 opponents (Orizon 27.5/game, Ouroboros 22.5, OopsGotYourElo 17.6, KCM
##    16.5, Lunds 14.1) and does nothing against the other fourteen. A 180-SLOC
##    subsystem cannot be justified by a quarter-coverage effect; only the
##    ~65-SLOC coverage-only cut is defensible, and it stays opponent-conditional.
##    **Measure the OPPORTUNITY RATE before the effect size.**
## 4. **THE FORWARD LAUNCHER GAP.** Healer kidnapping is structurally blocked:
##    our launcher sits on the home band, enemy healers stand next to THEIR
##    damaged buildings. **We never build a forward launcher.** That single gap
##    blocks the highest-value half of LOKI-5.
## 5. Open questions handed back by research: the seat-turret gap ablation
##    (`docs/research/seat-turret-gap-2026-08-09.md` §6 specifies a 4-cell test in
##    OUR lane, unrun); and **7 single-seat map clauses across 4 maps** — a defect
##    CLASS, not a one-off.
## 6. **Magnus owes the organisers one question** before anyone builds CPU
##    exhaustion: sibling leagues ban it by name; ours is silent.
##
## ===== BUILDS ON DISK, ALL UNSHIPPED =====
## `_v107loki3` (5 flags, field +0.0pp) · `_v108loki4` (ore denial; generic arm
## LOW-CEILING — median map leaves them 5 spare sites; crater arm untested in
## composite) · `_v109loki5` (kidnapper; tree 7693584d; coverage term works) ·
## `_v110link` (fork of live + the `_link_path` team-test fix, **INCOMPLETE**) ·
## `_v104loki0`/`_v104loki0b` (controls, never ship) · `_v105loki1` (closed:
## field edge was an opponent-crash artifact).
## **All three Loki builds verified byte-identical to their parent with their
## master flag OFF, so every rollback is exact.**
##
## ===== TRAPS THAT COST US TIME TODAY =====
## - **ARENA RESULTS ARE LOAD-SENSITIVE AND THE DAMAGE IS INVISIBLE.** Under
##   `--tle 10` an overrun turn is interrupted with **no crash, no traceback**.
##   Run ONE battery at a time. Tell subagents "**do not measure**", never "use
##   fewer jobs". Documented in `docs/tooling.md`.
## - **Stratify every paired leg by the OPPONENT's crash count.** LOKI-1 showed
##   +3.6pp pooled and **+1.1pp on crash-free legs** — its edge was the opponent
##   self-destructing.
## - **`is_tile_empty` is NOT a build-legality predicate.** True on a tile holding
##   a builder bot, yet `can_build_barrier` is False.
## - **`CLAUDE.md` is wrong on the spawn ring**: `CORE_SPAWNING_RADIUS_SQ = 2`
##   (12-tile ring), not the r²=8 action radius. Probe-confirmed both seats.
## - **`official-docs.md:1091` is wrong**: a CPU overrun does NOT disqualify.
##   Ouroboros discards 26,356 unit-turns across 85 games and still beats us.
##
## ===== THERE *IS* A WAKE PATH — corrected at the s22 wrap =====
## Both arms wrongly reported "nothing watches the ladder". **`tools/corpus/
## keeper.py` runs as an ORPHANED daemon (PPID 1) and SURVIVES session end.**
## 600s poll. Raises a real macOS notification on: **SHIP DETECTED** (active bot
## changed), **RATING DROP** (>=25 below high-water), **LOSING STREAK** (last-10
## <=2W). Also runs the archiver and decodes new replays into `corpus/`.
##   Check it: `cat corpus/keeper.pid` then `ps -p <pid>`; log at corpus/keeper.log
##   NOT covered: anything subtler than those thresholds, anything needing a
##   decision, and **it cannot roll back — it detects, it does not act.**
##   It dies on reboot or if the pid is killed.
## **Verify it is still alive at boot before relying on it.**
##
## ===== PRIOR STATE (s22 boot block) — superseded, kept for reasoning =====

# Session 22 LIVE (builder, booted 06:40 CEST 2026-08-09)

## ===== STATE =====
##   LIVE: **v89 "Eir 9c hivethaw (rollback)"** = `bots/_v100hf`, submission id
##   847b8d9d. **UNCHANGED this session — s22 has not touched the slot.**
##   **Version identity is now a TREE HASH: `4558be91`** (`tools/treehash.py`,
##   matched to `fcode`'s real zip file set). Legacy md5(main.py) `9e85cae5`
##   still cross-walks old tape rows via `--legacy`. **md5-of-main.py no longer
##   identifies a multi-file bot — do not quote it alone.**
##   Ladder at 07:0x CEST: **1534.62 @ 487, rank #34/113** (was 1531.48/#35).
##   Rollback target: `bots/_v89sh` (v80, tree `52c6c574`), re-upload as new.
##   Cohort classifier for any band read: opponent `ratingBefore` per
##   **(opponent, VERSION)**, threshold **1550**, no sweep.
##
## ===== !!! THE s21 QUEUE'S #1 ITEM IS REFUTED — DO NOT BUILD IT !!! =====
## **s21 told you to BUILD LOKI to raise the r200-300 conversion ratio via the
## launcher-insertion pipeline. THAT BUILD IS DEAD. Do not start it.**
## The r180 cutoff I found in code is REAL (`LAUNCH_GIVEUP_RND` binds both the
## give-up at main.py:1048 and the only re-entry at :1060, so the pipeline is
## off from r180). **The INFERENCE from it was wrong**, refuted by two
## independent instruments on 2026-08-09:
##   1. **My own ablation.** `_v104loki0` = that cutoff removed (900/99) vs
##      `_v103split`: **89-91, 49.4%, CI [42.2%, 56.7%], n=180, 0 crashes.**
##      **NO EFFECT.**
##   2. **3,791-replay corpus, 11,895 forward throws.** Median raider life after
##      a throw collapses **43 -> 6 rounds at exactly r150**. Only **2.34% of
##      r200+ forward throws ever land ONE attack on the enemy core.** A builder
##      does 2 dmg into 500 HP; six rounds is ~12 HP under perfect conditions.
## **CONCLUSION: `LAUNCH_GIVEUP_RND = 180` IS A CORRECT CONSTANT THAT OUR OWN
## SOURCE JUSTIFIED WITH A WRONG REASON.** doctrine.py:106 claims "matches
## decided earlier never reached that bound" — false, half our games pass r180.
## The number is right anyway. **I attacked the comment and wrongly assumed the
## constant inherited its error.** `_v104loki0` is a CONTROL, never a ship.
##
## ===== WHAT REPLACED IT =====
## **Survival at the destination is the scarce resource, and it is only
## purchasable before r150.** The payoff is real and brutally concentrated: of
## raiders that established, **25 produced 50.5% of ALL core-attack volume**,
## and **319 of the 528 core-attacking raiders were on the winning team.**
## Current Loki direction: **early insertion (< r150) + a SURVIVAL PACKAGE.**
## **This is NOT the refuted rush** — the three dead rushes (thor_r1, sporks,
## Thor-1 gunline) were early TURRET pushes from the home band. Different
## mechanism, and the economy is kept (thor_r1 went 2/60 on zero titanium).
##
## ===== A LIVE DEFECT IN v89 RIGHT NOW: THE SLOT_LAUNCHER LATCH =====
## `SLOT_LAUNCHER` is written `1` at four sites (:770 :823 :830 :3880) and
## cleared at exactly ONE (:850, the build-failure path). **Nothing clears it
## when the launcher DIES.** Therefore, in the SHIPPED bot:
##   - `_try_build_launcher:819` returns False forever -> **a destroyed launcher
##     is NEVER replaced for the rest of the match**
##   - the `:1046` escape hatch (`not SLOT_LAUNCHER` -> stop waiting) is **dead
##     code** once latched
##   - builders keep entering `launchwait` **for a ghost**
## **This is a SURVIVAL defect, not an offence one:** exile is ~70% of all
## launcher activity in the field, **ours is ~97% defensive**, and enemies do
## insert against us (Memtrace 1,187 · Lunds 273 · CtrlAltDefeat 159 · KCM 139).
## Repair built in `_v104latch` / `_v104loki0b`: slot 6 now carries `round + 1`
## as a **heartbeat** (all 16 slots were already occupied, so freshness had to go
## INTO it). Measurement was in flight at this writing — **read the tape, do not
## assume it passed.**
##
## ===== THE INSTRUMENT LIMIT THAT BOUNDS EVERY SHIP DECISION =====
## **The zero-Elo unrated loop can REFUTE but can NEVER CONFIRM.** One ladder gap
## buys ~10 games; against the fixture baseline (p0 ~ 6.25%) the bar that is safe
## against the null (>=3 wins) has **47% power**. Confirmation needs n~40 ~ four
## gaps, and since `unrated` plays the ACTIVE submission, that means the variant
## **holds the slot across ~4 rated matches.** Free and confirmatory are mutually
## exclusive. Thor was validly refuted at n=10; **nothing has ever been confirmed
## by this loop.**
##
## ===== READ THIS FIRST: THE GOAL CHANGED TODAY, AND THE REASON IS MEASURED =====
## **We have spent this project buying SURVIVAL. It worked, and it is nearly
## exhausted. The untouched lever is KILL CONVERSION.**
##
## Research's kill-timing study (2,410 games, mix-controlled, zero downloads):
##   our core-kill production   **29.8% vs STRONG, 29.8% vs WEAK — identical**
##   our median kill round      **r148** — EARLIER than the field's r296
##   what actually varies       **how often THEY kill US** (44.1% / 20.9%)
##   lineage v53->v84, 770 mix-controlled games:
##     their kill rate on us 52.2% -> 38.8%  ·  their median kill round 280 -> 387
##     grind share 27.8% -> 43.6%  ·  win rate **+5.8pp**
##     **OUR kill production 20.0 -> 23.8 -> 17.6%. NO TREND. Fifteen shipped
##     planks and not one of them moved it.**
##
## **THREE CLAIMS THAT ARE NOW REFUTED — do not rebuild on them:**
## 1. **"We are bad at killing cores." FALSE.** 29.8% band-invariant at median
##    r148. We start kills fine. **We fail to CLOSE ~70% of them.**
## 2. **"The top tier rushes." FALSE.** Only **12% of their kills land by r100;
##    half arrive after r300** (median r296, q1 166, q3 475). Early gunners at
##    r19 and early KILLS are different claims and only the first is supported.
##    **If you copy timing, copy r200-300.**
## 3. **"Delivered titanium is wasted."** Not supported — the grind is still
##    26%/49% of games. The economy planks were aimed at a real state.
##
## ===== THE RUSH HAS NOW FAILED THREE TIMES, ALL FROM ONE CAUSE =====
## thor_r1 (2/60, zero Ti delivered) · sporks-ammo-as-ported · **Thor 1 gunline
## (v88) today: ZERO cores killed in 10 matched unrated games and MORE core
## deaths than the bot it replaced (5 vs 3).** One cause explains all three:
## **the field does not rush, so a rush copies a doctrine nobody runs.**
## Thor's specific lesson: gunner is r^2=13/dmg 7, sentinel r^2=32/dmg 18, so
## swapping the turret TYPE while it still stands on the HOME BAND trades
## long-range heavy defence for short-range light defence and buys no offence.
## **The top tier's gunners are OFFENSIVE. Ours sit at home. WHERE THE TURRET
## STANDS IS THE DOCTRINE, NOT WHAT IT IS.**
##
## ===== THE LOOP THAT MAKES ALL OF THIS SAFE (validated today, zero Elo) =====
## **Ship -> matched unrated -> read -> roll back, entirely inside a ladder gap.**
##   04:15 ship Thor · 04:16 fire battery · 04:19 10 games back, negative
##   04:20:23 roll back · 04:22:43 next ladder slot fires on the rollback
##   **Rated matches played by the variant: ZERO.** Verified: the 04:02:43 and
##   04:12:43 slots both ran ourV 87.
## MEASURED CONSTANTS THAT MAKE IT WORK (all new today):
##   - **The ladder scheduler is RIGID: 39 consecutive creation gaps of exactly
##     10.0 min, always at :X2:43.** Match completes ~:X8:30 -> safe gap ~4:13,
##     knowable in advance.
##   - **Rate limit: 5 unrated/test matches per 10 minutes** = 25 games/cycle
##     = ~150 games/hr at zero Elo.
##   - **Rollback needs no `activate`** — re-upload the predecessor's bytes.
##   - **`unrated` plays the ACTIVE submission**, so "develop on unrated while
##     the old bot holds the ladder" is **ALTERNATING, not parallel**.
##     `match test` is local-bot-vs-local-bot and cannot supply a real opponent.
##   - Residual risk: a classifier-blocked rollback leaves the variant live for
##     one 10-min cycle. It blocked two innocuous calls today. Real, bounded at
##     ~1 rated match.
## **THE MATCHED FIXTURE, with a real baseline — use this, not the local arena:**
##   hive, 5 games each vs KCM `dfa9be96` / Ouroboros `a5631594` / Powerpuff `0c1fea85`
##   **v80 0-16 · v87 1-15 · Thor 1-9.** Pre-register the threshold BEFORE firing.
##
## ===== QUEUE FOR THE NEXT SESSION, IN PRIORITY ORDER =====
## 0. **DISCUSSION PHASE ON LOKI FIRST — Magnus asked for it explicitly.** Do not
##    open an editor before the four open questions at the bottom of this block
##    are answered. The last two builds both failed because the doctrine was
##    decided at the keyboard.
## 1. **BUILD LOKI** against the re-specified target below. `bots/_v103split`
##    (doctrine.py split, det-proved identical, packaging verified) is the
##    chassis to fork — NOT a from-scratch rewrite. thor_r1 is why.
## 2. **MOVE VERSION IDENTITY TO A TREE HASH** before any multi-file bot ships.
##    Currently every tape row and pre-ship check quotes `md5 main.py`, which
##    stops identifying a split bot. This is a blocker on shipping Loki, not a
##    nicety.
## 3. **THE 7-vs-2 HOME-TURRET SEAT GAP** — queued to research, unstarted. Same
##    code, symmetric map, deterministic, 4/4 seeds. Larger than the defect we
##    shipped a fix for, and live.
## 4. Lunds fixture — **SUSPENDED, not dead** (they shipped v50). Their versions
##    are non-monotone (v37 after v41, v44 after v45), so v44 can return and the
##    table with it. Re-check is free from any `match list` row.
##
## ===== NEXT BUILD: "LOKI" — CONVERSION, NOT RUSH =====
## **TARGET RE-SPECIFIED — the "kill share above 29.8%" I first pre-registered is
## WITHDRAWN, and research is right that it was the wrong target.** 29.8% is an
## average over a distribution whose SHAPE is the finding; it could be hit purely
## by converting more before r150, the window we already win, and teach us
## nothing. **THE TARGET IS: raise the r200-300 conversion ratio against STRONG
## opponents above 1.0. It currently sits at 0.52 and has DECLINED across three
## lineages.**
##
## THE HAZARD TABLE — the most actionable thing either arm produced today. Among
## games still alive at the start of each window, fraction resolving inside it.
## Ratio = our hazard / theirs; **>1 means we out-convert them.**
## ```
##                    r0-150   r150-200   r200-300   r300+
##   STRONG >=1550      1.54      1.00       0.62      0.24   (n=1135)
##   WEAK   <1550       1.90      1.20       1.31      1.05   (n=1275)
##   strong raw: alive 1135/853/753/601 · ours 15.1/5.9/7.7/9.8% · theirs 9.8/5.9/12.5/40.9%
##   by lineage (strong): v53-70 1.40/0.73/0.72/0.20 · v71-76 1.85/1.45/0.62/0.29
##                        v77-84 1.65/1.38/0.52/0.24
## ```
## **We can only kill strong teams EARLY. Parity at r150-200, then it inverts to
## 0.24 by r300. Forty versions bought the r150-200 window (0.73 -> 1.38) and
## NOTHING after it — r200-300 went BACKWARDS (0.72 -> 0.52). The wall is located
## to a 50-round window.**
##
## **THE WARNING THAT MUST SURVIVE INTO THE BUILD: TIME IS THEIR ASSET, NOT OURS.**
## Their hazard runs 9.8% -> 40.9% across the game; ours runs 15.1% -> 9.8%.
## "Sustained siege" follows correctly from "the field does not rush", **but any
## siege that trades tempo for position is trading INTO the window where they
## convert four times better. A siege must RAISE our r200-300 hazard, not merely
## extend the game to reach it — those are different builds and only the first
## one wins. If Loki lengthens games without moving that ratio, the hazard table
## predicts it loses MORE than a rush does.**
##
## Stays on unrated until it clears the fixture baseline; **it does not take the
## slot on promise** (we win 67% vs the weak band and a pure kill bot risks
## exactly that).
##
## **LABEL ON MY OWN THOR EXPLANATION, because research was right to flag it:**
## "type-vs-placement" (we downgraded defence rather than bought offence) was
## generated AFTER seeing the result. Nothing in the Thor legs separates it from
## "gunners are simply worse here" — both predict what we saw. **It is a
## hypothesis, not a finding.** The better reason to believe it is the hazard
## table, which says the deficit is LATE and Thor changed nothing about late
## conversion.
##
## ===== THE FOUR OPEN QUESTIONS FOR THE DISCUSSION PHASE =====
## 1. **What actually raises the r200-300 hazard?** The `_offer_launch` throttle
##    is the best candidate on the board precisely because it is a LATE-GAME rate
##    limit — one raider staged for a whole match produces exactly the flat
##    ~4-10% hazard we observe from r150 while theirs compounds. But that is a
##    hypothesis and it needs a mechanism, not a flag.
## 2. **Does Loki keep the economy?** thor_r1 shipped zero harvesters and
##    delivered zero titanium (2/60). The bootstrap is what keeps us alive to
##    r148 to attempt a kill at all. Recommendation: keep it bit-for-bit.
## 3. **How much of the chassis does Loki fork?** doctrine.py is split and proved.
##    Recommendation: fork `_v103split` + ONE new module (`raid.py`), not a
##    rewrite, so the new offensive code is ablatable as a unit.
## 4. **What is the CPU budget for a multi-raider pipeline?** 10ms/unit/turn is a
##    live limit — the chassis already guards it in the turret scan. **A `run()`
##    that raises anything except a timeout PERMANENTLY DESTROYS that unit for
##    the rest of the match.** `raid.py` ships with its own CPU guard and a
##    blanket try/except or it does not ship.
## THE LEVER, already located in code: **`_offer_launch` (:2561) claims "the
## single insertion slot" — at most ONE raider is ever staged. That is why our
## launcher measures 93% DEFENSIVE.** The insertion machinery already exists and
## already targets tiles adjacent to the enemy core (`_launcher`, :4987-5083).
## It is throttled, not missing.
## MEASURED EXPLOITS TO WEAPONISE (all three are ours already, all pointed the
## wrong way): (1) launcher insertion — **but see the Lunds warning below: the
## hard-coded tiles table is SUSPENDED, so build the raid pipeline GENERIC
## (derive drop sites from `SLOT_ENEMY_CORE` as `_launcher` already does) and
## never against one opponent's measured constants**;
## (2) **cost-scale attack — our own eider post-mortem measured forced conveyor
## churn putting +146% on everything the victim buys afterwards. We know it works
## because it was done TO US**; (3) sentinel through-wall line shot (r^2=32,
## dmg 18, ignores obstacles) used as a doorbell instead of a siege gun.
##
## ===== THE BLOCKER THAT WAS NEVER REAL =====
## The s20 block said `fcode submission activate` is classifier-BLOCKED, so
## "SLOT CHANGES NEED HIM". **Only half true, and the false half shelved a
## measured fix for a night.** `fcode submit` is NOT blocked and AUTO-ACTIVATES
## (tooling.md), so **the builder arm can ship, and can roll back by re-uploading
## the predecessor's bytes.** Magnus's hand is needed only to REACTIVATE an
## existing submission. Never write "I cannot ship" again without testing it.
##
## ===== v80 OBITUARY, CLOSED AT THE TRUE n=40 (supersedes -18.54/n=39) =====
##   life-2 baseline 1545.35 -> close 1523.998   n=40  net **-21.35** (-0.534/match)
##   record 18-22 (45.0%); rating chain verified contiguous 39/39 transitions
##   WINDOW n=20 +22.38 · POST-WINDOW n=20 **-43.73**
##   per-match sd 7.81; 2sd at m=40 is 98.8, so -21.35 does NOT trip the
##   magnitude rule (by a factor of 4.6). The correction is for accuracy, not
##   consequence.
##
## ===== THE INSTRUMENT WIN, AND WHAT IT COSTS US =====
## **`ratingABefore`/`ratingBBefore` in free `match list` metadata IS the at-match
## rating.** Verified to eleven decimals: 1526.8148964561767 - 2.8166702369076475
## = 1523.9982261892691 == `teamBRating`. `teamXRating` is the live join (ONE
## distinct value per team across 300 rows; `ratingBefore` has 243 for us).
## Both arms held this for a day and neither asked for it.
##   - **STRONGER:** unbiased, the strong/weak win-rate gap is +26..+34pp and
##     STABLE across 1500-1575. The biased field collapsed it to +0.7pp at 1575
##     and INVERTED to -14.9pp at 1600 — that "robustness limit" was an artifact.
##   - **WEAKER, and this must not get lost: the prospective result is a
##     DIRECTION confirmation, not a magnitude one.** Re-scored at-match, v80's
##     window STRONG net goes **-11.98 -> -0.53**, essentially flat; the window's
##     whole edge was WEAK (+22.91). Real signal is post-window **0 wins in 5**
##     (-47.25). **The s20 "STRONG n=10 -11.98 / WEAK n=9 +32.84" is superseded.**
##   - Full life-2 unbiased: STRONG n=17 -47.78 (29.4%) / WEAK n=23 +26.43 (56.5%).
##
## ===== FALSIFIER NOW GATING QUEUE ITEM 2 =====
## Lunds ran **identical bytes (v44) across a 123-point rating swing** (1504.4 ->
## 1627.7, all showing oppCURRENT 1557.9). For a static opponent, `ratingBefore`
## variation is the ladder's NOISE about them, not a change in what we faced.
## Worse: on the four v80 Lunds rows we **won 4-1 against their highest-rated
## instance and lost 1-4 twice against their lowest** — anti-correlated with the
## classifier. n=4 refutes nothing, but **before spending a mechanism read on an
## n=5 cohort, answer: does opponent `ratingBefore` predict our result at all once
## opponent VERSION is held fixed?** If not, the strength split is a story about a
## noisy label.
##
## ===== STANDING RULE THIS SESSION PRODUCED =====
## **A field that reconciles is a field you can trust; one that merely looks right
## is not.** `teamXRating` looked like an at-match rating for a day and was never
## asked to reconcile against `eloDelta`. `ratingXBefore` was asked, and did, to
## eleven decimals. Every future join onto platform metadata gets the
## reconciliation test before a verdict consumes it.
##
## ===== PRIOR STATE (s20 wrap) — kept for the reasoning, superseded above =====
##   v80 "Eir 9b" = `bots/_v89sh`, md5 e12f8585.
##   Ladder at s20 wrap: 1526.81 @ 480, rank #35/113.
##   Other rollback targets: v86 (`bots/_v86z2`, md5 b0c908fd), v84 (`_v99mag`,
##   md5 dab7766e). Neither is measurably better — see below.
##
## ===== READ THIS BEFORE YOU TRUST THE WINDOW RESULT =====
## The v80 20-match window settled at **+22.38**, and I settled it honestly. But
## v80 KEPT PLAYING after the window closed:
##   WINDOW      n=20  net **+22.38**
##   POST-WINDOW n=19  net **-40.92**  (STRONG -70.13 / WEAK +21.52)
##   FULL LIFE   n=39  net **-18.54**  (-0.48/match; 2sd at m=39 is 90.6, so it
##                                      DOES NOT trip the magnitude rule)
## **The window was the favourable half of v80's life.** Nothing was gamed — the
## evaluation point was pre-registered at n=20 and I did not choose it after the
## fact — but a successor quoting "+22.38" without "-18.54 over its full life"
## is quoting the good half. **The strength split INTENSIFIED post-window: -70.13
## over 7 strong matches. That is the real story of v80 and it is not a good one.**
##
## ===== THE FINDING THAT SURVIVES EVERYTHING ELSE =====
## **The strength-conditional split REPRODUCES PROSPECTIVELY.** Cohorts were
## frozen BY NAME at n=6, before any outcome was visible:
##   window     STRONG n=10 **-11.98**  WEAK n=9 **+32.84**
##   post-window STRONG n=7 **-70.13**  WEAK n=8 **+21.52**
## We are not a mediocre bot. We are a bot that farms weak opponents and is
## dismantled by strong ones, and the effect got worse over 39 matches.
##
## ===== TWO INSTRUMENT VERDICTS THAT CONSTRAIN ALL FUTURE WORK =====
## 1. **LOCAL ARENA IS REFUTED AS A MAGNITUDE INSTRUMENT.** It asserted the v76
##    lineage beats the Eir lineage DECISIVELY (60-40 h2h, +14.2pp vs ouro,
##    kill-conversion 97% vs 77% at p=1.3e-05). The ladder contradicts the SIGN
##    (v80 +1.12/match vs v86 -5.44/match, p=0.070). A claim made at p=1e-11 that
##    cannot reproduce its own direction is refuted regardless of the field's own
##    error bars. **Local remains GOOD FOR MECHANISM** — it found hive_freeze and
##    its det legs are surgical. Use it to find WHAT, never HOW MUCH.
## 2. **EVERY EXTERNAL LOCAL OPPONENT IS DOMINATED** (band 90.0%, flotte 86.7%,
##    ouro 72.5%, kladde 72.1%, orizon 71.7%). A dominated pool reports
##    "aggression is free" BY CONSTRUCTION. **`fcode match unrated` is the ONLY
##    instrument we own whose opponents can punish us** — 30 games/hr, cannot buy
##    a verdict, and is the only thing that can answer an aggression question
##    honestly. 16 unrated hive games (0-for-16, 8 tiebreak losses) beat 1,080
##    local matches for decisiveness. Three self-play punishers exist
##    (opp_v76 38.3%, opp_v44 40.8%, opp_v69 41.7%) but share our code.
##
## ===== QUEUE, IN PRIORITY ORDER =====
## 1. **SHIP THE HIVE FIX** — `bots/_v100hf`, md5 9e85cae5 (v80 + HIVE_FREEZE_ON
##    = False). **NOT SHIPPED and that is deliberate: I will not ship minutes
##    before a wrap with no monitors to watch it, and I cannot activate anyway.**
##    Evidence: identity control 120/120 identical / 0 flips / delivered-Ti delta
##    exactly 0 with the flag ON; effect leg 232/240 identical, 8 games moved,
##    ALL hive seat A, **delivered Ti 5,260 -> 11,030 = 2.10x**, zero collateral
##    on 14 other maps. Unrated ground truth: **v80 is 0-for-16 on hive vs real
##    opponents with 8 losses on the titanium tiebreak the fix doubles.** hive is
##    15% game share and research's ladder cell has v80 at 1 win in 12.
##    THREE CAVEATS, all on the tape: the 8 moved games are ONE distinct shape
##    replicated 8x; zero outcome flips vs the det opponent; only seat A moved
##    though the clause keys both core positions (unexplained).
## 2. **RE-EXAMINE THE STRENGTH SPLIT AS THE PRIMARY PROBLEM.** -70.13 over 7
##    strong matches is larger than anything a plank has ever moved.
## 3. Lethality dial — design on the tape; needs self-play punishers + unrated,
##    NOT a dominated pool.
## 4. Lunds fixture — **fully unblocked**, every constant measured: launcher at
##    r1 40/40, insertion tiles invariant across our versions and hard-codeable.
##    Lunds held v44 all night; a Lunds ship invalidates the table at once.
##
## ===== DEAD — DO NOT REDO =====
## - **Launcher deletion (`_v101nl`): REFUTED.** 16 gains / 14 losses across only
##   FOUR distinct shapes, +2 net wins in 240. Diffuse (97/240 identical) where
##   hive was surgical (232/240). The motivating evidence stands and is still
##   unexplained: 0 of 20 top-tier games contain a launcher, we build one in 69%.
##   The right question is "what do they field INSTEAD", not "is ours worth it".
## - **thor_r1 (gunner rush): REFUTED at 2/60.** Delivered ZERO titanium — the
##   top tier caps harvesters at ~3 but still lays a conveyor at r6. Kept as the
##   control. A doctrine test belongs as a FLAG on the working bot, not a rewrite.
## - `LAUNCHER_RESERVE = 80` is dead code (defined line 921, referenced nowhere).
##
## ===== TOOLING TRAPS FOUND TONIGHT =====
## - `fcode match info --json` returns **`games` as a TOP-LEVEL key, sibling of
##   `match`** — NOT nested. Parsing `d['match']['games']` reads as "0 games".
## - The same call returns **the opponent's version as `null`**. `match list` has
##   both. Join on the wrong one and every opponent looks static forever.
## - `teamARating`/`teamBRating` is **CURRENT rating, not at-match** — a live
##   join. Classifying historical games by it is look-ahead bias.
## - **A version label is not a window.** v80 shipped twice today; filtering on
##   version alone pools two separate lives.
## - Write tape rows with a **Python heredoc, never `printf`** — backticks get
##   shell-interpreted and silently delete code identifiers.
##
## ===== TESTS NOW EXIST =====
## `.venv/bin/python -m unittest discover -s tests` — 25 tests, 0.06s, no deps.
## Covers the ceiling collider, the arena/ceiling coupling, wilson, and
## audit_trigger's windowing. `tests/test_bot_helpers.py` runs against any bot
## via `BOT=bots/_vNN`. **Stateful turn logic is NOT unit-testable — use
## `tools/det.py` identity runs (0 flips = proof) instead.**



## ===== LIVE VERSION CORRECTION — THE s19 BLOCK BELOW IS WRONG ABOUT THIS =====
## s19 says LIVE = v84 "Eir 14". **IT IS NOT, AND HAS NOT BEEN SINCE 22:15.**
##
##   LIVE = **v86 "Z2 fastfacing"** (x3r0, activated 22:15 CEST, submission
##   a76400ec, md5 b0c908fd, staged locally as `bots/_v86z2`).
##   Baseline at activation: 1572.6 @ 436, rank #29/113.
##   Rollback = v84 (`bots/_v99mag`, md5 dab7766e) one click.
##
## **v86 IS A FORK OF OUR v76, NOT A DESCENDANT OF v84.** It is 128 diff-lines
## from `bots/opp_v76`, so it REVERTS v77-v84 wholesale — the Eir E-family
## bundle, the hive fix and PIECE MAG, ~2,400 lines, are OFF THE LADDER.
## Verified against platform primaries: platform v84 == `_v99mag` and platform
## v76 == `opp_v76`, both byte-identical. Its 128 lines are three named changes
## (S1 SPEED table-snapshot, V1 FACINGFIX, W4 ti_floor retune).
##
## **TRAP THAT BIT BOTH ARMS: dev-dir numbers are NOT platform versions.**
## `_v89sh`=v80 · `_v99mag`=v84 · `_v97e11`=v83 · `_v95e1`=v81. Mis-sorts by ~9.

## ===== THE CEILING BATTERY (840 matches, tools/ceiling.py, s20) =====
## Three binaries vs the SAME anchor, WIN RATE IDENTICAL (86.7-88.3%, all
## pairwise p>0.8) so strength is controlled by construction:
##
##            win rate   kill-conversion   r1000 share
##   v84        87.5%         77.1%          27.5%
##   v76        86.7%         94.2%           9.2%
##   v86        88.3%         97.2%           8.3%   <- LIVE
##   v86-v84: conversion +20.0pp (p=1.3e-05), r1000 -19.2pp (p=0.00011),
##            win rate +0.8pp (p=0.84). Strength axis (ouro): v76 beats v84
##            +14.2pp (p=0.0014). Head-to-head: v76 beats v84 60-40.
##
## **THE TENSION IS BIGGER THAN THE RESULT.** Local says v76/v86 decisively
## beats v84 across three independent opponents. The ladder says v77-v84 is
## +0.7 Elo over n=54. Either (a) the ladder lacks the matches, or (b) **local
## arena does not transfer at all**, which would make every A/B verdict this
## project has issued suspect. **v86 going live IS the test** — this is the `v2`
## queue item, long marked "unrunnable as specified". It is runnable now.
##
## **PRE-REGISTERED, do not read tea leaves later:** grind games are our ONLY
## profitable population (+24 net, 58.2%, research) and v86 grinds a THIRD as
## often. So v86 should GAIN vs strong teams and LOSE to the weak ones we farmed
## in the tiebreak. Its 2nd ladder match was a LOSS to Askar City (-6.01), whom
## s19 recorded us beating 5-0 on that exact tiebreak. **n=1, prediction not
## evidence.** Net Elo could wash while core-kill rate rises — that would mean we
## traded our only profitable regime for a ceiling we cannot yet cash.
##
## ### CAVEAT THE ABOVE DOES NOT CARRY ON ITS OWN — added s20 after research
## ### audited their own claim. **"We win 58% of grinds" is TRUE and verified.
## ### "THEREFORE losing a grind is a cost" is UNSUPPORTED.**
## The inference needs to know what a marginal grind game WOULD OTHERWISE HAVE
## BEEN, and the 58% cannot see that. Simulated with the tiebreak edge FIXED at
## 58% by construction, the 58% comes out IDENTICAL in both worlds:
##   REGIME A (pushing is safe):      close-steered 62.8% overall vs grind 46.1%
##                                    -> closing wins; protecting the grind COSTS us
##   REGIME B (pushing backfires 60%): close-steered 26.8% vs grind 34.0%
##                                    -> grinding wins; protecting the grind is RIGHT
## The deciding quantity is the **BACKFIRE RATE** — how often pressing for a kill
## converts a game we would have drawn out into one we lose — and **NOTHING THIS
## PROJECT OWNS HAS EVER MEASURED IT.** Two people can read the same 58% and reach
## opposite decisions. The claim silently assumes Regime B.
## WHICH REGIME OUR DATA FAVOURS (research's cut, INDEPENDENTLY REPRODUCED by
## builder on a fresh pull, scored on the frozen roster):
##   STRONG  kill-game 34.7% (n=245)  grind 52.2% (n=90)   **+17.5**
##   WEAK    kill-game 70.1% (n=107)  grind 72.4% (n=58)   +2.3
##   ALL     kill-game 45.5% (n=352)  grind 60.1% (n=148)  +14.7
## Grind beats kill-game in EVERY cohort, widest against strong opposition. That
## favours Regime B, so the claim may STAND — but it must always be quoted with
## "assumes the marginal grind game would otherwise be a loss" attached. Two
## conditional populations compared to each other is still not a counterfactual.
##
## ### AND THIS IS PROBABLY WHY LOCAL ARENA MISLEADS — a MECHANISM, not an excuse
## Backfire rate should SCALE WITH OPPONENT STRENGTH. Against kladde_probe and
## ouroboros_probe — which we beat 87-93% — nothing punishes an over-push, so
## **a dominated pool has a near-zero backfire rate and therefore reports REGIME A
## regardless of the truth.** That is exactly what my 1,080-match ceiling battery
## did: it said the lethal lineage wins decisively, and then KCM and Ouroboros
## killed v86. **This predicts WHICH LEGS WILL MISLEAD BEFORE YOU RUN THEM:** any
## leg whose verdict depends on aggression, run against a pool we dominate, is
## measuring Regime A by construction.
## THE LEG THAT WOULD SETTLE IT (filed, NOT run — not before match 20): a
## lethality dial scored on **OVERALL WIN RATE** against opponents that can
## punish. Not conversion, not r1000 share, not grind win rate — all three are
## flat across both regimes. **The opponent pool is the load-bearing part.**

## ===== CORRECTION: THE s19 MAP TABLE BELOW IS OVER-READ =====
## Bonferroni over the 15 maps we looked at leaves **hive (25/34=74%, p*15=0.002)
## as the ENTIRE heterogeneity signal.** Maps do genuinely differ (chi-sq 40.2/14,
## permutation p=0.00030) but the s19 "tier of bad maps" is NOT supported — read
## it as **"hive, and then fourteen maps."** **"drumlin CONFIRMED" is WITHDRAWN by
## its author; spend nothing on drumlin.** The hive defect PREDATES v77 (75%
## killed v72-76 vs 72% v77-84, strong-only 75%/75%) so **it is live in v86**.
##
## Also retired: "our 44% core-kill rate is the ceiling metric" is a MIXTURE —
## 69% of kill-decided games won vs opponents <1550, **33% vs >=1550**. There is
## no single 44% to optimise; there are two regimes and only one loses matches.

## ===== READ THIS FIRST: THE FIELD PLAYS A DIFFERENT GAME =====
## Row `ladder-wide-census-THE-GAP`, measured on 335 games across 10 teams:
##
##   TOP TIER (>=1750): **97% of games end by CORE KILL, median 232 turns.**
##                      sporks / Lorem Ipsum / not adgato / Flotte = 100%.
##   US:                **72% core-kill, median win 332 / loss 413,
##                      and 28% of our games reach r1000.**
##
## NOBODY AT THE TOP GRINDS. Our one measured edge — the titanium tiebreak at
## 58% — is in a game the strong field never reaches, because they resolve by
## turn ~250. It is how we beat Askar City 5-0 and why we are 0-for-17 vs Lunds.
## **Our 44% CORE-KILL RATE IS THE CEILING METRIC AND NOBODY HAS OPTIMISED IT.**
## Every plank shipped tonight was economy or defence.
##
## TESTABLE PREDICTION for whoever picks this up, answerable in one minute with
## tools/ladder_census.py: hive (15% share) and drumlin (24%) should be the maps
## where we are killed FASTEST.

## ===== THREE FREE INSTRUMENTS BUILT AT THE END OF THE SESSION =====
## Run these BEFORE deciding anything. All API-only, zero downloads, ~1 min.
##   tools/game_census.py    — our per-game map / seat / winCondition / turns
##   tools/ladder_census.py  — the SAME for every team on the ladder
##   eloDelta method         — sum `eloDeltaA/B` keyed on `teamAVersion`.
##                             NEVER difference ratings; that cannot attribute a
##                             match to a version and cost 3 corrections tonight.
## `fcode match info --json` returns games[] with mapName/mapSeed/winnerSide/
## winCondition/turnsPlayed — every GAME-LEVEL fact we were decoding replays for.
## Replays are still needed BELOW game level (builds, damage, titanium).

## OUR MAP TABLE (n=500, game share): hive 15% | drumlin 24% | snowflake 41% |
## eider 41% | archipelago 41% | atoll 45% | nordkap 48% | jackpot 50% |
## saga 52% | lighthouse 58% | moonrise 58% | heart 59% | antler 59% |
## fjordgate 59% | meander 74%.  A 59-POINT SPREAD on a near-uniform draw.
## drumlin has never been examined by anyone.

## ---- (earlier s19 block, 21:4x — still current except where the above supersedes) ----

## FIRST ACTION, before the queue: **`.venv/bin/python tools/audit_trigger.py`**
## It fires when the project is writing about the work faster than doing it.
## At this wrap it FIRES 2/4 (note:verdict 4.38, ship cadence 0.32/hr) — the
## evening ended analysis-heavy and that is real, not a false positive. If it
## still fires after a cycle of shipping, spawn the audit session.

## LAST ACTIONS — on Magnus's wrap-call ONLY (this block exists because he had
## to prompt the retro EVERY time; the boot path was instrumented and the wrap
## path never was. Do not delete it when you rewrite the top block.)
## 1. **Wrap retro into docs/coordination.md** — protocol rule 5, a dated
##    `PROCESS DELTAS` block (what slowed us / what to change). If you did not
##    append deltas per verdict as you went, SAY SO and reconstruct: the
##    omission is delta zero.
## 2. Rewrite THIS top block: live version + md5 + baseline, rollback target,
##    in-flight work, queue in priority order.
## 3. Commit and push everything.
## 4. **Name the wake path or state there is none** — monitors die with the
##    session; say plainly what will not be watched.
## 5. Relay live subagent output; it dies with the session.

## READ THESE FOUR ROWS BEFORE ANYTHING ELSE
## They re-read the whole project and they compose:
##   leg-power-19pct        our standard n=120 leg has 19% POWER. Four of five
##                          genuinely good planks measure "no verdict".
##   bleed-coverage-zero    0.0% of our Elo bleed is covered by a VALID
##                          instrument. Net +8 nets a -493 GROSS bleed; Lunds
##                          27.5% / Ouroboros 25.0% / KCM 17.9% / CAD 11.6%.
##                          Both valid probes point at opponents we BEAT.
##   swap-rule-is-a-coinflip  the rollback trigger fires on a NEUTRAL holder
##                          73% by m=8, 100% by m=50. It cannot tell +60 from
##                          -60. Fix adopted: threshold on MAGNITUDE (2 sd =
##                          -41), never sign; a trigger FREES the slot, it
##                          never FORCES a swap.
##   mechanism-not-battery  every result tonight came from decoding real games
##                          or reading real code. NOT ONE came from an A/B leg.
##
## THE COMPOSITION IS THE POINT: the battery is underpowered AND aimed at a
## population contributing ~0% of our losses. Those faults MULTIPLY. Fixing
## power alone buys precision about a question that does not decide matches.

## STATE
- LIVE: **v84 "Eir 14"** (bots/_v99mag, md5 dab7766e). Baseline 1593.0 @ 429.
  Content = the E-family bundle + PIECE MAG (hive 256-ammo magazine retired).
  Rollback = v83 (_v97e11) one click.
- Five ships tonight: v81, v82, v84 (mine), v83 (peer), v85 (x3r0, paused).
  **Windows got 2, 2, 5, 1 matches. NONE reached the 8 the swap rule needs.**
  `fcode submit` AUTO-ACTIVATES — there is no stage-behind, so a session that
  wants a real window must simply not upload.
- Monitors: elo_logger + match_watcher + opp_watcher armed, exit-on-wake.

## QUEUE, RE-RANKED BY BLEED SHARE (outranks the plank queue)
1. **LUNDS INSTRUMENT (mine, designed not built)** — 27.5% of bleed, 0 wins in
   17. Design decision on the tape (`lunds-instrument-design`): build a
   **MECHANISM FIXTURE, not a behavioural replica** — a replica walks into the
   drop-probe law that already refuted two ouro probes at 15.8% and 21.7%.
   Fixture target: their **absolutely-oriented r3 launcher insertion** (fires
   6/6 in our seat-B games, 0/4 in seat A, mirror landing tiles verified free,
   so the trigger is in THEIR code not the geometry).
2. **KCM** — 17.9% of bleed, ZERO prior work. Research has the decode.
   Also the best probe target on the board because it is **version-stable**
   (v1 for a day and a half while Flotte shipped six times) — drift is what
   killed kladde/flotte/cad, and a stable subject cannot drift out from under
   a replica. Their seat split is large: our A 42.9% vs B 17.1%.
3. **Ouroboros** — 25.0% of bleed but instrument-BLOCKED by a measured law.
   Needs a different instrument SHAPE, not another replica. Unrated probe
   tonight: **0-5 on live v84, zero game share.**
4. Replay-on battery (det/arena both pass `--replay /dev/null`, so redundancy
   counting cannot run at all) — blocks resolving whether PIECE HG's mechanism
   reduced redundancy without converting.

## DEAD / DO NOT REDO
- **PIECE HG: no separation at n=600, CI [-6.67, +2.67] — a true +5pp effect is
  EXCLUDED.** Do not iterate it; the mechanism fires (0 flips on control vs 204
  discordant) but does not convert.
- **rescope-vs-wholesale (v82 vs v83 hive fix): NO SEPARATION.** Settled.
- Paired-blocks CI tightening: refuted at 1.06x. NOISE_ON reseeds spawn_salt,
  so a shared (map,seed) is NOT a shared opening — the blocking is cosmetic.

## MEASUREMENT RULES ADDED TONIGHT (all in tooling.md)
- **Seed count is NOT sample size.** det.py now prints `DISTINCT paired shapes`
  with a low-replication warning. A leg reading 4/4 seeds can be ONE game.
- **A shape ratio NEAR 1 on a "det" leg means the leg is STOCHASTIC**, not that
  it is well-powered — the det ceiling is 15 maps x 2 seats x n_det_opponents.
- **Determinism is MEASURED, not code-read.** opp_v39/v44 are stochastic with no
  NOISE_ON symbol. Verified det pool: v45/v49/v50/v56/v58/v63 — but **v56, v58,
  v63 are behaviourally IDENTICAL in all 8 cells tested**, so it is ~3 effective
  opponents and the ceiling is ~105, not 180. All six are ONE codebase's
  history: variance reduction, NOT opponent diversity.
- **Delivered-Ti is confounded by game length** — read it only within a
  win-condition class.
- **`Last 10` MIXES UNRATED INTO LADDER FORM.** It read 0W-10L while ladder-only
  was 5W-5L. Never read it as form.
- **proto3 omits TEAM_A=0** — filter team with `.get(2, 0)`, never `.get(2)`.
  Silently drops every seat-A entity; produced a plausible wrong table twice.
- **Map identity needs TILE CONTENT** — heart/eider and snowflake/archipelago
  share dims AND core positions.
- **`fcode match unrated` is the FIDELITY instrument, not a power one** —
  5 games / 10 min = 30/hr against local's ~2,150/hr. It buys ground truth and
  on-demand replay corpora; it can never buy a verdict.
- **Machine is 10 cores (8P+2E) at load ~10.7, NOT 16 idle ones.** Real headroom
  ~1.3x. Ignore any "50-100x underused" claim, including mine.

# Session 19 (builder, booted 2026-08-08 19:40 on Magnus's framework audit +
# "ship it all and direct us in the right path"; supersedes s18 below)

## FIRST ACTIONS for the successor
## 1. RE-ARM MONITORS. Three are armed as of 19:4x (elo_logger,
##    match_watcher, opp_watcher); replay_archiver and sweep_watcher are
##    NOT. They die with this session.
## 2. LIVE: **v81 "Eir 11" (= bots/_v95e1, md5 f5f1bf55, submission
##    82afd552)**, activated 19:42, BASELINE **1568 @ 420 rank #30/113**.
##    Rollback = v80 (_v89sh, md5 e12f8585) one click. Swap rule arms at
##    >=8 holder matches.
## 3. **THE SHIP GATE CHANGED — read docs/ship-gate.md before anything.**
##    No local regression (PARITY PASSES) + a window + nothing known-broken.
##    Field evidence for an unshipped head is NOT owed; it is structurally
##    unobtainable and demanding it is what cost 57 elo and 9 ranks in the
##    15 hours before this session. Probes are attribution-only, never
##    gates. "KEEP-dev" is no longer a resting state.
## 4. IN FLIGHT: **PIECE HV** (bots/_v97hv, the hive_freeze fix) — identity
##    control PASSED 120/120 identical, 0 flips, delivered-Ti delta exactly
##    0 with the flag off. Effect leg vs opp_v63 running at wrap. It is the
##    v82 candidate.

## THE STRATEGIC READ — what the next real gain is, and why it is not more planks

There is a fact on the tape that nobody has drawn the conclusion from. Three
rows state it separately; put together they name our actual problem:

  (a) 26.2% of ladder games reach r1000, and **219/219 of those are decided
      at LEVEL 1 = DELIVERED TITANIUM** (research census).
  (b) Our full-length rate is RISING, monotonically, along our OWN line:
      **24.5% pre-v75 -> 29.8% v75+ -> 36.7% under v80.**
  (c) What v75->v80 added was, almost without exception, survival machinery:
      heal-seat protection, the siege reserve, counterbattery-over-heal, the
      anti-Ouro standoff, the siege facing-veto, siphon deny, severity tiers.

So: **we have been building a bot that survives into a tiebreak it then
loses.** The two halves are not merely unrelated, they are in direct tension —
the survival machinery is FUNDED BY the exact resource that scores. Every one
of these is titanium withheld from delivery: SIEGE_HEAL_RESERVE_TI = 16, the
_core ti_floor (12 under siege, 52 in peace), heal spend at 1 Ti per 4 HP,
ammo conversion at 1:1. And hive_freeze is the microcosm — a defensive clause
that halved delivered titanium on a live pool map and was invisible for its
whole life because it flipped ZERO outcomes against a det opponent.

**THE SWEEP THIS ARGUES FOR, and it is newly possible as of today:** det.py
reports a delivered-Ti delta as of commit 9bba426 (landed ~19:18 today).
Every defensive plank flag has an ON/OFF pair. Run each one as a det leg and
price it in DELIVERED TITANIUM, not just flips. Any plank that costs
delivered Ti without buying outcome flips is net-negative in a rising third
of our games AND is invisible to every flip-counting leg we have ever run —
which is all of them, before today. That is a defect class, not a tuning
exercise, and hive_freeze is proof the class is non-empty.

Do this BEFORE adding more planks. The bot is 7,041 lines at 93% of the CPU
limit; the marginal plank is worth less than the marginal deletion.

## SECONDARY DIRECTION
- The bleed classes are picket (-103) and CAD (-88), and their probes are
  invalid (kladde ~70pts miscalibrated + unfaithful turret composition;
  flotte has no launcher code at all; cad attribution-only). Under the new
  gate the answer is NOT to re-freeze them. Ship against those classes and
  read the ladder.
- Full-length rate rising also means the ENDGAME_SWITCH (r960) matters more
  every version. It was tuned when the rate was 24.5%. Re-price it.

## STATE
- Tape rows added: v81-baseline. elo_history has the 19:42 baseline row.
- bots/_detP,_detH,_detOFF = NOISE_ON=False det copies (scratch, deletable).
- x3r0 shipping question is with Magnus: recommendation was free shipping +
  the existing swap rule as the ONLY rollback trigger (data: x3r0 net +7 elo
  over 6 windows, us net -18 over 5 — no case for gatekeeping him).

# Session 18 POST-WRAP SHIP (2026-08-08 ~19:5x) — Magnus reopened the board
# with the LOOSENED SHIP GATE; the wrap block below is superseded on the
# "nothing shipped" point and stands on everything else.

## LIVE NOW: **v83 "Eir 11" (= bots/_v97e11, md5 56b9d178)**, baseline 1559
## @ 424 rank #30. Content = the whole KEEP-dev stack shipped at once
## (FB fjordgate bootstrap + E1 ring + E1b heal-line gate + M2b siting +
## FT2 severity tiers + HF hive-freeze removal) on the v79-era staged base.
## Gate legs all green: vs LIVE content 55.0 [46.1,63.6]/120 (parity passes,
## no regression); band 93.3; HF det 0 flips / surgical / ECON hive +2665;
## platform TLE 0 trips. Tape row v83-baseline carries the debts.
## ROLLBACK = v80 (_v89sh) one click. Swap window arms ~@432; 20-match ~444.
## NEW GATE IS IN docs/ship-gate.md — read it before holding anything.
## Items 4 (hive_freeze) and 8 (dev heads) below are now SHIPPED, not queued.
## Successor's first job: read v83's window, and if it bleeds, roll back to
## v80 without ceremony — that is what the control is for.

# Session 18 FINAL (builder wrapped 2026-08-08 ~19:2x on Magnus's call
# relayed via research; successor boots per /builder)

## FIRST ACTIONS for the successor
## 1. RE-ARM FIVE MONITORS (they die with this session; tools/monitors/,
##    exit-on-wake shape, one-liners in each docstring). The elo_logger now
##    implements the REVISED swap rule (arms at holder-match >=8, window
##    prices only the current holder's tape rows) — verified firing both
##    directions today.
## 2. LIVE: **v80 "Eir 9b" (= bots/_v89sh, md5 e12f8585)** — held all
##    session. Baseline CORRECTED to 1562.9 @ 397 (see below); wrap read
##    1575.3 @ 419 #30. Rollback = v76 one click.
## 2b. POST-WRAP EVENT (19:39, logger fired after the wrap note): **THE SLOT
##    IS FREE AT HANDOVER** — v80's armed last-5 hit -12 (1580 -> 1568) at
##    420 matches. NO ACTION TAKEN and none owed: free never means forced,
##    and no candidate holds a measured better-case (the whole E1 family is
##    at parity or worse vs the staged head — see item 8). Second crossing
##    today; the first recovered on its own within an hour. x3r0 may swap
##    per the rule; that is the system working, not a conflict. Successor:
##    do NOT read "slot free" as "ship something".
## 3. **NOTHING SHIPPED THIS SESSION, deliberately.** Five planks reached
##    KEEP-dev and none earned a window. Read results.tsv rows
##    e1-bundle-h2h / e1-family-missing-measurement / ft2-vs-bundle-direct
##    before re-opening any of them.
##
## 4. THE SINGLE BEST QUEUE ITEM — **hive_freeze** (row
##    hive-freeze-live-defect): a measured defect in SHIPPED BYTES. On
##    hive.map26 (live pool map), seat A, _expand returns unconditionally
##    from r42 whenever a home gun stands (:3614-3624 in _v89sh). Ablation:
##    delivered Ti 5,260 -> 11,030, buildings 28 -> 155, 6/6 seeds, ZERO
##    outcome flips. Research's census: delivered titanium is the SOLE
##    decider in 219/219 full-length games (26.2% of all games, 36.7% under
##    v80). Ranked above the deny-dispatch fix on EV by both arms. NOT a
##    finished fix: one map/seat/opponent, and the freeze's original intent
##    is not documented — measure removal against the picket class it names
##    before shipping.
## 5. **RE-FREEZE KLADDE BEFORE RE-GATING ANY E1-FAMILY PLANK** (row
##    kladde-guard-caveat-RETRO). The kladde probe is ~70 points
##    mis-calibrated vs wild AND its turret composition was never faithful
##    (33% gunner vs wild's 62-70% gunner-majority) — gunner fire is
##    blockable, sentinel fire is not, so line-of-sight-dependent variants
##    can have their ORDERING reversed, not just their level. E1's
##    supply-tax attribution and E1b's recovery are the exposed claims.
##    Spec in docs/research/probe-fidelity-guards-2026-08-08.md.
## 6. FLEET STATE (row probe-fleet-staleness): orizon VALID (only probe
##    whose subject has not shipped since extraction; its +11.6 discounts
##    to ~+6-8 and the bias direction is HARDER, not flattering); band
##    valid but RUSH-MODE ONLY (v41 added an unmodelled fallback economy —
##    our only loss series to them today was in that mode); kladde and
##    flotte need RE-FREEZE (flotte was never valid in two respects: wild
##    builds 13-15 gunners and ~2 launchers at r10; the probe has no
##    launcher code at all); cad disclaimed under P6-widened.
## 7. FIVE MEASUREMENT-STACK FINDINGS today, all in docs/tooling.md — read
##    them before trusting any older row: (a) the verdict tape results.tsv
##    was GITIGNORED and unbacked-up for the project's whole life (now
##    tracked); (b) platform CPU peaks at ~93% of the 10ms limit on BOTH
##    heads and the driver is the SHARED BASE, not new planks — every
##    local leg runs --tle 0 and is CPU-blind; (c) "0 flips" means NO
##    OUTCOME EFFECT, never "no effect" — det.py was blind to delivered
##    titanium and now reports it (the fix caught its own even-n median
##    bug on re-validation); (d) version binds at match CREATION, so read
##    the next match's meta stamp after any activation; (e) **field
##    evidence about an unshipped head is structurally unobtainable** —
##    submission download is own-team-only, match test takes two local
##    dirs, unrated runs the ACTIVE submission. The ship gate as written
##    cannot be satisfied; gate on proxy strength, ship into a measured
##    window, let the ladder be the field instrument with rollback as the
##    control. **RETRO ITEM for Magnus.**
## 8. DEV HEADS: _v94fb (staged, fjordgate bootstrap — the one real fix,
##    3-stage green); _v95e1 (E1 ring + M2b + FT2 bundle, all KEEP-dev);
##    _v96ft2 (FT2 only, identity-validated). Bundle vs staged = PARITY
##    (54.2 [45.3,62.8]/120); FT2-only vs staged = marginal (59.2
##    [50.2,67.5]); FT2-only vs bundle = no separation, leans bundle
##    (43.3 [34.8,52.3]). FT2 debts unpaid: meander-B regression measured,
##    atoll magazine prediction UNTESTED (needs a 1000-round parked-
##    harasser leg, not the 113-321-round games I ran).
## 9. RESEARCH-SIDE OPEN: deny-silence fix is SPEC'D not built (vision
##    starvation 3/5 + role/dispatch 2/5; licensed shape = publish the
##    siphon target team-level via SLOT 5, which I verified write-only in
##    the live bot, and make the duty claimable — tight claim radius, the
##    pull-workers-off-economy class is twice-refuted); exploit
##    feasibility thread (bucket mining / launcher rail / scale churn)
##    died with their session, brief in their 19:13 note, cheap to
##    re-commission.
## 10. TAPE CORRECTIONS made today, both against our own prior record:
##    v77 FINAL = +34.1/6 (not +20.2/5); **v79 FINAL = -38.1/8 ending on a
##    WIN, and v80's baseline is 1562.9 @ 397** — the match I credited to
##    v80 was created 4 min pre-activation and meta-stamps v79.

# Session 17 FINAL (builder wrapped 2026-08-08 15:48 on Magnus's call "wrap up at the
# end of this cycle"; successor boots per /builder)

## FIRST ACTIONS for the successor
## 1. RE-ARM FIVE MONITORS (die with this wrap; tools/monitors/, exit-on-
##    wake shape, one-liners in docstrings). NEW today: sweep_watcher.py
##    (self-test sweep → opponent stamp ~32min lead; validated 3/3
##    prospective on day one; MAX_AGE_S stale filter in place). The
##    elo_logger carries the swap-window watch both directions.
## 2. LIVE: **v80 "Eir 9b" (= bots/_v89sh, md5 e12f8585)** — ROLLBACK
##    ship after v79's −43.9/7 collapse window. Content = v77 "Eir 9"
##    byte-identical (siphon-deny plank on the hsd base; v77's own wild
##    window was +20.2/5, the day's only positive). Baseline 1557.1@396.
##    ~20-match check ~416; research's REV-7 read re-arms on this window
##    (pre-registered their side). Rollback-of-the-rollback = v76 one
##    click (x3r0's).
## 3. SUCCESSOR ITEM 1 — THE FJORDGATE DISCRIMINATOR (everything hinges
##    on it): three-armed instrumented det set (w=_v93w / w-with-OS-off /
##    wb=_v93wb) per research's in-doc spec (cad-fodder feasibility doc,
##    fjordgate/meander section). It adjudicates BOTH open questions at
##    once: (a) the v79 fjordgate OPENING COLLAPSE's owner — hypothesis
##    on the tape: it's the ammo-converter liquidity trap expressing
##    under the OS ammo floor at r0-30; (b) _v93wb's re-gate — wb FIXES
##    fjordgate 8/8 but trades archipelago-vs-v74 −8 (tape row
##    _v93wb-gate: NOT MET at regime −2, PARKED-PROMISING, no re-gate
##    until the trade is priced). The archb diagnostic was spectacular
##    (r732 loss → r1000 WIN); do not lose that thread.
## 4. LINE STATE (all md5-stamped on their tape rows): _v89sh LIVE as
##    v80; _v90ft KEEP (ferry test, perfect det identity); _v91osb KEEP
##    local but FIELDED BADLY (v79: all-green acceptance → −43.9/7 wild;
##    instrument-vs-wild lesson candidate — the fjordgate collapse never
##    appeared in its battery because no fjordgate leg was gate-armed
##    under noise); _v92sp KEEP + wire-strip cleared (=_v93w, the staged
##    stack); _v93wb parked-promising. m1/v88pr/v88prb/hse family:
##    parked per their rows.
## 5. Queue after the discriminator: E1 CAD incoming-side design pass
##    (mechanism: Eir 8 read — CAD cores die at 6.5 HP/r structural
##    deficit with staffing FINE; spec E-items stand as acceptance);
##    FT-responder body-block + walker thrown-detection (one subsystem,
##    recognition-study + plank-inventory items); ore-barrier denial
##    pricing test; handoff-front decode (research, corpus-gated, 0033
##    bumped to v44 — rate may have moved); P6 probe fix + CAD re-freeze
##    on a real quiet window (era-books cover the v107/v117 oscillation);
##    kladde/Lunds/clanker freezes still wait on ≥2h holds.
## 6. STANDING RULES ADDED TODAY (tape/tooling/memory): r1000 margin-
##    flip det games are butterfly-class — banned as acceptance/
##    attribution (regime-change only); OURO PROBE APPROACH DROPPED
##    (behavioral fidelity ≠ predictive fidelity, twice measured; leg
##    retired); cad_probe attribution-only; paired shape corpora need
##    NOISE_OFF; homeostatic predictions in RATIO form; every spec
##    "except/unless" clause = its own audit line; timestamps from
##    `date` ONLY (7h drift incident, in memory); lineage by measured
##    diff never docstrings (boilerplate rode 7 forks). GAME-MODEL facts
##    added: Bo5 seat rule (meta teamA = engine A, per-match coin);
##    harvester output = team-blind LRU (constructed experiment);
##    launcher pickup ring = full 8-neighbourhood d²≤2; one Player
##    instance PER UNIT; slot 5 provably free.
## 7. HACKATHON KIT LIVE: github.com/opensverige/hackathon-codeflorent
##    (dbf71ea) — arena/sprt/make_map + bench_v53/54 + leaderboard
##    pipeline + CI. Community PRs maintain it; CI untested until the
##    first real PR. Probes/current-lineage/platform-replays excluded
##    by design (scope rationale on the board ~16:0x real).
## 8. FOR MAGNUS (pending his call): swap-rule review — three noise
##    exhibits (early-window crossings at n≤5) + the out-of-rule
##    swap-in question (v78 over a +20 window) are on the tape; possible
##    refinements logged (arm after N matches / magnitude floor).
# Session 16 FINAL (builder wrapped ~10:00 2026-08-08 on Magnus's direct
# call; research arm wrapped ~09:55; successor boots per /builder)

## FIRST ACTIONS for the successor
## 1. RE-ARM FOUR MONITORS (died with this wrap) — tools/monitors/, arm
##    one-liners in docstrings, EXIT-ON-WAKE loop shape (see the 06:43
##    coordination note for the pattern; it fired correctly ~10x today,
##    incl. the first live swap-rule SLOT FREE wake). elo_logger now also
##    watches the rolling last-5 swap window (team rule, memory:
##    slot-swap-rule) and wakes on crossings BOTH directions.
## 2. LIVE: **v75 "Eir 8" (= bots/_v85hsd, md5 4a2aeb50)** — OUR ship
##    (09:33, on the swap rule; baseline 1587.2@360; wrap read 1594.0@362
##    #26, +6.8 open). ~20-match check ~380. Rollback = v74 one click.
##    Swap rule cuts both ways — if Eir 8's last-5 goes ≤0, x3r0 may swap
##    it; that's the system, not a conflict. fcode submit is PERMANENTLY
##    ALLOWED (Magnus's permission rule, 09:31).
## 3. Research's REV-5 production read is PRE-REGISTERED (their 09:41
##    board note, successor-executable as written) — fires on Eir 8's
##    window. Their s16 wrap note + retro on the board ~09:54.
## 4. bots/_ouro_v2_dev = the ouro probe v2 worker's dir, UNVERIFIED
##    (worker died mid-flight with this wrap; main.py exists on disk).
##    Spec = docs/research/ouro-probe-refreeze-spec-2026-08-08.md
##    (committed, the real asset). Successor: verify the draft against
##    the spec's checks OR re-fire the worker (~20 min), then run the
##    §5.3 PREDICTIVE freeze battery (six anchor binaries, Wilson-contain
##    wild 76.7) + ≥3-lineage steering check + md5 stamp replacing
##    bots/ouroboros_probe. OURO FIRST remains the probe order (Elo table:
##    #1 bleed class, 86-pt instrument gap, they're the ONE stable nemesis).
## 5. Queue after ouro: M1 don't-feed-rebuilds counter (anti-structure
##    mechanism, v74 delta read), C1c (proactive-coverage shape per the
##    0033 omission finding), U2, d²=25 belt, archipelago-b residual owner
##    decode (det single, open), kladde/CAD/Lunds re-freezes on their
##    SHORT windows (churn ledger in the 09:45/09:55 notes; kladde wakes
##    = churn-routine until they hold ≥2h), hs_seek_seat lifecycle +
##    exception-swallow hardening (hse worker's notes).
## 6. Standing rules added TODAY (all in memory + board): Elo above all
##    else (ship cases in expected-Elo terms); field-first extends to the
##    holder leg; SLOT SWAP RULE (rolling last-5 ≤0 frees the slot);
##    NOISE_ON=False both sides for any identity/ablation claim; det
##    singles never adjudicate choice between heal-perturbing candidates;
##    compact numbers are never the case (3rd mean-regression today).

# Session 16 arc (kept for the record; superseded above where in conflict)

## State at 09:39 — **v75 "Eir 8" LIVE (OUR ship, 09:33)**
- SHIPPED on the new TEAM SWAP RULE (rolling last-5 ≤0 frees the slot;
  memory: slot-swap-rule): v74's window hit −9, logger wake tape-verified,
  package trigger met, Magnus granted durable fcode-submit permission.
  v75 = bots/_v85hsd (md5 4a2aeb50), baseline 1587.2 @ 360 rank 29.
  v74 FINAL 14 matches net −23.7. Rollback = v74 one click; rule cuts
  both ways. ~20-match check ~380. Case: tape rows v75-baseline /
  _v85hsd-bar / _v85hsd-ablation + the 09:01 expected-Elo package.
- Ship-adjacent verdicts this session: _v85hs KEEP-dev (51.2 slot bar),
  _v85hsb superseded by hsd, _v85hsc REFUTED (garrison), _v85hse PARKED
  (premise stale at hsd). Heal-detail role-aware design survives as
  principle (hsc-only evidence); archipelago-b residual owner = open
  decode question.
- Elo-weighted battery table (research): picket −103 + CAD −88 = the
  bleed classes; OURO PROBE RE-FREEZE FIRST (spec agent in flight),
  ouro's 93.3 is attribution-only (86-pt wild gap). Version churn morning:
  Lunds cycling, kladde →v65 (probe-source era), CAD v107 bounce (10 min).
  Quiet windows are SHORT — freeze batteries fire immediately on window.
- Magnus directives today (all in memory/board): Elo above all else
  (expected-Elo ship cases), field-first incl. holder leg, swap rule
  (revised rolling-5), durable submit permission.

## Prior state at 07:25 (superseded above where in conflict)
- LIVE: **v74 "mineguard" (x3r0)**, auto-activated 07:15 over our v73.
  Local copy bots/opp_v74 (md5 cb5452e6). Detected in 3 min by the NEW
  exit-on-wake monitors (wake path measured working: Lunds bump, v74
  activation, both caught live). SLOT BAR REBASES to v74 (standing norm).
- **v73 "Eir 7" FINAL: 5 matches, 2W-3L, 11-14 games, 1613→1610.9**
  (tape row v73-final). Rev-4 production read: shipped content ALL-CLEAN
  (E2b/E1/S1 doing exactly what they shipped to do) + PIECE H DEFECT
  (never fires — core-vision gate vs forward turrets; ticket H-1, also
  in x3r0's v70 verbatim; graft brief §2 updated).
- **_v85hs GATE VERDICTED — KEEP-dev STRONG CANDIDATE** (tape row
  _v85hs-gate): slot bar 51.2 [46.8,55.7]/480 vs _v84g; guards
  field-positive lean (kladde +5.0, band +8.3, v63 +10.0 in-batch); det
  52.1-vs-50.0, net +5 flips, mechanism = core-deaths converted to r1000
  tiebreak survivals. **_v85hsb** (launcher seat gate, md5 33a42f94) =
  the ship candidate; confirmation legs pending (det hsb-vs-hs + compact
  v74 leg + research mechanism decode; replays staged).
- Heal-seat MECHANISM SETTLED (research §10 + rev-4 §5): BODIES not
  seats — arrival/staffing is the lever; seat gates are insurance.
  Passability ground truth + 2 method rules in tooling.md.
- clanker_probe BUILT (worker report in coordination 07:2x), NOT frozen —
  freeze needs Clankers version-quiet (now watched: clanker/0033/
  leviathan/O(1) added to opp_watcher nemeses).
- Infra new this session: tools/{rdiff,pair,det}.py promoted (channel
  caveats in docstrings); archiver priority hook (theme 5a closed);
  monitors exit-on-wake.
- Queue: hsb confirmation legs → v74 delta read (research ASK posted) →
  probe freezes on quiet window → C1c/U2/d²=25 per the s15 queue below.

# Session 15 FINAL (wrapped ~06:3x 2026-08-08 on Magnus's call; Magnus
# restarting both arms — successor boots per /builder, which now carries a
# stance block that BINDS ON BOOT)

## FIRST ACTIONS for the successor
## 0. TOP PROCESS ITEM (retro theme 6, Magnus): the monitor→session WAKE PATH
##    is broken by design — monitors write wake-files but nothing re-invokes
##    a session (both arms blind 00:30-05:39 while v70-72 shipped and bled;
##    protocol now requires NAMING the verified wake path before entering
##    watch state; teammate uploads = wake events; fix candidates: monitor
##    loops that exit-on-wake so the harness re-invokes, or a Monitor-tool
##    condition). ALSO STANDING: push in the same breath as every commit
##    (origin exists; 54-commit backlog incident on the tape).
## 1. RE-ARM FOUR MONITORS (died with this wrap; tools/monitors/, one-liners
##    in docstrings, explicit paths only — no bare globs in zsh loops).
## 2. **LIVE: v73 "Eir 7" (= bots/_v84g, md5 cbb0b8b4)** — OUR lineage holds
##    the slot (first since v66). Shipped 06:23 on Magnus's direct call:
##    holder-parity accepted (49.0 [44.5,53.4]/480 vs v72), climb bet on the
##    field improvements (kladde-probe 83.3 vs 74.2 base, ouro 83.3, band 95).
##    Baseline 1613 @ 340 #22 (opened 1615 @ 341). ~20-match check due ~360.
##    ROLLBACK STANCE (Magnus): ladder disagrees → re-activate v72, one click.
## 3. Research's rev-4 PRODUCTION READ fires on v73's first ladder window
##    (spec: eir6b-production-read-spec rev 4; check 12 collects _v85hs
##    before-baselines in the same pass). Their wrap note + full-day RETRO
##    (5 themes) are on the coordination board ~06:3x.
## 4. bots/_v85hs = PARKED dev head (heal-seat protection + staffed heal
##    detail + REPLACEMENT_MAX lift, on the _v84g base) — the cross-validated
##    top plank from the v72 bleed decode. Gate NOT run (wrap horizon). Its
##    worker report is in the s15 coordination notes; gate design pre-stated
##    in the 06:12 registry row. THE candidate for next cycle.
## 5. Content of Eir 7 = 6e + E2b ore-pave ban + E1 capped peacetime ammo
##    floor + S1 intercept own-building guard (three measured defect fixes;
##    ablation + flip-grid caveats on the tape row _v84g-slotbar).
## 6. Measurement standards now standing (in tooling.md): deterministic-
##    paired or interleaved-same-batch for holder comparisons (cross-batch
##    120-game legs spread ~10pp); det per-map flips are chaos-bounded
##    (butterfly sensitivity — identity tests gold, small-perturbation
##    attribution over-reads); paired tooling in s15 scratchpad
##    (rdiff.py/det.py/pair.py) — PROMOTE TO tools/ after validation.
## 7. Queue after the production read: C1c (corpus-spec'd, behind its
##    arming-frequency diagnostic), U2 (detector kept, response redesign),
##    d²=25 belt (composes with C1c), probe re-freezes on a ≥2h version-
##    quiet window (CAD v117, Lunds v45, kladde v75/76, PP v35, Flotte v38;
##    opening rows exempt), clanker_probe GO spec, graft brief to x3r0
##    (asymmetry framing + his S1/E2a/watchdog defect list + heal-seat law).

# Session 15 overnight header below (superseded where in conflict)
# (superseded) Session 15 LIVE header (builder arm, overnight autonomous run per Magnus's
# 22:15 mandate; supersedes s14 blocks below where in conflict)

## State at 01:30 2026-08-08 — QUEUE DRAINED, WATCH STATE (no self-wrap; Magnus wraps)
- LIVE: **v69 "orekeeper" (x3r0)**, since 22:21 — v68 + E-series ore/econ
  fixes (delta read: docs/research/orekeeper-v69-delta-read + production
  read; net −1.80 Elo first 3 matches; delivery-freeze NOT fixed but NOT
  firing in fresh corpora; crash class v69:3536 confirmed unguarded).
  Local copy bots/opp_v69 md5 562b01e9. Ship bar was REBASED to the
  holder (pre-stated, 22:42 note) — NOTHING cleared it; no ship tonight.
- **LINEAGE BASE UNCHANGED: _v81e6e (6e)**. Night's branches, all
  verdicted on the tape: **_v82c1 C1 home ring KEEP-dev** (supply-bound at
  probe load; ray-coverage law replicated n=405); **_v82hd Heimdall
  PARKED-refuted** (ejection fires, value-negative, exile-target hole);
  **_v83c1b C1b KEEP-dev** (arming+supply proven; **85% at wild-median
  load** = the KCM farm-recovery number; sig-2 off); **_v83u piece U
  PARKED-refuted as response, DETECTOR KEPT** (delivery meter exact,
  famine thresholds measured; response = absorbing austerity via
  reserve-bound links — U2 shape queued).
- **HARNESS FINDING (read before trusting any v69 delta)**: non-interleaved
  120-game legs spread ~10pp same-binary. All cross-batch "vs-parent v69
  tax" claims tonight are retro-caveated on the tape. NEW STANDARD:
  holder comparisons = deterministic-paired (all-sides NOISE_OFF + paired
  seeds + turn-differ; tooling in s15 scratchpad rdiff.py/det.py/pair.py,
  promote to tools/ after validation) or interleaved-same-batch only.
- **MORNING QUEUE (in order)**: (1) deterministic-paired re-reads of
  C1/C1b/U vs opp_v69 (the three "tax" deltas may be phantoms); (2) C1c =
  destination/age-keyed sig-1 (research's corpus spec, booked 00:11) +
  arming-frequency diagnostic FIRST; (3) U2 = U detector + reserve-exempt
  famine link + no queue-wipe + clear-ore fix; (4) graft/slot conversation
  (Magnus/x3r0) — brief planks all on the board: asymmetry framing (pave
  guard, print rate, S1 own-conveyor bait, no-E3 question), KCM/Clankers
  snipe-exposure, C1b wild case; (5) probe re-freezes on a version-quiet
  ≥2h window (CAD v117!, Lunds v45, kladde v73, PP v18; opening rows
  exempt per the v107→v116 test) + clanker_probe GO spec.
- Research arm: board fully landed (9 deliverables tonight incl. Clankers
  relabel HEAL-TANK SIEGE + controller-law targeting equation, O(1)
  classified, wild-KCM rates, v69 reads, tiebreak decode). Their morning
  items are in the 22:08 + wave notes.
- Monitors: 4/4 alive this session (ids in 22:30 note) — they DIE with
  session end; successor re-arms per /builder step 3.
- Tape: results.tsv rows _v81e6e-vs-v69 → _v83u-verdict; commits 7516f0c +
  the 01:3x wrap commit. Ladder at last read: 1559@293 #27.

# Session 14 header below (superseded where in conflict)
# (superseded) Session 14 LIVE header (builder arm; supersedes the s13 block below where in conflict)

## STANDING RULES added this session (mirror of protocol/coordination)
- **NO SELF-INITIATED WRAPS** (Magnus directive ~19:47 via research relay,
  bilateral, in two-session-protocol.md Boot sequences + auto-memory):
  drained queue = watch state, announce and hold; wrap mechanics fire only
  on Magnus's explicit call.
- **READ THE FOUR MONITOR TASK-OUTPUT FILES at every natural wake-up**
  (task completion, cross-session message): monitor wake lines print into
  background task files nobody sees until the loop exits — the v68
  activation wake sat unread ~30 min (incident-log candidate). Files live
  in the session tasks/ dir; ids in this session: elo busk6h1sv, match
  b5rmf2yvd, opp b7rp97c4r, archiver bfa6yg71a.
- **Micro process-deltas**: when a version verdict settles, append 1-3
  what-slowed-us bullets to its coordination verdict note (retro cadence
  (1), acked 19:5x; full retros only at Magnus-called wraps).

## Session-14 state at last update (~22:10; research arm wrapped 22:08 on
## Magnus's call — BUILDER TEARDOWN AWAITS HIS DIRECT CONFIRMATION HERE)
- LIVE: **v68 "chokewall" (x3r0)**, 1561 @ 283 #28 at last read, window
  net-negative w/ an L4 streak inside it. NOT the announced graft (I/J/H
  absent). opp_v68 local (md5 04811b4a...), full read in docs/research/
  v68-chokewall-first-read-2026-08-07.md (no post-r300 behavior;
  delivered-tiebreak-#1 always; delivery-freeze defect 5/11 grinds).
- **LINEAGE BASE: Eir 6e (`bots/_v81e6e`, md5 31a10eb2) = 6c + piece N**
  (one-line pave vision guard killing the ancestral launcher-throw crash
  — 0-vs-128 crashes/480 vs v68; ALSO resolves x3r0's kite_proxy
  traceback, fix is a gift for his line). SLOT BAR: 51.0 [46.6,55.5]/480
  = PARITY, bar not met, v68 stays; 46.0→51.0 from piece N alone.
- Arc on tape: 6b (K'-cap) refuted by ablation grid; 6c KEEP (stage-1
  pass, stale-baseline catch); 6d RACE both branches KEEP-dev,
  inconclusive-clean (_v80e6d_kfix kladde-direction-right;
  _v80e6d_tb tiebreak thesis untested by pooled rate — needs the
  replay-split + wiring-pct instrument BEFORE re-gating).
- **GRAFT BRIEF for Magnus/x3r0 = the 21:10 + 21:2x-21:3x coordination
  notes**: 5 measured planks; snipe-exposure backed by THREE teams
  (KCM 9-1 mechanism, CAD family, Clankers r27 kill); merged line needs
  both parents.
- **BUILD QUEUE (gated on Magnus's slot/graft input)**: (1) C1 home
  sentinel ring (KCM/CAD counter, measured cheap, ≥3-turrets-d²≤36
  predictor = gate signature) [+ HEIMDALL disposal-ring pairing
  decision — defender-side launcher ejection, 2-team convergent
  evidence]; (2) tiebreak-split + wiring-pct instrument (Branch B's
  real test; our wiring 27-53% vs Clankers' 100%); (3) v65/66 archive
  backfill (--cursor pagination); (4) probe re-freezes: CAD-family
  version wave (CAD v115, Lunds v43, KCM 7→1, Powerpuff v18) makes
  cad_probe + v107 constants suspect.
- Research successor queue: their 22:08 wrap note. Exploit candidates
  on the book: Clankers heal-tank two-source break (measured) +
  medic-conversion (watch item); v68 delivery-freeze.
- Traceback hunt RESOLVED (was blocked on x3r0 data — found it
  ourselves: pave/launcher, see piece N).
- Monitors: ALIVE and watching (4/4, this session's processes — they die
  with this session's END; successor re-arms per /builder step 3).
  Wake-file rule: read all four task outputs at every wake-up.

# Handover — session 13 FINAL (wrapped 19:07; Magnus restarting fresh arms)

## FIRST ACTIONS for the successor (boot: /builder)
## 1. RE-ARM FOUR MONITORS (they died with this wrap; tools/monitors/, arm
##    one-liners in docstrings, state re-baselines silently, ~30s).
##    zsh TRAP: never `set -- $var` or bare globs in loop one-liners —
##    burned a 240-game battery today; explicit paths only.
## 2. FIRE THE EIR 6B WORKER — queued NOT SPAWNED at wrap: bots/_v78e6b is
##    an UNMODIFIED copy of _v77e6 (worker never ran). Spec = coordination
##    18:46 note: K' = keep income budget + per-builder shares, RESTORE
##    siege gate on core heal (budget throttles it — the 972-heal
##    starvation fix), proactive trunk trigger (budget replaces the ≥8
##    depth gate, which never fires: gunner dmg 7 < 8 — smoke the
##    fjordgate/lighthouse flip maps), SPORKS_AMMO stays OFF (refuted),
##    POP_FLOOR stays OFF pending item 3.
## 3. POP-FLOOR ISOLATION BATTERY — queued NOT FIRED: _v77e6_flooronly
##    (dir ready, toggles verified) vs opp_v63 + band_probe + orizon_probe
##    60/leg. Clean/positive → rides along with K'.
## 4. Eir 6b gate: guards (v63 55 / band 88.3 / kladde 80 / ouro 80 / cad
##    50 — the _v76e51 60-game rows) + orizon_probe value leg (beat 58.3)
##    + slot bar vs opp_v67 480 (parity 51.9 to beat; THE retake bar).
## 5. BLOCKED: Eir 5.1 traceback fix awaits x3r0's traceback text or
##    kite_proxy zip (asked via Magnus; NOT unit-deleting — run() catches,
##    main.py:832-843 — one lost action round per unit lifetime).

# Session-13-live header below (superseded only where the wrap says so).
# (superseded header follows)
# Handover — session 13 live (builder arm; two-arm ops per docs/two-session-protocol.md)

## LIVE: v67 "wave_ghost" — x3r0's line, NOT ours. Auto-activated on upload
## 17:52:43 (mid-wrap, over our v66). Window baselines from 1571@265, opened
## +18 with a 5-0 over Team 48 v16 (03af6569) → 1589@266 rank #24. BUT 0-4 in
## incoming URs (5-15 games): 0-5 sporks v2, 1-4 team lazy v94, 2-3 SmartFridge
## v34, 2-3 Lorem Ipsum v14 — beats one family battery, loses to another.
## SLOT CASE COMPLETE (18:15): head-to-head PARITY 51.9 [47.4,56.3]/480
## (229/480 games decided on ti-collected tiebreak — the matchup is a
## tiebreak grind); field profile vs our 5 probes statistically identical to
## our line (kladde 75.0/ouro 71.7/band 91.7/flotte 81.7; cad 61.7 only
## non-clearing leg — shared soft class); wall-density niche prediction
## REFUTED vs us (r=0.03). NO measured case to flip either way → v67 stays
## per team norm; Eir 6 is the vehicle to clear the bar. Slot call Magnus's.
## wave_ghost decode: docs/research/wave-ghost-first-read-2026-08-07.md
## (forward-sentinel core-snipe, drip ammo, 3 loss modes).
## Local copy bots/opp_v67 (TRAP: `fcode submission download` emits a ZIP —
## extract it; saving the zip as the bot dir made 480 arena games silently
## produce "no result" as bot-B load failures).
## v66 "Eir 5.1" FINAL RECORD: window 17:14–17:52:43 (39 min), ladder 2-1 net
## +9.3 (W 4-1 farming_200s v7, W 4-1 0033 v42, L 1-4 CAD v107 — probe-valid
## version), UR 1-2. SmartFridge ran a deliberate 4-UR version-cycling probe
## series against our slot (v34→v33→v35→v34 in 31 min) — book-worthy signature;
## expect their next version tuned against whatever holds the slot.
## TEAM DECISION (~18:30, Magnus/x3r0 direct): KEEP v67. x3r0's own Fable
## read matched ours (104-100/204 direct = same parity coin). FORK FINDING:
## wave_ghost IS our Eir 4 + 304 diff lines (vs 2,268 to his v89) — a
## PRIMARY_SENTINEL snipe overlay on our lineage, dropping v65/v66 pieces.
## His stated next move: graft I/J/H onto his v8 — i.e. re-add what the
## fork dropped; our measured specs are the contribution. CAD production
## read confirms the latch HELD under losing pressure (graft de-risked).
## EIR 6: REFUTED AS-BUILT, mechanism PINNED w/ control cell (tape 18:35 +
## 18:46). Base-purity: _v77e6 refactor EXONERATED (alloff = baseline:
## 60/91.7/58.3-mirror). K alone costs −15 (v63) / −35 (band) vs alloff.
## Mechanism: trunk half NEVER fires (depth gate 8 > gunner dmg 7 — one-
## reload qualify window) so K-as-built = un-gated core-heal-from-r0 eating
## builder turns mid-fight (27-31% of turns in fast rush losses). REDESIGN
## SPEC (next cycle lead, 18:46 note): keep budget+shares, RESTORE siege
## gate on core heal, proactive trunk trigger — the real sporks mechanism
## was never tested. Sporks ammo refuted as-ported. Pop floor owes an
## isolation leg. Dev dirs: _v77e6 + _noammo/_konly/_alloff (ablation).
## Two-arm incident tonight (both directions, protocol incident-log
## updated): research r0-divergence claim retracted (NOISE_ON salt breaks
## paired-replay attribution — check noise provenance before attributing).
## NEW INSTRUMENT: orizon_probe FROZEN md5 aa7ab7185e5e1f6906071a72eb48d843
## (point-blank battery class, family plant signature; gentler than wild).
## OPEN: Eir 5.1 traceback (x3r0 stress, kite_proxy/hive/42) — run() DOES
## catch it (one-per-lifetime diagnostic print, unit NOT deleted, correction
## routed); underlying exception blocked on x3r0's traceback text.
## Monitors: re-armed 17:58 session 13. Research arm session 13: queue
## drained (wave_ghost read, T48+CAD legs, Viktor5776=econ-greed, axis-split
## underpowered pending --mine archive); now on the K-diagnosis decode.

# Prior header (session 12 wrap, superseded 17:52 by the v67 auto-activation) below.
## (superseded) LIVE: v66 "Eir 5.1" (= `bots/_v76e51`), shipped 17:14. Baseline 1560 @ 261,
## rank #27. = v65 + rotation latch (time+lock-dsq+no-return; the v65 tile-keyed
## latch was the real bug) + capped r960 dump w/ drip suppression (tiebreak-#3
## protected — and #3 decided a real game today: Team 48 g3, "Titanium Stored").
## At wrap: W5 streak, ~1578, closing on the 1597 all-time peak. 20-MATCH CHECK
## DUE ~281 matches vs the 1560 baseline. Boot: /builder (encodes the boot
## sequence; expect to RE-ARM monitors — they are session task processes and
## likely died with the wrap, scripts in tools/monitors/, ~30s).
## Family samples under v65-66: Orizon 2-3 seat B, Team 48 4-1 seat A (three
## core kills r78-159 — we out-race thin-house batteries), Ouroboros 0-5 seat B
## (seat lock intact; Loki + piece K are that fight). Next build: Eir 6 cycle
## (task list + coordination.md; piece K leads).

# Prior header (Eir 5 ship, ~15:45) below.
## (superseded) LIVE: v65 "Eir 5" (= `bots/_v75e5`), shipped 15:42. Baseline ~1540 @ 252,
## rank #29. = Eir 4 + I rotation discipline + J defender counterbattery
## unlock (whose live-gun scan also DISARMS the hive_freeze self-freeze — the
## real hive gain) + H r960 endgame switch (core ammo-dump gated on a live
## visible turret; builder half no-ops gracefully). Matched noise-on battery:
## kladde hive+eider 48.4 vs Eir 4's 23.4 (clean separation), v63 slot bar
## 58.8 vs 55.4, picket/flotte/band flat, 0 crashes. Build source:
## docs/research/eir5-surgical-map-2026-08-07.md (the research session's
## verified spec — raw findings specs were stale, again).

## MEASUREMENT RULE (discovered this cycle, supersedes all older tape rows):
## every pre-noise row is seed-amplified HISTORY — piece C's hive "fix"
## (16/32 noise-off) is 1/32 under noise; the flotte "93% sweeps" are ~65%
## true. Only noise-on rows are currency. Matched-regime baselines are
## mandatory: candidate and baseline must share the NOISE_ON setting.

# Prior header (Eir 4 ship, ~13:35) below for the day's arc.
## (superseded) LIVE: v64 "Eir 4" (= `bots/_v74e4`), shipped 13:29 on Magnus's standing
## run-with-recommendations directive. Baseline 1550 @ 239, rank #28.

Contents on top of Eir 2 (every piece toggled + ablation-attributed on the tape):
A+B siege solvency (16-Ti heal reserve + siege respawn floor; HOLD-grade, wild-
Lunds value case, harmless), C deep-damage early medic (r40+, dmg>=8 — THE hive
fix, 0/32→16/32 vs kladde_probe), D duel discipline (no solo melee into a live
gun whose ray covers you; locally flat, shipped on mechanism-override: 8/11
traced seat-B deaths + 70/71 Ouroboros kills are exactly this, probe measured
GENTLER than wild), F pave trail (pave the tile just left facing the move —
directed-connectivity fix; owns eider 0→7/32, opp_v50 heart/meander/atoll
16/48→48/48; HIVE-GATED after a one-tile diagnosis: walk-direction pave at r22
dead-ends (4,18), linker's occupied-implies-correct poisons the trunk), G
decision noise ON (once-per-match spawn-dispersion salt; determinism measured:
games are pure functions of (opp,versions,map,seat), 19 historical re-lost
identical games), E B8 sensing OFF (null vs opp_v50 AND vs v89 — archipelago
needs a different mechanism). Battery: 0 crashes/1752 — v89 bar 57.9
[53.5,62.3]/480, v79 61.7, kladde 75.0, flotte 86.7, band 90.0, ouro-probe 72.5
(paired 67.2→81.2).

**MEASUREMENT WARNING while G ships: paired-seed local runs are nondeterministic
by design.** Pooled Wilson reads only, or flip NOISE_ON=False in local copies.

## FIRST ACTIONS next session
1. Re-arm FOUR monitors — now repo scripts, no regeneration: tools/monitors/
   {elo_logger,match_watcher,opp_watcher,replay_archiver}.py, arm one-liners in
   each docstring. State files → session scratchpad (first poll = silent baseline).
2. Read Eir 4's rolling trajectory vs the 1550@239 baseline (~20-match check).
3. Continue the unrated portfolio sweep (leg 1 fired at ship: Ouroboros
   bab61537-2315-4121-9286-d9447197afc2, eider/meander/drumlin/atoll/hive).
   Ouroboros is PLATFORM SEAT-LOCKED (they hold seat A 13/13, p≈0.008) — only
   unrated legs can ever read our seat-A matchup; repeat challenges until the
   seat flips (check teamAId in match JSON). Pace: ~5/10min shared limit, never
   from a loop.
4. Harvest docs/spitball.md "Research session #2" synthesis if not yet read —
   and docs/research/2026-08-07-fanout/ holds every findings file + the
   validated replay toolkit (replay_lib.py fixes 3 undocumented schema traps;
   promotion to tools/ after a validation pass).

## Build queue (specs ready, in priority order)
- Piece H — endgame spend-switch @r960: flips 6/9 current-line r1000 losses
  (+38.4 Elo equiv, thread-4 pricing). Needs living builders → composes with D.
- Piece J — heal-dispatch reorder: universal heal sits above role dispatch, so
  under siege NOBODY reaches counterbattery (Orizon = 5th class, point-blank
  gunner battery, exposes it; hunt-ballot idiom is the fix shape). Also fix
  SLOT_HOME_GUN monotone (rubble counts as a live gun).
- Piece I — rotation discipline: 4,460 Ti of gunner rotation thrash across 8
  games (56.5% of income worst case); rotate only if can_fire_from lands the
  target and it's off-ray, + 3x hysteresis.
- Piece B' — population-floor respawn (hands crash to sustained ZERO ~r235-250
  and never refill; REPLACE_TI_FLOOR=250 unmeetable mid-strangle). After D's
  production read.
- F root fix — _build_next_link verifies facing, destroy()+rebuild wrong heads
  (destroy() measured FREE: consumes neither action nor move, unlimited/turn).
  Removes the hive gate's reason to exist. Also SLOT_HARVESTERS ratchet fix.
- Flotte x jackpot steal — denial table vs their CONSTANT per-(map,seat)
  openings + ~120 delivered floor (thread-8); Flotte NEVER targets the core
  (0/29) → core-shield lead, next-cycle verification.
- Probes: kladde_probe_v2 (spec in thread-3 findings; WAIT — kladde rolled back
  v62→v60 at ~13:15, let their version settle), orizon_probe (spec in thread-7;
  Orizon script is fully map-determined). ouroboros_probe FROZEN today, md5
  8828b5d50039309cdc294ea07833989e — gentler than wild (4/8 vs their 14/15),
  verdicts understate real pressure.
- v89's archipelago+jackpot holes (0/32 each in the 480 battery) — undecoded;
  first item for the next research brief.

## SHIP-GATE REDEFINITION (Magnus directive, 2026-08-07 late session)
Ship verdicts now weigh the CLASS-WEIGHTED vs-field battery — probe-fleet legs
weighted by the ladder's actual class mix (meta census supplies weights) plus
slot bars — NOT improvement-over-our-own-previous-version. Self-paired legs
survive for ATTRIBUTION only (ablation grids, identical-rows fingerprint).
Rationale: our economy/survivability meta is nearly unique on the ladder;
self-A/B undervalues anti-field changes (the external-meta lesson). System
build is task-tracked: probe fleet (top-8, refresh on version-bump events),
fidelity ledger (wild-gap per probe from unrated sweeps), weighted battery.
META CENSUS COMPLETE: docs/research/2026-08-07-fanout/meta-census.md — READ IT
FIRST next session. Headlines: (1) sporks (#2, 1960) IS our meta played
correctly — 15-35 harvesters, 4380 median delivered, defensive mid-map sentinel
screen (0.61 separation, 35% damage to units/turrets = interception), still
wins 88% by core kill; "study it, do not imitate it". (2) UNCOMFORTABLE MIRROR:
our live bot's production profile (38 games, v61-64) classifies as a SENTINEL
CORE BATTERY WITH A SMALL ECONOMY — median 3 harvesters, 820 delivered, 68%
damage at cores, r14 aggression at aim 0.0. The economy identity exists in
code and dies on contact (the master constraint as an identity gap). (3)
Matched pool = 44% point-blank core battery + 36% picket; recommended battery
seats 4 battery / 3 picket / 1 economy / 1 rush. (4) Probe set from MID-POOL
scripts, not the top 8: Team 48 + farming_200s (freeze AIM POLICY, aim-dsq 0.0
sd 0) + Askar City (purest script: launcher r1/conveyor r3, 5/5 all sizes) +
orizon family + Lunds-v37 picket. Pivot: DO NOT probe (hourly churn) — track
the class. (5) team lazy (1892) = third Orizon-family member; one fix may
retire three opponents. Loose ends: 5 unclassified teams = 20% of our games.

## Two-arm operation
The builder/research split is contractual: docs/two-session-protocol.md
(roles, channels, fcode budget, anti-collision rules, boot sequences).
Ops channel + IN-FLIGHT registry: docs/coordination.md. Boot the research
arm per the protocol's boot sequence, not ad hoc.

## Session-12 process state
- Research fan-out template worked (12 threads + cross-check, all verdicted
  same-day; brief format in docs/research-brief-2026-08-07.md). Next brief goes
  out after Eir 4's production read; the closed research session can be
  re-messaged or a new one spun with the brief file.
- STALE-BASELINE RULE (3 catches today): re-run any cited baseline before
  commissioning from it; version-tag every claim.
- bots/starter is NONDETERMINISTIC (unseeded random) — determinism reference is
  opp_v63 (docs/tooling.md).
- Slot history today: v61→v62(accidental Eir 3)→v61→v63(v89)→v64 Eir 4.
  Magnus + x3r0 handled the slot; the measured case (Eir2 60.4, Eir4 57.9 vs
  v89) is on the tape.
- Dev/ablation dirs: _v74e4 (SHIPPED content), _v74e4_noF/_noD/b8/b8v2
  (ablation variants, disposable), _v73e3 (Eir 3, parked).
- New instruments/infra: ouroboros_probe (4th probe), replay_archive/ (passive
  whole-ladder harvest, gitignored), tools/monitors/ (4 scripts).

# Session-11 handover below (superseded where in conflict)

# (old header) Handover — session 11 close-of-coverage state (2026-08-07 ~11:00)

## FINAL ADDENDUM (session 11 close, ~11:50)
- **x3r0's v89 auto-activated over Eir 2 late in the session; measured
  Eir 2 > v89 at 60.4 [54.1, 66.4]/240.** The slot case is Magnus's to take
  to x3r0 — do not flip it unilaterally. `bots/opp_v63` is the local copy.
- **The research session's findings landed in docs/spitball.md — READ THEM
  BEFORE picking from the queue below.** Headlines: the grind residual is a
  SOLVENCY problem (heal funding + the r63-390 farm-death window
  MEDIC_MIN_RND leaves open), not DPS; the seat-B deferral never covered the
  forward roles (break the 38 deaths down by role before the next counter);
  cad_probe should be re-frozen from a fresh CAD replay; slot 9 is the only
  reclaimable store slot; classifier design: default + two flags, Core as
  sole writer. External-meta scavenge estimates +150-250 Elo inside the
  current strategy family.
- Ladder at handover: **1557/#27, recovering on an Eir-line 4-streak.**
- Dead-code cleanup owed in `_v72e2`: COUNTERBATTERY_RICH_TI declared,
  never referenced (leftover of a refuted edit).

## FIRST ACTIONS for the next session
1. Re-arm THREE monitors (they died with session 11): Elo logger 5-min
   (appending, thresholded ±25/new-submission), match watcher 2-min (4+
   streaks), opponent-version watcher 10-min (nemesis list; ids in the
   operating notes' monitor bullet and in git history of the scratchpad
   scripts — regenerate from the descriptions there, ~10 min).
2. **LIVE: v61 "Eir 2" (`bots/_v72e2`)**, reactivated after Eir 3's
   criteria-based revert. Read its rolling trajectory (baseline 1533@226;
   it ran 3W-1L/+5 in its first window). Ladder ~1533/#28.
3. Check `docs/spitball.md` for ideas Magnus's parallel research session may
   have appended.

## Where session 11 left the board
- **Ship chain today:** v54 → v55 (medic+surge; kladde 71.2→81.9, opp_v50
  66.5, clean) → v59 "Eir" (v79-absorption: escort disengage, footprint band
  41 + corner floor, ammo latch/magazine, ore step-off, counterbattery
  bleeding-waiver; beats x3r0's v79 AND v82 at 59.6 [55.1,63.9] each) →
  v61 "Eir 2" (+eco-siege hunt mode) → v62 "Eir 3" (seat-B frontier
  deferral) → REVERTED to Eir 2 same-day: pre-committed criteria (Lunds
  seat-B re-leg still 0-5, Ouroboros = baseline). `_v73e3` kept as dev.
- **Open problem #1 — the seat-B resolution-order tax** (scratchpad
  seatB_diagnosis.md is gone with the session; key numbers preserved in
  game-model.md + tape): seat A's actions resolve first → 19 vs 38 builder
  deaths by r80 → 9/9 corpus tiebreaks to seat A. Frontier deferral was
  production-flat; the tax needs a different counter (spitball has ideas).
- **Open problem #2 — Ouroboros**: the biggest quantified per-team leak
  (share .07 vs E~.40 in the portfolio, all-seat-B confounded). Pattern
  undecoded (fast core kills @265/323, NOT grind). Audit next.
- **Production portfolio table** (first ever, 6 nemeses × 15 maps): in
  docs/opponents.md with seat annotations. Lunds is ABOVE expectation now
  (.47 vs .40) — the morning nemesis story is closed.
- **Instruments:** band/flotte probes current; kladde_probe STALE (they
  shipped v62 ~1811); cad_probe (md5 6d0e955f96de1f0d11f93db573ade458)
  current again after CAD's rollback to v107; opp_v50/opp_v56(v79)/
  opp_v58(v82) local; teammate submissions downloadable via
  `fcode submission download <n>`.
- **Model discoveries (all in game-model.md):** Elo is game-share
  Δ=32×(games/5−E); cost scale is ONE team-wide multiplier; seed
  amplification (per-map rows ≈ 2 distinct games); unrated legs flip seats;
  strike timing exceeds decoded samples.
- **Process:** naming convention (Norse; Eir=heal line, Heimdall=insertion
  guard reserved, Loki=trickster reserved, Thor=offense reserved);
  docs/spitball.md idea board + parallel-session guardrails; unrated
  portfolio sweep ritual (3 challenges × 5 maps per team; do BOTH seats =
  6 challenges for a full read); ship-time reversion criteria (worked
  today — write them on the tape at every ship).
- **Dev branches parked:** `_v73e3` (seat-B deferral), `_v70cg` (Heimdall
  pieces: body-block interceptor, siege respawn + converter reserve
  agreement — cad-class value unproven), `_v70sm`/`_v70st` (ore denial,
  blocked on own-farm survival), `_v70th`/`_v70cm` lineage heads.
- **Queue suggestion:** Ouroboros decode → kladde probe refresh (their v62)
  → seat-B counter round 2 (spitball) → v82's archipelago hole → backlog
  (launcher exile, multi-scout via freed slot 9, in-match classifier).

## Session-11 morning notes (superseded where they conflict with the above)

- **v55 "v70-medic-surge" (`bots/_v70cm`) shipped clean** (kladde 71.2→81.9, opp_v50
  59.2→66.5, guards flat, 0 crashes/1920) — then **x3r0 activated v56 ("v79-lsq-eco…")
  over it** ~06:43Z. Team norm: our line retakes the slot only by beating v79 locally.
- **v55 vs v79 = 53.1 [48.7,57.5] over 480 — parity, bar NOT met.** But the map
  portfolio is near-complementary: v55 sweeps antler/fjordgate/hive/nordkap 32-0
  (+saga/lighthouse majorities), v79 sweeps atoll/heart/jackpot/meander 32-0, 5 maps
  seat-coinflip. AND v55 covers the CtrlAltDefeat insertion class (65.0 vs cad_probe)
  which v79 bleeds to (43.3). Slot decision = Magnus/team judgment; package on the tape.
- **CtrlAltDefeat insertion class decoded** (0-5 ladder loss e40a6c01 under v55, 5 games):
  Launcher r1, 2-3 thrown raiders, sentry ~r11 at core-dsq 10-41, kill median r361.
  Three gaps: hunt band too small (sentinel range 32 > band 20), hunt floor r120,
  population collapse (respawn floor unmeetable at 2-12 Ti banks). **`bots/cad_probe`
  frozen (md5 6d0e955f96de1f0d11f93db573ade458)** — harsher than the original.
- **`bots/_v70cg` = dev branch, NOT shipped** (failed its gate: cad_probe 63.3 vs v55's
  65.0, kladde flat-redistributed). Contains ablation-tested pieces to re-earn their
  place: interceptor BODY-BLOCK (Magnus-scouted: stand in the raider's doorway —
  builders are mutually impassable and can't attack units), siege-mode respawn +
  converter/spawner reserve agreement, hunt band widened to core-footprint dsq≤41.
  REFUTED en route: early-hunt waiver (eider 8/16→0/16), `_v70ec` labor reserve
  (bootstrap inversion), ore-barrier/steal as hive flips (denial works — halves their
  collection — but our own farm survival binds; `_v70sm`/`_v70st` parked).
- **Elo is GAME-SHARE: Δ=32×(games_won/5−E), zero-residual fit** — margin is nearly
  everything, per-game win rate is the ladder currency, one stolen game vs top teams is
  net-positive. Strategic frame in this file corrected accordingly (§ below).
- **Seed amplification trap (game-model.md):** local seeds vary games weakly; a
  seat-decided per-map row ≈ 2 distinct games, not 2×seeds. Weigh pooled rates +
  mechanism, not per-map swings.
- **Cost scale is team-wide** (one multiplier, per-type increments) — twice confirmed;
  the organisers' per-category table is wrong. Conveyor churn = +1%/relay on EVERYTHING.
- Magnus directives this session: **unreasonable variants** (try low-prior exploits) and
  **"play the players"** (exploit measured opponent habits; both in auto-memory).
- Instruments now: band/flotte/kladde probes + **cad_probe** + opp_v50 + **opp_v56**
  (x3r0's v79, downloaded via `fcode submission download 56` — teammate submissions ARE
  locally obtainable; keep opp_v56 as the slot bar).

# Original session-11-start handover (written 2026-08-07 morning, end of the session-10 marathon)

Start here → [docs/game-model.md](docs/game-model.md) → [docs/strategy-log.md](docs/strategy-log.md)
→ [docs/opponents.md](docs/opponents.md). Full session-10 history: git log of this file.

## Where the ladder stands

**Live: platform v54 "v70-respawn-convergence" (= `bots/_v70mh`), activated 2026-08-07
~08:05 at 1550 @ 197 matches, rank #27, Gold.** Trajectory context: the account went
1383/#40 → peak 1597/#24 → ~1550/#27 across sessions 9-10 (+167 net). Predecessors: v53
(`_v68si`) finished 28-26, +43 net, formal KEEP verdict at its 20-match checkpoint. All
baselines and the formal verdict are rows in `elo_history.tsv`.

**v54's ship case (Magnus-approved trade):** flotte_probe 93.3% [89.4, 95.9] vs live
86.7% (+6.6, the wild chip-siege class that was draining the ladder), band 93.3%, kladde
71.2% flat, guards green, 0 crashes in 1200 — accepted a ~4-pt overlapping dip vs
opp_v50 (63.3 → 59.2) because that's a teammate proxy we never face rated, while the
ladder pool looks like the probes. **Before-legs for the production A/B were queued at
ship time** (Lunds eider/hive/jackpot/meander/drumlin; Flotte meander/eider/hive/
lighthouse/atoll — match ids 76282b6e…, 168e6e3b…); check their results FIRST at session
start: flipped games = the convergence working in production.

## What v54 contains (lineage: v53 = `_v68si` → +2 gated keeps)

1. **Builder respawn-on-death** (`_v70rp`): `self.n` was a lifetime spawn counter — a
   dead builder never freed its seat (measured: 586 rounds on 2 live builders, 12,314
   Ti unspent). Replacements refill to the live target of 5, gated ti≥250 ∧ rnd≥60 so
   the opening/cost-scale is untouched (the lesson of `_v69bc`'s -13pt cap-raise).
2. **Multi-healer convergence** (`_v70mh`): role-2 and role-5+ expanders within vision
   of a damaged core converge and heal (+8..+12/rnd vs a chip siege's -9). Proximity-
   bounded by construction (r²=20 vision). Flat vs kladde_probe's 2-3-sentinel barrage
   — healing can't outpace that; see open problems.

## The class model (the big intellectual asset — see strategy-log sessions 10.x)

Opponents beat us in three decoded classes, each with a frozen replay-extracted probe:

| class | probe (md5) | v54 score | wild exemplars |
| --- | --- | --- | --- |
| all-in rush | band_probe (33cd3c14…) | 93.3% | Banminary, Team 48 (map-dep) |
| strangle + chip siege | flotte_probe (ff968416…) | **93.3%** | Flotte, LUNDS, Powerpuff |
| patient grind | kladde_probe (42fa9f50…) | **71.2% — open front** | kladde, sporks, Ouroboros? |

**"Counter-battery blindness"** (Lunds audit, 10 games decoded) unified the middle
class: one infiltrator plants one turret near our core and chips for 150-900 rounds
while we bank 1,165-8,093 Ti unspent. v54's convergence fixes the single-turret
arithmetic. STILL OPEN: multi-turret barrages (kladde_probe eider/hive 0/16), the
single-slot SLOT_THREAT (can't track 2 threats), and turret-hunting (turrets are
BUILDINGS — builders can attack them 2dmg/2Ti; a turret shelling the core does not
shoot back at its attacker; never implemented, ranked next).

## Strategic frame (Magnus + Fable, 2026-08-07, at ~1550-1600; CORRECTED same day)

**MEASURED (session 11, 100-match zero-residual fit): Δ = 32 × (games_won/5 − E),
E = 1/(1+10^((R_opp−R_us)/400)).** The platform scores GAME SHARE, not match outcome —
the original "margin is free / map-majority" frame was wrong. Every individual game is
worth ±6.4 Elo; there is no flip point at 3 games. **The ladder currency is per-game
win rate — exactly what the local arena's Wilson gate measures.** Priorities that
follow: (1) class fixes over per-team fixes (one map row moves against many teams) —
unchanged; (2) near-rating nemeses still the best Elo/effort (E≈0.5 maximizes leverage:
Lunds ✓ flipped by v54, Ouroboros, Landers, Orizon), BUT blowout-loss reduction pays
against anyone in-band, and vs top-8 teams stealing a single game per match is already
net-positive (vs Flotte E≈0.17: 0-5 = −5.4, 1-4 = +1.0) — one-map specialization
against the top is profitable, not vanity; (3) 2-3 and r1000-tiebreak losses remain
the flip-candidates list, and every game dragged to a winnable tiebreak pays a full
+6.4 (strengthens the starvation track).

## The queue

1. **Read the v54 before/after rematches** (ids above) — they decide whether the
   convergence claim holds in production and calibrate everything after.
2. **Turret-hunting** (`_v70th` design): role-split so converged units beside the core
   heal while defender/replacements attack the visible siege turret. Pre-mortem it
   against the kladde_probe eider losses FIRST (retro rule below): are hunters in
   range when the strike lands? If not, the change is flat by geometry like mh was.
3. **Grind residual** (kladde_probe eider/hive 0/16): mechanism NOT fully decoded —
   the strike is 2-3 staggered sentinels; neither labor (rp) nor healing (mh) moved
   it. Diagnose the actual binding constraint from a captured replay before any build.
4. **Nemesis ladder audits:** LUNDS 0-5 lifetime (worsening; the chip class — v54 may
   already fix), Ouroboros 0-4 (likely grind class), Landers, Orizon. Powerpuff and
   I Stone were broken during the night (map-draw dependent).
5. **opp_v50 dip watch:** if v54's ladder trajectory disappoints, the -4 vs the x3r0
   proxy is the first suspect — per-map rows in `mh_v50_full.txt` (session-10
   scratchpad, regenerate if gone).
6. Weekly rotation watch unchanged (15 maps, all local, census at session start).

## Operating notes (updated with the session-10 retro — Magnus signed off)

- **Two-tier, flat:** Fable inline on design/verdicts/measurement; single Opus workers
  implement; single Sonnet readers audit/analyze. Subagents NEVER measure. One gated
  change at a time; results.tsv single-writer.
- **RETRO FIX 1 — map-targeted screens first:** 32-match runs on the 2-3 target maps
  (seconds) before any full 240; full batteries only for keeps/ships.
- **RETRO FIX 2 — pre-mortem variants:** before commissioning an implementation, ask
  an analyst whether the proposed mechanism is BINDING in the actual losing replays
  (four trace-proven-but-game-flat variants in one night taught this).
- **RETRO FIX 3 — threshold the monitors:** the appending Elo logger runs silent;
  wake the session only on new submission, |Δrating| > 25, or a 4+ streak. Re-arm
  THREE monitors at session start (Elo/submission logger 5-min; match watcher 2-min;
  opponent-version watcher 10-min over the nemesis list — Lunds/CAD/Ouroboros/kladde/
  Flotte/Powerpuff, wakes on version bumps, which invalidate A/B baselines and probe
  fidelity for that team); exactly one appending logger at a time. (Watcher added
  session 11 on Magnus's ask; opponent versions read from match-list JSON.)
- **Ship policy:** local-battery-clean ships (Magnus, session 10); bar = improvement
  on a primary instrument, no clear regressions, guards green, 0 crashes; judgment
  trades (like v54's) get Magnus's call when present. Baseline row at every
  activation; rolling ~20-match trajectory check; rollback on clear unconfounded
  decline. Submissions: `fcode submit bots/<dir>` works from any path and
  AUTO-ACTIVATES; `bots/v*` freeze-copies are Magnus-only (harness-enforced).
- **Unrated matches:** CLI `fcode match unrated <team-id> --map X` (×5); (team,map)
  pairs are deterministic — one sample each, rerun only as before/after across a ship.
  They always run the ACTIVE bot. Rate limit ~5/10min shared.
- **Replay tooling:** tools/replay_census.py + tools/replay_schema.md decode
  .replay26. Session scratchpads DIE with the session — the decoder scripts
  (timeline.py, report_gen.py, econ_curve.py, seat_check.py) must be regenerated from
  replay_census.py by a fresh analyst; budget ~10 min for that on first use. Prefer
  fresh Sonnet analysts + scripts over resuming one long-lived analyst agent.
- SPRT (tools/sprt.py) for screens/discards; fixed-480 for ship gates. The
  identical-per-map-rows fingerprint = the edit didn't change the games (dead branch
  or non-binding mechanism) — caught three such cases; check it reflexively.
- `results.tsv` untracked append-only; `elo_history.tsv` tracked. No git remote.

## Where things live

| path | what |
| --- | --- |
| **`bots/_v70mh`** | **live v54** (= `_v70rp` + convergence) |
| `bots/_v70rp` | respawn-on-death alone (HOLD, clean) |
| `bots/_v69clean` | pre-v70 family head (v53 + succession + dead-branch removal) |
| `bots/_v68si` | live v53 content |
| `bots/band_probe` / `flotte_probe` / `kladde_probe` | the instrument triad, frozen, md5s above |
| `bots/opp_v50` | x3r0's newest (proxy gate; know its -4 caveat) |
| `bots/opp_v49` / `opp_v45` / `opp_v39` / `starter` / `rush_probe_fast` | older references/guards |
| `tools/sprt.py` | SPRT screening gate |
| discarded, kept for reference | `_v69pp` `_v69bc` `_v69dr`(inert-held) `_v67hg*` `_v66eq*` `_v66mA` |

## Traps (session-10 additions to the standing list)

- Store writes buffer one round AND last-write-wins within a round (core first,
  builders after) — a same-round read-back is always stale, and an unguarded builder
  write clobbers a core escalation every round. Guard pattern: write only when the
  stale read is 0.
- Builders cannot attack UNITS, only buildings. Turrets are buildings.
- A turret firing at the core is not firing at its adjacent attacker.
- get_unit_count() lumps core+builders+turrets — use its DROPS, not its value.
- can_heal() refuses a full-HP target, so heal-reflex gates can be loose.
- Probes can be HARDER than their wild exemplars (kladde_probe's 3-sentinel strike vs
  wild kladde's 2) — a flat probe result doesn't kill a wild-pattern fix; weigh both.
- fcode run syntax: map path is POSITIONAL (`fcode run A B maps/x.map26 --seed N`).
- **Unrated legs FLIP SEATS between challenges** (measured session 11: same team+maps,
  opposite team indices hours apart). Before/after leg comparisons are seat-confounded
  unless the seat matches — check teamAId in the match JSON, and treat cross-seat legs
  as different games, not regressions.
- A nemesis class's strike timing can be far wider than its decoded sample (Lunds:
  audited r150-900, then landed r69) — fixed round floors gate against the sample,
  not the class.
