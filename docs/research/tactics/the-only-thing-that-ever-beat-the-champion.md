---
tactic: Against a far-stronger opponent, the only opening that ever scored was the all-in — measured, 150 games
source: http://satirist.org/ai/starcraft/blog/archives/989-AIIDE-2020-what-Microwave-learned-2.html
origin: AIIDE 2020 StarCraft AI Competition / Microwave (#6 of 13) vs Stardust (#1); Jay Scott's published learning-file dumps
evidence: documented
transfers: partial
---
WHAT IT IS — **The hardest number in this sweep, and it is exactly the question we asked.** In
AIIDE 2020, **Microwave finished #6 overall at 54.47% and scored 1% against #1 Stardust** — from
the crosstable row *"6 microwave 54.47% 1%"*, whose column header is *"# bot overall star purp
bana drag mcra micr stea daqi zzzk ualb will ecgb eggb"* (self-column omitted; Stardust's own row
is *"1 stardust 93.22% 83% 62% 93% 98% 99% 98% 93% 99% 98% 99% 99% 97%"*). **That is a bot beaten
almost as thoroughly as the top of our league beats the mid-field.**

Microwave's per-opening learning file against Stardust is published. **I re-parsed it myself from
the block header to the block total: 47 opening rows, 150 games, and exactly ONE row with a
nonzero win rate:**

> *"3HatchLingBust 9 11%"* — against a block total of *"47 openings 150 1%"*

`3HatchLingBust` is a zergling all-in bust. **Every other opening Microwave tried went 0%,
including its most-tried one, *"3HatchMuta 36 0%"* — 36 games, no wins.** The all-in was tried 9
times and won one.

**AND THE PART THAT MATTERS MOST, because it kills the obvious alternative explanation.**
Microwave's opponent model worked essentially perfectly and it bought nothing. The second table in
the same block records what Stardust was doing — *"HeavyRush -> HeavyRush 127 1%"*, and the page
explains the notation: *"The enemy strategies listed in the form “HeavyRush -> SafeExpand” are the
initially predicted and the later recognized enemy play"* … *"When they’re the same, the
prediction was correct."* So Microwave predicted correctly in 127 of 150 games. Jay Scott's own verdict, in the
sentence immediately after the tables:

> *"Stardust always plays the same strategy, so it’s no wonder that Microwave was able to predict
> it. Not that it helped."*

**Against a sufficiently stronger opponent, knowing exactly what they will do is worth nothing.
Only the highest-variance option scored at all.**

**Supporting theory, verified, and it is about problem-count rather than about being weak.**
BananaBrain (AIIDE #1 in 2022 and 2023), per Jay Scott: *"Unpredictably playing one of several
strong openings sets the opponent two problems (“what is this fiend doing, and then how do I live
through it?”)"* … *"which must both be solved, more than twice as difficult."* And the
tournament-scale version: AIIDE 2015's runner-up was a one-trick all-in — *"In a close second
place was ZZZKbot, which implement a 4-pool Zergling rush strategy every game. Despite the
relatively simple strategy, most bots did not have proper defense capabilities and lost in very
short games."*

WHY IT MIGHT TRANSFER — **It is the closest thing to a direct answer the sweep found to "what does
a 1603 bot do against a 2100 bot", and it agrees with the PROGRAMME.** `LINE: loki` and
`KILL_WINDOW_RND: 250` point at exactly the option this data says is the only one that ever
scored. It also reframes what a Loki plank is *for*: not to raise our expected result against the
top band — nothing did that — but to convert a 0% matchup into a small nonzero one. **Against
sporks at 2102 that is the whole available prize**, and INDEX's own framing (*Elo is game-share so
every stolen game pays*) says a small nonzero is worth having.

WHAT WOULD KILL IT — **Four things, and they are serious enough that this file is not a
recommendation.**
1. **11% of 9 games is one win.** The confidence interval on a single success is enormous, and Jay
   Scott himself notes elsewhere that Microwave's *"training data overestimated Microwave’s
   success"* against stronger opponents — so even the 11% is probably optimistic.
2. **The same author, on the same blog, ran the opposite experiment and reports it worked better.**
   *"Last year, Steamhammer scored many upsets against stronger players and many losses against
   the lower ranks. Today it is the other way around"*, and his stated method: *"I haven’t been
   trying to beat the top bots, I’ve been trying to play better."* … *"It’s the opposite plan
   from trying to beat the current #1."* **Upset-proneness and overall strength traded off against each
   other, and he chose strength.** Filed here rather than buried because it is the direct
   counter-argument.
3. **Our ruleset is the one where the all-in is structurally weakest.** Sweep 14 established the
   precondition BC2020/BC2023 had and we lack — cheap, mobile, continuously-producible damage —
   and the heal arithmetic prices sub-threshold aggression at a 2.2:1 donation. A zergling bust
   has no analogue here; our damage is immobile and must be paid for inside their kill zone.
4. **It is one bot, one opponent, one tournament.**

BUILDER HOOK — **A partition, not a plank, and it is the same query three files in this sweep now
ask for.** Against the 1900+ band, is our result-by-game *bimodal* — a set of games we lose the
same way every time, plus a few that were close? If our top-band losses are uniformly hopeless,
this file says the marginal value sits entirely in high-variance options and near-zero in
improving the base. If some are close, item 2's counter-argument applies instead and the base is
where the money is. **The corpus can answer which, and the answer changes what Loki should be.**
