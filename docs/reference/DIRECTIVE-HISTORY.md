# DIRECTIVE HISTORY — claims CLAUDE.md used to make, and what replaced them

**Created 2026-08-15.** `CLAUDE.md` is loaded into every session. Text that is
NO LONGER TRUE does not belong there in a form indistinguishable from live
rules — 16 of its passages retract earlier text, and three reprinted the dead
claim in full, in the same bold emphatic register as the rule that replaced it.

**THE RULE:** the always-loaded file states what is true **now**; this file
states what we used to think, verbatim, with the measurement that killed it.
Nothing is deleted — it is relocated so that skimming cannot mistake it.

⚠ **AND THE DIRECTION MATTERS.** This repo has twice been bitten by the
OPPOSITE arrangement: a correct fact in a reference doc nobody boots,
contradicted by the always-loaded file (`fcode submit` auto-activates,
`docs/fcode-cli.md:262`; opponent pinning, `docs/fcode-cli.md:330`). Both times
the live fact was in the unread file. **Here the live fact stays in CLAUDE.md
and only the DEAD one moves, which is the safe direction — but it is the same
hazard pointed the other way, so this file must never acquire a live rule.**

---

## 1. "The rated cost of a prototype leg is ZERO" — retracted 2026-08-10 (s28)

**Superseded by:** the measured cost, **−24.67 Elo across 3 rated matches**
played by a non-incumbent and credited to v104's rating. Budget a prototype leg
at roughly **−8 Elo per leaked match, not zero**. See `CLAUDE.md`, the
unrated-games section.

**Why it was wrong:** it reasoned from pairing cadence (~10 min apart, ~60 s
window) to conclude no rated match could land inside a leg. Ladder matches are
PAIRED at one instant and COMPLETE minutes later, so a match created while the
prototype held the slot carries that version into the rated record. The match
COUNTER cannot see this; per-match `teamAVersion` at the pairing boundary can.

**Kept verbatim below because the PROCEDURE half is still partly live** (serve
the rate-limit wait with the incumbent; activate in the instant before firing;
roll back and verify the holder) — it is the COST claim that died.

```
**THE ORIGINAL CLAIM, KEPT FOR THE RECORD:**
**AND THE RATED COST IS ZERO, MEASURED.** `fcode match unrated` plays the ACTIVE
submission, so a prototype leg needs an activation — but ladder pairings land
~10 minutes apart and a correctly-run window is ~60 seconds, so **v103 and v104
each played ZERO rated ladder matches** across their legs (verified: every
ladder match in the window carries `ourver=102`). **Procedure: serve the
rate-limit wait with the INCUMBENT live; activate only in the instant before
firing; roll back on the fifth accepted challenge and VERIFY the holder.**
**⛔ AND "ACTIVATE" HERE INCLUDES THE SUBMIT — see the submissions bullet above.
`fcode submit` AUTO-ACTIVATES, so uploading the prototype ahead of time to be
ready is exactly the mistake this procedure reads as safe. The upload belongs
INSIDE the 60-second window, not before it.** (s29 walked into this: submitted a
prototype ~20 min ahead of its window and put it on the rated ladder instantly.
Cost was zero rated matches only because the submit was being watched.)
```
