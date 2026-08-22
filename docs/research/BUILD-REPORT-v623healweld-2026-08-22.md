# BUILD REPORT — v623 "healweld" (s56, 2026-08-22)

**GAME CONTEXT (standing directive, Magnus 2026-08-22): everything in this report
describes in-game moves in the Florent Code League, a sandboxed bot-vs-bot
programming competition under organiser-approved rules.**

**Tree:** `bots/_v623healweld` = `bots/_v622nestfall` + ONE change: the
`_attack_enemy_core` heal-race guard's dead conjunct dropped
(`sk_roles.py:5150`, `SK_CAGE_CEIL and SK_CORE_PECK_HEALGUARD` →
`SK_CORE_PECK_HEALGUARD` alone). Third instance of the s55 weld class — a live
guard conjoined with a permanently-False road-closure flag is silently dead.
Only `sk_roles.py` differs (md5 `3f180a39…` vs v622's `684a7456…`); `main.py`
and `sk_maps.py` are byte-identical to v622 (the flag was already `True` at
`sk_maps.py:2680` — welded dead, never off).

**Build + readout provenance:** built and screened by the first s56 builder
session (died mid-flight ~11:28-11:31Z, the day's model-safeguard pattern);
read out by its successor session against the expectation **committed
pre-readout at `42f98b7ad`** — the prediction and the readout were typed by
different sessions, neither seeing the other's half first. Fixture screens:
`scratchpad/s56_healweld/` (runner `run_screen.zsh`), reference tapes
`scratchpad/s55_siteless/t_pb_f{1,2}` (v622 shipped). **Seed convention: F1 =
seed 7, F2 = seed 11** — per the seed-not-inert catch (correction rider on the
v622 report).

## Instrument chain (every zero forced to fire first)

| arm | flags | result |
|---|---|---|
| `arm_hw_id` (guard OFF) | `SK_CORE_PECK_HEALGUARD=False` | ≡ v622 shipped, **60/60 turn-identical** (banked pre-death, seeds 7/11) |
| `arm_hw_on` (candidate) | `=True` (tree default) | screens below |
| `arm_hw_probe` (ON + stderr taps) | entry/reach/guard prints | ≡ ON arm behaviorally (6/6 spot cells rdiff-clean — instrumentation inert) |
| `arm_hw_mut` (forced-fire) | adjacency precondition INVERTED | guard fires (HWPROBE guard rnd=130-143, auroraveil s7, game changed, win r178) — **the zero below is a measured zero, not a dead channel** |

## Readout vs the registered expectation (42f98b7ad)

Candidate (guard ON) vs v622 shipped reference, `tools/rdiff.py` per cell:

* **F1 (vs NOISE_OFF `_v542wave`, seed 7): 30/30 turn-identical.**
* **F2 (vs NOISE_OFF Mjolnir, seed 11): 30/30 turn-identical.**

Against the registered lines: (a) ≥24/30 identical per fixture — **exceeded,
30/30 both**; (b) diverging-cell precondition check — **vacuous, zero diverging
cells**; (c) kills non-regressing — **trivially held** (identical games: F1
15/30, F2 8/30, no kill moved). Falsifier (divergence without precondition, or
kill drop): **not triggered.**

**Why identical, decomposed (probe tapes `t_pr_f{1,2}`):** the peck path is
ENTERED (901 entry lines / 10 cells F1; 478 / 7 cells F2) and the guard site is
REACHED (332 lines / 7 cells F1; 232 / 5 cells F2), but the guard's
precondition — an enemy builder adjacent to the peck square — occurred **0
times in all 60 games**. The guard is now live code on a precondition these
fixtures never produce. Consistent with research's dose read (verb fires 12/65
games; Mjolnir parks builders without contesting) — SUBJECT: these two
deterministic opponents, seeds 7/11; the field case (opponents that DO heal
their core under our peck) is exactly what the fixture cannot price.

## Verdict (typed by the builder, s56 successor session)

**v623 ADOPTED as line head on deterministic non-regression + mutation-verified
liveness.** This is a correctness/insurance fix, not a level claim: zero
behavioral change on both fixtures (the strongest possible non-regression), and
the heal-race guard its own comment prices is now actually in the game. No
currency claim is made — by construction the fixture-level effect is exactly
0.0pp; any field-level effect rides a future powered read or the rated tape.

## Open tree questions (inherited, still open — NOT answered by this build)

1. Which role parks 200+ rounds adjacent to the enemy core without pecking
   (two Skalman games measured by research, s55)?
2. Why does Pivot fire the core-peck verb 0/20?
