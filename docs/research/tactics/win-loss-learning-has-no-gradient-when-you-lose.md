---
tactic: Against a far-stronger opponent a win/loss signal carries no gradient — you need a denser score
source: http://satirist.org/ai/starcraft/blog/archives/939-Steamhammer-and-machine-learning.html
origin: Jay Scott / Steamhammer, AIIDE StarCraft AI Competition; with Microwave (AIIDE 2020) and InfestedArtosis (AIIDE 2023)
evidence: documented
transfers: yes
---
WHAT IT IS — **The failure mode of measuring yourself by wins when you are losing, stated
mechanically by a bot author about his own learner:**

> *"against a much stronger opponent Steamhammer rarely wins and falls back on trying builds at
> random, hoping to hit one that works. Most of the random choices are poor, but it is losing
> every game anyway so it can’t tell."*

His proposed fix is not more games; it is **a denser reward than win/loss** — the next sentence is
*"The evaluator will tell it which tries are more nearly successful; it will try those more often
and have better chances."*

**The direction of the bias when you do use a weak pool, measured on a real bot.** AIIDE 2020,
Microwave's prepared training data versus its tournament results:

> *"In general, for stronger opponents training data overestimated Microwave’s success, while for
> weaker opponents it was the opposite"*

**Testing systematically flatters you against opponents above you and under-sells you against
opponents below you** — which is exactly the wrong way round for a team trying to size a plank
against a band 400 Elo up.

**And the counter-example that shows a small, well-shaped learner beating the field at learning.**
AIIDE 2023: the strongest bots *"were outlearned by the competition"*, while the bottom-ranked
entrant improved more after round 100 than anyone — *"The weakest bot outdid all others in
continuing to play better over the entire long tournament."* Its structure, per the same post, was
deliberately narrow: three independent choices, each from a short menu.

WHY IT MIGHT TRANSFER — **`transfers: yes`, and it is external validation of a choice the
PROGRAMME already made.** `WIN_RATE_IS_VERDICT: no` with `PRIMARY_CURRENCY: core_kill_share` and
`SECONDARY_CURRENCY: time_to_core_kill` is precisely the substitution Jay Scott says is needed:
**a denser signal than win/loss, on which "more nearly successful" is expressible.** The measured
justification in PROGRAMME is our own — LOKI-1 vs v92 was *"a win-rate NULL (+3.1pp, p=0.22) and a
core-kill landslide (91% vs 61% share, paired sign test p=5.2e-09)"* — and this file supplies the
independent reason that pattern is expected rather than anomalous.

**It also says the currency is still not dense enough for the top band**, and that is the
actionable part. Against sporks-class opponents `core_kill_share` will itself be near zero and
carries the same no-gradient problem one level up. The denser quantities our engine exposes, all
readable from a replay without a kill: **enemy core HP minimum reached**, **rounds of enemy
healing forced**, **enemy titanium diverted into defence**, **cumulative titanium delivered** (the
first tiebreak key). A plank that never kills a 2100 core can still be ranked on how far it pushed
the core-HP minimum — which is what *"more nearly successful"* means here.

WHAT WOULD KILL IT — **Two things.** (1) **A denser proxy is only useful if it is monotone in the
thing we want**, and that is unproven: pushing enemy core HP lower does not necessarily approach a
kill if the defender's heal rate simply absorbs more — the 2.2:1 arithmetic means we can spend
unboundedly to depress HP without ever crossing the threshold. **A proxy that rewards
sub-threshold aggression would actively steer us into the donation INDEX warns about**, which is
the single most likely way this file does damage. Any HP-based proxy must be paired with a cost
term. (2) Jay Scott's remark is a design note about a learner he had not yet built; the AIIDE
counter-example (InfestedArtosis) is one bot in one tournament and its mechanism is a bandit, not
an evaluator. **Neither is a demonstration that the denser signal worked** — only that the sparse
one demonstrably does not.

BUILDER HOOK — For our existing games against the 1900+ band, compute the **distribution of enemy
core HP minimum** rather than the kill count. If it is a wall at 500 (never scratched), the
matchup is in the no-gradient regime and even `core_kill_share` cannot rank planks there. If it
spreads, we have a usable denser currency for that band **and the ranking should be by HP pushed
per titanium spent**, not by HP pushed — per the cost-term caveat above. Corpus query only; no bot
change and no PROGRAMME change, which is Magnus's call.
