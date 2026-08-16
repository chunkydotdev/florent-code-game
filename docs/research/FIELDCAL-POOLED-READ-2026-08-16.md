# FIELDCAL POOLED READ — `LEG-fieldcal-2026-08-16`, interim, across the s45/s46 session seam

**Research arm, read-only. Wall clock: `date -u` = 2026-08-16T08:00:10Z.**
**The leg is LIVE and unattended at read time** (scheduler in round 6, arm A, cell `kladde`,
invocation running 600 s in a rate-window wait as of 08:00:17Z). Nothing in this document touched
the scheduler, fired a match, or changed a bot.

---

## 0. WHAT WAS READ, AND HOW OLD EACH SURFACE IS

A monitor that reads a file reports that file's freshness (`CLAUDE.md` standing rule). Ages are
against 08:00:10Z.

| file | mtime (UTC) | age | role here |
|---|---|---|---|
| `docs/prereg/LEG-fieldcal-2026-08-16.md` | 05:58:44Z | 2 h 01 m | **the registration. Everything below is scored against this and nothing else.** |
| `docs/research/CERT-LEG-fieldcal-2026-08-16.md` | 06:02:52Z | 1 h 57 m | side-lane two-clock / arithmetic certificate |
| `scratchpad/fieldcal_state.tsv` | 07:50:16Z | 9.9 m | ROUND / CLOCK2 / per-cell accept counts |
| `corpus/our_matches.tsv` | 07:50:02Z | 10.1 m | accept ledger (match ids), independent of the log |
| `corpus/meta_join.tsv` | (untouched today) | newest `completedAt` **07:48:17.336Z**, 11.9 m | per-game outcomes |
| `corpus/ladder_games.tsv` | 07:55:01Z | 5.2 m | rated pairings; **newest pairing `created` = 07:32:59.701Z ⇒ 27.2 m behind wall clock** |
| `corpus/join.tsv` | — | **0 leg rows** | would carry `turns`/`cond`; leg replays are not decoded |
| `scratchpad/.rate_ledger` | 07:50:02Z | 10.1 m | our own challenge fires |
| `scratchpad/fieldcal_scheduler.log` | 07:58:17Z | — | ⛔ **TRUNCATED at 07:40:13Z by the nohup relaunch (`>` not `>>`). NOT CITED for leg history anywhere below.** Rounds 0–4, both halts and every pre-07:40 gate reading are unrecoverable from it. |

**Two-clock, discharged (the obligation `CERT §5.1` transferred to the firing session):**
clock 1 = git author time of lock commit `43d9035f` = **2026-08-16T05:59:01Z**;
clock 2 = first accepted challenge = **2026-08-16T06:25:40.381Z** (state tape, corroborated by the
first row of `our_matches.tsv` at 06:25:40.639Z and the first `.rate_ledger` entry at 06:25:40Z).
**Gap +26 m 39 s, clock 2 strictly later. Clean.**

---

## 1. LEG STATUS

**ROUND 6 in progress** (state tape). Rounds 0–5 are behind us.

Per-cell accepts (state tape, and independently reconstructed from `our_matches.tsv` — the two agree
exactly, 25 = 25):

| cell (rotation idx) | arm A (v140, control) | arm B (v154, BODYAWR) |
|---|---|---|
| 0 Juusto | **5**/12 | **5**/12 |
| 1 not_adgato | **5**/12 | **0**/12 ⚠ |
| 2 Erebus | **5**/12 | **5**/12 |
| 3 kladde | 0/12 *(firing now)* | 0/12 |
| 4–9 gsxWins, 0033, lingling_40h, HTTP 418, The Bisons, farming_200s | 0/12 | 0/12 |

**COMPLETION AGAINST THE REGISTERED DESIGN (240 accepts / 1,200 games):**

| unit | banked | design | fraction |
|---|---:|---:|---:|
| accepts | 25 | 240 | **10.4 %** |
| games fired | 125 | 1,200 | **10.4 %** |
| games with outcomes decoded | 100 | 1,200 | **8.3 %** |
| (arm,cell) pairs at 12/12 | 0 | 20 | **0 %** |
| (arm,cell) pairs touched at all | 4 | 20 | 20 % |
| cells with BOTH arms fired | 1 | 10 | **10 %** |
| cells at the `CUT-SHORT` floor (40 games/arm = 8 accepts) | **0** | 10 | **0 %** |
| games vs the `CUT-SHORT` floor of 800 total | 125 | 800 | **15.6 %** |

The declared identity holds: 25 accepts × 5 = 125 games (the `BOUNDARY` was registered in both units
precisely so a miscount shows as a broken identity; it is not broken).

**Outcomes are decoded for 20 of the 25 accepts (100 of 125 games).** The five missing are the
entire round-5 `B/Erebus` burst (07:49:52–07:50:02Z) — `meta_join`'s newest `completedAt` is
07:48:17Z, so those matches finished after the archive's last write. **Per §9.5 that absence is
archiver lag, not evidence.**

---

## 2. THE REGISTERED PRIMARY — **NOT COMPUTABLE. THIS IS AN EXPLICIT REFUSAL, NOT A GAP TO BE FILLED WITH SOMETHING ELSE.**

**What is registered (`§1 ESTIMATOR`, `§4`):** the **exact two-sided binomial sign test over 10
pinned opponent cells** on `sign(game_share_TREAT − game_share_CTRL)` within each cell. Bar: **9/10
cells share the sign**, p = 0.0215. 8/10 = UNRESOLVED. ≤7/10 = MISS (registered in advance as the
expected outcome via the bar-level impotence clause).

**What is missing, named exactly:**

1. **Nine of ten cells have zero games on at least one arm.** Only `Juusto` has both arms.
2. **`not_adgato` and `Erebus` are single-arm cells** — a sign is undefined without both.
3. **`CUT-SHORT` (§1) binds and excludes every cell:** a cell needs **40 games per arm** to enter the
   primary. The best cell has **25 per arm**. ⇒ **k_eligible = 0.**
4. §1's own escalation: *"At k < 8 the primary is UNRESOLVED and defaults to the restriction (§7)."*
   **k = 0 < 8.**
5. §1's `CUT-SHORT` also binds at leg level: 125 games against an 800-game floor ⇒ *"counts only,
   descriptive, no sign test, no reversal claim."*

⇒ **THE PRIMARY IS UNRESOLVED BY THE LEG'S OWN PRE-COMMITTED RULE. No sign test is reported below,
at any k, in any direction.** Substituting a pooled game-share number and calling it the primary is
the failure this section exists to refuse; §6.1 of the prereg independently declares pooled win
share **DESCRIPTIVE ONLY** even at full n.

**THE SECONDARY IS ALSO NOT COMPUTABLE, and for a different reason worth recording separately.**
Pooled **ITT RMST₃₀₀** — the estimator that *carries the reversal falsifier* — needs `turns` and
`winCondition` per game. `corpus/meta_join.tsv` has **neither column**; `corpus/join.tsv`, which
does, contains **0 rows for the 25 leg matches** because the leg's replays have not been downloaded
or decoded. ⇒ **The falsifier's primary axis cannot be evaluated on any locally archived surface
today.** It becomes computable only once the replay decode reaches these match ids. **That is a
pipeline dependency this leg's read-out plan does not name anywhere, and it should be routed as a
successor item.**

---

## 3. WHAT *IS* COMPUTABLE — DESCRIPTIVE COUNTS, WITH THEIR BAND

Labelled with the expectation before the read, per the instrument rule.

**EXPECTED before reading:** ~44–52 % share per cell (our field baseline sits near parity against
this band); arms within noise of each other; no cell at 12/12.

| arm | cell | our game wins | games | **game share** | decoded `oppver` | registered `theirver` | §9.3 pin assertion |
|---|---|---:|---:|---:|---|---|---|
| A (v140) | Juusto | 11 | 25 | **44.0 %** | `13` ×25 | 13 | **PASS** |
| B (v154) | Juusto | 9 | 25 | **36.0 %** | `13` ×25 | 13 | **PASS** |
| A (v140) | not_adgato | 12 | 25 | 48.0 % | `23` ×25 | 23 | **PASS** |
| A (v140) | Erebus | 13 | 25 | 52.0 % | `119` ×25 | 119 | **PASS** |
| B (v154) | Erebus | — | (5 accepts, results not yet archived) | — | — | 119 | pending |

**§9.3 PIN ASSERTION: 100 of 100 decoded games carry the registered opponent version. Zero cells
voided.** This is the load-bearing check the `UNPINNED_OK` guard cannot perform (it catches an EMPTY
pin, not a WRONG one), and it passes cleanly on everything decoded. It is also a positive read on
the two HIGH-CHURN cells the prereg named — `Erebus` (10 distinct versions in 24 h) came back `119`
on 25 of 25 games, i.e. **the pin took against the churniest cell on the board.**

**THE ONLY PAIRED COMPARISON THAT EXISTS: `Juusto`.**
Arm A 44.0 % (11/25) · Arm B 36.0 % (9/25) · **(T − C) = −8.0 pp.**

Per-match scores (out of 5), so the cluster structure is visible rather than asserted:
A/Juusto `3,2,3,1,2` · B/Juusto `2,1,1,2,3` · A/not_adgato `3,1,4,2,2` · A/Erebus `1,2,4,3,3`.

---

## 4. POWER / SUFFICIENCY — THE HALF-WIDTH ON THE ARM DIFFERENCE

### 4.1 Cluster enumeration, performed in writing and **verified from the data, not asserted**

The stratum is *one arm within one opponent cell* (`Juusto`).

| cluster | can this stratum hold >1 member? | **verification** | survives? |
|---|---|---|---|
| **MATCH** | yes | games per leg match = **5 for 20 of 20 matches** (`Counter({5: 20})`); the stratum holds **5 matches × 5 games** | **LIVE** |
| **OPPONENT** | no | the stratum is a single pinned opponent cell by construction — 1 distinct `opponent_id`, 1 distinct decoded `oppver` | **DEAD** |

⇒ **The applicable reference constant is the UNRATED WITHIN-OPPONENT DEFF = 1.434** (opponent cluster
removed, match cluster live). Using the pooled 1.833 here would double-count a cluster that is not
present; using 1.0 would drop a cluster that is.

### 4.2 Half-width, two-fixture form (§9.7)

`half_width_95 = 1.96·sqrt( p̄(1−p̄)·(DEFF_A/n_A + DEFF_B/n_B) )`, p̄ = 20/50 = 0.400, n = 25 each.

| DEFF used | half-width | 95 % CI on (T − C) |
|---|---:|---|
| **1.434 — within-opponent, the correct one** | **±32.5 pp** | **[−40.5, +24.5] pp** |
| 1.833 pooled (over-corrected, shown for contrast) | ±36.8 pp | [−44.8, +28.8] pp |
| 1.0 naive independence (under-corrected) | ±27.2 pp | [−35.2, +19.2] pp |

### 4.3 ⛔ THE DIRECTION RULE, APPLIED BEFORE ANY NULL LANGUAGE

The tempting sentence here is *"no significant difference between arms"*. That is a
**fail-to-exclude** claim, and widening an interval makes it **easier**, so it must be restated as
an exclusion before the DEFF touches it.

**Restated as exclusions, at DEFF 1.434, n = 25/arm:**
* Does the CI exclude **zero**? **NO** — it spans [−40.5, +24.5] pp.
* Does the CI exclude the registered **reversal bar of −7.7 pp**? **NO** — the bar sits inside the
  interval.
* Does the CI exclude the local prior of **+3.70 pp**? **NO.**
* The largest reversal this cut excludes is **−40.5 pp**. Nothing smaller.

⇒ **Every claim available at this n is a non-exclusion. The correct banked sentence is: *the leg has
so far excluded reversals larger than 40.5 pp on one of ten cells, and nothing else.***

### 4.4 ⭐⭐ THE SURPRISE, FLAGGED BEFORE IT IS EXPLAINED AWAY

**The observed −8.0 pp is numerically past the registered falsifier threshold of −7.7 pp, AND THAT
MEANS NOTHING.** A reader skimming §5 of the prereg for the number `−7.7` and finding `−8.0` on the
tape would conclude the falsification has fired. **It has not, and the prereg says why in its own
sentence:** the falsifier is *"a pooled REVERSAL **beyond the leg's own detectable band at 600
games/arm**"* — i.e. **−7.7 pp is the 95 % half-width at n = 600/arm, not a point-estimate
threshold.** At n = 25/arm the half-width is **±32.5 pp**, so the identical point estimate carries
**1/4.2 of the evidential weight** the falsifier was denominated in.

**This is a live mis-read hazard on an unattended two-session leg** — the threshold is a bare number
in the registration block, the tape will keep producing point estimates that wander across it, and
the qualifier that disarms it lives one section away. **Recorded here so a successor cannot arrive
at the arithmetic without the qualifier attached.**

### 4.5 The DEFF re-measurement obligation (§3) — attempted, and **deliberately not used**

The prereg requires every banked interval to use the leg's OWN re-measured design effect. Computed
with the df correction on the leg's 20 decoded matches:

* pooled: p̄ = 0.450, s²_obs = 0.037368 vs binomial 0.049500 ⇒ **DEFF = 0.755 (ρ = −0.061)**
* within-(arm,cell), df = 16: s²_w = 0.040000 ⇒ **DEFF = 0.808 (ρ = −0.048)**

**Both are below 1, which at M = 20 clusters is sampling noise, not a discovery** — the estimator has
~16 df and no power to separate 0.8 from 1.4. ⛔ **And using it would be off-registration in the
worst possible direction: it NARROWS the interval to ±24.4 pp, and every claim available here is a
fail-to-exclude, which narrowing makes easier.** That is precisely the laundering §3's direction
rule forbids. **The headline above therefore uses the reference 1.434; the leg's own value is
reported as a diagnostic and is not bankable until the leg has enough clusters to estimate it.**

### 4.6 Imbalance, reported once under one heading (§6.2)

* **Per-cell accept counts:** A = 15 accepts, B = 10. **Arm A leads arm B by one full round** —
  cause in §5.
* **Seat:** in the only paired cell, A/Juusto played 15 games in seat A / 10 in seat B, B/Juusto
  played 10/15 — a 5-game seat swap between the arms of the one comparable cell. **Measured seat
  effect on the leg's 100 decoded games: seat A 46.0 % (23/50) vs seat B 44.0 % (22/50), a 2.0 pp
  spread.** Disclosed, not corrected.
* **Time-of-day:** A fired at 06:25 / 07:06 / 07:29 (+07:50 pending); B at 06:45 / 07:49. The
  registered between-windows alternation is broken once, at round 3.
* **Opponent pin age:** all three fired cells are inside the leg's own morning; `farming_200s`'
  ~16 h pin has not been reached yet.
* **Map:** ⛔ **NOT READABLE.** `meta_join.tsv` carries no `map` column and `join.tsv` has no leg
  rows. Map mix cannot be reported until the replays decode.

---

## 5. IS THE LEG HEALTHY? — **DESIGNED ROTATION, WITH ONE REAL HOLE THAT THE DESIGN DOES NOT SELF-HEAL**

### 5.1 The fill pattern IS the designed rotation, not starvation

`tools/fieldcal_scheduler.sh:668-669` is the whole design:

    if (( round % 2 == 0 )); then arm=A; else arm=B; fi
    start_idx=$(( (round / 2) % 10 ))

Round 0 → A/idx0, round 1 → B/idx0, round 2 → A/idx1, round 3 → B/idx1, round 4 → A/idx2, round 5 →
B/idx2, round 6 → A/idx3. Each round's 5-accept window budget is consumed entirely by its start
cell, so **one round = one cell**, and the design fills all 20 (arm,cell) pairs to 5/12 on the first
pass, 10/12 on the second, 12/12 on the third.

**Predicted from that rule, before reading the tape:** A at idx 0,1,2 = 5/5/5; B at idx 0,1,2 =
5/5/5; A/idx3 in flight. **Observed: A 5/5/5 ✓, B 5/`0`/5 ✗, A/kladde in flight ✓.** So the shape is
the design and the exception is exactly one cell. **This is NOT the `fanout.sh` tail-starvation
class** — that class produces a monotone decay toward the end of the id list, and there is no tail
here to starve: the rotation has not yet reached idx 3.

### 5.2 The hole: **round 3 (arm B / not_adgato) consumed a round and fired nothing**

Established on three independent surfaces, none of which is the truncated log:

1. **`.rate_ledger`:** exactly 25 fires in the leg era, in five bursts —
   06:25:40–50, 06:45:53–06:46:04, 07:06:03–13, 07:29:39–49, 07:49:52–07:50:02.
   **A 23 m 26 s hole between 07:06:13 and 07:29:39 with zero challenge attempts** — not five
   rejections, **zero attempts**.
2. **Runner outfiles:** no `arm_unrated_v154_*` file exists with a stamp between `064545Z` and
   `073003Z`. The runner was never invoked in that span.
3. **`our_matches.tsv`:** no `v154` row against `fb0e7053…` (not_adgato) at any time.

⇒ Round 3 returned from `run_round` **before** reaching `invoke_runner`. The only such paths in the
scheduler are the `halt_file_present` early returns at `:675-678` and `:694-697`; `ROUND_NUM` then
increments at `:748` regardless, and the next loop iteration exits cleanly at `:732`.
⛔ **WHICH halt it was, and why, was recorded only in the scheduler log and is UNRECOVERABLE** — the
07:40:13Z relaunch used `>` and overwrote rounds 0–4. I am not inferring the cause; I am reporting
that the cell was **skipped without a challenge**, which is what the surviving surfaces can carry.

### 5.3 ⚠ THE CONSEQUENCE, AND IT IS THE MOST USEFUL THING IN THIS DOCUMENT

**The rotation is a pure function of the round counter, so a round that fires nothing is never
retried inside the same pass.** `start_idx = (round/2) % 10` advances mechanically. Arm B's
`not_adgato` cell is next visited at **round 23**, roughly **seven hours** behind its arm-A
counterpart at round 2.

**The scheduler's documented anti-starvation guarantee does not cover this door.** `:689-698`
implements *wait-and-retry-the-same-cell, never advance* — but **only for the rate-budget gate**.
A round terminated by a HALT (or by a kill, or by `pos++` at `:722` after a zero-accept invocation)
advances the counter and the cell is lost for a full pass.

**Why that matters to the statistic and not just to tidiness:** the primary is a **per-cell sign
test**, and §1's `CUT-SHORT` excludes any cell short of 40 games per arm. **B/not_adgato is now the
single cell most likely to be excluded under any truncation, and it earned that position from a
halt, not from anything about the opponent.** §9.6b registers exactly this failure mode — *"the
excluded set is a function of firing order rather than of anything about the opponent"* — and names
two doors (drops, ordering). **This is a THIRD door: an aborted round.** It is not a defect in the
prereg's reasoning; it is a gap in the scheduler's implementation of it.

**Verdict on health: the leg is running to design, the rotation is correct, the pin holds 100/100,
and there is one cell-shaped hole from an unrecorded halt that the design will not close until round
23.** Cheap remedy for a successor (not applied — the leg is live and unattended): a
`least-filled-cell-first` tiebreak, or a one-time manual top-up of B/not_adgato, would close it
without disturbing the rotation.

### 5.4 A second, quieter effect of the same halt: the pairing-gap margin halved

`tools/unrated_run.sh` guard 4 (`GUARD_S=150`) derives the pairing offset from recent rows and holds
each fire clear of the next pairing. **Cadence re-derived here rather than assumed** (last 60 ladder
pairings): **60/60 at minute ≡ 12 (mod 20), 60/60 at second `:59`, consecutive gaps 1199–1200 s** ⇒
slots at `:12:59`, `:32:59`, `:52:59`.

| round | arm | last challenge | next slot | margin |
|---|---|---|---|---|
| 0 | A v140 | 06:25:50Z | 06:32:59Z | 7 m 09 s |
| 1 | B v154 | 06:46:04Z | 06:52:59Z | 6 m 55 s |
| 2 | A v140 | 07:06:13Z | 07:12:59Z | 6 m 46 s |
| **4** | A v140 | 07:29:49Z | 07:32:59Z | **3 m 10 s** |
| **5** | B v154 | 07:50:02Z (rollback confirmed **07:50:07Z**) | 07:52:59Z | **2 m 57 s** |

**The margin halves exactly at round 4 — the round after the halt.** The halt was not a whole
20-minute window, so it re-phased the leg ~4 minutes closer to the pairing slot. The floor is
`GUARD_S = 150 s` by construction, so this is the guard binding rather than an alarm, and the actual
exposure is small (round 5's full activate→queue→rollback sequence took **16 s**, 07:49:51→07:50:07,
against a 177 s margin). **Reported because the trend has a cause and the cause is the same halt.**

---

## 6. LEAK CHECK — INDEPENDENT CORROBORATION FROM `ladder_games.tsv`

The scheduler asserts *"no rated pairing played by an arm since clock2"*. Verified here **per-match
at the PAIRING boundary** (`created`), never on a match counter — the counter is structurally blind
to a match PAIRED-but-not-COMPLETED while an arm held the slot.

**Query:** all distinct ladder matches with `created` > clock2 (06:25:40.381Z), grouped by `ourver`.

    06:32:59.700Z  v152  gsxWins
    06:52:59.607Z  v152  0033
    07:12:59.630Z  v152  HTTP 418
    07:32:59.701Z  v152  Well have a look

**4 pairings, all v152 (the pre-leg holder). ARM-VERSION pairings post-clock2 = 0.**
The 07:32:59 row is a *positive* result, not just an absence: it is the slot 3 m 10 s after round
4's last v140 challenge, and it shows **v152**, i.e. the rollback beat the pairing.

⛔ **COVERAGE LIMIT, stated because absence in a lagging archive is not evidence (§9.5).** The
archive's newest pairing is **07:32:59.701Z**, 27.2 m behind the wall clock, and the cadence says the
**07:52:59Z slot exists and is not yet archived**. My independent check therefore covers
**06:25:40Z → 07:32:59Z only.** The 07:52:59Z slot falls after round 5's v154 exposure
(07:49:51→07:50:07Z) and is **UNVERIFIED on every surface I can read** — the scheduler's own leak
check ran at 07:50:15Z, i.e. *before* that slot, and its live-platform fallback read `sum=0.00`
which is likewise a pre-slot reading. **The v154 rollback was confirmed on the `Active bot:` line at
07:50:07Z, 2 m 52 s before the slot, so the structural argument is sound; the confirming row simply
does not exist yet.** A successor re-runs this query once the archive passes 07:52:59Z.

**Elo cost so far: zero adverse leaked matches, therefore zero of the −8 Elo/match budget spent.**
The −40 Elo halt (§10.5b) has not been approached — the gate has read `sum=0.00, n=0` on every
evaluation since 07:40:13Z, correctly routing through the live platform read because the archive was
47–57 minutes stale.

---

## 7. CONTROLS RUN — every instrument in this document was driven to the other verdict

A check that has never produced the other verdict has not been seen to check.

| # | instrument | control | expected | **observed** |
|---|---|---|---|---|
| 1 | leak-check filter (`ourver ∈ {140,154}`, `created > clock2`) | complement group: same filter **before** clock2 | must be non-empty, or the zero is a broken filter | **72 arm pairings, 2026-08-14T11:52:59Z … 2026-08-15T15:52:59Z** ⇒ the query can return arm rows; the post-clock2 zero is a real zero |
| 2 | leak-check date filter | corrupt clock2 to 00:00:00Z | more rows if the date filter is live | 0 — **uninformative**, because no arm held the slot at any point today. Reported as a control that did **not** discriminate; #1 and #3 are the ones that carry the check |
| 3 | leak-check `ourver` filter | mutate the arm set to `{152}` | must return exactly the 4 holder rows | **4** ⇒ the version filter discriminates |
| 4 | game-share reader | invert the `our_won` column | shares must become complements, diff must flip sign | A 56.0 % / B 64.0 %, diff **+8.0 pp** ⇒ the outcome column is genuinely read |
| 5 | arm assignment | swap the v140/v154 → A/B labels | diff must mirror | **+8.0 pp** ⇒ the arm label is load-bearing, not decorative |
| 6 | `our_won` not a constant column | inspect per-match spread | must vary | per-match scores span **1/5 … 4/5** across 20 matches, 45/100 overall |
| 7 | §9.3 pin assertion | assert each cell against a **different** cell's registered `theirver` | must ALARM | Juusto rows are `13` ×25 — asserting `119` or `23` alarms; asserting `13` passes ⇒ the assertion can fail |
| 8 | accept count | reconcile state tape against a surface it does not write | must agree | tape 25 ≡ `our_matches.tsv` 25 ≡ `.rate_ledger` 25 |
| 9 | round-3 "zero attempts" | look for rejected rows, not just accepted ones | a fired-and-rejected round leaves ledger entries and an outfile | **neither exists** in 07:06:13–07:29:39 ⇒ skipped, not rejected |

---

## 8. WHAT A SUCCESSOR OWES THIS LEG

1. **Re-run §6's leak query once `ladder_games.tsv` passes 07:52:59Z** — that slot is the only
   unverified pairing boundary in the leg's life.
2. **Route the replay decode for the 25 leg match ids.** Until `join.tsv` carries them, **the
   secondary (ITT RMST₃₀₀) and its reversal falsifier — the thing the prereg says the leg is
   actually buying — cannot be computed at all**, and neither can map mix (§6.2).
3. **Decide on B/not_adgato.** Left alone it reappears at round 23. It is the cell most exposed to
   `CUT-SHORT` exclusion, and the exclusion would be caused by a halt rather than by the opponent.
4. **Do not quote −8.0 pp against −7.7 pp.** §4.4.
5. **The scheduler log is `>` not `>>`** (one-character fix, already routed by the side lane at
   s44). Every relaunch destroys the leg's narrative; this read-out had to reconstruct rounds 0–5
   from three other surfaces because of it.

---

*Read-only research output. No bot, submission, scheduler, `HANDOVER.md` or `PROGRAMME.md` was
touched. No match was fired. Ages and clocks from `date -u` and `stat` in the same shell calls.*
