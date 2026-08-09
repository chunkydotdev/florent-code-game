---
tactic: (D) THE DEEPEST NEGATIVE — a plan whose only guarantee is "the goal will hold when the plan ends" cannot be steered by urgency, and its author calls that a DESIGN defect that no amount of tuning fixes
source: http://satirist.org/ai/starcraft/blog/archives/326-doing-away-with-the-BOSS.html
origin: Jay Scott, author of Steamhammer (StarCraft AI, SSCAIT/AIIDE), on BOSS — Dave Churchill's Build Order Search System, the planner inside UAlbertaBot
evidence: documented
transfers: yes
---

## WHAT IT IS

BOSS is a real planner: it searches for a *sequence* of builds that achieves a stated goal
and returns it. Steamhammer inherited it from UAlbertaBot. In 2017 its maintainer wrote a
post titled *"doing away with the BOSS"* — lower-case `d` in the source — laying out why he wanted it gone, and the argument
is structural rather than about tuning:

> *"BOSS also works more effectively with long build orders, which means that bots tend to
> react slowly when the situation changes."*

**Referent check.** *"bots"* is named in the same post as Steamhammer's protoss and terran
players and Steamhammer forks that use BOSS; *"BOSS"* is introduced in the first paragraph as
*"BOSS by Dave Churchill"*. The claim is about bots that use BOSS, not bots in general.

The crux, and it is the sentence worth carrying:

> *"If you say you want an observer, BOSS promises that by the end of the build order you
> will have an observer; that"*[’s the only promise.]

**(Glyph note: the source renders `that’s` with a curly `’`. The bracketed tail is the
source's continuation, shown for sense; the verified literal span ends at `that`.)**

**And the enumeration of what a bot holding a long plan can do when it learns something new**
— four options, each with a named cost. Option 2 verbatim:

> *"It can wait for the current build order to finish and call for a reaction in the next
> build order. If the current build order is long, it may be a long wait before the reaction
> occurs."*

**Referent check.** *"It"* is *"the bot"* — the preceding sentence reads *"When the bot makes
a discovery (“uh oh, we need detection” or “that’s too many tanks, I should make zealots
instead of dragoons”), it has four choices."* The other three are: insert the reaction into the plan
(no overlap with regular production), cancel and replan including the reaction (slow, because
BOSS has no priorities), or cancel and replan with only the reaction (fast, everything else
stops).

**The author then separates the two complaints, and this is the load-bearing distinction:**

> *"The problem that BOSS makes poor build orders is an implementation issue."*

> *"The problem that using BOSS makes a bot slow to react to discoveries is a design issue.
> It can only be fixed by designing a different API."*

**Referent check.** Both sentences open the author's own comment on his own post, timestamped
*"Jay Scott on Sunday, July 9. 2017 : I should add:"*. He also names the fix in the post
body: *"Incremental planning"* — that the plan be worked out in small chunks so reactions can
be quick.

Two supporting observations from the same post about what a terminal-goal planner produces:

> *"BOSS often orders more production buildings than it can use, and then does not use them
> efficiently."*

and, from a later post, on the same planner:

> *"And BOSS creates long and poorly-designed sequences with many items out of order."*
> (`http://satirist.org/ai/starcraft/blog/archives/531-Steamhammers-improved-queue-reordering.html`)

Where it ended up, in the author's own words in that 2018 post:

> *"Of course I intend to drop BOSS when I get that far."*

## WHY IT MIGHT TRANSFER

**This is the argument against the shape of plan our project would be most tempted to
build,** and it is made by someone who shipped one for years.

- **Our situation has BOSS's defect built in.** A plan of the form "buy N sentinels, walk a
  builder to seat S, then open fire" is a terminal-goal plan: it promises the state holds at
  the end and says nothing about round-by-round urgency. Our engine then adds a constraint
  StarCraft does not have — **acting and moving are mutually exclusive for a builder bot**,
  so "insert the reaction into the plan" costs a whole round of the plan, not a slice of
  parallel capacity. Option 1's *"no overlap"* penalty is strictly worse here.
- **It sharpens, rather than contradicts, 17A's mode-switch finding.** 17A concluded the
  converter is a **discrete mode switch that replaces the economy policy**. A mode switch is
  precisely *not* a terminal-goal plan: it has no length, so it cannot have latency. This
  file explains why 17A's answer took that shape and not the other one.
- **It names the design property to demand of anything we do build: a plan must be able to
  say what it wants NOW, not only what it wants at the end.** Concretely, a mode index (see
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md))
  is re-evaluated every round and therefore has zero reaction latency by construction; a
  queued build sequence has latency equal to its remaining length.

## WHAT WOULD KILL IT

- **BOSS's specific failure may be BOSS's, not planning's.** The author himself splits the
  complaint in two and calls only *one* half a design issue. A planner with priorities and
  pre-emption would not have option 3's problem. **The transferable claim is narrow: a plan
  with a terminal-only contract reacts slowly. It is not "planning is bad."**
- **StarCraft's build tree is deep and ours is flat.** BOSS searched over prerequisites and
  tech chains; our buildings have no prerequisites at all. Much of what made BOSS's sequences
  long simply does not exist here, so our plans would be short, and a short plan has short
  latency. That materially weakens the transfer and should be stated.
- **No numbers.** Nothing in this post is measured. The one quantified claim in the family is
  the *negative* in
  [`every-author-who-extended-the-plan-past-one-step-said-it-did-not-help`](every-author-who-extended-the-plan-past-one-step-said-it-did-not-help.md).
- **The author's own alternative was never shown to win either.** He describes incremental
  planning as the fix; the library holds no measurement that it did.

## BUILDER HOOK

Not a build — a **design rule to apply to the next plank that proposes a sequence**: any
multi-round commitment we add must be able to answer the question *what do I want this round* without
reference to how far through it we are. If the only way to know is "step 4 of 7", it has
BOSS's defect. The cheapest concrete form that passes the test is a mode index recomputed
each round from world state, with the *content* of each mode in code. If a plank proposes a
literal queue instead, it must ship with the disruption classifier from
[`classify-the-disruption-before-you-replan`](classify-the-disruption-before-you-replan.md)
in the same plank, because that is the fix the same author found actually worked.

## SOURCES QUOTED IN THIS FILE

- http://satirist.org/ai/starcraft/blog/archives/326-doing-away-with-the-BOSS.html
- http://satirist.org/ai/starcraft/blog/archives/531-Steamhammers-improved-queue-reordering.html

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
