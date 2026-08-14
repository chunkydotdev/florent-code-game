# SPEC — BEHAVIOUR-FIXTURE LIBRARY: the inventory (research s38, 2026-08-14)

**Origin: Magnus's synthesis of the coupling result** — *"we are blind when
testing experiments that exploit or counter something we don't do — all our
experiments are based toward an opponent such as ourselves."* This spec is
research's half (WHICH habits, ranked, with sources); the builder builds each
fixture with both-verdict validity runs per the s37 pattern. **Standing
caveats inherited from the ask: every fixture documents its lie direction;
pool screens narrow candidates cheaply and NEVER substitute for live n≥50 on
a ship path.**

**RANKING = prevalence-in-field × our-loss-correlation, each with its source.
A habit v125 already exhibits needs no fixture (self-play covers it) — that
is the selection criterion, per the coupling refinement.**

## 1. CHRONIC HEAL-CAMP (ring camp + core-tank + belt-heal at need) — BUILD FIRST
* **Prevalence:** chronic camp (≥100 rnds at d²≤64, camp_detect) in 8/10 of
  tonight's pinned-cell leg games; variants documented in FOUR profile books
  (Leviathan autopsy, team lazy, Juusto, Coreflood).
* **Loss-correlation: the highest measured anywhere in the repo.** Rated
  bleed 6/25 vs Leviathan; CAL-3 −0.231, CAL-4 1/25 (reference cell); rc8.3
  O2 0-5; parked-raider rates 53.5%/55.6% vs camp teams against 8.2% vs
  aggressives; the out-heal arithmetic (4 HP/Ti vs our best 1.8 dmg/Ti).
* **v125 lacks it:** our kill median is r167; we hold no ring (forward
  turret life 7-11 rounds contested).
* **Fixture spec:** the s37 camper, DERATED TO MEASURED RATES — heal uptime
  to Leviathan's actual (their core-heal share swings 7-100% BY NEED — a
  fixed-uptime camper is the wrong bot; key it on damage taken), belt-heal at
  their measured 127-heals/game shape.
* **Lie direction:** camper v1's measured defect — its healers held the core
  seats, starving melee adjacency (fixture-geometry false negatives for
  adjacency planks). And a NEED-keyed healer is still more regular than a
  real one: overstates defence coherence, understates our burst value.

## 2. POINT-BLANK CREEPER LADDER — EXISTS, needs derating check only
* **Prevalence:** LingLing40 (80 siege turrets/15 games, 58/80 gunners,
  median d²=5 from our core, rebuild latency 1-2 rounds) + team lazy v222
  (48 turrets, median d²=5) — two of our five most-played, map-controlled.
* **Loss-correlation:** the r150-250 window (our core dies in 46.3% of
  games); #45's provenance.
* **v125 lacks it:** we never ladder (forward share 35.9%, sentinels at
  range).
* **Fixture:** `_probe_creeper` EXISTS, both-verdict validated s37.
* **Lie direction (documented at birth):** rebuilds unconditionally, never
  retreats — overstates the renewable-turret premise, so a treatment null
  vs it is harder to excuse, not easier. Field-rate derating optional.

## 3. BELT-REPAIR-AT-FIELD-RATE — the repairer does not exist; build second
* **Prevalence:** 40.5% of the field repairs belts (salt's registered
  basis); Leviathan measured at 127 conveyor heals vs our 79 cuts in one
  game.
* **Loss-correlation:** moderate and indirect — but it is the habit behind
  BOTH confirmed transfers (salt's tax pays because repair is universal;
  TWORAID transfers because out-damaging heal is universal). **This fixture
  is what makes the coupling refinement TESTABLE locally**: a salt-class
  plank screened vs the repairer should transfer at face value.
* **v125 lacks it:** we cut belts; we do not repair them at field rate.
* **Fixture spec:** simple belt-layer + repair-on-cut at the field median
  rate (derive the rate from build_agg heal rows, not from Leviathan alone —
  he is the extreme).
* **Lie direction:** a dedicated repairer repairs PROMPTLY — overstates
  repair responsiveness, biasing salt-class screens toward false negatives
  (the safe direction for ship decisions).

## 4. BURST-SPAWN REACTIVE SENTINEL WAVE — the 1800-band's kill mechanism
* **Prevalence:** Leviathan documented (3 builders spawned in 3 rounds →
  4-5 sentinels at d²16-41 within 5-9 rounds of first blood; kill lands
  14-53 rounds after); "thin pre-defence, heavy reaction" shared with lazy
  (next-door counter-gunner +1 round).
* **Loss-correlation:** this + heal-camp IS the Leviathan loss mechanism
  (net core damage 0/0/14/0 HP in the four autopsy losses).
* **v125 lacks it:** our spawning is eco-paced, never burst-reactive.
* **Fixture spec:** trigger on damage-to-own-structures → burst spawn →
  stand-off sentinel wave at d²16-41.
* **Lie direction:** a scripted wave is more punctual than a need-based
  one — overstates the field's reaction speed (safe direction for testing
  our window-of-opportunity planks).

## 5. TERMINUS-FIRST WIRING — trivial to build, doubles as #50's opponent
* **Prevalence:** near-universal at the top (SmartFridge 100.0% n=3,260,
  kladde 99.6%, diverge/Focalground 100.0%; field 20,540 wire-first sides).
* **Loss-correlation: UNMEASURED** — that is #50's bank_trace go/no-go.
  Ranked low on evidence, high on prevalence; build only when #50 needs it.
* **v125 lacks it:** 99.7% harvester-first.

## 6. ORE-BARRIER DENIAL — HOLD until #49's cut reads
* Jython on icefloe (Magnus-observed); prevalence and bind both unmeasured.
  Admitting a fixture before the free cut answers BIND-vs-theatre would
  invert the cheap-first order.

## Explicitly NOT fixtures
* **Launcher eviction/kidnap** — v125 exhibits it (self-play covers it).
* **Version rollback / A-B behaviour** — meta-level, not in-game.

## Library-wide rules (from the ask, restated as spec)
1. Every fixture ships with both-verdict validity runs (s37 pattern) and its
   lie direction in the source header.
2. Pool screens carry a stated-bias caveat inline in every readout.
3. **The pool narrows; live decides.** No ship recommendation cites a
   fixture-pool screen as its live evidence — the n≥50 live bar stands.
4. Fixture rates derive from MEASURED numbers with the source named (a
   fixture constant without a source line is the s36 interpolation defect).
