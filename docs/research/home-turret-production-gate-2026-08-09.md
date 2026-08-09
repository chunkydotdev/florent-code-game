# Why our live turret count flatlines at 2: home turret production is reactive and single-threaded

**Research arm, session 23, 2026-08-09.** Code read, no runs.
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"** = `bots/_v104latch`
(per the ship announcement at `coordination.md:10058`, tree `2c6dbc17`), ladder
**1577 @ 504, #29**. Line numbers are `bots/_v104latch/main.py` and
`bots/_v104latch/doctrine.py`. **No bot edits — read only.**

Prompted by the measurement in `middle-game-hazard-and-economy-2026-08-09.md` §6c:
**our live turret count sits at a median of 2 from r200 onward and never moves,
while the field's goes 2 → 3 → 4 → 5 → 5, and turret survival is identical
(50.6% vs 50.8%).** The builder was about to run a production battery. This is the
pre-battery code read, and it says the battery would tune the wrong parameter.

---

## The finding

**Home turrets have exactly one build path, callable by exactly one unit, and it
fires only when an enemy is already standing inside our home band.**

**1. One path.** `doctrine.py:694`, verbatim:

> *"the role_n == 4 defender is the ONLY unit that ever calls
> `_try_counterbattery`, so **home turrets are its exclusive capability**."*

**2. One unit, and the failure mode is already measured.** Same comment, from the
eider loss vs The Flotte Experience: the defender *"died at round 36 charging a
forward gunner and, with MAX_BUILDERS = 5 and no respawn, we then built **no home
turret for the remaining 252 rounds while 1124 titanium sat banked**."* The fix
added **one** designated successor — so the capability is now two-deep, not
distributed.

**3. The trigger is an enemy already inside the home band.** `_try_counterbattery`
(`main.py:2236`) opens:

```python
threat = unpack_pos(ct.read_store(SLOT_THREAT))
if threat is None:
    return False
if B8_ON and min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
    return False
```

`HUNT_BAND_DSQ = 41` (≈6.4 tiles from the core footprint). **No published threat
inside that band ⇒ no home turret is built, ever, by the only path that builds
them.**

> **SHARPER STILL (builder arm, same hour; I verified it at `main.py:2321-2324`).**
> The gate is not merely "a threat is in the band" — the candidate tile *and
> facing* must be able to shoot **that specific threat, this turn**:
> ```python
> aligned = ct.can_fire_from(bp, facing, turret_type, threat)
> if not aligned:
>     continue
> ```
> **A home gun is only ever built if it can fire at a currently-visible threat from
> that exact tile and facing. Nothing in the bot builds a turret because turrets are
> good.** The builder's phrasing is the right one and I am adopting it:
> **we do not have a turret production policy, we have a reflex.**
>
> That is what §6c's trajectory looks like plotted against a policy — our median 2
> from r200 and never moving, theirs 2 → 3 → 4 → 5 → 5.

**4. Plus an early economy gate** (`main.py:2264`): if `SLOT_HARVESTERS < ECO_NEED`
(=3) **and** a live home gun already stands, the path returns — waived only if
`_core_shelled` shows the core actually taking damage. This one stops binding once
3 harvesters exist, so it shapes the opening rather than the whole game.

**5. And a permanent one-in-band ceiling on the heal-skip route.** `_cb_over_heal`
(`main.py:2029`) ends `return not self._live_home_gun(ct)`, where `_live_home_gun`
is True if **any** friendly gunner or sentinel stands within `HUNT_BAND_DSQ` of the
core footprint. So the defender may skip a heal to buy a gun **only while zero home
guns stand.** The second one never comes from this route.

## Why this explains the flatline better than a cap does

**The field builds proactively; we build reactively.** Their live count grows
monotonically to ~7 whether or not anything is happening. Ours is a *response
function* — it can only be driven by an intruder inside ~6.4 tiles of our core.

And intrusions are not reliable. From the corpus (`launcher-defensive-interception.md`),
using enemy builder deaths near our core as a proxy: **only 49.4% of our games have
an enemy builder die within d²≤32 of our core, and 29.0% within d²≤8.**

> **State the proxy's direction honestly:** deaths *undercount* presence (a raider
> we never kill never appears), so 49.4% is a **lower bound** on how often the
> trigger could fire. The structural point does not depend on the exact rate: the
> path is threat-gated, so in any game where the enemy does not come to us, **our
> only home-turret path never runs, no matter how much titanium is banked.**

That is also exactly the shape of the eider loss above: 1,124 Ti banked, zero
turrets built, for 252 rounds.

## What it means for the production battery

**A battery that tunes a production *rate* or a *cap* will measure nothing in the
games where the trigger never fires.** The candidate lever is not "how many" but:

1. **Should home turret production be threat-gated at all?** The field's is
   evidently not. A proactive floor — *"by round N, have K live turrets in the home
   band, threat or no threat"* — is a different change from raising a cap, and it is
   the one the field/us divergence actually points at.
2. **Should the capability stay exclusive to one role?** Two-deep succession still
   means two deaths silence home defence for the rest of the match.
3. If a proactive floor is added, **§6b's type question applies**: gunner lines are
   blocked by our own buildings and sentinel lines are not, and we run 59
   conveyors/game against the field's 34.

**I am not proposing which of these to build** — that is the builder's lane, and
the win-rate question is untouched by any of this. What I am claiming is narrower
and checkable: **the flatline has a named mechanism in source, and it is a trigger,
not a ceiling.**

## The prediction the reflex makes, and it holds

A reflex and a policy diverge in a specific, testable way: **on a wider map the
enemy arrives later and less often, so a threat-triggered producer builds less —
while a proactive producer builds *more*, because a bigger map needs more covered.**

Win rate by core separation, three lineage cuts, all monotone:

| core sep | ALL lineage (n=2,525) | recent v85+ (n=145) | v90 only (n=65) |
|---|---|---|---|
| narrow d²≤81 | **64.2%** | 61.4% | 61.9% |
| mid 128-144 | 53.6% | 51.5% | 41.2% |
| wide 288-392 | 47.5% | 48.3% | 40.0% |
| hive 650 | **33.6%** | 12.5% (n=8) | — (n=2) |

**A ~30-point gradient, stable across cuts.** This independently reproduces the
`:1434` v72-bleed step function already in the tape (*"6/6 wins at core-sep d²≤81,
8/9 losses ≥144"*) at 2,525 games instead of 15.

**And the turret counts show the predicted divergence:**

| core sep | **US live @r150** | THEM live @r150 | US @r300 | THEM @r300 | ratio @r300 |
|---|---|---|---|---|---|
| narrow ≤81 | 1.55 | 2.16 | 1.76 | 3.53 | 2.01× |
| mid 128-144 | 1.90 | 2.80 | 2.31 | 4.28 | 1.85× |
| wide 288-392 | **1.64** | **3.57** | 2.59 | 5.91 | **2.29×** |
| hive 650 | **1.14** | **2.70** | 1.89 | 5.41 | **2.86×** |

**At r150 our live turret count is essentially flat across map width — 1.55 / 1.90 /
1.64 / 1.14 — while the field's climbs 2.16 → 2.80 → 3.57.** The ratio widens from
1.39× on narrow maps to 2.36× on hive.

> ## ⚠️ CORRECTION, same session — I first wrote *"the field scales its defence to the map. We do not."* **That is wrong, and the real mechanism is more interesting.**
>
> **Neither side scales turret PRODUCTION with map width.** r0-150 turret builds,
> means (medians are too coarse at these counts):
>
> | band | US builds | THEM builds |
> |---|---|---|
> | narrow ≤81 | 2.80 | 4.80 |
> | mid 128-144 | 3.29 | 5.20 |
> | wide 288-392 | 3.01 | 4.93 |
> | hive 650 | 1.93 | 4.33 |
>
> **narrow → wide: US +7%, THEM +3%. Both flat.** If anything our spread across
> bands (1.36) is *larger* than theirs (0.87).
>
> **The r150 live-count divergence is a SURVIVAL effect, and it FLIPS with width.**
> Turrets built before r150, fraction still alive at r150:
>
> | band | US alive | THEM alive | gap |
> |---|---|---|---|
> | narrow ≤81 | **51.4%** | 40.8% | **+10.6pp (ours live longer)** |
> | mid 128-144 | 52.7% | 49.0% | +3.7pp |
> | wide 288-392 | 48.8% | **63.2%** | **−14.4pp (theirs live longer)** |
> | hive 650 | 54.1% | 57.3% | −3.2pp |
>
> **Our survival is flat (51.4 / 52.7 / 48.8 / 54.1). Theirs rises with width
> (40.8 → 49.0 → 63.2).** On narrow maps our turrets outlive theirs; on wide maps
> theirs outlive ours by 14 points.
>
> **And this is why the pooled number concealed it.** §6b reported turret survival
> as 50.6% vs 50.8% — *"we do not lose turrets faster than the field"*. That pooled
> equality is **the average of a flip**, and it is exactly the error class this
> session has been cataloguing: a pooled statistic hiding a map-conditional
> reversal. The pooled claim is true and the causal reading I drew from it was not.
>
> **What survives unchanged:** the live-count flatline (median 2 from r200 while
> the field reaches 5), shots-per-turret within 10%, and the source read showing
> production is a threat-triggered reflex. **What is withdrawn:** any claim that
> the field's *production* responds to map geometry. **What is new:** on wide maps
> — 36% of ladder games — **our turrets die and theirs do not**, and that is a
> siting/exposure question, not a production one.

First-turret timing scales with width for *both* sides (ours 4 / 7 / 21 / 28;
theirs 5 / 10 / 24 / 32) — **so both start later on a wide map, and then they
accelerate and we don't.** That is the reflex-vs-policy signature, not a
first-turret-timing problem.

**Design consequence, and it is specific: a proactive production floor should be
map-width-scaled** (a function of `core.distance_squared(enemy)`), not a constant.
A flat floor tuned on narrow maps would leave the widest maps — **36% of ladder
games** at 288-392, plus hive — exactly as under-defended as they are now.

**Causal honesty:** the width gradient is correlational and has other plausible
contributors — conveyor lines are longer and more exposed (we build 59/game),
raiders travel further, and a compact base makes the heal screen cheaper to
maintain. **What is measured here is that our turret production specifically fails
to scale with width while the field's does, which is the behaviour the source read
predicts.** That is consistency, not proof.

## Limits

- Read of `_v104latch` only. Other build paths exist for **forward/siege** guns
  (`_try_siege_build`, `main.py:1609-1618`) and are out of scope here; the claim is
  about *home* turrets specifically.
- I have not traced every writer of `SLOT_THREAT`, so "how often is a threat
  published inside the band" is bounded by the corpus proxy above, not read off the
  publication logic.
- **Scoping correction (builder arm), and my replacement reason was also slightly
  wrong.** I said "count was held constant so production was never tested". Count
  was held constant **between the home and forward arms** (2.67 vs 3.17) — but
  **against the parent it went 0.00 → 2.67**, so LOKI-3 *did* add and test a home
  production path. It tested it **in r200-300 only, surplus-gated**
  (`MIN_RND=200`, `TI_FLOOR=250`, `MAX_SCALE=520`). **The correct scope is that
  home production is untested across r0-300** — which is where §6c shows the field
  already **1.6× ahead by r100**.
- **And the gap is not first-turret timing.** Our median first turret is **r12**
  against the field's **r17**. **We start earlier and then stop.** That is a better
  sentence than either arm had separately.
- Whether proactive production would *win* is entirely unmeasured, and the honest
  prior is not encouraging: LOKI-3's home arm moved its mechanism metric only
  0.17 → 0.32 against a field reference of 2.79, and its composite returned
  **+0.0pp on n=360**. **Four instruments agreeing that we build fewer turrets is a
  description of what we do, not proof that doing more wins.**
