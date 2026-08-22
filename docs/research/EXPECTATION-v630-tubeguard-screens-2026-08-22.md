# REGISTERED EXPECTATION — v630 TUBE GUARD deterministic screens (F1/F2)

**GAME CONTEXT: everything below is in-game analysis for the Florent Code
League, a sandboxed bot-vs-bot programming competition on a simulated grid
under organiser-approved rules. "kill", "death", "enemy" refer exclusively to
in-engine unit removal between competing game bots.**

**PROVENANCE:** typed by the BUILDER s57 session (the lane that owns the
verdict), per the v623 precedent (expectation committed pre-readout, prediction
and readout separated). Inputs: the ratified design decisions on the
coordination tail (18:41:57Z note, repaired), the opus design read (banked in
the tail notes), `STUDY-drip-collapse-decomposition-2026-08-22.md`,
`scratchpad/s56_probe_barrier` (occlusion probe). **Committed BEFORE any
flag-ON tape is read** — the chain (`scratchpad/s57_v630/runchain.zsh`) runs
control tapes first; this file's commit precedes the first `t_on_*` readout.

**TREE:** `bots/_v630tubeguard` = `bots/_v628compose` + `SK_TUBE_GUARD`
(default **False**), three call-site changes in `_siege_engineer` (heal rung
ahead of the STAGE gate; enemy-side seat bias for prep walk and hold; helper
`_guard_seat`). ON arm: `scratchpad/s57_v630/arm_on` (mkarm-verified
`SK_TUBE_GUARD=True`).

**FIXTURES:** the s54 deterministic tape — 15 maps × 2 seats, seed inert
(both bots deterministic; vary MAP and SEAT never seed): F1 = NOISE_OFF
`_v542wave` seed 7, F2 = NOISE_OFF Mjolnir seed 11, runner
`scratchpad/s54_v620/tape.sh`. Fresh control tapes run this session under the
same load discipline (the cross-host non-determinism finding s56 means no
inherited tape is a valid comparator; same-host fresh runs are).

---

## Registered lines (each with its falsifier)

**E1 — FLAGS-OFF IDENTITY (gate for everything else):** `t_id_f1` and
`t_id_f2` (the committed tree, flag False) reproduce the fresh control tapes
**30/30 turn-identical per fixture** (`tools/rdiff.py` per cell).
*Falsifier: any diverging cell ⇒ the OFF-conjunction leaks; build defect;
nothing downstream is read until fixed. (v622 lesson: identity is RUN, never
asserted.)*

**E2 — LIVENESS (the anti-weld line):** the ON arm diverges from the fresh
control in **≥ 8/30 cells on each fixture**. Basis: the guard's first
divergence point is the engineer's walk target during prep, which is reached
in every game that plants a tube; the control partition (30 F1 games) shows
BOUGHT 67 with tubes planted in the large majority of games.
*Falsifier: 0 divergent cells ⇒ the flag is dead at its call sites (weld
class, fourth instance) ⇒ HALT, diagnose before any further step. 1–7 cells ⇒
under-reached; diagnose which gate starves it before screens are read as
levels.*

**E3 — NO NEW UNIT DEATHS:** 0 tracebacks in ON-arm logs; the per-game
engine traceback grep in tape.sh stays clean on all 60 ON cells.
*Falsifier: any traceback naming the arm's code ⇒ build defect.*

**E4 — DOSE DELIVERED (mechanism, decoded off the ON replays):**
(a) in ≥ 1/3 of ON games that plant ≥ 1 tube, at least one prep barrier lands
**front-side** (barrier tile strictly closer to the enemy core than the tube
tile, or on the tube→enemy cardinal ray); (b) ≥ 1 heal event on a tube or
screen-barrier tile somewhere in each fixture's ON tape (HP-regen readable
from replay events; heal = +4 quanta).
*Falsifier: (a) fails ⇒ the seat bias is not steering placement (geometry or
step_to interaction); (b) fails ⇒ the heal rung is unreachable in practice
(cooldown starvation or the STAGE gate ordering) — either way the plank's
mechanism is absent regardless of any level movement, and the row goes back
to design.*

**E5 — MECHANISM DIRECTION (screen-grade only):** ON-arm forward-turret
median life (censored) **non-decreasing** vs control on F2 (the
contact-shaped opponent), read with the M7d damage-linked discipline (only
damage-linked removals count against the guard; research's cause-filter,
SPEC-m7-cause-filter-2026-08-22).
*Registered scope: DIRECTION on a 30-game deterministic fixture; NOT a level
claim.*

**E6 — TIMELY-CHECKMATE GUARD (defence bar, screen-direction only):** ON-arm
by-r300 core-kill count on F1 within −2 of control (the fixture's same-bot
swing envelope, v620 duplicate-control 2.22pp ≈ ±1 game; −2 allows one game
beyond it). The BINDING form of DEFENCE_ADMISSION_BAR — ITT timely-checkmate
share, restated as an exclusion before any DEFF correction — is carried by
the POWERED read, not by this screen.

## Registered MDE statement (OB16)

n = 30 deterministic cells per fixture per arm. For a game-share style
contrast at p̄ ≈ 0.5 the naive MDE (80% power, α = .05, two-sided) is ≈ 35pp
— **this screen cannot resolve any plausible level effect and no level
sentence will be typed from it.** Levels belong to the registered powered
grid (pooled n = 1800/arm class, two-opponent rule, duplicate control, MAP
DEFF per the enumeration procedure). The screen's job is E1–E4: identity,
liveness, dose, and gross direction.

## What is NOT claimed

No field-general claim (fixture = two authored opponents); no currency claim;
the phantom-death confound is REGISTERED (the guard keeps the engineer in
vision of the tube, silencing the out-of-vision death booking — plants/game,
`nest_lives`, tube median life, adjacent-at-death share are co-diagnostics in
the powered read, and any adopted effect is the TOTAL effect of guard +
ledger-accuracy, stated as such).
