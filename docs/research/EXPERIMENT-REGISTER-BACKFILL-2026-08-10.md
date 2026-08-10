# EXPERIMENT REGISTER — PRE-s27 BACKFILL (point-in-time reconstruction, 2026-08-10)

**Provenance:** reconstructed by an opus subagent from `docs/prereg/`, the
obligations doc, `docs/RESULT-*.md`, `git log`, and `docs/coordination.md` — the
COMMITTED record only. Every load-bearing claim carries an anchor (commit or
file:line). **`NO PREREG`, `UNKNOWN`, and `RESULT NEVER BANKED` are used
literally where the record does not support a field — those are findings, not
gaps to paper over.** This is a reconstruction, not a live register: anchors are
the agent's citations and are spot-checkable, not re-verified line-by-line by the
side lane. Corrections land as dated addenda, never edits (append-only contract).

**Two structural findings that govern how this file is read:**
1. **The LOKI number is NOT a unique key.** `LOKI-2/3/5/9` each name TWO different
   experiments (s22 research "roads" vs later line iterations). **Join on the bot
   dir (`_v1xx…`), never on the LOKI label** — the label merges distinct
   experiments.
2. **The two-clock lock standard is satisfiable only from E-24.4 (2026-08-09
   15:46) onward.** Exactly ONE pre-s27 leg has a recorded platform `createdAt`
   (Leg B `d4db288e`). Every earlier leg has no second clock, so **no lock margin
   exists for any of them** — not a reconstruction failure, a historical fact
   about when the standard began.

---

## COMPACT INDEX (join on bot dir, not LOKI number)

| ID | experiment | prereg? | outcome | key method fault | anchor |
|---|---|---|---|---|---|
| E-14.1 | 6E slot bar | staged, hash UNKNOWN | bar not met (compact 55.0/120 → full 51.0) | never quote the compact number as the case | coord:1141-1144 |
| E-16.1 | C1/C1b/HD/U vs opp_v69 | **NO PREREG** | all "taxes" weakened — cross-batch on shared machine | cross-batch ≠ comparison | coord:1888-1906 |
| E-pre.1 | Ouro-v2 freeze gate | committed (band quoted) | FAILED by ~57pp (57/360 vs wild 76.7%) | code-conformance ≠ behavioural fidelity | coord:3224-3267 |
| E-21.1 | v87 hive conversion | committed | INCONCLUSIVE on its own bar (1/10 vs ≥2) | bar denom 8 read against realized 10; fired short | coord:9059-9091 |
| E-21.2 | Thor-1 gunline | **NO PREREG** | REFUTED (0 kills/10) | plank fired+rolled back in 3 min, only record is a wrap line | coord:9099-9109 |
| E-22.1 | LOKI-0 control | staged | PASS non-inferiority gate (49.4%, CI clears) | template for "control first" | coord:9475-9560 |
| E-22.2 | LOKI-1 vs incumbent | **NO PREREG** | slot: does not take it (+3.6pp, edge in opp-crash legs) | crash-confound stratify; self-play mislabelled "field" | 412ee7a |
| E-22.3 | LOKI-2 destroy/scale-prune | **NO PREREG** | REFUTED structurally (median 2 prunes vs 300-590% scale) | per-game census ≠ reachable set (→ D16); 10× leak conflict UNCLOSED | 4dbbe03 |
| E-22.4 | LOKI-5 kidnapper | partial (identity control) | mechanism real (37.5% vs 1.9%, p=0.015) DO NOT SHIP — rare trigger | frequency denom must be fixture-of-record | fe39786 |
| E-23.1 | plank SITE | read-rule staged | "REFUTED −6.7pp" — later shown p=0.25, overstated | self-play pool; discordant-pair count never reported | coord:12726-12795 |
| E-24.1 | plank DODGE | committed 87fe371 (pushed pre-battery) | mechanism PASS (p=3.7e-6); economy criterion FIRED, kept | a criterion that fires is kept not deleted; pool selected-not-generating | 87fe371 |
| E-24.2 | LOKI-1 foreign pool | **NO PREREG** | win null (+3.1pp p=0.22), core-kill share 61→91%, sign p=5.2e-9 | slot decision ≠ road verdict | 0b510ef |
| E-24.3 | LOKI-2 committed opening | committed a0d7178 (pre-battery) | PASS on secondary (kill turn 198→163, p=0.023) | passed on a currency it was never verdicted against | a0d7178 |
| E-24.4 | Ouroboros Legs A/B + 15:46 conv prereg | LOCKED 15:37 + ca3c3f8 15:46; **only 2-clock cert pre-s27 (2m33s)** | conv prereg fully refuted, anti-correlated with own outcome | obligation 7; +obl 1,2,3,corpus-freeze | ca3c3f8 |
| E-24.5 | v92 unrated baseline | **NO PREREG** (baseline) | comparator for later legs | obligation 8 (denominator rule) | b9394ef |
| E-24.6 | SITE re-price | **committed, BATTERY NEVER FIRED / RESULT NEVER BANKED** | — | discordant-pair ask, still unanswered | site-reprice-preregistration |
| E-25.1 | rush×map ablation | committed 19b8da3 (pre-play) | falsifier 2 FIRED — rush HARMFUL, worst on the band predicted to help | saturation rule (ouroboros/clanker probes measure nothing) | 19b8da3/d4b201b |
| E-25.2 | LOKI-3 kidnap | committed 7656924 | **STOOD DOWN pre-battery** (throws 16.7% vs 30% bar) | the treatment-occurrence template; obligation 9 (seat-rounds) | 7656924 |
| E-25.3 | real-TLE fidelity leg | covered by E-25.1 | 4-1 corroborates direction (p=0.19, not proof) | sourced self-play deflator ~2×; a self-play null isn't no-effect | 9039314 |
| E-25.4 | LOKI-4 ×3 + LOKI-QUIET | a676ca4 / 7beac55 | LOKI-4 8-7 53.3%; **QUIET INVALID ARM** (verified code not experiment) | obligation 11; seat confound self-inflicted | 6a2fae3 |
| E-25.5 | LOKI-6 arrival fixes | committed 685d3df | EXACTLY NULL — first published at 70% off partial fixture, self-corrected pre-successor | an incomplete run has no number, not a provisional one | 685d3df/712867d |
| E-25.6 | LOKI-7 composition | f42fdfb (premise struck pre-results) | 13/15 vs Eir 5/15 p=0.0078 — does NOT survive dropping Orizon (p=0.070) | fixture-relevance is a bar; significance leaned on a team we won't meet | 7d6b9c1 |
| E-25.7 | LOKI-8 + upward band | 93473bc | 15/25 vs 7/25 p=0.045; DOSE-RESPONSE 75%→60%→20% by opp strength | bars per band never pooled; "dies less totally" | 788d757 |
| E-25.8 | LOKI-9 garrison-less | 99874cf | REFUTED (40% vs 60%, 3/4 cells worse) — an INFERENCE refuted; first cut CRASHED (mixin no-op) | arena is the right place to test an inference; no knob-sweep | 23c1d79 |
| E-26.1 | LOKI-9 forward-survival | committed 6db96a2, **NEVER RUN**, later PROVEN INAPPLICABLE | planter already adjacent 59.4%; 0 forward-sentinel damage in 480 games | occurrence-zero saturation (D11 2nd species); Eir-tape subject fault | 57dcbfd |
| E-26.2 | LOKI-9 facing reorder | ff3e6bc (pre-leg) | **PROVEN-INAPPLICABLE NULL** — can_fire_from permits ≤1 facing, reordering a singleton is a no-op | 3rd falsifier branch made it cost one leg not two; absolute-pp bar went arithmetically impossible; D15 cwd-poison | 81c0ada |
| E-26.3 | LOKI-10 route-guard | committed deab025 (~5h pre-battery) | BAR NOT MET (control 58, variant 11 = 81%↓, bar was 0) | bar was a COVERAGE claim built on an OCCURRENCE measurement | 64efdde |

## STANDING CONSEQUENCES (pulled from the entries because they govern the live register)

1. **Join experiments on bot dir, not LOKI number** — the label is not unique.
2. **No pre-s27 leg except E-24.4 has a lock margin** — the two-clock standard
   begins there; earlier legs are single-clock by history, not by failure.
3. **The discordant-pair count is owed on five scoreboard verdicts** (LOKI-3
   +0.0, HOME −2.0, FLOOR −0.7, SITE −6.7, ESCALATE −7.8) and has never been
   supplied — so "four knobs, all nulls" cannot be distinguished from "the
   instrument could not see them." Named in a committed prereg; still open.
4. **Two batteries of 480 games each (LOKI-9 facing, LOKI-10) have NO recorded
   fixture** — opponents and maps absent from both leg blocks. The largest
   pre-s27 experiments cannot have their fixture reconstructed.
5. **Match ids for LOKI-6/7/8/9 legs were never recorded** — those legs cannot be
   re-decoded or re-verified against the platform.
6. **The pattern across the KNOWN-UNRECONSTRUCTABLE list is one thing:** results
   were banked, the APPARATUS around them (fixture, match ids, second clock,
   discordant pairs) was not. That is exactly what the live register + the
   durable match-id record (`docs/legs/`) now fix going forward.

*Full per-entry prose is in the backfill agent's report; the compact index above
carries every entry's prereg-status, outcome, method-fault and anchor, which is
the auditable core. If a prose detail is needed and absent here, it is a
documentation gap to close at the next experiment, not to reconstruct twice.*
