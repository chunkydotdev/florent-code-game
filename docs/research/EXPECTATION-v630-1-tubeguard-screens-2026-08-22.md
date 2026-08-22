# REGISTERED EXPECTATION — v630.1 TUBE GUARD screens (post-attribution iteration)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition under organiser-approved rules; "kill" /
"death" = in-engine unit removal between game bots.**

**PROVENANCE:** typed by BUILDER s57 (v623 precedent: expectation committed
pre-readout). Inputs: `BUILD-REPORT-v630tubeguard-2026-08-22.md` (v630.0
verdict + D14 rider), the E6 attribution (tail 19:11:10Z, scripts
`scratchpad/s57_v630/e46_attrib*.py`), and this lane's keeper code read
(restated in §1 so its primary lives in a builder artifact). **Committed
before any v630.1 identity/ON tape is generated or read.**

**TREE:** `bots/_v630tubeguard` iterated in place (v630.0 → v630.1; git
history preserves v630.0; the screen that refused v630.0 is banked). Changes:
(a) **terminal-only approach bias** — seat targeting engages only within
d²≤`SK_TUBE_GUARD_NEAR`(=8) of the site/hold, so the macro path is v628's
line for line (the E6 attribution traced all 9 flipped F1 cells to r4–45
macro-path divergence); (b) **band-scoped heal rung in the SITING path** —
`_near_live_tube` gate (d²≤8 of a live ledger tube) so the rung can fire
after a first tube death without ever stalling a home-territory walk
(v630.0 measured 1 heal event in 60 ON games; the hold-only rung was
unreachable when it mattered).

---

## 1. THE KEEPER MECHANISM, CONFIRMED IN CODE (this lane's read, own anchors)

The v630.0 E6 regression ran through OUR core dying more (16→21 cells), not
through kill tempo (rounds-to-500 = 121.0 both arms). The cascade's staffing
mechanism, confirmed by direct read of `bots/_v628compose/sk_roles.py`:

* **The home keeper has no damaged-building walk.** Its heal
  (`_heal_action`, :1443-1447) targets via `get_tile_building_id` on
  cardinal-adjacent tiles only — buildings only, adjacency only; a damaged
  forward builder or a remote damaged barrier is never a walk target. The
  "damaged-forward-attractor" hypothesis is REFUTED (and research's 14-row
  rider enumeration built on it was retired unstamped).
* **What ranges the keeper is its ECONOMY walk**: `_home_keeper_move`
  (:3855-3960) falls through medic-seat (dead flag, below), escalated
  shooter (fenced d²≤100 of our core, :3374-3402), seat/apron/gun walks
  (bounded), and lands on the belt/ore walk whose targets are fenced only by
  `is_home_half` — **no d² term** — so the plan legally holds the keeper at
  d²>50 from the core for long stretches of a long game. The docstring's
  "never leaves the home quadrant" is aspirational, not enforced.
* **The recall mechanism exists and is OFF**: `SK_CORE_MEDIC`
  (sk_maps.py:1009) was built, measured in the v607 era, and declined — on
  shapes where the keeper banked **694 incidental core heals / 30 games** by
  standing home. Under v630.0's shapes that channel measured **80**. The
  declination's premise is era-bound; re-testing is queue row **#128**
  (research-admitted), not part of v630.1.
* **Length coupling**: longer/contested games execute more of the belt plan
  (keeper out more). Any plank that lengthens games drains the incidental
  core-heal channel — the standing diagnostic research attached to powered
  reads (E6 core-footprint-heals cell).

v630.1 does NOT fix the keeper (that is #128's row). It removes the guard's
own contribution: the opening-corridor divergence that reshaped games.

## 2. FIXTURES

Same as v630.0: 15 maps × 2 seats, F1 = NOISE_OFF `_v542wave` seed 7, F2 =
NOISE_OFF Mjolnir seed 11, runner `scratchpad/s54_v620/tape.sh`. **Control
tapes reused from v630.0** (`t_ctrl_f1/f2` — same host, same session, same
load discipline; the cross-host caveat does not apply). New tapes:
`t_id1_*` (flags off), `t_on1_*` (mkarm `SK_TUBE_GUARD=True`).

## 3. REGISTERED LINES

**E1 identity:** `t_id1_*` ≡ `t_ctrl_*` 30/30 per fixture (rdiff per cell,
checker already driven both ways this session). *Falsifier: any divergence =
OFF-conjunction leak; halt.*

**E2 liveness:** ON diverges from control in ≥8/30 cells per fixture.
*Falsifier: 0 = dead flag; 1–7 = under-reached; halt either way.*

**E2b OPENING INVARIANCE (the v630.1-specific line):** across ALL divergent
ON cells on both fixtures, **no first behavioral divergence before r8**
(v630.0's nine flipped cells diverged r4–r45, earliest r4 — the macro-bias
signature this iteration removes). *Falsifier: any cell diverging < r8 means
the terminal gate leaks through some other path — back to code, do not read
levels.*

**E3:** traceback count on ON cells — **concurrent observation / health
check, not a prediction** (the v630.0 relabel, applied at registration this
time): expected 0.

**E4a′ FRONT-SHARE (the promised registered bar, side-lane rider honoured):**
per-barrier FRONT share of prep barriers in the ON arm **≥ 0.40 on each
fixture AND ≥ +0.10 over the same-session control's share**.
*PROVENANCE, stated per the rider: these numbers are CALIBRATED ON v630.0's
measured shares (ON 0.451 F1 / 0.506 F2 vs control 0.298 / 0.245) — this is
a registered REPRODUCTION of a mechanism sized from the prior screen, not a
blind prediction.* *Falsifier: share below bar or contrast below +0.10 ⇒ the
terminal-only bias no longer steers placement (the last-two-steps geometry
was insufficient) — mechanism lost, back to design.*

**E4b′ HEAL DOSE:** **≥3 heal events on tube or screen-barrier tiles per
fixture's ON tape** (v630.0 measured 1 across both; the siting-path rung is
the change under test). *Falsifier: <3 on either fixture ⇒ the rung is still
unreachable in practice; the babysit half is refused a second time and gets
dropped from the plank rather than iterated again (two strikes).*

**E5 LIFE DIRECTION, with the censoring discipline built in:** ON
forward-turret survival non-decreasing vs control on F2, read
**horizon-normalised (h=50 and h=100) and cell-matched** — the pooled
censored median is reported but cannot carry the line (two censoring-family
catches today; fixed-horizon comparators are the standing form).

**E6 TIMELY-CHECKMATE GUARD:** ON F1 by-r300 core-kill count within **−2**
of control (v630.0: −6, fail). **AND the attribution's channel watched
directly: our-core-death cell count on F1 within +2 of control** (v630.0:
16→21). *Falsifier: either miss ⇒ the guard still costs the race; the
composite is refused and the plank is decomposed (bias-only arm vs
heal-only arm) before any further composite iteration.*

## 4. MDE / SCOPE (OB16)

n=30 deterministic cells per fixture per arm; game-share-style MDE ≈35pp —
**no level sentence from this screen.** Levels belong to the registered
powered grid, which is reached only if E1–E6 above clear. The phantom-death
confound registration carries over from v630.0 unchanged (total-effect
adoption, plants/`nest_lives`/life/adjacency co-diagnostics).
