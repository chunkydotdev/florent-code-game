# ECON v2 REBUILD — AFFECTED-CLAIMS REGISTER (s39, 2026-08-14)

**Purpose (side-lane ask, 13:4xZ): this register exists BEFORE the rebuilt
table's numbers are read, so corrected numbers cannot be compared against
uncorrected claims silently.** The rebuild changes two things everywhere:
(1) the 31,986 drifted rows (files decoded after s36's `d62753c`) get their
TRUE column values; (2) **ALL eras** gain core unit-turns that were never
counted (9–15% more `turns_run`/`cpu_sum_us`; `cpu_max_us` changes wherever
the core was the peak spender). `shots` populates for pre-s36 files that
carried 0.

⛔ **THE ERA HAZARD, stated once for every future reader: any cpu- or
turns-denominated figure derived BEFORE this rebuild is a DIFFERENT
INSTRUMENT from one derived after.** Cite the rebuild date beside any
comparison that crosses it.

## Members, by column family

| # | claim | where | column family | status |
|---|---|---|---|---|
| a | "v125 runs at 87.6% of the TLE ceiling on 30x30" | QUEUE.md #44 | cpu | **RE-DERIVE, direction UNKNOWN** — cores add many cheap unit-turns, so mean cpu/turn can go DOWN while cpu_sum goes UP, and a max/p99 stat may not move. Until re-derived, 87.6% carries this caveat and is not citable as headroom. Owner: builder (next #44 touch). |
| b | "true cpu_max 6–8.4 ms" + the crash/CPU no-lever closure (0/371) | BOOK-0033-2026-08-14 | cpu | **RECHECK post-rebuild.** Owner: research. Direction of possible movement (⛔ corrected by the side lane — this line first said the opposite): the old cpu_max was a max over a SUBSET (cores excluded), so the corrected max can only RISE or hold ⇒ true headroom (10 ms − cpu_max) can only SHRINK or hold ⇒ **the no-lever closure can only WEAKEN or hold.** Practical expectation is "hold" (core turns are cheap), but the pre-registered direction points the way a reader must lean. The 0/371 crash count is cpu-column-independent and stands regardless. |
| c | any `ti_collected_end` read on v55+-era files | various (wrap-era embargo) | ti | Embargo HOLDS until the rebuild lands and this register's owner marks it. After the swap, v55+ reads are live again. |
| d | research #49 agent's r0–150 ti outcome on newer games | research s39 notes | ti | Already caveated at write time; re-derive on the rebuilt table before any promotion. Owner: research. |

## Closed by the repair itself

* `tled` retraction-of-the-retraction: the field is real (botOutput field 4);
  the column now carries true values on all rows. The Ouroboros census
  (26,356 tled unit-turns) was reading the wire, not the column — unaffected.
* `build_agg.tsv`: verified unaffected (741/742) — no member here.
* The fault CLASS (header drift on append) is guarded in `sync.py` for every
  appended surface, selftested 4 ways; `replay_econ.py --check-header` refuses
  a mismatched destination.

## Marking

When the rebuild lands (gated swap: single 19-col width + coverage vs the
ledger), the builder appends the completion line + old-table path here.

**LANDED 2026-08-14 (fill in at swap): pending.**
