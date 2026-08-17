# Odin (v157) — what x3r0 changed, and where the progress lives

**Written** 2026-08-17 (s48, analysis lane). **Asked by Magnus:** *"Also analyse
odin, seems like x3r0 made some progress."*

**Subject.** Platform submission **v157 "Odin"**, uploaded by **x3r0** at
2026-08-17 06:00 and **activated**, displacing our **v155 "Sleipnir"**
(`bots/_v468kladturbo`).

**Nothing in this work touched the ladder slot.** No `submit`, no `activate`, no
shard, no `results.tsv`. The only platform calls were `fcode submission list`
and `fcode submission download`, both classified **READ-ONLY** at
`docs/fcode-cli.md:125`.

---

## 0. The short version, for Magnus

1. **The source is downloadable, and I have it.** `fcode submission download` is
   read-only and works on a teammate's versions. **v153, v156 and v157 are now
   staged byte-identical** under `bots/`, alongside the v152 that was staged on
   2026-08-16. **v156 and v157 also ship x3r0's own `DOCTRINE.md` inside the
   zip — 965 lines in v157.** We are not reverse-engineering; we are reading
   their design document.
2. **Odin is a strict functional SUPERSET of our Sleipnir.** Of the 93 functions
   in `bots/_v468kladturbo`, **zero are absent from Odin**. Odin has 173.
3. **Odin ships two of OUR planks, lifted verbatim.** All four `_samestop_*`
   methods are **byte-identical** to ours, and BODYAWARE (#63) is ported behind
   a new flag. Their own source comment reads *"Sleipnir ships this branch
   ungated"* — they read our tree deliberately and carefully.
4. **The genuinely new doctrine is ARCH: a live opponent classifier that
   switches whole subsystems on and off.** We do not have this. It is the single
   most interesting thing in the build.
5. **The headline new weapon system (`_tw_*`, "terminal weapons") cannot fire
   against us.** Its gate requires the opponent be classified MACRO and requires
   that **no enemy turret has ever been seen**. Sleipnir builds forward
   sentinels. In 6 demo games it armed **0 times**.
6. **x3r0 says, in the artifact itself, that Odin has not cleared its own bar.**
   §15.7.1: *"§3b's pre-registered bar has not been run … the honest reading of
   15.4 is 'no signal at this n'."* And its direct parent `loki_leap5` carries
   their own verdict **"REJECT as configured"** (§14.5, `DOCTRINE.md:683,722`).
7. **All of Odin's treatment evidence is local arena against x3r0's own
   mimics.** Under our own point-6 rule that is an echo-loop fixture. There is
   **no unrated or live-game backing anywhere in the document** for any of the
   six new subsystems.
8. **Recommendation: register ODINVSSLEIP.** The nesting in (2) makes it an
   unusually clean A-vs-A+X shard, and it is the measurement neither team has.

---

## 1. Acquisition — the road is open, and it is read-only

```
fcode submission download 157      # Odin            (ACTIVE)
fcode submission download 156      # Loki leap v1    (never activated)
fcode submission download 153      # Loki turbo6
```

Each zip's member mtimes match the upload timestamp reported by
`fcode submission list`. Staged **unmodified** — the `.py` bytes are the
platform artifact, which is what makes every function-level identity claim below
checkable. Each tree carries a `PROVENANCE.md` marking it as x3r0's work and
forbidding edits; the precedent is `bots/_x3r0v152`, staged the same way
yesterday. `corpus/version_trees.tsv` rows added for 153/156/157 (the 157 row
previously read `UNKNOWN`).

> ⚠ **Deviation from the brief, stated for the record.** The brief asked for a
> top-of-file comment in each tree. I put the marker in a sibling
> `PROVENANCE.md` instead: editing the header would destroy byte-identity with
> the platform zip, and byte-identity is the whole instrument here — it is what
> lets us say "these four functions are *identical* to ours" rather than
> "similar".

---

## 2. The lineage — and one correction to the brief

| ver | name | by | uploaded | activated |
|---|---|---|---|---|
| 152 | Loki turbo4 (ammo/heal fix) | x3r0 | 08-15 17:55 | yes |
| 153 | Loki turbo6 (turbo4+CB aiming) | x3r0 | 08-15 20:37 | yes, then reverted |
| **154** | **Loki rc10.1** | **Moonfarm (us)** | 08-16 06:06 | yes |
| **155** | **Sleipnir v1** | **Moonfarm (us)** | 08-16 19:38 | yes |
| 156 | Loki leap v1 (repair+siege+collar, CB off) | x3r0 | 08-16 19:59 | **never** |
| 157 | **Odin** | x3r0 | 08-17 06:00 | **ACTIVE** |

x3r0's chain is **152 → 153 → 156 → 157**. Internally they call the trees
`loki_leap` (=v156) → `leap3` → `leap5` → `leap6` (=v157, shipped as "Odin"),
so **v157 is three internal iterations past v156, not one**.

Note the clock: **v156 was uploaded 21 minutes after our v155 Sleipnir**, and
v157 — the one carrying our samestop — landed the next morning. The port was
done in that overnight window.

---

## 3. The diff, quantified

Function-level identity across the four files (`main.py`, `doctrine.py`,
`eco.py`, `raid.py`). `doctrine.py` holds constants only, no functions.

| pair | identical | differ | only in A | only in B |
|---|---|---|---|---|
| v152 → v157 | 67 | 22 | **0** | 84 |
| v156 → v157 | 137 | 12 | **0** | 24 |
| **Sleipnir → v157** | 72 | 21 | **0** | **80** |
| Sleipnir → v152 | 85 | 4 | 4 | 0 |

**Two structural facts fall straight out.**

* **Nothing was ever removed.** Not one function, and **not one pre-existing
  constant changed value** from v152 to v157 (checked: 0 of the 199 v152
  constants have a different value in v157; 215 constants were added). Every new
  behaviour is behind a new flag. This is a disciplined additive build.
* **Odin ⊇ Sleipnir.** `only in A = 0` on the Sleipnir row means Odin contains
  every function our shipped bot had, including our own planks.

The last row also re-states what Sleipnir *is*: **v152 plus samestop**. Our
delta over their base was 4 new functions and 4 modified ones.

Line counts: v152 5,518 → v153 6,847 → v156 9,689 → **v157 11,181**. Sleipnir is
5,777.

---

## 4. (a) Mechanisms — added, removed, tuned

**Removed: nothing.** **Tuned: nothing** (no shared constant moved).
**Added: seven subsystems.** Which subsystem, what it does, whether it is
actually ON in Odin, and whether it serves the kill:

| # | plank | file | v | ON? | one line | serves |
|---|---|---|---|---|---|---|
| 1 | **COLLAR** `_collar_*` (12 fn) | raid | 156 | **yes** | barriers ("bricks") onto the **8 orthogonal seats of the enemy Core**, then *held* — tended and re-healed from the 4 diagonal corners | **kill speed** |
| 2 | **REPAIR** `_rep_*` (9 fn) | eco | 156 | **yes** | heals our own damaged conveyors/splitters/harvesters (1 Ti → +4 HP) and rebuilds the two-wide trunk hole the inherited repair refuses | economy/survival |
| 3 | **SIEGE** `_sge_*` (8 fn) | raid+main | 156 | **yes** | forward-sentinel siting **band** around the enemy core, staged massing, and **just-in-time Ti→ammo conversion** | **kill speed** + turret economy |
| 4 | **SAP** `_sap_*` (3 fn) | main | 156 | **yes** | builder melee (2 Ti → 2 dmg) against turrets besieging **our own** core, d≤8 of our core | defence |
| 5 | **ARCH** `_arch_*` (4 fn) | main | 156 | **yes** | classifies the **opponent** live into DEFAULT / PRESSURE / MACRO / MACRO_WEAK and publishes it to the comms store | **doctrine switch** |
| 6 | **TW** `_tw_*` (20 fn) | raid | 157 | **yes, but** | "terminal weapons" — a forward **launcher** that plucks seated enemy healers off their own wall every round for 0 Ti / 0 ammo, and a forward gunner | stall-break, **not** kill speed |
| 7 | **T5** `_t5_*` (15 fn) + **CB** aiming | raid+main | 153 | **no** | forward-gunner nests, idle-heal, counter-battery aiming | — (inert) |

**T5 is 100% inert in the shipped build, and this is worth knowing** because it
is a third of the added function count. Its three `True` flags
(`T5_IDLE_HEAL_ON`, `T5_IDLE_REPAIR_ON`, `T5_NEST_WALK_ON`) are all **orphaned
sub-flags under `False` masters** — verified: `raid.py:1519` gates
`T5_NEST_WALK_ON` behind `T5_NEST_ON=False`, and `main.py:863` gates
`_t5_zero_idle` (the only reader of the two idle flags) behind
`T5_ZERO_IDLE_ON=False`. The one live piece is `_t5_note_fwd_build`, which
publishes the forward-sentinel count to a slot COLLAR reads.

The **CB** block is likewise off except `CB_TARGET_BUILDERS_ON`, which is
itself dead behind `CB_LIVE_TARGET_ON=False` (x3r0 documents this at
`doctrine.py:1923`). ⚠ One correction I owe: `CB_OVER_HEAL_ON = True`
(`doctrine.py:799`, live at `main.py:1411`) **is** load-bearing — it predates
the v153 block, ships in v152, and is explicitly excluded from the v153 revert.

**Why so much of v153 is switched off:** x3r0's own ladder read
(`doctrine.py:1894-1895`) is **v152 +63.8 Elo over 57 matches, v153 −39.8 over
4**. They reverted the whole CB/T5 generation on that. ⚠ Note the n: **4
matches** carried the revert.

---

## 5. (b) What Odin adopted FROM our line — MEASURED, byte-level

This is not inference. Extracting each function's source text and comparing
strings:

| our function (`bots/_v468kladturbo/eco.py`) | in Odin |
|---|---|
| `_samestop_arm` (37 lines) | **IDENTICAL** |
| `_samestop_fire` (25) | **IDENTICAL** |
| `_samestop_plan` (16) | **IDENTICAL** |
| `_samestop_stand_pref` (19) | **IDENTICAL** |
| `_wire_on_build` (14) | **IDENTICAL** |

And the port is *documented by them*, in `bots/_x3r0v157odin/DOCTRINE.md` §15,
titled **"THE SLEIPNIR PORT: SAMESTOP + BODYAWARE"**:

> *"Fresh copy of `bots/loki_leap5` carrying **two of Moonfarm's planks** out of
> `bots/mate_sleipnir` (v155): **SAMESTOP (QUEUE #50)** and **BODYAWARE
> (#63)**."*

The one deviation is a flag they added around **our** plank, and their comment
in `eco.py` says so out loud:

```
elif et == EntityType.BUILDER_BOT and LOKI_BODYAWARE_ON:
    # BODYAWARE (#63).  GATED FOR ABLATION (leap6 only --
    # Sleipnir ships this branch ungated).
```

Their stated reason (§15.2) is that we fused the two planks into one bot and
**"nobody has ever measured which of the two carries the gain"** — a fair
criticism of our own shipping, and their `leap6_ss` / `leap6_ba` ablation trees
exist to answer it.

They also verified the port with a **trajectory-hash identity check**: with both
flags off, their tree reproduces its parent bit-for-bit (`c569801425cc ==
c569801425cc`, and again `db5bf56c950d` in a second invocation). That is a
better flag-off control than we usually build.

**Anything else lifted from us? No.** Every other new prefix — `_collar_*`,
`_rep_*`, `_sge_*`, `_sap_*`, `_arch_*`, `_tw_*`, `_t5_*` — appears in **0 files
under `bots/`** outside the staged x3r0 trees. The traffic is one-way in this
direction: they took samestop and bodyaware, and nothing of theirs came to us
except the v152 base we already had.

**One shared-ancestry caveat on COLLAR, so we do not overclaim novelty in either
direction.** Their v152 forks from **our** `_v223sealrepair`, so the *baseline*
collar — barriers on the enemy core ring, laid from the corners — is common code
in both trees, and Sleipnir does it too. x3r0's plank is a delta on that shared
base, and they say precisely what the delta is (`doctrine.py:3034`):

> *"turbo7 bricks ~2.5 seats by r150 and does not HOLD them. **The collar is not
> a new mechanism, it is UPTIME on an existing one.**"*

Our own `_det254collarseal` is a *different* delta on the same base — width
(8 heal seats → all 12 spawn-ring tiles) and build-before-attack priority. The
two are near-orthogonal and would stack, with one collision: their SQUAT branch
prefers a builder *standing* on a seat, and our corner-conversion rule would
brick over the tiles their tenders stand on.

---

## 6. (c) What is genuinely NOVEL — neither line had it

### ARCH — live opponent classification. This is the find.

Signals accumulate in comms slot 13 from any unit; the **Core alone** classifies
(`main.py:951-980`) and publishes to slot 9. Taxonomy derived from **400 of
their own ladder replays** (`doctrine.py:2415`). Memory 60 rounds, so it
re-classifies mid-game.

**Exactly three sites in the whole tree read it** (verified —
`grep '_archetype('` returns 3 call sites plus the definition):

| archetype | what changes |
|---|---|
| DEFAULT | **nothing** — a pure no-op class |
| PRESSURE | **SAP on** (`main.py:1177`) — home counter-siege enabled |
| MACRO / MACRO_WEAK | **COLLAR_SQUAT on** (`raid.py:1608`) — bodily seat denial, unremovable because builders cannot fire on builders; **and the entire TW layer** (`raid.py:2164`) |

So it resolves to two behavioural buckets, and MACRO vs MACRO_WEAK has **no**
behavioural consequence — both consumers OR them. But the doctrine is the point:
**a bot that reads who it is fighting and turns whole subsystems on and off.**
Our line has nothing like it. Everything we ship is unconditional.

### TW — "terminal weapons", and why it will not fire at us

Diagnosis (`doctrine.py:3330-3361`), from **144 local games**: in stalls, enemy
**damage/round == heal/round to two decimals in 42 of 46 stalls**, at 3.1 HP/r
and 23.4 HP/r alike. The enemy heal wall is a servo capped at `4 × manned seats`.
Conclusion: **buy seats, not damage.**

* **W3 PLUCK** — a launcher on one of *their* ring corners, where two heal seats
  sit inside the `d²≤2` pickup disc, throws an enemy builder off the wall **every
  round for 0 Ti and 0 ammo**. This is the LOKI launcher-kidnap asymmetric guard
  (`can_launch` is team-blind), and they cite it as such.
* **W1 GUNNER** — one forward gunner at their ring, 7 dmg / 4 ammo per round.
* **TW_COLLAR_BONUS = 24** — while a TW launcher stands at their ring, the
  collar's 32-Ti brick cap rises by 24, converting plucked-open seats into
  permanent bricks. That is the ratchet, and it is the neatest idea in the tree.

**The gate has six terms, all required** (`raid.py:2147-2193`), and two of them
close it against us permanently:

```
if a != ARCH_MACRO and a != ARCH_MACRO_WEAK:  return False
if self._tw_turret_seen(ct):                  return False   # a LATCH
```

Sleipnir builds forward sentinels, and Odin classifies us **PRESSURE**, not
MACRO. **TW is aimed at heal-wall macro bots and is inert against any opponent
that shows a turret** — which is our line and most of the top field.

⚠ **And by x3r0's own numbers, the shipped TW configuration is the weaker
half.** Their 60-game paired read (`DOCTRINE.md:683,722`) reads **wins 30/60 for
`leap5` vs 41/60 for `leap3`, 0 cells improved / 4 unchanged / 6 regressed**,
with the verdict **"REJECT as configured."** `TW_RESERVE_GUN = True` drives
gunner builds **15 → 0** across 60 games, and in `leap3`'s own games the gunner
class won **77% (n=13)** against 67% launcher-only (n=15). They left the flag on
so the directory would keep matching what §14 reports — then forked leap6 from
leap5 and shipped it. **In Odin, W1 is effectively dead and only launcher #1
fires ungated.**

⚠ **Free upside they left on the table, and it is ours to take.** `_tw_throw_sites`
(`raid.py:2526-2555`) sorts landing tiles **farthest from their core** to
maximise walk-back, and refuses tiles within `d²<9` of their core or `d²<2` of
our buildings. **There is no border preference and no crash-induction intent.**
Under our directive, a farthest-first ordering that *also* preferred map-border
tiles would add crash-induction at zero marginal cost. They are throwing 4,516
builders per 60 games and taking the stale-cache exceptions as an unmeasured
side effect.

### SIEGE-JIT — the cleanest small plank in the build

`AMMO_JIT_ON=True` replaces the parent's whole `ammo_target` ladder: opens
converting at **r1** (their measurement says the field opens r1 and v152 opened
r11), sizes the magazine at 3 rounds of *actual* burn (5/round per sentinel,
4 per gunner), and stops converting when ammo ≥20 has not fallen in 3 rounds —
against a measured 59.5 Ti sitting idle as ammo at r200. It costs nothing, it
touches no cost-scale, and its diagnosis comes from **145 games / 290 game-sides
of top-5 ladder replays** — the only part of the build whose evidence is drawn
from live ladder play at all.

The same replay cut produced the siting band (`doctrine.py:2706-2716`, 145 games
/ 290 game-sides): the furthest a sentinel that **ever** hit a core stood was
**6.364** (max over 402 core-hitting sentinels), the winners' band is
**2.5-5.7** — and of *their own* sentinels, **37.8% land in band and 35.1% land
beyond 6.4, "structurally incapable of ever contributing to the win
condition. A third of our sentinel budget, spent on nothing."** The shipped band
is `4·d² ∈ [25,129]`, i.e. d ∈ [2.5, 5.7], ranked toward d=4.30. **This is a
finding about forward-turret code our two trees SHARE, so it plausibly indicts
ours too — worth re-deriving on our own replays independently of anything else
here.**

---

## 7. (d) Constants that moved

**None.** That is the finding. Of the 199 top-level constants in v152, **0 have
a different value in v157**; 215 were added. The table below is therefore the
new gates rather than a before/after, showing which version introduced each and
whether it is live in Odin.

| block | new | introduced | live in Odin |
|---|---|---|---|
| `T5_*` | 39 | v153 | **no** (3 `True` flags all under `False` masters) |
| `TW_*` | 38 | **v157** | yes, but gated to MACRO + never-seen-a-turret |
| `SIEGE_*` | 31 | v156 | yes (`SITE`, `MASS`, `JIT` on; `SCREEN` off) |
| `REPAIR_*` | 24 | v156 | yes |
| `COLLAR_*` | 24 | v156 | yes |
| `CB_*` | 17 | v153 | **no** (only `CB_OVER_HEAL_ON`, which predates v153) |
| `SAP_*` | 14 | v156 | yes |
| `ARCH_*` | 14 | v156 | yes |
| `SCREEN_*` | 6 | v156 | **no** (`SCREEN_ON=False`) |
| `LOKI_*` | 3 | **v157** | **`LOKI_SAMESTOP_ON=True`, `LOKI_BODYAWARE_ON=True`** — ours |
| `AMMO_JIT_ON` | 1 | v156 | yes |
| `LAUNCHER_PLUCK_ON` | 1 | v156 | **no** — spawn-deletion, refuted as worse than bricking |

Selected values worth carrying: `TW_MIN_RND=60`, `TW_MIN_MANNED=3`,
`TW_LAUNCH_CAP=2`, `TW_COLLAR_BONUS=24`, `COLLAR_TI_BUDGET=32`,
`COLLAR_LANES=3`, `COLLAR_SURGE_MULT=2`, `SIEGE_BAND_MIN/MID/MAX_Q4=25/74/129`,
`SIEGE_MASS3_HP=400`, `REPAIR_MIN_DMG=4`, `SAP_BAND_DSQ=64`, `ARCH_MEMORY=60`,
`ARCH_R_MACRO=140`.

⚠ **Note `LAUNCHER_PLUCK_ON=False` and `TW_PLUCK_ON=True` are different
planks**, deliberately (`doctrine.py:3363-3367`): the first is launcher
*spawn-deletion* (throwing fresh builders off their own spawn ring), which they
refuted as worse than bricking the tile; the second plucks *seated healers off a
manned wall*. Different target.

---

## 8. Demo observations — MEASURED, n=6, mechanism-only

**6 games, Odin vs Sleipnir, 3 maps × both seat orders, seeds 990100/990107/990114.**
`fcode run`, tle 10. **These are NOT a win-rate read** — n=6 and the arms are
not paired against a common opponent. They exist to watch mechanisms fire.

Odin's subsystems all log to stdout, and **locally** stdout survives into the
replay, so the log lines are a free instrument. (They are stripped from
*platform*-downloaded replays — CLAUDE.md's s28 correction — so this instrument
is local-only.)

| map / seed | seats | result | kill round | Odin log lines |
|---|---|---|---|---|
| midgard 990100 | Odin A | Odin wins | **78** | ARCH 1, COL 7, REP 2, SGE 4 |
| midgard 990100 | Odin B | Sleipnir wins | **82** | ARCH 1, COL 5, REP 1, SGE 4 |
| ragnarok 990107 | Odin A | Sleipnir wins | **349** | ARCH 3, COL 26, REP 15, SGE 2 |
| ragnarok 990107 | Odin B | Sleipnir wins | **183** | ARCH 1, COL 12, REP 8, SGE 2 |
| fjordgate 990114 | Odin A | Odin wins | **193** | ARCH 3, COL 5, REP 2, SGE 2, TW 1 |
| fjordgate 990114 | Odin B | Odin wins | **113** | ARCH 1, COL 7, REP 6, SGE 2 |

**All 6 ended `core_destroyed`. No r1000.** 4 of 6 landed by r300.

**What fired:**

* **ARCH classified in every game**, and re-classified mid-game twice —
  `ARCH DEFAULT r=144` then `ARCH PRESSURE r=333` on ragnarok. Against Sleipnir
  it settles on **PRESSURE**, as early as r6.
* **COLLAR bricked the enemy core ring in every game.** Direct confirmation on
  midgard: our decoder puts team 0's core at (2,2)-(3,3) and team 1's at
  (26,26)-(27,27), and Odin's log reads `COL brick (25,26) (26,28) (27,28)
  (28,26) (28,27)` — five of the eight tiles orthogonally adjacent to the enemy
  core footprint. **The collar is enemy spawn-and-heal-seat denial**, and it is
  live on the ladder right now.
* **`SGE jit on` in all 6** — the just-in-time ammo policy is universally
  active.
* **REPAIR scaled with game length** — 15 lines in the 349-round game, 1-2 in
  the short ones, which is what a repair loop should do.
* ⚠ **`COL surge on` / `COL surge off` oscillated round-by-round on ragnarok**
  (on r83, off r84, on r85, off r86 … through r99). Reported as an observation,
  not a verdict — I did not establish it costs anything.

**TW armed ZERO times in 6 games.** The single `TW` line was
`TW gunkill (4,2)` — and reading `_tw_note_gun_shot` (`raid.py:2789`) that
marker is printed by **any** of their gunners near the enemy core, not by a TW
weapon. **None of `TW gate`, `TW resv`, `TW launch`, `TW pluck` or `TW gun`
appeared in any game.** This is exactly what §6's gate predicts against a
turret-building opponent, and it is the sharpest single observation here: **the
mechanism x3r0 spent three internal iterations on does not engage our bot.**

**Seat-seal parity.** Distinct tiles of the opponent's 8 core seats sealed by a
standing building (destroys applied):

| round | Odin | Sleipnir | n games |
|---|---|---|---|
| r60 | 3.00 | 2.83 | 6 |
| r100 | 4.25 | 4.00 | 4 |

x3r0's `leap6_nocol` ablation tree exists because of their own worry that *"the
v156 collar **degrades** seat denial — Sleipnir holds 4.06 seat buildings at
r100 with no collar at all, v156 scores 2.55"* (`DOCTRINE.md:939`). **My n=4
does not reproduce that gap** — it reads parity. But n=4 cannot resolve it in
either direction, and their cited source doc (`analysis/team_bot_recommendation.md`
§3c) is **not in the zip**, so their 4.06/2.55 carries no n I can see. **This is
the single most decision-relevant open question in the build**, and it is
exactly what a shard would settle.

⛔ **Instrument failure, disclosed.** My per-unit CPU/TLE probe returned **0
events** — I mis-mapped the `botOutput` field and it measured nothing. **Do not
read "TLE = 0" from this work as evidence of anything.** The only CPU numbers
available are x3r0's own (§15.5): worst p95 **186.2 µs = 1.86% of the 10,000 µs
budget**, ratio 1.12× over the parent, on nordkap × 150 timed rounds.

---

## 9. Assessment — where the progress likely lives

**MEASURED (by me, this session, verifiable from the staged trees):**

* Odin is a strict functional superset of Sleipnir; nothing was removed and no
  constant was retuned. **The build is additive, and its base is our shared
  v152/`_v223sealrepair` ancestry.**
* Four `_samestop_*` functions plus `_wire_on_build` are **byte-identical** to
  ours.
* T5/CB — a third of the added surface — is **inert**.
* TW **did not arm in 6 of 6 games** against Sleipnir, and its gate explains why.
* Seat-seal at r60/r100 is **parity** at n=6/n=4.

**MEASURED (by x3r0, quoted with their n, all LOCAL unless noted):**

* v152 **+63.8 Elo / 57 matches** vs v153 **−39.8 / 4 matches** — *live ladder*,
  and the only live number in the document. ⚠ n=4 carried the revert.
* Siting/ammo diagnosis from **145 games / 290 game-sides** of top-5 ladder
  replays; ARCH taxonomy from **400 ladder replays** — *live replays, analysed
  offline*, not treatment measurements.
* Heal-wall servo from **144 local games**; 42 of 46 stalls at damage == heal.
* `leap5` (Odin's direct base) **30/60 vs leap3's 41/60**, verdict **"REJECT as
  configured"** — local, vs their own mimic.
* Their instrument's null is **47.8%, not 50%** (a bot vs a byte-identical frozen
  copy of itself, n=270), and two runs of an identical config returned **35.6%
  and 43.3% at n=90**. They record that their tree is **not deterministic under
  a fixed seed**.

**INFERRED — my reading, and it should be read as a hypothesis:**

1. **The progress most likely lives in SIEGE, not in the headline weapons.**
   `AMMO_JIT` and the siting band are cheap, mechanism-clear, cost no
   cost-scale, and are the only planks whose diagnosis came off **live ladder
   replays**. A sentinel that is structurally out of range 35% of the time is a
   defect in code we *share*, and fixing it is close to free.
2. **COLLAR is the loudest plank and the one I would put a shard on**, because
   it fires constantly (26 log lines in one game), it is enemy-core-facing, and
   **x3r0's own ablation tree exists because they suspect it makes seat denial
   worse than ours**. Loud, live, and disputed by its own author is the profile
   of the plank most worth measuring.
3. **ARCH is the doctrine worth stealing regardless of whether Odin outscores
   Sleipnir.** It is 4 functions, one comms slot, and three read sites. Its
   current payload is thin (two buckets, one of them a no-op) but the *frame* —
   condition a plank on a live read of the opponent — is a capability our line
   does not have and would be cheap to add. Under `PLAY_THE_PLAYERS` this is the
   single most portable thing in the build.
4. **TW is off-currency for us.** By its author's own §12.6 it "sold damage to
   buy seats", it cannot fire before r60, empirically opens r140-360, and its
   stated output is converting r1000 stalls into late kills. That lands in the
   **r300+ band where our own field data reads 0.82 against us**. It is a
   stall-breaker, not a kill accelerator, and it is inert against turret
   opponents anyway.
5. **REPAIR is the plank I would watch for a kill-round cost.** It sits above
   the role split and can claim a whole round; x3r0 pre-registers the risk
   themselves — *"a body that heals is a body that did not arrive; ARRIVAL is
   the scarce quantity in this whole lineage."* Under `DEFENCE_ADMISSION_BAR`
   this is exactly the shape that needs its r300 timely-kill rate checked.
6. **The build has not cleared its own bar, and its author says so.** §15.7.1:
   the pre-registered 45-map / 3-rep panel plus the 13-big-map additivity test
   **has not been run**; §15.7.2: the crashtest guard **has not been run**; the
   smoke read is 5/6 vs 5/6 at n=6 cells and is explicitly labelled *"nothing
   exploded, not a result."* **Odin's superiority over Sleipnir is currently
   unmeasured by anyone.**

⚠ **One coordination item Magnus should see, stated neutrally because I cannot
know what was agreed off-repo.** `DOCTRINE.md` §15.7.3, shipped *inside the v157
zip*, reads: *"`fcode submission upload` AUTO-ACTIVATES and would displace
Moonfarm's live v155 mid-run; that needs Moonfarm's agreement and the user's
approval, separately. Nothing here was uploaded, and no `fcode submission`
command of any kind was run."* That tree was subsequently uploaded as v157 and
did displace v155. x3r0 identified the hazard correctly and wrote it down; only
Magnus knows whether the agreement it names was given.

---

## 10. Should the builder register ODINVSSLEIP?

**Yes. This is the strongest shard case I have seen in a while, for a design
reason rather than a curiosity reason.**

**Why the design is unusually clean.** `only in A = 0` on the Sleipnir → v157
row means **Odin contains every plank Sleipnir has, including our own samestop
byte-for-byte.** So an ODINVSSLEIP shard is not "bot X vs bot Y" — it is a
**nested A vs A+X**, where X is the whole v156/leap stack (collar-uptime,
repair, siege, sap, arch, tw). Almost nothing is confounded: the shared base is
literally shared source. That is the comparison the V140VS152 pattern was built
for, and it is a better-conditioned instance of it than V140VS152 itself was.

**What it would settle, in order of value:**

1. **Does the v156 stack add or subtract on top of the samestop base?** Nobody
   has measured this. x3r0's own smoke is n=6 cells and self-labelled "no
   signal"; our SLEIPH2H (n=2,700) measured Sleipnir at 55.33 [53.46, 57.21]
   over **v152**, which is now two generations stale.
2. **The collar/seat-denial dispute.** x3r0 suspects their collar *degrades*
   seat denial relative to ours (4.06 vs 2.55 at r100, n unstated, source doc
   not in the zip); my n=4 reads parity. A shard with a seat-seal-at-r100 column
   answers it directly, and the answer is actionable for both trees.
3. **The kill-round question.** REPAIR and COLLAR-TEND are both "spend a body's
   round on maintenance" planks. Our `DEFENCE_ADMISSION_BAR` is a **timely-kill
   rate at r300**, and this shard would produce that column for free.

**Sizing.** SLEIPH2H's n=2,700 gave ±1.87pp. For the same precision here, ask
for **n ≈ 2,700 in the same local paired form**. Local batteries carry
**DEFF ≈ 0.98** (s39 audit, balanced-by-construction), so the naive interval is
correct and marginally conservative — do **not** apply the platform 1.53/1.83
constants to it.

**Register these columns, not just win share** — the whole point is attribution,
and the mechanism logs make it nearly free:

* kill round + `win_condition`, and the **share of all games ending in a
  core-kill by r300** (the programme's primary, not the kill-conditioned share)
* **seats sealed on the opponent's 8 core-seat tiles at r60 / r100 / r150**
* the ARCH class Odin settles on, and its round
* **whether TW ever armed** (a `TW gate` line). My prior from n=6 is that it
  never will against Sleipnir; if the shard shows it arming, my §6 reading is
  wrong and I want to know.

**Pre-registration falsifier I would suggest:** *if Odin's game share over
Sleipnir does not clear 50% at n≈2,700, the v156 stack is not a net gain on the
shared base, and the components worth porting are the individually cheap ones
(ARCH frame, SIEGE-JIT, siting band) rather than the stack.*

**Two things a shard cannot do, so plan around them.** (i) It is a **local
fixture** — under point 6 it can prioritise a road but cannot close one; a live
read still needs unrated legs. (ii) x3r0 records that **their tree is not
deterministic under a fixed seed** and that run-to-run drift on a single cell is
the size of the effect (their `loki_leap5` read 393 turns in one invocation and
285 in another on the *identical* cell). **Pair within-invocation, and treat any
single-cell turn count as uninterpretable.**

**If the source had NOT been obtainable** — it was, but for the record — the
next-best measurement would have been behavioural: `_x3r0v157odin`'s ladder
replays via `tools/corpus/replay_events.py`, cutting first-build order,
enemy-core-ring barrier placement rounds, and forward-turret siting distance,
against the same cuts for v152. That reaches the collar and siege planks (both
leave unmistakable geometric signatures) but would have missed ARCH and TW
entirely, since both are gate logic with no distinctive footprint when they do
not fire. The archive tail is also partial in the last ~90 minutes, so a bot
active for only ~20 minutes would have had almost no rows.

---

## 11. Provenance and limits of this document

* **Staged trees:** `bots/_x3r0v157odin`, `bots/_x3r0v156lokileap`,
  `bots/_x3r0v153turbo6` — byte-identical platform artifacts, each with a
  `PROVENANCE.md`. Committed and pushed s48.
* **x3r0's own document** is `bots/_x3r0v157odin/DOCTRINE.md` (965 lines), which
  ships inside the zip. Every §-reference above resolves there. Files it cites
  and which are **not** in the zip — `analysis/team_bot_recommendation.md`,
  `analysis/heal_wall_diagnosis.md`, `tools/leap5_pool.py`, every `mimic_*` —
  are **unverifiable from our side**; numbers sourced only to those are quoted
  as their claims, not as findings.
* **My demo n is 6 games.** No win-rate claim is made or implied from it. The
  seat-seal numbers are n=6 (r60) and n=4 (r100).
* **My CPU/TLE probe did not work** (§8). Nothing about Odin's CPU is claimed
  here beyond x3r0's own §15.5.
* **This is a teammate's code, read as analysis.** Where I flag something as a
  defect — the stale MACRO comment, the surge oscillation, the shipped
  "REJECT as configured" base — x3r0 documented most of it first, in their own
  document, against themselves. The build is more honest about its limits than
  its ship decision was.
