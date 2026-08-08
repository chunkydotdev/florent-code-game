# v80 "Eir 9b" — production read (rev-6/7 pre-registration, fired at n=14)

**Research-arm decode, 2026-08-08.** Read-only: no games run, no bot files
touched, no platform calls, no downloads. All inputs on disk.

**Version stamp.** Live v80 = `bots/_v89sh/main.py`, md5
`e12f85855654e9e78227582d0dc15d4b` (prefix `e12f8585`) — reconfirmed against
the working tree at read time. Byte-identical to the v77 "Eir 9" content; the
v77→v80 relabel is an accounting event only.

**Window.** Baseline 1557.1 @ 396 → 1577.3 @ 410 (`elo_history.tsv` rows
2026-08-08 15:46 and 18:04). 14 matches played, **12 archived** — matches
#398–#409. The two unarchived matches are the **@397 opener (+5.8)** and the
**@410 tail (+9.4)**; both bracket the archive rather than sitting inside it
(proved by the rating chain, §5.1). Every number below is over the 12
archived matches / **60 games** unless the split is stated explicitly.

**Baselines cited (not re-derived, but see the calibration in §0.3).**
`docs/research/v77-truncated-mechanism-read-2026-08-08.md` + both addenda:
pooled enemy-banked 3.70%, mechanism 34.2 SIPHON / 65.8 HANDOFF / 0
MISROUTE, unwired-harvester-rounds A 43.17% / B 46.01% (v75-era 40.4% B,
v74-era 24.3% B), deny census 210 events / 420 Ti. Established facts built
on, not re-derived: `SLOT_UNDER=2` downstream-inert; `ferried()` is a
true-positive detector; the deny arm's FP-looking events have two innocent
producers (Addendum 2).

**Tooling.** Fresh implementation of the documented method (per-round
harvester wiring state, per-round belt-adjacency exposure, full-hop-path
stack ownership, deny-arm action detection), built on
`tools/replay_census.py`'s validated wire primitives. Parser trap honoured:
`Entity.team` is proto3 implicit-presence, so `team` defaults to **0**, never
`None`. Script + raw output live in this session's scratchpad
(`analyze.py`, `raw_games.json`, `raw_v77.json`).

---

## Verdict table

| check | verdict | headline number |
|---|---|---|
| **1. FT wild data** | **VOID AS POSED — v80 carries no FT arm.** Answered counterfactually instead | `ferried()` absent from `_v89sh`; wild FT triggers = **0 by construction**. Counterfactual: precision **1.000 (180/180)**, fires in **12/60 games**, median latency gain **+2.5 rounds**, expected gain over all games **+1.02 rounds**, and **zero** games where FT fires and proximity never does |
| **2. vs-Ouroboros kill condition** | **PATTERN SHIFTED — worse, and the shift is map/our-side, not opponent drift** | Same 0-5, same −15.1 Elo, same 100%-SIPHON leak fingerprint; but 2 core kills (r355, r571) vs v77's 1 (r683), and delivered-stack ratio 0.418 vs 0.498 |
| **3. leak family** | **RATE FLAT, MECHANISM MIX REAL BUT CONCENTRATED** | **3.31% pooled** (1,076/32,535) vs v77 3.70%. Split **52.9 SIPHON / 47.1 HANDOFF / 0 MISROUTE** — but 72.8% of all HANDOFF comes from one match |
| **4. wire arm** | **NO LONGER A NEGATIVE — but no improvement either; it sits on the baseline** | Metric **B 41.22%** vs v75's 40.4% (+0.8pt, was +5.6pt). Metric **A 5.82%**. Game-length confound **refuted** |
| **5. class/window** | **CLEAN, with one boundary ambiguity at the head** | 12/12 stamped `teamVersion=80`, contiguous rating chain, **+5.02 archived** on 31-29 games (0.517 share); window total ≈ **+20.2** |

**One-line verdict: on 12 archived matches v80 holds the field to a 0.517
game-share for +5.0 Elo, with the leak rate flat at 3.31% and the wire
regression closed to within a point of its v75 baseline — but the read's
biggest output is not a v80 number at all: a bit-exact calibration against
the v77 corpus shows the v77 read's mechanism split, metric A, and deny
census were produced by its pre-fix parser and are wrong, while every figure
its post-fix addendum produced reproduces exactly. Corrected, the v77 leak
was 99.2% SIPHON, not 65.8% HANDOFF — which inverts the v77 read's single
loudest conclusion.**

---

## 0. Corpus, validation, and a calibration that moves the baselines

### 0.1 Corpus

| # | match | opponent (their ver.) | seat | score (ours-theirs) | our eloDelta | createdAt → completedAt (UTC) |
|---:|---|---|:--:|:--:|---:|---|
| 398 | `bfd8cd46` | Team 48 (16) | B | **1-4** | −9.715 | 13:52:43.736 → 13:58:26.414 |
| 399 | `444942c2` | Focalground (4) | A | **2-3** | −3.294 | 14:02:43.720 → 14:07:42.482 |
| 400 | `2874c55e` | Memtrace (33) | A | **4-1** | +9.633 | 14:12:43.657 → 14:16:21.492 |
| 401 | `1e8c4e1b` | Kings College Munich (8) | B | **2-3** | −2.254 | 14:22:43.774 → 14:27:33.393 |
| 402 | `5a57ba6e` | Leviathan (27) | B | **5-0** | +17.905 | 14:32:43.655 → 14:37:14.593 |
| 403 | `5a8426ba` | The Bisons (2) | A | **3-2** | −0.661 | 14:42:43.719 → 14:46:40.249 |
| 404 | `7769008c` | opensverige - plan B (3) | A | **5-0** | +14.350 | 14:52:43.537 → 14:55:49.397 |
| 405 | `b8a10d95` | Lunds Stallions (44) | B | **1-4** | −9.220 | 15:02:43.716 → 15:03:21.755 |
| 406 | `16e6c29f` | **Ouroboros (8)** | B | **0-5** | −15.112 | 15:12:43.700 → 15:23:59.946 |
| 407 | `d540fe5a` | Powerpuff Girls (40) | A | **1-4** | −8.332 | 15:22:43.590 → 15:29:02.946 |
| 408 | `fe0c595f` | Memtrace (33) | A | **3-2** | +3.077 | 15:32:43.740 → 15:36:38.466 |
| 409 | `7371bd72` | Leviathan (32) | B | **4-1** | +8.646 | 15:42:43.643 → 15:48:22.902 |
| | **SUM (12 archived)** | | | **31-29** | **+5.0235** | |

All 12 stamped `teamVersion=80` for OpenSverige, all `triggeredBy: ladder`,
all 60 `.replay26` files present, zero exclusions. Seats taken from meta
`teamAName`/`teamBName`, never assumed.

**Two corrections to the task brief's corpus line, both from meta + seat:**

1. **`5a8426ba` (The Bisons v2) is a 3-2 WIN, not a 2-3 loss.** `scoreA=3`,
   `scoreB=2`, we are seat A, `winnerId` = OpenSverige. We won the match and
   still lost 0.661 Elo, because we entered at 1575.2 against their 1489.6 —
   a 3-2 is below the expected score at that gap. (The brief flagged this
   parenthetical as unverified; it was wrong.)
2. **`d540fe5a` (Powerpuff Girls v40) is a 1-4 loss** (seat A, `scoreA=1`)
   and **`b8a10d95` (Lunds Stallions v44) is a 1-4 loss** (seat B,
   `scoreB=1`). Both had no score in the brief; recorded here.

Everything else in the brief's corpus line reproduces exactly, including
every eloDelta to the stated decimal.

### 0.2 Mandatory validations

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected`, per team-side per game | **120/120 exact** (60 games × 2 sides), zero mismatches |
| **Winner reproduction** — per-game winner decoded from `Replay.winner`, tallied per match, compared to meta `scoreA`/`scoreB` | **12/12 matches, 60/60 games exact** |
| **Version stamp** | 12/12 metas `teamVersion=80` for OpenSverige; `_v89sh` md5 matches the ship note prefix |
| **Rating chain** | 11/11 transitions exact: `ratingBefore(k+1) == ratingBefore(k) + eloDelta(k)` to full precision. No gaps — the 12 archived matches are consecutive |
| **Stack accounting** | 32,535 our-origin stacks followed hop-by-hop via `resourceId`; **0 stacks of unknown origin** across 60 games |
| **Corpus completeness** | 60/60 replay files, 0 excluded |
| **Source stamp for check 1** | `grep -c "def ferried" bots/_v89sh/main.py` = **0**; `os_gate_open`/`OS_D_SQ_MAX`/`_os_armed` = **0** |

**No validation failed. Nothing to STOP on.**

### 0.3 CALIBRATION — the same implementation, re-run on the v77 6-match corpus

Because this read's whole job is comparison against the v77 baselines, the
implementation was re-run unchanged over the v77 corpus (`eb59c8bb`,
`83b0fd6d`, `d694094e`, `37e4f4ee`, `922b5da8`, `208e84f8`; 30 games, all on
disk). Result:

| v77 metric | v77 doc | this implementation | verdict |
|---|---:|---:|---|
| pooled mined / leaked / rate | 17,573 / 650 / 3.70% | **17,573 / 650 / 3.70%** | **exact** |
| per-match leaked (all 6) | 0 / 187 / 431 / 0 / 32 / 0 | **0 / 187 / 431 / 0 / 32 / 0** | **exact** |
| per-game Ouroboros leaks | 14 / 390 / 27 / 0 / 0 | **14 / 390 / 27 / 0 / 0** | **exact** |
| harvester-rounds (all 6) | 3,774 / 13,531 / 51,639 / 3,295 / 22,422 / 39,419 | **identical** | **exact** |
| metric **B** per match & pooled | …/46.01% | **…/46.01%** | **exact** |
| CAD deny / FP / exposure | 135 / 601 / 1,007 | **135 / 601 / 1,007** | **exact** |
| Memtrace deny / FP / exposure | 9 / 225 / 15 | **9 / 225 / 15** | **exact** |
| metric **A** pooled | 43.17% | **10.48%** | **DIVERGES** |
| mechanism split pooled | 222 S / 428 H (34.2 / 65.8) | **645 S / 5 H (99.2 / 0.8)** | **DIVERGES** |
| deny / FP / exposure totals | 210 / 989 / 2,709 | **509 / 2,418 / 9,000** | **DIVERGES** |

The divergences are **confined entirely to the four base-doc matches**. Every
figure the doc's **Addendum** produced (CAD v107 and Memtrace v33 — the two
matches computed after the addendum session caught and fixed the proto3
`team` default bug) reproduces **bit-exactly, on three independent counters
each**. That is not a coincidence a wrong implementation produces.

Reading it plainly: the v77 base doc's four-match rows for **metric A**, the
**mechanism split**, and the **deny census** came from the pre-fix
implementation and should not be quoted. Its four-match rows for **leak
volumes**, **harvester-rounds**, and **metric B** reproduce exactly and stand.
The addendum's pooled tables mixed pre-fix and post-fix rows, so the
published pooled 43.17% / 34.2-65.8 / 210-events figures are
mixed-implementation aggregates.

**Corrected v77 6-match baselines** (one implementation, all 30 games):

| | published | **corrected** |
|---|---:|---:|
| pooled enemy-banked rate | 3.70% | **3.70%** (unchanged) |
| mechanism SIPHON / HANDOFF / MISROUTE | 34.2 / 65.8 / 0 | **99.2 / 0.8 / 0** |
| unwired metric A | 43.17% | **10.48%** |
| unwired metric B | 46.01% | **46.01%** (unchanged) |
| deny events / Ti / FP-looking / exposure | 210 / 420 / 989 / 2,709 | **509 / 1,018 / 2,418 / 9,000** |

All v77-vs-v80 comparisons below use the **corrected** column. The published
column is shown alongside wherever it matters.

Confidence: **high.** Bit-exact agreement on seven independent post-fix
counters, plus exact agreement on every pre-fix counter that the fix could
not have touched (volumes, harvester-rounds, metric B), localizes the fault
precisely. What would change the answer: recovering the base doc's original
script (it lived in an ephemeral scratchpad and is gone from disk) and
finding a definitional difference rather than a bug.

---

## 1. Check 1 — FERRY-TEST (FT) wild data

### Verdict

**The check is void as posed: v80 does not contain the FT arm.** `ferried()`
is absent from `bots/_v89sh/main.py` (0 occurrences of `def ferried`); it
first appears in `bots/_v90ft/main.py:1179` (the FT plank) and thereafter in
`_v91os`, `_v91osb` (= v79), `_v92sp`, `_v93w`, `_v93wb`, `_v94fb`, `_v95e1`.
v80's three `SLOT_UNDER` writers (`:1538`, `:1548`, `:2026`) write only 0 or
1 — no site ever writes 2. **Wild FT trigger count over the corpus = 0 by
construction.** (v80 likewise carries no OS plank, confirming the brief.)

So the check was run as the counterfactual that actually answers the
question it was built to answer: *had v80 carried FT, what would it have
bought?* `ferried()`, `FERRY_SLACK=0`, `CORE_PAIRS`, `core_anchor_exact` and
`enemy_core_for` were lifted verbatim from `_v91osb` and evaluated against
the decoded replay state, with v79's own visibility model (an enemy is
sensed when it is within r²≤36 of our core anchor, or within r²≤20 of one of
our living builders).

**Answer: FT would have bought ≈1 round of expected earlier latch per game.**
Precision is confirmed at 1.000, but recall is the binding constraint, and
the latency gain — the whole of FT's live value, since `under=2` is
downstream-inert — is small and concentrated.

### Evidence

**Arming.** `core_anchor_exact` is true on **60/60 games** — every map in the
window is in `CORE_PAIRS`. FT would never have been silenced by an unknown
map in this window.

**Firing and precision.** `ferried()` returns true at least once in **12/60
games (20%)**, on **180 flagged builder-rounds**, **one distinct enemy
builder per game** in all 12.

| flagged builder-rounds | on a builder with a decoded teleport at-or-before the flag round | precision |
|---:|---:|---:|
| 180 | **180** | **1.000** |

A "decoded teleport" is a `moveBuilderBot` whose `d²(from, to) > 1` — the
same detection rule `cad-ferry-premortem-2026-08-07.md` established. **Zero
false positives via the physics predicate**, reproducing the 880-game
pre-ship claim on wild data.

**Latency gain, per game** (`ftvis` = first ferry latch under the visibility
model; `ftphys` = first round the predicate is true regardless of whether
anything of ours could see it; `prox` = the round v80's plain proximity path
actually first latches):

| match | g | opponent | map | ftphys | **ftvis** | **prox** | **gain** | flags |
|---|:--:|---|---|---:|---:|---:|---:|---:|
| `bfd8cd46` | 3 | Team 48 | 18x18 | r3 | r11 | r14 | **+3** | 19 |
| `bfd8cd46` | 5 | Team 48 | 25x25 | r3 | r15 | r27 | **+12** | 26 |
| `2874c55e` | 1 | Memtrace | 25x25 | r9 | r11 | r13 | **+2** | 21 |
| `2874c55e` | 4 | Memtrace | 16x16 | r5 | r7 | r14 | **+7** | 18 |
| `b8a10d95` | 1 | Lunds Stallions | 20x26 | r3 | r3 | r3 | **+0** | 4 |
| `b8a10d95` | 2 | Lunds Stallions | 24x24 | r3 | r10 | r31 | **+21** | 15 |
| `b8a10d95` | 3 | Lunds Stallions | 16x16 | r3 | r7 | r18 | **+11** | 19 |
| `b8a10d95` | 4 | Lunds Stallions | 21x8 | r3 | r3 | r3 | **+0** | 3 |
| `b8a10d95` | 5 | Lunds Stallions | 28x20 | r3 | r3 | r3 | **+0** | 5 |
| `fe0c595f` | 3 | Memtrace | 24x24 | r6 | r10 | r10 | **+0** | 15 |
| `fe0c595f` | 4 | Memtrace | 26x26 | r5 | r7 | r9 | **+2** | 19 |
| `fe0c595f` | 5 | Memtrace | 25x25 | r9 | r11 | r14 | **+3** | 16 |

- **Gain: median +2.5, mean +5.08, range 0–21, strictly positive in 8/12.**
- **Expected gain averaged over all 60 games: +1.02 rounds.**
- **Median trigger round: r8.5** (visibility-gated) / **r3.0** (pure
  physics). The pre-ship "~r5" claim sits between the two — consistent with
  both, and the difference is exactly the sensing delay.
- **Games where FT fires and the proximity path never does: ZERO.** The plain
  proximity path fires in **59/60 games** (median **r19**, mean 50.2, range
  1–587). The single game where it never fires (`d540fe5a` g2, 26x26, 1000
  rounds) has **zero** `ferried()` hits either — FT would not have covered it.

**Why recall, not precision, is the binding constraint.** 33/60 games contain
at least one enemy builder teleport, but only 12 produce a `ferried()` hit.
The predicate detects a throw only while the thrown builder is further than
`rnd + 2` manhattan from *its own* core footprint — a condition that
essentially only opening throws satisfy (every physics-first hit in the
table is r3–r9). Late-game throws are invisible to it: `bfd8cd46` g1 has
**168** enemy teleports starting at r27 and produces zero flags.

### Confidence and what would change the answer

**Confidence: high on precision and arming, medium-high on the gain
distribution.** Precision and arming are direct decodes. The gain figure
carries two modelling choices, both stated and both conservative:

1. The counterfactual evaluates the ferry check on every visible enemy
   builder every round. v79's core scan `break`s on the first proximity hit,
   so a real implementation could miss a ferried builder later in iteration
   order on that round. The builder scan has no such break. This biases the
   measured gain **upward** slightly.
2. `prox` is measured under the same visibility model. Measured on geometry
   alone (ignoring whether anything of ours could see the enemy), `prox` is
   **identical in all 60 games** — the proximity trigger geometry
   (turret d²≤64 / builder d²≤16 of the core anchor) is never satisfied
   before the enemy is sensed in this corpus. So the gain is not an artefact
   of the visibility model.

What would change the answer: an opponent mix with more opening ferries
(Lunds Stallions is the only opponent here that ferries in all 5 games), or a
`FERRY_SLACK` change — the cad-family study measured recall collapsing
0.79 → 0.42 at total margin 4, so slack is the wrong knob to loosen.

**Reading it against the s18 redesign.** `docs/ft-responder-redesign-2026-08-08.md`
establishes that the defect is *release*, not trigger: `SLOT_ATK_RND` is
refreshed by mere sighting, so the 50-round decay never fires while anything
is parked in vision. Against that, FT's measured wild contribution — an
expected 1 round of earlier onset for a latch that then never releases — is
close to zero value and non-zero cost (the expensive tier pins one round
sooner). This read supports the redesign's premise directly.

---

## 2. Check 2 — vs-Ouroboros kill-condition read (`16e6c29f`, 0-5)

### Verdict

**Ouroboros v8 beat v80 the same way it beat v77 — economic strangulation
first, screen-attrition core kill second — but harder: two core kills instead
of one, and both far earlier. The leak fingerprint is byte-for-byte the same
mechanism (100% adjacency siphon in both eras), which is the strongest single
piece of evidence that this is map draw plus our-side variance, not opponent
drift.**

### Evidence — how each game was won

| era | g | rounds | map | win condition | our deliv / theirs | ratio | mined | leaked | deny | exposure |
|---|:--:|---:|---|---|---:|---:|---:|---:|---:|---:|
| v77 `d694094e` | 1 | 1000 | 24x24 | titanium_collected | 598 / 2,079 | 0.288 | 686 | 14 | 44 | 1,548 |
| v77 | 2 | 1000 | 25x15 | titanium_collected | 1,489 / 1,552 | 0.959 | 1,946 | 390 | 32 | 2,512 |
| v77 | 3 | 1000 | 25x25 | titanium_collected | 930 / 2,510 | 0.371 | 1,059 | 27 | 167 | 1,946 |
| v77 | 4 | 1000 | 26x26 | titanium_collected | 1,144 / 2,349 | 0.487 | 994 | 0 | 0 | 818 |
| v77 | 5 | 684 | 16x16 | **core_destroyed** (r683) | 543 / 960 | 0.566 | 566 | 0 | 0 | 5 |
| **v80 `16e6c29f`** | 1 | 1000 | 16x16 | titanium_collected | **211 / 1,317** | **0.160** | 451 | **225 (49.9%)** | **0** | **914** |
| **v80** | 2 | 1000 | 24x24 | titanium_collected | 1,210 / 1,857 | 0.652 | 1,275 | 0 | 47 | 316 |
| **v80** | 3 | 356 | 25x25 | **core_destroyed** (r355) | 97 / 465 | 0.209 | 182 | 45 | **0** | 362 |
| **v80** | 4 | 572 | 18x18 | **core_destroyed** (r571) | 176 / 684 | 0.257 | 173 | 3 | 9 | 20 |
| **v80** | 5 | 1000 | 25x25 | titanium_collected | 814 / 1,676 | 0.486 | 1,070 | 131 | **239** | 1,711 |

**Match-level.** v77: delivered-stack ratio 4,704 / 9,450 = **0.498**, one
core kill at r683. v80: 2,508 / 5,999 = **0.418**, two core kills at **r355**
and **r571**. Leak rate 8.21% → **12.82%**.

**State at each core death** (decoded at the removeEntity round):

| game | round | our deliv / theirs | our harvesters / theirs | **our units / theirs** |
|---|---:|---:|---:|---:|
| v77 g5 | 683 | 543 / 960 | 4 / 6 | **2 / 14** |
| v80 g3 | 355 | 97 / 465 | 5 / 6 | **2 / 25** |
| v80 g4 | 571 | 176 / 684 | 2 / 6 | **1 / 23** |

The kill condition is unchanged in kind: by the time our core dies we are
down to 1–2 living units against 14–25 of theirs, with harvester parity
roughly intact — i.e. **they win the unit-count war long before they win the
building war, and the core falls as the last item on the list.** That is the
screen-attrition signature, reproduced. What changed is the clock: 25 units
against 2 at r355 is a substantially faster attrition curve than 14 against 2
at r683.

**Our deny arm vs their siphon exposure.** Deny fired **295** times across
this match (v77: 243), on 3,323 exposure harvester-rounds (v77: 6,829) — a
density of 0.089 vs 0.036, i.e. **2.5× denser response per exposed
harvester-round.** And yet the leak rate rose. The two games that carry
essentially the whole leak are the two the deny arm did not respond to at
all: **g1 (914 exposure harvester-rounds, 0 deny events, 225 stacks leaked =
49.9% of everything mined that game)** and **g3 (362 exposure, 0 deny, 45
leaked)**. Where the arm did fire hardest (g5: 239 events on 1,711 exposure)
the leak is 12.2%; where it fired at all (g2: 47 events) the leak is **zero**.

**Their mechanism, both eras: 100% ADJACENCY_SIPHON, 0 HANDOFF, 0 MISROUTE**
(v77: 431/0/0; v80: 404/0/0, under the calibrated classifier). Their kit is
unchanged and the published v77 claim of a 42.7/57.3 SIPHON/HANDOFF split
against them is an artefact of the pre-fix parser (§0.3).

### Same-version opponent: drift or our-side noise?

Ouroboros is v8 in both windows. The evidence supports **our-side/map
variance, not hidden opponent drift**:

- The leak mechanism fingerprint is identical (pure adjacency siphon, zero
  handoff) in both matches — a drifted opponent would be the natural place
  for a new channel to appear, and none does.
- The map sets are disjoint apart from 24x24 and 25x25 (v77: 24x24, 25x15,
  25x25, 26x26, 16x16; v80: 16x16, 24x24, 25x25, 18x18, 25x25), and the two
  worst v80 games (g1 on 16x16, g3 on 25x25) are exactly where our deny arm
  went silent under real exposure — a *geometry* failure, which is a map-draw
  interaction with our acquisition gate, not their behaviour.
- Elo is essentially identical across the two eras (−15.17 v77, −15.11 v80)
  because both are 0-5 at near-identical rating gaps.

Confidence: **medium-high.** n=1 match per era, and 5 games is thin for a
per-game claim. What would change the answer: a third Ouroboros match on
overlapping maps, or a deny-arm-disabled control (which does not exist in
the wild corpus).

**Note on scope.** The rev-7 pre-registration's "early standoff" framing does
not apply: v80 carries **no OS plank** (`os_gate_open` absent from `_v89sh`),
confirmed at source. The standoff-timing sub-question is void for this
window, and no OS-gate map analysis was run.

---

## 3. Check 3 — leak family

### Verdict

**Pooled rate flat and slightly better: 3.31% vs the corrected v77 3.70%.
The mechanism mix looks like a large shift (99.2% SIPHON → 52.9%) but it is
not broad — 72.8% of all pooled HANDOFF comes from a single match against
"opensverige - plan B", and 96.4% of it from a single game.**

### Evidence — per match

| match | opponent | mined | leaked | rate | SIPHON | HANDOFF | MISROUTE |
|---|---|---:|---:|---:|---:|---:|---:|
| `bfd8cd46` | Team 48 (16) | 269 | 0 | 0.00% | — | — | — |
| `444942c2` | Focalground (4) | 1,422 | 24 | 1.69% | 24 | 0 | 0 |
| `2874c55e` | Memtrace (33) | 1,173 | 0 | 0.00% | — | — | — |
| `1e8c4e1b` | Kings College Munich (8) | 3,422 | 81 | 2.37% | 81 | 0 | 0 |
| `5a57ba6e` | Leviathan (27) | 4,775 | 136 | 2.85% | 7 | **129** | 0 |
| `5a8426ba` | The Bisons (2) | 137 | 0 | 0.00% | — | — | — |
| `7769008c` | **opensverige - plan B (3)** | 5,104 | **378** | **7.41%** | 9 | **369** | 0 |
| `b8a10d95` | Lunds Stallions (44) | 651 | 16 | 2.46% | 16 | 0 | 0 |
| `16e6c29f` | **Ouroboros (8)** | 3,151 | **404** | **12.82%** | **404** | 0 | 0 |
| `d540fe5a` | Powerpuff Girls (40) | 4,848 | 0 | 0.00% | — | — | — |
| `fe0c595f` | Memtrace (33) | 3,993 | 27 | 0.68% | 27 | 0 | 0 |
| `7371bd72` | Leviathan (32) | 3,590 | 10 | 0.28% | 1 | 9 | 0 |
| **POOLED (12)** | | **32,535** | **1,076** | **3.31%** | **569 (52.9%)** | **507 (47.1%)** | **0 (0.0%)** |

vs **corrected v77 (6 matches): 17,573 / 650 / 3.70%, 645 SIPHON (99.2%) /
5 HANDOFF (0.8%) / 0 MISROUTE.**
(vs *published* v77: same rate, 34.2 / 65.8 / 0 — see §0.3.)

**MISROUTE is 0 in both windows and in every one of the 90 games decoded
across both corpora.** No stack in this corpus is ever delivered from a
harvester straight into the enemy core.

### The new dominant channel, and why it is narrower than it looks

HANDOFF rises from 5 stacks (v77) to 507 (v80). Its concentration:

| source | HANDOFF stacks | share of pooled HANDOFF |
|---|---:|---:|
| `7769008c` **plan B g5** | 366 | **72.2%** |
| `5a57ba6e` Leviathan v27 g5 | 124 | 24.5% |
| `7371bd72` Leviathan v32 g4 | 9 | 1.8% |
| `7769008c` plan B g3 | 3 | 0.6% |
| everything else (56 games) | 5 | 1.0% |

**Two games carry 96.6% of the pooled HANDOFF volume**, and one of them is
against **our own second-slot bot** ("opensverige - plan B" v3 — a mirror of
our lineage's belt geometry). A leak channel that only opens when the
opponent's conveyor network is shaped like ours is not evidence of a general
new channel in the field; it is closer to a self-play artefact. Flagged as
such rather than reported as a field trend.

The one genuinely field-relevant HANDOFF source is **Leviathan** (129 + 9
across two matches, both in a single game each, both games we won). Worth one
targeted look if Leviathan recurs; not worth a plank on this evidence.

**Opponent flag: Ouroboros remains the single worst leak matchup in the
field** — 12.82%, ~4× the pooled rate, 100% on the arm's own target mechanism
(§2).

### The 0033 question

**There are no 0033 matches in this corpus, so the handoff-per-0033 question
stays unanswered.** It also changes shape: under the calibrated classifier,
v77's 0033 match reads **182 SIPHON / 5 HANDOFF**, not the published 6 / 181.
The v77 read's framing — "0033 is a HANDOFF-dominated leak the deny arm was
never built to fix" — does not survive the calibration, and the successor
question is now "why did 0033 produce a 9.04% *siphon* rate that the deny arm
did not suppress", which is a different investigation.

Confidence: **high** on the volumes and rate (exact reproduction of the v77
corpus, zero unknown-origin stacks), **medium-high** on the mechanism labels
(the classifier is a literal reading of the documented definitions, and it
agrees with every post-fix v77 figure and with Ouroboros's known kit; it
disagrees with the pre-fix v77 labels). What would change the answer: a
third-party re-implementation of the mechanism classifier, or the recovery of
the base doc's original script.

---

## 4. Check 4 — wire-arm metric (unwired harvester-rounds)

### Verdict

**The wire-arm negative is essentially retired: metric B reads 41.22% against
the v75 baseline of 40.4% — a +0.8-point gap where v77 published +5.6 and its
base doc published +16.5. But that is "back to baseline", not "fixed": the
v75 regression was itself the thing to be fixed, and v80 sits on it.** The
game-length confound the v77 addendum invoked is **refuted**.

Definitions are the v77 read's exactly. **Metric A** = harvester alive with
zero friendly conveyor/splitter on any of its 4 orthogonal neighbours.
**Metric B** = complement of directed-wired: harvester is wired iff it is
orthogonally adjacent to our core footprint, or one of its 4 orthogonal
neighbours holds a friendly relay in the facing-respecting delivering set
(`replay_census.py`'s `chains()`/`directed`).

| match | opponent | harvester-rounds | **A** | **B** |
|---|---|---:|---:|---:|
| `bfd8cd46` | Team 48 | 2,038 | 40 (1.96%) | 1,096 (53.78%) |
| `444942c2` | Focalground | 8,034 | 45 (0.56%) | 2,622 (32.64%) |
| `2874c55e` | Memtrace | 13,166 | 55 (0.42%) | 8,878 (67.43%) |
| `1e8c4e1b` | Kings College Munich | 20,052 | 856 (4.27%) | 7,344 (36.62%) |
| `5a57ba6e` | Leviathan (27) | 34,460 | 611 (1.77%) | 12,347 (35.83%) |
| `5a8426ba` | The Bisons | 943 | 111 (11.77%) | 481 (51.01%) |
| `7769008c` | plan B | 26,613 | 131 (0.49%) | 7,741 (29.09%) |
| `b8a10d95` | Lunds Stallions | 4,097 | 235 (5.74%) | 1,892 (46.18%) |
| `16e6c29f` | **Ouroboros** | 36,969 | **10,340 (27.97%)** | **26,669 (72.14%)** |
| `d540fe5a` | Powerpuff Girls | 30,634 | 372 (1.21%) | 7,620 (24.87%) |
| `fe0c595f` | Memtrace | 31,928 | 82 (0.26%) | 12,685 (39.73%) |
| `7371bd72` | Leviathan (32) | 20,722 | 481 (2.32%) | 5,293 (25.54%) |
| **POOLED (12)** | | **229,656** | **13,359 (5.82%)** | **94,668 (41.22%)** |

**History.** Metric B: v74 24.3% → v75 **40.4%** (the regression) → v77
published 46.01% / corrected **46.01%** → **v80 41.22%**.
Metric A: local hsd 3.21% / sh 4.69% → v77 published 43.17% / **corrected
10.48%** → **v80 5.82%**. v80's metric A now sits in the same band as the
local-corpus comparators the ad-flips read produced, which is the first time
the wild and local metric-A readings have agreed.

**Ouroboros is again the heaviest single driver**: 26,669 of the 94,668
pooled metric-B unwired-rounds (28.2%) come from one match, and it is the
only match above 72% on B or above 28% on A. Excluding it, pooled B is
**35.2%** — *below* the v75 baseline.

### Game-length confound: tested and refuted

The v77 addendum attributed CAD's and Memtrace's low readings to shorter
games. Split both corpora by game length:

| corpus | segment | games | harvester-rounds | A | B |
|---|---|---:|---:|---:|---:|
| **v80 (12)** | full 1000-round | 20 | 180,227 | **5.89%** | **41.23%** |
| **v80 (12)** | sub-1000 | 40 | 49,429 | **5.57%** | **41.19%** |
| v77 (6) | full 1000-round | 12 | 116,444 | 10.42% | 46.60% |
| v77 (6) | sub-1000 | 18 | 17,636 | 10.91% | 42.10% |

**Game length is not the driver.** In the v80 corpus the two segments are
within 0.3 points of each other on A and 0.04 points on B. In the v77 corpus
the gap is 4.5 points on B, in the *opposite* direction to the addendum's
hypothesis for A. The variance is opponent/map, not clock.

**Evidence for the already-approved strip riding the staged head:** this read
supports it. The metric the strip targets is at baseline, not above it, and
the residual is concentrated in one matchup (Ouroboros) whose unwired-rounds
co-occur with the deny arm's own silent-under-exposure games. Nothing here
argues against shipping the strip; nothing here promises it a measurable
pooled win either.

Confidence: **high** (exact reproduction of the v77 corpus on both
harvester-rounds and metric B; metric A now agrees with the local corpus).
What would change the answer: a windowed comparison against a v75-content
window on the same opponent draw, which does not exist.

---

## 4b. Deny-arm census (supporting evidence for §2–§3)

| match | opponent | deny | Ti | FP-looking | exposure (harvester-rounds) |
|---|---|---:|---:|---:|---:|
| `bfd8cd46` | Team 48 | 0 | 0 | 49 | **0** |
| `444942c2` | Focalground | 22 | 44 | 351 | 215 |
| `2874c55e` | Memtrace | 0 | 0 | 45 | **0** |
| `1e8c4e1b` | Kings College Munich | 16 | 32 | 123 | 511 |
| `5a57ba6e` | Leviathan (27) | 94 | 188 | 148 | 168 |
| `5a8426ba` | The Bisons | 0 | 0 | 33 | **0** |
| `7769008c` | plan B | 263 | 526 | 1,243 | 1,157 |
| `b8a10d95` | Lunds Stallions | 7 | 14 | 90 | 72 |
| `16e6c29f` | Ouroboros | 295 | 590 | 102 | 3,323 |
| `d540fe5a` | Powerpuff Girls | 41 | 82 | 125 | 974 |
| `fe0c595f` | Memtrace | 0 | 0 | 81 | 211 |
| `7371bd72` | Leviathan (32) | 37 | 74 | 353 | 64 |
| **TOTAL (12)** | | **775** | **1,550** | **2,743** | **6,695** |

vs **corrected v77 (6): 509 / 1,018 / 2,418 / 9,000.**

**Primary gating claim STANDS and strengthens.** Zero-exposure games fire
zero deny events: **37/37** in v80 (16/16 in v77). The arm never attacks
speculatively.

**Proportionality claim FAILS in a specific, nameable way.** Of the 23 v80
games with non-zero exposure, **3 fired zero deny events**: `16e6c29f` g1
(914 exposure-rounds, 225 stacks leaked), `16e6c29f` g3 (362, 45 leaked),
`fe0c595f` g1 (211, 27 leaked). The corrected v77 corpus shows the same
failure mode at 4/14 (`d694094e` g4 at 818 exposure, `922b5da8` g2 at 761,
plus two trivial ones). **Every one of the three v80 silent-under-exposure
games leaked**, and together they carry 297 of the corpus's 1,076 leaked
stacks (27.6%) — this is the single sharpest actionable finding in the deny
family and it is a *new* one: the published v77 census could not see it.

Response density rose: **0.0566 → 0.1158 deny events per exposure
harvester-round** (2.05×). The arm responds harder where it responds at all.

FP-looking events co-occur freely with real deny activity (`7769008c` g3:
229 real + 292 FP-looking in one game) — consistent with Addendum 2's
resolution (stale-hold ≤24 rounds + siege-role belt attacks). No new
question raised.

---

## 5. Check 5 — class / window accounting

### 5.1 Boundary stamps

All 12 archived matches carry `teamVersion=80` for OpenSverige in meta.
`createdAt` runs 13:52:43.736Z → 15:42:43.643Z on an exact **10-minute ladder
cadence at :x2:43** (all 12, no exceptions). `completedAt` 13:58:26Z →
15:48:22Z. All `triggeredBy: ladder`.

The rating chain closes the window without gaps:

```
1557.1  @396  (baseline, elo_history 15:46)
  +5.806      @397  opener            [NOT ARCHIVED]
1562.9060 -> 12 archived matches -> 1567.9294   (net +5.0235)
  +9.4        @410  tail              [NOT ARCHIVED]
1577.3  @410  (elo_history 18:04)
```

`ratingBefore(k+1) == ratingBefore(k) + eloDelta(k)` holds exactly for all 11
internal transitions, and `ratingBefore(#398) = 1562.9060 = 1557.1 + 5.806`
reproduces the opener's stated +5.8. Every intermediate value is
independently confirmed by an `elo_history.tsv` row (16:17→1560@400,
16:27→1557@401, 16:37→1575@402, 16:48→1575@403, 16:58→1589@404,
17:08→1580@405, 17:28→1565@406, 17:33→1556@407, 17:39→1559@408,
17:49→1568@409). **The 12 archived matches are the contiguous interior of the
window; the two unarchived matches are its first and last.**

**Opponents of the two unarchived matches: NOT RECOVERABLE FROM DISK.**
Neither `elo_history.tsv` (rating/matches/rank only), `tools/monitors/` (no
state files persisted), `results.tsv` (local arena only), `HANDOVER.md`, nor
`docs/coordination.md` records them; no cached fcode CLI match list exists on
disk. No platform call was made. They remain +5.8 vs unknown and +9.4 vs
unknown.

**BOUNDARY AMBIGUITY AT THE HEAD — flagged, not resolved.** The ladder's
exact :x2:43 cadence places the @397 opener's `createdAt` at **13:42:43Z =
15:42:43 local**, which is **~4 minutes before** the builder's
`docs/coordination.md` note timestamped *2026-08-08 15:47 (from `date`) —
ROLLBACK SHIP, v80 LIVE*. Under the v67 activation precedent (a version goes
live at the upload second, and matches created after it carry the new stamp),
the opener may have been a **v79**-stamped match, with the builder's wrap note
("activation read 1562.9@397 — first match +5.8") attributing it to v80 by
inference rather than by a meta stamp. Both accountings:

| reading | matches | net Elo | note |
|---|---:|---:|---|
| window = 14 (brief's premise) | 14 | **+20.2** | opener attributed to v80 |
| window = 13 (opener is v79) | 13 | **+14.4** | from 1562.9060 to 1577.3 |
| archived only (unambiguous) | 12 | **+5.0235** | all meta-stamped v80 |

This affects only the Elo headline. **No mechanism check is affected** — all
12 mechanism-decoded matches are meta-stamped v80. Resolving it needs the
opener's meta, i.e. a platform call, which this read does not make.

### 5.2 Per-opponent-class accounting (12 archived, n=14 window)

| class (their ver.) | matches | games | game-share | net Elo | Elo/match |
|---|---:|:--:|---:|---:|---:|
| **Leviathan** (27, 32) | 2 | 9-1 | **0.900** | **+26.551** | +13.28 |
| opensverige - plan B (3) | 1 | 5-0 | 1.000 | +14.350 | +14.35 |
| **Memtrace** (33, 33) | 2 | 7-3 | **0.700** | **+12.711** | +6.36 |
| The Bisons (2) | 1 | 3-2 | 0.600 | −0.661 | −0.66 |
| Kings College Munich (8) | 1 | 2-3 | 0.400 | −2.254 | −2.25 |
| Focalground (4) | 1 | 2-3 | 0.400 | −3.294 | −3.29 |
| Powerpuff Girls (40) | 1 | 1-4 | 0.200 | −8.332 | −8.33 |
| Lunds Stallions (44) | 1 | 1-4 | 0.200 | −9.220 | −9.22 |
| Team 48 (16) | 1 | 1-4 | 0.200 | −9.715 | −9.72 |
| **Ouroboros (8)** | 1 | 0-5 | **0.000** | **−15.112** | −15.11 |
| **TOTAL** | **12** | **31-29** | **0.517** | **+5.0235** | +0.42 |

Plus **+5.8** (opener, opponent unknown) and **+9.4** (tail, opponent
unknown), neither of which can be assigned to a class.

**Strongest per-class read: Leviathan, +26.551 across 2 matches spanning
their own v27→v32 bump, 9-1 in games.** The bump did not help them: v27 lost
0-5 (−17.905), v32 lost 1-4 (+8.646 to us). Two matches is thin, but a 0.900
game-share across two of their versions is the cleanest positive signal in
the window and the one worth defending.

**Second: Memtrace v33, 7-3 across 2 matches (+12.711)** — and this class is
**concordant across windows**: the v77 window's single Memtrace v33 match was
5-0 (+13.892). Combined across both windows on identical bytes: **12-4 in
games, +26.603 Elo across 3 matches.** The strongest cross-window class read
available.

**Ouroboros v8 is also concordant across windows and negative in both**: 0-5
/ −15.172 (v77) and 0-5 / −15.112 (v80). **0-10 in games across two matches,
−30.284 Elo.** Same bytes, same opponent version, same result twice.

### 5.3 Concordance with the v77 6-match window (same bytes)

| | v77 window (6 matches) | **v80 window (12 archived)** |
|---|---:|---:|
| game record | 20-10 (**0.667**) | **31-29 (0.517)** |
| net Elo | +34.144 | **+5.024** |
| Elo per match | +5.69 | **+0.42** |
| shutouts for / against | 2 / 1 | 2 / 1 |
| our delivered-stack share | 0.465 | **0.523** |

**DIVERGENT on the headline, CONCORDANT where the classes overlap.** The
per-match Elo drops by an order of magnitude, but the two overlapping classes
(Memtrace, Ouroboros) reproduce almost exactly, and our *economic* share
actually improves (0.465 → 0.523 of delivered stacks). The divergence is
carried by a negative tail the v77 window simply did not draw: Team 48
(−9.7), Lunds Stallions (−9.2), Powerpuff Girls (−8.3) — three opponents
absent from the v77 window, contributing −27.3 between them, against a v77
window whose worst non-Ouroboros result was 0033 at −1.9.

**Read honestly: this is opponent-draw variance on identical bytes, not a
performance change.** The correct statement of v80's field position is the
combined 18-match record on this content: **51-39 in games (0.567), +39.17
Elo**, not either window alone.

Confidence: **medium-high** on the class table (exact meta arithmetic),
**medium** on the concordance claim (n=1–2 per class).

---

## 6. What moves / what stands — against the v77 read's conclusions

| # | v77 conclusion | status | why |
|---|---|---|---|
| 1 | **"Deny arm worked on Ouroboros" (18.16% → 8.21%)** | **REVERSES on the follow-up window.** | v80's Ouroboros match reads **12.82%**, up from 8.21%, with 2.5× denser deny response. The v75→v77 halving is not sustained. The arm's own target mechanism is still 100% of that leak |
| 2 | **"Pooled rate worse via HANDOFF" (published 34.2/65.8)** | **RETIRED — the split was a parser artefact.** | Corrected v77 = **99.2% SIPHON / 0.8% HANDOFF**. The v77 read's loudest mechanism claim inverts. v80's 52.9/47.1 is a real shift *from that corrected base*, but 96.6% of the HANDOFF volume is two games, one of them self-play |
| 3 | **"Wire arm negative" (metric B 46.01% vs 40.4%, +5.6pt)** | **WEAKENS to near-null.** | v80 metric B **41.22%**, +0.8pt over baseline; excluding Ouroboros, **35.2%** — below baseline. Still not "the wire arm works": it is at baseline, and the baseline was the regression |
| 4 | **"Shorter games explain the metric drop"** (addendum caveat) | **REFUTED.** | Full-1000 vs sub-1000 segments differ by 0.04pt on B and 0.3pt on A in the v80 corpus. Length is not the driver |
| 5 | **"Deny gating clean — fires only where exposure is real"** | **SPLITS: primary STANDS, proportionality FAILS.** | Zero-exposure → zero deny in **37/37** games (strengthens). But **3/23 exposed games fired zero deny, and all three leaked** (297 stacks, 27.6% of the corpus leak). The corrected v77 corpus shows the same at 4/14 |
| 6 | **"FP-looking events never co-occur with real deny"** (already requalified, Addendum 2) | **STANDS AS RETIRED.** | Co-occurrence is routine in v80 (plan B g3: 229 + 292). Addendum 2's two innocent producers cover it; nothing new needed |
| 7 | **"Metric A vs metric B ambiguity is unresolved"** (§6 bounded item 1) | **RESOLVED enough to standardise.** | Metric A published at 43.17% was a pre-fix artefact; corrected it is 10.48% (v77) and 5.82% (v80) — now consistent with the local hsd/sh comparators (3.21/4.69%). **Standardise on B for the wild series and A for local corpora**, and stop quoting the 43.17% figure |
| 8 | **"0033 is a HANDOFF-dominated matchup the deny arm can't fix"** | **RETIRED.** | Corrected, 0033's leak is **182 SIPHON / 5 HANDOFF**. No 0033 match in this corpus, so the follow-up is open — but it is now a *siphon* question |
| 9 | **`ferried()` precision 1.000 (pre-ship, 880 games)** | **STANDS — reproduced in the wild.** | 180/180 flagged builder-rounds on already-teleported builders, 12/60 games |
| 10 | **FT median trigger ~r5** | **STANDS, bracketed.** | Median r3.0 (physics) / r8.5 (visibility-gated). "~r5" is between the two |
| 11 | **FT is worth shipping for the earlier latch** | **DOES NOT HOLD at this opponent mix.** | Expected gain **+1.02 rounds per game**; zero games where FT covers a latch proximity misses; and per the s18 redesign the latch never releases anyway. FT's value is bounded by recall (only opening throws are detectable), not precision |

---

## 7. Self-checks

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected` | **120/120 team-sides**, 0 mismatches (60 games × 2 sides) |
| **Winner reproduction** vs meta `scoreA`/`scoreB` | **12/12 matches, 60/60 games exact** |
| **Version stamp — bot** | `bots/_v89sh/main.py` md5 `e12f85855654e9e78227582d0dc15d4b` matches the ship note prefix `e12f8585` |
| **Version stamp — matches** | 12/12 metas `teamVersion=80` for OpenSverige |
| **Window boundary** | `createdAt` 13:52:43.736Z–15:42:43.643Z, exact 10-min cadence; rating chain 11/11 transitions exact; 10/10 intermediate values confirmed against independent `elo_history.tsv` rows |
| **Stack accounting** | 32,535 our-origin stacks followed hop-by-hop via `resourceId`; **0 unknown-origin stacks** in 60 games; mechanism classified on first post-origin hop per the documented definitions |
| **Parser trap** | `Entity.team` defaulted to 0 (TEAM_A), per `replay_census.py`'s `parse_entity` convention; verified by the fact that seat-A matches produce non-zero friendly harvester-rounds and non-zero our-origin stacks |
| **Signed varint handling** | `UpdateHp.delta` decoded as signed int32 (10-byte two's-complement varints), needed for the core-HP-drop latch path |
| **Cross-implementation calibration** | Same implementation re-run on the v77 6-match corpus: **7 counters reproduce bit-exactly**, 3 diverge and the divergence is localised to the pre-fix base-doc rows (§0.3) |
| **FT counterfactual fidelity** | `ferried()`, `FERRY_SLACK`, `CORE_PAIRS`, `core_anchor_exact`, `enemy_core_for` lifted **verbatim** from `bots/_v91osb/main.py`; teleport detection is the `cad-ferry-premortem` rule (`d²(from,to) > 1`) |
| **Proximity-latch geometry** | Anchor-measured per the fjordgate read: turret d²≤64 / builder d²≤16 of the core anchor, `B8_ON = False` in `_v89sh` so `gun_sense`/`b_sense` are 64/16 in every game; geometry-only and visibility-gated latch rounds are **identical in all 60 games** |
| **Games excluded** | zero |

### Bounded and unexplained

1. **The @397 opener's version stamp is unverifiable on disk** (§5.1). The
   ladder cadence puts its creation ~4 minutes before the builder's "v80
   LIVE" note. Bound: one match, ±5.8 Elo on the window headline; zero effect
   on every mechanism check.
2. **The v77 base doc's pre-fix figures cannot be traced to a specific bug**
   — the original script is gone from disk. What is established is that they
   are not reproducible by an implementation that reproduces every one of the
   doc's post-fix figures bit-exactly. Bound: metric A, the mechanism split,
   and the deny census for 4 of 6 v77 matches.
3. **The FT counterfactual's latency gain carries a small upward bias** from
   modelling the ferry check without v79's core-scan `break` (§1). Bound:
   affects the core-scan path only; the builder scan has no break, and the
   builder scan is where the pre-ship study located the median 5-round gain.
4. **Deny Ti spend (1,550) uses the flat 2 Ti/attack figure from CLAUDE.md**,
   not a per-builder titanium-delta ledger. Same assumption the v77 read made.
5. **No matched control exists in the wild for any arm.** Nothing here is a
   causal payback number, and none is asserted as one.
6. **Per-class n is 1–2 matches everywhere.** The class table is exact
   arithmetic on noisy samples; only Memtrace and Ouroboros have a
   cross-window replicate.
