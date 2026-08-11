---
tactic: a per-opponent statistic must carry the VERSION HISTOGRAM of the games behind it
source: http://satirist.org/ai/starcraft/blog/archives/995-AIIDE-2020-what-BananaBrain-learned.html
origin: Jay Scott analysing BananaBrain (Johan Kayser), AIIDE 2020
evidence: documented (the tables are read off the tournament's write directories); the CAUSE is Jay Scott's stated hypothesis — anecdotal
transfers: yes
---
WHAT IT IS — **Sweep 22's surprise, already documented in 2020, with the arithmetic
visible and a worse outcome than ours.** BananaBrain entered AIIDE 2020 carrying
pre-trained opponent-model data — 3,000 games against "Stardust" — and the entity behind
that name was not the Stardust it met. Verified verbatim
(`pflat/995-AIIDE-2020-what-BananaBrain-learned.flat`):

> "BananaBrain had pre-trained data, 3000 (!) games versus Stardust and 100 each against
> PurpleWave, Dragon, McRave, Microwave, and DaQin."

> "This is the table of pre-trained games. It looks different from the tournament table;
> the overall score and the individual results by strategy do not match up. The training
> may have been against an older version of Stardust on the Starcraft AI Ladder, or it may
> have been against Locutus, which was wrapped around an encrypted Stardust binary on
> SSCAIT and played instead of Stardust if it didn't have its encryption key. **The
> misleading training cannot have helped BananaBrain's results.**"

> "It looks as though BananaBrain might have won the tournament if it had played against
> the same versions of opponents that it trained against. I take it as a sign that secret
> tournament improvements may be worth it."

**AND THE POOLED NUMBER DID NOT MERELY DILUTE THE SIGNAL — IT INVERTED THE RANKING.**
Pre-training vs "stardust": 3,000 games, 51%. Tournament vs Stardust: 150 games, 38%. Per
opening:

| BananaBrain opening | pre-training (n, win%) | tournament (n, win%) |
|---|---|---|
| PvP_2gatereaver | **1110, 66%** | 29, 24% |
| PvP_4gategoon | **56, 0%** | **26, 65%** |
| PvP_9/9proxygate | 437, 61% | 17, 41% |

**The single best real counter scored 0% in 56 pooled training games and 65% in the
tournament, and the pooled favourite with n = 1110 behind it collapsed to 24%.** A large n
on the wrong subject is worse than no data, because it buys confidence.

WHY IT MIGHT TRANSFER — it is structurally identical to the leg that opened this sweep:
one version of ours, N versions of theirs, the cell chosen on the pool, and the version
actually fielded contributing near-zero. The difference is only in severity — theirs was
60%+ of the mass from an entity that may not even have been the same *bot*. **The
transferable rule is blunt: a per-opponent statistic must carry the version histogram of
the games behind it, and a cell whose modal version is not the currently-active one is not
evidence about the current opponent.** Nothing about this requires bot state; it is an
analysis-pipeline change.

WHAT WOULD KILL IT — if our opponents' behaviour varies **less** between their own
versions than BananaBrain's target did — i.e. if version bumps here are mostly bugfixes.
That is exactly the quantity we measured for this sweep and it is not small: holding our
own bot frozen, a rival's later versions cost us **8.00pp of game share**, t = −15.81
(`block-on-opponent-version-not-opponent-id.md`). **So the objection is tested and fails.**
Second qualification: the *cause* of BananaBrain's mismatch (older Stardust vs a
Locutus-wrapped binary) is Jay Scott's hypothesis, offered with "may have been" twice —
the mismatch is documented, the explanation is not.

BUILDER HOOK — the fix that Steamhammer shipped for the same problem, plus the upgrade we
can make that it could not. Steamhammer's opponent model is keyed by NAME and handles
mutation with an exponential recency weight
(`pflat/474-the-opponent-model-in-Steamhammer-1.4.flat`):

> "It counts the recognized plans in the game records for this matchup, ignoring unknown
> plans, and weighting recent games more using a discount factor so that the past is
> gradually forgotten. That way it reacts quickly when the enemy changes its play."

*(Referent: "the enemy" is the single named opponent whose file this is; the discount runs
over game recency **within** that one opponent's record.)*

**Our cell statistic is Steamhammer's predictor with the discount factor set to 1.0.**
Steamhammer had to approximate version identity with time decay **because it was blind to
versions. We are not** — we get `teamAVersion`/`teamBVersion` per match — so we should do
the strictly stronger thing and segment by version, using decay only within a version.
**The honest form is hierarchical, not a hard segment:** shrink the current version's
small-n rate toward the recency-discounted all-version rate, because a hard segment starves
every cell (13 versions × our sample = nothing to select on).
