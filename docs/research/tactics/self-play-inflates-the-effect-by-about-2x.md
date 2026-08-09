---
tactic: Self-play measures roughly twice the true field effect — one competitor measured both instruments on the same feature, and published a mitigation
source: https://raw.githubusercontent.com/Agade09/Agade-Fall2020-Challenge-Postmortem/master/README.md
origin: CodinGame (Agade, multiple contests) and Halite II (reCurse, 1st place)
evidence: documented
transfers: yes
---

## WHAT IT IS

`self-play-ab-has-the-wrong-population.md` records that the BC2025 winner overrode its own
self-play A/B twice and won. This file is the harder version of the same finding: someone
measured **the same feature on both instruments** and published both numbers.

**Agade, CodinGame Fall 2020 Challenge — the same feature, two instruments:**

> *"Locally, in self-play, amputating this opponent modelling causes a loss of ~30% in
> winrate."*

> *"I used [CGBench](https://github.com/s-vivien/CGBenchmark) to double check the value of this
> specific feature because self-play evaluation is risky when it comes to opponent
> prediction."*

> *"Against other players the impact was not as dramatic but it was there, very roughly ~15%
> seen with CGBench."*

**Referent check.** *"this opponent modelling"* is his bot simulating the opponent's action
choices rather than assuming they idle; CGBench is a harness that plays a submission against
**other players' bots** rather than against itself. **30% self-play, ~15% versus the field —
a factor of two, on a real effect, in the same direction.** The instrument does not invert the
sign; it inflates the magnitude.

**The mechanism, named by the same author in a different contest:**

> *"I learned from GitC that the win rate you get in self play is often exaggerated because in
> the extreme case you'll play a bot against itself, minus a mistake, and win all the time."*

**Referent check.** GitC = Ghost in the Cell, which he won using a purely self-play-driven
workflow. The stated consequence: *"So a lesson I learned from GitC was to try and focus on big
features first and not waste too much time on supposedly 1% coefficient changes that are
actually worth 0.1% in the arena."*

**The bias has a name and a published mitigation:**

> *"One might argue that judging AIs against the previous version has risks of specialisation.
> And it's true."*

> *"In order to avoid specialisation against myself, I sometimes disabled guessing bomb targets
> in my tests, because I'm obviously really good at guessing my own bombs."*

**Referent check.** *"guessing bomb targets"* is his opponent-modelling module. The mitigation
is to **amputate, during self-play measurement, the module whose accuracy is inflated by the
opponent being a copy of yourself.**

**And non-transitivity, measured by the same author:**

> *"It was interesting to see that sometimes, playing better against a good AI makes you not as
> dominating against a weaker AI."*

**The Halite II winner reaches the same verdict independently and more bluntly:**

> *"Local testing against previous versions was helpful in the beginning, but the exercise
> became increasingly inaccurate and pointless over time."*

> *"I often had versions performing much better online while still performing poorly against
> the previous version."*

His stated top instrument is the opposite one — a per-opponent breakdown of **ladder** games:

> *"Statistics breakdown of the performance of a bot version online. By far the #1 way to
> evaluate the impact of changes!"*

Two null results he accepted from that instrument, both on aggression-related features, are
worth recording as the discipline in action: *"No prediction was done for the enemy as no
behavior or ranking improvement could be found, sometimes even being detrimental"* and, on an
offence-focusing feature whose replays looked bad but whose measurement was good, *"every time
I tried removing this masking, my bot performed worse overall."*

## WHY IT MIGHT TRANSFER

It transfers as **calibration**, which is a thing this project can use immediately.

- Our probe pool is dominated 87-90% by both arms, which `PROGRAMME.md` already encodes as
  `WIN_RATE_IS_VERDICT: no` — the *"bot against itself, minus a mistake"* case exactly.
- The ~2× inflation factor gives a prior for reading self-legs: a self-play delta should be
  discounted, not merely caveated, before it is compared to a field battery.
- **The amputation trick is directly applicable and cheap.** Any Loki feature that reads the
  opponent's behaviour — a contact trigger above all — is a module whose accuracy is inflated
  when the opponent is our own bot with our own near-constant opening (our r0-50 builder-bot
  **CV 0.09 against opponents' 0.26**). Agade's fix is to *turn that module off in the
  self-play leg* so the leg measures only what it can honestly measure.
- reCurse's verdict — ladder-versus-field breakdown above local self-play — is the same rule
  this project already holds (*benchmark vs field, not self*; the ladder is the field
  instrument, rollback is the control). It is now sourced twice from outside.

## WHAT WOULD KILL IT

- **One number, one contest, one feature.** 30% versus 15% is a single measurement by a single
  author. It is the only two-instrument comparison this sweep found anywhere, which makes it
  valuable and also unreplicated. Treat 2× as an order of magnitude, not a coefficient.
- **CGBench-style measurement against other people's bots is not available to us in the same
  form.** Our nearest equivalent is the class-weighted vs-field battery and the ladder itself,
  both slower and noisier than a local harness.
- **Non-transitivity cuts both ways** and makes "the field" itself a moving target: Agade's own
  observation is that improving against strong opponents can *reduce* dominance over weak ones,
  so a single aggregate field number can hide a sign flip by band.
- **This says nothing about cause versus marker.** It is about *which population you measure
  in*, not about confounding within a bot's own policy. See
  `nobody-separated-cause-from-marker.md` — that question remains unanswered by anyone.

## BUILDER HOOK

None in the bot; the hook is in the battery. When a contact trigger is measured on a self leg,
**run the leg with the trigger's opponent-reading input pinned to a constant** (Agade's
amputation), so the self-play number reports what the *action* is worth rather than what our
own predictability is worth. And read any self-play delta as roughly double the field delta
until we have our own two-instrument comparison.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/Agade09/Agade-Fall2020-Challenge-Postmortem/master/README.md
- https://raw.githubusercontent.com/Agade09/Agade-Coders-of-the-Caribbean-Postmortem/master/Agade_CotC_Postmortem.md
- https://raw.githubusercontent.com/Agade09/Agade-Ghost-in-the-Cell-Postmortem/master/Agade_GitC_Postmortem.md
- https://web.archive.org/web/20250912062821/https://recursive.cc/blog/halite-ii-post-mortem.html
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
