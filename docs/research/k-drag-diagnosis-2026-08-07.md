# Piece-K drag diagnosis — 2026-08-07

**Version tags (rule 2):** konly = `_v77e6_konly` (Eir 6 worker base,
K_HEAL_BUDGET_ON only), base = `_v76e51` (v66 Eir 5.1). 18 paired replays
from the builder's diag run (konly_orizon / base_orizon / konly_band ×
eider/nordkap/fjordgate × seeds 1,2; our bot seat A in every file;
orizon_probe frozen aa7ab718, band_probe). Our live slot at read time:
v67 wave_ghost. Research arm, session 13. Commissioned question: why does
piece K drag everywhere (all six ablation comparisons below baseline).

## Headline (CORRECTED ~18:45): suspects refuted; the r0-divergence claim was wrong

**Correction, builder-caught within minutes of relay (original preserved
for the record below):** this document's first version read the six
base/konly pairs as deterministic same-seed games and called their
round-0 spawn-tile divergence evidence that the `_v77e6` base refactor
changed the opening. That premise was false: **piece G (decision noise,
shipped v64, NOISE_ON in `_v76e51` and every `_v77e6` variant) rolls an
UNSEEDED spawn salt per match** — verified at `bots/_v76e51/main.py:1082-
1083` (`random.Random().randrange(97)`, comment: "cross-game determinism
is deliberately broken"), and HANDOVER's standing MEASUREMENT WARNING
says paired-seed local runs are nondeterministic by design (pooled Wilson
only). The r0 divergence is the designed noise expressing. It attributes
NOTHING.

What this means for the method: turn-diffing paired replays cannot
attribute anything downstream of the salt (openings, and with n=6, game
outcomes — the konly 5-1 sample in the table below is the same noise).
It CAN attribute salt-independent aggregate behavior, which is why the
suspect refutations below survive the correction unchanged.

Status of the base-drag hypothesis: **live but unevidenced** — my
original claim overreached. The builder's base-purity control
(`_v77e6_alloff` vs opp_v63 + band + a `_v76e51` mirror, 60/leg, pooled,
decision rule pre-stated) is running and settles it either way.

<details>original (incorrect) headline claim: all six pairs diverge at
r0 on the first builder spawn tile (eider s1 (9,9) vs (6,9); nordkap s2
(10,8) vs (11,6)) before any heal, therefore the refactored base plays a
different opening and the ablation attribution is void. The observation
was real; the inference required determinism that piece G deliberately
removes.</details>

## The three commissioned suspects: all refuted by direct measurement

- **(a) Quiet-round trunk top-ups: NO.** Across all 18 games our side
  made ZERO trunk heals (every single heal targets the CORE footprint —
  c-only in all 36 team-rows) and ZERO top-up-class heals (every heal
  landed on a target damaged within the previous 20 rounds). **K's
  "core+trunk" budget never trunk-heals at all.** Builder's code-side
  answer (~18:45): not dead code but **starved by arithmetic** — the
  trunk-heal depth discriminator requires ≥8 accumulated damage, but a
  gunner shot is 7: a once-hit conveyor (13/20) misses by one point and a
  twice-hit one (6/20) is one reload from death, so the qualify window is
  a single reload cycle, additionally behind MEDIC_TI_FLOOR and
  core-heal-first ordering. Redesign implication (agreed): the sporks
  "heal-as-income-line-item" port needs a proactive trigger (heal any
  damage when budget allows), not the raid-only discriminator.
- **(b) Forward-role heal capture: NO.** Zero heals at dsq>50 from our
  core by our side in any konly game.
- **(c) Rush-window substitution: unattributable but flagged.** In
  konly_band's fast losses (r39/r44/r52) 27-31% of ALL builder-turns went
  to core heals inside the rush window (heals from r5). No base_band
  replays exist for the paired comparison, and the r0-divergence means
  any difference would be confounded anyway. Revisit only after the base
  is clean. (Note: base also heals early — first heals r3-12 in
  base_orizon — so "K heals from r0, base gates at r40" is NOT the
  discriminator; the early-emergency heal path predates K.)

## Test status after the correction (~18:45)

1. **Base-purity check: LANDED (builder, 18:46 note, commit 790e411) —
   BASE CLEAN.** `_v77e6_alloff` vs v63 60.0 [47.4,71.4] (baseline 55.0),
   vs band 91.7 [81.9,96.4] (88.3), `_v76e51` mirror 58.3 ≈ equivalence.
   Refactor exonerated; base-drag hypothesis REFUTED; and the K
   refutation is now CONTROLLED: konly vs alloff on the same base = −15
   (v63) and −35 (band). Mechanism fully pinned: K-as-built = un-gated
   core-heal-from-r0 eating builder turns mid-fight, while the actual
   sporks trunk mechanism NEVER RAN (finding (a)) and remains untested.
   Redesign spec (builder's 18:46 note): restore siege gate on core
   heal, keep budget/shares, proactive trunk trigger.
2. **Slot-9 reclaim: CLEARED by builder inspection** — v66's only
   references are the two increment sites (value consumed by nothing);
   `_v77e6` has one writer (l.1105) and one K-gated reader (l.2299). No
   stale-reader hazard.
3. **Trunk-heal trigger: the redesign target** (see finding (a) — the
   ≥8-damage discriminator vs 7-damage gunner shots).

## Sample data (our side, seat A)

(Outcome columns are decision-noise samples at n=6 — see the corrected
headline; do not read a rate from them. Divergence column shows piece
G's salt expressing, not a toggle effect.)

| pair | base result/rounds/heals | konly result/rounds/heals | diverge |
|---|---|---|---|
| orizon eider s1 | L r147, 305 heals | W r69, 75 | r0 (spawn tile) |
| orizon eider s2 | W r97, 0 heals | W r67, 28 | r0 |
| orizon nordkap s1 | W r178, 290 | W r69, 26 | r1 |
| orizon nordkap s2 | W r86, 50 | W r64, 45 | r0 |
| orizon fjordgate s1 | L r1000, 1966 | L r385, 152 | r0 |
| orizon fjordgate s2 | L r1000, 820 | W r193, 183 | r0 |

konly_band (no paired base): 2W-4L, losses at r39/r44/r52/r105 with
27-31% of builder-turns on core heals during the rush in the sub-r60
losses.
