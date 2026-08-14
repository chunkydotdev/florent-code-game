# CLOSURE — QUEUE #21 (gunner count) and #2 (off-axis sentinel). 2026-08-14, builder s43.

Both NOT DRAFTABLE. **#21 closes at the RULES LEVEL, which under `CLAUDE.md`'s
carve-out needs no live game.**

## #21 — THE ROW'S OWN LEVER CANNOT DO WHAT THE ROW CLAIMS

**The sweep's premise for re-running GUNADD is false.**
`QUEUE-ECONOMICS-SWEEP-2026-08-14.md:112,218` ranks *"#21 — re-run GUNADD"*
top-5 build-ready on the grounds it *"was cancelled at n=388 with NO RATE
PRINTED"*. Verified against the tape by the builder, not relayed:

    scratchpad/overnight/GUNADD.tsv   n=388   T=194   C=194   share = 50.00%

A rate exists and it is dead flat — exactly 194/194.

**⭐ AND IT HAD TO BE FLAT: THE GUNNER BRANCH CAN NEVER ADD A TURRET.**
At the `LOKI38_GUNADD_ON` branch (`raid.py:452`) the gunner's admissible set is a
**strict subset** of the sentinel's:
* gunner needs `d^2 <= 13`; the enclosing loop already demands `<= 32`;
* `can_fire_from(...GUNNER...)` needs an **unobstructed** ray, while SENTINEL
  **ignores obstacles**;
* the outer gate at `raid.py:659` has **already reserved the higher sentinel
  cost**, so affordability cannot separate them inside the function.

⇒ It can only change the **TYPE** of a turret the incumbent was already going to
build — trading 18 dmg / reload 2 for 7 dmg / reload 1 against a 500 HP core to
save 10 Ti at an identical +20% scale contribution. Positive control: **6 of 6**
gunner-hits were followed by a sentinel build at the **same candidate** in the
same invocation. The tree's own docstring claims *"ADDITIVE, not a swap ... can
never remove a turret the incumbent would build"* — **the first half is false.**
This is the game's own predicate algebra, so it closes without a live leg.

**Dose, measured on the v140 chassis (90 games, 1,582 scans):** the GUNADD branch
fires **6 times = 0.067/game = 4.9% of forward turret builds**. A pooled n=5,400
screen measures that as **zero by construction** — the same arithmetic the sweep
itself applied to LAUNCHOFF/#51. Re-running it would have spent 5,400 cores on a
predictable non-experiment.

**Where forward turrets actually die:** **90.6% on the bank floor
`LOKI_FWD_TI_FLOOR = 40`** (`raid.py:659`), not the cap (1.3%). Relaxing that
floor is **already screened NEGATIVE** — `FWDFLOOR8`, n=2,787, share **45.89%
+/- 1.84**, outside-below. The binding constraint is **geometry** (our own collar
blocking `can_fire_from(GUNNER)`), and geometry is not a constant.

## #2 — DUPLICATE, then PREMISE-THIN

* Its **positioning** half is the already-locked and running `sentthreat` arm: a
  penalty on the on-axis tile among 12 ring stations **is** a preference for the
  off-axis one — same function, scorer, rescan and constant. No residue.
* Its **hunt** half is premise-thin at the enemy ring: `<= 0.81` reachable enemy
  sentinels/game against **20 builder-attacks and 40 Ti** per 40 HP kill, and on
  a seat `_raid_act` step 1 pre-empts step 6, so it would never peck anyway.

**⭐ RE-SCOPE, now in prereg as `finishhp`:** the same mechanism at the **HOME
SIEGE BAND** has **2.7-4.8x the population** — enemy turrets at `d^2 <= 8` of our
core **0.856/game**, at `d^2 <= 41` **2.214/game** (571 archived v140 games). And
`doctrine.py:169-235` is a ~65-line **present-tense spec with SEVEN constants
read zero times**, whose own text records a builder sitting at `d^2 = 2` from a
**4/40 HP** enemy sentinel for **283 rounds** without attacking it, because the
universal adjacent heal claims the action and returns.
**It is DEFENCE** and carries the kill-round non-regression bar **phrased as an
exclusion**.

## CORRECTION OWED TO THE LOCKED `sentthreat` ARM
It attributes *"86-89% of them forward"* to v140 citing `coordination.md:49134`;
that line carries only v140's **4.59 sentinels/game**. The 86-89% figure is
**Leviathan's**. v140's own is **65.4%** within `d^2 <= 41` of the opposing core.
Does not change that arm's design; it **misdescribes its threat population.**

## HOUSEKEEPING
Seeds **316001-316030 are burned** by the #21 probe (direct `fcode run`, no shard
tape). A future leg starts at **316100+**.

---

# PROMOTED RULE — SIZE OFF THE VALUE YOU MUST EXCLUDE, NOT THE ONE YOU HOPE TO OBSERVE
*(2026-08-15, builder + side lane, arrived at from opposite ends of the same error.)*

**THE ERROR.** #17's bar is *">=10.0% of cell-P games contain a destruction"*. The n=60
run read 5.0%, Wilson [1.71, 13.70] — unresolvable. The re-run was sized **off that 5%
point estimate**: hw +/-2.47pp at n=300, which "excludes 10.0%". The re-run then measured
**8.00%**, Wilson [5.43, 11.63] — **still containing the bar.**

**WHY IT WAS CIRCULAR: the estimate being corrected is the estimate used to size the
correction.** And the required n explodes as the truth approaches the bar:

| assumed truth | n/cell to put the CI's upper edge below a 10% bar |
|---|---|
| 5% | 73 |
| **8% (the actual)** | **707** |
| 9% | 3,147 |
| 10% | infinite |

⇒ **An estimate near the bar can never tell you how much data the bar needs.** Sizing off
ANY observed point estimate carries this, including the 8%.

**THE RULE.** A BAR must carry a **pre-specified MDE**, declared before any row exists:
*"we will call it a miss if the true rate is at or below X."* Size to exclude **X**, never
to confirm the hope. **A bar with no MDE beside it cannot be sized at all, and every
attempt will be circular.** This is Obligation 12 (a gate carries its own resolution
statement) reached from the other end — for BARS rather than GATES.

**PROVENANCE, because how it arrived is the point.** The builder made the sizing error and
published it; the side lane had **certified** that sizing — verifying the arithmetic while
never asking whether **p=5% was a legitimate input**. Their words: *"I verified the
CALCULATION and never asked whether the premise was true."* **Both halves are the same
defect — ARITHMETIC VERIFIED, PREMISE UNASKED — which is why a certification did not catch
it.**

**AND THE DECISION IT DID NOT CHANGE:** #17 was NOT re-fired at n=707. Lethality on
landing is 1.00 (128/128) and delivery is ~8% of games (24/300), with the guarded control
taking 104 border arrivals and dying zero times. **The bar had become the least
informative number in the leg.** Stopping is the correct call, not a concession.
