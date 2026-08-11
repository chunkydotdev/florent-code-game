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
