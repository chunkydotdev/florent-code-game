# SCREEN PREREG — QUEUE #52 COLLAR MEDIC (`_v232collarmedic`): staff the heal exchange

**DRAFT — not locked until the builder ratifies and commits.** Drafted by a
fresh prereg agent (Magnus's s40 one-agent-per-prereg rule; no inherited
context beyond the named inputs), builder arm, **2026-08-14 ~20:2xZ** (`date
-u` in the drafting shell: `2026-08-14T20:20:19Z`).

**TWO-CLOCK LOCK.** This document's lock time is its **ratifying commit's git
author time**, to be compared against **the first `CMEDICON`/`CMEDICOFF`
heartbeat line** in `scratchpad/overnight/`. Neither shard has been started at
drafting time. ⛔ **If either shard's heartbeat predates the commit, this
prereg is not blind and must be relabelled, not read.**

---

## 0. What this is and where it comes from

QUEUE #52 (⭐ promoted s40 on Magnus's twice-pushed ask, under his s38
deepening directive *"take what we do right and do it even better"*). The row's
premise: our tree already owns a heal exchange **in our favour** and **never
staffs it** — `_heal_adjacent` heals a damaged adjacent friendly building, but
only if a builder **already happens to be standing there**. Nothing in the tree
ever *walks* a builder to a wounded home building.

**THE EXCHANGE IS 4:1, NOT 8:1.** We pay **1 Ti for +4 HP** (0.25 Ti/HP); an
enemy peck pays **2 Ti for 2 dmg** (1.00 Ti/HP); undoing one peck costs us
**0.5 Ti** against the **2 Ti** they spent. The `eco.py` source comment says
*"eight to one"* and **that comment is WRONG** (research s42 correction, carried
in the row). **8:1 is quoted in this document only to flag it.** The plank was
sized on the corrected number: `LOKI_CMEDIC_MIN_DMG = 4` exists *because* at the
true 4:1 a 1-HP top-up is a Ti-neutral trade that spends a whole builder action
(`doctrine.py:1733-1747`).

**FIELD VOLUME (handed, from the row's s40 promotion block):** `build_agg`
`metric=='batk'`, `ourver ≥ 125`, archived — **the field pecks our buildings
85.5 times per game on average, and 19 of 20 opponents with n ≥ 15 games are
non-zero** (Coreflood 196.9/game · Big O 192.9 · Jython 138.9 · Juusto 129.4 ·
lingling_40h 109.1 · 0033 101.8 · team lazy 96.0; the single zero is Leviathan
at 1997.8, who barely pair us).
⚠ **CARRIED CAVEAT, UNRESOLVED AND NOT CLAIMED HERE:** `batk` counts builder
attacks on **any** building of ours. **That the 85.5 lands on the BARRIERS this
plank heals is NOT established** — `BOOK-0033` shows at least one opponent aims
them at the BELT. **No barrier-specific volume claim is licensed by this
document.**

---

## 1. Arms — a one-line ablation, diff verified

| arm | tree | flag |
|---|---|---|
| **TREATMENT** | `bots/_v232collarmedic` | `LOKI_COLLAR_MEDIC_ON = True` (`doctrine.py:1721`) |
| **CONTROL** | `bots/_v232collarmedic_off` | `LOKI_COLLAR_MEDIC_ON = False` (`doctrine.py:1721`) |

**`diff -r` verified at drafting time: ONE line differs** (`doctrine.py:1721`),
plus `__pycache__/*.pyc` byte differences, which are build artefacts and carry
no behaviour. Nothing else in either tree differs.

The plank is three additive methods in `eco.py`: `_collar_patient` (pick +
claim, `:410`), `_collar_medic_heal` (ACTION half, `:446`), `_collar_medic_move`
(DISPATCH/STAY half, `:506`); called from `eco.py:1368` and `eco.py:1405`.
Doctrine block `LOKI-52` at `doctrine.py:1700-1762`: home band `HOME_DSQ = 36`
(the core's own vision), reach `REACH_DSQ = 20` (builder vision — the patient is
*observed*, not remembered), `MAX = 2` medics per patient (local count, no store
slot), `MIN_DMG = 4` (the depth at which the +4 is not clipped),
`TI_FLOOR = 1`, and `CMEDIC_TYPES` = BARRIER first, then the eco chain and home
turrets.

**Instrumentation is ON IN BOTH ARMS** (`LOKI_HEALLOG_ON = True`,
`doctrine.py:1782`) — one `print` per heal landed, tagged by call site. That is
the correct choice (instrumenting one arm only would make the heal comparison
uninterpretable) and it is **LOCAL-ONLY**: platform replays strip `stdout`
(CLAUDE.md, measured 30,664/30,664 empty), so **nothing in this document may
ever be read off a live leg.**

---

## 2. Fixture — and the two ways it is not the field

**FIXTURE: `bots/_probe_creeper`, both arms, local corefill.**

**Why not self-play.** `LOKI_QUIET_ON = True` silences OUR builder melee, so a
self-play screen has **no damage source for the plank to answer** and reads
**HARM ONLY** — the row's COUPLING CLASS is *COUPLED, INCUMBENT-ABSENT*. The
s40 promotion block's finding is that this is a **fixture choice, not a rarity**:
the live customer is essentially every opponent, every game.

⛔ **DECLARED FIXTURE DEFECT 1 — THE CREEPER DOES NOT PECK. IT SHOOTS.**
Verified at drafting time: `bots/_probe_creeper/main.py` contains exactly one
`ct.fire(` call, at `:187`, inside `_gunner_turn`. **Its builders never attack
our buildings.** So the fixture supplies *damage to home buildings* — which is
what the medic's eligibility test actually reads — but **it does not reproduce
the peck shape the row prices.** Consequences, stated so no reader transports
them:
* The exchange under gunner fire is **≈2.3:1**, not 4:1 (their shot = 4 ammo =
  4 Ti at the core's 1:1 conversion for 7 dmg = 0.571 Ti/HP, against our
  0.25 Ti/HP), i.e. **about half the priced rate.**
* A 7-dmg burst clears `MIN_DMG = 4` in **one shot**, where a 2-dmg peck needs
  **two** — the fixture is *more* generous to dose delivery than the field on
  that axis and *less* generous on the economics.
* ⇒ **This screen tests the DISPATCH MACHINERY and HARM under a damage source.
  It does not test the peck economics, and it cannot resolve the row's
  batk-by-target caveat.**

⛔ **DECLARED FIXTURE DEFECT 2 — IT IS OUR OWN PROBE, AND IT LIES IN A KNOWN
DIRECTION.** Per its own docstring it *"rebuilds unconditionally and never
retreats"*. Per CLAUDE.md's standing rule, `bots/*_probe` is a fixture WE
authored; `FIXTURE_OF_RECORD` makes this a **MECHANISM** instrument only. **The
currency read for QUEUE #52 is the pinned live leg named in the row, and this
document does not substitute for it.**

**Opponent version stability (Obligation 14): N/A by construction** — the
fixture is a repo tree with no platform version churn. The builder records
`git rev-parse HEAD:bots/_probe_creeper` at lock so a later re-run is
comparable.

---

## 3. Dose evidence — PASSED BOTH DIRECTIONS, and THIN

**⚠ OBLIGATION 1 LABEL: OBSERVABLE-AT-LOCK.** The dose probe
(`scratchpad/collarmedic_dose_probe/results.tsv`, 48 games, run and **read**
before this document existed) is **not blind evidence**. It sizes and justifies
the design. **It may not serve as any bar's control.** The screen shards and the
instrumented sub-batch (§5) have not started.

Probe design: 2 arms × 4 maps (fjordgate, hive, midgard, drakkarfjord) × 3
seeds × 2 seed-sets (2001-2003, 3001-3003) = **24 games per arm.**

| tag | TREATMENT (24 g) | CONTROL (24 g) |
|---|---|---|
| **CMEDIC** (the treatment) | **9** in **2 games** | **0** in 24 games |
| CHAIN | 20 | 4 |
| CORE | 1,543 | 1,318 |
| **ADJ** (the incumbent's opportunistic path) | **0** | **0** |
| COLLARHOLD | 7 | 6 |
| BUDDY | 0 | 4 |
| exceptions | **0/24** | **0/24** |

**READ HONESTLY, and every one of these bounds the plank:**
1. **DELIVERY IS CONFIRMED IN BOTH DIRECTIONS** — non-zero in treatment, exactly
   zero in control, at plausible repeated-heal rounds. Zero-not-lower signature
   satisfied; **zero exceptions in either arm**, which matters because an
   escaping exception permanently destroys the unit.
2. **⛔ THE DOSE IS THIN. 0.375 events/game; 2 of 24 games non-zero.** The
   eligibility window (a home-band ECO builder AND a home building damaged by
   ≥4 HP AND both inside the radii, simultaneously) is narrow. **A thin dose
   bounds the effect ceiling — it does not merely widen the interval.**
3. **⛔ THE `CHAIN` DIFFERENCE IS ONE GAME.** All 20 treatment CHAIN heals came
   from `drakkarfjord/2003`, the same game that carries 7 of the 9 CMEDIC
   events. It is **not** a distributed effect and must not be reported as one.
4. **THE ROW'S LEAK IS CONFIRMED AT THE EXTREME: `ADJ` = 0 in 48 of 48 games.**
   The incumbent's opportunistic building-repair path **never fired once**. The
   plank raises the non-core building-heal channel from **4 (CHAIN only)** to
   **29 (CMEDIC 9 + CHAIN 20)** — a large multiple **on a tiny base, from two
   games.**
5. **CORE heals (1,543 vs 1,318) are NOT a treatment metric.** They are a
   co-moving quantity at n=24 with similar game lengths (mean end turn 122.0 vs
   124.5). Descriptive only; no claim.
6. **Obligation 8 (denominators):** the 0.375/game figure is over **4 maps**,
   not the 15-map pool. It is not transportable to the pool without
   restatement, and §5's floor is set below it for exactly that reason.

---

## 4. ⛔ WHAT THIS SCREEN CAN AND CANNOT RESOLVE — read this before the bars

**THE WIN-SHARE CHANNEL AGAINST THIS FIXTURE IS AT THE CEILING.** In the
observable-at-lock probe: **TREATMENT 24/24 = 100.0%**, **CONTROL 23/24 =
95.8%**. Forty-seven of forty-eight games won.

**OBLIGATION 7 BITES HERE, AND IT BITES THE OBVIOUS BAR.** Ob-7 requires a
prereg to verify **its predicted-change set is not already in the target
state.** A prediction that "the medic raises win share" is aimed at a variable
with **at most ~4.2pp of headroom** and an arm already observed at 100%. **Such
a prediction cannot fail honestly. IT IS THEREFORE NOT REGISTERED.**

What follows from the operating point, arithmetically (n = 2,700/arm, DEFF 1.00
— see §6):

| quantity | at p ≈ 0.96 (this fixture) | at p = 0.50 (the handed default) |
|---|---|---|
| half-width, one arm's share | **±0.75pp** | ±1.88pp |
| half-width, arm **difference** | **±1.06pp** | ±2.66pp |

⇒ **The handed ±1.88pp is the p=0.5 form and does not describe this fixture.**
Near the ceiling the binomial variance collapses, so a **DOWNWARD** (harm)
difference is measured *finely* while the **UPWARD** direction is capped by the
ceiling itself. That asymmetry is what makes harm-exclusion the honest primary.

**CAN resolve:** (a) that the plank does not **cost** us games against a
damage-dealing opponent, to ±1.06pp; (b) that it does not **slow the kill**, to
±2.9 rounds; (c) that the mechanism **delivers at pool scale** and remains
exception-free across 15 maps rather than 4.

**CANNOT resolve:** (a) **any currency claim** — the fixture is our own probe,
at a saturated operating point, with no peck shape; (b) the **magnitude** of the
plank's value on the live surface; (c) **dose scaling against opponent peck
volume**, because this design has exactly one opponent and that opponent does
not peck (§7 records the substitution).

---

## 5. Design

### 5.1 Shards (local corefill, `tools/overnight_pool26.sh`)

```
CMEDICON    bots/_v232collarmedic      bots/_probe_creeper   2700 312000
CMEDICOFF   bots/_v232collarmedic_off  bots/_probe_creeper   2700 312000
```

* **n = 2,700 games PER ARM (5,400 games total).** Sized as a **mechanism-probe
  screen, not a 5,400-per-arm currency screen** — the thin dose (§3.2) does not
  justify the larger spend. *(Ratification line R1 — see §9.)*
* **Same `seed_lo` (312000) in both shards** so the two arms run **identical
  (map, seed, seat) cells** and the contrast is **blocked**, not merely pooled.
  Precedent: `NESTSHOT`/`NESTSHOT2`, both seed 276000.
  ⚠ **This is BLOCKING, not deterministic pairing** — engine noise is left on
  (`NOISE_ON` is deliberately TRUE in the runner) and the arms' own trajectories
  diverge from round 1 regardless. Matched cells reduce map/seat variance; they
  do not make the two games comparable game-for-game.
* **Map pool: the full 15-map post-patch pool26 set** — antler, archipelago,
  auroraveil, drakkarfjord, drumlin, fjordgate, frostgate, glacierkeep, icefloe,
  midgard, nordkap, ragnarok, royale, valkyrie, yulerune
  (`tools/overnight_pool26.sh:109`). **Eleven of these fifteen are unseen by the
  dose probe.**
* **Seat-balanced by construction** (both seats every seed × map). Seat is worth
  ~7.6pp on byte-identical arms, so this is load-bearing, not hygiene.
* **`--tle 10`** enforced by the runner (a run without it measures a chassis
  that does not exist).
* **Name-collision check run at drafting time**, per the `L4REPAIR` incident:
  `CMEDICON` and `CMEDICOFF` appear **nowhere** in `scratchpad/corefill_started/`
  (130 existing markers checked, 0 matches on `CMEDIC`) and **neither is a
  prefix of the other**
  (deliberate — `CMEDIC`/`CMEDIC0` would be). Seeds 312000 and 314000 appear
  nowhere in `scratchpad/corefill_work.txt` (highest existing: 306000).
* ⚠ **BASENAME NOTE:** `_v232collarmedic` **is a substring of**
  `_v232collarmedic_off`. Each shard's own pair passes corefill's guard
  (`overnight_pool26.sh:120`) because the opponent is `_probe_creeper` in both.
  **But a head-to-head shard of the two arms would be REFUSED as unscorable,
  correctly, and any cross-shard analysis that substring-matches bot names will
  attribute CONTROL rows to TREATMENT.** The per-shard TSVs record `T`/`C`, not
  bot names, so the shard rows themselves are safe. If a head-to-head is ever
  wanted, rename the control tree first.

### 5.2 Instrumented sub-batch — REQUIRED, because the shards cannot see the mechanism

⛔ **THE COREFILL ROWS CANNOT CARRY THE DOSE METRIC AND THIS MUST NOT BE
DISCOVERED AT READ-OUT.** `overnight_pool26.sh:152-153` runs with
**`--replay /dev/null`**, and the row schema is
`ts shard game map seed seat winner cond turns`. `heal_log` writes to
**stdout**, captured only into a **local replay file**. ⇒ **CMEDIC events are
unreadable in `CMEDICON`/`CMEDICOFF`.** (This is the same class as LOKI-18's
inert bar: a metric downstream of a path the fixture does not record.)

**Therefore the mechanism bar is carried by a separate batch:**

```
CMEDICDOSE   both arms, 15-map pool26 set, 2 seats x 4 seeds = 120 games/arm
             seed base 314000, replays KEPT, heal_log decoded per game
             (extend scratchpad/collarmedic_dose_probe/run_probe.sh to pool26)
```
Disk: ~50 KB/replay × 240 ≈ 12 MB. *(Ratification line R2 — see §9.)*

---

## 6. Design effect — the enumeration, performed in writing

Per CLAUDE.md's scope **procedure** (not a taxonomy):

1. **Clusters this data has.**
   * **MATCH** — **does not exist locally.** One TSV row = one `fcode run`
     (`overnight_pool26.sh:152`); there are no 5-game matches on this surface.
     The cluster is absent, not merely emptied.
   * **OPPONENT** — exactly **one** (`_probe_creeper`), constant across every
     row and **identical in both arms**. A single-member opponent population
     contributes no between-cluster variance **to the arm contrast**; what it
     does limit is **external validity**, and that is handled by §4's
     "CANNOT resolve" clause, not by an interval.
   * MAP / SEED / SEAT are **design strata, balanced by construction** — not
     clusters.
2. **Surviving clusters: NONE. `CLUSTER UNIT: none`.**
3. **DEFF APPLIED TO EVERY BAR: 1.00 (naive).**
   ⛔ **The measured local value is 0.98** (s39 audit, 124 shards, ρ = −0.020,
   pair-weighted) **and it is deliberately NOT applied.** Every bar in this
   document is an **EXCLUSION** claim, and a DEFF below 1 **narrows** the
   interval — i.e. it would make exclusion **easier**, which is the flattering
   direction. Recorded and declined. The difference is ~1% of each half-width
   and changes no verdict.
   ⚠ Platform constants (1.529 rated / 1.833 unrated) **must not** be carried
   onto this surface; local is measured, not assumed.

---

## 7. BARS — each with its pre-committed resolution statement (Obligation 12)

**⛔ EVERY BAR BELOW IS WRITTEN AS AN EXCLUSION.** Per CLAUDE.md's direction
clause, a fail-to-exclude phrasing ("no significant harm", "consistent with
zero") is laundered by any interval correction and is banned in this document.

### P1 — HARM EXCLUSION on game share vs the fixture  *(PRIMARY)*
**Bar:** the 95% CI on **Δshare = share(CMEDICON) − share(CMEDICOFF)**, pooled
over all matched cells, **EXCLUDES a loss of 1.5pp** (i.e. lower bound > −1.5pp).
**Resolution:** at the probe's operating point (control ≈95.8%) the half-width
is **±1.06pp < 1.5pp ⇒ RESOLVABLE.**
**Pre-committed failure of resolution:** if the observed control share lands
below **90%** or above **99.5%**, the half-width or the headroom changes enough
that this bar is declared **UNRESOLVED**, and **per Obligation 12 an unresolved
gate defaults to the RESTRICTION — harm is NOT excluded**, and no permission
is granted.
**No upward claim is registered on this metric** (§4, Obligation 7).

### P2 — KILL-ROUND NON-REGRESSION  *(PRIMARY; `DEFENCE_ADMISSION_BAR`)*
The plank is a defensive plank, so `DEFENCE_ADMISSION_BAR:
kill_round_non_regression` binds. Restated as an exclusion, as required:
**Bar:** the 95% CI on **Δmean end-turn (CMEDICON − CMEDICOFF)** over
**decided** games **EXCLUDES a rise of +5 rounds** (upper bound < +5).
**Resolution:** dose-probe sd ≈ 55 rounds ⇒ SE_diff = 55·√(2/2700) ≈ **1.50
rounds** ⇒ half-width **±2.9 rounds < 5 ⇒ RESOLVABLE.** Re-estimated from the
shards' own rows at read-out; if the realised sd exceeds **91 rounds** the bar
becomes unresolved and defaults to the restriction.
**Reported alongside, not as bars:** median end-turn per arm; the **count of
r1000 games per arm** (an r1000 game is a defeat, and truncation biases the
mean — the r1000 share **must not rise**); `NOWINNER` counts.

### M1 — MECHANISM DELIVERY AT POOL SCALE  *(required; read from `CMEDICDOSE`)*
**Bar, both halves required:**
* **treatment:** ≥ **0.20 CMEDIC events/game** AND ≥ **5% of games non-zero**;
* **control:** **EXACTLY 0** CMEDIC events (zero-not-lower signature);
* **both arms: 0 uncaught exceptions** across all 240 games.
**Resolution:** at the probe's 0.375/game, 120 games/arm expect ≈45 events
(Poisson sd ≈ 6.7); the floor of 0.20/game = 24 events sits ≈3σ below that ⇒
**RESOLVABLE against the floor and against zero.** It **cannot** resolve fine
dose gradations (e.g. 0.35 vs 0.45/game) and no such claim is licensed.
**Pre-committed failure branch:** if treatment falls **below** the floor, the
plank is declared **UNDER-DOSED AT POOL SCALE**, and P1/P2 are then read as
**bounding a mechanism that barely ran** — explicitly **not** as a refutation of
the exchange. That branch is written here so it is not chosen at read-out.

### M2 — CHANNEL COMPOSITION  *(DESCRIPTIVE — not a bar, no verdict rides on it)*
Per-arm counts of CMEDIC / CHAIN / CORE / ADJ / BUDDY / COLLARHOLD, plus the
**per-game distribution** of CMEDIC (so a repeat of §3.3's one-game artefact is
visible immediately rather than pooled away).

### ANTI-GOODHART CLAUSE
* **Mechanism up + outcome flat = NULL, banked as a null.** Specifically: M1
  passes, Δshare inside ±1.06pp and Δkill-round inside ±2.9 rounds ⇒
  **"delivered but inert at this dose against this fixture"**. That is the
  expected result at 0.375 events/game and it is an iteration, not a failure.
* **Outcome moves without delivered heals ⇒ OFF-PREDICTION.** A share or
  kill-round difference with M1 failing may **not** be attributed to the plank.
* **Obligation 10 (identity):** no claim that heals *prevented building deaths*
  is licensed by any of these bars — the corefill rows carry no entity ledger,
  so the two sides of that ledger cannot be shown to be the **same entities**.
  If such a claim is ever wanted, it needs a per-entity decode, not this screen.

### SUBSTITUTION RECORDED (the handed primary, and why it changed)
The handed suggestion was *"primary = dose scales with opponent peck volume +
harm-exclusion on share"*. **The first half is not satisfiable by this design:
there is exactly one opponent and it does not peck** (§2, defect 1) — there is
no peck-volume axis to scale against. It is replaced by **M1 (delivery at pool
scale)**, which is the largest testable part of the same question here. **The
peck-volume scaling test requires either a peck-capable fixture (none exists in
`bots/_probe_*` — checked: only `_probe_creeper`, `_probe_sent`, `_probe_conv`,
`_probe_meleebot` and forks of our own tree call `ct.fire`, and only
`_probe_meleebot` melees at all) or the pinned live leg.** Recorded as an
adjacent queue item, not smuggled into this leg.

---

## 8. MAP DEPENDENCE  *(Obligation 15)*

**MAP SEGMENT: lock-heavy maps — {midgard, ragnarok, valkyrie} — EXPECTED
DIRECTION: NEGATIVE.**

**Mechanism reason (15a requires one, and a mechanism-specific segment beats a
size class whenever the mechanism names a terrain property):** the plank's only
new cost is a **WALK** — dispatch to a seat beside the patient, then STAY. QUEUE
#54's nav oscillation defect concentrates exactly on these maps (**midgard
35.6% of builder-rounds locked, ragnarok 14.1%, valkyrie 12.8%**, against 3-8%
on small maps). A builder that oscillates spends its turn without arriving, so
it pays the plank's cost and collects none of its benefit. **The doctrine block
says as much in its own comment — every radius was kept inside builder vision
"because the nav has a known oscillation defect, so a long dispatch is a builder
that never arrives."**

**Predicted sign, which is what makes this a test:** Δshare and Δkill-round on
the lock-heavy segment are **WORSE than on the other twelve maps** (a smaller
share difference, a larger kill-round rise). If the segment comes out **better**,
the walk-cost story is **wrong** and must be reported as such.

**15b — EXACTLY ONE PRIMARY SEGMENT.** The above. **Size class (small / mid /
900-area) is DESCRIPTIVE ONLY** and may not rescue a failed pooled read.

**Segment resolution, declared in advance (Obligation 12 applied to 15c):** 3 of
15 maps ⇒ n ≈ 540/arm ⇒ half-widths **±2.4pp on share** and **±6.6 rounds on
kill round** — **both WIDER than the P1/P2 bars they would be compared against.**
⇒ **The segment read is DESCRIPTIVE at this n and cannot on its own license a
conditional ship.** Per 15c, a pooled fail that *looks* rescued by this segment
requires a **NEW leg with its own n** — the rows that suggest a segment may not
also confirm it.

**Units rider:** a per-segment bar takes **no** match design effect (the match
cluster does not exist on this surface at all, §6) and the opponent cluster is
single-membered. **DEFF stays 1.00 on segment bars; the platform's 1.53 must not
be carried in.**

---

## 9. Obligations ledger

| Ob | requirement | status in this document |
|---|---|---|
| **1** | observable-at-lock labelling | **SATISFIED** — the 48-game dose probe is labelled OBSERVABLE-AT-LOCK (§3) and barred from serving as a control |
| **3** | half-leg sizing carries its numbers | **SATISFIED** — §3 and §4 carry every n and denominator inline |
| **7** | MIX vs IN-OUR-FAVOUR; predicted-change set not already in target state | **SATISFIED, AND IT CHANGED THE DESIGN** — share is already 95.8/100.0, so the upward share claim is **not registered** (§4) |
| **8** | denominators / no pooling of unlike cells | **SATISFIED** — probe = 4 maps, screen = 15 maps, stated as non-transportable (§3.6) |
| **10** | closure needs identity of the ledger's two sides | **SATISFIED BY EXCLUSION** — no prevention claim licensed (§7) |
| **11** | treatment check in the EXPERIMENT's causal variable | **SATISFIED** — see below |
| **12** | every gate carries its resolution statement + failure default | **SATISFIED** — P1, P2, M1 and the segment each carry one; all default to the RESTRICTION |
| **13** | metric `file:line` ∩ treatment diff | **SATISFIED — YES** — see below |
| **14** | opponent version stability per cell | **N/A, stated** — local fixture, no platform version churn (§2) |
| **15** | map dependence declared with expected direction | **SATISFIED** — §8, one primary segment, sign predicted |

### Obligation 13 — named exactly, both halves

```
MECHANISM METRIC READS: bots/_v232collarmedic/eco.py:479
                        (heal_log(ct, "CMEDIC")), emitted by
                        doctrine.py:1785-1790, gated by
                        LOKI_CMEDIC_LOG (doctrine.py:1762) and
                        LOKI_HEALLOG_ON (doctrine.py:1782).
TREATMENT DIFF TOUCHES: doctrine.py:1721 (one line; diff -r verified).
INTERSECTION:           YES.
```
**The path, named rather than asserted:** `doctrine.py:1721` defines
`LOKI_COLLAR_MEDIC_ON`; `eco.py:31` does `from doctrine import *`; `eco.py:364`
(`_collar_eligible`) returns `False` immediately when the flag is off;
`_collar_medic_heal` (`eco.py:446`) gates on `_collar_eligible` at `eco.py:448`
and reaches the heal and the log at `eco.py:472-479`; `_collar_patient`
(`eco.py:410`) gates on it identically. **The one line the diff changes is the
gate on the exact code path the metric reads** — which is what a healthy answer
to this obligation looks like.
⛔ **AND THE INSTRUMENT LIMIT IS NAMED IN THE SAME BREATH:** that path is
readable **only where replays are kept**, which the corefill shards do not do —
hence §5.2. **A bar that read CMEDIC out of `CMEDICON`'s TSV would be INERT.**

### Obligation 11 — the invariant the hypothesis needs, not the one the code states
The check is **not** "the flag is `False` in the control tree". It is:
**"in the control arm, no builder walks to and heals a damaged home building."**
Verified by decode on the observable-at-lock probe: **CMEDIC = 0 in 24/24
control games**, and **ADJ = 0 in 24/24 in BOTH arms**.
⚠ **The control is CMEDIC-free, NOT heal-free** — CORE (1,318), CHAIN (4),
COLLARHOLD (6) and BUDDY (4) all fire in the control arm. **That is the correct
invariant**: the plank adds a dispatch channel, it does not add healing as such,
and a check that demanded a heal-free control would be a clean check of the
wrong quantity.

---

## 10. Futility gates

`RULE-futility-gates-2026-08-13` binds all shards from their first row, **and
its thresholds are calibrated for a ~50% fixture. Against `_probe_creeper` at
~96% they are degenerate** (a share below 48% would mean total collapse, not
futility). Declared substitution, committed before any row is read:

* **GATE-1000 → FIXTURE-SANITY GATE (n ≥ 1000, read once per shard).** Drop
  **both** shards, label **`FIXTURE-SATURATED`**, if either arm's share is
  **< 90%** or **> 99.5%**, or `NOWINNER` **> 1%**. Rationale: outside that band
  the arms cannot be told apart on this fixture at any n, so more cores buy
  nothing. *(A `NOWINNER` rate > 1% already aborts inside the runner; this gate
  is the human-side twin.)*
* **GATE-2700 is the TERMINAL read, not a futility point** — n = 2,700/arm is
  the whole design; there is no 5,400 continuation to protect.
* **Rows are always KEPT.** A gate drop is an allocation decision, never a
  refutation.
* **Wake path:** the builder is woken at the gate crossing by the session
  watcher; **the watcher never decides — the builder types the gate decision.**

---

## 11. Era and target-value lines

**POOL ERA.** All rows produced by this screen are post-**2026-08-13T07:12:59Z**
by construction (neither shard has started). **Any base rate, comparator share
or segment share quoted at read-out is cut on the NEW-POOL era only** —
all-time cuts misprice by up to **9.1×**, and an all-time comparator would be
the single easiest way to launder this screen's result.

**TARGET BAND: N/A — local screen, zero live exposure, no submission, no
activation, no rated matches at risk.** The payout gate does not apply to a
local fixture. **The currency claim this row eventually wants is the pinned
live leg, and `tools/target_value.py` must be run BEFORE that prereg is
written** — not inherited from this one.

---

## 12. Not licensed by this document

* **No ship implication.** No combo claim, no `MAP_CODES`-style conditional
  ship, no promotion of `_v232collarmedic` to a ship candidate.
* **No currency claim.** §4 says why, and the row itself says the value read is
  the pinned live leg.
* **No barrier-specific claim.** The `batk`-by-target caveat is unresolved
  (§0), and this fixture damages via gunner fire, so nothing here speaks to
  which of our buildings the field actually pecks.
* **No 8:1 arithmetic** anywhere downstream. **⚠ AND THE SOURCE COMMENT AT
  `bots/_v232collarmedic/eco.py:325-343` ("eight to one") IS STILL WRONG AND IS
  THE BUILDER'S TO FIX** — it is the origin that re-seeds the error into the
  next row that greps for it. That fix is **not** part of the treatment diff and
  must not be made to these two trees while the shards are live (it would break
  the one-line-diff property); queue it against the next chassis.
* **No claim about `CORE`, `CHAIN`, `COLLARHOLD` or `BUDDY` heal counts.**
  Descriptive channels only.
* **No transport of the 0.375 events/game figure** to any population other than
  the 4-map probe it was measured on.

---

## 13. Ratification lines — the builder types these, this agent does not

**R1. n = 2,700 PER ARM (5,400 games total), or 2,700 total (1,350/arm)?** The
handed brief said "n=2700"; this draft reads it as **per arm**, which is what
makes §7's resolution statements true. **At 1,350/arm the half-widths become
±1.50pp (share) and ±4.2 rounds (kill), and P2's +5-round bar becomes
marginal** — it would still resolve, but barely.

**R2. Approve the `CMEDICDOSE` instrumented sub-batch (§5.2), 120 games/arm,
seed base 314000, replays kept.** **Without it there is NO mechanism bar at all**
— the corefill rows physically cannot carry CMEDIC counts, and the only
delivery evidence would be the 48-game probe, which Obligation 1 bars from
serving as a bar's control. Declining R2 means M1 is struck and the screen
becomes harm-and-kill-round only; that is a coherent choice but it must be typed,
not defaulted into.

**R3. Accept the primary-bar substitution (§7):** "dose scales with opponent
peck volume" → **M1 delivery at pool scale**, because the fixture has one
opponent and it does not peck.

**R4. Accept DEFF = 1.00 rather than the handed 0.98**, on the ground that
every bar here is an exclusion and 0.98 narrows in the flattering direction.
(Immaterial numerically; it is a discipline call.)

**R5. Accept the harm bar at −1.5pp and the kill-round bar at +5 rounds.** Both
are resolvable at R1-as-per-arm; both are choices, not derivations.

**R6. Accept the futility-gate substitution (§10)** — the standing GATE-1000 is
degenerate on a 96% fixture.

**R7. Confirm the shard names `CMEDICON` / `CMEDICOFF` and seed bases
312000 / 314000**, and record `git rev-parse HEAD` for
`bots/_v232collarmedic`, `bots/_v232collarmedic_off` and `bots/_probe_creeper`
in the ratifying commit message, so a later re-run is comparable.

## RATIFICATION + SCOPE (builder, 2026-08-14T20:28:05Z)

**Ratified:** R2 (approve CMEDICDOSE) · R3 (M1 delivery substitution; peck-scaling
struck — fixture doesn't peck) · R4 (**DEFF 1.00**, not 0.98 — every bar is an
EXCLUSION and the 0.98 shrink narrows in the flattering direction) · R5 (−1.5pp /
+5-round bar values) · R6 (FIXTURE-SATURATED futility gate) · R7 (shard/seed names).
Arm md5: on=cfa5498d9df754f8a777a430c5e4ff6b off=7f0d9065d90ae56999110cc2b6e9f365.

**⛔ SCOPE DECISION — ONLY THE DELIVERY/SAFETY BATCH FIRES LOCALLY.** The draft's
three findings establish the local fixture is structurally blind to #52's value:
_probe_creeper SHOOTS not pecks (wrong shape, exchange ~2.3:1 not the row's 4:1),
and our win-share is SATURATED ~96-100% so harm-to-win-share is near-unobservable.
⇒ **THIS REGISTRATION IS BANKED, NOT FIRED.** Nothing local runs tonight. The
already-passed dose probe (24+24 games, both verdicts, 0 crashes) established the
mechanism fires and is crash-safe; its one open weakness — delivery fired in 2 of
24 games, 7 of 9 events from ONE game (drakkarfjord/2003) — makes
DELIVERY-AT-SCALE (real-but-rare vs one-map-artifact) the cheap next step
(CMEDICDOSE: 120/arm across the 15-map pool, replays kept, seed 314000) WHEN A
SLOT FREES behind SEALFLOOR6/SALTREF2 — not urgent, #52 is below the seal work.
**The CMEDICON/CMEDICOFF harm-exclusion screen DOES NOT FIRE at all** — a
5400-game read of a saturated ~96-100% win-share is precision without a question.
**#52's value read AND its real harm read are OWNED BY THE LIVE PINNED LEG** per
the row's COUPLING CLASS (peck-capable opponent needed; none exists in
bots/_probe_*). The self-play-blindness rule (builder-retro open item) doing its
job: the finding IS that the local fixture cannot instrument this plank.

## RE-TAG: PREMISE-ABSENT, not FIXTURE-BLOCKED (research, consumed 2026-08-14T20:33:47Z)

**Supersedes the banked-not-fired scope above.** Research's cell-selection cut
(events.tsv BUILD/DEATH, our barriers, our games, ≥80 built / ≥20 games) found
**NO melee-dominant cell exists** — every opponent that actually kills our
barriers fields turrets (lowest 4.51/game), and our barriers die to TURRET FIRE.
The throughput arithmetic is why that is fatal not inconvenient: one builder
heals +4 HP/turn; a sentinel does 9 dmg/turn, a gunner 7 — the exchange RATE
favours us against all three (4.00:1 melee, 2.29:1 gunner, 2.22:1 sentinel) but
we cannot heal fast enough, so a 30-HP barrier under one sentinel dies in ~4
rounds whatever we spend. **#52's premise (the melee heal exchange) is a threat
the in-band field does not present.**
⇒ **TAG: PREMISE-ABSENT. Re-scope or retire, NOT fire-elsewhere.** The only
re-scope visible is heal-dispatch against BUILDER-PECK damage specifically, and
no cell with that damage has been found. Honest limit carried: DEATH does not
name its killer (no attack events), so turret COUNT proxies turret DAMAGE — the
load-bearing fact is the ABSENCE of a low-turret/high-death cell, not any row.
