# SCREEN PREREG — `BELTSEV` / **ORESALT**: deny the one tile in this game whose function cannot be relocated

**Drafted by a fresh Opus subagent with no inherited context beyond its brief and
the inputs listed under `PROVENANCE`. The builder lane ratifies and commits.**

**STATUS: committed BEFORE the `BELTSEV` shard is appended to
`scratchpad/corefill_work.txt` and BEFORE its first heartbeat.** Two-clock
standard: this file's git author time must precede the shard's first
`BELTSEV.heartbeat` line. Drafted at `2026-08-15T05:19:16Z` (`date -u`), repo at
`6c7bc8bd`.

**PROVENANCE: `CLAUDE.md` · `QUEUE.md` (rows #7 line 462, #29 long form lines 574-600, #37 line 125, #39 line 127, #49 line 141, #54 line 139) · `docs/coordination.md` (GREPPED BY LINE, never read whole: `:10195-10260` the `_probe_denial` ore-denial engine probe, `:10652-10700` the crater-play pricing, `:10795-10830` the "refuted alone is not refuted" ruling, `:42848-42880` the SALT-family opponent-class caveat, `:52187` the `#66a` beltstall fill) · `docs/prereg/SHIP-salt-v178-2026-08-13.md` · `docs/prereg/SHIP-saltidle-v187-2026-08-13.md` · `docs/prereg/SCREEN-bodyaware-2026-08-14.md` (OB16 exemplar + format template) · `docs/prereg/SCREEN-nestshot-2026-08-14.md` · `docs/prereg/SCREEN-sealrepair-2026-08-14.md` · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (`:441-545`, OB16 + its corollary) · `tools/prereg_check.py` · `tools/overnight_pool26.sh` · `tools/replay_schema.md` · `bots/_v223sealrepair/raid.py` · `bots/_v223sealrepair/doctrine.py` · `bots/_v223sealrepair/main.py` · `bots/_v223sealrepair/eco.py` · `bots/_probe_beltstall/main.py` · `corpus/events.tsv` (the 3,995,625-row BUILD-depth cut below) · `corpus/meta_join.tsv` (`us_side`, for the our-team join) · `replay_archive/*.replay26` (the 1,338-game `ourver>=130` adjacency census below) · `tools/replay_census.py` (decoder reused, not re-implemented) · `maps/{antler,archipelago,auroraveil,drakkarfjord,drumlin,fjordgate,frostgate,glacierkeep,icefloe,midgard,nordkap,ragnarok,royale,valkyrie,yulerune}.map26` (the ore census below) · `scratchpad/corefill_work.txt` (read only). Scratch scripts for the two censuses live in the session scratchpad (`beltadj.py`, `beltattack.py`, `report.py`). No file under `bots/`, `tools/`, or any tracked path was created or modified by the drafting agent; no `fcode` command and no local game was run.**

---

## 0. ⛔ READ THIS FIRST — MAGNUS'S IDEA IS TWO IDEAS AND WE ALREADY SHIP ONE OF THEM

**The instruction:** *"Barriers could be used to peck and block conveyor paths
instead, or if we just destroy harvesters and put barriers on them instead."*
*"It also starves them."*

**Clause A — peck and block conveyor paths — IS SHIPPED, IN THE LIVE INCUMBENT,
AND HAS BEEN SINCE 2026-08-13.** `bots/_v223sealrepair/raid.py:424 _salt_turn`
is LOKI-SALT/LOKI-48. Its own docstring is Magnus's sentence:

* **(1) salt the corpse** — `raid.py:485-508`, barrier the tile a dead enemy
  conveyor/splitter vacated.
* **(2) cut** — `raid.py:510-535`, `ct.fire()` an adjacent enemy
  conveyor/splitter, lowest HP first, tie-broken toward their core because a
  conveyor has out-degree 1 (`LOKI_SALTIDLE_DOWNSTREAM`, `doctrine.py:1577`).
* **(3) deny the rebuild seat** — `raid.py:537-566`, barrier an empty tile that
  is itself adjacent to a *live* belt.
* Budgets live: `LOKI_SALT_CUT_MAX = 40` pecks/unit (`doctrine.py:1585`),
  `LOKI_SALT_MAX_PER_UNIT = 4` barriers/unit (`:1581`),
  `LOKI_SALT_BLOCK_MAX = 2` (`:1583`), `LOKI_SALTIDLE_ON = True` (`:1575`).
* It was screened four ways and SHIPPED: `SALT` 61.00% (n=5,408), `SALTCUTONLY`
  59.31% (n=1,605), `SALTNOBLOCK` 62.11% (n=1,528), `SALTIDLE` 57.83%/65.54%.

**⇒ A leg that re-tests clause A is a leg testing a feature we already ship —
the cheapest null this project knows how to buy. This document does not do
that.**

**⭐ AND IT IS NOT SHIPPED-BUT-DORMANT — IT RUNS, MEASURED ON 1,338 PLATFORM
GAMES (§6):** our builders attack an enemy conveyor in **87.1%** of games,
**96.5% of all our builder attacks land on an enemy conveyor**, we kill one in
**27.3%** of games, and we barrier the corpse in **18.2%**. **The field's
conveyor repair rate against us has fallen from the pre-salt 40.5% to 32.3%,
with our barrier winning the contested tile 66.2% of the time.** Clause A is
live and working. *(This was found independently by two instruments in this
session — a source read of `raid.py` and a blind replay census — which is why it
is stated this strongly.)*

⛔ **AND CLAUSE A CARRIES A SCAR THE SUCCESSOR MUST NOT REOPEN:** `_v178salt`
shipped it ungated and **regressed median kill round r129 → r179, Mann-Whitney
p = 0.008**, failing `DEFENCE_ADMISSION_BAR: kill_round_non_regression`. It was
revived with exactly one change — `_salt_idle_ok` (`raid.py:362`), the gate that
permits salt **only on a round the raider would have stood still**. **Any
loosening of `LOKI_SALT_CUT_MAX`, `LOKI_SALT_MAX_PER_UNIT` or that idle gate is
a re-run of the experiment that failed. This arm loosens none of them** — it
adds a target class behind its own budget, ranked below every shipped action.

**Clause B — destroy harvesters and barrier the crater — is NOT shipped, and
its BARRIER half is not shipped in any form.** That is this arm. But the arm
below is **not** what clause B literally says either, and §3 is the arithmetic
that moved it.

---

## 1. RATIFY: HYPOTHESIS

> **An ORE tile is the only denial target in this game whose FUNCTION CANNOT BE
> RELOCATED.** A cut conveyor is rebuilt one tile over for 3 Ti; a barriered ore
> tile can never host a harvester again while it stands
> (`can_build_harvester == False`, engine-probed with a destroy-and-restore
> control, `docs/coordination.md:10211-10213`), and harvesters may be built
> **only** on ore. The pool carries a **median of 8 ore tiles per side**, so one
> barrier is ~12.5% of an enemy's harvestable sites and three is ~38%.
> **Therefore: a raider that would otherwise stand still, planting ONE barrier on
> a free enemy-side ore tile, buys permanent site denial for ~11 Ti and one
> action — and their cost to undo it is 30 Ti and 15 builder-turns, because
> `destroy()` is allied-only.** The channel to the kill is that
> `titanium_collected` counts DELIVERY, delivery funds `convert_ammo` 1:1, and
> ammunition has **no other source** — fewer harvestable sites is fewer guns
> firing in the r150-250 window our own kill has to survive.

**⚠ The ammo half of that sentence is a MECHANISM STORY, not a bar.** No bar in
this document depends on it, and §9 says what would.

---

## 2. RATIFY: SEGMENT

**MAP SEGMENT: none — this arm is registered POOLED over the full 15-map pool26
array.** An ore-density split is pre-declared below as a SECONDARY read carrying
no bar, so that a post-hoc slice cannot be presented as if it had been planned
as the primary.

**ORE CENSUS — computed for this document by parsing all 15 pool maps
(`maps/*.map26`, `battlecode.Map` field 3 packed-varint tile rows, schema
`tools/replay_schema.md`). Instrument check that the parser passes on every
map: the pool is symmetric by construction, so the ore count must be EVEN — it
is, 15 of 15; and the decoded dimensions match the known geometry
(midgard 30x30, fjordgate 10x10).**

```
fjordgate    10x10  ore  6  -> 3/side      frostgate  20x20  ore 20 -> 10/side
antler       14x18  ore 12  -> 6/side      icefloe    20x20  ore 20 -> 10/side
yulerune     20x20  ore 14  -> 7/side      nordkap    20x26  ore 22 -> 11/side
auroraveil   20x20  ore 16  -> 8/side      glacierkeep30x30  ore 24 -> 12/side
drakkarfjord 30x30  ore 16  -> 8/side      ragnarok   30x30  ore 26 -> 13/side
midgard      30x30  ore 16  -> 8/side      drumlin    25x25  ore 30 -> 15/side
royale       20x20  ore 16  -> 8/side      archipelago26x26  ore 38 -> 19/side
valkyrie     30x30  ore 16  -> 8/side      MEDIAN: 8 ore tiles per side
```

**This answers LOKI-4's own pre-stated kill criterion verbatim** (*"count the ore
tiles per side on the pool maps — if a side has 12 ore tiles, denying 2 is
noise, and the agent is instructed to say so"*, `docs/coordination.md:10237`):
**the median is 8, not 12, so denying 1-3 is 12-38% of their sites and the kill
criterion is NOT met — the row survives its own abandon test.**

**SECONDARY READ, DECLARED NOW, NO BAR ATTACHED:** split the pooled share at
≤8 ore/side (fjordgate, antler, yulerune, auroraveil, drakkarfjord, midgard,
royale, valkyrie — 8 maps) vs ≥10 (7 maps). **EXPECTED DIRECTION: POSITIVE
pooled; larger on the scarce-ore half.** ⚠ **And a confound is declared with
it:** scarce-ore maps are also mostly the SMALL maps, where a raider reaches
enemy ore sooner — so a scarce-ore effect is not cleanly attributable to
scarcity. **Reported, never banked as a mechanism claim.**

**SEGMENT VALUE CEILING: 53.3% x 2.00pp = 1.07pp pooled** (share = the eight
pool maps at or below eight ore per side, equal map weight by construction;
effect = twice the registered MDE).

⭐ **THAT NUMBER IS A WARNING ABOUT THIS ARM, NOT A CLAIM FOR IT, AND IT IS WHY
THE ARM IS REGISTERED POOLED RATHER THAN SEGMENTED.** If the whole effect were
confined to the scarce-ore half at **twice** the registered MDE, the POOLED
reading would still be only **1.07pp** — barely over the +1.00pp MDE and inside
the DROP band's upper reach at any n below 10,800. **A segment-confined effect
is therefore NOT separately bankable on this fixture, and a scarce-ore slice
that reads well while the pooled share sits in the DROP band is a DROP, not a
segment win.** Registered now so it cannot be discovered later.

---

## 3. ⭐⭐ THE ARITHMETIC THAT CHANGED MAGNUS'S CLAUSE B — AND IT IS THE MOST IMPORTANT SECTION IN THIS DOCUMENT

**Clause B says: destroy the harvester, then barrier it. THE DESTROY HALF CANNOT
DOSE ON A BUILDER, AND HERE IS THE NUMBER.**

**MEASUREMENT (this document, whole-corpus, `corpus/events.tsv`, all 7,480,451
rows scanned, no sampling):**

```
kind        BUILD events   built on own side   mean d2 to own core
conveyor      3,446,888          83.7%                62.8
harvester       548,737          82.4%                66.2
splitter            710          97.5%                10.2
```

**Two facts fall out and they point opposite ways:**

1. **⭐ OCCURRENCE IS PLAUSIBLE.** Harvesters and conveyors sit at
   **indistinguishable depth** (mean d² to own core 66.2 vs 62.8; own-side share
   82.4% vs 83.7%). The raider that demonstrably reaches an enemy conveyor —
   measured, see §6 — is standing in the same territory band as enemy ore.
   **There is no reachability gap between the shipped target class and the new
   one.**
2. **⛔ BUT THE MELEE KILL CANNOT DOSE, AND THE BASE RATE IS MEASURED, NOT
   ESTIMATED.** Conveyors outnumber harvesters **6.3 : 1** (3,446,888 /
   548,737). A harvester is **30 HP = 15 pecks** against a conveyor's 20 HP = 10
   pecks. **The shipped conveyor-melee path — 40 pecks of budget, best case,
   already tuned — realises 0.40 conveyor kills per game** (§6, platform
   measurement, n = 1,338 games). Deflating that by the 6.3× rarer target and
   the 1.5× harder kill: **≈ 0.40 / 6.3 × (10/15) ≈ 0.04 harvester kills per
   game, i.e. one per ~24 games.** That is not a dose; it is chip damage.
   *(An earlier draft of this section put the ceiling at 0.14/game from an
   8-game log probe. The platform measurement is ~3× harsher and supersedes it.)*
2b. **⭐⭐ AND THE GEOMETRY CLOSES IT: THE PLACES A RAIDER CAN ACCUMULATE TEN
   CONSECUTIVE PECKS ARE PRECISELY THE PLACES WITH NO ORE.** Of the ≥10-round
   same-builder/same-target adjacency runs, **88.6% sit at d² ≤ 2 of the ENEMY
   CORE** — that is the collar siege, on ground the core occupies, not ore.
   **Only 6.1% [4.4, 7.8] of games contain a ≥10-round run that is genuinely
   midfield (d² > 25)**, which is where harvesters and ore actually are. ⇒ **a
   plank that needs a long dwell can only run at the core; a plank that needs
   ONE action can run anywhere the raider walks. This arm is the second kind,
   and that is the design's whole answer to the dwell question.**
3. **AND CHIP DAMAGE IS WORSE THAN NOTHING AGAINST A HEALER.** Our peck is
   **2 dmg for 2 Ti = 1.00 HP/Ti**; their builder heal is **+4 HP for 1 Ti =
   4.00 HP/Ti**. **A defended harvester is unkillable by melee at 4:1 against
   us** — and this is the SALT-family opponent-class caveat already on the tape
   (`docs/coordination.md:42848`: *heals-in-place vs replaces-never-repairs split
   the payoff*; Leviathan healed belts 127 times against 79 cuts in one game).

**⇒ DESIGN CONSEQUENCE, STATED BEFORE ANY GAME: THIS ARM DOES NOT BUY A MELEE
KILL ROUTE TO A HARVESTER.** Clause B's destroy half is **priced and deferred**,
not silently dropped. What survives of it is a **free rider** (§4.3) that costs
zero pecks: mark adjacent enemy harvesters so the ALREADY-SHIPPED corpse-salt
fires when one dies to our forward sentinel — which the tree already places
(`raid.py:636 _try_forward_sentinel`) and which kills a 30-HP harvester in **two
shots at 18 dmg**, the route the 2026-08-09 pricing actually costed
(`docs/coordination.md:10680`).

**⇒ THE ARM IS THE BARRIER HALF, ON ORE, WITHOUT A KILL.** `build_barrier` needs
only an orthogonally adjacent EMPTY tile — no attack, no `can_fire`, and
therefore **no dependency on `LOKI_QUIET_ON`**.

### ⛔ AND THE OBJECTION THAT KILLED THE LAST PRE-EMPTIVE BARRIER ROW DOES NOT REACH THIS ONE — the discriminator is stated rather than assumed

`QUEUE.md` #29 point 9 measured `SALT-EMPTY` dead: *"the chain-head tile is
occupied at median r9 … already occupied before r22 in 83.2% of team-sides …
the window is shut."* **That measurement is about ONE tile class — the conveyor
seat beside their core — and it does not transfer**, for two reasons, both
checkable:

* **The tile population is different.** #29's target was the ≤8 collar seats,
  which their own trunk occupies early. This arm's target is **free ore**, of
  which the pool holds a median of 8 per side and of which they harvest only
  some. **#49 measured the field planting barriers on OUR ore in 19.8% of our
  rated games at a median 21% coverage — so free enemy-side ore tiles demonstrably
  exist and are demonstrably reachable, by opponents doing exactly this to us.**
* **#29 point 6 named the discriminator itself:** *"In open ground they lay a
  conveyor one tile over and our 11 Ti bought nothing."* **Ore has no 'one tile
  over'. That sentence is the argument FOR this row.**

`QUEUE.md` #39's re-basing points the same way: its r4 pre-emption was
unreachable, and what its author kept was *"denial of their LATER expansion
tiles (2nd/3rd harvester, mid-game, reachable)."* **This arm is that, built on
the salt chassis instead of an opening book.**

---

## 4. THE CHANGE — named to `file:line`, old → new

**TREATMENT TREE: `bots/_v243beltsever` — NOT YET BUILT. This prereg SPECIFIES
the diff; the builder lane creates the tree at ratification by copying
`bots/_v223sealrepair` and applying §4.1-§4.4. Every line number below is in the
PARENT `bots/_v223sealrepair`, which is on disk and is what was read.** The
drafting agent was forbidden to touch `bots/` (two screens are LIVE) and did not.

**Flag-off (`LOKI_ORESALT_ON = False`) must be byte-identical in BEHAVIOUR to
v140 — every new branch is inside that guard. The arm tree ships it `True`.**

### 4.1 `doctrine.py` — insert after line 1585 (`LOKI_SALT_CUT_MAX = 40`)

```python
# --- LOKI-70 ORESALT ------------------------------------------------------
# ORE is the one denial target whose function cannot be relocated: a conveyor
# rebuilds one tile over, an ore tile cannot move.  Engine-probed
# (coordination.md:10211-10213, bots/_probe_denial): on a free ore tile
# can_build_barrier == True, and once the barrier stands can_build_harvester
# == False -- with destroying our own barrier RESTORING it as the control.
LOKI_ORESALT_ON = True        # master flag; False == v140 behaviour exactly
LOKI_ORESALT_LOG = False      # dose tag "ORESALT bar r=.. t=x,y" / "ORESALT crater .."
# ONE per raider lifetime, deliberately.  #49's field prescription is 3-5
# barriers total, NOT spam (+1% global scale each; a 92-barrier game was
# observed at +92%).  With this tree's raider count, 1/unit lands in that band
# and caps the scale cost at +3-6%.  Its OWN counter, so it can never spend
# LOKI_SALT_MAX_PER_UNIT, which stays the conveyor budget.
LOKI_ORESALT_MAX_PER_UNIT = 1
LOKI_ORESALT_TI_FLOOR = 12    # bank floor above the barrier's own cost
```

### 4.2 `raid.py:62` — import `Environment`

`raid.py` and `main.py` contain **zero** reads of `Environment.*` today
(verified by grep; ore awareness exists only in `eco.py`, 6 hits). **The raid
layer is ore-blind. That is the grep answer to "do we already do it": ore denial
is ABSENT AS BEHAVIOUR in the raid layer, not specified-but-unwired.**

```
old: from fcode import Direction, EntityType, Position
new: from fcode import Direction, EntityType, Environment, Position
```

### 4.3 `raid.py:469-474` — the crater free rider (ONE `elif`, zero pecks)

Inside `_salt_turn`'s step-(0) MARK loop. `marks` and `LOKI_SALT_MAX_PER_UNIT`
are SHARED with the conveyor corpse deliberately: craters are rare (§3) so the
competition is negligible, and sharing keeps the diff to one branch.

```
old:            if et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                    marks[(t.x, t.y)] = rnd
                    ...
new:            if et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                    marks[(t.x, t.y)] = rnd
                    ...
                elif LOKI_ORESALT_ON and et == EntityType.HARVESTER:
                    # No peck is spent on it -- this only remembers the tile so
                    # step (1) salts the CRATER if the forward Sentinel kills it.
                    marks[(t.x, t.y)] = rnd
```

Step (1) at `raid.py:485-508` then fires unchanged on that mark. **No new code
path, no new budget, no new action.**

### 4.4 `raid.py:536` — insert new step (3) BEFORE the existing step (3), which renumbers to (4)

Ranked **above** the shipped `LOKI_SALT_BLOCK` seat-denial and **below** the
belt cut, so **no conveyor cut and no conveyor corpse-salt is ever displaced**;
this can only consume a round the parent had already declined to move on
(`_salt_idle_ok`, `raid.py:362`).

```python
        # (3) DENY THE ORE.  can_build_barrier already enforces orthogonal
        # adjacency and emptiness; _salt_forward keeps it on THEIR side of the
        # midline, which also stops us denying our own future ore -- our own
        # planner drops a barriered ore tile silently (it scores by
        # availability), so a home-side ore barrier is a self-inflicted wound.
        if (LOKI_ORESALT_ON and self.ore_bar_n < LOKI_ORESALT_MAX_PER_UNIT
                and ti >= bcost + LOKI_ORESALT_TI_FLOOR):
            for d in CARDINALS:
                t = p.add(d)
                if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                    continue
                if not self._salt_forward(t, E):
                    continue
                try:
                    if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                        continue
                    if not ct.can_build_barrier(t):
                        continue
                    ct.build_barrier(t)
                except Exception:
                    continue
                self.ore_bar_n += 1
                if LOKI_ORESALT_LOG:
                    print("ORESALT bar r=%d t=%d,%d" % (rnd, t.x, t.y))
                return True
```

### 4.5 `main.py:101` — one new per-unit counter

```
old:        self.salt_block_n = 0
new:        self.salt_block_n = 0
            self.ore_bar_n = 0        # LOKI-70 ORESALT, own budget
```

**CPU rider.** The new branch is **at most 4 `get_tile_env` + 4
`can_build_barrier` calls**, and only on a round already gated idle by
`_salt_idle_ok`; it adds **no scan**, reuses `p`, `E`, `bcost` and `CARDINALS`
already in hand, and short-circuits on the first success. Budget 10,000 µs/unit;
worst observed 8,748 µs on 900-area maps. ⛔ **`get_cpu_time_elapsed()` reads
ZERO locally and `tle_census.py` returns 0 across 1,649 local builder-turns —
local CANNOT see this dimension** (OB16 addendum's seventh D33 instance). ⇒ the
CPU gate is the **local retry-fire proxy plus the platform `cpu_watch` alarm
after any ship**, never a local zero.

---

## 5. HOW THIS DIFFERS FROM `#37`, `#39`, `#49` AND `#7` — required reconciliation

| row | what it does | relation to this arm |
|---|---|---|
| **#37 TAP THE BELT** | plant OUR conveyor beside THEIR harvester; harvester round-robin is team-blind, so the engine splits their output 50/50 and credits the DESTINATION core | **TAPPING, not severing or denying. COMPOSES, does not conflict** — #37 wants their harvester ALIVE and emitting (a dead harvester pays a tap nothing), this arm denies FUTURE sites and never kills. ⚠ **But they compete for the same raider round and the same 3-Ti bank**, and #37 additionally needs a route home (`doctrine.py:894-898`: a lone stub conveyor is a dead end and delivers zero over 990 measured rounds). **Not combined here.** |
| **#39 OPENING BOOK** | per (map, seat) modal FIRST-harvester tile, pre-empted with a barrier at ~r4 | **Different tile, different clock, and #39's own author retired the r4 form**: the modal tile is beside THEIR core and occupied at median r4, unreachable. This arm targets whatever free ore a raider is *standing next to* mid-game — **no table, no prediction, no book**. #39's surviving half ("denial of LATER expansion tiles, mid-game, reachable") is what this arm implements without needing the decode. |
| **#49 ORE-BARRIER DENIAL, DEFENCE SIDE** | does an ENEMY barrier on OUR ore bind? | **This arm's demand-side evidence, and it is the reason the arm exists.** (a) **THE TILE-LEVEL BIND IS REAL**: 0.106x receipt rate (n=389 vs 1,853, z=-15.78, per-game paired t=-21.98 over 199 games, s40 re-derivation) / 0.28x on the s39 cut, and **85.8% of 1,929 barriers stand to game end**. ⛔ (b) **THE ECONOMY-LEVEL BIND IS *UNRESOLVED*, WITHDRAWN s40** — sign flips twice under a min-n sensitivity sweep. **So this arm may claim the TILE bind and may NOT claim the economy bind.** |
| **#7 ORE-BARRIER CARVE-OUT** | barrier an ore tile a forward gun already covers | **The nearest neighbour, and this arm is a narrower, cheaper form of it**: no gun-coverage precondition, no new siting subsystem — it reuses the raider's existing adjacency and the existing salt budget machinery. #7's own rank caveat ("its channel is the enemy's economy, which is instrumental under `R1000_IS_DEFEAT`") **applies to this arm too and is answered in §1 and §9, not waved away.** |

**⛔ AND THE SENTENCE A READER WILL MISUSE TO CLOSE THIS ROAD:** `CLAUDE.md`
states *"destroying enemy buildings LOWERS THEIR scale — it helps them.
Demolition is not an economic attack."* **That is true of the SCALE channel and
says nothing about the DELIVERY channel or the SITE channel.** Concretely, and
priced: removing one harvester refunds them **5%** of cost scale — real, and
this arm **does not destroy anything** (it plants barriers on tiles that are
already empty), so **it does not pay that refund at all**. What it takes is a
harvestable SITE, which scale does not price. **A barrier we build ADDS +1% to
OUR OWN scale, and that cost is on our side of the ledger — see §7.**

---

## 6. MECHANISM METRIC, DOSE, AND MECHANISM OCCURRENCE

**MECHANISM METRIC READS: `bots/_v223sealrepair/raid.py:536` — the insertion
point of §4.4, instrumented as `LOKI_ORESALT_LOG` tag `ORESALT bar r=.. t=x,y`,
counted per game as ORE BARRIERS PLANTED ON ENEMY-SIDE FREE ORE. TREATMENT DIFF
TOUCHES: `bots/_v243beltsever/raid.py`, `bots/_v243beltsever/doctrine.py`,
`bots/_v243beltsever/main.py`. INTERSECTION: yes — the tag is emitted by the
new branch itself, so it cannot read identically in both arms and reads exactly
the code the diff adds.**

**⭐ THE INSTRUMENT, AND WHY IT IS THIS ONE.** The shard tape
(`ts shard game map seed seat winner cond turns`) carries **no mechanism
column**, and `corpus/events.tsv` covers only PLATFORM games — **local corefill
games are in neither**. The instrument is therefore a **local dose probe with
logging forced on in a copy**: `print()` **is** captured by local `fcode run`
(it is stripped only from platform-downloaded replays — `CLAUDE.md`, s28). **This
is a validated method in this repo, and it has already caught the failure it
guards:** SALTIDLE *"was written off last night as non-dosing — through a
switched-off log flag"* (`SHIP-saltidle-v187`), then measured at 196 SALT events
+ 2,571 funnel events over 8 games once the flag was on.

**DOSE: ⛔ NOT YET MEASURED — THIS LINE IS THE PRE-REGISTERED GATE, NOT A READING; metric is ORESALT barriers planted on enemy-side free ore, REQUIRED treatment >= 1.0/game vs REQUIRED flag-off 0.0/game (n = 12 + 12 games, pool26 array, logging forced on in a probe copy), and the arm tree does not exist yet so D1/D2/D3 below are BLOCKING.**

⛔ **READ THAT LINE AS A REQUIREMENT, NEVER AS A RESULT.** No dose has been
observed for this arm by anyone. The two numbers on it are the pre-committed
pass/fail values, written before the tree exists so they cannot be chosen after
seeing a counter.

The pre-fire gate is: `bots/_v243beltsever` with
`LOKI_ORESALT_LOG = True` vs a flag-off copy, **12 games per arm on the pool26
array**, reading `ORESALT bar` tags per game.
* **D1 (positive):** treatment ≥ 1.0 ore barriers/game, pooled.
* **D2 (negative control):** flag-off arm reads **exactly 0** `ORESALT` tags.
  A non-zero flag-off reading is an instrument alarm, not a result.
* **D3 (placement control):** every logged tile is `ORE_TITANIUM`, and
  `d²(tile, enemy_core) < d²(tile, own_core)` for every one. This drives the
  `_salt_forward` guard to its other verdict rather than trusting it.
* **⛔ IF D1 FAILS THE SHARD IS NOT APPENDED.** A shard whose mechanism does not
  occur measures the absence of the prerequisite, not the value of the plank —
  which is how four launcher rows died this session.

### ⭐⭐ MECHANISM OCCURRENCE — MEASURED ON THE PLATFORM, WHOLE POOL, NO SAMPLING

**This was the question that could have killed the row before a game was spent
(four launcher rows died this session on exactly this), so it was measured
first.** Decoder reused from `tools/replay_census.py` per `tools/replay_schema.md`;
full per-round position stream reconstructed from `placeEntity` /
`moveBuilderBot` / `removeEntity`; our side joined from
`corpus/meta_join.tsv.us_side`. **n = 1,338 games / 284 matches — the ENTIRE
`ourver ≥ 130` pool, 2026-08-13..15 (1,013 unrated, 325 ladder). CIs
DEFF-corrected at 1.75** (76% unrated at 1.833, 24% rated at 1.529; both MATCH
and OPPONENT clusters survive the enumeration on this stratum).

| quantity | value |
|---|---|
| our builder orthogonally adjacent to a LIVE enemy conveyor | **95.6% of games [94.1, 97.0]**, 391,363 builder-rounds |
| reciprocal (their builder ~ our conveyor) | 94.8% [93.2, 96.3] |
| dwell per game | median **159** builder-rounds, p90 666, max 5,066 |
| adjacency-run length (253,148 runs) | **94.7% are length 1**; only 1.8% reach ≥10 |
| games with a ≥10-round same-builder/same-conveyor run | 83.9% [81.2, 86.5] |
| first adjacency, per game | median **r25** (Q1 18, Q3 42) |
| when events happen | Q1 r89 · median **r167** · Q3 r337 |
| where — d² from the VICTIM's core | median **2**; 86.0% of events nearer the victim's core than ours |

**INSTRUMENT DRIVEN TO BOTH VERDICTS, per the standing rule.** POSITIVE control
(our builder ~ our OWN conveyor) **99.3% of games / 444,022 rounds — fires**.
NEG1 (conveyors of a nonexistent team) **0 of 1,338 games, 0 rounds — correctly
silent**. NEG2 diagonal-only offsets, NEG3 zombie conveyors with `removeEntity`
ignored (zombie > alive in 769/1,338 games and < alive in **0**), NEG4 shuffled
team labels — **all three return different counts, so orthogonality,
alive-tracking and team-keying are each demonstrably load-bearing.** 12/12
synthetic unit tests, **one of which caught a real bug in the counter** (an
early-return path merged runs across gaps) before any number above was produced.

**ENGINE-SIDE VALIDATION OF THE PREMISES THIS PLANK QUOTES** (60 v140 games):
`|dx|+|dy| == 1` for **6,618/6,619 = 99.98%** of real `builderAttack` events, so
the orthogonal rule is the engine's and not an assumption; attack `updateHp`
delta **= −2 in 3,625/3,625 (100.0%)**; conveyor `max_hp` **= 20 in 3,710/3,710**
⇒ ten attacks CONFIRMED, not inferred; **85.0% of 170,190 consecutive-attack
gaps are exactly 1 round**, so ten adjacent rounds really do buy ten attacks.

**⇒ WHAT THIS ESTABLISHES AND WHAT IT DOES NOT:**
* ⭐ **ADJACENCY IS NOT THE BINDING CONSTRAINT.** Raiders stand beside enemy
  economic buildings in 95.6% of games, first contact at median r25. **The
  reachability objection that killed four rows tonight does not apply here.**
* ⭐ **ORE IS AT THE SAME DEPTH AS BELT** (§3, n = 3.99M BUILD events), so the
  band the raider demonstrably occupies is the band ore occupies.
* ⛔ **NOT ESTABLISHED: adjacency to a FREE ore tile specifically.** The free-ore
  rate could run higher than the belt rate (ore is static terrain that is never
  consumed) or lower (ore is clustered and they take the good tiles early).
  **D1 is exactly this measurement, which is why D1 is a hard gate and not a
  note.**
* ⛔ **NOT ASSUMED ANYWHERE IN THIS DOCUMENT: that 10 or 15 consecutive pecks
  land on one target.** 94.7% of runs are length 1 and 88.6% of the long ones
  are at the enemy core. **This arm needs ONE action.**
* ⚠ **SURFACE CAVEAT: this occurrence measurement is PLATFORM (real opponents);
  the shard is LOCAL self-play.** Self-play under-doses opponent-induced
  variation in both directions and the rates will not transfer digit-for-digit.
  It is quoted as an ORDER-OF-MAGNITUDE reachability bound, not as the local
  dose — **the local dose is D1 and nothing here substitutes for it.**

### ⛔ THE REALISED RATE OF THE SHIPPED CONVEYOR PATH — the number that sized §3

Same 1,338 games: our builders attack an enemy conveyor in **87.1% of games
[84.7, 89.4]** (60,072 attacks; **96.5% of ALL our builder attacks land on an
enemy conveyor**); we chew one to death in **27.3% [21.5, 33.0]** of games
= **0.40 kills per game**; we barrier the vacated tile in **18.2% [13.2, 23.3]**
of games, and **66.2% of the 133 observed tile refills are OUR barrier** against
32.3% their conveyor repair. **Two independent corroborations that this
instrument agrees with the tree's own:** the shipped doctrine cites a field
repair latency of *"median 4 rounds"* and this decode measured **median 4** blind;
and the pre-salt **40.5%** repair rate now reads **32.3%** — i.e. **the shipped
salt is working**, which is both a validation of the decoder and the reason
clause A is not re-tested here.

---

## 7. HONEST COSTS, STATED BEFORE THE GAMES

1. **+1% GLOBAL SCALE PER BARRIER, ON US, PERMANENT UNTIL DESTROYED.** Our scale
   already runs high, and research measured scale as exactly what prices our
   launcher out (`LAUNCHER_RESERVE` wants 120-160 Ti against a median r150-200
   bank of 54). **`LOKI_ORESALT_MAX_PER_UNIT = 1` caps this at +3-6% for a
   typical raid force. This is the single most likely way the arm reads
   NEGATIVE**, and it is why the cap is 1 and not 4.
2. **~11 Ti per barrier at live scale** (3 Ti base), gated behind
   `LOKI_ORESALT_TI_FLOOR = 12` of retained bank.
3. **A raider round.** Mitigated structurally, not by assertion: the step sits
   below the belt cut and behind `_salt_idle_ok`, the gate that exists **because
   `_v178salt` regressed median kill round r129 → r179 by spending raider
   actions the arrival needed** (`raid.py:362` docstring). The arm inherits that
   gate rather than re-litigating it.
4. **`R1000_IS_DEFEAT` and `DEFENCE_ADMISSION_BAR`.** This is an offensive
   denial plank, but its proximate channel is the enemy's economy, which is
   INSTRUMENTAL. **KILL-ROUND NON-REGRESSION RIDES: the paired kill-round median
   is read beside the share, and a rise is reported whatever the share does.**
   ⛔ Per the DEFF direction clause, that non-regression read is a
   fail-to-exclude claim and **must be restated as an exclusion (the CI excludes
   the regression bar) before any correction is applied to it**; on this LOCAL
   surface the correction is 0.98 and does no work, which is stated so nobody
   later applies a platform constant to it.

---

## 8. REGISTRATION BLOCK

* **SURFACE: local** — corefill shard via `tools/corefill.sh` + `tools/overnight_pool26.sh`, 15-map pool26 array, both seats, zero platform exposure.
* **CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted. **MATCH cluster: does not exist locally** — one row is one game, there is no 5-game match object on this surface. **OPPONENT cluster: cannot hold more than one member per stratum** — the shard has exactly ONE opponent (`bots/_v223sealrepair`) for every row, so conditioning on opponent is conditioning on a constant. **Both clusters die ⇒ DEFF = 0.98** (the measured local pair-weighted constant, ρ = −0.020 over 124 shards; s39 audit). ⛔ **Applying the platform constants (1.529 / 1.833) here would widen intervals 24-35% for correlation that is not present.**
* **ESTIMATOR: unweighted treatment game share** — rows with `winner == T` over all scored rows in `scratchpad/overnight/BELTSEV.tsv`, pooled across maps and seats, no weighting.
* **PINNED: N/A — local self-play.** The opponent version is fixed by the control directory path; there is no platform submission to pin.
* **TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure** (no submission, no activation, no unrated challenge), so `tools/target_value.py` has no input. The rated-value question is deferred to a live leg and is priced in §9.
* **POOL_ERA: post-2026-08-13-rotation** · **POOL ERA: post-2026-08-13-rotation** — the pool26 15-map array, same era as every currently-running local shard.
* **PLANNED n: 10800 games.**
* **BOUNDARY: 10800 games** — LOCAL surface, one row is one game; there is no 5-game accept quantum.
* **CUT-SHORT: floor 5400 games** — below 5,400 rows this leg publishes descriptive tallies and the dose reading only, and takes NO comparative look. (Floor ≤ planned n, as required.)
* **BASE RATE: 50.00%** — the structural A/A expectation of a seat-balanced, map-balanced self-play shard.
* **BASE RATE SOURCE:** `NULL125` (`bots/_v198null125`, a renamed byte-identical copy) and the concurrently-running `NULL5400` (`bots/_v146null` vs `bots/_v146gunaxis`, md5-verified byte-identical across all four files), both on this exact fixture. ⛔ **`NULL5400` IS A LIVE DEPENDENCY OF THIS BAR — see §10.**
* **BAR: 51.93% or higher** on the treatment arm's pooled game share at n = 10,800.
* **BAR SOURCE:** constructed, not observed — `50.00 + MDE(1.00pp) + half_width(0.93pp)`. **MDE inside the bar rather than beside it**, per OB16 as amended by its first application.
* **REFERENCE n: none** — the comparator is the structural 50.00 generated inside the same shard by seat/map balance, not an external reference sample.

### ⭐ THE PRE-SPECIFIED MDE (Obligation 16) — sized off the value we must EXCLUDE

**MDE: +1.00pp. WE WILL CALL THIS ARM A MISS IF ITS TRUE LOCAL EFFECT IS AT OR
BELOW +1.00pp.** Clearing the bar means the 95% interval excludes **both** 50.00
**and** +1.00pp.

**Why +1.00pp and not something the data will more easily clear:**
* ⛔ **THE STANDARD COREFILL BAND CANNOT BE USED HERE.** OB16's corollary
  (2026-08-15T03:52:45Z): the 48.67/51.33 band at n=5,400 **is** 50 ± half-width,
  so its implied MDE is **0.000pp** and it is a POINT RULE licensing *"we can
  exclude 50"* and nothing about a minimum effect. **This document is explicit
  that it is NOT using that kind of bar.**
* **+1.00pp is the smallest effect this project has been willing to call
  shippable on a local screen** (`SCREEN-bodyaware-2026-08-14`, the OB16
  exemplar, same fixture, same n).
* **10,800 is the smallest n at which +1.00pp is expressible**: at n = 5,400 the
  half-width is 1.32pp, so a +1.00pp MDE bar would sit at 52.32 — demanding a
  point estimate larger than the effect it is trying to exclude by 1.3x. **That
  is the CAL-7 floor defect, and it is why n is 10,800 and not 5,400.**
* ⚠ **AND THE HONEST PRIOR SAYS THIS ARM MAY WELL MISS.** §3's density
  arithmetic and the 1-barrier-per-unit cap point to a SMALL effect. **That is
  registered as a reason to size properly, not as a reason to lower the bar** —
  a well-sized negative that closes the ore-denial road is worth a shard, and
  under OB16 an unresolvable bar is a reason to state what IS resolved, never a
  licence to spend games until it resolves.

### Arithmetic (DEFF = 0.98, local/none; `half_width = 1.96*sqrt(p(1-p)*DEFF/n)`)

```
n = 10800  half-width +-0.93pp   BAR 51.93   REAL-NEGATIVE 49.07
n =  5400  half-width +-1.32pp   (CUT-SHORT floor; GATE-5400)
n =  2700  half-width +-1.87pp   (GATE-2700)
n =  1000  half-width +-3.07pp   (GATE-1000)
```

---

## 9. RATIFY: DECISION RULE

**KEEP (ship-shaped, promotes to a live-surface leg):** pooled share **≥ 51.93%**
at n = 10,800 **AND** the paired kill-round median does not regress
(`DEFENCE_ADMISSION_BAR`, restated as an exclusion per §7.4). This excludes both
50.00 and the +1.00pp MDE.

**REAL NEGATIVE (bankable, closes the road for the ore-denial-by-raider form):**
pooled share **≤ 49.07%** at n = 10,800. The CI then excludes 50 from below and
the +1% scale cost of §7.1 is the leading explanation. **A real negative here is
a genuine result and is the outcome the §8 prior mildly favours.**

**⭐ DROP BAND, EXPLICIT: `49.07% < share < 51.93%`.** The arm neither excludes
50 nor clears the MDE. **Verdict: "moves nothing at or above +1.00pp on this
fixture."** Rows are kept, the dose evidence stands, the arm remains a combo
ingredient candidate — **and NO ship, NO live leg, and NO claim that the plank
works.** ⛔ **A reading inside this band may not be reported as a positive
because it is above 50.**

**GATE RESOLUTION: GATE-1000 cannot discriminate its own branch (±3.07pp against
a 2.0pp boundary) and is UNRESOLVED BY CONSTRUCTION; GATE-2700 (±1.87pp) resolves
only outside 48.63-52.37%; GATE-5400 (±1.32pp) resolves only outside
49.18-51.82%; and because these are FUTILITY gates, the pre-committed default on
an UNRESOLVED reading is the RESTRICTION, which here is the DROP.**
`docs/prereg/RULE-futility-gates-2026-08-13.md` binds this shard from its first
row: **GATE-1000 drop if share < 48.0% (`FUTILITY-EARLY`); GATE-2700 drop if
share ≤ 50.5% (`FUTILITY-ALONE`); GATE-5400 added here as the true halfway of a
10,800-game leg, same ≤50.5% rule.** ⇒ **the 10,800 is only PAID if the arm is
winning at halfway.**

**PRE-STATE (Obligation 7): neither the outcome nor the mechanism is already in
the target state at lock.** The mechanism metric (`ORESALT bar` events per game)
is **structurally 0 in the parent** — the branch does not exist, and `raid.py` +
`main.py` contain zero `Environment.*` reads, so no code path in the raid layer
can identify an ore tile at all. The outcome is likewise not pre-satisfied: the
parent is the control, so its share is 50.00 by construction.

**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_ORESALT_ON=True, LOKI_ORESALT_MAX_PER_UNIT=1, LOKI_ORESALT_TI_FLOOR=12, LOKI_SALTIDLE_ON=True, LOKI_PECK_TI_FLOOR=4, LOKI_SALT_MEMORY=8 — every one is a BOOLEAN, BUDGET or TITANIUM gate and NOT ONE IS A ROUND GATE. MECHANISM CAN OCCUR IN WINDOW: yes**

**⚠ THE CHECKER'S PARTIAL-WINDOW WARNS ARE ACCEPTED, NOT ARGUED AWAY.**
`prereg_check` reads a gate's numeric value as a round and warns that, e.g.,
`LOKI_ORESALT_TI_FLOOR=12` leaves r0-r11 unable to contain the mechanism.
**The literal reading is wrong (12 is titanium, not a round) but the conclusion
is right in the other currency and points the same way:** a raider cannot plant
a barrier before the bank clears the barrier's cost plus 12 Ti of retained
floor, so the opening rounds really are structurally empty for this metric.

**THE OBSERVED OCCURRENCE WINDOW, measured rather than argued (§6): first
adjacency at median r25, shipped-salt events at Q1 r89 / median r167 / Q3 r337.
⇒ the live window is roughly r25-r350 — comfortably inside the declared
r0-r1000 and comfortably clear of the floor-blocked prefix, so the declared
window is not inert.**

**AND THE ROUND GATES THAT ARE *NOT* ON THIS PATH, named so nobody re-derives
it:** `_salt_turn` and its caller `_raid_act` step 7 carry no `MIN_RND` of any
kind. The tree's round gates — `HUNT_MIN_RND`, `MEDIC_MIN_RND`,
`LAUNCHER_MIN_RND`, `SURGE_MIN_RND`, `REPLACE_MIN_RND`, `DEFEND_BEAT_MIN_RND` —
gate the hunt, medic, launcher, surge, replace and defend paths respectively,
and **none of them is in this call chain** (verified by grep against
`doctrine.py` and `raid.py`).

The real gate is ARRIVAL, not a round constant: a raider must be standing beside
enemy-side ore. That is a behavioural gate and it is what D1 measures.

---

## 10. INTERACTION WITH THE RUNNING SCREENS — required

* **`BODYAWR` (`bots/_v242bodyaware` vs the same control, n=10,800, seed 336000).**
  **File-disjoint**: BODYAWR rewrites the `blocked`-set construction in
  `eco.py:829-833` (`_bfs_direction`); this arm touches `raid.py`, `doctrine.py`,
  `main.py` and does not read `_bfs_direction`. **But NOT effect-disjoint, and the
  direction is stated: BODYAWR reduces nav refusals, so raiders arrive and STAND
  more — which increases the idle rounds `_salt_idle_ok` hands to this arm.
  ⇒ BODYAWR should AMPLIFY ORESALT, and a later combo must NOT be assumed
  additive.** Each is measured against the same v140 control on its own shard, so
  neither confounds the other's tape. ⚠ **Two concurrent 10,800-game shards is a
  real core-allocation claim** — the futility gates are what make it affordable,
  and BODYAWR's own read is separately gated on its G1/G2/G3 delivery harness.
* **`NULL5400` (`bots/_v146null` vs `bots/_v146gunaxis`, byte-identical, n=5,400,
  seed 344000).** ⛔ **THIS IS A DEPENDENCY OF THIS DOCUMENT'S BAR, NOT A
  NEIGHBOUR.** NULL5400 exists to measure the suspected HOST TERM: any deviation
  from 50.0 on byte-identical arms is pure fixture bias. **`BASE RATE: 50.00` is
  an assumption that NULL5400 is testing.** ⇒ **If NULL5400 finishes materially
  off 50.0, this arm's bar is re-based by that offset BEFORE the read, and the
  re-basing is recorded as an amendment.** Registered now so it cannot look like
  a post-hoc rescue.
* **`SALTREF` (`bots/_v231saltref`, seed 288000), `SEALFLOOR6` (seed 308000),
  `NESTSHOT2`, `GUNAXABL`, `SENTTHR`.** All share the v140 control and the same
  cores. No code overlap with §4. **`SALTREF` is the closest neighbour by name
  and by subject** (it touches the salt family's own constants); **if SALTREF's
  final moves `LOKI_SALT_*` in the shipped tree, this arm's parent changes and
  the diff must be re-based onto the new parent before the tree is cut.**
* **`#66a` (`bots/_probe_beltstall`) — an OPEN engine question this arm is
  IMMUNE to, which is itself a design argument.** #66a asks whether a harvester
  whose chain is saturated/dead-ended **STALLS** (lossless, resumes on repair) or
  **DISCARDS** (lossy). **That question governs the value of every belt-CUT
  plank, including the shipped clause A.** It does not touch this arm: **a denied
  ore SITE never hosts a harvester, so there is no emission to stall or
  discard.** ⇒ this arm's value is independent of #66a's answer; clause A's is
  not.

---

## 11. RATIFY: FALSIFIER

**FALSIFIER: the treatment arm finishes at or below 49.07% game share at
n = 10,800.** That reading excludes 50.00 from below, and the hypothesis of §1 —
that permanent site denial bought on an otherwise-idle raider round is worth more
than its +1% scale and ~11 Ti — is **refuted on this fixture**, with §7.1 (our own
scale inflation) as the named leading mechanism for the harm.

**A SECOND, EARLIER FALSIFIER THAT DOES NOT NEED THE SHARD: D1 fails** — the
dose probe reads **< 1.0 ore barriers per game** with the flag on. **Then the
mechanism does not occur, the shard is never appended, and the finding is
"raiders do not stand beside free enemy-side ore often enough for this to be a
plank"** — which is a real, cheap, road-closing negative and is banked as one.

**⛔ WHAT WOULD NOT FALSIFY IT, stated so it cannot be claimed later:** a result
inside the DROP band; a null on `titanium_collected` or any economy proxy (this
arm's registered channel is SITES, and #49's economy-level bind is *withdrawn as
unresolved* — §5); or a live-surface null against a barrier-CLEARING opponent,
which would bound the arm's opponent class rather than refute the mechanism.

---

## 12. ⛔ THE SELF-PLAY BIASES — TWO OF THEM, AND THEY RUN IN OPPOSITE DIRECTIONS

The victim is our own tree, so the fixture's tell must be declared per-half.

1. **⭐ FLATTERING, AND IT IS THE BIG ONE: in self-play, #49's transfer
   INFERENCE becomes an EXACT FACT, in the arm's favour.** #49 could only
   *assume* an opponent routes around a barriered ore tile rather than clearing
   it (*"transfer assumes their planner, like ours, routes around rather than
   clears"*). **Here the victim's planner IS ours, and we have grepped it:
   `_v197mapcode`-onward scores ore tiles by availability, so a barriered tile
   silently drops out of the candidate set and no code path targets an enemy
   barrier on ore.** ⇒ **self-play is the BEST CASE for the denial half: the
   victim is guaranteed never to clear.** Against a clearing opponent the effect
   is smaller. **Any local KEEP is therefore an UPPER BOUND on the field effect,
   and this document does not promote a KEEP past a live leg.**
2. **CONSERVATIVE: our own long-haul chains break, so a denied site would
   partly have been wasted anyway.** The L4 belt-repair machinery exists in v140
   precisely because our trunks are frequently abandoned mid-lay, and the nav
   limit cycle taxes **11.58% of all builder-rounds** (#54, v125 census). A
   harvester site we deny to a bot that would have failed to wire it is a denial
   of nothing. ⇒ **the delivery/ammo channel is UNDER-dosed by this fixture.**
3. **AND THE BRIEF'S OWN WARNING IS THE REASON THIS ARM IS NOT CLAUSE A:**
   *"severing a chain that was never going to connect measures nothing."*
   **Exactly — which is why this arm severs nothing.** Denying a SITE is
   independent of whether the chain that would have served it was ever going to
   work. **The redesign in §3 is what buys immunity to this bias, not an excuse
   offered after it.**

**⇒ NET: the two biases do not cancel and I am not claiming they do.** Bias 1 is
larger and flatters; bias 2 is smaller and is conservative. **The honest reading
of any positive is "an upper bound against a non-clearing opponent", and that is
written into the KEEP rule as "promotes to a live-surface leg", never "ships".**

---

## 13. WORKLIST ROW, AND THE COLLISION CHECK BOTH WAYS

**Append to `scratchpad/corefill_work.txt` (the builder lane appends; the
drafting agent did not touch it), AFTER the D1 dose gate passes:**

```
# BELTSEV (#29/#7 ORESALT) LOCK docs/prereg/SCREEN-beltsever-2026-08-15.md — n=10800 sized from a PRE-SPECIFIED MDE of +1.00pp (OB16), BAR 51.93.
# ⛔ MAY NOT BE APPENDED until the D1/D2/D3 dose gate passes (see §6). Bar is re-based if NULL5400 finishes off 50.0 (§10).
BELTSEV     bots/_v243beltsever    bots/_v223sealrepair   10800 346000
```

**SEED BASE 346000.** Highest base currently on the worklist is **344000**
(`NULL5400`); 336000 is `BODYAWR` at n=10,800. **346000 is free and is ≥346000
as required.**

**⛔ BASENAME COLLISION CHECK, BOTH DIRECTIONS — the fatal-and-silent one.**
`tools/overnight_pool26.sh:171` scores by SUBSTRING: `case "$L" in *"$B"*) WIN=T;; *) WIN=C;;`
where `B=$(basename $TREAT)`, `C=$(basename $CTRL)`. Its own guard at `:120` is
`[[ $B == $C || $B == *$C* || $C == *$B* ]]`.

```
B = _v243beltsever      C = _v223sealrepair
  B == C ?                       NO
  B contains C ?                 NO   ("_v223sealrepair" not in "_v243beltsever")
  C contains B ?                 NO   ("_v243beltsever" not in "_v223sealrepair")
```
**Both directions clear; the runner's guard would not fire and the scoring is
sound.** ⚠ **Note the near-miss the name was chosen to avoid: `bots/_probe_beltstall`
exists (untracked, created this session) and shares the `belt` prefix — it is
NOT in this shard, but any future shard pairing a `belt*` treatment against it
must re-run this check.** Shard id `BELTSEV` collides with no existing shard id
in `scratchpad/corefill_work.txt` or `scratchpad/overnight/` (checked against
SALTREF, NESTSHOT2, EVICT58, RETIRE60, TINYECO62, SPKT64P, V140VS145/B,
SEALFLOOR6, CRASHP/G/Z/S, GUNAXABL, SENTTHR, V140VS146, BODYAWR, NULL5400,
SENT41).

⚠ **`--seed` does NOT reproduce a local game** (`main.py:288`, unseeded
`random.Random()`), so **no paired-by-seed design is used or implied anywhere in
this document**; the seed base only partitions shards.

**LOCAL-ONLY, REGISTERED AS SUCH.** Cross-host pooling needs a variance term
(host term suspected, n=3 pairs, measurement in flight as `NULL5400`), so this
shard runs on **one host** and its rows are **not pooled across hosts**.

---

## 14. NOT LICENSED BY THIS DOCUMENT

* **No ship.** v140 is sitting; a KEEP promotes to a live-surface leg, nothing more.
* **No claim on the enemy's ECONOMY** (#49's economy-level bind is withdrawn as unresolved).
* **No claim on the AMMO-STARVATION channel or the `can_fire`-at-0-ammo self-kill channel.** Both are mechanism stories in §1; **no bar depends on either**, and the self-kill half is a hypothesis about opponents' code that only a live surface can test.
* **No melee kill route to a harvester** — priced at ≤0.14 kills/game and deferred (§3). The queue item that survives it is *"forward-sentinel harvester focus + crater salt"*, which is a DIFFERENT arm.
* **No combination with `#37` (belt tap) or `BODYAWR`** — the interaction is declared in §10, not measured here.
