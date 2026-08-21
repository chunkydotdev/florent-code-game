# PLAYBOOK: MOVE MINING — the continuous new-moves loop

COMMISSIONED by Magnus, 2026-08-16 (s47), verbatim: *"What you're doing now
should be in the loop somehow, we need to continuously find out new moves."*
The "what you're doing now" was the three-agent replay study whose first
report is `REPLAY-STUDY-0033-2026-08-16.md` — this playbook is that method,
written down so it recurs, with the trigger instrument that decides WHEN and
the ledger that records WHAT has been covered.

## The loop

1. **TRIGGER** — `.venv/bin/python tools/move_miner.py` (runs at research
   boot; builder runs it if no research lane is up). It reads the rated tape
   and `move-mining-ledger.tsv` and names the opponents with enough
   UNSTUDIED games on their CURRENT version (≥40, or ≥20 when our all-time
   share against them is under 45%). A version bump by the opponent resets
   their coverage — a new version is a new bot. BLIND on a stale tape, never
   quiet.
2. **STUDY** — one fresh opus subagent per candidate (same isolation rule as
   preregs: no inherited session context beyond named inputs). The brief that
   worked is reusable: give it (a) the ground (which opponent/map/segment and
   why), (b) our playstyle for compatibility, (c) the decode toolkit
   (`tools/replay_schema.md`, `tools/corpus/replay_autopsy.py`,
   `tools/replay_census.py` primitives, `corpus/join.tsv` for file lookup),
   (d) the EXCLUSION LIST of already-known/queued ideas — refreshed from
   QUEUE.md at commission time, or the study rediscovers the queue.
3. **DISCIPLINE inside the study** (what made the 0033 report trustworthy):
   * every claim labelled **MEASURED** (counted from decoded events) or
     **EYEBALL** (seen once, needs a count before it is quoted);
   * every mechanism claim carries a **control that must run the other way**
     — the exemplar is the gunner plug's sentinel control (obstacle-immune
     shots cannot be plugged, and measured 1.6 vs 6.6);
   * refuted mechanisms are RETAINED in the report so nobody re-derives them
     (the 0033 study killed two in passing);
   * ⭐ **the IN-LEG MIRROR CONTROL** (added 2026-08-21 s53, from the KLADDEDOSE
     decode): when the OPPONENT performs the very verb your leg is dosing (kladde
     pecked a core in 7c3e9ae0 g3), side-swap the decoder and confirm every
     column flips — a free positive control that validates the instrument on
     live data inside the same leg, no fixture needed;
   * a piece is SMALL (one behaviour), cited at ≥2 games with file+round
     anchors, and sketched against OUR doctrine (<r300 kill).
4. **BANK** — the report is committed verbatim under `docs/research/` with a
   provenance header (agent, inputs, ground). Agent reports die with the
   session; an unbanked study did not happen.
5. **LEDGER** — append one row to `move-mining-ledger.tsv`:
   `date  opp  oppver  games_covered  doc`. This is what stops the trigger
   re-firing on covered ground.
6. **ROWS** — research admits the pieces as QUEUE.md rows (normal admission
   gate: GREP against the incumbent). A piece that cannot name what the
   incumbent currently does is not admissible yet.

## Scope notes

* Non-opponent grounds (a map segment, a mechanic sweep across teams) do not
  fit the per-(opp,version) ledger; they are commissioned by hand when a
  segment cut points at one. The trigger automates only the opponent
  dimension, which is where staleness is measurable (their version bumps).
* The trigger's thresholds live in `tools/move_miner.py` and nowhere else.
* Building planks from pieces stays the builder's; admitting rows stays
  research's; nothing here changes lane limits.
