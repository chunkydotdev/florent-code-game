# Session 14 LIVE header (builder arm; supersedes the s13 block below where in conflict)

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

## Session-14 state at last update (~19:50)
- LIVE: **v68 "chokewall" (x3r0), uploaded 19:12, auto-activated mid-gate.**
  1589 @ 276 rank #25 and climbing at last elo row. opp_v68 local copy
  extracted (md5 04811b4a...); research first-read commissioned.
- **Eir 6c (`bots/_v79e6c`, md5 8aaa91e6...) PASSED gate stage 1**
  class-weighted (orizon +16.7 / v63 +6.7 / band +5.0 / cad flat / ouro at
  long-run / kladde soft −7 accepted trade, mechanism + parked fix on
  tape). = 5.1 + budgeted proactive trunk repair + pop floor (isolation-
  verified) + ammo actually off. K'-cap variant (6b) refuted; full arc in
  results.tsv rows _v78e6b*, _v79e6c*.
- **Stage 2 slot bar RUNNING vs opp_v68**, 480 games, bar = beat the slot
  holder (team norm). Ship decision after; slot calls remain Magnus/x3r0.
- Archiver our-matches-first SORT BUG found+fixed (session-14 comment in
  replay_archiver.py); older 5 of the 6 gap matches land next cycle.
- Still BLOCKED: Eir 5.1 traceback fix (x3r0 data).

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
