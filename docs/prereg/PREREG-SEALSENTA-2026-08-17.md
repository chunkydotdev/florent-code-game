# SCREEN PREREG — `SEALSENTA`: the SAME seat sentinel, WITH the eco-deferral. The registered primary is THE CONTRAST.

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `SEALSENTA` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/SEALSENTA.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:20:53Z`** (`date -u`,
same shell call); repo HEAD at draft `6bb6a947` (author time
`2026-08-17T07:20:22+02:00`). Verified at draft:
`grep -c 'SEALSENTA\b\|SEALSENTAN' scratchpad/corefill_work.txt` → **0**;
same grep on `docs/prereg/BARS.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i sealsent` → **empty**;
`grep -cE '81[24]000' scratchpad/corefill_work.txt` → **0** (the seed base is free).

### SECOND CLOCK — and the brief's boilerplate correction did NOT survive my check
My drafting brief instructed me to avoid the `# FIXTURE … start=` stamp on the
grounds that it "names an artifact that does not exist". **That is false and I am
registering the correct method rather than the one I was handed.**
`tools/overnight.sh:99-101` stamps `START=$(date -u …)` and writes
`# FIXTURE\tshard=…\tstart=$START\trunner=tools/overnight.sh` as the tape's first
line **before the first `fcode run`**, on any tape that does not already exist.
⇒ **PRIMARY second clock: this commit's git author time against the
`SEALSENTA.tsv` `# FIXTURE … start=` stamp.**
**BACKSTOP, registered now:** if the tape carries `# FIXTURE-RESUME …
start=UNKNOWN-legacy-tape` (`tools/overnight.sh:105`) or no `# FIXTURE` line, the
second clock is **the `ts` of the FIRST COMPLETED ROW** — conservative, because
the true start is strictly earlier, so the gap can only be OVERSTATED.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v474sealsentA`,
added `493df130`, author time `2026-08-17T07:07:12+02:00`). This document is
therefore **NOT** locked before the arm exists, only before the arm's first
screen row. Said here rather than left for a certifier to find.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THIS ARM'S OWN BAR IS SECONDARY. THE REGISTERED PRIMARY IS THE CONTRAST
AGAINST `SEALSENTAN`.** The two trees differ in **ONE CONSTANT** —
`LOKI_SEALSENT_FUND_ON`, `True` here (`bots/_v474sealsentA/doctrine.py:1391`) and
`False` there (`bots/_v481sealsentAnofund/doctrine.py:1424`) — and in **nothing
else** (`diff -rq bots/_v474sealsentA bots/_v481sealsentAnofund` names exactly
`doctrine.py`, and the doctrine delta is that constant plus a comment block;
verified at draft). ⇒ **the difference of the two shares IS the price of the
eco-deferral, isolated, with the plant held constant.** That is the only quantity
on this page that no other leg can produce.

**2. ⛔ "THE DEFERRAL IS THE POISON, NOT THE PLANT" IS THE HYPOTHESIS THIS PAIR
TESTS. IT IS NOT BACKGROUND AND MUST NOT BE WRITTEN AS THOUGH IT WERE.**
An earlier form of the drafting brief said *"three surfaces already agree"*; the
side lane retracted that before this draft was written. The honest inventory:
* **ONE REGISTERED ARM — `KLADLADDER`** (`results.tsv:kladladder-n-final-correction`,
  **41.86% [40.20, 43.52] at n = 3,404**; dose battery **DOSE DELIVERED**, 1.58 vs
  0.75 forward sentinels/game). That is **outcome and mechanism of the SAME
  treatment** — one arm licensing attribution about itself, not two surfaces — and
  it is about a **different plank** (a forward-sentinel priority ladder, not a
  seat substitution). Its mechanism CANDIDATE (builder deaths 1.91x, forward
  deaths 2.25x) is typed on that tape as **diagnostic, not verdict**, and travels
  with two caveats wherever it is cited: **correlation inside 24 games**, and
  **a dose DIFFERENCE, not presence/absence — the control plants 0.75 forward
  sentinels/game itself.**
* **ONE UNREGISTERED BUILD DEMO** — the deferral gradient in
  `bots/_v481sealsentAnofund/doctrine.py:1403-1420`: nofund 54.2% [40.3, 67.4],
  **A (this arm) 37.5% [25.2, 51.6]**, B (N=2) 22.9% [13.3, 36.5], **48 matches
  per arm, `tools/arena.py`, no `results.tsv` row, no gate, no registration.**
  The tree's own comment already prices the A-vs-nofund contrast at
  **z ≈ 1.64, p ≈ 0.10** and records that neither interval excludes 50.
⇒ **These are PRIORS and an EXPECTED DIRECTION only.** They carry no n-weight in
any verdict here, no band below was chosen to accommodate them, and **the demo's
~17pp gradient is explicitly NOT the effect size this leg is sized against** —
the sizing below is done against the smallest difference the fixture can exclude,
not against the difference we hope to see (OB16: *size off the value you must
EXCLUDE, never the one you hope to observe*).

**3. THE PRE-STATE IS CLEAN.** The control `bots/_v468kladturbo` contains
`LOKI_SEALSENT` **0 times in all four files** and `_sealsent_` **0 times in all
four files** (verified at draft), and neither sealsent tree inherits KLADLADDER
(`grep -c LOKI_LADDER_ON` → **0** in both). Nothing this leg predicts to change
is already in the target state, and the comparative claim cannot be pre-satisfied
because the comparator arm has not been run.

**4. THE CONTRAST IS UNPAIRED, AND SAYING SO IS THE DIFFERENCE BETWEEN A CORRECT
AND AN UNDERSTATED INTERVAL.** Both shards run the identical 15-map × 2-seat
design at 180 replicates per cell against the identical control tree, so the
DESIGN is matched exactly. **The REALISATIONS are not:** the shards carry
different seed bases (812000 vs 814000) and, more fundamentally, `NOISE_ON` pins
an **unseeded** engine RNG, so two runs at the same seed diverge at round 0 and
**no seed-matched pairing is available on this fixture at all.** ⇒ **the contrast
is a TWO-SAMPLE difference of independent shares, and its interval is computed as
such** (formula in `THE CONTRAST` below). Any later reader who quotes a
paired-difference half-width for this comparison is quoting an interval this
fixture cannot support.

**5. BOTH SHARDS MUST RUN LOCAL, ON THE SAME HOST, AT THE SAME PLANNED n.**
Two independent reasons, both measured:
* `tools/auto_gate.py:113` is **REPORT-ONLY on a remote worker** and has no
  per-shard cancel primitive there. That is exactly why `KLADLADDER` ground to
  n ≈ 3,404 at 41.86% with no automatic stop and needed a manual STOP file
  (`results.tsv:kladladder-manual-catastrophe-stop`). The strict-regime floors —
  CATASTROPHE@400 (CI-hi < 45.0), MARK-1000 (CI-hi < BAR), TREND-FLOOR@1000
  (prefix < 52.0) — **bind only on local corefill.**
* The obligations doc's cross-host rider (Addendum 11 rider, 2026-08-15): the
  local DEFF 0.98 exemption is a **WITHIN-HOST** measurement and **does not cover
  cross-host pooling**; three same-arm pairs across two boxes put two of three
  outside the ±1.87pp band with mixed directions. **A contrast computed across
  hosts would carry an unregistered host term of roughly the same magnitude as
  the effect it is trying to resolve.**
⇒ **Routing either shard remote is a REGISTERED DEVIATION requiring an amendment
BEFORE the row is written.** If it happens anyway, the CONTRAST is **NOT
COMPUTABLE AS REGISTERED** and each arm falls back to its own (secondary) bar.

**6. THE FIRINGS READ COMES FIRST, AND THE RULE WAS INVERTED ON ITS FIRST FIRING
TODAY.** The shard tape carries only `ts shard game map seed seat winner cond
turns` (`tools/overnight.sh:138-139` runs every game with `--replay /dev/null`),
so nothing about the mechanism is visible on it, and this plank's mechanism is
CONDITIONAL. `docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule binds.
`results.tsv:kladladder-verdict-amendment-f1f2-pending` records the builder typing
KLADLADDER's primary **before** its registered dose read, then amending. **That is
a procedural datum on the tape and the builder is on notice.**
> **REGISTERED ORDERING: D1, S1 and F1 (below) are READ, and their numbers written
> down, BEFORE any sentence containing this arm's share or the contrast is typed.**
> A primary typed ahead of them is a REGISTRATION BREACH regardless of what it
> says; the repair is the amendment chain, not a re-write.

---

## RATIFY: Hypothesis

**PRIMARY (the contrast).** *Adding the eco-deferral contention guard to the seat
sentinel LOWERS our local pooled game share against `bots/_v468kladturbo`
relative to the otherwise-identical unguarded arm:*
**Δ = share(SEALSENTA) − share(SEALSENTAN) < 0, by more than 1.87pp at n = 5,400
per arm.**

**SECONDARY (this arm's own bar).** *The guarded arm reaches 51.33% or higher
against `bots/_v468kladturbo` at n = 5,400.* Reported, but **it is not what this
leg exists to decide** — an arm can miss its own bar and still supply the
decisive contrast, and can clear it and still leave the contrast unresolved.

**Provenance of the idea, verbatim (Magnus, s48):** *"Can we test a few builds
where we place sentinels on some spots instead of barriers around their core? Be
aware that if we allow our builders to build unlimited harvestors they will take
the titanium from our offensive builders trying to set up turrets."*
**THIS ARM IS THE SECOND HALF OF THAT DIRECTIVE — the contention guard itself —
and the contrast is what prices the warning.** Magnus's concern is about a real
mechanism; the open question is whether the CURE (a stalled economy) costs more
than the DISEASE (a turret outbid by a harvester).

**The mechanism claim, stated so it can be wrong.** With
`LOKI_SEALSENT_FUND_ON = True`, a raider that is established at the enemy ring
(`dsq_core ≤ LOKI_ESTABLISH_DSQ = 40`), under the N-cap, and short of the
sentinel price publishes a **want-beat** into store slot 13
(`raid.py:926-931`) — no site required, because the money must accumulate before
the raider is standing on the tile. While that beat is fresh
(`LOKI_SEALSENT_FUND_STALE = 3` rounds), `eco.py:412-413` refuses **every** eco
spend that would leave less than `get_sentinel_cost() + 6` in the bank — harvester
expansion, belt links, L4 repair, the opportunistic lay, and the launcher. The
beat has a **second leg**: once the turret is standing but the team magazine is
under `LOKI_SEALSENT_AMMO_FLOOR = 20`, the beat re-arms, because a sentinel that
cannot shoot is an expensive barrier. Both legs share one budget of
`LOKI_SEALSENT_FUND_MAX = 60` raider-rounds.
* **The claimed BENEFIT:** the turret arrives earlier and arrives FUNDED.
* **The claimed COST, and it is the hypothesis's own predicted direction:** while
  the beat is fresh the economy stands still, and **the builders ARE the economy**.
⇒ **A flat contrast is INFORMATIVE:** it would say the deferral is neither the
poison nor the cure, and that whatever moves the seat-sentinel family is the
plant, not its funding.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted, and performed for BOTH the single-arm bar and the contrast: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every row in BOTH shards plays the identical control tree, so each stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) for the CONTRAST specifically, a third candidate cluster — **HOST** — is killed by construction rather than by measurement, because READ-BEFORE-RATIFYING #5 registers both shards to the same local host; if that registration is broken the host term is live and unmeasured, which is why breaking it voids the contrast. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit). **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.**
**ESTIMATOR: for the SECONDARY bar, the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats and all 15 maps pooled, no reweighting. **For the PRIMARY, the DIFFERENCE of the two arms' unweighted pooled shares, Δ = p̂(SEALSENTA) − p̂(SEALSENTAN)**, each computed by that same rule on its own 5,400 rows. Because both shards are exactly balanced on the same 15 maps × 2 seats × 180 design, the pooled difference and the map-stratified equal-weight difference coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~6.8pp on byte-identical arms, which is why each n is a multiple of 30.
**DOSE: seat-band sentinel plants — treatment ≥1 vs flag-off control 0, to be measured at n=48 games (the registered D1 battery size below); PLUS the deferral's own dose, F1, measured on the same 48 games as store-slot-13 want-beat rounds, treatment >0 vs flag-off control 0.** Both control zeros are **structural, not measured at lock, and that is stated rather than dressed up**: `LOKI_SEALSENT_ON = False` makes `_sealsent_try` return `(False, None)` at `raid.py:861` before any board read, and `LOKI_SEALSENT_FUND_ON = False` short-circuits `_sealsent_reserve` at `eco.py:393` so `eco.py:413` can never bind. ⛔ **NO UNIT PROBE WAS FIRED FOR EITHER LINE.** D1 and F1 below are what convert them into measured claims, and both are registered to run BEFORE the primary is typed.
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, exact map and seat balance; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). **The CONTRAST's planned n is 5,400 PER ARM, 10,800 total, and the comparator arm's 5,400 is registered in `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md`.**
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed header, and a naive `wc -l`/`awk '!/^#/'` over-reports n by exactly one (measured today on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`, for BOTH arms of the contrast.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies only and takes **NO comparative look and no bar verdict**. ⛔ **AND THE CONTRAST HAS ITS OWN, STRICTER FLOOR: it requires ≥ 2,700 completed rows in BOTH arms, and its half-width is recomputed on the ACTUAL two n's, never on the planned ones.** At 2,700 + 2,700 the contrast's half-width is ±2.64pp, which is 41% wider than the registered 1.87pp — so a double-short contrast resolves only a much larger deferral cost, and that widened number is what any short readout must quote. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, and is typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically incompatible with this arm's secondary bar, so it DOES license the secondary falsifier at the partial n — **provided D1/S1/F1 have been read first**, and provided the partial share is disclosed as **selected-pessimistic** if the stop was taken on an interim look. **It does NOT license a contrast sentence** unless the comparator arm has also reached its own floor.
**BAR: 51.33 (SECONDARY — this arm's own house band). MDE: 0.00pp — THE SECONDARY BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n=5,400, so clearing it puts the CI's lower edge at exactly 50.00). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. **⭐ THE PRIMARY'S BAR IS SEPARATE AND IS SIZED, NOT A POINT RULE — see `THE CONTRAST` below: Δ ≤ −1.87pp, MDE 1.87pp, n for that exclusion 5,400 per arm.**
**BASE RATE: 50.00** (for the secondary bar). **For the primary, the null is Δ = 0.00pp** — the deferral changes nothing — which is the correct comparator precisely because the two trees are byte-identical apart from the one constant.
**BAR SOURCE:** the secondary is the house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — identical to the bars `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO` and `KLADLADDER` already carry, which is what keeps this arm numerically comparable to the sentinel family. **Constructed, not observed.** The PRIMARY's bar is derived in `THE CONTRAST` from the two-sample half-width at the planned n's, also constructed and also naive at DEFF 0.98.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control is the treatment's own base, empirically calibrated by `IDNULL140` — **49.27% [47.94,50.60] at n=5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n=5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⚠ **AND THOSE TWO CELLS SIZE THE CONTRAST'S OWN CREDIBILITY: they are 1.77pp apart, which is just under the contrast's 1.87pp half-width.** Two byte-identical arms on this fixture have therefore produced a difference nearly as large as the smallest one this leg can call real. **That is disclosed here, before the data, and it is why the contrast's bar is not set any tighter than the arithmetic allows.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`, identical in both arms. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**REFERENCE n: none** — the SECONDARY bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5400 seeds; there is no external reference SAMPLE for it. The PRIMARY's finite comparator is handled under `THE CONTRAST` and carries its own two-sample half-width. See `WHY REFERENCE n IS none` immediately below the registration block — the alternative reading produces a real `prereg_check.py` FAIL and is answered rather than dodged.
**TREATMENT TREE: bots/_v474sealsentA**
**TREATMENT DIFF REFS: 493df130^ 493df130**
**MECHANISM METRIC READS: bots/_v474sealsentA/eco.py:413 — the `if res and ti < cost + res: return False` line, the single choke point through which the eco-deferral acts on every economic spend in the tree, and therefore the ONLY executable difference between this arm and `bots/_v481sealsentAnofund`. Observed as F1 (rounds on which store slot 13 carries a fresh want-beat, per game, and the count of eco spends refused while it is fresh) alongside D1 and S1, all decoded off the replay wire, never from `print()` — `LOKI_SEALSENT_LOG` is False in both trees and platform replays strip stdout regardless. TREATMENT DIFF TOUCHES: bots/_v474sealsentA/doctrine.py bots/_v474sealsentA/eco.py bots/_v474sealsentA/main.py bots/_v474sealsentA/raid.py. INTERSECTION: yes — `eco.py:413` is inside the hunk the diff ADDS at `eco.py:371-413`; the `_sealsent_reserve` method and its call site did not exist in the control at all, and grepping the four control files for `_sealsent_` returns 0 in every one (verified at draft). The metric cannot read identically in both arms, and it is specifically the line that reads DIFFERENTLY between this arm and the contrast arm.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_SEALSENT_MIN_HARV=2, LOKI_SEALSENT_FUND_STALE=3, LOKI_SEALSENT_FUND_MAX=60, LOKI_SEALSENT_HOLD_MAX=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these four is a ROUND FLOOR.** `LOKI_SEALSENT_MIN_HARV` is a HARVESTER COUNT; `LOKI_SEALSENT_FUND_STALE` is a want-beat FRESHNESS span; `LOKI_SEALSENT_FUND_MAX` and `LOKI_SEALSENT_HOLD_MAX` are per-raider round BUDGETS, not earliest rounds. The plank has **no round gate whatsoever** — it arms the first turn a raider is established at the enemy ring with 2 harvesters on the board, and the tree's own demo plants at **r24 on drumlin s3**. The window is the whole game because the want-beat's SECOND leg (the magazine leg, `raid.py:918-925`) re-arms at any round the team's ammunition falls under 20 with a seat sentinel standing, and because a dead seat sentinel frees its N-cap slot on a LIVE-board census (`raid.py:678-719`).
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 2 is reported as "rounds r0-r1 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind.
⚠ **AND ONE FURTHER CHECKER LINE IS ANSWERED HERE RATHER THAN LEFT TO A CERTIFIER:** `METRIC_WINDOW` reports *"3 more elsewhere in `bots/_v474sealsentA/eco.py`"* and names `HUNT_MIN_RND = 120`. **Those are PRE-EXISTING BASE constants** (`HUNT_MIN_RND = 120`, `MEDIC_MIN_RND = 150`, `SURGE_MIN_RND = 300` at `doctrine.py:416,269,403`), they gate unrelated eco behaviours — hunt, medic, surge — **they are present identically in `bots/_v468kladturbo` and in `bots/_v481sealsentAnofund`, and none of them appears anywhere on the sealsent code path.** They are not declared as gating constants because they do not gate this mechanism; they are named here so that "3 more elsewhere" is not read as three undisclosed gates.
**GATE RESOLUTION: three gates, sized separately. (a) THE PRIMARY (the contrast) — resolvable at the planned n's: |Δ| must exceed 1.87pp, and that IS the registered MDE, so the gate's branches are separated by construction; if the observed |Δ| falls inside ±1.87pp the gate is UNRESOLVED and, per the pre-committed default, defaults to the RESTRICTION — no attribution of the seat-sentinel family's performance to its funding, in EITHER direction, and specifically no claim that the deferral is harmless. (b) THE SECONDARY (this arm's own bar) — margin 1.33pp against half-width ±1.32pp, resolvable and only just. (c) THE OPERATIONAL FLOORS — the pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0), MARK-1000 (CI-hi < BAR 51.33), TREND-FLOOR@1000 (prefix < 52.0) and the same floors at MARK-2700, all Magnus's confirmed constants; their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out written into CUT-SHORT. ⛔⛔ THOSE FLOORS BIND ONLY ON LOCAL COREFILL (`tools/auto_gate.py:113` is REPORT-ONLY on a remote worker), which is half of why READ-BEFORE-RATIFYING #5 registers this shard as LOCAL. ⚠ AN ASYMMETRIC-STOP HAZARD IS NAMED HERE BECAUSE IT IS THE MOST LIKELY WAY THIS PAIR BREAKS: if the floors cancel ONE arm and not the other, the contrast is being computed between a full arm and a SELECTED-PESSIMISTIC partial, which biases Δ in a direction the fixture chose rather than the mechanism. Registered handling: the contrast is then computed on the COMMON PREFIX (the first min(n_A, n_AN) completed rows of each tape, in tape order) and is labelled PREFIX-MATCHED, with the full-arm number reported beside it and neither presented as the other. Everything else on this page (D1, S1, F1, D2, D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft: `grep -c LOKI_SEALSENT bots/_v468kladturbo/*.py` → **0** in `doctrine.py`, `eco.py`, `main.py`, `raid.py`; `grep -c _sealsent_` → **0** in all four; `git diff --name-only 493df130^ 493df130` names exactly the four files of the new tree. The control has no want-beat, no reserve, no store-slot-13 write and no seat-sentinel machinery of any kind; it seals every free heal seat with a 3 Ti barrier unconditionally. **And the COMPARATIVE claim is likewise not pre-satisfied:** the comparator arm `SEALSENTAN` has never been run at screen n on this fixture, its only prior is an unregistered 48-game demo, and Band C below (Δ ≥ +1.87pp, the deferral HELPS) is a live, pre-named outcome that would refute the hypothesis outright.
**MAP SEGMENT: none expected** — the primary is the POOLED contrast over all 15 maps and both seats. The deferral acts through the global titanium bank, which is a team-global quantity with no terrain dependence; it arms on a raider's establishment distance and on the sentinel price, and neither is a map property. **No map cut may rescue this arm or this contrast.** Per-map shares and per-map Δ WILL be printed at readout as exploratory description — they carry no pre-registered direction and nothing may be banked off them without a fresh prereg. ⚠ **One candidate segment is named and DELIBERATELY NOT REGISTERED**: the five 900-area maps (midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep), where the longest approach plausibly holds the want-beat armed longest and so should show the largest deferral cost. Registering it would give this arm a second chance to pass, which is OB15b's exact prohibition; if the pooled contrast fails and that cut looks alive, it needs its OWN leg with its OWN n (OB15c: the rows that suggested a segment cannot also confirm it).
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**

---

## WHY `REFERENCE n` IS `none` — TWO BARS, TWO SAMPLINGS, AND THE FAIL I HIT ON THE WAY

Written out because the obvious alternative produces a `prereg_check.py` FAIL, and
a certifier should see that I hit it rather than wonder whether I dodged it.

* **The SECONDARY bar (51.33) is a ONE-SAMPLE bar** against the constructed null
  50.00, generated inside this shard from its own seeds. Its half-width is the
  one-sample ±1.32pp and its margin (1.33pp) resolves — barely, exactly as every
  house-band shard on this fixture resolves.
* **Writing `REFERENCE n: 5400`** — naming `SEALSENTAN`'s shard as a reference
  SAMPLE — makes the checker size 51.33 as a TWO-FIXTURE comparison at ±1.87pp and
  **correctly FAIL it.** Verified on this document before the line was changed:
  `BAR_RESOLVABLE FAIL — margin 1.3pp < half-width 1.9pp`.
* **That FAIL is a true statement about a bar nobody registered.** 51.33 is never
  compared against `SEALSENTAN`'s share. **The PRIMARY is**, and the primary
  carries its OWN two-sample bar — **1.87pp on Δ** — derived at the same n's in
  `THE CONTRAST` below, where the margin EQUALS the half-width and the gate
  therefore resolves by construction.
⇒ **Two bars, two samplings, and neither borrows the other's half-width.** The
contrast's comparator is still `SEALSENTAN`'s registered 5400-row shard and is
still finite, so the contrast's resolution does not improve without a registered n
increase in BOTH arms. Pooling extra rows into either arm after lock is an
unregistered n increase (optional stopping with extra steps) and is prohibited; a
replication is reported SEPARATELY and NEVER pooled, per the GUNAXABL/SENTTHR
precedent.

⚠ **TOOL DEFECT FOUND WHILE DOING THIS, ROUTED TO THE BUILDER, NOT FIXED BY ME:**
`tools/prereg_check.py:366-371`'s `int_before` uses `re.search(r"([\d,]+)\s*" +
word, …)`, and `[\d,]+` matches a **bare comma**. Any `REFERENCE n:` free text
whose first digit-or-comma character is a comma (e.g. a value beginning
`none — and this line, because …`) makes `int("")` raise, and
**`prereg_check.py` dies with a `ValueError` traceback instead of returning a
verdict.** Reproduced on this exact document during drafting. **A checker that
CRASHES on a prose value is a checker whose OK line can be absent for reasons
unrelated to the prereg** — and the crash exits non-zero, which on this platform
is not a health signal either way.

---

## THE CONTRAST — how Δ is computed, and what it can and cannot exclude

**ESTIMAND.** `Δ = p̂_A − p̂_AN`, where `p̂_A` is `SEALSENTA`'s pooled game share
against `bots/_v468kladturbo` over its own 5,400 rows and `p̂_AN` is
`SEALSENTAN`'s over its own 5,400 rows. **Both arms share the control tree, the
15-map pool, the 2-seat balance, the 180-replicate cell design, the runner
(`tools/overnight.sh`) and the host.** They differ in the treatment tree's ONE
constant and in the seed base.

**INTERVAL.** Two independent samples, DEFF 0.98:
```
se(Δ)  = sqrt( DEFF * ( p_A(1-p_A)/n_A + p_AN(1-p_AN)/n_AN ) )
       = sqrt( 0.98 * ( 0.25/5400 + 0.25/5400 ) )   at p ≈ 0.5
       = 0.009527          ->   half_width_95 = 1.96 * se = 1.867pp
```
**PRIMARY BAR: Δ ≤ −1.87pp.** Registered direction **NEGATIVE** (the deferral
costs). **MDE: 1.87pp — WE WILL CALL THE DEFERRAL COST A MISS IF ITS TRUE
MAGNITUDE IS AT OR BELOW 1.87pp. n for that exclusion: 5,400 per arm, which is
the planned n.** This is the OB16 preferred form: the bar IS
`null(0.00) + MDE(1.87)`, so clearing it IS the exclusion and the bar cannot be
quoted without its MDE.

**⛔ WHAT THIS LEG CANNOT DO, STATED BEFORE THE DATA.** A true deferral cost
smaller than ~1.9pp is **invisible to this fixture**, and sizing up to see it is
not free: excluding a 1.0pp difference would need ≈ 19,000 games per arm. **⇒ if
Δ lands inside ±1.87pp the registered reading is UNRESOLVED, not "the deferral is
harmless".** Restating the fail-to-exclude form as an exclusion is mandatory here
per CLAUDE.md's DEFF direction clause: the only harmlessness claim admissible is
*"the 95% interval on Δ excludes a cost larger than X"*, with X read off the
data, never *"no significant difference was found"*.

**⚠ AND THE UNREGISTERED PRIOR IS ~17pp (54.2 vs 37.5 on 48-game arms).** If
anything near that is real, this leg resolves it with an enormous margin — which
is exactly why the leg is worth firing and exactly why **the prior was not used to
size it.** A prior that large would have licensed a much smaller n, and the s42
circularity finding (OB16: `p → bar ⇒ n → ∞`) is that sizing off an observed
point estimate is invalid regardless of how comfortable the estimate is.

---

## FALSIFIER

**PRIMARY FALSIFIER: the 95% CI on Δ does NOT lie entirely below −1.87pp.**
Two sub-cases, both pre-named:
* **CI on Δ contains 0.00** → the deferral's cost is not resolvable at this n.
  **UNRESOLVED ⇒ restriction.** No sentence in any readout, wrap, or QUEUE row may
  claim the deferral is cheap, harmless, or the poison. The honest output is an
  upper bound on |Δ| and the observation that the seat-sentinel family's fate is
  decided by the plant, not by its funding — **which is itself a finding, because
  it retires the funding axis as a tuning direction.**
* **CI on Δ lies entirely ABOVE +1.87pp** → **the hypothesis is refuted with its
  sign reversed: the deferral HELPS.** Magnus's contention warning would then be
  correct in both direction AND magnitude, the unregistered 48-game gradient is
  refuted at 112× its n, and `SEALSENTA` — not `SEALSENTAN` — is the arm that
  carries the family forward. **This is a live outcome and it is named here so it
  cannot be explained away as noise if it lands.**

**SECONDARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's own
pooled share falls BELOW 51.33.** That excludes the arm's own bar. It does **not**
by itself decide the contrast, and a readout that reports only this number has
reported the less informative half of the leg.

**MECHANISM FALSIFIER (independent of both, and it can fire first):**
* if **S1** shows no seat-band shift in the treatment's sentinel-build positions,
  the PLANT did not fire and both the arm's bar and the contrast are
  **uninterpretable** — the primary is reported as **NOT MEASURED**, not as a null;
* if **F1** shows the want-beat is never published, or is published but refuses no
  eco spend, then the **DEFERRAL** did not fire and **the contrast is measuring
  two identical bots** — a Δ near zero would then mean "the constant had no
  runtime effect", which is a wiring null and not a finding about funding.
  **This is not hypothetical: s47's delta D2 records a wiring null escaping demos
  to a 436-game shard, and today's KLADLADDER amendment chain exists because a
  42.07 could equally have been one.**
Per FIRINGS-BEFORE-PRIMARY both are read BEFORE the primary is typed.

---

## READING, PRE-COMMITTED — four bands on the CONTRAST, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. Rows are disjoint.**

| # | band on Δ at 5,400 + 5,400 | pre-committed reading |
|---|---|---|
| **A** | **CI on Δ entirely below −1.87pp** | **THE DEFERRAL COSTS, AND THE COST IS RESOLVED.** The hypothesis holds. The funding guard is removed from the family, `SEALSENTAN` is the arm that carries forward, and Magnus's contention warning is answered as *"real in direction, and the cure costs more than the disease"* — with the size quoted, since this bar carries a real MDE. Promotes `SEALSENTAN` (subject to its OWN band) to a combination input and to a separately-registered head-to-head. |
| **B** | **point Δ < −1.87pp but CI contains −1.87pp** | **REAL-BUT-SMALL, DIRECTIONAL ONLY.** The direction is consistent with the hypothesis and the magnitude is not separated from the MDE. Rows are KEPT; the funding guard is deprioritised, not refuted; **no ship conversation and no closure of the funding axis.** A replication on fresh seeds, same host, is the price of promoting it. |
| **C** | **CI on Δ contains 0.00** | **UNRESOLVED ⇒ RESTRICTION.** See the primary falsifier. Report an upper bound on \|Δ\|. **The funding axis is retired as a TUNING direction** (there is nothing here to tune toward) without any claim that the deferral is harmless. |
| **D** | **CI on Δ entirely above +1.87pp** | **SIGN REVERSED — THE DEFERRAL HELPS.** The hypothesis is refuted. `SEALSENTA` carries the family, the unregistered demo gradient is overturned at 112× its n, and the next iteration tunes the guard UP (`_v475sealsentB`'s N=2 form becomes live again) rather than removing it. |

**And this arm's own share is read on the same four-band structure the sibling
prereg uses** (ADDS / REAL-BUT-SMALL / PARITY / SUBTRACTS against 51.33, 50.00),
reported as the SECONDARY. ⚠ **A cross-band note, registered so it is not
improvised: Band A together with a Band-4 (subtracts) reading on `SEALSENTAN`
means BOTH arms are worse than Sleipnir and the deferral is merely the worse of
two losses. That combination closes the seat-sentinel family and does NOT promote
anything, however clean Δ is.** The contrast prices a component; it does not
resurrect a plank that loses on its own.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**D1, S1 and F1 run and are written down BEFORE any sentence containing this
arm's share or the contrast is typed.** See READ-BEFORE-RATIFYING #6.

### D1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape.
```
tools/dose.py bots/_v474sealsentA --kind sentinel --ctrl bots/_v468kladturbo --games 48
```
**REGISTERED SIZE: 48 games (8 maps × 2 seats × 3 seeds — `tools/dose.py:126-131`
rotates its 8-map default two games at a time and plays both seats), SERIAL**
(never parallel: D65, `tools/dose.py:26-30`). **Pre-registered expectation:
forward-sentinel builds/game ≥ control's, paired difference outside the tool's own
2×SE band.**
⭐ **REGISTERED-SIZE SHORTFALL RULE, pre-committed, because KLADLADDER's battery
ran 24 of its registered 120 and its diff cleared the band by only 16%:** a short
battery states its shortfall factor, and **a `DOSE DELIVERED` verdict whose
|paired diff| clears its own band by less than 2× on a short battery is
UNRESOLVED** ⇒ restriction ⇒ the primary is typed with the mechanism unverified.

⛔⛔ **D1 ALONE CANNOT ANSWER THIS PLANK'S DOSE QUESTION — AN OB13 FINDING MADE AT
DRAFT.** `tools/dose.py`'s headline is `fwdbuild_sentinel/game`, and the seat
sentinel **shares** `LOKI_FWD_GUN_CAP = 3` with the base's own forward sentinel;
the tree says so in terms at `raid.py:874-878` (*"a seat Sentinel IS a forward
Sentinel… this plank relocates a turret rather than adding one"*). ⇒ **a treatment
that fires perfectly can read FLAT on D1**, and **a flat D1 is NOT evidence of
non-delivery and must never be reported as one.**

### S1 — THE SEAT-BAND READ. MEASURABLE, but it needs a battery that KEEPS replays.
The discriminator is the **`d2_enemy` distribution of sentinel `BUILD` events**,
treatment vs control. `tools/corpus/replay_events.py` emits one row per build with
columns `file ev rnd team kind x y d2_own d2_enemy mw mh` (`:157`):
```
.venv/bin/python tools/corpus/replay_events.py OUT.tsv <replays…>
# then: rows with ev == BUILD and kind == sentinel, grouped by team, histogram d2_enemy
```
**Pre-registered expectation: the treatment's distribution is shifted DOWN (closer
to the enemy core) and contains a low mode the control's does not reach on the
same map.**
⚠ **THE NUMERIC THRESHOLD IS DELIBERATELY NOT ASSERTED AT LOCK:**
`replay_events.py:95-96,113` measures `d2` to a **single core anchor position**
(`corepos[team]`), while the bot's `dsq_core` measures to the nearest tile of the
2×2 footprint — **so "a seat reads d2_enemy == 1" is an untested inference and is
not registered as a fact.** ⇒ **the cut point is CALIBRATED FROM THE CONTROL ARM'S
OWN DISTRIBUTION at readout** (the control plants on CORNERS, never on seats — its
own census note is at `raid.py:697-706`), so any treatment mass below the control's
minimum on the same map is the seat plant. **The DIRECTION is registered; only the
cut point is deferred, and it is deferred to a control-derived quantity that
cannot be tuned toward a verdict.**

⛔ **OB17 — S1 IS NOT EXECUTABLE OFF A `tools/dose.py` RUN.** `tools/dose.py:157`
calls `rp.unlink(missing_ok=True)` on every replay right after decoding, and its
argparse (`:110-116`) defines only `bot`, `--ctrl`, `--kind`, `--games`, `--maps`
— **there is no `--keep`.** ⇒ S1 needs either (a) a `--keep` flag added before the
battery runs, or (b) its own serial loop passing `--replay <unique path>`.
**CONSEQUENCE OF SILENT NON-EXECUTION (OB17 clause 3): if S1 is skipped, the dose
evidence is D1's headline ALONE, which cannot separate relocation from
non-delivery — the primary must then be typed with "MECHANISM NOT VERIFIED"
attached.** This is the clause that could still surprise the person running it;
run it first.

### F1 — THE DEFERRAL'S OWN DOSE. THE METRIC THAT IS UNIQUE TO THIS ARM.
**This is the read that makes the contrast interpretable, and no other leg has a
reason to run it.** On the same replay set S1 keeps, count per game:
* **want-beat rounds** — rounds on which store slot 13 carries a fresh beat
  (published at `raid.py:930`, consumed at `eco.py:395-401` within
  `LOKI_SEALSENT_FUND_STALE = 3` rounds);
* **deferred spends** — economic builds that the control arm makes and this arm
  does not, in the rounds when the beat is fresh, as a HARVESTER/CONVEYOR build
  count difference off the same `replay_events.py` BUILD rows.
**Pre-registered expectation: want-beat rounds > 0 in this arm and exactly 0 in
`SEALSENTAN` and in the control** (the constant short-circuits `_sealsent_reserve`
at `eco.py:393` and guards the publication at `raid.py:926`), **and the treatment's
harvester/conveyor builds in the beat window fall below the control's.**
⚠ **MEASURABILITY CAVEAT, stated rather than assumed:** store writes are NOT on
the replay wire. **Want-beat rounds are therefore INFERRED, not directly observed
— from the difference in economic build timing between the two arms.** If that
inference is judged too weak at readout, the honest statement is that F1 read the
CONSEQUENCE of the beat and not the beat, and the deferral's firing rests on the
code plus the build-count difference. **What is NOT admissible is quoting a
want-beat count as if it were decoded.**

### D2, D3 — the kill-round read. MEASURABLE, shard-native.
* **D2 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary).** Share of ALL
  treatment-seat games ending `cond == core_destroyed` with `turns ≤ 300`,
  treatment vs control, on the same 5,400 rows. **Non-regression is the bar and it
  is stated as an EXCLUSION, per CLAUDE.md's fail-to-exclude clause: the 95% CI on
  the difference must EXCLUDE a fall of more than 2.0pp.** "No significant rise"
  is not admissible phrasing. ⭐ **This is also the diagnostic most likely to
  explain a Band-A contrast:** a deferral that stalls the economy plausibly delays
  the kill, and D2 is where that would show.
* **D3 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (median
  crossing 300 is disqualifying), reported with the r1000 rate since
  `R1000_IS_DEFEAT` makes an r1000 share a cost even when the tiebreak is won.
  Anchor: KLADTURBO's own local full read had median kill 193
  (`results.tsv:kladturbo-local-confirm-5400`, 61.09% [59.79,62.39] n=5,400).

### NOT MEASURABLE on this leg — named, not silently dropped.
* **The want-beat itself** — see F1's caveat. Store contents are not on the wire.
* **Whether the HOLD ever costs an open seat.** `LOKI_SEALSENT_HOLD_MAX = 12`
  bounds it per raider, but seat-occupancy-over-time is not decoded by any shipped
  tool. **The plank's most plausible cost channel is UNOBSERVED on this leg**, in
  both arms equally — which is a reason the contrast is cleaner than either arm's
  own bar, since the unobserved channel is common to both.
* **Whether the planted sentinel ever FIRES.** The tree's own drumlin s3 demo found
  a seat sentinel that survived 279 rounds and never fired once, at 2-14 team
  ammo. `replay_events.py` decodes builds and deaths, not shots. **The magazine leg
  of the want-beat exists precisely to fix that, and this leg cannot verify that it
  does.** That is the single largest gap in this registration and it is named here.
* **Which of the deferral's two legs (build vs magazine) carries a Band-A result**
  — **NOT SEPARABLE**; they share one budget and one constant. Separating them
  needs an arm with `LOKI_SEALSENT_AMMO_ON = False`, and no readout sentence may
  attribute Δ to one leg.
* **Per-unit CPU** — local replays zero-fill `execTimeUs`; no timing claim is
  available on this surface.
* **Seed determinism** — `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0. **No seed-matched, paired, or replay-diff claim is
  available on this fixture** (this is why READ-BEFORE-RATIFYING #4 exists), and
  the flag-off base-equivalence claim is made on the CODE, never on a replay
  comparison. The engine is not run-to-run deterministic and nothing here assumes
  it is.

---

## THE CHANGE — `file:line`, and what separates this tree from its own contrast arm

**vs THE CONTROL `bots/_v468kladturbo`:** identical to the change list in
`docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` — doctrine block and constants
(`doctrine.py:1387-1408`), step 2a and the barrier skip (`raid.py:293-309`), the
`_sealsent_live` / `_sealsent_site` / `_sealsent_try` family (`raid.py:672-988`,
plant at `:950`), two cached frozensets (`raid.py:104-114`), two per-unit counters
(`main.py:136-142`), and `_sealsent_reserve` + its call site
(`eco.py:371-403`, `:412-413`).

**vs THE CONTRAST ARM `bots/_v481sealsentAnofund` — ONE CONSTANT:**
```
doctrine.py:1391   LOKI_SEALSENT_FUND_ON = True     <- this tree
doctrine.py:1424   LOKI_SEALSENT_FUND_ON = False    <- bots/_v481sealsentAnofund
```
`diff -rq` between the two trees names **`doctrine.py` and nothing else**
(verified at draft; `__pycache__` entries are build artefacts). Its two runtime
consequences, and there are exactly two:
* **`eco.py:393`** — `if not LOKI_SEALSENT_FUND_ON: return 0`. With the flag off,
  `_sealsent_reserve` is a constant zero, so `eco.py:413`'s `if res and …` can
  never bind and every economic spend behaves as `bots/_v468kladturbo` spends.
* **`raid.py:926`** — `if (LOKI_SEALSENT_FUND_ON and (short or dry) and …)`. With
  the flag off the want-beat is never published and store slot 13 is never
  written.
**⇒ the plant, its siting filter, its N-cap, its hold and its waived
`LOKI_SEALSENT_TI_FLOOR = 0` are IDENTICAL in both arms. Δ is the deferral and
nothing else.** ⚠ **Corollary the readout must respect: `LOKI_SEALSENT_TI_FLOOR = 0`
is present in BOTH arms, so neither arm — and therefore not the contrast — says
anything about the waived reserve floor.**

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 48 serial games for D1/S1/F1** — and it
is the second half of a pair whose sibling costs the same, so the CONTRAST costs
two local cores to 5,400 each. ZERO rated ladder exposure, zero submissions, zero
unrated challenges; nothing on this page touches the platform, which is why
`TARGET BAND` is N/A rather than a number.

**It does NOT decide a ship.** The strongest branch on this page decides which
FORM of the seat-sentinel plank goes forward — not whether any form ships. That
question belongs to the surviving arm's own band and then to a separately
registered head-to-head against the live holder, per Magnus's procedure verbatim
(*"we start by testing it against the current slot, If it beats it we can
switch"*), for which `SLEIPH2H` is the template. **A local screen against the
incumbent is gate 1; gate-1-to-gate-2 transitivity is UNVALIDATED in this repo
(QUEUE #65: 3 concordant, 1 not).**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-KLADLADDER-2026-08-17.md` (today's house style, read in full) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` (this leg's contrast arm, drafted in the same pass) · `docs/prereg/BARS.tsv` (registry header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad/sealsent-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `check_presence`, `check_arithmetic`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py` (`MARK_CATASTROPHE=400`, `MARK_MID=1000`, `MARK_HALF=2700`, `CATASTROPHE_CI_HI=45.0`, `TREND_FLOOR=52.0`, and the `:113` remote report-only limitation) · `tools/overnight.sh` (`:66` the 15-map pool, `:99-101` the `# FIXTURE … start=` stamp, `:105` the legacy-resume form, `:138-139` `--replay /dev/null`) · `tools/dose.py` (`:110-116` argparse, `:126-131` map/seat rotation, `:157` the replay unlink, `:80-105` the decoder, `:171-205` the paired band) · `tools/fwd_read.py` (docstring + `:191-208` decode output columns) · `tools/corpus/replay_events.py` (`:56`, `:95-96`, `:113-117`, `:157`) · `bots/_v474sealsentA/doctrine.py` · `bots/_v474sealsentA/raid.py` · `bots/_v474sealsentA/eco.py` · `bots/_v474sealsentA/main.py` · `bots/_v481sealsentAnofund/doctrine.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows `null125-final`, `idnull140-cert-5400`, `kladturbo-local-confirm-5400`, `kladladder-manual-catastrophe-stop`, `kladladder-verdict-amendment-f1f2-pending`, `kladladder-final-attribution`, `kladladder-n-final-correction`) · git commits `493df130` and `aba27582` and `git diff --name-only 493df130^ 493df130` · the drafting brief supplied by the builder lane s48 and its mid-task correction consumed from the side lane. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.

---

## AMENDMENT 1 (builder s48, 2026-08-17T05:48:46Z, BEFORE the leg's first game — surface change LOCAL → worker@work-server-1)

The registered LOCAL-ONLY routing cited auto_gate.py:113 (remote = report-only,
floors cannot bind) as its reason. **That reason died one hour after lock:**
commit a50f27ef gives auto_gate --apply a guarded remote stop path
(tools/remote_cancel.py), so the strict floors NOW BIND on ws1. Meanwhile the
local box is load-held (agent work; the load ceiling correctly protects row
validity — wall-clock TLE corruption is load-sourced regardless of cause), so
LOCAL routing would idle both arms indefinitely against Magnus's iterate
directive. CHANGES: host = worker@work-server-1 (seed offset +32,000,000 per
the sidecar; registered seedbases unchanged); second clock = first-completed-row
/ serial-ordering backstop (remote tapes carry no FIXTURE stamp — the registered
backstop, now primary); host certification = NULLWS1S (this host, TODAY,
54.25 [49.37,59.13] n=400, collision/sanity scope as pre-committed). Everything
else — bars, bands, contrast, stops semantics, FIRINGS-BEFORE-PRIMARY —
unchanged. Local worklist rows retired with pointers here.
