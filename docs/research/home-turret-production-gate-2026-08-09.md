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

## Limits

- Read of `_v104latch` only. Other build paths exist for **forward/siege** guns
  (`_try_siege_build`, `main.py:1609-1618`) and are out of scope here; the claim is
  about *home* turrets specifically.
- I have not traced every writer of `SLOT_THREAT`, so "how often is a threat
  published inside the band" is bounded by the corpus proxy above, not read off the
  publication logic.
- Whether proactive production would *win* is entirely unmeasured. LOKI-3 held
  turret count constant by construction and therefore never tested production in
  either band — which is the correct reason home production is open, and it remains
  open after this read.
