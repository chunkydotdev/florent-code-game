---
tactic: Sentinel file — stack obstacle-ignoring shooters on one ray to beat the adjacency heal cap
source: https://wiki.screepspl.us/Combat/ (damage-vs-heal doctrine); the formation itself is unsourced
origin: inference by tactics sweep 2 applied to our ruleset; Screeps combat doctrine for the framing only
evidence: documented — engine probe, 2026-08-09 (was: inference)
transfers: partial — LEGAL AND PROBED, BUT THE ECONOMICS SHRINK THE CLAIM
---

> **⛔ CLAIM DOWNGRADED 2026-08-09 (s23), by my own arithmetic.** I billed this as
> *"the one mechanism that beats the 2.2:1 defensive edge by concentration."*
> **Against a defender who actually mans the heal cap it does not.** Sentinel = 9.0
> HP/round each; a 2×2 core with 8 healers cancels 32 HP/round, so a file needs **N=4
> minimum and N=6 for pace** — and the full exchange is:
> ```
> N=6 vs maxed core: 23 rounds to kill
>   attacker 298 Ti sentinels + 682 Ti AMMO = 980 Ti
>   defender 182 Ti of healing        ->  5.4 : 1 AGAINST the attacker
> ```
> **The ammo dominates, and ammo is the line we are already worst at.**
>
> **What survives is smaller and better evidenced: against the MEASURED field detail
> of 2.68 adjacent healers (10.7 HP/round), N=2 already wins at +7.3 HP/round** — and
> the broad field **does not scale its guard** (no-us games cancel 34.6%, TOP ≥1750
> 31.5%). **Two sentinels beat most of the ladder's actual defence; six lose to a
> theoretical maxed one.**
>
> **Legality was never the binding constraint. The cap was — and the cap is rarely
> manned.** Full arithmetic in
> [`../turret-line-blocking-2026-08-09.md`](../turret-line-blocking-2026-08-09.md).

> **UPDATE 2026-08-09 (s23): the decisive unknown below is RESOLVED, and the
> answer is the favourable one.** Probed with the gunner as a positive control
> (`docs/research/turret-line-blocking-2026-08-09.md`):
> - `can_fire_from` GUNNER **True → False** with a friendly barrier in the line —
>   control passed, method sound.
> - `can_fire_from` SENTINEL **True → True**, and a **real sentinel landed a real
>   shot for −18 HP (= `SENTINEL_DAMAGE`) straight through our own builder bot AND
>   our own barrier.**
>
> **Sentinels do not block each other. The file formation is legal.** Kill
> condition (d) below is struck. Conditions (a) 50-unit cap, (b) +20% scale, and
> (c) reload-2 throughput all still stand — **legal is not the same as affordable**,
> and nothing here says the formation wins.

WHAT IT IS — **Inference by tactics sweep 2. There is no source for this
formation; do not attribute it to any team.** The reasoning:

- The defender's heal throughput **at any one tile** is hard-capped by orthogonal
  adjacency: at most **4 builder bots** can heal a given tile, so **≈16 HP/round
  for 4 Ti/round**. There is no way to add a fifth.
- The attacker's damage **at that same tile** is capped only by titanium.
- **Sentinels ignore obstacles.** So in principle any number of sentinels can be
  stacked in single file along the same ray, all firing *through each other* into
  the same tile.

WHY IT MIGHT TRANSFER — **This is the structural break in the 2.2:1 defensive edge,
if it exists anywhere.** The defender's heal is a *linear-law, density-capped*
resource; the attacker's fire is a *concentrable* one — the Lanchester distinction.

Sentinel: 18 damage, reload 2 → ~6-9 HP/round each. Against a 16 HP/round cap you
need **2-3 sentinels bearing on one tile** to make net progress, and **every
sentinel beyond that is pure surplus the defender cannot answer.** Barriers do not
help them: sentinel line shots pass straight through.

This is also the arithmetic behind the alpha-strike discipline in
[sweep 2](2026-08-09-sweep-2.md): sub-threshold damage is not merely inefficient,
it is a **2.2:1 donation.**

WHAT WOULD KILL IT — four things, and the fourth is decisive:

1. `MAX_TEAM_UNITS = 50` caps the fleet alongside builders and harvesters.
2. Sentinel scale is **+20% each** — the 6th costs ~3× base. The surplus is not free.
3. If `reload 2` means firing every 3rd round, per-sentinel rate drops to ~6
   HP/round and you need 3+ just to break even.
4. ~~**UNVERIFIED AND DECISIVE: whether two sentinels on the same ray can both hit
   the same tile.**~~ **RESOLVED 2026-08-09 — friendly entities do not absorb a
   sentinel's shot (measured, with a gunner control).** One residue: the blockers
   tested were a builder bot and a barrier, **not another sentinel**. Assumed
   equivalent since both are buildings, but that specific case is untested.

BUILDER HOOK — **the gating probe is done and passed.** The next question is no
longer legality but economics: at +20% scale per sentinel and reload 2, how many
sentinels can we field before the marginal one costs more than the heal it
out-paces? That is arithmetic against `get_sentinel_cost()`, not a battery.

**The probe's by-product is the more urgent item**, and it cuts the other way:
**GUNNER lines ARE blocked by our own bots and buildings, while
`get_attackable_tiles()` reports the target as attackable anyway.** Siting logic
scored with that function is scoring coverage the gun will not deliver — and with
41,921 gunner builds against 13,298 sentinel, gunners are the dominant case.
**Corollary: gunners and sentinels want OPPOSITE geometry** — a gunner needs a
clear lane, a sentinel can sit behind our own wall. A ring that places both by one
rule is wrong for one of them.

Related: [sweep 2](2026-08-09-sweep-2.md) ·
[heal arithmetic](../heal-arithmetic-2026-08-09.md) ·
[machinery audit](../machinery-audit-2026-08-09.md) (sentinels cannot rotate — so a
mis-sited sentinel file cannot be re-aimed, only destroyed and rebuilt)
