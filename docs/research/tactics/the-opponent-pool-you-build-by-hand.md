---
tactic: Replace one aggregate win rate against your own bot with a handful of NAMED, behaviourally distinct opponents and per-opponent gates
source: https://forum.codingame.com/raw/195736/28
origin: CodinGame Spring Challenge 2022 / VirtualAtom (115th Legend); with BattleSnake (Asymptotic Labs) and Halite II's winner
evidence: documented
transfers: yes
---
WHAT IT IS — **The constructive answer to (C), from someone who states our exact problem first.**
VirtualAtom: *"we cannot test locally how well our bot performs, so we have to rely on the
arena"*, and the naive self-pool failed him in the way ours fails us — *"None of those bots were
clearly better than others when tested locally."*

**His fix was not more games. It was to stop treating the pool as one number.** He hand-built five
deliberately *different* opponents and named them:

> *"On my computer, I made a bot version that defends only, another one that defends and farms
> wild mana with three heroes, another one that uses a hero as a dumb attacker, and two variations
> of the latest on the defense tactics. For clarity's sake, we could name those bots DEFEND, FARM,
> MIXED1, MIXED2, and MIXED3."*

Then he gated progress on **per-opponent thresholds that differ by opponent**, with the reason for
each gate written down:

> *"once the bot clearly defeats the DEFEND version (so could defend better with only two bots)
> and has more than 20% win rate against the three mixed versions (resist correctly to a dumb
> attack with only two heroes to farm/defend), go to the next step"*

and the later gate, *"until the win rates are all above 90% vs DEFEND, FARM, MIXED1, MIXED2, and
MIXED3"*. **It transferred to the real ladder, and his own account of the moment is the
validation:** *"For fun, I decided to submit a borked version of my attacker, as I got some high
win rates against all my previous versions. That version passed legend, to my great amusement."*

**The complementary mechanism, from a different game, explains why a pool of old versions is safe
at all.** BattleSnake's Asymptotic Labs sample opponents deliberately: *"80% of the time we train
against the current best model, and 20% randomly select one of the prior best models as the
opponent."* Their stated reason is non-transitivity — *"the current policy will be forced to
“remember” how to play against the older strategies, and will be less likely to learn cyclical
strategies as presented above"* (the referent of *"as presented above"* is their worked
rock-paper-scissors example in which a policy cycles R→P→S→R and ends up no better).

**And the decay this is a remedy for, from the Halite II champion** (*"after 3 months I won the
Halite 2 AI competition with a decisive lead"*) — the second sentence is the one sweep 15 did not
have, and it gives the *direction* of the error:

> *"Local testing against previous versions was helpful in the beginning, but the exercise became
> increasingly inaccurate and pointless over time. I often had versions performing much better
> online while still performing poorly against the previous version."*

WHY IT MIGHT TRANSFER — **`transfers: yes`. It is a change to how we run probes, not to the game.**
PROGRAMME already says the pool is dominated 87-90% and that win rate is not the verdict; INDEX
adds that our opening is a near-constant (CV 0.09) *while the field's is 0.26*. **That variance
gap is precisely what VirtualAtom manufactured by hand.** We have the raw material to do the same
cheaply, because the library already contains the behavioural axes to build variants along:
a **turtle** (heal-screen defence, no forward placement), a **rusher** (the Loki shape), an
**economy-max** bot (conveyor spam, no turrets), and a **launcher-defensive** bot (sweep 12's
finding that the field prefers the launcher defensively). Four named opponents whose *behaviour*
differs, plus per-opponent gates, converts a flat 87-90% blob into a profile — and a plank that
moves one gate while breaking another is information, where a 1pp aggregate move is not.

WHAT WOULD KILL IT — **Two real limits.** (1) **These are still copies of us**, so the population
defect sweep 15 documented does not disappear — it is *reduced*, not removed, and the ~2×
inflation should still be assumed. The variants only contain behaviours we can imagine; the top of
our league beats us with behaviours we have not imagined, which is exactly the gap. (2) **Building
four maintained variants costs builder time that could go into planks**, and every variant is a
second bot to keep alive as the engine and the chassis move. VirtualAtom was working inside a
two-week contest with a throwaway codebase. **The cheap version, and probably the right first
step, is not to write new bots but to designate existing archived iterations** — the repo already
holds many — **as the named pool, on the basis of how they behave rather than how recent they
are.**

BUILDER HOOK — Pick 3-4 archived bot versions whose *behaviour* differs on a named axis, label
them, and report every future probe as a **vector of per-opponent win rates plus core-kill share**
rather than one aggregate. No new bot code, no arena policy change, no new tooling beyond a
column in the report. **The single check that tells us whether it was worth it: do the per-opponent
numbers ever disagree in sign?** If they never do, the axes chosen are not real axes and the pool
should be rebuilt on different ones; if they do, we have recovered discriminating power the
aggregate was averaging away.
