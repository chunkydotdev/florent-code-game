# SPEC — ANTI-SYCOPHANCY COVERAGE: THE CLAUSE EXISTS IN THREE FILES, ALL OF THEM UNLOADED

**Side lane, s42, 2026-08-14 20:5xZ.** Written in answer to a direct question from
Magnus: *"does our claude.md state anti-psychophantic behaviour for all our agents?"*

**Version tag:** repo HEAD `b8de3b77`; incumbent `bots/_v223sealrepair` (v140);
three lanes live (builder `-75`, research `-b2` s43, side lane this session).

**Write-surface note:** `CLAUDE.md` and `.claude/commands/*.md` are **outside this
lane's write surface** and are not edited here. This document is the SPEC and the
exact insertion text; the edit belongs to the builder or to Magnus.

---

## 1. THE ANSWER: NO. AND THE SHAPE OF THE GAP IS THIS REPO'S OWN RECORDED FAILURE.

| surface | auto-loaded? | anti-sycophancy clause |
|---|---|---|
| `CLAUDE.md` (project) | **yes** | **NONE** |
| `~/.claude/CLAUDE.md` (global) | **yes** | **NONE** |
| `PROGRAMME.md` | via lane boot steps | **NONE** |
| `.claude/commands/builder.md:73` | **NO** | **yes — the strongest, and the only Magnus-facing one** |
| `.claude/commands/research.md:45` | **NO** | yes — builder-facing |
| `.claude/commands/sidelane.md:26` | **NO** | weakest; does not use the word |

**Derived, not relayed** — every cell above was grepped in this session against the
files themselves.

**THE NEGATIVE CONTROL WAS RUN BEFORE THE ABSENCE WAS PUBLISHED**, because "absent
from my grep" and "absent from the repo" are the two readings an empty result admits
and this lane's characteristic failure is publishing the first as the second.
Terms swept across both `CLAUDE.md` files: `sycophan*`, `flatter*`, `courtesy`,
`adversarial`, `disagree*`, `defer`, `echo`, `praise`, `oversell`, `overstate`,
`hold request`, `push back`, `yes-man`, `say so`, `honest`, `flag back`.
**Hits in project `CLAUDE.md`: five, all unrelated** — `:645`/`:649` `FLATTERING` is
the DEFF scope clause about *statistical* error direction; `:243` is
numbers-carry-subjects; `:288` is nulls-are-iterations; `:415` is *"the only honest
fixture"*. **Hits in the global file: zero on every term.**

## 2. THE SUBAGENT HALF WAS AN INFERENCE. IT IS NOW A MEASUREMENT.

**Pre-registered three-outcome probe with a SKIP for non-evidence**, copying the
`_probe_nearby_default` design the drift watch records as the template: a probe that
can only confirm has not been seen to check.

A `sonnet` subagent was spawned with no repo access instruction and asked to report
presence/absence of four exact strings **from its own context only**, plus two
positive controls. **Pre-committed reading, written before the result:** if C and D
come back ABSENT the agent has no project instructions at all and **the probe is
UNINFORMATIVE and must say so** rather than return a clean result.

| string | source file | result |
|---|---|---|
| A. *"Agreement is a measurement outcome, not a courtesy"* | charters only | **ABSENT** |
| B. *"no sycophancy"* | charters only | **ABSENT** |
| C. *"Numbers carry subjects"* | project `CLAUDE.md` | **PRESENT** (quoted verbatim) |
| D. *"Loki is the ultimate trickster"* | project `CLAUDE.md` | **PRESENT** (quoted verbatim) |

**Controls pass ⇒ the probe is informative.** Asked directly whether it held *any*
instruction against sycophancy, against default deference, or to state disagreement,
it returned **NONE**. Files it could enumerate in its own context: project
`CLAUDE.md`, global `CLAUDE.md`, `MEMORY.md`. **No `.claude/commands/*.md`.**

⇒ **MEASURED, not inferred: a subagent inherits both `CLAUDE.md` files and the
memory index, and receives zero stance instruction.**

*(Recorded as a datum, not a finding, n=1: offered the closest adjacent item — the
`run-with-recommendations` memory line — the probe declined to count it, unprompted,
as "not a match for what was asked." An instrument given a leading frame that still
refuses the near-miss is behaving correctly.)*

## 3. WHY THIS IS A REAL EXPOSURE AND NOT A TIDINESS ITEM

1. **The instruction is present exactly where a human is reading the transcript and
   absent exactly where nobody is.** All three lanes spawn subagents constantly and
   under standing permission (`CLAUDE.md:211-214`). That bullet mandates the MODEL
   TIER on every `Agent` call and says nothing about stance.
2. **A subagent's product arrives as a RELAY** — this repo's most-measured error
   channel (s40's CAL-8 chain: a relayed figure entering a prescription and
   hardening into a false ground in another lane's commit).
3. **Two of three lanes have nothing written about disagreeing with Magnus.** Only
   `builder.md` carries it: *"When Magnus's or research's preferred direction
   disagrees with the tape, say so as evidence plus a hold request — a gate that
   would pass because passing is wanted is not a gate."* Research's clause is
   builder-facing. The side lane's does not use the word at all.
4. **Our own `SessionStart` hook states the mechanism verbatim:** *"the charter,
   hard limits and boot sequence live in `.claude/commands/` and are NOT
   auto-loaded."*

**THIS IS THE SHAPE `CLAUDE.md` NAMES TWICE ABOUT ITSELF** — *a fact recorded in a
reference nobody boots and contradicted by the always-loaded file is a fact nobody
has* — and the s29 retro's *a rule promoted into a file nobody opens*, **which is the
routing rule this lane wrote.** Promoter's-first-use, at the level of the repo.

## 4. THE FIX — EXACT INSERTION TEXT, SO NOBODY HAS TO INVENT WORDING

### 4a. Into project `CLAUDE.md`, in the "Team standing practices" block

> - **NO SYCOPHANCY — THIS BINDS EVERY LANE AND EVERY SUBAGENT.** Agreement is a
>   measurement outcome, not a courtesy. Praise is not a coordination signal;
>   measurements are. A relayed number is a claim until you have re-derived it from
>   the primary, whoever relayed it. **When Magnus's stated direction, another
>   lane's preferred reading, or your own live hypothesis disagrees with the
>   measurement, say so — as evidence plus a hold request, never as compliance and
>   never as a veto.** A gate that would pass because passing is wanted is not a
>   gate. Never oversell your own result: a claim carries exactly what its intervals
>   support. **Amend your own published work the moment you find it overstated, and
>   say that you did.** Deferring by default destroys the independent verification
>   that is the whole value of having more than one arm — it fails in exactly the
>   same way as ignoring a peer, and it is harder to see.

### 4b. Appended to the existing `CLAUDE.md` "Use subagents" bullet

> **A subagent inherits this file and NOT the lane charters (measured 2026-08-14 by
> probe, positive controls passing), so the stance above is the only version it
> gets. Every `Agent` brief states the deliverable AND the standard: report the
> number you measured, name what you did not check, and return a null or a refusal
> rather than a plausible answer. An agent that cannot verify something says so.**

### 4c. Do NOT remove the three charter clauses

They are lane-specific and sharper than the general one (the builder's covers the
verdict-holder's asymmetry; research's covers the check-arm's). **The general clause
is a FLOOR, not a replacement.** ⚠ And the side lane's clause should gain the
Magnus-facing sentence it currently lacks — that omission is in this document's
author's own charter.

## 5. HOW TO AUDIT THAT THE FIX LANDED — a check with a hard bound (D31)

The failure mode to defend against is the one this whole document is about: the
clause being edited into a file that is not loaded. **So the check is not a grep of
the repo — it is a probe of a live agent's context**, which is the only surface where
the property is true or false.

    Spawn one throwaway subagent. Ask it to report PRESENT/ABSENT on
    "Agreement is a measurement outcome, not a courtesy" plus ONE known
    CLAUDE.md-only positive control. Required reading:
      controls PRESENT + clause PRESENT -> fix landed
      controls PRESENT + clause ABSENT  -> fix did NOT land (this is today's state)
      controls ABSENT                   -> UNINFORMATIVE, re-run; report nothing

**The controls are what make an ABSENT mean something.** Without them a subagent with
no instructions at all returns the same ABSENT as a subagent whose file lacks the
clause — the byte-identical healthy/blind line this repo has paid for twice.

## 6. ROUTING

* **Owner of the edit:** builder (`tools/` and repo-wide writes) or Magnus directly.
  **Not this lane.**
* **Magnus's call is wanted on 4a's WORDING, not on whether to do it** — it is the
  always-loaded team file and the clause governs how every agent talks to him.
* **Verified against:** the six-surface grep above with its negative control; the
  live subagent probe with two passing positive controls; `.claude/settings.json`'s
  SessionStart hook text. **No figure in this document was relayed.**
