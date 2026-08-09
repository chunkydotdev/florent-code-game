---
tactic: (A)+(D) THE ARCHITECTURE THAT RESOLVES THE SWEEP'S CONTRADICTION — a Battlecode finalist ran BOTH layers with a strict precedence: the reactive layer picks the move, and the multi-step plan is only allowed to break ties among moves the reactive layer rated equal
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021, wololo — 7th in the final tournament; corroborated as general practice by Jay Scott
evidence: documented
transfers: yes
---

## WHAT IT IS

wololo's units decide in two stages, and he names them:

> *"My units typically made decisions in two steps: the “micro” step and the “macro” step. The
> micro step was dedicated to choices which would incur an immediate effect in one round,
> while the macro step handled all other strategies."*

The micro step runs a minimax over immediate conviction gain. **The plan layer only sees what
minimax could not decide:**

> *"If there was a tie between multiple move directions (which occured in most cases), then
> all of the best move directions were fed to the macro step, which chose one of these move
> directions."*

**Referent check, and the parenthetical is load-bearing.** *"(which occured in most cases)"*
is his own estimate — **ties are the common case, so the plan layer does in fact drive most
turns.** It simply never overrides an urgent move. His stated intent:

> *"This ensured that my units always prioritized actions which urgently, clearly, and
> immediately produced gains or prevent opponent gains, and only afterwards did they consider
> taking actions to encourage more unpredictable longer-term gains."*

**And his plan layer is real, not decorative** — a per-unit persistent role assigned at build
time: *"my code assigned each unit a “role”, which described the functional portion of the
strategy which the unit helped to execute, and the manner in which it did so."*
**(Glyph note: the PDF uses curly quotation marks around `role`; the ASCII-quoted form does
not grep. The same applies to `"micro"` and `"macro"` in the first quotation above.)**

**A second author states the same allocation as a general principle.** Jay Scott, in a post
opposing search to knowledge:

> *"Unit control, by the same general principles, should be as reactive and knowledge-based as
> possible"*

**Referent check.** *"the same general principles"* is the preceding paragraph's argument that
StarCraft is real-time and so its bots should use more knowledge and less search than chess or
Go programs. His complementary claim in the next sentence is that tactical and strategic
decisions are made less often over more abstract state, *"which favors searches that compare
alternatives."* And, on what top bots actually do:

> *"Other than that, it seems to me that play is reactive: What have I seen, what do I see
> right now?"*

**Referent check.** *"that"* refers to his preceding sentence, that top bots predict *"at the
lowest and highest levels"* — individual unit movements for micro, and initial strategy choice
— **and everything in between is reactive.** Population: "top bots" at 2018 tournament level;
no list, no count, and he frames it as *"it seems to me"*.

## WHY IT MIGHT TRANSFER

**This is the architecture that reconciles the two halves of sweep 18, and it does so without
choosing a side.** RoboCup measured that stored multi-step plans win as a coordination device;
MicroRTS measured that planners lose as substitutes for one agent's move choice. wololo's
precedence rule assigns each to the layer where it won.

- **It fits our engine's hardest constraint exactly.** A builder bot's action and movement are
  **mutually exclusive** and both are cooldown-gated, so the per-round decision is genuinely
  scarce. Letting a multi-round intention override an urgent, immediately-priced action costs
  a whole round. wololo's rule says: never.
- **It gives the plan a job that is cheap and safe — tie-breaking.** Under our arithmetic most
  moves genuinely are ties: a builder walking through open ground has several equally-scored
  cardinal steps. **A plan that only selects among already-acceptable options cannot make a
  locally-bad choice**, which means it costs nothing when it is wrong.
- **It is the safe form of what 17A said we lack.** 17A found that a return-priced bot is
  *correct* never to commit, and that the documented converter is a discrete mode switch. A
  tie-break-only plan layer does **not** suspend per-step pricing — so it is not the converter
  — but it is the version that can be shipped without risking the thing we already win on.
- **It names the precedence explicitly, which our bot currently does not.** Our own code
  interleaves urgent reactions (heal the damaged core) with longer intentions (walk to a seat)
  without a stated order, and the measured consequence is the 4.4× movement suppression the
  library already holds.

## WHAT WOULD KILL IT

- **A tie-breaking plan can never redeem a locally-bad step, which is the thing our project
  lead actually asked about.** his ask for *"more steps that might make a bad tactic actually a good
  tactic"* (quoted from the sweep brief, not from a source) requires the plan to sometimes **beat** the reactive layer, not defer to it.
  **This file is explicitly the conservative option and should not be sold as the answer to
  that question.** The answer to that question, if there is one, is
  [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)
  plus 17A's mode switch.
- **wololo placed 7th, not 1st, and reports no ablation.** He describes the design and his
  reason for it; there is no comparison against a version without the macro step. Evidence is
  `documented` for the architecture.
- **Ties being the common case is his game, not ours.** If our move scoring is fine-grained enough
  that ties are rare, the plan layer never gets to act and this buys nothing. **That is
  measurable before anything is built.**
- **Jay Scott's own corroboration is explicitly hedged** (*"it seems to me"*) and carries no
  population. It is a practitioner's impression, filed as such.
- **He also removed a multi-unit coordination plan for over-constraining his units:** *"I later
  removed the relay chain behavior because it would cause my explorers to have trouble
  splitting their focus to target multiple locations at once."* Even inside the layer he kept,
  the direction of travel was toward less coordination.

## BUILDER HOOK

Smallest test, and it is a measurement of whether the architecture is even available to us:
for one builder class, compute the reactive score for all four legal cardinal moves and
`print()` how many are tied at the maximum. **If ties are common, the plan layer has somewhere
to live and costs nothing; if the argmax is almost always unique, this road is closed.** That
is one print and no behaviour change, and it is the precondition for every other
plan-shaped idea in this sweep.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
- http://satirist.org/ai/starcraft/blog/archives/73-search-versus-knowledge.html
- http://satirist.org/ai/starcraft/blog/archives/636-react-to-more-of-the-future.html

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
