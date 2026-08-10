# SIDE LANE RETRO — s28, 2026-08-10

**Written because the research arm noticed the generic wrap never asks whether a
lane was USEFUL** — it is a lane-agnostic failure log. This is the same six
questions applied to the drift-watch lane, whose failure modes are not theirs.

## 1. CONSUMPTION — were the flags acted on, or filed?

**Acted on, nearly all within minutes.** Flags that changed an outcome:

| flag | what it prevented |
|---|---|
| watchdog counts cycle NUMBERS, cycle 1 banked zero | a leg stopping at ~120 throws against its own 150 gate → ANSWERED NOTHING |
| stop rule cut the dose; the ≥5 bar is now misleading | the modal outcome (3) being written as a null while proving the mechanism (Amendment 7) |
| panel3's abort test was panel2's, cited not run | an unattended 6h runner whose only guard had never fired |
| MDE computed on a post-hoc denominator | 21.7pp quoted as the fixture's resolution; true 19.5pp |
| dead-path OR broken-guard? name the test | **inverted two plank decisions** and exposed a metric that was wrong, not a bot |
| validate the new decoder against LOKI-16's own games | a real mechanism retired on a sign-flipped instrument |

**Unconsumed: none that mattered.** Two cosmetic flags (`target_value`'s missing
date column, its id-vs-name input gap) were raised, deprioritised on Magnus's
time directive, and stayed dropped — correctly.

## 2. LATENCY — did the flag beat the decision it bore on?

**Mostly yes, and that is the whole product.** The dose-gate flag landed ~40 min
before the wrong stop would have fired; Amendment 7 landed before the leg
decoded; the decoder-validation flag landed before +0.017 was read as a plank
failure. **The lane's value is almost entirely in this column** — the same flag
an hour later is a post-mortem, not a save.

## 3. THIS LANE'S UNIQUE FAILURE MODE — **INFERENCE PUBLISHED AS FACT**

Research's is relay fidelity (they compress agent output at scale). **Mine is
different: I read primaries directly, and three times today I published a
conclusion the primary would have contradicted, when checking cost seconds.**

* *"+64 doubles the reachable ceiling"* — the band was already us−80..us+125.
* *"`CORE_PAIRS` contradicts the platform"* — tested a table against a FORMULA,
  not the engine. Our table was right; the "fix" would have broken a live map.
* *"the builder edited a live script and got lucky"* — the pid had changed
  (4404→6659, a restart). **Published about another lane, in a durable record.**

**A timestamp, a formula and an inconsistency each licensed an inference. All
three were checkable. None were checked before publishing.**

## 4. DID MY OWN CHECKS EVER FIRE ON ME? — **partially, and the number is bad**

The drift monitor fired on my own commits all day, but only ever as
notification — **it never made a substantive catch on my own work.**
**3 of my 8 misses were caught by other lanes**, not by me: the poll-time
`ourver` tag (builder), the LOKI-16b missing n (builder), the clobbered
`PROGRAMME.md` fields (builder). **A watch that audits three lanes and catches
its own faults least often is worth saying out loud.**

The rules that DID catch me were mine, applied by me: the arithmetic that did
not sum caught the `meta_join` shortfall; re-deriving instead of adopting caught
the Ouroboros discrepancy (which then turned out to be my own error).

## 5. WHAT I DECLINED, and why declining was the deliverable

* **Killing the leg runner myself** — a blind `pkill` landing mid-cycle leaves
  the prototype live, which is the s27 contamination arriving from a new
  direction. Gave the builder the boundary-safe command instead.
* **Editing `PROGRAMME.md` on my own relay of a Magnus directive** — the builder
  refused it first and was right; I then over-read a QUESTION as an
  authorisation and had to correct the spec against myself.
* **Every verdict.** Routed three to the builder, including two that were
  signed to me.

## 6. WHAT EACH LANE GOT, AND DID IT SURVIVE?

**Builder:** ~15 flags, all resolved same-session; three became tools
(`claim_check`, the target-value gate as a SCRIPT not a template line, the
band-admission argument). **Survival: high — the mechanised ones cannot rot.**
**Research:** the discriminating test for the weakness confound, the
denominator-beside-every-zero requirement, the reachability re-derivation
(confirmed their ±60 to the digit and caught one internally inconsistent number).
**Magnus:** the currency spec, the shutdown checklist, H1's falsifier, and the
closing count — **12 instrument defects against 1 plank that failed on merit.**

## THE HONEST LEDGER

**Prevented: ~6 bad outcomes**, two of which (the dose gate, the decoder
validation) would have destroyed a leg's meaning rather than merely cost time.
**Caused: 1** (clobbered machine-readable fields via a read-modify-write race).
**Nearly caused: 1** (the `CORE_PAIRS` "fix" would have broken a live pool map).

**The lane paid. Its failure mode is now named and is not the one the generic
wrap would have found** — a failure log records what broke; it never asks
whether the auditor's own claims were checked before publication.
