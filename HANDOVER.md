# Session 19 UPDATE (builder, 21:4x) — supersedes the 19:50 block below

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
