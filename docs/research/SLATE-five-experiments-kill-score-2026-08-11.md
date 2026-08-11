# FIVE EXPERIMENTS TO MOVE THE KILL SCORE — ranked by expected points, not by appeal

**Side lane, 2026-08-11 08:2xZ (s30), at Magnus's direct commission: *"figure out
5 ways we could improve our kill rounds according to our scoring… we need to
experiment like there's no tomorrow."*** **This is a proposal slate, not a
verdict and not a firing order.** Which of these gets built and fired is the
builder's call. Every number below is measured on `corpus/ladder_games.tsv`
(n=3,670 rated games, our record, `ourver` unpinned) and is re-derivable.

---

## ⛔ FIRST: THE SUCCESS CRITERION AS STATED CANNOT MOVE, AND THAT IS A MEASUREMENT FACT

The commission says *"as long as our median score improves, an experiment is
successful."* **Our current score distribution:**

| score | games | share |
|---|---|---|
| **−10** | **2,387** | **65.0%** |
| 10 (kill <100) | 250 | 6.8% |
| 8 (<130) | 224 | 6.1% |
| 6 (<170) | 209 | 5.7% |
| 4 (<250) | 274 | 7.5% |
| 2 (<400) | 208 | 5.7% |
| 1 (slower) | 118 | 3.2% |

**65% of games score −10, so the MEDIAN GAME SCORES −10 — and it stays −10 until
we convert FIFTEEN PERCENTAGE POINTS of all games (≈551 games).** No realistic
single experiment moves it. **A median-based bar would score every real
improvement as a failure**, which is the opposite of what the commission wants.

**⇒ USE THE MEAN, which is currently −4.549/game and moves continuously**, or the
share of games scoring above −10 (currently 35.0%). Both are sensitive to exactly
the improvements below. **This is a bar-selection point, and it is the one thing
in this document I would insist on** — the rest is a menu.

## ⭐ SECOND: THE SCORING SAYS CONVERSION BEATS SPEED BY ~5×, AND THAT REFRAMES THE ASK

The buckets are **step functions**, so speeding up pays only when a boundary is
crossed. Every kill we already have, moved one bucket faster:

| band | kills | within 20 rounds of the line | worth |
|---|---|---|---|
| 100–130 | 224 | 161 | +322 |
| 130–170 | 209 | 111 | +222 |
| 170–250 | 274 | 87 | +174 |
| 250–400 | 208 | 35 | +70 |

**Every near-boundary speedup on the board, added together, is worth ~+788
points.** Against that:

| the −10 pile, 2,387 games | n | |
|---|---|---|
| **TIEBREAK WINS — we won at r1000 and never killed** | **603** | **we outlasted them and could not convert** |
| tiebreak losses (survived, lost the count) | 503 | |
| core losses (they killed us) | 1,281 | |

**1,106 games — 30% of everything we play — we SURVIVED to r1000.** Each one
converted to a sub-r170 kill is worth **+16**; sub-r100, **+20**.
**Converting just 10% of them = +1,760 points — more than double every speedup on
the board combined.**

**⇒ The highest-value "improve our kill round" experiment is not making fast kills
faster. It is making a kill happen at all in the 1,106 games where we are still
alive at r1000 — and 603 of those are games we were WINNING.**

---

# THE FIVE, RANKED BY EXPECTED POINTS

### 1. THE CLOSER — commit the bank when we are ahead and the game is drifting to r1000
**Target: the 603 tiebreak WINS.** In these we finished with the better economy
and never converted it. **Under `R1000_IS_DEFEAT` each is scored identically to a
loss.** Mechanism to test: a round-N trigger (N≈600–700) that, when we are ahead
on economy and the enemy core is reachable, spends the bank on assault rather
than continuing to accumulate. **Currency effect if 10% convert: +1,760.**
**Why it is credible: we already have the titanium — these are wins.** The plank
is a spending rule, not a new capability.
**Risk to pre-register: converting a tiebreak WIN into a LOSS is score-neutral
(−10 either way), so the downside is bounded at zero on this currency** — which
is unusual and makes it the cheapest large bet on the board.

### 2. THE DIVERGE CONSISTENCY GAP — the ceiling is identical, the median is 59 rounds apart
**diverge is rated 1682 to our 1686 and kills our core at median r103 across 57
kills; we kill at median r162 across 1,283.** Head-to-head over 100 games they
beat us 57–43, and inside that matchup **they kill us at r103 while we kill them
at r138** — same maps, same era, both bots fixed.
**⭐ AND OUR FASTEST KILL EVER IS r58 AGAINST THEIR r59.** The ceiling is the
same. **This is not a capability gap, it is a consistency gap** — they convert
routinely, we convert when conditions happen to align. **All 51 of their fast
kills against us are archived (100% coverage)** and the timeline reconstruction is
in flight. **Expected value: moving our median from r162 to r130 is +2/kill across
~1,283 kills.**

### 3. CONVEYOR DENIAL — a rival is running it now and climbed +162 while doing so
farming_200s v13 added builder-melee on enemy conveyors: **0 attacks across 310
archived games in v7–v12, then 3,329 across 87 of 105 v13 games, 94.3% on
conveyors, median target d²=2 from the enemy core** — and climbed **1644 → 1806 in
eight hours**. **Our six-roads queue carries conveyor denial as REPRICED BUT NEVER
DOSED.** ⚠ **Their 3,329 attacks bought exactly ONE conveyor kill**, so if it works
it is not by destruction — tempo or occupancy. **And their gain is not attributed:
the rating jump lives in 120 ladder games we hold 10 replays of.** Prioritises the
road; proves nothing.

### 4. BURST ABOVE THE HEAL CEILING — a measured arithmetic gap, not a guess
Defenders heal back **0.763 HP per HP our turrets remove** (r=0.858, n=50) — **on a
control arm with zero pecks, so it is a LEVEL, not a trigger.** But healing is
throughput-capped: **4 HP per builder per turn, and they run 0.86–1.54 simultaneous
healers, maximum 4 ever observed across 100 games** — a realised ceiling of
~6 HP/round typical, ~16 at the maximum. **A sentinel is 18 damage on a 2-round
reload = 9 HP/round: one exceeds their typical throughput, two exceed even the
4-healer ceiling.** ⇒ Test CONCENTRATION — two sentinels bearing on one core —
against the same damage spread across time. **Prices from the rules table, counts
from measurement; no leg has tested either.**

### 5. FORWARD/HOME TURRET MIX — the one surviving reading of today's siting work
**We sit 51.4% HOME against the field's 31.1%**, and **our home sentinels fire
4.04 shots/100 alive-rounds against 32.74 forward — eight times less
productive**, at 30 Ti and a permanent +20% cost-scale contribution each.
**⚠ FENCED, and this is the weakest of the five for a specific reason:** the 8×
compares turrets in different POSITIONS and assumes productivity is a property of
position rather than of the conditions that produced the siting. A home sentinel
may exist *because* forward siting was unavailable. **That is a selection effect
no n fixes — it needs a design that breaks it, not more games.** Listed for
completeness, not recommended next.

---

## WHAT I WOULD FIRE FIRST, AND WHY (a recommendation, not a ruling)

**#1, THE CLOSER.** It is the largest addressable block (603 games we were
winning), the downside on this currency is bounded at zero, the capability
already exists (we hold the titanium), and it needs a spending rule rather than a
new mechanism. **#2 is the best-evidenced but is waiting on a decode; #3 has field
evidence and no attribution; #4 is clean arithmetic and untested; #5 is fenced.**

## OBLIGATIONS ANY OF THESE MUST CARRY (pre-checked so the builder need not)
* **Ob. 12** — size every GATE, not just every bar; unresolved gate ⇒ RESTRICTION.
* **Ob. 13** — `MECHANISM METRIC READS / TREATMENT DIFF TOUCHES / INTERSECTION`;
  `tools/inert_check.py` answers it in one command. **LOKI-18 burned a window on
  an inert bar.**
* **Ob. 14** — per-cell opponent-version counts before selection. **Drop
  SmartFridge (six failed admission checks in a day); the other four cells were
  version-stable at 161 minutes.**
* **Sizing** — against the ~400 banked v104 control games, **200 treatment games
  (8 windows, ≈2.7 h) resolves 15pp**; 25-game windows resolve nothing and every
  leg fired at that size was pre-committed to returning "unresolved".
* **Arm `window_watcher`** in the same commit as the prereg — it is DOWN, and its
  docstring records **40.92 Elo** lost the last time an evaluation point had
  nobody watching.

**LIMITS:** the score distribution is our RATED record pooled across all our
versions (`ourver` unpinned), so it describes the line's history rather than the
live tree; the +1,760 assumes a 10% conversion rate that nothing has yet
demonstrated; and the diverge comparison is us-only by construction.

---

# ADDENDUM, 08:2xZ — I TRIED TO KILL #1 BEFORE ANYONE BUILT IT. THE PREMISE SURVIVED AND GOT STRONGER.

**The Closer assumes those 603 games leave us with unspent capacity. If we finish
broke, the plank is dead and proposing it would have cost a window.** Measured on
`corpus/econ.tsv` joined through `meta_join` (our side only):

**Titanium on hand, band `r300+`, by outcome:**

| outcome | n | median `ti_end` | mean | p90 |
|---|---|---|---|---|
| **TIEBREAK WIN (scores −10)** | 182 | **4,318** | 6,019 | 15,677 |
| tiebreak LOSS (−10) | 210 | 1,150 | 3,593 | 11,737 |
| core-kill WIN | 258 | **148** | 2,391 | 8,953 |
| core LOSS | 382 | 124 | 2,140 | 7,522 |

**⭐ AND THE LIKE-FOR-LIKE VERSION, which is the one that counts — BOTH ARMS ARE
LONG GAMES**, since a kill-win reaching the `r300+` band is by construction a SLOW
kill:

| band | tiebreak WIN: ti / builds / attacks | core-kill WIN: ti / builds / attacks |
|---|---|---|
| r0–150 | 50 / 49 / 57 | 33 / 33 / 0 |
| r150–200 | 74 / 8 / 15 | 46 / 2 / 0 |
| r200–300 | 232 / 11 / 14 | 56 / 3 / 0 |
| **r300+** | **3,496** / 32 / 34 | **92** / 5 / 5 |

**Among games that ran past r300, the ones we KILLED in finished holding 92
titanium and the ones we did not finished holding 3,496 — a 38× difference on
comparable populations.**

**AND WE ARE NOT IDLE WHILE HOARDING: 32 builds and 34 attacks in the `r300+`
band of tiebreak wins.** We are active *and* rich simultaneously — so this is not
"nothing to spend it on". **The hoard also forms LATE** (50 → 74 → 232 → 3,496),
i.e. income outruns spending progressively after ~r200.

**⛔ WHAT THIS DOES NOT ESTABLISH, and it is the same fork this lane flagged on
the turret-mix reading:** whether **hoarding causes the failure to kill** (the
Closer fixes it) or **the failure to find a kill causes the hoard** (the Closer
changes nothing and the constraint is elsewhere). **The correlation cannot
separate them.**
**What IS established either way: the RESOURCE is not the binding constraint.**
4,318 titanium is a large assault even at inflated late-game scale. **So the
Closer's premise — "we have the means and do not use them" — holds; its mechanism
is exactly what the leg would test.** That is the right reason to fire it rather
than a reason to assume it.

---

# ⛔ CORRECTION, 08:3xZ — MY DAMAGE-RATE ARITHMETIC DESCRIBED A BOT THAT HAS NOT EXISTED SINCE 2026-08-09

**The addendum above reasoned from `batk_core ≈ 104/game` in long games. That
figure is POOLED ACROSS ALL OUR VERSIONS and it describes the DEAD tree.**
Era-pinned:

| our version | games | batk/game | batk_core/game | shots/game |
|---|---|---|---|---|
| v64–v94 (Eir era) | 45–366 each | **117–322** | 5.8–130.8 | 47–169 |
| **v102, v103, v104, v105, v106, v107** | **1,573 on v104 alone** | **0.00** | **0.00** | 42–58 |
| v108 (LOKI-19 treatment) | 50 | 192.9 | **192.90** | 34.8 |

**THE LIVE TREE DOES ZERO BUILDER MELEE.** I flagged "`ourver` unpinned" as a
limit in this document's own header and then reasoned from the pooled number
anyway two sections later. **That is the era rider firing on me — the exact
failure the drift-watch file warns about: "any 'we/our bot' figure pooled over
the archive describes the dead bot unless recomputed on the live subset."**
**The 1.81 HP/round rate is v64–v94's, not ours.** Withdrawn.

## ⭐ AND THE CORRECTION POINTS SOMEWHERE BETTER THAN THE ERROR DID

The field census (`SCOUT-field-mechanism-census-2026-08-11.md`) measured, on the
same archive: **20 of 20 teams above us do builder melee, median 90% of their
games. Our v104 does it in 0 of 1,605.** It is **one boolean** —
`bots/_v130loki13/doctrine.py:1470`, `LOKI_QUIET_ON = True`, four call sites —
and **our own v94 ran 218 attacks/game until 2026-08-09**, when we switched it
off. **⚠ The census's own control demotes melee VOLUME (the heaviest attackers
are rated 1313–1669) but not melee PRESENCE: 15 of 50 teams below us have none,
14 of those 15 rated <1550, and we group with vjg 730 / Troupe 1011.**

**⇒ THE HIGHEST-VALUE ACTION IS NOT A NEW PLANK. IT IS FINISHING ONE.**
**LOKI-19 already re-tested exactly this** — v108, core-peck restored, **dose
verified at 192.90 attacks/game against a control of exactly 0.00** — and
returned **band 2: dose delivered, mechanism measured, currency UNRESOLVED at
n=50/arm**, precisely as its own prereg predicted it would.

**It is 150 treatment games short of resolving.** Against the ~400 banked v104
control games — **still version-stable on 4 of 5 cells at 161 minutes, measured**
— **200 treatment games resolves 15pp.** LOKI-19 has 50.

> **150 more v108 games = 30 matches = 6 windows ≈ 2 hours.**

**No new tree. No new prereg — its own says "pooling more windows is the ONLY
route and windows are free". Dose already verified. Control already banked. And
the field census now says every team above us runs the mechanism we switched off.**

**HONEST CAVEAT ON #1, THE CLOSER: its premise rests on the 4,318 vs 148
titanium gap, which I have NOT era-pinned.** The same correction may apply.
**Pin it before building anything** — one query, and it is the query I should
have run before writing the addendum.
