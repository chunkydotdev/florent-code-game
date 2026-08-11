# ⛔⛔ THE RING-HOLD CLAIM: THE ASSOCIATION REPLICATES, THE CAUSAL READING DOES NOT — AND `CLAUDE.md` CARRIES A CORRUPTED QUOTATION OF ITS OWN SOURCE

**Research arm, s31, 2026-08-11.** Commissioned by me against **my own lead
generator candidate**, because it rested on an inherited number I had not
re-derived. **Re-derived from scratch over 19,178 replays (13,935 third-party +
5,243 ours), 0 parse failures, 16.0M core-rounds.** Script
`scratchpad/ring_hazard_s31.py`; full output `scratchpad/ring_hazard_s31_out.txt`.

---

# ⭐ THE FINDING THAT OUTRANKS THE NUMBER: THE ALWAYS-LOADED FILE LOST ITS SOURCE'S CAVEAT

`CLAUDE.md` states, in the block every session loads at boot:

> *"one hostile body on the ring **DOUBLES** the 25-round core-death hazard,
> 2.24% → 4.77%, CIs disjoint"*

**The original is `docs/coordination.md:16649`, a research-arm entry from
2026-08-09. It says, in its own words, immediately under its own table:**

> *"**THE CAVEAT I AM NOT BURYING, raised by the agent itself: the 2× is partly
> REVERSE CAUSATION and cannot be separated from this data.** A core about to die
> is a core whose defenders are already dead — exactly when a body can stand on
> its ring. **The round-matched control being NULL at R=50 is consistent with that
> and is the most uncomfortable number in the set. Treat 2.1× as an UPPER BOUND,
> not an effect size.**"*

The same entry also records that **the effect PEAKS AT ONE BODY AND DECLINES**
(j=1 4.77% → j=2 4.01% → j=3 2.91%) and that the cut is **restricted to rounds
< 250**.

**⇒ FOUR THINGS WERE DROPPED IN TRANSIT INTO `CLAUDE.md`: the reverse-causation
warning, the "UPPER BOUND, not an effect size" instruction, the null at R=50, and
the r<250 restriction.** The original author did nothing wrong. **The number in the
always-loaded file is not the number they published**, and it reads as a
established causal effect because every hedge was stripped.

**This is the most expensive kind of defect this repo has: a caveat that dies in
transit into a file nobody re-derives, in the one document every lane boots on.**
It is the same shape as the s29 retro finding — *the one number that got worse was
the one a successor most needed* — applied to a load-bearing claim.

---

# 1. THE ASSOCIATION IS REAL AND REPLICATES AT 14× THE n

On the original's own cut (r < ~250): **clear 2.199% → occupied 5.858%**, against
their 2.24% → 4.77%. Pooled over all rounds, `≥1 body vs 0`: **1.656% → 4.742%,
×2.86**, n_clear = 12.6M, n_occ = 3.4M core-rounds. Game-clustered bootstrap CIs
(400 resamples) are 5–10× wider than Wilson and still disjoint.

**The descriptive number is not in doubt.**

# 2. DOSE SATURATES AT ONE BODY

FIELD (third-party): `1.529% / 4.001% / 4.892% / 5.165% / 5.347%` for 0/1/2/3/4+
bodies. **The first body buys +2.47pp; bodies two, three and four together buy
+1.35pp** — 55% of the dose is on the first body.
*(The original's outright DECLINE at j≥2 does not reproduce; mine is
flat-to-slightly-rising. Same practical conclusion: a presence effect, not a
stacking effect.)*

# 3. ⛔ THE CAUSAL READING FAILS FIVE INDEPENDENT CONTROLS

### 3a. POLARITY — the one that settles it

A core's **own** builder bots on its **own** ring. **They cannot damage their own
core.**

| friendly bodies on own ring | 25-round death rate |
|---|---:|
| 0 | 2.302% |
| 1 | 3.312% |
| **2** | **4.641%** |
| 3+ | 3.531% |

**×2.02 — statistically indistinguishable from the ×2.13 the inherited claim
attributes to a HOSTILE body.** *(INFERENCE: these are healers arriving because
the core is already under attack.)* **A predictor that works at nearly full
strength for bodies that provably cannot kill the core is measuring convergence,
not causation.**

### 3b. LAG — 68% of the effect survives 100 rounds

| predictor lag | occupied | clear | ratio |
|---:|---:|---:|---:|
| 0 | 4.941% | 1.727% | ×2.86 |
| 25 | 4.776% | 1.779% | ×2.68 |
| 100 | 4.173% | 1.998% | **×2.09** |

**A body that stood on the ring 100 rounds ago predicts death in the next 25
rounds at ×2.09.** A cause with a 25-round action window has nothing left at lag
100. *(The literal backward test I specified is structurally degenerate — a core
alive at r did not die in [r−25, r], so the backward rate is 0 by construction.
The agent substituted the lag table and said so.)*

### 3c. DISCORDANT PAIRS — ~75% of the effect is carried by a body that has left

`neither 1.563%` · **`ago_only` (ring provably CLEAR now, occupied 50 rounds ago)
4.581%** · `now_only 5.823%` · `now&ago 4.690%`.

**⭐ ONE ASYMMETRY WORTH KEEPING:** in `US_ATTACK` alone the pattern flips —
`now_only 6.566%` vs `ago_only 2.325%`, ×2.8 in the **causal** direction. **That is
the only cause-shaped cell in the analysis, it is us-only (n=49,559 core-rounds),
and it is observational.**

### 3d. NULL OUTCOME — does not go to null

Death in `(r+200, r+225]`: **×1.47**, down from ×2.86. **Occupancy now predicts
death two hundred rounds later.** ⇒ ×1.47 is unambiguously marker; ×1.9 is the
*most* a causal effect could be, and 3b/3c say most of that is marker too.

### 3e. SAME FORCE, DIFFERENT TILE — the plank's own manipulation

Holding core HP, enemy builders within d²≤36, and enemy turrets near the core
**fixed**, and varying only *where those same bots stand*: **44 of 56 cells have a
ratio BELOW 1.0.** Given the same force near a core of the same HP, moving it
**onto** the ring is associated with the core dying **less** often.

**The plank's manipulation is precisely "stand on the ring tile rather than one
tile off it." That contrast is null-to-negative.**

# 4. ⛔ THE RETENTION PLANK'S OWN NUMBER IS THE WEAKEST IN THE SET

Unstratified, restricted to rounds where the ring **is** occupied (presence held,
only duration varying): `1-5/25 → 3.559%` · `6-15/25 → 4.194%` ·
`16-25/25 → 4.962%`. **+1.40pp for a full camp against presence's +2.5pp.**

**And it INVERTS, monotonically, in every stratum with usable n** once core HP and
enemy-builders-near are held fixed — e.g. `hp 250-399, eb1`: `6.223% → 3.152% →
1.202%`. That is **immortal-time selection** (conditioning on "occupied 25 of the
last 25" conditions on the core having *survived* 25 rounds of it).

**Raw and stratified point in opposite directions, so neither identifies anything.
There is no duration number here a plank can be sized on.**

# 5. INSTRUMENT CONTROLS

* **Ring geometry** verified on a real replay, 12 tiles, **independently re-derived
  (4×4 box minus footprint) = identical**, every tile min d² ∈ {1,2}. Ring function
  **imported from `tools/ring_read.py`**, whose selftest was re-run: **40
  assertions, 0 failed, PASS.** *(`tools/ring_retention.py` is the retired wrong
  one, refuses to run, and imports `subprocess`+`fcode` — not touched.)*
* **Outcome variable** cross-validated against `corpus/events.tsv`: **agree 397,
  disagree 0**; winCondition consistent 500/500; **MUTANT CONTROL — shifting
  death_round by +1 drops agreement to 0.0%**, so the check can produce the other
  verdict.
* **Coverage stated, not dropped:** 19,178 decoded, **0 parse failures**; 177 of
  19,355 archive files (0.91%) excluded for having no `meta_join` row; 589,471
  core-rounds (3.55%) dropped as censored. Seats keyed on `teamAId`/`teamBId`
  (TRAP 7).

---

# VERDICT

**The 2.24% → 4.77% figure is real, replicates at 14× the n, and is not evidence
that a body on the ring kills cores. Its own author said so and `CLAUDE.md` lost
the sentence.**

**⇒ C1 RING RETENTION IS WITHDRAWN AS A GENERATOR CANDIDATE.** It was my lead
candidate; I commissioned the check against it; the check killed it. **It is not
queued and must not be queued on this evidence.**

**IF IT EVER GOES FORWARD**, it may not be pre-registered against core-death
hazard. The honest bar is the **rules-level** spawn-denial fact from the same
2026-08-09 entry — **0 spawns in 2,405,604 body ring-tile-rounds** — which needs no
causal identification. And `tools/target_value.py` must be run first regardless.

**THE ONLY INSTRUMENT THAT COULD SEPARATE THE TWO STORIES IS A LIVE LEG**, because
nothing in an archive can randomise the body's tile: **hold our raider on the ring
vs deliberately step it one tile off, same bot otherwise.** That, plus the
`US_ATTACK` asymmetry in 3c, is the entire surviving case.
