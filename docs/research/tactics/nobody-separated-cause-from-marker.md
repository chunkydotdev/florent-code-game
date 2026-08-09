---
tactic: Distinguishing "we engaged early because we were winning" from "engaging early made us win"
source: https://battlecode.org/past (all 22 official postmortems, 2019-2026, machine-searched)
origin: Battlecode 2019-2026 — negative result across the entire published corpus
evidence: documented (the absence is measured, not assumed)
transfers: no
---

## WHAT IT IS

**Nobody did this.** Across all 22 official Battlecode postmortems from 2019 to 2026 —
downloaded, converted, whitespace-flattened and grepped case-insensitively — the following
terms appear **zero times in every document**:

| term | occurrences across 22 postmortems |
| --- | ---: |
| `correlat` | **0** |
| `causal` | **0** |
| `confound` | **0** |
| `ablat` | **0** |
| `regression` | **0** |
| `hypothes` | **0** |
| `sample size` | **0** |
| `noise` | **0** |
| `misleading` | **0** |
| `coincidence` | **0** |
| `p-value` | **0** |
| `random seed` | **0** |
| `number of games` | **0** |

`significan` appears in 16 documents and `luck` in 12, but every inspected occurrence is
colloquial (*"significantly better"*, *"getting lucky on the maps"*) — not a statement about
inference. `variance` appears twice, both times about **strategy variance** (the Kragle on
their own opening producing *"high variance"* outcomes), never about measurement error.

The field's causal instruments, in full, are three:

1. **Self-play A/B against your own past versions** (see
   `self-play-ab-has-the-wrong-population.md`).
2. **Ladder rating movement after a change** — e.g. cout for clout: *"This improved our
   rating a whopping 130 points (from 1720 to 1850)"*, an uncontrolled before/after on a
   moving field.
3. **Watching the replay.**

No source in the corpus separates *"the winning games are the ones where we engaged early"*
from *"engaging early is what won them"*. The question is not answered badly; it is **not
asked**.

## WHY IT MIGHT TRANSFER

It does not transfer as a tactic. It transfers as a **bound on what the library can supply**.

Our own core-kill incidence cut states its position honestly: `US_shot_w50` is *"a marker,
not a proven dial"*, and *"Only an arena A/B can turn this into a dial"*. This sweep was sent
to find out whether any comparable league had already done the separation and could hand us
the answer. **They have not, and there is nothing to import.** The arena leg is the only
instrument, and that is now a sourced conclusion rather than a default.

Two second-order consequences worth carrying:

- **Every "what converted a rush" finding in this library — sweep 14's five preconditions
  included — rests on the same evidence class our cut is trying to escape.** Winners
  describing their own winning games is exactly the outcome-conditioned view. The sourcing
  is real; the inference layer under it is not stronger than ours, and in the specific
  respect of stratification and multiplicity it is considerably weaker.
- **Our own cut is, as far as this sweep can establish, methodologically ahead of the
  published field on this question** — landmark at r50 with zero censoring, four
  stratifications, a pre-registered K=64 Holm family, and two controls. That is not a reason
  to trust it more than it claims; it is a reason to stop expecting the library to
  adjudicate it.

## WHAT WOULD KILL IT

- **Non-Battlecode leagues were searched separately and are covered in the sweep summary's
  non-coverage section; this file's census is Battlecode only.** A negative from 22
  documents in one league is not a negative for all of competitive programming-game writing.
- **Absence of the vocabulary is not proof of absence of the practice.** A team could have
  run a stratified comparison and described it in plain words. The inspected passages do not
  support that reading, but the census cannot exclude it.
- **Postmortems are marketing as well as documentation.** Teams write up what worked. A
  team that discovered their headline tactic was a marker rather than a cause has a weak
  incentive to publish it.

## BUILDER HOOK

None, and that is the point. This file exists so that the next session does not re-sweep the
field looking for a cause/marker separation that is not there. The instrument is the arena:
per `PROGRAMME.md`, LOKI-N against LOKI-(N−1) on `core_kill_share`, with the contact trigger
as the only varied term.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/past
- https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
