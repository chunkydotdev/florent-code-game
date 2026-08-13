# PREREG — TRI-ARM LIVE PANEL: UNDERECO + TWORAID vs the live slot, paired maps

**Committed BEFORE any leg activity (two-clock: git author time precedes every
leg createdAt). Designed by Magnus in-session** (*"pit [the arms] against 5
different opponents in our band with 5 specific maps and compare with our
current slot"*; FWDFLOOR8→TWORAID swap his direct amendment — its local read
was trending negative and TWORAID carries the volume hypothesis). Builder
fires; research decodes; verdict sentences the builder's.

## ARMS (3 × 5 matches = 15 matches, 75 games)
* **A — CONTROL: v125 "Loki v8"** (the ACTIVE submission; fires need no
  activation, zero exposure).
* **B — UNDERECO** (`bots/_v201undereco`, leg name "Loki rc8.1"): chronic-siege
  harvester-reserve restore. Local regression screen 53.6% trending (inside
  band at interim boundary).
* **C — TWORAID** (`bots/_v203tworaid`, leg name "Loki rc8.2"): seat 4 raid
  conversion — the volume-not-sequence discriminator. Local 52.8% at n~600.

## OPPONENTS (5, from the 1716 band table, ids verified in league_matches)
| cell | team | gap | id |
|---|---|---|---|
| O1 | team lazy | +33 | 648d1d5b-5443-4257-a0aa-7048661b612d |
| O2 | Leviathan | +27 | 26286680-d861-4f9e-9073-a6201bd48d3b |
| O3 | LingLing40 | +21 | 86d0b484-783c-47dc-99d9-6ed9af2794f8 |
| O4 | Juusto | −25 | 32087804-2dde-4265-acb2-b6ec9039fbee |
| O5 | Coreflood | −33 | ea0d33c8-ca2b-497a-9be0-1837379eab1e |

**TARGET BAND line:** all five inside us−80..us+125 at our 1716; unrated pays 0
— the band's role is relevance. O2 Leviathan is deliberate: the core-tank/camp
class arms B and C exist to beat.

## MAPS (pinned per match via --map; every match's 5 games = these 5)
`midgard drakkarfjord` (GRAND) · `drumlin frostgate` (STD) · `fjordgate` (CQ)
— mirrors pool class weights at small n and includes the geometry both
mechanisms care about. **Identical across all 15 matches: the design's power
is MATCHED PAIRS (same opponent, same map, different arm).**

## WHAT EACH ARM MUST SHOW (mechanism bars — the falsifiers)
* **B UNDERECO:** in any game where an enemy camp latches `under` >100 rounds
  with our belt cut, the bank must NOT sit pinned ≤12 Ti for 50+ consecutive
  post-chronic rounds, and harvester rebuild activity must appear. **Falsifier:
  a chronic-camp game with the bank still pinned — the fix is inert live.**
  (If the bank unpins but income stays dead, that is the CHAIN-REPLANNER
  discriminator firing — recorded as such, not as a pass or fail of B.)
* **C TWORAID:** in games reaching the siege phase, ≥2 simultaneous forward
  sentinels must OCCUR (control's measured base: two-at-once in ~1 of 10
  autopsied games). **Falsifier: no C game ever shows 2 simultaneous — the
  second seat is not arriving, dose failure.**
* **A CONTROL** provides the paired baseline for every metric.

## WHAT THIS MAY NOT CLAIM
No game-share verdict at n=25/arm (same-bot swing ~12pp). Ship decisions cite
these mechanisms + the local batteries + Magnus. Matched-pair contrasts may be
reported as counts (arm B beat arm A on k of 25 shared cells) with no
inferential dressing.

## EXECUTION
Panel STOP during (yield rule; resumes after). Arm A fires in the first clean
rate window (active bot, no activation). Arms B and C each: safe window just
after an observed pairing → submit_clean --leg (hold-until-sentinel, 300s
auto-restore) → 5 fires with the pinned map list → sentinel → holder restored
+ verified. Leak check per-match `ourver` at every pairing boundary. ONE read
after all 15 matches decode.

---

# AMENDMENT 1 — ADD-ONLY (side lane audit, pre-fire for arms B/C). Three fixes.

1. **C's dose bar is the PAIRED CONTRAST, not bare occurrence.** At the
   control's measured ~1-in-10 base rate, P(≥1 two-at-once game in 25 inert
   games) ≈ 93% — a bare occurrence confirms nothing (the s28 bar-null rule:
   the null expectation now stands beside the bar). C's dose reads as: C's
   two-at-once cell count vs the control's on the SAME 25 opponent×map cells.
   A bare ≥1 may not be quoted as dose-confirmed.
2. **Obligation 13 (mechanism-metric ∩ treatment-diff), both arms:**
   B's metrics (bank level, harvester rebuild activity) are downstream of the
   under_since/chronic diff at `_v201undereco/main.py` (the ti_floor/reserve
   block) — intersection nonempty. C's metric (simultaneous forward-sentinel
   count) is downstream of the seat-4 conversion at `_v203tworaid/main.py`
   (the _raid_seat condition) — intersection nonempty.
3. **Obligation 14 (opponent churn):** O1 team lazy shipped 13+ versions in
   48h. The readout carries a churn table from league_matches per cell;
   high-churn cells are reportable, not poolable across the arm boundary.

**CPU stamp for B (UNDERECO), closing the rider precedent gap:** NEUTRAL —
the diff is a per-round flag update + one comparison in the CORE's turn (no
loops, no scans), nowhere near any per-unit budget path.

---

# AMENDMENT 2 — ADD-ONLY, 2026-08-13T15:05:51Z, BEFORE arm B's leg creation. **O3 IS
# PRE-DECLARED VERSION-CONFOUNDED.** LingLing40 shipped EIGHT versions in four
# hours today (v33→v41, ~one per 40 min — faster than the tri-arm's inter-arm
# spacing), and arm A's O3 match already fired at 14:40:09Z, so the three arms
# CANNOT share an O3 opponent version. Consequences, declared before any B/C
# data exists: O3's matched triples are DOWN-WEIGHTED to descriptive-only in
# the read (no pair-count contribution); the other four cells carry the
# matched-pair analysis; research's decode carries oppver per game and flags
# every O3 triple's version split. The cell stays in the design (its games
# still inform the per-arm mechanism bars, which are opponent-version-robust:
# a bank unpinning and a second sentinel arriving are OUR mechanisms).
