# SCREEN PREREG — `bodyblock` (QUEUE #70): ZERO IDLE-AND-FREE — the terminal fallback is a FREE verb

Drafted by a **fresh opus subagent with no inherited session context** beyond the
inputs listed under `PROVENANCE`. **Research commissioned this draft and supplies
the evidence; the OWNING LANE IS THE BUILDER** — `bots/_v262bodyblock` is their
tree, they ratify every ⚖ line, and they type the lock commit. This agent wrote
no file under `bots/`, appended no row to `scratchpad/corefill_work.txt`, ran no
`fcode` platform command, and committed nothing.

**STATUS: drafting began BEFORE `bots/_v262bodyblock` existed on disk** (verified
at **07:49Z**: `ls bots/ | grep -i bodyblock` → **empty**; `grep -rn "BODYBLOCK\|bodyblock" bots/_v223sealrepair/`
→ **0 hits**). ⛔ **THE TREE LANDED MID-DRAFT — the builder created it between
07:49Z and 08:03Z while this document was being written. That is recorded rather
than smoothed over, and §0.5 carries what changed as a result.** This document is
still committed **BEFORE the `BBLOCK70` shard is appended to
`scratchpad/corefill_work.txt`** and **BEFORE its first game**, which is the lock
that matters. Two-clock form:
this commit's git author time against the shard tape's own `# FIXTURE … start=`
stamp, which `tools/overnight.sh:96-100` writes **before the first game** (a
START, not a first-completed-row). Drafting session wall clock at write time:
**`2026-08-15T07:55:56Z`** (`date -u`, same shell call), repo HEAD `d5a2ead0
2026-08-15T09:54:38+02:00`.

---

## 0. ⛔ READ THIS BEFORE RATIFYING — FOUR THINGS THIS AGENT FOUND THAT CHANGE THE DESIGN

**(0.1) THE #54 FALSIFIER'S INSTRUMENT DOES NOT EXIST ON DISK.** `QUEUE.md`'s #54
says *"census scripts in scratchpad (`nav_limit_cycle_census.py`)"* and the row's
own s42 annotation says *"the census that supplies its dose is currently
MISSING"*. **Verified: `find . -name "*nav_limit*" -o -name "*oscillation*"`
returns no script; `scratchpad/nav_limit_cycle_census.py` is absent.** The
mandated falsifier therefore had no executing tool. **This agent rebuilt a STRICT
detector from the row's own prose in `/tmp` tonight and drove it to BOTH verdicts
on 8 local games** (§8.3). It is a **PROTOTYPE, not a validated instrument** —
OB17 clause 2 is registered as a **BLOCKING pre-fire condition**, not waved
through.

**(0.2) ⭐ THE MECHANISM METRIC *IS* READABLE ON THE LOCAL SURFACE — MEASURED
TONIGHT, AND IT IS THE OPPOSITE OF THE CPU CASE.** `SCREEN-bodyaware-2026-08-14.md`
established that local replays carry **no exec-time fields**, so no local fixture
can see CPU. **That does NOT generalise.** This agent ran one throw-away local
game (`bots/_v223sealrepair` vs itself, midgard, seed 999777, `--tle 10`, replay
to `/tmp`) and ran `scratchpad/idle_split_s31.py`'s own `walk()` over it:

```
turns 275 · core death r274 · anomalies 0
builder SetActionCooldown writes {1: 200} · SetMoveCooldown writes {1: 2268}
cooldowns at PLACEMENT {(0,0): 28}
bucket A/B/C/D classify cleanly; bucket D = 0
```

⇒ **local replays carry the verb updates (2/13/15/16) and BOTH cooldown updates
(7/8), so bucket A is measurable on this fixture.** ⛔ **But corefill runs
`--replay /dev/null`, so the SHARD cannot carry it** — the read must come from a
separate **kept-replay batch** (§8), exactly as `BODYAWARE` structured its
pre-fire gate.

**(0.3) ⛔ THIS IS NOT A ONE-HUNK ARM, AND THE PRECEDENTS ON THIS FIXTURE ARE.**
`GUNAXABL` moved one constant; `SENTTHREAT` moved one hunk. A terminal fallback
needs (i) a "did this turn emit a verb" signal that **does not exist in the
tree**, (ii) a destination scorer, (iii) a nav call. `_builder` dispatches to
**three** terminal branches — `main.py:445-451`, `self._raid` / `self._defend` /
`self._expand`, with `_expand` reachable from a **second** call site at
`main.py:689`. **Where the fallback attaches, and how "terminal" is enforced, is
a ⚖ RATIFY decision the builder owns** (§3.1), and the weaker attribution is
declared here rather than discovered at read-out.

**(0.4) THE SEGMENT PREDICTION RUNS *OPPOSITE* TO THE NAIVE READING.** Long walks
mean more idle time to fill — which argues for the 900-area maps. **The
deliverable is a BODY ON A DENIAL TILE, not a move emitted**, and occupancy =
arrival × dwell. On a 30×30 map an idle builder ordered to their spawn ring
spends its idle rounds *walking*, scores as ACTIVE, delivers nothing, and raises
the exposure the #54 falsifier watches. ⇒ **PRIMARY SEGMENT is the 10 ≤676-area
maps, EXPECTED DIRECTION POSITIVE there and ~ZERO-or-NEGATIVE on the five
900-area maps** (§2, §10).

---

## 0.5 ⛔⛔ THE TREE LANDED WHILE THIS WAS BEING WRITTEN — WHAT IT CHANGES, READ AT A STAMPED CLOCK

**Read at `2026-08-15T08:04:34Z` (`date -u`, same shell call), `git status` =
`?? bots/_v262bodyblock/` (untracked), file mtimes 09:54–10:03 local (07:54–08:03Z)
— i.e. THE TREE WAS STILL BEING WRITTEN AT READ TIME.** Everything in this section
is a snapshot of a moving target and must be **re-read by the builder before the
lock**. It is here because three of the four findings change what this document
registers.

### (1) IT IS A 641-LINE, FOUR-FILE DIFF — NOT "a single toggle"

```
main.py       871 ->  908    (  37 changed lines)
eco.py       1242 -> 1253    (  11)
doctrine.py  1686 -> 1827    ( 141)
raid.py       958 -> 1410    ( 452)   <-- +47% of the file
```

**The brief handed to this agent said "v140 + single toggle `LOKI_BODYBLOCK_ON`".
The tree on disk is 641 changed lines across four files, and `raid.py` — which
this document's `TREATMENT DIFF TOUCHES` line did not list before this section was
written — carries 452 of them.** ⇒ **`TREATMENT DIFF TOUCHES` is corrected in §2
to include `raid.py`.**

**⛔ AND THE CONSEQUENCE FOR ATTRIBUTION IS THE ONE THAT MATTERS.** The registered
control is `bots/_v223sealrepair`, a DIFFERENT TREE. A KEEP or a REAL NEGATIVE is
therefore attributable to **all 641 lines**, not to the bodyblock behaviour. The
tree's own master flag says `LOKI_BODYBLOCK_ON = True   # MASTER. False ==
_v223sealrepair, exactly.` — **an equivalence CLAIM, not an equivalence
MEASUREMENT.**

**⚖ RATIFY — REQUIRED: A FLAG-OFF NULL, and it is cheap.** Build
`bots/_v263bbnull` = `_v262bodyblock` with `LOKI_BODYBLOCK_ON = False` and run it
against `bots/_v223sealrepair` for **≥1,000 games** at seedbase 355000. **Pass
condition: share inside 50 ± 3.07pp** (the n=1000 half-width). ⛔ **A drift here
means the 641 lines are NOT inert with the flag off and the screen's contrast is
not the contrast this document registers.**
⚠ **The naming is forced, not stylistic:** `overnight.sh:78-80` refuses on a
SUBSTRING basename collision in either direction, so a control named
`_v262bodyblock_off` (which CONTAINS `_v262bodyblock`) would be **refused**, and a
name that slipped past an equality-only check would score ~100% for the treatment.
`_v263bbnull` collides with neither.

### (2) THE ARM IS A BUNDLE, AND ITS FIRST CLASS IS **PAID**, NOT FREE

The tree's destination classes, read at `doctrine.py:1731-1827`:

| class | what it does | flag | free? |
|---|---|---|---|
| **0 TERMINAL PECK** | idle builder beside an enemy CONVEYOR/SPLITTER melees it | `LOKI_BB_PECK_ON = True`, **`LOKI_BB_PECK_TI_FLOOR = 20`** | ⛔ **NO — 2 Ti/swing and bank-floor-gated at 20 Ti** |
| **0b OPPORTUNISTIC** | one step onto the tile a visible enemy builder is about to enter | `LOKI_BB_OPP_ON = True` | yes |
| **a GUNNER SHIELD** | stand in a live enemy gunner's fire line | **`LOKI_BB_SHIELD_ON = False`** | — **SHIPPED OFF** |
| **b SPAWN DENIAL** | an unoccupied tile of the enemy core's 12-tile spawn envelope | `LOKI_BB_BLOCK_ON = True` | yes |
| **c ORE DENIAL** | an ore tile in their half | ″ | yes |
| **d BELT PINCH** | an empty tile pinched between two live enemy belt pieces | ″ | yes |

**⛔ THE BRIEF'S CENTRAL ARITHMETIC DOES NOT DESCRIBE CLASS 0.** The case handed to
this agent — *"at q1 = 12 Ti every PAID verb is unaffordable simultaneously; a move
is not"* — is an argument for a **FREE** terminal. **Class 0 costs 2 Ti and carries
a 20 Ti bank FLOOR, so it is switched off in exactly the bank state that motivated
the plank** (LOSS q1 = 12 Ti). That is not necessarily wrong — a paid verb that
fires at median 26/53 Ti is still a verb — **but the "0 Ti, never bank-gated"
sentence may not be quoted as a description of the arm.** It describes classes
0b/b/c/d only.
**⇒ §8.2's G2 gate ("paid verbs must not fall by >5%") now has a second job: class 0
makes paid verbs RISE. G2 is therefore restated as a two-sided check — |Δ| ≤ 5% for
build+heal, and ATTACK reported separately with no bar**, because the peck lands in
the attack column by construction and would otherwise trip a gate it is supposed to
trip.

### (3) ⭐ A ROUND-RUN GATE EXISTS THAT THE DELIVERY BAR MUST BE SCORED AGAINST

**`LOKI_BB_IDLE_RNDS = 6`** — *"how long a body must be useless before it is
RELOCATED… the peck has no such gate."* ⇒ **the relocation half of this arm cannot
touch a builder-round that is not part of a ≥6-round idle run**, and the archive
says idleness is largely BURSTY: per-builder A-share has **median 0.000, mean
0.292**, with only **1.17 (LOSS) / 1.36 (WIN) builders per game at A-share ≥ 0.8**
out of 4.76 / 5.44 alive (`scratchpad/idle_split_out.txt:48-51`).

**⇒ G1 IS RESTATED BEFORE THE FIRE, because as originally written it could not be
met by construction:** the bar is scored on **bucket-A rounds that fall inside a
≥6-round consecutive idle run** — the arm's actual addressable population — and
**TOTAL bucket A is reported beside it, unbarred, because that is the number
Magnus's directive names.** ⛔ **The addressable fraction of bucket A is UNMEASURED
and this document does not invent it; the §8 batch computes it, and if it is small
the honest finding is "the plank addresses a minority of the idle pool", which is a
result about the design.**

### (4) WHAT THE TREE GETS RIGHT, recorded so this section is not read as an objection

The anti-oscillation requirement of §3.3 is **met and exceeded**:
`LOKI_BB_TRAIL = 6` tiles (the brief required ≥4) · `LOKI_BB_STALL_MAX = 3`
blocked steps before a destination is abandoned · `LOKI_BB_BAN_RNDS = 80` ·
`LOKI_BB_HYSTERESIS = 3` · `LOKI_BB_RESCAN = 20` · **and, in the tree's own words,
*"when no fresh legal step exists it STANDS STILL and counts a stall rather than
taking the stale step — the stale step is the lock."*** That is the #54 hazard
answered by construction rather than by a promise. H1 is answered too: relocation
destinations are enemy-half-tested via the raid layer's `_salt_forward`, with the
gunner shield named as the one exemption **and shipped OFF**.
**⚖ AND §3.1's ATTACHMENT QUESTION IS ANSWERED BY THE BUILDER, NOT BY THIS AGENT —
the builder re-reads §3.1 and records which of (A)/(B)/(C) the tree implements,
because §5's Obligation 13 intersection claim depends on it.**

---

## 1. THE BRIEF, RECORDED AS HANDED (not re-derived)

Plank: `QUEUE.md` **#70** — *"ZERO IDLE-AND-FREE — an idle builder must always
emit a verb, and the terminal fallback is a free one: BODYBLOCK"*, provenance
**Magnus, 2026-08-15**, verbatim: *"I want us to get as close to 0% idle and free
builders as possible. If they cant heal or build or peck, they can still
bodyblock and be annoying."*

Treatment `bots/_v262bodyblock` = v140 (`bots/_v223sealrepair`) + single toggle
`LOKI_BODYBLOCK_ON`. **TERMINAL FALLBACK ONLY**: it fires after the existing
action ladder has declined every verb. An idle-and-free builder is given a NAMED
destination and moves toward it; **the move costs 0 titanium and is never
bank-gated.**

Control `bots/_v223sealrepair` (v140, LIVE incumbent, md5 of concatenated `*.py`
= `c4e563af4730b4c1595c679fc25098e7`, re-verified by this agent and matching the
figure `SCREEN-gunaxabl` recorded on 2026-08-14 — the control has not drifted).

---

## 2. REGISTRATION BLOCK

**TARGET BAND: N/A — LOCAL corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. The rated-value question is owed later, by a live leg (§9).**
**PINNED: N/A — local self-play. The control is a byte-frozen tree on disk, so there is no opponent version to pin and no churn to absorb; `CLAUDE.md`'s pin/never-pin rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — `CLAUDE.md`'s enumeration PERFORMED in §4, not asserted. Applicable DEFF = 0.98 (local pair-weighted, ρ = −0.020, 124 shards, s39 audit).**
**ESTIMATOR: unweighted treatment game share = rows with `winner == T` over all non-comment, non-`NOWINNER` rows of `scratchpad/overnight/BBLOCK70.tsv`. One local row is one game, so game share and win rate are the same number on this fixture; the "match win rate is not a verdict" rule governs the PLATFORM and does not reach here. No map weighting, no seat weighting, no pooling with any other shard.**
**TREATMENT TREE: bots/_v262bodyblock — DOES NOT EXIST AT LOCK TIME. This agent is forbidden to write under `bots/`; the builder builds the tree to the spec in §3 and re-runs `tools/prereg_check.py --fire` once it is `git add -N`'d.**
**PLANNED n: 10800 games**
**BOUNDARY: 10800 shard rows = 10800 games (LOCAL fixture: 1 row = 1 game. The platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption, §12, and `tools/prereg_check.py:616-634` models it explicitly.)**
**CUT-SHORT: floor 5400 games. Below 5400 rows nothing is read and no branch is claimed; rows are KEPT and remain poolable with a later completion of THIS shard on THIS seed base and with nothing else. At 5400 ≤ n < 10800 the ONLY claims permitted are branch 1 or branch 2 read at that n's own wider band (±1.320pp ⇒ KEEP needs ≥ 52.32%, REAL NEGATIVE ≤ 48.68%), NEVER branch 3 — an under-powered shard cannot deliver a "could not separate" verdict, because that is what an under-powered shard always says. Floor (5400) ≤ planned n (10800).**
**BAR: 51.93**
**BASE RATE: 50.00**
**BAR SOURCE: constructed, not observed — `50.00 + MDE(1.00pp) + half_width(0.93pp)`. Half-width recomputed here as ±0.933pp from `1.96·sqrt(p̄(1−p̄)·0.98/10800)` at the conservative p̄ = 0.5. Clearing this bar means the 95% interval excludes BOTH 50.00 AND the +1.00pp indifference threshold — the MDE is INSIDE the bar's construction, not beside it (OB16 as amended 2026-08-14T23:56:13Z). ⛔ This is therefore NOT a standard-corefill-band screen: per the OB16 corollary of 2026-08-15T03:52:45Z the standard 48.67/51.33 band has an implied MDE of 0.000pp and licenses no exclusion of any effect size. This bar does.**
**BASE RATE SOURCE: structural null of a seat-balanced paired local screen — `tools/overnight.sh:125-136` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 the expected treatment share is exactly 50.00. No historical population is consumed by the bar. ⚠ CORROBORATING CELL, DISCLOSED NOT CORRECTED: `NULL125` (`bots/_v198null125`, a renamed byte-identical copy of `_v197mapcode`, vs `_v197mapcode`) read 51.04% ±1.32 at n=5400 on this same 15-map pool; its interval 49.72–52.36 contains 50, so 50.00 stands — but the null cell ran ~1pp HIGH and there is NO null cell on the v140 chassis itself, so a marginally-clearing KEEP is the reading most exposed to that residual. `NULL5400` (seedbase 344000) is live and is the cell that would fix this.**
**REFERENCE n: none** — the comparator is generated inside the same shard from the same seeds; no fixed external reference contributes a variance floor.
*(⚠ TOOL BUG FOUND WHILE CHECKING THIS FILE, reported not worked around: `tools/prereg_check.py:346` `int_before()` does `re.search(r"([\d,]+)\s*\b", s)` and then `int(...)`. A comma in a digit-free prose value matches `[\d,]+`, so `int("")` raises and **the whole checker CRASHES with a traceback instead of reporting a FAIL** — no check runs at all. Triggered here by a `REFERENCE n:` value containing a comma. Repro: `int_before("none - a, b", r"\b")`. **A crash reads to an operator as "my document is malformed" when it means "the tool is broken", which is this repo's signature defect wearing new clothes.** The line above is written in the precedent's `**KEY: value**` form to route around it; the fix belongs in the tool.)*
**MECHANISM METRIC READS: bots/_v223sealrepair/main.py:445-451 — the terminal of `_builder`'s role dispatch (`self._raid` / `self._defend` / `self._expand`), observed as BUCKET A, the share of OUR builder-rounds in which both cooldowns are 0 at round start AND no verb update (2 move / 13 attack / 15 heal / 16 build) is emitted. Classifier: `scratchpad/idle_split_s31.py`'s `walk()` + bucket rule, VERIFIED BY THIS AGENT TO RUN ON A LOCAL REPLAY (§0.2, §8.1). TREATMENT DIFF TOUCHES: bots/_v262bodyblock/main.py, bots/_v262bodyblock/doctrine.py, bots/_v262bodyblock/eco.py, bots/_v262bodyblock/raid.py — CORRECTED IN DRAFT after the tree landed mid-write (§0.5): 641 changed lines across FOUR files, 452 of them in raid.py. INTERSECTION: YES — the fallback IS the new terminal of the dispatch the metric classifies, so with `LOKI_BODYBLOCK_ON = False` the counter is the shipped 29.01%/17.77% and with it True the counter must fall; the metric cannot read identically in both arms. ⛔ AND THE ASSERTION IS NOT SELF-CERTIFYING: it becomes COMPUTED only when the builder re-runs `tools/prereg_check.py --fire` against the built tree (§5).**
**TREATMENT DIFF REFS: HEAD -- bots/**
**METRIC WINDOW: r1–r1000, read at three fixed sub-windows — `[0,10]`, `[40,60]`, `[T−20,T]` where T is the round the decisive core dies.**
**GATING CONSTANTS: SLOT_ENEMY_CORE seeded from MAP SYMMETRY at round 0 by the CORE (`main.py:166-167` → `eco.py:38-53 enemy_core_for`, a dimensions-and-anchors table with a point-reflection fallback, so it is terrain not opponent-identity). Comms writes are BUFFERED, so the anchor is visible to builders from ROUND 1. No other round gate in the tree constrains a builder MOVE: `HUNT_MIN_RND=120`, `MEDIC_MIN_RND=150`, `LOKI_COLD_INSERT_RND=150`, `LAUNCHER_MIN_RND=160`, `SURGE_MIN_RND=300`, `LOKI2_RUSH_RND=60`, `REPLACE_MIN_RND=60` all gate SPEND or ROLE, none gates movement. THE ARM ITSELF MUST CARRY NO ROUND GATE — if the builder adds one, this line is stale and the prereg is amended ADD-only BEFORE the fire.**
**MECHANISM CAN OCCUR IN WINDOW: yes for r1–r1000, i.e. in all three sub-windows. ⚠ NO at round 0 exactly (no anchor yet), so the `[0,10]` window contains 10 of its 11 rounds as usable — stated because it is the one round where a zero is structural rather than behavioural.**
**GATE RESOLUTION: see §6.4 — GATE-1000 is UNRESOLVED BY CONSTRUCTION (±3.07pp against a 2.0pp boundary); GATE-2700 (±1.87pp) resolves only outside 48.63–52.37; GATE-5400 (±1.32pp, added because "halfway" must move with n) resolves only outside 49.58–52.22. PRE-COMMITTED DEFAULT: these are FUTILITY gates, so the PERMISSION is continuing to spend cores and the RESTRICTION is the DROP — an UNRESOLVED futility gate DROPS the shard. ⛔ AND THE POWER COST OF THAT DEFAULT IS COMPUTED IN ADVANCE IN §6.4 RATHER THAN DISCOVERED: it kills ~82% of arms whose true effect is exactly +1.5pp. That number is on the ⚖ RATIFY list.**
**PRE-STATE: neither the outcome nor the mechanism is already in its predicted state. OUTCOME — no bodyblock tree exists; the only reading on this chassis-and-pool cell is the structural 50.00 of a tree against itself, so 51.93 is demonstrably NOT already there. MECHANISM — grepped at the primary this session, not relayed: `grep -rn "BODYBLOCK\|bodyblock\|body_block" bots/_v223sealrepair/` = 0 hits; `_idle_rotate` (`main.py:797`) is guarded GUNNER-only at `:801` and is reached only from the TURRET path at `:757`; `grep -riE "SLOT_IDLE|idle.*destination|idle.*broadcast"` finds only `_salt_idle_ok` (`raid.py:362`, a raid-station salt gate, not an idle handler). Bucket A sits at 29.01% LOSS / 29.44% WIN at `[T−20,T]`, not at the predicted near-zero, so a null cannot be blamed on a treatment that was already true.**
**MAP SEGMENT: the 10 ≤676-area maps — antler, archipelago, auroraveil, drumlin, fjordgate, frostgate, icefloe, nordkap, royale, yulerune — versus the 5 900-area maps (drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie).**
**PRIMARY SEGMENT: the 10 ≤676-area maps. MECHANISM: the deliverable is OCCUPANCY OF AN ENEMY-HALF DENIAL TILE, and occupancy = arrival × dwell. Arrival cost scales with approach length, for which map area is the available proxy; and the 900-area maps carry 3–6× the nav-lock base rate (midgard 35.6% of builder-rounds, ragnarok 14.1%, valkyrie 12.8% vs small maps 3–8%, #54 census over 1,160 v125 games) that this plank's own falsifier watches. On a 30×30 map the fallback converts idle rounds into WALKING rounds that score as ACTIVE and deliver no body.**
**EXPECTED DIRECTION: POSITIVE on-segment (treatment share ABOVE its pooled share on the 10 ≤676-area maps) and ~ZERO-OR-NEGATIVE off-segment (at or below pooled on the 5 900-area maps).**
**SEGMENT VALUE CEILING: 66.7% × 3.0pp on-segment = 2.00pp pooled. ⛔ AN ADMISSION, NOT A FORECAST — see §2.1.**
**CELLS: N/A — not a panel. One control tree, pinned by being a file.**
**CELL VERSION CHURN: N/A — not a panel; no opponent cells exist, so there is no 24 h distinct-version count to take (Ob. 14 N/A by shape).**
**POOL ERA: post-2026-08-13-rotation** · **POOL_ERA: post-2026-08-13-rotation**
*(both spellings deliberately — the underscore form is the lane's, the spaced form is what `tools/prereg_check.py` parses; normalise to one when the format lands)*. The 15-map pool at `tools/overnight.sh:68`: antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune.
**SPANS-POOL-CHANGE: no — the shard starts and ends inside the current pool era.**
**DOSE: STRUCTURAL dose is 1 → 0 idle-fallback branches: the control has NO builder-side idle handler (grep above) and the treatment has one. BEHAVIOURAL dose is BUCKET A, measured on the ARCHIVE at 3.31%/3.12% `[0,10]`, 17.77%/16.86% `[40,60]`, 29.01%/29.44% `[T−20,T]` (LOSS/WIN, 8,338 games, 894,638 builder-rounds — reproduced by this agent from `scratchpad/idle_split_out.txt` line-by-line, §7). ⛔ THE ARM-VS-ARM DOSE IS NOT MEASURED AND IS GATED BY §8 — n=0 games of the built arm have been played by anyone at lock time, which is the honest denominator and is why §8 is a BLOCKING gate rather than a companion read.**

### 2.1 ⛔ THE CEILING IS AN ADMISSION, NOT A FORECAST

**2.00pp pooled is roughly 2× this screen's 95% half-width and ~2× the registered
MDE.** It is the largest pooled effect this document will put its name to.

⚠ **THE CONVERSION FROM "IDLE BUILDER-ROUNDS RECOVERED" TO "GAME SHARE" HAS NEVER
BEEN MADE IN THIS REPO AND IS NOT MADE HERE.** It is the same missing arithmetic
`SCREEN-sentthreat-2026-08-14.md` declared for builder deaths (*"a VALUE case, not
a COUNT case, and it needs its own number"*). **This document does not smuggle it
in.** #14's own row says it plainly and it is carried, not quoted away: *"an idle
round is not necessarily a wasted one."*

**EXACTLY ONE PRIMARY SEGMENT (Ob. 15b).** Every other cut on this shard —
per-map, per-seat (`ORD` A vs B), per-`cond`, per-turn-count, per-role — is
**DESCRIPTIVE ONLY** and may not rescue a pooled fail. **Ob. 15c applies:** a
pooled fail that clears the pre-declared primary segment in the predicted
direction buys a **NEW screen with its own n and its own seed base**; these rows
may never confirm it.

**Proxy dilution, declared (Ob. 15's own warning turned on this page).** The
mechanism names **APPROACH LENGTH TO AN ENEMY-HALF DENIAL TILE**, and no per-map
approach table exists in the repo at draft time. **Map area is a declared proxy
and a proxy dilutes** — the segment reads weaker than a true mechanism-specific
split would. **The §8 kept-replay batch emits per-map arrival latency for free,
which is the route to replacing the proxy with the real property before any
re-screen.**

---

## 3. THE ARM — spec, and the three points the builder must decide

### 3.1 ⚖ RATIFY — WHERE THE FALLBACK ATTACHES, AND HOW "TERMINAL" IS ENFORCED

`bots/_v223sealrepair/main.py:445-451`, the tail of `_builder`:

```python
        self._wire_tick(ct)
        if self.role == "raid":
            self._raid(ct)
        elif self.role == "defend":
            self._defend(ct)
        else:
            self._expand(ct)
```

**There is no "did this turn emit a verb" signal anywhere in the tree.** Three
attachment designs are available and they are NOT equivalent:

| design | how "terminal" is enforced | cost |
|---|---|---|
| **(A) post-dispatch probe** — after the dispatch, re-read `ct.get_action_cooldown()` and `ct.get_move_cooldown()`; if both are still 0 the turn emitted nothing | **engine-side, cannot be fooled by our own bookkeeping** | one extra pair of getters per builder-turn |
| **(B) explicit flag** — every `build/attack/heal/move` site sets `self.acted = True` | precise, but touches **many** sites ⇒ a large diff and a real chance of a missed site | large diff, missed-site risk |
| **(C) wrapper** — the three role methods return a bool | clean, but changes **three** signatures and every `return` inside them | medium diff, many returns |

**⚖ THE RECOMMENDATION, and the reason is measured rather than aesthetic: (A).**
Bucket D is **0.00% at all three windows in both arms** across 894,638
builder-rounds, **every `SetActionCooldown`/`SetMoveCooldown` ever written for a
builder is `1`**, and **placement is `(0,0)` in 115,624 of 115,624 cases**
(`scratchpad/idle_split_out.txt:118-121`). ⇒ **both cooldowns are 0 at the start
of every builder-round without exception, so "both still 0 after the ladder ran"
is exactly equivalent to "no verb was emitted" — the same predicate the mechanism
metric uses, read from the engine instead of from our own flags.** Design (A)
makes the arm's trigger and the arm's metric the *same* quantity, which is the
strongest form of Obligation 13 available here.

⚠ **IF THE BUILDER PICKS (B) OR (C), §5's INTERSECTION CLAIM WEAKENS** — the
trigger and the metric stop being the same predicate and a missed site becomes a
silent non-delivery. **Say so in the amendment; do not change it silently.**

### 3.2 ⚖ RATIFY — THE DESTINATION SCORER, AND THE TWO HAZARDS THAT SHAPE IT

`#70` names four destinations in cost order:
**(a)** stand in an enemy gunner's fire line (a gunner's shot is a straight line
that does NOT pierce, so one body blanks it — 0 Ti, 0 ammo) ·
**(b)** stand on their core's spawn-adjacent tiles (spawn-tile denial, one of the
three roads `CLAUDE.md` records as never balance-changed) ·
**(c)** stand on the ore tile they want a harvester on ·
**(d)** stand in the belt corridor so their builder must path around.

**⛔ HAZARD H1 — PASSABILITY IS TEAM-BLIND, SO OUR OWN BODY BLOCKS OUR OWN
BUILDERS.** `Tile::is_bot_passable@0x2eabc` **returns false for ANY tile holding a
live builder bot** — disassembly, not inference
(`docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md:171`, quoted at the
primary by this agent). **And the cost is already sized on this exact chassis:
`SCREEN-bodyaware-2026-08-14.md` measured that the FIRST refused nav step is a
builder-bot tile in 67.6% of refusals = 21.8% of ALL nav rounds, and 40.5% of
refusals are FRIENDLY bodies.** A bodyblock body is *parked*, so unlike a transient
walker it never clears.
⇒ **HARD CONSTRAINT: every destination must lie in THEIR HALF** (`d²` to the enemy
core anchor < `d²` to our own core — the same midline test `idle_split_s31.py`
uses for its forward/home split, `walk()`'s `fwd()`). **Destinations (c) and (d)
are the two most likely to be mis-sited into OUR half, where a bodyblock walls our
own belt-layers out of their own corridor.** ⚖ **The builder states, in the arm,
which of (a)–(d) are enabled and asserts the midline test on every candidate.**

**⛔ HAZARD H2 — DESTINATION (b) SITS INSIDE THE ENEMY LAUNCHER PICKUP ENVELOPE BY
CONSTRUCTION, AND IT IS PRICED AS A TRADE, NOT AVOIDED.** Pickup is **d² ≤ 2, no
team check, no vision guard, 0 ammo, cooldown += 1, POSITION-ONLY mutation**
(`CLAUDE.md`, engine-read). Standing on their core's spawn-adjacent tiles IS that
envelope.
**The exposure is ASYMMETRIC IN OUR FAVOUR: their throw costs them 0 ammo and one
cooldown; our thrown builder SURVIVES.** ⇒ **the cost is the WALK-BACK, not the
unit**, and a bodyblock beside their core may well be worth being thrown for.
**Cross-reference `QUEUE.md` #59 (`DON'T GET FARMED`), which is the row that
already knows this and is open:** `_bfs_direction` (`eco.py:809-832`) adds an
enemy LAUNCHER to `blocked` — **verified at the primary: `eco.py:830` puts
`LAUNCHER` in the tuple that does `blocked.add((ep.x, ep.y))`, i.e. its OWN TILE
ONLY** — and the only envelope penalty in the tree, `LOKI_EXILE_PENALTY = 24`
(`doctrine.py:1286`), is read at **exactly one site, `raid.py:809`, inside the
RAID STATION picker.** **The eco/idle walk path has nothing.**
⇒ **#70 and #59 are ONE DESIGN.** ⚖ **The builder decides whether the bodyblock
destination scorer carries a launcher-envelope term at all**; §8.5 registers the
walk-back metric either way, so the trade is measured rather than assumed.

**⛔ ENGINE-BARRED VERB, STATED SO NOBODY ASSUMES OTHERWISE: BUILDER MELEE CANNOT
TARGET AN ENEMY BUILDER BOT.** `can_fire = False` on an adjacent enemy builder,
**every occurrence**, banked in `QUEUE.md` #45 from the s37 FEEDER45 dose.
**"Peck" only ever means an enemy BUILDING.** ⇒ a bodyblock body standing beside
an enemy builder has **no** melee option; the only anti-body tools in the game are
**turret fire and launcher eviction**. *(Hedge carried from #45's own wording: the
finding is PREDICATE-LEVEL — ungated `fire()` was not tested, per the side lane's
scope rider. Do not upgrade it here.)*

### 3.3 ⚖ RATIFY — THE ANTI-OSCILLATION REQUIREMENT, AND HOW A VIOLATION IS DETECTED

The brief requires **committed progress toward a named destination plus an
explicit recent-tile memory (≥4 tiles; refuse a return unless no alternative)**.

**WHY IT IS NOT OPTIONAL, in the tree's own terms:** `_nav` (`eco.py:898-910`)
already treats **`desired.opposite()` as a successful move**, and `self.stuck += 1`
fires **only when all four moves fail** — so a backstep never increments the stuck
counter and the only exits (`p == self.tgt`, `stuck >= 5` at `eco.py:1226`) can
never trigger inside a two-tile loop. **A bodyblock destination that is
unreachable feeds exactly this defect a new, permanent target.**

**⛔ DETECTION IN THE READOUT — TWO INDEPENDENT SIGNALS, NEITHER OF WHICH IS THE
BUCKET-A COLUMN:**
1. **`F-LOCK` (§10, the #54 falsifier)** — locked-builder-round share, treatment
   vs control, from the detector in §8.3. A violation of the memory requirement
   shows up here as a **rise**, and per §10 that **refutes the plank regardless of
   bucket A**.
2. **RECENT-TILE VIOLATION COUNT (descriptive, same batch)** — the share of
   bodyblock-driven moves whose destination tile is in the mover's own last-4-tile
   set. **Under a correctly-implemented memory this is structurally 0**; a non-zero
   reading is an implementation bug and **no bucket-A number from that batch may be
   read**. ⇒ this is a both-ways check: it can return the other verdict.

### 3.4 HOT-TURN COST — **ADDS**, on exactly the rounds that currently do nothing, and the local instrument for it is DEAD

* **ADDS:** a destination scorer plus one `_bfs_direction` call on builder-rounds
  that currently emit nothing and therefore currently cost almost nothing. **Bucket
  A is 17.77% of builder-rounds at `[40,60]` and 29.01% at `[T−20,T]`, so the added
  work lands on roughly one builder-round in five to one in three.**
* **⛔ NO LOCAL FIXTURE CAN MEASURE IT IN µs.** `ct.get_cpu_time_elapsed()` returns
  0 under local `fcode run` (`doctrine.py:1072`), and `tools/tle_census.py` on a
  LOCAL kept replay returns `tled / exec_sum / exec_max / over10k = 0` across 1,649
  builder-turns while the same decoder reads 8,847 µs on platform replays
  (`SCREEN-bodyaware-2026-08-14.md` §7, live positive control). **A clean local
  screen is NOT a clean CPU result.**
* **The gate therefore binds the SHIP, not the screen, in two halves:** a **LOCAL
  PROXY** (§8.2 G4 — `_bfs_direction` node-expansions per builder-turn, both arms;
  a Python counter, not an engine timer) and the **PLATFORM GATE**
  (`tools/monitors/cpu_watch.py`, alarm at 9,200 µs against a worst observed
  8,847 µs — **~353 µs, 3.5% headroom**). Budget for the alarm firing and for an
  immediate rollback on the first live leg.

---

## 4. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

1. **MATCH cluster — DIES.** A local corefill shard has no 5-game match wrapper;
   each row is an independently seeded single game (`tools/overnight.sh:121`,
   `seed = SEEDLO + n/16`, one `fcode run` per (seed, map, ORD) triple at
   `:135-136`). **No stratum can hold two games from one match because no match
   object exists.**
2. **OPPONENT cluster — DEGENERATE.** Exactly one opponent
   (`bots/_v223sealrepair`) for all 10,800 rows; no between-opponent contrast is
   drawn, so there is no multi-member opponent stratum to inflate.

⇒ **Applicable DEFF = 0.98** (local pair-weighted, ρ = −0.020, 124 shards, s39
audit). **The platform constants 1.529 rated / 1.833 unrated are NOT imported** —
over-applying a correction is an error in the same family as omitting it, and here
it would widen every interval by 24–35% for correlation that is not present.

⚠ **WHERE THIS COULD BITE, DECLARED:** the s39 audit found local outlier arms with
strong map interaction at **DEFF ≈ 1.20–1.25**, and this arm **declares a map
segment**. ⇒ **the segment split is INDICATIVE**; a segment claim is banked only
via the Ob. 15c re-screen, never off these rows.

⛔ **CROSS-HOST RIDER (OB16/OB12 rider, 2026-08-15): THIS SHARD IS REGISTERED
WITHIN-HOST.** The 0.98 exemption was measured without separating within-host from
cross-host pooling, and the s42 cross-host finding (2 of 3 identical-arm pairs
outside ±1.87pp, mixed directions, n=3, hinging on 0.053pp) prioritises a
measurement it does not establish. ⇒ **`BBLOCK70` runs on ONE host and pools with
nothing. If it is ever split across hosts, the host term is named and registered
BEFORE the split, not reconciled after.** *(`NULL5400`, seedbase 344000, is the
commissioned measurement that settles it.)*

---

## 5. OBLIGATION 13 — the intersection, stated exactly

```
MECHANISM METRIC READS:  bots/_v223sealrepair/main.py:445-451  (the terminal of
                         _builder's role dispatch), observed as BUCKET A
TREATMENT DIFF TOUCHES:  bots/_v262bodyblock/{main.py, doctrine.py, eco.py}
INTERSECTION:            YES — declared, NOT YET COMPUTED (the tree does not exist)
```

**Why the intersection is real and not decorative:** with `LOKI_BODYBLOCK_ON =
False` the fallback branch does not execute, so bucket A is **structurally the
shipped 29.01%/17.77%**; with it True the branch is precisely what converts a
verb-less builder-round into a move. **LOKI-18's failure — a metric behind a guard
whose behaviour could not differ between arms, reading 100%/100% — cannot occur
here.** And under attachment design (A) (§3.1) the arm's *trigger predicate* and
the *metric's classifier* are literally the same quantity read from the engine.

⚠ **TOOL STATE, REPORTED RATHER THAN WORKED AROUND.** `OB13_INTERSECTION` is
computed from `git_diff_paths()` (`tools/prereg_check.py:1075-1094`), which shells
`git diff --name-only <refs>` and defaults to `HEAD`. **The working tree at draft
time carries ~40 modified/untracked paths under `corpus/`, `scratchpad/` and
`elo_history.tsv` from concurrent shards.** `TREATMENT DIFF REFS: HEAD -- bots/`
scopes the diff to where an arm can live. **At draft time the arm tree does not
exist, so the check renders CANNOT-COMPUTE — the tool's own legitimate case for a
prereg locked before its tree (`prereg_check.py:1078-1082`).**
⇒ **The builder must `git add -N bots/_v262bodyblock` and re-run with `--fire`
before firing; at that point a FAIL is real, and `--fire` also escalates the
Obligation 17 `METRIC WINDOW` block from WARN to FAIL.**

### 5.1 THE CHECKER WAS RUN AGAINST THIS FILE. HERE IS ITS OUTPUT AND THE RESPONSE TO EACH ITEM

`.venv/bin/python tools/prereg_check.py docs/prereg/SCREEN-bodyblock-2026-08-15.md`
— 24 presence checks `ok`, all arithmetic checks `ok`, **one FAIL and eight
WARNs.** Reported rather than tuned away:

* **`FAIL OB13_UNTRACKED_ARM`** — *"the arm tree EXISTS on disk and git does not
  track it, so `git diff` returns nothing… `git add -N` the tree before firing."*
  ⇒ **CORRECT AND EXPECTED.** The tree landed mid-draft (§0.5) and is `??`
  untracked. **This is the one blocking item the builder clears with one command,
  and until they do, `PREREG_CHECK: FAIL` is the true state of this document — not
  a formatting artefact.**
* **`OB13_INTERSECTION: CANNOT-COMPUTE`** — the tool's own words: *"This is NOT
  'checked and clean' — the check did not run."* Carried as such; §5's YES is a
  DECLARATION until `--fire` computes it.
* **8 × `OBLIGATION 17, PARTIAL WINDOW`** — the checker discovered
  `HUNT_MIN_RND=120`, `MEDIC_MIN_RND=150`, `LOKI_COLD_INSERT_RND=150`,
  `LAUNCHER_MIN_RND=160`, `SURGE_MIN_RND=300`, `LOKI2_RUSH_RND=60`,
  `REPLACE_MIN_RND=60` inside the declared r1–r1000 window and warns that the early
  part of the window cannot contain the mechanism. **⇒ INSPECTED, AND THE WARNINGS
  DO NOT BIND — with a reason per constant, not a blanket dismissal:** every one of
  them gates a **SPEND** or a **ROLE**, and the mechanism here is a **MOVE**, which
  is the one verb no titanium gate can reach (that is the plank's entire premise,
  §7). The checker cannot know this and is right to raise it. ⛔ **BUT ONE OF THEM
  BECOMES LIVE UNDER §0.5: `LOKI_BB_PECK_TI_FLOOR = 20` is a real bank gate on
  class 0, and it is NOT in the checker's discovered list because it lives in the
  ARM, not the control.** ⇒ **the `GATING CONSTANTS` line must be re-declared to
  include `LOKI_BB_PECK_TI_FLOOR=20` and `LOKI_BB_IDLE_RNDS=6` once the tree is
  tracked, and `--fire` re-run.** *(This is exactly the failure OB17 exists for: a
  gate the author did not know about. It was found because the checker was run, and
  it was found in the ARM rather than the control — a place the checker does not
  look.)*
* **`WARN DOSE line carries no n=`** — addressed in §2 (`n=0 games of the built arm
  at lock time`).

---

## 6. HYPOTHESIS, DECISION RULE, SIZING AND GATES

### 6.1 ⚖ RATIFY — HYPOTHESIS (one sentence, falsifiable)

*Giving an idle-and-free builder a terminal, zero-titanium fallback — a NAMED
destination in the enemy half, reached by a committed walk with recent-tile memory
— converts idle builder-rounds into denial occupancy and raises our pooled LOCAL
game share against the shipped v140 tree to **51.93% or higher at n = 10,800**,
without raising the #54 nav-lock rate and without slowing the kill.*

**⛔ AND THE HYPOTHESIS HAS A CREDIBLE OPPOSITE, WHICH IS WHY IT CAN FAIL — three
named channels, not a hedge:**
1. **H1 self-blocking.** Parked friendly bodies are permanent obstacles to our own
   builders on a chassis where 21.8% of nav rounds already propose a step into a
   body.
2. **Displacement.** A builder that walks away is *somewhere else next round*. The
   `[T−20,T]` bucket-B split says **93.69% of active HOME builder-rounds in a LOSS
   are HEALS** (`idle_split_out.txt:104`) — i.e. the idle bodies this plank
   redirects are standing exactly where the core-repair work appears. **Walking
   them into the enemy half can trade a heal-in-reserve for an annoyance.**
3. **Lock inflation.** An unreachable destination feeds `_nav`'s
   backstep-is-success defect a permanent target (§3.3).

### 6.2 ⚖ RATIFY — EXPECTED DIRECTION (pooled): ABOVE 50.0; and INSIDE THE BAND is the modal outcome

**This document registers "inside the band" as the expectation so that a clear
result is a SURPRISE and reads as one.** Grounds: the conversion from recovered
builder-rounds to game share has never been measured (§2.1); the nearest built
arm on this row-family, **`DEST14A`** (`bots/_v228dest14a`, #14 arm A —
destination-for-the-idle-builder, the plank this row *absorbs*), is on the
worklist as a direction prior and is **not** a comparator in any bar on this page.
⚠ **`DEST14A` is a DIFFERENT ARM (no terminal fallback, no free verb) and pooling
its rows with these is barred.**

### 6.3 n, MDE and resolution — sized off the value we must EXCLUDE, never one we hope to observe

**MDE: +1.00pp. WE WILL CALL THIS ARM A MISS IF ITS TRUE LOCAL EFFECT IS AT OR
BELOW +1.00pp OF GAME SHARE.**

**There is no observed point estimate to size off and that is deliberate** — the
treatment tree does not exist, so nothing here can be circular (OB16's whole
point). The indifference threshold is derived from the arm's PRICE, which is
knowable before any row:

> **This arm adds a scorer and a BFS to the hot path on ~1 builder-round in 5, on a
> chassis measured at 8,847 µs of a 10,000 µs budget with an alarm at 9,200 µs
> (~3.5% headroom) and NO local µs instrument — and unlike `BODYAWARE`, which
> carried the CPU price alone, it carries THREE additional named self-harm
> channels (§6.1). An arm with strictly more named risk than `BODYAWARE` cannot
> honestly carry a SMALLER indifference threshold than the +1.00pp `BODYAWARE`
> registered on the same chassis and fixture.**

| quantity (p̄ = 0.5, DEFF 0.98) | n = 10,800 |
|---|---|
| σ (game share) | **0.4763pp** |
| 95% half-width | **±0.933pp** |
| smallest excluded effect at the bar | **1.00pp** |
| true effect needed to CLEAR the bar with 80% power | **≥ 2.33pp** (= 1.93 + 0.8416·σ) |
| n needed to EXCLUDE 1.00pp (half-width < 1.00) | **9,412** ⇒ 10,800 is the next multiple of 30 |
| n needed to DETECT 1.00pp at 80% power | **19,230** — NOT bought, and this leg does not claim it |

**⇒ WHAT THIS LEG CAN AND CANNOT DO.** It can separate *"worth more than a point"*
from *"worth a point or less"*. It **cannot** distinguish *"worth 0.6pp"* from
*"worth nothing"* — that needs 19,230 games (3.6 standard shards) and is not being
bought.

**⚖ RATIFY — THE CHEAPER ALTERNATIVE, PRICED SO THE CHOICE IS DELIBERATE.** A
single 5,400-game shard gives ±1.320pp, which forces the bar to **52.32%** and
raises the 80%-power requirement to **≥ 2.89pp** (= 2.32 + 0.8416·0.6736) — a bar
this arm has no reason to clear. **10,800 is the smallest n at which the registered MDE is expressible.**
⛔ **If the lane will only fund 5,400 cores, the MDE is RE-REGISTERED at +1.39pp
BEFORE the fire and the bar recomputed to 52.32 — the bar is never quietly moved
while the MDE stays on the page.** *(Scheduling reality at draft time:
`scratchpad/corefill.log` reads `hold: running=1/1 … unstarted=1` at
2026-08-15T07:47:28Z — **one worker slot, one shard already queued**. A
10,800-game leg at one worker is a multi-day commitment. **This is the single
biggest practical objection to the registered n and it is the builder's call, not
this agent's.**)*

| quantity | in pp | **in games (of 10,800)** |
|---|---|---|
| **BAR (KEEP)** | **≥ 51.93** | **≥ 5,609** |
| DROP BAND | 49.07 – 51.93 | 5,300 – 5,608 |
| **REAL NEGATIVE** | **≤ 49.07** | **≤ 5,299** |

### 6.4 GATES (Obligation 12 — sized, with the default's power cost computed in advance)

`docs/prereg/RULE-futility-gates-2026-08-13.md` binds every shard from its first
row and is read **ONCE each at first crossing**; the builder types the decision,
the watcher never decides.

* **GATE-1000 (n ≥ 1000), rule "drop if share < 48.0%".** Half-width **±3.07pp**;
  the boundary sits 2.0pp from 50, **inside its own interval**. **UNRESOLVED BY
  CONSTRUCTION**, declared before the fire. Label on a drop: `FUTILITY-EARLY`.
* **GATE-2700 (n ≥ 2700), rule "drop if share ≤ 50.5%".** Half-width **±1.87pp**.
  Resolved only at share ≤ 48.63% or share > 52.37%; **UNRESOLVED between.** Label:
  `FUTILITY-ALONE`.
* **GATE-5400 (n ≥ 5400) — the true halfway of a 10,800-game leg, added because
  Magnus's rule was written for a 5,400 shard and "halfway" must move with n.**
  Rule: **drop if share ≤ 50.9%.** Derivation, not taste: the final informative
  edge is 51.93, so finishing from ≤50.9 at halfway requires the second 5,400 to
  run **≥ 52.96** — a worse buy than re-spending the cores. Half-width **±1.32pp**;
  resolved only outside 49.58–52.22.
* **Not an ablation arm** (LOW does not determine the decision on its own), so the
  `DECISION-REACHED` clause does not apply.

**⭐ THE DEFAULT, AND ITS DIRECTION.** Obligation 12's rule is *"an unresolved gate
takes the RESTRICTION, never the PERMISSION."* **Here the gates are FUTILITY
gates: the permission is CONTINUING to spend cores on an arm that has not shown
itself; the restriction is the DROP.** ⇒ **an UNRESOLVED futility gate DROPS the
shard.** A futility drop is **not a refutation**: rows are KEPT, the arm stays a
combo ingredient, and the label is recorded with its n and share.

**⛔ ⚖ RATIFY — AND THE PRICE OF THAT DEFAULT IS COMPUTED HERE RATHER THAN
DISCOVERED AT READ-OUT, BECAUSE IT IS LARGE.** The strict CI reading and the
standing rule's literal POINT reading are **not** the same filter:

| true effect | GATE-2700 as a **POINT rule** (drop iff observed ≤ 50.5) | GATE-2700 with **UNRESOLVED ⇒ DROP** (survive only if observed > 52.37) |
|---|---|---|
| **+1.5pp** (a genuine KEEP-worthy arm) | survives **85.3%** | survives **18.1%** |
| **+1.0pp** (exactly the MDE ⇒ a registered MISS) | survives **70.0%** | survives **7.5%** |
| **+2.5pp** (well above the bar) | survives **98.2%** | survives **55.4%** |

⇒ **The strict default kills ~82% of arms whose true effect is +1.5pp — i.e. it
makes the registered 10,800-game MDE unreachable in practice for most of the
effect range the leg was sized for.** `SCREEN-bodyaware-2026-08-14.md` registered
the strict form; **`RULE-futility-gates-2026-08-13.md`, which is the standing rule
and binds every shard, is written as a POINT rule.**
**THIS DOCUMENT REGISTERS THE POINT RULE AS OPERATIVE** (it is the standing rule)
**and puts the divergence on the ⚖ RATIFY list with the arithmetic above**, so the
builder chooses deliberately. **Whichever is chosen, the choice is made BEFORE the
first row.**

### 6.5 ⚖ RATIFY — DECISION RULE

| final at n = 10,800 | in games | branch |
|---|---|---|
| **≥ 51.93%** | **≥ 5,609** | **KEEP-dev.** The interval excludes both 50.00 and +1.00pp. **Mandatory next steps, both OWED before any verdict sentence cites mechanism:** the §8 delivery gate (if not already taken), a **D26 replication** at seedbase 354000 scored alone, and the **CPU release gate** (§3.4), which this branch does **not** automatically pass. **No ship implication** — `SHIP_SIT` governs and v140 is sitting. |
| **49.07% – 51.93%** | 5,300 – 5,608 | **COULD NOT SEPARATE → DROP; `main.py:445-451` unchanged.** Per the pre-committed UNRESOLVED default: the restriction, never the permission. ⛔ Written as *"the screen could not separate the effect from the ≤1.00pp indifference region at ±0.93pp on this fixture"*, **NEVER** as *"the effect is zero"* and never as *"idle builders are fine as they are"*. |
| **≤ 49.07%** | **≤ 5,299** | **REAL NEGATIVE → road closes for the FALLBACK form.** Bodyblocking costs us. The plausible mechanism is named in advance (§6.1): H1 self-blocking plus the loss of a heal-in-reserve. **`#70` then narrows to a DESTINATION-only plank (i.e. back to `#14` arm A) and the "free terminal verb" idea is retired.** ⚠ **The negative branch is deliberately NOT symmetric with the positive one** (0.93pp below 50 against 1.93pp above): a credible harm kills an arm that also costs CPU and carries three self-harm channels, so no indifference margin is granted on the downside. |

**D26:** any final with |share − 50| ≥ 2.0pp (≤ 5,184 or ≥ 5,616 games) replicates
at seedbase 354000.

**⚖ RATIFY — the single sentence:** *only a final ≥ 51.93% that ALSO clears the
§8 delivery gate, the §10 `F-LOCK` falsifier and the §9 kill-round rider keeps this
arm alive; the band, everything below it, and a failure of any of those three drop
it and leave `main.py:445-451` unchanged.*

---

## 7. THE EVIDENCE — REPRODUCED AT THE PRIMARY, NOT COPIED

**Instrument: `scratchpad/idle_split_s31.py`** (s31 research, read-only; decodes
`replay_archive/*.replay26` + `corpus/meta_join.tsv` + `corpus/events.tsv`).
**Output re-read by this agent at `scratchpad/idle_split_out.txt`
(mtime 2026-08-15 09:41 local = 07:41Z, i.e. this session's run).** Every figure
handed to this agent in the brief was checked against that file line by line and
**all match**:

| claim in the brief | value in `idle_split_out.txt` | line |
|---|---|---|
| bucket A `[0,10]` 3.31% LOSS / 3.12% WIN | 5,878/177,334 = **3.31%** · 5,267/169,055 = **3.12%** | :73, :79 |
| bucket A `[40,60]` 17.77% / 16.86% | 82,375/463,483 = **17.77%** · 77,372/458,938 = **16.86%** | :61, :67 |
| bucket A `[T−20,T]` 29.01% / 29.44% | 124,509/429,167 = **29.01%** · 137,031/465,471 = **29.44%** | :19, :24 |
| **bucket D = 0.00% at ALL THREE windows, BOTH arms** | **0 / 0.00%** at every one of the six cells | :22,:27,:64,:70,:76,:82 |
| every builder cooldown ever written is `1`; placement `(0,0)` | `{1: 4,192,185}` action · `{1: 10,409,853}` move · `{(0,0): 115,624}` placement | :118-120 |
| titanium at T−1: median 26 LOSS / 53 WIN, q1 12 | median **26** / **53**, LOSS q1 **12** | :127-128 |
| 8,338 games / 894k builder-rounds | 8,338 games · 429,167 + 465,471 = **894,638** builder-rounds | :4,:18,:23 |
| idle headcount at T−1 1.44 / 1.62 | **1.44** / **1.62** builders/game | :31, :37 |

**THE INSTRUMENT CARRIES ITS OWN BOTH-WAYS CONTROLS, which is why it is usable:**
CONTROL 1 reproduces the anchor's headcount on the anchor's *own* instrument
(`events.tsv`); CONTROL 2b gives a **verb-blind** forward share so a flat bucket C
can be told from a broken classifier (2.86% at `[0,10]` vs 41.15% at `[T−20,T]` —
it moves); CONTROL 3 is the cooldown sanity read; CONTROL 4 shows the residual
non-behavioural explanations for an idle-looking round are **0.00% TLE, 0.19%
died-that-round, 0.15% no-`BotOutput`** — i.e. bucket A is ~99.7% genuine choice.
**`anomalous builder-rounds (verb emitted while cooldown>0) = 0`.**

**⚠ THREE SCOPE FACTS THE HEADLINE NUMBERS DO NOT CARRY, ADDED HERE:**
1. **The population is games with EXACTLY ONE core death — 8,338 of 9,231 archived
   games with us on a side. 884 games with ZERO core deaths (r1000 tiebreaks) are
   EXCLUDED**, and the `[0,10]` / `[40,60]` control windows are computed over the
   same core-decided subset. ⇒ **the decay curve describes DECISIVE games. It is
   not a whole-archive rate.**
2. **`#14`'s 25.76% is a `[T−20,T]`-ONLY figure** on an older population and **must
   not be quoted as a whole-game rate**. Today's `[T−20,T]` reading is 29.01%.
3. **`q1 = 12` is the LOSS quartile** (WIN q1 is 23). The arithmetic against
   `_eco_spendable`'s `ti >= cost + SIEGE_HEAL_RESERVE_TI(16)` under siege
   (**verified at the primary: `eco.py:228-235`, `SIEGE_HEAL_RESERVE_TI = 16` at
   `doctrine.py:437`**) is a LOSS-side argument, which is the side that matters.

**⛔ AND ONE THING THE ARITHMETIC DOES *NOT* SAY, because it is the mistake nearest
to hand: A MOVE IS FREE IN TITANIUM, NOT IN TURNS.** `CLAUDE.md`: *"acting or
moving is mutually exclusive per round for builder bots."* The fallback is
harmless **only because it is terminal** — the round it consumes had already
declined every verb. ⇒ **"terminal" is a property that must be VERIFIED, not
asserted, which is what §8.2's G2 is for.** *(The next-round cost is zero and this
is measured, not assumed: every cooldown ever written is 1 and ticks at end of
round, so both cooldowns are 0 at the start of every builder-round — bucket D =
0.00%.)*

---

## 8. ⛔ THE PRE-FIRE DELIVERY GATE — the shard may not be SCORED until this passes

`tools/overnight.sh:135-136` runs `--replay /dev/null`, **so the shard tape
(`ts shard game map seed seat winner cond turns`) cannot carry ONE mechanism
number.** The mechanism read is a **separate kept-replay batch** — the same
structure `SCREEN-bodyaware-2026-08-14.md` used.

### 8.1 The instrument, and the check that it works on THIS surface

**PROVEN TONIGHT, both halves:**
* **`scratchpad/idle_split_s31.py`'s `walk()` + bucket classifier RUNS on a LOCAL
  kept replay** and returns 0 anomalies, bucket D = 0, placement `(0,0)`, all
  cooldown writes `= 1` (§0.2). ⇒ **the bucket-A metric is executable on the local
  fixture.**
* **It is NOT a constant column on this fixture.** Across 8 throw-away local games
  (v140 vs itself, one seed each, `--tle 10`, replays written to `/tmp`, one per
  map) bucket A at `[40,60]` spans **0.00% (antler, drumlin, midgard) to 33.33%
  (valkyrie)**, and at `[T−20,T]` spans **16.67% (ragnarok) to 75.86% (antler)`.
  **The classifier returns both a zero and a large value on the same fixture.**

⛔ **TWO ADAPTATIONS ARE REQUIRED AND NEITHER IS WRITTEN YET (OB17 clause 2 — the
runner must emit what the prereg registers).** The script as it stands (a) keys
our seat off `corpus/meta_join.tsv` `teamAId`/`teamBId`, which **does not exist for
local games**, and (b) walks `replay_archive/`. **The local batch must key the seat
off the shard tape's own `seat` column (`ORD` A ⇒ treatment is team 0, `ORD` B ⇒
team 1) and walk the batch directory.** **The builder confirms this adaptation
exists and runs BEFORE the batch is read; a seat-keying error silently swaps the
arms and reads as a clean result.**

### 8.2 ⚖ RATIFY — THE FOUR GATES

**Batch: both arms, 15-map pool, both seat orders, kept replays, `--tle 10`,
seedbase 353000 (disjoint from the shard's 352000–352674). Target ~120 games/arm.**

| gate | control (measured / expected) | required of the treatment | why this number |
|---|---|---|---|
| **G1 — DELIVERY.** Bucket A share at `[40,60]` and at `[T−20,T]`, per arm, pooled over the batch | the shipped rates; archive anchors 17.77% and 29.01% | **≤ 50% of the control's rate at BOTH windows** | Magnus's target is *"as close to 0% as possible"* and bucket D = 0 proves 0% is reachable, not asymptotic. **A halving is the weakest reading that is still delivery.** ⚠ A residual is EXPECTED and is not failure: `can_move` can be False in all four cardinals, and `BODYAWARE` measured that 21.8% of nav rounds already propose a refused first step |
| **G2 — NO VERB THEFT (the "terminal" check).** Per-game counts of BUILD + ATTACK + HEAL actions, per arm | the shipped counts | **must not fall by more than 5%** | **A terminal fallback cannot cost a paid verb.** A move and an action are mutually exclusive within a round, so **if paid verbs fall, the fallback is NOT terminal and the arm is not the arm this document describes.** This is the clause that can surprise |
| **G3 — ACCOUNTING.** `anomalies` (verb emitted while cooldown > 0) and bucket D, both arms | **0** and **0.00%** | **0** and **0.00%** | an instrument that stops balancing is not measuring; and a non-zero bucket D on the local surface would falsify the cooldown premise the whole design rests on |
| **G4 — CPU PROXY.** `_bfs_direction` node-expansions per builder-turn, both arms | the shipped count | **≤ 1.5× control** | the only CPU signal a local fixture can produce (§3.4). **Above 1.5× the arm is blocked from SHIP on a chassis with 3.5% alarm headroom WHATEVER the game-share column reads**, and that is a finding, not a footnote |

**A failure of G1 or G2 means the arm was not delivered as specified. The shard is
then NOT SCORED**, and the reading banked is *"bodyblock as written does not change
the behaviour it was designed to change"* — a real finding about the design, not
about the currency.

### 8.3 ⚖ RATIFY — THE #54 LOCK DETECTOR: MISSING, PROTOTYPED TONIGHT, AND BLOCKING

**`scratchpad/nav_limit_cycle_census.py` IS NOT ON DISK** (§0.1). This agent
rebuilt a **STRICT** detector from `QUEUE.md` #54's own definition — *a two-tile
oscillation with dwell exactly 1, i.e. `p[i] == p[i−2] != p[i−1]`, over a run of
≥ 50 rounds* — on top of the same `walk()`, and ran it over the 8 local games:

```
antler 0.00%  drumlin 0.00%  midgard 0.00%   glacierkeep 5.84%
valkyrie 18.55%  icefloe 17.93%  ragnarok 29.03%  royale 37.52%
(locked builder-rounds / all our builder-rounds; locked bots 0/13, 0/7, 0/13,
 1/6, 2/6, 1/19, 3/6, 4/6)
```

**⇒ the detector is BUILDABLE, it runs on the local surface, and it returns BOTH
verdicts (three exact zeros and a 37.52%) — it is not a constant column.**

⛔ **AND IT IS NOT YET AN INSTRUMENT, WHICH IS THE POINT OF SAYING SO.** It has
**not** been driven against #54's own controls: the **positive control** (game
`483b5bcd` g1, midgard, rc8.4 — all 11 builders locked, including six named ids)
and the **negative control** (1/6). **A detector that has never reproduced a known
answer has not been seen to check.**
⇒ **BLOCKING PRE-FIRE CONDITION: the `F-LOCK` falsifier (§10) may not be READ until
the detector reproduces both of those controls.** If it cannot be validated, `F-LOCK`
reads **UNRESOLVED**, and per §10's pre-committed default **that alone blocks
promotion** — bucket A cannot carry the arm on its own.

⛔ **BASE-RATE RULE, from #54's own annotation and it is load-bearing:** the
census's 11.58% is **REAL-OPPONENT, v125, PLATFORM**; this fixture is **SELF-PLAY,
v140, LOCAL**, and self-play **under-doses** lock exposure because lock exposure is
partly opponent-induced. ⇒ **`F-LOCK` is a WITHIN-FIXTURE treatment-vs-control
comparison and may NEVER be scored against the 11.58% platform figure.**

### 8.4 ⚖ RATIFY — pre-declared directions for the batch, so it is falsifiable rather than confirmatory

* **`stations`/`destinations offered` > 0 in a majority of games.** If the scorer
  can never name a legal enemy-half destination, the mechanism is absent and the
  screen is pointless.
* **The control's bodyblock-move counter is STRUCTURALLY 0.** A non-zero control
  reading means the instrument is wired wrong and **no number from that batch may
  be read.**
* **Recent-tile violations = 0** (§3.3). Non-zero ⇒ implementation bug ⇒ the batch
  is void.
* **Total builder-rounds IDENTICAL between arms to within ±2%.** The arm is a
  FALLBACK, not a roster change; a large divergence means it changed something
  other than what this document describes.

### 8.5 THE H2 WALK-BACK METRIC — registered, and honestly bounded

**Metric, both arms:** *evictions of OUR builders* (a position discontinuity of
> 1 tile for one of our builders inside one round — readable off the same `walk()`
position stream) **per game**, and **walk-back rounds lost** = rounds until that
builder is again within d² ≤ 2 of its pre-throw tile, right-censored at game end.

**⛔ AND THE LOCAL FIXTURE CANNOT PRICE THIS FOR THE FIELD, STATED BEFORE IT IS
READ.** The throw population depends on the OPPONENT's launcher policy, and here
the opponent is our own v140 with `LAUNCHER_MIN_RND = 160` (`doctrine.py:1536`) and
`LAUNCHER_RESERVE = 80` (`doctrine.py:965`) — a late, bank-gated launcher. The
ladder population is different and larger: **#59's archive cut counts 8,274 throws
of our builders at `ourver ≥ 125`, 60.1% of them after r150, median r209.**
⇒ **the local column is DESCRIPTIVE and bounds nothing about the field. The
priced-trade question — "is a bodyblock beside their core worth being thrown
for?" — is OWED TO A LIVE LEG and is not answered here.**

---

## 9. THE KILL-ROUND RIDER (`DEFENCE_ADMISSION_BAR`, scored as an EXCLUSION)

**This plank carries the bar, and the classification is stated honestly rather than
assumed.** Destinations (a), (c), (d) are **denial/economic**; (b) is **spawn
denial**, which is offensive. **The bar binds anyway, for a real mechanism:** the
idle bodies this plank redirects are, in the `[T−20,T]` window, standing where
**93.69% of active HOME builder-rounds in a LOSS are HEALS**
(`idle_split_out.txt:104`). **Walking them into the enemy half trades a
heal-in-reserve for an annoyance** — and `PROGRAMME.md`'s
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` is the bar that catches the
reverse trade. `R1000_IS_DEFEAT` is unconditional.

**⚖ RATIFY — THE RIDER, in exclusion form:** the arm passes iff the **95% bootstrap
CI (10,000 resamples) on Δ median kill round (treatment − control), paired by
seed, EXCLUDES a +10-round regression.** +10 ≈ **+5.7%** of our 174-round median
kill (us-only, `CLAUDE.md`).

* **A/A noise floor:** `NULL125`, byte-identical arms, read **T 211.5 vs C 208.5
  rounds** — a +3.0-round treatment-slot offset with nothing changed. The +10
  threshold is >3× that floor.
* **⛔ RESTATED AS AN EXCLUSION BEFORE ANY DEFF IS APPLIED**, per `CLAUDE.md`'s
  direction clause. *"Bodyblock did not slow the kill"* is a **fail-to-exclude**
  claim, and widening an interval makes that class of claim EASIER — DEFF applied
  to the unrestated form would launder a weak null into a confident one. **The bar
  above is already the exclusion form.** Applicable DEFF is 0.98 (§4); no inflation
  is applied — same fixture, same two dead clusters.
* **UNRESOLVED ⇒ RESTRICTION:** if the CI cannot exclude +10, the rider does **not**
  pass and a clearing share does **not** promote the arm on its own.
* **⛔ THE CONDITIONING TRAP, named before the read.** `tools/overnight_read.py`
  prints *median kill round GIVEN a kill*. **A change in WHICH games end in a kill
  moves that median without anything getting faster or slower.** ⇒ **the rider is
  reported as a PAIR — P(core-kill win) AND median-kill-round-given-a-kill, both
  arms, with both kill counts — or it is not reported.**
* **Companion column (descriptive):** share of rows with `cond == tiebreak`, per
  arm. Predicted **DOWN or FLAT**. Reference density on the same control tree:
  `GUNAXABL` read 130 / 2,242 = **5.8% tiebreak**.

---

## 10. ⭐ THE #54 LOCK RATE IS A FALSIFIER, NOT A COMPANION COLUMN

**The row's own sharpening, adopted verbatim in force:** *"If lock rate RISES while
bucket A falls, the plank is REFUTED regardless of what bucket A does."*

**Why it is not merely a Goodhart guard — it has a named causal pathway.** A bot
oscillating in a two-tile nav lock **emits a MOVE**, so it classifies as ACTIVE and
is **invisible to bucket A**. And the pathway is specific: `_nav`
(`eco.py:898-910`) counts `desired.opposite()` as a successful move, so a backstep
never increments `self.stuck`, and the only exits (`p == self.tgt`, `stuck >= 5` at
`eco.py:1226`) cannot fire inside a loop. **This plank hands that defect a new,
permanent, possibly-unreachable target.** #54's census sizes the standing exposure:
**11.58% of ALL v125 builder-rounds in permanent locks, 39.8% of locked bots never
acted in their lives, 47.6% of games with ≥1 locked builder.**

### ⚖ RATIFY — `F-LOCK`, with its own threshold and its own UNRESOLVED default

**`F-LOCK` — THE PLANK IS REFUTED IF BOTH HOLD:**
1. the point estimate of Δ(locked-builder-round share, treatment − control) is
   **≥ +1.0pp of builder-rounds**, AND
2. the 95% paired CI on that difference **excludes zero from above**.

**Where +1.0pp comes from, stated so it can be argued with rather than defended
later:** #54's own arm-1 dose moved the self-play lock rate **5.37% → 1.55%**, a
**3.8pp** move that this fixture demonstrably resolves. **+1.0pp is roughly a
quarter of a demonstrated real move on this exact fixture** — small enough to catch
a material regression, large enough not to fire on instrument noise. **It is a
judgment line, not a derived constant, and it is on the ⚖ RATIFY list for exactly
that reason.**

**⛔ AND THE PASS SIDE IS RESTATED AS AN EXCLUSION, per `CLAUDE.md`'s direction
clause — this is the clause most exposed to DEFF laundering on this page.** *"Lock
rate did not rise"* is a fail-to-exclude claim and may **not** be banked in that
form. **To PASS the lock gate, the 95% CI must EXCLUDE a +1.0pp rise.**
**UNRESOLVED ⇒ RESTRICTION: a CI that can neither exclude +1.0pp nor establish it
reads UNRESOLVED, and an UNRESOLVED `F-LOCK` BLOCKS PROMOTION** — bucket A may not
carry the arm alone. *(This is deliberately the harder reading: the alternative
lets a plank whose whole hazard is invisible-to-bucket-A be promoted on
bucket A.)*

**Reported alongside, descriptive:** ΔL / ΔA — the share of the "recovered" idle
rounds that turned into oscillation.

---

## 11. COUPLING CLASS, INTERACTIONS, AND WHAT THIS SCREEN MAY CONCLUDE

**COUPLING CLASS: SELF-KNOWLEDGE / PARTIALLY FIELD-EXPRESSED.** The idle handler is
ours and its trigger is our own tree's behaviour, so the local fixture is
fixture-honest about **bucket A, G2, G4 and `F-LOCK`**. ⇒ **screen-trustworthy for
those**, which is why a local shard is the right first instrument and no live
window is spent here.
**⛔ It is NOT field-honest about the VALUE of the denial**, because the thing being
denied is a v140 opponent doing v140 things: our own tree's gunner density is
**1.26 gunners/game against Leviathan 13.86 / Erebus 8.35 / Lunds Stallions 10.56**
(`scratchpad/corefill_work.txt:619-622`), so **destination (a) — blanking an enemy
gunner's line — is under-expressed here by roughly 7–11×.** A local inside-band
result bounds the LOCAL value of this plank and **says nothing about its ladder
value.**

### Interaction with the live legs (required declaration)

At draft time `scratchpad/corefill.log` reads `hold: running=1/1 … unstarted=1`
(2026-08-15T07:47:28Z) — **one worker, one shard already queued.** Shards on the
worklist against the same control tree and the same 15-map pool:

* **`BODYAWR`** (`bots/_v242bodyaware`, seedbase 336000, n=10800) — diff is
  `eco.py:809-896`, `_bfs_direction`'s blocked set. ⛔ **THIS IS THE ONE REAL
  DESIGN ADJACENCY ON THE BOARD AND IT RUNS ONE WAY:** `BODYAWARE` teaches the BFS
  that **bodies block**, which is exactly the world model `BODYBLOCK` deliberately
  perturbs by parking bodies. **A future COMBO of the two must be attributed
  against its best single ingredient, not only against the control.** Neither
  shard's own contrast is confounded (each is one arm against the same frozen
  control on its own seeds), and **no combo claim may be drawn from the two tapes
  read together.**
* **`GUNAXABL`** (`bots/_v240gunaxabl`, seedbase 312000) and **`SENTTHR`**
  (`bots/_v241sentthreat`, seedbase 314000) — raid-layer diffs
  (`doctrine.py:1533`, `raid.py:753-776`), no shared line with `main.py:445-451`.
* **`NULL5400`** (`bots/_v146null` vs `bots/_v146gunaxis`, seedbase 344000) — the
  commissioned host-term measurement; **its result changes §4's cross-host rider,
  not this shard's bar.**
* **`DEST14A`** (`bots/_v228dest14a`, seedbase 282000) — **#14 arm A, the row this
  one absorbs.** Different arm (destination without a free terminal verb).
  **Reportable as a direction prior; NOT poolable and not a comparator in any bar
  here.**

⇒ **NO STATISTICAL CONFOUND WITHIN THIS SCREEN:** separate shards, disjoint seed
bases, each arm measured against the same frozen control. **The one real
interaction is ALLOCATION** — a 10,800-game leg against a one-worker board is the
scheduling objection in §6.3, and it is a scheduling decision for the builder, not
a design one.

### Fixture and shard line

`tools/corefill.sh` → `tools/overnight.sh`, full 15-map post-patch pool
(`overnight.sh:68`), `--tle 10` wall-clock enforced (`:135-136`), `--replay
/dev/null`, **both seat orders per seed** (`:125-136`). Worklist row **for the
BUILDER to append — this agent did not touch `scratchpad/corefill_work.txt`:**

```
BBLOCK70    bots/_v262bodyblock    bots/_v223sealrepair   10800 352000
```

**BASENAME-COLLISION CHECK, BOTH DIRECTIONS** (`overnight.sh:78-80` refuses on
`$B == *$C*` **or** `$C == *$B*`, because scoring is a SUBSTRING match on the
`Winner:` line and a one-way check reads ~100% for the treatment):
* `_v262bodyblock` contains `_v223sealrepair`? **NO.** Reverse? **NO.**
* `ls bots/ | grep -iE "bodyblock|_v262"` → **empty**, so no existing tree can
  collide with the new basename.
* Shard-key collision, both directions, against every key in
  `scratchpad/corefill_work.txt`: no existing key contains `BBLOCK70` and
  `BBLOCK70` contains none of them. ⚠ **READ HYGIENE: the key is `BBLOCK70`
  exactly.** A `grep BLOCK` pools `GUNBLOCK` and `SALTNOBLOCK`; a `grep BODY`
  pools `BODYAWR`. **Any read that cannot show it matched the exact key is not a
  read of this shard.**

**SEED BASE 352000, span 352000–352674.** `overnight.sh:121` advances the seed
every 16 games, so 10,800 games consume 675 seeds. **Highest live base in the
worklist is 344000 (`NULL5400`, 5,400 games ⇒ 344000–344337); `BODYAWR` holds
336000–336674; the `c63` probe burned 330000–335999.** **No overlap in either
direction.** *(The §8 batch takes 353000; the D26 replication takes 354000.)*

### NOT LICENSED by this screen

* **No ship implication.** `SHIP_SIT` governs; v140 is sitting. A KEEP buys a D26
  replication, the delivery gate and the CPU release gate — not an activation.
* **No field claim about denial value** (§11 opening) — that needs a live leg.
* **No claim about the H2 trade** (§8.5) — the local launcher population is our
  own late, bank-gated one.
* **No combo claim** with `BODYAWARE`, `DEST14A`, `SENTTHREAT` or any other arm.
* **No claim about WHICH destination works.** This screen tests the fallback as a
  bundle. **If (a)–(d) are all enabled, a null does not tell you which destination
  failed** — a per-destination sweep is a follow-up row, admissible only if this
  screen or the §8 batch shows the mechanism fires at all. ⚖ **The builder may
  instead enable exactly ONE destination for this screen, which buys attribution
  and costs dose. That trade is on the RATIFY list.**
* **No revival of `#14` arm B (RECALL).** #70 absorbs arm A only; arm B keeps its
  own `kill_round_non_regression` bar and is untouched here.

---

## FALSIFIER

**The hypothesis (§6.1) is falsified by any of:**

1. **A final ≤ 49.07% (≤ 5,299 of 10,800)** — bodyblocking is measurably worse than
   the shipped idle behaviour. The road closes for the FALLBACK form (§6.5).
2. **`F-LOCK` fires (§10)** — the treatment's locked-builder-round share is ≥ +1.0pp
   above the control's with the CI excluding zero. **The plank is REFUTED
   REGARDLESS OF BUCKET A.** *(And an UNRESOLVED `F-LOCK` blocks promotion; it does
   not refute.)*
3. **The delivery gate G1 fails** — bucket A does not fall to ≤50% of control at
   both windows. The arm did not change the behaviour it was designed to change;
   the shard is **not scored**; the finding is about the design.
4. **G2 fails** — paid verbs (build+attack+heal) fall by >5%. **The fallback is not
   terminal**, so it is not the arm this document registers, and no share reading
   may be read either way.
5. **The kill-round rider fails to exclude +10 rounds (§9)** — the arm buys
   annoyance at the kill's expense and is off-programme whatever it does to share.
6. **A futility drop at any gate** (§6.4) — the arm is not worth more cores; no
   claim is made at that resolution.
7. **A final inside the band (5,300–5,608)** — not supported at ±0.93pp; the
   shipped behaviour stays by the UNRESOLVED default. **This is the modal outcome
   (§6.2) and it is pre-typed as a DROP, not as a null to be argued with.**
8. **Instrument falsifiers, any of which voids the batch:** a non-zero bodyblock
   counter in the control · non-zero recent-tile violations · bucket D ≠ 0.00% or
   `anomalies` ≠ 0 in either arm · total builder-rounds differing by >2% between
   arms · the §8.3 lock detector failing to reproduce #54's positive (11/11) and
   negative (1/6) controls.

**The PRIMARY SEGMENT prediction is falsified** if the treatment's share on the
10 ≤676-area maps is **≤** its share on the 5 900-area maps. *(A reversal — the
plank helping most where approaches are longest — would mean the deliverable is
something other than denial occupancy, and per Ob. 15c it buys its own screen with
its own n; it does not rescue a pooled fail on these rows.)*
**Segment resolution:** 10/15 of 10,800 = **7,200 games, half-width ±1.14pp**;
off-segment 3,600 games, **±1.62pp**.

---

## 12. OBLIGATIONS REGISTER (`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`)

* **Ob. 1–6, 9–11:** Ouroboros/CAD-leg-specific or platform-mechanism-leg specific;
  they do not instantiate on a local single-chassis screen. **Stated rather than
  skipped.** *(Ob. 11's spirit — verify the treatment the EXPERIMENT requires, not
  the one you CODED — is instantiated as G2 in §8.2: the experiment requires
  "terminal", and G2 is the check on THAT, not on the flag.)*
* **Ob. 7 (PRE-STATE / outcome form):** **satisfied** — the outcome is **game share
  IN OUR FAVOUR** on this shard, not a win-condition mix; the predicted-change set
  is verified not pre-satisfied, grepped at the primary (§2 `PRE-STATE`).
* **Ob. 8 (denominator rule):** **satisfied** — single control, single fixture,
  single shard; the denominator is 10,800 rows from one worklist row, pooled with
  nothing, and explicitly not with `DEST14A` or `BODYAWR` (§11).
* **Ob. 12 (gate carries its resolution statement + pre-committed unresolved
  default):** **satisfied in §6.4**, including the arithmetic of what the default
  costs — which is more than the obligation requires and is on the RATIFY list.
* **Ob. 13 (`file:line` + intersection):** **satisfied as a DECLARATION in §5, NOT
  as a computation** — the tree does not exist, so the tool renders CANNOT-COMPUTE
  (its own legitimate case). **The builder must re-run `--fire` after `git add -N`.**
* **Ob. 14 (opponent version stability):** **N/A by shape** — the control is a
  byte-frozen local tree, not a platform cell. No `CELLS:` line exists.
* **Ob. 15a/b/c (map dependence):** **satisfied in §2** — one primary segment, a
  signed direction, a recomputable value ceiling, an explicit descriptive-only
  list, the proxy-dilution declaration, and segment resolution arithmetic.
* **Ob. 16 (MDE inside the bar):** **satisfied in §2 / §6.3** in the PREFERRED form
  `BAR = null + MDE + half_width`, with the standard-corefill-band corollary
  explicitly disclaimed so this bar is not later quoted as a point rule.
* **Ob. 17 (the registered METHOD must be executable by the tool that will execute
  it):** **PARTIALLY SATISFIED — and the gaps are named, not papered over.**
  1. **NAME THE EXECUTING TOOL** — ✅ `tools/corefill.sh` → `tools/overnight.sh`
     for the shard; `scratchpad/idle_split_s31.py`'s `walk()` + classifier, plus a
     rebuilt lock detector, for the mechanism batch.
  2. **CONFIRM THE PATH EXISTS IN THAT TOOL** — ⛔ **TWO FAILURES FOUND AND BOTH
     ARE BLOCKING:** (i) the shard runner uses `--replay /dev/null`, so the shard
     **cannot** carry the mechanism metric — hence the separate batch in §8;
     (ii) `scratchpad/nav_limit_cycle_census.py` **does not exist**, so the
     mandated `#54` falsifier had no executing tool at all — prototyped tonight
     (§8.3) and gated on validation. ✅ **The one that CAN be confirmed was
     confirmed by running it**: the bucket classifier does run on a local replay,
     which was not known before tonight.
  3. **CONSEQUENCE OF SILENT NON-EXECUTION** — ⛔ **the quiet case is the one that
     bites here.** A seat-keying error in the adapted instrument (§8.1) **silently
     swaps the arms** and produces a clean, wrong result; a missing lock detector
     produces **no alarm at all**, only a missing column that a read-out can round
     past. ⇒ both are registered as **BLOCKING pre-fire conditions**, not warnings.
  *(OB17's rider applied: the clause that could still surprise was (2), and it was
  run first. It returned two answers nobody had.)*
* **⛔ `BOUNDARY` in accepts — NOT SATISFIED, STRUCTURALLY.**
  `tools/prereg_check.py`'s `BOUNDARY_UNITS` demands the boundary in both accepts
  and games with the platform identity `games = 5 × accepts`. **A local shard has
  no accepts:** one row is one game, and there is no 5-game match wrapper (which is
  also why the MATCH cluster dies in §4). The boundary is declared in the only two
  units it has — **10,800 rows = 10,800 games**. The tool models this exemption
  explicitly (`prereg_check.py:616-634`); recorded here rather than passed over.

---

## 13. ⚖ THE RATIFY LIST — the BUILDER types these, not this agent

1. **Whether to fire at all**, and at **which n** — 10,800 (registered, expresses
   the +1.00pp MDE) vs 5,400 (bar 52.32, MDE re-registered at +1.39pp) — **against a
   one-worker board** (§6.3, §11).
2. **THE ATTACHMENT DESIGN** — (A) post-dispatch cooldown probe / (B) explicit flag
   / (C) wrapper. **(A) is recommended and the reason is measured** (§3.1).
3. **WHICH DESTINATIONS (a)–(d) ARE ENABLED**, and whether the screen runs the
   bundle (dose) or exactly one (attribution) (§3.2, §11 NOT-LICENSED).
4. **Whether the destination scorer carries a launcher-envelope (`d² ≤ 2`) term**
   — the #59 fix (§3.2 H2).
5. **HYPOTHESIS** (§6.1) and **EXPECTED DIRECTION** (§6.2).
6. **THE MDE (+1.00pp) and therefore the BAR (51.93)** (§6.3).
7. **THE GATE DEFAULT** — point rule (registered) vs the stricter
   UNRESOLVED-⇒-DROP form `BODYAWARE` used; **the power table is in §6.4** (§6.4).
8. **DECISION RULE** branch labels and the single KEEP-vs-DROP sentence (§6.5).
9. **THE FOUR PRE-FIRE GATES G1–G4 and their thresholds** (50% of control, 5%,
   0/0.00%, 1.5×) (§8.2).
10. **`F-LOCK`'s +1.0pp threshold and its UNRESOLVED-blocks-promotion default**
    (§10) — a judgment line.
11. **THE KILL-ROUND RIDER** at +10 rounds, in exclusion form (§9).
12. **SEGMENT** — the 10 ≤676-area maps, positive on-segment (§2), **which is the
    OPPOSITE of the naive long-walk reading** (§0.4).
13. **FALSIFIER** (all eight clauses plus the segment clause).
14. **⛔ THE FLAG-OFF NULL** — `bots/_v263bbnull` vs `_v223sealrepair`, ≥1,000
    games at seedbase 355000, pass inside 50 ± 3.07pp. **Without it, a 641-line
    diff is attributed to a behaviour** (§0.5 (1)).
15. **⛔ G1 RESTATED** against the `LOKI_BB_IDLE_RNDS = 6` addressable population
    rather than against total bucket A, with total bucket A reported unbarred
    beside it (§0.5 (3)).
16. **⛔ G2 RESTATED TWO-SIDED** — build+heal within ±5%, ATTACK reported
    separately and unbarred, because class 0's paid peck lands in the attack
    column by construction (§0.5 (2)).
17. **Whether class 0 (the 2 Ti, 20-Ti-floor terminal PECK) belongs in this arm at
    all**, given that the brief's motivating arithmetic is an argument for a FREE
    terminal and the peck is switched off at the LOSS-side q1 of 12 Ti (§0.5 (2)).
18. **Re-declaring `GATING CONSTANTS`** to include the ARM's own gates
    (`LOKI_BB_PECK_TI_FLOOR=20`, `LOKI_BB_IDLE_RNDS=6`) and re-running
    `prereg_check --fire` (§5.1).

---

## §N — TWO-CLOCK LOCK  ⬜ UNSIGNED — the BUILDER signs this

```
CLOCK 1  prereg lock ............ git author time of the commit adding this file
                                  (`git log -1 --format=%aI -- docs/prereg/SCREEN-bodyblock-2026-08-15.md`)
CLOCK 2  leg creation ........... the `# FIXTURE … start=` stamp written by
                                  tools/overnight.sh:96-100 into
                                  scratchpad/overnight/BBLOCK70.tsv BEFORE the
                                  first game (a START, not a first-completed-row)

ASSERTION ....................... CLOCK 1  <  CLOCK 2, i.e. PREDATES-LEG-CREATION
GAP ............................. ____________
SIGNED .......................... ____________  (builder lane)
DATE ............................ ____________  (`date -u`, same shell call)

PRE-FIRE CONDITIONS, all BLOCKING, all unchecked at draft:
  ⬜ bots/_v262bodyblock FROZEN (it was still being written at 08:04:34Z, §0.5);
     `diff -rq` re-run and the four-file, 641-line diffstat re-stated at freeze
  ⬜ `git add -N bots/_v262bodyblock` && `tools/prereg_check.py --fire` PASSES
     (clears the live FAIL OB13_UNTRACKED_ARM; OB13 intersection COMPUTED;
      OB17 METRIC WINDOW escalated to FAIL-on-absent)
  ⬜ GATING CONSTANTS re-declared to include LOKI_BB_PECK_TI_FLOOR=20 and
     LOKI_BB_IDLE_RNDS=6 (arm-side gates the checker cannot discover)
  ⬜ FLAG-OFF NULL: bots/_v263bbnull vs bots/_v223sealrepair, >=1000 games,
     seedbase 355000, share inside 50 +- 3.07pp
  ⬜ §3.1 attachment design (A/B/C) recorded, since §5's intersection depends on it
  ⬜ §8 kept-replay batch run; G1, G2, G3, G4 all PASS
  ⬜ §8.3 lock detector reproduces #54's positive (11/11) and negative (1/6) controls
  ⬜ §8.1 seat-keying adaptation confirmed against the shard tape's `seat` column
  ⬜ BBLOCK70 row appended to scratchpad/corefill_work.txt at seedbase 352000
```

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read whole, all 12 addenda, obligations 1–17 enumerated) · `CLAUDE.md` (repo root, read whole) · `QUEUE.md` (rows **#70** including its 2026-08-15T07:5xZ AMENDED hazard block, **#54**, **#14**, **#59**, **#45**) · `docs/prereg/SCREEN-sentthreat-2026-08-14.md` (structure) · `docs/prereg/SCREEN-gunaxabl-2026-08-14.md` (structure) · `docs/prereg/SCREEN-bodyaware-2026-08-14.md` (structure, the OB16 bar form, the local-CPU-instrument finding, the NULL125 cell) · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md:165-176` (H1, quoted at the primary) · `docs/coordination.md:56280-56340` (the side lane's #70/#59 collision note, grepped by line, never read whole) · `bots/_v223sealrepair/main.py` (`:155-175`, `:307-451`, `:689`, `:757`, `:797-860`) · `bots/_v223sealrepair/eco.py` (`:35-60`, `:215-245`, `:800-845`, `:898-910`, `:1226`) · `bots/_v223sealrepair/doctrine.py` (round-gate constants, `:437`, `:965`, `:1286`, `:1533`, `:1536`) · `bots/_v223sealrepair/raid.py:809` · `scratchpad/idle_split_s31.py` (source read; `walk()` and `parse_ent()` executed by this agent) · `scratchpad/idle_split_out.txt` (this session's research run, every headline figure re-derived from it) · `tools/overnight.sh` (`:55-145`) · `tools/corefill.sh` · `tools/prereg_check.py` (`:108-180`, `:456-482`, `:611-700`, `:840-950`, `:1151-1230`) · `tools/replay_census.py` · `scratchpad/corefill_work.txt` (seedbase + shard-key collision check) · `scratchpad/corefill.log` (board state) · **plus nine throw-away local games run by this agent** (`bots/_v223sealrepair` vs itself, `--tle 10`, seeds 999777/999778, one per map on midgard ragnarok valkyrie antler drumlin royale glacierkeep icefloe, replays written to `/tmp` only) used to establish that local replays carry the cooldown and verb updates the bucket classifier needs, and to drive a prototype #54 lock detector to both verdicts. **No file under `bots/`, `tools/`, `docs/` (other than this one), or `scratchpad/` was created or modified by this agent, and nothing was committed.**

## Target-value line

**TARGET BAND: N/A** — local screen, zero live rated exposure, no submit, no
activation, no unrated challenge ⇒ `tools/target_value.py`'s reachable-band gate
does not bind (see §2). **The rated-value question is OWED by the live leg that
would follow a KEEP, and it must be run through the gate at that point.**
