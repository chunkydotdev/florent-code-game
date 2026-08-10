# PREREG — LOKI-11: RE-OPEN THE COMMITTED OPENING, ON LIVE TEAMS

**Committed BEFORE submission, activation, and leg creation.** Line `loki`.
Comparator **LOKI-8 = v102 = `bots/_v124loki8`**, the previous line iteration and
the currently live bot, on the **pinned testbed control already fired**
(same 5 maps, same 5-team panel, **denominator /25**).

Platform clock read in the same shell call as this commit — see the commit body.

## The treatment is ONE CONSTANT

    bots/_v128loki11 = bots/_v124loki8 with LOKI2_RUSH_ON: False -> True

`main.py`, `raid.py`, `eco.py` are **byte-identical** to the live bot; the
`doctrine.py` diff is that one line plus its comment. Flipping it waives the
2-harvester prerequisite and cuts the bank floor 40 -> 8 Ti for rounds < 60.

## Why re-open a road that was CLOSED ON REPLICATED EVIDENCE

**The old measurement is not disputed** — 360 paired deterministic games, gate
cleared 12/12, `core_kill_share` **-15.6pp (p=0.020)** on orizon and **-18.9pp
(p=0.003)** on cad, harm concentrated exactly where benefit was predicted. It
replicated. I am not claiming it was mis-run.

**What is disputed is the ARENA.** `orizon` and `cad` are two of the five
self-authored probes carrying the `best_core or best_any` short-circuit, with
turrets welded to the core ray at build time and `rotate()` never called. **Our
forward turrets took ZERO damage across 480 arena games against 46.9% on the
ladder.** A committed opening's entire cost is *raider exposure deep in enemy
ground before the economy exists* — and that is precisely the quantity a fixture
with no forward damage cannot price. The audit this morning put it plainly: the
two fixtures our preregs call "RESOLVING" are the two that cannot see this class
of plank, and a survival plank was once pre-registered against a fixture where
survival is 100% by construction.

**Three things changed under that verdict:**
1. **The fixture.** `FIXTURE_OF_RECORD: live_unrated` (Magnus, today). The old
   verdict has never faced a live team.
2. **The currency.** `R1000_IS_DEFEAT: yes`. The economy the flag protects wins
   games that now count as losses.
3. **The evidence about the field.** The league's fastest killers ARE this
   doctrine: the Bisons plant sentinels **r29-r47** with near-zero economy and
   put **65-68% of titanium into sentinels and ammo** against our **~21%** — and
   beat us **5-0 on this exact pinned testbed**, killing our core in **56, 58,
   65, 69** turns.

**Our own first forward sentinel lands r73-r93** (paired local run, measured
today) **because this flag is False.**

## Bars — QUANTIFIED, because "strictly more" is a rubber stamp

The side lane flagged that a bar cleared by one extra sentinel across 25 games is
noise. Both mechanism bars therefore carry an effect size, stated now:

**MECHANISM A (timing):** median round of our FIRST forward sentinel plant.
Control measures r73-r93 locally. **BAR: median first plant < 60** — inside the
rush window, which is the only thing the constant can do. A treatment that does
not beat 60 has not engaged the mechanism at all.

**MECHANISM B (volume):** mean forward sentinels per game. Control ~1.0.
**BAR: >= 1.8/game**, i.e. the plank must roughly double it. Below that, the
constant moved timing without moving the siege and the leg is weak evidence.

**Either mechanism bar missed -> THE LEG ANSWERED NOTHING about the rush** (D7
shape), and is NOT evidence against it.

**VERDICT (PRIMARY_CURRENCY): `core_kill_share`**, paired by map and opponent
against the pinned control's **/25**. **SECONDARY, reported and never
substituted:** time-to-core-kill against `KILL_WINDOW_RND: 250`, and **their**
kill time against us.

## Falsifier — and the adverse branch is the one I expect

1. **Mechanisms fire, `core_kill_share` flat -> LABELLED NULL.** I write the
   word, and the old arena verdict survives its fixture challenge.
2. **Mechanisms fire, `core_kill_share` DOWN -> the arena was RIGHT.** That is a
   real possible outcome and it would be the most valuable one on offer: it
   would establish that the self-authored fixture agreed with live teams on this
   plank, which is evidence ABOUT THE FIXTURE that we cannot get any other way.
   **I will report it as a vindication of the arena, not bury it.**
3. **Mechanisms fire, `core_kill_share` UP -> the road was closed by a lying
   fixture**, and every other verdict resolved on orizon/cad is suspect. That
   would be the largest finding of the programme and it is exactly why this is
   worth a window.
4. **Their kill time against us gets FASTER** -> the opening bought tempo at the
   cost of our own core. Reported either way; this is the specific harm the
   waived bank floor could cause.

**Pre-committed so it cannot be found convenient:** the old arena effect was
**-15.6 to -18.9pp**. If live-unrated lands anywhere in that band, **the arena
is corroborated and I will say so plainly.** n=25 resolves roughly a 20pp
difference at best, so **this leg cannot detect a small effect and I am not
going to claim one either way** — it is powered only for the large effect the
arena reported.

## Cost, priced before it is paid

`fcode match unrated` plays the **ACTIVE** submission, so this requires
activating LOKI-11: **~6 rated ladder matches/hour of window, so ~2-3 matches**,
each worth roughly +-18 rating. **v102 is re-activated immediately after the
leg.** Rollback target **v102 = submission `ff270a6c`**, live at **1593, k=57,
net_act +25.6, `slot_free` False**. `ship_watch` stays armed on the v102
baseline throughout and the slot rule is untouched by this leg.

## What this leg does NOT test

Facing search (parked as `_v129loki12`, unfired), plant distance (SUSPENDED
pending subject resolution, not refuted), economy suppression, ring-body denial,
launcher kidnap.

---

## ⚠ CORRECTION, MID-LEG — **THE STOP-LOSS CANNOT FIRE DURING THIS WINDOW**

The section above says *"The slot rule is untouched by this leg and `ship_watch`
stays armed on the v102 baseline throughout."* **Both halves are wrong, and the
second is wrong in the dangerous direction.** Flagged by the side lane, verified
here against the source before accepting:

    tools/monitors/ship_watch.py:50   SHIP_BASELINE / SHIP_VERSION are REPORTING-ONLY
    tools/monitors/ship_watch.py:280  "the rule follows whoever the tape says is live"
    tools/slot_rule.py:42             ARM_AFTER = 8
    tools/slot_rule.py:88             armed = (matches - holder_start) >= ARM_AFTER
    elo_history.tsv                   06:25 -> 1590  628  v103   (the tape has flipped)

**`SHIP_VERSION=v102` in the daemon's environment does NOT pin it to v102.** The
rule segments the tape by the live version tag, so a holder change resets the
window: **v103 starts at k=0, and this leg costs ~2-3 rated matches. 3 < 8, so
`armed` is False for the entire window and `slot_free` is False BY CONSTRUCTION.
v103 could lose every rated match in the window and `ship_watch` would log
`RULE=held` throughout.**

**This is the fault its own docstring was written against — *"a stop-loss that
cannot fire is worse than none"* — arriving through the SEGMENTATION rather than
the constants, which is exactly how it arrived last time.** The process is alive
and healthy; the rule is disarmed. **Alive is not working.**

**IT GENERALISES TO EVERY TRICK LEG THIS PROGRAMME WILL FIRE.** The directive
makes live-unrated the fixture of record, `fcode match unrated` plays the ACTIVE
submission, so every prototype leg is a short activation. **Any activation
shorter than 8 rated matches is structurally unprotected by the slot rule.**
That is a permanent property of the instrument under the new method.

### THE ABSOLUTE FLOOR, pre-committed now, while it is still cheap and honest

Since the rolling rule cannot wake up inside a leg, the stop is a fixed number
checked by hand:

    ROLL BACK TO v102 IMMEDIATELY IF RATING < 1550 AT ANY POINT IN THIS WINDOW.

1550 is ~40 below v102's 1590 at handover and ~17 below the 1567.44 activation
baseline v102 has held all night — i.e. **roughly two lost matches' worth of
swing beyond normal noise**, chosen because a single match is +-18 and two
consecutive losses must NOT trip it.

    ROLLBACK: .venv/bin/fcode submission activate 102   # VERSION INT, THEN VERIFY

**The real protection during this window is that command and lane attention, NOT
the slot rule.** A successor reading the original paragraph would have believed
otherwise, which is the reason this correction is written into the prereg rather
than only into the coordination log.
