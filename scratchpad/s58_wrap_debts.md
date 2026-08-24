# s58 wrap debts (builder) — tooling fixes go to the wrap (Magnus s47/s48 rule)
*(Game context: in-game Florent Code League.)*

1. **holder_watch — window-era monitoring question** (CORRECTED: the
   "blind since 08-22" claim was research's filtered-grep artifact, retracted
   06:28:37Z; the instrument is alive and caught the v192 incident flip live).
   The true residual: a 120s poller structurally cannot see sub-2-minute
   window flips (so it can neither log nor exclude them — e.g. a <2-min v211
   flip at 05:16 is invisible either way). At wrap: decide faster poll vs a
   different surface for window-era holder monitoring.
2. **now.py "last 10" pools unrated** — inherited from s57 HANDOVER header
   (wrap debt there too); rated-only differs.
3. **fanout.sh** still drops on retry exhaustion + no start-cell rotation
   (CLAUDE.md standing note) — only matters if the fanout pattern is revived.
4. **MAGNUS QUESTION (not tooling, parked here so the wrap names it):** ask
   x3r0 whether they fire a 5-team spot-check after shipping and whether they
   touched v211 at ~05:16Z on 2026-08-24 — the single answer that settles the
   unrated-burst mechanism (research's discriminator; full note in the tail).
5. **Iteration-12 probe trees + smoke dirs** under scratchpad/s58_it12/ —
   clean at wrap (probe copies carry stderr instrumentation; never submit).
6. **RETRO NOTE (process delta, pre-logged):** the final-hours slot guard v1
   was armed WITHOUT being driven to both verdicts (my own boot config's
   probe-the-guard rule) — it read the elo tape's match-counter column as the
   version and false-fired HOLDER CHANGED on its first row. v2 was driven to
   all 4 verdicts on synthetic lines before arming. Same-session violation of
   a booted rule; the false alarm was benign (v188 healthy, 1819 #22 at
   06:42Z) but the class is the s39 "the check ran and asserted nothing"
   family, inverted: a check that fires on everything asserts nothing either.

## WRAP DISPOSITION (s58 wrap, season end — D-7): items 1-3 and the ledger
## auto-row defect are EXPIRED-WITH-PLATFORM — documented, not built (fixing
## instruments for a dead league is waste; the class lessons live in the
## process deltas). Item 4 (x3r0 questions) stays open for Magnus as a
## curiosity. Item 5 (scratchpad hygiene): probe trees carry stderr
## instrumentation and were never submitted; left in place as part of the
## day's record.
