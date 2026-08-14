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
- 2026-08-14T15:1xZ SEGMENT-SWEEP (fable, Magnus-authorized) → docs/research/SEGMENT-SWEEP-2026-08-14.md
- 2026-08-14T15:2xZ QUEUE-ECONOMICS (opus) → docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md

## NEXT (ordered; anyone may append with a line + rationale)
1. SEGMENT-CANDIDATE SIZING — take the segment sweep's top candidates and
   draft the 15c re-screen preregs (segment, 15a direction, n, cost). Opus.
2. ENGINE 2.3.6→2.3.8 CHANGELOG CHECK — closes the "transfer UNVERIFIED"
   caveat on SCREEN-v140vs142 A1 and pre-clears the fleet upgrade boundary
   (s38 checklist taped). Sonnet if the changelog is published; opus if it
   needs binary diffing.
3. HOME-LOCK MECHANISM — WHY two-tile limit cycles form at our own core
   (23x concentration, research's inversion): decode 10-20 locked-bot
   trajectories from replays; the answer designs the nav arm that beats the
   51-bar (mapfix-class candidate). Opus.
4. CAL-7 SALVAGE READ — the 110 descriptive games: per-cell tallies + ob-14
   churn only, labeled non-comparative (research to consume; no P1). Sonnet.
5. OPPONENT-POOL SEGMENT MAP — which live opponents concentrate on which
   map segments (pairing × map from league_matches if map-columned):
   connects Obligation 15 segments to live-leg targeting. Sonnet.

## COMPLETED (newest first; the report commit is the verdict record)
- 2026-08-14 AUDIT (opus) → docs/workflow-analysis/AUDIT-2026-08-14-s39.md
- 2026-08-14 V141VS140 per-map splits (sonnet) → banked in coordination tail 14:2xZ
- 2026-08-14 ECON-DECODER diagnosis (opus) → tools/corpus/replay_econ.py v2 + register
- 2026-08-14 QUEUE-ROW extraction (sonnet) → consumed into the s39 VPS slate
