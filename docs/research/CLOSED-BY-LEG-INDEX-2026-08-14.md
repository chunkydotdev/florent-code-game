# CLOSED-BY-LEG INDEX — 2026-08-14

**Purpose.** Three (really four) surfaces each hold a third of the truth on
any given plank — the corefill screen tape, the QUEUE.md row, the
live/`coordination.md` leg tape, and (discovered while building this) any
standalone research sweep that recommends a fire-order path off the same
evidence — and nothing joins them. That gap let `#47` almost get re-fired
live tonight on "screen-passed twice" seven hours after its own pinned live
leg had already closed the road (`coordination.md` 2026-08-14T08:07:23Z,
caught ~15:3x–15:4xZ, QUEUE.md row fixed the same session). **This index is
the join, and it found the gap has not closed — it has moved to a sibling
family that nobody has checked yet.** RECOMMENDATIONS ONLY — research owns
queue edits; nothing here has been written back to QUEUE.md or committed.

---

## METHOD

**ARMS.** Every treatment tree named in `scratchpad/corefill_work.txt`
(current + commented/cancelled rows) unioned with every `bots/_v2*`
directory (40 trees) — **112 unique trees**. Two independent link signals,
kept separate throughout because they carry different evidentiary weight:

1. **In-tree citation** — `grep -rn "QUEUE #" bots/_v2*` (the convention
   named in the brief: `_v207apprlaunch/doctrine.py:1538` opens *"LOKI-APPR
   (QUEUE #47 = #28 x #45-iter3)"*). Full result, 9 trees:
   `_v198feederfirst`→#45 · `_v200siegelaunch`→#45(iter2) ·
   `_v207apprlaunch`→#47 · `_v208idlepeck`/`_v210idlepeck2`→#48 ·
   `_v209quiet0`→#48(ablation) · `_v206gunaxis0`→#33(ablation) ·
   `_v211pavefirst`→#50 · `_v216seatrel`→#8.
2. **Worklist citation** — `scratchpad/corefill_work.txt`'s own doctrine
   comments, e.g. `TWORAID (#42 discriminator b...)` (line 1018),
   `FWDFLOOR8 (#42 discriminator a...)` (line 997). Same evidentiary weight
   as (1): both are the arm's own author naming its row.
3. **QUEUE.md row text itself** — grepped for tree/shard basenames
   independently of (1)/(2), since a row can cite an arm without the arm
   citing back (e.g. row #42's body names `TWORAID`/`COMBO`/`FWDFLOOR8`
   explicitly, confirmed by direct string search of the row's own line).
4. **A fourth surface, found only by reading it in full**:
   `docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md` (commissioned
   `coordination.md:49142-49152`, written 15:21:20Z by a builder-spawned
   opus agent) is a companion document, not QUEUE.md, that maps screen
   evidence to row numbers explicitly in its own table — e.g. its row **"36
   | 900-area eco-as-kill-enabler | ... | UNDERECO 51.56 · ECORAID 53.22 ·
   ECORAID2 52.91"** is the *only* place in the repo that names `#36`
   alongside `UNDERECO`/`ECORAID` by string; **QUEUE.md's own row #36 text
   never mentions those trees.** This citation is kept, but flagged as
   **sourced to the sweep doc, not to QUEUE.md**, in every table below —
   precision over recall means the two link strengths must not be blurred.

**LIVE LEGS.** Every dated block in `docs/coordination.md` matching `TRIAGE
VERDICT` (2 hits), `road CLOSE` (2 genuine closure hits; the case-sensitive
"road CLOSE" grep the brief suggested undercounts — a case-insensitive
`road clos` pass returns 20, of which 18 are older/unrelated closures from
2026-08-07–13 predating this session's arms, read and excluded), `net −`/
`net -` (~90 hits, filtered by inspection to matched-leg game-count deltas
vs rated-Elo deltas — the latter are a different quantity and excluded),
`live leg` (43 hits, filtered to blocks reporting a *returned* outcome, not
a plan), plus `docs/prereg/LEG-*.md` (all 3, read in full) and a keyword
pass (not full read) over the 19 `docs/prereg/SCREEN-*.md` files dated
2026-08-13/14 — none of the 19 contain a fired live-leg verdict, only
forward-looking mentions ("it would go to a pinned live leg…").
**Result, cross-checked by two independent passes: exactly two arms in the
entire corpus have a returned, pinned, matched live-leg verdict as of
2026-08-14T15:55Z** — confirmed independently by `coordination.md:46634-
46637`'s own arm-retro tally: *"2 matched-leg triages (MC −1, MD 0 — both
candidates stopped, test complete)."*

---

## (a) ARM → ROW → LIVE-VERDICT — every arm with a returned live-leg verdict

| leg | arm (tree) | QUEUE row(s) | link basis | design | result | disposition | source |
|---|---|---|---|---|---|---|---|
| MC | `_v207apprlaunch` (rc8.4b/rc8.6) — CONDITIONAL SIEGE LAUNCHER | **#47** | in-tree citation (`doctrine.py:1538`) **and** row now cites back | map-gated, U1–U5 upward opponents, pinned to MA's (v125) anchors | **8/20 vs 9/20 — net −1** (bar ≥+4) | **CLOSED**, and QUEUE.md already carries a `STOP — LIVE ROAD CLOSED` note (row #47, added same session ~15:4xZ) | `coordination.md:45752-45770`; QUEUE.md:134 |
| MD | `_v213ecoraid` (rc8.5c/rc8.7) = `_v205combo` (UNDERECO+TWORAID+DIGOUT) with `LOKI_DIGOUT_ON=False` | **#42** (QUEUE.md-explicit, via TWORAID/COMBO) and **#36** (sweep-doc-explicit only — see METHOD item 4) | #42: worklist citation + row's own text. #36: `QUEUE-ECONOMICS-SWEEP-2026-08-14.md:73` only | map-gated, U1–U5 upward opponents, pinned to MB's (v125) anchors | **5/20 vs 5/20 — net 0** (same bar) | **CLOSED** — *"the eco family's LAST pre-registered road… closes on LIVE MATCHED evidence."* **Neither #42 nor #36 nor the sweep doc's own LIVE-PATH list has been updated with this.** See (b)/(c). | `coordination.md:46415-46431`, `:46450-46463`, `:46465-46480` (independent builder + side-lane certification) |
| rc8.3 (D vs A/B/C) | `_v205combo` (COMBO) vs `_v197mapcode`/`_v201undereco`/`_v203tworaid` | **#42** (same lineage) | worklist + row text | counts-only, n=25, **no game-share verdict licensed at this n** per its own prereg | vs A(control) +3/−5 net −2 · vs B(UNDERECO) +7/−6 net +1 · vs C(TWORAID) +4/−7 net −3 | **INFORMATIONAL, not a closing verdict** — feeds MD's design | `coordination.md:44157-44175` (verified: all 20 matches' scores independently reproduced, 0/20 discrepancies) |

Both MC and MD fired under **one** prereg
(`docs/prereg/LEG-mapconditional-test-2026-08-14.md`), same decision rule
(≥+4 matched games → build the map-gated variant; otherwise stop both),
same day, ~3.5 hours apart (08:07Z, 11:49Z). **Only MC's closure made it
back into a row.**

⚠ **Sizing caveat that applies to both closures equally, carried forward
because it changes what "CLOSED" should mean going forward, not just what
happened**: `coordination.md:48582-48593` (14:35:14Z, i.e. *before* the #47
row-fix but *after* MD's closure) — the ±4-at-n=20 rule was never sized
(≈0.9σ), so **both roads belong at the bottom of the queue, re-openable by
research, not permanently off the map.** `#47`'s STOP note reads consistent
with this (invites "a named design change"); nothing has said the
equivalent for `#42`/`#36` because nothing has touched them since the close.

---

## (b) ⭐ THE LIST THAT MATTERS — arm has a closed live leg, the text does not mention it

**Two rows, one arm, one closed leg, currently live and uncorrected — this
is `#47`'s exact failure shape, one session later, not yet caught:**

| row | citation strength | current text | the gap |
|---|---|---|---|
| **#42** (QUEUE.md:130, "VOLUME-NOT-SEQUENCE") | **Strong** — row's own body names `TWORAID`/`COMBO`/`FWDFLOOR8`; `_v213ecoraid` is COMBO minus DIGOUT (`docs/prereg/SCREEN-ecoraid-v9fix-2026-08-13.md:7-8`) | Row's last line: *"the row's QUESTION is answered; what remains is the SHIP decision on TWORAID/COMBO, which is the builder's and is gated on singles' finals."* Written before MD fired (before 11:49Z). | Grep of the **current** QUEUE.md: `ECORAID`, `_v213ecoraid`, `rc8.5`, `rc8.7`, `MD`, `5/20`, `net 0` occur **zero times** anywhere in the file. Reads as an open ship call; it was already closed net 0. |
| **#36** (QUEUE.md:124, "900-area eco-as-kill-enabler") | **Weaker, sourced externally** — QUEUE.md's own row #36 text never names UNDERECO/ECORAID/COMBO/TWORAID (verified by direct grep of the row's own line); the link exists only in `QUEUE-ECONOMICS-SWEEP-2026-08-14.md:73`, which explicitly places `UNDERECO 51.56 · ECORAID 53.22 · ECORAID2 52.91` against row `#36` | Row #36's text (last carry, s40) discusses map-area eco caps only; no live-leg language at all, consistent with never having cited ECORAID in the first place. | Same absence. But the sharper instance is the **sweep document**, not this row — see (c). |

**The builder's own log claims otherwise.** `coordination.md:46426-46431`
states *"Rows annotated"* in the same breath as MD's closure. That
annotation did not land — confirmed by the grep above. Unlike `#47` (fixed
same day, ~15:4xZ), **`#42`/`#36` have had zero correction as of this read
(2026-08-14T~16:00Z).**

---

## (c) Rows / documents recommending LIVE-PATH for an already-closed family (the `#47` class)

| item | what it recommends | why it collides with a closed leg |
|---|---|---|
| **`#47`** *(historical, self-corrected — kept as the calibration case, not a new finding)* | Ranked to the **top** of the live fire order at ~15:3xZ on "screen-passed twice" | Caught by research going to the primary before drafting the live-leg prereg (`coordination.md:49586-49638`); QUEUE.md row and the sweep doc (below) both got an erratum. |
| **`QUEUE.md` row `#42`** | *"the SHIP decision on TWORAID/COMBO… gated on singles' finals"* — reads as pending | MD already answered it (net 0, stop) 3.5h before the sweep doc that also missed it. Not yet re-ranked to the fire order today only because nobody has touched the row since. |
| **`docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md`, LIST 2 items 4–5 (lines 191-196)** | Explicitly lists **`#42` — "Question closed, lever measured (ECORAID 53.22). This is a ship decision, not an experiment"** and **`#36` — "Screened three times above the bar… the leg should test the eco→pressure conversion"** under the heading **"LIVE-PATH (screens are pointless; legs are the only honest surface)"** | **This document was written 2026-08-14T15:21:20Z — 3h32m *after* MD closed at 11:49:11Z — and still recommends firing a live leg on `#42`/`#36`.** The same document carries a same-day `ERRATUM` (lines 255-266) withdrawing its *own* `#47` LIVE-PATH recommendation for exactly this reason ("a row can be CLOSED LIVE and still look screen-supported"), timestamped after the #47 catch — **but nobody has re-run that erratum's own logic against the sweep's other five LIVE-PATH rows that share the same evidence (`#42`, `#36`, and by extension `#20`, which the same sweep merges "into the eco family" on the identical UNDERECO/ECORAID numbers, `QUEUE-ECONOMICS-SWEEP-2026-08-14.md:111`).** This is the sharper, currently-live instance: an actively-consulted document (it drove the actual `#47` near-miss via its own LIST 2 ranking) still carries the mistake it already corrected once, one row over. |
| **`QUEUE.md` row `#45`** *(softer, secondary — not a confirmed repeat)* | Still lists *"pinned live leg vs CAL-3 C1/C4"* as the remaining step for the launcher-conditional mechanism | `#45` is `#47`'s direct parent (`_v207apprlaunch` doctrine cites *"QUEUE #47 = #28 x #45-iter3"`); `#47`'s own live leg (MC) already tested and lost the near-identical conditional-launcher idea. `#45`'s text was not touched when `#47`'s was. Flagged as a WATCH item, not asserted as the same mistake, since `#45`'s remaining scope nominally covers the broader "kill the builder" plank rather than `#47`'s specific design. |

No other row or document in the corpus currently recommends firing a live
leg on a family that already has one closed — because, per section (a),
only these two families (`#47`, `#42`/`#36`) have reached a live-leg
disposition at all. **The bucket is small because so few arms have gotten
far enough to close a road, not because the risk is contained** — and the
sweep-doc finding shows the risk reproduces in a *second* document the
moment a *second* family closes.

---

## (d) UNRESOLVED — verdict-shaped or leg-adjacent items not confidently resolved

* **~50 of the ~90 `net −N`/`net -N` hits in `coordination.md`** not covered
  by the two TRIAGE VERDICT blocks (e.g. lines 100, 242, 3031, 3045,
  3739-9333, 15407-24193, 32280, 36794-44636) were sampled, not
  individually opened — most read as Elo-delta or cost arithmetic in
  unrelated contexts (submission-leak pricing, panel-power tables), not
  match-tally leg verdicts, but this pass did not open every one.
* **19 `docs/prereg/SCREEN-*.md` files** — keyword-scanned, not read in
  full. None surfaced a TRIAGE/road-CLOSE/live-net hit, but several of
  their arms (`_v219sealfloor0/24`, `_v221mapseal`, `_x3r0v137/141/142`,
  `_v226nestshot`/`_v227nestshot2`, `_v228dest14a`/`_v229dest14b`) have not
  been checked against QUEUE.md for a row link at all — out of scope for
  this pass (no live-leg hit ⇒ not a (b)/(c) candidate today, but the arm
  inventory itself is incomplete for these).
* **`docs/prereg/SCREEN-ammo0-2026-08-13.md:31`** and
  **`SCREEN-osclock-2026-08-14.md:67`** — both name a future pinned live
  leg as their resolving instrument (AMMO0/AMMO02 → no row yet;
  `_v220osclock` → row **#54**, already exists). Neither leg has fired.
  `#54` is a clean candidate for a *future* (a)-table entry the moment its
  leg returns — worth a standing watch, not a current finding.
* **`docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md`'s remaining LIST 2
  items** (`#58`, `#52`, `#41`, `#38`, `#43`, `#5`, `#37`) — cross-checked
  against every live-leg verdict block found; none intersect (no live leg
  has fired on any of them). Flagged here rather than silently dropped
  because the same document already got two rows wrong (`#47` corrected,
  `#42`/`#36` not) — a human pass is warranted before trusting the rest of
  its LIST 2 the way it was trusted for `#47`.
* **Row `#20`** ("the harvester target") — the sweep doc merges it "into
  the eco family" on the same UNDERECO/ECORAID numbers
  (`QUEUE-ECONOMICS-SWEEP-2026-08-14.md:111`) but recommends *closing*
  rather than firing a leg on it, and QUEUE.md's own row #20 text does not
  name ECORAID either. Listed for completeness, not as a (b)/(c) item —
  its recommended disposition doesn't collide with the closed leg the way
  `#42`/`#36`'s does.
* **9 of research's own 10 flagged rows** (`#8 #12 #23 #28 #30 #50 #53 #54
  #56` — the 10th, `#42`, is section (b)) were cross-checked against every
  live-leg verdict block and none intersect: no live leg was ever fired on
  SEATREL (`#8`, died on `GATE-2700 50.40±1.87 ≤ 50.5`,
  `coordination.md:45742`), PAVEFIRST (`#50`), or the rest. Research's own
  read — *"10 flagged rows is the NORMAL state for never-fired planks, not
  a defect count"* — holds for these 9.

---

## Bottom line for the fire-order

**Two live actions, not one:**
1. **Append MD's result to `QUEUE.md` rows `#42` and `#36`** before either
   can recruit a fire-order slot the way `#47` almost did — same corrective
   research already applied to `#47`.
2. **Re-run the sweep document's own `#47` erratum logic against its LIST 2
   items 4–5** (`#42`, `#36` in
   `docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md`) — the document
   already contains the fix pattern for exactly this failure and has not
   applied it to itself a second time.

The durable fix remains what research proposed in the `#47` correction
(`coordination.md:49726-49731`): rows cite their arms, not only arms citing
rows. Right now 9 of ~112 trees are citation-linked from the arm's own
source at all; the two that mattered today (`#42`'s TWORAID/COMBO link,
`#36`'s sweep-only link) were found by lineage and by reading a companion
document in full, not by either convention.
