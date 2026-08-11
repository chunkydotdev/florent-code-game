# POST-FIX DRIVE OF `tools/overnight_read.py` AGAINST THE SEVEN KNOWN-ANSWER FIXTURES

**Side lane, s32, 2026-08-11T18:00–18:03Z.** Read-only: the tool was run with
`--dir` against a COPY of the fixture set; `scratchpad/overnight/` was not
written to and no live file was touched.

**Why now:** the seven arms were at 4,611–4,772 of 5,408 (85–88%) at 18:00:14Z
and land ~18:35–18:45Z at the observed rate. The read-out fires on ~38,000 games
within the hour, on a tool whose F1/F2/F3/F5 fixes landed at 16:39Z
(`3f0c343`, `8db0d12`) and **have never been driven to the verdict they must
refuse.** That is this repo's most-repeated defect and the fixtures for it
already existed.

**Provenance of the fixtures.** Seven fixtures with pre-stated expected verdicts
were built during the s31 audit and left in a dead session's scratchpad. **They
still exist** at
`/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/3a0a7134-.../scratchpad/fx/`
and are one tmp sweep from gone. Copied into this session's scratchpad to drive
them. **They belong in `tools/fixtures/` — builder-owned, flagged not done.**

---

## THE HEADLINE, AND IT IS NOT THE ONE I EXPECTED: **THE TOOL IS SOUND FOR TONIGHT'S DATA.**

I went looking for what breaks tonight's read-out and **the live census says
nothing does.** Every finding below is either latent, or has measured
zero exposure on the data now on disk. Recorded in that order deliberately —
the comfortable direction here was to publish four defects before pricing them.

**LIVE WINNER-COLUMN CENSUS, all nine shards, 18:02:50Z:** every row is `T` or
`C` plus one header. **`NOWINNER` = 0 and unparseable = 0 across 37,203 rows.**
Duplicate `(map,seed,seat)` triples run **0.02%–0.35%**, two orders of magnitude
under the 20% refusal.

---

## ⭐ FINDING 1 — **THE NULL RE-CENTRING CANNOT RE-CENTRE ANYTHING, AND WHEN IT FIRES IT PRINTS A FALSE STATEMENT.**
**Status: CONFIRMED by reading, latent tonight. This is the sharpest one.**

`overnight_read.py:205` sets `centre = nul["p"]` when the null is off 50% by
`|z| > 3`, and `:224–225` prints:

    ⇒ BANDS RE-CENTRED ON THE MEASURED NULL (xx.xx%), not on 50%.

**No band is re-centred.** `centre` is assigned at `:205`, compared at `:224`,
printed at `:225`, **and read nowhere else** (`grep centre` returns exactly
those three lines). The verdicts are computed at `:183–184` against a
**hardcoded `0.5`** — and that loop has **already run and printed** by the time
`centre` is assigned, so even a corrected band could not reach them. The
`NEGCTRL` test at `:217` is likewise hardcoded to `0.5`.

⇒ **In the one scenario the branch exists for — a harness measured as biased —
the tool announces it has corrected for the bias and reports verdicts that have
not been corrected.** An alarm that fires is worse than one that cannot, because
its firing is read as an action taken.

**IT CANNOT FIRE TONIGHT** — NULL is 2,328/4,742 = **49.09%**, `z = −1.25`,
against a `|z| > 3` trigger. So this is a latent defect, not a live one, and I
am not asking anyone to touch a tool thirty minutes before it runs.

**WHERE IT CAME FROM, and this is the part worth keeping:** this branch IS the
F3 fix — the repair for *"NULL and NEGCTRL calibrate nothing"*, written at
16:37Z. **The fix for a control that did not act is a control that still does
not act and now says it did.** Same family as D68, inside the repair for it.

## FINDING 2 — F6 IS LIVE AND IT DISABLES TWO GUARDS AT ONCE, NOT ONE
**Status: CONFIRMED by driving. Exposure tonight: low but non-zero.**

`M6_NOHB` (a shard with no heartbeat) is **not refused**. It prints

    n=298/None  PARTIAL nan%   …   VERDICT: NO-INFORMATION

against a docstring that commits to refusing exactly this: *"what is not usable
is a shard whose denominator is unknown."* `status = "NO_HEARTBEAT"` is set at
`:61` and never consulted.

**The half that was not in the s31 write-up:** the truncation guard at `:86` is
gated on `if d["n_hb"] is not None`, so a missing heartbeat **also silently
disables the corrupt-tsv check.** One missing file, two guards off, and a `nan`
printed where the completion percentage goes.

**Tonight:** all nine heartbeats are present and fresh (18:00:09–18:00:14Z). The
exposure is a shard killed between its `.tsv` append and its heartbeat write.

## FINDING 3 — **THE `M5_NOWIN` FIXTURE REFUSES FOR THE WRONG REASON, WHICH MEANS DRIVING IT PROVES NOTHING. THIS ONE IS MINE.**
**Status: CONFIRMED. It is a defect in the fixture set I built.**

`M5_NOWIN` was built to exercise the no-winner path (F7: `overnight.sh:83`
resets `nowin=0` after the resume block, so the 1% abort cannot trip on a
restarted shard, and **the read-out has no no-winner threshold either**).

Driven, it prints:

    ⛔ REFUSED: 210 duplicate rows (42.2%) …

**It never reaches anything to do with no-winner rows.** Its 200 `NOWINNER` rows
repeat `(map,seed,seat)` triples, so the DUPLICATION guard trips first. A reader
running the fixture set sees `M5 → REFUSED` and ticks it.

⇒ **A fixture that produces the right verdict for the wrong reason is worse than
no fixture: it converts an untested path into an apparently tested one.** F7 is
still completely undriven. **The general form, and it is the same standard I
hold other lanes to: a known-answer fixture must assert the REASON, not only the
outcome.**

## FINDING 4 — THE DUPLICATION RATE AND THE WIN RATE ARE COMPUTED ON DIFFERENT POPULATIONS
**Status: CONFIRMED. Exposure tonight: zero, measured.**

`keys` at `:83` is built from **all** rows; `good` at `:103` keeps only `T`/`C`.
So the `dup_pct` that drives a **refusal** has a denominator including rows the
scorer discards. On a shard with many `NOWINNER` rows the percentage inflates
and can refuse data that is fine — which is precisely what `M5` demonstrates,
from the other side.

This is research's R7 from this morning (*numerator and denominator must cover
the same side-set*) on a new surface. **Live exposure is zero: with `NOWINNER`
= 0 the two denominators differ by exactly the one header row** (e.g. NULL
4,743 vs 4,742), and dup% is identical to two decimals on all nine shards.

## FINDING 5 — THE MULTIPLICITY LINE COUNTS CONTROLS AND REFUSED SHARDS AS SCREENED ARMS
**Status: CONFIRMED. Direction: CONSERVATIVE. Live tonight.**

`:228` — `n_arms = sum(1 for k in data if not k.startswith("CAL"))` — counts
every non-CAL shard. Tonight that is **7**, giving `P(≥1 spurious) = 0.30`.
But **NULL and NEGCTRL are calibration cells with pre-registered directions, not
hypotheses under test**; the screened arms are **5** (CAP6, CAP12, GUNAXIS,
ROSTER, BESTFIT) ⇒ the correct figure is **0.23**. It also counts refused
shards, which cannot produce a verdict at all.

**The error is in the safe direction** (it overstates the chance of a spurious
finding) and it is worth one line only because the number is printed as a guard
against over-reading a single escalate.

**Companion inconsistency, same block:** CAL shards are excluded from the
multiplicity count and **still receive full `VERDICT:` lines** in the shard loop,
because `:155` iterates everything. So the read-out will print more
`escalate`/`real negative` lines than the multiplicity sentence is about.

---

## WHAT DRIVING CONFIRMED IS WORKING — a successor should not re-spend this

* **F1 fires.** `M4_ABORTED` now prints `⇒ NOT SCORED. No verdict is printed for
  a refused shard.` and stops. The failure it was written for — declaring rows
  not-games and then scoring them — is closed on the fixture that produced it.
* **F2 fires in both directions.** `M1_DUP150` (35.7%) and `M2_DUP_ALL` (51.7%)
  refuse; the live shards at 0.02–0.35% pass with the warning printed and the
  count attached. **The 20% threshold separates the fixture set from the live
  data by two orders of magnitude** — that is a real margin, not a tuned one.
* **F3's ABSENT branch fires correctly.** With no `NEGCTRL` in the fixture dir
  the tool prints `⚠ NO NEGCTRL DATA — the screen's power is unverified
  tonight.` (The PRESENT branch works too — the live run reads NEGCTRL at
  1,709/4,666 = 36.6%, far outside the band, so the screen has power.)
* **The seat guard fires and its tolerance is right.** `M3_SEATSKEW` (149/0)
  refuses; every live shard is within tolerance.
* **F5 prints.** The multiplicity sentence is there, subject to Finding 5.

---

## THE ONE THING THAT BEARS ON HOW TONIGHT'S OUTPUT IS READ

At the projected `n ≈ 5,400/arm` the band half-width is `1.96 × √(0.25/5400)`
= **±1.33pp**, i.e. 48.67%–51.33%. With **five** screened arms, `P(≥1 spurious
OUTSIDE) = 0.23` — **not** the 0.30 the tool will print.

⇒ **An arm sitting within a few tenths of a percentage point of the band edge is
a coin-flip against the multiplicity, not a result.** This is methodology stated
before the numbers land, and it is deliberately not a verdict — the read-out is
the builder's to run and to call.

**I have NOT reported which arms are where.** The arms are mid-run; reading them
now and acting on it is optional stopping, and the whole design's power argument
assumes the declared `n`.

---

## ROUTING

| finding | route | owner |
|---|---|---|
| 1 (dead re-centring) | flag to builder; `tools/` is theirs. **After tonight's read-out, not before** — it cannot fire tonight and the tool runs in ~30 min | builder |
| 2 (F6, two guards off) | already open in the tool header; this adds the second guard | builder |
| 3 (M5 refuses wrongly) | **mine.** Recorded here; the fixture set must assert reasons, not outcomes | side lane |
| 4 (dup denominator) | flag, zero live exposure, bundle with 2 | builder |
| 5 (multiplicity count) | flag; also the CAL-verdict inconsistency | builder |
| fixtures live only in a dead session's tmp | **commit them to `tools/fixtures/`** — this is the `--selftest` that still does not exist (`grep selftest` → 0 matches) | builder |
