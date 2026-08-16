# MDE CONVENTION AUDIT — is this repo sizing experiments at ~50% power without meaning to?

**Research arm, read-only, 2026-08-16.** Commissioned after a peer lane ran a keyword grep over
8 prereg files, found power language in 2, and correctly refused to file that as a finding.
This audit answers the **sizing** question by reading the tools and the preregs.

---

## HEADLINE

**The convention was defective, the repo found it ITSELF on 2026-08-14/15, fixed it as
OBLIGATION 16, and every prereg written after the fix is properly constructed.** The audit
reproduces that boundary independently and to the hour.

Two residual issues survive the fix, and both are real:

1. ⛔ **OB16 IS PROSE, NOT ENFORCEMENT.** `tools/prereg_check.py` has no `MDE` token in
   `KNOWN_KEYS` and no OB16 check. That tool's own docstring says *"The measured half-life of
   a prose rule in this repo is about one session."* OB16 is currently living on that half-life.
2. ⚠ **"MDE" NOW NAMES TWO DIFFERENT QUANTITIES IN THIS REPO**, and they differ by ~2.3x.

⭐ **And the harm did NOT materialise.** All three 50%-power legs that reached full n
(SENTTHR, GUNAXABL, V140VS146) reported their nulls as **`UNRESOLVED`**, named their margin, and
declined to promote the arm — never as "no effect". A fourth (`wirehold`) was **refused
authorisation on power grounds before firing**. The only nulls in this repo reported as
refutations from intervals straddling 0.50 sit at rows 108 and 171 of 415, at bot versions
`_v64`/`_v77`, and predate every piece of the current apparatus.

⚠ **But Residual 2 has already bitten once, today.** `MAP-CONDITIONAL-CEILING-2026-08-16.md:72,451`
twice calls a **post-OB16** result *"dead"* on a +0.24pp effect **inside its own ±0.93pp
half-width** — while correctly hedging a *larger* null two lines later. The failure is not in the
leg; it is a downstream reader converting *"did not clear the bar"* into *"the plank is dead"*,
which is precisely what the overloaded "MDE" label invites.

**Bottom line: NOT systemic, NOT ongoing. A closed defect with an unenforced fix and a live
naming collision.**

---

## 1. THE ARITHMETIC (verified, one correction to the brief)

An effect sitting exactly at `k × SE`, two-sided α=0.05:

| k | power |
|---|---|
| 1.960 | **50.0%** |
| 2.486 | 70.1% |
| **2.802** | **80.0%** |
| 3.242 | 90.0% |

`2.802 / 1.960 = 1.4296` ⇒ **n must be 2.044× larger** for 80% power than for the 1.96 rule.

⚠ **The brief states 51.0%; the correct figure is 50.0%.** Power at the boundary is
`P(Z>0) + P(Z<−3.92) = 0.5000 + 0.00004`. Immaterial to every conclusion, corrected for the
record because this project's own rule is that numbers carry their derivation.

---

## 2. THE CONVENTION IN CODE — three tools, and they do NOT agree

| tool | constant | power | what it computes |
|---|---|---|---|
| `tools/mde.py:92` | `Z = 2.802` | **80%** ✅ | MDE on kill-speed sd from a byte-identical null |
| `tools/leg_read.py:308-315` | `2.802` | **80%** ✅ | worst-case MDE on live panel cells |
| `tools/prereg_check.py:135,391` | `Z95 = 1.96` | — | 95% CI half-width, used by `BAR_RESOLVABLE` |

**`mde.py` is correct and knew about the problem.** Its docstring, line 17:

> *"Everything else in this repo quotes MDE from a BINOMIAL on win rate; this measures the
> CURRENCY's own variance."*

**`leg_read.py` is correct AND narrates the exact harm this audit was sent to look for**
(lines 300-310): the hardcoded string it replaced *"printed the SAME sentence at n=25 and at
n=150 … this one reassured two legs that had already spent their power … the audit's worked
case is a true 18pp on live cells showing as 7.2pp pooled at **~20% power**."*

⇒ **The 1.96-as-MDE error was diagnosed in this repo at s28 and fixed in the two tools that
compute an MDE.** Neither is the tool that gates preregs.

### `prereg_check.py`'s use of 1.96 is legitimate, with one caveat

`half_width()` computes a **95% confidence half-width** — 1.96 is the *correct* constant for
that. `BAR_RESOLVABLE` (line 759) then passes when `margin >= hw`, i.e. asks *"is the declared
decision threshold outside the noise?"* That is a resolvability question, not a power question,
and the tool never claims otherwise.

⚠ **The caveat: on the live corpus the check is near-tautological.** Where a prereg sets
`BAR = base + half_width` (the standard corefill band), `margin == hw` **by construction** and
the gate passes carrying zero information. Measured below: that is **7 of 15** computable cases,
all at ratio exactly 1.00.

✅ **Control, in the tool's favour:** the selftest DOES drive `BAR_RESOLVABLE` to both verdicts
(`prereg_check.py:1841` forced FAIL, `:1843` forced pass), and
`docs/research/CERT-prereg-check-forced-fail-2026-08-14.md:51,59` certifies it. The tool is
validated per house rules; the constant-column concern is about the live corpus only.

---

## 3. POPULATION — stated in full, because the denominator is the peer lane's trap

| | count |
|---|---|
| `docs/prereg/*.md` | 88 |
| `docs/research/PREREG-*.md` | 16 |
| `docs/PREREG-*.md` | 1 (minus overlap) |
| **TOTAL prereg-family files scanned** | **104** |
| declare a machine-readable `PLANNED n:` | **17** |
| declare `BAR:` | 30 |
| declare `BASE RATE:` | 17 |
| **`BAR_RESOLVABLE` fully computable (BAR + BASE RATE + PLANNED n)** | **15** |
| mention `2.802` or "80% power" | **18** |
| carry an OB16-form `MDE:` declaration | **7** |

**Method:** `tools/prereg_check.py` was run against all 104 (read-only). The 89 "not computed"
files lack one of the three tokens — most predate the token vocabulary, which was introduced
2026-08-14. **The per-leg power table below therefore describes 15 of 104 files.** It is not a
sample: it is *every* file whose bar is machine-checkable.

⭐ Against the peer lane's 2-of-8 keyword result: **13 of the 17 legs that declare a `PLANNED n`
also reason explicitly about 80% power.** Power reasoning in this repo is not rare — it is
concentrated in exactly the legs that size themselves.

---

## 4. THE PER-LEG TABLE — computed power at the registered bar

`ratio = margin / half-width`. `ratio = 1.00` ⇒ 50% power. `ratio ≥ 1.43` ⇒ ≥80%.

| prereg | gate | margin | hw | ratio | n | **power** | OB16 MDE? |
|---|---|---|---|---|---|---|---|
| `SCREEN-finishhp-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-gunaxabl-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-sealfloor6-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-seatscan-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-sentthreat-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-wirehold-2026-08-14` | ok | 1.3 | 1.3 | **1.00** | 5400 | **50.0%** | no |
| `SCREEN-v140vs146-2026-08-14` | ok | 3.1 | 3.1 | **1.00** | 1000 | **50.0%** | no |
| `SCREEN-bodyaware-2026-08-14` | ok | 1.9 | 0.9 | 2.11 | 10800 | 98.5% | **yes** |
| `SCREEN-beltsever-2026-08-15` | ok | 1.9 | 0.9 | 2.11 | 10800 | 98.5% | **yes** |
| `SCREEN-bodyblock-2026-08-15` | ok | 1.9 | 0.9 | 2.11 | 10800 | 98.5% | **yes** |
| `SCREEN-launchmax-2026-08-15` | ok | 3.3 | 1.3 | 2.54 | 5400 | 99.9% | **yes** |
| `LEG-juustopin-2026-08-14` | ok | 27.3 | 8.7 | 3.14 | 175 | 100% | no |
| `SCREEN-crashdrive-2026-08-14` | ok | 10.0 | 2.7 | 3.70 | 240 | 100% | no |
| `SCREEN-homeearly-2026-08-15` | ok | 3.6 | 0.9 | 4.00 | 10800 | 100% | **yes** |
| `LEG-fieldcal-2026-08-16` | ok | 40.0 | 3.5 | 11.43 | 1200 | 100% | no |

**15/15 pass the gate. 7 of the 15 sit at exactly 50% power.**

### ⭐ THE BOUNDARY IS A DATE, AND IT IS OB16

OBLIGATION 16 was written **2026-08-14T23:41:01Z**
(`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md:441`). Git first-commit
times (local +02:00):

| prereg | committed | vs OB16 (01:41+02) | ratio |
|---|---|---|---|
| `SCREEN-gunaxabl` | 2026-08-14T23:13:13 | **BEFORE** | 1.00 |
| `SCREEN-seatscan` | 2026-08-14T23:23:59 | **BEFORE** | 1.00 |
| `SCREEN-finishhp` | 2026-08-15T00:16:52 | **BEFORE** | 1.00 |
| `SCREEN-bodyaware` | 2026-08-15T01:54:35 | **AFTER** (13 min) | 2.11 |
| `SCREEN-beltsever` | 2026-08-15T07:41:47 | AFTER | 2.11 |
| `SCREEN-launchmax` | 2026-08-15T07:41:47 | AFTER | 2.54 |
| `SCREEN-bodyblock` | 2026-08-15T10:11:08 | AFTER | 2.11 |
| `SCREEN-homeearly` | 2026-08-16T06:50:02 | AFTER | 4.00 |

**Every computable prereg locked before OB16 sits at ratio 1.00. Every one locked after carries
an OB16 MDE and sits at ratio ≥ 2.11.** The boundary is clean, and `SCREEN-bodyaware` — OB16's
named first application, 13 minutes after it was written — is the hinge.

**This is the control driven the other way.** The method identifies both classes correctly and
has produced both verdicts on real files. It is not an instrument that can only say "underpowered".

---

## 5. ⭐ THE REPO DIAGNOSED THIS BEFORE I DID — OB16 and its corollary

The 7-at-ratio-1.00 result is not a discovery. It is written up, in general form, at
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md:527`:

> **OB16 COROLLARY, 2026-08-15T03:52:45Z — THE STANDARD COREFILL BAND HAS AN MDE OF ZERO BY
> CONSTRUCTION, AND THAT IS A PROPERTY OF EVERY SCREEN ON IT**
>
>     standard corefill band : 48.67 / 51.33 at n=5400
>     half-width at n=5400   : 1.334pp
>     => the band IS 50 +- half_width, so the implied MDE is 0.000pp
>
> *"Clearing 51.33 puts the CI's lower edge at exactly 50.00 — it just touches the null and
> excludes NO positive effect size. … every arm screened on the standard band is a POINT RULE.
> It licenses 'we can exclude 50' and NOTHING about a minimum effect. … it must not be quoted
> as having excluded an effect size, because it cannot."*

The fix, adopted at `:504`: **`BAR = null + MDE + half_width`** — *"MDE inside the bar rather
than beside it"*, so a bar cannot be quoted detached from its MDE.

### And the pre-OB16 screens knew they were underpowered — they SAID SO, pre-hoc

This is the part a keyword grep cannot see. The ratio-1.00 legs are not naive:

* `SCREEN-seatscan-2026-08-14.md:374` — a table row: **`80%-power MDE (one-sample vs 0.5,
  Z=2.802) | 1.91pp`**. Correct constant, stated in the prereg.
* `SCREEN-seatscan-2026-08-14.md:91` — *"THE SCREEN IS POWERED FOR THE TOP THIRD OF THE EFFECT
  RANGE THIS PLANK CAN PRODUCE AND FOR NOTHING BELOW IT; **UNRESOLVED is the MODAL outcome**."*
* `SCREEN-seatscan-2026-08-14.md:380` — *"⛔ THE POWER STATEMENT, WRITTEN BEFORE THE DATA."*
* `SCREEN-sealfloor6-2026-08-14.md:219` — same `Z=2.802` table row, `≈1.91pp`.
* `SCREEN-sentthreat-2026-08-14.md:372` — *"this prereg registers 'inside the band' as the
  [modal outcome]"*.
* `SCREEN-gunaxabl-2026-08-14.md:273-275` — *"an under-powered shard cannot deliver a 'could
  not separate' verdict, because that is what an under-powered shard [produces anyway]"* —
  the exact harm this audit hunts, pre-registered as a **prohibition**.
* `SCREEN-wirehold-2026-08-14.md:181-190` — a full n-vs-MDE table: *"80% power at 1.67pp needs
  6,887 games; at 0.5pp it needs 76,832. The 5,400-game screen is powered only for the fair-coin
  ceiling."* ⇒ **`PLANNED n: 5400 games — NOT AUTHORISED`** (`:260`). **A leg refused on power
  grounds before firing.** This is the strongest single piece of evidence against the systemic
  reading.

⇒ **The pre-OB16 defect was that the machine-readable `BAR:` field carried no MDE, so the bar
could be detached from the power statement sitting three sections away. It was NOT that nobody
computed power.**

---

## 6. ⚠ RESIDUAL 1 — "MDE" NOW NAMES TWO QUANTITIES THAT DIFFER BY ~2.3x

OB16 fixed the detachment problem. It also overloaded the acronym.

* **`mde.py` / `leg_read.py` sense:** *the smallest true effect detectable at 80% power.*
* **OB16 sense:** *the effect size we will call a MISS — the value the CI must exclude.*

These are different, and the OB16 bar does **not** deliver 80% power at its own registered MDE:

| screen | n | registered "MDE" | hw | bar | true effect for 80% power | **P(clear bar) if truth == registered MDE** |
|---|---|---|---|---|---|---|
| BODYAWARE | 10800 | +1.00pp | 0.93 | 51.93 | **+2.33pp** | **2.5%** |
| BODYBLOCK | 10800 | +1.00pp | 0.93 | 51.93 | **+2.33pp** | **2.5%** |
| BELTSEVER | 10800 | +1.00pp | 0.93 | 51.93 | **+2.33pp** | **2.5%** |
| LAUNCHMAX | 5400 | +2.00pp | 1.33 | 53.33 | **+3.90pp** | **2.5%** |
| HOMEEARLY | 10800 | +2.70pp | 0.93 | 53.63 | **+4.03pp** | **2.5%** |

**This is not an error in OB16.** Its stated guarantee — *"clearing this bar means the 95%
interval excludes BOTH 50.00 AND the MDE"* — is delivered exactly. The hazard is purely one of
reading: **a later reader who sees `MDE: +1.00pp` and assumes the screen is powered to find a
+1.00pp effect is wrong by a factor of 2.3.** The screens are powered for roughly **2.3× their
registered MDE**.

Under this repo's own rule that *a promoted claim carries its hedges or it carries a pointer*,
the OB16 form should name its parameter something that cannot be confused with the 80%-power
quantity two tools already compute — e.g. `EXCLUSION FLOOR` or `MISS THRESHOLD`.

---

## 7. ⛔ RESIDUAL 2 — OB16 IS NOT ENFORCED ANYWHERE

`tools/prereg_check.py` `KNOWN_KEYS` (lines 141-156) enumerates 30+ obligations —
`PLANNED n`, `BAR`, `BAR SOURCE`, `BASE RATE`, `REFERENCE n`, `GATE RESOLUTION`,
`SEGMENT VALUE CEILING`, `DOSE`, `METRIC WINDOW` … **and contains no `MDE` token.**
`grep -n "OB16\|OBLIGATION 16\|MDE" tools/prereg_check.py` returns nothing.

The tool's own docstring (lines 30-33) states the risk precisely:

> *"The measured half-life of a prose rule in this repo is about one session. The durable
> surfaces are booted files and tools that exit non-zero. This is the second kind."*

**Every obligation `prereg_check.py` enforces was written into prose first and then broken by
its own author** — that is the tool's stated reason for existing. OB16 is currently in the
prose stage. Its compliance record so far is 7 of 7 (all preregs written since it landed carry
the form), which is a two-day record, not a durable one.

**The cheapest durable fix — and this is a pricing, not a decision:** add `MDE` to `KNOWN_KEYS`
and one arithmetic check recomputing `BAR == BASE RATE + MDE + half_width`. It reuses
`half_width()` unchanged and is the same shape as the existing `SEGMENT_CEILING` product check.

---

## 8. THE DISCRIMINATING QUESTION — were any nulls reported as informative?

The programme-level rule is present and live:

* `CLAUDE.md` — *"A fail-to-exclude claim must first be RESTATED AS AN EXCLUSION … before the
  correction is applied. Applied to the unrestated form, DEFF launders a weak null into a
  confident one."*
* `PROGRAMME.md:474` — the `DEFENCE_ADMISSION_BAR` is scored *"as 'the CI excludes the
  registered rise', never as a bare fail-to-find"*, with each prereg registering *"its own
  n/MDE"*.
* `PROGRAMME.md:~505` — the RMST₃₀₀ bar: *"must not RISE vs control by more than its prereg's
  registered MDE, **scored as exclusion**."*

The rule is also actively applied in **28 documents under `docs/`, 11 of them dated 2026-08-16
alone**, each performing the restatement in writing before quoting an interval — e.g.
`RATED-LADDER-POWER-2026-08-16.md:153-155`, `RMST300-BOARD-RESCAN-2026-08-16.md:74`,
`FIELDCAL-POOLED-READ-2026-08-16.md:164`, `FORWARD-ARRIVAL-BASELINE-2026-08-16.md:342`,
`MAP-CONDITIONAL-CEILING-2026-08-16.md:425`.

`PROGRAMME.md:622` additionally forbids the exact failure this audit hunts:

> *"A leg reporting it as its primary repeats the 2026-08-10 failure exactly — an 18pp bar
> fired at a fixture whose own MDE floor was 19.5pp — with a better-looking number."*

### ⭐ THE ANSWER: the three 50%-power legs that actually completed were all reported UNRESOLVED

`results.tsv` (415 rows, chronological) carries a status vocabulary that already separates the
two cases: **`no-verdict` ×19**, `verdict` ×83, `discard` ×21, `refuted` ×7. Every row whose
confidence interval **contains 0.50** was extracted and read. Of the seven ratio-1.00 screens,
three reached full n, and all three are hedged correctly:

| row | leg | result | how it was reported |
|---|---|---|---|
| 378 | **SENTTHR** | 49.80%, n=5400, CI [48.47, 51.13] | *"INSIDE the 48.67-51.33 band = **UNRESOLVED**. Prereg rule :84: UNRESOLVED defaults to the RESTRICTION, arm NOT promoted"* ✅ |
| 379 | **GUNAXABL** | 48.69%, n=5400, CI [47.36, 50.02] | *"INSIDE band = **UNRESOLVED**, falsifier NOT met. ⚠⚠ MARGIN 0.02pp"* ✅ |
| — | **V140VS146** | 53.00%, n=1000, CI [49.9, 56.1] | *"inside band = **UNRESOLVED**. ⚠ MARGIN 0.10pp, knife-edge; **not a comfortable null**"* ✅ |

**None of the three claims "no effect". All three name the margin, and two flag their own
knife-edge.** `SCREEN-wirehold` never fired at all (`NOT AUTHORISED`). This is the direct answer
to the discriminating question, and it is the good outcome: **the underpowered designs did not
produce overconfident nulls.**

The most recent closure is also correctly restated — row 413, `ECOSIPC`, 2026-08-16T09:32:23Z,
49.28% at n=5400, status `refuted`: *"**CI upper bound EXCLUDES** the 51.33 futility bar."*
That is the exclusion form the rule demands, not a bare fail-to-find.

### ⚠ Two genuine outliers, both from the pre-prereg era

| row (of 415) | leg | n | CI | status | wording |
|---|---|---|---|---|---|
| **108** | QUEUE-1 strict variant `_v64cbB` | **32** | [33.6, 66.4] | `discard` | *"**REFUTED** as a fix — pooled 16/32"* |
| **171** | EIR 6 ablation `_v77e6` | **360** | [42.1, 52.4] | `refuted` | *"EIR 6 VERDICT: **REFUTED AS-BUILT**, all three pieces PARKED"* |

Both intervals straddle 0.50, so both are fail-to-exclude claims labelled as refutations —
**the harm this audit was sent to find.** Both sit at rows 108 and 171 of 415, at bot versions
`_v64` and `_v77` against a current head above `_v316`: they predate the prereg apparatus, OB16,
the exclusion-restatement rule and the `no-verdict` status entirely. **Neither is evidence about
current practice, and both are already superseded.** An n=32 screen with a 33pp-wide interval
calling anything "REFUTED" is the clearest single illustration of why the later machinery exists.

⛔ **AUTHOR'S CORRECTION, recorded rather than silently fixed.** A draft of this section flagged
row 415 (`ECOSCK6`, 2026-08-16, 50.33% at n=5400) as a borderline over-claim, on the strength of
its opening phrase *"DISCARDED as a NULL at full n"*. **That flag was wrong, and it was wrong
because I read a 230-character truncation of the field instead of the field.** The row continues:

> *"⛔ **NOT an exclusion-refutation** like ECOSIPH/ECOSIPC: the CI excludes NEITHER 50 NOR the
> 51.33 futility bar — **could-not-separate is the honest class** … As a 60-line candidate it is
> dead regardless of the interval (a candidate must MEASURE ≥60)."*

**It is a model entry, not a violation:** it names the honest class, refuses the refutation
reading explicitly, and quarantines the word "dead" to a *separate non-statistical* criterion.
This is the repo's own instrument rule turned on the auditor — a verdict quoted from a truncated
field is a verdict computed from something other than the data.

### ⚠ ONE LIVE VIOLATION, DATED TODAY — and it is an instance of Residual 1

A parallel sweep of `results.tsv` (415 rows), all 88 `docs/prereg/` files and all 332
`docs/research/` files (596 candidate phrases, each read in context) found the hedging discipline
holding almost everywhere. The one clean sentence-level breach is current, and it lands on a
**post-OB16** screen:

* `docs/research/MAP-CONDITIONAL-CEILING-2026-08-16.md:72` — *"the whole effect sits inside
  bodyaware's own ±0.93pp half-width at n=10,800. **The cheap idea is dead.**"*
* `:451` — *"**The bodyaware plank-off oracle is dead.** +0.24pp cross-validated (+0.33pp naive),
  inside its own ±0.93pp half-width."*
* `:453`, **two lines later** — *"**Seat-conditioning alone is a null.** +0.55pp, p = 0.3632."*
  ⇒ a *larger* effect, correctly hedged. **The same document hedges the bigger null and refutes
  the smaller one.**

An effect inside the half-width is a fail-to-exclude; under the standing rule it must be restated
as *"the interval excludes effects above ~+1.2pp"*, never as "dead". ⭐ **This is exactly the
hazard Residual 1 predicts:** BODYAWARE registered an **MDE of +1.00pp**, its bar excludes only
effects above that, and a downstream reader converted "did not clear the bar" into "the plank is
dead". The naming collision has now produced a real mis-statement, in a document written today.

### Two stale unhedged claims, already caught, not yet rewritten

* `docs/builder-method.md:24` — *"imprisonment (**refuted**)"*, no n, no hedge. Flagged by
  `docs/research/D12-closure-sweep-2026-08-10.md:68-69` **six days ago** (the enemy case was never
  tested); still live in a booted methods file.
* **Twelve `docs/research/tactics/*.md` files** assert *"THE FORWARD ROAD IS CLOSED"* or that
  turret production is settled, in body text. Each carries an appended
  `⚠ CAVEAT ADDED 2026-08-10 — DEMOTED, DO NOT REASON DOWNSTREAM AS SETTLED`, and
  `tactics/INDEX.md:255,1265` states the n=439 floor supports only *"does not reproduce"*.
  **The correction sits downstream of the claim instead of replacing it** — a reader hits the
  unhedged sentence first. Propagation lag, not a live analytic error.

**Where the rule is stated canonically:** `docs/coordination.md:23120` — *"**Cannot detect, not
no effect.**"* — restated at `:31393, :33148` (*"the honest sentence is 'inside the band, no
information'"*) and eight other points, plus
`docs/research/SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md:201,229` and
`docs/prereg/SCREEN-homeearly-2026-08-15.md:485`.

---

## 9. VERDICT

**Not systemic. Not ongoing. A closed defect plus a naming collision plus an unenforced fix.**

| question | answer |
|---|---|
| Is `1.96×SE` used as an MDE in code? | **No.** Both MDE tools use `Z=2.802`. `prereg_check.py`'s 1.96 is a CI half-width, correctly. |
| Were legs actually sized at 50% power? | **Yes — 7 of the 15 computable preregs, all locked before 2026-08-14T23:41Z.** |
| Did anyone intend it? | **No — and they knew.** Those same preregs quote the `Z=2.802` MDE and register UNRESOLVED as the modal outcome; one was refused authorisation on power grounds. |
| Was it caught? | **Yes, by this repo, on 2026-08-15T03:52:45Z, as the OB16 corollary.** This audit reproduces the boundary to the hour. |
| Is it fixed? | **In form, yes** — 7 preregs carry `BAR = null + MDE + hw`. **In enforcement, no.** |
| ⭐ **Was any null from an underpowered design reported as informative?** | **Not in the current era.** All three completed 50%-power legs (SENTTHR, GUNAXABL, V140VS146) reported `UNRESOLVED` and named their margin. **Two pre-apparatus rows (108, 171 of 415) did** — `_v64cbB` at n=32 and `_v77e6` at n=360, both intervals straddling 0.50, both labelled REFUTED. Superseded, not live. |
| Residual harm | The overloaded "MDE" label: post-OB16 screens are powered for **~2.3× their registered MDE**, and nothing in the document says so. **It has already produced one live mis-statement** (`MAP-CONDITIONAL-CEILING-2026-08-16.md:72,451`). |

### One line, if Magnus wants the convention written down

> **`MDE` in a prereg means the effect size the interval must EXCLUDE (OB16: `BAR = null + MDE +
> half_width`), never the smallest detectable effect — a screen is powered for roughly 2.3× its
> registered MDE, and any leg quoting detection power computes it at `Z = 2.802`, never `1.96`.**

**The decision is Magnus's; this document prices it.** The enforcement change (§7) is the
higher-value half and costs one `KNOWN_KEYS` entry plus one arithmetic check.

---

*Read-only audit. No bot, tool, prereg, `results.tsv`, `PROGRAMME.md` or `CLAUDE.md` was
modified. Population: 104 prereg-family files; power computed for the 15 with machine-checkable
bars; every count above carries its denominator.*
