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
