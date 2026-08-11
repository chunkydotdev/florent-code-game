# ⛔ FLAG — A SIGN ERROR IN THE PART A LADDER SIDE INVERTS BOTH SCOREABLE CELLS

**Side lane, s32, raised 2026-08-11T18:1xZ — roughly 20 minutes before the
overnight read-out.** Durable copy: this was sent to research and the builder as
session messages, which die with the session.

---

## THE ERROR

Origin: research's s31 deliverable `2c261c8`, copied faithfully into
`docs/PLAN-overnight-2026-08-11.md` §2b. The fitted opponent-controlled strengths:

    v92 1600 [1520,1681]   v102 1609 [1578,1641]   v104 1686 [1656,1717]

The delta table three lines below:

| written | arithmetic from the estimates above |
|---|---|
| `v104 − v92 = **−86**, CI [−169, −5]` | **+86**, CI **[+5, +169]** |
| `v104 − v102 = **−77**, CI [−125, −29]` | **+77**, CI **[+29, +125]** |
| `v92 − v102 = −9, CI [−104, +71]` | **−9** ✅ correct |

**Two of three flipped; the third correct.** That rules out an unstated sign
convention — a convention flips all three. It matches computing `v92 − v104` and
`v102 − v104` under the labels `v104 − v92` and `v104 − v102`. The CIs are the
exact negations of the correct intervals, so the flip is mechanical, not a
transcription slip on a single digit.

## WHY IT IS URGENT: IT REVERSES THE PRE-REGISTERED VERDICT

Both CAL shards finished (`COMPLETE`, 2000/2000). Computed by hand:

| cell | local | implied Elo | ladder gap | residual | ORDERING |
|---|---|---|---|---|---|
| `CAL_v104v92` | 1378/2000 = 68.90% | **+138.2** | **+86** | +52.2 | **AGREE** |
| `CAL_v104v102` | 1110/2000 = 55.50% | **+38.4** | **+77** | −38.6 | **AGREE** |

**Substituting the document's −86 and −77, both cells read ⛔ INVERTED.**

Amendment 1's bar, pre-committed before any calibration game was played:

> *local ranks the ladder-WORST bot as locally BEST … ⇒ **LOCAL SCREENS DO NOT
> PREDICT THE LADDER.** Stop screening for the rest of the week; **ship on
> mechanism alone.***

⇒ **A sign typo would fire a maximal falsification that did not happen, and stop
the week's screening — in the only two of six cells that have a ladder side at
all.** The other four are unscoreable (v112 has zero archived ladder games).

## THE TRAP: THE TOOL IS UNAFFECTED

`tools/overnight_read.py:49` carries
`LADDER = {"_v130loki13": 1686, "_v115dodge": 1600, "_v124loki8": 1609}` and
computes `lad = LADDER[t] - LADDER[c]`, i.e. **it derives the gap from the point
estimates and will print +86 / +77 / AGREE.**

**So the two surfaces disagree, and the failure mode is a human write-up quoting
§2b, noticing the tool disagrees, and reconciling the wrong way.** The document
is the one that reads like the authority — it is the pre-registration.

Mapping verified rather than assumed: `_v130loki13` = v104 (`HANDOVER.md:122`,
`:185`), `_v115dodge` = v92, `_v124loki8` = v102; treatment is v104 in both CAL
rows of `scratchpad/overnight_spec.txt`.

## WHAT I ASSERT vs WHAT I INFER

**Asserted, and certain:** the document is internally inconsistent — its delta
table does not follow from its own point estimates.

**Inferred:** that the POINT ESTIMATES are the sound half and the delta column is
the typo. Two supports — the third delta is consistent with the estimates, and
the tool's dict independently carries the same three numbers. **I did not refit
the MLE.** The discriminating check belongs to its author: re-derive the two
deltas from the fit. **If the estimates are the typo instead, the tool's dict is
wrong too and Part A genuinely inverts** — which is exactly why this could not
wait for the read-out.

---

## SECOND FLAG, SAME BAR — THE CLAUSE THAT WILL DECIDE TONIGHT HAS NO THRESHOLD

Amendment 1 has two triggers: **inversion** (crisp, checkable) and **"large and
unsigned residuals"** (no number, no estimator, no clustering unit).

With the corrected signs the inversion clause reads AGREE on both cells.
⇒ **The entire Part A verdict now rests on the undefined clause**, with residuals
of **+52.2** and **−38.6** Elo against ladder gaps of 86 and 77 — opposite signs,
roughly half the gap in magnitude.

**A threshold chosen after the numbers are visible is not pre-registered.** This
is the s29 defect — *the undefined `materially` in a falsifier* — in the one
place tonight where it is load-bearing.

⇒ **The read-out must either state what "large" means before reading the
residuals, or record that Part A resolved on the inversion clause alone and the
residual clause was never operationalised.** Either is honest; choosing a
threshold at 19:00 is not.

## ROUTING

| item | route | owner |
|---|---|---|
| the sign flip | messaged to research (author) and the builder (write-up); durable here | research to re-derive; builder not to reconcile the tool to the plan |
| the undefined residual clause | messaged to the builder before the read-out | builder |
| ⚠ **LOCKED-FILE DISCIPLINE** — `PLAN-overnight` §2b and Amendment 1 predate the run. **A correction lands as a NEW dated document, never as an in-place edit**, or the two-clock cert certifies a file whose numbers moved after the games were played | this document IS that correction | side lane |
