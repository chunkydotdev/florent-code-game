# AGENT PIPELINE — the rolling analysis queue (Magnus, s39 2026-08-14)

**The rule (builder lane, standing):** there is ALWAYS at least one analysis
agent running (opus default; fable on Magnus's say-so for wide sweeps). When
an agent completes: (1) its report is COMMITTED+PUSHED under docs/research/
or docs/workflow-analysis/ — that commit IS the durable, revertible verdict
record; (2) the builder types receipts/routes findings; (3) the builder
IMMEDIATELY spawns the next item from this file. An empty NEXT list is a
stocking failure — flag research (analysis items) or Magnus (direction).

**The guarantee:** the builder's 30-min gate heartbeat prints this file's
state (in-flight count + next-item count + last-spawn time), so a stalled
pipeline surfaces within one heartbeat. At wrap, in-flight agents die — the
HANDOVER top block carries this file as a re-arm duty and the successor
respawns from NEXT on boot.

## IN-FLIGHT (update on spawn/completion; timestamps from date -u)
- 2026-08-14T15:5xZ OPP-SEGMENT-MAP (sonnet) → docs/research/OPP-SEGMENT-MAP-2026-08-14.md
- 2026-08-14T15:2xZ HOME-LOCK-MECHANISM (opus) → docs/research/HOME-LOCK-MECHANISM-2026-08-14.md

## NEXT (ordered; anyone may append with a line + rationale)
⛔ NEXT IS EMPTY (15:5xZ) — stocking flag raised to research; the worst-maps
book brief (Magnus directive) is the obvious refill.

## COMPLETED (newest first; the report commit is the verdict record)
- 2026-08-14 CAL-7 SALVAGE (sonnet) → docs/research/CAL7-SALVAGE-2026-08-14.md (descriptive, no alarms, research consumes)
- 2026-08-14 ENGINE-238-DELTA (sonnet) → RULES-IDENTICAL; A1 caveat closed at source level; side finding: same-seed local runs non-reproducible even within one version
- 2026-08-14 QUEUE-ECONOMICS (opus) → docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md (6 answered rows, kills, top-5 — routed to research)
- 2026-08-14 SEGMENT-SWEEP (fable) → docs/research/SEGMENT-SWEEP-2026-08-14.md (3 candidates routed; NEXT-1 sizing absorbed)
- 2026-08-14 AUDIT (opus) → docs/workflow-analysis/AUDIT-2026-08-14-s39.md
- 2026-08-14 V141VS140 per-map splits (sonnet) → banked in coordination tail 14:2xZ
- 2026-08-14 ECON-DECODER diagnosis (opus) → tools/corpus/replay_econ.py v2 + register
- 2026-08-14 QUEUE-ROW extraction (sonnet) → consumed into the s39 VPS slate
