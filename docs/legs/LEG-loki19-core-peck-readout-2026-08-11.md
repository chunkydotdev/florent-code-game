# LOKI-19 READ-OUT — the core peck, 100 games, read against a locked prereg

**Written 2026-08-11 by the s30 BUILDER.** Governing document:
`docs/prereg/PREREG-loki19-core-peck-2026-08-11.md` + Amendments 1, 2, 3, all
committed before the arm each governs existed. **No bar, threshold, estimator,
stratum or band-language in this read-out was chosen after seeing a number.**
Every sentence below that carries a verdict is quoted from the prereg's
pre-committed tables.

**THE LEG.** 100 games / 20 matches, all archived locally and decoded off
`replay_archive/` — **this read-out made no platform write and created no
match.** Control = v104 (`bots/_v130loki13`), treatment = v108
(`bots/_v136loki19`, md5 `fb5cba8c`), 4 interleaved windows, 50 games per arm,
§6's stated minimum.

---

# THE VERDICT, IN THE PRE-COMMITTED LANGUAGE

§6's band table has four rows. The leg lands in row 2, which the prereg named
**"THE EXPECTED OUTCOME"** before any game was played:

> **DOSE DELIVERED, MECHANISM MEASURED, CURRENCY UNRESOLVED AT THIS n.**

**The words "null", "refuted" and "fails" are FORBIDDEN in this band by §6 and
are not used anywhere in this document.** Bar 5d lands in Amendment 3c row 4
(point above control) and licenses **no claim**. Nothing here ships.

**AND THE LEG PRODUCED A SURPRISE THAT NO BAR ASKED FOR — §11 below.** Under the
directive's point 4 (*"a surprise is the point, not an anomaly — write it down
before explaining it away"*) it is reported before it is interpreted.

---

# 1. BAR 5a — DOSE. GO. The gate fires, and it fires cleanly.

Instrument: `tools/peck_read.py` (**new this session**; selftest 21 assertions
over 6 forced-answer protobuf cells, independently mutation-tested by me — see
§9). Statistic: builder attacks on the ENEMY CORE 2x2 footprint, per game, ours.

| | treatment (v108) | control (v104) |
|---|---:|---:|
| core-pecks / game, mean | **192.90** | **0.00** |
| games with >= 1 peck | **44/50 = 88.0%** | **0/50 = 0.0%** |
| median / p90 / max | 98 / 641 / 1033 | 0 / 0 / 0 |

**§5a's bar was "treatment > 0 and control ~= 0". The control is not
approximately zero, it is EXACTLY zero across all 50 games.** The leg is not
VOID; every other bar may be read.

**⭐ AND ONE NUMBER HERE VERIFIES A CLAIM §4 COULD ONLY ASSERT.** In the
treatment arm `our_core_atk == our_total_atk` to the unit in **every cell**
(192.90 == 192.90 pooled; Askar 291.60/291.60, Landers 442.20/442.20, Lunds
54.70/54.70, SmartFridge 85.40/85.40, farming 90.60/90.60). **Every builder
attack we made went at the enemy core footprint and nowhere else.** §4 claimed
gate completeness by *exhaustive enumeration of the four `fire()` call sites*;
this is that claim **confirmed live on the wire**, not re-asserted. Counterbattery
and siphon melee stayed silenced, as designed.

**And the control arm reproduces §1's headline IN-ARM, which §2 required.**
v104's total builder attacks of ANY kind, any target: **0.00 per game across all
50 control games.** §1's "0 builder attacks across 2,247 self-inserts" was a
stored figure from another population; this is the same fact measured inside the
leg, and **§2 forbade the stored one from entering any bar.** It did not need to.

---

# 2. BAR 5a-bis — THE ARRIVAL GATE. IT DOES NOT RESOLVE, AND THE LEG TAKES THE RESTRICTION.

Measured by the RESEARCH ARM on the control arm only, per cell, never pooled
(`docs/research/GATE-5abis-loki19-arrival-2026-08-11.md`). Our `kind=INSERT`
reach, this leg's own games:

| cell | reached / inserts | rate | 95% Wilson |
|---|---:|---:|---:|
| farming_200s | 2/2 | 100% | 34.24–100% |
| Askar City | 3/4 | 75.0% | 30.06–95.44% |
| Lunds Stallions | 4/6 | 66.7% | 30.00–90.32% |
| Landers | 2/7 | 28.6% | 8.22–64.11% |
| **Powered by SmartFridge** | **0/0** | **—** | **NOT MEASURABLE** |

**⛔ THE GATE UNDER-RESOLVES ITS OWN BANDS AND THAT IS THE FINDING, NOT THE
RATES.** Amendment 1b's bands are 10pp apart; the whole control arm yields
**19 events over 50 games**, and at n=4 a single throw is 25pp. Landers' interval
spans all three bands, Lunds spans two, and **Askar's lower bound is 30.06% —
inside a rounding error of the edge it would be clearing.**

**⇒ MY CALL, AND IT IS THE RESTRICTIVE ONE: the gate does not resolve, so the
leg does NOT claim to have tested "the changed premise."** Amendment 1b makes
the gate the thing that decides what may be claimed; an unresolved gate defaults
to the restriction, never to the permission. Three of four measurable cells sit
above 30% on the point estimate and I am **not** banking that — the intervals do
not separate it from Amendment 2d's forecast of the AMBIGUOUS band. **Saying 2d
was wrong would be the same error as saying the gate was cleared**, and the
research arm applied that standard against its own forecast first.

**§6 pre-declared 5c unresolvable at this n and ran that audit for every bar
except the gate itself.** That omission is this leg's clearest process finding
and it is routed in §12.

---

# 3. BAR 5b — MECHANISM. Measured, and the pre-registered estimator turns out to measure something narrower than its own name.

§5b: *"Enemy-core HP removed by builder melee, per game (2 dmg/swing)"*, no
threshold, *"the honest prior is that it is small."*

**As pre-registered (swings x 2):** treatment **385.80 HP/game** (median 196,
max 2066), control **0.00**. The opponent column is alive and non-constant
(treatment 5.36, control 0.12), so the decoder can read the other team's melee
and is not returning a structural zero.

**⛔ THE ESTIMATOR IS NOT WHAT ITS NAME SAYS, AND I FOUND THAT BY CHECKING IT
RATHER THAN BY QUOTING IT.** 385.80 against a **500 HP** core reads as "we
removed 77% of a core per game", and **in 10 of 50 games swings x 2 exceeds a
full 500 HP core outright (max 2066).** A 500 HP core cannot lose 2,066 HP. So
`swings x 2` is **gross melee damage DEALT**, not **HP removed** — the two
differ by exactly the healing the opponent buys, and §5b's wording invites the
second reading. **The defect is in my own prereg's phrasing, not in the decode.**

**So I walked the actual core HP ledger** (cores seeded at 500 — they are never
placed by an update — then every `UpdateHp{id,delta}` on the enemy core id,
split by sign; `scratchpad/hp_ledger.py`). **Validation that the walk is real:
its independently-derived "enemy core destroyed" count is 18/50 treatment and
24/50 control, reproducing `leg_read.py`'s `core_kill_share` of 36.0% and 48.0%
EXACTLY, by a completely different path** (replay `removeEntity` vs the
platform's `winnerId`).

| per game, mean | treatment | control | delta |
|---|---:|---:|---:|
| melee estimator (swings x 2) | 385.8 | 0.0 | +385.8 |
| **enemy-core damage, ALL our sources** | **831.7** | **489.0** | **+342.7** |
| **enemy healing ON their core** | **594.0** | **223.9** | **+370.1** |
| **net (damage − healing)** | **237.7** | **265.1** | **−27.4** |

**Damage and healing are unattributable to a source on the wire** — our turrets
and our melee land on the same core and the format records no attacker for
`UpdateHp`. What can be said: the damage increase (+342.7) is **consistent in
magnitude with the melee estimator (385.8)**, i.e. ~89% of it, which is what you
would expect if the melee is the whole difference. That is consistency, not
attribution, and it is written as such.

---

# 4. BAR 5c — CURRENCY. UNRESOLVED AT THIS n, exactly as §6 pre-declared.

`tools/leg_read.py`, which joins on `winnerId == OUR_TEAM_ID` per game and never
touches `scoreA`/`scoreB`.

| | treatment | control | delta |
|---|---:|---:|---:|
| **core_kill_share** (ours / ALL games) | 18/50 = **36.0%** | 24/50 = **48.0%** | **−12.0pp** |
| r1000 rate (a DEFEAT under `R1000_IS_DEFEAT`) | 4.0% | 6.0% | −2.0pp |
| our median kill turn | 196 | 232 | −36 |
| our kills inside `KILL_WINDOW_RND` 250 | 11/18 | 13/24 | — |
| kill-speed score [scale v2] | −4.88 | −3.28 | — |
| win rate (**NOT A VERDICT**, `PROGRAMME.md`) | 38.0% | 48.0% | — |

**MDE at this n is 28.0pp (all cells, 80% power, a=0.05). The observed −12.0pp
sits well inside it.** §6's table says 5c **resolves: NO** at 50 games/arm, and
it does not. This is band 2 of the four-band table and the forbidden words are
not used.

`kill_speed_score` is the PRIMARY currency but `KILL_SPEED_IS_LEG_VERDICT: no`
and `KILL_SPEED_MIN_N: 200`; at n=50 it is quoted as a scorecard line only.

---

# 5. BAR 5d — THE FALSIFIER. Amendment 3c row 4: point ABOVE control, NO CLAIM.

Instrument: `tools/loki19_5d.py` (**new this session**, 10 forced-answer cells,
two independent mutations both driven to FAIL — §9). Statistic `hold_pinned`
= longest same-bot-same-tile ring hold / game length, game-mean, **12-ring
stratum**, match-clustered bootstrap, 4,000 draws, seed fixed in the file.

**The stratum is pre-registered and is NOT all games.** §5d says 12-ring and §7
says the leg *"may not pool `jackpot` into the retention stratum"* — jackpot
anchors both cores in a corner so its ring is 5 tiles and a hold FRACTION on it
is a different quantity. **My first run pooled all 100 games; that was wrong and
the tool now filters and prints the exclusion every run** (treatment 50→46,
control 50→49, all exclusions ring_size 5).

| | treatment | control | delta |
|---|---:|---:|---:|
| pooled `hold_pinned` | **0.6665** | **0.6376** | **+0.0289** |
| 95% CI on the difference | | | **[−0.1381, +0.1816]** |

Amendment 3b needs **BOTH** conditions: point >= 25% below control (i.e.
<= 0.4782) **AND** CI upper bound < 0. **Neither holds — the point is above
control.** → **Amendment 3c row 4: "reported as observed. No claim."**

**Per cell, and the heterogeneity is larger than the pooled number by an order of
magnitude:**

| cell | treat | ctrl | delta | % of ctrl |
|---|---:|---:|---:|---:|
| Lunds Stallions | 0.339 | 0.594 | **−0.256** | 57% |
| Landers | 0.687 | 0.857 | −0.170 | 80% |
| Askar City | 0.804 | 0.797 | +0.006 | 101% |
| farming_200s | 0.746 | 0.640 | +0.106 | 117% |
| Powered by SmartFridge | 0.748 | 0.424 | **+0.324** | 177% |

**Two cells clear Amendment 3b's 25% magnitude on the point estimate (Lunds 57%
of control, and Landers at 80% does not). Neither carries an interval at ~2
clusters, and §6 already said 5d only PARTIALLY resolves at ~10 clusters per
arm — per cell it does not resolve at all.** The pooled CI is ±0.16 on a
quantity whose cell-level spread is 0.58. **No cell-level claim is made and the
25% threshold is not applied per cell — it was fixed for the pooled comparison
and applying it somewhere else would be exactly the revision Amendment 3d
forbids.**

---

# 6. ⛔ ONE UNPRICED CONFOUND, WITH ONE NAME: **THE ARMS ARE NOT BALANCED ON THE FIXTURE AXES**

*(Written as one defect on the side lane's audit. I first disclosed the seat mix
and the map mix as two separate facts and the stratum exclusion as a third
footnote. **They are one thing: the arms differ in their fixture composition, and
that single imbalance drives all three symptoms.** A future pooled reading of
this leg will inherit one named confound and is likelier to carry it than three
scattered ones — D52b applied inside a document instead of across documents.)*

**SYMPTOM 1 — the seat mix differs in all five cells.**

`leg_read.py`'s own docstring: *"A paired comparison whose seat mix differs from
its control is NOT paired."* **The prereg has no seat clause at all.**

| cell | treatment seats | control seats |
|---|---|---|
| Askar City | 10×B | 5×A 5×B |
| Landers | 5×A 5×B | 5×B |
| Lunds Stallions | 5×A 5×B | 10×B |
| **Powered by SmartFridge** | **10×B** | **10×A** — a COMPLETE INVERSION |
| farming_200s | 5×A 5×B | 10×A 5×B |

**SYMPTOM 2 — the map mix differs** (treatment 14 maps, control 15): `hive` 0 vs
3, `jackpot` 4 vs 1, `eider` 1 vs 4, `lighthouse` 6 vs 2, `drumlin` 4 vs 2.
Research has separately established that **the map × opponent interaction cancels
in every pooled statistic we compute** while hiding a ±0.3 within-map spread.

**SYMPTOM 3 — §5's stratum exclusion is asymmetric, 4 treatment vs 1 control, AND
THAT ASYMMETRY *IS* SYMPTOM 2.** `jackpot` is the ring-clipped map, and the arms
carry it 4 vs 1. The exclusion is mechanical and pre-specified, so it is not
outcome-selected — but it is not independent evidence either, and reporting it
as a separate caveat would have double-counted one imbalance as two.

**ALL THREE ARE DISCLOSED, NOT CORRECTED.** A seat-matched or map-matched
estimator would be chosen after seeing the data, which is the fault this line
exists to catch. The imbalance pushes in an unknown direction and is not priced.
**Any future pooled reading of this leg inherits it.**

---

# 7. D18 — OPPONENT VERSIONS. Three cells PINNED, one pinned THINLY.

Read off `league_matches.tsv` directly by the side lane, **not** via
`oppver_window` (which returns CLEAN off a stale tape — that lane's own open
finding, and using it here would have been a verification sharing its subject's
failure mode). **Tape newest row 05:52:59Z; leg window 04:35–05:31Z — the tape
reaches 22 minutes past the window's end, so the answer is answerable and is not
UNKNOWN.**

* **Askar City v94, Lunds Stallions v64, farming_200s v13 — PINNED**, single
  version across the whole day, no boundary within 6h of the window.
* **Powered by SmartFridge — pinned THINLY, and the qualifier is load-bearing.**
  One team id, no name collision, but **four distinct versions in the 4.5h before
  the window and two in the 29 minutes after.** In-window rows carry v57 **on
  n=2 rows**. *"Their version was held constant"* is an inference from thin
  evidence, not an observation.

**Independently corroborated inside my own decode**, which reads opponent version
per match off `meta.json`: it agrees exactly, and adds a fact the tape cut could
not show — **SmartFridge's v57 and v67 are BALANCED ACROSS ARMS, 5 games each in
both.** Nothing in the prereg controlled that; it is luck, but it is checkable
luck and it checks out.

---

# 8. ⭐ THREE UNRELATED DEFECTS LAND ON ONE OF FIVE CELLS

**Powered by SmartFridge is simultaneously:**
1. the cell that **fails the mechanism's precondition** — 7.6% archived arrival
   on n=512 against the 18.6% that made silencing the melee correct, and **0/0
   measurable inserts in this leg's control arm**;
2. the **only opponent-version-churn cell** (§7);
3. a **complete seat inversion** (§6).

It is also the cell with the **largest 5d delta in the plank's favour (+0.324)**.
**A cell carrying three independent defects should not be the one supplying the
most favourable number, and it is.** No weight is placed on it anywhere in this
read-out.

**AND A CORRECTION TO THE FIGURE THAT DEMOTED IT, from research, which cuts
against the demotion:** Amendment 2a's arrival table pools over opponent
versions. **SmartFridge's 7.6% is 60% carried by their v30 alone — 311 of 516
inserts at 4.5% — a version they no longer run.** The leg faced v57 and v67,
which contribute **5 inserts and 0 reaches**. Version-pinned, the other cells
move mostly upward (Lunds 23.6→30.0%, Askar 30.8→42.9%, Landers 63.9→71.7%,
farming 60.0→53.8%). **§2 forbids stored figures entering bars, so none of this
touches the gate — it bears on CELL SELECTION, which is where 2a used it.**

---

# 9. THE INSTRUMENTS, AND EACH WAS DRIVEN TO THE OTHER VERDICT BEFORE ITS NUMBER WAS USED

| tool | selftest | mutation driven to FAIL |
|---|---|---|
| `tools/peck_read.py` (5a, 5b) | `PECK_READ_SELFTEST: PASS`, 21 assertions / 6 forced-answer protobuf cells | (a) footprint 2x2 → the visualiser's 3x3 superset → FAIL on `OFF_FOOTPRINT`; (b) **mine, run independently of the builder subagent**: `atk_team == our_team` → `atk_team is not None` → FAIL, 5 assertions, on `TEAM_enemy_attacks_our_footprint` and `SEAT_ceiling_bytes_other_seat` |
| `tools/loki19_5d.py` (5d) | `LOKI19_5D_SELFTEST: PASS`, 10 cells | (a) Amendment 3b's `AND` → `OR` → FAIL on `3c row 2 big fall, CI straddles`, the cell that exists for exactly that reading; (b) drop `hold_pinned`'s normalisation → FAIL on `NORMALISED` and `BOOTSTRAP separates arms` |
| `tools/ring_read.py` (5d decode) | `RING_READ_SELFTEST: PASS` — re-run green by me before use | pre-existing self-mutation harness |
| `tools/leg_read.py` (5c) | pre-existing | pre-existing |
| `scratchpad/hp_ledger.py` (§3 check) | **no selftest — see below** | — |

**⛔ `hp_ledger.py` HAS NO SELFTEST AND ITS FIRST OUTPUT WAS WRONG.** It reported
enemy healing of **4x10^21 HP per game**: a protobuf `int32` holding a negative
value is sign-extended to 64 bits, and I folded it back at 2^32 instead of 2^64.
**It announced itself only because the wrong number was absurd.** A sign error
that landed at 1.5x instead of 10^19x would have been published. Its result is
kept because the corrected walk **independently reproduces `leg_read`'s core-kill
counts exactly on both arms**, which is an external check the ledger could not
fake — but that is a validation found after the fact, not a test.

**Seat/parse validation on every decode: replay winner tally == platform
`scoreA` in 10/10 matches, both arms, both tools.**

---

# 10. WHAT THIS LEG MAY NOT BE READ AS (§7, enforced)

Not a win-rate result. It borrows no bar from LOKI-QUIET's 12/15, LOKI-16 or
LOKI-16b. **No threshold was revised because an implementation reached a
different number** — the one change made to an instrument mid-read-out (5d's
stratum filter) moved the analysis TOWARD the pre-registered spec, not away, and
the all-games figure is printed beside it. `jackpot` is excluded from the
retention stratum. The local dose figure from §4 is not treated as evidence of
effect. **Kidnap effectiveness remains a DECODER GAP and is not read as a null.**

---

# 11. ⭐⭐ THE SURPRISE, WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY

> **⛔ STATUS OF THIS SECTION, FENCED ON THE SIDE LANE'S AUDIT AND CORRECTLY:
> OBSERVATION, WITH ITS MAGNITUDE MARKED INSTRUMENT-UNVERIFIED. NOTHING MAY BE
> SIZED OFF IT UNTIL `hp_ledger.py` HAS FORCED-ANSWER CELLS.**
> The programme says a surprise is written down before it is explained away, so
> this stays where it is. But the external validation in §9 confirms **core-kill
> COUNTS** (18/50, 24/50) and this section's content is a **healing MAGNITUDE** —
> a different quantity, and an untested one. **Recording is not licensing.** The
> distinction costs nothing today because §11 is not a build input; it becomes
> load-bearing the moment somebody prices a heal-rate-beating dose, and this is
> the sentence that must stop them.

**The peck works, and the opponents answer it with healing — in five cells out of
five.**

| cell | our core damage t/c | their healing t/c | net t/c | core kills t/c |
|---|---|---|---|---|
| Askar City | 1522.3 / 619.2 | 1128.3 / 267.0 | 394.0 / 352.2 | 6/10 / 7/10 |
| Landers | 1352.4 / 1018.8 | 1183.2 / 874.4 | 169.2 / 144.4 | 3/10 / 1/5 |
| Lunds Stallions | 519.8 / 535.3 | 142.6 / 80.0 | 377.2 / 455.3 | 7/10 / 9/10 |
| SmartFridge | 431.8 / 264.6 | 254.6 / 90.4 | 177.2 / 174.2 | 1/10 / 2/10 |
| farming_200s | 332.4 / 344.4 | 261.2 / 163.3 | 71.2 / 181.1 | 1/10 / 5/15 |

**Healing rises in 5 of 5 cells** (pooled median 23 → 287 HP/game, a 12x jump).
Damage rises in 4 of 5. **Net damage does not improve, and pooled it is
−27.4 HP/game.**

**The exchange rate is the thing, and it is in this repo's own rules table:** a
peck is **2 Ti for 2 damage**; a heal is **1 Ti for +4 HP to every friendly
entity on the tile**. **Titanium-for-HP, the defender's answer is four times more
efficient than our attack** — and unlike our peck it does not cost the healer a
raider's position, because their healer is already home. **We are spending an
arrived raider's round on the losing side of a 4:1 trade, against an opponent
behaviour that was largely dormant in the control arm.**

**This is a HYPOTHESIS about mechanism, not a finding.** It is consistent with
every cell and with the currency direction, and **it is not established** — the
healing column cannot be attributed to a trigger, no leg has tested it, and
**`FIXTURE_OF_RECORD: live_unrated` plus the standing rule that a refutation
without live-game backing is a hypothesis means this may prioritise a road and
may not close one.** What it does do is name a cheaper question than the one
LOKI-19 asked: **the peck's problem may not be that it costs a move; it may be
that 2 damage is under the opponents' heal rate.** A dose that clears +4 HP per
builder-turn — or a target that cannot be healed — is a different plank, and it
is the one this leg argues for.

---

# 12. PROCESS FINDINGS, ROUTED AT WRITE TIME

1. **A GATE MUST BE POWER-AUDITED LIKE A BAR.** §6 tabulated what resolves at
   n=50 for every bar and never asked it of gate 5a-bis — which then arrived
   under-resolved and decided what the leg may claim. **→ behaviour change,
   promoted to the builder boot config: a prereg's resolution table must include
   every GATE, not only every BAR.**
2. **AN ESTIMATOR'S NAME IS NOT ITS DEFINITION.** §5b said "HP removed" and
   computed gross damage dealt; the gap is exactly the opponent's healing, and it
   was invisible until the number exceeded a physically possible value. **→ a
   bar that names a physical quantity states its CEILING, so an impossible
   reading is caught by the bar rather than by luck.**
3. **`hp_ledger.py` shipped a number with no selftest and was saved by absurdity.**
   **→ instrument change: it stays in `scratchpad/` and its §3 result is quoted
   only with its external validation attached.** Do not promote it to `tools/`
   without forced-answer cells.
4. **A DANGLING PRONOUN IN A BOOTED DOCUMENT PRODUCED A FALSE REFUTATION TWO
   LANES DOWNSTREAM.** HANDOVER read *"Use `scratchpad/ring_read.py`. **Its**
   `--selftest` PASSES and is worthless"* where the subject was
   `ring_retention.py`. I copied that antecedent into an audit brief, the audit
   mutated `ring_read.py`, found the defect absent, and reported the claim
   refuted — **truthfully, about the wrong file.** The side lane caught it.
   **→ HANDOVER corrected in the same commit as this read-out; the rule is that a
   document naming two files by one shape must name each in full.**
5. **THREE DEFECTS ON ONE CELL WAS FOUND BY THREE LANES SEPARATELY AND BY NOBODY
   DELIBERATELY.** Arrival admission, version churn and seat inversion all landed
   on SmartFridge and each was noticed in isolation. **→ OBSERVATION — NOT
   ROUTED**, pending a cheap per-cell defect roll-up at panel-admission time.

---

# 13. WHAT THE LEG COST, AND THE LOCK CERTIFICATE

Verified by the side lane on primaries, not accepted on report.

**RATED COST: ZERO, read at the PAIRING BOUNDARY and not on the match counter**
— CLAUDE.md is explicit that the counter proves no match COMPLETED and is blind
to whether one was PAIRED. Per-match `ourver` off `league_matches.tsv` across the
whole period: `04:32:59 v104` · `04:52:59 v104` · `05:12:59 v104` ·
`05:32:59 v104`. **Four consecutive ladder pairings, none carrying v108.**
Prototype exposure was **16 seconds per window** (04:53:16–04:53:32 and
05:00:53–05:01:09); W1 begins 17 s after a pairing with 19.5 min of clear air.
The pairing cadence was **re-derived from today's rows** (minute ≡ 12 mod 20,
second `:59`, 4/4) rather than taken from the file, per the never-hardcode rule.

**LOCK CERTIFICATE, two clocks, and the tightest margin is 34 seconds in the
right direction:** Amendment 3 committed `e775a0c` **05:00:20Z**; first treatment
match created **05:00:54Z**. The 04:53 attempt cannot contaminate it — **0/5
accepted, all five rate-limit rejections**, so no treatment game existed from it.
Amendments 1 (04:38:07Z) and 2 (04:46:21Z) precede the treatment arm by 22 and 14
minutes. **Three amendments inside a 56-minute leg window is the SHAPE of a
lock-discipline failure and the side lane went looking for one; it is not one
here.**

**⚠ ONE MECHANISM FLAG, which changes no number and is still worth the line:**
`loki19_treat_w1.sh` waits for the derived pairing boundary **exactly once, at
the top**. The log shows `boundary passed, starting` before W1 and **no such line
before W2** — so the 05:00:50 activation never passed through the guard. It
landed in clear air anyway (12 minutes from the nearest pairing either side), so
nothing was risked, **but the second activation's safety was a property of when I
happened to re-run the script, not of the guard.** → routed: the boundary wait
belongs **inside** the retry path, not above it. `tools/unrated_run.sh` is the
runner of record and must be checked for the same shape before the next leg.

---

# 14. WHAT THIS LEG DID NOT ANSWER, STATED SO IT IS NOT REDISCOVERED

* Whether the changed premise holds — **the gate did not resolve** (§2).
* Whether the peck helps or hurts the currency — **MDE 28.0pp against an observed
  −12.0pp** (§4). §6: *"Pooling more windows is the ONLY route and windows are
  free."*
* Whether the peck costs retention — **the falsifier's interval is ±0.16 on a
  quantity whose per-cell spread is 0.58** (§5).
* Whether the healing response is CAUSED by the peck — §11 is a hypothesis with
  no live test behind it.
* **Whether any of this survives the seat and map imbalances** (§6), which are
  disclosed and unpriced.
