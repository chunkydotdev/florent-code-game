# s53 WRAP DEBTS — research lane (wrap-batch per Magnus's rule, none executed mid-session)

## RD-s53-1 — audit_trigger ship-cadence cell: subject filter (spec commit's author clock 12:58:35Z is the stamp; side-lane confirmed the hazard; hand-rounded "13:0x" stamp corrected per timestamps rule at 12:59:47Z)
INCIDENT: the s53 boot trip counted 8 activations/24h as "our" ship cadence; side-lane subject check
(commit 111bbbb59) attributed only 2 to our line (v174, v177 ships), 5 to x3r0's slot actions
(incl. their v175 ship + self-rollback to v174 — ours-by-VERSION, theirs-by-HAND), 1 unattributed
(v172, no version_trees.tsv row). The s43 class exactly: a true reading of the wrong subject.
SPEC (one line of behaviour, D29-proofed):
- the cadence cell counts only activations whose version maps to OUR tree in version_trees.tsv;
- unattributed versions (no ledger row) emit their OWN alarm line — never silently dropped, never
  counted in either bucket (a sparse column must fail LOUD: v172 and v176 currently have no ledger
  rows, so the filter must alarm on the gap, not return a clean zero);
- attribution by HAND where known (an x3r0 rollback to OUR version number is not our activation).
OWNER: research (cell owner per side-lane assignment). EXECUTE: at wrap or Magnus-called fix batch,
with a both-ways drive (a window containing a known x3r0-only churn day must NOT trip; a window
containing our 2-ship day must count exactly 2).

## RD-s53-2 — audit_trigger delegation cell + selftest rule (from the s53 audit session's report, ack'd 2026-08-21T13:12:43Z)
- delegation cell is DEAD (parses a header format the coordination tail no longer uses) — fix or retire;
- standing rule from the audit: audit_trigger selftests must run against LIVE tail slices, not frozen
  fixtures (a selftest on a frozen fixture validates the parser of a format that can silently die).
OWNER: research (cell owner). Execute at wrap batch with RD-s53-1, both-ways drives.
