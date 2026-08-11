# ⭐ QUEUE FOR THE BUILDER — FORWARD EFFICIENCY: WE PAY 4.57× AS MANY BUILDERS PER FORWARD BUILD

> # ⛔⛔ HEADLINE CORRECTION, s31 — **THE 2.28× DWELL FIGURE IS A SAMPLING ARTEFACT. THE POPULATION VALUE IS 1.30×, AND CORRECTING IT INVERTS THIS DOCUMENT'S CENTRAL RECOMMENDATION.**
>
> **Instrument B was run on the FULL population (US 5,178 games, TOP 3,165) instead
> of 120 games/group.** Result: **US 44.12 rounds per forward build vs TOP 33.98 —
> `1.30×`, not `2.28×`.** Over 2,000 draws of 120 games/group,
> **`P(sampled ratio ≥ 2.28×) = 0.0005`.** The US half reproduces on exactly one cut
> (game-1-of-match, 53.82 ≈ the published 54.55); **the TOP half reproduces on none —
> TOP is flat at 33.7–34.2 across all five game indices, so 23.93 is unreachable.**
>
> **AND THE CORRECTED VALUE CLOSES AN IDENTITY THE PUBLISHED ONE BROKE**, which is
> why it should be believed rather than merely preferred. This document's own
> `deaths/build = deaths/round × rounds/build`:
> ```
>   published 2.28 x 3.44 = 7.85  vs Instrument A's 4.57   ERROR +72%
>   measured  1.30 x 3.44 = 4.47  vs Instrument A's 4.57   ERROR  -2%
> ```
> **The defect was visible here all along:** §"THE HEADLINE" asserts *"~2.0× is
> PER-ROUND HAZARD"* — which is only `4.57/2.28` back-solved — **while the same
> paragraph quotes `2.915 vs 0.847 = 3.44×` as separately measured.** Those never
> matched, and in log shares the two halves summed to **135%**, which is not a
> decomposition. Corrected, they sum to **99%**.
>
> ## ⇒ THE RECOMMENDATION INVERTS
> | | as published | **measured** |
> |---|---:|---:|
> | dwell share of the gap | 54% | **17%** |
> | per-round hazard share | 81% | **81%** |
>
> **This document said *"the dwell half is the larger lever and it is the one nothing
> has been aimed at"*. DWELL IS THE SMALLER LEVER BY ~5×.** The hazard/geometry half
> — **deprioritised below on a 34% tile-selection ceiling** — is **81% of the gap**,
> and a 34% ceiling on 81% beats a free hand on 17%.
>
> **WHERE THE RESIDUAL DWELL EXCESS SITS, and it contradicts the constant list below:**
> excess is **early** (r0–99 1.38–1.45×; r100–179 1.24–1.39×), **parity at r180–250**,
> and **INVERTS after — we are 0.80–0.86×, BETTER than the top group, from r250 to
> r999.** Both band schemes agree; the waiting-time framing narrows it to r0–59;
> censored-mass gap +19.5pp at r0–59, ~0 by r250. **On the live v104 alone (n=1,750)
> peak excess is r60–179 at 1.73×, gone after r250.**
> ⇒ **`LAUNCH_GIVEUP_RND = 180` is NOT implicated.** *(INFERENCE — a round-band
> profile was measured; no constant was varied.)*
>
> **⭐ AND THE TEAM-SWAP CONTROL SUPPLIES THE ANCHOR THIS PLANK NEVER HAD: against
> the field we ACTUALLY PLAY, we are the better side — 44.12 vs our opponents'
> 62.65.** The 4.57× is against a ≥1900 group we rarely meet.
>
> **UNPREDICTED, REPORTED WITHOUT EXPLANATION:** US dwell falls systematically by
> game index within a match (**53.8 → 33.0**, game 1 → game 5) while **TOP is flat to
> ±0.5**. ⇒ **any cut of ours that is not index-balanced is biased**, cause unknown.
> Separately, our games are far longer in the tail: **14.2% reach r999 vs TOP's 5.8%.**
>
> **Method:** side keyed on `teamAId`/`teamBId`, not `us_side` (corpus-howto TRAP 7);
> seat validated against the replay-internal winner byte, **8,343/8,343 = 100.0000%**.
> All four controls ran. The band-shuffle as commissioned was a **no-op** and was
> reported as such rather than silently substituted; the form testing the intent
> flattens spread 3.78×→1.56× (US), 6.04×→2.24× (TOP). Empty bands print `UNDEFINED`;
> a real zero still prints `0.00`.
> **Script `scratchpad/dwell_band_s31.py`; tables `scratchpad/_dwell_band_full.txt`.**

**Research arm, s30, 2026-08-11. Two independent instruments, both reported.
Population: our 5,143 games vs 3,080 THIRD-PARTY games of nine ≥1900 teams
(sporks, Clankers, Jython, Lorem Ipsum, not adgato, Erebus, The Flotte
Experience, Pantheon, O(1)) — games we are not in, so not an echo loop.**

## THE HEADLINE

**Instrument A — `corpus/events.tsv`, one table, same method both sides:**

| | games | forward deaths/game | forward builds/game | **DEATHS PER FORWARD BUILD** |
|---|---:|---:|---:|---:|
| **US** | 5,143 | **1.79** | **13.91** | **0.1290** |
| **TOP (3rd-party)** | 3,080 | 0.67 | 23.59 | **0.0282** |
| ratio | | 2.69× | 0.59× | **4.57×** |

**Instrument B — direct replay decode, 120 games per group, positions per round:**

| | fwd builder-rounds/game | fwd builds/game | **ROUNDS PER FORWARD BUILD** | fwd share of builder-rounds |
|---|---:|---:|---:|---:|
| **US** | **742.7** | 13.62 | **54.55** | 36.4% |
| **TOP** | 494.9 | 20.68 | **23.93** | 27.2% |
| ratio | 1.50× | 0.66× | **2.28×** | |

**⇒ WE SPEND 50% MORE TIME IN THE ENEMY HALF, PRODUCE 41% FEWER FORWARD BUILDS,
AND LOSE 4.57× AS MANY BUILDERS PER FORWARD BUILD.**

The two instruments agree and **decompose the gap cleanly**, since
`deaths per build = deaths per round × rounds per build`:

* **⛔ ~2.28× is DWELL — RETRACTED s31. The population value is 1.30×** (see the
  correction banner at the top). At 2.28× the decomposition does not close.
* **⛔ "~2.0× is PER-ROUND HAZARD" WAS NEVER MEASURED — it is `4.57/2.28`
  back-solved**, and it sits in the same sentence as the figure that WAS measured,
  **2.915 vs 0.847 = 3.44×**. The two never matched and the mismatch went unflagged.

**⇒ CORRECTED: dwell 1.30×, hazard 3.44×, and 1.30 × 3.44 = 4.47 ≈ 4.57. In log
shares that is dwell 17% / hazard 81%, summing to 99%. As published the shares
summed to 135%, which is not a decomposition.**

**~~Roughly half the problem is loitering and half is where we loiter.~~ THE
PROBLEM IS OVERWHELMINGLY WHERE WE LOITER, NOT HOW LONG.**

## WHY THIS IS THE RIGHT TARGET AND LOKI-25 WAS NOT

`FORWARD-HAZARD-geometry-2026-08-11.md` measured the ceiling on the routing
half: our builders stand on gunner-covered tiles **2.04% of forward builder-rounds
against a 1.34% map baseline — 1.53× chance**, so **perfect tile selection cuts
exposure by at most 34%.**

**The dwell half is 2.28× and has no such ceiling.** It is the larger lever and it
is the one nothing has been aimed at.

## ⛔ POWER AUDIT — AMENDED 2026-08-11, AFTER THE BAR BELOW FAILED ITS OWN CHECK

**The bar specified below said "deaths per forward build, a RATIO" and did NOT
name the aggregation. Measured, 4,831 of our games:**

| estimator | value | MDE at n=64/arm |
|---|---:|---:|
| **mean of per-game ratios** (what I originally implied) | 0.1541, sd 0.4007, **CV 2.60** | **129% of level** |
| **pooled ratio** (total deaths ÷ total builds), game-resampled bootstrap | 0.1281, **SE 0.0330 AT n=64/arm** | **102% of level** |

**⚠ THE `n` ON THAT SE WAS MISSING UNTIL s31 AND ONLY ARITHMETIC PINNED IT.** As
first published the SE was printed bare, in a row whose other column says
`n=64`; a reader could as easily have taken it for the SE at the full 4,831
games, which would make the ~440 below wrong by a factor of 75. It is the SE at
**n=64/arm**, and it is forced twice over: `2.8 × √2 × 0.0330 = 0.1307 = 102%`
of the 0.1281 level, reproducing the same row's MDE; and `64 × (0.0330/0.0126)²
= 439`, reproducing the n below. **Self-caught, s31. A standard error without
its n is not a standard error.**

**Both are useless at n=64. The one I implied is the worse of the two.** This is
the defect this repo logged when four defensible estimators straddled the
ring-hold threshold inside 0.010 — **a bar names its estimator or it can be met
and missed by choosing one afterwards.**

**The obvious rescue does not work either.** Self-play looks like a free paired
design (same map, same seed, both arms in one game). **Measured within-game
correlation between the two sides' deaths-per-forward-build: r = +0.027 —
variance reduction 3%.** Reported because it is the design I would otherwise have
prescribed.

### ⇒ THE FIX: POOLED RATIO, GAME-RESAMPLED BOOTSTRAP, **n ≈ 440 PER ARM**

Detecting a move that closes **half** the top-tier gap (a 39% reduction) needs
SE ≈ 0.0126 → **~440 games/arm, 880 total.** **A 4,096-game self-play screen has
already been run today, so 880 costs zero unrated windows.** The protected floor
rides along in the same run.

**⚠ THE VARIANCE INPUT COMES FROM A DIFFERENT POPULATION THAN THE SCREEN WILL
RUN IN, and the reader should carry that.** SE 0.0330 was measured on **4,831 of
our LADDER games, against a heterogeneous field**; the screen runs in
**SELF-PLAY against one fixed opponent**. Removing opponent heterogeneity should
*lower* per-game variance, which would make ~440/arm **conservative rather than
optimistic** — *(INFERENCE: the direction is reasoned, not measured.)* **It
cannot be measured from anything we have, because no local battery has retained
replays to measure it from** — see the retraction below. ⇒ **If the screen's
battery retains replays, read the empirical per-game sd of the pooled ratio off
it before trusting 440.**

**⚠ And one correction to a rule in circulation:** *"mechanism bars are ~160×
cheaper"* is true of LOKI-25 (huge effect, low-variance statistic) and **NOT of
this plank** — here the mechanism bar needs 880 games and the win rate at 880
detects 4.7pp. **Comparable, not 160× apart. The principle is right; the multiple
is a property of that plank.**

## ⛔ THE BAR MUST BE A RATIO, AND THIS IS THE DESIGN CONTRIBUTION

**LOKI-25 died because it moved a numerator and a denominator together**: deaths
−24%, forward presence −23%, deaths per forward build −2.3%. **Any plank in this
family can buy its metric by simply going forward less.**

⇒ **PRIMARY BAR: `deaths per forward build`, a RATIO.**
⇒ **PROTECTED DENOMINATOR: `forward builds/game` must NOT fall** — pre-register a
floor (our current 13.91) and treat a breach as the falsifier, exactly as LOKI-25's
5d was written and then fired.

### ⛔ AMENDED s31 — **THAT FLOOR WAS A DIRECTION WITH NO THRESHOLD, WHICH IS THE SAME DEFECT AS "INSERT → RISES"**

Raised by the side lane as an obligation and independently forced when the
builder's own tool failed a selftest cell. **Measured, 5,178 archived games:
`forward builds/game` mean 13.94, sd 24.31, CV 1.74.**

**An unsized `db < 0` gate fires on ~half of all null pairs** — bootstrap, two
arms drawn from the SAME distribution, 4,000 reps: **50.5% at n=64, 48.5% at
n=440.** Sized to `db < −2·SE(diff)`: **2.2% / 2.5%.**

| n/arm | SE(arm) | SE(diff) | **2·SE(diff)** | as % of level |
|---:|---:|---:|---:|---:|
| 64 | 3.039 | 4.297 | 8.595 | 61.6% |
| 256 | 1.519 | 2.149 | 4.297 | 30.8% |
| **440** | **1.159** | **1.639** | **3.278** | **23.5%** |
| 880 | 0.819 | 1.159 | 2.318 | 16.6% |
| 2048 | 0.537 | 0.760 | 1.519 | 10.9% |

⇒ **At n=440 the breach threshold is `db < −3.28`, i.e. the treatment must fall
below 10.66 builds/game — not below 13.94.**

### ⛔⛔ AND THE GATE CANNOT CATCH THE FAILURE IT WAS BUILT FOR AT THE n THIS DOC PRESCRIBES

**`2·SE(diff)` is 23.5% of level at n=440**, so a `PASS` there means *"no fall
≥23.5% detected"*, **not** *"the denominator held"*. **That is D61 in a second
instrument: the gate has an informative band, and inside it a non-breach is no
information.**

**LOKI-25 — the plank this guard exists because of — died with forward presence
−23%.** A 23% fall is `0.23 × 13.94 = 3.21`; the threshold is `3.278`;
**3.21 < 3.278, so the gate does NOT fire.** It misses LOKI-25's own magnitude by
a hair and anything smaller outright.

**To catch a 23% fall at 80% power: ~700 games/arm one-sided, ~900 two-sided.**

⇒ **THE TWO HALVES OF THIS BAR HAVE DIFFERENT SAMPLE REQUIREMENTS AND THE
ORIGINAL DID NOT NOTICE. The ratio resolves at ~440; its protected denominator
needs ~700–900.** Sizing on the numerator alone buys a bar whose guard is
decorative. Options, in preference order if the run is not yet committed:
**(1) run at ~700–900/arm** so both halves resolve · **(2) run at 440 and
pre-register the gate's own MDE (23.5%)**, reporting `PASS-DENOM` as *"no fall
≥23.5% detected"* · **(3) find a lower-variance denominator** — CV 1.74 is the
driver.

### ⚠ AND A PRIOR OBJECTION TO THE DENOMINATOR ITSELF, from tactics sweep 23

**"Rounds per forward structure" charges every spawn-denial round to a build that
was never the point.** We hold a body on the enemy 12-tile ring in ~59–64% of
rounds — **state-valued forward work with no build attached**, which this metric
scores as waste. Where the field found longer dwell correct, the forward work was
state-valued rather than event-valued. ⇒ **The 2.28× is not yet established as a
defect**, and the three-way state split (action available and unused / no legal
action / errand complete) is now wanted ahead of the band split.

**⛔ RETRACTED BY ITS AUTHOR, 2026-08-11 s31, BEFORE THE SCREEN WAS RUN. The
sentence here read: *"Both quantities are already in `events.tsv`, so the
read-out needs no new decoder and the builder's 64-game self-play harness can
compute both."* IT IS WRONG. `events.tsv` is built from PLATFORM replays and
says nothing about what a LOCAL battery can emit.**

Verified by reading, file and line:
* **`tools/arena.py:53` runs every match with `--replay /dev/null`** — so
  `arena.py` produces **win rate and `score.py` only, and zero forward
  quantities.**
* **⚠ CORRECTION TO THIS RETRACTION, same day, raised by the side lane and
  verified by me: `h2h.sh` is NOT downstream of `arena.py`.** It contains no
  reference to it (two comment lines only) and calls `$FC run` **directly** at
  `:66-67` with **no `--replay` flag**, so its replays go to the `fcode.toml`
  default `replay = "replay.replay26"` — **one path, overwritten every game**
  (confirmed: exactly one `.replay26` at repo root). **The conclusion is
  unchanged — nothing forward is readable from today's output — but the hole on
  the h2h side is a ONE-LINE FLAG, not a missing architecture, and my original
  wording overstated it.** The `mech_battery.py` decode findings below are
  untouched by this correction.
* **`tools/mech_battery.py` DOES retain replays** (it exists for exactly this
  reason; `:6-7` states *"no local battery this project has ever run produced a
  decodable replay"*) — **but its decoder reads only builder-bot deaths by round
  band and builder-bot spawns.** No core-position read, no
  `d2_enemy < d2_own` test, and **no position tracking**: it sets `team_of[e.id]`
  on first sight and never updates from move events. `removeEntity` carries an
  **id only**, so **even a DEATH cannot be classified as forward** without adding
  that pass. It computes neither the numerator nor the denominator.
* Its `BANDS` are `r0_99 / r100_249 / r250_499 / r500p` — **not** the doctrine
  edges used by the band cut.

**THE PARTS EXIST AND ARE DEBUGGED — this is assembly, not research.**
`scratchpad/dwell.py::walk()` already reads both cores out of the map buffer
(`field 4` → `(team, pos)`), tracks positions through `unum==2` move events, and
applies the forward test to builder-rounds and to non-`builder_bot` placements.
`tools/loki17_mech.py` already drives `fcode run --replay` directly for this
reason (`:34-35`) and carries the traps `loki9_facing.py` paid for — including
that **a `rotate()` re-emits `placeEntity` for an existing id, so only the FIRST
is a build**, which will silently inflate a forward-build denominator written
fresh.

**Why the retraction is recorded here rather than only relayed:** this file is
the builder's brief for an ~880-game run, and a wrong sentence about
instrumentation in a brief is spent compute. Caught by going to look, not by the
run failing at its read-out.

## WHERE TO LOOK IN THE TREE — NAMED, NOT PRESCRIBED

The dwell constants a raider is governed by: `raid.py:232-234`
(`raid_pause_until = rnd + 60`; **both `3` and `60` are bare literals with no
doctrine constant** — found by the a–f library agent), `ESCORT_STALL_RNDS = 25`
(`doctrine.py:158`), `LAUNCH_STALL_RNDS = 36` (`doctrine.py:108`),
`LAUNCH_GIVEUP_RND = 180` (`doctrine.py:103`).

**I am naming the constants and NOT the intervention.** I do not know whether the
fix is a shorter pause, an earlier rotate-out, or acting-then-leaving — and
guessing the intervention is the error I made twice today on healer eviction.

## PRECONDITION: MEASURED, AND THE DOSE IS THE WHOLE BEHAVIOUR

742.7 forward builder-rounds per game across 5,143 games. **There is no
"does the treatment ever fire" risk** — this is what our raiders do all game.

## ⚠ WHAT THIS IS NOT

* **Not a causal claim.** Top teams may produce forward builds faster *because*
  they are better, not the reverse. **Cross-sectional, behavioural premise ⇒ under
  D12 this PRIORITISES a road and does not retire or confirm one.**
* **The TOP group is nine teams**, chosen by rating ≥1900 before the cut was run.
* **"Forward build" counts every non-builder-bot build with `d2_enemy < d2_own`**,
  so it mixes turrets with conveyors — the same definitional caveat LOKI-25's
  read-out carried.
* Instrument B samples one game per match; Instrument A uses all games.
