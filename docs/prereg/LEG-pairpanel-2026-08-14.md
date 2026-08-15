# LEG `pairpanel` — QUEUE #65, PAIRED PANEL FOR A SCREEN'S LOSING ARM

## ⛔ RULING: **NOT DRAFTABLE AT THE ROW'S SCOPE.** The row asks the expensive instrument to resolve a smaller effect than the cheap instrument has already measured.

**Drafted by a fresh opus subagent, no inherited context. Clock: `date -u` =
`2026-08-15T03:55:37Z`, same shell call as the readouts below. Nothing was
fired; every `fcode` call in this document is read-only.**

**STATUS: BEFORE any fixture. No panel was run, no submission was activated, no
match was created. This document is a ruling on whether a fixture is buyable,
written before buying one.**

**PROVENANCE: every file read, verbatim —**
`QUEUE.md:152` (row #65) ·
`docs/research/SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md` (all 450 lines) ·
`docs/coordination.md` (grepped, never read whole: `:50007`, `:51819-51830`,
`:51994-52000`, `:52145-52152`, and the `^--- 2026-08-1[45]` entry index to
`:54148`) ·
`docs/fcode-cli.md:27-44,60-67,123-141,223-295,320-420,510-587` ·
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md:441-560`
(Addendum 11 / Obligation 16) ·
`docs/research/SPEC-prereg-check-2026-08-14.md:1-175` ·
`tools/prereg_check.py:1-260` · `tools/target_value.py` (docstring + `--band`) ·
`results.tsv:365-367` · `corpus/meta_join.tsv.gz` · `CLAUDE.md` (booted).
**Live read-only CLI:** `fcode status`, `fcode submission list`,
`fcode match list --mine --type ladder --limit 60`,
`fcode match list --mine --type unrated --limit 200`.
**Result tapes for the arms under discussion were read** (`results.tsv`) — this
is a ruling about instrument cost, not a blind analysis, and the numbers it
prices come from those tapes on purpose.

**POOL ERA: post-2026-08-13-rotation.**
**SPANS-POOL-CHANGE: yes, and it cannot bind.** The derived boundary at
`2026-08-13T07:12:59Z` (10 new maps) sits inside the declared label's day. Every
input to this ruling is map-set-independent by construction — the rate limit
(5 accepts / 20 min), the unrated DEFF (1.833), the pairing clock, and the
logistic transitive map. **The three quantities I measured live — pairing
cadence, bucket occupancy, submission states — were all sampled
2026-08-14T07:52Z → 2026-08-15T03:55Z, entirely AFTER the boundary**, so the
span is a labelling artefact rather than a pooled population. *(The screen shares
quoted from `results.tsv` are local-fixture reads, which the pool rotation does
not touch.)*

---

## 0. THE ONE-PARAGRAPH ANSWER

The row wants a live field read for arms a local screen DROPPED near parity
(tonight: `GUNAXABL` 47.9, `SENTTHR` 49.6, `SEALFLOOR6` 47.6, `V140VS146` 53.0).
**A screen reading near 50 IS the prediction that the field difference is near
zero** — the transitive map is `d_field ≈ 0.1439 pp per Elo` and
`Elo = 400·log10(p/(1−p))`, so 49.6% predicts a **0.40pp** field difference and
47.9% predicts **2.10pp**. Resolving 0.40pp on the unrated surface takes
**110,021 paid games**; resolving 2.10pp takes **3,987**. Our unrated bucket is
**5 accepts / 20 min = 15 accepts/h = 75 games/h, confirmed observationally
tonight (max observed hour = exactly 15, never exceeded)**, and it is serialised
and shared with every other live instrument. **The arms this row exists to
rescue are, by construction, exactly the arms whose predicted field effect no
affordable live panel can see.** The admissible band under the most generous
budget I can build is `|screen − 50| ≥ 4.19pp`; all four named arms sit inside
it. The row's own stated primary (a concordance *slope*) is affordable only at
**2,640 accepts = 176 h of cap-rate window ≈ 15.7 days of the team's entire
spare unrated bucket**, for one coefficient, and errors-in-variables on its
x-axis roughly doubles that. **⇒ NOT DRAFTABLE. Close the row, ship its cheap
half, and keep screening locally where a game costs CPU instead of window.**

---

## 1. WHAT THE ARTEFACT WOULD HAVE BEEN — and why Obligation 13 has no diff

**This row is NOT a bot change. There is no `bots/` diff, no `file:line` in any
bot tree, and no treatment tree.** The artefact would have been a **fixture: a
repeatable operating procedure plus its bars** — a pinned six-opponent unrated
panel, an activation/rollback loop timed against the ladder's pairing clock, and
a registry joining each screen's two arms to their platform versions.

**MECHANISM METRIC READS: N/A — this leg has no mechanism and no bot diff. The
"treatment" is a measurement protocol; the quantity read is a game-share
difference computed from `fcode match list --mine --type unrated` rows joined on
`teamAVersion`/`teamBVersion`, not from any code path in `bots/`.**
**TREATMENT DIFF TOUCHES: N/A — zero files under `bots/`. INTERSECTION: N/A.**
Stated explicitly rather than left dangling, per the brief: OB13 exists because
LOKI-18 spent 25 unrated games on a metric that was byte-identical between arms.
A protocol leg cannot commit that error because it has no arms in the tree —
but it can commit the adjacent one, which is measuring a quantity no fixture can
resolve. **That is the error this document is about.**

---

## 2. THE MECHANICS, RE-VERIFIED TONIGHT — the constraint is real and it is structural

| fact | verification |
|---|---|
| **`fcode match unrated` plays our ACTIVE submission. There is no local-tree flag.** `POST /api/matches/unrated {opponentTeamId, sourceMatchId?, mapNames?}` — no bot upload, no own-side version selector. | `docs/fcode-cli.md:330-352` (CLI source read) |
| **`fcode match test BOT_A BOT_B` is local-bot-vs-local-bot and structurally cannot supply a real opponent** — no `opponentTeamId` parameter exists on that path. **So it is NOT an escape hatch from activation.** | `docs/fcode-cli.md:354-368`, `:129` |
| **`fcode submit` AUTO-ACTIVATES.** Submitting IS shipping. | `docs/fcode-cli.md:262-295` |
| ⭐ **BUT NO SUBMIT IS NEEDED: every arm in the screen inventory is ALREADY an uploaded `ready` submission.** `fcode submission list` tonight: v139 `ready`, v140 `ready`+active, v141/v142/v143/v145/v146 all `ready`. A swap is `fcode submission activate <N>` — no zip, no upload, no auto-activation ambiguity, verifiable on the `Active bot:` line. | live `fcode submission list`, `docs/fcode-cli.md:223-243` |
| **Rate limit 5 test/unrated per 20 min, shared bucket, rejected attempts count.** | `CLAUDE.md` (s28 correction, CLI verbatim) |

### ⭐ 2a. THE PAIRING CLOCK, RE-DERIVED LIVE — never hardcoded

`fcode match list --mine --type ladder --limit 60`, span
**2026-08-14T07:52:59.612Z → 2026-08-15T03:32:59.738Z (19.7 h, 60 pairings):**

```
minute mod 20 :  {12: 60}      <- 60 of 60
second        :  {59: 60}      <- 60 of 60
gaps          :  min 1199.718 s, max 1200.304 s, n gaps < 180 s = 0
```

**Tighter than the booted figure** (`CLAUDE.md`: 55/60 minute, 49/60 second,
"some gaps are 600 s"). In the current era the slots are `:12:59`, `:32:59`,
`:52:59` with sub-second jitter and **no short gaps at all**. Rated cadence
= 3.05 matches/h = **73/day**, which reproduces `CLAUDE.md`'s 72/day.
⚠ **This is re-derived, not inherited, and it must be re-derived again before
any use** — `CLAUDE.md` records that the offset has shifted at least once inside
an 18-hour span and my sample is 19.7 h, so it establishes the current era and
cannot exclude a future shift. **React to an OBSERVED pairing; never predict
one.**

### 2b. THE BUCKET, MEASURED — this is the binding constraint, not Elo

Our own account, `fcode match list --mine --type unrated` (newest 100 accepts,
2026-08-14T14:19:23Z → 2026-08-15T03:41:45Z = 13.4 h):

```
peak hour = 15 accepts (2026-08-14T17)  <- exactly the cap, never exceeded
mean      = 7.5 accepts/h               <- ~50% of cap
```

⇒ **spare ≈ 7.5 accepts/h.** And the multi-account lever is **NOT available on
current evidence**: `meta_join` 2026-08-14 unrated rows are **league-wide**
(`us_side = none` for 3,469 of 4,500 games; 58 distinct opponents), and our own
team's share is ~1,031 games ≈ 206 accepts/day ≈ **8.6 accepts/h — one
account's worth.** Teammates hold accounts and therefore buckets in principle,
but **nobody else is firing**, so a 3-account coordinated burst is a
team-coordination proposal for Magnus, not capacity this lane can spend.

---

## 3. THE AFFORDABILITY ARITHMETIC — the deliverable

### 3a. Cluster enumeration, performed rather than asserted

**SURFACE: unrated.** **CLUSTER UNIT: match+opponent.**
Panel stratum = one arm's panel read: 6 opponents × 5 matches/cell × 5 games.
1. **Clusters this data has: MATCH and OPPONENT.** (No third; no window effect
   has been shown to bind.)
2. **MATCH — can the stratum hold >1 member?** **YES.** An accepted challenge
   returns exactly 5 games and all 5 land in the same arm's stratum
   (`GAMES_PER_ACCEPT = 5`, platform fact, `tools/prereg_check.py:106`).
   **SURVIVES.**
3. **OPPONENT — can it hold >1 match against the same opponent?** **YES, and
   more densely than any cut this project has priced: m̄ = 5.0 matches per
   opponent per cell by construction**, against the m̄ = 1.98 that produced the
   small per-map residual. **SURVIVES.**
⇒ **Both live ⇒ pooled unrated DEFF = 1.833.**
⚠ **1.833 is a FLOOR here, not a ceiling**: it was measured on the archived
unrated pool, whose opponent cluster is far sparser than a 5-matches-per-cell
panel. A design that concentrates the cluster cannot inherit a constant measured
on a diffuse one and call it conservative.

**⛔ AND THE SOURCE DOCUMENT UNDER-CORRECTED — a correction that fails in the
flattering direction, which is the direction `CLAUDE.md` names.**
`SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md:344` quotes *"a two-arm 95% MDE of
~13pp on the unrated surface (DEFF 1.833)"*. **The parenthetical and the number
disagree: 13pp is what DEFF 1.434 gives.** Recomputed at n = 150/arm:

```
DEFF 1.434 (within-opponent, opponent cluster REMOVED) -> +-13.6pp   <- the doc's number
DEFF 1.833 (pooled, both clusters LIVE)                -> +-15.3pp   <- correct for this stratum
```

The opponent cluster cannot be removed from a panel that puts five matches in
every opponent cell. **The spec's headline MDE is 13% too narrow, and it is the
number the QUEUE row was costed against.** *(Half-width function audited against
`tools/prereg_check.py`'s published fixtures — EVICT58 25 games unrated
within-opponent reproduces at ±23.5pp, matching the committed value.)*

### 3b. What a screen share PREDICTS on the field

`G = 400·log10(p/(1−p))`; `d_field = G × 0.14391 pp` (derivative of the logistic
at p = 0.5; checked against the exact two-sided form at G = 65 → 9.32pp exact vs
9.35pp linear).

### 3c. ⭐ THE TABLE. Paid side = the losing arm; the winning arm is the incumbent and its side is free

`n paid` assumes the free (incumbent) side is grown arbitrarily large — the most
generous assumption available, and it halves the paid n. One burst = 5 accepts =
25 games = one pairing gap. Exposure per burst ≈ 90 s of slot-hold inside
1,199.7 s of measured clear air.

| screen | G (Elo) | predicted `d` | n paid | bursts | hours | **Elo UB (conservative)** | Elo UB (refined) |
|---|---|---|---|---|---|---|---|
| **59.26** SEALREPAIR | +65.1 | **9.37pp** | 201 | 8 | 2.7 | **−3.2** | −0.24 |
| **57.06** V140VS143 | +49.4 | 7.11pp | 348 | 14 | 4.6 | −5.6 | −0.42 |
| **56.80** V140VS142 | +47.5 | 6.84pp | 376 | 15 | 5.0 | −6.0 | −0.45 |
| 53.63 V141VS140 | +25.3 | 3.64pp | 1,331 | 53 | 17.8 | −21.3 | −1.60 |
| 53.05 X3R0V134 | +21.2 | 3.05pp | 1,888 | 76 | 25.2 | −30.2 | −2.27 |
| **53.0 V140VS146** ← row's case | +20.9 | 3.00pp | 1,951 | 78 | 26.0 | −31.2 | −2.34 |
| **47.6 SEALFLOOR6** ← row's case | −16.7 | 2.40pp | 3,052 | 122 | 40.7 | **−48.8** | −3.66 |
| **47.9 GUNAXABL** ← row's case | −14.6 | 2.10pp | 3,987 | 159 | 53.2 | **−63.8** | −4.78 |
| 50.59 ferry-first | +4.1 | 0.59pp | 50,567 | 2,023 | 674 | −809 | −60.7 |
| **49.6 SENTTHR** ← row's case | −2.8 | 0.40pp | **110,021** | 4,401 | **1,467** | **−1,760** | −132 |

**The Elo column, both ways, because the honest answer is a range:**
* **Conservative (budgeted): 5.0% leak per burst × −8 Elo.** 5.0% is the
  rule-of-three 95% upper bound on `0 off-cadence pairings observed in 60`.
* **Refined: 0.375% per burst** — an off-cadence pairing must ALSO land inside
  the 90 s exposure, which is 7.5% of a 1,200 s gap.
* **Point estimate under both: ZERO leaked rated matches**, which is what the
  measured clock says and what the s28/s29 procedure achieved in practice.
**⇒ Elo is NOT the binding constraint. The bucket is.** Say it that way round;
inflating the Elo number would make the kill look better than its true reason.

### 3d. THE ADMISSION RULE — derived, and it is the opposite of the row's title

Fix a paid budget, invert the half-width, and read off the screen share that
budget can speak about:

```
paid   400 games ( 16 bursts,  5.3 h) -> detects 6.63pp -> admits screen >= 56.60% or <= 43.40%
paid 1,000 games ( 40 bursts, 13.3 h) -> detects 4.20pp -> admits screen >= 54.19% or <= 45.81%
paid 2,000 games ( 80 bursts, 26.7 h) -> detects 2.97pp -> admits screen >= 52.96% or <= 47.04%
```

**ADMISSION RULE (the answer the brief asked for): a losing arm qualifies for a
paired-panel field read iff `|screen_share − 50| ≥ 4.19pp` at a 1,000-game paid
budget — i.e. `≥ 54.2%` or `≤ 45.8%`.**

⛔ **AND THAT RULE ADMITS NONE OF THE ARMS THE ROW WAS COMMISSIONED TO RESCUE.**
`GUNAXABL` 47.9 · `SENTTHR` 49.6 · `SEALFLOOR6` 47.6 · `V140VS146` 53.0 — **all
four inside `[45.8, 54.2]`.** Doubling the budget to 80 bursts moves the band to
`[47.0, 53.0]` and still admits none of them. **This is not a budget shortfall
that a bigger allocation fixes; it is the definition of the DROP band. An arm is
in the DROP band precisely because its measured effect is small, and a small
effect is what a 15-accept/hour serialised fixture cannot see.**

### 3e. THE COST INVERSION — the finding underneath all of it

A local screen game costs CPU: parallel, overnight, 5,400 games in a shard, DEFF
0.98 (balanced by construction). A live panel game costs 1/75th of an hour of a
serialised shared bucket plus slot-hold risk, at DEFF 1.833.

```
resolution at n = 5,400 local  (DEFF 0.98) : +-1.32pp on a one-sample share
resolution at n = 5,400 unrated (DEFF 1.833): would need 5,400 PAID games = 216 bursts = 72 h
```

**⇒ For resolving a small difference the LOCAL screen is the cheap instrument by
one to two orders of magnitude. The live panel's unique value is not
resolution — it is that its enemy-side population is the ladder's** (zero of our
forward turrets died in 480 arena games vs 46.9% on the ladder; our bot builds
1.26 gunners/game vs Leviathan's 13.86). **That is a BIAS, and a bias is
detected by measuring a MECHANISM RATE at n in the dozens, not by measuring a
game share at n in the thousands.** The row proposes to spend the live fixture's
scarce currency on the one job the local fixture already does better.

---

## 4. THE ROW'S OWN PRIMARY — the slope — priced, then killed on its own terms

QUEUE #65's registered primary is *"concordance … as a SLOPE not a sign"*:
regress `panel_share_A − panel_share_B` on the screen's transitive prediction,
null **slope = 1** (perfect transitivity) against **slope = 0** (screen predicts
nothing). A regression does NOT need each pair resolved — noise in `y` inflates
`SE(β)` without biasing it — so this is the row's strongest form and it deserves
a real price.

Spread of `x` across the eight screens in the inventory
(`SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md:166-177`): **SD(x) = 3.29pp.**

```
n = 150/arm  ->  SE_y = 7.82pp  ->  k = 44 pairs for 80% power on slope 1 vs 0
n = 300/arm  ->  SE_y = 5.53pp  ->  k = 22 pairs         (k x n is invariant: 6,600)
TOTAL, either split: 2,640 accepts = 13,200 games = 176 h of CAP-RATE window
   at our measured spare of 7.5 accepts/h  ->  352 h  =  14.7 days
   at the team's measured 8.6 accepts/h    ->  ~15.7 days of ALL spare bucket
```

**⇒ The QUEUE row's *"~40 paired observations in a fortnight"* is arithmetically
right and operationally wrong: it double-books the bucket.** A fortnight of
panel at this rate consumes the entire spare unrated capacity — the same
capacity that runs every calibration panel, every dose probe and every live
screen — and displaces roughly 44 legs of mill throughput to buy one instrument
coefficient. Under `R1000_IS_DEFEAT` and *"the exploit hunt is the job"*, that
trade loses.

### ⛔ 4a. AND THE x-AXIS IS MEASURED WITH ERROR, WHICH ROUGHLY DOUBLES THE PRICE

The screen's own cross-host reproducibility is already flagged at
`results.tsv:367`: **SEALREPAIR local 59.30 vs remote SEALREPAIRR 56.77 — the
same comparison, two hosts, z ≈ 2.7**, i.e. `x` for one pair reads **9.37pp and
6.81pp**. From that single replicate, `sd(x_error) ≈ 1.81pp`, against
`var(x_observed) = 3.29² = 10.82`:

```
var_true = 10.82 - 3.28 = 7.54    ->  attenuation 1/(1+0.435) = 0.70
```

**A PERFECTLY transitive screen would produce an expected slope of ~0.70, not
1.0** — so the row's registered null of `slope = 1` is **wrong by
construction**, and the attenuation factor is estimated from **one** replicate
(df = 1) and is therefore itself unusable. The `slope ≠ 0` test survives
(attenuation moves an estimate toward zero, never past it) but loses power by
`1/0.70² ≈ 2.06×`: **k ≈ 90 pairs, ~30 days of all spare bucket.**
⚠ Stated as a **cost multiplier on §4, not as an independent kill** — the kill is
§3d and §4's headline number.

---

## 5. WHAT I RECOMMEND INSTEAD

**1. CLOSE #65's panel half. Annotate the row rather than leaving it live** — the
brief notes nine of thirteen rows tonight were dead with `QUEUE.md` never
updated, and a row that looks live is worse than a row that is closed.

**2. SHIP THE CHEAP HALF. It needs no prereg and no panel.** Already banked as
W3 (`docs/coordination.md:51994`): **record BOTH arms' platform versions per
screen.** `results.tsv` keys screens by local tree name only, and
`corpus/version_trees.tsv` has no entry for x3r0's v134/v141/v142/v143/v145 —
which is why the validity join had to be rebuilt by grepping
`docs/coordination.md`. **It is a schema line, not an experiment.** Nothing
retroactive substitutes for it, and it costs one field.

**3. WRITE THE IMPLIED TRANSITIVE GAP INTO EVERY SCREEN PREREG NOW** —
`IMPLIED TRANSITIVE GAP: +XX.X Elo (95% CI [a,b]) from share p @ n`. **Free,
immediate, and it is the only part of §5c that does not need the panel.** It
also makes §3d's arithmetic visible at the moment a screen is written: a screen
reading 49.6% would carry `+2.8 Elo` on its face, and nobody would then propose
buying a live read of it.

**4. IF A LOSING ARM EVER *MUST* GET A LIVE READ**, §3d's admission rule and the
loop below are ready. **The loop is the reusable artefact from this row and it
is worth keeping even though I recommend against firing it:**

```
PER BURST (one per pairing gap; ~90 s of slot-hold in 1,199.7 s of clear air)
 0. Re-derive the pairing clock TODAY:
      fcode match list --mine --type ladder --limit 60   -> minute mod 20, second, min gap
    Refuse to proceed if any observed gap < 300 s. NEVER hardcode the offset.
 1. WAIT for an OBSERVED pairing to appear (react, do not predict).
 2. fcode submission activate <LOSER_VERSION>
 3. VERIFY on the `Active bot:` line of `fcode status`. ⛔ NEVER on $? —
    `fcode status` exits 0 while printing `Error: True`.
 4. Fire 5 x `fcode match unrated <TEAM> --match <PINNED_PAST_MATCH_ID>`.
    Count ACCEPTS, not attempts (rejected attempts consume the bucket).
 5. fcode submission activate <INCUMBENT>;  VERIFY the `Active bot:` line again.
 6. Serve the remaining ~18 min of the bucket window WITH THE INCUMBENT LIVE.
    A retry is a NEW burst after a NEW observed pairing — never an overrun.
 7. AUDIT: read `teamAVersion` off `fcode match list --mine --type unrated` for
    the 5 matches. The platform stamps which version actually played; that is
    the only proof the swap bound to the challenge, and it is not assumed.
    ⛔ A pinned set whose decoded `oppver` values DIFFER is an INSTRUMENT ALARM:
    report it and do not read the cell.
```

**PINNED: YES, and the reason is that this is a matched-pair TREATMENT leg, not
a calibration panel.** `CLAUDE.md`'s rule — pin treatment legs, never pin
calibration panels — resolves cleanly here: a matched-pair design cannot absorb
opponent variation, so churn is noise and must be frozen with
`--match <past_match_id>`. **It must be registered under a different name from
the calibration panel or the next reader will apply the wrong rule to one of
them** (the source doc makes the same point at `:350-355`).

**5. THE ONE LEVER THAT WOULD CHANGE THE VERDICT, named for Magnus, not spent by
this lane:** the 5-per-20-min bucket is **per account**, and OpenSverige has four
members (x3r0, Jimmy76, Mr.Smith, Moonfarm) submitting to one shared slot.
**Three accounts firing into the SAME 90-second slot-hold would deliver 15
accepts = 75 games per burst — cutting bursts, wall clock and Elo risk by 3×**
and bringing §4 from ~15 days to ~5. The tape shows nobody but this account is
currently firing unrated, so this is a **team-coordination question**, not
available capacity. **It is the only route to affordability I found, and it is
not a technical one.**

---

## 6. REGISTRATION BLOCK — declared so the ruling is checkable, not so a leg can fire

**No fixture is registered by this document. These lines record what the leg
WOULD have declared, so the arithmetic above can be audited by the same tool
that audits real preregs.**

**TARGET BAND: N/A — no opponent is beaten by this leg.** It is an
instrument-validation protocol with no ladder payout channel; `target_value.py`
prices matchups, and this leg's product is a coefficient. **For the record, the
gate was run** (`.venv/bin/python tools/target_value.py --band`, 2026-08-15,
our live rating **1726**, rank #24, active **v140**): 14 admissible teams, gaps
**−66 .. +117**, a 5-0 pays **+12.98 .. +21.20**, reachable **YES** — so the
band is healthy and the leg still has no claim on it. **The gate's own caveat
applies and is why this is not quoted as a payout: opponent ratings are CACHED
(newest observation 0.9 h old) and must be verified live before any selected
target is priced.**

**PINNED: YES — treatment leg, `--match <past_match_id>` per cell, mandatory
(see §5.4). A pinned set with differing decoded `oppver` is an instrument alarm.**
**SURFACE: unrated.**
**CLUSTER UNIT: match+opponent (both clusters survive — enumeration in §3a).**
**ESTIMATOR: difference of two per-arm game shares, `panel_share_A −
panel_share_B`, games as the unit, DEFF-corrected two-arm 95% interval.**
**PLANNED n: 0 games — NOTHING IS PLANNED. This document buys no games.** The
sizes it prices are §3c's table (201 to 110,021 paid games per arm, by screen
margin) and §4's 13,200 games for the slope.
**BOUNDARY: 0 accepts = 0 games — no fixture is authorised by this document.**
**CUT-SHORT: 0 games — a leg that is not started cannot be stopped early, so the
floor equals the planned n (0 ≤ 0) and no short-leg claim is licensed.**
**BAR: N/A — POINT RULE ONLY, AND DELIBERATELY SO. This document registers NO
BAR and therefore licenses NO exclusion claim about any arm.** Its output is the
admission rule of §3d and the cost table of §3c.
**BASE RATE: 50.00pp — a zero difference between two arms on the same pinned
panel. BASE RATE SOURCE: the null of a matched-pair design; no observed rate is
used as an input anywhere in this document.**
**BAR SOURCE: N/A — no bar. Per Obligation 16 the MDE is stated as the
CONSTRUCTION of §3d's admission rule rather than beside a bar: `MDE = 4.19pp at
a 1,000-game paid budget, DEFF 1.833`, and an arm is a MISS if its true field
difference is at or below that. ⛔ THE MDE IS DECLARED FROM THE BUDGET, NEVER
FROM AN OBSERVED SCREEN SHARE — sizing a panel off the point estimate of the
screen it is meant to adjudicate is exactly the circularity Addendum 11 names,
and it is the trap this row walks into if anyone sizes a cell off "the screen
said 56.8".**
**GATE RESOLUTION: the single gate is affordability, and it resolves: the
admissible band `[45.8, 54.2]` excludes all four candidate arms with no
overlap. Nothing here is UNRESOLVED; had it been, the pre-committed default is
the RESTRICTION — do not fire.**
**PRE-STATE: all four candidate arms are currently DROPPED and no live read
exists for any of them; v140 is active (`fcode status`, 2026-08-15T03:55Z) and
v139/v141/v142/v143/v145/v146 are all `ready` and reactivatable without a
submit. That is the state this ruling leaves unchanged.**
**MAP SEGMENT: none expected — the ruling is a property of the rate limit and
the DEFF, both map-independent. No segment is claimed, so no segment ceiling is
owed.**
**DOSE: paid games needed to resolve the arm — 376 (screen 56.80%, ADMITTED) vs 3987 (screen 47.90%, REFUSED), n=10 screens priced.**
There is no bot mechanism to dose here — the
instrument under test is the admission rule itself, and **it was driven to BOTH
verdicts on real screens rather than only to the one that supports the ruling**:
three of the ten inventory screens clear the band and seven do not. A rule that
had only ever returned REFUSE would not have been seen to check.

### FALSIFIER

**This ruling is wrong, and #65's panel should be reopened, if ANY of the
following is shown:**

1. **The rate limit is not 5 accepts / 20 min for this account** — e.g. a
   sustained hour above 15 accepts from `fcode match list --mine --type unrated`.
   §3's entire cost column scales inversely with that number. *(Tonight: peak
   hour exactly 15, never exceeded, over 100 accepts / 13.4 h.)*
2. **A coordinated multi-account burst is actually available** (§5.5) — three
   accounts firing into one slot-hold cuts every cost by 3× and moves §4 from
   ~15 days to ~5. **This is the single most likely way this ruling flips, and
   it is a Magnus decision, not a measurement.**
3. **`match unrated` gains a local-bot or version selector**, or any path
   appears that plays a non-active submission against a real opponent. That
   deletes activation, deletes the Elo term, and deletes this ruling's premise.
   *(Re-check with `tools/cli_capabilities.py`, which alarms on unclassified CLI
   capabilities — the mechanised guard against exactly this going unnoticed.)*
4. **The transitive map is wrong** — i.e. a screen share of `p` does NOT imply a
   field difference of `400·log10(p/(1−p)) × 0.1439pp`. If the true field
   response to a screen margin is materially steeper, the near-null arms become
   detectable and the admission rule widens. **Note this cuts both ways and is
   the row's best defence: it is precisely the coefficient the row wanted to
   measure, so this falsifier is circular for the row and honest only for me —
   I am asserting the map, and the map is unmeasured.** ⚠ **State this as the
   ruling's main weakness rather than hiding it.**
5. **The pairing clock loses its structure** (off-cadence pairings, gaps under
   300 s). That would raise the Elo term from a rounding error to the binding
   constraint and make the verdict *more* negative, not less — listed for
   completeness, not as a route to reopening.

---

## 7. WHAT I AM NOT CLAIMING

* **Nothing here retires the screen or `X3R0_SLOT_RULE` (`PROGRAMME.md:28`).**
  Point 6 governs: a corpus statistic and a cost calculation may **prioritise**
  a road, never **close** one. This is written **beside** the screen rule, as
  `SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md` was.
* **Nothing here says the near-null arms are bad.** It says the opposite and
  says it precisely: **their true effect is small, and no fixture we can afford —
  local or live — separates them from the incumbent.** A DROP on a near-null
  screen is a **TIE-BREAK, not a measurement**, and that is a fair description of
  what those decisions have always been. Recording them as tie-breaks rather
  than as verdicts costs nothing and is more honest than either firing a panel
  or pretending the screen resolved it.
* **The one resolved concordance pair still stands.** P1 (v140/v139): screen
  59.26% @ 5,400, field +27.2pp CI [+4.2, +50.2] — **the screen was right on the
  one pair the field could adjudicate.** That is one observation and it is in the
  rule's favour.
* **I did not verify** that the s28 `−8 Elo per leaked rated match` figure still
  holds in the current era; it is inherited from `CLAUDE.md` and used only in a
  term I argue is not binding. Had it been binding, it would have needed
  re-measuring first.
