# Thor brief — the win-condition layer (Move 2 design, 2026-08-07)

Research session (Fable). Design spec for the builder session; no code here.
Names per convention: **Thor** = offense (reserved until now), **Loki** =
denial/harassment. Eir remains the heal/survive line underneath.

## Thesis

The plateau is structural, not incremental. Five locally-green ship cycles
since the 1597@169 peak converted to ~zero ladder Elo (1546 @ 247, #24→#28),
and the ladder inflated under the in-family ceiling estimate: +150-250 from
the remaining queue lands ~ranks 15-19 on TODAY'S board, not top-8. What no
queue item addresses:

- **We have no way to win a game the opponent doesn't lose for us.** All five
  decoded classes take initiative; we return 178 dmg for 7,818 taken (T12),
  fire 13 shots/1000 rounds on 2,782 banked Ti (atoll), and have literally
  zero `destroy()`-class aggression: harassment measured only ever against us
  (819/708/905 consecutive rounds of one builder's action budget defending a
  3 Ti conveyor).
- **Seat B playing for round 1000 is playing to lose**: 9/9 corpus tiebreaks
  went to seat A; three defensive seat-B counters failed (blanket deferral,
  second gun, threat-conditional deferral). Meanwhile Powerpuff beats the
  seat-B tax 4/5 **by being the aggressor** — the tax falls on exposed melee
  builders and tiebreak resolution, and initiative sidesteps both.
- **The picket family (Ouroboros, Orizon — two of six nemeses, both in or
  near our pairing band) commits everything forward.** Orizon fields 4
  builders ever and parks its whole army at OUR core; Ouroboros is
  script-static per (map, seat). Against an all-in, script-static opponent, a
  counter-strike hits an empty house. Our 5 CtrlAltDefeat wins are all fast
  core kills r117-215 — when we ever commit, it already works.

## Design principles

1. **Layer, not rewrite.** The economy engine is our unique asset (tiebreak-1
   majorities, delivered-Ti wins). Thor is a coordinator + triggers on top.
2. **SPAARK rule holds**: every mechanism below has decoded replays behind
   it; conservative trigger values first, observed, then widened. No
   last-minute swings before Stockholm.
3. **Seat-aware, class-aware, toggleable.** Separate constants per arm
   (THOR_ON, THOR_B_ON, LOKI_ON) for the ablation grid.

## Inventory — Eir 4 already contains most of the machinery

This is the de-risking fact: Thor is mostly WIRING, not new subsystems.

| Existing subsystem | Where (_v74e4) | Thor gap |
|---|---|---|
| Siege planner + forward gun builder | `_plan_siege` :1505, `_try_siege_build` :1622, SLOT_SIEGE | fires opportunistically; needs a bank/round TRIGGER and sentinel-preference at strike time |
| Launcher insertion w/ claim+ACK + leapfrog advance | `_launcher` :3056-3173 | already throws saboteurs at the enemy core; needs escalation (2nd body) on trigger |
| Saboteur role + promotions | role_n 0; :1144-1152 promotions | needs a "strike" mode: prefer building the kill sentinel over pecking |
| One-round bank→ammo conversion | `_core` :772-806; uncapped, action-free, same-turn usable (engine-confirmed) | needs the terminal override (piece H) and a strike override |
| Turret priority scan prefers CORE | `_turret` :2995-3030 | healer-first variant already exists for snowflake (:3010-3017) — generalize as strike option |
| Escort/heal-in-passing | chain medic :2257-2307, escort logic in saboteur | siege sentinels need 1 escort healer to outlast melee (40 HP vs 2 dmg/peck) |

## Thor-T — terminal strike protocol

**Ammo math:** core ≈ 504 net HP; sentinel 18 dmg / 10 ammo / reload 2. One
sentinel: 28 shots = 280 ammo, ~56 rounds. Two sentinels: ~28 rounds, 560
ammo worst case. Their heal offset (we offset 52-79% when defending — assume
symmetric) argues for the two-sentinel + healer-suppression variant. Budget
600 ammo ≈ 600 Ti — **we die with 2,700-3,000 banked.** The money exists.

**Trigger (staged):**
- Stage 1 (ships with Eir 5 as piece H, already validated by the T4 sim,
  flips 6/9 r1000 losses): `rnd >= 960` → convert bank, harvester spam, fire
  everything.
- Stage 2 (Thor proper): `rnd >= THOR_MIN_RND (700)` ∧ `ti >= THOR_BANK
  (1200)` ∧ home quiet (`SLOT_UNDER == 0` sustained ~30 rounds) → escalate:
  launcher throws role_n 3 (+ one replacement seat) to the enemy core ring;
  siege builder wires TWO sentinels with clear lines (sentinel lines are
  never blocked — barriers/bodies don't help them); core converts the bank in
  one call; turrets run kill-priority (healer-first if their builders are
  parked adjacent — the Orizon fingerprint — else core-first).
- Stage 3 (only after Stage 2 reads green in production): class-triggered
  early strike vs picket fingerprints (gunner-only opponent, zero
  sentinels/launchers seen by r150 = Ouroboros/Orizon family with p≈1) —
  their home is empty by construction.

**Counterplay analysis:** script-static classes cannot respond (Orizon never
rotates; Ouroboros deterministic). Adaptive teams punish an overextended
strike — hence the quiet-home + surplus-bank gates: the strike spends only
money and bodies the defense demonstrably isn't using. kladde's own strike
trigger is ammo>=150 (7/7 games) — if we see their wave forming (their ammo
is invisible, but wave timing is decoded: first r137-314, then every
~150-165), don't launch into it; THOR_MIN_RND=700 clears kladde's first two
waves on median timing anyway.

**Known risks:** friendly fire on thrown builders standing in our sentinel
lines (measured: our gunner killed our own builder #3) — drop sites must
avoid our planned firing lines; unit-cap interplay is a non-issue at
MAX_BUILDERS=5 vs cap 50; CPU — reuse existing phase gates.

## Thor-B — seat-B posture

`ct.get_team()` is known at r0; turn order (global ascending unit-ID) makes
seat A resolve first all game. Change NOTHING about the seat-B opening (three
refutations say the opening isn't the leak). Change the COMMITMENT: as seat
B, lower THOR_BANK / THOR_MIN_RND one notch (e.g. 900 Ti / r600) — because
seat B's alternative, the r1000 tiebreak, is a measured 0/9. Seat A keeps
Stage-1-only defaults (its tiebreak wins are real wins; don't spend them).
One constant pair, gated on team — the cheapest true seat-conditional play,
and the first one aimed at the win condition instead of the exposure.

## Loki — denial + attention tax

Inputs land in `docs/research/denial-book-2026-08-07.md` (agent in flight):
per-(map, seat) first-turret plant tiles + full opening sequences for
Ouroboros/Orizon (+Flotte/Landers where observed), each marked
DENIABLE/TIGHT/UNREACHABLE from our spawn ring.

- **Denial mode:** where DENIABLE, occupy the plant tile with a 3 Ti
  conveyor/barrier before their plant round (they are deterministic; a taken
  tile at minimum displaces the picket outward — every dsq step outward is
  rounds of walking and worse angles — and may derail the script entirely;
  measure which in probe legs). Cost: 3 Ti + a builder detour on maps where
  we already know the opponent class... which we DON'T know at r6. So Stage 1
  of Loki is map+seat keyed only where the plant tile is useful against the
  whole field (a tile near OUR core denies every picket class at once — the
  wired-economy insight from thread 6: a conveyor denies a plant tile at the
  same 3 Ti and stays bot-passable and delivers). Fingerprint-triggered
  denial (r6 sighting → tile) only for tiles inside our natural opening path.
- **Attention-tax mode:** one builder stationed at their farm lane, pecking
  conveyors (2 Ti/2 dmg kills a 20 HP conveyor in 10 rounds; their stateless
  relay costs 3 Ti + 1% scale each time — the bill we've been paying, run in
  reverse). Target selection from the denial book's economy maps. Gate: only
  from surplus (post-ECO_NEED), only vs non-rush classes, disengage on
  gunner threat (piece D's _duel_safe already provides the discipline).
- **Flotte core-shield (ride-along, next-cycle verification):** Flotte never
  targets the core (0/29, single-match provenance) — any body on the
  besieging sentinel's line postpones core damage indefinitely. If verified,
  the escort/converge machinery gains a "stand IN the line" placement rule vs
  the chip class. Composes with the jackpot theft build (their 7W-31L map).

## Expected effect by class (honest priors, to be measured)

| Class | Thor-T | Thor-B | Loki | Basis |
|---|---|---|---|---|
| Picket (Ouroboros, Orizon) | HIGH — empty house | HIGH (Ouroboros pairing is seat-B locked in production) | HIGH — deterministic plants | 13-replay decode; 4-builders-ever |
| Grind (kladde) | MED — time strike between waves | MED | MED — treadmill camper is the real target | wave timing decoded |
| Chip (Lunds, Powerpuff, Flotte) | MED-LOW — they keep home guns | MED | core-shield + theft | Flotte 0/29 core shots |
| Rush (band class) | NONE (game over early) | — | NONE | keep guards green |
| Econ race (eider-style) | HIGH — they never defend | HIGH | LOW | eider: both cores full HP at r1000 |

## Kill criteria (pre-committed, Eir 3 discipline)

Roll back a Thor stage if: guard bars regress (band/flotte legs), or
core_destroyed-AGAINST rises in the strike window (overextension signature),
or the stage's target metric (core kills FOR vs picket/econ classes; r1000
loss share) fails to move over its 20-match production read. Write the
criteria on the tape at ship time.

## Build order

1. Eir 5 ships pieces I/J/H (surgical map) — H is Thor Stage 1.
2. Thor Stage 2 + Thor-B constants (small: trigger + escalation wiring over
   existing subsystems) — gate on the class-weighted battery once
   meta-census lands; heavy ouro-probe/kladde legs.
3. Loki denial constants from the denial book + attention-tax mode — screen
   vs ouroboros_probe (frozen today, md5 8828b5d5…) and orizon_probe (spec
   ready in thread-7 findings; strongest instrument candidate — build it
   with this).
4. Stage 3 (fingerprint-triggered early strike) only after Stage 2's
   production read.

## CENSUS RECONCILIATION (added ~15:30, after meta-census.md landed)

`docs/research/2026-08-07-fanout/meta-census.md` (builder session) corrects
this brief in two load-bearing places. The corrections make Thor MORE
specific, not less necessary.

**1. The identity premise was overdrawn.** §3.1: our live bot's production
profile is a *sentinel core battery with a small economy* — median 3
harvesters built, 820 Ti delivered, 68% of our damage aimed at enemy cores,
first aggression r14 at aim-distance 0.0, only 7/38 games reaching r1000.
"We have no win condition" is wrong as stated; the truth is worse: we are a
HALF-COMMITTED HYBRID — a battery bot without the battery class's killing
power (they are 44% of our pool and specialized at it) and an "economy meta"
without a production economy (sporks, the existence proof at #2/1960,
delivers 4380 median to our 820 and keeps 13+ harvesters alive to our 3).
Thor's job restated: COMMIT BOTH ARCS — the survivability/economy pieces
(D/J/B'/I) make the economy real; Thor makes the strike real. The thesis
numbers I cited (178 dmg returned, 13 shots) were loss-subset figures, not
the production median — the plateau mechanism stands, the framing is fixed.

**2. Trigger staging must be class-aware — the game-length data kills a
one-trigger design.** Battery-class games median 114-136 rounds (team lazy
114.5, 0033 136); picket kills land r226-427; rush ends ~82. A Stage-2
trigger at r700 NEVER FIRES in exactly the games where the pool lives.
Restaged:
- Stage 2 (quiet-home surplus trigger, r700/1200 Ti) fires only in
  grind/economy/adaptive LONG games — it is the tiebreak-flipper. Correct as
  designed, but it addresses ~11% of the classified pool, not 80%.
- The 80% (battery+picket) answer is the RACE: piece J's counterbattery +
  convergence extends OUR core's clock past r250-450, while Stage 3's
  counter-strike (launcher + saboteur + sentinel at their core, funded by a
  mid-game bank convert) shortens THEIRS — their houses are measured-empty
  (team lazy: zero sentinels/launchers/barriers in 10/10, 0-1 harvesters;
  Orizon: 4 builders ever). Stage 3 must therefore trigger DURING the siege
  (~r120-200, on the battery/picket fingerprint: gunner-only opponent, zero
  sentinels/launchers seen, aim-at-core), not after it. This inverts the
  build order below: Stage 3 is no longer last — it is the second deliverable
  after Eir 5, gated on the new battery-class probe seats (census §4.3:
  Team 48 v16 / farming_200s v7 / Askar City v72 aim-policy freezes +
  orizon_probe).
- Weights correction carried from the census: kladde-grind is 2.3% of the
  classified pool — Stage-2-vs-kladde-waves logic stays but its battery
  weight drops accordingly.

**3. Sporks changes the study queue, not this spec.** Brief-b thread 1 (their
screen mechanism: 35% damage-to-units defensive share behind a 0.61-of-
separation sentinel screen, economy scaling behind it) is the survivability
arc's existence proof and is being decoded separately. If their screen rule
is portable, it slots UNDER Thor as the thing that keeps the economy alive
long enough for either win condition to matter.
