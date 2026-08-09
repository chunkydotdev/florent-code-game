# Ship gate (Magnus, 2026-08-08 ~19:40 — supersedes the 2026-08-07 field-battery gate)

## The gate

**Ship when: no measured local regression (PARITY PASSES) + an available window
+ nothing known-broken.**

Field evidence for an unshipped head is **not owed** — it is structurally
unobtainable on this platform (`fcode submission download` is own-team-only;
`fcode match test` takes two local dirs; unrated challenges run the ACTIVE
submission). Demanding it was a gate with no gate-opening move.

## Why it changed

Audit at 19:40: the project peaked at 1625 Elo / rank #21, then lost **57 Elo
and 9 ranks in 15 hours with ZERO ships** while five planks sat in KEEP-dev.
Measured signature of the deadlock: ship cadence 0.79 → 0.46/hr, committed
doc:code churn 0.14 → 1.88, eleven straight hours of zero bot lines.

**Rigor that cannot terminate in a decision is a cost, not a virtue.** The
failure looked *more* rigorous the whole time it was happening.

## How to apply

- **Ship the biggest available change per window.** A window is ~8 matches ≈ 1h;
  the team gets ~10-12 evaluated ships/day. **Windows are the scarce resource,
  not code.**
- **State debts on the tape row rather than holding for them.** An untested
  prediction or a known single-map regression is a row line, not a blocker.
- **Identity / 0-flip controls stay MANDATORY.** They are how a plank ships
  without regressing the 14 maps it never meant to touch. This is the one part
  of the old rigor that pays for itself every time.
- **Probes are attribution-only now, never gates.** (Fleet state 2026-08-08:
  orizon valid; band valid rush-mode-only; kladde and flotte need re-freeze;
  cad disclaimed.)
- **A plank that stays KEEP-dev through two windows is refuted by neglect —
  close it.**
- Safety comes from the [slot swap rule](../elo_history.tsv) — rolling last-5
  arms at holder-match ≥8, **net ≤ −21 frees the slot** (threshold recalibrated
  2026-08-09, see the amendment below — the original ≤0 was measured firing on
  a coin flip), rollback is one click. **The rule's implementation and this
  sentence change together or not at all** — four incompatible versions of it
  circulated for a day, and one of them was live in the monitor.

## What did NOT change

Self-legs remain attribution-only **in both directions** — parity is not a
reason to hold, and a good det number is not a field claim. "0 flips" still
means *no outcome effect measured*, never *no effect*: pair it with the
delivered-titanium delta `tools/det.py` now reports.

## AMENDMENT 2026-08-08 21:1x — "ship the biggest available change" was a workaround, and its premise just changed

This document told you to **ship the biggest available change per window**. That
was correct *given* an instrument that could not resolve a single plank — and
that premise no longer holds. Put the two capacities side by side:

| | throughput | parallel? | utilisation |
|---|---|---|---|
| local eval | ~2,150–5,000 matches/hr | yes | underused (headroom is real but bounded: **10 cores**, measured load ~10 under two batteries — the "50-100×" first written here was inherited from a 16-core assumption nobody verified; corrected 2026-08-09) |
| ladder window | ~1/hr, ~8 matches | no | fully saturated |

**Bundling was a workaround for the underpowered instrument, not for the scarce
window.** At n=800 legs of ~22 minutes you can resolve roughly **three planks per
hour locally** and spend the window on the one that won — getting attribution
*and* a pre-validated head from the same window, instead of a 7-plank bundle
that cannot be decomposed afterwards. v81 and v83 both shipped as bundles for
exactly the reason this amendment removes.

**So the gate changes as follows:**

- The window remains the scarce resource. That part was right.
- **Stop spending it on unresolved candidates.** "Parity passes" was the correct
  rule when parity was all the instrument could ever say; now parity at n=120 is
  a statement about our sample size, not about the plank (see `leg-power-19pct`:
  19% power against a true +5pp change).
- **Raise the standard head-to-head leg toward n=800**, and on deterministic
  legs read the **distinct-shape ratio** first — power is nominal until divided
  by it (`shape-ratio-power`).
- Prefer **one resolved plank** per window over a bundle. Bundle only when the
  planks genuinely interact.

What does NOT change: the ladder is still the field instrument, rollback is
still the control, and field evidence for an unshipped head is still
unobtainable. Shipping still beats paralysis — that call was right and the
57-elo deadlock is what the alternative cost. The instrument was simply the
cheaper fix, and it still is.

## AMENDMENT 2026-08-09 12:4x — process-review adoption (Magnus approved; implemented by the side lane)

Four changes, each from a measured incident in
`docs/research/builder-process-review-2026-08-09.md`:

**1. The founding premise of this document is corrected.** The header above
says the project lost 57 Elo in 15 hours "with ZERO ships." The instrument
audit (`docs/workflow-analysis/instrument-audit-2026-08-08-late.md:217-238`)
shows the active submission over that window went v72 → v73 → v74 → v75 → v76
→ v77 → v78 → v76 → v79 → v80 → v81 — **ten slot changes. The −57 Elo was
earned by ten different binaries, not by one binary sitting still.** The
gate's conclusion (ship > paralysis, rollback is the control) stands on its
other legs; its origin story does not. Read the deadlock as "unresolved
candidates + an underpowered instrument," not "no shipping."

**2. The safety rule is ONE statement, magnitude-based.** Rolling last-5 net
Elo, arming at holder-match ≥8 (unchanged), threshold **≤ −21 (−1 sd of the
rolling-5 sum; per-match sd 9.25 measured over 302 increments)** frees the
slot. Never forces a swap. `workflow-analysis/v3` measured the old ≤0
threshold as a timer, not a control: 50.4% fire rate on a *neutral* holder at
match 8, 78.6% on a genuinely +60-Elo holder by match 20. At −21 all three
real tape cases come out right: the v79 rollback (−43.9, the one trigger a
human acted on) still fires; both v80 crossings (−19, −12, both overridden)
go silent. Implemented in `tools/monitors/elo_logger.py` in the same commit
as this text — **doc and tool change together, always**. Two prior
statements are void: s19's "2 sd = −41" (announced adopted, implemented
nowhere) and "≤0 after 3 matches" (a misquote that circulated at s23).
Known residual defect, accepted: re-testing every match with no multiplicity
correction still drives P(fire)→1 on long tenures — the real fix is a
ladder-side SPRT (`tools/sprt.py` has the machinery, bounds like [−10, 0]);
queued, not blocking.

**3. The slot is a STOP-LOSS and a WAKE PATH, not an evaluation instrument.**
The audit's arithmetic: 46 slot runs, mean 6.9 matches, median 5, 27% ever
reached 8; an 8-match window resolves ≥9.2 Elo/match against an all-version
spread of 12.0; three of five window closures on the audited night were not
the session's decision. Of the audit's two consistent options (cap ship
cadence so windows can arm, or stop describing the slot as evaluated), **the
project adopts the second**: evaluation happens BEFORE the ship (resolved
n≈800 local legs per the amendment above, S5 unrated fidelity per
`docs/research/test-process-proposal-2026-08-09.md`) and AFTER it (corpus
production read, unrated fixture re-reads). The ladder hold answers exactly
one question — "is this version bleeding?" — via the recalibrated swap rule.
Do not write "confirmed on the ladder" at n<40; the phrase for a survived
hold is **"held N matches, stop-loss silent."**

**4. Tape-row requirements for every ship row** (the forcing-function half of
the test-process proposal, adopted): `S5_unrated:` (result, or the one-line
skip reason), `treatment_occurrence:` (local count / unrated count), and the
**join key** — both the version tag AND the bot directory (`vNN` +
`bots/_xxx`) in the same row. The join-key rule exists because only 4 of 61
historical gate rows can be joined to their ladder outcome, which is why
"does the local gate predict Elo?" is still unanswerable. `tools/preflight.py`
refuses the ready-to-ship line while any of the three is missing.
