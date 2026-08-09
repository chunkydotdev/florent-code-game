---
tactic: (B) THE MEASURED WARNING — a strong bot was ahead on the tournament's own score, on average, in the games it LOST; fighting efficiently and converting are different things and a proxy score cannot tell them apart
source: http://satirist.org/ai/starcraft/blog/archives/139-SSCAIT-scores-summary-by-bot.html
origin: SSCAIT / Jay Scott's analysis of tournament score data
evidence: documented
transfers: yes
---
WHAT IT IS — Jay Scott tabulated SSCAIT's in-game scores per bot and found the
result that should govern how we measure any offensive change:

> *"The most striking point is that Krasi0 was ahead in points, on average, in the
> games that it lost."*

and the mechanism, in the same piece:

> *"It’s perfectly possible to lose while ahead on points, when you fight
> efficiently and destroy masses of enemy stuff before dying."*

The score in question is defined on the same page:

> *"According to the SSCAIT rules, a player’s score is the sum of units killed plus
> buildings razed"*

So the metric is a **destruction proxy** — kills plus razings — and a bot could
maximise it while systematically losing. Note the direction: the proxy did not
merely fail to predict wins, it was **anti-correlated** for this bot.

Beside it, the reason a defensive equilibrium is stable among machine opponents,
from the same author:

> *"But there is a reason that so many bots play turtle strategies. Turtling is
> strong against bots which do not adapt, which is most of them."*

> *"Static defense can’t go attack; it costs resources and it offers initiative to
> the opponent."*

Referent: "so many bots" is the SSCAIT field generally.

WHY IT MATTERS HERE — This is the measurement discipline that
[`the-grinder-is-a-legitimate-strategy`](the-grinder-is-a-legitimate-strategy.md)
argues for, arrived at from data instead of from strategy, and it lands directly on
how sweep 17A's question could be got wrong.

Our natural proxy for "did the offensive change work" is damage dealt to the enemy
core, or rounds of siege sustained, or forward turrets placed. **All three are
Krasi0's metric.** A change that raises damage dealt while the sieging turrets die
and the pipeline stalls looks like progress on every intermediate instrument and is
a loss. The library's own damage-to-repair ratio (1.11:1 against the field's 2.79:1)
is exactly this class of number: informative about *style*, not about outcome.

The turtle observation adds the reason this trap is especially live for us.
Turtling beats non-adapting opponents, and our field is machine opponents that
mostly do not adapt — so the defensive equilibrium is not a phase the field is
passing through, it is where it sits. Combined with our own 2.2:1 arithmetic, a
proxy that rewards destruction will keep telling us an offensive change is working
right up until the win rate says otherwise.

WHAT WOULD KILL IT — It is one bot, on one ladder, in an aggregate that Jay Scott
himself presents as striking rather than typical; other bots on the same page do
not all show the inversion. The generalisation "destruction proxies are
anti-correlated with winning" is **not** what the source says and is not claimed
here. What is sourced is that the inversion is possible and was observed in a
strong bot.

The SSCAIT score is also not our tiebreak. Their fallback pays for kills and
razings; ours pays for titanium delivered and harvesters alive. So our proxy risk
runs the *other* way — our tiebreak keys reward economy, and a change that improves
them could hide a collapse in kill capability just as easily.

BUILDER HOOK — none in the bot; a rule for reading experiments. Any offensive
change is judged on **win rate**, with `core_kill_share` and r1000 win rate reported
beside it as diagnosis. Damage dealt, siege duration and forward placement counts
are attribution instruments only, and this file is the reason they can never
promote a change on their own.
