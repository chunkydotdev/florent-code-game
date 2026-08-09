# Revert brackets: version semantics verified, the league reverts constantly, and the real finding is that CtrlAltDefeat owns us on every version

**Side lane, 2026-08-09 13:18 CEST. Closes the spitball item "opponents roll
back too" (2026-08-09 07:2x) — all three of its uncosted directions, plus the
semantics check it demanded. Play-the-players deliverable: measured reaction
latency and revert discipline per team.**

**Version tag:** live v91 = `bots/_v100hf`, tree `4558be91`. Data:
`corpus/league_matches.tsv` (27,073 matches, 2026-08-01..09Z) cross-validated
against `elo_history.tsv` as activation ground truth. Zero replay downloads,
zero platform calls. Analysis: opus subagent (read-only, scratchpad scripts);
the three most load-bearing claims re-verified by hand against the primary
before this doc was written (CAD-vs-us 18/14/61-29/+80.8 exact; 46-of-71
revert count exact; CAD v118 13-match 42-23 cell exact).

## 1. Semantics: VERIFIED — `teamXVersion` is the active submission at match time

The spitball's standing caveat is closed, not assumed away:

- Aligning `league_matches` against our own `elo_history.tsv` activation log
  requires exactly the +2h CEST→Z offset and then agrees on **340/370
  covered matches (91.9%)**. Disagreements are poll staleness (≤1 version,
  at activation boundaries) plus one genuine single-match platform blip
  (2026-08-07T16:02:43Z reports v66 during a firmly-held v67 tenure).
- League-wide, first-appearance monotonicity holds at a 0.1% inversion rate
  (29 inversions in 27,073 matches, all ±1-2 at activation boundaries) —
  the upload-counter reading survives.
- **Detector noise floor, calibrated on ourselves:** single-match reverts
  (`n=1, lat=10min`) carry a **~14% false-positive rate**. Multi-match
  reverts are safe. Every per-team number below inherits this caveat on its
  single-match events only.
- **The expected asymmetry does not exist: we re-activate old versions
  too** (v78→v76→v79; v86→v80 for 6.7h/40 matches; v84→v85→v84). CAD's
  107→116→117→107→117→118 is the same instrument we run.

## 2. Correction to the spitball, and it flips the frame

**"5 of 30 teams non-monotone" is wrong. Measured: 46 of 71 teams with ≥6
matches have ≥1 revert — 502 backward runs league-wide.** Reverting is the
league norm. The informative list is the complement: teams that ship 10+
versions and NEVER revert — Innovex (28 versions), Lorem Ipsum (22),
Hugging Farce (17), Team 48 (15), LingLing40 (14), Kvarnholmen (11),
Hiver01 (10). Those seven either measure before shipping or don't measure at
all; either way their live binary is predictable-forward, never backward.
(One more context row: Powered by SmartFridge reverts **13.7 per 100
matches** — their live binary is effectively a lottery.)

## 3. CtrlAltDefeat's A/B, scored (n=1,044; per-match Elo sd 8.17)

| cell | matches | game win% | Elo/match | verdict |
| --- | ---: | ---: | ---: | --- |
| v107 (pre-revert) | 156 | 47.7% | −0.40 | the "known good" baseline was itself sub-50 |
| v117 (pre-revert) | 69 | 47.0% | −0.53 | **z = −0.23 vs v107 — indistinguishable** |
| v107 (revert window, 2.5h) | 15 | 49.3% | −0.58 | the revert bought nothing |
| v117 (re-shipped) | 28 | 50.0% | +0.08 | "recovery" is noise (z = +0.61 vs itself) |
| **v118** | **13** | **64.6%** | **+4.26** | **z = +2.61 vs v107, +2.54 vs v117 — their only above-noise version** |
| v120 (current, 41+ matches) | 52 | 50.0% | +0.11 | indistinguishable from v107 |

**Their 117→107 revert was unjustified (they cannot tell 47.0% from 47.7%),
and they abandoned v118 — the only version in the band that clears noise —
after 13 matches.** Their measurement loop churns faster than it resolves;
their live binary is close to a random draw from their recent pool.

**The finding that outranks all of the above: they own us regardless.**
Head-to-head, CAD is **14-4 in matches, 61-29 in games, +80.8 Elo taken off
us (+4.49/match)** — at 62-90% game rate on *every* version they fielded
(107, 116, 117, 118, 120), spanning our v55→v83. Whatever CAD does to us is
**invariant across their entire version churn**, while they run 47.8%
against the field. Manipulating their version choice is worth less than
diagnosing the invariant. Standing corpus fact worth joining here: CAD kills
our home builders at only 1.525/1k builder-rounds (7th of 8 in the
attribution table) — they do NOT beat us the way Ouroboros/Lunds do. The
mechanism is unmeasured; this is the next question this deliverable opens.
**ASK-shaped, for the queue: a 3-5 replay mechanism read of CAD-vs-us games,
stratified by their version, precisely because the outcome is
version-invariant.**

## 4. Reaction latency & discipline, the play-the-players table

`p(noise)` = share of reverts fired on ≤2 intervening matches whose Elo sum
is statistically blank (|z| < 1) — high means steerable by variance.

| team | reverts/100m | median latency | median matches tolerated | reverts justified | **p(noise)** |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ouroboros | 0.3 | 10 min | 1 | 3/3 | **0%** |
| Banminary | 1.1 | 35 min | 4 | 12/12 | 25% |
| Powerpuff Girls | 2.3 | 70 min | 7 | 60% | 13% |
| CtrlAltDefeat | 4.9 | 30 min | 3 | 67% | 33% |
| Lunds Stallions | 2.5 | 20 min | 2 | 43% | **50%** |
| *(us, for calibration)* | 2.0 | 15 min | 2 | — | — |

Per-team reads:

- **Lunds Stallions — most manipulable in the league set.** Half their pulls
  fire on ≤2 statistically-blank matches; they three times reverted versions
  that were UP (+11.6, +20.3, +22.0). One lopsided loss inflicted on a fresh
  Lunds ship has a real chance of pushing them back onto an older binary we
  already fingerprint. This is the reaction-latency lever Magnus asked for.
- **Banminary — a damage sponge, never wrong.** 12/12 reverts on genuinely
  negative blocks, but they absorbed ~140 Elo twice over 77-104 matches
  before pulling. A real edge against them pays for **10-17 hours** before
  they react — the widest exploitation window in the set.
- **Powerpuff Girls — slowest trigger, mediocre discipline.** Tolerate
  ~60-match negative blocks; sponge profile, noisier decisions.
- **Ouroboros — not manipulable, and the more actionable fact is that they
  are STATIC: same v8 for 373 matches since 2026-08-06T15:12Z.** A fixed,
  known target with proven-slow re-ship latency; every constant we extract
  from their replays stays valid until they ship, and they almost never do.
- **CtrlAltDefeat — high churn, medium discipline, but see §3: the lever
  that matters with CAD is not their version choice.**

## 5. What this changes

1. **Spitball direction 1 ("read their experiment") works and is now
   scored** — for CAD it shows their A/B resolves nothing at their churn
   rate. Directions 2-3 (revert-as-admission, timing) are delivered as §4.
2. **The spitball's 5-team framing and its "5 of 30" count should be
   retired**; the never-revert seven are the anomaly worth watching.
3. **New top question from the data: the CAD invariant.** 14-4 across five
   of their versions and 28 of ours is not a version effect on either side —
   it is a persistent mechanism, currently unmeasured, worth 3-5 replays.
4. Caveats that bind: single-match reverts carry ~14% FPR; latency floor is
   one 10-min batch; elo_history before 2026-08-07T09:00 local has known
   drift; 31 league rows (08-07 22:02-22:32Z) carry None ratings, coerced
   to 0 and outside every window used above.

## Provenance

Subagent scripts in session scratchpad `cadread/` (lib + q0b-g, q1b/c, q2,
q3, q3b) — methods restated inline above; batch-integrity checks (27,073
unique ids, 1:1 name→id, 0 intra-batch version changes) ran before any
conclusion. Hand-verification by this lane, 13:1x CEST: CAD-vs-us cell,
46-of-71 count, v118 cell — all exact matches against
`corpus/league_matches.tsv`.
