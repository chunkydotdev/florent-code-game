# PRE-STATED audit criteria — the crash-induction leg, written BEFORE its prereg exists

**Side lane, 2026-08-10 07:0x CEST.** This lane's standing discipline is to state
the audit before the artifact lands, so it cannot be fitted to what gets written.
Crash-induction is queued behind LOKI-13 and its prereg does not yet exist.
**These are the criteria I will audit it against. Committed now.**

**Nothing here is a verdict, a plank, or a prediction of gain.** Under **D12** the
whole road is a hypothesis: the mechanism half is engine-established, the gate is
archive-correlational, and **the weapon has never been fired by anyone in 940
archived games** — which is precisely why it needs the live fixture rather than
another corpus cut.

---

## ⚠ THE BAR AS CURRENTLY SKETCHED IS SET AT ITS OWN NULL. FLAG BEFORE IT IS WRITTEN.

The sketch circulating is: **"≥3/10 undamaged removals within 3 rounds, against
their unconditional first-border-round rate of 947/3,194 = 29.6%; falsifier
0/10."**

**3/10 = 30.0%. The base rate is 29.6%. The bar is the null.** As literally
worded it is a superiority test set at the value it is testing against, and a
result of exactly 3/10 would be indistinguishable from doing nothing.

**But I think the bar is right and its FRAMING is wrong, and the distinction
matters enormously for how a result reads.** The 29.6% is the hazard **conditional
on a builder standing on a border tile**. The throw does not raise that hazard —
**it CAUSES the border-standing that would not otherwise have occurred.** So the
mechanism predicts removals at approximately the natural border rate, and:

- **~30% is CONFIRMATION that the hazard transfers to an induced border-standing**,
  not a failure to beat baseline.
- **0/10 refutes**, because it says an induced border-standing does not carry the
  hazard that a natural one does.

**Required of the prereg: state explicitly that this is a CONSISTENCY test
against a known hazard, not a superiority test against a control.** Otherwise the
first reader — quite reasonably — scores 3/10 as a null. **And name the quantity
the treatment is claimed to move: it is BORDER-STANDING EVENTS CAUSED, not
removal rate.**

### ⇒ SUPERSEDED BY A BETTER DESIGN — adopt the research arm's split-throw control

**My reframe fixes how ≥30% reads. It does NOT fix how anything BELOW 30% reads,
because it smuggles an assumption: that an induced border-standing is equivalent
to a natural one.** The 29.6% population is builders that walked to a border
under their own navigation, plausibly while running the very routine (paving,
routing, edge-following) that performs the fatal off-map query. **A thrown builder
arrives in a different state and may never run it.** So under my version, **any
result strictly between 0 and ~30% is ambiguous** — it cannot separate *"the
mechanism is weaker when induced"* from *"thrown builders are in a different
mode"* — and **0/10 does not cleanly refute either.**

**THE FIX, at zero extra cost, same leg: SPLIT THE THROWS — half to BORDER tiles,
half to INTERIOR tiles.**
- **Holds "being thrown" constant and varies only the border property**, which is
  the causal variable — obligation 11 expressed in the right quantity.
- **The interior arm is a within-treatment placebo that MUST read ~0**, since the
  census gives **0 events in 2,334,017 non-border builder-rounds**.
- **It removes the equivalence assumption entirely:** if thrown builders are in a
  different mode, *both arms are*, so the contrast still isolates the border.
- **And it gives the instrument its own negative control inside the leg** —
  which is what criterion 4 below demands of every instrument here.

**This supersedes my consistency framing as the required design. Adopted from the
research arm.**

## THE CRITERIA — what I will check when it lands

### 1. OPPONENT-CONDITIONALITY MUST BE PRE-DECLARED, WITH NAMES
**The border is not lethal per se: six teams have 722,545 border builder-rounds
between them and ZERO events.** So the leg's targets must be **named before
firing, with the reason each is predicted vulnerable.** A leg fired at an
unselected panel produces a null that cannot be read — "the mechanism is false"
and "we threw at the six immune teams" are indistinguishable after the fact.
**This is the single most likely way this leg wastes a window.**

### 2. TREATMENT OCCURRENCE, MEASURED BEFORE THE CURRENCY (obligation 11 / the LOKI-3 lesson)
**LOKI-3 died having never been dosed** — 16.7% throws against a 30% bar,
measured pre-battery, and stood down. Crash-induction has the same exposure: a
launcher must be built forward, an enemy builder must come within pickup range
(d²≤2), and a border tile must be reachable within throw range (1≤d²≤26).
**Required: throws-onto-border-tiles per game, barred, and checked BEFORE any
currency claim.** If the dose is not reached the leg answered nothing.

### 3. THE CHECK MUST BE IN THE CAUSAL VARIABLE, NOT THE IMPLEMENTATION
Obligation 11 in its original words: *a clean check of the wrong quantity is
worse than no check, it launders an invalid arm as verified.* **The invariant
this hypothesis needs is: "an enemy builder stood on a border tile as a result of
our throw, and then vanished with no damage event accounting for it."** Not "we
called `launch()` N times". **Decode-verified, both halves.**

### 4. THE INSTRUMENT MUST BE THE ONE THAT WORKS
**Replays do NOT capture tracebacks** — established tonight by positive control
(`bots/_probe_crash`: the engine printed 5+ tracebacks to console, the replay
contained zero occurrences of the sentinel). **Any "no crashes observed" claim
built on scanning replays for `Traceback` is void.** The working instrument is
*unit vanished with no damage event accounting for it*, and it must be validated
against a positive AND a negative control before its output is trusted.

### 5. A NULL MUST DECOMPOSE
Pre-registered branches, so no null can be argued away:
- **No throws landed on border tiles** → the leg answered nothing (dose).
- **Throws landed, no removals** → the induced hazard does not transfer. **This is
  the informative refutation and the one worth firing for.**
- **Removals at ~the natural rate** → mechanism confirmed (see the framing flag).
- **Removals but our currency unmoved** → the weapon works and does not pay;
  price it in seat-rounds, per obligation 9's shape.

### 6. THE PANEL PROBLEM APPLIES HERE TOO, AND HARDER
**D11/D13: three of five current panel cells are inert constants.** A
crash-induction leg scored on `core_kill_share` against that panel inherits a
two-cell instrument. **But its mechanism bars are per-game event counts, which
saturation does not touch** — so, exactly as with LOKI-13, **this leg is readable
as a mechanism probe on the existing panel and NOT as a currency test.** The
prereg should say which it is claiming to be.

### 7. NORMS, WHICH ARE NOT A RESEARCH QUESTION
**Crash-induction is adjacent to CPU-timeout induction, which `HANDOVER.md` holds
on NORMS, not evidence — Magnus owes the organisers one question.** My reading is
that these are distinct: a launcher throw is a sanctioned game action and what an
opponent's code does on arrival is its own business, whereas exhausting a shared
clock is a different kind of act. **That reading is mine, it is not authoritative,
and the prereg should not assume it.** If Magnus wants both questions asked
together, this leg waits.

**AMENDMENT 2026-08-10 (research sweep 21, `5faa99a`): the norms premise is
NARROWED, and it cuts toward "ask Magnus first", not away.** My reading above
leaned on "no comparable league bans degrading the opponent bot." That is no
longer clean: **Battlesnake's Code of Conduct bans "exploiting the engine or API
with the intent to interfere with the performance of another person's
Battlesnake" — engine/API level, and the test is INTENT** (caveats: competitors
self-host; the clause is in `policies/`, not `rules.md`). Per-league now:
SSCAIT/BASIL score it an ordinary loss, AIIDE/SC2 engine-and-ladder only,
**Battlesnake bans it by name**, Lux/Halite/Terminal silent, **ours silent**. A
launcher throw remains a sanctioned action — but "what their code does on arrival
is their business" is exactly the intent-shaped argument Battlesnake's clause
reaches. **The distinction I drew is weaker than when I drew it; Magnus's
organiser question is more load-bearing, not less.**

### 8. MEASUREMENT CONTAMINATION — the carrier list has the crash-win problem (research sweep 21)
The carrier rates this leg targets (`vjg` 96.1%, `S` 89.1%, …) are computed over
archived games. **Any opponent-behaviour rate computed over games where that
opponent was CRASHING is measuring the crash, not the opponent** — documented in
the wild: learning bots converged on crashing Steamhammer with NO INTENT because
the engine scored the crash a win, while PurpleWave (which shut Steamhammer out
anyway) never learned to, because every game was already a win. **This is the
carrier-list problem's own shape: a rate contaminated by the very failure it is
measuring.** Consequence for the leg: **the carrier percentages must be read as
"how often this team ends up on a border-death", NOT as a clean base rate the
throw improves on** — and the split-throw interior arm is what protects against
it, since both arms draw from the same contaminated population. **The
prerequisite corpus cut research proposes** (does an enemy unit's action-idleness
over N rounds predict a crash, per team, with `self_destruct()` as the confound
control) **is the right next step and is zero-risk during the outage** — it also
answers this doc's open question, "how would we know the throw worked", by
building the LIVE detection surface the disappearance signature does not give us.

---

## Authority

Pre-registration hygiene: this lane. Firing, currency reads and verdicts: the
builder. Mechanism and corpus evidence: the research arm, whose cut established
the border gate (224.06 per 10,000 builder-rounds on border tiles vs **0 in
2,334,017** non-border rounds) and whose sweep independently established that
`get_tile_*`/`is_tile_*` raise off-map while `can_*` are total.

---

## STATUS UPDATE 2026-08-10 11:1x — CRASH-INDUCTION APPROVED; criteria now LIVE

Section 7's norms hold is LIFTED. **Magnus asked the organisers and APPROVED
crash-induction** (46e407a; CLAUDE.md point 0). So LOKI-14 (`_v131loki14`) is
unblocked; its leg-prereg is owed before fire, and **the criteria above are now
the live audit standard for it** — the split-throw within-leg control
(border/interior), carriers named in advance, treatment-occurrence pre-battery,
and the consistency-not-superiority bar framing. Section 7's "this reading is mine
and not authoritative" is moot: Magnus made the call.

**The boundary that replaced the hold, and it is now a drift rule (D17):**
per-instance exploits within an APPROVED class fire under standing permission;
a genuinely NEW exploit CLASS needs a Magnus→organisers norms question first,
because a league can rule a whole class out of bounds. "Ask again for a new
CLASS, never per instance."
