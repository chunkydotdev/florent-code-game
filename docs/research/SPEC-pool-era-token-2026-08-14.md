# SPEC — `POOL ERA`: make a share declare the pool it was measured in

**2026-08-14, research arm (s42).** Written at the builder's request: *"that check is a
natural `prereg_check` token (`POOL ERA` on any share-carrying line); if you want it
enforced, spec it and I'll build it into the tool alongside the wiring pass."*

**Scope: `tools/prereg_check.py` + one small derivation helper.** Nothing else changes.

---

## 1. THE DEFECT

**Ten maps entered the rated pool on 2026-08-13 between 07:12:59Z and 10:32:59Z** —
`valkyrie · midgard · icefloe · frostgate · auroraveil · glacierkeep · drakkarfjord ·
yulerune · royale · ragnarok`. **They are now 66% of pairings.** An all-time share averages
over a period in which they did not exist:

| segment | all-time | new-pool | **misprice** |
|---|---|---|---|
| `#63` primary {midgard, ragnarok} | 1.6% | 14.6% | **9.1×** |
| SPAWNPOCKET primary {midgard, fjordgate} | 6.5% | 14.4% | **2.2×** |

**A `SEGMENT VALUE CEILING` computed off the all-time tape would have priced `#63` at
0.16pp pooled instead of ~2pp** — a kill on arithmetic that was 9× wrong. The number was
computable at prereg time **and computable wrong from the obvious population**, which is
what makes this a tool problem rather than a diligence problem.

---

## 2. THE TOKEN

Any line carrying a **share, base rate, reference or segment ceiling** must declare the
window its population came from:

```
BASE RATE: 38.5%   BASE RATE SOURCE: ladder_games.tsv, map in {midgard,fjordgate}
POOL ERA: 2026-08-13T07:12:59Z..now  (n=540)
```

`POOL ERA:` accepts either an explicit ISO range, or a named era resolved from the derived
boundary table (§3). **Required iff the document contains any of `BASE RATE:`,
`REFERENCE n:`, `SEGMENT VALUE CEILING:` or a `%`-bearing `BAR:`.**

---

## 3. ⭐ THE BOUNDARY TABLE IS **DERIVED**, NEVER HARDCODED

**This is the load-bearing design decision and it is not stylistic.** A hardcoded list of
pool-change dates is a constant in a tool with no source — precisely the failure this repo
has recorded four times (an interpolated constant in a tool once filtered 30 games and
produced a false accusation). **The next pool change would arrive and the table would be
silently stale, which is the same defect one layer up.**

**Derive boundaries from `corpus/ladder_games.tsv` itself:**

```
POOL EVENT := a window in which >= 3 previously-unseen maps make their first rated
              appearance within 24 hours of each other,
              AND at least MIN_PRIOR_GAMES (500) rated games precede the window.
```

⛔ **THE SECOND CLAUSE IS NOT DECORATION — I SPECIFIED THIS RULE WITHOUT IT AND RAN IT
BEFORE HANDING IT OVER, AND IT PRODUCED A FALSE EVENT.** The first version yielded **two**
events: the real 2026-08-13 one, and **2026-08-05T19:42:43 with 33 maps** — which is not a
pool change at all, it is **the tape's own beginning, where every map is trivially
"previously unseen."** A pool CHANGE requires a pool to change FROM.

**With the clause, run against the live tape (4,920 rated rows):**
```
MIN_PRIOR_GAMES=100 / 500 / 1000  ->  1 event, all three:
    2026-08-13T07:12:59Z   10 maps   prior=4380 games
```
**The verdict is insensitive to the threshold across a 10× range**, which is what makes 500
a defensible choice rather than a fitted one.

⚠ **The `>= 3`, the 24h window and `MIN_PRIOR_GAMES` are the tunable parts and must be
PRINTED in the tool's output, not buried** — a single rare map appearing is not a pool
change, and the check must not fire on one.

⚠ **AND THE GENERAL WARNING THIS EPISODE EARNS: a derived boundary rule needs its
degenerate case driven before it ships.** Mine failed on the most obvious input there is —
the start of the data — and it would have shipped as a silent extra era that split every
whole-history cut in two.

**Emit the derived table on every run** (`POOL ERAS: [pre-2026-08-13] [2026-08-13..now]`),
so a reader can see what the tool believes rather than trusting it.

---

## 4. THE CHECK

| id | rule | verdict |
|---|---|---|
| `POOL_ERA_PRESENT` | the token exists when a share-carrying line does | FAIL if absent |
| `POOL_ERA_SINGLE` | the declared window lies within ONE derived era | FAIL if it spans a boundary |
| `POOL_ERA_SPAN_OK` | a spanning window is legal **only** with `SPANS-POOL-CHANGE: <reason>` | FAIL if spanning and unjustified |
| `POOL_ERA_NONEMPTY` | non-empty value (per the empty-is-absent ruling) | FAIL if blank |

**`SPANS-POOL-CHANGE:` is an escape hatch on purpose and it must stay one.** Some cuts
legitimately span — a whole-history CPU-cost measurement does not care which maps were in
the pool. **The point is never to forbid spanning; it is to make spanning a sentence
somebody wrote rather than a population somebody defaulted to.**

⚠ **`POOL_ERA_SINGLE` needs the window to be MACHINE-READABLE.** If `POOL ERA:` carries a
named era, resolve it; if a free-text range, parse ISO dates; **if neither parses, WARN and
say the check was not computed — never silently pass.** *(The empty-diff precedent: a check
that cannot compute must say so, and per the `--fire` ruling a WARN that nothing re-runs is
a PASS.)*

---

## 5. BOTH-VERDICTS CELLS

| cell | drive | must |
|---|---|---|
| P1 | real prereg text, share line, no `POOL ERA:` | **FAIL**, naming `POOL_ERA_PRESENT` |
| P2 | same + `POOL ERA: 2026-08-13T07:12:59Z..now` | **PASS** |
| P3 | `POOL ERA: 2026-08-01..now` (spans, unjustified) | **FAIL**, naming `POOL_ERA_SINGLE` |
| P4 | P3 + `SPANS-POOL-CHANGE: CPU cost is pool-independent` | **PASS** |
| P5 | `POOL ERA:` present but empty | **FAIL** (empty-is-absent) |
| P6 | `POOL ERA: the recent era` (unparseable) | **WARN**, explicitly "not computed" |
| P7 | derivation on a tape with **one** new map | **no event** — the ≥3 threshold binds |
| P8 | derivation on the live tape | **exactly one event, 2026-08-13** (prior=4380) |
| **P8b** | **derivation with `MIN_PRIOR_GAMES` disabled** | **TWO events — the spurious tape-start cohort reappears.** The cell that proves the clause does anything |
| P9 | derivation on an unreadable tape | **announces it is blind**, never "no events" |

**P7 and P9 are the ones that will be skipped and must not be.** P7 is the only cell
proving the threshold does anything; **P9 is the alarm-that-cannot-tell-it-is-blind trap,
which this repo has produced in at least four forms.**

---

## 6. WHAT THIS DOES NOT DO

* **It does not validate that the population is the RIGHT one** — only that its pool era is
  stated and internally consistent. A correctly-declared but badly-chosen population still
  passes. *(Presence-with-arithmetic-underneath is the strongest form available here, per
  the vocabulary ruling: `POOL_ERA_SINGLE` is the arithmetic that keeps this from being a
  presence-only rule.)*
* **It does not retroactively fix banked numbers.** The `#63` ceiling is corrected in its
  own doc; SPAWNPOCKET's leg is closed and its misprice runs in the understating direction.
* **It does not apply to LOCAL screens**, whose map pool is a property of our own fixture
  config rather than the ladder.
  ✅ **AND THE SEPARATE QUESTION THIS SPEC FIRST FLAGGED IS NOW ANSWERED — CLEAN NEGATIVE,
  the local fixture was updated.** Measured on the shard row files rather than on the
  config:

  | fixture | n | distinct maps | **new-pool share** |
  |---|---|---|---|
  | `SALTREF.tsv` (remote) | 5,400 | 15 | **66.7%** |
  | `SEALFLOOR0R.tsv` (remote) | 5,400 | 15 | **66.7%** |
  | `SEALREPAIRR.tsv` (remote) | 5,400 | 15 | **66.7%** |
  | `V140VS143.tsv` (remote) | 1,000 | 15 | **66.4%** |
  | **RATED LADDER, same era** | 540 | — | **66.0%** |

  **The screen fixture's map pool tracks the ladder's to within a point.** ⇒ **local screens
  are NOT measuring on a stale pool, and the pool-era defect is a LADDER-CUT problem only.**
  *(Recorded as a resolved negative rather than deleted: the question was worth asking, the
  answer is reusable, and a successor should not have to re-ask it.)*

---

## 7. PROVENANCE

Derived numbers in §1 and §3 come from `corpus/ladder_games.tsv` (4,920 rated game rows at
2026-08-14T20:1xZ), computed by the research arm while closing the `#63`
`SEGMENT VALUE CEILING` debt. The pool-change discovery was a by-product of that
computation, not its object.
