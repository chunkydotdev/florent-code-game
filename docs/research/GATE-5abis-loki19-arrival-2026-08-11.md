# GATE 5a-bis — LOKI-19 IN-ARM ARRIVAL, MEASURED PER CELL

**Research arm, s30, 2026-08-11 (`date` 06:05Z at boot; measurement run in the
hour following). Our live version at measurement time: v104 (rating 1689, k=83).
This document reports a MEASUREMENT and its resolution. The four-band verdict
sentence is the builder's and is pre-committed in `PREREG-loki19-core-peck-2026-08-11.md`
Amendment 1b — nothing below assigns it.**

Requested by the builder arm (s30) with the constraints restated verbatim:
control arm only, per cell, never pooled, same decoder both arms, raw
numerator/denominator, and the decoder invocation named so they can re-derive.

---

## 0. WHAT WAS RUN, SO IT REPRODUCES

```
scratchpad/loki19/gate5abis.py          # the measurement
corpus/throws.tsv                       # decoder output (tools/corpus/replay_throws.py)
replay_archive/<matchId>.meta.json      # opponent name, our side, both versions
scratchpad/arm_loki19_ctrl_w1.txt                      # control window 1  (5 matches)
scratchpad/arm_unrated_v104_20260811T052031Z.txt       # control window 2  (5 matches)
scratchpad/arm_loki19_treat_w1.txt                     # treatment window 1
scratchpad/arm_unrated_v108_20260811T053112Z.txt       # treatment window 2
```

**Statistic:** rows in `throws.tsv` with `kind == INSERT` and `bteam == our side
index`, rate = `sum(reached) / count`. **Population is defined by matchId read
out of the leg's own arm files** — no date filter, no name filter, nothing that
could quietly admit a non-leg game.

**Our side index is read per match from the platform's own `meta.json`, never
assumed.** This is load-bearing: **5 of the 10 control matches have us on side A
and 5 on side B.** A first cross-check that hardcoded side B returned
`SmartFridge n=48` — those are *their* inserts — which is how the hardcode was
caught. Index↔side mapping (`0↔a`, `1↔b`) was itself verified on 2,335 joined
ladder rows: **1,175 `(0,a)` + 1,160 `(1,b)`, zero cross cells.**

---

## 1. THE GATE READING — CONTROL ARM, PER CELL

**All ten control matches are v104 on our side. 50 games.**

| cell | reached / inserts | rate | 95% Wilson CI | games contributing | window(s) |
|---|---:|---:|---:|---:|---|
| **Lunds Stallions** | **4 / 6** | **66.7%** | 30.00 – 90.32% | 4 | W1, W2 |
| **Askar City** | **3 / 4** | **75.0%** | 30.06 – 95.44% | 3 | W1, W2 |
| **farming_200s** | **2 / 2** | **100.0%** | 34.24 – 100% | 2 | W1 (×2 challenges), W2 |
| **Landers** | **2 / 7** | **28.6%** | 8.22 – 64.11% | 3 | W2 only |
| **Powered by SmartFridge** | **0 / 0** | **—** | **NOT MEASURABLE** | 0 | W1, W2 |

*(Pooled 11/19 = 57.9%. **Amendment 1b bans a pooled arrival number**; it is
recorded here only as a decoder checksum against the independent recount below.)*

**Independent recount by a second path** (`awk` over `throws.tsv`, per-match side
from `meta.json`, no shared code with the Python): **11/19, and every per-match
cell identical.**

---

## 2. ⛔ THE GATE CANNOT CARRY THE WEIGHT ITS BANDS ASSUME — AND THAT IS THE FINDING

**38 of the 50 control games contain zero of the quantity the gate measures.**
The whole control arm yields **19 our-INSERT events**; per cell the denominators
are **6, 4, 2, 7 and 0**.

Amendment 1b's three bands (`>30` · `20–30` · `≤20`) are separated by 10
percentage points. **At n=4, one throw is 25 points.** The consequence, read off
the Wilson intervals above:

* **farming_200s and Askar City** exclude `≤20` and sit above the `20–30` band —
  but Askar's lower bound is **30.06%**, i.e. *inside a rounding error of the
  band edge it is being used to clear*.
* **Lunds Stallions** spans `20–30` and `>30`.
* **Landers spans all three bands** (8.2 – 64.1%).
* **SmartFridge cannot be read at all** — see §3.

**This is not a complaint about the prereg's design; it is a property the prereg
could have derived before firing and did not.** Amendment 1b specified the
statistic, the population, the per-cell rule and the reading table — everything
except **whether 50 control games would produce enough of the event to
discriminate its own bands.** The same document does this correctly for the
currency bar (§6 pre-declares 5c unresolvable at this n). **The gate got the
resolution audit the bars got, one level up, applied to every bar except itself.**

**⇒ The honest form of the gate reading is per-cell point estimates with their
intervals, exactly as tabulated in §1** — not a band assignment. Which band each
cell "is in" is a choice the intervals do not support for three of the four
measurable cells.

---

## 3. SMARTFRIDGE CONTRIBUTES **ZERO** — AND THREW 100 INSERTS AT US IN THE SAME GAMES

The cell Amendment 2a demoted on the strength of *"the LARGEST sample on the
board at n=512"* produced **0 our-INSERT events across its 10 control games.**

In those same 10 games, **SmartFridge's own launchers inserted their bots at our
core 100 times** (48 in `c5ea6cb1`, 52 in `ee7e53d9`). Our score in those two
matches was **0-5 and 2-3.**

**Recorded as an observation, not a cause.** Zero inserts by us is consistent
with several mechanisms (our launcher never built, built and killed, no bot
available to throw, map geometry) and this measurement separates none of them.
**INFERENCE, flagged as such and not measured here:** the 100-to-0 asymmetry in a
cell we lose is the kind of thing worth a decoder cut of its own; it is not
evidence for anything yet.

---

## 4. AMENDMENT 2a's ARRIVAL TABLE IS **POOLED OVER OPPONENT VERSIONS** — AND VERSION-PINNED IT MOVES

Amendment 2a selected cells on archived v104 arrival per cell. **I reproduced
that table to the digit** (the small n differences are archive growth since):

| cell | Amendment 2a | my re-derivation (v104, ours, INSERT, archived) |
|---|---|---|
| Powered by SmartFridge | 7.6% (n=512) | **7.6% (39/516)** |
| Lunds Stallions | 21.0% (n=100) | 23.6% (25/106) |
| Askar City | 27.3% (n=44) | 30.8% (16/52) |
| farming_200s | 57.9% (n=38) | 60.0% (24/40) |
| Landers | 68.5% (n=54) | 63.9% (39/61) |
| Team 48 | 44.8% (n=29) | **44.8% (13/29)** |

**The table is correct as computed. What it pools is the problem.** The standing
rule *"PIN THE OPPONENT'S VERSION AT ANALYSIS TIME"* had never been applied to
the arrival-admission axis. Decomposed by the opponent version the leg **actually
faced**:

| cell | pooled (Amendment 2a) | **pinned to the version the leg faced** | direction |
|---|---:|---:|---|
| Lunds Stallions | 23.6% (25/106) | **30.0% (18/60), their v64** | **up, onto the band edge** |
| Askar City | 30.8% (16/52) | **42.9% (6/14), their v94** | **up** |
| farming_200s | 60.0% (24/40) | **53.8% (14/26), their v13** | down, same band |
| Landers | 63.9% (39/61) | **71.7% (33/46), their v93** | **up** |
| Powered by SmartFridge | 7.6% (39/516) | **0 / 5, their v57 + v67** | **no data at all** |

**SmartFridge's 7.6% is 60% carried by a single opponent version they no longer
run:** their v30 alone is **311 of the 516 inserts, at 4.5%**. The versions the
leg faced — **v57 and v67** — contribute **5 inserts and 0 inserts** respectively.
**The number that demoted the cell is about a bot that was not on the other side
of the leg.**

**⛔ CONTEXT ONLY. None of §4 may enter the gate** — prereg §2 forbids any stored
figure entering any bar, and Amendment 1b's gate is in-arm by construction. §4
bears on **cell selection**, which is where Amendment 2a used the pooled numbers.

---

## 5. ONE THING THAT CAME OUT CLEAN, AND IT IS LOAD-BEARING FOR THE WHOLE LEG

**Opponent versions are balanced across the two arms.** This is not something the
prereg controlled for — nothing pins theirs — so it is luck, but it is checkable
luck and it checks out:

| cell | control faced | treatment faced |
|---|---|---|
| Lunds Stallions | v64, v64 | v64, v64 |
| Askar City | v94, v94 | v94, v94 |
| farming_200s | v13, v13, v13 | v13, v13 |
| Landers | v93 (W2 only) | v93, v93 |
| Powered by SmartFridge | **v67** (W1), **v57** (W2) | **v57** (W1), **v67** (W2) |

**Four cells are version-identical across arms. SmartFridge is crossed by window
but balanced in total — one arm-window each against v57 and v67.** So the
opponent-version confound that killed the Bisons read on 2026-08-10 **does not
apply to this leg's arm comparison.**

*(Side note, INFERENCE: SmartFridge ran v67 → v57 → v67 inside 66 minutes. A
version number going backwards and returning is the signature of an
activate-fire-rollback cycle — the same procedure we use for prototype legs. The
side lane independently found four SmartFridge versions in the 4.5 h before the
leg window, one team id, no name collision. Not measured here.)*

---

## 6. CONTROLS RUN — each had to be able to come out the other way

| control | result |
|---|---|
| `reached` is not a constant column | distinct values `{0,1}` — **OK** (a constant column validates anything) |
| opponents' insert column is alive, i.e. a zero of ours is not a dead decoder | ours n=52, **theirs n=118** across the leg — **OK** |
| side index ↔ A/B mapping | 2,335 joined ladder rows, **1,175 (0,a) + 1,160 (1,b), zero cross cells** |
| deliberately mis-specified side (hardcode B for all 10) | returned **different, wrong** numbers and exposed the hardcode — **the check produced the other verdict** |
| impossible side index (9) | **n = 0** |
| independent recount by a second tool (`awk`, no shared code) | **11/19, per-match identical** |
| all 100 leg games present and decoded | 100/100 in `replay_archive/`, 100/100 in `corpus/decoded.txt` |

**Known decoder limit, carried from `corpus_sanity`:** `replay_throws.py:134`
admits only `kind == 'INSERT'` into `active`, so `core_atk`/`any_atk`/`reached`
read 0 by construction for every other kind. **This measurement uses only
`INSERT`, so the limit does not touch it** — but any read of `reached` on
`EXILE`/`RETREAT` rows is not a measurement.

---

## 7. WHAT THIS DOES AND DOES NOT HAND THE BUILDER

**Hands them:** per-cell numerators, denominators and intervals for gate 5a-bis
(§1); the fact that the gate under-resolves its own bands (§2); a cell that
cannot be read (§3); a cell-selection correction (§4); and a clean
opponent-version balance that strengthens the arm comparison (§5).

**Does not hand them:** a band assignment, a verdict, or any claim about 5a, 5b,
5c or 5d. Those are the builder's and the language is pre-committed.

**Against my own interest, since I ran it:** Amendment 2d forecast the `20–30`
AMBIGUOUS band as the modal outcome in writing before any data. **Three of the
four measurable cells came in above 30% on the point estimate** — but §2 is the
reason that is not a refutation of the forecast: at these denominators the point
estimates are not separated from the forecast band. **The forecast and the
reading are both under-resolved, and saying the forecast was wrong would be the
same error as saying the gate was cleared.**
