# RATED DAY DECODE — 2026-08-14 UTC

**Lane:** research arm (read-only analysis agent). **Written:** `date -u` in the
producing shell read **2026-08-14T18:32:59Z** (a pairing boundary, as it happens).
**Scope:** every RATED LADDER game whose match `created` falls on 2026-08-14 UTC.
**Population: US ONLY** — this is OpenSverige's own rated record and nothing else.

**No verdict sentence is written here. That is the builder's.** Everything below
is observation plus explicitly-labelled inference.

---

## 0. FRESHNESS — stated before any number is read

| surface | rows | newest row | age at 18:32:59Z | file mtime |
|---|---|---|---|---|
| `corpus/ladder_games.tsv` (PRIMARY, rated denominator) | 4,910 | `created` **2026-08-14T18:12:59.600Z** | **20 min** | 2026-08-14T20:21:06+0200 = 18:21:06Z |
| `corpus/league_matches.tsv` (elo deltas, opp timelines) | 45,280 | `createdAt` **2026-08-14T18:12:59.600Z** | 20 min | 18:22:04Z |
| `elo_history.tsv` (activation timeline) | 2,246 | **2026-08-14T20:27** *(LOCAL, UTC+2)* = **18:27Z** | 6 min | 18:27:26Z |

**The 20-minute gap is NOT staleness — it is one pairing slot.** Ladder pairings
today landed at **minute ≡ 12 (mod 20), second `:59`, in 55 of 55 slots with
zero gaps** (verified: 54 consecutive inter-slot gaps, all exactly 20.0 min;
second offset `:59` in 55/55). The next pairing was due at **18:32:59Z**, i.e.
the same second this file's clock was read. **The corpus is current through the
last completed pairing.** Any statement here is safe to publish; a statement
about the 18:32:59Z match is not, because that match does not exist on the
surface yet.

⚠ **`elo_history.tsv` timestamps are LOCAL (UTC+2), not UTC.** Every activation
time in §2 is converted by −2 h. This is a real trap: read raw, its newest row
(`20:27`) sits two hours in the future of `date -u`.

---

## 1. THE LEDGER — 55 rated matches, 275 games, in time order

`d` = official `eloDeltaA/B` from `corpus/league_matches.tsv`, joined on match id
(**55 of 55 matches joined, 0 misses**). Maps abbreviated to 4 chars.

| # | created (UTC) | opponent | oppver | ourver | ourbef | share | d (elo) | maps |
|---|---|---|---|---|---|---|---|---|
| 1 | 00:12:59 | team lazy | v226 | v125 | 1781.2 | 4/5 | +11.12 | ragn/auro/valk/drak/glac |
| 2 | 00:32:59 | arsonist duck | v24 | v125 | 1792.3 | 4/5 | +7.95 | icef/auro/yule/ragn/midg |
| 3 | 00:52:59 | Erebus | v103 | v125 | 1800.3 | 2/5 | −4.20 | roya/auro/antl/drak/midg |
| 4 | 01:12:59 | Juusto | v11 | v125 | 1796.1 | 3/5 | +1.86 | yule/nord/ragn/drum/arch |
| 5 | 01:32:59 | Jython | v136 | v125 | 1797.9 | 2/5 | −5.46 | ragn/yule/drum/fjor/auro |
| 6 | 01:52:59 | HTTP 418 | v103 | v125 | 1792.5 | **1/5** | −8.36 | antl/yule/roya/glac/arch |
| 7 | 02:12:59 | team lazy | v226 | v125 | 1784.1 | 4/5 | +10.82 | ragn/drak/roya/nord/valk |
| 8 | 02:32:59 | Erebus | v103 | v125 | 1794.9 | 2/5 | −3.32 | icef/yule/drak/midg/auro |
| 9 | 02:52:59 | Juusto | v11 | v125 | 1791.6 | 3/5 | +3.20 | glac/roya/antl/yule/ragn |
| 10 | 03:12:59 | Big O | v18 | v125 | 1794.8 | 3/5 | +1.22 | valk/yule/antl/nord/fjor |
| 11 | 03:32:59 | HTTP 418 | v103 | v125 | 1796.0 | 2/5 | −2.92 | roya/fros/nord/arch/glac |
| 12 | 03:52:59 | kladde chatte tville | v97 | v125 | 1793.1 | **1/5** | −6.57 | antl/icef/valk/arch/drak |
| 13 | 04:12:59 | Pantheon | v79 | v125 | 1786.5 | 2/5 | +0.58 | roya/ragn/midg/fros/icef |
| 14 | 04:32:59 | Juusto | v11 | v125 | 1787.1 | **1/5** | −8.82 | fros/ragn/drum/roya/auro |
| 15 | 04:52:59 | team lazy | v226 | v125 | 1778.3 | 3/5 | +4.30 | midg/drak/arch/fjor/nord |
| 16 | 05:12:59 | 0033 | v56 | v125 | 1782.6 | 3/5 | +5.02 | ragn/valk/glac/arch/antl |
| 17 | 05:32:59 | kladde chatte tville | v97 | v125 | 1787.6 | 2/5 | +0.21 | antl/nord/fjor/roya/fros |
| 18 | 05:52:59 | LingLing40 | v46 | v125 | 1787.8 | 3/5 | +1.27 | midg/arch/valk/ragn/yule |
| 19 | 06:12:59 | diverge | v20 | v125 | 1789.1 | 4/5 | +8.09 | yule/fros/fjor/glac/nord |
| 20 | 06:32:59 | Erebus | v103 | **v134** | 1797.2 | 3/5 | +3.76 | fjor/arch/roya/glac/icef |
| 21 | 06:52:59 | HTTP 418 | v103 | v134 | 1800.9 | **1/5** | −10.87 | arch/glac/icef/ragn/nord |
| 22 | 07:12:59 | diverge | v20 | v134 | 1790.1 | 2/5 | −4.41 | glac/valk/fjor/yule/midg |
| 23 | 07:32:59 | 0033 | v56 | **v135** | 1785.7 | **0/5** | **−13.89** | fros/antl/fjor/midg/drak |
| 24 | 07:52:59 | Jython | v137 | v125 | 1771.8 | 3/5 | +1.59 | auro/antl/icef/valk/ragn |
| 25 | 08:12:59 | HTTP 418 | v103 | **v137** | 1773.4 | 2/5 | −2.63 | midg/yule/drak/arch/drum |
| 26 | 08:32:59 | LingLing40 | v48 | v137 | 1770.7 | **1/5** | −11.41 | arch/antl/yule/nord/auro |
| 27 | 08:52:59 | Erebus | v103 | v137 | 1759.3 | 2/5 | −0.22 | roya/glac/icef/antl/arch |
| 28 | 09:12:59 | diverge | v20 | **v139** | 1759.1 | 3/5 | +2.86 | drum/icef/midg/antl/arch |
| 29 | 09:32:59 | team lazy | v226 | v139 | 1762.0 | 4/5 | +11.65 | ragn/fros/antl/glac/drum |
| 30 | 09:52:59 | Big O | v19 | v139 | 1773.6 | **1/5** | −10.63 | midg/yule/glac/nord/drum |
| 31 | 10:12:59 | 0033 | v57 | v139 | 1763.0 | **1/5** | −7.00 | ragn/roya/fros/midg/yule |
| 32 | 10:32:59 | Jython | v137 | v139 | 1756.0 | 2/5 | −5.15 | roya/fjor/antl/drum/midg |
| 33 | 10:52:59 | LingLing40 | v49 | v139 | 1750.8 | **0/5** | **−14.63** | antl/fros/arch/drum/valk |
| 34 | 11:12:59 | diverge | v20 | v139 | 1736.2 | 2/5 | −2.24 | antl/midg/yule/fjor/fros |
| 35 | 11:32:59 | The Bisons | v8 | v139 | 1734.0 | **1/5** | −9.79 | arch/fjor/ragn/icef/drum |
| 36 | 11:52:59 | arsonist duck | v24 | **v140** | 1724.2 | **5/5** | **+16.06** | antl/ragn/icef/midg/nord |
| 37 | 12:12:59 | Askar City | v104 | v140 | 1740.2 | 4/5 | +4.05 | valk/yule/fjor/midg/drak |
| 38 | 12:32:59 | Jython | v137 | v140 | 1744.3 | 3/5 | +2.53 | roya/drum/arch/antl/icef |
| 39 | 12:52:59 | Coreflood | v86 | v140 | 1746.8 | 2/5 | −5.88 | midg/yule/glac/ragn/fros |
| 40 | 13:12:59 | lingling_40h | v52 | v140 | 1740.9 | 2/5 | −0.77 | glac/icef/antl/nord/roya |
| 41 | 13:32:59 | Big O | v21 | v140 | 1740.2 | 3/5 | +3.85 | ragn/fjor/fros/nord/midg |
| 42 | 13:52:59 | The Bisons | v8 | v140 | 1744.0 | 3/5 | +3.35 | arch/fjor/yule/fros/nord |
| 43 | 14:12:59 | Coreflood | v88 | v140 | 1747.4 | 4/5 | +8.21 | glac/arch/antl/roya/drum |
| 44 | 14:32:59 | Jython | v137 | v140 | 1755.6 | 2/5 | −5.35 | arch/nord/drum/valk/icef |
| 45 | 14:52:59 | Landers | v93 | **v142** | 1750.2 | 3/5 | −3.10 | midg/icef/antl/ragn/valk |
| 46 | 15:12:59 | The Bisons | v8 | v142 | 1747.1 | 3/5 | +2.74 | roya/antl/valk/icef/yule |
| 47 | 15:32:59 | Erebus | v103 | v140 | 1749.9 | 4/5 | +13.37 | ragn/icef/drak/yule/valk |
| 48 | 15:52:59 | Big O | v21 | **v143** | 1763.2 | 3/5 | +1.61 | nord/drak/fros/fjor/valk |
| 49 | 16:12:59 | Jython | v137 | v143 | 1764.8 | 3/5 | +0.44 | ragn/auro/fjor/midg/drak |
| 50 | 16:32:59 | HTTP 418 | v103 | v140 | 1765.3 | **1/5** | −7.57 | drum/auro/midg/fjor/drak |
| 51 | 16:52:59 | Erebus | v103 | v140 | 1757.7 | 3/5 | +5.79 | fjor/arch/drak/glac/roya |
| 52 | 17:12:59 | arsonist duck | v24 | v140 | 1763.5 | 3/5 | +2.70 | yule/icef/glac/valk/roya |
| 53 | 17:32:59 | team lazy | v226 | v140 | 1766.2 | **5/5** | **+18.41** | drak/nord/valk/roya/icef |
| 54 | 17:52:59 | lingling_40h | v49 | v140 | 1784.6 | 3/5 | +4.19 | midg/yule/fros/antl/valk |
| 55 | 18:12:59 | Big O | v21 | v140 | 1788.8 | 4/5 | +6.15 | fros/arch/yule/ragn/auro |

**DAY TOTAL: 55 matches · 275 games · 140 wins · game share 50.9% · NET
+13.76 Elo.**

**RECONCILIATION (independent, and it could have failed):** first match's
`ourbef` 1781.19 **+ 13.76 = 1794.95**; `elo_history` at 18:27Z reads **1795**.
The `eloDeltaA/B` join and the poll tape agree to under 0.05 Elo across 55
matches.

**`oppver` null check: 0 of 275 rows are null/`'None'`.** Post-backfill this
column is live for every game today, so no cell is dark. *(The check has
discriminating power: the same column was the literal string `'None'` in
4,375 of 4,375 rows before the 08-13 backfill.)*

---

## 2. THE DAY'S ARC BY OUR VERSION — and the incumbency question

### 2a. Holder timeline (activation times from `elo_history.tsv`, LOCAL→UTC −2h)

| activation (UTC) | version | what it is (per `docs/coordination.md`) |
|---|---|---|
| (carried from 08-13 10:18Z) | **v125** | our previous ship |
| ≤ 06:27Z | **v134** | x3r0's authorised slot run |
| ≤ 07:22Z | **v135** | x3r0 upload (= our rc8.5/ECORAID tree) |
| ≤ 07:43Z | v125 | rollback (Magnus-directed, after one pairing) |
| ≤ 08:03Z | **v137** | x3r0 |
| ≤ 08:48Z | v125 | brief revert |
| ≤ 08:53Z | v137 | x3r0 re-activated |
| ≤ 09:08Z | **v139** | x3r0 |
| ≤ 11:40Z | **v140** | **our ship — `Loki v10`** |
| ≤ 14:46Z | **v142** | x3r0 "Counter Router v3" (displacement) |
| ≤ 15:21Z | v140 | our re-activation (Magnus-ordered) |
| ≤ 15:46Z | **v143** | x3r0 "Counter Router v2 Artifact Counter" (displacement) |
| ≤ 16:21Z | v140 | our re-activation — **still holding at 18:27Z** |

**Every `ourver` in the ledger is consistent with this timeline at its pairing
second — 55 of 55.** No match carries a version that was not the active
submission at its creation.

### 2b. Per-version table

| ourver | matches | games | share | net Elo | window (UTC) | DEFF used | 95% half-width |
|---|---|---|---|---|---|---|---|
| v125 | 20 | 100 | **52.0%** | **+17.58** | 00:12–07:52 | 1.529 | ±12.1pp |
| v134 | 3 | 15 | 40.0% | −11.52 | 06:32–07:12 | 1.366 | ±29.0pp |
| v135 | 1 | 5 | **0.0%** | **−13.89** | 07:32 | — | *normal approx invalid at p=0, n=5* |
| v137 | 3 | 15 | 33.3% | −14.26 | 08:12–08:52 | 1.366 | ±27.9pp |
| v139 | 8 | 40 | **35.0%** | **−34.93** | 09:12–11:32 | 1.529 | ±18.3pp |
| **v140** | **16** | **80** | **63.7%** | **+69.10** | 11:52–18:12 | 1.529 | ±13.0pp |
| v142 | 2 | 10 | 60.0% | −0.37 | 14:52–15:12 | 1.366 | ±35.5pp |
| v143 | 2 | 10 | 60.0% | +2.04 | 15:52–16:12 | 1.366 | ±35.5pp |

DEFF choice is derived per stratum in §5, not asserted.

**Independent replication of two tape numbers, both exact:**
* Tape (`coordination.md:49169`, ~15:1xZ): *"v140 ERA: 9 MATCHES, 28/45 GAMES
  = 62.2%, NET +26.1 Elo."* My cut restricted to ≤14:32:59Z gives **9 matches,
  28/45, +26.05**. Agrees to rounding.
* Tape (`:49118`): *"v139's full era 14/40 = 35.0%, NET −34.9."* My cut:
  **14/40 = 35.0%, −34.93.** Agrees.
**No contradiction with the coordination tape was found anywhere in this decode.**

### 2c. LEAKED EXPOSURE — the count is ZERO, and the instrument was controlled

**⛔ A CORRECTION TO THE TASK FRAMING.** The brief describes today's holder arc
as "v140, v141, v142, v143, back to v140" and asks how much of it was a
prototype leak. Both halves need adjusting:

1. **`v141` played ZERO rated games — today or ever.** Its 25 archived games are
   all unrated (`coordination.md:49132`). It is not in the rated ledger.
2. **None of today's holder changes was one of OUR prototype leaks.** v134,
   v135, v137, v139, v142, v143 are **uploads by our human teammate x3r0** to the
   team's own slot — they were the *legitimate active submission* at every
   pairing they played. There is no non-incumbent version in the 275 games.

**OUR arm's prototype submissions today were `v138` (Loki rc8.7) and `v144`
(Loki rc9.1 / EVICT58)** — read off `scratchpad/md_leg_submit.log:5` and
`scratchpad/leg_evict58_submit.log:5`. Rated game rows carrying them:

```
v138: 0 rated game rows EVER
v144: 0 rated game rows EVER
```

**POSITIVE CONTROL — this check CAN come out the other way.** The same query on
known historical leaks returns non-zero: **`v105` → 5 rated game rows
(2026-08-10T12:52:59Z)** and **`v120` → 10 rated game rows (2026-08-12)**. A
version-census that only ever returns 0 would validate nothing; this one
returns the leak when a leak exists.

⇒ **Leaked rated exposure attributable to our prototype legs today: 0 matches,
0 games, priced at 0 × −8 = 0 Elo.**

**What DID cost, and it was authorised rather than leaked:** v135's single
pairing at 07:32:59Z went **0/5 for −13.89 Elo**. The tape records this as a
deliberate decision (*"Magnus: v135 gets one more ladder pairing (~07:32:59Z),
then rollback"*, `:45376`). Budgeting it at the −8/match leak rate would
**understate** it by 74%. **The −8 constant is a leak budget, not a price list
for authorised exposure.**

**And the larger number is the same shape:** the four holders between v125 and
v140 (v134/v135/v137/v139, 15 matches, 75 games, **33.3% share, −74.60 Elo**)
were all incumbent and all authorised — so this cost sits outside every
leak-accounting instrument the repo has. Our rating fell **1800.9 → 1724.2**
across that block.

> ⛔ **CORRECTED IN PLACE, 2026-08-14T18:40Z, by the research arm against the
> primary.** This line first read **32.0%**. Re-derived directly from
> `corpus/ladder_games.tsv` — rows with `created` on 2026-08-14 and
> `ourver ∈ {134,135,136,137,138,139}` — the block is **25 wins in 75 games =
> 33.3%**, not 24 in 75. `won` is encoded `'1'`/`'0'` (2,523/2,387 tape-wide),
> so there is no truthiness ambiguity to hide behind. **The direction, the
> −74.60 Elo, the 1800.9 → 1724.2 rating fall and every conclusion drawn from
> this block are unaffected** — the correction is recorded because a number
> published in a deliverable carries its own audit, not because it changed a
> verdict.

---

## 3. THE BAD CELLS

### 3a. Matches at 0/5 or 1/5 — eleven of 55 (20.0%)

Every game in every one of these eleven matches ended `core_destroyed` **except
one** (match 50, one `titanium_collected` at r1000). **We are being killed, not
out-tiebroken.**

| created | opponent | oppver | ourver | share | d | median turns | maps lost on |
|---|---|---|---|---|---|---|---|
| 01:52:59 | HTTP 418 | v103 | v125 | 1/5 | −8.36 | 169 | antl 205 · roya 282 · glac 158 · arch 169 |
| 03:52:59 | kladde chatte tville | v97 | v125 | 1/5 | −6.57 | 266 | antl 82 · icef 269 · arch 266 · drak 448 |
| 04:32:59 | Juusto | v11 | v125 | 1/5 | −8.82 | 129 | fros 129 · ragn 333 · roya 114 · auro 197 |
| 06:52:59 | HTTP 418 | v103 | v134 | 1/5 | −10.87 | 203 | arch 588 · glac 203 · ragn 155 · nord 150 |
| **07:32:59** | **0033** | **v56** | **v135** | **0/5** | **−13.89** | **130** | fros 104 · antl 130 · fjor 123 · midg 147 · drak 539 |
| 08:32:59 | LingLing40 | v48 | v137 | 1/5 | −11.41 | 111 | arch 109 · antl 339 · nord 111 · auro 104 |
| 09:52:59 | Big O | v19 | v139 | 1/5 | −10.63 | 234 | midg 270 · glac 169 · nord 385 · drum 234 |
| 10:12:59 | 0033 | v57 | v139 | 1/5 | −7.00 | 129 | ragn 843 · roya 164 · fros 121 · yule 126 |
| **10:52:59** | **LingLing40** | **v49** | **v139** | **0/5** | **−14.63** | **97** | antl 158 · fros 91 · arch 97 · drum 93 · valk 183 |
| 11:32:59 | The Bisons | v8 | v139 | 1/5 | −9.79 | 74 | fjor 119 · ragn 74 · icef 59 · drum 54 |
| 16:32:59 | HTTP 418 | v103 | v140 | 1/5 | −7.57 | 563 | drum 153 · auro 563 · fjor **r1000** · drak 815 |

**The two 0/5 matches are the day's worst cells: −13.89 (0033 v56 vs our v135)
and −14.63 (LingLing40 v49 vs our v139).** Both are pure core-kill sweeps.

**The Bisons 11:32:59 is the fastest death cluster on the board** — we lost at
turns **54, 59, 74, 119**, i.e. three of four losses before r80. *(UNTESTED
INFERENCE, flagged as such: that looks like a rush landing before our opening
completes. Nothing in this decode tests it — a replay read would.)*

**Nine of eleven bad cells fall in the 00:12–11:32Z block; only one (16:32,
HTTP 418) is in the v140 afternoon.**

### 3b. Opponents we are net-losing to today

| opponent | oppver(s) | matches | games | share | ±95% (DEFF 1.366) | net Elo |
|---|---|---|---|---|---|---|
| **HTTP 418** | v103 | 5 | 25 | **28.0%** | ±20.6pp | **−32.36** |
| **LingLing40** | v46, v48, v49 | 3 | 15 | 26.7% | ±26.2pp | **−24.77** |
| **0033** | v56, v57 | 3 | 15 | 26.7% | ±26.2pp | −15.87 |
| kladde chatte tville | v97 | 2 | 10 | 30.0% | ±33.2pp | −6.36 |
| Pantheon | v79 | 1 | 5 | 40.0% | ±50.2pp *(n=5, one match — not usable)* | +0.58 |
| Juusto | v11 | 3 | 15 | 46.7% | ±29.5pp | −3.75 |
| The Bisons | v8 | 3 | 15 | 46.7% | ±29.5pp | −3.70 |
| Jython | v136, v137 | 6 | 30 | 50.0% | ±20.9pp | −11.40 |
| Landers | v93 | 1 | 5 | 60.0% | ±50.2pp *(n=5, one match — not usable)* | −3.10 |

*(Jython and Landers show a negative net at ≥50% share — that is the game-share
scoring rule doing exactly what `CLAUDE.md` says: a 3-2 against a lower-rated
opponent can lose rating.)*

**Net-positive side, for the denominator's sake:** team lazy v226 **80.0%,
+56.29** over 5 matches; arsonist duck v24 **80.0%, +26.71**; Erebus v103
**53.3%, +15.18** over 6 matches.

⚠ **HTTP 418 (v103) and Erebus (v103) share a version tag and split opposite
ways** (28.0% vs 53.3%, 25 and 30 games). Reported as an observation. **No
mechanism story.** *(An `oppver` collision across two different teams is a
different team's version numbering, not a shared bot — that is a fact about the
column's grain, not a finding about either opponent.)*

**INSTRUMENT NOTE with teeth:** the `oppver` column is NOT constant across this
cut — LingLing40 alone moved v46 → v48 → v49 within one day, and 0033 moved
v56 → v57. A per-opponent share pooled across those versions is pooling
*different bots*, and no per-opponent row above should be read as a fixed
matchup rate.

### 3c. Deliberately no mechanism story

Per the brief: nothing in §3 is explained. The eleven bad cells are reported as
observations with their maps, conditions and turn distributions. The two
inference-shaped sentences above carry an **UNTESTED INFERENCE** label. Neither
was tested here and neither may be cited as a finding.

---

## 4. WIN-CONDITION MIX

Of **275 rated games** today:

| | core_destroyed | titanium_collected (r1000 tiebreak) |
|---|---|---|
| **our wins (140)** | **135 (96.4%)** | 5 (3.6%) |
| **our losses (135)** | **128 (94.8%)** | 7 (5.2%) |

**R1000 RATE, BOTH DIRECTIONS — `turns == 1000`: 11 of 275 games = 4.00%
(±2.86pp, DEFF 1.529).** Split **4 of our 140 wins (2.9%) and 7 of our 135
losses (5.2%)**. Under `R1000_IS_DEFEAT` the correct total is **11 defeats, not
7** — and the four r1000 "wins" are worth flagging to the builder because they
scored on the ladder while counting as programme defeats.

**Kill / death rounds (core_destroyed games only, so the r1000 tail cannot drag
the median):**

* **Median KILL round, our wins: 178** (n = 135; mean 234.4)
* **Median DEATH round, our losses: 182** (n = 128; mean 262.5)

That is a **four-round race**, tighter than the thirteen-round figure carried in
`CLAUDE.md` (median kill 174, median death 187 — a different and older
population).

Per holder:

| ourver | median kill (n) | median death (n) |
|---|---|---|
| v125 | 186 (52) | 182 (46) |
| v139 | **136 (12)** | **158 (25)** |
| v140 | 173 (48) | **293 (25)** |

**v140 is the only holder today whose median death is far behind its median
kill (293 vs 173).** v139's numbers are the inverse shape: it killed *faster*
than v125 (136 vs 186) and still ran 35.0%, because it died at 158.

### ⭐ THE SURPRISE — written down before any explanation

**Match 28 (09:12:59Z, diverge v20, our v139), game 5 on `archipelago`: a WIN
with `cond = titanium_collected` at `turns = 146`.** A tiebreak condition is
supposed to be reachable only at r1000.

Corpus-wide check: **1,060 `titanium_collected` rows exist; 1,058 have
`turns == 1000`; exactly 2 do not** — this one, and
**2026-08-12T10:12:59.502Z vs Powered by SmartFridge (our v115), turns = 140**.
**Both are on `archipelago`. Both are wins for us.** *(Separately, 25 rows carry
`cond = 'error'` with `turns = 0`; those are a different, already-known class
and are excluded.)*

**I have no explanation and am not offering one.** Two events, same map, same
direction, 2 of 1,060 — small enough to be coincidence, structured enough that
it should not be filed away. **Recommendation (not a verdict): pull the two
replays (`006f3c12…_game_5.replay26`, and the 08-12 SmartFridge game) and see
what ends a game at r140-146 with a tiebreak condition.** If it is an
early-termination path, it is an engine behaviour nobody in this repo has
written down.

---

## 5. INTERVALS — the procedure, performed and verified

**Step 1 — enumerate every cluster this data has.** Two: **MATCH** and
**OPPONENT**. (No window cluster is asserted; none has been shown to bind here.)

**Step 2 — for each stratum, does it hold more than one member of the cluster?
VERIFIED, not assumed:**

| stratum | MATCH cluster | OPPONENT cluster | DEFF |
|---|---|---|---|
| **pooled (all 275 today)** | **ALIVE** — games per match = exactly 5 in 55 of 55 matches | **ALIVE** — 14 of 17 opponents appear in >1 match | **1.529** |
| **per-ourver, v125/v139/v140** | ALIVE (20/8/16 matches) | **ALIVE** — max matches vs one opponent = 3/2/2 | **1.529** |
| **per-ourver, v134/v135/v137/v142/v143** | ALIVE | **DEAD** — max matches vs one opponent = **1** in every case | **1.366** |
| **per-opponent** | **ALIVE** — HTTP 418 = 5 matches, Jython = 6 | removed by construction | **1.366** |
| **per-map** (not quoted as a bar below) | **DEAD** — (match, map) cells with >1 game = **0 of 275**; all 55 matches use 5 distinct maps | ALIVE — 70 of 171 (map, opp) cells hold >1 game, m̄ = 1.61 | ≈1.07 |

The v134/v135/v137/v142/v143 row is the one that would be got wrong by a
taxonomy: those strata *look* like per-version cuts (which normally keep both
clusters) but each opponent contributes exactly one match inside them, so the
opponent cluster genuinely dies and 1.529 would over-correct.

**Step 3 — apply.** `half_width_95 = 1.96·sqrt(p(1−p)·DEFF/n)`.

| claim | n | p | DEFF | ±95% |
|---|---|---|---|---|
| **day share, all rated games** | 275 | 50.9% | 1.529 | **±7.3pp** |
| v140 share | 80 | 63.7% | 1.529 | ±13.0pp |
| v125 share | 100 | 52.0% | 1.529 | ±12.1pp |
| v139 share | 40 | 35.0% | 1.529 | ±18.3pp |
| r1000 rate | 275 | 4.00% | 1.529 | ±2.86pp |

**Two-fixture form, applied to the day's split** (afternoon 11:52–18:12Z, all
versions, 100 games vs morning 00:12–11:32Z, 175 games):
`1.96·sqrt(p̄(1−p̄)·(1.529/100 + 1.529/175))` = **±15.2pp** against an observed
gap of **63.0% − 44.0% = +19.0pp**. It clears — **narrowly**, and per the
`CLAUDE.md` direction clause a narrowly-cleared exclusion is exactly the exposed
class. **Treat it as suggestive, not established**, and note that the split is
confounded with the holder change (v140 took the slot at 11:40Z) — it is not an
independent test of v140.

**v135 (0/5) carries no interval:** the normal approximation is invalid at
p = 0 and n = 5 is a single match. No share claim is admissible from it; only
the Elo fact (−13.89) is.

---

## 6. WHAT I DID NOT DO

* No verdict sentence. §2c, §3 and §4 are observations; the two labelled
  inferences are labelled.
* No `meta_join.tsv` was read. Every denominator here is `ladder_games.tsv`.
* Versions were read per-match from the platform (`ourver`/`oppver`), never from
  the poll-time tag in `elo_history.tsv` — that tape was used only for
  activation *times*, and its LOCAL timezone was converted explicitly.
* The 18:32:59Z pairing is not in this decode; it did not exist on any surface
  at the writing clock.
