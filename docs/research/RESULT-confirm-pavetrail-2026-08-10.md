# RESULT — THE CONFIRMATORY TEST. **NOT CONFIRMED.**

Prereg `docs/prereg/PREREG-confirm-pavetrail-2026-08-10.md`, committed
**08:22:30Z** before the arm's first window. It declared itself **THE single
confirmatory test at a fixed n=100**, with no early stop and no extension.
**n=100 has been reached and this is the one read.**

## The number

    CONTROL  v104 "Loki v2"   81/150 = 54.0%   CI 46.0-61.8
    ARM      v102 (parent)    47/100 = 47.0%   CI 37.5-56.7
    delta -7.0pp     Fisher exact two-sided p = 0.3030

**PREDICTION WAS -18pp. OBSERVED -7.0pp, interval includes zero.**

**The pre-registered bar was: "CONFIRMED if v102 is worse than v104 by a margin
whose two-sided interval excludes zero." It does not.**

## THE SHIP'S EVIDENCE DID NOT REPLICATE.

Writing the sentence the prereg pre-committed me to write. **The +18.0pp that
justified shipping v104 does not reproduce as a pre-registered test.** What
reproduces is a **-7.0pp shadow of it, not distinguishable from zero.**

**This is exactly what the prereg existed to detect**, and it is the outcome
that the original evidence's weaknesses predicted: the +18.0pp was pooled into
significance after a null, its honest family-wise p was **~0.05 not 0.016**, and
its per-opponent split showed three of five cells with seat differences.

**What is NOT established:** that v104 is worse than v102. The direction still
favours v104 by 7pp; the leg simply cannot distinguish that from chance.
**"Not confirmed" is not "refuted".**

## AND THE MECHANISM STORY IS NOW DOUBLY DEAD

The sister arm settles the *why* question in the opposite direction to the
plank's own thesis:

    LOKI-15 (hard per-builder conveyor quota)  59/150 = 39.3%
    vs control                                 81/150 = 54.0%
    delta -14.7pp   Fisher p = 0.0149   ** SIGNIFICANT NEGATIVE **

**Cutting the economy hard MAKES US WORSE, significantly.** So the theory that
v104 gains by suppressing economy is refuted from the other side as well —
LOKI-13's own conveyor bar had already failed (0.86x against <=0.70x), and now
a treatment that genuinely does cut economy is measurably harmful.

**v104 remains better than its parent by an unconfirmed 7pp, for reasons that
are now positively NOT economy suppression.**

## THE COUNTER-EVIDENCE, stated because it is real and points the other way

**On the rated ladder v104 has gone 1615 -> 1666, +51, rank #28 -> #25**, its
best run of the session. That is a different population (the whole field, not a
five-team panel) and it is uncontrolled — opponents differ, seats differ,
nothing is paired. **It is not evidence that survives a prereg. But it is not
nothing, and a rollback decision should not pretend it is.**

## THE ROLLBACK QUESTION — MAGNUS'S CALL, PUT PLAINLY

The prereg pre-committed that a non-confirmation goes to Magnus rather than
being quietly dropped. The honest options:

1. **HOLD v104.** Its ladder run is strong, the panel direction still favours it,
   and "not confirmed" is not "refuted". **Cost: we are flying a bot whose
   claimed advantage failed its own confirmatory test.**
2. **ROLL BACK to v102.** Defensible on the prereg alone. **Cost: gives up a
   +51 ladder run on a panel result that is itself only p=0.30 in the other
   direction — i.e. rolling back on evidence no stronger than what shipped it.**
3. **HOLD AND KEEP MEASURING.** Windows are free; the control arm keeps growing
   and the confirm arm could be re-run as a fresh pre-registered test at larger
   n. **Cost: nothing but wall-clock, and it is the only option that ends with
   an answer.**

**My recommendation is (3), and I want to be explicit that it is not the
comfortable-middle choice.** Option 1 ignores a failed test; option 2 acts on a
p=0.30. **Option 3 is the only one that treats the panel as a two-cell
instrument that has now twice failed to resolve an 18pp claim** — which is the
actual finding here, and it is about the fixture, not the bot.
