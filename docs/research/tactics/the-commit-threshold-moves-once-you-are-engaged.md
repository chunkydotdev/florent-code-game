---
tactic: (C) THE ONLY COMMIT RULE IN THE FIELD WRITTEN AS NUMBERS — a force differential compared against a threshold that DROPS once you are already fighting and RISES while you are idle
source: https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Information/Battles/Types/BattleJudgment.scala
origin: PurpleWave / Dan Gant (StarCraft AI); contrasted with UAlbertaBot and CommandCenter
evidence: documented
transfers: yes
---
WHAT IT IS — Three StarCraft bots, three different answers to "should we fight",
and they form a ladder from no rule to a real one. All three strings below are
verbatim from the current source.

**UAlbertaBot — the threshold is literally zero.** In `Squad::needsToRegroup()`:

```
    bool retreat = score < 0;
```

`score` is the result of a 2000-frame SparCraft playout evaluated with LTD2. There
is no ratio, no margin, no EV: **just the sign of a simulated outcome.** (Its two
status strings are `"\x04 Retreat - simulation predicts defeat"` and
`"\x04 Attack - simulation predicts success"`.) The only softening is a
`int switchTime = 100;` hysteresis constant.

**CommandCenter — an absolute own-unit count, and it latches.** From `BotConfig.txt`:

```
                "AttackCondition"   : [ ["Self", "Zealot"], ">=", [ 3 ] ]
```

consumed by `bool CombatCommander::shouldWeStartAttacking()`. It is not a ratio
against the enemy at all, and once true the flag is never reset.

**PurpleWave — a normalised force differential against a moving target.** From
`BattleJudgment.scala`:

```
  val shouldFight         : Boolean = scoreTotal  >= scoreTarget
```
```
    lazy val scoreSkim = Maff.nanToOne((skimUs - skimEnemy) / (skimUs + skimEnemy))
```

`scoreSkim` is a signed strength differential normalised to [-1, 1]; `scoreTarget`
is `Maff.clamp11(battle.judgmentModifiers.view.map(_.targetDelta).sum)` — a sum of
named situational deltas. And the delta that matters most for us, from
`JudgmentModifiers.scala`, in the `hysteresis` block:

```
    if (fighting) {
      amount  -= .25  * entanglement
      amount  -= .15  * stickiness
      amount  -= .25  * tankLock
    } else {
      amount  += .10  * staticThreat
      amount  += .03  * obscurity
```

`fighting` is `unit.matchups.engagedUpon || unit.matchups.engagingOn`. So the bar
to **keep** fighting is **lowered** by up to 0.65, and the bar to **start**
fighting is **raised** — including a `+.10 * staticThreat` term whose predicate
fires on an enemy **building** in the threat set. The author's own design comment
on the proximity modifier states the philosophy plainly:

```
  // Prefer fighting
  //  when close to home,
```

WHY IT MIGHT TRANSFER — This is the only asymmetric commit rule the sweep found,
and asymmetry is exactly what our arithmetic demands.

Our defensive edge is 2.2:1 (4.4:1 on a stacked core tile). A **symmetric**
threshold — "commit when our damage exceeds their heal" — is a threshold we will
essentially never clear, because clearing it requires out-spending them by more
than 2.2× at the point of contact. PurpleWave's structure says the threshold
should not be one number: **it should be harder to start than to continue.** In
our terms, once turrets are placed and firing at the enemy core, the sunk immobile
cost means abandoning is nearly as expensive as continuing — so the continue-bar
belongs below the start-bar, by construction, not as a tuning choice.

The `staticThreat` term is a second direct import and it points the other way from
our instinct: PurpleWave makes itself **more reluctant** to initiate when an enemy
*building* is in the threat set. Our library already holds
[`initiation-is-a-placement-decision-not-a-fire-decision`](initiation-is-a-placement-decision-not-a-fire-decision.md);
this supplies the number-shaped version of the same idea from a top bot.

The signed-differential form also settles an open item. Sweep 15's outstanding
list flagged that UAlbertaBot's gate is *"a simulated outcome, not a ratio"* and
asked whether it would be a fifth league converging on a **sign** rather than a
ratio. **It verifies, and the answer is: UAlbertaBot is a sign, but PurpleWave is
a genuine normalised ratio compared to a nonzero moving target.** So the library's
"everyone uses a sign" reading is too strong — the field has both, and the
stronger, more recent bot uses the ratio.

WHAT WOULD KILL IT — All three rules govern a *mobile army* deciding whether to
engage, and all three are re-evaluated every frame because retreating is free. Our
damage is immobile: a sentinel that "disengages" is a dead 30 Ti. So the
continue-discount is arguably *automatic* here rather than something to encode —
and encoding it might just be encoding sunk-cost fallacy, which is a real risk and
should be stated. The honest position is that the **shape** (asymmetric bars) is
sourced; the claim that we need it is our inference.

Second, PurpleWave's constants (.25/.15/.10/.03) are tuned against StarCraft unit
values over years of ladder play. Importing the numbers would be the error sweep 16
filed as [`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md).

BUILDER HOOK — If a commit gate is built, give it two thresholds and one bit of
state, not one threshold: `START_MARGIN` (high) to open fire on the enemy core the
first time, `CONTINUE_MARGIN` (lower) once a store slot records that a siege is
live. That is one extra constant and one store bit on top of the count-based gate
in [`the-defenders-reserve-and-what-defeats-it`](the-defenders-reserve-and-what-defeats-it.md),
and it converts a gate we will never clear into one we can.
