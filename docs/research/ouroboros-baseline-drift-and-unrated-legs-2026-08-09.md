# Ouroboros: PREREG baseline drift + both unrated legs, confirmed from primary sources

**Research arm, session 25, 2026-08-09 ~16:30 CEST.** Commissioned by the side lane
(re-scoped): *independently recompute the per-(map,seat) baseline vs Ouroboros from the
SYNCED corpus and diff it against the frozen table in `PREREG-ouroboros-loki2-2026-08-09.md`;
then list every post-freeze game vs Ouroboros with map, seat, win condition and kill round.*

**Version tag.** Live slot **v94** = `bots/_v115dodge` (Eir/v92 tree), treehash `6ae6871c`,
submission `d7a0cd62`, 1580 @ #28. The probed bot is **v93** = `bots/_v118loki2b`
(submitted, held the slot ~18 s, rolled off — **not** active). Corpus git sha `7418e13`.

**Sources read, exactly.** Frozen snapshot of `corpus/ladder_games.tsv` (2,715 game rows,
md5 `ca2c6f59…`) and `corpus/join.tsv` (1,445 rows, md5 `e943d4ac…`), copied to scratchpad
before analysing — the keeper auto-syncs and the archive moved from 6,193 to 6,233 replays
*during this session*, which is exactly the mid-run growth hazard s24 logged. Plus the free
platform channel: `fcode match list --type unrated --mine --json` and `fcode match info
--json` on two match ids. **Zero replay downloads.**

**Method note on anchoring.** The per-(map,seat) table below was computed **before** I
opened the PREREG, then diffed against it. That ordering is the point of the request.

---

## 1. THE DIFF — two cells moved, and the cause is NOT new play

Recomputed from the synced corpus, against the PREREG's frozen table:

| map | seat | PREREG (15:37) | recomputed (16:08) | moved? |
| --- | --- | --- | --- | --- |
| lighthouse | a | 0/8 | 0/8 | — |
| lighthouse | b | 0/5 | 0/5 | — |
| atoll | a | 0/11 | 0/11 | — |
| atoll | b | 0/3 | 0/3 | — |
| eider | a | 0/6 | 0/6 | — |
| eider | b | 0/4 | 0/4 | — |
| **drumlin** | **a** | **0/5** | **0/6** | **+1 game, still 0%** |
| drumlin | b | 0/3 | 0/3 | — |
| hive | a | 0/5 | 0/5 | — |
| hive | b | 0/2 | 0/2 | — |
| saga | a | 0/11 | 0/11 | — |
| **saga** | **b** | **0/6** | **1/7 = 14.3%** | **CELL IS NO LONGER 0%** |

Headline aggregates likewise:

| | PREREG (15:37) | recomputed (16:08) |
| --- | --- | --- |
| overall | 15.3% (23/150) | **16.8% (26/155)** |
| core-decided | 9/86 = 10% | **9/87 = 10.3%** |
| tiebreak | 14/64 = 22% | **17/68 = 25.0%** |

**The whole difference is one ladder match**, `3f1be807-92cc-4a6c-9b97-620f81e81cfa`,
5 games, `ourver 92`: drumlin/a L (tiebreak), nordkap/a L (core, r413), **saga/b W
(tiebreak, r1000)**, **meander/b W (tiebreak, r1000)**, **antler/b W (tiebreak, r1000)**.
Removing it reproduces the PREREG's numbers **exactly** — 23/150, 9/86, 14/64, and every
cell back to 0. So the recompute and the frozen table agree on a common population; there
is no methodological disagreement to resolve.

**But note WHEN that match was played: `2026-08-09T12:42:43Z` = 14:42 CEST — fifty-five
minutes BEFORE the PREREG was committed at 15:37 CEST.** It is not post-freeze play. It is
**decode latency**: the game existed on the platform, and had not yet reached
`ladder_games.tsv` when the baseline was frozen from it.

**What this does and does not damage.** It does **not** damage the anti-fitting property —
the prediction was still locked before the Loki-2 leg ran, which is what the
pre-registration is for. It **does** mean the sentence *"every cell is 0%, so any single
win is signal"* is **now false for one cell in the table**: `saga/b` is 1/7. Saga is not in
the PREREG's *primary* map list `{lighthouse, atoll, eider, drumlin, hive}`, so the
falsifiable prediction is untouched; the five primary maps are still 0/50 across both seats.
**The correct amendment is one sentence in the next dated result doc, not a re-freeze.**

**Generalisable, and it is the s24 freeze lesson pointing at a different clock:** freezing a
baseline from the corpus freezes *what has been decoded*, not *what has been played*. Those
differed by ~3 hours here. Any future pre-registration whose baseline comes from `corpus/`
should either sync immediately before freezing, or state the decode lag it accepted.

---

## 2. POST-FREEZE LADDER GAMES vs OUROBOROS: **ZERO**

Rows in the frozen `ladder_games.tsv` with `created >= 2026-08-09T13:37Z` (the PREREG
commit instant), opponent Ouroboros: **0**. The most recent Ouroboros *ladder* match is the
12:42:43Z one above. So there is no post-freeze ladder evidence at all yet.

**And the corpus structurally cannot answer the unrated half of the question.**
`ladder_games.tsv` is ladder-only by construction, and `join.tsv` maps replay files only to
our *ladder* matches — unrated files fall into the 4,788 unmatched. Asking the corpus about
the 15:50 unrated leg returns nothing, and that is a decoder limit, not an absence of games.
**The free `match list --type unrated` channel answers it instead**, and does so completely.

---

## 3. BOTH UNRATED LEGS vs OUROBOROS, GAME BY GAME (free channel, primary)

Two unrated legs were fired against Ouroboros today, **27 minutes apart**, on the **same
five maps** (different seeds) — a v92 control and the Loki-2b probe.

### Leg A — BASELINE, `3c6d91d2-94d4-49d1-a797-de51e9e56e18`, **v92**, completed 13:22:23Z (15:22 CEST). We are seat **b**. Result **1–4**.

| # | map | seat | result | win condition | turns |
| --- | --- | --- | --- | --- | --- |
| 1 | saga | b | **WIN** | `titanium_collected` | 1000 |
| 2 | atoll | b | loss | `core_destroyed` | 563 |
| 3 | lighthouse | b | loss | `titanium_collected` | 1000 |
| 4 | eider | b | loss | `core_destroyed` | 521 |
| 5 | nordkap | b | loss | `core_destroyed` | 279 |

**3/5 core-decided. Our single win is an r1000 tiebreak steal.**

### Leg B — PROBE, `d4db288e-9b24-487a-a30f-6b7e63c0b408`, **v93 = `_v118loki2b`**, completed 13:49:53Z (15:49 CEST). We are seat **a**. Result **1–4**.

| # | map | seat | result | win condition | turns |
| --- | --- | --- | --- | --- | --- |
| 1 | saga | a | loss | `core_destroyed` | 351 |
| 2 | atoll | a | loss | `core_destroyed` | 720 |
| 3 | **lighthouse** | **a** | **WIN** | **`core_destroyed`** | **211** |
| 4 | eider | a | loss | `core_destroyed` | 338 |
| 5 | nordkap | a | loss | `core_destroyed` | 361 |

**5/5 core-decided. Our single win is a CORE KILL at r211.**

**The side lane's headline is CONFIRMED from primary source on every element**: 5/5
core-decided vs 3/5 baseline; the win moved from an r1000 tiebreak to a core kill at r211.
Nothing was taken from memory of a commit message.

### The ladder cell that win landed on

Leg B was **entirely seat a**. Ladder baseline on those five (map, seat-a) cells, from the
frozen corpus: saga 0/11, atoll 0/11, lighthouse 0/8, eider 0/6, nordkap 0/6 — **0 wins in
42 ladder games.** Leg B took 1/5, by core kill, on `lighthouse/a`, which is a **primary**
PREREG map and a **0/8** cell.

Against `KILL_WINDOW_RND: 250`: **r211 is inside the window.** It is the only game of the
ten that is.

---

## 4. THREE THINGS THE COMPARISON CANNOT CARRY, stated because they are easy to lose

1. **THE TWO LEGS ARE ON OPPOSITE SEATS.** Baseline = seat b throughout; probe = seat a
   throughout. Unrated flips seats, and the PREREG anticipated this (item 3) by requiring
   the seat be recorded — it is recorded here. But *"the win moved from tiebreak to core
   kill"* also moved **map** (saga/b → lighthouse/a) **and seat**, so it is not a paired
   comparison of one cell; it is one win in each of two differently-seated legs.
2. **THE BASELINE LEG WAS ALREADY VISIBLE WHEN THE PREREG WAS LOCKED.** Leg A completed
   **13:22:23Z**, fifteen minutes *before* the 13:37Z commit. The PREREG's *ladder* baseline
   is genuinely pre-committed and unaffected; but if any later doc uses **Leg A** as the
   comparator for Leg B, that comparator was **observable at lock time** and must be
   labelled as such rather than presented as a blind control.
3. **n=5, and the PREREG's own bar is ≥3 core-kill wins in a 10-game leg.** Leg B is half a
   leg and returned **1**. Whether that is on pace, or a coin, is the side lane's and the
   builder's call — **this document reports data and writes no verdict.** The one thing the
   data does say cleanly is that the *win condition mix* moved hard: 3/5 → 5/5 core-decided,
   i.e. Loki-2b converts tiebreak games into decided games in both directions, including the
   four it lost.

---

## 5. LIMITS / NON-COVERAGE

- Ladder cells are **"against us, in N archived ladder games"**, never "Ouroboros never
  wins X" — per-opponent archive coverage is not a field sample (corpus trap 4).
- **Version columns are dead** in `join.tsv` (`oppver`), `ladder_games.tsv` (`oppver`) and
  `league_games.tsv` (`verA`/`verB`) — all the literal string `None`. Nothing here is
  stratified through them. Our own `ourver` in `ladder_games.tsv` **is** populated and was
  used only to identify the drifting match, not to stratify.
- **`match info --json` returns the opponent's version as `null`** — re-confirmed on both
  legs today (CLI trap 3). Leg B's opponent version (Ouroboros **v8**) comes from
  `match list --json`, which carries it.
- The five maps of the two legs were **not** the PREREG's five primary maps: they cover
  lighthouse, atoll and eider, plus saga and nordkap. **drumlin and hive were not played**,
  so two of the five pre-registered primary maps have no probe evidence at all.
- Turn counts are the platform's `turnsPlayed`; the *kill round* for a `core_destroyed` game
  is taken to be that value. No replay was decoded for this document.
