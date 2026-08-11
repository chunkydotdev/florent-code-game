---
tactic: CIAO matrix — score our versions against THEIR versions as a matrix, never as a column mean
source: https://seis.bristol.ac.uk/~cszjpc/pubs/04adap.pdf
origin: Cliff & Miller, "Tracking the Red Queen", ECAL 1995 — as reported and critiqued by Cartlidge & Bullock, Adaptive Behavior 12(2), 2004
evidence: documented (the technique and its measured ambiguity); see PROVENANCE below
transfers: partial
---
WHAT IT IS — When both sides of a competition are improving, a fitness number measured
against "the current population" is not comparable across time. Cliff & Miller's answer
was to stop reporting a number and report a **matrix**: current individual on one axis,
*every ancestral opponent* on the other, each cell shaded with the result. Progress reads
as a smooth diagonal gradient; cycling reads as bands.

Verified verbatim (`acad_ciao_cartlidge.flat`):
> "Cliff and Miller (1995) proposed the “Current Individual versus Ancestral Opponent”
> (CIAO) plot as a visualization tool for detecting coevolutionary progress."

> "CIAO plots can be constructed by pitting the elite (i.e., best-scoring) individual from
> every generation against the elite opponent from each ancestral generation and plotting
> the results as shaded cells in a matrix."

**PROVENANCE — read before citing.** The Cliff & Miller 1995 primary could not be
obtained (Springer paywalled; Semantic Scholar reports the open-access PDF as CLOSED with
an empty URL; ResearchGate, CiteSeerX, both Sussex hosts and the authors' pages all
403/404/204'd — eleven probes logged). **Every CIAO claim here is Cartlidge & Bullock's
rendering of Cliff & Miller, not Cliff & Miller in their own words.** Attribute it that
way.

WHY IT MIGHT TRANSFER — **the matrix is the shape our data already has and the column mean
is the operation CIAO exists to prevent.** We hold both axes: our bot versions × the
opponent's per-match `teamAVersion`, from the league-wide match list. Our current
per-opponent statistic collapses that matrix to a **column mean over their versions** —
precisely the collapse Cliff & Miller built the instrument to avoid. In matrix form,
"60% of this cell came from a version they no longer run" is a *visible shape* rather than
something an analyst has to remember to ask. It is pure analysis pipeline: no agent-side
learning, nothing shipped, no rated exposure.

WHAT WOULD KILL IT — **cell sparsity, and the instrument's own measured ambiguity.**

CIAO assumes you can play any pairing on demand. We cannot: an opponent's v4 is **gone**,
and there is no `fcode match unrated <team> --version 4`. Our matrix is ragged and
upper-triangular-ish, most cells at n = 0 and the rest at n = 5. Read a diagonal gradient
off a matrix whose density is confounded with time and you have measured your own
sampling schedule.

And the instrument is not self-validating. Cartlidge & Bullock's census —
> "Of 22 plots found in the literature, 10 are tartan in nature, 8 show progress (smooth
> gradation) and 4 show no progress (a largely homogeneous plot)."

with the finding that such plots
> "suffer from ambiguity with respect to an important but rarely discussed class of cyclic
> behavior"

and the recommendation that
> "their use should be accompanied by more problem-specific analysis"

**Referent for the last two: CIAO plots as an instrument**, not the underlying runs. A
"tartan" (irregular patchwork) plot is consistent with *both* irregular cycling *and*
random drift through strategy space — the instrument cannot separate them. Nearly half the
published plots are in that unreadable state. **This is the warning label, not a footnote:**
ship the matrix only with a per-cell `n` overlay and a null model, or it will read as
progress when it is drift.

BUILDER HOOK — build the matrix read-only off `corpus/league_matches.tsv`, one per
opponent team: rows = our versions, columns = their versions ordered by debut, cells =
game share with `n`. Do not draw a conclusion from any cell with n < 5, and print the
zero cells rather than hiding them — the empty upper triangle *is* the finding about what
we can and cannot know.
