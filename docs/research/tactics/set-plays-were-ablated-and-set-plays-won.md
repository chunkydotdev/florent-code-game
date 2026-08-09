---
tactic: (C) THE SURPRISE — the planner-versus-its-own-ablation comparison the brief expected not to exist DOES exist, it is 27 years old, it is in RoboCup, and the stored multi-step plan won on its own leg
source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
origin: RoboCup Simulation League — Stone & Veloso, CMUnited-97; *Artificial Intelligence* 110(2):241-273, June 1999
evidence: documented
transfers: partial
---

## WHAT IT IS

**Sweep 15 established, and this library has repeated since, that competitive game leagues
essentially never separate cause from marker.** That is true of the *game leagues*. It is not
true of RoboCup, which this library had never swept, and the omission cost us a result.

Stone & Veloso built a soccer team with three additions — flexible positioning within roles,
**set-plays** (their pre-stored multi-step multi-agent plans), and changeable formations —
and then ran the ablation:

> *"we are able to isolate the effects of each contribution through controlled testing"*

**The control is stated explicitly:**

> *"In order to test the flexible teamwork structure, we ran a team using ball-dependent
> flexible positions with set-plays against one using rigid positions and no set-plays."*

> *"with rigid positions and no set-plays. The behaviors of the players on the two teams are
> otherwise identical."*

**Referent check.** *"the two teams"* are (i) the flexible team with changeable positions and
set-plays and (ii) the *"default team"* with rigid positions and no set-plays; both used a
4-4-2 formation. The phrase *"otherwise identical"* is the authors' own single-difference claim, and it
is what makes this an ablation rather than a matchup.

**Combined result, 38 games of 10 simulated minutes each:**

> *"The flexible team won 34 out of 38 games with 3 ties."*

The table (Table 3): Flexible-and-Set-Plays **34 games won, 223 total goals, 5.87 avg goals,
43.8% ball in own half**; Default **1, 82, 2.16, 56.2%**.

**And then the componentwise legs — this is the part that matters, because one of them
isolates the plan library alone.** Table 4, again 38 games per leg, against the same default
team:

| leg | games won | total goals | avg goals | ball in own half |
|---|---|---|---|---|
| Only Flexible Positions | **26** (vs Default 6) | 157 (vs 87) | 4.13 (vs 2.29) | 44.1% (vs 55.9%) |
| **Only Set-Plays** | **28** (vs Default 5) | **187** (vs 108) | **4.92** (vs 2.84) | 47.6% (vs 52.4%) |

> *"Both characteristics provide a significant advantage over the default team, but they
> perform even better in combination."*

**The "Only Set-Plays" row is a plan-library-versus-no-plan-library ablation with positions
held rigid on both sides: 28 wins to 5 over 38 games, and 187 goals to 108.**

**A second, weaker instance was run in a live tournament.** CMUnited-97 entered its own
ablation as a separate team:

> *"was also our own team and was identical to CMUnited except that it did not use a flexible
> teamwork structure: players did not switch positions, did not use flexible positioning of
> any sort, and did not use set-plays."*

**Referent check.** The subject is *FCMellon*, named in the preceding clause — *"Its 5th
opponent, FCMellon"* — where *"Its"* is CMUnited-97. And the ablation was not weak going in:
*"Before the game between CMUnited and FCMellon, FCMellon won its 4 games by a combined score
of 49"* — 49–4 across its first four games. CMUnited beat it **6–0**.

**The authors then say the thing this library has been circling for four sweeps:**

> *"Since competitions are not controlled experiments, their results are not presented as
> scientific validation of our individual techniques."*

## WHY IT MIGHT TRANSFER

`transfers: partial`, and the partiality is the whole point of the file.

- **What transfers is the existence proof and the methodology, not the effect size.** The
  library's standing bound — that this library cannot adjudicate cause versus marker for us
  and the arena is the only instrument (an internal INDEX statement, paraphrased, not a source
  quote) — is a statement about the game-competition literature. It
  survives. What changes is that **an adjacent literature does run ablations, publishes the
  populations, and states in so many words that tournament results are not validation.** The
  next time a sweep needs a controlled comparison, RoboCup is where to look first, not last.
- **The set-play is the closest published object to what our project lead asked for.** His
  standing ask — quoted from the sweep brief, not from any external source — is *"what i would
  like to investigate is bigger plans than that, more steps that might make a bad tactic
  actually a good tactic"*, and the set-play was measured in isolation and it paid. That is a real answer to a question the
  library has held open since before it existed.
- **The mechanism that made it work is cheap in our engine.** A set-play is trigger +
  behaviour + termination condition, stored in code shared by all agents. See
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)
  and
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md).

## WHAT WOULD KILL IT

- **The baseline is rigid-scripted, not reactive.** Nobody here ablated against a memoryless
  reactive agent. The measured claim is **stored multi-step plans beat no stored plans, roles
  held constant** — not *deliberation beats reaction*. Anyone quoting this file must quote that
  boundary with it.
- **Soccer is not our game, and the disanalogy is exactly our unifying fact.** Set-plays are
  passing sequences among mobile attackers. Our attackers are immobile, bought, and cannot
  retreat; healing beats the best damage source 2.2:1 (4.4:1 on a stacked core tile). **A
  measured gain for coordinated multi-agent offence in a game with no defender's edge does
  not license one here.**
- **The noise is acknowledged in the source**: *"due to the large amount of noise, game
  results vary greatly"*, which is why every figure is cumulative over 38 games. No
  confidence intervals are published; *"significantly"* is used without a test statistic in
  the text I verified.
- **27 years old, and the soccer server of 1997 is not a modern engine.** Nothing here has
  been replicated in this form since, as far as this sweep found.
- **The competing evidence is filed beside it and is more recent and more adversarial** —
  see [`the-htn-planner-lost-every-game-to-a-scripted-rush`](the-htn-planner-lost-every-game-to-a-scripted-rush.md).
  The reconciliation the sweep proposes is in the summary: **plans win as coordination
  devices across agents, and lose as substitutes for one agent's move choice.** That
  reconciliation is the sweep's own inference, not either source's claim.

## BUILDER HOOK

None directly — this file licenses *looking*, not building. The buildable descendants are
[`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)
and [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md).
What it does license immediately is a **method demand on any future incidence experiment**:
Stone & Veloso got a usable answer by changing exactly one component and holding behaviour
otherwise identical, over a fixed game count, reporting four statistics rather than one. Our
own parity-first discipline is the same instrument; this is the field's precedent for it.

## SOURCES QUOTED IN THIS FILE

- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). Tables 3 and 4 were additionally re-extracted with
`pdftotext -layout` and the row/column assignment checked against the layout output.
