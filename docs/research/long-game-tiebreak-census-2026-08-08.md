# Long-game tiebreak census — the missing denominator (2026-08-08)

**Research arm. Measurement only — no bot edits, no arena, no downloads.
Everything below is read from `replay_archive/` already on disk.**

## Purpose

A defensive "posture" under evaluation suppresses economy. A prior census
found 4/4 full-length games where that posture pins for the whole game
(without the enemy ever dealing core damage) were **losses decided on the
titanium tiebreak** — all 4 against Ouroboros, an obvious selection worry.
This document supplies the denominator: across **all** our games, how often
do we go the full distance and get decided on economy, against whom, and by
what margins?

## 0. Version tags and corpus

| | |
|---|---|
| Live version at write time | **v80 "Eir 9b"** = `bots/_v89sh/main.py`, md5 `e12f8585` (confirmed: `md5 -q bots/_v89sh/main.py` → `e12f8585…`) — content byte-identical to v77 "Eir 9" (rollback-of-rollback; see `HANDOVER.md` item 2) |
| Archive read | `replay_archive/` as of 2026-08-08 evening: **554 `*.meta.json`, 2,771 `*.replay26`** |
| Our matches in archive | **225 matches** where `teamAName`/`teamBName` == `OpenSverige` — **167 `triggeredBy=ladder`, 58 `unrated`** — every one `status=complete`, every one has all 5 `_game_1..5.replay26` present (1,125 of 1,125 game files, 0 missing, 0 parse failures) |
| Our version span in archive | ladder games span our **v64–v80** (submission-counter version, not bot-dir name) |
| **Era split used below** | **pre-v75** (v64–74, n=560 ladder games) vs **v75+** (v75–80, n=275 ladder games) — the modern line per the brief. v77 and v80 share bytes (see above), so they are the same bot content under two version numbers; both are counted in their own version bucket for the trend table but represent one behavioural point where noted. |
| Seat identification | Per `docs/research/bo5-seat-assignment-2026-08-08.md` (validated 2026-08-08, 158/158 + 583/583 checks, 0 exceptions): **metadata `teamAName` is engine `TEAM_A` for the whole match, always.** Used directly — no behavioural classifier needed. |
| Headline scope | **Ladder matches only** (167 matches / 835 games) per the brief; unrated (58 matches / 290 games) reported separately in §6, not pooled into the headline numbers. |
| Tooling | `tools/replay_census.py`'s `Replay` class, driven from a scratch script (`census.py` + `analyze.py`, session scratchpad) — no new parsing logic; reused the existing entity/flow/win-condition decode. |

**Tiebreak-level decode shortcut, validated below:** the replay's undeclared
`winCondition` field (`tools/replay_schema.md`) already names the deciding
tiebreak directly when a game reaches round 1000: `titanium_collected` (level
1 — this is the *delivered* metric, not stored, per `docs/game-model.md`),
`harvesters` (level 2), `titanium_stored` (level 3). No `coinflip` value was
observed anywhere in the archive (see §7). This was used instead of manually
re-deriving the tiebreak from the raw fields, then cross-checked (§7).

---

## 1. Length distribution (ladder, n=835 games / 167 matches)

| outcome | games | share |
|---|---|---|
| **Full-length (round 1000, tiebreak decides)** | **219** | **26.2%** |
| Core destroyed (< round 1000) | 616 | 73.8% |

All 616 short games carry `win_condition == core_destroyed` — no other short-game
outcome exists in the corpus (confirms core-kill and tiebreak are exhaustive
and mutually exclusive, as the rules imply).

Round-length histogram, `core_destroyed` games only:

| rounds | 0–100 | 100–200 | 200–300 | 300–400 | 400–500 | 500–600 | 600–700 | 700–800 | 800–900 | 900–1000 |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 96 | 181 | 111 | 80 | 54 | 26 | 28 | 16 | 13 | 11 |

Skewed early — over 40% of all core kills (277/616) land before round 200.

**By era:**

| era | n | full-length | rate |
|---|---|---|---|
| pre-v75 | 560 | 137 | 24.5% |
| v75+ | 275 | 82 | **29.8%** |

**By our seat** (engine `TEAM_A`/`TEAM_B`, fixed per match):

| seat | n | full-length | rate |
|---|---|---|---|
| A | 435 | 135 | **31.0%** |
| B | 400 | 84 | 21.0% |

Seat B games reach full length markedly less often than seat A (10 points).
This is consistent with the known seat/map win-rate asymmetry already
documented (`docs/research/bo5-seat-assignment-2026-08-08.md`: seat worth
~4pp win rate) rather than a new finding — noted, not investigated further
here.

**By version** (n = games at that version, ladder only):

| v | 64 | 65 | 66 | 67 | 68 | 69 | 70 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| n | 25 | 45 | 20 | 35 | 95 | 45 | 40 | 25 | 135 | 25 | 70 | 70 | 40 | 30 | 10 | 35 | 90 |
| full% | 32.0 | 35.6 | **0.0** | 31.4 | 24.2 | 20.0 | 32.5 | 36.0 | 20.0 | 12.0 | 25.7 | 28.6 | 17.5 | 40.0 | **0.0** | 28.6 | **36.7** |

v66 (n=20) and v78 (n=10) show 0% full-length — small-n, flagged rather than
interpreted. v80 (live, n=90) is the largest single-version sample and the
highest rate among versions with n≥30 (36.7%).

---

## 2. Tiebreak level distribution (ladder, full-length games only, n=219)

| level | what it is | n | share of full-length games | our record |
|---|---|---|---|---|
| **1 — titanium delivered** | `win_condition == titanium_collected` | **219** | **100%** | **130 W – 89 L (59.4%)** |
| 2 — harvesters alive | `win_condition == harvesters` | 0 | 0% | — |
| 3 — titanium stored | `win_condition == titanium_stored` | 0 | 0% | — |
| 4 — coinflip | (not observed) | 0 | 0% | — |

**Every single ladder full-length game in the archive was decided on level 1
(delivered titanium).** Levels 2–4 never fired once in 219 ladder full-length
games. (One level-2 game exists elsewhere in the archive — an *unrated*
OpenSverige-vs-Powered-by-SmartFridge game, delivered tied 2480–2480, decided 2–1 harvesters;
see §6 and §7. No level-3 or level-4 case exists anywhere in the archive.)
This matches the shape found in the unrelated local-arena tiebreak-split
decode (`docs/research/tiebreak-split-decode-2026-08-07.md`: harvesters
decided 0/120 there too) — independent corpus, same structural finding: in
this game, ties precise enough to fall through level 1 are essentially never
observed in practice at the population sizes played so far.

**Consequence: "full-length game" and "delivered-titanium-decided game" are
the same population in the ladder archive.** 219/219, not 4/4.

---

## 3. Per-opponent table (ladder, full-length games, n=219)

| opponent | n | our record (W–L) | our win% | level-1 L |
|---|---|---|---|---|
| OopsGotYourElo | 34 | 23–11 | 67.6% | 11 |
| Powerpuff Girls | 27 | 15–12 | 55.6% | 12 |
| **Ouroboros** | **26** | **6–20** | **23.1%** | **20** |
| Lunds Stallions | 19 | 8–11 | 42.1% | 11 |
| I Stone | 18 | 10–8 | 55.6% | 8 |
| Memtrace | 17 | 12–5 | 70.6% | 5 |
| Kings College Munich | 16 | 10–6 | 62.5% | 6 |
| CtrlAltDefeat | 14 | 11–3 | 78.6% | 3 |
| Leviathan | 9 | 8–1 | 88.9% | 1 |
| Orizon | 6 | 6–0 | 100% | 0 |
| opensverige - plan B | 6 | 4–2 | 66.7% | 2 |
| Focalground | 5 | 5–0 | 100% | 0 |
| Askar City | 5 | 4–1 | 80.0% | 1 |
| Coreflood | 4 | 2–2 | 50.0% | 2 |
| 0033 | 3 | 2–1 | 66.7% | 1 |
| Team 48 | 2 | 0–2 | 0.0% | 2 |
| SingleCore | 2 | 2–0 | 100% | 0 |
| Jacobs Code | 1 | 0–1 | 0.0% | 1 |
| Viktor5776 | 1 | 1–0 | 100% | 0 |
| kladde chatte tville (och oss) | 1 | 1–0 | 100% | 0 |
| farming_200s | 1 | 0–1 | 0.0% | 1 |
| Banminary | 1 | 0–1 | 0.0% | 1 |
| gsxWins | 1 | 0–1 | 0.0% | 1 |

**Every level-1 loss column exactly equals the "L" column** in this table
(all 219 games are level 1, per §2), so "L" and "level-1 L" are the same
number here.

**Answer to the selection worry: general across the field, not
Ouroboros-specific.** Level-1 losses occur against **14 of 23 opponents** we
played a full-length game against, spanning small and large samples alike:
OopsGotYourElo (11), Powerpuff Girls (12), Ouroboros (20), Lunds Stallions
(11), I Stone (8), Memtrace (5), Kings College Munich (6), CtrlAltDefeat (3),
Team 48 (2), opensverige-plan B (2), Coreflood (2), Leviathan (1), Askar City
(1), 0033 (1), plus four single-game opponents (Jacobs Code, farming_200s,
Banminary, gsxWins).

That said, **Ouroboros is the one clear outlier by rate, not just by
count**: 23.1% win rate at n=26 is far below every other opponent with n≥14
(next-worst is Lunds Stallions at 42.1%, n=19). Ouroboros contributes 20/89 =
22.5% of all level-1 losses — the single biggest slice, but well under half.
Its full-length games span versions 65, 67–69, 72–75, 77, 79, 80 — spread
across both eras, not concentrated in one bot generation, so the Ouroboros
weakness is not an artifact of when we happened to play them.

---

## 4. Margin distribution, level-1 games (ladder, n=219: 130 W / 89 L)

Margin = our delivered − their delivered (Ti). Ratio = margin / their
delivered (guards against div-by-zero with `max(theirs, 1)`).

| | n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|---|
| **margin — WINS** | 130 | +20 | +2,780 | **+6,065** | +9,430 | +31,300 | +7,134 |
| **margin — LOSSES** | 89 | −28,820 | −9,140 | **−6,310** | −2,280 | −60 | −6,532 |

Ratio (margin/theirs): wins median **+112.5%**, losses median **−42.2%**.
(Mean ratio is not reported — a handful of wins against opponents who
delivered near-zero titanium produce ratios in the hundreds-to-thousands of
percent and make the mean meaningless; median is the honest summary here.)

**This is the decisive output.** The loss population is not one of blowouts:

| plausible-flip threshold | level-1 LOSSES within threshold | share of 89 |
|---|---|---|
| within 10% of opponent's total | **9** | 10.1% |
| within 25% of opponent's total | **25** | 28.1% |
| within 50% of opponent's total | **49** | 55.1% |

Over half of our level-1 losses (49/89) are within 50% of the winning
total, and more than a quarter (25/89) are within 25%. The single closest
loss is a 60-titanium deficit out of 9,440 (0.6%, vs Kings College Munich,
match `1e8c4e1b` g1); the next closest are 190 Ti (2.5%, I Stone `f9a0f66d`
g4) and 260 Ti (1.3%, OopsGotYourElo `94a8c05c` g2).

The population is not uniformly close, either — 40 of 89 losses (44.9%) sit
beyond the 50% mark, several of them clear routs (deficits of 70–97% against
Ouroboros, I Stone, CtrlAltDefeat, Team 48, OopsGotYourElo). **Read this as a
descriptive margin distribution, not a claim that any specific economy
change would flip a specific count of games** — a distribution with real
mass near zero is a distribution where a modest economy shift is
*structurally capable* of moving outcomes; it says nothing about whether the
posture change under evaluation is that shift, or how many of these 9/25/49
games it would actually touch, since none of these games ran the posture
being tested.

---

## 5. Trend across versions (ladder)

Full-length rate by era: **pre-v75 24.5% (n=560) → v75+ 29.8% (n=275)**, a
+5.3pp rise. Per-version, the rate is noisy (0%–40%, n from 10 to 135 —
see §1 table) and does not show a clean monotonic trend inside either era;
the era-level shift is a real but modest effect, consistent with — not proof
of — a modern line that plays for the long game slightly more often than the
pre-v75 line. This is directionally the same conclusion the brief's premise
implies (a defensive posture suppressing economy would be expected to
correlate with *more* full-length games, not fewer), and the data is
consistent with that without establishing the posture as the cause: era also
carries every other bot change made across 16 versions, not just the posture
in question.

---

## 6. Unrated games, reported separately (not pooled into headline)

58 matches / 290 games. Full-length: 51/290 = 17.6% (well below ladder's
26.2% — unrated challenges likely skew toward different opponents/settings
and should not be blended into the ladder headline). Tiebreak levels among
the 51 full-length unrated games: **level 1 = 50, level 2 = 1, level 3 = 0**.
Our level-1 record: 22 W – 28 L (44.0%), worse than the ladder's 59.4% —
plausibly an opponent-mix effect (unrated challenges are not a random sample
of the ladder field) rather than anything about the posture question; not
investigated further, out of scope for this brief.

The one level-2 (harvesters) game in the whole archive is unrated: match
`08d0654d…` game 2 vs `Powered by SmartFridge`, delivered titanium tied exactly 2480–2480,
harvesters 2 (us) vs 1 (them), we won — textbook level-2 decision, useful as
a positive control that the tiebreak-level decode is reading real ties, not
an artifact (see §7).

---

## 7. Self-checks

| check | method | result |
|---|---|---|
| **Parser errors** | `Replay(path)` over all 1,125 of our archived game files | **0 failures** |
| **`core_deliv × 10 == titaniumCollected`**, per team-side per game, our matches | checked every side of every one of our 1,125 games (2,250 team-sides) | **2,249/2,250 exact (99.96%)** — the one exception is `9aae86c9… game 3` (unrated, vs `sporks`), not a ladder game, and not in any headline number above |
| Same check, **whole archive** (not just us) | all 2,771 replay files, both sides (≈5,542 team-sides) | **3 mismatches**, all short `core_destroyed` games (rounds 104/105/134), all involving the same opponent, `sporks`, on one side — consistent with an in-flight delivery stack at the exact moment of core death, not a systematic parser defect. Our one mismatch above is one of these three. |
| **Winner agreement**: per-match engine-`TEAM_A`/`TEAM_B` win tally vs meta `scoreA`/`scoreB` | all 225 of our matches (167 ladder + 58 unrated), 5 games each | **225/225 agree, 0 disagreements** |
| **Seat mapping** (meta `teamAName` == engine `TEAM_A`) | reused, not re-derived: `docs/research/bo5-seat-assignment-2026-08-08.md`, validated same-day at 158/158 (match-level, p=1.4e-132 under null) + 583/583 (game-level behavioural stamp), 0 exceptions | adopted directly |
| **Tiebreak-level decode via `win_condition` string vs manual field comparison** | for every level-1 game (n=269, ladder+unrated), checked `our_win == (our_deliv > opp_deliv)` | **0/269 mismatches** |
| Level-2 sanity check | the one level-2 game found: delivered titanium tied exactly, harvester count differed, winner matched the higher-harvester side | consistent, positive control (§6) |
| Level 3 / 4 | 0 instances anywhere in the 2,771-replay archive | nothing to validate; noted as a null result, not assumed |
| "Full-length" definition | `rounds == 1000` used as the operational definition; cross-checked against `win_condition`: **100% of `rounds==1000` games carry a tiebreak `win_condition` (titanium_collected/harvesters/titanium_stored) and 0% of `rounds<1000` games do** (all are `core_destroyed`) | exhaustive, no edge cases |
| Version/seat/opponent extraction | straight from meta JSON fields (`teamAVersion`/`teamBVersion`, `teamAName`/`teamBName`, `triggeredBy`), no inference | n/a — ground truth fields |

---

## What this says about the economy-release question — and what it doesn't

**What the denominator establishes:**

1. **Full-length games are ~26% of our ladder games (219/835)**, and **every
   one of them (219/219) is decided at tiebreak level 1 — delivered
   titanium.** "Full-length" and "delivered-titanium-decided" are the same
   population here; there is no dilution from levels 2–4 to worry about.
2. **The population the posture-suppression worry lives in is real and not
   small**: 219 games, 89 of them losses.
3. **Losing long games on delivered titanium is a general phenomenon across
   the field** — it happens against 14 of 23 opponents we've played a
   full-length game against — **not a Ouroboros-only artifact.** Ouroboros
   is the worst single opponent by rate (23.1% win, n=26) and the largest
   single contributor to the loss count (20/89), but it is a large minority
   share, not the whole picture.
4. **The margin distribution on those 89 losses has real mass near zero**:
   9 within 10%, 25 within 25%, 49 within 50% of the opponent's total. A
   population this close is one where a modest economy improvement is
   *structurally capable* of flipping some outcomes.
5. **The full-length rate rose modestly from the pre-v75 to the v75+ era**
   (24.5% → 29.8%), directionally consistent with — though not proof of — a
   more defensive modern line producing more games that go the distance.

**What this does NOT establish:**

- **No counterfactual.** None of these 219 games were played with the
  specific posture change under evaluation isolated as a variable; this
  census cannot say how many of the 9/25/49 flip-range losses the change
  would actually touch, or whether it would touch any of them at all — it
  only describes how much room for a flip exists in principle.
- **Not causal on the era trend.** The pre-v75 → v75+ full-length-rate rise
  is a population-level correlation across 16 bot versions carrying many
  changes at once, not an isolated effect of the posture in question.
- **Not a same-opponent, same-map, same-seed comparison.** These are wild
  ladder outcomes against a field of independently-evolving opponents;
  opponent version drift, map draw, and seat (see §1) are all uncontrolled
  here. Use this as the population denominator the posture question needed,
  not as a verdict on the posture itself.
- **Blowout losses are also real** (40/89 losses sit beyond the 50%-of-total
  mark) — the loss population is mixed, not uniformly rescuable.

---

## Appendix — full per-game level-1 loss and win lists

Full per-game detail (match id prefix, game, opponent, our/opp delivered
titanium, margin, deficit or surplus %) for all 89 level-1 losses and 130
level-1 wins is in the scratch analysis output
(`census.py`/`analyze.py`, session scratchpad — not committed; regenerate
from `replay_archive/` + `tools/replay_census.py` if needed, both files are
short and reuse only existing parsing code). The ten closest losses (by
deficit): Kings College Munich 0.6% (60 Ti), I Stone 2.5% (190 Ti),
OopsGotYourElo 1.3% (260 Ti), CtrlAltDefeat 8.0% (400 Ti), Memtrace 2.9%
(550 Ti), OopsGotYourElo 6.6% (580 Ti), Lunds Stallions 9.0% (590 Ti),
Ouroboros 4.1% (630 Ti), I Stone 19.0% (1,160 Ti), Kings College Munich
25.6% (1,260 Ti).
