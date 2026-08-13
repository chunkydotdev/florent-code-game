# PREREG — PANEL-CAL-2: v125 field-calibration panel (unrated, incumbent)

**Committed 2026-08-13T10:21:59Z (`date -u`), BEFORE any leg of this panel is created (two-clock).
Successor to PANEL-CAL-1 (closed at 30 decoded games / 6 matches on v123's
displacement — below the n=150 floor, so per its own A1.3 it wrapped
DESCRIPTIVE-ONLY and licenses no comparative sentence, ever).**

## What this is
Identical design to CAL-1 (`PREREG-PANEL-CAL1-v123-field-2026-08-13.md`,
including Amendment 1 in full: obligation-14 churn discipline, MATCH-level
clustering primary, de-elasticized looks), re-based on the NEW holder —
**v125 "Loki v8", `bots/_v197mapcode`, INCUMBENT (verified live: `Active
bot: v125`, rating 1662, script-maintained field)**. **SAME SIX CELLS as
CAL-1, deliberately: identical opponents buy a per-cell v125-vs-v123
contrast** (labeled cross-panel, descriptive unless both sides clear 25/cell).

## Obligation 13: N/A by construction (no arms, no treatment diff), stated.

## Frozen gaps (ours 1662 live; theirs = newest league_matches ratingBefore, obs 10:12Z)
| cell | team | gap (E target frozen at these) |
|---|---|---|
| C1 | team lazy | −85 |
| C2 | Focalground | −15 |
| C3 | Juusto | −48 |
| C4 | Jython | −65 |
| C5 | The Bisons | +28 |
| C6 | Lunds Stallions | +50 |
Team_ids unchanged from CAL-1's table.

## Looks (pre-committed)
Descriptive any time; **no comparative sentence below 25 games/cell;
comparative reads at panel totals n=150 and n=300 exactly; wrap below 150 =
descriptive only.** Verdict sentences are the builder's. Not rated evidence;
v125's rated record is governed by its own ship prereg (one look at k=8).

## Lessons wired in from CAL-1/s36 (operational, not statistical)
1. **Fire-registration gates on `match info <id>` status** — never on the CLI
   accept, never on `match list` (COMPLETES-ONLY, verified: 20/20 complete,
   queued invisible).
2. **Accepts consume rate-limit slots from CREATION; completion is
   irrelevant** (builder's production rejections at 10:04/10:09/10:14 against
   five queued 09:57 accepts). Rejections do NOT count (n=1, 09:15:32 accept).
3. The platform runner can back up 25+ min — a queued leg is a live leg;
   readouts treat absent-from-corpus as NOT-COMPLETE, never as nonexistent.
4. The team account has a second live operator today (teammate fires at
   09:16/09:18/10:06) — window arithmetic must tolerate foreign accepts.

## Why now
The fixture is idle again post-ship; v125 shipped on a mechanism fix
(MAP_CODES livelock) whose live evidence is one queued 5-match leg; the same
six cells give the cheapest possible live v125-vs-v123 read.
