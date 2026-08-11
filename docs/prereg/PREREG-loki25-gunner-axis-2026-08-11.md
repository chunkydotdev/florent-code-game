# PREREG — LOKI-25: STAND OFF THE ENEMY GUNNER'S AXIS. **PROBE TIER.**

**Written 2026-08-11 by the s30 BUILDER. Committed BEFORE submission and before
any LOKI-25 game exists.** Tree `bots/_v146gunaxis`. Diff vs v104
(`bots/_v130loki13`): **one enumeration + one penalty term**, in `raid.py` and
one constant in `doctrine.py`. `main.py` and `eco.py` byte-identical.

**FIRED ON MAGNUS'S CALL** — *"It sounds significant enough to test on unrated
games and see if it gives something."*

## 1. WHY THIS ONE AND NOT THE OTHER SEVEN

It is the only arm today that beat a **properly powered** null.

| arm | vs v104 | n |
|---|---:|---:|
| **LOKI-25 gunner-axis** | **34/64 = 53%** | 64 |
| null — byte-identical renamed v104 copy | **32/64 = 50.0%** | 64 |
| best-fit siting | 12/24 = 50% | 24 |
| `FWD_GUN_CAP` 3→6 | 32/64 = 50% | 64 |
| heal budget · home turrets | 43% · 42% | 64 |
| rush | 16/64 = 25% | 64 |

**And it is the only arm all day with a positive kill differential at full
power: 33 core kills FOR against 27 AGAINST.**

**⛔ IT IS NOT SIGNIFICANT AND THIS DOCUMENT SAYS SO BEFORE THE LEG, NOT AFTER.
34/64 against a 50% null is p ≈ 0.35.** Two arms today read positive at n=24 and
collapsed to exactly 50% at n=64 (`FWD_GUN_CAP` 58%→50%), and the null itself
read 44% at n=36. **This is a PRIORITISATION, not a result.** The live leg is
being spent because it is the best candidate we have, not because the screen
settled anything.

## 2. THE MECHANISM

**`get_attackable_tiles_from` has ZERO call sites anywhere in the tree.** We never
compute a hypothetical turret's firing pattern, so we neither site into good rays
nor route out of bad ones. The diff enumerates visible enemy **gunners**, takes
their attackable set, and penalises any raid station inside it — reusing the
`threats`/`LOKI_EXILE_PENALTY` machinery that already exists for launchers.

**The engine asymmetry it exploits:** a gunner's shot is a straight line **blocked
by obstacles**, r²=13; a sentinel's **ignores obstacles**, r²=32. **Gunner damage
is avoidable by geometry. Sentinel damage is not.** And rotating costs a gunner
**10 Ti plus a full action cooldown**, so forcing a rotate is a tempo trade in our
favour even when they answer it.

## 3. PRECONDITION — measured, with a correction the research arm made against its own headline

**Exposure-normalised forward builder deaths per 1,000 builder-rounds:**
**US 2.915 · FIELD_pure 0.847 — 3.4×.** That is the attrition claim with exposure
controlled and it does not depend on any killer split.

**⛔ AND THE HEADLINE FIGURE WAS CORRECTED DOWNWARD BEFORE THIS DOCUMENT WAS
WRITTEN.** The first relay said our forward deaths are 91.94% gunner against a
field 42.77%. **That field number pooled games where WE did the killing** — we
are sentinel-heavy, which dragged the field's gunner share down. **The honest
comparison is 91.94% vs FIELD_pure 64.39% = +27.5pp, not +49pp.** The proposal
is unaffected — the diff targets 92% of *our* forward deaths whatever the field's
share is — but the two-fold framing was wrong and is not used here.

## 4. BARS

* **5a DOSE (live) — GATE.** Forward builder deaths per game, ours, and forward
  builds per game. **Treatment must DIFFER from control.** If the raid stations
  do not move, VOID — implementation failure, no claim about geometry.
* **5b MECHANISM.** Forward builder deaths per 1,000 forward builder-rounds.
  *What moves it: the penalty term, and nothing else in the diff.*
* **5c CURRENCY — NOT RESOLVABLE AT THIS n AND NOT CLAIMED.**
* **5d COST.** Forward presence must not fall. If raiders avoid gunner axes by
  simply not going forward, the plank has bought survival by abandoning the
  assault — **that is the falsifier and it is the most likely way this dies.**

## 5. n AND WHAT RESOLVES — gates sized as well as bars

**PROBE: 25 games, one window.** Control: the banked v104 games.

| item | kind | resolves at 25? |
|---|---|---|
| 5a dose | GATE | **YES** — a station shift shows in build/death positions |
| 5b mechanism | BAR | **PARTIALLY** — a large change in death rate, not a small one |
| 5c currency | BAR | **NO. Not claimed under any result.** |
| 5d falsifier | BAR | **YES for a collapse** in forward presence, no for a small fall |

## 6. OBLIGATION 13

```
MECHANISM METRIC READS: bots/_v146gunaxis/raid.py:499
TREATMENT DIFF TOUCHES: raid.py, doctrine.py
INTERSECTION: raid.py
```

## 7. WHAT THIS PROBE MAY NOT DO

No currency claim. No verdict. **It may not be described as confirming the
head-to-head** — 53% at p≈0.35 is not a finding, and one unrated window does not
make it one. It may not borrow any other plank's bars.

---

# AMENDMENT 1 — **THE SCREEN IS SIZED AT 4,096 GAMES. DECIDED HERE, BEFORE ANY RE-RUN.**

**Written 2026-08-11 09:3xZ, after the live window fired and BEFORE any further
head-to-head is run.** ADD-only; moves no bar.

## A1.1 THE ARITHMETIC THAT FORCES A CHOICE

A true 53% effect against a 50% null needs, at 80% power:
```
n=  64   z=0.48   no
n= 256   z=0.96   no
n=1024   z=1.92   no
n=4096   z=3.84   RESOLVES
```
**So re-running at 64 CANNOT EVER SETTLE THIS.** A series of 64-game screens will
keep returning 50% ± 6% forever, and each one will feel like new information.

**⇒ THERE ARE EXACTLY TWO HONEST POSITIONS AND DRIFTING BETWEEN THEM IS HOW A 53%
BECOMES A BELIEF:**
* **size the screen at ~4,096 and say so**, or
* **declare it PRIORITISATION-ONLY and stop re-running it.**

## A1.2 THE DECISION: 4,096, AND IT IS LAUNCHED

**Head-to-head games are free, instant, unlimited and need no rate-limit slot** —
the one resource this project is not short of. **A live window can never buy
4,096 games; the harness can buy them overnight.** That asymmetry is the whole
argument for the instrument and it would be wasted by screening at 64 forever.

**8 maps × both seats × 256 seeds = 4,096 games**, treatment `bots/_v146gunaxis`
vs control `bots/_v130loki13`. **The null control has already been established at
32/64 = 50.0% and will be re-run at the same n for a matched baseline** — a 4,096
treatment against a 64 null would be comparing a tight interval to a loose one.

**PRE-COMMITTED READING, written before the number exists:**

| result at n=4,096 | how it MUST be written |
|---|---|
| CI excludes 50% and above | *"the gunner-axis penalty beats the previous line iteration in self-play at n=4,096."* **Still not a currency claim and still not the field** — self-play is deterministic and one opponent. |
| CI excludes 50% and below | **refuted in self-play.** The live window's games are read on their own bars and the plank is demoted. |
| CI includes 50% | **NO EFFECT DETECTABLE AT 4,096 GAMES.** Not "promising", not "needs more games" — **4,096 was chosen as the resolving n and this is the answer at it.** |

**⛔ AND NO INTERIM PEEK MOVES ANYTHING.** The read is at 4,096. **I have already
seen 34/64 and that is exactly why the final n is fixed here** — the same
optional-stopping problem Amendment 4 of LOKI-19 was written to close, arriving
on the local harness instead of the live ladder.

## A1.3 WHAT THIS DOES NOT DO

It does not touch the live leg's bars — those 25 unrated games are read against
§4 as written. It does not upgrade the plank. **And it does not make self-play the
fixture of record: `FIXTURE_OF_RECORD: live_unrated` is unchanged, and a 4,096-game
self-play result PRIORITISES rather than CLOSES, per D12.**

---

# AMENDMENT 2 — READ-OUT ADDENDUM: THE FALSIFIER AS ONE NUMBER, AND WHAT IT DOES **NOT** CLOSE

## A2.1 THE FALSIFIER COLLAPSES TO A SINGLE RATIO, AND IT NEEDS NO SIGNIFICANCE TEST

The read-out gave two proportions whose near-identity was the signal — deaths
−24%, forward presence −23%. **Two numbers invite an argument about which one
matters. One does not:**

```
DEATHS PER FORWARD BUILD    treatment 12/211 = 0.0569
                            control   32/550 = 0.0582      -2.3%
```
**Exposure-normalised survival is UNCHANGED.** The 24% fewer deaths is bought
**entirely** by 23% less forward presence.

**⭐ AND THIS FORM REQUIRES NO STATISTICS AT ALL: a plank that improves survival
MOVES this ratio; a plank that retreats leaves it flat.** That is the falsifier
as a single quantity and it is the form the read-out should have led with.

*(Provenance and a correction: the side lane derived **−1.2%** from the two
published RATES; computed directly from raw counts it is **−2.3%**. Same
conclusion, and the direct form is the one quoted.)*

## A2.2 ⛔ WHAT THIS KILLS AND WHAT IT DOES NOT — the LOKI-18 distinction, applied before it costs anything

**KILLED: THIS IMPLEMENTATION** — penalising raid stations that sit on enemy
gunner rays, as built. **The penalty makes raiders retreat rather than reroute.**

**NOT KILLED: THE UNDERLYING FINDING.** We die forward at **2.915 deaths per
1,000 builder-rounds against FIELD_pure's 0.847 — 3.44×** — on a proper
denominator that survives the pooling error research corrected against its own
headline. **That number is untouched by this leg.** We still lose builders to
avoidable turret fire at three and a half times the field's rate; **this plank
tried to fix it by going forward less often, and that is a property of the
implementation, not of the road.**

⇒ **STATUS: ONE IMPLEMENTATION REFUTED. The gunner axis is NOT closed.** The
surviving question — untested here and untestable by this design — is **whether a
route exists that holds forward presence at ~11 builds/game while cutting the
death rate.** A penalty term subtracts score from a bad station; it never
proposes a good one. **The version worth building REPLACES the station rather
than taxing it.**

## A2.3 THE 4,096-GAME SIZING: THE DECISION WAS CORRECT AND WAS MADE MOOT BY A BETTER BAR

Both are true and only one is obvious afterwards. **Amendment 1 was right that a
53% needs ~4,096 games and that re-running at 64 could never settle it.** It was
also aimed at the WRONG QUESTION: **a head-to-head win rate cannot see whether a
win was bought by retreating, and the mechanism bar resolved the plank at n=25.**

⇒ **THE GENERAL FORM, worth more than this leg: a well-designed MECHANISM bar
resolves at a sample size a CURRENCY bar cannot reach.** `PROGRAMME.md` already
says `WIN_RATE_IS_VERDICT: no`; this is the power argument for it rather than the
principled one.

**ACTION TAKEN:** the treatment's 4,096-game run is **STOPPED** — it can no
longer change the disposition and it was consuming hours of CPU. **The 4,096-game
NULL is left running deliberately: a properly-powered null is reusable
infrastructure for every future screen, not an artefact of this plank.**
