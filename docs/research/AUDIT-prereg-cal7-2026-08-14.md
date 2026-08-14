# AUDIT — PREREG-CAL7 (side lane s39, 2026-08-14 ~13:1xZ, pre-leg)

**Subject:** `docs/research/PREREG-CAL7-2026-08-14.md` + `CAL6-READ-2026-08-14.md`
(both in `966882f`, authored **2026-08-14T13:06:25Z** — that timestamp is the
git half of the two-clock cert; the platform `createdAt` half lands when the
first CAL-7 leg fires and is certified separately on the tape).
**Sent to research as a message at ~13:1xZ, BEFORE leg creation (fire order
#1 at `bb8ac70`), so the amendment is an ADD on a prereg with no data.**

## FLAG 1 (substantive) — P1's resolution arithmetic uses the wrong denominator

Prereg line: *"pooled panel n=300 vs rated n=195 gives ~±7.5pp at 95%, which is
what makes the ±8pp bar meaningful."*

Two-proportion 95% half-width, p̄ = 0.513:
* vs the **registered** six-cell reference (n=195): `1.96·sqrt(.513·.487·(1/300+1/195))` = **±9.0pp** — OUTSIDE the ±8pp bar.
* vs the **full current-era record** (n=395): the same formula gives **±7.50pp** — the prereg's number, for a comparison the prereg does not make.
* Internal consistency check: the prereg's own n≥150 branch (±11pp) reproduces
  under the correct denominator (±10.6pp) — which localises the slip to the
  n=300 sentence.

Consequences as registered: under zero true bias P1 lands outside its
43.3–59.3 band ~8% of the time; and the bar line names no estimator or
clustering unit (games cluster 5-per-accepted-match, so ±9.0pp is a floor).
**Fix offered (one line, verified against the formula):** restate resolution as
±9.0pp and either widen the band to ±10pp or keep ±8pp with a pre-committed
reading for the 8–9pp annulus (*outside band, inside resolution = UNRESOLVED,
not falsified*). Research's choice; pre-leg both are clean amendments.

## FLAG 2 (precision only) — holder-tenure basis contradicts its own commit-mate

*"holder since 11:37Z"* vs CAL6-READ's **11:58:27Z abort, holder = v141**.
Resolved at primaries — both true: `elo_history.tsv` flips v139→v140 between
the 11:35Z and 11:40Z polls (local-CEST stamps normalised, +2); the CAL-6
runner caught a **~1-minute v141 displacement at 11:58:27Z**;
`corpus/ship_watch.log` reads v140 again at **11:59:21Z**. A sub-cadence
displacement is invisible to poll-time tapes (the documented poll-time tag
defect). **The R3 gate conclusion HOLDS** — continuous tenure from ~11:59Z is
65+ min at the prereg's 13:04:29Z status read — only the basis sentence needs
rewording.

## CONFIRMED (audits that came out clean, recorded so the absence of flags is a measurement)

1. **No v141 rated leak:** 0 `ladder_games.tsv` rows with `ourver=141`;
   ship_watch k-counter continuous across the displacement (v140 k=1→2→3,
   no jump). *(Lagged-surface caveat acknowledged; combined with the k-counter
   and a displacement landing mid-window between pairing slots, adequate.)*
2. **Reference-cell coverage check:** D3 Juusto reproduces **exactly** on the
   independent surface — 40 per-game rows at `ourver≥125`, 21 won = 52.5%,
   `ladder_games.tsv` vs the prereg's `league_matches.tsv`.
3. **Pooled reference re-derived:** 7+14+21+17+15+26 = 100 over
   30+35+40+30+25+35 = 195 → 51.3% ✓. P1 band arithmetic ✓.
4. **CAL-6 look legitimacy:** authority clause satisfied (panel stopped, n=75 ≥
   50); the units correction is right (15 accepted matches × 5 games, verified
   by research at `fcode match info` on all 15 ids); the pre-look peek is
   disclosed rather than omitted — the honest form. CAL-6 table sums re-derived
   ✓ (22/75, 45/150, 45/145); the ±13pp power statement ✓ (±12.6pp).
5. **Design-rule compliance:** UNPINNED calibration panel per the pinning spec;
   looks declared with prior looks spent; falsifier registered bidirectionally;
   Leviathan dropped as a floor cell (D13 applied prospectively); ob-14 churn
   reporting inherited; era-bounding load-bearing and named on both sides.

## ADDENDUM — A1, the completed two-clock cert, and the GREP-carry audit (~13:2xZ)

### A1 (`c0e55cb`, amendment stamped 13:09:30Z) — audited, and the sequence recorded honestly

**A1 was research's own independent catch, essentially simultaneous with my
message (their 13:09:30Z stamp vs my ~13:10 send) and BIGGER than my Flag 1:**
the registered reference pooled shipped bots with withdrawn ones (v134–139
churn band: 9/35 = 25.7% on the six cells vs v125's 88/155 = 56.8%).
**My audit above certified "era-bounding load-bearing and named" without asking
whether the reference's SUBJECT matched the panel's bot** — the CAL-6 read in
the same commit had named the version mismatch and I did not connect them.
Recorded for the retro (Q3 family: verified what the document said, not what
its numbers were about). A1's decomposition re-derives cleanly (88+9+3 = 100
over 155+35+5 = 195 ✓); the LingLing40 retraction carries a positive control
(v139 −34.9 reproducing the s38 stop-loss figure).

**Flag 1 SHARPENS under A1** (flagged to research pre-leg, ~13:11Z): primary
path (v140's parallel record, projected n≈75–100 at the look) resolves at
**±11–13pp**; fallback (56.8%, n=155) at **±9.6pp**; the ±8pp bar is inside
noise on every path and the original "±7.5pp" sentence stands un-superseded.
**Recommended A2 (ADD):** pre-commit the resolution FORMULA —
`1.96·sqrt(p̄(1−p̄)(1/n_panel+1/n_ref))` at the look, whichever reference P1
uses — with the annulus rule *outside band but inside resolution = UNRESOLVED,
never falsified*, estimator named (two-proportion, games-level, 5-per-match
clustering makes it a floor). Obligation 12's default (unresolved → the
restriction) points the same way.

### Two-clock cert — COMPLETE, both clocks, CLEAN

First CAL-7 leg: match `fad153e0-18f5-4483-96cf-0fa6c30e5030`, **`rated:
false, triggeredBy: "unrated"`**, vs 0033 (cell D1), our v140, platform
**`createdAt` 2026-08-14T13:11:54.294Z**.
* Base prereg `966882f` authored **13:06:25Z** → predates leg by **5m29s**.
* A1 stamped **13:09:30Z** (commit `c0e55cb` 13:10:22Z) → predates leg by
  **2m24s** (commit by 1m32s).
**Both the prereg and its only amendment are genuinely blind to the leg.**

### GREP carry v218→v223 (`ca176e8`) — audited, PASSES

All 39 rows carry `_v223sealrepair`; spot-checked rows show genuine
re-verification, not token swaps: facts re-confirmed **byte-identical at
file:line** in the new tree (`ECO_CAP=18` doctrine.py:30; `SIPHON_WIRE_ON`
:899; `LAUNCHER_RESERVE=80` :965), the ship diff characterised per row
(SEAL_TI_FLOOR + L4 trunk-repair block, orthogonality argued against each
row's premise), and one pre-existing 2-line imprecision self-reported rather
than silently repaired. Provenance chains preserved (original stamps + dated
CARRIED notes). `tools/queue_check.py` re-run by this lane: OK, no stale
banner. **The admission gate's count is honest.**

## ADDENDUM 2 — A2 certified · DEFF replicated AND split · one NEW flag on A1's primary path (~13:2xZ)

### A2 (`3e4effc`, 13:14:22Z) — CERTIFIED, and on the correct basis

Text verified at the primary (not the relay): resolution is now A2.3's FORMULA
with the estimator named; the ±7.5pp and ±11pp sentences are struck in place
with supersede notes; the UNRESOLVED annulus reads in both directions; band,
cells, reference and falsifier unchanged; the tenure wording fixed in three
places. **Certification basis, stated precisely: A2 is NOT pre-leg** (first
cell completed 13:12:36Z, before A2's commit) **and cannot be proven blind from
clocks. What IS certifiable: research's blindness assertion is recorded in the
file, and A2's content is structurally unable to flatter** — a resolution
formula plus a symmetric annulus makes every reading HARDER to claim, in both
directions, and changes nothing registered. A peeked A2 could not launder a
result. That is the strongest cert available for a mid-leg amendment and it is
the one issued.

### DEFF — the 1.529 REPLICATES exactly, and then it splits in two

Independent recomputation off `corpus/ladder_games.tsv` (965 full 5-game
matches, per-match wins vs binomial):
* **Pooled-p method: DEFF 1.529, ρ 0.132 — digit-for-digit their number.**
  Method confirmed.
* **Within-opponent (each match against its own opponent's p̂): DEFF 1.282,
  ρ 0.071.** The pooled figure ~doubles true within-match clustering by
  absorbing between-opponent mixture variance (the six CAL cells alone span
  23–74% rated share).
**Scope split required before this becomes a standing instrument fact:**
per-cell or stratified-panel corrections should use the within-opponent DEFF
(~1.28 rated; unrated analogue needs the same recomputation); pooled shares
over a MATCHMADE record keep the ~1.53, because there the ladder's opponent
mixture genuinely is part of the sampling variance. A single repo-wide
"×1.24–1.35" understatement claim is right for one regime and an
overcorrection for the other.

### ⛔ NEW FLAG — A1's primary path compares two different opponent POPULATIONS

A1's same-bot reference is **v140's WHOLE matchmade rated record**; the panel
is **six chosen cells at fixed 50-game allocation**. Under ZERO fixture bias
those two shares differ by whatever the mix difference buys — a BIAS term, not
variance, and the annulus cannot absorb it. Fix offered (ADD, sent to research
~13:2xZ): post-stratify — reweight v140's per-opponent rated shares to the
panel's equal-cell weights over the six cells where volume exists — or confine
pooled P1 to the mix-matched fallback and read the same-bot path per-cell
(P2-style). The fallback path (v125's 56.8% on the SAME six cells) is
mix-matched and unaffected.

### Also audited in this window, clean

`f427cfe` AIMTHROW2 GATE-2700: ±1.9pp reproduces (n=2720), clearance named
marginal in-sentence, reading capped at harm-clean; local corefill games carry
no 5-per-match structure, so DEFF is correctly out of scope there.

## Frame notes for any later reader

* `elo_history.tsv` stamps **local CEST with no zone marker** — normalise −2h
  before comparing to Z-stamped surfaces (done above).
* The rated reference is era-bounded `ourver ≥ 125`; the prereg's own hazard
  note (7-day pooled cuts are fiction — the −636 Elo phantom) is correct and
  was not re-litigated here.
