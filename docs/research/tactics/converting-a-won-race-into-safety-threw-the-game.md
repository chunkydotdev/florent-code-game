---
tactic: Having WON the race, spending the lead on safety instead of on the follow-up is the documented way to lose it — the tempo/robustness dial has a wrong setting on the winning side too
source: http://satirist.org/ai/starcraft/blog/archives/353-turtle-strategies.html
origin: RTS theory / Jay Scott, "turtle strategies", on the bot game Steamhammer vs KillAll
evidence: documented
transfers: partial
---

## WHAT IT IS — arm B from the side we are actually on

Arm B assumed we are the one 13 rounds ahead and asked what to buy. Jay Scott
records a bot that was ahead, bought safety, and lost — and he is precise about
the counterfactual:

> *"It is a build order win for KillAll—if both sides play well, the 9 pool wins
> with little risk. But instead of making a second hatchery to win with mass
> lings, or getting quick gas to win with mutalisks, KillAll turtled. It threw
> away its advantage."*

**Referent check.** KillAll is the bot that had the *advantage* — the preceding
sentence reads *"KillAll opened 9 pool with extractor trick to get 10 drones, and
Steamhammer unluckily chose 5 pool"*, and Jay Scott adds *"the 9 pool wins with
little risk"*. So the turtling bot was **the one who had already won the opening
race**, not the one behind. "Its advantage" is the build-order lead. The two
rejected alternatives he names — *"a second hatchery to win with mass lings"* and
*"getting quick gas to win with mutalisks"* — are both **conversions of the lead
into a bigger or faster follow-up**, not into durability.

The same document states the general condition a defensive purchase must meet,
and it is a *conversion* requirement rather than a survival one:

> *"static defense has to pay for itself with a countervailing advantage: You
> have to use the temporary safety it brings to get ahead in economy"*

**Referent check.** The full sentence continues *"…as in a protoss forge-expand
opening or as Killerbot by Marian Devecka tries to do, or to get ahead in tech,
as when in ZvZ you make a sunken to tide yourself over until your spire
finishes."* So "get ahead in economy" is one of two named channels, the other
being tech — and in **both** the safety is a means to a *later, faster* thing.
Safety that buys only safety fails the test as he states it.

This is the sourced version of the intuition behind
`DEFENCE_ADMISSION_BAR: kill_round_non_regression`, arriving from outside the
repo: **a defensive purchase is admissible when it is spent, not when it is
held.** Sweep 24 filed the naming half of this as
[`static-defence-must-name-what-the-safety-bought`](static-defence-must-name-what-the-safety-bought.md);
this adds the failure case with an outcome attached.

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**Our 13-round margin means we are frequently the bot with the lead, and the
lead is perishable in a way the engine makes explicit.** Median kill r174 vs
median death r187: in the games we win the race, we win it by a margin roughly
the length of one sentinel's work on a healed core. Anything that converts that
lead into durability instead of into damage is spending the only currency we
have on the one thing `R1000_IS_DEFEAT` says does not score.

**Two engine facts sharpen it:**
* **Cost scale is one global additive factor.** A defensive gunner or sentinel
  is **+20%**, and it inflates every subsequent build of every type — including
  the follow-up we would otherwise have bought with the lead. **The safety
  purchase does not merely cost its price; it taxes the conversion.** A barrier
  is +1% and taxes it twenty times less, which is the engine's own argument for
  which instrument a lead should be spent through.
* **Ammo has no passive income.** A turret held for safety is inert until
  titanium is converted 1:1, so "banking safety" is doubly illusory — the
  structure sits at +20% scale while the thing that makes it dangerous has not
  been bought yet.

**EFFECT ON MEDIAN KILL ROUND: this file argues for changes that LOWER it, and
against a class that raises it.** It is a *constraint on defensive planks*, not
a plank: any purchase made while we are ahead must name the faster kill it buys,
or it is KillAll's second hatchery not built.

**⚠ AND IT MUST NOT BE OVER-READ INTO THE RETIRED "NEVER PLAY DEFENCE" CLAUSE.**
`PLAY_DEFENCE` is now `not_at_the_kill_s_expense`, and s30 measured
`home-turrets-off` at 433/1024 and `barrier-seal-off` at 399/1024 — **removing
defensive behaviour COST us, twice, measured.** Jay Scott's rule is compatible
with that and the reconciliation is his own wording: our home turrets and seal
are admissible precisely to the extent they buy the window in which our kill
lands. **The rule bites on defence bought with a LEAD, which is a narrower and
rarer case than defence bought at all.**

## WHAT WOULD KILL IT

* **StarCraft build-order economics do not map cleanly.** KillAll's alternatives
  (a second hatchery, quick gas) are *production and tech* conversions with no
  analogue in a game with one resource, no tech tree and no production
  buildings. Our only conversions are more bodies, more turrets, more belt.
  The *principle* transfers; **no constant does.**
* **A single bot game, chosen by the author to illustrate a thesis.** Selection
  is not controlled and no aggregate is offered. `evidence: documented` covers
  the quotes and the game; the generalisation is his and ours.
* **Our lead may not be legible to the bot.** KillAll could in principle know it
  had won the opening; a builder of ours cannot see the enemy core's HP trend or
  their build. **Without a reliable in-match "we are ahead" signal, a rule
  conditioned on having a lead cannot fire** — and a mis-firing version spends
  on offence while behind, which is the all-in variance tax already filed at
  [`all-in-variance-is-a-ladder-tax`](all-in-variance-is-a-ladder-tax.md).

## BUILDER HOOK — none yet, and the blocker is a signal we do not have

None, deliberately. The prerequisite is an **"are we ahead?" observable**, and
the incumbent's nearest thing is the HP-delta arming primitive at the core
(sweep 23 verified `bots/_v135loki18/main.py:176-178` is core-only, under
`# --- Core-only accounting ---`), which measures being *attacked*, not being
*ahead*.

The cheap descendant is a corpus cut rather than code: **in our games where we
land the first meaningful core damage, what do we spend the next 25 rounds of
titanium on, and does spending share on defensive structures in that window
predict a later kill round?** That is directly Jay Scott's claim, on our data,
with no bot change and no leg — and if defensive spend after taking the lead
predicts nothing, this road closes cheaply. Use `ladder_games.tsv` for the
denominator per the standing corpus rule.
