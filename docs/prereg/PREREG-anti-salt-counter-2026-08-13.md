# PREREG — THE ANTI-SALT COUNTER PROGRAMME (s35, 2026-08-13)

**Committed BEFORE any counter arm fires.** The arms are still being built at
write time; nothing in this file is informed by a result.

## THE FRAME, AND IT IS MAGNUS'S

> *"Now that we have a salt bot, we can probably pit counters against it and see
> what we can find and then put them together?"*
> *"A counter + salt vs just salt should win more than it loses."*

**SALT becomes the ADVERSARY.** We hold the weapon, so we can develop the defence
against it for free and locally. And the bar he states is not merely reasonable —
**it is `PROGRAMME.md`'s `COMPARE_AGAINST: previous_line_iteration` verbatim.**
SALT is v122, the live incumbent, so the next iteration answers to it.

## THE DEFECT THE COUNTER TARGETS — FOUND BY READING, NOT BY MEASURING

`eco.py`, `_build_next_link`:

    occupied = ct.get_tile_building_id(tile) is not None
    if occupied:
        self.link_queue.pop(0); continue      # <-- NO TEAM CHECK

`get_tile_building_id` is **team-blind**. An ENEMY barrier on our trunk route is
popped as *"this link is already built."*

**⭐ AND THE CORRECT GUARD IS 36 LINES ABOVE IT, IN THE SAME FILE** —
`_has_acceptor`, `eco.py:516-517`:

    bid = ct.get_tile_building_id(t)
    if bid is None or ct.get_team(bid) != self.team:

⇒ **This is `CLAUDE.md`'s own exploit heuristic turned on us verbatim: *"LOOK FOR
ASYMMETRIC GUARDS. A guard present on one path and absent from its neighbour is
where exploits live."*** And `eco.py` is the very file `CLAUDE.md` cites under
*"MINE OUR OWN BUG FIXES FOR THEIR BUGS"* — hardened once for the launcher-teleport
case, and **this path was missed.** Credit: the side lane found the neighbouring
guard.

**⚠ SCOPE, STATED BEFORE THE MEASUREMENT: the MECHANISM is verified by reading.
The CONSEQUENCE is not measured.** Two readings survive a careful static read and
**I cannot separate them from the code**:
* **(a) PERMANENT STALL.** After popping barriered tile T the head becomes T+1,
  which is 2 tiles from a builder at T-1 and unreachable because T is barriered;
  `_build_next_link` returns False forever, and the queue only re-plans at
  `_wire_on_build` **`if not self.link_queue`** — which never empties. Enemy cost
  **3 Ti**; our cost the whole harvester route.
* **(b) SELF-HEALING.** The builder wanders, becomes adjacent to a later tile, the
  queue drains, and a re-plan happens.
**`_link_path` IS already team-aware** (it blocks enemy buildings), so the
PLANNER is not the hole — only the incremental builder is.
⇒ **THE DISCRIMINATING TEST IS ONE LOCAL GAME: put an enemy barrier on a trunk
tile mid-route and watch whether `link_queue` ever empties.** This is D12
territory and the reading decides whether the fix is a nicety or the most
valuable line in the tree.

## ⛔ THE ONE-LINE FIX STANDS ALONE

**The `:517`-shaped team check does not depend on this programme.** If every
counter arm reads null, the one-line fix is still correct. **A null on the counter
must not retire it by association.**

## THE FIXTURE, AND WHAT EACH CELL DOES AND DOES NOT BUY

| cell | arm vs control | status |
|---|---|---|
| **NULL** | `_v195nullcell` (byte-identical salt copy) vs `_v178salt` | **RUNNING** (`NULLSALT`, seed_lo 205000) |
| **NEG** | `_v169launchlate160` vs `_v178salt` = **39.00% at n=5,408** | **ALREADY MEASURED — free** |

**⚠ AND THE FREE NEG CALIBRATES AT SALT-SIZE, NOT COUNTER-SIZE.** Its arm differs
from salt by the WHOLE salt block, an effect at **z ≈ 16**. So 39.00% establishes
*"this fixture resolves a salt-sized difference"* — **it says nothing about
resolution at the counter's plausible (much smaller) size.** That is D13: *live
but does not RESOLVE*. `NULLSALT` gives the null end; 39.00% gives a far-off
point; **neither gives the MDE at the size that matters.** Flag raised by the
side lane before the leg fired, which is the only time it is cheap.

**⇒ MDE, STATED NOW: at n = 5,408 per arm the informative band is ±1.33pp.**
**A counter worth less than ~1.3pp returns NO POWER, not NO EFFECT — and those
imply opposite actions.**

## THE BAR — MAGNUS'S DIRECTION, PLUS THE RESOLUTION STATEMENT IT NEEDS

**⛔ "MUST CLEAR 50%" IS MET BY 50.01%, AND AS WRITTEN CANNOT FAIL.** The
direction is his and is unambiguous and right; what is missing is an n and a
margin. **This repo's own evidence, from last session:** `SHIPGATE160` read
**49.44%** and `SHIPGATE0` **49.19%** and both were correctly cancelled as
INSIDE-BAND against a ±1.33pp band — **values within 0.6pp of 50 treated as
no-information.** A bare "clear 50%" would have **passed a 50.4%** sitting in
exactly that band.

**THE BAR, ADD-ONLY TO HIS FRAMING:**
* **SHIP the counter iff `salt+counter` vs `salt` reads ABOVE the informative
  band at n >= 5,408** — i.e. **> 51.33%**, not merely > 50.
* **INSIDE BAND (48.67–51.33%) ⇒ NO SHIP.** Pre-committed here, before the number
  exists, because this is the branch that will be under pressure if it reads
  50.6%. **An unresolved gate defaults to the RESTRICTION, never the
  PERMISSION** — already the standing default in the obligations doc.
* **BELOW band ⇒ the counter is a real cost** and the arm is demoted.
* **⛔ NULL CELL GATES EVERYTHING: if `NULLSALT` does not read ~50%, the fixture
  is biased on this contrast and NO counter verdict may be read at all.**

## ⚠ THE LIMIT ON WHAT THIS PROGRAMME MAY CLAIM

**A counter developed against `_v178salt` and measured against `_v178salt`
optimises against the specific salt implementation WE wrote.** That is
`FIXTURE_OF_RECORD`/D11 in its purest form — the same shape as five of our probes
sharing a `best_core or best_any` short-circuit, where every verdict we resolved
faced an opponent that preferred our core over anything else.
⇒ **This programme licenses HARDENING. It does NOT license a claim about what
opponents would actually do to us.** Not a blocker; a boundary, written down
before the result rather than after. Raised by the side lane.

## ARMS

Built on `_v178salt` (so the contrast is salt+counter vs salt). `eco.py` is
**byte-identical** between `_v169launchlate160` and `_v178salt` (md5
`3b636ca892a038a51b2dcab536510167` both), so the patch ports cleanly.
1. **CLEARLINK** — enemy building on the head tile: do not pop; peck it (2 Ti / 2
   dmg; a 30 HP barrier = 15 pecks — that price is the arm's honest cost).
2. **ROUTELINK** — enemy building on the head tile: ban the tile, clear the queue,
   force a re-plan. **Cheaper if it works, and the planner is already team-aware.**
Defence-only variants on `_v169launchlate160` are also being built, to separate
*"the counter works"* from *"the counter is worth its price in a salt bot."*

---

# AMENDMENT 1 — 2026-08-13T05:4xZ. **THE ATTRIBUTION ARMS INHERITED THE WRONG BAND.**

**ADD-ONLY, and it TIGHTENS what may be claimed.** Raised by the side lane before
any arm reported.

The prereg states one band, **±1.33pp at n=5,408**, and applies it to the ship
bar. **The attribution arms were added after that line and silently inherited it.
They must not.** The two contrasts are different shapes:

* **BAR — `salt+counter` vs `salt`.** The two arms play **each other**, so the
  result is ONE proportion against a **theoretical 50% null**. Band **±1.33pp**.
  **`> 51.33%` stands, unchanged.**
* **⛔ ATTRIBUTION — `counter-only` vs `salt`, read against the free 39.00%.** That
  39.00% is a **separate measurement** (its own battery, its own n=5,408, its own
  error). So this is a **difference of two INDEPENDENT proportions** and its band
  is **√2 × 1.33 = ±1.88pp**.

**ATTRIBUTION BAND: ±1.88pp about 39.00% (37.12–40.88%). INSIDE BAND ⇒ NO
ATTRIBUTION** — same pre-committed default as the ship bar: an unresolved gate
defaults to the RESTRICTION.

**WHICH WAY THE ERROR LEANED, stated because that is the part worth recording:** a
counter-only reading of **40.5%** is +1.5pp over 39.00% — **inside the correct
band, i.e. no information** — but it clears the too-tight ±1.33pp band and would
have published as *"the counter has an independent effect against salt."*
**The mistake made a favourable claim EASIER.** Third time today my own error ran
toward flattering the plank; the s29 rule holds — an error distribution with a
mean is not noise.

**⭐ AND THE STRUCTURAL CAUSE IS THE SEED CONVENTION, arriving from a second
direction.** The BAR contrast gets the narrow band **for free** because both arms
play head-to-head and are paired at the match level. **The ATTRIBUTION contrast
pays the √2 penalty precisely because its comparator lives in a DIFFERENT battery
on a DISJOINT seed block.** Every arm here runs its own seed range (SALT
133000–133337, SHIPGATENULL 123000–123337, NEG169 124000–124337 — **0 shared
cells**), so every cross-battery comparison is unpaired.
⇒ **ROUTED, NOT DONE: the next battery should run treatment and control on the
SAME seed block and read the PAIRED contrast.** The engine is deterministic
(verified s34, 6/6 byte-identical on a flags-off arm), so the same
`(map, seed, seat)` cell played by two arms differing in one flag differs ONLY by
the treatment. Concordant cells contribute nothing to a paired difference, so the
band narrows **at the same n and the same cost.** Not changed mid-flight here —
`NULLSALT` is already filling on 205000 and re-seeding now would cost more than
the gain.

---

# AMENDMENT 2 — 2026-08-13T06:2xZ. **THE DISCRIMINATING TEST RAN. BOTH MY READINGS WERE WRONG, AND THE CONTROL BEAT THE TREATMENT.**

16 instrumented games (8 vs `_v178salt`, 8 vs `_v169launchlate160` as control),
4 maps x 2 seeds each, stderr-only instrumentation, zero tracebacks. **Every
load-bearing claim below re-verified by me at the code, not taken on report.**

## NEITHER (a) NOR (b). A THIRD FAILURE MODE.

* **NOT (a) PERMANENT STALL.** The feared "head is 2 tiles away and unreachable"
  geometry **never occurred** — the loop only inspects a tile once the builder is
  ADJACENT, so the builder keeps walking and the block resolves the moment it
  arrives. My inference was wrong about the control flow.
* **NOT (b) SELF-HEALING**, despite `len(link_queue)` reaching 0 in 8 of 9 cases.
  **In 7 of 9 the enemy building sat on the LAST queue tile** — the delivery seat
  itself — **so popping it empties the queue TRIVIALLY.** Verified directly on
  `ctrl_antler_910001` tile `(7,6)`: **never rebuilt or revisited across the
  remaining ~190 rounds.**
* **⭐ THE ACTUAL DEFECT: `len(link_queue)==0` IS NOT EVIDENCE OF CONNECTIVITY. It
  is the code silently declaring the trunk DONE one tile short of our own core,
  permanently.** `_wire_on_build` only re-plans on `not self.link_queue`, and this
  is exactly how the queue empties — so **the re-plan never fires.** The symptom
  is not a frozen builder; it is **an abandoned, unmonitored delivery connection.**

## ⛔⛔ AND IT IS NOT SALT-SPECIFIC — THE CONTROL TRIGGERED IT MORE OFTEN

    games with >=1 enemy-owned pop   SALT 3/8      CONTROL 6/8
    total enemy-owned pop events     SALT 4        CONTROL 9

**Verified at the code:** `LOKI_BARRIER_SEAL_ON = True` in **both** bots, and
`_link_path`'s `raw_goals` are precisely the tiles cardinally adjacent to our core
— **the heal seats a raider seals.** So ANY raider that reaches our core
manufactures this position. **Salt is not the cause; salt was the excuse to look.**

⇒ **THIS MAKES THE ONE-LINE FIX MORE VALUABLE, NOT LESS.** It was scoped as an
anti-salt counter; it is a **generic economic defect** that fires against every
raiding opponent, and the counter arms already built target it directly.
⇒ **AND IT WEAKENS THE COUNTER LEG'S ATTRIBUTION**: `salt+counter vs salt` will
capture a benefit that has little to do with salt. **The bar is unchanged; the
CLAIM must not become "this counters salt."**

## ⚠ WHAT IS STILL NOT MEASURED
**Whether the abandoned seat costs delivered titanium.** Other seats or the
pave-trail may bridge it incidentally. **Unmeasured, and the counter legs do not
measure it either** — they measure outcomes, not delivery. Named here so a
favourable counter result is not read as proof of this mechanism.

## ⛔ AND A FIXTURE FACT THAT REACHES EVERY BATTERY IN THIS REPO
`main.py:276` — **`self.spawn_salt = random.Random().randrange(97) if NOISE_ON
else 0`** — is seeded from OS entropy, NOT from `--seed`. **So the same
`(map, seed, seat)` cell is NOT reproducible while `NOISE_ON` is True.** This is
the single nondeterminism site HANDOVER already names, now confirmed to matter in
practice. ⇒ **It is a precondition on the paired-seed design proposed earlier: a
paired contrast requires `NOISE_ON = False` in BOTH trees, or the pairing buys
nothing.**

---

# AMENDMENT 3 — 2026-08-13T06:1xZ. **A PRE-REGISTERED LOOK SCHEDULE, BECAUSE I DID NOT HAVE ONE.**

**ADD-ONLY, and it CONSTRAINS me rather than the data.**

I shipped v123 partly on `IDLEVSALT` at n=517 and disclosed the reason to
distrust it: **I chose when to look, repeatedly, at a shard filling
continuously.** The side lane first offered z≈3.56 as reassurance and then
withdrew it, correctly: **that is a MULTIPLICITY correction and this is OPTIONAL
STOPPING — different faults, and a fixed-n z cannot see the second at all.**

**⛔ AND THE INFLATION IS NOT RECOVERABLE AFTER THE FACT: it depends on the LOOK
SCHEDULE, which was never pre-registered, so nobody can compute it now.** That is
not a reason to discount the disclosure — **it IS the disclosure.**

⇒ **It cannot be fixed retrospectively for `IDLEVSALT`. It CAN be fixed
prospectively for every arm still filling, and all four are under 25% of target,
so nothing here is chosen with knowledge of a final number.**

## THE SCHEDULE — committed now, before any of these arms is near done

**Exactly TWO scoring looks per arm. No verdict may be read at any other n.**

| look | n | what may be concluded |
|---|---|---|
| **INTERIM** | **2,704** (half target, exactly 8 maps x 2 seats x 169 seeds) | STOP EARLY **only** if outside the band at that n; otherwise say nothing and continue |
| **FINAL** | **5,408** | the verdict |

**Bands: ±1.88pp at n=2,704 · ±1.33pp at n=5,408.** Applies to `NULLSALT`,
`SALTCLEAR`, `SALTROUTE`, `IDLEVSALT` and `ROUTEONLY`.

**⚠ AND THE HONEST COST OF EVEN TWO LOOKS, stated rather than hidden:** two looks
at nominal 5% is a family-wise error near 8-9%, not 5%. **A stop at the interim
is therefore a WEAKER result than the same number at full n**, and any interim
stop must be reported with that sentence attached.

**WHAT I MAY STILL DO BETWEEN LOOKS — and the distinction is the whole point:**
report **progress** (n, and the rate as a running figure) to Magnus on request.
**What I may not do is treat a between-look reading as a RESULT, or ship on one.**
Watching a number is not the fault; **letting the moment I happened to look decide
the verdict is.**

**⛔ THIS DOES NOT RETROSPECTIVELY VALIDATE v123.** v123 shipped on a look taken
outside any schedule, on Magnus's call, and that stands as recorded. **The
schedule binds what comes next.**
