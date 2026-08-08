# Swap-rule review pack — for Magnus / team conversation

**Version tag:** compiled 2026-08-08 16:3x CEST by the research arm (s18).
Live: v80 "Eir 9b" (= `bots/_v89sh`, md5 e12f8585), 1557.3 @ 401 #31 at
compile time. Sources: `elo_history.tsv` tape rows, `docs/coordination.md`
dated notes (line refs below), `replay_archive/` match metas (exact
eloDeltas), platform status API. All numbers re-verified against primaries
at compile time, including the v77 window correction landed today 16:20.

**The rule as used** (team convention): a holder whose rolling last-5 net
Elo is ≤ 0 frees the slot; swapping in still requires a measured
better-case. It has governed every slot change on our side today.

---

## 1. What the tape shows — one day, seven slot events

| event | trigger | outcome |
|---|---|---|
| v74 → v75 (09:33) | last-5 **−9** @359, 13-match window net −36.3 | Founding use. Material. Worked as designed. |
| v75 → v76 (x3r0, ~13:0x) | v75 last-5 **−8** @369 | Material. Slot was free; x3r0 took it. |
| v76 noise pair (~12:45 real; note stamped 18:4x, drift-era) | last-5 **−2** @378 → **+7** @379 | **Noise exhibit 1**: crossing reversed within two matches. Builder flagged: any two early losses free the slot under the rule as written. |
| v76 → v77 (ours) | v76 last-5 **−20** @381 | Material. Clean use. |
| **v77 → v78 (x3r0, 12:05Z)** | **none — v77 last-5 stood at +20** | **The out-of-rule swap-in.** See §2. |
| v78 → v76 (x3r0, ~14:35) | v78 +7/3 self-rollback | Not rule-governed either direction; his test, his rollback. |
| v79 window crossing @391 | last-5 **−8** spanning the v78/v76/v79 boundary (v79 itself only 2 matches, −2/−13) | **Noise exhibit 2**: the rolling window straddled three holders; the crossing priced other bots' matches into v79's window. |

(v79 → v80 at 15:47 was a material rollback — v79 −43.9/7 — plus Magnus's
direct call; not an exhibit, the rule worked.)

**Noise exhibit 3** (the founding observation, builder note real-≈12:45):
the two founding triggers were −9 and −8 with 13- and 9-match windows
behind them; a −2 crossing five matches into a window is a different
animal that the rule's letter treats identically.

## 2. The v77 truncation — sharpened by today's correction

x3r0 uploaded v78 at 12:05:00Z while v77's rolling last-5 stood at +20 —
the slot was NOT free under the rule. Today's archive reconciliation
(16:20 note; builder-verified, tape row `v77-final-corrected`) makes the
truncated window **+34.1 over 6 matches**, not +20.2/5: a 4-1 over CAD
and a 5-0 over Memtrace landed late in the archiver, the Memtrace match
created 12:02:43Z — before the swap — and **completing 12:09:27Z, during
it**. The day's strongest holder window was truncated mid-5-0.

The open question routed to Magnus at the time (14:09 note), unchanged:
**does the rule bind swaps-IN while the holder's window is positive, or
does it only define when the slot is free?** Today's tape now contains
both readings acted out.

## 3. New intel for the same conversation (16:2x)

Five unrated challenges of our v80 ran 15:57–16:00 local — between the
two builder sessions, so a teammate (presumably x3r0, owner) triggered
them. v80 went 5-0 vs **"opensverige - plan B"** (a shadow team), 3-2 vs
sporks v8, then 1-4 Pantheon v56, 1-4 Lorem Ipsum v25, 0-5 "not adgato"
v19. Read-through: ten minutes after the rollback ship, the fielded bot
was being benchmarked, and a "plan B" team exists. Not priced (5-game
unrated samples, unknown seat/map mix) — but it says the slot question
is live on his side too, and the conversation is timely.

## 4. Options on the table (builder's refinements + one addition)

Decision is the team's; research states a recommendation because Magnus
asked for stated recommendations. All refinements keep the rule's core
(rolling last-5 ≤ 0 frees the slot; measured better-case to enter).

1. **Arm the window only after N matches on the holder** (builder
   floated N=8). Kills noise exhibits 1 and 2 (both were early-window).
2. **Magnitude floor** (builder floated ≤ −5). Kills exhibit 1; exhibit
   2's −8 would still have fired — but it was a boundary-straddling
   window, which N-matches also fixes.
3. **Window resets on holder change** (addition, from exhibit 2): the
   rolling last-5 should never span a slot boundary — price only the
   current holder's matches. Cheap, purely mechanical, no judgment.
4. **Swap-in clause**: explicit answer to §2 — e.g. "a positive-window
   holder is not displaced except by team agreement or a measured
   better-case at ≥ some bar." This is the piece that needs x3r0 in the
   room; the other three are our-side mechanics.

**Recommendation:** adopt 1 (N=8) + 3 (reset on holder change)
unilaterally for our own swap decisions — they only constrain us and
remove the two measured noise modes; bring 4 (and today's v77 exhibit,
corrected numbers) to the team conversation rather than legislating it
from one side. Option 2 becomes unnecessary if 1+3 land.

---

## 5. ADOPTED — 2026-08-08 16:48 CEST

Magnus reports x3r0 **accepted** the proposal. The revised rule is now
team convention:

1. Rolling last-5 arms only after the holder's 8th match.
2. The window prices only the current holder's matches (resets on any
   slot change).
3. A holder with a positive rolling window is not displaced except by
   team agreement or a measured better-case at an agreed bar.

Entering still requires a measured better-case; ≤ 0 frees the slot but
never forces a swap; the rule cuts both ways. Operational follow-up
routed to the builder: the elo_logger swap-rule wake logic implements
the OLD trigger (any last-5 ≤ 0 crossing) and needs the arming
threshold + holder-reset to match the adopted rule.

---

*Research arm compilation; no verdicts herein — tape rows and slot
actions remain builder-owned. Exhibit line refs: coordination.md :3029
(v74 founding), :3737 (v75 −8), :4754/:4771 (−2/+7 noise pair), :4961
(v76 −20), 14:09/14:51/16:20 notes (v78 swap-in, @391 crossing, v77
correction).*
