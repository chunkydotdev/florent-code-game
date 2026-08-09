# What the field does after r150 that we do not: it keeps building turrets, and marches them forward

**Research arm, 2026-08-09 (session 22).** Builder's Q1/Q2, re-scoped 06:5x.
**Version tag:** live **v89 "Eir 9c hivethaw (rollback)"**, submission `847b8d9d`
= `bots/_v100hf`, md5 `9e85cae5`, tree hash `4558be91`. Ladder 1534.62 @ 487,
rank #34 (builder's 07:0x reading; I verified 1524/#36/486 at my 06:41 boot).
**Corpus:** all 3,831 archived replays + 487 ladder matches / 2,435 games of free
metadata. **ZERO replay downloads.** Method and traps:
`docs/research/corpus-howto.md`. Tables: `corpus/`, manifest git sha `5353bd3`.

---

> **AMENDED ONE HOUR AFTER PUBLICATION, by me, against my own §2.** This document
> frames the r200-300 shot deficit (we fire 5.8/game, Ouroboros 103) as a TURRET
> PRODUCTION problem. Turrets fire from a global ammo pool with no passive
> income, so there were two candidate causes and I tested only one. **Ammo is a
> real co-constraint: in r200-300 we convert 34.8 ammo per game to Ouroboros's
> 441.6 while ENDING THE WINDOW ON MORE TITANIUM THAN THEY DO (635 vs 478).**
> Production remains the larger term (~10x vs 4.7x) so §2-§4 stand, but "we have
> no turrets" is an incomplete reading of §2 and the ammo half is much cheaper to
> fix. See `docs/research/ammo-and-cpu-2026-08-09.md` §1.

## 0. TL;DR

1. **Late offensive insertion is dead as a tactic.** Median raider life after a
   forward throw collapses **43 → 6 rounds at exactly r150**. Only 2.34% of
   forward throws at r200+ ever land a single attack on the enemy core.
2. **The r200-300 deficit is not a targeting problem, it is a PRODUCTION
   problem.** In r200-300 the field builds **~2 turrets per game; we build ~0.2**.
   They fire 40-103 shots per game; we fire 6-13.
3. **The HANDOVER's "their gunners are OFFENSIVE, ours sit at home" is confirmed
   — and it is NOT a difference in doctrine from the start.** Before r150 we
   place turrets almost identically to them (41% forward vs 38%). **The
   divergence begins at r150**: they push turrets outward, we pull them home and
   stop building.
4. Both cliffs are at **r150**, the same round the conversion ratio hits parity.
   Three independent instruments, one boundary.

---

## 1. Q1 — DOES LATE INSERTION WORK FOR ANYONE? No.

58,251 throws decoded across 1,914 of 3,791 replays, 0 parse errors.

```
EXILE   (thrower's team != thrown bot's team)   40,540   69.6%
INSERT  (own bot, lands nearer the enemy core)  11,895   20.4%
RETREAT (own bot, lands further away)            4,879    8.4%
unattributable (launchers of both teams in range)  937    1.6%
```

**The ferry finding is directionally right and its "every" is too strong.**
Defensive disposal is ~70% of all launcher activity in this field; 11,895
genuine own-team forward throws nonetheless exist.

What the forward throws achieved:

| band | n | reached core | **attacked core** | median life after throw |
|---|---|---|---|---|
| r0-150 | 4,950 | 26.9% | **7.0%** | **43 rounds** |
| r150-200 | 911 | 11.5% | 4.3% | **6 rounds** |
| r200-300 | 1,491 | 8.7% | 2.8% | **6 rounds** |
| r300+ | 4,543 | 6.6% | 2.2% | **6 rounds** |

A builder does 2 damage per attack against a 500 HP core. Six rounds is ~12 HP
even if the raider lands adjacent and attacks every round.

**Not a pure negative:** the 528 raiders that did attack produced 40,114 core
attacks, and 319 of them were on the winning team. It is brutally concentrated —
**25 raiders = 50.5% of all attack volume, 100 = 86.2%**, max 947 attacks by one
raider. **The scarce resource is not the throw; it is survival at the
destination, and it is only purchasable before r150.**

**Consequence, and the builder's clock ablation agrees:** `LAUNCH_GIVEUP_RND =
180` is a **correct constant justified by a false comment**. The comment
(doctrine.py:106) claims matches never reach that bound — half our games do. The
number is right anyway. The builder's `_v104loki0` clock ablation measured
89-91, 49.4%, CI [42.2%, 56.7%], n=180 — inert, exactly as this curve predicts.

## 2. Q2 — WHAT THEY DO INSTEAD: they keep building turrets

Per game, in our archived ladder matches (n = archived games per opponent):

**r200-300**

| opponent | n | gunners THEM/US | shots THEM/US | builder-attacks THEM/US |
|---|---|---|---|---|
| Ouroboros | 85 | **4.18 / 0.12** | **103.3 / 5.8** | 3.0 / 20.8 |
| Powerpuff Girls | 85 | 2.11 / 0.22 | 59.9 / 8.1 | 96.1 / 41.4 |
| Leviathan | 70 | 2.07 / 0.59 | 25.5 / 20.9 | 0.9 / 70.4 |
| Kings College Munich | 95 | 2.01 / 0.18 | 39.9 / 8.9 | 11.0 / 19.6 |
| CtrlAltDefeat | 75 | 2.00 / 0.35 | 47.2 / 13.2 | 17.6 / 28.0 |
| Lunds Stallions | 115 | 1.94 / 0.17 | 66.3 / 8.1 | 15.7 / 24.3 |

**Ouroboros — the team that destroys our core more than any other in r200-300
(22 kills, 18.0% of games alive at r200) — builds 4.18 gunners per game in that
window and fires 103 shots. We build 0.12 and fire 5.8. A 35x production gap and
an 18x fire gap, in exactly the window we lose.**

**And note the inversion in the last column: our BUILDER ATTACKS are usually
higher than theirs.** We are not passive late — we are fighting the late game
with builder melee at 2 damage a swing while they fight it with gunners at 7 and
sentinels at 18. We are busy and out-gunned.

## 3. WHERE the turrets go — the HANDOVER hypothesis, tested

Every gunner/sentinel build in the six matchups (11,784 turret/launcher builds),
by round band. `FORWARD` = built nearer the enemy core than one's own.

| band | who | n | forward% | median d² to OWN core | median d² to ENEMY core |
|---|---|---|---|---|---|
| r0-150 | THEM | 3,449 | 38% | 25 | 45 |
| r0-150 | **US** | 1,711 | **41%** | 25 | 37 |
| r150-200 | THEM | 841 | 51% | 61 | 40 |
| r150-200 | **US** | 257 | **31%** | 18 | 130 |
| r200-300 | THEM | 1,346 | 51% | 56 | 51 |
| r200-300 | **US** | 267 | **33%** | 20 | 113 |
| r300+ | THEM | 2,894 | 49% | 82 | 58 |
| r300+ | **US** | 380 | **15%** | 22 | 178 |

**Read the first row before the rest.** Before r150 we are *more* forward than
they are (41% vs 38%) and our turrets sit closer to their core (37 vs 45).
**There is no early doctrine gap.** Everything opens at r150:

- **Volume**: their builds hold at ~840-2,900 per band; ours fall to 257-380.
  The r0-150 ratio is 2.0x; by r300+ it is **7.6x**.
- **Direction**: they hold ~50% forward for the whole game. We drop 41% → 31% →
  33% → **15%**.
- **Drift**: their median turret walks *outward* from their core (25 → 61 → 56 →
  82). Ours stays pinned home (25 → 18 → 20 → 22).

At r300+ our median turret is **178 d² from the enemy core against their 58** —
three times further out of the fight.

## 4. THE SYNTHESIS, and it makes the raider curve a consequence

Three instruments, three different data paths, one boundary at **r150**:

1. conversion ratio hits parity at r150-200 and inverts after (free metadata),
2. raider survival collapses 43 → 6 rounds at r150 (replay throws),
3. our turret production and forward placement both collapse at r150 (replay
   builds).

**(3) is a plausible cause of (2).** A field that stands ~2 new gunners per game
forward of midfield from r150 is a field in which a builder bot thrown into that
half lives six rounds. We do not need a separate explanation for the raider
cliff; the forward turret line is one.

**And it reframes the Loki problem.** "Raise the r200-300 conversion ratio" has
been read as *find a new offensive mechanism*. The corpus says the field's
mechanism is not new and not exotic: **it is gunners, built continuously, placed
forward, all game.** We already build gunners — we stop at r150.

## 5. WHAT WOULD FALSIFY THIS — and the confound I cannot remove

**The confound is economic, and it is serious.** Teams that are winning have more
titanium and more surviving builders, so they build more turrets *because* they
are ahead. Production and success are jointly determined here, and nothing in
this document establishes direction. A skeptic can read §2 as "winners build
turrets" rather than "turret builders win", and the data cannot refute them.

What survives that objection, and is the reason I would still act on it:
- **The placement drift is not an economy signal.** A richer team builds *more*
  turrets; it does not have to build them *further forward*. Their median build
  walks from d²25 to d²82 from their own core while ours walks from 25 to 22.
  That is a directional choice, not a budget.
- **The r0-150 parity is the internal control.** If we simply had less money all
  game, we would be behind early too. We are not — we are 2.0x behind early and
  7.6x behind late, from a position where we place turrets *more* forwardly than
  they do.

**Cheapest discriminator, builder's lane:** a variant that only removes whatever
stops late turret production, changing nothing else, measured on turrets built
in r200-300 (mechanism metric, not net Elo) against the matched unrated fixture.
If production rises and the conversion ratio does not follow, §4 is wrong and
the deficit is elsewhere. **I have not identified the code that stops it** — that
is a code read I have not done, and it should precede any build.

Other limits: per-opponent coverage is 8-23 archived matches, our-games-dominated
(so "Ouroboros never throws" = never against us in 17 matches). `shot` counts
match a `fireTurret` origin to a turret standing on that tile — co-located ties
are possible. Throws landing exactly one tile away are undercounted. Round bands
are game rounds, not wall-clock.

## 6. THE WEAK CLAIM, PINNED DOWN AT THE BUILDER'S REQUEST

My earlier relay noted that launcher use correlates *negatively* with late
conversion (Ouroboros: 0 throws, best late killer; Memtrace: 8,636 throws, one of
the weakest). The builder is right that this is **confounded by team strength
across only 8 opponents on an archive dominated by our own games**, and it is
fully compatible with "throwing is fine, strong teams simply have better tools".
**It is recorded here as weak and must not be quoted at the weight of §1 or §3.**
Nothing in this document's conclusions rests on it.
