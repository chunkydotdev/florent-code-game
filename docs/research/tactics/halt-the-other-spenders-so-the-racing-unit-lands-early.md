---
tactic: When one unit must win a race, the OTHER producers stop for a turn so it can be afforded — concentration of a shared bank, not a bigger bank
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019 / smite (1st place, seeding tournament)
evidence: documented
transfers: partial
---

## WHAT IT IS — arm A: a team that diagnosed a race and shipped a specific mechanism for it

smite diagnosed their game as a race to contested resource clusters, and stated
the deciding variable as *when* their unit arrives rather than *what* it is:

> *"We settled on building up to three units as early as possible, and sending
> them sprinting across the map to the optimal enemy resource clusters."*

They then flag the operative phrase themselves:

> *"there’s one keyword here: as early as possible"*

The intervention is not a faster unit or a shorter path. It is a **team-wide
spending freeze that concentrates a shared bank onto the racing unit.** Each of
their castles independently computes whether *it* is the closest to a target
cluster, and:

> *"If I’m not the closest castle, I don’t just continue with my standard
> pilgrim-production. Instead, I return immediately, halting all production for
> one turn."*

with the reason given explicitly:

> *"Otherwise, it’s very difficult for the harass-producing castle to have
> enough karbonite to produce the attack unit."*

and — unusually for this corpus — **the outcome stated as an arrival round**:

> *"With this production-halting hack, our harassers emerge from castles around
> turn 4-6, early enough to beat enemies to most clusters."*

**Referent check.** "I" is a castle executing the shared `Player` code (their
castles each run the same logic and had already *"spent the first three turns
castle-talking their locations"*); "the harass-producing castle" is whichever
castle won the closest-to-cluster computation; "the attack unit" is the harasser.
The halt is a **non-racing unit deferring**, not the racer waiting.

Note the shape (**my gloss, not their words**): it is **not** a reserve. A
reserve is a floor — do not spend below X. This is the opposite — the units
that are not on the critical path stop spending entirely, for exactly as long
as it takes — and it is self-terminating,
because the halt is recomputed each turn from the same closest-castle test.

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**The precondition is exactly our situation and it is unusual.** This works
because titanium (their karbonite) is a **single global pool spent by many
independent decision-makers running the same code**, with no way to earmark. Our
`get_global_resources()` is precisely that, and `run()` is called once per unit
per round for every living unit — so every builder is a competing claimant on the
same bank, exactly like smite's castles.

We have **floors** but no **halt**. `bots/_v148ferryfirst` carries
`LOKI_FWD_TI_FLOOR = 40`, `LOKI2_RUSH_TI_FLOOR = 8`, `SIEGE_HEAL_RESERVE_TI`,
`SURGE_TI_FLOOR = 1500`, `MEDIC_TI_FLOOR = 20`, `REPLACE_TI_FLOOR = 250`
(`doctrine.py`). **Every one of them protects the bank from the spender that is
about to act.** None of them makes a spender *stand down so a different unit can
afford something*. A grep of `eco.py` for `priority|preempt|yield|defer` returns
nothing — the economy never defers to the raid.

The lever that matters for us is the forward SENTINEL. `raid.py:407-412` gates
it on `LOKI_FWD_MIN_HARV = 2` harvesters **and** a 40 Ti bank floor *after*
paying. `doctrine.py:1229` records the measured failure this creates: on the
LOKI-2 smoke *"the control planted 3 forward sentinels and the variant planted
1"*, and the whole forward arm exists because *"99.3% of early core kills are
turret fire"* with a corpus recipe of *"3 turrets by r22"*. **A sentinel is 30 Ti
base at scale, and every builder bot already added +20% to the global additive
scale before it is bought** — so the round on which the first forward sentinel
becomes affordable is directly set by what everyone else spent that round.

**EFFECT ON MEDIAN KILL ROUND: PREDICTED EARLIER.** This is a pure tempo plank
with no defensive component; it moves the first forward-turret round earlier and
nothing else. It is the one plank in this sweep that should *fail* the bar if it
regresses, rather than merely needing to clear it.

## WHAT WOULD KILL IT

* **The buffered store makes the coordination one round late.** smite's castles
  coordinated by *"castle-talking"* over three turns before it mattered. Our
  writes are visible only next round, so a halt signalled this round takes effect
  next round — and a builder that reads a stale "halt" flag stands down for a
  round after the purchase already happened. **A halt that is one round late is a
  pure tempo LOSS**, which inverts the plank.
* **Our halt has a cost theirs did not.** A builder that stands down has spent
  its action for the round doing nothing; an idle builder is exactly the defect
  sweep 23 identified as ours (`the-idle-forward-unit-gets-a-destination-not-a-recall`).
  smite's castles lost one turn of *production*; ours would lose one turn of a
  *unit*.
* **Cost scale runs the wrong way for a hoard.** Waiting does not make the
  sentinel cheaper — scale is additive on builds, not time — so the halt only
  pays if the bank genuinely binds. If the binding constraint is
  `LOKI_FWD_MIN_HARV` (a harvester prerequisite) or arrival rather than money,
  the halt buys nothing. **`doctrine.py:1456` says ARRIVAL is the scarce
  quantity, which is a live argument against this plank and must be checked
  first.**

## BUILDER HOOK — smallest thing that would test it

**Measure before building.** No code change: over our own corpus, on games where
a forward sentinel was eventually planted, compute the number of rounds between
the first round a raider was in position with `can_build_sentinel` true, and the
first round the bank covered `get_sentinel_cost() + LOKI_FWD_TI_FLOOR`.
**If that gap is ~0,
the bank does not bind and this plank is dead for free.** If it is materially
positive, the halt has something to buy and the number is its ceiling.

If it survives that: the smallest implementation needs **no new store slot** (the
16 are fully bound, `doctrine.py:931-961`, `:1166-1170`) — `SLOT_RAID_LIVE`
already carries a foothold heartbeat, so a builder that can read "a raider is
established at the ring" can gate its own discretionary spends (medic heals above
the floor, non-trunk conveyors) on the bank being above sentinel cost, with no new
signal at all. That is smite's halt with our existing wiring, and it inherits the
one-round buffer lag as a known, bounded cost.
