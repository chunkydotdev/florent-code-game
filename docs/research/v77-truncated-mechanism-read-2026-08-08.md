# v77 "Eir 9" (`bots/_v89sh`) — truncated wild mechanism read

**Research-arm decode, 2026-08-08.** REV-6 pre-registration checks 1-3 only
(mechanism/case-metric field test). **Class-Elo scoring (checks 4+) is
explicitly OUT OF SCOPE — n=5 matches is noise; folds into any future
v77-content window.** No games run, no bot files touched, no downloads (all
4 matches were already archived).

**Version-stamp:** v77 = `bots/_v89sh`, md5 `e12f85855654e9e78227582d0dc15d4b`
(prefix `e12f8585` — confirmed against the working tree). Window: 5 matches,
truncated by x3r0's v78 swap-in at 14:05 local / 12:05:00Z (out-of-rule swap,
v77's rolling last-5 stood at +20 net when swapped over — see
`docs/coordination.md` 14:09 note). Archive state at read time: **4 of 5
matches archived** (20 games); the 5th (~+10 net, per the builder's WAKE
note) had not landed in `replay_archive/` as of this read.

**Tooling note:** the method this read follows — per-round harvester wiring
state, per-round belt-adjacency situation detection, full-hop-path stack
ownership tracking for mechanism classification, deny-arm action detection —
is the one documented in `docs/research/ad-flips-margin-decode-2026-08-08.md`
Appendix C and `docs/research/eir8-production-read-2026-08-08.md` §8.2. The
scripts those docs cite (`scratchpad/ad_flips`, `scratchpad/lh_misroute`,
`scratchpad/sh_accounting`) lived in a prior session's ephemeral scratchpad
and are gone from disk; this read is a **fresh implementation of the same
documented method**, built directly on `tools/replay_census.py`'s validated
wire-level parsing primitives. Script: `analyze.py`, run from this session's
scratchpad (`v77_trunc/`); output persisted alongside it as `raw_games.json`.

---

## Verdict

| arm | wild signal | vs. cited baseline |
|---|---|---|
| **Case metric (enemy-banked rate)** | **7.17% pooled (618/8,615)** — *worse* than baseline headline, but mechanism-share and the priority (Ouroboros) case both moved the right direction | v75 wild: **4.33%**. Pooled rate is up, not down — see caveats below |
| **Wire arm (unwired harvester-rounds)** | **56.9%** (directed-wired-complement, the definition that actually produced the cited 40.4%) / **77.7%** (simple zero-adjacent-acceptor definition) | v74 24.3% → v75 **40.4%** (the regression). **Both v77 readings sit above 40.4% — the wire arm did not fire; the regression got worse, not better** |
| **Deny arm** | **ACTIVE — yes.** 66 attacks (132 Ti), fired only in the 2 of 4 matches with real belt-adjacency exposure, zero in the 2 with none (clean gating) | no prior wild baseline (new mechanism) |

**One-line verdict: the deny arm fired and fired selectively, with a strong
positive signal on the one game set that mattered most (Ouroboros: 18.16% →
8.21%, more than halved, even in a 0-5 loss) — but the wire-queue arm shows
no improvement in the wild, consistent with (and now reproducing at wild
scale) the local corpus's own negative finding in
`ad-flips-margin-decode-2026-08-08.md` §C.4. The pooled case-metric headline
going UP (4.33% → 7.17%) is real but is carried by 0033, a HANDOFF-dominated
leak the deny arm was never built to fix — not by a failure of the arm on
its own target mechanism, whose share of the leak fell from 79.7% to 30.7%.**

---

## 0. Corpus and validation

| match | opponent (their ver.) | score | createdAt→completedAt (UTC) |
|---|---|---|---|
| `eb59c8bb` | Askar City (73) | **5-0** | 11:12:43 → 11:20:48 |
| `83b0fd6d` | 0033 (43) | **2-3** | 11:22:43 → 11:26:41 |
| `d694094e` | Ouroboros (8) | **0-5** | 11:32:43 → 11:38:41 |
| `37e4f4ee` | Banminary (41) | **4-1** | 11:42:43 → 11:45:34 |

All 4 stamped `teamVersion=77` for OpenSverige in `*.meta.json`, all inside
the 11:20-11:45Z window from the task brief, all `triggeredBy: ladder`. Seats
taken from meta (`teamAName`/`teamBName`), not assumed: OpenSverige is seat A
for Askar City and 0033, seat B for Ouroboros and Banminary. **20/20 replay26
files present**, no exclusions.

**Self-check 1 — delivery identity** (`core_deliv × 10 == titaniumCollected`,
per team-side, per `replay_schema.md`): **40/40 exact**, both sides, all 20
games. Zero mismatches.

**Self-check 2 — seat/winner reproduction**: per-game winners decoded from
the replay's `winner` field, independently tallied per match and compared to
`scoreA`/`scoreB` in the match meta: **4/4 matches reproduce exactly**
(5-0, 2-3, 0-5, 4-1), **20/20 games** consistent with the tallied score. This
also cross-validates the seat assignment used for every downstream metric.

---

## 1. Check 1 — enemy-banked rate (case metric)

Every stack is followed individually via `DistributeResources.resourceId`
from its origin harvester to wherever it banks (either core), exactly as
`eir8-production-read-2026-08-08.md` §8.1 does. "Leaked" = stacks we mined
that ended up banked in the **enemy** core.

### Ouroboros first (priority game set)

| | v75 wild baseline | **v77 (this match)** |
|---|---:|---:|
| our mined stacks vs Ouroboros | ~5,771 (implied by 1,048/18.16%) | **5,251** |
| **enemy-banked** | **1,048 (18.16%)** | **431 (8.21%)** |
| games with a leak | 4/5 | **3/5** (games 1-3; games 4-5 zero) |

**Answer to the priority question: yes — the drain roughly halved (18.16% →
8.21%) even though this window's Ouroboros match was a 0-5 loss.** Per-game:
g1 2.04% (14/686), g2 20.04% (390/1,946, the one bad game — carries 90.5% of
this match's leak), g3 2.55% (27/1,059), g4/g5 0.00%. Same concentration
pattern the eir8 doc warns about (§8.1: "concentrated, not diffuse") — one
game (g2) is doing almost all of the damage, same as v75's worst-game
pattern there.

**Mechanism split on what leaks remain** (per the eir8 §8.2 method — full
hop-path ownership, originating harvester hop excluded):

| mechanism | Ouroboros stacks | share |
|---|---:|---:|
| HANDOFF (our belt partway, then their belt) | 247 | 57.3% |
| ADJACENCY SIPHON (harvester outputs straight onto their belt) | 184 | 42.7% |
| DIRECT MISROUTE / SINGLE-HOP-DIRECT | 0 | 0.0% |

No wild v75 Ouroboros-specific mechanism split exists to compare against
(only the volume figure, §8.4) — this table is new information. Deny fired
32 times against Ouroboros (9 in g1, 3 in g2, 20 in g3; 0 in g4/g5, where
nothing leaked), all 32 on-target (0 false-positive-looking) — see §3.

### All 4 matches, pooled and per-match

| match | mined | leaked | rate | mechanism (SIPHON / HANDOFF / MISROUTE) |
|---|---:|---:|---:|---|
| Askar City | 840 | 0 | 0.00% | — (no leak arose) |
| 0033 | 2,069 | 187 | **9.04%** | 6 / 181 / 0 |
| **Ouroboros** | **5,251** | **431** | **8.21%** | 184 / 247 / 0 |
| Banminary | 455 | 0 | 0.00% | — (no leak arose) |
| **POOLED** | **8,615** | **618** | **7.17%** | **190 (30.7%) / 428 (69.3%) / 0** |

vs. **v75 wild rated: 4.33% (1,856/42,826)**, mechanism 79.7% SIPHON / 13.6%
HANDOFF / 6.7% MISROUTE.

**Reading this honestly, both directions:**
- The pooled rate is *up*, not down (4.33% → 7.17%) — the deny arm's ship
  case does not show as a clean pooled-rate win at this n.
- The mechanism the arm actually targets (ADJACENCY_SIPHON — a builder
  attack on an enemy belt tile orthogonally adjacent to our harvester) fell
  from 79.7% to 30.7% of the leak's composition. **The pooled headline is
  now carried by HANDOFF (69.3%, up from 13.6%)** — multi-hop drift onto
  enemy belt after partial travel on ours — a mechanism the deny arm was
  never built to address (it only acts on belt tiles directly adjacent to a
  harvester, not on relay tiles further downstream).
- 0033 alone (187 leaked, 96.9% of it HANDOFF: 181/187) is doing most of the
  pooled damage — one of 0033's games (`_game_4`, 669 rounds) leaked 147
  stacks (21.91% of that game's mined volume) with **zero deny events fired**
  that game, meaning the exposure never presented as adjacency-siphon
  geometry for the arm to act on.
- n=4 matches (2 with any leak at all) is not enough to separate "the arm
  underperforms on HANDOFF-shaped leaks" from "0033 is a harder matchup" —
  flagged, not resolved, here.

---

## 2. Check 2 — unwired harvester-rounds (wire arm)

**Definitional note, flagged up front:** the task brief's phrasing
("harvester-rounds with zero friendly orthogonal acceptors") and its cited
baselines (v74 24.3%, v75 40.4%) come from **two different metrics in two
different docs**, and they disagree by an order of magnitude on the local
corpus where both were measured side by side:

- **Metric A — "zero friendly orthogonal acceptor"** (harvester alive × has
  ≥1 friendly conveyor/splitter immediately adjacent): this is the literal
  definition stated in the brief, and it is exactly what
  `ad-flips-margin-decode-2026-08-08.md` §C.4 measures on the **local**
  hsd/sh corpus — where it reads **3.21% / 4.69%**, nowhere near 40.4%.
- **Metric B — "directed-wired" complement** (full facing-respecting chain
  from harvester through friendly relays to the Core, OR direct orthogonal
  adjacency to the Core footprint — same definition as
  `replay_census.py`'s `chains()`/`directed` column): this is what actually
  produces the cited **24.3% (v74) / 40.4% (v75)** figures in
  `eir8-production-read-2026-08-08.md` §8.3.

Both are computed below so the number that's actually comparable to the
cited baseline is on the record, alongside the number the brief's wording
literally asked for.

| match | harvester-rounds | **A: zero-adjacent-acceptor unwired** | **B: directed-wired-complement unwired** |
|---|---:|---:|---:|
| Askar City | 3,774 | 1,678 (44.5%) | 564 (14.9%) |
| 0033 | 13,531 | 10,559 (78.0%) | 6,338 (46.8%) |
| Ouroboros | 51,639 | 41,465 (80.3%) | 32,495 (62.9%) |
| Banminary | 3,295 | 2,429 (73.7%) | 1,708 (51.8%) |
| **POOLED** | **72,239** | **56,131 (77.7%)** | **41,105 (56.9%)** |

vs. baselines: metric A local comparators **hsd 3.21% / sh (`_v89sh`
predecessor tag) 4.69%**; metric B wild comparators **v74 24.3% / v75
40.4%**.

**On either definition, v77 is worse, not better.** Metric B — the one
that's actually apples-to-apples with the cited 40.4% — reads **56.9%
pooled, ~16.5 points above the v75 regression it was supposed to fix.**
Ouroboros alone (the longest-running match, 5×~1000-round-scale games) is
the heaviest driver at 62.9%. This is not a contradiction of the local read;
it's a **reproduction of it**: `ad-flips-margin-decode-2026-08-08.md` §C.4
already found, on a controlled local corpus, "the wire-queue arm shows no
measurable reduction in unwired time on this corpus — if anything, sh runs a
higher unwired-rounds share and a higher never-wired-harvester share than
hsd." The wild read agrees.

**Time-to-first-wire distribution** (pooled, rounds from harvester build to
its first round with a friendly orthogonal acceptor, metric A):

| n (harvesters that ever wired) | mean | median | p90 | max |
|---:|---:|---:|---:|---:|
| 124 | 23.14 | **2.0** | 11.8 | 901 |

Median/p90 (2 / 12 rounds) look fine and are consistent with the local
corpus's near-identical 2 / 4 finding — **when a harvester does get wired, it
tends to get wired fast.** The gap is the tail: mean (23.14) is pulled far
above the median by a long right tail (max 901 rounds — a harvester that sat
unwired almost an entire 1000-round tiebreak game), and:

**Never-wired harvesters: 34 / 158 built (21.5%)** — over a fifth of every
harvester built in this window never once had a friendly orthogonal
conveyor/splitter for its entire life (destroyed first, or the game ended
first). Ouroboros alone accounts for 18 of the 34 (its long tiebreak games
give unwired harvesters more rounds to matter, and more chances to never
catch up). This is the sharper story than the aggregate rate: **the wire
arm's failure mode in the wild is concentrated in a tail of harvesters that
never get wired at all**, not a uniform small delay across every harvester.

---

## 3. Check 3 — deny-arm field behavior

Deny event = a builder-controlled `BuilderAttack` (2 Ti/action, per
CLAUDE.md) whose target tile holds an **enemy** conveyor or splitter that is
orthogonally adjacent to one of **our** harvesters at the time of the
attack — the deny trigger's literal geometry. Attacks on enemy belt tiles
*not* adjacent to one of our harvesters are logged separately as
false-positive-looking.

| match | deny events | distinct targets | distinct rounds | Ti spent | false-positive-looking | belt-adjacent exposure (harvester-rounds) |
|---|---:|---:|---:|---:|---:|---:|
| Askar City | 0 | 0 | 0 | 0 | 0 | 0 |
| 0033 | 34 | 2 | 33 | 68 | **125** | 184 |
| Ouroboros | 32 | 6 | 32 | 64 | 0 | 1,409 |
| Banminary | 0 | 0 | 0 | 0 | **38** | 94 |
| **TOTAL** | **66** | **8** | **65** | **132** | **163** | **1,687** |

**The arm is well-gated:** it fired zero times in the two matches (Askar
City, Banminary) where the belt-adjacency exposure census (component (a)
from the ad-flips §C.2 method) reads zero-to-near-zero — it is not attacking
speculatively when there is nothing to deny. Where exposure was real
(0033, Ouroboros), it fired at a rate of roughly one attack per exposed
target-round-cluster (8 distinct targets total across both matches, close
to one attack cadence per emergent belt-adjacency situation rather than a
frantic per-round spam), consistent with the cooldown-gated, one-action-
per-turn builder economy.

**The 163 false-positive-looking events are concentrated entirely in the two
matches with zero on-target denies** (125 in 0033, 38 in Banminary) — i.e.
they never co-occur with real deny activity in the same match in this
corpus. Read with the caveat the task itself flags ("should be ~baseline"):
these are attacks on enemy belt tiles that are *not* near one of our
harvesters, which could be ordinary siege/economic-harassment builder
behavior unrelated to the deny-specific worker, not necessarily a
miscalibration of the deny arm itself — this read cannot distinguish "the
deny logic fired on the wrong geometry" from "a *different*, non-deny
builder-attack behavior is doing this," and does not attempt to.

**Payback estimate.** Ti spent denying: **132**. Stacks lost via the exact
mechanism the arm targets (ADJACENCY_SIPHON) despite its activity: **190
stacks = 1,900 Ti**, i.e. realized loss on the targeted mechanism is ~14×
the spend on defense — **this is not a clean payback win by direct
before/after volume**, and should not be read as one. The honest framing,
per the same caution `eir8-production-read-2026-08-08.md` §8.5 applies to
its own leak-correlation claim: this corpus has no matched control (no v77
game against Ouroboros/0033 with the deny arm disabled) to isolate what the
190 stacks would have been *without* the arm firing — only the local
hsd-vs-sh comparison in `ad-flips-margin-decode-2026-08-08.md` §C.3 has
that structure, and it found a real (if smaller-than-headline, ~7×) ADJACENCY
SIPHON-specific reduction there. What this wild read *can* say: the arm
fired selectively on real exposure, its target mechanism's *share* of the
wild leak fell by more than half (79.7% → 30.7%), and the Ouroboros
match-level rate (the single largest, most-priced leak class per the eir8
doc) more than halved even in a loss. **Whether that nets positive against
132 Ti of attack spend is not established by this read and should not be
asserted as a payback win** — it is a plausibility signal, not a measured
ROI.

---

## 4. Pending 5th match

The builder's WAKE note logged a 5th v77 match at ≈+10 net that had not yet
landed in `replay_archive/` as of this read (archiver runs on a ~30-min
cycle). Not included above. If it archives before this window closes, it
should fold into the pooled tables (mechanism split, wiring rates, deny
census) as a fifth row — the per-match structure above is built so that's a
mechanical append, not a re-decode.

## 5. Deferred scope (explicit)

**Class-Elo scoring (checks 4+ of the rev-6 pre-registration) is
out of scope for this read.** n=5 matches (and effectively n=4 archived) is
below any threshold where a class-level Elo claim would be more than noise —
this was the scope call research made explicitly under delegation
(`docs/coordination.md`, 14:10 note) when the truncated window closed. Any
v77-attributable Elo signal folds into a future window with more matches on
this exact code (contingent on whether/when the slot returns to v77-lineage
content, per the swap-rule question already routed to Magnus).

## 6. Self-checks

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected` | **40/40 team-sides**, 0 mismatches |
| **Seat/winner reproduction** — decoded per-game winner tally vs meta `scoreA`/`scoreB` | **4/4 matches, 20/20 games exact** (5-0, 2-3, 0-5, 4-1) |
| **Corpus completeness** | 4/4 archived matches read, 20/20 replay26 files present, 0 excluded |
| **Stack accounting** | every leaked stack followed hop-by-hop via `resourceId`, per the eir8 §8.2 method; mechanism classified on full path (origin hop excluded) |
| **Version stamp** | `bots/_v89sh` md5 `e12f85855654e9e78227582d0dc15d4b` matches the working tree and the coordination-log ship note prefix `e12f8585` |
| **Games excluded** | zero |

### Bounded and unexplained

1. **The metric-A/metric-B disagreement in the task brief itself** (§2) —
   the brief's own wording and its own cited baseline describe two different
   measurements. Both are reported; metric B is the one actually comparable
   to "24.3% / 40.4%." Not resolved here which one the next rev's
   pre-registration should standardize on — flagged for the builder/Magnus.
2. **False-positive-looking deny events (163) are not classified further** —
   this read cannot tell ordinary builder-attack behavior apart from a
   genuinely miscalibrated deny trigger without reading the `_v89sh` source
   directly (out of scope for a replay-only read). Bound: 163 events, 8
   distinct targets, entirely confined to 2 of 4 matches.
3. **Payback estimate is explicitly not a validated causal number** (§3) —
   no matched control exists in the wild corpus; the local hsd-vs-sh
   comparison in the ad-flips doc is the only place that structure exists,
   and it is cited, not re-derived, here.
4. **Ti-cost assumption**: deny Ti spent (132) uses the flat 2 Ti/attack
   figure from CLAUDE.md; not independently re-derived from a titanium-delta
   ledger on the attacking builders (would require tracking each builder's
   global-pool contribution, out of scope for this read).

---

## Addendum — 2026-08-08 16:2x: matches 5-6 fold-in (922b5da8 CAD v107, 208e84f8 Memtrace v33)

**Version stamp, unchanged content.** Ladder-live version is now **v80 "Eir
9b"** — byte-identical v77 content (`bots/_v89sh`, md5
`e12f85855654e9e78227582d0dc15d4b`, prefix `e12f8585`, reconfirmed against
the working tree at fold-in time). Both matches below are stamped
`teamAVersion=77` for OpenSverige in their `*.meta.json` — they are v77-code
reads, folded into the v77 window per §4's stated mechanical-append plan; the
v80 relabel is an accounting event only (no bot bytes changed between v77 and
v80). Archive files read: `replay_archive/922b5da8-9d0d-456b-8bd9-501cb9f3355a_game_[1-5].replay26`
+ `.meta.json`; `replay_archive/208e84f8-584c-4450-aedc-e85eb5ac5198_game_[1-5].replay26`
+ `.meta.json`. Tooling: fresh implementation of the same method (per-round
harvester wiring state, per-round belt-adjacency exposure, full-hop-path
stack ownership for mechanism classification, deny-arm action detection),
built on `tools/replay_census.py`'s wire-level primitives, run from this
session's scratchpad. One parser bug caught and fixed in-session before any
numbers were trusted: `Entity.team` is proto3 implicit-presence — `TEAM_A`
(field value 0) is omitted from the wire, so a naive parser that defaults an
unset team field to `None` instead of `0` silently drops every friendly
(team-A) entity from ownership lookups. Fixed by defaulting `team = 0`
before scanning fields, matching `tools/replay_census.py`'s own
`parse_entity` convention (`eid = team = hp = max_hp = 0`) — flagged here
because it is a trap for the next fresh implementation too.

### Corrected window facts

**6 matches, +34.14 net Elo** (exact per-match `eloDeltaA`/`eloDeltaB` from
each `*.meta.json`, oriented to OpenSverige's seat):

| match | opponent (ver.) | seat | score | our eloDelta |
|---|---|---|---:|---:|
| `eb59c8bb` | Askar City (73) | A | 5-0 | +14.29477 |
| `83b0fd6d` | 0033 (43) | A | 2-3 | −1.91797 |
| `d694094e` | Ouroboros (8) | B | 0-5 | −15.17216 |
| `37e4f4ee` | Banminary (41) | B | 4-1 | +13.01515 |
| `922b5da8` | **CtrlAltDefeat (107)** | A | **4-1** | **+10.03226** |
| `208e84f8` | **Memtrace (33)** | A | **5-0** | **+13.89224** |
| **SUM** | | | | **+34.14429** |

Matches the task brief's stated +34.14 figure to 2dp — cross-validates the
seat assignments used below (both new matches: OpenSverige seat A, per
`teamAName` in each meta, matching the task brief).

### Self-checks — matches 5-6

**Self-check 1 — delivery identity** (`core_deliv × 10 == titaniumCollected`,
per team-side, per `replay_schema.md`): **20/20 exact** (2 matches × 5 games
× 2 sides), zero mismatches. Combined with the original 40/40: **60/60
exact across the full 6-match window.**

**Self-check 2 — seat/winner reproduction**: CAD v107 decoded per-game
winners A,A,A,A,B → tallies to 4-1, matching `scoreA=4/scoreB=1` exactly.
Memtrace v33 decoded A,A,A,A,A → tallies to 5-0, matching `scoreA=5/scoreB=0`
exactly. **2/2 new matches reproduce exactly, 10/10 new games consistent.**
Combined with the original 20/20: **30/30 games across the full window.**

No self-check anomalies. Proceeding.

### §1 fold-in — enemy-banked leak accounting

| match | mined | leaked | rate | mechanism (SIPHON / HANDOFF / MISROUTE) |
|---|---:|---:|---:|---|
| CtrlAltDefeat v107 | 3,491 | 32 | **0.92%** | 32 (100%) / 0 / 0 |
| Memtrace v33 | 5,467 | 0 | **0.00%** | — (no leak arose) |

CAD's 32 leaked stacks are concentrated entirely in `_game_4`
(the only one of its 5 games with any leak) — **100% ADJACENCY_SIPHON**,
zero HANDOFF, zero MISROUTE. This is the same target mechanism the deny arm
is built to address, and it's the one match where the deny arm actually
fired (see below).

**UPDATED POOLED — 6 matches / 30 games** (original four's row values pulled
from the doc's own §1 table above, not re-decoded):

| match | mined | leaked | rate | mechanism (SIPHON / HANDOFF / MISROUTE) |
|---|---:|---:|---:|---|
| Askar City | 840 | 0 | 0.00% | — |
| 0033 | 2,069 | 187 | 9.04% | 6 / 181 / 0 |
| Ouroboros | 5,251 | 431 | 8.21% | 184 / 247 / 0 |
| Banminary | 455 | 0 | 0.00% | — |
| CtrlAltDefeat v107 | 3,491 | 32 | 0.92% | 32 / 0 / 0 |
| Memtrace v33 | 5,467 | 0 | 0.00% | — |
| **POOLED (6)** | **17,573** | **650** | **3.70%** | **222 (34.2%) / 428 (65.8%) / 0** |

**This is the headline number that moves.** The 4-match pooled rate was
7.17% — read in the base doc as "worse, not better" than the v75 wild
baseline of 4.33%. The 6-match pooled rate is **3.70%**, now *below* the
4.33% baseline it was being compared against. Mechanism share shifts too:
SIPHON's share of the (smaller, relatively) leaked pool rises from 30.7% to
34.2%, HANDOFF's falls from 69.3% to 65.8% — still HANDOFF-dominated, but
less so. **Both new matches added zero HANDOFF volume** (CAD's leak is
100% SIPHON, Memtrace leaked nothing at all) — the pooled rate drop is
entirely a denominator effect (8,958 more mined stacks, only 32 more leaked)
plus a numerator effect specific to these two opponents not reproducing
0033's HANDOFF-heavy exposure geometry. n=2 additional matches is still too
few to call this a trend rather than "two opponents that happened not to
create HANDOFF-shaped exposure" — flagged, not resolved.

### §2 fold-in — unwired-harvester-rounds (wire arm)

| match | harvester-rounds | **A: zero-adjacent-acceptor unwired** | **B: directed-wired-complement unwired** |
|---|---:|---:|---:|
| CtrlAltDefeat v107 | 22,422 | 1,402 (6.25%) | 8,977 (40.04%) |
| Memtrace v33 | 39,419 | 355 (0.90%) | 11,603 (29.44%) |

Both new matches read **far lower** on both metrics than any of the original
four (which ranged 44.5-80.3% on metric A, 14.9-62.9% on metric B). Neither
CAD nor Memtrace comes close to Ouroboros's 80.3%/62.9% — plausibly shorter
games (CAD g1/g3 = 275/103 rounds; Memtrace g3/g5 = 83/110 rounds; only 2 of
the 10 new games ran the full 1000-round tiebreak, versus Ouroboros's 5/5)
giving harvesters proportionally less time to drift unwired, not necessarily
a wire-arm behavior change. Flagged, not asserted as causal.

**UPDATED POOLED — 6 matches / 30 games:**

| match | harvester-rounds | **A: zero-adjacent-acceptor unwired** | **B: directed-wired-complement unwired** |
|---|---:|---:|---:|
| Askar City | 3,774 | 1,678 (44.5%) | 564 (14.9%) |
| 0033 | 13,531 | 10,559 (78.0%) | 6,338 (46.8%) |
| Ouroboros | 51,639 | 41,465 (80.3%) | 32,495 (62.9%) |
| Banminary | 3,295 | 2,429 (73.7%) | 1,708 (51.8%) |
| CtrlAltDefeat v107 | 22,422 | 1,402 (6.25%) | 8,977 (40.04%) |
| Memtrace v33 | 39,419 | 355 (0.90%) | 11,603 (29.44%) |
| **POOLED (6)** | **134,080** | **57,888 (43.17%)** | **61,685 (46.01%)** |

**Big pooled drop on both metrics** (A: 77.7% → 43.17%; B: 56.9% → 46.01%),
driven almost entirely by the two new matches' much lower rates, which in
turn are plausibly driven by shorter average game length rather than a wire
arm behavior change (see caveat above — this fold-in did not re-examine
per-game length weighting). **Metric B — the one actually comparable to the
cited v75 baseline (40.4%)** — is now only **+5.6 points above it** (was
+16.5 points at n=4). Still above the baseline, so the base doc's directional
claim ("the wire arm did not fire; the regression got worse, not better")
is **not reversed**, but the margin has shrunk by roughly two-thirds. This
is not yet "the wire arm works" — it is "the pooled gap to the thing it was
supposed to fix narrowed a lot with two shorter, lower-exposure games added,"
which is a different and much weaker claim.

### §3 fold-in — deny-arm census

| match | deny events | distinct targets | distinct rounds | Ti spent | false-positive-looking | belt-adjacent exposure (harvester-rounds) |
|---|---:|---:|---:|---:|---:|---:|
| CtrlAltDefeat v107 | 135 | 1 | 122 | 270 | 601 | 1,007 |
| Memtrace v33 | 9 | 1 | 9 | 18 | 225 | 15 |

Both matches reproduce the base doc's clean-gating pattern: deny volume
scales with belt-adjacency exposure, not with game length or opponent
identity in general. CAD (1,007 exposure harvester-rounds, all concentrated
in `_game_4`) drew 135 deny events, **all 135 against the same single target
tile** (`(10, 8)`) across 122 distinct rounds — read as sustained
re-attack/re-destruction cycling on one recurring enemy conveyor, not a
scattered response. Memtrace (15 exposure harvester-rounds, `_game_1` only)
drew a proportionally small 9 events, also at 1 distinct target. Neither
match shows deny firing with zero exposure present — the "well-gated" claim
holds on both.

**UPDATED POOLED — 6 matches / 30 games:**

| match | deny events | distinct targets | distinct rounds | Ti spent | false-positive-looking | belt-adjacent exposure (harvester-rounds) |
|---|---:|---:|---:|---:|---:|---:|
| Askar City | 0 | 0 | 0 | 0 | 0 | 0 |
| 0033 | 34 | 2 | 33 | 68 | 125 | 184 |
| Ouroboros | 32 | 6 | 32 | 64 | 0 | 1,409 |
| Banminary | 0 | 0 | 0 | 0 | 38 | 94 |
| CtrlAltDefeat v107 | 135 | 1 | 122 | 270 | 601 | 1,007 |
| Memtrace v33 | 9 | 1 | 9 | 18 | 225 | 15 |
| **TOTAL (6)** | **210** | **10** | **196** | **420** | **989** | **2,709** |

CAD alone contributes more deny events (135) than all four original matches
combined (66) — the single largest deny-arm activation in the corpus so far,
concentrated on one target. False-positive-looking events also grow
substantially (163 → 989), still concentrated in matches with little or no
genuine deny activity (Memtrace: 225 false-positive-looking vs. 9 real; CAD:
601 false-positive-looking vs. 135 real, in the *same* match this time —
unlike the original four, where false-positive-looking and real deny events
never co-occurred in one match. **This breaks the base doc's "never co-occur"
observation** (§3, "The 163 false-positive-looking events are concentrated
entirely in the two matches with zero on-target denies") — CAD has both real
deny activity (135, `_game_4`) and false-positive-looking events (601,
spread differently — not verified here which games). Flagged for a closer
look; not re-litigated in this fold-in pass.

### What moves / what stands — the four headline conclusions

1. **"Deny arm worked on Ouroboros" (18.16% → 8.21%, more than halved).**
   **UNCHANGED.** Neither new match is against Ouroboros; this is an
   opponent-specific claim the fold-in cannot speak to directly. The
   general "deny arm is active and selective" story it sits inside is
   reinforced (see #4).
2. **"Pooled rate worse via handoff" (4.33% wild baseline → 7.17% at n=4,
   carried by HANDOFF).** **WEAKENS, substantially.** The 6-match pooled
   rate is 3.70% — now *below* the 4.33% baseline it was being read against,
   reversing the base doc's "up, not down" framing at n=4. HANDOFF still
   dominates the leak composition (65.8% of a now-larger pool), so the
   mechanism-level caution stands, but the headline pooled-rate framing
   from the base doc no longer holds as stated. This is the single biggest
   change from the fold-in and should be the first thing re-quoted.
3. **"Wire arm negative" (metric B 56.9% vs. v75's 40.4% baseline, +16.5pt
   gap).** **WEAKENS but does not reverse.** Pooled metric B is now 46.01%,
   a +5.6pt gap to the 40.4% baseline — about a third of the original gap.
   Still directionally "the wire arm underperforms the thing it targets,"
   just by much less. Plausible confound (shorter games in the new pair)
   flagged, not resolved.
4. **"Deny gating clean" (fires only where exposure is real).** **STRENGTHENS
   on the core claim, complicated on a secondary one.** Both new matches
   reproduce proportional firing (high exposure → high volume in CAD;
   low exposure → low volume in Memtrace; zero speculative firing with zero
   exposure anywhere). But the "false-positive-looking events never
   co-occur with real deny activity in the same match" sub-finding from the
   base doc's §3 is broken by CAD (601 false-positive-looking + 135 real,
   same match) — that specific secondary claim should be dropped or
   requalified, not the primary gating claim.

### CAD v107 extra paragraph — launcher/deny interaction

CtrlAltDefeat is the launcher-heavy class the v79 cad-leg question concerned,
so its match gets one extra pass. **Deny-arm activity**: all 135 deny events
are in `_game_4`, the match's only leak game, and all target the single tile
`(10, 8)` — a real, sustained deny response to a fixed enemy belt tile, not
a one-off. **Launcher throws** (`moveBuilderBot` with `d²(from,to) > 1`, the
same detection rule `cad-ferry-premortem-2026-08-08.md` established):
across all 5 games, **every single throw event moves a CAD-owned builder
bot** (never one of ours) — CAD's own launcher never once threw one of our
builders in this match, reproducing the ferry-premortem's "100% of CAD's
throws move CAD's own bots" fingerprint exactly, including the r2-r4
opening-throw timing signature (`_game_1/2/4/5` all show a CAD-launcher
throw of a CAD bot at r2-4). More interesting: in **`_game_5` (the one loss),
starting r202 and recurring 14 more times through r450**, an
**OpenSverige launcher at (8,8)** repeatedly ejects the *same* CAD builder
bot (landing consistently at (11,12), pulled from a small cluster of source
tiles around (7-9, 7-9)) — a defensive repeat-throw loop matching the
ferry-premortem's "long-game repeat-throw loop belongs to the defender,
disposing of already-neutralized raiders" pattern, reproduced here on our
side against CAD. A single similar one-off event also appears in `_game_4`
at r70. **This did not prevent the `_game_5` loss** — worth a dedicated read
on whether that 14x-ejected raider was doing anything load-bearing each
cycle it returned, or whether the launcher was tied up on a low-value loop
while the game was lost elsewhere. Flagged, not investigated further here.
