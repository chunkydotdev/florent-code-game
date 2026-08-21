# DECODE — raider launch timing in v174 ("Baltsars banditer v1" = `bots/_v537socket`)

**Provenance.** Fresh opus decode agent, research lane, session s52, 2026-08-21
(`date -u` at start of work: `Fri 21 Aug 2026 05:45:54 UTC`). Trigger: Magnus
watched the maiden rated match of v174 (match `20a19adb`, 3-2 win vs
`lingling_40h` v86, created `2026-08-21T05:32:59.730Z`) and marked: *"We launch
our two raiders really late in the games vs lingling."* Relayed by the builder.
**Decode-only** — no games run, no bot edits, no platform mutations. All
surfaces are local files.

**Inputs (all read-only):**
* `replay_archive/20a19adb-54f8-4cfd-a464-5159b1a0085e_game_{1..5}.replay26`
  + `.meta.json` — the maiden match, **all 5 games archived**.
* `replay_archive/*.meta.json` + replays — **92 matches / 460 games of ours vs
  `lingling_40h`** across our v90…v174, used for the same-opponent baseline.
* `scratchpad/s52_v537_build/mech/rep/` (600 games, arms `v537socket` /
  `v536trust`) and `scratchpad/s52_v537_build/mech2/rep/` (900 games, arms
  `v537socket` / `v537noraid` / `v536trust`) — **the paired local surface**,
  5 maps × 30 seeds × 2 seats, opponent `bots/_x3r0v169mjolnir` (the Mjolnir
  holder family — the same line that was live on the ladder as **v168**).
* `scratchpad/s51_v529_build/head/rep/` (960 games decoded: arms `v529`,
  `parent`; opponent `bots/_v488beltbreak2`) — the lineage anchor surface.
* `scratchpad/s52_v535_build/dose/{dose_v535,dose_par}/*.rep` (48 games,
  4 maps × 3 seeds × 2 seats) — the v535-era dose tape.
* Trees read-only: `bots/_v537socket`, `bots/_v536trustport`, `bots/_v529merge`.
* `scratchpad/s52_v535_build/dose.sh` was NOT the paired v535 replay surface the
  brief expected — `scratchpad/s52_v535_build/` contains **0 `.replay26` files**;
  its dose replays are `.rep` (same format, different extension) and are the
  48 games above. Named so the count is not silently smaller than the brief.

**Instruments written for this decode** (in `scratchpad/s52_launchtime/`, not
committed): `launchtime.py` (per-team launch/throw/arrival timeline off the turn
stream), `agg.py` (arm aggregation + paired within-cell diffs), `field_agg.py`
(platform-archive aggregation joined to `meta.json` seat/version),
`trace.py` (round-by-round opening trace). Reused: `tools/replay_census.py`
primitives and `scratchpad/s52_diffstudy/ringtime.py` (socket-claim instrument).

**Instrument validation (each guard driven to the other verdict):**
* Every metric is computed **identically for both teams**, so each number
  carries its own mirror control. The opponent columns are non-degenerate and
  differ from ours in every cut below (e.g. same replays: our `launch_r` med 5,
  their med 1) — the columns are not constants.
* `launch_r`'s paired-diff column reports `worse=0` for `v537socket − v536trust`
  (600 cells over two batteries). That is meaningful only because the same
  routine reports non-zero `worse` counts on the other columns from the same
  rows (`arr2_r` worse=64, `nlaunch` worse=133) — the "worse" branch fires.
* `eco_pre_launch` is the **positive dose control** for the socket plank and it
  fires in **300/300** paired cells (+1.86 eco builds before the launcher in the
  socket arm, 95% CI [+1.82, +1.90]) — the plank demonstrably ran in every
  treatment game.
* Throw detection = a `MoveBuilderBot` with d² > 1 from the bot's previous
  position (a legal walk is always d² = 1). Cross-checked against `trace.py`
  output on a game where the launcher placement, the throw, and the launcher's
  `removeEntity` appear in the expected r5 → r6 → r7 order.
* Maps were identified by **exact tile-grid fingerprint** against `maps/*.map26`
  (34 maps indexed); 5/5 maiden games and 90/90 baseline games matched a named
  map, 0 `UNKNOWN`.
* ⛔ **ONE DEFECT FOUND IN THIS DECODE'S OWN INSTRUMENT, AND IT LANDED ON THE
  COMPARISON ARM.** The first version of `launchtime.py` built the per-round
  launcher snapshot used for throw attribution **after** applying that round's
  `removeEntity` events, so a ferry launcher that throws and self-destructs in
  the **same** round was already gone from its own throw round and the throw
  fell through unattributed. That is exactly the Mjolnir-family ferry pattern
  (place r1, throw r2, remove r2) — i.e. **the bug systematically under-reported
  the comparison arm's throw clock**, and it was caught only because a
  downstream number (v168 reaching the midgard ring at r12 with a "first throw"
  of r12) was **geometrically impossible** — 34 tiles in 12 rounds. Fixed, then
  validated against a hand trace of
  `replay_archive/c94ff793-…_game_3.replay26` (launcher#7 placed r1 @(5,3),
  throws bb#3 from (4,3) at r2): pre-fix `throw1_own_r` = 12, post-fix = **2**,
  matching the trace. **Every number in this document is from the post-fix
  re-run** of all six surfaces (2,973 games re-decoded). The un-fixed reading
  is retained here rather than deleted because it is the reason the check
  existed.

---

## 1. The maiden match, per game — MEASURED

We are team B (`teamBVersion 174`); lingling_40h is team A (v86). Rounds are
0-indexed. `arr1`/`arr2` = round the **first** / **second distinct** own builder
bot reached d² ≤ 2 of the enemy core footprint (the ring band).

| game | map | rounds | result | first launcher | first own throw | arr1 | arr2 | launchers built |
|---|---|---|---|---|---|---|---|---|
| 1 | **midgard** 30x30 | 1000 | WIN `titanium_collected` | **NEVER** | **NEVER** | 49 | 54 | 0 |
| 2 | drumlin 25x25 | 202 | WIN `core_destroyed` | r5 | r6 | 10 | 13 | 5 |
| 3 | ragnarok 30x30 | 149 | LOSS `core_destroyed` | r5 | r6 | 24 | 78 | 15 |
| 4 | icefloe 20x20 | 311 | WIN `core_destroyed` | r5 | r6 | 12 | 165 | 7 |
| 5 | valkyrie 30x30 | 173 | LOSS `core_destroyed` | r5 | r6 | 12 | 53 | 5 |

**Reading.** The launcher/throw clock is **not variable** — r5/r6 in 4 of 5
games, and absent entirely in the 5th. The *arrival* clock is what varies:
first raider r10/r24/r12/r12 (and r49 in game 1); second raider r13/r78/r165/r53
(r54 in game 1, on foot). One game in five (midgard) had **no raid at all** and
became a round-1000 game — a defeat by `R1000_IS_DEFEAT` even though we won it.

---

## 2. Same opponent, previous holder — the v168 baseline (FIELD)

`lingling_40h` v86 is the opponent version in the maiden. Our previous ladder
holder **v168** (the Mjolnir family, `x3r0`) met **the same opponent version 25
times** (5 matches: 1 unrated + 4 ladder, 2026-08-20T11:20Z → 2026-08-21T00:52Z).

| cut | n games | first launcher (med) | first own throw (med) | arr1 (med) | arr2 (med) | arr1 ≤ 16 | arr2 ≤ 16 | no launcher ever |
|---|---|---|---|---|---|---|---|---|
| **our v168 vs lingling v86** | 25 | **1** | **2** | 12 | 91 | 0.720 | **0.000** | 2/25 |
| **our v174 vs lingling v86** | 5 | **5** | **6** | 12 | 54 | 0.600 | 0.200 | 1/5 |

Per map, same opponent version (v174 n = 1 per map — the whole maiden):

| map | v168 launch / throw / arr1 / arr2 | v174 launch / throw / arr1 / arr2 |
|---|---|---|
| drumlin | 1 / 2 / 8 / 96 (n=1) | 5 / 6 / 10 / **13** |
| icefloe | 1 / 2 / 9-13 / 97-202+never (n=4) | 5 / 6 / 12 / 165 |
| **midgard** | 1 / 2 / **12** (5/5) / 75-96 (n=5) | **-1 / -1 / 49 / 54** |
| ragnarok | 1 / 2 / 27 / never (n=2) | 5 / 6 / **24** / **78** |
| valkyrie | 1 / 2 / 25-36 / never+181 (n=2) | 5 / 6 / **12** / **53** |

The holder's ferry is **uniform**: launcher r1, throw r2 in every game on every
one of these maps. Its hop chain is one launcher per hop, throwing every second
round (traced: r2 →(8,7), r4 →(11,12), r6 →(15,16), r8 →(19,20), r10 →(23,24),
r12 → the ring on midgard — 34 tiles in 12 rounds).

**When the r1 ferry became the thing to compare against — dated.** Decoding the
launch clock for **all 26 of our versions** in the 460-game lingling archive:
the r1 launcher / r2 throw opening appears **only from v161 onward**
(v161 launch med 1 · v162 med 1, throw med 2, n=45 · v163 med 1 · v168 med 1,
throw med 2). Everything before it (v140 n=110, v152 n=45, v154 n=25, v155,
v159 …) has launcher medians of **160-350 with the launcher NEVER built in most
games** — that is the home-defence launcher at `LAUNCHER_MIN_RND = 160`, not a
ferry. ⇒ **The reference behaviour Magnus is comparing v174 against is ~3 days
old (v161, 2026-08-18), and v174 is the FIRST ship of the v529merge development
lineage.** Its r5 clock is new *to the ladder* while being old *in the tree*.

**Reading, and it splits Magnus's marker in two.**
* **The LAUNCH clock really is 4 rounds later than the bot he had been
  watching**: holder ferry throw at r2, ours at r6; holder launcher at r1, ours
  at r5. That is a genuine, visible change in what the opening looks like.
* **The ARRIVAL clock is not worse** — first-raider median r12 either way, and
  on valkyrie (r12 vs r25/r36) and ragnarok (r24 vs r27) v174 arrives *earlier*
  despite starting its ferry four rounds later, because its chain converts more
  of the throws it does make.
* **The second raider is markedly better under v174**, not worse: holder
  `arr2 ≤ 16` in **0 of 25** games vs the same opponent, median r91; v174 median
  r54 in the maiden and median **r15** on the local paired tape (§3).
* **midgard is a real regression against the holder**: v168 launched at r1 and
  reached the ring at r12 in **5/5** games there; v174 never built a ferry
  launcher and walked in at r49. See §6 — this is a lineage-old map refusal, not
  a v537 defect.

---

## 3. Is it the socket plank? — the paired local mechanism test

Two batteries, arms interleaved inside each cell (so arms share a wall-clock
slice), opponent `bots/_x3r0v169mjolnir`, maps glacierkeep / drakkarfjord /
auroraveil / yulerune / icefloe, 30 seeds × 2 seats.

**Per-arm medians (ours), 300 games per arm:**

| arm | battery | launcher | own throw | arr1 | arr2 | arr1 ≤ 16 | arr2 ≤ 16 | game share |
|---|---|---|---|---|---|---|---|---|
| `v536trust` (no socket plank) | mech | 5 | 6 | 13 | 17.5 | 0.857 | 0.427 | 0.280 |
| `v537socket` (SHIPPED as v174) | mech | 5 | 6 | 14 | 15 | 0.963 | 0.670 | 0.507 |
| `v536trust` | mech2 | 5 | 6 | 13 | 17 | — | — | — |
| `v537noraid` (raider excluded from claiming) | mech2 | 5 | 6 | 13.5 | 15 | — | — | — |
| `v537socket` | mech2 | 5 | 6 | 14 | 15 | 0.960 | 0.663 | — |
| **opponent `_x3r0v169mjolnir` in the same games** | both | **1** | **2** | **10** | ~105-119 | — | — | — |

**Paired within-cell differences (same map, same seed, same seat), treatment
minus `v536trust`:**

| battery | metric | n cells | mean diff | 95% CI | worse / better / tie |
|---|---|---|---|---|---|
| mech | `launch_r` | 300 | **−0.11** | [−0.15, −0.07] | **0** / 33 / 267 |
| mech | `throw1_own_r` | 300 | **−0.79** | [−0.96, −0.62] | **0** / 68 / 232 |
| mech | `arr2_r` (first arrival) | 299 | **−5.65** | [−7.99, −3.31] | 64 / 50 / 185 |
| mech | `arr2_r2` (second arrival) | 271 | **−8.44** | [−15.01, −1.88] | 33 / 132 / 106 |
| mech | `eco_pre_launch` (dose control) | 300 | **+1.86** | [+1.82, +1.90] | 300 / 0 / 0 |
| mech2 | `launch_r` (`v537noraid`) | 300 | −0.01 | [−0.05, +0.03] | 19 / 22 / 259 |
| mech2 | `throw1_own_r` (`v537noraid`) | 300 | −0.69 | [−0.86, −0.52] | 19 / 68 / 213 |

Local batteries are balanced-by-construction fixtures, so naive intervals are
used (measured pair-weighted DEFF = 0.98 on this class, s39 audit); the platform
DEFF constants do **not** apply here.

**Reading — THE ORDERING HYPOTHESIS IS REFUTED ON THIS SURFACE.** The socket
claim demonstrably fires (dose control 300/300, +1.86 eco builds land *before*
the launcher), and the launcher round does not move: mean −0.11 rounds, and in
**600 paired cells across two batteries the socket arm was never once later**
than its parent on `launch_r`. Throw and both arrivals move in the **faster**
direction. `v537noraid` — the arm that removes the raider from the claim
entirely, i.e. the direct control on the only builder-turn channel — is
indistinguishable from both. The plank costs the raid **0 measurable rounds**.

**One honest limit on the within-game dose test the brief asked for.** The
socket-claim round has **no variance to correlate against**: `own1_r = 1` in
**300/300** local v537socket games and **5/5** maiden games (`ringtime.py`,
`b_own1_r`). Pearson r against `launch_r` is undefined (`nan`), and the
"instant vs contested claim" control **cannot be run** — there are no contested
cases (our ring was never plugged before r37 in any maiden game; `b_plug1_r` =
−1, −1, −1, 37, 92). ⇒ **A cause that is constant across games cannot explain an
effect that varies across games.** That is a valid refutation of the ordering
story for the *maiden variation*, but it is a weaker instrument than the arm
contrast above, which is what carries the verdict.

---

## 4. Where the "r9-16 arrival" anchor comes from in the decoded data

Not trusted from the brief — located in the tapes:

| surface | arm | n | launcher | own throw | arr1 | arr1 ≤ 16 |
|---|---|---|---|---|---|---|
| `s51_v529_build/head` (opp `_v488beltbreak2`) | `parent` | 480 | **5** | **6** | **12** | 0.83 |
| same | `v529` | 480 | **5** | **6** | **12** | 0.83 |
| `s52_v535_build/dose` (opp `arms/opp_off`) | `par` (v534) | 24 | 5 | 6 | glacierkeep 12, ragnarok 16-20 | — |
| same | `v535` | 24 | 5 | 6 | glacierkeep 12, ragnarok 16-20 | — |
| `s52_v537_build/mech` | `v536trust` | 300 | 5 | 6 | 13 | 0.857 |
| same | `v537socket` | 300 | 5 | 6 | 14 | 0.963 |

**The r9-16 arrival anchor is confirmed and it belongs to the whole
v527→v537 lineage**: first-ring-arrival median r12-14, inside the band in
83-96% of games. **And so does the r5 launcher / r6 throw** — it is a hard
lineage constant (p10 = 5, p90 = 6) present in v527, v528, v529, the v529 parent,
v534-par, v535, v536trust and v537socket alike. **v174 is exactly on its
lineage's own anchor.** What changed is the *ladder incumbent*: v168 belongs to
the Mjolnir family, which ferries at r1/r2.

**Round-by-round trace of the difference** (`trace.py`,
`mech/rep/v536trust_glacierkeep_s1_A.replay26`; T0 = ours, T1 = Mjolnir; our core
(14,2), theirs (14,26)):

```
r0: T0 PLACE builder_bot#3@(14,4)          | T1 PLACE builder_bot#4@(15,25)
r1: T0 PLACE builder_bot#5@(13,4)          | T1 PLACE launcher#7@(15,24)
r2: T0 PLACE builder_bot#8@(13,3)          | T1 THROW bb#4 (15,25)->(14,19)
r3: T0 PLACE builder_bot#11@(13,4)         | T1 PLACE launcher#12@(14,18)
r4: (T0 bb#3 still idle)                   | T1 THROW bb#4 (14,19)->(14,13)
r5: T0 PLACE launcher#14@(14,5)            | T1 PLACE launcher#15@(14,12)
r6: T0 move bb#3 (14,4)->(15,4); T0 THROW bb#3 (15,4)->(15,10)
r7: T0 THROW bb#11 (13,6)->(14,10); T0 REMOVE launcher#14   <- ONE link, TWO riders
```

**Our seat-0 raider is spawned at r0 and sits on (14,4) doing nothing through
r4**, then builds the ferry launcher at r5. Mjolnir's raider builds at r1 and is
already 12 tiles downrange by r4. Note also the design difference the trace
exposes: **our single ferry link carries both riders (r6 and r7) before
self-destructing** — that is the "two raiders" Magnus is watching, and it is why
our second raider arrives at r15 (median, local) while Mjolnir's second body
arrives around r105-119.

---

## 5. Mechanism anchors

**For the socket plank (the hypothesis under test) — LOCATED, and measured at
zero cost.** The only channel that exists in the source is builder-turn
contention:
`bots/_v537socket/main.py:1556` — `if FS_V537_SOCKET and self._v537_socket_claim(ct, rnd): return`
sits **above** the role dispatch at `main.py:1559`, so a raider that claims a
socket spends that round and skips `_fs_turn`/`_fs_ferry_turn`. Ceiling is
2 turns inside `rnd ≤ FS_V537_BY_ROUND = 4` (`doctrine.py:5471`,
`FS_V537_MAX_SOCKETS = 2`), and it is gated by `FS_V537_RAIDER_CLAIMS = True`
(`doctrine.py:5482`, checked at `eco.py:625`).
The other three candidate channels are **refuted in source**: no queue/priority
insertion (nothing is pushed into `link_queue`; both launcher siters already ban
all 8 heal seats — `siege.py:1642`, `main.py:1910`); funding is 2 × 3 Ti against
a ~400 Ti opening bank while the ferry gate is
`get_global_resources() < cost + FS_LAUNCHER_TI_FLOOR(=6)` (`siege.py:1636-1639`),
never binding at r0-5 (measured `ti_at_launch` median 310); and no store slot or
phase flag is latched (`eco.py:589-612` re-derives from the engine each call).
`raid.py` and `siege.py` are **byte-identical** between `_v536trustport` and
`_v537socket`, so no ferry-path line changed in v537 at all.

**For the r1 → r5 ferry delta vs the Mjolnir holder — LOCATED, see §7.** It is
*not* in the v537 delta and predates v536: the same r5/r6 shows in v527/v528/v529
tapes from s51.

---

## 6. midgard — the one game that had no raid at all

Maiden game 1 = **midgard**, no launcher ever, first raider on foot at r49,
round-1000 game.

This reproduces **exactly** on the local v535-era dose tape, on the same map,
against a different opponent, in **both** arms:

```
dose_par (v534)  midgard n=6  launch=[-1,-1,-1,-1,-1,-1]  arr1=[56,56,56,57,57,57]
dose_v535        midgard n=6  launch=[-1,-1,-1,-1,-1,-1]  arr1=[55,55,55,60,60,60]
dose_par         archipelago  launch=[-1,-1,-1,188,188,188] arr1=[42,42,42,58,58,58]
```

⇒ **The midgard ferry refusal is a map-gate property of the v529merge dev
lineage, present at least since v534, and it is NOT caused by the socket plank.**
It is nonetheless a **real regression against the bot that was on the ladder**:
v168 launched at r1 and reached the ring at r12 in **5 of 5** midgard games
against this same opponent version.

---

## 7. What holds the raider idle in rounds 0-4 — LOCATED

Targeted source read of `bots/_v537socket` (commissioned this session), against
the trace in §4.

**The blocking predicate is the v514 relay MUSTER, and it is live only because
of a flag-override that the tree's own comments deny.**

`siege.py:1252-1266` inside `_fs_ferry_turn`:

```python
        # ⛔ INERT IN THE FIRED CONFIG: with FS_CREW_ON False there is one body,
        # `fs_body` is 1 and `_fs_relay_mustered` returns True on its first
        # line, so this whole block reduces to the parent's.
        may_build = True
        relay = LOKI_FS_V514 and FS_V514_RELAY and FS_RELAY_ON \
            and LOKI_FS_CREW and fs_crew_on()
        if relay and getattr(self, "fs_body", 1) == 1 and self.fs_ride_rnd is None:
            if not self._fs_relay_mustered(ct, p, rnd):
                return
```

**That comment is false in this tree.** `doctrine.py:4641-4653`:

```python
def fs_crew_on():
    if LOKI_FS_V520 and FS_V520_PINCER and FS_V520_CREW:
        return True
    return FS_CREW_ON
```

with `LOKI_FS_V520 = True` (`doctrine.py:3947`), `FS_V520_PINCER = True`
(`:3950`), `FS_V520_CREW = True` (`:3960`) — so **`fs_crew_on()` returns True
even though `FS_CREW_ON = False`** (`doctrine.py:2741`). Evaluated by importing
each tree's `doctrine.py`: `_v527collar`, `_v529merge`, `_v536trustport` and
`_v537socket` all report `crew_on=True`, i.e. **the relay is live across the
whole lineage**, which is exactly the span over which the r5 constant is
measured.

**The chain, round by round** (matches the §4 trace exactly):

| round | what blocks |
|---|---|
| r0 | Seat 0 = the raider (`main.py:1466`), `fs_body = 1` (`main.py:1532`), `fs_body_born = 0` (`siege.py:1218`). |
| r1-r4 | Muster branch: backstop `rnd - fs_body_born >= FS_MUSTER_WAIT(8)` not met; `_fs_state_at(FS_SUPP_SLOT)` returns `rid == 0` — **body 2 has not reported** — so `_fs_relay_mustered` returns False (`siege.py:1405-1419`) and the caller **`return`s above both `_fs_build_ferry` and the walk fall-through**. Idle, and it cannot even move. |
| r1-r3 | The core keeps spawning; the 4th spawn is legal only because `fs_crew_on()` swaps `FS_OPEN_BUILDERS`(3) for **`FS_CREW_OPEN_BUILDERS = 4`** (`main.py:1150-1155`) — the same override. |
| r4 | Seat 3 (`FS_CREW_SEAT = 3`, `doctrine.py:2742`) first runs, takes `"supp"`, `fs_body = 2`, and publishes `rid` into `FS_SUPP_SLOT` (store slot 10). **Store writes are buffered one round.** |
| **r5** | Lead reads `rid != 0`, body 2 is at d² = 1 ≤ `FS_MUSTER_DSQ(4)` → mustered → `_fs_build_ferry` → the launcher. |

**No constant contains the number 5.** It is derived: crew seat 3 ⇒ body 2 is
the 4th spawn ⇒ born r3 ⇒ first run + one buffered store round ⇒ the lead
unblocks at r5. The p90 = 6 in the tapes is one round of jitter in when seat 3
first runs.

⭐ **AND THE COST IS ALREADY ON THE RECORD IN OUR OWN DOCTRINE**, measured, in
`doctrine.py:4837-4852`: *"ROSTER SEQUENCING IS THE CAUSE: `_fs_relay_mustered`
returns False with reason `norid` … for rounds 1..4 … The lead does not merely
decline to build; the muster branch `return`s, so it does not move either. FOUR
ROUNDS OF A RUSH SPENT STANDING STILL, 4/4 games."* The fix was built
(`FS_V526_CREW_SEAT = 1`, `FS_V526_MUSTER_WAIT = 3`) and **deliberately disabled
at v527** (`doctrine.py:4864-4876`) because the tempo change alone measured
**−10.83pp at k ≤ 200 with median kill 173 → 237**, replicated over two seed
blocks. ⇒ **The r5 stall is a knowingly accepted price for the
two-riders-one-link relay. What is NEW here is that the relay it buys was
believed inert** — four separate comment sites (`siege.py:1252`, `siege.py:299`,
`raid.py:1217`, `doctrine.py:3007`) assert inertness from `FS_CREW_ON = False`
while the read site has returned True since v520.

**Ruled out, with anchors** (so these are not re-derived): `FS_V519_GF_MIN_RND`
/ `_v519_gunfirst` (`siege.py:1359-1394` — returns False here, and a firing
would emit a `PLACE gunner` the tape does not show); `FS_LAUNCHER_TI_FLOOR`
(`siege.py:1637-1639` — bank ~434 Ti against a launcher at ~28); the
`_home_seat_keys_set()` build-tile ban (`main.py:1927-1937` — round-independent,
and (14,5) is not in it); `_fs_gate` (`siege.py:467-498` — one-shot, cached, no
round term); `SLOT_ROLE_N` (`main.py:1271-1274` — the lead's own slot costs it
nothing); `_v526_rendezvous` (`siege.py:1268-1291` — body-2 only); and
`_v537_socket_claim` (`eco.py:614-661` — v537-only, cannot explain a constant
that holds at v527-v536).

**Side finding worth banking separately:** `FERRY_HOME_ON` (`doctrine.py:3011`)
is a module-level default derived from `FS_CREW_ON` rather than `fs_crew_on()`,
so it evaluates True while the effective crew state is on. The tree only
survives it because `raid.py:1250-1254` re-derives at the read site under
`LOKI_FS_V516`. If `LOKI_FS_V516` were ever flipped off, store slot 10 would get
two writers and the muster would unblock on a stale foreign `rid`.

---

## VERDICTS

**(1) Is the late launch REAL in the maiden? — SPLIT, and both halves matter.**
* **Against the previous ladder holder (v168): YES for the launch clock.** First
  ferry launcher r5 vs r1, first own throw r6 vs r2 — **+4 rounds**, and it is
  the same +4 measured against the same family locally (opponent `_x3r0v169mjolnir`
  in 600 games: their launcher med r1, throw med r2; ours med r5/r6).
* **Against v174's own lineage: NO.** r5/r6 is the v527→v537 constant (960 v529-era
  games, 48 v535-era games, 1,500 v536/v537 games — all median 5/6).
* **The arrival clock is NOT late**: first raider median r12 in the maiden, the
  same as v168 vs the same opponent version, and inside the lineage's r9-16
  anchor in 3 of 5 games (r10, r12, r12; misses are ragnarok r24 and midgard r49).
* **The second raider is FASTER under v174, not slower** — maiden median r54 and
  local median r15, against v168's median r91 with `arr2 ≤ 16` in **0 of 25**
  games vs this opponent.
* **The one true failure in the maiden is midgard**: no ferry, no raid, r1000
  "win" = a defeat under `R1000_IS_DEFEAT`.

**(2) lingling-conditional or general? — GENERAL / chassis-wide.**
The r5/r6 launch clock appears against three different opponents
(`_x3r0v169mjolnir` 1,500 games, `_v488beltbreak2` 960 games, `arms/opp_off` 48
games) and on every map that launches at all. It is not lingling-conditional and
not field-conditional. **One thing IS field-conditional:** the second raider's
arrival degrades from local median r15 to maiden median r54 — the field opponent
interferes with the second rider; that is worth a separate look and is **not** a
v174 regression (v168 was worse on it).

**(3) Ordering-caused? — NO. REFUTED.**
Paired within-cell, 600 cells over two batteries: `launch_r` mean diff −0.11
rounds [95% CI −0.14, −0.07], **worse in 0 cells**; `throw1_own_r` −0.79
[−0.96, −0.62]; both arrivals faster. The dose control fired in 300/300 cells
(+1.86 eco builds before the launcher). The `v537noraid` arm — raider removed
from the claim, the only channel that exists in source — is indistinguishable.
The socket claim is also **constant at r1 in 300/300 local and 5/5 maiden
games**, so it cannot explain per-game variation in arrival. **The "unexplained
−22.5pp cost class" does not run through launcher/raid timing** — whatever it
is, this decode excludes this route.

**(4) Mechanism anchor — BOTH LOCATED, and they are different code.**
* Socket plank: `bots/_v537socket/main.py:1556` (claim branch returns above the
  role dispatch), gated by `FS_V537_RAIDER_CLAIMS` (`doctrine.py:5482`), ceiling
  2 turns inside `rnd ≤ FS_V537_BY_ROUND = 4` — **measured at 0 rounds of actual
  cost** (§3). The other three candidate channels are refuted in source.
* The r1→r5 ferry delta: **`bots/_v537socket/siege.py:1252-1266`** — the v514
  relay muster returns before the ferry build, because
  `_fs_relay_mustered` (`siege.py:1405-1419`) reads `rid == 0` out of
  `FS_SUPP_SLOT` until the seat-3 support body (spawned r3, publishes r4,
  buffered one round) is visible at r5. It is live only because
  `fs_crew_on()` (`doctrine.py:4641-4653`) returns True through the v520
  pincer override while `FS_CREW_ON = False` — **so four comment sites in the
  tree describe this path as inert and it is not.** Not in the v537 delta at
  all (`raid.py` and `siege.py` are byte-identical v536↔v537).

---

## What this does and does not license

* It does **not** license reverting or flag-flipping the socket plank on
  launch-timing grounds — that plank is measured at zero cost to the raid and
  positive on local game share (0.507 vs 0.280 in the mech battery).
* The two things this decode puts on the table are **(a) the 4-round ferry
  start-up gap against the Mjolnir line**, now traced to a muster the tree
  believes is switched off, and **(b) the midgard/archipelago class of maps
  where the ferry gate refuses outright and the game becomes an r1000 economy
  game** — a `R1000_IS_DEFEAT` failure the previous holder did not have.
* ⚠ **(a) is NOT a free fix, and the tree already paid to learn that.** The
  obvious lever (`FS_V526_CREW_SEAT = 1` / `FS_V526_MUSTER_WAIT = 3`) was built
  and disabled at v527 on a measured **−10.83pp at k ≤ 200 with median kill
  173 → 237**. What this decode adds is the *other* half of the trade, which
  was never stated: the relay being paid for was documented as inert, so the
  −10.83pp was priced against a benefit nobody had verified was live.
* Both are **constraints on the next leg, not a build order**: any candidate
  that claims to fix the "late launch" must be measured on `throw1_own_r` and
  `arr2_r` (not on win rate), must be paired within cell, must clear
  `DEFENCE_ADMISSION_BAR`'s timely-kill test given the v526 tempo history above,
  and must be shown not to break the maps that currently launch at r5 — the
  instruments in `scratchpad/s52_launchtime/` will read all of it.
