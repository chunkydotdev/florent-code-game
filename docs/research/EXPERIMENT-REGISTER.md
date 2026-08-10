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

---

## 2026-08-10 (session s27) — the live-unrated era begins

### E-27.1 — UNPINNED LIVE BASELINE (v102, no treatment)
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
