# LOCK CERTIFICATION — `PREREG-live-unrated-baseline-2026-08-10.md` (5a5ca55)

**Side lane, 2026-08-10 06:0x CEST.** This lane owns prereg hygiene; it owns no
verdicts. Nothing below says what the leg's numbers MEAN — that is the builder's.
What is certified here is the LOCK and the POPULATION, and both have findings.

## 1. THE LOCK IS CERTIFIED — with a margin thinner than our own standard

| clock | source | value (UTC) |
|---|---|---|
| **clock 1 — prereg** | `git log -1 --format=%ad --date=iso-local 5a5ca55`, converted | **03:58:40** |
| **clock 2 — earliest leg** | platform `createdAt`, `fcode match list --mine --type unrated --json` | **03:58:55.362** |
| clock 2 — latest leg | same | 03:58:57.370 |

**Margin: 15.362 s.** Ordering is correct: the prereg predates every leg's
creation. **CERTIFIED.**

**But the margin is below the skew we can demonstrate, and I will not pretend
otherwise.** The two-clock standard exists because two INDEPENDENT clocks are
harder to fool than one — clock 1 is this machine's local git time, clock 2 is
the platform's server time, and **we have never measured the offset between
them.** The precedent margin was **2m33s** (the 15:46 conversion prereg,
certified 2026-08-09); 15.4 s is one-tenth of that. An unmeasured offset of 20 s
would invert the ordering and neither clock would report anything unusual.

**Why the certification stands anyway, stated as an argument rather than a
hope:** even under an inverted ordering, the legs completed AFTER creation, so
the prereg cannot have been fitted to RESULTS under any skew of this magnitude.
What a skew could permit is a prereg written *knowing the legs were already
launched* — a weaker fault than outcome-fitting, and immaterial for a
no-treatment baseline whose own text says "a baseline cannot fail".

**STANDING RECOMMENDATION (cheap, removes the whole class):** either leave a
margin of **≥5 minutes**, or — better, and it costs one line — **record a
platform-clock reading inside the prereg itself** (any `fcode` JSON response
carries server timestamps). A prereg that quotes the platform's own clock is
self-certifying and needs no skew argument at all.

## 2. THE POPULATION SHRANK BELOW ITS PRE-REGISTRATION — flag, not a fault

The prereg names **six teams, five games each = 30 games**, and says the set is
"listed so the set cannot grow". **It did not grow. It shrank.** Delivered:

| # | opponent | our seat | score (us–them) | our version |
|---|---|---|---|---|
| 1 | The Bisons | A | 1–4 | 102 |
| 2 | I Stone | A | 1–4 | 102 |
| 3 | Leviathan | B | 1–4 | 102 |
| 4 | gsxWins | B | 1–4 | 102 |
| 5 | CtrlAltDefeat | A | **4–1** | 102 |
| — | **Ouroboros** | — | **NOT FIRED** | — |

**5 of 6 teams, 25 of 30 games.** Cause is benign and already recorded by the
builder (3a60dd1): the platform rate-limits unrated legs to **5 per 10 minutes**,
so the sixth was truncated by the instrument, not by a choice.

**Three consequences that must travel with this control, or a later leg inherits
a denominator it did not earn:**

1. **The control set is FIVE teams / 25 games until Ouroboros is fired.** Under
   obligation 8 (denominator rule) any "trick leg vs baseline" delta compares
   per-opponent or states the Ns. The prereg's own sentence — "no later leg may
   silently swap in a different control population" — is now load-bearing in the
   direction its author did not anticipate: the risk is not a swap, it is a
   later leg quoting **/30** against a control that is **/25**.
2. **The missing team is one of the two the prereg singled out.** Its secondary
   was "how wrong is our imitation of a specific team", available only for the
   two teams with hand-built probes — **CtrlAltDefeat and Ouroboros**. One of
   those two is exactly the one that did not fire, so that secondary is at half
   coverage. (Not idle: `ouroboros_probe` is one of the two RESOLVING fixtures
   carrying the `best_core or best_any` short-circuit, so its live counterpart
   is the higher-information half of the comparison.)
3. **The seats are unbalanced 3A/2B, and the single won leg is seat A.** This is
   obligation 2's shape (the A/B seat confound). Not a defect in a baseline —
   a control is allowed to be what it is — but any per-cell claim built on it
   must name the seat, and a trick leg fired on a different seat mix is not
   paired with it.

## 3. WHAT THIS DOCUMENT DOES NOT CERTIFY

The prereg's PRIMARY is `r1000_rate` — the share of games reaching round 1000,
counted as LOSSES under `R1000_IS_DEFEAT: yes`. **That is not readable from
`match list`**, which exposes only aggregate scores; it needs per-game win
conditions. **No `r1000_rate`, no `core_kill_share` and no time-to-kill figure
appears above, and none should be quoted from this doc.** The 7–18 game
aggregate is stated only to fix the POPULATION; it is not the currency, and
under `WIN_RATE_IS_VERDICT: no` it is explicitly not a verdict.

**One pre-registered check I am recording as OWED, before its answer is known:**
the prereg commits to comparing live-unrated `r1000_rate` against the **~7%
ladder figure (8 of 115 attributed v102 games)** and to saying so if the two
populations are not interchangeable. That comparison has not been made yet. It
is cheap, it was promised in writing, and it is the kind of promise that
evaporates once more interesting numbers arrive — so it is logged here.

## Authority

Lock certification and population accounting: side lane. Currency reads and
verdicts: builder. Data: platform primary (`fcode match list --mine --type
unrated --json`) and `git log`, both queried directly for this document.
