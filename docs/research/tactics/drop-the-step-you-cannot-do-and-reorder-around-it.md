---
tactic: (B) TWO ONE-LINE PREDICATES THAT KEEP A PLAN MOVING — drop every leading step that demonstrably cannot be done, then pull a later affordable step forward. And the measured warning: the first version of the second one fired once per game and was worth nothing
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ProductionManager.cpp
origin: Steamhammer (StarCraft AI), with the measurement from its author's blog and a corroborating account from the author of Locutus
evidence: documented
transfers: partial
---

## WHAT IT IS

**The drop rule.** Steamhammer runs this every frame, before anything else touches the plan:

> *"// Drop any initial items from the queue that will demonstrably cause a production jam."*

The loop pops the head while it fails a single predicate whose own comment states its
conservatism:

> *"// Return false if the item definitely can't be made next."*
> *"// This doesn't yet try to handle all cases, so it can return false when it shouldn't."*

and the caller's comment names the purpose:

> *"// Drop any initial queue items which can't be produced next because they are missing"*
> *"// prerequisites. This prevents most queue deadlocks."*

**The reorder rule.** When the head is unaffordable but a later step is not:

> *"// If we can't immediately produce the top item in the queue but we can produce a"*
> *"// later item, we may want to move the later item to the front."*

with guards that stop it firing in an emergency (*"If we're in a severe emergency situation,
don't try to reorder the queue."*), never in front of a command, and never ahead of supply.

## ⚠ THE MEASUREMENT, AND IT IS A NEGATIVE

The author published what the first version of the reorder rule was worth:

> *"Because of this conservatism, queue reordering happens rarely, about once per game on
> average, and has virtually no effect on the bot’s strength."*

**Referent check, and it is essential.** *"this conservatism"* refers to the restrictions of
the **first** implementation, enumerated in the two preceding sentences: it recognised only
the gas case, looked at most **3 items** ahead, required the pulled item to have no
dependencies other than a worker, and *"doesn’t try to predict mineral income"*. **The number
carries its subject: "about once per game on average", population = Steamhammer's own games,
denominator = one game; no sample size and no win rate are given.** *(Glyph note: `bot’s` uses
a curly apostrophe.)*

He kept it anyway, widened the window from 3 to 4 items and added a second trigger case, after
which the same post reports qualitatively that protoss and especially terran see frequent
reordering and *"it helps noticeably"* — again with no number.

**And the independent corroboration is a simplification, not an elaboration.** The author of
Locutus (a UAlbertaBot descendant; the same person later wrote **Stardust**, 2nd at AIIDE
2025 — *"which happened with my previous bot Locutus in 2018"*, his own Stardust README)
commented on that post:

> *"In Locutus I'm still using BOSS but am severely limiting its decision making."*

> *"This helped immensely for relatively little effort."*

> *"I also added code in the production manager to just erase the item in the top of the queue
> if we can't make it and it isn't a building."*

> *"Longer-term I think I'm leaning towards not having a queue at all after the opening, and
> instead just deciding each frame what is most important to build."*

**Referent check.** *"This"* refers to the sentence immediately before it in the same comment,
which describes pre-filtering the planner's *inputs* by idle-producer availability and
prerequisites — **not** the erase rule, which is described in the following sentence.
*(Glyph note: these use ASCII apostrophes while Jay Scott's own text on the same page uses
curly ones — the per-string glyph trap, inside one document.)*

## WHY IT MIGHT TRANSFER

- **The drop rule is nearly free here and maps onto an engine call we already have.** Our
  legality predicate is `can_build_<type>(position, direction)`, and the library has measured
  that it is **strictly stronger than `is_tile_empty`**. A "drop the head while
  `not can_build(...)`" loop is one `while` and one engine call.
- **The reorder rule has a much better prior here than in StarCraft.** Steamhammer's version
  was crippled by not predicting income; **our income is closed-form** — a harvester emits one
  10-titanium stack every 4 rounds, passive income is 10 every 4 rounds, and costs are exact
  via the `get_*_cost()` getters. The exact objection that made his version fire once per game
  does not apply to us.
- **Our cost scale gives reordering a second, sharper motive he did not have.** Every build
  raises the price of every future build. So the *order* in which two affordable steps are
  taken changes what the second one costs — which the library already filed as
  [`a-rising-price-makes-the-ORDER-of-actions-matter`](a-rising-price-makes-the-ORDER-of-actions-matter.md).

## WHAT WOULD KILL IT

- **The only measurement in the family says it was worth nothing at first.** *"about once per
  game on average, and has virtually no effect"* is the number to beat. **The right first
  question is not "does reordering help" but "how often would it fire", and that is countable
  without changing behaviour.**
- **The trend among the people who built it is away from it.** The Locutus author's stated
  direction is no queue after the opening; Jay Scott's is *"Of course I intend to drop BOSS
  when I get that far."* Anyone building this should read
  [`the-planners-only-promise-is-terminal-not-temporal`](the-planners-only-promise-is-terminal-not-temporal.md)
  first.
- **A drop rule that is too eager silently deletes intentions.** Steamhammer's predicate is
  deliberately conservative and its own comment admits it can return false when it shouldn't.
  Ours would inherit that: `can_build_*` is false when a *transient* condition holds (a
  friendly bot standing on the tile), and dropping the plan for that is wrong.
- **Neither rule exists in our engine's shape yet, because we have no queue.** These are
  operations on a representation we do not have; adopting them means adopting the
  representation, which is `partial` for the reasons in
  [`the-plan-is-a-queue-and-each-step-carries-one-bit`](the-plan-is-a-queue-and-each-step-carries-one-bit.md).

## BUILDER HOOK

Counting before building, exactly as the negative advises: wherever the bot wants to buy the
next thing and cannot afford it, `print()` whether **any** cheaper item on its wish list is
affordable this round. **Count the rounds per game where the answer is yes.** If that count is
near one, this is Steamhammer's first version and it is not worth a plank. If it is large,
reordering is worth exactly one comparison and the closed-form income arithmetic is already
available through the cost getters.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ProductionManager.cpp
- http://satirist.org/ai/starcraft/blog/archives/531-Steamhammers-improved-queue-reordering.html
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/README.md

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
