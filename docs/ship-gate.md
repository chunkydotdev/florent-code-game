# Ship gate (Magnus, 2026-08-08 ~19:40 — supersedes the 2026-08-07 field-battery gate)

## The gate

**Ship when: no measured local regression (PARITY PASSES) + an available window
+ nothing known-broken.**

Field evidence for an unshipped head is **not owed** — it is structurally
unobtainable on this platform (`fcode submission download` is own-team-only;
`fcode match test` takes two local dirs; unrated challenges run the ACTIVE
submission). Demanding it was a gate with no gate-opening move.

## Why it changed

Audit at 19:40: the project peaked at 1625 Elo / rank #21, then lost **57 Elo
and 9 ranks in 15 hours with ZERO ships** while five planks sat in KEEP-dev.
Measured signature of the deadlock: ship cadence 0.79 → 0.46/hr, committed
doc:code churn 0.14 → 1.88, eleven straight hours of zero bot lines.

**Rigor that cannot terminate in a decision is a cost, not a virtue.** The
failure looked *more* rigorous the whole time it was happening.

## How to apply

- **Ship the biggest available change per window.** A window is ~8 matches ≈ 1h;
  the team gets ~10-12 evaluated ships/day. **Windows are the scarce resource,
  not code.**
- **State debts on the tape row rather than holding for them.** An untested
  prediction or a known single-map regression is a row line, not a blocker.
- **Identity / 0-flip controls stay MANDATORY.** They are how a plank ships
  without regressing the 14 maps it never meant to touch. This is the one part
  of the old rigor that pays for itself every time.
- **Probes are attribution-only now, never gates.** (Fleet state 2026-08-08:
  orizon valid; band valid rush-mode-only; kladde and flotte need re-freeze;
  cad disclaimed.)
- **A plank that stays KEEP-dev through two windows is refuted by neglect —
  close it.**
- Safety comes from the [slot swap rule](../elo_history.tsv) — rolling last-5
  arms at holder-match ≥8, ≤0 frees the slot, rollback is one click. **That rule
  must not drift**, because it is now the entire control on shipping fast.

## What did NOT change

Self-legs remain attribution-only **in both directions** — parity is not a
reason to hold, and a good det number is not a field claim. "0 flips" still
means *no outcome effect measured*, never *no effect*: pair it with the
delivered-titanium delta `tools/det.py` now reports.
