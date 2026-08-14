# SPEC — six machine-checkable checks `tools/prereg_check.py` must carry (side lane, s40, 2026-08-14)

**Context:** the builder is drafting `tools/prereg_check.py` (Magnus's prereg-automation
ask, IN-FLIGHT at `1a9f14b`). The tool mechanises this lane's charter, so these are the
lane-ledger checks that are MACHINE-CHECKABLE and not named in the IN-FLIGHT announcement
(which already carries: target band, DEFF half-width at planned n, segment ceiling,
boundary in accepts AND games). Token vocabulary is research's to bless per the builder's
ASK; this spec is the check list, sent to the builder in-session the same minute and
committed here because session messages die with sessions.

| # | check | incident it closes | mechanisable form |
|---|---|---|---|
| 1 | **Bar-null assertion** — structured block (bar value, comparator base rate, source of each); assert `bar != base_rate` | 3/10-vs-29.6% (2026-08-10); enforcement-ledger mechanisation candidate #2, specified 08-10, never built — the oldest unbuilt spec in the ledger | one comparison over two declared tokens |
| 2 | **Obligation 13 intersection COMPUTED, not declared** — `MECHANISM METRIC READS <file:line>` × `TREATMENT DIFF TOUCHES <paths>`: run the actual diff and verify the claimed intersection | LOKI-18: 25 games on an inert bar (metric behind a guard in a byte-identical file) | `git diff --stat` membership test |
| 3 | **Reference-side resolution floor** — the half-width computation must include the reference's fixed-n floor at panel n=∞; a bar below that floor is unresolvable BY CONSTRUCTION | CAL-7 P1: ±8pp bar under a ±9.1pp floor set by a retired reference (n=155, cannot grow); found after 4 preregs + 5 amendments | closed-form from reference n + DEFF |
| 4 | **Bar line names its ESTIMATOR and CLUSTERING UNIT** | s28 ring-hold: four estimators within 0.010 of the bar, MEET/MISS flipping among them | presence check, two tokens |
| 5 | **Planned n + cut-short clause present** | s28 LOKI-16b (unfixed n permits optional stopping); CAL-8's 2026-08-14 stop is the live example of the cut-short branch doing work | presence check |
| 6 | **ADD-only amendment enforcement** — an amendment may only ADD a constraint; loosening/retargeting/reinterpreting an existing bar is a NEW prereg | s28 timestamps-prove-WHEN-never-WHAT: two honest clocks beside a quietly widened bar certify clean | diff class over the locked file: flag any amendment commit that EDITS an existing bar/branch line rather than appending |

**Also carry** (mechanisable part is the presence-of-declaration; the judgment stays human):
Obligation 12 (a gate states the n at which it discriminates its branches; unresolved
defaults to the RESTRICTION) · Obligation 7 (predicted-change set not already in the
target state at lock).

**Certification offer, in-lane and standing:** when the draft lands, the side lane runs
the forced-fail certification — every obligation check driven to its FAILING verdict on a
corrupted fixture, per the `tools/corpus/meta_attrib.py` standard (each corruption aimed
at a DIFFERENT check, mutating real prereg text, agreement required to collapse). A check
that has never produced the other verdict has not been seen to check. Wiring-into-the-
firing-path verdict stays the builder's; vocabulary stays research's.
