# How the ladder assigns engine seats across a best-of-five (2026-08-08)

**VERDICT — the engine seat is FIXED FOR THE WHOLE MATCH, and match metadata's
`teamAName` IS engine `TEAM_A`, always.** Not alternating, not re-rolled per game.
Evidence: 158 archived OpenSverige matches / 790 games. Match level, meta-blind: the
count of games won by engine `TEAM_A` equals `scoreA` in **158/158** matches and equals
`scoreB` in 0 (null model for a fair per-game seat coin: p = 1.4e-132). Game level,
meta-blind behavioural stamping: **583/583 confidently stamped games put us on the seat
our own metadata row implies, 0 exceptions, 0 matches with mixed seats across their five
games.** Which of the two teams the metadata calls "A" is itself an unbiased coin flip
per match (we were meta-A in 77 of 158), uncorrelated with rating, name, team id or
`triggeredBy`.

**Consequence in one line:** all five games of a best-of-five are played on one seat, so a
whole match — five different maps — is tilted the same way by the seat-A edge, and per-map
records are seat-confounded at *match* granularity, not game granularity.

---

## 0. Version tags and provenance

| | |
|---|---|
| Archive read | `replay_archive/` as of **2026-08-08 morning**: 418 `*.meta.json`, 2,091 `*.replay26`, 614 MB. Read-only; nothing downloaded, no games run. |
| Our live version at write time | **v75 "Eir 8"** (`bots/_v85hsd`) |
| Corpus version span | our **v64 … v75** (v64:9, v65:11, v66:8, v67:15, v68:26, v69:14, v70:8, v71:5, v72:36, v73:5, v74:14, v75:7 matches) — the brief said v56–v75; the archive's OpenSverige matches only reach back to v64. |
| Date span | 2026-08-07 → 2026-08-08 (the archive itself is that young) |
| Opponents | 30 distinct teams; top: Powered by SmartFridge 16, Team 48 / CtrlAltDefeat / Lunds Stallions 10 each, Powerpuff Girls 9, I Stone 9, Ouroboros 8 |
| Decode | stdlib protobuf reader built on `tools/replay_census.py`'s `fields()` / varint code, per `tools/replay_schema.md`. Scripts in the session scratchpad (`seat_decode/features.py`, `opening.py`, `cluster.py`, `stamp2.py`, `final.py`). |
| Not used | `fcode`, the arena, the platform, `--json` runs. Every number here comes off files already on disk. |

Corpus shape: 158 OpenSverige matches × 5 games = **790 games, all five replays present
for every match**.

---

## 1. Why a classifier is needed at all

`.replay26` carries no team names, and our bot deliberately prints to stderr only — which
the engine does not capture. Confirmed on this corpus: **`botOutput.stdout` is empty on
all 4,172 team-sides in the archive** (no side, ours or anyone's, has a stdout
fingerprint), and `IndicatorLine`/`IndicatorDot` counts are 0 everywhere too. So "which
engine seat were we?" has to be answered behaviourally.

Also established while parsing, and load-bearing for the classifier: **each map assigns
its two core positions to fixed seats.** Across all 2,091 replays, every map layout shows
exactly one `(coreA, coreB)` pair — e.g. archipelago/snowflake 26×26 is always
A@(5,5) / B@(19,19), atoll 18×18 always A@(2,14) / B@(14,2). The cores never swap seats.
So "our seat" and "which core position we started on" are the same question, and a
map-plus-core-position bucket cleanly separates the two seats.

---

## 2. Test 1 — match-level, no classifier needed (meta-blind)

`scoreA`/`scoreB` in the meta JSON are game counts for metadata teams A and B. Each replay
carries `Replay.winner` as an engine `Team`. Tally engine winners over a match's five games
and compare:

| result | matches |
|---|---|
| engine-`TEAM_A` win count == `scoreA` (meta A = engine A) | **158** |
| engine-`TEAM_A` win count == `scoreB` (meta A = engine B) | 0 |
| neither (would imply seats moved inside the match) | 0 |

Because `scoreA + scoreB = 5`, the two scores are never equal, so this test is decisive
per match — it cannot be satisfied by both hypotheses at once. Under the null "each game's
seat is an independent fair coin", the per-match pass probability averages **0.197**, so
all-158-pass has probability **1.36e-132**.

This alone kills "seats alternate per game" and "seats are re-rolled per game" and pins
meta-A = engine-A at match granularity for every match in the archive. What it cannot do
is prove seats are constant *within* a match in the cases where an alternation happens to
preserve the tally — hence Test 2.

---

## 3. The our-side classifier

### 3.1 Signal

Per team, per game, an **opening trace**: every `placeEntity` / `moveBuilderBot` /
`builderBuild` / `builderAttack` / `builderHeal` / `coreConvertAmmo` event of the first 12
rounds, expressed as offsets from that team's own Core NW corner and canonicalised into a
per-round string. Deterministic bots reproduce this byte-for-byte on the same map and seat
until the two sides make contact.

### 3.2 Classifier B (primary) — prefix margin, meta-blind

For each side of each OpenSverige game, within its map+core bucket, measure how many
leading rounds of its trace agree with the best match from:

* **POS** — a side in a *different* OpenSverige match against a *different* opponent team.
  Only our own bot can score deep here: an opponent's opening only recurs in matches
  against that same opponent, and those are excluded by construction.
* **NEG** — a side in a match **OpenSverige never played in at all** (260 such matches,
  2,592 sides). Only a non-OpenSverige bot can score deep here.

Stamp the side with the larger `POS − NEG` margin as ours, requiring `max(POS) ≥ 2` and a
margin gap ≥ 2. Nothing in this procedure reads `teamAName`, `scoreA` or the winner —
the labels it consumes are only "was OpenSverige in this match at all" and "which opponent
team", both of which are seat-free.

### 3.3 Classifier A (independent corroboration) — trace-class recurrence

Coarser and completely different in construction: bucket the first-2-round trace
(builds/converts/attacks/heals, no moves) by map+core position, and call a trace class
*ours* if it recurs across ≥ 2 **distinct opponent teams**. Stamp a game if exactly one of
its two sides falls in an ours-class.

### 3.4 Validation

| check | result |
|---|---|
| **Specificity (hard negative control).** Take the recurrence library *without* the "never seen in a non-OpenSverige match" filter and run it over the 2,592 sides from the 260 matches OpenSverige never played. Ground truth: none of them is us. | **106/2,592 = 4.09% false-positive rate** for classifier A's coarse 2-round trace. Classifier B's NEG term is exactly the mechanism that suppresses these. |
| **Sensitivity.** Classifier A resolves exactly one side per game in **565/790 (71.5%)**; classifier B in **583/790 (73.8%)**. Neither ever nominates both sides at the confidence thresholds used (A: 6 double-hits and 219 no-hits are *excluded*, not guessed; B: 166 below-floor and 41 margin-ties excluded). |
| **Two independent classifiers against each other.** Where both fire (511 games): **510 agree, 1 disagrees.** |
| **Known-side local replay** (`archb_decode/archipelago_b_hsd_off.replay26`, 26×26 archipelago, v84g=v73 lineage seat A vs `_v85hsd`-off seat B — sides pinned by the matching `.out`, "Winner: v84g_off, core destroyed turn 732"). Score both sides against the archive. | Both sides: best prefix vs the archive's ours-cluster = 1, vs archive opponent-sides = 0, vs non-OpenSverige sides = 0. Directionally correct on **4/4 sides** (round-0 first-builder offset `(0,2)` is already ours-only on that bucket), though shallow — the local runs are ablated variants at a different version, so this is a weak positive control, and the corpus-internal checks above carry the weight. |
| **Coverage bias.** Stampability is flat across the five game slots (game 1: 113 stamped / 45 not; g2 115/43; g3 112/46; g4 123/35; g5 120/38), so the unclassified games are not concentrated in any position where a swap could hide. |

The 4 games where classifier B's *unthresholded* form disagreed with metadata all had
margins of 0 or 1 (e.g. `POS=1,NEG=1` on both sides — round-0 spawn offset only), and all
4 fall below the gap-≥2 threshold. Three of the four are CtrlAltDefeat games, a bot whose
opening collides with ours in round 0. Sweeping the thresholds:

| floor | gap | stamped | agree with meta | disagree |
|---|---|---|---|---|
| 2 | 1 | 616 | 612 | 4 |
| **2** | **2** | **583** | **583** | **0** |
| 3 | 2 | 501 | 501 | 0 |
| 4 | 2 | 374 | 374 | 0 |
| 6 | 2 | 195 | 195 | 0 |

There is no threshold at which a *confident* stamp contradicts the metadata mapping.

---

## 4. Pattern table

Primary stamp set = classifier B at floor 2 / gap 2: **583 of 790 games (73.8%), covering
157 of 158 matches**, 1–5 games stamped per match (median 4).

| our metadata position | distinct engine seats stamped across the match's 5 games | matches |
|---|---|---|
| A | **{A} only** | **77** |
| B | **{B} only** | **80** |
| B | (no game reached the confidence threshold) | 1 |
| either | mixed {A,B} inside one match | **0** |

Stamped games per match: 5 games in 31 matches, 4 in 68, 3 in 42, 2 in 14, 1 in 2, 0 in 1
(`fe045ae6…`, I Stone vs OpenSverige 2–3 — still covered by Test 1, which passes for it).

Seat by game slot among stamped games — flat, as required by a per-match assignment:
g1 55A/58B, g2 57A/58B, g3 57A/55B, g4 59A/64B, g5 64A/56B.

A **bootstrap pass** (build a reference library from the 583 confident our-sides, then
re-score the abstentions against it — still meta-blind) lifts coverage to **602 games,
still 0 disagreements and 0 mixed matches**. The union with classifier A reaches 637 games
with 2 disagreements, both of them games where classifier B abstained and classifier A
fired on a round-0-only collision — i.e. inside its measured 4.09% false-positive rate.
They are reported here rather than dropped silently; neither survives any confidence
threshold.

**Pattern verdict: AAAAA / BBBBB. Never ABABA, never random.**

---

## 5. Metadata team A vs engine `TEAM_A`

**Always.** 158/158 by the winner tally, 583/583 by per-game behavioural stamp, and the
whole-match consistency means the mapping cannot be drifting inside a series either.

Which team the ladder *calls* A is a coin flip per match and carries no other information:

| candidate rule for "who is metadata team A" | archive (418 matches) |
|---|---|
| higher-rated team | 217 A-higher / 201 B-higher — no |
| alphabetically first name | 210 / 208 — no |
| lexicographically smaller team id | 199 / 219 — no |
| the winner | 226 / 192 — no (this is the seat-A edge, not a rule) |
| our own share | OpenSverige meta-A in 77 of 158, meta-B in 81 — no |

Per opponent it is also unlocked — e.g. Ouroboros 4A/4B, Team 48 5A/5B, CtrlAltDefeat
5A/5B, Lunds Stallions 5A/5B — though small samples skew (Askar City 1A/6B, Powerpuff
Girls 7A/2B), which is exactly the trap §7 warns about.

Maps are drawn per game, not per match: 340 of 418 matches use 5 distinct maps, 74 use 4,
3 use 3, 1 uses a single map five times. So a match = one seat × five map draws.

---

## 6. Ouroboros cross-check

The prior **"Ouroboros seat-lock (their-A/our-B every game)"** claim, already refuted
2026-08-07 by the probe re-freeze work. This decode reproduces the artefact and names its
cause exactly.

All 9 archived Ouroboros matches (8 of them vs us), chronologically:

| completed (UTC) | match | metadata A | metadata B | series | our seat (stamped) |
|---|---|---|---|---|---|
| 08-07 10:29 | 22f55a05 | Ouroboros v8 | Powered by SmartFridge v35 | 2–3 | n/a |
| 08-07 11:31 | bab61537 | Ouroboros v8 | **OpenSverige v64** | 5–0 | `???BB` → **B** |
| 08-07 14:21 | 071cd20c | Ouroboros v8 | **OpenSverige v65** | 5–0 | `BBBB?` → **B** |
| 08-07 **16:47** | fb23a610 | **OpenSverige v67** | Ouroboros v8 | 1–4 | `AAAAA` → **A** |
| 08-07 19:37 | 313d303f | **OpenSverige v68** | Ouroboros v8 | 2–3 | `?A?AA` → **A** |
| 08-07 21:47 | 50f00a69 | Ouroboros v8 | **OpenSverige v69** | 3–2 | `??BBB` → **B** |
| 08-08 01:17 | 067dcff2 | **OpenSverige v72** | Ouroboros v8 | 0–5 | `?AAAA` → **A** |
| 08-08 04:58 | 4e0874d0 | Ouroboros v8 | **OpenSverige v73** | 3–2 | `BB??B` → **B** |
| 08-08 06:16 | 621b841e | **OpenSverige v74** | Ouroboros v8 | 0–5 | `AAAAA` → **A** |

Corrected reading: **4 matches on seat A, 4 on seat B, and the seat is constant inside
every one of them.** The "lock" was the first two OpenSverige-vs-Ouroboros matches — 10
consecutive games — both happening to list Ouroboros as metadata team A. The prior note's
"broke 07T16:47Z" is precisely `fb23a610`, the third match. There was never a seat rule
here; there was a two-match run of the same coin flip, and per-game stamping was never the
missing piece — the metadata row already said it.

---

## 7. What this means for per-map deltas

**Per-map results are seat-confounded at match granularity.** A best-of-five contributes
five different maps all played on a single seat, so map-level records do not average the
seat draw away within a match; they average it only over *matches*, and only if the
matches happen to be seat-balanced.

Our archived corpus, by map (our games, all 790, seat taken from the now-verified
metadata mapping):

| map | seat-A games | our win % | seat-B games | our win % | seat skew (A−B) |
|---|---|---|---|---|---|
| antler | 32 | 46.9 | 25 | 44.0 | +7 |
| archipelago | 24 | 37.5 | 28 | 50.0 | −4 |
| atoll | 34 | 47.1 | 28 | 46.4 | +6 |
| drumlin | 29 | 44.8 | 25 | 24.0 | +4 |
| eider | 20 | 25.0 | 27 | 37.0 | −7 |
| fjordgate | 19 | 57.9 | 23 | 39.1 | −4 |
| heart | 25 | 60.0 | 32 | 62.5 | −7 |
| hive | 19 | 42.1 | 23 | 17.4 | −4 |
| jackpot | 25 | 40.0 | 27 | 44.4 | −2 |
| lighthouse | 22 | 45.5 | 29 | 41.4 | −7 |
| meander | 30 | 56.7 | 29 | 55.2 | +1 |
| moonrise | 29 | 62.1 | 25 | 44.0 | +4 |
| nordkap | 20 | 35.0 | 28 | 35.7 | −8 |
| saga | 28 | 42.9 | 31 | 48.4 | −3 |
| snowflake | 29 | 51.7 | 25 | 44.0 | +4 |
| **TOTAL** | **385** | **47.0** | **405** | **43.0** | **−20** |

Reading notes:

1. **Pooled, we are close to seat-balanced** (385 A / 405 B over 790 games), so aggregate
   ladder Elo is not systematically seat-biased. Per map the imbalance runs up to ±8
   games on a base of ~20–34, i.e. a per-map row can be 60/40 on seat before any bot
   effect is measured.
2. **Seat is worth ~4 points of win rate to us overall** (47.0% on A vs 43.0% on B), and
   engine `TEAM_A` took **412/790 = 52.2%** of our games. That is smaller than the ~78%
   measured on the small-map probe leg, because it is pooled over all 15 maps — the
   contested-ore maps carry the edge, per `docs/game-model.md`.
3. **The unit of seat variance is the match, not the game.** A per-map arena or ladder
   comparison built from a handful of matches inherits whole blocks of one seat. Combined
   with the already-documented seed amplification (`game-model.md`: a per-map row of N
   games can be ~2 distinct games), a per-map delta drawn from few ladder matches should
   be treated as evidence about *those matches' seats* until it is shown seat-balanced.
   The remedy is the one already in the playbook: weigh the pooled rate plus a mechanism
   explanation, not the per-map row.
4. **Local arena work is unaffected in kind but must still be paired.** Locally we choose
   the seat, so nothing about ladder assignment changes local design — but the ladder will
   hand a candidate five games on one seat at a time, so a candidate that is seat-fragile
   will show up on the ladder as high match-to-match variance rather than as an even
   trickle.

---

## 8. Self-checks

| check | result |
|---|---|
| All five replays present for every OpenSverige match | 158 × 5 = **790/790** |
| Parser errors across the full archive | **0/2,091** files (feature pass and opening-trace pass both clean) |
| Every map layout has one fixed (coreA, coreB) assignment | **13 distinct core-position layouts across 11 dimension classes, 0 exceptions** in 2,091 replays (archipelago/snowflake share 26×26 A@(5,5)/B@(19,19); eider/heart share 28×20 A@(7,9)/B@(19,9)); all 790 of our games' tile-hashes matched one of the 15 files in `maps/` (0 unidentified) |
| Test 1 vs Test 2 independence | Test 1 uses only `Replay.winner` + `scoreA/scoreB`; Test 2 uses only opening traces + "was OpenSverige in this match" + opponent identity. They share no input and agree on all 158 matches. |
| Classifier A vs classifier B agreement where both fire | 510/511 |
| Confident stamps contradicting the metadata mapping | **0/583** (and 0/602 after bootstrap) |
| Matches with mixed seats across their five games | **0/157 stamped** |
| Ambiguous games — counted, not guessed | classifier B abstains on **207/790** (166 below trace-recurrence floor, 41 margin ties); classifier A abstains on 225/790 (219 no-hit, 6 double-hit). All excluded from the pattern table; none of them is a match whose *match-level* seat is unknown, because Test 1 covers all 158. |
| Known false-positive rate of the coarse classifier, stated rather than hidden | 4.09% (106/2,592 hard negatives), which is why classifier B is primary and the 2 union-level disagreements are reported in §4 rather than dropped |
| Scope limit | The archive is 2026-08-07 → 2026-08-08 only. This establishes the rule for the current ladder software; it is not evidence about earlier weeks, and it says nothing about *why* a given team is listed A (that assignment is upstream of the replays and looks like a per-match coin flip from here). |

---

## 9. Suggested edit to `docs/game-model.md`

The open question at `game-model.md:79–90` ("**how the ladder assigns seats within a
best-of-five is a first-order question**") can be closed with:

> **Seat assignment [answered 2026-08-08]: fixed for the whole best-of-five, and metadata
> `teamAName` is engine `TEAM_A` in every archived match.** 158 matches / 790 games:
> engine-A win tally equals `scoreA` in 158/158 (p = 1.4e-132 under a per-game seat coin),
> and 583 behaviourally stamped games put us on our metadata seat 583/583 with 0
> mixed-seat matches. Which team is listed A is an unbiased per-match coin flip
> (uncorrelated with rating, name, id, trigger). Therefore a match's five map draws all
> carry one seat: per-map deltas are seat-confounded at match granularity, and per-map
> rows built from few matches can be seat rather than bot.
> (`docs/research/bo5-seat-assignment-2026-08-08.md`)
