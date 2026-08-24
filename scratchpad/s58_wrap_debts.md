# s58 wrap debts (builder) — tooling fixes go to the wrap (Magnus s47/s48 rule)
*(Game context: in-game Florent Code League.)*

1. **holder_watch is BLIND** (research wire cut, 2026-08-24 ~06:2xZ): alive in
   ps, 120s poll, but has logged NOTHING since 2026-08-22 17:04 across 20+
   overnight window flips (v191–v211 activations + restores all invisible to
   it). The s43 class: an alarm that cannot tell it is blind. Fix at wrap:
   freshness self-report + a forced-fire test against a known flip from the
   window artifacts.
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
