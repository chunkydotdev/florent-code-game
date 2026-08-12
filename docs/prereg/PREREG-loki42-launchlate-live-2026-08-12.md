# PREREG — LOKI-42 LAUNCHLATE160 vs The Bisons (live unrated)

**Committed BEFORE leg creation (two-clock standard: git author time vs platform `createdAt`).**

## THE PLANK
`bots/_v169launchlate160` — `LAUNCHER_MIN_RND = 160`. One condition, one constant:
do not build a launcher before r160. Everything else is `_v146gunaxis` (v114, live).

## THE QUESTION — AND IT IS NOT THE CURRENCY
**Does deferring the launcher COLLAPSE against a live opponent that attacks early?**
5 unrated matches = 25 games. se = 10pp, **MDE ~28pp at 80% power.**
⛔ **THIS LEG CANNOT CONFIRM +2pp AND MUST NOT BE WRITTEN UP AS IF IT COULD.**
Detecting the local effect would need ~4,900 games = 65 h at the 5-per-20-min
rate limit. **It is a REGIME CHECK: does the arm break in a way self-play
structurally cannot show?**

## WHY SELF-PLAY CANNOT ANSWER IT
Every LAUNCHLATE number is self-play against `_v146gunaxis`. **Our own bot is
measured as a LATE attacker** — 30.5% of our forward rounds sit in r500-999
against the top tier's 16.8%. **So "go undefended until r160" has only ever been
tested against an opponent that does not attack early.** That is precisely the
axis the arm is exposed on.

## TARGET AND WHY
**The Bisons — 1762, +98, admissible, a 5-0 pays +20.38 / a 0-5 costs -11.62.**
Selected on `ladder_games.tsv` (the rated surface), n=125 rated games:
* **44.8% of our games against them end with our core dead before r160 — the
  HIGHEST early-kill rate in the field.** They are the opponent most able to
  punish an undefended opening.
* our historical share against them: **46.4%** — this is the CONTROL.
⚠ **`oppver` is NULL for Bisons games; their version is not pinned and a null
column reads as "no version change" to any cut that trusts it.** Their build may
have changed since those 125 games.

## THE BAR, WRITTEN BEFORE THE DATA
* **COLLAPSE (arm is regime-fragile, deferral is OFF):** game share **<= 20%**
  (a ~26pp drop from the 46.4% control, inside this leg's MDE).
* **NO COLLAPSE DETECTED:** game share **>= 35%**.
* **20-35% = INDETERMINATE**, and it is the most likely outcome at n=25. It must
  be reported as indeterminate, not read as either result.
* **Median kill round and core-death round are recorded but are NOT the verdict.**

## FALSIFIER
If the arm reads >= 35% share **AND** our core dies before r160 no more often
than the 44.8% baseline, the "undefended opening is fatal against real early
aggression" objection is not supported and deferral proceeds to a ship decision
on its local number.

## RATED-COST PROCEDURE — the leg is free, the ACTIVATION is not
`fcode submit` **AUTO-ACTIVATES**; the upload happens INSIDE the window or not
at all. Pairing clock re-derived at 12:16Z: **60/60 recent pairings at minute
= 12 (mod 20), second :59** -> slots `:12:59`, `:32:59`, `:52:59`.
**Fire immediately AFTER an observed pairing** for ~18 min of clear air.
Rollback `fcode submission activate 112`... **NO: the holder is v114. Restore is
handled by `tools/submit_clean.py`, verified on the `Active bot:` line, NEVER `$?`.**
**Verification of zero rated leakage is per-match `teamAVersion` at the PAIRING
BOUNDARY, never the match COUNTER** — a match paired at T completes minutes
later and carries that version into the rated record.

## ⛔ A DEFECT FOUND WHILE WRITING THIS, RECORDED BECAUSE IT ALMOST SET THE TARGET
My first target selection used `meta_join.tsv`. **`our_won` is EMPTY in 18,575
of 24,203 rows (77%)**, and counting blanks as losses turned a 118W-62L record
against Leviathan into "23.4% share". The whole early-kill ranking inherited it.
**`CLAUDE.md` states the rule I broke verbatim: "NEVER `meta_join` for a
win-rate denominator."** Redone on `ladder_games.tsv`; the target changed from
Leviathan to The Bisons as a result.

## ⛔ AMENDMENT, 12:21Z, BEFORE LEG CREATION — THE TARGET'S RATING WAS STALE
The band listing above read **The Bisons 1762, +98, 5-0 pays +20.38**. A LIVE
`fcode team search` reads **1682 / 845 matches** — **80 points lower.**
`tools/target_value.py --band` is reading a cached leaderboard and I did not
check it against the live value before selecting.
**Recomputed at our ~1664: gap +18, E=0.474, a 5-0 pays ~+16.8 and a 0-5 costs
~-15.2.** Still ADMISSIBLE (>= the 1650 floor) and still worth firing, so the
target does NOT change — but the payoff is ~18% lower than the prereg claimed
and the number on the record must be the live one.
**Everything else in this prereg stands: the 46.4% control and the 44.8%
early-kill rate come from `ladder_games.tsv` and are unaffected.**
