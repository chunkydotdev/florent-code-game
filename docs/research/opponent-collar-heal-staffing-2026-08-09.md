# Per-opponent collar-heal staffing: BOTH Ouroboros and CAD garrison their core. Neither is the near-zero the plank feared — but only CAD gives the middle game anything to deny.

**Research arm, session 24, 2026-08-09.** Answers the builder arm's blocking question
for the unrated probe leg: *does the opponent staff healer builder bots on its own
core's collar seats, and at what rate?*

**Version tag:** live slot **v94** = `bots/_v115dodge`, treehash `6ae6871c`.
**Corpus** git sha `7418e13`, archive **6,233** replays at `manifest.json` build time.
**Inputs frozen before the run** — replay file list snapshotted to scratchpad
(`6,273` `.replay26` files on disk at freeze, i.e. the keeper had already appended 40
past the manifest); `corpus/join.tsv` copied at freeze, md5 `e943d4ac38e5339ac7c577263b9156cf`,
**1,445 attributed rows, all 1,445 present on disk**. The keeper's later appends
cannot affect anything here. **Zero replay downloads.**

**Corpus files read:** `corpus/join.tsv` (the only one consumed by the decoder),
`corpus/manifest.json` (provenance). `corpus/league_matches.tsv` was **not** used —
no version stratification is needed for this question, and the `oppver`/`verA`/`verB`
columns are dead in every row (verified elsewhere, not re-litigated here).

**Decoder:** `docs/research/scripts/collar-heal-2026-08-09/collar_decode.py`
(md5 `60e56934`), `analyse.py` (md5 `90952fbc`).
**1,445 files × 2 sides → 1,443,480 round rows in 26 s, 0 errors.**

---

## 1. THE ANSWER, in the form the leg needs

| | **Ouroboros** | **CtrlAltDefeat** |
| --- | ---: | ---: |
| archived games vs us | **105** | **85** |
| rounds decoded | 71,836 | 43,684 |
| **rounds with ≥1 bot on their 8 heal-capable collar seats** | **40.7%** | **39.3%** |
| mean collar seats occupied / round | 0.497 | 0.546 |
| **core heals per game** | **22.3** | **22.3** |
| core heals / 100 rounds | 3.26 | 4.34 |
| games with ≥1 core heal | **81%** | **66%** |
| heal events per 100 HP of core damage taken | **13.5** | **10.1** |
| **share of their core damage healed back** | **53.7%** | **40.3%** |
| **core heals / 100 rounds, r151–300, in-window** | **1.26** | **7.51** |

**Neither opponent is a near-zero.** Both put bodies on their own collar and both
convert them into real HP on the core — Ouroboros recovers **53.7%** of the core damage
we inflict, CAD **40.3%**. A denial plank is *falsifiable against both*.

**But the middle game — the band the plank targets — separates them, and not through
their behaviour: through ours.** Inside their own siege window:

| r151–300, in their core's siege window | Ouroboros | CAD |
| --- | ---: | ---: |
| core damage we inflict / 100 rounds | **9.3** | **68.0** |
| their core heals / 100 rounds | **1.26** | **7.51** |
| their heals per 100 HP damage | 13.5 | 11.1 |
| collar occupied ≥1 seat | 35.6% | 48.9% |

**Their per-damage heal reflex is the same (13.5 vs 11.1). The volume differs 6×
because against Ouroboros we barely touch their core after r150 at all.** Against
Ouroboros in r301+ their core takes **0.0 HP per 100 rounds** — there is literally
nothing to heal, so a denial signal there cannot exist regardless of their policy.

**RECOMMENDATION FOR THE LEG: fire the denial probe at CAD.** Against CAD the middle
game already carries 68 HP/100rd of core pressure and a 7.5/100rd heal response to
suppress, so the leg measures denial. Against Ouroboros the plank would first have to
manufacture the pressure it intends to deny — the probe would be measuring our own
approach rate, not their heal policy. **This is a different reason from "Ouroboros
doesn't heal" — that hypothesis is refuted; they do.**

---

## 2. Seat definition — and why the primary ring is 8, not 12

A 2×2 core footprint has a **12-tile Chebyshev-1 ring**, not 8. The requester's
"8 tiles orthogonally adjacent to its own core footprint" is a *different and narrower*
set. **This document uses the 8 as primary, deliberately.**

```
      . A B .          FP = the 4 core tiles (x)
      H x x C          ORTH8 = A B C D E F G H  <-- PRIMARY
      G x x D          CHEB12 = ORTH8 + the 4 diagonal corners (.)
      . F E .
```

* **ORTH8 (primary).** A builder bot's `heal(position)` requires an **orthogonally
  adjacent** tile. These 8 tiles are therefore *exactly* the tiles from which the core
  can be healed. The 4 Chebyshev corners cannot heal the core at all — counting them
  would inflate "collar staffing" with bots that are structurally incapable of the
  behaviour the plank targets.
* **CHEB12 (secondary occupancy only).** Reported because it is cheap and because a bot
  on a corner is one cardinal step from a seat. It is **never** used for any heal rate.
* **FP (the 4 footprint tiles).** A bot standing on a footprint tile is orthogonally
  adjacent to another footprint tile and could heal. Measured: **max 1 on-footprint
  builder, in 4 of 85 CAD games** — it essentially never happens and changes nothing.
  Included in the seat-turn ledger (`H_LOOSE = ORTH8 ∪ FP`) purely to stay
  bit-comparable with the published census.

Rings are expanded from the four footprint tiles read out of `map.cores` in the replay
binary. **No corpus distance column is involved**, so the known `d2` NW-corner
contamination cannot reach these numbers. Wall and out-of-bounds tiles are excluded, so
a core in a map corner yields a truncated collar: **(orth 8, cheb 12) in 2,734 of 2,890
game-sides; (orth 4, cheb 5) in 156** (2.7–8% of games per opponent, evenly spread —
maps are symmetric, so both sides are truncated together and no opponent comparison is
biased by it).

**Occupancy is counted as DISTINCT SEATS, not bots**, so co-occupation cannot inflate
it. (Two builders are never observed sharing a tile anyway.)

---

## 3. Method

`collar_decode.py` is a **two-sided derivative of the validated
`docs/research/scripts/seat-census-2026-08-09/seat_decode.py`**, itself derived from the
preserved `side-lane-2026-08-09/bb_decode.py`. **The event-decoding core is unchanged.**
Three things were changed and only these:

1. **`decode(path, side_team)` is run twice per replay** — once with our team index from
   `join.tsv`, once with the opponent's. Every "us"-relative quantity becomes
   "this-side"-relative. Rows carry `side ∈ {US, THEM}`.
2. **Symmetric truncation.** The original stopped the round loop when *our* core died;
   this one stops when **either** core is removed, so the US and THEM rows for a file
   cover identical rounds and are directly comparable.
3. **Three explicit rings** (§2) instead of one, and distinct-seat counting.
   The original's idle-supply BFS is retained but **off by default** (`--bfs`) — this
   question does not need it and it dominated runtime.

**Heals are measured as `builderHeal` events (Update field 15) whose target tile is on
the healing team's own core footprint.** This is the definition the requester asked for:
a heal *landing on their core*, not general heal activity anywhere on the map. The
distinction is load-bearing and the two diverge sharply — see §6.

The known traps are handled as in the parent decoder: `placeEntity` re-emission on
gunner rotate is guarded (a build is the **first** `placeEntity` for an entity id);
`updateHp.delta` is decoded as a **64-bit two's-complement varint** via `s64()`, and
**both signs are observed** (§4).

```bash
.venv/bin/python docs/research/scripts/collar-heal-2026-08-09/collar_decode.py \
    <outdir> corpus/join.tsv @<frozen-file-list>
.venv/bin/python docs/research/scripts/collar-heal-2026-08-09/analyse.py \
    <outdir> corpus/join.tsv
```

---

## 4. VALIDATION — the published census reproduces to the digit

`analyse.py` §A recomputes the headline cells of
`docs/research/heal-seat-census-2026-08-09.md` (US side, CAD games where our core was
destroyed, siege window = first enemy turret shot on our footprint → end).

| cell | published | **this decoder** |
| --- | ---: | ---: |
| CAD files | 85 | **85** ✓ |
| loss games | 54 | **54** ✓ |
| siege-rounds | 19,393 | **19,393** ✓ |
| healers / round, mean | 1.10 | **1.10** ✓ |
| healers / round, median | 0 | **0** ✓ |
| share of rounds with 0 healers | 56.7% | **56.7%** ✓ |
| no-damage rounds, n / mean | 12,388 / 0.45 | **12,388 / 0.45** ✓ |
| damage rounds, n / mean | 7,005 / 2.24 | **7,005 / 2.24** ✓ |
| incoming HP/rd (window / damage rounds) | 5.67 / 15.70 | **5.67 / 15.70** ✓ |
| terminal-25 n / healers / staffed / incoming | 1,350 / 1.99 / 2.22 / 18.79 | **1,350 / 1.99 / 2.22 / 18.79** ✓ |
| seat-turn ledger n | 30,109 | **30,109** ✓ |
| ledger: healed / walked / other / idle | 70.5 / 17.2 / 2.6 / 9.7 | **70.5 / 17.2 / 2.6 / 9.7** ✓ |
| max on-footprint builders | 1, in 4 of 85 games | **1, in 4 of 85** ✓ |

**Every cell matches.** The decoder reproduces a known cell, so its unknown cells are
usable.

**One definitional correction found while reproducing.** The published "54 loss games"
is *games in which our core was destroyed*, **not** `join.tsv.won == 0`. Using `won == 0`
gives **58** games and **23,353** siege-rounds and reproduces nothing (healers 1.05,
share-0 59.7%). The 4-game gap is CAD games we lost on the **titanium tiebreak** with our
core still standing. The published doc's own arithmetic confirms this reading
(54 core-death losses + 18 tiebreaks + 10 wins + 3 no-window = 85). **This is a note for
the next session, not an error in the published document** — but "loss" is ambiguous in
this corpus and the two readings differ by 20% of the round count.

### Signal cross-checks (an exact zero is a bug signature first)

* **HP stream, both signs present.** CAD/US: 27,704 core-heal events, **+107,878 heal
  HP**, ratio `heal_HP / (4 × events)` = **0.9735** (published 0.9750; the shortfall is
  heals capped at max HP), against **−135,446 damage HP**. THEM-side ratios by opponent
  run 0.85–1.00 — **all ≤ 1.00 and none zero**, so the two's-complement decode is right
  on both sides.
* **The heal path is cross-checked against the HP path for every opponent**
  (§1 "share of core damage healed back" is computed from the independent
  `updateHp` stream, not from event counts). For Ouroboros: 2,342 events →
  9,305 HP recovered against 17,335 taken. **The event count and the HP stream agree,
  so neither is a phantom.**
* **Invariant `healers ≤ seats_at_start + born`: 8 violations in 1,443,480 rows
  (0.0006%)** — 6 US, 2 THEM — matching the published 6-in-682,011 (0.0009%). Almost
  certainly launcher-thrown-then-healed within a round.
* **Genuine zeros exist and are not decoder failures.** `The Bisons` THEM = **0.0 core
  heals across 35 games** while its collar is occupied on 40.2% of rounds; `Banminary`
  THEM = 0.76 heals per 100 HP damage, **3.0% of damage recovered**, on 70 games. These
  are what a real near-zero looks like in this decoder — and **neither Ouroboros nor CAD
  resembles them.**

---

## 5. Per-opponent table — all rounds, all attributed games

ORTH8 seats, start-of-round snapshot. `%rnd≥1` = share of rounds with at least one of
that team's builders on one of its own 8 heal-capable collar seats.

| opponent | side | games | rounds | %rnd≥1 | seats/rd | cheb12/rd | heals/game | heals/100rd | %games≥1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ouroboros** | **THEM** | **105** | **71,836** | **40.7%** | **0.497** | 0.749 | **22.3** | **3.26** | **81%** |
| Ouroboros | US | 105 | 71,836 | 50.9% | 0.777 | 1.036 | 197.9 | 28.93 | 59% |
| **CtrlAltDefeat** | **THEM** | **85** | **43,684** | **39.3%** | **0.546** | 0.755 | **22.3** | **4.34** | **66%** |
| CtrlAltDefeat | US | 85 | 43,684 | 59.4% | 1.224 | 1.591 | 325.9 | 63.42 | 96% |
| Lunds Stallions | THEM | 130 | 67,807 | 14.5% | 0.158 | 0.669 | 9.5 | 1.82 | 65% |
| Lunds Stallions | US | 130 | 67,807 | 71.6% | 1.619 | 1.955 | 485.8 | 93.13 | 95% |
| Kings College Munich | THEM | 115 | 62,271 | 47.2% | 0.605 | 0.833 | 23.4 | 4.32 | 83% |
| Kings College Munich | US | 115 | 62,271 | 63.5% | 1.329 | 1.750 | 327.6 | 60.51 | 91% |
| Team 48 | THEM | 110 | 22,804 | 63.1% | 1.070 | 1.210 | 182.6 | 88.06 | 94% |
| Team 48 | US | 110 | 22,804 | 73.6% | 1.251 | 1.472 | 154.9 | 74.70 | 97% |
| Powerpuff Girls | THEM | 105 | 83,829 | 45.3% | 0.619 | 0.890 | 110.6 | 13.85 | 98% |
| Powerpuff Girls | US | 105 | 83,829 | 63.7% | 1.285 | 1.612 | 492.2 | 61.65 | 66% |
| Leviathan | THEM | 95 | 44,063 | 68.1% | 1.019 | 1.112 | 308.6 | 66.54 | 87% |
| Leviathan | US | 95 | 44,063 | 69.8% | 1.260 | 1.603 | 251.7 | 54.26 | 81% |
| OopsGotYourElo | THEM | 95 | 76,904 | 67.9% | 1.759 | 1.883 | 613.7 | 75.80 | 98% |
| OopsGotYourElo | US | 95 | 76,904 | 69.0% | 1.095 | 1.518 | 213.8 | 26.41 | 61% |
| Memtrace | THEM | 85 | 48,758 | 85.1% | 2.227 | 3.467 | 176.6 | 30.79 | 59% |
| Memtrace | US | 85 | 48,758 | 80.1% | 1.579 | 1.994 | 263.7 | 45.97 | 78% |
| Askar City | THEM | 75 | 25,991 | 84.3% | 2.090 | 2.428 | 509.5 | 147.01 | 95% |
| Askar City | US | 75 | 25,991 | 66.6% | 1.013 | 1.294 | 139.3 | 40.19 | 84% |
| Banminary | THEM | 70 | 20,875 | 26.3% | 0.362 | 0.603 | 3.4 | 1.15 | 24% |
| Banminary | US | 70 | 20,875 | 64.7% | 1.081 | 1.347 | 187.2 | 62.78 | 99% |
| I Stone | THEM | 40 | 23,472 | 38.6% | 0.484 | 0.742 | 27.7 | 4.72 | 20% |
| I Stone | US | 40 | 23,472 | 73.5% | 1.626 | 2.131 | 427.8 | 72.90 | 72% |
| The Bisons | THEM | 35 | 5,969 | 40.2% | 0.546 | 0.985 | **0.0** | **0.00** | **0%** |
| The Bisons | US | 35 | 5,969 | 77.4% | 1.789 | 2.023 | 233.8 | 137.11 | 91% |
| **ALL (1,445 games)** | **THEM** | 1,445 | 721,740 | 52.8% | 0.983 | 1.300 | 180.8 | 36.19 | 75% |
| **ALL (1,445 games)** | **US** | 1,445 | 721,740 | **67.3%** | **1.268** | 1.617 | 287.6 | 57.59 | 82% |

**Read the US rows as the reference column.** Our own collar is staffed on 67.3% of all
rounds at 1.27 seats — **roughly 1.7× the median opponent's occupancy and 3× that of
Ouroboros/CAD.** We are a garrisoning bot playing mostly non-garrisoning opponents.

**Do not compare `heals/100rd` across opponents directly** — it is dominated by how much
core damage each side inflicts, which is a property of the *matchup*, not of the healer.
The damage-normalised column in §1 and §6 is the behavioural measure.

---

## 6. Band split — r0-150 / r151-300 / r301+

All rounds (not window-restricted), THEM side, the decision opponents plus reference:

| opponent | band | rounds | %rnd≥1 | seats/rd | heals/100rd | their coredmg/100rd |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| **Ouroboros** | r0-150 | 15,653 | 45.7% | 0.581 | **13.48** | 103.4 |
| **Ouroboros** | **r151-300** | 14,257 | **37.3%** | **0.430** | **1.08** | **8.0** |
| **Ouroboros** | r301+ | 41,926 | 39.9% | 0.489 | **0.19** | **0.0** |
| **CtrlAltDefeat** | r0-150 | 12,759 | 39.6% | 0.575 | **9.16** | 99.0 |
| **CtrlAltDefeat** | **r151-300** | 10,013 | **38.7%** | **0.462** | **5.28** | **47.8** |
| **CtrlAltDefeat** | r301+ | 20,912 | 39.4% | 0.569 | 0.95 | 6.5 |
| US (vs Ouroboros) | r151-300 | 14,257 | 53.5% | 0.795 | 34.64 | 197.4 |
| US (vs CAD) | r151-300 | 10,013 | 54.4% | 1.045 | 62.02 | 353.5 |

**The collar occupancy of both opponents is essentially FLAT across the game** — ~40% of
rounds, ~0.5 seats, from r0 to r1000. **They do not ramp a garrison; they keep a
low-level standing presence.** What collapses after r150 is the *heal rate*, and it
collapses in lockstep with the damage we inflict:

* Ouroboros heals/100HP-damage: **13.04 (r0-150) → 13.54 (r151-300) → n/a (r301+, zero
  damage)**. Constant.
* CAD heals/100HP-damage: **9.26 → 11.06 → 14.64**. Constant-to-rising.

**So neither team stops healing its core. We stop attacking it.** The r301+ ratios for
Ouroboros (557 heals/100HP, 2214% recovery) and Lunds Stallions (312% recovery) are
**divide-by-near-zero artefacts and must not be quoted** — the denominators are 0.0 and
3.0 HP/100rd respectively.

### Garrison vs field healer — the requester's distinction, measured

Share of *all* the team's heal actions that land on its **own core**:

| team | THEM | US (reference, same games) |
| --- | ---: | ---: |
| Team 48 | 98.1% | 99.1% |
| Askar City | 95.1% | 77.1% |
| OopsGotYourElo | 79.6% | 53.9% |
| Leviathan | 72.7% | 83.2% |
| Memtrace | 59.8% | 98.1% |
| **CtrlAltDefeat** | **42.3%** | 74.3% |
| I Stone | 29.9% | 75.8% |
| **Ouroboros** | **22.9%** | 38.3% |
| Lunds Stallions | 17.0% | 80.1% |
| Banminary | **4.4%** | 57.6% |

**This is the column that most sharply separates the two decision opponents.** CAD spends
**42.3%** of its healing on its own core; Ouroboros only **22.9%** — Ouroboros heals a lot
(10,243 heal actions across 105 games) but three quarters of it lands elsewhere on the
map. **CAD is closer to a garrisoner, Ouroboros closer to a field healer** — the exact
distinction the requester flagged as decision-relevant, and it points the same way as §1.

---

## 7. NON-COVERAGE AND LIMITS

* **Attribution ceiling.** `join.tsv` maps **1,445 of ~6,233** archived replays (23.2%).
  The other ~4,788 are unrated matches and other teams' games — decodable but
  unattributable, so they cannot be assigned to an opponent and are excluded entirely.
  **All 1,445 attributed files were present on disk at freeze and all 1,445 decoded with
  0 errors.**
* **The archive is not a random sample of the field** (corpus trap 4). It is dominated by
  our own games; per-opponent coverage runs 5–130 matches. **Every figure here means
  "against us, in N archived games"** — Ouroboros N=105, CAD N=85. Nothing here licenses
  "team X never does Y" as a general claim about that team.
* **Every opponent number is confounded by our own bot.** Their core-heal *rate* is a
  response to damage *we* inflict. The damage-normalised columns (heals per 100 HP taken,
  share of damage recovered) are the ones that survive this; the per-round rates do not.
  **The r151-300 Ouroboros/CAD gap in §1 is a statement about the matchup, and that is
  precisely why it decides the leg** — but it is not a statement that Ouroboros heals
  less than CAD per unit of pressure. Per unit of pressure it heals slightly *more*.
* **No version stratification.** These 105 Ouroboros / 85 CAD games span whatever
  versions they shipped over the archive's lifetime. `join.tsv.oppver` is dead
  (literal `"None"`), and `league_matches.tsv` at 85.7% coverage was not joined because
  the question did not require it. **If the leg's result disagrees with this doc, an
  opponent version change is an unexcluded explanation.**
* **Positions are start-of-round snapshots.** The engine resolves units sequentially
  within a round, so a seat empty at round start can be taken mid-round. Occupancy is
  therefore a slight **under**count of "was a seat ever occupied this round".
* **`heal_core_ev` counts heal *actions* targeting a footprint tile.** A heal targets a
  tile and heals all friendly entities on it; since a builder essentially never stands on
  the footprint (max 1, in 4 of 85 CAD games), a footprint-targeted heal is a core heal.
  Heals that hit the max-HP cap still emit the event, which is why event counts run
  slightly ahead of HP recovered (ratio 0.85–1.00).
* **I cannot separate "their policy chose not to heal" from "their policy tried and the
  `can_heal()` guard returned False".** Both are policy outcomes, so direction is
  unaffected.
* **`destroy()` emits no Update message** and is invisible to this decoder, as in the
  parent.
* **Truncated collars.** 156 of 2,890 game-sides have a wall/edge-truncated ring
  (orth 4 rather than 8). Maps are symmetric so both sides truncate together; per
  opponent this is 2.7–8% of games and does not bias the US/THEM comparison.

## Provenance

Scripts at `docs/research/scripts/collar-heal-2026-08-09/` — `collar_decode.py`
(md5 `60e56934`), `analyse.py` (md5 `90952fbc`). Derived from, and leaving untouched,
`docs/research/scripts/seat-census-2026-08-09/seat_decode.py`. Outputs
(`collar_rounds.tsv`, 1,443,480 rows, 177 MB; `collar_games.tsv`, 2,890 rows) were left
in the session scratchpad, **not** committed — re-run the two commands in §3 to
regenerate in ~30 s.
