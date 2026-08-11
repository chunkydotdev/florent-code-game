# Are we being scouted? Opponent version-bump hazard after we play them

Side lane, read-only. Written 2026-08-11T06:26:07Z (`date -u`, same shell).
Repo at `888d699`. **No verdict is issued here** — this lane reports what the
numbers show and what they cannot separate.

---

## 1. The question, and why it is not cosmetic

Magnus, 2026-08-11: *"We have been known to be scouted now and then."*

If opposing teams observe our play and ship in response, then the collinearity
between our version timeline and theirs is a **causal effect running from our
activity to their releases**, not the coincidental confound that drift rule D18
("pin the opponent's version at analysis time") currently treats it as. D18's
control assumes the two timelines are independent. If they are not, the control
is unsound — you cannot adjust away a variable that sits on the causal path.

**Operationalised:** does a team's version-bump hazard rise in the T hours after
we play them, relative to that same team's own baseline cadence, and relative to
what our activity clock alone would produce?

---

## 2. Surfaces, population, clock

| | |
|---|---|
| **Bump-detection surface** | `corpus/league_matches.tsv` — 35,642 **ladder** matches, league-wide, 72 distinct teams. Newest row `2026-08-11T05:52:59.649Z` (33 min before writing). |
| **Treatment surface A (ladder)** | our 729 ladder matches vs **55** teams. These rows **are** in the detection surface. |
| **Treatment surface B (unrated)** | our 726 unrated matches vs **45** teams, pulled live via `fcode match list --mine --type unrated --json` (8 pages, gated on the presence of the `matches` key, never on `$?`). **Verified: 0 of 726 appear in `league_matches.tsv`.** |
| **Analysis window** | `2026-08-06T00:00:00Z` .. `2026-08-11T05:52:59Z` = 125.88 h. Start set by our unrated record, which begins `2026-08-06T07:52:38Z`. |
| **Our teamId** | `379a5d80-9921-4c9e-949b-f9b1dcba16be` (OpenSverige). |

`corpus/ladder_games.tsv` was used only to **cross-check** the population: its 729
distinct match ids are exactly the 729 OpenSverige rows in `league_matches.tsv`,
symmetric difference 0. No win-rate denominator is taken from `meta_join`.

**Population of every number below: the 71 non-OpenSverige teams appearing on the
league-wide ladder surface in that window.** Numbers derived from our own match
list are marked **us-only** inline.

---

## 3. Method

### 3.1 Bump definition

**Definition A (primary).** For a teamId, walk its version observations in time
order. A **bump** is an observation whose version is *strictly greater than the
running maximum* for that team. The first observation only initialises the
maximum and is never a bump.

**Definition B (robustness).** A bump is the first appearance of *any* version
not previously seen for that team — this also catches rollbacks and re-issues.

**Concurrent versions are handled by construction.** "Powered by SmartFridge"
(`7fd91e77-812c-44da-bce7-457be94d2548`) fielded v55/v57/v58/v67 inside 4.5 h;
running-max-strict-exceed counts that as bumps at the *first* sighting of each
new high and ignores the later low-version stragglers, rather than counting four
independent events or oscillating. **Every headline below was recomputed under
definition B and moved by less than 0.04 in risk ratio** (§5, last row) — the
answer does not turn on the definition.

### 3.2 The trial, and the observation-density confound it exists to kill

The naive design (bumps per hour) has a fatal flaw: **a bump is only observed when
somebody plays that team.** Our own matches against a team *are* observations of
that team. Playing them therefore mechanically raises the chance a bump is
*detected* soon after, with no scouting whatsoever.

So the unit of analysis is a **trial = one third-party observation of team X**,
i.e. a ladder match involving X and **not** us. Our own matches are removed from
X's observation stream entirely — they are never trials and never update the
running maximum. The outcome is binary: does this trial reveal a bump?

This makes the treatment fully exogenous to the trial sequence. **44,450 trials,
1,029 bumps, base rate 0.02315 (def A), across 71 teams.**

### 3.3 Treatment, baseline, and the two controls

- **Treatment(T)** — we played team X in the interval `(t − T, t]`. Reported at
  **T = 2, 6, 12 h**, all three, fixed before the analysis was run.
- **Baseline** — each team's unconditional bump rate, given per team both per
  trial and per hour (`bump/h` column, §5).
- **Stratified estimate** — Mantel-Haenszel risk ratio pooled **within team**,
  so no between-team difference in development tempo can produce it. The crude
  pooled ratio is reported alongside and is always the larger of the two.
- **Negative control 1 — pair swap.** Team X is given the our-match times of a
  **different** team Y, then MH-pooled exactly as the real estimate. This is the
  brief's requirement (*does X's hazard rise after we play Y?*) and it holds our
  activity's real clustering fixed while destroying its target.
- **Negative control 2 — permutation.** Our entire match timeline is circularly
  shifted by a random offset, preserving both within-session clustering and the
  per-team allocation of matches. **1,000 draws.** Two nulls:
  - **free shift** — any offset;
  - **day-preserving shift** — offset constrained to near-whole multiples of 24 h,
    which preserves *time of day* and therefore tests the effect against the
    hypothesis "our legs and the league's deploys simply share an evening".
- **Event study** — bump rate in 6 h bins from −24 h to +24 h around each
  **leg-initiating** match (first match vs X after ≥12 h, and ≥24 h, of no
  contact with X). This is the design that separates *response* from *common
  cause*: a response can only produce a step at t = 0; a shared driver produces a
  hump straddling it.

### 3.4 The instrument was run against cases where it must come out the other way

Required before any of the above is trusted.

| check | expected | measured |
|---|---|---|
| **Synthetic positive** — inject a response into 15% of treated trials | must fire | **MH-RR 6.53**, day-shift p = 0.0033 |
| **Synthetic positive** — inject into 30% | must fire harder | **MH-RR 11.76**, p = 0.0033 |
| **Synthetic negative** — shuffle bump labels within team, 50 draws | must sit at 1 | **mean 1.000, sd 0.072**, range 0.853–1.159 |
| **Permutation null** (free shift, 1,000 draws) | must sit at 1 | **mean 1.007, sd 0.182** (unrated, T=6) |

The instrument produces both verdicts on demand. It is not a constant column.

---

## 4. Result

### 4.1 Headline, by treatment arm (def A; MH = team-stratified)

**LADDER arm** — opponent chosen by matchmaking, not by us:

| T | treated | untreated | crude RR | **MH-RR** | z | p (free shift) | p (day-preserving) |
|---|---|---|---|---|---|---|---|
| 2 h | 132/6,423 = 0.02055 | 897/38,027 = 0.02359 | 0.871 | **0.729** | −2.98 | 0.980 | 0.948 |
| 6 h | 243/10,538 = 0.02306 | 786/33,912 = 0.02318 | 0.995 | **0.890** | −1.27 | 0.802 | 0.667 |
| 12 h | 308/13,754 = 0.02239 | 721/30,696 = 0.02349 | 0.953 | **0.893** | −1.24 | 0.810 | 0.791 |

**UNRATED arm** — opponent chosen by us; these matches are absent from the
detection surface, so the density confound cannot operate at all:

| T | treated | untreated | crude RR | **MH-RR** | z | p (free shift) | p (day-preserving) |
|---|---|---|---|---|---|---|---|
| 2 h | 115/2,777 = 0.04141 | 914/41,673 = 0.02193 | 1.888 | **1.466** | +3.81 | 0.012 | **0.085** |
| 6 h | 224/5,615 = 0.03989 | 805/38,835 = 0.02073 | 1.925 | **1.460** | +4.72 | 0.034 | **0.137** |
| 12 h | 321/8,626 = 0.03721 | 708/35,824 = 0.01976 | 1.883 | **1.428** | +4.68 | 0.060 | **0.250** |

**The single headline number: MH-RR 1.46 at T = 6 h, on 224 bumps in 5,615
treated and 805 in 38,835 untreated third-party ladder observations of the 45
teams we played unrated, 2026-08-06 → 2026-08-11.** Everything in §4.2 is about
why that number does not survive its controls.

### 4.2 The controls

**Negative control 1 — pair swap, team-stratified, 25 draws each.** Team X given
team Y's our-match times:

| arm | T=2 h | T=6 h | T=12 h |
|---|---|---|---|
| **UNRATED placebo** | 1.162 ± 0.170 | **1.263 ± 0.175** | 1.085 ± 0.143 |
| observed | 1.466 (+1.79 sd) | 1.460 (**+1.13 sd**) | 1.428 (+2.40 sd) |
| **LADDER placebo** | 1.039 ± 0.150 | 1.027 ± 0.147 | 1.014 ± 0.147 |
| observed | 0.729 | 0.890 | 0.893 |

**The unrated placebo is itself elevated — 1.26 at T = 6 h.** Handing a team
somebody else's treatment times reproduces roughly half the observed excess on
the ratio scale. The observed value sits 1.1 sd above its own placebo at the
headline T. The ladder placebo sits at 1.0, as it should.

**Negative control 2 — the two permutation nulls disagree, and the disagreement
is informative.** Free-shift null mean 1.007 → p = 0.034. Day-preserving null
mean **1.178** → p = 0.137. Constraining the shift to preserve time of day moves
the null 18% of the way to the observed value. **A large share of the raw
association is our unrated legs and the league's deploy activity occupying the
same hours of the day.**

**Event study — the elevation precedes the treatment.** Leg-initiating unrated
matches only, MH-stratified, each bin against that team's own all-window rate:

| bin | ≥12 h gap (90 events, 45 teams) | ≥24 h gap (66 events, 45 teams) |
|---|---|---|
| [−24,−18] h | 1.202 (z +1.48) | 1.068 (z +0.39) |
| [−18,−12] h | 0.957 (z −0.35) | 0.591 (z −2.74) |
| [−12, −6] h | 0.754 (z −2.20) | 0.628 (z −2.78) |
| **[ −6, 0] h** | **1.331 (z +2.85)** | **1.471 (z +3.48)** |
| **[ 0, +6] h** | **1.459 (z +3.82)** | **1.177 (z +1.32)** |
| [ +6,+12] h | 1.061 (z +0.52) | 0.937 (z −0.47) |
| [+12,+18] h | 0.885 (z −0.99) | 0.830 (z −1.26) |
| [+18,+24] h | 1.026 (z +0.21) | 0.928 (z −0.51) |

**This is the load-bearing table.** At the ≥24 h cut, the bump hazard in the six
hours **before** we open an unrated leg (1.471) is **higher** than in the six
hours after (1.177). At the ≥12 h cut the two are comparable (1.331 vs 1.459).
A bump detected before our match cannot have been caused by our match, and bump
*detection lags actual deployment* (a deploy is only seen at the team's next
third-party match), which pushes the causing event **further** before our leg,
not closer. **The shape is a hump centred near t = 0, not a step at t = 0.**

**Does our targeting react to their releases?** Tested directly, and **no**:
comparing our real match times to 2,000 random times drawn in the same window
for the same team, the probability that team X had bumped in the preceding L
hours when we opened a leg was —

| L | unrated real | unrated random-time | ratio | ladder real | ladder random | ratio |
|---|---|---|---|---|---|---|
| 6 h | 295/726 = 0.4063 | 0.4197 | **0.968** | 235/729 = 0.3224 | 0.3198 | 1.008 |
| 12 h | 422/726 = 0.5813 | 0.5853 | **0.993** | 359/729 = 0.4925 | 0.4669 | 1.055 |
| 24 h | 540/726 = 0.7438 | 0.7423 | **1.002** | 467/729 = 0.6406 | 0.5993 | 1.069 |

(us-only, n = 726 unrated / 729 ladder matches). **We do not preferentially open
legs against teams that just shipped.** So the pre-window elevation is *not*
explained by us chasing fresh releases — which leaves the common driver
unidentified. That is a gap, not a resolution.

### 4.3 Robustness

- **Definition B** (any previously-unseen version): 44,450 trials, 1,057 bumps,
  base rate 0.02378. Unrated MH-RR **1.428 / 1.438 / 1.421** at T = 2/6/12 vs
  1.466 / 1.460 / 1.428 under def A. Ladder MH-RR **0.728 / 0.877 / 0.891** vs
  0.729 / 0.890 / 0.893. **No conclusion changes.**
- **Leave-one-team-out**, unrated arm T = 6 h: full 1.460, range **1.347**
  (dropping Jython) to **1.571** (dropping team lazy). Not carried by one team.
- **Burst stratification** (drop trials within *c* hours of that team's own last
  observed bump), unrated T = 6 h: c = 6 h → MH-RR 1.293 (z +1.35, 36/2,735
  treated); c = 12 h → 1.497 (z +1.61, 19/1,756); c = 24 h → 0.605 (z −0.82,
  **4/1,095 treated — 4 events, uninformative**). The c = 24 h cell is reported
  for completeness and carries no weight.
- **Ladder-arm power.** Injecting a true RR of 1.46 into the ladder arm recovers
  a measured MH-RR of 1.267, against a free-shift null of 1.029 ± 0.184 — about
  +1.3 sd. **The ladder null mildly disfavours an effect of unrated size; it does
  not exclude one.** Do not read the ladder row as a clean zero.

---

## 5. Per-team table (repo obligation 8 — no pooled delta without the rows)

Treatment = **our unrated matches**, bump def A, third-party ladder trials,
2026-08-06T00:00Z → 2026-08-11T05:52:59Z. `ourN` is us-only (count of our
unrated matches vs that team). `bump/h` is that team's unconditional baseline
over the 125.88 h window. Cells are `bumps/trials`.

| team | ourN | trials | bumps | bump/h | T2 trt | T2 unt | RR | T6 trt | T6 unt | RR | T12 trt | T12 unt | RR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Powered by SmartFridge | 76 | 692 | 11 | 0.0874 | 2/231 | 9/461 | 0.44 | 5/361 | 6/331 | 0.76 | 5/449 | 6/243 | 0.45 |
| Pivot | 74 | 703 | 53 | 0.4210 | 18/146 | 35/557 | 1.96 | 27/267 | 26/436 | 1.70 | 29/342 | 24/361 | 1.28 |
| CtrlAltDefeat | 66 | 674 | 26 | 0.2065 | 9/179 | 17/495 | 1.46 | 12/311 | 14/363 | 1.00 | 14/468 | 12/206 | 0.51 |
| gsxWins | 55 | 682 | 8 | 0.0636 | 2/145 | 6/537 | 1.23 | 5/246 | 3/436 | 2.95 | 5/358 | 3/324 | 1.51 |
| I Stone | 50 | 674 | 17 | 0.1350 | 6/103 | 11/571 | 3.02 | 10/161 | 7/513 | 4.55 | 12/237 | 5/437 | 4.43 |
| The Bisons | 39 | 685 | 3 | 0.0238 | 0/65 | 3/620 | 0.00 | 0/80 | 3/605 | 0.00 | 0/98 | 3/587 | 0.00 |
| Lunds Stallions | 37 | 658 | 23 | 0.1827 | 5/114 | 18/544 | 1.33 | 6/174 | 17/484 | 0.98 | 11/241 | 12/417 | 1.59 |
| Leviathan | 34 | 664 | 47 | 0.3734 | 1/55 | 46/609 | 0.24 | 5/65 | 42/599 | 1.10 | 8/83 | 39/581 | 1.44 |
| farming_200s | 28 | 682 | 8 | 0.0636 | 1/51 | 7/631 | 1.77 | 1/75 | 7/607 | 1.16 | 1/111 | 7/571 | 0.73 |
| Ouroboros | 25 | 672 | 0 | 0.0000 | 0/128 | 0/544 | — | 0/223 | 0/449 | — | 0/300 | 0/372 | — |
| Powerpuff Girls | 22 | 659 | 36 | 0.2860 | 7/113 | 29/546 | 1.17 | 16/258 | 20/401 | 1.24 | 27/376 | 9/283 | 2.26 |
| Landers | 21 | 690 | 12 | 0.0953 | 2/102 | 10/588 | 1.15 | 4/199 | 8/491 | 1.23 | 5/314 | 7/376 | 0.86 |
| Team 48 | 19 | 667 | 1 | 0.0079 | 0/75 | 1/592 | 0.00 | 0/136 | 1/531 | 0.00 | 0/209 | 1/458 | 0.00 |
| The Flotte Experience | 17 | 703 | 27 | 0.2145 | 7/109 | 20/594 | 1.91 | 13/258 | 14/445 | 1.60 | 21/407 | 6/296 | 2.55 |
| kladde chatte tville (…) | 17 | 695 | 32 | 0.2542 | 5/72 | 27/623 | 1.60 | 9/153 | 23/542 | 1.39 | 18/248 | 14/447 | 2.32 |
| sporks | 14 | 703 | 9 | 0.0715 | 2/136 | 7/567 | 1.19 | 4/283 | 5/420 | 1.19 | 6/380 | 3/323 | 1.70 |
| Askar City | 14 | 668 | 28 | 0.2224 | 9/39 | 19/629 | 7.64 | 11/73 | 17/595 | 5.27 | 11/109 | 17/559 | 3.32 |
| Banminary | 12 | 683 | 21 | 0.1668 | 3/53 | 18/630 | 1.98 | 6/113 | 15/570 | 2.02 | 10/203 | 11/480 | 2.15 |
| 0033 | 11 | 686 | 8 | 0.0636 | 1/47 | 7/639 | 1.94 | 2/121 | 6/565 | 1.56 | 3/209 | 5/477 | 1.37 |
| Pantheon | 9 | 703 | 34 | 0.2701 | 0/95 | 34/608 | 0.00 | 3/204 | 31/499 | 0.24 | 14/312 | 20/391 | 0.88 |
| Orizon | 9 | 689 | 0 | 0.0000 | 0/43 | 0/646 | — | 0/112 | 0/577 | — | 0/216 | 0/473 | — |
| Lorem Ipsum | 7 | 703 | 14 | 0.1112 | 1/73 | 13/630 | 0.66 | 4/192 | 10/511 | 1.06 | 10/313 | 4/390 | 3.12 |
| Jython | 7 | 703 | 54 | 0.4290 | 9/62 | 45/641 | 2.07 | 27/160 | 27/543 | 3.39 | 33/268 | 21/435 | 2.55 |
| OopsGotYourElo | 7 | 674 | 10 | 0.0794 | 0/46 | 10/628 | 0.00 | 0/89 | 10/585 | 0.00 | 0/143 | 10/531 | 0.00 |
| Coreflood | 6 | 697 | 24 | 0.1907 | 7/51 | 17/646 | 5.22 | 8/99 | 16/598 | 3.02 | 8/171 | 16/526 | 1.54 |
| Kings College Munich | 6 | 471 | 10 | 0.0794 | 2/46 | 8/425 | 2.31 | 4/128 | 6/343 | 1.79 | 4/182 | 6/289 | 1.06 |
| not adgato | 5 | 703 | 10 | 0.0794 | 0/60 | 10/643 | 0.00 | 4/161 | 6/542 | 2.24 | 7/269 | 3/434 | 3.76 |
| team lazy | 5 | 703 | 51 | 0.4051 | 0/49 | 51/654 | 0.00 | 1/118 | 50/585 | 0.10 | 3/190 | 48/513 | 0.17 |
| Besvikomat | 4 | 695 | 17 | 0.1350 | 1/48 | 16/647 | 0.84 | 4/126 | 13/569 | 1.39 | 5/183 | 12/512 | 1.17 |
| opensverige - plan B | 4 | 322 | 15 | 0.1192 | 7/40 | 8/282 | 6.17 | 8/120 | 7/202 | 1.92 | 12/216 | 3/106 | 1.96 |
| Big O | 3 | 409 | 6 | 0.0477 | 1/14 | 5/395 | 5.64 | 1/38 | 5/371 | 1.95 | 1/74 | 5/335 | 0.91 |
| Torsko | 3 | 425 | 36 | 0.2860 | 3/31 | 33/394 | 1.16 | 12/79 | 24/346 | 2.19 | 19/119 | 17/306 | 2.87 |
| S | 2 | 695 | 0 | 0.0000 | 0/7 | 0/688 | — | 0/19 | 0/676 | — | 0/37 | 0/658 | — |
| vjg | 2 | 648 | 0 | 0.0000 | 0/7 | 0/641 | — | 0/19 | 0/629 | — | 0/37 | 0/611 | — |
| Jacobs Code | 2 | 697 | 18 | 0.1430 | 1/23 | 17/674 | 1.72 | 2/70 | 16/627 | 1.12 | 3/125 | 15/572 | 0.92 |
| Albert And Einstein | 2 | 696 | 4 | 0.0318 | 0/23 | 4/673 | 0.00 | 0/49 | 4/647 | 0.00 | 0/85 | 4/611 | 0.00 |
| Troupe | 2 | 687 | 0 | 0.0000 | 0/7 | 0/680 | — | 0/19 | 0/668 | — | 0/37 | 0/650 | — |
| LingLing40 | 2 | 367 | 22 | 0.1748 | 3/14 | 19/353 | 3.98 | 6/38 | 16/329 | 3.25 | 6/74 | 16/293 | 1.48 |
| Ship Happens | 2 | 339 | 0 | 0.0000 | 0/7 | 0/332 | — | 0/19 | 0/320 | — | 0/37 | 0/302 | — |
| Erebus | 1 | 703 | 38 | 0.3019 | 0/12 | 38/691 | 0.00 | 3/36 | 35/667 | 1.59 | 4/72 | 34/631 | 1.03 |
| HTTP 418 | 1 | 703 | 21 | 0.1668 | 0/12 | 21/691 | 0.00 | 0/36 | 21/667 | 0.00 | 0/72 | 21/631 | 0.00 |
| Memtrace | 1 | 679 | 23 | 0.1827 | 0/11 | 23/668 | 0.00 | 1/33 | 22/646 | 0.89 | 5/69 | 18/610 | 2.46 |
| arsonist duck | 1 | 681 | 10 | 0.0794 | 0/11 | 10/670 | 0.00 | 0/35 | 10/646 | 0.00 | 1/71 | 9/610 | 0.95 |
| Focalground | 1 | 358 | 9 | 0.0715 | 0/11 | 9/347 | 0.00 | 0/24 | 9/334 | 0.00 | 0/41 | 9/317 | 0.00 |
| StarTrekker | 1 | 697 | 0 | 0.0000 | 0/11 | 0/686 | — | 0/35 | 0/662 | — | 0/71 | 0/626 | — |
| **POOLED (45 teams)** | **726** | **28,787** | **796** | — | **115/2,777** | **681/26,010** | **1.58** | **224/5,615** | **572/23,172** | **1.62** | **321/8,626** | **475/20,161** | **1.58** |
| **MH (team-stratified)** | | | | | | | **1.466** | | | **1.460** | | | **1.428** |

Read the rows, not the pool. **Nine of the 45 teams have zero bumps in the entire
window** and contribute nothing but denominator. The direction is genuinely mixed
among the teams we played most: SmartFridge 0.76, CtrlAltDefeat 1.00, The Bisons
0.00, team lazy 0.10, Pantheon 0.24 sit at or below 1, while Askar City 5.27,
I Stone 4.55, Jython 3.39, Coreflood 3.02 carry the top end. The pooled figure is
a weighted average over cells that are not comparable to one another.

The 55-team ladder-arm per-team table was produced identically and is summarised
by its pooled and MH rows in §4.1; it contains no team with a treated-cell RR
that survives its own N (the largest, Viktor5776 at 42.18, rests on 1/11 vs
1/464 and 1 of our matches).

---

## 6. What the numbers show

1. **In the arm where we choose the opponent (unrated), a team's ladder-observed
   bump hazard is about 1.46x higher in the hours after we play them than
   otherwise**, team-stratified, 224 vs 805 bumps, robust to bump definition and
   to leaving any single team out.
2. **That association does not survive its own controls.** Its team-stratified
   pair-swap placebo already reaches 1.26; its day-preserving permutation null
   reaches 1.18 and returns p = 0.137 at the headline T; and the **event study
   puts as much or more of the elevation in the six hours *before* the leg as
   after it** (1.471 vs 1.177 at the ≥24 h cut). An effect that appears before
   its cause is not that cause's effect.
3. **In the arm where matchmaking chooses the opponent (ladder), there is no
   elevation at all** — MH-RR 0.73/0.89/0.89, all permutation p above 0.66 —
   though that arm is only powered to about +1.3 sd against an effect of unrated
   size, so it disfavours rather than excludes.
4. **The obvious mechanism for a spurious hump is not present:** we do not
   preferentially open legs against teams that just shipped (ratio 0.97–1.00 vs
   random times). **The common driver behind the pre-window elevation is
   therefore unidentified**, and naming it would be manufacturing a finding.

**These data cannot separate "opponents ship in response to our unrated legs"
from "our unrated legs and opponents' deploys share an unmeasured driver."** The
temporal ordering argues against the first as the dominant channel; it does not
eliminate a smaller response component sitting on top of a shared driver.

**Bearing on D18:** on this surface, nothing supports upgrading our-timeline /
their-timeline collinearity from confound to causal path. D18's control is not
shown to be unsound. Equally, the ladder arm — which is the arm D18 actually
operates on — shows a *flat* profile, so D18's assumption is unstressed there.
This is not a licence to relax the rule: pinning the opponent's version remains
required for the reason it was written (their v-change and ours are collinear and
fit the data identically), independent of *why* they are collinear.

---

## 7. LIMITS

1. **Direction of initiation is unobservable.** `fcode match list --mine` includes
   matches opponents started against us; the platform records `triggeredBy` as
   the match *type* and leaves `sourceMatchAId`/`sourceMatchBId` null. **No claim
   here distinguishes "we challenged them" from "they challenged us".** For the
   unrated arm this matters directly — an opponent-initiated unrated match
   against us is plausibly *already* a scouting act, which would invert the
   arrow on an unknown share of the 726.
2. **Bumps are observed, not deployed.** A version change is seen at that team's
   next third-party ladder match. Detection lag is short for busy teams (the
   median team plays ~5.5 ladder matches/hour) and long for quiet ones, so
   low-activity teams have systematically blurred event times.
3. **Our unrated matches are a leading observation channel that the detection
   surface does not have.** 33 of 726 (4.55%) of our unrated matches fielded an
   opponent version higher than anything yet seen for that team on the ladder
   surface. Excluding them from detection is what makes the design clean, and it
   costs a small amount of timing precision in exactly the post-treatment window.
4. **The window is 5.2 days.** It contains only ~5 whole-day offsets, which
   limits how finely the day-preserving null can be resolved; its 1,000 draws are
   jittered ±1.5 h around whole-day multiples, not independent days.
5. **Trials within a team are not independent** and the MH z-statistics assume
   more independence than exists. The permutation p-values do not — they preserve
   the clustering — and they are the ones quoted in the headline. Where the two
   disagree, the permutation is the honest number: **z = +4.72 against
   p = 0.137 at T = 6 h is that disagreement, and it is large.**
6. **`ladder_games.tsv.oppver` was not used** and could not have been: it is null
   for large stretches, and a null column reads as "no version change" to any cut
   that trusts it. The opponent timeline here comes from `league_matches.tsv`
   only, per the standing corpus rule.
7. **Unrated pools our prototypes; ladder pools our shipped bot.** The two arms
   are never pooled in this document. They differ in what we fielded as well as
   in who chose the opponent, so the ladder/unrated contrast is not a clean
   experiment on opponent choice alone.
8. **Third-party ladder coverage is the top-72 ladder teams.** Teams outside that
   set have no trials and are absent from the population entirely.
9. **Nine of 45 unrated-arm teams recorded zero bumps in the window**, and the
   `RR` for those cells is undefined rather than 1. They are in the denominators
   and out of the ratios.

---

## 8. Reproduction

Scripts were written to the session scratchpad, not to `tools/` (side lane,
read-only). To rebuild: derive the observation stream from
`corpus/league_matches.tsv` per §3.1–3.2, pull the unrated list with
`fcode match list --mine --type unrated --json --limit 100` paged on
`next_cursor` and gated on the presence of the `matches` key, then apply the
estimators in §3.3 and the instrument checks in §3.4. **If any future run of
this instrument reports a synthetic-positive MH-RR near 1 or a label-shuffle
null away from 1, the run is broken and its output is not evidence.**
