# BRIEF — THE WORST-MAPS BOOK (research s40, 2026-08-14, on Magnus's direction)

**Magnus, direct, this session:** *"Does the researcher also check for things that
can be improved on small segments of maps or just all maps?"* → then
*"Improvements at our worst maps would be a significant upgrade for example."*

**THE HONEST ANSWER TO THE FIRST QUESTION IS NO, AND THAT IS THE GAP THIS BRIEF
CLOSES.** `OBLIGATION 15` (written today) makes NEW rows declare a segment —
**reactive**. The segment sweep audited OLD arms — **backward**. **Nobody's
charter said "our worst segment is X; go find what winning there requires."**
Segment-FIRST hunting did not exist. It does now, and this is its first subject.

---

## THE TARGET, MEASURED — 36% OF OUR GAMES AT 39.9%

Current era (`ourver` ≥ 125, rated, 415 games, overall **52.3%**):
| map | share | n | area |
|---|---|---|---|
| antler | **36.7%** | 30 | 252 |
| midgard | **38.2%** | 34 | 900 |
| fjordgate | **38.5%** | 26 | 100 |
| ragnarok | **42.4%** | 33 | 900 |
| frostgate | **44.0%** | 25 | 400 |
| **POOLED** | **39.9%** | **148 = 36% of the pool** | |

**Half-closing that gap is worth roughly +2.2pp on 36% of games ≈ +0.8pp
overall** — plank-sized, concentrated, and on cells we already know.

## ⭐ THE ONE RESULT THAT MAKES THIS WORTH COMMISSIONING — THE OBVIOUS CONFOUND IS ALREADY DEAD
*"We lose there because we meet harder opponents there"* was the cheap
explanation. **Run and refuted on the small pair (antler + fjordgate, 56 games):**
**observed 21 wins against 29.6 EXPECTED — where "expected" uses OUR OWN
elsewhere-rate against EACH SAME OPPONENT — a shortfall of 8.6 wins = −15.3pp,
z = −2.43, p ≈ 0.015.** Match clustering in that set is negligible (7 of 49
matches contribute a second game; m̄ = 1.14 ⇒ DEFF 1.019 ⇒ **z = −2.41,
p ≈ 0.016**). **We play worse against the SAME opponents on those maps.**
⚠ **The per-opponent SIGN test is NOT significant (10 of 17 negative, p = 0.315)
and is reported here so nobody quotes it: the mix-adjusted MAGNITUDE is the
load-bearing statistic, not the count of negative cells.**

## ⛔ THE DESIGN POINT THAT MATTERS MOST: DO NOT ASSUME ONE CAUSE
**These five cells are THREE different terrain classes** — antler/fjordgate are
small (252, 100), midgard/ragnarok are 900-area and **lock-heavy** (`#54`:
midgard 35.6% of builder-rounds in permanent locks), frostgate is 400.
**⇒ "These five are weak for five different reasons" MUST BE A PERMITTED
ANSWER, and the book must be able to return it.** A book that arrives looking for
one story will find one. **State per cell whether its mechanism is shared or
private, and say which cells you could NOT explain.**

## WHAT TO DECODE — mechanism-first, the style that produced arms from the opponent books
Per cell, ours vs the same opponents elsewhere:
1. **OPENING** — first 8 builds, order and tiles; does our opening differ on these maps at all, or is it map-blind?
2. **ARRIVAL** — round our first builder reaches d²≤8 of their core, and the SHARE of games where it never does (the Juusto decode found we no-show in 26% of games against them — check it per cell here).
3. **BUILD MIX** — per-game counts by kind, and self-levied cost-scale.
4. **LOCK RATE** — `#54`'s detector per cell (`nav_limit_cycle_census.py` is recoverable; see below).
5. **LOSS ANATOMY** — round of our core death, what killed it, what we had standing at r100/r150.
6. **THEIR side** — do opponents do anything DIFFERENT on these maps, or only we?

## INPUTS ALREADY IN FLIGHT — do not duplicate
* **HOME-LOCK MECHANISM agent** (builder, in flight) covers the midgard/ragnarok lock channel.
* **OPPONENT-SEGMENT MAP** (queued) — per-cell opponent concentration; the small-pair version is already run above.
* **`nav_limit_cycle_census.py`** survives at
  `/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/248fc65e-25d6-4cbc-b63a-4d4fb90e6993/scratchpad/` —
  **⛔ a recovered script is a CLAIM: it must reproduce `#54`'s headline before its output is read.**

## ⛔ HOUSE RULES THIS BOOK MUST CARRY
* **ERA-BOUND both axes.** `ourver` ≥ 125 throughout; our bot moved ~90 versions across the archive.
* **UNITS: name the cluster.** A per-map bar takes NO match DEFF (verified 0 of 415 (match,map) pairs with >1 game); the residual is the OPPONENT cluster (ρ=0.0743, m̄≈2 ⇒ ≈1.07). **Follow `CLAUDE.md`'s three-step scope procedure; do not carry 1.53 into a per-map bar.**
* **Per-cell n is 25–34 games. Print the minimum stratum n and the count below floor INLINE**, per the banking rule, and flag anything under n=15 as a hint.
* **`econ.tsv` is rebuilt (v2, 14:01:25Z) — cite the rebuild**; pre-rebuild cpu/turns figures are a different instrument.
* **NAME YOUR SCRIPTS BY FILENAME** in the write-up (banking rule clause v) so the next audit can re-run rather than re-argue.

## OUTPUT
`docs/research/BOOK-worstmaps-2026-08-14.md`, the shape of the opponent books
(headline / per-cell mechanism / shared-vs-private / routing), **80–120 lines,
every line carrying a number.** Final section is `## Routing` naming the
`QUEUE.md` rows it feeds or creates — **each with an `OBLIGATION 15` segment
declaration and an EXPECTED DIRECTION**, so a worst-map plank that does not
generalise can ship MAP_CODES-style gated rather than being pooled into a null.
**A book that names a knob gets consumed; a book that describes terrain gets
filed.**
