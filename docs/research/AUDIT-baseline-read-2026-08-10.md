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

**Map size does not explain the Bisons — it anti-explains them.** Their two
fastest kills in context land on the two **largest** maps in the pinned set:
snowflake 26×26 at t=66 and saga 24×24 at t=74. **Distance does not protect us
from them**, which is exactly the property that makes the lead worth studying
rather than dismissing as a small-map artifact.

**And the same 25 games contain paired same-map comparisons in BOTH directions,
so no cross-population inference is needed:**

| map | THEM killing US | US killing someone | ratio |
|---|---|---|---|
| snowflake | **66** (Bisons) | 148 (vs Leviathan) | **2.2×** |
| jackpot | **49** (Bisons) | 298 (vs Leviathan) | **6.1×** |

Our own kill-turn median across the 14 wins is **151** (n=14; independently
reproduces the addendum's figure). **On maps we played in the same 25-game block,
the Bisons kill 2–6× faster than we do.** Available without opening a replay.

**Caveat that must travel with any archive follow-up:** the ~195 Bisons games in
the corpus are OUR games against them across eras (92.4% of our archive is
v101-or-earlier per the ⛔ era block), so any pooled "how the Bisons play" rate is
confounded by which of our bots they faced. **The five games above are the only
ones against v102.**

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
