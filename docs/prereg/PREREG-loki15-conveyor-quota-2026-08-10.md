# PREREG — LOKI-15: a PER-BUILDER CONVEYOR QUOTA, pre-registered for POOLED windows

**Committed BEFORE submission, activation and leg creation.** Line `loki`.
Platform clock quoted in the commit body.

    bots/_v132loki15 = bots/_v124loki8 (v102) with
        LOKI15_CONV_CAP_ON = True
        LOKI15_CONV_MAX    = 3     # conveyors any ONE builder may lay, lifetime

`main.py` and `raid.py` **byte-identical** to v102 (md5 verified); `eco.py` adds
three helpers and two early-out gates; `doctrine.py` adds the block and the two
constants. Flag off restores parent behaviour exactly.

## Why the dose is a QUOTA and not a cap on the link path

**The obvious lever was measured DEAD before this one was built.** A cap on
link-path length was swept at N = 3/4/5/6 over 54 games per arm and produced
conveyor ratios of **1.08 / 1.09 / 0.94 / 1.01** — *no dose binds*. Two
compensators were visible in the fixture: harvesters built rose 25-50% (a
builder that cannot wire goes digging) and the pave trail re-laid the ground the
refused plans would have covered. **Cutting one SOURCE does not cut conveyors
while another source has spare capacity** — the same class of error that made
LOKI-13 miss. So the shipped flag caps the **quantity, source-agnostically**.

## Why this leg is pre-registered at n=100 PER ARM

Magnus, 2026-08-10: *"You are free to use unrated games as much as you want,
it's a free tool meant to be used."* **Power is now free, so an underpowered leg
is a choice rather than a constraint.** Three legs tonight returned point
estimates that flattered the treatment and failed their own resolution floors;
LOKI-11 went from +16.0pp at n=25 to **+0.0pp at n=50**.

**This leg fires as a PLANNED MULTI-WINDOW POOL: 4 windows, n=100 treatment,
against the pooled control at n=100.** The currency bar is written against that
n from the start and **no currency claim will be made at any smaller n**, even
if an intermediate read looks decisive.

## BAR A — treatment occurrence. Derived from LIVE arithmetic, not a local ratio.

**This is the correction LOKI-13 earned and it is the whole reason this bar is
shaped differently.** LOKI-13's bar came from the flag's own *local* paired-seed
action (0.43-0.67x) and the same flag produced **0.86x live** — a local run is
still a stored figure from the wrong fixture (local games run long and
uncontested; live games are short and contested).

**So this bar rests on arithmetic that transfers rather than on a ratio that
might not:** conveyors/game is bounded above by
`LOKI15_CONV_MAX × builder bots SPAWNED`, by construction. LOKI-13's live arms
spawned **6.92 (control) / 6.68 (treatment)** builders per game.
**3 × 6.92 = 20.8 = 0.54x of the control's 38.66 — under bar before a game is
played.**

**BAR A: conveyors/game <= 23 (<= 0.60x the live control's 38.66).**

**AND THE SPAWN COUNT IS READ FROM THE LEG'S OWN REPLAYS, NOT ASSUMED.** The
ceiling is conditional on it: a long game exercising `REPLACEMENT_MAX` (8) and
`SURGE_EXTRA` (5) over `POP_FLOOR` (5) could spawn 15+ bodies and lift the
ceiling past 23. **Bar A is reported next to measured spawns/game, and if spawns
run high the bar is read against `3 × measured spawns`, stated at the time.**

**Bar A missed -> THE LEG ANSWERED NOTHING**, exactly as LOKI-13.

## BAR B — diagnostic, no threshold

`titanium_collected`, forward sentinels built, **ammo converted / end balance /
shots fired**, harvesters built, builder spawns, our own units lost. Both arms.
(Ammo stays instrumented even though LOKI-13 established it is not our
constraint — conversion 1.10x, end balance 1.60x, shots flat — because this
dose is far larger.)

## VERDICT — PRIMARY_CURRENCY `core_kill_share` at n=100 vs n=100

Reported with its interval, **the per-opponent Δ column MANDATORY**, and the
**seat mix printed per cell**. The panel is known to be a **two-cell instrument**
(The Bisons 0/20 floor, Leviathan and CtrlAltDefeat at ceiling; I Stone and
gsxWins carry all movement) — **so this is a read on I Stone and gsxWins wearing
a five-cell denominator, and it says so here before the data exists.**

## Falsifier

1. **Bar A met, `core_kill_share` flat -> LABELLED NULL**, and the honest
   reading is then strong: **~70% of our economy is removable at no cost to the
   kill**, which is a real finding about what our titanium was buying.
2. **Bar A met, `core_kill_share` DOWN -> the economy WAS funding the kill**, and
   the dose-response is already mapped locally (cap 1 -> 0.11x conveyors and a
   bot that stops working; cap 2 -> 0.21x; cap 3 -> 0.30x; cap 5 -> 0.46x), so
   the follow-up is a retune, not a new plank.
3. **Bar A met, `core_kill_share` UP -> our conveyor economy was actively
   costing us kills.**
4. **Bar A missed -> answered nothing.**

**Pre-committed against convenience:** local win rate was **50/54 = 92.6% for
LOKI-15 against 51/54 = 94.4% for the parent** — i.e. *slightly worse*, on our
own probes, which are not the fixture. **I am recording that before the leg so a
live win cannot be presented as if nothing pointed the other way.**

## Cost

Zero rated exposure, measured: v103 and v104 each played **0** rated ladder
matches across their legs. Procedure: rate-limit wait served with v102 live;
activate only in the instant before firing; **roll back and VERIFY the holder**
(200 retries, `corpus/HOLDER_ALERT` if it never verifies). Absolute floor
**1550**; live rating at writing ~1637, rank #27.
