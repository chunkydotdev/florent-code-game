# s48 WRAP DEBT LIST (tooling fixes deferred to wrap per Magnus's momentum rule, 2026-08-16)

1. **now.py: ADD A RETRY, do NOT relax the gate.** now.py exits 2/BLIND on the
   platform's PARTIAL response state (rating+rank present, no active_submission)
   while raw `fcode status` text sometimes carries the full block in the same
   second. The flap is sub-second (side lane s48: 5 samples in 2 s, 1 FULL), so
   ONE retry converts most BLINDs into reads. ⛔ The active_submission gate is
   CORRECT and its selftest asserts it — in PARTIAL, now.py is the only
   instrument that can tell FULL from PARTIAL; a text reader grepping `Rating:`
   cannot. Retry, don't relax. (Side lane s48 04:2xZ, consumed.)

2. ✅ **FIXED INLINE s48 ~05:0xZ under the loop carve-out** (side lane re-tagged
   DEFER→NOW when the shredder leg made a submit today plausible; a prototype
   leg IS the loop). `_restore_verdict` pure function per ship_ledger:567;
   loud exit-2 unknown branch; `--selftest-holder-guard` drives all 6 states;
   mutation-tested (broken guard → selftest exits 1). Original entry kept
   below for the record. ~~submit_clean.py: fail CLOSED on unknown holder.~~ `_holder()` returns None
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

9. **Mixed provenance in `scratchpad/overnight-remote/<host>/`** — heartbeat/
   tsv/COMPLETE files are PULLED (fresh) but `worklist.txt` there is a
   PUSH-TIME artifact that goes stale on regeneration; a reader pairing fresh
   heartbeats with the stale worklist concludes falsely about what runs.
   Side lane nearly flagged a live defect off it (04:4xZ). Fix: write the
   regenerated worklist into the mirror on push so the directory tells one
   story. (Side lane s48.)

10. **auto_gate_cancelled.tsv: add a control/era COLUMN to the writer**
    (auto_gate.py) so every future cancellation row names its control —
    a row cannot currently distinguish "failed vs the weak baseline" from
    "failed vs the champion", and the strict regime will mint many of the
    latter into a pool marketed for reuse. The expiring half (the era
    boundary) is DONE — written as a # comment into the ledger at s48
    (readers verified comment-tolerant: auto_gate.py:298,376,454). The
    column is the durable fix. ⚠ NEVER INDENT a comment in that file —
    reader at :376 has no lstrip and would read an indented comment as data
    (side lane drive). Ledger verified append-only (:958/:971 "a"-mode,
    truncate at :954 guarded by not-exists), so the positional boundary
    cannot drift. (Side lane s48.)

11. ⚠ SCOPE CORRECTED by the SEALSENT prereg agent (05:2xZ, reproduced from
    overnight.sh:99-101): LOCAL tapes DO get `# FIXTURE ... start=` as their
    FIRST LINE, written before the first game — the side lane's "does not
    exist" was true of REMOTE tapes (0 of 84) and the heartbeat (overwritten),
    and 131 of 232 local tapes lack it only because they predate the stamp.
    The correct boilerplate: PRIMARY = the local FIXTURE stamp where present;
    BACKSTOP = first completed row / serial-ordering bound (remote + legacy).
    The SEALSENT preregs registered exactly that form. Original entry below
    kept for history. **Prereg obligations boilerplate: fix the two-clock
    second-clock sentence** —
    the "shard tape's `# FIXTURE start=` stamp (overnight.sh:99)" method is NOT
    executable: remote tapes carry no FIXTURE line (0 of 84), and the heartbeat
    START is overwritten by the first progress update (`>` not `>>`). The
    executable substitutes: (a) first completed row (conservative — true start
    earlier, can only overstate the gap), or (b) serial-ordering bound off the
    preceding shard's COMPLETE. Same class as the LOKI-14 stdout lesson. Until
    the doc is fixed, every s48 prereg brief I write carries the corrected
    sentence inline. (Side lane s48, KLADLADDER certification.)

12. **league_matches.tsv tail is PARTIAL, not lagged (research, verified vs
    live pull)** — last 4 slots ~25% complete (10/11/11/7 vs ~41 steady),
    all four of our own 03:12-04:12 rated matches missing; freshness and
    completeness are different properties and only one is measured. TWO
    HALVES: (a) tool fix — target_value.py (:489-491) prints newest-row age;
    add rows-in-newest-N-slots vs trailing median beside it (research's dated
    spec, coordination 05:02:11Z); (b) INVESTIGATE the archiver's miss —
    likely the platform flap; check whether later passes backfill the
    03:12-04:12 window, else re-pull by hand. STANDING until fixed: an
    absence in the last ~90 min of league_matches.tsv is NOT evidence.

13. **unrated_run.sh:369 — guards that cannot fail when VER==MAIN** — with
    our own holder as the arm, `activate 155` on an already-active slot makes
    both holder guards (:367,:372) unfalsifiable. Benign but must be NAMED in
    the lock commit of any leg that runs with the holder as an arm. (Research
    s48, Clankers draft agent.)

14. **CROSS-LANE CATCH: research's s47 "three-valued owner predicate" for
    audit_trigger NEVER LANDED** — deferred at coordination.md:67177 ("my
    audit_trigger three-valued owner predicate is DEFERRED TO WRAP", research
    s47) and absent from every debt list since; side lane's landing-check
    found 2 of 3 s47 deferrals landed and this is the third. Design is
    research's (side lane's original three-valued spec at coordination:66810);
    pinned HERE so it stops falling through — route back to research at their
    next wrap, or build it at mine if they're down. (Side lane s48 Q.)

15. **move_miner ranking inverted vs study value** — coverage resets on THEIR
    version bump, never on OURS; our faster churn makes "unstudied on their
    current version" accumulate fastest for stable-version opponents we played
    heavily in the PAST (top-3 candidates: two with zero modern games, all
    three outside the band; the learnable three ranked 4-6). A THEM-liveness
    check passes all eight — the staleness is on OUR side of the pairing.
    Fix spec = research's coordination note ~05:2xZ (our-version coverage
    term, payout term, our-side pairing recency, print-what-was-suppressed).
    My tool; research manually gating meanwhile. (Research s48.)
    ⛔ ADDENDUM (research, ~05:3xZ): SECOND DEFECT, compounds the first —
    "their current version" is inferred from OUR tape, so it freezes at our
    last pairing (named lingling v61; they run v66 since 21:52Z). Fix
    addendum: read their current version from league_matches (league-wide),
    never ladder_games (our pairings), and PRINT BOTH ("their current vN;
    our newest games vs vM") — the gap IS the staleness signal. Both defects
    worsen together for the same candidates.

16. **ADOPTED, not debt: tools/cluster_ci.py is the interval instrument** —
    research built it (side lane mutation-tested); every measurement brief I
    write now points agents at it instead of restating the DEFF/exclusion
    rules in prose. Note its <30-cluster NO-VERDICT regime is deliberate.

17. **overnight.sh:157 scorer substring hazard** — winner matched by
    `*"$B"*` substring on the treatment basename with control as the ELSE:
    if TREAT is a proper substring of CTRL, every control win scores as
    treatment (silent one-directional inflation). 36 ordered hazard pairs
    exist in bots/ (the `_f`/`_off`/`ON` ablation convention creates exactly
    this shape); side lane's historical sweep: 0 of 101 FIXTURE-headed local
    tapes ran a hazardous pairing (remote tapes UNCHECKED — no headers).
    FIX SHAPE (theirs, adopted): match on exact token OR resolve against
    BOTH names and REFUSE when both match — the refusal also retires the
    same-path null case the ws1 worklist hit today. ⛔ Until fixed: no shard
    may pair a tree with its own ablation-suffixed sibling (current planned
    pairings all safe — everything runs vs _v468kladturbo; A-vs-A-nofund
    contrasts are computed BETWEEN shards, never as a pairing). (Side lane
    s48, DEFER.)

18. **`tools/turbo_identity.py` DOES NOT EXIST — a doc cites a guard nobody
    has.** bots/_v468kladturbo/eco.py:44 AND the eco study cite it as the
    seam guard for the hand-merged TURBO×BODYAWARE block; it is not in this
    checkout and never was. The eco-trio build covered the seam with a
    strictly stronger instrument (replay-SHA flag-off equivalence with
    positive controls, NOISE_ON=False + --tle 0 — banked as
    scratchpad/s48_flagoff.sh). Fix: either build turbo_identity as a thin
    wrapper over the flagoff harness or edit the two citations to point at
    the harness. Same class as the CLAUDE.md fact-nobody-has lesson. (Eco
    build agent s48.)

19. **corefill.sh:310 shell error on the empty-worklist path** — after the s48
   re-pin, the runner printed "COREFILL done." then
   `tools/corefill.sh:310: command not found: SH:-` / `= not found` (looks like
   a `${SH:-...}` parsed under the wrong shell). Loop-relevant only if it
   prevents relaunch when real work arrives — VERIFY when the ladder-no-cap
   shard is queued; fix at wrap if benign.
