# OPPONENT AUTOPSY — Leviathan v63, match 18f30710 (1-4, 2026-08-13T11:53Z)

**Provenance:** opus subagent, builder s36, five platform replays, autopsy
self-check 10/10 core-sides 0 mismatches, our seat A verified two ways. Full
result in the s36 session record; this doc is the durable extract.

## The build (DIFFERENT CLASS from team lazy — docs/research/OPP-team-lazy-profile-2026-08-13.md)
1. **Last-mile tile capture (from ~r27-r50):** destroy our core-adjacent
   conveyor, barrier that tile NEXT ROUND (g4: cut r75→barrier r83, r88→r89,
   r103→r104). One action = income severed + spawn ring locked + siege
   platform pre-built. g4: 14/21 of our spawn tiles held for 750 rounds.
2. **Burst-spawn stand-off sentinel wave:** 3 builders spawned in 3 rounds,
   then 4-5 sentinels at d²16-41 built in 5-9 rounds; kill 14-53 rounds after
   first blood (g2: spawn r180-182, wave r186-194, dead r201).
3. **Core-tank + belt-healing:** heals belts in place (127 conveyor heals vs
   our 79 cuts in g2) — ⛔ belt-cutting CONFIRMED DEAD vs healers. Core-heal
   share swings 7%-100% by need. g4: won a GRAND game with ZERO harvesters and
   titanium_collected=0 — pure passive income spent on 1056 core heals.
4. **Disposable gunners:** 32/38 gunner deaths are self-removals (median life
   6 rounds, ~3 shots) — refunds the +20% cost-scale contribution.
5. **Thin pre-defence, heavy reaction:** next-door counter-gunner +1 round
   (same class as lazy); our forward turret life 7-11 rounds contested.
6. **THEY TLE: 519/1/86/1473/2 truncated turns g1-g5** (p99 ~10,4xx µs); we
   had 0. An 1800-band team drowning in CPU on big maps — live evidence for
   the CPU-pressure road.

## Why we lost: the out-heal arithmetic
Net core damage in the four losses: **0, 0, 14, 0 HP** (of 2000/game). Their
heal = 4 HP/Ti; our sentinel = 1.8 dmg/Ti (gunner 1.75, builder attack 1.0) —
**a 2.2x titanium deficit; no damage type out-buys the heal**. g4: one
sentinel, 814 rounds untouched, 4.80 dmg/round vs 4.78 heal/round — lost by
0.02 HP/round. **The win (g1) is the only game with TWO simultaneous forward
sentinels: second landed r208, core dead r357.** Volume-not-sequence now
confirmed vs TWO opponents (lazy M2g4, Leviathan all five games).

## Our defect, named line: the under-latch income lock
Their ring camp latches `under` permanently → `main.py:242` pins
`ti_floor = 12` and line 243 skips the harvester-rebuild reserve → bank sits
at EXACTLY 12 Ti for 108/750 consecutive rounds (g2/g4), ti_collected flat
from ~r90 in every loss, 0/21 harvesters connected across the four losses
(8/10 in the win). The tree names the parent defect itself (doctrine.py:638
"nothing re-plans a chain once its head is destroyed"; :984 "pinning the bank
under the rebuild price for 850 straight turns"). **Inference from code +
pinned constant — BUILDER OWNS CONFIRMING before any fix ships.** Related:
post-fix builder oscillation persists in SIEGE/SEVERED states (g4 bot #11:
660 moves in a 2-tile shuttle on the dead belt line) — chain-loop, not the
MAP_CODES class.

## Verdict: MATCHUP (not variance: net 14 HP; not map: we're 98/180=54.4% on
## today's rotation and won a new map in this match; the defect is the
## transmission mechanism). Lifetime vs Leviathan 128/270 (47.4%); since
## 08-12 24/65; today 4/20. v63 first paired at this match — collinear as
## always, trend flag not attribution.
