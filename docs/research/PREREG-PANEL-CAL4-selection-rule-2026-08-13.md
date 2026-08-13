# PREREG — PANEL CAL-4 SELECTION RULE (committed before any CAL-4 game fires)

**Research arm s37, 2026-08-13. This prereg commits the SELECTION RULE and the
look schedule; the concrete cell list and frozen E gaps are recorded by the
builder at fire time as an ADD-only amendment (live ratings drift — Obligation
14 requires re-verify at selection, so freezing gaps now would fake precision).**

## Why a new panel
CAL-3's pre-committed n=150 look is TAKEN and SPENT (2026-08-13 ~20:4xZ,
disclosed late — boundary passed at n≈150 while no instrument watched; the
wake now exists: session Monitor + the durable runner-side fix routed to the
builder). Our rating moved 1646 → 1783 in one day; a calibration panel
measures RELEVANCE and the relevant band has moved up with us.

## Selection rule (six cells)
1. **Band admissibility at selection time**: every cell team must be
   admissible per `target_value.py --band` run LIVE at selection (not cached;
   the 20:26Z basis below is a CANDIDATE list, not the selection).
2. **Continuity cells (2-3)**: keep C3 Leviathan (in-band, our largest bleed,
   camp-class — unless its live gap exceeds the +125 ceiling at selection, in
   which case record the exclusion and substitute the nearest camp-class
   in-band team); keep C1 team lazy if still in-band. C5 Juusto only if
   in-band at selection (borderline −79 at boot).
3. **Drop**: C6 Coreflood (−99 at 20:26Z live read — below band) and any cell
   whose live gap is below the band floor at selection.
4. **Upward stratum (2-3 new cells)**: from the 20:26Z candidate basis —
   Erebus (+0), HTTP 418 (+50), 0033 (+59), farming_200s (+73) — re-verified
   LIVE at selection with a version-stability check (`league_matches.tsv`
   timeline; a team mid-ship-storm is noise, note it in the cell).
5. **Never pin any cell** (design rule: churn is signal in a panel).
6. **E gaps frozen at selection**, recorded in the fire-time amendment;
   per-cell oppver mix REPORTED at every read (the Jython v33→v119 lesson).

## Look schedule
* Descriptive reads any time; **comparative look at proper-n = 150 ONLY**
  (first 150 in completion order, `panel_read --panel cal4 --look 150`).
* Proper-n counts ONLY the CAL-4 runner's own fire-log accepts (R5: leg games
  vs shared opponents are excluded by construction; any other counter is not
  the denominator).
* **The boundary has an instrument this time**: a research-session Monitor
  watches `scratchpad/panel_cal4_fires.tsv` for ≥30 accepts (with a 45-min
  stall alarm), and the DURABLE fix — the runner itself printing/refusing at
  the boundary — is routed to the builder as spec (D2-class: enforcement
  inside the tool, not in a session watcher).

## What this prereg does not license
No verdict sentences (builder's), no ship inference from panel deltas, no
comparative read before proper-n 150, no mid-scan cell changes ("nothing
changes mid-scan; the boundary executes it" — Magnus + side lane, 20:2xZ).

---

## AMENDMENT 1 (ADD-only, 2026-08-13T20:34:15Z, before any CAL-4 game fires) — the D13 resolution rider (side lane)

CAL-3's C3 read ±0.000 cluster SE — **every Leviathan match exactly 1/5, a
floor-pinned cell: it measures the OPPONENT, not treatment deltas, because it
has no variance to price a delta against.** Therefore selection asks TWO
questions per cell, not one:
1. in-band at live selection (rule 1 above), AND
2. **can the cell RESOLVE anything** — D13's prospective check: the cell's
   per-match spread in recent games vs this opponent (fire-log/corpus, our
   holder only). A cell at a constant share is admitted only DELIBERATELY,
   recorded as a reference cell whose deltas will not be readable.
Keeping Leviathan may still be right (three surfaces converge on the camp
class; a stable reference has value) — but the fire-time amendment must say
which kind of cell it is.

---

## FIRE-TIME AMENDMENT (ADD-only, builder s37; clock = this commit's git
## author time) — CELLS SELECTED, E GAPS FROZEN

Live band read at selection (`target_value.py --band`, our 1783, corpus
0.4h fresh): 12 admissible. **Cells:**
* C1 team lazy **−2** (continuity, in-band)
* C2 Juusto **−67** (continuity, in-band; was borderline at boot, admissible
  at selection)
* C3 Leviathan **+101** (continuity, in-band under the +125 ceiling;
  **REFERENCE CELL per the D13 rider** — CAL-3 read it floor-pinned at
  ±0.000, every match 1/5; kept DELIBERATELY as the camp-class reference,
  its deltas declared unreadable)
* C4 HTTP 418 **+38** (upward; churn NOTED: 4 versions in its last 15
  matches, last change 17:32Z)
* C5 0033 **+64** (upward; stable, 2 versions/15)
* C6 farming_200s **+73** (upward; most stable, 1 version/15)
* **Dropped:** Coreflood (below band, as the rule forecast). **Excluded:**
  Erebus (+10) — SHIP-STORM at selection (5 versions in 15 matches incl. an
  apparent rollback 102→63); the rule's version-stability check exists for
  exactly this.
* **E gaps frozen as listed above** (basis: our 1783 vs the live table);
  per-cell oppver mix reported at every read; no cell pinned (panel rule).
* Runner: `tools/panel_cal1.sh` cells updated in place (tracked, committed —
  the runner is the record); fresh `panel_cal4_fires.tsv` + pointer 0; the
  30-accept boundary stop rides in the runner.
