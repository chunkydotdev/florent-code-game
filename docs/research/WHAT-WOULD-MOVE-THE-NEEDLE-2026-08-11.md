# WHAT WOULD MOVE THE NEEDLE AT ~1690 — THE AGGREGATES ARE FLAT

**Research arm, s30, 2026-08-11, answering Magnus directly. League-wide:
17,268 archived games, 12,425 of them third-party, 72 teams with a rating
trajectory. Our v104, 1689, rank #21. Top of board 2082.**

## 1. FIVE CANDIDATE LEVERS, MEASURED LEAGUE-WIDE. ALL FLAT.

| candidate | association with rating | verdict |
|---|---|---|
| convert more titanium to ammo | r = **+0.153** | settled axis: ~100% of teams convert in ~100% of games, median first conversion **round 0** |
| convert **earlier** | r = **+0.096** | nothing to win |
| build more turrets | r = **+0.094** (in-band +0.050) | flat |
| **fire more shots** | overall +0.209, **+0.069 controlling for turret count** | flat. **Clankers is 2040 on 64 shots/game** |
| be more decisive (avoid r1000) | r = **−0.854** | **the only strong one, and it is a MARKER — see §2** |

## 2. THE −0.854 DISSOLVES, AND IT DISSOLVES IN OUR FAVOUR

r1000 share by **absolute** strength, not by rating gap:

| both teams | n | r1000 share |
|---|---:|---:|
| < 1300 | 2,565 | **71.8%** |
| 1600–1800 | 4,640 | 8.1% |
| ≥ 1900 | 1,010 | 5.9% |

**The correlation is weak teams grinding because they cannot kill anything.**
Between our band and the top the gap is **2.2pp**.

**And apples-to-apples we are already better than our band:**

| | n | r1000 share |
|---|---:|---:|
| **our games, both teams 1600–1800** | 1,940 | **5.0%** |
| league games excluding us, both 1600–1800 | 2,700 | **10.4%** |

**−5.4pp, z = −6.60.** We are *more* decisive than our peers, better than the
pooled ≥1900 figure, and level with Clankers (4.1%). **Our headline 14.7% was a
composition artefact of who we play.**

⇒ **Decisiveness is not our deficit. This road is closed for us specifically**
(and note it was never an Elo lever anyway — see §3).

## 3. ⛔ THE DISTINCTION THAT REFRAMES THE QUESTION

**Elo pays GAME SHARE: `delta = 32 × (S − E)`, S = games won / 5.** A game won at
r1000 pays **exactly** what a game won at r180 pays. **So "kill faster" is a
PROGRAMME goal (`R1000_IS_DEFEAT`), not a rating lever.** The only thing that
moves rating is winning more of the five.

And the reachable band is narrow: **1598–1803, 17 teams.** The 2000+ teams are
not reachable — we are not paired with them. Climbing means taking game share off
Leviathan (+121), HTTP 418 (+102), kladde (+83), 0033 (+73), team lazy (+68).

## 4. SO WHAT IS LEFT

**Nothing we can count per game separates us from 2000.** We build a normal number
of turrets, convert normal ammo, close games faster than our band — and sit 350
points below the top. **That is the finding: the lever is not an aggregate**, which
is consistent with the programme's own position that the lever is a trick.

Ranked by expected value:

1. **READ CLANKERS.** 2040 rating, **462 archived games we already hold**, and a
   profile that is ours with the numbers halved: **6.1 turrets/game to our 12.6,
   64 shots to our 67, 4.1% r1000 to our 5.0%.** Same decisiveness, half the
   army, +350 rating. **The cheapest intelligence available and we have never
   read it.**
2. **TURN THE EJECTION MACHINERY AROUND.** We are the field's heaviest user of
   enemy-bot ejection — **3,727 hostile throws to their 1,927** — and we do it
   **deep in our own half**: median d² of the ejected bot to *its own* core is
   **265**, only **1.8%** inside their core's heal ring. That is home defence,
   which `PLAY_DEFENCE: never` governs and which scores nothing. **Only 194 of
   12,157 forward turret builds are launchers (1.6%).** The machinery exists,
   the class is approved and engine-verified, and it is pointed at the wrong end
   of the map.
3. **THE HEAL CEILING IS QUANTIFIED AND LOW.** Opponents run **0.86–1.54
   simultaneous core-healers (max 4 ever seen in 100 games)** at 4 HP/turn — so
   **6–16 HP/round** of defence, against which sustained damage is converted to
   titanium for them at **0.25 Ti/HP**, cheaper than every weapon we own.
   **Burst above the ceiling beats it; grinding below it feeds it.**
4. **RESOLVE THE SHOT GAP AS A CORRECTNESS QUESTION, NOT A LEVER.** 12.6 turrets,
   67 shots, rank 61/72 on shots per turret. **Shots do not predict rating, so
   this is not the needle** — but turrets that never fire cost 20–30 Ti *and*
   **+20% each on the global additive cost scale**. The builder's idle-gap
   histogram says whether it is ammo, reload or target availability.

## 5. WHAT THIS IS NOT

League-wide and third-party, so not an echo loop — but **10 days, one league, one
window**, ratings are final-window values, and **every team starts at 1500 here,
so this is a STRENGTH association and not a climb-rate finding.** Correlations
across 72 teams cannot see execution quality, which is where §4 argues the gap
actually lives. **Under `FIXTURE_OF_RECORD: live_unrated` this prioritises roads
and closes none of them except the r1000 road for us specifically, which is closed
on our own apples-to-apples measurement.**
