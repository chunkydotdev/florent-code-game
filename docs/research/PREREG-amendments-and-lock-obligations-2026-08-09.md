# PREREG amendments + standing obligations for the next leg-lock doc

**Side lane, 2026-08-09 16:1x CEST.** `PREREG-ouroboros-loki2-2026-08-09.md` is
LOCKED and immutable; per its own amendment clause, corrections land as new
dated docs. This is that doc. It also pre-commits the obligations the NEXT
leg-lock doc must honour, so a session reboot cannot lose them — they were
agreed in session messages, which die with sessions.

**Version tag:** live v94 = `bots/_v115dodge` (v92 Eir tree). `_v118loki2b`
submitted as v93, not active. Kidnap plank `bots/_v119*` IN BUILD (2dcbae8),
reshaped to healer-exile primary. Source for everything below:
`ouroboros-baseline-drift-and-unrated-legs-2026-08-09.md` (research arm,
bc19a76), computed blind and diffed against the frozen table.

## Amendment 1 — the `saga/b` cell is not 0%

The frozen table's sentence "every cell is 0%, any single win is signal" is
FALSE for `saga/b`: the true cell at freeze time was **1/7 = 14.3%** (aggregates
15.3%→16.8%, tiebreak 14/64→17/68). Cause is **decode latency, not post-freeze
play**: ladder match `3f1be807` (5 games, ourver 92) was PLAYED 14:42 CEST, 55
min before the 15:37 freeze, but had not reached `ladder_games.tsv` when the
table was cut. Removing that one match reproduces the frozen table exactly —
no methodological disagreement.

**The falsifiable prediction is untouched:** saga is not a primary map, and the
five primary maps remain **0/50 across both seats** (`drumlin/a` drifted 0/5→0/6,
still 0%).

**Process rule adopted (the s24 freeze rule pointing at a different clock):**
freezing from `corpus/` freezes what has been DECODED, not what has been
PLAYED — here ~3h apart. Any future prereg baselined on the corpus must sync
immediately before freezing, or state the lag it accepts.

## Amendment 2 — probe facts confirmed from primary source, with the confounds named

Both unrated Ouroboros legs confirmed game-by-game via `fcode match list/info`
(free channel; the corpus is structurally ladder-only and cannot see them):

- **Leg A** baseline `3c6d91d2`, v92, 15:22 CEST, all seat b, 1–4; 3/5
  core-decided; our win = saga tiebreak r1000.
- **Leg B** probe `d4db288e`, v93 `_v118loki2b`, 15:49 CEST, all seat a, 1–4;
  5/5 core-decided; our win = **lighthouse core kill r211** — a primary-map
  seat-a cell that is 0/8 on the ladder, and the only game of the ten inside
  `KILL_WINDOW_RND: 250`.
- The 15:46 per-map conversion prereg (ca3c3f8) stands **fully refuted** as
  committed: atoll/eider/nordkap did not convert, saga was lost, and the map
  predicted untouched (lighthouse) is the one that converted.

## Obligations binding the next leg-lock doc (pre-committed now)

1. **Leg A is not a blind control.** It completed 15 min before the 15:37
   lock and was observable at lock time. If used as Leg B's comparator, or as
   any future leg's, it must be labelled OBSERVABLE-AT-LOCK, never presented
   as pre-registered.
2. **The A/B seat confound is named.** Leg A all seat b, Leg B all seat a; the
   "tiebreak→core kill" movement also moved map and seat. No paired-cell claim
   may be built on it.
3. **Leg B is half a leg against the bar.** n=5, 1 core-kill win vs a bar of
   ≥3/10. No verdict language; the clean datum is the win-condition mix moving
   3/5→5/5 core-decided — in both directions (the four losses too).
4. **`drumlin` and `hive` are fully blind.** Neither appeared in either leg;
   no probe evidence exists on two of the five primary maps.
5. **The kidnap-plank leg gets a NEW prereg doc** (ruling of 16:2x, bbcaec7):
   outcome bar unchanged (≥3 core-kill wins/10 on the 0%-maps), mechanism
   clause rewritten to "measured collar denial enables the kill" (win without
   measured denial = off-prediction), secondary metrics = enemy-core
   HP-recovery r0–250 + collar-seat occupancy denial, and the anti-Goodhart
   sentence: denial metrics up + currency flat = null.
6. **Opponent choice waits on the collar-heal staffing number** (research, in
   flight): if Ouroboros staffs ~0 collar healers, a denial leg vs them is
   unfalsifiable and CAD is the discriminating opponent.

## Addendum, 16:3x CEST — the 15:46 prereg's lock certified, its refutation sharpened, obligation 7 adopted

Research certified the 15:46 conversion prereg's lock against two independent
clocks: `ca3c3f8` git author time **15:46:23 CEST**; Leg B platform
`createdAt` **15:48:56 CEST** (ran 15:49:02→15:49:53, 57 seconds). **The
prereg predates leg creation by 2m33s — genuinely blind to Leg B.** (This
paragraph supersedes the bare "15:46/15:49" times above; the two-clock form is
the one that survives a reboot.)

**But the refutation is sharper than "fully refuted", and one half of the
prediction was unfalsifiable as worded.** Side-by-side on win condition (a
game property, so it survives the A/B seat flip):

| map | Leg A (v92) | Leg B (Loki-2b) | prereg said |
| --- | --- | --- | --- |
| atoll | core L 563 | core L 720 | "converts to core kill" |
| eider | core L 521 | core L 338 | "converts to core kill" |
| nordkap | core L 279 | core L 361 | "converts to core kill" |
| **lighthouse** | tiebreak L 1000 | **core W 211** | "does not touch" |
| **saga** | tiebreak W 1000 | **core L 351** | "does not lose" |

Atoll/eider/nordkap were **already core-decided at lock time** (Leg A completed
15:22, observable at 15:46) — read as "core-decided rather than tiebreak" the
prediction was pre-satisfied and could not fail honestly; read as "core kills
IN OUR FAVOUR" it went 0/3. And the only two games whose win condition changed
are exactly the two the prereg excluded from change. **The prediction was
anti-correlated with its own outcome variable: 2/2 on excluded maps, 0/3 on
named maps.**

**Obligation 7 (adopted, generalises past Ouroboros):** a pre-registration
must state whether its outcome is the win-condition MIX or the win-condition
IN OUR FAVOUR, and must verify the predicted-change set is not already in the
target state at lock time. A prereg predicting change on cells already changed
cannot fail honestly. (The LOCKED 15:37 file already satisfies this — it names
"`core_destroyed` in OUR favour, not a tiebreak steal" — which is the template.)

## Addendum 2, 16:4x CEST — obligation 3 sized with numbers; denominator rule; the r74 outlier

From research's v92 unrated-baseline audit (`v92-unrated-baseline-audit-2026-08-09.md`,
b9394ef), adopted into the obligations:

**Obligation 3 is amended to carry its own numbers:** the 3/5→5/5
core-decided movement is **Fisher one-sided p = 0.2222** (two-sided 0.4444) —
a direction, not a result — and at fixed bot version v92's own core-decided
share spans **0%→100% by opponent** (CAD 100%, KCM 75%, Ouroboros 60%, Lunds
50%, Powerpuff 0%), wider than the 60%→100% the probe is read for. The
same-opponent framing (Ouroboros vs Ouroboros) remains the right comparison;
these numbers size it so no later reader inflates it.

**Obligation 8 (denominator rule):** the 4-13 v92 unrated baseline is
game-pooled from legs of **5/5/4/2/1** maps (verified fired-short, not
truncated). Ouroboros and CAD carry 29% of it each, Powerpuff 6%. Any "LOKI
delta vs baseline" compares **per-opponent or states the Ns**; the five teams
are not five comparable cells.

**Noted, not an obligation:** `f92f1ca2` game 5 (nordkap, seat a, unrated,
v92) — **CAD core killed at r74**, resignMessage null. CORRECTED SCOPE
(research amendment, same day): fastest **vs CAD** (ladder best against them
r103, n=15 core-kill wins, median r194), NOT fastest overall — the bot has
killed at r58, and Ouroboros at r65. Still well outside the known CAD
distribution; autopsy in flight, re-briefed with the corrected table so it
does not over-read an "unprecedented" event that isn't.

## Addendum 3, 16:5x CEST — obligation 6's premise REFUTED, conclusion survives on a different mechanism; obligation 9 added (denial must be priced in seat-rounds)

From `opponent-collar-heal-staffing-2026-08-09.md` (a21e742; decoder validated by
reproducing all 13 census cells to the digit, with genuine zeros — The Bisons,
0 core heals in 35 games — proving the detection floor):

**Obligation 6 as originally written carried a premise the data refutes.** The
near-zero hypothesis is DEAD for both teams: Ouroboros staffs its collar on
40.7% of rounds and recovers **53.7%** of the core damage we inflict (CAD:
39.3%, 40.3%). "A denial leg vs Ouroboros is unfalsifiable because there is
nothing to deny" is false and must not appear in the leg-lock doc — the first
opened replay would refute it.

**The conclusion — fire the denial leg at CAD — survives on the correct
mechanism:** the discriminating variable is OUR approach rate, not their heal
policy. In the r151–300 band we inflict **68.0 HP/100rd** on CAD's core vs
**9.3** on Ouroboros's (6× the denial volume) while their per-damage heal
reflex is near-identical (11.1 vs 13.5 per 100 HP). Against Ouroboros the leg
would measure our own approach rate, not denial. Identity read agrees: CAD
spends **42.3%** of all heals on its own core (garrisoner), Ouroboros **22.9%**
(field healer). **The leg-lock doc states THIS rationale, not the refuted one.**

**Obligation 9 (denial is priced in seat-rounds, not throws):** post-throw
dwell (`post-throw-tile-dwell-2026-08-09.md`) measures modal dwell **1 round**
(96.4% of enemy victims gone within one) and the throw→gunner-kill outcome at
~1 in 200. So one throw ≠ one denied healer; a throw buys roughly (1 + walk-back
distance) seat-rounds of absence. The leg-lock doc's mechanism metric must be
**collar-seat-rounds denied** (and heals/100HP suppressed in-window vs the CAD
baseline of 11.1), with throws/game recorded so a null decomposes into "few
throws" vs "throws that didn't deny". A claim of caused denial without
seat-round accounting is off-prediction.

Matchup caveat carried from the source doc: all opponent rates are confounded
by our own bot; only damage-normalised columns are behavioural, and no version
stratification exists (dead columns). If the leg disagrees with the doc, an
opponent version change is an unexcluded explanation.

## Addendum 4, 17:1x CEST — KIDNAP LEG STOOD DOWN before firing; obligations convert to templates for the next leg

Builder stand-down, direct message: LOKI-3 (`bots/_v119loki3`) built, gated,
crash-free across 96 games — and **not going to battery**. It failed its own
pre-registered treatment-occurrence bar (throws 16.7% vs bar 30%; collar-aim
placement 33.3% FAIL) measured BEFORE the battery. Root cause is on our side:
LOKI already seals collar seats with 3 Ti barriers, so a sealed seat has no
healer left to kidnap — the denial job had a cheaper mechanism on the chassis,
and a 20 Ti +10%-scale launcher evicting one body that walks back (obligation
9's dwell numbers) never reached dose. **Honest status of the mechanism
signature "measured collar denial enables the kill": never dosed — not
refuted, not confirmed.**

Consequences for this doc:
- **No leg-lock doc is owed** for a leg that never fired. Obligations 1–4
  (Leg A labelling, seat confound, half-leg sizing, drumlin/hive blindness)
  remain live for ANY future Ouroboros leg. Obligations 5, 6 and 9's
  kidnap-specific clauses convert to **templates**: the next leg's prereg
  re-instantiates them with its own mechanism.
- **The next mechanism, per the builder's re-aim on research's incidence
  table, is ARRIVING, not clock speed:** 74.4% of our 827 core-kill wins are
  already inside r250 (holds at 1600+: 71.4%); vs Ouroboros we win by kill in
  5.8% of ladder games but 8 of those 9 are ≤r250 (median r95). The scarce
  event is the kill happening. Research is running the incidence cut (what
  separates the 5.8% from the 94.2%); the next leg's pre-registered mechanism
  clause should be arrival-denominated, bar unchanged (core-kill wins per 10
  on 0%-maps — already share-denominated, which is why it survives the re-aim
  untouched).
- Drift-watch note (D5/D6, for the record): the stand-down is the OPPOSITE of
  drift — a treatment-occurrence bar measured pre-battery, a null owned as
  "never dosed" rather than banked or buried. This is the template.

## Addendum 5, 18:4x CEST — obligation 10 (closure needs identity) and the discriminating condition any CAD leg must carry

From `cad-suppression-mechanism-2026-08-09.md` (research, 225 games): healer
displacement REFUTED as the suppression mechanism despite the arithmetic
closing at ratio 1.00 — the ledger's two sides belonged to DISJOINT bots
(heal turns on-collar; missing builds off-collar, structurally unable to heal
the core). What CAD actually does under early core fire: off-collar builders
holding ≥30 Ti build on 0.94% of turns vs 8.25% undamaged — solvent, moving
normally, cooldown-free, idle.

**Obligation 10 (companion to the zero-not-lower rule):** a closure test must
verify that the SAME UNITS account for both sides of the ledger — aggregate
magnitudes that balance across disjoint populations are a coincidence reading
as a mechanism. Two bars, both required: the effect's signature must match in
kind (zero-not-lower), and its accounting must match in identity.

**Discriminating condition for ANY future CAD leg (pre-registered here so it
is designed in, not discovered after):** the population data cannot separate
"CAD reacts to core damage" from "CAD reacts to a raider present in its
base" — in the corpus they are the same event. The two set different prices:
presence-triggered means a body in their base buys ~25 rounds of build
suppression WITHOUT landing a hit; damage-triggered means the raider must
connect. The leg that decides it: a raider that arrives and deliberately does
NOT attack (one-flag variant of an existing raider), paired against the
attacking control. A CAD leg fired without this arm cannot attribute its own
result to the right trigger.

## Addendum 6, 19:0x CEST — the no-attack arm ran and is INVALID; obligation 11 (verify the treatment the EXPERIMENT requires)

The discriminating arm this doc required (addendum 5) fired and failed for a
reason the requirement itself did not guard: LOKI-QUIET's treatment held
exactly as coded (0 builder attacks in all 5 live games, decode-verified) and
was irrelevant — the flag silenced builder melee but never gated the forward
SENTINEL, which fired 43–315 shots/game and killed CAD's core in 3 of 5.
Builder's own words: "I verified the treatment I CODED, not the treatment the
EXPERIMENT REQUIRED." Damage-vs-presence remains OPEN.

**Obligation 11:** a prereg's treatment check must be expressed in the
experiment's causal variable, not in implementation terms. For any future
presence arm the check is "**enemy core HP never decreases**" (and, generally:
state the invariant the hypothesis needs, then verify THAT by decode — a
clean check of the wrong quantity is worse than no check, it launders an
invalid arm as verified).

Salvage, properly damped: a bot landing zero builder melee went 3-2 vs CAD
with three core kills — builder melee (peck, siphon, counterbattery) is not
load-bearing against them. LOKI-4's own read: 8-7, 53.3% core_kill_share on
three real opponents, 18/20 games core-decided; the Ouroboros 3-2 vs 1-4
baseline is two different experiments (2/5 shared maps), not a before/after.

## Addendum 7, 20:1x CEST — upward-leg framing (from the upward pricing, 460d40a)

Any upward unrated leg (≥1650 opponent) pre-registers as **MEASUREMENT, not
climb**: the question is "what does a stronger defence do to our arrival/kill
mix", never "can we win upward" (every ≥1750 team kills us at 0–12%; a win
prediction would be predicting the tail). Recommended first target from the
pricing: **Landers (+103)** — our 25-game base runs 36% kills, 32% inside
r250. Bars per band, never pooled (obligation 8). And the leg's read must
carry the weapon-mix covariate: top-tier cores die 53.1% gunner / 44.4%
sentinel / 2.5% melee while our mix inverts it (22.7/69.2/8.1) — a
quiet-melee-line result upward is a result about the mechanism that does
2.5% of the killing there, and must not be read as pricing the other 97.5%.

## Authority

Amendments: side lane (this lane owns the PREREG discipline). Data: research
arm, blind-computed, primary-source-confirmed. Verdicts: none here — firing
and verdicts remain the builder's.

## Addendum 8, 2026-08-11 06:3xZ (s30) — OBLIGATION 12: A GATE IS A BAR AND MUST BE SIZED LIKE ONE

**Found in the LOKI-19 read-out audit, and the miss is THIS LANE'S.** I reviewed
Amendment 1b before the treatment arm fired and reported no flags on it.

**WHAT 1b DID RIGHT, which is why the omission was invisible:** it named its
statistic (INSERT reach), its population (control arm, in-arm, this leg's own
games), its per-cell rule (*"never pooled — a 6x spread makes a pooled mean a
fiction"*), it barred stored figures, and it pre-committed a **three-branch
reading table** (`>30%` / `20–30%` / `≤20%`) written before the number existed.
By every check on this lane's prereg list it is a model amendment.

**WHAT NOBODY ASKED — including me, and I own this list:** *at what n can this
gate tell its own branches apart?* Its bands are **10 percentage points wide**
and it was answered by **19 events across 50 control games**. Askar's lower
bound sits at 30.06%, i.e. astride a branch boundary. **The gate could not
resolve the question it was built to decide, and nothing in the document
required it to say so in advance.**

**⇒ OBLIGATION 12. A GATE CARRIES ITS OWN RESOLUTION STATEMENT: the n at which
it discriminates its branches, and — pre-committed — WHAT HAPPENS WHEN IT DOES
NOT.** We size bars as a matter of course (`KILL_SPEED_MIN_N`, MDEs, the
2,100-games-per-arm note) and **we have never once sized a GATE**, because a
gate looks like a definition rather than a measurement. It is a measurement.

**THE DEFAULT, pre-committed here so it is not a judgement made at read-out:
AN UNRESOLVED GATE DEFAULTS TO THE RESTRICTION, NEVER THE PERMISSION.** The
builder ruled exactly this way on LOKI-19 without a clause to lean on, and the
reasoning is the one to keep: **1b's own sentence is *"This gate cannot flatter
the result"*, and granting the permissive branch on an estimate that cannot
distinguish delivery from non-delivery is precisely a flatter.** The restrictive
default is the only branch that cannot launder a result.

**COMPANION, from the same audit — TWO IMBALANCES ARE ONE DEFECT AND MUST BE
NAMED ONCE.** LOKI-19 disclosed a seat-mix difference in all five cells
(SmartFridge a complete inversion, 10xB vs 10xA) and a map-mix difference
(`jackpot` 4v1, `eider` 1v4, `lighthouse` 6v2, `drumlin` 4v2) as two separate
facts. **They are one property — the arms were not balanced on the fixture axes
— and the same imbalance drives the retention stratum's asymmetric exclusion
(treatment 50→46, control 50→49).** Disclosing rather than correcting is right
(a matched estimator chosen after the data is the fault this line exists to
catch), **but a future pooled reading inherits BOTH and is far likelier to carry
one named confound than two scattered ones.** D52b — a correction lands where it
was discovered, not where it will be read — applied INSIDE a document.
**Prereg consequence: where a leg's arms are assigned by anything other than an
explicit balancing rule, the prereg names the fixture axes (seat, map, opponent
version) and pre-commits to reporting imbalance on all of them under ONE
heading.**

**AND ONE OBLIGATION THIS AUDIT DID NOT PRODUCE, recorded so the absence is
deliberate:** nothing here requires a leg to CORRECT for these. Correcting
post-hoc is worse than disclosing, and LOKI-19 got that right.

## Addendum 9, 2026-08-11 07:0xZ (s30) — OBLIGATIONS 13 AND 14, BOTH INTERIM GUARDS FOR SCRIPTS THAT ARE QUEUED AND UNBUILT

**Written because both fixes are routed to the builder and neither exists yet.
A prereg locked before they ship must carry the requirement by hand, or the gap
sits open for exactly as long as the queue does.**

### OBLIGATION 13 — A PREREG NAMES THE `file:line` ITS MECHANISM METRIC READS, AND ASSERTS THAT PATH APPEARS IN THE TREATMENT DIFF

The human form of the D42 checker (spec:
`docs/research/TRIAGE-prose-only-deltas-2026-08-11.md`, routed to `tools/`).

**THE INCIDENT IT CLOSES IS THREE HOURS OLD AND COST A WINDOW.** LOKI-18's bar 1
measured `shootable-on-build` on a diff that was **one hunk in `main.py:560`**,
while the metric sits downstream of a `can_fire_from` guard in **`raid.py`, which
was byte-identical between arms.** The metric therefore read **100% in BOTH
arms** — 39/39 treatment, 229/229 control, live — and **could not have moved
whatever the plank did.** 25 unrated games.

**THE OBLIGATION, one line in the prereg:**
`MECHANISM METRIC READS: <file:line>. TREATMENT DIFF TOUCHES: <paths>. INTERSECTION: <yes/no>.`
**If the intersection is NO, the bar is INERT and the leg may not be fired on
it. If the prereg cannot name the file:line, that is the finding** — an
unnameable read path is not a measured one.

**AND THE POSITIVE HALF IS NOT OPTIONAL:** a check that answers NO to everything
looks correct. **The obligation is satisfied by naming the path, not by asserting
the intersection** — LOKI-19's 5a dose bar reads exactly the gate its diff
changes and answers YES, which is what a healthy answer looks like.

### OBLIGATION 14 — A PANEL CELL IS SCORED ON OPPONENT VERSION STABILITY BEFORE IT IS SELECTED

**Evidence:** `docs/research/PANEL-selection-version-stability-2026-08-11.md`.
D13 replaced *rating proximity* with *"measured mid-range performance against
us"*. **That criterion then selected the cell it could not measure:
SmartFridge is the MOST mid-range opponent on the board (51.4% over 35 v104
games) and ran TEN versions in 24 hours**, producing five independent defects in
a single day — failed arrival precondition, no version-matched control, a seat
inversion, the most favourable 5d number, and a control arm that is itself a
blend of two opponent bots.

**THE OBLIGATION:** a prereg naming its cells states, per cell, **the opponent's
distinct-version count over the preceding 24 h**, and treats a high-churn cell as
**reportable but not poolable**. Free off `league_matches.tsv`.
**THE DENOMINATOR NEEDS NO NORMALISATION AND THAT IS MEASURED, NOT ASSUMED:
every team in the league played EXACTLY 87 matches in the window**, so version
counts are directly comparable and the volume confound cannot arise. Re-check
that at selection time rather than inheriting it — it is a property of the
league's scheduler, not a law.

**Companion, so this is not read as a strength claim:** sweep 22 measures
freshly-shipped versions as **STRONGER** (matched DiD **+0.524**, t = +4.89).
**A stable cell is a READABLE one, not a weak one.**

---

## Addendum 10, 2026-08-14 ~15:0xZ (s40) — **OBLIGATION 15: A PREREG DECLARES ITS MECHANISM'S MAP DEPENDENCE, OR DECLARES THAT IT EXPECTS NONE**

**THE INCIDENT.** Magnus, direct, this session: could map-segment effects be
CANCELLING tactics that we pool across all maps — and we do not account for it
when building experiments. **Checked: none of s40's six preregs declared a
segment split.** Supporting evidence, all from the same day: **V141VS140's 29pp
per-map spread** · the s39 audit's **map-interaction DEFF outliers at 1.20-1.25**
· **`#54`'s lock concentration on midgard (35.6% of builder-rounds vs 3-8% on
small maps)** · and **v142 being a terrain-fingerprint router with no
opponent-identity reads — an opponent has already shipped map-conditional
policy while we screen pooled.**

**THE ARITHMETIC THAT MAKES THIS A REAL LOSS AND NOT A REFINEMENT: a plank worth
+6pp on 5 of 15 maps pools to +0.67pp.** Against any bar this project types, that
is a null. **A pooled screen does not measure a conditional plank weakly — it
measures it as ZERO, and the road closes.**

### THE OBLIGATION, three parts

**15a. EVERY screen prereg carries a MAP DEPENDENCE line.** One of:
* `MAP SEGMENT: none expected — <why the mechanism is map-invariant>`, or
* `MAP SEGMENT: <named set> — <mechanism reason> — EXPECTED DIRECTION <sign>`.

**⛔ THE EXPECTED DIRECTION IS NOT OPTIONAL.** A segment declared without a
predicted sign is unfalsifiable: whichever way it lands, it "confirms" the
mechanism. **The direction is what makes it a test.**

**15b. EXACTLY ONE PRIMARY SEGMENT. Any others are DESCRIPTIVE.**
*(This clause is mine and is not in the version handed to me — without it, 15c
becomes a licence: declaring K segments gives K chances to rescue a failed arm,
which is textbook subgroup fishing and is how a 51-bar gets defeated by anyone
patient enough to enumerate. One primary, declared before the fire.)*

**15c. A POOLED-FAIL THAT CLEARS ITS PRE-DECLARED PRIMARY SEGMENT RE-SCREENS ON
THAT SEGMENT** and, if it holds, ships MAP_CODES-style conditional. ⚠ **The
re-screen is a NEW leg with its own n — not a re-read of the same rows.** The
rows that suggested the segment cannot also confirm it.

### SEGMENT VOCABULARY — pick from these or define one with a mechanism reason
* **SIZE CLASS** — the default: `small` · `mid` · `900-area` (the 30×30s:
  midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep).
* **MECHANISM-SPECIFIC, and usually better than size** —
  **ring-geometry maps** for seal/spawn-ring planks · **lock-heavy maps** for the
  `#54` nav family (midgard 35.6%, ragnarok 14.1%, valkyrie 12.8%) ·
  **open-lane maps** for sentinel/gunner line-of-fire planks · **long-approach
  maps** for raid/transport planks.
**A mechanism-specific segment beats a size class whenever the mechanism names a
terrain property — size is a proxy for the property, and a proxy dilutes.**

### AND THE UNITS RIDER, because it is the same day's other lesson
**A per-map or per-segment bar does NOT take the match design effect** —
verified, (match, map) pairs with more than one game = **0 of 415**, since a
5-game match uses five different maps. **The residual is the OPPONENT cluster:
ρ = 0.0743, m̄ ≈ 2 games per opponent per map cell ⇒ DEFF ≈ 1.07.**
**Enumerate both clusters per `CLAUDE.md`'s scope procedure; do not carry 1.53
into a segment bar.**

---

## Addendum 11, 2026-08-14T23:41:01Z (s42) — **OBLIGATION 16: A BAR CARRIES A PRE-SPECIFIED MDE, OR IT CANNOT BE SIZED AND EVERY ATTEMPT TO SIZE IT IS CIRCULAR**

**Formulated by the builder (`50bab486`) out of an error we made jointly; REHOMED
HERE because that commit put it in `CLOSURE-queue-21-2-2026-08-14.md`, a dated
closure doc that NO lane boots — and this file is where preregs are written and
is in the side lane's boot sequence.** The s29 finding (*a rule promoted into a
file nobody opens*) applied to a rule about rules.

**THE INCIDENT, and both lanes own a half.** `#17`'s bar: *"≥10.0% of cell-P games
contain ≥1 weapon-attributable destruction."* Measured at n=60: **5.0%, Wilson
[1.71%, 13.70%] — contains the bar.** The re-run was then sized **off that 5%
point estimate**, giving n=300 and *"±2.47pp excludes 10.0%"*. **At n=300 the true
rate read 8.00%, Wilson [5.43%, 11.63%] — STILL contains the bar.**
* **Builder's diagnosis, verbatim and better than mine:** *"sizing a confirmatory
  run off the point estimate of the underpowered run it is meant to replace is
  circular — the estimate I was correcting is the estimate I sized with."*
* **Side lane's half: I CERTIFIED that sizing.** I checked the arithmetic, found
  it correct, and never asked whether **p=5% was a legitimate input.** Arithmetic
  verified, premise unasked — the borrowed-premise class, third instance from
  this lane in one session.

**⛔ AND THE CIRCULARITY IS NOT SPECIFIC TO A BAD FIRST ESTIMATE — IT IS A
PROPERTY OF SIZING OFF ANY OBSERVED POINT ESTIMATE.** Required n to exclude a
10% bar from above:

    truth  5%  ->  n =    73 / cell
    truth  8%  ->  n =   707 / cell     (the corrected figure; reproduces)
    truth  9%  ->  n =  3147 / cell
    p -> bar   ->  n -> INFINITY

**An estimate near the bar can never tell you how much data the bar needs.**

### THE OBLIGATION
**Every prereg carrying a BAR states, on the bar line, the effect it must be able
to EXCLUDE — a pre-specified MDE — and the n that exclusion requires.** One of:
* `BAR: <x>. MDE: we call it a MISS if the true rate is at or below <y>. n for that exclusion: <N>.`
* or a declaration that the bar is a **POINT RULE ONLY** and **licenses no
  exclusion claim** — which is honest and is what `#17`'s bar actually was.

**⇒ SIZE OFF THE VALUE YOU MUST EXCLUDE, NEVER THE ONE YOU HOPE TO OBSERVE.**

**⚠ THIS IS OBLIGATION 12 FOR BARS, REACHED FROM THE OTHER END.** OB12 requires a
GATE to carry its resolution statement; **a bar was never asked for one**, because
a bar looks like a definition rather than a measurement. **It is a measurement.**

**⭐ AND THE HALF THAT KEEPS THIS FROM BECOMING BAR-CHASING, from the same leg:
the builder did NOT re-fire at n=707, and was right.** Lethality on landing
**1.00 (128/128)**, delivery **~8% of games**, guarded control **104 arrivals /
zero deaths**. **The bar had become the least informative number in the leg.**
⇒ **An unresolvable bar is a reason to state what IS resolved, not a licence to
spend games until it resolves.** Sizing discipline exists to make bars honest,
not to make them mandatory.

### ⭐ OBLIGATION 16 — AMENDED 2026-08-14T23:56:13Z, THIRTEEN MINUTES AFTER IT WAS WRITTEN, BY ITS FIRST APPLICATION

**`SCREEN-bodyaware-2026-08-14.md` (`fafb68f6`) is OB16's first use and it
improved on the obligation.** I required the MDE **beside** the bar. It puts the
MDE **INSIDE** the bar's construction:

    BAR SOURCE: constructed, not observed — 50.00 + MDE(1.00pp) + half_width(0.93pp)
    MDE: +1.00pp. WE WILL CALL THIS ARM A MISS IF ITS TRUE LOCAL EFFECT IS AT OR BELOW IT.
    Clearing this bar means the 95% interval excludes BOTH 50.00 AND the MDE.

**⇒ ADOPTED AS THE PREFERRED FORM: `BAR = null + MDE + half_width`, so clearing
the bar IS the exclusion.** A bar built this way **cannot be quoted without its
MDE**, because the MDE is one of its terms. **A bar with the MDE merely stated
beside it can be detached from it by any later reader — which is how `#17`'s bar
came to be quoted, and sized, with no MDE in sight.** The prereg's own phrase is
the rule: **"MDE inside the bar rather than beside it."**
*(Second time this session a consumer specified my fix better than I did. Per the
arm retro's v1.9 note: the system routing around this lane's known weaker half is
acceptable; RELYING on it is not — so the improvement is adopted here rather than
left in one prereg.)*

**⚠ AND A SEVENTH D33 INSTANCE FROM THE SAME LOCK, on a surface nobody had
tested — recorded because it is the most consequential one yet:** `tle_census.py`
on a LOCAL game returns `tled / exec_sum / exec_max / over10k = 0` across **1,649
builder-turns**, while the same decoder reads **8,847 µs** on platform replays
(live positive control). **Local replays carry NO exec-time fields at all.** ⇒
**a local KEEP could ship a CPU regression invisible to every local test** — a
blind zero and a real zero, byte-identical, on the dimension that silently
destroys units. The lock splits its gate into a local proxy (retry-fire rate ≤20%,
ship-blocking on its own) and the platform `cpu_watch` alarm, which is the right
response: **when a surface cannot see a dimension, the gate moves to a surface
that can, rather than the dimension being dropped.**

### ⭐⭐ OB16 COROLLARY, 2026-08-15T03:52:45Z — **THE STANDARD COREFILL BAND HAS AN MDE OF ZERO BY CONSTRUCTION, AND THAT IS A PROPERTY OF EVERY SCREEN ON IT**

**Found while certifying the GUNAXABL/SENTTHR verdicts (`7ca0b370`), whose author
had already named the instance — this is the GENERAL form.**

    standard corefill band : 48.67 / 51.33 at n=5400
    half-width at n=5400   : 1.334pp
    => the band IS 50 +- half_width, so the implied MDE is 0.000pp

**Clearing 51.33 puts the CI's lower edge at exactly 50.00 — it just touches the
null and excludes NO positive effect size.** ⇒ **under OB16, every arm screened on
the standard band is a POINT RULE. It licenses "we can exclude 50" and NOTHING
about a minimum effect.** Contrast the OB16-form bar the same night:

    BODYAWARE : 50.00 + 1.00 (MDE) + 0.94 (hw) = 51.94   -> clearing it excludes 50 AND +1.00pp

**These are two different KINDS of bar and the difference is invisible from the
number alone.** ⇒ **a screen prereg states which kind it is using.** The standard
band is not wrong — it is the right instrument for *"does this move anything at
all"* — but **it must not be quoted as having excluded an effect size, because it
cannot.**

**⚠ AND GUNAXABL IS WHAT A ZERO-SLACK BAR COSTS, measured: it missed its keep edge
by 0.0152pp — ONE GAME** (2629/5400 = 48.6852% against a bar of 48.67; 2628 would
have been KEEP). **Its own prereg flagged the fragility IN ADVANCE — "bar slack
was zero by construction, margin 1.33pp vs half-width 1.320pp"** — which is OB16's
spirit honoured pre-hoc, before OB16 existed. **A bar with no slack produces a
verdict with no slack, and the honest reading of a one-game margin is that the
fixture cannot resolve the question.** The author refused to round toward the
answer they preferred; **that refusal is what the corollary is here to make
unnecessary next time.**

**⭐ AND THE REPLICATION DISCIPLINE ON THE SAME READ IS THE TEMPLATE, recorded so
it is not lost in a verdict commit:** remote replications existed
(GUNAXABLR 50.61%, SENTTHRR 47.92%) and were **reported separately and refused as
verdict inputs**, because the preregs registered `PLANNED n = 5400` and the remote
copies were stocked AFTER the lock without registering the pooling. **Pooling them
to move a verdict would be an unregistered n increase — optional stopping with
extra steps — and it would have been MOST tempting on GUNAXABL, the arm that
missed by one game.** ⇒ **they corroborate a null they are not allowed to rescue.**
**And both pairs STRADDLE 50 AND FLIP SIGN** — independent seed draws of one
comparison should preserve sign if an effect is real; neither does — **so the
replication strengthens "could not separate" rather than changing it.**
