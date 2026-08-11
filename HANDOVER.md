# LIVE: **v104 = "Loki v2"**. s28 state, 2026-08-10 17:31 CEST (15:31Z).

## ===== ⭐ TOMORROW'S BEST-CORROBORATED CANDIDATE: TURRET MIX =====
##   **212,563 builds, third-party matches included. Us vs the 23 teams at or
##   above 1683:**  gunner **56.4% / 69.8%** · sentinel **32.8% / 23.2%** ·
##   launcher **10.8% / 7.0%**. **We build the expensive turret; they build the
##   cheap one 2:1.**
##   **It independently reproduces a finding already in CLAUDE.md FROM THE KILL
##   SIDE** — top-tier cores die 53.1% gunner / 44.4% sentinel while our kill mix
##   inverts it at 22.7 / 69.2. **Two different measurements (built vs
##   killed-with), same direction. More corroboration than anything else queued.**
##
##   **⛔⛔ s29 2026-08-11 06:1x — THE D30 GREP BELOW WENT ONE LINE TOO SHALLOW.
##   `main.py:544` IS INSIDE `_try_counterbattery`, WHICH IS A DEFENSIVE PATH.**
##   Its own docstring: *"Build only a weapon ray that already contains the
##   reported threat."* It is gated on `SLOT_THREAT` being set, on the threat
##   sitting inside `HUNT_BAND_DSQ` of **our own** core, and on `_live_home_gun`;
##   its sibling `_cb_over_heal` opens with `self.role != "defend"`. **So the
##   "one-constant change" is a change to HOME DEFENCE, and `PLAY_DEFENCE: never`
##   puts it off-programme regardless of what it would measure.**
##   **The grep found the right LINE and stopped before the enclosing FUNCTION.**
##   Same shape as the LOKI-17 death two blocks down: the diff was read, the
##   thing the diff sits inside was not.
##
##   **THE ON-PROGRAMME HALF IS THE OTHER SENTENCE, and it is NOT one constant.**
##   *"`raid.py` builds ONLY sentinels — zero `build_gunner` calls"* — that is
##   the forward siege, turrets bought to open a lane to the enemy core, and it
##   is squarely on-programme. **But a gunner is not a drop-in for a sentinel
##   there:** gunner r²=**13** vs sentinel r²=**32**, so a forward gunner must be
##   planted more than twice as close, and **a gunner's shot is BLOCKED by
##   obstacles while a sentinel's ignores them** — which is a live reason to
##   prefer the sentinel when sieging a core behind cover, not an oversight.
##   A forward-gunner plank needs its own d²≤13 siting routine. **Real, and it is
##   a build, not a constant.**
##
##   **AND THE CORROBORATION IS WEAKER THAN THE BLOCK BELOW PRESENTS.** We build
##   **56.4%** gunners against the top-23's 69.8% — a 13pp gap, not an inversion.
##   The striking half (*cores die 53.1% gunner while OUR kills are 69.2%
##   sentinel*) is **substantially tautological**: our forward siege is sentinel
##   by construction, so our kills are sentinel by construction. **Two
##   measurements pointing the same way is worth less when one of them is
##   downstream of the other.** Still worth testing; not worth calling
##   "more corroboration than anything else queued".
##
##   **⭐ D30 GREP DONE — AND IT IS A ONE-CONSTANT CHANGE, exactly like LOKI-16:**
##   `main.py:544` — the choice is a FIXED TUPLE ORDER, not a costed decision:
##   ```
##   choices = ((EntityType.SENTINEL, cost), (EntityType.GUNNER, cost))
##   for turret_type, cost in choices:   # takes the FIRST affordable one
##   ```
##   **And `raid.py` builds ONLY sentinels — zero `build_gunner` calls — so our
##   entire forward siege is sentinel by construction.** Nothing weighs 6 dps and
##   r2=32 against 20 Ti vs 30 with **46.9% of our turrets dying on the ladder**.
##   **THE PUZZLE A PREREG MUST NAME RATHER THAN ASSUME:** the sentinel dominates
##   on paper (6 dps vs 3.5, r2 32 vs 13, ignores obstacles) and better teams
##   build the weaker-looking turret anyway. Candidate mechanisms: cheap turrets
##   lose less per death at a 46.9% death rate; a gunner ROTATES for 10 Ti while a
##   sentinel's single-tile line must be sited right first time.
##   **STATUS: PRIORITISES, DOES NOT ESTABLISH (D12)** — observational, our own
##   archive, build mix is not effectiveness, and `builds.tsv` cannot see
##   conveyors/harvesters/barriers.
##   **It fits the race frame below**: turret mix moves kill TIME, and our losses
##   are races lost by margin.
##
## ===== ⭐ THE FRAME FOR TOMORROW: OUR LOSSES ARE RACES, NOT ROUTS =====
##   Independently re-derived by the builder from `ladder_games.tsv`, v104 only:
##   **107 of 109 losses are CORE DEATHS — only 2 tiebreaks.** Timings overlap
##   almost entirely:
##     we kill      n=129  q1 128 · **median 170** · q3 228
##     we are cored n=107  q1 134 · **median 209** · q3 296
##   **39% of losses (42/107) land BEFORE our own median kill round.**
##   **Median margin +39 rounds — we are FASTER and still lose 45%.**
##   **⇒ SPEED AND LOSS-CONVERSION ARE ONE LEVER, NOT TWO.** A game they win at
##   r180 that we would have won at r200 flips on a **25-round** improvement.
##   **The kill-speed score's balance calculation UNDERSTATES speed**: it counted
##   bucket upgrades on games already won and never counted RACES FLIPPED. That
##   value is real and currently unpriced.
##   **CONSEQUENCE FOR THE QUEUE:** the core-guess disambiguation candidate moves
##   UP — worth ~24 rounds where the rot-180 fallback guesses wrong, **paid at
##   the FAR end**, which against a 39-round margin is race-flipping rather than
##   cosmetic. **GREP THE INCUMBENT FIRST (D30):** we already do the rot-180
##   fallback; the untested half is whether we disambiguate EN ROUTE or eat the
##   full penalty on arrival.
##   **AND LOKI-16b's read-out should carry the race frame** — retention that
##   delays THEIR kill is worth as much as speeding ours, and its bar
##   (longest-hold) measures neither directly.
##
## ===== ⚠ AN OPEN DOCTRINE QUESTION FOR MAGNUS, NOT FOR A LANE =====
##   The old currency scored a LOSS and a TIEBREAK WIN identically (both 0, no
##   kill). **The new one separates them by 10 points**, so the score now rewards
##   NOT-LOSING while `PLAY_DEFENCE: never` forbids survival mechanisms.
##   **This tension could not exist under `core_kill_share`.** A workable reading
##   is *doctrine governs MECHANISM, the score measures OUTCOME* — **but it is
##   Magnus's to rule and it is deliberately UNRESOLVED. Do not settle it inside
##   a prereg.**
##
## ===== ⛔ NO AUTO-ROLLBACK TONIGHT — MAGNUS'S DECISION, 2026-08-10 ~22:3x =====
##   Verbatim: *"We dont do an auto rollback tonight, we will stand down and see
##   if we need one for next night."* **Nothing will ACT on the stop-loss
##   overnight.** `ship_watch` will still WRITE `corpus/SHIP_ALERT` if the
##   conjunction fires; **nobody reads it until morning, and that is accepted.**
##   Sizing behind the call: **v104 is +51 on its activation baseline (1615)** and
##   the trigger needs `net_act < 0` AND `net5 <= -21`, against a halved ladder
##   cadence of ~24 unattended matches. At 17:00 we were 26 points out and
##   falling and this would have been a different call.
##   **The build is ~20 minutes if wanted tomorrow** — it is a loop on a rule
##   Magnus already approved, so it delegates EXECUTION, not judgement.
##   **MORNING: read `corpus/SHIP_ALERT` and `tail corpus/ship_watch.log` FIRST.**
##
## ===== ✅ OVERNIGHT COLLECTOR IS ALREADY RUNNING — DO NOT START IT AGAIN =====
##   Launched 21:03Z by the builder. **Holder verified `v104 (Loki v2)` on the
##   PLATFORM 60 s after launch, and again at 21:06Z. Rating 1686.**
##   `tools/night_collector.sh 40` · log `scratchpad/night_run.log` ·
##   outfile `scratchpad/arm_night.txt`. **NON-ACTIVATING** (grep-verified zero
##   `submission activate` calls) so it cannot leak and there is nothing to roll
##   back. Pacing off the live meter, retry floored at 300 s so it cannot spend
##   the budget it is waiting for.
##   **MORNING: STOP IT AND WAIT ONE FULL 20-MINUTE WINDOW BEFORE ANY LEG.**
##   `.venv/bin/python tools/rate_budget.py` must read `a slot is free NOW`
##   AFTER it is stopped.
##
## ===== (reference) THE COMMAND, IF IT EVER NEEDS RESTARTING =====
##   ```
##   cd /Users/junghard/Projects/Work/florent-code-game
##   nohup zsh tools/night_collector.sh 40 >> scratchpad/night_run.log 2>&1 &
##   ```
##   **NON-ACTIVATING** — zero `submission activate` calls (grep-verified), so it
##   cannot leak a prototype and there is NOTHING TO ROLL BACK. Asserts the
##   holder before every challenge; abort branch mutation-tested on this file
##   (`docs/legs/LEG-night-collector-2026-08-10.md`).
##   **VERIFY 60s AFTER LAUNCH:** `.venv/bin/fcode status` -> `Active bot: v104`
##   and `tail -2 scratchpad/night_run.log` shows a `fired n/9` line.
##   Targets the **bleed band** (ranks ~25-40, us-110..us+15, 9 cells) — the
##   -438.6 Elo across 58% of our diet that has **no mechanism attached**.
##   ~15 challenges/hour => ~90 challenges / 450 games over six hours.
##   **⚠ MORNING: STOP IT AND WAIT ONE FULL 20-MINUTE WINDOW BEFORE ANY LEG.**
##   Rejected attempts count against the limit; `rate_budget.py` must read
##   `a slot is free NOW` AFTER the collector is stopped.
##
## ===== LOKI-16b: BANKED AND UNREAD (not abandoned, not null) =====
##   Ran its own schedule to completion — 8 cycles, exited cleanly, **holder
##   verified v104 on the platform**. **10 challenges / 50 games**, spread
##   3·3·2·2 (farming_200s, SmartFridge, Askar City, Lunds Stallions).
##   **NO VERDICT WRITTEN, and the reason is the instrument, not the data:** the
##   primary (longest-hold/length, game-mean, match-clustered) needs a RETENTION
##   DECODER that does not exist. Both halves exist to build it —
##   `map_admits` for ring geometry, `replay_census.parse_entity` for positions.
##   **⚠ AND THE PREREG NEVER FIXED AN n** — a defect recorded in the document.
##   Decide n explicitly BEFORE reading the number, not after.
##
## ===== ⛔ NO OTHER UNRATED RUNNER SHOULD BE FIRING OVERNIGHT =====
##   Verified: no `panel3_cal`/`panel2_cal`/`loki14b`/`fanout` processes.
##   Holder **v104**, **1659, rank #26/116**, 697 matches. Budget 0/5 spent.
##   No `FANOUT_ABORT`, no `HOLDER_ALERT`.
##
## ===== PANEL-3 COMPLETE: 4 OF 6 ADMITTED, AND A MAP CONFOUND THAT OUTRANKS IT
##   Admitted (use with `leg_read.py --live-cells`): **Lunds Stallions 70.0% ·
##   Askar City 53.3% · farming_200s 28.6% · SmartFridge 26.7%.**
##   Floors: **0033 17.1% · The Bisons 8.0%.** Effective n 125/185 = 68%.
##   **The Bisons re-derivation resolved at the full n=25: FLOOR, D22 STANDS.**
##   **⛔ MAP-AXIS CLAIM RETRACTED (mine, within the hour).** Ladder cut: pinned
##   5 maps **55.1%** vs other 10 **54.5%** (n=69/156). Within-panel cross-tab:
##   variance is on the CELL axis (8%-70%) not the MAP axis (24%-46%), and
##   **Lunds is 6/6 on saga where Bisons is 0/5.** A per-map cell split is n=5
##   — noise by construction. **Do NOT rebuild the panel a third time.**
##   **STILL OPEN, and not maps: same bot, unrated on our 5
##   pinned maps 2/25 (8%), LADDER ourver=104 5/10 (50%). Per map vs Bisons:
##   atoll 0/5, fjordgate 0/5, saga 0/5, snowflake 0/5, jackpot 2/5.**
##   **We lose every game on 4 of 5 pinned maps; the ladder rotates all 15.**
##   Either the pinned set is unrepresentative (the panel measures MAPS, not
##   opponents) or the 10-game ladder sample is lucky. **NOT SEPARATED.**
##   **Resolve the map axis before this panel decides anything.**
##
## ===== s28 STATE, READ LIVE OFF THE PLATFORM =====
##   **v104 live · 1641 · rank #27/116 · 685 matches · last-10 6W-4L.**
##   `slot_rule`: `k=39 net5=-17.0 armed=True slot_free=False` -> **HOLD**, and
##   this time on the FIRST condition (net5 -17 has not reached -21).
##   **net_act +26.0** against the 1615 activation baseline; peak 1698,
##   **drawdown -57**. `sprt_fast=BLEED` — the fast test is unhappy, the slow
##   one is OK. **Roll back to v102 only if rating < 1615 while net5 <= -21.**
##   Six monitors alive. Rate budget 0/5 spent, a slot free now.
##
## ===== ⛔⛔ LOKI-17 AND LOKI-18 ARE DEAD. BOTH. KILLED s28 22:03, `c91c078`. =====
##   **THE BLOCK BELOW IS THE 17:31 TEXT AND IT IS WRONG. IT IS KEPT, STRUCK,
##   BECAUSE THE WAY IT FAILED IS WORTH MORE THAN THE WORDS ARE.**
##   `c91c078` (2026-08-10 22:03:16) verbatim: *"No defect; LOKI-17 and LOKI-18
##   both dead."* **That is FIVE HOURS after this block was written, by the same
##   session, and this block was never updated. The s29 builder booted, read it,
##   ran the gate, picked cells, verified the tree, and got within one commit of
##   activating a prototype for a plank its own author had already withdrawn.**
##   Caught by the side lane reading the commit log, and independently by the
##   builder's own local run. **A HANDOVER BLOCK IS A CLAIM WITH AN EXPIRY DATE,
##   AND THE ONE THING A SUCCESSOR CANNOT DO IS NOTICE THAT IT EXPIRED.**
##   ⇒ **STANDING RULE, EARNED: a plank's death is written to HANDOVER IN THE
##   SAME COMMIT that kills it, or it is not written.** A wrap-time sweep is too
##   late — the next session boots on whatever is in the file at the time.
##
##   **WHY IT DIED, and this is the reusable part — it is a METRIC lesson, not a
##   plank lesson.** `raid.py` gates every sentinel build behind
##   `can_fire_from(...)`, and **LOKI-17 did not touch that guard.** So
##   shootable-on-build reads ~100% in the CONTROL arm too. The pre-registered
##   primary sat **causally downstream of an unchanged guard**: it could not
##   move, in either direction, for any implementation. Not a pre-satisfied bar
##   — an **inert** one. Confirmed twice on 2026-08-11: side lane by reading the
##   diff, builder by running both arms (forward subset **16/16 and 20/20**).
##   ⇒ **BEFORE PRE-REGISTERING ANY MECHANISM METRIC, ASK WHAT IN THE DIFF CAN
##     CHANGE IT. If the answer is nothing, the leg spends a window to learn
##     nothing.** This is the cheapest check in the repo and it is new.
##
##   **AND DO NOT REVIVE THE 50.4% / 62.2% / 67.6% BASELINES.** They are a
##   **45° angular tolerance** (`loki9_facing.py`, `ALIGNED_DEG = 45.0`) on
##   Ouroboros/Askar games. `tools/loki17_mech.py` computes **exact-ray
##   collinearity**. Different predicate — so **a reconciled-looking number
##   across the two is evidence of a units error, not a validation.**
##   **"Forward" also carries THREE incompatible definitions** across this
##   plank's evidence (`d2_own>41` n=327 · `d2_own>145` n=287 · midpoint
##   `d2_enemy<d2_own`). The **100.0% that killed the plank attaches ONLY to
##   `d2_own>145`.** All three are named in `tools/loki17_mech.py`'s comments.
##
##   **WHAT IS STILL GOOD HERE:** `bots/_v134loki17` is a clean, crash-safe
##   one-function diff and `tools/loki17_mech.py` now runs (it raised
##   `ValueError` on **every** invocation until 2026-08-11 — 4-tuple yielded,
##   3-tuple unpacked — so **no number in circulation came from it**; the 100.0%
##   came from `scratchpad/shootable.py`, **untracked**). If the closest-plant
##   idea is ever revived it needs a **NEW pre-registration on distance /
##   coverage / lifetime** — not an amendment, because the bar changes quantity.
##
## ~~===== WHAT s28 SHIPPED: NOTHING. WHAT IT BUILT: ONE PLANK AND SIX TOOLS =====~~
##   ~~**LOKI-17 = `bots/_v134loki17`** (md5 `8df01ffe`), prereg~~
##   ~~`docs/prereg/PREREG-loki17-sentinel-siting-2026-08-10.md` (`03d2314`~~
##   ~~17:27:01, tree 88s later — two-clock clean, bars unmoved).~~
##   ~~**NOT SHIPPED, NOT MEASURED.** Smoke-tested only: **0 uncaught exceptions**~~
##   ~~in 4 local games.~~
##   ~~**THE DEFECT:** our sentinel siting was FIRST-FIT... **the CHOICE was~~
##   ~~missing.**... only **52.1%** of our sentinels could fire on the round we~~
##   ~~built them.~~ **← THE 52.1% IS A 45°-TOLERANCE FIGURE. STRUCK.**
##   ~~**NEXT: the facing decoder replaces the 52.1% BASELINE. The >85% TARGET~~
##   ~~DOES NOT MOVE WITH IT.**~~ **← THERE IS NO NEXT. THE PLANK IS WITHDRAWN.**
##
## ===== LEGS: BOTH STOPPED, BOTH ABANDONED, NEITHER IS A RESULT =====
##   **LOKI-14b** killed at **8/16 matches** on a Magnus directive, between
##   cycles, holder verified. Below its own dose gate -> **no bar attaches, no
##   verdict language, and the decode against the 150-throw gate is WITHDRAWN.**
##   Survives as a yield fact: **8.8 throws/match vs LOKI-14's ~45.**
##   **PANEL2-CAL** stopped at **13/25**, **ABANDONED**: all five cells sit
##   outside the reachable band, and I had already seen its interim per-cell
##   numbers, so re-scoping it would have been post-data selection.
##   **Its interims must not be cited** (n=5/cell, sampling SD ~0.20).
##
## ===== THE MEASUREMENT THAT REFRAMED THE DAY =====
##   **The ladder only pairs neighbours: 94.0% of 678 matches within +-100, and
##   the highest-rated opponent we have EVER met is +64.1.** Reachable band
##   `us-80..us+125` = 18 teams. **And it scores GAME SHARE, not match wins:**
##   `delta = 32*(S-E)`, residual **0.000000** over 100 matches, verified twice.
##   **=> `tools/target_value.py` is the new gate. Run it BEFORE a prereg and
##   paste its `TARGET BAND:` line in.** On today's abandoned leg it reads
##   *"NO TARGET IS REACHABLE"* with a perfect 5-0 paying **1.18** points,
##   against **16-21** in band. **The machinery inspected the experiment and
##   never asked whether the question was worth answering.**
##
## ===== TOOLS ADDED s28 (all selftested to BOTH verdicts) =====
##   `target_value.py` (the gate) · `map_admits.py` (D34 map axis) ·
##   `rate_budget.py` (the 5-per-20-min meter — **and opponents challenge US,
##   so it attributes by our own match ids**) · `corpus_sanity` freshness ·
##   `submit_clean` loader lint (caught a real syntax error hours later) ·
##   `league_matches.py --update` wired into the keeper (**the corpus was 21h
##   stale while the daemon logged healthy**).

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

## ===== A STANDING SELF-CHECK FOR WHOEVER HOLDS THE VERDICTS =====
## **MY ERRORS RUN IN THE DIRECTION OF THE WORK I WANT TO DO NEXT.** Three in
## one session, all narrowing claims I had made about roads I wanted OPEN:
## the LOKI-14 null's scope, the MDE denominator (I checked only the direction
## that could embarrass me), and "the displacement trigger is untouched" (it
## was 164 interior throws at the climbing band, reading zero).
## **None was a calculation error; each was a check I did not run because its
## result would have been inconvenient.** The countermeasure that actually
## worked all three times was another lane re-deriving the ARITHMETIC rather
## than reviewing the REASONING. Ask for that on any verdict you want to be true.

## ===== ⛔ RETRACTED 16:3x — "THE CLIMB IS GATED ON OUROBOROS" WAS WRONG =====
## **MAGNUS CHALLENGED IT AND HE IS RIGHT.** *"we don't need to bother with
## Ouroboros anymore right? The ladder will keep kicking them down and we are
## trying to climb it."* Checked rather than agreed, and the data backs him:
## **the matchup is IMPROVING and we are pulling away.** Game share by OUR
## version era (`ladder_games.tsv`, 160 games): v5-v59 **14.3%** · v60-v79
## **18.5%** · v80-v89 **11.4%** · **v90+ 36.0%**. Last 4 matches 40.0%, last
## match (v102) **80.0%**. Rating gap +28.1 at first contact -> **-111 today**.
## **The -301 lifetime figure is REAL but dominated by the v53-v86 era.**
## **THE WORD THAT CAUSED IT: "flat".** The research arm relayed the matchup as
## "flat -- nothing we shipped touched it", compressing quartiles of
## **0.150 -> 0.175 -> 0.100 -> 0.314** whose own source said "flat-to-slightly-up".
## **A RISING FINAL QUARTILE COMPRESSED INTO ONE WORD IS WHAT MADE IT LOOK LIKE
## A STATIC COUNTER WORTH REORDERING THE QUEUE AROUND** -- and I reordered it
## without asking to see the quartiles.
## **The one part that survives, against Magnus's mechanism:** their rating ROSE
## 1469.7 -> 1558 (+89); **we simply climbed faster (1441 -> 1669, +228)**. So the
## separation is us improving, not them declining, **and it reverses if we
## stall.** 36% still sits under the ~48% Elo expectation (n=25, +-10pp), so a
## residual exists -- it is just not the largest thing on the board.
## **=> NOT the queue headline. No dedicated counter-plank.** The five-bleeder
## history stands; the Ouroboros-specific urgency does not.
##
## ===== (superseded) THE FIVE-BLEEDER FINDING, AS HISTORY =====
## **We are net-POSITIVE against everyone above us (+183.6) and everyone well
## below us (+416.7), and we BLEED to the teams just beneath: ranks 25-40 are
## -438.6 Elo and 58% of our match diet (72% recently).**
## **FIVE named teams, 162 matches, -875 Elo lifetime.** Removing just those five
## turns our recent record from +0.51/match into **+1.79/match**.
##
## | opponent | rank/rating | n | game share | expected | net |
## |---|---|---:|---:|---:|---:|
## | **Ouroboros** | #36 / 1558 | 31-32 | **0.168-0.188** | 0.482 | **-301 (-9.42/m)** |
## | Lunds Stallions | #27 / 1639 | 38-44 | 0.279-0.309 | 0.496 | -262.5 |
## | Powerpuff Girls | #29 / 1603 | 35-43 | 0.349-0.386 | 0.490 | -143.1 |
## | Kings College Munich | #33 / 1572 | 25-30 | 0.288-0.353 | 0.499 | -139.4 |
## | diverge | #26 / 1659 | 5-13 | 0.43-0.52 | 0.500 | -28.9 |
## *(two ranges = builder's corpus cut vs research's platform cut; same shape)*
##
## **OUROBOROS IS THE SINGLE LINE THAT MATTERS. Match record 2-29/3-29. Game
## record ~30-130, share 0.168-0.188 against an expectation of 0.482 — they are
## ~300 points better against US than their rating says. THEY HAVE BEEN ON
## VERSION 8 SINCE 2026-08-06 while we shipped ~24 versions across those games.**
## A stable hard counter, sitting still, ~160 archived games on disk, **inside
## the reachable band (-111)**, and **nobody has ever gone after it.**
## **AND IT INDICTS TODAY: we spent the session building an exploit for teams
## 550-860 BELOW us while a -301 Elo matchup 111 below us sat on the same bot for
## four days.**
## **NEXT ACTION: a replay study of the ~160 archived Ouroboros games — what
## kills us, in what round band — then a pre-registered counter-plank.** It pays
## on the currency Magnus named, needs no exploit, and the target cannot move.
##
## **NOT a broad decline: the low band is IMPROVING** (+0.031 game share per 100
## matches, t=+2.69; ranks 25-40 by day -2.42 -> -1.17 -> -0.76 -> +1.69
## Elo/match). Magnus's worry is measured and answered in the negative.
## **The counter-shipping hunt found NO culprit and killed its own instrument
## correctly:** apparent "declines" correlate r=-0.721 with first-half S-E, i.e.
## regression toward parity, because E absorbs the very results being scored.

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
##    **THE ROAD STILL OPEN: the DISPLACEMENT / stale-plan trigger** — but
##    **"UNTOUCHED" WAS AN OVERSTATEMENT AND IS RETRACTED.** Every number in the
##    cut is OBSERVATIONAL (builders that WALKED to a border), so it says
##    nothing about displacement — **however LOKI-14's INTERIOR arm was 164
##    displacement throws AT THE CLIMBING BAND and returned ZERO.** Not a
##    closure (a short throw may leave the cached plan valid, and that arm was
##    built as a PLACEBO, never dosed as a displacement treatment) — but not
##    nothing. **LOKI-14c must answer those 164 in its PROVENANCE line**: what
##    distinguishes its treatment from an interior arm that already read zero
##    where we care. If the answer is throw DISTANCE, that is a dose parameter
##    and must be pre-registered as one.
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
