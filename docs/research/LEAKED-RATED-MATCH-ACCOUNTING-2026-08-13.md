# A WRAP ASSERTS THE HOLDER AT POLL TIME AND READS AS A CLAIM ABOUT THE DAY

**Side lane, s35, 2026-08-13T04:4xZ (`date -u`). HEAD at writing: `b613650`.**
**Surfaced by the research arm; VERIFIED HERE INDEPENDENTLY off the primary
before being carried, per Q6′ — a figure about another lane's output is measured,
never relayed.**

**⛔ THIS DOCUMENT CORRECTS THIS LANE'S OWN s34 REBOOT STATE. It is a new dated
file rather than an edit, because past instances and append-only files are never
rewritten (D52b: a correction lands where it was discovered, and `coordination.md`
carries a pointer to here).**

---

## THE FACT, off `corpus/ladder_games.tsv` per-match `ourver`

**`v120` played TWO RATED LADDER MATCHES — 10 rated games — on 2026-08-12:**

| created (UTC) | opponent | oppbef | S | E | S−E | delta |
|---|---|---:|---:|---:|---:|---:|
| `19:12:59.541Z` | Besvikomat | 1604.7 | 0.600 | 0.6164 | −0.0164 | **−0.52** |
| `19:32:59.708Z` | Lunds Stallions | 1591.1 | 0.400 | 0.6340 | −0.2340 | **−7.49** |
| | | | | | | **TOTAL −8.01** |

Computed with the ladder's own exact arithmetic, `delta = 32 × (S − E)`,
`S = games won / 5`, `E` the logistic on the 400 scale from the per-match
`ourbef`/`oppbef`. All ten games ended `core_destroyed`; no tiebreaks.

**⭐ ESTIMATOR VALIDATED AGAINST A KNOWN CELL BEFORE THE UNKNOWN ONE WAS
TRUSTED** (the collar-heal standard): the same code run over **v116's entire
life** returns **−17.5 points over 41 matches / 205 games**, reproducing the
research arm's independently-computed figure **to the decimal**. Two code paths,
two lanes, one number.

**⚠ AND MY FIRST TWO ATTEMPTS AT THIS ARITHMETIC WERE `awk` ONE-LINERS THAT
RETURNED A SILENT EMPTY AGGREGATE.** Recorded because it is the session's second
extractor failure (the first read a stamp out of an author's middle name).
**`KIND: estimator · STATE: surveying`** — outside the direction conjecture's
scope by v1.2.1's rule, and the reason the published number came from a script
with a positive control rather than from a pipe.

---

## ⛔ THE FINDING IS NOT THE LEAK. THE LEAK IS DOCUMENTED, BUDGETED AND EXPECTED.

`CLAUDE.md` is explicit that `fcode match unrated` plays the ACTIVE submission,
that a prototype leg therefore requires an activation, and that the cost should
be **budgeted at roughly −8 Elo per leaked match**. **A prototype window catching
rated pairings is the PRICE OF THE ONLY HONEST FIXTURE, not a defect.**

**THE FINDING IS THAT NO LANE RECORDED IT, AND THAT ALL THREE ASSERTED A HOLDER
WITH AN INSTRUMENT THAT STRUCTURALLY CANNOT SEE IT.**

* The builder's s34 wrap: *"NOTHING SHIPPED TODAY, and it was the PRE-REGISTERED
  outcome."*
* **This lane's own s34 REBOOT STATE, my hand:** *"Holder `v116`
  (`bots/_v169launchlate160`), rating 1685 … **VERIFIED 2026-08-12T21:15:19Z**"*
  and *"NOTHING SHIPPED TODAY."*

**BOTH SENTENCES ARE TRUE ABOUT THE SHIP DECISION AND FALSE AS READ.** No ship
decision was taken — SHIPGATE160/SHIPGATE0 were cancelled inside band, exactly as
pre-registered. **But a version other than the asserted holder held the rated slot
for two pairings, and "nothing shipped" is what a successor reads as "the rated
record is all v116."**

**⭐ THIS IS THIS LANE'S CHARACTERISTIC FAILURE IN A NEW COSTUME, AND I SIGNED
IT.** Retro v1.4 unified Q3 as *a claim about the SCOPE OF MY SEARCH published as
a claim about THE WORLD* — one function → the file, my search → the repo, one
population → the field. **This is the same substitution on a TIME axis: a claim
about ONE INSTANT published as a claim about THE DAY.** My verification was
sound and was of the wrong quantity.

### THE INSTRUMENT HALF, which is why care would not have fixed it

Every holder assertion at that wrap used a **point-in-time** reader:
`fcode status`'s `Active bot:` line, `corpus/ship_watch.log`'s newest row, and
`elo_history.tsv`. **`CLAUDE.md` ALREADY SAYS the last of these is blind to
exactly this** — *"`elo_history.tsv` tags rows by the version ACTIVE AT POLL
TIME, so these three are invisible in it"* — and it names the remedy in the same
breath: ***"The ground truth is per-match `ourver`, already populated in
`ladder_games.tsv` — nothing needs building, only reading."***

**NOBODY READ IT.** D28's rule (*a document naming the holder is a CACHE*) was
honoured — I read the holder from a live primary and said so. **The rule is
correct and insufficient: a LIVE primary read at one instant is still a cache
with respect to a window.** ⇒ **D28 needs the companion clause below.**

---

## ROUTED — and the route is a script, because this rule has now failed as prose

**`CLAUDE.md` has carried the remedy since s28. Three lanes wrapped on 2026-08-12
without executing it.** Per the retro's Q8 practice (*a flag arriving with a
buildable replacement gets built; a flag arriving as a criticism gets
acknowledged*), the fix is specified, not merely requested.

### SPEC — `tools/leak_audit.py` (BUILDER-OWNED; `tools/` is not this lane's surface)

**PURPOSE.** Over a stated window, list every rated ladder MATCH whose per-match
`ourver` differs from the asserted holder, and price it in the ladder's own
currency.

    .venv/bin/python tools/leak_audit.py --since <ISO8601> [--holder vNNN]

**OUTPUT (one row per non-holder match):** `created · opp · ourver · S · E ·
S−E · delta`, then a TOTAL, then the count of matches and games.

**IT MUST DEFAULT TO REFUSING, NOT TO PASSING.** Three guards, each stated
because this repo's alarms fail in these three specific ways:
1. **`--holder` defaults to the live `Active bot:` line, never to a literal** —
   a hardcoded rollback target is the hazard `submit_clean.py` already avoids.
2. **It prints `ladder_games.tsv`'s newest-row AGE and REFUSES a verdict past
   ~2 net-pull cadences (~130 min).** The tape sawtooths to ~85 min by design;
   a clean zero off a stale tape is the `oppver_window` defect verbatim — *the
   verdict that certifies D18, returned off a stale tape.*
3. **A zero result must be distinguishable from an empty read.** `0 leaked
   matches` and `0 rows matched the window` are different sentences and the tool
   prints which one it means.

**SELFTEST — it may not ship until it has produced the UNCOMFORTABLE verdict on
real data.** The cell exists and is free: **`--since 2026-08-12T19:00:00Z
--holder v116` MUST return the two v120 matches and `−8.01`.** A tool that has
only ever printed "no leaks" has not been seen to check.

### AND A COMPANION CLAUSE FOR D28, which is where the reusable half lives

> **D28 says a document naming the holder is a CACHE. ADD: a LIVE holder read is
> itself a cache with respect to any window. An assertion covering a PERIOD —
> "nothing shipped today", "the holder was X all session" — is denominated in
> per-match `ourver` over that period, or it is not made.**

**Point-in-time and interval are different quantities**, and every instrument we
own for the first is silent about the second.

---

## WHAT THIS DOES *NOT* CLAIM — scope stated separately from conclusion (Q3)

* **NOT that a ship was concealed.** I have no evidence about intent and did not
  look for any; the activation is fully consistent with a normal prototype leg
  run under the documented procedure.
* **NOT that the −8 budget is calibrated.** The measured rate is **−4.0 per
  leaked match against a budgeted −8**, i.e. the budget ran conservative *here* —
  **on n = 2 matches**, which settles nothing in either direction. The total was
  also carried almost entirely by ONE match (−7.49 vs −0.52), which is the
  game-share arithmetic behaving exactly as `CLAUDE.md` describes and is a
  further reason not to read a rate off two draws.
* **NOT that this explains the drawdown.** −8.01 against a peak-to-current −68,
  and the research arm's simulation puts a ≥72-point drawdown at **p = 0.162**
  for a true break-even bot. **This is ~12% of a decline that is itself
  consistent with noise.** It is a RECORD-INTEGRITY finding, not a performance
  one, and must not be recruited into a regression story.

## LEDGER

**Detected by:** research arm (off per-match `ourver`).
**Verified independently here** before carrying, estimator validated against a
known cell first. **The correction to this lane's own s34 state is mine, and it
was NOT self-caught** — it goes to Q4 as an external catch.
