---
tactic: The one league with a priced two-tier turret says FEW-STRONG — and the reason it says so is that its costs are flat
source: https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/game-configs.json
origin: Terminal (Correlation One / Citadel) — shipped engine config; doctrine from nknguyenhc/Terminal-Lostkids (3rd place, APAC final)
evidence: documented (config numbers) / anecdotal (doctrine — a competitor writeup, not an organiser doc)
transfers: partial
---

## WHAT IT IS

Terminal is the only league surveyed where the same structure exists in a cheap tier and
an expensive tier at the same time, with both prices published. From the shipped
`game-configs.json` (re-verified from raw bytes by the research arm):

```
"S3_destructor", ... "attackDamageWalker":5.0, "cost1":2.0, ... "attackRange":2.5,
   ... "startHealth":90.0, ... "upgrade": { "cost1": 4.0, "attackRange":3.5, "attackDamageWalker":15.0 }
"S3_filter", "cost1": 1.0, ... "startHealth":75.0, ... "upgrade": { "startHealth": 150.0 }
```

**Subjects, because the numbers need them:** `destructor` is Terminal's **TURRET**
(`game_state.py` binds `TURRET` to unit index 2); `filter` is the **WALL** (index 0).
The turret's base price is **2.0 structure points**, its upgrade **4.0** — and the
upgrade cost is **absolute, not additive** (the sweep leg established this two ways: the
starter kit's `game_state.get_cost` returns `unit_def['upgrade']['cost1']` when present,
and the engine builds the upgrade config as a copy of the base then overwrites it).

**So the trade Terminal offers is: 3× damage and +40% range for 2× the price.** Two
un-upgraded turrets cost the same 4 SP as one upgraded one and deliver 10 damage at range
2.5; the single upgraded one delivers 15 at range 3.5. **Few-strong wins on the raw
numbers, and the field played it that way.** The APAC third-place team's layout:

> *"Three upgraded turrets in the front line near the edge on each side, to clear
> demolishers and scouts directed towards the edges."*

and their stated reason for abandoning an expensive *attacking* unit is the same
structure seen from the other side:

> *"we realised that such strategy is not very effective when there are upgraded enemy
> turrets at the sides, as our demolishers are still destroyed by those turrets before
> they can open up the walls"*

## THE CATCH, AND IT IS THE POINT OF FILING THIS

**Terminal has NO cost scaling of any kind.** The sweep leg grepped the decompiled engine
and the shipped config for every scaling idiom and got nothing; the research arm
re-verified `grep -ci "costscal\|scalecost\|costmultiplier"` on the raw config → **0**. A
Terminal wall costs 1 SP whether it is your first or your two-hundredth.

**That is exactly the variable question (C) is about, and its absence is what makes
Terminal's answer clean.** "Few strong beats many cheap" there is a pure combat-efficiency
result with no count penalty on either side of the comparison.

## WHY IT MIGHT TRANSFER — against our ruleset

**It transfers as a null, and the null is informative.** Our two tiers do NOT offer
Terminal's trade. Terminal buys 3× damage for 2× price; we buy **1.29× damage for 1.5×
price** (sentinel 9/round for 30 Ti against gunner 7/round for 20 Ti). Run the same
comparison Terminal's numbers invite:

| | 60 Ti buys | damage/round |
|---|---|---|
| Gunners | 3 (before scaling) | **21** |
| Sentinels | 2 (before scaling) | **18** |

**Our expensive tier is not a Terminal upgrade — it is a sidegrade.** The doctrine
"upgrade rather than multiply" has no purchase here because the premium does not buy a
multiple; it buys reach and obstacle-piercing. See
[`the-turret-mix-is-not-a-cost-decision`](the-turret-mix-is-not-a-cost-decision.md) for
the full arithmetic including the scale externality.

**The one thing that does transfer directly is the shape of their siting rule:** a small
integer of strong emplacements, **in the front line**, on the *specific approach axes*
that the attack uses — not distributed for coverage. That is the same shape as BC2025's
winner capping defense towers at two on choke tiles, and the same shape as sweep 8's
finding that winners price static defence with forward-ness positive.

## WHAT WOULD KILL IT

- **The doctrine leg is a single competitor writeup**, self-described as third place in
  the APAC final. It is `anecdotal`, not documented, and one team's README is not a meta.
- **Terminal's config is not one config.** The sweep leg found the shipped
  `game-configs.json` and the engine's hardcoded fallback carry *different* turret
  balance patches, both live in the repo at HEAD. The numbers above are the shipped-config
  set — what a local match actually loads. Any other Terminal number quoted anywhere must
  say which set it came from.
- **Terminal's official rules page is unretrievable** (confirmed again by this leg:
  `terminal.c1games.com/rules` is referenced from the starter kit's own README and does
  not resolve). Every rules claim here rests on shipped config or engine bytecode and is
  labelled accordingly.
- Terminal structures have **no ammunition and no upkeep** — fire-and-forget once placed.
  Our per-shot ammo cost is a term their arithmetic does not contain, and it is the term
  that makes our two turrets nearly equal.

## BUILDER HOOK

None as a build change — the transferable conclusion is negative. The usable artefact is
the **comparison table above**, which should be run whenever anyone proposes a turret-mix
change: *what does a fixed titanium budget buy in damage per round, in each mix, at the
live scale?* If the answer is within 15%, the proposal is not an economic proposal and
must justify itself on geometry.
