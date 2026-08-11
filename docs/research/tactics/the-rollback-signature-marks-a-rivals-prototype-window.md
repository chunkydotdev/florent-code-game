---
tactic: read the A→B→A version excursion off the public league table to identify a rival's own prototype legs
source: tools/corpus/version_drift.py section 4, over corpus/league_matches.tsv (35,642 matches, 2026-08-01..2026-08-11); external taxonomy https://forum.codingame.com/t/2642
origin: measured in-repo (research arm, sweep 22, 2026-08-11); the practice is named and catalogued by CodinGame competitors, 2017
evidence: documented (the signature); inference (what it means) — research arm's inference
transfers: partial
---

**⛔ D12 RELABEL (side-lane flag, 2026-08-11, adopted): this road is at the BOTTOM OF THE QUEUE, NOT CLOSED.** The finding rests on archive statistics with a BEHAVIOURAL premise — how opponents' versions perform — which is exactly the evidence class D12 forbids retiring a road with, and **no leg has ever been aimed at a freshly-shipped version or an excursion window.** The statistics stand; the claim they support is *"unpromising, queue it last"*, not *"closed"*. D12's own remedy: archive evidence sends a road to the bottom of the queue, never off it.
WHAT IT IS — We run a procedure where a prototype is activated, fired at a target, and
rolled back to the incumbent within minutes. On the public league table that leaves an
unmistakable trace: a team's version sequence goes **A → B → A**, with B holding for a
handful of matches. The team that triggered this sweep produced the textbook case — a
version number moving 67 → 57 → 67 inside 66 minutes.

Measured league-wide, **we are not remotely alone in doing it**: 46 of 72 active teams
(**63.9%**) show at least one A→B→A excursion, and **3.81%** of all league matches
(2,715 of 71,170 team-sides, after dropping 57 rows with a null `eloDelta`) are played
inside one. The distribution is very skewed —
Powered by SmartFridge alone accounts for 123 excursions, CtrlAltDefeat 36, Lunds
Stallions 25; our own OpenSverige shows 10.

**INSTRUMENT GUARD, run because the first version of this cut looked wrong.** Many
excursions have a median span of 0.0 minutes, which raised the possibility that
within-second ordering of same-timestamp matches was *manufacturing* the signature — ladder
pairings cluster at `:59` seconds, so ties are plentiful. Measured directly: **0.00% of
same-team timestamps carry more than one version** (0 of 71,284). A strict variant that
requires every excursion to be strictly time-separated from both neighbouring runs returns
**identical** numbers to the naive one (46/72, 3.81%). The signature is real; the 0.0-minute
spans are simply single-match excursions.

WHY IT MIGHT TRANSFER — two uses, and only one of them is offensive.

**1. ANALYSIS HYGIENE (solid, and it is the one to act on).** Matches a rival played
inside an excursion were played by a **prototype they chose not to keep**. Pooling those
into a per-opponent statistic is worse than pooling across their shipped versions — it
imports a bot that team has actively rejected. Any cell statistic should exclude
excursion-window matches, or at minimum report what share of the cell they are.

**2. INTELLIGENCE (real but currently without a lever).** The excursion tells us which
teams run a test-and-rollback discipline, how often, and when. It also tells us which of a
rival's versions are prototypes versus fielded bots — which is exactly the discriminator
we lack when estimating "what will they field against us". What it does **not** buy is an
attack: we cannot choose our rated ladder pairings, so we cannot arrange to meet a rival
while their prototype holds the slot. And per
`the-fresh-version-is-not-the-weak-version.md`, we would not want to on the mean anyway.

**AND THE PATTERN HAS A NAME IN ANOTHER LEAGUE, WHICH RAISES THE PRIOR WITHOUT SETTLING
IT.** CodinGame competitors named, catalogued and argued about the practice as *"AI hiding"*
(`lad_cg_aihiding.flat`, Marchete, 2017 — curly apostrophes as in the source):

> "AI Hiding: Take advantage of fighting against real AI’s while trying to minimize the time
> your real AI is exposed to the public. That minimization comes in several ways: Submit of
> real AI, then replace for a bad one ASAP; creating killswitches based on time; creating
> killswitches to timeout some % of sure victories, or just force segfaults"

**The first implementation on that list — "Submit of real AI, then replace for a bad one
ASAP" — is exactly the A→B→A trace.** In that league the purpose was to score a measurement
while minimising public exposure. If our rivals are doing the same, then **the version they
leave up is not the one they would bring to a deadline**, and the short-lived version is the
strong one — the opposite of the "un-debugged prototype" reading.

WHAT WOULD KILL IT — three things, and the third is the serious one.
* Version numbers are opaque integers; a team that never reuses a number (monotone
  increments even on rollback) is invisible to this cut. We would under-count them.
* Ten days of one league; the 63.9% is a snapshot, not a constant.
* **THE READING IS AN INFERENCE, NOT A MEASUREMENT.** "A→B→A means they ran a prototype
  leg" is the research arm's inference from our own procedure looking identical. It is
  consistent with at least two other stories — a bad ship reverted, or a platform
  re-activation artifact — and **nothing here distinguishes them.** The library's second
  rule applies in its statistical form: the pattern is right, what it is taken to MEAN is
  not established. Do not upgrade this to `documented` without a discriminator.

**AND THE SAME EXTERNAL CORPUS SUPPLIES THE CAUTIONARY WORKED EXAMPLE, WHICH IS WHY THIS
FILE STOPS AT `partial`.** A CodinGame community read a rival's timeout pattern as exactly
the deliberate anti-scouting killswitch that platform staff had described as feasible three
weeks earlier — and the accused author investigated and concluded
(`lad_cg_spunkhiding.flat`): *"it appears I have been wrong since the beginning because I
use CPU time instead of wall-clock time."* **A whole field inferred intent from a trace that
was a clock bug.** "A team believed they were scouted" is not "a team was scouted".

**⇒ THE DISCRIMINATOR WAS RUN, AND IT SETTLES IT: ROLLED-BACK VERSIONS ARE BAD SHIPS, NOT
HIDDEN STRENGTH.** Each excursion version compared against the incumbent that brackets it,
paired within excursion (407 excursions, 2,539 excursion games,
`tools/corpus/version_drift.py` section 5):

| | excursion version | bracketing incumbent | paired diff | t |
|---|---|---|---|---|
| game share | 0.4278 | 0.5101 | **−0.0823** | **−6.61** |
| eloDelta | −2.505 | +0.098 | **−2.603** | **−6.76** |

**The "AI hiding" reading is unsupported for this league.** A version that appears briefly and is
withdrawn is a *worse* bot, by 8.2pp of game share — which is what our own procedure
produces too, since a prototype is normally worse than the tuned incumbent it displaces.
The external taxonomy raised a real hypothesis and our own data killed it.

**AND THE CONSEQUENCE IS THE OPPOSITE OF THE OFFENSIVE ONE — IT COMPOUNDS THE POOLING
BIAS.** Games against a rival's excursion version are games against a bot they rejected, and
those games make that rival look **8.2pp weaker than they are**. So our per-opponent cells
are biased optimistic from **two independent sources**: stale retired versions
(`block-on-opponent-version-not-opponent-id.md`, −8.00pp) and rolled-back prototypes
(−8.23pp). Both point the same way. Both make us look better than we are.

BUILDER HOOK — `python3 tools/corpus/version_drift.py` prints sections 4 and 5 directly.
The action is a filter, not a plank: when computing any per-opponent cell, **drop matches
falling inside that opponent's A→B→A excursions** and report the dropped count. Now that the
direction is measured, this is a bias correction with a known sign rather than a hygiene
nicety.
