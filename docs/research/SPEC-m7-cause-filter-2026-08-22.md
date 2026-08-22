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

---

## VALIDATION RECORD — BUILT AND PASSED, 2026-08-22T18:31:40Z (research s57)

Implemented in `tools/skalman_fidelity.py`: `updateHp` (unum 5, id + signed delta per
`replay_autopsy.py:67`) feeds `dmg_ids` (ids with >=1 negative delta, whole life);
new columns `fwd_turrets_removed_dmg`, `fwd_turrets_removed_by_id_dmg`,
`own_fwd_turrets{,_removed,_removed_dmg}`; new aggregate row **`M7d
fwd_turret_removal_rate_dmg`**; `M7_raw` unchanged (continuity). Corruption control is
`--strip-hp`.

**1. Positive control — REPRODUCED DIGIT-FOR-DIGIT** on the builder's exact population
(the `fwd_theirs`/`fwd_ours` per-entity records of `scratchpad/s54_fc_games.json`,
65 games, classifier = this patch's `dmg_ids`): MIRROR **22/38** · PIVOT **20/50** ·
KLADDE **7/26** undamaged enemy forward-turret kills; ours **0/112** undamaged. All four
match `DESIGN-v629-homeanswer-2026-08-22.md` §S2 exactly.
⚠ Scope note discovered in validation: the builder's cells live on the s54 pool's
per-entity forward records, NOT on M7's (kind, tile, later-round) matching — M7's loose
matching counts rebuilds (e.g. PIVOT cell: M7-matched 58 removals vs 50 per-entity kills).
The CLASSIFIER is what this control validates; M7d applies it to M7's own population, raw
column retained beside it, and the by-id diagnostic now has a dmg variant too.

**2. Corruption control — FIRES.** `--strip-hp` on a MIRROR replay: damage-linked
removals collapse 2+2 → 0+0 while raw counts are byte-identical. The check can fail and
was made to.

**3. Subject-side invariant holds in the shipped row's own note:** our removed forward
turrets read damage-linked == raw in every validation cell (a gap is an instrument alarm
by construction).

First honest readout available (MIRROR cell, n=20 games): M7 raw 37.6 → **M7d 17.7**
(16/82 damage-linked vs 36/82 raw) — consistent with the s56 tail's predicted ~19-33%
honest band. Full re-reads of banked M7 docs remain AT NEXT TOUCH per the routing note.

**4. Standing structural-guard harness, named for the claim-check (2026-08-22T18:41:41Z):**
`tools/skalman_fidelity_selftest.py` is the s54 instrument selftest for
`tools/skalman_fidelity.py` (commit 7f1ffec6b) whose header claims four-plus structural
guards "each driven to both verdicts" — this record is the doc that names it: its guards
(lattice both-ways, chains-shim vs corrupted control, attribution ordering, empty-population
refusal, mirror-column reproduction) are the harness the M7d patch was landed under, and it
was RE-RUN GREEN against the patched scanner this session: **20/20 metrics + 5/5 guards
PASS** (M7 raw row unchanged at its recorded values — continuity verified by the harness
itself, not asserted). M7d's own two controls are §§1-2 above.
