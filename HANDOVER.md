# LIVE: **v104 = "Loki v2"**. s29 WRAP, 2026-08-11 07:4x CEST (05:4xZ).

## ===== ⭐ BOOT: RUN THESE THREE BEFORE ANYTHING =====
##   1. `.venv/bin/python tools/plank_status.py --all`  — **NEW s29.** Gate on the
##      `PLANK_STATUS:` line, never on `$?` (behind a pipe `$?` is the pipe's).
##      It exists because I got ONE COMMIT from activating a plank its own author
##      had withdrawn five hours earlier.
##   2. `.venv/bin/python tests/test_instruments.py` (34/34 at wrap)
##   3. `.venv/bin/python tools/corpus_sanity.py`
##   **`tools/freshness.py --selftest` is new too — see the queue.**
##
## ===== STATE, VERIFIED ON THE PLATFORM AT WRAP =====
##   **LIVE: v104 "Loki v2" = `bots/_v130loki13`, py-tree md5 `798d2df4`.**
##   **1680, rank #23/117, 728 matches. last-10 3W-7L.**
##   `RULE=held` · net_act **+65** · peak 1698 · drawdown **−18** ·
##   `sprt_fast=BLEED` `sprt_slow=OK`. **ACTIVATION BASELINE 1615.**
##   **ROLLBACK TARGET: v102 = `bots/_v124loki8`**, md5 `e8697ffa`,
##   `.venv/bin/fcode submission activate 102`. **Roll back only if rating < 1615
##   AND net5 <= −21.** Neither is close.
##   ⚠ **A STATE BLOCK IS AN EXPIRY DATE, NOT A GUARANTEE. Re-read it live.**
##
## ===== ✅ `breakin_watch` IS DOWN AND THAT IS CORRECT — STOP RE-FLAGGING IT =====
##   Raised as an unrepaired monitor by BOTH other lanes today. It is not.
##   Its docstring: it guards a fresh ship's first 8 matches and **"hands back to
##   the slot rule at k >= 8; exits when it does."** v104 is at **k=82** — it
##   exited because it was FINISHED. **Re-arm it before the next
##   ACTIVATION-AS-A-SHIP, not before an unrated leg** (a leg activates ~20s and
##   rolls back; there is no break-in window to guard).
##
## ===== ⛔ NOTHING IS WATCHING OVERNIGHT EXCEPT THE MONITORS =====
##   7 monitor processes alive at wrap (4 watchers + keeper + ship_watch + loop).
##   **NO runner is live. NO auto-rollback is armed. `ship_watch` will WRITE
##   `corpus/SHIP_ALERT` if its conjunction fires and NOBODY WILL READ IT until
##   someone boots.** That is the same accepted risk as last night.
##   **MORNING: read `corpus/SHIP_ALERT` and `tail corpus/ship_watch.log` FIRST.**
##
## ===== ⛔⛔ LOKI-18 — I FIRED 25 GAMES ON A PLANK ITS OWN AUTHOR KILLED TWICE =====
##   **`docs/legs/LEG-loki18-void-and-the-live-closure-2026-08-11.md`.**
##   VOID ON PREMISE. `c91c078` (2026-08-10 22:03Z) retracted the 0/319 baseline
##   — the delta table had omitted CENTRE=0 and rotated every facing one step —
##   and `38bc735` re-confirmed it dead at 06:08Z. **My Amendment 1 at 06:45Z
##   reinstated the retracted number, forbade its revision, and cited the
##   correction zero times.** Side lane caught it ~70 s after the window closed.
##   **COST: one unrated window + one submission slot (v109). RATED COST ZERO** —
##   8 consecutive pairings all v104, verified per-match **ON THE LIVE CLI**.
##   ⛔ **`league_matches.tsv` STOPPED AT 05:52:59Z AND COULD NOT SEE THE 06:46
##   WINDOW. The corpus lags the platform by up to an hour ⇒ ANY SAME-SESSION LEG
##   CERTIFICATION READS THE LIVE CLI, NEVER THE TAPE.** My own "verified at the
##   boundary" was a STRUCTURAL argument, not a per-match one.
##   **⭐ WHAT THE WASTED WINDOW BOUGHT — prediction committed BEFORE measuring:**
##   treatment **39/39 = 100.0%**, control **229/229 = 100.0%** shootable-on-build
##   (`d2_own>145`, the definition NAMED because `11bcb6d` records three
##   incompatible ones). **Known-answer control: rotate one compass step → 0/39
##   and 0/229.** ⇒ **LOKI-17/18 CLOSED WITH LIVE-GAME BACKING** on 268 sentinels
##   over 122 games. The bar was **INERT**, not pre-satisfied. Do not reopen.
##   **⭐ FIVE INDEPENDENT DEFECTS LANDED ON ONE OF FIVE CELLS TODAY** (SmartFridge:
##   arrival precondition · version churn · seat inversion · most-favourable 5d
##   number · no version-matched control). **The panel criterion is RATING
##   PROXIMITY and it selects for nothing a mechanism needs.**
##   ⛔ **`plank_status.py` RAN AT BOOT ON THIS PLANK AND SAID NOTHING** — HANDOVER
##   had never mentioned loki18, so it exited at UNMENTIONED before the kill
##   scan, and **a recency check reads a withdrawal commit as FRESHNESS.**
##   **FIXED s30:** whole-history scan, word-boundary patterns, `PLANK-REVIVED`
##   token, a **SUSPECT** tier and `tools/plank_ack.tsv`. Both prose-matching
##   mistakes are fixtures now: `core_kill_share` flagged our **LIVE INCUMBENT**,
##   and a VOID commit containing "reinstated" **cleared the plank's death**.
##   **⇒ `PLANK_STATUS: WITHDRAWN` IS NOW A REAL VERDICT. GATE ON IT.**
##
## ===== ✅ LOKI-19 — READ OUT s30. BAND 2. NOTHING SHIPS. =====
##   **`docs/legs/LEG-loki19-core-peck-readout-2026-08-11.md` (`888d699`).**
##   §6 row 2 verbatim: **"dose delivered, mechanism measured, currency
##   unresolved at this n."** "null"/"refuted"/"fails" FORBIDDEN in this band and
##   not used. **5d = Amendment 3c row 4** (point ABOVE control +0.0289, CI
##   [−0.1381, +0.1816]) → no claim. **`bots/_v136loki19` is NOT a ship
##   candidate on this evidence and v104 stays live.**
##   * **5a DOSE GO:** 192.90 core-pecks/game, 44/50 games; control **EXACTLY
##     0.00 across all 50**. And `our_core_atk == our_total_atk` in every cell —
##     §4's gate-completeness claim confirmed LIVE, not enumerated.
##   * **5c:** core-kill share 36.0% vs 48.0% = **−12.0pp against a 28.0pp MDE.**
##   * **5a-bis GATE DID NOT RESOLVE** (19 events over 50 control games; Askar's
##     lower bound 30.06%). ⇒ **the leg does NOT claim to have tested the changed
##     premise.** An unresolved gate defaults to the RESTRICTION.
##   **⭐⭐ THE SURPRISE, AND IT IS THE MOST VALUABLE THING THE LEG PRODUCED:
##   THE PECK LANDS AND THEY ANSWER IT WITH HEALING, 5 CELLS OF 5** (median
##   23 → 287 HP/game). Damage +342.7/game, their healing +370.1/game, **net
##   −27.4/game.** A peck is **2 Ti for 2 dmg**; a heal is **1 Ti for +4 HP** —
##   **4× against us, and it costs them no raider's position.** ⇒ the peck's
##   problem may not be that it costs a move; **2 damage may simply sit under
##   their heal rate.** HYPOTHESIS, not a finding — no live test, and
##   `scratchpad/hp_ledger.py` has NO SELFTEST (its first output was wrong by
##   10^19; kept only because the corrected walk reproduces `leg_read`'s
##   core-kill counts 18/50 and 24/50 exactly, by a different path).
##   **⛔ CONFOUND NOBODY PRE-REGISTERED: THE SEAT MIX DIFFERS IN ALL FIVE
##   CELLS**, SmartFridge a complete inversion (10×B vs 10×A). Disclosed, NOT
##   corrected — a seat-matched estimator would be chosen after seeing the data.
##   Map mix differs too. **Any future pooled reading of this leg inherits both.**
##   **D18: Askar v94 / Lunds v64 / farming v13 PINNED; SmartFridge pinned
##   THINLY** (4 versions in the 4.5h before the window, in-window on n=2 rows) —
##   read off `league_matches.tsv` directly, **never `oppver_window`**, which
##   returns CLEAN off a stale tape.
##   **RATED COST ZERO**, at the PAIRING BOUNDARY (4/4 pairings v104), not the
##   match counter. Lock cert: Amendment 3 lands **34 s** before the first
##   treatment game — blind, and the margin is that thin.
##
## ===== ✅ LOKI-16b CLEARED ITS BAR (read out s29) =====
##   **+0.164 [+0.073, +0.253]** on the 12-ring stratum vs **+0.15**.
##   Amendment 2c row 1 verbatim; **"confirmed" is forbidden and is not used.**
##   **The statistic choice was the deciding call and was made BLIND** (per-tile
##   +0.164 clears, the other series misses; chosen on the bar's PROVENANCE at
##   06:15:21, the blind replication launched 06:08:52).
##   **CORRECTION 1 in that prereg: the row published as `hold_any` is a THIRD
##   statistic — `ring_read.py` computes no `hold_any` at all.** Primary and
##   verdict unaffected.
##   **A confirmation leg is now justified. The prereg's own fork is open:
##   retention cleared, KILL-SPEED WAS NOT READ.**
##
## ===== ⛔ FOUR THINGS FROM RESEARCH'S WRAP — DO NOT INHERIT THESE UNCHECKED =====
##   **Carried HERE and not left in their docs, because today's most-repeated
##   failure (D14, three firings) is that a correction lands where it was
##   DISCOVERED and never where it will be READ.**
##   1. **The v95–v101 melee transition zone is UNRESOLVED, and research was
##      wrong about it TWICE.** `bde1627` Part 9 says "resolved"; **`e96371e`
##      Part 10 SUPERSEDES it.** ⛔ **Do not let "nineteen healthy versions, then
##      the flag" back into circulation** — v98 was submitted 20 minutes BEFORE
##      the LOKI-QUIET tree existed and still reads 0.0%. The current tree's gate
##      is established by exhaustive enumeration; the HISTORY is not.
##   2. **Team 48 is a MECHANISM lead, not a currency target.** Unrated S−E
##      −0.147, **rated +0.107 on n=2 matches**, both confounds dead. Real gap
##      (they kill r93, we need r140), 2.7% of v104's rated diet.
##   3. **Kidnap effectiveness has NO column in `throws.tsv`.** A DECODER GAP,
##      **never a null.** Prerequisite if the kidnap line comes back up.
##   4. **The map × opponent interaction CANCELS in every pooled statistic we
##      compute** — pooled share by map is flat 0.485–0.633 and that flatness
##      averages a ±0.3 within-map spread. kladde 10x10 0.82 vs bigger 0.23
##      (p=0.0005); Landers the exact mirror. **This is about our whole
##      measurement practice, not about v104.**
##
## ===== ⚠ TWO SIZING FACTS LOKI-19's READ-OUT MUST NOT GET WRONG =====
##   * **The primary's baseline is 2,247-scale, NOT the rated-only 475.**
##     Sizing n against 0/475 over-buys games by 4.7x.
##   * **The arrival figure carries its POPULATION or it is a different number:**
##     **38.1% rated-only vs 23.3% pooled**, range 18.2–40.9% across v102–v107.
##     Amendment 1 tags it; a read-out that recomputes on another population is
##     testing a different bar.
##
## ===== ⛔⛔ MAGNUS, s30 06:4xZ — A LEG MUST ALWAYS BE READY =====
##   *"We are leaving unrated games unplayed, games that could potentially find
##   something that surprises."* · *"When there's a free slot to run unrated games
##   we should have experiments ready to test one or many hypotheses or an
##   experimental new bot."*
##   ⇒ **A PREREG'D, DOSE-VERIFIED, PLANK-STATUS-CLEAN CANDIDATE IS A STANDING
##   OBLIGATION, NOT A PER-SESSION TASK.** `rate_budget.py` says a slot is free
##   roughly every 20 minutes and they are free.
##   ⛔ **AND THE COUNTER-LESSON FROM THE SAME HOUR: SPEED IS WHAT PUT 25 GAMES
##   INTO A DEAD PLANK.** "Ready" means the checks are ALREADY DONE, not skipped.
##   **Run `plank_status.py <plank>` and require OK — not "not stale".**
##
## ===== QUEUE, IN PRIORITY ORDER (rebuilt s30 after the LOKI-19 read-out) =====
##   0. **THE NEXT LEG — build it BEFORE the slot is free, per the block above.**
##      **Best candidate on today's evidence: the HEAL-RATE plank (queue 3).**
##      Do NOT reach for a built tree with a committed prereg without running
##      `plank_status` first; that is exactly how LOKI-18 got fired.
##   0b. **BUILD THE D42 CHECKER — routed, and its acceptance fixture already
##      exists on disk so nothing needs inventing.** A prereg must NAME the
##      `file:line` its mechanism metric reads; the checker asserts that path
##      appears in the treatment diff. **NEGATIVE CELL: LOKI-18 Amendment 1 MUST
##      FAIL** (metric reads `raid.py`'s guard, diff touches only `main.py:560`).
##      **POSITIVE CELL: LOKI-19's 5a dose bar MUST PASS.** Without the positive
##      cell a checker that fails everything looks correct. **D42 was violated by
##      its own author 2 h 37 m after writing it — that is the `name_check.py`
##      signature and it is why this jumps the queue.**
##   1. **`corpus/our_matches.tsv` — THE MATCH-INITIATIVE LEDGER.** ✅ **BUILT AND
##      LIVE s30** (`tools/match_ledger.py`, wired into `unrated_run.sh`, which now
##      REFUSES TO FIRE if the ledger is blind). 5 rows on its first leg, 5/5
##      attribution against the platform. ⚠ **The FOREIGN-challenge direction is
##      still UNTESTED — no foreign challenge has landed since it shipped, and a
##      zero on a minutes-long denominator is not evidence.** Remaining work:
##      point `rate_budget.py:77` at it instead of the regex scrape.
##      *(Original justification retained below.)* Magnus's own
##      ask, spec at `docs/research/SPEC-match-initiative-ledger-2026-08-11.md`
##      (`314d326`). **Deliberately ranked ABOVE the freshness work, and here is
##      the reason: the freshness fix repairs an alarm that failed to summon an
##      audit — and the audit happened anyway today, twice, by two lanes. The
##      ledger fixes a meter whose failure SILENTLY STALLS EVERY RUNNER.** s28's
##      meter read **7 of 5** and was caught only because 7-of-5 is
##      arithmetically impossible; ONE foreign challenge reads a plausible 5/5.
##      **A wrong-but-plausible reading outranks a missed alarm.** Today the
##      attribution is `rate_budget.py:77` regexing `matchId` back out of
##      untracked scratchpad files. **Two selftests are non-negotiable: a
##      REJECTED challenge must still write a row** (rejections consume budget)
##      **and the blind state must REFUSE, not permit.**
##   2. **`audit_trigger`'s `cross_lane_analysis` ROW — the ONE genuinely
##      suppressed signal.** Two lanes converged on this independently today.
##      Numerator windowed to 24h off git; denominator is *the last 50 tape rows
##      with no clock at all* — `results.tsv` HAS NO TIMESTAMP COLUMN, so it
##      cannot be windowed in place. **`results.tsv` has had ZERO rows in 24h
##      (newest commit `4ad19ab` 2026-08-09T18:38:18Z, 35.6h).** As shipped
##      47/21 = 2.29 ok; same-window **47/0 = 47.00 against a threshold of 4.0 →
##      TRIP.** On a day with 47 new analysis docs and zero recorded decisions,
##      the row built to catch exactly that reads `ok`.
##      **⛔ AND "ONE HELPER, FOUR BUGS" IS WRONG — it is 2 clean fits
##      (`oppver_window`, `ship_watch`), 1 NECESSARY-BUT-NOT-SUFFICIENT
##      (`audit_trigger`: even on a fresh tape this row divides 24h-of-docs by
##      50-rows-of-tape, different populations — freshness makes it REFUSE when
##      stale, it does not make the ratio mean anything when fresh), and 1
##      MISDIAGNOSIS (`breakin_watch`'s named defect is selftest fidelity — its
##      selftest duplicates `main()` and the `k>=8` stand-down branch is in NO
##      test; its real freshness defect is gating on `TAPE.stat().st_mtime`, the
##      clock `freshness.py`'s own docstring calls the wrong one). **Fix them as
##      four different bugs, not one wiring job.**
##      **⛔ AND DO NOT ACT ON `doc:code churn`. IT IS A BAD ROW.** Recomputed at
##      six window offsets: 20h 1.0043 TRIP · 22h 0.9536 ok · 24h 0.9333 ok ·
##      26h 1.0279 TRIP · 28h 0.9939 ok · 30h 1.0691 TRIP. **No trend — it
##      hovers on its own threshold, so the verdict is set by WHEN YOU RUN IT**,
##      and it prints `{val:.2f}`, so `1.00` renders on both sides of a 1.0
##      threshold and only the TRIP/ok tag discriminates. Its anchors are 0.14
##      vs 1.88 and today sits in the dead zone with no resolution. **~43% of
##      the numerator is `coordination.md` (4,517 lines), `HANDOVER.md` (1,109)
##      and three preregs (1,692) — artefacts this repo's method REQUIRES. A leg
##      run correctly RAISES this signal.**
##   2b. **⛔ EVERY PER-OPPONENT NUMBER IN THIS REPO READS HIGH — research, s30.**
##      League-wide, 4,157 blocks with each team's own bot frozen: a team scores
##      materially LESS against an opponent's LATER versions. Direction and
##      significance replicate across four estimators (all t < −13); **the
##      magnitude does NOT — it spans 1.8x, so treat it as order 5-9pp and
##      NEVER apply a numeric correction.**
##      **AND THE REPAIR IS NOT EXECUTABLE: 419 of our 599 matches (69.9%) were
##      played against a version the opponent no longer runs**, and conditioning
##      leaves n=1 or 2 in every LOKI-19 panel cell (Lunds "80%" off ONE match).
##      **The conditioning is well-powered exactly where it is unnecessary.**
##      ⇒ **STOP QUOTING PER-OPPONENT SHARES TO A DECIMAL** — including in target
##      bands. ⇒ **PREFER CELLS WHERE THE OPPONENT IS STABLE OVER CELLS WHERE OUR
##      SAMPLE IS LARGE. Those are nearly opposite properties right now**, and
##      only **Ouroboros and OopsGotYourElo** have stored statistics that describe
##      the bot we would actually meet. That is a free panel criterion nobody has
##      applied, and it is the sixth arrival of "rating proximity selects for
##      nothing a mechanism needs".
##      ⇒ `ladder_games.tsv.oppver` is NULL, so anything computing a per-opponent
##      number off it is blind to this BY CONSTRUCTION. Use `league_matches.tsv`
##      or the `replay_archive/*.meta.json` sidecars.
##      **DEPLOY-CADENCE SNIPING: BOTTOM OF THE QUEUE — *NOT* CLOSED.**
##      Fresh opponent versions measure STRONGER (matched DiD +0.524, t=+4.89);
##      the naive +1.25 is mean reversion because **teams ship when they are
##      losing**. ⛔ **AND THE FIRST VERSION OF THIS BULLET SAID "refuted, saves
##      a leg", WHICH WAS D12 VIOLATED IN A BOOTED FILE BY ME.** The statistics
##      are sound; the modal word was not. **This rests on ARCHIVE STATISTICS
##      WITH A BEHAVIOURAL PREMISE — how an opponent's versions perform — which
##      is exactly the evidence class D12 forbids retiring a road with.** No leg
##      has ever been aimed at a fresh version. Archive evidence sends a road to
##      the BOTTOM OF THE QUEUE, never off it.
##      ⇒ **CHEAP CONVERSION IF ANYONE WANTS IT GENUINELY CLOSED: one leg fired
##      at a cell inside its first hour post-ship.** The matched DiD design
##      already exists; version-stability counts off `league_matches.tsv` say
##      which cells re-version often enough to schedule it — the same tape that
##      produced the Focalground nomination.
##      *(The **rollback-excursion bias correction is unaffected and stands**:
##      excursion games make rivals look weaker, so our cells read optimistic
##      from a second independent direction alongside the pooling bias. That is
##      a statement about OUR OWN stored statistics, not about an opponent's
##      behaviour, so D12 does not reach it.)*
##   2c. **⭐⭐ SENTINEL SITING — THE ONE LEAD TODAY THAT COULD BE A PLANK, AND ITS
##      TWO PROSPECTIVE FLAGS. `docs/legs/` none yet; tape row `sentinel-siting`.**
##      Our sentinels have an enemy in their firing ray **20.91% of alive-rounds
##      vs the field's 48.89%**, while CONVERTING an available target BETTER
##      than they do (**39.35 vs 32.60** per 100 opportunity-rounds) and
##      declining a shot a third as often (**1.63% vs 4.90%**). Two independent
##      decoders on the never-fire rate; the attribution is ONE decoder with 15
##      forced-answer fixtures and a live opponent control.
##      ⇒ **THE PLANK IS NOT "SHOOT MORE". IT IS "PUT THE TURRET WHERE SOMETHING
##      WALKS".**
##      **⛔ FLAG 1 — THAT SENTENCE FORKS ON `PLAY_DEFENCE: never`, AND THE EASY
##      BRANCH IS THE FORBIDDEN ONE.** Enemy units are most available WHERE THEY
##      COME TO US — our approaches, our collar. **A siting change that raises
##      availability by covering our own ground is HOME DEFENCE and is
##      off-programme no matter how well it measures.** The legal branch is to
##      site FORWARD, near THEIR core, to open a lane to it. **Both raise the
##      pooled availability statistic identically, so the pooled 20.91% CANNOT
##      TELL THEM APART.** ⇒ any prereg here states which branch it tests and
##      carries availability measured **at d² from THEIR core**, never pooled.
##      **✅ MEASURED, AND IT LANDED THAT WAY. THE ON-PROGRAMME BRANCH IS DEAD.**
##      US FORWARD n=3,341 availability **83.18%** vs OPP FORWARD **89.72%** —
##      **a 6.5pp gap, not 28pp. Our forward sentinels are already
##      near-saturated and there is almost nothing to buy there.**
##      US HOME 10.26% vs OPP HOME 23.44%, and **MIX: we sit 51.4% HOME against
##      their 31.1%.** ⇒ the pooled gap is (a) HOME availability, which is home
##      defence and off-programme to fix, and (b) mix.
##      **⭐ THE ONE SURVIVING ON-PROGRAMME READING IS THE MIX, and it is the
##      directive restated rather than a loophole: our HOME sentinels fire 4.04
##      shots/100 alive-rounds against 32.74 forward — 8x less productive — at
##      30 Ti and a permanent +20% cost-scale contribution each. The plank is
##      not "defend better", it is "STOP DEFENDING".**
##      **⛔⛔ AND THE FENCE ON IT IS NOT "NEEDS A BIGGER n" — IT IS A SELECTION
##      EFFECT THAT MAY NOT TRANSFER AT ANY n.** 4.04-vs-32.74 compares turrets
##      in different POSITIONS. Reading it as *"move them forward and they fire
##      8x more"* assumes productivity is a property of the **position** rather
##      than of **the conditions that produced the siting**. A home sentinel
##      exists because at that moment forward siting was not available or not
##      survivable; **the forward ones may be forward BECAUSE conditions allowed
##      it.** That is the SAME independence assumption the availability-binned
##      test just falsified for conversion (69.82 → 26.68 as availability rises),
##      one level down, inside the only reading that survived the fork.
##      ⇒ **Before this becomes a prereg it needs a design that breaks the
##      selection — e.g. compare home sentinels that COULD have been sited
##      forward against those that could not — not more games.** NOT
##      pre-registered, NOT sized, and the sizing limit on the attribution
##      instrument also still stands.
##      ⛔ **AVAILABILITY IS A LOWER BOUND AND THE ARTEFACT IS *NOT*
##      COMMON-MODE — MEASURED, s30.** End-of-round snapshot, so a target
##      entering and leaving inside one round is invisible. Sentinels reading 0%
##      availability yet firing: **OURS 46/6,869 = 0.67% · THEIRS 4/4,280 =
##      0.09% — a 7.17x asymmetry AGAINST US.** (Broader 0-availability counts:
##      600 vs 176, 8.7% vs 4.1%.) **So it suppresses OUR availability harder,
##      which is the direction that erodes the 6.5pp forward gap.**
##      **⚠⚠ AND THE DISCRIMINATOR IS ONE-SIDED BY CONSTRUCTION, WHICH IS THE
##      PART THAT MATTERS: it can only see ghosts that FIRED. A transient target
##      that was never shot at leaves NO TRACE AT ALL.** So the bound it gives —
##      ghost shots are 101 of all our shots, **0.097%** — bounds the FIRING
##      side only. **It does NOT bound the availability side, and availability is
##      the quantity in dispute.** ⇒ **the 6.5pp forward gap survives on the
##      firing evidence and is NOT established on the availability evidence.**
##      Anyone re-opening this needs a within-round occupancy trace, not a
##      snapshot. `scratchpad/symm.py` reproduces the discriminator.
##      **✅ AND THE TRACE IS BUILDABLE — THE WIRE IS AN ORDERED EVENT STREAM,
##      NOT A PER-ROUND SNAPSHOT.** `replay_schema.md:47`:
##      `message Turn { repeated Update updates = 1; }` — `repeated` is ordered,
##      and `moveBuilderBot`/`fireTurret`/`removeEntity` are all sequenced inside
##      a turn. **So availability has NO permanent ceiling and this is a cost
##      question, not a structural one.** Written down so nobody re-derives it,
##      and so this is never filed beside the kidnap DECODER GAP, which it is not.
##      **⭐⭐ AND THAT READ PARTLY REVERSES MY OWN 7.17x, AGAINST MY INTEREST:**
##      **a builder bot moves AT MOST ONE STEP PER ROUND**, so "enters and leaves
##      a ray by moving inside one round" is **impossible for a single unit**.
##      The transient-target story therefore requires the target to DIE (or a
##      building to be built and destroyed) in that round — and **death-in-round
##      is real and common: 9.07% of 170,109 turret shots in a 600-replay slice
##      land on a tile that ALSO saw a `removeEntity` that same round.**
##      ⇒ **the ghost cases are plausibly KILLS rather than missed opportunities,
##      which inverts the direction of the concern — a sentinel that fired and
##      erased its own target reads as "0 availability" BECAUSE it worked.**
##      **✅ ATTRIBUTED, CASE BY CASE, 50 CASES: `scratchpad/ghost50.py`.** For
##      every ghost sentinel, did a `removeEntity` land on ITS ray in the round
##      it fired? **OURS 44/46 = 96% KILLS, 2 blind. THEIRS 4/4 = 100% kills.**
##      ⇒ **THE GHOSTS ARE KILLS, NOT BLINDNESS. The mechanism is settled.**
##      **⭐⭐ AND THE CORRECTION TO THE 6.5pp GAP IS ROBUST TO WHICH MECHANISM
##      WON, WHICH IS STRONGER THAN "TWO READINGS, NEITHER ESTABLISHED":**
##      **under BOTH readings a target WAS present in those rounds** — otherwise
##      there is no shot to have observed — **so availability is undercounted
##      either way, and 7.17x more often for us than for them.** Blindness and
##      kills disagree about WHY we undercount and agree that WE UNDERCOUNT
##      MORE. ⇒ **the true forward gap is SMALLER than 6.5pp, possibly zero,
##      possibly inverted.** A reader told the mechanism is contested must not
##      conclude the correction is contested; it is not.
##      ⛔ **MAGNITUDE STILL NOT ESTABLISHED, AND DERIVING IT HERE WOULD BE THE
##      FIFTH BOLTED-ON INFERENCE OF THE DAY.** The attributed subset is 46
##      sentinels of 6,869. The tempting generalisation — *every in-round kill
##      undercounts that sentinel's availability that round, and 9.07% of all
##      shots coincide with a same-round removal* — is a MECHANISM, not a
##      measured correction. **Do not adjust 83.18%/89.72% by any number derived
##      from it.**
##      **AND OUR FORWARD POPULATION IS BIMODAL: 3,331 of 3,341 sit at
##      d²_enemy ≤ 32 — parked at the doorstep — with ZERO beyond 100.** No
##      mid-distance population exists, so there is no availability curve to
##      climb.
##      **✅ FLAG 2 (the 19.24 counterfactual) IS VINDICATED BY MEASUREMENT:
##      conversion is NOT independent of availability.** Binned on our own
##      sentinels: (0-10%] 69.82 · (10-25%] 51.23 · (25-50%] 32.30 ·
##      (50-75%] 26.68 · (75-100%] 37.20. **At the field's pooled 48.9%
##      availability our own conversion reads 26.7-32.3, BELOW the 39.35 the
##      counterfactual used. ⇒ 19.24/100 OVERSTATES and is retired as a
##      forecast.**
##      **⚠ FLAG 2 — "at their availability and our conversion we would fire
##      19.24/100" IS AN UPPER-BOUND SKETCH, NOT A FORECAST.** It multiplies two
##      rates measured on opposite sides of a 2.3x gap and assumes **conversion
##      is independent of availability**, which is untested — a unit transiting
##      a lane is not the same kind of target as one that wandered into a quiet
##      corner, so conversion could FALL as availability rises. **Anything sized
##      off 19.24 inherits an untested independence assumption.**
##      **⛔ SIZING LIMIT (recorded in the side lane's booted drift-watch file at
##      my own request): the RATE is two-path, the ATTRIBUTION is one decoder on
##      one population. Nothing may be SIZED off 20.91%/48.89% until a second
##      path reproduces the availability figure.**
##      **AND IT IS A CORRECTNESS FIX, NOT A TRICK** — a sentinel that never
##      fires is 30 Ti plus a permanent +20% cost-scale contribution buying
##      nothing. Instrumental under `KILL_WINDOW_RND`; **not a Loki lever and it
##      must not be dressed as one.**
##   3. **THE HEAL-RATE PLANK — LOKI-19's §11 turned into a question.** If 2
##      damage sits under their heal rate, the plank is not "peck" but **a dose
##      that clears +4 HP/builder-turn, or a target that cannot be healed.**
##      Prereg it properly; §11 is a HYPOTHESIS with no live test and
##      `hp_ledger.py` has no selftest. **Research has been asked to reproduce
##      the healing asymmetry with a forced-answer decoder — that is worth more
##      than another window of games.**
##   4. **LOKI-16b confirmation leg** (`tools/unrated_run.sh 106 <games>`).
##      **Before firing it, check `unrated_run.sh` for the boundary-guard shape
##      the side lane found in `loki19_treat_w1.sh`: the pairing wait runs ONCE
##      AT THE TOP, so a re-run's second activation never passes through it.**
##      The wait belongs INSIDE the retry path.
##   5. **Launcher chains** — still demoted: a six-link express lane delivering
##      bodies that provably do not attack on arrival spends +60% permanent cost
##      scale to move the same zero forward.
##   6. `docs/research/SPEC-mutation-harness-2026-08-11.md` — commissioned by
##      Magnus, unbuilt. Signature **5 BLIND / 1 CAUGHT**.
##   **⭐ NEW STANDING RULE, from the read-out: A PREREG'S RESOLUTION TABLE MUST
##   INCLUDE EVERY *GATE*, NOT ONLY EVERY *BAR*.** LOKI-19 §6 tabulated what
##   resolves at n=50 for all four bars and never asked it of gate 5a-bis —
##   which then arrived under-resolved and decided what the leg may claim.
##   **AND: A BAR THAT NAMES A PHYSICAL QUANTITY STATES ITS CEILING.** §5b said
##   "HP removed" and computed gross damage dealt; the gap was invisible until
##   the number exceeded a physically possible one.
##
## ===== TOOLS ADDED s29 — all selftested to BOTH verdicts =====
##   `plank_status.py` (HANDOVER vs artefacts) · `unrated_run.sh` (**the runner
##   for every unrated leg — do NOT hand-roll one**) · `freshness.py` ·
##   `ring_read.py` tracked + 11-cell selftest whose declared mutant FAILS it ·
##   `ring_retention.py` **REFUSES TO RUN** (wrong, and its selftest passed) ·
##   `loki17_mech.py` fixed (it raised ValueError on EVERY invocation) ·
##   `corpus_sanity` conditional-dead check · `rate_budget` persisted ledger ·
##   `submit_clean` restores the holder.
##
## ===== s29 DETAIL BELOW; s28 BLOCK FURTHER DOWN =====
## ===== ⭐ s29 — READ THIS BLOCK BEFORE THE s28 ONE BELOW IT =====
##   **LADDER: v104, ~1663-1678, rank #24-25/117, ~724 matches. `RULE=held`,
##   net_act ~+48, peak 1698, drawdown -35. NO ROLLBACK. Nothing was shipped.**
##
##   **⭐ FIRST: `.venv/bin/python tools/plank_status.py --all`. NEW, AND IT
##   EXISTS BECAUSE OF THIS SESSION'S NEAR-MISS.** I booted, read this file, ran
##   the target-value gate, picked cells, verified a tree, and got **one commit
##   from activating LOKI-17 — withdrawn by its own author five hours earlier**
##   (`c91c078`). The block saying it was next was written at 17:31; the kill
##   landed at 22:03. **A HANDOVER BLOCK IS A CLAIM WITH AN EXPIRY DATE AND THE
##   ONE THING A SUCCESSOR CANNOT DO IS NOTICE THAT IT EXPIRED.**
##   ⇒ **STANDING RULE: a plank's death is written to HANDOVER IN THE SAME COMMIT
##     that kills it, or it is not written.** A wrap-time sweep is too late.
##
##   **⭐ AND THE RULE THAT WOULD HAVE SAVED THE MOST TIME TODAY:**
##   **BEFORE PRE-REGISTERING A MECHANISM METRIC, ASK WHAT IN THE DIFF CAN CHANGE
##   IT. IF THE ANSWER IS NOTHING, THE LEG SPENDS A WINDOW TO LEARN NOTHING.**
##   LOKI-17's primary sat downstream of an `can_fire_from` guard it never
##   touched — ~100% in BOTH arms. Not pre-satisfied: **inert**.
##
## ===== ✅ LOKI-16b: READ OUT, AND IT CLEARS ITS BAR =====
##   **+0.164 [+0.073, +0.253]** on the 12-ring stratum vs a **+0.15** bar, CI
##   lower bound above zero. Amendment 2c row 1, verbatim: *"clears the
##   pre-registered bar at n≈8 matches; underpowered, and a confirmation leg is
##   now WORTH the exposure."* **"Confirmed" is forbidden and is not used.**
##   **THE STATISTIC CHOICE WAS THE DECIDING CALL AND IT WAS MADE BLIND:**
##   per-tile **+0.164 clears**, any-builder **+0.137 misses**, bar between them.
##   Chosen on the BAR'S PROVENANCE at `3b56e9b` 06:15:21; the blind replication
##   launched `14d7720` 06:08:52 and the number landed after. **Two clocks,
##   verified against `git log`, not accepted on report.**
##   **NEXT: a confirmation leg is now justified.** And the prereg's own fork is
##   open — retention cleared, **kill-speed was NOT read**.
##   ⛔ `tools/ring_retention.py` IS RETIRED (no entity-kind filter; **66.4% of
##   its "bodies" are barriers/conveyors** and it FLIPS THE SIGN). It now
##   **REFUSES TO RUN** (`8ec5222`, exit 2). **`tools/ring_retention.py`'s
##   `--selftest` PASSED and was worthless — every one of its three assertions
##   is on `ring_of()`, i.e. it tested the RING GEOMETRY and never the OCCUPANCY
##   RULE.** Use **`tools/ring_read.py`** (tracked `05:53Z`, 40 assertions over
##   11 cells, carries its own self-mutation harness).
##   ⛔⛔ **NAME BOTH FILES IN FULL, EVERY TIME — THIS BULLET USED TO SAY "Use
##   `scratchpad/ring_read.py`. **Its** `--selftest` PASSES and is worthless",
##   and the pronoun's antecedent was `ring_retention`, two clauses back.** s30
##   copied that antecedent into an audit brief; the audit dutifully mutated
##   `ring_read.py`, found the defect absent, and reported the claim REFUTED —
##   truthfully, about the wrong file. The side lane caught it. **THREE OBJECTS
##   SHARE TWO NAMES** (`tools/ring_read.py`, `tools/ring_retention.py`, and an
##   untracked `scratchpad/ring_read.py`), so a bare "it" here is not a style
##   problem, it is a defect generator.
##   **STILL OPEN from that sweep: `map_admits` — its selftest exercises
##   `classify()` and NEVER invokes `map_facts()` (0 calls in the selftest body
##   vs 2 in the shipped path, :191/:284).** That one is real.
##
## ===== ⭐⭐ LOKI-19 = `bots/_v136loki19` (md5 `fb5cba8c`) — BUILT, DOSE-VERIFIED, PREREG COMMITTED, NOT YET FIRED =====
##   **PREREG: `docs/prereg/PREREG-loki19-core-peck-2026-08-11.md` (`5aa5233`
##   06:32:49) — committed BEFORE leg creation, two-clock clean. n fixed at 4
##   interleaved windows / 50 games per arm, with a table saying which bars
##   resolve at that n (dose and mechanism YES, currency NO) and four-band
##   read-out language with forbidden words per band.**
##   **NEXT ACTION: fire it.** `rate_budget.py` said a slot was free at 06:32.
##   **ONE GATE. `LOKI19_CORE_PECK_ON`, re-enabling the enemy-core peck only.**
##   `main.py` and `eco.py` are BYTE-IDENTICAL to v104; counterbattery
##   (defensive) and siphon (economic) stay silenced deliberately.
##   **DOSE VERIFIED, and this is the anti-LOKI-17 check: 777 -> 3,005
##   builderAttack events over the same 10 local games.** The treatment fires.
##   **THE FINDING BEHIND IT:** `LOKI_QUIET_ON = True` has silenced all builder
##   melee since the Eir->Loki switch. **0 builder attacks across 2,247
##   self-inserts over SIX versions** (v104 alone 0/1,490) against a pre-quiet
##   **80.7% any_atk / 17.5% core_atk** — and **28.1% of night inserts stood
##   ORTHOGONALLY ADJACENT TO THE ENEMY CORE and never swung.**
##   **LOKI-QUIET WAS NOT WRONG. ITS PREMISE EXPIRED.** Its stated reason was
##   *"ARRIVAL is the scarce quantity, not damage"*; arrival went **18.6% ->
##   38.1%**. **A conditional optimisation outliving its condition — nothing
##   fails, no test goes red.**
##   **THE PREREG MUST CARRY THE COUNTER-ARGUMENT:** a peck still costs that
##   raider its move. The question is **not** "does melee help" but **"at 38%
##   arrival, is an arrived-round worth more spent on damage than on holding
##   position?"** — a different question from the one v96 answered at 18%.
##   **PREREG LINES RESEARCH ASKS FOR, both to prevent a units error:**
##   `ARRIVAL BASELINE: 38.1% reach, kind=INSERT, ours, rated corpus, n=475` and
##   size n against **0/2,247**, never the rated-only 0/475 (understates 4.7x).
##   **⛔ AND THE ARRIVAL NUMBER IS POPULATION-SENSITIVE — THIS IS THE SIXTH
##   UNITS-NOT-DATA INCIDENT OF THE DAY AND IT IS INSIDE THE GUIDANCE ITSELF:**
##   v104 reads **39.5% rated-only** but **23.3% pooled with unrated** (n=1,493),
##   and v102-v107 all-games spans **18.2%-40.9%**. **A leg that reads reach on
##   any other population will not get 38.1% and will test the bar against the
##   wrong number.** The tag travels with the number or the number is worthless.
##
## ===== ⭐ LOKI-19 IS FIRING. WINDOW 1 BOTH ARMS BANKED, 50 GAMES =====
##   **control 5/5 (04:35Z) · treatment 5/5 (05:00Z), v108 live 19 s, rollback
##   confirmed. ZERO rated leak — verified at the PAIRING BOUNDARY, not on the
##   match counter** (exposure 05:00:50–05:01:09Z sat between pairings at
##   04:52:59 and 05:12:59).
##   Prereg + 3 amendments committed before their respective arms existed:
##   **A1 arrival gate · A2 per-cell arrival admission · A3 the falsifier's
##   magnitude + CI rule.** Outfiles `scratchpad/arm_loki19_*`.
##   **NEXT: windows 2+ via `tools/unrated_run.sh 108 <games>`** — do NOT
##   hand-roll a runner, see below.
##
## ===== ⭐⭐ `tools/unrated_run.sh` — USE THIS FOR EVERY UNRATED LEG =====
##   `tools/unrated_run.sh <version> <games> [opponent_id ...]`
##   Magnus's spec. Never submits (submitting IS shipping); writes
##   `scratchpad/arm_*.txt` **by construction**; gates on `Active bot:` never
##   `$?`; waits past an imminent pairing with the period **derived from recent
##   rows, not hardcoded**; rotates cells; rollback verified + retried 4x, writes
##   `corpus/HOLDER_ALERT` and exits 1 on failure; SIGINT/SIGTERM trap restores.
##   **Abort branch mutation-tested ON THIS FILE and the result recorded in its
##   header** (MAIN=999 -> ABORT, exit 1, arm file EMPTY, zero fired).
##
## ===== ⛔ THE TOP QUEUE ITEM: `tools/ring_read.py` HAS NO SELFTEST =====
##   I retired the broken ring decoder and tracked the correct one — and **the
##   fix carried the fault one layer over: "wrong decoder, green test" became
##   "right decoder, NO test."** `ring_read.py` is now **the most load-bearing
##   instrument in the line**: it produced **LOKI-16b's +0.164** and it is the
##   decoder for **LOKI-19's §5d falsifier, the only band that may be written
##   plainly.** Its seven-cell validation exists as PROSE in
##   `docs/research/ADJUDICATION-ring-occupancy-decoders-2026-08-11.md`, was run
##   once by an agent in scratch, and **is not runnable today. A correctness
##   argument that cannot be re-executed is a claim, not a control.**
##   **The two cells that carry it are already known-answer:**
##   (a) a BARRIER on the ring with zero builder-rounds **must read 0.000**
##       (`ring_retention` read 0.900) — the cell that separates the decoders;
##   (b) a relay cell forcing **1.000 `hold_any` / 0.500 `hold_pinned`** — pins
##       the granularity Amendment 2a turned on.
##   **Declared mutant (harness spec fixture #1): drop the entity-kind filter ->
##   the selftest MUST fail.** Today it cannot fail; there is nothing to fail.
##
## ===== ⚠ QUEUE REORDERED MID-SESSION — LAUNCHER CHAINS DEMOTED BEHIND LOKI-19 =====
##   Chains were the lead for ~30 minutes (Magnus asked; we build exactly ONE
##   launcher, latched, on the DEFEND path — verified in the LIVE Loki tree).
##   **Demoted on the side lane's objection: building a six-link express lane to
##   deliver bodies that provably do not attack on arrival spends +60% permanent
##   cost scale to move the same zero further forward.** Insertion and conversion
##   are different planks and **conversion is upstream**. If a chain leg fires
##   and nulls, this is why — and the null would be **indistinguishable from
##   "chains don't work"**, closing a road wrongly.
##
## ===== ⛔ TURRET MIX (the s28 "best-corroborated candidate") IS OFF-PROGRAMME AS SPECIFIED =====
##   `main.py:544` is inside **`_try_counterbattery`** — a DEFENSIVE path. The
##   D30 grep found the right LINE and stopped before the enclosing FUNCTION.
##   The on-programme half (raid.py builds zero gunners) is real but is **a
##   build, not a constant**: gunner r²=13 vs sentinel r²=32, and a gunner's shot
##   is BLOCKED by obstacles. Corroboration also downgraded — the kill-mix half
##   is **substantially tautological**.
##
## ===== INSTRUMENT DEFECTS FOUND s29 — five, and two nearly killed live planks =====
##   1. **`tools/loki17_mech.py` COULD NOT RUN** (4-tuple yielded, 3 unpacked).
##      **No number in circulation came from it.** Fixed.
##   2. **`throws.tsv` CONDITIONALLY DEAD** — `reached`/`any_atk`/`core_atk` are
##      computed for **`kind=='INSERT'` ONLY**. `replay_throws.py:134` admits only
##      INSERT rows into `active`, and the attack/reach loops read only from
##      `active`, so **for every other kind the columns are NEVER COMPUTED.**
##      EXILE 171,984 · **RETREAT 24,277 (SAME-TEAM!)** · UNATTRIB 1,253 all read
##      exactly 0.00%; INSERT 77,844 reads 22.65% / 10.61% / 2.25%.
##      **This was about to retire the kidnap line, and the withdrawal stands.**
##      **⛔ MY FIRST PUBLISHED CAUSE WAS WRONG** — I said the columns were keyed
##      to the thrown bot's enemy so a kidnap's `core_atk` counted the enemy
##      hitting OUR core. **RETREAT is same-team and identically zero, which team
##      keying cannot explain.** The team-keyed line sits DOWNSTREAM of a gate it
##      never passes. **And my first version of the check split on team, pooling
##      the dead RETREAT rows into the half it printed as healthy — 17.29% vs a
##      true 22.65%, diluted ~24%: the check committing the defect it was built
##      to catch.** Both corrected; `corpus_sanity` now splits on `kind`.
##   3. `ring_retention.py` sign flip (above).
##   4. **`elo_history.tsv` and `corpus/SHIP_ALERT` stamp LOCAL CEST with NO ZONE
##      MARKER** — a successor reading `05:52` as Zulu thinks the tape is 2h
##      FRESHER than it is. **STILL UNFIXED. Builder-owned. Queued.**
##   5. `league_games.tsv` **47h STALE** (corpus_sanity flags it).
##   **⇒ Five units-not-data incidents in two days** (45° vs exact-ray; two
##   `undamaged`; three "forward"; `hold_any` vs `hold_pinned`; four at once in
##   `throws.tsv`). **The pattern is not carelessness — this project computes the
##   same quantity in two places and names it once.**
##
## ===== ENGINE FACTS ESTABLISHED s29 (subagent, `2181300`) =====
##   * **`can_fire_from` is UNAFFECTED by an intervening entity** — barrier built
##     on the ray, accept/reject identical at every distance on 3 maps.
##     **Retires PREREG-loki17 Amendment 1g limit 1.** (Legality only; the
##     damage-side version was not attempted.)
##   * **`_probe_firefrom` extended to ALL 8 facings** (was 3, all in one
##     quadrant): pure-Python geometry matches the engine on every facing.
##   * **Rotation control exact: 4067/4067 = 100.0% at rotate=0, 0/4067 = 0.0% at
##     rotate=1** on the same n.
##   * **⚠ TRAP FOR ANY MULTI-UNIT PROBE: `Player` CLASS-LEVEL STATE IS NOT
##     SHARED ACROSS A TEAM'S UNITS.** A probe's core wrote `Player.builder_id`
##     and the builder never saw it — **idle for 1000 rounds, no exception
##     raised.** Only `read_store`/`write_store` crosses units.
##   * `--archived` mode added to `loki17_mech.py` (resolves OUR seat per file
##     from `meta_join.us_side`; never assumes team 0).
##
## ===== ⚠ OPEN, AND DO NOT LET THEM LAPSE =====
##   * **Flag 2 on LOKI-16b:** `P(point <= 0 | true = +0.15, 8 clusters)` governs
##     the KILL band. **Moot today (the kill band did not fire), MUST be computed
##     before that row is ever used.**
##   * **The v95-v101 transition zone is NOT explained.** v98 was submitted
##     **17:10**, twenty minutes BEFORE the LOKI-QUIET tree existed (`7beac55`
##     17:30), and reads 0.0%. **Do not write the tidy history.**
##   * **Kidnap effectiveness has NO column in `throws.tsv`.** That is a decoder
##     gap and **must never be read as a null**. Prerequisite if the kidnap line
##     comes back up the queue.
##   * **Team 48**: mechanism real (they kill r93, we need r140) but **currency
##     dropped** — 2.7% of v104's rated diet and the rated sample INVERTS (7/10).
##
## ===== ⚠ RESEARCH RETRACTED ITS OWN "THE RACE TIGHTENED" TREND CLAIM =====
##   Subset-vs-whole comparison; disjoint periods give **+39 -> -10, p=0.123**,
##   opponent composition uncontrolled. **What survives is arithmetic only: the
##   +39 margin was computed on 240 of 365 games; the full-sample figure is +17.**
##   **Do not carry "the race is tightening over time" into a prereg.**

## ===== s28 BLOCK BELOW — SUPERSEDED WHERE IT CONFLICTS WITH THE ABOVE =====
# s28 state, 2026-08-10 17:31 CEST (15:31Z).

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
