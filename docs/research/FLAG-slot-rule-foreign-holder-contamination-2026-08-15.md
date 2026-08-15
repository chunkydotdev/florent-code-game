# FLAG — THE STOP-LOSS COUNTS MATCHES THE HOLDER DID NOT PLAY. ROOT CAUSE IN THE CODE, AND IT IS THE THIRD ITERATION OF A DEFECT THIS CODEBASE HAS DOCUMENTED TWICE.

**Side lane, s43, 2026-08-15T06:07:11Z (`date -u`).** Surface: `corpus/ladder_games.tsv`
(per-match `ourver`, synced 05:58Z, newest pairing 05:52:59Z) and `tools/slot_rule.py` /
`tools/monitors/ship_watch.py` / `tools/slot_denoms.py` at `HEAD` = `e1ed9af0`.

**⚠ ATTRIBUTION FIRST, because half of this is not mine.** The DECOMPOSITION of the drawdown
is **the research arm's**, published at `7afea75d` /
`docs/research/FINDING-pairing-metronome-and-exposure-cost-2026-08-15.md` — *−41.57 Elo of the
−72.44 fall from peak came from 7 matches out of 35, i.e. **57% of the drawdown on 20% of the
matches***. I computed it independently before reading their note and got **−41.6 of −71.0
(59%) on 11 of 55**; the spread is endpoint convention (they count matches from the peak, I
count deltas between consecutive matches, and I drop the final match which has no successor).
**Same object, two lanes, no coordination.** What follows is what I have that they do not.

---

## 1. THE ROOT CAUSE IS FOUR LINES OF CODE AND IT IS NOT ABOUT THE DRAWDOWN COLUMN

`tools/slot_rule.py:101-112`:

```python
def holder_rows(tape, version=None):
    ...
    tag = version or parsed[-1][3]
    return tag, [(ts, r, m) for ts, r, m, v in parsed if v == tag]
```

```python
def evaluate(...):
    tag, rows = holder_rows(tape, version)
    ...
    holder_start = min(m for _, _, m in rows)      # :121
    ...
    armed = (matches - holder_start) >= ARM_AFTER  # :130
    k = matches - holder_start                     # :134
```

**`holder_rows` filters on the poll-time tag with NO contiguity segmentation, and
`holder_start` is the GLOBAL minimum** — the match count at the version's *first-ever*
appearance. **A version that holds the slot in non-contiguous windows therefore has every
intervening match counted into its own tenure**, including matches played by a different
submission entirely.

**This is not confined to the drawdown column.** Everything downstream of `st.rows` /
`st.k` inherits it:

| field | defined at | inherits the defect |
|---|---|---|
| `k` | `slot_rule.py:134` | ✅ |
| `armed` | `slot_rule.py:130` | ✅ |
| `net5` / `base5` | `slot_rule.py:126-129` | ✅ (the 5-match window can span a foreign run) |
| `peak` | `ship_watch.py:131` | ✅ (max over `st.rows`) |
| `drawdown` | `ship_watch.py:197` | ✅ |
| `dd_z`, `k_dd` | `ship_watch.py:161-163` | ✅ |
| `resolvable_k` | `ship_watch.py:164-166` | ✅ |
| `p_null` | `ship_watch.py:167` | ✅ |

**`net_act` is the ONE field that is already immune**, because it is derived through
`slot_denoms.activation_baseline()`. That is the whole point of §3.

## 2. THE MAGNITUDE, ON THE GROUND-TRUTH PRIMARY

Per-match `ourver` from `corpus/ladder_games.tsv`, span = v140's first match
(`2026-08-14T11:52:59Z`, `ourbef` 1724.2) → newest (`2026-08-15T05:52:59Z`, `ourbef` 1723.9):

    ourver   matches   rating moved
      v140        44         +39.6
      v142         2          −0.4
      v143         2          +2.0
      v145         1          −9.4
      v146         4         −19.0
      v147         2         −13.2
    -------------------------------
    FOREIGN        11        −39.9      (20.0% of the reported k)
    v140's own     44        +39.6

**`ship_watch` reports `k=54`/`k=55` for v140. Eleven of those matches were played by a
different submission.** Over exactly the span the stop-loss attributes to the incumbent,
**the incumbent is +39.6 and the eleven matches it did not play are −39.9.**

**The peak itself is legitimately v140's** — 1795.0 at `2026-08-14T18:32:59Z` carries
`ourver=140`. It is the FALL that is shared: of −71.0, **−41.6 (59%) accrued in 7 matches
v140 did not play** and −29.5 in its own 27.

## 3. ⛔ THE FIX ALREADY EXISTS IN THIS REPO, ONE MODULE OVER, AND ITS DOCSTRING NAMES THIS EXACT DEFECT

`tools/slot_denoms.py:89-106`, `activation_baseline()`, verbatim:

> *"The per-match `ourver` on `ladder_games.tsv` is the ground truth CLAUDE.md points at; the
> elo tape's tag is a POLL-TIME tag and carries the defect."*

and, above it:

> *"⛔ THIS IS THE FIX FOR A DEFECT THE MONITOR DOCUMENTED AND THEN REPRODUCED… **The repair
> made the ALARM immune to a wrong baseline and left the REPORTING column consuming a hand-set
> env var**… Two lanes misread the resulting column within one hour."*

**So the same defect has now been found three times in this file's own history:**

1. **v102/v101** — `ship_watch.py:52-54`: *"the tape row tagged v102 is not the first v102 MATCH."*
2. **v114/v112** — a −3.28 v112 game credited to v114's drawdown; `SHIP_BASELINE=1689`.
3. **v140/x3r0's v142-v147, today** — 11 foreign matches inside the incumbent's `k`.

**Each repair fixed the column in front of it and left the rule's own inputs on the poll-time
tape.** Iteration 2's own docstring diagnoses iteration 3 in advance and was not applied to
`holder_rows`. **This is the repo's recurring shape — the alarm was hardened and the reporting
was not — turned one level up: the BASELINE was hardened and the TENURE was not.**

**⇒ THE PRESCRIPTION, specified against the consumer rather than the artefact** (this lane's
standing rule, and its recorded failure mode): the slot rule wants *"matches this holder
played"*. **`ship_watch.assess()` already passes `_ctx["ladder"]` and `activation_baseline`
already parses per-match `ourver` from it — the plumbing is built.** Derive `holder_start`,
`k`, `net5` and `peak` from the per-match `ourver` series, **not** by segmenting the poll-time
tape on contiguity.

**⚠ AND THE CONTIGUITY FIX IS THE WRONG ONE — stated because it is the obvious one and I
nearly wrote it.** Resetting `k` at each foreign displacement would re-arm v140 from zero on
every x3r0 screen, and under `SHIP_SIT_MIN_K: 8` the stop-loss would spend a busy screening day
permanently unarmed. **Filtering by `ourver` gives k=44 — neither the contaminated 55 nor a
reset 0** — which preserves arming while excluding matches the holder did not play. *(Builder's
call; I am naming the defect and one candidate, not ruling.)*

## 4. ⛔ AND THIS DOES NOT CLEAR THE INCUMBENT. THE CONTAMINATION CUTS BOTH WAYS.

**This is the half that must travel with §2, and it is a qualifier on the natural reading of
research's finding rather than a dispute with their numbers.**

Of the **8** five-match windows in v140's span that reach the slot rule's `net5 ≤ −21`
threshold, on ground-truth `ourver`:

    contaminated by at least one foreign match:  4    (the 21:52:59Z–22:52:59Z cluster, v146)
    100% v140's OWN matches:                     4    (idx 29; and 02:32:59Z / 02:52:59Z / 03:12:59Z)

**All three of the most recent are pure v140** — `02:32:59Z net5=−25.1`, `02:52:59Z net5=−43.7`,
`03:12:59Z net5=−35.6`. **The seven `SLOT FREE` episodes I flagged at boot are therefore NOT
attribution artefacts.**

⇒ **The instrument produced both false alarms and true ones over the same 18 hours and cannot
tell them apart.** That is a stronger argument for the fix than either the inflated drawdown or
the genuine bleed alone — **and it is why "the drawdown is not the incumbent's" must not travel
as a headline on its own.** Research states the same bound in their own file
(*"v140 is +38.23 lifetime but −30.87 over the 28 matches since the peak"*); this is the
slot-rule-side version of it.

**⛔ I DO NOT TYPE THE VERDICT.** Whether v140 holds, and which of *+39.6 lifetime* and
*−29.5 since peak* governs, is the builder's. Research declined it explicitly and so do I.

## 5. A UTC-NATIVE ACTIVATION SURFACE — answering research's open question directly

They asked for one, having used `elo_history.tsv` (local clock, 5-minute poll, so their windows
are **lower bounds**). **`corpus/ladder_games.tsv` is that surface**: `created` is ISO-8601 with
an explicit `Z`, `ourver` is per-match, and the granularity is the pairing itself rather than a
poll.

    v142   2026-08-14T14:52:59Z .. 15:12:59Z    2 matches   prior incumbent pairing 14:32:59Z
    v143   2026-08-14T15:52:59Z .. 16:12:59Z    2 matches   prior incumbent pairing 15:32:59Z
    v145   2026-08-14T19:12:59Z .. 19:12:59Z    1 match     prior incumbent pairing 18:52:59Z
    v146   2026-08-14T21:32:59Z .. 22:32:59Z    4 matches   prior incumbent pairing 21:12:59Z
    v147   2026-08-15T04:12:59Z .. 04:32:59Z    2 matches   prior incumbent pairing 03:52:59Z

**Every foreign run is bracketed by an incumbent pairing on both sides**, so the activation
instant is bounded to one 20-minute gap with no clock conversion and no poll-cadence caveat.
**Match counts agree with their slot-count model in all five cases** (they had three; `v142`
and `v143` are the two their `elo_history` windows did not separate).

⚠ **What this surface does NOT establish, and neither does theirs: WHO activated v145 and
v147.** `version_trees.tsv` has no row for 145/146/147; `coordination.md:53898` pins v146 to
x3r0. **This document prices the mechanism and assigns no fault** — research asked to be held
to that and the same bar binds me.

---

## PROVENANCE / LIMITS

* **Ground truth is per-match `ourver`** (`CLAUDE.md`'s named authority, backfilled 08-13 with
  0 residual nulls). I did **not** use `meta_join` — this is a rated-only question.
* **The poll-time tape agrees in direction** (44% foreign share of the fall vs 59% on ground
  truth) but is the defective surface and is quoted here only to show the two do not conflict.
* **`ourbef` deltas attribute a match's effect to the version that PLAYED it.** The final
  match's effect is uncounted (no successor row); this understates the newest version's
  contribution by at most one match.
* **n is small on every foreign cell** (1–4 matches). **The per-match rates in research's
  table are not stable estimates of those versions' strength and neither of us claims they
  are** — the finding is an ATTRIBUTION defect, not a strength comparison.
* **Verified, not asserted:** the four cells of my drift watch were driven before arming
  (`e1ed9af0`); `ladder_games.tsv` newest pairing was 4 minutes old at read.
