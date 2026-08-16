# s47 WRAP DEBTS (per Magnus's 2026-08-16 momentum rule: tooling fixes land at wrap)
Owed receipts included — answer each in the wrap coordination note.

1. (side lane, defer-tagged) BARS.tsv header: one line naming the combo-bar COST
   (true-55 coin flip; 53→98.13%, 55→50.00%, 56→14.76%, 57→1.79% — figures live in
   auto_gate.py:219-222 and are verified) so the bar registry shows the price, not
   just the bar. RECEIPT OWED: their s45 carry-forward correction ("unpriced" was
   false when written) — CONSUME at wrap.
2. (side lane, defer-tagged, carried from s45) prereg_check has no
   DEFENCE_ADMISSION_BAR / RMST / r300 rule; both test verdicts already routed
   (sealfloor6 PASS, sealrepair:31 FAIL — the incumbent's own prereg). Decide
   build-or-decline at wrap and say which.
3. (side lane, third instance today) grep -c exits 1 on zero matches — fires
   exactly when the answer is clean. Standardise the guard idiom (grep -c ... ;
   test on the COUNT, never on $?) wherever we write inline gates.
4. (mine) tests/test_instruments.py runner-context quirk: suite is GREEN via
   `.venv/bin/python tests/test_instruments.py` (157 OK) but 2 elo_logger
   announcement asserts fail under `python -m unittest tests.test_instruments....`
   — path/import-context difference, canonical runner is the file itself. Diagnose
   at wrap or file as instrument debt.
5. (mine, from SENTBAN verdict) registered mechanism metrics for #76
   (forward-sentinel builds/game, max-plants-on-one-tile) need an instrumented
   run before any higher-K SENTBAN arm — owed to whoever builds it.
6. (mine) H609-H628 h3/h4 block: 14 queued-never-started shards sitting ahead of
   any newly appended arm in corefill_work.txt (file-order hazard, bit twice in
   s46). ASKED Magnus whether to kill the block after he killed H601/602.
7. (from the ECOPAVR2 incident) auto_gate --apply REFUSES remote shards by
   design (orchestrate.sh cancel exists but needs kill->cancel->start over
   ssh). The trend floor is therefore MANUAL on 2 of 3 hosts — ECOPAVR2 sat
   at 48.40 prefix@1000 unkilled. Wants: a safe auto path (auto_gate writes a
   wanted-cancel file; orchestrator loop or human applies it), or at minimum
   a dashboard badge "BELOW FLOOR — needs manual cancel".
