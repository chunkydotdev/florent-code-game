# PREREG — PANEL-2 CALIBRATION. Measuring the instrument, not a plank.

**Committed BEFORE the calibration arm's first window.** No treatment: this runs
the **live incumbent v104** against a **new opponent set**, to measure which
cells can actually move before any plank is measured on them.

## Why the instrument is the blocking problem

Two 18pp claims have now failed to resolve on the current panel:
**LOKI-11** (+16.0pp at n=25 -> **+0.0pp** at n=50) and **the v104 ship** (+18.0pp
pooled -> **-7.0pp, p=0.30** as a pre-registered confirmation). Across all pinned
windows the panel decomposes as:

| cell | record | range across 4 windows | verdict |
|---|---|---|---|
| The Bisons | 0/20 then 1/20 | **0** | **FLOOR — inert** |
| Leviathan | 16/20 | **0** (4,4,4,4) | **CEILING — inert** |
| CtrlAltDefeat | 15/20 | 1 | ceiling |
| I Stone | 8/20 | **4** | **live** |
| gsxWins | 6/20 | **3** | **live** |

**Three of five cells are inert constants.** They contribute neither variance nor
information; every currency number this project has produced on this panel is a
read on **I Stone and gsxWins wearing a five-cell denominator.** That is D11
saturation — the defect we diagnosed in the self-authored ARENA — rebuilt into
the live fixture.

**More games on this panel cannot fix it.** A cell with range 0 does not become
informative at n=500.

## The candidate cells, and the trap they were selected to avoid

| team | id | rating | why |
|---|---|---|---|
| OopsGotYourElo | `f61d19c1-600e-457b-861b-dbeb6b3d8691` | 1513 | only cell measured at exactly 0.50 vs v102; **never a 0/5**, 86% of matches in the 1-4 band |
| Team 48 | `48340ad8-701f-4a40-850d-1f3f3d56d8ca` | 1578 | **most era-stable** on the list (0.63 -> 0.60); 94% of 35 matches in band; a top-5 league fast-killer, so it also stresses the rush axis |
| Banminary | `0774b1b2-df40-4cf2-915e-5d5a6133a13a` | 1449 | off-centre, but owns **14 of the corpus's 25 fastest core kills** — diagnostic value no mid-range cell supplies |

**Retained: I Stone, gsxWins** — the only two cells that have ever moved.

**THE SELECTION TRAP, NAMED BECAUSE WE ALREADY FELL IN IT ONCE.** CtrlAltDefeat
reads **0.45 overall but 0.66 on v102** — we picked it from an era-mixed pooled
statistic and got a ceiling. `farming_200s` is the mirror: 0.51 overall, 0.25 on
v102. **Selecting a fixture from a pooled-era number builds an instrument that
cannot move**, and that is exactly how the current panel was built.

## AND THE CANDIDATES' NUMBERS ARE THEMSELVES SUSPECT — which is why this leg exists

**All three candidate figures come from RATED LADDER play, and the ladder cell
demonstrably does not predict the unrated cell:** Leviathan 0.55 ladder -> 0.80
unrated; CtrlAltDefeat 0.60 -> 0.73; The Bisons 0.33 -> 0.07. **A panel built
from unmeasured cells is the mistake that produced the current one.**

**So this leg measures them on the fixture we will actually use, before any
treatment touches them.**

## What is measured, and the bar

**Per cell, v104 only, n=25 (5 matches x 5 pinned maps): `core_kill_share`.**

**A cell is ADMITTED to panel-2 if its measured share is in [0.20, 0.80].**
Outside that band it is a floor or a ceiling and is excluded from the currency
denominator — **it may still be played, but its games do not enter a treatment
comparison.** The Bisons remain on the schedule under exactly this rule: worth
watching, not worth counting.

**No plank is tested here and no plank result may be derived from it.** If a
candidate lands inert, that is the finding and it is cheap — far cheaper than
discovering it inside a treatment leg, which is what happened twice already.

## Falsifier for the exercise itself

**If all three candidates land inside [0.20, 0.80] AND the retained two stay
inside it, then the panel was never the problem** and the failure to resolve
18pp is about effect sizes or about seat confounding instead. **I will write
that** rather than treating a panel rebuild as self-justifying.

## Cost

Zero rated exposure — v104 is the live incumbent, so this arm needs no
activation at all. One window per rotation cycle.
