# Early-kill arsenal: the league already shows how to kill a core before r80, and we do it slower than the specialists

**Side lane, 2026-08-09 14:57 CEST, on Magnus's maximum-aggression directive
to the builder ("manipulate, exploit, kidnap, poison — kill the other team
EARLY"). This is the corpus half: every early core kill in the league,
decoded to who / what / when / where, and the specific recipe that kills
fastest. The doc-mine half (offensive-mechanic catalog with refutation
status) lands as a companion. Builder owns which recipes get built.**

**Version tag:** live v92 (per builder, holder 1534 @ 526). Data: 2,735
attributed replays via the preserved side-lane decoders (rx_shooter with the
survivorship fix committed today; dc reconciles at 20,929). Zero downloads.
Every headline number below is a direct corpus count.

## 1. Early core-kills are common, turret-only, and start with a rush-plant

**1,269 of 1,849 decided games have a core dead by r300** (median death
**r154**, p10 **r69**, minimum **r24**). The mechanism is turret fire and
essentially nothing else: of 1,269 early kills, **9 had no killer-team
core-shooter** (builder-attack or other) — 99.3% are gunner/sentinel. The
league-wide early recipe: **2 killer turrets/game, planted at median r61
(p25 r22)**, gunners point-blank (median d²=8 to victim core), sentinels at
stand-off (median d²=25). Builder attacks do not kill cores; the launcher
does not kill cores (§4). **The only early-kill weapon on the board is a
turret planted near the enemy core, early.**

## 2. The fastest recipe, and it is a SENTINEL RUSH

190 games have a core dead by **r80**. Their recipe is the league one,
compressed and intensified: **median 3 killer turrets, planted at r22
(p25 r11)**. Broken out by the fastest-killing specialists (kills ≤ r120):

| team | median death | plant round | turrets/game | mix | gun d² / sen d² |
| --- | ---: | ---: | ---: | --- | --- |
| **Banminary** | **r52** | r17 | 2 | sentinel-heavy (855 sen / 122 gun) | 2 / **18** |
| Big O | r63 | **r14** | 2 | **pure sentinel** (350 / 0) | — / 25 |
| gsxWins | r71 | r25 | 3 | mixed (430 sen / 293 gun) | 4 / 26 |
| Team 48 | r74 | r30 | 3 | **pure gunner** (2734 / 0) | **10** / — |
| Cookie | r88 | r21 | 2 | sentinel, **point-blank** (686) | — / **2** |
| **OpenSverige (us)** | **r91** | r24 | **1** | sentinel-heavy | 13 / 32 |

**The arithmetic behind the sentinel preference** (rule-derived, S1, free):
a core is 500 HP. Gunner = 7 dmg, reload 1 → 3.5 DPS, needs **144 rounds
solo**. Sentinel = 18 dmg, reload 2 → 6 DPS, needs **84 rounds solo** — and
its shot **ignores obstacles** and outranges every gunner (r²=32 vs 13). A
**3-sentinel plant = 18 DPS = ~28 rounds of sustained fire to kill a 500-HP
core.** That is why the r52-kill specialists are sentinel-rushers: three
sentinels planted by r17, firing from stand-off the defender cannot block,
kill the core around r50. This is the exact weapon we found is nearly
undefendable when CAD uses it on us (cad-core-kill doc: the sentinel half
carries 65% of the damage, 28% planted outside the home band). **The
league's fastest kill and our worst weakness are the same mechanic.**

## 3. We are the #1 early killer by VOLUME and behind on SPEED — the lever

We (OpenSverige) already lead the league in raw early kills: **309 early, 48
sub-r80** — more than anyone. But we are not on the fast-RATE leaderboard,
and the recipe table says why: in our fast kills we plant **1 turret/game**
vs the specialists' 2-3, and our turrets stand **farther** (sen d²=32 vs
Banminary's 18, Cookie's 2), so our median kill lands at **r91 vs
Banminary's r52 — ~40 rounds slower**. We win the early race by out-*starting*
opponents, not by out-*rushing* them.

**The dirty lever, stated for the builder:** copy Banminary. Plant **denser
(3 sentinels, not 1), closer (d²≈18, not 32), earlier (r17, not r24)**,
against the enemy core, as a committed opening — not a defensive turret that
happens to face out. The measured target is a ~40-round-faster kill, and it
converts our existing #1-volume position into a #1-speed one. Caveat that
binds it (our own scoreboard): this is a **committed opening**, so it must be
priced as an opening — what it costs in economy if it *fails* to kill, and
against which opponents it fails, is the build question S5-unrated answers.

## 4. Kidnap and poison: heavily used, but the corpus says displacement, not kills

- **Launcher kidnap (throw an enemy builder — legal: `launch` picks up an
  adjacent builder from EITHER team):** 61,109 enemy-bot throws league-wide,
  and **we are the #1 kidnapper (11,106; Memtrace 9,756).** But **every one
  is attribution-ambiguous in the corpus (`amb`=all 61,109)** and they
  produce **0 core attacks** — kidnap in the data is pure displacement
  (matches the `displace-dont-kill` tactic doc), not a kill path. The
  offensive-throw question (throw an enemy builder into our own turret arc,
  or into a wall/off its work) is NOT answered here and is deferred to the
  doc-mine and the throw-into-prebuilt-cell / escorted-forward-plant tactics.
- **Own-bot insertion throws:** 29,368, of which 3,633 reached a core and
  713 attacked one — the raider path, already refuted **as LATE doctrine**
  on four instruments (HANDOVER: 2.34% of r200+ forward throws touch a core;
  raider life 43→6 rounds at r150). **The early window (r<150) was never the
  refuted claim** — that distinction is the open door.
- **Poison / denial (ore-tile denial, ammo-drain baiting, CPU-timeout
  induction):** these are mechanic-legal and catalogued in the tactics docs;
  their evidence + refutation status is the doc-mine's job. Flagging here so
  the builder does not double-count: **ammo-drain baiting died pre-build**
  (drain-discriminator doc) — do not rebuild it.

## 5. Aim: which opponents the rush pays against most (from revert-brackets)

The manipulation overlay, so nastiness gets pointed at soft targets:

- **Fast kill beats slow defenders regardless of their meta-game.** The
  rush's target is the *core*, so opponent revert-discipline is secondary —
  but two aims still matter.
- **Ouroboros is a static target** (same v8, 373 matches) — a rush tuned
  against it stays tuned; they cannot patch it out inside our measurement
  window.
- **Lunds is steerable** (revert-brackets: 50% of their reverts fire on
  blank data, they've reverted UP versions) — a lopsided early loss inflicted
  on a fresh Lunds ship plausibly reverts them onto an older binary we
  fingerprint. Lower confidence (two inferential steps), banked behind the
  rush itself.
- **CAD is the exception and the tension:** we are 16-4 vs CAD at r1000, so
  the CAD-specific objective is *survive to r1000* (cad-core-kill adoption
  note), which a committed all-in rush works AGAINST. **The early-kill
  doctrine and the CAD-survive doctrine are opposite postures.** They must be
  map/opponent-gated, not run globally — the bot already computes map+seat at
  runtime (`known_map_for`), so a per-opponent posture switch is mechanically
  available.

## 6. What this hands the builder, ranked

1. **The sentinel rush (Banminary recipe).** Positive field evidence
   (28 sub-r80 kills), rule-arithmetic backing (3 sentinels = ~28-round
   kill), and it exploits the weapon we already know is hard to defend.
   **Cheapest high-value build.** Price it as an opening (fail-cost + S5).
2. **Posture-gating by opponent/map.** The rush and CAD-survive are opposite;
   the runtime map/seat table makes gating free. Build the switch alongside.
3. **The offensive throw (kidnap into a hazard/arc).** Unmeasured for kills;
   needs an engine probe (does a thrown enemy builder take our turret fire on
   the destination tile the same round?) before any build — S2, builder-owned.
4. **DO NOT rebuild:** ammo-drain baiting (dead), late forward insertion as
   doctrine (refuted 4 instruments), more-defence/ESCALATE (−7.8pp), SITE
   forward siting (−6.7pp). The doc-mine's C-list is the full protection set.

## Methods & limits

Early kill = corehp≤0 by rN in `bb_rows` (survivorship-fixed decoder). Killer
recipe = rx_shooter (ncore>0, killer team) joined to `builds.tsv` for plant
round + d²-to-enemy-core. Kill-time arithmetic is rule-derived (HP/damage/
reload from CLAUDE.md, S1). Limits: 2,735 of ~6,200 archived replays are
attributed (the mine is over the attributed set — a large, not total,
sample); kidnap throw direction is un-attributable (`amb`=all); per-team
fast-kill cells are n=11-29 (directional, and the direction is consistent
across five independent specialist teams). Recipe reproduces the
cad-core-kill mirror finding (our wins: gunners d²=10, plant r125) at
league scale.
