---
tactic: resubmitting the same bot to re-roll the match draw / reset an unlucky rating
source: https://forum.codingame.com/t/1752 · https://forum.codingame.com/t/92373 · https://raw.githubusercontent.com/HaliteChallenge/Halite-II/master/website/about/frequently-asked-questions.md
origin: CodinGame 2015-2019 (MMMAAANNN, Agade, Ozzie, Merome, anon4743054); Halite II (Two Sigma) official FAQ
evidence: documented (the practice and the enabling mechanism); no measured effect size exists anywhere in the corpus
transfers: no
---
WHAT IT IS — On CodinGame, resubmitting identical code changes your rank, so competitors
resubmitted repeatedly until the draw was favourable. Described as standard practice
(`lad_cg_addbattles.flat`, MMMAAANNN, opening a feature request titled *"'Add more battles'
option for multiplayer games and contests instead of repeated resubmissions"*):

> "It is well known that to get an optimal place in ranking, one has to do resubmissions
> several times until some luck will give him somewhat higher position or a chance to fight
> with boss."

> "My last submit isn't my best bot, it's the one that randomly gets highest rank. Went for
> the dice roll with highest win chances and left it as it is"
> — anon4743054, Code a la Mode, 2019 (`lad_cg_alamode.flat`)

The noise being exploited was large: *"I resubmitted the same code and I dropped from 30 to
60"* (Ozzie, 2015) and *"A difference of 200 to 300 places on the gold league between two
submits of the same code"* (Merome, 2016).

**AND THE ENABLING MECHANISM IS OFFICIALLY DOCUMENTED** (`lad_cg_rankingsys.flat`,
CodinGame staff, 2014):
> "each time you enter the arena, your AI will fight 10 games in parallel against opponents
> taken from the whole leaderboard (from first to last). Based on the results of these 10
> games you will be positioned into the arena at a given position"

followed by: "After the 10+100 matches are played, you will play additional matches only
against opponents re-submitting into the arena." **On CodinGame, submission triggers the
match batch.** A resubmit buys a fresh placement draw plus ~110 fresh games; standing still
buys almost nothing.

Halite is the one league where a submit carried an explicit rating consequence
(`lad_h2_frequently-asked-questions.flat`, official):
> "In Halite I, when a player submitted a bot, their rating was completely reset, for
> Halite II, we only reduce the rating by a constant factor and not to zero."

Note the direction: the reset was a **tax on iterating**, and the organisers reduced it.
Nobody in this corpus reports exploiting a reset for gain.

WHY IT MIGHT TRANSFER — **it does not, and the reason is a measurement we already own.**
The CodinGame exploit exists only because the arena batch is triggered *by submission*. **Our
ladder pairs on a CLOCK, not on submission** — 55 of 60 consecutive pairings at minute ≡ 12
(mod 20), 49 of 60 at second `:59`. Our games arrive whether or not we submit. So
resubmitting buys us **no extra games and no new draw**, while `fcode submit`
auto-activates and places the uploaded artifact on the rated ladder. **On our platform,
resubmit-as-reroll is all cost and no reroll.**

The Halite branch is equally closed: our Elo carries across submissions with **no reset and
no decay** — the Halite II regime, more forgiving still. The load-bearing consequence runs
the *other* way: because there is no reset and no soft landing, **a prototype that holds the
slot inherits the incumbent's rating and every game it plays is charged to it**, which is
exactly the −24.67 Elo across 3 leaked matches already on file.

WHAT WOULD KILL IT — i.e. what would reopen the road: only a finding that our pairing
selection is seeded per-submission rather than per-clock. Our own pairing-clock measurement
is direct evidence against that, and the offset has shifted at least once inside 18 hours,
so it should be re-derived rather than assumed — but the *clock* structure, not the
submission, is what schedules our games.

BUILDER HOOK — none. **Do not resubmit to change a result.** File so the next session does
not rediscover a well-documented CodinGame practice and assume it applies here. The one
transferable residue is diagnostic and is filed separately: a frozen artifact's rank still
moves, which is a null distribution we should measure rather than an exploit we can run —
see `a-frozen-bot-moves-on-the-ladder-anyway.md`.
