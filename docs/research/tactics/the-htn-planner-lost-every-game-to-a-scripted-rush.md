---
tactic: (D) THE HARDEST NUMBER IN THE SWEEP — in a 10-agent round robin on an RTS, a hierarchical-task-network PLANNER and an MCTS searcher finished 8th and last, below three of four hand-coded reactive rushes, and the simplest rush beat the planner 100.0% of the time
source: https://arxiv.org/pdf/1709.03480
origin: µRTS (MicroRTS) — Barriga, Stanescu & Buro, *Combining Strategic Learning and Tactical Search in Real-Time Strategy Games*; corroborated by the µRTS competition standings 2017 and 2020
evidence: documented
transfers: yes
---

## WHAT IT IS

µRTS is a minimal RTS built specifically so that planning and search algorithms can be
benchmarked against hand-coded scripts. Table 4 of this paper is a full round robin of ten
agents. The caption gives the population:

> *"Table 4: Mixed Strategy/Tactics agents: round-robin tournament using 60 different
> starting positions per match-up."*

**Rows are agents; the last column is the average win rate; each interior cell is the row
agent's win rate against the column agent.** Column order, from the header, is
Policy-net-Naïve, PS-Naïve, PS, Policy Network, LightRush, HeavyRush, RangedRush, AHTN-P,
WorkerRush, NaïveMCTS. Three rows, verbatim from the layout-preserving extraction:

> *"LightRush 0.0 10.0 13.3 5.8 - 71.7 100.0 100.0 100.0 96.7 55.3"*

> *"AHTN-P 27.5 10.0 3.3 42.5 0.0 0.0 0.0 - 64.2 68.3 24.0"*

> *"veMCTS 1.7 6.7 6.7 2.5 3.3 25.8 13.3 31.7 28.3 - 13.3"*

**(The MCTS row is quoted from mid-name because "Naïve" uses a dotless i plus a combining
diaeresis, which no literal grep of the ASCII form can match. See the method note in the
summary.)**

**Read the average column.** LightRush **55.3**, HeavyRush **52.4**, RangedRush **33.4**,
**AHTN-P 24.0**, WorkerRush 20.6, **NaïveMCTS 13.3**.

**AHTN-P is a planner.** The paper says so:

> *"AHTNs are an alternative approach, similar to Puppet Search, that instead of sampling
> from the full action space, uses scripted actions to reduce the search space. It combines
> minimax tree search with HTN planning."*

**Referent check.** *"AHTNs"* is expanded in the same section as *"Adversarial Hierarchical
Task Networks (AHTNs)"*. NaïveMCTS is described in the adjacent sentences as an MCTS variant
over Combinatorial Multi-Armed Bandits where *"each variable represents a unit"*.

**The interior cells are worse than the averages.** Against AHTN-P, LightRush scores
**100.0**, HeavyRush **100.0**, RangedRush **100.0** — three hand-coded scripts each winning
**60 of 60** starting positions against the HTN planner. The MCTS agent finishes **last of
ten**.

**And the compute budget is generous.** From the paper:

> *"3ms versus a time budget of 100ms per frame for search-based agents"*

**Referent check.** The full sentence is *"Finally, with the policy network running
significantly faster (3ms versus a time budget of 100ms per frame for search-based agents)
than Puppet Search we can use the unused time to refine tactics."* So **100 ms per frame is
what the search agents were given**; 3 ms is the neural policy's own cost. The organisers'
rules page states the same figure for the competition:
*"Each bot will be given a computation budget of 100 milliseconds per game cycle"*
(`https://sites.google.com/site/micrortsaicompetition/rules`).

**The competition standings agree.** The 2017 CIG results page
(`https://sites.google.com/site/micrortsaicompetition/competition-results/2017-cig-results`)
publishes each track's standings as an HTML **ordered list** (`<ol style="list-style-type:
decimal">`, verified in the raw markup, so list position is rank). Standard Track, Open Maps,
the first four entries in order: **`LightRushPO (baseline)`**, `StrategyTactics`,
`PVAIML_ED`, `WorkerRushPO (baseline)` — with `PuppetSearch (baseline)`, `NaiveMCTS
(baseline)` and `BS3_NaiveMCTS` below them. **A scripted baseline won the track.**

**What the search DID win at is worth recording, because it is the shape that worked.** Table
3 of the same paper — same 60-starting-positions population — puts Puppet Search top at
**65.8** average against the best individual script's **48.3**. And Puppet Search's entire
action space *is* those scripts:

> *"The Puppet Search version we used for all the following experiments utilizes alpha-beta
> search over a single choice point with four options."*

> *"The four options are WorkerRush, LightRush, RangedRush and HeavyRush, and were also used
> as baselines in the following experiments."*

**So the winning use of search was choosing among a small library of pre-authored scripts at
one choice point — not constructing a plan.**

## WHY IT MIGHT TRANSFER

- **This is the direct empirical answer to sub-question (D), with populations, in an RTS.**
  Nothing else in the library comes close to a scripted policy winning 60 of 60 starting
  positions against a planner.
- **The budget comparison points the wrong way for us.** These results were measured at
  **100 ms per decision cycle for the whole army**. We get **10 ms per unit per turn**, and
  exceeding it silently discards that unit's turn. We are an order of magnitude below the
  budget at which planning already lost.
- **The surviving positive shape is exactly the one sweep 18's RoboCup leg found
  independently** — searching over a small library of authored options, rather than
  constructing a sequence. Combined with
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md),
  the two literatures converge on: *author a handful of modes; pick between them; do not
  build a sequence.*
- **It supplies a warning about our own doctrine, not just theirs.** Our field's
  documented converters are all discrete mode switches (17A). This is the negative that
  explains why nobody in the RTS-AI literature built anything richer and made it stick.

## WHAT WOULD KILL IT

- **µRTS is not our game and its scripts are not our bots.** LightRush is a hard-coded
  all-in on a small map with no healing and no defender's edge. Our own arithmetic says the
  defender wins a titanium-symmetric attrition race 2.2:1, so a µRTS-style rush is not
  automatically strong here — sweep 14 already established that our rush road is narrow.
  **The finding transfers as "planning did not beat scripts", not as "rush".**
- **AHTN-P's poor showing may be AHTN-P's.** One implementation of one HTN planner, in one
  paper, on 128×128 maps (*"All experiments were performed on 128x128 maps ported from the
  StarCraft: Brood War maps"*). It is a strong data point, not a proof about HTNs.
- **The competition standings flip on the hidden-map set.** On All Maps (Open + Hidden) the
  2017 Standard Track order begins `StrategyTactics`, then `LightRushPO` — the hybrid first
  and the script second. Reporting only the Open-Maps line would overstate the negative, so
  both are stated.
- **These are academic agents, not competitors under a deadline.** The scripts were written
  by the organisers as baselines. A ladder where every entrant is tuned for months may look
  different.

## BUILDER HOOK

None — this is a **stop sign**, and the useful form of it is a budget rule rather than a
build. If any future plank proposes forward search or sequence construction inside `run()`,
this file is the prior: at 10× the compute we have, the same idea finished 8th of 10 and lost
60–0 to three separate hand-written policies. The affordable version of "search" here is
**one choice point over a handful of authored modes**, which is Puppet Search's shape and
costs a comparison, not a rollout.

## SOURCES QUOTED IN THIS FILE

- https://arxiv.org/pdf/1709.03480
- https://sites.google.com/site/micrortsaicompetition/rules
- https://sites.google.com/site/micrortsaicompetition/competition-results/2017-cig-results

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). **Table 4 and Table 3 must be read from
`pdftotext -layout`; the default extraction reorders those tables column-wise and produces
number sequences that do not correspond to any row.**
