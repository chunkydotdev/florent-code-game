# CERT — the CAL-8 registered read

> ## ⛔⛔ AMENDED 2026-08-14T19:4xZ, AGAINST MYSELF — §1's PREMISE IS FALSE. D2 IS NOT TWO TEAMS; IT IS A **RENAME**, AND THE CELL IS **USABLE**.
>
> **I certified a finding whose premise I did not check.** §1 below endorses
> research's *"cell D2 measures a different team than the reference"* and I
> reproduced everything around it — the cell counts, the sign test, the
> robustness arithmetic — **without ever asking whether the two names were one
> team.** The builder corrected it; I then verified it myself rather than
> inheriting the correction:
>
> ```
> name 'LingLing40'    distinct teamIds = 1   86d0b484…   975 games, last seen 2026-08-14T11:37:21
> name 'lingling_40h'  distinct teamIds = 1   86d0b484…   135 games, first seen 2026-08-14T12:44:52
> DISTINCT teamIds across BOTH names: 1  ->  RENAME (one team), non-overlapping windows
> the runner's D2 id is that id.
> ```
>
> ⇒ **`tools/panel_cal8.sh:27` was CORRECT ALL ALONG.** The panel and the
> reference measure the same team. **D2 is not void.**
>
> **REVISED P4, recomputed by teamId rather than by name:**
> panel D2 = **6/15 = 40.0%** vs reference **13/25 = 52.0%** ⇒ **Δ = −12.0pp,
> BELOW the ≥10pp filter.**
> ⇒ **below 3** (Jython −30.0, Big O −20.0, **D2 −12.0**) · **above 1** · within 2.
> **3 < 5 ⇒ P4 STILL DOES NOT FIRE. THE VERDICT IS UNCHANGED — and it now rests
> on SIX cells rather than five, i.e. on more evidence, not less.**
>
> **WHAT THIS DOES TO §2 AND §3: NOTHING.** The non-contamination ruling, the
> domain-violation ground, the independent re-derivation of the pooled share and
> the holder guard, and the ±3.07pp screen confirmation are all untouched.
> **§1's matched-composition computation is now MOOT** (there was no composition
> mismatch to correct for) — kept below unedited, because it was a correct check
> of the hypothesis as it stood and deleting it would hide that I ran it on a
> false premise.
>
> **⭐ THE REAL DEFECT, AND IT IS SHARPER THAN THE ONE I CERTIFIED: NAMES ARE NOT
> KEYS.** The runner fires by **teamId**; `cal8_read.py` assigns cells by **NAME**;
> the certified reference table is keyed by **NAME**. A team renamed at ~12:44Z
> and the two halves silently desynchronised. **The failure mode is the dangerous
> one: it produced an EMPTY cell, which reads as "no data" rather than as "wrong
> key" — and both I and the read's author took the empty at face value and built
> a defect story on top of it.**
>
> **AND MY OWN STANDING CONSEQUENCE IS VINDICATED RATHER THAN WEAKENED, which is
> the only comfortable thing here:** I wrote *"it is not a certification of the
> COMPARISON until the other side exists **and the JOIN KEY has been checked**."*
> **The join key was exactly the defect — it was a mutable label.** I wrote the
> right rule and did not apply it in the same document. **Promoter's-first-use
> (retro v1.9), third firing this session, and the first one that reached a
> published certification rather than a draft.**
>
> **Tagged:** `KIND: judgement · STATE: auditing · WHOSE HYPOTHESIS: the author's
> I was certifying` — the first instance this session where my error ran toward
> **someone else's** live hypothesis rather than my own, which the v1.2.1 model
> covers only by saying errors run toward whatever hypothesis is live in the
> author's head. **Here the live hypothesis was the one I was auditing, and I
> adopted it instead of testing it. That is Q10's shape — addressing the concern
> as stated rather than as it is.**


**Side lane, s41, 2026-08-14T19:3xZ.** Certifies `docs/research/READ-CAL8-2026-08-14.md`
(research, `3fbf6e4`) against the cert points carried on the tape since the s40
wrap. **This is a certification, not a verdict** — the read is research's, the
plank consequences are the builder's.

## 0. VERDICT

**CERTIFIED.** Every registered cert point is met, and **every load-bearing
number reproduces on an independent path.**

⭐ **The re-derivation deliberately did NOT re-run `cal8_read.py`.** A second run
of the same instrument controls for nothing (drift-watch standing note, four
instances s26). I joined the fires tape's 15 `matchId`s to `meta_join` on `match`,
and — the point of the exercise — **resolved our wins via `game_winner_id ==
<our team id>`, which is a different code path from the `us_side` column their
disclosed bug was in.**

| quantity | research | mine | |
|---|---|---|---|
| ACCEPT rows → games | 15 → 75 | 15 → 75 | ✓ |
| holder guard `ourver` | `{'140': 75}` | `{'140': 75}` | ✓ |
| pooled panel | 34/75 = 45.3% | 34/75 = 45.3% | ✓ |
| per-cell table | 6 rows | reproduced to the digit | ✓ |
| P4 | below 2 · above 1 · **DOES NOT FIRE** | below 2 · above 1 · **DOES NOT FIRE** | ✓ |
| panel half-width | ±15.3pp | ±15.3pp | ✓ |
| reference floor | ±9.1pp | ±9.1pp | ✓ |
| two-fixture | ±17.8pp | **±17.9pp** | see note |

*Note, stated rather than smoothed: the ±17.8 / ±17.9 difference is the rounded
`45.3` vs the exact `45.333` as the p̄ input. Immaterial to a comparison against
|Δ| = 11.5pp, and recorded because a certification that quietly rounds to
agreement is not a certification.*

**Registered cert points, each checked:** STOP-branch clause named in the first
paragraph (not the n=150 branch, whose ±11.3pp interval would have flattered) ·
**both** gaps declared with spans and commits · P4 primary with P1–P3 descriptive
and the ±9.1pp floor sentence adjacent · alpha **0.109** stated non-upgradable ·
A4/A4.1 gate **not entered** · `df54ea7` not re-litigated · rows declared SPENT.

---

## 1. (a) THE ROBUSTNESS CLAIM — CHECKED, AND CARRIED ONE STEP FURTHER THAN ITS AUTHOR TOOK IT

**Their sign-test arithmetic is correct:** best case for NEGATIVE is
`2 + 1 (D2) = 3 < 5`; for MIRROR `1 + 1 = 2 < 5`. **D2 cannot flip P4 in either
direction.** Reproduced on my own run.

**⚠ BUT ONE SENTENCE OF THEIRS IS LOOSER THAN THE REST, AND IT IS ABOUT P1.**
They write that P1's pooled share *"does not depend on cell identity."* **That is
true of computing the PANEL side and it is not true of the COMPARISON** — P1
compares panel against reference, and after the D2 defect **the two sides contain
a different team in one cell.** That is a composition mismatch, and it is
checkable, so I checked it:

```
as read                     panel 34/75 = 45.3%   ref  88/155 = 56.8%   Δ = −11.5pp
mismatched cell dropped
        from BOTH sides     panel 28/60 = 46.7%   ref  75/130 = 57.7%   Δ = −11.0pp
```

⇒ **the matched-composition difference is essentially identical, so their
conclusion stands — and now it stands on a computation rather than on an
assertion.** The distinction matters because the loose sentence would license the
same move on a future panel where the mismatched cell is not this benign.

**Their refusal to substitute a `lingling_40h` reference to fill D2 is correct
and is the disciplined call** — choosing a comparator after seeing the panel is
the exact DoF `R3` closed on this prereg six hours earlier. **D2 is void and
stays void.**

**AND I ACCEPT THEIR FINDING ABOUT MY OWN CERTIFICATION'S SCOPE.** `df54ea7`
certified that the *reference* side totals n=155/88. It could not have caught
that the *panel* fired at a different team, because **the panel side did not
exist when I certified.** Their phrasing is the right one and I adopt it:
**a reference validated alone is half an identity.** ⇒ **standing consequence for
this lane: a certification of one side of a comparison carries an explicit
expiry — it is not a certification of the comparison until the other side exists
and the JOIN KEY has been checked.**

---

## 2. (b) THE BROKEN FIRST RUN — **NOT A SECOND LOOK**, AND THE REASON IS STRONGER THAN THE ONE THEY GAVE

They asked me to adjudicate this precisely because they should not adjudicate it
themselves. **Ruling: the read is NOT contaminated.**

Their own argument — *the fix is forced rather than chosen, and the analysis was
pinned in a certified function before either run* — is correct but incomplete,
because it is an argument about the FIX and the live hazard is about the
TRIGGER.

**THE HAZARD A "FORCED FIX" ARGUMENT DOES NOT COVER: asymmetric debugging.** An
author who dislikes a verdict hunts for a bug and an author who likes it does
not, so *"I found a bug and fixed it"* can smuggle in outcome-dependent effort
even when every individual step is forced.

**⭐ AND THAT HAZARD IS CLOSED HERE BY A FACT IN THEIR OWN DISCLOSURE THAT THEY
DID NOT USE: THE BUG ANNOUNCED ITSELF THROUGH A DOMAIN VIOLATION, NOT THROUGH AN
UNWELCOME NUMBER.** The broken run resolved **`OpenSverige` — ourselves — as our
own opponent**, and produced a "our version" histogram of `49, 13, 58, 226, 21`,
i.e. **opponent** versions. Neither is a surprising value; **both are ILLEGAL
values.** A bug hunt triggered by an illegal value is **outcome-independent by
construction** — it would have fired identically had the broken verdict been
`FIRES`.

That is D31's own catch mechanism (*the only reliable catch is a domain
violation, not a value check*) doing exactly what it was written for, and it is
what upgrades their claim from *asserted* to *verifiable*. **Certified on that
ground.**

*Their refusal to offer the agreement of the two P4 verdicts as evidence of
harmlessness is also correct: two runs of a broken and a fixed computation
agreeing is a coincidence, not a control.*

---

## 3. THE DURABLE FINDING, ENDORSED

> *"an instrument that stops short of the final join has not been certified
> end-to-end, and the uncertified remainder is reliably the fiddly part."*

`cal8_read.py` certified `accepted_match_ids`, `panel_games`, `v125_reference`,
`p4` and `half_width` — **and the error landed in the read-time glue that did the
cell assignment and the holder guard.** The certified core was never wrong.
**This is the strongest single lesson of the read and it generalises past CAL-8:
the boundary of an instrument is where its certification stops, and that boundary
is where the next defect will be.**

**Open and builder-owned (flagged, not edited): `tools/panel_cal8.sh:27` carries
a mislabelled cell** — id `86d0b484…` labelled `# D2 LingLing40` fires at
`lingling_40h`. **Any future panel reusing that id list inherits the defect.**

---

## 4. SEPARATE, AND IT BEARS ON A LIVE DECISION — THE SCREEN BAR CONFIRMED

Research's `SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md`, re-derived by me:

```
local screen, n=1000, DEFF 0.98 (s39 pair-weighted, 124 shards)
  95% half-width = ±3.07pp                          [research: ±3.07pp] ✓
  a reading of exactly 51.0 -> CI [47.9, 54.1]      CONTAINS 50.0
  bar-to-null distance 1.0pp  vs  half-width ±3.07pp
```

⇒ **`SCREEN-v140vs145`'s 51.0 bar cannot exclude the null it tests. This is
precisely the `BAR_RESOLVABLE` failure `prereg_check` was built to catch, on a
LIVE prereg** — which is a considerably more pointed argument for wiring that
tool than my certification of it was.

**Research flagged it BEFORE the number is looked at and explicitly declined to
recommend changing a bar mid-leg. Both are correct** and I endorse both: moving a
bar after the fixture is running is the s28 hazard whatever the motive, and a bar
that cannot resolve is a fact to be REPORTED beside the read, not repaired
underneath it. ⇒ **this belongs in my screen-read cert plan as a mandatory
carried caveat** (`CERT-PLAN-…` B6), not as a reason to alter the rule.
