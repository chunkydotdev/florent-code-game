# THE LADDER PAIRS ON A METRONOME — EXPOSURE COST IS COMPUTABLE BEFORE YOU TYPE THE COMMAND

> ## ⛔ AMENDED IN PLACE 2026-08-15T06:1xZ — FOUR CORRECTIONS, THREE OF THEM AGAINST MY OWN TEXT
> Two peers found these within twenty minutes of publication. **Read this block before §2–§5;
> where it conflicts with the body, this block wins.**
>
> **A1. THE SURFACE I USED WAS THE WRONG ONE, AND THE RIGHT ONE WAS ALREADY IN THE REPO.**
> *(Side lane.)* I read activation windows off `elo_history.tsv` — a **5-minute poll on a LOCAL
> (UTC+2) clock**, which forced a "windows are lower bounds" caveat. **`corpus/ladder_games.tsv` is
> UTC-native, per-match, and granular to the pairing.** Re-run there, **verified by me at the
> primary rather than taken from the relay**:
> ```
> v142  2026-08-14T14:52:59Z .. 15:12:59Z   2 matches   bracketed by v140 pairings 14:32:59 / 15:32:59
> v143  2026-08-14T15:52:59Z .. 16:12:59Z   2 matches   bracketed by         15:32:59 / 16:32:59
> v145  2026-08-14T19:12:59Z                1 match     bracketed by         18:52:59 / 19:32:59
> v146  2026-08-14T21:32:59Z .. 22:32:59Z   4 matches   bracketed by         21:12:59 / 22:52:59
> v147  2026-08-15T04:12:59Z .. 04:32:59Z   2 matches   bracketed by         03:52:59 / 04:52:59
> ```
> **Every foreign run is bracketed by an incumbent pairing on BOTH sides**, so each activation is
> bounded inside one 20-minute gap with no clock conversion and no lower-bound hedge. **The slot
> model holds on all five runs — including v142 and v143, which my `elo_history` windows did not
> separate at all.** That is an independent confirmation of the model, not merely a re-read.
> ⇒ **§3's table is superseded by this one. The "lower bounds" caveat is withdrawn.**
>
> **A2. THE FOREIGN-HOLDER COUNT IS 11, NOT 7 — the 7 was window-scoped and I did not say so.**
> Over **v140's full tenure** (its first pairing `11:52:59Z` → newest, **55 matches**):
> ```
> v140's OWN 44 matches   +38.23   (+0.87/m)
> FOREIGN     11 matches   −39.89   (−3.63/m)     v146 −19.00 · v147 −13.22 · v145 −9.35
>                                                  v142 −0.37 · v143 +2.04  (these two ~free)
> NET over the tenure       −1.66
> ```
> ⭐ **THE SHARPER STATEMENT, and it replaces my headline: over v140's ENTIRE TENURE OUR RATING IS
> FLAT (−1.66) — v140 EARNED +38.23 AND FOREIGN HOLDERS GAVE BACK −39.89.** My "7 matches / −41.57 /
> 57% of the drawdown" is **correct for the peak→now window only** (v142/v143 predate the peak).
> Both windows are right; quoting either without its endpoint is not.
>
> **A3. ⛔ I OVERSTATED A VERDICT-SHAPED SENTENCE. RETRACTED.** §2 said *"on this cut the stop-loss's
> `RULE=held` is the **correct** verdict."* **That reads wider than my cut supports and I withdraw
> the word "correct".** The side lane ran the slot-free windows on ground-truth `ourver`: of the
> **8** windows reaching `net5 ≤ −21`, **4 were contaminated by the v146 cluster and 4 are 100%
> v140's own — including all three most recent** (02:32:59Z −25.1, 02:52:59Z −43.7, 03:12:59Z −35.6).
> ⇒ **The rule freed the slot on genuine v140 bleed as well as on artefacts, and could not tell them
> apart.** The defensible sentence is the narrow one: **`held` is correct *at this moment* (net5
> = +3.0), for a reason the instrument cannot see.** ⚠ **Neither lane has typed the verdict and this
> file does not.**
>
> **A4. THE ATTRIBUTION IS NOW PARTLY CLOSED — AND STAYS OPEN WHERE IT MUST.** v145 and v146 were
> **teammate x3r0's uploads**, documented (`coordination.md:51360`, `:53898`; commits `e06b64eb`,
> `19ec81a6`). **v147's activator is NOT ESTABLISHED** — no document, commit, prereg or log in the
> repo names it; the only signal is circumstantial and is not evidence. **v147 stays unattributed.**
> ⇒ **This is a TOCTOU hole, not lane procedure drift**: x3r0 uploads on no schedule and `fcode
> submit` auto-activates, so a check-then-act sequence has a gap by construction. **That strengthens
> the case for the DETECTION half (record the holder PER ACCEPT) over any further procedure fix.**
>
> **A5. `19m58s` OF CLEAR AIR IS AN US-ONLY SAMPLE** and says so here (side lane's point) — the same
> caveat that should have travelled with the 60-second figure it replaces.


**Research arm, s43, 2026-08-15T06:0xZ.** Surface: `corpus/ladder_games.tsv`, synced 05:58Z,
newest pairing `2026-08-15T05:52:59Z` (4 min old at read). Live holder **v140**, rating **1723**,
1017 matches (`fcode status`, 05:57Z).

**ROUTING:** behaviour change → promoted to `docs/coordination.md` as a FIRE ORDER + cadence plan.
Two clauses of `CLAUDE.md` are **understated by this measurement** and are flagged for Magnus (that
file is his) — see §5. Nothing here is a verdict; the verdict sentence stays the builder's.

---

## 1. THE MEASUREMENT

All distinct rated ladder pairings, `created >= 2026-08-12`:

```
pairings                 234   over 77.7 h
inter-pairing gap        1200 s in 229/233 · 1199 s in 2 · 1201 s in 2   (NO other value)
minute mod 20            12 in 232/234 (99.1%)   13 in 2
second                   :59 in 232/234          :00 in 2
slot fill                3.01 pairings/hour against a theoretical 3.00
```

Tightened to the last 19 hours (`>= 2026-08-14T11:00Z`, n=57): **57/57 at minute ≡ 12 (mod 20),
57/57 at second `:59`, and 56 of 56 gaps at exactly 1200 s.** Zero exceptions.

⇒ **Slots are `:12:59`, `:32:59`, `:52:59` past every hour, and WE ARE PAIRED IN EVERY ONE.**
A slot fill of 3.01/hr against 3.00 means there is no such thing as "we might not get paired this
window" — over 77.7 hours we missed none.

---

## 2. ⭐ THE FIRST CONSEQUENCE: EXPOSURE IS DETERMINISTIC, NOT PROBABILISTIC

Because fill is 100%:

```
leaked_rated_matches  =  number of :12:59 / :32:59 / :52:59 slots
                         between activation and rollback
```

This is arithmetic, available **before** the submit command is typed. It replaces "budget a
prototype leg at roughly −8 Elo per leaked match" (`CLAUDE.md`) with a number you can compute
exactly, from the wall clock alone.

### The measured price of getting it wrong — last 19 hours

Our rating peaked at **1795** (`ourbef` on the `2026-08-14T18:32:59Z` pairing vs arsonist duck) and
sits at **1723.9** on the newest pairing. **35 rated matches, −72.44 Elo.** Decomposed by which
version actually played, off per-match `ourver`:

| ver | matches | sum Δelo | mean Δ/match | game share |
|---|---|---|---|---|
| **140 (incumbent)** | **28** | **−30.87** | −1.10 | 0.471 |
| 146 | 4 | −19.00 | −4.75 | 0.350 |
| 147 | 2 | −13.22 | −6.61 | 0.300 |
| 145 | 1 | −9.35 | −9.35 | 0.200 |
| **non-incumbent total** | **7** | **−41.57** | **−5.94** | **0.286** |

⇒ **57% of the drawdown came from 20% of the matches.**

**⭐ AND THE HEADLINE READ IS THE ONE NOBODY HAS: v140 IS NOT THE BLEEDER.** Over its **full** rated
tenure — 44 matches, 220 games, `2026-08-14T11:52Z → 2026-08-15T05:52Z` — v140 is
**+38.23 Elo net, 53.2% game share, mean(S−E) = +0.0272.** The stop-loss reads `RULE=held` on v140
and, on this cut, **held is the correct verdict** — the drawdown the alarm sits next to was
substantially not v140's to answer for.

⚠ **BOUND ON THAT SENTENCE, stated because it is the load-bearing one:** v140 is +38.23 over its
whole tenure but **−30.87 over the 28 matches since the peak.** "Not the bleeder" is a claim about
the *attribution of the −72*, **not** a claim that v140 has been fine since the peak. Both numbers
are in this file so neither can be quoted without the other.

### ✅ CLOSURE CHECK ON THE DECOMPOSITION — residual 0.0000, run BEFORE publishing

A per-match delta table is worthless if it does not reproduce the rating path, so:

```
window 08-14T11:12:59Z .. 08-15T05:52:59Z (57 matches)
  first ourbef 1736.204  +  sum(deltas excl. last) −12.286  =  1723.918
  observed last ourbef                                          1723.918
  RESIDUAL                                                       −0.0000

peak→now segment (35 matches, the one this finding uses)
  peak ourbef  1794.953  +  sum(deltas excl. last) −71.035  =  1723.918
  observed last ourbef                                          1723.918
  RESIDUAL                                                       +0.0000
```

**`delta = 32×(S−E)` reproduces our rating path digit-for-digit over both windows.** The version
attribution above is a partition of a sum that is itself exact, so the only way it is wrong is if
`ourver` mislabels a match — and `ourver` is 0.00% null across all 5,085 rows (checked).

⭐ **AND IT AGREES WITH AN INDEPENDENT INSTRUMENT BY A DIFFERENT PATH.** My reconstruction gives the
peak→now drawdown as **−71.035**; the side lane's `corpus/ship_watch.log`, derived from the elo tape
rather than from per-match deltas, reads **drawdown = −71.0**. Two instruments, two surfaces,
same number.

⚠ **TWO ENDPOINTS, DO NOT CONFLATE THEM: −71.035 is peak → the last match's `ourbef`. −72.44 is
that plus the newest match's own delta, which has not yet appeared as anyone's `ourbef`.** Both are
correct; they answer "how far have we fallen so far" and "what did these 35 matches cost". The
predicted end rating **1722.51** against `fcode status` **1723** is consistent with the newest match
having settled after the status read.

### Attribution of the 7 — and it is NOT lane procedure drift

`corpus/version_trees.tsv` has **no row for 145, 146 or 147** (it has 140 and 144), so none was a
recorded lane ship. `docs/coordination.md:53898` records **v146's activation as teammate x3r0's**,
and `:54125` puts it at `21:23Z→22:48Z, matches 991→995 ⇒ k = 4`. **A second agent is confirming
v145 and v147 provenance; until it reports, treat their activator as NOT ESTABLISHED.**
⇒ The cost is real and measured; **whose action it was is a separate question and is open.** This
file prices the mechanism, it does not assign fault.

### The windows, against the slot grid

Activation windows read off `elo_history.tsv` (⚠ its `timestamp` column is **LOCAL, UTC+2** —
converted here; a live drift-watch cell):

| ver | window (UTC) | length | slots covered | matches tagged |
|---|---|---|---|---|
| v145 | 19:13 → 19:18 | ≥5 min | 1 | 1 (`19:12:59Z`) |
| v146 | 21:23 → 22:53 | **90 min** | 4 | 4 (`21:32:59`, `21:52:59`, `22:12:59`, `22:32:59`) |
| v147 | 04:15 → 04:45 | 30 min | 2 | 2 (`04:12:59`, `04:32:59`) |

**Every tagged match lands exactly on a slot, and the count equals the slot count. The model is
exact on all three cases.**

⚠ **These windows are LOWER BOUNDS.** `elo_history` polls every 5 minutes, and in two of three cases
(v145, v147) the tagged pairing **precedes** the first poll showing the new version — so activation
was earlier than the table's left edge. This strengthens the finding rather than weakening it.

---

## 3. ⭐⭐ THE SECOND CONSEQUENCE, AND IT IS THE USEFUL ONE: THERE ARE ~19 MINUTES OF CLEAR AIR, NOT 60 SECONDS

`CLAUDE.md` prescribes "a correctly-run window is ~60 seconds" and "do submit→fire→rollback just
AFTER an observed pairing". The second half is right. The first is **19× more conservative than the
tape requires**:

```
pairing at  T = :12:59
clear air   T+00:00:01  ..  T+00:19:59      <- 19m58s, zero rated exposure
next slot   T+00:20:00
```

**And the fixture fits inside it with room to spare:**

| | |
|---|---|
| unrated rate limit | **5 test/unrated matches per 20 minutes** (CLI verbatim, `CLAUDE.md` s28) |
| a match completes in | ~15 s |
| 5 matches + challenge overhead | **~2–4 min** |
| clear air per gap | **~19.9 min** |

⇒ **A FULL 5-MATCH UNRATED LEG — THE ENTIRE RATE-LIMIT ALLOWANCE — FITS IN ONE INTER-PAIRING GAP,
FIVE TIMES OVER.** The rate limit and the pairing cadence have the **same 20-minute period**, so the
natural cadence is exactly **one leg per gap**: activate at ≈`:13:30`, fire 5, verify, roll back by
≈`:25`, and the next pairing at `:32:59` meets the incumbent.

**⇒ THE RATED COST OF PROTOTYPE TESTING IS GENUINELY ZERO WHEN PHASED — and the −41.57 above is
what the same testing costs when it is not.** The binding constraint on throughput was never the
pairing cadence; it is the 5-per-20-min rate limit, which the gap fully absorbs.

⚠ **One thing this does NOT establish:** whether the rate limit's own 20-minute window is
*phase-locked* to the pairing grid or is a rolling window from first use. **I did not measure that
and it does not matter for the plan** — the leg fits either way, because 4 min ≪ 19.9 min. Do not
promote "the two are phase-locked" as an engine fact; the durable claim is only that one full leg
fits in one gap.

---

## 4. THE PROCEDURE THAT FALLS OUT

Replaces "activate only in the instant before firing" with something a lane can execute and a
successor can audit:

1. **Read the last pairing** off `corpus/ladder_games.tsv` — do not guess the phase, derive it
   (`CLAUDE.md` is explicit that the offset has shifted before, and this file's §5 does not retire
   that warning, it only reports that no shift occurred in 77.7 h).
2. **Wait for a pairing to land.** The slot is `:12:59` / `:32:59` / `:52:59`.
3. **Submit + verify holder as a SEPARATE BLOCKING STEP** (the s42 procedure fix — a guard in the
   same command block as the guarded action is not a guard).
4. **Fire all 5 unrated matches.** Budget 4 minutes; you have 19.
5. **Roll back and assert the `Active bot:` line**, never `$?` — exit code is not a health signal
   on this CLI.
6. **Record the holder PER ACCEPT, not per window** (the s42 complement — prevention has a floor,
   detection does not; a contaminated accept must be identifiable by a column afterwards).

**Deadline arithmetic for the lane:** rollback must complete before `:31:59` for a `:12:59` start.
If it has not, the next slot leaks one rated match at a measured mean of **−5.94 Elo** — and that
is now a number you chose, not a number that happened to you.

---

## 5. ⚠ TWO `CLAUDE.md` CLAUSES THIS MEASUREMENT UNDERSTATES — routed to Magnus, that file is his

`CLAUDE.md` currently reads:

> *"55 of 60 consecutive pairings land at minute ≡ 12 (mod 20) and 49 of 60 at second `:59`"* … *"the
> offset **has shifted at least once** inside an 18-hour span, so **re-derive it from recent rows and
> never hardcode it**; and the sample is us-only. The **offset** is the robust part, the 20-minute
> **interval** is not (some gaps are 600 s)."*

Measured over 77.7 h / 234 pairings, `created >= 2026-08-12`:

| claim | current tape |
|---|---|
| 55/60 at offset 12 | **232/234 (99.1%)**; 57/57 in the last 19 h |
| 49/60 at second `:59` | **232/234**; 57/57 in the last 19 h |
| "some gaps are 600 s" | **zero 600 s gaps.** All 233 gaps are 1200 ± 1 s |
| "the interval is not robust" | **the interval is the most robust part measured** |

⇒ **The "re-derive, never hardcode" instruction should STAY** — it is cheap and it is what makes the
plan safe against a future shift. **What is stale is the pessimism about the interval**, and it
matters because it is exactly what justifies a 60-second window instead of a 19-minute one.
⚠ **Both samples are us-only** — that caveat is `CLAUDE.md`'s and it survives intact here.

**Second clause, `CLAUDE.md` on prototype cost:** *"Budget a prototype leg at roughly −8 Elo per
leaked match."* Measured on tonight's 7: **−5.94/match** (range −9.35 to −4.75). The −8 budget is
**conservative in the right direction** and needs no change; recording the re-measurement so it is
not re-derived a third time.

---

## 6. WHAT THIS DOES NOT SHOW

* **It does not price a leg's VALUE**, only its cost. `tools/target_value.py --band` still gates
  which opponent is worth a window.
* **It does not establish who activated v145/v147** — open, agent running.
* **It says nothing about whether v140 should hold the slot.** v140's +38.23 lifetime and its
  −30.87 since peak are both in §2; choosing between them is a verdict and is the builder's.
* **The 100% slot fill is measured on OUR pairings only.** It is a fact about how the ladder has
  treated us for 77.7 hours, not a documented engine guarantee.
