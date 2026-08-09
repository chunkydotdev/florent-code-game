---
tactic: A published observation of LLM agents failing at EXACTLY our failure — checking whether each entity works and never checking whether the structure is connected correctly
source: https://arxiv.org/pdf/2503.09617v1
origin: Jack Hopkins, Mart Bakler, Akbir Khan, "Factorio Learning Environment" (arXiv 2503.09617, v1 2025-03-06)
evidence: documented
transfers: partial
---

WHAT IT IS — the authors report, of six frontier models playing a factory-building
benchmark, a failure mode that is our binding-tile cut restated. The referent of
*"the agents"* is established by the sentence that precedes it, which is quoted so
the label the authors themselves put on the claim travels with it:

> *"Anecdotally, the agents were not proficient at debugging complex environments."*

> *"For instance, when debugging non-working structures or factories where the throughput was not at expected levels, agents often focused on whether all singular entities were working but did not investigate whether the topology of the whole structure was correct."*

Two more, from the same passage:

> *"the agents broke existing working structures due to incorrectly identifying the root-cause of problems"*

> *"Agents often fell into a loop of greedily repeating the same fix rather than exploring additional potential sources of the problem."*

and, from the abstract:

> *"We demonstrate across both settings that models still lack strong spatial reasoning."*

**Fixture, because these are claims about a population:** six frontier LLM agents,
FLE lab-play (8 structured tasks) and open-play, 128 environmental interactions.
**The authors label the first passage `Anecdotally` themselves** — it is an
observational remark in a paper, not a measured statistic, and it must not be
quoted as one.

WHY IT MIGHT TRANSFER — uncomfortably directly:

- **Our bot was written by agents of this class, and our measured failure is the one
  named here.** 85.15% of our binding tiles have no directed path to the core;
  `can_build_conveyor` returns `True` for every one of them. **Each entity is
  working. The topology is wrong.** The correspondence is close enough that this
  should be read as a statement about our development process, not only about our
  bot.
- **The second quote names a specific hazard for the planks in this sweep.** Several
  of them give a builder a new reason to `destroy()` or rebuild. *"the agents broke
  existing working structures due to incorrectly identifying the root-cause"* is the
  failure mode of a repair loop with a bad diagnosis, and our `destroy()` is free,
  uncapped and instant. **A wrong terminus predicate plus an eager destroy loop can
  dismantle a working network faster than the enemy can.**
- **The third names the shape of a bad reaction to a latched detector** — repeating
  the same fix. That is the argument for the hysteresis and the randomised response
  in [`the-stuck-counter-is-the-universal-primitive`](the-stuck-counter-is-the-universal-primitive.md)
  and for CluelessPlus's post-repair baseline damping.

WHAT WOULD KILL IT —

- **It is not a competitive league and it is explicitly anecdotal.** No score, no
  ablation, no per-model breakdown of this specific failure. `transfers: partial`
  is generous and rests on the closeness of the description, not on its rigour.
- **The population is LLM agents playing interactively via a tool API, not a
  compiled bot running 1000 rounds.** Our bot does not "debug"; it executes a policy
  someone wrote. **The correspondence is between their agents and *us as authors*,
  which is a different claim from the one the paper makes** and is my inference.
- **And the paper's agents had `connect_entities` available** — a route primitive
  that removes hand-routing entirely (see
  [`make-the-route-a-primitive-not-an-authored-path`](make-the-route-a-primitive-not-an-authored-path.md))
  — and still failed on topology. **So the route primitive is necessary and not
  sufficient**, which is a caution against expecting too much from the (A) planks.

BUILDER HOOK — a process guard rather than a code change, and the cheapest one
available: **every plank in sweep 19 must be gated on a topology-level mechanism
counter** (chains reaching the core; head-to-head pairs created; conveyors aimed at
friendly buildings) **and never on an entity-level one** (conveyors built, builders
alive, titanium spent). This paper is the reason to write that down rather than
assume it.
