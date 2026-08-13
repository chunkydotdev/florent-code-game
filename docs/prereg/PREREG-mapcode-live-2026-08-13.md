# PREREG — MAPCODE live leg (unrated, prototype): the rotation fix in front of the field

**Committed BEFORE leg creation (two-clock standard: this file's git author time
precedes the platform `createdAt` of every leg match).** Builder s36 authors and
fires. Treatment tree: `bots/_v197mapcode` (committed, this session). Control
context: the live holder v123 = `bots/_v187saltidle_f`, whose rated 900-area
record today is 2/8 (research decode @c3317b7).

## TARGET BAND (gate run 09:14Z, output in the session log)
`team lazy, gap +122, 5-0 pays +21.41 rated-equivalent, reachable YES` —
**unrated pays 0 rating; the band's role is RELEVANCE** (the ladder pairs us
with these ratings). Team id `648d1d5b-5443-4257-a0aa-7048661b612d` (panel C1's
id, re-verified against the panel prereg table at write time).

## WHAT THIS LEG IS
**A mechanism + smoke leg, NOT a currency leg.** 5 unrated matches (25 games)
cannot resolve game share (observed same-bot swing 12pp at n=25) and no share
claim will be made. It answers, on live opposition:
1. **SMOKE:** does `_v197mapcode` survive contact — zero crash-class unit losses
   of ours, zero TLE-truncation clusters, across all 25 games (replay decode)?
2. **MECHANISM (the dose):** on every game drawn on a 900-area map, our side
   must show the fixed signature: **at least one harvester built after round
   10** (v123's 900-signature is 2 harvesters at r5 and none for the remaining
   995 rounds), and builder action count > 40/game (v123 measured 9/1000
   rounds). Precondition arithmetic: P(a match draws ≥1 of its 5 games on a
   900 map) = 1 − C(10,5)/C(15,5) = **91.6%**, so ~4.6 of 5 matches deliver the
   precondition by construction.
3. **DESCRIPTIVE ONLY:** per-map game tally, kill rounds, win condition — no
   comparative sentence at this n.

## FALSIFIER
If ≥1 crash-class loss of ours, or any 900-area game shows the OLD signature
(no harvester after r10 AND <40 builder actions), the arm does NOT ship today —
back to local diagnosis regardless of the game tally.

## WINDOW DISCIPLINE (the leg's rated-leak protocol)
Pairings re-derived live this session: :12:59/:32:59/:52:59 (mod 20). Submit
via `tools/submit_clean.py` (leg name `Loki rc7.1`, NO `--activate`) **just
after the observed 09:52:59Z pairing**; fire 5 challenges rapid (all 5
rate-limit slots verified clear from 09:35:32 — accepts C4 09:02/C5 09:06/C6
09:15:32 all aged out; rejections confirmed non-counting @937f62b); restore is
submit_clean's automatic holder-restore, verified on the `Active bot:` line.
Leak check: per-match `ourver` at the pairing boundary — no rated match may
carry the prototype's version.

## LOOK SCHEDULE
ONE read, after all 5 matches complete and decode. Progress observable, not
readable as a result.

## WHAT THIS LEG MAY NOT CLAIM
No game-share verdict at n=25. It cannot alone ship, displace, or roll back
anything. The ship decision cites: this leg's smoke+mechanism outcome + the
MAPCODE local battery (n=5,400, live pool, running) + Magnus's call. The
panel (PANEL-CAL-1) yielded this window per the fire order's yield rule and
resumes after the leg (delete `scratchpad/PANEL_CAL1_STOP`).

---

# AMENDMENT 1 — ADD-ONLY, committed BEFORE leg creation. THE ACTUAL FIRE SEQUENCE.

**The side lane caught (verified at submit_clean.py:350-366, pre-fire) that the
original "restore is submit_clean's automatic holder-restore" sequence would
have fired all 5 challenges at the RESTORED v123** — the restore runs inside
the submit command — measuring the wrong bot and falsely tripping this prereg's
own falsifier against an undosed treatment.

**THE SEQUENCE ACTUALLY RUN (submit_clean `--leg` mode, built + driven for
this leg: sentinel/timeout/mid-hold 3/3, --leg×--activate mutual exclusion,
stale-sentinel pre-clean):**
1. `rm -f scratchpad/LEG_FIRES_DONE` (also done by the tool itself).
2. `submit_clean.py bots/_v197mapcode --name "Loki rc7.1" --leg` in background
   — submits (auto-activates), prints `LEG MODE: <proto> IS LIVE`, then HOLDS.
3. On the LIVE line: fire 5 × `fcode match unrated 648d1d5b-…` sequentially.
4. `touch scratchpad/LEG_FIRES_DONE` → the tool restores v123 and confirms on
   the `Active bot:` line (never the exit code).
5. **Fail-safe: a 300s timeout auto-restores even if the operator dies** — the
   hold cannot span the next pairing (window 09:53→10:12 is 19+ min).
6. Leak check unchanged: per-match `ourver` at the pairing boundary.
