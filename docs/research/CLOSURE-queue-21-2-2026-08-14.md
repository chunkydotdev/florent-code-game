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

# SIZING RULE THAT CAME OUT OF #17 — MOVED, NOT RESTATED

**⇒ THE AUTHORITY IS `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`,
Addendum 11 / OBLIGATION 16** (`45dc0245`): *a BAR carries a pre-specified MDE, or it
cannot be sized and every attempt to size it is circular.*

**IT IS NOT RESTATED HERE ON PURPOSE.** I first wrote it into this file — a dated closure
doc **no lane boots** — which is the s29 finding (*a rule promoted into a file nobody
opens*) committed against **a rule about rules**. The side lane rehomed it into the
obligations doc, which **is** in a boot sequence and **is** where preregs are actually
written. Two homes for one rule is the next defect and the copy in the un-booted file goes
stale first, so this is a pointer and stays a pointer.

The origin, for provenance only: #17's re-run was sized off the point estimate of the
underpowered run it was replacing. **Both lanes own a half — I sized off that estimate;
the side lane certified the arithmetic without asking whether the input was legitimate.**
Full statement, the n-explosion table and the rider live at the authority above.
