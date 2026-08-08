# v75 "Eir 8" production read — rev-5 pre-registered check set (2026-08-08)

**Research-arm deliverable. Measurement and attribution only — no games run, no
downloads, no bot files touched.** Executes the rev-5 pre-registration verbatim
(coordination board, 09:41 note), minus the diagnostic-print check, which was
dropped pre-execution as unmeasurable in platform replays.

> ## VERDICT
>
> **Did the expected-Elo bet pay where it claimed? MECHANISM YES, ELO HALF —
> and the headline it is being scored against is wrong by one match.**
>
> **1. The mechanism landed exactly where the case said it would.** The ship
> case was "fix the bleed on picket and CAD-family by putting bodies on heal
> seats". Bodies-on-seats per core-damage round, versus the same measurement on
> the predecessor v74's window: **picket 2.161 → 3.309 (+53%)**, **CAD-family
> 1.721 → 3.323 (+93%)** — the two largest gains in the corpus, in exactly the
> two classes named. Siege heal/damage ratio moved with them (picket median
> 0.810 → 0.917, CAD 0.470 → 0.809), and the survive-lobe clearance rate went
> picket 33.3% → 47.4%, CAD 21.4% → 37.0%. This is not a diffuse improvement
> that happened to cover the target: the target classes are where it is
> concentrated.
>
> **2. The Elo half-paid, and the two classes are still net-negative.** Bleed
> per match halved in both: **picket −12.67 → −5.22**, **CAD-family −13.37 →
> −7.16**. Game share more than doubled: **picket 13.3% → 35.0%**, **CAD 10.0%
> → 26.7%**. But both remain losses, and pooled over the two bleed classes the
> game-share gain (3/25 → 11/35) is **not significant at this n** (Fisher
> p = 0.12). Seven matches against the claimed classes still cost **−42.4 Elo**.
>
> **3. The +3.8 headline is not the bet.** Decomposed: claimed classes
> **−42.36** over 7 matches, all other classes **+45.81** over 6 matches, net
> **+3.44** (the tape's +3.8 is the same number through rounded tape rows). Every
> point of the positive headline came from point-blank, economy-first and all-in
> rush — classes the case made no claim about.
>
> **4. HEADLINE CORRECTION — v75 played 14 rated matches, not 13, and finished
> net −4.65.** Match #374 (Banminary v41, 1-4, **−8.09**) was **created at
> 09:52:43Z under v75** and completed at 09:58:13Z, **76 seconds after v76
> activated**. Three independent legs stamp it v75 (§0.3). The tape's
> "13 rated, +3.8" stops one match short and credits the loss to v76's account.
> **v75's true ladder record is 14 rated, 7W-7L, 33/70 games, net −4.65 Elo.**
>
> **5. STANDING GIVEAWAY, NEW HEADLINE — the stack leak reproduces in the wild
> and is mostly an opponent exploit, not our routing bug.** 1,856 of 42,826
> mined stacks (**4.33% = 18,560 Ti**) were banked by the enemy core across 15
> of 70 rated games. **79.7% is an adjacency siphon** — our unwired harvester
> outputs straight onto an enemy conveyor planted next to it — not the
> misdirected-own-chain signature the local lighthouse det game showed (that is
> 6.7%). Owner: **Ouroboros, 18.16% of everything we mined against them**. Root
> cause is a wiring regression: unwired harvester-rounds **24.3% (v74) → 40.4%
> (v75)** as the harvester count grew faster than the belt. Full numbers and fix
> scoping in §8; relayed early to the builder per the mid-flight pre-clearance.
>
> **6. Carryover grafts all clean, and one of them was nearly reported as a
> regression.** E2b **0 / 4,700** relay builds on ore; E1 **1 sub-floor
> conversion / 6,537**; S1 **26 naive own-building-fire candidates → 0 verified
> by an HP-delta ledger**. Every one of the 26 is our turret killing an enemy
> builder bot standing on our own (bot-passable) conveyor. A detector that
> trusted the fire event's target tile would have manufactured a 26-event S1
> regression out of a clean guard.

| | |
|---|---|
| Subject | **v75 "Eir 8"** = `bots/_v85hsd/main.py` md5 `4a2aeb50ef8ff63ea55ddc25baca2628` |
| Window | live **09:33 → 11:57 local** 2026-08-08 (07:33Z → 09:57Z). Baseline **1587.2 @ 360**, tape row `v75-final` **+3.8 @ 373** |
| Corrected window | **14 rated matches (#361–#374), net −4.65 Elo**, 1587.2 → 1582.55 (§0.3) |
| Successor | **v76 live from 09:57Z** (11:57 local); adopted fact at write time: v76 beats hsd **61.7%** head-to-head over 480 games (tape `hsd-vs-v76-bar`) |
| Archive state at read time | 20 v75 matches (14 ladder + 6 unrated), 100 replays, **all present, no pending tail** (§0.4) |
| Comparators | v74 "mineguard" (x3r0) 14 rated / 70 games; v73 "Eir 7" (`_v84g`, our lineage) 5 rated / 25 games; v76 reference match `e64c3327` (5 games, behavioural fingerprint only) |
| Ship case scored | `docs/research/v85hs-mechanism-read-2026-08-08.md` + the 09:01 expected-Elo routing package (fix-the-bleed on picket/CAD) |
| Decode contract | `tools/replay_schema.md` (incl. the damage-target law), `tools/replay_census.py` primitives, `docs/tooling.md` ratio rule |
| Tooling | `scratchpad/eir8_read/{ext,pass2,an,checks,checks2,checks3,verify8,verify8b,verify8c}.py`, built on `scratchpad/ad_flips/decode.py` |
| Channel | `.replay26` wire events + `.meta.json` + `elo_history.tsv` only. **Zero downloads, zero games run, zero bot edits.** |

---

## 0. Corpus, seats, and boundary stamps

### 0.1 Enumeration

Every `replay_archive/*.meta.json` where `teamAName` or `teamBName` ==
`OpenSverige` **and that side's version == 75**. Re-enumerated fresh at read
time; the archiver landed two further ladder matches **during** this read
(§0.4), and both are folded in.

| segment | matches | games |
|---|---|---|
| **RATED (`triggeredBy: ladder`)** — primary | **14** | **70** |
| UNRATED annex (`triggeredBy: unrated`) | 6 | 30 |

### 0.2 Seats — free, and used as a self-check

Per `docs/research/bo5-seat-assignment-2026-08-08.md`, engine seat is fixed per
match and meta `teamAName` == engine `TEAM_A` always. Our seat = **A iff
`teamAName == 'OpenSverige'`**, all 5 games of the match.

**This is checkable and it checks out.** Decoding each replay's winner under
that seat map reproduces the meta's `scoreA`-`scoreB` in **20 of 20 matches**,
game for game. Seat mapping is not an assumption anywhere below.

### 0.3 Boundary stamps — decisions, listed

v76 activated **09:57Z**. The MATCH-BOUNDARY RULE was pre-registered because
the meta version field alone is not trustworthy across that line. Decisions:

| match | createdAt | completedAt | meta ver | decision |
|---|---|---|---|---|
| `019771d2` … `d61337ce` (12 matches) | 07:42Z–09:32Z | 07:47Z–09:37Z | 75 | **v75**, unambiguous — both timestamps ≥20 min clear of the boundary |
| `aa8ef0eb` (gsxWins 3-2, +5.78) | 09:42:43Z | 09:44:36Z | 75 | **v75**, unambiguous |
| **`9db6a45d` (Banminary v41 1-4, −8.09)** | **09:52:43Z** | **09:58:13Z** | 75 | **v75 — BOUNDARY CASE, adjudicated below** |
| `e64c3327` (Lunds 2-3, −1.51) | 10:02:43Z | 10:06:53Z | 76 | **v76**, excluded from the v75 corpus; retained as a behavioural reference |

**`9db6a45d` adjudication — v75, on three independent legs:**

1. **Creation timestamp.** Created 09:52:43Z, **4 min 17 s before** v76
   activated. The bots are snapshotted at match creation; a match created under
   v75 is played by v75 whatever the clock says when it finishes.
2. **Elo chain.** Reconstructing the ladder rating from the pre-registered
   baseline 1587.2 @ 360 and the 14 archived deltas reproduces **every**
   `elo_history.tsv` row across the window, including the last two:
   `#373 → 1590.64` (tape 1591 @ 373) and `#374 → 1582.55` (tape 1583 @ 374).
   The −8.09 belongs to match #374 and to no other.
3. **Behavioural fingerprint.** Build-profile rates per 1,000 rounds, our side:

   | corpus | barrier | games w/ barrier | gunner | sentinel |
   |---|---|---|---|---|
   | v75 rated (12 clean matches) | 0.06 | 2/60 | 4.39 | 4.53 |
   | v73 "Eir 7" (our lineage) | 0.24 | 2/25 | 4.66 | 5.13 |
   | **`9db6a45d` (boundary)** | **0.37** | **1/5** | **2.20** | **8.06** |
   | **`e64c3327` (v76, known)** | **6.42** | **4/5** | **10.54** | **4.58** |

   v76's barrier rate is two orders of magnitude above v75's and it lays
   barriers in 4 of 5 games; the boundary match lays one barrier in five games
   and sits squarely in the v73/v75 band on every row. (n=5 for the v76
   reference, so this leg corroborates rather than decides — the two metadata
   legs carry the call.)

**Consequence.** The pre-registered "13 rated / +3.8" window is scored below as
the primary (it is what the ship case was to be judged on), with the 14-match
corrected record reported alongside everywhere it changes an answer.

### 0.4 Pending tail — CLOSED

At the pre-registration's last check the archive held 12 rated matches and the
13th was missing. **It is no longer missing.** During this read the archiver
landed `aa8ef0eb` (gsxWins, +5.78 — this is the 13th) and `9db6a45d`
(Banminary, −8.09 — the 14th, §0.3). The archive is now **complete for v75**:
every match in the Elo chain #361–#374 has a meta and 5 replays. Nothing is
pending, and the +6.1 that the pre-read reconstruction attributed to a missing
match resolved as the gsxWins **+5.78** (the residual is tape rounding).

---

## 1. Check 1 — heal staffing vs the bimodal law

T-state sampled late per decoder v2 (first-crossing is noise); bodies-on-seats
per damage round as the volume measure; arrival latency as the control.
Episodes are v1 machinery: contiguous core-damage rounds merged across gaps
< 30, substantive = ≥100 HP and ≥10 rounds.

### 1.1 Pooled, against both predecessors and against decoder v2's baseline

| corpus | substantive sieges on our core | ratio median | ≥0.94 lobe | latency median | latency ≤3 | **bodies/damage-round** | heal HP/r | incoming HP/r |
|---|---|---|---|---|---|---|---|---|
| decoder-v2 baseline (v72-era, 45 games) | 53 | **0.73** | 16/53 = 30.2% | 1 | 36/53 = 68% | not measured | — | — |
| v73 "Eir 7" (our lineage) | 24 | 0.776 | 8/24 = 33.3% | 1 | 19/24 = 79% | **1.868** | 6.27 | 14.02 |
| v74 "mineguard" (slot predecessor) | 66 | 0.829 | 25/66 = 37.9% | 1 | 41/66 = 62% | **2.322** | 6.97 | 11.11 |
| **v75 "Eir 8"** | **79** | **0.857** | **29/79 = 36.7%** | **1** | **70/79 = 89%** | **3.025** | **9.43** | **14.42** |

**The volume lever moved and the latency control stayed flat, which is exactly
the shape the pre-registration predicted.** Bodies-on-seats per damage round is
up **+30.3%** on v74 and **+61.9%** on our own v73; heal output per damage round
is up **+35.3%** on v74. Arrival latency — the control — has a median of 1 round
in every corpus including the v2 baseline, and never moved. Decoder v2's reading
("the problem is heal volume per round, not heal reaction time") is confirmed as
the right diagnosis, and hsd is the first ship to move the diagnosed quantity.

**But the ratio did not move as far as the bodies did, because incoming rose
with it** — 11.11 → 14.42 HP/r. The heal line got 35% stronger against an
opponent set hitting 30% harder, so survive-lobe clearance is flat on v74
(37.9% → 36.7%) even though median ratio improved (0.829 → 0.857). The lever
works; the pool got harder over the same window.

### 1.2 By class — where it landed (v74 → v75, same measurement, same code)

| class | bodies/dmg-rnd | ratio median | ≥0.94 lobe | latency ≤3 | incoming HP/r |
|---|---|---|---|---|---|
| **picket** (Ouro/Lunds/PP) | **2.161 → 3.309 (+53%)** | 0.810 → **0.917** | 33.3% → **47.4%** | 57% → **89%** | 12.16 → 14.52 |
| **CAD-family** (CAD/KCM) | **1.721 → 3.323 (+93%)** | 0.470 → **0.809** | 21.4% → **37.0%** | 50% → **81%** | 15.16 → 18.06 |
| point-blank | 1.928 → 2.551 | 0.749 → 0.868 | 30.8% → 45.5% | 54% → 100% | 9.09 → 6.84 |
| economy-first | 3.775 → 2.448 | 1.111 → **0.596** | 80.0% → **0%** | 80% → 100% | 7.36 → **18.25** |
| all-in rush | 2.791 → 1.901 | 0.884 → 0.690 | 33.3% → 31.2% | 83% → 88% | 22.09 → 20.20 |

**The two claimed classes are the top two gainers on the designed quantity, by a
wide margin.** CAD-family nearly doubles its heal-line staffing and its median
siege ratio goes from deep in the die-lobe (0.470) to the edge of the gap
(0.809). This is the clearest "the mechanism did what it shipped to do" result
in the read.

**Two classes went the other way and both have an identifiable cause.**
economy-first collapses from 1.111 to 0.596 — but its incoming rate went
7.36 → 18.25 HP/r, i.e. we met a different (harder) opponent mix, not a weaker
heal line; 0033 v43 is the same sentinel-on-an-uncovered-bearing mechanism the
v73 read named as expected-unfixed. all-in rush drops because the class now
contains **two** matches, and the second is Banminary **v41** — a version bump
from the v39 we beat 4-1 — which is the boundary loss (§0.3).

### 1.3 Bimodal law placement

Of 79 substantive sieges on our core, placement against end-of-game core state:
**53 agree, 17 disagree, 9 fall inside the 0.86–0.94 gap.** The 17 disagreements
are dominated by episodes that were *interrupted* rather than resolved (the same
mode as the v73 read's single exception: we killed their core first, or the game
ended at r1000 with the siege live). Placement here is scored against
end-of-game core state, which is coarser than the v73 read's per-episode outcome
test — the 10/11 replication in that read is the stronger form and is not
contradicted. Read this row as "the law survives production contact", not as a
retune.

---

## 2. Check 2 — CLASS PRIORITY: did the bet pay where it claimed?

Class map is the authoritative one from
`docs/research/elo-weighted-battery-2026-08-08.md` §1. **Note a discrepancy with
the brief:** the brief listed Lunds Stallions under CAD-family as well as picket;
the battery doc places Lunds in **creeping gunner picket** only, and CAD-family
as **CtrlAltDefeat + Kings College Munich**. The doc is followed; Lunds is
scored under picket.

### 2.1 The pre-registered window (13 rated matches, #361–#373)

**7W-6L, 32/65 games, net +3.44 Elo** (tape-rounded +3.8).

| class | matches | W-L | net Elo | Elo/match | games | game share |
|---|---:|---|---:|---:|---|---:|
| **CAD-family** | 3 | 1-2 | **−21.49** | −7.16 | 4/15 | 26.7% |
| **picket** | 4 | 1-3 | **−20.87** | −5.22 | 7/20 | 35.0% |
| economy-first | 2 | 1-1 | +8.73 | +4.36 | 6/10 | 60.0% |
| all-in rush | 1 | 1-0 | +10.81 | +10.81 | 4/5 | 80.0% |
| point-blank | 3 | 3-0 | **+26.27** | +8.76 | 11/15 | 73.3% |

### 2.2 The same table for the predecessor v74 (14 rated, net −23.67)

| class | matches | W-L | net Elo | Elo/match | games | game share |
|---|---:|---|---:|---:|---|---:|
| **picket** | 3 | 0-3 | −38.01 | −12.67 | 2/15 | 13.3% |
| **CAD-family** | 2 | 0-2 | −26.75 | −13.37 | 1/10 | 10.0% |
| economy-first | 2 | 0-2 | −13.47 | −6.74 | 3/10 | 30.0% |
| unclassified (Focalground) | 1 | 1-0 | +12.62 | +12.62 | 5/5 | 100% |
| all-in rush | 2 | 2-0 | +18.63 | +9.31 | 8/10 | 80.0% |
| point-blank | 4 | 3-1 | +23.32 | +5.83 | 14/20 | 70.0% |

### 2.3 The answer

**Directionally yes, at half the claimed size, and not significantly at this n.**

| claimed class | v74 Elo/match | v75 Elo/match | Δ | v74 game share | v75 game share | Wilson 95% |
|---|---:|---:|---:|---|---|---|
| picket | −12.67 | **−5.22** | **+7.45** | 13.3% (2/15) | **35.0% (7/20)** | [18.1, 56.7] vs [3.7, 37.9] |
| CAD-family | −13.37 | **−7.16** | **+6.21** | 10.0% (1/10) | **26.7% (4/15)** | [10.9, 52.0] vs [1.8, 40.4] |
| **pooled bleed** | −12.95 | **−6.05** | **+6.90** | 12.0% (3/25) | **31.4% (11/35)** | Fisher **p = 0.12** |

The intervals overlap; picket alone is p = 0.24, CAD alone p = 0.61. **The
direction is right in both classes and consistent with the mechanism numbers in
§1.2, but seven matches cannot carry a significance claim, and the read should
not be quoted as one.** Against the longer POST68 class baselines
(picket −7.34/match, CAD −6.77/match) picket still improves and CAD is flat —
the v74 window was an unusually bad one for both classes, and part of the
apparent gain is regression toward that longer mean.

### 2.4 Per-game mechanism notes, claimed classes

**picket (1W-3L, 7/20 games).** The pattern is *economy built, economy not
connected, economy drained*. In the three Ouroboros games we lost with a live
economy (`5a6a1a8f` g1/g2/g5) our harvesters/round were 6.48 / 11.48 / 10.55
while directed-wired harvesters/round were **1.41 / 2.56 / 3.90** — we mined
two to four times more than we could ship. Those are precisely the three games
carrying **47.1% / 29.9% / 38.6%** stack leak into Ouroboros's core (§8). The
one Ouroboros win (`g4`) is the mirror image: 19.09 harvesters/round at 11.56
wired, delivered 27,540 to their 1,540. Against Lunds the failure is starker and
earlier — `g2` runs 1.34 harvesters/round at **0.17** wired and delivers 170 Ti
in 370 rounds. Against Powerpuff the heal line is genuinely good — heal/incoming
**0.92–1.09 in every game where a real siege happened** — and the losses are
r1000 tiebreak losses on delivery volume, not core deaths. (The one exception,
`019771d2` g3, is not a heal failure at all: 0.99 harvesters/round at 0.04
wired, 100 Ti delivered in 659 rounds — a total economic collapse.)

**CAD-family (1W-2L, 4/15 games).** Different failure. Staffing is *fine* —
bodies/damage-round 3.32, heal/incoming 0.82–0.97 in four of the five
`0ae5da15` games — and the cores die anyway, because incoming is 18.06 HP/r, the highest
sustained rate in the rated corpus. This is the class where the heal lever is
working and is still being outgunned: heal 11.55 HP/r against 18.06 HP/r
incoming is a 6.5 HP/r structural deficit that no plausible number of seats
closes (eight staffed seats is 32 HP/r, but we are seating 3.3). **CAD-family is
a damage-suppression problem wearing a heal-line costume**, and the ship case
bought the wrong half of it. The `8d0e02c1` win (3-2) and the `0ae5da15` loss
(0-5) are the same bot against the same opponent version 66 minutes apart, which
is a useful reminder of how wide the match-level variance is at n=3.

---

## 3. Check 3 — H1 economy signature

### 3.1 Delivery lift and the wiring gap

| corpus | delivered/100 r (us) | (them) | harvesters/r | **directed-wired/r** | Ti per harvester-round | builders/r |
|---|---:|---:|---:|---:|---:|---:|
| v73 "Eir 7" | 43.38 | 80.80 | 4.72 | 1.70 | 0.920 | 4.95 |
| v74 "mineguard" | **110.39** | 96.69 | 6.82 | **5.16** | **1.620** | 6.72 |
| **v75 "Eir 8"** | 104.08 | 98.96 | **7.52** | 4.48 | **1.384** | 6.65 |

**The antler-style lift is real against our own lineage and flat-to-slightly-down
against v74.** Delivery per 100 rounds is 2.4× our v73 and within 6% of v74.
The interesting number is the third one: **v75 runs 10% more harvesters than
v74 on 13% fewer wired harvesters, and each harvester-round yields 15% less
titanium (1.620 → 1.384)**. The mine expanded faster than the belt. §8 shows
that gap is not merely idle capacity — it is the surface the siphon feeds on.

By class the lift is strongest in exactly the claimed classes: picket 89.20 →
111.78 per 100 r, CAD-family 70.51 → 104.49, and CAD flips from being
out-delivered (70.51 vs 95.61) to out-delivering (104.49 vs 87.20).

### 3.2 Seat pin vs shuffle

| corpus | seat-resident builder-rounds / r | seat departures / 100 r | **departures per resident-round** |
|---|---:|---:|---:|
| v73 "Eir 7" | 1.195 | 18.64 | **0.1560** |
| v74 "mineguard" | 1.363 | 39.44 | **0.2894** |
| **v75 "Eir 8"** | **1.424** | 40.18 | **0.2822** |

**Answer: v75 does not pin — it staffs.** Departures per resident-round is
statistically indistinguishable from v74 (0.2822 vs 0.2894) and nearly twice our
own v73's. What changed is the number of bodies present, not their stickiness.
In the claimed classes the body count is where the whole move is: picket
1.203 → 1.599 seat-resident rounds per round (+33%), CAD-family 0.830 → 1.525
(+84%). **The H1 sticky tie-break is not visible as stickiness in production;
the ceiling lift and heal detail are visible as headcount.** If the design intent
was pinning, that intent is unconfirmed in the wild.

### 3.3 Tiebreak-#1 margins (games reaching r1000)

| corpus | r1000 games | won | delivered-Ti margin median | mean | delivered ratio median |
|---|---:|---:|---:|---:|---:|
| v73 "Eir 7" | 3 | 1 | **−7,260** | −5,857 | 0.62 |
| v74 "mineguard" | 18 | 9 | +900 | +1,697 | 1.10 |
| **v75 "Eir 8"** | **20** | **13** | **+5,990** | **+4,585** | **1.96** |

**This is the strongest single improvement in the read.** In games that go the
distance v75 does not merely edge the tiebreak, it dominates it — the median
r1000 game is won on delivery by roughly 2:1, against v74's coin-flip 1.10 and
v73's losing 0.62. Best margins: OopsGotYourElo 31,350–50, Ouroboros
27,540–1,540, CtrlAltDefeat 13,120–480. The three worst are all picket
(Ouroboros −15,200; Powerpuff −7,990 and −7,760) and all three are games where
the wiring gap and the leak (§8) are both live.

---

## 4. Check 4 — hsb launcher seat gate

The gate under test: **no own launcher on any of the 8 core-orthogonal heal
seats** — deliberately the full seat set with *no* delivery-terminus exemption
(`_v85hsd/main.py:1830-1846`). The wider `HS_SEAT_PROTECT` rule bans own
turrets/harvesters/barriers on non-delivery seats, with the ≤2 delivery termini
exempt.

**Launcher gate: 0 violations in 70 rated games (0 in 30 unrated).** Not one
own launcher was ever placed on a heal seat. The gate is clean, exact, and
requires no interpretation — it uses the full seat set, so it has no dependence
on the delivery-seat computation.

**Impassables on seats: 8 events in 70 rated games, all terminus-exempt.** Of
the 8, five land on delivery seats under a full-map reconstruction of
`delivery_seats()`. The remaining three (and one unrated) are flagged only
because my reconstruction uses **full** map knowledge while the bot uses **its
own decoded** walls and ore. All four are on the same map (25×15), and under the
bot's undecoded-map fallback (the centre-distance scorer the function uses when
`ores` is empty) all four tiles **are** delivery seats:

| event | map | tile | full-map dseats | undecoded-fallback dseats | verdict |
|---|---|---|---|---|---|
| `74f3e7a3` g1 r3 sentinel | 25×15 | (12,5) | (10,3),(13,3) | **(12,5),(11,5)** | exempt |
| `3cd88b65` g1 r3 sentinel | 25×15 | (11,5) | (10,3),(13,3) | **(12,5),(11,5)** | exempt |
| `3311f968` g2 r344 sentinel | 25×15 | (12,9) | (10,11),(13,11) | **(12,9),(11,9)** | exempt |
| `1f2a1381` g5 r1 sentinel *(unrated)* | 25×15 | (12,5) | (10,3),(13,3) | **(12,5),(11,5)** | exempt |

**Watch item, as pre-registered: the terminus exemption fires, and it fires on
a known site.** Three of the eight exempt events are a **barrier at (20,4)** —
the hand-coded `hive_bunker` special case the v73 read already flagged, now
observed in production on the 25×25 seat in `8d0e02c1` g4, `873cfde7` g2 and
`9db6a45d` g2. The exemption is doing what it was designed to do (keeping a
delivery terminus usable) but it is also the one route by which an impassable
still reaches the ring.

**Cost side, and the counterweight the mechanism read predicted.** Own
impassable seat-tile-rounds are **0.0511/r** against own *conveyor* seat-tile
rounds of **5.517/r** — i.e. our seat ring is ~99% bot-passable, confirming the
plank's own red-flag note that the conveyor half of the original correlation was
confounded. Meanwhile **enemy builder bots stood on our heal seats for 6,736
rounds = 17.61 per 100 rounds** of play. The ring rent the hs mechanism read
warned about (disqualifier (a): "any opponent that melees the core ring can
collect the same rent") **is being collected in the wild, at 3.4× the rate our
own buildings occupy those seats** (0.176 enemy-bot seat-rounds per round
against 0.051 own-impassable seat-tile-rounds per round).

---

## 5. Check 5 — ceiling-lift signature

Ceiling = `spawn_cap 5 + REPLACEMENT_MAX 8 = 13`.

| corpus | spawns median | mean | max | games > 13 spawns | at-ceiling games: max bank after r20 (median) |
|---|---:|---:|---:|---|---:|
| v73 "Eir 7" | 6 | 7.6 | 15 | 2/25 = 8.0% | 92 |
| v74 "mineguard" | 8 | 9.6 | 18 | 15/70 = 21.4% | 227 |
| **v75 "Eir 8"** | **10** | **16.2** | **88** | **27/70 = 38.6%** | 142 |

**`POP_CEILING_LIFT_ON` fires hard, and the regime the v73 read described is
gone.** That read concluded "the soft ceiling is NOT the constraint; titanium is
— any plank that raises the ceiling buys nothing in this class of game", with
every game spending 5–7 spawns and peak banks of 20–140. One version later the
lift is firing in nearly two of every five games, the mean spawn count has
doubled again, and the extreme cases are far past the ceiling: **88 spawns**
(`d61337ce` g3 vs Powerpuff, 14th spawn at r192, banks at the lifted spawns
126 → 1,496), **83** (`7bcba428` g5 vs Lunds), **70** (`5a6a1a8f` g5 vs
Ouroboros).

**Two distinct regimes are visible in the bank series at the lifted spawns**, and
they should not be pooled:

- **Rich attrition** — banks of 1,500–11,914 at the lifted spawns (`5a6a1a8f`
  g4, `8d0e02c1` g2, `b3dfa660` g3, `019771d2` g1/g2). Here the lift is doing
  exactly what it shipped for: converting an idle bank into bodies on seats. This
  is the regime the plank was designed against and it is now real in production,
  where v73 could not exercise it at all.
- **Poor churn** — banks of 51–130 at the lifted spawns, over dozens of spawns
  (`5a6a1a8f` g1/g2/g3/g5, `7bcba428` g1/g5). Here the lift is refilling a
  population floor that keeps being emptied by a picket that farms builders. It
  buys bodies, but at 30 Ti× rising scale each, out of an economy that is already
  losing the delivery race. **The 70-spawn and 83-spawn games are both losses,
  and both are picket.** Whether that spend is better than the alternative is a
  question this read cannot answer without a paired battery; it is flagged as the
  sharpest open question the ceiling lift raises.

---

## 6. Check 6 — base carryover sanity (E2b / E1 / S1)

Inherited from the `_v84g` family and verified clean at v73. All three still
hold, with one important method correction.

| graft | v73 (our lineage) | v74 | **v75 rated** | v75 unrated |
|---|---|---|---|---|
| **E2b** conveyor/splitter built on an ORE tile | 0 / 908 | 0 / 3,161 | **0 / 4,700** | 0 / 1,870 |
| **E1** sub-floor peacetime conversions | 0 / 1,504 | 4 / 8,784 | **1 / 6,537** | 2 / 3,165 |
| **S1** own-building fires, naive detector | 20 | 27 | **26** | 1 |
| **S1** own-building fires, **HP-ledger verified** | **0** | **1** | **0** | **0** |

**E2b — CONFIRMED, with a separate finding.** Zero ore paves across 4,700 rated
relay builds. Separately, **6 turrets were sited on ore tiles** in the rated
corpus (and 4 unrated). That is *not* an E2b violation — the ban gates
`pave_blocked`, which governs conveyor/splitter placement only — but each one
permanently occupies a mine site. Small (6 sites across 70 games), named, and
logged here so it is not rediscovered as an E2b regression.

**E1 — CONFIRMED.** The `under` latch is reconstructed **exactly** from the wire
(`main.py:1429-1462`: enemy gunner/sentinel at d²≤64 of the core anchor, or enemy
builder bot at d²≤16, or core HP dropped since the previous core turn; latched 50
rounds), and every `convert_ammo` is priced against
`max(12 if weapons else 52, min(harvester_cost, 23) + 23)` with `harvester_cost`
replayed from our own harvester builds. **One violation in 6,537 conversions,
2,969 of them in confirmed-quiet rounds.** Ammo starvation watch: turret-alive
rounds with team ammo < 4 = **4.8%** rated (17.8% unrated, where the economy
never gets going).

**S1 — CONFIRMED, and this is the methodological headline.** The naive detector —
"our turret fires at a tile holding our own building and no unit" — reports
**26 events**. An HP-delta ledger on the target building says **all 26 took
exactly 0 damage**. Four were traced to the wire in full (`8d0e02c1` g2, rounds
182/271/545/644): in every case an **enemy builder bot** had moved onto our
conveyor that round, took **−7**, and died; our conveyor ended the round at full
20 HP. The events are our gunners killing raiders standing on our own
bot-passable belt — the guard working, not failing. The naive count is a decoding
artefact of event ordering (the `FireTurret` update is emitted *after* the
victim's `removeEntity`, so a snapshot taken at fire time sees an empty tile).

> **Method rule for `tools/replay_schema.md`, earned here:** an own-building-fire
> detector must be closed with an HP-delta ledger on the target building, not
> with tile occupancy at the fire event. Occupancy at that instant is wrong in
> the one direction that manufactures false positives — this read would have
> reported a 26-event S1 regression against a clean guard.

---

## 7. Check 7 — eco-optimal scorecard (decoder-v2 template, first production use)

Five components, each HOLD or BREAK, per `tipping-point-decoder-v2` §6.1.
**Implementation note, load-bearing:** this is a re-implementation of the v2
walker, not v2's own code. Components 1, 3 and 5 are exact. **UDMG is
approximated** (uncovered near-core enemy turret present *and* our core already
damaged, sampled every 10 rounds) and **component 4's actor attribution is
approximated** (a shift against us with no proximate enemy event in the
preceding ≤15 rounds from the v1 ladder counts as our omission). Cross-document
comparison to v2's published 0.84/5 is therefore indicative only. **The
v73/v74/v75 comparison below uses identical code on all three and is internally
valid.**

### 7.1 Distance from optimal

| corpus | n | mean | median | 0/5 | 1/5 | 2/5 | 3/5 | 4/5 | **5/5** | mean in wins | mean in losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| decoder-v2 baseline (v72-era) | 45 | 0.84 | 1 | 22 | 13 | 5 | 5 | 0 | **0** | 2.08 | 0.34 |
| v73 "Eir 7" | 25 | 1.12 | 1 | 9 | 8 | 4 | 4 | 0 | **0** | 1.82 | 0.57 |
| v74 "mineguard" | 70 | 1.99 | 2 | 12 | 20 | 10 | 16 | 9 | **3** | 3.00 | 1.08 |
| **v75 "Eir 8"** | 70 | **1.87** | 2 | 14 | 20 | 11 | 14 | 8 | **3** | 3.00 | 0.86 |

**The template's monotone separation replicates cleanly, which is the validation
that it measures something real:** at 0/5 we won **0 of 14**; at 3/5, 11 of 14;
at 4/5, **8 of 8**; at 5/5, **3 of 3**. Mean score in wins 3.00 against 0.86 in
losses.

**We now play our own game sometimes.** v2's corpus had zero 5/5 games in 45.
v75 has **three** (`3cd88b65` g3/g4/g5, all vs OopsGotYourElo, all r1000 wins) and
eight at 4/5. Against our own lineage predecessor the jump is large
(v73 1.12 → 1.87); against the slot predecessor it is a wash (1.99 → 1.87), and
the small decline is entirely component 2.

### 7.2 Which component breaks first

| component | v73 | v74 | **v75** |
|---|---:|---:|---:|
| 1 DELIV-EARLY | 96% | 86% | **86%** |
| 2 FLAT | 100% | 79% | **84%** |
| 3 SIEGE-MINOR | 68% | 56% | **51%** |
| 4 NO-OMISSION | 64% | 30% | **37%** |
| 5 TERMINAL | 60% | 51% | **54%** |

**FLAT breaks first in 59 of 70 games** (the remaining 11 never break anything),
with a median of **4 breakage crossings against us per game** and a max of 17.
This replicates v2's finding exactly: *the first thing that goes wrong in our
games is a breakage curve crossing against us*, not a heal failure and not an
economy failure.

**The component the ship case was aimed at is the one that improved most.**
SIEGE-MINOR — the component that is literally "heal latency ≤3 and episode ratio
≥0.94 for every substantive siege" — broke in 68% of v73's games, 56% of v74's,
and **51% of v75's**. That is the ship case's own scoreboard and it moved in the
right direction across both predecessors.

### 7.3 By class

| class | n | mean score | wins |
|---|---:|---:|---:|
| economy-first | 10 | **2.90** | 6 |
| point-blank | 15 | 2.33 | 11 |
| picket | 20 | 1.80 | 7 |
| CAD-family | 15 | **1.27** | 4 |
| all-in rush | 10 | 1.20 | 5 |

The scorecard ranks the classes in almost exactly the order the Elo table does,
from an entirely independent construction. **CAD-family at 1.27/5 is where we
are furthest from playing our own game**, consistent with §2.4's reading that it
is a damage-suppression problem the heal lever does not reach.

---

## 8. Check 8 — STACK LEAK (added post-registration)

**The question:** the margin decode (`ad-flips-margin-decode-2026-08-08.md` §5)
found v75 leaking 27% of mined stacks into the *enemy* core on lighthouse in a
local deterministic game — misdirected delivery, stacks banked by the opponent.
Does it reproduce in the wild?

**Answer: YES — and the wild mechanism is not the local one.** Relayed to the
builder ahead of this document per the mid-flight pre-clearance.

### 8.1 Volume

Stacks are followed individually via `ResourceMove.resourceId`, from the
harvester tile that emitted them to the core footprint that banks them.

| corpus | our mined stacks | **leaked into enemy core** | their stacks banked by us | games with a leak |
|---|---:|---:|---:|---|
| v73 "Eir 7" | 4,903 | **897 = 18.29%** | 9 | 9/25 |
| v74 "mineguard" | 38,220 | **1,025 = 2.68%** | 504 | 19/70 |
| **v75 "Eir 8" rated** | **42,826** | **1,856 = 4.33% = 18,560 Ti** | 596 | **15/70** |
| v75 unrated | 13,391 | 200 = 1.49% | 797 | 8/30 |

**The leak is inherited, not new.** Our own v73 leaked four times worse (18.29%).
v75 is a **regression against v74** (2.68% → 4.33%), not against our lineage. Net
flow is **−1,260 stacks = −12,600 Ti** handed over across the rated window.

It is concentrated, not diffuse. Worst games: **58.5%** (`7b532aea` g2, 0033),
**47.1% / 38.6% / 29.9%** (`5a6a1a8f` g1/g5/g2, Ouroboros), **19.0%**
(`0ae5da15` g3, CAD), **18.6%** (`b3dfa660` g3, KCM).

### 8.2 Mechanism — the correction

Every leaked stack's full hop path was classified by the ownership of the relay
tiles it crossed (the originating harvester hop excluded):

| mechanism | stacks | share |
|---|---:|---:|
| **ADJACENCY SIPHON** — our harvester outputs directly onto an **enemy** conveyor planted orthogonally adjacent; **zero** hops on our own belt | **1,479** | **79.7%** |
| HANDOFF — our chain carries it partway, then feeds their belt | 252 | 13.6% |
| DIRECT MISROUTE — entirely on **our own** belt into their core (the lighthouse det signature) | 125 | 6.7% |

**The wild leak is overwhelmingly an opponent exploit against our unwired
harvesters, not our own misrouted chain.** The det finding is real and it
reproduces — but it is 7% of the wild volume. Worked example, `5a6a1a8f` g5
(Ouroboros, 28×20, our core at (7,9), theirs at (19,9)): our harvester at
(11,12), built by us at r96, emits a stack at r113 that walks twelve hops
**east** — (11,13)→(12,13)→(13,13)→(13,12)→(14,12)→(14,11)→(15,11)→(16,11)→
(16,10)→(17,10)→(18,10)→(19,10) — into Ouroboros's core at r133. Every relay on
that path is **theirs**. Four of our harvesters ((15,12), (11,12), (12,10),
(8,13)) fed their economy for the rest of the game: 561 stacks, **5,610 Ti**.

### 8.3 Root cause — the wiring gap

| corpus | harvester-rounds | directed-wired harvester-rounds | **UNWIRED** |
|---|---:|---:|---:|
| v73 "Eir 7" | 39,499 | 14,199 | **64.1%** |
| v74 "mineguard" | 224,597 | 170,087 | **24.3%** |
| **v75 "Eir 8" rated** | 287,574 | 171,347 | **40.4%** |

**v75's mine grew faster than its belt.** Harvesters/round went 6.82 → 7.52 while
wired/round went 5.16 → 4.48 (§3.1), leaving 40.4% of all harvester-rounds
unwired against v74's 24.3%. An unwired harvester is not merely idle capacity —
it is a free tap for any opponent who lays a conveyor beside it, and the picket
class does exactly that.

### 8.4 Where it hits

| class | leaked / mined | games with leak |
|---|---|---|
| **picket** | **1,248 / 17,725 = 7.04%** | 8/20 |
| CAD-family | 337 / 9,711 = 3.47% | 4/15 |
| economy-first | 227 / 7,933 = 2.86% | 2/10 |
| all-in rush | 44 / 1,821 = 2.42% | 1/10 |
| point-blank | **0 / 5,636 = 0.00%** | 0/15 |

Per opponent, **Ouroboros owns it: 1,048 stacks = 18.16% of everything we mined
against them, in 4 of 5 games.** Then KCM 5.84%, 0033 7.38%, CAD 2.44%, OGE
2.19%, Lunds 1.81%, Powerpuff 1.64%. **Memtrace, Team 48 and gsxWins: exactly
zero.**

Per map size (leaked/mined): 14×18 36.8%, 10×10 16.3%, 28×20 12.5%, 20×26 9.9%,
25×15 2.8%, 26×26 1.5%, 24×24 1.0%, 21×8 0.1%, and **16×16, 18×18, 25×25 all
exactly 0.0%**. It is not a map-size law — it tracks the *opponent*, with map
geometry only modulating.

### 8.5 What it does and does not license

Win rate in games with a leak: **4/15**. Without: **29/55**. That correlation is
**not** a causal Elo estimate — leak games are also the games we were already
losing (an opponent who is winning has time and board control to lay a tap next
to our mine). **The defensible claim is: a confirmed, repeatable, cross-opponent
mechanism that hands away 18,560 Ti per 70 games, concentrated in our #1 bleed
class.** The Elo attribution is not established here and should not be asserted.

**Fix scoping implied by the mechanism split:** the high-volume fix is
**denial-side, not routing-side** — wire our own harvester at or near the build
turn so its output has a friendly destination, and/or treat an enemy conveyor
orthogonally adjacent to one of our harvesters as an attack target. A worker
scoped to "fix our chain direction" addresses 6.7% of the measured bleed.

---

## 9. UNRATED ANNEX — mechanism observations only

> **Provenance stamp: teammate-triggered, unconfirmed.** Six unrated matches,
> 30 games. **No Elo claim of any kind is made or implied from this section.**
> Opponent selection was not ours and is not a ladder-representative sample.

| match | opponent | result | note |
|---|---|---|---|
| `524cc1c6` | sporks v8 | 0-5 | all five core deaths, r106–301 |
| `adbedc98` | Pantheon v56 | 1-4 | four core deaths |
| `883acaab` | The Flotte Experience v38 | 0-5 | strangle class, r146–821 |
| `edd3f08d` | Landers v93 | 0-5 | melee grind; two r1000 tiebreak losses |
| `1f2a1381` | Torsko v5 | 4-1 | |
| `62bc6dd5` | Torsko v6 | 4-1 | |

**Mechanism observations, stated as observations:**

- **The heal line looks like a different bot here.** 22 substantive sieges:
  median ratio **0.497** (rated 0.857), survive-lobe clearance **2/22 = 9.1%**
  (rated 36.7%), **bodies/damage-round 1.952** (rated 3.025), latency median
  **4 rounds** with **5 zero-heal sieges** (rated: median 1, zero zero-heal
  sieges). Both the volume and — uniquely in this corpus — the *latency* control
  fail together.
- **The economy never starts.** Delivered 93.12 per 100 r against their 123.79,
  the only corpus segment where we are out-delivered; median 5.5 spawns
  (rated 10); wired/r 3.74 (rated 4.48).
- **The seat gates hold anyway.** 0 launchers on heal seats; 3 impassable-on-seat
  events, all terminus-exempt (§4); E2b 0/1,870; S1 1 naive candidate, 0
  verified.
- **Leak is low (1.49%)** and the *inbound* direction is high (797 of their
  stacks banked by us, against 200 of ours lost) — the reverse of the rated
  picture, and consistent with these being short games we lost before either
  belt matured.

The honest reading: these opponents are a different and harder mix (sporks,
Flotte and Landers are all classes with zero current battery weight), the games
are short, and the sample cannot separate "v75 is bad against these classes" from
"these are five bad map draws". It is on the board as a **mechanism flag on the
zero-battery classes**, nothing more.

---

## 10. Self-checks

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected` | **200 / 200 team-sides** (100 v75 games), plus **190 / 190** on the v73/v74 comparator corpus. **0 mismatches.** |
| **Seat mapping** — decoded per-game winners vs meta `scoreA`/`scoreB` | **20 / 20 matches reproduce exactly**, game for game. Seat map independently validated, not assumed. |
| **Elo chain** — 14 archived deltas from baseline 1587.2 @ 360 | Reproduces **every** `elo_history.tsv` row #361–#374 (1589.43 / 1594.00 / 1602.11 / … / 1590.64 / **1582.55** vs tape 1583). **0 unexplained steps.** |
| **`under` latch reconstruction** (E1) | Reconstructed from wire events per `main.py:1429-1462`; 6,537 conversions priced, 2,969 in confirmed-quiet rounds |
| **S1 HP-delta ledger** | 26 naive candidates → **0 verified**; 4 traced to the wire in full, all showing an enemy builder bot taking −7 and dying with our conveyor at full HP |
| **Stack accounting** | Every leaked stack followed hop-by-hop via `resourceId`; **0 unknown-origin stacks** in the games spot-audited |
| **Boundary stamps** | 4 decisions listed in §0.3, each with its evidence; 1 genuine boundary case, adjudicated on 3 independent legs |
| **Games excluded** | **Zero.** |

### Bounded and unexplained

1. **Bimodal-law disagreements: 17 of 79 substantive sieges** (§1.3). Placement
   is scored against *end-of-game core state*, which mis-scores interrupted
   sieges (we killed their core first, or r1000 arrived with the siege live).
   The v73 read's per-episode outcome test is the stronger form and reported
   10/11; this read does not contradict it and does not retune the law.
   **Bound: ≤17 episodes, all in the interrupted-siege mode, none affecting a
   §1.1 or §1.2 number.**
2. **Four seat "violations" resolved as map-knowledge artefacts** (§4). All on
   25×15; all exempt under the bot's own undecoded-map fallback. **Bound: 4
   events, 0 confirmed gate misses.** The residual uncertainty is that I cannot
   observe the bot's decoded-ore set directly — only bracket it between full-map
   and empty-map.
3. **Eco-optimal components 4 and UDMG are approximations** of the v2 walker
   (§7 preamble). Cross-document comparison to v2's 0.84/5 is indicative;
   the v73/v74/v75 comparison uses one implementation throughout.
4. **v74 is x3r0's codebase, not our lineage.** The §6 graft rows for v74 measure
   *his* bot's behaviour and are context, not a like-for-like graft test. Our
   lineage predecessor for graft purposes is **v73**. The §1/§3/§5/§8
   behavioural comparisons are valid against both, since they measure
   team-level outcomes rather than our specific code paths.
5. **n. Seven matches against the claimed classes.** Every class-level Elo
   figure in §2 rests on 3–4 matches and carries match-level variance visible in
   the corpus itself (CAD-family: 3-2 win and 0-5 loss against the same opponent
   version, 66 minutes apart). Direction is reportable; magnitude is not.

---

## 11. So-what — what this feeds

1. **The heal-staffing plank is validated as a mechanism and should be kept.**
   It moved the quantity it was designed to move, by the largest margin in the
   two classes it was aimed at, with the latency control flat. That is as clean
   a mechanism confirmation as production data allows.
2. **It is the wrong lever for CAD-family.** 3.32 bodies and heal 11.55 HP/r
   against 18.06 HP/r incoming is a structural deficit; the class needs damage
   suppression (the ray-coverage / L3 fix), not more seats. The expected-Elo
   package bought heal capacity in a class that was losing to damage.
3. **The stack leak is a standing giveaway with a named, denial-side fix**, and
   the fix worker should be scoped to harvester wiring latency and enemy-conveyor
   adjacency — not to chain direction (§8.5).
4. **The wiring gap is the common root** of the leak (§8.3), the picket losses
   (§2.4) and the flat Ti-per-harvester-round (§3.1). One defect, three
   symptoms — the highest-leverage single item this read surfaces.
5. **`v75-final` on the tape should be corrected to 14 rated / −4.65** (§0.3), or
   at minimum annotated, so the swap-rule ledger and any future holder comparison
   are not built on a 13-match number that stops one match short.
6. **Two method rules earned here** belong in the standing docs: the S1
   HP-delta-ledger requirement (§6) and the delivery-seat map-knowledge bracket
   (§4).
