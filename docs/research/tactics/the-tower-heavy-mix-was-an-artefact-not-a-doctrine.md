---
tactic: THE COUNTERWEIGHT, DOCUMENTED — a strong bot's structure mix was an artefact of its search, the field read it as strategy, and the author says so himself
source: https://github.com/Agade09/Agade-Code-Royale-Postmortem/blob/master/Agade_CR_Postmortem.md
origin: CodinGame Code Royale — Agade (3rd); the field's misreading from Shingy (9th) in the official feedback thread
evidence: documented
transfers: yes
---

## WHAT IT IS

This sweep was told to look actively for the reading in which a top bot's observed
structure mix is a **consequence** rather than a **cause**. This is the strongest instance
found anywhere: **the author of a tower-spamming bot states that he did not choose to spam
towers, while a rival, in the same thread, wrote defensive code specifically against
"Agade's strategy of covering the map with towers".**

Agade, on why his bot built towers:

> *"But very often this was overridden by a "Knight danger" criterion, and since my search
> algorithm only builds towers that is mostly what my AI did."*

**Referent check.** *"this"* is the site-scoring path described in the preceding
sentences — *"According to this sorting the top 2 sites were fed as targets to my search
algorithm which handled the pathfinding. If I was touching a site I had some conditions on
what to build, therefore not calling the search algorithm."* So: the deliberate
build-choice branch was **very often bypassed**, and the fallback path could only produce
towers. He also names why the *deliberate* branch would have been hard anyway:

> *"Building towers is simple and safe, when you build a mine, you have to consider if it
> won't be destroyed by enemy creeps"*

and preceding it, his own verdict on the result:

> *"I believed a balanced AI, which does not only build towers, but uses some mines and
> barracks to place additional pressure on the opponent was optimal but I did not manage
> to achieve it."*

and, in his closing self-assessment: *"I'm not very proud of this AI (tower spamming,
losing alot of HP by playing daredevil in front of the enemy barracks while they were
producing,...)"*.

**Meanwhile, in the official feedback thread, Shingy (9th) writes:**

> *"This was mainly for Agade's strategy of covering the map with towers."*

**Referent check.** *"This"* is the preceding bullet, *"Try not to walk into enemy tower
range."* — i.e. a rival built a real behavioural counter to a mix its author had not
chosen and was not proud of.

## WHY IT MATTERS — against our ruleset

**This is exactly the shape of the inference the sweep was aimed at.** We measured that
against ≥1700-rated teams, cores die 53.1% to gunners and 44.4% to sentinels, against our
own 22.7 / 69.2. The tempting move is to read that as their doctrine. **Agade is a
documented case of that reading being wrong about a top-three finisher, published by the
finisher himself, and of a top-ten opponent nonetheless building against the phantom.**

**Our project has already paid for this error once** — top teams garrison thinner, we
inferred "garrison less", built it, and it was refuted 40% vs 60%
([`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md)). Agade
supplies the mechanism for how such an error gets manufactured: **a bot's output
distribution is the joint product of its intent and its code paths, and the observer sees
only the output.** A fallback branch that can build only one kind of thing produces a mix
statistic indistinguishable from a doctrine.

**A NARROW CORRECTION TO OUR OWN LIBRARY, and it should be recorded rather than buried.**
[`2026-08-09-sweep-8.md`](2026-08-09-sweep-8.md) presents Agade's site-scoring formulas —
`tower score: 11*(Max_Dist - Dist_To_Enemy(Site))/Max_Dist` versus the mine score with the
opposite sign — as the encoding of his doctrine, and that reading is **still sound for
what the formulas do: they choose WHERE.** But those same formulas are introduced in the
sentence *immediately after* the "very often overridden" admission, and they governed the
branch that was bypassed. **So the forward-ness-positive finding stands as a published
site-choice weight and must not be upgraded into "this is why Agade's bot was
tower-heavy".** Sweep 8's other three sources (robostac, ryandy, and the Screeps
material) are untouched by this.

## WHAT WOULD KILL IT

- **It does not show that the top tier's mix is *generally* an artefact** — it shows that
  one top-three bot's was, by its author's account. One documented case licenses
  *scepticism*, not a conclusion.
- Agade is describing a **search-based** bot; a rule-based bot's mix is much more likely
  to reflect intent. We do not know which shape our own top tier is.
- The self-deprecation (*"not very proud"*) is a competitor's tone, not a measurement, and
  should not be leaned on beyond the mechanical claim it accompanies.

## BUILDER HOOK

Procedural, and cheap: **before any change justified by "the top tier does X", state the
code path that would have to exist in their bot for X to be intentional, and say whether
we have any evidence it does.** For the gunner question specifically, the discriminating
observation is not the kill-share at all — it is whether their gunners are *sited*
somewhere a sentinel could not have gone (see
[`a-gunner-kill-is-a-clear-line-not-a-doctrine`](a-gunner-kill-is-a-clear-line-not-a-doctrine.md)).
If their gunners sit where either turret would work, the mix is an artefact of something
else and copying the ratio buys nothing.
