# Kings College Munich classification — 2026-08-07

> **STALENESS FLAG (s14, ~21:15): the entire CAD family moved versions
> tonight** — CAD v107→v115, Lunds v42→v43, KCM 7→1, Powerpuff 26→18.
> Historical analysis in this doc (era-internal reads, identity matches
> against v107-era replays) stands; every FORWARD-LOOKING v107-era claim
> (exact opening/throw constants, probe-fidelity assumptions, calibration
> values) is SUSPECT until re-frozen against the new versions per the
> standing constants rule.

**Version tags (rule 2):** target = Kings College Munich (KCM), team id
`dfa9be96`. Two version labels appear in today's corpus: **v7** (2 matches,
15:36Z, both unrated, both 0-5 losses) and **v1** (3 matches, 16:27-17:47Z —
the two ladder matches against us plus one unrated). **v1 is live** and is what
beat us. Our live slot at read time: **v68 chokewall**; the two matches against
us were played by **v67 wave_ghost** (b3656fe7) and **v68 chokewall**
(9a32a859). Research arm, session 13. 25 games decoded from the local archive,
no downloads.

**vs-us confound, stated explicitly:** 10 of the 25 games are against our own
bots, so their behaviour there may be shaped by ours. The classification below
is anchored on the 15 games against Pantheon v36, team lazy v94 and
Powered by SmartFridge v33; the vs-us games are used only for §3 (loss modes)
and to confirm that the opening constants are opponent-independent — which they
are, byte-for-byte.

**Parser note:** all turret counts here are **deduped by entity id**
(`placeEntity` re-emission on gunner rotation, per docs/tooling.md). Rotations
are reported separately. Cross-validated against `tools/replay_census.py -v` on
b3656fe7 g1 (6 unique gunners + 13 rotations = the 19 the naive count reports;
end-of-game counts and `core_deliv*10 == titaniumCollected` both agree).

---

## Headline: KCM is a CtrlAltDefeat-family launcher-ferry bot

The opening is **the same script as CtrlAltDefeat**, at an earlier rung.
Verified three independent ways against `9d2b38bb` (CAD v107 vs our v68) and
the constants recorded in `docs/research/cad-ferry-premortem-2026-08-07.md`:

| Constant | KCM (25 games, v1 and v7) | CAD v107 (5 games) |
| --- | --- | --- |
| Ammo conversion r0/r1/r2 | 8 / 8 / 8 | 8 / 8 / 8 |
| Launcher built | r1, on a Core-adjacent tile | r1, on a Core-adjacent tile |
| Launcher destroyed | **r6, every game** | **r6, every game** |
| Own builders thrown | r2, r3, r4 (±1), 2-3 of them | r2-r4 |
| 25×25 (5,5)/(18,18) throw table | (11,11), (11,11), (10,5) | (13,13), (13,13), (14,19) *in the mirrored seat* → rotates to (11,11), (11,11), (10,5) |
| 18×18 throw table | (8,9), (8,9) [core (2,14)] / (9,8), (9,8) [core (14,2)] | (9,8), (9,8), (12,0) |

The 25×25 opening table matches **exactly** under the map's 180° rotation, and
the launcher tile matches exactly too ((17,16) for a core at (18,18) rotates to
(7,8), which is KCM's launcher tile for a core at (5,5)). This is the same
opening table, not a convergent idea.

**Measured deltas KCM-v1 vs CAD-v107:** (a) KCM's 4th ammo conversion is a
fixed **24**; CAD's is a variable lump (89/146/24/141/187 = "convert the
surplus"). (b) KCM never builds a second launcher in any of 25 games; CAD
likewise built exactly 1 per game in this corpus. (c) KCM's forward turret mix
is gunner-dominant and it **rotates gunners heavily** (0-22 rotations/game,
10 Ti each); CAD leans more on sentinels.

---

## 1. Match / meta table

| Match | Time (Z) | Trigger | KCM ver | Opponent | Score (KCM) | Maps | Wall clock |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `4a36151e` | 15:36:16 | unrated | **7** | team lazy v94 | **0-5** | 18×18, 26×26, 28×20, 16×16, 28×20 | 1m21s |
| `484095e3` | 15:36:40 | unrated | **7** | Pantheon v36 | **0-5** | 18×18, 26×26, 28×20, 16×16, 28×20 | 1m39s |
| `b3656fe7` | 16:26:58 | ladder | **1** | **OpenSverige v67** | **5-0** | 24×24, 16×16, 10×10, 20×26, 26×26 | 4m15s |
| `9e41db1a` | 16:28:01 | unrated | **1** | Powered by SmartFridge v33 | **0-5** | 20×26, 26×26, 28×20, 18×18, 10×10 | 59s |
| `9a32a859` | 17:47:00 | ladder | **1** | **OpenSverige v68** | **4-1** | 25×25, 28×20, 18×18, 24×24, 26×26 | 4m17s |

**Version stability verdict:** the label went **7 → 1** between 15:36Z and
16:27Z, i.e. they *rolled back* after two 0-5 unrated results. Read as eras,
the two eras are **behaviourally indistinguishable in the opening**: identical
launcher tile, identical throw rounds, identical throw targets on shared maps,
identical 8/8/8→24 ammo ladder, identical r6 launcher self-destroy. The only
visible difference is late-game volume (v1 games reach 11-12 harvesters and
40-49 conveyors when unpressured; the v7 games were all short losses, so this
is confounded with pressure and should not be called a version change). **Treat
KCM as one bot, live version v1.**

**Total record across all 5 matches: 9 wins, 16 losses.** Every single one of
those 9 wins is against OpenSverige.

---

## 2. Mechanism

### 2.1 Opening build order (invariant across all 5 opponents, both versions)

```
r0   core spawns builder #3 on the ring tile toward the enemy;  convert_ammo(8)
r1   core spawns builder #5;  builder #3 builds a LAUNCHER on the tile
     adjacent to it (Core-adjacent, enemy-facing) and stands in its pickup ring
     convert_ammo(8)
r2   the launcher THROWS builder #3 ~5 tiles toward the enemy   convert_ammo(8)
r3   the launcher throws builder #5 to (usually) the same tile
r4   the launcher throws builder #11 — a third throw, sometimes backward/lateral
r5   thrown builders start walking / start planting
r6   the LAUNCHER IS DESTROYED by its own team.  25/25 games. No exceptions.
r5-r30  first turret goes up; convert_ammo(24) fires on that round
```

Throw geometry: every observed throw is at or near the launcher's max range
(target d² to launcher = 25 or 26 of a max 26). On maps with ~12-tile core
separation the first two throws land the raider **3-5 tiles from the enemy core**
(d²_enemycore 17-29) at round 2. On 24×24+ maps they only reach mid-map
(d²_enemycore 98-288) and the raider then walks.

**Map-size branch:** on **10×10** maps there is *no launcher at all*. Instead
`convert_ammo(48)` at r0 and gunners planted point-blank on the enemy core from
**r1/r2** (d²_enemycore = 5). Seen in b3656fe7 g3 and 9e41db1a g5, the only two
10×10 maps in the corpus.

### 2.2 Builder counts

4-7 builders in short games; **12-24** in long ones (they keep replacing losses
all game — 24 builders in three separate 445-1000 round games). Not a fixed-4
bot like the Orizon family.

### 2.3 Turret mix and placement geometry (deduped by id)

Per game, medians across the 25 games: **6 gunners, 1 sentinel, 1 launcher,
0 splitters, 0-1 barriers**. Gunner-dominant. Ranges: gunners 2-17, sentinels
0-5, barriers 0-4, splitters **0 in every game**.

Two distinct placement modes, both present:

- **Forward battery (the win condition).** Gunners/sentinels planted at
  d²_enemycore **2-32**. First forward turret round is bimodal by core
  separation: r1-r5 on 10×10/28×20 maps, r16-r45 on 16×16-26×26 maps.
- **Diagonal sentinel finisher.** On big maps the killing blow is a line of
  sentinels planted on the **exact diagonal ray onto a core footprint tile at
  d²=32** (max sentinel range). b3656fe7 g5: sentinels at (16,15) SE,
  (17,16) SE, (16,16) SE, (17,17) SE against a core at (19,19) — every one a
  clean SE ray onto (18,18)/(19,18). First core damage r103, core dead r156.
  b3656fe7 g1: sentinel (14,14) SE onto core (18,18) at r224 → first core
  damage **r225**, dead r274.
- **Home defence is purely reactive and late.** In 20 of 25 games KCM's first
  turret within d²≤36 of its *own* core is built **after** the first enemy
  turret arrives there (vs SmartFridge g3: enemy gunner r8, KCM home turret
  r70). There is no pre-built home ring, no barrier wall, and the only launcher
  is deleted at r6.

**Gunner rotations:** 0-22 per game (10 Ti + 1 cooldown each). They re-aim
rather than only adding new guns — unlike the Orizon family, which never
rotates.

### 2.4 Ammunition

The tightest signature on the board:

```
r0: 8    r1: 8    r2: 8    r<first turret>: 24    then a drip of 2-48
```

`8, 8, 8, …, 24` opens **25/25 games** except the two 10×10 maps, which open
`48` at r0. Total converted scales with game length and pressure: 107-532 in
short games, 946-3486 in long ones (346 conversion calls in b3656fe7 g2).
They convert **continuously, nearly every turn they can**, and this is the
single biggest functional difference from us (see §3).

### 2.5 Economy

Small footprint, **immaculately wired**. Harvesters 0-12, conveyors 0-49,
splitters 0.

| Metric (KCM side, vs-us games) | KCM | our v67/v68 |
| --- | --- | --- |
| relay tiles wired to core | 31/31, 5/6, 19/19, 18/22, 23/23, 35/40, 32/36, 4/4, 40/43, 25/28 (**86-100%**) | 28/39, 66/94, 5/30, 43/46, 152/177, 24/27, 60/77, 68/84, 76/100 (**17-93%**) |
| chain facing-correct vs connected | **identical in 10/10 games** | diverges badly (5/5 connected but 1/5 facing-correct; 6/8 vs 2/8; 4/7 vs 1/7) |
| Ti collected, 9a32a859 g1 | 7030 off 40 relay tiles | 6120 off **177** relay tiles |

KCM lays a fifth of the road we do and delivers more titanium. Their harvester
ramp is slower than a dedicated econ bot (first harvester r5-r11) but never
orphaned. Against real pressure the economy collapses entirely — vs Pantheon
their chain_dir is **0/3, 3/4, 0/3, 0/4, 0/3** and they banked 0 titanium in
2 of 5 games.

### 2.6 Timing curves (all 25 games)

- First turret: **r1-r30** (median r14).
- First forward turret (d²_enemycore ≤ 36): r1-r5 on close maps, r12-r45 typical,
  never at all in 3 games (all losses).
- First damage on the enemy core: r2-r225 (median r16).
- Kill round when they win: **r124, r157, r227, r275, r445, r455, r663** —
  they are a **slow grind**, not a rush. Median time-to-kill ≈ 275 rounds.
- Kill round when they lose: opponents killed *them* at **r66, r67, r73, r76,
  r77, r82, r91, r99, r156, r192, r209, r233, r256, r259, r324** — median
  **r156**, i.e. roughly twice as fast as KCM kills.

### 2.7 Invariant vs adaptive

**Invariant (their identity — reproduces against all 5 opponents):** the r1
launcher / r2-r4 triple throw / r6 self-destroy; the 8/8/8→24 ammo ladder; the
map-keyed throw table; zero splitters; the diagonal max-range sentinel
finisher; no proactive home defence.

**Adaptive:** which turret type goes forward (gunner on close maps, sentinel on
open ones); home-turret construction (reactive, triggered by an enemy turret
arriving near their core); builder replacement rate; gunner rotation volume.

**No timeouts and no stdout in any of the 25 games** — 0 TLE, 0 bot output.
It is a clean, cheap script.

---

## 3. Why they beat us — the 10 games

### 3.1 The two structural reasons

**(a) They out-shoot us 3-20×.** Shots fired per game, KCM vs us:

| | g1 | g2 | g3 | g4 | g5 |
| --- | --- | --- | --- | --- | --- |
| b3656fe7 KCM / v67 | 171 / **7** | 454 / 79 | 127 / 107 | 111 / **10** | 93 / **13** |
| 9a32a859 KCM / v68 | 401 / 96 | 63 / 18 | 278 / 76 | 137 / 43 | 253 / **5** |

Our snipe bot fires 5-13 shots in four of the ten games. KCM converts ammo
every turn it can; we do not.

**(b) The counter-gunner answer to a forward sentinel — measured.** Our forward
sentinel goes up; KCM plants a **gunner 1-3 tiles from it within 0-5 rounds**
and plinks it dead. Every case in the corpus:

| Game | our sentinel | KCM answer | died | life |
| --- | --- | --- | --- | --- |
| b3656fe7 g1 | #43 r25 (8,8) | gunner #46 **r26** @(7,7), d²=2 | r38 | 13 |
| b3656fe7 g2 | #41 r17 (5,5) | gunner #48 r19 @(5,2), d²=9 | r32 | 15 |
| b3656fe7 g5 | #54 r22 (9,9) | gunner #67 r27 @(7,7), d²=8 | r39 | 17 |
| 9a32a859 g1 | #124 r53 (10,10) | gunner #177 r81 @(9,11), d²=2 (+4 builder-attacks from r75) | r86 | 33 |
| 9a32a859 g3 | #45 r20 (3,9) | gunner #48 r22 @(3,12), d²=9 | r36 | 16 |
| 9a32a859 g4 | #49 r24 (8,8) | gunner #50 **r24** @(6,6), d²=8 | r36 | 12 |
| 9a32a859 g5 | #56 r26 (9,10) | gunner #53 r25 @(10,8), d²=5 | r36 | 10 |

Median forward-sentinel lifetime: **15 rounds**, in which it lands 3-9 shots =
**54-162 damage on a 500 HP core**. A single wave-ghost sentinel is
arithmetically incapable of killing a core; the counter-gunner is exactly
tuned to that (40 HP ÷ 7 dmg = 6 gunner shots at reload 1 = 12 rounds).
**Our forward *gunners* die even faster — 3-7 rounds.**
They never use builder attacks for this; it is turret-on-turret.

### 3.2 Per-game mechanism

**b3656fe7 (our v67 wave_ghost, 0-5):**

1. **g1 24×24, dead r274.** Ferry to (10,10) r2. Our sentinel (8,8) r25 killed
   r38 by their r26 counter-gunner. They then walked a gunner line up the map
   (r106/r122/r123 at d²_ocore 58-89, r156 at 13) and finished with three
   diagonal sentinels r224/r249/r273. First core damage **r225**. Their core
   never dropped below 400. We fired **7 shots all game** (94 Ti converted).
2. **g2 16×16, r1000 tiebreak loss 3670-4930.** Their ferried raider planted a
   **sentinel at (11,14) on r16**, three tiles from our core → 272 shots into
   our core over the game, taking it to 102 HP. Our heal line held (1259 heal
   actions) but lost tiebreak #1 on titanium.
3. **g3 10×10, dead r454.** No launcher; KCM planted gunners point-blank
   (d²_ocore=5) on **r1 and r2** and first-damaged our core on **r2**. Our three
   sentinels (r2/r3/r4) had **no firing line onto their core** — 107 shots fired,
   **0 landed on the core footprint**, their core finished 500/500 — and we
   banked **0 titanium** (no harvesters, no conveyors).
4. **g4 20×26, dead r123.** Ferry landed a raider at (10,14) on **r2**, three
   tiles from our core; gunner at (10,15) on **r3**; first core damage **r4**.
   Their core was never touched (0 shots into it).
5. **g5 26×26, dead r156.** Our sentinel (9,9) r22 killed r39. Our replacement
   gunners at (8,8) lived **3 rounds each**. Four diagonal sentinels r102-r134
   finished the core.

**9a32a859 (our v68 chokewall, 1-4):**

1. **g1 25×25, dead r662.** Their forward sentinels (13,18)/(16,19)/(17,20)
   r17-r44 took our core 500→300 by r62 — then our heal line stalled them for
   **575 rounds** before they finished it. We killed all three forward
   sentinels. We laid 177 relay tiles to their 40 and still lost the titanium
   race 6120-7030. Notable: **our launcher spent r64-r86+ repeatedly throwing
   their raiders from ~(19,15) to (20,11)** — a working denial loop that never
   converted into a kill.
2. **g2 28×20, dead r126.** Ferry to (14,11) r2 → gunner (17,11) **r5** →
   first core damage **r6**. 12 harvesters behind it. Our core never landed a
   shot on theirs (0).
3. **g3 18×18 — OUR ONLY WIN, r1000 titanium 7150-4830.** Their one forward
   gunner (#30, r12 at (12,5), d²_ocore 13) was **two-shot by our sentinel #39
   at (12,2)** (built r16, clean N-S alignment, d²=9) and died **r19**. They
   never established another forward turret all game (`fwd=[12]`, one entry).
   Our nine sentinels sat as a **ring around our own core** (d²_ourcore 202-346)
   rather than forward. 18 KCM shots into our core in 1000 rounds.
4. **g4 24×24, dead r444.** Our sentinel (8,8) r24 died r36; their forward
   sentinel (18,13) r38 died r65; long attrition, our core stalled at 400+
   until r407, then collapsed. Out-collected 4390-3090.
5. **g5 26×26, dead r227.** Our sentinel (9,10) r26 died r36. Their gunners
   crept (10,8) r25 → (14,13) r130 → **(20,18) r144 at d²_ocore=2**; first core
   damage r145, dead r227. 150 shots into our core; we fired **5 all game**.

### 3.3 The one-line predictor

**Count KCM's turrets planted within d²≤36 of our core.** Games where they
established ≥3: we lost all nine. The one game they got exactly one (killed at
r19): we won. This is the whole match.

---

## 4. Class verdict

### Class: **launcher-insertion**, CtrlAltDefeat family — high confidence

Nearest taxonomy row: **launcher-insertion**, unambiguously. Secondary flavour
of **point-blank gunner battery** (the forward turrets are planted at
d²_enemycore 2-32 and the 10×10 branch is pure point-blank), and a real but
subordinate econ layer. It is **not** a rush (median time-to-kill 275 rounds)
and **not** grind (it wins by core destruction in 7 of 9 wins, not by
tiebreak).

Confidence: **high** for the class, **high** for CAD-family identity. The
evidence is a byte-for-byte match on the map-keyed opening throw table, the
launcher tile, the r6 self-destroy and the 8/8/8 ammo ladder, all reproducing
across five different opponents (so opponent-independent, no confound).

### Probe coverage: **covered by `cad_probe` — no new probe warranted**

`bots/cad_probe/main.py`'s docstring already targets exactly these medians
("Launcher next to their own Core on round 1, two or three of their own
builders thrown at our Core on rounds 2-4, 8 Ti converted on each of r0/r1/r2,
turret planted just outside our Core's melee ring, home economy keeps
running"). Everything KCM does in the first 30 rounds is inside that
instrument's envelope.

Two calibration deltas worth folding into `cad_probe` (cheap, not a new probe):

1. **Fix the 4th ammo conversion at 24** for a KCM-flavoured leg (CAD v107
   dumps a variable surplus of 89-187 instead).
2. **Add the diagonal max-range sentinel finisher** — sentinels planted on the
   exact diagonal ray onto a core footprint tile at d²=32, from ~r100 on
   26×26 maps. `cad_probe` currently models forward turrets only in the
   melee ring; the big-map win condition is this diagonal line, and it is what
   killed us in b3656fe7 g1/g5.

If someone does want a standalone KCM leg, the **5 signature constants a probe
must reproduce** are:

1. `convert_ammo(8)` on r0, r1, r2 — then `convert_ammo(24)` on the round the
   first turret is built. (10×10 branch: `convert_ammo(48)` on r0, no launcher.)
2. Launcher on the Core-adjacent enemy-facing tile at **r1**; three own-builder
   throws at **r2/r3/r4** at max range (target d² to launcher = 25-26);
   **`destroy()` the launcher at r6**.
3. Gunner-dominant forward battery, forward turrets at d²_enemycore ≤ 32,
   first one at r1-r5 (close maps) or r12-r45 (open maps); gunner
   **rotation** used freely (up to 22/game).
4. **Zero splitters, ≤4 barriers, no pre-built home defence** — home turrets
   only after an enemy turret enters d²≤36 of their core.
5. Economy: 4-12 harvesters with **100% facing-correct chain** (chain_dir ==
   chain in every game); first harvester r5-r11.

---

## 5. Counter-candidates

### C1 — Home sentinel ring, not forward sentinels (strongest; we already did it once)

The only game we took off them, we had **nine sentinels around our own core**
and one of them two-shot their forward gunner at r19; they never recovered and
we won the r1000 tiebreak. A sentinel (18 dmg, reload 2, range r²=32) **two-shots
a 25 HP gunner and three-shots a 30 HP launcher/harvester** — it is the perfect
answer to a bot whose entire offence is 20-Ti gunners planted 3-5 tiles from
our core. Forward sentinels, by contrast, live a median of **15 rounds** and do
≤162 damage. Evidence: 9a32a859 g3 (win, home ring) vs the other nine (loss,
forward sentinel). This is the single highest-leverage change and it needs no
new mechanism, only re-aiming what v68 already builds.

### C2 — Point-blank gunner battery on *their* core (proven 5-0, twice)

team lazy v94 (orizon family) killed them in **r66-r91** in all five games:
4 builders, walk from r0, gunners planted at d²_KCMcore 8-13 from **r23**.
SmartFridge v33 did it in **r77-r233**: creeping conveyor road + gunners at
d²_KCMcore 8-17 from **r8**. KCM's home defence is reactive and one-gunner-at-a-
time; it loses the stacking race every time. Our own `orizon_probe` is a frozen
implementation of exactly this. **KCM has zero pre-built home defence and no
barriers — they are the softest core on the board.**

### C3 — Barrier-shielded forward battery (Pantheon's 5-0 recipe)

Pantheon v36 beat them 0-5 while building **12-26 barriers per game** alongside
8-10 gunners. Barriers are 3 Ti / 30 HP and block gunner LOS (gunner shots are
obstacle-blocked; sentinel shots are not). KCM's *only* answer to a forward
turret is a counter-gunner at d²=2-9 — a barrier between them denies the shot
outright, which is why Pantheon's forward sentinel at (6,12) r17 survived when
ours never do. KCM built ≤4 barriers in any game; they have no counter-play to
a walled battery.

### C4 — Deny the r2-r4 ferry landing zone (cheap, opportunistic; low ceiling)

The throw table is **map-keyed and opponent-independent** (confirmed here across
five opponents, and independently in the CAD pre-mortem). On maps with ~12-tile
core separation the raiders land at d²_enemycore **17-29** — inside our own
half — at round 2. A barrier or a body on that tile at r0-r1 costs 3 Ti.
Caveat, carried over from `docs/research/cad-ferry-premortem-2026-08-07.md`
K2: **deny-vs-displace is untested** — `can_launch` needs a passable target, and
whether their selector falls through to the next tile is unknown. On large
maps (24×24+) the landing zone is mid-map and worthless to deny (K3). Treat as
a small opportunistic add-on to C1/C2, not a plan.

### C5 — Just convert ammo

Not a counter so much as a defect fix, but it is the largest single number in
the corpus: we fired **5, 7, 10, 13, 18, 43, 76, 79, 96, 107** shots per game
against their **63, 93, 111, 127, 137, 171, 253, 278, 401, 454**. Ten forward
sentinels that never shoot lose to six gunners that always do.

---

## 6. Anomalies + open questions

1. **The "CAD ferry loop" may be misattributed — worth re-checking.** In every
   KCM game with a long repeat-throw loop, the launcher doing the throwing is
   the **opponent's**, not KCM's: KCM's only launcher is destroyed at r6, yet
   9a32a859 g1 shows *KCM builders* thrown from ~(19,15) to (20,11) ten-plus
   times between r64 and r86 — by **our** launcher #30 at (19,16). CAD v107
   likewise builds exactly 1 launcher per game in `9d2b38bb` and destroys it at
   r6, in a 582-round game. The pre-mortem's "≥3-repeat ferry tile in 6 of 7
   long games" may therefore be *the defender recycling the attacker's raiders*,
   not an attacker ferry — which would invert the K1/K2 analysis (there would be
   nothing to deny). Recommend re-running the launcher-attribution on
   a7aa49ec/b10cce55/cdbd5b52 before any further investment in that line.
2. **Why the v7 → v1 rollback?** v7 lost 0-5 twice in unrated challenges at
   15:36Z and the label reverted to 1 by 16:27Z. The openings are identical, so
   whatever v7 changed is invisible in a 66-324 round loss. If they re-ship a
   v8+, re-read before assuming this classification holds.
3. **The 10×10 branch is a different bot.** No launcher, `convert_ammo(48)` at
   r0, gunners point-blank at r1/r2. n=2 (b3656fe7 g3, 9e41db1a g5). It won
   one and lost one. Whether it is a size threshold on map area, on core
   separation, or on wall count is undetermined.
4. **The third throw (r4) is not always forward.** On the 16×16 (0,0)-core map
   it goes to (4,0) — d²=16 from their *own* core, away from the enemy. Either
   a fallback when the preferred tile is taken, or a deliberate home-side
   placement. Unresolved; the first two throws are the reliable ones.
5. **Our v67's g3 sentinels had no firing line.** Three sentinels built r2-r4 on
   a 10×10 map, 107 shots fired, **zero** landed on the enemy core footprint,
   and none of them was ever killed. That is our bug, not their counter — but it
   means b3656fe7 g3 carries no information about how KCM handles a snipe.
6. **They rotate gunners a lot (up to 22 × 10 Ti = 220 Ti/game).** The Orizon
   family explicitly never rotates because a new gunner adds DPS while a
   rotation only redirects. Whether KCM's rotations are productive or a leak is
   untested; if it is a leak, it is ~11 extra gunners' worth of titanium.
7. **Elo note.** They are ~1585 with 49-52 rated matches, and this corpus says
   they lose to Pantheon (1891), team lazy (1895) and SmartFridge (1752) 0-5.
   Their rating is being held up substantially by beating *us*. Fixing C1
   should move both ratings.
