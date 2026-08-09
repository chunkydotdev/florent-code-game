# Is the v90 drift v90-specific? The launcher latch repair, checked in production

**Research arm, session 23, 2026-08-09.** Corpus only. Zero downloads, zero arena.
**Live context:** v90 at **1540 @ 507, rank #34, last-10 3W-7L, −49 from a 1589
peak.** The builder's reversion bar tripped; they are holding v90 on the rule's
second clause (no measured-better candidate exists) and named this as *"the
highest-value open question on the slot… checkable and unchecked."*

v90 = `bots/_v104latch`. Its reason for existing was the **launcher latch defect**:
a destroyed launcher was never replaced, and builders kept entering `launchwait` for
a ghost. The hypothesis to test: **is the repair backfiring — rebuilding launchers
into bad positions?**

---

## 1. The repair fires — hard

Launcher builds after r100, i.e. replacements, which is what the latch repair
enables:

| version | total launchers | after r100 | share |
|---|---|---|---|
| older | 493 | 68 | 13.8% |
| v80-84 | 235 | 28 | 11.9% |
| v85-89 | 58 | 4 | **6.9%** |
| **v90** | 49 | 16 | **32.7%** |

**6.9% → 32.7%, a 4.7× jump.** The repair is not inert.

## 2. But placement is fine — the hypothesis as stated is REFUTED

| version | launcher d²_own p25 | median | p75 | forward% |
|---|---|---|---|---|
| older | 4 | 5 | 10 | 3.9% |
| v85-89 | 5 | 10 | 18 | 3.4% |
| **v90** | 4 | **5** | 13 | 6.1% |

**v90's launchers sit at median d² = 5 from our own core — the long-run baseline,
and *closer* than v85-89's 10 — with only 6.1% forward.** They are rebuilt at home.
**"Rebuilding launchers into bad positions" is not supported.**

## 3. There is a real delta, and it is TIMING, not position

| version | games with a launcher | launchers/game | **median build round** |
|---|---|---|---|
| older | 65.4% | 0.66 | 22 |
| v80-84 | 64.4% | 0.64 | 19 |
| v85-89 | 71.2% | 0.72 | **14** |
| **v90** | 66.2% | 0.75 | **47** |

**Median launcher build round moved r14 → r47**, while launchers/game barely moved
(0.72 → 0.75) *despite* the 4.7× replacement rate. Decomposing by the late share:
v85-89 ≈ 0.67 early + 0.05 late; **v90 ≈ 0.50 early + 0.25 late.**

**So v90 appears to build fewer OPENING launchers and more late replacements — the
same total, shifted about 30 rounds later.**

Why that could matter: the launcher is the insertion enabler, and raider lifetime is
**43 rounds at r0 against 6 at r150**. A launcher arriving at r47 instead of r14
spends its best window not existing.

## 4. Verdict and limits

**The "v90-specific defect" branch of the builder's pre-stated mind-changers is
PARTIALLY LIVE** — not through bad placement, which is refuted, but through a
**timing shift the repair plausibly caused as a side effect.**

**I would not call this sufficient to roll back**: n is small and the second-clause
argument stands on its own. But the question is no longer unchecked, and this points
at **one replay rather than a battery** — *watch a v90 game and see why the first
launcher is late.*

**Limits, and they bind:**
- **n = 65 v90 games, 49 launcher builds.** Suggestive, not conclusive.
- The 0.50 early / 0.25 late decomposition is **derived from the share**, not
  directly measured per game.
- Version cohorts differ in opponent mix and map draw; nothing here is matched.
- "Builds after r100" is a **proxy** for replacement. A first launcher built late
  for any other reason counts as a replacement here, and §3 suggests that is exactly
  what is happening in some games — so §1 and §3 are not independent readings of the
  same number, and §1's 32.7% should be read as *"late launcher builds"*, not
  strictly *"rebuilds"*.
