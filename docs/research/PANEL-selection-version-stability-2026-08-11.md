# PANEL SELECTION — the axis nobody scored, and a candidate that beats every current cell on it

**Side lane, 2026-08-11 07:0xZ (s30).** Written because SmartFridge accumulated
**five independent defects in one day** and the count, not any single entry,
is the finding. **This is a recommendation with numbers, not a verdict — panel
composition is the builder's call.**

---

## THE DIAGNOSIS: THE CRITERION SELECTED THE CELL IT COULD NOT MEASURE

D13 already replaced *rating proximity* with **"measured mid-range performance
against us"**. That repair is right and it is **not sufficient**, and today shows
why in the sharpest possible way:

**SmartFridge is the MOST mid-range cell on the board — 51.4% game share over 35
v104 games, closer to 50% than any other opponent we play. It scored BEST on the
stated criterion, and it is the cell that produced five defects.**

**Because the criterion never scored VERSION STABILITY.** SmartFridge ran **10
distinct versions in 24 hours.** A cell that re-versions ten times cannot supply
a version-matched control, cannot hold an arrival precondition, and cannot be
pooled with itself.

## THE CONFOUND THAT WOULD HAVE VOIDED THIS RANKING, CHECKED AND DEAD

A team that plays more matches has more chances to be *seen* with more versions,
which would make "churn" an artefact of exposure. **It is not — and the reason is
structural rather than statistical: every team in the league played EXACTLY 87
matches in the last 24 hours.** The correlation could not even be computed
(zero variance in the denominator), which is the strongest possible form of the
answer. **Version counts are directly comparable across teams with no
normalisation.**

## THE TABLE — v104 rated games only, n ≥ 15, versions over the same 24 h window

| opponent | n | our game share | their rating | gap vs 1689 | versions/24h | |
|---|---|---|---|---|---|---|
| **Powered by SmartFridge** | 35 | **51.4%** | 1706 | +17 | **10** | mid-range / **HIGH CHURN** |
| **Focalground** | 35 | **45.7%** | 1699 | **+10** | **1** | **mid-range / STABLE** |
| diverge | 45 | 44.4% | 1688 | −1 | 5 | mid-range / churn |
| farming_200s | 25 | 44.0% | 1722 | +33 | 3 | mid-range / churn |
| kladde chatte tville | 25 | 44.0% | 1674 | −15 | 6 | mid-range / HIGH CHURN |
| Landers | 35 | 57.1% | 1618 | −71 | 2 | mid-range / STABLE |
| Coreflood | 20 | 60.0% | 1674 | −15 | 2 | mid-range / STABLE |
| arsonist duck | 25 | 36.0% | 1689 | +0 | 1 | mid-range / STABLE |
| Askar City | 40 | 65.0% | 1683 | −6 | **7** | mid-range / **HIGH CHURN** |
| Lunds Stallions | — | — | — | — | **6** | **HIGH CHURN** |

## ⭐ THE RECOMMENDATION

**THREE OF THE FIVE CURRENT PANEL CELLS ARE HIGH-CHURN** — SmartFridge 10,
Askar City 7, Lunds Stallions 6. **The panel was never scored on the axis that
decides whether a leg can be read.**

**Focalground is the strongest available replacement and it wins on all three
axes at once:**
* **mid-range: 45.7% over n=35** — resolving, neither floor nor ceiling;
* **STABLE: ONE version in 24 hours**, against SmartFridge's ten;
* **in the reachable band: +10 rating gap**, i.e. a win pays near the top of what
  `target_value.py` prices, unlike Landers at −71.

**arsonist duck (36.0%, 1 version, gap +0)** is the second candidate and is
attractive for the same reasons; it sits nearer the resolving floor.

## LIMITS, STATED

* **Game share is v104-only and rated-only.** That is deliberate — `ourver`
  pinned to the live tree, per the era rider — but it means these are OUR
  matchups, not the field's, and the denominators differ by cell (15–45).
* **Version counts are a 24-hour window** ending 2026-08-11 07:00Z. A team quiet
  today may churn tomorrow; **the check is cheap and should be re-run at panel
  selection time rather than inherited from this document.**
* **Stability is desirable for MEASUREMENT, not a claim about strength.** Sweep
  22 measured that fresh versions are *stronger* (DiD +0.524), so a stable
  opponent is not a weak one — it is a **readable** one.
* **This does not price whether a cell ADMITS a given mechanism.** That is D52d
  and it is per-plank; version stability is a precondition for measuring
  anything at all, not a substitute for the per-mechanism admission check.
