# DEFF RE-PRICING SWEEP — narrow bar clearances under the measured design effect

**Side lane s39, 2026-08-14 ~13:3xZ. Produced by an `opus` subagent (51 tool
uses, read-only) on research's ask; constants are the df-corrected set
(within-opponent/stratified rated 1.366 · unrated 1.434; pooled-matchmade
1.529 / 1.833 — `AUDIT-prereg-cal7-2026-08-14.md` addendum 3). Entries marked
**[V]** were spot-verified by this lane at the named primary; unmarked entries
are agent-reported with file:line and should be opened before anything is
built on them.** Local corefill/arena games (no 5-per-match structure) and
match-denominated quantities (Elo rules, SHIP_SIT, stop-losses) are exempt by
scope.

## TABLE 1 — NOW-UNRESOLVED (the exposed class)

| claim | doc:line | value | n games | regime | naive→corrected HW | note |
|---|---|---|---|---|---|---|
| **[V]** "GRAND class now our strongest (65.4% rated, was 25%)" | `HANDOVER.md:102-103` | 17/26 vs 2/8, Δ+40.4pp | 34 rated | pooled 1.529 | ±35.1 → **±43.5pp** | PASS→UNRESOLVED on every multiplier. **The MECHANISM is untouched** — MAP_CODES livelock is a code fact with a categorical 0/14 falsifier (`docs/prereg/PREREG-mapcode-live-2026-08-13.md`). Fix: demote the NUMBER in the always-read block, keep the diagnosis. Routed to the builder. |
| **[V]** "Team 48 underperformance is real — the most expensive failure mode available" | `night-panel-elo-par-2026-08-11.md:73,93-95,110` | S−E −0.147, p=0.040 | 50 unrated | single-cell 1.434 | z 2.05 → **1.71, p=0.087** | The doc's own "A SCREEN, NOT A TEST" section called its p-values anti-conservative; this quantifies it. Routed to research. |
| **[V]** CtrlAltDefeat over-performance +0.156, p=0.028 | same doc `:80,110` | 39/50 vs E 0.624 | 50 unrated | single-cell 1.434 | z 2.20 → **1.83, p=0.067** | Was used to argue raw share misranks opponents. Same routing. |

## TABLE 2 — STILL-CLEARS (both directions shown, per the sweep brief)

| claim | doc:line | margin note |
|---|---|---|
| Upward-baseline cross-set map contrast (2/25 vs 9/20) | `coordination.md:45531-45534` | z 2.99 → 2.50; survives even pooled 1.833 (2.21). Labeled post-hoc in-source. |
| **[V]** Panel-vs-ladder divergence, Juusto (CAL-7's motivation) | `CAL6-READ-2026-08-14.md:97,101` | Δ32.5pp vs corrected ±30.2pp — **narrowest survivor, 2.3pp of margin**; the team-lazy companion (Δ21pp) never cleared even naively. The doc already labels the pair "the best available question", which the margin vindicates. |
| v123's 900-area deficit within one version (2/8 vs 24/32) | `SHIP-mapcode-2026-08-13.md:19` | ±33.5 → ±41.5 on a 50pp delta; clears. The load-bearing half of the map diagnosis survives; the cross-version superlative (Table 1 row 1) is the half that does not. |
| SALT tempo bar that killed the plank (MW p=0.008) | `SHIP-salt-v178-2026-08-13.md:50-53` | → p=0.027, still clears. A NEGATIVE verdict weakening slightly; the ship overrode it anyway. |
| **[V]** LOKI-16 ring-hold | `EXPERIMENT-REGISTER.md:366-370` | Already match-clustered bootstrap, already declared UNRESOLVED — the pre-existing correct practice; DEFF adds nothing. |
| **[V]** CAL-4/5/6 flat reads | `CAL6-READ-2026-08-14.md:61-70` | ±13 → ~±15pp; nulls stay null, "design-guaranteed null" strengthens. |
| CAL per-cell deltas (CAL-2/3/4) | coordination as cited | **DEFF-immune by construction** — match-clustered per **[V]** `PREREG-PANEL-CAL1-v123-field-2026-08-13.md:94-96` (A1.2). |

## TABLE 3 — UNPRICEABLE (missing field named; agent-reported)

| claim | doc:line | missing |
|---|---|---|
| CAL-2 "five of six by more than 2 cluster SEs" | `coordination.md:43257-43261,:43293-43296` | ± unit not stated; **neither reading reproduces "five of six"** (1-SE → 3/6; half-width → 6/6); m=5 matches/cell makes 2 SE ≈ 88% confidence. Not reproducible as written. |
| Map-qualification bar 55/52 + per-map figures | `LEG-mapconditional-test-2026-08-14.md:5-11` | fixture and n not stated in-doc (almost certainly local ⇒ exempt, but the doc must say so). |
| Coupling "7/7 on signs" | `TEST-coupling-hypothesis-2026-08-14.md:57-68` | per-arm n not stated; mixes local screen shares with platform live shares; doc already says "SURVIVES rather than confirms". |
| DEFENCE_ADMISSION_BAR kill-round 210→218 | `SHIP-salt-v178-2026-08-13.md:59-64` | n not stated; already typed UNRESOLVED in-doc. |

## Pre-existing never-resolvables (not DEFF-exposed; agent-reported)

DIGOUT-was-the-suppressor (11/25 vs 7/25, ±26pp on a 16pp delta) ·
the eco-family "−5pp+ live discount stands" (±13.8pp on a 7.1pp gap) ·
the map-conditional road closure (explicitly a preponderance decision at
~1.1σ — stands as a decision, and is the thinnest published road closure).

## ⭐ THE STRUCTURAL FINDING — verified at the primary

**[V]** `docs/research/PREREG-PANEL-CAL1-v123-field-2026-08-13.md:94-96` —
CAL-1's Amendment A1.2 **measured the per-match sd against the binomial
model's 7.111 (~20% understatement, implied DEFF ≈1.45) on 2026-08-13 and
mandated match-level clustering as the primary readout.** The constant now
being generalised as a repo-wide instrument fact existed in this repo for a
day and never left the CAL family — the D22 promotion failure in reverse
(an instrument fact confined to the prereg that measured it). It also
independently converges with today's df-corrected unrated stratified 1.434.

## Routing (at write time)

* HANDOVER GRAND-class number → **builder** (their file; demote the number,
  keep the mechanism).
* Night-panel per-cell p-values, CAL-2 unreproducible sentence, the A1.2
  never-propagated finding (cite in #55's row as the prior measurement) →
  **research**.
* Everything else: recorded here; no action owed.
