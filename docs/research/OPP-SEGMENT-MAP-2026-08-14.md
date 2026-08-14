# OPPONENT × MAP-SEGMENT MAP — current era (ourver ≥ 125), read 2026-08-14

**Read time (UTC, `date -u`): 2026-08-14T15:42:41Z.** Source:
`corpus/ladder_games.tsv` (4,860 raw data rows). **Era bound: `ourver` ≥ 125**
→ **430 games, 86 matches, 22 distinct opponents**, spanning
`created` 2026-08-13T10:32:59Z → 2026-08-14T14:52:59Z (~28h). Versions actually
present in the era: 125 (305 games), 134 (15), 135 (5), 137 (15), 139 (40),
140 (45), 142 (5) — v125 dominates the sample by volume; treat cells that are
mostly v125 as describing v125 more than the era as a whole.

**Dedup: performed, found nothing to remove.** Checked the full 4,860-row file
under three independent keys — (a) exact full-row equality, (b) `(match, map)`,
(c) the lenient key `(match, opp, map, winner_seat, cond, turns)` ignoring
`created`/ratings/replay-path — and all three return **0 duplicate rows**, era
or full-file. The task brief's note of "~41 duplicate rows" does not match
today's file: 25 rows do have an **empty replay-path column** (`cond=error`,
`turns=0` — genuine errored games, not duplicates; e.g. match
`74d30f5c…` has three such rows, one per map, all distinct), which may be what
an earlier pass over a different file snapshot flagged. Reported here rather
than silently assumed away, per the standing instrument-verification rule —
if a stale duplicate set turns up elsewhere it is not in this TSV today.

**Segments** (fixed by brief): **TINY** {fjordgate 100, antler 252} · **S400**
{auroraveil, frostgate, icefloe, royale, yulerune, all 400} · **MID** {atoll,
drumlin, heart, hive, meander, nordkap, saga, snowflake, archipelago, 500-676}
· **BIG900** {drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie, 900}. All
15 maps that appear in the era rows classify cleanly; no unclassified map
observed.

**Map win rate in era, for reference** (worst → best; confirms the brief's
worst-map list is in fact the bottom five): antler 36.7% (n=30) · midgard
38.2% (n=34) · fjordgate 38.5% (n=26) · ragnarok 42.4% (n=33) · frostgate
44.0% (n=25) · nordkap 44.8% · royale 48.0% · auroraveil 50.0% · drakkarfjord
52.4% · icefloe 52.9% · drumlin 54.2% · archipelago 58.3% · yulerune 72.2% ·
glacierkeep 73.3% · valkyrie 77.8%.

---

## 1. Opponent × area-class table (era-bounded, ourver ≥ 125)

Our win share per cell; `n<5` marked **THIN**, no share printed under `n<3`.
Opponents sorted by total era games, descending.

| Opponent | TINY | S400 | MID | BIG900 | Era total |
|---|---|---|---|---|---|
| Juusto | n=4 25.0% THIN | n=12 58.3% | n=8 50.0% | n=16 56.2% | n=40 52.5% |
| Erebus | n=5 0.0% | n=16 62.5% | n=5 60.0% | n=14 50.0% | n=40 50.0% |
| LingLing40 | n=3 33.3% THIN | n=8 37.5% | n=11 9.1% | n=13 69.2% | n=35 40.0% |
| Jython | n=6 66.7% | n=11 27.3% | n=10 80.0% | n=8 50.0% | n=35 54.3% |
| team lazy | n=2 THIN(n<3) | n=7 100.0% | n=8 87.5% | n=18 61.1% | n=35 74.3% |
| arsonist duck | n=4 100.0% THIN | n=11 63.6% | n=6 66.7% | n=9 88.9% | n=30 76.7% |
| Big O | n=5 40.0% | n=9 88.9% | n=8 37.5% | n=8 62.5% | n=30 60.0% |
| diverge | n=5 20.0% | n=11 90.9% | n=4 75.0% THIN | n=10 30.0% | n=30 56.7% |
| 0033 | n=7 28.6% | n=11 18.2% | n=2 THIN(n<3) | n=10 20.0% | n=30 23.3% |
| HTTP 418 | n=1 THIN(n<3) | n=8 50.0% | n=8 50.0% | n=8 25.0% | n=25 40.0% |
| Coreflood | n=2 THIN(n<3) | n=7 71.4% | n=4 75.0% THIN | n=7 71.4% | n=20 75.0% |
| kladde chatte tville (och oss) | n=4 0.0% THIN | n=5 40.0% | n=2 THIN(n<3) | n=4 75.0% THIN | n=15 40.0% |
| Leviathan | n=3 0.0% THIN | n=4 50.0% THIN | n=1 THIN(n<3) | n=2 THIN(n<3) | n=10 30.0% |
| Powered by SmartFridge | — | n=2 THIN(n<3) | n=4 50.0% THIN | n=4 75.0% THIN | n=10 70.0% |
| The Bisons | n=2 THIN(n<3) | n=3 33.3% THIN | n=4 50.0% THIN | n=1 THIN(n<3) | n=10 40.0% |
| Focalground | — | n=2 THIN(n<3) | n=1 THIN(n<3) | n=2 THIN(n<3) | n=5 80.0% |
| farming_200s | — | n=3 0.0% THIN | n=1 THIN(n<3) | n=1 THIN(n<3) | n=5 20.0% |
| The Flotte Experience | — | n=3 0.0% THIN | n=1 THIN(n<3) | n=1 THIN(n<3) | n=5 0.0% |
| Pantheon | — | n=3 0.0% THIN | — | n=2 THIN(n<3) | n=5 40.0% |
| Askar City | n=1 THIN(n<3) | n=1 THIN(n<3) | — | n=3 66.7% THIN | n=5 80.0% |
| lingling_40h | n=1 THIN(n<3) | n=2 THIN(n<3) | n=1 THIN(n<3) | n=1 THIN(n<3) | n=5 40.0% |
| Landers | n=1 THIN(n<3) | n=1 THIN(n<3) | — | n=3 66.7% THIN | n=5 60.0% |
| **Class totals** | **n=56, 37.5%** | **n=140, 55.0%** | **n=89, 52.8%** | **n=145, 55.9%** | **n=430, 52.6%** |

TINY is the weak class overall (37.5% vs 51-56% elsewhere) — consistent with
it being the worst map bucket by construction (antler + fjordgate are two of
the five worst maps individually).

---

## 2 & 3. Worst-map focus — per-opponent losses and attribution

For each of {antler, midgard, fjordgate, ragnarok, frostgate}: opponents we
**lost** to on that specific map this era, games and our wins against them
there, then the concentration read (top-2-by-losses share of that map's total
losses; **≥60% from ≤2 teams ⇒ OPPONENT-CONCENTRATED, else TERRAIN-GENERAL**).

### antler (n=30, we won 11, lost 19)

| Opponent | games | our wins | our losses |
|---|---|---|---|
| 0033 | 5 | 2 | 3 |
| kladde chatte tville (och oss) | 3 | 0 | 3 |
| Erebus | 3 | 0 | 3 |
| diverge | 2 | 0 | 2 |
| LingLing40 | 2 | 0 | 2 |
| Leviathan | 1 | 0 | 1 |
| Juusto | 2 | 1 | 1 |
| HTTP 418 | 1 | 0 | 1 |
| Big O | 1 | 0 | 1 |
| Jython | 3 | 2 | 1 |
| Landers | 1 | 0 | 1 |

Top-2 (0033 + kladde/Erebus tie at 3 each) = 6/19 = **31.6%**.
**⇒ TERRAIN-GENERAL (n=19 losses, 11 distinct opponents contributing).**

### midgard (n=34, we won 13, lost 21)

| Opponent | games | our wins | our losses |
|---|---|---|---|
| Erebus | 5 | 0 | 5 |
| diverge | 3 | 0 | 3 |
| Juusto | 2 | 0 | 2 |
| 0033 | 3 | 1 | 2 |
| team lazy | 2 | 0 | 2 |
| Big O | 2 | 0 | 2 |
| Coreflood | 3 | 2 | 1 |
| Jython | 2 | 1 | 1 |
| HTTP 418 | 2 | 1 | 1 |
| Askar City | 1 | 0 | 1 |
| Landers | 1 | 0 | 1 |

Top-2 (Erebus + diverge) = 8/21 = **38.1%**.
**⇒ TERRAIN-GENERAL (n=21 losses, 10 distinct opponents contributing).**

### fjordgate (n=26, we won 10, lost 16)

| Opponent | games | our wins | our losses |
|---|---|---|---|
| Leviathan | 2 | 0 | 2 |
| Big O | 4 | 2 | 2 |
| Juusto | 2 | 0 | 2 |
| Erebus | 2 | 0 | 2 |
| 0033 | 2 | 0 | 2 |
| diverge | 3 | 1 | 2 |
| Jython | 3 | 2 | 1 |
| kladde chatte tville (och oss) | 1 | 0 | 1 |
| team lazy | 1 | 0 | 1 |
| The Bisons | 2 | 1 | 1 |

Top-2 (any two of the six tied at 2) = 4/16 = **25.0%**.
**⇒ TERRAIN-GENERAL (n=16 losses, 10 distinct opponents contributing — the flattest of the five).**

### ragnarok (n=33, we won 14, lost 19)

| Opponent | games | our wins | our losses |
|---|---|---|---|
| 0033 | 4 | 0 | 4 |
| Juusto | 5 | 2 | 3 |
| LingLing40 | 2 | 0 | 2 |
| team lazy | 5 | 3 | 2 |
| Erebus | 3 | 1 | 2 |
| Jython | 2 | 0 | 2 |
| HTTP 418 | 2 | 1 | 1 |
| The Flotte Experience | 1 | 0 | 1 |
| The Bisons | 1 | 0 | 1 |
| Coreflood | 1 | 0 | 1 |

Top-2 (0033 + Juusto) = 7/19 = **36.8%**.
**⇒ TERRAIN-GENERAL (n=19 losses, 10 distinct opponents contributing).**

### frostgate (n=25, we won 11, lost 14)

| Opponent | games | our wins | our losses |
|---|---|---|---|
| 0033 | 3 | 0 | 3 |
| Leviathan | 2 | 0 | 2 |
| LingLing40 | 3 | 1 | 2 |
| Juusto | 2 | 1 | 1 |
| arsonist duck | 1 | 0 | 1 |
| The Flotte Experience | 1 | 0 | 1 |
| HTTP 418 | 1 | 0 | 1 |
| Pantheon | 1 | 0 | 1 |
| Big O | 1 | 0 | 1 |
| Coreflood | 1 | 0 | 1 |

Top-2 (0033 + LingLing40) = 5/14 = **35.7%**.
**⇒ TERRAIN-GENERAL (n=14 losses, 9 distinct opponents contributing).**

### Reading across all five

**All five worst maps read TERRAIN-GENERAL — none reaches the 60% concentration
bar** (range 25.0%–38.1%, no single opponent contributes more than 5 losses to
any one map). Losses on these five maps are not a "we lose to team X on map Y"
story; they spread across 9-11 distinct opponents per map. The one recurring
name is **0033**, present in the loss table on all five worst maps (and
overall our weakest matchup at 23.3% era-wide, n=30) — it raises every map's
loss count somewhat but at 2-5 losses per map it never approaches the
concentration bar on its own. This points toward a **terrain/build weakness on
these five maps that generalizes across the field**, not a specific
opponent-counter problem, though the samples are modest (14-21 losses per map)
and a single map's picture could still flip with more games.

---

## 4. Strongest opponent per area class (n≥5 only, sorted by our win share ascending)

Candidates for segment-pinned live legs (`fcode match unrated <team> --match <id>`,
pinned per opponent-pinning spec) or books, since these are where the class is
worst for us specifically:

| Class | Strongest-vs-us opponent | n | our wins | our share | Runner-up (n≥5) |
|---|---|---|---|---|---|
| **TINY** | Erebus | 5 | 0 | **0.0%** | diverge (n=5, 20.0%) |
| **S400** | 0033 | 11 | 2 | **18.2%** | Jython (n=11, 27.3%) |
| **MID** | LingLing40 | 11 | 1 | **9.1%** | Big O (n=8, 37.5%) |
| **BIG900** | 0033 | 10 | 2 | **20.0%** | HTTP 418 (n=8, 25.0%) |

**0033 anchors two of four classes** (S400, BIG900) at n≥10 each and is also
the weakest matchup overall (23.3% era-wide, n=30 — the single worst
opponent-total row in section 1). **LingLing40 on MID (9.1%, n=11)** is the
single worst class cell in the whole table at n≥5. **Erebus on TINY (0.0%,
n=5)** is a clean sweep against us but on the smallest sample of the four —
worth a confirming leg before weighting it as strongly as the other three.

---

**Files:** none beyond this doc; source is `corpus/ladder_games.tsv` (untracked
raw file, compressed copy is what's committed) plus the fixed map→area-class
table given in the task brief. No commit made per instructions.
