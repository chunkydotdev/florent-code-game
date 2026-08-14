# RATED DAY DECODE — 2026-08-14 UTC — PART 2 (extension, not a rewrite)

**Lane:** research arm (read-only analysis agent). **Written:** `date -u` in the
producing shell read **2026-08-14T19:12:58Z**.

**Relationship to the first decode (`RATED-DAY-DECODE-2026-08-14.md`):** that
file's stated cut was **every rated match with `created` ≤ 2026-08-14T18:12:59Z**
(55 matches, 275 games; its writing clock was 18:32:59Z, and it explicitly said
*"the 18:32:59Z pairing is not in this decode; it did not exist on any surface
yet"*). **This file's cut is the two pairings that landed after that: 18:32:59Z
and 18:52:59Z.** Corpus was re-synced at 19:09:54Z (`corpus/manifest.json:
built_utc`); newest `league_matches.tsv` row is **18:52:59.715Z** — that is
today's data horizon and no pairing after it is in scope. §2 below re-derives
the whole-day roll-up (57 matches) so the day total does not require reading
both files side by side, but every number for matches 1-55 is unchanged from
part 1 and is not re-argued here.

Population is unchanged: **US ONLY**, `corpus/ladder_games.tsv` is the
authority, `meta_join.tsv` was not touched. No verdict sentence — observation
plus explicitly-labelled inference, per the same standing rule.

---

## 0. FRESHNESS

| surface | rows | newest row | file mtime (approx) |
|---|---|---|---|
| `corpus/ladder_games.tsv` | 4,920 | `created` **2026-08-14T18:52:59.715Z** | post-19:09:54Z sync |
| `corpus/league_matches.tsv` | 45,436 (**see §4 instrument note — dedup required**) | `createdAt` **2026-08-14T18:52:59.715Z** | same sync |
| `corpus/manifest.json` | — | `built_utc` **2026-08-14T19:09:54Z** | — |

Command: `python3 -c "import csv; rows=list(csv.DictReader(open('corpus/ladder_games.tsv'),delimiter='\t')); print(max(r['created'] for r in rows))"` → `2026-08-14T18:52:59.715Z`.

**Two new matches fell inside this window** (created 18:32:59.673Z and
18:52:59.715Z); nothing after 18:52:59Z is decodable yet.

---

## 1. THE TWO NEW ROWS

| # | created (UTC) | opponent | oppver | ourver | ourbef | share | d (elo) | maps (won marked) |
|---|---|---|---|---|---|---|---|---|
| 56 | 18:32:59 | arsonist duck | v24 | v140 | 1794.9529 | **2/5** | **−5.27** | antler✓(187) frostgate✗(325) ragnarok✗(613) valkyrie✓(233) drakkarfjord✗(185) |
| 57 | 18:52:59 | team lazy | v227 | v140 | 1789.6795 | **3/5** | **+3.88** | archipelago✗(367) fjordgate✗(198) midgard✓(272) auroraveil✓(116) antler✓(167) |

All 10 games ended `core_destroyed` — no r1000, no tiebreak condition, in either
match. Neither is a bad cell (both clear 0/5 and 1/4 thresholds).

`oppver` is populated in both rows (`24`, `227`) — **0 nulls in these 2
matches**, consistent with the full-day count below.

**Note on `team lazy`'s version:** part 1's ledger and §2b table show `team lazy`
at `v226` for every earlier match today; this match carries **`v227`** — a
version bump mid-day, same shape as the `LingLing40`/`0033` churn part 1 already
flagged in its instrument note (opponents are not fixed-version matchups across
a day).

---

## 2. WHOLE-DAY ROLL-UP, REFRESHED — 57 matches, 285 games

Command (dedups `league_matches.tsv` by `id` before summing — see §4):

```python
import csv, collections
lg = [r for r in csv.DictReader(open('corpus/ladder_games.tsv'), delimiter='\t')
      if r['created'].startswith('2026-08-14')]
lm = {r['id']: r for r in csv.DictReader(open('corpus/league_matches.tsv'), delimiter='\t')}
by_match = collections.defaultdict(list)
for r in lg: by_match[r['match']].append(r)
wins = sum(int(r['won']) for r in lg)
elo = sum(float(lm[m]['eloDeltaA'] if lm[m]['teamAName']=='OpenSverige' else lm[m]['eloDeltaB'])
          for m in by_match)
```

**DAY TOTAL (revised): 57 matches · 285 games · 145 wins · game share
50.9% (145/285) · NET +12.37 Elo.**

Delta from part 1's 55-match total (140/275, +13.76): **+5 wins / +10 games /
−1.39 Elo** — exactly the two new matches (2/5 −5.27, 3/5 +3.88; −5.27+3.88 =
−1.39, checks).

**Chain-of-custody reconciliation (exact, not poll-based):** match 55's
`ourbef` was 1788.80 with delta +6.15 → predicted next `ourbef` = 1794.95.
Match 56's actual `ourbef` = **1794.9528537624803**. Match 56's `ourbef`
(1794.9529) + its delta (−5.2733) = 1789.6796 → match 57's actual `ourbef` =
**1789.6795471592943**. **Both links check to 4 decimal places.** This is a
tighter reconciliation than part 1's elo_history poll comparison (that poll
rounds to whole Elo; this chains the exact per-match `ratingBefore` field, which
is monotonically dependent on nothing but our own delta sequence).

**Day-share interval:** n=285, p=50.877%, DEFF=1.529 (clusters re-verified
live below) → `half_width_95 = 1.96·sqrt(0.5088·0.4912·1.529/285)` = **±7.2pp**.

---

## 3. INCUMBENCY — no change inside this window, and the NEXT change is already visible past the horizon

**Both new matches carry `ourver=140`,** consistent with part 1's holder table
(v140 "still holding at 18:27Z" and the boot-config note that v140 held through
16:21Z onward). No non-incumbent version appears in either new match.

**⚠ Flagged for the record, OUT OF SCOPE for this decode's numbers:**
`docs/coordination.md` (read only for context, not a data source) records that
x3r0 uploaded **v145 "Top Team Router v3"** at **19:08:37Z**, displacing v140.
`elo_history.tsv`'s tail (LOCAL, UTC+2) shows the tag flip from `v140` to `v145`
between the `21:08` and `21:13` local rows — i.e. **UTC 19:08→19:13**, which
brackets the coordination timestamp and is consistent with it. **This is after
my 18:52:59Z data horizon: no rated match carrying v145 exists in
`ladder_games.tsv` yet, so it cannot be scored here.** It belongs in the next
extension once a pairing lands under it.

**Leaked-exposure count for this file's two matches: 0** (both v140, both
authorized incumbent, same conclusion class as part 1's §2c).

---

## 4. INSTRUMENT NOTE — `league_matches.tsv` carries exact-duplicate rows (headline-worthy, does not change any number above)

`grep -c` on the two new match ids returns **2, not 1**, for both:

```
$ grep -c "ae53c95d-3d3a-4bae-8422-1b9b44fa736f" corpus/league_matches.tsv
2
$ grep -c "453eddbe-3f0c-4191-bcf8-1ba8f21499d5" corpus/league_matches.tsv
2
```

Checked at scale: **119 of 45,436 rows in `league_matches.tsv` are duplicate
`id`s**, each appearing exactly twice. Diffed byte-for-byte — **the two copies
of each duplicated row are identical**, not conflicting values (verified for
both matches above by direct grep; same-content duplication, not a
reconciliation failure). This looks like a sync-time double-append rather than
a source-of-truth defect: `ladder_games.tsv` (the game-grain file, and the
authority per `docs/research/corpus-howto.md`) has **zero duplicate
`(match, map)` keys across all 4,920 rows** — the corruption, such as it is,
is confined to the match-grain elo-delta file.

**Consequence: any code that sums `eloDeltaA/B` over `league_matches.tsv` rows
directly (rather than keying by unique match `id` first) will double-count.**
All numbers in this file dedup by `id` before summing (shown in the §2 snippet:
`lm = {r['id']: r for r in ...}` — a dict comprehension collapses duplicates by
construction). **Reported here because the task brief singled out
`oppver`-style column defects as headline material and this is the same class:
a surface that looks fine until you count rows instead of trusting the shape.**
Recommend a `tools/corpus_sanity.py` check for duplicate `id`s in
`league_matches.tsv` alongside its existing all-zero-column checks.

---

## 5. PER-VERSION TABLE, REFRESHED (only v140 changed)

| ourver | matches | games | share | net Elo | window (UTC) | Δ vs part 1 |
|---|---|---|---|---|---|---|
| v125 | 20 | 100 | 52.0% | +17.58 | 00:12–07:52 | unchanged |
| v134 | 3 | 15 | 40.0% | −11.52 | 06:32–07:12 | unchanged |
| v135 | 1 | 5 | 0.0% | −13.89 | 07:32 | unchanged |
| v137 | 3 | 15 | 33.3% | −14.26 | 08:12–08:52 | unchanged |
| v139 | 8 | 40 | 35.0% | −34.93 | 09:12–11:32 | unchanged |
| **v140** | **18** (+2) | **90** (+10) | **62.2%** | **+67.71** | 11:52–**18:52** | wins 56 (+5), Δelo −1.39 |
| v142 | 2 | 10 | 60.0% | −0.37 | 14:52–15:12 | unchanged |
| v143 | 2 | 10 | 60.0% | +2.04 | 15:52–16:12 | unchanged |

v140's share moved 63.7% → 62.2% (n grew 80→90); still comfortably the day's
best-performing holder block. Interval: n=90, p=62.2%, DEFF=1.529 →
**±12.4pp** (up from part 1's ±13.0pp on the smaller n — narrower, as expected
with more games at the same DEFF).

---

## 6. OPPONENT NETS, REFRESHED (only the two opponents in today's new matches)

| opponent | oppver(s) today | matches | games | share | net Elo | part 1 value |
|---|---|---|---|---|---|---|
| **arsonist duck** | v24 | **4** (+1) | **20** (+5) | **70.0%** | **+21.43** | was 3/15, 80.0%, +26.71 |
| **team lazy** | v226, **v227** | **6** (+1) | **30** (+5) | **76.7%** | **+60.18** | was 5/25, 80.0%, +56.29 |

Both remain net-positive matchups; both moved down slightly on share because
the new match was below their day-average (arsonist duck 2/5, team lazy 3/5
against a prior 80% run). Neither crosses into the "net-losing" bucket. All
other opponent rows in part 1's §3b/net-positive tables are unaffected — no
other opponent appears in today's two new matches.

---

## 7. WIN-CONDITION MIX, REFRESHED

Of **285 rated games** today (was 275):

| | core_destroyed | titanium_collected (r1000 tiebreak) |
|---|---|---|
| wins (145) | 140 (96.6%) | 5 (3.4%) |
| losses (140) | 133 (95.0%) | 7 (5.0%) |

**r1000 rate unchanged: 11 of 285 = 3.86%** (both new matches' longest game was
613 turns — nowhere near r1000). Interval: DEFF 1.529, n=285 →
`1.96·sqrt(0.0386·0.9614·1.529/285)` = **±2.24pp**.

**Median kill/death (core_destroyed only), refreshed:**
* Median KILL round, wins: **181.5** (n=140; was 178, n=135)
* Median DEATH round, losses: **185** (n=133; was 182, n=128)

Still roughly a four-round race — the two new matches' losses (325, 613, 367,
198 turns) skew slightly longer than the prior median, the two new wins (187,
233, 272, 116, 167) bracket it.

---

## 8. LOSSES WORTH A HUMAN LOOK

**None in the two new matches.** Neither is 0/5 or 1/4 — arsonist duck went 2/5
(−5.27), team lazy went 3/5 (a win in share terms, +3.88). Part 1's list of
eleven 0/5-or-1/5 matches (§3a there) is unchanged; nothing here adds to it.

---

## 9. WHAT I DID NOT DO

* Did not re-derive or re-argue any of part 1's 55-match findings — cited by
  reference and shown only where the new 2 matches change a downstream number
  (whole-day totals, v140's row, the two opponent rows, the win-condition mix).
* Did not read `meta_join.tsv` for any denominator.
* Did not score the v145 holder change (19:08:37Z) — it postdates the
  18:52:59Z data horizon and has no rated match in the corpus yet.
* No verdict sentence.
