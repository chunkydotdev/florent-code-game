# BUILD REPORT — `bots/_v600skalman1` (SKALMAN v1, the founding tree)

**Builder s54, 2026-08-21.** Built by a fresh opus agent against
`docs/SKALMAN-DESIGN-2026-08-21.md` (incl. the mid-build §2.8 coverage amendment, relayed
and applied) + `SKALMAN-IMPORT-MANIFEST-2026-08-21.md` + playbook §6. Verified by the agent
(5 checks, each driven both ways) and spot-verified by the builder in-lane (line counts,
forbidden-form AST scan CLEAN, disclosed edits present). **No submit, no platform matches,
no game-share claim anywhere in this report.**

## Tree (2,972 lines: ~2,600 player logic + ~100 imported map data; verbatim imports ≈566)

main.py 152 (Player/run wrapper/dispatch) · sk_maps.py 417 (constants + imported map data
+ map layer) · sk_common.py 674 (verbatim lifts + in_bounds + tile arbiter + displacement
guard + V7) · sk_core.py 229 (drip, spawn plan, threat publication) · sk_roles.py 1,500
(the four roles + turret behaviour, all new). Manifest ranges imported at the marked cut
points; F2 restated as pattern only; `_move` rewritten pave-free 51→14 lines; the
`FS_V534_MAPTRUST=False` legacy branch deleted (it IS the v123 bug). One in-lift edit per
manifest §6.3.2 (mirror re-keyed `self.idx&1` → `self.role_parity`). Cut-line correction
vs manifest: eco.py cut at 224 (def at 218, guard at 222/223, AST-checked), not 223.

## Verification (all driven both ways; aliveness only, zero quality claims)

1. AST: 5/5 parse; forbidden forms (finally/BaseException/SystemExit) CLEAN with a DIRTY
   positive control; an undefined-global scan added and driven — it caught a real
   `NameError` pre-battery (the class `ast.parse` cannot see).
2. 8/8 local games vs `_v542wave` (inv_small12/atoll/midgard, both seats) complete: 0
   tracebacks, 0 CPU-guard trips, 0 exception deaths. All 8 lost core_destroyed r96-271 —
   recorded as aliveness, the old line currently kills the new one.
3. Forced-raise drive (scratchpad copy): raising unit survived r40→r105 with report-once;
   wrapper-removed control died permanently after 1 turn. Design §6.2 driven both ways.
4. Flag ablations read via `tools/skalman_fidelity.py`: SK_DRIP off ⇒ 0 converts (control
   69) · SK_ORE_DENY off ⇒ 0.0% ore barriers (control 8.3%) · SK_CAGE off ⇒ 0.0% ring
   share (control 66.7%). Other verbs' signatures intact under each ablation.
5. Drip sanity (6 games): 161 converts, 95.0% on the 4/10 lattice, first convert median
   r42, r0 in 0/6, peak median 20.

## Incidental fidelity read (n=6, NOT a verdict, misses attributed per-verb per §6.3)

M4c nest band 100% in-band / 0% point-blank (design-conform) · M6b/c ore denial 100%
coverage at latency 1 · M5a 4 builders, fourth at r3 · drip lattice 95.0% (target ≥97.3),
calls 22.5/game (target ~67), first convert r42 (target ~r27.5) — drip misses entangled
with turret mortality (need-based drip under-fires when turrets die) · **M1 belt
connectivity 14.3% (2/14 harvesters alive at end) — THE WEAK VERB, attributed to
SK_BELT/HOME KEEPER survivability. v601's iteration target #1.**

## As-built deviations from the design (all disclosed, design §7 updated)

1. Slots 10-13 = per-role beats (4×11-bit beats don't fit one word); phase-2 keeps 14-15.
2. Slot 7 pack_tile (10-bit) not pack_pos.
3. Forward turrets: SIEGE ENGINEER only (one-writer slot 8 + the 0-ammo-fire raise hazard).
4. Two-bot column handoff NOT implemented (arbiter + lap skip-ahead only) — deferred, open.
5. V5 yield: ORE DENIER only (walker-inclusive yield cost every seal in a measured game).
6. COPY 9 eviction second-pass only (gated on no empty seals — measured 9-round chew death).
7. `SK_DOOR_GUN_CAP = 2` added (uncapped bought 6 gunners, +20% scale each).
8. §2.8(b): belt-coverage term in home-gun siting + the uncovered-belt-tile gap MEASURED
   and published on slot 5 b18-23 (no re-siting in v1, per the amendment).

## Engine facts banked (each measured in this build, worth the permanent record)

* `_bfs_direction` returns CENTRE when the target is the walker's own tile — "walk to
  nearest plan tile" deadlocks underfoot (keeper stood still r19→end in a measured game).
* A builder can BUILD ITSELF INTO A BOX permanently — guarded now via
  `free_neighbours(exclude=build_tile)` on every build site + a destroy-escape with a
  30-round tile ban (the ban prevents V8-class thrash).
* An enemy BODY on the next lap tile freezes a naive cage lap (buildings clear, bodies
  don't) — fixed with skip-ahead.
* The wrapper took an unplanned live drive: a genuine NameError fired mid-game; the unit
  survived, the game completed, report-once held.

## §6.4 ADDENDUM (builder, s54 — completing the ablation set after a side-lane flag)

The build agent drove 3 of 7 flags; the original status line over-claimed §6.4 and is
amended below. The remaining four were driven by the builder on a deterministic fixture
(NOISE_OFF copy of `_v542wave`, inv_small12/atoll/midgard, seeds 1-3, 3 games/arm + a
3-game shared control; replays + logs at `scratchpad/s54_fidtape/`), read via
`skalman_fidelity.py --dir --side 0 --deff 0.98`:

| flag off | its metric, control → ablation | identity shape |
|---|---|---|
| SK_NEST | M4c/d sentinel builds 2/2 in-band → **0/0 builds** | CLEAN — signature vanishes |
| SK_DOOR | M7 removal 16.7% (1/6 turrets) → **0.0% (0/5)** | direction-clean on THIN events (control's own base is one removal) |
| SK_BELT | M1 connectivity 16.7% (1/6 harv) → **0.0% (0/1)** | present-but-thin — the verb's positive signature is weak even in control (the known weak row) |
| SK_ROLES | cage 10/14 barriers → **0/0** · drip median 27 → **0** · builders median 5 → **9 (mean 9.33, max 10)** | **CHASSIS COLLAPSE, not a leaf no-verb signature** — SK_ROLES is the dispatch backbone; identity demonstrated BY the collapse (multiple verb signatures vanish at once, the spawn cap disappears), stated as such |

Cross-verb signatures stayed alive under each single ablation except roles_off (the
backbone). One additional observation from the shared control, recorded not spun:
**M5a counts DISTINCT builder ids = median 5 / max 8 vs BC's 4.0** — our role bodies die
and are replaced (BC's modal game has zero deaths); the living count respects the cap but
builder MORTALITY is part of the same weak-row cluster as the belt.

## Status (amended s54, supersedes the original line)

**FOUNDED. §6.1, §6.2, §6.3 (misses attributed), §6.5 satisfied per the build agent's
drives; §6.4 now 7/7 flags driven** — 3 by the build agent, 4 by the builder per the
addendum above, with each identity's shape named (clean / thin / collapse). Next: a
gate.py-governed fidelity battery at real n vs the frozen benchmark for the phase-1
parity table, and v601 opens on the belt verb (now with builder mortality attached to it).
