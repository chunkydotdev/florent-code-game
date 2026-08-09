# Opponent nest rate: stable, reproducible, and worthless. Do not build on it.

**Research arm, session 24, 2026-08-09.** Closes the play-the-players lead left at the
bottom of `nest-precursor-refuted-2026-08-09.md` — nest rate by opponent spanning
4.7% to 68.2%, a factor of fourteen.

**Version tag:** live **v92 "PLANK DODGE"** = `bots/_v115dodge`, submission `7b1d8d73`
(shipped by the builder arm at ~13:0x; v91 `bots/_v100hf` is the rollback control).
**Corpus only, zero replay downloads.** Frozen snapshot at 13:18 — `join.tsv` 1,355
rows (md5 `f3bc78bc`), `events.tsv` 882,645 rows — because **the keeper was appending
live during the run** and grew `join.tsv` 1,350→1,355 mid-analysis. Anyone re-running
against the live corpus will get slightly different n.

**Label reproduces:** corpus-wide **881/3,465 = 25.4%** on the grown corpus, against the
published **834/3,295 = 25.3%**.

---

## The verdict in one line

**Nest rate is a genuinely opponent-stable property — and it predicts nothing we care
about. It is a real, reproducible, actionable-in-principle prior on a quantity that
does not move our outcomes.**

## 1. It is stable. That part of the lead was right.

| split (unit = MATCH, 5 games) | Pearson r | Spearman | slope |
| --- | ---: | ---: | ---: |
| **A — interleaved by chronological match rank** (isolates sampling noise) | **0.888** | 0.762 | 0.86 |
| **B — chronological halves** (noise + real drift) | **0.782** | 0.685 | 0.80 |
| A, standardised on round band | 0.817 | — | — |

12 opponents with ≥6 matches and ≥60 seeds. Cluster-permutation (shuffle opponent
labels across matches preserving match sizes, 4,000 reps): observed between-opponent
variance **0.01811 against a null mean of 0.00365, p = 0.0002**; observed spread 61.3pp
against a median null spread of 23.9pp. Leave-one-match-out at seed level: opponent
prior **Brier 0.1759 vs 0.1902** for the global base rate — **+7.5% skill**.

**This reproduces better than almost anything else measured in this corpus.** It is not
the failure mode.

## 2. It predicts nothing we care about. That is the failure mode.

Across the 15 opponents with ≥60 seeds:

| relationship | Pearson r | Spearman |
| --- | ---: | ---: |
| nest rate ↔ **our win rate** | **−0.074** | −0.229 |
| nest rate ↔ **our home builder deaths / 1k builder-rounds** | **−0.003** | +0.218 |
| nest rate ↔ home builder deaths per game | +0.102 | — |

**The nesting leaders are not the teams beating us.** The three worst for our home
builder deaths are exactly the three the attribution doc named — **Ouroboros** (4.16 per
1k builder-rounds, we win **15%**), **Lunds Stallions** (4.02, 28.5%), **Powerpuff
Girls** (2.13, 35.0%) — and **two of them nest below the 25.4% field average** (22.8%
and 17.8%). Meanwhile the top nester, **Team 48 at 66.5%**, is a team **we beat 62% of
the time** while losing **0.6 home builders per game**.

Within games, demeaned by opponent (n=1,107 games with ≥1 seed): r(nests, home
deaths/1k) = **+0.096**, r(nests, we won) = **−0.100**. And stratifying on seed count
dissolves it:

| seeds planted that game | home deaths/1k, no nest | with nest |
| --- | ---: | ---: |
| 1 | 0.87 (n=205) | 2.92 (n=191) |
| 2 | 1.16 | 1.80 |
| 3–4 | 1.85 | 2.20 |
| **5+** | **1.95** | **1.89** |

**The harm tracks plant COUNT, not nest formation.** Win rate shows no consistent nest
effect in any stratum.

## 3. The per-opponent table — and how the "factor of 14" should actually be quoted

**ICC of the nest label is 0.148 within match and 0.249 within game**; at 12.9
seeds/match that is a **design effect of 2.76**, so **plant-level intervals are ~1.7×
too narrow.** Team 48's "n=170 plants" is **20 matches / 97 games.**

| opponent | matches | games | seeds | nest rate | 95% CI (match-clustered) |
| --- | ---: | ---: | ---: | ---: | --- |
| Team 48 | 20 | 97 | 176 | **66.5%** | [60.8, 72.3] |
| Orizon | 5 | 25 | 69 | 49.3% | [40.8, 61.5] |
| Powerpuff Girls | 20 | 56 | 89 | 40.4% | [27.2, 54.7] |
| Banminary | 13 | 64 | 205 | 33.2% | [28.1, 39.1] |
| OopsGotYourElo | 18 | 61 | 127 | 32.3% | [25.6, 40.4] |
| Kings College Munich | 22 | 107 | 312 | 30.4% | [25.9, 35.2] |
| CtrlAltDefeat | 17 | 82 | 299 | 25.1% | [20.9, 30.0] |
| Ouroboros | 20 | 90 | 324 | 22.8% | [18.7, 26.9] |
| Leviathan | 17 | 71 | 554 | 19.7% | [11.7, 30.4] |
| Askar City | 14 | 66 | 104 | 18.3% | [10.2, 27.5] |
| Lunds Stallions | 26 | 127 | 398 | 17.8% | [13.1, 22.5] |
| Memtrace | 17 | 55 | 146 | 15.1% | [8.5, 22.5] |
| The Bisons | 5 | 20 | 89 | 14.6% | [7.6, 37.9] |
| I Stone | 8 | 20 | 129 | **5.4%** | [1.3, 16.9] |
| farming_200s | 4 | 18 | 175 | 5.1% | [2.2, 15.0] |

The extremes do not overlap, so **the ordering is real** — but the honest quotation is
**66.5% [60.8–72.3] vs 5.4% [1.3–16.9]**, and **at the interval edges it is a factor of
about 4, not 14.**

## 4. Confounding — and the one thing that would have to change if a prior were ever built

* **Round composition: partly, not mostly.** The published gradient reproduces
  (r0–50 **39.0%** n=1,129 → r301+ **13.6%** n=788), and opponents differ hugely in
  *when* they plant (Team 48: 73% of seeds in r0–50; I Stone: 74% at r301+). Indirect
  standardisation still leaves **O/E from 0.22 to 1.94** — a factor of ~9 — and
  within-band contrasts confirm it (at r0–50: Team 48 69% n=129, Ouroboros 47% n=49,
  field 39%, Memtrace 7% n=46). Out-of-sample Brier, match-disjoint 2-fold: global
  0.1896 → round band 0.1803 → opponent 0.1775 → **opponent × round band 0.1750.**
  **If a prior were ever built the key is opponent × round band, not opponent.**
* **Opponent version: no detectable effect, and untestable where it matters most.**
  Within-opponent between-version variance 0.00573 against a between-match noise floor
  of 0.01140; permutation over 10 opponents × 3,000 reps gives **1 of 10 significant at
  p<0.05 — chance.** But **Ouroboros (v8), Team 48 (v16), OopsGotYourElo (v21), Orizon
  (v34) and The Bisons (v2) appear in our corpus on exactly ONE version each**, so for
  the extreme nester opponent and version are **perfectly confounded**, and a prior
  keyed on opponent would be stale the day they ship.
* **Map: separable, with two exceptions.** Map spread 16.4% (moonrise) to 34.5%
  (antler); expected-from-map-mix rates all fall in **22–28%** against observed 5–66%,
  so map explains almost none of it. Within-map confirms (meander: Team 48 79% n=19,
  farming_200s **0%** n=73; atoll: Team 48 57%, I Stone **0%** n=89). **Not separable:
  I Stone (69% of seeds on atoll) and The Bisons (69% on fjordgate).**
* **Seat: null overall, decisive for two opponents.** Seat 0 24.3% (n=1,593) vs seat 1
  26.4% (n=1,872), z = −1.41. But **Leviathan −18.9pp** (32.3% n=186 vs 13.3% n=368)
  and Memtrace +16.0pp. Since `d2` is to the NW corner, the band is not the same
  physical region for the two seats, and for those opponents **seat moves the estimate
  as much as opponent identity does.**
* **Our own bot version: uninterpretable.** 6.5% (v66) to 37.9% (v72), no monotonicity,
  confounded with ladder time and opponent mix. Every per-opponent rate is averaged
  over a changing "us".
* **Label sensitivity: the low end is partly seed MORTALITY, not restraint.**
  r(nest rate, seed-alive-at-30-rounds) across opponents = **+0.633**. Leviathan 15.9%
  alive at +30 (median seed life 9 rounds), farming_200s 8.6% (4 rounds), I Stone 16.3%
  (2 rounds). Dropping the coexistence requirement raises Leviathan 19.7→34.8% and
  Memtrace 15.1→32.9% — **but the ranking survives, r(strict, loose) = 0.964.**

## 5. A THIRD ALL-NULL CORPUS COLUMN, AND A GAP IN THE TOOL THAT EXISTS TO CATCH THEM

**`oppver` is NULL in every row of both `corpus/join.tsv` (1,355) and
`corpus/ladder_games.tsv` (2,625).** I verified this myself rather than relaying it:
`oppver` has exactly **one distinct value, the literal string `None`**, in both files,
while `ourver` is fully populated (25 and 82 distinct values).

**`tools/corpus_sanity.py` cannot catch it, and I checked why.** At line 30 it filters
`r.get(col) not in (None, "")` — the *string* `"None"` passes that filter — and then at
line 33 `float("None")` raises `ValueError`, which is caught and `continue`d. **The tool
silently skips every non-numeric column.** It catches all-zero numeric columns and is
structurally blind to all-null string columns, which is exactly `oppver`'s shape.

**This is corpus trap 7**, after `econ.tsv:shots` and `econ.tsv:deliveries`. **The
working substitute is `corpus/league_matches.tsv`'s `teamAVersion`/`teamBVersion`
joined on match id — 236 of 271 of our matches, 85.7% of seeds.** The sanity tool
belongs to the builder's lane; flagged, not edited.

## 6. Limits

* **The home-builder-death denominator is a proxy** — numerator is our builder DEATH
  rows with `d2_own ≤ 32`, denominator is **all** our builder-rounds in the game.
  Per-round positions are not in the corpus, so a true home builder-round count needs a
  replay decode.
* **`destroy()` remains indistinguishable from a kill**, so "seed alive at +30" is
  really "seed still on the map" — and that feeds directly into the coexistence
  requirement and therefore into the nest label itself.
* **Causality is untouched.** The harm null is observational: it says high-nesting
  opponents do not hurt us more, **not** that a nest-specific counter would fail to
  help.
* **Our games only**, 4–26 matches per opponent. Everything here is "against us,
  against a version of us that changed 20 times".
* **Intent is unobservable** — a nest is still two plants near each other, not a
  demonstrated plan.

## Provenance

Analysis by a research-arm subagent (`opus`); scripts `n1_seeds.py` … `n9_harm.py` in
the session scratchpad, method fully stated above, all reading the frozen 13:18
snapshot. The `oppver` null and the `corpus_sanity.py` blind spot were **re-verified by
me directly against the committed corpus and the committed tool** before publication.
