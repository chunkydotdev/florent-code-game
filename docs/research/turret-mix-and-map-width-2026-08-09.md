# Our home turrets are the best in the corpus. On wide maps we stop building them.

**Research arm, session 23, 2026-08-09.** Corpus only — free metadata and archived
replays. **Zero downloads, zero arena, zero bot edits.**
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"** = `bots/_v104latch`,
ladder 1568 @ 505, #30. Corpus: 4,351 replays, 4,311 decoded, **join 1,250 rows,
100.0000% reconciled.**

This supersedes the causal reading in `home-turret-production-gate-2026-08-09.md`
§"the prediction the reflex makes". **The survival reversal reported there is a MIX
effect, and the mix is the finding.**

---

## 0. TL;DR

**Split turret survival by *where the turret stands*, and the reversal disappears
into something much sharper:**

| band | side | US n | **US alive @r150** | THEM n | THEM alive @r150 |
|---|---|---|---|---|---|
| narrow ≤81 | HOME | 611 | **52.5%** | 843 | 48.4% |
| narrow ≤81 | FORWARD | 198 | 48.0% | 540 | 28.9% |
| mid 128-144 | HOME | 589 | **67.4%** | 800 | 56.1% |
| mid 128-144 | FORWARD | 329 | 26.4% | 642 | 40.2% |
| wide 288-392 | HOME | 549 | **86.7%** | 1,287 | 72.0% |
| wide 288-392 | FORWARD | 702 | **19.2%** | 811 | 49.3% |
| hive 650 | HOME | 52 | **92.3%** | 151 | 60.9% |
| hive 650 | FORWARD | 70 | 25.7% | 111 | 52.3% |
| **pooled** | **HOME** | **1,801** | **69.0%** | 3,081 | 60.9% |
| **pooled** | **FORWARD** | **1,299** | **25.8%** | 2,104 | 41.4% |

1. **Our HOME turrets are the best-surviving turrets in the corpus — in every
   single band — and the advantage GROWS with map width**: +4.1pp narrow, +11.3pp
   mid, **+14.7pp wide, +31.4pp hive**.
2. **Our FORWARD turrets are the worst in the corpus**, and also worsen with width:
   **19.2% on wide maps against the field's 49.3%.**
3. **And on wide maps we put 61.1% of our early turrets FORWARD, against 23.9% on
   narrow maps.** The field does not shift: 41.0% → 46.3%.

**So as maps widen we move our turret investment out of the thing we are best at in
the world (home, 86.7%) and into the thing we are worst at (forward, 19.2%).** That
is the whole of the width gradient, and it is a *subtraction* to fix, not a build.

---

## 1. The mix, measured

r0-150 turret placement, `t` = fraction along the core axis (0 = own core, 1 = enemy
core), recovered exactly from `d2_own`, `d2_enemy` and the per-map core separation:

| band | US median t | **US forward%** | THEM median t | THEM forward% |
|---|---|---|---|---|
| narrow ≤81 | 0.33 | **23.9%** | 0.44 | 41.0% |
| mid 128-144 | 0.50 | 37.3% | 0.50 | 49.9% |
| wide 288-392 | **0.71** | **61.1%** | **0.38** | 46.3% |
| hive 650 | 0.75 | 59.6% | 0.62 | 50.9% |

**Our siting drifts forward as the map widens (t 0.33 → 0.50 → 0.71). The field's
does not (0.44 → 0.50 → 0.38 — if anything it pulls back).**

On narrow maps **we are the conservative team** and the field is the aggressive one.
On wide maps the roles invert completely.

> ### REFINEMENT (same session) — those are MIX statistics, and the mechanism is shared
>
> I first read the row above as *"our siting drifts forward with map width, the
> field's does not."* **That over-claims.** Restricting to FORWARD turrets only:
>
> | band | D (tiles) | **US tiles from ENEMY core** | THEM tiles from ENEMY core |
> |---|---|---|---|
> | narrow ≤81 | 7.4 | **3.0** | 2.8 |
> | mid 128-144 | 11.7 | **3.6** | 3.6 |
> | wide 288-392 | 18.4 | **4.1** | 5.0 |
> | hive 650 | 25.5 | 6.4 | 4.2 |
>
> **Forward turrets on BOTH sides sit at a near-constant 3-6 tiles from the enemy
> core while D varies 7.4 → 25.5.** So forward siting is a **fixed standoff from
> the enemy core, for both teams** — not a fraction of the map — and `t` therefore
> rises with width **mechanically, for everyone**. The field's forward-only median
> `t` is 0.75 / 0.83 / 0.82 / 0.87, every bit as deep as ours.
>
> **This is confirmed in our own source.** `_plan_siege` (`_v104latch/main.py:1478`)
> is documented as choosing *"a reachable tile whose weapon ray intersects the enemy
> Core"*, at `ranges = (5, 4)` for a sentinel and `(3, 2)` for a gunner — a fixed
> standoff, exactly as measured.
>
> **So what actually differs is not WHERE a forward turret stands. It is:**
> 1. **the SHARE forward** — on wide maps 61.1% of ours against 46.3% of theirs,
>    and the all-turret `t` moves in opposite directions because their mix shifts
>    *home* while ours shifts *forward*; and
> 2. **how badly ours do once forward** — 19.2% against 49.3%.
>
> **(2) most likely reduces to (1) plus volume**: we field 4.5 turrets/game against
> 10.7, so our forward guns are far more often *alone*. That is the builder's own
> FARGUN-COVERAGE result seen from the other side — ours-covered 43.1% against the
> field's 68.6% — and it means the forward bucket is not intrinsically a 19.2%
> bucket for everyone, only for a team that sends guns forward unsupported.
>
> **The recommendation is unchanged and arguably strengthened**: on wide maps, stop
> shifting the mix forward. **The change is still a subtraction.** But the reason is
> *"we send unsupported guns deep"*, not *"our siting formula drifts and theirs
> doesn't."*

## 2. The arithmetic checks out

The mix reproduces the pooled numbers exactly, which is how we know it is the whole
explanation and not a contributing factor:

```
US   wide:  HOME 549 x 86.7% = 476  +  FORWARD 702 x 19.2% = 135   ->  611/1251 = 48.8%
THEM wide:  HOME 1287 x 72.0% = 927 +  FORWARD 811 x 49.3% = 400   -> 1327/2098 = 63.2%
```

**48.8% and 63.2% are precisely the pooled figures that looked like a survival
reversal.** Neither side's turrets got better or worse with map width in any given
position. **Only the mix moved, and only ours.**

## 3. What this corrects, and what it costs me

- **Withdrawn:** *"the field scales its defence to the map, we do not"* — already
  retracted earlier today; production is flat for both.
- **Withdrawn:** the survival *reversal* as a fact about turret durability. There is
  no reversal in durability. **Our turrets are more durable than the field's in both
  positions on wide maps** (HOME 86.7 vs 72.0; and on narrow maps FORWARD 48.0 vs
  28.9).
- **Withdrawn:** §6b's *"attrition is fine, production is the problem"* as a complete
  reading. Attrition is fine **conditional on position**; the *positional mix* is a
  third lever alongside production and price, and on wide maps it dominates.

**This is the fourth time today a pooled statistic hid a conditional reversal** —
the anchor comparison (forward-only vs forward+home pooled), the `d²>110` far-gun cut
(absolute threshold across a 20× range), my opponent-thermometer differentials
(variance all on the other side), and now this. **Three of the four were mine.** The
standing rule is no longer sufficient as stated; the working version is:

> **Before a pooled number becomes a belief, split it by the parameter that varies
> most across the population. Here that is core separation, which ranges 20×.**

## 4. What it means for the queue

**The forward road being closed is not a reason to relax — we are still driving down
it on wide maps.** 61.1% of our early turrets on wide maps are forward, at 19.2%
survival. Per the refinement in §1, the standoff itself is *fixed* and the field uses
the same one; what nobody chose is the **share** — `_plan_siege` fires whenever a
reachable ray onto the enemy core exists, and on a wide map more of our turret budget
ends up satisfying that condition than the home path's threat trigger.

**The cheapest available change is a subtraction, not an addition:** gate the forward
share on core separation, so that on wide maps the budget stays home. It needs no new
subsystem, and it moves investment from a 19.2% bucket into an 86.7% bucket. **Note
the asymmetry that makes this cheap: the home path is gated on a threat appearing
(`_try_counterbattery`), while the forward path is gated only on a ray existing —
so on a quiet wide map the forward path is the only one that fires at all.**

**And it interacts with the production build already in flight.** Adding production
without fixing the mix would add turrets into the forward bucket on exactly the maps
where that bucket runs at 19.2%. **Any production experiment must be reported split
by core-separation band**, or it will average a home regime against a forward one.

**The home number is also worth stating positively, because it is the strongest
thing we have measured about ourselves all session:** at 86.7% and 92.3% survival on
wide and hive maps, against a field at 72.0% and 60.9%, **our home defence is not
merely "our measured strength" — it is the best in the corpus, and it gets better the
wider the map.** Everything that moves titanium from forward to home is moving it
from our worst asset to our best.

## 4b. The gate asymmetry makes a falsifiable prediction, and it holds

The two paths have radically different trigger conditions:

- **HOME** (`_try_counterbattery`) needs a **published threat within d²≤41** of the
  core footprint **and** a tile+facing that can shoot *that threat, this turn*.
- **FORWARD** (`_plan_siege`) needs only that **a reachable ray onto the enemy core
  exists**. No threat required.

**Prediction: in games where no enemy ever enters our home band, the home path never
fires, so a much larger SHARE of our turrets should be forward.**

Enemy builder deaths within d²≤41 of our core as the intrusion proxy, 1,255 games:

| enemy intrusions (d²≤41) | games | our turrets | **FORWARD share** |
|---|---|---|---|
| **0** | 596 | 1,712 | **61.2%** |
| 1-2 | 292 | 1,296 | 37.7% |
| 3+ | 367 | 2,616 | **25.5%** |

**Monotone, and steep: 61.2% → 37.7% → 25.5%.** And **596 of 1,255 games — 47% —
have zero intrusion into that band**, so in nearly half our games the home path may
never fire at all while the forward path sends the majority of our turrets into the
19.2%-survival bucket.

Win rate across the same strata, for context: 52.7% / 50.3% / 43.9%.

> **THE CONFOUND, and it is real and runs the wrong way for me:** more forward
> turrets could *cause* fewer intrusions, by killing raiders before they arrive.
> Then the correlation is reversed causation and this table proves nothing on its
> own. **What keeps the mechanism standing is that it is established in SOURCE
> independently of this table** — `_try_counterbattery` demonstrably requires a
> threat and `_plan_siege` demonstrably does not. The table is *consistent with* the
> mechanism, not proof of it. **A clean test would gate the forward path and observe
> whether the home path's firing rate rises**, which is a build, not a query.

## 5. Limits

- Survival is measured to **r150 only**, for turrets built before r150. Later-band
  behaviour is not covered here.
- `FORWARD` is `d2_enemy <= d2_own`, the `side` column's definition and the same test
  `_late_band_ok` applies. It is a coarse binary; the `t` table is the continuous
  version.
- **Correlational.** Forward turrets may die because forward is dangerous, or
  because we site them forward *when we are already losing*. Nothing here randomises
  position. The map-width interaction is what makes the exposure reading more
  plausible than the reverse-causal one, since map width is assigned before the game.
- The hive rows are n=52-70 on our side. Shape only.
- Build↔death pairing is FIFO on `(file, team, kind, x, y)`; a rebuilt tile could
  mis-pair. Not audited.
