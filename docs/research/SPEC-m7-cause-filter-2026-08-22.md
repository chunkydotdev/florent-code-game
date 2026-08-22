# SPEC — M7 cause filter for `tools/skalman_fidelity.py` (dated 2026-08-22, research s56)

GAME CONTEXT: everything here describes in-game mechanics of the Florent Code League, a
sandboxed bot-vs-bot programming competition.

**DEFECT (verified on the primary this shell):** `scan_replay`'s `removeEntity` branch
(`skalman_fidelity.py:398-408`) appends every removal to `deaths` with no cause linkage, and
M7 (home clearance, computed AGAINST the subject) counts them raw — so an opponent
demolishing its own turret (e.g. lingling v86's 6.0 self-removals/game, relocating defence)
scores as the DEFENDER's clearance. Builder-measured one-sidedness on the first-contact
cells: 22/38 / 20/50 / 7/26 enemy forward turrets "killed by us" with ZERO damage events, vs
0/112 of ours (`DESIGN-v629-homeanswer-2026-08-22.md` §S2).

**FIX:** classify each non-builder removal as DAMAGE-LINKED iff the entity received >=1
negative `updateHp` in its lifetime (window: whole life; no trailing-k heuristic — the
builder's 0/112 shows damage-death always leaves a damage event). Emit BOTH columns:
`M7_raw` (today's number, for continuity with every banked doc) and `M7_dmg` (the honest
clearance). No column is silently replaced.

**VALIDATION (the instrument bar, both directions, before any re-read is quoted):**
1. Positive control: on the first-contact pool, enemy-side undamaged share must reproduce the
   builder's 22/38 / 20/50 / 7/26 cells and `M7_dmg` for our removed turrets must equal
   `M7_raw` (0/112 undamaged).
2. Corruption control: strip `updateHp` events from one input replay — every removal in it
   must flip to non-damage-linked (the check must be able to fail).

**OWNERSHIP:** research patches (instrument is a research read surface); wrap-scoped unless a
decision needs `M7_dmg` sooner. Every doc quoting M7 levels is listed in the coordination
tail note of this timestamp; each gets a rider or a re-read AT NEXT TOUCH, not silently.
