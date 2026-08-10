# LIVE: **v104 = "Loki v2"**. Session 27 wrap, 2026-08-10 ~14:5x CEST.

## ===== READ `PROGRAMME.md` FIRST, THEN THIS. `tools/gate.py` ENFORCES IT. =====
## Then read **`CLAUDE.md` POINT 0** — the exploit hunt is the standing brief.
## Before any ship row: `tools/preflight.py`. **SUBMIT ONLY VIA
## `tools/submit_clean.py`** — bare `fcode submit` ships our docs to the platform.

## ===== STATE, VERIFIED AT WRAP ON THE PLATFORM (not recalled) =====
##   LIVE: **v104 "Loki v2" = `bots/_v130loki13`**, py-tree md5 **bb4140f5**.
##   **1675 @ 677 matches, rank #23/116, last-10 5W-5L.** Peak this session 1698.
##   **ACTIVATION BASELINE = 1615** (captured 07:18:15Z). **net_act +60.0.**
##   The treatment is ONE CONSTANT vs its parent: `PAVE_TRAIL_ON: True -> False`.
##
##   **ROLLBACK TARGET: v102 = `bots/_v124loki8`**, md5 **e8697ffa**, submission
##   `ff270a6c`. `.venv/bin/fcode submission activate 102` —
##   **VERSION INT, THEN VERIFY WITH `fcode status`.**
##
##   **⚠ v104 SHIPPED ON EVIDENCE THAT LATER FAILED ITS OWN CONFIRMATION.**
##   The pre-registered confirmatory test returned **-7.0pp, p=0.303** against a
##   predicted -18pp. **NOT CONFIRMED.** Magnus chose **HOLD AND KEEP MEASURING**
##   — rolling back on p=0.30 would act on evidence no stronger than what
##   shipped it. **"Not confirmed" is NOT "refuted"**: the direction still
##   favours v104 by 7pp and its ladder run is +60. See
##   `docs/research/RESULT-confirm-pavetrail-2026-08-10.md`.

## ===== THE FIRST THING TO DO, AND IT IS NOT A PLANK =====
## **THE PANEL IS A TWO-CELL INSTRUMENT.** Across four windows: The Bisons
## **0,0,0,0**; Leviathan **4,4,4,4** — range ZERO, inert constants.
## CtrlAltDefeat is a third ceiling. **Only I Stone and gsxWins ever move**, so
## every currency number on record is a read on two cells wearing a five-cell
## denominator. **Two separate 18pp claims have now failed to resolve on it.**
##   **`docs/prereg/PREREG-panel2-calibration-2026-08-10.md` is committed and its
##   arm has fired ZERO matches. RUN IT FIRST.** It measures 5 candidate cells on
##   the live fixture (admission band 0.20-0.80) before any plank is measured on
##   them. Candidates: OopsGotYourElo `f61d19c1-…`, Team 48 `48340ad8-…`,
##   Banminary `0774b1b2-…`, plus retained I Stone and gsxWins.
##   **The old panel was picked on RATING PROXIMITY, which does not predict
##   whether a cell can MOVE.** Do not repeat that.

## ===== SIX ARMS, PRE-REGISTERED, PARTIALLY FILLED — ALL STOPPED AT WRAP =====
## `tools/fanout.sh` rotates arms through the free windows. **IT IS STOPPED AND
## MUST NOT BE LEFT RUNNING UNATTENDED** — see the wake path below.
## Match ids: `docs/legs/LEG-MATCH-IDS-2026-08-10.md` + `scratchpad/arm_*.txt`.
##
## | arm | n | reading |
## |---|---|---|
## | CONTROL v104 | 30 matches (150g, cleaned) | the denominator |
## | LOKI-15 quota v105 | 32 | **-14.7pp, p=0.0149 — SIGNIFICANTLY WORSE** |
## | CONFIRM v102 | 20 (n=100, **COMPLETE**) | **-7.0pp, p=0.303, NOT CONFIRMED** |
## | LOKI-16 ring-hold v106 | 15 (75g of 100) | interim -0.7pp, p=1.00 |
## | LOKI-14 kidnap v107 | 15 (75g of 100) | interim -2.0pp, p=0.78 |
## | PANEL2 calibration | **0** | **not started — run first** |
##
## **LOKI-14's PRIMARY bar is NOT currency** — it is undamaged enemy removals
## within 3 rounds of a BORDER throw vs an INTERIOR throw (the within-leg
## placebo). **That decode has not been run.** Its currency reading says nothing
## about the exploit.

## ===== ⚠ THE TWO SAFETY FAULTS THAT BIT TODAY =====
## 1. **A fanout arm's rollback failed and left v102 live for ~5 minutes**, then
##    the next arm — CONTROL, which activates nothing and so asserted nothing —
##    fired **10 games into the wrong bot**, contaminating the denominator.
##    **FIXED**: `fire()` now asserts the holder before every challenge and
##    writes `corpus/FANOUT_ABORT`. Mutation-tested both ways.
##    Quarantine record: `docs/legs/QUARANTINE-2026-08-10.md`.
## 2. **`elo_history.tsv` tags rows by the version ACTIVE AT POLL TIME, not by
##    the version that PLAYED the match.** `slot_rule` and `ship_watch` both
##    segment on that tag, so every arm flip fragments the incumbent's window.
##    **Documented in `tools/slot_rule.py`, NOT patched** (four instruments broke
##    IN the fixing in s26). **Durable fix: attribute by per-match
##    `teamAVersion`/`teamBVersion` from `match list --type ladder`.**
##    With fanout stopped the tag settles and the rule reads correctly again —
##    verified at wrap: `v104 k=31 armed=True slot_free=False`.

## ===== ⚠ TWO THINGS A SUCCESSOR WILL SEE IMMEDIATELY =====
## **`slot_free=True` — AND THE ANSWER IS HOLD.** At wrap: `v104 k=32
## rating=1664 net5=-31.0 slot_free=True`. The rule is a **CONJUNCTION**:
## `net5 <= -21` **AND** `net_act < 0`. **net_act is +49.0**, so it is FALSE.
## **`slot_free` is a PERMISSION AND A WAKE, NEVER A VERDICT.**
## Roll back only if the rating drops **below 1615** while net5 stays <= -21.
##
## **`tests/test_instruments.py` HAS ONE RED TEST AND IT IS LEFT RED ON PURPOSE.**
## `test_does_not_fire_on_a_normal_shipping_day` fails: a 12-activation, 20-hour
## day reads as a cadence STALL, so **`audit_trigger` would summon an audit on a
## normal working day.** It was inside the 18 tests the boot procedure silently
## skipped until this session, so it has been red for an unknown time while every
## boot block logged "14/14 OK". **`audit_trigger` fired 2/5 at this session's
## boot, one signal being ship cadence.** Fix the calibration or narrow the
## signal — **do not delete the test.**

## ===== QUEUE, IN PRIORITY ORDER =====
## 1. **PANEL-2 CALIBRATION.** Nothing else is trustworthy until it runs.
## 2. **LOKI-14's crash-mechanism decode** — border vs interior undamaged
##    removals, via `tools/crash_census.py`. The exploit's actual bar, unread.
## 3. **Finish LOKI-16 and LOKI-14 to their pre-registered n=100**, on a panel
##    that can resolve them.
## 4. **Generalised throw-to-stale-state** — RULED IN-CLASS (`CLAUDE.md` point 0);
##    no new organiser question needed. Build after LOKI-14 reads out.
## 5. **A fresh pre-registered confirmation of v104 at larger n**, on panel-2.
## **OFF-PROGRAMME, do not re-open:** economy suppression (LOKI-15 is
## significantly worse; LOKI-13's mechanism bar failed), and the four exploit
## roads the guard-matrix sweep closed (`CLAUDE.md` point 0's road list).

## ===== WAKE PATH — WHAT IS AND IS NOT WATCHED =====
## **SURVIVES (detached, verified BY OUTPUT at wrap):** elo_logger 25811 ·
## match_watcher 25942 · opp_watcher 25943 · replay_archiver 25944 ·
## keeper 89444 · **ship_watch** (armed, `RULE=held net_act +60.0`).
## `slot_rule` reads **v104 k=31 armed=True slot_free=False**.
## **`breakin_watch` correctly STOOD DOWN** at k=64 >= 8 — by design, it hands
## back to the slot rule.
## **STOPPED DELIBERATELY: `tools/fanout.sh`.** A rotation that activates
## experimental bots must not run unattended — **twice today a rollback failed
## and left a non-incumbent live**, and one of those was v105, which measures
## **-14.7pp worse**. **Restart it only with a session watching.**
## **NOTHING WAKES A SESSION.** First actions at next boot: `fcode status`
## (confirm `Active bot: v104`), `cat corpus/SHIP_ALERT` (absent = fine),
## `cat corpus/FANOUT_ABORT`, `tail corpus/ship_watch.log`.

## ===== PRIOR STATE — ARCHIVED, NOT DELETED =====
## s26 block: `docs/archive/HANDOVER-s26-block.md`.
## s24 and earlier: `docs/archive/HANDOVER-prior-blocks-through-s26.md`.
## **Read them deliberately. Do not read them by default** — they were costing
## ~32k tokens of every builder boot on 93%-superseded state.
