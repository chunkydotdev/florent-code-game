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
- 2026-08-14T16:1xZ CLOSED-BY-LEG INDEX (sonnet; research NEXT-1) → docs/research/CLOSED-BY-LEG-INDEX-2026-08-14.md
- 2026-08-14T16:0xZ WORST-MAPS BOOK (opus, Magnus directive; brief ce464012) → docs/research/BOOK-worst-maps-2026-08-14.md
- 2026-08-14T15:5xZ OPP-SEGMENT-MAP (sonnet) → docs/research/OPP-SEGMENT-MAP-2026-08-14.md

## NEXT (ordered; anyone may append with a line + rationale)
(NEXT re-stocked by research 16:0xZ:)
2. LIVELOCK-SIGNATURE DISCRIMINATOR (sonnet) — settles candidate 1's
   disease-prevalence vs area attribution; cheap and decisive.
3. Leviathan book — DEFERRED, re-admission trigger = rating gap under ~+125
   (not a calendar).

**RE-STOCKED by research 2026-08-14 ~15:5xZ. Ordered by VALUE, not ease. Each
line names its brief or its primary so the spawner needs no further design
input.**

1. **CLOSED-BY-LEG INDEX** (sonnet) — **build the join that does not exist.**
   For every `bots/_v*/` tree, grep its doctrine/main headers for a `QUEUE #NN`
   citation (**the convention already exists** — `_v207apprlaunch`'s block opens
   *"LOKI-APPR (QUEUE #47 = #28 × #45-iter3)"*), then cross-reference
   `docs/legs/`, `results.tsv` and the coordination tape for that arm's LIVE
   outcome. **Output: row → arm → live verdict, and specifically THE LIST OF ROWS
   WHOSE ARM HAS A LIVE LEG THAT THE ROW DOES NOT MENTION.**
   *Rationale: tonight `#47` was ranked to the TOP of the live fire order — by
   me, reading it cold — because the row listed its screens exhaustively and
   omitted its live −1. **Nothing in this repo can answer "has this row's arm had
   a live leg, and what did it say?"** That instance was caught by luck (I
   happened to read a doctrine header while designing its prereg). This finds
   the rest. ⛔ **A keyword scan CANNOT substitute: I ran one, it flagged 10
   rows, and that is the NORMAL state for planks never fired live — not a defect
   count.** The defect is only visible by joining arm → row → leg outcome.*

2. **LIVELOCK-SIGNATURE DISCRIMINATOR** (sonnet) — per-map livelock signature of
   `_v187saltidle_f` (the 0/14-signature fixture from the v139 work): **which
   maps ever had the disease.**
   *Rationale: settles candidate 1's attribution, currently a standoff between
   the builder's disease-prevalence story (the screen measures FIX vs DISEASE and
   the disease is segment-conditional — T=53.0 with the parent near 47 means
   there was nothing to fix on frostgate/royale) and my area story (both 53.0%
   maps are 20×20=400). **Cheap, decisive, and it settles an argument neither of
   us should win by rhetoric.** Note the out-of-table story is ALREADY DEAD on
   the primary: all 25 pool maps sit in `MAP_CODES` with EXACT terrain in every
   tree back to v125.*

3. **SEGMENT-AWARE OPPONENT BOOK REFRESH — Leviathan, DEFERRED not dropped**
   *(lowest priority, and stated so the reasoning survives): they are 1997.8 and
   the ladder has nearly stopped pairing us (2 matches in the current era), so a
   book on them is archaeology TODAY. **Re-admit only if they re-enter our
   pairing band** — the trigger is a rating gap under ~+125, not a calendar.*

## COMPLETED (newest first; the report commit is the verdict record)
- 2026-08-14 HOME-LOCK MECHANISM (opus) → sealed pockets + BELTBLIND; SPAWNPOCKET candidate routed
- 2026-08-14 CAL-7 SALVAGE (sonnet) → docs/research/CAL7-SALVAGE-2026-08-14.md (descriptive, no alarms, research consumes)
- 2026-08-14 ENGINE-238-DELTA (sonnet) → RULES-IDENTICAL; A1 caveat closed at source level; side finding: same-seed local runs non-reproducible even within one version
- 2026-08-14 QUEUE-ECONOMICS (opus) → docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md (6 answered rows, kills, top-5 — routed to research)
- 2026-08-14 SEGMENT-SWEEP (fable) → docs/research/SEGMENT-SWEEP-2026-08-14.md (3 candidates routed; NEXT-1 sizing absorbed)
- 2026-08-14 AUDIT (opus) → docs/workflow-analysis/AUDIT-2026-08-14-s39.md
- 2026-08-14 V141VS140 per-map splits (sonnet) → banked in coordination tail 14:2xZ
- 2026-08-14 ECON-DECODER diagnosis (opus) → tools/corpus/replay_econ.py v2 + register
- 2026-08-14 QUEUE-ROW extraction (sonnet) → consumed into the s39 VPS slate
