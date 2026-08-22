# s56 wrap debts (builder) — wrap-scoped per the momentum rule (Magnus s47/s48)

Game context: all items concern in-game Florent Code League tooling.

1. **h4-era tree collision (side-lane warning, s56):** `bots/_v623h4` (s44-era)
   coexists with `bots/_v623healweld`, and `_v624h4` awaits the next version
   number. Any tooling resolving "v623"/"v624" by glob can grab the wrong era;
   LINE_DIRS matches both. Decide rename vs quarantine for the h4 trees at wrap
   (a rename commit names the old term once for grep continuity).
2. **rdiff wrapper class:** my readout one-liner grepped "identical" and
   mislabeled 60/60 identical cells DIVERGE (rdiff's pass phrase is "NO
   behavioral divergence"). Consider a machine-readable exit code or `--quiet
   PASS/DIVERGE` line on tools/rdiff.py so wrappers can't misparse the prose.
3. **Fleet-health hook counts archiver wrapper+child as a duplicate** (pid
   19887 loop + transient 30-min child) — two peers flagged it as a defect in
   two sessions; teach the hook the loop/child pattern or it cries wolf every
   30 minutes.
4. **Inherited s55 debts stand:** `scratchpad/s55_wrap_debts.md` — incl. the
   weld-pattern AST sweep (#5) and the twice-carried audit_trigger/results.tsv
   decision-surface escalation (now three wrap cycles if not discharged here).
5. **Weld-sweep second shape (side-lane audit, s56):** the specced AST sweep
   covers multi-flag CONJUNCTIONS (`DEAD_FLAG and LIVE_FLAG`); the
   SK_CAGE_CEIL dynamic-accept block is a single-dead-flag-gated ENHANCEMENT
   (`if DEAD_FLAG:` guarding replacement logic) and escapes that pattern. Add
   the second shape: any `if <flag>:` block whose flag is permanently False
   and whose body carries measurement-bearing logic.
6. **Cross-host non-determinism (measured s56, POWERED-V624 dose spot):** the
   same trees+map+seed produce DIFFERENT games locally vs on the work servers
   (grid row outcomes differ on local re-run). Consequences to encode durably
   (side-lane ask): remote grids can never be spot-reproduced byte-for-byte;
   any registered check on a remote grid must name an instrument that exists
   ON that surface (TSVs only — no replays retained); local re-runs of grid
   cells are fresh same-cell samples, never reproductions. Candidate home:
   the remote_battery.py docstring + the builder-method doc.
7. **Registration-template fixes (from v625 + v627 readouts):** (a) every
   pooled dose metric states per-cell vs pooled explicitly (v625's ambiguity);
   (b) every rate/clock metric states its normalization (v627's tube-down
   clock was raw rounds — a longer game reads as a worse clock; normalize by
   post-first-death rounds or state why not); (c) operational primary is
   candidate−dup with its own interval (adopted mid-session, encode in the
   template).
