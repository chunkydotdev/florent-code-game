---
tactic: What the field explicitly WARNED AGAINST — four independent sources removed or delayed early aggression and measured a gain
source: https://raw.githubusercontent.com/Agade09/Agade-Code-Royale-Postmortem/master/Agade_CR_Postmortem.md
origin: CodinGame Code Royale (Agade, 3rd); Halite III TheDuck314 (6th); Halite II rooklift and reCurse (1st)
evidence: documented
transfers: partial
---

## WHAT IT IS

The brief asked what sources *explicitly warned against*. Four did, in four different games,
and three of them report a measured gain from **removing** early aggression.

**1. Agade (Code Royale) flipped the sign of a placement term specifically to make his opening
less aggressive, and gained rating:**

> *"in the early game for the first wave of knights because I was sick of losing to my AI
> simply being too aggressive and losing HP in the early game. This gained a lot of trueskill
> points."*

**Referent check.** The preceding sentence reads *"On Monday morning I added a hack to change
`-Dist_To_Enemy(Site)` to `+Dist_To_Enemy(Site)`"* — the flip makes his queen prefer building
sites **far from** the enemy during the first knight wave. *"my AI"* is his own bot; the loss
being avoided is HP, not units.

**2. TheDuck314 (Halite III) gates ramming on game phase, and states the reason:**

> *"we only start ramming late in the game, since early in the game it's probably better to
> keep our ships alive"*

**Referent check.** *"we"* is his bot in 4-player games, contrasted in the same list with its
2-player rules — *"the conditions for ramming are stricter"* and *"we are much less likely to
actively run away from enemy ships"*.

**3. rooklift — the author of a rush theory whose bot went 1279-176 in 2-player rush games —
refuses to rush at all in the other format:**

> *"I never rush in 4 player games. In fact, I dock without even looking at the opponent."*

**Referent check.** The reason given is a payoff structure, not tactical weakness: *"if I rush
my opponent, and he defends adequately, we are likely to get 3rd and 4th. If we both play
normally, we might both get a chance at 1st or 2nd."* He still defends — *"I do defend though,
by detecting incoming ships at the earliest moment when undocking is possible."*

**4. reCurse (Halite II winner) gates his give-up-and-survive mode behind a round number
*because early evidence is not diagnostic*:**

> *"More than 60 turns have elapsed, to avoid early aggression being seen as apocalyptic."*

**Referent check.** This is one of several ANDed conditions for entering "survival mode"; the
others include *"For all owned planets, the number of enemy undocked ships exceeds the number
of allied undocked ships by more than 3 in a radius of 50"*. The stated worry is that **an
early aggression signal, read literally, produces a wrong strategic conclusion.**

And the abort condition on rooklift's own safe-engagement doctrine, which is the mirror image —
sometimes safety is what loses:

> *"Our theory is great if we can get into the right situation fast enough. But if the enemy is
> docked, he will be producing ships soon and we will lose; so we must use more aggressive
> play, ignoring our theory."*

## WHY IT MIGHT TRANSFER

Read against `PROGRAMME.md`, this is the counter-evidence file, and it should be read as
counter-evidence rather than filed and forgotten. Three points survive translation:

- **reCurse's warning is directly about the trap our own cut names.** Our best runtime signal
  (`US_shot_w50`) is an *early aggression reading*, and the cut says plainly it is *"a marker,
  not a proven dial"*. reCurse independently concluded that early aggression signals mislead —
  in his case in the pessimistic direction — and dealt with it by refusing to act on them
  before turn 60. That is a real design option for us: **read the signal, delay acting on it**.
- **Agade's is the only measured before/after on removing early aggression** found in this
  sweep, and the sign is against aggression. It is a ladder-rating claim with no control, so it
  is weak evidence — but it is the same evidence class as every pro-aggression claim in this
  library, including sweep 14's.
- **rooklift's rule is about payoff structure, not strength.** In a 1v1 with a core-kill win
  condition, his 2-player reasoning applies to us and his 4-player reasoning does not. That is
  the honest reading, and it is *favourable* to the programme.

## WHAT WOULD KILL IT

- **Three of the four warnings are format-specific (4-player free-for-all).** Halite II and III
  4p games have a placement payoff and a prisoner's-dilemma structure that **does not exist in
  our 1v1 core-kill game**. rooklift's and TheDuck314's warnings largely evaporate on
  translation, and that must be said plainly rather than used to argue against the programme.
- **Agade's Code Royale gain is uncontrolled** — a hack shipped on a Monday morning, judged on
  TrueSkill movement, with other changes in flight.
- **None of these warnings is about a *triggered* commitment.** Every one is about
  **unconditional** early aggression. Sweep 14's central finding — that deadline attacks
  converted **only** as conditional fallbacks keyed to a scouting trigger — is untouched by all
  four, and reCurse's own bot *does* rush on a trigger (*"rushes if it owns no planet but the
  enemy does"*).
- Our library's standing counter-fact stands: BC2020 and BC2023 were offence-dominant seasons
  in this engine's own family. The precondition we lack is cheap mobile continuously-producible
  damage, not permission.

## BUILDER HOOK

None directly. The usable design is reCurse's: **compute the early-contact signal from round 0
and log it, but do not let it change behaviour before a floor round.** That separates "is the
signal readable" from "is acting on it early correct" — two questions our own cut cannot
separate observationally, and which cost one constant to separate in the arena.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/Agade09/Agade-Code-Royale-Postmortem/master/Agade_CR_Postmortem.md
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
- https://raw.githubusercontent.com/rooklift/halite2_rush_theory/master/README.md
- https://web.archive.org/web/20250912062821/https://recursive.cc/blog/halite-ii-post-mortem.html

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
