# PLAN — RESTART THE MILL. The constraint is TREATMENT GAMES, and we have been buying the other thing.

**Side lane, 2026-08-11 08:1xZ (s30), at Magnus's direct ask ("I believe you can
get us going again").** **This is a costed plan, not a verdict and not an
instruction** — firing, verdicts and bot edits are the builder's, and this lane
does not hold them. Everything below is measured today and re-derivable.

---

## 1. THE CONSTRAINT, MEASURED — AND WE SPENT THE NIGHT BUYING THE WRONG SIDE

Our unrated matches since 23:00Z, keyed on **our** version (each distinct
prototype = one experiment):

| our version | matches | games | what it is |
|---|---|---|---|
| **v104** | **85** | **425** | **the INCUMBENT — control pool, not an experiment** |
| v108 | 10 | 50 | LOKI-19 |
| v109 | 5 | 25 | LOKI-18 (void on premise) |

**500 games, 85% of them on the incumbent. Two experiments. 21 firing windows, 16
of them pure overnight control accumulation at one every 20 minutes.**

**⭐ AND CONTROL GAMES ARE NEARLY WORTHLESS AT THIS RATIO.** Power in a two-arm
comparison is the harmonic mean — driven by the SMALLER arm. From the actual
50/400 split:

| what you buy | effective n | gain |
|---|---|---|
| +400 more CONTROL (double the whole overnight pool) | 88.9 → **94.1** | **+5.2** |
| +50 more TREATMENT (double the arm) | 88.9 → **160.0** | **+71.1** |

**A treatment game is worth 109× a control game right now.** Last night's 85
matches, spent on treatment, would have resolved a ~10pp currency effect. Spent
on control, they moved effective n by five points. **That is the whole staleness
— not idleness. The mill ran at the rate-limit ceiling all night on the arm that
cannot resolve anything.**

## 2. THE BANKED ASSET, AND IT IS STILL LIVE — VERIFIED, NOT ASSUMED

**We already hold ~400 v104 control games** (LOKI-19's control + the overnight
pool). The obvious objection is decay: median opponent-version lifetime is
**1.17 h** and the control window closed at **05:31Z**. Measured at **08:12Z,
161 minutes later**:

| cell | control-window version | now | |
|---|---|---|---|
| Lunds Stallions | v64 | v64 | **SAME** |
| Askar City | v94 | v94 | **SAME** |
| farming_200s | v13 | v13 | **SAME** |
| Landers | v93 | v93 | **SAME** |
| Powered by SmartFridge | v57/67 | **v33, v35, v67** | **MOVED — three concurrent** |

**FOUR OF FIVE CELLS ARE STILL VERSION-STABLE AT 2.7× THE MEDIAN LIFETIME.** That
is not luck: **stability is a cell property** (Obligation 14), and these four have
it. **So the banked control is REUSABLE TODAY on four cells, and every window
from here can be pure treatment.**

## 3. WHAT THAT BUYS — MDE against the banked 400, by treatment games

Match-clustered (5 games/match); `icc` spans the plausible range because a
25-game window has shown a 12pp same-bot swing.

| treatment games | icc=0.0 | icc=0.1 | icc=0.2 |
|---|---|---|---|
| 25 | 28.9 | 34.1 | 38.7 |
| 50 | 21.0 | 24.8 | 28.2 |
| **100** | 15.7 | **18.5** | 21.0 |
| **200** | 12.1 | **14.3** | 16.3 |
| 400 | 9.9 | 11.7 | 13.3 |

* **~200 treatment games = 40 matches = 8 windows ≈ 2.7 h** → resolves **15pp**.
* **~875 treatment games ≈ 35 windows ≈ 12 h** → resolves **10pp**.
* For scale: **LOKI-13 shipped on +18.0pp (Fisher p=0.016)** — the line's one
  significant currency result. **A 200-game treatment arm can see a LOKI-13-sized
  effect. A 25-game window never could**, and every leg fired at that size was
  pre-committed to returning "unresolved".

## 4. THE PANEL — DROP SmartFridge, FIRE THE FOUR STABLE CELLS

SmartFridge has now failed **six** independent admission checks in a day
(arrival precondition · version churn · seat inversion · most-favourable 5d
number · no version-matched control · **and now three concurrent versions**).
**It is not an unlucky cell — rating proximity selects for nothing a mechanism
needs.** The four stable cells are the panel; **Focalground** is the
evidence-backed fifth if one is wanted (45.7% share on n=35, **one** version in
24 h, +10 rating gap so a win pays near the top of the reachable band).

## 5. WHAT IS READY TO FIRE — three built, pre-registered, unconverted planks

| plank | tree | status |
|---|---|---|
| **LOKI-15** — per-builder conveyor quota | `bots/_v132loki15` | **pre-registered FOR POOLED WINDOWS at n=100/arm** (`1e76196`). **Already the right design shape.** |
| **LOKI-16b** — ring-hold | `bots/_v133loki16` | mechanism bar **CLEARED +0.164 [+0.073, +0.253]** vs +0.15; confirmation leg queued and unfired |
| **LOKI-14** — crash-induction | `bots/_v131loki14` | prereg exists, **norms hold released by Magnus** |

**LOKI-15 is the one I would put first if the choice were mine** — it is the only
one already pre-registered for the pooled design the arithmetic demands, so it
needs no new prereg, only windows. **The choice is the builder's.**

**And a NEW candidate with field evidence, needing a build:** farming_200s v13
added a **builder-melee conveyor raid** (0 attacks in 310 games across v7–v12,
then 3,329 across 87 of 105 v13 games) and climbed **+162 in eight hours**. Our
six-roads queue carries conveyor denial as **repriced but never dosed**. A rival
paid for that experiment.

## 6. OBLIGATIONS, PRE-CHECKED SO THE BUILDER DOES NOT HAVE TO

* **Ob. 12 — size every GATE, not only every bar**, and pre-commit that an
  unresolved gate defaults to the RESTRICTION.
* **Ob. 13 — `MECHANISM METRIC READS / TREATMENT DIFF TOUCHES / INTERSECTION`.**
  `tools/inert_check.py` now answers it in one command. **LOKI-18 spent a window
  on an inert bar; this is the check that catches it before firing.**
* **Ob. 14 — per-cell version counts before selection.** Done above; four cells
  pass, SmartFridge fails.
* **Blocking is DISCLOSED, not corrected:** the control is banked, so the design
  is **blocked, not interleaved** — the read-out says so, and the arms are
  unbalanced on the fixture axes (seat, map). **Both were already priced today.**
* **`window_watcher` is DOWN and nothing schedules it.** Its docstring records
  **40.92 Elo lost** the last time a pre-registered evaluation point had nobody
  watching. **Arm it in the same breath as the prereg that defines the point.**

## 7. THE ONE-LINE CHANGE THAT MATTERS

**Stop firing the incumbent overnight. The control pool is bought, it survives 2.7
hours on four cells, and another 400 control games buy 5 points of effective n
against 71 for the same spend on treatment.** Every window from here goes to a
prototype, or it is worth 1/109th of what it could be.

**LIMITS OF THIS DOCUMENT:** no verdict is issued and none may be read into it;
the sizing assumes core-kill share at p≈0.5 and a 5-game cluster, and `icc` is
bracketed rather than measured; the 109× is arithmetic about THIS 50/400 split
and shrinks as the arms equalise; and **which plank fires is the builder's call,
not this lane's.**
