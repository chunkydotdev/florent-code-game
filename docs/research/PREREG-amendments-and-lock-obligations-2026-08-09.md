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

## Addendum, 16:3x CEST — the 15:46 prereg's lock certified, its refutation sharpened, obligation 7 adopted

Research certified the 15:46 conversion prereg's lock against two independent
clocks: `ca3c3f8` git author time **15:46:23 CEST**; Leg B platform
`createdAt` **15:48:56 CEST** (ran 15:49:02→15:49:53, 57 seconds). **The
prereg predates leg creation by 2m33s — genuinely blind to Leg B.** (This
paragraph supersedes the bare "15:46/15:49" times above; the two-clock form is
the one that survives a reboot.)

**But the refutation is sharper than "fully refuted", and one half of the
prediction was unfalsifiable as worded.** Side-by-side on win condition (a
game property, so it survives the A/B seat flip):

| map | Leg A (v92) | Leg B (Loki-2b) | prereg said |
| --- | --- | --- | --- |
| atoll | core L 563 | core L 720 | "converts to core kill" |
| eider | core L 521 | core L 338 | "converts to core kill" |
| nordkap | core L 279 | core L 361 | "converts to core kill" |
| **lighthouse** | tiebreak L 1000 | **core W 211** | "does not touch" |
| **saga** | tiebreak W 1000 | **core L 351** | "does not lose" |

Atoll/eider/nordkap were **already core-decided at lock time** (Leg A completed
15:22, observable at 15:46) — read as "core-decided rather than tiebreak" the
prediction was pre-satisfied and could not fail honestly; read as "core kills
IN OUR FAVOUR" it went 0/3. And the only two games whose win condition changed
are exactly the two the prereg excluded from change. **The prediction was
anti-correlated with its own outcome variable: 2/2 on excluded maps, 0/3 on
named maps.**

**Obligation 7 (adopted, generalises past Ouroboros):** a pre-registration
must state whether its outcome is the win-condition MIX or the win-condition
IN OUR FAVOUR, and must verify the predicted-change set is not already in the
target state at lock time. A prereg predicting change on cells already changed
cannot fail honestly. (The LOCKED 15:37 file already satisfies this — it names
"`core_destroyed` in OUR favour, not a tiebreak steal" — which is the template.)

## Addendum 2, 16:4x CEST — obligation 3 sized with numbers; denominator rule; the r74 outlier

From research's v92 unrated-baseline audit (`v92-unrated-baseline-audit-2026-08-09.md`,
b9394ef), adopted into the obligations:

**Obligation 3 is amended to carry its own numbers:** the 3/5→5/5
core-decided movement is **Fisher one-sided p = 0.2222** (two-sided 0.4444) —
a direction, not a result — and at fixed bot version v92's own core-decided
share spans **0%→100% by opponent** (CAD 100%, KCM 75%, Ouroboros 60%, Lunds
50%, Powerpuff 0%), wider than the 60%→100% the probe is read for. The
same-opponent framing (Ouroboros vs Ouroboros) remains the right comparison;
these numbers size it so no later reader inflates it.

**Obligation 8 (denominator rule):** the 4-13 v92 unrated baseline is
game-pooled from legs of **5/5/4/2/1** maps (verified fired-short, not
truncated). Ouroboros and CAD carry 29% of it each, Powerpuff 6%. Any "LOKI
delta vs baseline" compares **per-opponent or states the Ns**; the five teams
are not five comparable cells.

**Noted, not an obligation:** `f92f1ca2` game 5 (nordkap, seat a, unrated,
v92) — **CAD core killed at r74**, resignMessage null, the fastest kill on our
record, 3x faster than our ladder-kill median vs CAD (r217, plants from r125,
n=11). Side-lane autopsy in flight; mechanism unknown until it lands.

## Authority

Amendments: side lane (this lane owns the PREREG discipline). Data: research
arm, blind-computed, primary-source-confirmed. Verdicts: none here — firing
and verdicts remain the builder's.
