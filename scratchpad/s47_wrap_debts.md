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
8. (side lane, defer-tagged) TREND_FLOOR header: add the EITHER-look line —
   true-52 kills 63.6% across both marks (their nested sim, corr 0.609), not
   the single-look 50.0 "coin flip"; their 55.2 recompute is 2.09 vs my 2.4
   (mine conservative, keep). One header line.
9. (side lane, defer-tagged) HOST-CENSORING: local arms are floor-cancelled
   early, remote arms run to full n — whether a board row has a full readout
   now correlates with HOST, not arm quality. Mechanism verified
   (auto_gate.py:1321,1341), magnitude unmeasured. Attaches to debt 7; the
   likely answer is "read the board as half-censored", not "build remote
   cancel".
10. tools/corpus/replay_autopsy.py has no --help guard (tracebacks on
    FileNotFoundError '--help') — tools/corpus/ appears outside the
    test_instruments help-contract sweep; extend the sweep or guard the file.
11. (research AMENDMENT2 §9, defer-unless-leg-resumes) fieldcal_scheduler.sh:167
    --limit 60 read horizon: the −40 halt's platform fallback will cross it
    (~57 projected matches in the leg era), and :555 judges blindness on AGE
    ALONE — a fresh-but-truncated read prints blind=0 with a permissively
    SMALL loss sum (drops oldest rows). Fix + a --selftest cell that returns
    the other verdict, BEFORE any leg resume (then it is loop-breaking and
    jumps the wrap queue); trigger registered: before the era hits 50 matches.
12. (side lane, defer-tagged, latent) PARSER DIVERGENCE on PROGRAMME.md fields:
    slot_rule.stop_loss_active returns on the FIRST matching line (indented or
    not); gate.py takes the LAST indented one. Agree today (field appears once);
    a prose copy below the block would give slot_rule 'off' (safe) / gate 'on'
    (wrong). Live decision-maker holds the safe value, so it fails in the right
    direction — but that file has produced exactly this failure once (s31).
    Fix: one shared parse (slot_rule adopting last-indented-wins, or gate
    exporting its parser); driven-both-ways test on a constructed divergence.
13. (research free finding, builder ticket) valkyrie build-legality: 31 builds
    across 76 valkyrie games landed on tiles doctrine.py labels WALL,
    concentrated at (6,14) and (23,14); midgard/ragnarok/glacierkeep/
    drakkarfjord clean at 0. Our terrain table is wrong on a live pool map —
    planning paths avoid legal tiles (and possibly vice versa). Fix the table
    from decoded terrain + a both-ways check per map.

## LIVE TICKLER (not wrap debt — session-active)
T1. ~16:15Z: G413g4 (ws1, starts after G412g4) crosses n=1000 — compute its
    prefix from the mirror; if <52.0, run the kill/cancel/start sequence on
    ws1 (4,400 games recoverable at that point vs ~minutes for G412 now —
    the side lane's dry-run finding, marginal-cost-corrected). ECOSCK4R2
    completes ~15:55Z: type the eco-batch replication verdict from its
    full-n tape (REFUTED-class expected at prefix 46.40).
14. (wrap task) Playbook update — add the self-claim staleness rule in
    RESEARCH'S sharpened form: "Every self-claim names its ourver span. A
    claim whose span crosses more than one incumbent is PRESUMED STALE UNTIL
    SPLIT" — bite on the TENSE (present-tensing a pooled claim is the step
    where damage happens). ⛔ ATTRIBUTION: the stock-vs-flow worked example
    is the SIDE LANE's (their 7,950/440 self-correction), NOT research's —
    I misattributed it in a message; the playbook must credit the side lane
    or a successor reads the wrong transcript. Reproduce-the-number-FIRST
    ordering (era-split method) also goes in, credited to the resolution
    exchange.
15. (side lane) FLOOR-STOP ESTIMATES ARE SELECTED-PESSIMISTIC — arithmetic,
    not empirical: the floor stops on a low prefix draw, so conditional on
    stopping, true share is higher (measured on the only 2 observable cases:
    +2.82 and +1.33, mean +2.08pp). fired_on is the WORST number to reuse
    for combination mining yet the ledger foregrounds it. Wrap fix: one
    header line in results.tsv/auto_gate cancellation text — "prefix-stopped
    estimates are selected low; for combination mining use the full-tape
    share, expect ~+2pp regression." Also carry their correction: the
    retrospective-threshold note's "no live arm affected" had false evidence
    (SEALPECK was already dead 5pp below when written) though the conclusion
    survives (46.90 dies under either floor).
16. (side lane, defer) V140VS152 BARS row carries bar 100.0 — outside the
    plausible [30,70] band; the guard correctly REFUSES it so the shard has
    no effective bar. Fix the row or record why it is right (it's a
    head-to-head screen row, likely a sentinel value someone typed — check
    provenance before editing).
