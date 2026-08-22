# s55 wrap debts (builder) — fixed at WRAP only (Magnus s48 rule), unless the loop stalls

1. **CLAUDE.md ladder-scoring block cites `WIN_RATE_IS_VERDICT: no` — the field flipped
   no→yes 2026-08-11 (d7b0248dc, Magnus "WIN RATE DECIDES", PRIMARY_CURRENCY: game_share).**
   Substance of the paragraph stands (game share is the currency); only the quoted field
   value is stale. Research flagged 2026-08-22 ~10:1xZ with paste-ready text on the tail
   (third instance of the always-loaded-file divergence class). Side lane verifies
   text-vs-evidence at the batch commit.

2. **From the s55 boot-fire audit (docs/workflow-analysis/AUDIT-2026-08-22-s55-boot-fire.md)**
   — all audit_trigger repairs were ALREADY s53 wrap debt and have now survived TWO wrap
   cycles unrepaired; the audit spent a second session on the same cells:
   a. results.tsv: no row type for refusals/deferrals (28 of 96 window decisions = 29%,
      zero on the tape); DECISION_KINDS omits `cancellation` (auto_gate.py:173 writes it;
      28 of last 50 rows); counters recognize 6/50 rows (12%).
   b. ship-cadence cell: counts rollbacks as decisions, shared-account numerator over
      our-git denominator, missed the v180 activation entirely, saturating denominator.
   c. delegation-drought cell: both regexes match 0 of 7 real in-window headers
      (3-line window vs 4-6-line wrapped headers); 0/0 prints healthy.
   d. selftests are frozen-fixture-only — pass 6/6 while every live defect is format
      drift. The audit's own phrase: live-tail selftests (= the inherited s53 HIGH item).
   e. #117 content-fingerprint tool exists nowhere; scratchpad/s54_v620/pool.py still
      enumerates two DEFF clusters (also inherited).
   ⇒ ESCALATION CANDIDATE at wrap: twice-carried instrument debt on the decision surface
   is no longer a debt list item, it is a standing misreading risk — Magnus's call.

3. v622 build lesson (routed to retro at wrap): the flags-off "identity by construction"
   claim was FALSE until the identity RUN caught a NameError swallowed by the run()
   exception wrapper (explicit import list in sk_roles, new flags not added). The
   import smoke test cannot see it. Rule candidate: any new sk_maps flag consumed in
   sk_roles gets a same-shell `sk_roles.<FLAG>` attribute assert (mkarm already does
   this for arms — the BASE tree needs it too), and flags-off identity is RUN, never
   asserted.

4. Inherited s54 residue (scratchpad/s54_wrap_debts.md): pool.py MAP fold · tape.sh case
   guard · submit_clean --restore-to · now.py last-10 label (pools unrated) · anat620
   zero-comparison blind alarm · fidtab schema · the inherited s53 HIGH batch
   (results.tsv schema, audit_trigger live-tail selftests, R2 ship-gate parsed SHIP_BAR).
