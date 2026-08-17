# BUILD REPORT — `bots/_v511sealonly` (barriers-only siege raider), s50 2026-08-17

*Banked by the builder s50 from the opus build agent. Magnus's iteration 2 ("ONLY builds
barriers around the enemy core"), carrying all three fixes from the v510 demo autopsy
(AUTOPSY-v510-demo-midgard-2026-08-17.md). 289 lines across doctrine.py/siege.py/main.py;
eco.py + raid.py untouched; every diff behind `LOKI_FS_SEAL_ONLY` (doctrine.py:2189), False
restores v510.*

## Changes
doctrine.py:2154-2204 (flag block, FS_CLEAR_MAX_PECKS=8, FS_AVOID_TURRET_AXIS) ·
siege.py: `_fs_stale` :136 (replacement defect note) · `_fs_park_seat` :294 (**park on a
DIAGONAL — barrier all 8 orthogonals**, the autopsy's park-seat leak closed) · `_fs_census`
:386 · `_fs_body_blocked` :478 · `_fs_ring_turn` :694-776 (verb gates: no evict/sentinel/heal
for the raider) · `_fs_try_clear` :878-892 (peck cap + defer-and-return) · `_fs_stand_target`
:970 (turret-ray blacklist, gunners AND sentinels) · main.py :484 KILL reserve cleared, :499
RING reserve re-priced (12×bar+margin+6, smallest strictly exceeding `_fs_seal_ok` — the
anti-deadlock constraint).

## Results (5 maps × 6 repeats/arm = 30 games/arm, local --tle 10)

| | **v511** | v511 pre-autopsy-fixes | **v510 control** |
|---|---|---|---|
| orthogonal-8 CLOSED | **9/30 (30%)** | 6/30 | 3/30 (10%) |
| rounds held at full seal | **2,069** | 1,971 | 104 |
| first-full round (closed games) | 44-56 (7/9) | 82-225 | 65/91/300 |
| wins | 7/30 | 6/30 | 8/30 |
| r1000 games (programme defeats) | **2/30** | 5/30 | 6/30 |
| FS-raider heals | **0** | — | 67 |

Per map closed/6: **glacierkeep 6/6** (v510 1/6) · nordkap 2/6 · atoll 1/6 · **midgard 0/6** ·
heart 0/6. Ferry arrival unchanged (r4-15). 3 degrades/30.

**⭐ THE ZERO-LAW HOLDS IN COMBAT, conditioned on state not arm: 2,069 full-seal rounds → 0
enemy on-core heals, 0 spawns**, vs 0.1122 heals/rnd + 0.0236 spawns/rnd over 9,587 open-ring
rounds in the same games. (Raw per-arm heal totals are confounded — an arm with no damage
source gives the defender nothing to heal; hence the conditioning.)

**Flag-off both ways:** False → 15 sentinels/9 evictors/244 evicts; True → 0/0. Raider heals
0 vs 67; attacks 446 vs 200; stderr CLEAR count == replay attack count 446/446 (two
instruments agreeing).

## Autopsy fixes, status
1. **Park-seat leak CLOSED** (barrier-all-8, park on diagonal); the 51/59-heals-from-(28,27)
   figure was independently reproduced before fixing.
2. **Replacement**: fires 13/30 (v510 10/30). ⛔ Agent's first count ("0/30") was an
   INSTRUMENT ERROR (awk field tallied the literal token `id`), corrected. REAL residual
   defect documented at siege.py:136: the heartbeat rides the shared store beat which
   raid.py:174/:191 refresh for ANY established body — replacement declines exactly when the
   ring is contested; needs a dedicated store field (not available in the shared slot; the FS
   raider is lowest builder id and can never write last). Open design item.
3. **Ti reserve re-priced + KILL-cleared**: starvation reproduced first (ammo 0 on every STAT
   line r60-r940 midgard s21); post-fix same fixture reads ammo 53→176.
4. Clearing KEPT but capped 8 pecks/tile with defer-and-return (3 of midgard's 8 seats carry
   the defender's own conveyors — with clearing off the collar cannot close there at any bank).
5. Turret-ray stand-tile blacklist added (both turret types).

## Deviations
Diagonals open when no actionable orthogonal work remains (no kill-window deferral — no
raider-built kill asset exists). Imports the full-12 provocation hazard (field study: median
9-round break vs 56) — prereg must price it. 47 eviction throws still occur from ferry
launchers landing inside the ring role-gate (launcher's turn, not the raider's; kept to
preserve the role gate).

## Surprises
1. ⛔⛔ **LOCAL RUNS ARE NOT DETERMINISTIC UNDER `--seed`**: NOISE_ON seeds an unseeded
   `random.Random()` spawn salt (main.py:571) both sides. Three runs of v510 on midgard seed 7:
   r1000 / r133 / r362 with different openings. **Every single-game read in the v510 build
   report is ONE DRAW, not a fixture.** (Consistent with the s49 law — NOISE_ON pairing
   impossible — now shown to bite single-game reads too.) All v511 numbers are 30-game paired
   grids for this reason.
2. **Midgard is the plank's WORST map, not its showcase** (0/6 both arms; the defender's
   delivery belt permanently occupies 3 of 8 heal seats). The demo choice of midgard was
   unlucky in exactly this way.
3. The pre-autopsy build degenerated into a barrier TREADMILL (226 barriers, 221 on one
   contested tile, bank stalled, r1000 loss) — the peck-cap/defer logic is what fixed it.

## Demos
- **`demos/DEMO-glacierkeep-sealonly-CLOSED.replay26`** — the plank working end-to-end: seal
  closes r50, held 600 rounds, WIN by core kill r650.
- **`demos/DEMO-midgard-sealonly.replay26`** — the honest requested fixture: midgard s21,
  best 7/8, loss r185 (all four s21 runs lost; none closed — see surprise 2).

## Open items
- CPU NOT measured (local `get_cpu_time_elapsed`/`execTimeUs` are stubs — 0 in 200,633
  BotOutput events; the added `get_attackable_tiles_from` sweep needs a platform `match test`
  before any ship — BLOCKED by lock-in mode, needs Magnus).
- Replacement store field (dedicated slot bits) — next design item.
- Midgard-class maps (belt-on-seats) need their own answer or a map gate.
