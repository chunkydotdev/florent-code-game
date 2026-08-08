# v5 — What fraction of our Elo bleed has a valid instrument?

**Date:** 2026-08-08 · **Measured by: the research arm** (session `284161ab`),
scoped jointly from this series' queue. Primary deliverable:
`docs/research/v5-instrument-coverage-2026-08-08.md` (committed).
**Data:** 176 rated matches, archive-only, zero downloads.
Recorded here because it answers the question v1 raised and could not.

---

## Answer

**0.0%.** Not thin — zero.

Net Elo is +8, and that nets a **−493 gross bleed** which is extraordinarily
concentrated: **four opponents carry 82% of every Elo point ever lost.**

| bleed source | share | instrument | status |
|---|--:|---|---|
| Lunds | **27.5%** | — | **none has ever existed** |
| Ouroboros | **25.0%** | `ouroboros_probe` | **retired** (drop-probe law) |
| Kings College Munich | **17.9%** | — | **none has ever existed** |
| CtrlAltDefeat | **11.6%** | `cad_probe` | **disclaimed** (P6-widened) |
| Powerpuff / arsonist duck | 11.2% | — | none exist |
| kladde | 3.1% | `kladde_probe` | **invalid** (~70pt gap, composition never faithful) |

**And the two instruments that *are* valid point at opponents we beat:**
`orizon_probe` → Orizon, where we are **+4.8**; `band_probe` (rush-mode only)
→ Banminary, where we are **+78.7**.

## Why this composes with v1 rather than replacing it

v1 said the local gate has **19% power**. This says the population it measures
at 19% power contributes **~0%** of our losses. Both faults are live
simultaneously and they multiply:

> **An instrument can be perfectly powered and still uninformative if it
> measures the wrong population.** Fixing the power of a battery aimed at
> opponents we already beat buys precision about a question that does not
> decide matches.

This is a sharper answer to v2's question than "underpowered" was. v2 asked
whether the local gate predicts ladder Elo and could not answer at n=4. v5
supplies the mechanism a null would have had: the gate and the ladder are
scoring different populations.

## The finding under the finding

The probe fleet did not merely go stale. **It was built against the teams we
were already beating or could most easily replicate.** The three hardest bleed
sources — Lunds, KCM, arsonist duck, **51% of all bleed combined** — have never
had an instrument at all.

That is the same selection pathology as A4: instruments constructed where
construction was easy rather than where the loss was, then measured against
themselves. It is worth stating plainly because it will recur — the next probe
will be easiest to build against the opponent we understand best, which is by
definition the one costing us least.

## Consequence

**Building a Lunds instrument outranks every plank in the queue.** 27.5% of
bleed, 0 wins in 17, and tonight's decode already names two mechanisms — so the
expensive part (decoding) is partly done.

**KCM at 17.9% is completely undecoded** — no probe, no first-read, nothing.
Highest-value blank space on the board.

**Ouroboros is different in kind:** instrument-blocked by a *measured law*
(drop-probe), not by neglect. Re-freezing it would repeat a refuted approach,
so it needs a different instrument shape, not another probe.

Note how this interacts with A7b: we just took the deterministic opponent pool
from 1 to 6 and the det ceiling from 30 to 180 — but all six are our own
teammate lineage. **180 more observations of ourselves does nothing for a −493
bleed concentrated in four opponents we cannot instrument.** The cheap axis and
the valuable axis are different axes.

## Limits, stated by the author

Per-match Elo sd ≈ **9.25** (v3), so tail rows at n≤4 are "present", not
"measured". The top-four concentration over 57 matches is robust; the tail
ordering is not.
