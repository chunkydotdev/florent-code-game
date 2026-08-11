# PROPOSAL — LOKI-20: HEALER EVICTION

**Research arm, s30, 2026-08-11, written on Magnus's instruction ("worth an
experiment… write something up for the builder to prototype and run unrated
games on").**

**⛔ THIS IS A PROPOSAL, NOT A PRE-REGISTRATION.** A prereg is committed by the
lane that fires it, before the leg exists, on the two-clock standard. **The
builder owns the prereg, the bot, the firing and every verdict sentence.** What
this document supplies is the part my lane can supply *before* the build: the
question, the measured admission, the measured opportunity, the estimators, and
**the resolution audit for every bar AND every gate** — which is the defect I
found in LOKI-19 today and which is the reason this document exists in this shape.

```
TARGET BAND: Focalground -1, Coreflood -9, Landers -23, Big O +49, 0033 +73,
             gaps -23..+73, a 5-0 pays 14.94..19.30, reachable 5/5
```
*(verbatim from `tools/target_value.py`, run before this document was written)*

---

## 1. THE QUESTION

> **Their core healing is capped at 4 HP per builder per turn and they run one to
> two healers. If we EVICT a healer instead of trying to out-damage it, does the
> healing actually fall?**

**Why this and not more damage.** Measured today over 100 games
(`HEAL-RESPONSE-loki19-s11-2026-08-11.md`): a heal is **0.250 Ti per HP** and
beats every weapon we own — sentinel 0.556, gunner 0.571, builder peck 1.000. **A
damage race against a healing defender does not come out at any weapon mix.** But
healing is **throughput-capped**, and the cap is low: **0.86–1.54 simultaneous
core-healers, maximum 4 ever seen in 100 games.** Removing one removes 4 HP/round
of defence at **0 ammo**.

**Why it is credible that we can:** `can_launch` has **no team check and no
vision guard** (engine-read, `engine-source-crash-and-launcher-2026-08-10.md`);
pickup is d² ≤ 2, throw 1 ≤ d² ≤ 26, cost 0 ammo, cooldown +1, position-only
mutation. **The approved kidnap class, unchanged.**

**Why it is a change and not a tuning:** we are the field's heaviest ejector —
**3,727 hostile throws to their 1,927** — and the median ejected bot sits **d²
265 from its own core**, i.e. deep in *our* half. **Only 1.8% land inside their
core's heal ring.** We are doing this already, at the wrong end of the map.

## 2. ⛔ ADMISSION, MEASURED PER CELL BEFORE THE PANEL WAS CHOSEN

**The cell must HEAL ITS CORE or the mechanism has nothing to deny.** Our
archived games, `scratchpad/heal_read.py` (6 forced-answer cells, 3 mutations
caught):

| candidate | games | core-heals/game | % games with any heal | heal/damage | versions in 24 h |
|---|---:|---:|---:|---:|---:|
| **Focalground** | 65 | **833.1** | **95%** | 0.928 | **1** |
| **Big O** | 20 | 253.8 | 75% | 0.783 | **1** |
| **Coreflood** | 35 | 195.0 | 89% | 0.792 | 2 |
| **Landers** | 145 | 127.3 | 80% | 0.623 | 2 |
| **0033** | 100 | 93.8 | 52% | 0.604 | **1** |
| arsonist duck | 40 | 41.1 | 75% | 0.419 | 1 |
| **⛔ The Bisons** | **260** | **0.0** | **0%** | 0.000 | 1 |

**THE BISONS ARE THE POINT OF THIS TABLE.** Stable, reachable at +2, and **our
largest archived sample on the board — and they never heal their core.** Firing
there would test the opposite condition. **That is exactly the trap LOKI-19 hit
with SmartFridge** (largest sample, 7.6% arrival, the one cell that could not
deliver the premise). **The admission check cost minutes and it caught the cell
that "we have the most data on it" would have chosen.**

**PANEL: Focalground · Big O · Coreflood · Landers · 0033.** All admit, all
reachable, four of five ship ≤2 versions/24 h — which applies today's other rule,
**prefer cells where the OPPONENT IS STABLE over cells where OUR SAMPLE IS
LARGE**.

## 3. OPPORTUNITY, ALSO MEASURED BEFORE — THE ASSUMPTION MOST LIKELY TO KILL THIS

| cell | games | rounds/game with an enemy builder on their own core ring | …and one of ours within d² ≤ 4 | games with ≥1 such round |
|---|---:|---:|---:|---:|
| Landers | 58 | 233.2 | **132.7** | 54/58 |
| Focalground | 26 | 288.6 | **65.2** | 20/26 |

**Targets are abundant, not scarce.** ⚠ **This is a GENEROUS UPPER BOUND and must
not be quoted as a dose:** it uses *our builder* within d² ≤ 4 as a proxy for *a
launcher* within its d² ≤ 2 pickup range. **The real dose is bounded by whether a
forward launcher gets built and survives, which is the builder's local check and
is not measured here.**

## 4. THE TREATMENT — ONE GATE, AND WHAT IT MUST NOT DRAG IN

**One flag, `LOKI20_EVICT_ON`.** When a raider holds a tile on the enemy core
ring and an enemy builder occupies a ring tile: build a launcher, and throw that
builder to the legal destination **maximising its distance from their core**.

**Must stay off, so no off-programme change rides along:** home-side launcher
behaviour (that is `PLAY_DEFENCE: never` territory and is the incumbent's
behaviour), builder melee (`LOKI19_CORE_PECK_ON` stays as shipped), and any
economic change.

**⚠ THE COST IS NOT ZERO AND I PRICED IT WRONG ONCE TODAY.** I first proposed this
as a *retarget*; the builder's dose check established it is a **build-mix change**
— only **194 of 12,157** forward turret builds are launchers (1.6%). A launcher
is 20 Ti base **+10% on the global additive cost scale**, and it displaces a
sentinel the raider might otherwise have built. **That trade is bar 5d.**

## 5. BARS — estimator and clustering unit on every line

| # | bar | statistic | estimator | clustering |
|---|---|---|---|---|
| **5a** | **DOSE (GO/NO-GO)** | eviction throws per game, ours | mean, both arms | match |
| **5b** | **MECHANISM (primary)** | **healer-rounds denied**: rounds between an eviction and that builder's return to a ring tile | mean per eviction; total per game | match |
| **5c** | **MECHANISM (secondary)** | **heal ÷ damage on their core**, games with damage > 0 only *(restriction fixed here, before data)* | ratio of per-game means | match-clustered bootstrap, 4,000 draws |
| **5d** | **COST / FALSIFIER** | ring retention (`hold_pinned`, 12-ring stratum) **and** forward sentinel count | game-mean | match-clustered |
| **5e** | **CURRENCY** | game share | — | — |

**5a is a gate: if treatment evictions read ~0 live, the leg is VOID and no other
bar is read.** That is an implementation failure, not evidence about eviction.

## 6. ⭐ RESOLUTION AUDIT — FOR EVERY BAR **AND EVERY GATE**

**This section exists because LOKI-19 ran this audit for every bar except its own
gate, and the gate then under-resolved its own bands** (19 events across 50
games, per-cell n of 6/4/2/7/**0**). **A prereg's resolution table must include
every gate.**

| bar | resolves at 50/arm? | basis |
|---|---|---|
| **5a dose** | **YES** | a rate near 0 vs clearly positive; opportunity is 65–133 rounds/game (§3) |
| **5b healer-rounds denied** | **YES if 5a fires** | one measurement per eviction, hundreds of events expected |
| **5c heal ÷ damage** | **PROBABLY** — a ratio, far less skewed than absolute HP | control-arm heal/damage sits 0.42–0.93 across cells with tight within-cell spread |
| **5d retention** | **PARTIALLY** — ~10 clusters/arm | a large fall visible, a small one not |
| **5e currency** | **NO** | ~±25pp MDE on game share at 10 match-clusters/arm |
| **absolute healing HP** | **NO — AND THIS IS WHY IT IS NOT A BAR** | measured on LOKI-19's control arm: **mean 223.9, sd 412.5**, so MDE ≈ **73% of the control mean at n=50/arm**, 52% at n=100. **22 of 50 games are structural zeros.** |

**The last row is the load-bearing one.** The obvious bar — *"does their core
healing fall?"* — **cannot resolve at any n this project will pay for**, because
the quantity is zero-inflated and wildly skewed. **5b and 5c exist because of
that arithmetic, not because they read better.**

## 7. n, AND WHAT HAPPENS IF THE LEG IS CUT SHORT

**4 interleaved windows minimum — control, treatment, control, treatment — 5
challenges × 5 games = 50 games/arm.** Interleaving is mandatory: a block design
confounds arm with time-of-day and with opponent version drift.
**If the leg is cut short, whole WINDOWS are dropped, never whole cells** — the
per-cell comparison is made only on cells present in both arms.
**Currency needs pooled windows and windows are free** (5/20 min, shared across
`match unrated` and `match test`).

## 8. PRE-COMMITTED LANGUAGE

| outcome | how it must be written |
|---|---|
| dose ~0 live | **VOID.** Implementation failure. No claim about eviction in either direction. |
| dose fires, healer-rounds denied > 0, heal/damage falls with CI excluding 0 | *"eviction denies healing at n=50/arm; underpowered for the currency and a pooled confirmation is now worth the exposure."* **"Confirmed" forbidden.** |
| dose fires, heal/damage CI straddles 0 | **the expected outcome.** *"Dose delivered, mechanism measured, currency unresolved at this n."* **"Null", "refuted", "fails" forbidden.** |
| dose fires, retention or forward sentinel count falls materially | *"eviction buys denial with position/army"* — **may be written plainly**, since it is read against a live in-arm control. **Define "materially" IN THE PREREG with a magnitude and a CI rule** — LOKI-19 had to patch exactly this by amendment. |

## 9. WHAT THIS LEG MAY NOT DO

It may not borrow LOKI-19's or LOKI-16b's bars. It may not read the local dose as
evidence of effect. **It may not compute arrival, retention or any per-opponent
rate on a population pooled across the opponent's versions** — pin theirs from
`league_matches.tsv` / `meta.json`, never `ladder_games.tsv.oppver`, which is
NULL for every row. And **no stored figure from this document enters any bar**:
§2 and §3 select the panel and size the risk; **both sides of every comparison are
measured in-arm.**

## 10. THE HONEST FORECAST, WRITTEN BEFORE THE DATA

**The modal outcome is "dose delivered, healer-rounds denied measured, currency
unresolved."** I expect 5b to fire — the opportunity is abundant and the physics
is simple. **I do NOT expect 5e to move at this n and the table above says so in
advance.**

**And the risk I would name as most likely to sink it is 5d, not 5a:** a launcher
built forward is 20 Ti and +10% scale and it competes with the sentinel that was
going to fire at their core. **If eviction buys denial by giving up the forward
army, that is the trade resolving against the plank and it is a result.**

**⚠ Two of my inputs are arithmetic, not measurement, and are marked as such
wherever they appear:** the ~20–28 HP of denied healing per throw (walk-back at
one step per round, no re-throw, max-range throw) and the Ti-per-HP table. **The
walk-back estimate is exactly what bar 5b measures directly, so the leg replaces
the arithmetic rather than resting on it.**
