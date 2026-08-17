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

3. **prereg_check: add the DEFENCE_ADMISSION_BAR rule** — 0 matches for
   `DEFENCE_ADMISSION|RMST|r300` (35 `def ` positive control), unchanged since
   s47's measurement; the s47 WRAP-FIX agent specced it at ~10 lines + fixtures
   with both test verdicts routed. ⭐ JUSTIFICATION UPGRADED s48: research
   applied the bar BY HAND for the v155-vs-v152 timely-kill read and slipped
   exactly the way the rule would catch — quoted the DEFF half-width where the
   interval's LOWER BOUND belonged (largest un-excluded regression −14.6pp,
   not −13.1pp), erring in the null-flattering direction. n=1 and caught
   (side lane), but the failure is no longer hypothetical. Cheapest item,
   best-evidenced.

4. **queue_check: prose-negation escape** — `GREP-TREE` appears only in a
   comment (queue_check.py:571), 0 rows use the token. Re-derived s48 by the
   side lane, still open.

5. **Stale comment: `raid.py:782-784` (incumbent tree)** claims
   `get_attackable_tiles_from` "has ZERO call sites anywhere in this tree" and
   is contradicted four lines below itself (:786-790 materialises enemy gunner
   rays, consumed at :831). Doc-only; fix on next tree touch or at wrap.
   (Research batches 2+4, s48.)

6. **fleet_dispatch.py:1590 stale `--control` default** —
   `default="bots/_v223sealrepair"` in live argparse; any `--seed-from` run
   omitting `--control` seeds rows on the superseded benchmark and trips the
   guard-6 refusal. Running daemon is `--once --remote-mode live` (no seeding)
   so DEFER — but it bites the NEXT seeding run. Fix: default from PROGRAMME
   INCUMBENT the way control_pin.incumbent() does. Also unassessed-stale:
   era_guard.py:197 `LIVE_VERSION_HINT = 140`. (Side lane s48.)

7. **orchestrate.sh cmd_start: `CORES` unbound when WORKERS arg omitted**
   (line 452 under set -u) — worked around by always passing WORKERS
   explicitly per host_capacity.tsv; fix is initializing CORES="" outside the
   `[ -n "$W" ]` branch. Found spinning up ws1 on Magnus's order, s48.

8. **⛔ ANNOTATION FOR WHOEVER CLOSES THE REMOTE GATE GAP (s47 wrap debt 12):**
   closing it retroactively invalidates the band-readings of any IN-FLIGHT
   remote prereg whose reachability assumes full n (KLADLADDER's locked
   four-band reading is the live instance — its falsifier is reachable ONLY
   because ws1 shards cannot be auto-stopped). Check for in-flight remote
   shards with locked band-readings BEFORE closing the gap. (Side lane s48.)

9. **corefill.sh:310 shell error on the empty-worklist path** — after the s48
   re-pin, the runner printed "COREFILL done." then
   `tools/corefill.sh:310: command not found: SH:-` / `= not found` (looks like
   a `${SH:-...}` parsed under the wrong shell). Loop-relevant only if it
   prevents relaunch when real work arrives — VERIFY when the ladder-no-cap
   shard is queued; fix at wrap if benign.
