# Cardinal vs. diagonal core-pair split — our own games, 2026-08-07

**Corpus:** the local `replay_archive/` as of 2026-08-07 evening. Our team is
OpenSverige (team ID `379a5d80-9921-4c9e-949b-f9b1dcba16be`), currently live on
v67 (`wave_ghost`). Every per-game row below is tagged with the version
actually stamped in that match's `.meta.json` (`teamAVersion`/`teamBVersion`
for whichever seat we held) — not with "current version" — so v64 rows are a
snapshot of the bot as it was when that match was played, not a claim about
today's build.

**Method:** replicates the axis-split analysis in
`docs/research/sporks-decode-2026-08-07.md` §1.5/§7.2, applied to our own
matches instead of sporks'. Script: scratchpad `axis_split.py`, run via
`.venv/bin/python`, parsing with `tools/replay_census.py`'s `Replay` class
(`track_flow=False`).

## Classification rule applied

Taken **verbatim** from the sporks doc: a core pair is **cardinal** if
`dx == 0 or dy == 0`, else **diagonal**, where `(dx, dy)` is the difference
between the two cores' NW-corner positions (`Replay.cores`, same field the
sporks decode's own toolkit reads). This is the doc's literal rule, not the
task brief's fallback fuzzy version (`dx <= 2` etc.) — the doc's own rule
turned out to be usable as stated: sampled across 15 games ahead of this
analysis, `dx` and `dy` land on an exact 0 or a large nonzero value in every
case (maps are reflection-symmetric → one axis literally matches; rotation-
symmetric → neither does), so no fuzz margin was needed.

Seat/version mapping (which replay "team 0/1" is which meta.json team) was
verified empirically before trusting it: across all 96 local matches, summing
per-game replay winners with `team==0` reproduces `scoreA` and `team==1`
reproduces `scoreB` with **zero mismatches**. So replay team 0 = that match's
`teamA`, team 1 = `teamB`, consistently for a whole series.

## What's actually in the archive for us

Only **two** of the 96 local matches involve OpenSverige at all:

| match id | our seat | our version | opponent | opp version | score (A-B) | type |
|---|---|---|---|---|---|---|
| `bab61537` | B | v64 | Ouroboros | v8 | 5-0 (we lost 0) | unrated |
| `b7c0ea11` | B | v67 (`wave_ghost`) | Powered by SmartFridge | v34 | 3-2 (we won 2) | unrated |

That's **10 games total** across 2 five-game series. Both are unrated test
matches, not ladder games — the archiver evidently has not kept our recent
ladder history locally, only these two scouting/sparring series.

## Per-version × axis table

| version | axis | W | L | win% | n | median rounds |
|---|---|---|---|---|---|---|
| v64 | cardinal | 0 | 2 | 0.0% | 2 | 285 |
| v64 | diagonal | 0 | 3 | 0.0% | 3 | 313 |
| v67 | cardinal | 2 | 0 | 100.0% | 2 | 468 |
| v67 | diagonal | 0 | 3 | 0.0% | 3 | 70 |

Per-version totals (both axes):

| version | record | win% |
|---|---|---|
| v64 | 0W-5L | 0.0% |
| v67 | 2W-3L | 40.0% |

**v65 and v66 are not present in the local archive at all** — no rows for
either, so no split can be computed for them here.

## Overall split (irrespective of version)

| axis | W | L | win% | n | median rounds |
|---|---|---|---|---|---|
| cardinal | 2 | 2 | 50.0% | 4 | 402 |
| diagonal | 0 | 6 | 0.0% | 6 | 273 |

Total across both matches: **2W-8L** (n=10). Every one of our diagonal games
in this tiny sample is a loss, matching the *direction* of the sporks
finding, but on a sample far too small to call a rule (see caveats).

## Comparison to the sporks decode

From `docs/research/sporks-decode-2026-08-07.md` §1.5, sporks' own 25-game
record, same classification rule:

> | map geometry | sporks record |
> |---|---|
> | cores offset on a **cardinal** axis (dx==0 or dy==0) | **9W-0L** |
> | cores offset **diagonally** | **6W-10L** |

And the doc's own caveat on that number (§8), which applies with even more
force to our numbers below:

> The 9W-0L cardinal split rests on 9 games; the direction of the effect is
> unambiguous but the magnitude is one sample's worth. Cardinal maps in this
> sample are also the low-separation ones (12.0 and below except `c96904fa`
> g5), so **axis and separation are confounded** and this decode cannot
> separate them.

Side by side:

| | cardinal | diagonal |
|---|---|---|
| sporks (25 games, 5 opponents) | 9W-0L (100%) | 6W-10L (37.5%) |
| us, all versions (10 games, 2 opponents) | 2W-2L (50%) | 0W-6L (0%) |
| us, v67 only (5 games, 1 opponent) | 2W-0L (100%) | 0W-3L (0%) |

Our diagonal record (0W-6L, and 0W-3L within v67 alone) is at least as stark
as sporks' diagonal weakness. Our cardinal record is much noisier — v64 is
0W-2L cardinal, v67 is 2W-0L cardinal — which given the sample is
indistinguishable from "cardinal games happened to go the version's way,"
not evidence of a cardinal-specific strength the way sporks shows one.

## Caveats

- **Sample size is the dominant problem.** This is 2 matches / 10 games /
  1-2 opponents, against sporks' 25 games / 5 opponents. Every cell in the
  per-version table above has n=2 or n=3 — a single flipped game changes a
  cell's win rate by 33-50 points. Treat every number in this doc as
  anecdotal, not as a validated finding, until the local archive holds more
  of our own matches.
- **Version, opponent, and map rotation are fully confounded here.** The
  entire v64 sample is one series vs. Ouroboros v8; the entire v67 sample is
  one series vs. Powered by SmartFridge v34. Any apparent v64-vs-v67
  difference could equally be "Ouroboros counters us" or "that day's five
  maps happened to favor/disfavor us" — there is no way to separate version
  effect from opponent effect or map-draw effect with two single-opponent
  series.
- **The archive is not a uniform or representative sample of our play.** It
  is dominated by opponent-vs-opponent scouting matches (94 of 96 local
  matches don't involve us at all); the archiver favors recent pulls and
  matches judged useful for research, not a systematic log of our own ladder
  record. These two series are both unrated test matches, not ladder games,
  so this doc says nothing about our rated win rate by axis.

## v2 re-run (session 14, corpus n=22/110)

**Corpus growth.** The local archive grew from 96 to **144** total matches
since v1. Matches involving OpenSverige grew from 2 to **22**, all with
complete 5-game series (110 games total, zero missing games, zero replay
parse failures) — a much larger jump than the "~13 matches" estimated in the
task brief that triggered this re-run. Versions represented: **v64, v67,
v68**. **v65 and v66 are still entirely absent from the local archive** —
same gap as v1. Unlike v1 (2/2 unrated scouting matches), this corpus mixes
**12 ladder-triggered matches** (`triggeredBy: "ladder"`, `eloDeltaA/B`
populated) and **10 unrated** matches — the first time this analysis line has
any rated-ladder data.

**Method reused verbatim** from v1: a core pair is cardinal iff `dx == 0 or
dy == 0` on `Replay.cores` NW-corner positions, diagonal otherwise; replay
"team 0"/"team 1" mapped to that match's `teamA`/`teamB`. The seat-mapping
assumption was **re-verified from scratch** on the full grown 144-match
archive (not just carried over from v1's 96-match check): summing per-game
replay winners by `team==0`/`team==1` reproduces every match's `scoreA`/
`scoreB` exactly, **144/144, zero mismatches, zero parse failures**. Script:
this session's scratchpad `axis_split.py`, recovered from a prior session's
scratchpad (v1's original) and extended with Wilson 95% CIs (formula ported
verbatim from `tools/arena.py`'s `wilson()`), run via `.venv/bin/python`. A
spot-check against raw replay fields (e.g. `03e63d07…_game_1`: cores at
`(6,4)`/`(6,12)`, `dx=0` → cardinal, `winner=1` → seat-A loss) confirms the
classifier and win attribution agree with the source data.

### Per-version x axis (with Wilson 95% CI)

| version | axis | W | L | win% | n | Wilson 95% CI | median rounds |
|---|---|---|---|---|---|---|---|
| v64 | cardinal | 0 | 2 | 0.0% | 2 | [0.0%, 65.8%] | 285 |
| v64 | diagonal | 0 | 3 | 0.0% | 3 | [0.0%, 56.2%] | 313 |
| v67 | cardinal | 11 | 8 | 57.9% | 19 | [36.3%, 76.9%] | 258 |
| v67 | diagonal | 7 | 24 | 22.6% | 31 | [11.4%, 39.8%] | 279 |
| v68 | cardinal | 4 | 11 | 26.7% | 15 | [10.9%, 52.0%] | 300 |
| v68 | diagonal | 16 | 24 | 40.0% | 40 | [26.3%, 55.4%] | 250 |

### Per-version totals (both axes)

| version | record | win% | Wilson 95% CI |
|---|---|---|---|
| v64 | 0W-5L | 0.0% | [0.0%, 43.4%] |
| v67 | 18W-32L | 36.0% | [24.1%, 49.9%] |
| v68 | 20W-35L | 36.4% | [24.9%, 49.6%] |

### Overall split (irrespective of version)

| axis | W | L | win% | n | Wilson 95% CI | median rounds |
|---|---|---|---|---|---|---|
| cardinal | 15 | 21 | 41.7% | 36 | [27.1%, 57.8%] | 280 |
| diagonal | 23 | 51 | 31.1% | 74 | [21.7%, 42.3%] | 277 |

Total across all 22 matches: **38W-72L** (n=110), Wilson 95% CI
[26.3%, 43.8%].

### Comparison to the sporks decode and to the v1 (2-match) result

| | cardinal | diagonal |
|---|---|---|
| sporks (25 games, 5 opponents) | 9W-0L, 100% CI [70.1%, 100%] | 6W-10L, 37.5% CI [18.5%, 61.4%] |
| us v1 (2 matches, 10 games) | 2W-2L, 50% | 0W-6L, 0% |
| us v2, all versions (22 matches, 110 games) | 15W-21L, 41.7% CI [27.1%, 57.8%] | 23W-51L, 31.1% CI [21.7%, 42.3%] |
| us v2, v67 only (10 matches, 50 games) | 11W-8L, 57.9% CI [36.3%, 76.9%] | 7W-24L, 22.6% CI [11.4%, 39.8%] |
| us v2, v68 only (11 matches, 55 games) | 4W-11L, 26.7% CI [10.9%, 52.0%] | 16W-24L, 40.0% CI [26.3%, 55.4%] |

Sporks' own cardinal/diagonal CIs don't overlap at all (70.1% floor clears
the 61.4% diagonal ceiling) — that is what "unambiguous direction" looks
like on this test. None of our cuts clear that bar:

- **Overall (n=110):** CIs overlap substantially — [27.1%, 57.8%] vs.
  [21.7%, 42.3%], a 15-point overlap band.
- **v67 alone (n=50):** the closest we get to the sporks signal — CIs overlap
  only narrowly, [36.3%, 76.9%] vs. [11.4%, 39.8%], a 3.5-point overlap band
  at 36.3–39.8%. Direction matches sporks (cardinal > diagonal) but the
  overlap means it does not clear a standard non-overlapping-CI bar on its
  own.
- **v68 alone (n=55): direction reverses.** Cardinal (26.7%) is now *worse*
  than diagonal (40.0%) — the opposite of both sporks and our own v67. CIs
  overlap heavily here too, so this isn't a confirmed reversal either, just
  a data point that flatly contradicts the "diagonal is bad for us" framing.

### What changed since v1

- v1's headline observation — "every one of our diagonal games in this tiny
  sample is a loss" (0W-6L) — **does not survive the larger sample**:
  diagonal win rate is now 31.1% (23W-51L). That 0% figure was a 6-game
  artifact of an underpowered draw, exactly as v1's own caveats warned.
- v67's split (58% cardinal vs. 23% diagonal, n=50) is the strongest
  same-direction evidence we have for a sporks-like effect, now spread across
  10 opponents instead of 1 — but the CIs still touch, so it is suggestive,
  not confirmed. v67 was live when v1 was written; v68 (`x3r0 "chokewall"`)
  is live now and shows the opposite pattern, with CIs that comfortably
  contain the null.
- The corpus is no longer all-unrated (12/22 ladder, 10/22 unrated), a first
  for this analysis line — the axis split itself was not re-cut by rated
  status in this pass (out of scope here; worth a follow-up if the split
  ever looks strong enough to act on).

### Caveats

- Sample size improved by an order of magnitude (2→22 matches, 10→110 games)
  but is still well below sporks' 25-game/5-opponent reference, and
  per-version-per-axis cells (n=2 to n=40) still produce wide CIs — the v64
  cells (n=2, n=3) are unchanged from v1 and remain uninformative.
- Version/opponent/map confounding is reduced (v67 now spans 10 opponents,
  v68 spans 11, vs. 1 opponent each in v1) but not eliminated: no opponent is
  repeated across enough games on both axes to separate "this version is
  diagonally weak" from "this version drew tougher diagonal opponents."
- v65 and v66 remain entirely absent from the local archive; no split is
  possible for either.

### Verdict

**Still underpowered, and now direction-inconsistent across our own
versions — not claimable.** v67 leans the sporks direction (cardinal >
diagonal) but the CI overlap is too narrow to call significant on its own;
v68 flips the sign entirely, and the overall pooled cut has a wide CI overlap
too. Combined with v1's now-refuted "0% diagonal" headline, the honest read
is that we do not have evidence our team should treat core-pair axis as
actionable the way sporks' numbers suggest sporks should — more data, ideally
with repeated opponents split across both axes per version, is needed before
acting on this.

## v3 re-run (overnight session, rated-only cut, corpus n=37/185)

**Date:** 2026-08-07 (overnight). **Corpus growth.** The local archive grew
again since v2: OpenSverige matches went from **22 to 37** (as the task brief
anticipated), all with complete 5-game series — **185 games total, zero
missing games**. Versions represented are unchanged: **v64, v67, v68** (v65
and v66 remain entirely absent from the local archive — same gap as v1/v2).
v67's sub-corpus is **unchanged from v2** (still exactly 10 matches / 50
games — v67 is retired and no new matches for it are appearing); all of the
growth is in **v68** (11 → 26 matches, 55 → 130 games) plus one untouched v64
match.

**Method reused verbatim** from v1/v2: cardinal iff `dx == 0 or dy == 0` on
`Replay.cores` NW-corner positions (exact 0/nonzero, no fuzz — reconfirmed on
this corpus, no ambiguous cases), diagonal otherwise; replay `team 0`/`team 1`
mapped to that match's `teamA`/`teamB`. Script: fresh minimal parser written
this session in scratchpad `axis_split_v3.py`, importing `Replay` directly
from `tools/replay_census.py` (`track_flow=False`) and `wilson()` ported
verbatim from `tools/arena.py`, same formula v2 used. **Zero parse failures,
zero exclusions** across all 185 games. Seat mapping was **re-verified from
scratch** on this corpus: per-match replay-summed winners (`team==0` count,
`team==1` count) reproduce `scoreA`/`scoreB` exactly for **all 37 matches,
zero mismatches**. Spot-check: `01e4679f…_game_1`, cores at `dx=13, dy=13` →
diagonal, consistent with the raw `Replay.cores` fields.

**New cut for this pass:** every match's `.meta.json` carries `triggeredBy`
(`"ladder"` = rated, `"unrated"` = scouting/sparring). Of the 37 matches, **25
are ladder-triggered and 12 are unrated** — v64 is 100% unrated (1 match),
v67 is 6 ladder / 4 unrated, v68 is 19 ladder / 7 unrated (**19 matches / 95
games**, matching the task brief's estimate exactly). This section re-cuts
the axis split by rated status to test v2's suspicion that v68's sign flip
was an unrated-opponent-strength artifact.

### Per-version x axis, RATED-ONLY (primary cut)

| version | axis | W | L | win% | n | Wilson 95% CI | median rounds |
|---|---|---|---|---|---|---|---|
| v64 | — | — | — | — | 0 | no rated v64 matches in archive | — |
| v67 | cardinal | 7 | 5 | 58.3% | 12 | [32.0%, 80.7%] | 237 |
| v67 | diagonal | 5 | 13 | 27.8% | 18 | [12.5%, 50.9%] | 487 |
| v68 | cardinal | 17 | 17 | 50.0% | 34 | [34.1%, 65.9%] | 375.5 |
| v68 | diagonal | 26 | 35 | 42.6% | 61 | [31.0%, 55.1%] | 230 |

### Per-version totals, RATED-ONLY

| version | record | win% | Wilson 95% CI |
|---|---|---|---|
| v67 | 12W-18L | 40.0% | [24.6%, 57.7%] |
| v68 | 43W-52L | 45.3% | [35.6%, 55.3%] |

### Pooled all-version, RATED-ONLY x axis

| axis | W | L | win% | n | Wilson 95% CI | median rounds |
|---|---|---|---|---|---|---|
| cardinal | 24 | 22 | 52.2% | 46 | [38.1%, 65.9%] | 347.5 |
| diagonal | 31 | 48 | 39.2% | 79 | [29.2%, 50.3%] | 269 |

Rated-only total across all versions: **55W-70L** (n=125), Wilson 95% CI
[35.6%, 52.8%].

### Comparison to v2 — does the v68 sign flip survive?

| | cardinal | diagonal |
|---|---|---|
| sporks (25 games, 5 opponents) | 9W-0L, 100% CI [70.1%, 100%] | 6W-10L, 37.5% CI [18.5%, 61.4%] |
| v2, v67 only, all types (10 matches, 50 games) | 11W-8L, 57.9% CI [36.3%, 76.9%] | 7W-24L, 22.6% CI [11.4%, 39.8%] |
| v2, v68 only, all types (11 matches, 55 games) | 4W-11L, 26.7% CI [10.9%, 52.0%] | 16W-24L, 40.0% CI [26.3%, 55.4%] |
| **v3, v67 only, RATED-ONLY (6 matches, 30 games)** | 7W-5L, 58.3% CI [32.0%, 80.7%] | 5W-13L, 27.8% CI [12.5%, 50.9%] |
| **v3, v68 only, RATED-ONLY (19 matches, 95 games)** | 17W-17L, 50.0% CI [34.1%, 65.9%] | 26W-35L, 42.6% CI [31.0%, 55.1%] |
| v3, v68 only, UNRATED-ONLY (7 matches, 35 games) | 1W-13L, 7.1% CI [1.3%, 31.5%] | 8W-13L, 38.1% CI [20.8%, 59.1%] |
| v3, all versions, RATED-ONLY (25 matches, 125 games) | 24W-22L, 52.2% CI [38.1%, 65.9%] | 31W-48L, 39.2% CI [29.2%, 50.3%] |

**The v68 sign flip does not survive excluding unrated matches.** In v2's
mixed (rated+unrated) v68 cut, diagonal (40.0%) beat cardinal (26.7%) — the
finding v2 flagged as possibly confounded. In the rated-only cut, v68's
cardinal win rate is **50.0%**, now *above* diagonal's 42.6% — same
direction as v67 and sporks, not reversed. The gap is narrow and the CIs
overlap almost completely, so this is not a confirmed cardinal advantage
either, but the flat contradiction v2 reported is gone once unrated games are
excluded.

**The confound v2 suspected is directly confirmed by opponent ratings.**
Pulling `teamARating`/`teamBRating` from the meta.json of v68's unrated
matches: the 7 unrated opponents average **1813 Elo** (median 1936) versus
the 19 rated opponents' average of **1570 Elo** (median 1573) — a ~250-point
gap. Four of those unrated opponents are well above any rated opponent we've
faced at v68: Pivot (1953), "not adgato" (1953), Jython (1936), and **sporks
itself (2039)**. Those four matches (20 games) went **0W-16L** overall, and
within them cardinal fared worse than diagonal: **0W-9L on cardinal** (Pivot
1 game, Jython 3, sporks 2, not adgato 3 — all losses) versus **3W-8L on
diagonal** (2 wins from Pivot, 1 from Jython). The v68 unrated-only split
overall is stark: cardinal cratered to **7.1%** (1W-13L, n=14) while diagonal
held at 38.1% (8W-13L, n=21) — that lopsided cardinal collapse against
elite-rated scouting opponents is what was dragging v2's combined v68
cardinal number down to 26.7%, not a genuine cardinal weakness in rated play.

Per-match detail for the v68 unrated-cardinal cluster (7 matches, 14 games,
1W-13L):

| match | opponent | opp rating | our rating | cardinal games | wins |
|---|---|---|---|---|---|
| `01e4679f` | gsxWins | 1642 | 1568 | 2 | 1 |
| `12afd14a` | gsxWins | 1665 | 1559 | 1 | 0 |
| `3eda3021` | I Stone | 1506 | 1559 | 2 | 0 |
| `799cc587` | Pivot | 1953 | 1589 | 1 | 0 |
| `877eb868` | Jython | 1936 | 1589 | 3 | 0 |
| `a05472b6` | sporks | 2039 | 1589 | 2 | 0 |
| `b0d7bba8` | not adgato | 1953 | 1589 | 3 | 0 |

Only two of the seven opponents (gsxWins, I Stone) are within normal ladder
range of us; the other five are 300-450 Elo above us and account for 9 of the
14 cardinal games and all but one loss.

### Secondary: v67 rated-only and pooled rated-only

- **v67 rated-only (6 matches, 30 games)** looks essentially identical in
  direction and magnitude to v2's all-type v67 cut (58.3%/27.8% here vs.
  57.9%/22.6% in v2) — unsurprising since 6 of v67's 10 total matches were
  already ladder, and the 4 unrated ones don't shift the picture much. This
  is still the closest we get to the sporks signal: CIs [32.0%, 80.7%]
  (cardinal) and [12.5%, 50.9%] (diagonal) overlap from 32.0% to 50.9%, an
  18.9-point band — direction matches sporks but does not clear a
  non-overlap bar.
- **Pooled all-version, rated-only (25 matches, 125 games):** cardinal
  52.2% CI [38.1%, 65.9%] vs. diagonal 39.2% CI [29.2%, 50.3%]. Direction now
  matches sporks and both individual versions (v67, v68) for the first time
  in this analysis line — v2's pooled all-type cut had the two overlapping
  in a way that included v68's contradictory sign; with unrated excluded,
  every rated cut (v67 alone, v68 alone, pooled) now points the same
  direction. CIs still overlap heavily (38.1-50.3%, a 12.2-point band), so
  this remains **suggestive, not significant**.

### Caveats

- **CIs still overlap in every cut.** Excluding unrated matches fixes the
  sign *inconsistency* between v67 and v68, but does not produce a
  statistically clean split anywhere — every rated-only CI pair overlaps by
  double digits. This is directionally consistent now, not proven.
- **Rated corpus per axis-cell is still modest.** v67 rated cells are n=12
  and n=18; even v68's larger rated cells (n=34, n=61) are well short of
  sporks' 25-game/5-opponent reference taken as a whole cut, though v68
  alone now has 12 distinct rated opponents (up from effectively unmeasured
  in v1) — opponent diversity within the rated cut is reasonable.
  v64 has **zero** rated matches in the archive at all, so no rated split is
  possible for it (its one match is unrated and excluded from every table in
  this section except the "for comparison" line).
- **Excluding unrated data doesn't fully remove confounding within the rated
  cut either.** Version, opponent, and map are still not orthogonal to axis
  within the rated-only games — no single opponent is repeated enough times
  split across both axes within one version to isolate a pure axis effect
  from an opponent-matchup effect.
- **This does not mean unrated data is "bad" data, only that it is a biased
  sample for this particular cut.** The unrated matches are disproportionately
  scouting/sparring games the archiver picked against strong opponents (four
  of seven v68 unrated opponents rated 300+ points above us) — appropriate
  for their original purpose, but they inflate variance and bias the pooled
  all-type split whenever axis happens to correlate with which opponents
  showed up in that bucket, exactly as v2 warned.
- v65 and v66 remain entirely absent from the local archive; no split is
  possible for either, in any cut.

### Verdict

**The v68 sign flip does not survive the rated-only cut — it was the unrated
burst v2 suspected.** Once unrated matches are excluded, v68 rated-only shows
cardinal (50.0%, n=34) slightly ahead of diagonal (42.6%, n=61), matching the
direction of v67 rated-only (58.3% vs. 27.8%, n=12/18) and the pooled
rated-only split (52.2% vs. 39.2%, n=46/79) — all now pointing the same way
as sporks' finding for the first time in this analysis line. But **every one
of these CIs still overlaps substantially** (12-19 point overlap bands), so
this is a consistent *direction*, not a *significant* one: still not
something to bake into Thor-layer map-choice logic as a hard rule. The
actionable takeaway is narrower than "prefer cardinal maps" — it's that the
sign-flip anomaly v2 flagged as likely-confounded **was** confounded, our own
rated data no longer contradicts the sporks-style cardinal-favored direction,
and a future re-run with a larger rated-only corpus (particularly more v68
opponent diversity on the cardinal axis) is the next useful step before this
could graduate to "claimable."
