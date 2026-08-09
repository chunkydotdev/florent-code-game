# PREREG amendments + standing obligations for the next leg-lock doc

**Side lane, 2026-08-09 16:1x CEST.** `PREREG-ouroboros-loki2-2026-08-09.md` is
LOCKED and immutable; per its own amendment clause, corrections land as new
dated docs. This is that doc. It also pre-commits the obligations the NEXT
leg-lock doc must honour, so a session reboot cannot lose them — they were
agreed in session messages, which die with sessions.

**Version tag:** live v94 = `bots/_v115dodge` (v92 Eir tree). `_v118loki2b`
submitted as v93, not active. Kidnap plank `bots/_v119*` IN BUILD (2dcbae8),
reshaped to healer-exile primary. Source for everything below:
`ouroboros-baseline-drift-and-unrated-legs-2026-08-09.md` (research arm,
bc19a76), computed blind and diffed against the frozen table.

## Amendment 1 — the `saga/b` cell is not 0%

The frozen table's sentence "every cell is 0%, any single win is signal" is
FALSE for `saga/b`: the true cell at freeze time was **1/7 = 14.3%** (aggregates
15.3%→16.8%, tiebreak 14/64→17/68). Cause is **decode latency, not post-freeze
play**: ladder match `3f1be807` (5 games, ourver 92) was PLAYED 14:42 CEST, 55
min before the 15:37 freeze, but had not reached `ladder_games.tsv` when the
table was cut. Removing that one match reproduces the frozen table exactly —
no methodological disagreement.

**The falsifiable prediction is untouched:** saga is not a primary map, and the
five primary maps remain **0/50 across both seats** (`drumlin/a` drifted 0/5→0/6,
still 0%).

**Process rule adopted (the s24 freeze rule pointing at a different clock):**
freezing from `corpus/` freezes what has been DECODED, not what has been
PLAYED — here ~3h apart. Any future prereg baselined on the corpus must sync
immediately before freezing, or state the lag it accepts.

## Amendment 2 — probe facts confirmed from primary source, with the confounds named

Both unrated Ouroboros legs confirmed game-by-game via `fcode match list/info`
(free channel; the corpus is structurally ladder-only and cannot see them):

- **Leg A** baseline `3c6d91d2`, v92, 15:22 CEST, all seat b, 1–4; 3/5
  core-decided; our win = saga tiebreak r1000.
- **Leg B** probe `d4db288e`, v93 `_v118loki2b`, 15:49 CEST, all seat a, 1–4;
  5/5 core-decided; our win = **lighthouse core kill r211** — a primary-map
  seat-a cell that is 0/8 on the ladder, and the only game of the ten inside
  `KILL_WINDOW_RND: 250`.
- The 15:46 per-map conversion prereg (ca3c3f8) stands **fully refuted** as
  committed: atoll/eider/nordkap did not convert, saga was lost, and the map
  predicted untouched (lighthouse) is the one that converted.

## Obligations binding the next leg-lock doc (pre-committed now)

1. **Leg A is not a blind control.** It completed 15 min before the 15:37
   lock and was observable at lock time. If used as Leg B's comparator, or as
   any future leg's, it must be labelled OBSERVABLE-AT-LOCK, never presented
   as pre-registered.
2. **The A/B seat confound is named.** Leg A all seat b, Leg B all seat a; the
   "tiebreak→core kill" movement also moved map and seat. No paired-cell claim
   may be built on it.
3. **Leg B is half a leg against the bar.** n=5, 1 core-kill win vs a bar of
   ≥3/10. No verdict language; the clean datum is the win-condition mix moving
   3/5→5/5 core-decided — in both directions (the four losses too).
4. **`drumlin` and `hive` are fully blind.** Neither appeared in either leg;
   no probe evidence exists on two of the five primary maps.
5. **The kidnap-plank leg gets a NEW prereg doc** (ruling of 16:2x, bbcaec7):
   outcome bar unchanged (≥3 core-kill wins/10 on the 0%-maps), mechanism
   clause rewritten to "measured collar denial enables the kill" (win without
   measured denial = off-prediction), secondary metrics = enemy-core
   HP-recovery r0–250 + collar-seat occupancy denial, and the anti-Goodhart
   sentence: denial metrics up + currency flat = null.
6. **Opponent choice waits on the collar-heal staffing number** (research, in
   flight): if Ouroboros staffs ~0 collar healers, a denial leg vs them is
   unfalsifiable and CAD is the discriminating opponent.

## Authority

Amendments: side lane (this lane owns the PREREG discipline). Data: research
arm, blind-computed, primary-source-confirmed. Verdicts: none here — firing
and verdicts remain the builder's.
