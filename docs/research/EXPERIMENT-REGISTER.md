# EXPERIMENT REGISTER — every leg, how it was conducted, what it taught

**Standing mandate (Magnus, 2026-08-10):** *"We need to explicitly document all
our experiments and how they are conducted; we want to be able to improve our
experimentation methods and that's only possible through documenting what we are
doing."* Maintained by the side lane. **Append-only per experiment; entries are
never edited after their result lands — corrections go in a dated addendum line.**

Companion: `EXPERIMENT-METHOD-CHANGELOG.md` — the protocol itself, with every
rule traced to the incident that created it. **An entry here records which method
version was in force when the leg fired**, so a result can be re-weighed when a
method defect is found later.

## Entry schema

Every experiment records: **ID · date · prereg commit + author time (UTC) ·
platform createdAt of earliest leg · lock margin · treatment (exact diff) ·
comparator · fixture (opponents, maps, seats as realized) · bars (mechanism /
currency, as pre-registered) · result vs each bar · surprises (recorded before
explanation) · method faults found · anchors.** Missing fields are written
`UNKNOWN`, never inferred.

**THIS REGISTER IS THE CANONICAL SPINE (Magnus, 2026-08-10).** Every experiment's
full record is reachable from its entry. Each entry carries an **Artifacts:**
line linking its prereg / result / cert / match-ids / audit — so "everything
about experiment X" is ONE lookup, not a file hunt. The entry is the durable
record for EVERY experiment; the elaborate prose verdict lives in the linked
RESULT doc and is written ONLY for legs that produced a decision or a method
fault (proportionality rule, method changelog) — a null that answered nothing
needs its entry, not an essay. **Join on the bot dir (`_v1xx…`), never the LOKI
number** (the label is not unique). Corrections are dated addenda, never edits.

---

## 2026-08-10 (session s27) — the live-unrated era begins

### E-27.1 — UNPINNED LIVE BASELINE (v102, no treatment)
**Artifacts:** prereg `docs/prereg/PREREG-live-unrated-baseline-2026-08-10.md` · cert `docs/research/LOCK-CERT-live-unrated-baseline-2026-08-10.md` · read `docs/research/AUDIT-baseline-read-2026-08-10.md` · match-ids `docs/legs/LEG-MATCH-IDS-2026-08-10.md` (unpinned baseline section)
- **Prereg:** `5a5ca55`, author 03:58:40 UTC. **Legs:** created 03:58:55–57 UTC.
  **Lock margin: 15.4 s** — certified, but on argument (no creation-dependent
  surface; population-shrink ratchet) rather than margin. `LOCK-CERT-live-unrated-baseline-2026-08-10.md`.
- **Conducted:** 5 named opponents × 5 games, **maps NOT pinned** (platform chose;
  25 games spanned 13 maps). Registered 6 opponents/30 games; **delivered 5/25**
  (rate limit truncated Ouroboros — 5 legs per 10 min, learned by hitting it).
  Seats 3A/2B, platform-assigned.
- **Result:** 14–11 games (after my seat-flip erratum — first published as 7–18);
  0/25 r1000; 25/25 core-decided; our kill median 151, theirs 162.
- **Surprise (recorded pre-explanation):** Bisons 4–1 against us with kills at
  49–92 turns.
- **Method faults found:** thin lock margin against unmeasured clock skew;
  unpinned maps make it a field read, not a control; the 0/25-vs-7% comparison
  was reported as "populations differ" when P(0|7%)=0.163 — a NULL misread as
  positive (corrected `b0585b5`); my seat-flip (platform scoreA/B read without
  resolving seat).
- **Status: superseded as a control by E-27.2; stands as a field read.**

### E-27.2 — PINNED TESTBED CONTROL (v102, no treatment), windows 1+2
**Artifacts:** prereg `docs/prereg/PREREG-pinned-testbed-control-2026-08-10.md` · match-ids `docs/legs/LEG-MATCH-IDS-2026-08-10.md` (pinned control n=50) · panel-saturation analysis in `docs/coordination.md` (07:0x, e63a6f8)
- **Prereg:** `3c9400a`, author 04:07:13 UTC — **first self-certifying clock**
  (platform reading quoted in the commit; skew bound measured [−13.4 s, +1.9 s]).
  **Legs:** w1 04:15:22 (margin 489 s), w2 04:44–:45. **Certified on clocks alone.**
- **Conducted:** pinned panel (Bisons/I Stone/Leviathan/gsxWins/CAD) × pinned
  size-ordered maps (fjordgate/jackpot/atoll/saga/snowflake). 25 games = one
  rate-limit window. mapSeed uncontrolled (pre-declared). Seats platform-assigned:
  w1 AABBB, w2 BBBBB.
- **Result:** w1 11/25, w2 13/25 → pooled **control n=50: core_kill_share 21/50 =
  42.0%, r1000 6/50 = 12.0%**, our kill median 246.
- **What its own data later revealed (E-27.3):** 3 of 5 cells are inert constants
  (Bisons 0,0,0,0 · Leviathan 4,4,4,4 · CAD 4,3,4,4) — **a two-cell instrument in
  a five-cell denominator**, selected on rating proximity from era-mixed win
  rates (CAD 0.45 overall = 0.38 Eir / 0.66 v102).
- **Status: live control at n=50; panel replacement adopted, one calibration
  window required before any treatment touches the new panel.**

### E-27.3 — LOKI-11 "RUSH RE-OPEN" (`LOKI2_RUSH_ON = False → True`), windows 1+2
**Artifacts:** prereg `docs/prereg/PREREG-loki11-aimed-plant-2026-08-10.md` (rescoped pre-fire, 33f7e5e) · result `docs/research/RESULT-loki11-rush-reopen-2026-08-10.md` · match-ids `docs/legs/LEG-MATCH-IDS-2026-08-10.md` (LOKI-11 n=50)
- **Prereg:** originally the *facing-search* plank (`aba28f3`); **rescoped
  PRE-FIRE** (`33f7e5e`) when a 90-second paired local run showed the mechanism
  could not bind (both arms: 1 sentinel, same tile; treatment 20 rounds LATER) —
  falsifier branch 2 collected before rated exposure; facing plank parked as
  `_v129loki12`, unfired. Re-preregged `b0728b3`, author 04:24:02 UTC. **Legs:**
  w1 04:32:20 (margin 498 s, certified), w2 04:55:58–:56:01 (margin ~32 min).
- **Treatment:** ONE constant — the committed-opening window on (min_harv 2→0,
  Ti floor 40→8, 60 rounds). Only non-comment diff vs v102.
- **Bars as pre-registered:** mechanism A median first forward sentinel < r60;
  mechanism B ≥1.8 forward sentinels/game; currency core_kill_share vs E-27.2,
  paired by (opponent, map); pre-declared MDE 39pp at n=25/25.
- **Result:** **NULL, the word written.** Currency +16.0pp at n=25 → **+0.0pp at
  n=50 (21/50 vs 21/50)**, Fisher p=0.393. Mechanism decoded from the leg's own
  50 replays: first plant **r32 vs r43** (flag bound); forward sentinels/game
  **2.08 vs 3.44** — *earlier plant, FEWER sentinels: the flag buys tempo by
  spending the economy that funds later emplacements* (research's mechanism read).
  Real per-game deltas: harvesters 3.12 vs 5.44, conveyors 20.92 vs 38.20, own
  units lost 2.76 vs 4.52.
- **Bar autopsy (builder, `bd31bb7`):** both bars passed their literal thresholds
  **while both premises were false** — sized off ONE local match vs
  `_probe_victim`; the live control already planted at r43 and built 3.44/game.
- **Surprises:** window swing 52%→32% on identical treatment (5 games on n=25,
  larger than any claimed effect — empirical confirmation of the 39pp MDE);
  entire w1 aggregate was one cell (gsxWins 1→3→0); **true rated cost ZERO**
  (v103 played no ladder match — pairings ~10 min apart, window shorter).
- **Method faults found:** bars sized from a self-authored probe; the r45
  STANDING gate never measured (bar A = first plant, bar B = per-game count —
  neither is the gate); panel saturation (see E-27.2); elo-tape version column
  labels the SAMPLE not the MATCH (slot-rule windows misattributed across flips).
- **Status: NULL at n=50 on a two-cell instrument. Power buy or supersession —
  builder's call. LOKI-12 (facing) parked unfired.**

### E-27.4 — LOKI-13 "ECONOMY SUPPRESSION" (`PAVE_TRAIL_ON off`) — SUBMITTED, UNFIRED
**Artifacts:** prereg `docs/prereg/PREREG-loki13-economy-suppression-2026-08-10.md` (+ pre-leg amendment 6d734f7) · result `docs/research/RESULT-loki13-economy-suppression-2026-08-10.md` · match-ids `docs/legs/LEG-MATCH-IDS-2026-08-10.md` (LOKI-13) · cert + result + pooled-audit in the dated addenda below. **NOTE: authorized to SHIP by Magnus 2026-08-10 (see final addendum).**
- **Prereg:** `e9135e5`, author 06:51:12 +0200, **amended PRE-LEG** (`6d734f7`):
  mechanism-A bar re-derived from the flag's own paired-seed action (51→33,
  61→41, 75→32; bar ≤27 conveyors/game = 0.70× control) after the original ≤25
  was shown already cleared by LOKI-11 without the flag; **ammo + shots added**
  to mechanism B (the unmeasured link: conveyors→Ti→ammo→shots→kill).
- **Declared: a dose-and-mechanism probe, NOT a currency test** (panel cannot
  resolve currency; mechanism bars are per-game and saturation-immune).
- **Status: v104 submitted; five challenges failed in the 07:1x platform outage;
  waiting behind a field-presence gate (three consecutive reads with
  `active_submission` populated). v102 verified holder throughout. Lock margin
  will be certified when it fires.**

### Queued, with pre-work done
- **Ring-body denial** — the one reopened road whose own primary measures it
  positive on the currency (hazard 2.24%→4.77% at j=1, 539k builder-rounds);
  bars agreed: arrival = 2+ forward in-range sentinels **STANDING at r45**,
  conversion barred separately (field conversion spans 6× at the same gate; ours
  unmeasurable from the corpus — 4 of 2,508 team-sides).
- **Crash-induction (border throws)** — pre-stated audit criteria committed
  BEFORE its prereg (`PRESTATED-audit-criteria-crash-induction-2026-08-10.md`);
  design upgraded to research's **split-throw within-leg control** (half border /
  half interior; interior must read ~0 vs 0 events in 2,334,017 non-border
  rounds); carriers named in advance (`vjg` 96.1%, `S` 89.1%, `Ship Happens`
  87.4%, `Troupe` 84.9%), Cookie excluded (adversary-locked), four teams
  UNCLASSIFIED not immune. **Holds on Magnus's organiser question re norms.**

---

## Pre-s27 experiments — SUMMARY ROWS, backfill in progress

(An opus agent is reconstructing full entries from preregs, coordination and
result docs; these anchors are verified, details pending.)

| ID | experiment | outcome | anchor |
|---|---|---|---|
| E-26.x | LOKI-10 route-guard ARENA battery (480 games) | BAR NOT MET — bar was a coverage claim built on an occurrence measurement | `64efdde` |
| E-25.x | LOKI-9 facing reorder | proven-INAPPLICABLE null (engine permits ≤1 facing; resolved mathematically, third falsifier branch added pre-run) | s26 wrap |
| E-24.x | LOKI-QUIET no-attack arm | INVALID — treatment verified as coded, not as the experiment required (forward sentinel never gated) | obligation 11 |
| E-24.y | LOKI-3 kidnap plank | STOOD DOWN pre-battery — treatment-occurrence bar failed (throws 16.7% vs 30%) | addendum 4 |
| E-23.x | Ouroboros Legs A/B + 15:46 conversion prereg | prereg fully refuted; anti-correlated with its own outcome variable → obligation 7 | `ca3c3f8` |

---

*Register format itself is an instrument: if an entry cannot be filled from the
committed record, that is a documentation failure to fix at the NEXT experiment,
not retroactively invent.*

---

## DATED ADDENDA (append-only)

**2026-08-10 07:4x — input-registration for the queued ring-body leg (research
arm, via `91b21bc`):** the dose cut (r45 gate, 3.6%→23.1%, p=1.9e-12) enters that
leg's bar-sizing WITH its header constraints: *claim describes the FIELD; our own
conversion is unmeasurable from it by construction (4 of 2,508 team-sides); the
pooled effect is a mixture over a 6× spread; the powered placebo covers "gate is
spurious", not "gate means different things to different bots".*

**2026-08-10 07:4x — method fault in the fault-tracking apparatus itself
(research's adversarial pass, `ef97fcb`; adopted as v3.1, `c8bb019`):** the
changelog counted CREATING incidents as FIRINGS, so the improvement loop could
not run; the protocol's evidence for itself was ONE production firing (rule 7's
staleness branch). Filed here because a fault in the fault tracker is the
category most likely to go unrecorded — which is why this line exists.

**2026-08-10 08:0x — E-27.4 (LOKI-13) STATUS CORRECTION (addendum, not an edit):**
the entry above says "SUBMITTED, UNFIRED" — that was true at writing and is now
stale. **LOKI-13 FIRED 2026-08-10T05:40:41Z, rollback verified 05:41:00Z**
(builder's durable match-id record, `docs/legs/LEG-MATCH-IDS-2026-08-10.md`, the
five matchIds are banked there). It fired in a platform flap window behind the
field-presence gate; v102 re-verified as holder immediately after. **RESULT NOT
YET READABLE** — `match info` is flapping null through the ongoing outage.
**LOCK: prereg git author time 04:51:12 UTC (amended pre-leg 05:04:36 UTC) vs
fire 05:40:41Z = ~36 min margin against the amendment; two-clock CERTIFICATION
OWED pending a readable platform `createdAt`** (the second clock). Nothing lost —
the git clock is fixed and the fire time is in the durable record.

**2026-08-10 08:1x — E-27.4 (LOKI-13) RESULT + LOCK CERT (addendum):**
- **LOCK CERTIFIED.** Clock 1 (prereg git author): e9135e5 **04:51:12 UTC**,
  amendment 6d734f7 **05:04:36 UTC**. Fire (durable record, platform Z-stamp):
  **05:40:41Z**. **Margin ~36 min against the amendment** — ~150× the measured
  git/platform skew bound ([−13.4, +1.9]s), and the result postdates all of it,
  so the ordering holds under any clock. Unlike the baseline leg's 15.4 s, the
  per-match `createdAt` cannot change this verdict; it stays flapping-unreadable
  through the outage and is noted confirm-when-readable, immaterial to the lock.
- **CURRENCY: NULL, word written** (`c3ce6b2`). core_kill_share control 21/50 =
  42.0% vs LOKI-13 +18.0pp, Fisher p=0.152 — **under the pre-registered ~25–30pp
  resolution floor**, so a null by pre-registration, not a spun positive.
  r1000 direction favourable (n=5/cell, not claimed).
- **MECHANISM BARS: UNREAD** (conveyors/game ≤27; ammo + shots) — decode pending.
  Prereg pre-commits "MECHANISM A missed → THE LEG ANSWERED NOTHING", so **NO
  VERDICT until the bars are read.** The two-bar discipline held: the currency
  null is not read as "economy suppression fails" while the mechanism is unread.
- **D6 + D16: clean.** Autopsied against its own bar; NULL owned; the ammo link
  I flagged pre-leg is in Bar B; per-cell honesty ("n=5, seat A, not claimed").

**2026-08-10 08:3x — E-27.4 (LOKI-13) MECHANISM BARS READ, VERDICT FINAL (addendum):**
**BAR A NOT MET → THE LEG ANSWERED NOTHING about economy suppression, as
pre-committed** (`b3517cc`). Conveyors 33.32 vs bar ≤27 (ratio 0.86 — a **14%**
cut, not the 30% the bar required). The +18.0pp currency reading is therefore
**NOT attributable to the flag.** Two-bar discipline vindicated end-to-end: a
currency null on an unread mechanism would have been misread as "economy
suppression fails"; it was not.
- **NEW METHOD FAULT (D16, banked to the changelog): a bar derived from the
  flag's OWN paired-seed LOCAL action does not transfer to live.** Local cut
  ~35% (the bar's basis); live cut 14%. Cause: local games run long and
  uncontested so the pave trail dominates; live games are shorter/contested.
  **This defeated the exact fix that replaced LOKI-13's original ≤25 bar** — even
  "derive the bar from what the flag controls" is unsafe if the derivation is
  local.
- **MY FLAGGED AMMO LINK: MEASURED AND CLEARED.** Criterion 8 / the pre-leg worry
  ("conveyors→Ti→ammo→shots→kill, ammo the unmeasured self-defeat link") is
  REFUTED: conversion 1.10× under treatment, end balance 1.60×, shots 0.98×
  flat. **Ammo is NOT our kill constraint at this economy level.** This is why
  ammo was added to Bar B — so the worry could die on data. It did.
- **SURPRISE (channel): conveyors −14% but `titanium_collected` −38%** — a
  disproportionate economy hit for a small conveyor cut. Unattributed, recorded.

**2026-08-10 09:20 — E-27.4 (LOKI-13) SHIPPED (addendum):** **v104 "Loki v2" is
LIVE on the rated ladder (Magnus's call, `792cdb7`).** The ship record carries
the caveats intact: **ships on CURRENCY ALONE** (+18.0pp core_kill_share held
n=100/100), **honest significance ~0.05 family-wise not 0.016** (multiplicity +
asymmetric stopping), **mechanism bar FAILED** so the +18pp is NOT attributed to
economy suppression — we ship a currency effect whose cause is unknown. This is
the line's **first ship to the rated ladder** (prior ladder bot was v102 =
LOKI-8; the frozen Eir incumbent `_v115dodge` is a separate concept). A fresh
pre-registered PAVE_TRAIL_ON=False confirmatory leg at n=100 remains the clean
way to nail 0.016 vs ~0.05; LOKI-15 tests the mechanism, not this effect.

**2026-08-10 10:2x — E-27.5 (CONFIRM-PAVETRAIL) PRE-REGISTERED, D5 SATISFIED (new entry stub):**
The D5 flag on fanout's CONFIRM arm was actioned within minutes. **Artifacts:**
prereg `docs/prereg/PREREG-confirm-pavetrail-2026-08-10.md` (0f4dd41).
- **Two-clock: prereg committed 08:22:30Z; CONFIRM arm 0 windows fired** at
  audit, scheduled ~08:39Z → structurally pre-registered (~17 min margin);
  final margin to be confirmed against the first window's `createdAt` on fire.
- **THE SINGLE confirmatory test, declared in advance at fixed n=100** — this is
  what removes the pooled result's multiplicity/optional-stopping inflation
  (ship was ~0.05 family-wise; this is one pre-registered test).
- **Falsifiable prediction, pre-data:** v102 (`_v124loki8`, PAVE_TRAIL_ON=True,
  the arm) scores **~18pp WORSE** than v104 (`_v130loki13`, PAVE_TRAIL_ON=False,
  the live control) on `core_kill_share`. If the shipped effect is real the old
  bot must lose the panel. **This is the leg that turns the ship's ~0.05 into a
  clean pre-registered result — the confirmatory value the un-pre-registered
  version would have lost.** Result + final lock cert to follow on fire.

**2026-08-10 10:5x — E-27.6 (LOKI-16 ring-hold) PRE-REGISTERED, audited vs my 6 pre-stated criteria (2755aca):**
**Artifacts:** prereg `docs/prereg/PREREG-loki16-ring-hold-2026-08-10.md`.
PASSES the criteria — and its headline self-flag corrects MY six-roads
nomination:
- **The "one body on the enemy ring" road I called an untested reopened lever is
  ALREADY IMPLEMENTED by our incumbent.** The prereg: "both arms already exceed
  the prescription's ONE body." So the six-roads 2.24%→4.77% finding is not a new
  lever for us — our bot already places ring bodies. **My nomination was partly
  wrong: that road isn't untested, it's already pulled.** The correction is the
  builder's, honestly headlined ("THE PLANK IS NOT THE THING THE EVIDENCE
  MEASURED").
- **So LOKI-16 tests the MARGINAL lever instead: RETENTION** — refusing the
  walk-off from ring tiles the barrier path never covers, i.e. **trading a
  barrier for a held body.** Different mechanism from the observational evidence;
  correctly flagged as such.
- **Criteria met:** mechanism bar = ring-body COVERAGE (arrival), verdict =
  `core_kill_share` (conversion) — SEPARATED ✓; the hold is measured as
  **duration** (longest single-tile hold 0.809 vs 0.578), i.e. seat-rounds not
  throws ✓; **bar set BELOW the local delta because local probes die ~136 rounds
  and live games do not** — v3.2 local-to-live awareness, applied ✓; **pooled
  n=100, MDE ~14pp stated, "nothing under resolves"** ✓; **falsifier decomposes
  4 ways incl. "coverage bar missed → answered nothing"** (treatment-occurrence)
  ✓; mechanism is denial on the ENEMY ring → offensive ✓.
- **The trade it actually tests:** a body sits where `can_build_barrier` would
  have — so the currency question is whether a HELD BODY beats a BARRIER on that
  tile. Clean, and different from what I nominated. D5 lock cert on fire.

**2026-08-10 11:1x — E-27.7 (LOKI-14 crash-induction) PRE-REGISTERED, D5+D17 satisfied, audited vs my pre-stated criteria (3535000):**
**Artifacts:** prereg `docs/prereg/PREREG-loki14-crash-induction-2026-08-10.md`;
criteria `docs/research/PRESTATED-audit-criteria-crash-induction-2026-08-10.md`.
**The first APPROVED exploit leg. It passes ALL pre-stated criteria — the whole
point of committing them before the prereg existed:**
- **Split-throw placebo ✓** — half border / half interior; interior MUST read ~0
  (census 0 in 2,334,017 non-border rounds); removes the induced-vs-natural
  equivalence assumption by construction.
- **Named carriers ✓** — vjg 96.1%, S 89.1%, Ship Happens 87.4%, Troupe 84.9%;
  Cookie excluded (adversary-locked, p=5.2e-08); four unclassified, not called
  immune. Plus a geometry nuance it added: a border target needs the launcher
  ~5 tiles from an edge, so a large-map panel can return n=0 — folded into the
  treatment-occurrence bar.
- **Treatment-occurrence pre-battery ✓** — border-arm throws ≥20; missed →
  answered nothing (local: 20/19 over 16 matches).
- **The working instrument ✓** — primary = "enemy removed WITHOUT a damage event"
  via `crash_census.py`, validated against a POSITIVE control (`_probe_crash`, 20
  detections / 97 tracebacks) AND a NEGATIVE control (0), false-positive class
  stated. Not a replay-traceback scan (which is void — replays don't capture them).
- **Pooled n=100, engine-sourced (disassembly, two toolchains), deterministic
  (not `random.`), norms APPROVED (D17 approved class) ✓.**
- **Two-clock ✓** — prereg 09:17:20Z; LOKI-14 arm (fanout 5th, v107) not fired
  (no outfile) → structurally pre-registered. Final margin on first window.
- **NULL decomposes** incl. "mechanism bar missed → answered nothing."
This is the pre-stated-criteria discipline working end to end: criteria committed
before the artifact, prereg meets them, audit fitted to nothing. Result + lock
cert on fire.

**2026-08-10 14:2x — E-27.5 (CONFIRM-PAVETRAIL) RESULT + LOCK CERTIFIED: NOT CONFIRMED:**
- **LOCK CERTIFIED.** prereg 0f4dd41 committed 08:22:30Z; arm fired 20 windows
  from ~08:39Z (~17 min margin) — pre-registered, single test at fixed n=100, no
  early stop, no extension. Clean.
- **RESULT: NOT CONFIRMED (not refuted).** v104 control 81/150 = 54.0%, v102 arm
  47/100 = 47.0%, **delta −7.0pp, Fisher p=0.303, interval includes zero.**
  Prediction was −18pp. **The ship's +18pp DID NOT REPLICATE** — what reproduces
  is a −7pp shadow indistinguishable from zero. Cause is exactly the weaknesses
  flagged at ship time: +18 pooled-into-significance after a null, honest ~0.05
  family-wise, seat differences in 3/5 cells.
- **NOT REFUTED:** direction still favours v104 by 7pp; the leg cannot
  distinguish it from chance. "Not confirmed" ≠ "refuted."
- **THE TWO INSTRUMENTS DISAGREE, and it's controlled-weak vs field-strong:**
  the CONTROLLED panel (pre-registered, n=100) says +7pp unconfirmed — but it is
  the **2-cell saturated instrument (D13)**, our weakest. The UNCONTROLLED rated
  ladder says v104 **1690, rank #23, +47 over v102's peak (1643), 61 tape rows,
  sustained** — the field instrument the programme weighs as the verdict
  (benchmark-vs-field). Not a contradiction: a weak controlled test on a
  near-saturated panel vs a strong field signal. **The +18 magnitude is dead;
  v104's real edge is a modest field lead, not a panel effect.**

**2026-08-10 14:3x — E-27.5 DATA-INTEGRITY CAVEAT (fanout holder-assert bug, fixed 77385e0):**
A CONFIRM-v102 window failed to roll back; the next arm (CONTROL-v104, which
activates nothing and so checked nothing) fired **10 games (2 matches) into a
live v102**, silently entering a v104 pool. **OPEN for the builder: verify whether
those 10 are inside E-27.5's v104 control (81/150) or a later CONTROL/PANEL2 pool;
discard and recompute if so.** (Contamination discovered 12:39Z, 19 min after
CONFIRM banked 12:20Z — timing alone doesn't settle it; the builder knows which
windows.)
- **BUT THE VERDICT IS ROBUST, and the bias direction favours HOLD:** the 10
  contaminants are v102 (47%) sitting in the v104 control (54%), so they dragged
  the measured control DOWN — the measured **−7pp UNDERSTATES v104's true edge**.
  Correcting moves the delta MORE negative (toward the −18pp prediction), i.e.
  toward confirmation — but from −7pp to at most ~−9pp, nowhere near the bar. **So
  "NOT CONFIRMED" stands, and if anything v104's real edge is slightly larger
  than the CONFIRM showed** — mildly supporting the HOLD recommendation, not
  undercutting it. The fix (assert holder before EVERY challenge, incumbent arms
  included) is the mechanism behind the v102 tape-pollution flagged at 14:2x.

**2026-08-10 14:4x — E-27.5 CAVEAT RESOLVED, CLEAN (5e3287b):** verified independently:
contaminants created **12:32:08Z**; CONFIRM banked **12:20:32Z** — all 150 control
games completed ≥12 min BEFORE the contamination existed, so it could not be in
the CONFIRM control. **CONFIRM needs no recomputation; "NOT CONFIRMED" is fully
clean, not just robust.** The 10 games are removed from `arm_v104.txt` (control
restored to 30 clean matches) and durably quarantined
(`docs/legs/QUARANTINE-2026-08-10.md`, "do not re-ingest"). Found by auditing
every arm against the platform's own timestamps — the right instrument. My bias
analysis stands as the counterfactual (would have been ~−9pp if contaminated,
still short of the bar). **E-27.5 caveat closed.**

---

**2026-08-10 15:5x — E-27.6 (LOKI-16 ring-hold) RESULT: UNRESOLVED AT n. NOT ADVANCED, NOT KILLED.**
Verdict typed by the builder (`b1ca257`); read-outs `f13e375` + `b5266ee`; lock
cert two-clock clean (prereg 08:55:54Z vs leg 09:53:26Z, side lane `bcc17c5`).
* **Bar (>=+0.08 ring coverage) does not resolve.** game-mean +0.086 MEETS ·
  round-weighted +0.076 MISSES · equal-cell +0.084/+0.085 MEET — a spread of
  0.010 straddling the threshold. Match-clustered bootstrap **+0.086, 95% CI
  [-0.038, +0.196]**. **A number that changes verdict with the estimator is not
  a pass.**
* **Mechanism DOES move, and this is not banked as a consolation.** Episodes
  >=50 rounds **11.8% vs 5.6%** (median episode is 1 round in BOTH arms — a mean
  buries it entirely); on fjordgate the treatment holds **longer (+0.182) with
  FEWER body-rounds** (-0.216 seat-rounds/round), i.e. one pinned body replacing
  several transiting ones — the shape the plank claims. Predicted cost landed
  live: ring tiles holding our building **2.64 vs 3.65 (-1.011)**.
* **Currency arm is separately uninformative, now with a number.** Patched
  `tools/leg_read.py` reads this pair at **MDE 21.7pp on live cells (n=60/135)**
  against a currency delta of **+0.0pp**. The leg could not have resolved a
  currency claim either.
* **`jackpot` IS KEPT.** Dropping it would move +0.086 to +0.117 — **that is
  fitting the panel to the plank.** jackpot does not harm the treatment (flat,
  0.675 vs 0.672); the **CONTROL gains there (+0.159)** because a 5-tile corner
  ring hands the incumbent the same ~0.65-0.68 ceiling the plank works to reach.
  That is a real property of the plank, not a broken cell.
* **Bar swap REFUSED for this leg, PRE-REGISTERED for the next.**
  longest-hold/length is the better statistic (+0.182/+0.184/+0.264/+0.263 on the
  four 12-tile maps) and research recommends it; adopting it now would be
  choosing the estimator after seeing which one clears. **Named for LOKI-16b
  before 16b fires.**
* **NEXT STEP IS AN INSTRUMENT FIX, NOT A MAP DELETION.** "Fix the panel's map
  axis" means **add a map-admission check to PANEL2-CAL** (does the map admit the
  mechanism the plank is defined on?) — per D34. **It does NOT mean drop
  jackpot**; see above. Recorded this way because the two sentences could
  otherwise be read against each other.

**2026-08-10 15:5x — E-27.7 (LOKI-14 border-throw crash induction) RESULT: FALSIFIER 1 FIRES. NOT ADVANCED.**
Verdict typed by the builder (`b1ca257`); lock cert two-clock clean (prereg
09:17:20Z vs leg 10:04:12Z).
* **Primary: 0 undamaged enemy builder removals of 150 border throws**, bar was
  **>=45**. **Placebo clean: interior 0/164.** Mechanism bar met **7.5x** (314
  kidnaps decoded).
* **SCOPE, pre-committed by the prereg and binding on me: this is refuted
  AGAINST THESE FIVE PANEL TEAMS AT A DELIVERED DOSE OF 150 BORDER THROWS.** It
  is **not** a refutation of border-throw crash induction and **not** a challenge
  to the class ruling. The census is bimodal — 4 named carriers vs 6 teams with
  722,545 border builder-rounds and 0 events — and **no carrier is on our panel**.
  Against field-average the zero is surprising (P(0|lambda~3.4) ~ 3.5%); against
  these five it is unremarkable.
* **Under-dosing is ruled out and I am not permitted to reach for it:** the
  prereg's own big-map escape did not apply — every map produced border throws
  (saga 71, snowflake 12), launcher edge-margin <=4 for 278/314.
* **NEXT: a carrier-targeted leg** (vjg 96.1%, S, Ship Happens, Troupe) — the
  only test that separates "our panel is immune" from "it does not fire live."
  **Queued, not fired:** PANEL2-CAL owns the rate-limit budget.
* **Free findings banked:** enemy launchers threw OUR builders onto borders
  **54 times, 0 undamaged removals** (our `eco.py` guard holds live); and
  **Leviathan gave 0 kidnaps in 15 games**, inert on a second mechanically
  independent axis beyond D22's 4,4,4,4.
* **Instrument consequence, D35:** the prereg's stated method (decode the arm
  from our own `print()` stream) **was not executable** — platform replays strip
  stdout, 30,664/30,664. `CLAUDE.md` corrected.

---

**2026-08-10 18:0x — PANEL-3 (reachable-band calibration) RESULT: PANEL PRODUCED, 4 OF 6 ADMITTED — WITH A MAP CONFOUND THAT THREATENS IT.**
Prereg `PREREG-panel3-reachable-band-2026-08-10.md` (`90875ef`, before first
challenge). **37 challenges / 185 games, v104 live incumbent, ZERO rated
exposure, zero activations.** All cells reached the pre-registered n>=25.

| cell | gap | core_kill_share | verdict |
|---|---:|---:|---|
| Lunds Stallions | -30 | 21/30 = **70.0%** | **ADMITTED** |
| Askar City | +18 | 16/30 = **53.3%** | **ADMITTED** |
| farming_200s | +35 | 10/35 = **28.6%** | **ADMITTED** |
| Powered by SmartFridge | +5 | 8/30 = **26.7%** | **ADMITTED** |
| 0033 | +111 | 6/35 = 17.1% | **FLOOR** |
| The Bisons | +41 | 2/25 = **8.0%** | **FLOOR** |

**Effective n 125/185 = 68%.** Four admitted clears the prereg's floor of three,
so **the panel is produced.** Falsifier 1 did NOT fire (not all six landed in
band), so the reachability axis was real.

**THE BISONS RE-DERIVATION, PRE-COMMITTED TWO WAYS: <0.20 => D22 STANDS.**
8.0% at the full n=25. The morning's floor verdict was **not** a small-sample
artefact. **But see the confound below before treating that as settled** — D22's
verdict and this one rest on the same unrated fixture.

**⛔ THE FINDING THAT OUTRANKS THE CALIBRATION: THE PINNED MAP SET MAY BE THE
CONFOUND.** Same bot (v104), same opponent, opposite results:
* **unrated, our 5 pinned maps: 2/25 (8%)** — they core us in 23 of 25
* **ladder, ourver=104: 5/10 (50%)**

Per map vs The Bisons: **atoll 0/5 · fjordgate 0/5 · saga 0/5 · snowflake 0/5 ·
jackpot 2/5.** **We lose every game on four of the five pinned maps and win only
on jackpot**, while the ladder rotates all 15.
**Two readings, not yet separated:** (a) the pinned set is unrepresentative, so
the panel measures MAPS rather than opponents; (b) the ladder sample is 10 games
and wide. **We fixed the panel's OPPONENT axis today and its MAP axis is now the
suspect one — the same defect shape, one column over.**

**AND THE PANEL IS STILL A LARGE IMPROVEMENT.** Against the OLD panel we killed
**54-74%** on 4 of 5 cells; against the neighbours the ladder actually pairs us
with, **0033 cores us in 83% of games and The Bisons in 92%.** The old fixture
was populated with teams we beat, which is why two separate 18pp claims died on
it: we were measuring improvements against opponents that could not show one.

**ARTEFACT PRODUCED (the point of the leg):** admitted set =
`Lunds Stallions, Askar City, farming_200s, Powered by SmartFridge` — pass to
`leg_read.py --live-cells` on every subsequent leg, so no leg derives its own
live-cell denominator from its own outcomes.
**NEXT: resolve the map confound before this panel is used for a verdict.**
