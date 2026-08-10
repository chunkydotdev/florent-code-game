# PREREG — PANEL-3: CALIBRATING THE **REACHABLE** BAND

**PROVENANCE: a Magnus directive plus a corpus/archive cut.** Magnus flagged that
the ladder only pairs within ~±60; the research arm measured it on our own
**3,405 ladder games** and on a **1,638-game** record against the resulting band.
**Nothing in `docs/research/tactics/` spoke to this** — it is a property of the
platform's matchmaking, not a tactic.

**Committed before this leg's first challenge.** Body certified at
`git log --diff-filter=A`; any amendment self-certifies with its own hash and may
only ADD (see `PREREG-loki14b`'s lock-cert block for the convention this follows).

## Why PANEL-2 is not simply extended

PANEL-2's methodology is right and **its candidate pool is wrong.**

**Measured: the ladder pairs us within a narrow window.** |gap| ≤ 60 in **81.2%**
of 3,405 games, ≤100 in 94.0%, ≤150 in 97.4%. Since we passed 1600 (530 games)
the **entire** observed range is **−78.1 to +122.3**, and the highest-rated
opponent we have **ever** met is `0033` at gap **+64.1**.

**⇒ the reachable band is `us − 80 … us + 125`.**

All five PANEL-2 cells sit outside it: Banminary −204, OopsGotYourElo −185,
Team 48 −99, gsxWins −97, I Stone −88.

**The argument is EXTERNAL VALIDITY, not mechanics.** Unrated challenges have no
±60 restriction, so reachability does not stop us playing anyone. But **our
rating is produced entirely by games against `us−80…us+125`**, so a panel at −200
measures performance against a population that never touches it.

## ⚠ THE RULE THAT MAKES THIS DIFFERENT FROM PANEL-2, AND IT IS THE WHOLE LESSON

**REACHABLE DOES NOT IMPLY RESOLVING.** `The Bisons` at +32 read **0,0,0,0**
across four D22 windows — a FLOOR, and it is inside the reachable band. A panel
exists to **resolve differences**, not to mirror the ladder.

**ADMISSION IS THE INTERSECTION:**
> a cell is admitted only if it is **in `us−80…us+125`** **AND** its measured
> share on THIS calibration falls in **`[0.20, 0.80]` inclusive**.

**AND NO CELL INHERITS AN ADMISSION VERDICT.** Every number in the candidate
table below is **pooled across all eras and all versions, ours and theirs** —
which is *precisely* D22's failure mode: CtrlAltDefeat read **0.45 pooled but
0.66 against v102**, and the panel was built from the era-mixed figure.
**The table PRIORITISES a pool. It cannot ADMIT a cell.**

## Candidate pool (six), and what each is for

Record from `corpus/meta_join.tsv`, joined per-game on `us_side`:

| candidate | gap | games | win% | why this one |
|---|---:|---:|---:|---|
| **Powered by SmartFridge** | **+5** | **220** | **36.4%** | adjacent, high volume, demonstrably movable, **and it has been scrimmaging us on an 11-minute timer all day** — a live opponent generating fresh data whether we ask or not, **never once in a panel** |
| **0033** | +111 | 60 | 55.0% | **beat us 3–2 at +64 in our most recent meeting**; top of the reachable band, demonstrably moves |
| Askar City | +18 | 120 | 67.5% | adjacent, high end of the band — guards against a panel clustered at one end |
| farming_200s | +35 | 65 | 44.6% | mid-band, near 50% pooled |
| Lunds Stallions | −30 | 197 | 37.6% | below-but-inside, high volume |
| **The Bisons** | +32 | 230 | **21.3%** | **included specifically to RE-DERIVE D22's floor verdict — see below** |

Pooled across the whole reachable band: **723/1,638 = 44.1%**, spanning 36–68%,
so the pool is not clustered. **`team lazy` is excluded: 1/10 is INSUFFICIENT,
not a floor** — the same distinction applied to the LOKI-14b carriers.
`HTTP 418` has zero archived games and is excluded for want of a prior.

## The Bisons: a pre-registered re-derivation of a retired verdict

**D22 retired The Bisons as an inert floor (0,0,0,0) on four windows of ~5 games,
n≈20.** Its 230-game archived record is **21.3% — inside the admission band.**
At a true 21.3%, four consecutive five-game shutouts has probability **≈0.8%** —
unlikely, not impossible, and era-mixed besides.

**Pre-committed readings, so this cannot be settled by preference:**
* measured share **≥ 0.20** ⇒ **D22's floor verdict was a small-sample artefact**
  and The Bisons is admitted. **A cell we retired was retired wrongly**, and that
  is a finding about our method, not about The Bisons.
* measured share **< 0.20** ⇒ **D22 stands, now on a proper denominator**, and
  the 21.3% pooled figure is era-mixing.

## Design

**Per cell, n=25 (5 matches × 5 pinned maps), v104 (the live incumbent), no
activation, zero rated exposure.** Runner: `tools/panel2_cal.sh` with the
PANEL-3 id list. **Rate limit is 5 per 20 minutes, shared** — check
`tools/rate_budget.py` before starting; pausing another runner does not refund
budget it already spent.

**Map axis:** run `tools/map_admits.py` over the pinned maps and **report
per ring-stratum** (D34). Four of the five pinned maps are 12-tile; `jackpot`
clips to 5. **`jackpot` is KEPT** — see `PREREG-loki14b` A8 and the LOKI-16
verdict for why removing it fits the panel to the plank.

**Read-out:** `leg_read.py`, whose per-opponent split and computed MDE now exist.
**Pass the admitted set to `--live-cells` on every subsequent leg** — that is the
input this calibration exists to produce, and it is what stops a leg deriving its
own live-cell denominator from its own outcomes.

## Falsifiers for the exercise itself

1. **If all six candidates land inside `[0.20, 0.80]`, then reachability was not
   the problem either** — the panel axis is exhausted and the failure to resolve
   18pp claims is about effect sizes or seat confounding. **I will write that**
   rather than treating a third panel rebuild as self-justifying.
2. **If fewer than three cells are admitted, the leg does not produce a panel.**
   A two-cell instrument is what D22 named and it is not fixed by being newly
   selected.
3. **A candidate whose measured n falls short of 25 is reported as
   INSUFFICIENT, never as a floor or a ceiling.**

## What this leg cannot do

It measures **no plank** and no plank result may be derived from it. It cannot
resolve anything in the primary currency: at n=25/cell the computed MDE is far
above any plausible effect, and `leg_read.py` prints it.
