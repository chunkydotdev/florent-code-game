---
tactic: Find the thing nobody at the top ever does, and delete or exploit the machinery that assumed they would
source: https://forum.codingame.com/raw/184113/81
origin: CodinGame Spring Challenge 2020 / Gonny (finished #29); with Halite II's Shummie on live false-positive testing
evidence: documented
transfers: partial
---
WHAT IT IS — **A competitor measured a blindness in the top of the leaderboard and acted on it,
and the action was to DELETE code.** Gonny (*"Finished #29"*) had built the correct defensive
reflex — switching his unit's rock-paper-scissors form when an enemy could kill it next turn — and
then checked whether anyone was actually punishing him for not having it:

> *"Regarding abilities, I initially switched if I knew an enemy pac could try and kill me next
> turn, but I then realized that at the top of the leaderboard no one ever does that."*

(The referent of *"that"* is an enemy pac trying to kill his pac next turn. He continues that he
saw a top player *"who always assumed no one would try to kill his pacs if their cooldown was 0"*,
and concludes: *"at that point I removed switch altogether"*.)

**Two distinct plays fall out of one measurement.** The *defensive* play is to stop paying for a
counter to something that never happens. The *offensive* play is the mirror — the same measurement
identifies a behaviour the top tier has left undefended. **Gonny took the first and explicitly did
not take the second**, which is why this file is honest about cost: *"since I did not implement
any sort of attacking for sure kills or preemptively defending against those, I just never
switched."*

**AND THE METHOD FOR VALIDATING AN OPPONENT-FINGERPRINT SAFELY, from Halite II's Shummie**, which
is the most portable single idea in this packet:

> *"I even uploaded my alliance dance code for about 2 weeks, but if it detected a positive, i
> would immediately crash. This would give us an idea of how often our signal would have a false
> positive."*

**Ship the detector live with a harmless payload, and read its false-positive rate off real ladder
traffic before arming it.** (His payload was a deliberate self-crash so a false positive could
never help him — the measurement is uncontaminated by the thing being measured.)

WHY IT MIGHT TRANSFER — **This is INDEX's `play the players` mandate with a measurement procedure
attached, and both halves are cheap for us.** We hold 3.8k decoded replays with league-wide match
listing, so "what does the 1900+ band never do" is a corpus query, not an experiment. Candidate
questions in our vocabulary, all answerable from the corpus without touching the bot: *do top
teams ever rotate a gunner?* (10 Ti + a cooldown — a real cost they may decline to pay); *do they
ever build a launcher?* (sweep 12 says the field prefers it defensively — do the best?); *do they
ever heal a builder standing on a core footprint tile?* (the 4.4:1 stacked case INDEX flags as
load-bearing); *do they respond at all to a unit parked at the edge of their vision?* **Each "no"
is either code we are paying for and need not, or a hole.**

And the Shummie pattern maps exactly onto our engine: any fingerprint we intend to act on can be
computed and **written to the comms store or printed to the replay** for a submission or two,
firing no behaviour at all, and its false-positive rate read off the resulting replays. That costs
one store slot and no strategic risk. **Note the store constraint while doing it: writes are
buffered to next round, last writer wins, and a negative write RAISES and permanently destroys the
unit** — a fingerprint counter that can go negative is a unit-killer.

WHAT WOULD KILL IT — **Three limits, and the first is the one that bites hardest here.**
(1) **An absence in a replay corpus is not an absence in the bot.** "They never rotate a gunner"
may mean their code never chooses to, or that the situation never arose in the games we hold —
and our games against them are a biased sample, because *we* generate the situations. A negative
measured only in our own matchups is confounded by our own behaviour; the cleaner read is their
games against **third parties**, which the corpus supports.
(2) **Deleting the counter is only safe while the absence holds**, and the top tier iterates. Same
depreciation logic as [`probing-the-target-teaches-the-target`](probing-the-target-teaches-the-target.md).
(3) Gonny finished **#29**, not near the top, and his own thread contains the warning label for
anyone reading isolated results in a high-variance game — *"so any decent bot can easily win a
couple games against #1"*.

BUILDER HOOK — One corpus query, no bot change: **for each of the five 1950+ teams, the count of
each action type per game** (gunner rotations, launcher builds, launches, heals on stacked tiles,
ammo conversions), computed on their games against *third parties* as well as against us. Any cell
that is **zero across all their games** is a candidate — and per (1), a zero that appears only in
their games against us is a finding about us, not about them.
