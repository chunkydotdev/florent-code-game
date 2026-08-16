# CERTIFICATE — `LEG-fieldcal-2026-08-16` — **CLEAR TO FIRE**

**Side lane, s44. Issued 2026-08-16T06:0xZ (`date -u`).**
**Subject:** `docs/prereg/LEG-fieldcal-2026-08-16.md`, locked at **`43d9035f`**.
**Scope of this certificate — stated before the verdict, because OB17 exists precisely because a
predecessor's scope note did not repair its headline:** this covers **LOCK DISCIPLINE, the
ARITHMETIC I recomputed, and OB17 EXECUTABILITY**. It does **not** certify the hypothesis, the
choice of bar, or whether the leg is worth firing — those are judgement and belong to the builder
and to Magnus.

---

## 1. TWO-CLOCK — **CLEAN**, and clock 2 is deliberately still open

    CLOCK 1  git AUTHOR time of the lock commit   2026-08-16T05:59:01Z   (43d9035f)
             pushed to origin/main                 YES — a hash a peer cannot see is not auditable
    CLOCK 2  platform createdAt of the FIRST ACCEPTED CHALLENGE of the leg   DOES NOT YET EXIST

**Verified at 05:59:37Z: the three newest unrated matches on the account are 05:50:26Z, 05:39:21Z
and 05:36:33Z — ALL PREDATE the lock, and all three are other-operator traffic (§9.6a), not this
leg.** ⇒ **zero challenges of this leg exist; the window is open and clean.**

⛔ **THE OBLIGATION THEREFORE TRANSFERS, and it is the one thing this certificate cannot do for
you: the FIRING SESSION records the first accept's `createdAt` off `fcode match list --mine --type
unrated` and quotes the gap against 05:59:01Z.** §1 already registers the correct definition — the
first ACCEPTED CHALLENGE, **not** the first result row, because a result row is written when a game
FINISHES and at a small gap that error decides the SIGN. **Nothing in this certificate substitutes
for taking that reading.**

## 2. §12.5's ASSIGNED MANUAL ITEM — **CELL VERSION CHURN: VERIFIED**

§12.5 hands this to the side lane by name (*"the checker verifies presence only… treat it as a
manual certification item or it will pass unfilled"*). Recomputed independently from
`corpus/league_matches.tsv`, distinct versions in the preceding 24 h:

    Juusto 1 ✓ · not adgato 1 ✓ · Erebus 10 ✓ · kladde 17 ✓ · gsxWins 6 ✓
    0033 2 ✓ · lingling_40h 3 ✓ · HTTP 418 1 ✓ · farming_200s 1 ✓
    The Bisons — archive reads 1 (v9) against a claimed 2

**9 of 10 exact.** The Bisons is **explained, not a defect**: the archive's newest row is
**04:52:59Z against a 05:59:01Z lock — 66 minutes of lag** — and the prereg's own parenthetical
names the second version (*"v9 pinned, v53 also live"*), i.e. read from a live surface the archive
has not caught up to. **§9.5 registers exactly this hazard and it is behaving as registered.**

### ⛔ AND MY OWN NEAR-MISS, RECORDED BECAUSE IT ALMOST BECAME A FALSE FLAG ON A LOCKED PREREG

**My first pass computed `kladde chatte tville` = 0 against a claimed 17** and I was one keystroke
from reporting a fabricated count. **The prereg writes `kladde chatte tville`; the archive carries
`kladde chatte tville (och oss)`.** Exact-match on a truncated name.
**Recomputed with the full name: exactly 17** — `['94','96','97','99','101','102','103','105','106',
'107','109','111','113','114','116','118','119']`.
⇒ **This is the two-names-one-team class `CLAUDE.md` records and that this lane's own retro (v1.11)
names as its most expensive failure — checking everything AROUND a claim and never its premise.**
The premise here was *"the name I am matching on is the name in the file."*

## 3. OTHER RECOMPUTED CHECKS

| check | result |
|---|---|
| `TARGET BAND` rating (doc says ours **1786**) | ✅ **CONFIRMED LIVE** — `fcode status`: 1786 (Emerald), 1089 matches, #18 of 126. *My own earlier reads of 1796–1802 were the stale ones; flagging would have been wrong.* |
| `prereg_check.py` on the locked file | ✅ **`PREREG_CHECK: OK`** — matching §12.6's stated requirement exactly |
| OB13 — metric read path in the treatment diff | ✅ `eco.py:813`; `eco.py` is the ONLY file differing between arms |
| OB17.1/.2/.3 — executable method | ✅ and §11 goes beyond the obligation: it reports **which clauses could have surprised**, and three did |
| §9.3 post-fire per-match `oppver` assertion, voiding cells | ✅ present, bar-level, with the right rationale (the guard catches an EMPTY pin, not a WRONG one) |
| §9.6a rate gate + §9.6b starting-cell rotation | ✅ **both halves** of `CLAUDE.md:551-552` registered, with the reason neither substitutes for the other |
| Impotence clause at BAR level, not prose | ✅ §1 |
| Cross-fixture constants labelled PLANNING | ✅ §1 DEFF block; §9.7 carries the cross-host caveat |
| §13 amendment clause | ✅ immutable, ADD-ONLY, blind-to-data, and an amendment after any result row excludes itself |

**Read by me, not taken on report:** §1, §9, §10, §11, §12, §13.

## 4. ⚠ THE ONE FINDING — A SUPERSEDED INTERVAL IN THE PRIORS, AND §9.9 ANTICIPATED IT

**§1 `BASE RATE SOURCE` quotes `BODYAWR: RMST₃₀₀ −6.84 rounds [−8.61, −5.08], n = 10,800`.**
**That interval is the SUPERSEDED two-sample form.** The estimator is PAIRED — both arms play the
same games, `corr ≈ −0.40` — so the correct interval is **[−8.95, −4.73]**, ~×1.18 wider (research
`4e7305e1`; independently recomputed by me at **×1.163–1.197** across seven shards).
**The POINT ESTIMATE −6.84 is unchanged, and the corrected interval still excludes zero.**

⭐ **§9.9 CARRIES A PENDING-AUDIT FLAG ON EXACTLY THESE NUMBERS AND IT IS HEREBY DISCHARGED:** the
side-lane audit is closed. **Every point estimate holds; only the intervals widen; no verdict among
the load-bearing arms moves** (BODYAWR and AWRLNCH still exclude zero, NULL114 still includes it,
NEG114 still slower). The prereg's own sentence — *"any figure that moves on audit moves this leg's
PRIORS, not its DESIGN"* — is correct and is what makes this a note rather than a blocker.
⛔ **Per §13 the document is IMMUTABLE: this correction lives here, not as an edit.** Nothing in the
leg's design, bar, estimator, falsifier or cells depends on the interval.

## 5. VERDICT

**CLEAR TO FIRE.**

**Three obligations that survive this certificate and belong to the firing session:**
1. **Record clock 2** — the first accepted challenge's `createdAt`, and quote the gap. Nothing here
   does it for you.
2. **`UNPINNED_OK` must never be set** (§9.3), and **every stream writes `scratchpad/arm_*.txt`**
   (§9.4.4) or `rate_budget.py` goes blind and the meter reports a free slot into a spent window.
3. **Gate on `rate_budget.py` before every invocation** (§9.6a) — the co-operator was consuming
   **40% of a window** while this certificate was being written, and a scheduler counting its own
   fires cannot see why it is being rejected.

**⭐ AND THE THING WORTH SAYING ABOUT THIS DOCUMENT RATHER THAN ABOUT ITS COMPLIANCE:** §1 registers,
before any game is fired, that **the leg will MISS its own primary at the true effect size**
(π ≈ 0.63 against the 0.92 the bar needs for 80% power; k ≈ 109 opponents required, ten exist).
**A prereg that states in advance the conditions under which its own headline will fail — and then
registers an impotence clause so nobody quotes that failure as a refutation — is the strongest form
of this artefact I have certified.** The falsifier, not the bar, is what this leg buys, and the
document says so itself.
