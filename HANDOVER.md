# LIVE: **v104 = "Loki v2"**. Session 27 wrap, 2026-08-10 ~14:5x CEST.

## ===== READ `PROGRAMME.md` FIRST, THEN THIS. `tools/gate.py` ENFORCES IT. =====
## Then read **`CLAUDE.md` POINT 0** — the exploit hunt is the standing brief.
## Before any ship row: `tools/preflight.py`. **SUBMIT ONLY VIA
## `tools/submit_clean.py`** — bare `fcode submit` ships our docs to the platform.

## ===== STATE, VERIFIED ON THE PLATFORM (not recalled) =====
##   LIVE: **v104 "Loki v2" = `bots/_v130loki13`**, py-tree md5 **bb4140f5**.
##   **REFRESHED s28 2026-08-10 13:44Z: 1658 @ 680 matches, rank #25/116,
##   last-10 7W-3L.** Peak 1698 (s27). **ACTIVATION BASELINE = 1615.**
##   **net_act +43.0.** `slot_rule`: `k=34 net5=-31.0 armed=True slot_free=True`
##   -> **still HOLD**: the conjunction needs `net_act < 0` and it is +43.
##   **43 points of headroom to 1615, and ship_watch's conjunction goes TRUE
##   exactly at that crossing, so the alarm is armed for it.**
##   Trajectory 1698 -> 1658 over ~1h40 (drawdown -40) against a v102 control of
##   -36 over a longer run: **top of range, not a regime change.**
##   (s27 wrap block read 1675 / net_act +60 and was 17 points stale within two
##   hours. **A STATE BLOCK THAT SAYS "VERIFIED AT WRAP" IS AN EXPIRY DATE, NOT
##   A GUARANTEE — re-read it live at boot before acting on it.**)
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
## | LOKI-16 ring-hold v106 | 15 (75g) | **s28 VERDICT: UNRESOLVED — not advanced, not killed** |
## | LOKI-14 kidnap v107 | 15 (75g) | **s28 VERDICT: FALSIFIER 1 FIRES — refuted vs THIS PANEL only** |
## | PANEL2 calibration | **RUNNING s28** | own runner `tools/panel2_cal.sh`, no activation |
##
## **BOTH DECODES ARE DONE AND BOTH VERDICTS ARE TYPED** (`b1ca257`; register
## rows `857ac2c`; read-outs `f13e375` + `b5266ee`).
## * **LOKI-14: 0 undamaged removals from 150 border throws** (bar >=45), placebo
##   clean (interior 0/164), mechanism bar met 7.5x, under-dosing RULED OUT.
##   **Scope is pre-committed: refuted against THESE FIVE TEAMS, not as a class.**
##   The census is bimodal and **no carrier is on our panel.**
## * **LOKI-16: coverage +0.086 vs a >=+0.08 bar, bootstrap 95% CI
##   [-0.038, +0.196]** — and the bar is met or missed by choosing an estimator
##   afterwards (four estimators inside 0.010). Mechanism DOES move in the tail.
##   **jackpot KEPT on the panel** — dropping it would be fitting the panel to
##   the plank (the CONTROL gains there, +0.159; the treatment is flat).

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
## **RETRACTED s28 — THE SUITE IS GREEN (32/32) AND THAT IS CORRECT.**
## This block used to say `test_does_not_fire_on_a_normal_shipping_day` was left
## RED ON PURPOSE, proving `audit_trigger` "would summon an audit on a normal
## working day." **That reading was WRONG and the test is now repaired, not
## deleted** (commit `c347ec7`). `ship_cadence` measures its cutoff from
## `datetime.now()`; the fixture hardcoded the literal `2026-08-09T10:00`; once
## the clock passed 2026-08-10T10:00 every fixture row aged out of the 24h
## window, the check counted ZERO transitions, and the test failed reporting
## `0.0`. **THE FIXTURE ROTTED. THE CHECK WAS NEVER MISCALIBRATED** — pinned to a
## fixed clock it returns 0.60/hr on the normal day (ok, threshold 0.5) and
## 0.10/hr on the stalled day (trips), correct in both directions. `now` is now
## overridable alongside `elo`/`hours`, and the repair is mutation-tested
## (breaking `ship_cadence` turns the test red).
## **DELTA, and it is the durable one: A RED TEST IS EVIDENCE OF A DEFECT, NOT
## EVIDENCE OF *WHICH* DEFECT.** This one misnamed its own component; the
## misnaming was promoted into HANDOVER as an instrument fact and from there into
## the brief given to the audit session. Note also that the s26 repair which
## de-live-ified `hours` **reintroduced wall-clock coupling one layer down** —
## a repair against a failure CLASS must be verified against the class, not
## against the instance that prompted it.
## **CONSEQUENCE: the boot FIRE is REAL on both signals.** Raw ship cadence
## 0.38/hr; stripping the 4 fanout round-trips (v102→v103→v102, v104→v102→v104)
## leaves **4 durable activations in 24h = 0.19/hr**. Counting logic deliberately
## LEFT UNCHANGED while the audit session evaluates that instrument.

## ===== QUEUE, IN PRIORITY ORDER (rewritten s28) =====
## 0. **THE FIXTURE CANNOT RESOLVE AN 18pp CLAIM. THIS IS THE FRAME FOR
##    EVERYTHING BELOW.** `tools/leg_read.py` now computes it instead of printing
##    a hardcoded "~20pp at best" at every n: **MDE 21.7pp on live cells.**
##    Every 18pp-class claim fired on 2026-08-10 sat BELOW the panel's own
##    resolution, which is why p=0.303 was the expected output. **Do not fire
##    another currency leg on this panel without checking `--bar` against MDE.**
## 1. **PANEL-2 CALIBRATION — RUNNING.** `tools/panel2_cal.sh` (5 cycles,
##    n=25/cell, no activation, zero rated cost). Admission band [0.20, 0.80]
##    INCLUSIVE. Read out with `leg_read.py`'s per-opponent split.
##    **Add the map-admission check to it** — `tools/map_admits.py` (D34).
## 2. **LOKI-14b — ⚑ FIRING NOW. Its CEILING IS ALREADY KNOWN: the border road
##    is DEAD FOR CLIMBING.** The inverted cut (archive-only, fidelity gate
##    passed to the digit) found **ZERO carriers among the 23 teams at or above
##    our rating** — pooled 4 events / 400,852 border rounds, **>=460x below the
##    weakest carrier**, and IMMUNE not under-observed (smallest denominator
##    16.8x the detection threshold). **The escape hatch is closed by
##    measurement: top teams stand on borders MORE than carriers do** (Pivot
##    9.78%, sporks 7.53% vs vjg 5.66%) and do not die there.
##    **=> No result licenses shipping border-throwing; no further leg on this
##    trigger after 14b** (PREREG amendment 8). It finishes anyway because its
##    NEGATIVE closes the road on an interventional test rather than an archive
##    cut. **8 amendments, ALL blind vs the first accepted challenge
##    14:10:40.033Z**; v107 exposure per cycle: **10 SECONDS**.
##    **THE ROAD THAT IS STILL OPEN: the DISPLACEMENT / stale-plan trigger.**
##    Every number above is OBSERVATIONAL (builders that WALKED to a border); a
##    thrown builder stands on a tile its own cached plan never chose. Same
##    approved class (D17), untested by all of it. That is LOKI-14c.
##    **AND THE CONFOUND IS ONLY PARTIAL** — immune teams sit in the SAME low
##    band as carriers (S 1093.7 vs Tyvrets 1098.6: **4.9 Elo apart, >=891x
##    apart in hazard**). Vulnerability is a property of border-handling CODE,
##    not of weakness. Supports the legality-mask explanation (amendment 5a).
##
## 2b. **(superseded) LOKI-14b as originally queued — PRE-REGISTERED, NOT FIRED.**
##    `docs/prereg/PREREG-loki14b-carrier-targeted-2026-08-10.md` (15:29:57 CEST;
##    Amendment 1 at 15:38:30). Same bot (v107), **fixture varied** — the four
##    boundary carriers (vjg/Troupe/S/Ship Happens), whose border hazard is
##    224/10k pooled against **ZERO** off-border (HR >= 17,432x).
##    **BLOCKED ON:** research's per-carrier recency table, gated by Amendment
##    1's pre-committed thresholds (PATCHED vs INSUFFICIENT kept distinct;
##    **<2 carriers admitted = the leg does not fire**; no substitutions).
##    **Needs a real v107 activation** — D26 holder-verify on rollback applies.
## 3. **LOKI-16b** — same plank, bar changed to **longest-hold/length**, named in
##    the prereg BEFORE firing (it was refused for LOKI-16 as post-hoc), reported
##    **per ring-stratum** (12-tile maps vs jackpot's 5).
## 4. **Generalised throw-to-stale-state** — RULED IN-CLASS (`CLAUDE.md` point 0).
## 5. **A fresh confirmation of v104 at an n the fixture can actually resolve.**
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
