# LOKI-QUIET (v121) — a DISCRIMINATING PROBE against CtrlAltDefeat. Not a plank.

version: unrated probe only; the slot returns to v94 immediately after.
dev_dir: bots/_v121lokiquiet
line: loki (PROGRAMME.md). Forked from `_v120loki4`; single flag `LOKI_QUIET_ON`.
  `LOKI_QUIET_ON = False` reproduces LOKI-4 exactly.

**THIS PROBE IS NOT MEANT TO WIN AND ITS WIN RATE IS NOT A RESULT.** It is
designed to lose more than LOKI-4 does. Read it on the OPPONENT.

produces: **A SEPARATION THE CORPUS CANNOT MAKE.** Measured over 225 CAD games
  / 88,066 rounds: after early core damage, CAD's off-collar builders holding
  ≥30 Ti build on **0.94%** of turns vs **8.25%** in undamaged games — identical
  move rate, **100% of idle turns cooldown-free**, deaths flat (0.13 vs 0.14),
  zero TLEs, and **32 of 32 matches show the gap** under within-match pairing.
  Poverty is refuted *inside every titanium bucket* (50–99 Ti: 1.35% vs 14.63%),
  as are rebuilding, walking and blocked/dying.
  **But DAMAGE and INTRUDER-PRESENCE are the same event in that corpus.** This
  probe makes them different: the raider arrives and does **nothing hostile**.

falsifier / the two outcomes, both useful:
  - **CAD still goes idle with a quiet raider present** ⇒ the trigger is
    **PRESENCE**. We never have to land a hit; arriving IS the exploit, and it
    costs no damage race. This is the cheap world.
  - **CAD keeps building against a quiet raider, and only goes idle against the
    attacking LOKI-4 arm** ⇒ the trigger is **DAMAGE** and we must connect.
  - **Neither arm reproduces the idle at all** ⇒ the corpus effect does not
    reproduce live, and the whole exploit is off the table. **That outcome is a
    result, not a failed run**, and I will record it as one.

treatment_occurrence: **VERIFIED BY DECODE, NOT ASSUMED — and the first cut was
  WRONG, which is why this line is measured.** Gating the two obvious raid
  attack sites left **154 attacks in a "quiet" game (control 170)**, a 9%
  reduction: two further builder-attack paths existed — the **siphon melee**
  (`eco.py`, attacking enemy conveyors for resources) and a **counterbattery
  melee** (`main.py`). With all four gated, decoded over 3 maps vs `cad_probe`:
  **quiet arm 0 attacks (0/0/0), control 985 (393/290/302).** Had I trusted the
  flag, the probe would have attacked 154 times and I would have concluded
  something about "presence".

S5_unrated: **this probe REQUIRES real CtrlAltDefeat** — `cad_probe` is our own
  imitation of their opening and cannot reproduce a behaviour we never coded
  into it. So it cannot be settled locally and needs an unrated leg, per
  Magnus's standing directive (*"test theories using unrated games between
  ladder games"*). **BLOCKED pending the slot decision**, which is Magnus's, not
  mine — the leg displaces a climbing bot.

## LIMITS, STATED BEFORE THE LEG

- **Two arms are needed, not one.** A quiet-only leg cannot distinguish "the
  trigger is presence" from "the idle does not reproduce live". LOKI-4 is the
  attacking control and must run on the same fixture.
- **The corpus cut cannot separate *"tried and `can_build` refused"* from
  *"never tried"***. Poverty and blocking are refuted, so the remaining
  candidates are inside CAD's own code, and this probe does not open that box.
- **Arrival is a precondition, and we are bad at it.** If the quiet raider never
  reaches their base, the leg measures nothing. Arrival must be verified in the
  replay before either outcome above is read.
- **`LOKI_QUIET_ON` silences the siphon**, which is real economic income. The
  quiet arm is therefore economically handicapped as well as toothless — another
  reason its win rate is not a result.
