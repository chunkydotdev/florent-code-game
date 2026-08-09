# PREREG — LOKI-9, turret facing (SUPERSEDES the forward-survival plank for the v9 slot)

**Committed BEFORE leg creation** (two-clock: this file's git author time must
predate the platform `createdAt` of every leg it governs).
Line `loki`. Comparator **LOKI-8 = `bots/_v124loki8`**, the previous line
iteration per `PROGRAMME.md: COMPARE_AGAINST`.

**Status of the other prereg.** `PREREG-loki9-forward-survival.md` is committed
and **NOT RUN**. It is not withdrawn and not refuted — it is out-competed on
cost for this slot and stays queued. Recording that rather than deleting it,
because a prereg that quietly vanishes when a better idea arrives is how a
line launders its misses.

## The defect, and why it is a defect rather than a preference

Our home turrets choose facing as **the first direction in `DIRECTIONS` order
that can hit `SLOT_THREAT`** — a *transient* enemy position at build time
(`_v124loki8` home counterbattery path). The facing is then frozen for the rest
of the match. If the reported threat is a raider inside our own collar, the
turret is permanently aimed **inward**.

Measured by research over **2,218 clean side-games / 5,456 emplacements /
1,188,099 idle sentinel-rounds** (OpenSverige only, stated inline):

* idle sentinel-rounds decompose **(a) no target 22.0% / (b) wrong facing
  64.4% / (c) other 13.6%**, and (c) is *accounted* — reload 6.5%, ammo<10
  6.4%, TLE 0.00%, unexplained 0.7% — not a residual.
* **13.2% of our home sentinels have a target on their line, against 14.2% for
  a RANDOM draw among 8 facings with position held fixed.** We aim **0.9pp
  worse than chance**.
* **11.4% point exactly at our own core.** **13.7% never had a single enemy on
  their line across a median 175-round life** (≥1900 teams: 1.1%; sporks: 0.3%).

**Worse than chance is the whole argument.** A strategy can be bad; it cannot
be reliably worse than random unless the choice is not being made on the
relevant axis at all. That matches the code exactly.

### THE SUBJECT OF THOSE NUMBERS IS NOT LOKI-8, AND THAT IS LOAD-BEARING

**Every figure above is drawn from our full ladder archive, which is dominated
by Eir (`_v115dodge`); LOKI-8 has ~70 ladder games in it.** So they describe
*our team over time*, not this tree. This matters because the sibling plank
died on exactly that: the forward-GUNNER survival statistic (57.2% dead inside
30 rounds, n=1,132) is Eir tape, and **LOKI-8 plants zero forward gunners** —
its only forward path builds a sentinel (`raid.py:386-448`). A leg filtering on
forward gunners would have returned **n=0** and been misread as "the treatment
did not fire". Third instance tonight of a number carrying the wrong subject.

**What licenses THIS plank is therefore not the corpus magnitude but a direct
CODE reading of LOKI-8**: the home counterbattery path
(`main.py:529-579`) selects facing as *the first direction in `DIRECTIONS`
order that satisfies `can_fire_from(bp, facing, turret_type, SLOT_THREAT)`* and
then freezes it. The defect is present in this tree by construction, whatever
the archive says. **The corpus figures are demoted to motivation; the bars below
are all paired within this leg.**

## The treatment — one preference, no new mechanism, nothing moves

Among facings the existing gate already permits, **prefer the one pointing at
the known enemy core** (`SLOT_ENEMY_CORE`, already populated by symmetry at
build time), falling back to current behaviour when none qualifies.
**Build incidence, siting, cost and timing are unchanged.** No forward plant,
no new exposure, no collar interaction — the cost-to-destroy guard rail cannot
be tripped because nothing relocates.

## Bars, stated before the leg

* **DID-IT-FIRE (mechanism, NOT the verdict):** share of our newly-built home
  turrets whose facing is within 45° of the enemy-core direction must rise from
  the LOKI-8 control arm of **this leg** to **>= +30pp**. Computed per-turret
  at build time from the leg's own replays. **Not anchored to any corpus
  figure** — the 61.4%-violation number is a different subject (full archive,
  all versions) and is context only.
* **VERDICT (`PROGRAMME.md: PRIMARY_CURRENCY`): `core_kill_share` vs LOKI-8**,
  same opponents, same maps, same n, paired, reported with its interval.
* **SECONDARY:** `time_to_core_kill`. Reported, never substituted.
* **DUTY CYCLE IS NOT A BAR.** sporks sits at **11.9%** of reload ceiling at
  rating 2079, *below* our 13.5% — so duty cycle is a mechanism reading and
  cannot be a currency. Recorded because our own earlier framing leaned on it.

## Falsifier

**If facing moves past the bar and `core_kill_share` does not, that is a
LABELLED NULL** — I will write the word — and the facing road closes for this
line. **If facing does not move, the leg answered nothing** (treatment-
verification failure, the D7 shape), and the diff is at fault, not the idea.

## Known ceiling and the companion we are NOT building yet

Fixing facing at fixed siting caps at **58.6%** on-line; the rest needs siting,
which is the separate, riskier, later decision. Separately, **ammunition binds
once duty cycle rises**: `ammo < 10` already blocks **6.4%** of our idle
sentinel-rounds and **27.7%** of forward-sited ones. **If this leg moves the
mechanism but the currency stalls, ammo starvation is the first thing to check
before concluding the mechanism does not pay.**

## Opponents and power

Saturated fixtures **excluded**: `clanker` (96.7%), `ouroboros` (93.3%).
Resolving: `cad_probe` (66.7%), `orizon_probe` (50.0%). Unrated legs only.
Seats recorded from the **in-replay index**, never `ladder_games.tsv:seat`,
which is the WINNER's side (TRAP 7).
**Power up front:** the comparable LOKI-7 fixture saturates at 86.7% where
15/15 vs 13/15 is p=0.483. A null at feasible n is **a null about this n**, and
I will report the n rather than the direction.

## Standing gap this leg does not close

**LOKI-7 vs LOKI-8 has never been run** and is underpowered at feasible n
(~350/arm). So LOKI-9 is measured against a baseline with **no line-internal
predecessor read behind it**. Stated, not fixed.

---

## ADDENDUM, 23:2x CEST — added AFTER the battery started. NO BAR IS CHANGED.

Recording the clock explicitly: the local battery was already running when this
was written. **Not one bar above is altered** — changing a bar mid-run is how a
prereg becomes decoration. This adds a *diagnostic branch* to the falsifier and
sharpens one argument.

### A THIRD BRANCH THE FALSIFIER WAS MISSING (research, and they are right)

The treatment reorders facings **among those the existing gate already
permits**, and that gate is `can_fire_from(bp, facing, kind, SLOT_THREAT)`.
`SLOT_THREAT` is typically **a raider inside our own collar** — which is
geometrically close to the OPPOSITE of the enemy-core direction. **So the
permitted set and the enemy-core direction may rarely intersect, the fallback
fires nearly every time, and facing compliance barely moves.**

That outcome is **indistinguishable, from the bars alone, from "the diff is
broken"** — and the two have different fixes. So the falsifier now reads:

* facing moves, currency doesn't -> **LABELLED NULL**, road closes. (unchanged)
* facing moves, currency moves -> gain, reported with its interval. (unchanged)
* **facing does NOT move -> DO NOT conclude "diff at fault". Disambiguate
  first:** measure, per home-turret build, whether an enemy-core-ward facing
  was even *in* the permitted set. If it usually was not, **the gate is the
  binding constraint, not the diff** — and the honest next treatment is "prefer
  core-ward, and drop the threat gate when it forbids it", which is a LARGER
  change needing its own prereg. It is not this plank failing; it is this plank
  never having been applied.

**This is cheap here because `mech_battery --keep-replays` is already retaining
both arms**, so the control arm supplies the permitted-set baseline directly.

### SHARPENING: the defect is ANTI-CORRELATION, not absence of choice

The file argued the choice "is not being made on the relevant axis at all".
**That under-claims it, and predicts compliance EQUAL to chance, not below it.**
The truth is the choice **is** made on an axis that is *anti-correlated* with
the target one: we aim where a raider **was seen** (inward), and targets
subsequently arrive from **outward**. **The 11.4%-aimed-at-our-own-core figure
is the direct evidence**, and only the anti-correlation reading explains
compliance landing *below* random.

### A POWER NOTE ON THE BAR, so it is not read as more than it is

45° over 8 facings admits the target direction plus its two neighbours — **3 of
8, so RANDOM compliance is already ~37.5%**. The pre-registered +30pp therefore
lands near **68%**, comfortably inside what the treatment can deliver **if the
gate permits it**. The bar is well set; the branch above decides whether it was
ever reachable.
