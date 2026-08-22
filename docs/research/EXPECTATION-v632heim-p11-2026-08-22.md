# REGISTERED EXPECTATION — v632heim PLANK 1.1 (keeper medic-yield) composite screen

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s57, committed before any p1.1 tape exists. The tree
now carries SK_KEEPER_LEASH=True as the ADOPTED default (leash-alone passed
every registered bar; costs banked in the flag comment), so **the identity
baseline changes: flags-off v632heim must now reproduce the t_leash tapes,
not t_ctrl.** Change under test: one ordering rule — the KEEPER yields
`_citadel_answer` while `corefire_fresh` (its core's own HP-delta latch);
denier/walker unchanged.

## Registered lines (control values measured, from the banked p4 readout)

**Y1 identity:** flags-off v632heim ≡ **t_leash** 30/30 ×3 (the new baseline).
*Falsifier: any divergence ⇒ the default flip or the 1.1 edit leaks outside
its gates; halt.*

**Y2 composite (p11 arm = FORTRESS+CITADEL+IDLE_ALL on the leash-default
tree) heals guard, vs the ORIGINAL t_ctrl constants (raw per-game, the same
convention as X3; horizon-convention defect from X-doc noted and NOT
repeated — raw governs, common-horizon reported):** F1 ≥ 10.6 [ctrl 13.27;
p14 measured 9.10], F2 ≥ 5.76 [7.20; 5.13], F3 ≥ 8.42 [10.53; 12.07].
**Y2b death cells:** F1 ≤ 18 [16; p14 20], F2 ≤ 23, F3 ≤ 20.
*The five carrying F1 cells are named in the plank comment — if F1 still
fails, report their per-cell heals; a repair that misses those cells is not
this fix working.*

**Y3 dose retention (the X4 bars unchanged):** zone chews ≥ +20% on ≥2/3
[727/557/594; p14: +50.5/−42.9/−17.5] and destroyed-share ≥ +0.03 on ≥2/3
[0.277/0.184/0.091; p14: +0.037/−0.030/+0.002]. *The open question is F2:
whether the keeper-yield recovers its chew regression (hypothesis: NOT — the
F2 regression was not keeper-carried; if F2 stays low, the fallback below
fires on the dose axis, not the guard axis.*

**Y4 survival + econ:** P(alive@r300) within −1/fixture of ctrl [16/13/16],
sum ≥ 45; eco builds common-horizon within −15% of ctrl.

**Y5 tracebacks:** concurrent observation, expected 0.

## Pre-registered decision rule

Y1+Y2 pass, Y3 pass → the full composite advances; plank 2 stacks.
Y1+Y2 pass, Y3 fail on F2 only with F1/F3 holding → **adopt the dispatch for
F1/F3-class matchups as-is is NOT available (no per-opponent flags in a
shipped bot); instead the composite adopts if the three-fixture SUM of
destroyed-share deltas is ≥ +0.02 and no fixture's survival fell** — the
aggregate form, pre-registered here to prevent post-hoc cherry-picking.
Y2 fail → the ordering fix missed; plank 1 is returned to design a second
time and PARKED (two strikes, the E4b' precedent), and the build proceeds to
plank 2 on the leash-only base.
