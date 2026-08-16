# RATED DAY DECODE — UTC 2026-08-16 (partial day), with 2026-08-15 as comparison

**Written:** 2026-08-16T08:04:16Z (`date -u`, same shell call as the queries below).
**Repo HEAD at write time:** `7a96d216` (`2026-08-16T10:03:37+02:00` = `08:03:37Z`).
**Lane:** research arm, read-only. No bot edits, no matches fired, no verdicts. This
file is the only artefact written.

---

## 0. INSTRUMENT PROVENANCE AND FRESHNESS

| source | how read | mtime (UTC) | newest content |
| --- | --- | --- | --- |
| `corpus/ladder_games.tsv` | 5,470 data rows, per-GAME grain, columns `match created opp oppver ourver ourbef oppbef map winner_seat won cond turns s3` | `2026-08-16T07:55:01Z` | **newest row `created` = `2026-08-16T07:32:59.701Z`** |
| `corpus/league_matches.tsv` | 49,662 rows, league-wide, used ONLY for opponent version timelines | `2026-08-16T07:55:56Z` | newest `createdAt` = `2026-08-16T07:52:59.793Z` |
| `elo_history.tsv` | poller tape, integer rating + `matches` counter | `2026-08-16T07:56:58Z` | `2026-08-16T08:02Z` row |
| `fcode match list --mine --type ladder --json --limit 200` | run `2026-08-16T08:00:18Z`, returned 100 matches | live | `createdAt 2026-08-16T07:52:59.793Z` |

**AGE OF THE NEWEST ROW USED:** the newest `ladder_games.tsv` row was created
`07:32:59Z` and this decode was written at `08:04:16Z` — **31 minutes 17 seconds old**.
At a 20-minute pairing cadence that is **~1.6 cadences**, i.e. right at the edge where a
monitor should refuse to print a verdict. It does not blind this report because the
platform reconciliation below closes the gap explicitly.

### 0.1 CORPUS ↔ PLATFORM RECONCILIATION (the archiver lag, measured not assumed)

> The brief's rule: *an ABSENCE in the tape is not evidence of absence.* So it was checked.

```
2026-08-15   platform 72 matches   in corpus 72   MISSING 0
2026-08-16   platform 24 matches   in corpus 23   MISSING 1
   -> 2026-08-16T07:52:59.793Z  0033 (A) 2 - 3 OpenSverige (B)   [we won 3/5]
```

**The archive lags by exactly one match — the most recent one.** That match is included
in every MATCH-level and ELO figure below (the platform list carries score, versions,
ratings and `eloDelta`) and is **excluded** from every GAME-level figure that needs
`cond` / `turns` / `map`, because those come only from the decoded replay rows.

**Two denominators are therefore in play and each number below says which:**
* **115 games / 23 matches** — corpus grain (win condition, kill turns, maps).
* **120 games / 24 matches** — platform grain (game share, Elo).

### 0.2 CONTROLS RUN BEFORE ANY NUMBER WAS TRUSTED

Each was required to produce the *other* verdict on a case where it must.

| # | check | expectation stated first | result |
| --- | --- | --- | --- |
| **A** | corpus `won`-column sum per match == platform score for us | 0 mismatches over the 99 corpus matches inside the platform window | **tested 99, mismatches 0** |
| **A-neg** | same check with one match's `won` column deliberately flipped | must FAIL | see §0.3 |
| **B** | day filter must separate two days | 08-16 and 08-15 shares must differ | **0.4957 vs 0.5111 — differ** |
| **B-neg** | day filter on nonexistent `2026-08-99` | must return 0 | **0 matches** |
| **C** | `delta == 32*(S − E)`, S = games_won/5, E = logistic on the 400 scale, ratings from `ratingABefore`/`ratingBBefore` | residuals ~0 across the day | **max \|residual\| = 0.000000000 over 24 matches** |
| **C-neg** | same, with the first match's score corrupted by +1 game | must show a large residual | **residual 6.4000 — DETECTED** |
| **D** | timely-kill threshold sweep must be monotone and hit both endpoints | r0 → 0, r1000 → all our core-kill wins (56) | **r0 = 0/115, r300 = 49/115, r1000 = 56/115** ✓ |
| **E** | the post-hoc "big three" split (§6.2) re-tested on 300 random 3-opponent groupings | a post-hoc extreme should pass often; measure how often | **68/300 = 22.7% of random groups also "exclude 0"** — the split is post-hoc and its nominal interval is optimistic. Reported as such. |
| **F** | opponent version-change detector must both fire and not fire | must flag known churners and stay silent on known-stable teams | fired on The Bisons / kladde / gsxWins / lingling / team lazy / Well have a look / 0033; **silent on HTTP 418, Coreflood, Juusto, not adgato** ✓ |

**0.3 — a control that did NOT execute, recorded rather than hidden.** The A-neg
negative control (corrupt one match's `won` column and confirm the comparator fires) was
written but selected `list(by)[0]`, which fell outside the 100-match platform window, so
the branch never ran and printed nothing. **Control A therefore has a passing positive
arm and no demonstrated negative arm.** By this repo's own rule that is a check not yet
seen to check. Its load-bearing use here is small — Control C reconciles the same
quantity from a different direction (platform score → Elo → observed rating movement,
max residual 0) and does have a demonstrated negative arm — but the gap is stated, not
papered over.

### 0.4 KNOWN CORPUS TRAPS AND WHETHER THEY BIND HERE

Per `docs/research/corpus-howto.md`:
* **TRAP 7 — `winner_seat` holds the WINNER's side, not ours.** **Not used anywhere in
  this document.** No by-seat statistic is computed.
* **TRAP 4 — `oppver` was the literal `'None'` before the 2026-08-13 backfill.**
  Checked: **0 nulls in the 115 rows of this day**; every value is a plausible integer
  and every one agrees with the same team's version in `league_matches.tsv` for the same
  timestamp.
* **`econ.tsv` dead columns (`shots`, `deliveries`).** Not touched — no economy column is
  read here.

---

## 1. EVERY RATED MATCH, 2026-08-16 UTC

`ourver` was **152 in every one of the 115 corpus games and all 24 platform matches** —
distinct `ourver` on the day = `{152}`. **No prototype leaked into the rated record
today.** Times are match `createdAt` (pairing time); every one lands at `:12:59`,
`:32:59` or `:52:59`, i.e. the 20-minute pairing clock is unchanged today.

`kills` = turns at which we destroyed their core. `deaths` = turns at which they
destroyed ours. `r1000` = a game that reached the tiebreak ladder.

| # | created (UTC) | opponent | theirv | ourv | ours/5 | eloΔ | our kill turns | our death turns | r1000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 00:12:59 | lingling_40h | 61 | 152 | 2/5 | −3.02 | 119, 228 | 113, 152, 153 | — |
| 2 | 00:32:59 | HTTP 418 | 103 | 152 | 3/5 | +2.72 | 238, 276, 321 | 181, 289 | — |
| 3 | 00:52:59 | kladde chatte tville (och oss) | 119 | 152 | **1/5** ⚑ | **−8.73** | 113 | 190, 297, 335, 458 | — |
| 4 | 01:12:59 | gsxWins | 46 | 152 | **0/5** ⚑⚑ | **−14.45** | *(none)* | 132, 207, 250, 360 | 1 (lost, `titanium_collected`) |
| 5 | 01:32:59 | Coreflood | 89 | 152 | 4/5 | +7.03 | 152, 163, 241, 320 | 345 | — |
| 6 | 01:52:59 | The Bisons | 9 | 152 | **5/5** | +16.40 | 79, 95, 118, 295, 299 | — | — |
| 7 | 02:12:59 | not adgato | 23 | 152 | 2/5 | +0.85 | 129, 146 | 201, 212, 287 | — |
| 8 | 02:32:59 | 0033 | 57 | 152 | 2/5 | −2.40 | 69, 141 | 167, 277, 335 | — |
| 9 | 02:52:59 | gsxWins | 46 | 152 | 3/5 | +4.09 | 152, 495 | 156, 192 | 1 (**won**, `titanium_collected`) |
| 10 | 03:12:59 | lingling_40h | 61 | 152 | 4/5 | +9.08 | 165, 200, 250, 253 | 105 | — |
| 11 | 03:32:59 | HTTP 418 | 103 | 152 | 2/5 | −4.51 | 215, 488 | 152, 166, 187 | — |
| 12 | 03:52:59 | kladde chatte tville (och oss) | 119 | 152 | 2/5 | −1.96 | 197, 213 | 180 | 2 (both lost, `titanium_collected`) |
| 13 | 04:12:59 | The Bisons | 9 | 152 | 3/5 | +1.07 | 88, 102, 209 | 69, 74 | — |
| 14 | 04:32:59 | lingling_40h | 61 | 152 | 4/5 | +8.13 | 155, 156, 178, 180 | 103 | — |
| 15 | 04:52:59 | 0033 | 57 | 152 | **0/5** ⚑⚑ | **−16.34** | *(none)* | 148, 235, 277, 401 | 1 (lost, `titanium_collected`) |
| 16 | 05:12:59 | team lazy | 231 | 152 | **5/5** | +13.36 | 125, 144, 192, 211, 543 | — | — |
| 17 | 05:32:59 | Juusto | 13 | 152 | 3/5 | +6.30 | 72, 133, 382 | 114, 203 | — |
| 18 | 05:52:59 | kladde chatte tville (och oss) | 119 | 152 | **0/5** ⚑⚑ | **−15.55** | *(none)* | 322, 346, 349, 374, **746** | — |
| 19 | 06:12:59 | not adgato | 23 | 152 | 2/5 | +1.75 | 76, 104 | 165, 184, 222 | — |
| 20 | 06:32:59 | gsxWins | 46 | 152 | **1/5** ⚑ | **−7.65** | 210 | 133, 204, 270, 284 | — |
| 21 | 06:52:59 | 0033 | 57 | 152 | **1/5** ⚑ | **−9.45** | 181 | 149, 209, 301, 561 | — |
| 22 | 07:12:59 | HTTP 418 | 103 | 152 | 3/5 | +2.74 | 105, 154, 178 | 243, 342 | — |
| 23 | 07:32:59 | Well have a look | 9 | 152 | **5/5** | +13.03 | 102, 143, 157, 167, 403 | — | — |
| 24 | 07:52:59 | 0033 | 57 | 152 | 3/5 | +3.61 | *not yet archived* | *not yet archived* | *n/a* |

**Win-condition breakdown, 115 archived games:**

| `cond` | we won | we lost | total |
| --- | --- | --- | --- |
| `core_destroyed` | 56 | 54 | 110 |
| `titanium_collected` | 1 | 4 | 5 |
| `harvesters` | 0 | 0 | 0 |
| `titanium_stored` | 0 | 0 | 0 |
| **total** | **57** | **58** | **115** |

Every one of the 5 non-`core_destroyed` games has `turns == 1000`; the `turns` set for
that group is exactly `{1000}`. **95.7% of today's games were decided by a core kill.**

---

## 2. GAME SHARE — THE CURRENCY

> `PROGRAMME.md`: `WIN_RATE_IS_VERDICT: no`. The ladder pays `32·(S − E)` with
> `S = games_won/5`, so the unit is the GAME. Match win rate is not reported as a headline.

**Population: OpenSverige, RATED LADDER matches only, v152 in 24 of 24 matches.
Clock: pairings `2026-08-16T00:12:59Z` → `2026-08-16T07:52:59Z`, a 7h40m partial UTC day.**

| population | games won / played | game share | matches |
| --- | --- | --- | --- |
| **2026-08-16, platform grain (complete)** | **60 / 120** | **0.5000** | 24 |
| 2026-08-16, corpus grain (archived subset) | 57 / 115 | 0.4957 | 23 |
| **2026-08-15, platform grain (full 24h)** | **184 / 360** | **0.5111** | 72 |
| match win rate 08-16 (reported for completeness only, NOT the currency) | 12 of 24 matches ≥3/5 | 0.500 | 24 |

**Headline: game share 0.500 — 60 games won of 120 played, across 24 rated ladder
matches, all by v152, pairings 00:12:59Z–07:52:59Z on 2026-08-16.** The corpus-grain
figure (0.4957 over 115 games) is what the interval arithmetic below uses, because
`cond`/`turns`/`map` exist only for those 115; the 5-game difference is the single
unarchived match, which we won 3–2.

### 2.1 CLUSTERING — enumerated and verified, not asserted

Clusters this data has: **MATCH** and **OPPONENT**.

**Day-level stratum (the whole day):**
* MATCH — can the stratum hold >1 member of a match? **VERIFIED: games per match within
  the day = exactly 5 for all 23 archived matches.** Cluster is **LIVE**.
* OPPONENT — **VERIFIED: HTTP 418 15, lingling_40h 15, gsxWins 15, kladde 15, 0033 15,
  not adgato 10, The Bisons 10, Coreflood 5, Juusto 5, team lazy 5, Well have a look 5.**
  Six opponents contribute more than one match. Cluster is **LIVE**.
* Both survive ⇒ **pooled rated DEFF = 1.529 (ICC ρ = 0.132)**.

```
2026-08-16   share 0.4957, n = 115 games
             half_width_95 = 1.96*sqrt(0.4957*0.5043*1.529/115) = 0.1130
          -> 0.496 ± 0.113   (naive, uncorrected, would have been ± 0.091)

2026-08-15   share 0.5111, n = 360 games
             half_width_95 = 1.96*sqrt(0.5111*0.4889*1.529/360) = 0.0639
          -> 0.511 ± 0.064
```

**Two-fixture comparison, 08-16 vs 08-15** (both RATED, so `DEFF_r` on both terms):
```
half_width_95 = 1.96*sqrt( p̄(1-p̄) * (1.529/115 + 1.529/360) ) = 0.1298
difference = 0.4957 − 0.5111 = −0.0155
-> DOES NOT EXCLUDE ZERO.
```
**Measured:** today's game share is 1.6 percentage points below yesterday's, against a
±13.0pp two-sample interval. **A 115-game partial day cannot separate these two days.**
No day-over-day claim is made.

**⚠ DIRECTION CHECK, per the standing rule.** "Today is not different from yesterday" is
a **fail-to-exclude** claim, and DEFF makes those *easier*, not harder. Restated as an
exclusion: *does the interval exclude a 10pp drop?* **It does not** — the interval spans
−14.5pp to +11.4pp. So the honest statement is **not** "no change"; it is **"a drop as
large as 14pp is still inside today's interval and this sample cannot see it."** A
one-day rated read at this n is a monitor, not a measurement.

---

## 3. KILL-ROUND PROFILE

**Population: 115 archived rated games, v152, 2026-08-16T00:12:59Z–07:32:59Z.**

### 3.1 Of games we WON

| | count | share of our 57 wins |
| --- | --- | --- |
| won by `core_destroyed` | **56** | **98.2%** |
| won on the r1000 tiebreak (`titanium_collected`) | 1 | 1.8% |

**Turn distribution of our 56 core kills:** min **69**, p25 **128**, **median 166**,
p75 **231**, max **543**.

| band | our kills | share of the 56 |
| --- | --- | --- |
| ≤ r100 | 6 | 10.7% |
| r101–200 | 30 | 53.6% |
| r201–300 | 13 | 23.2% |
| r301–500 | 6 | 10.7% |
| r501–999 | 1 | 1.8% |

### 3.2 TIMELY-KILL RATE — the `DEFENCE_ADMISSION_BAR` primary

Defined per `PROGRAMME.md` as the share of **ALL** games (not kill-conditioned — the
kill-conditioned form carries a collider) ending in a core-kill **by r300**.

| threshold | 2026-08-16 (n=115) | 2026-08-15 (n=360) |
| --- | --- | --- |
| our core-kill by **r200** | 36/115 = **0.3130** | 106/360 = **0.2944** |
| our core-kill by **r250** | 45/115 = **0.3913** | 134/360 = **0.3722** |
| **our core-kill by r300 (the primary)** | **49/115 = 0.4261** | **152/360 = 0.4222** |
| our core-kill by r400 | 52/115 = 0.4522 | 169/360 = 0.4694 |
| *their* core-kill of **us** by r300 | 40/115 = 0.3478 | 139/360 = 0.3861 |

**Measured: today's timely-kill rate is 0.426 (49 of 115 games).** Yesterday's on the
same instrument was 0.422 (152 of 360). The difference is +0.4pp; the two-sample
interval at pooled rated DEFF 1.529 is ±12.9pp, so this day cannot resolve movement in
either direction. **Both days are reported; no non-regression verdict is asserted here —
the bar is scored on a plank against its control, not on a calendar day, and that
scoring is the builder's.**

### 3.3 r1000 / tiebreak finishes — REPORTED SEPARATELY, A DEFEAT EVEN WHEN WON

**2026-08-16: 5 of 115 games = 4.3% reached r1000.** We "won" 1 of them
(`titanium_collected`, match #9 vs gsxWins) — **by `R1000_IS_DEFEAT` that game is a
defeat that happens to have paid rating.** The other 4 were losses.
**2026-08-15: 13 of 360 = 3.6%**, of which we "won" 4 (1 `titanium_collected`,
3 `harvesters`).

The r1000 rate is low on both days and neither day's tiebreaks touched
`titanium_stored`.

### 3.4 Our death profile (context for §4)

Of the 54 games where they killed our core: min **69**, median **208**, max **746**.
**Our median kill (166) still leads our median death (208) by 42 rounds today** — a
wider gap than the ~13-round race quoted in `CLAUDE.md` from the long-run corpus. On a
115-game day that is a description, not a trend.

---

## 4. ⚑ FLAGGED — BAD MATCHES BY THE LIVE HOLDER v152

**Every one of these was played by v152, the live holder. Six matches at ≤1/5, all
inside a 6-hour window, all concentrated on three opponents.**

| created | opponent | **their version** | ours | score | eloΔ |
| --- | --- | --- | --- | --- | --- |
| 01:12:59 | **gsxWins** | **v46** | v152 | **0/5** | **−14.45** |
| 04:52:59 | **0033** | **v57** | v152 | **0/5** | **−16.34** |
| 05:52:59 | **kladde chatte tville (och oss)** | **v119** | v152 | **0/5** | **−15.55** |
| 00:52:59 | kladde chatte tville (och oss) | v119 | v152 | **1/5** | −8.73 |
| 06:32:59 | gsxWins | v46 | v152 | **1/5** | −7.65 |
| 06:52:59 | 0033 | v57 | v152 | **1/5** | −9.45 |
| | | | | **3 wins / 30 games = 0.100** | **−72.17 total** |

**These six matches cost −72.2 Elo. The other eighteen matches of the day paid +78.3.
The day netted +6.08.**

### 4.1 The three shutouts, game by game — they are NOT the same failure

**01:12:59 vs gsxWins v46 — 0/5, mixed-length losses.**
```
archipelago   lost  core_destroyed  r250
valkyrie      lost  titanium_collected  r1000
nordkap       lost  core_destroyed  r360
drakkarfjord  lost  core_destroyed  r207
yulerune      lost  core_destroyed  r132
```

**04:52:59 vs 0033 v57 — 0/5, mixed-length losses.**
```
archipelago   lost  core_destroyed  r277
nordkap       lost  core_destroyed  r235
antler        lost  titanium_collected  r1000
midgard       lost  core_destroyed  r401
frostgate     lost  core_destroyed  r148
```

**⭐ 05:52:59 vs kladde chatte tville v119 — 0/5, and EVERY loss is LATE.**
```
icefloe       lost  core_destroyed  r746
auroraveil    lost  core_destroyed  r322
yulerune      lost  core_destroyed  r346
valkyrie      lost  core_destroyed  r374
drakkarfjord  lost  core_destroyed  r349
```
**Earliest death in that match is r322.** We were not rushed down; we survived the
r150–250 window in all five games, failed to convert in any of them, and were then
ground out between r322 and r746. **This is the shape `R1000_IS_DEFEAT` was written
about — a 0/5 that is a conversion failure, not a defensive one — and it is
categorically different from the other two shutouts, which contain deaths at r132 and
r148.** Flagged as the most informative single match of the day.

### 4.2 Opponent versions that CHANGED — cross-checked against `league_matches.tsv`

> The rule this obeys: *a null or stale version column reads as "no version change" to
> any cut that trusts it.* So the timeline was rebuilt league-wide from BOTH seats of
> `league_matches.tsv` (49,662 rows), not from our own matches.

**⭐⭐ THE BISONS SHIPPED v10 TODAY.**
```
The Bisons   08-15 versions = [9]    08-16 versions = [9, 10]
   -> v10 FIRST SEEN LEAGUE-WIDE at 2026-08-16T07:32:59.701Z
```
Both of our Bisons matches today (01:52:59 → 5/5, 04:12:59 → 3/5) met **v9**. Our
Bisons record is `v9: 16/25 = 0.640` all-time in the corpus. **We have not yet played
v10 and the 8/10 above does not describe it.** Any read on The Bisons is now stale as
of 07:32:59Z today.

**Opponents whose version differs from yesterday (all changed BEFORE today's window, so
today's matches are internally consistent):**

| opponent | 08-15 versions seen league-wide | 08-16 | note |
| --- | --- | --- | --- |
| **kladde chatte tville (och oss)** | **94, 96, 97, 99, 101, 102, 103, 105, 106, 107, 109, 111, 113, 114, 116, 118, 119 — seventeen** | 119 | **The fastest shipper on the board by a wide margin.** Our all-time record vs their v119 is **5/20 = 0.250**; vs their v94 it was 3/5. They iterated 17 times in a day and the result beats us. |
| gsxWins | 39, 42, 43, 44, 45, 46 | 46 | Our record: `v39 6/20`, `v42 3/5`, `v45 0/5`, **`v46 4/15 = 0.267`** — a monotone decline across their ship sequence. |
| **0033** | **57 and 60 — and the direction is BACKWARD** | 57 | 0033 ran v60 through mid-08-15 then **reverted to v57**. Our record is `v60 6/20 = 0.300` and `v57 13/45 = 0.289` — **the rollback does not explain today's 6/20; we were at ~0.29 against both.** |
| lingling_40h | 59, 60, 61 | 61 | v61: 14/25 = 0.560 all-time. |
| team lazy | 230, 231 | 231 | v231: 5/5 (one match). |
| Well have a look | 8, 9 | 9 | v9: 5/5 (one match). |
| HTTP 418 · Coreflood · Juusto · not adgato | unchanged | unchanged | **detector correctly silent — Control F's negative arm.** |

**A pinned-triple instrument alarm was checked for and is absent:** within each of
today's matches, all five games carry a single `oppver`, and no opponent shows two
versions inside our own day's matches.

### 4.3 Opponents and maps conspicuously below the day average

**Day average game share: 0.4957 (57/115, corpus grain).**

**Per-OPPONENT.** Cluster enumeration for this stratum: MATCH cluster **LIVE** (six
opponents have 2–3 matches today, verified above); OPPONENT cluster **DEAD by
construction** (a per-opponent cell holds exactly one opponent). ⇒ **within-opponent
rated DEFF = 1.366.**

| opponent | theirv | won/n | share | matches | ±95% (DEFF 1.366) | timely-kill (≤r300) |
| --- | --- | --- | --- | --- | --- | --- |
| **kladde chatte tville** | 119 | **3/15** | **0.200** ⚑ | 3 | ±0.237 | 3/15 = 0.200 |
| **0033** | 57 | **3/15** | **0.200** ⚑ | 3 | ±0.237 | 3/15 = 0.200 |
| **gsxWins** | 46 | **4/15** | **0.267** ⚑ | 3 | ±0.262 | **2/15 = 0.133** |
| not adgato | 23 | 4/10 | 0.400 | 2 | ±0.355 | 4/10 = 0.400 |
| HTTP 418 | 103 | 8/15 | 0.533 | 3 | ±0.295 | 6/15 = 0.400 |
| Juusto | 13 | 3/5 | 0.600 | 1 | ±0.502 | 2/5 = 0.400 |
| lingling_40h | 61 | 10/15 | 0.667 | 3 | ±0.279 | 10/15 = 0.667 |
| Coreflood | 89 | 4/5 | 0.800 | 1 | ±0.410 | 3/5 = 0.600 |
| The Bisons | 9 | 8/10 | 0.800 | 2 | ±0.290 | 8/10 = 0.800 |
| team lazy | 231 | 5/5 | 1.000 | 1 | ±0.000† | 4/5 = 0.800 |
| Well have a look | 9 | 5/5 | 1.000 | 1 | ±0.000† | 4/5 = 0.800 |

† A Wald interval degenerates at p = 1. Those two cells have **no usable interval**; the
zero is an artefact of the formula, not a precise measurement. Flagged rather than
printed as if meaningful.

Only `kladde` and `0033` have an interval whose upper edge (0.437) sits below the day
average of 0.496. Everything else overlaps the day average.

**Per-MAP.** Cluster enumeration: MATCH cluster — **VERIFIED DEAD: (match, map) pairs
holding more than one game = 0 of 115**, i.e. a 5-game match uses five distinct maps, so
a map cell can never hold two games of one match. OPPONENT cluster — **LIVE**, a map
cell holds games against several opponents and sometimes the same one twice. ⇒ the
residual per-map DEFF is the ≈1.07 measured in `CLAUDE.md`, not the pooled 1.529.

| map | won/n | share | | map | won/n | share |
| --- | --- | --- | --- | --- | --- | --- |
| **frostgate** | **1/6** | **0.167** | | drakkarfjord | 6/11 | 0.545 |
| **fjordgate** | **1/5** | **0.200** | | midgard | 5/9 | 0.556 |
| **icefloe** | **1/5** | **0.200** | | antler | 5/9 | 0.556 |
| drumlin | 2/5 | 0.400 | | glacierkeep | 4/7 | 0.571 |
| nordkap | 4/9 | 0.444 | | auroraveil | 5/8 | 0.625 |
| archipelago | 4/9 | 0.444 | | yulerune | 6/9 | 0.667 |
| valkyrie | 5/11 | 0.455 | | ragnarok | 5/6 | 0.833 |
| royale | 3/6 | 0.500 | | | | |

**All 15 map cells hold 5–11 games. At n=6 and DEFF 1.07 the half-width on frostgate's
0.167 is ±0.30, which covers the day average.** The three low maps are named because the
brief asks them to be named; **no map effect is claimed, and one day of 115 games cannot
support one.** Note also that the low-map cells are not independent of §4.2 — frostgate
and icefloe each carry a game from one of the three shutout matches.

---

## 5. ELO ACCOUNTING

### 5.1 The formula reconciles EXACTLY

`delta = 32·(S − E)`, `S = games_won/5`, `E = 1/(1 + 10^((R_opp − R_us)/400))`, with
`R` taken from the platform's own `ratingABefore` / `ratingBBefore`.

**Max |residual| = 0.000000000 across all 24 rated matches of 2026-08-16.**
K = 32 confirmed again today. Negative control (score corrupted by one game) produced a
residual of 6.4000 — the check fires.

**Two sign-inverting matches today**, the phenomenon `CLAUDE.md` flags:
* **#7, 02:12:59 vs not adgato — a 2/5 LOSS that PAID +0.85 Elo** (they were rated 1874
  against our 1784; E = 0.373, S = 0.400).
* **#19, 06:12:59 vs not adgato — a 2/5 LOSS that PAID +1.75** (they were 1898, E = 0.345).
* Conversely **#13, 04:12:59 vs The Bisons — a 3/5 WIN that paid only +1.07**, because
  we were 47 points above them (E = 0.567).

### 5.2 The day's movement, three independent readings

| reading | value |
| --- | --- |
| sum of per-match `eloDelta`, 24 platform matches | **+6.082** |
| rating before match #1 (1784.351) → rating after match #24 (1790.433) | **+6.082** ✓ |
| `elo_history.tsv`, `00:00Z` row 1784 → `08:02Z` row 1790 | **+6** (integer column) ✓ |

**All three agree.** The `elo_history.tsv` `matches` counter moved **1071 → 1095 = 24**,
exactly the number of rated ladder matches the platform reports for the day — an
independent confirmation that no rated match is missing from this decode.

**Subtotal over only the 23 matches present in the corpus: +2.473.** The one
platform-only match (07:52:59 vs 0033, 3/5) contributed **+3.608** — over half the day's
net. **A decode that had trusted the archive's silence would have reported the day at
+2.5 instead of +6.1, a 59% understatement of the day's gain.** This is the concrete
cost of the lag and the reason the reconciliation in §0.1 is not ceremonial.

**⚠ `elo_history.tsv`'s `active_bot` column is tagged AT POLL TIME, not per match.** It
reads `v152` for all 97 rows of today. That happens to be correct today because v152 was
the holder for the entire window and `ladder_games.tsv`'s per-match `ourver` independently
says `152` in 115 of 115 games — but the agreement is a coincidence of a quiet day, not a
property of the column. **Per-match `ourver` remains the ground truth.**

### 5.3 Observed minus expected, per opponent

`E` here is the games-share the ladder's own ratings predicted for us at pairing time.

| opponent | matches | won/n | observed S | expected E | S − E | Elo |
| --- | --- | --- | --- | --- | --- | --- |
| **kladde chatte tville** | 3 | 3/15 | 0.200 | 0.473 | **−0.273** | **−26.24** |
| **0033** | 4 | 6/20 | 0.300 | 0.492 | **−0.192** | **−24.59** |
| **gsxWins** | 3 | 4/15 | 0.267 | 0.454 | **−0.188** | **−18.01** |
| HTTP 418 | 3 | 8/15 | 0.533 | 0.523 | +0.010 | +0.95 |
| not adgato | 2 | 4/10 | 0.400 | 0.359 | +0.041 | +2.60 |
| lingling_40h | 3 | 10/15 | 0.667 | 0.519 | +0.148 | +14.19 |
| Juusto | 1 | 3/5 | 0.600 | 0.403 | +0.197 | +6.30 |
| Coreflood | 1 | 4/5 | 0.800 | 0.580 | +0.220 | +7.03 |
| The Bisons | 2 | 8/10 | 0.800 | 0.527 | +0.273 | +17.46 |
| Well have a look | 1 | 5/5 | 1.000 | 0.593 | +0.407 | +13.03 |
| team lazy | 1 | 5/5 | 1.000 | 0.582 | +0.418 | +13.36 |
| **all** | **24** | **60/120** | **0.50000** | **0.49208** | **+0.00792** | **+6.08** |

The day's aggregate `S − E` is **+0.0079 game-share** — `32 × 24 × 0.007918664 = +6.0815`,
which is the day's Elo movement to five decimals. **v152 performed within eight tenths
of a percentage point of what its own rating predicted, across 120 games.** The +6.08 is
not a broad edge; it is the residue of a wide *distribution* — large overperformance
against six lower-rated opponents and large underperformance against the three
higher-rated ones in §4.

---

## 6. WHAT SURPRISED ME

**Written before explaining it away**, per `LOKI` point 4.

### 6.1 A 0/5 in which we were never rushed

Match #18 (kladde v119) is a shutout whose **earliest core loss is r322** and whose
latest is **r746**. I expected a 0/5 to look like the other two — a spread of deaths
including something under r200. It does not. We survived the entire r150–250 window
that `CLAUDE.md`'s defence clause is scoped to, in five out of five games, and lost all
five anyway. **The failure was conversion, not survival**, and no defence-shaped
intervention would have touched it. I have no explanation and am not offering one.

### 6.2 The whole day is a two-population day, and the split replicates on 08-15

Splitting the day on the three opponents that produced all six flagged matches:

```
2026-08-16   {kladde, 0033, gsxWins}   10/45 = 0.222
             all other 8 opponents     47/70 = 0.671
             gap = −0.449   hw95 (two-sample, DEFF 1.529 both) = 0.232   EXCLUDES 0
```
**A 45pp gap inside one day, one bot version, one 8-hour window.**

**⚠ THIS SPLIT WAS CHOSEN AFTER SEEING THE DATA, AND CONTROL E PRICES THAT.** Re-testing
300 random 3-opponent groupings of the same day, **68 of 300 (22.7%) also "exclude
zero"** on the same test. So the nominal interval above is optimistic and the test is not
by itself evidence.

**What *is* evidence is that the split, specified by 08-16, holds on 08-15 — a
different day, a different bot version for most of it, and a different match count:**
```
2026-08-15   {kladde, 0033, gsxWins}   29/85  = 0.341
             all other opponents      155/275 = 0.564
             gap = −0.222   hw95 = 0.150   EXCLUDES 0
```
Out-of-sample on the day dimension, the same three opponents are the same three
opponents. **Measured, not concluded:** on both days our rated record is bimodal by
opponent, and the same three names sit on the low side. Whether that is a stable
matchup property, a rating artefact (all three are rated near or above us) or something
about their current builds is not answerable from two days of ladder record — it needs
a pinned treatment leg, which is the builder's call.

### 6.3 The archiver lag concealed the day's largest single positive

Covered in §5.2 and repeated here because it is the surprise with an operational
consequence: **the single match missing from the corpus carried +3.608 of the day's
+6.082.** The lag was one match — the smallest possible non-zero lag — and it still
moved the headline by 59%. The stated daily-floor incident this decode exists to prevent
was a *bad* match going unseen; today the lag hid a *good* one. **The lag is not biased
toward bad news, and a decode that reads only the archive is wrong in an unpredictable
direction, not a conservative one.**

### 6.4 The Bisons shipped v10 during the last archived pairing slot of the window

`v10` first appears league-wide at `2026-08-16T07:32:59.701Z` — the same pairing slot as
our own match #23. Our 8/10 against them today is entirely against **v9**. This is
exactly the collinearity hazard `CLAUDE.md` records from the v102/Bisons-v4 episode, and
it is live again right now: **any Bisons number carried forward from today is a v9
number wearing a "The Bisons" label.**

---

## 7. LIMITS OF THIS DOCUMENT

* **Partial day.** 7h40m of pairings, 24 matches, 120 games. `2026-08-15` had 72
  matches / 360 games over 24h. The two are not like-for-like in size and no
  day-over-day inference survives the interval (§2.1).
* **One day is a small sample and no verdict is written here.** Every statement is of
  the form *"measured X on population Y at clock Z"*. Bar-clearing, plank attribution
  and ship decisions are the builder's.
* **Us-only.** Every share, rate and record in this file is OpenSverige's own rated
  record. None of it is a field-wide statistic.
* **`corpus/ladder_games.tsv` is rated-only by construction**, which is why it is the
  right denominator here — `meta_join` would silently pool unrated prototype legs into a
  rated win rate.
* **Control A has no demonstrated negative arm** (§0.3).
* **The per-opponent cells at 5 games are decorative.** Four opponents contributed a
  single match; their intervals span most of the unit interval or degenerate entirely.

---

*Generated by the research arm, 2026-08-16T08:04:16Z. Read-only decode; no bot, no
`PROGRAMME.md`, no `HANDOVER.md` and no submission was touched.*
