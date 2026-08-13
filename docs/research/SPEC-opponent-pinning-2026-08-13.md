# STANDING PRACTICE SPEC — OPPONENT-SUBMISSION PINNING (`--match`)

**Written 2026-08-13T15:12:51Z (`date -u`) by research s36, on the builder's ask after they
and Magnus independently hit the flag mid-leg.**

## ⛔ FIRST, THE CORRECTION THAT MATTERS MORE THAN THE FLAG
**This was not a discovery. It was already documented, correctly and in full,
in `docs/fcode-cli.md:330-342` — committed `5353bd3`, 2026-08-09T07:05Z —
four days before the tri-arm design needed it**, including the exact
semantics: *"pass `--match <match-id>` to instead play against whichever
submission they had in a specific past match."*
**It appears in ZERO booted files** (`CLAUDE.md`, `PROGRAMME.md`, `QUEUE.md`,
all three `.claude/commands/*.md`: no hits). Meanwhile `CLAUDE.md` has carried
*"nothing pins or even reads THEIRS"* as a standing limitation, and this lane
spent today's O3 flag reasoning about an opponent-churn problem the CLI could
already solve. **This is the exact failure `CLAUDE.md` names about itself:
a fact recorded in a reference doc and contradicted by the always-loaded file
is a fact nobody has** — second confirmed instance (the first was
submit-auto-activates), and it cost a design amendment and a research flag.

## VERIFIED (by research, at the CLI, 2026-08-13T15:12:51Z)
`fcode match unrated --help` → `--match TEXT  Use opponent's submission from
this match ID`. API body carries `sourceMatchId` (`commands/test.py:13-42`).
**Not verified by me:** that a pinned fire actually reproduces the old build —
that is the builder's live use, and the decode check below is what proves it.

## ⭐ THE DESIGN RULE — PIN TREATMENT LEGS, NEVER PIN CALIBRATION PANELS
The two fixture types want OPPOSITE things and conflating them is the way this
capability gets misused:
* **TREATMENT LEGS (matched pairs: same opponent, same map, different arm) →
  PIN, ALWAYS.** The comparison is between OUR arms; any opponent variation is
  pure noise the design cannot absorb. Pin every arm to the control arm's
  match ids. **This repairs opponent churn completely** — the O3/LingLing40
  problem (8 versions in 4 hours) stops being a confound.
* **CALIBRATION PANELS (CAL-1/2/3: "where do we stand?") → DO NOT PIN.**
  The panel's whole rationale is RELEVANCE — what the ladder will actually
  pair us against. Pinning turns it into "our standing against a build the
  ladder no longer runs", which is precisely the staleness the CAL-3 band
  refresh existed to remove. **Churn is not noise here; it is the signal.**
* **Corollary for opponent PROFILING (`OPP-*` docs): pin.** A profile
  describes one build; pinning makes the profile's population match its claim,
  and re-profiling on a bump becomes a deliberate act rather than an accident.

## THE VERIFICATION IT UNLOCKS (research duty, from this leg on)
A pinned triple whose decoded `oppver` values DIFFER is an **instrument
alarm**, not a data point: either the pin did not take or our version decode is
wrong. **Report it as an alarm and stop reading that cell until resolved.**
`oppver` decode is thereby upgraded from observation to PIN VERIFICATION.

## FAILURE MODES TO CARRY
1. **A `--match` fire that ERRORS is not a pinned fire.** Log verbatim, abort
   the burst (builder's executor already does this); the fallback is the
   Amendment-2 down-weighting, never a silent unpinned substitute.
2. **The pinned build ages out of relevance.** A leg pinned to a morning build
   measures the morning. State the pin's age in the readout.
3. **Pinning does NOT pin OUR side** — `unrated` always plays our ACTIVE
   submission (`fcode-cli.md:344`). Arm identity still costs an activation.

## ROUTING
* This spec: research-owned, cited from the coordination tail.
* **`CLAUDE.md` line: RECOMMENDED TO MAGNUS, NOT WRITTEN BY ME.** That file's
  standing limitation sentence (*"nothing pins or even reads THEIRS"*) is now
  wrong in half and should be corrected — **but it is Magnus's file and a peer
  lane's request is not authorisation to edit it.** Proposed replacement text
  is in the coordination note beside this spec.
