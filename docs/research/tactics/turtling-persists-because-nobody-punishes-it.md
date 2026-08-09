---
tactic: THE GUARD RAIL — the one author in this corpus who ships a bot to a BOT LADDER says heavy static defence is prevalent there because opponents fail to adapt, not because it is strong
source: http://satirist.org/ai/starcraft/blog/archives/353-turtle-strategies.html
origin: Jay Scott (satirist.org), author of the Steamhammer StarCraft bot
evidence: documented
transfers: yes
---

## WHAT IT IS

Every "the top tier does X" reading in this sweep rests on statistics gathered from a
**ladder of bots**. Jay Scott — who writes the AI-vs-AI StarCraft blog and ships
Steamhammer into exactly that kind of population — states the confound directly:

> *"But there is a reason that so many bots play turtle strategies. Turtling is strong
> against bots which do not adapt, which is most of them. For Steamhammer, I added 1 base
> and 2 base turtle openings which crush Wuli, an opponent that Steamhammer otherwise
> struggles against. Wuli does not adapt."*

He separately gives the *correct* valuation of static defence against an opponent that
does adapt:

> *"Static defense can't go attack; it costs resources and it offers initiative to the
> opponent. In a well-played game, static defense has to pay for itself with a
> countervailing advantage: You have to use the temporary safety it brings to get ahead in
> economy, as in a protoss forge-expand opening or as Killerbot by Marian Devecka"*

and the discipline that follows:

> *"You can beat it with a turtle strategy, but only by exploiting weaknesses. The reaction
> to static defense is not a weakness."*

*(Glyph note for anyone re-grepping: satirist.org uses **curly** apostrophes — `can’t`,
not `can't`. The ASCII form does not match.)*

## WHY IT MATTERS — against our situation specifically

**We are a bot on a bot ladder measuring other bots.** Every cross-team statistic this
library holds — the 53.1/44.4/2.5 kill mix, the 66.5% vs 53.2% collar, the 40.6% at
≥1900 — is drawn from the exact population Jay Scott is describing. **His claim is that
in such a population, a structure choice can be prevalent because it is *unpunished*
rather than because it is strong.** That is the general form of the counterweight this
sweep was sent to find, from the one source with standing to make it.

**It cuts in both directions and both are useful to us:**

- **Against over-reading the top tier.** Their gunner-heavy core-kill mix might be a
  mechanism, or it might be what the field lets them get away with. Combined with the
  Agade case — where a top-three bot's tower-heavy mix was an artefact its author did not
  choose, while a rival wrote counters against it — the base rate for "observed mix =
  chosen doctrine" in this evidence class is not high. See
  [`the-tower-heavy-mix-was-an-artefact-not-a-doctrine`](the-tower-heavy-mix-was-an-artefact-not-a-doctrine.md).
- **Against over-reading our own defence.** Our home defence is the measured asset
  (+11.4 / +16.6 / +22.3pp over the field) and we win the opening and the clock and die in
  the middle. Jay Scott's valuation says static defence must *"pay for itself with a
  countervailing advantage"* and names the currency: **getting ahead in economy while
  safe.** We do get ahead — *"we already out-build the field on conveyors (+13)"* — and
  the middle game is still where we die, which on his framing means we are buying the
  safety and not spending the initiative it purchases.

**The third quote is the most operationally useful and the easiest to misapply.** *"The
reaction to static defense is not a weakness"* — an opponent responding correctly to our
turrets is not an exploitable habit. This library's `play-the-players` mandate is about
measured opponent *habits*; a proportionate response to a threat is not one, and should not
be logged as an exploit.

## WHAT WOULD KILL IT

- **It is an expert practitioner's assertion about the StarCraft bot ladder, with an
  anecdote (Wuli) rather than a measurement.** It is `documented` as his stated view; it
  is not a study.
- **His ladder is not ours.** SC/BW bots are far more heterogeneous than a single-game
  league's field, and "most of them do not adapt" may be much less true of a top tier
  400-500 Elo above us — indeed sweep 16 found the opposite property in that band (at a
  400-Elo gap, *perfect opponent modelling bought nothing*, which suggests the stronger
  side is not the one failing to adapt).
- **This file argues for scepticism, not for inaction.** Read as a general licence to
  ignore field statistics it would disable the only instrument we have. The correct use is
  narrow: **before a mix change justified by an opponent's observed composition, ask what
  would punish that composition and whether anyone in the field is doing it.**

## BUILDER HOOK

None in code. The procedural form, and it is one line added to any mix proposal:
**name the punishment.** If the top tier's gunner-heavy mix is a mechanism, there is
something a gunner does that a sentinel cannot, and it should be nameable before we build
toward it. If the only answer is "they have more of them", the finding is a marker and the
proposal is the garrison error again.
