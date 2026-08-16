# THE RATED LADDER CANNOT ADJUDICATE A SHIP OR A SLOT — measured, 2026-08-16

**Research arm, s45. Written 2026-08-16T04:45Z (`date -u`).**
**Live version at write time: HOLDER `v152` "Loki turbo4 (ammo/heal fix)" (x3r0's, uploaded
2026-08-15T17:55:21.217Z), rating 1791–1799, rank #18–19 of 126, 1084–1085 matches.
CONTROL per `PROGRAMME.md` INCUMBENT: `bots/_v223sealrepair` (v140).**
**Surfaces read: `corpus/ladder_games.tsv` (5,415 rows, newest 2026-08-16T03:52:59.561Z),
`fcode status`, `fcode match list --mine --type unrated`, `fcode match list --team`.**

---

## 0. WHAT THIS DOC IS FOR

`PROGRAMME.md` sets `FIXTURE_OF_RECORD: live_unrated` and `X3R0_SLOT_RULE` resolves the
slot on a **local n=1000 screen**. Both designs decline to use the rated ladder as an
adjudicator. **Neither has ever carried a number saying why.** This is that number.

It exists because the temptation is live right now: a teammate's `v152` is reading 56.7%
against our control's 51.9% on the rated tape, and that gap is the sort of thing a lane
reaches for when deciding whether to displace a holder.

---

## 1. THE MEASUREMENT UNIT

The ladder pays `delta = 32 × (S − E)` where `S` = games won / 5 and `E` is the logistic
on the 400 scale (exact, verified to 0.000000 residual across 100 matches by the builder
and 678 by research — `CLAUDE.md`). So **`S − E` per match is the ladder's own payout unit
divided by 32, and it is already adjusted for opponent strength.** Every figure below is
computed on it, per match, from `ourbef` / `oppbef` (the pre-match ratings carried on each
row) — not from a pooled win rate.

**Per-match `S − E` standard deviation, measured:**

| version | matches | sd of (S − E) |
|---|---|---|
| v140 (since 2026-08-14) | 72 | **0.2530** |
| v152 | 30 | **0.2410** |
| **pooled** | 102 | **0.2496** |

The stability across two different bots is the load-bearing part: **sd ≈ 0.25 is a property
of the fixture, not of the arm**, so the power table below is reusable.

**Measured rated cadence:** v140 72 matches / 28.0 h = **2.57/h**; v152 30 matches / 9.7 h =
**3.10/h**. The table uses **3.0 matches/hour**, the optimistic end.

---

## 2. THE POWER TABLE — TWO-ARM RATED A/B, 80% POWER, α = .05, sd = 0.250

| effect (elo/match) | effect (S−E) | matches/arm | games/arm | hours/arm | **DAYS/arm** |
|---|---|---|---|---|---|
| +0.50 | 0.0156 | 4,005 | 20,025 | 1,335 | **55.6** |
| +1.00 | 0.0312 | 1,002 | 5,010 | 334 | **13.9** |
| **+1.62 (observed v152−v140)** | 0.0506 | **382** | 1,910 | 127 | **5.3** |
| +2.00 | 0.0625 | 251 | 1,255 | 84 | **3.5** |
| +3.00 | 0.0938 | 112 | 560 | 37 | **1.6** |
| +5.00 | 0.1562 | 41 | 205 | 14 | **0.6** |
| +8.00 | 0.2500 | 16 | 80 | 5 | **0.2** |

**One-arm "is this above zero":** +1.0 → 501 matches (7.0 days) · +2.0 → 126 (1.8 days) ·
+2.28 → 97 (1.3 days) · +3.0 → 56 (0.8 days) · +5.0 → 21 (0.3 days).

### ⭐ THE RULE THAT FALLS OUT
**The rated ladder resolves effects of roughly +3 elo/match and coarser inside one day, and
nothing finer. A ship or slot decision denominated in rated data is either a multi-day
instrument or it is underpowered.**

⚠ **DEFF is NOT applied here and that is deliberate.** The match-level cluster is dissolved
by construction — the unit of analysis *is* the match, one row per match, so a match cannot
contain more than one member of itself. The **opponent** cluster survives in principle
(several matches per opponent), so these figures are mildly optimistic; the direction of
that error makes the conclusion *stronger*, not weaker, so it is not chased here. Per the
`CLAUDE.md` procedure: clusters enumerated = MATCH (dead, unit of analysis) and OPPONENT
(live, uncorrected, biases toward smaller n).

---

## 3. THE DECODE THAT PROMPTED IT

Per-match, opponent-adjusted, from `ladder_games.ourver` (per-match truth, **not** the
poll-time tag in `elo_history.tsv`):

| version | matches | games | share | expected | **elo/match [95%]** |
|---|---|---|---|---|---|
| **v152** (holder, x3r0's) | 30 | 150 | 56.7% | 49.5% | **+2.28 [−0.48, +5.04]** |
| **v140** (control) | 72 | 360 | 51.9% | 49.9% | **+0.66 [−1.21, +2.53]** |
| **v152 − v140** | — | — | +4.7pp | — | **+1.62 [−1.71, +4.96]**, t = 0.96 |

⇒ **Neither version is established above zero on its own, and they are not distinguishable
from each other.** Both are on-programme on the kill: v152 median kill round **170** over 84
kill-wins, tiebreaks **6 of 150 games (4.0%)**; v140 median **174**, tiebreaks 16/360 (4.4%).

### ⛔ AMENDED — THE CI IS THE SECOND-BEST REASON TO DISBELIEVE THIS ROW. **D18 IS THE FIRST.**
*Added after the side lane audited this doc; the gap was theirs to find, not mine.*

§3 is a **before/after cut on OUR version**, and D18 says that is uninterpretable unless the
opponent's version is held constant or shown to have moved. **This doc adjusts for opponent
RATING and never reports opponent VERSION.** `oppver` is backfilled, so the check runs:
**0 null cells across 104 matches, and 7 of 9 shared opponents shipped a new version across the
v140→v152 boundary** — 0033 (59,60→57) · Coreflood (86,88,89→89) · The Bisons (8,9→9) · diverge
(20,23→25) · gsxWins (39,42,45→46) · lingling_40h (49,52,59,61→61) · team lazy
(226,227,228,230→230). Only HTTP 418 and arsonist duck held.

⇒ **The +1.62 elo/match is UNATTRIBUTABLE on grounds INDEPENDENT of its confidence interval.**
This is the shape that killed the −31.4pp Bisons finding: *"our version got better"* and *"their
version got better"* fit the same data identically.

**And it strengthens §4 rather than softening it.** §4 says the 56.7% is "not evidence either
way"; **D18 supplies a second reason, and unlike the CI this one does not go away with more
matches.** A reader under slot pressure will reach for the point estimate's *direction* once the
CI denies them significance. **D18 denies them the direction too.**

### ⭐ THE INSTABILITY DEMONSTRATED ITSELF INSIDE ONE HOUR
The side lane recomputed this table independently ~1 h later and got **v152 n=32, sd=0.2354,
+2.43 elo/match** against my n=30, sd=0.2410, **+2.28**. Not a disagreement — the archive
advanced two matches between the reads. **The headline moved 6.6% on 6.7% more data.** That is
§2's argument reproducing itself on §3's own numbers, unprompted, within the hour.
*(v140 reproduced exactly: n=72, sd=0.2530.)*

### ⛔ A CLAIM FORMED AND KILLED IN THE SAME PASS — RECORDED SO IT DOES NOT RESURFACE
The raw per-opponent table invites a story: v152 reads **0033 36.0% (n=25), gsxWins 30.0%,
kladde 40.0%, Juusto 20.0%, not adgato 40.0%** against **Coreflood 90%, The Bisons 90%,
team lazy 80%** — i.e. *"we farm the bottom of the band and lose the top."* Those five losing
teams are exactly the highest-payout admissible targets, which makes the story attractive.

**It does not survive the Elo adjustment.** Splitting by whether the opponent's pre-match
rating exceeded ours:

| | matches | share | expected | S−E |
|---|---|---|---|---|
| vs STRONGER | 17 | 52.9% | 45.9% | **+0.0707 ± 0.1239** |
| vs WEAKER/EQUAL | 13 | 61.5% | 54.3% | **+0.0721 ± 0.1214** |
| difference | | | | **−0.0014 ± 0.1734, t = −0.02** |

**The raw table is opponent strength, which Elo already prices.** v140 gives the same null
(t = 0.17). ⇒ **There is no measured strength asymmetry in either version.** The per-opponent
cells are 5–30 games each and cannot support a per-opponent claim at any rate.

---

## 4. CONSEQUENCE FOR THE SLOT

`X3R0_SLOT_RULE` says: on an x3r0 upload, screen **n=1000 locally** and reactivate ours on
≥51.0%. **Section 2 is the justification for that design.** The same question asked of the
rated tape needs 382 matches per arm — **5.3 days per arm, 10.6 days for the pair** — during
which the slot is held by whichever bot is being tested.

⇒ **A slot argument built on "v152 is reading 56.7%" is built on 30 matches with a CI that
spans −0.48 to +5.04 elo/match.** It is not evidence either way. The local screen is the only
instrument that closes in useful time.

### ⛔ RESTATED AS AN EXCLUSION, BECAUSE `CLAUDE.md` REQUIRES IT AND I OWED IT
*"v152 and v140 are not distinguishable"* is a **fail-to-exclude** claim, and the standing rule
is that such a claim must be **restated as an exclusion before any DEFF reasoning is applied to
it** — otherwise the correction launders a weak null into a confident one. The restatement:

> **The 95% CI on v152 − v140 is [−1.71, +4.96] elo/match, so the data EXCLUDE a v152 advantage
> above +4.96 and a v152 deficit below −1.71.**

**+4.96 elo/match is ≈ +149 rating over a 30-match tenure.** ⇒ **the upper bound excludes nothing
operationally interesting** — the interval is consistent with v152 being worth a rank or two and
with it being worth nothing. **The restatement does not weaken the conclusion; it converts a soft
null into a hard statement that the instrument is blind**, which is §2's claim arrived at by a
second route. *(Restatement supplied by the side lane's audit; the gap was real and mine.)*

**State at write time, flagged not acted:** the s44 ruling suspending `X3R0_SLOT_RULE` was
scoped *"FOR TODAY" / "FOR THIS SESSION"* (2026-08-15) and has lapsed by its own wording.
v152 has held ~10.7 h. **No `_x3r0v152` staged in `bots/`, no `SCREEN-v140vs152` in
`docs/prereg/`.** Whether the rule resumes is Magnus's call.

---

## 5. INSTRUMENT RANKING PER WALL-CLOCK HOUR (the reason to spend unrated windows on
validity, not on power)

For the observed +1.62 elo/match ≡ **+5.06pp game share**, two-arm, 80% power:

| fixture | DEFF | games/arm | throughput | **wall-clock/arm** |
|---|---|---|---|---|
| **local corefill** | 0.98 | ~1,500 | fleet, 8 shards parallel | **hours** |
| **live unrated** | 1.834 | ~2,810 | 75 games/h (cap) | **~37 h** |
| **rated ladder** | (n/a, per-match) | 1,910 | ~15 games/h | **~127 h** |

⇒ **Local is ~40× the rated ladder per hour and ~4× unrated.** Unrated's value is **not
power — it is validity**: real opponents' real bots, which is the whole content of the
anti-echo-loop rule. **So unrated windows should buy MECHANISM and SURPRISE against live
teams, never an A/B that local can answer more cheaply.** That is `FIXTURE_OF_RECORD` read
correctly: it is the fixture of record for *confirming a plank against the field*, not the
fixture for *ranking two planks*.

---

## 6. SIDE FINDING — AN OPPONENT IS RUNNING OUR OWN PANEL DESIGN, AT THE CAP, CONTINUOUSLY

While attributing our unrated volume I found 16 overnight matches of `Hugging Farce v41` vs
`OpenSverige v125` — a version of ours inactive since 08-13, so **we did not fire them.**
Reading their team list (`fcode match list --team d667ee5b-…`):

> **Hugging Farce ran 60 unrated matches in under 4 hours**, at a fixed own version **v41**,
> against a rotating **10-team panel, each pinned to a fixed opponent version**: Juusto v10,
> team lazy v225, diverge v20, **OpenSverige v125**, 0033 v56, Jython v135, arsonist duck
> v24, Powered by SmartFridge v35, Lunds Stallions v69, Torsko v67.

That is **the pinned calibration panel this repo specifies in
`SPEC-opponent-pinning-2026-08-13.md`**, run by a 1526-rated team at ~15 matches/hour — the
full rate-limit cap — around the clock.

**AND IT SETTLES AN OPERATIONAL QUESTION WE HAD NOT VERIFIED: the 5-per-20-min limit is
charged to the CHALLENGER.** They fired at 01:02 / 01:28 / 02:03 / 02:43 while we fired at
02:31 / 02:44 — same 20-minute windows, both succeeding. ⇒ **an opponent's campaign against
us costs us none of our budget.**

**Our own overnight usage: ~9 matches in 11 hours ≈ 5% of our cap.** The windows are free and
we are not using them.

⚠ Scope: one team, one 4-hour observation, read off match metadata. It says nothing about
whether their panel is *working*, and `triggeredBy` is the literal string `unrated` for every
row, so the actor is inferred from version-pinning, not read from a field.

---

## PROVENANCE
`corpus/ladder_games.tsv` @ 2026-08-16T04:00Z (5,415 rows, newest event 03:52:59.561Z) ·
`fcode status` and `fcode match list` read live 04:35–04:42Z · local board via
`tools/corefill_status.sh` @ 04:42:36Z · trees diffed directly under `bots/`.
All timestamps from `date -u` in the same shell call.
