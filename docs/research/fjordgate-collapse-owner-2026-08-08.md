# Fjordgate / meander collapse: naming the owner

Research arm, 2026-08-08 16:51 CEST. Repo HEAD `eb4366a`.

**Version tags**

| thing | path | md5 |
| --- | --- | --- |
| live v80 "Eir 9b" | `bots/_v89sh/main.py` | `e12f85855654e9e78227582d0dc15d4b` |
| staged head (arm `w`) | `bots/_v93w/main.py` | `52b1f306266ac77997e07e7f35a66f5b` |
| reserve-fix variant (arm `wb`) | `bots/_v93wb/main.py` | `b835132aff45200bcfc5f78bf41988ab` |
| frozen opponent | `bots/cad_probe/main.py` | `6d0e955f96de1f0d11f93db573ade458` |

All line cites below are **`bots/_v93w/main.py`** unless stated otherwise.

**Discriminator bundle** (read-only, produced by the builder arm):
`/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/284161ab-b59c-40d1-b62e-89fea0a300d9/scratchpad/fjord_disc/`
— 72 games, 3 arms x {fjordgate, meander} x 2 seats x 6 seeds vs `cad_probe`, replays kept.
Arms differ from their source bots only by `NOISE_ON=False` and one Core instrument
`print` (verified by diff): `arm_w` = `_v93w`, `arm_woff` = `_v93w` with `OS_ON=False`
(`:1100`), `arm_wb` = `_v93wb`.

Inherited findings taken as given (verified twice already, not re-derived): the
fjordgate seat-B collapse and the meander seat-A collapse persist in all three arms;
SLOT_UNDER never releases in 72/72; SLOT_UNDER latches at r1 pre-damage on
fjordgate seat-B and at r4 on seat-A.

---

## Q1 — What writes SLOT_UNDER=1 at r1 on fjordgate seat-B, and why is it seat-asymmetric?

### Verdict

**The writer is the Core's own proximity scan, branch `:1842`
(`if et == EntityType.BUILDER_BOT and d <= 16`), fired on round 0 by
`cad_probe`'s opening builder standing at (4,4).** The builders' mirror branch
(`:2381-2389`, `b_sense = 16`) writes the same value the same round wherever a
builder can see that tile; it is a co-writer, not a different owner.

**The asymmetry is neither resolution order nor cad seat behaviour. It is pure
measurement geometry in our own code: `d` is measured from the Core's *NW-corner
anchor*, not from the nearest footprint tile.** On a symmetric map the NW anchor
is the *near* corner for one seat and the *far* corner for the other, so two
mirror-identical enemy openings read as d²=8 and d²=18 against a threshold of 16.

### Evidence

Replay-decoded board state, fjordgate, round 0 (all 18 fjordgate games — 3 arms x
2 seats x 3 sampled seeds — byte-identical openings):

| seat | our core anchor | cad's r0 builder | d² anchor-measured | d² footprint-measured | `d <= 16`? |
| --- | --- | --- | --- | --- | --- |
| B (us = B, core (6,6)) | (6,6) | (4,4) | **8** | 8 | **YES** |
| A (us = A, core (2,2)) | (2,2) | (5,5) | **18** | 8 | no |

The two enemy openings are the *same* opening: `cad_probe:539-556` picks the spawn
ring tile nearest the enemy Core anchor, and the source comment says explicitly
that the whole ring is enumerated via `get_nearby_tiles(8)` "never by `pos.add(d)`
— that only reaches the N/W half of the ring and is an absolute-direction bug that
decides maps by seat". Cad is seat-symmetric by construction. Footprint-measured,
both openings sit at d²=8 from our Core. Only *our* anchor-measured number differs.

Round-0 board contents in the seat-B game: exactly two entities placed — cad
builder id=3 at (4,4) and our builder id=4 at (8,5). No enemy turret exists, our
Core is at full HP (Core instrument line `IN r=0 u=0 ti=500 am=0`, then
`IN r=1 u=1 ti=454 am=16`). Store writes are buffered, so `u=1` read at r1 means
the write landed in round 0 — with **no turret on the board and no HP loss**, the
only branch that can have fired is `:1842`. First Core damage is r4, four rounds
later. The launcher hypothesis is dead on source: launchers appear in neither
trigger (`:1837`, `:1842`, `:2381-2383`), and the probe's launcher is placed at
(4,5) on r1 anyway — after the write.

Why the seat-A trigger does **not** fire at r1, checked on the same entities:
cad's builder sits at (5,5), d²=18 from our anchor (2,2) — two over the 16
threshold — and stays out of range until it is thrown to (4,3) at r2 (d²=5). Our
units act with that new position on r3, so seat A's first write is r3 and its
first read r4, matching the measured `under_transitions [[0,0],[4,1]]`. Seat A
builds its first harvester at r5 regardless.

A second, smaller asymmetry rides along and is worth naming because it buys the
attacker one round: **team A resolves before team B within a round** (in every
decoded replay the r0 `PLACE` for team A precedes team B's). So our seat-B Core
sees cad's r0 spawn *on r0*; our seat-A Core would only see cad's r0 spawn on r1.
This accelerates the latch by one round but is not decisive — at d²=18 seat A does
not qualify on r1 either.

### Confidence

**High** for the branch identity and the geometry. The round-0 board has exactly
one candidate entity and one candidate branch; the 8-vs-18 arithmetic is
checkable by hand from the decoded positions.

**Medium-high** on "the Core wrote it, not a builder". Both writers produce
identical output and the replay does not record store writes; the Core is the one
unit *guaranteed* a turn on r0. If a fix is scoped to only one of the two call
sites this distinction becomes load-bearing and should be settled with a
per-writer instrument print.

### What would change the answer

- A `cad_probe` build whose r0 spawn is *not* the enemy-facing diagonal (would
  move the d² numbers, possibly across the threshold for both seats).
- Evidence that our builder id=4 ran on r0 before the Core (would make the builder
  branch a co-equal first writer; does not change the geometry finding).

---

## Q2 — Why zero harvesters for 392 rounds with 5 builders alive?

### Verdict

**It is a money gate stacked on a labour inversion, not a geometry failure.** The
builder that should mine is standing next to ore, action-ready, for hundreds of
rounds. Two independent gates keep it from building, and which one binds depends
on the round:

1. **r0–r119 — the bank never clears bare harvester cost (20 Ti).** Under the
   latch the Core's ammo drip floors the bank at `ti_floor = 12` (`:2024`,
   `:2032-2035`); E1's harvester reserve that would raise the floor to 43 is
   explicitly `not under` only (`:2030`). Meanwhile the siege roles spend the
   income: measured 323 builder attacks (2 Ti each = 646 Ti) + 198 heals (198 Ti)
   + 212 Ti converted, against 980 Ti of passive income over 392 rounds. Bank
   median **10 Ti**; rounds with bank ≥ 20: **9 / 392**.
2. **r120+ — `_eco_spendable`'s siege reserve (`:2226-2231`).** With
   `SIEGE_RESERVE_ON ∧ SLOT_UNDER != 0 ∧ rnd >= HUNT_MIN_RND(120)` the economy
   path demands `ti >= cost + SIEGE_HEAL_RESERVE_TI(16)` = **36 Ti**. This is the
   binding gate in arm `wb`, which fixes gate (1): `_v93wb` raises the under-siege
   conversion floor to harvester-price + 4 (its `RA_ON` block, `_v93wb:1005-1020`,
   `:2071-2080`), and the bank duly reaches 24–25 Ti for **98 / 354 rounds** — and
   the team **still builds zero harvesters**, because 25 < 36.

The **starving branch is `_expand`, `:4065-4072`**:

```python
if (ct.get_global_resources() >= ct.get_harvester_cost() if endgame
    else (self._eco_spendable(ct, ct.get_harvester_cost())
          and harv < self._eco_cap(ct))):
```

with `_eco_spendable` at `:2207-2232`. The builder reaching it is parked correctly:
in `arm_wb_fjordgate_b_1`, builder id=10 (role_n 3, the one pure expander left)
stands at **(3,8) continuously from r160 to r300**, orthogonally adjacent to ore at
(3,7) and (3,9) (fjordgate rows 7 and 9 both carry `o` at x=3). `_expand:4263-4268`
retargets it onto the adjacent ore and `_nav` then returns `Direction.CENTRE`, so it
waits in place — for money that the reserve makes unreachable.

### The labour inversion behind it

Under a permanent latch, the five-seat role table leaves at most **one** economy
worker:

| role_n | role | fate while `SLOT_UNDER != 0` |
| --- | --- | --- |
| 0 | saboteur (`:2286`) | forward siege; pecks the enemy Core forever (measured: builder id=4 attacks (3,2) every round from r11 to r392) |
| 1 | expand → interceptor | `_expand:4050` hands the turn to `_intercept` |
| 2 | expand → converging healer | `_expand:4180-4194` returns before the action phase whenever `SLOT_UNDER != 0 ∧ _core_shelled` |
| 3 | expand | the only seat that can still mine — and it is the one blocked by the money gate |
| 4 | defend | `_defend:3895-3923`: while `under`, the action goes to heal / `_sabotage_prio` / `_try_counterbattery`; the harvester bootstrap at `:3925` and `:3942` is only reached when `defended` is False, and the `_heal_core` fallback at `:3923` succeeds on any damaged Core |

Note `_defend`'s harvester lines use a **raw** `ti >= ct.get_harvester_cost()` — they
bypass the siege reserve entirely. The defender is therefore the seat that *could*
bootstrap on a 25-Ti bank, and it is precisely the seat whose action is claimed
first by the heal/counterbattery ladder.

One more amplifier, worth naming because it converts the opening bank into turrets:
`_try_counterbattery:3748-3764`. The "one emergency battery is free, further ones
wait for income" gate is **waived whenever `_core_shelled`**. On fjordgate seat-B the
Core is shelled from r4 and effectively never whole again, so the waiver is
permanently open. Measured builds, first 40 rounds, all three arms:

| game | our builds r0–40 |
| --- | --- |
| `arm_w_fjordgate_b_1` | sentinel r2 (8,3), sentinel r5 (5,4), sentinel r7 (5,3) — **nothing else, ever** |
| `arm_woff_fjordgate_b_1` | sentinel r1 (8,4), sentinel r5 (5,4), sentinel r7 (5,3) |
| `arm_wb_fjordgate_b_1` | sentinel r2 (8,3), sentinel r5 (5,4), sentinel r7 (5,3) |
| `arm_w_fjordgate_a_1` (control) | sentinel r2 (6,1), **harvester r5**, conveyor r7, conveyor r9, harvester r9, … |

Three sentinels at ~109 Ti scaled is the exact money that seat A spent on its first
harvester + first two conveyors. After r8 the bank is at the floor and the game is
decided.

### Wild-CAD transfer

**Verdict: the wild version of this defect is milder — probably much milder — but
the archive cannot fully clear it, and one mechanism transfers cleanly.**

Latch release is impossible in a wild game as much as in a probe game *once cad is
in range at all*: the decay at `:1857-1869` needs 50 rounds with no re-trigger, and
`cad_probe`'s home sentinels sit permanently inside `d <= 64` of our anchor (`:1837`)
— on fjordgate seat-B our Core anchor is 8 from cad's spawn ring, so **any** turret
cad ever builds near its own Core re-arms `SLOT_ATK_RND` every round. Wild
CtrlAltDefeat also builds early sentinels/gunners on that ring (archive decode
below shows gunners at (4,5),(5,4),(5,2),(5,1) by r4), so the never-releasing latch
is a wild property, not a probe artefact.

What does **not** transfer is the total collapse. Archive reality check (only
`replay_archive/`, no downloads; 8 CAD-vs-OpenSverige games on the two gate maps,
found by decoding map dims + core positions):

| replay | map | our seat | our version | first harvester | first delivery | rounds |
| --- | --- | --- | --- | --- | --- | --- |
| `3e8bd0bf…_game_2` | fjordgate | B | v72 | **r4** | r18 | 381 |
| `8d0e02c1…_game_1` | fjordgate | B | v75 | **r4** | r101 | 316 |
| `2b05487d…_game_2` | fjordgate | A | v72 | r4 | r9 | 1000 |
| `0803bd92…_game_5` | fjordgate | A | v69 | r5 | r10 | 1000 |
| `0803bd92…_game_1` | meander | A | v69 | r5 | — | 277 |
| `8704178a…_game_1` | meander | B | v74 | r7 | r18 | 413 |
| `922b5da8…_game_3` | meander | A | v77 | r6 | r17 | 103 |
| `b4287ac4…_game_3` | meander | A | v79 | r7 | r18 | 218 |

**No wild game in the archive shows the zero-harvester signature on either gate
map, on either seat.** The two wild fjordgate seat-B games built a harvester on r4
— the exact turn the probe games spend on their second standoff sentinel.

Two concrete differences between wild and frozen, both replay-verified:

- The probe places a launcher at (4,5) on r1 and **never loses it** (no `RemoveEntity`
  in 392 rounds). In the archived wild fjordgate seat-B game cad places **no launcher
  at all** on that seat. This is the P6 caveat made concrete: the probe's permanent
  launcher is an extra impassable enemy building 5 tiles² from our Core anchor for
  the whole game.
- The probe plants a sentinel at (5,7) on r3 — d²=2 from our anchor — which is what
  keeps `SLOT_THREAT` hot and drives the counterbattery waiver into buying two more
  sentinels on r5 and r7.

**Caveat, stated plainly: this is not a clean control.** The archive contains no
v93w-vs-wild-CAD fjordgate game; the wild samples are v69–v79. I checked that the
mechanism is not a recent regression — the `d <= 16` anchor trigger exists
unchanged in `bots/opp_v72/main.py:846`, `opp_v74:880`, `opp_v76:964`,
`opp_v78:817`, and the counterbattery bleeding-waiver comment is present in
`opp_v72` onward and in the live `_v89sh:3336`. So both mechanisms predate the
wild games that did *not* collapse, which points the residual at the probe's
opening (permanent launcher, r3 near-Core sentinel) rather than at our version
drift — but it does not prove it.

### Confidence

**High** on the money-gate identification: the `wb` arm is a natural experiment
that separates gate (1) from gate (2), and it lands on the wrong side of 36 by a
measured 11 Ti.
**High** on the labour inversion (source-read, and corroborated by the parked
expander).
**Medium** on wild transfer being milder — 2 wild seat-B samples, older bot
versions.

### What would change the answer

- One `_v93w`-vs-wild-CAD fjordgate seat-B game with a harvester before r10 would
  upgrade "milder" to "probe-specific opening".
- A fourth arm with `SIEGE_HEAL_RESERVE_TI = 0` that still builds zero harvesters
  would refute gate (2) and push the whole weight onto the labour inversion.

---

## Q3 — Does the under-siege-economy defect generalize beyond gate maps?

### Verdict

**Yes, and the right class name is neither "gate map" nor "cores in sentinel
lane". It is "the enemy's *home* ring is inside our anchor-measured trigger
radii" — which makes the latch a property of the map, not of enemy aggression.**
Fjordgate is the pool's only map where that holds at `b_sense = 16`, but four maps
hold it at the turret radius of 64, and every one of them is seat-asymmetric in the
same NW-anchor direction.

Computed from `maps/*.map26`: for each seat, the anchor-measured d² from our Core's
NW corner to the *nearest tile of the enemy Core's own spawn ring* — i.e. how close
an enemy unit that never leaves home already is to tripping our triggers.

| map | dims | core fp d² | seat A anchor d² | seat B anchor d² | class |
| --- | --- | --- | --- | --- | --- |
| **fjordgate** | 10x10 | 18 | 18 | **8** | builder-trigger (≤16) **on seat B only** — seat-asymmetric; also turret-trigger both seats; cores in sentinel lane |
| **meander** | 25x15 | 36 | 36 | 25 | turret-trigger (≤64) both seats |
| **antler** | 14x18 | 49 | 49 | 36 | turret-trigger both seats |
| **moonrise** | 21x8 | 64 | 64 | 49 | turret-trigger both seats (seat A exactly at threshold) |
| lighthouse | 16x16 | 98 | 98 | 72 | — |
| eider / heart / nordkap | 28x20 / 28x20 / 20x26 | 121 | 121 | 100 | — |
| atoll | 18x18 | 242 | 221 | 221 | — |
| drumlin, jackpot, saga, snowflake, archipelago | — | 288–338 | 288–338 | 242–288 | — |
| hive | 25x25 | 580 | 549 | 545 | — |

Two structural readings fall out:

- **The NW-anchor bias is systematic, not a fjordgate quirk.** On every
  non-degenerate map the seat-B number is smaller than the seat-A number, by
  roughly the diagonal of the footprint. Fjordgate is simply the one map where the
  gap straddles a threshold (8 vs 18 across 16). Moonrise seat A sits *exactly* at
  64, i.e. one tile of map-editor drift from doing the same thing at the turret
  radius.
- **The "gate map" class as currently used is really the turret-trigger class**:
  fjordgate, meander, antler, moonrise. On all four, an opponent that builds a
  single home turret and never advances pins `SLOT_UNDER` for the entire match via
  `:1837` and `:2381`, because `:1857-1869` needs 50 consecutive quiet rounds that
  can never occur.

### Could the same latch express as a *late* collapse at high economy? (heart)

**Yes, and it would look exactly like the heart signature.** Heart's anchor
distances (121 / 100) are far outside both radii, so heart cannot latch from
opening geometry — the latch has to be *earned* by an enemy unit advancing to
within d²≤64 (turret) or ≤16 (builder) of our anchor, which on a 28x20 map happens
mid-game. From that round on, at 10,780 Ti collected, the money gates are all
vacuous (a 16-Ti reserve against a four-figure bank) but the **labour** gates are
not:

- `_expand:4180-4194` — role_n 2 **and every role_n ≥ 5 replacement** stop expanding
  and converge on the Core for as long as `SLOT_UNDER != 0 ∧ _core_shelled`. Late
  game, replacements are most of the workforce, so this scales *up* with how many
  builders we have.
- `_defend:3895-3923` — the defender's action is claimed by heal/sabotage/
  counterbattery; its harvester and link lines (`:3925`, `:3931`, `:3942`) are
  unreachable while `defended`.
- `_try_counterbattery:3748-3764` — with a shelled Core the "wait for income" gate
  is waived permanently, so late-game bank flows into fixed-facing turrets rather
  than into harvester replacement.

Net predicted late signature: **harvester count stops growing and stops being
replaced from the latch round onward, while the bank is large and ore remains
unmined** — which is what "lost r922/633 both seats at 10,780/7,850 Ti collected"
looks like from the inside.

### Testable prediction (confirm/refute shared ownership)

Run the heart games with the same Core instrument (`SLOT_UNDER` per round) plus a
per-round harvester-alive count and an ore-occupancy count, and measure:

> **Predicted (shared ownership):** there is a single round `R` at which
> `SLOT_UNDER` first becomes non-zero and never returns to zero; harvester *net
> adds* in the 100 rounds after `R` are ≥80 % below the 100 rounds before `R`; the
> bank exceeds `harvester_cost + 16` on the large majority of post-`R` rounds; and
> at least one builder of role_n ∈ {2, ≥5} is within vision of the Core (d² ≤ 20)
> on the large majority of post-`R` rounds.
>
> **Refuted (separate owner):** harvester net adds fall *before* `R`, or the bank
> sits below `harvester_cost + 16` post-`R` (that would be the money gate, i.e. the
> fjordgate mechanism, not the labour one), or the converge predicate is false most
> post-`R` rounds (then the plateau is owned by something else — harvester
> *destruction* rate, or `_eco_cap`, which is 18 and could simply be saturated at
> that economy).

The `_eco_cap = 18` ceiling (`:26`, `_eco_cap:3161-3171`, surge to 24 only at
≥1500 Ti and ≥r300) is the most likely confounder and must be measured, not
assumed, before heart is attributed to this defect.

### Confidence

**High** on the map-class table (arithmetic over the shipped map files).
**Medium** on the heart hypothesis — it is a source-derived mechanism with a
matching signature, not a measurement. No heart replay was decoded for this note.

### What would change the answer

- A heart decode showing harvester adds falling before the latch, or showing
  `_eco_cap` saturation.
- Any evidence that `SLOT_UNDER` *does* release on heart (a real 50-round quiet
  window), which would break the whole "never releases" premise off the gate maps.

---

## Fix-design implications

The builder owns the fix. These are the options the evidence directly supports,
each with the risk surface the evidence also shows. No tuning numbers are proposed
beyond the thresholds already in the file.

**A. Footprint-measure the trigger distances (Q1's direct owner).**
Replace the anchor-measured `p.distance_squared(ep)` at `:1832` / `:1837` / `:1842`
and `self.core.distance_squared(ep)` at `:2380` with a min-over-footprint distance
— the file already has `core_tiles()` and uses exactly this idiom in
`_hunt_turret:3623` and `_try_counterbattery:3736`.
*Effect:* seats become symmetric — fjordgate seat A then reads 8 as well.
*Risk:* this makes the latch **more** eager, not less: seat A gains the r1 latch it
currently escapes. On the measured evidence seat A's late latch is what lets it
bootstrap (1840 Ti collected vs 0), so this change alone would plausibly turn the
one surviving fjordgate seat into a second collapse. **It is a correctness fix that
must not ship without B or C.** Its real value is removing an invisible seat
lottery from every map in the table above.

**B. An economy floor that survives the latch.**
The `wb` arm proves the *conversion* floor is not enough. The evidence points at
`_eco_spendable:2226-2231` instead: while a team has fewer than `ECO_NEED`
harvesters (or zero delivered titanium), the siege reserve should not apply to the
first harvester. Note `_defend:3925` already encodes exactly this idea — a raw
`harv < 1 and ti >= harvester_cost` bootstrap that bypasses the reserve — and it is
simply unreachable because `defended` is set first.
*Risk surface:* the reserve exists to keep a till for heals and pecks under siege
(`SIEGE_HEAL_RESERVE_TI` comment, `:2208-2223`); exempting the bootstrap spends
into that till exactly when the Core is being shot. Bounded exposure: one harvester
cost, once, and only while the team has no income at all.

**C. Make the bootstrap reachable in `_defend`.**
Move the `harv < 1` harvester bootstrap (`:3925`) **above** the `if under:` block at
`:3897`, or make `defended` not swallow the turn when `harv == 0`. The defender is
the one seat that already bypasses `_eco_spendable`, and in the `wb` arm it stood on
a 24–25 Ti bank for ~98 rounds with 20-Ti harvesters unbuilt.
*Risk:* one round of the defender's action is taken away from healing a bleeding
Core. The universal adjacent heal at `:2607-2626` still fires first on every round
the defender is on a seat, so the cost is bounded to the rounds where it is *not*
adjacent — which are exactly the rounds it is walking anyway.

**D. Tighten what counts as a sighting.**
The latch currently fires on an enemy unit **standing at home**, which on four pool
maps is a permanent state. Candidate discriminators the source already supports:
require the sighting to be *inside our half*, or require a turret whose attack
pattern actually reaches our footprint (`can_fire_from` / `get_attackable_tiles_from`
are already used in `_sp_covered_tiles:1792-1809`).
*Risk:* this is the widest-blast-radius option — `SLOT_UNDER` gates the Core heal,
the hunt, the converge, the counterbattery, the ammo magazine and the siege
respawn floor. Every one of those was individually measured into the file. A
sighting-trigger change re-opens all of them at once and needs the full vs-field
battery, not a two-map discriminator.

**E. Cap the counterbattery waiver (`:3748-3764`).**
The "unless the Core is provably BLEEDING" waiver is unbounded, and it is what
converts the opening bank into three fixed-facing sentinels before the first
harvester. A count bound (rather than a state bound) would keep the meander case
the waiver was written for while stopping the third turret.
*Risk:* the waiver's own docstring records the meander regression it was added to
fix (zero turrets alive after r299 against 804 shots). Any bound must be verified
against meander specifically.

**Interaction to flag for the builder:** A and D both change *when* the latch is
on; B, C and E change *what happens while it is on*. The measured evidence says the
damage is in the second group — `woff` and `wb` both prove that changing one input
to the latch leaves the collapse intact — so the smallest shippable scope is
B and/or C, with A held back as a correctness follow-up.

---

## Self-checks

Every claim above, and how it was established.

| claim | how verified |
| --- | --- |
| Core trigger branches are turret d²≤64, builder d²≤16, ferry, HP-drop | source read, `:1828-1850` |
| Builder trigger branches use `gun_sense`/`b_sense` (64/16; 100/36 on B8 big squares, `B8_ON=False` at `:451`) | source read, `:2366-2396`, `:1538-1539`, `:2277-2279` |
| Launchers are in neither trigger | source read (inherited pre-read, re-confirmed on the same lines) |
| fjordgate 10x10, cores A(2,2) B(6,6), core fp d²=18 | replay Map block decode + `maps/fjordgate.map26` |
| cad's r0 builder at (4,4) [seat B] / (5,5) [seat A]; d² 8 / 18 from our anchor | replay decode, 18 games (3 arms x 2 seats x seeds 1,3,6) — identical every time |
| r0 board has no enemy turret and our Core at full HP | replay decode (2 PlaceEntity events in turn 0) + Core instrument `IN r=0 u=0 ti=500 am=0` |
| SLOT_UNDER read 1 at r1 ⇒ written r0 | Core `BotOutput` instrument line + the buffered-write rule in project CLAUDE.md |
| first Core damage r4 | `instruments.json`, `first_core_damage` (built by the builder arm's `instr.py`, which decodes 64-bit two's-complement HP deltas) |
| cad's spawn choice is seat-symmetric by construction | source read, `bots/cad_probe/main.py:539-556` |
| team A resolves before team B within a round | replay decode — ordering of r0 `PlaceEntity` events in every fjordgate/meander game inspected |
| seat A latches r4 via cad's builder reaching (4,3) on r2 | replay decode + `instruments.json` `under_transitions [[0,0],[4,1]]` |
| meander latches r4 at value **2** (ferry), both seats | `instruments.json` (inherited) + `ferried()` arithmetic on the decoded r2 position (10,4), which is footprint-measured (`:1291-1305`) and therefore seat-symmetric |
| fjordgate seat-B builds: sentinels r2/r5/r7 and nothing else; seat A: sentinel r2, harvester r5, conveyors r7/r9 | replay build-event decode (`BuilderBuild` + `PlaceEntity`), one game per arm |
| bank median 10, rounds ≥20 = 9/392 (arm w seat B) | replay `UpdatePlayers` decode |
| 323 attacks / 198 heals / 212 Ti converted (arm w seat B) | replay `BuilderAttack` / `BuilderHeal` / `CoreConvertAmmo` decode |
| arm `wb` reaches bank 24–25 for 98/354 rounds and still builds zero harvesters | replay decode + `disc_results.json` (`usTi=0`, loss r354, all 6 seeds) |
| `_eco_spendable` demands cost+16 under siege past r120 | source read, `:2207-2232`; constants `:412`, `:433` |
| ammo `ti_floor` is 12 under siege, 43 in peace | source read, `:2024-2032`; `E1_*` at `:996-1004` |
| `_v93wb` raises the under-siege conversion floor to harvester price + 4 | source diff `_v93w` vs `_v93wb` (`:1005-1020`, `:2071-2080`) |
| expander id=10 parked at (3,8) r160–r300 adjacent to ore at (3,7)/(3,9) | replay position track + decoded map rows 7 and 9 |
| role table under a permanent latch | source read: `:2285-2303` (assignment), `:4050` (intercept), `:4180-4194` (converge), `:2483-2487` (role 3 stays expand while harvesters < 4), `:3895-3945` (defend) |
| counterbattery waiver is permanently open once the Core is shelled | source read, `:3748-3764`; `_core_shelled` at `:3516-3535` |
| latch decay needs 50 quiet rounds | source read, `:1857-1869` |
| probe's launcher at (4,5) never dies; wild CAD built none in the archived seat-B game | replay `RemoveEntity` scan over the full match, both files |
| archived wild-CAD gate-map games and their first-harvester/first-delivery rounds | `replay_archive/*.meta.json` name match + map decode; instrumented with the builder arm's `instr.py` `parse_game` |
| the `d <= 16` trigger and the CB waiver both predate the wild archive games | source grep in `bots/opp_v72/74/76/78/main.py` and `bots/_v89sh/main.py:3336` |
| pool map anchor/footprint distance table | arithmetic over all 15 `maps/*.map26` core positions |
| `ECO_CAP = 18`, surge 24 at ≥1500 Ti / ≥r300 | source read, `:26`, `:398-401`, `_eco_cap:3161-3171` |
| heart late-collapse mechanism | **source-derived hypothesis only — no heart replay decoded.** Flagged as medium confidence with an explicit refutation test. |

**Scope note.** This is a research-arm note: no bot file was edited, no arena run,
no platform contact. The only file written is this one. All measurements come from
the builder arm's existing 72-game bundle plus read-only decodes of
`replay_archive/` and `maps/`.

---

## Addendum — 2026-08-08 17:1x: FB v1 battery refines the fix implications

Builder-measured (arm_fb byte-reproduced arm_w 24/24, fboff identity
24/24 — harness clean, the v1 fix never fired): on fjordgate-B the bank
cycles 0→10→6→2→0 from ~r10 onward — the heal line (~4 Ti/r) plus the
ammo trickle outspend the 2.5 Ti/r passive income, so no money gate ever
sees harvester cost again. **Option B as a gate *exemption* is therefore
insufficient: it must be an ACCUMULATION floor** (siege spenders barred
from spending the bank below harvester cost while harv==0), which is FB
v2's shape. This also refines this doc's wb reading: wb's reserve fix
held the bank up, which is *why* the 36-Ti reserve was the binding
constraint in that arm — in the unfixed w arm the binding constraint is
upstream total insolvency. The gate-stack analysis (Q2) stands; the
binding-order statement is arm-dependent. Still open builder-side: the
r1-8 opening non-build at bank 50-454 (pre-insolvency) — expander
walk-time hypothesis, possibly the same link machinery as the meander
read's Q1.
