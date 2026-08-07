# Eir 5 surgical map — pieces I / J / H against the ACTUAL `_v74e4` source

Research session, 2026-08-07 ~15:05. Verified line-by-line against
`bots/_v74e4/main.py` (3173 lines, the SHIPPED Eir 4 content). Written because
every findings file specs these pieces against `_v72e2` line numbers, and the
code has moved under them — two of the three specs are partially stale.
STALE-BASELINE RULE applied: everything below was re-read in `_v74e4` today,
not relayed from the findings.

## Headline corrections to the specs

1. **Piece J's target has already been half-built.** Eir 4 added a turret-hunt
   interception ABOVE the universal heal (`main.py:1191-1216`) and a
   defend-role succession heartbeat (`:352-372`, `:1104-1123`), which were the
   two worst consequences of the v72e2 lockout. The residual lockout is real
   but has a NARROWER mechanism (below) — a blanket "move the heal below role
   dispatch" would now be a regression risk for zero gain.
2. **Piece I's site moved and changed shape.** The v72e2 rotate-with-no-check
   loop is gone; Eir 4's `_turret` already has the v44-style priority scan.
   The surviving leak is the IDLE-rotation tail at `:3037-3054` — still no
   `can_fire_from` ray check, still no hysteresis, and it chases nearest
   visible ANYTHING (including wandering enemy builders = the drumlin
   325-rotation game).
3. **`SLOT_HOME_GUN` counts forward artillery too.** The third increment site
   (`:1649`) is inside `_try_siege_build` — the saboteur's FORWARD gun at the
   enemy core increments the same counter the home-defense gates read. The
   findings' "rubble counts as a live gun" understates it: distant live guns
   count as home guns too.

## Piece I — rotation discipline

**Current code** (`_turret`, `:2971-3054`): fire paths all return; if nothing
was fired, `:3037-3045` picks `enemy` = nearest visible enemy entity
(fallback: stored enemy core), then `:3046-3054` rotates a GUNNER toward
`p.direction_to(enemy)` (45° bearing, diagonal allowed), falling back to
`nearest_cardinal`. No ray check (`can_fire_from` is never called in
`_turret`), no memory of the previous target, no cost awareness.

**Measured leak** (thread 12, still applies): 446 rotations = 4,460 Ti across
8 games; worst case 3,250 Ti = 56.5% of income (a5671738 g1 drumlin); 146
A→B→A reversals on one gunner (8ed4d332 g4); each rotate also costs the next
shot (cooldown 1) and 10 Ti that competes with heal/respawn solvency.

**Fix, in these terms** (new toggle, e.g. `ROTATE_DISCIPLINE_ON`):
- Rotate only if BOTH: `ct.can_fire_from(p, want, EntityType.GUNNER, target)`
  is True for the candidate facing, AND the target is NOT already coverable on
  the current facing (`can_fire_from` with `ct.get_direction()` False).
  `can_fire_from` ignores ammo/cooldown by contract — exactly right here.
- Hysteresis (thread-12 spec: 3×): keep `self.rot_tgt`; retarget only when the
  current target is dead/out of range or a new candidate is ≥3× closer (dsq).
- Skip idle rotation toward `BUILDER_BOT` sightings entirely unless the bot is
  inside gunner range r²≤13 AND the ray lands (builders outrun facing; this is
  the drumlin thrash source). Rotating toward the stored enemy CORE bearing
  when idle is harmless (fires once, then `want == current`).

## Piece J — counterbattery lockout + the gun counter

**Where the heal actually sits now:** universal adjacent heal =
`:1218-1238` (fires for ANY builder: cooldown 0 ∧ `SLOT_UNDER` ≠ 0 ∧
`_heal_core` succeeds → return). Above it: the hunt interception
(`:1191-1216`). Below it: role dispatch `:1307-1314`. In `_defend`'s action
phase the order is heal-first-under-shelling BY DESIGN (`:2109-2132` — the
heart lesson), then `_sabotage_prio` → `_try_counterbattery` (`:2123-2126`),
then heal fallback.

**The residual Eir-4 lockout mechanism (new synthesis, this session):** vs a
point-blank battery (Orizon class; Ouroboros endgame), piece D's `_duel_safe`
(`:1351+`) correctly refuses the melee duel → `_hunt_turret` disengages → the
universal heal at `:1236` (or `:2120`) claims the defender's every action →
`_try_counterbattery` at `:2125` is unreachable for the whole siege. The
defender heals +4/rnd into 18-25 dmg/rnd and never buys the turret that would
return fire. Same lockout as v72e2, one layer deeper. Do NOT blanket-reorder:
heal-first is measured-correct for the chip class when a home gun already
stands (heart decode). The fix is role- and state-scoped:

- Exempt ONLY the `role_n == 4` defender from the universal heal (`:1236`) and
  from heal-first (`:2120`) when ALL of: a threat is in band
  (`SLOT_THREAT` within `HUNT_BAND_DSQ` = 41 of the footprint, the `:1991-1994`
  test), NO live home turret exists (next bullet), and
  `ti >= sentinel cost + SIEGE_HEAL_RESERVE_TI` (16, `:273`). Other builders
  keep healing — convergence supplies +8..12/rnd while the defender buys the
  gun. One in-ray turret flips the arithmetic; heal-only was measured losing
  150-900-round sieges before convergence existed.

**The gun-counter half — recommend LOCALIZING, not a store redesign:**
increments at `:1649` (forward siege gun!), `:2048`, `:2052`; zero decrements
anywhere; consumers with DIFFERENT intended semantics:
- `:776` + `:796-798` ammo magazine — wants "guns that drink ammo", lifetime
  count of all guns is roughly fine here; leave it.
- `:1999` counterbattery economy gate — wants "live HOME defense exists".
- `:2218-2225` `hive_freeze` — `_expand` returns unconditionally on hive both
  seats once `SLOT_HOME_GUN ≥ 1` ∧ rnd ≥ 42. With a monotone counter this is
  the confirmed economy self-freeze vs picket classes; and via `:1649` it may
  self-trigger off our OWN forward gun (verify whether `_plan_siege` can fire
  pre-r42 on hive — if yes this bug bites every hive game).
Fix: at the two gate sites, replace the store read with a defender-local live
scan: friendly GUNNER/SENTINEL among `get_nearby_buildings()` within
footprint-dsq ≤ 41. No new slot, no buffered-write clobber trap (store writes
are next-round visible, last-write-wins, core-first — a builder decrement
scheme WILL corrupt), always current. Cost ~a dozen engine calls on defender
turns only. This also defuses `hive_freeze` for free.

## Piece H — endgame spend-switch @ r960

**Core sites:** conversion block `:772-806` — at `rnd ≥ 960` override
`ammo_target` to the whole bank above a small reserve and convert in ONE call
(`convert_ammo` is action-free, once/turn, amount UNCAPPED — engine-confirmed
same-round convert→fire). Spawn gates `:808-863` — optionally lift
`spawn_budget` late (cost scale is irrelevant with 40 rounds left).

**Builder sites:** `_expand` harvester path `:2245-2256` and `_defend`
`:2134/:2146` — at `rnd ≥ 960` bypass `_eco_spendable`/`_eco_cap` and build a
harvester on ANY adjacent ore; skip the medic (`:2283-2307`) and link-building
to free actions. Tiebreak order is delivered → harvesters → stored: the T4 sim
says the switch flips 6/9 current-line r1000 losses (+38.4 Elo equiv), and the
real atoll case was delivered-TIED, lost by ONE harvester.

**Honest intersection caveat (T2×T4):** several flippable games had ZERO
builders alive at r960 — H's realized value in those games also needs the
population-floor work (B'). Ship H anyway (it flips the games where hands
survive, and piece D is now keeping more hands alive), but don't attribute
missing flips to H's mechanism without checking builder count at r960 in the
loss replays.

## Traps for the build (all verified today)

- `NOISE_ON = True` (`:310`) ships; local paired-seed A/B is nondeterministic
  by design — pooled Wilson reads, or flip the toggle in LOCAL copies only.
- B8 is OFF, so `SLOT_THREAT` is last-write-wins in sighting-iteration order
  (`:1028-1061`): under multi-turret pressure the counterbattery may aim at an
  arbitrary one of them. Known, accepted; don't "fix" it inside J.
- CPU phase gates at `:1304`, `:2156`, `:2314` — new action-phase code (H's
  harvester spam, J's counterbattery-first) must stay inside the existing
  action phase, before the BFS move phase, or it inherits truncation risk the
  guards were built to prevent.
- Suggested toggles, Eir-4 idiom: `ROTATE_DISCIPLINE_ON`, `CB_OVER_HEAL_ON`,
  `ENDGAME_SWITCH_ON` — one constant each, ablation grid flips them.

## Screens (RETRO FIX 1 — before any full battery)

- I: drumlin/heart/jackpot (the thrash games) vs opp_v50 + kladde_probe;
  mechanism check = rotation count per game collapses, wins move or hold.
- J: no orizon_probe exists yet (spec in thread-7 findings; freeze queued) —
  screen guards for no-regression (flotte fjordgate/lighthouse 16/16, band
  fjordgate 16/16, the exact maps that set MEDIC_MIN_RND) + decode one
  under-battery replay and count counterbattery builds >1 per game.
- H: eider/atoll/hive r1000 games vs kladde_probe + opp_v50; mechanism check =
  harvester count at r1000 and tiebreak-2 flips.
- Gate per ce93bb3: class-weighted vs-field battery. **CORRECTED ~15:25 — the
  census landed** (`docs/research/2026-08-07-fanout/meta-census.md`, builder
  session's; my in-flight duplicate agent killed). Weights from its §4/§4.3:
  POINT-BLANK BATTERY heaviest (44.3% of classified pool — no probe exists
  yet; Orizon spec + Team 48 v16 / farming_200s v7 / Askar City v72
  aim-policy freezes are the recommended seats), creeping picket next (35.6%,
  ouro-probe + Lunds), economy-first 8.9%, rush 8.9% (band guard),
  kladde-grind LIGHT (2.3% — its legs were over-weighted in every prior
  battery, including my earlier line here). Keep the v89 slot bar.
