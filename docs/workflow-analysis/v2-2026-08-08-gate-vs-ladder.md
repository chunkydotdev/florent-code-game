# v2 — Does the local gate predict ladder Elo?

**Date:** 2026-08-08 · **Author:** third session (main dir, not an arm)
**Data:** `results.tsv` + `elo_history.tsv` · **Surfaces touched:** none, read-only
**Method:** `v2_gate_vs_ladder.py` · raw: `v2-raw-output.txt`
**Status: UNANSWERABLE ON THE CURRENT TAPE. Reported as an instrumentation gap.**

---

## Answer

**Cannot be run — and the reason is more basic than the statistics.** I planned
this against ~35 shipped versions. The tape yields **4 joinable ships.**

The join does not exist because the two halves are keyed differently: **gate
rows key on bot directory** (`_v89sh-acceptance`), **ladder rows key on version
number** (`v80`), and the mapping between them survives only where a tape row
happened to write both in prose (`"SHIP — v80 'Eir 9b' LIVE (bots/_v89sh…)"`).

```
ship rows found (version -> bot dir):   9
gate rows with a usable interval:      61
ladder windows with a delta:           37
JOINABLE:                               4
```

| ver | bot dir | gate wr | ± | n | ladder Δ | matches | Elo/match |
|---|---|---|---|---|---|---|---|
| 75 | `_v85hsd` | 0.481 | 4.5pp | 480 | −11.0 | 10 | −1.10 |
| 77 | `_v89sh` | 0.608 | 6.2pp | 240 | +10.0 | 4 | +2.50 |
| 79 | `_v91osb` | 0.642 | 6.2pp | 240 | −42.0 | 6 | −7.00 |
| 80 | `_v89sh` | 0.608 | 6.2pp | 240 | +12.0 | 22 | +0.55 |

Raw r = −0.247 at n=4, t(2) = −0.36. **This number must not be quoted.** Note
also that rows 77 and 80 are the *same bot directory* shipped twice, so the
four points are not four independent ships.

## Why a null here would have been misleading (research arm's critique, adopted)

Even with n=35 the design was unsound. Both variables are noise-dominated:

- **Y** — a window's net Elo has large sampling error; per-match Elo sd is
  **9.25** (measured in v3), so a 5-match window carries SE ≈ 21 Elo against a
  signal of a few Elo.
- **X** — by v1's finding, gate numbers at n=120 carry SE ≈ 4.6pp against
  effects of ~5pp.

Regression dilution: observed r = true r × √(reliability). Measured on the 4
points available, reliability is **0.83 for X but only 0.28 for Y**, giving an
attenuation factor of **0.48** — a true correlation of 0.6 would present as
0.29. **So a null is consistent with "the gate is useless" AND with "the gate
is perfect but both instruments are noisy."** The most consequential study was
the one whose null carried the least information. That pairing was the flaw,
and catching it before publishing a null is the point of the exercise.

## The fix, and it is cheap

Two changes make v2 answerable in ~2 weeks of normal shipping:

1. **Add one field to the ship row: the gate row it was gated on.** A ship row
   already carries version, bot dir, and md5; it does not carry the identifier
   of the leg that authorised it. One column closes the join permanently and
   costs nothing per ship.
2. **Record ladder outcome in GAME SHARE, not match Elo** (research arm). Elo
   is `32 × (games/5 − E)`, so games are the underlying unit — recording game
   share gives ~5× the observations per window and materially raises Y's
   reliability, which is the binding half at 0.28.

Additionally: **exclude or separately model bundle ships.** v83 carried seven
planks, so its "gate number" corresponds to no single change. With v1's power
fix in place, single-plank ships become the norm and this stops being a problem
at source.

## What this says about the folder's own method

The v1 house rule says a process claim gets measured or it does not go in. v2
adds the companion rule, learned by nearly violating it:

> **State what a null would mean before running.** If "no signal" and "signal
> we cannot see" produce the same output, the study is not yet a study.

The credit is the research arm's — they raised the dilution objection before
this ran, which is the second time in one evening that an independent arm
caught a design fault upstream of a published number.

---

## Falsifiable prediction

With change (1) in place, ~15 single-plank ships accumulate within two weeks of
normal cadence, and at reliability ~0.5 on both axes the design can distinguish
"true r ≥ 0.6" from "true r ≈ 0" at n≈15. Until then, **no claim about local
gate → ladder transfer is supported in either direction**, including the
optimistic one everything currently assumes.
