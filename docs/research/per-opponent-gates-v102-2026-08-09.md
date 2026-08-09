# Per-opponent decision surface for v102 (LOKI-8) — core-kill share and time-to-core-kill

**Research arm, 2026-08-09 22:47 CEST.** Programme currencies: `PRIMARY_CURRENCY: core_kill_share`,
`SECONDARY_CURRENCY: time_to_core_kill`, `WIN_RATE_IS_VERDICT: no`, `KILL_WINDOW_RND: 250`.

## THE HEADLINE

**Zero cells are gateable. Not one.** The v102 arm is **12 rated matches against 11 distinct
opponents**; after keying cells on `(opponent, opponent_version)` — which is mandatory, see §4 —
**seven** of eleven v102 cells have any comparison arm at all, and **every one of them has k₁ = 1 or 2
matches**. The best cell on the board (Powerpuff Girls / v49, k₁=2 vs k₂=4) has an *exact
cluster-permutation floor of p = 0.067* — meaning it **cannot** produce a significant result at
α=0.05 one-sided no matter what the games say, until it gains a third match.

The pooled number looks great (**53.3% core-kill share vs 31.7%, +21.6pp**) and it is **not a
verdict**. It is printed in §8 for context only, under its own subject line.

---

## 1. Provenance, and the exact snapshot these numbers cover

`corpus/meta_join.tsv` is **being appended to live** by the running monitors — it grew from 7,794 to
7,835 rows during this analysis, and a 12th rated v102 match landed mid-run. Every number below is
computed against a **frozen copy**:

| | |
| --- | --- |
| snapshot | `meta_join.snap.tsv`, **md5 `91e2ba8baffbfeea7cb5e7c1e7238d75`**, **7,834 data rows** |
| max `completedAt` in snapshot | **2026-08-09T20:44:31.840Z** |
| taken at | 2026-08-09 22:45 CEST |
| replay events | `events.snap.tsv` (copy of `corpus/events.tsv`), 1,328,907 rows |
| repo HEAD | `292b1b9` |

**Which arm the numbers cover, stated plainly (rule 4):**

| source | v102 matches | note |
| --- | --- | --- |
| `corpus/ladder_games.tsv` | **10** | synced 20:12Z; **stale, do not use for this question** |
| `elo_history.tsv` | **11** rated, through match 581 @ 22:28 CEST | the rating tape |
| **`meta_join.tsv` snapshot (used here)** | **12 rated + 1 unrated** | 12 rated matches / **60 games, all decoded** |

The 12th rated match (**Team 48 / v16**, 20:35:52Z) and the 11th (**diverge / v8**, 20:26:59Z) are
**absent from `ladder_games.tsv` entirely**. The unrated match (**Askar City / v83**, 19:29:45Z) is
excluded from every rated figure and reported separately in §8. Filter is `triggeredBy == 'ladder'`.

The tape is still moving: at the time of writing the live ladder has almost certainly produced a
13th match. **This document covers the arm through 20:44:31Z and nothing after it.**

---

## 2. How the core-kill attribution was established — and it was NOT taken on trust

`cond` records *how* a game ended, not *who* won. The claim under test was
`cond == core_destroyed AND won == 1` ⟺ **we destroyed their core**.

**Established against an independent in-replay source, not assumed.** `corpus/events.tsv` carries a
`DEATH` event with `kind == 'core'` and the **team index of the core that died** — decoded from the
replay binary, entirely independent of the platform's `cond`/`won` metadata.

```
core_destroyed & we-killed(replay) & won=1 : 543
core_destroyed & they-killed(replay) & won=0 : 606
DISAGREEMENTS                                :   0        (1,149 / 1,149 = 100.0000%)
titanium_collected games with 0 core deaths  : 481 / 481
```

**Teeth proven per branch, not per tool (rule 2).** Restricted to each arm separately:
v102 arm **46/46 agree**, v94/v101 era arm **98/98 agree**. Neither branch was inferred from the other.

**The side index was then validated behaviourally, which is the check that actually matters.**
Attribution depends on knowing which replay team index is us. LOKI-8's documented signature is that
**all builder melee is silenced (LOKI-5 removal)**. Counting `batk` from `build_agg.tsv`:

| arm | builder-attack events, US | builder-attack events, THEM |
| --- | --- | --- |
| **v102 (60 rated games)** | **0** | 3,517 |
| v94/v101 era (145 games) | 36,040 | 34,836 |

A flat zero on our side of every v102 game, against a live opponent count, is the bot's own
fingerprint confirming the seat assignment from inside the replay. The era arm (Eir, which *does*
melee) shows the expected non-zero. **Both branches identified independently.**

**Time-to-core-kill was verified as the quantity the question needs (rule 6).** `turns` is game
length; it is only time-to-core-kill if the game ended when the core died. Checked directly:
`turns − core_death_round == 1` in **1,149 of 1,149** games (v102 branch 46/46, era 98/98). TTK below
is reported as `core_death_round + 1`, i.e. identical to `turns` on core-decided games.

**Self-tests: every guard was required to fire on corrupted input (rule 1).**
`scratchpad/final.py --selftest` — flipping the side index turns our-kills into their-kills exactly
(v102 32→24 = their 24; era 46→52 = their 52); collapsing `oppv` to a constant drops the count of
unmatched v102 games from 20 to 10; flipping `won`, forcing `cond`, and forcing `turns` each fire.
All alarms **FIRED**; no guard passed silently.

---

## 3. A CORPUS BUG FOUND WHILE DOING THIS — `ladder_games.tsv`'s `seat` column is not our seat

**`ladder_games.tsv` (and `sync.py`) declare a column `seat`, documented at
`tools/corpus/ladder_meta.py:5` as "our seat". It is populated with `winnerSide`:**

```python
tools/corpus/ladder_meta.py:60    map=g["mapName"], seat=(g.get("winnerSide") or ""),
tools/corpus/sync.py:159          row2 = dict(row, map=g.get("mapName",""), seat=g.get("winnerSide",""), ...
```

Verified against the replay binary's own winner index: `seat == 'a'` ⟺ winner team index 0 in
**880/880** rows, `seat == 'b'` ⟺ index 1 in **750/750**. It is `winnerSide`, deterministically.

**I nearly shipped a false finding on it.** Using `seat` as our seat produced
*"v102 seat B 87.5% core-kill vs seat A 26.9%, Fisher p = 1.7e-05"* — an enormous, clean, entirely
spurious result, because on losses the column names the opponent's side. The correct variable is
`join.our_team` / `meta_join.us_side` (which *is* validated, §2). Recomputed on the true side, the
effect **vanishes**: v102 side A 70.0% (n=10) vs side B 52.5% (n=40), Fisher **p = 0.48**; era arm
side A 36.0% vs side B 27.1%, **p = 0.29**. **There is no seat effect in either arm.**

Two facts make this the dangerous class: the column has a plausible name, and *nothing about the
value looks wrong* — it is always 'a' or 'b'. **Anyone who has used `ladder_games.seat` as our seat
has an inverted result on every loss.** Recommend renaming the column to `winner_side` in
`ladder_meta.py` / `sync.py` and adding a `corpus_sanity.py` check that `seat` never disagrees with
`winnerSide`. Filed here rather than fixed — I am read-only.

---

## 4. Cells MUST be keyed on (opponent, opponent version), and that halves the surface

`ladder_games.tsv`/`join.tsv` carry `oppver = None` universally. **`meta_join.tsv` does not** — its
`teamAVersion`/`teamBVersion` are 100% populated, and `league_matches.tsv` independently corroborates
them. Opponents ship constantly, so "the same opponent" is not a stable unit:

| opponent | version in the **era** arm | version in the **v102** arm | cell survives keying? |
| --- | --- | --- | --- |
| Askar City | v79 ×3 matches | **v82** | **NO — different bot** |
| CtrlAltDefeat | v124 ×3 | **v127** | **NO — different bot** |
| Banminary | v41 ×1, **v44 ×1** | v44 | yes, but era arm shrinks 2 → **1** |
| diverge | v7 ×1, **v8 ×1** | v8 | yes, era arm 2 → **1** |
| Kings College Munich | v8 ×2 | v8 | yes |
| OopsGotYourElo | v21 ×3 | v21 | yes |
| Powerpuff Girls | v49 ×4 | v49 ×2 | yes |
| farming_200s | v9 ×2 | v9 | yes |
| gsxWins | v22 ×3 | v22 | yes |
| Leviathan | — | v35 | no era arm at all |
| Team 48 | — | v16 | no era arm at all |

**Version-keying costs two whole cells (Askar City, CtrlAltDefeat) and halves two more.** It makes
the n problem strictly worse, not better. Ignoring it would silently pool Askar v79 with v82 and CAD
v124 with v127 — two different programs each — under one opponent name.

**Askar City shipped mid-arm**: v81 @ 18:35:01Z → v82 @ 18:46:13Z → **v83 @ 19:29:45Z**. Our rated
Askar match (19:25:36Z) caught v82; the unrated one four minutes later caught v83. Even *within one
arm* the name is not a unit.

---

## 5. THE PER-OPPONENT TABLE

Population, inline on every figure (rule 4): **our rated ladder games**; v102 arm = `ourver 102`,
`triggeredBy=ladder`, 12 matches / 60 games, all decoded; era arm = `ourver 94 or 101`
(`_v115dodge`, **byte-identical main.py**, md5 `77ae5c09`, per HANDOVER — so pooling v94 and v101 is
pooling one bot with itself, not two bots), 29 matches / 145 games. **Core-kill share = OUR kills as
a share of that cell's games.** TTK = median round the enemy core died, our kills only. `≤250` counts
kills inside `KILL_WINDOW_RND`. **Empty cells are empty; nothing is imputed.**

| opponent / version | opp rating | **v102** M | G | our kills | **share** | med TTK | ≤250 | **era** M | G | our kills | **share** | med TTK | ≤250 | **Δ share** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
| **Powerpuff Girls / v49** | 1599 | **2** | 10 | 5 | **50.0%** | 236 | 3/5 | **4** | 20 | 0 | **0.0%** | — | 0/0 | **+50.0pp** |
| **OopsGotYourElo / v21** | 1551 | **1** | 5 | 4 | **80.0%** | 138.5 | 4/4 | **3** | 15 | 3 | **20.0%** | 183 | 2/3 | **+60.0pp** |
| **gsxWins / v22** | 1611 | **1** | 5 | 2 | **40.0%** | 238.0 | 1/2 | **3** | 15 | 9 | **60.0%** | 124 | 7/9 | **−20.0pp** |
| **Kings College Munich / v8** | 1559 | **1** | 5 | 3 | **60.0%** | 306 | 1/3 | **2** | 10 | 0 | **0.0%** | — | 0/0 | **+60.0pp** |
| **farming_200s / v9** | 1654 | **1** | 5 | 2 | **40.0%** | 166.0 | 2/2 | **2** | 10 | 4 | **40.0%** | 251.5 | 2/4 | **0.0pp** |
| Banminary / v44 | 1560 | **1** | 5 | 3 | 60.0% | 164 | 3/3 | **1** | 5 | 4 | 80.0% | 214.5 | 3/4 | −20.0pp |
| diverge / v8 | 1652 | **1** | 5 | 1 | 20.0% | 118 | 1/1 | **1** | 5 | 2 | 40.0% | 106.5 | 2/2 | −20.0pp |
| Askar City / v82 | 1608 | **1** | 5 | 3 | 60.0% | 176 | 2/3 | — | — | — | — | — | — | **no arm** |
| CtrlAltDefeat / v127 | 1590 | **1** | 5 | 2 | 40.0% | 182.0 | 2/2 | — | — | — | — | — | — | **no arm** |
| Leviathan / v35 | 1518 | **1** | 5 | 4 | 80.0% | 175.0 | 3/4 | — | — | — | — | — | — | **no arm** |
| Team 48 / v16 | 1557 | **1** | 5 | 3 | 60.0% | 205 | 2/3 | — | — | — | — | — | — | **no arm** |
| *Askar City / v79* | 1604 | — | — | — | — | — | — | **3** | 15 | 4 | 26.7% | 187.0 | 3/4 | *era only* |
| *CtrlAltDefeat / v124* | 1606 | — | — | — | — | — | — | **3** | 15 | 3 | 20.0% | 271 | 1/3 | *era only* |
| *I Stone / v22* | 1630 | — | — | — | — | — | — | **3** | 15 | 6 | 40.0% | 309.0 | 2/6 | *era only* |
| *Lunds Stallions / v57* | 1591 | — | — | — | — | — | — | **2** | 10 | 4 | 40.0% | 145.0 | 4/4 | *era only* |
| *Banminary / v41* | 1536 | — | — | — | — | — | — | **1** | 5 | 5 | 100.0% | 196 | 3/5 | *era only* |
| *diverge / v7* | 1585 | — | — | — | — | — | — | **1** | 5 | 2 | 40.0% | 126.0 | 2/2 | *era only* |

---

## 6. GATEABILITY VERDICT — per opponent

### The unit of analysis is the MATCH, not the game

Games inside a 5-game match are **not independent**. Measured on the era arm's 29 matches, the
intra-match correlation of our core-kill outcome is **ICC = 0.278**, giving a design effect
**DEFF = 1 + 4×0.278 = 2.11**. **A 5-game match is worth ≈ 2.37 independent games.** (The v102 arm's
own ICC is ≈ 0 — but on 12 matches that estimate is worthless, so the era arm's 29-match estimate is
used throughout. Using the v102 estimate would *manufacture* power, which is exactly the failure this
document exists to avoid.)

Consequently the honest test is a **cluster-level exact permutation test** on match-level kill
counts. Its **minimum achievable p is 1/C(k₁+k₂, k₁)** — a hard bound that depends only on how many
matches each arm has, *not on how large the effect is*. Below that floor a cell **cannot** return
p ≤ 0.05 even on perfect separation.

### The measurement that makes this concrete — and it is an observation, not an argument

**We played Powerpuff Girls twice in the v102 arm and neither side shipped between the two matches:**
`OpenSverige/v102` vs `Powerpuff Girls/v49`, both times, **83 minutes apart.**

```
18:55:19Z   v102 vs Powerpuff Girls/v49   4-1 WIN    our core kills 4/5,  their kills 1
20:18:10Z   v102 vs Powerpuff Girls/v49   1-4 LOSS   our core kills 1/5,  their kills 0
```

**Identical bots on both sides. Opposite results.** Under p=0.5/game, P(4-1 or better) = 6/32 =
0.1875 and P(1-4 or worse) = 0.1875 — one of each in two matches is entirely unremarkable, **which is
the point**. This is a direct empirical measurement of how far a single 5-game cell swings with
*nothing changed*. It is the citation for the verdicts below: **a per-opponent cell of one match is a
coin flip with a name.**

### Verdicts

| opponent / version | verdict | k₁ | k₂ | perm. floor | needs k₁ ≥ | binomial+DEFF check |
| --- | --- | ---: | ---: | ---: | --- | --- |
| **Powerpuff Girls / v49** | **UNDERPOWERED (k₁=2, need 3)** | 2 | 4 | **0.067** | **3** (1-sided) / 4 (2-sided) | 17 games/arm ≈ 4 matches |
| **OopsGotYourElo / v21** | **UNDERPOWERED (k₁=1, need 3)** | 1 | 3 | 0.250 | **3** / 5 | 15 games/arm ≈ 3 matches |
| **gsxWins / v22** | **UNDERPOWERED (k₁=1, need 3)** | 1 | 3 | 0.250 | **3** / 5 | 200 games/arm ≈ 40 matches |
| **Kings College Munich / v8** | **UNDERPOWERED (k₁=1, need 5)** | 1 | 2 | 0.333 | **5** / 8 | 12 games/arm ≈ 3 matches |
| **farming_200s / v9** | **UNDERPOWERED (k₁=1, need 5)** — and Δ = 0.0pp, no effect to detect | 1 | 2 | 0.333 | **5** / 8 | undefined (Δ=0) |
| Banminary / v44 | **SATURATED** *and* **UNDERPOWERED (k₁=1, need 19)** | 1 | 1 | 0.500 | 19 / 39 | 166 games/arm ≈ 34 matches |
| diverge / v8 | **UNDERPOWERED (k₁=1, k₂=1, need 19)** | 1 | 1 | 0.500 | 19 / 39 | 166 games/arm ≈ 34 matches |
| Askar City / v82 | **NO COMPARISON ARM** (era faced v79) | 1 | 0 | — | — | — |
| CtrlAltDefeat / v127 | **NO COMPARISON ARM** (era faced v124) | 1 | 0 | — | — | — |
| Leviathan / v35 | **NO COMPARISON ARM** (never met in the era) | 1 | 0 | — | — | — |
| Team 48 / v16 | **NO COMPARISON ARM** (never met in the era) | 1 | 0 | — | — | — |

**`SATURATED` — Banminary.** Against Banminary the era arm went **10 games, 10 wins, 9 core kills**
(v41 5/5 kills, v44 4/5). Core-kill share has ≤1 game of headroom; an instrument reading 90-100% in
the baseline arm cannot show an improvement. Excluded from any gate.

**Two figures the raw numbers will tempt you with, and why they are not evidence.** Unclustered
Fisher exact on the *games* gives Powerpuff p=0.0018, OopsGotYourElo p=0.031, KCM p=0.022 — three
apparently significant cells. Deflating the counts by the measured DEFF=2.11 sends all three to
p ≥ 0.077. And for every cell with **k₁=1 the between-cluster variance is unestimable from one
cluster**, so no valid clustered test exists there at any p. **The three "significant" cells are the
artefact this whole exercise was set up to prevent.**

**On the "binomial+DEFF" column.** It answers the brief's question — *what n would the observed delta
need* — using the observed per-game variance inflated by DEFF. It is reported for completeness and
should be read with suspicion: it takes the observed delta as the true one, which at n=5 is
post-hoc-power reasoning. Note how it disagrees violently with itself between cells: KCM says 3
matches, gsxWins says 40, on data of the same size. **The permutation floor is the number to use** —
it is a hard bound independent of the effect estimate.

---

## 7. THE ACCRUAL ANSWER — how long until the first cell is gateable

**Cadence, derived not assumed.** Our rated ladder matches arrive on a **fixed 10-minute slot**:
across 121 consecutive inter-arrival intervals on 2026-08-09, every gap was 9 or 10 minutes (sub-minute
jitter crossing a minute boundary), zero gaps. **6 rated matches/hour, 144/day.**

**Per-opponent appearance rate** over the recent regime (the 41 rated matches under v94/v101/v102,
13:52Z–20:44Z, our rating 1565-1613): Powerpuff Girls **14.6%** of matches (1 per 68 min);
OopsGotYourElo / Askar City / gsxWins / CtrlAltDefeat **9.8%** each (1 per 102 min); KCM / farming_200s
/ diverge / Banminary / I Stone **7.3%** (1 per 137 min); Lunds Stallions 4.9%; Leviathan, Team 48 2.4%.

**But a version-keyed cell only accrues when the opponent is on the matched version.** Effective rate
= appearance rate × P(opponent on that version). Powerpuff oscillates (v49→51→52→49→54→49) and was on
v49 in 25 of 50 observations during the v102 window, so it accrues at **half** its appearance rate.

| opponent / version | ships/h today | P(matched ver) | eff. rate/match | **to reach k₁ (1-sided)** | to reach k₁ (2-sided) |
| --- | ---: | ---: | ---: | --- | --- |
| **Powerpuff Girls / v49** | 0.40 | 0.50 | 0.073 | **+1 match ⇒ ~14 matches ⇒ 2.3 h** | +2 ⇒ 27 matches ⇒ 4.6 h |
| OopsGotYourElo / v21 | 0.50 | 1.00 | 0.098 | +2 ⇒ ~21 matches ⇒ **3.4 h** | +4 ⇒ 41 matches ⇒ 6.8 h |
| gsxWins / v22 | **0.00** | 1.00 | 0.098 | +2 ⇒ ~21 matches ⇒ **3.4 h** | +4 ⇒ 41 matches ⇒ 6.8 h |
| Kings College Munich / v8 | **0.00** | 1.00 | 0.073 | +4 ⇒ ~55 matches ⇒ **9.1 h** | +7 ⇒ 96 matches ⇒ 15.9 h |
| farming_200s / v9 | **0.00** | 1.00 | 0.073 | +4 ⇒ ~55 matches ⇒ **9.1 h** | +7 ⇒ 96 matches ⇒ 15.9 h |

### The answer

**The first cell becomes gateable after ONE more Powerpuff Girls / v49 match — expected in ~14 rated
matches ≈ 2.3 hours of ladder play.**

Three qualifications the builder must carry with that number:

1. **It is a floor-touching gate, not a comfortable one.** At k₁=3 vs k₂=4 the minimum achievable p is
   1/C(7,3) = **0.029**. The cell reaches significance *only on perfect cluster separation* — all
   three v102 matches strictly above all four era matches. The era arm is 0,0,0,0 kills, so any third
   v102 match with ≥1 core kill achieves it. That is likely (v102 has killed a Powerpuff core in 5 of
   10 games) but it is one draw, and the 18:55 vs 20:18 pair above is the reminder of what one draw is
   worth.
2. **For a two-sided gate at 0.05, Powerpuff needs +2 matches ≈ 4.6 h.**
3. **For a five-name gate where all five are simultaneously capable, the binding constraints are KCM
   and farming_200s at +4 matches each: ~55 rated matches ≈ 9.1 hours** (they accrue in parallel, so
   this is elapsed time, not a sum). **This is at the edge of reachable.** gsxWins, KCM, farming_200s
   and I Stone have shipped **zero** times today, but zero over ~13-20 h of observation only bounds
   their rate at ≈0.15-0.25/h (rule of three), so P(KCM still on v8 after 9.1 h) ≥ ~0.24. **A
   version-keyed cell has a half-life, and for half the field it is shorter than the accrual time.**
   Priced honestly: the five-name gate at 2-sided significance is **not** reachable against a churning
   field, and should not be promised.

---

## 8. THE FIVE-NAME SHORTLIST

**Criterion (revised after §4 — version churn changed it).** A standing gate name must:

1. **have a version-matched era arm with k₂ ≥ 2** — without it there is nothing to compare against,
   and this test alone eliminates Askar City, CtrlAltDefeat, Leviathan and Team 48;
2. **be version-stable, or version-recurrent** — a cell whose key dissolves faster than it accrues is
   not a gate;
3. **appear often enough** — ≥1 per ~14 rated matches (~140 min);
4. **be resolving, not saturated** — baseline core-kill share not pinned at the ceiling;
5. **span the rating range.**

**The five names are not chosen — they are exactly what survives the criterion.** Every opponent with
a version-matched era arm of k₂ ≥ 2 is on this list, and there are precisely five:

| # | name | rating | era baseline (core-kill share) | why |
| --- | --- | ---: | --- | --- |
| 1 | **Powerpuff Girls / v49** | 1599 | **0/20 = 0%** (k₂=4) | Fastest accrual on the board (14.6% of matches) and the largest era arm. Baseline pinned at the **floor**, so it resolves *upward* with maximal sensitivity — but it can only measure improvement, not regression. Version oscillates; halve its accrual rate. |
| 2 | **gsxWins / v22** | 1611 | **9/15 = 60%** (k₂=3) | **Zero ships all day** — the most stable instrument in the field. Baseline mid-range, so it resolves in *both* directions. It is also the one cell where v102 currently reads **worse** (40% vs 60%), which makes it a genuine two-sided instrument rather than a cheerleader. |
| 3 | **OopsGotYourElo / v21** | **1551** | **3/15 = 20%** (k₂=3) | Anchors the **low** end of the range. k₂=3 and 9.8% appearance. Caveat: ships often (0.50/h, 10 changes today) but repeatedly **returns to v21** as its home version — it was v21 for 25/25 observations across the whole v102 window. Monitor the key. |
| 4 | **Kings College Munich / v8** | 1559 | **0/10 = 0%** (k₂=2) | **Zero ships all day**, on v8 since 00:56Z. Baseline floor-pinned. Slow accrual (7.3%). The KCM classification doc makes it a mechanism-relevant name (CAD-family launcher-ferry). |
| 5 | **farming_200s / v9** | **1654** | **4/10 = 40%** (k₂=2) | Anchors the **top** of the range — the only >1650 opponent with any comparison arm — and **zero ships all day** on v9. Mid-range baseline, resolves both ways. Slow accrual (7.3%). Currently Δ = 0.0pp, i.e. the honest read is "no measured change against the strongest opponent we have an arm for". |

**Rating span: 1551 → 1654, 103 Elo.** Our rating over the arm was 1565-1613, so the set brackets us.

**Named exclusions and why** (so the next session does not re-propose them):
**Askar City** — no version-matched arm; ships 0.31/h and shipped twice mid-arm, the worst churner
among our regulars. **CtrlAltDefeat** — no version-matched arm (v124 → v127); documented serial
churner. **Leviathan / Team 48** — never played in the era arm; no baseline exists.
**Banminary** — **SATURATED** (era 10/10 wins, 9/10 core kills) and k₂=1 after version-keying.
**diverge** — k₂=1 after version-keying; also ships 0.26/h.
**I Stone / v22** — **the strongest reserve**: zero ships all day, era baseline a well-centred
6/15 = 40%, rating 1630 (fills the 1611-1654 gap), 7.3% appearance — it is excluded *only* because
v102 has not yet drawn it. **Promote I Stone into the five the moment it has one v102 match**, most
likely in place of Kings College Munich (same accrual rate, better rating placement, non-degenerate
baseline).

**A drift covariate the gate must carry.** Across the arm chronologically, opponent strength **rose
by +37.8 Elo** (first five matches mean 1570.0, last five 1607.8; derived from `meta_join` sorted on
`completedAt`, 11 rated matches at the time the coordinator's figure was set, +37.8 reconfirmed on
this snapshot). Any pooled read across the arm is fighting a strengthening field; the per-opponent
surface is immune to it, which is one more reason to prefer it.

### Pooled figures — CONTEXT ONLY, explicitly not a verdict (`WIN_RATE_IS_VERDICT: no`)

| population | G | win rate | **our core-kill share** | their core-kill share | core-decided | median TTK | ≤250 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **v102 rated arm** (12 matches) | 60 | 53.3% | **53.3%** | 40.0% | **93.3%** | **177.0** | 24/32 |
| **v94/v101 era rated** (29 matches) | 145 | 49.7% | **31.7%** | 35.9% | 67.6% | 184.0 | 31/46 |
| *v102 unrated, Askar City/v83* | 5 | 80.0% | 80.0% | 20.0% | 100.0% | 237.5 | 2/4 |

Two mechanism observations worth the builder's attention, both **game-level and therefore
underpowered by the same ICC argument** — flagged as leads, not findings:

- **Every single v102 win is a core kill: 32 wins, 32 core kills, 0 economic wins.** The era arm won 72
  games of which **26 were titanium wins**. LOKI-8 does not win by economy at all. 93.3% of its games
  are core-decided against the era's 67.6%.
- **Their core-kill share against us is flat**: 40.0% (v102) vs 35.9% (era). The line is not trading
  defence for offence in any measurable way; it is converting *its own* economic wins into core kills.

---

## 9. WHAT I COULD NOT COMPUTE, AND WHY

1. **Any per-opponent significance test.** Seven of eleven v102 cells have k₁=1 — **one cluster**,
   from which the between-cluster variance is not estimable. This is not "a weak test"; it is **no
   valid test**. Reported as `UNDERPOWERED (k₁=X, need Y)` rather than as a p-value.
2. **The opponent's version during the era arm's *later* matches, from a second source.**
   `league_matches.tsv` (which independently carries opponent versions) ends at 17:32:43Z. The Askar
   City 18:12Z and Banminary 18:02Z era matches sit past it, so their versions rest on `meta_join`
   alone rather than on two agreeing sources. `meta_join` and `league_matches` agree on every match
   where both cover it, which is why I trust them — but that check does not reach the last hour of the
   era arm.
3. **A map-matched comparison, which is the analysis this question actually wants.** Maps are **not**
   controlled between arms: every opponent's era arm contains maps its v102 arm does not and vice
   versa (Powerpuff overlaps on 8 of 10+ maps, gsxWins on only 4). Restricting to shared maps leaves
   3-8 games per cell — a smaller n on an already-untestable cell, so I did **not** run it as a
   headline. For the record the direction is unchanged where it can be computed at all (Powerpuff
   map-matched: v102 4/8 vs era 0/13). **Once cells reach k₁≥3, map-matching is the right refinement
   and should be built in, not bolted on.**
4. **Seat balance as a covariate.** Discarded, because the column I would have used is not what it
   claims (§3). On the corrected variable there is no seat effect in either arm (p=0.48 / p=0.29), so
   nothing is lost — but I cannot state a *seat-adjusted* per-opponent share, because at n=5/cell the
   seat split within a cell is 0-5 or 5-0 in several cells.
5. **Anything after 2026-08-09T20:44:31.840Z.** The ladder is live and running at 6 matches/hour; by
   the time this is read the arm is larger than 12. Re-run `scratchpad/final.py` against a fresh
   snapshot — but **re-pin the snapshot**, because `meta_join.tsv` grew twice during this analysis.
6. **Whether the opponent's *behaviour* changed even at a constant version string.** A version number
   is a claim about identity, not a measurement of it. I did not verify from the replays that
   e.g. Powerpuff/v49 in the era arm plays like Powerpuff/v49 in the v102 arm. That check is
   available (`build_agg.tsv` opening rows) and is the natural next hardening of the version key.

---

## 10. THINGS IN THE BRIEF THAT ARE WRONG — corrections, offered as claims to check

1. **"`oppver` is universally `None` — dead by platform design, do not try to use it."** True of
   `ladder_games.tsv` and `join.tsv`. **False of the platform.** `meta_join.tsv`'s
   `teamAVersion`/`teamBVersion` are **100% populated**, and `league_matches.tsv` carries them
   independently for 29,680 league-wide matches. Opponent version is available and **it is
   load-bearing** — §4 shows it deletes two cells outright. "Dead by platform design" would have cost
   this deliverable its most important guard.
2. **"The v102 arm is 11 matches against 9 distinct opponents."** At the snapshot it is **12 rated
   matches against 11 distinct opponents** (+1 unrated). Keyed on `(opponent, version)` there are
   **11 cells in the v102 arm and 17 distinct keys** across both arms (6 era-only). The count was
   correct when written; the point is that **the arm
   size is a moving quantity and any figure quoting it must carry a snapshot pin.**
3. **"Combine `cond` with `won`… `core_destroyed` + `won=1` should mean our kill."** Correct, and
   verified 1,149/1,149. But the brief's suggested cross-check — "cross-check against `meta_join`'s
   winner fields" — would have been **circular**: `meta_join`'s `us_side`, `join`'s `our_team` and
   `ladder_games`'s `won` all derive from the same free-metadata `winnerSide`. The check that actually
   discriminates is the **in-replay `DEATH`/`core` event team index**, plus the **behavioural**
   identification of our side (§2). Recommend that as the standing recipe.
4. **A trap the brief did not warn about, and should have**: `ladder_games.seat` is `winnerSide`, not
   our seat (§3). It produced a p=1.7e-05 finding that is pure artefact. This is the same failure class
   as the `econ.tsv` dead columns already documented in `corpus-howto.md` — a plausibly-named column
   that never looks wrong. **Add it to THE FOUR TRAPS as #7.**
5. **Not wrong but worth naming: the "era arm" is a cross-line comparison.** v94 ≡ v101 ≡
   `_v115dodge` = **Eir**. So this document measures **Eir → LOKI-8 on the ladder**, which is a
   legitimate field read, but it is **not** the programme's `COMPARE_AGAINST: previous_line_iteration`.
   The programme's comparison — LOKI-7 vs LOKI-8 — **has never been run** (HANDOVER queue item 3), and
   nothing here substitutes for it.
6. **Confirmed, not corrected**: the coordinator's three updates all check out against the snapshot —
   `meta_join` rebuilt with 100% version population; the rated/unrated split (`triggeredBy=='ladder'`)
   with diverge/v8 as the extra rated match and Askar City/v83 as the unrated one; and the
   Powerpuff/v49 4-1 / 1-4 pair with both sides unchanged. The opponent-strength drift is **+37.8**,
   reconfirmed independently on this snapshot.

---

## Reproducing this

Analysis script and its self-tests: `scratchpad/final.py` (session-scoped; regenerate against a fresh
snapshot). The self-test corrupts each input a guard consumes and requires the alarm to fire —
`--selftest` must print `PASS` with every listed alarm `FIRED` before any number here is trusted.
Nothing in `bots/`, `docs/coordination.md`, `HANDOVER.md`, the arena or the platform CLI was touched;
no network call was made; nothing was committed.
