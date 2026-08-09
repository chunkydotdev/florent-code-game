---
tactic: (B) THE UNCOMFORTABLE HALF — a bot that deliberately never finishes took 3rd in its contest, a 3rd-place bot won mostly on the tiebreak, and the obvious "know if you are ahead" fix is reported to have repeatedly failed
source: http://satirist.org/ai/planetwars/playing-styles.html
origin: Planet Wars 2010 (Slin, #3; wagstaff, #17; Jay Scott's oddshrimp); CodinGame Code Royale (Agade, 3rd)
evidence: documented
transfers: yes
---
WHAT IT IS — Sweep 17A's question (B) assumed the converter is the better bot.
The field does not agree, and the counter-evidence is strong enough that it has to
be filed beside every conversion finding in this sweep.

**A top-3 bot that refused to convert, on purpose.** Jay Scott on Slin, which
placed 3rd in Planet Wars 2010:

> *"Slin does not want to wipe you out. Slin wants to get solidly ahead and lock
> you in a wrestling hold that you can’t break, and then it is content to wait for
> the game to run out. It avoids the risk of going wrong in a finishing attack, a
> serious problem for other bots against oddshrimp4.1."*

Referent: "It" is Slin; the "serious problem" is *going wrong in a finishing
attack*, which he attributes to other bots. This is a third-party characterisation,
not Slin's author's own words — flagged, because that matters.

**A 3rd-place bot in a kill-condition game winning mostly on the tiebreak.** Agade,
Code Royale:

> *"In effect I won my games in two ways: getting in some initial damage to the
> enemy queen in the opening and then "drawing out" the game with a lot of towers
> (although I didn't implement any extra hiding if I had an HP advantage), or
> sometimes grabbing so much territory that the enemy had nothing left"*

> *"At the higher levels a lot of games were won simply by having 1 more HP than
> the opponent"*

**And the obvious fix is reported to have failed repeatedly, by a competent
author.** Jay Scott, in the entry on wagstaff — a bot that *did* implement
standing-awareness and finished 17th (*"It is acutely aware of whether it is ahead
or behind."*):

> *"Curiously, my tries to improve oddshrimp by making it aware of when it is
> ahead or behind have never come to much."*

The counterweight, from the same author about his own bot, so the file is not
one-sided:

> *"It has the killer instinct. When it gets a decisive advantage it finishes off
> the opponent quickly and viciously"*

> *"Many contestants, even much stronger ones, were satisfied to exploit advantages
> slowly and look milquetoast in comparison."*

(The two are separated in the source by the parenthetical *"(well, as viciously as
it can when launching against only one enemy planet per turn)"* — they are not
contiguous.)

WHY IT MATTERS HERE — Our own numbers put us on Slin's side of this argument, and
the file exists so that is a *decision* rather than an oversight. We reach r1000 in
353 games and **win 57.2% of them**. Conditional on a core kill happening, the odds
it is ours climb to 72-76% in the late game. We are, measurably, good at the
wrestling hold.

Two consequences follow and they pull in opposite directions, which is the honest
state of the evidence:

1. **Raising incidence is not automatically raising win rate.** Every titanium
   moved from the pipeline to the assault is moved off tiebreak key 1, which is the
   road we currently win. An incidence gain that costs tiebreak win rate can be net
   negative, and no A/B that measures only `core_kill_share` would see it. **Any
   incidence experiment must report win rate and tiebreak win rate alongside.**
2. **"Be aware of whether you are ahead" is the specific fix that is reported not
   to work.** That is directly relevant, because it is the most natural way to
   write a commit gate. Jay Scott's report is one author's experience and not a
   measurement — but it is the *only* report either way, and it is negative.

WHAT WOULD KILL IT — Slin was 3rd, not 1st; Agade was 3rd, not 1st. In both
contests the winner was a bot that could finish. And Planet Wars' "draw" is
*exactly equal ship counts at turn 200*, not "reached the turn limit" — so Slin's
wrestling hold produced a **win** on ship count, which is a much more decisive
tiebreak than ours. Our tiebreak includes an actual coinflip; theirs effectively
did not.

The strongest thing that would kill it is our own data: if the 57.2% collapses
against ≥1900 opponents, then the wrestling hold works only on the field we
already beat, and grinding is not a strategy — it is a symptom. That cut has not
been run and is flagged in
[`a-rising-hazard-makes-every-game-decisive`](a-rising-hazard-makes-every-game-decisive.md)
as the cheapest measurement in this sweep.

BUILDER HOOK — None in the bot. A gate on the *process*: any experiment aimed at
core-kill incidence reports three numbers, not one — win rate, `core_kill_share`,
and win rate among games reaching r1000. If the third falls while the second
rises, the change is trading our best road for our showiest one.
