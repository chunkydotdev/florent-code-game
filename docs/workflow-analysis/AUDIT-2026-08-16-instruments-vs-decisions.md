# AUDIT 2026-08-16 — can the instruments support the decisions? (short-lived audit session, opus, read-only)

Triggered by `tools/audit_trigger.py` FIRING 2/6 at builder s46 boot (ship cadence
0.24/hr; 16 analysis docs / 1 decision row in 24h). Commissioned per the boot rule;
prior art: `docs/workflow-analysis/` 2026-08-08 (19%-power finding). The agent had
no stake in the queue. Relayed verbatim below by the builder; verification status
of each load-bearing claim is marked ⟦VERIFIED⟧ (builder re-checked against a
primary) or ⟦UNVERIFIED⟧ (agent's own read, not yet re-derived).

## HEADLINE
The 60±2 gate is statistically sound and strategically unreachable. Multiplicity
is a non-issue. The binding failure is not the gate — it is that 7 of 8 local
shards, including the priority-1 eco batch, ran at background QoS (nice=15,
pri=4) on the efficiency cores at ~1/40 of remote speed ⟦VERIFIED: ps shows seven
pri=4 python procs at ~16% CPU each⟧, while the answer to the priority-1 question
already existed on ws2, finished ⟦VERIFIED: ECOSIPHR COMPLETE 08:00:08Z, n=5,400,
48.83% T-share, 0 NOWINNER, NULLHOST cert 52.00% n=400⟧.

## Q1 — POWER OF THE 60±2 GATE
* Half-width at p=.60, n=5,408, local DEFF 0.98: ±1.293pp → the ±2pp clause is
  slack; the gate reduces to "observed ≥ 60.0". CI-lo ≥58 binds at point ≥59.29.
* False qualification impossible at this n (true 55.24 → P(reads ≥60) = 5.8e-13).
* 50% power at its own threshold (true 60.00 → P(qualify)=0.500; 80% needs true
  60.55). No re-test rule is registered anywhere.
* Reachability off the 27-arm board: mean 53.02, true between-arm sd 1.507pp.
  A true-60 arm is a +4.64σ draw ≈ 1 in 560,000 arms. True-57 ≈ 1 in 244.
* Board max flat for 16.5h / 17 arms (55.24 MIX280mix4; best since 55.20).
  Composition beats best solo by +1.30pp once, then saturates.
* HANDOVER.md called the seat seam "biggest lead toward the 60-bar" while the
  research doc it summarises caps it at ~58.4 (coordination.md:60590). ⟦UNVERIFIED
  line refs, claim consistent with research's relay⟧
* Gate 2 (head-to-head vs holder) distance UNMEASURED: only read is the
  fixture-broken V140VS152 shard, v152 = 58.26% of decided, n=230, ±6.37pp. If
  the point survives, an arm at exactly 60 vs v140 is at PARITY with the holder.
  Re-run queued on ws2 ⟦builder action, done 07:55Z⟧.

## Q2 — SELECTION / MULTIPLICITY
* At per-arm measurement sd 0.672pp, P(any of 1,000 true-55.24 arms reads ≥60)
  = 5.8e-10 → the first observed 60 will not be a max-over-many artefact.
* Registered winner's curse (+1.7pp in HANDOVER) is overstated ~4.7x: shrinkage
  fit gives selection bias 0.37pp; the 1.74 is max-minus-baseline, mostly signal.
* No confirmation rule / fresh-seed re-test exists in any tool (see Q5-1).

## Q3 — THROUGHPUT vs DECISION RATE
* The analysis-outpacing-decisions trip is STRUCTURAL: the local fixture was
  throttled to ~1.08 core-equivalents across 7 shards. `nice` set in no checked-in
  script — inherited from how the fill chain was launched. ⟦VERIFIED⟧
* Decisive control: ECOSIPH local 140 rows @ 92/h, 8.05% NOWINNER vs ws2 ECOSIPHR
  5,400 @ 3,727/h, 0.00% NOWINNER, same trees, host-keyed seeds. ⟦VERIFIED⟧
* NOWINNER is a throttling artefact: all 7 throttled shards 1.5–8.1%; every
  full-speed shard 0.00%. The 1%-abort check runs at launch only, so none will
  ever trip it. Scheduling rule confirmed: CPU-sensitive fixtures measure on
  uncontended allocation only.
* Fleet ceiling ≈ 52 full-n arms/day (can search a true-57 in ~5 days; cannot
  search a true-60 ≈ 560k arms).
* ws1 sat idle 9.85h while fleet_dispatch printed worker_alive=True — another
  monitor that cannot report blindness. ⟦UNVERIFIED⟧
* Queue defensible range 24–55 unblocked (31 carry legacy marker words with no
  STATUS: token). The queue is not starving the fixture; the fixture starves the queue.

## Q4 — LEG-fieldcal
* Prereg's own numbers reproduced digit-for-digit: primary has ~7–10% power
  against its target (P(9/10)=7.0%/9.9%); pooled MDE ≈ 11pp / 14.4 rounds vs
  local effects 3.7pp / 6.8 rounds. It can resolve only a SIGN REVERSAL — a
  correctly-shaped exclusion, and the only product to expect. On schedule at the
  platform ceiling (15.5 accepts/h); pooling point ~10.8h out from 08:02Z.

## Q5 — INSTRUMENTS THAT CANNOT PRODUCE THE OTHER VERDICT
1. The 60±2 rule exists in PROGRAMME.md and in no tool. gate.py parses and never
   reads it; slot_rule/slot_sprt implement the older Elo-drawdown rule.
   Adjudication of "cleared 60" is by hand against prose.
2. overnight_read C2 band hardcodes 0.25 (never p(1−p)); its inputs are chosen
   known-negatives → cannot fail. C1 recorded as never having executed.
3. overnight_read prints P(≥1 spurious OUTSIDE)=1.00 across 183 arms and adjusts
   no threshold.
4. gate.py enforces 1 of 23 PROGRAMME fields (LINE_DIRS) and that field is stale:
   patterns stop at v199 while the incumbent is _v223sealrepair ⟦VERIFIED:
   fnmatch — _v223sealrepair, _v242bodyaware, _v315siphit all FAIL the line
   check; 26/27 battery invocations passed --off-programme⟧. The s31 defect
   class recurring: a guard that refuses everything gets routed around.
5. auto_gate is the healthy one (selftest PASS, both verdicts live) — but 224 of
   228 registered bars are the identical 51.33-ge futility band, and V140VS152's
   deliberate 100.0-le ablation bar is silently dropped by the [30,70] range
   check, so it ran under the house trend floor instead.
6. Two coordination entries carry hand-written FUTURE timestamps (09:1x/09:4xZ
   against a 05:59Z commit) — fifth recurrence of the timestamp failure.
7. Genuinely sound: RMST₃₀₀ (four ground-truth controls right to 2dp; can fail
   and does). Residual risk: 85 of 150 "flat" verdicts are unrestated
   fail-to-excludes; BARS.tsv has no MDE column.

## RECOMMENDATIONS (agent's ranking; builder disposition in brackets)
1. Un-nice the fill chain, cancel the redundant local eco twins, read the ws2
   replications, route freed slots to SEATSPAWN/SEATFULL. [TAKEN 08:12Z — seven
   shards cancelled, chain relaunched at normal QoS.]
2. Take the 60-bar reachability number to Magnus; V140VS152 first (gate-2
   distance unmeasured). [V140VS152 re-queued on ws2 07:55Z; reachability
   question put to Magnus in-session 08:1xZ.]
3. Give the 60 rule a body (BARS.tsv bar + registered fresh-seed confirmation +
   MDE column) or stop calling it a gate; repair/delete overnight_read C1/C2;
   add a verdict column to gate_invocations.tsv. [QUEUED — builder items.]

Not answerable from the repo: QUEUE.md rows added per day (no per-row date);
why nice was 15 (inherited from launch environment, set in no script).
