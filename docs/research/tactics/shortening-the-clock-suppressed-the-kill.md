---
tactic: (D) COUNTER-INTUITIVE — the one league that HALVED its round limit mid-season made the kill condition HARDER to reach, and pushed at least one top competitor onto the score fallback
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 (organisers), documented by wololo
evidence: documented
transfers: partial
---
WHAT IT IS — Battlecode 2021's win condition was: destroy every enemy Enlightenment
Center, otherwise the team with more votes at the round limit wins. Mid-season the
organisers cut the round limit in half.

> *"The game consisted of 3000 rounds (later changed to 1500 by Teh Devs)"*

wololo — who finished top-tier that season — records what the change did to a plan
whose whole point was to reach the **kill** condition:

> *"because of an impending rule change by Teh Devs which halved the number of
> rounds in the game. I believed that this would make my strategy non-viable since
> the slow exponential growth technique which I required would not produce enough
> conviction in time for me to be able to end the game by extermination."*

Referent check: "my strategy" is the slanderer-economy plan described in the
preceding paragraphs; "extermination" is BC2021's kill condition (destroying all
enemy ECs), as distinct from the vote win at the round limit. And the change was
not cosmetic — it cost him the ladder outright:

> *"My refusal to modify my Sprint 1 code during my development of my new code led
> to me losing every game as a result of the rule change"*

**Read the direction carefully, because it is the opposite of the intuition.** A
shorter clock does not create urgency that produces kills. The kill condition was
the one that needed *accumulation*; the score fallback was the one available
immediately. Halving the clock therefore made the **score** the realistic road and
the kill the unrealistic one. Nothing in this sweep found an organiser shortening a
clock and getting more decisive games.

WHY IT MIGHT TRANSFER — We cannot change our clock, so this is not a lever. It
transfers as a **correction to a tempting inference** about our own numbers, and
it is a correction the programme file specifically invites.

Our corpus says the probability that a core kill is *ours*, conditional on one
happening, rises monotonically 29% → 55% → 72% → 76% across r0-150 / r151-300 /
r301-600 / r601-999. The natural reading of `KILL_WINDOW_RND: 250` is that we
should compress our kills forward. wololo's case is the counter-example that says
compressing a kill plan into less time is how you *lose* the kill: the accumulation
his plan needed did not compress, it simply failed. Our kill requires accumulation
of exactly the same character — ammo bought 1:1 from titanium, turrets that must be
paid for and placed, and the +20%/+10% scale ladders — and none of that is
purchasable in fewer rounds.

This does not contradict the programme; the window is a target, not a mechanism.
It says that if the mechanism is *acceleration*, the field's one natural experiment
predicts it backfires. The lever that has evidence behind it is **incidence via
allocation** (see
[`a-standing-allocation-to-the-win-condition`](a-standing-allocation-to-the-win-condition.md)),
not compression.

WHAT WOULD KILL IT — This is one competitor's account of one rule change, and he
is describing the effect on *his own* strategy, not measuring the league's
decisiveness rate before and after. He is a hostile witness in the useful sense —
the change hurt him and he says so — but no per-season kill-rate figure exists in
the source, so the claim "the change lowered decisiveness league-wide" is **not
sourced and is not made here.** What is sourced is narrower: for one top-tier
competitor, the kill road became non-viable and the score road did not.

The other limit is that BC2021's kill condition required destroying *every* enemy
EC, including neutral ones converted mid-game, which is a far larger accumulation
than our single 500 HP core. The mechanism is the same shape; the magnitude does
not import.

BUILDER HOOK — none. This is a guardrail: any proposal that pursues the r250
window by *doing the same thing sooner* should be checked against this file. The
question to ask of such a proposal is "does the thing being accelerated actually
compress, or does it just fail earlier?"
