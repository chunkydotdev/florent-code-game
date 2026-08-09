---
tactic: TRANSFERS: NO — the "repair vs rebuild" literature measured COMPUTE, not resources, and returned a negative
source: https://gki.informatik.uni-freiburg.de/papers/nebel-koehler-aij95.pdf
origin: Bernhard Nebel and Jana Koehler, "Plan reuse versus plan generation: a theoretical and empirical analysis", Artificial Intelligence 76 (1995) 427-454
evidence: documented
transfers: no
---

WHAT IT IS — sub-question (B) asked whether anyone **measured** which pays,
repairing a broken route or rebuilding it. The closest thing to a measured answer
in any adjacent literature is the AI-planning result on **plan reuse versus plan
generation**, and it is filed here as a `no` so the next session does not spend a
sweep discovering the same mismatch.

Nebel and Koehler test the reuse hypothesis both ways:

> *"We test this hypothesis from an analytical and empirical point of view."*

The analytical half returns a negative on the worst case — reuse buys no provable
efficiency gain over generation, and *conservative* reuse (the variant that insists
on keeping as much of the old plan as possible) is strictly worse:

> *"plan reuse can actually be strictly more"*

> *"gain of reuse over generation"*

*(Those two spans are quoted separately and truncated deliberately: the source PDF
loses its `fi`/`ffi`/`ff` ligatures on extraction — see the method note below — so
the words `difficult` and `efficiency` that complete both sentences cannot be
literally re-grepped and are therefore not placed inside quotation marks. The
sentences they belong to are, in the extraction,* `plan reuse can actually be
strictly more dicult than plan generation` *and* `it is not possible to achieve a
provable eciency gain of reuse over generation`.)

The conclusion states where reuse *does* make sense, and it is not the efficiency
argument that motivated it:

> *"only seems to make sense in a replanning context where one wants to minimize the perturbation of the original plan"*

And it names what actually costs the money, which is not the repair but the lookup:

> *"The bottleneck in retrieving such a candidate from the library seems to be that the matching problem"*

Its description of what working systems actually do is the one line a builder
should take from it:

> *"instead of using as much of the old plan as possible these systems recycle as much of the old plan as the particular planning algorithm will perhaps be able to use in solving the new problem instance"*

WHY IT DOES NOT TRANSFER — stated as a `no` rather than stretched into a `partial`:

- **Wrong currency.** Our (B) is *titanium and builder-rounds*: is it cheaper to
  rebuild the one destroyed conveyor (3 Ti, one builder action, +1% scale) or to
  lay a new route around it? Nebel and Koehler measure **worst-case computational
  complexity and planner runtime**. The result is about how hard the *search* is,
  not about what the *actions* cost. No arithmetic in the paper converts.
- **Wrong failure mode.** Their "old plan" is invalidated by a changed goal or a
  changed initial state. Ours is invalidated by **20 HP of conveyor being shot
  off**, with the rest of the route intact and still correct. That is the easiest
  possible case for repair and the paper's hard cases are elsewhere.
- **The retrieval bottleneck does not exist here.** The paper's central practical
  warning is that *finding* the right plan to reuse costs more than reusing it
  saves. **We have exactly one route per harvester and we know where it is.** The
  bottleneck the paper identifies is the part of the problem our ruleset deletes.
- **And the one place it might have paid, the library already has better.** Sweep
  18's [`classify-the-disruption-before-you-replan`](classify-the-disruption-before-you-replan.md)
  records a competitive-league instance of the same idea with a measured
  consequence — replanning from scratch on every disruption produced an infinite
  restart loop and lost the matchup. **That is a game-league source with an
  outcome attached; this is a complexity theorem.** Prefer the former.

WHAT WOULD KILL THE `no` — i.e. what would make me refile this as `partial`: a
demonstration that our 10 ms per unit per turn is actually binding on route
recomputation. If a builder cannot afford to re-derive a route from scratch inside
its budget, then the *computational* reuse question becomes our question too, and
the paper's warning (reuse is not provably cheaper; the retrieval is the cost)
becomes live guidance. **Nobody has measured our route-planning cost against the
budget, so this is an open condition, not a claim.**

BUILDER HOOK — none from this source. The one thing it argues against is building
a plan library and a matcher; the shape it argues for is the one sweep 18 already
landed on independently — **patch in place, do not regenerate.**

---

**Method note — a NEW trap for the library's list, and it is a false-negative
generator.** This 1995 LaTeX PDF has no `ToUnicode` map for its ligatures, so
`pdftotext` (with or without `-enc UTF-8`; no second extractor was available on
this machine) **silently drops `fi`, `ffi` and `ff` entirely**: `efficiency`
extracts as `eciency`, `modification` as `modi cation`, `difficult` as `dicult`,
`offer` as `o er`, `finding` as `nding`. **A literal grep for the true string
returns zero on every one of those words** — the exact false-negative shape the
whole verification procedure exists to prevent, and it is invisible unless you
read the extracted text rather than only grepping it. **The disciplined response is
the existing no-elision rule applied to word boundaries: quote only ligature-free
spans, and state the extraction artifact explicitly rather than "correcting" the
extraction back to what you believe the source says.** Correcting it would be
paraphrase-into-unmarked-text, which is this library's documented recurring failure.
