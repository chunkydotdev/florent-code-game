---
tactic: The two leagues that DO price the Nth structure higher — and the only doctrine either produced is an ACTION-ORDERING rule
source: https://raw.githubusercontent.com/CodinGame/SpringChallenge2021/main/config/statement_en.html.tpl
origin: CodinGame Spring Challenge 2021 (Photosynthesis) — official statement and referee constants; doctrine from jolindien and aCat in the official feedback thread. Second mechanic: GemCraft (community wiki)
evidence: documented (rules) / anecdotal (doctrine — forum posts, ranks not established)
transfers: partial
---

## WHAT IT IS

Question (C) asked whether any league had superlinear structure costs. Across Battlecode,
Screeps and Terminal the answer is **no** (see
[`nobody-else-has-a-rising-build-cost`](nobody-else-has-a-rising-build-cost.md)). Two
outside that set do have it, and one of them produced a doctrine.

**1. CodinGame Spring Challenge 2021 (Photosynthesis) — the price of an action is the base
cost PLUS the number of things you already own of that kind.** From the official statement
template (verified after stripping HTML tags — the raw file interleaves `<const>` markup
inside the numerals, so the sentence does not grep as one literal string in raw bytes;
this is a new markup trap for the library's method):

> *"Growing a seed into a size 1 tree costs 1 sun point + the number of size 1 trees you
> already own. Growing a size 1 tree into a size 2 tree costs 3 sun points + the number of
> size 2 trees you already own. Growing a size 2 tree into a size 3 tree costs 7 sun
> points + the number of size 3 trees you already own."*

> *"To perform a seed action, you must pay sun points equal to the number of seeds (size 0
> trees) you already own in the forest."*

Referee constants confirm: `TREE_BASE_COST = new int[] { 0, 1, 3, 7}; TREE_COST_SCALE = 1;`.

**The doctrine that came out of it is about ORDER, not about counts.** jolindien, in the
official feedback thread:

> *"impose an order in actions during a day : first COMPLETE, then GROW for trees of size
> 2, size 1, size 0 and eventually SEED."*
>
> *"It usually make actions cheaper in this order (GROW price depend on number of trees of
> higher size)."*

*(Quoted as two spans because a line break sits between them in the source; the two
sentences do not grep as one string. The typo "make" is the author's.)*

**Retire first, then build — because the count you are charged against has already been
decremented.** aCat reports the same shape as a search-pruning rule.

**2. GemCraft — an arithmetic rising price on the Nth tower.**

> *"In GemCraft the first tower costs 200 mana (minus 20 per level of Masonry) and each
> subsequent one costs an additional 75 mana (minus 3 per level of Masonry)."*

200, 275, 350, … **This is the closest published analogue to our scale mechanic, and the
sweep leg found no doctrine attached to it on the wiki** — the mechanic is documented and
its consequence is not. Recorded so nobody re-searches it expecting more.

*(A third mechanic that looks like this and is not: Kaggle Kore's shipyards gain **spawn
capacity** with turns controlled. The engine source is `upgrade_times = [pow(i, 2) + 1 for
i in range(1, 10)]` (verified verbatim in `kaggle_environments/envs/kore_fleets/helpers.py`
line 350), with a flat ship cost. **Paraphrase, marked as such:** capacity rises with how
long you have held the shipyard, on a quadratic schedule; the price never moves. **The
rules prose stating the same thing does NOT grep from raw bytes — the Wayback capture
stores it as JSON in which every plus sign is escaped to its six-character `\u00` unicode
form** — so only the source line is quoted here.
Rising capacity is not rising price; filed so it is not miscounted as one.)*

## WHY IT MIGHT TRANSFER — and there is a live, testable consequence

**Our engine has the Photosynthesis property and a free retire action, which is a
combination Photosynthesis did not have.** `docs/game-model.md:393-395` (measured):
`effective_cost = floor(scale × base_cost)`, scale rises additively per entity built and
**"decreases again when an entity is destroyed"**. And `destroy()` on an allied building
is **free, cooldown-free and unlimited per turn** — a builder bot can destroy *and still
take its one action* in the same turn.

**⇒ The direct translation of jolindien's rule: when a build and a demolition are both
planned, DEMOLISH FIRST.** The scale contribution of the demolished entity is refunded,
so the new build is priced against the lower scale.

Worked, at a scale of 2.0 with a sentinel (+0.20) coming down and another going up:
demolish-then-build prices the new sentinel at `floor(1.8 × 30) = 54`; build-then-demolish
prices it at `floor(2.0 × 30) = 60`. **10% of a sentinel, for free, purely from ordering
two actions we were taking anyway** — and the same 0.2 discount applies to *every other
build made in that window*, not just the replacement.

**This composes with the existing `destroy-rebuild-converter` file** rather than
duplicating it: that one is about converting a structure into something else; this is
about the *order* in which the two halves happen.

## WHAT WOULD KILL IT — and one thing that must be probed before anyone builds it

- **⚠ UNVERIFIED PRECONDITION, stated plainly: I have NOT probed whether a `destroy()`
  updates the scale factor within the same round, or only at end of round.** If scale is
  recomputed at end of round, the ordering trick is worth nothing within a turn and only
  works across turns. **Probe `get_scale_percent()` immediately before and after a
  `destroy()` call before acting on this.** This is the single load-bearing engine fact
  and it is currently an assumption.
- Cross-turn, the same ordering still holds and is safe: destroy on round N, build on
  round N+1 at the lower scale.
- **The doctrine limb is a forum post by an author whose rank I did not establish** —
  `anecdotal`. The *mechanic* it reasons about is `documented` from the official statement
  and referee constants.
- Photosynthesis's cost rises with the count of a **single tier**; ours is one global
  number shared across every category, so the ordering benefit spills onto unrelated
  builds — which makes it larger here, not smaller.

## BUILDER HOOK

1. **The probe first, and it is three lines**: read `get_scale_percent()`, call
   `destroy()` on a disposable allied barrier, read it again in the same turn. That single
   observation decides whether the rest exists.
2. **If it holds:** anywhere the bot already plans a demolish-and-rebuild — the
   destroy-rebuild converter, replacing a damaged turret, clearing a conveyor to reroute —
   emit the `destroy()` before the `build()` in the same turn, and prefer scheduling any
   *other* pending build into the same window.
