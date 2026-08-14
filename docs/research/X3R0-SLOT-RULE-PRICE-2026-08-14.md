# X3R0_SLOT_RULE, PRICED IN THE LADDER'S OWN CURRENCY — 2026-08-14 (research arm, s42)

**WRITTEN WHILE THE RULE WAS FIRING.** x3r0 uploaded **v145 "Top Team Router v3" at
2026-08-14T19:08:37Z, `isActive=true`**, displacing our v140. The builder is staging the
standard response (artifact + `SCREEN-v140vs145` prereg + n=1000 local screen; ≥51.0
reactivates v140). This document does not tell that decision what to do. **It prices the
one quantity the decision turns on and nobody had computed: what an hour of screening
latency costs.**

**Live version at write time: v140 = `bots/_v223sealrepair` (displaced 19:08:37Z).**
**Population: `corpus/ladder_games.tsv`, 285 rated game rows across 57 matches with
`created` on 2026-08-14.** Corpus synced 19:1xZ, newest `league_matches` row 18:52:59Z.
**Never `meta_join` for a rated denominator** — it pools rated with our own unrated legs.

---

## 0. RULING, up front

**An hour of x3r0 holding the slot costs us ≈ −11.5 Elo, measured.** The ladder paired at
a median of **20.0 minutes** today (n=56 gaps) ⇒ **3 rated matches/hour**, and x3r0-held
versions ran at **−3.84 Elo/match** across 19 matches. **A four-hour screen therefore
spends ~46 Elo to avoid reactivating a bot that might have been fine.** Whether that is
worth paying is the builder's call and depends on how fast the local screen runs — which
is why the number is delivered as a price and not as a verdict.

**And one thing this data does NOT support, stated because it is the claim most likely to
harden into doctrine this week: "x3r0 uploads are bad" is not established.** The −74.60
result is solid and belongs to **four named versions**. Two further x3r0 versions cost
essentially nothing. The prior does not decide v145 — **which is the actual argument for
running the screen.**

---

## 1. THE INHERITED NUMBER, RE-DERIVED BEFORE IT WAS USED

`HANDOVER.md` carries *"X3R0_SLOT_RULE cost measured for the first time: −74.60 Elo over
v134–v139"*. A prescription that cites a number re-derives that number first (side lane
S1, 2026-08-14). **It reproduces to the digit:**

| block | matches | games | wins | share | net Elo | `ourbef` span |
|---|---|---|---|---|---|---|
| v134/135/137/139 | 15 | 75 | 25 | **33.3%** | **−74.60** | 1797.2 (06:32:59Z) → 1724.2 (11:52:59Z) |

Elo recomputed from the engine-exact rule, not read off a tape:
`delta = 32 × (S − E)`, `S = games won / 5`, `E = 1/(1+10^((oppbef−ourbef)/400))`
— the form verified at max |residual| = 0.000000 across 100 matches (s28).

---

## 2. THE DAY DECOMPOSES BY WHO HELD THE SLOT

```
per-version, 2026-08-14, corpus/ladder_games.tsv
ourver  matches games  share   netElo  Elo/match
   125       20    100  52.0%   +17.58     +0.88   <- ours
   134        3     15  40.0%   -11.52     -3.84
   135        1      5   0.0%   -13.89    -13.89
   137        3     15  33.3%   -14.26     -4.75
   139        8     40  35.0%   -34.93     -4.37
   140       18     90  62.2%   +67.71     +3.76   <- ours
   142        2     10  60.0%    -0.37     -0.18
   143        2     10  60.0%    +2.04     +1.02
```

| held by | matches | games | share | net Elo | **Elo/match** |
|---|---|---|---|---|---|
| **OURS** (v125, v140) | 38 | 190 | **56.8%** | **+85.29** | **+2.25** |
| **X3R0** (134/135/137/139/142/143) | 19 | 95 | **38.9%** | **−72.92** | **−3.84** |

**Interval, DEFF-corrected.** Cluster enumeration performed, not asserted: within a
version block a stratum holds **many games per match** (5) **and many matches per
opponent** — **both clusters survive** ⇒ the pooled rated constant **DEFF = 1.529**
applies to both arms.

```
half_width_95 = 1.96*sqrt( p̄(1-p̄) * ( 1.529/190 + 1.529/95 ) ) = 15.2pp
diff = 56.8% − 38.9% = 17.9pp   ⇒  EXCLUDES ZERO
```

⚠ **IT CLEARS BY 2.7pp ON A 15.2pp INTERVAL.** This is an **exclusion** claim, so the
DEFF correction makes it *harder* and applying it is the honest direction — but
`CLAUDE.md`'s direction clause names "claims that cleared a bar NARROWLY" as the exposed
class, and this is one. **Directional finding, not a constant.**

---

## 3. THE PRICE OF LATENCY — the number the decision actually needs

The rule's cost is **not** the cost of x3r0's versions playing; those matches happen
whether or not we have a rule. **The rule's cost is the window between their upload and
our reactivation** — the time we spend screening.

```
pairing gaps, 2026-08-14: n=56, median 20.0 min, mean 20.0 min   ⇒ 3 rated matches/hour
```

| prior on v145 | Elo/match | **cost per hour of screening** |
|---|---|---|
| x3r0-held mean (all 6 versions, n=19 matches) | −3.84 | **−11.5 Elo/hour** |
| the bad block only (134/137/139, n=14 matches) | −4.99 | **−15.0 Elo/hour** |
| v142/143 only (n=4 matches) | +0.42 | **+1.3 Elo/hour** (i.e. no cost) |

⇒ **the screen is worth its latency iff it finishes fast.** A 1-hour screen costs ~12
Elo; a 4-hour screen costs ~46 — comparable to the entire −74.60 the rule exists to
prevent. **The binding constraint on X3R0_SLOT_RULE is turnaround, not correctness.**

### 3b. ⭐ AND THE ELO IS THE SMALLER HALF OF THE BILL

**`fcode match unrated` plays the ACTIVE SUBMISSION — there is no flag for a local tree.**
That is the constraint this repo has lived with since 2026-08-10, and it has a consequence
nobody has priced: **while a version we did not write holds the slot, the entire unrated
fixture is dark.** Every leg's holder-assert-per-fire guard voids its window (which is
exactly why CAL-8's resume is blocked right now, at 2 accepts from a legal read).

**The unrated cap is 5 matches / 20 minutes ⇒ 15 matches = 75 games per hour of
measurement capacity.** So an hour of screening latency costs:

```
  −11.5 Elo   (rated, measured above)
+  75 games   of FIXTURE_OF_RECORD capacity, unbuyable later
```

⇒ **the −11.5 Elo/hour is the FLOOR of the price, not the price.** The lane-structure
review's central finding was that this fixture already runs at 8–20% of its cap; holder
displacement is one of the mechanisms that keeps it there, and it is the one we have a
protocol for. **This strengthens rather than softens the conclusion: turnaround is the
binding constraint, and it binds on both currencies at once.**

---

## 4. ⛔ THE DOCTRINE THIS DATA DOES NOT SUPPORT

**"x3r0 uploads are bad" — NOT ESTABLISHED, and the failure is one of population.**

* The **−74.60 is real** at n=75 games and belongs to **v134, v135, v137, v139**.
* **v142 and v143 ran 60.0% share over 20 games for +1.67 Elo net.** They point the other
  way.
* **I cannot promote that to "some x3r0 uploads are fine":** 20 games at 60% carries
  **±26.6pp** (DEFF 1.529) and does not distinguish itself from the bad block. *(That is
  the honest reading of my own counter-evidence, and it stays honest in both directions.)*
* **But it is sufficient to block the general claim.** Extending a four-version result to
  "x3r0 uploads generally" rests on 20 further games that resolve nothing.

⇒ **The prior does not decide v145. That is the argument for the screen, and it means the
screen needs a bar that can genuinely fail** — not a formality en route to a foregone
reactivation.

---

## 5. WHAT WOULD MAKE ME WRONG

**These blocks were not randomised.** They ran in different windows against different
pools. Pricing in **Elo rather than share** is a deliberate partial defence — the `E`
term conditions on opponent rating — but two threats survive it and both are named
rather than waved off:

1. **Reverse causality.** If x3r0 tends to upload *after* a bad run, the blocks are
   selected on the outcome. **I cannot exclude this from observational tape.** (Testable:
   correlate upload timestamps against the preceding 5-match Elo trend. Not run.)
2. **Window effects.** A third cluster — time slice — is hypothesised but never measured
   in this repo. If it binds, the DEFF used here is too small and the 2.7pp margin goes.

⇒ **The local randomised screen is a genuine instrument here, independent of the latency
price.** ⚠ **The −11.5 Elo/hour is a price on TIME. It is not evidence about v145's
quality and must not be cited as any.**

---

## 6. ROUTING

* **Behaviour change → the booted tape** (`docs/coordination.md`, this session): the
  latency price and the "not established" correction.
* **`PROGRAMME.md` owes a line** — `HANDOVER` already records that X3R0_SLOT_RULE should
  be priced in Elo at the next PROGRAMME touch. **The price now exists: −11.5 Elo/hour of
  screening latency, and the rule's binding constraint is turnaround.**
* **Not routed, observation only:** the v142/143 counter-signal, until an n exists that
  can resolve it.

---

## 7. ⭐ CLOSING THE LOOP — WHAT THE v145 WINDOW ACTUALLY COST

**Added ~2 hours after §3 was written, because a price nobody checks against an outcome is
a number rather than a model.**

The window closed early: **Magnus rolled v145 back himself at 19:17:14Z**, ~9 minutes after
x3r0's 19:08:37Z upload. The arithmetic reconciles exactly:

```
18:52:59Z match, ourbef 1789.7, result 3/5   ->  delta +3.88  ->  1793.6
19:12:59Z pairing, ourver = 145              ->  delta -10.00 ->  1783.6
live rating read off `fcode status` via target_value --band:  1783
```
⇒ **the entire cost of the v145 window is ONE rated pairing at −10.0 Elo**, and the whole
of our rating movement since this session's boot reading of 1794 is attributable to it.
Nothing else is hiding in the gap.

**HOW THE PREDICTION DID, scored honestly rather than favourably:**

| | |
|---|---|
| model in §3 | 3 matches/hour × **−3.84**/match ⇒ **−11.5 Elo/hour** |
| realised | **1 match, −10.00 Elo**, over a **0.14-hour** window |
| naive rate | ≈ −70 Elo/hour |

⛔ **THE NAIVE RATE IS NOT A REFUTATION AND MUST NOT BE QUOTED AS ONE.** Two reasons, both
structural:
1. **Pairing arrival is lumpy at this timescale.** A 9-minute window either catches one of
   the 20-minute pairings or catches none. **The per-hour form is only meaningful over
   windows long enough to average pairings**, which is exactly the multi-hour screening
   window it was built to price. Dividing a single catch by 0.14 h estimates the arrival
   process, not the cost.
2. **n = 1.** The realised **−10.0/match** is a high draw against the modelled **−3.84**
   mean, but it sits inside the observed per-version range (v135 read **−13.89**). **One
   draw cannot update the mean and I am not updating it.**

⇒ **the model survives, unrevised, and the honest summary is that this episode did not test
it.** What it *does* confirm is the cheaper claim underneath: **a displaced holder costs
real rated Elo immediately — not eventually, and not only in expectation.** The first
pairing after the displacement was already −10.

**AND THE FIXTURE HALF OF §3b WENT UNTESTED ENTIRELY:** the window was too short for the
75-games/hour of lost unrated capacity to bind. **It bound on CAL-8 all the same** — the
resume was blocked until the rollback, which is the mechanism, observed, at a duration too
small to price.
