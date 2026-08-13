# COMBO-MINING SWEEP — missed pairs among shelved arms (2026-08-13, s37)

Produced by an opus subagent at Magnus's ask ("scan old shards… see if
there's any combo we have missed", + "analyse dosage from those"); banked by
the builder. **Status: PRIORITISATION LIST, not verdicts — every number
below must be re-verified at its primary when a prereg cites it** (house
rule; the agent's tables were internally cross-checked but not
builder-re-derived line by line).

**Structural finding first: no existing shard row can discriminate any
pair** — the shard schema carries outcomes only and every screen ran
--replay /dev/null, so every candidate's first step is a kept-replay dosage
run (~3 min, the IDLEPECK pattern). The five v169-era planks (SENTSAFE,
GBNOSHIELD, SCREEN, HEALERFIRST, L4REPAIR) are all UNSHIPPED and need a
port across the 366-line chassis gap before screening.

[Full agent report follows verbatim.]

## RANKED CANDIDATES (agent's findings, condensed; dosage column per Magnus)

**C1. SENTSAFE2 (49.83, n=5408) × GBNOSHIELD (51.02, n=5408)** — sentinel-vs-
gunner class complement on engine physics: barriers stop gunner lines, never
sentinel lines; SENTSAFE's 14/14 redirects were all sentinel-driven,
GBNOSHIELD covers only gunners. Zero shared resources (SENTSAFE is a choice,
not a purchase). Dosage: SENTSAFE dose-CONFIRMED-null (3.4% of builds
redirected, plant count unchanged); GBNOSHIELD local 0.83/game, LIVE DOSE
UNKNOWN (predecessor 0 in 25 live games). Test: port to _v197mapcode, 9-game
dose vs incumbent.

**C2. HEALERFIRST (50.80) × SENTSAFE2 (49.83)** — produce-consume: SENTSAFE
produces surviving forward-turret rounds at zero spend; HEALERFIRST converts
them into denied enemy builder-actions (a healing builder can't build/attack/
move). Dosage: HEALERFIRST dose-CONFIRMED (30 vs 19 builder kills) WITH the
recorded cost that explains its null — own sentinel losses 18 vs 13, i.e. it
lacked exactly what SENTSAFE buys. Hazard for the prereg: SENTSAFE may move
the seat off the healer cluster; column required. Context: NOAPPROACH 18.55%
says forward-turret rounds are the chassis's most load-bearing quantity.

**C3. BURST64B/32B (51.04/50.33) × HEALERFIRST** — BURST's own kill reason
was "the r13-20 window contains no killable target" (1 of 28 builder deaths
across 50 live games); HEALERFIRST manufactures that target class. BURST is
DOSE-UNKNOWN (screened to /dev/null, never dosed) → 9-game wire read of
global_ammo at r13/r17 FIRST; pair dies for 3 minutes if the fill doesn't
land earlier.

**C4. UNDERECO (51.56, OUTSIDE-ABOVE) × L4REPAIR (51.28)** — source+route:
collected = delivery, so a rebuilt harvester with a severed chain scores 0;
UNDERECO restores the source under chronic siege (dose-confirmed ACTIVE on
the rc8.3 wire), L4REPAIR restores the route (dose-confirmed 40/40 repairs,
control 0). NAMED HAZARD: both spend bank in the same phase — the
UNDERECO+TWORAID suppression template — survives only because the chain is
explicit and prices are an order apart. UNDERECO's −11-round flag rides
along. Test: camp-probe games, metric = harvester-rebuild→first-delivery
latency, research's camp_detect/bank_trace.

**C5. APPRLAUNCH (52.8, running, best on board) × GBNOSHIELD** — the ladder
is gunner+feeder; GBNOSHIELD silences the gunner without killing it (no
refund, no scale gift), APPRLAUNCH removes the irreplaceable feeder at 0
ammo. Together the ladder can't regenerate. Test: GBNOSHIELD port onto
_v207, 9 games vs _probe_creeper (the fixture that manufactures ladders).

**C6. SCREEN/SCREEN4 (48.84/48.85, dose-confirmed at 2.57/game, twice
null-negative) × the SALTIDLE idle-gate (+3.57pp over ungated SALT)** —
SCREEN's flat negative with collar/sentinel counts unmoved is the signature
of an action-round price problem; the idle-gate makes exactly that resource
free, and #48's cut says 10.68% of all builder-rounds are parked (TLE=0,
chose-to-idle). Counter-evidence respected: QUIET0/widened-IDLEPECK failed
on SPEND efficiency; a 3 Ti chosen-tile barrier is a different spend. Test:
9 games, does the gate ever open for a screening body?

## REJECTED (the rejections carry the rule)
**R1. APPRLAUNCH × HEALERFIRST** — target competition: both consume the same
40 HP feeder; whichever fires first suppresses the other's dose.
**R2. SCREEN × COLLARVOL** — same bank, same action-rounds, same phase,
shared +1%/barrier scale tax; and COLLARVOL's dose FAILED outright.
**R3. UNDERECO × FWDFLOOR8/MINHARV1** — the measured suppression shape
exactly: one plank withholds bank in the siege phase, the partner exists to
spend it there; both partners negative alone, FWDFLOOR8 dose-unknown.
(Mention: IDLECULL×TWORAID — opposed on bodies; IDLECULL's negative is
intrinsic, a rebuild treadmill, not complement-shaped.)

---

## AXIS 2 (same agent, Magnus's follow-up): old-null × SHIPPED-plank

**S1. SCREEN × the SHIPPED idle-gate** — correction to C6: LOKI_SALTIDLE_ON
already lives in the incumbent (doctrine.py:1575); the pair needs a 123-line
port of SCREEN only, no new machinery. Warning carried: the gate opens 64.6%
of rounds, 92% of its first product was pecking.
**S2. ⭐ x3r0's r0 AMMO PRE-BUY × the salt kill-share chassis** — 5 lines
(_x3r0_v115/main.py:206-211, `rnd==0: convert_ammo` to 17), VERIFIED absent
from the incumbent (v116 reverted it; everything since descends from v116).
LATE160AMMO 53.31/ZEROAMMO 52.90/AMMO115 51.16 all n=5408 — the record's own
amplification example — and the pre-buy has NEVER been screened alone on any
chassis; the two shipgate arms that buried it bundled launcher deletions.
Product (first sentinel volley funded at r13) is worth strictly more on a
kill-share chassis. Cost 17 Ti of 500, action-free, zero bodies/tiles.
**S3. SENTSAFE × shipped GUNAXIS term** — completes a half-built scorer
(theirs: gunner-only for stations; SENTSAFE's dose was 14/14 sentinel-only);
free corpus cut first (gunner- vs sentinel-covered forward deaths, 0.60/game
baseline, ≥0.15 movement bar). Ceiling honest: builder vision r²=20 vs
sentinel r²=32.
**S4. L4REPAIR × SALT** — the fixture CHANGED: on the incumbent, self-play
salts both belts by construction, so L4REPAIR's v169-era null was measured
where no belts died. Free 9-game belt-death cut decides exposure first. ⛔
Carries the #44 CPU blocker (local CPU instrument confirmed dead: 0 on all
6,515 calls).
**Rejections:** RA HEALERFIRST×SALT (same enemy-builder denial resource —
and it BACK-FLAGS C2/C3: HEALERFIRST's 50.80 is a pre-salt UPPER BOUND; its
target-density column must be re-measured on the salt chassis) · RB
idle-round consumers (gate already monetises the round; IDLECULL worse, not
revivable) · RC GUNBORDER (enabler is an unguarded OPPONENT — a live-window
question, not a combo) · RD LAUNCHRES (already harvested into _v207's
conditional). FWDFLOOR8's 45.88 explained: floor 8 undercuts the shipped
12 Ti salt floors.
