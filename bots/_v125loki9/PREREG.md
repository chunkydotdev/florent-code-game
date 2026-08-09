# LOKI-9 (v125) — GARRISON LESS. Heal the Core only when it is really hurt.

version: unrated benchmark only. **NOT for the ladder** (Magnus: "No ladder yet").
dev_dir: bots/_v125loki9
line: loki. **COMPARE_AGAINST `_v124loki8` (v99)** on the identical fixture.

produces: **CORE-KILL SHARE, by converting garrison rounds into work.**
  Measured across 6.6M third-party rounds: **our collar occupancy 66.5% vs the
  top tier's 40.6%** (field 53.2%), and **our core costs 1,596 damage to kill
  against their 1,019** — while we sit 400–500 Elo *below* them. They are not
  short of bodies (5.59 alive/round vs our 5.96); they hold 0.121 collar-seats
  per bot against our 0.206. **They choose not to garrison and spend it on
  killing.** The mechanism: `SLOT_UNDER` latches **50 rounds off a single point
  of chip damage**, and every nearby builder then heals at 1 Ti and **one move**
  each. This gates that on the Core being below `LOKI9_HEAL_HP_FRAC = 0.80` of
  max.

falsifier: **core-kill share at or below LOKI-8's**, or a material WIN-rate drop
  with share flat — that second shape is the trade going wrong, i.e. chip damage
  we now ignore accumulating into a lost core. **"Our core is expensive to kill"
  was being described as a STRENGTH by the same measurement; this plank bets it
  is a cost centre, and the bet can lose.**

treatment_occurrence: **VERIFIED, and the first cut CRASHED.** My edit anchored
  on `def _heal_core`, which lives in a mixin, not `main.py` — both replaces
  were **silent no-ops**, only the call site landed, and the bot threw
  `AttributeError` on 4 units (a unit that raises is destroyed for the match).
  The smoke test caught it. Now inserted with assertions, and the treatment is
  visible in the economy: same map/seed, **LOKI-9 mined 2,210 Ti vs LOKI-8's
  1,150** — builders working instead of topping up an undamaged Core.

S5_unrated: this IS the unrated read. Same fixture and opponents as the arms in
  `docs/RESULT-loki-iterations-2026-08-09.md`, **including the upward band**,
  because that is where the finding came from and where it might fail.

## LIMITS

- **0.80 is a guess.** No measurement says 80% is the right threshold; it was
  chosen to ignore chip damage while still answering a real siege. It is a
  knob, and I have not swept it.
- **The finding it is built on is observational.** Top teams garrison less AND
  win more; that they win *because* they garrison less is an inference the
  research arm explicitly labelled as such. **This plank is the arena test of
  that inference** — which is the right way round, but it means a null here
  refutes the plank, not the observation.
- **n=5 per cell.** Same as every arm on this line.
