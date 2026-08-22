# DRAFT PREREG — `CRASHREP-BC`: does the `5ee3afec_game_2` crash cascade RECUR under a version-pinned, same-map re-fire? — an unrated MECHANISM/REPRODUCIBILITY leg vs **Bean counters, PINNED to their v68**

## ⛔ DRAFT — UNRATIFIED. NOTHING HERE IS LOCKED.

* **Drafted by a FRESH opus agent with NO inherited session context** beyond the
  files named under `PROVENANCE` (the s40 rule). This agent read no result tape,
  no `HANDOVER.md`, no `coordination.md`, no prior s55 session message.
* **THE BUILDER RATIFIES + LOCKS.** Every judgment line below — hypothesis, bar,
  falsifier, dose, scope of claim — is a **PROPOSAL**. They are written
  decisively because a hedged proposal cannot be ratified, not because they are
  settled.
* **What this agent wrote:** this file, and nothing else. No commit to `bots/`,
  `tools/`, `QUEUE.md`, `HANDOVER.md` or `coordination.md`; no `BARS.tsv` row;
  no challenge; no match; no submit; no activation.
* **⚠ WHAT THIS AGENT DID RUN, disclosed rather than left to boilerplate — and it
  is MORE than the KLADDEDOSE precedent, so it is spelled out.** Read-only
  commands, in this agent's own shell, under the parent's explicit
  "read-only platform commands are permitted":
  * `.venv/bin/python tools/target_value.py "Bean counters"` (the gate; output
    pasted verbatim below).
  * `.venv/bin/python tools/crash_census.py --selftest` — **PASS, run by this
    drafter, not relayed**: positive control `bots/_probe_crash` 20 candidates
    on the crashing side / 0 on the other, negative control 0/0.
  * `.venv/bin/fcode match info <id> --json` on **six** matches and
    `.venv/bin/fcode match list --team "Bean counters" --type unrated --json` —
    read-only per `docs/fcode-cli.md` (`GET /api/matches/{id}`, `GET
    /api/matches`). **These produced the map/seat/version facts in §MAP-AND-SEAT
    and they are the single largest change this draft makes to the commission's
    design.**
  * `date -u`, `git log -1`.
  **No mutating platform call of any kind.**

**PROVENANCE:** `scratchpad/s55_crashrep_commission.md` ·
`docs/research/DECODE-firstcontact-v180-2026-08-22.md` §2, §8 ·
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` ·
`CLAUDE.md` ("WHAT LOKI IS", the TARGET-BAND gate rule, the DEFF cluster
enumeration, the rate-limit and submit-is-shipping blocks) ·
`docs/fcode-cli.md` §`match info` / §`match list` / §`match unrated` (~ll.300-355) ·
`tools/crash_census.py` (module docstring) · `tools/target_value.py` (docstring +
run) · `docs/prereg/PREREG-LEG-KLADDEDOSE-2026-08-21.md` (structure only).

**STATUS: DRAFT, written BEFORE any lock commit, BEFORE any challenge is issued,
and BEFORE any game of this leg exists.** Drafting-shell wall clock
**`2026-08-22T10:25:48Z`** (`date -u`, same shell call); repo HEAD at draft
**`e92af209c`** (2026-08-22 12:24:47 +0200).

**LOCK, TWO CLOCKS — PLATFORM LEG (per the obligations doc's 16:3x addendum;
the `# FIXTURE … start=` local-shard form of the 2026-08-17T07:24:55Z addendum
does NOT apply, this leg produces no shard tape):**
* **CLOCK 1** = the ratified file's **lock commit git author time**.
* **CLOCK 2** = the **first accepted match's platform `createdAt`**, quoted
  verbatim (`fcode match info <id> --json` → `match.createdAt`; the source match
  reads `"createdAt": "2026-08-22T08:24:08.570Z"`, so the field is present and
  the form is executable).
* ⛔ **CLOCK 1 MUST STRICTLY PRECEDE CLOCK 2.** A lock whose author time is at or
  after the first fire is not a pre-registration and the leg is descriptive only.

---

## ⛔ WHAT THIS LEG CAN AND CANNOT BUY — STATED FIRST, BECAUSE IT SETS THE DESIGN

**THIS IS A MECHANISM / REPRODUCIBILITY LEG. IT IS NOT A CURRENCY READ AND NO
SENTENCE IN ITS READOUT MAY BE DENOMINATED IN GAME SHARE.** 25 games at the
unrated within-opponent DEFF of 1.434 carries a ±23.5pp half-width on any share.
`CLAUDE.md`: *a 25-game window is a DOSE AND MECHANISM probe; a currency read
requires pooling windows.*

**AND THE VALUE IS NOT BEAN COUNTERS' SCALP.** The TARGET-BAND gate (below) says
in its own words that no rating is reachable here: **gap +448, outside all 1,022
observed pairings.** The value is the **CLASS**: crash-induction is the standing
`WHAT LOKI IS` road, and a trigger that fells one opponent's builder line tends to
fell every opponent sharing that code shape. **A reproducible cascade is a weapon
we can then bisect and aim at the reachable band; an irreproducible one is a road
closed for the price of one window.** Both outcomes are worth the window; neither
is worth a rating claim.

**⛔ THE CLASS QUESTION IS ALREADY ANSWERED — DO NOT RE-ASK IT.** Crash-induction
was put to the organisers and **APPROVED** (`CLAUDE.md`, "WHAT LOKI IS", §0 and
the CLASS RULING). This leg introduces **no new mechanism** — it does not even
introduce a new *trigger*, because it changes nothing about our play; it re-fires
an existing fixture. Standing permission covers it in full.

**⛔ `R1000_IS_DEFEAT` AND THE r300 GUARD DO NOT BIND.** `PROGRAMME.md`'s
`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression` prices *planks that could
slow the kill*. **This leg ships no plank.** Our tree is byte-identical to the one
that already played the source match; there is nothing to regress. No kill-round
bar is registered and none may be read into it.

---

## REGISTRATION BLOCK

**STATUS:** DRAFT — before the lock commit, before the first challenge, before any game exists.

**PLANK CLASS:** **none — this leg has no plank.** The "treatment" is a FIXTURE
(a pinned opponent version + a fixed map), not a code change. *(Consequence: the
r300 admission bar does not bind; see above.)*

**SURFACE:** unrated (platform challenge, `fcode match unrated`).

**OUR SIDE:** submission **v180 "Skalman rc619.1"** — already uploaded; the exact
build that played the source match (`teamBVersion: 180` on `5ee3afec`, verified by
this drafter). **It must be ACTIVE at every accept** (§FIRE GATES gate 1).
Restore **v176** by integer afterwards.

**OPPONENT / CELL:** one — **Bean counters**, teamId
`47803c19-e264-4492-bd62-fbdd58cfd7e6`, **PINNED to their v68**.

**PINNED:** YES — `fcode match unrated 47803c19-e264-4492-bd62-fbdd58cfd7e6
--match 5ee3afec-17b1-46a5-ba8d-116a25cceaba`, **every accept, no exceptions.**
*(`PIN TREATMENT LEGS, NEVER PIN CALIBRATION PANELS` — this is a treatment leg,
and the pin IS half the fixture.)*

**MAP:** **`midgard`, fixed** — `--map midgard` ×5 per accept. See §MAP-AND-SEAT;
this is the cascade game's own map and the commission did not know it was
knowable.

**CELL VERSION CHURN (OBLIGATION 14):** **LOW, and measured by this drafter, not
assumed** — every OpenSverige-vs-Bean-counters unrated row on the platform reads
`Bean counters v68`, including the **unpinned** 06:04Z match `a6be5b6e`, i.e. v68
is both the pinned version and their current live one. **The pin is therefore
belt-and-braces rather than load-bearing today — and it is still mandatory,**
because BC may ship between the lock and the fire and a silent version change is
exactly the failure the pin exists to prevent.

**MECHANISM METRIC READS:** `tools/crash_census.py` — the `crash_candidate`
bucket, classification rule in its module docstring (*"NEVER had an `updateHp`
event, AND is a kind that runs code each round → crash_candidate"*), plus the two
corroborating engine-side columns in §MECHANISM METRIC.

**TREATMENT DIFF TOUCHES:** ⛔ **NOTHING — and OBLIGATION 13 IS ANSWERED, NOT
SKIPPED.** OB13 exists to catch a metric that sits downstream of code identical in
both arms. **Here there are no arms and no diff:** the metric reads the
*opponent's* units on the wire, and the quantity that varies between the source
match and this leg is the fixture (a re-draw of the same pinned pairing on the same
map). OB13's guarantee — *the metric is not blind to what the leg varies* — holds
trivially, because the metric reads the OPPONENT and the leg varies the OPPONENT'S
execution. **What replaces OB13 here is OBLIGATION 17, discharged in §FIRE GATES.**

**METRIC WINDOW:** r0–r1000, whole game. The source cascade ran r46–r74.

**BAR (PROPOSED):** **≥ 1 CASCADE GAME in this leg's DISTINCT games**, where

> **CASCADE GAME** ≝ a game in which `crash_census` reports **≥ 3 Bean-counters
> `crash_candidate` removals of kind `builder_bot`**, each removed **≤ 1 round
> after it was built** and **at full HP (40/40)** with **no `updateHp` event ever**,
> **AND** Bean counters built **> 4 builder bots** in that game.

**WHY N = 3 AND WHY THE SECOND CLAUSE — defended, per the commission.**
`crash_census`'s own docstring names the conflation: a lone no-damage removal of a
builder bot is *crash OR `self_destruct()`*, 2-way ambiguous, and the tool cannot
separate them. **One event is inside that ambiguity; three consecutive ones on
successive spawns are not a plausible policy for a bot whose four doctrine builders
are simultaneously alive and working.** The `>4 builders` clause is an
**independent channel on the same event**: BC's `exactly_four_builders` signature
holds **19 of 20** on the live tape (decode §2.2), so a builder count above four is
itself evidence of the spawn-and-vanish loop, measured off entity-creation events
rather than off removals. **A bar that requires two independent signatures cannot be
cleared by a single mis-bucketed removal.**

**BAR SOURCE:** constructed on this page from the cascade's own measured signature
(decode §2.1/§2.2: 10 removals, all age ≤1 at 40/40, 14 builders vs a doctrine of
4). **Not copied from any banked bar.** The threshold 3 is set *below* the observed
10 deliberately — a bar set at the observed value would only detect a cascade of
identical severity, and the question is whether the phenomenon recurs at all.

**OBLIGATION 16 — THE MDE, INSIDE THE BAR'S CONSTRUCTION AND NOT BESIDE IT:**
**the bar is an OCCURRENCE BAR and is a POINT RULE ONLY on the positive side.** It
licenses **no** claim about the cascade's RATE if it fires. The exclusion claim
lives entirely on the falsifier side and is stated with its own MDE there:

    FALSIFIER MDE : we call the STRONG hypothesis a MISS if the true per-game
                    cascade rate in this cell is at or below 18.1%.
                    n for that exclusion: 25 games (n_eff 17.43 at DEFF 1.434)
                    -- Wilson-95 upper bound on 0 successes = 18.06%.
    NOT EXCLUDED  : the WEAK (background) rate of ~4%/game. Excluding 4% from
                    above needs n_eff >= 92.2, i.e. ~132 games / 27 accepts /
                    ~6 windows. THIS LEG DOES NOT BUY THAT AND DOES NOT CLAIM IT.

**BASE RATE — three denominators, kept separate on purpose, all measured:**

| population | cascade games | rate | source |
|---|---|---|---|
| all first-contact games, 3 opponents | 1 of 65 | 1.5% | decode §2.2 (effective 58 after duplicates, §0.3) |
| **Bean counters cell, v180 era** | **1 of 25** | **4.0%** | this drafter, `match list --team "Bean counters"`: 5 unrated matches 08:24–08:41Z |
| **`midgard` games in that cell** | **1 of 2** | — | this drafter (§MAP-AND-SEAT). **n=2. This number sizes NOTHING and is quoted only to show the fixture is not exotic.** |

**POOL ERA:** 2026-08-22T08:24:06Z (v180's first BC match) → this leg's games.
Same rated-map pool, same day, same our-side build.

**CLUSTER UNIT + DEFF — `CLAUDE.md`'s ENUMERATION PROCEDURE, PERFORMED IN WRITING,
ALL FOUR CLUSTERS NAMED:**

| cluster | can this leg's stratum hold >1 member? | verdict |
|---|---|---|
| **MATCH** | **YES** — 5 games share an accept, an opponent version and one time slice | **LIVE** |
| **OPPONENT** | NO — one pinned opponent at one version | **DIES** |
| **MAP** | NO — one map by construction | **DIES** (removed in the exclusion direction: variation is eliminated, not averaged) |
| **CONTENT-DUPLICATE** | ⛔ **YES, AND IT IS THE CENTRAL HAZARD OF THIS DESIGN** | **LIVE — see §DUPLICATE** |

⇒ **DEFF = 1.434** (unrated, within-opponent) applied to the nominal n, **and then
n is further reduced to the DISTINCT-game count** per §DUPLICATE. ⚠ *Caveat
registered before the fire: 1.434 was measured on a map-heterogeneous pool. Fixing
the map can only raise within-match correlation, so 1.434 is a **floor** here; the
duplicate count is the empirical backstop and is what the readout actually uses.*

**ESTIMATOR:** Wilson score interval on the per-game cascade rate, computed on
`n_eff = distinct_games / 1.434`. Declared here so it cannot be chosen after the
data: **no normal approximation, no Agresti-Coull, no exact-binomial substitution
at readout.**

**PLANNED n:** **25 games = 5 accepted unrated matches × 5 games = ONE rate-limit
window** (5 test/unrated matches per **10** minutes — re-corrected s54; **re-derive
from a fresh rejection string in the firing shell, never from this line**).

**BOUNDARY:** 5 **ACCEPTS**, never attempts. `games = 5 × accepts` is the identity
that makes a miscount visible (the CAL-8 incident).

**CUT-SHORT:** below 3 accepts (15 games), or below **10 DISTINCT games**, the leg
is **DESCRIPTIVE ONLY** — counts reported, no bar verdict, no falsifier verdict.

**MAP SEGMENT (OBLIGATION 15):** **`MAP SEGMENT: midgard only — the cascade's own
map, held FIXED rather than varied — EXPECTED DIRECTION: n/a, this is a fixture
constraint and not a subgroup read.`** ⚠ **The direction clause is inapplicable
BECAUSE THE SEGMENT IS THE WHOLE POPULATION** — 15b's hazard (declaring K segments
to get K rescue attempts) cannot arise where K = 1 and the segment is declared as
the sampling frame. **No cross-map claim is registered and no per-map comparison
exists to make.** Mechanism reason for fixing rather than varying: the trigger is
**UNIDENTIFIED** (decode §2.4), so terrain is a live candidate and must be held
constant, not averaged over.

**DOSE:** ⛔ **THERE IS NO BEHAVIOURAL DOSE TO COUNT, AND SAYING SO IS THE HONEST
FORM.** In a plank leg the dose is *how often our new code acted*. Here our code is
unchanged and the trigger is unknown, so **the dose is the FIXTURE INSTANTIATION:
25 games of (v180) × (BC v68) × (midgard).** *Dose delivered* = 25 games that pass
the §PIN DISCIPLINE alarm with our side reading v180 and theirs v68.
**Recorded per game as trigger covariates for the eventual bisect — never as bar
inputs:** (a) the round of our first barrier at d² ≤ 2 of BC's core *(the refuted
candidate, 65/65 base rate — recorded so a positive result can be checked against
it immediately)*, (b) BC's builder-bot build count, (c) BC's core residual HP at
removal, (d) our seat, (e) `mapSeed`.

---

## §MAP-AND-SEAT — ⭐ THE COMMISSION'S PREMISE IS WRONG IN OUR FAVOUR, AND THIS SECTION IS WHY THE LEG IS WORTH FIRING

The commission (item 3) and decode §8 both assume the map is out of our hands:
*"unrated matches draw their own maps"*, *"map identities are not recorded"*.
**Both are false at the platform layer, and this drafter verified all of it.**

**1. THE MAP IS SELECTABLE.** `fcode match unrated` takes `--map` **repeatable, up
to 5** (installed fcode 2.3.6: `commands/match_group.py:58` declares it,
`commands/test.py:18-19` sets `body["mapNames"] = list(maps[:5])`).

**2. THE CASCADE GAME'S MAP IS KNOWN.** `fcode match info
5ee3afec-17b1-46a5-ba8d-116a25cceaba --json` returns per game `mapName`,
`mapSeed`, `turnsPlayed`, `winnerSide`. **Game 2 = `midgard`, `mapSeed`
1399900204, 75 turns, `winnerSide: b` = us.** That matches decode §2's *"30×30, our
seat B, 75 rounds"* on three independent fields. *(Decode §8 is right about the
REPLAY and wrong about the platform record — the identity was one read-only call
away.)*

**3. THE MAP FILE IS THE SAME FILE ACROSS MATCHES; ONLY THE SEED IS REDRAWN.**
`midgard` carries `s3Key
maps/d7be95c06ce141a87e694344d2c80a7fd72ae65517e6cbda2ba8508e894f7d9f.map26` in
BOTH `5ee3afec` (seed 1399900204) and `4bc7ed13` (seed 411946209). ⇒ **`--map
midgard` buys the SAME TERRAIN. It does not buy the same game instance** — the
`mapSeed` is drawn per game and there is no seed selector in the `unrated` POST
body. **Registered as an uncontrolled variable, reported per game.**

**4. SEAT IS NOT SELECTABLE — and there is a suggestive regularity, labelled as
such.** Across all six OpenSverige-vs-BC unrated matches: the **two** fired with a
`--match` pin (`5ee3afec`, `ae8dd8c2`) seated **BC as team A and us as B**; the
**four** fired unpinned seated **us as A**. **n = 6. This is an OBSERVATION, not a
control** — the leg does not depend on it, seat is reported per accept, and a
same-seat sub-count is a diagnostic column, never the bar.

**5. THE MAP CELL, MEASURED.** Of the 25 v180-era BC games, **`midgard` appears
twice**: `5ee3afec/2` (our seat B, 75 turns, **we won — the cascade**) and
`4bc7ed13/2` (our seat A, 80 turns, BC won). **Every other BC game we have ever
won is… none.** The cascade game is our only game off Bean counters in the set.

⇒ **THE DESIGN CONSEQUENCE, AND IT IS THE WHOLE REASON THIS IS A LEG AND NOT A
SHRUG:** the commission imagined ~2 midgard games in a 25-game random-map leg,
which resolves nothing. **A `--map midgard` leg puts all 25 games on the cascade's
own terrain against its own pinned opponent with its own our-side build.** That is
as close to a re-run as this platform sells.

---

## §DUPLICATE — ⛔⛔ THE HAZARD FIXING THE MAP CREATES, REGISTERED BEFORE THE FIRE

**`CLAUDE.md` names CONTENT-DUPLICATE as a live cluster and requires every powered
grid to carry a duplicate control.** This leg maximises the risk on purpose:
decode §0.3 measured **15% byte-identical repeats in the MIRROR (Bean counters)
cell already**, at n=20 with five different maps; **§0.4 measured OUR side as
byte-identical across a matched pair.** Fix the map and pin the opponent and the
only remaining source of variation is `mapSeed` and seat.

⇒ **MANDATORY, AND IT OUTRANKS THE BAR:**

1. **Compute the DISTINCT-GAME COUNT** — group the 25 replays by content hash
   (byte hash of the `.replay26`, with a per-round event-stream digest as the
   tie-breaker for any near-identical pair). **Report `distinct / 25` FIRST, before
   any cascade number.**
2. **ALL bars and intervals are computed on DISTINCT games.** `n_eff =
   distinct / 1.434`.
3. **THE COLLAPSE BRANCH, pre-committed:** if `distinct` ≤ 3, the leg **cannot
   resolve the falsifier** and reads **UNRESOLVED — DETERMINISTIC COLLAPSE**, with
   the informative sentence being *which* branch it collapsed onto (cascade or no
   cascade). **A 0/25 with distinct = 1 excludes nothing whatsoever** and any
   sentence claiming otherwise is a registration breach.
4. ⭐ **AND THE COLLAPSE IS NOT A FAILURE — IT IS THE MOST ACTIONABLE OUTCOME
   AVAILABLE.** 25/25 identical-and-cascading means the trigger is deterministic
   and **bisectable by local arms**, which is the decode's own named next step. The
   readout must say so rather than filing it as a null.

---

## §MECHANISM METRIC — ENGINE-SIDE ONLY, AND HOW EACH QUANTITY IS OBTAINED

**No quantity below is read from our own stdout.** Platform replays carry
`BotOutput` with an EMPTY `stdout` field (30,664 of 30,664, `CLAUDE.md` s28), and
under fcode 2.3.6 stdout does not even survive locally (s54). **All four are read
from entity/HP events on the wire.**

1. **CRASH CANDIDATES (the bar's numerator).** `tools/crash_census.py` per game,
   restricted to Bean counters' entities, kind `builder_bot`, `removeEntity` with
   **no `updateHp` event ever**, age ≤ 1 round, HP 40/40.
2. **BC BUILDER-BOT BUILD COUNT (the corroborating signature).** Entity-creation
   events of kind `builder_bot` on BC's team. Doctrine baseline: exactly 4 (19/20).
3. **BC CORE RESIDUAL HP AT REMOVAL (diagnostic).** The source cascade ended with
   BC's core removed at **284/500** — a core vanishing above ~0 HP is the same
   wire signature applied to the core (crash *or* `resign()`, 3-way ambiguous per
   the census docstring).
4. **TRIGGER COVARIATES** (a)–(e) from the DOSE line.

**INSTRUMENT VALIDATION — DRIVEN TO BOTH VERDICTS, BY THIS DRAFTER, TODAY:**
`crash_census.py --selftest` builds a **positive control** (`bots/_probe_crash`,
which crashes every builder deliberately) and a **negative control** (a
non-crashing bot against itself) and reports **20 candidates on the crashing side,
0 on its opponent, 0/0 on both negative sides — PASS.** The complementary negative
on **this exact surface** is the decode's own 64 of 65 platform games reading
**zero**. ⇒ **the instrument has been seen to fire and seen to stay silent, on both
a synthetic and a live fixture. A constant column would validate nothing; this one
is not constant.**

⚠ **THE CONFLATION IS NOT CLOSED AND THE READOUT MUST SAY SO.** `crash_candidate`
cannot separate a genuine uncaught exception from `self_destruct()` (builder bots)
or `destroy()`/`resign()` (buildings/core). **The bar's two-signature construction
narrows it; it does not eliminate it.** Any verdict sentence says *"crash-signature
removals"*, never *"crashes"*, unless a future engine-side probe closes the gap.

---

## §n-PLAN — WHY 25, AND EXACTLY WHAT 25 RESOLVES

DEFF 1.434 → `n_eff = 17.43` at 25 distinct games. Wilson-95 on the per-game
cascade rate:

```
cascade games  0 of 25  ->  [0.00%, 18.06%]   upper < 50%          FALSIFIER FIRES (strong form)
cascade games  1 of 25  ->  [1.02%, 26.44%]   BAR MET (occurrence)
cascade games  2 of 25  ->  [3.20%, 33.65%]   BAR MET
cascade games  3 of 25  ->  [6.03%, 40.23%]   BAR MET
```

**POWER, STATED HONESTLY IN BOTH DIRECTIONS — this is the number that decides
whether the leg is worth the window:**

```
if the true rate is the 1-of-2 midgard cell (50%)   -> P(at least one hit in 25) = 99.99%
if the true rate is the cell background (5%)        -> P(at least one hit in 25) = 59.1%
```

⇒ **25 games is decisive against the STRONG hypothesis and only a coin-flip against
the WEAK one.** That asymmetry is registered, not discovered later: **a 0/25 refutes
"this fixture reproduces the cascade at a usable rate" and leaves "rare background
event" standing.** Closing the weak form needs ~132 games (~6 windows) and **is not
proposed** — a rare-and-untriggerable crash is not a weapon, and the road worth
buying is the reproducible one.

**GATE RESOLUTION (OBLIGATION 12) — sized, with the branches pre-committed:**

| observed (on DISTINCT games) | verdict | what it licenses |
|---|---|---|
| ≥1 cascade game | **REPRODUCED** | the cascade is not a one-off; **next step is a local bisect of the trigger**, not another platform leg |
| 0 cascade games, distinct ≥ 20 | **NOT REPRODUCED (strong form refuted)** | rate < 18.1% (95%); the deterministic/high-rate road is **CLOSED on live games** |
| 0 cascade games, 10 ≤ distinct < 20 | **UNRESOLVED** | recompute the bound on the actual distinct count and print it; no closure |
| distinct ≤ 3 | **UNRESOLVED — DETERMINISTIC COLLAPSE** | nothing about rate; report which branch it collapsed to |
| ≥1 game with 1–2 candidates and/or ≤4 builders | **SUB-THRESHOLD** | reported, does **not** clear the bar |

⛔ **AN UNRESOLVED GATE DEFAULTS TO THE RESTRICTION, NEVER THE PERMISSION.**
UNRESOLVED means the cascade is **not credited** as reproducible. It does not mean
"promising".

**NO EXTENSION IS PRE-COMMITTED.** A second window would move the exclusion from
18.1% to 9.9% (n=50) — which buys nothing on the decision this leg exists to make.
*(If the builder wants an extension it must be registered at lock, with its own
gate table, or it is a re-roll.)*

---

## §PIN DISCIPLINE — ⛔⛔ THE PIN **IS** THE TREATMENT, SO ITS INSTRUMENT ALARM IS MANDATORY IN THE LOCK

**Any decoded `oppver` other than `68` on any accept in this leg is an INSTRUMENT
ALARM: either the pin did not take, or the decode is wrong. REPORT IT AND DO NOT
READ THAT CELL.**

* The alarm is **per accepted match**, checked at readout against the decoded
  opponent version — **never assumed from the fact that `--match` was typed.**
* **A pinned set whose decoded `oppver` values DIFFER AMONG THEMSELVES is the same
  alarm, and it invalidates the POOLING of those matches, not merely one of them.**
  With a fixed map and a pinned opponent this leg has no other axis to absorb an
  opponent change; a mixed set is not a result, it is a broken fixture.
* **A NULL `oppver` IS NOT A PASS** (the literal string `'None'` stood in 4,375 of
  4,375 rows until the 2026-08-13 backfill; a null reads as "no version change" to
  any cut that trusts it).
* ⭐ **READ IT FROM THE RIGHT ENDPOINT — verified by this drafter, and it is a trap
  that would have produced exactly a null:** `fcode match info <id> --json` returns
  **`teamAVersion: null`** for the opponent (the documented `match info` bug —
  `docs/fcode-cli.md` "Trap: the opponent's submission version is `null` in this
  payload"), while **`fcode match list --team "Bean counters" --type unrated
  --json` returns `teamAVersion: 68` for the same match.** **The readout uses
  `match list`.**
* **OUR SIDE CARRIES THE SAME ALARM:** every accept must decode `OpenSverige`
  version **180**. If v176 (or anything else) appears, our half of the fixture
  changed mid-leg and that cell is unreadable.

---

## §FIRE GATES — CHECKED IN THE SAME SHELL, IN THIS ORDER

1. ⛔ **HOLDER READ, SAME SHELL, LOAD-BEARING FIELD.** `fcode status` must print an
   `Active bot:` line. **Gate on the presence of that line, never on `$?`** — this
   CLI exits 0 while printing `Error: True`. Record the holder (**v176 at draft
   time**, verified by this drafter off `match list --mine`: every unrated row
   after 09:10Z reads `OpenSverige v176`).
2. **ACTIVATE v180 BY INTEGER** — the validated read-then-restore-by-integer
   procedure (relayed: 5 windows, zero rated leak). **⛔ SUBMITTING IS SHIPPING** —
   there is no upload-now-activate-later; the activation window IS the exposure.
   **No CPU/TLE gate is owed:** v180 already ran 25 live platform games at
   08:24–08:41Z (5 matches, `teamBVersion: 180`, all completed, decode §6.2 reads
   our own exception-deaths at effectively zero).
3. **RE-DERIVE THE LADDER PAIRING CADENCE IN THE FIRING SHELL** from fresh
   `createdAt` rows (`fcode match list --mine --type ladder --json`) and fire **just
   AFTER an observed pairing**. ⛔ **Never hardcode the `:12/:32/:52` offset — it has
   shifted at least once inside 18 hours.** Rated-leak budget: **~−8 Elo per leaked
   match**, and a leak is detected at the **PAIRING BOUNDARY** (per-match
   `teamAVersion`/`teamBVersion`), **never by the match counter**, which is blind to
   exactly this failure mode.
4. **OBLIGATION 17 — NAME THE EXECUTING TOOL, CONFIRM IT EMITS EVERY REGISTERED
   ELEMENT, STATE THE CONSEQUENCE OF SILENT NON-EXECUTION.** ⚠ **The clause that can
   still surprise the runner is the third, and it is run first.**
   * **NAMED TOOL: ⟨RATIFY⟩ the builder names it at lock** — a hand-typed
     `.venv/bin/fcode match unrated …` per accept, or a runner. ⛔ **If a runner is
     used it must be grepped for BOTH `--match` AND `--map` before the lock:**
     `tools/unrated_run.sh` historically fired a bare `fcode match unrated "$id"
     --json` with **no pin path at all** (the CAL418 incident, OB17's founding
     case), and `fanout.sh` still **drops a rejected cell after 3 retries** and logs
     `fired 3/5` — under a 10-minute window that drop is systematic and always lands
     on the same cell.
   * **PATH EXISTS (verified by this drafter in the installed CLI, not from
     `--help`):** `commands/match_group.py:57-58` declares `--match → source_match`
     and `--map → maps`; `commands/test.py:13-19` sets `body["sourceMatchId"]` and
     `body["mapNames"] = list(maps[:5])` and posts `/api/matches/unrated`; on accept
     the CLI echoes `Opponent version from match: <id>` and `Maps: …`.
   * **CONSEQUENCE OF SILENT NON-EXECUTION — the one nobody has checked:** ⛔ **it
     is UNKNOWN whether the server honours FIVE REPEATS of the same map name.** The
     client sends `["midgard"]*5` unvalidated; the server may dedupe to one game, or
     fill the rest at random. **Pre-committed branch, decided before any crash data
     is read: the FIRST accept is a PROBE — read its five games' `mapName` off
     `fcode match info --json`. If they are not 5×`midgard`, the leg's map plan is
     re-registered by an ADD-only amendment BEFORE the remaining four accepts, and
     non-midgard games are reported in a separate stratum.** The failure mode this
     closes is quiet: a map plan that silently degrades to random gives 25 games
     that look fine and answer a different question.
5. **RATE LIMIT:** 5 test/unrated matches per **10** minutes, shared across
   `match unrated` and `match test`; **rejected attempts appear to count.** **Wait
   out the window and retry the SAME cell** — never log `fired 3/5` and move on.
   **Re-derive the constant from a fresh rejection string** (`Error: Rate limit
   exceeded: max 5 test/unrated matches per 10 minutes`); it has flip-flopped
   10→20→10.
6. **EXPOSURE IS A FREE LOOK FOR THE FIELD, PRICED NOT PROHIBITED.** Opponents can
   and do challenge our live prototype mid-window (Jacobs ×2, 2026-08-22) and those
   challenges do **not** consume our budget. Expect it; it is not a reason to
   shorten the window.
7. **RESTORE v176 BY INTEGER** and **confirm the restore against the `Active bot:`
   line**, never the exit code.
8. **SIDE-LANE CERTIFICATE** per the s54 template, two clocks, after the fire.

**TARGET BAND — `tools/target_value.py "Bean counters"`, run by this drafter at
`2026-08-22T10:20:45Z`, PASTED VERBATIM:**

```
RATINGS from corpus/league_matches.tsv — newest observation 2026-08-22T09:41 (0.7h old)
our rating 1804   (reachable band us-80..us+125, from 1022 observed pairings)

  opponent                    rating    gap  5-0 pays  0-5 costs  reachable   where that gap sits
  Bean counters                 2252   +448    +29.75      -2.25  ** NO **   ABOVE every one of 1022 observed pairings
                                                                     ^ outside band
                                                                     ^ but PLAYED 5x on the ladder, most recently at gap +55 -- reachable UNTIL RECENTLY, not now

TARGET BAND: gaps +448..+448, a 5-0 pays 29.75..29.75, admissible 0/1  (band AND a 5-0 paying >= 10)
NOTE: the absolute 1650 floor was RE-DENOMINATED to MIN_PAYOUT = 10 rating points on 2026-08-12.
** NO TARGET IS REACHABLE ON THE LADDER. Even a total success here cannot be converted into rating by playing them. **
```

⭐ **AND THE GATE IS A GATE, NOT A VETO — THE JUSTIFICATION IS WRITTEN DOWN BEFORE
THE WORK, WHICH IS THE ENTIRE POINT OF THE RULE.** We are firing at an opponent the
ladder will not pair us with. **We are not buying their scalp; we are buying whether
an approved-class weapon is reproducible.** The s28 case this gate was built from is
the opposite error — a leg aimed *down* at unreachable teams to measure a plank whose
value was assumed. Here the unreachability is the reason the leg is cheap
(nothing rated is at stake in the matchup itself) and the class transfer is the
payoff. **If the builder disagrees, the honest move is to stand the leg down, not to
re-argue the number.**

---

## PREDICTIONS

**P1 (PRIMARY — the bar).** **≥ 1 CASCADE GAME** (≥3 full-HP age-≤1 BC builder
removals with no damage event, plus >4 BC builders) among this leg's distinct
games.

**P2 (PRE-STATE, OBLIGATION 7 — and the coordinator's amendment (2) is what this
line answers).** ⭐ **THE OUTCOME IS NOT ALREADY IN THE TARGET STATE AND THE
HYPOTHESIS IS WORDED AS A QUESTION.** This prereg does **not** assume the cascade
is reproducible; it asks. The predicted-change set is *this leg's own games, which
do not exist at lock* — outcome variable identically 0 by construction — and the
comparable measured cell (BC v180 era, all maps) sits at **1 of 25**, far from
saturation. **Both outcomes are priced and both are a legitimate iteration:** a hit
opens a bisect; **a 0/25 closes the strong road for one window's cost and is banked
as a null, not as a failure.**

**P3 (DIAGNOSTIC, never the bar).** BC's core-removal residual HP and our
win/loss/`turnsPlayed` per game. **No game-share verdict, no Elo claim, and these
may not appear in any verdict sentence.**

**P4 (DESCRIPTIVE).** Distinct-game count, seat per accept, `mapSeed` per game,
and the trigger covariates (a)–(e). These feed the bisect; they resolve nothing.

---

## FALSIFIER

**⛔ THE FALSIFIER, STATED SO IT CAN FIRE — AND IT IS REPRODUCIBILITY-SHAPED, NOT
TRIGGER-SHAPED, BECAUSE THE TRIGGER IS UNIDENTIFIED (decode §2.4 refuted the
ring-barrier candidate at a 65/65 base rate):**

> **ZERO cascade games across ≥20 distinct games of this pinned, same-map,
> same-our-build fixture ⇒ THE `5ee3afec_game_2` CASCADE IS NOT REPRODUCIBLE BY
> RE-FIRE, and the deterministic / usable-rate form of the crash channel against
> Bean counters is CLOSED on live-game evidence.**

**What that refutation proves, and what it does not — enumerated so nothing is
over-read:**

* **IT DOES prove** the per-game rate in this exact cell is **below 18.1% (95%)**,
  i.e. the cascade cannot be *relied upon* — which is what "weapon" means.
* **IT DOES NOT prove** the cascade never happens: the ~4% background rate survives
  a 0/25 comfortably (it would need ~132 games to exclude). **A null here says
  "not repeatable on demand", never "did not happen"** — the source event is
  measured on the wire and stands regardless.
* **IT DOES NOT identify or exonerate any trigger.** No trigger is registered, so
  none can be refuted. It says only that whatever the trigger was, it is not
  reliably re-instantiated by (v180 × BC v68 × midgard).
* **IT DOES NOT generalise past this fixture.** `mapSeed`, seat, and BC's
  submission beyond v68 are all unvaried or uncontrolled. **A different opponent
  sharing the same vulnerable code shape is untouched by this result.**
* **IT DOES close the road on the right kind of evidence** — `CLAUDE.md` point 6:
  roads close only on live games, and these are live games against a real team's
  real bot.

**⭐ THE ANTI-GOODHART CLAUSE.** **Removals up is not crashes up.** Three things
would produce the number without producing the phenomenon and each is excluded by
construction: (i) *damage deaths* — excluded by the census rule (any `updateHp`
ever → `damage_death`); (ii) *a deliberate `self_destruct` policy* — excluded by
the pin holding BC at v68, the same build that showed the doctrine-4 signature in
19 of 20 games; (iii) *our own units crashing* — the metric is restricted to BC's
team and our own crash count is reported separately as a control. **If BC's
builder count stays at 4 while candidates rise, the bar is NOT met** — the
two-signature construction is what makes that automatic rather than a judgement
call at readout.

---

## §WHAT THIS LEG DOES NOT REGISTER (enumerated, so nothing is smuggled in later)

| not registered | why |
|---|---|
| any game-share or win-rate verdict | 25 games, ±23.5pp; mechanism leg |
| any Elo or ladder claim | unrated surface; the matchup is unreachable (+448) |
| a kill-round / r300 read | no plank ships; `DEFENCE_ADMISSION_BAR` does not bind |
| a `titanium_collected` or tiebreak claim | `R1000_IS_DEFEAT`; economy is instrumental |
| any trigger identification | the trigger is unknown and no candidate is registered |
| a cross-map or cross-opponent claim | one map, one pinned opponent, by construction |
| a claim that the removals are *crashes* rather than *crash-signature removals* | the census conflation is not closed |
| pooling with any unpinned or non-midgard BC games | different fixture; report separately |
| a second window / any extension | not pre-committed; registering one after the data is a re-roll |

---

## §WHERE THIS DRAFT DEPARTS FROM THE COMMISSION — flagged, not silently adapted

1. **⭐ COMMISSION ITEM 3 IS WRONG ON THE MAP.** It asks the drafter to state how
   *"unrated matches draw their own maps"* limits the claim. **They need not:
   `--map` is selectable (up to 5) and the cascade game's map is recoverable from
   `fcode match info` (`midgard`).** The leg is therefore proposed as a **same-map
   REPRODUCIBILITY probe**, which is strictly stronger than the any-map version the
   commission envisaged. **Decode §8's "map identities are not recorded" is true of
   the replay and false of the platform record.**
2. **A TRUE DETERMINISM PROBE IS NOT PURCHASABLE.** `mapSeed` is redrawn per game
   (same `s3Key`, different seed — verified across two matches) and there is no seed
   selector in the `unrated` POST body. **Same terrain: yes. Same game instance:
   no.** The word "determinism" is therefore not used in any bar or verdict.
3. **SEAT IS NOT SELECTABLE**, and the pinned/seat-B regularity is n=2. The
   commission's "same map+seat question" is answerable only on the map half.
4. **THE COMMISSION'S BAR SHAPE NEEDS A DENOMINATOR IT DID NOT NAME.** With map
   fixed and opponent pinned, 25 games can collapse toward one distinct game.
   **§DUPLICATE is an addition, and it outranks the bar** — without it a 0/25 with
   n_eff=1 would be reported as an 18% exclusion, which would be false.
5. **THE BASE RATE IS THREE NUMBERS, NOT ONE.** 1/65 (all opponents) is the
   commission's; the leg-matched one is **1/25** (BC cell, v180 era) and the
   map-matched one is **1 of 2**, which sizes nothing and is quoted only for
   context.
6. **NOT VERIFIED BY THIS DRAFTER, and the builder must not inherit them as
   measured:** that v180 is uploaded and activatable by integer; that the
   read-then-restore procedure has run 5 windows with zero leak; that the builder
   reproduced the 10 candidates on the primary this session. **All three are
   (relayed).** *(What this drafter DID verify: v180 played the source match, v176
   is the current holder on the unrated tape, and `crash_census --selftest` passes.)*
7. **ONE OPEN QUESTION THIS DRAFT CANNOT CLOSE:** whether the server honours five
   repeats of one map name. It is registered as a pre-committed probe branch in
   §FIRE GATES gate 4 rather than assumed in either direction.

---

## AUTHORITY

**Drafted by:** a fresh opus agent with no inherited session context, from the
`PROVENANCE` inputs.
**Ratification, the lock commit, the fire, and the verdict sentence:** the
**BUILDER** lane.
**Verdicts here:** none. This is a draft.
