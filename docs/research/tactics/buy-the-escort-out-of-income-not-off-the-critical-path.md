---
tactic: Fund the survivability out of INCOME, never off the critical path — the tempo/robustness trade is dissolved, not resolved
source: http://satirist.org/ai/starcraft/blog/archives/817-timing-openings-the-fast-lurker-challenge-3-competitive-builds.html
origin: RTS theory / Jay Scott (Steamhammer author), "timing openings: the fast lurker challenge" 1 & 3, 2019
evidence: documented
transfers: yes
---

## WHAT IT IS — ⭐ this is sweep 25's answer to arm B, and it is not one of the two options the question offered

Arm B asked: 13 rounds ahead on a race, do you go FASTER or become HARDER TO
STOP? The only competitor in 65 primary documents who worked this problem
explicitly **refused the dichotomy**, and the refusal is the transferable part.

Jay Scott set out to build the fastest possible lurker rush and then to make it
*competitive*, i.e. to add escorting units that keep the strike alive. He states
the constraint as an absolute:

> *"But in either case, it defeats the purpose if zerglings delay the lurkers."*

**Referent check.** "either case" is the two reasons he wants zerglings, listed
in the preceding sentences: *"First, you’d like at least one pair of zerglings
early to handle the enemy scout"* … *"Second,"* — and here is the second, quoted
verbatim — *"you’d like as many zerglings as possible to accompany the lurkers
and make the rush stronger"*. So "zerglings" are the escort/robustness purchase
and "the lurkers" are the timed strike. The rule is: **the escort may not move
the strike.**

He then writes two candidate builds that buy the *same* escort, and rejects the
obvious one:

> *"I do not recommend the A version above. I think the B version below is
> better. It keeps the 9th drone and gets the 2 zergling pairs later. With the
> income from the 9th drone, it is possible to get the same 4 zerglings without
> delaying the lurkers."*

Version A paid for the escort by **deleting a worker** — funding robustness out
of the economy that drives the timing. Version B **kept the worker**, took the
same escort **later**, and the strike landed at the same frame. Identical
robustness, zero tempo cost, and the difference is purely *which budget it came
out of*.

The same principle appears in the first post of the series as a test for whether
a unit is free at all:

> *"The build includes 3 drones after the lair which are not on the critical
> path to get lurkers, but they fit into gaps and use available resources, so
> they add no delay"*

And the honest limit of the approach is stated in the same document — a build
tight enough has no slack to exploit:

> *"The build is extremely tight and does not have room for zerglings until
> after lurker research starts. Even then, to avoid delaying the lurkers the
> build needs to squeeze in 1 additional drone."*
> *"A fast build can barely afford supporting units, and depends on a fast
> strike for its power—if any."*

**He also produced the one tempo-favouring MEASUREMENT in the corpus, and
named its own confound.** Rather than win rate, he counts how often the bot's
own opening chooser picked each build:

> *"The interesting number is not each opening’s winning rate, which depends on
> the opponents that it was used against, but the number of games it was played
> in: How often did Steamhammer think it was the best opening?"*

with the tally `9PoolLurker 91 / OverpoolLurker 76 / 2HatchLurkerAllIn 52 /
2HatchLurker 6`, listed fastest to slowest, and the verdict

> *"The numbers say that the faster lurker rushes were more useful"*

immediately followed by the confound, unprompted:

> *"Well, it may be simply because the faster rushes get zerglings right away,
> which by themselves are enough to destroy a low-end terran opponent"*

and the correctly hedged conclusion: *"it’s suggestive evidence that a faster
lurker rush may be worthwhile"*.

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

Our race is a 13-round margin (median kill 174 vs median death 187), so every
plank is exactly this problem. And **our engine makes the A-vs-B distinction
unusually sharp, because our two budgets are genuinely different currencies:**

* **Titanium** is one global pool. Spending it on a barrier does not slow a
  later sentinel by any amount except the time to re-earn 3 Ti.
* **BUILDER-TURNS are the scarce serial resource.** A builder bot's actions are
  mutually exclusive per round (act XOR move, cooldown-gated), so a barrier laid
  by the raider *en route* costs a MOVE and therefore delays arrival by one
  round — that one is on the critical path. A barrier laid by a **different**
  body, or by the raider **during a round it could not move anyway** (move
  cooldown non-zero), is version B: same robustness, zero delay.
* **Cost scale is the third budget and it is global and additive.** A +20%
  purchase (builder/gunner/sentinel) inflates every later build of every type,
  so it is on the critical path *even when titanium is abundant*. A +1% purchase
  (conveyor/splitter/barrier) is 20× cheaper in that currency. **This is the
  engine-level reason our escort should be barriers and bodies-already-present
  rather than extra turrets:** the barrier is the "3 drones that fit into gaps".

**EFFECT ON MEDIAN KILL ROUND: NEUTRAL BY CONSTRUCTION — that is the entire
point.** This is not a tempo plank and not a defence plank; it is a *funding
rule* that makes a defensive purchase pass `DEFENCE_ADMISSION_BAR:
kill_round_non_regression` **at design time instead of at measurement time**.
It is the same shape as [`the-rush-cost-budget-gate`](the-rush-cost-budget-gate.md)
(sweep 24's most buildable item) approached from the other side: the rush cost
makes non-rush spending *expensive*; the critical-path rule makes it *free where
it is genuinely free* and forbidden elsewhere.

## WHAT WOULD KILL IT

* **If our critical path is not titanium-bound or turn-bound but ARRIVAL-bound
  in a way slack cannot touch.** `doctrine.py:1456` and `:1478` both say ARRIVAL
  is our scarce quantity, and the ferry exists because walking is the binding
  cost. If the raider is move-cooldown-saturated for the whole approach, there
  are no "gaps" to fit anything into and version B does not exist — the build is
  Jay Scott's *"extremely tight"* case, where he concedes the slack runs out.
* **If the slack is illusory because of the 5% CPU-buffer/10 ms turn budget.**
  A "free" extra computation per round is not free the way an extra drone is.
* **This is a build-order theory from a game with continuous time, worker
  income and tech prerequisites.** Our economy has none of the prerequisite
  structure that makes a "critical path" well-defined; the analogue has to be
  constructed, not imported. Evidence class is `documented` for the SOURCE, and
  the transfer is our inference.

## BUILDER HOOK — smallest thing that would test it

**No new store slot needed** (the 16-slot store is fully bound,
`doctrine.py:931-961` / `:1166-1170`).

`bots/_v148ferryfirst/raid.py:245` already places a barrier *"on the first
action after landing"*, and the module header (`raid.py:55`) calls it *"value
that outlives the body"* — so the escort purchase exists. **What is not
separated is whether it is version A or version B**: the barrier claims the
raider's action for that round, and a builder cannot act and move in the same
round.

Smallest test: gate the seal barrier on `ct.get_move_cooldown() != 0` — i.e.
**lay it only in rounds the raider could not have advanced anyway** — and A/B
that against the unconditional placement. Same barriers, strictly fewer delayed
rounds. Read out **median kill round** and forward-structure survival together;
version B predicts survival flat and kill round flat-or-earlier, version A's
defenders predict survival flat and kill round later. Either result is
informative, and it is a one-line predicate.
