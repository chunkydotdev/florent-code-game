# REPLAY STUDY — "not adgato" v25 rush (2026-08-21)

**Status: COMPLETE.**


Commissioned by the lane; author = replay-study subagent. Read-only study; no
matches fired, no bot/tool/QUEUE edits, nothing committed.

## 0. Provenance and freshness

- Corpus synced by the commissioning lane at ~2026-08-21T12:52Z; this study
  started 2026-08-21T12:57:34Z (`date -u`, same shell).
- Tables used: `corpus/league_matches.tsv`, `corpus/ladder_games.tsv`,
  `corpus/meta_join.tsv`, `replay_archive/`.

### Archive coverage — CHECKED (the premise flagged UNVERIFIED)

`ls replay_archive | grep -c '^<matchid>'` for each v25 match:

| match | opponent of not adgato | archived files |
| --- | --- | --- |
| `e0e72d55-c9cb-4213-8f5f-f1855cc66c2b` | **OpenSverige v176 (us)** | **6** (5 replays + meta) |
| `7584fe46-…` O(1) v38 | O(1) | 0 |
| `96e07f65-…` team lazy v253 | team lazy | 0 |
| `7b162fa2-…` Besvikomat v75 | Besvikomat | 0 |
| `5ca855f9-…` Juusto v13 | Juusto | 0 |
| `1120a4f0-…` Focalground v32 | Focalground | 0 |
| `fead2eb8-…` Erebus v178 | Erebus | 0 |
| `a7a227f0-…` gsxWins v87 | gsxWins | 0 |

⇒ **Only OUR match is decodable from disk.** The archiver stores our own
matches; other teams' matches are metadata-only in `league_matches.tsv`.
Q3 (stability on non-us sweeps) is therefore answered from metadata +
`league_matches` shape, and is labelled as such. See §4.

### The v25 sweep, from `corpus/league_matches.tsv` (metadata, free channel)

All matches with `not adgato` at version **25**, 2026-08-21 (n=8 rows incl. one
`0-0` un-scored row):

| createdAt (Z) | opponent (ver) | score (adgato first) | adgato eloDelta |
| --- | --- | --- | --- |
| 10:52:59 | team lazy (253) | **5-0** | +15.80 |
| 11:12:59 | Juusto (13) | **5-0** | +16.15 |
| 11:32:59 | gsxWins (87) | 3-2 | +3.74 |
| 11:51:10 | farming_200s (19) | 0-0 (no result recorded) | — |
| 12:01:10 | **OpenSverige (176) = us** | **5-0** | +13.80 |
| 12:11:10 | Besvikomat (75) | **5-0** | +10.24 |
| 12:21:10 | O(1) (38) | **5-0** | +18.58 |
| 12:31:10 | Focalground (32) | 2-3 (adgato loses) | +6.49 |
| 12:41:10 | Erebus (178) | 4-1 | +8.59 |

**33 of 40 games (82.5%) in the v25 era, 8 matches, all 2026-08-21 10:52–12:41Z.**
Denominator note: this is `league_matches.tsv` as synced ~12:52Z; later matches
are not in it.

v23 for comparison (same table, 2026-08-21 04:52–09:52Z, n=13 matches):
match record 7-6, game record 36-29 (55.4%) — **v23 was a mid-board bot.**
v25 is a different bot, not a tuned v23. (v24 appears in 2 rows at 10:12/10:32Z,
4-1 and 5-0.)

---

## 1. MECHANISM — measured, 5 of 5 games of match `e0e72d55` (us, v176, all losses)

Instrument: `tools/corpus/replay_autopsy.py` (existing decoder, self-checking:
attributed damage must equal summed `UpdateHp` deltas on the core id; **all 10
core ledgers in these 5 games printed `MATCH`**). In every game we are **team A**,
not adgato is **team B** (confirmed by `league_matches.teamAName = OpenSverige`
and by `ladder_games.won = 0` with `winner_seat = b` on all five rows).

### 1.1 Their entire build, per game — this is the whole list, not an excerpt

| game | map (size) | B builder spawns | B total builds, whole game | sentinel build rounds | sentinel tiles | B launcher |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | glacierkeep 30x30 | **1** (r0) | **5** | r30, r31, r33, r34 | (11,6) (10,7) (10,6) (11,5) | — |
| 2 | helheim 18x18 | **1** (r0) | **8** | r40, r41, r42, r43 | (5,5) (4,6) (6,6) (5,7) | r38 @(4,5) |
| 3 | fimbulwinter 20x20 | **1** (r0) | **6** | r35, r36, r38, r39 | (4,0) (7,1) (5,0) (6,1) | r33 @(6,0) |
| 4 | yggdrasil 30x30 | **1** (r0) | **5** | r43, r45, r46, r48 | (7,0) (8,0) (7,1) (8,3) | — |
| 5 | bifrost 26x12 | **1** (r0) | **5** | r43, r45, r46, r48 | (2,11) (3,11) (3,9) (3,10) | — |

**They build ONE builder bot, at round 0, and never spawn another — 5/5.**
Their non-sentinel builds are 0–3 barriers plus (2/5) one launcher. **Zero
harvesters, zero conveyors, zero gunners, zero economy — 5/5.**

### 1.2 What kills our core

| game | first core damage | core dead | rounds under fire | attributed source | builderAttack by B (whole game) |
| --- | --- | --- | --- | --- | --- |
| 1 | r31 | r47 | 16 | **sentinel 558/558** | **0** |
| 2 | r41 | r59 | 18 | **sentinel 648/648** | **0** |
| 3 | r36 | r55 | 19 | **sentinel 648/648** | **0** |
| 4 | r44 | r62 | 18 | **sentinel 612/612** | **0** |
| 5 | r44 | r66 | 22 | **sentinel 756/756** | **0** |

**100% of core damage in 5/5 games is sentinel fire. Zero builder attacks by
them, all game, in all five games.**

Damage profile is exactly the sentinel arithmetic: 18 dmg, reload 2 ⇒ 9 dmg/round
per sentinel. Observed per-round series climb 18 → 36 as sentinels come online and
then sit at **36/round flat** (= 4 sentinels × 18 / 2 rounds) until the core dies.
Overkill above 500 HP is our own healing: `healed = +56/+132/+144/+100/+248`.

### 1.3 Ammo

| game | B titanium→ammo | A (us) titanium→ammo |
| --- | --- | --- |
| 1 | **400** | 20 |
| 2 | **380** | 156 |
| 3 | **384** | 32 |
| 4 | **440** | 20 |
| 5 | **450** | 130 |

They convert **380–450 of their 500 starting titanium into ammunition** (5/5).
10 ammo/sentinel shot × 4 sentinels × ~18 rounds ≈ 360 ammo — **the conversion is
sized to the kill, with almost nothing left over.** INFERENCE: this is a
one-shot all-in; they have no economy to refill ammo, so a rush that fails to
kill leaves them with a dead position (consistent with the 2 matches they did
not sweep — see §4).

### 1.4 The clock — per-round trace of their lone builder

Instrument: a scratch trace built **on `tools/replay_census.py` primitives**
(`fields` / `parse_entity` / `read_pos` / `scalars`) — no new decoder. Distances
are min d² from their bot to our **core footprint** (2x2, NW corner = core pos).

| game | map | our core | their core | their bot enters our CORE vision (d²≤36) | enters BUILDER vision (d²≤20) | bot stops moving | first sentinel | idle before building | min d² sentinel→our core |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30x30 | (14,2) | (14,26) | **r18** | r19 | r25 | **r30** | 5 | 13 |
| 2 | 18x18 | (2,8) | (14,8) | **r7** | r8 | r39 | **r40** | 1 | 5 |
| 3 | 20x20 | (2,1) | (16,17) | **r18** | r20 | r34 | **r35** | 1 | 2 |
| 4 | 30x30 | (3,3) | (25,25) | **r32** | r34 | r42 | **r43** | 1 | 13 |
| 5 | 26x12 | (2,5) | (22,5) | **r20** | r22 | r42 | **r43** | 1 | 16 |

**THE WARNING WINDOW IS LARGE AND IT IS FREE.** Their bot is inside our own
core's vision radius **12 / 33 / 17 / 11 / 23 rounds before the first sentinel
exists** (median 17), and **29 / 52 / 37 / 30 / 46 rounds before our core dies**
(median 37). Nothing about this rush is a surprise to a bot that looks.

**⭐ A DETERMINISTIC r0 FINGERPRINT: `B ammo = 120 at round 0` in 5 of 5 games.**
Read off `updatePlayers` field 7 on turn 0. Start is 500 Ti; at r0 they hold
Ti=350 / ammo=120 — i.e. **30 Ti on the one builder bot and an immediate
`convert_ammo(120)`**, before anything else happens. They then drip-convert
~20 Ti/round during the barrage to fund 4 sentinels × 10 ammo × 2-round reload
(g1: their Ti runs 420 at r29 → 10 at r46, core dies r47 — **budgeted to land on
zero**). ⚠ **We cannot read the enemy's ammo balance in-game** (`get_global_ammo()`
is own-team). This fingerprint is an analysis-time discriminator, not a runtime
sensor. The runtime sensor is the lone bot's approach (above).

### 1.5 Geometry

Sentinels are planted **3–6 tiles from our core footprint** (min d² 2–16, all
≤ 32 = sentinel attack r²), in a tight 2x2-ish clump around their bot, on the
**far side from where our units are**. In 5/5 they are built by the SAME single
builder bot that walked there; the bot then sits adjacent and (g2 only, 8 events)
heals them.

Sentinel line-fire **ignores obstacles**, so our barriers and buildings between
the nest and the core do nothing. INFERENCE: this is why they pick sentinel over
gunner despite the 2:3 price and 10-vs-4 ammo cost — gunner shots are blocked and
gunner range is r²=13, which would force them adjacent to our core.

### 1.6 Their launcher — present in 2/5, and it is anti-defender

| game | B launcher built | B throws |
| --- | --- | --- |
| 2 | r38 @(4,5) | r39/r45/r51/r57 — all `bot_team=A`, i.e. **kidnapping OUR builder** and throwing it to (5,0), away from the nest, four times |
| 3 | r33 @(6,0) | r34/r35/r37 reposition their OWN bot; r36/r38 throw **our** bots from (5,1)/(6,1) out to (11,1) |

INFERENCE: the launcher is conditional — it appears in exactly the two games where
our units were near the nest site, and it is used to evict the defender rather
than to insert. **They have the kidnap trick too, and they use it defensively.**

---

## 2. OUR FAILURE — what v176 was doing while dying

### 2.1 We fired almost nothing

From `corpus/build_agg.tsv`, `metric == 'shot'`, band `r0-150` (team 0 = us):

| game | **our shots, whole game** | their shots |
| --- | --- | --- |
| 1 | **0** (no row) | 31 |
| 2 | 27 | 36 |
| 3 | **2** | 37 |
| 4 | **0** (no row) | 34 |
| 5 | 13 | 42 |

**In 2 of 5 games we did not fire a single shot all game.** Our ammo conversions
were 20 / 156 / 32 / 20 / 130 Ti against their 400 / 380 / 384 / 440 / 450.

### 2.2 Where our economy went

Our builds in the first 50 rounds: **28 / 28 / 29 / 40 / 30** — dominated by
conveyors, harvesters and barriers. We spawned 6/5/5/5/5 builder bots. Our Ti
balance in g1 sits at **0–16 from r18 onward** (per-round trace): we were broke
for the entire second half of the game, which is why the ammo column is 20.

### 2.3 The forward plank ran, on schedule, and did not reach

We ran the launcher ferry in 5/5: build launcher → throw our builder 4–6 tiles →
destroy the launcher → repeat. It **worked as designed** — a builder was adjacent
to their core by **r9 / r7 / r8 / r13 / r6**. Then:

| game | our core damage dealt to THEM | delivered by | our builderAttack events (whole game) |
| --- | --- | --- | --- |
| 1 | **0** | — | 3 |
| 2 | 144 | **our forward sentinel @(11,8), built r5** | 0 |
| 3 | **0** | — | 3 |
| 4 | **0** | — | 0 |
| 5 | 234 | **our forward sentinels @(25,8) r29 and @(20,8) r37** | 20 |

**The inserted builder produced 0 core damage in 5/5.** What it did instead was
**barrier-seal their core**: g1 barriers at (13,27) (14,25) (13,26) (15,28)
(14,28) (16,27) (16,26) (15,25); g4 at (24,26) (25,24) (24,25) (26,27); g5 at
(22,4) (21,5) (23,4) (24,5) (24,6) (24,7) (23,7) (22,7) (21,7).

**⭐ THE SEAL IS AIMED AT A BEHAVIOUR THIS OPPONENT DOES NOT HAVE.** Spawn-denial
prices a core that keeps spawning builders. **not adgato spawns exactly one
builder, at round 0, and never spawns again (5/5).** By the time our seal is up
(r8–r36) there is nothing left to deny. INFERENCE: against this opponent the
entire barrier budget and the builder-turns spent placing it are dead weight.

Where our two damage-dealing forward sentinels did exist (g2 r5, g5 r29/r37) they
worked at the expected rate — 1 sentinel = 9 dmg/round, so 500 HP needs ~56
rounds of uninterrupted fire and our core died first, at r59 and r66. **We lost
both games by having ONE forward sentinel where they had FOUR.**

---

## 3. STABILITY — is the rush open-loop? YES

⭐ **The premise said these replays were not on disk, and they were not — but
`fcode match replay <ID> --game N` is READ-ONLY (`docs/fcode-cli.md:130,368`) and
downloads ANY match, including matches we are not in.** Pulled to scratchpad at
2026-08-21T13:02Z (`date -u`), decoded with the same `replay_autopsy.py`.
**No matches were fired.** Files live in the session scratchpad, not in
`replay_archive/` — nothing was added to the corpus.

Downloaded and decoded: `7584fe46` (vs **O(1) v38**, adgato 5-0) games 1–3;
`96e07f65` (vs **team lazy v253**, adgato 5-0) games 1–3; `1120a4f0`
(vs **Focalground v32**, adgato **lost** 2-3) games 1–2. In these three matches
adgato is **team A** (in `7584fe46`/`96e07f65`) or **team B** (`1120a4f0`) —
`league_matches.teamAName` gives the seat.

| match | opponent | game | adgato builder spawns | adgato total builds ≤r50 | sentinel rounds | adgato Ti→ammo | victim core dead |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7584fe46 | O(1) v38 | 1 | **1** (r0) | **5** | r43,44,46,48 | **410** | r60 |
| 7584fe46 | O(1) v38 | 2 | **1** (r0) | **5** | r35,36,37,39 | **410** | r52 |
| 96e07f65 | team lazy v253 | 1 | **1** (r0) | **5** | r29,30,31,33 | — | r46 |
| 1120a4f0 | Focalground v32 | 1 | **1** (r0) | **5** | r31,32,34,35 | 670 | **adgato's core dies r153** |
| 1120a4f0 | Focalground v32 | 2 | **1** (r0) | **5** | r32,33,34,36 | 420 | r53 |

**Identical in 5 of 5 non-us games: one builder at r0, four sentinels, nothing
else. 100% of all core damage in all of them is `sentinel`-attributed (every
ledger printed `MATCH`).**

### ⭐ THE OPEN-LOOP CONTROL — same map, different victim, same clock

`96e07f65` game 1 is **the same map as our game 1**: 30x30, cores (14,2) and
(14,26). Against **team lazy** they planted at **r29, r30, r31, r33**; against
**us** at **r30, r31, r33, r34**. **One round apart, against bots that opened
completely differently** (team lazy built 31 things in 50 rounds and raced its own
sentinels in at r26/r33; we ran a launcher ferry and a barrier seal).

⇒ **The rush is OPEN-LOOP. It does not read the victim's opening.** Its clock is
set by map geometry (walk time) and nothing else. INFERENCE, from this control
plus the 5/5 identical build list: this is a fixed script, not adaptive play.

### What Focalground did — the only measured counter on the board

`1120a4f0` game 1: Focalground **took the full rush and won at r153.** The
ledger, all from the same decoder:

- **Sentinel damage taken: 1,116. Healed: +1,100. Core finished at 484/500.**
  `builderHeal` events **A=275** (ours in the same situation: 14–62).
  275 heals × 4 HP = 1,100 exactly.
- **They reinforced:** 8 builder spawns — 4 at r0–r3 and **4 more at r36–r39**,
  i.e. immediately after the first sentinel landed at r31.
- **They killed the nest with a HOME GUNNER.** Gunner built **r43 @(6,5)**;
  adgato's sentinels sat at (6,2) (6,4) (5,2) (4,3) — d² from the gunner = 9, 1,
  10, 8, **all ≤ 13 = gunner attack r²**. Sentinel deaths **r50, r63, r124, r135**.
  Second gunner r80 @(6,1). They converted 384 Ti to ammo.
- Then they built their own sentinels at r126 beside adgato's core and killed it
  at r153.

Game 2 they did none of that (52 heals, **0 Ti converted to ammo**, no turret)
and died at r53. **Same opponent, same bot, two games: the counter is the
behaviour, not the matchup.**

**THE ARITHMETIC THIS EXPOSES.** A gunner is **7 dmg, reload 1, 4 ammo/shot**; a
sentinel has **40 HP** ⇒ **6 shots = 6 rounds = 24 ammo per sentinel, 96 ammo for
the nest of four**, plus one gunner (20 base Ti). Against a rush that spends
~400 Ti on ammo and ~180 on turrets, **the counter costs under a quarter of what
the attack costs.** The catch is range: gunner r²=13 means the gunner must sit
within ~3 tiles of the nest, and the nest is 3–6 tiles from the core.

---

## 4. COUNTER SURFACE — what `bots/_v542wave` (live v177) already has, and what is switched off

All line numbers below were opened or grepped in this session against
`bots/_v542wave/` at git `07735243f85701e45835ab1ce214a2f4fe59b5a0`.

### 4.1 Detection — PRESENT, and it fires in time

`main.py:441-468` (core's threat latch) and `main.py:1420-1437` (the same test on
the builder path):

```
if (et in CORE_THREAT_TYPES and d <= 64) or (
    et == EntityType.BUILDER_BOT and d <= 16
):
```
with `CORE_THREAT_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))`
(`main.py:60`) and a **50-round latch** at `main.py:463-468`.

Measured against the five games (d² from the enemy entity to our core's own
`get_position()`, i.e. the NW corner, which is what the code compares):

| game | BUILDER_BOT trigger (d²≤16) | TURRET trigger (d²≤64) | first sentinel |
| --- | --- | --- | --- |
| 1 | **r21** | r30 | r30 |
| 2 | **r11** | r40 | r40 |
| 3 | **r23** | r35 | r35 |
| 4 | **r38** | r43 | r43 |
| 5 | **never** | r43 | r43 |

⇒ `SLOT_UNDER` was latched **before the first sentinel existed in 4 of 5 games**
(9, 29, 12 and 5 rounds of warning), and in game 5 it latched **on the sentinel
itself, r43, with the core dying r66 — 23 rounds later.**
**Detection is NOT the failure.** ⚠ One real gap: their bot ends up at d² = 25 /
13 / 9 / 29 / 25 from our core corner, so **in 3 of 5 games it PARKS outside the
`d <= 16` builder radius** — the early trigger came from its transit, and the
50-round latch is what carried it. A rush that walked wide would not trigger at
all until a sentinel appeared.

### 4.2 Counterbattery turret — PRESENT, correctly shaped, and it never bought one

`main.py:1882-1934 _try_counterbattery`. It is well-designed for exactly this:
- gate `dsq_core(threat, self.core) > HUNT_BAND_DSQ` → `return False`
  (`main.py:1887`), `HUNT_BAND_DSQ = 41` (`doctrine.py:163`). Their nest sits at
  d² 2–16 from our core footprint — **inside the band.**
- it tries **SENTINEL first, then GUNNER** (`main.py:1898-1901`) and only accepts
  a tile+facing where `can_fire_from(bp, facing, turret_type, threat)` is already
  true (`main.py:1918`) — i.e. it never builds a turret that cannot see the
  threat. This is the right shape.

**Why it produced zero home turrets in 5/5:**
1. **It runs on ONE unit.** `_defend` (`main.py:2020-2028`) is the only caller,
   and only `role == "defend"` reaches it; `LOKI_DEFEND_SEAT = 4`
   (`doctrine.py:1210`), assigned at `main.py:1341-1342` — **one bot in the whole
   army.** It also returns after **one** build (`main.py:1933`).
2. **We were broke.** `main.py:1903`: `if ct.get_global_resources() < cost:
   continue`, and `_cb_over_heal` additionally demands
   `sentinel_cost + SIEGE_HEAL_RESERVE_TI` with `SIEGE_HEAL_RESERVE_TI = 16`
   (`main.py:1878`, `doctrine.py:437`). Our global titanium over r20–50, measured
   per round off `updatePlayers`:

   | game | min | median | max |
   | --- | --- | --- | --- |
   | 1 | **0** | **6** | **16** |
   | 2 | 4 | 22 | 91 |
   | 3 | 25 | 64 | 88 |
   | 4 | **0** | 13 | 84 |
   | 5 | 7 | 59 | 122 |

   In game 1 our bank never exceeded **16 Ti** across the entire window — **a
   sentinel at our live scale is unaffordable at every single round of it.**
   INFERENCE: the counterbattery is not missing, it is **unfunded**, because the
   opening spends the 500 Ti on ferry launchers, conveyors, harvesters and the
   barrier seal.

**What we DID build at home, and why it was not enough:** a home **gunner** in
2 of 5 games — g2 r13 @(5,9) and g3 r19 @(4,4). In g2 three of their four
sentinels were within the gunner's r²=13 and **we killed exactly one, at r59 —
the same round our core died.** In g3 only one of four was in range (d²=13,
exactly at the limit) and **we fired 2 shots all game.**

### 4.3 Builder melee on the nest — SILENCED BY FLAG

- `LOKI_QUIET_ON = True` (`doctrine.py:1687`), commented in the file itself as
  *"no builder melee: no core peck, no siphon hit, no counterbattery"*. It gates
  the counterbattery melee at `main.py:1857-1861`:
  `if LOKI_QUIET_ON: return False  # QUIET: counterbattery melee silenced`.
- The one path built to **pierce** quiet for enemy turrets near our core —
  `_door_turret_turn` (`main.py:1708+`, "⭐ THIS DELIBERATELY PIERCES
  LOKI_QUIET_ON", `main.py:1711`), with `FS_DOOR_DSQ = 40` (`doctrine.py:2654`),
  which would cover their nest — **is switched off**:
  ```
  main.py:1729-1730:  if LOKI_FS_V515 and FS_V515_DOOR_OFF:
                          return False
  ```
  `LOKI_FS_V515 = True` (`doctrine.py:3113`), `FS_V515_DOOR_OFF = True`
  (`doctrine.py:3132`). The doctrine note at `doctrine.py:3115-3131` records why
  and **flags its own limitation**: both measurements that turned it off were
  *"played against `_v488beltbreak2`, our own bot"*, and the note says in terms
  that *"the field plants door turrets and we should ignore them is NOT what was
  measured."* **not adgato v25 is exactly the field case that note excluded.**

⇒ **Against a home nest, our builders can neither shoot it nor peck it.**

### 4.4 Healing — PRESENT, arithmetically insufficient

`eco.py:2585-2601`: expanders converge on heal seats when `SLOT_UNDER` and
`_core_shelled`, from `role_n >= min_seat` with `min_seat = 2` (or 1 under
`T4_CONVERGE_SEAT1_ON` past `T4_SEAT1_MIN_DMG`). `main.py:2040-2051`
(`T4_SEAT_FIRST_ON = True`, `doctrine.py:2004`) makes the defender prefer a heal
seat over chasing once the core is bleeding.

**The file already states the problem** (`eco.py:2589-2592`): *"seat 0 raids,
seats 1-3 expand but seat 3 defects to the raid… seat 4 defends — so the
convergence is a one-healer plan against a two-turret siege."*
**not adgato brings FOUR sentinels = 36 HP/round.** One heal = +4 HP for 1 Ti;
**nine simultaneous healers are needed to break even, and we field at most three.**
Measured `builderHeal` on our side: 14 / 33 / 36 / 25 / 62 events per game against
Focalground's **275**.

### 4.5 The Loki-native answer we cannot reach — LAUNCHER KIDNAP

Their **entire game is one builder bot**. `can_launch` has no team check, pickup
d² ≤ 2, throw 1 ≤ d² ≤ 26 (CLAUDE.md, engine-read). A home launcher could pick up
their lone builder as it arrives and throw it 5 tiles back, repeatedly — resetting
5+ rounds of walk each time, for **0 ammo**, against a bot that has no second body.

**We cannot: `LAUNCHER_MIN_RND = 160` (`doctrine.py:1735`), enforced at
`main.py:1956-1957`:**
```
if ct.get_current_round() < LAUNCHER_MIN_RND:
    return False
```
**Our core dies at r47–r67. The home launcher is 93–113 rounds too late.**
And the docstring immediately under that gate (`main.py:1958-1960`) says the
launcher is *"bought as home defence first and as the raid ferry second"*, while
the deferral comment at `main.py:1952-1953` names the cost it accepted:
*"deferring also delays the ferry, and early exile is our cheapest home defence."*
**This rush is the case that bill comes due on.** (Note: we DO build ferry
launchers at r1–r12 — those are the raid chain, built forward and destroyed after
each throw; the gate above is the HOME launcher.)
⚠ Their own bot uses this trick on us: in g2 they built a launcher r38 and threw
**our** builder away from the nest four times (r39/45/51/57); in g3 twice.

### 4.6 Summary table — the five answers we own

| answer | status in `_v542wave` | anchor |
| --- | --- | --- |
| detect the rush | **LIVE, fires in time 4/5** | `main.py:441-468`, `1420-1437` |
| home counterbattery turret | **LIVE but unfunded + one unit only** | `main.py:1882-1934`, `doctrine.py:163,437,1210` |
| builder peck on the nest | **SILENCED** | `doctrine.py:1687`, `main.py:1857-1861` |
| door-turret peck (pierces quiet) | **FLAGGED OFF** | `doctrine.py:3113,3132`, `main.py:1729-1730` |
| home launcher kidnap of their lone bot | **UNREACHABLE before r160** | `doctrine.py:1735`, `main.py:1956-1957` |
| heal convergence | **LIVE, ~3 healers vs 9 needed** | `eco.py:2585-2601`, `main.py:2040-2051` |

---

## 5. LEG DESIGN — should we spend unrated windows on not adgato?

### 5.1 The value gate (run BEFORE any prereg, per the standing rule)

```
.venv/bin/python tools/target_value.py "not adgato"     # 2026-08-21T13:0xZ
TARGET BAND: not adgato, gaps +92..+92, win pays 20.16..20.16, reachable YES
    (our rating 1821, theirs 1913, p99 of 896 observed pairings; a 0-5 costs -11.84)
```
They are the **3rd most valuable admissible target on the board** (`--band`:
O(1) +122/+21.40, The Flotte Experience +105/+20.71, **not adgato +92/+20.16**).
This is not a low-value target; the gate says spend.

### 5.2 What the rated tape does NOT give us free — and it is one thing

We meet them on the ladder anyway, so **more measurement of THEM is not worth a
window.** The mechanism is already closed at n=10 games: §1 and §3 leave nothing
material unanswered about what v25 does.

**The one thing only unrated buys is a PINNED, REPEATABLE v25 fixture.**
`fcode match unrated <team_id> [--match SOURCE_MATCH_ID]` plays *"the opponent's
submission from that past match"* (`docs/fcode-cli.md:330-340`, quoting
`docs/reference/official-docs.md:1853`). **not adgato shipped v23 → v24 → v25
inside six hours today** (`league_matches.tsv`: v23 last seen 09:52Z, v24 at
10:12/10:32Z, v25 from 10:52Z). **v25 is perishable.** Once they ship v26 the
rated tape can no longer answer "did our change beat the rush", because the rush
will have moved. A pinned unrated leg against
`--match e0e72d55-c9cb-4213-8f5f-f1855cc66c2b` freezes it.

Per the standing design rule (**pin treatment legs, never pin calibration
panels**), this is a treatment leg, so pinning is mandatory.

Their team id, for the record: **`fb0e7053-f8f3-4cc8-a38f-1856a518c7d2`**. Read
off `league_matches.tsv` row `e0e72d55…`, where `teamBName = not adgato` and
`teamBId = fb0e7053…` (`teamAId = 379a5d80…` = OpenSverige). Stable across all
23 rows in which they appear.

### 5.3 What the leg should MEASURE — mechanism, not win rate

The rated tape gives win/loss free. What it does not give free is whether a
treatment **neutralises the nest**, and that is directly readable off a replay
with the decoder already validated on this exact fixture:

- **PRIMARY (mechanism): enemy home sentinels alive at r70**, where "home" =
  d² ≤ 41 from our core (the `HUNT_BAND_DSQ` band). **Control value, measured:
  4 / 4 / 4 / 4 / 4 in 5 of 5 games.** Any treatment that does not move this
  number has not engaged the mechanism, whatever it does to the score.
- **SECONDARY: our core HP at r70.** Control: **dead in 5/5** (r47/56/59/62/66).
- **SECONDARY: rounds from first enemy home sentinel to the SECOND one dying.**
  Control: **never (5/5)**; Focalground's winning game read **r31 → r63 = 32
  rounds** and that sufficed.
- **INSTRUMENT NOTE:** all three come from `tools/corpus/replay_autopsy.py`, whose
  self-check (attributed damage == summed `UpdateHp`) printed `MATCH` on 20 of 20
  core ledgers in this study. It has been driven to the other verdict here in the
  sense that it distinguished sentinel-only (adgato, 10/10 games) from
  builder-mixed (`builderAttack B=20` in `7584fe46` g1) — it is not a constant column.

**GUARD, non-negotiable:** every candidate below is DEFENSIVE, so
`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression` binds. The leg must carry
the timely-kill rate (share of ALL games ending in a core-kill by r300) on the
calibration panel — **unpinned**, because a panel measures relevance — against
control, and that claim must be **restated as an exclusion** before any DEFF
correction is applied (a "no significant rise" null is the exact class the
direction clause warns about).

### 5.4 CANDIDATE QUEUE ROWS (drafted — QUEUE.md NOT edited)

---
**CAND-A · Arm the home-defence reserve when the threat latch fires**
- **CHANGE:** once `SLOT_UNDER` is latched by a threat inside `HUNT_BAND_DSQ`
  before some round floor, refuse discretionary spends (barrier seal, further
  conveyor extension, additional ferry launchers) below
  `get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI`. No new mechanism: it unblocks
  the counterbattery that already exists and is already correctly shaped.
- **MECHANISM METRIC:** enemy home sentinels alive at r70 (control 4/4/4/4/4);
  our global Ti at the round `_try_counterbattery` first returns False on the
  cost gate (control: bank 0–16 Ti through r20–50 in game 1).
- **FIXTURE:** pinned unrated vs not adgato `--match e0e72d55…`, ≥4 windows
  pooled (a 25-game window is a dose probe, not a currency read); plus the
  unpinned calibration panel for the r300 guard.
- **WHY NOW:** this is the **measured binding constraint**. §4.2 shows the
  counterbattery is not missing — it is unfunded. Our bank never exceeded
  **16 Ti** across r20–50 in game 1, and `main.py:1903` refuses on exactly that.
- **GREP (incumbent `bots/_v542wave`):** checked `_try_counterbattery`
  (`main.py:1882-1934`) — present, tries SENTINEL then GUNNER (`:1898-1901`),
  gated `dsq_core(threat, core) > HUNT_BAND_DSQ` (`:1887`, `doctrine.py:163` = 41)
  and `get_global_resources() < cost` (`:1903`); `_cb_over_heal`
  (`main.py:1864-1880`) additionally requires `sentinel_cost +
  SIEGE_HEAL_RESERVE_TI` (`doctrine.py:437` = 16). **FOUND: no reserve anywhere
  that protects a home-turret purchase** — `_eco_spendable` guards the LAUNCHER
  (`main.py:1984`) and `SIEGE_HEAL_RESERVE_TI` guards the SIEGE, neither guards
  counterbattery. Caller is `_defend` only (`main.py:2025`), one seat
  (`LOKI_DEFEND_SEAT = 4`, `doctrine.py:1210`; assigned `main.py:1341-1342`).

---
**CAND-B · Release the home launcher on a latched home threat**
- **CHANGE:** `LAUNCHER_MIN_RND` becomes conditional — bypassed when `SLOT_UNDER`
  is latched by a BUILDER_BOT threat inside `HUNT_BAND_DSQ`. The launcher then
  kidnaps their lone builder (no team check, pickup d²≤2, throw 1≤d²≤26, 0 ammo)
  and throws it back down the map, repeatedly.
- **MECHANISM METRIC:** round of the first enemy home sentinel (control r30/40/35/43/43)
  and total enemy home sentinels ever built by r70 (control 4/4/4/4/4). A single
  successful throw should push the first number by ≥5 rounds.
- **FIXTURE:** same pinned leg as CAND-A; can share windows if the arms are
  separated (they touch different gates).
- **WHY NOW:** their **entire game is ONE builder bot, 5/5 ours and 5/5 non-us**.
  It is a single point of failure and displacing it costs 0 ammo. It is also the
  house plank — and **they used it on us first** (g2: 4 kidnaps of our builder;
  g3: 2).
- **GREP (incumbent):** `LAUNCHER_MIN_RND = 160` (`doctrine.py:1735`), enforced
  unconditionally at `main.py:1956-1957` before any threat test. **FOUND: no
  bypass of any kind.** Our core dies r47–67, so the home launcher is 93–113
  rounds late in 5/5. The deferral comment (`main.py:1952-1953`) already names
  the accepted cost: *"early exile is our cheapest home defence."*
  ⚠ **CAND-B is only reachable if CAND-A (or equivalent) funds it** — launcher
  base 20 Ti at live scale is also unaffordable at game 1's 0–16 Ti bank. Do not
  fire CAND-B alone and read a null as "kidnap does not work".

---
**CAND-C · Re-open the door-turret peck for SENTINEL threats only**
- **CHANGE:** `FS_V515_DOOR_OFF` becomes type-conditional rather than global —
  the peck stays off for gunners/launchers and turns on for a SENTINEL inside
  `FS_DOOR_DSQ`.
- **MECHANISM METRIC:** enemy home sentinel deaths by r70 (control: 1 in 5 games,
  and that one at r59 = the round our core died).
- **FIXTURE:** same pinned leg; this is a flag flip so it is nearly free to arm.
- **WHY NOW:** the doctrine note that turned it off **states its own limitation
  in the file**: both measurements were *"played against `_v488beltbreak2`, our
  own bot"*, and *"the field plants door turrets and we should ignore them is
  NOT what was measured"* (`doctrine.py:3115-3131`). **not adgato v25 is exactly
  the excluded case.**
- **GREP (incumbent):** `LOKI_FS_V515 = True` (`doctrine.py:3113`),
  `FS_V515_DOOR_OFF = True` (`doctrine.py:3132`), enforced `main.py:1729-1730`.
  `FS_DOOR_DSQ = 40` (`doctrine.py:2654`) **would cover their nest** (measured d²
  2–16 from our footprint). `_door_turret_turn` explicitly pierces
  `LOKI_QUIET_ON` (`main.py:1711`). **FOUND: the code is intact and one flag away.**
  ⚠ **Peck arithmetic is poor on its own:** 2 dmg/peck, sentinel 40 HP = 20 pecks
  per sentinel, 80 bot-rounds for the nest, against `FS_DOOR_MAX_RNDS = 40`
  (`doctrine.py:2659`). Expect this to *delay*, not *break*, the rush. Rank it
  below A and B.

---
**CAND-D · Widen the builder-bot threat radius**
- **CHANGE:** `main.py:449-451` / `1432-1434` use `d <= 16` for BUILDER_BOT;
  raise to `HUNT_BAND_DSQ` (41) so a bot that parks at nest range latches.
- **MECHANISM METRIC:** round `SLOT_UNDER` first latches (control, measured:
  r21 / r11 / r23 / r38 / **never**).
- **FIXTURE:** same leg, as a rider — it is one constant.
- **WHY NOW:** in **3 of 5 games their bot parks OUTSIDE d²≤16** (final d² to our
  core corner 25 / 13 / 9 / 29 / 25) and in game 5 the builder trigger **never
  fired** — the latch came from the sentinel itself at r43.
- **GREP (incumbent):** the two call sites above are the only BUILDER_BOT threat
  tests; `CORE_THREAT_TYPES` (`main.py:60`) covers GUNNER/SENTINEL at d≤64.
  **FOUND: no wider builder test exists anywhere in the tree.**
  ⚠ **Lowest priority.** Detection already fired before the first sentinel in
  4/5; widening it buys warning we currently cannot spend. **Do not fire this
  alone** — a null would be uninformative.

### 5.5 RECOMMENDATION

**Spend windows — but on ONE pinned leg with CAND-A as the treatment (optionally
A+B as a two-arm), not on more observation.** Reasons, in order:
1. The mechanism is closed at n=10; nothing more to learn by watching.
2. v25 is perishable (three versions in six hours) and **only unrated can pin it**.
3. The value gate says +20.16 for a 5-0 and they are p99-reachable — this is a
   top-3 target, not a curiosity.
4. **CAND-A is aimed at the measured binding constraint, not at a guess.**

**Do NOT fire CAND-C or CAND-D as standalone arms.** C is arithmetically weak
(80 bot-rounds against a 40-round cap) and D buys warning we cannot spend; both
would produce nulls that close nothing.

---

## 6. CAVEATS — carry these with every number above

1. **n is small and clustered.** Our side: **5 games = ONE match = one opponent,
   one version, one 20-minute ladder slot.** The MATCH and OPPONENT clusters are
   both live and un-averaged, so **every "5/5" here is descriptive, not
   inferential** — do not attach a confidence interval to it. Non-us side: 5 games
   from **3 matches**, 2 of which come from the one match adgato LOST.
2. **The v25 era is ~2 hours old** (10:52–12:41Z on 2026-08-21) and the
   `league_matches.tsv` snapshot ends at 12:41Z. Anything after that is unknown.
   **v25 may already be superseded by the time this is read.**
3. **The Focalground counter is n=1 GAME.** Their own game 2 shows the same bot
   losing to the same rush in 53 rounds. Treat "heal + home gunner + reinforce"
   as a **hypothesis with one worked example**, not as a validated counter.
4. **The r0 ammo=120 fingerprint is an ANALYSIS-time discriminator only.**
   `get_global_ammo()` is own-team; we cannot sense it in-game.
5. **Seat attribution:** in match `e0e72d55` we are team A per
   `league_matches.teamAName` and `ladder_games.won=0 / winner_seat=b`. This is
   NOT circular with `join.tsv`/`meta_join.us_side` here because the behavioural
   fingerprint is independent and unambiguous: **team A runs the launcher ferry
   and the barrier seal (our signature), team B builds five things.** TRAP 7
   (`corpus-howto.md:167`) does not bite this study.
6. **Downloaded replays live in the session scratchpad and die with it.** They are
   NOT in `replay_archive/` and NOT in the corpus. Re-pull with
   `fcode match replay <ID> --game N` (read-only) if needed.
7. **`build_agg.tsv` shot counts** are read with `metric == 'shot'` per
   `corpus-howto.md:134-145` (trap 5 — `econ.tsv.shots` is dead). Games 1 and 4
   have **no row**, which this study reads as zero shots; that is an absence, and
   an absence in an aggregate table is weaker evidence than a measured zero.
   It is corroborated independently by the ammo column (20 Ti converted) and by
   there being no home turret in those games.
8. **No matches were fired. Nothing was committed. `QUEUE.md`, `bots/` and
   `tools/` were not touched.**

**STATUS: COMPLETE.** Study run 2026-08-21T12:57Z–13:0xZ (`date -u`), tree at
git `07735243f85701e45835ab1ce214a2f4fe59b5a0`.
