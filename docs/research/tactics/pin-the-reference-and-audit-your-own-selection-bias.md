---
tactic: test every patch against ONE frozen released reference, and audit the gap between summed patch gains and the measured end-to-end delta
source: https://github.com/official-stockfish/Stockfish/wiki/Regression-Tests · https://official-stockfish.github.io/docs/fishtest-wiki/Fishtest-FAQ.html
origin: Stockfish / Fishtest, 2013-2026
evidence: documented (first-party project documentation; the regression page IS the data)
transfers: partial
---
WHAT IT IS — The most disciplined answer to "what do I compare against" in any competitive
software project. Every progression test runs against **one frozen released version**, never
against current master and never against the current best. Measured on the flat page
(`lad_sf_regression.flat`): the literal string `master vs Stockfish 17` occurs **30** times,
`master vs Stockfish 16` **27** times, `master vs Stockfish 4` **26** times. The page also
versions the *test conditions themselves* with explicit date ranges — a "Current Testing
Criteria" block and a **"Previous Testing Criteria"** block, e.g. "8moves_v3.pgn opening book
(2013-11-09 - 2023-06-29)" — so an old number can be re-scoped rather than silently compared
to a new one.

**AND THE PROJECT DOCUMENTS ITS OWN SELECTION BIAS, WHICH IS THE PART WE CAN ACT ON**
(`lad_fish_faq.flat`):

> "Elo estimates of single patches (SPRT runs) typically come with large error bars. Take
> this into account when adding Elo estimates. Furthermore, Elo's estimates of passing
> patches are biased. The SPRT Elo estimates are only unbiased if one takes all patches into
> account, both passed and non-passed ones. As a result, the Elo gain measured by a
> regression test will typically be less than the sum of the estimated Elo gains of the
> individual patches since the previous regression test."

WHY IT MIGHT TRANSFER — **two things, and the second is a concrete audit we can run this
week.**

1. **A conditions header on every leg.** Our prereg pins `ourver` and nothing pins theirs.
   Stockfish's doctrine is that the comparator is *a pinned artifact plus a dated condition
   block*. Ours would be: opponent ids, each opponent's version **as read at the pairing
   boundary**, our version, and the window — stored with the result, so that a later pooling
   is a deliberate act rather than the default. That is the cheap half and it costs nothing.

2. **THE SELECTION-BIAS AUDIT.** We ship planks that passed their own legs, and we have both
   halves of Fishtest's check: sum the claimed per-plank gains since an anchor, then measure
   the anchor-to-now rating delta directly from the elo tape and per-match `ourver`. **The
   gap is our selection bias, in rating points.** It also formalises why owning nulls cheaply
   is not merely good manners — the nulls are load-bearing for unbiasedness, and a pipeline
   that only records passes cannot produce an unbiased estimate of anything.

WHAT WOULD KILL IT — **the mechanism does not transfer at all; only the method does.** We
cannot freeze the ladder, cannot replay a fixed opponent, and cannot run 60,000 games. A
pinned reference buys **comparability between our own legs** and nothing more; it cannot
tell us whether the field moved, which is the question that actually bit us — that one needs
`anchor-on-opponents-who-did-not-change.md`. The two are complements, not substitutes.

**AND ONE QUOTE FROM THIS SOURCE MUST NOT BE GENERALISED.** The FAQ also says:

> "Do not run tests of master vs an earlier version. This may give misleading results as it
> favors the current book. This effect (selection bias) has been shown to exist several
> times."

**Referent — and it inverts the apparent meaning.** That sentence sits inside a procedure
headed **"How to compare opening books"**. Its subject is a *book-comparison* methodology:
when the thing under test is the fixture, master-vs-old-version is an invalid yardstick
because master was selected *on that book*. "The current book" is the book used for routine
testing. **It is NOT a blanket prohibition on regression tests** — the same project runs 30
`master vs Stockfish 17` tests on the very page quoted above. Reading it as general doctrine
would be exactly the "this timeout" error.

Correctly scoped, it names a hazard we *are* exposed to: substitute "opening book" → "the
opponent panel we selected cells on". **A plank tuned on a panel must be confirmed on a
panel it was not selected on**, or its measured gain is partly the panel. The related
first-party statement — "Selection bias is a book-related effect, patches are more likely to
be selected if they perform well with the testing book. When they are retested with a
different book their Elo score may be adversely affected." — is the general form.

BUILDER HOOK — smallest first: add the conditions header to the prereg template (opponent
ids + their versions at the pairing boundary + our version + window). Then run the audit —
sum the claimed gains of every plank shipped since a chosen anchor version, compare to the
anchor-to-now delta measured off per-match `ourver`, and report the gap. Neither needs a
single match played.
