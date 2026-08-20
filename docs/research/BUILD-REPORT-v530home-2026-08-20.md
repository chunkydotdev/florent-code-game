# BUILD REPORT — `bots/_v530home`, s51, 2026-08-20

**THE HOME-DEFENCE PACKAGE.** Three Magnus-designed planks plus one mid-build
candidate, all pointed at **our own core ground** — which the parent line
defends with nothing at all. The s51 replay study measured our buildings on our
own 12-tile ring across 80 modern rated games: **565 conveyors, 20 launchers,
9 sentinels, 8 gunners and 0 barriers**, against **528 barriers on THEIRS**
(`docs/research/REPLAY-STUDY-notadgato-v23-2026-08-20.md` §2). The collar
doctrine exists, is correct, and is pointed only outward.

Parent `bots/_v529merge`. Tree **uncommitted**, per instruction. `PAR=4`
throughout; PIDs in `scratchpad/s51_v530_build/PIDS`. `scratchpad/overnight*`
and `corefill_forever.sh` were **not touched**. Wall clock from `date -u` in the
same shell call: freeze `06:14:16Z`, tree final `06:21:01Z`, byte-identity +
dose `06:21:07Z`, headline `06:25:46Z`.

---

## ⛔ TOP LINE — FOUR SENTENCES

1. **THE PRIMARY MECHANISM IS VERIFIED, DECISIVELY, ON THE EXACT FIXTURE IT WAS
   DESIGNED FROM.** Against the ring-claimer `_x3r0v165mjolnirB` on the
   crater-oversampled panel, the race margin `eseal₁ − head1` flips from
   **−14.0 to +21.1**, the socket race is won in **75.0%** of games against
   36.0%, and **the dead-heads class dies: games in which our belt NEVER reaches
   a core-ring socket fall from 36.7% to 9.4% — and to 0.0% in the ring form,
   on 5 of 5 crater maps.** icefloe's socket claim moves from **r123.8 to r6.0**.
2. **AND THE CURRENCY SAYS NO, ON BOTH BATTERIES, OUTSIDE EVERY INTERVAL.**
   `DEFENCE_ADMISSION_BAR` (ITT, share of ALL games killed by r300) reads
   **0.537 → 0.358 (−17.92 ± 6.29)** vs `_v488beltbreak2` and **0.338 → 0.156
   (−18.13 ± 5.46)** vs `_x3r0v165mjolnirB`, against a known-zero arm moving
   −0.83 and +1.25 on the same column. **Two opponents, same sign, same
   magnitude, both excluding zero. The bar is breached, not merely uncleared.**
3. **THE CAUSE IS DIAGNOSED AND IT IS AN IMPLEMENTATION TAIL, NOT THE DESIGN.**
   The median first harvester moves **r5 → r8**, which is the +3 rounds the
   design predicted in writing beforehand. The MEAN moves **r5.79 → r42.74**,
   and the gap between those two numbers is the whole finding: **in 9.6% of
   games this tree builds no harvester at all** (parent: 0.0%) and in 15.4% the
   first one lands after r60. §11 names the suspect line and the cheap test.
4. **DO NOT SHIP `_v530home` AS FIRED.** P1 is a good trade priced wrong; P2
   fires, costs nothing measurable (our own spawns went *up*, 5.93 → 6.34) and
   has no measured benefit on either local opponent; P3 works on a fixture built
   for it (**a launcher at our door lives a median 28 rounds against the parent
   and 7 against the rule, with a clean zero-moved control on out-of-band
   launchers**) and gets no dose from real opponents. The candidate `ring`
   (`FS_V530_RING`, shipped OFF) is the only arm in the build that **gained**
   win rate — **+4.38 pp ± 6.33 on the crater panel, inside its own interval** —
   while killing latest of all (medkill 329 vs 208). Recorded as a lead.

⛔ **AND ONE ENGINE FINDING THAT OUTLIVES THIS BUILD (§3.2): CONVEYORS ARE NOT
BOT-PASSABLE — `can_move` and `is_tile_passable` both read False on a tile
holding our own conveyor, 18/18 with a same-round control — WHICH IS THE
OPPOSITE OF WHAT `doctrine.py:599-616` SAYS AND USES AS THE REASON
`HS_SEAT_BAN_CONVEYORS = False` SHIPS.** Flagged, not resolved, per instruction.

---

## 0. WHAT SHIPPED, AND WHAT DID NOT

| flag | state | what it is |
|---|---|---|
| `FS_V530_MOUTH` | **True** | **P1, the primary.** The trunk belt is laid CORE-OUTWARD: link 1 on a delivery socket of our own core at r1-3, each further link extending toward the v528-chosen ore and facing back along the chain, the harvester built LAST at the far end. |
| `FS_V530_CORNERS` | **True** | **P2.** Barriers on the 4 diagonal corners of our own core ring (`V530_CORNER_KEEP = 1` leaves one open), inside r2–r120. |
| `FS_V530_DOORKILL` | **True** | **P3.** An enemy LAUNCHER within d² ≤ 40 of our own core footprint is the top target for our home turrets — a ladder promotion for sentinels plus a pre-empt clause for gunners. |
| `FS_V530_RING` | **False** | **P1b, the candidate.** Conveyors on ALL 8 orthogonal sockets, each facing the footprint, so every one is a mouth. Ships OFF and is measured as its own arm. |
| `FS_V530_LOG` | False | stderr instrument tapes; the instrumented arms set it. |
| `LOKI_FS_V530` | True | master. False reproduces `_v529merge` exactly. |
| `FS_HOME_TURRET_RESPONSE` | **True, UNTOUCHED** | the parent's value. |
| `FS_V515_DOOR_OFF` | **True, UNTOUCHED** | the parent's value. **The v513 builder door-peck path stays exactly as shut as it is in the parent** — P3 reuses the DETECTION SHAPE of `_door_turret` and nothing else. |

**Why P1b ships OFF rather than ON-with-an-ablation.** Magnus, direct: *"an idea
we could try, not sure its worth it."* The primary read of this build is the
MOUTH, and a candidate that turns out to cost opening tempo would contaminate
the arm the mouth is read on. A default of False makes the ring an **increment
measured against the package**, which is the question actually asked.

**Files touched:** `doctrine.py` (one appended v530 block), `eco.py` (P1, P1b,
P2), `main.py` (per-unit state + P3). `raid.py` and `siege.py` are
**byte-identical to the parent**.

```
PARENT  _v529merge  doctrine 95e46641  eco 91cd121a  main 93a85f57  raid 3b3a0456  siege 0ee5bb2d
CHILD   _v530home   doctrine 92ead92c  eco 88f4cb30  main 5af34cc1  raid 3b3a0456  siege 0ee5bb2d
                             ^^new blk  ^^P1/P1b/P2  ^^state+P3    ^^unchanged   ^^unchanged
```

---

## 1. VERIFY-FIRST (1) — FLAG-OFF BYTE-IDENTITY **20/20**, PLUS THE SUB-FLAG STANDDOWN

`byte_identity.py`; `NOISE_ON = False` on **both** sides (opponent copy `eq_opp`
differs from `bots/_v488beltbreak2` by that one line), `--tle 0`, seed 530820,
replay **bytes** compared. 10 maps × 2 seats.

```
A1  eq_off  (master False)          vs eq_parent  IDENTICAL 20/20  PASS  <- the known zero
A2  eq_v530 (as fired)              vs eq_parent  DIFFERS   10/10  PASS  <- negative control
A3  eq_sub  (master TRUE, all three
             sub-flags False)       vs eq_parent  IDENTICAL 20/20  PASS  <- standdown
A4  eq_sub                          vs eq_v530    DIFFERS   10/10  PASS  <- negative control for A3
TRACEBACKS 0                                                        RESULT: PASS
```

**A2 and A4 are why A1 and A3 mean anything.** A flag-off identity is also
satisfied by a tree that does nothing at all; the negative controls are what
make the identity a statement about the flag rather than about the code being
inert. **A3 is the one that licenses every per-plank ablation below**: with the
master True and all three sub-flags False the tree is still byte-identical to
the parent, so neither the master nor any shared scaffolding does anything on
its own.

## 2. VERIFY-FIRST (2) — AST DERIVED-DEFAULT SCAN: **0**, WITH ITS POSITIVE CONTROL

```
GUARD: pos=True neg=False if=True         (all three exercised on the V530 name set)
doctrine.py 0 · eco.py 0 · main.py 0 · siege.py 0 · raid.py 0
  (v530 AND every inherited set v518–v528)
REAL-CASE CONTROL (FERRY_HOME_ON reads FS_CREW_ON, the known v515 hazard): 2 found
TOTAL derived-default hits: 0             RESULT: PASS
```

Every v530 flag is read at its point of use as `LOKI_FS_V530 and FS_V530_<X>`;
nothing is folded into a module-level default, and `mkarm.sh` edits in place at
the definition site rather than appending. The FERRY_HOME_ON pair is the
positive control: the scanner still sees the real defect class.

---

## 3. TWO ENGINE PROBES, AND ONE OF THEM CONTRADICTS SHIPPED DOCTRINE

Both planks P1 and P1b put a conveyor on a tile that is also a core **heal
seat**, and Magnus asked explicitly whether that is safe and whether a conveyor
blocks a gunner ray. Neither question is answerable from a document, so both
were measured on the engine.

### 3.1 ⭐ A CONVEYOR **DOES** BLOCK A GUNNER RAY — 16/16, with both controls

`bots/_probe_convray`. One builder, one straight EAST line. It builds the far
target, backs up one tile so the target sits at d = 2, then reads the engine's
own hypothetical-turret predicate with the middle tile empty / conveyor /
barrier.

```
PHASE0  clear line, target at d=2         can_fire_from = True   22 of 23 cells
PHASE1  OUR CONVEYOR at d=1               can_fire_from = False  16 of 16 cells
PHASE2  OUR BARRIER  at d=1  (POS. CTRL)  can_fire_from = False  10 of 10 cells
```

⇒ **A conveyor is an obstacle to a gunner ray exactly as a barrier is.** So the
ring form (P1b) buys ray denial on top of its acceptor value, and even the
single mouth conveyor of P1 denies one line.

⛔ **THE FIRST VERSION OF THIS PROBE WAS WRONG AND THE ERROR IS RECORDED RATHER
THAN DELETED.** It read `can_fire_from` down an EMPTY line and got False at
every distance, which *looks* like "blocked" and is not: **the predicate requires
an OCCUPANT on the target tile**, and it went True the moment any building stood
there — **including one of our own**. A probe that never plants a far target
measures nothing. PHASE0 exists so that a False in PHASE1 cannot be a probe that
never had a shot; PHASE2 exists because a check that has never returned the
other verdict has not been seen to check. *(1 of 23 PHASE0 cells read False — a
cell where the far target build did not land; reported, not smoothed.)*

### 3.2 ⛔⛔ CONVEYORS ARE **NOT** BOT-PASSABLE — 18/18 — AND `doctrine.py:599-616` SAYS THEY ARE

`bots/_probe_healseat`. The shipped doctrine states, and uses as the stated
reason for `HS_SEAT_BAN_CONVEYORS = False`:

> *"Conveyors and Splitters are BOT-PASSABLE in this engine… So a PAVED seat
> does not actually deny a healer the seat — a builder can stand on the conveyor
> and heal. Only a Harvester, a Barrier or a turret on a seat blocks it
> permanently."*

Measured, with the control **inline in the same round** (every row reports
`can_move` and `is_tile_passable` for all four cardinal neighbours at once):

```
tile holding OUR OWN CONVEYOR     can_move = False   is_tile_passable = False   18 of 18
empty neighbour, same rows        can_move = True    is_tile_passable = True    28 reads
                                  (and every one of the 18 rows contains at least one True)
```

⇒ **A paved seat DOES deny a healer that seat.** The inline control is what
makes this a finding rather than "this body could not move at all this round" —
in all 18 rows some other neighbour was legal in the same call.

**WHAT THIS DOES AND DOES NOT CHANGE FOR THIS BUILD:**
* **P1 (shipped):** the mouth takes **one** of the 8 seats, and takes it at
  r2–r3 instead of r8–r97. The parent paves seats too — `_pave_ban()` returns
  `None` because `HS_SEAT_BAN_CONVEYORS = False`, so all 8 are legal conveyor
  goals in both trees. **The delta is TIMING, not COUNT.**
* **P1b (candidate, OFF):** this is a serious hazard and it is the strongest
  single argument for the flag's default. The ring paves **all 8** seats;
  `_free_seats` (eco.py:455) filters on `is_tile_passable`, so it would return
  **empty**, `_seat_seek_target` would return None, and the multi-healer
  convergence would have nowhere to stand. The ring arm's own measured claim
  (§4) is ~6 of 8 sockets paved by r30.
* **⛔ NOT RESOLVED HERE, BY INSTRUCTION.** This is flagged for the next builder,
  not fixed: the doctrine sentence and the engine disagree, and which one is
  right today changes the price of `HS_SEAT_BAN_CONVEYORS`, of the ring, and of
  the incumbent's own 483 ring conveyors. Re-run `bots/_probe_healseat` before
  spending anything on the strength of either.

**One unexplained secondary, reported because it is exactly the asymmetric-guard
shape this project hunts:** the same probe repeatedly observed a **builder bot
standing on a tile that held a conveyor** (`standing_on=CONVEYOR` at a core
seat) even though `can_move` onto such a tile reads False. Occupancy by some
other route — spawn, or a throw — appears not to apply the check that movement
does. Not chased further in this build; recorded as an open item.

---

## 4. VERIFY-FIRST (3) — DOES EACH PLANK FIRE, AND DOES ITS OWN ABLATION KILL IT?

8 maps × 3 seeds × 2 seats = **48 games/arm, 288 games, 0 tracebacks**,
`NOISE_ON = True`, `--tle 10`, stderr kept. ⚠ `NOISE_ON = True` re-rolls the
spawn salt per process, so these are **magnitudes, not constants**. Every arm is
**the same tree with one flag moved**, so the tape comes from one instrument.
Reader: `doseread.py` (`--selftest` drives every counter to both verdicts and
asserts they are not aliases of one another).

```
arm            games  Marm  Mlink  Mharv  Mttl  CORNER  DOORKILL   RING | sock_med harv_med chain_md | tb
inst_v530         48   116    480     39    63     132         5      0 |        4        9        3 |  0
inst_nomouth      48     0      0      0     0     123         5      0 |       -1       -1       -1 |  0   <- P1 off
inst_nocorner     48   128    569     44    77       0         0      0 |        3        9        3 |  0   <- P2 off
inst_nodoor       48   120    461     39    61     132         0      0 |        4        9        2 |  0   <- P3 off
inst_ring         48   120    408     38    67     134         0    201 |        3        9        2 |  0   <- P1b ON
inst_flagoff      48     0      0      0     0       0         0      0 |       -1       -1       -1 |  0   <- master off
```

**Every ablation drives its own counter to exactly zero and leaves the others
alone**, and the master drives all of them to zero. `RING` is 201 in the one arm
that turns it on and **0 in the fired tree**, which is the flag's default doing
what it says.

⛔ **THE FIRST DOSE FOUND A REAL DEFECT AND IT IS RECORDED, NOT SMOOTHED.** Run
before the fix, the same tape read **117 chains armed, 453 links laid, 22
terminal harvesters, 61 TTL abandonments.** Cause: the parent's own chain
planner and harvester bootstrap were still reachable while a mouth chain was
live, so the parent built a harvester on an adjacent ore, `_wire_on_build`
queued a SECOND chain into `link_queue`, and that queue was never walked because
the mouth mover owned the body's move. The fix is the `_v530_mouth_live()`
predicate that makes the two planners mutually exclusive, plus the removal of a
movement HOLD that parked a body beside its ore for as long as the harvester cap
refused the spend. **Without the dose this would have shipped, and the headline
below would have been read as the plank's price rather than as a bug's.**

---

## 5. THE HEADLINE — BATTERY A, n=480/arm, 3,360 games, 0 tracebacks

7 arms interleaved per cell, the same 8-map panel v526–v529 used
(`atoll drakkarfjord glacierkeep nordkap yulerune antler fjordgate midgard`),
15 blocks × 2 seeds × 2 seats, `PAR=4`, opponent `bots/_v488beltbreak2`.
`flagoff` is the tree with the master False, proved byte-identical to `parent`
on 20/20 cells — so **every flagoff-vs-parent number is pure fixture spread and
is the yardstick**.

### 5.1 THE KILL_TARGET PANEL

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   76.5%  129(.269)  164(.342)  186(.388)  229(.477)  258(.537)     190     103   0
flagoff       480   75.6%  116(.242)  159(.331)  185(.385)  224(.467)  254(.529)     185     111   0
v530          480   66.7%   46(.096)   66(.138)   90(.188)  138(.287)  172(.358)     264     126   0
nomouth       480   68.1%  114(.237)  140(.292)  163(.340)  198(.412)  224(.467)     193     143   0
nocorner      480   68.3%   41(.085)   67(.140)   89(.185)  137(.285)  186(.388)     272     130   0
nodoor        480   63.5%   43(.090)   66(.138)   91(.190)  137(.285)  166(.346)     254     141   0
ring          480   67.7%   39(.081)   71(.148)   96(.200)  156(.325)  195(.406)     245     118   0
```

| arm | Δwins | Δk≤200 | Δk≤300 (ITT) | known-zero on the same column |
|---|---|---|---|---|
| **v530** | **−9.79 pp** | **−20.00 pp** | **−17.92 pp** | −0.83 / −0.21 / −0.83 |
| nomouth | −8.33 | −4.79 *(inside)* | −7.08 | " |
| nocorner | −8.12 | −20.21 | −15.00 | " |
| nodoor | −12.92 | −19.79 | −19.17 | " |
| ring | −8.75 | −18.75 | −13.12 | " |

Half-widths 5.4–6.3 pp; every cell marked above is OUTSIDE except the one
labelled.

### 5.2 ⛔ `DEFENCE_ADMISSION_BAR` — **BREACHED, AND NOT NARROWLY**

The registered read is ITT: the share of **ALL** games ending in a core kill by
r300 must not FALL vs control.

```
parent 0.537  ->  v530 0.358      delta = -17.92 pp,  hw 6.29
```

Restated as the exclusion the correction requires (CLAUDE.md: a fail-to-exclude
claim must be restated before DEFF is applied — not applicable here since this
is a LOCAL fixture with a measured pair-weighted DEFF of 0.98, so naive
half-widths stand): **the 95% band is roughly [−24.2, −11.6] pp and excludes
zero.** The bar is not "not cleared"; it is **breached by three half-widths**.
`nomouth` also breaches, at −7.08 ± 6.33, marginally.

⇒ **`PLAY_DEFENCE: not_at_the_kill_s_expense` disqualifies this package in its
fired configuration.** The number is the verdict; §5.3 is why.

### 5.3 ⭐⭐ THE MECHANISM WORKED. THE ECONOMY IT WAS BUILT FOR DID NOT SURVIVE IT.

Read off the research arm's own `routetape.py` (winner-vs-tape **3,360/3,360
agree, 0 parse failures**), the same instrument the crater autopsy was measured
on:

| column | parent | flagoff (known zero) | **v530** | ring |
|---|---|---|---|---|
| `head1` — first round a conveyor OF OURS stands on one of our 8 sockets (mean) | 13.2 | 14.3 | **5.2** | **2.0** |
| `head1` median | 6 | 6 | **3** | **2** |
| **won the socket race** (ours before theirs) | 0.821 | 0.821 | **0.990** | **1.000** |
| **belt NEVER reaches a socket** — the dead-heads class | 0.025 | 0.027 | **0.000** | **0.000** |
| our conveyors on our own 8 sockets @r30 | 1.85 | 1.85 | 2.37 | **5.22** |

**P1 does precisely what it was designed to do.** The socket is claimed at a
median r3 instead of r6, the race is won in 990 of 1,000 games instead of 821,
and **the dead-heads class is gone by construction: 0 of 480 games in which the
belt never reaches home, against 12 of 480 for the parent.** P1b takes it
further — r2, 1,000 of 1,000, 5.2 of 8 sockets held at r30.

**AND THE ECONOMY COLLAPSES ANYWAY, IN A TAIL:**

| column | parent | **v530** | ring |
|---|---|---|---|
| first harvester, **median** round | 5 | **8** | 8 |
| first harvester, **mean** round | 5.79 | **42.74** | 42.23 |
| games with **NO harvester ever** | **0.000** | **0.096** | 0.119 |
| games with first harvester **after r60** | **0.000** | **0.154** | 0.094 |
| live harvesters @r30 | 2.32 | 1.46 | 1.37 |
| **`titanium_collected` = 0 at r100** | **0.033** | **0.281** | 0.194 |
| `titanium_collected` @r100 (mean) | 379 | 249 | 253 |

⇒ **The median cost is +3 rounds — exactly the price the design predicted and
wrote down before the battery. The mean cost is +37 rounds, and the difference
between those two numbers IS the finding: a TAIL of roughly a quarter of games
in which the harvester economy never starts at all.** In 9.6% of games this bot
builds no harvester for the entire match; the parent does that in 0.0%.

**That tail is what buys the −20 pp on timely kills.** It is not the ordering
inversion, which is cheap and works; it is a residual defect in how the
mouth-first body hands back to the parent's economy when its own chain does not
complete. The v530 dose still shows **63 TTL abandonments against 39 terminal
harvesters** — the same shape at a smaller scale, after the §4 fix already
removed a factor of two of it.

**⇒ THE ROAD IS NOT CLOSED, THE IMPLEMENTATION IS.** A plank that converts
`beltfail 2.5% -> 0.0%` and `head1 r6 -> r3` for **three median rounds** is a
good trade. This build does not get to claim it, because it also converts
`no-harvester-ever 0.0% -> 9.6%`.

---

## 6. BATTERY B — THE CRATER-CLASS TEST, vs `bots/_x3r0v165mjolnirB`

n=480/arm, 2,400 games, 0 tracebacks. 5 arms, crater-oversampled panel
(`icefloe auroraveil glacierkeep yulerune drakkarfjord` + `ragnarok royale
nordkap` as sweep controls). This is the fixture the defect fires on: the s51
autopsy measured this opponent standing on one of OUR 8 sockets at **r7.2**
against our belt head at **r80.6**, with `titanium_collected` at r100 = **0 in
60/60 icefloe games**.

### 6.1 ⭐⭐ THE DEAD-HEADS CLASS DIES. THIS IS THE STRONGEST RESULT IN THE BUILD.

`beltfail` = games in which **no conveyor of ours ever reaches a core-ring
socket**, per map (60 games each). `head1` = mean round our socket is claimed,
over the games where it ever is.

| map | parent beltfail | **v530** | **ring** | parent head1 | **v530 head1** | **ring head1** |
|---|---|---|---|---|---|---|
| **icefloe** | **0.45** | **0.00** | **0.00** | 123.8 | **6.0** | **2.0** |
| **yulerune** | **0.70** | **0.00** | **0.00** | 107.9 | **2.0** | **2.0** |
| **drakkarfjord** | **0.48** | **0.00** | **0.00** | 28.4 | **9.0** | **2.0** |
| auroraveil | 0.43 | 0.35 | **0.00** | 38.6 | 26.4 | **2.0** |
| glacierkeep | 0.87 | 0.40 | **0.00** | 286.1 | 46.5 | **2.0** |
| nordkap / ragnarok / royale (controls) | 0.00 | 0.00 | 0.00 | 9.4 / 4.5 / 14.0 | 3.1 / 8.0 / 3.6 | 2.0 / 3.0 / 2.0 |

Pooled over the panel:

| | parent | flagoff (known zero) | **v530** | **ring** |
|---|---|---|---|---|
| `head1` mean | 40.1 | 33.9 | **10.6** | **2.1** |
| `margin` = eseal₁ − head1 | **−14.0** | −3.1 | **+21.1** | **+23.9** |
| won the socket race | 0.360 | 0.367 | **0.750** | **1.000** |
| **belt never reaches home** | **0.367** | 0.381 | **0.094** | **0.000** |

**The autopsy's whole diagnosis is inverted by construction.** The race margin
flips from −14.0 to +21.1; the belt-fail rate falls from 36.7% to 9.4% (mouth)
and to **0.0%** (ring); icefloe's socket claim moves from r123.8 to r6.0.
**`P1` and `P1b` do exactly and verifiably what they were designed to do, on the
exact fixture the design was derived from.**

⚠ v530's residual 35–40% belt-fail on auroraveil and glacierkeep is the two
DEEPEST-ore maps in the pool (`ore_d1` 8 and 11): a 8–11 link chain is ~20+
rounds of one body's actions and often meets `V530_MOUTH_TTL`. The ring form,
which pays no chain, is 0.00 on both.

### 6.2 AND THE CURRENCY SAYS NO, ON THIS BATTERY TOO

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   48.3%   41(.085)   77(.160)  110(.229)  143(.298)  162(.338)     208     208   0
flagoff       480   48.5%   42(.087)   72(.150)  101(.210)  139(.290)  168(.350)     218     213   0
v530          480   44.6%    0(.000)   14(.029)   26(.054)   41(.085)   75(.156)     337     234   0
nomouth       480   46.9%   69(.144)   78(.163)   88(.183)  118(.246)  134(.279)     237     226   0
ring          480   52.7%   30(.062)   42(.087)   47(.098)   72(.150)  100(.208)     329     189   0
```

| arm | Δwins | Δk≤200 | **Δk≤300 (the BAR)** |
|---|---|---|---|
| v530 | −3.75 *(inside, hw 6.31)* | **−17.50** | **−18.13** (hw 5.46) |
| nomouth | −1.46 *(inside)* | −4.58 *(inside)* | −5.83 *(inside)* |
| **ring** | **+4.38** *(inside, hw 6.33)* | **−13.12** | **−12.92** (hw 5.64) |

⛔ **`DEFENCE_ADMISSION_BAR` BREACHED ON BOTH BATTERIES**: A −17.92 ± 6.29,
B −18.13 ± 5.46. Two independent opponents, same sign, same magnitude, both
excluding zero.

⭐ **AND ONE GENUINE SURPRISE, WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY: the RING
arm is the only arm in either battery that GAINS win rate — +4.38 pp on the
crater panel, and it takes 19 fewer of our own core deaths (189 vs 208).** It is
also the arm with the slowest kills in the whole build (medkill 329 vs 208).
Under `R1000_IS_DEFEAT` and the amended `PLAY_DEFENCE` clause that is not a
ship — a plank that buys wins by surviving longer is buying the currency we
retired. But it is the second time this project has measured a home-defence
change reading as a real positive on wins (s30: `home-turrets-off` 433/1024 and
`barrier-seal-off` 399/1024 were both real negatives, i.e. removing home defence
COST us), and it is +4.38 ± 6.33, i.e. **inside its own interval and not a
claim**. Recorded as a lead, not a finding.

---

## 7. P3 — THE DOOR-LAUNCHER KILL, MEASURED ON A FIXTURE BUILT FOR IT

⛔ **THE LADDER OPPONENTS DO NOT SUPPLY THE DOSE.** Across battery A's 3,360
games the whole-battery census found **5 door launchers for the parent and 18
for v530** — a rule whose dose is single digits cannot be verified on that
fixture, and saying so is the honest first result.

So the event was manufactured: `bots/_probe_doorlaunch` walks builders at the
opponent's core and plants LAUNCHERS on the tiles around it (plus one ranged
gunner, so that our own home counter-battery actually builds the turret the rule
is a rule FOR — without incoming fire the instrument would never be present).
**FIXTURE, NOT AN OPPONENT, AND IT LIES IN A KNOWN DIRECTION:** it plants far
more door launchers than any real bot and defends none of them, so only
mechanical claims can be read off it.

64 games/arm, opponent pinned to the probe, read off the WIRE
(`doorcensus.py`, placeEntity/removeEntity — never off our own stdout):

| arm | door launchers | died | **median life** | mean life | **killed ≤6 rounds** |
|---|---|---|---|---|---|
| **nodoor** (P3 off) | 201 | 27 | **28** | 52.0 | **6** |
| **v530** (P3 on) | 223 | 39 | **7** | 24.4 | **19** |
| — *within-game control* — | | | | | |
| nodoor, launchers OUTSIDE the band | 22 | **0** | −1 | −1 | 0 |
| v530, launchers OUTSIDE the band | 21 | **0** | −1 | −1 | 0 |

⇒ **A launcher that puts itself at our door lives a median 28 rounds against the
parent's targeting and 7 rounds against P3's — and the number killed inside 6
rounds of appearing triples, 6 → 19.** The FAR cell is the control that makes
this a TARGETING result rather than a "we kill more of everything" result: zero
out-of-band launchers died in either arm, so nothing moved except the cell the
rule names.

**What P3 is NOT shown to do:** change any currency column. Its ablation
(`nodoor`) is the worst arm in battery A on wins (63.5% vs v530's 66.7%), which
is +3.2 pp in P3's favour — **inside the 5.8 pp half-width, and therefore not a
claim.** P3 is a verified mechanism with no measured currency effect, on a dose
the real opponents do not supply.

---

## 8. P2 — CORNER BARRIERS: THE PLANK FIRED, THE FEARED COST DID NOT MATERIALISE, THE BENEFIT IS UNMEASURED

**Fires:** 132 corner barriers / 48 dose games (≈2.75/game, consistent with
`V530_CORNER_KEEP = 1` leaving one corner open); 0 in the `nocorner` and
`flagoff` arms.

**The cost that was flagged before the battery — self-spawn denial — did not
appear.** Our own 12 ring tiles are also our 12 spawn tiles, and P2 takes three
of the four corners. Measured:

| | parent | v530 | nocorner |
|---|---|---|---|
| our builder spawns, whole game (battery A) | 5.93 | **6.34** | 6.37 |
| our builder spawns by r30 | 4.90 | **5.09** | 5.08 |

**Spawns go UP, not down.** The hedge was not needed at `KEEP = 1`; whether it
would be needed at `KEEP = 0` is untested.

**The benefit is NOT measured by this build.** The mechanism claim is the
`notadgato` §2 finding — 44 of their 88 ring gunners were built on corners, and
26.6% of all core damage we take is gunner fire from the 12 ring tiles — and
that is a claim about **a ladder opponent's** behaviour. Neither local opponent
builds gunners on our corners at a rate that would register. §3.1's engine probe
does establish the ray half (a conveyor, and by the same test a barrier, blocks
a gunner line), but **the denial half is inference from someone else's replay
corpus and is not tested here.** `v530 − nocorner` on wins is −1.6 pp, hw 5.7 —
no reading.

---

## 9. DOCTRINE COLLISIONS — FLAGGED, NOT RESOLVED

Per instruction: reported for the next builder to arbitrate, not fixed here.

1. **⛔⛔ `doctrine.py:599-616` IS CONTRADICTED BY THE ENGINE (§3.2).** It states
   conveyors are bot-passable and that a paved heal seat therefore does not deny
   a healer; measured, a tile holding our own conveyor reads `can_move = False`
   and `is_tile_passable = False` in **18/18** cells with a same-round control.
   That sentence is the stated reason `HS_SEAT_BAN_CONVEYORS = False` ships, and
   it prices the incumbent's own 483 ring conveyors as well as P1 and P1b.
   **Nothing in this build was changed on the strength of either reading.**
2. **The mouth conveyor takes a heal seat EARLIER than the parent's does.** Both
   trees pave sockets — `_pave_ban()` returns `None` in both — so the delta is
   timing (median r3 vs r6), not count. Under finding 1 that is one seat lost to
   healers from r3. Under the doctrine's version it costs nothing. **The two
   readings differ and this build does not adjudicate.**
3. **P1b would pave ALL EIGHT.** `_free_seats` (`eco.py:455`) filters on
   `is_tile_passable`; under finding 1 the ring arm would leave the multi-healer
   convergence with nowhere to stand. Measured claim in that arm: **5.22 of 8
   sockets held at r30 (battery A), 3.35 (battery B)**. This is the strongest
   single argument for `FS_V530_RING = False` and is independent of the currency
   result.
4. **`V530_DOOR_DSQ = 40` deliberately equals `FS_DOOR_DSQ` (doctrine.py:2654)**
   so the tree's two "door" definitions cannot drift. `HUNT_BAND_DSQ = 41` is a
   third, neighbouring, un-unified one. Not merged here.
5. **Unexplained engine asymmetry (§3.2 tail):** a builder was repeatedly
   observed OCCUPYING a tile that held a conveyor, while `can_move` onto such a
   tile reads False. Occupancy by spawn or throw appears not to apply the check
   movement does. This is the asymmetric-guard shape the LOKI brief hunts;
   recorded, not chased.

---

## 10. FAILURE REEL

Selection rule (house convention, stated before looking): the **earliest
our-core-death on each map**, for the `v530` arm, across the whole battery; ties
by lowest seed then seat A; capped at 5 rows. One per map is what stops the reel
being five copies of one board.

**BATTERY A** (vs `_v488beltbreak2`) — deaths 126 of 480 (26.2%), r1000 games 60:

| map | turn | seed | seat | replay |
|---|---|---|---|---|
| antler | 96 | 8 | A | `headA/rep/v530_antler_s8_A.replay26` |
| atoll | 118 | 19 | B | `headA/rep/v530_atoll_s19_B.replay26` |
| fjordgate | 131 | 22 | B | `headA/rep/v530_fjordgate_s22_B.replay26` |
| midgard | 192 | 24 | A | `headA/rep/v530_midgard_s24_A.replay26` |
| yulerune | 202 | 28 | A | `headA/rep/v530_yulerune_s28_A.replay26` |

**BATTERY B** (vs `_x3r0v165mjolnirB`) — deaths 234 of 480 (48.8%), r1000 41:

| map | turn | seed | seat | replay |
|---|---|---|---|---|
| nordkap | 105 | 21 | B | `headB/rep/v530_nordkap_s21_B.replay26` |
| auroraveil | 125 | 6 | A | `headB/rep/v530_auroraveil_s6_A.replay26` |
| ragnarok | 145 | 1 | A | `headB/rep/v530_ragnarok_s1_A.replay26` |
| drakkarfjord | 160 | 4 | A | `headB/rep/v530_drakkarfjord_s4_A.replay26` |
| yulerune | 168 | 7 | B | `headB/rep/v530_yulerune_s7_B.replay26` |

Labelled extension, NOT part of the reel — the other tail, which is the one the
kill-round bar binds on: latest-kill WINS are `midgard s14 B r901` and
`glacierkeep s13 B r794` (battery A), `glacierkeep s9 A r946` and `royale s5 B
r923` (battery B).

⚠ **auroraveil is where the reel and the panel agree:** v530 wins **4/60** there
against the parent's 17/60, and it is one of the two maps where the mouth chain
is long enough to meet its TTL (§6.1). If one board is worth opening a replay
on, it is that one.

---

## 11. WHAT WOULD FIX IT — for the successor, stated as tests not as conclusions

The mechanism is verified and the implementation is what fails. The
next iteration is not a redesign:

1. **THE ONE NUMBER TO MOVE IS `no-harvester-ever`, 9.6% → 0.0%.** Every currency
   loss in this build traces to it and to the 15.4% of games whose first
   harvester lands after r60. The median cost of the ordering inversion is
   **+3 rounds** and that is affordable.
2. **Suspect first:** `_v530_mouth_live()` suppresses the parent's harvester
   bootstrap on EVERY eco seat while that seat's chain is live. If all eco seats
   are in chain phase together, no harvester exists on the whole team. A cheap
   test is to exempt the FIRST harvester of the match from the suppression, or to
   let only ONE seat run mouth-first (`FS_V530_MOUTH_SEATS = False`, already a
   flag) and leave the others on the parent's order.
3. **`V530_MOUTH_MAX_LINKS = 16` is too generous on deep-ore boards.**
   auroraveil (`ore_d1` 8) and glacierkeep (11) are the only two maps where v530
   still fails the belt, and they are the two longest chains. A cap near 6, with
   the parent's order as the fallback, converts those boards back to the
   parent's behaviour at no cost to the three maps where the plank already wins
   100% of the race.
4. **P1b is the cleaner form of the same idea and should be tested as its own
   plank, not as an increment.** It achieves `head1 = 2.0` and `beltfail = 0.000`
   on **5 of 5** crater maps, pays no chain, and is the only arm in the build
   that gained win rate (+4.38 ± 6.33). It is blocked by the heal-seat question
   (§9.3), not by its own numbers — **resolve §3.2 first.**
5. **P3 needs a real dose or it stays unfalsifiable.** The rule works
   (28 → 7 rounds, with its control); no ladder opponent supplies enough door
   launchers for it to matter. Either pin an opponent that does, or accept it as
   a cheap insurance clause and stop measuring it.

---

## 12. RAW — tapes, instruments, and their selftests

**Tapes** (all under `scratchpad/s51_v530_build/`):
`headA/results.tsv` 3,360 rows · `headB/results.tsv` 2,400 · `doorfix/results.tsv`
128 · `raceA.tsv` 3,360 (routetape, winner-vs-tape **3,360/3,360 agree, 0 parse
failures**) · `raceB.tsv` 2,400 (**2,400/2,400 agree, 0 parse failures**) ·
`dose/*` 288 games of stderr · `BYTEID_OUT.txt` · `ASTSCAN_OUT.txt` ·
`CONVRAY_OUT.txt` · `HEALSEAT_OUT.txt` · `DOSE_OUT.txt` · `HEADA_OUT.txt` ·
`HEADB_OUT.txt` · `RACEA_OUT.txt` · `RACEB_OUT.txt` · `DOORFIX_OUT.txt` ·
`DOORA_OUT.txt` · `PIDS`.

**Totals: 6,224 games. 0 tracebacks, 0 timeouts, 0 no-winner games**
(3,360 headline A · 2,400 headline B · 288 dose · 128 door fixture · 40
byte-identity · 8 smoke).

**Instruments and the control each was driven to:**

| tool | what it reads | the branch that must also exist |
|---|---|---|
| `byte_identity.py` | replay BYTES, `NOISE_ON=False`, `--tle 0` | A2/A4 negative controls: the as-fired tree DIFFERS on 10/10 |
| `flagoff_ast.py` | module-level reads of any v530 name | GUARD pos/neg/if all exercised; FERRY_HOME_ON positive control returns 2 |
| `doseread.py` | the FS_V530_LOG tapes | `--selftest`: a stripped tape reads 0 on all six counters; a corner-only tape proves the counters are not aliases |
| `headline.py` | the KILL_TARGET + DELIVERY panels | `--selftest`: all-win / all-loss / mixed fold to different counters; an r300 cell is EXCLUDED not zeroed |
| `raceread.py` | folds routetape by arm | `--selftest`: a won-race game and a belt-fail game fold to opposite verdicts on every column, including the DERIVED `oconv` |
| `doorcensus.py` | placeEntity/removeEntity off the wire | `--selftest`: `dead` does not alias `existed`; the dsq band both includes (25≤40) and excludes (49>40) |
| `bots/_probe_convray` | `can_fire_from` through an obstacle | PHASE0 must read True or PHASE1's False is meaningless; PHASE2 barrier is the positive control |
| `bots/_probe_healseat` | `can_move` / `is_tile_passable` on a paved seat | the four-cardinal row is the same-round control; every one of 18 rows contains a True |
| `routetape.py` (research arm's, reused verbatim) | the socket race, belt head, delivery | its own control table, plus winner-vs-tape 5,760/5,760 here |

⛔ **`raceread.py` PRINTED A CONSTANT COLUMN AND WAS CAUGHT BY ITS OWN SELFTEST.**
Its first version reported routetape's `oseal{r}` as the ring-claim column and
read **0.00 for every arm including the one whose entire plank is a conveyor on
a socket** — `oseal` counts our NON-BELT buildings ("Ob"); our conveyors are
"Oc" and have no column. The corrected column is derived
(`homering_n − eseal − oseal − free`) and the selftest now asserts it separates
the two synthetic rows (3.00 vs 0.00). A constant column validates anything.

⛔ **NO CPU CLAIM IS MADE ANYWHERE IN THIS REPORT.** `execTimeUs` is 0 in the
local harness; the mouth planner calls `_link_path` once per body per match and
that is an argument, not a measurement.

**Local fixture, no DEFF.** The s39 audit measured a pair-weighted local DEFF of
**0.98** on a balanced-by-construction shard fixture, so the platform constants
(1.529 rated / 1.833 unrated) do not apply and are not used. Naive two-sample
half-widths throughout. **Every number in this report is LOCAL, us-vs-one-
opponent, and nothing here is a ladder read.**

---
## BUILDER VERDICT LINES (s51)
* P1 MOUTH-FIRST: DESIGN VALIDATED on the autopsy's own fixture (race −14→+21, beltfail
  36.7→9.4%, crater signature dead) — FIRED CONFIG BLOCKED by the implementation tail
  (harvester bootstrap suppressed; 9.6% zero-harvester games; §11 suspect line). v530.1
  fixes exactly that and re-runs the two batteries; nothing ships until the defence bar
  reads clean.
* P2/P3 verified (door-launcher median life 28→7 on the fixture); RING stays OFF — recorded
  as the lead it is (+4.38 wins inside interval, latest kills), pending the passability
  conflict.
* ⛔ ENGINE CONFLICT ROUTED TO RESEARCH: conveyors measured NOT bot-passable (18/18 + control)
  vs the banked corpus fact ("33.5% of throws LAND on conveyors; landing legality is
  is_tile_passable") and doctrine.py:599-616's stated basis — one of the two is wrong or the
  landing check differs from walking. Downstream stakes: heal-from-belt reasoning (Mjolnir
  sockets, heal-outrun mechanism), HS_SEAT_BAN_CONVEYORS pricing, the ring's heal-seat cost.
* ⭐ Conveyors DO block gunner rays (16/16) — banked for the ring's ledger and siting logic.

---
*⛔ DATED CORRECTION (s51, same day, live-probe half of the reconciliation): the "conveyors
are NOT bot-passable" engine finding above is RETRACTED — an instrument bug. Definitive truth
table (scratchpad/s51_convey_probe/, 8 deterministic games, barrier+empty controls both ways,
SDK docstring corroboration at fcode/_types.py:345): builders WALK ONTO and LAND ON conveyors
and splitters, OWN and ENEMY alike (6/6); is_tile_passable correctly reads False only when a
BOT already occupies the tile — the likely shape of this build's probe bug (probing occupied
tiles). Consequences: the banked 33.5%-landings fact STANDS; healers-stand-on-conveyors STANDS
(the builder's statement to Magnus needed no correction after all); the RING candidate's
heal-seat objection DISSOLVES (ring conveyors are healer-standable) while its gunner-ray
blocking (verified correctly, 16/16) stands — the ring lead strengthens. The v530 probe code's
specific defect is the reconcile doc's to name.*
