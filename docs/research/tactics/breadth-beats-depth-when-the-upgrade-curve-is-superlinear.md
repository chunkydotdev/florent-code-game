---
tactic: The only published cost-curve comparison in the sweep — breadth beats depth when the price curve is superlinear and the output curve is linear
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025, The Kragle (finalists)
evidence: documented
transfers: partial
---

## WHAT IT IS

The Kragle open their postmortem with two observations and a published cost table. **The
subject is BC2025 MONEY towers — the economic structure, not the defensive one — and they
say so themselves: *"we ignore defense towers for now"*.** That subject must travel with
the numbers.

> *"It is not worth upgrading towers."*

and the table it rests on, quoted exactly as the PDF renders it:

> *"Level 1 2 3 Upgrade Cost (Chips) 1000 2500 5000 Mining Rate (Chips / Turn) 20 30 40"*

**Cost 1000 → 2500 → 5000 is superlinear; output 20 → 30 → 40 is linear.** Their
conclusion:

> *"when you have the choice between spending on a new tower, or upgrading an existing
> one, there is no reason to upgrade"*

They then graph both strategies against total cost and follow the same reasoning to a
second, sharper result — that money towers out-produce paint towers *as paint* via
disintegration, at *"an effective paint mining rate of 10 paint per turn, which is double
what paint towers are capable of"*.

**This is the only place in the sweep where a competitor published the actual price curve
and derived the mix from it rather than asserting a preference.** The method is worth more
than the answer: *tabulate cost and output at each tier, and take the strategy whose
output-per-total-cost curve dominates.*

## WHY IT MIGHT TRANSFER — and our curve is a different shape

**Our cost curve is superlinear too, but on the OTHER axis, and that inverts the
conclusion.** The Kragle's superlinearity punished *depth* (upgrading one structure);
ours punishes *breadth* — the single global scale factor rises **+20% per gunner or
sentinel built** and multiplies every subsequent build (`docs/game-model.md:393-402`,
marked measured). We have no upgrade mechanic at all.

So the correct transfer is **the method, not the verdict.** Running it on our two turrets:

| | build | dmg/round | Ti per dmg/round | scale added | scale per dmg/round |
|---|---|---|---|---|---|
| Gunner | 20·s | 7 | 2.857·s | +0.20 | 0.0286 |
| Sentinel | 30·s | 9 | 3.333·s | +0.20 | 0.0222 |

**The two columns disagree**: the gunner is 14% cheaper in titanium per unit of standing
damage, and 29% more expensive in *scale* per unit of standing damage. The Kragle's
dominance test therefore returns **no dominance** for us — neither curve dominates the
other — which is a real result and not a failure to compute. Our tiers are a sidegrade;
BC2025's were a genuine tier.

**The transferable habit** is that they wrote the table down before choosing. We have
never published ours; the table above is this sweep's.

## WHAT WOULD KILL IT

- **The subject.** These numbers are **money towers** — economy. The Kragle explicitly
  bracket defense towers out of the analysis at this point in the document. Anyone
  quoting the 1000/2500/5000 curve as a *defensive* cost curve is repeating precisely the
  error this library corrected in its own INDEX (a true figure attached to the wrong
  referent).
- **BC2025's upgrade was optional and reversible-ish; our scale is neither.** Ours applies
  to categories we did not choose to grow — a builder bot pays the same +20% as a turret —
  so an "upgrade vs new" framing does not exist here at all.
- The disintegration limb (money towers out-producing paint towers as paint) depends on a
  BC2025-specific rule that a destroyed tower yields 500 paint. **We have a structurally
  similar mechanic** — `destroy()` is free, unlimited, cooldown-free and **returns the
  entity's scale contribution** — and it is already filed as
  [`destroy-rebuild-converter`](destroy-rebuild-converter.md). This file does not restate
  it; note only that The Kragle reached the same *shape* of idea independently.

## BUILDER HOOK

Free and one-off: **publish our own version of that table** — every buildable, its
scaled cost, its output per round in the currency the win condition uses, and its scale
increment — and require any mix proposal to point at a row. The Kragle's entire
contribution here is that they did the boring version of this before choosing, and it
took them to the final tournament with a strategy nobody else was running.
