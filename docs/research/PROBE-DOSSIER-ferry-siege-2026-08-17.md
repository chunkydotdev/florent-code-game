# S50 PRIOR-ART + ENGINE-PROBE DOSSIER — SELF-FERRY SIEGE RAIDER

*Banked by the builder s50 from the opus probe agent's final report, 2026-08-17. Probe scripts
live in the s50 session scratchpad under `ferryprobe/` (session-private; scripts named below).
Nothing in the repo was modified by the agent; no matches fired.*

**Anchor discipline (agent's own statement).** The agent personally opened only
`bots/_probe_scale/main.py` and `bots/_probe_victim/main.py`. **Every `file:line` in section 1
is RELAYED from its three subagents** (each reported opened-vs-grepped anchors). Treat section 1
anchors as *agent-opened, not builder-opened* — re-grep before pre-registering. Section 2
(probes) is entirely the agent's own measurement.

Probe scripts: `ferry_src.py` → `selfdestruct/ persist/ builderdestroy/` (P1,P2,P5) ·
`seal_src.py` → `seal_full/ seal_off/ seal_gap1/ seal_evict/ seal_evictonly/` (P3) ·
`evictprobe/` + `evictprobe_off/` (P4) · `boundsprobe/` (is_in_vision) · victims:
`idle/ siegevictim/ siegevictim_nospawn/ victim_crowd/` · logs `*.log`.

---

## 1. PRIOR-ART TABLE

| tree | mechanism | verdict + fixture + n + date | currency | reusable |
|---|---|---|---|---|
| **`_v148ferryfirst`** (shipped v112) | **CORE** builds one home launcher; launcher throws our own adjacent builder forward. Rendezvous over the store: raider pings `SLOT_FERRY_ID=id+1` at d²≤8 (`raid.py:574-597`), launcher honours it for 3 rounds. Ferry target = **strictly closer to enemy anchor or no throw** (`raid.py:693-708`). **Launcher never destroyed.** | ship on direction only, live panel **n=25**, 2026-08-11. Local screens: 32/64 NO-INFO; **518/1024 = 50.6%** | ship decision pre-r300; screens are win-share → **void as refutation** | the strict-improvement break; site enumeration (cached form `_v490rush2/raid.py:916-934`); **post-throw stale-state guard `raid.py:167-187`**; the crash guard `eco.py:756-770` |
| **`_v167ferry0`** | ferry-OFF ablation (`LOKI_FERRY_ON=False`, doctrine:1257) | **50.15%, n=5,408** local corefill, 2026-08-12 ⇒ ferry at ~0.9 throws/game is worth ~0 | local self-play share | control arm only |
| **`_v154gunferry`** | ferry-first + gunner-ray station penalty (`LOKI_GUNAXIS_PENALTY=8`) | **50.20%, n=5,408**, bar 51.33 → null. Re-priced r300: timely-kill ITT **+0.91pp [−0.31,+2.12] PASS(nd)** | r300 re-price is current | gunner-ray penalty loop (92% of our forward builder deaths are enemy gunners) |
| **`_v131loki14`** (+`off`) | **kidnap**: enemy builder at d²≤2 → thrown to a **border/corner** tile to induce their crash. Arms alternate B/I on a per-launcher counter | **0/150 border vs 0/164 interior**, bar ≥45/150. Live 5-team panel, **75 games**, 2026-08-10. 2026-08-15 corpus read **deconfounded even the positive** (all 6 signature hits are v107 × its 4 hand-picked targets; **0/930 on the ladder**) | clean (removal counts) | **destination-arm machinery**: border/corner sort `raid.py:660-673`; per-site `try` around `can_launch`/`launch` `:773-780`; fallback list always appended |
| **`_v201launch0evict` / `_v321launch0evict`** | one constant: `LAUNCHER_MIN_RND 160→0`. Throw = farthest from **our** core | dose 6/15 pooled on `_probe_creeper`, 16 games, 2026-08-13. Arm **did not proceed** — its LAUNCH0 citation was wrong (LAUNCH0 = the *no-launcher* arm) | clean | home-launcher gate stack `main.py:613-663`, incl. **never seat a launcher on a heal seat** |
| **`_v233evict58`** | **forward** eviction launcher at THEIR core. Siting gated on a live forward sentinel, d²≤18, census cap 1, scored by **`cov` = their heal seats inside the launcher's own d²≤2 ring** (`raid.py:694-696`). Forward throw key = farthest from **their** core, border secondary; **healer-on-a-seat evicted first** | ⛔ **REFUTED AS DESIGNED**, pinned live leg vs 0033, **25 games**, 2026-08-14: **0.04 evictions/game vs a ≥1.0 bar (25× miss)**. ⭐ **Plant fired at 1.240 launchers/game = 3.6× control; the THROW starved. Binding constraint = PICKUP OPPORTUNITY, opponent-shaped** | clean | **`cov` siting score — reused in P4 and it is what made eviction fire at all**; forward throw key; healer-first victim ordering |

**Load-bearing context the agents surfaced:**

- ⛔ **`LAUNCHER_MIN_RND = 160`** in the holder (`_v490rush2/doctrine.py:1536`, `_v488beltbreak2/doctrine.py:1735`) sits past our median kill round of 174. **v140 made ZERO exile throws across 115 rated ladder games.** There is no launcher capability to inherit — the plank owns it end to end.
- ⛔ **`ct.destroy(`/`can_destroy(` appear ZERO times in `_v131loki14`, `_v233evict58`, `_v490rush2`.** "Disposable launchers" is unwritten code. (`_v170launchrent/raid.py:704-708` has `self_destruct()` after an EXILE throw; **LOKI-43 was withdrawn before firing** at 0.62 cycles/game.)
- ⭐ **The live proof-of-concept is an opponent's.** Juusto v11: **403 launchers built, 402 demolished at age exactly 2 rounds**, 3-round cadence, 0 ammo; payload is a **spawn-ring barrier wall** (708/717 barriers at d²≤5 of the defender core); **+132 Elo in 11.7 h, 62.2% game share.** Closing speed **2.52 tiles/round vs walking 1.0**.
- ⭐ **Turn order is entity-id ASCENDING.** A *rebuilt* ferry launcher gets a **higher** id, so it acts **after** the body it must throw — costing the zero-round hop. Direct consequence for disposable chains.
- ⭐ **The id-order filter, from the tactics atlas:** with `victim_id < launcher_id` the victim is still on the landing tile next round **99.64%** of the time vs **1.83%** otherwise, and **48.79% of the bots we throw today are on the wrong side of it.** One line. Any payload depending on where the victim lands is worth ~half of nothing without it.
- ⚠ **Five collar/seal planks have already failed locally**: spawnlock 49.70 · sentshell 48.75 · collarseal 47.71 · bodyblock 47.26 · sealquiet 25.35 (catastrophe). **But collarseal's two dose rungs measured 0/32 dose** — diagnosed in-repo as a **fixture-admission failure** (`_probe_creeper` sends its builders to *our* core, so our raider never reaches their ring). Those shares are unexposed arms, not refuted mechanisms.
- ⭐ **The one clean large dose in this family is the ferry half**: `_v269awrspawn` vs control — **INSERT 6 → 244 (40×), game coverage 12/32 → 30/32, and slightly faster (124 vs 130 rounds)**. A launcher sited *forward* is the demonstrated supplier of self-ferry throughput. Its full-n 55.06% came with **+21 rounds of kill latency** — the currency problem.
- ⛔ **Doctrine error live in `_det269awrspawn/raid.py:673-675` and `_det252spawnlock/doctrine.py:1274-1281`**: they claim *any* building on a spawn tile denies spawn. **False for conveyors/splitters** (bot-passable; 40.1% of all spawns land on a conveyor tile). Barriers are correct; the sentence is not.
- **The barrier-form spawn lock has NEVER had a live-game test.** Under repo rule 6 it is an open road, not a closed one.

---

## 2. PROBE RESULTS

All local `fcode run`, `--tle 10`. **No TLE fired in any probe run.**

### P1 — Can a LAUNCHER `self_destruct()`? ✅ PASS

| | treatment (`selfdestruct/`) | control (`persist/`, call skipped) |
|---|---|---|
| launcher after the call | never logs again | logs `ALIVE hp=30` every round |
| team scale (core line) | **flat 150.000 forever** | **150 → 160 → 170 → 180** |
| `units` | flat 4 | 4 → 5 → 6 → 7 |
| `get_launcher_cost()` | **flat 30** | **30 → 32 → 34 → 36** |

**The +10% contribution is fully returned**, visible on the very next round's core reading, five cycles in a row.

⭐ **`self_destruct()` never returns and raises nothing catchable.** Sandbox rejects
`except BaseException` and `except SystemExit` at load (`is not an allowed exception type`);
`finally:` blocks are rejected by the AST validator. The unwind is uncatchable by design.
**Put no cleanup code after `ct.self_destruct()` — it will never run.**

**Fallback (`builderdestroy/`) also PASS:** `can_destroy(own launcher)` = True from an
orthogonally adjacent tile; `get_scale_percent()` drops **170.000 → 160.000 the same turn**.
Free, no cooldown. **Not a ferry fallback** — after the throw the builder is ~5 tiles away.

### P2 — Ferry cycle timing ✅ PASS

```
r=1  BUILD launcher (builder action)
r=2  launcher's FIRST run() — ac=0 already — and it throws the SAME round
r=3  builder ac=0 mc=0, builds the NEXT launcher; old launcher self-destructs
```
- A just-built launcher acts the NEXT round, no spawn cooldown. **CYCLE = 2 ROUNDS**, repeatable.
- **Being thrown consumes NOTHING** — the round after landing the builder reads `ac=0 mc=0`.
- Throw range confirmed **d²=26** from the launcher; with the launcher one tile forward,
  **max displacement per cycle d²=37 ≈ 6.08 tiles ⇒ ~3.0 tiles/round, 3× walking**
  (matches Juusto's decoded 2.52 with imperfect geometry).
- Launcher throw cooldown 1 ⇒ **can throw EVERY round** (cooldown decrements at end of round).
- **Arrival at the enemy core, 8 maps:** atoll r5 · royale r5 · nordkap r5 · heart r5 ·
  drumlin r7 · meander r3 · saga r9 · midgard r13 · **jackpot never** (no route found).
  2-launcher chain = 54 Ti on 4 of 8 maps.
- Stale-position hazard real but cheap: re-read `get_position()` every turn; never desynced.
  The hazard is for *cached* Positions — see surprise 1 below, which makes it worse.

### P3 — Spawn + heal denial ✅ PASS, both controls behaved

Treatment vs a non-spawning reporting victim, map atoll (identical on royale, nordkap, drumlin):

| arm | barriers | victim's legal spawn tiles |
|---|---|---|
| **FULL** | 12 | **12 → 0 by r37, and 0 for the remaining 963 rounds** |
| **GAP1** (one tile left open) | 11 | **→ 1, stays 1** |
| **OFF** (ferry in, build nothing) | 0 | **stays 12 all game** |

- **Denial is exactly 1:1 per tile** — each barrier removes exactly one legal spawn target.
- **An enemy BODY on a ring tile also denies spawn** — our own sealer's tile counts.
- **The core cannot retaliate:** `can_fire(<our barrier>)` = False in every adjacent reading.
  ⚠ NOT measured: an enemy builder attacking a barrier (sealed victims never got adjacent).
  30 HP ÷ 2 dmg = 15 builder-turns / 30 Ti per 3-Ti barrier is arithmetic, not measurement.
- **Cost: 12 barriers = 36 Ti; barrier cost stayed 3 Ti throughout** (floor(1.32×3)=3).
  Final team scale after the whole siege: **132%**.

**⭐ HEAL DENIAL — the open repo contradiction is now DECIDED.**
Victim builders tested every round on their own core footprint tiles:
`is_tile_passable/is_tile_empty/can_move` = **False/False/False in 1,996 of 1,996** on
footprint tiles vs True/True/True on 1,999 non-footprint control rows (plus 2,991 occupied rows).
⇒ **A builder can NEVER stand on its own core's 2×2 footprint.** The 2026-08-08 corpus read
(0 of 185,029 bot-rounds) is right; **`BUILDER-TACTICS-ATLAS-2026-08-14.md:239` §5.5's
"immunity theorem" is refuted** (it rests on the `_types.py` stub clause). **The 8 orthogonal
ring seats ARE the only heal stations, so a collar seal does zero the defender's heal rate.**

Two heal facts measured on the way:
- **`can_heal()` returns False on a FULL-HP core** — a heal-denial reading against an
  undamaged core is vacuous (this confounded the agent's first run).
- **One healer exactly nullifies one pecker, forever:** 994 heals over 1,000 rounds held the
  core at **498/500** against a builder attacking every round. Attack 1 HP/Ti vs heal 4 HP/Ti:
  **one healer out-heals four peckers.** Heal denial, not damage, is the plank's engine.

### P4 — Eviction ✅ PASS, with a decisive control

Launcher sited by the `cov` score, map heart, vs a victim spawning up to 8 defenders:

| | treatment (`EVICT_ON=True`) | control (`EVICT_ON=False`, identical plant) |
|---|---|---|
| throws | **248** | 0 |
| rounds with a defender inside the launcher's d²≤2 envelope | **248 / 989 = 25.1%** | **989 / 989 = 100%** |

⇒ **the throw removes the defender from the ring 74.9% of the time, at 0 ammo.**

- Pickup envelope in practice: **d²=1 and d²=2 both accepted** — the 8 neighbours, not own tile.
- **Re-throw cadence: EVERY round is legal.** Observed steady-state gap = 4, set entirely by the
  victim's walk-back (thrown ~5 tiles, returns at 1 tile/round). **One launcher holds ~4
  approaching builders off indefinitely.**
- Throw target d²=26 reached routinely.
- ⛔ **HAZARD (hit live in the integrated run): the ring launcher took the FERRY branch on our
  own sealer** and threw it 2 tiles off the ring. **Ferry launcher and eviction launcher are the
  same entity type doing opposite jobs; distinguish by SITE** (gate: enemy core within d²≤8 ⇒
  never ferry).
- ⛔ **SITING IS THE WHOLE GAME — #58's null reproduced by accident:** launcher on fixed ring
  indices landed on the wrong side and read **0 evictions in 1,000 rounds with a perfect plant**;
  switching to `cov` took it to 248. **#58's live null is at least partly a siting bug, not an
  opponent problem.**

### P5 — Costs ✅ PASS

`floor(scale × base)` verified live: scale 160.000 → launcher 32 (20), barrier 4 (3),
builder 48 (30), harvester 32 (20), conveyor 4 (3).
**⭐ Self-destruct makes the chain cost CONSTANT:** treatment held `get_launcher_cost()` at 30 Ti
all match; the PERSIST control climbed 30→32→34→36 over four launchers. Barriers stay 3 Ti to
~166% scale.

---

## 3. DESIGN CONSTRAINTS THAT FOLLOW

1. **Ferry = 2 rounds per ~6 tiles ≈ 3 tiles/round, 3× walking.** Arrival r3–r7 with a
   2-launcher 54-Ti chain on 5 of 8 maps; r9–r13 / 4–6 launchers on saga+midgard;
   **jackpot never**. Budget for map variance — the chain is 26–166 Ti, not a constant.
2. **Full siege budget: 1 builder (30) + 2 launchers (54) + 12 barriers (36) = 120 Ti,
   complete by r34–r37, ending at 132% scale.** Leaves the two eco builders' economy intact.
   The self-destruct keeps it at 132% instead of ~152%.
3. **A 12-barrier seal locks YOU out too.** Build **11 barriers and park our body on the 12th**
   (a body denies spawn identically — measured); with an eviction launcher: 10 barriers +
   1 launcher + our body = 12 denied tiles, keeping a heal-denied peck station.
4. **The seal does not kill; it makes damage permanent.** Peck = 250 rounds for 500 HP.
   The kill is a **sentinel** (18 dmg / 2 rounds ⇒ ~84 rounds) — its line ignores obstacles so
   it shoots *through* our own collar; a gunner's ray dies on it. **Without a damage source the
   plank is a 1000-round stall, which is a defeat.**
5. **Eviction is the seal's PRECONDITION, not its garnish.** Defenders parked on ring tiles make
   those tiles unbuildable; in the spawning-victim run 3 of 12 tiles were permanently
   body-blocked and the seal capped at 4/12. **Eviction launcher up before/during the seal,
   sited by `cov`.**
6. **Site the ring launcher by defender coverage or it fires zero times** (measured both ways).
7. **Never let a ring launcher take the ferry branch** — gate on distance to the enemy core.
8. **Id-order:** rebuilt launchers get higher ids and act after earlier bodies; the
   `victim_id < launcher_id` filter (99.64% vs 1.83% dwell) wants the eviction launcher
   **late/high-id** while the ferry launcher wants **early/low-id** — **separate launchers.**

---

## 4. SURPRISES, VERBATIM

1. ⛔⛔ **`is_in_vision()` IS NOT A BOUNDS GUARD, AND CLAUDE.md SAID IT IS.** Measured on atoll
   (core at 2,14): `is_in_vision(-1,14)` = **True**, `(2,18)` = **True**, `(-2,11)` = **True** —
   and each raises `GameError: Position out of bounds` on the next `get_tile_*`. It is a **pure
   radius test with no bounds check**; off-map tiles read False only when also outside the
   radius — on heart (core central) all eight off-map probes read False, **which is how this
   survived**. Controls: in-bounds near True, in-bounds far False — the instrument discriminates.
   It killed the agent's own probe on atoll through an `is_in_vision` gate. **Live hazard in any
   code trusting the pre-check near a border — precisely where the ferry lands the raider.**
   (Holder v159 audit, builder s50: all 7 usage sites sit under the blanket run() guard +
   local try/excepts → wasted lookup, not unit death.) Also widens our border-throw crash
   weapon's trigger beyond what was documented.
2. **`self_destruct()` does not return and cannot be caught** — `except BaseException`,
   `except SystemExit`, and `finally:` are all rejected by the AST validator at load.
3. **Module-level state is NOT shared between units** (core wrote a module dict at r0; a builder
   read None at r1). The 16-slot store is the only channel, buffered one round.
4. **`can_heal()` returns False on a full-HP core** — silently vacuous heal-denial readings.
5. **A single healer held a core at 498/500 for 994 rounds** vs a builder attacking every round.
6. **#58's live null reproduced locally as a siting bug** (0 evictions mis-sited → 248 with `cov`).
7. **The eviction launcher threw our own sealer** — same entity type, opposite job.
8. **A seal routine walls itself out by default** — the ring is a closed curve; greedy pathing
   deadlocked 995 rounds against its own barrier. Needs BFS + a build order that keeps a route open.
