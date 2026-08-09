---
tactic: (D) THE RICHEST BODY OF ORGANISER RULES ON DECISIVENESS IS IN STARCRAFT AI — an anti-stalemate timer, a tiebreak that pays for RAZINGS, abolished draws, and one organiser rule whose incentive effect is stated outright
source: https://sscaitournament.com/index.php?action=rules
origin: SSCAIT; AIIDE (Dave Churchill); IEEE CoG; BASIL (Bytekeeper), as described by Jay Scott
evidence: documented
transfers: partial
---
WHAT IT IS — Four StarCraft AI tournaments, four different pieces of endgame
legislation. Together they are the clearest picture this sweep found of what
designers actually reach for.

**SSCAIT — an explicit anti-stalemate timer, and a tiebreak that pays for
destruction.** From the rules page:

> *"The game ends automatically either after 90 in-game minutes (86400 frames) or
> when no unit dies for 5 real-world minutes. When any of that happens, the win is
> assigned to the bot that has higher in-game kills+razings score, computed as"*

(the sentence continues into a monospace span containing
`BWAPI::Player::getKillScore() + BWAPI::Player::getRazingScore()`, which is why the
quote ends where it does). Two separate levers in one sentence: **games are cut
short when nothing is dying**, and the fallback score explicitly includes
*razings* — buildings destroyed — not just unit kills. Elsewhere on the same page
the win condition is *"If it loses all the buildings."* and, flatly,
*"Draw results are no longer possible."*

**AIIDE — a frame limit and the built-in score, and nothing else.**

> *"Games will have a 'frame limit' of 86400 frames, to simulate one hour of
> gameplay. If a game goes this long, it will be stopped and the in-game score
> will be used to determine the winner."*

IEEE CoG runs the identical sentence with a different number (85714 frames; the
page notes *"※Base Rules come from AIIDE StarCraft AI Competition Rules"*), and
the 2011 AIIDE rules already had it in embryo: *"Games are timed. If the winner of
a game is undecided after 1 hour, the player with the higher Starcraft built-in
score at that point in time wins."*

**BASIL — the only source anywhere that states the incentive structure of a
decisiveness rule in one sentence.** Jay Scott, describing Bytekeeper's ladder:

> *"A peculiarity is that games run with a real time limit of 20 minutes instead
> of a game time limit, and games which run over are dropped. Authors have
> incentive to finish off the opponent when winning, and to try to drag things out
> indefinitely when losing (“I’ll hide that command center in the corner”)."*

Referent: "games which run over are dropped" — not scored, **discarded**. That is
what creates the asymmetric incentive he then names.

WHY IT MATTERS HERE — We cannot change our rules, so this is a lens rather than a
lever, and it is a sharp one. Read our own ruleset against these four and the
diagnosis is immediate:

- **We have no anti-stalemate timer.** SSCAIT cuts a game when nothing dies for
  five minutes. Our engine runs all 1000 rounds regardless, so a mutual turtle is
  fully subsidised.
- **Our tiebreak pays for ECONOMY, theirs pays for DESTRUCTION.** SSCAIT's fallback
  score is kills **plus razings**; a bot that destroys enemy structures and then
  dies can still win the tiebreak. Ours is titanium delivered → harvesters alive →
  titanium stored: **not one key rewards damage done to the opponent.** So our
  ruleset does not merely permit grinding, it *pays* for it — and that is the
  cleanest single explanation this sweep has for why our incidence is low and our
  tiebreak record is good.
- **Our fallback bottoms out in a coinflip**, which BASIL's dropped-game rule and
  SSCAIT's abolished draw both deliberately avoid.

That is worth stating as a finding rather than a complaint: **the incidence gap the
programme is aimed at is partly legislated.** Three of the four leagues here put an
explicit thumb on the scale toward finishing. Ours puts it on the other side.

WHAT WOULD KILL IT — These are tournament-operations rules for a commercial RTS
with a wall-clock cost per game; the frame limits exist to bound compute as much as
to force decisions, and none of the four pages states decisiveness as the goal. The
one that *does* state an incentive effect (BASIL) is Jay Scott's reading of
someone else's rule, not the organiser's stated intent. So "designers believed the
lever was X" is over-claiming on this evidence; what is sourced is "designers
legislated the endgame, and one experienced observer describes the resulting
incentive."

BUILDER HOOK — None in the bot. One framing consequence for the programme: since
our tiebreak keys pay nothing for damage dealt, **any measurement of an offensive
change must be against win rate, never against a proxy score** — there is no
partial credit in this ruleset for a siege that nearly worked. This is the same
warning as [`the-grinder-is-a-legitimate-strategy`](the-grinder-is-a-legitimate-strategy.md),
arrived at from the rules rather than from the field's behaviour.
