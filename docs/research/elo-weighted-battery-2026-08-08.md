# Elo-weighted battery table — 2026-08-08

**Commissioned by:** Magnus, 08:40 local (`docs/coordination.md`, "S16 ELO-WEIGHTED
BATTERY TABLE" row + the 08:40 directive note: *"our goal above all else is to gain
ELO"*). Directly feeds the live hsb/hsd-vs-v74 routing decision (see §6).

**Version tags:** live ladder slot **v74 "mineguard"** (x3r0, `bots/opp_v74` md5
`cb5452e6`, activated 07:15 local) at write time. Our rating/rank from the freshest
row: **1602 @ 355 matches, rank #27/109** (`fcode status`, cross-checked against
`elo_history.tsv`'s last line `2026-08-08T08:48 1602 355 v74 rank #27`). Candidates
under live gate: `_v85hsb` (md5 `33a42f94`) and `_v85hsd` (md5 `4a2aeb50`), both on
the `_v84g` (= our v73 "Eir 7") lineage; their 480-game interleaved bar vs `opp_v74`
is running concurrently with this deliverable (per `docs/coordination.md` 08:41 note
— "nothing waits on nothing").

**Data window:** all 355 ladder matches (`triggeredBy: "ladder"`) pulled via
`.venv/bin/fcode match list --mine --type ladder --json`, paginated by cursor, plus
one incremental refresh mid-task (355th match, Banminary 5-0, landed while this
doc was being written). Three cuts used throughout, chosen and justified below:

- **FULL** — all 355 matches, 2026-08-05T19:46Z → 2026-08-08T06:47Z. Context only;
  contaminated by a rating band (~1150-1300) we no longer play at (§7).
- **LAST100** — the most recent 100 matches, 2026-08-07T14:09Z → 2026-08-08T06:47Z.
  A recency cut independent of our own version history.
- **POST68** — all 82 matches played since our submission version first read ≥68
  (2026-08-07T17:16Z, the "chokewall" ship), → 2026-08-08T06:47Z. A cut aligned to
  *our own lineage* rather than wall-clock, chosen because the class model and
  battery instruments in active use (kladde/ouro/band/cad/orizon probes) were all
  built or frozen in the v67-v69 window — this is the window those instruments are
  actually meant to be gating.

Both recency cuts agree closely (see §4), which is itself a data point: the
picture is not an artifact of window choice.

**Docs consumed:** `docs/research/2026-08-07-fanout/meta-census.md` (baseline
pool-composition weights, §4/§4.1); `kings-college-classification-2026-08-07.md`,
`clankers-classification-2026-08-07.md` + `clankers-noconfound-2026-08-07.md` (incl.
its 2026-08-08 seat-mapping addendum), `orizon-family-2026-08-07.md`,
`viktor5776-classification-2026-08-07.md`, `unclassified-five-2026-08-07.md`,
`v72-bleed-cad-family-2026-08-08.md`, `v72-bleed-nonfamily-2026-08-08.md`,
`v74-mineguard-delta-read-2026-08-08.md`, `v73-production-read-2026-08-08.md`
(Leviathan v25 gunner-rush read), `2026-08-07-fanout/findings/thread7_landers_orizon.md`
and `thread3_kladde_v62.md`; `docs/opponents.md` (pre-taxonomy per-team notes, used
low-confidence only); `HANDOVER.md` (the standing class/probe table, §"The class
model"); `docs/coordination.md` (probe-leg battery composition, the live
hsb/hsd routing thread, the commissioning notes); the probe bots themselves —
`bots/{band,kladde,ouroboros,orizon,cad,clanker,flotte}_probe/main.py` docstrings,
which carry primary-source provenance (exact team name, exact match id) that some
of the narrative docs omit; `elo_history.tsv` and `results.tsv` (read-only,
reconciliation only, no edits). A background research subagent (read-only, same
constraints) did a second independent pass over the classification docs to
cross-check and extend the team→class map; conflicts it found are resolved and
noted inline (§2, §7).

---

## 0. Method

Per-match `eloDelta` for our side is the unit of "Elo stake" throughout — it is a
per-**match** (5-game series) quantity already, computed by the platform's own
`Δ = 32 × (games_won/5 − E)` rule (documented in `HANDOVER.md`'s strategic frame,
confirmed by a 100-match zero-residual fit last session). This already encodes the
rating-difference structure: near-parity opponents produce the biggest swings,
blowouts against far-mismatched opponents move less. No fitted model is used here
beyond what the platform already applies.

For each opponent and each class:

- **n** — match count in the window.
- **win rate** — match win rate (best-of-5 series decided 3+/5).
- **net Δ** — sum of our `eloDelta` (signed; the actual Elo P&L).
- **mean |Δ|** — mean absolute per-match stake (how much is riding on a typical
  match against this opponent/class, win or lose).
- **stake weight** — `frequency_share × mean|Δ|`, the mission's requested
  estimator (frequency × expected |Elo| swing per match). This is a **magnitude**
  measure, not signed — a class we win 100% of the time can still carry a large
  stake weight if it's common and high-variance (see all-in rush, §3). Net Δ is
  reported alongside it precisely so magnitude and direction don't get conflated;
  §4-§6 lean on both.

Two share bases are reported per class: **raw share** (of *all* matches in the
window, classified or not) and **classified share** (of only the matches mapped to
a named class) — the second is what's comparable to the census's own "share of
classified games" column.

## 1. Team → class map used

Built from `meta-census.md` as the base layer, overridden wherever a newer, more
specific doc classifies a team by name (full source-by-team table available in the
subagent transcript this doc draws on; the load-bearing rows are below). Three
notable **conflicts resolved to the newest doc**:

- **0033**: census (v42, 2026-08-07 14:45) called it "point-blank core battery,
  sentinel variant." `v72-bleed-nonfamily-2026-08-08.md` (v43, next day) measured
  73% of shots from d²>13 and an explicit standoff pattern — reclassified
  **economy-first/tiebreak**. Flagging that the version also ticked v42→v43, so
  this may be genuine drift rather than a pure re-read disagreement.
- **OopsGotYourElo** and **gsxWins**: both "unclassified" at census time (§6 of
  that doc); `unclassified-five-2026-08-07.md` decoded both — OopsGotYourElo into
  **economy-first/tiebreak** (highest r1000 rate of any team measured),
  gsxWins into **point-blank/orizon family** (100% core-kill, sentinel-led,
  aim distance 0.0).
- **Banminary**: the background subagent read it as unclassified/thin (only an
  indirect mention as *someone else's* opponent in the archive). Overridden here
  from a primary source it wasn't pointed at: `bots/band_probe/main.py`'s own
  docstring — *"band_probe — a Banminary-style all-in launcher rush... extracted
  from the 1711-rated team 'Banminary', platform match 82bc1754 game 1, which
  core-killed our live bot on round 42"* — an exact-team, exact-match provenance
  record, not an inference. Kept as **all-in rush**.

| Class | Teams (this pool) | Instrument | Confidence |
|---|---|---|---|
| point-blank/orizon family | Orizon, Team 48, Memtrace, Askar City, gsxWins, SingleCore, Leviathan | `orizon_probe` | HIGH (Orizon/Team48/Askar/Memtrace/gsxWins); Leviathan is family-**adjacent** (adjacent-gunner rush, economy-optional — same mechanism, lighter commitment), not a core member |
| creeping gunner picket | Ouroboros, Lunds Stallions, Powerpuff Girls | `ouroboros_probe` | HIGH |
| launcher-insertion/CAD family | CtrlAltDefeat, Kings College Munich | `cad_probe` | HIGH (KCM explicitly verified as "a CtrlAltDefeat-family launcher-ferry bot, byte-for-byte matching opening constants") |
| economy-first/tiebreak | I Stone, 0033, OopsGotYourElo, Viktor5776, ArjunWorks | *none currently* | HIGH (I Stone, 0033, OopsGotYourElo); MEDIUM (Viktor5776, ArjunWorks — thin samples) |
| all-in rush | Banminary, farming_200s, Cookie | `band_probe` | HIGH (Banminary, farming_200s); MEDIUM (Cookie — pre-taxonomy read) |
| patient grind (kladde/standoff) | kladde chatte tville (och oss) | `kladde_probe` | HIGH, but n=2 in every recent window — cannot be load-bearing alone (§7) |
| patient grind (melee, ungated) | Jacobs Code, Landers, Coreflood | *none currently* | MEDIUM-HIGH |
| heal-tank siege | Clankers | `clanker_probe` (built, **not yet frozen/gated**) | HIGH classification, ZERO current battery weight |
| strangle/chip-siege | The Flotte Experience | `flotte_probe` (**dropped from current S14-S16 gates**) | HIGH classification, ZERO current battery weight |
| UNCLASSIFIED | Troupe, Kleos, 1337, StarTrekker, vjg, Albert And Einstein, The Bisons, S, TKB, Git Glam, Klarum, Prompt Engineers Anonymous, Kvarnholmen, "the one piece", PromptNPray, Bean counters, Tyvrets, Oresund Overflow, Innovex, Mimercraft, Atlas | — | genuinely absent from every doc searched |
| non-functional | arsonist duck | — | compile-error auto-forfeit, not a strategy |

Classified coverage of the actual pairing pool: **66.8% of FULL, 99.0% of
LAST100, 98.8% of POST68** — the reclassifications above (mainly 0033/
OopsGotYourElo/gsxWins) are most of why current-window coverage is now near-total
versus the census's own 75.1%-classified claim.

## 2. Pairing distribution

### 2.1 Per-opponent, ranked by match count (FULL, n=355)

| Opponent | n | win% | net Δ | mean\|Δ\| | avg our rating | avg opp rating |
|---|---:|---:|---:|---:|---:|---:|
| Leviathan | 21 | 52.4 | −7.8 | 5.85 | 1406 | 1401 |
| Lunds Stallions | 19 | 5.3 | **−165.0** | 9.10 | 1572 | 1585 |
| Ouroboros | 17 | 5.9 | **−159.0** | 9.91 | 1564 | 1586 |
| Powerpuff Girls | 16 | 37.5 | −70.4 | 7.47 | 1554 | 1554 |
| I Stone | 16 | 56.2 | +16.5 | 4.70 | 1555 | 1516 |
| Team 48 | 16 | 62.5 | +48.7 | 7.25 | 1579 | 1602 |
| Askar City | 15 | 93.3 | **+128.5** | 10.23 | 1560 | 1575 |
| 0033 | 14 | 71.4 | +57.7 | 7.40 | 1564 | 1564 |
| Orizon | 13 | 61.5 | +11.7 | 5.91 | 1558 | 1518 |
| CtrlAltDefeat | 10 | **0.0** | **−76.1** | 7.61 | 1591 | 1621 |
| farming_200s | 10 | 90.0 | +48.3 | 6.39 | 1532 | 1512 |
| OopsGotYourElo | 9 | 55.6 | +21.4 | 8.59 | 1582 | 1595 |
| Kings College Munich | 8 | 25.0 | −60.5 | 9.38 | 1586 | 1579 |
| Memtrace | 8 | 100.0 | +56.1 | 7.01 | 1553 | 1531 |
| gsxWins | 7 | 85.7 | +55.5 | 7.93 | 1585 | 1649 |
| Banminary | 4 | 100.0 | +62.9 | 15.73 | 1598 | 1667 |
| kladde chatte tville (och oss) | 2 | 0.0 | −15.4 | 7.68 | 1619 | 1734 |
| Clankers | 1 | 0.0 | −6.5 | 6.48 | 1568 | 1636 |

(Full 48-opponent table, incl. every extinct/low-rating-band name, lives in the
session scratchpad; the above is every opponent that appears in either recency
window plus the two other 8+-match FULL entries for context.)

### 2.2 Per-class (all three windows)

| Class | FULL n / share | LAST100 n / share | POST68 n / share |
|---|---|---|---|
| point-blank/orizon family | 87 / 36.7% cls | 29 / 29.3% cls | 25 / 30.9% cls |
| creeping gunner picket | 52 / 21.9% cls | 20 / 20.2% cls | 14 / 17.3% cls |
| economy-first/tiebreak | 45 / 19.0% cls | 21 / 21.2% cls | 17 / 21.0% cls |
| launcher-insertion/CAD family | 18 / 7.6% cls | 15 / 15.2% cls | 13 / 16.0% cls |
| all-in rush | 21 / 8.9% cls | 7 / 7.1% cls | 5 / 6.2% cls |
| patient grind (kladde) | 2 / 0.8% cls | 2 / 2.0% cls | 2 / 2.5% cls |
| patient grind (melee, ungated) | 10 / 4.2% cls | 4 / 4.0% cls | 4 / 4.9% cls |
| heal-tank siege | 1 / 0.4% cls | 1 / 1.0% cls | 1 / 1.2% cls |
| strangle/chip-siege | 1 / 0.4% cls | 0 | 0 |
| UNCLASSIFIED + non-functional | 118 / 33.2% raw | 1 / 1.0% raw | 1 / 1.2% raw |

CAD-family's share **doubles** from FULL (7.6%) to POST68 (16.0%) — CtrlAltDefeat
and KCM are both recent/current-rating-band opponents (avg our rating 1586-1591),
not a legacy artifact.

## 3. Elo exchange and expected-Elo weight per class

POST68 is the primary table (aligned to the live instrument set, §0); LAST100
shown alongside as the recency cross-check.

### POST68 (n=82, 98.8% classified)

| Class | n | win% | net Δ | mean\|Δ\| | stake weight (% of classified stake) |
|---|---:|---:|---:|---:|---:|
| point-blank/orizon family | 25 | 76.0 | **+105.5** | 7.68 | **25.7%** |
| economy-first/tiebreak | 17 | 70.6 | +56.0 | 6.03 | 23.5% |
| creeping gunner picket | 14 | **7.1** | **−102.7** | 7.67 | 18.2% |
| launcher-insertion/CAD family | 13 | 15.4 | **−88.0** | 7.89 | 17.4% |
| all-in rush | 5 | 100.0 | +63.3 | 12.66 | 10.7% |
| patient grind (kladde) | 2 | 0.0 | −15.4 | 7.68 | 2.6% |
| patient grind (melee, ungated) | 4 | 25.0 | +5.5 | 2.06 | 0.9% |
| heal-tank siege | 1 | 0.0 | −6.5 | 6.48 | 1.1% |

### LAST100 (n=100, 99.0% classified) — cross-check

| Class | n | win% | net Δ | stake weight |
|---|---:|---:|---:|---:|
| point-blank/orizon family | 29 | 79.3 | +149.9 | 26.6% |
| economy-first/tiebreak | 21 | 71.4 | +72.5 | 21.6% |
| creeping gunner picket | 20 | 15.0 | −130.4 | 19.4% |
| launcher-insertion/CAD family | 15 | 13.3 | −112.2 | 17.2% |
| all-in rush | 7 | 100.0 | +85.7 | 11.6% |
| patient grind (kladde) | 2 | 0.0 | −15.4 | 2.1% |
| others | 5 | mixed | +4.0 | 1.6% |

The two windows agree closely on both ranking and magnitude — not a
window-selection artifact.

**Headline number:** creeping-gunner-picket and CAD-family together account for
**−190.7 net Elo over 27 matches (33% of POST68) at a combined ~11% win rate.**
Point-blank/orizon and economy-first together earn back **+161.5 over 42 matches
(51%) at ~74%.** All-in-rush adds another clean +63.3 (small n=5, flagged). The
account is close to balanced in raw match count between "classes we're crushing"
and "classes crushing us" — but the two losing classes are exactly the two most
volatile and least-instrumented ones (§5-6).

## 4. Comparison: census pool-mix weights vs. Elo-weighted

Census basis: `meta-census.md` §4, "share of classified games," 300-game window,
2026-08-07 ~14:45, our v53-v64. Elo basis: POST68 classified share (§2.2) and
stake weight (§3), same table, one day later.

| Class | Census (classified share) | Elo classified share (POST68) | Elo stake weight (POST68) | Net Δ (POST68) |
|---|---:|---:|---:|---:|
| Point-blank/orizon family | **44.3%** (#1) | 30.9% (#1) | 25.7% (#1) | +105.5 |
| Creeping gunner picket | **35.6%** (#2) | 17.3% (#3) | 18.2% (#3/4) | **−102.7** |
| Launcher-insertion/CAD family | **0%** (not a category — both member teams "unclassified") | 16.0% (#4) | 17.4% (#3/4) | **−88.0** |
| Economy-first/tiebreak | 8.9% (tied #3) | **21.0% (#2)** | 23.5% (#2) | +56.0 |
| All-in rush | 8.9% (tied #3) | 6.2% (#5) | 10.7% (#5) | +63.3 |
| Patient grind (melee) | 2.3% (#5) | 4.9%/2.5% combined (#6) | ~3.5% combined | −9.9 |

**Does the ordering change? Yes, in two places, one of them a full class
appearing from nowhere:**

1. **CAD-family enters the top tier from a standing start of zero.** It wasn't a
   census category at all — CtrlAltDefeat and Kings College Munich were both
   sitting in the census's own 24.9%-unclassified bucket on 2026-08-07. One day
   and two classification docs later, this class is tied for **#3 by Elo weight**
   and is our **#2 net-Elo bleeder** (−88.0, second only to creeping-picket). A
   pool-composition battery literally could not have weighted this class, because
   its own method (classify by decoded replay) hadn't reached these two teams yet.
2. **Economy-first/tiebreak jumps from a tied-for-third 8.9% to a clear #2 at
   21-23.5%.** This is mostly the OopsGotYourElo and 0033 reclassifications
   (§1) — both substantial-volume, high-win-rate opponents that were either
   unclassified or misclassified at census time. It is a *good* reorder for us
   (this class pays, doesn't cost), but it means the battery's current complete
   absence of an economy-first/tiebreak instrument (no I-Stone-style probe exists)
   is now a bigger blind spot than the census suggested, even though the risk
   direction is "we might get complacent" rather than "we're bleeding here."
3. **Creeping gunner picket drops from a dominant #2 (35.6%) to #3 (17.3-18.2%)**
   — not because it matters less (it's still, by net Elo, our **single worst
   class**), but because it's a smaller *share* of what we now play. Its
   per-match stakes and loss rate are unchanged from the census era; only its
   pairing frequency fell. Weight-by-share and weight-by-damage diverge sharply
   here — see §6.

Point-blank/orizon family keeps its #1 rank in every framing, but its census-era
"nearly half of everything we play" framing (44.3%) is now overstated by roughly a
third against current pairing reality (25.7-30.9%).

## 5. Mapping onto the probe legs actually used in batteries

The live guard battery for the hsb/hsd routing decision (per `docs/coordination.md`
08:17, and `results.tsv`'s `_v85hsb-bar` row) is a 4-leg set: **kladde_probe /
ouroboros_probe / band_probe / cad_probe**, each compared in-batch against v74
holder baseline. Absolute scores at write time: **kladde 85.0 (baseline 75.0, +10.0)
/ ouro 93.3 (81.7, +11.7) / band 95.0 (91.7, +3.3) / cad 61.7 (60.0, +1.7).**
Mapping each onto its wild class:

| Leg | Wild class | Probe score | Wild win rate (POST68) | Gap | Read |
|---|---|---:|---:|---:|---|
| `ouroboros_probe` | creeping gunner picket | 93.3% | **7.1%** | **86.2 pts** | **SEVERELY OVER-CONFIDENT.** This is the single biggest calibration gap found. The leg both hsb and hsd score best on is testing a regime the wild opponents (Lunds/Ouroboros/Powerpuff) apparently don't present, or present in a form the probe doesn't reproduce. A near-perfect probe score is currently buying false confidence about our #1-or-2 real Elo bleed. |
| `cad_probe` | launcher-insertion/CAD family | 61.7% | 15.4% | 46.3 pts | Over-confident, but *honestly* so — 61.7% ("barely clearing," per the tape's own framing) is the weakest of the four legs, which at least points the right direction. Real stakes (17.4% weight, −88.0 net) are essentially tied with creeping-picket, yet the leg's own delta over baseline (+1.7pp) is the smallest of the four — it is being read as "solved-ish" when it's arguably our co-#1 open problem. |
| `kladde_probe` | patient grind (kladde/standoff) | 85.0% | 0.0% | 85 pts | Directionally consistent with the ouro finding but **n=2** in POST68 — cannot be claimed as a validated gap, only flagged as consistent with one. |
| `band_probe` | all-in rush | 95.0% | 100.0% | −5 pts (probe *harder* than wild) | **Well-calibrated.** This is the one leg where probe and wild reality agree; appropriately weighted, no correction needed. |

**Legs absent from this routing package that real stakes say should be present:**
`orizon_probe` (our #1 class by share and stake, +105.5 net — currently winning,
so its absence from *this* decision is lower-risk, but it's still the single
biggest thing we play and isn't in the field-line citation) and **no economy-first
instrument at all** (our #2 class by share and stake, +56.0 net — a real,
un-gated blind spot, lower urgency only because it currently pays rather than
costs).

**Over-weighted relative to Elo reality:** `ouroboros_probe` (in confidence terms —
its score is being trusted far past what it's shown to predict about the wild
matchup it claims to represent). **Under-weighted relative to Elo reality:**
`cad_probe` (real stakes tied with the picket leg, but its modest delta reads as
a footnote next to ouro's headline number) and, structurally, the complete absence
of any economy-first instrument despite that class now outweighing all-in-rush and
patient-grind combined.

## 6. Routing impact

The live decision is whether `_v85hsb`/`_v85hsd` should replace `v74` "mineguard"
as the ladder-active bot; per the 3-match swap rule Magnus and x3r0 agreed today,
v74 has already met the "free to swap" condition (net −8.7 Elo over its first 9
matches), so the case now turns entirely on whether the field evidence favors a
candidate. The candidates' entire measured field case is the four-leg absolute
score line in §5 (kladde 85.0 / ouro 93.3 / band 95.0 / cad 61.7), read as "all
four legs positive vs. baseline." Under the Elo-weighted view that reading needs
two corrections, one that weakens the case and one that's neutral-to-positive.
**Weakens:** the ouro leg's +11.7pp is the strongest single number in the package,
and it's exactly the leg shown here to have the least demonstrated connection to
the wild matchup (Lunds/Ouroboros/Powerpuff, 7.1% real win rate) it's supposed to
stand in for — so the case should not lean on "the picket problem looks handled"
without a wild-opponent production read to back it up; that read does not yet
exist for hsb/hsd. **Strengthens, conditionally:** cad_probe is the leg most
directly tied to our real #2 Elo bleed (CAD-family, −88.0 net, tied with picket by
stake weight), and a mechanism as general as heal-staffing/convergence
(hsb/hsd's actual content, per `results.tsv`) plausibly transfers to a standoff
siege class the way it does to a picket class — if it does, the modest +1.7pp on
cad_probe is undercounting the real value, because cad_probe was built as an
easier imitation of the family's opening and may not stress the mechanism hsb/hsd
actually changed. **Net effect on the routing package:** don't let the four-leg
average read as "solved across the board" — split it. Band is validated and
low-priority (already winning). Kladde is unvalidated (n=2, can't move the
needle either way). The real swing questions for whether this ship is worth
+/−100 Elo/day are the two classes census never weighted and this package still
under-measures: does hsb/hsd's mechanism generalize to wild Ouroboros/Lunds/
Powerpuff pressure (currently unknown — ouro_probe cannot answer it), and does it
generalize to wild CAD-family pressure (cad_probe's honest-but-small +1.7pp is
the closest thing to an answer, and it's thin). A wild-opponent production read
on whichever candidate ships, targeted at exactly these two classes, is worth
more to the Elo case than another guard-leg rerun.

## 7. Honesty and caveats

- **Rating-band drift is real and large.** 37.7% of FULL-history match volume
  (134/355 matches) is against opponents that appear in FULL but in *neither*
  recency window — every one of them paired with us only while our rating sat in
  the ~1150-1300 band during the first ~36 hours (2026-08-05/06). None of Troupe,
  Kleos, 1337, StarTrekker, vjg, Albert And Einstein, TKB, S, ArjunWorks, and 14
  more have been paired with us since. This is why POST68/LAST100, not FULL, are
  used as the primary basis in §3-§6 — FULL is reported only for context and its
  class shares should not be used for routing.
- **Small-n classes, explicitly flagged, not silently dropped:** patient grind
  (kladde/standoff) sits at **n=2** in every recent window — the 0% win rate and
  −15.4 net Δ are consistent with the wild-vs-probe gap pattern seen elsewhere but
  cannot be claimed as validated on their own. Heal-tank siege (Clankers) is
  **n=1** in every window — reported for completeness, not decision-weight.
  All-in-rush's 100% win rate rests on **n=5** (POST68) / **n=7** (LAST100) — real
  and currently very good, but a small enough sample that "we've solved rush"
  would be overclaiming.
- **A genuine surprise, and it's a *positive* one:** OopsGotYourElo — unclassified
  at census time, still labeled generically here — is now a top-8 opponent by
  match count in both recent windows (7 in LAST100, 6 in POST68) and a clean net
  earner (+15.8 / +17.8), now reclassified into economy-first/tiebreak by
  `unclassified-five-2026-08-07.md`. It was invisible to the census's weighting
  entirely. So was gsxWins (+20.4 net in both windows, now point-blank/orizon
  family). Both reclassifications move volume *out of* "unclassified" and *into*
  classes we're already winning — good news, but it means the census's 24.9%
  unclassified bucket was hiding real signal in both directions, not just risk.
- **Win-rate sensitivity on the stake-weight number, stated plainly:** stake
  weight is a magnitude measure and does not distinguish "large class we're
  losing" from "large class we're winning." All-in-rush's 10.7% stake weight
  (POST68) is driven almost entirely by one high-leverage, high-rated opponent
  (Banminary, avg opp rating 1667 vs our 1598, mean |Δ| 15.7) winning big, not by
  risk — read net Δ alongside stake weight, never stake weight alone, exactly as
  the mission's estimator note asked.
- **Probe-vs-wild gaps (§5) are read-only findings, not verdicts.** This
  deliverable does not and cannot say *why* ouroboros_probe scores so much better
  than the wild picket class performs for us — that needs a production read on
  actual Ouroboros/Lunds/Powerpuff replays under the current or candidate bot,
  which is a builder-arm-scoped or separately-commissioned research item, not
  something this pairing-frequency analysis can resolve.

## 8. Self-checks

- **Delta-sum reconciliation vs. `elo_history.tsv`:** reconstructing our rating
  match-by-match from `ratingBefore + eloDelta` (starting rating 1500, the
  team's actual creation baseline, confirmed by the first-ever match's
  `ratingBefore`) gives a **zero-mismatch chain across all 354 consecutive
  match-to-match transitions** and a final computed rating of **1602.16**, which
  rounds to the platform's live-reported **1602** (`fcode status`, `elo_history.tsv`
  last row) — exact agreement, not approximate. Mid-chain spot check: match #127
  (completing 2026-08-06T16:47Z, just before `elo_history.tsv`'s first logged
  entry) computes to rating 1344.85, matching the log's first entry of **1345** at
  **17:00** the same evening.
- **Match-count totals:** `fcode match list --mine --type ladder` paginated to
  **355 matches**, exactly matching `fcode status`'s "355 matches played" and
  `elo_history.tsv`'s last `matches` column value (355). All match ids unique (no
  duplicate pulls across the 4 pagination pages + 1 refresh).
- **Class-sum reconciliation:** summed per-class net Δ equals the direct sum of
  `our_delta` over the same window in all three cuts (FULL +102.16, LAST100
  +54.82, POST68 +23.40) — checked programmatically, zero residual in all three.
- **Platform reads only:** `match list`/`match info` (unmetered per the shared
  budget rules), no replay downloads, no submissions/activations/arena runs,
  no writes outside this file.
