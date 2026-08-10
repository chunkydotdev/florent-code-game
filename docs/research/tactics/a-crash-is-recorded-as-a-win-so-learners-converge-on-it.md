---
tactic: (C) Crash-induction does not have to be DESIGNED — a bot that picks openings by win rate finds it on its own, because the engine scores a crash as a win
source: http://satirist.org/ai/starcraft/blog/archives/679-CIG-2018-what-Steamhammer-learned.html
origin: Jay Scott (author of Steamhammer), "CIG 2018 - what Steamhammer learned", Brood War AI ladder; engine consequence corroborated at SSCAIT (https://sscaitournament.com/index.php?action=rules) and BASIL (https://www.basil-ladder.net/rules.html)
evidence: documented
transfers: partial — the MECHANISM transfers, the LEARNING LOOP does not. Read the norms note.
---

WHAT IT IS — the sharpest single fact in sweep 21, and it is a bot author reporting on
his own bot being farmed. Steamhammer's author wrote a script to analyse its opponent-model
file after CIG 2018 and found the crash rate was opponent-dependent, not random:

> *"Steamhammer crashed in nearly half of its games in CIG 2018."*

> *"Why was Steamhammer’s crash rate higher than I expected?"*
> *(the answer clause is quoted separately because an inline link splits the string in the
> extracted text, and the library forbids eliding across a gap:)*
> *"Because many opponents learned to make Steamhammer crash"*

> *"A crash for the opponent is a win, and the bot doesn’t care how it wins, so if it can learn a plan that makes the opponent crash reliably, it will."*

> *"The stronger opponents tend to be learning bots, so Steamhammer crashed more often on average against strong opponents."*

*(Apostrophes in the source are U+2019 and are reproduced as such above — the
straight-apostrophe variants of these strings are NOT present in the source and were
checked as a negative control. The referent of "the bot" in the third quote is the
OPPONENT bot doing the learning, established by the immediately preceding sentence
"Because many opponents learned to make Steamhammer crash".)*

**Three consequences the author states, all of them load-bearing:**

1. **No intent is required.** The opponents were multi-armed-bandit opening pickers. They
   never had a "crash the enemy" module. They had a table of `opening → win rate`, the
   engine wrote a win into that table when Steamhammer died, and the bandit converged.
2. **The crash also blinds the victim's adaptation.** *"It can’t save learning data after a
   crash, so against some opponents Steamhammer had few opportunities to experiment."*
   The exploit is self-reinforcing: the victim cannot learn its way out because the act of
   losing destroys the record it would have learned from.
3. **It only appears where the opponent is otherwise competitive.**
   *"PurpleWave shut out Steamhammer. It didn’t learn to make Steamhammer crash because
   every game was a win for it anyway."* A bandit only finds the crash lever when the
   ordinary levers are not already winning.

**And it ran in the other direction in the same tournament, by the same author's account:**
*"this Locutus version had a bug when facing certain zergling timings, and Steamhammer
quickly figured out how to exploit the bug."*

**Why the engine scored it that way** — the two ladders state it as a rule, and BASIL says
its consequence is unconditional:

> SSCAIT: *"A bot loses immediately under these conditions:"* … *"If it crashes."*

> BASIL: *"A crash counts as a loss, unless both bots crash."* and
> *"Every played game is counted as “played”, even if it crashes."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The scoring premise holds here and is sharper.** An uncaught exception permanently
  destroys the unit, and we measured the field-side shape of it: **224 undamaged builder
  disappearances per 10,000 border-tile builder-rounds for four teams, against 0 in
  2,334,017 non-border builder-rounds** — while six other teams have 722,545 border
  builder-rounds and zero events. **That is the same "opponent-dependent crash rate" the
  author found, in our league, already measured.** Half the field appears to guard its
  neighbour enumeration and half does not.
- **The Loki programme wants the core dead inside 250 rounds.** A builder that vanishes is
  a builder that is not repairing, not walling, not contesting the plant — the exploitation
  half of this is on-programme (press the kill), not defensive.
- **But the mechanism that produced it there is absent here.** Those bots learned across
  ~125 games with a persistent opponent-model file. **We have 16 integers that reset every
  match and no cross-game memory whatsoever.** Anything of this shape has to be
  hand-derived from the corpus offline and hard-coded, not learned in play.

## NORMS — and this file does NOT open the road

**Our organisers' rules govern, and no other league's silence or practice is permission.**
The library's existing position stands: see
[`no-league-bans-inducing-an-opponent-timeout`](no-league-bans-inducing-an-opponent-timeout.md)
and [`cpu-timeout-induction`](cpu-timeout-induction.md), which are HELD pending an
organiser ruling. **And sweep 21 found a league that bans exactly this by name** — see
[`battlesnake-bans-degrading-the-opponent-bot-by-name`](battlesnake-bans-degrading-the-opponent-bot-by-name.md),
which weakens the "nobody bans it" line the hold was partly reasoned against. The honest
summary is now: *one comparable league prohibits it in its Code of Conduct; two Brood War
ladders score it as an ordinary win; ours is silent.* **Ask, do not ship.**

WHAT WOULD KILL IT — for us, three things, and the first is decisive on its own:

- **We have never identified a trigger.** The whole thing rests on knowing what board state
  makes a specific opponent throw. Our border-tile hazard is a *correlate* we measured from
  the outside; **we do not know that we can cause a builder to stand on a border tile**, and
  a builder walks where its own bot sends it. Until a named, reproducible mechanism exists
  there is nothing to build.
- **The bandit is the actor there, not the tactic.** Strip the learning loop and what
  remains is "some opponents crash more", which is a fact about the field, not a plank.
- **A discarded turn is not a lost game.** Even where it fired, Steamhammer still played
  half its games to completion. Nobody has shown that pushing a bot into its failure mode
  changes a result in OUR league.

BUILDER HOOK — **nothing that acts on the opponent. One thing that acts on us, and it is
free:** the border-tile hazard is the clearest measured statement that some bots in this
league die to unguarded neighbour enumeration. **Re-audit our own `get_tile_*` /
`is_tile_*` call sites against a map-border builder** — the sweep's own engine facts say
those raise off-map and out-of-vision, and `is_in_vision` plus the whole `can_*` family are
total and safe. That is the half of this file that is unambiguously ours to take.

Related: [`the-crash-win-contaminates-your-measurement-of-the-opponent`](the-crash-win-contaminates-your-measurement-of-the-opponent.md) ·
[`catch-everything-at-the-top-of-run`](catch-everything-at-the-top-of-run.md) ·
[`battlecode-destroys-the-robot-too-and-its-own-spec-says-otherwise`](battlecode-destroys-the-robot-too-and-its-own-spec-says-otherwise.md)
