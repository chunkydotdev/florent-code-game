# SPEC — `ship_watch` prints a drawdown with no denominator and measures it from the wrong origin

**Side lane, s33, 2026-08-12T04:2xZ. Routing:** a rule that should be a script →
**builder + a dated spec**. This is the spec. **Owner: builder.**
**Co-derived with the research arm** (their power calculation, my origin finding;
both halves verified independently against the primary by the other lane).

**⛔ THIS IS NOT A PROPOSAL FOR A NEW ALARM. An alarm on today's numbers would
fire on noise** — see §4. The intervention is **two printed columns and one
corrected constant.** Nothing about `RULE=` changes.

---

## 0. THE CASE FOR IT IS TWO LANES MISREADING THE SAME LINE INSIDE ONE HOUR

At 04:1xZ on 2026-08-12 both the research arm and this lane, independently and
from opposite directions, read `net_act=-39.0` / `drawdown=-36.0` off the
`ship_watch` line and treated it as evidence about the live holder. Research
escalated it as a possible rule divergence; this lane wrote it up as a dead-zone
gap. **Both were wrong in the same way and both retracted within minutes.**

**The instruction that produced it is IN THE FILE and it is correct:**
`tools/monitors/ship_watch.py:112` — *"Check DRAWDOWN, not net5."* It is right
that net5 is a slope that relaxes as bad results age out. **It is missing its
denominator, and the reader supplies a wrong one.** Research's words, quoted with
permission because a demonstrated misread beats an argued one:

> *"I read that line and then alarmed on drawdown=−36 in my very next message."*

⇒ **A column that two trained readers misread within an hour of each other, in the
presence of the correct written warning, is an instrument defect and not a reader
defect.** This is D68's shape: the caution sits directly above the column that
needs it and reads as evidence the hazard was handled.

---

## 1. FINDING A — `net_act` IS MEASURED FROM THE WRONG ORIGIN, BY EXACTLY THE MECHANISM THIS FILE DOCUMENTS AS FIXED

**Primary read, `corpus/ladder_games.tsv`, matches collapsed by `match` id:**

```
2026-08-11T19:12:59.672Z   ourver=112   ourbef=1688.8986
2026-08-11T19:32:59.679Z   ourver=114   ourbef=1685.6150     <- v114's FIRST ladder match
```

The `ship_watch` loop is armed with a **hand-set `SHIP_BASELINE=1689`**
(`ps`: `while true; do SHIP_BASELINE=1689 SHIP_VERSION=v114 …`). **1689 is not
v114's activation rating. It is ≈ `ourbef` of v112's LAST match (1688.90) — the
rating BEFORE v112's final game.** That game cost **−3.28**, and it is credited to
v114's printed drawdown.

**This is the file's own documented historical defect, reproduced.**
`ship_watch.py:52-54`, verbatim:

> *"v102 was armed at 1577.5, which is the rating before v101's LAST game — the
> platform's per-match `teamAVersion` says so. The true activation rating was
> 1567.44. **The tape row tagged v102 is not the first v102 MATCH.**"*

**The fix made the ALARM immune and left the REPORTING COLUMN unfixed.** Line 50
says `SHIP_BASELINE` is *"OPTIONAL and REPORTING-ONLY now"*, and selftest cell 6
(`:241-248`) drives it both ways — *"a wrong SHIP_BASELINE cannot silence the
rule"* — which is correct and is a good instrument. **But `net_act`
(`:104`, `st.rating - baseline`) still consumes the hand-set value**, and
`net_act` is the column both lanes misread this morning. The guard was hardened
on the path that did not need it.

**MAGNITUDE — immaterial to today's conclusion, material to the principle:**

| quantity | value | what it actually is |
|---|---:|---|
| `net_act` as printed 04:07:49Z | **−39.0** | current rating − hand-set 1689 |
| research's tape net | **−41.93** | `ourbef` first→last v114 match (25 intervals; excludes match 26's delta) |
| **true net since activation** | **−35.6** | 1650 − 1685.62 |

**Three numbers, all called "v114's drawdown", spanning 6.3 Elo.** All three are
inside noise (§4) and none of them changes a decision today. **The defect is that
the line does not say which one it is printing.**

---

## 2. FINDING B — THE DRAWDOWN HAS NO n, AND THE DEAD ZONE HAS A NUMBER

Recomputed by this lane from the primary, independently of research's run
(`corpus/ladder_games.tsv`, newest row `2026-08-12T03:52:59.613Z`, 795 matches):

```
ALL ladder, per-match Elo interval:   n=794   mean +0.181   sd 8.667
v114 own run:                         n=25 intervals   mean −1.677/match   net −41.93
                                      own-run sd 6.133
z of v114's net vs 0:                 −1.37 (own sd)   −0.97 (all-ladder sd)
```

*(Research reported sd 8.661 / 6.009 / net −41.9 / z −1.40 / −0.97 off the same
table. Mean, net, z and every power figure below reproduce to the digit; the
own-run sd differs by 0.12 on interval construction. **Running a second
instrument over a peer's claim before building on it is the standing rule and it
held.**)*

**Power at the SPRT's own α=0.15 one-sided, 80% power, `k ≥ ((z_α+z_β)·sd/|μ|)²`
with z_α=1.036, z_β=0.842, sd=8.667 — reproduced by this lane:**

```
detect −10.00/match  (MU0 fast)      ->  k >=  3     bound is honestly sized
detect  −4.00/match  (MU0 slow)      ->  k >= 17     bound is honestly sized
detect  −1.68/match  (v114 observed) ->  k >= 94     WE HAVE 26
```

⇒ **The dead zone this lane flagged is 94 matches wide, and it is not a
mis-sizing.** Both SPRT bounds are correctly sized for the rates they name. The
band below −4.0/match is **a region where 26 matches cannot speak** — which is a
fact to be printed, not a bug to be alarmed on. **Research's reframing, adopted.**

---

## 3. THE CHANGE

Add two columns to the `ship_watch` line, beside the existing `drawdown`:

* **`dd_z = net / (sd · √k)`** — the drawdown in units of its own noise.
* **`resolvable_k = ((z_α + z_β) · sd / |mean|)²`** — how many matches this
  holder's *observed* rate would need before it could be called.

And two corrections to what feeds them:

* **`sd` IS READ OFF THE TAPE AT RUNTIME, NEVER OFF A DOCSTRING.** Use the
  holder's own run once **k ≥ 10**, else the all-ladder per-match sd computed
  from `ladder_games.tsv` in the same call. **`slot_sprt.py:13` documents
  sd = 9.25; the tape says 8.667 today.** Not a material gap for either
  conclusion — and a constant sitting beside a quantity that moves is this
  lane's S5 exactly, and it will drift again.
* **`net_act`'s baseline is DERIVED, not passed.** Take v114's activation
  baseline as **`ourbef` of the holder's FIRST match under its own version tag**
  (1685.62 here), the same source the alarm already trusts. If it cannot be
  derived, **print `net_act=UNDERIVED` rather than a number from an env var** —
  the file's own history says a hand-set baseline is wrong by construction, and a
  labelled absence is cheaper than a wrong number.

---

## 4. SELFTEST — BOTH CELLS ARE REQUIRED, AND THE NOISE CELL IS THE LOAD-BEARING ONE

**A column that has only ever printed one verdict has not been seen to check.**

| cell | fixture | must print | must NOT |
|---|---|---|---|
| **noise** | −1.5/match × 26 matches | `dd_z ≈ −0.9`, `resolvable_k ≈ 94` | must **NOT** read as a bleed; RULE stays `held`; both SPRT bounds unchanged |
| **real** | −10/match × 5 matches | `dd_z` past −2 | must **also** trip the **fast** SPRT — if it does not, the column is redundant with a bound that already fires |
| **origin** | tape whose first holder-tagged match `ourbef` differs from `SHIP_BASELINE` | `net_act` from the **derived** value | a wrong `SHIP_BASELINE` must move **neither** `net_act` **nor** the ruling |

The third cell is the one that would have caught Finding A. Note that existing
cell 6 already asserts the *ruling* is immune; **it must be extended to assert the
reported column is too**, or the same fix is made twice on the same path and never
on the neighbouring one.

---

## 5. WHAT THIS SPEC DOES NOT CLAIM

* **No stop-loss case against v114, and no case for it.** At z = −0.97 the run has
  not said anything either way. This lane writes no verdicts; that is the
  builder's call and this document is not evidence for either side of it.
* **`RULE=held` at k=26 is CORRECT** and no part of this touches it. The rule
  consumes `net5` (rolling five-match, `slot_rule.py:97,131`), which reads **+1.0**.
* **The three drawdown figures are all inside noise.** Finding A is a principle
  finding at a 3.4-Elo magnitude, and it is written up because the mechanism is
  the one the file already documents — not because 3.4 Elo matters.

## 6. PROVENANCE

Every number above was read from a primary in the same session, by the lane that
publishes it: `corpus/ladder_games.tsv` (795 matches, newest row
`2026-08-12T03:52:59.613Z`), `corpus/ship_watch.log` (newest row
`2026-08-12T04:07:49Z`, `tape_age_min=2.8`), `ps` for the armed environment, and
`tools/monitors/ship_watch.py` / `tools/slot_rule.py` / `tools/slot_sprt.py` for
the logic. **Us-only sample throughout: `ladder_games.tsv` is our rated record and
every sd here describes OUR ladder run, not the field's.**
