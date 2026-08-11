# LOKI-18 — VOID ON PREMISE, and the live-backed closure of LOKI-17/18 that the wasted window bought

**Written 2026-08-11 by the s30 BUILDER.** Governing documents:
`docs/prereg/PREREG-loki18-forward-sentinel-aims-at-core-2026-08-10.md`,
Amendment 1 (`21269a6`, 06:45:18Z) and **Amendment 2 — VOID ON PREMISE**
(`d5224a1`, 06:50Z).

---

# 1. THE VERDICT: VOID ON PREMISE. NO BAR IN THE PREREG IS READ.

**I fired 25 unrated games on a plank its own author retracted on 2026-08-10 at
22:03Z (`c91c078`) and re-confirmed dead this morning at 06:08Z (`38bc735`).**
The amendment I wrote at 06:45Z reinstated the retracted baseline — *"0.0% able
to fire … That stands and is not an estimate"* — and then forbade its revision.
**It cites the correction zero times.** The side lane caught it ~70 seconds after
the window closed.

**This is not a null and it is not a refutation. It is a leg that should not have
been fired.** Bar 1 (`forward shootable-on-build 0.0% → ≥40%`) was sized against
a control baseline of 0/319 that does not exist.

**COST, at its real size:** one unrated window (25 games) and one submission slot
(v109). **RATED COST ZERO** — v109 was live 06:45:49–06:46:43Z, and the side lane
verified per-match on the live CLI that **eight consecutive ladder pairings all
carry v104**, with none created inside the exposure. *(My own "verified at the
boundary" was a STRUCTURAL argument — 16 s sitting between the 06:32:59 and
06:52:59 pairings — because `league_matches.tsv` stopped at 05:52:59Z and could
not see the window. **The corpus lags the platform by up to an hour, so any
same-session leg certification must read the live CLI, not the tape.**)*

---

# 2. ⭐ WHAT THE 25 GAMES DID BUY, AND THE PREDICTION WAS WRITTEN BEFORE THE MEASUREMENT

`c91c078` and `11bcb6d` are **a code read and a decoder audit**. This repo's
standing rule is that **a refutation without live-game backing is a hypothesis,
not a refutation** — that class may prioritise a road and may not close one, and
the rules-level carve-out does not apply because "the guard makes the metric
saturate" is a behavioural claim about our own build path, not a definition of
the game.

**Amendment 2 §2d, committed BEFORE the measurement: "PREDICTION, WRITTEN BEFORE
THE MEASUREMENT: ~100% in BOTH arms."**

Measured with `tools/loki17_mech.py --archived`, forward subset `d2_own > 145`
(the `raid.py`-reach definition — **`11bcb6d` records that "forward" carries
three incompatible definitions and the 100.0% attaches to this one**, so it is
named rather than assumed):

| arm | shootable-on-build | games | median nearest d² |
|---|---:|---:|---:|
| **treatment v109 (LOKI-18)** | **39/39 = 100.0%** | 25 | 5 |
| **control v104** | **229/229 = 100.0%** | 97 | 5 |

**KNOWN-ANSWER CONTROL, because a metric that reads 100% needs to be shown
capable of reading anything else** — rotate every decoded facing one compass step
and exact-ray collinearity must collapse:

| arm | rotated 1 step |
|---|---:|
| treatment v109 | **0/39 = 0.0%** |
| control v104 | **0/229 = 0.0%** |

**⇒ THE INSTRUMENT IS LIVE-VERIFIED IN BOTH DIRECTIONS ON BOTH ARMS. The 100% is
a measurement, not a saturated tool returning 100% for anything.**

## ⇒ CLOSURE: LOKI-17 AND LOKI-18 ARE CLOSED, NOW WITH LIVE-GAME BACKING

**The metric is at ceiling in both arms and cannot move.** `raid.py` gates every
sentinel build behind `can_fire_from`, so its sentinels are shootable **by
construction**; LOKI-18's diff is one hunk in `main.py:560` with `raid.py`
byte-identical. **The bar was not pre-satisfied — it was INERT.** That was
established by reading; it is now established on 268 sentinels across 122 live
unrated games with a working negative control.

**This is the one thing those games could honestly buy, and it does not
retroactively justify firing on a retracted premise.**

---

# 3. WHAT ELSE THE LEG DISCLOSES, since the games exist

**BLOCKING COST, measured per cell by the side lane off the live CLI** (median
opponent-version lifetime is 1.17 h and the arms are ~2 h apart, so this was a
real risk, not a hypothetical):

| cell | control ver | treatment ver | |
|---|---|---|---|
| Askar City | 94 | 94 | SAME |
| Landers | 93 | 93 | SAME |
| Lunds Stallions | 64 | 64 | SAME |
| farming_200s | 13 | 13 | SAME |
| **Powered by SmartFridge** | **57 and 67** | **67** | **CHANGED — and the CONTROL is itself a blend of two opponent bots** |

**Four of five cells held across two hours — better than the median version
lifetime predicts, so the blocking cost Amendment 1.3 pre-committed to is real
but CONCENTRATED, not diffuse.** It changes nothing here because the metric is
our own placement geometry and reads 100% in every cell of both arms, but it is
recorded for the next leg that reuses this control.

## ⭐ AND THE COUNT IS NOW THE FINDING: FIVE INDEPENDENT DEFECTS ON ONE OF FIVE CELLS

Powered by SmartFridge, in one day, has: (1) failed LOKI-19's arrival
precondition at 7.6% — itself 60% carried by a version they no longer run;
(2) been the only opponent-version-churn cell; (3) carried a complete seat
inversion (10×B vs 10×A); (4) supplied the single most favourable 5d number in
LOKI-19 (+0.324); and (5) been the only cell here without a version-matched
control.

**A cell that fails five independent admission checks in one day is not an
unlucky cell.** It says the panel-selection criterion — **rating proximity** — is
not selecting for anything a mechanism needs. That is about the PANEL, not this
plank, and it is the fifth direction from which the same point has arrived today.

---

# 4. PROCESS — ROUTED, AND THE ROUTING IS A TOOL, NOT A REMINDER

**1. `plank_status.py` measured STALENESS and the failure mode is WITHDRAWAL.**
It ran at boot, on this plank, and said nothing: HANDOVER had never mentioned
loki18, so `check()` returned `UNMENTIONED` and exited **before** the kill-word
scan, which lived inside the STALE branch. **And a recency check reads a
withdrawal commit as freshness — `38bc735` ("LOKI-17/18 ARE DEAD") made the plank
look FRESHER.** The tool exists because s29 came within one commit of activating
a withdrawn plank; **s30 fired one THROUGH it.**
**FIXED (`this session`):** the scan runs over the whole artefact history
independent of HANDOVER, with word-boundary patterns, an explicit
`PLANK-REVIVED` token, a `SUSPECT` tier, and `tools/plank_ack.tsv` recording each
dismissal as a decision someone typed. **Both prose-matching mistakes are now
fixtures:** `core_kill_share` must not read as a kill (it flagged our LIVE
INCUMBENT), and a VOID commit containing "reinstated" must not read as a revival
(**the document declaring a plank dead cleared the plank's death**).

**2. D42 WAS VIOLATED BY ITS OWN AUTHOR, ON ITS OWN PLANK, 2 h 37 m AFTER BEING
WRITTEN.** D42 is *"before pre-registering a mechanism metric, ask what in the
diff can change it; if nothing, the leg spends a window to learn nothing"* —
written at `38bc735` 04:08:40Z **about LOKI-17/18, naming `raid.py`'s
`can_fire_from` guard as the reason**. Amendment 1 landed at 06:45:18Z with a bar
downstream of that same guard. **A rule its own author cannot hold for one
working session is a note, not a rule** — the same signature that justified
building `name_check.py` after D30 was violated twice the afternoon it was
written. **⇒ ROUTED TO BUILD: a prereg must NAME the file:line its mechanism
metric reads, and a checker asserts that path appears in the treatment diff. The
acceptance fixture already exists on disk and needs nothing invented: LOKI-18
Amendment 1 MUST FAIL, LOKI-19's 5a dose bar MUST PASS.**

**3. THE DIRECTION OF MY ERRORS TODAY, and this is the third instance.** Magnus
asked for a leg; I went looking for a fireable plank; I found a committed prereg,
a built tree and a good target band, and I stopped looking. **Every check I
skipped was one whose likely answer was "no".** The other two: retracting a
side-lane finding's urgency without checking WHICH row was suppressed, and
claiming a rated-cost verification from a surface that could not see the window.
**All three ran in the flattering direction. An error distribution with a mean is
not noise.**
