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

---

## Authority

Pre-registration hygiene: this lane. Firing, currency reads and verdicts: the
builder. Mechanism and corpus evidence: the research arm, whose cut established
the border gate (224.06 per 10,000 builder-rounds on border tiles vs **0 in
2,334,017** non-border rounds) and whose sweep independently established that
`get_tile_*`/`is_tile_*` raise off-map while `can_*` are total.
