# REGISTERED EXPECTATION — v632heim PLANK 4 (keeper leash) alone + the 1+4 composite

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** typed by BUILDER s57, committed BEFORE any plank-4 or
composite tape exists. Inputs: the p1 readout (banked, e46p1_*), the thrice-
measured F1 keeper-collapse signature, queue row #128(a), the E6 attribution's
keeper-range numbers (healthy median d²6.5 / 7.3% beyond 50; drifted 20.5 /
16.6%). **Per the side-lane forward requirement, every bar below states the
CONTROL's measured value next to it — the two prior spec defects (v630 E4a,
p1 E4) both died on unverified inertness assumptions; here the control side
is measured, not assumed.**

**ARMS (each vs the same-session controls t_ctrl_f1/f2/f3):**
- `id` — v632heim all flags OFF (tree changed again ⇒ identity re-proven).
- `leash` — SK_KEEPER_LEASH=True only.
- `p14` — SK_FORTRESS+SK_CITADEL+SK_IDLE_ACT_ALL+SK_KEEPER_LEASH=True.

## Registered lines

**X1 identity:** id ≡ ctrl 30/30 ×3 (rdiff, checker driven divergent first).
*Falsifier: any divergence ⇒ leak; halt.*

**X2 leash-alone liveness + scope:** the leash binds only under threat, so
leash-alone divergence is expected in SOME but not necessarily most cells.
Registered: ≥5/30 divergent per fixture (every fixture's control shows threat
episodes in ≥22/30 cells) AND ≥10 cells identical across the three fixtures
combined (a leash that diverges everywhere is binding without threat — a
scope leak). *Both directions registered.*

**X3 keeper-drift repair (the plank's whole point), leash-alone AND composite,
against the control values measured in the p1 readout:**
- F1 core-footprint heals/game: CTRL measured **13.27**; p1-ON measured 8.87
  (−33%). Bar: **leash arm ≥ 11.9 (within −10%); composite ≥ 10.6 (within
  −20%)** — the composite carries plank 1's duty-pull, the leash must claw
  back most of it.
- Our-core-death cells F1: CTRL **16**; p1-ON read 22. Bar: **composite ≤ 18
  (+2)**; leash-alone ≤ 17.
- F2/F3 same forms (CTRL heals 7.20 / 10.53; death cells 21 / 18): composite
  within −20% and +2.

**X4 THE RESPECIFIED DISPATCH DOSE (composite only) — discriminating form,
control side measured:** per fixture, ON zone-chew events vs CTRL measured
(**727 F1 / 557 F2 / 594 F3**): bar **≥ +20% on ≥2 of 3 fixtures**; AND
enemy-structure destroyed-share in our half vs CTRL measured (**0.277 /
0.184 / 0.091**): bar **≥ +0.03 absolute on ≥2 of 3 fixtures**. (p1-alone
measured +64% F1 / −29% F2 / +5% F3 and +0.065 / −0.001 / +0.035 — the bar
asks the composite to hold the F1/F3 gains and not pay F2's regression twice.)

**X5 survival + econ guards (composite):** P(alive@r300) per fixture within
−1 cell of CTRL (**16/13/16**) with the three-fixture SUM non-decreasing
(45); eco builds/game within −15% of CTRL (**13.23/15.23/14.17**) at the
common horizon; by-r300 kills reported, no gate.

**X6 tracebacks:** concurrent observation; expected 0.

## Adoption rule (pre-registered)

Leash-alone adopts if X1, X2, X3(leash bars) pass — it is a guard plank; flat
everything else is fine. The composite advances to plank-2 stacking if X3
(composite bars) and X4 pass and X5 holds; if X3 passes but X4 fails, plank 4
adopts alone and plank 1 returns to design with the leash underneath it.

## Scope

30-cell screens ×3 fixtures; MDE ≈35pp; no level sentences. The F1-carrying
pattern is the explicit subject: this is the first arm built to REMOVE a
measured systematic rather than add capability, and its success metric is the
guard columns, not the dose columns.
