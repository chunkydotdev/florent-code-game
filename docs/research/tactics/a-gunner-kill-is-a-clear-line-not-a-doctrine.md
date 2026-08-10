---
tactic: The counterweight — a gunner-heavy core-kill mix is mostly a MARKER of an unobstructed close approach, not a CAUSE of it
source: docs/reference/official-docs.md:242 (gunner line rule) + docs/research/tactics/INDEX.md (s23 probe: gunner line blocked by own bots and buildings, sentinel line is not)
origin: research arm, sweep 17b, 2026-08-09 — own reading, filed because the brief demanded the counterweight be looked for on purpose
evidence: inference
transfers: yes
---

## WHAT IT IS

The measured surprise this sweep was aimed at: **against ≥1700-rated teams, cores die
53.1% to gunners, 44.4% to sentinels, 2.5% to builder melee; our own kill mix is 22.7 /
69.2 / 8.1.** The tempting inference is *"build gunners."* This file is the argument that
the inference is mostly backwards, and it is filed on purpose because **this project has
already been burned once by copying a stronger bot's symptom** — we measured that top
teams garrison thinner, inferred "garrison less", built it, and it was refuted 40% vs 60%
(see [`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md)).

**The mechanical argument.** Our two damage turrets differ on exactly one thing that is
large: what stops the shot.

- Gunner: *"The line stops at the first targetable tile (a builder bot or a building) in
  its facing direction; empty tiles don't block it, but walls do"*
  (`docs/reference/official-docs.md:242`). The s23 probe recorded in
  [`INDEX.md`](INDEX.md) confirms **our own** bots and buildings block it too.
- Sentinel: the line is *"never blocked by walls or units in the way"* (same doc, :259),
  probe-confirmed to land 18 damage through a friendly bot **and** a friendly barrier.
- Range: gunner ray reaches **3 tiles** cardinally (3²=9 ≤ 13, 4²=16 > 13), sentinel
  **5** (5²=25 ≤ 32, 6²=36 > 32). Diagonally: **2** and **4**.

**So a gunner can only ever be credited with a core kill if, at the moment it fired,
(a) it stood within 3 tiles of the core and (b) nothing — not one enemy barrier, not one
enemy conveyor, not one of their builders, not one of OUR OWN bots or buildings — lay
between it and the core on its facing axis.** A sentinel needs neither condition.

**Therefore a high gunner share of core damage is, first and foremost, a measurement of
how clean and how close the approach was.** It is the same quantity as "we got a turret
planted three tiles from their core through an undefended lane", reported in a different
unit. A team that wins the approach gets a gunner share for free; a team that does not
win the approach *cannot* get one, no matter how many gunners it builds, because the
gunners it builds will be firing into the first barrier they meet.

**And the economic leg is closed off separately.** If the gunner-heavy mix were an
affordability effect — "gunners are what you can buy early" — the arithmetic in
[`the-turret-mix-is-not-a-cost-decision`](the-turret-mix-is-not-a-cost-decision.md) says
the two turrets sit within ~10% on every titanium metric, so affordability is not a large
enough lever to produce a 53/44 vs 23/69 inversion on its own.

## THE HONEST SPLIT — what is mechanism and what is marker

| reading | class | why |
|---|---|---|
| "Gunners kill cores because they were close and unobstructed" | **MARKER** | tautological from the line rule; the kill share *measures* the approach |
| "Once you are close with a clear line, the gunner is the correct weapon and we fail to switch to it" | **MECHANISM, and testable** | at ≤3 tiles with a clear line the gunner is 14% cheaper per point of standing DPS and can rotate; the sentinel's whole premium (reach, obstacle-piercing) is worthless at that range |
| "Build more gunners and the kill share follows" | **REFUTED SHAPE** | this is the garrison error's exact form: import the statistic, not the condition that produced it |

**The one live mechanism is narrow and specific:** *we may be paying for
obstacle-piercing we no longer need at the moment we get close.* Every sentinel planted
inside 3 tiles of an unscreened core is 10 Ti of build premium and 6 ammo per shot spent
on a property that is not being used.

## WHAT WOULD KILL IT

- **Corpus evidence would settle it and this sweep did not gather it.** The decisive cut
  is: *conditional on a core kill, what was the distance and line-clearance of the
  killing turret at the moment of the killing shot, ours vs theirs?* If the top tier's
  gunners fire from 3 tiles through lanes they cleared, marker. If they fire from tiles
  that were *already* clear at build time, mechanism (they site better). **Stated
  plainly: I have not run this and it is not a finding.**
- **The reverse causal story is live and I cannot rule it out**: gunners might *cause*
  clean approaches by being cheap enough to plant several, so that the first one to get a
  clear line fires. That is a real mechanism and it would look identical in the kill-share
  statistic.
- **The 2.5% vs 8.1% melee share is a third variable** the mix framing ignores: we do
  3.2× as much of our core damage with builder attacks as the top tier does. Builder
  melee is 1.00 damage per titanium — the worst rate available — so that share is a
  straightforward efficiency loss regardless of how the turret question resolves.

## BUILDER HOOK

**The smallest thing that would test it is a siting predicate, not a build-ratio change.**
At turret-build time, walk the candidate facing axis toward the enemy core and check
whether any tile between the site and the target holds a building or a bot. Then:

- clear line **and** target within r²=13 → **gunner** (cheaper per DPS, and rotatable
  if the threat axis moves)
- blocked line **or** target beyond r²=13 → **sentinel** (paying the premium for the
  property being used)

That is a distance-and-clearance conditional turret type, not a quota. It converts the
measured kill-mix surprise into a rule that can only fire when the geometry that produced
the surprise is actually present — which is exactly what the garrison error lacked.

> ### ⚠ BROKEN CITATION, 2026-08-10 (research arm)
> This file cites [`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md)
> for a **"garrison refuted 40% vs 60%"** claim. **That file was read in full and
> contains NO garrison content** (`grep -ci garrison` = **0**). **The claim is
> UNSOURCED as cited.** Either it points at the wrong file or it was never sourced;
> until someone identifies the real source it must not be relied on.
