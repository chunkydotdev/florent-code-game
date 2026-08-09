---
tactic: Self-play A/B against your own past versions measures the wrong population — and the BC2025 winner shipped against its own A/B twice and won
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 Just Woke Up (tournament winner); corroborated by BC2023 4 Musketeers, BC2023 no thoughts, BC2024 cout for clout
evidence: documented
transfers: yes
---

## WHAT IT IS

The field's standard experimental instrument is a scripted A/B against your own earlier
bots. Its adoption is documented as a competitive advantage:

> *"At the final tournament we found out that many top teams had built up custom systems for
> quickly running many matches in parallel for A/B testing."* — BC2023 no thoughts

> *"we would have one of the teammates run that version against all previous versions
> locally"* — BC2023 4 Musketeers, describing their pre-automation workflow

> *"enabled me to AB test two bots on every single map I had at my disposal"* — BC2025 Just
> Woke Up

And the **BC2025 winner explicitly recorded its limitation, twice, and shipped against it
both times.**

Case 1 — defence towers:

> *"When we performed AB testing against our past bots, and using defense towers did not
> seem to be very good… Against our past bots it usually went even in wins, or even slightly
> lost. But our bot wasn’t super aggressive, and we believed that this, in theory, SHOULD be
> better against the teams that we have the worst matchups against."*

**Referent check.** "our past bots" are Just Woke Up's own earlier versions; "the teams that
we have the worst matchups against" are named in the same document as the *"hyper aggressive"*
teams they struggled with — the preceding paragraph reads *"we knew that we needed to do
something to counter some of the hyper aggressive"* … *"teams that we often struggled
against in scrimmages and in past tournaments"* (a page number is interpolated between the
two fragments by the PDF extraction). The stated defect in the instrument is that **the
self-play pool does not contain the opponent behaviour the feature is designed to counter.**
The outcome, in their words: *"So we sent it, and the results were unbelievable."*

Case 2 — mopper resurrection, the same reasoning applied a second time:

> *"Even though in our AB tests the results of rezzing seemed to be not super meaningful, we
> agreed that it was a feature we believed should make our bot better, and even if the
> numbers against our own bots did not show it, we thought it would work better against
> other teams."*

**The counter-example — what a controlled test looks like when it works.** BC2024 cout for
clout isolated a single variable and got an unambiguous read:

> *"By doing a simple test of 47 vs 50 ducks, we found that the version with 47 lost 90% of
> the games, and it wasn’t even close."*

**Referent check.** The passage is about the "sitting duck" strategy — three units parked on
the spawn — and the surrounding sentence is *"Turns out, using 3 ducks to sit on your spawn
makes you lose just about every micro battle."* The comparison is unit-count-vs-unit-count
with everything else held fixed; it is a *mechanism* test, not a strategy test, which is why
it survives the population objection.

The same team's strategy-level evidence is, by contrast, an uncontrolled before/after:

> *"Instead we decided to be even less defensive and go full aggro – making our micro as
> aggressive as possible. This improved our rating a whopping 130 points (from 1720 to
> 1850)."*

## WHY IT MIGHT TRANSFER

It transfers directly and it **corroborates a standing project rule from outside the
project**: *benchmark vs field, not self* — ship verdicts weigh the class-weighted vs-field
battery, self-legs are for attribution only.

The mechanism Just Woke Up names is precisely our situation on the contact question. The
feature under consideration is a **trigger keyed to an opponent's early behaviour**. Our
self-play pool is Loki against Loki (and Eir), which:

- opens as a near-constant (our r0-50 builder-bot **CV 0.09 against opponents' 0.26**), so
  the trigger sees almost no variation in the input it is designed to read;
- is dominated 87-90% by both arms, so win rate cannot resolve it — which `PROGRAMME.md`
  already encodes as `WIN_RATE_IS_VERDICT: no`.

A contact trigger tested against ourselves is being asked to discriminate a distribution
that our own measurement says is **flat**. Just Woke Up's failure mode is not a risk for us;
it is the guaranteed outcome.

The constructive half is cout for clout's shape: **when the question is a mechanism, hold
everything fixed but one number and the self-play pool is fine.** "Does N=2 sentinels out-
damage the heal rate on this tile" is a 47-vs-50-ducks question. "Should we commit on this
trigger" is not.

## WHAT WOULD KILL IT

- **"Ship against your A/B" is survivorship evidence.** Just Woke Up won, so their two
  overrides are remembered. Teams who overrode a null A/B on a hunch and lost did not write
  a postmortem. Read this as *the instrument has a known population defect*, **not** as
  *override your instrument when you feel strongly*.
- Their arbitrariness is stated by the authors: the defence-tower conditions were *"kind of
  arbitrary, and they were, but that's what seemed to work best for us."*
- Our ladder is a shared, moving field, so the "before/after rating" instrument that BC teams
  fall back on is even noisier for us than for them — our own slot-swap rule already
  encodes this (arms at ≥8, net ≤ −21 frees the slot; the slot is stop-loss and wake, **not**
  an n=8 evaluation).

## BUILDER HOOK

None in the bot. The hook is in the **battery design**: a contact trigger must be measured
against the **field**, in a pool containing opponents whose early economy actually varies —
because the trigger's input is exactly the thing our self-play pool holds constant.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
- https://battlecode.org/assets/files/postmortem-2023-no-thoughts.pdf
- https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
- https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
