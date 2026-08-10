# LIVE: **v102 = LOKI-8**. Session 26 wrap, 2026-08-10 05:4x CEST.

## ===== READ `PROGRAMME.md` FIRST, THEN THIS. `tools/gate.py` ENFORCES IT. =====
## Before any battery: `tools/gate.py`. Before any ship row: `tools/preflight.py`.
## **SUBMIT ONLY VIA `tools/submit_clean.py`** — bare `fcode submit` ships docs.

## ===== STATE, VERIFIED AT WRAP (not recalled) =====
##   LIVE: **v102 = `bots/_v124loki8`**, submission `ff270a6c`, py-tree md5
##   **72a3baf6**. **1586.2 @ 624 matches, rank 30/116, last-10 4W-6L.**
##   **ACTIVATION BASELINE = 1567.44** (NOT the 1577.5 in older blocks — that is
##   the rating before v101's LAST game; the platform's per-match `teamAVersion`
##   settles it). **Net +18.8 over 54 matches.**
##   **ROLLBACK TARGET: v101, verified `ready` on the platform at wrap.**
##   `.venv/bin/fcode submission activate 101` — **VERSION INT, NOT ID — then
##   VERIFY** (s25 D9: an id-based restore chain failed open with an untested
##   bot live).
##
## ===== THE SLOT: FIRED TWICE TONIGHT, HELD BOTH TIMES, CURRENTLY CLEAR =====
##   At wrap: **k=54, net5 -3.0, `slot_free` False, no `SHIP_ALERT`.**
##   The arm ran **1567 -> 1600 -> 1572 -> 1616 -> 1585 -> 1599 -> 1580 -> 1586**.
##   **`SLOT_FREE` fired at k=36 and k=52. HOLD both times, per a decision
##   PRE-COMMITTED at k=34 while the alarm was still silent.**
##   **THE PRE-COMMITMENT IS A CONJUNCTION AND IT STILL GOVERNS:**
##   **`net5 <= -21` AND `net_act < 0`.** net_act is **+18.8** — v102 is still
##   ABOVE the rating v101 handed it, which is the whole test: **hold while the
##   ship beats its replacement.** The other trigger is the **slow SPRT
##   (MU0=-4)** accepting BLEED. **At 1567.4 or below with net5 <= -21, ROLL.**
##   **`slot_free` is a PERMISSION AND A WAKE, NEVER A VERDICT.**
##
## ===== WAKE PATH — WHAT IS AND IS NOT WATCHED AFTER THIS SESSION =====
##   **SURVIVES (detached, PPID 1, all verified BY OUTPUT at wrap, not by `ps`):**
##   elo_logger 25811 · match_watcher 25942 · opp_watcher 25943 ·
##   replay_archiver 25944 · keeper 89444 · **ship_watch 66915** (armed on the
##   CORRECTED 1567.44 baseline). All five owned files written within ~7 min of
##   wrap. *(An earlier flag that `match_watcher` was stale was a quiet ladder
##   hour; it is writing.)*
##   **DIES WITH THIS SESSION:** every subagent (all relayed, none live).
##   **NOTHING WAKES A SESSION.** `ship_watch` will write `corpus/SHIP_ALERT`
##   and clear it on recovery — **observed doing all three tonight** — but no
##   process boots a session to act. **FIRST THING AT NEXT BOOT:
##   `cat corpus/SHIP_ALERT` (absent = fine), then `tail corpus/ship_watch.log`.**
##   **Any `CLEARED` line in that log is PRE-s26 and means nothing** — two
##   schemas. **The tape lags live by up to 5 min** (elo_logger polls at 300s).

## ===== ⛔ THE STANDING CONTEXT DESCRIBES EIR, NOT THE BOT YOU ARE RUNNING =====
##   The replay archive is **~92% Eir** (1,580 Eir games vs 130 LOKI-8), so every
##   figure in the tactics library and in this file's older blocks is an EIR
##   figure unless it says otherwise. Re-run on the v102 subset, **four standing
##   claims INVERT** (research, s26):
##
##   | standing claim | Eir, as published | v102, SAME instrument |
##   |---|---|---|
##   | "we bank and do not spend" (Ti held r200-300) | us 506 / field 348 | **us 96 / field 210 — INVERTED** |
##   | "we under-build turrets" (r200-300) | us 0.64 / field 2.22 | **us 2.15 / field 1.18 — we OUT-build** |
##   | "everything breaks at r150" (ammo Ti/100r) | 212 -> 156 -> 130 | **209 -> 300 -> 253: 43% MORE after r150** |
##   | "353 games reached r1000, we won 57.2%" | 30.2% reach r1000 | **6.9% — 1 in 9. No current denominator.** |
##
##   **"We bank and do not spend" is the library's oldest complaint and it is
##   FALSE OF THE LIVE BOT.** Both arms reasoned from it repeatedly this session.
##   **Also does not reproduce:** the home-defence advantage under "the forward
##   road is closed" — Eir **+16.3pp**, v102 **-10.0pp** (n=439). That is
##   "does not reproduce", NOT "refuted" — but a headline conclusion is no longer
##   standing on its published number.
##
##   **RULE FOR A SUCCESSOR, and it is the sharpest form we reached:
##   USE A STORED FIGURE TO CHOOSE *WHAT* TO TEST, NEVER *HOW MUCH* TO EXPECT.**
##   Nine failures tonight across two lanes were one fault in different clothes —
##   **a number true SOMEWHERE, used SOMEWHERE ELSE**: a view used as a
##   population, an assumed capacity used as a measured utilisation, an assumed
##   game length used as a per-turn rate, a 480-file battery used as "the arena",
##   an Eir archive used as the current line.
##
##   **THE FIX IS THE SAME IN ALL NINE: MEASURE BOTH SIDES OF THE COMPARISON
##   INSIDE THE THING YOU ARE TESTING.** A paired within-arm control is immune to
##   era drift BY CONSTRUCTION — both arms are the same bot on the same day, so
##   what the archive is made of cannot matter. A control arm in the same fixture
##   is immune to fixture contamination — a probe that cannot see your buildings
##   cannot see them for EITHER arm.
##
##   **THE DEMONSTRATION, because it is better than the argument:** three planks
##   were sized in one evening. **Two died of era drift before firing.** The third
##   (LOKI-10) survived **not because anyone foresaw the era problem** but because
##   its prereg pinned every bar to a paired within-leg control and pre-declared
##   its currency channel closed. **Subject hygiene, applied for unrelated
##   reasons, turned out to be the same defence.**


## ===== QUEUE, IN PRIORITY ORDER (s26 wrap) =====
## **MAGNUS'S STANDING CORRECTION, 05:3x: "We havent runt any unrated games for
## 8 hours."** Each leg-skip was individually defensible and collectively the
## mill stopped producing. **THE OUTPUT STAGE IS A LEG. Fire one early.**
##
## 1. **FINISH LOKI-10 — it is one commit from meeting its bar.** The leg fired
##    (480 games, gate cleared): builds onto a conveyor-faced tile went
##    **control 58 -> variant 11, an 81% cut, but the bar was ZERO. NOT MET.**
##    Cause is named: `_feeds_tile` is wired into `_try_counterbattery` ONLY,
##    while emplacements also come from raid.py (forward sentinel, barriers) and
##    the launcher. **Call the same predicate at those sites, re-run, re-read.**
##    **Then add the MIRROR predicate** (prereg addendum 2): refuse a CONVEYOR
##    whose facing points at an existing friendly turret/barrier — that is
##    **66 Ti/game against the forward pairs' 36**, so the plank goes from ~35%
##    of its class to all of it. **No currency claim either way: the prereg
##    pre-declares the channel closed (93% of v102 games end core_destroyed).**
## 2. **CLASS-1-AIMED ROUTING — the best-specified unbuilt plank we have.**
##    +411 Ti/game net, 11.9x return, fires in **59% of games** and least
##    tail-carried. **The discriminator: walk upstream from a dead end; if the
##    chain reaches a friendly harvester, finish it.** That predicate is the
##    entire difference between **+411 and -223** — unconditional completion is
##    NEGATIVE. **Two things settled for the build: a visited set is MANDATORY
##    (cycles are ~1 in 10 of our binding tiles), and DO NOT walk per builder
##    per turn** — topology changes only on build/destroy, so use the
##    `roadCoverage` shape: one unit walks and writes a small non-negative
##    integer to the store, every builder reads it. We currently have no way to
##    express "the network is broken" at all.
## 3. **THE FORWARD-GATE REVERT.** v102 gates on a LIVE census
##    (`_live_fwd_guns`) which sits below cap in 96-100% of rounds — **a cap
##    that is never approached is not a cap.** Eir still uses a CUMULATIVE
##    per-builder budget and shows a hard cliff at 3. **Revert the LOKI-2b
##    conversion.** Costed: fires in 11.9% of games, 42% excess share, but
##    **88.1% of games bit-identical and 77% of the mass in FOUR games** —
##    so **ship it bundled, never as its own leg.**
## 4. **CORRECTED FIXTURE VARIANTS — `cad_probe2` / `orizon_probe2`, ALONGSIDE,
##    NEVER IN PLACE.** Both resolving fixtures carry `best_core or best_any`,
##    which short-circuits. Editing them in place would make future measurements
##    incomparable with every banked one, INVISIBLY. Also classify
##    `ouroboros_probe:1053` as a possible sixth member.
## 5. **Per-opponent gates** and **the 79.95%-of-gunner-rounds-with-no-enemy-on-
##    the-ray siting road** (LOKI-9 proved facing is NOT the lever).

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

