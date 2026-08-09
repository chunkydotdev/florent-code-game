---
tactic: (C) ANSWERED POSITIVELY, AND IT CORRECTS THIS LIBRARY — a contest WINNER commits on a bare turn number, unconditionally on whether he is ahead
source: https://raw.githubusercontent.com/robostac/cg-code-royale-postmortem/master/README.md
origin: CodinGame Code Royale / robostac (1st place)
evidence: documented
transfers: yes
---
WHAT IT IS — Code Royale is a 200-turn game whose win condition is killing the
enemy queen, with an HP tiebreak at the limit. The winner's postmortem contains
the endgame rule this sweep went looking for, and it is a **clock**:

> *"- For the last 40 turns spend gold as fast as possible - for every idle
> barracks if I can afford to train then train."*

That is turn 160 of 200 — the last 20% of the game — and it is **unconditional on
standing**: he does not check whether he is winning. It sits in a list with its
mirror at the other end of the game:

> *"- For the first 50 turns just send knights from the closest barracks to the
> enemy queen whenever possible."*

He also has a *standing*-triggered switch, and its history is instructive because
the trigger **loosened** over development:

> *"On any turn after 50 I could switch to an alternate strategy involving giants.
> This originally occured if the enemy had 0 barracks or 0 mines and later it
> would switch whenever I was losing or drawing."*

Referent: "This" is the switch to the giant strategy (giants are the anti-tower
siege unit). It began as an **opponent-state** condition and ended as a
**score-standing** condition — "losing or drawing" is literally a tiebreak-standing
trigger. (`occured` is misspelled in the source; it is quoted as written.)

And he states the problem that motivated all of it, from first place:

> *"a large number of games finished with me either just winning in the last few
> turns or being a few turns away from getting through the enemy defenses."*

WHY THIS CORRECTS THE LIBRARY — Sweep 15 recorded as standing context that
*"`KILL_WINDOW_RND: 250` is a round number, and NO winning bot in this sweep
branches on a round number"*, and concluded that the implementation of a
commitment *"should probably not be a clock."*

**That generalisation is now falsified outside Battlecode.** A contest winner
branches on **two** bare turn numbers (50 and 160), and the later one is
specifically the commit-everything deadline. Sweep 15's evidence was drawn from
Battlecode postmortems and a slice of RTS code; this is a different league with
the same structure as ours (kill condition, hard turn limit, score tiebreak), and
it goes the other way.

The narrower statement that survives both sweeps: **a clock is a poor ARMING
trigger and a good DISARMING/DEADLINE trigger.** Every arming trigger the library
has found is on an achievement, a structure count, a resource threshold or map
geometry; every clock it has found — robostac's turn 160, The High Ground's
*"return to normal build order at round 400 whether we are being rushed or not"* —
fires to **stop hoarding** or **stop reacting**, i.e. to end a state that has no
natural exit. That is a genuinely different job and the library was conflating
them.

WHY IT MIGHT TRANSFER — Our version writes itself and is nearly free. Our clock is
1000 rounds; our bank is titanium; our library's standing complaint is that
*"We bank and do not spend"* — we end r200-300 holding more titanium than
Ouroboros while buying a twelfth as much ammunition. A terminal spend-down rule is
therefore aimed at a **measured** defect, not a hypothesised one.

It also interacts correctly with our tiebreak instead of fighting it. Key 1 is
titanium **delivered** (cumulative) and key 3 is titanium **stored** — so titanium
sitting in the bank at r1000 only serves the *weakest* key we have. Spending it
late costs key 3 and can only help key 2 (harvesters alive) and the kill. Sweep 1
already noted the cheap version: *"harvesters alive is key #2 at 20 Ti base — a
handful rebuilt at ~r990 is nearly free."*

WHAT WOULD KILL IT — robostac's deadline works because his spend converts into
units that can *reach* the enemy in the remaining turns. Ours converts into
immobile turrets that must be built adjacent to a builder bot, inside the enemy
kill zone, and the library measured that **2.34% of forward throws at r200+ ever
land a single attack on the enemy core**. A late spend-down on offence is
therefore likely to be pure waste here. The version that survives our measurements
is a spend-down on **key 2 and key 1** — harvesters and pipeline — not on a
last-minute assault.

The proportions also do not import. 40/200 is 20% of the game; 20% of ours is 200
rounds, which is not a deadline, it is a phase. Any transfer must pick our own
number from our own data, and no measurement in this library sizes it.

BUILDER HOOK — A single round-number branch in the core's spend logic: past round
R, stop banking — spend down to a floor on whatever serves the tiebreak keys, and
rebuild harvesters. Pick R from the corpus (the round after which banked titanium
demonstrably never converts into anything), not from a guess. The measurement to
run first: in our 353 r1000 games, how much titanium were we holding at the end,
and what would it have bought at r900 in harvesters?
