# ⛔ CORRECTION — `throws.tsv`'s OUTCOME COLUMNS ARE NOT MEASURED FOR `EXILE`
*(builder s43, 2026-08-15. I published a finding off a constant column and it was
wrong. This file exists so nobody repeats it, including me.)*

## THE ERROR
Asked whether we really threw one enemy builder **152 times in a single game**, I
verified the count (**true** — game `77d7e100…_game_1` vs 0033 v57, one victim
bot, rounds 241→996, all 152 border landings) and then read three further columns
off the same rows and reported:

> *"`life: -1` — it NEVER died. `core_atk/any_atk: 0/0` — it never attacked
> anything, ever."*

**Both statements are unsupported.** `tools/corpus/replay_throws.py`'s own
docstring says it plainly:

> *"**Per own-team forward throw ("INSERT")** we record, from the throw until the
> bot dies or is thrown again: `life`, `core_atk`, `any_atk`, `reached`."*

**Those four columns are populated for `INSERT` ONLY.** Measured across 400,000
throw rows:

| kind | n | rows where `life != -1` | distinct `life` values |
|---|---|---|---|
| **INSERT** | 114,972 | **100.0%** | 990 |
| **EXILE** | 243,790 | **0.0%** | **1** |
| RETREAT | 39,455 | 0.0% | 1 |
| UNATTRIB | 1,783 | 0.0% | 1 |

⇒ For an `EXILE` row, `-1/0/0/0` means **NOT APPLICABLE**, never "measured zero."
**I read an unmeasured column as a measurement.** `CLAUDE.md` states the rule in
these words — **a constant column validates anything** — and this session had
already catalogued six instances of the same class in other instruments before I
committed the seventh in my own analysis.

## WHAT I ALSO GOT WRONG IN THE SAME BREATH
I called it *"the first field evidence"* on the crash weapon's field
applicability. **Wrong twice:** not first — **v105 threw 548 times in one game,
all 548 border landings**, and v72/v91 are comparable — and not evidence, because
the lethality column is blind for this throw kind.

## WHAT SURVIVES
* **152 throws, ONE game, ONE victim bot, rounds 241→996** — real, row counts.
* **All 152 landed on border tiles** — real; `border` **is** measured for every
  kind and varies (EXILE 63,100 of 243,790).
* **We won that GAME on `harvesters` at turn 1000 — a DEFEAT under
  `R1000_IS_DEFEAT` — and LOST THE MATCH 2-3** to 0033.

## ⭐ THE FINDING THAT REPLACES IT, AND IT IS LARGER
**We have NO field measurement of whether a border-thrown ENEMY builder dies —
for any version, ever.** `throws.tsv` tracks outcomes only for our FORWARD throws.
⇒ **The surface anyone would reach for to answer `#17`'s open scope question —
*what share of the real field is vulnerable?* — is STRUCTURALLY BLIND to it.**
`#17`'s ≤4.24% field bound has **no corpus check available**; closing it needs a
DECODER CHANGE (track EXILE victims the way INSERT victims are tracked), not a
query. That is a concrete, cheap, and currently-unbuilt instrument.

---

# ⛔ SECOND CORRECTION, SAME TABLE — "ZERO EXILE THROWS ACROSS 115 RATED GAMES" IS FALSE

Relayed into `#51`'s kill, repeated by me to Magnus and into the `#38` brief, and
flagged by the side lane as an unverified relay because **`throws.tsv` has no
version column** — the claim needs a `file → version` join nobody had done.
**I did the join. It does not hold:**

| v140, archived | games | our EXILE throws |
|---|---|---|
| **rated (ladder)** | **200** | **193** |
| unrated | 483 | 180 |

The unrated half (**180**) reproduces the relay **exactly**; the rated half is a
sign flip — **193, not 0.**

## BUT THE CONCLUSION SURVIVES, AND FOR A SHARPER REASON
The throws are not spread across rated play. **They occur in 3 of 200 rated games
(1.5%), and ONE game carries 176 of the 193 (91%).**

```
176  0c73af5c…_game_5      <- 91% of all rated EXILE throws, one game
 12  696e1af2…_game_3
  5  d5e53d97…_game_1
```

⇒ **`#51`'s kill stands on the corrected number**: aiming a loop that fires in
**1.5% of rated games** buys nothing, and the extreme concentration (one game =
91%) is the same pathological signature as the 152-throw and 548-throw games —
**a launcher latching onto a single victim and cycling it, not a weapon being
delivered across the field.** The verdict was right; **the evidence I gave for it
was wrong, and "zero" is a stronger and falser claim than "1.5% of games."**

## THE PATTERN ACROSS BOTH CORRECTIONS
Both errors came from **`throws.tsv`, both from not doing the join myself, and
both landed in a headline I handed to the principal.** The table has three traps
and I hit two of them in one hour:
1. **Outcome columns are populated for `INSERT` only** — `EXILE` reads a constant.
2. **There is no version column** — every version claim needs a `meta_join` join,
   and the surface pooled rated with unrated.
3. `join.tsv` covers only ~3,735 files against `meta_join`'s ~44,230, so a cut
   built on it **understates throw counts by ~10x** and silently misses the
   largest games entirely.
