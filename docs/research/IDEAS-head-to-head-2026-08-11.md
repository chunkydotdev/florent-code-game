# THREE HEAD-TO-HEAD IDEAS + PRECONDITIONS (Magnus's trigger, 2026-08-11)

**Research arm, s30. Magnus: *"trigger the other arms and make them give you at
least 6 new total ideas to run head to head against v104."* These are my three
(the side lane is asked for three more). Each is flag-sized against
`bots/_v130loki13`, names its `file:line`, and states its precondition MEASURED
or explicitly UNMEASURED. Relayed live to the builder; recorded here because
relays die with the session.**

**The builder owns the prereg, the bot, the dose check and every verdict.**

---

## ⛔ FIRST — A PRECONDITION THAT KILLS AN IDEA BEFORE IT IS PROPOSED

**We are NOT ammo-starved. We are TARGET-starved.** `econ.tsv`, last band row per
game, ammo left in the bank at game end:

| team | games | median `ammo_end` | % games ending <10 | turrets/g | shots/g |
|---|---:|---:|---:|---:|---:|
| **OpenSverige** | 5,048 | **28** | **21%** | 12.6 | **67** |
| Erebus | 445 | **4** | 75% | 12.0 | **247** |
| Lorem Ipsum | 360 | 8 | 51% | 9.4 | 161 |
| sporks | 537 | 20 | 13% | 14.9 | 95 |

**Erebus fires 3.7× our shots on the same turret count and runs its bank dry.**
⇒ *"convert more ammo"* is dead as a plank, and the builder's idle-gap histogram
should discriminate **reload vs targets**, not ammo vs anything.

---

## IDEA 2 (my highest confidence) — **THE OWN-CORE HEAL BUDGET**

**We spend 272.8 Ti/game healing, 228.0 of it on our own core. Our opponents
spend 69.2.** A heal is 1 Ti, so heal actions are titanium one-for-one. Measured
on the LOKI-19 control arm, v104, **50/50 games**.

**We heal 3.9× more than the teams we play**, and 228 Ti/game is roughly **seven
sentinels** at base cost.

* **Mechanism:** healing our own core converts titanium into survival at
  0.25 Ti/HP instead of into damage — the purest `PLAY_DEFENCE: never` violation
  in the tree.
* **Diff:** `K_HEAL_RATE_PCT = 5` (`doctrine.py:376`), `K_HEAL_BASE_GRANT = 30`
  (`doctrine.py:375`), published at `main.py:198` (single publisher, so the diff
  reaches the metric). Floors: `MEDIC_TI_FLOOR` (`doctrine.py:259`),
  `SIEGE_HEAL_RESERVE_TI` (`doctrine.py:437`).
* **Precondition: MEASURED and unusually clean — no dose risk at all.** 272.8
  actions/game in 50 of 50 games.
* **⛔ Strong counter-argument:** the core is healed because it is *damaged*; this
  may be load-bearing. **The archive cannot separate wasteful from load-bearing
  healing — self-play against v104 settles it in 64 free games**, because v104
  attacks the way we attack.
* **Either branch is worth knowing:** if healing is simply correct for both sides,
  **LOKI-21's eviction plank gets MORE valuable, not less.**

## IDEA 1 — **STOP BUILDING HOME TURRETS**

* **Mechanism:** 56% of our turrets are home turrets on a never-play-defence
  programme; nothing enters their range. Each costs 20–30 Ti **and +20% global
  scale**, and fires almost nothing.
* **Numbers:** forward share **43.7%** vs band **58%**, top **63%**, rank
  **44/72**. **5.34 shots/turret, rank 61/72** (league median 12.89). Not
  ammo-limited (table above). Clankers (2040) runs 3.6 turrets, 63% forward.
* **Diff:** home build path `main.py:566–576`, reached via the defend-seat branch
  at `main.py:321` (`LOKI_DEFEND_SEAT`, `doctrine.py:1192`; `DEFEND_BEAT_*`
  `doctrine.py:694–698`). Cap turrets with `d2_own < d2_enemy`, or gate the
  defend-seat turret build. Forward path `raid.py:435–439` untouched.
* **Precondition: MEASURED** (the home turrets exist and are the majority).
  **UNMEASURED: whether they are load-bearing against real incursions** —
  self-play is the falsifier.
* **⚠ The case is the MECHANISM, not the correlation.** Forward share does **not**
  predict rating within our band (+0.090, n=23). It only separates functional
  teams from broken ones league-wide.

## IDEA 3 — **BARRIER THEIR ORE TILES** (a carve-out `CLAUDE.md` itself calls unmeasured)

* **Mechanism:** a barrier is **3 Ti, +1% scale — the cheapest thing in the
  game**. On an enemy-side ore tile it blocks the harvester; clearing it costs
  them **15 builder-turns and 30 Ti** (30 HP ÷ 2 dmg at 2 Ti a swing). ~10:1.
* **Precondition: MEASURED, 25,900 opponent harvester builds in our games** —
  median build round **31**, **45% after round 40**, **32% after round 80**. The
  window is wide open. *(Our own median harvester is r43, so raiders are already
  out then.)*
* **Diff:** one branch on the existing raider build path (`raid.py:435–439`
  already builds forward). **Check `E2B_ORE_PAVE_BAN_ON` (`doctrine.py:565`)
  first — it already encodes "do not build on ore", so this may be a scoped
  exception rather than new code.** Also `ORE_STEPOFF_MIN_WALLS`
  (`doctrine.py:167`).
* **⚠ UNMEASURED:** how often a raider is *actually adjacent* to a still-empty
  enemy ore tile. **The 45% is an upper bound on the WINDOW, not a dose** — same
  caveat as LOKI-21's 233 rounds/game.
* **On-programme:** denial, not defence. The refuted ore-poisoning result killed a
  **price** computed under the retired `titanium_collected` currency; the
  mechanism was engine-confirmed.

## IDEA 4 — filler, and I am least confident in it

Harvesters **6.4/game** vs Clankers 4.9 and a top-tier mean near 5, each **+5%
scale**. `ECO_CAP = 18` / `ECO_NEED = 3` (`doctrine.py:30–31`). **The correlation
argues AGAINST it** — r(rating, harvesters/game) = **+0.250**, mildly positive —
and only the scale-tax mechanism argues for it. **Flagged as weakest rather than
padding the count.**

---

**My confidence order: 2 (biggest number, cleanest dose, cheapest falsifier) ·
1 (strongest mechanism, needs the self-play falsifier) · 3 (best programme fit,
weakest dose evidence) · 4 (would not fire).**

**Nothing here is a verdict and none of it has been tested live.**
