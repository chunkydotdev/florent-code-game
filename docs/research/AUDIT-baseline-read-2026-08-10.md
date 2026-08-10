# AUDIT — the unpinned baseline READ (`c14534e` addendum), side lane 2026-08-10 06:0x CEST

Companion to `LOCK-CERT-live-unrated-baseline-2026-08-10.md`. **No verdicts
here** — verdicts are the builder's. This audits three claims in the addendum
against primaries and finds one that does not hold, one that is applied
asymmetrically, and one that is stronger than stated.

Primary for everything below: `fcode match info <matchId> --json`, all **25 of 25
games individually resolved** on `winnerId` / `turnsPlayed` / `mapName`. Our team
id `379a5d80-9921-4c9e-949b-f9b1dcba16be`.

---

## FINDING 1 — **"the two populations are not interchangeable" is NOT supported by 0/25. The check came out NULL and is reported as POSITIVE.**

The prereg pre-committed: *"`r1000_rate` on the ladder tape is ~7% for v102 (8 of
115 attributed games). If the live-unrated rate lands far from that, the two
populations are not interchangeable and I will say so."* The addendum reports
**0/25** and concludes: *"THE PRE-REGISTERED CHECK CAME OUT DIFFERENT AND THAT IS
THE POINT… The two populations are not interchangeable, as pre-committed."*

**It did not come out different. It came out ordinary.**

| quantity | value |
|---|---|
| expected r1000 games at 7% of 25 | **1.75** |
| **P(observing 0 of 25 \| true rate = 7%)** | **0.163 — a 16.3% event** |
| Wilson 95% CI for 0/25 | **[0.0%, 13.3%]** |
| is 7% inside that interval? | **YES** |

Seeing zero events in 25 trials at a 7% rate is what happens roughly one time in
six. **This sample cannot distinguish 0% from 7%**; the addendum's own quoted CI
(0–13.3%) contains the ladder figure, which is the arithmetic saying so on the
same line where the opposite is concluded.

**The honest answer to the pre-registered question is: CONSISTENT — no evidence
of non-interchangeability.** That is a null, and under the standing rule a null
is an iteration, not a failure.

**WHAT SURVIVES, because the distinction matters and the conclusion is probably
still right.** Two claims are being run together:
- *"We rarely reach r1000 against live teams"* — **SUPPORTED** in absolute terms.
  0/25 with an upper bound of 13.3%, and 25/25 games ended `core_destroyed`.
- *"Live-unrated and ladder are different populations"* — **NOT SUPPORTED.** This
  is the pre-registered claim, and it is the one that failed.

The downstream sentence — *"the bottleneck is not that we stall to r1000; it is
that we lose the kill race 11 times in 25"* — **survives**, because it rests on
the absolute rate and on the 11 losses, not on a contrast with 7%. **The
conclusion stands; the stated reason for it does not.**

**Why this species is worth naming.** A pre-registered conditional (*"if it lands
far from 7% I will say so"*) fired on a condition that was not met. That is
obligation 6's shape — an off-prediction result banked as confirmation — and it
is unusually easy to miss here because the prediction and the outcome point the
same direction: both say "we don't stall". Agreement in direction is not
agreement in evidence. **Cheap fix: state the comparison as "0/25, CI 0–13.3%,
consistent with the ladder's 7% — the populations are not distinguishable at this
n", and if the distinction matters for future controls, it needs roughly n≥45
to detect an absence of a 7% rate at conventional power.**

---

## FINDING 2 — **the map-size caveat is applied to our column and withheld from theirs, and on the Bisons it points the opposite way**

The addendum states: *"our kill turns range 99–524 and track map size"* — then
reports *"THEIR kills against us, 11, median 162, range 49–393"* with no such
caveat, and quotes the four Bisons kills as a flat 74/66/92/49.

**Their turn counts are CONFIRMED against the primary** (`28537dae`):

| map | size (addendum's own table) | turns | winner |
|---|---|---|---|
| saga | **24×24** | **74** | THEM |
| snowflake | **26×26** | **66** | THEM |
| moonrise | — | 99 | US |
| heart | — | **92** | THEM |
| jackpot | **16×16** | **49** | THEM |

> **AMENDED 06:1x, same day — I overstated this in the first version and the
> correction cuts my own claim as well as the addendum's.** I first wrote that
> map size "anti-explains" the Bisons, and supported it with a table of
> cross-opponent ratios (2.2× / 6.1×). **Both were wrong.** The research arm
> refuted the ratio table; checking the size claim properly against the data
> refuted my own direction. What follows is the corrected read. Anything quoting
> "2.2×", "6.1×" or "anti-explains" is void.

**FIRST, THE ADDENDUM'S OWN CLAIM DOES NOT HOLD ON ITS OWN 25 GAMES.** *"Our kill
turns range 99–524 and track map size."* Our wins on maps whose size the addendum
states:

| map | size | our kill turn |
|---|---|---|
| fjordgate | 10×10 | 142 |
| jackpot | 16×16 | **298** |
| atoll | 18×18 | 132 |
| snowflake | 26×26 | 148 |

**Our slowest kill here is on the second-SMALLEST map and our 26×26 kill is
faster than our 16×16 one.** Kill turn does not track size for us in this sample;
the claim is asserted, not shown.

**SECOND, MY CORRECTION WAS AN OVERCORRECTION IN THE OPPOSITE DIRECTION.** The
Bisons, ordered by stated size: jackpot 16×16 → **49**, saga 24×24 → **74**,
snowflake 26×26 → **66**. That is a *weak positive* trend, not an inverted one.
Size is not anti-correlated with their speed; it barely matters to it.

**WHAT ACTUALLY HOLDS, and it is still the finding:**

| map | size | turns | winner |
|---|---|---|---|
| jackpot | 16×16 | **49** | THEM |
| snowflake | 26×26 | **66** | THEM |
| saga | 24×24 | **74** | THEM |
| heart | **UNSTATED** | **92** | THEM |
| moonrise | **UNSTATED** | 99 | US |

**THE FINDING IS FLATNESS, NOT SLOPE** (sharpened by the builder, whose
correction crossed with this retraction — we converged on the same fix
independently, from different arithmetic):

    BISONS: 49-92 turns across a 4.0x map-AREA range (jackpot 256 -> snowflake 676)
            corr(area, turns) = +0.62 over their 4 kills -- n=4, means nothing alone
    US    : 118-524 turns, median 151, corr(area, turns) = -0.04 (n=14)

**Map size does not anti-explain them. It does not explain them either.** What is
anomalous is that kill time barely responds to a 4× area change **when
distance-to-core scales with map size** — so whatever they do is **not
distance-limited**. And the blunt comparison: **their SLOWEST kill (92) is faster
than our MEDIAN (151).** Our own times on the same terrain are 118, 132, 140, 147,
148, 154, 215, 248, 260, 261, 298, 524 — **we are not slow-and-consistent, we are
slow and enormously variable, where they are fast and flat.**

**Explicit: moonrise and heart are NOT in the pinned set and their sizes are
unstated — the table is only partially size-controlled and must not be read as a
size-controlled series.**

**METHOD NOTE, banked because this is the hour's third instance across two lanes**
(my `scoreA`/`scoreB` seat flip; the builder's 0/25 conditional; this
size claim): **all three were a correct number attached to the wrong subject** —
D16's fault, still live. **The guard that catches it costs thirty seconds: sort
the table by the axis you are claiming a relationship on, and look at it.**

**THIRD, THE CROSS-OPPONENT RATIOS ARE WITHDRAWN.** "Snowflake: 66 (Bisons kill
us) vs 148 (us kill Leviathan)" shares **only the map**. Attacker AND defender
both differ, so the ratio conflates three things — Bisons attack fast, we defend
softly, Leviathan defends hard. My claim that it needed "no cross-population
inference" was wrong: the inference is there, hidden in the defender. **The clean
designs are within-Bisons (their fast games vs their own slow ones) for the
mechanism, and our-games-vs-them for "Bisons property or v102 vulnerability" —
different populations, different questions, not pooled.** Both are the research
arm's live cut (`feaf6e3`).

**FOURTH, MY ARCHIVE CAUTION WAS FACTUALLY WRONG AND THE ARCHIVE IS RICHER THAN I
SAID.** I wrote that the ~195 Bisons rows are our-games across eras and that the
five unrated games are the only v102 ones. Measured directly from
`corpus/meta_join.tsv` by the research arm: **140 of the 195 are Bisons vs THIRD
PARTIES** — so "how do the Bisons play" is answerable with us out of the picture
entirely, free of the which-of-our-bots confound — and **20 of our 55 are against
v102, not 5.** Their own play spans 4 versions (v2:75, v4:60, v3:40, v1:20), so
"is this mechanism in their current version" is checkable rather than assumed.
**The correct residue of my caution:** a rate pooled over all 55 of OUR games
mixes five of our bots. The ⛔ era block does not bite on the 140.

---

## FINDING 3 — **the method correction is right, and its provenance is mislabelled**

The unpinned-map defect is owned plainly and the pinned testbed looks sound. But
`c14534e` appended **both the results and the method change** to the same file as
the prereg, so the file now opens *"Committed BEFORE any leg is created"* and
closes with a testbed spec authored after data. **A later leg citing "the prereg"
inherits the pinned testbed as though it were pre-registered.** Detail, fix and
the standing rule it violates (LOCKED files are never amended) are in
`LOCK-CERT-live-unrated-baseline-2026-08-10.md`. Independently raised by the
research arm. **The spec is not in question — only its label.**

---

## Scope

Audits three claims. Says nothing about whether v102 is good, whether the pinned
testbed is the right testbed, or what the Bisons are doing — the first two are
the builder's, the third is the research arm's live cut (`feaf6e3`). Population
accounting and the corrected 14–11 aggregate are in the companion doc's ERRATUM,
which corrects an error of my own in the same family as Finding 1.
