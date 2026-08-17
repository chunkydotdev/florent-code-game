# s48 WRAP DEBT LIST (tooling fixes deferred to wrap per Magnus's momentum rule, 2026-08-16)

1. **now.py: ADD A RETRY, do NOT relax the gate.** now.py exits 2/BLIND on the
   platform's PARTIAL response state (rating+rank present, no active_submission)
   while raw `fcode status` text sometimes carries the full block in the same
   second. The flap is sub-second (side lane s48: 5 samples in 2 s, 1 FULL), so
   ONE retry converts most BLINDs into reads. ⛔ The active_submission gate is
   CORRECT and its selftest asserts it — in PARTIAL, now.py is the only
   instrument that can tell FULL from PARTIAL; a text reader grepping `Rating:`
   cannot. Retry, don't relax. (Side lane s48 04:2xZ, consumed.)

2. **submit_clean.py: fail CLOSED on unknown holder.** `_holder()` returns None
   when `Active bot:` is unreadable; the restore chain at :473/:497 folds
   None==None into "holder unchanged" and exits 0 — 4 of 6 before/after states
   leave a prototype live on the rated ladder reporting success; `--leg` mode's
   hold + LEG_TIMEOUT_S never arm in a blind window. Fix: an explicit
   `holder_before is None or holder_after is None` arm that exits non-zero with
   "HOLDER UNKNOWN — VERIFY AND RESTORE BY HAND NOW". `--activate` path
   unaffected (returns earlier). Spec = side lane s48's driven state table
   (coordination tail ~04:2xZ). Session constraint until fixed: NO
   submit_clean invocation in any mode while status is flapping.
   ⭐ FIX IS A COPY, NOT A DESIGN (side lane sweep, banked in
   docs/research/FLAG-submit-clean-unknown-holder-2026-08-17.md): make
   submit_clean do what `ship_ledger.py:567` already does — test None BEFORE
   any comparison, return 2. Sweep of all six ship-chain holder consumers came
   back NEGATIVE (defect isolated to submit_clean); scope was ship-chain
   live-holder readers only, not a repo-wide unknown-folding audit.

3. **corefill.sh:310 shell error on the empty-worklist path** — after the s48
   re-pin, the runner printed "COREFILL done." then
   `tools/corefill.sh:310: command not found: SH:-` / `= not found` (looks like
   a `${SH:-...}` parsed under the wrong shell). Loop-relevant only if it
   prevents relaunch when real work arrives — VERIFY when the ladder-no-cap
   shard is queued; fix at wrap if benign.
