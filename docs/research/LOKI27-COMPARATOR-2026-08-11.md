# ⛔ LOKI-27'S MECHANISM COMPARATOR IS WRONG ON TWO INDEPENDENT AXES, AND BOTH LEG READINGS INVERT WHEN MATCHED

**Research arm, s31, 2026-08-11. Delivered BEFORE the leg read-out.**
**Establishes:** the comparator in `PREREG-loki27-ferryfirst-2026-08-11.md:76` is
presence-conditioned *and* opponent-pooled. **Does not establish:** whether
ferry-first worked — **that is the builder's verdict and this lane does not write
verdicts.**

Commissioned by the side lane, who disclosed that their `+59%` informative band
had been sized off the stored `0.91` in the same message where they warned against
sizing on a stored figure. **The correction exists only because they flagged their
own fault.**

## THE PREREG'S TABLE

| quantity | incumbent (corpus) | prediction if the plank works |
|---|---:|---|
| INSERT (ferry) throws / game | **0.91** | RISES |
| EXILE throws / game | **~9.2** | falls or holds |
| INSERT : EXILE | 1 : 10.1 | shifts toward INSERT |

Treatment arm, builder's decode: **13 INSERTs across 25 leg games = 0.520**,
EXILE **2.40**.

## AXIS 1 — THE DENOMINATOR IS CONDITIONED ON THROW-PRESENCE

```
ALL OPPONENTS   ALL-games denominator      n=5178   INSERT/g 0.670   EXILE/g 6.78
                throw-PRESENT denominator  n=3802   INSERT/g 0.912   EXILE/g 9.24
```

**The stored `0.91 / ~9.2` reproduces to three digits on the throw-present
denominator.** *(That reproduction is also an inadvertent control on this cut: it
says the `tteam` keying here counts the same throws the builder's decode does.)*

**`corpus/throws.tsv` is a per-throw table, so a zero-throw game has no row.**
Dividing by 3,802 conditions the denominator on throw-presence and **inflates any
per-game rate by ~36%.** This is not an unnamed cut that might have been
defensible — **it is a cut that cannot be correct for a rate**, and it is
invisible precisely because the missing rows are zeros.

## AXIS 2 — THE COMPARATOR POOLS OPPONENTS WE THROW FAR MORE AGAINST

Our throws only, per our game, all-games denominator, gap = opponent rating − ours:

| tier | games | INSERT/g | EXILE/g |
|---|---:|---:|---:|
| opp < −100 (much weaker) | 320 | 0.753 | 3.39 |
| opp −100..−25 | 1,659 | 0.687 | 7.53 |
| opp −25..+25 (even) | 1,702 | 0.605 | 7.84 |
| opp +25..+100 | 1,102 | 0.822 | 5.54 |
| opp > +100 (much stronger) | 395 | 0.390 | 5.24 |

**The three leg opponents present in the archive:**

| opponent | games | mean gap | INSERT/g | EXILE/g |
|---|---:|---:|---:|---:|
| 0033 | 105 | +55 | 0.381 | 0.74 |
| Big O | 20 | +182 | 0.350 | 2.65 |
| Leviathan | 295 | −38 | 0.556 | 0.98 |
| **POOLED** | **420** | | **0.502** | **1.00** |

## ⇒ BOTH READINGS INVERT

The treatment's `13/25` uses an **all-games** denominator, so the matched
comparator is **0.502**, not 0.912.

| quantity | vs PREREG comparator | **vs MATCHED comparator** |
|---|---|---|
| INSERT/game = 0.520 | 0.910 → **−43%** — reads as the plank failing its predicted rise | **0.502 → +4%. FLAT.** |
| EXILE/game = 2.40 | 9.20 → **−74%** — reads as an alarm on a quantity the plank does not touch | **1.00 → +140%. EXILE ROSE.** |

**Against these specific opponents we historically exile ~1.0/game, not 9.2.
There is no collapse to explain.** And INSERT did not fall 43%; it moved +4%.

**⇒ THE MECHANISM BAR AS PRINTED CANNOT BE READ. A leg scored against it would
conclude the opposite of what the data says, in BOTH rows.**

## CAVEATS — stated up front, not on request

* **Only 3 of the 5 leg opponents exist in the archive.** `HTTP 418` and `kladde`
  have **zero** archived games. **A 3-of-5 comparator is a scalar standing in for
  a population** — the exact objection this repo raises most often, and it applies
  here.
* **`Big O` is n=20**, and it carries the +182 gap.
* **The archive pools OUR versions** (92.4% v101-or-earlier), so this is *older
  us* against these opponents, not v104. **A version confound running the same
  way as everything else measured today.**
* Restricted to throw-present games the 3-cell comparator reads **1.128 / 2.25**.
  That is **denominator-inconsistent with the treatment** and must not be used
  against it; it is given only to show the spread. **The honest comparator range
  on INSERT is 0.50–1.13 depending on convention. The prereg quoted a point.**
* **`tteam` semantics are assumed** to be the throwing team, keyed against
  `meta_join.us_side`. The three-digit reproduction of the stored figure supports
  the keying but does not independently verify the field's direction.

## THE RULE THIS IS AN INSTANCE OF

**A comparator and a treatment must share a denominator convention, and the
comparator must be cut to the treatment's population.** Neither held here, and
the two faults compounded in the same direction. ⇒ **A read-out should carry the
matched comparator and its spread, never a point.**
